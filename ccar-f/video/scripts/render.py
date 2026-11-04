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
CREDIT2 = "立ち絵：東北ずん子・ずんだもんプロジェクト公式素材"
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
CHAR_H = 1120
SHOW_CHARS = False  # 立ち絵表示（ユーザー要望でオフ）
SUB = (40, 790, 1880, 1040) if not SHOW_CHARS else (40, 795, 1290, 1050)  # subtitle box
ACCENT = (214, 72, 52)

_fc = {}
def font(size, bold=False, mono=False):
    k = (size, bold, mono)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FONT_B if bold else FONT_R, size, index=5 if mono else JP)
    return _fc[k]

# ---------------- parsing ----------------
RUBY = re.compile(r"\{([^|{}]+)\|([^{}]+)\}")
def disp(t): return RUBY.sub(lambda m: m.group(1), t)
def yomi(t): return RUBY.sub(lambda m: m.group(2), t)

def parse(path):
    slides, cur, incode = [], None, False
    text = re.sub(r"<!--.*?-->", "", open(path, encoding="utf-8").read(), flags=re.S)
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            incode = not incode; continue
        if incode and cur is not None:
            cur["code"].append(line); continue
        if line.startswith("## SLIDE:"):
            cur = {"title": line[9:].strip(), "sub": "", "bullets": [], "table": [], "code": [], "lines": []}
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
    # group ASCII word characters so words are not split across lines
    toks, groups = rich_tokens(s), []
    for ch, b in toks:
        if groups and re.match(r"[A-Za-z0-9_.\-/]", ch) and groups[-1][-1][1] == b and re.match(r"[A-Za-z0-9_.\-/]", groups[-1][-1][0]):
            groups[-1].append((ch, b))
        else:
            groups.append([(ch, b)])
    lines, cur, w = [], [], 0
    for g in groups:
        gw = sum(font(size, b).getlength(ch) for ch, b in g)
        if w + gw > maxw and cur:
            lines.append(cur); cur, w = [], 0
        cur.extend(g); w += gw
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

SL = (40, 30, 1880, 760) if not SHOW_CHARS else (40, 30, 1290, 770)  # slide card box

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
    if s["code"]:
        size = 32
        while max(font(size, mono=True).getlength(l) for l in s["code"]) > maxw - 50 and size > 16:
            size -= 1
        # leave room for the bullets below the code block
        reserve = sum(len(wrap_rich(b_, 34, maxw - 50)) * int(34 * 1.45) + int(34 * 0.55) for b_ in s["bullets"]) + 40
        while int(size * 1.45) * len(s["code"]) + 36 + 30 + reserve > SL[3] - 20 - y and size > 16:
            size -= 1
        if size < 28:
            print(f"WARNING: code on slide '{s['title']}' shrunk to {size}px; consider splitting", flush=True)
        lh = int(size * 1.45)
        hgt = lh * len(s["code"]) + 36
        d.rounded_rectangle([x0, y, x0 + maxw, y + hgt], 14, fill=(30, 36, 48))
        yy = y + 18
        for l in s["code"]:
            col = (140, 200, 140) if l.lstrip().startswith("#") or "# " in l and l.index("# ") > 0 and False else (225, 230, 240)
            if "#" in l:
                i = l.index("#")
                d.text((x0 + 25, yy), l[:i], font=font(size, mono=True), fill=(225, 230, 240))
                d.text((x0 + 25 + font(size, mono=True).getlength(l[:i]), yy), l[i:], font=font(size, mono=True), fill=(140, 205, 140))
            else:
                d.text((x0 + 25, yy), l, font=font(size, mono=True), fill=col)
            yy += lh
        y += hgt + 30
    if s["bullets"]:
        size = 46
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
        size = 40
        while True:
            f = font(size); fb = font(size, True)
            nat = [max(fb.getlength(r[c]) for r in rows) + 40 for c in range(ncol)]
            tot = sum(nat)
            cw = [nat[0]] + [(maxw - nat[0]) * n / sum(nat[1:]) for n in nat[1:]] if nat[0] < maxw * 0.4 else [maxw * n / tot for n in nat]
            # each column must fit its longest unbreakable ASCII word
            minw = [max([fb.getlength(w_) for r in rows for w_ in re.findall(r"[A-Za-z0-9_.\-/]+", r[c])] + [0]) + 34 for c in range(ncol)]
            minw = [max(minw[c], nat[c] if nat[c] < 260 else 0) for c in range(ncol)]  # keep short columns unwrapped
            for c in range(ncol):
                if cw[c] < minw[c]:
                    deficit = minw[c] - cw[c]; cw[c] = minw[c]
                    others = [k for k in range(ncol) if k != c and cw[k] > minw[k]]
                    room = sum(cw[k] - minw[k] for k in others)
                    for k in others:
                        cw[k] -= deficit * (cw[k] - minw[k]) / room if room else 0
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

_chars = {}
def char_img(kind, active, mouth_open):
    key = (kind, active, mouth_open)
    if key in _chars:
        return _chars[key]
    f = "metan.png" if kind == "めたん" else ("zundamon_open.png" if mouth_open else "zundamon_closed.png")
    im = Image.open(os.path.join(ASSETS, f)).convert("RGBA")
    im = im.resize((round(im.width * CHAR_H / im.height), CHAR_H), Image.LANCZOS)
    if not active:
        rgb, a = im.convert("RGB"), im.getchannel("A")
        gray = rgb.convert("L").convert("RGB")
        rgb = Image.blend(rgb, gray, 0.25)
        rgb = Image.blend(rgb, Image.new("RGB", im.size, (60, 70, 90)), 0.22)
        im = rgb.convert("RGBA"); im.putalpha(a)
    _chars[key] = im
    return im

# placement: (left x, top y, body-center offset ratio for name badge)
CHAR_POS = {"めたん": (1285, 230, 0.50), "ずんだもん": (1585, 200, 0.36)}

def render_frame(slide_img, spk, text, mouth_open=False):
    img = slide_img.copy()
    d = ImageDraw.Draw(img)
    if not SHOW_CHARS:
        d.text((1880, 1062), CREDIT, font=font(22, True), fill=(50, 60, 75), anchor="rm")
    else:
        d.text((1900, 34), CREDIT, font=font(22, True), fill=(50, 60, 75), anchor="ra")
        d.text((1900, 64), CREDIT2, font=font(18), fill=(70, 80, 95), anchor="ra")
    order = [] if not SHOW_CHARS else [k for k in CHAR_POS if k != spk] + [spk]  # speaker in front
    for kind in order:
        active = kind == spk
        ic = char_img(kind, active, mouth_open and active and kind == "ずんだもん")
        x, y, bc = CHAR_POS[kind]
        if not active:
            y += 18
        img.paste(ic, (x, y), ic)
    d = ImageDraw.Draw(img)
    for kind in (CHAR_POS if SHOW_CHARS else []):
        active = kind == spk
        x, y, bc = CHAR_POS[kind]
        cx = x + int(char_img(kind, True, False).width * bc)
        nm = SPEAKERS[kind]["name"]; nf = font(28, True); nw = nf.getlength(nm) + 40
        d.rounded_rectangle([cx - nw / 2, 1018, cx + nw / 2, 1064], 23,
                            fill=SPEAKERS[kind]["color"] if active else (130, 138, 150), outline=(255, 255, 255), width=3)
        d.text((cx, 1041), nm, font=nf, fill=(255, 255, 255), anchor="mm")
    # subtitle box
    box = SUB
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle(box, 26, fill=(22, 28, 40, 230), outline=SPEAKERS[spk]["color"] + (255,), width=5)
    img.paste(ov, (0, 0), ov)
    d = ImageDraw.Draw(img)
    nm = SPEAKERS[spk]["name"]; nf = font(32, True); nw = nf.getlength(nm) + 44
    d.rounded_rectangle([box[0] + 30, box[1] - 26, box[0] + 30 + nw, box[1] + 26], 26, fill=SPEAKERS[spk]["color"])
    d.text((box[0] + 30 + nw / 2, box[1]), nm, font=nf, fill=(255, 255, 255), anchor="mm")
    size = 54 if not SHOW_CHARS else 46
    while True:
        f = font(size, True)
        lines = wrap_plain(text, f, box[2] - box[0] - 90)
        if len(lines) <= 3 or size <= 32: break
        size -= 2
    lh = int(size * 1.4)
    y = (box[1] + box[3]) / 2 - lh * len(lines) / 2 + 6
    for ln in lines:
        d.text((box[0] + 45, y), ln, font=f, fill=SPEAKERS[spk]["text"], stroke_width=3, stroke_fill=(10, 12, 18))
        y += lh
    return img

LIP_STEP = 1 / 15
def mouth_track(wp):
    """open/closed per LIP_STEP from audio RMS (simple lip-sync)."""
    import array
    with wave.open(wp) as w:
        sr, n = w.getframerate(), w.getnframes()
        data = array.array("h", w.readframes(n))
    step = int(sr * LIP_STEP)
    rms = []
    for i in range(0, len(data), step):
        ch = data[i:i + step]
        rms.append((sum(v * v for v in ch[::4]) / max(1, len(ch[::4]))) ** 0.5)
    peak = max(rms) if rms else 1
    track = [r > max(900, peak * 0.22) for r in rms]
    # avoid 1-step flicker
    for i in range(1, len(track) - 1):
        if track[i - 1] == track[i + 1] != track[i]:
            track[i] = track[i - 1]
    return track

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
    work = os.path.abspath(a.work or os.path.join(os.path.dirname(os.path.abspath(a.out)), "build"))
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
            if SHOW_CHARS and spk == "ずんだもん" and os.path.exists(os.path.join(ASSETS, "zundamon_open.png")):
                fo = os.path.join(work, "frames", f"{n:04d}o.png")
                render_frame(simg, spk, disp(line), mouth_open=True).save(fo)
                tr = mouth_track(wp)
                segs, acc = [], 0.0
                for st in tr:
                    dd = min(LIP_STEP, dur - acc)
                    if dd <= 0: break
                    if segs and segs[-1][0] == st: segs[-1][1] += dd
                    else: segs.append([st, dd])
                    acc += dd
                segs.append([False, total - acc])
                for st, dd in segs:
                    if dd > 0.001:
                        concat.append(f"file '{fo if st else fp}'\nduration {dd:.4f}\n")
            else:
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
