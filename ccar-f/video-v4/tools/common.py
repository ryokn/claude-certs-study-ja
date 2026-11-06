#!/usr/bin/env python3
"""Shared helpers: fonts, TTS, heads, speakers. Paths are relative to the kit root."""
from __future__ import annotations
import hashlib, json, os, re, wave
import urllib.request, urllib.parse
from pathlib import Path
from PIL import Image, ImageFont, ImageEnhance

KIT_ROOT = Path(__file__).resolve().parent.parent
ASSETS = KIT_ROOT / "assets"
CHARS = ASSETS / "chars"
FONTS_DIR = ASSETS / "fonts"
BGM_DIR = ASSETS / "bgm"
BGM_FILE = BGM_DIR / "昼下がり気分.mp3"

SPEAKERS = {
    "ずんだもん": {"id": 3, "color": (90, 160, 74), "text": (255, 255, 255), "name": "ずんだもん", "tag": (90, 160, 74)},
    "めたん":     {"id": 2, "color": (138, 106, 168), "text": (255, 255, 255), "name": "四国めたん", "tag": (138, 106, 168)},
}
ALIASES = {"四国めたん": "めたん", "ずんだ": "ずんだもん"}
SPEED = 1.2
HEAD_W = 220
CODE_FG = "#cdd6f4"

# Font resolution: bundled Noto Sans CJK (OFL) preferred; macOS Hiragino fallback.
_FONT_CFG = {
    "regular": [
        FONTS_DIR / "NotoSansCJK-Regular.ttc",
        Path("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"),
        Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
        Path("/Library/Fonts/Arial Unicode.ttf"),
    ],
    "bold": [
        FONTS_DIR / "NotoSansCJK-Bold.ttc",
        Path("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"),
        Path("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"),
        Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
    ],
}
# NotoSansCJK TTC: index 0 = JP Sans, index 5 ≈ mono-ish face used by the approved renderer.
JP_IDX = 0
MONO_IDX = 5


def _pick(paths):
    for p in paths:
        if Path(p).exists():
            return str(p)
    raise FileNotFoundError(
        "No Japanese font found. Bundle assets/fonts/NotoSansCJK-*.ttc "
        "or install Hiragino on macOS. Checked: " + ", ".join(str(p) for p in paths)
    )


FONT_R = None
FONT_B = None


def _ensure_fonts():
    global FONT_R, FONT_B
    if FONT_R is None:
        FONT_R = _pick(_FONT_CFG["regular"])
        FONT_B = _pick(_FONT_CFG["bold"])
        # Hiragino / non-Noto TTC may not have index 5; fall back to 0 for mono.
        global MONO_IDX
        try:
            ImageFont.truetype(FONT_R, 20, index=MONO_IDX)
        except Exception:
            MONO_IDX = 0


_fc: dict = {}


def font(size, bold=False, mono=False):
    _ensure_fonts()
    k = (size, bold, mono, FONT_R, FONT_B, MONO_IDX)
    if k not in _fc:
        path = FONT_B if bold else FONT_R
        idx = MONO_IDX if mono else JP_IDX
        try:
            _fc[k] = ImageFont.truetype(path, size, index=idx)
        except Exception:
            _fc[k] = ImageFont.truetype(path, size, index=0)
    return _fc[k]


RUBY = re.compile(r"\{([^|{}]+)\|([^{}]+)\}")


def disp(t):
    return RUBY.sub(lambda m: m.group(1), t)


def yomi(t):
    return RUBY.sub(lambda m: m.group(2), t)


def voicevox_url():
    return os.environ.get("VOICEVOX_URL", "http://127.0.0.1:50021").rstrip("/")


def tts(engine, text, spk, cache):
    key = hashlib.sha1(f"{spk}|{SPEED}|{text}".encode()).hexdigest()[:16]
    out = os.path.join(cache, f"{key}.wav")
    if os.path.exists(out):
        return out
    sid = SPEAKERS[spk]["id"]
    q = urllib.request.urlopen(
        urllib.request.Request(
            f"{engine}/audio_query?" + urllib.parse.urlencode({"text": text, "speaker": sid}),
            method="POST",
        )
    ).read()
    qj = json.loads(q)
    qj["speedScale"] = SPEED
    qj["prePhonemeLength"] = 0.05
    qj["postPhonemeLength"] = 0.05
    qj["outputSamplingRate"] = 48000
    wav = urllib.request.urlopen(
        urllib.request.Request(
            f"{engine}/synthesis?speaker={sid}",
            data=json.dumps(qj).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
    ).read()
    open(out, "wb").write(wav)
    return out


def wav_info(p):
    with wave.open(p) as w:
        return w.getnframes() / w.getframerate(), w.getframerate(), w.getnchannels(), w.getsampwidth()


def load_head(kind, dim=False):
    path = CHARS / ("metan_head.png" if kind == "めたん" else "zunda_head.png")
    im = Image.open(path).convert("RGBA")
    w = HEAD_W
    h = int(im.height * w / im.width)
    im = im.resize((w, h), Image.LANCZOS)
    if dim:
        rgb = ImageEnhance.Brightness(im.convert("RGB")).enhance(0.55)
        rgb.putalpha(im.getchannel("A"))
        im = rgb
    return im, 0


def code_color(line):
    s = line.lstrip()
    if s.startswith("#"):
        return "#6c7086"
    if s.startswith('"') or s.startswith("'"):
        return "#a6e3a1"
    for kw, col in [
        (("async", "def", "return", "if", "else"), "#cba6f7"),
        (("True", "False", "None"), "#fab387"),
    ]:
        for k in kw:
            if re.search(rf"\b{k}\b", line):
                return col
    if "deny" in line or "permissionDecision" in line:
        return "#f38ba8"
    if any(x in line for x in ("allow", "PreToolUse", "PostToolUse", "HookMatcher")):
        return "#89b4fa"
    return CODE_FG
