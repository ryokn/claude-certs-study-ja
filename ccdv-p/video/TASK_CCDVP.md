# 依頼: CCDV-P（Claude Certified Developer – Professional）解説動画 11本

このキット（ccarp-claude-kit をコピーしたもの。CCAR-F/CCAR-P と同じ承認済みの制作一式）で、CCDV-P の解説動画を作る。
素材は `episodes/guide.md`（ryokn/claude-certs-study-ja の ccdv-p/ccdv-p-study-guide.md、main 版）。

## 構成（学習ガイドの章に合わせて11本）
| Video | ディレクトリ | ガイドの章 |
|---|---|---|
| 0 | episodes/ep00 | 第0章 試験概要・CCDV-Fとの違い・学習プラン |
| 1〜8 | episodes/ep01〜ep08 | 第1〜8章（各出題分野） |
| 9 | episodes/ep09 | 第9章 公式サンプル問題の要点（問題文の丸写しはしない） |
| 11 | episodes/ep11 | 第11章 直前チェックリスト |
第10章（模擬試験の案内）は作らない。各本の尺は内容に応じて約10分を目安。水増しはしない。

## 手順
1. まず CLAUDE.md・README・tools/ を読み、出力名やタイトル表記を CCDV-P 用に直す（例: ccdv-p-sNN.mp4、帯や章タイトル、エンドカード、CREDITS）。ロジックやレイアウトは変えない。
2. 台本書式は reference/ccarp-sample-ep01/script.md を手本にする。CLAUDE.md も CCDV-P 用に書き換えてよい。
3. 各本: `episodes/epNN/script.md` を一度で書く → `python3 tools/build_episode.py episodes/epNN`（Python は ~/.venvs/ccarf/bin/python 等、CCAR-P 制作時と同じ環境）→ 数枚のフレームだけ確認。
4. 1本ずつ順番に ep00 → ep11 まで全部作る。

## 必ず守る形式
- VOICEVOX ずんだもん（解説）× 四国めたん（質問）の対話。字幕は下部中央。左にめたん顔、右にずんだもん顔。話していない側は暗くする。
- 左右2分割のスライドは話している側をオレンジ枠＋「いまココ」で強調。全スライドに図・表・コードのいずれかを入れる。
- 自己紹介や定型の締めは入れない。自作例は「（オリジナル）」、未確認の事実は「要確認」。
- BGM「昼下がり気分」を小さめで通しで流す。クレジット（VOICEVOX:ずんだもん / VOICEVOX:四国めたん、BGM）は最後のエンドカード1枚と概要欄だけ。
- 公開・アップロード・git push・Release 作成はしない。Linear も触らない。

## 完了時
`episodes/REPORT.md` に各本の長さ（分:秒）、合計時間、要確認点を書き、最後の出力にも同じ表を出す。
