"""Dựng 1 bản đồ chung (2D + 3D) cho ống nước và cáp ngầm từ các tuyến GPR đã xử lý bằng ReflexW.

Cách dùng (chạy trong thư mục 02_SoDoTuyen_BanDo):
    python3 dung_ban_do_3d.py                  # độ sâu theo mô hình 2 lớp của nhóm, khối 3D từ dữ liệu migration 700 MHz
    python3 dung_ban_do_3d.py --v 0.095        # một vận tốc cho mọi độ sâu (0,095 = vận tốc migration trong ReflexW)
    python3 dung_ban_do_3d.py --v 0            # một vận tốc, tự ước lượng bằng khớp hyperbol
    python3 dung_ban_do_3d.py --khoi goc       # khối 3D từ dữ liệu chưa migration
    python3 dung_ban_do_3d.py --kenh 250MHz    # khối 3D từ kênh 250 MHz

Đầu vào:
    tuyen_do.csv     vị trí đầu/cuối từng tuyến (m) theo ảnh sơ đồ bố trí tuyến trong "Ảnh hiện trường/"
    muc_tieu.csv     đỉnh hyperbol đã chọn; cùng `ten` = cùng một ống/cáp -> nối thành đường;
                     cột do_sau_nhom_m (nếu có) = độ sâu nhóm đọc trong bản chú thích, được dùng thay độ sâu tính lại
    diem_rd7000.csv  điểm RD7000 (x, y, độ sâu) để đối chiếu, có thể để trống
Độ sâu (mặc định): mô hình 2 lớp theo bản chú thích của nhóm (New Data/GPR_chu_thich_duong_ong.pdf):
    v = 0,12 m/ns trong lớp bê tông (5 ns đầu, ≈ 0,30 m), v = 0,10 m/ns trong đất bên dưới.
Hệ tọa độ: x dọc đường, y ngang đường; gốc = góc khung khảo sát 10 m x 3,5 m ở đầu có nhãn C1–C4, mép phía nhà.
Tuyến nhóm "lap" (đo lặp) chỉ dùng để lấy điểm mục tiêu, không vẽ và không đưa vào khối 3D.
Đầu ra (ket_qua/):
    BanDo_OngNuoc_Cap.png    bản đồ chung: ảnh IMG_9558 có chồng ống/cáp + mặt bằng theo mét
    KetQua_IMG_9558.jpg      ống + cáp vẽ lên ảnh hiện trường (qua ve_so_do_anh.py)
    Canh3D_HienTruong.html   cảnh 3D tương tác: mặt đất = ảnh IMG_9558, máy GPR chạy tuyến, bấm ống/cáp xem thông số
Chữ trên hình và trang 3D viết tiếng Anh vì slide viết tiếng Anh.
    BanDo3D_OngNuoc_Cap.html mô hình 3D tương tác (mở bằng trình duyệt, cần Internet để tải plotly.js)
    LatCat_DoSau.png         lát cắt ngang theo độ sâu (C-scan)
    muc_tieu_3d.csv          tọa độ x, y, độ sâu của từng điểm ống/cáp
    muc_tieu_tu_dong.csv     đỉnh hyperbol do script tự tìm (gợi ý để bổ sung vào muc_tieu.csv)
"""
import argparse
import csv
import json
import shutil
import warnings
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from scipy.interpolate import LinearNDInterpolator
from scipy.ndimage import gaussian_filter, uniform_filter1d
from scipy.signal import find_peaks, hilbert
from scipy.spatial import cKDTree

from doc_reflexw import doc_tuyen
import ve_so_do_anh as anh_hien_truong
import canh_3d

warnings.filterwarnings("ignore", "Mean of empty slice")  # ô lưới nằm ngoài vùng có tuyến đo

THU_MUC = Path(__file__).resolve().parent
DU_LIEU = THU_MUC.parent / "03_DuLieuHienTruong" / "Data - processed"
DU_LIEU_MIG = THU_MUC.parent / "03_DuLieuHienTruong" / "SaoLuu" / "Data_backup_migration"  # Kirchhoff, v = 0,095
V_REFLEXW = 0.095  # m/ns, vận tốc nhóm dùng cho Kirchhoff migration trong ReflexW (đọc từ header .00R)
V_BT, V_DAT, T_BT = 0.12, 0.10, 5.0  # mô hình 2 lớp của nhóm: bê tông 5 ns đầu (≈ 0,30 m), đất bên dưới
V_DON = None  # m/ns; đặt bằng --v để dùng một vận tốc cho mọi độ sâu thay cho mô hình 2 lớp
KET_QUA = THU_MUC / "ket_qua"
HINH_SLIDE = THU_MUC.parent / "01_Slide" / "HinhAnh"  # hình cho slide được chép sang đây sau mỗi lần chạy
KENH = ("700MHz", "250MHz")
CAT_DAU_NS = {"700MHz": 6.0, "250MHz": 7.0}  # bỏ sóng trực tiếp ở đầu vết
MAU_LOAI = {"ong_nuoc": "#1c7ed6", "cap": "#e8590c", "khac": "#868e96"}
TEN_LOAI = {"ong_nuoc": "Water pipe", "cap": "Power cable", "khac": "Unidentified reflector"}  # chữ trên hình: tiếng Anh (slide)
MAU_TUYEN = {"doc_duong": "#fab005", "cat_ngang": "#40c057"}  # giống màu vạch trên ảnh
PLOTLY_CDN = "https://cdn.jsdelivr.net/npm/plotly.js-dist-min@2.35.2/plotly.min.js"


# ---------------------------------------------------------------- đọc cấu hình
def doc_csv(ten):
    p = THU_MUC / ten
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8-sig") as f:
        return [r for r in csv.DictReader(f) if any(v.strip() for v in r.values() if v)]


def doc_tuyen_do(kenh, migration=False):
    """Đọc các tuyến theo tuyen_do.csv; migration=True lấy bản .00 đã Kirchhoff migration cùng tên."""
    tuyen = []
    for r in doc_csv("tuyen_do.csv"):
        if migration:
            b, h = doc_tuyen(DU_LIEU_MIG / (r[f"file_{kenh}"][:8] + ".00T"))
        else:
            b, h = doc_tuyen(DU_LIEU / r[f"file_{kenh}"])
        if not migration and r.get("xu_ly_them", "").strip() == "nen":
            b = b - uniform_filter1d(b, 31, axis=0)  # dewow
            b = b - b.mean(axis=1, keepdims=True)  # xóa nền
        p0 = np.array([float(r["x_dau"]), float(r["y_dau"])])
        p1 = np.array([float(r["x_cuoi"]), float(r["y_cuoi"])])
        s = np.arange(h["ntr"]) * h["dx"]  # khoảng cách dọc tuyến; chiều dài lấy theo dữ liệu
        huong = (p1 - p0) / np.linalg.norm(p1 - p0)
        tuyen.append(dict(ten=r["tuyen"], nhom=r["nhom"], b=b, h=h, p0=p0, huong=huong, s=s,
                          xy=p0 + s[:, None] * huong))
    return tuyen


def vi_tri(t, x_tren_tuyen):
    return t["p0"] + float(x_tren_tuyen) * t["huong"]


def do_sau(t):
    """Thời gian hai chiều (ns) -> độ sâu (m)."""
    t = np.asarray(t, float)
    if V_DON:
        return V_DON * t / 2
    return V_BT * np.minimum(t, T_BT) / 2 + V_DAT * np.maximum(t - T_BT, 0) / 2


def thoi_gian(z):
    """Độ sâu (m) -> thời gian hai chiều (ns), ngược với do_sau()."""
    z = np.asarray(z, float)
    if V_DON:
        return 2 * z / V_DON
    z_bt = V_BT * T_BT / 2
    return np.where(z <= z_bt, 2 * z / V_BT, T_BT + 2 * (z - z_bt) / V_DAT)


def mo_ta_do_sau():
    """Một câu tiếng Anh cho chân hình."""
    if V_DON:
        return f"Depth from two-way travel time, v = {V_DON:.3f} m/ns."
    return f"Depth: v = {V_BT:.2f} m/ns in concrete (top {V_BT * T_BT / 2:.2f} m), {V_DAT:.2f} m/ns in soil."


# ---------------------------------------------------------------- vận tốc & mục tiêu
def khop_van_toc(b, h, x0, t0, ban_rong=0.5):
    """Tinh chỉnh đỉnh (x0, t0) rồi quét v để cực đại semblance dọc hyperbol điểm."""
    dx, dt = h["dx"], h["dt"]
    j0, i0 = int(round(x0 / dx)), int(round(t0 / dt))
    j_a, i_a = max(j0 - 5, 0), max(i0 - 8, 0)
    o = np.abs(b[i_a:i0 + 8, j_a:j0 + 6])
    ii, jj = np.unravel_index(o.argmax(), o.shape)
    i0, j0 = i_a + ii, j_a + jj
    t0 = i0 * dt
    js = np.arange(max(j0 - int(ban_rong / dx), 0), min(j0 + int(ban_rong / dx), b.shape[1] - 1) + 1)
    tot = (-1.0, np.nan)
    for v in np.arange(0.05, 0.2001, 0.0025):
        k = np.round(np.sqrt(t0**2 + (2 * (js - j0) * dx / v) ** 2) / dt).astype(int)
        ok = k < b.shape[0] - 3
        cua_so = np.stack([b[k[ok] + d, js[ok]] for d in range(-2, 3)])
        s = (cua_so.sum(1) ** 2).sum() / (ok.sum() * (cua_so**2).sum() + 1e-9)
        tot = max(tot, (s, v))
    return j0 * dx, t0, tot[1], tot[0]


def tim_dinh_hyperbol(t, kenh, nguong=20.0):
    """Gợi ý đỉnh hyperbol: cực đại bao biên độ nổi bật so với trung vị của tuyến."""
    b, h = t["b"], t["h"]
    e = gaussian_filter(np.abs(hilbert(b, axis=0)), 2)
    i0, i1 = int((CAT_DAU_NS[kenh] + 1) / h["dt"]), int(60 / h["dt"])
    w = e[i0:i1] / np.median(e[i0:i1])
    hs = w.max(axis=0)
    dinh, _ = find_peaks(hs, height=nguong, distance=int(0.5 / h["dx"]))
    return [(j * h["dx"], (i0 + w[:, j].argmax()) * h["dt"], hs[j]) for j in dinh]


def duong_ong_cap(muc_tieu, x_lim, y_lim):
    """Nối các điểm cùng tên thành đường thẳng (khớp PCA).

    Trả về {ten: dict(loai, diem, quan_sat, du_doan)}; `quan_sat` là đoạn giữa hai điểm đo xa nhất,
    `du_doan` là đoạn kéo dài thẳng tới mép vùng khảo sát (chỉ là dự đoán).
    """
    ket_qua = {}
    for m in muc_tieu:
        ket_qua.setdefault(m["ten"], dict(loai=m["loai"], diem=[]))["diem"].append(m)
    for ten, d in ket_qua.items():
        p = np.array([[m["x"], m["y"], m["z"]] for m in d["diem"]])
        if len(p) < 2:
            d["quan_sat"] = d["du_doan"] = None
            continue
        tam = p.mean(0)
        huong = np.linalg.svd(p[:, :2] - tam[:2])[2][0]
        u = (p[:, :2] - tam[:2]) @ huong
        d["diem"] = [d["diem"][i] for i in np.argsort(u)]
        u_sap, z_sap = np.sort(u), p[np.argsort(u), 2]
        # giới hạn kéo dài: điểm mà đường thẳng chạm mép khung x_lim/y_lim
        han = []
        for k, (lo, hi) in enumerate((x_lim, y_lim)):
            if abs(huong[k]) > 1e-6:
                han += sorted(((lo - tam[k]) / huong[k], (hi - tam[k]) / huong[k]))
        u_min = max(han[0::2]) if han else u_sap[0]
        u_max = min(han[1::2]) if han else u_sap[-1]

        def diem(uu):
            uu = np.asarray(uu, float)
            xy = tam[:2] + uu[:, None] * huong
            return np.column_stack([xy, np.interp(uu, u_sap, z_sap)])  # độ sâu giữ nguyên ngoài đoạn đo

        d["quan_sat"] = diem(np.linspace(u_sap[0], u_sap[-1], 20))
        d["du_doan"] = [diem([u_min, u_sap[0]]), diem([u_sap[-1], u_max])]
    return ket_qua


# ---------------------------------------------------------------- khối 3D
def bao_bien_do(t, kenh, v, z):
    """Bao biên độ (envelope) chuẩn hóa, nội suy từ thời gian sang độ sâu z (m)."""
    b, h = t["b"], t["h"]
    e = np.abs(hilbert(b, axis=0))
    tt = np.arange(h["ns"]) * h["dt"]
    e[tt < CAT_DAU_NS[kenh]] = 0
    e = gaussian_filter(e, (1.5, 1.0))
    e /= np.percentile(e[tt >= CAT_DAU_NS[kenh]], 99.5) + 1e-9
    t_z = thoi_gian(z)
    return np.array([np.interp(t_z, tt, e[:, j]) for j in range(h["ntr"])])  # [vết, z]


def dung_khoi(tuyen, kenh, v, z, buoc_xy, xa_nhat=0.55):
    """Nội suy khối 3D; bỏ (NaN) các ô cách vết đo gần nhất quá `xa_nhat` m."""
    xy = np.vstack([t["xy"] for t in tuyen])
    gia_tri = np.vstack([bao_bien_do(t, kenh, v, z) for t in tuyen])
    lo, hi = xy.min(0), xy.max(0)
    gx = np.arange(lo[0], hi[0] + 1e-6, buoc_xy)
    gy = np.arange(lo[1], hi[1] + 1e-6, buoc_xy)
    X, Y = np.meshgrid(gx, gy, indexing="ij")
    o = np.column_stack([X.ravel(), Y.ravel()])
    khoi = LinearNDInterpolator(xy, gia_tri, fill_value=np.nan)(o)
    khoi[cKDTree(xy).query(o)[0] > xa_nhat] = np.nan
    return gx, gy, khoi.reshape(len(gx), len(gy), len(z))


# ---------------------------------------------------------------- hình 2D
def ve_lat_cat(gx, gy, z, khoi, tuyen, duong, z_dau, tieu_de, duong_dan):
    do_sau = np.linspace(z_dau, 1.2, 8)
    fig, axs = plt.subplots(4, 2, figsize=(14, 12), sharex=True, sharey=True, layout="constrained")
    for ax, d in zip(axs.flat, do_sau):
        k = np.argmin(np.abs(z - d))
        lop = np.nanmean(khoi[:, :, max(k - 2, 0):k + 3], axis=2)
        anh = ax.imshow(lop.T, origin="lower", extent=[gx[0], gx[-1], gy[0], gy[-1]], cmap="inferno",
                        vmin=0, vmax=1, aspect="equal", interpolation="bilinear")
        for t in tuyen:
            ax.plot(t["xy"][:, 0], t["xy"][:, 1], color="white", lw=0.4, alpha=0.5)
        for dd in duong.values():
            for m in dd["diem"]:
                if abs(m["z"] - d) < 0.1:
                    ax.plot(m["x"], m["y"], "o", mfc="none", mec=MAU_LOAI[dd["loai"]], mew=1.5, ms=8)
        ax.set_title(f"depth {d:.2f} m", fontsize=9, loc="left")
    fig.colorbar(anh, ax=axs, shrink=0.5, label="envelope amplitude (normalised)")
    fig.suptitle(tieu_de + " – depth slices (circles: pipe/cable picks within ±0.1 m)")
    for ax in axs[-1]:
        ax.set_xlabel("x – along the road (m)")
    for ax in axs[:, 0]:
        ax.set_ylabel("y – across (m)")
    fig.savefig(duong_dan, dpi=120)
    plt.close(fig)


def ve_duong(ax, duong, f=lambda x, y: (x, y), chu=True):
    for d in duong.values():
        mau = MAU_LOAI[d["loai"]]
        lech = {"ong_nuoc": (6, 6), "cap": (8, 7)}.get(d["loai"], (5, 5))  # tránh chữ chồng nhau
        if d["quan_sat"] is not None:
            for doan in d["du_doan"]:
                ax.plot(*f(doan[:, 0], doan[:, 1]), color=mau, lw=3, ls=(0, (2, 1.5)), alpha=0.8)
            ax.plot(*f(d["quan_sat"][:, 0], d["quan_sat"][:, 1]), color=mau, lw=4.5, solid_capstyle="round")
        da_ghi = []
        for m in d["diem"]:
            px, py = f(m["x"], m["y"])
            ax.plot(px, py, "o", color=mau, mec="white", mew=1.2, ms=8 if d["loai"] != "khac" else 6, zorder=5)
            if chu and all(np.hypot(m["x"] - x, m["y"] - y) > 0.3 for x, y in da_ghi):  # bỏ nhãn lần đo lặp
                da_ghi.append((m["x"], m["y"]))
                ax.annotate(f"{m['z']:.2f} m", (px, py), xytext=lech, textcoords="offset points",
                            fontsize=8, color=mau, fontweight="bold")


def ve_ban_do(tuyen, duong, rd, v, duong_dan):
    f_anh = anh_hien_truong.px if anh_hien_truong.ANH.exists() else None
    fig = plt.figure(figsize=(17, 6.3), layout="constrained")
    if f_anh:
        gs = fig.add_gridspec(1, 2, width_ratios=[1, 2.7])
        ax_anh, ax = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
        anh = mpimg.imread(anh_hien_truong.ANH)
        ax_anh.imshow(anh)
        ve_duong(ax_anh, duong, f_anh, chu=False)
        ax_anh.set_xlim(0, anh.shape[1])
        ax_anh.set_ylim(anh.shape[0], 500)
        ax_anh.set_axis_off()
        ax_anh.set_title("Site photo (top view)\nblue: water pipe; orange: power cable", fontsize=10)
    else:
        ax = fig.add_subplot()
    for t in tuyen:
        mau = MAU_TUYEN.get(t["nhom"], "0.6")
        ax.plot(t["xy"][:, 0], t["xy"][:, 1], color=mau, lw=2, alpha=0.9, zorder=1)
        ax.annotate("", xy=t["xy"][-1], xytext=t["xy"][-8], arrowprops=dict(arrowstyle="-|>", color=mau, lw=1.5))
        dau = t["xy"][0] - 0.25 * t["huong"]
        ax.text(*dau, t["ten"], fontsize=8, ha="center", va="center", color="0.25")
    ve_duong(ax, duong)
    for p in rd:
        ax.plot(p["x"], p["y"], "^", color="#2b8a3e", ms=9, mec="white", zorder=6)
        ax.annotate(f"{p['diem']} {p['z']:.2f} m", (p["x"], p["y"]), xytext=(5, -10), textcoords="offset points",
                    fontsize=8, color="#2b8a3e")
    ax.plot([], [], color=MAU_LOAI["ong_nuoc"], lw=4.5, label="Water pipe (measured)")
    ax.plot([], [], color=MAU_LOAI["cap"], lw=4.5, label="Power cable (measured)")
    ax.plot([], [], color="0.4", lw=3, ls=(0, (2, 1.5)), label="Straight extension (not measured)")
    ax.plot([], [], "o", color=MAU_LOAI["khac"], label="Unidentified reflector (one line)")
    ax.plot([], [], color=MAU_TUYEN["doc_duong"], lw=2, label="Lines C1–C4 along the road")
    ax.plot([], [], color=MAU_TUYEN["cat_ngang"], lw=2, label="Lines N1–N5 across the road")
    ax.add_patch(plt.Rectangle((0, 0), 10, 3.5, fill=False, ec="#e03131", lw=1.5, zorder=0,
                               label="Survey area 10 m × 3.5 m"))
    if rd:
        ax.plot([], [], "^", color="#2b8a3e", label="RD7000 point")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), fontsize=8, ncol=4, frameon=False)
    ax.set_aspect("equal")
    ax.set_xlim(-1.8, 11.0)
    ax.set_ylim(4.0, -1.3)  # y tăng từ phía nhà sang vỉa hè, giống ảnh khi xoay
    ax.set_xlabel("x – along the road (m)")
    ax.set_ylabel("y – across the road (m)")
    ax.grid(alpha=0.25)
    ax.set_title(f"Water pipe and power cable mapped by GPR (labels: depth to top)\n{mo_ta_do_sau()}", fontsize=11)
    fig.savefig(duong_dan, dpi=150, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


# ---------------------------------------------------------------- HTML 3D
def _phan_tram(a):
    """Mã hóa bao biên độ 0..1 thành số nguyên 0..100 (null nếu ngoài vùng đo) cho gọn file."""
    a = np.clip(np.round(np.asarray(a) * 100), 0, 100)
    return [None if np.isnan(v) else int(v) for v in a.ravel()]


def xuat_html(gx, gy, z, khoi, tuyen, duong, rd, kenh, v, duong_dan):
    bz = max(1, len(z) // 80)
    du_lieu = dict(z=z[::bz].round(3).tolist(), tuyen=[], duong=[], rd=rd, mau=MAU_LOAI, ten_loai=TEN_LOAI)
    for t in tuyen:  # mặt cắt B-scan dựng đứng theo vị trí tuyến
        bx = max(1, len(t["s"]) // 150)
        e = bao_bien_do(t, kenh, v, z)[::bx, ::bz]
        du_lieu["tuyen"].append(dict(ten=t["ten"], x=t["xy"][::bx, 0].round(3).tolist(),
                                     y=t["xy"][::bx, 1].round(3).tolist(), e=_phan_tram(e.T)))
    sx, sy, sz = max(1, len(gx) // 70), max(1, len(gy) // 25), max(1, len(z) // 50)
    du_lieu["khoi"] = dict(x=gx[::sx].round(3).tolist(), y=gy[::sy].round(3).tolist(),
                           z=z[::sz].round(3).tolist(), gia_tri=_phan_tram(khoi[::sx, ::sy, ::sz]))
    for ten, d in duong.items():
        r = lambda a: np.asarray(a).round(3).tolist()
        du_lieu["duong"].append(dict(
            ten=ten, loai=d["loai"],
            diem=[[round(m["x"], 3), round(m["y"], 3), round(m["z"], 3)] for m in d["diem"]],
            quan_sat=None if d["quan_sat"] is None else r(d["quan_sat"]),
            du_doan=[] if d["quan_sat"] is None else [r(x) for x in d["du_doan"]]))
    rong = np.array([np.ptp(gx), np.ptp(gy), 1.2])
    ti_le = {k: float(max(v_ / rong.max(), 0.15)) for k, v_ in zip("xyz", rong)}
    tieu_de = f"3D map of the water pipe and power cable (GPR {kenh.replace('MHz', ' MHz')})"
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GPR 3D Map</title><script src="{PLOTLY_CDN}"></script>
<style>
body{{margin:0;font-family:system-ui,sans-serif;background:#fff;color:#222}}
header{{padding:10px 16px;border-bottom:1px solid #ddd}} h1{{font-size:18px;margin:0 0 4px}}
header p{{margin:0 0 4px;font-size:13px;color:#555}} label{{font-size:13px;margin-right:14px}}
#hinh{{height:calc(100vh - 120px);min-height:480px}}
</style></head><body>
<header><h1>{tieu_de}</h1>
<p>{mo_ta_do_sau()}</p>
<p>Blue = water pipe, orange = power cable; dashed = straight extension (not measured). x along the road, y across, origin = corner of the 10 m × 3.5 m survey area.
Drag to rotate, scroll to zoom, click the legend to show or hide layers.</p>
<label>Strong-reflection threshold <input id="nguong" type="range" min="20" max="90" value="55"> <span id="gt">0.55</span></label>
<label>Section opacity <input id="mo" type="range" min="0" max="100" value="70"></label>
</header>
<div id="hinh"></div>
<script>
const D = {json.dumps(du_lieu, separators=(",", ":"))};
const tl = {json.dumps(ti_le)};
function luoi(n, m, f) {{ const r = []; for (let i = 0; i < n; i++) {{ const h = []; for (let j = 0; j < m; j++) h.push(f(i, j)); r.push(h); }} return r; }}
const cot = (a, k) => a.map(p => k === 2 ? -p[2] : p[k]);
function dung(nguong, mo) {{
  const tr = [], nz = D.z.length;
  D.tuyen.forEach((t, i) => {{
    const n = t.x.length;
    tr.push({{type: "surface", name: "GPR line " + t.ten, legendgroup: "tuyen", showlegend: i === 0,
      showscale: false, opacity: mo,
      x: luoi(nz, n, (i, j) => t.x[j]), y: luoi(nz, n, (i, j) => t.y[j]), z: luoi(nz, n, (i) => -D.z[i]),
      surfacecolor: luoi(nz, n, (i, j) => t.e[i * n + j] / 100), colorscale: "Greys", reversescale: true,
      cmin: 0, cmax: 1, hovertemplate: "Line " + t.ten + "<br>x=%{{x:.2f}} y=%{{y:.2f}}<br>depth=%{{z:.2f}} m<extra></extra>"}});
  }});
  const K = D.khoi, X = [], Y = [], Z = [], V = [];
  let k = 0;
  for (const x of K.x) for (const y of K.y) for (const z of K.z) {{
    const v = K.gia_tri[k++]; X.push(x); Y.push(y); Z.push(-z); V.push(v === null ? 0 : v / 100);  // lưới phải đủ điểm
  }}
  tr.push({{type: "isosurface", name: "Strong reflections", x: X, y: Y, z: Z, value: V, visible: "legendonly",
    isomin: nguong, isomax: 1, surface: {{count: 2}}, colorscale: "YlOrRd", opacity: 0.3, showscale: false,
    caps: {{x: {{show: false}}, y: {{show: false}}, z: {{show: false}}}}, hovertemplate: "depth=%{{z:.2f}} m<extra></extra>"}});
  for (const d of D.duong) {{
    const mau = D.mau[d.loai], ten = D.ten_loai[d.loai];
    if (d.quan_sat) {{
      tr.push({{type: "scatter3d", mode: "lines", name: ten, legendgroup: d.ten, x: cot(d.quan_sat, 0),
        y: cot(d.quan_sat, 1), z: cot(d.quan_sat, 2), line: {{color: mau, width: 14}}, hoverinfo: "skip"}});
      for (const p of d.du_doan) tr.push({{type: "scatter3d", mode: "lines", legendgroup: d.ten, showlegend: false,
        x: cot(p, 0), y: cot(p, 1), z: cot(p, 2), line: {{color: mau, width: 6, dash: "dash"}}, hoverinfo: "skip"}});
    }}
    tr.push({{type: "scatter3d", mode: "markers+text", legendgroup: d.ten,
      name: d.loai === "khac" ? "Unidentified " + d.ten.replace("KHAC_", "#") : ten + " – picks",
      showlegend: !d.quan_sat, x: cot(d.diem, 0), y: cot(d.diem, 1), z: cot(d.diem, 2),
      text: d.diem.map(p => p[2].toFixed(2) + " m"), textposition: "top center", textfont: {{color: mau, size: 11}},
      marker: {{size: 5, color: mau, line: {{color: "white", width: 1}}}},
      hovertemplate: ten + "<br>x=%{{x:.2f}} y=%{{y:.2f}}<br>depth=%{{z:.2f}} m<extra></extra>"}});
  }}
  if (D.rd.length) tr.push({{type: "scatter3d", mode: "markers+text", name: "RD7000 points",
    x: D.rd.map(p => p.x), y: D.rd.map(p => p.y), z: D.rd.map(p => -p.z), text: D.rd.map(p => p.diem),
    marker: {{size: 6, symbol: "diamond", color: "#2b8a3e"}}}});
  const x0 = K.x[0], x1 = K.x[K.x.length - 1], y0 = K.y[0], y1 = K.y[K.y.length - 1];
  tr.push({{type: "surface", name: "Ground surface", showscale: false, opacity: 0.1, hoverinfo: "skip",
    x: [[x0, x1], [x0, x1]], y: [[y0, y0], [y1, y1]], z: [[0, 0], [0, 0]],
    colorscale: [[0, "#8d6e63"], [1, "#8d6e63"]]}});
  return tr;
}}
const layout = {{margin: {{l: 0, r: 0, t: 10, b: 0}}, legend: {{x: 0, y: 1}}, uirevision: "giu",
  scene: {{xaxis: {{title: "x along the road (m)"}}, yaxis: {{title: "y across (m)", autorange: "reversed"}},
    zaxis: {{title: "depth (m)"}}, aspectmode: "manual", aspectratio: tl,
    camera: {{eye: {{x: -0.6, y: -1.6, z: 0.9}}}}}}}};
const ve = () => {{
  const n = +document.getElementById("nguong").value / 100, mo = +document.getElementById("mo").value / 100;
  document.getElementById("gt").textContent = n.toFixed(2);
  Plotly.react("hinh", dung(n, mo), layout, {{responsive: true}});
}};
document.getElementById("nguong").addEventListener("change", ve);
document.getElementById("mo").addEventListener("change", ve);
ve();
</script>
</body></html>"""
    duong_dan.write_text(html, encoding="utf-8")


# ---------------------------------------------------------------- chương trình chính
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kenh", choices=KENH, default="700MHz", help="kênh dùng cho khối 3D và lát cắt")
    ap.add_argument("--v", type=float, default=None,
                    help=f"dùng một vận tốc (m/ns) thay mô hình 2 lớp, ví dụ {V_REFLEXW} như migration trong ReflexW; "
                         "0 = tự ước lượng bằng khớp hyperbol")
    ap.add_argument("--khoi", choices=("migration", "goc"), default="migration",
                    help="dữ liệu dựng khối 3D: đã migration (mặc định) hoặc chưa migration")
    ap.add_argument("--z-max", type=float, default=1.5, help="độ sâu lớn nhất của khối 3D (m)")
    ap.add_argument("--dz", type=float, default=0.01)
    ap.add_argument("--dxy", type=float, default=0.05, help="bước lưới ngang (m)")
    a = ap.parse_args()
    KET_QUA.mkdir(exist_ok=True)

    tuyen_theo_kenh = {k: doc_tuyen_do(k) for k in KENH}
    tra_tuyen = {(k, t["ten"]): t for k, ds in tuyen_theo_kenh.items() for t in ds}

    # gợi ý đỉnh hyperbol tự động
    goi_y = []
    for k, ds in tuyen_theo_kenh.items():
        for t in ds:
            for x0, t0, manh in tim_dinh_hyperbol(t, k):
                x0, t0, v, s = khop_van_toc(t["b"], t["h"], x0, t0)
                x, y = vi_tri(t, x0)
                goi_y.append(dict(kenh=k, tuyen=t["ten"], x_tren_tuyen_m=round(x0, 3), t_ns=round(t0, 2),
                                  v_khop=round(v, 4), semblance=round(s, 3), do_noi_bat=round(float(manh), 1),
                                  x=round(x, 3), y=round(y, 3)))
    with open(KET_QUA / "muc_tieu_tu_dong.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(goi_y[0]))
        w.writeheader()
        w.writerows(goi_y)

    # mục tiêu đã chọn
    muc_tieu = []
    for r in doc_csv("muc_tieu.csv"):
        t = tra_tuyen[(r["kenh"], r["tuyen"])]
        x0, t0, v, s = khop_van_toc(t["b"], t["h"], float(r["x_tren_tuyen_m"]), float(r["t_ns"]))
        if (r.get("ky_hieu") or "").strip():  # điểm nhóm đã chú thích: giữ đúng x, t của nhóm, không tinh chỉnh
            x0, t0 = float(r["x_tren_tuyen_m"]), float(r["t_ns"])
        loai = r["loai"].strip() if r["loai"].strip() in MAU_LOAI else "khac"
        nhom = (r.get("do_sau_nhom_m") or "").strip()
        muc_tieu.append(dict(ten=r["ten"], loai=loai, tuyen=r["tuyen"], kenh=r["kenh"],
                             x_tren_tuyen_m=x0, t_ns=t0, v_khop=v, semblance=s,
                             z_nhom=float(nhom) if nhom else None))
    # vận tốc: khớp hyperbol mọi điểm đã chọn trên cả hai kênh, lấy trung vị các lần khớp tin cậy
    tin_cay = []
    for m in muc_tieu:
        for k in KENH:
            t = tra_tuyen[(k, m["tuyen"])]
            _, _, vk, sk = khop_van_toc(t["b"], t["h"], m["x_tren_tuyen_m"], m["t_ns"])
            if sk > 0.2 and 0.055 < vk < 0.195:
                tin_cay.append(vk)
    v_uoc_luong = float(np.median(tin_cay)) if tin_cay else 0.10
    global V_DON
    if a.v is not None:
        V_DON = a.v or v_uoc_luong
    v = V_DON or V_REFLEXW  # chỉ còn dùng cho chữ trong cảnh 3D khi chọn một vận tốc
    print(f"Đổi độ sâu: {'v = %.3f m/ns' % V_DON if V_DON else 'mô hình 2 lớp (0,12 / 0,10 m/ns)'}; "
          f"khớp hyperbol cho trung vị {v_uoc_luong:.3f} m/ns từ {len(tin_cay)} lần khớp")
    for m in muc_tieu:
        m["x"], m["y"] = vi_tri(tra_tuyen[(m["kenh"], m["tuyen"])], m["x_tren_tuyen_m"])
        # độ sâu nhóm ghi trong bản chú thích (nếu có), không thì tính từ t
        m["z"] = m["z_nhom"] if (m["z_nhom"] is not None and not V_DON) else float(do_sau(m["t_ns"]))
    with open(KET_QUA / "muc_tieu_3d.csv", "w", newline="", encoding="utf-8-sig") as f:
        cot = ["ten", "loai", "tuyen", "kenh", "x_tren_tuyen_m", "t_ns", "v_khop", "semblance", "x", "y"]
        w = csv.DictWriter(f, fieldnames=cot + ["do_sau_m"])
        w.writeheader()
        for m in muc_tieu:
            w.writerow({**{c: (round(m[c], 3) if isinstance(m[c], float) else m[c]) for c in cot},
                        "do_sau_m": round(m["z"], 3)})
            print(f"  {m['ten']:8s} tuyến {m['tuyen']:>6s}  x={m['x']:6.2f}  y={m['y']:5.2f}  sâu={m['z']:.2f} m")

    rd = [dict(diem=r["diem"], loai=r["loai"], x=float(r["x"]), y=float(r["y"]), z=float(r["do_sau_m"] or 0))
          for r in doc_csv("diem_rd7000.csv")]

    tuyen = [t for t in tuyen_theo_kenh[a.kenh] if t["nhom"] != "lap"]
    if a.khoi == "migration" and DU_LIEU_MIG.is_dir():
        tuyen_khoi = [t for t in doc_tuyen_do(a.kenh, migration=True) if t["nhom"] != "lap"]
        print(f"Khối 3D dựng từ dữ liệu đã migration: {DU_LIEU_MIG.name}")
    else:
        tuyen_khoi = tuyen
    xy = np.vstack([t["xy"] for t in tuyen])
    duong = duong_ong_cap(muc_tieu, (xy[:, 0].min(), xy[:, 0].max()), (xy[:, 1].min(), xy[:, 1].max()))
    for ten, d in duong.items():
        if d["quan_sat"] is not None:
            p = d["quan_sat"]
            goc = np.degrees(np.arctan2(p[-1, 1] - p[0, 1], p[-1, 0] - p[0, 0])) % 180
            print(f"  -> {ten}: {len(d['diem'])} điểm, hướng {goc:.0f}° so với trục x (dọc đường), "
                  f"sâu {min(m['z'] for m in d['diem']):.2f}–{max(m['z'] for m in d['diem']):.2f} m")

    z = np.arange(0, a.z_max + 1e-9, a.dz)
    gx, gy, khoi = dung_khoi(tuyen_khoi, a.kenh, v, z, a.dxy)
    ve_ban_do(tuyen, duong, rd, v, KET_QUA / "BanDo_OngNuoc_Cap.png")
    ve_lat_cat(gx, gy, z, khoi, tuyen, duong, float(do_sau(CAT_DAU_NS[a.kenh])) + 0.05,
               f"GPR {a.kenh.replace('MHz', ' MHz')}{', after migration' if tuyen_khoi is not tuyen else ''}",
               KET_QUA / "LatCat_DoSau.png")
    xuat_html(gx, gy, z, khoi, tuyen_khoi, duong, rd, a.kenh, v, KET_QUA / "BanDo3D_OngNuoc_Cap.html")
    if anh_hien_truong.ANH.exists():
        anh_hien_truong.ve_ket_qua(duong, mo_ta_do_sau())  # ống + cáp vẽ lên ảnh IMG_9558 (slide 5, 7)
        canh_3d.xuat_canh_3d(duong, [t for t in tuyen_theo_kenh["250MHz"] if t["nhom"] != "lap"],
                             dict(thoi_gian=thoi_gian, v=V_DON, v_bt=V_BT, v_dat=V_DAT, z_bt=V_BT * T_BT / 2),
                             "250MHz", KET_QUA / "Canh3D_HienTruong.html")  # cảnh 3D tương tác (Three.js)
    if HINH_SLIDE.is_dir():
        for ten in ("BanDo_OngNuoc_Cap.png", "LatCat_DoSau.png", "SoDoTuyen_GPR.png", "SoDoTuyen_GPR.pdf"):
            if (KET_QUA / ten).exists():
                shutil.copy2(KET_QUA / ten, HINH_SLIDE / ten)
    print(f"Đã xuất bản đồ vào {KET_QUA} và chép hình sang {HINH_SLIDE}")


if __name__ == "__main__":
    main()
