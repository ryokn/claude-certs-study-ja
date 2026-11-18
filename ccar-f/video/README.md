# CCAR-F 対話解説動画（全13回）

[`../ccar-f-study-guide.md`](../ccar-f-study-guide.md) をもとに、ずんだもん（解説役）と四国めたん（質問役）の対話形式で解説する動画の台本とビルドスクリプトです。

- **動画はリポジトリには含めず、GitHub Release で配布しています**：[https://github.com/ryokn/claude-certs-study-ja/releases/tag/ccar-f-videos-v1](https://github.com/ryokn/claude-certs-study-ja/releases/tag/ccar-f-videos-v1)
- 各回は約5〜8分、合計約88分。各回に確認クイズ・まとめ・次回予告あり。最終回はひっかけ25選のクイズ形式
- 内容は学習ガイド（2026/11/03 作成、公式試験ガイド v1.0 範囲）に基づいています。自作の問題（本ガイドの模擬試験 `../ccar-f-mock-exam.html` から引用したものを含む）はスライドタイトルに（オリジナル）と表記。公式サンプル問題は問題文を載せず要点のみ
- 音声：VOICEVOX:ずんだもん / VOICEVOX:四国めたん（画面右下に常時表示）

## エピソード一覧

| 回 | タイトル | 長さ | 台本 | 動画（直接ダウンロード） |
|---|---|---|---|---|
| 0 | 試験概要と使い方 | 6:52 | [script_ep00.md](script_ep00.md) | [ccar-f-ep00.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v1/ccar-f-ep00.mp4) |
| 1 | 試験ガイドと現行ドキュメントのズレ（新旧名称） | 5:39 | [script_ep01.md](script_ep01.md) | [ccar-f-ep01.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v1/ccar-f-ep01.mp4) |
| 2 | 分野1（その1）エージェントループとサブエージェント | 7:41 | [script_ep02.md](script_ep02.md) | [ccar-f-ep02.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v1/ccar-f-ep02.mp4) |
| 3 | 分野1（その2）強制とハンドオフ、フック、タスク分解、セッション | 6:45 | [script_ep03.md](script_ep03.md) | [ccar-f-ep03.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v1/ccar-f-ep03.mp4) |
| 4 | 分野3（その1）CLAUDE.md、コマンドとスキル、パス固有のルール | 7:39 | [script_ep04.md](script_ep04.md) | [ccar-f-ep04.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v1/ccar-f-ep04.mp4) |
| 5 | 分野3（その2）プランモード、反復的な改良、CI/CD | 6:01 | [script_ep05.md](script_ep05.md) | [ccar-f-ep05.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v1/ccar-f-ep05.mp4) |
| 6 | 分野4（その1）明示的な基準、few-shot、tool_use と JSON スキーマ | 6:14 | [script_ep06.md](script_ep06.md) | [ccar-f-ep06.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v1/ccar-f-ep06.mp4) |
| 7 | 分野4（その2）検証とリトライ、Message Batches API、マルチパスレビュー | 5:55 | [script_ep07.md](script_ep07.md) | [ccar-f-ep07.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v1/ccar-f-ep07.mp4) |
| 8 | 分野2　ツール設計とMCP統合 | 8:03 | [script_ep08.md](script_ep08.md) | [ccar-f-ep08.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v1/ccar-f-ep08.mp4) |
| 9 | 分野5　コンテキスト管理と信頼性 | 7:52 | [script_ep09.md](script_ep09.md) | [ccar-f-ep09.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v1/ccar-f-ep09.mp4) |
| 10 | シナリオ別ウォークスルー（6シナリオ） | 6:06 | [script_ep10.md](script_ep10.md) | [ccar-f-ep10.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v1/ccar-f-ep10.mp4) |
| 11 | 公式サンプル問題12問の要点と演習リソース | 5:14 | [script_ep11.md](script_ep11.md) | [ccar-f-ep11.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v1/ccar-f-ep11.mp4) |
| 12 | 直前チェックリストと高頻出ひっかけ25選 | 7:47 | [script_ep12.md](script_ep12.md) | [ccar-f-ep12.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v1/ccar-f-ep12.mp4) |

構成の詳細は [outline.md](outline.md) を参照。

## ファイル構成

| パス | 内容 |
|---|---|
| `script_ep00.md` 〜 `script_ep12.md` | 各回の台本（スライド＋セリフ） |
| `outline.md` | 全13回の構成案 |
| `scripts/render.py` | 台本 → 音声合成 → スライド画像 → mp4 のレンダラー（CCDV-F 版と同一） |
| `scripts/start_engine.sh` | VOICEVOX エンジン起動スクリプト |
| `scripts/rerender.sh` | 指定した回をバックグラウンドで（再）レンダリング（lint_script.py を実行してから render.py） |
| `scripts/lint_script.py` | 台本の整形：表セル内の `**太字**` 記号を除去（表は太字非対応）、絵文字（✅❌⚠️）をフォントにある記号（○×△）へ置換 |
| `scripts/split_long.py` | 字幕が長すぎるセリフを文末で2つに分割 |
| `scripts/check_frames.py` | 完成した mp4 から各スライドの1フレームを ffmpeg で抜き出し、2×2 のシートにまとめる（目視確認用、`frames_check/`） |
| `scripts/prep_assets.py` | 立ち絵素材の取得・加工（立ち絵非表示のため未使用） |
| `scripts/render_v1_icons.py`, `scripts/render_v2_chars.py` | 旧版（アイコン版／立ち絵版） |
| `assets/CREDITS.md` | 素材クレジットと利用条件 |

## 再ビルド手順

### 必要なもの
- Python 3 + Pillow（`pip install pillow`）
- ffmpeg / ffprobe
- フォント：Noto Sans CJK JP / Noto Sans Mono CJK JP（例：`fonts-noto-cjk`）
- [VOICEVOX engine](https://github.com/VOICEVOX/voicevox_engine) 0.26.0（CPU 版で可）を `127.0.0.1:50021` で起動

### 手順
```bash
# 1. VOICEVOX エンジンを起動（start_engine.sh 内のパスは環境に合わせて変更）
bash scripts/start_engine.sh

# 2. 1回分をレンダリング
python3 scripts/render.py script_ep01.md ep01.mp4 --work build_ep01

# 3. 全13回を一括レンダリング
for e in 00 01 02 03 04 05 06 07 08 09 10 11 12; do
  python3 scripts/render.py script_ep$e.md ep$e.mp4 --work build_ep$e
done

# 4. （任意）フレーム確認シートを作る
python3 scripts/check_frames.py 01   # → frames_check/ep01_sheet*.png
```

- 音声は `build_epNN/wav` にキャッシュされ、セリフを変更した行だけ再合成されます
- 話者：ずんだもん ノーマル（speaker id 3）、四国めたん ノーマル（id 2）、話速 1.2
- 出力：1920×1080、H.264 + AAC。キャラクターの立ち絵は表示しません（`SHOW_CHARS = False`）
- コードが 28px 未満に縮小されるとログに `WARNING` が出ます（スライド分割の目安）

## 台本の書式

````text
## SLIDE: スライドタイトル
> サブタイトル
- 箇条書き（**太字** で強調）
| 表 | ヘッダー |        ← 表のセルでは **太字** は使えない
| 1行目 | 値 |
（``` で囲むとコードブロック。表示順はサブタイトル → コード → 箇条書き → 表）
めたん: 質問のセリフ
ずんだもん: 解説のセリフなのだ。{表示|よみ} で読み方を指定（例：{custom_id|カスタムアイディー}）
````
