## 9. 直前チェックリスト

### 前日（11/15）
- [ ] Pearson VUE の予約日時・形式（OnVUE / テストセンター）・**日本語版**で予約されているかを確認（英語で予約済みなら、48時間前までにキャンセル→日本語で再予約。FAQ）
- [ ] 本人確認書類（有効期限内・政府発行・写真付き）。**氏名が Pearson の登録名と完全一致**（ローマ字）か確認。不一致なら受験前に certifications-support@anthropic.com へ（FAQ：24時間前までに依頼）
- [ ] OnVUE の場合：Pearson のシステムテストを実施。会社PCで管理制限があるなら個人PCかテストセンターへ。机の上を空に、サブモニター・スマホ・スマートウォッチ・ヘッドホンは不可
- [ ] §0.3（ガイドと現行ドキュメントのズレ）と §7（サンプル12問）を読み返す
- [ ] 模試で間違えた問題の task をもう一度読む
- [ ] 早めに寝る

### 当日（11/16）
- [ ] 開始前に機密保持契約（NDA）に同意（同意しないと終了・返金なし）
- [ ] 時間配分：**60問/120分＝1問2分**。4シナリオ×約15問なので、**1シナリオ約30分**を目安に。迷ったら印を付けて先へ
- [ ] 複数選択式は**「選ぶ数」を必ず確認**（各問題に明記される）
- [ ] シナリオの前提（ツール名、目標値「初回解決率80%」、「誤検知を最小化」など）を最初にしっかり読む。問題文の「**最も効果的な最初の一手**」「**最も保守しやすい**」「**確実に**」などの修飾語が決め手
- [ ] 結果は終了時に画面表示。合格なら Credly からバッジのメール

### 高頻出ひっかけ 総復習（これだけは落とさない）
1. ループ終了は **stop_reason**（`tool_use`→継続、`end_turn`→終了）。テキストの有無・自然言語・反復上限を主役にしない。
2. サブエージェントは**親の履歴を継承しない** → プロンプトで**明示的・構造化**して渡す。並列は**1応答で複数Task**。コーディネーターの allowedTools に **"Task"**（現行名 Agent）。
3. 確実な遵守（本人確認、金額しきい値）＝**フック/前提条件ゲート**。プロンプト強調・few-shotは確率的。
4. 結果の正規化＝**PostToolUse**、禁止操作のブロック＝**PreToolUse（呼び出しのインターセプト）**。
5. ツール選択ミス → まず**ツール説明の拡充**（入力形式・例・エッジケース・境界）。重複は改名・分割。
6. エラーは**構造化**（errorCategory、isRetryable、説明、部分結果、試行内容）。握りつぶし・全体停止はどちらもNG。アクセス失敗 ≠ 有効な空結果。
7. ツールは**役割ごとに4〜5個**、役割横断は**スコープ限定**（verify_fact）。
8. `tool_choice`：`auto`＝テキストもあり／`any`＝どれか必ず／`{"type":"tool","name":...}`＝指定ツール必ず。
9. 共有MCP＝**`.mcp.json`＋`${TOKEN}`**、個人MCP＝**`~/.claude.json`**。
10. 内容検索＝**Grep**、ファイル名＝**Glob**、Edit 失敗＝**Read＋Write**。
11. CLAUDE.md：ユーザー（`~/.claude/CLAUDE.md`、非共有）／プロジェクト（`./CLAUDE.md` or `.claude/CLAUDE.md`、共有）／ディレクトリ。`@import`、`.claude/rules/`、`/memory`。
12. 散在ファイルの規約＝**`.claude/rules/` ＋ `paths` glob**。
13. チーム共有コマンド＝**`.claude/commands/`**、冗長スキル＝**`context: fork`**、引数の催促＝**`argument-hint`**。
14. 大規模・複数案・アーキテクチャ判断＝**プランモード**、明確な単一修正＝**直接実行**、冗長な探索＝**Explore サブエージェント**。
15. CI＝**`-p`**、構造化＝**`--output-format json` ＋ `--json-schema`**。`CLAUDE_HEADLESS`/`--batch` は**存在しない**。
16. 誤検知 → **具体的なカテゴリ基準**、高誤検知カテゴリの**一時停止**。「保守的に」「確信度の高いものだけ」は効かない。
17. **tool_use＋スキーマ＝構文エラー排除**、でも**意味的エラーは残る**。無いかもしれない値は **nullable**、カテゴリは **enum＋"other"＋詳細**。
18. リトライが効く＝形式・構造の誤り。効かない＝**情報がソースに無い**。
19. Batches＝**50%安い、最大24時間、SLAなし、custom_id、ツールの往復不可** → マージ前は同期、夜間はバッチ。送信間隔＋24h ≦ SLA。
20. レビューは**独立インスタンス**、大規模PRは**ファイル単位＋統合パス**。
21. 長い会話は **case facts ブロック**、ツール出力は**トリミング**、冒頭に要約（lost in the middle）。
22. エスカレーション：**明示的要求は即**、不満だけなら解決を申し出る、**ポリシーの空白**はエスカレーション、複数一致は**追加の識別情報**。感情・自己申告確信度はNG。
23. 長時間探索：**スクラッチパッド**、**サブエージェント委譲**、**マニフェスト**で復旧、`/compact`。
24. 97%でも油断しない：**種別・フィールド別**、**層化無作為抽出**、**ラベル付き検証セットでキャリブレーション**。
25. 矛盾する統計は**両方を出典・日付つきで注記**。財務＝表、ニュース＝文章、技術＝リスト。

### 出典（2026/11/03 JST 取得）と注意
- 公式試験ガイド（英語 v1.0）：https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542750%2FClaude+Certified+Architect+%E2%80%93+Foundations+Exam+Guide.pdf
- 公式試験ガイド（日本語 v1.0）：https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F34hhd92iyp94a0gtbr15cy5jk%2Fpublic%2F1792453693%2FClaude+Certified+Architect+-+Foundations+Exam+Guide+%28Japanese%29.pdf
- Prep Courses（Partner Academy）：https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses
  - 掲載コース：AI Fluency: Framework & Foundations / Building with the Claude API / Claude on Google Cloud / **Claude Code in Action** / Claude 101 / Claude with Amazon Bedrock / **Introduction to Model Context Protocol**（いずれも表示言語は English。日本語版の有無は【要確認】）
- 認定FAQ：https://anthropic-partners.skilljar.com/page/faq-certifications
- Claude API：Tool use 概要 https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview ／ ツール定義・tool_choice https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools ／ ツール呼び出しの処理 https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls ／ stop_reason https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons ／ Structured outputs https://platform.claude.com/docs/en/build-with-claude/structured-outputs ／ Batch processing https://platform.claude.com/docs/en/build-with-claude/batch-processing ／ Prompt caching https://platform.claude.com/docs/en/build-with-claude/prompt-caching ／ Context editing https://platform.claude.com/docs/en/build-with-claude/context-editing ／ Compaction https://platform.claude.com/docs/en/build-with-claude/compaction
- Agent SDK：Hooks https://code.claude.com/docs/en/agent-sdk/hooks ／ Subagents https://code.claude.com/docs/en/agent-sdk/subagents ／ Sessions https://code.claude.com/docs/en/agent-sdk/sessions
- Claude Code：Memory（CLAUDE.md・rules） https://code.claude.com/docs/en/memory ／ Settings https://code.claude.com/docs/en/settings ／ Skills（コマンド統合） https://code.claude.com/docs/en/skills ／ Hooks https://code.claude.com/docs/en/hooks ／ MCP https://code.claude.com/docs/en/mcp ／ Headless（-p, --json-schema） https://code.claude.com/docs/en/headless ／ CLI reference https://code.claude.com/docs/en/cli-reference ／ Permission modes（plan mode） https://code.claude.com/docs/en/permission-modes ／ Subagents（Explore） https://code.claude.com/docs/en/sub-agents ／ Commands https://code.claude.com/docs/en/commands
- MCP仕様（isError）：https://modelcontextprotocol.io/specification/2025-06-18/server/tools ／ Resources：https://modelcontextprotocol.io/specification/2025-06-18/server/resources

**注意**
- 本ガイドの模擬試験・シナリオ別の「典型的な問い」は、公式ガイドのタスクステートメントに基づく**オリジナル問題**であり、実際の試験問題ではありません（試験内容はNDAで非公開）。
- 試験はガイド v1.0 の記述を基準にしています。現行ドキュメントと名称・細部が異なる箇所は §0.3 にまとめました。迷ったら**ガイドの表現**を優先して解答してください。
- Claude Code / Agent SDK は更新が速く、バージョン番号つきの記述は 2026/11/03 時点のものです。
