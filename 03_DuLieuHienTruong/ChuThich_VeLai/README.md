# ChuThich_VeLai – radargram "New Data" vẽ lại kèm chú thích

Vẽ lại 10 file dữ liệu trong `../New Data/` (kênh 250 MHz) bằng Python, thay cho ảnh chụp màn hình ReflexW
trong `../New Data/GPR_chu_thich_duong_ong.pdf`, kèm các chú thích của nhóm (P1, O1–O5, A1).

```bash
cd 03_DuLieuHienTruong/ChuThich_VeLai
python3 ve_lai_chu_thich.py
```

| File | Nội dung |
|---|---|
| `GPR_chu_thich_ve_lai.pdf` | báo cáo A4: trang 1 gồm vận tốc, chú giải, chiều đo, bảng tóm tắt, sơ đồ mặt bằng; trang 2–6 gồm mỗi tuyến một radargram và bảng chú thích |
| `png/<tuyến>_<file>.png` | từng tuyến một ảnh ngang (radargram + bảng) |

- Vòng tròn đánh dấu đỉnh hyperbol; đường dọc chỉ vị trí x và kéo dài tới hết đuôi tín hiệu (khi bao biên độ còn trên 2,5 lần nền). Màu: đỏ P = cáp / kim loại, cam O = dị thường, xanh A = ống nước.
- Cột **Mô tả** do script đo trên dữ liệu: biên độ đỉnh so với nền của tuyến và thời điểm hết đuôi tín hiệu.
- Điểm chú thích lấy từ `02_SoDoTuyen_BanDo/muc_tieu.csv` (cột `ky_hieu`). Hướng tuyến lấy từ `tuyen_do.csv`. Độ sâu theo mô hình 2 lớp (bê tông 0,12 / đất 0,10 m/ns, xem `02_SoDoTuyen_BanDo/SDT_Tai/README.md`).
- Các file `.T` trong New Data không có header `.R` đi kèm, nên header lấy từ file cùng tên trong `../Data - processed/` (dữ liệu hai nơi giống hệt nhau từng byte).
- C2, C4, N2, N4 đo ngược chiều nên được lật lại. `LZZ20003.11T` là bản XFlip của C3, nên cũng được lật lại về chiều đo để khớp với chú thích.
- `LZZ20010.00T` (đo lặp N5) chưa xử lý trong ReflexW, nên script tự dewow và xóa nền trước khi vẽ.
