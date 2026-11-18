#!/usr/bin/env python3
"""Dialogue explainer video renderer (VOICEVOX + Pillow + ffmpeg).

Usage: python3 render.py SCRIPT.md OUT.mp4 [--engine http://127.0.0.1:50021]
Script format: see header comment in script_prototype.md.
Several script files can be given (comma-separated) to render a full video.
"""
import argparse, hashlib, io, json, os, re, subprocess, sys, wave, urllib.request, urllib.parse
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
FONT_R = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_B = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
JP = 0  # TTC index for "Noto Sans CJK JP"
SPEAKERS = {
    "ずんだもん": {"id": 3, "color": (122, 196, 74), "text": (200, 245, 160), "name": "ずんだもん"},
    "めたん":     {"id": 2, "color": (226, 84, 150), "text": (255, 190, 225), "name": "四国めたん"},
}
ALIASES = {"四国めたん": "めたん", "ずんだ": "ずんだもん"}
SPEED = 1.2
GAP = 0.2        # silence after each line (s)
SLIDE_GAP = 0.5   # extra silence at slide change
CREDIT = "VOICEVOX:ずんだもん / VOICEVOX:四国めたん"
ACCENT = (214, 72, 52)

_fc = {}
def font(size, bold=False):
    k = (size, bold)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FONT_B if bold else FONT_R, size, index=JP)
    return _fc[k]

# ---------------- parsing ----------------
RUBY = re.compile(r"\{([^|{}]+)\|([^{}]+)\}")
def disp(t): return RUBY.sub(lambda m: m.group(1), t)
def yomi(t): return RUBY.sub(lambda m: m.group(2), t)

def parse(path):
    slides, cur = [], None
    text = re.sub(r"<!--.*?-->", "", open(path, encoding="utf-8").read(), flags=re.S)
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("## SLIDE:"):
            cur = {"title": line[9:].strip(), "sub": "", "bullets": [], "table": [], "lines": []}
            slides.append(cur); continue
        if cur is None or not line.strip():
            continue
        if line.startswith(">"):
            cur["sub"] = line[1:].strip()
        elif line.startswith("- "):
            cur["bullets"].append(line[2:].strip())
        elif line.startswith("|"):
            cur["table"].append([c.strip() for c in line.strip().strip("|").split("|")])
        else:
            m = re.match(r"^(\S+?)[:：]\s*(.+)$", line)
            if m:
                spk = ALIASES.get(m.group(1), m.group(1))
                if spk not in SPEAKERS:
                    sys.exit(f"unknown speaker: {m.group(1)}")
                cur["lines"].append((spk, m.group(2).strip()))
    return slides

# ---------------- TTS ----------------
def tts(engine, text, spk, cache):
    key = hashlib.sha1(f"{spk}|{SPEED}|{text}".encode()).hexdigest()[:16]
    out = os.path.join(cache, f"{key}.wav")
    if os.path.exists(out):
        return out
    sid = SPEAKERS[spk]["id"]
    q = urllib.request.urlopen(urllib.request.Request(
        f"{engine}/audio_query?" + urllib.parse.urlencode({"text": text, "speaker": sid}), method="POST")).read()
    qj = json.loads(q)
    qj["speedScale"] = SPEED
    qj["prePhonemeLength"] = 0.05
    qj["postPhonemeLength"] = 0.05
    qj["outputSamplingRate"] = 48000
    wav = urllib.request.urlopen(urllib.request.Request(
        f"{engine}/synthesis?speaker={sid}", data=json.dumps(qj).encode(),
        headers={"Content-Type": "application/json"}, method="POST")).read()
    open(out, "wb").write(wav)
    return out

# ---------------- drawing helpers ----------------
def rich_tokens(s):
    toks, bold = [], False
    for part in re.split(r"(\*\*)", s):
        if part == "**":
            bold = not bold; continue
        toks += [(ch, bold) for ch in part]
    return toks

def wrap_rich(s, size, maxw):
    lines, cur, w = [], [], 0
    for ch, b in rich_tokens(s):
        cw = font(size, b).getlength(ch)
        if w + cw > maxw and cur:
            lines.append(cur); cur, w = [], 0
        cur.append((ch, b)); w += cw
    if cur: lines.append(cur)
    return lines

def draw_rich_line(d, x, y, toks, size, color, bold_color):
    for ch, b in toks:
        d.text((x, y), ch, font=font(size, b), fill=bold_color if b else color)
        x += font(size, b).getlength(ch)

def wrap_plain(s, f, maxw):
    lines, cur = [], ""
    for ch in re.findall(r"[A-Za-z0-9_.\-/]+|.", s):  # keep ASCII words intact
        if f.getlength(cur + ch) > maxw and cur:
            # avoid starting a line with punctuation
            if ch in "、。！？」』）)ー…" and len(cur) > 1:
                lines.append(cur[:-1]); cur = cur[-1] + ch; continue
            lines.append(cur); cur = ch
        else:
            cur += ch
    if cur: lines.append(cur)
    return lines

def background():
    img = Image.new("RGB", (W, H))
    top, bot = (236, 244, 250), (210, 226, 240)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)))
    return img

SL = (50, 36, 1480, 770)  # slide card box

def render_slide(base, s, idx, total):
    img = base.copy()
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([SL[0] + 6, SL[1] + 8, SL[2] + 6, SL[3] + 8], 24, fill=(0, 0, 0, 60))
    img.paste(sh.filter(ImageFilter.GaussianBlur(8)), (0, 0), sh.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(SL, 24, fill=(255, 255, 255))
    d.rounded_rectangle([SL[0], SL[1], SL[2], SL[1] + 110], 24, fill=(40, 62, 98))
    d.rectangle([SL[0], SL[1] + 80, SL[2], SL[1] + 110], fill=(40, 62, 98))
    tf = font(52, True)
    title = s["title"]
    while tf.getlength(title) > SL[2] - SL[0] - 220 and tf.size > 34:
        tf = font(tf.size - 2, True)
    d.text((SL[0] + 40, SL[1] + 55), title, font=tf, fill=(255, 255, 255), anchor="lm")
    d.text((SL[2] - 30, SL[1] + 55), f"{idx}/{total}", font=font(26), fill=(170, 190, 220), anchor="rm")
    x0, y = SL[0] + 50, SL[1] + 140
    maxw = SL[2] - SL[0] - 100
    if s["sub"]:
        d.text((x0, y), s["sub"], font=font(28), fill=(95, 105, 120)); y += 56
    if s["bullets"]:
        size = 40
        while True:
            blocks = [wrap_rich(b, size, maxw - 50) for b in s["bullets"]]
            hgt = sum(len(b) * int(size * 1.45) + int(size * 0.55) for b in blocks)
            if y + hgt < SL[3] - 30 or size <= 26: break
            size -= 2
        for bl in blocks:
            d.ellipse([x0, y + size * 0.45, x0 + 16, y + size * 0.45 + 16], fill=ACCENT)
            for ln in bl:
                draw_rich_line(d, x0 + 40, y, ln, size, (35, 40, 50), ACCENT)
                y += int(size * 1.45)
            y += int(size * 0.55)
    if s["table"]:
        rows = s["table"]; ncol = max(len(r) for r in rows)
        rows = [r + [""] * (ncol - len(r)) for r in rows]
        avail = SL[3] - 30 - y
        size = 36
        while True:
            f = font(size); fb = font(size, True)
            nat = [max(fb.getlength(r[c]) for r in rows) + 40 for c in range(ncol)]
            tot = sum(nat)
            cw = [nat[0]] + [(maxw - nat[0]) * n / sum(nat[1:]) for n in nat[1:]] if nat[0] < maxw * 0.4 else [maxw * n / tot for n in nat]
            cells = [[wrap_plain(r[c], fb if i == 0 else f, cw[c] - 30) for c in range(ncol)] for i, r in enumerate(rows)]
            rh = [max(len(cl) for cl in row) * int(size * 1.35) + 18 for row in cells]
            if sum(rh) <= avail or size <= 20: break
            size -= 2
        tw = sum(cw); ty = y
        for i, row in enumerate(cells):
            fill = (40, 62, 98) if i == 0 else ((246, 249, 253) if i % 2 else (255, 255, 255))
            d.rectangle([x0, ty, x0 + tw, ty + rh[i]], fill=fill, outline=(200, 210, 225))
            cx = x0
            for c, cl in enumerate(row):
                yy = ty + 9
                for ln in cl:
                    col = (255, 255, 255) if i == 0 else ((35, 40, 50) if c == 0 else (55, 60, 72))
                    if i > 0 and c == 1 and ncol >= 3 and re.search(r"\d", ln) and "%" in ln:
                        col = ACCENT
                    d.text((cx + 15, yy), ln, font=fb if i == 0 or c == 0 else f, fill=col)
                    yy += int(size * 1.35)
                cx += cw[c]
            ty += rh[i]
    return img

def char_icon(kind, active, size=300):
    S = size * 2
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = S // 2
    if kind == "ずんだもん":
        g, dg = (140, 205, 90), (80, 150, 50)
        # edamame-pod "ears"
        d.ellipse([c - 200, 40, c - 90, 260], fill=g, outline=dg, width=8)
        d.ellipse([c + 90, 40, c + 200, 260], fill=g, outline=dg, width=8)
        d.ellipse([c - 230, c - 190, c + 230, c + 250], fill=g, outline=dg, width=10)  # hair/head
        d.ellipse([c - 175, c - 110, c + 175, c + 230], fill=(255, 236, 222))          # face
        for ex in (-75, 75):
            d.ellipse([c + ex - 26, c + 20, c + ex + 26, c + 90], fill=(60, 120, 40))
            d.ellipse([c + ex - 10, c + 30, c + ex + 6, c + 50], fill=(255, 255, 255))
        mouth = [c - 40, c + 120, c + 40, c + 175] if active else [c - 30, c + 130, c + 30, c + 150]
        d.chord(mouth, 0, 180, fill=(200, 70, 80))
        for ex in (-120, 120):
            d.ellipse([c + ex - 30, c + 105, c + ex + 30, c + 130], fill=(255, 180, 180))
    else:
        p, dp = (230, 110, 170), (170, 60, 120)
        # twin drill side tails
        for sx in (-1, 1):
            for k in range(4):
                yy = c + 20 + k * 55
                xx = c + sx * (215 + k * 6)
                d.ellipse([xx - 55, yy - 35, xx + 55, yy + 45], fill=p, outline=dp, width=6)
        d.ellipse([c - 230, c - 210, c + 230, c + 230], fill=p, outline=dp, width=10)
        d.ellipse([c - 170, c - 100, c + 170, c + 230], fill=(255, 238, 228))
        d.pieslice([c - 190, c - 190, c + 190, c + 60], 180, 360, fill=p)  # bangs
        for ex in (-72, 72):
            d.ellipse([c + ex - 26, c + 25, c + ex + 26, c + 90], fill=(150, 60, 110))
            d.ellipse([c + ex - 10, c + 35, c + ex + 6, c + 55], fill=(255, 255, 255))
        mouth = [c - 38, c + 120, c + 38, c + 170] if active else [c - 28, c + 132, c + 28, c + 150]
        d.chord(mouth, 0, 180, fill=(200, 70, 90))
        for ex in (-118, 118):
            d.ellipse([c + ex - 30, c + 105, c + ex + 30, c + 130], fill=(255, 185, 200))
    im = im.resize((size, size), Image.LANCZOS)
    if not active:
        r, g_, b, a = im.split()
        gray = Image.merge("RGB", (r, g_, b)).convert("L").convert("RGB")
        im = Image.blend(Image.merge("RGB", (r, g_, b)), gray, 0.6)
        im = Image.blend(im, Image.new("RGB", im.size, (200, 210, 220)), 0.25)
        im.putalpha(a)
    return im

def render_frame(slide_img, spk, text):
    img = slide_img.copy()
    d = ImageDraw.Draw(img)
    # credit (required by VOICEVOX terms)
    d.text((1880, 1064), CREDIT, font=font(24), fill=(50, 60, 75), anchor="rm")
    # characters (right column): めたん upper, ずんだもん lower
    for kind, cy in (("めたん", 250), ("ずんだもん", 560)):
        active = kind == spk
        sz = 270 if active else 220
        ic = char_icon(kind, active, sz)
        cx = 1700
        if active:
            glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(glow).ellipse([cx - 155, cy - 155, cx + 155, cy + 155], fill=SPEAKERS[kind]["color"] + (110,))
            glow = glow.filter(ImageFilter.GaussianBlur(18))
            img.paste(glow, (0, 0), glow)
        img.paste(ic, (cx - sz // 2, cy - sz // 2), ic)
        d = ImageDraw.Draw(img)
        nm = SPEAKERS[kind]["name"]
        nf = font(30, True)
        nw = nf.getlength(nm) + 40
        by = cy + sz // 2 - 6
        d.rounded_rectangle([cx - nw / 2, by, cx + nw / 2, by + 48], 24,
                            fill=SPEAKERS[kind]["color"] if active else (170, 178, 188))
        d.text((cx, by + 24), nm, font=nf, fill=(255, 255, 255), anchor="mm")
    # subtitle box
    box = (40, 800, 1880, 1040)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle(box, 26, fill=(22, 28, 40, 225), outline=SPEAKERS[spk]["color"] + (255,), width=5)
    img.paste(ov, (0, 0), ov)
    d = ImageDraw.Draw(img)
    nm = SPEAKERS[spk]["name"]
    nf = font(32, True)
    nw = nf.getlength(nm) + 44
    d.rounded_rectangle([box[0] + 30, box[1] - 26, box[0] + 30 + nw, box[1] + 26], 26, fill=SPEAKERS[spk]["color"])
    d.text((box[0] + 30 + nw / 2, box[1]), nm, font=nf, fill=(255, 255, 255), anchor="mm")
    size = 50
    while True:
        f = font(size, True)
        lines = wrap_plain(text, f, box[2] - box[0] - 100)
        if len(lines) <= 3 or size <= 34: break
        size -= 2
    lh = int(size * 1.4)
    y = (box[1] + box[3]) / 2 - lh * len(lines) / 2 + 8
    for ln in lines:
        d.text((box[0] + 50, y), ln, font=f, fill=SPEAKERS[spk]["text"],
               stroke_width=3, stroke_fill=(10, 12, 18))
        y += lh
    return img

def wav_info(p):
    with wave.open(p) as w:
        return w.getnframes() / w.getframerate(), w.getframerate(), w.getnchannels(), w.getsampwidth()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scripts")
    ap.add_argument("out")
    ap.add_argument("--engine", default="http://127.0.0.1:50021")
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    work = a.work or os.path.join(os.path.dirname(os.path.abspath(a.out)), "build")
    for sub in ("wav", "frames"):
        os.makedirs(os.path.join(work, sub), exist_ok=True)
    slides = []
    for sp in a.scripts.split(","):
        slides += parse(sp)
    base = background()
    concat, pcm, sr = [], bytearray(), None
    timeline, t = [], 0.0
    n = 0
    for si, s in enumerate(slides, 1):
        simg = render_slide(base, s, si, len(slides))
        for li, (spk, line) in enumerate(s["lines"]):
            n += 1
            wp = tts(a.engine, yomi(line), spk, os.path.join(work, "wav"))
            dur, rate, ch, sw = wav_info(wp)
            if sr is None: sr, nch, swid = rate, ch, sw
            assert (rate, ch, sw) == (sr, nch, swid)
            with wave.open(wp) as w: pcm += w.readframes(w.getnframes())
            gap = GAP + (SLIDE_GAP if li == len(s["lines"]) - 1 else 0)
            pcm += b"\x00" * int(gap * sr) * nch * swid
            fp = os.path.join(work, "frames", f"{n:04d}.png")
            render_frame(simg, spk, disp(line)).save(fp)
            total = dur + gap
            concat.append(f"file '{fp}'\nduration {total:.4f}\n")
            timeline.append({"n": n, "slide": si, "speaker": spk, "start": round(t, 2), "dur": round(total, 2), "text": disp(line)})
            t += total
            print(f"[{n:03d}] {t:7.2f}s {spk}: {disp(line)[:40]}", flush=True)
    concat.append(f"file '{fp}'\n")  # concat demuxer needs last file repeated
    open(os.path.join(work, "frames.txt"), "w").write("".join(concat))
    with wave.open(os.path.join(work, "audio.wav"), "wb") as w:
        w.setnchannels(nch); w.setsampwidth(swid); w.setframerate(sr); w.writeframes(bytes(pcm))
    json.dump(timeline, open(os.path.join(work, "timeline.json"), "w"), ensure_ascii=False, indent=1)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(work, "frames.txt"),
                    "-i", os.path.join(work, "audio.wav"), "-vf", "fps=30,format=yuv420p",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-tune", "stillimage",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", a.out], check=True)
    print("done:", a.out, f"{t:.1f}s")

if __name__ == "__main__":
    main()
