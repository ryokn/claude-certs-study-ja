# -*- coding: utf-8 -*-
import json, random
from questions import Q
DN = {1:"分野1 ソリューション設計とアーキテクチャ",2:"分野2 Claudeモデル、プロンプト作成、コンテキストエンジニアリング",3:"分野3 統合",
      4:"分野4 評価、テスト、最適化",5:"分野5 ガバナンス、安全性、リスク管理",6:"分野6 ステークホルダーとのコミュニケーションとライフサイクル管理",7:"分野7 開発者の生産性と運用支援"}
W = {1:17,2:13,3:19,4:16,5:14,6:14,7:7}
L = "ABCDEFG"
# 単一選択の正解位置をあらかじめ分散させる（ABCD をほぼ均等に）
targets = [1,3,0,2,2,0,3,1,0,2,1,3,3,1,2,0,1,0,2,3,0,3,1,2,2,1,0,3,1,2]
out=[]
for i,x in enumerate(Q):
    n=len(x['opts']); idx=list(range(n))
    if len(x['ans'])==1:
        t=targets[i]%n
        rest=[k for k in idx if k!=x['ans'][0]]; random.Random(100+i).shuffle(rest)
        order=rest[:t]+[x['ans'][0]]+rest[t:]
    else:
        order=idx[:]; random.Random(200+i).shuffle(order)
    opts=[x['opts'][k] for k in order]
    ans=sorted(order.index(a) for a in x['ans'])
    out.append(dict(no=i+1,d=x['d'],dn=DN[x['d']],multi=len(ans)>1,pick=len(ans),stem=x['stem'],
                    opts=[o[0] for o in opts],notes=[o[1] for o in opts],ans=ans,why=x['why'],src=x['src']))
json.dump(out,open('questions.json','w'),ensure_ascii=False,indent=1)

# ---- Markdown ----
md=[]
md.append("## 9. 模擬試験（30問・目安57分）\n")
md.append("> 本番のペース（120分/63問 ≒ 1問1.9分）に合わせ、**30問を57分**で解いてください。問題は分野の配点に比例して配分しています（分野3：6問、分野1：5問、分野4：5問、分野5：4問、分野6：4問、分野2：4問、分野7：2問）。【2つ選んでください】と書かれた問題は、選んだものがすべて一致したときだけ正解です。HTML版（ccar-p-mock-exam.html）も同じ問題です。\n")
for x in out:
    md.append(f"**問{x['no']}**（{x['dn']}）{'【複数選択：'+str(x['pick'])+'つ】' if x['multi'] else ''}  \n{x['stem']}\n")
    for j,o in enumerate(x['opts']): md.append(f"- {L[j]}. {o}")
    md.append("")
md.append("---\n\n## 10. 解答・分野別スコア表・解説\n")
md.append("### 10-1. 解答一覧\n")
md.append("| 問 | 正解 | 分野 | 問 | 正解 | 分野 | 問 | 正解 | 分野 |\n|---|---|---|---|---|---|---|---|---|")
for r in range(10):
    cells=[]
    for c in range(3):
        x=out[c*10+r]; cells+= [str(x['no']), ",".join(L[a] for a in x['ans']), str(x['d'])]
    md.append("| "+" | ".join(cells)+" |")
from collections import Counter
cnt=Counter(x['d'] for x in out)
md.append("\n### 10-2. 分野別スコア表（自己採点用）\n")
md.append("| 分野 | 配点 | 問題番号 | 問題数 | 正解数 | 正答率 |\n|---|---|---|---|---|---|")
for d in [3,1,4,5,6,2,7]:
    nos=",".join(str(x['no']) for x in out if x['d']==d)
    md.append(f"| {DN[d]} | {W[d]}% | {nos} | {cnt[d]} | ／{cnt[d]} | ％ |")
md.append("| 合計 | 100% |  | 30 | ／30 | ％ |")
md.append("\n> 目安：**全体で80%（24問）以上**、各分野で60%以上を目標にしてください（本番のスケールスコア720は正答率72%を意味しない【要確認】。余裕を持たせた目安です）。正答率が低い分野は、第1〜7章の該当する章を読み直してください。\n")
md.append("### 10-3. 各問の解説\n")
for x in out:
    md.append(f"**問{x['no']}　正解：{','.join(L[a] for a in x['ans'])}**（{x['dn']}）  ")
    md.append(f"{x['why']}  ")
    for j,nt in enumerate(x['notes']):
        mark="○" if j in x['ans'] else "×"
        md.append(f"- {mark} {L[j]}：{nt}")
    md.append(f"- 出典：{x['src']}\n")
md.append("---\n")
body=open('part1.md').read()+open('part2.md').read()+"\n".join(md)+"\n"+open('part4.md').read()
open('../ccar-p-study-guide.md','w').write(body)

# ---- HTML ----
html=open('template.html').read().replace('/*__DATA__*/[]', json.dumps(out,ensure_ascii=False)).replace('/*__DN__*/{}', json.dumps({str(k):v for k,v in DN.items()},ensure_ascii=False))
open('../ccar-p-mock-exam.html','w').write(html)
print("ok", Counter(len(x['ans']) for x in out), Counter(tuple(x['ans']) for x in out))
