# CLAUDE.md — CCAR-F 解説動画シリーズ（Claude Code 用）

このキットで Videos 2–11 を、承認済みの第1回スタイルで制作する。
**公開・アップロード・GitHub push・Release 作成はしない。** ローカルで mp4 と chapters.txt まで作って報告する。

## 0. シリーズ対応表

| Video | ディレクトリ | 旧エピソード | 状態 |
|------|--------------|--------------|------|
| 1 | `episodes/ep01/` | ep00 + ep01 | **DONE**（`script.md` が手本） |
| 2 | `episodes/ep02/` | ep02 | 未作成 |
| 3 | `episodes/ep03/` | ep03 | 未作成 |
| 4 | `episodes/ep04/` | ep04 | 未作成 |
| 5 | `episodes/ep05/` | ep05 | 未作成 |
| 6 | `episodes/ep06/` | ep06 | 未作成 |
| 7 | `episodes/ep07/` | ep07 | 未作成 |
| 8 | `episodes/ep08/` | ep08 | 未作成 |
| 9 | `episodes/ep09/` | ep09 | 未作成 |
| 10 | `episodes/ep10/` | ep10（シナリオ） | 未作成 |
| 11 | `episodes/ep11/` | ep11 + ep12 | 未作成 |

素材: 各 `episodes/epNN/source/`、横断参照 `episodes/guide.md` / `episodes/outline.md` / `episodes/old_episodes.tsv`。

## 1. Linear（使えるとき）

チーム **RYO**、プロジェクト **「CCAR-F 解説動画シリーズ」**。issue タイトルは **「CCAR-F #NN …」**（NN は Video 番号、ゼロ埋め2桁）。

Linear MCP / Linear ツールが Claude Code で使える場合:

1. **開始時**: issue「CCAR-F #NN」を検索し、状態を **In Progress** にする。
2. **完了時**: 状態を **Done** にする（自信がなければ **In Review**）。コメントに次を書く:
   - 動画の長さ（分:秒）
   - `chapters.txt` の全文
   - 台本中の「要確認」点の箇条書き

Linear が未接続ならスキップしてよい。接続手順は `setup_mac.md`（公式: `claude mcp add --transport http linear-server https://mcp.linear.app/mcp`）。

## 2. 1本あたりの作業フロー（トークン節約）

1. 該当 `episodes/epNN/README.md` と `source/`、必要なら guide の該当節を読む。
2. **一度で** 目標尺（約10分）の `script.md` を書く。短い言い換えの連続・冗長な前置きは書かない。やり直し前提で下書きを重ねない。
3. `python3 tools/build_episode.py episodes/epNN` を実行。
4. 確認は **数枚のフレーム画像だけ**（例: `build/slides/01.png` と、左右フォーカスが切り替わる1枚、エンドカード直前）。動画全体の連続視聴や大量スクリーンショットはしない。
5. 長さ・`chapters.txt`・要確認を報告（Linear があればコメント）。

エントリコマンド:

```bash
python3 tools/build_episode.py episodes/epNN
# デバッグ:
python3 tools/build_episode.py episodes/epNN --slides-only
python3 tools/build_episode.py episodes/epNN --max-slides 2
```

出力: `episodes/epNN/ccar-f-sNN.mp4` と `episodes/epNN/chapters.txt`。
VOICEVOX: 環境変数 `VOICEVOX_URL`（既定 `http://127.0.0.1:50021`）。

## 3. 台本フォーマット（`episodes/ep01/script.md` が正）

- 先頭に HTML コメントで出典・注意。
- 各スライド:

```markdown
## SLIDE: 第N章　タイトル
@code_label: 左パネル見出し
@diagram: <type> | <右パネル見出し>
# type = flow | table | ba | struct | branch | grid
@node: ...          # flow
@cols: A | B        # table
@row: 項目 | A値 | B値
@before: タグ | 文   # ba
@after: タグ | 文
@result: ...
@from: ...          # struct
@to: ...
@items: a | b | c | ...
@root: ...          # branch
@branches: 左 | 右
@shared: ...
@card: タイトル | 本文   # grid（複数行可）
@note: 補足帯（任意）
@yt: YouTubeチャプター名  # 任意。無い場合は章の先頭スライドだけ自動で chapters に入る
```text
左パネルのコード／設定例
```
[L] ずんだもん: セリフ…
[R] めたん: セリフ…
[R:2] ずんだもん: 整理図でカードを2枚まで表示して話すとき
```

- 読み分け: `{表示|読み}`（例: `{FAQ|エフエーキュー}`）。
- 話者: `ずんだもん`（解説）/ `めたん`（質問）。エイリアス可。
- **すべてのセリフ行に `[L]` または `[R]`**（どちらをフォーカスするか）。
- 右パネルの話に入る **最初のセリフ** で図の名前を言う（「右の表は…」「右の流れ図は…」）。
- タイトルは `第N章　…` で始める（章内スライド番号ピル用）。
- 自作シナリオ・クイズはタイトルか本文で「（オリジナル）」と分かるようにする。

## 4. 承認済みスタイル（厳守）

画面 1920×1080。

- **上部**: ほぼ全幅のスライドカード。緑の章タイトル帯（タイトル約 **54px**）。右端にスライド番号ピル **`現在 / 章内総枚数` のみ**（進捗バーは付けない）。
- **本編中に VOICEVOX クレジットを出さない。**
- **左パネル**: ダークコード／設定。紫タグ「**具体例**」＋ `@code_label`。コード約 **38px**。
- **右パネル**: 内容に合う図タイプを選ぶ（全部を縦流れ図にしない）:
  - `flow` 流れ図 / `table` 比較表 / `ba` 前後比較 / `struct` 構造図 / `branch` 分岐図 / `grid` 整理図
  - 緑のタイプタグ＋ラベル。
- **フォーカス**: 各セリフの `[L]`/`[R]`。アクティブ側に **8px `#ffb000` 枠** と「**いまココ**」札。非アクティブ側は **薄くしない**（通常表示のまま）。キャラ頭は話者以外を暗くする（従来どおり）。
- **下部**: 字幕ボックス（約 **48px**、最大2行、単語途中で折らない）。左にめたん、右にずんだもんのちび頭（約 **220px**）と名前札。
- **エンドカード** 約4秒:
  - `VOICEVOX:ずんだもん / VOICEVOX:四国めたん`
  - `BGM：昼下がり気分（KK / OpenTracks）`
  - 同じ文言を YouTube 概要欄にも入れる（アップロードはユーザーが行う。こちらからは上げない）。
- **BGM**: 声より **18 LU** 低く。先頭 **2秒** フェードイン、末尾 **3秒** フェードアウト。ライセンス上、音源の単体再配布・AI学習・Content ID 登録は不可 → `assets/bgm/` は gitignore。リモートに載せない。
- **教える順序**: 結論 → 理由 → 具体例 → 試験ではこう問われる。初学者向け。専門用語は初出で一言。同じ説明の繰り返し・言い換えだけの水増しは禁止。
- **尺**: 約 **10分**（複数章OK）。情報量を絞り、長いコードはスライド分割。
- **chapters.txt**: YouTube 用タイムスタンプ付き。ビルドが自動生成（章先頭＋`@yt:`）。必要なら `chapters_plan.txt`（`スライド番号|ラベル`）で上書き。

## 5. 内容上の注意

- 数値・仕様は推測しない。確認できなければ「要確認」。
- **キャンセル／予約変更期限**: ガイドは24時間前、FAQは48時間前 → **48時間前で案内し、要確認と明記**（第1回台本どおり）。
- 公式サンプル問題の問題文は載せない。オリジナル例は明示。
- 旧 `source/script_ep*.md` は旧レイアウト。骨子の参考にし、必ず第1回書式で書き直す。

## 6. 依存

- Python 3 + Pillow（`requirements.txt`）
- ffmpeg / ffprobe
- VOICEVOX Engine（`setup_mac.md`）
- フォント: 同梱 Noto Sans CJK、または macOS ヒラギノ

詳細セットアップは `setup_mac.md`。クレジットは `CREDITS.md`。
