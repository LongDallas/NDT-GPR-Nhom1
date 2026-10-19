"""Hình slide 4: cùng một tuyến GPR trước và sau xử lý (chữ tiếng Anh vì slide viết tiếng Anh).

Dữ liệu: LZZ20010.00 = tuyến N5 đo lặp, kênh 250 MHz. Đây là file duy nhất trong
03_DuLieuHienTruong/Data - processed chưa được xử lý (nền chiếm ~90 % tín hiệu, còn lệch DC).
Chuỗi xử lý dùng các hàm trong xu_ly_bscan.py: bỏ DC -> dewow -> xóa nền -> khuếch đại -> khớp hyperbol.

Chạy:  python3 ve_truoc_sau_xu_ly.py   -> 01_Slide/HinhAnh/XuLy_TruocSau.png
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import xu_ly_bscan as xl

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "02_SoDoTuyen_BanDo"))
from doc_reflexw import doc_tuyen  # noqa: E402
import dung_ban_do_3d as bd  # noqa: E402

FILE = GOC / "03_DuLieuHienTruong" / "Data - processed" / "LZZ20010.00T"
RA = GOC / "01_Slide" / "HinhAnh" / "XuLy_TruocSau.png"
V = bd.V_REFLEXW
T_MAX = 30.0
MUC_TIEU = (2.5, 9.0)  # vị trí gần đúng của đỉnh hyperbol ống nước (m, ns)


def xu_ly(b, dt_s):
    b = b - b.mean(axis=0, keepdims=True)   # DC removal (từng vết)
    b = xl.dewow(b, 21)
    b = xl.xoa_nen(b)
    return xl.khuech_dai_sec(b, dt_s, alpha=0.0, mu=1.5)


def ve(ax, b, h, tieu_de):
    i = int(T_MAX / h["dt"]) + 1
    gh = np.percentile(np.abs(b[:i]), 99)
    dai = h["ntr"] * h["dx"]
    ax.imshow(b[:i], cmap="gray", vmin=-gh, vmax=gh, aspect="auto", extent=[0, dai, i * h["dt"], 0],
              interpolation="bilinear")
    ax.set_xlabel("Distance along line N5 (m)", fontsize=11)
    ax.set_ylabel("Two-way travel time (ns)", fontsize=11)
    ax.set_title(tieu_de, fontsize=14, fontweight="bold", loc="left")
    phai = ax.secondary_yaxis("right", functions=(lambda t: V * t / 2, lambda d: 2 * d / V))
    phai.set_ylabel("Depth (m)", fontsize=11)


def main():
    b, h = doc_tuyen(FILE)
    sau = xu_ly(b, h["dt"] * 1e-9)
    x0, t0, v_khop, _ = bd.khop_van_toc(sau, h, *MUC_TIEU)

    fig = plt.figure(figsize=(14, 7.875))
    # chuỗi bước xử lý
    buoc = ["Raw data", "DC removal", "Dewow", "Background\nremoval", "Gain", "Hyperbola\n→ depth"]
    for k, chu in enumerate(buoc):
        x = 0.07 + k * 0.148
        fig.patches.append(FancyBboxPatch((x, 0.86), 0.115, 0.075, boxstyle="round,pad=0.005,rounding_size=0.012",
                                          transform=fig.transFigure, fc="#e7f0fa" if k else "#eeeeee",
                                          ec="#1c5d99" if k else "#888888", lw=1.5))
        fig.text(x + 0.0575, 0.8975, chu, ha="center", va="center", fontsize=11, fontweight="bold",
                 color="#1c3d5a")
        if k < len(buoc) - 1:
            fig.text(x + 0.131, 0.8975, "→", ha="center", va="center", fontsize=20, color="#1c5d99")

    ax1 = fig.add_axes([0.07, 0.12, 0.38, 0.62])
    ax2 = fig.add_axes([0.56, 0.12, 0.38, 0.62])
    ve(ax1, b, h, "Before: raw radargram")
    ve(ax2, sau, h, "After processing")
    dai = h["ntr"] * h["dx"]
    xx = np.linspace(max(x0 - 0.8, 0), min(x0 + 0.8, dai), 200)
    ax2.plot(xx, np.sqrt(t0**2 + (2 * (xx - x0) / V) ** 2), color="#e8590c", lw=2.2)
    for ax in (ax1, ax2):
        ax.set_xlim(0, dai)
    ax2.annotate(f"Water pipe\ndepth to top ≈ {V * t0 / 2:.2f} m",
                 xy=(x0, t0), xytext=(0.25, 21), fontsize=12, fontweight="bold", color="#e8590c",
                 arrowprops=dict(arrowstyle="-|>", color="#e8590c", lw=2),
                 bbox=dict(fc="white", ec="#e8590c", boxstyle="round,pad=0.3"))
    ax2.text(0.98, 0.04, f"hyperbola drawn for v = {V:.3f} m/ns", transform=ax2.transAxes, ha="right", fontsize=10,
             color="#e8590c", bbox=dict(fc="white", ec="none", alpha=0.85))
    ax1.text(0.98, 0.04, "background banding hides\nthe pipe reflection", transform=ax1.transAxes, ha="right",
             fontsize=10, color="0.25", bbox=dict(fc="white", ec="none", alpha=0.85))
    fig.text(0.99, 0.015, "IDS Detector Duo, 250 MHz, line N5 (repeat scan, file LZZ20010.00)", ha="right",
             fontsize=8.5, color="0.45")
    fig.savefig(RA, dpi=150)
    plt.close(fig)
    print(f"Đã lưu {RA}  (đỉnh x = {x0:.2f} m, t = {t0:.2f} ns, sâu {V * t0 / 2:.2f} m; v khớp riêng = {v_khop:.3f})")


if __name__ == "__main__":
    main()
