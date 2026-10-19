// Seminar deck (English), academic seminar structure: 16 slides (~10:00) + 4 backup slides.
// Slide 1 keeps the storytelling hook (Kaohsiung 2014 → our courtyard). From slide 2 on the talk follows the
// structure required by the course (00_QuanLy/YeuCau_Seminar_MonHoc.md): Introduction → Overview →
// Methods → Results → Conclusions → References, with an outline slide and a section navigator on every slide.
// v3: sections 1 (Introduction) and 2 (Overview), slides 3–5, follow §1 of the written report (06_BaoCao/BaoCao_GPR_Nhom1.pdf);
// every other slide is identical to v2 (tao_seminar.js).
// Usage: node tao_seminar_v3.js <out.pptx> [storyboard]
//   storyboard: slide 1 is written as 4 separate frames (one per click) for previewing.
// After building the real deck, run: python3 them_hieu_ung.py <out.pptx>  (click fades on slide 1, video autoplay)
// Figures: same sources as tao_bai_trinh_bay.js (see README_CauTruc_10phut.md).
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const [out, mode] = process.argv.slice(2);
const STORY = mode === "storyboard";
const IMG = path.join(__dirname, "..", "HinhAnh");
const img = (f) => path.join(IMG, f);
const grad = (f) => path.join(__dirname, f);

const TEAM = ["Quốc Long", "Quốc Tài", "Thành Trung", "Đăng Khoa", "Đăng Quang"];
const GROUP = "Group 1";
const SUPERVISOR = "Supervisor: MSc. Nguyễn Văn Thuận";

const C = {
  // HCMUS academic theme
  blue: "0B4A9E", gold: "C9A227", goldLight: "F2C94C", card: "EEF3FA", ink: "1B1B1D", grey: "5F6368", paleBlue: "D6E2F3", navOff: "9AA0A6",
  // storytelling opening
  night: "0A0A0B", red: "E5482D", paper: "F4F1EC", mute: "9A9A9A", dim: "6E6E6E",
  // data colours used in the figures
  pipe: "1E7BD9", cable: "E8590C",
};
const W = 13.333, H = 7.5;
const T = (o) => Object.assign({ isTextBox: true, margin: 0, fontFace: "Arial", valign: "top" }, o);
const EQ = "Cambria";
const TALK = "Talk (10 min)";
const SECTIONS = ["Introduction", "Overview", "Methods", "Results", "Conclusions"];

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "Application of GPR in Surveying Underground Cables and Utilities";
pres.theme = { headFontFace: "Arial", bodyFontFace: "Arial" };

pres.defineSlideMaster({ title: "DARK", background: { color: C.night }, objects: [] });
pres.defineSlideMaster({ title: "PLAIN", background: { color: "FFFFFF" }, objects: [] });
pres.defineSlideMaster({
  title: "SEMINAR",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.55, w: 11.2, h: 0.75, fontFace: "Arial", fontSize: 26, bold: true, color: C.blue, valign: "middle", align: "left", margin: 0 }, text: "" } },
    { image: { path: img("Logo_HCMUS.png"), x: 12.05, y: 0.3, w: 0.73, h: 0.6 } },
    { text: { text: `${GROUP} · GPR for underground cables and utilities · Non-Destructive Testing Methods – HCMUS`, options: { x: 0.6, y: 7.02, w: 9, h: 0.28, fontFace: "Arial", fontSize: 10, color: C.grey, margin: 0 } } },
  ],
  slideNumber: { x: 12.2, y: 7.02, w: 0.5, h: 0.28, fontFace: "Arial", fontSize: 10, color: C.grey, align: "right" },
});

// Section navigator (Beamer-style): the current section in bold blue, the others grey.
const nav = (s, cur) => {
  const runs = [];
  SECTIONS.forEach((name, i) => {
    const on = i === cur;
    runs.push({ text: `${i + 1}  ${name}`, options: { bold: on, color: on ? C.blue : C.navOff } });
    if (i < SECTIONS.length - 1) runs.push({ text: "      ", options: { color: C.navOff } });
  });
  s.addText(runs, T({ objectName: "nav", x: 0.6, y: 0.2, w: 11.2, h: 0.28, fontSize: 11 }));
};
const seminar = (sec, title, section = TALK) => {
  const s = pres.addSlide({ masterName: "SEMINAR", sectionTitle: section });
  if (sec !== null) nav(s, sec);
  s.addText(title, { placeholder: "title" });
  return s;
};
const card = (s, x, y, w, h, color = C.card) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color }, line: { color, width: 0 } });
const source = (s, text) => s.addText(text, T({ x: 0.6, y: 6.72, w: 12.1, h: 0.26, fontSize: 10, color: C.grey }));
const numDot = (s, x, y, d, label, color = C.blue, fontSize = 16) => {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color }, line: { color, width: 0 } });
  s.addText(String(label), T({ x, y, w: d, h: d, fontSize, bold: true, color: "FFFFFF", align: "center", valign: "middle" }));
};
const bullets = (items, o = {}) => items.map((t, i) => ({ text: t, options: Object.assign({ bullet: { indent: 14 }, breakLine: i < items.length - 1 }, o) }));

// ================================================================ 1. Hook (storytelling, 4 layers; fades added by them_hieu_ung.py)
const NOTES1 = `[0:00–1:00] [Black screen. Stand still, look at the audience, 2 seconds of silence.]

July 31st, 2014. Kaohsiung, Taiwan.
Late in the evening, people on the street begin to smell gas.
Firefighters arrive. They search for the leak — for almost three hours.
They cannot find it. [pause 1 s]

[CLICK 1] Just before midnight, the street explodes.
Thirty-two people dead. Three hundred and twenty-one injured.
The cause? A leaking pipe — buried right under their feet — that nobody could see.

[CLICK 2] And this is not rare. In the US alone, buried utilities are hit more than half a million times a year.
Here in Ho Chi Minh City, newspapers put it simply: dig up any street, and you hit a spider web.

[CLICK 3] Now look at this. Our own campus. We walk across it every day.
Under this asphalt there is a water pipe and a power cable — and no drawing of where they are.
If someone digs here tomorrow… where is it safe?

Today, we will answer that — without digging a single hole.
[One sentence: "We are Quốc Long, Quốc Tài, Thành Trung, Đăng Khoa and Đăng Quang — and this is our seminar on GPR for underground cables and utilities."]

CHECK BEFORE PRESENTING: confirm the timeline (~20:46 gas reports, explosions ~23:57) on Wikipedia "2014 Kaohsiung gas explosions".`;

const hookLayers = [
  (s) => {
    s.addText("31 JULY 2014", T({ objectName: "L0_date", x: 0.9, y: 2.55, w: 11.5, h: 1.2, fontSize: 66, bold: true, color: C.paper, charSpacing: 6 }));
    s.addText("Kaohsiung, Taiwan", T({ objectName: "L0_place", x: 0.9, y: 3.8, w: 11.5, h: 0.7, fontSize: 28, color: C.mute }));
  },
  (s) => {
    s.addImage({ objectName: "L1_photo", path: img("Slide1_Kaohsiung_2014.jpg"), x: 0, y: 0, w: W, h: H, altText: "Sanduo 1st Road in Kaohsiung torn open after the 2014 gas explosions, with exposed pipes" });
    s.addImage({ objectName: "L1_shade", path: grad("grad_left.png"), x: 0, y: 0, w: W, h: H, altText: "" });
    s.addText("32 dead", T({ objectName: "L1_dead", x: 0.8, y: 1.7, w: 6.5, h: 1.5, fontSize: 96, bold: true, color: C.red }));
    s.addText("321 injured", T({ objectName: "L1_injured", x: 0.8, y: 3.25, w: 6.5, h: 0.9, fontSize: 44, bold: true, color: C.paper }));
    s.addText([
      { text: "A leaking pipe under the street.", options: { breakLine: true } },
      { text: "Nobody could see it." },
    ], T({ objectName: "L1_cause", x: 0.8, y: 4.45, w: 6.0, h: 1.0, fontSize: 22, italic: true, color: C.paper }));
    s.addText([
      { text: "Sanduo 1st Rd, Kaohsiung, 11 Aug 2014 · Photo: " },
      { text: "玄史生", options: { fontFace: "PingFang TC" } },
      { text: " / Wikimedia Commons · CC BY-SA 4.0" },
    ], T({ objectName: "L1_credit", x: 5.8, y: 7.05, w: 7.2, h: 0.3, fontSize: 10, color: "D0D0D0", align: "right" }));
  },
  (s) => {
    s.addShape(pres.shapes.RECTANGLE, { objectName: "L2_bg", x: 0, y: 0, w: W, h: H, fill: { color: C.night }, line: { color: C.night, width: 0 } });
    s.addText("And this is not rare.", T({ objectName: "L2_lead", x: 0.9, y: 0.75, w: 11.5, h: 0.5, fontSize: 22, color: C.mute }));
    s.addText("500,000+", T({ objectName: "L2_n1", x: 0.9, y: 1.45, w: 6.0, h: 1.4, fontSize: 80, bold: true, color: C.paper }));
    s.addText("buried utilities hit by digging each year (US)", T({ objectName: "L2_n1lab", x: 0.9, y: 2.9, w: 5.6, h: 0.8, fontSize: 18, color: C.mute }));
    s.addText("$30B", T({ objectName: "L2_n2", x: 7.3, y: 1.45, w: 5.2, h: 1.4, fontSize: 80, bold: true, color: C.goldLight }));
    s.addText("in damage, every year", T({ objectName: "L2_n2lab", x: 7.3, y: 2.9, w: 5.2, h: 0.8, fontSize: 18, color: C.mute }));
    s.addText("“Dig up any street, and you hit a spider web.”", T({ objectName: "L2_quote", x: 0.9, y: 4.35, w: 11.6, h: 0.9, fontSize: 34, italic: true, color: C.paper }));
    s.addText("— headline, Người Lao Động newspaper, Ho Chi Minh City (translated)", T({ objectName: "L2_quoteby", x: 0.9, y: 5.3, w: 11.6, h: 0.5, fontSize: 16, color: C.mute }));
    s.addText("Sources: Common Ground Alliance, DIRT Report 2019 · nld.com.vn", T({ objectName: "L2_src", x: 0.9, y: 6.95, w: 11.6, h: 0.3, fontSize: 10, color: C.dim }));
  },
  (s) => {
    s.addImage({ objectName: "L3_photo", path: img("Slide1_SanTruong_16x9.jpg"), x: 0, y: 0, w: W, h: H, altText: "Asphalt courtyard and stone benches on the HCMUS campus" });
    s.addImage({ objectName: "L3_shade", path: grad("grad_bottom.png"), x: 0, y: 0, w: W, h: H, altText: "" });
    s.addText("This courtyard · HCMUS campus", T({ objectName: "L3_tag", shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, x: 0.8, y: 0.5, w: 3.7, h: 0.45, fontSize: 14, color: "FFFFFF", fill: { color: "000000", transparency: 35 }, align: "center", valign: "middle" }));
    s.addImage({ objectName: "L3_logo", path: img("Logo_HCMUS_trang.png"), x: 11.75, y: 0.4, w: 1.0, h: 0.82, altText: "HCMUS logo" });
    s.addText("What is under our feet?", T({ objectName: "L3_q", x: 0.8, y: 3.95, w: 11.8, h: 1.1, fontSize: 58, bold: true, color: "FFFFFF" }));
    s.addText("Application of GPR in Surveying Underground Cables and Utilities", T({ objectName: "L3_title", x: 0.8, y: 5.15, w: 11.8, h: 0.5, fontSize: 24, bold: true, color: C.goldLight }));
    s.addText(TEAM.join("  ·  "), T({ objectName: "L3_team", x: 0.8, y: 5.8, w: 11.8, h: 0.4, fontSize: 16, bold: true, color: "FFFFFF" }));
    s.addText(`${GROUP}   ·   ${SUPERVISOR}   ·   Non-Destructive Testing Methods   ·   Faculty of Physics & Engineering Physics – HCMUS`,
      T({ objectName: "L3_info", x: 0.8, y: 6.3, w: 11.8, h: 0.4, fontSize: 13, color: "D8D8D8" }));
  },
];

pres.addSection({ title: TALK });
for (const upTo of STORY ? [0, 1, 2, 3] : [3]) {
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: TALK });
  for (let i = 0; i <= upTo; i++) hookLayers[i](s);
  s.addNotes(NOTES1);
}

// ================================================================ 2. Outline
{
  const s = pres.addSlide({ masterName: "PLAIN", sectionTitle: TALK });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 4.4, h: H, fill: { color: C.blue }, line: { color: C.blue, width: 0 } });
  s.addImage({ path: img("Logo_HCMUS_trang.png"), x: 0.7, y: 0.6, w: 0.85, h: 0.7, altText: "HCMUS logo" });
  s.addText("Outline", T({ x: 0.7, y: 2.6, w: 3.3, h: 0.9, fontSize: 44, bold: true, color: "FFFFFF" }));
  s.addText("Application of GPR in Surveying Underground Cables and Utilities", T({ x: 0.7, y: 3.6, w: 3.3, h: 1.2, fontSize: 16, color: C.paleBlue }));
  s.addText("Seminar · Non-Destructive Testing Methods", T({ x: 0.7, y: 6.55, w: 3.3, h: 0.3, fontSize: 12, color: C.paleBlue }));
  [
    ["Introduction", "Problem, objectives and approach"],
    ["Overview", "Previous work abroad and in Vietnam · NDT methods for buried utilities"],
    ["Methods", "GPR and electromagnetic-induction principles · field survey · data processing"],
    ["Results", "Model · cable and pipe sections · utility map and evaluation"],
    ["Conclusions", "Conclusions, limitations and recommendations"],
  ].forEach(([head, sub], i) => {
    const y = 0.85 + i * 1.22;
    numDot(s, 5.1, y + 0.05, 0.7, i + 1, C.blue, 22);
    s.addText(head, T({ x: 6.1, y, w: 6.6, h: 0.45, fontSize: 22, bold: true, color: C.ink }));
    s.addText(sub, T({ x: 6.1, y: y + 0.5, w: 6.6, h: 0.4, fontSize: 14, color: C.grey }));
  });
  s.addNotes(`[1:00–1:15] Our talk has five parts: the problem and what we set out to do; what others have done; the physics and how we measured; what we found; and what we learned.`);
}

// ================================================================ 3. Introduction
{
  const s = seminar(0, "1  Introduction: problem, objectives and approach");
  s.addImage({ path: img("Slide1_SanTruong_16x9.jpg"), x: 0.6, y: 1.45, w: 3.7, h: 4.75, sizing: { type: "cover", w: 3.7, h: 4.75 }, altText: "The paved courtyard behind Building I, HCMUS Nguyen Van Cu campus, where the survey was made" });
  s.addText("Survey site: courtyard behind Building I, HCMUS", T({ x: 0.6, y: 6.28, w: 3.7, h: 0.3, fontSize: 11, italic: true, color: C.grey }));
  const boxes = [
    ["Problem", [
      "Cables, pipes and trenches were buried over decades; as-built drawings are incomplete or wrong.",
      "Digging blind costs money, blocks traffic and can hit live lines.",
    ]],
    ["Objectives", [
      "Locate buried cables and pipes behind Building I without digging.",
      "Estimate the depth to the top of each.",
      "Map them in plan view (2D / 3D).",
    ]],
    ["Approach", [
      "GPR IDS Detector Duo, 250\u00a0+\u00a0700\u00a0MHz.",
      "Zigzag grid of 9 lines (4 C + 5 N), 10\u00a0m\u00a0×\u00a03.5\u00a0m.",
      "ReflexW processing + 2-layer velocity model.",
    ]],
    ["Expected results", [
      "Each utility shows as a hyperbola on every line that crosses it.",
      "Apexes joined across lines give its path; apex time + velocity give its depth.",
    ]],
  ];
  boxes.forEach(([head, items], i) => {
    const x = 4.7 + (i % 2) * 4.12, y = 1.45 + Math.floor(i / 2) * 2.65, w = 3.92, h = 2.5;
    card(s, x, y, w, h);
    s.addText(head, T({ x: x + 0.25, y: y + 0.2, w: w - 0.5, h: 0.4, fontSize: 18, bold: true, color: C.blue }));
    s.addText(bullets(items), T({ x: x + 0.25, y: y + 0.7, w: w - 0.5, h: h - 0.85, fontSize: 14, color: C.ink, paraSpaceAfter: 5 }));
  });
  s.addNotes(`[1:15–2:00] Problem: power cables, telecom cables, water pipes and utility trenches were laid over many decades, and in most Vietnamese cities the as-built drawings are incomplete or simply wrong. Digging or drilling to find them is expensive, blocks traffic, and risks hitting a live cable or a pressure pipe. Decree 39/2010 regulates underground space — but in the field we still need a way to find position and depth without breaking the surface.
Our objectives: locate the cables and pipes behind Building I without digging, estimate how deep they are, and draw a map.
Approach: one IDS Detector Duo radar with 250 and 700 MHz antennas, on a zigzag grid of nine lines over 10 by 3.5 metres. We processed the data in ReflexW and converted time to depth with a two-layer model — concrete over soil.
What we expected: each utility should appear as a hyperbola on every line that crosses it; joining the apexes gives its path, and the apex time with the velocity gives its depth.`);
}

// ================================================================ 4. 1.1 Previous work
{
  const s = seminar(1, "2.1  Previous work: abroad and in Vietnam");
  const col = (x, head, rows) => {
    s.addText(head, T({ x, y: 1.45, w: 5.9, h: 0.4, fontSize: 18, bold: true, color: C.blue }));
    rows.forEach(([who, what], i) => {
      const y = 2.0 + i * 1.24;
      card(s, x, y, 5.9, 1.12);
      s.addText(who, T({ x: x + 0.2, y: y + 0.12, w: 5.5, h: 0.32, fontSize: 14, bold: true, color: C.ink }));
      s.addText(what, T({ x: x + 0.2, y: y + 0.45, w: 5.5, h: 0.62, fontSize: 13, color: C.grey }));
    });
  };
  col(0.6, "International", [
    ["Lai, Dérobert & Annan (2018)", "30 years of GPR in civil engineering: from locating and testing to imaging and diagnosis."],
    ["Xiang et al. (2019) · Hong et al. (2018)", "Depth error from mm to cm, ~10 % of depth; 400 MHz + measured permittivity matched pipes ~1 m deep to the utility map."],
    ["Thitimakorn et al. (2016) · Bangkok", "Voids under city roads found in soft clay, a ground similar to Ho Chi Minh City."],
  ]);
  col(6.8, "Vietnam", [
    ["Trần Viết Tuấn (2011, 2012) · RAMAC/X3M", "Urban utility mapping: position error ≈ ±6.2 cm, depth error ≈ ±10 cm."],
    ["Nguyễn Phi Sơn et al. (2024)", "Base standard for shallow scanning (to 6 m) with four location-quality levels, QLB1–QLB4."],
    ["HCMUS Geophysics group · Vấn, Thuận, Cường, Trung", "GPRTVN software; velocity by energy, entropy and Kirchhoff migration; 3D data cubes with ReflexW and OpendTect."],
  ]);
  s.addText([
    { text: "Standards: ", options: { bold: true, color: C.blue } },
    { text: "ASCE/UESI/CI 38-22 and ASTM D6432-19 (US) · PAS 128:2022 (UK) · AS 5488 (AU) · CJJ 61-2017 (CN)" },
  ], T({ x: 0.6, y: 5.82, w: 12.1, h: 0.32, fontSize: 14, color: C.ink }));
  s.addText([
    { text: "Our work: ", options: { bold: true, color: C.blue } },
    { text: "the same IDS radar and ReflexW chain, end to end on a site with no drawings — following ASTM D6432-19." },
  ], T({ x: 0.6, y: 6.2, w: 12.1, h: 0.32, fontSize: 14, color: C.ink }));
  source(s, "Full reference list in the written report (§1.3–1.4)");
  s.addNotes(`[2:00–2:40] GPR has more than fifty years of history; the principles were set out by Annan, Daniels and Jol. A 2018 review by Lai and colleagues traces thirty years of GPR in civil engineering, from simply locating objects to imaging and diagnosis.
How accurate is it? Xiang and colleagues report depth errors from millimetres to centimetres — about ten percent of the depth. Hong and colleagues, with a 400 MHz antenna and permittivity measured on site, matched pipes about one metre deep to the utility map. In Bangkok, on soft clay much like ours, Thitimakorn found voids under city roads.
In Vietnam, Trần Viết Tuấn mapped urban utilities with errors of about 6 cm in position and 10 cm in depth; Nguyễn Phi Sơn and colleagues wrote a base standard with four quality levels. And the Geophysics group at our own university built the GPRTVN software, methods to estimate the wave velocity, and 3D data cubes from 2D lines.
Several countries have standards — ASCE 38 and ASTM D6432 in the US, PAS 128 in the UK, AS 5488 in Australia, CJJ 61 in China. We follow ASTM D6432 and apply the same chain end to end on a site with no drawings.`);
}

// ================================================================ 5. 1.2 NDT methods and scope
{
  const s = seminar(1, "2.2  NDT methods for buried utilities, and our scope");
  const hd = (t) => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: C.blue } } });
  const gpr = (t) => ({ text: t, options: { bold: true, fill: { color: C.paleBlue } } });
  s.addTable([
    [hd("Method"), hd("Physical principle"), hd("What it detects"), hd("Depth range"), hd("Data"), hd("Main limitation")],
    [gpr("Ground-penetrating radar (GPR)"), gpr("Reflection of a high-frequency EM pulse (10\u00a0MHz to 3\u00a0GHz)"), gpr("Metal, non-metal (PVC, HDPE, concrete) and voids"), gpr("0.2–6 m (frequency, soil)"), gpr("2D B-scan, 3D C-scan"), gpr("Strong loss in wet or saline clay; needs processing")],
    ["EM locator (RD7000)", "Low-frequency / VLF magnetic induction (50 Hz–200 kHz)", "Conductors only (Cu/Al cable, steel pipe) or a sonde", "0.3–5 m (current, mode)", "Peak / null, current, depth", "Misses non-metal pipes; distorted by nearby cables"],
    ["Ultrasonic pulse–echo", "Reflection of elastic (mechanical) waves", "Defects in concrete, welds, wall thickness", "0.01–1.5 m in solid material", "A-scan, tomography", "Needs good contact; slow on long lines"],
    ["Eddy current", "Local EM induction in a conductor", "Surface and near-surface cracks in metal", "< 10 mm", "Impedance plane", "Not for soil, rock or insulators"],
  ], { x: 0.6, y: 1.45, w: 12.1, colW: [1.85, 2.4, 2.35, 1.55, 1.95, 2.0], fontFace: "Arial", fontSize: 12, color: C.ink, border: { type: "solid", pt: 0.75, color: "D5D7DB" }, rowH: [0.45, 0.8, 0.8, 0.8, 0.8], valign: "middle", margin: 0.07 });
  card(s, 0.6, 5.35, 12.1, 1.15);
  s.addText("Scope of this work", T({ x: 0.85, y: 5.48, w: 3.0, h: 0.35, fontSize: 16, bold: true, color: C.blue }));
  s.addText(bullets([
    "GPR uses: locate position and depth · check before digging · find voids around pipes · feed utility maps.",
    "Here: shallow targets (≤ 2 m) under one paved 10 m × 3.5 m courtyard — GPR alone, as it sees metal and non-metal.",
  ]), T({ x: 0.85, y: 5.85, w: 11.6, h: 0.6, fontSize: 14, color: C.ink, paraSpaceAfter: 2 }));
  source(s, "After Table 1 of the report: Metje et al. (2007), Royal et al. (2011), Nguyễn Việt Hà (2016)");
  s.addNotes(`[2:40–3:10] How does GPR compare with other NDT methods? The EM locator, like the RD7000, only sees conductors — a PVC or HDPE pipe is invisible unless it carries a tracer wire or a sonde. Ultrasonic and eddy-current testing are excellent for defects in concrete or metal parts at close range, but they cannot sweep the ground for a network of lines.
GPR is the only one here that sees both metal and non-metal, and even voids. Its weakness: the signal fades fast in wet or saline clay, and the images need processing and an experienced eye.
GPR has four main uses for utilities: locating position and depth, checking before digging, finding voids around pipes that warn of subsidence, and feeding the underground utility map.
Our scope: shallow targets, down to about two metres, under one paved courtyard — with GPR as the only instrument.`);
}

// ================================================================ 6. 2.1 GPR principle
{
  const s = seminar(2, "3.1  Principle of ground-penetrating radar");
  // Equations are LaTeX-style PNGs from ve_cong_thuc.py (same font size and DPI) → one common scale keeps them equal in size.
  const eqImg = (s, n, x, yMid, scale, alt) => {
    const f = img(`CongThuc_GPR_${n}.png`), buf = fs.readFileSync(f);
    const w = (buf.readUInt32BE(16) / 300) * scale, h = (buf.readUInt32BE(20) / 300) * scale;
    s.addImage({ path: f, x, y: yMid - h / 2, w, h, altText: alt });
  };
  const sub = (t) => ({ text: t, options: { subscript: true } });
  const EQS = 0.72;  // widest equation (4) → 3.2 in, glyphs ≈ 22 pt

  s.addImage({ path: img("Slide2_NguyenLy_EN.png"), x: 0.6, y: 1.45, w: 5.0, h: 2.16, altText: "Antenna positions above a buried pipe and the resulting hyperbola in travel time" });
  card(s, 0.6, 3.85, 5.0, 1.25);
  s.addText("Pulse–echo, like ultrasound", T({ x: 0.8, y: 3.97, w: 4.6, h: 0.35, fontSize: 15, bold: true, color: C.blue }));
  s.addText("Pulse → echo at an interface → time gives depth. The wave is electromagnetic: no contact, no couplant.",
    T({ x: 0.8, y: 4.35, w: 4.6, h: 0.7, fontSize: 13, color: C.ink }));
  card(s, 0.6, 5.25, 5.0, 1.35);
  s.addText("Resolution vs. depth", T({ x: 0.8, y: 5.35, w: 4.6, h: 0.35, fontSize: 15, bold: true, color: C.blue }));
  eqImg(s, 5, 0.75, 6.1, 0.6, "Delta z is approximately lambda over 4, equal to v over 4 f");
  s.addText([
    { text: "250 MHz ≈ 10 cm", options: { bold: true } }, { text: " · deeper", options: { color: C.grey, breakLine: true } },
    { text: "700 MHz ≈ 3.6 cm", options: { bold: true } }, { text: " · sharper", options: { color: C.grey } },
  ], T({ x: 2.4, y: 5.75, w: 3.1, h: 0.7, fontSize: 13, color: C.ink, valign: "middle" }));

  const eqs = [
    ["v equals c over the square root of epsilon r", "Wave speed",
      [{ text: "c = 0.3 m/ns · ε" }, sub("r"), { text: ": relative permittivity of the ground" }]],
    ["d equals v t over 2", "Depth",
      [{ text: "t: two-way travel time, down and back" }]],
    ["R equals root epsilon 1 minus root epsilon 2, over root epsilon 1 plus root epsilon 2", "Reflection coefficient",
      [{ text: "ε" }, sub("1"), { text: ", ε" }, sub("2"), { text: ": either side of the interface · metal: R = −1 · air: R > 0" }]],
    ["t of x equals 2 over v times the square root of d squared plus x minus x0 squared", "Hyperbola",
      [{ text: "x" }, sub("0"), { text: ": target position · apex t" }, sub("0"), { text: " = 2d / v" }]],
  ];
  eqs.forEach(([alt, name, sym], i) => {
    const x = 5.95, y = 1.45 + i * 1.29, w = 6.78, h = 1.17;
    card(s, x, y, w, h);
    numDot(s, x + 0.18, y + h / 2 - 0.18, 0.36, i + 1, C.gold, 12);
    eqImg(s, i + 1, x + 0.7, y + h / 2, EQS, alt);
    s.addText(name, T({ x: x + 4.2, y: y + 0.17, w: 2.45, h: 0.3, fontSize: 14, bold: true, color: C.blue }));
    s.addText(sym, T({ x: x + 4.2, y: y + 0.5, w: 2.45, h: 0.6, fontSize: 11.5, color: C.grey }));
  });
  source(s, "Daniels (2004) [1]; Jol (2009) [2]; ASTM D6432-19. Resolution at v = 0.10 m/ns.");
  s.addNotes(`[3:10–4:05] GPR is the pulse-echo method from this course — but with radio waves instead of ultrasound, so it needs no contact with the ground.
(1) The wave speed depends on the relative permittivity of the ground. (2) Depth is speed times the two-way time, divided by two.
(3) Energy reflects wherever the permittivity changes. The sign matters: metal reflects with R = −1, an air-filled pipe with a positive R — so metal and an empty pipe have opposite polarity. (A water-filled pipe reflects with the same sign as metal, only weaker.)
(4) As we push the antenna across a small target, the echo arrives earliest right above it — the target draws a hyperbola, and the apex gives its position and depth.
Resolution is about a quarter wavelength: 10 cm at 250 MHz, under 4 cm at 700 MHz. Lower frequency sees deeper, higher is sharper — our radar records both at once.`);
}

// ================================================================ 7. 2.2 EM induction (RD7000)
{
  const s = seminar(2, "3.2  Principle of the electromagnetic locator (RD7000)");
  s.addImage({ path: img("Slide2_RD7000_EN.png"), x: 0.6, y: 1.45, w: 5.6, h: 4.56, altText: "Magnetic field around a current-carrying cable and the peak and null responses of the receiver" });
  const x = 6.6, w = 6.13;
  card(s, x, 1.45, w, 1.25);
  s.addText([{ text: "B = μ" }, { text: "0", options: { subscript: true } }, { text: "I / (2πr)" }].map((r) => ({ text: r.text, options: Object.assign({ fontFace: EQ, bold: true }, r.options || {}) })),
    T({ x: x + 0.25, y: 1.58, w: w - 0.5, h: 0.45, fontSize: 20, color: C.ink }));
  s.addText("An AC current I in a buried conductor makes a circular magnetic field that falls off as 1/r.",
    T({ x: x + 0.25, y: 2.06, w: w - 0.5, h: 0.55, fontSize: 13, color: C.grey }));
  card(s, x, 2.9, w, 1.6);
  s.addText("Peak and null", T({ x: x + 0.25, y: 3.02, w: w - 0.5, h: 0.35, fontSize: 16, bold: true, color: C.blue }));
  s.addText(bullets([
    "Horizontal coil: maximum (peak) right above the line.",
    "Vertical coil: zero (null) above the line; peak = null → undistorted field.",
    "Two stacked coils give the depth (±5 %).",
  ]), T({ x: x + 0.25, y: 3.4, w: w - 0.5, h: 1.05, fontSize: 13, color: C.ink, paraSpaceAfter: 2 }));
  card(s, x, 4.7, w, 1.85);
  s.addText("Modes and role in this work", T({ x: x + 0.25, y: 4.82, w: w - 0.5, h: 0.35, fontSize: 16, bold: true, color: C.blue }));
  s.addText(bullets([
    "Passive: Power 50/60 Hz, Radio VLF. Active: transmitter by direct connection, clamp, induction or sonde.",
    "Sees metallic lines only — a plastic pipe is invisible, hence GPR.",
    "Here: proposed cross-check of the cable depth (not yet measured).",
  ]), T({ x: x + 0.25, y: 5.2, w: w - 0.5, h: 1.3, fontSize: 13, color: C.ink, paraSpaceAfter: 2 }));
  source(s, "Radiodetection RD7000+ manual; Metje et al. (2007) [3]");
  s.addNotes(`[4:05–4:35] The second method is electromagnetic induction. An alternating current in a metal cable creates a magnetic field around it, falling off as one over r.
The receiver has coils: the horizontal coil gives a maximum — the peak — right above the cable, the vertical coil a zero — the null. When peak and null agree, the field is clean; two coils give the depth.
It is fast, but it only sees metal: a plastic water pipe is invisible. In our project it is the planned cross-check for the cable depth — we have not measured with it yet.`);
}

// ================================================================ 8. 2.3 Field survey
{
  const s = seminar(2, "3.3  Field survey: a 10 m × 3.5 m grid of 9 lines");
  s.addImage({ path: img("Slide3_LuoiTuyen.jpg"), x: 0.6, y: 1.45, w: 4.01, h: 4.7, altText: "Top view of the courtyard with survey lines C1–C4 and N1–N5" });
  s.addText([
    { text: "C1–C4", options: { bold: true, color: "B98900" } }, { text: " along the road, 1 m apart → cable", options: { breakLine: true } },
    { text: "N1–N5", options: { bold: true, color: "1E8E3E" } }, { text: " across the road, ~0.8 m apart → pipe" },
  ], T({ x: 0.6, y: 6.2, w: 4.6, h: 0.45, fontSize: 11, color: C.ink }));
  [
    ["Step1_DanhDauLuoi.jpg", "1  Mark the grid", "Measuring tape and chalk marks on the asphalt"],
    ["Step2_LapMay.jpg", "2  Set up the radar", "Assembling the dual-antenna GPR cart"],
    ["Step3_KeoMay.jpg", "3  Scan each line", "Pushing the GPR cart along one survey line"],
    ["Step4_KiemTraDuLieu.jpg", "4  Check data on site", "Checking the radargram on the laptop in the field"],
  ].forEach(([f, label, alt], i) => {
    const x = 5.3 + (i % 2) * 2.55, y = 1.45 + Math.floor(i / 2) * 1.95;
    s.addImage({ path: img(f), x, y, w: 2.4, h: 1.8, altText: alt });
    s.addText(label, T({ shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, x: x + 0.08, y: y + 0.08, w: 1.95, h: 0.34, fontSize: 12, bold: true, color: "FFFFFF", fill: { color: C.blue, transparency: 10 }, align: "center", valign: "middle" }));
  });
  const hd = (t) => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: C.blue } } });
  s.addTable([
    [hd("Parameter"), hd("Value")],
    ["Radar", "IDS Detector Duo"],
    ["Antennas", "250 + 700 MHz, shielded"],
    ["Trace interval", "2.78 cm"],
    ["Lines", "4 C + 5 N, 1 repeat (N5)"],
    ["Line layout", "perpendicular to the target"],
    ["Velocity (depth)", "0.12 | 0.10 m/ns"],
  ], { x: 10.55, y: 1.45, w: 2.18, colW: [1.0, 1.18], fontFace: "Arial", fontSize: 10.5, color: C.ink, border: { type: "solid", pt: 0.75, color: "D5D7DB" }, rowH: 0.52, valign: "middle", margin: 0.05 });
  card(s, 5.3, 5.45, 7.43, 1.05);
  s.addText([
    { text: "Why this layout: ", options: { bold: true, color: C.blue } },
    { text: "a target gives the clearest hyperbola when it is crossed at a right angle — C lines cross the cable, N lines cross the pipe." },
  ], T({ x: 5.5, y: 5.57, w: 7.05, h: 0.85, fontSize: 14, color: C.ink, valign: "middle" }));
  source(s, "Procedure after ASTM D6432-19 and PAS 128:2022. Velocity: 0.12 m/ns concrete, 0.10 m/ns soil (team 2-layer model).");
  s.addNotes(`[4:35–5:25] This is how we measured, on the courtyard you saw.
We planned a grid, 10 metres by 3.5. A target gives the clearest hyperbola when we cross it at a right angle. The cable runs across the road, so four lines go along the road — C1 to C4, one metre apart. The water pipe runs along the road, so five lines cross it — N1 to N5.
[photos] We marked the lines, set up the IDS Detector Duo with its two antennas — 250 and 700 megahertz — pushed it along every line, and checked each radargram on the laptop before moving on.
[table] One trace every 2.78 cm, ten scans including a repeat of N5 to check repeatability.`);
}

// ================================================================ 9. 2.4 Data processing
{
  const s = seminar(2, "3.4  Data processing: from raw traces to depth");
  [
    ["Move start time", "time zero at the ground surface"],
    ["DC removal + dewow", "removes the slow drift of each trace"],
    ["Background removal", "deletes flat bands repeated on every trace"],
    ["Gain", "boosts weak, deeper echoes"],
    ["Kirchhoff migration", "collapses a hyperbola to its apex (v = 0.095 m/ns)"],
    ["Time → depth", "2-layer model: 0.12 m/ns concrete, 0.10 m/ns soil"],
  ].forEach(([head, sub], i) => {
    const y = 1.5 + i * 0.84;
    numDot(s, 0.6, y + 0.03, 0.45, i + 1, C.blue, 14);
    s.addText(head, T({ x: 1.2, y, w: 3.1, h: 0.3, fontSize: 14, bold: true, color: C.ink }));
    s.addText(sub, T({ x: 1.2, y: y + 0.32, w: 3.1, h: 0.45, fontSize: 12, color: C.grey }));
  });
  s.addImage({ path: img("XuLy_TruocSau.png"), x: 4.5, y: 1.45, w: 8.23, h: 4.63, altText: "Raw and processed radargram of line N5, with the processing chain and the fitted hyperbola of the water pipe" });
  s.addText("Line N5 (repeat), 250 MHz: raw (left) and processed (right); the water-pipe hyperbola appears, depth to top ≈ 0.39 m.",
    T({ x: 4.5, y: 6.15, w: 8.23, h: 0.45, fontSize: 12, italic: true, color: C.grey }));
  source(s, "Software: ReflexW (Sandmeier); figures and maps in Python. Migration methods: Özdemir et al. (2014).");
  s.addNotes(`[5:25–6:05] Each processing step removes one problem. We move the start time to the ground surface; DC removal and dewow remove the slow drift; background removal deletes the bands that repeat on every trace; gain boosts the weak, deeper echoes.
[figure] Left: raw line N5 — the bands hide almost everything. Right: after processing, the water-pipe hyperbola is clear.
Migration with 0.095 m/ns collapses each hyperbola to its apex. For depths we use a two-layer model: 0.12 m/ns in the concrete, 0.10 in the soil.`);
}

// ================================================================ 10. 3.1 Model results
{
  const s = seminar(3, "4.1  Model results: the model matches the field hyperbolas");
  s.addImage({ path: img("MoHinh_BScan_EN.png"), x: 1.01, y: 1.45, w: 11.31, h: 5.15, altText: "Synthetic radargram of a metal cable and a PVC pipe compared with field lines C1 and N5" });
  s.addNotes(`[6:05–6:40] Before trusting the field data, we built a simple model: soil with v = 0.095 m/ns, a metal cable and an air-filled PVC pipe, both 0.45 m deep, a 250 MHz pulse.
The model predicts a hyperbola with its apex at about 9.5 ns — and on the real lines C1 and N5 the measured hyperbolas follow the same curve, the dashed gold line.
It also shows the opposite polarity of metal and an air-filled pipe, from equation (3). This is a ray model; a gprMax input file is prepared for a full-wave simulation.`);
}

// ================================================================ 11. 3.2 Field results: cable
{
  const s = seminar(3, "4.2  Field results: four aligned anomalies trace one power cable");
  s.addImage({
    path: img("Cap_4DiThuong_C1C4.png"), x: 0.6, y: 1.45, w: 6.13, h: 5.08,
    altText: "Radargrams of parallel lines C1, C2, C3 and C4 (250 MHz) drawn on the same position axis. Anomaly P1 sits at 2.5 m along the road on every line, at depths 0.65, 0.45, 0.46 and 0.43 m; a dashed orange vertical line joins the four hyperbola apexes.",
  });
  s.addText("Plan view", T({ x: 7.95, y: 1.45, w: 4.75, h: 0.35, fontSize: 14, bold: true, color: C.grey }));
  s.addImage({
    path: img("Cap_MatBang_C1C4.png"), x: 8.2, y: 1.82, w: 3.9, h: 2.39,
    altText: "Plan view: lines C1 to C4 run parallel 1 m apart, C2 and C4 walked in the opposite direction; the four P1 points fall on one dashed orange line straight across the road, the cable.",
  });
  [
    { num: "4 / 4", head: "Same echo on every line", sub: "strong, ringing hyperbola → metal" },
    { num: "90°", head: "Straight across the road", sub: "C1, C3 at 2.50 m · field marks agree" },
    { num: "≈ 0.45 m", head: "Depth to the top", sub: "C2–C4: 0.43–0.46 m · C1: 0.65 m" },
  ].forEach((r, i) => {
    const x = 7.95, y = 4.3 + i * 0.8, w = 4.78, h = 0.7;
    card(s, x, y, w, h);
    s.addText(r.num, T({ x: x + 0.2, y, w: 1.6, h, fontSize: 22, bold: true, color: C.cable, valign: "middle" }));
    s.addText(r.head, T({ x: x + 1.9, y: y + 0.07, w: 2.8, h: 0.3, fontSize: 14, bold: true, color: C.ink }));
    s.addText(r.sub, T({ x: x + 1.9, y: y + 0.38, w: 2.8, h: 0.28, fontSize: 11, color: C.grey }));
  });
  source(s, "250 MHz, lines C1–C4 (LZZ20001–20004; C3 = LZZ20003.11 flipped back), team picks. C2, C4 walked in reverse, placed from the cable marked on site.");
  s.addNotes(`[6:40–7:20] One hyperbola alone could be anything — a stone, a pocket of fill. So we look for the same echo on neighbouring lines.
[left] Lines C1 to C4 run parallel, one metre apart, drawn on the same position axis. On every line we find the same anomaly, P1 — a strong hyperbola with a long ringing tail, typical of metal.
[dashed line] The four apexes sit in one column, at 2.5 m: the cable crosses the road at a right angle. That is also what we saw on site — the marks we made lined up straight across the road.
[cards] Depth to the top is about 0.45 m on C2 to C4, and 0.65 m on C1.
(If asked: C2 and C4 were walked in the opposite direction; we flipped them and placed their start so that P1 sits on the cable we marked. C1 and C3 agree at 2.50 m on their own.)`);
}

// ================================================================ 12. 3.3 Field results: water pipe
{
  const s = seminar(3, "4.3  Field results: the water pipe on lines N1–N5");
  s.addImage({ path: img("Hinh2_OngNuoc_MatCatGPR_EN.png"), x: 0.6, y: 1.45, w: 9.2, h: 5.17, altText: "GPR sections over the water pipe: line N2 with the pipe hyperbola A1, line N1 with no clear hyperbola, line N2 after migration, and a zoom on the pipe hyperbola" });
  [
    { num: "3 / 5", lab: "lines show the pipe hyperbola: N2, N4, N5" },
    { num: "≈ 1 m", lab: "from the bench-side edge of the road (0.67–1.09 m)" },
    { num: "0.43–0.59 m", lab: "depth to the top" },
    { num: "N1: none", lab: "only flat pavement layers — we do not claim a pipe" },
  ].forEach((r, i) => {
    const x = 10.05, y = 1.45 + i * 1.29, w = 2.68, h = 1.15;
    card(s, x, y, w, h);
    s.addText(r.num, T({ x: x + 0.18, y: y + 0.1, w: w - 0.3, h: 0.4, fontSize: 18, bold: true, color: i === 3 ? C.grey : C.pipe }));
    s.addText(r.lab, T({ x: x + 0.18, y: y + 0.52, w: w - 0.3, h: 0.58, fontSize: 11, color: C.grey }));
  });
  source(s, "250 MHz; (a) N2, (b) N1, (c) N2 after migration, (d) zoom on the pipe hyperbola. Depth: 0.12 m/ns concrete, 0.10 m/ns soil.");
  s.addNotes(`[7:20–7:50] Same idea for the water pipe, on the lines across the road.
(a) N2: a clear hyperbola, A1; its top is about 0.43 m deep. We see the same pipe on N4 and N5 — about one metre from the bench-side edge of the road.
(b) N1: no clear hyperbola — only flat reflections from the pavement layers. We say so rather than guess.
(c) After migration this hyperbola does not focus well, so we do not claim a pipe size — (d) only zooms in on it.`);
}

// ================================================================ 13. 3D scene (video recorded from the Three.js page)
{
  const s = pres.addSlide({ masterName: "PLAIN", sectionTitle: TALK });
  const poster = "image/jpeg;base64," + fs.readFileSync(img("Canh3D_HienTruong_poster.jpg")).toString("base64");
  s.addMedia({ type: "video", path: img("Canh3D_HienTruong_tua.mp4"), x: 0, y: 0, w: W, h: H, cover: poster });
  s.addNotes(`[7:50–8:10] (4.4 – the video starts by itself, 19 s; the scanning part runs at 3× speed. Talk over it.)
This is our survey in 3D, built from the real data: the ground is our own top-view photo.
The radar cart scans each line — every C line, then every N line — and under each line its radargram appears.
At the end, the hyperbola apexes are joined: the orange cable straight across the road, the blue water pipe along it.
(Live version for questions: open 02_SoDoTuyen_BanDo/ket_qua/Canh3D_HienTruong.html in a browser and click the pipe or cable.)`);
}

// ================================================================ 14. 3.5 Results summary and evaluation
{
  const s = seminar(3, "4.5  Results summary and evaluation");
  s.addImage({ path: img("Canh3D_XoayVong.gif"), x: 0.6, y: 1.45, w: 6.2, h: 3.49, altText: "Animated 360-degree view of the survey area with the ground made transparent, showing the water pipe in blue and the power cable in orange with depth labels" });
  s.addText("360° view, ground made transparent · blue = water pipe · orange = power cable · labels = depth to top",
    T({ x: 0.6, y: 5.0, w: 6.2, h: 0.45, fontSize: 11, italic: true, color: C.grey }));
  card(s, 0.6, 5.55, 6.2, 1.0);
  s.addText([
    { text: "Depth uncertainty: ", options: { bold: true, color: C.blue } },
    { text: "the 2-layer model and the migration velocity (0.095 m/ns) give depths ~20 % apart — about ±0.1 m at 0.5 m." },
  ], T({ x: 0.8, y: 5.62, w: 5.8, h: 0.86, fontSize: 13, color: C.ink, valign: "middle" }));
  const hd = (t) => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: C.blue } } });
  const dot = (t, color) => ({ text: t, options: { bold: true, color } });
  s.addTable([
    [hd("Target"), hd("Seen on"), hd("Path"), hd("Depth to top"), hd("Confidence")],
    [dot("Power cable", C.cable), "C1–C4 (4/4)", "across the road, 90°", "0.43–0.65 m", dot("High", "1E8E3E")],
    [dot("Water pipe", C.pipe), "N2, N4, N5 (3/5)", "along the road, ~1 m from the edge", "0.43–0.59 m", dot("Medium", "B98900")],
    [dot("Other reflectors O1–O5", C.grey), "1 line each", "–", "0.26–0.90 m", dot("Low", C.grey)],
  ], { x: 7.1, y: 1.45, w: 5.63, colW: [1.2, 1.0, 1.2, 1.12, 1.11], fontFace: "Arial", fontSize: 11, color: C.ink, border: { type: "solid", pt: 0.75, color: "D5D7DB" }, rowH: [0.45, 0.75, 0.75, 0.75], valign: "middle", margin: 0.06 });
  card(s, 7.1, 4.4, 5.63, 2.15);
  s.addText("Evaluation", T({ x: 7.3, y: 4.52, w: 5.2, h: 0.35, fontSize: 16, bold: true, color: C.blue }));
  s.addText(bullets([
    "Cable: the same ringing echo on 4 parallel lines, in line with the marks made on site.",
    "Pipe: seen on 3 of 5 crossing lines; the path between lines is interpolated.",
    "O1–O5 appear on one line only, so they are not interpreted.",
  ]), T({ x: 7.3, y: 4.9, w: 5.25, h: 1.6, fontSize: 13, color: C.ink, paraSpaceAfter: 3 }));
  s.addNotes(`[8:10–8:55] So, what is under our feet?
[table] A power cable crosses the road at a right angle, about 0.45 m to its top — seen on all four lines: high confidence.
A water pipe runs along the road, about a metre from the bench-side edge, 0.43 to 0.59 m deep — seen on three of five lines: medium confidence.
Five other reflectors appear on one line only — we do not claim what they are.
[bottom left] The main uncertainty is the wave speed: two velocity models give depths about 20 % apart.
In Kaohsiung, nobody could see the pipe. Here, we can.`);
}

// ================================================================ 15. Conclusions and recommendations
{
  const s = seminar(4, "5  Conclusions and recommendations");
  s.addText("Conclusions", T({ x: 0.6, y: 1.5, w: 6.0, h: 0.45, fontSize: 20, bold: true, color: C.blue }));
  [
    "GPR located a power cable and a water pipe under asphalt — without digging.",
    "Crossing the target at a right angle is what makes the hyperbola visible.",
    "700 MHz gives sharp images, 250 MHz sees deeper — using both is safer.",
  ].forEach((t, i) => {
    const y = 2.15 + i * 1.15;
    numDot(s, 0.6, y, 0.55, i + 1, C.blue, 20);
    s.addText(t, T({ x: 1.4, y: y - 0.02, w: 5.2, h: 0.9, fontSize: 17, color: C.ink }));
  });
  s.addText("Limitations → recommendations", T({ x: 7.1, y: 1.5, w: 5.6, h: 0.45, fontSize: 20, bold: true, color: C.blue }));
  [
    ["Depth depends on the velocity: 2-layer model vs 0.095\u00a0m/ns shifts depths by ~20\u00a0%.", "Calibrate with the RD7000 or one small test pit."],
    ["Line positions were paced, not surveyed; reversed lines were placed from field marks.", "Fix line positions with GPS or a total station."],
    ["Pipe diameter not determined: its hyperbola does not focus; sizes seen are resolution-limited.", "Fit the pipe radius on 700\u00a0MHz hyperbolas."],
  ].forEach(([lim, next], i) => {
    const y = 2.1 + i * 1.22;
    card(s, 7.1, y, 5.6, 1.1);
    s.addText(lim, T({ x: 7.35, y: y + 0.12, w: 5.1, h: 0.5, fontSize: 14, color: C.ink }));
    s.addText([{ text: "→ ", options: { bold: true, color: C.gold } }, { text: next, options: { bold: true } }],
      T({ x: 7.35, y: y + 0.69, w: 5.1, h: 0.3, fontSize: 14, color: C.ink }));
  });
  s.addText([
    { text: "28 %", options: { bold: true, color: C.blue } },
    { text: " of utility strikes in the US are traced to locating errors (CGA, 2019). Locating well is exactly what GPR is for." },
  ], T({ x: 0.6, y: 6.05, w: 12.1, h: 0.6, fontSize: 17, italic: true, color: C.ink }));
  s.addNotes(`[8:55–9:40] Three conclusions.
One: with nine lines on a small grid, GPR found a cable and a water pipe under asphalt — no digging. The key was finding the same echo on neighbouring lines.
Two: geometry matters — crossing the target at a right angle is what makes the hyperbola appear.
Three: the two antennas complement each other — 700 MHz is sharper, 250 MHz goes deeper.
Three limits. Our depths depend on the wave speed — next time we calibrate with the RD7000 or one small test pit. Our line positions were set by hand — a GPS or a total station would make the map more accurate. And we could not determine the pipe diameter: the pipe hyperbola does not focus after migration, and the 31 by 14 cm spot on the cable is set by the resolution, not by the real size. Fitting the hyperbola shape with a radius term on the sharper 700 MHz data is the next step.
More than a quarter of utility strikes start with a locating mistake. Locating well is exactly what GPR is for.`);
}

// ================================================================ 16. References + Thank you / Q&A
{
  const s = pres.addSlide({ masterName: "PLAIN", sectionTitle: TALK });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 5.6, h: H, fill: { color: C.blue }, line: { color: C.blue, width: 0 } });
  s.addImage({ path: img("Logo_HCMUS_trang.png"), x: 0.7, y: 0.45, w: 0.73, h: 0.6, altText: "HCMUS logo" });
  s.addText("What is under our feet?", T({ x: 0.7, y: 1.3, w: 4.5, h: 0.45, fontSize: 20, color: C.paleBlue }));
  s.addText("Now we know.", T({ x: 0.7, y: 1.75, w: 4.5, h: 0.9, fontSize: 44, bold: true, color: "FFFFFF" }));
  s.addText("Thank you — Questions?", T({ x: 0.7, y: 2.7, w: 4.5, h: 0.6, fontSize: 26, bold: true, color: C.goldLight }));
  s.addImage({ path: img("Nhom_HienTruong.jpg"), x: 0.7, y: 3.7, w: 2.4, h: 1.8, altText: "Our team with the GPR on site" });
  s.addText([
    { text: "Our team", options: { bold: true, color: C.goldLight, breakLine: true } },
    ...TEAM.map((n, i) => ({ text: n, options: { color: "FFFFFF", breakLine: i < TEAM.length - 1 } })),
  ], T({ x: 3.3, y: 3.7, w: 2.1, h: 1.8, fontSize: 14 }));
  s.addText(`${GROUP} · ${SUPERVISOR}`, T({ x: 0.7, y: 5.75, w: 4.5, h: 0.3, fontSize: 12, color: C.paleBlue }));
  s.addText("Non-Destructive Testing Methods · HCMUS", T({ x: 0.7, y: 6.1, w: 4.5, h: 0.3, fontSize: 12, color: C.paleBlue }));

  s.addText("References", T({ x: 6.1, y: 0.55, w: 6.6, h: 0.6, fontSize: 26, bold: true, color: C.blue }));
  const refs = [
    "Daniels, D. J. (2004). Ground Penetrating Radar, 2nd ed. IET.",
    "Jol, H. M. (2009). Ground Penetrating Radar: Theory and Applications. Elsevier.",
    "Metje, N. et al. (2007). Mapping the Underworld – state-of-the-art review. Tunn. Undergr. Space Technol. 22, 568–586.",
    "Royal, A. C. D. et al. (2011). Site assessment of multiple-sensor approaches for buried utility detection. Int. J. Geophys.",
    "Lai, W. W.-L., Dérobert, X., Annan, P. (2018). A review of GPR application in civil engineering. NDT & E Int. 96, 58–78.",
    "Nguyễn Thành Vấn et al. (2018). GPRTVN – processing GPR data software. Sci. Technol. Dev. J. – Nat. Sci. 2(5), 97–104.",
    "Đặng Hoàng Duy et al. (2020). Data analysis of 2D GPR profiles in 3D space. Sci. Technol. Dev. J. – Nat. Sci. 3(3), 169–179.",
    "Common Ground Alliance (2020). DIRT Report 2019. · ASTM D6432-19. · PAS 128:2022.",
  ];
  s.addText(refs.flatMap((r, i) => [{ text: `[${i + 1}]  `, options: { bold: true, color: C.blue } }, { text: r, options: { breakLine: i < refs.length - 1 } }]),
    T({ x: 6.1, y: 1.35, w: 6.6, h: 5.4, fontSize: 12, color: C.ink, paraSpaceAfter: 7 }));
  s.addNotes(`[9:40–10:00] At the start we asked: what is under our feet? Now we know — a cable crossing the road and a water pipe along it, about half a metre down.
Thank you for listening. We are happy to take your questions.
(Backup slides follow: plan-view map, depth slices, cable sections C1/C3, migration on line C1.)`);
}

// ================================================================ 17. Project repository (QR → GitHub), left on screen during Q&A
{
  const REPO = "github.com/LongDallas/NDT-GPR-Nhom1";
  const MONO = "Courier New";
  const s = seminar(null, "Project repository: data, code and slides");
  card(s, 0.6, 1.45, 4.3, 5.1);
  s.addImage({ path: img("QR_GitHub.png"), x: 0.9, y: 1.7, w: 3.7, h: 3.7, altText: `QR code linking to https://${REPO}` });
  s.addText("Scan to open", T({ x: 0.9, y: 5.55, w: 3.7, h: 0.35, fontSize: 16, bold: true, color: C.blue, align: "center" }));
  s.addText(REPO, T({ x: 0.75, y: 5.95, w: 4.0, h: 0.35, fontSize: 13, color: C.ink, align: "center" }));

  s.addText("How to use it", T({ x: 5.4, y: 1.45, w: 7.3, h: 0.45, fontSize: 20, bold: true, color: C.blue }));
  const code = (t) => ({ text: t, options: { fontFace: MONO, color: C.ink } });
  const steps = [
    ["Open", [{ text: "Scan the QR code or type the address. The repository is public — no account needed." }]],
    ["Download", [{ text: "Code → Download ZIP, or " }, code("git clone https://" + REPO)]],
    ["Read", [{ text: "Slides " }, code("01_Slide/"), { text: " · report " }, code("06_BaoCao/"), { text: " · step-by-step guide " }, code("README.md")]],
    ["Reproduce", [{ text: "Raw lines " }, code("03_DuLieuHienTruong/"), { text: " → ReflexW → " }, code("python3 dung_ban_do_3d.py"), { text: " → maps and 3D scene" }]],
  ];
  steps.forEach(([head, body], i) => {
    const y = 2.1 + i * 1.12;
    numDot(s, 5.4, y + 0.05, 0.5, i + 1, C.blue, 18);
    s.addText(head, T({ x: 6.15, y, w: 6.55, h: 0.35, fontSize: 16, bold: true, color: C.ink }));
    s.addText(body, T({ x: 6.15, y: y + 0.38, w: 6.55, h: 0.62, fontSize: 13, color: C.grey }));
  });
  source(s, "Raw GPR data, processing scripts, figures, slides and report of Group 1 · guide in Vietnamese (README.md)");
  s.addNotes(`[Q&A – leave this slide on screen while answering questions]
Everything we showed is online: the raw GPR lines, the processing scripts, the maps, these slides and the written report. Scan the QR code — the repository is public. The README explains, step by step and in Vietnamese, how to open the files and how to reproduce our maps from the raw data.`);
}

// ================================================================ Backup
const BK = "Backup";
pres.addSection({ title: BK });
{
  const s = seminar(null, "Backup · Plan view: every target with its depth", BK);
  s.addImage({ path: img("BanDo_OngNuoc_Cap.png"), x: 0.6, y: 1.6, w: 12.1, h: 4.7, altText: "Plan view map of the water pipe and power cable with depth labels" });
  s.addNotes("Use if asked where exactly each point was measured, or about the dashed extensions.");
}
{
  const s = seminar(null, "Backup · Depth slices (C-scan) of the 700 MHz data", BK);
  s.addImage({ path: img("LatCat_DoSau.png"), x: 3.6, y: 1.45, w: 6.13, h: 5.25, altText: "Horizontal depth slices of GPR amplitude" });
  s.addNotes("Use if asked at which depth the targets appear. Amplitude between lines is interpolated; cells far from any line are left blank.");
}
{
  const s = seminar(null, "Backup · GPR sections over the cable: lines C1 and C3", BK);
  s.addImage({ path: img("Hinh1_Cap_MatCatGPR_EN.png"), x: 1.87, y: 1.45, w: 9.6, h: 5.4, altText: "GPR sections over the cable: line C1 with anomaly P1 and anomalies O1–O3, line C3 with P1 and O5, line C1 after migration, apparent size of the target" });
  s.addNotes("Use if asked to see the raw sections: (a) C1 and (b) C3 with P1 in red, other anomalies in orange; (c) C1 after Kirchhoff migration; (d) apparent size ~31 × 14 cm, limited by the ~10 cm resolution.");
}
{
  const s = seminar(null, "Backup · What migration does: line C1 before and after", BK);
  s.addImage({ path: img("Hinh3_VungTinHieu_EN.png"), x: 1.87, y: 1.45, w: 9.6, h: 5.4, altText: "Line C1 before and after Kirchhoff migration with a zoom on the cable signal" });
  s.addNotes("Use if asked what migration does: (a) filtered line C1 with the cable region boxed, (b) after Kirchhoff migration, (c) zoom on the signal of interest.");
}

pres.writeFile({ fileName: out }).then(() => console.log("wrote", out));
