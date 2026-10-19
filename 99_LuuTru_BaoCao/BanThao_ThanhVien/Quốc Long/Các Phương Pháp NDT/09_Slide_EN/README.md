# Slide thuyết trình (tiếng Anh) – Phân loại theme và bố cục

> Theme được chọn qua bình chọn trong nhóm (trang bình chọn đã đóng).
> Dàn ý nội dung 15 slide: [DanY_Slide_EN.md](DanY_Slide_EN.md)

## 1. Nguyên tắc phân loại

Thiết kế một bộ slide gồm bốn lớp **độc lập** với nhau. Nhóm quyết định từng lớp riêng, theo thứ tự từ tổng thể đến chi tiết. Đổi lớp này không buộc phải đổi lớp kia.

| Lớp | Trả lời câu hỏi | Ví dụ | Bình chọn? |
|---|---|---|---|
| **1. Theme** (giao diện) | Slide *trông* thế nào: màu, phông chữ, nền, thanh tiêu đề, chân trang | Metropolis, Blueprint | ✅ chọn 1 |
| **2. Cấu trúc bài nói** (macro-structure) | Bài nói đi theo *trình tự* nào, mỗi phần bao nhiêu phút | IMRaD, Vấn đề → Giải pháp | ✅ chọn 1 |
| **3. Kiểu slide nội dung** (micro-structure) | Một slide thân bài *dựng* thế nào: tiêu đề, chữ, hình | Assertion–Evidence, gạch đầu dòng | ✅ chọn 1 |
| **4. Thư viện bố cục** (layout archetypes) | Những *khuôn* slide nào cần có cho từng loại thông tin | Bìa, công thức, bảng số liệu | ❌ tham khảo |

## 2. Lớp 1 – Theme (6 lựa chọn)

| Theme | Cảm giác | Phông chữ | Bảng màu chính | Hợp với | Lưu ý |
|---|---|---|---|---|---|
| Học thuật HCMUS | Trang trọng, đúng chuẩn trường | Source Sans 3 | Trắng · xanh #0B4A9E · vàng #C9A227 | Hội đồng chấm truyền thống | In đẹp, an toàn nhất |
| Metropolis (Beamer) | Tối giản, quen thuộc trong khoa học | Fira Sans | Xám #23373B · cam #EB811B | Hội nghị, nhiều công thức | Có bản LaTeX gốc nếu nhóm dùng Beamer |
| Swiss Grid | Sắc nét, kỹ thuật | Archivo | Trắng · đen · đỏ #E5341D | Thông điệp ngắn, hình lớn | Cần kỷ luật căn lưới |
| Radargram Dark | Hiện đại, chất đo đạc | Barlow + JetBrains Mono | Nền #0D1117 · hổ phách · xanh lơ | Chiếu phòng tối; ảnh B-scan | Không hợp để in |
| Soil Strata | Gần gũi, kể chuyện | Bitter + Work Sans | Các lớp đất nâu – vàng đất | Người nghe phổ thông | Họa tiết lớp đất chỉ dùng ở bìa |
| Blueprint | Bản vẽ kỹ thuật công trình | Overpass + Overpass Mono | Xanh bản vẽ #0E3A63 · vàng #FFD166 | Sơ đồ tuyến, hạ tầng ngầm | Nền tối, cần kiểm tra máy chiếu |

**Tiêu chí chọn:** (1) đọc rõ trên máy chiếu của phòng học; (2) ảnh radargram xám đen nổi trên nền; (3) dễ làm lại trong PowerPoint; (4) hợp với hội đồng chấm.

## 3. Lớp 2 – Cấu trúc bài nói (3 lựa chọn, giả định 12 phút)

| Cấu trúc | Trình tự (phút) | Ưu điểm | Hạn chế |
|---|---|---|---|
| **IMRaD** | Title 0,5 · Outline 0,5 · Introduction 2 · Literature 1 · Methods 3 · Results 3 · Discussion 1 · Conclusion 0,5 · Q&A 0,5 | Chuẩn bài báo khoa học, dễ theo dõi | Dễ khô nếu mở đầu dài |
| **Vấn đề → Giải pháp → Bằng chứng** | Hook 1 · Problem 1,5 · Approach 2 · How it works 2,5 · Evidence 3 · Limits 1 · Takeaways 0,5 · Q&A 0,5 | Thu hút, mạch lạc như kể chuyện | Cần ví dụ thực tế mạnh để mở đầu |
| **Theo chương báo cáo** | Title 0,5 · Introduction 1,5 · Ch.1 2,5 · Ch.2 4 · Ch.3 2,5 · Conclusion 0,5 · Q&A 0,5 | Khớp với báo cáo in, dễ chia việc | Lặp lại báo cáo |

Hỏi thầy thời lượng thật (câu E4 trong `00_QuanLy/CauHoi_HoiThay.md`) rồi nhân tỉ lệ lại.

## 4. Lớp 3 – Kiểu slide nội dung (4 lựa chọn)

| Kiểu | Cách dựng | Dùng tốt nhất cho |
|---|---|---|
| **Assertion–Evidence** | Tiêu đề là một câu khẳng định đầy đủ, thân slide là hình minh chứng (Michael Alley, Penn State) | Kết quả, cơ chế vật lý |
| **Chủ đề + gạch đầu dòng** | Tiêu đề ngắn, 3–5 gạch đầu dòng | Mục lục, giới thiệu nhanh |
| **Hai cột: chữ + hình** | Trái 2–3 ý hoặc công thức, phải hình | Lý thuyết có công thức |
| **Hình toàn khung + chú thích** | Một hình lớn, vòng đánh dấu và chú thích trên hình | Radargram, bản đồ tuyến |

Có thể kết hợp: chọn một kiểu **chủ đạo** cho phần thân bài, các slide khác lấy khuôn ở Lớp 4.

## 5. Lớp 4 – Thư viện bố cục (tham khảo)

| Bố cục | Vị trí trong dàn ý 15 slide | Quy tắc |
|---|---|---|
| Bìa (Title) | 1 | Đề tài, nhóm, người hướng dẫn, logo, ngày |
| Mục lục (Outline) | 2 | 4–6 mục, đánh dấu mục hiện tại |
| Chuyển phần (Section) | Trước mỗi phần lớn | Số phần và tên phần, chữ lớn |
| Công thức (Equation) | 6 | Một công thức ở giữa, giải thích ký hiệu |
| So sánh (Comparison) | 5 | Các cột cùng tiêu chí |
| Quy trình (Process) | 9 | Bước nối bằng mũi tên, mỗi bước 2–4 chữ |
| Hình có chú thích | 7, 10, 12 | Đánh dấu hyperbol, ghi độ sâu trên hình |
| Bảng số liệu | 12 | Tối đa 5 hàng × 4 cột |
| Thông điệp chính (Takeaways) | 14 | Ba kết luận, mỗi kết luận một câu |
| Tài liệu & Hỏi đáp | 15 | 3–5 tài liệu chính, "Questions?" |

## 6. Cách bình chọn

1. Mở trang bình chọn, xem 6 theme (bấm *Bìa / Nội dung / Kết quả* để so sánh), 3 cấu trúc và 4 kiểu slide.
2. Mỗi lớp bấm **Bình chọn** cho 1 lựa chọn; bấm lại để bỏ. Bảng kiểm phiếu ở đầu trang cập nhật ngay.
3. **Chia sẻ cho nhóm:** chủ trang mở menu *Share* của trang và **mời từng bạn qua email với quyền Editor**. Bạn ở ngoài tổ chức mở bằng link công khai chỉ có quyền xem nên không bỏ phiếu được.
4. Nếu không bỏ phiếu chung được, bấm **Sao chép phiếu** và dán vào nhóm chat (Zalo/Messenger).
5. Lựa chọn thắng ở mỗi lớp được ghi vào bảng dưới đây.

| Lớp | Kết quả | Ngày chốt |
|---|---|---|
| Theme | | |
| Cấu trúc | | |
| Kiểu slide | | |
