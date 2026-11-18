#!/usr/bin/env python3
"""Extract one frame per slide from epNN.mp4 (via ffmpeg) and tile them 2x2 into frames_check/epNN_sheetK.png."""
import json, subprocess, sys, os
from PIL import Image
ep = sys.argv[1]; root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tl = json.load(open(f"{root}/build_ep{ep}/timeline.json"))
first = {}
for e in tl:
    first.setdefault(e["slide"], e)
out = f"{root}/frames_check"; os.makedirs(out, exist_ok=True)
paths = []
for s, e in sorted(first.items()):
    p = f"{out}/ep{ep}_s{s:02d}.png"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(e["start"] + 0.5), "-i", f"{root}/ep{ep}.mp4", "-frames:v", "1", p], check=True)
    paths.append(p)
for k in range(0, len(paths), 4):
    sheet = Image.new("RGB", (1920, 1080), "black")
    for j, p in enumerate(paths[k:k + 4]):
        im = Image.open(p).resize((960, 540))
        sheet.paste(im, ((j % 2) * 960, (j // 2) * 540))
    sheet.save(f"{out}/ep{ep}_sheet{k // 4}.png")
print(len(paths), "slides")
