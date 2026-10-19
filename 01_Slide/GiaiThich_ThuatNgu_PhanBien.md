# Thuật ngữ và những chỗ dễ bị hỏi vặn – Seminar GPR

> Dùng chung với [Seminar_GPR_EN_v3.pptx](Seminar_GPR_EN_v3.pptx), [kịch bản tiếng Anh](KichBan_ThuyetTrinh_EN.md) và [kịch bản tiếng Việt](KichBan_ThuyetTrinh_VI.md).
>
> - **Phần A** giải thích các thuật ngữ trên slide bằng lời dễ hiểu.
> - **Phần B** gom các con số cả nhóm nên thuộc.
> - **Phần C** đoán trước các câu thầy cô có thể hỏi, đi theo từng slide. Mỗi câu có ý trả lời bằng tiếng Việt và câu nói sẵn bằng tiếng Anh.
> - **Phần D** là mấy chỗ trên slide nên sửa trước khi nộp.
>
> Mức độ: ★★★ gần như chắc chắn bị hỏi · ★★ dễ bị hỏi · ★ có thể bị hỏi.

---

## A. Thuật ngữ

### A1. Khái niệm chung

| Thuật ngữ | Tiếng Việt | Hiểu đơn giản là | Slide |
|---|---|---|---|
| NDT (Non-Destructive Testing) | Kiểm tra không phá hủy | Kiểm tra một vật mà không làm hư nó. GPR được tính là NDT vì mình chỉ đẩy máy trên mặt đường, không đào, không khoan. | 5 |
| GPR (Ground-Penetrating Radar) | Ra đa xuyên đất | Máy phát sóng điện từ xuống đất rồi thu sóng dội lại. Chỗ nào dưới đất khác với xung quanh (ống, cáp, lỗ rỗng) thì sóng dội về. | 3–14 |
| Utility | Công trình ngầm | Những thứ chôn dưới đất: ống nước, ống gas, cáp điện, cáp viễn thông, cống. | 1, 3 |
| Utility strike | Đào trúng công trình ngầm | Máy xúc hay cuốc làm bể ống, đứt cáp vì không biết nó nằm đó. | 1, 3, 15 |
| As-built drawing | Bản vẽ hoàn công | Bản vẽ ghi lại công trình thực tế nằm ở đâu sau khi thi công xong. Sân trường mình không có bản vẽ này. | 3 |
| Pulse–echo | Phát xung, nghe tiếng vọng | Bắn một xung thật ngắn rồi đo xem bao lâu tiếng vọng quay về. Siêu âm và GPR cùng cách làm này, chỉ khác loại sóng. | 6 |
| A-scan / B-scan / C-scan | Một vết / mặt cắt / lát cắt ngang | Ba chữ này mượn từ siêu âm. A-scan là tín hiệu ghi được tại một điểm. B-scan (radargram) là nhiều A-scan xếp cạnh nhau dọc một tuyến. C-scan là cắt ngang ở một độ sâu, nhìn từ trên xuống. | 9, 11, dự phòng |
| Radargram | Ảnh ra đa, mặt cắt ra đa | Ảnh B-scan: trục ngang là vị trí trên tuyến, trục đứng là thời gian (hoặc độ sâu). | 9–12 |
| Anomaly | Dị thường | Chỗ tín hiệu khác hẳn xung quanh. Khi chưa chắc là vật gì thì cứ gọi là dị thường (P1, A1, O1–O5). | 11, 12, 14 |

### A2. Vật lý của sóng

| Thuật ngữ | Tiếng Việt | Hiểu đơn giản là | Slide |
|---|---|---|---|
| Relative permittivity εr (dielectric constant) | Hằng số điện môi tương đối | Con số cho biết vật liệu làm sóng điện từ chậm đi bao nhiêu. Không khí là 1, bê tông khô khoảng 5–8, đất ẩm 9–25, nước 81. | 6 |
| Wave velocity v = c/√εr | Vận tốc sóng | c là vận tốc ánh sáng, 0,3 m/ns. Đất có εr = 9 thì sóng chạy 0,10 m/ns. Dùng đơn vị m/ns vì GPR đo thời gian tính bằng nano giây. | 6 |
| Two-way travel time | Thời gian hai chiều | Thời gian sóng đi xuống tới vật rồi quay lên. Vì đi hai lần nên độ sâu d = v·t/2. | 6, 9 |
| Reflection coefficient R | Hệ số phản xạ | Cho biết bao nhiêu phần sóng dội lại ở chỗ hai lớp vật liệu tiếp giáp: R = (√ε1 − √ε2)/(√ε1 + √ε2). Hai bên càng khác nhau thì dội càng mạnh. Công thức này đúng khi sóng đi thẳng góc vào mặt tiếp giáp và bỏ qua hao hụt. | 6, 10 |
| Polarity | Dấu (cực tính) của sóng dội | R âm nghĩa là sóng dội về bị lật ngược. Kim loại: R = −1. Ống rỗng chứa không khí: R dương. **Ống đang chứa nước: R âm, cùng dấu với kim loại, chỉ yếu hơn.** | 6, 10 |
| Hyperbola | Hyperbol | Kéo máy ngang qua một vật nhỏ thì vết dội về có hình vòm, gọi là hyperbol: t(x) = (2/v)·√(d² + (x − x0)²). Nó ra hình này vì khoảng cách từ anten tới vật tính theo định lý Pythagore. | 6, 10–12 |
| Apex | Đỉnh hyperbol | Điểm cao nhất của vòm, ứng với lúc anten nằm ngay trên vật. Vị trí đỉnh cho biết vật ở đâu, thời gian đỉnh t0 = 2d/v cho biết vật sâu bao nhiêu. | 6, 11 |
| Wavelength λ = v/f | Bước sóng | Anten 250 MHz trong đất (v = 0,10 m/ns) có bước sóng 40 cm; anten 700 MHz khoảng 14 cm. | 6 |
| Vertical resolution ≈ λ/4 | Độ phân giải theo chiều sâu | Hai vật nằm chồng lên nhau gần hơn một phần tư bước sóng thì máy không tách ra được: khoảng 10 cm với 250 MHz, khoảng 3,6 cm với 700 MHz. | 6, dự phòng |
| Horizontal resolution, Fresnel zone | Độ phân giải ngang, đới Fresnel | Ở độ sâu d, anten "nhìn" một vùng rộng cỡ r ≈ √(λd/2). Ở 0,45 m: khoảng 30 cm (250 MHz), 18 cm (700 MHz). Vì vậy vật trên ảnh lúc nào cũng trông to hơn thật. | dự phòng |
| Attenuation | Sóng yếu dần | Sóng càng đi càng yếu. Đất càng dẫn điện (sét ướt, nước mặn) và tần số càng cao thì yếu càng nhanh. Vì vậy 250 MHz nhìn sâu hơn 700 MHz. | 5, 6 |
| Ringing | Đuôi rung | Sóng dội qua dội lại nhiều lần, tạo thành một cái đuôi dài bên dưới đỉnh hyperbol. Hay gặp ở vật kim loại. | 11 |

### A3. Đo ngoài hiện trường

| Thuật ngữ | Tiếng Việt | Hiểu đơn giản là | Slide |
|---|---|---|---|
| Survey line / profile | Tuyến đo | Đường thẳng mình đẩy máy đi qua. C1–C4 chạy dọc đường để tìm cáp, N1–N5 chạy ngang đường để tìm ống. | 8 |
| Survey grid | Lưới đo | Các tuyến song song và vuông góc nhau, ở đây nằm trong khung 10 m × 3,5 m. | 8 |
| Trace, trace interval | Vết, khoảng cách giữa hai vết | Mỗi lần máy ghi tín hiệu tại một chỗ là một vết. Hai vết liền nhau cách 2,78 cm. | 8 |
| Sample, time window | Mẫu, khoảng thời gian ghi | Mỗi vết có 483 mẫu, mỗi mẫu cách nhau 0,25 ns, tức máy ghi trong khoảng 121 ns. | – |
| Shielded antenna | Anten có vỏ chắn | Vỏ chắn giúp bớt nhiễu từ những thứ trên mặt đất như xe, tường, người đứng gần. | 8 |
| Dual-frequency antenna | Anten kép hai tần số | Máy IDS Detector Duo ghi cùng lúc 250 MHz và 700 MHz trên cùng một tuyến. File bắt đầu bằng `LZZ1` là 700 MHz, `LZZ2` là 250 MHz. | 8 |
| Zigzag survey | Đo đi về (zigzag) | Đo xong một tuyến thì quay đầu đo tuyến kế theo chiều ngược lại (C2, C4, N2, N4). Lúc xử lý phải lật các tuyến này lại cho cùng chiều. | 11 |
| Repeat line | Đo lặp | Đo lại tuyến N5 lần nữa để xem kết quả có giống lần đầu không. | 8 |

### A4. Xử lý dữ liệu

| Thuật ngữ | Tiếng Việt | Hiểu đơn giản là | Slide |
|---|---|---|---|
| Time-zero correction | Chỉnh mốc thời gian 0 | Dời mốc 0 về đúng lúc sóng chạm mặt đất. Nếu không chỉnh thì độ sâu của mọi vật đều bị lệch như nhau. | 9 |
| DC shift removal | Bỏ độ lệch DC | Trừ đi giá trị trung bình của mỗi vết để tín hiệu dao động quanh số 0. | 9 |
| Dewow | Lọc dewow | Bỏ phần tín hiệu trôi rất chậm do anten đặt sát mặt đất. Khung lọc dài khoảng một chu kỳ sóng: 4 ns với 250 MHz, 1,43 ns với 700 MHz. | 9 |
| Bandpass filter | Lọc thông dải | Chỉ giữ lại tần số quanh tần số của anten, bỏ nhiễu ở ngoài. | – |
| Background removal | Xóa nền | Lấy trung bình cả tuyến rồi trừ đi, để mất mấy vệt ngang lặp lại. **Cái giá phải trả:** nó cũng xóa luôn các lớp nằm ngang thật và những ống chạy song song với tuyến. | 9 |
| Gain | Khuếch đại | Tăng độ lớn tín hiệu theo thời gian để thấy rõ phản xạ yếu ở sâu. Riêng AGC làm méo tỉ lệ độ lớn thật, nên chỉ dùng để nhìn. | 9 |
| Hyperbola fitting / velocity analysis | Khớp hyperbol / tìm vận tốc | Chỉnh v cho tới khi hyperbol tính ra trùng với hyperbol đo được; khi trùng thì biết vận tốc sóng. | 9, 10 |
| Migration (Kirchhoff) | Dịch chuyển, gom hyperbol | Gom cái vòm hyperbol về một điểm ở đỉnh, cho vật về đúng chỗ. Chọn đúng vận tốc thì gom thành một chấm gọn; chọn sai thì còn sót một vệt cong. | 9, dự phòng |
| Two-layer velocity model | Mô hình hai lớp | Nhóm tính độ sâu theo hai lớp: lớp bê tông trên cùng (khoảng 5 ns đầu, dày cỡ 0,30 m) với 0,12 m/ns, và lớp đất bên dưới với 0,10 m/ns. | 8, 9, 14 |
| Ray model | Mô hình tia | Tính đường đi và thời gian của sóng bằng hình học, giống vẽ tia sáng. Nhanh nhưng không mô phỏng đủ hình dạng sóng. | 10 |
| FDTD, gprMax | Mô phỏng sóng đầy đủ | gprMax giải phương trình Maxwell từng bước thời gian, ra ảnh ra đa mô phỏng rất sát thực tế. Nhóm đã có file đầu vào, chưa chạy. | 10 |
| Interpolation / extrapolation | Nội suy / ngoại suy | Nội suy là đoán phần nằm giữa hai tuyến đã đo. Ngoại suy là kéo dài ra ngoài chỗ đã đo (nét đứt trên bản đồ), chỉ là dự đoán. | 13, 14 |

### A5. Máy dò cáp RD7000

| Thuật ngữ | Tiếng Việt | Hiểu đơn giản là | Slide |
|---|---|---|---|
| Electromagnetic induction | Cảm ứng điện từ | Dòng điện xoay chiều trong cáp sinh ra từ trường B = μ0I/(2πr). Cuộn dây trong máy thu "bắt" được từ trường này. | 7 |
| Peak / null | Đỉnh / điểm câm | Đứng ngay trên cáp thì cuộn nằm ngang bắt tín hiệu mạnh nhất (peak), cuộn đứng thì bằng 0 (null). Nếu hai chỗ này trùng nhau thì từ trường không bị nhiễu. | 7 |
| Passive mode | Dò thụ động | Không cần máy phát: dò dòng điện 50/60 Hz có sẵn trong cáp đang chạy điện, hoặc sóng radio tự nhiễm vào các vật dẫn dài. | 7 |
| Active mode | Dò chủ động | Dùng máy phát kèm theo: nối thẳng vào cáp, kẹp quanh cáp, hoặc đặt trên mặt đất cho cáp tự nhiễm tín hiệu. | 7 |
| Sonde | Đầu phát luồn ống | Một đầu phát nhỏ luồn vào trong ống nhựa để máy thu dò theo. Đây là cách duy nhất để RD7000 "thấy" được ống nhựa. | 5, 7 |

### A6. Tiêu chuẩn và nguồn số liệu

| Tên | Là gì |
|---|---|
| ASTM D6432-19 | Hướng dẫn của Mỹ về cách khảo sát bằng GPR trên mặt đất. |
| PAS 128:2022 | Quy định của Anh về dò tìm công trình ngầm. Chia làm 4 loại khảo sát: D (tra hồ sơ), C (đi xem hiện trường), B (dò bằng máy địa vật lý), A (đào lộ ra để kiểm chứng). Nhóm mình làm tới loại B. |
| CGA DIRT Report | Báo cáo thống kê hằng năm của Hiệp hội Common Ground Alliance (Mỹ) về các vụ đào trúng công trình ngầm. |
| ReflexW | Phần mềm xử lý dữ liệu GPR (của Sandmeier) mà nhóm dùng để lọc, khuếch đại và migration. |

---

## B. Con số cả nhóm nên thuộc

| Nội dung | Con số | Ghi chú |
|---|---|---|
| Khung khảo sát | 10 m × 3,5 m | 9 tuyến + 1 lần đo lặp = 10 file |
| Tuyến C1–C4 | dọc đường, cách nhau 1 m | để tìm cáp |
| Tuyến N1–N5 | ngang đường, cách nhau khoảng 0,8 m (ước chừng) | để tìm ống nước |
| Máy đo | IDS Detector Duo, 250 + 700 MHz | 2,78 cm một vết; 483 mẫu × 0,25 ns |
| Vận tốc dùng khi migration | 0,095 m/ns (εr ≈ 10) | trong ReflexW và mô hình ở slide 10 |
| Vận tốc dùng tính độ sâu | 0,12 m/ns trong bê tông (εr ≈ 6,3), 0,10 m/ns trong đất (εr = 9) | lớp bê tông khoảng 5 ns đầu, dày cỡ 0,30 m |
| Vận tốc khớp hyperbol tự động | 0,085–0,17 m/ns, thường quanh 0,12–0,14 | dao động nhiều, không lấy làm số chính |
| Cáp (P1) | ở 2,5 m, vuông góc với đường; sâu 0,43–0,46 m (C2–C4), 0,65 m (C1) | thấy trên cả 4 tuyến |
| Ống nước (A1) | chạy dọc đường, cách mép phía ghế đá khoảng 1 m (0,67–1,09 m); sâu 0,43–0,59 m | thấy trên N2, N4, N5 |
| Dị thường O1–O5 | mỗi cái chỉ thấy trên 1 tuyến; sâu 0,26–0,90 m | không kết luận |
| Độ phân giải theo chiều sâu | khoảng 10 cm (250 MHz), 3,6 cm (700 MHz) | λ/4 với v = 0,10 m/ns |
| Độ sâu lệch vì vận tốc (ví dụ) | t = 7,9 ns: 0,45 m (hai lớp), 0,38 m (0,095), 0,51 m (0,129) | đây là chỗ ra con số "lệch khoảng 20 %" |
| Kích thước P1 trên ảnh sau migration | khoảng 31 × 14 cm | do giới hạn độ phân giải, không phải đường kính cáp |
| Cao Hùng, 31/7/2014 | 32 người chết, 321 người bị thương | ống propylene bị ăn mòn, nằm trong cống thoát nước |
| Mỹ (CGA 2019) | khoảng 532.000 vụ/năm, khoảng 30 tỷ USD; khoảng 28 % do định vị sai | xem D4 |

---

## C. Những câu có thể bị hỏi, theo từng slide

**Cách trả lời chung:** nói câu trả lời ngắn trước, giải thích sau. Chỗ nào nhóm chưa làm thì nói thẳng là chưa làm, kèm hướng làm tiếp. Tuyệt đối không bịa số liệu.

Mỗi câu có ba phần: **câu hỏi** (thầy cô có thể hỏi bằng tiếng Việt hoặc tiếng Anh), **ý trả lời** bằng tiếng Việt để hiểu, và **nói bằng tiếng Anh** là câu nói sẵn.

### Slide 1 – Chuyện ở Cao Hùng

**C1 ★★ – Có GPR thì vụ nổ ở Cao Hùng có tránh được không?**
*(Could GPR have prevented the Kaohsiung explosion?)*

**Ý trả lời:** Không hẳn. GPR chỉ cho biết ống nằm ở đâu, chứ không phát hiện được gas rò; muốn tìm chỗ rò thì phải dùng cảm biến khí hoặc thiết bị nghe âm thanh. Bài học nhóm muốn nói là không ai nắm được bên dưới con đường có gì. Biết vị trí là bước đầu tiên, và đó chính là việc của GPR.

**Nói bằng tiếng Anh:** *Not directly. GPR maps where pipes are; it does not detect a gas leak — that needs gas sensors or acoustic methods. The lesson we took is that nobody had a reliable map of what was under the street. Locating is the first step, and that is the step GPR does.*

**Lưu ý:** đừng nói kiểu "có GPR là cứu được 32 người". Câu chuyện chỉ để nói chuyện **không biết vị trí**, không liên quan tới việc dò rò rỉ.

**C2 ★ – Sao lại lấy số liệu của Mỹ, ở Việt Nam thì sao?**

**Ý trả lời:** Số liệu của Mỹ được thống kê kỹ nhất. Ở Việt Nam nhóm chưa tìm được thống kê cấp quốc gia, nhưng báo chí TP.HCM nói rất nhiều về chuyện này.

**Nói bằng tiếng Anh:** *We use the US numbers because they are the best-documented statistics. In Vietnam we found no national statistics, but newspapers in Ho Chi Minh City report the same problem.*

### Slide 3 – Đặt vấn đề

**C3 ★★ – Không có bản vẽ thì sao nhóm biết dưới đó có ống và cáp?**

**Ý trả lời:** Nhóm biết là có vì [điền căn cứ thật: dấu hiệu trên mặt đất, nắp hố, người quản lý cho biết…], nhưng không ai biết chính xác nó nằm ở đâu và sâu bao nhiêu. Khảo sát này để trả lời hai chuyện đó.

**Nói bằng tiếng Anh:** *We knew there were utilities from [surface signs / the site staff], but nobody had their exact position or depth. The survey answers where and how deep.*

**Lưu ý:** cả nhóm phải thống nhất trước căn cứ này. Nếu không chắc thì nói *"we expected utilities because…"*, đừng khẳng định chắc nịch.

### Slide 4–5 – Tổng quan và so sánh các phương pháp NDT

**C4 ★★ – Nhóm có gì mới so với nhóm Vật lý Địa cầu?**

**Ý trả lời:** Về phương pháp thì không có gì mới, vì nhóm dùng cùng loại máy và cách xử lý quen thuộc. Cái nhóm làm được là tự đi hết các bước ở một chỗ chưa có bản vẽ, rồi đối chiếu kết quả với các dấu đã đánh ngoài hiện trường.

**Nói bằng tiếng Anh:** *Methodologically, nothing new — we use the same equipment and standard processing. Our contribution is applying the full chain ourselves on an undocumented site, and checking the result against what we marked on the ground.*

**Lưu ý:** cứ nhận thẳng là không mới về phương pháp. Với một bài seminar môn học, trả lời vậy là an toàn nhất.

**C5 ★★ – GPR thì liên quan gì tới môn Các phương pháp NDT?**

**Ý trả lời:** GPR giống hệt siêu âm xung – phản xạ, chỉ thay sóng âm bằng sóng điện từ: phát xung, sóng dội ở mặt tiếp giáp, đổi thời gian ra độ sâu. Ngay cả mấy chữ A-scan, B-scan, C-scan cũng là mượn từ siêu âm.

**Nói bằng tiếng Anh:** *GPR is the electromagnetic version of ultrasonic pulse–echo testing: a pulse, an echo at an interface, and time converted to depth. Even the terms A-scan, B-scan and C-scan come from ultrasonic testing.*

**C6 ★ – Sao không dùng từ kế hay đo điện trở suất?**

**Ý trả lời:** Mấy cách đó không thấy được ống nhựa, hoặc quá thô để thấy một vật cỡ 10 cm nằm sâu nửa mét. Chỉ vào bảng ở slide 5.

**Nói bằng tiếng Anh:** *They do not see plastic pipes, or their resolution is too coarse for a 10-centimetre object at half a metre.*

### Slide 6 – Nguyên lý GPR

**C7 ★★★ – Tại sao vật tròn lại cho ra hình hyperbol?**

**Ý trả lời:** Vì máy đo khoảng cách thẳng từ anten tới vật. Anten ở vị trí x thì khoảng cách đó bằng √(d² + (x − x0)²), đúng định lý Pythagore. Đổi khoảng cách ra thời gian hai chiều thì được t(x) = (2/v)·√(d² + (x − x0)²), và đó là phương trình một hyperbol. Nếu có bảng thì vẽ nhanh một tam giác vuông là thầy cô thấy ngay.

**Nói bằng tiếng Anh:** *Because the antenna measures the straight-line distance to the object. At position x, that distance is the square root of d squared plus (x − x0) squared — Pythagoras. Converting distance to two-way time gives t(x) = (2/v)·√(d² + (x − x0)²), which is a hyperbola.*

**C8 ★★★ – Sao trong d = vt/2 lại chia hai?**

**Ý trả lời:** Vì máy đo thời gian sóng đi xuống tới vật rồi quay lên, tức là đi hai lần quãng đường. Độ sâu chỉ là một nửa.

**Nói bằng tiếng Anh:** *The radar measures the time down to the target and back up. The depth is only half of that path.*

**C9 ★★ – R âm là sao? Dựa vào đó phân biệt kim loại với nhựa được không?**

**Ý trả lời:** R âm nghĩa là sóng dội về bị lật ngược. Kim loại cho R = −1. Ống nhựa rỗng chứa không khí có hằng số điện môi thấp hơn đất nên R dương, vì vậy hai loại dội ngược dấu nhau.

**Nói bằng tiếng Anh:** *A negative R means the reflected wave is inverted. Metal gives R = −1. An empty plastic pipe filled with air has a lower permittivity than soil, so R is positive. That is why their echoes have opposite polarity.*

**Lưu ý, đây là cái bẫy:** ống nước đang dùng thì bên trong là **nước** (εr khoảng 81, cao hơn đất). Với đất εr = 10 thì R ≈ −0,48, tức **cùng dấu với kim loại**. Như vậy dựa vào dấu chỉ phân biệt được kim loại với ống **rỗng**. Nếu bị hỏi tiếp thì nói: *"For a water-filled pipe the polarity is the same as metal, so polarity alone cannot separate them; we also use the ringing and the direction of the line."* Đừng bao giờ nói "ống nhựa luôn ngược dấu với kim loại".

**C10 ★★ – Công thức R này dùng được khi nào?**

**Ý trả lời:** Khi sóng đi thẳng góc vào một mặt phẳng, không tính hao hụt, và vật liệu không có từ tính. Với ống tròn nhỏ thì nó chỉ cho biết gần đúng dấu và độ mạnh yếu.

**Nói bằng tiếng Anh:** *For a wave arriving at normal incidence on a flat, lossless interface, with non-magnetic materials. For a small round pipe it is an approximation of the sign and relative strength.*

**C11 ★★ – Độ phân giải 10 cm tính ra sao?**

**Ý trả lời:** Bước sóng λ = v/f = 0,10 m/ns chia 0,25 GHz = 0,40 m; lấy một phần tư là 10 cm. Ở 700 MHz bước sóng khoảng 14 cm, một phần tư là khoảng 3,6 cm.

**Nói bằng tiếng Anh:** *λ = v/f = 0.10 m/ns divided by 0.25 GHz = 0.40 m, so λ/4 ≈ 10 cm. At 700 MHz, λ ≈ 14 cm, so about 3.6 cm.*

**C12 ★★ – Sao tần số thấp lại nhìn được sâu hơn?**

**Ý trả lời:** Tần số càng cao thì sóng trong đất mất năng lượng càng nhanh. Sóng 250 MHz yếu đi chậm hơn sóng 700 MHz nên xuống được sâu hơn, nhưng bước sóng dài hơn nên hình kém nét hơn.

**Nói bằng tiếng Anh:** *Attenuation in soil increases with frequency, so a 250 MHz pulse loses energy more slowly than a 700 MHz pulse. The price is a longer wavelength, so less detail.*

**C13 ★ – 0,3 m/ns là gì?** Là vận tốc ánh sáng: 3×10⁸ m/s đổi ra bằng 0,3 m/ns.

### Slide 7 – RD7000

**C14 ★★★ – Nhóm đo RD7000 chưa? Chưa đo thì đưa vào làm gì?**

**Ý trả lời:** Dạ chưa đo. Đề bài của môn yêu cầu trình bày cả hai phương pháp; máy dò điện từ là thứ thường được dùng chung với GPR, và nhóm dự định dùng nó để kiểm tra lại độ sâu của cáp. Trên slide nhóm chỉ trình bày nguyên lý, không đưa ra kết quả nào của RD7000.

**Nói bằng tiếng Anh:** *No, we have not measured with it yet. The course asks for both methods — the electromagnetic one is the standard partner of GPR, and it is our proposed check of the cable depth. We show only the principle and do not present any RD7000 result.*

**Lưu ý:** trả lời "chưa đo" ngay câu đầu tiên, không vòng vo.

**C15 ★★ – Sao peak với null lại cùng nằm ngay trên cáp?**

**Ý trả lời:** Ngay phía trên cáp, từ trường nằm ngang. Cuộn dây nằm ngang thì đón trọn từ trường nên tín hiệu mạnh nhất; cuộn dây đứng thì không có từ trường nào xuyên qua nên tín hiệu bằng 0.

**Nói bằng tiếng Anh:** *Right above the cable the magnetic field is horizontal. A horizontal coil aligned with it sees the maximum flux — the peak. A vertical coil sees no flux at that point — the null.*

**C16 ★ – RD7000 đo độ sâu bằng cách nào?**

**Ý trả lời:** Máy có hai cuộn dây đặt chồng lên nhau, cách một khoảng cố định. Từ trường yếu dần theo 1/r, nên so tín hiệu của hai cuộn là tính ra được khoảng cách tới cáp.

**Nói bằng tiếng Anh:** *It compares the signals in two coils stacked a fixed distance apart; because the field falls off as 1/r, the ratio gives the distance to the cable.*

### Slide 8 – Đo ngoài hiện trường

**C17 ★★★ – Sao tuyến đo phải vuông góc với vật?**

**Ý trả lời:** Cắt vuông góc qua ống thì hyperbol mới gọn và cân hai bên. Còn nếu đi dọc theo ống thì ống chỉ hiện ra như một lớp nằm ngang, mà bước xóa nền còn xóa mất luôn.

**Nói bằng tiếng Anh:** *Crossing a pipe at a right angle gives a sharp, symmetric hyperbola. If a line runs along the pipe, the pipe looks like a flat layer — and background removal would even erase it.*

**C18 ★★★ – Vị trí các tuyến có chính xác không? Khoảng cách 0,8 m đo bằng gì?**

**Ý trả lời:** Trên từng tuyến thì khoảng cách do máy tự đếm, cứ 2,78 cm một vết. Cái chưa chính xác là điểm bắt đầu của mỗi tuyến và khoảng cách 0,8 m giữa các tuyến N, vì nhóm ước chừng bằng bước chân. Đó là lý do vị trí ống xê dịch khoảng 0,4 m, và lần sau nhóm sẽ dùng GPS hoặc máy toàn đạc.

**Nói bằng tiếng Anh:** *Along each line, distance comes from the radar's trace counter, one trace every 2.78 cm. What is approximate is where each line starts and the 0.8 m spacing of the N lines, which we paced. That is why the pipe position has a spread of about 0.4 m, and why we recommend a GPS or total station next time.*

**Lưu ý:** nhóm kiểm tra lại xe GPR có bánh xe đo quãng đường hay không, để nói cho đúng.

**C19 ★★ – Sao đo hai tần số? Kết quả trên slide là của tần số nào?**

**Ý trả lời:** Hai tần số được ghi cùng lúc. Kết quả về cáp và ống trên slide là của 250 MHz, vì nó nhìn được sâu hơn. Còn 700 MHz cho hình nét hơn ở gần mặt đất, nhóm dùng để làm các lát cắt theo độ sâu.

**Nói bằng tiếng Anh:** *The two channels record at the same time. The results on the cable and pipe slides are from 250 MHz, which sees deeper; the 700 MHz channel gives sharper images near the surface and is used for the depth slices.*

**C20 ★ – Đo lại N5 để làm gì? Hai lần có khớp nhau không?**

**Ý trả lời:** Để xem kết quả có lặp lại được không. Hai lần đo đều thấy ống ở gần như cùng một chỗ: cách mép đường 0,72 m và 0,67 m.

**Nói bằng tiếng Anh:** *To check repeatability. The pipe appears at nearly the same place on both runs — 0.72 and 0.67 m from the road edge.*

### Slide 9 – Xử lý dữ liệu

**C21 ★★★ – Xóa nền có làm mất luôn tín hiệu thật không?**

**Ý trả lời:** Có. Cái gì giống nhau suốt dọc tuyến thì đều bị xóa, kể cả các lớp nằm ngang thật và ống chạy song song với tuyến. Với đề tài này thì chấp nhận được, vì ống và cáp đều cắt ngang tuyến đo. Nếu muốn vẽ các lớp mặt đường thì không dùng bước này.

**Nói bằng tiếng Anh:** *Yes — it removes anything that is the same along the whole line, including flat layers and a pipe running parallel to the line. That is acceptable here because our targets cross the lines; we would not use it to map pavement layers.*

**C22 ★★ – Dewow là gì? Chọn khung lọc bao nhiêu?**

**Ý trả lời:** Dewow bỏ phần tín hiệu trôi rất chậm, sinh ra do anten đặt sát mặt đất. Khung lọc dài khoảng một chu kỳ sóng: chừng 4 ns với 250 MHz và 1,4 ns với 700 MHz.

**Nói bằng tiếng Anh:** *Dewow removes the very low-frequency drift caused by the antenna near the ground. The window is about one period of the centre frequency: about 4 ns at 250 MHz and 1.4 ns at 700 MHz.*

**C23 ★★ – Khuếch đại có làm sai độ lớn tín hiệu không?**

**Ý trả lời:** Có, nên nhóm chỉ dùng nó để nhìn và chọn điểm, không dùng để so phản xạ nào mạnh hơn.

**Nói bằng tiếng Anh:** *Yes, gain changes the true amplitude, so we use it for display and picking, not for comparing reflection strength.*

**C24 ★★★ – Migration dùng 0,095 m/ns mà tính độ sâu lại dùng 0,12 và 0,10. Vậy là không thống nhất?**

**Ý trả lời:** Đúng là có chỗ chưa thống nhất, và nhóm biết điều đó. 0,095 là vận tốc gom hyperbol gọn nhất khi chạy migration trong ReflexW. Còn khi tính độ sâu, nhóm chia hai lớp (bê tông thì sóng nhanh hơn, đất thì chậm hơn) cho sát với cấu tạo mặt đường hơn. Hai cách cho độ sâu lệch nhau cỡ 15–20 %, và đây là chỗ chưa chắc nhất của nhóm. Muốn chốt thì phải đào thử một hố hoặc đo bằng RD7000.

**Nói bằng tiếng Anh:** *It is a known inconsistency. 0.095 is the single velocity that focused the hyperbolas best in ReflexW. For depths we use a two-layer model — faster in the concrete, slower in the soil — which matches the layered pavement better. The two give depths about 15–20 % apart, and that is our main uncertainty. A test pit or the RD7000 would settle it.*

**Nếu bị hỏi con số cụ thể:** với t = 7,9 ns thì mô hình hai lớp cho 0,45 m, còn 0,095 m/ns cho 0,38 m.

**C25 ★★ – Vận tốc 0,12 và 0,10 lấy ở đâu ra?**

**Ý trả lời:** Từ hình dạng các hyperbol khi nhóm chú thích dữ liệu, và hai số này cũng khớp với giá trị thường gặp: hằng số điện môi của bê tông khoảng 6, của đất ẩm khoảng 9. Nhóm chưa đo riêng vận tốc bằng cách khác, ví dụ đo CMP.

**Nói bằng tiếng Anh:** *From the hyperbola shapes in our own annotation, and they match typical values: about 6 for concrete and 9 for moist soil in relative permittivity. We did not measure them independently, for example with a CMP survey.*

**C26 ★ – Migration để làm gì? Chọn sai vận tốc thì sao?**

**Ý trả lời:** Migration gom mỗi hyperbol về điểm đỉnh của nó. Đúng vận tốc thì gom lại thành một chấm gọn. Vận tốc thấp quá thì còn sót một vệt cong xuống, cao quá thì thành vệt cong lên.

**Nói bằng tiếng Anh:** *Migration collapses each hyperbola back to its apex. With the right velocity it focuses to a point; too low a velocity leaves a downward curve, too high gives an upward "smile".*

### Slide 10 – Mô hình

**C27 ★★ – Đây là mô hình thật hay chỉ vẽ đường cong cho khớp?**

**Ý trả lời:** Là mô hình tia: nhóm tính thời gian sóng đi rồi đặt vào đó một xung 250 MHz với đúng dấu phản xạ. Đây chưa phải mô phỏng sóng đầy đủ; file cho gprMax đã chuẩn bị nhưng nhóm chưa chạy.

**Nói bằng tiếng Anh:** *It is a ray model: we compute travel times and add a 250 MHz Ricker wavelet with the right reflection sign. It is not a full-wave simulation; a gprMax input file is prepared but we have not run it.*

**C28 ★★ – Mô hình lấy vận tốc 0,095 từ chính dữ liệu, vậy khớp với dữ liệu thì có gì lạ?**

**Ý trả lời:** Dạ đúng một phần. Vận tốc lấy từ dữ liệu nên chuyện hình dạng đường cong khớp nhau chỉ là kiểm tra cho hợp lý, chưa phải bằng chứng độc lập. Cái mô hình cho thêm là dấu của sóng dội và thời gian đỉnh ứng với một vật sâu 0,45 m.

**Nói bằng tiếng Anh:** *Partly, yes — the velocity was chosen from the data, so the match of the curve shape is a consistency check, not independent proof. What the model adds is the expected polarity and the apex time for a target at 0.45 m.*

**Lưu ý:** nhận ý này thì được đánh giá cao hơn là cố cãi.

### Slide 11 – Sợi cáp (dễ bị hỏi nhất)

**C29 ★★★ – Điểm bắt đầu của tuyến C2, C4 là nhóm tự đặt cho P1 trùng với cáp. Vậy bốn điểm thẳng hàng có phải do nhóm tự sắp không?**
*(Isn't the alignment circular?)*

**Ý trả lời:** Với C2 và C4 thì đúng là có một phần như vậy, và nhóm nói rõ: điểm bắt đầu của hai tuyến này không đo được, nên nhóm đặt theo các dấu cáp đã đánh ngoài hiện trường. Nhưng có ba bằng chứng không phụ thuộc vào việc đó:
1. C1 và C3 đo theo chiều xuôi, tự hai tuyến đã cho P1 ở đúng 2,50 m.
2. Lúc đo, mỗi khi gặp tín hiệu này nhóm đánh dấu xuống đất, và các dấu đó nằm trên một đường thẳng cắt ngang đường.
3. Ảnh chụp từ trên cao có một vết cắt bê tông thẳng, nằm đúng chỗ đó.

**Nói bằng tiếng Anh:** *For C2 and C4, partly yes, and we say so: their start points were not measured, so we placed them using the cable marks we painted on site. The independent evidence is three things: C1 and C3, walked forward, both put P1 at 2.50 m on their own; the marks we made on the ground while scanning lie on one straight line across the road; and the top-view photo shows a straight saw-cut in the concrete at the same place.*

**Lưu ý:** đây là câu khó nhất cả bài. Nhận thẳng trước, rồi mới đưa ba bằng chứng.

**C30 ★★★ – Sao biết P1 là cáp, mà không phải thanh thép hay cục đá?**

**Ý trả lời:** Có ba lý do. Nó xuất hiện trên cả bốn tuyến song song và nằm trên một đường thẳng, cục đá thì không như vậy. Nó có đuôi rung dài, kiểu thường thấy ở kim loại. Và nó nằm ở độ sâu hay chôn cáp. Tuy vậy nhóm chưa đào hay đo RD7000 để kiểm chứng, nên nói cho chính xác thì đây là một vật kim loại chạy thẳng, nhiều khả năng là cáp.

**Nói bằng tiếng Anh:** *Three reasons: it appears on all four parallel lines along one straight path — a stone would not; it has a long ringing tail typical of metal; and it is at a typical cable depth. But we have not verified it by excavation or with the RD7000, so strictly it is a linear metallic target, most likely a cable.*

**C31 ★★ – Sao ở C1 cáp lại sâu tới 0,65 m, còn mấy tuyến khác chỉ 0,45 m?**

**Ý trả lời:** Có thể vì ba lý do, hiện nhóm chưa tách ra được: cáp chúi sâu xuống ở phía mép đường đó; lớp mặt đường ở đó dày hơn; hoặc hyperbol ở C1 yếu hơn nên nhóm chọn điểm đỉnh bị trễ. Sau migration thì đỉnh ở C1 còn khoảng 0,53 m, gần với các tuyến kia hơn.

**Nói bằng tiếng Anh:** *We have three possible reasons and cannot separate them yet: the cable may dip near that edge of the road; the pavement may be thicker there; or our pick on C1 is later because the hyperbola there is weaker. After migration the C1 apex is at about 0.53 m, closer to the others.*

**C32 ★★ – Kích thước 31 × 14 cm ở slide dự phòng là đường kính cáp à?**

**Ý trả lời:** Không. Đó là kích thước vật trông thấy trên ảnh sau migration, bị giới hạn bởi độ phân giải: khoảng 10 cm theo chiều sâu và 30 cm theo chiều ngang ở độ sâu này. Cáp thật chỉ vài cm.

**Nói bằng tiếng Anh:** *No. That is the apparent size after migration, limited by resolution — about 10 cm vertically and 30 cm horizontally at this depth. A real cable is a few centimetres.*

**C33 ★ – Mấy tuyến đo ngược chiều thì xử lý thế nào?**

**Ý trả lời:** Nhóm lật C2, C4, N2, N4 lại cho mọi tuyến cùng một chiều. Việc lật này được kiểm tra bằng cách so với ảnh nhóm đã chú thích: lật thì độ tương quan 0,61–0,67, không lật chỉ 0,34–0,51.

**Nói bằng tiếng Anh:** *We flipped C2, C4, N2 and N4 so that all lines share the same direction. The flip is confirmed by correlation with the images the team annotated: 0.61–0.67 flipped versus 0.34–0.51 not flipped.*

### Slide 12 – Ống nước

**C34 ★★★ – Ống chỉ thấy trên 3 trong 5 tuyến, sao dám nối thành một đường?**

**Ý trả lời:** Vì ở N2, N4 và N5, ống đều nằm cách mép đường cỡ một mét, khớp với những gì nhóm kiểm tra ngoài hiện trường: một ống thẳng chạy song song mép đường. Đoạn nằm giữa các tuyến là nội suy, nên nhóm chỉ đánh giá độ tin cậy trung bình, không phải cao.

**Nói bằng tiếng Anh:** *We connect N2, N4 and N5 because they fall at about the same distance from the road edge — about one metre — which matches our field check: a straight pipe parallel to the road. Between lines it is interpolated, and that is why we rate it medium, not high, confidence.*

**Lưu ý:** nhóm thống nhất trước "kiểm tra ngoài hiện trường" cụ thể là thấy gì, ai xác nhận, để nói tiếp được nếu bị hỏi sâu.

**C35 ★★ – Sao N1, N3 không thấy hyperbol?**

**Ý trả lời:** Ở N1 chỉ thấy các lớp mặt đường nằm ngang. Có thể tuyến không cắt qua ống ở chỗ nhóm nghĩ, có thể chỗ đó có khớp nối làm tín hiệu khác đi, hoặc độ tương phản quá yếu. Nhóm không thấy thì không kết luận là có ống.

**Nói bằng tiếng Anh:** *On N1 we see only flat pavement layers. Possible reasons: the line may not cross the pipe where we think, a joint or fitting may change the reflection, or the contrast is weak. We do not claim a pipe where we do not see one.*

**C36 ★★ – Ống bằng nhựa hay kim loại? Đường kính bao nhiêu?**

**Ý trả lời:** Từ số liệu hiện có thì nhóm không nói được. Hyperbol không gom gọn sau migration, và dấu sóng dội cũng không phân biệt được ống nhựa chứa nước với kim loại. Nhóm chỉ đưa ra vị trí và độ sâu tới mặt trên của ống.

**Nói bằng tiếng Anh:** *We cannot tell from our data. The hyperbola does not focus well after migration, and polarity cannot separate a water-filled plastic pipe from metal. We report only the position and depth to the top.*

**C37 ★ – Độ sâu là tính tới mặt trên hay tâm ống?** Tới **mặt trên** của ống. Muốn ra tâm thì cộng thêm bán kính, mà bán kính thì chưa biết.

### Slide 13 – Video 3D

**C38 ★★ – Hình 3D là số liệu đo thật hay vẽ ra?**

**Ý trả lời:** Ảnh ra đa và các điểm đỉnh là số liệu thật, mặt đất là ảnh nhóm chụp từ trên cao. Đoạn ống và cáp nằm giữa các tuyến là nối thẳng (nội suy), còn phần nét đứt ra ngoài vùng đo là kéo dài thêm (ngoại suy), không phải đo được.

**Nói bằng tiếng Anh:** *The radargrams and the apex points are real data. The ground is our top-view photo. The pipe and cable between lines are straight-line interpolation, and the dashed parts beyond the survey area are extrapolation, not measurement.*

### Slide 14 – Tổng hợp và đánh giá

**C39 ★★★ – Độ tin cậy cao, trung bình, thấp dựa vào đâu?**

**Ý trả lời:** Nhóm tự đặt tiêu chí đơn giản: bao nhiêu tuyến thấy vật, và có khớp với dấu ngoài hiện trường không. Cao là thấy trên cả bốn tuyến và khớp dấu; trung bình là ba trên năm tuyến; thấp là chỉ một tuyến. Đây không phải cấp chất lượng chính thức của PAS 128; theo PAS 128 thì khảo sát của nhóm mới tới loại B (dò bằng máy), chưa có loại A (đào lộ ra để kiểm chứng).

**Nói bằng tiếng Anh:** *Our own simple criteria: how many lines show the target, and whether field marks agree. High: all four lines plus field marks. Medium: three of five lines. Low: one line only. It is not a formal PAS 128 quality level; our survey corresponds to a PAS 128 type B detection survey, without type A verification by excavation.*

**C40 ★★ – Sai số ±0,1 m tính thế nào?**

**Ý trả lời:** Đó là độ chênh giữa hai cách chọn vận tốc ở độ sâu cỡ nửa mét, khoảng 20 %. Đây chưa phải phân tích sai số đầy đủ; còn sai số do chọn điểm đỉnh và do đặt vị trí tuyến cộng thêm vào.

**Nói bằng tiếng Anh:** *It is the spread between the two velocity models at about half a metre depth — roughly 20 %. It is not a full error analysis; picking error and line position error add to it.*

### Slide 15 – Kết luận

**C41 ★★ – Kết luận thứ ba (dùng cả hai tần số) có số liệu chứng minh không?**

**Ý trả lời:** Kết quả cáp và ống là của kênh 250 MHz; còn kênh 700 MHz thì cho hình gần mặt đất nét hơn ở các lát cắt theo độ sâu. Nên kết luận ba là nhận xét từ những gì nhóm thấy, chưa phải một phép so sánh có đo đạc.

**Nói bằng tiếng Anh:** *Our cable and pipe results use the 250 MHz channel; the 700 MHz channel gave sharper shallow images in the depth slices. So conclusion three is a qualitative observation from our data, not a measured comparison.*

**C42 ★★ – Nếu làm lại thì nhóm sửa gì trước tiên?**

**Ý trả lời:** Trước hết là chốt vận tốc ở một điểm biết chắc độ sâu, bằng cách đào thử một hố nhỏ hoặc đo RD7000. Sau đó dùng GPS hoặc máy toàn đạc để định vị các tuyến. Cuối cùng là chạy mô phỏng gprMax để kiểm tra dấu sóng dội.

**Nói bằng tiếng Anh:** *Calibrate the velocity at one known point — a small test pit or the RD7000 — and fix line positions with GPS or a total station. Then run the gprMax simulation for the polarity.*

### Câu hỏi chung

**C43 ★★ – Mỗi bạn trong nhóm làm phần nào?** Mỗi người chuẩn bị sẵn một câu nói về phần mình: ai đo, ai xử lý trên ReflexW, ai vẽ bản đồ, ai làm slide.

**C44 ★ – Đo ngày nào, thời tiết ra sao?** Lấy từ nhật ký hiện trường. Nếu trước đó trời mưa thì đất ướt, sóng chạy chậm hơn và yếu nhanh hơn.

---

## D. Nên sửa trước khi nộp

| # | Việc cần làm | Vì sao |
|---|---|---|
| D1 | Điền tên nhóm và giảng viên hướng dẫn vào `_build/tao_seminar.js` (hai dòng `GROUP`, `SUPERVISOR`) rồi dựng lại slide | Hiện slide 1, slide 16 và chân mọi slide còn để trống `[ ]` |
| D2 | ✅ Đã sửa: slide 15 ghi "Fix line positions with GPS or a total station" thay vì "odometer wheel" | Máy đã tự ghi 2,78 cm một vết; thứ còn thiếu là vị trí bắt đầu của các tuyến |
| D3 | Thống nhất năm của hai bài báo: slide ghi Nguyễn Thành Vấn (2018) và Nguyễn Văn Thuận, Lê Văn Anh Cường (2021), còn `references.bib` ghi 2019 và 2020 | Thầy cô đọc trang tài liệu tham khảo sẽ thấy lệch |
| D4 | Kiểm tra lại con số 28 % "do định vị sai" trong báo cáo CGA DIRT 2019 và mốc giờ vụ Cao Hùng (xem `README_CauTruc_10phut.md`) | Số liệu mở đầu mà bị hỏi thì phải nói được nguồn |
| D5 | Slide dự phòng "Plan view" (`BanDo_OngNuoc_Cap.png`) còn vẽ ống nước chéo, nét đứt, trong khi cách hiểu hiện tại là ống chạy thẳng dọc đường | Mở slide này ra khi bị hỏi sẽ vênh với slide 12 và 14. Chạy lại `02_SoDoTuyen_BanDo/dung_ban_do_3d.py` hoặc bỏ slide |
| D6 | Thống nhất căn cứ để nói "dưới sân có ống và cáp" (C3) và "kiểm tra ngoài hiện trường" (C34) | Hai câu này rất dễ bị hỏi |
