# Quy trình khảo sát cáp và công trình ngầm bằng GPR kết hợp RD7000

> Dùng cho mục 2.4 "Quy trình thực hiện" của báo cáo. Tham chiếu: ASTM D6432-19, PAS 128:2022, Metje et al. (2007), Royal et al. (2011).
> Hai phương pháp bổ sung cho nhau. **RD7000** chỉ dò được vật dẫn điện (cáp, ống kim loại, hoặc ống có dây dò/sonde) nhưng định tuyến nhanh và ít bị ảnh hưởng bởi đất ẩm.
> **GPR** thấy được cả ống phi kim (PVC, HDPE, bê tông) và cho độ sâu, nhưng tín hiệu suy giảm mạnh trong đất sét ẩm hoặc nhiễm mặn.

## Bước 0 – Chuẩn bị (trong phòng)

- [ ] Thu thập bản vẽ hoàn công, bản đồ hạ tầng và thông tin từ đơn vị quản lý (điện lực, cấp nước, viễn thông)
- [ ] Mô phỏng trước bằng gprMax (`04_MoPhong_gprMax/`) để chọn tần số anten và cửa sổ thời gian
- [ ] Kiểm tra thiết bị: pin GPR, pin RD7000 và máy phát Tx, dây kết nối, kẹp, cọc tiếp đất, bánh xe đo khoảng cách
- [ ] Đồ bảo hộ: áo phản quang, biển báo, găng cách điện (khi kẹp cáp)
- [ ] Phân công: 1 người vận hành, 1 người ghi nhật ký và đánh dấu, 1 người chụp ảnh và cảnh giới giao thông

## Bước 1 – Trinh sát hiện trường

- [ ] Xác định ranh giới khu đo, chụp ảnh toàn cảnh, ghi loại mặt đường (nhựa, bê tông, đất)
- [ ] Đánh dấu dấu hiệu nổi: nắp hố ga, tủ điện, trụ cứu hỏa, đồng hồ nước, hộp cáp
- [ ] Lập lưới tuyến đo. Tuyến chính **vuông góc** với hướng dự kiến của cáp/ống; khoảng cách tuyến 0,5–2 m

## Bước 2 – Quét bằng RD7000 (định tuyến nhanh)

1. **Thụ động – Power (50/60 Hz):** quét zigzag cả khu vực để tìm cáp điện đang mang tải
2. **Thụ động – Radio (VLF):** tìm thêm cáp/ống kim loại dài có tín hiệu radio cảm ứng
3. **Chủ động – Tx (nếu tiếp cận được đầu cáp/ống):**
   - Kết nối trực tiếp (direct connection): tín hiệu mạnh nhất, dùng cho ống kim loại hoặc cáp đã cắt điện
   - Kẹp (clamp): cho cáp đang mang điện, **không** cần cắt điện
   - Cảm ứng (induction): đặt Tx trên mặt đất phía trên tuyến
   - Sonde: luồn vào ống phi kim để dò
4. Tại mỗi điểm đánh dấu: dùng **peak** để tìm vị trí, kiểm tra lại bằng **null**. Nếu hai vị trí lệch nhau nhiều thì trường bị méo do cáp khác ở gần
5. Ghi **độ sâu** và **dòng tín hiệu** (current) mà máy hiển thị. Đánh dấu bằng sơn hoặc cờ, đo tọa độ (GNSS hoặc thước dây so với mốc cố định)

## Bước 3 – Đo GPR

| Thông số | Giá trị gợi ý | Ghi chú |
|---|---|---|
| Tần số anten | 250 MHz (đến ~3 m) và 700 MHz (≤ 2 m, độ phân giải cao) | Detector Duo đo đồng thời 2 tần số |
| Cửa sổ thời gian | 60–100 ns (250 MHz); 30–50 ns (700 MHz) | Chọn ≈ 1,3 × (2·d_max / v) |
| Số mẫu / vết | 512 | |
| Khoảng cách vết | 1–2 cm | Dùng bánh xe đo khoảng cách |
| Hiệu chỉnh vận tốc | Khớp hyperbol trên một đối tượng đã biết độ sâu | Hoặc dùng phương pháp CMP nếu có anten tách rời |

- [ ] Đo các tuyến **vuông góc** với tuyến RD7000 đã đánh dấu để thấy hyperbol rõ nhất
- [ ] Đo thêm các tuyến song song để dựng mặt cắt 3D hoặc bản đồ lát cắt theo độ sâu (C-scan)
- [ ] Ghi tên file của từng tuyến vào nhật ký (mẫu ở `05_DuLieuHienTruong/NhatKy_HienTruong.md`)

## Bước 4 – Xử lý dữ liệu GPR

1. Hiệu chỉnh thời gian không (time-zero)
2. Khử dewow (bỏ thành phần tần số thấp)
3. Lọc thông dải (band-pass) quanh tần số trung tâm của anten
4. Xóa nền (background removal, trừ vết trung bình) để làm nổi hyperbol
5. Khuếch đại theo thời gian (gain SEC/AGC)
6. Phân tích vận tốc bằng khớp hyperbol; dịch chuyển (Kirchhoff hoặc F-K migration)
7. Đổi thời gian ra độ sâu theo `d = v·t/2`; minh giải (vị trí, độ sâu, kim loại hay phi kim)

Script mẫu: `06_XuLyPhanTich/xu_ly_bscan.py` (bước 1, 2, 4, 5 và khớp hyperbol).

## Bước 5 – Đối chiếu và đánh giá

- [ ] Lập bảng so sánh: vị trí và độ sâu theo GPR, theo RD7000, theo bản vẽ hoàn công; tính sai lệch
- [ ] Phân cấp độ tin cậy theo PAS 128 hoặc ASCE 38 (nếu áp dụng được)
- [ ] Vẽ bản đồ công trình ngầm (QGIS hoặc AutoCAD) với ký hiệu riêng cho từng loại cáp/ống

## An toàn

- Không đo GPR gần nguồn phát sóng mạnh nếu chưa ghi chú (trạm BTS có thể gây nhiễu)
- Khi dùng Tx kết nối trực tiếp: **không** nối vào cáp đang mang điện; dùng kẹp
- Tuân thủ quy định giao thông khi đo trên đường; có người cảnh giới
