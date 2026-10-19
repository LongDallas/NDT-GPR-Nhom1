# Thiết bị có thể sử dụng cho đề tài

> Cập nhật ngày 07/10/2026, tổng hợp từ nguồn công khai trên Internet.
> **Mọi thiết bị đánh dấu ⚠️ cần hỏi lại giảng viên phụ trách / cán bộ PTN trước khi đưa vào báo cáo.**

## 1. Bộ môn Vật lý Hạt nhân – Phòng thí nghiệm Kỹ thuật Hạt nhân (PTN KTHN)

- Đơn vị: Khoa Vật lý – Vật lý Kỹ thuật, Trường ĐH Khoa học Tự nhiên, ĐHQG-HCM
- Văn phòng Bộ môn: Phòng E304, Tòa nhà E (cơ sở Nguyễn Văn Cừ), ĐT 028-38-304092
- PTN KTHN: thành lập năm 2012, đặt tại Tòa B2-3, cơ sở Linh Trung (Khu đô thị ĐHQG); Trưởng PTN: PGS.TS. Lê Công Hảo
- Hướng nghiên cứu: phân tích phóng xạ môi trường; ứng dụng kỹ thuật hạt nhân trong công nghiệp và xây dựng; phát triển hệ đo hạt nhân; phân tích nguyên tố bằng phổ tia X
- Nguồn: <https://ntlab.hcmus.edu.vn/?page_id=298> (trang "Hệ thiết bị")

| # | Thiết bị | Hãng / Model | Thành phần chính | Công dụng | Liên quan NDT? |
|---|---|---|---|---|---|
| 1 | Hệ phổ kế huỳnh quang tia X (EDXRF) | không ghi | Nguồn Am-241, đầu dò Si(Li), tiền KĐ, DSA-LX, phần mềm WinAXIL | Phân tích nguyên tố, kiểm tra không phá hủy | ✅ |
| 2 | Hệ đo gamma truyền qua | không ghi | Nguồn Cs-137, Am-241; đầu dò NaI(Tl); ống chuẩn trực chì | Đo bề dày, mật độ, phát hiện lỗ rỗng | ✅ (NDT phóng xạ) |
| 3 | Hệ phổ kế gamma HPGe | Canberra GC3520 | HPGe đồng trục loại p, làm lạnh LN₂, buồng chì, Lynx DSA | Phân tích phóng xạ môi trường | – |
| 4 | Hệ đếm tổng alpha/beta | Canberra LB4200 | 4 ống đếm tỉ lệ khí P10, phản trùng phùng, Apex-Alpha/Beta | Tổng hoạt độ α/β | – |
| 5 | Hệ phổ kế alpha | ORTEC Alpha Ensemble | 2 đầu dò PIPS 1200 mm², buồng chân không, MAESTRO | Phổ alpha | – |
| 6 | Máy đo radon | Durridge RAD8 | Bơm khí, RAD H2O, Soil Gas Probe | Radon trong không khí, nước, khí đất | – |

Ngoài ra, học phần *Thực tập cơ sở Kỹ thuật hạt nhân* có dùng ống đếm Geiger–Müller, đầu dò NaI(Tl), hệ phổ kế HPGe, phổ kế alpha và phổ kế tia X
(nguồn: <https://phys.hcmus.edu.vn/en/mon-hoc/nte10104-thuc-tap-co-so-ky-thuat-hat-nhan>).

## 2. Thiết bị chính của đề tài (GPR và RD7000)

| Thiết bị | Tình trạng xác minh | Ghi chú |
|---|---|---|
| **Máy GPR – IDS Detector Duo** (anten kép có bọc chắn 250 MHz + 700 MHz) | ⚠️ Có trong các bài báo của **Bộ môn Vật lý Địa cầu** – HCMUS (đo tại đường Nguyễn Hồng, Gò Vấp và khu công nghiệp Đồng Nai) | Hỏi giảng viên xem máy thuộc Bộ môn nào và cách mượn. Nếu dùng máy khác, sửa lại tên, tần số và thông số |
| **Máy dò cáp Radiodetection RD7000 / RD7000+** (máy thu + máy phát Tx) | ⚠️ README của môn có nhắc RD7000 nhưng **không thấy trong danh mục công khai** của PTN KTHN | Ghi lại model chính xác (RD7000 DL/PL/TL hoặc RD7000+), các tần số mà máy phát hỗ trợ, phiên bản phần mềm |
| Phần mềm xử lý GPR | ⚠️ ReflexW (dùng trong bài Đặng Hoàng Duy và cs., 2020); GPRTVN (do Bộ môn Vật lý Địa cầu phát triển) | Có thể thay bằng gprMax (mô phỏng) và `04_XuLy_MoPhong/xu_ly_bscan.py` (xử lý cơ bản) |

### Thông số RD7000+ theo nhà sản xuất và nhà phân phối (cần đối chiếu với sổ tay của máy thực tế)

- Chế độ thụ động: Power (50/60 Hz) và Radio (VLF). Chế độ chủ động: dùng tần số của máy phát Tx (kết nối trực tiếp, kẹp, cảm ứng)
- Độ nhạy: 5 µA ở 1 m (33 kHz); dải động: 140 dB rms/√Hz
- Sai số độ sâu: ±5 %; độ sâu tối đa khoảng 6 m (tuyến cáp/ống) và 15 m (sonde)
- Nguồn: <https://store.ttech.vn/thiet-bi-xac-dinh-duong-di-cua-cap-dien-duong-ong-cap-vien-thong---rd7000plus---radiodetection-p3675>,
  <https://microprecision.com/calibration/radiodetection-rd-7000-cable-avoidance-tool-system-pipe-locator-rd7000/>

## 3. Câu hỏi cần hỏi giảng viên trước khi đo

1. Bộ môn có máy GPR nào (hãng, model, tần số anten, có bánh xe đo khoảng cách hay GPS không)? Nếu không có, có mượn được máy của Bộ môn Vật lý Địa cầu không?
2. Model RD7000 cụ thể là gì, đi kèm máy phát Tx nào, có kẹp (clamp) và sonde không?
3. Đo ở bãi thử trong trường hay ở hiện trường thật? Có bản vẽ hoàn công để đối chiếu không?
4. Có phần mềm ReflexW / GPRTVN bản quyền để dùng không?
5. Có cần giấy phép hay xin phép đơn vị quản lý hạ tầng khi đo ngoài đường không?
