"""Vẽ các hình mặt cắt GPR theo mẫu trình bày trong thư mục này (2 ảnh .jpg mẫu).

Vị trí, phân loại dị thường lấy theo bản chú thích của nhóm (03_DuLieuHienTruong/New Data/GPR_chu_thich_duong_ong.pdf),
đã ghi vào ../muc_tieu.csv (cột ky_hieu: P = cáp/kim loại, O = dị thường, A = ống nước).
Hướng tuyến lấy theo ../tuyen_do.csv: C2, C4, N2, N4 đo ngược chiều (zigzag) nên được lật lại khi vẽ,
để khoảng cách trên mọi mặt cắt tính từ cùng một đầu, giống cách nhóm xem trong ReflexW.

Chạy:  python3 ve_mat_cat_gpr.py        -> ket_qua/Hinh1_Cap_MatCatGPR.png, Hinh2_OngNuoc_MatCatGPR.png,
                                           Hinh3_VungTinHieu.png (16:9, dùng thẳng cho slide)
       python3 ve_mat_cat_gpr.py --en   -> cùng các hình, chữ tiếng Anh, tên file thêm đuôi _EN (cho slide tiếng Anh)
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import ConnectionPatch, Rectangle
from scipy.ndimage import gaussian_filter
from scipy.signal import hilbert

THU_MUC = Path(__file__).resolve().parent
sys.path.insert(0, str(THU_MUC.parent))
import dung_ban_do_3d as bd  # noqa: E402

KET_QUA = THU_MUC / "ket_qua"
HINH_SLIDE = bd.HINH_SLIDE
V_BT, V_DAT = 0.12, 0.10  # m/ns: lớp bê tông và đất, theo chú thích của nhóm
T_BT = 5.0  # ns hai chiều trong lớp bê tông (≈ 0,30 m), suy từ bảng độ sâu của nhóm
V_MIG = bd.V_REFLEXW  # 0,095 m/ns – vận tốc nhóm dùng cho Kirchhoff migration trong ReflexW
KENH = "250MHz"
T_MAX = 40.0  # ns hiển thị
MAU_TIEU_DE = "#6f42c1"  # tím, như dòng tiêu đề trên ảnh mẫu
MAU_CHU_THICH = "#3a768a"  # xanh ngọc, như chú thích lớn trên ảnh mẫu
MAU_TEN_TUYEN = "#1f6fb2"
MAU_KY_HIEU = {"P": "#d62828", "O": "#f08c00", "A": "#1c7ed6"}  # màu giống bản chú thích của nhóm
BONG = [pe.withSimplePatchShadow(offset=(1.5, -1.5), alpha=0.35)]
EN = "--en" in sys.argv
DUOI = "_EN" if EN else ""


def chu(vi, en):
    """Chọn chữ theo ngôn ngữ đang vẽ."""
    return en if EN else vi


def do_sau(t):
    """Thời gian hai chiều (ns) -> độ sâu (m): bê tông v = 0,12 tới T_BT, bên dưới là đất v = 0,10."""
    t = np.asarray(t, float)
    return V_BT * np.minimum(t, T_BT) / 2 + V_DAT * np.maximum(t - T_BT, 0) / 2


def thoi_gian(d):
    d = np.asarray(d, float)
    d_bt = V_BT * T_BT / 2
    return np.where(d <= d_bt, 2 * d / V_BT, T_BT + 2 * (d - d_bt) / V_DAT)


def v_rms(t0):
    """Vận tốc trung bình bình phương tới đỉnh hyperbol – dùng để vẽ hyperbol lý thuyết qua 2 lớp."""
    return float(np.sqrt((V_BT**2 * min(t0, T_BT) + V_DAT**2 * max(t0 - T_BT, 0)) / t0))


def lat_chuan(t):
    """Tuyến đo ngược chiều thì lật lại, để x tính từ đầu chuẩn (x = -1,3 m với tuyến C, y = -0,64 m với tuyến N)."""
    t["nguoc"] = bool(t["huong"].sum() < 0)
    if t["nguoc"]:
        t["b"] = t["b"][:, ::-1]
    return t


def tai_du_lieu():
    goc = {t["ten"]: lat_chuan(t) for t in bd.doc_tuyen_do(KENH)}
    mig = {t["ten"]: lat_chuan(t) for t in bd.doc_tuyen_do(KENH, migration=True)}
    return goc, mig


def doc_chu_thich(goc):
    """Các điểm nhóm đã chú thích (dòng có ky_hieu trong ../muc_tieu.csv); x đổi sang chiều hiển thị."""
    ds = {}
    for r in bd.doc_csv("muc_tieu.csv"):
        k = (r.get("ky_hieu") or "").strip()
        if not k or r["kenh"] != KENH:
            continue
        t = goc[r["tuyen"]]
        s = float(r["x_tren_tuyen_m"])
        ds[(r["tuyen"], k)] = dict(ky_hieu=k, ten=r["ten"], tuyen=r["tuyen"], loai=r["loai"], t=float(r["t_ns"]),
                                   x=t["s"][-1] - s if t["nguoc"] else s, xy=bd.vi_tri(t, s))
    return ds


def nhan_diem(m):
    ten = {"cap": chu("cáp", "cable"), "ong_nuoc": chu("ống nước", "water pipe")}.get(m["loai"])
    return f"{m['ky_hieu']} · {ten}" if ten else m["ky_hieu"]


def ve_bscan(ax, t, x_lim=None, t_max=T_MAX, nhan=None, mui_ten=(), hyperbol=None, do_tuong_phan=99.0):
    """Mặt cắt kiểu ReflexW: khoảng cách ở trên, thời gian bên trái, độ sâu bên phải.

    mui_ten: danh sách điểm chú thích (dict từ doc_chu_thich); hyperbol: một điểm chú thích để vẽ hyperbol lý thuyết.
    """
    b, h = t["b"], t["h"]
    dai = t["s"][-1]
    i_max = int(t_max / h["dt"]) + 1
    phan = b[:i_max]
    gh = np.percentile(np.abs(phan[int(8 / h["dt"]):]), do_tuong_phan)
    ax.imshow(phan, cmap="gray", vmin=-gh, vmax=gh, aspect="auto", extent=[0, dai, i_max * h["dt"], 0],
              interpolation="bilinear")
    ax.set_xlim(*(x_lim or (0, dai)))
    ax.set_ylim(t_max, 0)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")
    ax.set_xlabel(chu("Khoảng cách [m]", "Distance [m]"), fontsize=9, labelpad=2)
    ax.set_ylabel(chu("Thời gian [ns]", "Time [ns]"), fontsize=9)
    ax.tick_params(labelsize=8)
    phai = ax.secondary_yaxis("right", functions=(do_sau, thoi_gian))
    phai.set_ylabel(chu("Độ sâu [m]", "Depth [m]"), fontsize=8)
    phai.tick_params(labelsize=8)
    for m in mui_ten:  # mũi tên trắng chỉ lên đỉnh hyperbol, nhãn màu theo loại
        x, tt = m["x"], m["t"]
        ax.annotate("", xy=(x, tt + 1.0), xytext=(x, tt + 8),
                    arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.6", color="white", lw=3.2))
        ax.text(x, tt + 8.6, nhan_diem(m), ha="center", va="top", fontsize=7.5, color="white", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.25", fc=MAU_KY_HIEU[m["ky_hieu"][0]], ec="white", lw=0.8))
    if hyperbol:
        x0, t0 = hyperbol["x"], hyperbol["t"]
        v = v_rms(t0)
        xx = np.linspace(x0 - 0.75, x0 + 0.75, 200)
        ax.plot(xx, np.sqrt(t0**2 + (2 * (xx - x0) / v) ** 2), color="black", lw=1.6)
        ax.text(x0, t0 - 1.5, f"{v:.3f}", ha="center", va="bottom", fontsize=8,
                bbox=dict(fc="white", ec="none", pad=0.5, alpha=0.85))
    if nhan:
        ax.text(0.03, 0.04, nhan, transform=ax.transAxes, fontsize=12, fontweight="bold", va="bottom",
                bbox=dict(fc="white", ec="none", pad=1.5, alpha=0.8))


def duong_ong(goc):
    """Mọi điểm ống nước trong ../muc_tieu.csv (A1 của nhóm + điểm bổ sung trên N4, N5) và đoạn thẳng khớp qua chúng."""
    p = np.array([bd.vi_tri(goc[r["tuyen"]], float(r["x_tren_tuyen_m"]))
                  for r in bd.doc_csv("muc_tieu.csv") if r["loai"] == "ong_nuoc"])
    if len(p) < 2:
        return p, None
    a, b = np.polyfit(p[:, 0], p[:, 1], 1)  # y = a·x + b (ống chạy dọc đường)
    x = np.array([p[:, 0].min(), p[:, 0].max()])
    return p, np.column_stack([x, a * x + b])


def ve_so_do_nho(ax, goc, ct, tuyen_noi_bat):
    """Sơ đồ tuyến thu nhỏ: mũi tên theo chiều kéo máy (tuyen_do.csv), tô đậm tuyến đang trình bày,
    chấm các điểm nhóm đã chú thích và nối các điểm của đường cáp (ten = CAP trong muc_tieu.csv: P1 trên C1–C4,
    cáp cắt ngang vuông góc đường ở x ≈ 2,5 m theo dấu đánh tại hiện trường)."""
    ax.add_patch(Rectangle((0, 0), 10, 3.5, fill=False, ec="#d62828", lw=1.2))
    for t in goc.values():
        if t["nhom"] == "lap":
            continue
        p0, p1 = t["p0"], t["p0"] + t["s"][-1] * t["huong"]
        noi = t["ten"] in tuyen_noi_bat
        mau = "#1f2fa0" if noi else "#adb5bd"
        ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle="-|>", color=mau, lw=2.2 if noi else 1))
        chuan = -t["huong"] if t["nguoc"] else t["huong"]  # nhãn luôn đặt ở đầu chuẩn (trái / trên)
        nhan = (p1 if t["nguoc"] else p0) - 0.4 * chuan
        ax.text(*nhan, t["ten"], fontsize=7, ha="center", va="center", color=mau,
                fontweight="bold" if noi else "normal")
    cap = sorted((m["xy"] for m in ct.values() if m["ten"] == "CAP"), key=lambda p: p[1])
    if cap:
        ax.plot(*np.array(cap).T, color=MAU_KY_HIEU["P"], lw=2.2, zorder=4)
    ong, doan = duong_ong(goc)
    if doan is not None:
        ax.plot(*doan.T, color=MAU_KY_HIEU["A"], lw=2.2, zorder=4)
        ax.plot(*ong.T, "o", ms=4, mfc=MAU_KY_HIEU["A"], mec="white", mew=0.6, zorder=5)
    for m in ct.values():
        ax.plot(*m["xy"], "o", ms=5.5, mfc=MAU_KY_HIEU[m["ky_hieu"][0]], mec="white", mew=0.8, zorder=5)
        if m["ky_hieu"][0] != "P":
            ax.text(m["xy"][0] + 0.18, m["xy"][1] - 0.12, m["ky_hieu"], fontsize=6,
                    color=MAU_KY_HIEU[m["ky_hieu"][0]], fontweight="bold", zorder=6)
    ax.legend(handles=[Line2D([], [], color=MAU_KY_HIEU["P"], lw=2.2, marker="o", ms=4, label=chu("P1: cáp", "P1: cable")),
                       Line2D([], [], color=MAU_KY_HIEU["A"], lw=2.2, marker="o", ms=4,
                              label=chu("ống nước (A1, N4, N5)", "water pipe (A1, N4, N5)")),
                       Line2D([], [], ls="", marker="o", ms=5, mfc=MAU_KY_HIEU["O"], mec="white",
                              label=chu("O: dị thường", "O: anomaly"))],
              loc="upper center", bbox_to_anchor=(0.5, 0.02), ncol=3, fontsize=6.5, frameon=False,
              handletextpad=0.3, columnspacing=1.0)
    ax.set_xlim(-2, 11)
    ax.set_ylim(4.2, -1.3)
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_title(chu("Sơ đồ tuyến (mũi tên: chiều kéo máy; đậm: tuyến trên hình)",
                     "Survey lines (arrow: scan direction; bold: lines shown)"), fontsize=8, color="0.3")


def kich_thuoc(t, x0, t0, rong=0.3, cao=2.5):
    """Kích thước biểu kiến của dị vật trên mặt cắt đã migration: độ rộng tại nửa biên độ bao."""
    b, h = t["b"], t["h"]
    e = gaussian_filter(np.abs(hilbert(b, axis=0)), 1)
    j0, i0 = int(round(x0 / h["dx"])), int(round(t0 / h["dt"]))
    js = slice(max(j0 - int(rong / h["dx"]), 0), j0 + int(rong / h["dx"]) + 1)
    is_ = slice(max(i0 - int(cao / h["dt"]), 0), i0 + int(cao / h["dt"]) + 1)
    o = e[is_, js]
    ii, jj = np.unravel_index(o.argmax(), o.shape)
    hang, cot = o[ii], o[:, jj]
    nua = o[ii, jj] / 2
    trai = jj - np.argmax(hang[:jj + 1][::-1] < nua)
    phai_ = jj + np.argmax(hang[jj:] < nua)
    tren = ii - np.argmax(cot[:ii + 1][::-1] < nua)
    duoi = ii + np.argmax(cot[ii:] < nua)
    x_a, x_b = (js.start + trai) * h["dx"], (js.start + phai_) * h["dx"]
    t_a, t_b = (is_.start + tren) * h["dt"], (is_.start + duoi) * h["dt"]
    return x_a, x_b, t_a, t_b


def ve_kich_thuoc(ax, t, m, nhan):
    x_a, x_b, t_a, t_b = kich_thuoc(t, m["x"], m["t"])
    xc, tc = (x_a + x_b) / 2, (t_a + t_b) / 2
    ve_bscan(ax, t, x_lim=(xc - 0.9, xc + 0.9), t_max=min(tc + 14, T_MAX), nhan=nhan)
    ax.add_patch(Rectangle((x_a, t_a), x_b - x_a, t_b - t_a, fill=False, ec="#e03131", lw=1.6))
    rong_cm = (x_b - x_a) * 100
    cao_cm = float(do_sau(t_b) - do_sau(t_a)) * 100
    ax.annotate("", xy=(x_a, t_b + 1.2), xytext=(x_b, t_b + 1.2), arrowprops=dict(arrowstyle="<->", color="white", lw=1.4))
    ax.annotate("", xy=(x_b + 0.06, t_a), xytext=(x_b + 0.06, t_b), arrowprops=dict(arrowstyle="<->", color="white", lw=1.4))
    ax.text(xc, t_b + 2.2, f"{rong_cm:.0f} cm", color="white", ha="center", va="top", fontsize=9, fontweight="bold",
            path_effects=[pe.withStroke(linewidth=2, foreground="black")])
    ax.text(x_b + 0.1, tc, f"{cao_cm:.0f} cm", color="white", ha="left", va="center", fontsize=9, fontweight="bold",
            path_effects=[pe.withStroke(linewidth=2, foreground="black")])
    lam4 = V_DAT / 0.25 / 4 * 100
    sau = float(do_sau(t_a))
    ax.text(0.97, 0.04, chu(f"sâu tới đỉnh sau migration ≈ {sau:.2f} m\n(kích thước biểu kiến, giới hạn\nđộ phân giải ≈ λ/4 = {lam4:.0f} cm)",
                            f"depth to top after migration ≈ {sau:.2f} m\n(apparent size, limited by\nresolution ≈ λ/4 = {lam4:.0f} cm)"),
            transform=ax.transAxes, ha="right", fontsize=7.5, bbox=dict(fc="white", ec="none", pad=1.5, alpha=0.85))
    return rong_cm, cao_cm, sau


def khung_hinh(tieu_de):
    fig = plt.figure(figsize=(14, 7.875))  # 16:9
    fig.text(0.5, 0.965, tieu_de, ha="center", va="center", fontsize=15, fontweight="bold", color=MAU_TIEU_DE,
             family="serif")
    return fig


def ten_tuyen(fig, ax, chu):
    p = ax.get_position()
    fig.text((p.x0 + p.x1) / 2, p.y0 - 0.045, chu, ha="center", va="top", fontsize=14, fontweight="bold",
             color=MAU_TEN_TUYEN, family="serif")


def chu_thich(fig, x, y, dong, co=17):
    fig.text(x, y, "\n".join(dong), ha="center", va="top", fontsize=co, fontweight="bold", color=MAU_CHU_THICH,
             family="serif", linespacing=1.45, path_effects=BONG)


def chan_trang(fig, sau_mig):
    fig.text(0.99, 0.01, chu(f"GPR IDS Detector Duo, kênh 250 MHz; vị trí và phân loại theo chú thích của nhóm; "
                             f"độ sâu: bê tông v = {V_BT} m/ns (0–{T_BT:.0f} ns), đất v = {V_DAT} m/ns;\n"
                             f"C2, C4, N2, N4 đo ngược chiều nên đã lật; {sau_mig}: Kirchhoff migration (v = {V_MIG}) trong ReflexW",
                             f"GPR IDS Detector Duo, 250 MHz channel; positions and classes from the team's picks; "
                             f"depth: concrete v = {V_BT} m/ns (0–{T_BT:.0f} ns), soil v = {V_DAT} m/ns;\n"
                             f"C2, C4, N2, N4 scanned in reverse and flipped; {sau_mig}: Kirchhoff migration (v = {V_MIG}) in ReflexW"),
             ha="right", va="bottom", fontsize=7, color="0.4", linespacing=1.3)


def hinh_mat_cat(goc, mig, ct, cau_hinh, tieu_de, chu_thich_dong, duong_dan):
    """Bố cục như ảnh mẫu 1: (a) trên-trái, (b) dưới-trái, (c), (d) trên-phải, sơ đồ tuyến + chú thích dưới-phải.

    Mỗi ô: tuyen, ky_hieu (các điểm chú thích cần chỉ), x_lim; ô (a) thêm khop = ký hiệu để vẽ hyperbol.
    """
    fig = khung_hinh(tieu_de)
    ax_a = fig.add_axes([0.06, 0.55, 0.29, 0.33])
    ax_b = fig.add_axes([0.06, 0.09, 0.29, 0.33])
    ax_c = fig.add_axes([0.42, 0.50, 0.23, 0.38])
    ax_d = fig.add_axes([0.75, 0.50, 0.20, 0.38])
    ax_m = fig.add_axes([0.40, 0.07, 0.27, 0.33])
    a, b, c, d = cau_hinh["a"], cau_hinh["b"], cau_hinh["c"], cau_hinh["d"]

    def diem(o):
        return [ct[(o["tuyen"], k)] for k in o.get("ky_hieu", ())]

    ve_bscan(ax_a, goc[a["tuyen"]], x_lim=a.get("x_lim"), nhan="(a)", mui_ten=diem(a),
             hyperbol=ct[(a["tuyen"], a["khop"])])
    ve_bscan(ax_b, goc[b["tuyen"]], x_lim=b.get("x_lim"), nhan="(b)", mui_ten=diem(b))
    if b.get("ghi_chu"):
        ax_b.text(0.5, 0.55, b["ghi_chu"], transform=ax_b.transAxes, ha="center", va="center", fontsize=10,
                  fontweight="bold", color="white", bbox=dict(boxstyle="round,pad=0.4", fc="0.25", ec="white", alpha=0.85))
    ve_bscan(ax_c, mig[c["tuyen"]], x_lim=c.get("x_lim"), nhan="(c)", mui_ten=diem(c))
    md = ct[(d["tuyen"], d["ky_hieu"])]
    if d.get("kieu") == "phong_to":  # sau migration không hội tụ -> chỉ phóng to hyperbol, không đo kích thước
        ve_bscan(ax_d, goc[d["tuyen"]], x_lim=(md["x"] - 0.8, md["x"] + 0.8), t_max=md["t"] + 14, nhan="(d)",
                 mui_ten=[md], hyperbol=md)
        sau = float(do_sau(md["t"]))
        ax_d.text(0.97, 0.04, chu("sâu tới đỉnh", "depth to top") + f" ≈ {sau:.2f} m", transform=ax_d.transAxes,
                  ha="right", fontsize=8, bbox=dict(fc="white", ec="none", pad=1.5, alpha=0.85))
        kq = (np.nan, np.nan, sau)
    else:
        kq = ve_kich_thuoc(ax_d, mig[d["tuyen"]], md, "(d)")
    ten_tuyen(fig, ax_a, chu("Tuyến ", "Line ") + a["tuyen"])
    ten_tuyen(fig, ax_b, chu("Tuyến ", "Line ") + b["tuyen"])
    ve_so_do_nho(ax_m, goc, ct, {a["tuyen"], b["tuyen"], c["tuyen"], d["tuyen"]})
    chu_thich(fig, 0.83, 0.40, chu_thich_dong, co=16)
    chan_trang(fig, "(c)" if d.get("kieu") == "phong_to" else "(c), (d)")
    fig.savefig(duong_dan, dpi=150)
    plt.close(fig)
    return kq


def hinh_vung_tin_hieu(goc, mig, ct, tuyen, ky_hieu, duong_dan):
    """Bố cục như ảnh mẫu 2: (a) trước, (b) sau migration, (c) phóng to vùng tín hiệu quan tâm."""
    fig = khung_hinh(chu(f"XÁC ĐỊNH CÁP NGẦM – VÙNG TÍN HIỆU QUAN TÂM TRÊN TUYẾN {tuyen}",
                         f"LOCATING THE CABLE – SIGNAL OF INTEREST ON LINE {tuyen}"))
    ax_a = fig.add_axes([0.06, 0.45, 0.36, 0.40])
    ax_b = fig.add_axes([0.57, 0.45, 0.36, 0.40])
    t_goc, t_mig = goc[tuyen], mig[tuyen]
    m = ct[(tuyen, ky_hieu)]
    x0, t0 = m["x"], m["t"]
    ve_bscan(ax_a, t_goc)
    ve_bscan(ax_b, t_mig, mui_ten=[m])
    for x, dong in ((0.24, chu("(a) Số liệu đã lọc (dewow, xóa nền, gain)", "(a) Filtered data (dewow, background removal, gain)")),
                    (0.75, chu("(b) Sau Kirchhoff migration", "(b) After Kirchhoff migration"))):
        fig.text(x, 0.375, dong, ha="center", fontsize=13, fontweight="bold", color=MAU_CHU_THICH, family="serif",
                 path_effects=BONG)
    hop = (x0 - 0.8, max(t0 - 6, 0), 1.6, 14)
    ax_a.add_patch(Rectangle(hop[:2], hop[2], hop[3], fill=False, ec="#e03131", lw=2.2))
    ax_c = fig.add_axes([0.43, 0.12, 0.15, 0.22])
    b, h = t_goc["b"], t_goc["h"]
    i_max = int((hop[1] + hop[3]) / h["dt"]) + 1
    gh = np.percentile(np.abs(b[int(8 / h["dt"]):i_max]), 99)
    ax_c.imshow(b[:i_max], cmap="gray", vmin=-gh, vmax=gh, aspect="auto",
                extent=[0, t_goc["s"][-1], i_max * h["dt"], 0], interpolation="bilinear")
    ax_c.set_xlim(hop[0], hop[0] + hop[2])
    ax_c.set_ylim(hop[1] + hop[3], hop[1])
    ax_c.tick_params(labelsize=7)
    for sp in ax_c.spines.values():
        sp.set_edgecolor("#e03131")
        sp.set_linewidth(2)
    fig.add_artist(ConnectionPatch(xyA=(hop[0] + hop[2] / 2, hop[1] + hop[3]), coordsA=ax_a.transData,
                                   xyB=(0.5, 1.0), coordsB=ax_c.transAxes, arrowstyle="-|>", color="#e03131",
                                   lw=2.2, mutation_scale=18))
    fig.text(0.60, 0.23, chu("(c) Vùng tín hiệu\nquan tâm", "(c) Signal of\ninterest"), ha="left", va="center", fontsize=13, fontweight="bold",
             color=MAU_CHU_THICH, family="serif", path_effects=BONG)
    sau = float(do_sau(t0))
    fig.text(0.5, 0.055, chu(f"Mặt cắt GPR tuyến {tuyen} – cáp ngầm ({ky_hieu}) ở x ≈ {x0:.1f} m, sâu tới đỉnh ≈ {sau:.2f} m",
                             f"GPR section, line {tuyen} – cable ({ky_hieu}) at x ≈ {x0:.1f} m, depth to top ≈ {sau:.2f} m"),
             ha="center", fontsize=18, fontweight="bold", color=MAU_CHU_THICH, family="serif", path_effects=BONG)
    fig.text(0.99, 0.01, chu(f"GPR IDS Detector Duo, kênh 250 MHz; độ sâu: bê tông v = {V_BT}, đất v = {V_DAT} m/ns",
                             f"GPR IDS Detector Duo, 250 MHz channel; depth: concrete v = {V_BT}, soil v = {V_DAT} m/ns"),
             ha="right", fontsize=7.5, color="0.4")
    fig.savefig(duong_dan, dpi=150)
    plt.close(fig)


def main():
    KET_QUA.mkdir(exist_ok=True)
    goc, mig = tai_du_lieu()
    ct = doc_chu_thich(goc)
    kq_cap = hinh_mat_cat(
        goc, mig, ct,
        dict(a=dict(tuyen="C1", ky_hieu=("O1", "P1", "O2", "O3"), khop="P1"),
             b=dict(tuyen="C3", x_lim=(0, 6), ky_hieu=("O5", "P1")),
             c=dict(tuyen="C1", x_lim=(0, 6), ky_hieu=("P1",)),
             d=dict(tuyen="C1", ky_hieu="P1")),
        chu("XÁC ĐỊNH CÁP NGẦM BẰNG GPR – TUYẾN DỌC C1–C4", "LOCATING THE BURIED CABLE WITH GPR – LINES C1–C4"),
        chu(["Mặt cắt GPR dò cáp ngầm", "(a) Tuyến C1; (b) Tuyến C3;", "(c) Tuyến C1 sau migration;",
             "(d) Tính kích thước dị vật"],
            ["GPR sections over the cable", "(a) Line C1; (b) Line C3;", "(c) Line C1 after migration;",
             "(d) Apparent size of the target"]),
        KET_QUA / f"Hinh1_Cap_MatCatGPR{DUOI}.png")
    kq_ong = hinh_mat_cat(
        goc, mig, ct,
        dict(a=dict(tuyen="N2", ky_hieu=("A1",), khop="A1"),
             b=dict(tuyen="N1", ghi_chu=chu("Không thấy hyperbol rõ\n(chỉ phản xạ phẳng lớp mặt)",
                                            "No clear hyperbola\n(flat near-surface reflections only)")),
             c=dict(tuyen="N2", ky_hieu=("A1",)),
             d=dict(tuyen="N2", ky_hieu="A1", kieu="phong_to")),
        chu("XÁC ĐỊNH ỐNG NƯỚC BẰNG GPR – TUYẾN NGANG N1–N5", "LOCATING THE WATER PIPE WITH GPR – LINES N1–N5"),
        chu(["Mặt cắt GPR dò ống nước", "(a) Tuyến N2; (b) Tuyến N1;", "(c) Tuyến N2 sau migration;",
             "(d) Phóng to hyperbol ống nước"],
            ["GPR sections over the water pipe", "(a) Line N2; (b) Line N1;", "(c) Line N2 after migration;",
             "(d) Zoom on the pipe hyperbola"]),
        KET_QUA / f"Hinh2_OngNuoc_MatCatGPR{DUOI}.png")
    hinh_vung_tin_hieu(goc, mig, ct, "C1", "P1", KET_QUA / f"Hinh3_VungTinHieu{DUOI}.png")
    for m in sorted(ct.values(), key=lambda m: (m["ky_hieu"], m["tuyen"])):
        print(f"  {m['ky_hieu']:3s} {m['tuyen']}: x trên tuyến {m['x']:5.2f} m, t {m['t']:5.2f} ns, sâu {float(do_sau(m['t'])):.2f} m"
              f"  -> mặt bằng x = {m['xy'][0]:5.2f}, y = {m['xy'][1]:5.2f}")
    print(f"Cáp: kích thước biểu kiến {kq_cap[0]:.0f} × {kq_cap[1]:.0f} cm, sâu {kq_cap[2]:.2f} m")
    print(f"Ống: sâu tới đỉnh {kq_ong[2]:.2f} m (không đo kích thước: sau migration chưa hội tụ)")
    if HINH_SLIDE.is_dir():
        import shutil
        for p in sorted(KET_QUA.glob("Hinh*.png")):
            shutil.copy2(p, HINH_SLIDE / p.name)
    print(f"Đã lưu vào {KET_QUA}")


if __name__ == "__main__":
    main()
