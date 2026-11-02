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

from collections import Counter
# ---- Markdown（模擬試験・解答・解説はHTMLに集約。.md には案内だけを入れる） ----
md=["## 9. 模擬試験（HTML版）\n",
    f"模擬試験（{len(out)}問・解答と解説つき）は `ccar-p-mock-exam.html` で解いてください。目安時間は57分です。分野別スコアもHTML上で自動集計されます。\n",
    "---\n"]
body=open('part1.md').read()+open('part2.md').read()+"\n"+"\n".join(md)+"\n"+open('part4.md').read()
open('../ccar-p-study-guide.md','w').write(body)

# ---- HTML ----
html=open('template.html').read().replace('/*__DATA__*/[]', json.dumps(out,ensure_ascii=False)).replace('/*__DN__*/{}', json.dumps({str(k):v for k,v in DN.items()},ensure_ascii=False))
open('../ccar-p-mock-exam.html','w').write(html)
print("ok", Counter(len(x['ans']) for x in out), Counter(tuple(x['ans']) for x in out))
