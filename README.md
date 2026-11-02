# Claude 認定資格 学習パック（日本語）

Anthropic の Claude 認定資格 **CCDV-F / CCAR-F / CCAR-P** 向けの日本語学習ガイドと模擬試験です。
試験ガイド **v1.0** に基づいて作成しています（**2026/12/7 の改訂前**の内容）。

## 推奨学習順序

| 順番 | 資格 | 目標日 |
|---|---|---|
| 1 | CCDV-F | 〜11/10 |
| 2 | CCAR-F | 〜11/16 |
| 3 | CCAR-P | 〜11/20–24 |

## ファイル一覧

| パス | 内容 |
|---|---|
| `ccdv-f/ccdv-f-study-guide.md` | CCDV-F 学習ガイド（各分野の解説・公式サンプル問題の要点・直前チェックリスト・出典。模擬試験は含まずHTMLを案内） |
| `ccdv-f/ccdv-f-mock-exam.html` | CCDV-F 模擬試験（30問、インタラクティブHTML。解答・解説・分野別スコアつき） |
| `ccdv-f/build/` | CCDV-F 生成スクリプト・問題データ・テンプレート |
| `ccar-f/ccar-f-study-guide.md` | CCAR-F 学習ガイド（各分野の解説・公式サンプル問題の要点・直前チェックリスト・出典。模擬試験は含まずHTMLを案内） |
| `ccar-f/ccar-f-mock-exam.html` | CCAR-F 模擬試験（32問、インタラクティブHTML。解答・解説・分野別スコアつき） |
| `ccar-f/build/` | CCAR-F 生成スクリプト・問題データ・テンプレート |
| `ccar-p/ccar-p-study-guide.md` | CCAR-P 学習ガイド（各分野の解説・公式サンプル問題の要点・直前チェックリスト・出典。模擬試験は含まずHTMLを案内） |
| `ccar-p/ccar-p-mock-exam.html` | CCAR-P 模擬試験（30問、インタラクティブHTML。解答・解説・分野別スコアつき） |
| `ccar-p/build/` | CCAR-P 生成スクリプト・問題データ・テンプレート |

> 📝 模擬試験の問題・解答・解説はすべて HTML に集約しています（学習ガイド .md には含めていません）。

> ⚠️ 模擬試験の問題はすべてオリジナルで作成したものであり、**実際の試験問題ではありません**。

## 模擬試験（HTML）の開き方

このリポジトリは **プライベート** のため、GitHub Pages や直接リンクでは表示できません。
各 `*-mock-exam.html` を GitHub 上で開き、**Raw** または **Download** でローカルに保存してから、ブラウザで開いてください。

## 再生成方法

公式資料（PDF等）は著作権の都合で含めていません（`src/` と `*.pdf` は `.gitignore` 済み）。
```bash
cd ccdv-f/build && python3 gen.py     # CCDV-F
cd ccar-f/build && python3 build.py   # CCAR-F
cd ccar-p/build && python3 gen.py     # CCAR-P
```
各スクリプトが問題データ（`questions.py` / `questions.json` / `items.json`）とテンプレート・Markdown部品から学習ガイド（.md）と模擬試験HTMLを生成します。模擬試験の問題・解答・解説は HTML にだけ出力され、.md には案内文だけが入ります。
