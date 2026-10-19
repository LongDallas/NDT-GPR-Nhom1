# Báo cáo công việc – Đề tài "Ứng dụng GPR trong khảo sát hệ thống cáp và công trình ngầm"

> Học phần **Các phương pháp NDT** – Bộ môn Vật lý Hạt nhân, Khoa Vật lý – Vật lý Kỹ thuật, Trường ĐH KHTN, ĐHQG-HCM
> Ngày lập: 07/10/2026. File `README.md` gốc (hướng dẫn seminar của môn học) **giữ nguyên, không chỉnh sửa**.

## 1. Tóm tắt những gì đã làm

| # | Hạng mục | Kết quả | Vị trí |
|---|---|---|---|
| 1 | Tìm hiểu thiết bị của Bộ môn | Lập danh mục 6 hệ thiết bị của PTN Kỹ thuật Hạt nhân (từ trang chính thức) và tình trạng xác minh GPR/RD7000 | `02_ThietBi/ThietBi_BoMon.md` |
| 2 | Tạo cấu trúc thư mục đề tài | 11 thư mục chính (quản lý → tài liệu → thiết bị → phương pháp → mô phỏng → dữ liệu → xử lý → hình → báo cáo → slide → phụ lục) | xem mục 3 |
| 3 | Tìm tài liệu trong nước và nước ngoài | 12 tài liệu trong nước, 19 tài liệu nước ngoài, 4 tiêu chuẩn/sổ tay. **28 DOI đã được xác minh** qua CrossRef/OpenAlex | `01_TaiLieuThamKhao/TongHop_TaiLieu.md`, `references.bib` |
| 4 | Viết mẫu báo cáo chuẩn | File Word 30 trang theo quy định trình bày luận văn của Trường ĐH KHTN, bố cục theo đúng `README.md` của môn học, kèm văn bản nháp, 29 trích dẫn, công thức, bảng và hướng dẫn | `08_BaoCao/BaoCao_Seminar_GPR_Mau.docx` |
| 5 | Mô phỏng | Tệp đầu vào gprMax: cáp kim loại và ống PVC trong đất, anten 700 MHz | `04_MoPhong_gprMax/cap_ngam_2D.in` |
| 6 | Xử lý dữ liệu | Script Python: time-zero, dewow, xóa nền, khuếch đại SEC, khớp hyperbol để tìm v, d, εr. Chạy thử trên dữ liệu tổng hợp tìm lại được v = 0,098 m/ns (giá trị đúng 0,100) | `06_XuLyPhanTich/xu_ly_bscan.py` |
| 7 | Hình lý thuyết Chương 2 | Hình 2.1 (đáp ứng Peak/Null của máy dò cáp) và Hình 2.3 (hyperbol GPR theo vận tốc), vẽ từ công thức, in đen trắng được | `07_HinhAnh/Chuong2/`, `06_XuLyPhanTich/ve_hinh_ly_thuyet.py` |
| 8 | Quy trình đo và biểu mẫu | Quy trình khảo sát 5 bước (GPR + RD7000), nhật ký hiện trường mẫu, kế hoạch phân công, dàn ý slide tiếng Anh | `03_PhuongPhap/`, `05_DuLieuHienTruong/`, `00_QuanLy/`, `09_Slide_EN/` |

## 2. Thiết bị của Bộ môn (tóm tắt)

**Đã xác minh** (trang "Hệ thiết bị" của PTN Kỹ thuật Hạt nhân – <https://ntlab.hcmus.edu.vn/?page_id=298>):
EDXRF (Am-241, Si(Li)); hệ đo gamma truyền qua (Cs-137, Am-241, NaI(Tl)), dùng được cho NDT; phổ kế gamma HPGe Canberra GC3520; hệ đếm alpha/beta Canberra LB4200; phổ kế alpha ORTEC Alpha Ensemble; máy đo radon Durridge RAD8.

**Cần hỏi giảng viên** ⚠️:

- **GPR:** máy **IDS Detector Duo** (anten 250/700 MHz) xuất hiện trong các bài báo của **Bộ môn Vật lý Địa cầu** – HCMUS, không thuộc danh mục của Bộ môn Vật lý Hạt nhân.
- **RD7000:** được nhắc trong README của môn học nhưng không có trong danh mục công khai.

## 3. Cấu trúc thư mục

```
Các Phương Pháp NDT/
├── README.md                      ← hướng dẫn gốc của môn học (không sửa)
├── README_BAO_CAO_CONG_VIEC.md    ← file này
├── 00_QuanLy/                     kế hoạch, phân công, biên bản họp
├── 01_TaiLieuThamKhao/            bảng tổng hợp, references.bib; PDF chia theo TrongNuoc/NgoaiNuoc/TieuChuan_PhapLy/SoTayThietBi
├── 02_ThietBi/                    danh mục thiết bị và câu hỏi cho giảng viên
├── 03_PhuongPhap/                 quy trình khảo sát GPR + RD7000
├── 04_MoPhong_gprMax/             tệp .in; KetQua/
├── 05_DuLieuHienTruong/           01_Raw_GPR, 01_Raw_RD7000 (không sửa), 02_DaXuLy, ảnh, nhật ký
├── 06_XuLyPhanTich/               script Python xử lý và vẽ hình
├── 07_HinhAnh/Chuong1..3/         hình gốc dùng trong báo cáo
├── 08_BaoCao/                     mẫu báo cáo .docx; BanNop/ cho bản nộp
├── 09_Slide_EN/                   dàn ý slide tiếng Anh
└── 10_PhuLuc/
```

## 4. Mẫu báo cáo – định dạng đã cài sẵn

Theo *Quy định hình thức trình bày luận văn thạc sĩ* của Trường ĐH KHTN – ĐHQG-HCM, áp dụng cho báo cáo seminar:

- Khổ A4, Times New Roman 13, giãn dòng 1,5; lề trên 3,5 cm, dưới 3 cm, trái 3,5 cm, phải 2 cm; số trang ở giữa cuối trang
- Phần đầu đánh số i, ii, …; **Mở đầu bắt đầu trang 1** (theo README của môn học)
- Đề mục đánh số tối đa 3 cấp (1.1.1); hình, bảng, công thức đánh số theo chương (Hình 2.1, Bảng 3.2, (2.5)); tên bảng đặt trên bảng, tên hình đặt dưới hình
- Trích dẫn dạng số [1] theo thứ tự xuất hiện; danh mục tài liệu theo mẫu "Tác giả (năm). Tên bài, Tạp chí, Số, Trang, doi"; từ 3 tác giả trở lên ghi "và cộng sự" hoặc "et al."
- Thứ tự: Bìa → Giới thiệu nhóm → Lời cảm ơn → Mục lục → Danh mục chữ viết tắt, bảng, hình → Mở đầu → Chương 1–3 → Kết luận và kiến nghị → Tài liệu tham khảo → Phụ lục

**Cách dùng:** chữ **màu xám** là hướng dẫn, cần xóa trước khi in. Ô `[…]` và khung `[CHÈN HÌNH]` cần thay bằng nội dung thật. Sửa xong thì nhấn Ctrl+A rồi F9 (Mac: Cmd+A rồi Fn+F9) để cập nhật mục lục. Bản mẫu hiện có 30 trang (8 trang phần đầu và 22 trang phần chính). Khi chèn hình thật, cần rút gọn văn bản để không vượt **30 trang**.

## 5. Những việc nhóm cần làm tiếp

1. Hỏi giảng viên các câu hỏi trong `02_ThietBi/ThietBi_BoMon.md` (thiết bị, địa điểm, phần mềm, giấy phép đo).
2. Tải PDF tài liệu vào `01_TaiLieuThamKhao/`. Kiểm tra lại tên tiếng Việt của sách Nguyễn Thành Vấn và Nguyễn Văn Giàng (2013).
3. Viết lại văn bản nháp bằng lời văn của nhóm, vì bài sẽ được kiểm tra đạo văn.
4. Cài gprMax (<https://www.gprmax.com>), chạy `cap_ngam_2D.in`, xử lý bằng `xu_ly_bscan.py` (cần `pip install h5py`).
5. Đo hiện trường, điền vào nhật ký, Bảng 3.2–3.4 và các hình của Chương 3.
6. Làm slide tiếng Anh theo `09_Slide_EN/DanY_Slide_EN.md`.

## 6. Công cụ đã dùng và cài đặt

- Skill đã cài: `citation-management` và `literature-review` (K-Dense-AI/scientific-agent-skills, giấy phép MIT), dùng để tìm tài liệu qua OpenAlex và xác minh DOI qua CrossRef.
- Phần mềm cài qua Homebrew để kiểm tra file Word: LibreOffice, poppler, pandoc.
- Tạo file .docx bằng thư viện `docx` (Node.js). Đã kiểm tra cấu trúc XML (đạt) và xuất PDF để xem từng trang.

## 7. Nguồn chính đã tham khảo

- PTN Kỹ thuật Hạt nhân – HCMUS: <https://ntlab.hcmus.edu.vn/>
- Bộ môn Vật lý Hạt nhân: <https://phys.hcmus.edu.vn/vat-ly-hat-nhan>
- Quy định hình thức luận văn thạc sĩ – Trường ĐH KHTN: <https://www.fit.hcmus.edu.vn/vn/UserFiles%5C7763_SDH_Qui-dinh-hinh-thuc-va-bao-ve-luan-van-thac-si.doc>
- Bài GPRTVN (thiết bị IDS Detector Duo): <https://doi.org/10.32508/stdjns.v2i5.784>
- Thông số RD7000+: <https://store.ttech.vn/thiet-bi-xac-dinh-duong-di-cua-cap-dien-duong-ong-cap-vien-thong---rd7000plus---radiodetection-p3675>
