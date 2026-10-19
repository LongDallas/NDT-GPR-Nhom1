// One slide (English, HCMUS academic theme): four P1 anomalies on parallel lines C1–C4 line up straight across the road → cable path.
// Data: 03_DuLieuHienTruong/New Data/ (LZZ2000x .T files, 250 MHz); P1 picks from GPR_chu_thich_duong_ong.pdf.
// Figures first: python3 _build/ve_cap_4_di_thuong.py
// Usage: node _build/slide_cap_4_di_thuong.js Slide_Cap_4DiThuong.pptx
const path = require("path");
const pptxgen = require("pptxgenjs");

const out = process.argv[2] || "Slide_Cap_4DiThuong.pptx";
const img = (f) => path.join(__dirname, "..", "HinhAnh", f);
const C = { blue: "0B4A9E", card: "EEF3FA", ink: "1B1B1D", grey: "5F6368", cable: "E8590C" };
const T = (o) => Object.assign({ isTextBox: true, margin: 0, fontFace: "Arial", valign: "top" }, o);

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "Four anomalies trace the buried cable";
pres.theme = { headFontFace: "Arial", bodyFontFace: "Arial" };
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 11.0, h: 0.8, fontFace: "Arial", fontSize: 28, bold: true, color: C.blue, valign: "middle", align: "left", margin: 0 }, text: "" } },
    { image: { path: img("Logo_HCMUS.png"), x: 12.05, y: 0.33, w: 0.73, h: 0.6 } },
    { text: { text: "GPR for underground cables and utilities · HCMUS", options: { x: 0.6, y: 7.02, w: 7, h: 0.28, fontFace: "Arial", fontSize: 10, color: C.grey, margin: 0 } } },
  ],
  slideNumber: { x: 12.2, y: 7.02, w: 0.5, h: 0.28, fontFace: "Arial", fontSize: 10, color: C.grey, align: "right" },
});

const s = pres.addSlide({ masterName: "CONTENT" });
s.addText("Four aligned anomalies trace one buried cable", { placeholder: "title" });

s.addImage({
  path: img("Cap_4DiThuong_C1C4.png"), x: 0.6, y: 1.3, w: 6.34, h: 5.25,
  altText: "Radargrams of parallel lines C1, C2, C3 and C4 (250 MHz) drawn on the same position axis. Anomaly P1 sits at 2.5 m along the road on every line, at depths 0.65, 0.45, 0.46 and 0.43 m; a dashed orange vertical line joins the four hyperbola apexes.",
});
s.addText("Plan view", T({ x: 7.95, y: 1.3, w: 4.75, h: 0.35, fontSize: 14, bold: true, color: C.grey }));
s.addImage({
  path: img("Cap_MatBang_C1C4.png"), x: 8.2, y: 1.7, w: 3.9, h: 2.39,
  altText: "Plan view: lines C1 to C4 run parallel 1 m apart, C2 and C4 walked in the opposite direction; the four P1 points fall on one dashed orange line straight across the road, the cable.",
});
[
  { num: "4 / 4", head: "Same echo on every line", sub: "strong, ringing hyperbola → metal" },
  { num: "90°", head: "Straight across the road", sub: "C1, C3 at 2.50 m · field marks agree" },
  { num: "≈ 0.45 m", head: "Depth to the top", sub: "C2–C4: 0.43–0.46 m · C1: 0.65 m" },
].forEach((r, i) => {
  const x = 7.95, y = 4.2 + i * 0.82, w = 4.75, h = 0.72;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: C.card }, line: { color: C.card, width: 0 } });
  s.addText(r.num, T({ x: x + 0.2, y, w: 1.6, h, fontSize: 22, bold: true, color: C.cable, valign: "middle" }));
  s.addText(r.head, T({ x: x + 1.9, y: y + 0.08, w: 2.75, h: 0.3, fontSize: 15, bold: true, color: C.ink }));
  s.addText(r.sub, T({ x: x + 1.9, y: y + 0.4, w: 2.75, h: 0.28, fontSize: 11.5, color: C.grey }));
});
s.addText("250 MHz, lines C1–C4 (LZZ20001–20004; C3 = LZZ20003.11 flipped back), team picks. Depth: 0.12 m/ns concrete, 0.10 m/ns soil. C2, C4 walked in reverse, placed from the cable marked on site.",
  T({ x: 0.6, y: 6.68, w: 12.1, h: 0.3, fontSize: 10, color: C.grey }));

s.addNotes(`[~40 s] One hyperbola alone could be anything — a stone, a pocket of fill. So we look for the same echo on neighbouring lines.
[left, top to bottom] Lines C1 to C4 run parallel, one metre apart, drawn on the same position axis. On every line we find the same anomaly, P1 — a strong hyperbola with a long ringing tail, typical of metal.
[dashed line] The four tops sit in one column, at 2.5 m: the cable crosses the road straight, at a right angle. That is also what we saw on site — each time we hit the anomaly we marked the ground, and the marks lined up straight across the road.
[cards] Depth to the top is about 0.45 m on C2 to C4, and a little deeper on C1, 0.65 m.
(If asked: C2 and C4 were walked in the opposite direction. We flipped them, as the team did in ReflexW, and placed their start so that P1 sits on the cable we marked. C1 and C3, walked forward, already agree at 2.50 m on their own.)`);

pres.writeFile({ fileName: out }).then((f) => console.log("wrote", f));
