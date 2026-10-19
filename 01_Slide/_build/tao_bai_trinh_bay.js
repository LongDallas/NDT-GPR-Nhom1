// Full seminar deck (English), HCMUS academic theme: 13 slides (~9:50) + 4 backup slides.
// Usage: node tao_bai_trinh_bay.js <out.pptx> [storyboard]
//   storyboard: slide 1 is written as 4 separate frames (one per click) for previewing.
// After building the real deck, run: python3 them_hieu_ung.py <out.pptx>  (adds the click fades on slide 1)
// Figures: ve_hinh_slide.py (slide 3), ../../04_XuLy_MoPhong/mo_hinh_bscan.py (slide 6),
//          ../../02_SoDoTuyen_BanDo/SDT_Tai/ve_mat_cat_gpr.py --en (slides 7, 9, A3),
//          ve_cap_4_di_thuong.py (slide 8: four aligned anomalies on C1–C4 → cable straight across the road),
//          quay_video_3d.js (slide 10: video of 02_SoDoTuyen_BanDo/ket_qua/Canh3D_HienTruong.html)
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const [out, mode] = process.argv.slice(2);
const STORY = mode === "storyboard";
const IMG = path.join(__dirname, "..", "HinhAnh");
const img = (f) => path.join(IMG, f);
const grad = (f) => path.join(__dirname, f);

const TEAM = ["Quốc Long", "Quốc Tài", "Thành Trung", "Đăng Khoa", "Đăng Quang"];
const GROUP = "Group [ ]";
const SUPERVISOR = "Supervisor: [ ]";

const C = {
  // HCMUS academic theme
  blue: "0B4A9E", gold: "C9A227", goldLight: "F2C94C", card: "EEF3FA", ink: "1B1B1D", grey: "5F6368", paleBlue: "D6E2F3",
  // storytelling opening
  night: "0A0A0B", red: "E5482D", paper: "F4F1EC", mute: "9A9A9A", dim: "6E6E6E",
  // data colours used in the figures
  pipe: "1E7BD9", cable: "E8590C",
};
const W = 13.333, H = 7.5;
const T = (o) => Object.assign({ isTextBox: true, margin: 0, fontFace: "Arial", valign: "top" }, o);
const TALK = "Talk (10 min)";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "Application of GPR in Surveying Underground Cables and Utilities";
pres.theme = { headFontFace: "Arial", bodyFontFace: "Arial" };

pres.defineSlideMaster({ title: "DARK", background: { color: C.night }, objects: [] });
pres.defineSlideMaster({ title: "BLUE", background: { color: C.blue }, objects: [] });
pres.defineSlideMaster({ title: "FIGURE", background: { color: "FFFFFF" }, objects: [] });
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

const content = (title, section = TALK) => {
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: section });
  s.addText(title, { placeholder: "title" });
  return s;
};
const figure = (file, alt, notes, section = TALK) => {
  const s = pres.addSlide({ masterName: "FIGURE", sectionTitle: section });
  s.addImage({ path: img(file), x: 0, y: 0, w: W, h: H, altText: alt });
  s.addNotes(notes);
  return s;
};
const card = (s, x, y, w, h) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: C.card }, line: { color: C.card, width: 0 } });
const source = (s, text) => s.addText(text, T({ x: 0.6, y: 6.72, w: 12.1, h: 0.26, fontSize: 10, color: C.grey }));

// ================================================================ 1. Hook (4 layers; fades added by them_hieu_ung.py)
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
[One sentence: "We are Quốc Long, Quốc Tài, Thành Trung, Đăng Khoa and Đăng Quang — and this is GPR for underground utilities."]

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

// ================================================================ 2. Previous work (abroad and in Vietnam)
{
  const s = content("GPR for buried utilities: abroad and in Vietnam");
  const col = (x, head, rows) => {
    s.addText(head, T({ x, y: 1.35, w: 5.9, h: 0.4, fontSize: 18, bold: true, color: C.blue }));
    rows.forEach(([who, what], i) => {
      const y = 1.9 + i * 1.32;
      card(s, x, y, 5.9, 1.18);
      s.addText(who, T({ x: x + 0.2, y: y + 0.13, w: 5.5, h: 0.32, fontSize: 14, bold: true, color: C.ink }));
      s.addText(what, T({ x: x + 0.2, y: y + 0.47, w: 5.5, h: 0.65, fontSize: 13, color: C.grey }));
    });
  };
  col(0.6, "International", [
    ["Metje et al. (2007) · UK, Mapping the Underworld", "Review of utility-locating methods: no single sensor finds every utility, so GPR and EM locators are combined."],
    ["Royal et al. (2011) · UK", "Site trials of multi-sensor approaches for buried utility detection."],
    ["Lai, Dérobert & Annan (2018)", "30 years of GPR in civil engineering: from locating and testing to imaging and diagnosis."],
  ]);
  col(6.8, "Vietnam · HCMUS Geophysics group", [
    ["Nguyễn Thành Vấn et al. (2018)", "GPRTVN processing software; water pipe Φ0.2 m on Nguyễn Hồng St. with the IDS Detector Duo 250/700 MHz."],
    ["Nguyễn Văn Thuận & Lê Văn Anh Cường (2021)", "Kirchhoff migration and energy analysis to find the wave velocity; power, telecom and water lines in Gò Vấp."],
    ["Đặng Hoàng Duy et al. (2020)", "2D profiles assembled in 3D: 10 objects 0.45–1 m deep, cross-checked with an EM method."],
  ]);
  s.addText([
    { text: "Our work: ", options: { bold: true, color: C.blue } },
    { text: "the same IDS Detector Duo on our own campus — the full chain from field scan to a utility map." },
  ], T({ x: 0.6, y: 5.95, w: 12.1, h: 0.45, fontSize: 16, color: C.ink }));
  source(s, "Full references in the report: Metje 2007, Royal 2011, Lai 2018 (international); Nguyễn T.V. 2018, Nguyễn V.T. 2021, Đặng H.D. 2020 (Vietnam)");
  s.addNotes(`[1:00–1:45] We are not the first. Abroad, the UK "Mapping the Underworld" project reviewed every locating method and concluded that no single sensor finds every utility — so radar and electromagnetic locators are used together. A 2018 review shows thirty years of GPR moving from simply locating objects to imaging and diagnosis.
In Vietnam, the Geophysics group at our own university has used the same radar — the IDS Detector Duo — to find water pipes and cables in Ho Chi Minh City, and to build 3D pictures from 2D lines.
What we add is small but complete: the whole chain, from scanning our own courtyard to a map of what is under it.`);
}

// ================================================================ 3. Two methods: GPR and RD7000
{
  const s = content("Two NDT methods: radar echoes and induced currents");
  s.addText("GPR · ground penetrating radar", T({ x: 0.6, y: 1.35, w: 7.4, h: 0.4, fontSize: 18, bold: true, color: C.blue }));
  s.addText("Ultrasonic pulse–echo  →  electromagnetic pulse  →  GPR", T({ x: 0.6, y: 1.8, w: 7.4, h: 0.32, fontSize: 13, bold: true, color: C.grey }));
  s.addImage({ path: img("Slide2_NguyenLy_EN.png"), x: 0.6, y: 2.25, w: 7.4, h: 3.2, altText: "Antenna positions above a buried pipe and the resulting hyperbola in travel time" });
  card(s, 0.6, 5.6, 7.4, 1.0);
  s.addText([
    { text: "v = c / √εr", options: { bold: true, color: C.ink } }, { text: "   speed set by soil permittivity", options: { color: C.grey, breakLine: true } },
    { text: "d = v · t / 2", options: { bold: true, color: C.ink } }, { text: "   two-way time · site: ", options: { color: C.grey } },
    { text: "0.12 concrete | 0.10 soil (m/ns)", options: { bold: true, color: C.blue } },
  ], T({ x: 0.8, y: 5.72, w: 7.0, h: 0.8, fontSize: 15, paraSpaceAfter: 4 }));
  s.addText("RD7000 · electromagnetic locator", T({ x: 8.4, y: 1.35, w: 4.4, h: 0.4, fontSize: 18, bold: true, color: C.blue }));
  s.addText("AC current  →  induced magnetic field  →  coils", T({ x: 8.4, y: 1.8, w: 4.4, h: 0.32, fontSize: 13, bold: true, color: C.grey }));
  s.addImage({ path: img("Slide2_RD7000_EN.png"), x: 8.4, y: 2.25, w: 4.3, h: 3.2, altText: "Magnetic field around a current-carrying cable and the peak and null responses of the receiver" });
  card(s, 8.4, 5.6, 4.3, 1.0);
  s.addText([
    { text: "Finds metallic lines only", options: { bold: true, color: C.ink, breakLine: true } },
    { text: "plastic pipes are invisible → GPR needed", options: { color: C.grey } },
  ], T({ x: 8.6, y: 5.72, w: 3.95, h: 0.8, fontSize: 14, paraSpaceAfter: 4 }));
  source(s, "Daniels (2004), Ground Penetrating Radar, 2nd ed. · Jol (2009) · Radiodetection RD7000+ manual");
  s.addNotes(`[1:45–3:00] We studied two physical ideas.
GPR works like the ultrasonic pulse-echo method from this course — only with radio waves. The antenna sends a short pulse; anything with different electrical properties — a pipe, a cable — sends part of it back. Depth is speed times the two-way time, divided by two.
As we push the antenna across a pipe, the echo arrives earliest right above it and later on both sides — so a small round object draws a hyperbola. Its top tells us where the pipe is and how deep.
The RD7000 works differently: an alternating current in a metal cable creates a magnetic field around it. The receiver coils see a maximum — the peak — or a zero — the null — right above the cable. But it only works for metal. A plastic water pipe is invisible to it — that is why we need GPR.`);
}

// ================================================================ 4. Field process
{
  const s = content("We scanned a 10 m × 3.5 m grid with 9 lines");
  s.addImage({ path: img("Slide3_LuoiTuyen.jpg"), x: 0.6, y: 1.35, w: 4.44, h: 5.2, altText: "Top view of the courtyard with survey lines C1–C4 and N1–N5" });
  s.addText([
    { text: "C1–C4", options: { bold: true, color: "B98900" } }, { text: " along the road, 1 m apart → cable", options: { breakLine: true } },
    { text: "N1–N5", options: { bold: true, color: "1E8E3E" } }, { text: " across the road, ~0.8 m apart → pipe" },
  ], T({ x: 0.6, y: 6.6, w: 4.6, h: 0.42, fontSize: 11, color: C.ink }));
  [
    ["Step1_DanhDauLuoi.jpg", "1  Mark the grid", "Measuring tape and chalk marks on the asphalt"],
    ["Step2_LapMay.jpg", "2  Set up the radar", "Assembling the dual-antenna GPR cart"],
    ["Step3_KeoMay.jpg", "3  Scan each line", "Pushing the GPR cart along one survey line"],
    ["Step4_KiemTraDuLieu.jpg", "4  Check data on site", "Checking the radargram on the laptop in the field"],
  ].forEach(([f, label, alt], i) => {
    const x = 5.55 + (i % 2) * 3.6, y = 1.35 + Math.floor(i / 2) * 2.7;
    s.addImage({ path: img(f), x, y, w: 3.4, h: 2.55, altText: alt });
    s.addText(label, T({ shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, x: x + 0.12, y: y + 0.12, w: 2.25, h: 0.4, fontSize: 14, bold: true, color: "FFFFFF", fill: { color: C.blue, transparency: 10 }, align: "center", valign: "middle" }));
  });
  s.addText("IDS Detector Duo · 250 + 700 MHz antennas · one trace every 2.78 cm · 10 scans (incl. 1 repeat of N5)",
    T({ x: 5.55, y: 6.8, w: 7.15, h: 0.25, fontSize: 11, color: C.grey }));
  s.addNotes(`[3:00–4:15] This is how we did it, on the courtyard you saw.
We planned a grid, 10 metres by 3.5. GPR sees a pipe best when we cross it at a right angle. The cable runs across the road, so four lines go along the road — C1 to C4, one metre apart. The water pipe runs along the road, so five lines cross it — N1 to N5.
[point to the photos] We marked the lines with a tape, set up the IDS Detector Duo with its two antennas — 250 and 700 megahertz — pushed it along every line, and checked each radargram on the laptop before moving on.
Ten scans in total, including one repeat of N5 to check repeatability.`);
}

// ================================================================ 5. Processing
{
  const s = content("Processing reveals the hidden hyperbola");
  s.addImage({ path: img("XuLy_TruocSau.png"), x: 1.7, y: 1.25, w: 9.93, h: 5.58, altText: "Raw and processed radargram of line N5, with the processing chain and the fitted hyperbola of the water pipe" });
  s.addNotes(`[4:15–5:00] Left: what the radar gives us on line N5 — strong horizontal bands hide almost everything.
Each processing step removes one problem: DC removal and dewow remove the slow drift; background removal deletes the bands that are the same on every trace; gain boosts the weak, deeper echoes.
Right: the water pipe now appears as a clear hyperbola. With v = 0.095 m/ns its top is about 0.4 m deep.`);
}

// ================================================================ 6. Model results
{
  const s = content("A simple model reproduces the measured hyperbolas");
  s.addImage({ path: img("MoHinh_BScan_EN.png"), x: 0.6, y: 1.3, w: 12.1, h: 5.51, altText: "Synthetic radargram of a metal cable and a PVC pipe compared with field lines C1 and N5" });
  s.addNotes(`[5:00–5:45] Before trusting the field data, we built a simple model: soil with v = 0.095 m/ns, a metal cable and an air-filled PVC pipe, both 0.45 m deep, a 250 MHz pulse.
The model predicts two things. First, a hyperbola with its top at about 9.5 ns — and on the real lines C1 and N5 the measured hyperbolas follow the same curve, the dashed gold line.
Second, metal and plastic reflect with opposite polarity — metal reverses the wave, air in the PVC pipe does not. That is how we can tell them apart.
This is a ray model, not a full-wave simulation; a gprMax input file is prepared for that next step.`);
}

// ================================================================ 7, 9. 2D sections (SDT_Tai style); 8. four aligned anomalies → cable path
figure("Hinh1_Cap_MatCatGPR_EN.png",
  "GPR sections over the cable: line C1 with anomaly P1 and anomalies O1–O3, line C3 with P1 and O5, line C1 after migration, apparent size of the target, and a small map of the survey lines",
  `[5:45–6:15] The raw evidence, as ReflexW shows it: distance on top, time on the left, depth on the right.
(a) Line C1 and (b) line C3: the red labels mark P1 — a strong hyperbola with a long ringing tail, typical of metal. The orange labels are other anomalies we do not claim.
(c) After Kirchhoff migration P1 on C1 collapses towards one point. (d) Its apparent size, about 31 by 14 cm, is limited by the ~10 cm resolution — not the real cable diameter.
But one hyperbola on one line is just a point. To get a cable, we need the same echo on neighbouring lines.`);

// ================================================================ 8. Four aligned anomalies → cable path
{
  const s = content("Four aligned anomalies trace one buried cable");
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
    card(s, x, y, w, h);
    s.addText(r.num, T({ x: x + 0.2, y, w: 1.6, h, fontSize: 22, bold: true, color: C.cable, valign: "middle" }));
    s.addText(r.head, T({ x: x + 1.9, y: y + 0.08, w: 2.75, h: 0.3, fontSize: 15, bold: true, color: C.ink }));
    s.addText(r.sub, T({ x: x + 1.9, y: y + 0.4, w: 2.75, h: 0.28, fontSize: 11.5, color: C.grey }));
  });
  source(s, "250 MHz, lines C1–C4 (LZZ20001–20004; C3 = LZZ20003.11 flipped back), team picks. Depth: 0.12 m/ns concrete, 0.10 m/ns soil. C2, C4 walked in reverse, placed from the cable marked on site.");
  s.addNotes(`[6:15–6:50] One hyperbola alone could be anything — a stone, a pocket of fill. So we look for the same echo on neighbouring lines.
[left, top to bottom] Lines C1 to C4 run parallel, one metre apart, drawn on the same position axis. On every line we find the same anomaly, P1 — a strong hyperbola with a long ringing tail, typical of metal.
[dashed line] The four tops sit in one column, at 2.5 m: the cable crosses the road straight, at a right angle. That is also what we saw on site — each time we hit the anomaly we marked the ground, and the marks lined up straight across the road.
[cards] Depth to the top is about 0.45 m on C2 to C4, and a little deeper on C1, 0.65 m.
(If asked: C2 and C4 were walked in the opposite direction. We flipped them, as the team did in ReflexW, and placed their start so that P1 sits on the cable we marked. C1 and C3, walked forward, already agree at 2.50 m on their own.)`);
}

figure("Hinh2_OngNuoc_MatCatGPR_EN.png",
  "GPR sections over the water pipe: line N2 with the pipe hyperbola A1, line N1 with no clear hyperbola, line N2 after migration, and a zoom on the pipe hyperbola",
  `[6:50–7:25] Same idea for the water pipe, on the lines across the road.
(a) N2: a clear hyperbola, A1, about 2.25 m along the line; its top is about 0.43 m deep, and the black curve fits it.
(b) N1: no clear hyperbola — only flat reflections from the pavement layers. We say so rather than guess.
(c) After migration this hyperbola does not focus well, so we do not claim a pipe size — (d) only zooms in on it.`);

// ================================================================ 9. 3D scene (video recorded from the Three.js page)
{
  const s = pres.addSlide({ masterName: "FIGURE", sectionTitle: TALK });
  const poster = "image/jpeg;base64," + fs.readFileSync(img("Canh3D_HienTruong_poster.jpg")).toString("base64");
  s.addMedia({ type: "video", path: img("Canh3D_HienTruong_tua.mp4"), x: 0, y: 0, w: W, h: H, cover: poster });
  s.addNotes(`[7:25–7:45] (The video starts by itself – 19 s; the scanning part runs at 3× speed. Talk over it.)
This is our survey in 3D, built from the real data: the ground is our own top-view photo.
Watch the radar cart scan each line — sped up three times — every C line, then every N line. Under each line, its radargram appears.
At the end, the hyperbola tops are joined: the orange cable straight across the road, the blue water pipe along it.
(Live version for questions: open 02_SoDoTuyen_BanDo/ket_qua/Canh3D_HienTruong.html in a browser and click the pipe or cable.)`);
}

// ================================================================ 10. Results
{
  const s = content("One cable crosses the road; one pipe runs along it");  // 11
  // GIF xoay 360° (quay từ cảnh 3D bằng quay_video_3d.js, mặt đất mờ để thấy ống) – PowerPoint tự chạy, lặp vô hạn
  s.addImage({ path: img("Canh3D_XoayVong.gif"), x: 0.6, y: 1.35, w: 7.1, h: 3.99, altText: "Animated 360-degree view of the survey area with the ground made transparent, showing the water pipe in blue and the power cable in orange with depth labels" });
  s.addText("360° view, ground made transparent · blue = water pipe · orange = power cable · labels = depth to top",
    T({ x: 0.6, y: 5.45, w: 7.1, h: 0.5, fontSize: 12, italic: true, color: C.grey }));
  [
    { dot: C.cable, name: "Power cable", sub: "straight across the road · on C1–C4", num: "0.43–0.65 m", lab: "depth to top" },
    { dot: C.pipe, name: "Water pipe", sub: "along the road, ~1 m from the benches · N2, N4, N5", num: "0.43–0.59 m", lab: "depth to top" },
    { dot: "9AA0A6", name: "Other reflectors", sub: "O1–O5 · 1 line each", num: "5", lab: "single-line hits" },
  ].forEach((r, i) => {
    const x = 7.95, y = 1.35 + i * 1.45, w = 4.75;
    card(s, x, y, w, 1.3);
    s.addShape(pres.shapes.OVAL, { x: x + 0.22, y: y + 0.24, w: 0.26, h: 0.26, fill: { color: r.dot }, line: { color: r.dot, width: 0 } });
    s.addText(r.name, T({ x: x + 0.6, y: y + 0.15, w: 2.6, h: 0.45, fontSize: 18, bold: true, color: C.ink }));
    s.addText(r.num, T({ x: x + 2.6, y: y + 0.12, w: 1.95, h: 0.5, fontSize: 22, bold: true, color: i === 2 ? C.grey : C.blue, align: "right" }));
    s.addText(r.sub, T({ x: x + 0.6, y: y + 0.68, w: 2.75, h: 0.5, fontSize: 12, color: C.grey }));
    s.addText(r.lab, T({ x: x + 3.35, y: y + 0.68, w: 1.2, h: 0.3, fontSize: 11, color: C.grey, align: "right" }));
  });
  s.addText("Depth to the top: v = 0.12 m/ns in concrete, 0.10 m/ns in soil. Dashed lines are straight-line extensions, not measurements.",
    T({ x: 7.95, y: 5.75, w: 4.75, h: 0.6, fontSize: 11, italic: true, color: C.grey }));
  s.addNotes(`[7:45–8:30] So, what is under our feet? [the view turns around the site, the ground is see-through]
[orange] A power cable crosses the road at a right angle, about 0.45 m to its top — the same echo on all four lines, exactly where we marked it on site.
[blue] A water pipe runs along the road, about one metre from the edge by the benches, 0.43 to 0.59 m deep — seen on N2, N4 and N5.
[grey] Five other reflectors appear on one line only — so we do not claim what they are. The dashed parts are extensions — we did not measure there.
In Kaohsiung, nobody could see the pipe. Here, we can. If someone digs here tomorrow — now we know where NOT to dig.`);
}

// ================================================================ 11. Conclusions and recommendations
{
  const s = content("What we learned, and what we would do next");
  s.addText("Conclusions", T({ x: 0.6, y: 1.4, w: 6.0, h: 0.45, fontSize: 20, bold: true, color: C.blue }));
  [
    "GPR located a cable and a water pipe under asphalt — without digging.",
    "Cross the target at a right angle: that is what makes the hyperbola visible.",
    "700 MHz gives sharp images, 250 MHz sees deeper — using both is safer.",
  ].forEach((t, i) => {
    const y = 2.05 + i * 1.15;
    s.addShape(pres.shapes.OVAL, { x: 0.6, y, w: 0.55, h: 0.55, fill: { color: C.blue }, line: { color: C.blue, width: 0 } });
    s.addText(String(i + 1), T({ x: 0.6, y, w: 0.55, h: 0.55, fontSize: 20, bold: true, color: "FFFFFF", align: "center", valign: "middle" }));
    s.addText(t, T({ x: 1.4, y: y - 0.02, w: 5.2, h: 0.9, fontSize: 17, color: C.ink }));
  });
  s.addText("Limits → recommendations", T({ x: 7.1, y: 1.4, w: 5.6, h: 0.45, fontSize: 20, bold: true, color: C.blue }));
  [
    ["Depth depends on the velocity: our 2-layer model vs 0.095 m/ns shifts depths by ~20 %.", "Calibrate with the RD7000 or one small test pit."],
    ["Line positions were paced, not surveyed: lines walked backwards had to be placed from our field marks.", "Use an odometer wheel or GPS."],
  ].forEach(([lim, next], i) => {
    const y = 2.05 + i * 1.75;
    card(s, 7.1, y, 5.6, 1.55);
    s.addText(lim, T({ x: 7.35, y: y + 0.18, w: 5.1, h: 0.75, fontSize: 15, color: C.ink }));
    s.addText([{ text: "→ ", options: { bold: true, color: C.gold } }, { text: next, options: { bold: true } }],
      T({ x: 7.35, y: y + 0.98, w: 5.1, h: 0.4, fontSize: 15, color: C.ink }));
  });
  s.addText([
    { text: "28 %", options: { bold: true, color: C.blue } },
    { text: " of utility strikes in the US are traced to locating errors (CGA, 2019). Locating well is exactly what GPR is for." },
  ], T({ x: 0.6, y: 5.8, w: 12.1, h: 0.6, fontSize: 17, italic: true, color: C.ink }));
  s.addNotes(`[8:30–9:20] Three conclusions.
One: with nine lines on a small grid, GPR found a cable and a water pipe under asphalt — no digging. The key was finding the same echo on neighbouring lines.
Two: geometry matters — crossing the target at a right angle is what makes the hyperbola appear.
Three: the two antennas complement each other — 700 MHz is sharper, 250 MHz goes deeper.
Two honest limits. Our depths depend on the wave speed: our two-layer model and the migration velocity give depths about 20 % apart — so next time we calibrate with the RD7000 or one small test pit. And our line positions were paced by hand — for the lines walked backwards we had to rely on our marks on the ground; an odometer wheel or GPS would make the map more accurate.
More than a quarter of utility strikes start with a locating mistake. Locating well is exactly what GPR is for.`);
}

// ================================================================ 12. Thank you + team
{
  const s = pres.addSlide({ masterName: "BLUE", sectionTitle: TALK });
  s.addImage({ path: img("Slide5_KetQua.jpg"), x: 6.93, y: 0, w: 6.4, h: H, altText: "The courtyard from above with the mapped pipe and cable" });
  s.addImage({ path: img("Logo_HCMUS_trang.png"), x: 0.7, y: 0.3, w: 0.73, h: 0.6, altText: "HCMUS logo" });
  s.addText("What is under our feet?", T({ x: 0.7, y: 1.05, w: 5.9, h: 0.45, fontSize: 20, color: C.paleBlue }));
  s.addText("Now we know.", T({ x: 0.7, y: 1.5, w: 5.9, h: 0.9, fontSize: 48, bold: true, color: "FFFFFF" }));
  s.addText("Thank you — Questions?", T({ x: 0.7, y: 2.45, w: 5.9, h: 0.6, fontSize: 28, bold: true, color: C.goldLight }));
  s.addImage({ path: img("Nhom_HienTruong.jpg"), x: 0.7, y: 3.35, w: 2.4, h: 1.8, altText: "Our team with the GPR on site" });
  s.addText([
    { text: "Our team", options: { bold: true, color: C.goldLight, breakLine: true } },
    ...TEAM.map((n, i) => ({ text: n, options: { color: "FFFFFF", breakLine: i < TEAM.length - 1 } })),
  ], T({ x: 3.35, y: 3.35, w: 3.3, h: 1.8, fontSize: 14 }));
  s.addText(`${GROUP} · ${SUPERVISOR}`, T({ x: 0.7, y: 5.25, w: 5.9, h: 0.3, fontSize: 12, color: C.paleBlue }));
  s.addText([
    { text: "Daniels, D. J. (2004). Ground Penetrating Radar, 2nd ed. IET.", options: { breakLine: true } },
    { text: "Metje, N. et al. (2007). Mapping the Underworld – state-of-the-art review. Tunn. Undergr. Space Technol. 22, 568–586.", options: { breakLine: true } },
    { text: "Lai, W. W.-L., Dérobert, X., Annan, P. (2018). A review of GPR application in civil engineering. NDT & E Int. 96, 58–78." },
  ], T({ x: 0.7, y: 5.75, w: 5.9, h: 1.4, fontSize: 10, color: C.paleBlue, paraSpaceAfter: 4 }));
  s.addNotes(`[9:20–9:50] At the start we asked: what is under our feet? Now we know — a cable crossing the road and a water pipe along it, about half a metre down.
Thank you for listening. We are happy to take your questions.
(Backup slides follow: plan-view map, depth slices, migration on line C1, comparison of NDT methods.)`);
}

// ================================================================ Backup
const BK = "Backup";
pres.addSection({ title: BK });
{
  const s = content("Backup · Plan view: every target with its depth", BK);
  s.addImage({ path: img("BanDo_OngNuoc_Cap.png"), x: 0.6, y: 1.5, w: 12.1, h: 4.48, altText: "Plan view map of the water pipe and power cable with depth labels" });
  s.addNotes("Use if asked where exactly each point was measured, or about the dashed extensions.");
}
{
  const s = content("Backup · Depth slices (C-scan) of the 700 MHz data", BK);
  s.addImage({ path: img("LatCat_DoSau.png"), x: 3.4, y: 1.3, w: 6.53, h: 5.6, altText: "Horizontal depth slices of GPR amplitude" });
  s.addNotes("Use if asked at which depth the targets appear. Amplitude between lines is interpolated; cells far from any line are left blank.");
}
figure("Hinh3_VungTinHieu_EN.png", "Line C1 before and after Kirchhoff migration with a zoom on the cable signal",
  "Backup – use if asked what migration does: (a) filtered line C1 with the cable region boxed, (b) after Kirchhoff migration, (c) zoom on the signal of interest.", BK);
{
  const s = content("Backup · Why GPR? NDT methods compared", BK);
  const hd = (t) => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: C.blue } } });
  s.addTable([
    [hd("Method"), hd("What it detects"), hd("Plastic pipes?"), hd("Main limitation")],
    ["Ground penetrating radar (GPR)", "Any contrast in permittivity: metal, plastic, voids", "Yes", "Signal fades fast in wet clay"],
    ["EM locator (e.g. RD7000)", "Metallic lines carrying a current", "Only with a tracer wire or sonde", "Blind to non-metallic pipes"],
    ["Magnetometer", "Ferrous (iron, steel) objects", "No", "Disturbed by nearby metal"],
    ["Electrical resistivity (ERT)", "Large resistivity contrasts", "Poorly", "Low resolution for small pipes"],
    ["Acoustic methods", "Leak noise and vibration in pipes", "Yes, if filled with water", "Needs access to the pipe"],
  ], { x: 0.6, y: 1.45, w: 12.1, colW: [3.0, 3.8, 2.4, 2.9], fontFace: "Arial", fontSize: 14, color: C.ink, border: { type: "solid", pt: 0.75, color: "D5D7DB" }, rowH: 0.62, valign: "middle", margin: 0.08 });
  source(s, "Based on Metje et al. (2007) and Royal et al. (2011)");
  s.addNotes("Use if asked why GPR: it is the only method here that sees both metallic and plastic utilities without touching them.");
}

pres.writeFile({ fileName: out }).then(() => console.log("wrote", out));
