# -*- coding: utf-8 -*-
import json, random, sys
from collections import Counter
from questions import Q
DN = {1:"分野1 高度なエージェントアーキテクチャとオーケストレーション",2:"分野2 本番環境の統合、信頼性、知識グラウンディング",
      3:"分野3 オブザーバビリティと本番環境のモニタリング",4:"分野4 高度なデバッグとインシデント対応",5:"分野5 評価エンジニアリングと品質保証",
      6:"分野6 大規模環境でのコストとレイテンシの最適化",7:"分野7 ランタイムガードレールと本番環境のセキュリティ",8:"分野8 ソフトウェア提供のためのエージェントフリート運用"}
W = {1:17,2:20,3:12,4:10,5:12,6:8,7:11,8:10}
L = "ABCDEFG"
# 単一選択の正解位置（0=A）。単一27問は A7 / B7 / C7 / D6。
# 複数選択は multi_pos（Q の index）へ正解を置く。3問連続で同じ正解文字にしない。
# 問題の並び：分野2(Q1-6) 分野1(Q7-11) 分野3(Q12-15) 分野5(Q16-19) 分野7(Q20-22) 分野4(Q23-25) 分野8(Q26-28) 分野6(Q29-30)
targets = [1,3,0,1,0,2, 3,0,2,1,0, 0,3,1,2, 0,2,3,1, 0,0,3, 2,1,0, 3,2,0, 1,2]
multi_pos = {2: [0, 2], 11: [1, 2], 19: [2, 4]}
# 同一問の選択肢長の許容差（文字数）。これを超える、または正解だけが最長/最短ならビルドしない。
# CCDV-P は選択肢が長め（50〜65字）なので許容差を12字にしている。
SPREAD_MAX = 12

out=[]
for i,x in enumerate(Q):
    n=len(x['opts']); idx=list(range(n))
    if len(x['ans'])==1:
        t=targets[i]%n
        rest=[k for k in idx if k!=x['ans'][0]]; random.Random(100+i).shuffle(rest)
        order=rest[:t]+[x['ans'][0]]+rest[t:]
    else:
        if sorted(x['ans'])!=list(range(len(x['ans']))):
            raise SystemExit(f"Q source {i+1}: multi ans must be the leading options {x['ans']}")
        slots=multi_pos[i]
        if len(slots)!=len(x['ans']) or any(s<0 or s>=n for s in slots):
            raise SystemExit(f"Q source {i+1}: bad multi_pos {slots} for n={n}")
        wrong=[k for k in idx if k not in x['ans']]
        random.Random(200+i).shuffle(wrong)
        order=[None]*n
        for s,a in zip(sorted(slots), x['ans']):
            order[s]=a
        wi=0
        for j in range(n):
            if order[j] is None:
                order[j]=wrong[wi]; wi+=1
    opts=[x['opts'][k] for k in order]
    ans=sorted(order.index(a) for a in x['ans'])
    out.append(dict(no=i+1,d=x['d'],dn=DN[x['d']],multi=len(ans)>1,pick=len(ans),stem=x['stem'],
                    opts=[o[0] for o in opts],notes=[o[1] for o in opts],ans=ans,why=x['why'],src=x['src']))

def validate(items):
    problems=[]
    if len(items)!=30:
        problems.append(f"count {len(items)}")
    domains=Counter(q['d'] for q in items)
    if dict(domains)!={2:6,1:5,3:4,5:4,7:3,4:3,8:3,6:2}:
        problems.append(f"domains {dict(domains)}")
    multis=[q for q in items if q['multi']]
    if len(multis)!=3:
        problems.append(f"multi count {len(multis)}")
    for q in multis:
        if q['pick']!=2 or '2つ' not in q['stem']:
            problems.append(f"Q{q['no']} multi stem/pick")
    c_lens=[]; w_lens=[]
    single=Counter(); sets=[]
    for q in items:
        ls=[len(o) for o in q['opts']]
        ans=set(q['ans'])
        for i,l in enumerate(ls):
            (c_lens if i in ans else w_lens).append(l)
        mx,mn=max(ls),min(ls)
        long_i=[i for i,l in enumerate(ls) if l==mx]
        short_i=[i for i,l in enumerate(ls) if l==mn]
        flags=[]
        if len(long_i)==1 and long_i[0] in ans:
            flags.append('unique-longest-correct')
        if len(ans)==1 and len(short_i)==1 and short_i[0] in ans:
            flags.append('unique-shortest-correct')
        if len(ans)>1:
            wrong=[ls[i] for i in range(len(ls)) if i not in ans]
            corr=[ls[i] for i in ans]
            if wrong and min(corr)>max(wrong):
                flags.append('corrects-strictly-longer')
        if mx-mn>SPREAD_MAX:
            flags.append(f'spread-{mx-mn}')
        if len(q['opts'])!=len(q['notes']) or not q['why'] or not q['src']:
            flags.append('missing-note-or-why')
        if flags:
            problems.append(f"Q{q['no']} {flags} lens={ls}")
        sets.append(frozenset(q['ans']))
        if not q['multi']:
            single[L[q['ans'][0]]]+=1
    for i in range(len(sets)-2):
        inter=sets[i]&sets[i+1]&sets[i+2]
        if inter:
            problems.append(f"run Q{i+1}-Q{i+3} share {sorted(inter)}")
    if single and (max(single.values())-min(single.values())>1 or len(single)<4):
        problems.append(f"single balance {dict(single)}")
    stats=dict(n=len(items), mean_correct=round(sum(c_lens)/len(c_lens),2), mean_wrong=round(sum(w_lens)/len(w_lens),2),
               single=dict(single), multi=Counter(tuple(L[a] for a in q['ans']) for q in items if q['multi']))
    return problems, stats

problems, stats = validate(out)
print("stats", stats)
if problems:
    print("FAILED", len(problems))
    for p in problems:
        print(p)
    sys.exit(1)

json.dump(out,open('questions.json','w'),ensure_ascii=False,indent=1)

# ---- Markdown（模擬試験・解答・解説はHTMLに集約。.md には案内だけを入れる） ----
# 外部リソース節は学習ガイドに既にある案内。再生成で落とさない。
extra = """### 追加の演習問題（外部リソース）

HTML模試を解き終えたら、初めて見る問題で実力を確認するために次を使ってください（2026年11月20日時点の情報）。

**公式**

- 試験ガイド §7 のサンプル問題（3問）：公式の練習問題はこれだけです（公式の模擬試験は見つかっていません：要確認）。本ガイドの第9章には要点だけを載せているので、問題そのものは公式ガイドで解いてください。
- [公式の準備コース（Partner 向けラーニングパス）](https://anthropic-partners.skilljar.com/path/claude-certified-developer-professional)：各コースの確認問題も演習として使えます。

**非公式の問題集**

- CCDV-P は公開されたばかりで、2026年11月20日時点では信頼できる日本語の問題集を確認できていません（要確認）。見つけた場合も、下の注意点を守って使ってください。

**使い方のコツ**

- 同じ問題を何周もするより、初めて見る問題で9割を安定して取れるかを指標にする。
- 間違えた問題は公式ドキュメントで裏付けを取り、本ガイドの該当分野を読み直す。
- 外部の問題集は非公式なので、解説の誤りや古い仕様に注意する（本ガイドの「要確認」項目も参照）。
- 実際の試験問題を流出させた「dump」系サイトは受験規約違反で、合格取り消しや受験禁止のリスクがあるため使わない。
"""
md=["## 10. 模擬試験（HTML版）\n",
    f"模擬試験（{len(out)}問・解答と解説つき）は `ccdv-p-mock-exam.html` で解いてください。目安時間は51分です（本番の120分÷70問≒1.7分/問）。分野別スコアもHTML上で自動集計されます。\n",
    extra,
    "---\n"]
body=open('part1.md').read()+open('part2.md').read()+"\n"+"\n".join(md)+"\n"+open('part4.md').read()
open('../ccdv-p-study-guide.md','w').write(body)

# ---- HTML ----
html=open('template.html').read().replace('/*__DATA__*/[]', json.dumps(out,ensure_ascii=False)).replace('/*__DN__*/{}', json.dumps({str(k):v for k,v in DN.items()},ensure_ascii=False))
open('../ccdv-p-mock-exam.html','w').write(html)
print("ok", Counter(len(x['ans']) for x in out), Counter(tuple(L[a] for a in x['ans']) for x in out))
