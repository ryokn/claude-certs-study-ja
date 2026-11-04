#!/usr/bin/env python3
"""Split dialogue lines wider than LIMIT (full-width char units) at the sentence end nearest the middle."""
import re, sys
R = re.compile(r"\{([^|{}]+)\|([^{}]+)\}")
LIMIT = 80
def w(t): return sum(1 if ord(c) < 128 else 2 for c in R.sub(lambda x: x.group(1), t)) / 2
def split(spk, t):
    if w(t) <= LIMIT: return [f"{spk}: {t}"]
    cuts = [m.end() for m in re.finditer("。|！|？", t) if m.end() < len(t)]
    if not cuts: return [f"{spk}: {t}"]
    c = min(cuts, key=lambda i: abs(w(t[:i]) - w(t) / 2))
    return split(spk, t[:c]) + split(spk, t[c:])
for p in sys.argv[1:]:
    out = []; n = 0
    for l in open(p).read().split("\n"):
        m = re.match(r"^(めたん|ずんだもん): (.*)$", l)
        if m:
            r = split(m.group(1), m.group(2)); n += len(r) - 1; out += r
        else: out.append(l)
    open(p, "w").write("\n".join(out)); print(p, "split", n)
