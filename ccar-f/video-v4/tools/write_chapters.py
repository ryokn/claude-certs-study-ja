#!/usr/bin/env python3
"""Write YouTube chapters.txt from timeline.json + script slide titles.

Rules:
- First slide of each 第N章 becomes a chapter (use shortened title).
- Slides with `@yt: label` become extra chapter markers.
- Optional chapters_plan.txt in the episode dir: lines `SLIDE_NUM|label`
  (1-based slide index) override / add labels.
"""
from __future__ import annotations
from pathlib import Path
import argparse, json, re, sys

KIT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KIT_ROOT))
from tools.render import parse  # noqa: E402


def fmt(t: float) -> str:
    t = max(0, int(t))
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def write_chapters(ep_dir: Path) -> Path:
    ep = ep_dir.resolve()
    slides = parse(str(ep / "script.md"))
    tl = json.loads((ep / "build" / "timeline.json").read_text())
    # first timeline entry start per slide
    starts = {}
    for e in tl:
        starts.setdefault(e["slide"], e["start"])

    plan = {}
    plan_path = ep / "chapters_plan.txt"
    if plan_path.exists():
        for line in plan_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            n, label = line.split("|", 1)
            plan[int(n)] = label.strip()

    markers = []  # (start, label)
    prev_ch = None
    for i, s in enumerate(slides, 1):
        label = None
        if i in plan:
            label = plan[i]
        elif s.get("yt"):
            label = s["yt"]
        elif s["chapter"] != prev_ch:
            # strip leading 「第N章　」
            title = re.sub(r"^第\d章\s*", "", s["title"])
            label = f"第{s['chapter']}章 {title}"
        prev_ch = s["chapter"]
        if label and i in starts:
            markers.append((starts[i], label))

    # always start at 0:00
    if not markers or markers[0][0] > 0.5:
        markers.insert(0, (0.0, markers[0][1] if markers else "導入"))
    else:
        markers[0] = (0.0, markers[0][1])

    # dedupe identical consecutive timestamps
    out_lines = []
    last_t = None
    for t, lab in markers:
        key = int(t)
        if key == last_t:
            continue
        out_lines.append(f"{fmt(t)} {lab}")
        last_t = key

    out = ep / "chapters.txt"
    out.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print(out.read_text(encoding="utf-8"))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("episode_dir")
    write_chapters(Path(ap.parse_args().episode_dir))
