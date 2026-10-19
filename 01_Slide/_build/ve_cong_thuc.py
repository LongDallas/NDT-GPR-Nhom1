"""Vẽ công thức cho slide 3.1 (nguyên lý GPR) thành ảnh PNG nền trong, kiểu LaTeX (matplotlib mathtext).

Mọi công thức vẽ cùng cỡ chữ và cùng DPI, nên khi đặt lên slide với kích thước = pixel / DPI
thì chữ trong các công thức to bằng nhau.
Cách dùng: python3 ve_cong_thuc.py  → ghi HinhAnh/CongThuc_GPR_1.png … _5.png
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "HinhAnh"
DPI = 300
SIZE = 30  # pt; tao_seminar.js thu nhỏ đồng loạt nếu cần
INK = "#1B1B1D"

plt.rcParams["mathtext.fontset"] = "cm"

CONG_THUC = {
    1: r"$v=\dfrac{c}{\sqrt{\varepsilon_r}}$",
    2: r"$d=\dfrac{v\,t}{2}$",
    3: r"$R=\dfrac{\sqrt{\varepsilon_1}-\sqrt{\varepsilon_2}}{\sqrt{\varepsilon_1}+\sqrt{\varepsilon_2}}$",
    4: r"$t(x)=\dfrac{2}{v}\sqrt{d^{2}+(x-x_0)^{2}}$",
    5: r"$\Delta z\approx\dfrac{\lambda}{4}=\dfrac{v}{4f}$",
}

for i, tex in CONG_THUC.items():
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, tex, fontsize=SIZE, color=INK)
    path = OUT / f"CongThuc_GPR_{i}.png"
    fig.savefig(path, dpi=DPI, transparent=True, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print("wrote", path.name)
