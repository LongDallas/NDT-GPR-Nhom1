"""Đọc file ReflexW (.##R = header, .##T = dữ liệu) do ReflexW xuất ra.

Cấu trúc đã kiểm tra trên dữ liệu trong 03_DuLieuHienTruong/Data - processed:
  header (.##R, 2196 byte):
    byte 420  int16   số mẫu mỗi vết (ns)
    byte 422  int16   số vết (ntr)
    byte 460  float32 khoảng cách vết dx (m)
    byte 464  float32 bước thời gian dt (ns)
    byte 468  float32 cửa sổ thời gian (ns)
    byte 500  float32 tọa độ cuối tuyến (m)
  dữ liệu (.##T): mỗi vết = 156 byte trace header + ns mẫu int16 (little-endian).
"""
import struct
from pathlib import Path

import numpy as np

TRACE_HEADER = 156


def doc_header(duong_dan_r):
    b = Path(duong_dan_r).read_bytes()
    ns, ntr = struct.unpack_from("<hh", b, 420)
    dx, dt, cua_so = struct.unpack_from("<fff", b, 460)
    x_cuoi = struct.unpack_from("<f", b, 500)[0]
    # các bước xử lý ReflexW đã áp dụng (chuỗi ASCII có độ dài đứng trước)
    buoc = []
    for ten in (b"move starttime", b"subtract-DC-shift", b"subtract-mean(dewow)",
                b"background removal", b"gain function", b"average xy-filter",
                b"XFlipProfile", b"migration", b"static correction"):
        if ten in b:
            buoc.append(ten.decode())
    return dict(ns=ns, ntr=ntr, dx=dx, dt=dt, cua_so=cua_so, x_cuoi=x_cuoi, buoc_xu_ly=buoc)


def doc_tuyen(duong_dan):
    """Nhận đường dẫn tới .##R hoặc .##T, trả về (B-scan [mẫu, vết] float32, header)."""
    p = Path(duong_dan)
    r = p.with_suffix(p.suffix[:-1] + "R")
    t = p.with_suffix(p.suffix[:-1] + "T")
    h = doc_header(r)
    raw = np.fromfile(t, dtype=np.uint8)
    do_dai = TRACE_HEADER + 2 * h["ns"]
    if raw.size != do_dai * h["ntr"]:
        raise ValueError(f"{t.name}: kích thước {raw.size} không khớp {h['ntr']} vết x {do_dai} byte")
    vet = raw.reshape(h["ntr"], do_dai)[:, TRACE_HEADER:].copy().view("<i2")
    return vet.T.astype(np.float32), h


if __name__ == "__main__":
    import sys

    for f in sys.argv[1:]:
        b, h = doc_tuyen(f)
        print(Path(f).name, b.shape, h)
