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

# ---------- Markdown（模擬試験・解答・解説はHTMLに集約。.md には案内だけを入れる） ----------
note = ("## 10. 模擬試験（HTML版）\n\n"
        "模擬試験（%d問・解答と解説つき）は `ccdv-f-mock-exam.html` で解いてください。"
        "分野別スコアもHTML上で自動集計されます。目標時間は65分です。\n\n---\n\n" % len(out))
guide = open("guide_head.md").read() + note + open("guide_tail.md").read()
open("../ccdv-f-study-guide.md", "w").write(guide)

# ---------- HTML ----------
tpl = open("template.html").read()
open("../ccdv-f-mock-exam.html", "w").write(tpl.replace("/*__DATA__*/[]", json.dumps(out, ensure_ascii=False)).replace("/*__DOMAINS__*/{}", json.dumps(DOMAINS, ensure_ascii=False)))
print("ok", [x["answer"] for x in out])
