# CCDV-P 解説動画（全11回）

[`../ccdv-p-study-guide.md`](../ccdv-p-study-guide.md) をもとに、ずんだもん（解説役）と四国めたん（質問役）の対話形式で解説する非公式の学習用動画です。公式教材・公式試験問題の転載ではなく、合格を保証するものでもありません。

動画本体は git に含めず Release で配布：https://github.com/ryokn/claude-certs-study-ja/releases/tag/ccdv-p-videos-v1

結合版: [ccdv-p-all.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-p-videos-v1/ccdv-p-all.mp4)（57:26。各回末尾のエンドカードは最後に1回だけ）

YouTube（結合版・限定公開）: [CCDV-P 解説動画 全11回まとめ【非公式・試験対策】](https://youtu.be/2WwKBQUnVYU)（57:26）

## 各話の長さ

完成済み mp4 の ffprobe による長さです（各話末尾にエンドカード約4秒を含みます）。mp4 自体は git 管理外です。第10回（模擬試験の案内）は作っていません。

| 回 | タイトル | 長さ | ダウンロード |
|---|---|---:|---|
| 第0回 | 試験概要・CCDV-Fとの違い・学習プラン | 6:44 | [ccdv-p-s00.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-p-videos-v1/ccdv-p-s00.mp4) |
| 第1回 | 本番環境の統合、信頼性、知識グラウンディング | 8:40 | [ccdv-p-s01.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-p-videos-v1/ccdv-p-s01.mp4) |
| 第2回 | 高度なエージェントアーキテクチャとオーケストレーション | 6:11 | [ccdv-p-s02.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-p-videos-v1/ccdv-p-s02.mp4) |
| 第3回 | オブザーバビリティと本番環境のモニタリング | 4:38 | [ccdv-p-s03.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-p-videos-v1/ccdv-p-s03.mp4) |
| 第4回 | 評価エンジニアリングと品質保証 | 5:09 | [ccdv-p-s04.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-p-videos-v1/ccdv-p-s04.mp4) |
| 第5回 | ランタイムガードレールと本番環境のセキュリティ | 5:00 | [ccdv-p-s05.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-p-videos-v1/ccdv-p-s05.mp4) |
| 第6回 | 高度なデバッグとインシデント対応 | 4:22 | [ccdv-p-s06.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-p-videos-v1/ccdv-p-s06.mp4) |
| 第7回 | ソフトウェア提供のためのエージェントフリート運用 | 5:18 | [ccdv-p-s07.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-p-videos-v1/ccdv-p-s07.mp4) |
| 第8回 | 大規模環境でのコストとレイテンシの最適化 | 4:29 | [ccdv-p-s08.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-p-videos-v1/ccdv-p-s08.mp4) |
| 第9回 | 公式サンプル問題の要点 | 4:07 | [ccdv-p-s09.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-p-videos-v1/ccdv-p-s09.mp4) |
| 第11回 | 直前チェックリスト | 3:23 | [ccdv-p-s11.mp4](https://github.com/ryokn/claude-certs-study-ja/releases/download/ccdv-p-videos-v1/ccdv-p-s11.mp4) |
| 合計 | | 58:05 | |

## ファイル構成

| パス | 内容 |
|---|---|
| `episodes/epNN/script.md` | 各回の台本（スライド＋セリフ） |
| `episodes/epNN/chapters.txt` | 各回の章立て |
| `episodes/REPORT.md` | 制作レポート（長さ・要確認点） |
| `tools/` | ビルドスクリプト（`python3 tools/build_episode.py episodes/epNN`） |
| `CLAUDE.md` | 承認済みスタイルと制作ルール |
| `setup_mac.md` | Mac での環境構築（VOICEVOX は Docker、Python） |
| `CREDITS.md` | 音声・BGM・フォントのクレジットと利用条件 |
| `TASK_CCDVP.md` | 制作時の依頼内容（全11回の構成） |
| `reference/` | 台本書式の見本 |

学習ガイド本文は重複して置かず、[`../ccdv-p-study-guide.md`](../ccdv-p-study-guide.md) を参照してください（制作時の `episodes/guide.md` と同一内容です）。

## ビルド

BGM 音源と Noto Sans CJK フォントは git に入れていません。配置方法は `assets/bgm/README.md` と `CREDITS.md` を見てください。VOICEVOX Engine が必要です。顔アイコンは `assets/chars/` にあります。

```bash
# 例: 第0回
python3 tools/build_episode.py episodes/ep00
```

クレジット（エンドカードと概要欄）:

```
VOICEVOX:ずんだもん / VOICEVOX:四国めたん
BGM：昼下がり気分（KK / OpenTracks）
```
