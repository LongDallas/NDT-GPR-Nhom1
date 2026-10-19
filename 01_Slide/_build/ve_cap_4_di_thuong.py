"""Hình cho slide "4 dị thường trên C1–C4 → đường cáp" (chữ tiếng Anh).

Nguồn: file dữ liệu kênh 250 MHz trong 03_DuLieuHienTruong/New Data/ (LZZ20001–20004 = tuyến C1–C4; đã xử lý trong
ReflexW). Header .##R lấy ở Data - processed/ (file .T giống hệt). LZZ20003.11T là bản XFlip của C3 nên được lật lại.
Vị trí tuyến (chiều đo, điểm xuất phát) theo 02_SoDoTuyen_BanDo/tuyen_do.csv; P1 theo muc_tieu.csv (ten = CAP).
Cáp cắt ngang vuông góc với đường – đúng như 3 dấu nhóm đánh tại hiện trường; C2, C4 (đo ngược) được đặt theo đó.

Chạy:  python3 _build/ve_cap_4_di_thuong.py
Ra:    HinhAnh/Cap_4DiThuong_C1C4.png   (4 radargram xếp theo thứ tự tuyến, cùng trục mặt bằng, đỉnh P1 thẳng cột)
       HinhAnh/Cap_MatBang_C1C4.png     (mặt bằng: 4 tuyến song song cách 1 m, cáp vuông góc đi qua 4 điểm)
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "03_DuLieuHienTruong" / "New Data"
HEADER = ROOT / "03_DuLieuHienTruong" / "Data - processed"
sys.path.insert(0, str(ROOT / "02_SoDoTuyen_BanDo"))
sys.path.insert(0, str(ROOT / "02_SoDoTuyen_BanDo" / "SDT_Tai"))
from doc_reflexw import TRACE_HEADER, doc_header  # noqa: E402
import dung_ban_do_3d as bd  # noqa: E402
import ve_mat_cat_gpr as g  # noqa: E402  (độ sâu theo mô hình 2 lớp của nhóm)

OUT = HERE.parent / "HinhAnh"
CABLE, INK, GREY, BLUE = "#E8590C", "#1B1B1D", "#5F6368", "#0B4A9E"
plt.rcParams.update({"font.family": "Arial", "font.size": 13, "axes.edgecolor": GREY,
                     "xtick.color": GREY, "ytick.color": GREY, "axes.labelcolor": GREY})
T_HIEN = 30.0  # ns hiển thị
X_HIEN = (0.0, 6.0)  # đoạn mặt bằng hiển thị (m dọc đường)


def doc_tuyen():
    """4 tuyến C: B-scan đặt trên trục x mặt bằng (tăng dần), cùng điểm P1 của tuyến đó."""
    p1 = {r["tuyen"]: r for r in bd.doc_csv("muc_tieu.csv") if r["ten"] == "CAP"}
    ds = []
    for r in bd.doc_csv("tuyen_do.csv"):
        if r["nhom"] != "doc_duong":
            continue
        f = next(DATA.glob(r["file_250MHz"][:8] + ".*T"))  # file có trong New Data (C3 là bản .11T)
        h = doc_header(HEADER / (f.stem + f.suffix[:-1] + "R"))
        raw = np.fromfile(f, dtype=np.uint8)
        b = raw.reshape(h["ntr"], TRACE_HEADER + 2 * h["ns"])[:, TRACE_HEADER:].copy().view("<i2").T.astype(np.float32)
        if "XFlipProfile" in h["buoc_xu_ly"]:
            b = b[:, ::-1]  # về lại thứ tự ghi của máy
        x0, x1 = float(r["x_dau"]), float(r["x_cuoi"])
        dai = (h["ntr"] - 1) * h["dx"]
        nguoc = x1 < x0
        if nguoc:
            b = b[:, ::-1]  # đo ngược chiều: lật để trục x mặt bằng tăng dần
        p = p1[r["tuyen"]]
        s, t = float(p["x_tren_tuyen_m"]), float(p["t_ns"])
        ds.append(dict(ten=r["tuyen"], y=float(r["y_dau"]), b=b, h=h, nguoc=nguoc,
                       x_tu=(x0 - dai) if nguoc else x0, dai=dai, x0=x0,
                       px=(x0 - s) if nguoc else (x0 + s), pt=t, sau=float(g.do_sau(t))))
    return ds


def hinh_radargram(ds):
    fig, axs = plt.subplots(len(ds), 1, figsize=(8.6, 7.0), sharex=True, gridspec_kw={"hspace": 0.28})
    for ax, t in zip(axs, ds):
        h = t["h"]
        b = t["b"][: int(round(T_HIEN / h["dt"])) + 1]
        j0, j1 = [int(round((x - t["x_tu"]) / h["dx"])) for x in X_HIEN]
        c = np.percentile(np.abs(b[:, max(j0, 0):j1]), 98.5)
        ax.imshow(b, cmap="gray", vmin=-c, vmax=c, aspect="auto", interpolation="bicubic",
                  extent=[t["x_tu"], t["x_tu"] + t["dai"], b.shape[0] * h["dt"], 0])
        ax.set_ylim(T_HIEN, 0)
        ax.set_xlim(*X_HIEN)
        ax.set_yticks([0, 10, 20, 30])
        ax.set_ylabel("t (ns)", fontsize=11)
        ax.text(0.985, 0.88, f"Line {t['ten']}" + ("  ←" if t["nguoc"] else "  →"), transform=ax.transAxes,
                ha="right", va="top", fontsize=14, fontweight="bold", color="white",
                bbox=dict(boxstyle="round,pad=0.3", fc=BLUE, ec="none"))
        ax.add_patch(Ellipse((t["px"], t["pt"]), 0.45, 7.0, fill=False, ec=CABLE, lw=3))
        ax.text(t["px"] + 0.32, t["pt"] + 1.0, f"P1 · {t['sau']:.2f} m", color="white", fontsize=12.5,
                fontweight="bold", va="center", bbox=dict(boxstyle="round,pad=0.25", fc=CABLE, ec="none"))
    x_cap = np.mean([t["px"] for t in ds])
    for ax in axs:  # đường cáp: cùng một x mặt bằng trên cả 4 tuyến
        ax.axvline(x_cap, color=CABLE, lw=2.2, ls=(0, (4, 3)), zorder=0.5, alpha=0.9)
    axs[-1].set_xlabel("Position along the road (m)")
    fig.savefig(OUT / "Cap_4DiThuong_C1C4.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return x_cap


def hinh_mat_bang(ds, x_cap):
    fig, ax = plt.subplots(figsize=(4.6, 3.6))
    for t in ds:
        a, b = (6.2, 0.6) if t["nguoc"] else (0.6, 6.2)
        ax.annotate("", xy=(b, t["y"]), xytext=(a, t["y"]),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2, mutation_scale=14))
        ax.text(0.45, t["y"], t["ten"], ha="right", va="center", fontsize=14, fontweight="bold", color=BLUE)
    ys = np.array([t["y"] for t in ds])
    ax.plot([x_cap, x_cap], [ys.min() - 0.45, ys.max() + 0.45], color=CABLE, lw=3.2, ls=(0, (4, 2.5)), zorder=3)
    ax.scatter([t["px"] for t in ds], ys, s=150, color=CABLE, ec="white", lw=2, zorder=4)
    for t in ds:
        ax.text(t["px"] + 0.2, t["y"] - 0.12, f"{t['sau']:.2f} m", fontsize=11.5, color=INK, va="bottom")
    ax.annotate("", xy=(6.6, ys[1]), xytext=(6.6, ys[0]), arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.2))
    ax.text(6.72, ys[:2].mean(), "1 m", fontsize=11, color=GREY, va="center")
    ax.text(x_cap + 0.15, ys.max() + 0.5, "cable, 90° to road", color=CABLE, fontsize=13, fontweight="bold", va="top")
    ax.set_xlim(-0.2, 7.2)
    ax.set_ylim(ys.max() + 0.85, ys.min() - 0.55)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(OUT / "Cap_MatBang_C1C4.png", dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    ds = doc_tuyen()
    x_cap = hinh_radargram(ds)
    hinh_mat_bang(ds, x_cap)
    for t in ds:
        print(f"{t['ten']}: P1 ở x mặt bằng {t['px']:.2f} m, sâu {t['sau']:.2f} m")
    print(f"Cáp: x = {x_cap:.2f} m, lệch tối đa {max(abs(t['px'] - x_cap) for t in ds) * 100:.0f} cm")
