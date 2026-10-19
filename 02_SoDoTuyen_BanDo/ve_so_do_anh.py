"""Vẽ lên ảnh hiện trường IMG_9558 (chụp từ trên cao) – chữ tiếng Anh vì slide viết tiếng Anh.

Chạy:  python3 ve_so_do_anh.py   -> ket_qua/SoDoTuyen_IMG_9558.jpg  (sơ đồ bố trí tuyến, slide 3)
Hàm ve_ket_qua() được dung_ban_do_3d.py gọi -> ket_qua/KetQua_IMG_9558.jpg (ống + cáp trên ảnh, slide 5 và 7).
Cả hai được chép sang 01_Slide/HinhAnh/.

Khung khảo sát 10 m x 3,5 m được đặt lên ảnh bằng phép chiếu phối cảnh (homography) từ 4 góc khung:
cạnh phải = mép vỉa hè (C4 trùng mép phải), cạnh trái = mép nhựa đường phía nhà,
cạnh trên/dưới theo mốc ghế đá giống ảnh sơ đồ cũ. Hệ toạ độ: x dọc đường (m), y ngang đường (m).
"""
import csv
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

THU_MUC = Path(__file__).resolve().parent
ANH = THU_MUC / "Ảnh hiện trường" / "IMG_9558.jpg"  # bản JPG đứng của IMG_9558.HEIC
KET_QUA = THU_MUC / "ket_qua"
HINH_SLIDE = THU_MUC.parent / "01_Slide" / "HinhAnh"

DAI, RONG = 10.0, 3.5                       # khung khảo sát (m)
C_Y = [0.5, 1.5, 2.5, 3.5]                  # C1–C4: cách nhau 1 m, C1 cách mép trái 0,5 m
with open(THU_MUC / "tuyen_do.csv", encoding="utf-8-sig") as f:  # N1–N5 lấy từ tuyen_do.csv
    _N = [r for r in csv.DictReader(f) if r["nhom"] == "cat_ngang"]
N_X = [float(r["x_dau"]) for r in _N]
# đoạn y mỗi tuyến N thật sự đo (đầu phía ghế đá sát mép đường y = 3,5 m, đầu phía nhà tuỳ chiều dài)
N_Y = [tuple(sorted((float(r["y_dau"]), float(r["y_cuoi"])))) for r in _N]
KC_N = float(np.mean(np.diff(N_X)))         # khoảng cách giữa các tuyến N
C_X = (-1.3, 11.5)                          # tuyến dọc dài hơn khung (dữ liệu ~11 m)

# 4 góc khung trên ảnh (pixel ảnh 3024 x 4032): (x, y) mét -> (px, py)
GOC = {(0, 0): (432, 1112), (0, RONG): (1740, 1112), (DAI, 0): (446, 3758), (DAI, RONG): (1572, 3758)}

VANG, XANH, DO = (255, 214, 0), (46, 184, 76), (230, 40, 40)
MAU_ONG, MAU_CAP, MAU_KHAC = (28, 126, 214), (232, 89, 12), (134, 142, 150)
DEN, TRANG = (25, 25, 25), (255, 255, 255)
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_THUONG = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_NGHIENG = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"


def homography(nguon, dich):
    A = []
    for (x, y), (u, v) in zip(nguon, dich):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y, -u], [0, 0, 0, x, y, 1, -v * x, -v * y, -v]]
    h = np.linalg.svd(np.array(A, float))[2][-1]
    return h.reshape(3, 3) / h[-1]


H = homography(list(GOC), list(GOC.values()))


def px(x, y):
    """(x, y) mét -> (px, py) trên ảnh; nhận số hoặc mảng."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    u = H[0, 0] * x + H[0, 1] * y + H[0, 2]
    v = H[1, 0] * x + H[1, 1] * y + H[1, 2]
    w = H[2, 0] * x + H[2, 1] * y + H[2, 2]
    return u / w, v / w


def m(gia_tri, so=1):
    return f"{gia_tri:.{so}f} m"


def duong(ve, p0, p1, mau, rong, vien=True):
    a, b = tuple(map(float, px(*p0))), tuple(map(float, px(*p1)))
    if vien:
        ve.line([a, b], fill=DEN, width=rong + 8)
    ve.line([a, b], fill=mau, width=rong)


def net_dut(ve, diem, mau, rong, dai=60, ho=40):
    """Đường nét đứt qua dãy điểm (pixel)."""
    for a, b in zip(diem[:-1], diem[1:]):
        a, b = np.array(a), np.array(b)
        L = np.linalg.norm(b - a)
        n = (b - a) / L
        s = 0.0
        while s < L:
            ve.line([tuple(a + n * s), tuple(a + n * min(s + dai, L))], fill=mau, width=rong)
            s += dai + ho


def nhan_vien(ve, tam, chu, nen, co=52, mau_chu=DEN):
    f = ImageFont.truetype(FONT, co)
    x0, y0, x1, y1 = ve.textbbox((0, 0), chu, font=f)
    w, h = x1 - x0, y1 - y0
    pad = co * 0.35
    hop = [tam[0] - w / 2 - pad, tam[1] - h / 2 - pad * 0.8, tam[0] + w / 2 + pad, tam[1] + h / 2 + pad * 0.8]
    ve.rounded_rectangle(hop, radius=(hop[3] - hop[1]) / 2, fill=nen, outline=DEN, width=5)
    ve.text((tam[0] - w / 2 - x0, tam[1] - h / 2 - y0), chu, font=f, fill=mau_chu)


def kich_thuoc(ve, p0, p1, chu, co=46, t=0.5):
    """Đường ghi kích thước có vạch hai đầu; nhãn đặt ở tỉ lệ t dọc đường (0,5 = giữa)."""
    a, b = np.array(px(*p0), float), np.array(px(*p1), float)
    ve.line([tuple(a), tuple(b)], fill=TRANG, width=6)
    n = (b - a) / np.linalg.norm(b - a)
    vg = np.array([-n[1], n[0]]) * 22
    for q in (a, b):
        ve.line([tuple(q - vg), tuple(q + vg)], fill=TRANG, width=6)
    nhan_vien(ve, tuple(a + t * (b - a)), chu, TRANG, co=co)


def ve_khung_tuyen(ve, mo=False):
    """Khung đỏ + tuyến; mo=True vẽ mảnh, không nhãn (làm nền cho ảnh kết quả)."""
    rong = 10 if mo else 22
    for p0, p1 in (((0, 0), (0, RONG)), ((0, RONG), (DAI, RONG)), ((DAI, RONG), (DAI, 0)), ((DAI, 0), (0, 0))):
        duong(ve, p0, p1, DO, 14 if mo else 26, vien=False)
    for i, (x, (y0, y1)) in enumerate(zip(N_X, N_Y), 1):
        duong(ve, (x, y0), (x, y1), XANH, rong, vien=not mo)
        if not mo:
            u, v = px(x, y1)
            nhan_vien(ve, (u + 95, v), f"N{i}", XANH, mau_chu=TRANG)
    for i, y in enumerate(C_Y, 1):
        duong(ve, (C_X[0], y), (C_X[1], y), VANG, rong, vien=not mo)
        if not mo:
            u, v = px(C_X[0], y)
            nhan_vien(ve, (u, v - 55), f"C{i}", VANG)


def dai_chu_thich(anh, tieu_de, muc, chan):
    """Thêm dải chú thích trắng phía dưới ảnh. muc = [(màu, kiểu, dòng chính, dòng phụ)]."""
    W, Hh = anh.size
    cao = 300 + sum(105 + (95 if phu else 0) for *_, phu in muc) + 120
    ket = Image.new("RGB", (W, Hh + cao), TRANG)
    ket.paste(anh, (0, 0))
    ve = ImageDraw.Draw(ket)
    f_muc, f_phu = ImageFont.truetype(FONT, 76), ImageFont.truetype(FONT_THUONG, 60)
    ve.text((110, Hh + 70), tieu_de, font=ImageFont.truetype(FONT, 104), fill=DEN)
    y = Hh + 270
    for mau, kieu, chu, phu in muc:
        if kieu == "khung":
            ve.rectangle([110, y + 8, 330, y + 70], outline=mau, width=16)
        elif kieu == "dut":
            for x0 in (110, 200, 290):
                ve.line([(x0, y + 40), (x0 + 50, y + 40)], fill=mau, width=22)
        elif kieu == "cham":
            ve.ellipse([195, y + 15, 245, y + 65], fill=mau, outline=TRANG, width=4)
        else:
            ve.rounded_rectangle([110, y + 22, 330, y + 58], radius=18, fill=mau, outline=DEN, width=3)
        ve.text((390, y), chu, font=f_muc, fill=DEN)
        y += 105
        if phu:
            ve.text((390, y - 4), phu, font=f_phu, fill=(90, 90, 90))
            y += 95
    ve.text((110, Hh + cao - 100), chan, font=ImageFont.truetype(FONT_NGHIENG, 54), fill=(110, 110, 110))
    return ket


def luu(anh, ten):
    KET_QUA.mkdir(exist_ok=True)
    anh.save(KET_QUA / ten, quality=90)
    if HINH_SLIDE.is_dir():
        shutil.copy2(KET_QUA / ten, HINH_SLIDE / ten)
    print(f"Đã lưu {KET_QUA / ten}")


def ve_so_do():
    """Sơ đồ bố trí tuyến (slide 3)."""
    anh = Image.open(ANH).convert("RGB")
    ve = ImageDraw.Draw(anh)
    ve_khung_tuyen(ve)
    kich_thuoc(ve, (-0.75, 0), (-0.75, RONG), m(RONG))
    kich_thuoc(ve, (-0.3, 0), (-0.3, C_Y[0]), m(C_Y[0]), co=40)
    for a, b in zip(C_Y[:-1], C_Y[1:]):
        kich_thuoc(ve, (-0.3, a), (-0.3, b), m(b - a, 0), co=40)
    kich_thuoc(ve, (0, -0.95), (DAI, -0.95), m(DAI, 0), t=0.7)  # nhãn tránh cụm N1–N5
    for a, b in zip(N_X[:-1], N_X[1:]):
        u, v = px((a + b) / 2, -0.35)
        nhan_vien(ve, (u, v), m(b - a), TRANG, co=36)
    ket = dai_chu_thich(anh, "GPR SURVEY LINE LAYOUT", [
        (DO, "khung", f"Survey area: {DAI:.0f} m long × {RONG} m wide", None),
        (VANG, "dai", "C1–C4: lines along the road – to find the cable",
         "1 m apart · C1 is 0.5 m from the left edge · C4 on the right edge"),
        (XANH, "dai", "N1–N5: lines across the road – to find the water pipe",
         f"About {KC_N:.1f} m apart · each starts or ends at the road edge by the benches")],
        "Perspective photo: the grid is drawn approximately to scale.")
    luu(ket, "SoDoTuyen_IMG_9558.jpg")


def ve_ket_qua(duong_ong_cap, mo_ta_do_sau):
    """Ống nước và cáp tìm được, vẽ lên ảnh (slide 5 và 7). duong_ong_cap: kết quả duong_ong_cap() trong dung_ban_do_3d;
    mo_ta_do_sau: một câu (tiếng Anh) nói độ sâu được tính thế nào, in ở chân hình."""
    anh = Image.open(ANH).convert("RGBA")
    nen = Image.new("RGBA", anh.size, (0, 0, 0, 0))
    ve_khung_tuyen(ImageDraw.Draw(nen), mo=True)
    nen.putalpha(nen.getchannel("A").point(lambda a: int(a * 0.55)))  # tuyến đo mờ đi
    anh = Image.alpha_composite(anh, nen).convert("RGB")
    ve = ImageDraw.Draw(anh)
    mau = {"ong_nuoc": MAU_ONG, "cap": MAU_CAP, "khac": MAU_KHAC}
    sau = {}
    for ten, d in duong_ong_cap.items():
        c = mau.get(d["loai"], MAU_KHAC)
        if d["quan_sat"] is not None:
            for doan in d["du_doan"]:
                diem = list(zip(*map(lambda a: a.tolist(), px(doan[:, 0], doan[:, 1]))))
                net_dut(ve, diem, DEN, 30)
                net_dut(ve, diem, c, 22)
            q = d["quan_sat"]
            diem = list(zip(*map(lambda a: a.tolist(), px(q[:, 0], q[:, 1]))))
            ve.line(diem, fill=DEN, width=48, joint="curve")
            ve.line(diem, fill=c, width=38, joint="curve")
        da_ghi = []
        for p in d["diem"]:
            u, w_ = map(float, px(p["x"], p["y"]))
            r = 26 if d["loai"] != "khac" else 20
            ve.ellipse([u - r, w_ - r, u + r, w_ + r], fill=c, outline=TRANG, width=6)
            if d["loai"] != "khac" and all(np.hypot(p["x"] - a, p["y"] - b) > 0.3 for a, b in da_ghi):
                da_ghi.append((p["x"], p["y"]))
                lech = (150, -70) if d["loai"] == "ong_nuoc" else (0, 95)  # cáp: nhãn dưới điểm
                nhan_vien(ve, (u + lech[0], w_ + lech[1]), m(p["z"], 2), TRANG, co=46, mau_chu=c)
        if d["loai"] != "khac" and d["quan_sat"] is not None:  # chỉ đường đã nối, không tính điểm lẻ
            sau[d["loai"]] = (min(p["z"] for p in d["diem"]), max(p["z"] for p in d["diem"]),
                              ", ".join(sorted({p["tuyen"] for p in d["diem"] if not p["tuyen"].endswith("_lap")})))
    muc = []
    if "ong_nuoc" in sau:
        muc.append((MAU_ONG, "dai", "Water pipe – runs along the road",
                    f"Found on {sau['ong_nuoc'][2]} · depth to top {sau['ong_nuoc'][0]:.2f}–{sau['ong_nuoc'][1]:.2f} m"))
    if "cap" in sau:
        muc.append((MAU_CAP, "dai", "Power cable – crosses the road",
                    f"Found on {sau['cap'][2]} · depth to top {sau['cap'][0]:.2f}–{sau['cap'][1]:.2f} m"))
    muc += [(DEN, "dut", "Straight-line extension (not measured)", None),
            (MAU_KHAC, "cham", "Unidentified reflector (seen on one line only)", None)]
    ket = dai_chu_thich(anh, "WHAT IS UNDER OUR FEET – GPR RESULT", muc,
                        f"{mo_ta_do_sau} Perspective photo: positions approximate.")
    luu(ket, "KetQua_IMG_9558.jpg")


if __name__ == "__main__":
    ve_so_do()
