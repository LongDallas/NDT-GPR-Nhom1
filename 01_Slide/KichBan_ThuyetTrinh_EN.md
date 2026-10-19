# Kịch bản thuyết trình (tiếng Anh) – Seminar GPR, 10 phút

> Dùng cho bộ slide [Seminar_GPR_EN_v3.pptx](Seminar_GPR_EN_v3.pptx) (17 slide + 4 dự phòng; kịch bản viết cho bản v2 – lời nói mới của slide 3–5, 15 và 17 nằm trong Notes của bản v3).
> Lời nói viết **tiếng Anh**. Dòng *Ý chính* bằng tiếng Việt để người nói hiểu mình đang nói gì, **không đọc lên**.
> Ký hiệu: **[BẤM]** = bấm chuyển; *[nghiêng trong ngoặc]* = động tác, không đọc; **đậm** = nhấn giọng.
> Tổng ≈ 1.300 từ ≈ 10:00 ở tốc độ ~130 từ/phút. Tập với đồng hồ: mỗi slide có mốc giờ.
> Thuật ngữ và câu hỏi phản biện: [GiaiThich_ThuatNgu_PhanBien.md](GiaiThich_ThuatNgu_PhanBien.md). Bản dịch tiếng Việt của kịch bản: [KichBan_ThuyetTrinh_VI.md](KichBan_ThuyetTrinh_VI.md).

## Chia người nói (đề xuất, mỗi người khoảng 2 phút)

| Người | Slide | Thời gian | Phần |
|---|---|---|---|
| 1 | 1–3 | 0:00 – 2:00 | Câu chuyện mở đầu, mục lục, đặt vấn đề |
| 2 | 4–6 | 2:00 – 4:05 | Tổng quan tài liệu, so sánh NDT, nguyên lý GPR |
| 3 | 7–9 | 4:05 – 6:05 | RD7000, đo hiện trường, xử lý dữ liệu |
| 4 | 10–13 | 6:05 – 8:10 | Mô hình, kết quả cáp, kết quả ống, video 3D |
| 5 | 14–16 | 8:10 – 10:00 | Tổng hợp và đánh giá, kết luận, cảm ơn và hỏi đáp |

Nếu thầy cho ít người nói hơn thì gộp theo phần: (1+2), (3+4), 5. Câu chuyển lượt (*handover*) đã viết sẵn cuối mỗi phần; nếu một người nói liền thì bỏ câu đó.

## Phát âm cần tập trước

| Từ | Đọc gần đúng | Từ | Đọc gần đúng |
|---|---|---|---|
| Kaohsiung | kao-SHÙNG | permittivity | pơ-mi-TÍ-vi-ti |
| radargram | RÊY-đa-gram | hyperbola | hai-PƠ-bơ-lơ |
| apex | ÊY-pếch | anomaly | ơ-NÓ-mơ-li |
| polarity | pâu-LA-ri-ti | perpendicular | pơ-pần-ĐÍ-kiu-lơ |
| dewow | ĐI-wao | Kirchhoff migration | KIA-khóp mai-GRÊY-shơn |
| electromagnetic induction | i-lec-trâu-mag-NÉ-tic in-ĐẮC-shơn | megahertz | MÉ-gơ-hơts |

---

## NGƯỜI 1

### Slide 1 – Hook (0:00 – 1:00) · 4 lần bấm

*[Màn hình đen. Đứng yên, nhìn khán phòng, im lặng 2 giây rồi mới nói. Nói chậm, câu ngắn.]*

> July thirty-first, 2014. Kaohsiung, Taiwan.
> Late in the evening, people on the street smell gas.
> Firefighters search for the leak — for almost **three hours**.
> They cannot find it. *[ngừng 1 giây]*

**[BẤM 1]** *[ảnh con đường bị xé toạc]*

> Just before midnight, the street explodes.
> **Thirty-two people dead. Three hundred and twenty-one injured.** *[chậm, trầm giọng]*
> The cause: a leaking pipe under their feet — that **nobody could see**.

**[BẤM 2]** *[hai con số lớn]*

> And this is not rare. In the US, buried utilities are hit more than **half a million times a year**.
> In Ho Chi Minh City, a newspaper put it simply: *dig up any street, and you hit a spider web.*

**[BẤM 3]** *[ảnh sân trường. Đổi giọng sang trò chuyện, chỉ tay vào ảnh]*

> Now look at this. Our own campus.
> Under this asphalt there is a water pipe and a power cable — and **no drawing** of where they are.
> If someone digs here tomorrow… where is it safe?
> Today we answer that — **without digging a single hole.**
> We are Quốc Long, Quốc Tài, Thành Trung, Đăng Khoa and Đăng Quang.

*Ý chính:* thảm họa thật → con số → về TP.HCM → về chính sân trường. Tên đề tài đã hiện trên màn hình, không cần đọc lại.

### Slide 2 – Outline (1:00 – 1:15)

> Our talk has five parts: the problem, previous work, our methods, our results, and what we conclude.

*Ý chính:* đọc nhanh, chỉ tay theo 5 số.

### Slide 3 – 1 Introduction (1:15 – 2:00)

> **The problem:** there is no as-built drawing of this courtyard, and digging blind is how strikes happen — over a quarter of utility damage in the US starts with a **locating** error.
> **Our objectives:** locate the cable and the pipe without digging, estimate their depth, and draw a map.
> **Our approach:** ground-penetrating radar as the main method, and the RD7000 electromagnetic locator for metal lines.
> **We expected** each utility to show as a hyperbola on every line that crosses it. Joining them from line to line gives its path and depth.

*Ý chính:* 4 ô trên slide = vấn đề, mục tiêu, cách làm, kết quả dự kiến.

*Handover:* > **[Tên người 2]** will show what others have done before us.

---

## NGƯỜI 2

### Slide 4 – 2.1 Previous work (2:00 – 2:40)

> Thank you. **Abroad**, the UK project *Mapping the Underworld* found that **no single sensor finds every utility**, so radar and electromagnetic locators are combined. A 2018 review traces thirty years of GPR, from locating objects to imaging them.
> **In Vietnam**, the Geophysics group at our own university used the same radar — the IDS Detector Duo — to map pipes and cables in Ho Chi Minh City.
> We apply the same chain, end to end, on a site with **no drawings at all**.

*Ý chính:* nhóm không mới về phương pháp; điểm của nhóm là tự làm trọn quy trình trên một hiện trường chưa có bản vẽ.

### Slide 5 – 2.2 NDT methods and scope (2:40 – 3:10)

> Among these five NDT methods, *[chỉ dòng GPR]* only ground-penetrating radar sees **both metal and plastic** without contact. The electromagnetic locator is fast but sees metal only; magnetometers see only iron; resistivity is too coarse for a small pipe.
> So our scope: shallow utilities, under one metre, in one courtyard — with GPR as the main method.

*Ý chính:* vì sao chọn GPR.

### Slide 6 – 3.1 Principle of GPR (3:10 – 4:05)

> GPR is the **pulse–echo** method from this course — like ultrasonic testing, but with an electromagnetic pulse, so no contact is needed.
> *[công thức 1]* The wave speed depends on the relative permittivity: *v equals c over the square root of epsilon r.*
> *[2]* The radar measures the **two-way** time, so depth is *v times t, over two.*
> *[3]* Energy reflects where the permittivity changes. Metal gives *R equal to minus one*; an empty pipe gives a positive R — **opposite polarity**.
> *[4, chỉ hình bên trái]* As the antenna crosses a small target, the echo comes back earliest right above it. So a pipe draws a **hyperbola**, and its apex gives position and depth.
> *[ô Resolution]* Resolution is about a quarter wavelength: ten centimetres at 250 megahertz, under four at 700. Low frequency sees deeper; high frequency is sharper.

*Ý chính:* 4 công thức = vận tốc, độ sâu, phản xạ, hyperbol. Không giải thích sâu; để dành cho phần hỏi đáp.

*Handover:* > **[Tên người 3]** continues with the second method and our field work.

---

## NGƯỜI 3

### Slide 7 – 3.2 Electromagnetic locator, RD7000 (4:05 – 4:35)

> The second method is **electromagnetic induction**. A current in a metal cable makes a magnetic field that falls off as one over r. Right above the cable, the horizontal coil gives a **peak** and the vertical coil a **null**; two coils give the depth.
> But it sees metal only. For us it is the **planned cross-check** of the cable depth — we have not measured with it yet.

*Ý chính:* nói rõ "chưa đo RD7000" ngay trên slide, để không bị hỏi vặn.

### Slide 8 – 3.3 Field survey (4:35 – 5:25)

> We laid out a grid, ten by three and a half metres. *[chỉ ảnh lưới]* A target gives the clearest hyperbola when it is crossed **at a right angle**. So four lines run **along** the road — C1 to C4, one metre apart — to cross the cable; and five lines **cross** the road — N1 to N5, about eighty centimetres apart — to cross the water pipe.
> *[chỉ 4 ảnh]* We marked the lines, set up the IDS Detector Duo with both antennas, scanned every line, and checked each radargram on site.
> *[chỉ bảng]* One trace every 2.78 centimetres; ten scans, including a repeat of N5.

*Ý chính:* lý do bố trí tuyến là ý quan trọng nhất của slide này.

### Slide 9 – 3.4 Data processing (5:25 – 6:05)

> Each processing step removes **one** problem. *[chỉ lần lượt 1 → 6]* Time zero goes to the ground surface; DC removal and dewow take away the slow drift; background removal deletes the flat bands repeated on every trace; gain lifts the weak, deep echoes.
> *[chỉ hình]* Left, raw line N5; right, after processing — the water-pipe hyperbola is clear.
> Migration at 0.095 metres per nanosecond focuses each hyperbola. For depth we use two layers: 0.12 in the concrete, 0.10 in the soil.

*Ý chính:* mỗi bước nói một câu "bỏ cái gì". Hai vận tốc khác nhau là điểm dễ bị hỏi (xem C24).

*Handover:* > So — what did we find? **[Tên người 4]**.

---

## NGƯỜI 4

### Slide 10 – 4.1 Model results (6:05 – 6:40)

> Before trusting the field data, we built a simple model: a metal cable and an empty PVC pipe, both 45 centimetres deep, under a 250-megahertz pulse.
> It predicts an apex at about 9.5 nanoseconds — and the real hyperbolas on C1 and N5 follow the **same curve**, the dashed gold line.
> It also shows the opposite polarity from equation three. This is a ray model; a gprMax simulation is our next step.

*Ý chính:* mô hình là bước kiểm tra tính hợp lý, không phải bằng chứng độc lập.

### Slide 11 – 4.2 The power cable (6:40 – 7:20)

> One hyperbola alone could be a stone. So we look for the **same echo on neighbouring lines**.
> *[chỉ 4 mặt cắt từ trên xuống]* On all four lines, C1 to C4, we find the same anomaly, P1 — a strong hyperbola with a long **ringing** tail, typical of metal.
> *[chỉ đường đứt cam]* The apexes line up at two and a half metres: the cable crosses the road **at a right angle** — exactly where we marked the ground on site.
> *[chỉ thẻ]* Depth to the top: about forty-five centimetres, and sixty-five on C1.

*Ý chính:* bằng chứng chính của cả bài. Câu hỏi khó nhất (C29: vị trí C2, C4) đã chuẩn bị sẵn câu trả lời.

### Slide 12 – 4.3 The water pipe (7:20 – 7:50)

> For the water pipe we use the lines across the road. *[a]* On N2 there is a clear hyperbola, A1, 43 centimetres deep. We see the same pipe on N4 and N5, about **one metre** from the bench-side edge.
> *[b]* On N1 we see only flat pavement layers — so we do not claim a pipe there. *[c, d]* And we do not claim a pipe size, only its depth.

*Ý chính:* trung thực về chỗ không thấy.

### Slide 13 – 4.4 Video 3D (7:50 – 8:10) · video tự chạy 19 giây

> This is our survey in 3D, built from the real data. The cart scans every line, the radargrams appear, and the apexes are joined: the **orange cable** across the road, the **blue pipe** along it.

*Ý chính:* nói ít, để video chạy.

*Handover:* > **[Tên người 5]** will sum up.

---

## NGƯỜI 5

### Slide 14 – 4.5 Results summary and evaluation (8:10 – 8:55)

> So — what is under our feet? *[chỉ bảng]*
> A **power cable** crosses the road at a right angle, about 45 centimetres deep, seen on all four lines: high confidence.
> A **water pipe** runs along the road, about a metre from the edge, 43 to 59 centimetres deep, seen on three of five lines: medium confidence.
> Five other reflectors appear on one line only; we do not interpret them.
> *[ô dưới trái]* Our main uncertainty is the wave speed: depths could be about **twenty per cent** off.
> In Kaohsiung, nobody could see the pipe. **Here, we can.**

*Ý chính:* trả lời câu hỏi ở slide 1, nêu rõ mức tin cậy và sai số.

### Slide 15 – 5 Conclusions and recommendations (8:55 – 9:40)

> Three conclusions. **One:** GPR found a cable and a water pipe under asphalt, without digging. **Two:** crossing the target at a right angle is what makes the hyperbola appear. **Three:** 700 megahertz is sharper, 250 goes deeper — using both is safer.
> And two limits. Depth depends on the wave speed, so we would calibrate with the RD7000 or one small test pit. And our line positions were set by hand, so a GPS or a total station would make the map more accurate.
> **Locating well is exactly what GPR is for.**

*Ý chính:* 3 kết luận, 2 hạn chế kèm hướng khắc phục.

### Slide 16 – References, Thank you, Q&A (9:40 – 10:00)

> At the start we asked: *what is under our feet?* **Now we know** — a cable crossing the road and a water pipe along it, about half a metre down.
> Thank you for listening. We are happy to take your questions.

---

## Phần hỏi đáp

**Khi nhận câu hỏi:**
- *Thank you, that's a good question.* / *Let me make sure I understand: you are asking whether …?*
- Nếu chưa nghe rõ: *Sorry, could you repeat the question, please?*

**Khi trả lời:** một câu trả lời thẳng trước, rồi mới giải thích; mở slide dự phòng nếu cần.
- *The short answer is … The reason is …*
- *We can show that on a backup slide.* → bản đồ mặt bằng, lát cắt độ sâu, mặt cắt C1/C3, migration.

**Khi không biết hoặc chưa làm:** nói thẳng, kèm hướng làm tiếp.
- *We did not measure that. If we did it again, we would …*
- *That is a limitation of our survey. Our evidence for this point is …*

**Kết thúc:** *Thank you. If there are no more questions, that concludes our presentation.*

## Nếu lố giờ (cắt theo thứ tự)

1. Slide 5: chỉ nói câu "Only GPR sees both metal and plastic…" (~10 s).
2. Slide 7: chỉ nói đoạn "But it sees metal only… not measured with it yet" (~15 s).
3. Slide 10: bỏ câu cuối về ray model và gprMax (~5 s).
4. Slide 9: bỏ câu về hai vận tốc, để dành cho hỏi đáp (~8 s).

**Không cắt** slide 1, 11, 14: đó là câu chuyện, bằng chứng chính và câu trả lời.
