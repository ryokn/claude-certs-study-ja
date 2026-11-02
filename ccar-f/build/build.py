# -*- coding: utf-8 -*-
import json, random, html, os
from questions import Q, DOMAINS, S
OUT = "/workspace/claude-certs/ccar-f"
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

# ---------- Markdown: §8 mock & §9 answers ----------
md = []
md.append("## 8. 模擬試験（%d問・目標 %d分）\n" % (len(items), TARGET_MIN))
md.append("- 本番と同じく **1問2分**ペース。単一選択が基本で、【2つ】と書かれた問題は複数選択（本番も各問題に選ぶ数が明記されます）。")
md.append("- 分野配分：" + "、".join("%s %d問" % (dshort[d], sum(1 for x in items if x['d'] == d)) for d in ["D1", "D2", "D3", "D4", "D5"]) + "（配点比率にほぼ比例）。")
md.append("- 同じ問題をスマホ/ブラウザで解ける `ccar-f-mock-exam.html` もあります（進捗は自動保存）。")
md.append("- 問題はすべてガイドのタスクステートメントに基づくオリジナル問題です。\n")
for it in items:
    md.append("### Q%d（%s ／ タスク%s）%s" % (it["id"], it["scenario"], it["task"], "【2つ選択】" if it["multi"] > 1 else ""))
    md.append("")
    md.append(it["q"])
    md.append("")
    for k, c in enumerate(it["choices"]):
        md.append("- **%s.** %s" % (L[k], c["t"]))
    md.append("")
md.append("---\n")
md.append("## 9. 解答一覧・分野別スコア表・解説\n")
md.append("### 9.1 解答一覧\n")
md.append("| 問 | 正解 | 分野 | タスク | 問 | 正解 | 分野 | タスク |")
md.append("|---|---|---|---|---|---|---|---|")
half = (len(items) + 1) // 2
for r in range(half):
    a = items[r]; b = items[r + half] if r + half < len(items) else None
    row = "| Q%d | %s | %s | %s |" % (a["id"], "・".join(a["answer"]), a["d"][1], a["task"])
    row += (" Q%d | %s | %s | %s |" % (b["id"], "・".join(b["answer"]), b["d"][1], b["task"])) if b else " | | | |"
    md.append(row)
md.append("\n（複数選択は全部正しく選んで1点、とする採点。本番の部分点の有無は【要確認】）\n")
md.append("### 9.2 分野別スコア表（記入用）\n")
md.append("| 分野 | 問題番号 | 問題数 | 正解数 | 正答率 | 目標 |")
md.append("|---|---|---|---|---|---|")
for d in ["D1", "D2", "D3", "D4", "D5"]:
    ids = [x["id"] for x in items if x["d"] == d]
    md.append("| %s | Q%d〜Q%d | %d | ／%d | %% | 80%%以上 |" % (DOMAINS[d], ids[0], ids[-1], len(ids), len(ids)))
md.append("| 合計 | | %d | ／%d | %% | 80%%以上（※スケールスコア720は正答率と1対1対応しない。目安として余裕を持つ） |" % (len(items), len(items)))
md.append("\n### 9.3 各問の解説\n")
for it in items:
    md.append("#### Q%d 正解：%s（%s ／ タスク%s）" % (it["id"], "・".join(it["answer"]), DOMAINS[it["d"]], it["task"]))
    md.append("")
    for k, c in enumerate(it["choices"]):
        md.append("- %s **%s.** %s" % ("✅" if c["ok"] else "❌", L[k], c["why"]))
    md.append("")
mock_md = "\n".join(md) + "\n---\n\n"

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
