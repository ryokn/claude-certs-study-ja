#!/usr/bin/env python3
"""Strip **bold** markers inside table rows (render.py tables do not support bold) and report suspicious lines."""
import sys, re
for p in sys.argv[1:]:
    lines = open(p).read().split("\n"); n = 0
    for i, l in enumerate(lines):
        if not re.match(r"^(めたん|ずんだもん):", l):  # emoji have no glyph in Noto Sans CJK
            l = lines[i] = l.replace("⚠️", "△").replace("⚠", "△").replace("✅", "○").replace("❌", "×").replace("✕", "×")
        if l.startswith("|") and re.search(r"\*\*(?!/)", l):
            lines[i] = re.sub(r"\*\*(?!/)", "", l); n += 1
    open(p, "w").write("\n".join(lines))
    bad = [l for l in lines if re.match(r"^(めたん|ずんだもん):", l) and re.search(r"\{[^|}]*\}", l)]
    print(p, "table bold fixed:", n, "bad ruby:", len(bad))
