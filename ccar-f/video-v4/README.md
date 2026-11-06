# CCAR-F 対話解説動画 v4（全11回）

ずんだもん×四国めたんの対話形式で CCAR-F を解説する新シリーズ（v4 スタイル）。#01 は Grok Bot、#02〜#11 は Mac 上の Claude Code（Orca 経由）で制作。

動画本体は git に含めず Release で配布：https://github.com/ryokn/claude-certs-study-ja/releases/tag/ccar-f-videos-v4

| 回 | 内容 | 長さ | ダウンロード |
|---|---|---|---|
| #01 | 概要と名称変更 | 10:55 | [ccar-f-s01.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v4/ccar-f-s01.mp4) |
| #02 | 分野1（その1） | 7:41 | [ccar-f-s02.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v4/ccar-f-s02.mp4) |
| #03 | 分野1（その2） | 6:59 | [ccar-f-s03.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v4/ccar-f-s03.mp4) |
| #04 | 分野3（その1） | 6:35 | [ccar-f-s04.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v4/ccar-f-s04.mp4) |
| #05 | 分野3（その2） | 5:44 | [ccar-f-s05.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v4/ccar-f-s05.mp4) |
| #06 | 分野4（その1） | 6:02 | [ccar-f-s06.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v4/ccar-f-s06.mp4) |
| #07 | 分野4（その2） | 5:27 | [ccar-f-s07.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v4/ccar-f-s07.mp4) |
| #08 | 分野2 | 6:58 | [ccar-f-s08.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v4/ccar-f-s08.mp4) |
| #09 | 分野5 | 6:42 | [ccar-f-s09.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v4/ccar-f-s09.mp4) |
| #10 | シナリオ別ウォークスルー | 7:56 | [ccar-f-s10.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v4/ccar-f-s10.mp4) |
| #11 | 最終回 | 9:43 | [ccar-f-s11.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccar-f-videos-v4/ccar-f-s11.mp4) |

## 構成
- `CLAUDE.md`：承認済みスタイルと制作ルール（Claude Code 用の指示書）
- `tools/`：ビルドスクリプト（`python3 tools/build_episode.py episodes/epNN`）
- `episodes/epNN/`：各回の台本 `script.md`、章立て `chapters.txt`、制作レポート `REPORT.md`（要確認点）
- `setup_mac.md`：Mac での環境構築（VOICEVOX は Docker、Python venv）

画像・BGM・フォント素材とビルド成果物はコミットしていません（クレジットは `CREDITS.md`）。音声：VOICEVOX:ずんだもん / VOICEVOX:四国めたん
