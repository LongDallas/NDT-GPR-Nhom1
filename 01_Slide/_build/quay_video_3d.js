// Quay cảnh 3D (02_SoDoTuyen_BanDo/ket_qua/Canh3D_HienTruong.html) thành video MP4 để chèn vào slide.
// Dùng "thời gian ảo": mỗi khung hình đồng hồ của trang chỉ tiến đúng 1/FPS giây rồi mới chụp,
// nên video mượt và đúng nhịp như animation thật dù máy render chậm.
// Cần: npm i playwright-core; ffmpeg (brew install ffmpeg); Chrome for Testing (đường dẫn CHROME bên dưới).
// Chạy: node quay_video_3d.js <canh.html> <ra.mp4> [fps=30] [giu_cuoi_giay=4]   -> video animation
//       node quay_video_3d.js <canh.html> <ra.gif>                           -> GIF xoay 360° quanh cảnh cuối (mặt đất mờ)
const { chromium } = require("playwright-core");
const { spawn } = require("child_process");
const { pathToFileURL } = require("url");
const os = require("os");

const [html, out, fpsArg, holdArg] = process.argv.slice(2);
const FPS = Number(fpsArg || 30), HOLD = Number(holdArg || 4), MAX_S = 120;
const CHROME = process.env.CHROME || `${os.homedir()}/Library/Caches/ms-playwright/chromium-1248/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing`;

// Thay đồng hồ của trang: performance.now, Date.now, requestAnimationFrame, setTimeout/setInterval
const VIRTUAL_TIME = `(() => {
  let now = 0; const t0 = Date.now(); const raf = []; let rid = 0;
  const timers = []; const cleared = new Set(); let tid = 0;
  performance.now = () => now; Date.now = () => t0 + now;
  window.requestAnimationFrame = (cb) => { raf.push([++rid, cb]); return rid; };
  window.cancelAnimationFrame = (i) => { const k = raf.findIndex((e) => e[0] === i); if (k >= 0) raf.splice(k, 1); };
  window.setTimeout = (fn, ms = 0, ...a) => { const id = ++tid; timers.push({ id, t: now + ms, fn: () => fn(...a) }); return id; };
  window.setInterval = (fn, ms = 0, ...a) => { const id = ++tid; const o = { id, t: now + ms, fn: () => { fn(...a); if (!cleared.has(id)) { o.t += Math.max(ms, 1); timers.push(o); } } }; timers.push(o); return id; };
  window.clearTimeout = window.clearInterval = (i) => { cleared.add(i); const k = timers.findIndex((e) => e.id === i); if (k >= 0) timers.splice(k, 1); };
  window.__step = (ms) => {
    now += ms;
    for (;;) { timers.sort((a, b) => a.t - b.t); if (!timers.length || timers[0].t > now) break; timers.shift().fn(); }
    for (const [, cb] of raf.splice(0)) cb(now);
  };
})();`;

// Video không bấm được: ẩn nút điều khiển và các lời nhắc "kéo / bấm"
const VIDEO_CSS = `#dieukhien, #goiy, #bang, #chugiai div:last-child { display: none !important; }`;

// GIF xoay vòng: GIAY giây cho một vòng, GIF_FPS khung/giây, camera cách tâm R (m), cao CAO (m)
const GIF = { GIAY: 10, GIF_FPS: 10, R: 6.2, CAO: 2.6, DO_MO_DAT: 0.3, RONG: 720, MAU: 96 };

async function quayVong(page, out) {
  await page.addStyleTag({ content: ".the { display: none !important; }" });  // GIF sạch, chữ để trên slide
  await page.evaluate((doMo) => {
    document.getElementById("boqua").click();                                   // nhảy tới cảnh cuối
    const dat = document.getElementById("dat");
    dat.value = String(Math.round(doMo * 100)); dat.dispatchEvent(new Event("input"));
    const mc = document.getElementById("matcat");
    mc.checked = false; mc.dispatchEvent(new Event("change"));                 // ẩn mặt cắt radargram cho thấy rõ ống
    const xq = document.getElementById("xungquanh");
    xq.checked = false; xq.dispatchEvent(new Event("change"));                 // ẩn ghế đá, tường để không che ống
  }, GIF.DO_MO_DAT);
  // tâm xoay = giữa khối bao của ống nước và cáp
  const tam = await page.evaluate(() => {
    const { doiTuong, controls } = window.__canh;
    const T = controls.target.constructor, box = { min: [1e9, 1e9, 1e9], max: [-1e9, -1e9, -1e9] };
    for (const g of doiTuong) if (g.ong) {
      g.ong.geometry.computeBoundingBox(); g.ong.updateMatrixWorld();
      const b = g.ong.geometry.boundingBox.clone().applyMatrix4(g.ong.matrixWorld);
      ["x", "y", "z"].forEach((k, i) => { box.min[i] = Math.min(box.min[i], b.min[k]); box.max[i] = Math.max(box.max[i], b.max[k]); });
    }
    const c = box.min.map((v, i) => (v + box.max[i]) / 2);
    controls.target.copy(new T(c[0], c[1], c[2]));
    return c;
  });
  console.log("  tâm xoay:", tam.map((v) => v.toFixed(2)).join(", "));
  for (let i = 0; i < 30; i++) await page.evaluate(() => window.__step(1000 / 30));
  const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(GIF.GIF_FPS), "-c:v", "png", "-i", "-",
    "-vf", `scale=${GIF.RONG}:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=${GIF.MAU}:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle`,
    "-loop", "0", out], { stdio: ["pipe", "inherit", "inherit"] });
  const n = GIF.GIAY * GIF.GIF_FPS, goc0 = Math.atan2(8.5, -7.5);
  for (let i = 0; i < n; i++) {
    const a = goc0 + (2 * Math.PI * i) / n;
    await page.evaluate(([x, y, z]) => window.__canh.camera.position.set(x, y, z),
      [tam[0] + GIF.R * Math.cos(a), tam[1] + GIF.CAO, tam[2] + GIF.R * Math.sin(a)]);
    for (let k = 0; k < 30 / GIF.GIF_FPS; k++) await page.evaluate(() => window.__step(1000 / 30));
    const png = await page.screenshot({ type: "png" });
    if (!ff.stdin.write(png)) await new Promise((r) => ff.stdin.once("drain", r));
  }
  ff.stdin.end();
  await new Promise((r) => ff.on("close", r));
  console.log("Đã lưu", out, `(${n} khung, ${GIF.GIAY} s một vòng)`);
}

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, args: ["--ignore-gpu-blocklist", "--use-angle=metal", "--enable-gpu-rasterization"] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1.5 });
  await page.addInitScript(VIRTUAL_TIME);
  let trang = html;
  if (out.endsWith(".gif")) {  // GIF cần điều khiển tâm xoay: dùng bản sao HTML có `controls` trong window.__canh (file gốc giữ nguyên)
    const fs = require("fs"), path = require("path");
    const goc = fs.readFileSync(html, "utf8");
    if (!goc.includes("window.__canh = { scene,")) throw new Error("Không tìm thấy window.__canh trong HTML");
    trang = path.join(os.tmpdir(), "canh3d_gif.html");
    fs.writeFileSync(trang, goc.replace("window.__canh = { scene,", "window.__canh = { controls, scene,"));
  }
  await page.goto(pathToFileURL(trang).href);
  await page.waitForFunction(() => window.__canh, null, { timeout: 60000 });
  await page.addStyleTag({ content: VIDEO_CSS });
  await page.evaluate(() => {
    const p = document.querySelector("#dau p");
    if (p && p.id !== "trangthai") p.textContent = "GPR survey of the campus road (10 m × 3.5 m). Ground = our top-view photo, rectified.";
  });
  await page.waitForTimeout(2500);  // chờ ảnh nền / texture giải mã xong (thời gian thật)

  if (out.endsWith(".gif")) {  // chế độ GIF: cảnh cuối, mặt đất mờ, camera xoay 360° quanh khu khảo sát
    await quayVong(page, out);
    await browser.close();
    return;
  }

  const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "png", "-i", "-",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "slow", "-crf", "18", "-movflags", "+faststart", out], { stdio: ["pipe", "inherit", "inherit"] });
  let doneAt = null;
  for (let f = 0; f < MAX_S * FPS; f++) {
    await page.evaluate((ms) => window.__step(ms), 1000 / FPS);
    const png = await page.screenshot({ type: "png" });
    if (!ff.stdin.write(png)) await new Promise((r) => ff.stdin.once("drain", r));
    if (doneAt === null && (await page.textContent("#trangthai")).startsWith("Done")) doneAt = f;
    if (doneAt !== null && f - doneAt >= HOLD * FPS) break;
    if (f % (5 * FPS) === 0) console.log(`  ${(f / FPS).toFixed(0)} s: ${await page.textContent("#trangthai")}`);
  }
  ff.stdin.end();
  await new Promise((r) => ff.on("close", r));
  await browser.close();
  console.log("Đã lưu", out, doneAt === null ? "(chưa tới cảnh cuối – tăng MAX_S)" : `(${((doneAt + HOLD * FPS) / FPS).toFixed(1)} s)`);
})();
