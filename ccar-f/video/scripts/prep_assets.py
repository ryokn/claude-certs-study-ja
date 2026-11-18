#!/usr/bin/env python3
"""Download & prepare official 立ち絵 (東北ずん子・ずんだもんプロジェクト公式素材 zunko.jp/con_illust.html).
- ずんだもん: zunmon008.psd → flatten ベース + ノーマル(目:開, 口:ん / あ) → closed/open mouth PNGs
- 四国めたん: met011.png (single PNG, no expression layers)
Outputs assets/zundamon_closed.png, zundamon_open.png, metan.png (cropped, height 1400px)."""
import os, urllib.request
from psd_tools import PSDImage
from PIL import Image
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
SRC = os.path.join(A, "src"); os.makedirs(SRC, exist_ok=True)
URLS = {"zunmon008.psd": "https://zunko.jp/sozai/zundamon/zunmon008.psd",
        "met011.png": "https://zunko.jp/sozai/methane/met011.png"}
for f, u in URLS.items():
    p = os.path.join(SRC, f)
    if not os.path.exists(p):
        urllib.request.urlretrieve(u, p)
TH = 1400
def fit(im):
    im = im.crop(im.getbbox())
    return im.resize((round(im.width * TH / im.height), TH), Image.LANCZOS)
psd = PSDImage.open(os.path.join(SRC, "zunmon008.psd"))
def find(g, name):
    return next(l for l in g if l.name == name)
def put(canvas, layer):
    canvas.alpha_composite(layer.topil().convert("RGBA"), (layer.left, layer.top))
normal = find(psd, "ノーマル")
for tag, mouth in (("closed", "ん のコピー"), ("open", "あ")):
    c = Image.new("RGBA", psd.size, (0, 0, 0, 0))
    put(c, find(psd, "ベース")); put(c, find(normal, "開")); put(c, find(find(normal, "口"), mouth))
    # crop with the same bbox for both variants so they align
    if tag == "closed":
        bbox = c.getbbox()
    c = c.crop(bbox)
    c.resize((round(c.width * TH / c.height), TH), Image.LANCZOS).save(os.path.join(A, f"zundamon_{tag}.png"))
fit(Image.open(os.path.join(SRC, "met011.png")).convert("RGBA")).save(os.path.join(A, "metan.png"))
print("ok")
