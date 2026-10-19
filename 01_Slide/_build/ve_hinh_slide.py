"""Vẽ hình nguyên lý cho slide (tiếng Anh).
Chạy: python3 ve_hinh_slide.py   -> ../HinhAnh/Slide2_NguyenLy_EN.png (GPR), ../HinhAnh/Slide2_RD7000_EN.png (RD7000)
"""
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
plt.rcParams.update({"font.family": "Arial", "font.size": 15})
INK, MUTE, EMBER, PIPE, SOIL = "#1B1B1D", "#5F6368", "#E5482D", "#1E7BD9", "#E9DFCC"
v, d = 0.10, 0.5
xs = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
fig, (a, b) = plt.subplots(1, 2, figsize=(13, 4.8), gridspec_kw={"wspace": 0.28})
a.add_patch(Rectangle((-1.6, -1.1), 3.2, 1.1, color=SOIL, zorder=0))
a.axhline(0, color=INK, lw=1.5)
a.add_patch(Circle((0, -d - 0.08), 0.08, color=PIPE, zorder=3))
for x in xs:
    a.add_patch(FancyBboxPatch((x - 0.11, 0.02), 0.22, 0.12, boxstyle="round,pad=0.01", color=EMBER if x == 0 else "#F2A08F", zorder=4))
    a.plot([x, 0], [0, -d], color=EMBER, lw=2.4 if x == 0 else 1.2, alpha=1 if x == 0 else 0.55, zorder=2)
a.annotate("", xy=(1.45, 0.32), xytext=(-1.45, 0.32), arrowprops=dict(arrowstyle="->", color=MUTE, lw=1.5))
a.text(0, 0.40, "antenna moves along the surface", ha="center", color=MUTE)
a.text(0.16, -d - 0.12, "buried pipe", color=PIPE, va="center", fontweight="bold")
a.text(-1.5, -1.0, "soil", color=MUTE)
a.text(0.05, -0.26, "d", color=EMBER, fontweight="bold", fontsize=17)
a.set_xlim(-1.6, 1.6); a.set_ylim(-1.1, 0.6); a.set_aspect("equal"); a.axis("off")
xx = np.linspace(-1.5, 1.5, 300)
b.plot(xx, 2 / v * np.sqrt(xx**2 + d**2), color=INK, lw=2.6)
b.scatter(xs, 2 / v * np.sqrt(xs**2 + d**2), s=70, color=[EMBER if x == 0 else "#F2A08F" for x in xs], zorder=3)
b.annotate("apex  $t_0 = 2d/v$\n→ depth of the pipe", xy=(0, 2 * d / v), xytext=(0.3, 4.5),
           color=EMBER, fontweight="bold", arrowprops=dict(arrowstyle="->", color=EMBER, lw=1.5))
b.set_ylim(36, 0); b.set_xlim(-1.6, 1.6)
b.set_xlabel("antenna position (m)", color=MUTE); b.set_ylabel("two-way travel time (ns)", color=MUTE)
for s in ("top", "right"): b.spines[s].set_visible(False)
b.tick_params(colors=MUTE); b.grid(alpha=0.25)
fig.savefig(Path(__file__).resolve().parent.parent / "HinhAnh" / "Slide2_NguyenLy_EN.png", dpi=200, bbox_inches="tight", facecolor="white")
print("saved")

# ---------------------------------------------------------------- RD7000: peak / null response over a cable
HCM_BLUE = "#0B4A9E"
xr = np.linspace(-1.5, 1.5, 400)
dc = 0.5
bx = dc / (xr**2 + dc**2)          # horizontal field  -> peak coil
bz = xr / (xr**2 + dc**2)          # vertical field    -> null coil
fig, (c1, c2) = plt.subplots(2, 1, figsize=(6.2, 4.6), gridspec_kw={"height_ratios": [1, 1.35], "hspace": 0.12}, sharex=True)
c1.add_patch(Rectangle((-1.6, -1.0), 3.2, 1.0, color=SOIL, zorder=0))
c1.axhline(0, color=INK, lw=1.2)
c1.add_patch(Circle((0, -dc), 0.07, color="#E8590C", zorder=3))
for rr in (0.18, 0.32, 0.46):
    c1.add_patch(Circle((0, -dc), rr, fill=False, ec="#E8590C", lw=1, alpha=0.6, ls="--"))
c1.text(0.12, -dc - 0.02, "  cable with AC current I", color="#E8590C", va="center", fontweight="bold", fontsize=13)
c1.text(-1.5, -0.92, "magnetic field  B = μ₀I / 2πr".replace("₀", "0"), color=MUTE, fontsize=12)
c1.set_ylim(-1.0, 0.1); c1.set_xlim(-1.6, 1.6); c1.axis("off")
c2.plot(xr, bx / bx.max(), color=HCM_BLUE, lw=2.6, label="peak coil (horizontal B)")
c2.plot(xr, bz / np.abs(bz).max(), color=MUTE, lw=2, ls="--", label="null coil (vertical B)")
c2.axvline(0, color="#E8590C", lw=1, alpha=0.6)
c2.axhline(0, color=MUTE, lw=0.8)
c2.set_xlabel("receiver position (m)", color=MUTE)
c2.set_ylabel("signal", color=MUTE)
c2.set_yticks([]); c2.tick_params(colors=MUTE)
for s_ in ("top", "right"): c2.spines[s_].set_visible(False)
c2.legend(loc="lower right", frameon=False, fontsize=12)
c2.text(-1.5, 0.75, "peak = max, null = zero\nright above the cable", color=HCM_BLUE, fontsize=12, fontweight="bold")
fig.savefig(Path(__file__).resolve().parent.parent / "HinhAnh" / "Slide2_RD7000_EN.png", dpi=200, bbox_inches="tight", facecolor="white")
print("saved RD7000")
