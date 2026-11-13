# -*- coding: utf-8 -*-
"""CCAR-F 模試を questions.py から HTML と items.json へ生成する。

学習ガイド (ccar-f-study-guide.md) と part1.md–part5.md は書き換えない。
模試の問題文と解説は HTML だけに置く。ガイド側の「追加の演習問題」は
part 再連結では再現できないため、ここでガイドを再生成しない。
"""
import json, os, random, sys
from collections import Counter
from questions import Q, DOMAINS, S

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..")
L = "ABCDE"
# 同一問の選択肢文字数の許容差。正解だけが最長・最短になる配置も失敗にする。
SPREAD_MAX = 8
# 単一選択 29 問は A8 / B7 / C7 / D7。複数選択の True は文字列の左から順に対応する。
# どの連続 3 問も、共通の正解位置を持たない。
KEYLETTERS = [
    "B", "D", "A", "BD", "C", "A", "B", "D", "C",
    "A", "B", "D", "C", "AE", "A", "B", "D", "C",
    "A", "B", "D", "C", "A", "CD", "B", "D", "C",
    "A", "B", "D", "C", "A",
]
EXPECTED_DOMAINS = {"D1": 9, "D2": 6, "D3": 6, "D4": 6, "D5": 5}

def place(q, letters, rng):
    ch = list(q["c"])
    cor = [c for c in ch if c[1]]
    oth = [c for c in ch if not c[1]]
    if len(cor) != len(letters):
        raise SystemExit("correct-count != key letters")
    rng.shuffle(oth)
    if len(letters) == 1:
        p = L.index(letters)
        if p > len(oth):
            raise SystemExit("single key out of range")
        return oth[:p] + cor + oth[p:]
    slots = [L.index(ch_) for ch_ in letters]
    if len(set(slots)) != len(slots) or max(slots) >= len(ch):
        raise SystemExit("bad multi slots %s" % letters)
    arr = [None] * len(ch)
    for s, c in zip(slots, cor):
        arr[s] = c
    it = iter(oth)
    return [a if a is not None else next(it) for a in arr]

items = []
if len(Q) != len(KEYLETTERS):
    raise SystemExit("Q %d != keys %d" % (len(Q), len(KEYLETTERS)))
for i, q in enumerate(Q):
    letters = KEYLETTERS[i]
    multi = q.get("multi", 1)
    if multi != len(letters):
        raise SystemExit("Q%d multi %s != %r" % (i + 1, multi, letters))
    ch = place(q, letters, random.Random(1000 + i))
    items.append(dict(
        id=i + 1, d=q["d"], task=q["task"], scenario=S[q["s"]], q=q["q"].strip(),
        multi=multi, choices=[{"t": c[0], "ok": c[1], "why": c[2]} for c in ch],
    ))
for it in items:
    it["answer"] = [L[k] for k, c in enumerate(it["choices"]) if c["ok"]]

def validate(items):
    problems = []
    if len(items) != 32:
        problems.append("count %d" % len(items))
    domains = Counter(it["d"] for it in items)
    if dict(domains) != EXPECTED_DOMAINS:
        problems.append("domains %s" % dict(domains))
    tasks = [it["task"] for it in items]
    if tasks != [
        "1.1", "1.2", "1.3", "1.3", "1.4", "1.5", "1.5", "1.6", "1.7",
        "2.1", "2.2", "2.3", "2.3", "2.4", "2.5",
        "3.1", "3.2", "3.3", "3.4", "3.5", "3.6",
        "4.1", "4.2", "4.3", "4.4", "4.5", "4.6",
        "5.1", "5.2", "5.4", "5.5", "5.6",
    ]:
        problems.append("task order changed")
    c_lens, w_lens = [], []
    single = Counter()
    sets = []
    for it in items:
        ls = [len(c["t"]) for c in it["choices"]]
        ans = {i for i, c in enumerate(it["choices"]) if c["ok"]}
        if it["multi"] == 1 and len(it["choices"]) != 4:
            problems.append("Q%d single choices %d" % (it["id"], len(it["choices"])))
        if it["multi"] > 1 and len(it["choices"]) != 5:
            problems.append("Q%d multi choices %d" % (it["id"], len(it["choices"])))
        if len(ans) != it["multi"]:
            problems.append("Q%d answer count" % it["id"])
        if it["multi"] > 1 and "2つ" not in it["q"]:
            problems.append("Q%d stem does not say how many to pick" % it["id"])
        for i, ln in enumerate(ls):
            (c_lens if i in ans else w_lens).append(ln)
        mx, mn = max(ls), min(ls)
        long_i = [i for i, ln in enumerate(ls) if ln == mx]
        short_i = [i for i, ln in enumerate(ls) if ln == mn]
        flags = []
        if len(ans) == 1 and len(long_i) == 1 and long_i[0] in ans:
            flags.append("unique-longest-correct")
        if len(ans) == 1 and len(short_i) == 1 and short_i[0] in ans:
            flags.append("unique-shortest-correct")
        if len(ans) > 1:
            wrong = [ls[i] for i in range(len(ls)) if i not in ans]
            corr = [ls[i] for i in ans]
            if wrong and min(corr) > max(wrong):
                flags.append("corrects-strictly-longer")
        if mx - mn > SPREAD_MAX:
            flags.append("spread-%d" % (mx - mn))
        if any(not c["t"].strip() or len(c["why"].strip()) < 20 for c in it["choices"]):
            flags.append("empty-choice-or-why")
        if len(set(c["t"] for c in it["choices"])) != len(it["choices"]):
            flags.append("duplicate-choice")
        if flags:
            problems.append("Q%d %s lens=%s" % (it["id"], flags, ls))
        sets.append(frozenset(i for i, c in enumerate(it["choices"]) if c["ok"]))
        if it["multi"] == 1:
            single[it["answer"][0]] += 1
        if "".join(it["answer"]) != KEYLETTERS[it["id"] - 1]:
            problems.append("Q%d placed %s != %s" % (it["id"], "".join(it["answer"]), KEYLETTERS[it["id"] - 1]))
    for i in range(len(sets) - 2):
        inter = sets[i] & sets[i + 1] & sets[i + 2]
        if inter:
            problems.append("run Q%d-Q%d share %s" % (i + 1, i + 3, sorted(L[k] for k in inter)))
    if single and (max(single.values()) - min(single.values()) > 1 or set(single) != set("ABCD")):
        problems.append("single balance %s" % dict(single))
    stats = dict(
        n=len(items),
        mean_correct=round(sum(c_lens) / len(c_lens), 2) if c_lens else None,
        mean_wrong=round(sum(w_lens) / len(w_lens), 2) if w_lens else None,
        max_spread=max((max(len(c["t"]) for c in it["choices"]) - min(len(c["t"]) for c in it["choices"])) for it in items),
        single=dict(single),
        unique_longest_correct=sum(
            1 for it in items
            if it["multi"] == 1 and (lambda ls, ans: len([i for i, ln in enumerate(ls) if ln == max(ls)]) == 1 and [i for i, ln in enumerate(ls) if ln == max(ls)][0] in ans)(
                [len(c["t"]) for c in it["choices"]], {i for i, c in enumerate(it["choices"]) if c["ok"]}
            )
        ),
    )
    return problems, stats

problems, stats = validate(items)
print("stats", stats)
print("answers", Counter(a for it in items for a in it["answer"]))
if problems:
    print("FAILED", len(problems))
    for p in problems:
        print(p)
    sys.exit(1)

dshort = {
    "D1": "分野1 エージェント",
    "D2": "分野2 ツール/MCP",
    "D3": "分野3 Claude Code",
    "D4": "分野4 プロンプト/構造化",
    "D5": "分野5 コンテキスト/信頼性",
}
tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
data = {"items": items, "domains": DOMAINS, "dshort": dshort, "targetMin": len(items) * 2}
js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
html = tpl.replace("/*__DATA__*/null", js)
if "ccarf-mock-v20261114" not in html:
    raise SystemExit("localStorage key was not bumped")
open(os.path.join(OUT, "ccar-f-mock-exam.html"), "w", encoding="utf-8").write(html)
json.dump(items, open(os.path.join(HERE, "items.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", len(items), "items")
