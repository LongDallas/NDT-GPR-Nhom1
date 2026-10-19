// Slide 1 (hook) – one slide, 4 click steps that fade in over each other.
// Usage: node slide1_hook.js <out.pptx> <gradDir> [storyboard]
//   storyboard: write 4 slides (one per click state) for previewing instead of 1 animated slide.
const path = require("path");
const pptxgen = require("pptxgenjs");

const [out, gradDir, mode] = process.argv.slice(2);
const IMG = path.join(__dirname, "..", "HinhAnh");
const STORY = mode === "storyboard";

const COL = { night: "0A0A0B", ember: "E5482D", emberLight: "F07A55", paper: "F4F1EC", mute: "9A9A9A", dim: "6E6E6E" };
const W = 13.333, H = 7.5;

const NOTES = `[Black screen. Stand still, look at the audience, 2 seconds of silence.]

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
[Then one sentence: "We are group …, and this is GPR for underground utilities."]

CHECK BEFORE PRESENTING: confirm the timeline (~20:46 gas reports, explosions ~23:57) on Wikipedia "2014 Kaohsiung gas explosions".`;

const T = (o) => Object.assign({ isTextBox: true, margin: 0, fontFace: "Arial", valign: "top" }, o);

// Each layer adds its shapes; every object gets objectName "L<n>_..." so the animation step can find it.
const layers = [
  (s) => {
    s.addText("31 JULY 2014", T({ objectName: "L0_date", x: 0.9, y: 2.55, w: 11.5, h: 1.2, fontSize: 66, bold: true, color: COL.paper, charSpacing: 6 }));
    s.addText("Kaohsiung, Taiwan", T({ objectName: "L0_place", x: 0.9, y: 3.8, w: 11.5, h: 0.7, fontSize: 28, color: COL.mute }));
  },
  (s) => {
    s.addImage({ objectName: "L1_photo", path: path.join(IMG, "Slide1_Kaohsiung_2014.jpg"), x: 0, y: 0, w: W, h: H, altText: "Sanduo 1st Road in Kaohsiung torn open after the 2014 gas explosions, with exposed pipes" });
    s.addImage({ objectName: "L1_shade", path: path.join(gradDir, "grad_left.png"), x: 0, y: 0, w: W, h: H, altText: "" });
    s.addText("32 dead", T({ objectName: "L1_dead", x: 0.8, y: 1.7, w: 6.5, h: 1.5, fontSize: 96, bold: true, color: COL.ember }));
    s.addText("321 injured", T({ objectName: "L1_injured", x: 0.8, y: 3.25, w: 6.5, h: 0.9, fontSize: 44, bold: true, color: COL.paper }));
    s.addText([
      { text: "A leaking pipe under the street.", options: { breakLine: true } },
      { text: "Nobody could see it." },
    ], T({ objectName: "L1_cause", x: 0.8, y: 4.45, w: 6.0, h: 1.0, fontSize: 22, italic: true, color: COL.paper }));
    s.addText([
      { text: "Sanduo 1st Rd, Kaohsiung, 11 Aug 2014 · Photo: " },
      { text: "玄史生", options: { fontFace: "PingFang TC" } },
      { text: " / Wikimedia Commons · CC BY-SA 4.0" },
    ], T({ objectName: "L1_credit", x: 5.8, y: 7.05, w: 7.2, h: 0.3, fontSize: 10, color: "D0D0D0", align: "right" }));
  },
  (s) => {
    s.addShape("rect", { objectName: "L2_bg", x: 0, y: 0, w: W, h: H, fill: { color: COL.night }, line: { color: COL.night, width: 0 } });
    s.addText("And this is not rare.", T({ objectName: "L2_lead", x: 0.9, y: 0.75, w: 11.5, h: 0.5, fontSize: 22, color: COL.mute }));
    s.addText("500,000+", T({ objectName: "L2_n1", x: 0.9, y: 1.45, w: 6.0, h: 1.4, fontSize: 80, bold: true, color: COL.paper }));
    s.addText("buried utilities hit by digging each year (US)",
      T({ objectName: "L2_n1lab", x: 0.9, y: 2.9, w: 5.4, h: 0.8, fontSize: 18, color: COL.mute }));
    s.addText("$30B", T({ objectName: "L2_n2", x: 7.3, y: 1.45, w: 5.2, h: 1.4, fontSize: 80, bold: true, color: COL.ember }));
    s.addText("in damage, every year", T({ objectName: "L2_n2lab", x: 7.3, y: 2.9, w: 5.2, h: 0.8, fontSize: 18, color: COL.mute }));
    s.addText("“Dig up any street, and you hit a spider web.”",
      T({ objectName: "L2_quote", x: 0.9, y: 4.35, w: 11.6, h: 0.9, fontSize: 34, italic: true, color: COL.paper }));
    s.addText("— headline, Người Lao Động newspaper, Ho Chi Minh City (translated)",
      T({ objectName: "L2_quoteby", x: 0.9, y: 5.3, w: 11.6, h: 0.5, fontSize: 16, color: COL.mute }));
    s.addText("Sources: Common Ground Alliance, DIRT Report 2019 · nld.com.vn",
      T({ objectName: "L2_src", x: 0.9, y: 6.95, w: 11.6, h: 0.3, fontSize: 10, color: COL.dim }));
  },
  (s) => {
    s.addImage({ objectName: "L3_photo", path: path.join(IMG, "Slide1_SanTruong_16x9.jpg"), x: 0, y: 0, w: W, h: H, altText: "Asphalt courtyard and stone benches on the HCMUS campus" });
    s.addImage({ objectName: "L3_shade", path: path.join(gradDir, "grad_bottom.png"), x: 0, y: 0, w: W, h: H, altText: "" });
    s.addText("This courtyard · HCMUS campus", T({ objectName: "L3_tag", shape: "roundRect", rectRadius: 0.1, x: 0.8, y: 0.5, w: 3.7, h: 0.45, fontSize: 14, color: "FFFFFF", fill: { color: "000000", transparency: 35 }, align: "center", valign: "middle" }));
    s.addImage({ objectName: "L3_logo", path: path.join(IMG, "Logo_HCMUS_trang.png"), x: 11.75, y: 0.4, w: 1.0, h: 0.82, altText: "HCMUS logo" });
    s.addText("What is under our feet?", T({ objectName: "L3_q", x: 0.8, y: 4.3, w: 11.8, h: 1.1, fontSize: 58, bold: true, color: "FFFFFF" }));
    s.addText("Ground Penetrating Radar for Underground Cables and Utilities",
      T({ objectName: "L3_title", x: 0.8, y: 5.5, w: 11.8, h: 0.5, fontSize: 22, bold: true, color: COL.emberLight }));
    s.addText("Group [name]   ·   Supervisor: [name]   ·   Non-Destructive Testing Methods   ·   Faculty of Physics – HCMUS",
      T({ objectName: "L3_info", x: 0.8, y: 6.15, w: 11.8, h: 0.45, fontSize: 15, color: "D8D8D8" }));
  },
];

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.title = "GPR seminar – Slide 1 (hook)";
  const frames = STORY ? [0, 1, 2, 3] : [3];
  for (const upTo of frames) {
    const s = pres.addSlide();
    s.background = { color: COL.night };
    for (let i = 0; i <= upTo; i++) layers[i](s);
    s.addNotes(NOTES);
  }
  await pres.writeFile({ fileName: out });
  console.log("wrote", out);
})();
