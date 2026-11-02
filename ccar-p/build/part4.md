## 10. 直前チェックリスト

### 前日（11/23 または受験日の前日）
- [ ] Pearson VUE の予約日時（JST）、**日本語版**で予約しているか、本人確認書類の氏名（ローマ字）が登録内容と完全に一致しているかを確認する。予約の変更やキャンセルは **48時間前まで**（FAQ）
- [ ] オンライン受験なら、Pearson のシステムテストを実行する。会社の端末やネットワークでブロックされないかも確認する（必要なドメインのリストは FAQ にリンクがある）
- [ ] 机の上を片付ける（メモ、電話、サブモニター、スマートウォッチ、ヘッドホンは不可）。**ブラウザの翻訳ツールも不可**
- [ ] 第8章のサンプル3問と、模擬試験で間違えた問題だけを解き直す
- [ ] 下の「ひっかけ総復習」を2回読む

### 当日
- [ ] チェックインの30分前には準備を終える（着席時間は約135分を見込む）
- [ ] ペース配分：**63問・120分 → 1問あたり約1.9分**。30問目の時点で残り60分以上あるのが目安。迷った問題はマークして先に進む
- [ ] 複数選択式は「**選ぶ数**」を必ず確認する
- [ ] 「最も適切な（best）」「最初に（first）」「最も直接的に（most directly）」などのキーワードに印をつけて読む

### 高頻出の「ひっかけ」総復習
| # | ひっかけ | 正しい考え方 |
|---|---|---|
| 1 | より大きなモデルにすれば解決する | 権限、検索、設計の問題はモデルでは解決しない。まず原因を切り分ける |
| 2 | プロンプトに禁止事項を書けば安全 | 強制はアプリ層で行う（ツールの除去、認可、管理設定の deny） |
| 3 | ログや確認ダイアログを付ければ、ツールは残してよい | 最小権限 ＝ 不要なツールを外す（サンプル1） |
| 4 | 長いプロンプトは切り詰めるか、few-shotに移す | 変化しない内容を先頭に置いてキャッシュする（サンプル2）。tools → system → messages の順 |
| 5 | 誤答が出たらモデルを疑う | 何が変わったかから考える。文書の更新なら検索側（サンプル3） |
| 6 | 定型業務にもエージェントやマルチエージェントを使う | 最も単純な構成から始める。マルチエージェントはチャットの約15倍のトークンを使う |
| 7 | リアルタイム用途で Batch API を使う | Batch は非同期（多くは1時間以内、最大24時間）で50%割引。ZDRの対象外 |
| 8 | ライブ状態もRAGに入れる | 在庫や注文はツールやAPIで都度照会する |
| 9 | 埋め込みだけで十分 | 型番やコードには BM25 を併用する（Contextual Retrieval でBM25併用時の検索失敗 −49%、リランキングも加えて −67%） |
| 10 | 全件を人がレビュー、または完全自動化 | 信頼度、可逆性、誤った場合のコストで振り分ける |
| 11 | 安全管理策が落ちたら処理を続ける | 高リスクの操作はフェイルクローズにする |
| 12 | MCPサーバーがトークンを下流へ転送する | トークンパススルーは禁止。audienceを検証する |
| 13 | Claude直のAPIなら FedRAMP High に対応している | Bedrock（GovCloud）、Vertex（Assured Workloads）、Claude for Government を使う【要確認】 |
| 14 | プレフィルで JSON を強制する | 4.6以降のモデルではサポートされていない。構造化出力を使う |
| 15 | CLAUDE.md で組織のルールを強制する | 管理設定（permissions.deny）を使う。評価順は deny → ask → allow |
| 16 | A/Bテストで少しでも改善したら展開する | 事前に決めたサンプル数、指標、ガードレールを守る。過大に主張しない |
| 17 | 全件人手採点が最良の評価 | コード → LLM（キャリブレーション済み）→ 人の順に検討し、質より量 |
| 18 | ベンチマークの数値で価値を説明する | 価値の柱（効率性、変革、生産性、コスト、SLA）をKPI、ベースライン、目標で示す |
| 19 | まずPoCを作る | 先に体系的なディスカバリーを行い、要件と前提条件を文書にする |
| 20 | 推奨案だけを示す | 選択肢ごとにコスト、リスク、変更に必要なことを示して推奨する |
| 21 | キャッシュの最小トークン数に届かないとエラーになる | エラーにはならず、キャッシュされないだけ（usage の値で確認する） |

### 数字の暗記カード（公式の出典あり）
- 試験：63問、120分、720/1000、$175、有効期間12か月、再受験の待機期間 14日 / 30日 / 90日、12か月で4回まで
- キャッシュ：TTL 5分（既定）または1時間。書き込み 1.25倍 / 2倍、読み取り 0.1倍。ブレークポイントは最大4個
- Batch：50%割引。10万リクエストまたは256MB。多くは1時間以内、最大24時間。結果の保持は29日
- Contextual Retrieval：文脈説明は50〜100トークン。検索失敗 −35% / −49% / −67%。知識ベースが20万トークン未満なら全体をプロンプトに入れる
- ツール：30〜50個を超えると選択精度が下がる。ツール検索でツール定義のトークンを85%以上削減
- Skills：メタデータは1スキルあたり約100トークン、本文は5,000トークン未満
- マルチエージェント：トークン使用量はチャットの約4倍（エージェント）、約15倍（マルチエージェント）。単一エージェントを90.2%上回った
- pass^k：成功率75%で3回試行すると約42%

### 出典URL（2026-11-03 JST に確認）
- 試験ガイド（英語、v1.0）：https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542810%2FClaude+Certified+Architect+%E2%80%93+Professional+Exam+Guide.pdf
- 試験ガイド（日本語、v1.0。PDFの作成日は 2026-10-20）：https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F34hhd92iyp94a0gtbr15cy5jk%2Fpublic%2F1792453714%2FClaude+Certified+Architect+-+Professional+Exam+Guide+%28Japanese%29.pdf
- 準備コース：https://anthropic-partners.skilljar.com/path/claude-certified-architect-professional
- 認定試験のFAQ：https://anthropic-partners.skilljar.com/page/faq-certifications
- Pearson VUE（12/7の更新の告知）：https://www.pearsonvue.com/us/en/anthropic.html
- モデルの概要：https://platform.claude.com/docs/en/about-claude/models/overview
- モデルの選び方：https://platform.claude.com/docs/en/about-claude/models/choosing-a-model
- effort：https://platform.claude.com/docs/en/build-with-claude/effort
- プロンプトキャッシング：https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Batch処理：https://platform.claude.com/docs/en/build-with-claude/batch-processing
- 構造化出力：https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- コンテキスト編集とコンパクション：https://platform.claude.com/docs/en/build-with-claude/context-editing
- 成功基準と評価：https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
- ハルシネーションの低減：https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- ジェイルブレイクとインジェクションの軽減：https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks
- プロンプト漏えいの低減：https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-prompt-leak
- ZDRとHIPAA：https://platform.claude.com/docs/en/build-with-claude/zero-data-retention
- 料金（データの所在、リージョン）：https://platform.claude.com/docs/en/about-claude/pricing
- レート制限：https://platform.claude.com/docs/en/api/rate-limits
- ツール検索：https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool
- Agent Skills：https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Contextual Retrieval：https://www.anthropic.com/news/contextual-retrieval
- Building effective agents：https://www.anthropic.com/engineering/building-effective-agents
- コンテキストエンジニアリング：https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- マルチエージェントの調査システム：https://www.anthropic.com/engineering/multi-agent-research-system
- エージェントの評価：https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- MCPの認可（2026-07-28版）：https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
- MCPのトランスポート：https://modelcontextprotocol.io/specification/2026-07-28/basic/transports
- Claude Code の設定：https://code.claude.com/docs/en/settings ／ 権限：https://code.claude.com/docs/en/permissions ／ CLAUDE.md：https://code.claude.com/docs/en/memory ／ フック：https://code.claude.com/docs/en/hooks ／ MCP：https://code.claude.com/docs/en/mcp ／ コスト：https://code.claude.com/docs/en/costs ／ 監視：https://code.claude.com/docs/en/monitoring-usage
- 政府向け（FedRAMP）：https://claude.com/solutions/government

> **注意**：モデル名、料金、認可の状況は頻繁に変わります。本ガイドの数値は2026-11-03時点の公式ページによるものです。試験は v1.0（2026年7月）の時点の知識を前提にしている可能性があるので、**具体的な数値より「考え方」で解く** ことを優先してください。模擬試験は本ガイドのオリジナル問題で、実際の試験問題とは関係ありません。
