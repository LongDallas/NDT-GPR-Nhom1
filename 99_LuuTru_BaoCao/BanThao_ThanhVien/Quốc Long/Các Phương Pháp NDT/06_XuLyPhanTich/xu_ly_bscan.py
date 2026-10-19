"""Xử lý cơ bản B-scan GPR và khớp hyperbol để ước lượng vận tốc, độ sâu.

Cách dùng:
    # 1) Dữ liệu mô phỏng gprMax (cần: pip install h5py)
    python xu_ly_bscan.py ../04_MoPhong_gprMax/cap_ngam_2D_merged.out --dx 0.01

    # 2) Dữ liệu thực xuất ra dạng .npy (ma trận [số mẫu, số vết]) kèm bước thời gian
    python xu_ly_bscan.py tuyen_T01.npy --dt 0.1e-9 --dx 0.02

    # 3) Tự kiểm tra bằng dữ liệu tổng hợp (không cần file)
    python xu_ly_bscan.py --demo

Các bước xử lý: time-zero -> dewow -> xóa nền -> khuếch đại SEC -> vẽ hình.
Khớp hyperbol: t(x) = (2/v) * sqrt((x - x0)^2 + (d + R)^2) - 2R/v
(d: độ sâu tới đỉnh vật, R: bán kính vật, v: vận tốc sóng điện từ trong đất).
"""
import argparse
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

C0 = 0.2998  # vận tốc ánh sáng, m/ns


def doc_du_lieu(duong_dan, dt=None, thanh_phan="Ez"):
    """Trả về (B-scan [mẫu, vết], dt tính bằng giây)."""
    p = Path(duong_dan)
    if p.suffix == ".out":
        import h5py

        with h5py.File(p, "r") as f:
            return np.array(f["rxs"]["rx1"][thanh_phan]), float(f.attrs["dt"])
    if p.suffix == ".npy":
        if dt is None:
            raise SystemExit("Cần --dt (giây) cho dữ liệu .npy")
        return np.load(p), dt
    raise SystemExit(f"Chưa hỗ trợ định dạng {p.suffix}; hãy xuất dữ liệu ra .npy")


def time_zero(b, nguong=0.1):
    """Cắt bỏ phần trước sóng đến đầu tiên (lấy trung vị trên các vết)."""
    bien = np.abs(b)
    chi_so = [np.argmax(bien[:, j] > nguong * bien[:, j].max()) for j in range(b.shape[1])]
    return b[int(np.median(chi_so)):, :]


def dewow(b, cua_so=31):
    """Trừ trung bình trượt dọc theo trục thời gian để bỏ thành phần tần số thấp."""
    nhan = np.ones(cua_so) / cua_so
    nen = np.apply_along_axis(lambda v: np.convolve(v, nhan, mode="same"), 0, b)
    return b - nen


def xoa_nen(b):
    """Trừ vết trung bình (background removal) để làm nổi hyperbol."""
    return b - b.mean(axis=1, keepdims=True)


def khuech_dai_sec(b, dt, alpha=0.0, mu=1.0):
    """Khuếch đại bù suy giảm hình cầu và hấp thụ: g(t) = t^mu * exp(alpha t)."""
    t = (np.arange(b.shape[0]) + 1) * dt * 1e9  # ns
    g = t**mu * np.exp(alpha * t)
    return b * (g / g.max())[:, None]


def mo_hinh_hyperbol(x, x0, d, v, R=0.0):
    return 2.0 / v * np.sqrt((x - x0) ** 2 + (d + R) ** 2) - 2.0 * R / v


def khop_hyperbol(x, t, R=0.0):
    """Khớp (x0, d, v) bằng quét lưới và bình phương tối thiểu (chỉ cần numpy)."""
    tot = (np.inf, None)
    for v in np.linspace(0.04, 0.20, 161):
        for x0 in np.linspace(x.min(), x.max(), 101):
            # với v và x0 cố định, chọn d để khớp đỉnh hyperbol
            d = max(v * t.min() / 2.0, 1e-3)
            sai_so = np.mean((mo_hinh_hyperbol(x, x0, d, v, R) - t) ** 2)
            if sai_so < tot[0]:
                tot = (sai_so, (x0, d, v))
    x0, d, v = tot[1]
    return {"x0": x0, "d": d, "v": v, "eps_r": (C0 / v) ** 2, "rmse_ns": np.sqrt(tot[0])}


def ve_bscan(b, dt, dx, tieu_de, duong_dan_ra, diem_hyperbol=None):
    t_max = b.shape[0] * dt * 1e9
    x_max = b.shape[1] * dx
    gioi_han = np.percentile(np.abs(b), 99)
    fig, ax = plt.subplots(figsize=(6.3, 3.6), dpi=200)
    ax.imshow(b, cmap="gray", aspect="auto", vmin=-gioi_han, vmax=gioi_han,
              extent=[0, x_max, t_max, 0])
    if diem_hyperbol is not None:
        x, t = diem_hyperbol
        ax.plot(x, t, color="white", lw=1.0, ls="--", label="Hyperbol khớp")
        ax.legend(loc="lower right", fontsize=8, frameon=True)
    ax.set_xlabel("Khoảng cách theo tuyến (m)")
    ax.set_ylabel("Thời gian hai chiều (ns)")
    ax.set_title(tieu_de, fontsize=10)
    fig.tight_layout()
    fig.savefig(duong_dan_ra)
    plt.close(fig)


def du_lieu_demo(dt=0.025e-9, dx=0.01, v=0.10, x0=0.8, d=0.40, R=0.025):
    """B-scan tổng hợp: một hyperbol với xung Ricker 700 MHz cộng nhiễu."""
    x = np.arange(0, 1.6, dx)
    t = np.arange(0, 25e-9, dt)
    f = 700e6
    b = np.zeros((t.size, x.size))
    for j, xj in enumerate(x):
        for t0, a in [(1.5e-9, 1.0), (1.5e-9 + mo_hinh_hyperbol(xj, x0, d, v, R) * 1e-9, 0.3)]:
            tau = np.pi * f * (t - t0)
            b[:, j] += a * (1 - 2 * tau**2) * np.exp(-tau**2)
    rng = np.random.default_rng(0)
    return b + 0.01 * rng.standard_normal(b.shape) + 0.05, dt, dx, (x0, d, v, R)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tep", nargs="?", help=".out (gprMax) hoặc .npy")
    ap.add_argument("--dt", type=float, help="bước thời gian (s), bắt buộc với .npy")
    ap.add_argument("--dx", type=float, default=0.01, help="khoảng cách vết (m)")
    ap.add_argument("--ra", default="../07_HinhAnh/Chuong3", help="thư mục lưu hình")
    ap.add_argument("--demo", action="store_true", help="chạy thử với dữ liệu tổng hợp")
    a = ap.parse_args()

    if a.demo:
        b, dt, dx, dung = du_lieu_demo()
        ten = "demo"
    else:
        if not a.tep:
            ap.error("cần đường dẫn tệp hoặc --demo")
        b, dt = doc_du_lieu(a.tep, a.dt)
        dx, ten, dung = a.dx, Path(a.tep).stem, None

    ra = Path(a.ra)
    ra.mkdir(parents=True, exist_ok=True)
    ve_bscan(b, dt, dx, "B-scan thô", ra / f"{ten}_01_tho.png")

    b2 = khuech_dai_sec(xoa_nen(dewow(time_zero(b))), dt)
    # Chọn đỉnh mạnh nhất trên từng vết làm điểm hyperbol (đơn giản; dữ liệu thực nên chọn tay)
    t_ns = np.arange(b2.shape[0]) * dt * 1e9
    x = np.arange(b2.shape[1]) * dx
    bo_qua = int(3e-9 / dt)  # bỏ 3 ns đầu (sóng trực tiếp còn sót)
    t_dinh = t_ns[bo_qua + np.argmax(np.abs(b2[bo_qua:, :]), axis=0)]
    giu = np.abs(b2[bo_qua:, :]).max(axis=0) > 0.3 * np.abs(b2[bo_qua:, :]).max()
    kq = khop_hyperbol(x[giu], t_dinh[giu])

    xx = np.linspace(x[giu].min(), x[giu].max(), 200)
    ve_bscan(b2, dt, dx, "Sau xử lý: time-zero, dewow, xóa nền, SEC",
             ra / f"{ten}_02_xuly.png", (xx, mo_hinh_hyperbol(xx, kq["x0"], kq["d"], kq["v"])))

    print(f"x0 = {kq['x0']:.3f} m | độ sâu d = {kq['d']:.3f} m | v = {kq['v']:.4f} m/ns "
          f"| eps_r = {kq['eps_r']:.2f} | RMSE = {kq['rmse_ns']:.3f} ns")
    if dung:
        print(f"(Giá trị đúng của demo: x0 = {dung[0]}, d+R = {dung[1] + dung[3]:.3f}, v = {dung[2]})")
    print(f"Đã lưu hình vào {ra.resolve()}")


if __name__ == "__main__":
    main()
