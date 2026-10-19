# Áp dụng REFLEXW vào đề tài: khảo sát cáp và công trình ngầm bằng GPR

> **Dựa trên:** `../../04_XuLy_MoPhong/xu-ly-du-lieu-gpr.md` (quy trình xử lý của nhóm), `../QuyTrinh_KhaoSat.md`, `../../04_XuLy_MoPhong/gprMax/cap_ngam_2D.in`, `../../04_XuLy_MoPhong/xu_ly_bscan.py`, `../ThietBi_BoMon.md`, và sổ tay REFLEXW trong thư mục này (`reflexw_manual.pdf`).
> **Mục đích:** chọn lọc các hướng trong sổ tay REFLEXW có liên quan, và ánh xạ từng bước xử lý của nhóm sang chức năng cụ thể của REFLEXW.

## 1. Ánh xạ quy trình xử lý của nhóm sang REFLEXW

Quy trình trong `xu-ly-du-lieu-gpr.md` có 4 nhóm bước. Dưới đây là chức năng tương ứng trong REFLEXW (số mục trong sổ tay trong ngoặc).

| Bước của nhóm | Chức năng REFLEXW | Ghi chú cho đề tài |
|---|---|---|
| **1. Move start time** | *Processing → StaticCorrection/muting → Move starttime* (1.11.3.3); hoặc *correct max. phase* (1.11.3.7) để tự tìm pha | Đưa time-zero về mặt đất. Với anten IDS 700 MHz, kiểm tra lại start time sau bước này |
| **2. Bộ lọc 1D** | *subtract-mean (dewow)* (1.11.1.9); *subtract DC-shift* (1.11.1.10); *bandpass frequency* (1.11.1.3) | Cửa sổ dewow ≈ 1 chu kỳ: **1,43 ns cho 700 MHz**, 4 ns cho 250 MHz. Bandpass đặt quanh tần số anten |
| **3. Bộ lọc 2D** | *background removal* (1.11.8.3); *running average* (1.11.8.1); *median xy-filter* (1.11.8.5) | Xóa nền để làm nổi hyperbol cáp/ống; **không xóa nền khi xác định ranh giới lớp** (mặt phản xạ nằm ngang bị mất) |
| **4. Khuếch đại** | *manual gain (y)* (1.11.2.6); *AGC* và *energy decay* (1.11.2.1–2) chỉ để hiển thị; *gain function* (1.11.2.3) | Sổ tay khuyên không dùng AGC như bộ lọc khi xử lý tiếp |
| **Xác định kích thước: migration** | *Kirchhoff* (1.11.9.2), *Stolt f–k* (1.11.9.3), *diffraction 2D-veloc* (1.11.9.5), *FD-migration* (1.11.9.7) | Với vật tròn nhỏ (cáp, ống): Kirchhoff có thể giới hạn độ rộng cộng |

## 2. Quy trình đề xuất trong REFLEXW cho một tuyến đo

Áp dụng cho dữ liệu thực địa (`03_DuLieuHienTruong/Data - processed`) và dữ liệu mô phỏng gprMax sau khi xuất sang ASCII-MATRIX:

1. **Nhập**: *File → Import*, định dạng tương ứng (RADAN, IDS, hoặc ASCII-MATRIX cho dữ liệu gprMax). Chọn *data type = const. offset*, bật *read coordinates* nếu có. Bước vết: đo bằng bánh xe thì đọc từ file; đo bằng marker thì chạy bước 3.
2. **Kiểm tra hình học**: *Edit FileHeader* – tọa độ đầu/cuối, bước vết, **start time** và **tần số danh định** (nominal frequency = 700 MHz hoặc 250 MHz). Nếu đo bằng marker, chạy *markerinterpol* (1.11.6.1) để tọa độ vết đúng.
3. **Hiệu chỉnh thời điểm phát** (shot time): xác định time-zero từ sóng truyền thẳng; *move starttime* hoặc *correct max. phase*; cập nhật lại gain trong đầu file.
4. **Lọc 1D**: dewow → bandpass quanh tần số anten.
5. **Khuếch đại**: *manual gain (y)* hoặc *gain function* với a′, b′ tính theo độ suy hao của đất ẩm/khô (nhóm chưa đo được giá trị thực; xem `05_TaiLieu/ThietBi_BoMon.md`).
6. **Xóa nền** (chỉ khi xác định vị trí vật, không dùng cho ranh giới lớp).
7. **Khớp vận tốc** (*Velocity adaptation*, kiểu D – hyperbol): điều chỉnh v, *radius* (bán kính ống/cáp; ví dụ ống PVC D110 → 0,055 m), *angle* (≈ 90° khi tuyến vuông góc với vật). Đây là vận tốc dùng để đổi thời gian ra độ sâu.
8. **Migration** (Kirchhoff với vận tốc đã khớp) → vị trí và kích thước vật.
9. **Chọn điểm**: *Pick → Auto-Pick* (loại *single objects*) hoặc chọn tay; kiểm tra bằng *interactive choice → show picks*.
10. **Xuất**: *Pick save → ASCII-columns*, bật *xy-coordinates* và *depths* → bảng vị trí–độ sâu cho bước đối chiếu (mục 5 của `QuyTrinh_KhaoSat.md`).
11. **Lát cắt thời gian** (3D, nếu đo lưới nhiều tuyến): *Generate 3D-file from 2D-files* (3.5) rồi *timeslice* (3.6) – chỉ sau khi đã hiệu chỉnh tĩnh và migration từng tuyến.

## 3. Ứng dụng cho mô phỏng gprMax

- Cần một bước chuyển B-scan từ gprMax (file .out/HDF5) sang văn bản ma trận rồi nhập bằng **ASCII-MATRIX** (1.5.4). **Chưa kiểm chứng**: nhóm chưa chạy thử bước này; có thể dùng trực tiếp `xu_ly_bscan.py` thay thế. Khi nhập phải khai báo *time increment* (theo bước thời gian trong file `.in`: `time_window: 25e-9`, số mẫu tương ứng).
- Ý nghĩa: đối chiếu hyperbol mô phỏng với hyperbol thực để kiểm tra vận tốc và độ sâu – đúng tinh thần bài tập 3.1 trong `cap_ngam_2D.in` (đổi ε_r, đổi tần số, đổi nội dung ống).
- Có thể dùng *Add random noise* (1.11.5.8) để mô phỏng nhiễu trước khi thử chuỗi xử lý.

## 4. Các hướng trong sổ tay **không** áp dụng cho đề tài

| Hướng | Lý do bỏ qua |
|---|---|
| Địa chấn khúc xạ, intercept time, tomography (0.7, 0.10.3–0.10.4, 5, 6.3) | Đề tài dùng GPR/RD7000, không phải địa chấn |
| Địa chấn phản xạ CMP/NMO (0.8, 1.12.4) | Dữ liệu 2D GPR zero-offset không cần cộng CMP |
| Ba thành phần, dipole/frame (1.12.8) | Thiết bị không có |
| Băng từ Exabyte, DOS, dongle (1.5.8, 0.2) | Lỗi thời |
| Yo-Yo section (1.11.6.10) | Giếng khoan, không có trong đề tài |

## 5. Việc cần làm để áp dụng thực tế

- [ ] Xác nhận với giảng viên có **REFLEXW** trong phòng thí nghiệm không; nếu không, dùng `xu_ly_bscan.py` và gprMax (đã ghi trong `05_TaiLieu/ThietBi_BoMon.md`).
- [ ] Kiểm tra **định dạng** dữ liệu máy IDS Detector Duo có được REFLEXW nhập trực tiếp không (sổ tay liệt kê IDS trong 1.5).
- [ ] Đo thử một tuyến có vật đã biết (ống/cáp) để kiểm tra chuỗi: start time → dewow → bandpass → gain → migration → khớp vận tốc.
- [ ] Ghi lại các tham số đã dùng (vận tốc, radius, angle, độ rộng migration, nhãn xử lý) vào `03_DuLieuHienTruong/NhatKy_HienTruong.md` và *File → Processing flow → export to ASCII* để báo cáo có quy trình rõ ràng.
- [ ] Viết lại toàn bộ phần mô tả bằng lời của nhóm, không chép nguyên văn sổ tay (bài sẽ được kiểm tra đạo văn; xem `README_BAO_CAO_CONG_VIEC.md` mục 5).
