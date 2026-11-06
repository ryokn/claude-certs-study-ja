# Credits / ライセンス

## 音声・キャラクター
- VOICEVOX:ずんだもん / VOICEVOX:四国めたん
- エンジン想定: VOICEVOX Engine（Docker `voicevox/voicevox_engine:cpu-arm64-latest` または同等）。話者 ID: ずんだもん=3、四国めたん=2。speedScale 1.2。
- 顔アイコン（`assets/chars/*_head.png`）: 公式立ち絵を参考に生成したデフォルメ画像（ユーザー承認済み）。
- キャラクターガイドライン: https://zunko.jp/guideline.html

エンドカード（約4秒）と YouTube 概要欄の両方に入れる文言:
`VOICEVOX:ずんだもん / VOICEVOX:四国めたん`
`BGM：昼下がり気分（KK / OpenTracks）`

本編スライド上には VOICEVOX クレジットを出さない。

## BGM
- 曲名: 昼下がり気分（通常版）
- 作曲: KK
- 配布: OpenTracks（旧 DOVA-SYNDROME） https://opentracks.com/bgm/detail/4695
- 利用条件の要約（必ず公式を再確認）:
  - 解説動画の BGM としての YouTube 使用は無料（営利・非営利）
  - 音源単体の再配布・販売、BGM を主目的にした配信、AI 学習利用、Content ID への音楽登録は禁止
  - そのため `assets/bgm/` は `.gitignore` 済み。配布用 tarball には個人利用のため含めるが、git remote には載せない

## フォント
- Noto Sans CJK（`assets/fonts/`）: SIL Open Font License 1.1（`assets/fonts/COPYRIGHT`）
- 未バンドル時のフォールバック: macOS のヒラギノ角ゴシック

## 内容
- 非公式の学習用解説。公式試験問題の転載ではない。
- 数値・仕様で一次情報と食い違う／確認できない点は「要確認」と書く。
- 既知の食い違い例: キャンセル／予約変更期限 — ガイドは24時間前、FAQは48時間前 → **48時間前で案内し「要確認」**。
