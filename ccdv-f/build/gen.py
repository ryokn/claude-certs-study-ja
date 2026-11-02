# -*- coding: utf-8 -*-
import json, random, re, html
from questions import Q, DOMAINS
random.seed(20261110)
LET = "ABCD"
# 問題順を混ぜる（分野が偏らないように）
qs = Q[:]
random.shuffle(qs)
# 選択肢を並べ替えて正解位置を均す
target = (["A","B","C","D"]*8)[:30]; random.shuffle(target)
out = []
for i, x in enumerate(qs):
    keys = list(x["choices"].keys())
    ans = x["answer"]
    others = [k for k in keys if k not in ans]
    random.shuffle(others)
    t = target[i]
    order = others[:]
    # 先頭の正解を target の位置に置き、残りの正解はランダムな位置に入れる
    order.insert(LET.index(t), ans[0])
    for a in ans[1:]:
        order.insert(random.randint(0, len(order)), a)
    m = {old: LET[j] for j, old in enumerate(order)}
    out.append(dict(
        n=i+1, domain=x["domain"], dname=DOMAINS[x["domain"]], skill=x["skill"], q=x["q"],
        multi=len(ans) > 1,
        choices=[[m[k], x["choices"][k]] for k in order],
        answer=sorted(m[a] for a in ans),
        why=x["why"],
        wrong=sorted([[m[k], v] for k, v in x["wrong"].items()]),
    ))
json.dump(out, open("questions.json", "w"), ensure_ascii=False, indent=1)

# ---------- Markdown ----------
md = []
md.append("## 10. 模擬試験（30問・目標65分）\n")
md.append("- 分野ごとの出題数は配点比率に合わせています（分野2:10、分野5:5、分野1:4、分野6:3、分野8:3、分野7:3、分野3:1、分野4:1）。")
md.append("- 【2つ選択】と書かれた問題は、2つとも正しく選んで正解です（部分点はなし）。それ以外は1つ選択です。")
md.append("- 合格の目安（独自の基準）：**8割（24問）以上**。本番はスケールスコアのため、正答率とは直接対応しません。\n")
for x in out:
    tag = "【2つ選択】" if x["multi"] else ""
    q = re.sub(r"^【2つ選択】", "", x["q"])
    md.append(f"**問{x['n']}**（{x['dname']}／{x['skill']}）{tag}  \n{q}\n")
    for k, v in x["choices"]:
        md.append(f"- {k}. {v}")
    md.append("")
md.append("\n---\n\n## 11. 解答一覧・分野別スコア表・解説\n")
md.append("### 11-1. 解答一覧\n")
md.append("| 問 | 正解 | 分野 | 問 | 正解 | 分野 | 問 | 正解 | 分野 |\n|---|---|---|---|---|---|---|---|---|")
for r in range(10):
    cells = []
    for c in range(3):
        x = out[r + c*10]
        cells += [str(x["n"]), ",".join(x["answer"]), x["domain"].replace("D", "分野")]
    md.append("| " + " | ".join(cells) + " |")
md.append("\n### 11-2. 分野別スコア表（自己採点用）\n")
md.append("| 分野 | 問題番号 | 問題数 | 正解数 | 正答率 |\n|---|---|---|---|---|")
for d in ["D2","D5","D1","D6","D8","D7","D3","D4"]:
    ns = [str(x["n"]) for x in out if x["domain"] == d]
    md.append(f"| {DOMAINS[d]} | {', '.join(ns)} | {len(ns)} | ／{len(ns)} | % |")
md.append("| **合計** | | **30** | ／30 | % |\n")
md.append("### 11-3. 各問の解説\n")
for x in out:
    md.append(f"**問{x['n']}　正解：{','.join(x['answer'])}**（{x['dname']}／{x['skill']}）  ")
    md.append(f"- なぜ正解か：{x['why']}")
    for k, v in x["wrong"]:
        md.append(f"- {k} が誤りの理由：{v}")
    md.append("")
open("mock_section.md", "w").write("\n".join(md) + "\n")

# ---------- HTML ----------
tpl = open("template.html").read()
open("../ccdv-f-mock-exam.html", "w").write(tpl.replace("/*__DATA__*/[]", json.dumps(out, ensure_ascii=False)).replace("/*__DOMAINS__*/{}", json.dumps(DOMAINS, ensure_ascii=False)))
print("ok", [x["answer"] for x in out])
