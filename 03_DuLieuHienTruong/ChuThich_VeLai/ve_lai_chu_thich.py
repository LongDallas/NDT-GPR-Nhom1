"""Vẽ lại 10 radargram trong "New Data" (file .10T / .11T / .00T, kênh 250 MHz) kèm chú thích của nhóm.

Bản chú thích gốc (New Data/GPR_chu_thich_duong_ong.pdf) là ảnh chụp màn hình ReflexW, đánh dấu tay.
Script này đọc thẳng file dữ liệu và vẽ lại cùng nội dung:
  - vòng tròn = đỉnh hyperbol, đường dọc = vị trí x và phần đuôi tín hiệu (như chú giải của nhóm);
  - màu: đỏ P = ống cáp / vật kim loại, cam O = dị thường, xanh A = ống nước;
  - bảng dưới mỗi mặt cắt: ký hiệu, x, t đỉnh, độ sâu, phân loại, mô tả (mô tả đo từ dữ liệu).
Điểm chú thích lấy từ 02_SoDoTuyen_BanDo/muc_tieu.csv (cột ky_hieu), hướng tuyến từ tuyen_do.csv;
độ sâu theo mô hình 2 lớp của nhóm (02_SoDoTuyen_BanDo/SDT_Tai/ve_mat_cat_gpr.py).

File .T trong New Data không kèm header .R, nên header lấy từ file cùng tên trong "Data - processed".

Chạy:  python3 ve_lai_chu_thich.py
  -> GPR_chu_thich_ve_lai.pdf (báo cáo A4) và png/<tuyến>_<file>.png (từng tuyến)
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.ndimage import gaussian_filter, uniform_filter1d
from scipy.signal import hilbert

THU_MUC = Path(__file__).resolve().parent
GOC_DU_AN = THU_MUC.parent.parent
NEW_DATA = THU_MUC.parent / "New Data"
HEADER = THU_MUC.parent / "Data - processed"
sys.path.insert(0, str(GOC_DU_AN / "02_SoDoTuyen_BanDo"))
sys.path.insert(0, str(GOC_DU_AN / "02_SoDoTuyen_BanDo" / "SDT_Tai"))
import doc_reflexw  # noqa: E402
import dung_ban_do_3d as bd  # noqa: E402
import ve_mat_cat_gpr as g  # noqa: E402

T_HIEN = 50.0  # ns hiển thị, như cửa sổ nhóm chụp trong ReflexW
MAU = g.MAU_KY_HIEU
PHAN_LOAI = {"P": "Ống cáp / vật kim loại\n(khả năng cao)", "O": "Dị thường", "A": "Ống nước\n(khả năng cao)"}
GHI_CHU_THEM = {  # nhận xét riêng cho từng điểm, nối vào cột Mô tả
    ("C3", "O5"): "Nhóm ghi sâu 0,40 m, nhưng t = 4,25 ns chỉ ứng với ≈ 0,26 m (trong lớp bê tông).",
}
KHONG_CHU_THICH = {
    "N1": "Không thấy hyperbol hay dị thường rõ ràng. Chỉ có các phản xạ phẳng ở lớp mặt (theo chú thích của nhóm).",
}
A4 = (8.27, 11.69)


def doc_file_new_data(file_t):
    """Đọc .T trong New Data, header .R cùng tên lấy trong Data - processed."""
    h = doc_reflexw.doc_header(HEADER / (file_t.stem + file_t.suffix[:-1] + "R"))
    raw = np.fromfile(file_t, dtype=np.uint8)
    do_dai = doc_reflexw.TRACE_HEADER + 2 * h["ns"]
    if raw.size != do_dai * h["ntr"]:
        raise ValueError(f"{file_t.name}: kích thước không khớp header")
    b = raw.reshape(h["ntr"], do_dai)[:, doc_reflexw.TRACE_HEADER:].copy().view("<i2").T.astype(np.float32)
    return b, h


def tai_tuyen():
    """Mỗi file trong New Data -> một tuyến, đã xoay về chiều chuẩn (x tính từ đầu trái với C, đầu trên với N)."""
    theo_ma = {r["file_250MHz"][:8]: r for r in bd.doc_csv("tuyen_do.csv")}
    chu_thich = {}
    for r in bd.doc_csv("muc_tieu.csv"):
        if (r.get("ky_hieu") or "").strip() and r["kenh"] == "250MHz":
            chu_thich.setdefault(r["tuyen"], []).append(r)
    ds = []
    for f in sorted(NEW_DATA.glob("LZZ2*.*T")):
        r = theo_ma[f.name[:8]]
        b, h = doc_file_new_data(f)
        if r.get("xu_ly_them", "").strip() == "nen":  # file .00T chưa xử lý: dewow + xóa nền như dung_ban_do_3d
            b = b - uniform_filter1d(b, 31, axis=0)
            b = b - b.mean(axis=1, keepdims=True)
        p0 = np.array([float(r["x_dau"]), float(r["y_dau"])])
        p1 = np.array([float(r["x_cuoi"]), float(r["y_cuoi"])])
        huong = (p1 - p0) / np.linalg.norm(p1 - p0)
        nguoc = bool(huong.sum() < 0)  # đo ngược chiều (zigzag)
        xflip = "XFlipProfile" in h["buoc_xu_ly"]  # file đã bị lật trong ReflexW (LZZ20003.11T)
        lat = nguoc != xflip
        if lat:
            b = b[:, ::-1]
        dai = (h["ntr"] - 1) * h["dx"]
        diem = []
        for c in chu_thich.get(r["tuyen"], []):
            s = float(c["x_tren_tuyen_m"])  # theo thứ tự ghi của máy
            diem.append(dict(ky_hieu=c["ky_hieu"], loai=c["ky_hieu"][0], t=float(c["t_ns"]),
                             x=dai - s if nguoc else s, xy=p0 + s * huong,
                             do_sau_nhom=float(c["do_sau_nhom_m"] or "nan")))
        ds.append(dict(ten=r["tuyen"], file=f.name, b=b, h=h, dai=dai, nguoc=nguoc, xflip=xflip, lat=lat,
                       diem=sorted(diem, key=lambda d: d["x"])))
    return ds


def do_dac_trung(t, d):
    """Biên độ đỉnh so với nền của tuyến và thời điểm cuối của đuôi tín hiệu (bao > 2,5 lần nền)."""
    b, h = t["b"], t["h"]
    e = gaussian_filter(np.abs(hilbert(b, axis=0)), (2, 1))
    nen = np.median(e[int(8 / h["dt"]):int(50 / h["dt"])])
    j, i = int(round(d["x"] / h["dx"])), int(round(d["t"] / h["dt"]))
    cot = e[:, max(j - 2, 0):j + 3].mean(axis=1)
    ti_le = cot[max(i - 8, 0):i + 8].max() / nen
    k = i
    while k < len(cot) - 1 and cot[k] > 2.5 * nen:
        k += 1
    d["ti_le"], d["t_duoi"] = float(ti_le), max(k * h["dt"], d["t"] + 2)


def mo_ta(t, d):
    dau = {"P": "Hyperbol mạnh", "O": "Phản xạ cong", "A": "Hyperbol rõ"}[d["loai"]]
    chu = f"{dau}, biên độ ≈ {d['ti_le']:.0f}× nền của tuyến, đuôi tín hiệu tới ~{d['t_duoi']:.0f} ns."
    if t["nguoc"]:
        chu += " x đo trên tuyến đã lật."
    them = GHI_CHU_THEM.get((t["ten"], d["ky_hieu"]))
    return chu + (" " + them if them else "")


def ngat_dong(chu, rong):
    """Ngắt chữ thành nhiều dòng, mỗi dòng tối đa `rong` ký tự (cho ô bảng)."""
    dong, cur = [], ""
    for tu in chu.split():
        if cur and len(cur) + 1 + len(tu) > rong:
            dong.append(cur)
            cur = tu
        else:
            cur = f"{cur} {tu}".strip()
    return "\n".join(dong + [cur])


def ve_radargram(ax, t, co=8):
    b, h = t["b"], t["h"]
    i_max = int(T_HIEN / h["dt"]) + 1
    gh = np.percentile(np.abs(b[int(8 / h["dt"]):i_max]), 99)
    ax.imshow(b[:i_max], cmap="gray", vmin=-gh, vmax=gh, aspect="auto",
              extent=[0, t["dai"], i_max * h["dt"], 0], interpolation="bilinear")
    ax.set_xlim(0, t["dai"])
    ax.set_ylim(T_HIEN, 0)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")
    ax.set_xlabel("Khoảng cách [m]", fontsize=co, labelpad=2)
    ax.set_ylabel("Thời gian [ns]", fontsize=co)
    ax.tick_params(labelsize=co - 1)
    ax.set_xticks(np.arange(0, t["dai"] + 1e-9, 1.0 if t["dai"] > 5 else 0.5))
    phai = ax.secondary_yaxis("right", functions=(g.do_sau, g.thoi_gian))
    phai.set_ylabel("Độ sâu [m]", fontsize=co - 1)
    phai.tick_params(labelsize=co - 1)
    for d in t["diem"]:
        mau = MAU[d["loai"]]
        ax.plot([d["x"], d["x"]], [d["t"], d["t_duoi"]], color=mau, lw=2, solid_capstyle="round")
        ax.plot(d["x"], d["t"], "o", ms=13, mfc="none", mec=mau, mew=2.2)
        ax.annotate(d["ky_hieu"], (d["x"], d["t"]), xytext=(9, 9), textcoords="offset points", fontsize=co,
                    fontweight="bold", color=mau, bbox=dict(boxstyle="square,pad=0.25", fc="white", ec=mau, lw=1))


def ten_mat_cat(t):
    chu = f"Tuyến {t['ten'].replace('_lap', ' (đo lặp)')} – {t['file']} ({t['h']['ntr']} vết, {t['dai']:.2f} m)"
    if t["xflip"] and not t["lat"]:
        chu += " · file đã XFlip, giữ nguyên"
    elif t["xflip"]:
        chu += " · file đã XFlip, lật lại về chiều đo"
    elif t["lat"]:
        chu += " · đo ngược chiều, đã lật"
    return chu


def ve_bang(ax, t, co=7.5):
    ax.set_axis_off()
    if not t["diem"]:
        ax.text(0, 0.9, KHONG_CHU_THICH.get(t["ten"], "Nhóm chưa chú thích tuyến này."), fontsize=co + 1,
                va="top", ha="left", style="italic", color="0.25", transform=ax.transAxes)
        return
    hang = [[d["ky_hieu"], f"{d['x']:.2f}", f"{d['t']:g}", f"{float(g.do_sau(d['t'])):.2f}",
             PHAN_LOAI[d["loai"]], ngat_dong(mo_ta(t, d), 58)] for d in t["diem"]]
    tieu_de = ["Ký\nhiệu", "Vị trí x\n(m)", "t đỉnh\n(ns)", "Độ sâu\n(m)", "Phân loại", "Mô tả"]
    bang = ax.table(cellText=hang, colLabels=tieu_de, colWidths=[0.06, 0.08, 0.07, 0.07, 0.18, 0.54],
                    loc="upper left", cellLoc="left")
    bang.auto_set_font_size(False)
    bang.set_fontsize(co)
    cao_ax = ax.get_position().height * ax.figure.get_figheight()  # inch
    dong_in = co * 1.3 / 72
    for (r, c), o in bang.get_celld().items():
        so_dong = max(str(v).count("\n") for v in (hang[r - 1] if r else tieu_de)) + 1
        o.set_height((so_dong * dong_in + 0.06) / cao_ax)
        o.PAD = 0.012 / o.get_width()  # đệm cố định ~1,2 % bề rộng bảng (mặc định 10 % bề rộng ô, cột rộng bị lệch)
        o.get_text().set_multialignment("left")
        o.set_edgecolor("0.6")
        o.set_linewidth(0.6)
        if r == 0:
            o.set_facecolor("#e9ecef")
            o.get_text().set_fontweight("bold")
        elif c == 0:
            o.get_text().set_color(MAU[hang[r - 1][0][0]])
            o.get_text().set_fontweight("bold")


def ve_khoi(fig, y0, cao, t, co=8):
    """Một tuyến: tên + radargram + bảng, chiếm dải [y0, y0 + cao] của trang (tọa độ figure)."""
    ax = fig.add_axes([0.09, y0 + cao * 0.36, 0.80, cao * 0.52])
    ve_radargram(ax, t, co)
    fig.text(0.09, y0 + cao * 0.995, ten_mat_cat(t), fontsize=co + 2, fontweight="bold", va="top", color="#1f2fa0")
    ve_bang(fig.add_axes([0.06, y0, 0.88, cao * 0.31]), t, co - 0.5)


def trang_bia(pdf, tuyen):
    fig = plt.figure(figsize=A4)
    fig.text(0.06, 0.955, "Báo cáo chú thích radargram GPR – vẽ lại từ dữ liệu", fontsize=17, fontweight="bold")
    fig.text(0.06, 0.93, "Vị trí, độ sâu và phân loại dị thường (đường ống, dị vật) trên 10 file trong \"New Data\" "
             "(IDS Detector Duo, kênh 250 MHz)", fontsize=9, color="0.3")
    muc = [
        ("1. Vận tốc và cách tính độ sâu",
         f"Theo chú thích của nhóm: trong bê tông v = {g.V_BT} m/ns, trong đất v = {g.V_DAT} m/ns. Lớp bê tông chiếm "
         f"{g.T_BT:.0f} ns đầu (≈ {float(g.do_sau(g.T_BT)):.2f} m, suy ngược từ bảng độ sâu của nhóm). "
         f"Độ sâu d = 0,06·min(t, {g.T_BT:.0f}) + 0,05·max(t − {g.T_BT:.0f}, 0), t là thời gian hai chiều (ns). "
         "Trục độ sâu bên phải mỗi mặt cắt vì vậy không chia đều."),
        ("2. Chú giải",
         "Đỏ (P): ống cáp / vật kim loại, khả năng cao (hyperbol mạnh, đuôi ringing dài). Cam (O): dị vật hoặc vùng "
         "nhiễu loạn. Xanh (A): ống nước. Vòng tròn là đỉnh hyperbol, đường dọc là vị trí x và phần đuôi tín hiệu "
         "(tới khi bao biên độ còn trên 2,5 lần nền). Cột Mô tả do script đo trên dữ liệu."),
        ("3. Chiều đo",
         "Máy đi zigzag: C2, C4, N2, N4 đo ngược chiều nên được lật lại (như nhóm đã làm trong ReflexW); khoảng cách "
         "trên mọi mặt cắt tính từ đầu trái (tuyến C) hoặc đầu phía nhà (tuyến N). LZZ20003.11T là bản XFlip của C3, "
         "được lật lại về chiều đo để khớp chú thích."),
    ]
    y = 0.895
    for tieu_de, noi_dung in muc:
        fig.text(0.06, y, tieu_de, fontsize=11, fontweight="bold")
        fig.text(0.06, y - 0.017, ngat_dong(noi_dung, 118), fontsize=8.3, va="top", linespacing=1.45)
        y -= 0.017 + 0.0145 * (ngat_dong(noi_dung, 118).count("\n") + 1) + 0.022
    fig.text(0.06, y, "4. Tóm tắt kết quả", fontsize=11, fontweight="bold")
    hang = []
    for t in tuyen:
        for d in t["diem"]:
            hang.append([t["ten"], d["ky_hieu"], f"{d['x']:.2f}", f"{d['t']:g}", f"{float(g.do_sau(d['t'])):.2f}",
                         PHAN_LOAI[d["loai"]].replace("\n", " "), f"{d['xy'][0]:.2f}; {d['xy'][1]:.2f}"])
    ax = fig.add_axes([0.06, y - 0.27, 0.88, 0.255])
    ax.set_axis_off()
    bang = ax.table(cellText=hang, colLabels=["Tuyến", "Ký hiệu", "x (m)", "t (ns)", "Độ sâu (m)", "Phân loại",
                                              "Mặt bằng x; y (m)"],
                    colWidths=[0.08, 0.08, 0.08, 0.08, 0.1, 0.38, 0.18], loc="upper left", cellLoc="center")
    bang.auto_set_font_size(False)
    bang.set_fontsize(8)
    bang.scale(1, 1.25)
    for (r, c), o in bang.get_celld().items():
        o.set_edgecolor("0.6")
        o.set_linewidth(0.6)
        if r == 0:
            o.set_facecolor("#e9ecef")
            o.get_text().set_fontweight("bold")
        elif c == 1:
            o.get_text().set_color(MAU[hang[r - 1][1][0]])
            o.get_text().set_fontweight("bold")
    y -= 0.29
    fig.text(0.06, y, "5. Sơ đồ mặt bằng", fontsize=11, fontweight="bold")
    goc, _ = g.tai_du_lieu()
    ct = g.doc_chu_thich(goc)
    g.ve_so_do_nho(fig.add_axes([0.08, 0.07, 0.84, y - 0.09]), goc, ct, set())
    fig.text(0.06, 0.035, "Không có chú thích: N1 (nhóm ghi không thấy dị thường rõ), N3, N4, N5 và lần đo lặp N5 "
             "(nhóm chưa chú thích).", fontsize=8, style="italic", color="0.35")
    pdf.savefig(fig)
    plt.close(fig)


def main():
    tuyen = tai_tuyen()
    for t in tuyen:
        for d in t["diem"]:
            do_dac_trung(t, d)
    (THU_MUC / "png").mkdir(exist_ok=True)
    with PdfPages(THU_MUC / "GPR_chu_thich_ve_lai.pdf") as pdf:
        trang_bia(pdf, tuyen)
        for i in range(0, len(tuyen), 2):  # 2 tuyến mỗi trang A4
            fig = plt.figure(figsize=A4)
            for k, t in enumerate(tuyen[i:i + 2]):
                ve_khoi(fig, 0.52 - 0.48 * k, 0.45, t)
            pdf.savefig(fig)
            plt.close(fig)
    for t in tuyen:  # từng tuyến một ảnh ngang, dùng cho slide / báo cáo
        fig = plt.figure(figsize=(11, 6.2))
        ve_khoi(fig, 0.03, 0.95, t, co=9)
        fig.savefig(THU_MUC / "png" / f"{t['ten']}_{t['file'].replace('.', '_')}.png", dpi=170)
        plt.close(fig)
    for t in tuyen:
        print(f"{t['ten']:7s} {t['file']}  lật={t['lat']}  " +
              ", ".join(f"{d['ky_hieu']} x={d['x']:.2f} sâu={float(g.do_sau(d['t'])):.2f}" for d in t["diem"]))
    print(f"Đã lưu {THU_MUC / 'GPR_chu_thich_ve_lai.pdf'} và png/")


if __name__ == "__main__":
    main()
