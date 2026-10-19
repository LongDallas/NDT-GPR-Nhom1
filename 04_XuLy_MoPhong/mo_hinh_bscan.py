"""Kết quả mô hình: B-scan tổng hợp (mô hình tia) so với mặt cắt đo thực tế.

Mô hình: đất đồng nhất v = 0,095 m/ns (εr ≈ 10), anten 250 MHz (xung Ricker), hai vật tròn:
  - cáp kim loại (hệ số phản xạ Γ = −1),
  - ống PVC chứa không khí (Γ = (√εr − 1)/(√εr + 1) ≈ +0,52)  → hai hyperbol ngược pha.
Thời gian hai chiều tới mặt trên vật: t(x) = (2/v)·(√((x−x0)² + (d+R)²) − R).
Đây là mô hình tia (ray-based), không phải mô phỏng sóng đầy đủ FDTD như gprMax (file gprMax/cap_ngam_2D.in).

Chạy:  python3 mo_hinh_bscan.py   -> 01_Slide/HinhAnh/MoHinh_BScan_EN.png
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "02_SoDoTuyen_BanDo"))
import dung_ban_do_3d as bd  # noqa: E402

V = bd.V_REFLEXW            # m/ns
C0 = 0.2998                 # m/ns
F0 = 0.25                   # GHz (250 MHz)
DT, DX = 0.1, 0.02          # ns, m
T_MAX, X_MAX = 30.0, 3.4    # ns, m
VAT = [  # (tên, x0 [m], độ sâu tới đỉnh d [m], bán kính R [m], Γ)
    ("metal cable", 1.0, 0.45, 0.025, -1.0),
    ("PVC pipe (air-filled)", 2.4, 0.45, 0.055, None),
]
INK, MUTE = "#1B1B1D", "#5F6368"
MAU = {"metal cable": "#E8590C", "PVC pipe (air-filled)": "#1E7BD9"}


def ricker(t, f=F0):
    a = (np.pi * f * t) ** 2
    return (1 - 2 * a) * np.exp(-a)


def bscan_tong_hop(seed=7):
    er = (C0 / V) ** 2
    g_pvc = (np.sqrt(er) - 1) / (np.sqrt(er) + 1)
    t = np.arange(0, T_MAX, DT)
    x = np.arange(0, X_MAX, DX)
    b = np.zeros((t.size, x.size))
    b += 1.5 * ricker(t[:, None] - 1.5)  # sóng trực tiếp + phản xạ mặt đất (giống nhau mọi vết)
    for ten, x0, d, r, g in VAT:
        g = g_pvc if g is None else g
        kc = np.sqrt((x - x0) ** 2 + (d + r) ** 2) - r          # quãng đường một chiều tới mặt vật
        tt = 2 * kc / V
        bup = (d / (kc + r)) ** 2                                # búp sóng anten (cos²)
        bien_do = g * bup * np.exp(-1.2 * kc) / np.maximum(kc, 0.05) * 0.45
        b += bien_do[None, :] * ricker(t[:, None] - tt[None, :])
    b += np.random.default_rng(seed).normal(0, 0.012, b.shape)
    b -= b.mean(axis=1, keepdims=True)                           # xóa nền như khi xử lý dữ liệu thật
    b *= (1 + t[:, None] / 6) ** 1.5                             # khuếch đại theo thời gian
    return t, x, b, g_pvc


def anh(ax, b, x0, x1, t_max, tieu_de, dt):
    gh = np.percentile(np.abs(b[int(4 / dt):int(t_max / dt)]), 99)
    ax.imshow(b, cmap="gray", vmin=-gh, vmax=gh, aspect="auto", extent=[x0, x1, b.shape[0] * dt, 0],
              interpolation="bilinear")
    ax.set_ylim(t_max, 0)
    ax.set_title(tieu_de, loc="left", fontsize=13, fontweight="bold", color=INK)
    ax.set_xlabel("distance [m]", color=MUTE)
    ax.set_ylabel("two-way time [ns]", color=MUTE)
    ax.tick_params(colors=MUTE, labelsize=10)
    phai = ax.secondary_yaxis("right", functions=(lambda tt: V * tt / 2, lambda z: 2 * z / V))
    phai.set_ylabel("depth [m]", color=MUTE)
    phai.tick_params(colors=MUTE, labelsize=10)


def mui_ten(ax, x, t, chu, mau="white"):
    ax.annotate(chu, xy=(x, t + 0.6), xytext=(x, t + 7), ha="center", va="top", color=mau, fontsize=11,
                fontweight="bold", arrowprops=dict(arrowstyle="-|>", color=mau, lw=2.4),
                bbox=dict(fc="black", ec="none", alpha=0.45, pad=1.5))


def main(duong_dan):
    plt.rcParams.update({"font.family": "Arial", "font.size": 12})
    t, x, b, g_pvc = bscan_tong_hop()
    fig = plt.figure(figsize=(14, 6.2))
    gs = fig.add_gridspec(2, 3, width_ratios=[1.25, 1, 1], height_ratios=[0.8, 1.6], wspace=0.42, hspace=0.45)

    ax_g = fig.add_subplot(gs[0, 0])  # (a) hình học mô hình
    ax_g.add_patch(Rectangle((0, -1.1), X_MAX, 1.1, color="#E9DFCC"))
    ax_g.axhline(0, color=INK, lw=1.2)
    for ten, x0, d, r, g in VAT:
        ax_g.add_patch(Circle((x0, -d - r), max(r, 0.04), color=MAU[ten]))
        ax_g.text(x0, -d - 2 * r - 0.1, ten, ha="center", va="top", fontsize=10.5, color=MAU[ten], fontweight="bold")
    ax_g.text(0.05, -1.05, f"soil: v = {V} m/ns (εr ≈ {(C0 / V) ** 2:.0f})", fontsize=10, color=MUTE)
    ax_g.set_xlim(0, X_MAX); ax_g.set_ylim(-1.1, 0.05); ax_g.set_aspect("equal"); ax_g.axis("off")
    ax_g.set_title("(a) Model: two objects 0.45 m deep", loc="left", fontsize=13, fontweight="bold", color=INK)

    ax_m = fig.add_subplot(gs[1, 0])  # (b) B-scan tổng hợp
    anh(ax_m, b, 0, X_MAX, 22, "(b) Synthetic radargram, 250 MHz", DT)
    for ten, x0, d, r, g in VAT:
        mui_ten(ax_m, x0, 2 * d / V, "metal: Γ = −1\n(reversed)" if ten == "metal cable" else f"PVC: Γ ≈ +{g_pvc:.2f}")

    goc = {tt["ten"]: tt for tt in bd.doc_tuyen_do("250MHz")}
    for cot, (ten_tuyen, x0, t0, chu, x_lim) in enumerate([("C1", 3.62, 9.5, "cable", (2.4, 4.8)),
                                                          ("N5", 2.45, 9.5, "water pipe", (1.2, 3.2))]):
        tr = goc[ten_tuyen]
        ax = fig.add_subplot(gs[:, 1 + cot])
        anh(ax, tr["b"], 0, tr["s"][-1], 22, f"({'cd'[cot]}) Field: line {ten_tuyen}", tr["h"]["dt"])
        ax.set_xlim(*x_lim)
        xx = np.linspace(x_lim[0], x_lim[1], 200)
        ax.plot(xx, 2 / V * np.sqrt((xx - x0) ** 2 + (V * t0 / 2) ** 2), color="#C9A227", lw=2, ls="--")
        mui_ten(ax, x0, t0, chu)
    fig.text(0.99, 0.005, "Ray-based model (not full-wave FDTD). Dashed gold curve: hyperbola for v = 0.095 m/ns, "
             "top at 0.45 m. Field data: IDS Detector Duo, 250 MHz.", ha="right", fontsize=9.5, color=MUTE)
    fig.savefig(duong_dan, dpi=170, bbox_inches="tight", facecolor="white")
    print("Đã lưu", duong_dan, f"(Γ_PVC = {g_pvc:.2f})")


if __name__ == "__main__":
    main(GOC / "01_Slide" / "HinhAnh" / "MoHinh_BScan_EN.png")
