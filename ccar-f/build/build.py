# -*- coding: utf-8 -*-
import json, random, html, os
from questions import Q, DOMAINS, S
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
L = "ABCDE"
# 正解位置をバランスよく配置（単一選択）：A..Dを循環させつつ乱数で並べ替え
rng = random.Random(20261116)
singles = [i for i, q in enumerate(Q) if q.get("multi", 1) == 1]
pos_cycle = (list(range(4)) * 10)[:len(singles)]
rng.shuffle(pos_cycle)
items = []
for i, q in enumerate(Q):
    ch = list(q["c"])
    if q.get("multi", 1) == 1:
        correct = [c for c in ch if c[1]][0]
        others = [c for c in ch if not c[1]]
        rng.shuffle(others)
        p = pos_cycle[singles.index(i)]
        ch = others[:p] + [correct] + others[p:]
    else:
        multi_pos = {3: [1, 4], 13: [0, 2], 23: [2, 3]}.get(i)
        cor = [c for c in ch if c[1]]; oth = [c for c in ch if not c[1]]
        rng.shuffle(cor); rng.shuffle(oth)
        if multi_pos:
            arr = [None] * len(ch)
            for pidx, c in zip(multi_pos, cor): arr[pidx] = c
            it_o = iter(oth); arr = [a if a is not None else next(it_o) for a in arr]
            ch = arr
        else:
            rng.shuffle(ch)
    items.append(dict(id=i + 1, d=q["d"], task=q["task"], scenario=S[q["s"]], q=q["q"], multi=q.get("multi", 1),
                      choices=[{"t": c[0], "ok": c[1], "why": c[2]} for c in ch]))
for it in items:
    it["answer"] = [L[k] for k, c in enumerate(it["choices"]) if c["ok"]]

TARGET_MIN = len(items) * 2
dshort = {"D1": "分野1 エージェント", "D2": "分野2 ツール/MCP", "D3": "分野3 Claude Code", "D4": "分野4 プロンプト/構造化", "D5": "分野5 コンテキスト/信頼性"}

# ---------- Markdown（模擬試験・解答・解説はHTMLに集約。.md には案内だけを入れる） ----------
mock_md = ("## 8. 模擬試験（HTML版）\n\n"
           "模擬試験（%d問・解答と解説つき）は `ccar-f-mock-exam.html` で解いてください。"
           "目標時間は%d分です。分野別スコアもHTML上で自動集計され、進捗は自動保存されます。\n\n---\n\n" % (len(items), TARGET_MIN))

parts = [open(os.path.join(os.path.dirname(__file__), p), encoding="utf-8").read() for p in ["part1.md", "part2.md", "part3.md", "part4.md"]]
tail = open(os.path.join(os.path.dirname(__file__), "part5.md"), encoding="utf-8").read()
guide = "".join(parts) + "\n" + mock_md + tail
open(os.path.join(OUT, "ccar-f-study-guide.md"), "w", encoding="utf-8").write(guide)

# ---------- HTML ----------
tpl = open(os.path.join(os.path.dirname(__file__), "template.html"), encoding="utf-8").read()
data = {"items": items, "domains": DOMAINS, "dshort": dshort, "targetMin": TARGET_MIN}
js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
open(os.path.join(OUT, "ccar-f-mock-exam.html"), "w", encoding="utf-8").write(tpl.replace("/*__DATA__*/null", js))
json.dump(items, open(os.path.join(os.path.dirname(__file__), "items.json"), "w"), ensure_ascii=False, indent=1)
from collections import Counter
print("answers:", Counter(a for it in items for a in it["answer"]), "target", TARGET_MIN)
