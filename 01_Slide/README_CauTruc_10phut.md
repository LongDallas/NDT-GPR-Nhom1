# Cấu trúc slide seminar 10 phút (13 slide + 4 slide dự phòng)

> Thay cho dàn ý 15 slide ở [LuuTru/DanY_Slide_EN.md](LuuTru/DanY_Slide_EN.md) khi thời lượng là **10 phút**.
> Slide viết **tiếng Anh**. File này viết tiếng Việt để nhóm hiểu ý đồ từng slide.
> Hình nằm trong [HinhAnh/](HinhAnh/).
> **Bản dựng:** [LuuTru/Seminar_GPR_EN.pptx](LuuTru/Seminar_GPR_EN.pptx) (xem nhanh: [LuuTru/Seminar_GPR_EN_preview.jpg](LuuTru/Seminar_GPR_EN_preview.jpg)). Lời nói tiếng Anh nằm trong Notes của từng slide. Dựng lại: `node _build/tao_bai_trinh_bay.js LuuTru/Seminar_GPR_EN.pptx` rồi `python3 _build/them_hieu_ung.py LuuTru/Seminar_GPR_EN.pptx` (cần `pptxgenjs`; video 3D cần thêm `playwright-core` – cả hai đã cài trong `_build/node_modules`, máy khác chạy `npm install` trong `_build/`).

## 1. Ý tưởng chung

Bài nói kể một câu chuyện duy nhất:

> **Có một khoảng sân trong trường mà ai cũng đi qua. Bên dưới có ống nước và cáp, nhưng không có bản vẽ nào. Nhóm dùng GPR để "nhìn xuyên" mặt đường mà không đào, và vẽ được bản đồ.**

Mạch bài nói: **Câu hỏi → Cách nhìn xuống đất → Đi đo → Xử lý → Bản đồ → Bài học.**

Bài có ít slide vì ba lý do:

- **Bỏ slide mục lục và slide tổng quan tài liệu.** Tài liệu được trích dẫn bằng chữ nhỏ ở chân slide có dùng tới nó.
- **Gộp slide bìa vào slide mở đầu.** Tên đề tài và tên nhóm nằm trên ảnh hiện trường.
- **Mỗi slide một thông điệp.** Tiêu đề slide là một câu khẳng định, thân slide là hình chứng minh cho câu đó (kiểu Assertion–Evidence).

## 2. Bảng thời gian

| # | Slide (tiêu đề tiếng Anh) | Thời điểm | Thời lượng | Hình chính |
|---|---|---|---|---|
| 1 | *Kaohsiung 2014 → What is under our feet?* (kiêm slide bìa: tên đề tài, 5 thành viên, nhóm, GVHD) | 0:00 – 1:00 | **1:00** | ảnh vụ nổ Cao Hùng → `Slide1_SanTruong_16x9.jpg` |
| 2 | GPR for buried utilities: abroad and in Vietnam *(Ch.1 – tình hình nghiên cứu trong và ngoài nước)* | 1:00 – 1:45 | 0:45 | 3 bài nước ngoài + 3 bài nhóm Vật lý Địa cầu HCMUS |
| 3 | Two NDT methods: radar echoes and induced currents *(Ch.2 – siêu âm → sóng điện từ → GPR; dòng xoay chiều → cảm ứng → RD7000)* | 1:45 – 3:00 | 1:15 | `Slide2_NguyenLy_EN.png` + `Slide2_RD7000_EN.png` |
| 4 | We scanned a 10 m × 3.5 m grid with 9 lines *(quy trình đo)* | 3:00 – 4:15 | 1:15 | `Slide3_LuoiTuyen.jpg` + 4 ảnh quá trình đo `Step1–4_*.jpg` |
| 5 | Processing reveals the hidden hyperbola *(xử lý)* | 4:15 – 5:00 | 0:45 | `XuLy_TruocSau.png` |
| 6 | A simple model reproduces the measured hyperbolas *(Ch.3 – kết quả mô hình)* | 5:00 – 5:45 | 0:45 | `MoHinh_BScan_EN.png` (`04_XuLy_MoPhong/mo_hinh_bscan.py`) |
| 7 | *(hình toàn slide)* Locating the buried cable – lines C1–C4 | 5:45 – 6:15 | 0:30 | `Hinh1_Cap_MatCatGPR_EN.png` (kiểu SDT_Tai) |
| 8 | Four aligned anomalies trace one buried cable *(dị thường P1 trên cả 4 tuyến C1–C4 cùng một vị trí x = 2,5 m → cáp cắt ngang vuông góc với đường, khớp dấu đánh tại hiện trường)* | 6:15 – 6:50 | 0:35 | `Cap_4DiThuong_C1C4.png` + `Cap_MatBang_C1C4.png` (`_build/ve_cap_4_di_thuong.py`, đọc thẳng file `.T` trong `03_DuLieuHienTruong/New Data/`). Bản slide lẻ: `Slide_Cap_4DiThuong.pptx` (`_build/slide_cap_4_di_thuong.js`) |
| 9 | *(hình toàn slide)* Locating the water pipe – lines N1–N5 | 6:50 – 7:25 | 0:35 | `Hinh2_OngNuoc_MatCatGPR_EN.png` (kiểu SDT_Tai) |
| 10 | *(video toàn slide, tự chạy 19 s; đoạn máy đi đo 0:05–0:26 tua 3×)* Cảnh 3D: máy GPR quét từng tuyến → nối đỉnh hyperbol thành ống và cáp | 7:25 – 7:45 | 0:20 | `Canh3D_HienTruong_tua.mp4` (cắt từ `Canh3D_HienTruong.mp4`), quay từ `02_SoDoTuyen_BanDo/ket_qua/Canh3D_HienTruong.html` bằng `_build/quay_video_3d.js` |
| 11 | One cable crosses the road; one pipe runs along it *(kết quả thực tế)* | 7:45 – 8:30 | 0:45 | GIF xoay 360° `Canh3D_XoayVong.gif` (mặt đất mờ, thấy rõ ống và cáp) + 3 thẻ kết quả |
| 12 | What we learned, and what we would do next *(kết luận và kiến nghị)* | 8:30 – 9:20 | 0:50 | 3 kết luận + 2 kiến nghị |
| 13 | Now we know. Thank you — Questions? *(giới thiệu nhóm + tài liệu tham khảo)* | 9:20 – 9:50 | 0:30 | ảnh nhóm `Nhom_HienTruong.jpg` + `Slide5_KetQua.jpg` |
| A1–A4 | *Backup* (chỉ mở khi bị hỏi) | – | – | bản đồ mặt bằng, lát cắt độ sâu, `Hinh3_VungTinHieu_EN.png`, bảng so sánh NDT |

Giao diện: **Học thuật HCMUS** (nền trắng, xanh #0B4A9E, vàng #C9A227); riêng slide 1 giữ nền tối để kể chuyện. Tổng 9:50, dư 10 giây.

**Cách hiểu đường cáp và ống (cập nhật 18/10/2026, theo New Data và xác nhận tại hiện trường):** cáp = dị thường P1 trên cả 4 tuyến C1–C4, cắt ngang **vuông góc** với đường ở x ≈ 2,5 m (3 dấu nhóm đánh trên mặt đất thẳng hàng vuông góc với mép đường). Sâu 0,43–0,46 m trên C2–C4, 0,65 m trên C1. C1, C3 (đo xuôi) tự cho đúng x = 2,50 m; điểm xuất phát của C2, C4 (đo ngược) đặt theo cáp. Ống nước chạy dọc đường, cách mép đường phía ghế đá khoảng 1 m (dữ liệu: 0,67–1,09 m trên N2, N4, N5), sâu 0,43–0,59 m; đầu tuyến N phía ghế đá sát mép đường. Phương án cũ "cáp chéo qua C2–C4, P1 trên C1 là vật riêng" đã bị loại. Độ sâu mọi mục tiêu theo mô hình 2 lớp của nhóm (bê tông 0,12 m/ns, đất 0,10 m/ns); slide 3 ghi "0.12 | 0.10 m/ns". Slide 5–6 (xử lý, mô hình) vẫn dùng v = 0,095 m/ns vì đó là vận tốc migration trong ReflexW.

**Video 3D (slide 10):** sửa cảnh 3D xong thì quay lại: `node _build/quay_video_3d.js ../02_SoDoTuyen_BanDo/ket_qua/Canh3D_HienTruong.html HinhAnh/Canh3D_HienTruong.mp4` (cần `playwright-core`, `ffmpeg`), rồi tua đoạn máy đi đo 3× (từ 0:05 tới lúc quét xong tuyến cuối, hiện ~0:26.1):
`ffmpeg -i HinhAnh/Canh3D_HienTruong.mp4 -filter_complex "[0:v]trim=0:5,setpts=PTS-STARTPTS[a];[0:v]trim=5:26.1,setpts=(PTS-STARTPTS)/3[b];[0:v]trim=start=26.1,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0,fps=30[v]" -map "[v]" -c:v libx264 -pix_fmt yuv420p -crf 18 HinhAnh/Canh3D_HienTruong_tua.mp4`, rồi dựng lại bài.

**GIF xoay 360° (slide 11):** `node _build/quay_video_3d.js ../02_SoDoTuyen_BanDo/ket_qua/Canh3D_HienTruong.html HinhAnh/Canh3D_XoayVong.gif` (đuôi `.gif` → chế độ xoay vòng; chỉnh góc, độ mờ mặt đất trong hằng `GIF` của script), rồi nén: `gifsicle -O3 --lossy=40 HinhAnh/Canh3D_XoayVong.gif -o HinhAnh/Canh3D_XoayVong.gif`. Đây là phần công sức thật của nhóm nên được nhiều thời gian nhất.

## 3. Chi tiết từng slide

### Slide 1 – Mở đầu bằng câu chuyện (0:00 – 1:00) ★

**Ý đồ:** mở bằng một **thảm họa có thật**, dồn tới **một con số lớn**, đưa câu chuyện **về TP.HCM**, rồi kết lại ở **chính sân trường mình**. Thông điệp người nghe phải mang theo:

> **Thứ giết người không phải là đường ống, mà là việc không ai biết nó nằm ở đâu.**

Đề tài **chưa** hiện ra ngay. Tên đề tài chỉ xuất hiện ở bước cuối, khi người nghe đã muốn biết câu trả lời.

**Bố cục:** một slide, 4 lần bấm. Các hình chồng lên nhau, chuyển bằng hiệu ứng *Fade*. Như vậy vẫn tính là 1 slide.

| Lần bấm | Trên màn hình | Giây |
|---|---|---|
| 0 | **Nền đen.** Chỉ có dòng chữ trắng: `31 July 2014 · Kaohsiung, Taiwan` | 0–15 |
| 1 | Ảnh mặt đường Cao Hùng bị xé toạc sau vụ nổ (lấy từ Wikimedia Commons, ghi nguồn nhỏ ở góc). Chữ lớn màu đỏ: **32 dead · 321 injured** | 15–30 |
| 2 | Nền tối, hai con số lớn: **500,000+ utility strikes / year · ≈ $30 billion** (US, CGA 2019). Bên dưới là tít báo: *"Dig a street, hit a spider web"* (Người Lao Động) | 30–42 |
| 3 | **Ảnh sân trường** (`AnhHienTruong_SanTruong.jpg`) phủ kín slide, câu hỏi **"What is under our feet?"**. Dải dưới có tên đề tài, nhóm, giảng viên, logo HCMUS | 42–60 |

**Lời nói (tiếng Anh, khoảng 140 từ, nói chậm, có ngắt nghỉ):**

> *[Nền đen. Đứng yên, nhìn người nghe, im lặng 2 giây.]*
>
> July 31st, 2014. Kaohsiung, Taiwan.
> Late in the evening, people on the street begin to smell gas.
> Firefighters arrive. They search for the leak — for almost **three hours**.
> They cannot find it. *[ngừng 1 giây]*
>
> *[bấm 1]* Just before midnight, the street explodes.
> **Thirty-two people dead. Three hundred and twenty-one injured.**
> The cause? A leaking pipe — buried right under their feet — that nobody could see.
>
> *[bấm 2]* And this is not rare. In the US alone, buried utilities are hit
> more than **half a million times a year**. Here in Ho Chi Minh City, newspapers put it simply:
> *dig any street, and you hit a spider web.*
>
> *[bấm 3]* Now look at this. Our own campus. We walk across it every day.
> Under this asphalt there is a water pipe and a power cable — and **no drawing** of where they are.
> If someone digs here tomorrow… where is it safe?
>
> Today, we will answer that — **without digging a single hole.**

**Bản tiếng Việt để hiểu ý (không chiếu):**
Đêm 31/7/2014 ở Cao Hùng, người dân ngửi thấy mùi gas. Lính cứu hỏa tìm chỗ rò gần ba tiếng mà không thấy. Gần nửa đêm, cả con đường nổ tung: 32 người chết, 321 người bị thương. Nguyên nhân là một đường ống rò rỉ nằm ngay dưới chân họ mà không ai nhìn thấy. Chuyện này không hiếm: chỉ riêng ở Mỹ, mỗi năm có hơn nửa triệu vụ đào trúng công trình ngầm. Báo chí TP.HCM thì viết "đào đường là trúng mạng nhện". Còn đây là sân trường mình, ngày nào cũng đi qua. Bên dưới có ống nước và cáp điện, nhưng không có bản vẽ. Nếu mai có người đào ở đây thì đào chỗ nào cho an toàn? Hôm nay nhóm em trả lời câu hỏi đó mà không đào một nhát nào.

**Kỹ thuật nói:**
- **Im lặng 2 giây** trước câu đầu tiên. Khán phòng sẽ tự im theo.
- Câu ngắn, mỗi câu một ý. **Ngừng sau "They cannot find it."** Đó là lúc người nghe bắt đầu thấy rợn.
- Đọc con số thương vong **chậm và trầm giọng**, không đọc nhanh như đọc số liệu.
- Ở lần bấm 3 thì **đổi giọng**: từ kể chuyện sang trò chuyện ("Now look at this…"), và chỉ tay vào ảnh.
- Không nói "Hello, today our topic is…". Phần chào và giới thiệu tên nhóm để sau câu cuối, gói trong một câu.

**Gọi lại câu chuyện ở cuối bài** (để bài nói khép vòng):
- Cuối slide 5, khi chỉ vào bản đồ: *"In Kaohsiung, nobody could see the pipe. Here, we can."*
- Slide 7 dùng lại ảnh sân trường, nhưng lần này có vẽ ống và cáp lên ảnh. Câu hỏi "What is under our feet?" đã có câu trả lời.

**Nguồn (đặt chữ nhỏ ở chân slide 1):**
- Kaohsiung 2014: [Wikipedia – 2014 Kaohsiung gas explosions](https://en.wikipedia.org/wiki/2014_Kaohsiung_gas_explosions); [Al Jazeera, 01/08/2014](https://www.aljazeera.com/news/2014/8/1/taiwan-city-rocked-by-deadly-gas-explosions). Nguyên nhân: ống propylene rò rỉ, đi xuyên một cống thoát nước rồi bị ăn mòn ([Plasteurope](https://plasteurope.com/news/TAIWAN_t230049)).
- Số vụ đào trúng ở Mỹ: CGA DIRT Report 2019, khoảng 532.000 vụ, khoảng 30 tỷ USD; 28 % số vụ do khâu *định vị* sai ([Underground Infrastructure, 10/2020](https://undergroundinfrastructure.com/news/2020/10-october/cga-report-reveals-utility-damages-cost-us-30-billion-in-2019)).
- TP.HCM: báo Người Lao Động, [*"Đào đường là trúng 'mạng nhện'"*](https://nld.com.vn/xa-hoi/dao-duong-la-trung-mang-nhen-225572.htm).

> ⚠️ **Kiểm tra trước khi nói:** đọc lại mục *Explosions* trên trang Wikipedia để xác nhận mốc giờ (báo rò gas lúc khoảng 20:46, nổ lúc gần 0:00) và chi tiết "lính cứu hỏa không tìm ra nguồn rò". Nếu khác thì sửa câu "almost three hours".
> Con số 28 % do định vị sai rất hợp để dùng ở slide 6 (*"locating is where damage starts – that's what GPR fixes"*).

### Slide 2 – Nguyên lý: nhìn bằng tiếng vọng (1:00 – 2:30)

**Tiêu đề:** *GPR sees echoes; a buried pipe draws a hyperbola*

**Bố cục hai cột:**
- Trái: sơ đồ anten phát xung, xung phản xạ ở ống rồi quay về. Có hai công thức:
  `v = c / √εr` và `d = v·t / 2`.
- Phải: `Hinh2_2_hyperbol_van_toc.png`. Kéo anten qua một vật tròn thì vết phản xạ có dạng **hyperbol**. Độ cong của hyperbol cho biết vận tốc, từ đó suy ra độ sâu.

**Nói:** so sánh với siêu âm kiểu xung–phản xạ (pulse-echo) đã học trong môn NDT, chỉ khác là dùng sóng điện từ. Nói thêm một câu về RD7000: máy dò cáp dùng cảm ứng điện từ, đỉnh tín hiệu (peak) và điểm lặng (null) nằm ngay trên cáp. Hai phương pháp bổ sung cho nhau.
**Trích dẫn ở chân slide:** Daniels (2004) hoặc Jol (2009); Metje et al. (2007).

### Slide 3 – Quá trình đo ngoài hiện trường (2:30 – 4:30) ★

**Tiêu đề:** *We scanned a 10 m × 3.5 m grid with 9 lines*

**Bố cục:**
- Trái (khoảng 55 % slide): `SoDoTuyen_IMG_9558.jpg`, ảnh chụp từ trên cao có vẽ khung đỏ, tuyến vàng C1–C4 (cách nhau 1 m) và tuyến xanh N1–N5 (cách đều ~0,8 m). Chữ trên hình là tiếng Anh.
- Phải trên: **ảnh nhóm đang kéo máy GPR** (cần bổ sung, xem mục 5).
- Phải dưới: thanh 4 bước nối bằng mũi tên:

```
Plan grid  →  Acquire  →  Process  →  Map
(10×3.5 m)    (IDS Duo     (ReflexW)    (Python,
              250/700 MHz)              2D + 3D)
```

**Ý chính khi nói:**
- **Tại sao bố trí lưới như vậy:** đo vuông góc với vật cần tìm thì hyperbol rõ nhất.
  - 4 tuyến dọc C1–C4 (cách nhau 1 m) để bắt **cáp cắt ngang đường**.
  - 5 tuyến ngang N1–N5 để bắt **ống nước chạy dọc đường**.
- **Thiết bị:** IDS Detector Duo, anten kép **250 MHz** (đi sâu) và **700 MHz** (rõ nét). Mỗi vết cách nhau 2,78 cm. Tổng cộng 10 lượt đo, có 1 lượt đo lặp N5 để kiểm tra độ lặp lại.
- Một khó khăn gặp ở hiện trường, kể trong một câu (ví dụ: đo nhanh, khoảng cách N1–N5 chỉ áng chừng ~0,8 m, không có bánh xe đo hay GPS). Người nghe thường nhớ chi tiết thật kiểu này.

### Slide 4 – Xử lý dữ liệu (4:30 – 6:00)

**Tiêu đề:** *Processing turns noisy traces into clear hyperbolas*

**Hình:** `XuLy_TruocSau.png` (đã làm, chữ tiếng Anh). Hai radargram của **cùng một tuyến**: N5 đo lặp, kênh 250 MHz (file `LZZ20010.00`, file duy nhất còn ở dạng chưa xử lý).
- Trái: dữ liệu thô. Các sọc nền và lệch DC che mất phản xạ của ống.
- Phải: sau xử lý, hyperbol ống nước hiện rõ, có vẽ hyperbol với v = 0,095 m/ns và ghi độ sâu tới đỉnh ≈ 0,39 m.

Phía trên hai hình là chuỗi bước xử lý:
`Raw data → DC removal → Dewow → Background removal → Gain → Hyperbola → depth`

Script: `04_XuLy_MoPhong/ve_truoc_sau_xu_ly.py`.

**Nói:** mỗi bước nói một câu, tập trung vào việc bước đó *loại bỏ cái gì*. Vận tốc dùng để đổi thời gian ra độ sâu: **v = 0,095 m/ns**, cũng là vận tốc nhóm dùng cho migration trong ReflexW. Khớp hyperbol tự động trên từng tuyến cho kết quả dao động 0,085–0,17 m/ns, nên không nói con số này như một giá trị chính xác.

### Slide 5 – Kết quả: bản đồ (6:00 – 8:00) ★

**Tiêu đề:** *One cable crosses the road; one pipe runs along it*

**Bố cục:** `BanDo_OngNuoc_Cap.png` (chữ tiếng Anh). Bên trái là ảnh IMG_9558 chồng ống và cáp lên, bên phải là mặt bằng theo mét có ghi độ sâu. Nếu muốn hình to và dễ hiểu hơn với người nghe phổ thông, dùng `KetQua_IMG_9558.jpg` (ảnh từ trên cao, ống xanh, cáp cam, ghi độ sâu). Dưới hình là bảng 3 dòng:

| Target | Lines | Direction | Depth to top |
|---|---|---|---|
| Power cable | C1–C4 | straight across the road (90°) | 0.43–0.65 m |
| Water pipe | N2, N4, N5 | along the road, ~1 m from the benches | 0.43–0.59 m |
| Unknown objects (O1–O5) | single lines | – | 0.26–0.89 m |

**Nói:** chỉ tay lần lượt theo cáp (màu cam) rồi theo ống (màu xanh). Nhấn mạnh rằng nét đứt chỉ là **ngoại suy**. Nếu còn thời gian thì mở `02_SoDoTuyen_BanDo/ket_qua/Canh3D_HienTruong.html` (mở sẵn tab, kiểm tra Internet trước). Bấm **⏭ Skip** để vào thẳng trạng thái cuối, xoay cảnh, rồi **bấm vào ống nước** để hiện bảng thông số, tất cả **trong 20–30 giây**. Nếu thời gian cho phép, chạy animation quét (khoảng 25 giây ở tốc độ 1×, bấm *Speed* để chạy 2× hoặc 4×).

Câu chốt nối lại slide 1: *"So — if someone digs here tomorrow, now we know where not to dig."*

### Slide 6 – Thảo luận và kết luận (8:00 – 9:30)

**Tiêu đề:** *What we learned and what we would do next*

**Bố cục:** 3 ý chính bên trái, 2 hạn chế cùng hướng phát triển bên phải.

- **Takeaways**
  1. GPR định vị được cáp và ống dưới mặt nhựa đường mà không cần đào.
  2. Bố trí tuyến đo vuông góc với đối tượng là yếu tố quyết định để thấy được hyperbol.
  3. Kênh 700 MHz cho hình rõ nét, kênh 250 MHz đi sâu hơn. Dùng cả hai kênh thì chắc chắn hơn.
- **Limitations → Next steps**
  - Độ sâu phụ thuộc vận tốc: v = 0,095 m/ns (ReflexW) và 0,129 m/ns (khớp tự động) cho kết quả lệch nhau tới ~30 % → hiệu chỉnh bằng RD7000 hoặc đào kiểm chứng một điểm.
  - Migration trong ReflexW chỉ hội tụ tốt trên vài tuyến; khoảng cách các tuyến N (~0,8 m) chỉ áng chừng → đo lại với bánh xe đo khoảng cách hoặc GPS.

### Slide 7 – Cảm ơn và hỏi đáp (9:30 – 10:00)

Nền là `KetQua_IMG_9558.jpg` (ảnh sân trường từ trên cao, đã vẽ ống và cáp), làm mờ. Câu hỏi "What is under our feet?" ở slide 1 giờ có câu trả lời ngay trên ảnh. Chữ **"Thank you – Questions?"**. Ở chân slide có 3 tài liệu chính, lấy từ `05_TaiLieu/ThamKhao/references.bib`.

## 4. Slide dự phòng (đặt sau slide 7, chỉ mở khi được hỏi)

| # | Nội dung | Hình / nguồn | Câu hỏi có thể gặp |
|---|---|---|---|
| A1 | Lát cắt theo độ sâu (C-scan) | `LatCat_DoSau.png` | "Ống/cáp thấy ở độ sâu nào?" |
| A2 | Mô phỏng gprMax: cáp kim loại và ống PVC | chạy `04_XuLy_MoPhong/gprMax/cap_ngam_2D.in` | "Làm sao phân biệt kim loại với nhựa?" (dấu của phản xạ ngược nhau) |
| A3 | Bảng so sánh các phương pháp NDT dò công trình ngầm | dàn ý cũ, slide 5 | "Tại sao chọn GPR?" |

## 5. Việc cần làm trước khi dựng slide

| # | Việc | Vì sao | Ai |
|---|---|---|---|
| 1 | ✅ **Đã chốt v = 0,095 m/ns** (vận tốc migration trong ReflexW). Mọi hình, bảng slide 5 và `02_SoDoTuyen_BanDo/README.md` đều dùng giá trị này | Số trên slide 4–5 phải khớp nhau và khớp với hình | |
| 2 | ✅ **Đã có** `XuLy_TruocSau.png` (tuyến N5 đo lặp, 250 MHz). Không dùng N2 được vì không còn file thô của N2 | Slide 4 | |
| 3 | ✅ **Đã có ảnh nhóm đang đo** (`Ảnh thực hiện/`). Slide 3 dùng IMG_9511, 9503, 9525, 9528 (`HinhAnh/Step1–4_*.jpg`); ảnh nhóm IMG_9529 ở `HinhAnh/Nhom_HienTruong.jpg` (chưa dùng) | Slide 3 | |
| 4 | **RD7000:** `diem_rd7000.csv` đang trống. Nếu đã đo thì điền số vào. Nếu chưa đo thì trên slide chỉ nói RD7000 là *bước kiểm chứng đề xuất* | Không trình bày kết quả mà nhóm chưa có | |
| 5 | Tải **ảnh vụ nổ Cao Hùng** từ Wikimedia Commons (ghi tác giả và giấy phép). Kiểm tra mốc giờ trên Wikipedia (xem ⚠️ ở slide 1) | Cho lần bấm 1 của slide 1 | |
| 6 | Hỏi thầy câu E4: thời lượng thật và số người trình bày | Nếu 2–3 người nói thì chia: slide 1–2 / 3–4 / 5–7 | |
| 7 | Tập nói và bấm giờ ít nhất 2 lần. Nếu lố giờ thì cắt ở slide 2 và slide 4 trước, **không cắt slide 1 và slide 5** | | |

## 6. Hình đã có sẵn trong `HinhAnh/`

| Hình | Slide |
|---|---|
| `AnhHienTruong_SanTruong.jpg` (chuyển từ `IMG_9560.HEIC`) | 1, 7 |
| `AnhHienTruong_NhinTuTren.jpg` (chuyển từ `IMG_9558.HEIC`) | 3 (ảnh phụ, hoặc làm nền) |
| `SoDoTuyen_IMG_9558.jpg` (sơ đồ tuyến, tiếng Anh) | 3 |
| `XuLy_TruocSau.png` | 4 |
| `KetQua_IMG_9558.jpg` (ống + cáp trên ảnh, tiếng Anh) | 5, 7 |
| `Hinh2_2_hyperbol_van_toc.png` | 2 |
| `BanDo_OngNuoc_Cap.png` (tiếng Anh) | 5 |
| `LatCat_DoSau.png` (tiếng Anh) | A1 |
| `Hinh1_Cap_MatCatGPR.png`, `Hinh2_OngNuoc_MatCatGPR.png`, `Hinh3_VungTinHieu.png` (chữ tiếng Việt, theo mẫu SDT_Tai) | dự phòng, nếu được hỏi về mặt cắt từng tuyến |
| `Logo_HCMUS.png` | 1 |
