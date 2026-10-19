"""Thêm hiệu ứng cho bài trình bày.

- Slide 1: mọi hình có tên L1_*, L2_*, L3_* hiện ra (Fade) cùng lúc ở lần bấm 1, 2, 3 (L0_* hiện sẵn).
- Slide có video: video tự chạy khi tới slide (Start: Automatically).
Cách dùng: python3 them_hieu_ung.py deck.pptx
"""
import re
import sys
import zipfile
import shutil
import tempfile
import subprocess

SLIDE = "ppt/slides/slide1.xml"
FADE_MS = 900


def build_timing(groups, sp_ids):
    nid = [2]

    def next_id():
        nid[0] += 1
        return nid[0]

    clicks = []
    for shapes in groups:
        outer, inner = next_id(), next_id()
        effects = []
        for k, (spid, _) in enumerate(shapes):
            node = "clickEffect" if k == 0 else "withEffect"
            e, s1, s2 = next_id(), next_id(), next_id()
            effects.append(
                f'<p:par><p:cTn id="{e}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" grpId="0" nodeType="{node}">'
                f'<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
                f'<p:set><p:cBhvr><p:cTn id="{s1}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
                f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr>'
                f'<p:to><p:strVal val="visible"/></p:to></p:set>'
                f'<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{s2}" dur="{FADE_MS}"/>'
                f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>'
                f'</p:childTnLst></p:cTn></p:par>'
            )
        clicks.append(
            f'<p:par><p:cTn id="{outer}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>'
            f'<p:par><p:cTn id="{inner}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            + "".join(effects)
            + "</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>"
        )
    bld = "".join(f'<p:bldP spid="{i}" grpId="0" animBg="1"/>' for i in sp_ids)
    return (
        '<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
        '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
        + "".join(clicks)
        + '</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
        '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
        "</p:childTnLst></p:cTn></p:par></p:tnLst>"
        + (f"<p:bldLst>{bld}</p:bldLst>" if bld else "")
        + "</p:timing>"
    )


VIDEO_TIMING = (
    '<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
    '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
    '<p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/>'
    '<p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>'
    '<p:par><p:cTn id="4" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
    '<p:par><p:cTn id="5" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="afterEffect">'
    '<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
    '<p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr><p:cTn id="6" dur="{dur}" fill="hold"/>'
    '<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:cmd>'
    '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>'
    '</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
    '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
    '<p:video><p:cMediaNode vol="80000"><p:cTn id="7" fill="hold" display="0"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst></p:cTn>'
    '<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cMediaNode></p:video>'
    '</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>'
)


def thoi_luong_ms(z, ten):
    """Độ dài video (ms) đọc bằng ffprobe; không có ffprobe thì lấy 60 s."""
    with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
        f.write(z.read(ten)); f.flush()
        try:
            out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f.name],
                                 capture_output=True, text=True, check=True).stdout
            return int(float(out) * 1000)
        except (OSError, subprocess.CalledProcessError, ValueError):
            return 60000


def video_tu_chay(z, ten_slide, xml):
    """Slide có video và chưa có <p:timing>: cho video tự chạy khi tới slide."""
    m = re.search(r'<p:cNvPr id="(\d+)"[^>]*>(?:(?!</p:pic>).)*?<a:videoFile r:link="(rId\d+)"', xml, re.S)
    if not m or "<p:timing>" in xml:
        return xml
    rels = z.read(ten_slide.replace("slides/", "slides/_rels/") + ".rels").decode("utf-8")
    dich = re.search(r'Id="%s"[^>]*Target="([^"]+)"' % m.group(2), rels) or re.search(r'Target="([^"]+)"[^>]*Id="%s"' % m.group(2), rels)
    media = "ppt/" + dich.group(1).replace("../", "")
    timing = VIDEO_TIMING.format(spid=m.group(1), dur=thoi_luong_ms(z, media))
    print(f"Video tự chạy: {ten_slide} ({media})")
    return xml.replace("</p:sld>", timing + "</p:sld>", 1)


def main(deck):
    with zipfile.ZipFile(deck) as z:
        xml = z.read(SLIDE).decode("utf-8")
        sua = {n: video_tu_chay(z, n, z.read(n).decode("utf-8")) for n in z.namelist()
               if re.fullmatch(r"ppt/slides/slide\d+\.xml", n) and n != SLIDE and b"videoFile" in z.read(n)}
    # (kind, id, name) of every shape/picture, in document order
    found = re.findall(r'<p:(sp|pic)>\s*<p:nv(?:Sp|Pic)Pr>\s*<p:cNvPr id="(\d+)" name="([^"]*)"', xml)
    groups = []
    for n in (1, 2, 3):
        groups.append([(i, kind) for kind, i, name in found if name.startswith(f"L{n}_")])
    if not all(groups):
        sys.exit(f"Không tìm thấy đủ lớp L1–L3: {[len(g) for g in groups]}")
    sp_ids = [i for g in groups for i, kind in g if kind == "sp"]
    timing = build_timing(groups, sp_ids)
    xml = re.sub(r"<p:timing>.*?</p:timing>", "", xml, flags=re.S)
    xml = xml.replace("</p:sld>", timing + "</p:sld>", 1) if "<p:extLst" not in xml.split("</p:clrMapOvr>")[-1] \
        else xml.replace("<p:extLst", timing + "<p:extLst", 1)

    tmp = tempfile.mktemp(suffix=".pptx")
    with zipfile.ZipFile(deck) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == SLIDE:
                data = xml.encode("utf-8")
            elif item.filename in sua:
                data = sua[item.filename].encode("utf-8")
            else:
                data = zin.read(item.filename)
            zout.writestr(item, data)
    shutil.move(tmp, deck)
    print("Đã thêm hiệu ứng:", [len(g) for g in groups], "hình ở lần bấm 1/2/3")


if __name__ == "__main__":
    main(sys.argv[1])
