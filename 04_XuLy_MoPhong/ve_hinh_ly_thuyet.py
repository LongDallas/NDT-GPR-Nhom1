"""Vẽ các hình lý thuyết của Chương 2 (tính trực tiếp từ công thức, in đen trắng được).

    python ve_hinh_ly_thuyet.py   -> lưu vào ../01_Slide/HinhAnh/

Hình 2.2: đường hyperbol thời gian truyền hai chiều t(x) của vật hình trụ, với ba vận tốc.
(Hàm hinh_peak_null() thuộc bản có RD7000 – không còn dùng trong báo cáo chỉ GPR.)
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RA = Path(__file__).resolve().parent.parent / "01_Slide" / "HinhAnh"
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "0.88", "grid.linewidth": 0.6,
})


def hinh_hyperbol():
    x = np.linspace(-1.5, 1.5, 400)
    d, R = 0.5, 0.05  # độ sâu tới đỉnh (m), bán kính (m)
    kieu = [(0.06, "-", "v = 0,06 m/ns (đất sét ẩm, εr ≈ 25)"),
            (0.10, "--", "v = 0,10 m/ns (cát ẩm, εr ≈ 9)"),
            (0.15, ":", "v = 0,15 m/ns (cát khô, εr ≈ 4)")]
    fig, ax = plt.subplots(figsize=(6.0, 3.4), dpi=200)
    for v, ls, nhan in kieu:
        t = 2 / v * np.sqrt(x**2 + (d + R) ** 2) - 2 * R / v
        ax.plot(x, t, color="black", lw=1.6, ls=ls, label=nhan)
    ax.invert_yaxis()
    ax.annotate("đỉnh hyperbol\n$t_0$ = 2d/v", xy=(0, 2 * d / 0.10), xytext=(0.35, 4.0),
                fontsize=9, arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.set_xlabel("Vị trí anten so với đỉnh vật, $x - x_0$ (m)")
    ax.set_ylabel("Thời gian hai chiều t (ns)")
    ax.legend(loc="lower center", fontsize=8.5, frameon=False)
    fig.tight_layout()
    fig.savefig(RA / "Hinh2_2_hyperbol_van_toc.png")
    plt.close(fig)


def hinh_peak_null():
    d = 1.0  # độ sâu dây dẫn (m)
    x = np.linspace(-3, 3, 601)
    peak = d**2 / (d**2 + x**2)               # thành phần ngang, chuẩn hóa
    null = 2 * np.abs(x) * d / (d**2 + x**2)  # thành phần đứng, chuẩn hóa
    fig, ax = plt.subplots(figsize=(6.0, 3.4), dpi=200)
    ax.plot(x, peak, color="black", lw=1.6, ls="-", label="Cuộn ngang – chế độ Peak")
    ax.plot(x, null, color="black", lw=1.6, ls="--", label="Cuộn đứng – chế độ Null")
    ax.annotate("", xy=(-d, 0.5), xytext=(d, 0.5), arrowprops=dict(arrowstyle="<->", lw=0.8))
    ax.text(0, 0.53, "độ rộng tại 50 % = 2d", ha="center", fontsize=9,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
    ax.annotate("Null = 0 ngay trên dây", xy=(0, 0), xytext=(0.9, 0.12), fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.set_xlabel("Khoảng cách ngang tới trục dây dẫn, x (m)   [d = 1 m]")
    ax.set_ylabel("Tín hiệu chuẩn hóa")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=8.5, frameon=False)
    fig.tight_layout()
    fig.savefig(RA / "Hinh2_1_peak_null.png")
    plt.close(fig)


if __name__ == "__main__":
    RA.mkdir(parents=True, exist_ok=True)
    hinh_hyperbol()
    print("Đã lưu:", *sorted(p.name for p in RA.glob("*.png")))
