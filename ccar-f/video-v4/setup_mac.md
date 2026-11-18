# Mac (Apple Silicon) セットアップ

前提: macOS（Apple Silicon）、Homebrew、Docker Desktop、ffmpeg と python3 が `/opt/homebrew/bin` にあること。VOICEVOX アプリは不要（Engine を Docker で起動する）。

## 1. 依存関係

```bash
cd /path/to/ccarf-claude-kit
/opt/homebrew/bin/python3 -m pip install -r requirements.txt
# ffmpeg が無ければ:
# brew install ffmpeg
which ffmpeg python3
```

## 2. VOICEVOX Engine（Docker）

公式イメージ（Docker Hub で確認済み、Apple Silicon 向け）:

```bash
docker run -d --rm -p 50021:50021 --name voicevox-engine \
  voicevox/voicevox_engine:cpu-arm64-latest
```

- タグ: `cpu-arm64-latest`（= `cpu-arm64-ubuntu24.04-latest` 系）
- ピン留めするなら例: `voicevox/voicevox_engine:cpu-arm64-0.26.1`
- 起動確認:

```bash
curl -s http://127.0.0.1:50021/version
# 例: "0.26.0" や "0.26.1"
```

別ホスト／ポートなら:

```bash
export VOICEVOX_URL=http://127.0.0.1:50021
```

## 3. BGM ファイル

tarball 展開済みなら `assets/bgm/昼下がり気分.mp3` がある。
git clone だけした場合は OpenTracks から個人用に取得し、同パスへ置く（**git remote には追加しない**）。

## 4. スモークテスト

```bash
# 第1回台本の先頭2枚だけ（TTS→描画→BGM→chapters）
python3 tools/build_episode.py episodes/ep01 --max-slides 2
ls -lh episodes/ep01/ccar-f-s01.mp4 episodes/ep01/chapters.txt
```

フルビルド:

```bash
python3 tools/build_episode.py episodes/ep01
```

## 5. Linear（任意・推奨）

動画進捗は Linear（チーム RYO / プロジェクト「CCAR-F 解説動画シリーズ」、issue タイトル「CCAR-F #NN …」）で管理する。

Claude Code に Linear MCP が無ければ、公式ドキュメントどおり:

```bash
claude mcp add --transport http linear-server https://mcp.linear.app/mcp
```

その後セッションで `/mcp` を実行して OAuth する。
（公式: https://linear.app/docs/mcp — エンドポイントは `https://mcp.linear.app/mcp`。古い `/sse` は非推奨・廃止。）

接続できない場合は Linear 操作をスキップして動画制作だけ進めてよい（`CLAUDE.md` 参照）。

## 6. フォント

`assets/fonts/NotoSansCJK-*.ttc` を同梱済み（OFL）。欠ける場合は macOS のヒラギノを自動利用する。
