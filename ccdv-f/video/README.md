# CCDV-F 対話解説動画（全12回）

[`../ccdv-f-study-guide.md`](../ccdv-f-study-guide.md) をもとに、ずんだもん（解説役）と四国めたん（質問役）の対話形式で解説する動画の台本とビルドスクリプトです。

- **動画はリポジトリには含めず、GitHub Release で配布しています**：[https://github.com/ryokn/claude-certs-study-ja/releases/tag/ccdv-f-videos-v1](https://github.com/ryokn/claude-certs-study-ja/releases/tag/ccdv-f-videos-v1)
- 各回は約6〜8分（第0回は約5分）、合計約75分。各回にひっかけクイズ・まとめ・次回予告あり
- 内容は学習ガイドに基づいています。自作のシナリオ問題はスライドタイトルに（オリジナル）と表記
- 音声：VOICEVOX:ずんだもん / VOICEVOX:四国めたん（画面右下に常時表示）

## エピソード一覧

| 回 | タイトル | 長さ | 台本 | 動画（直接ダウンロード） |
|---|---|---|---|---|
| 0 | 試験概要と使い方 | 5:26 | [script_ep00.md](script_ep00.md) | [ccdv-f-ep00.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-f-videos-v1/ccdv-f-ep00.mp4) |
| 1 | 分野2 ― 1-1 Claude APIの仕組み | 7:53 | [script_ep01.md](script_ep01.md) | [ccdv-f-ep01.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-f-videos-v1/ccdv-f-ep01.mp4) |
| 2 | 分野2 ― 1-2 Claudeアプリケーションの設計／1-3 ソフトウェアエンジニアリングの基礎 | 6:05 | [script_ep02.md](script_ep02.md) | [ccdv-f-ep02.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-f-videos-v1/ccdv-f-ep02.mp4) |
| 3 | 分野2 ― 1-4 構成管理／1-5 要件の理解／1-6 システムライフサイクル | 6:17 | [script_ep03.md](script_ep03.md) | [ccdv-f-ep03.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-f-videos-v1/ccdv-f-ep03.mp4) |
| 4 | 分野5 ― モデルの選択と最適化 | 6:07 | [script_ep04.md](script_ep04.md) | [ccdv-f-ep04.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-f-videos-v1/ccdv-f-ep04.mp4) |
| 5 | 分野1 ― エージェントとワークフロー | 6:11 | [script_ep05.md](script_ep05.md) | [ccdv-f-ep05.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-f-videos-v1/ccdv-f-ep05.mp4) |
| 6 | 分野6 ― プロンプトとコンテキストのエンジニアリング | 6:10 | [script_ep06.md](script_ep06.md) | [ccdv-f-ep06.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-f-videos-v1/ccdv-f-ep06.mp4) |
| 7 | 分野8 ― ツールとMCP | 6:26 | [script_ep07.md](script_ep07.md) | [ccdv-f-ep07.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-f-videos-v1/ccdv-f-ep07.mp4) |
| 8 | 分野7 ― セキュリティと安全性 | 5:57 | [script_ep08.md](script_ep08.md) | [ccdv-f-ep08.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-f-videos-v1/ccdv-f-ep08.mp4) |
| 9 | 分野3 Claude Code ／ 分野4 評価、テスト、デバッグ | 6:09 | [script_ep09.md](script_ep09.md) | [ccdv-f-ep09.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-f-videos-v1/ccdv-f-ep09.mp4) |
| 10 | 公式サンプル問題の要点と演習リソース | 6:17 | [script_ep10.md](script_ep10.md) | [ccdv-f-ep10.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-f-videos-v1/ccdv-f-ep10.mp4) |
| 11 | 直前チェックリストと頻出ひっかけ22選 | 5:58 | [script_ep11.md](script_ep11.md) | [ccdv-f-ep11.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-f-videos-v1/ccdv-f-ep11.mp4) |

構成の詳細は [outline.md](outline.md) を参照。

## ファイル構成

| パス | 内容 |
|---|---|
| `script_ep00.md` 〜 `script_ep11.md` | 各回の台本（スライド＋セリフ） |
| `outline.md` | 全12回の構成案 |
| `scripts/render.py` | 台本 → 音声合成 → スライド画像 → mp4 のレンダラー（現行版） |
| `scripts/start_engine.sh` | VOICEVOX エンジン起動スクリプト |
| `scripts/prep_assets.py` | 立ち絵素材の取得・加工（現在は立ち絵非表示のため未使用） |
| `scripts/render_v1_icons.py`, `scripts/render_v2_chars.py` | 旧版（アイコン版／立ち絵版） |
| `assets/CREDITS.md` | 素材クレジットと利用条件 |

## 再ビルド手順

### 必要なもの
- Python 3 + Pillow（`pip install pillow`。立ち絵を使う場合は `psd-tools` も）
- ffmpeg / ffprobe
- フォント：Noto Sans CJK JP / Noto Sans Mono CJK JP（例：`fonts-noto-cjk`）
- [VOICEVOX engine](https://github.com/VOICEVOX/voicevox_engine) 0.26.0（CPU 版で可）を `127.0.0.1:50021` で起動

### 手順
```bash
# 1. VOICEVOX エンジンを起動（start_engine.sh 内のパスは環境に合わせて変更）
bash scripts/start_engine.sh

# 2. 1回分をレンダリング
python3 scripts/render.py script_ep01.md ep01.mp4 --work build_ep01

# 3. 全12回を一括レンダリング
for e in 00 01 02 03 04 05 06 07 08 09 10 11; do
  python3 scripts/render.py script_ep$e.md ep$e.mp4 --work build_ep$e
done
```

- 音声は `build_epNN/wav` にキャッシュされ、セリフを変更した行だけ再合成されます
- 話者：ずんだもん ノーマル（speaker id 3）、四国めたん ノーマル（id 2）、話速 1.2
- 出力：1920×1080、H.264 + AAC
- コードが 28px 未満に縮小されるとログに `WARNING` が出ます（スライド分割の目安）
- 立ち絵を表示する場合は `scripts/render.py` の `SHOW_CHARS = True` にし、`python3 scripts/prep_assets.py` で素材を生成（利用条件は `assets/CREDITS.md`）。画像素材はリポジトリに含めていません

## 台本の書式

````text
## SLIDE: スライドタイトル
> サブタイトル
- 箇条書き（**太字** で強調）
| 表 | ヘッダー |
| 1行目 | 値 |
（``` で囲むとコードブロック）
めたん: 質問のセリフ
ずんだもん: 解説のセリフなのだ。{表示|よみ} で読み方を指定
````
