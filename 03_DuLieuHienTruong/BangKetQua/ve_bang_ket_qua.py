# Vẽ bảng kết quả minh giải GPR (song ngữ Việt – Anh) theo mẫu "Ảnh thông tin.jpg".
# Số liệu lấy theo bản chú thích của nhóm (02_SoDoTuyen_BanDo/muc_tieu.csv, ket_qua/muc_tieu_3d.csv).
# Chạy: python3 ve_bang_ket_qua.py  ->  Bang_KetQua_GPR.png
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path

FONT = "Times New Roman"
XANH_O = "#C6EFCE"      # nền ô
TIM = "#7030A0"         # dòng tiêu đề trên cùng
XAM_XANH = "#4F6F7F"    # tên bảng
# màu kí hiệu theo chú giải radargram: P đỏ = cáp/kim loại, A xanh = ống nước, O cam = dị thường
MAU_KH = {"P": "#D00000", "A": "#0055CC", "O": "#E07000"}

# (tiêu đề tiếng Việt, tiếng Anh, độ rộng tương đối)
COT = [
    ("Kí hiệu", "Symbol", 1.0),
    ("Công trình ngầm", "Underground utility", 1.55),
    ("Tuyến đo", "Survey line", 1.15),
    ("Độ sâu tới đỉnh (m)", "Depth to top (m)", 1.55),
    ("Φ (mm)", "Diameter (mm)", 1.05),
]

# ô đầu là kí hiệu; các ô khác: chuỗi, hoặc (tiếng Việt, tiếng Anh). Bảng chỉ trình bày cáp và ống nước.
DONG = [
    ("P1", ("Cáp ngầm", "Buried cable"), "C1 – C4", "0,43 – 0,64 ¹", "≈ 25 ³"),
    ("A1", ("Ống cấp nước", "Water pipe"), "N2, N4², N5²", "0,43 – 0,59", "– *"),
]

GHI_CHU = [
    ("¹ C2–C4: 0,43–0,45 m; C1: 0,64 m. Cáp cắt ngang vuông góc đường tại x ≈ 2,5 m.",
     "C2–C4: 0.43–0.45 m; C1: 0.64 m. The cable crosses the road perpendicularly at x ≈ 2.5 m."),
    ("² Điểm bổ sung trên cùng ống (nhóm chưa chú thích N4, N5).",
     "Supplementary picks on the same pipe (N4, N5 not annotated by the team)."),
    ("³ Theo thông tin của nhóm. Nhỏ hơn λ/4 ≈ 4 cm (700 MHz) nên GPR không đo trực tiếp được.",
     "As given by the team. Below λ/4 ≈ 4 cm (700 MHz), so GPR cannot measure it directly."),
    ("* Khớp hyperbol có bán kính: Φ từ 0 đến ~430 mm khi v đổi ±10 % → GPR chưa xác định được.",
     "Hyperbola fit with radius: Φ ranges 0 to ~430 mm for v ±10 % → not resolved by GPR."),
    ("Độ sâu: bê tông v = 0,12 m/ns, đất v = 0,10 m/ns.",
     "Depth: concrete v = 0.12 m/ns, soil v = 0.10 m/ns."),
]


def o(ax, x, y, w, h):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=XANH_O, edgecolor="black", lw=1.2))


def chu_hai_dong(ax, cx, cy, vi, en, co, dam=False):
    ax.text(cx, cy + 0.17, vi, ha="center", va="center", fontsize=co, family=FONT,
            weight="bold" if dam else "normal")
    ax.text(cx, cy - 0.20, en, ha="center", va="center", fontsize=co - 3.5, family=FONT,
            style="italic", color="#333333", weight="bold" if dam else "normal")


def ve(duong_ra):
    tong_rong = sum(c[2] for c in COT)
    W = 11.0
    don_vi = W / tong_rong
    rong = [c[2] * don_vi for c in COT]
    h_dau, h_dong = 0.85, 0.78
    x0 = 0.6
    H = 2.0 + h_dau + h_dong * len(DONG) + 0.42 * len(GHI_CHU) * 2 + 0.3

    fig, ax = plt.subplots(figsize=((W + 1.2) * 1.0, H * 1.0), dpi=200)
    ax.set_xlim(0, W + 1.2)
    ax.set_ylim(0, H)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    y = H - 0.35
    ax.text(x0 + W / 2, y, "KHẢO SÁT CÁP NGẦM VÀ ỐNG NƯỚC BẰNG RA ĐA XUYÊN ĐẤT (GPR)",
            ha="center", va="center", fontsize=12, family=FONT, weight="bold", color=TIM)
    ax.text(x0 + W / 2, y - 0.32, "Buried cable and water pipe survey by ground-penetrating radar",
            ha="center", va="center", fontsize=10, family=FONT, style="italic", color=TIM)
    y -= 0.95
    ax.text(x0 + W / 2, y, "Bảng 1. Kết quả minh giải số liệu ra đa xuyên đất",
            ha="center", va="center", fontsize=19, family=FONT, weight="bold", color=XAM_XANH)
    ax.text(x0 + W / 2, y - 0.42, "Table 1. Interpretation results of GPR data",
            ha="center", va="center", fontsize=14, family=FONT, weight="bold", style="italic",
            color=XAM_XANH)
    y -= 0.75

    # hàng tiêu đề
    y -= h_dau
    x = x0
    for (vi, en, _), w in zip(COT, rong):
        o(ax, x, y, w, h_dau)
        chu_hai_dong(ax, x + w / 2, y + h_dau / 2, vi, en, 15, dam=True)
        x += w

    # các dòng số liệu
    for dong in DONG:
        y -= h_dong
        x = x0
        for gt, w in zip(dong, rong):
            o(ax, x, y, w, h_dong)
            cx, cy = x + w / 2, y + h_dong / 2
            if x == x0:
                ax.text(cx, cy, gt, ha="center", va="center", fontsize=15, family=FONT,
                        weight="bold", color=MAU_KH[gt[0]])
            elif isinstance(gt, tuple):
                chu_hai_dong(ax, cx, cy, gt[0], gt[1], 15)
            else:
                ax.text(cx, cy, gt, ha="center", va="center", fontsize=15, family=FONT)
            x += w

    # ghi chú
    y -= 0.38
    for vi, en in GHI_CHU:
        ax.text(x0, y, vi, ha="left", va="center", fontsize=10.5, family=FONT)
        ax.text(x0 + 0.17, y - 0.33, en, ha="left", va="center", fontsize=9.5, family=FONT,
                style="italic", color="#444444")
        y -= 0.78

    fig.savefig(duong_ra, bbox_inches="tight", pad_inches=0.15, facecolor="white")
    print("Đã lưu", duong_ra)


if __name__ == "__main__":
    ve(Path(__file__).with_name("Bang_KetQua_GPR.png"))
