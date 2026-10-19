"""Xuất phần nền B-scan (ảnh xám, không trục) và các số liệu cho hinh_mat_cat_gpr.tex.

TikZ không vẽ được dữ liệu radar, nên script này cắt sẵn từng mặt cắt thành PNG trong nen/,
rồi ghi mọi số liệu (điểm chú thích, khung kích thước, vạch độ sâu, sơ đồ tuyến) vào so_lieu.tex;
file .tex chính \\input{so_lieu} nên không cần dán tay.
Chạy:  python3 xuat_nen_tikz.py
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

THU_MUC = Path(__file__).resolve().parent
sys.path.insert(0, str(THU_MUC.parent))
import ve_mat_cat_gpr as g  # noqa: E402

NEN = THU_MUC / "nen"
W, H = 14, 7.875  # khung hình 16:9 (inch), giống ve_mat_cat_gpr.khung_hinh
DPI = 200


def luu_nen(t, ten, o, x_lim, t_lim, t_gain=None):
    """Lưu vùng [x_lim] × [t_lim] của mặt cắt t thành PNG cỡ đúng ô o = (rộng, cao) theo tỉ lệ khung hình.

    Độ tương phản lấy như ve_bscan: phân vị 99 của |biên độ| từ 8 ns tới t_gain.
    """
    b, h = t["b"], t["h"]
    t_gain = t_gain or t_lim[1]
    i_max = int(t_gain / h["dt"]) + 1
    gh = np.percentile(np.abs(b[int(8 / h["dt"]):i_max]), 99)
    i_ve = int(t_lim[1] / h["dt"]) + 1
    fig = plt.figure(figsize=(o[0] * W, o[1] * H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(b[:i_ve], cmap="gray", vmin=-gh, vmax=gh, aspect="auto",
              extent=[0, t["s"][-1], i_ve * h["dt"], 0], interpolation="bilinear")
    ax.set_xlim(*x_lim)
    ax.set_ylim(t_lim[1], t_lim[0])
    ax.set_axis_off()
    fig.savefig(NEN / f"{ten}.png", dpi=DPI)
    plt.close(fig)


def so(v):
    return f"{float(v):.4f}"


def vach_do_sau(buoc, d_max):
    """Vị trí (ns) và nhãn (m) của các vạch độ sâu: trục độ sâu không tuyến tính vì có 2 lớp vận tốc."""
    d = np.round(np.arange(0, d_max + 1e-9, buoc), 2)
    return ",".join(so(t) for t in g.thoi_gian(d)), ",".join(f"{x:.2f}" for x in d)


def main():
    NEN.mkdir(exist_ok=True)
    goc, mig = g.tai_du_lieu()
    ct = g.doc_chu_thich(goc)
    T = g.T_MAX
    dong = [f"% Tạo bởi xuat_nen_tikz.py – không sửa tay.",
            f"\\def\\VBT{{{g.V_BT}}}\\def\\VDAT{{{g.V_DAT}}}\\def\\TBT{{{g.T_BT}}}\\def\\VMIG{{{g.V_MIG}}}\\def\\TMAX{{{T:g}}}"]
    for ten, buoc, d_max in (("A", 0.25, 2.0), ("B", 0.2, 1.4)):
        vt, nh = vach_do_sau(buoc, d_max)
        dong.append(f"\\def\\VachT{ten}{{{vt}}}\\def\\VachD{ten}{{{nh}}}")

    # điểm chú thích: \ct{tuyến}{ký hiệu}{x | t | v | sau | mx | my}
    for (tuyen, k), m in ct.items():
        for khoa, gt in (("x", m["x"]), ("t", m["t"]), ("v", g.v_rms(m["t"])), ("sau", g.do_sau(m["t"])),
                         ("mx", m["xy"][0]), ("my", m["xy"][1])):
            dong.append(f"\\expandafter\\def\\csname ct-{tuyen}-{k}-{khoa}\\endcsname{{{so(gt)}}}")
    dai = {ten: t["s"][-1] for ten, t in goc.items()}
    for ten in ("C1", "N1", "N2"):
        dong.append(f"\\expandafter\\def\\csname dai-{ten}\\endcsname{{{so(dai[ten])}}}")

    # sơ đồ tuyến: tên/x đầu/y đầu/x cuối/y cuối/x nhãn/y nhãn (nhãn ở đầu chuẩn: trái với C, trên với N)
    tuyen = []
    for t in goc.values():
        if t["nhom"] == "lap":
            continue
        p0, p1 = t["p0"], t["p0"] + t["s"][-1] * t["huong"]
        chuan = -t["huong"] if t["nguoc"] else t["huong"]
        nhan = (p1 if t["nguoc"] else p0) - 0.4 * chuan
        tuyen.append("/".join([t["ten"], *map(so, (*p0, *p1, *nhan))]))
    dong.append(f"\\def\\DanhSachTuyen{{{', '.join(tuyen)}}}")
    diem = [f"{m['ky_hieu']}/{so(m['xy'][0])}/{so(m['xy'][1])}" for m in ct.values()]
    dong.append(f"\\def\\DanhSachDiem{{{', '.join(diem)}}}")
    cap = sorted((m["xy"] for m in ct.values() if m["ten"] == "CAP"), key=lambda p: p[1])  # đường cáp: P1 trên C1–C4
    dong.append(f"\\def\\DuongCap{{{' -- '.join(f'({so(x)},{so(y)})' for x, y in cap)}}}")
    ong, doan = g.duong_ong(goc)  # ống nước: đoạn khớp + các điểm (A1, N4, N5)
    dong.append(f"\\def\\DuongOng{{{' -- '.join(f'({so(x)},{so(y)})' for x, y in doan)}}}")
    dong.append(f"\\def\\DanhSachOng{{{', '.join(f'{so(x)}/{so(y)}' for x, y in ong)}}}")

    # Hình 1 – cáp: (a) C1, (b) C3, (c) C1 sau migration, (d) kích thước dị vật trên C1 sau migration
    luu_nen(goc["C1"], "h1a", (0.29, 0.33), (0, dai["C1"]), (0, T))
    luu_nen(goc["C3"], "h1b", (0.29, 0.33), (0, 6), (0, T))
    luu_nen(mig["C1"], "h1c", (0.23, 0.38), (0, 6), (0, T))
    p1 = ct[("C1", "P1")]
    x_a, x_b, t_a, t_b = g.kich_thuoc(mig["C1"], p1["x"], p1["t"])
    xm, tm = (x_a + x_b) / 2, (t_a + t_b) / 2
    td = min(tm + 14, T)
    luu_nen(mig["C1"], "h1d", (0.20, 0.38), (xm - 0.9, xm + 0.9), (0, td))
    for k, v in dict(HkXa=x_a, HkXb=x_b, HkTa=t_a, HkTb=t_b, HkDXmin=xm - 0.9, HkDXmax=xm + 0.9, HkDTmax=td,
                     HkCaoCm=(g.do_sau(t_b) - g.do_sau(t_a)) * 100, HkSau=g.do_sau(t_a)).items():
        dong.append(f"\\def\\{k}{{{so(v)}}}")

    # Hình 2 – ống nước: (a) N2, (b) N1, (c) N2 sau migration, (d) phóng to hyperbol A1 trên N2
    luu_nen(goc["N2"], "h2a", (0.29, 0.33), (0, dai["N2"]), (0, T))
    luu_nen(goc["N1"], "h2b", (0.29, 0.33), (0, dai["N1"]), (0, T))
    luu_nen(mig["N2"], "h2c", (0.23, 0.38), (0, mig["N2"]["s"][-1]), (0, T))
    a1 = ct[("N2", "A1")]
    luu_nen(goc["N2"], "h2d", (0.20, 0.38), (a1["x"] - 0.8, a1["x"] + 0.8), (0, a1["t"] + 14))
    dong.append(f"\\expandafter\\def\\csname dai-mig-N2\\endcsname{{{so(mig['N2']['s'][-1])}}}")

    # Hình 3 – vùng tín hiệu trên C1: (a) đã lọc, (b) sau migration, (c) phóng to khung đỏ
    luu_nen(goc["C1"], "h3a", (0.36, 0.40), (0, dai["C1"]), (0, T))
    luu_nen(mig["C1"], "h3b", (0.36, 0.40), (0, mig["C1"]["s"][-1]), (0, T))
    hop = (p1["x"] - 0.8, max(p1["t"] - 6, 0), 1.6, 14)
    luu_nen(goc["C1"], "h3c", (0.15, 0.22), (hop[0], hop[0] + hop[2]), (hop[1], hop[1] + hop[3]),
            t_gain=hop[1] + hop[3])
    dong += [f"\\expandafter\\def\\csname dai-mig-C1\\endcsname{{{so(mig['C1']['s'][-1])}}}",
             f"\\def\\HbHopX{{{so(hop[0])}}}\\def\\HbHopT{{{so(hop[1])}}}"]

    (THU_MUC / "so_lieu.tex").write_text("\n".join(dong) + "\n", encoding="utf-8")
    print(f"Đã lưu nền vào {NEN} và số liệu vào {THU_MUC / 'so_lieu.tex'}")


if __name__ == "__main__":
    main()
