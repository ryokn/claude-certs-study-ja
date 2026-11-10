# -*- coding: utf-8 -*-
import json, random, sys
from collections import Counter
from questions import Q
DN = {1:"分野1 ソリューション設計とアーキテクチャ",2:"分野2 Claudeモデル、プロンプト作成、コンテキストエンジニアリング",3:"分野3 統合",
      4:"分野4 評価、テスト、最適化",5:"分野5 ガバナンス、安全性、リスク管理",6:"分野6 ステークホルダーとのコミュニケーションとライフサイクル管理",7:"分野7 開発者の生産性と運用支援"}
W = {1:17,2:13,3:19,4:16,5:14,6:14,7:7}
L = "ABCDEFG"
# 単一選択の正解位置（0=A）。単一27問は A7 / B7 / C7 / D6。
# 複数選択は multi_pos（Q の index）へ正解を置く。3問連続で同じ正解文字にしない。
targets = [1,3,0,2,1,0, 2,0,3,1,2,0, 0,3,1,2, 0,3,1,0, 2,0,3,1, 2,0,3,1, 2,0]
multi_pos = {5: [2, 4], 12: [1, 3], 19: [0, 3]}
# 同一問の選択肢長の許容差（文字数）。これを超える、または正解だけが最長/最短ならビルドしない。
SPREAD_MAX = 8

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
    if dict(domains)!={1:5,2:4,3:6,4:5,5:4,6:4,7:2}:
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

HTML模試を解き終えたら、初めて見る問題で実力を確認するために次を使ってください（2026年11月3日時点の情報。価格は変動します）。

**公式**

- 試験ガイド §8 のサンプル問題（3問）：公式の練習問題はこれだけです。本ガイドには要点のみを載せているので、問題そのものは公式ガイドで解いてください。

**日本語（優先）**

- [CCAR-P 難問ドリル（みのるん氏）](https://html-files.minoruonda.com/public/ccarp-drill-share/index.html)：無料・日本語63問
- [日本語受験対応 CCAR-P 問題集（Yota Arahata氏・Udemy）](https://www.udemy.com/course/claude-architect-professional-jp-ay/)：有料（¥3,600前後）・日本語378問

**英語**

- [ClaudePrep（termidy）](https://claude.termidy.com/)：無料・英語（全問解くには無料登録が必要）

**使い方のコツ**

- 同じ問題を何周もするより、初めて見る問題で9割を安定して取れるかを指標にする。
- 間違えた問題は公式ドキュメントで裏付けを取り、本ガイドの該当分野を読み直す。
- 外部の問題集は非公式なので、解説の誤りや古い仕様に注意する（本ガイドの「要確認」項目も参照）。
- 実際の試験問題を流出させた「dump」系サイト（例：ITExamsPro.com）は受験規約違反で、合格取り消しや受験禁止のリスクがあるため使わない。
"""
md=["## 9. 模擬試験（HTML版）\n",
    f"模擬試験（{len(out)}問・解答と解説つき）は `ccar-p-mock-exam.html` で解いてください。目安時間は57分です。分野別スコアもHTML上で自動集計されます。\n",
    extra,
    "---\n"]
body=open('part1.md').read()+open('part2.md').read()+"\n"+"\n".join(md)+"\n"+open('part4.md').read()
open('../ccar-p-study-guide.md','w').write(body)

# ---- HTML ----
html=open('template.html').read().replace('/*__DATA__*/[]', json.dumps(out,ensure_ascii=False)).replace('/*__DN__*/{}', json.dumps({str(k):v for k,v in DN.items()},ensure_ascii=False))
open('../ccar-p-mock-exam.html','w').write(html)
print("ok", Counter(len(x['ans']) for x in out), Counter(tuple(L[a] for a in x['ans']) for x in out))
