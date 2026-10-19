"""Cảnh 3D tương tác (Three.js) của khu khảo sát: mặt đất là ảnh IMG_9558 đã nắn thẳng,
có ghế đá, tường nhà; máy GPR chạy theo các tuyến; bên dưới là ống nước, cáp và mặt cắt radargram.
Bấm vào ống nước / cáp / điểm dị vật để xem thông số. Chữ trong cảnh viết tiếng Anh (dùng khi thuyết trình).

Được gọi từ dung_ban_do_3d.py -> ket_qua/Canh3D_HienTruong.html (mở bằng trình duyệt, cần Internet để tải three.js).
"""
import base64
import io
import json

import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates

import ve_so_do_anh as anh_ht

THREE_CDN = "https://cdn.jsdelivr.net/npm/three@0.160.0"
Z_MAX = 1.2           # độ sâu hiển thị mặt cắt (m)
VUNG_DAT = (-3.0, 11.0, -1.0, 6.3)  # x0, x1, y0, y1 (m) – phần ảnh phủ được
DO_PHAN_GIAI = 0.01   # m / pixel cho ảnh mặt đất
# ghế đá: vị trí dọc đường (m) đo trên ảnh IMG_9558, mỗi vị trí là 2 ghế quay lưng vào nhau
GHE_X = [0.18, 1.43, 2.73, 3.92, 5.17, 6.23, 7.56, 8.88, 10.19]


def _b64(anh, dang="JPEG", **kw):
    buf = io.BytesIO()
    anh.save(buf, dang, **kw)
    return f"data:image/{dang.lower()};base64," + base64.b64encode(buf.getvalue()).decode()


def anh_mat_dat():
    """Nắn ảnh IMG_9558 về mặt bằng (x, y) bằng homography; hàng 0 = y lớn nhất (khớp UV của plane)."""
    x0, x1, y0, y1 = VUNG_DAT
    xs = np.arange(x0, x1, DO_PHAN_GIAI)
    ys = np.arange(y1, y0, -DO_PHAN_GIAI)
    X, Y = np.meshgrid(xs, ys)
    u, v = anh_ht.px(X, Y)
    goc = np.asarray(Image.open(anh_ht.ANH).convert("RGB"), dtype=np.float32)
    kenh = [map_coordinates(goc[..., c], [v, u], order=1, mode="nearest") for c in range(3)]
    anh = Image.fromarray(np.clip(np.dstack(kenh), 0, 255).astype(np.uint8))
    return _b64(anh, quality=82)


def anh_bscan(t, mo_hinh):
    """Radargram của một tuyến thành ảnh xám có kênh alpha (cột 0 = vết đầu tiên, hàng 0 = mặt đất).

    Các hàng chia đều theo độ sâu 0..Z_MAX (đổi thời gian -> độ sâu bằng mo_hinh["thoi_gian"]), để đỉnh hyperbol
    trên mặt cắt nằm đúng độ sâu của ống/cáp vẽ trong cảnh.
    """
    b, h = t["b"], t["h"]
    i_z = np.asarray(mo_hinh["thoi_gian"](np.linspace(0, Z_MAX, 241))) / h["dt"]  # chỉ số mẫu (thực) cho mỗi hàng
    phan = map_coordinates(b, np.meshgrid(i_z, np.arange(b.shape[1]), indexing="ij"), order=1, mode="nearest")
    buoc = max(1, phan.shape[1] // 300)
    phan = phan[:, ::buoc]
    gh = np.percentile(np.abs(phan[60:]), 98) + 1e-9  # bỏ ~0,3 m đầu (sóng trực tiếp) khi chọn độ tương phản
    xam = np.clip(127.5 + 127.5 * phan / gh, 0, 255).astype(np.uint8)
    alpha = np.full_like(xam, 235)
    return _b64(Image.fromarray(np.dstack([xam, xam, xam, alpha]), "RGBA"), "PNG", optimize=True)


def xuat_canh_3d(duong, tuyen_bscan, mo_hinh, kenh_bscan, duong_dan):
    """duong: kết quả duong_ong_cap(); tuyen_bscan: các tuyến (không tính đo lặp) dùng làm mặt cắt;
    mo_hinh: dict(thoi_gian=hàm z -> t, v=một vận tốc hoặc None, v_bt, v_dat, z_bt) – cách đổi thời gian ra độ sâu."""
    if mo_hinh["v"]:
        van_toc = f"v = {mo_hinh['v']:.3f} m/ns (ε<sub>r</sub> ≈ {(0.2998 / mo_hinh['v']) ** 2:.1f})"
        cong_thuc = "d = v·t₀ / 2"
    else:
        van_toc = (f"{mo_hinh['v_bt']:.2f} m/ns in concrete (top {mo_hinh['z_bt']:.2f} m), "
                   f"{mo_hinh['v_dat']:.2f} m/ns in soil")
        cong_thuc = "d = Σ v·Δt / 2 over the two layers (team annotation)"
    du_lieu = dict(van_toc=van_toc, cong_thuc=cong_thuc, z_max=Z_MAX, kenh=kenh_bscan.replace("MHz", " MHz"), vung_dat=VUNG_DAT,
                   anh_dat=anh_mat_dat(), ghe_x=GHE_X, khung=[10.0, 3.5], tuyen=[], doi_tuong=[])
    for t in tuyen_bscan:
        du_lieu["tuyen"].append(dict(ten=t["ten"], nhom=t["nhom"], p0=t["xy"][0].round(3).tolist(),
                                     p1=t["xy"][-1].round(3).tolist(), dai=round(float(t["s"][-1]), 2),
                                     anh=anh_bscan(t, mo_hinh)))
    for ten, d in duong.items():
        diem = [dict(tuyen=m["tuyen"], kenh=m["kenh"].replace("MHz", " MHz"), x=round(m["x"], 2),
                     y=round(m["y"], 2), z=round(m["z"], 3), t=round(m["t_ns"], 2)) for m in d["diem"]]
        muc = dict(ten=ten, loai=d["loai"], diem=diem)
        if d["quan_sat"] is not None:
            q = d["quan_sat"]
            muc["quan_sat"] = q.round(3).tolist()
            muc["du_doan"] = [p.round(3).tolist() for p in d["du_doan"]]
            muc["huong"] = round(float(np.degrees(np.arctan2(q[-1, 1] - q[0, 1], q[-1, 0] - q[0, 0])) % 180), 0)
            muc["dai_do"] = round(float(np.hypot(*(q[-1, :2] - q[0, :2]))), 2)
        du_lieu["doi_tuong"].append(muc)
    html = MAU_HTML.replace("__THREE__", THREE_CDN).replace("__DATA__", json.dumps(du_lieu, separators=(",", ":")))
    duong_dan.write_text(html, encoding="utf-8")
    print(f"Đã lưu {duong_dan} ({duong_dan.stat().st_size / 1e6:.1f} MB)")


MAU_HTML = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GPR Site 3D</title>
<style>
:root{--nen:#eef3f8;--the:#ffffffee;--chu:#1d2733;--phu:#5b6b7c;--vien:#d5dde6;--xanh:#1c7ed6;--cam:#e8590c;--xam:#868e96}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--nen:#121820;--the:#1c2430ee;--chu:#e6edf3;--phu:#9fb0c2;--vien:#33414f}}
:root[data-theme="dark"]{--nen:#121820;--the:#1c2430ee;--chu:#e6edf3;--phu:#9fb0c2;--vien:#33414f}
*{box-sizing:border-box}html,body{margin:0;height:100%;overflow:hidden;background:var(--nen);color:var(--chu);
font-family:system-ui,-apple-system,"Segoe UI",sans-serif}
#canh{position:fixed;inset:0}
.the{position:fixed;background:var(--the);border:1px solid var(--vien);border-radius:12px;box-shadow:0 6px 24px #0002;
backdrop-filter:blur(6px)}
#dau{top:12px;left:12px;padding:12px 14px;max-width:min(430px,calc(100vw - 24px))}
#dau h1{font-size:17px;margin:0 0 4px}#dau p{margin:0;font-size:12.5px;color:var(--phu);line-height:1.4}
#trangthai{margin-top:8px!important;font-weight:600;color:var(--chu)!important}
#dieukhien{bottom:12px;left:12px;padding:10px 12px;display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;
max-width:calc(100vw - 24px);font-size:12.5px}
button{font:inherit;font-size:12.5px;padding:6px 10px;border-radius:8px;border:1px solid var(--vien);background:transparent;
color:var(--chu);cursor:pointer}button:hover{border-color:var(--xanh)}
label{display:flex;align-items:center;gap:6px;color:var(--phu)}input[type=range]{width:110px}
#chugiai{top:12px;right:12px;padding:10px 12px;font-size:12px;line-height:1.7}
.o{display:inline-block;width:22px;height:6px;border-radius:3px;margin-right:6px;vertical-align:middle}
#bang{right:12px;top:172px;width:min(360px,calc(100vw - 24px));padding:14px 16px;display:none;max-height:calc(100vh - 230px);
overflow:auto}
#bang h2{margin:0 0 2px;font-size:17px}#bang .loai{font-size:12px;color:var(--phu);margin-bottom:10px}
#bang dl{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;margin:0 0 10px;font-size:13px}
#bang dt{color:var(--phu)}#bang dd{margin:0;font-weight:600}
#bang table{width:100%;border-collapse:collapse;font-size:12.5px;font-variant-numeric:tabular-nums}
#bang th,#bang td{padding:4px 6px;border-bottom:1px solid var(--vien);text-align:right}#bang th:first-child,#bang td:first-child{text-align:left}
#bang .ghichu{font-size:11.5px;color:var(--phu);margin-top:10px;line-height:1.45}
#dong{position:absolute;top:8px;right:10px;border:none;font-size:18px;padding:2px 6px}
#goiy{position:fixed;left:50%;top:14px;transform:translateX(-50%);font-size:13px;padding:6px 12px;display:none}
@media (max-width:700px){#chugiai{display:none}#bang{top:auto;bottom:120px}}
</style>
<script type="importmap">{"imports":{"three":"__THREE__/build/three.module.js","three/addons/":"__THREE__/examples/jsm/"}}</script>
</head><body>
<div id="canh"></div>
<div id="dau" class="the"><h1>What is under our feet?</h1>
<p>GPR survey of the campus road (10 m × 3.5 m). Ground = our top-view photo, rectified. Drag to orbit, scroll to zoom.</p>
<p id="trangthai">Loading…</p></div>
<div id="chugiai" class="the">
<div><span class="o" style="background:var(--xanh)"></span>Water pipe</div>
<div><span class="o" style="background:var(--cam)"></span>Power cable</div>
<div><span class="o" style="background:var(--xam)"></span>Unidentified reflector</div>
<div><span class="o" style="background:#f5c400"></span>GPR lines C1–C4</div>
<div><span class="o" style="background:#2fb84c"></span>GPR lines N1–N5</div>
<div style="color:var(--phu)">Click the pipe or cable for details</div></div>
<div id="goiy" class="the">Click the pipe or the cable to see its parameters</div>
<div id="bang" class="the"><button id="dong" aria-label="Close">×</button><div id="noidung"></div></div>
<div id="dieukhien" class="the">
<button id="phatlai">▶ Replay scan</button><button id="boqua">⏭ Skip</button><button id="tocdo">Speed 1×</button>
<button id="nhintren">Top view</button><button id="nhinduoi">Under-ground view</button>
<label>Ground <input id="dat" type="range" min="0" max="100" value="100"></label>
<label><input id="matcat" type="checkbox" checked> GPR sections</label>
<label><input id="xungquanh" type="checkbox" checked> Benches & walls</label>
</div>
<script type="module">
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const D = __DATA__;
const CX = 4.5, CY = 2.0;
// (x dọc đường, y ngang đường, z sâu) -> toạ độ three.js (Y hướng lên, giữ đúng chiều trái/phải)
const W = (x, y, z = 0) => new THREE.Vector3(x - CX, -z, -(y - CY));
const $ = (id) => document.getElementById(id);
const MAU = { ong_nuoc: 0x1c7ed6, cap: 0xe8590c, khac: 0x868e96 };
const TEN = { ong_nuoc: "Water pipe", cap: "Power cable", khac: "Unidentified reflector" };

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
$("canh").appendChild(renderer.domElement);
const scene = new THREE.Scene();
const toi = matchMedia("(prefers-color-scheme: dark)").matches && document.documentElement.dataset.theme !== "light";
scene.background = new THREE.Color(toi ? 0x16202b : 0xdfe9f3);
const camera = new THREE.PerspectiveCamera(45, innerWidth / innerHeight, 0.05, 200);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.target.set(0, -0.3, 0);
controls.maxDistance = 40;

scene.add(new THREE.HemisphereLight(0xffffff, 0x6b5a45, 1.1));
const nang = new THREE.DirectionalLight(0xfff4e0, 1.6);
nang.position.set(-6, 12, 5); nang.castShadow = true;
nang.shadow.mapSize.set(2048, 2048);
Object.assign(nang.shadow.camera, { left: -10, right: 10, top: 10, bottom: -10 });
scene.add(nang);

// ---------- chữ nổi (sprite) ----------
function nhan(chu, { mau = "#1d2733", nen = "rgba(255,255,255,0.92)", co = 46, cao = 0.22 } = {}) {
  const c = document.createElement("canvas"), g = c.getContext("2d");
  g.font = `bold ${co}px system-ui,sans-serif`;
  const w = Math.ceil(g.measureText(chu).width) + co, h = Math.ceil(co * 1.5);
  c.width = w; c.height = h;
  g.font = `bold ${co}px system-ui,sans-serif`;
  g.fillStyle = nen; g.beginPath(); g.roundRect(0, 0, w, h, h / 2); g.fill();
  g.fillStyle = mau; g.textBaseline = "middle"; g.fillText(chu, co / 2, h / 2 + 2);
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, depthTest: false, transparent: true }));
  s.scale.set(cao * w / h, cao, 1); s.renderOrder = 20;
  return s;
}

// ---------- mặt đất từ ảnh ----------
const [gx0, gx1, gy0, gy1] = D.vung_dat;
const texDat = new THREE.TextureLoader().load(D.anh_dat, () => { $("trangthai").textContent = "Ready"; });
texDat.colorSpace = THREE.SRGBColorSpace; texDat.anisotropy = renderer.capabilities.getMaxAnisotropy();
const vatDat = new THREE.MeshBasicMaterial({ map: texDat, transparent: true, opacity: 1 });  // ảnh đã có ánh sáng thật -> không chiếu sáng lại
const matDat = new THREE.Mesh(new THREE.PlaneGeometry(gx1 - gx0, gy1 - gy0), vatDat);
matDat.rotation.x = -Math.PI / 2;
matDat.position.copy(W((gx0 + gx1) / 2, (gy0 + gy1) / 2));
matDat.receiveShadow = true; matDat.renderOrder = 5;
scene.add(matDat);
function datDoMo(a) { vatDat.opacity = a; vatDat.depthWrite = a > 0.97; $("dat").value = Math.round(a * 100); }

// khối đất cắt lớp bên dưới khu khảo sát
const kd = { x0: -1.6, x1: 10.6, y0: -0.9, y1: 4.0 };
const khoiDat = new THREE.Group();
{
  const a = W(kd.x0, kd.y1, 0), b = W(kd.x1, kd.y0, D.z_max);
  const hop = new THREE.BoxGeometry(b.x - a.x, a.y - b.y, b.z - a.z);
  const m = new THREE.Mesh(hop, new THREE.MeshBasicMaterial({ color: 0x8a6a48, transparent: true, opacity: 0.12,
    side: THREE.BackSide, depthWrite: false }));
  m.position.set((a.x + b.x) / 2, (a.y + b.y) / 2, (a.z + b.z) / 2);
  khoiDat.add(m);
  const vien = new THREE.LineSegments(new THREE.EdgesGeometry(hop), new THREE.LineBasicMaterial({ color: 0x8a6a48 }));
  vien.position.copy(m.position); khoiDat.add(vien);
  for (let z = 0.25; z < D.z_max + 1e-6; z += 0.25) {  // vạch độ sâu ở mép khối
    const p = [W(kd.x0, kd.y0, z), W(kd.x0, kd.y1, z), W(kd.x1, kd.y1, z)];
    khoiDat.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(p),
      new THREE.LineBasicMaterial({ color: 0x8a6a48, transparent: true, opacity: 0.35 })));
    if (Math.abs(z * 2 - Math.round(z * 2)) < 1e-6) {
      const s = nhan(`${z.toFixed(1)} m`, { co: 40, cao: 0.16 }); s.position.copy(W(kd.x0 - 0.35, kd.y0, z)); khoiDat.add(s);
    }
  }
}
scene.add(khoiDat);

// ---------- xung quanh: tường, bảng tin, ghế đá, biển ----------
const xungQuanh = new THREE.Group();
const be = new THREE.MeshStandardMaterial({ color: 0xd9c2a0, roughness: 0.9, transparent: true, opacity: 0.55,
  depthWrite: false });  // tường mờ không được che mặt đất phía sau
function hop(x0, x1, y0, y1, z0, z1, vat) {  // z âm = trên mặt đất
  const a = W(x0, y1, z1), b = W(x1, y0, z0);
  const m = new THREE.Mesh(new THREE.BoxGeometry(b.x - a.x, b.y - a.y, b.z - a.z), vat);
  m.position.set((a.x + b.x) / 2, (a.y + b.y) / 2, (a.z + b.z) / 2); m.castShadow = true; m.receiveShadow = true;
  return m;
}
const tuong = [hop(-3, 11, -1.25, -0.85, -3.2, 0, be.clone()), hop(-3, 11, 5.6, 6.1, -3.6, 0, be.clone())];  // nhà hai bên
xungQuanh.add(...tuong);
{
  const c = document.createElement("canvas"); c.width = 1024; c.height = 300; const g = c.getContext("2d");
  g.fillStyle = "#f4f1e6"; g.fillRect(0, 0, 1024, 300); g.fillStyle = "#1f3f7a"; g.font = "bold 46px system-ui";
  g.fillText("CÁC NGÀNH ĐÀO TẠO", 40, 80); g.fillText("SAU ĐẠI HỌC", 40, 140);
  g.fillStyle = "#c8d84a"; for (let i = 0; i < 9; i++) g.fillRect(560 + (i % 3) * 140, 50 + Math.floor(i / 3) * 70, 120, 26);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  const bang = new THREE.Mesh(new THREE.PlaneGeometry(4.0, 1.15), new THREE.MeshStandardMaterial({ map: t }));
  bang.position.copy(W(2.6, 5.59, -1.7)); xungQuanh.add(bang);  // mặt bảng quay ra phía đường (+Z)
}
const da = new THREE.MeshStandardMaterial({ color: 0xc9ccce, roughness: 0.8 });
for (const x of D.ghe_x) for (const [y, quay] of [[4.62, 1], [5.08, -1]]) {
  const g = new THREE.Group();
  g.add(hop(x, x + 1.1, y - 0.19, y + 0.19, -0.45, -0.39, da));                       // mặt ghế
  g.add(hop(x, x + 1.1, y + 0.17 * quay - 0.03, y + 0.17 * quay + 0.03, -0.85, -0.45, da)); // lưng ghế
  for (const xc of [x + 0.12, x + 0.98]) g.add(hop(xc - 0.05, xc + 0.05, y - 0.15, y + 0.15, -0.39, 0, da));
  xungQuanh.add(g);
}
{
  const cot = hop(0.02, 0.08, 5.35, 5.41, -1.5, 0, new THREE.MeshStandardMaterial({ color: 0x555555 }));
  const bien = hop(-0.15, 0.25, 5.36, 5.40, -1.75, -1.45, new THREE.MeshStandardMaterial({ color: 0xf2f2f2 }));
  xungQuanh.add(cot, bien);
}
scene.add(xungQuanh);

// ---------- tuyến đo, mặt cắt radargram ----------
const tuyen = D.tuyen.map((t) => {
  const a = W(...t.p0), b = W(...t.p1), d = b.clone().sub(a), L = d.length(), goc = -Math.atan2(d.z, d.x);
  const mau = t.nhom === "doc_duong" ? 0xf5c400 : 0x2fb84c;
  const hinh = new THREE.PlaneGeometry(1, 0.06).rotateX(-Math.PI / 2).translate(0.5, 0, 0);
  const mo = new THREE.Mesh(hinh, new THREE.MeshBasicMaterial({ color: mau, transparent: true, opacity: 0.35, depthWrite: false }));
  const ro = new THREE.Mesh(hinh, new THREE.MeshBasicMaterial({ color: mau }));
  for (const m of [mo, ro]) { m.position.copy(a).setY(0.008); m.rotation.y = goc; m.renderOrder = 8; }
  mo.scale.x = L; ro.scale.x = 0.0001; mo.position.y = 0.006;
  const lb = nhan(t.ten, { mau: "#1d2733", nen: t.nhom === "doc_duong" ? "rgba(245,196,0,0.95)" : "rgba(47,184,76,0.95)" });
  lb.position.copy(a).add(d.clone().normalize().multiplyScalar(-0.35)).setY(0.25);
  const tex = new THREE.TextureLoader().load(t.anh); tex.colorSpace = THREE.SRGBColorSpace;
  const mc = new THREE.Mesh(new THREE.PlaneGeometry(L, D.z_max),
    new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false }));
  mc.position.copy(a.clone().add(b).multiplyScalar(0.5)).setY(-D.z_max / 2); mc.rotation.y = goc;
  scene.add(mo, ro, lb, mc);
  return { ...t, a, b, L, goc, ro, mc, hien: 0 };
});
let doMoMatCat = 0.85;  // sau khi lộ ống/cáp thì mặt cắt mờ đi để không che
function hienMatCat(t, a) { t.hien = a; t.mc.material.opacity = $("matcat").checked ? doMoMatCat * a : 0; t.mc.visible = $("matcat").checked && a > 0; }

// ---------- ống nước, cáp, dị vật ----------
const chonDuoc = [];
const doiTuong = D.doi_tuong.map((o) => {
  const g = { ...o, nhom: new THREE.Group(), diem3: [] };
  const mau = MAU[o.loai];
  if (o.quan_sat) {
    const r = o.loai === "ong_nuoc" ? 0.05 : 0.03;  // bán kính vẽ danh nghĩa (chưa đo được đường kính)
    const duong = new THREE.CatmullRomCurve3(o.quan_sat.map((p) => W(p[0], p[1], p[2] + r)));
    const hinh = new THREE.TubeGeometry(duong, 80, r, 20, false);
    let vat;
    if (o.loai === "ong_nuoc") {  // vân nước chảy dọc ống
      const c = document.createElement("canvas"); c.width = 64; c.height = 8; const x = c.getContext("2d");
      const gr = x.createLinearGradient(0, 0, 64, 0);
      gr.addColorStop(0, "#1c7ed6"); gr.addColorStop(0.5, "#8fd0ff"); gr.addColorStop(1, "#1c7ed6");
      x.fillStyle = gr; x.fillRect(0, 0, 64, 8);
      const t = new THREE.CanvasTexture(c); t.wrapS = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace;
      t.repeat.set(Math.max(2, duong.getLength() / 0.35), 1);
      vat = new THREE.MeshStandardMaterial({ map: t, emissive: mau, emissiveIntensity: 0.25, roughness: 0.35 });
      g.chay = t;
    } else vat = new THREE.MeshStandardMaterial({ color: mau, emissive: mau, emissiveIntensity: 0.4, roughness: 0.5 });
    g.ong = new THREE.Mesh(hinh, vat); g.ong.userData.dt = g; g.ong.castShadow = true;
    g.quang = new THREE.Mesh(new THREE.TubeGeometry(duong, 80, r * 1.9, 12, false),  // quầng sáng nhìn xuyên mặt cắt
      new THREE.MeshBasicMaterial({ color: mau, transparent: true, opacity: 0.32, depthTest: false, depthWrite: false,
        blending: THREE.AdditiveBlending }));
    g.quang.renderOrder = 15;
    g.nhom.add(g.ong, g.quang); chonDuoc.push(g.ong); moc(g, 0);
    for (const p of o.du_doan) {  // phần kéo dài: các đoạn nét đứt
      const a = W(p[0][0], p[0][1], p[0][2] + r), b = W(p[1][0], p[1][1], p[1][2] + r), L = a.distanceTo(b);
      for (let s = 0; s < L; s += 0.3) {
        const c1 = a.clone().lerp(b, s / L), c2 = a.clone().lerp(b, Math.min(s + 0.18, L) / L);
        const m = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.7, r * 0.7, c1.distanceTo(c2), 10),
          new THREE.MeshStandardMaterial({ color: mau, transparent: true, opacity: 0.45 }));
        m.position.copy(c1).add(c2).multiplyScalar(0.5);
        m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), c2.clone().sub(c1).normalize());
        m.visible = false; g.nhom.add(m); (g.dut ||= []).push(m);
      }
    }
  }
  for (const p of o.diem) {  // điểm đỉnh hyperbol + dây dọi chỉ độ sâu
    const vt = W(p.x, p.y, p.z);
    const cau = new THREE.Mesh(new THREE.SphereGeometry(o.loai === "khac" ? 0.06 : 0.045, 20, 14),
      new THREE.MeshStandardMaterial({ color: o.loai === "khac" ? mau : 0xffffff, emissive: mau, emissiveIntensity: 0.6 }));
    cau.position.copy(vt); cau.userData.dt = g; cau.visible = false; chonDuoc.push(cau);
    const doi = new THREE.Line(new THREE.BufferGeometry().setFromPoints([W(p.x, p.y, 0), vt]),
      new THREE.LineDashedMaterial({ color: mau, dashSize: 0.04, gapSize: 0.03, transparent: true, opacity: 0.9 }));
    doi.computeLineDistances(); doi.visible = false;
    const lb = nhan(`${p.z.toFixed(2)} m`, { mau: "#" + mau.toString(16).padStart(6, "0"), co: 40, cao: 0.15 });
    lb.position.copy(vt).add(new THREE.Vector3(0, 0.13, 0)); lb.visible = false;
    g.nhom.add(cau, doi, lb); g.diem3.push({ p, cau, doi, lb, no: 0 });
  }
  scene.add(g.nhom);
  return g;
});

function moc(g, f) {  // ống/cáp "mọc" dần theo tỉ lệ f (0..1)
  for (const m of [g.ong, g.quang]) {
    const buocTron = m.geometry.parameters.radialSegments * 6, n = m.geometry.index.count;
    m.geometry.setDrawRange(0, f >= 1 ? Infinity : Math.floor(n * f / buocTron) * buocTron);
  }
}

// ---------- máy GPR (xe đẩy) ----------
const may = new THREE.Group();
{
  const than = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.2, 0.42), new THREE.MeshStandardMaterial({ color: 0xd9480f }));
  than.position.y = 0.16; than.castShadow = true; may.add(than);
  const nap = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.04, 0.3), new THREE.MeshStandardMaterial({ color: 0x222831 }));
  nap.position.y = 0.28; may.add(nap);
  const banhVat = new THREE.MeshStandardMaterial({ color: 0x111111 });
  for (const [x, z] of [[-0.2, 0.23], [0.2, 0.23], [-0.2, -0.23], [0.2, -0.23]]) {
    const b = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.04, 16), banhVat);
    b.rotation.x = Math.PI / 2; b.position.set(x, 0.06, z); may.add(b);
  }
  const tay = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 1.0, 8), new THREE.MeshStandardMaterial({ color: 0x9aa4ad }));
  tay.position.set(-0.55, 0.55, 0); tay.rotation.z = Math.PI / 4.2; may.add(tay);
  const lb = nhan("GPR", { mau: "#ffffff", nen: "rgba(217,72,15,0.95)", co: 40, cao: 0.14 }); lb.position.y = 0.55; may.add(lb);
}
may.visible = false; scene.add(may);
const xung = [];  // sóng phát xuống đất
const hinhXung = new THREE.SphereGeometry(1, 28, 10, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2);
function phatXung(vt) {
  let s = xung.find((q) => !q.song);
  if (!s) {
    s = { m: new THREE.Mesh(hinhXung, new THREE.MeshBasicMaterial({ color: 0x4dabf7, transparent: true, opacity: 0.5,
      side: THREE.DoubleSide, depthWrite: false, wireframe: true })) };
    scene.add(s.m); xung.push(s);
  }
  s.song = true; s.tuoi = 0; s.m.position.copy(vt); s.m.visible = true;
}

// ---------- kịch bản animation ----------
let tocDo = 1, dung = false, kichBan = [], buoc = 0, tBuoc = 0, tXung = 0;
function lapKichBan() {
  kichBan = [{ loai: "bay", thoi: 2.8 }];
  let vt = null;
  for (const t of tuyen) {
    if (vt) kichBan.push({ loai: "di", a: vt, b: t.a, thoi: Math.max(0.4, vt.distanceTo(t.a) / 7) });
    kichBan.push({ loai: "quet", t, thoi: t.L / 3.2 });
    vt = t.b;
  }
  kichBan.push({ loai: "lo", thoi: 3.2 }, { loai: "xong", thoi: Infinity });
}
const camBatDau = new THREE.Vector3(-14, 16, 14), camMacDinh = new THREE.Vector3(-7.5, 6.5, 8.5);
const em = (x) => x < 0.5 ? 2 * x * x : 1 - (-2 * x + 2) ** 2 / 2;
function trangThai(chu) { $("trangthai").textContent = chu; }
function batDau() {
  lapKichBan(); buoc = 0; tBuoc = 0; doMoMatCat = 0.85;
  datDoMo(1); may.visible = false;
  for (const t of tuyen) { t.ro.scale.x = 0.0001; hienMatCat(t, 0); }
  for (const g of doiTuong) {
    if (g.ong) moc(g, 0);
    (g.dut || []).forEach((m) => (m.visible = false));
    g.diem3.forEach((d) => { d.cau.visible = d.doi.visible = d.lb.visible = false; d.no = 0; });
  }
  $("bang").style.display = "none";
}
function hienDiemGan(t, f) {  // máy đã quét qua điểm phát hiện (theo quãng đường, không sót khi chạy nhanh) -> hiện điểm
  const huong = t.b.clone().sub(t.a).normalize();
  for (const g of doiTuong) for (const d of g.diem3) {
    if (d.p.tuyen.replace("_lap", "") !== t.ten || d.cau.visible) continue;
    if (W(d.p.x, d.p.y).sub(t.a).dot(huong) <= t.L * f) { d.cau.visible = d.doi.visible = d.lb.visible = true; d.no = 1; }
  }
}
function ketThuc() {  // trạng thái cuối: mọi thứ hiện đủ
  may.visible = false; datDoMo(0.45); doMoMatCat = 0.35;
  for (const t of tuyen) { t.ro.scale.x = t.L; hienMatCat(t, 1); }
  for (const g of doiTuong) {
    if (g.ong) moc(g, 1);
    (g.dut || []).forEach((m) => (m.visible = true));
    g.diem3.forEach((d) => { d.cau.visible = d.doi.visible = d.lb.visible = true; });
  }
  buoc = kichBan.length - 1;
  trangThai("Done – a power cable crosses the road, a water pipe runs along it.");
  $("goiy").style.display = "block"; setTimeout(() => ($("goiy").style.display = "none"), 6000);
}
function chay(dt) {
  if (dung || buoc >= kichBan.length) return;
  const k = kichBan[buoc];
  tBuoc += dt * (k.loai === "bay" ? 1 : tocDo);
  const f = Math.min(1, tBuoc / k.thoi);
  if (k.loai === "bay") {
    camera.position.lerpVectors(camBatDau, camMacDinh, em(f)); trangThai("Our campus road – no drawing of what is underneath");
  } else if (k.loai === "di") {
    may.visible = true; may.position.lerpVectors(k.a, k.b, f);
  } else if (k.loai === "quet") {
    const t = k.t; may.visible = true; may.position.lerpVectors(t.a, t.b, f); may.rotation.y = t.goc;
    t.ro.scale.x = Math.max(0.0001, t.L * f); datDoMo(0.7);
    trangThai(`Scanning line ${t.ten} (${t.dai.toFixed(1)} m)…`);
    tXung += dt * tocDo; if (tXung > 0.16) { tXung = 0; phatXung(may.position.clone()); }
    hienDiemGan(t, f);
    if (f >= 1) hienMatCat(t, 1); else if (f > 0.05) hienMatCat(t, Math.min(1, t.hien + dt));
  } else if (k.loai === "lo") {
    may.visible = false; datDoMo(0.7 - 0.25 * em(f));
    trangThai("Connecting the hyperbola apexes → pipe and cable");
    doMoMatCat = 0.85 - 0.5 * em(f); tuyen.forEach((t) => hienMatCat(t, t.hien));
    for (const g of doiTuong) if (g.ong) moc(g, em(f));
  }
  if (f >= 1 && k.loai !== "xong") { buoc++; tBuoc = 0; if (kichBan[buoc].loai === "xong") ketThuc(); }
}

// ---------- bấm chọn -> bảng thông số ----------
const tia = new THREE.Raycaster(), chuot = new THREE.Vector2();
let dangChon = null, xuongLuc = null;
function chon(g) {
  for (const o of doiTuong) if (o.ong) o.ong.material.emissiveIntensity = o === g ? 0.9 : (o.loai === "ong_nuoc" ? 0.25 : 0.4);
  dangChon = g; if (!g) { $("bang").style.display = "none"; return; }
  const z = g.diem.map((p) => p.z), tb = z.reduce((a, b) => a + b, 0) / z.length;
  const tuyenTen = [...new Set(g.diem.map((p) => p.tuyen.replace("_lap", " (repeat)")))].sort((a, b) => a.localeCompare(b)).join(", ");
  const huong = g.huong == null ? "–" : (g.loai === "ong_nuoc" ? "Along the road" : "Across the road") + ` (${g.huong}° to road axis)`;
  let h = `<h2 style="color:#${MAU[g.loai].toString(16).padStart(6, "0")}">${TEN[g.loai]}</h2>`;
  h += `<div class="loai">${g.loai === "khac" ? "Seen on one GPR line only – not identified" : "Interpreted from GPR hyperbolas"}</div><dl>`;
  h += `<dt>Detected on</dt><dd>${tuyenTen}</dd><dt>Direction</dt><dd>${huong}</dd>`;
  if (g.dai_do) {
    const q = g.quan_sat;
    h += `<dt>Measured length</dt><dd>${g.dai_do.toFixed(2)} m (x ${q[0][0].toFixed(1)}→${q[q.length - 1][0].toFixed(1)} m, y ${q[0][1].toFixed(1)}→${q[q.length - 1][1].toFixed(1)} m)</dd>`;
  }
  h += `<dt>Depth to top</dt><dd>${Math.min(...z).toFixed(2)}–${Math.max(...z).toFixed(2)} m (mean ${tb.toFixed(2)} m)</dd>`;
  h += `<dt>Wave velocity</dt><dd>${D.van_toc}</dd>`;
  h += `<dt>Depth formula</dt><dd>${D.cong_thuc}</dd></dl>`;
  h += `<table><tr><th>Line</th><th>Antenna</th><th>x (m)</th><th>y (m)</th><th>t₀ (ns)</th><th>Depth (m)</th></tr>`;
  for (const p of g.diem) h += `<tr><td>${p.tuyen.replace("_lap", " rep.")}</td><td>${p.kenh}</td><td>${p.x.toFixed(2)}</td><td>${p.y.toFixed(2)}</td><td>${p.t.toFixed(1)}</td><td>${p.z.toFixed(2)}</td></tr>`;
  h += `</table><div class="ghichu">${g.loai === "ong_nuoc" ? "Diameter not measured: after migration the pipe hyperbola does not focus, so the tube is drawn at a nominal 10 cm." :
    g.loai === "cap" ? "Cable drawn at a nominal 5 cm diameter (true size below GPR resolution, λ/4 ≈ 9.5 cm at 250 MHz)." :
    "Strong single hyperbola; more lines are needed to tell its shape and direction."}
    Depth uncertainty: up to ~30 % depending on the velocity model. Dashed parts are straight extensions, not measured.</div>`;
  $("noidung").innerHTML = h; $("bang").style.display = "block";
}
function viTriChuot(e) {
  const r = renderer.domElement.getBoundingClientRect();
  chuot.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
}
function trung() { tia.setFromCamera(chuot, camera); const h = tia.intersectObjects(chonDuoc.filter((o) => o.visible && (!o.geometry.drawRange || o.geometry.drawRange.count > 0)), false); return h[0]?.object.userData.dt; }
renderer.domElement.addEventListener("pointerdown", (e) => (xuongLuc = [e.clientX, e.clientY]));
renderer.domElement.addEventListener("pointerup", (e) => {
  if (!xuongLuc || Math.hypot(e.clientX - xuongLuc[0], e.clientY - xuongLuc[1]) > 5) return;  // kéo xoay thì không tính là bấm
  viTriChuot(e); chon(trung() || null);
});
renderer.domElement.addEventListener("pointermove", (e) => { viTriChuot(e); renderer.domElement.style.cursor = trung() ? "pointer" : "grab"; });

// ---------- điều khiển ----------
$("dong").onclick = () => chon(null);
$("phatlai").onclick = () => { dung = false; $("phatlai").textContent = "▶ Replay scan"; batDau(); };
$("boqua").onclick = () => ketThuc();
$("tocdo").onclick = () => { tocDo = tocDo === 1 ? 2 : tocDo === 2 ? 4 : 1; $("tocdo").textContent = `Speed ${tocDo}×`; };
$("dat").oninput = (e) => datDoMo(e.target.value / 100);
$("matcat").onchange = () => tuyen.forEach((t) => hienMatCat(t, t.hien));
$("xungquanh").onchange = (e) => (xungQuanh.visible = e.target.checked);
function bayToi(vt, dich) { const a = camera.position.clone(), b = controls.target.clone(); let f = 0;
  const id = setInterval(() => { f = Math.min(1, f + 0.04); camera.position.lerpVectors(a, vt, em(f)); controls.target.lerpVectors(b, dich, em(f)); if (f >= 1) clearInterval(id); }, 16); }
$("nhintren").onclick = () => bayToi(new THREE.Vector3(0.01, 15, 0.6), new THREE.Vector3(0, 0, 0));
$("nhinduoi").onclick = () => { datDoMo(0.25); bayToi(new THREE.Vector3(-6, -1.8, 5.5), new THREE.Vector3(-0.5, -0.45, 0)); };
addEventListener("resize", () => { camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); renderer.setSize(innerWidth, innerHeight); });

window.__canh = { scene, camera, doiTuong, tuyen, khoiDat, matDat, xungQuanh, vatDat };  // để kiểm tra từ console
// ---------- vòng lặp ----------
camera.position.copy(camBatDau); camera.lookAt(controls.target);
batDau();
const dongHo = new THREE.Clock();
renderer.setAnimationLoop(() => {
  const dt = Math.min(dongHo.getDelta(), 0.05), t = dongHo.elapsedTime;
  chay(dt);
  for (const s of xung) if (s.song) {
    s.tuoi += dt * 1.3; const r = 0.05 + s.tuoi * 1.1; s.m.scale.set(r, r, r);
    s.m.material.opacity = 0.5 * (1 - s.tuoi); if (s.tuoi >= 1) { s.song = false; s.m.visible = false; }
  }
  for (const g of doiTuong) {
    if (g.chay) g.chay.offset.x -= dt * 0.6;                                   // nước chảy
    if (g.loai === "cap" && g.ong && g !== dangChon) g.ong.material.emissiveIntensity = 0.35 + 0.3 * Math.sin(t * 4); // xung điện
    for (const d of g.diem3) if (d.no > 0) { d.no = Math.max(0, d.no - dt * 2); d.cau.scale.setScalar(1 + 1.5 * d.no); }
  }
  for (const m of tuong) {  // tường nằm giữa camera và khu khảo sát thì mờ đi
    const giua = Math.sign(m.position.z) === Math.sign(camera.position.z) && Math.abs(camera.position.z) > Math.abs(m.position.z) - 0.3;
    m.material.opacity += ((giua ? 0.06 : 0.55) - m.material.opacity) * 0.15;
  }
  controls.enabled = !(buoc === 0 && kichBan[0]?.loai === "bay");
  controls.update();
  renderer.render(scene, camera);
});
</script></body></html>"""
