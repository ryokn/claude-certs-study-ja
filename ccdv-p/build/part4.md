## 11. 直前チェックリスト

### 11-1. 前日
- [ ] Pearson の予約で**試験言語が日本語**になっているか、日時・方式（OnVUE / テストセンター）を確認した（OnVUE の変更は1時間前まで、テストセンターは48時間前まで）。
- [ ] 身分証（政府発行・有効期限内・写真付き、登録名と完全一致）を用意した。
- [ ] OnVUE なら、PC・ネットワークのシステムテストを済ませ、机の上を片付けた（メモ、スマートフォン、2台目のモニターは不可）。
- [ ] 第9章（公式サンプルの型）と、各章の「ひっかけ」だけを読み直した。

### 11-2. 当日
- [ ] 70問・120分 ＝ **1問あたり約1.7分**。長いシナリオは、最後の1文（何を問うか：best / first / most directly）を先に読む。
- [ ] 採点対象外の10問は区別できないので、**全問を同じように解く**。
- [ ] 複数選択は**選ぶ数**を確認する。
- [ ] 迷ったらマークして先へ進み、最後に見直す。

### 11-3. 頻出ひっかけの総復習（★）
| ひっかけ | 正しい考え方 |
|---|---|
| 失敗の種類を区別せず、リトライ回数・バックオフを増やす | レート制限・長さ切れ・拒否・支出上限で**分岐**する |
| 拒否（refusal）を同じモデルにリトライする | 再び拒否されやすい。**別モデルのフォールバック**か安全性の処理経路へ。拒否は HTTP 200 なので**独立したシグナル**として計測 |
| 支出上限の429を待てば直ると考える | `retry-after` がなく、上限変更か月替わりまで回復しない |
| `max_tokens` を下げてレート制限を回避 | OTPM は実際の生成量で数える。ITPM が律速ならキャッシュ（キャッシュ読み取りは ITPM に数えない） |
| 上限内なのに429 → 上限を上げる申請だけ | **ランプ制限**（急増・バースト）。徐々に増やす |
| 新モデルを評価なしで全面切り替え | 同じ評価スイートで比較 → 段階的ロールアウト → ロールバック手段 |
| 検索の失敗をモデルの変更で直す | 段階（取り込み・検索・リランキング・生成）で切り分ける |
| セッションの resume でファイルも元に戻る | セッションは**会話**、ファイルは**チェックポイント**で戻す |
| 途中で指示を変えるために `system` を書き換える | キャッシュが無効になる。**会話途中の system メッセージ** |
| ツール定義を頻繁に変える | キャッシュ全体が無効。遅延読み込み・会話途中のツール変更 |
| 監視は5xxとエラー率で十分 | LLMの失敗の多くは HTTP 200（誤答・拒否・長さ切れ） |
| ZDR だからトレースに内容は出せない | Claude API の OTel は ZDR でも Full content を選べる（保存先の要件は別途確認） |
| LLM-as-judge をすぐゲートに使う／大きいモデルにすれば直る | 人間ラベルでキャリブレーション、位置バイアス対策、一致するまでゲート権限なし |
| 評価スイートは一度作れば十分 | 汚染・飽和・カバレッジ不足を継続的に管理 |
| プロンプトに禁止事項を書けば流出は防げる | **送信先の許可リスト・承認・データ範囲の限定**などモデルの外の制御 |
| 送信をすべてログに残す | 検知であって防止ではない |
| 静的APIキーを CI のシークレットに保存してローテーション | **ワークロードIDフェデレーション**で短命トークン |
| 原因が分かるまでロールバックしない | 緩和（ロールバック）が先、根本原因の調査は後 |
| AIコードレビューに最初からマージの合否を任せる | シャドーモード → 人とのキャリブレーション → ゲート化 |
| 利用者の設定で管理設定を上書きできる | 管理設定が最優先。MCP は拒否リストが優先 |
| ストリーミングで総レイテンシが下がる | 下がるのは TTFT（体感）。総時間は出力量・effort・並列化で |
| 支出上限があるのでテナント別の予算管理は不要 | 組織の上限は全体を止める最後の安全網。テナント予算はアプリ層で強制 |

### 11-4. 出典（2026-11-20 JST に確認）
**公式（試験）**
- 認定ページ（試験ガイドのダウンロード）：https://anthropic-partners.skilljar.com/claude-certified-developer-professional-certification
- 試験ガイド v1.0（英語版PDF）：https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794947325/Claude_Certified_Developer-Professional_Exam_Guide.pdf
- 試験ガイド v1.0（日本語版PDF）：https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794947417/Claude_Certified_Developer-Professional_Exam_Guide_Japanese.pdf
- 準備コース：https://anthropic-partners.skilljar.com/path/claude-certified-developer-professional
- 認定試験のFAQ：https://anthropic-partners.skilljar.com/page/faq-certifications
- Pearson VUE（Anthropic）：https://www.pearsonvue.com/us/en/anthropic.html

**公式ドキュメント（Claude Platform）**
- エラー：https://platform.claude.com/docs/en/api/errors
- レート制限：https://platform.claude.com/docs/en/api/rate-limits
- 停止理由とフォールバック：https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons
- 拒否とフォールバック：https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback ／ フォールバッククレジット：https://platform.claude.com/docs/en/build-with-claude/fallback-credit
- ストリーミング：https://platform.claude.com/docs/en/build-with-claude/streaming
- プロンプトキャッシング：https://platform.claude.com/docs/en/build-with-claude/prompt-caching ／ キャッシュ診断：https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics
- Batch処理：https://platform.claude.com/docs/en/build-with-claude/batch-processing
- コンパクション：https://platform.claude.com/docs/en/build-with-claude/compaction ／ コンテキスト編集：https://platform.claude.com/docs/en/build-with-claude/context-editing
- 会話途中の system メッセージ：https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages
- メモリツール：https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool ／ ツール検索：https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool ／ Advisor ツール：https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool
- effort：https://platform.claude.com/docs/en/build-with-claude/effort ／ 遅延の削減：https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency
- Citations：https://platform.claude.com/docs/en/build-with-claude/citations ／ 検索結果ブロック：https://platform.claude.com/docs/en/build-with-claude/search-results
- OpenTelemetry：https://platform.claude.com/docs/en/manage-claude/opentelemetry
- データ保持（ZDR）：https://platform.claude.com/docs/en/manage-claude/api-and-data-retention
- ワークロードIDフェデレーション：https://platform.claude.com/docs/en/manage-claude/workload-identity-federation
- モデルの概要：https://platform.claude.com/docs/en/about-claude/models/overview ／ モデルの非推奨化：https://platform.claude.com/docs/en/about-claude/model-deprecations
- サービスティア：https://platform.claude.com/docs/en/api/service-tiers
- Managed Agents：https://platform.claude.com/docs/en/managed-agents/overview ／ マルチエージェント：https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration
- 成功基準と評価：https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
- ジェイルブレイクとインジェクションの軽減：https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks

**公式ドキュメント（Claude Code / Agent SDK）**
- 設定と優先順位：https://code.claude.com/docs/en/settings ／ 設定リファレンス：https://code.claude.com/docs/en/settings-reference
- 管理 MCP：https://code.claude.com/docs/en/managed-mcp ／ MCP：https://code.claude.com/docs/en/mcp
- 監視（OpenTelemetry）：https://code.claude.com/docs/en/monitoring-usage
- フック：https://code.claude.com/docs/en/hooks ／ ヘッドレス：https://code.claude.com/docs/en/headless ／ worktree：https://code.claude.com/docs/en/worktrees
- Code Review：https://code.claude.com/docs/en/code-review ／ LLMゲートウェイ：https://code.claude.com/docs/en/llm-gateway
- Agent SDK のセッション：https://code.claude.com/docs/en/agent-sdk/sessions ／ 安全なデプロイ：https://code.claude.com/docs/en/agent-sdk/secure-deployment

**Anthropic のエンジニアリング記事**
- Building effective agents：https://www.anthropic.com/engineering/building-effective-agents
- マルチエージェントの調査システム：https://www.anthropic.com/engineering/multi-agent-research-system
- 長時間エージェントのハーネス：https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- エージェントの評価：https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Contextual Retrieval：https://www.anthropic.com/news/contextual-retrieval
- ポストモーテム（3つの問題）：https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues

> **注意**：モデル名、料金、ベータ機能、ドキュメントの内容は頻繁に変わります。本ガイドの数値と機能の説明は2026-11-20時点の公式ページによるものです。試験は v1.0（2026年11月発効）の時点の知識を前提にしているので、**具体的な数値より「考え方」で解く** ことを優先してください。模擬試験は本ガイドのオリジナル問題で、実際の試験問題とは関係ありません。
