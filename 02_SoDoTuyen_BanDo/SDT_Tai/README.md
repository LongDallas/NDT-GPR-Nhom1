# SDT_Tai – Hình mặt cắt GPR theo mẫu trình bày

Hai ảnh `.jpg` trong thư mục này là **mẫu trình bày**: trang "Bản đồ công trình ngầm cho ga ngầm Metro" và trang "Xác định cáp dự ứng lực".
Script `ve_mat_cat_gpr.py` vẽ lại cùng kiểu đó cho dữ liệu của nhóm.

**Nguồn số liệu (cập nhật 18/10/2026):** vị trí và phân loại dị thường theo bản chú thích mới của nhóm
`03_DuLieuHienTruong/New Data/GPR_chu_thich_duong_ong.pdf`, đã chép vào `../muc_tieu.csv` (cột `ky_hieu`).
Hướng tuyến lấy theo `../tuyen_do.csv`.

```bash
cd 02_SoDoTuyen_BanDo/SDT_Tai
python3 ve_mat_cat_gpr.py      # ghi vào ket_qua/ và tự chép sang 01_Slide/HinhAnh/
```

| Hình (16:9) | Nội dung | Theo mẫu |
|---|---|---|
| `ket_qua/Hinh1_Cap_MatCatGPR.png` | (a) C1 cả tuyến: P1 (cáp) và O1, O2, O3, hyperbol lý thuyết trên P1; (b) C3: P1 và O5; (c) C1 sau migration; (d) kích thước dị vật; sơ đồ tuyến thu nhỏ | ảnh mẫu 1 |
| `ket_qua/Hinh2_OngNuoc_MatCatGPR.png` | (a) N2: A1 (ống nước); (b) N1: không thấy hyperbol rõ; (c) N2 sau migration; (d) phóng to hyperbol A1 | ảnh mẫu 1 |
| `ket_qua/Hinh3_VungTinHieu.png` | Tuyến C1: (a) đã lọc, (b) sau Kirchhoff migration, (c) phóng to vùng tín hiệu quanh P1 (khung đỏ) | ảnh mẫu 2 |

## Các điểm nhóm đã chú thích (kênh 250 MHz)

Ký hiệu và màu giống bản PDF: **P** đỏ = cáp / vật kim loại, **O** cam = dị thường, **A** xanh = ống nước.
`x` là khoảng cách trên mặt cắt đã lật về cùng chiều (như nhóm xem trong ReflexW); mặt bằng theo hệ toạ độ của `tuyen_do.csv`.

| Ký hiệu | Tuyến | x (m) | t (ns) | Độ sâu (m) | Mặt bằng (x; y) |
|---|---|---|---|---|---|
| P1 | C1 | 3,8 | 12,0 | 0,65 | 2,50; 0,5 |
| P1 | C2 | 4,4 | 7,9 | 0,45 | 2,50; 1,5 |
| P1 | C3 | 3,8 | 8,2 | 0,46 | 2,50; 2,5 |
| P1 | C4 | 3,0 | 7,6 | 0,43 | 2,50; 3,5 |
| A1 | N2 | 2,25 | 7,6 | 0,43 | 2,10; 2,41 (cách mép phía ghế đá 1,09 m) |
| O1 / O2 / O3 | C1 | 2,63 / 7,4 / 10,5 | 15,5 / 16,8 / 10,1 | 0,82 / 0,89 / 0,55 | 1,33 / 6,10 / 9,20; 0,5 |
| O4 | C2 | 2,8 | 7,9 | 0,45 | 0,90; 1,5 |
| O5 | C3 | 2,0 | 4,25 | 0,26 | 0,70; 2,5 |

- N1: nhóm ghi "không thấy hyperbol hay dị thường rõ". N3, N4, N5: chưa có bảng chú thích.
- **O5:** bảng của nhóm ghi độ sâu 0,40 m, nhưng t = 4,25 ns chỉ ứng với khoảng 0,26 m (nằm trong lớp bê tông). Cần nhóm kiểm tra lại.
- **Cáp cắt ngang vuông góc với đường ở x ≈ 2,5 m, đi qua P1 trên cả 4 tuyến C1–C4.** Hiện trường xác nhận: 3 dấu đánh trên mặt đất thẳng hàng, vuông góc với mép đường.
  Điểm xuất phát của C2, C4 (đo ngược) đã được hiệu chỉnh theo cáp, xem `../README.md` mục 4. P1 trên C1 sâu hơn (0,64 m so với 0,43–0,46 m).

## Độ sâu: mô hình 2 lớp

Bản chú thích dùng **v = 0,12 m/ns trong bê tông** và **v = 0,10 m/ns trong đất**.
Độ sâu = 0,06 · min(t, 5) + 0,05 · max(t − 5, 0), với t là thời gian hai chiều (ns). Lớp bê tông chiếm 5 ns đầu, tức khoảng 0,30 m.
Con số 5 ns được suy ngược từ bảng độ sâu của nhóm: với giá trị này, các độ sâu tính lại lệch không quá 0,02 m so với bảng, trừ O5.
Vì có 2 lớp nên trục độ sâu bên phải mặt cắt không chia đều. Hyperbol lý thuyết vẽ với vận tốc v_rms tới đỉnh (số ghi trên hyperbol).
Ô (c), (d) là dữ liệu đã Kirchhoff migration trong ReflexW với v = 0,095 m/ns (`03_DuLieuHienTruong/SaoLuu/Data_backup_migration/`).

## Chiều đo: đi zigzag

Khi so ảnh ReflexW trong bản chú thích với dữ liệu, thấy nhóm đã **lật (XFlip) C2, C4, N2, N4**: hệ số tương quan khi lật là 0,61–0,67, khi không lật chỉ 0,34–0,51.
Như vậy cả tuyến dọc và tuyến ngang đều đi zigzag. Script lật các tuyến này khi vẽ, để mọi mặt cắt tính khoảng cách từ cùng một đầu: x = −1,3 m với tuyến C, y = −0,64 m với tuyến N.
Sơ đồ tuyến thu nhỏ vẽ mũi tên theo **chiều kéo máy thật**.

## Lưu ý khi trình bày
- **Kích thước ở Hình 1 (d)** (≈ 31 × 14 cm) là **kích thước biểu kiến**, đo là độ rộng tại nửa biên độ của vùng phản xạ sau migration. Con số này bị giới hạn bởi độ phân giải (λ/4 ≈ 10 cm ở 250 MHz), **không phải đường kính cáp**. Độ sâu tới đỉnh sau migration (≈ 0,53 m) nông hơn độ sâu nhóm đọc trên mặt cắt chưa migration (0,65 m).
- **Ống nước không đo kích thước**: chỉ phóng to hyperbol A1 và ghi độ sâu tới đỉnh.

## Bản tiếng Anh cho slide
`python3 ve_mat_cat_gpr.py --en` vẽ lại cả 3 hình với chữ tiếng Anh, lưu thành `Hinh1_Cap_MatCatGPR_EN.png`, `Hinh2_OngNuoc_MatCatGPR_EN.png`, `Hinh3_VungTinHieu_EN.png` (cũng tự chép sang `01_Slide/HinhAnh/`). Slide 4a, 4b và A3 của `01_Slide/Seminar_GPR_EN.pptx` dùng các hình này. File `.pptx` nhúng ảnh, nên phải chèn lại ảnh mới vào slide.

## Bản TikZ (thư mục `tikz/`)
`tikz/hinh_mat_cat_gpr.tex` vẽ lại cả 3 hình bằng TikZ/pgfplots, mỗi hình một trang 16:9. TikZ không vẽ được dữ liệu radar, nên nền B-scan lấy từ `tikz/nen/*.png`. Các phần còn lại (trục, mũi tên, hyperbol, khung kích thước, sơ đồ tuyến, chữ) là code TikZ. Số liệu nằm trong `tikz/so_lieu.tex` do script ghi ra, không cần dán tay.
```bash
cd 02_SoDoTuyen_BanDo/SDT_Tai/tikz
python3 xuat_nen_tikz.py            # tạo nen/*.png và so_lieu.tex
lualatex hinh_mat_cat_gpr.tex       # bản tiếng Việt
lualatex -jobname=hinh_mat_cat_gpr_EN "\def\BanEN{}\input{hinh_mat_cat_gpr}"   # bản tiếng Anh
```
