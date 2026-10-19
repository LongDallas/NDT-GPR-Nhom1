# Xử lý dữ liệu GPR

## Các bước xử lý dữ liệu

1. **Move start time**
2. **Bộ lọc 1D** (lọc từng trace): bộ lọc trung bình trường, bộ lọc tần số (1D filter)
3. **Bộ lọc 2D** (lọc nhiều traces)
   - Ranh giới: không dùng khử nhiễu nền.
   - Xác định dị vật (kích thước): khử nhiễu nền.
   - Lọc nhiễu bằng các thuật toán.
4. **Khuếch đại (gain)**: gain energy, auto-gain (AGC), gain function, ...

**Xác định kích thước: migration**

- Quan trọng nhất là tính được vận tốc → độ sâu đúng, kích thước đúng.

---

## Chương 3

1. **Giới thiệu khu vực khảo sát**
   - Mục tiêu, tuyến, sơ đồ tuyến khảo sát → tổng quan tuyến khảo sát.
2. **Kết quả**
   1. Trình bày xử lý đo chi tiết.
   2. Trực quan bằng các mô hình 2D, 3D sơ đồ tuyến.
3. **Tiểu kết chương**
   - Làm được
   - Chưa làm được
   - Kiến nghị

---

## Mẫu (quy trình xử lý)

1. Move start time
2. Lọc 1D: dùng *subtract DC shift* (trung bình trường), *dewow subtract mean* (why 1.428?)
3. ...
