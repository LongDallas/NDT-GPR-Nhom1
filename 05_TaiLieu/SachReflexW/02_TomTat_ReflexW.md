# Tóm tắt: REFLEXW 4.5 – Hướng dẫn sử dụng (K.-J. Sandmeier, 2008)

> **Nguồn:** `../reflexw_manual.pdf` (235 trang). Bản tóm tắt này dựa trên việc đọc các chương 0, 1 và phần đầu chương 2, 3, 6 trong sổ tay.
> **Đối tượng:** nhóm seminar “Ứng dụng GPR trong khảo sát hệ thống cáp và công trình ngầm”.

## 1. Phần mềm là gì

REFLEXW là phần mềm xử lý và diễn giải dữ liệu **địa vật lý 2D/3D** (GPR, địa chấn, radar). Gồm bốn mô-đun:

| Mô-đun | Chức năng |
|---|---|
| **2D-Data-Analysis** | Nhập dữ liệu, lọc, chọn sóng tới (picking), thích nghi vận tốc, layer-show – *mô-đun chính cho GPR* |
| **CMP velocity analysis** | Phân bố vận tốc–độ sâu 1D từ dữ liệu CMP (semblance) |
| **3D data-interpretation** | Hiển thị lát cắt x, y, thời gian (timeslice) từ khối 3D |
| **Modelling** | Mô phỏng sai phân hữu hạn (FD), dò tia, tomography |

Tổ chức dữ liệu theo **dự án**: thư mục chuẩn → thư mục dự án → các thư mục con `ASCII` (dữ liệu gốc), `ROHDATA` (đã chuyển sang định dạng REFLEX), `PROCDATA` (đã xử lý), `LINEDATA` (điểm chọn), `MODEL`.

## 2. Quy trình chuẩn cho dữ liệu GPR (theo sổ tay)

Sổ tay đưa ra một chuỗi lọc chuẩn cho dữ liệu radar thô (RAMAC, PULSEEKKO):

1. **Nhập** (File/Import) → chuyển sang định dạng REFLEX, lưu trong ROHDATA.
2. **Subtract-mean (dewow)** – khử thành phần tần số thấp, cửa sổ ≈ một chu kỳ chính.
3. **Static correction / Move starttime** – đưa thời điểm phát về t = 0.
4. **Manual gain (y)** hoặc **energy decay / AGC** – bù suy giảm theo thời gian.
5. **Background removal** (2D-filter) – xóa nền để làm nổi hyperbol.

Sổ tay khuyến cáo: AGC và energy decay **không nên** dùng như bộ lọc khi xử lý tiếp; chỉ dùng để hiển thị.

Các bước sau đó: **migration** (Kirchhoff, Stolt f–k, diffraction stack) để thu gọn hyperbol về đúng vị trí; **khớp vận tốc** trên hyperbol nhiễu xạ; **chọn điểm** và **xuất tọa độ** ra ASCII.

## 3. Các ý chính có liên quan trực tiếp đến đề tài

- **Vận tốc từ hyperbol:** khớp hyperbol tương tác (Velocity adaptation, kiểu D) là cách lấy vận tốc trung bình đúng cho vùng đo; các tham số *radius* (bán kính ống/cáp) và *angle* (góc giữa tuyến và vật) ảnh hưởng đến hình dạng hyperbol.
- **Migration là bắt buộc để đo kích thước/vị trí vật:** sổ tay nhấn mạnh migration làm *co* năng lượng nhiễu xạ về điểm nguồn; với vật tròn nhỏ như cáp, Kirchhoff thường tốt hơn Stolt vì có thể giới hạn độ rộng cộng.
- **Lát cắt thời gian (timeslice)** là cách nhìn bình đồ các cáp/ống nằm ngang; cần **hiệu chỉnh tĩnh** chung và migration trước.
- **Chọn điểm tự động** (Auto-Pick, loại *single objects*) có thể liệt kê vị trí vật trên nhiều tuyến, kèm kiểm tra bằng tay.
- **Xuất tọa độ:** tọa độ đầu vết (GPS hoặc tính từ đầu file) được ghi cùng điểm chọn ở định dạng ASCII, dùng để vẽ bản đồ trong AutoCAD/QGIS.
- **Thời điểm phát (shot time):** radar không ghi chính xác lúc phát nên phải hiệu chỉnh start time, rồi cập nhật lại khuếch đại trong đầu file.
- **Marker thay cho bánh xe đo:** nếu đo đánh dấu tay mỗi 1 m, phải chạy *markerinterpol* để tọa độ vết đúng.

## 4. Lưu ý khi dùng sổ tay

- Sổ tay viết cho **phiên bản 4.5**, giao diện Windows; một số tính năng (dongle, băng từ Exabyte, định dạng DOS) đã lỗi thời.
- REFLEXW là phần mềm **có bản quyền** (K.-J. Sandmeier). Nhóm chỉ được dùng theo giấy phép của Bộ môn; không được phân phối lại tài liệu gốc.
- Nhóm **chưa xác minh** có REFLEXW trong phòng thí nghiệm hay không (xem `05_TaiLieu/ThietBi_BoMon.md`). Phần mềm xử lý GPR đang dùng trong đề tài là `04_XuLy_MoPhong/xu_ly_bscan.py` và gprMax.
