
---

## 12. 直前チェックリスト

### 12-1. 前日（11/9）
- [ ] Pearson の予約が**日本語**になっているか確認する（英語で予約していたら、48時間前までにキャンセルして日本語で取り直す：FAQ）
- [ ] 本人確認書類（有効期限内の政府発行の写真付きID）の**ローマ字氏名が、Pearson の登録氏名と完全に一致**しているか確認する
- [ ] オンライン受験なら：Pearson のシステムテスト、個室、机の上の片付け、外部モニターを外す。社内ネットワークなら OnVUE に必要なドメインへ通信できるか確認する
- [ ] 模擬試験で間違えた問題を解き直す。この学習ガイドの「ひっかけ」表をすべて読み直す

### 12-2. 当日
- [ ] 開始の30分前には準備を終える（着席時間は約135分）
- [ ] 時間配分：53問を120分、1問あたり約2.2分。迷った問題はフラグを付けて先に進む。最後の15〜20分で見直す
- [ ] 「○つ選択」の数を必ず確認する
- [ ] 消去法：「お願い」「temperature」「とりあえず大きなモデル」「無限リトライ」「全部をコンテキストに貼る」は、たいてい誤り

### 12-3. 頻出ひっかけの総復習（★）
| # | よくある誤答 | 正解の方向 |
|---|---|---|
| 1 | 同期の並列送信で安くなる | **バッチ（50%割引、24時間以内、custom_id で照合）** |
| 2 | バッチの結果は投入順 | **順不同**。custom_id で照合する |
| 3 | 可変部分の末尾にキャッシュのブレークポイント | **固定部分の最後**。順序は tools → system → messages |
| 4 | ツール定義を変えてもキャッシュは無事 | **全体が無効**になる |
| 5 | キャッシュされなければエラーになる | 最小長未満は**黙ってキャッシュされない** |
| 6 | temperature 0 なら決定的 | 完全には決定的にならない |
| 7 | max_tokens で入力の肥大化を解消 | max_tokens は**出力**（思考も含む）の上限 |
| 8 | CLAUDE.md で権限を強制 | **settings.json の permissions、フック** |
| 9 | 個人の上書きは .claude/settings.json | **.claude/settings.local.json** |
| 10 | API でも CLAUDE.md が読まれる | 読まれない。システムプロンプトで明示する |
| 11 | プロンプトの指示で確実に阻止 | **PreToolUse フック**（終了コード2、または deny） |
| 12 | フックが終了コード0でも stderr で止められる | 0の stderr は Claude に見えない |
| 13 | stdio の MCP サーバーで print デバッグ | **stdout は MCP メッセージ専用**。ログは stderr |
| 14 | 社内 API を各アプリにハードコード | **MCP サーバー**で共有する |
| 15 | 決まった手順でも自律エージェント | **ワークフロー** |
| 16 | サブエージェントは履歴を全部引き継ぐ・無料 | 独自のコンテキスト。利用量は計上される |
| 17 | 「JSON で」とお願いする | **構造化出力**＋業務ルールの検証 |
| 18 | インジェクション対策は「従わないで」の一文 | **分離＋最小権限＋フック・承認** |
| 19 | 400 をリトライする | 400 は**直す**。429・500・529 はバックオフしてリトライ |
| 20 | 504 は再送 | **ストリーミング** |
| 21 | CI で対話モード | `claude -p`、`--output-format json`、`--bare` |
| 22 | モデルは常に最新を自動で | **固定して eval で検証**してから更新する |

### 12-4. 出典（2026-11-03 JST に確認）
- 試験ガイド（英語）v1.0：https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542875%2FClaude+Certified+Developer+%E2%80%93+Foundations+Exam+Guide.pdf
- 試験ガイド（日本語）v1.0：https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F34hhd92iyp94a0gtbr15cy5jk%2Fpublic%2F1792453728%2FClaude+Certified+Developer+-+Foundations+Exam+Guide+%28Japanese%29.pdf
- Partner Academy FAQ：https://anthropic-partners.skilljar.com/page/faq-certifications
- Prep Course（5講座・合計774分）：https://anthropic-partners.skilljar.com/path/claude-certified-developer-foundations
- Pearson VUE（12/7の改定告知）：https://www.pearsonvue.com/us/en/anthropic.html
- Models overview：https://platform.claude.com/docs/en/about-claude/models/overview
- Prompt caching：https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Batch processing：https://platform.claude.com/docs/en/build-with-claude/batch-processing
- Effort：https://platform.claude.com/docs/en/build-with-claude/effort ／ Adaptive thinking：https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking ／ Fast mode：https://platform.claude.com/docs/en/build-with-claude/fast-mode
- Structured outputs：https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- Context editing：https://platform.claude.com/docs/en/build-with-claude/context-editing
- Tool use overview：https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview ／ Define tools（tool_choice）：https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools ／ Handle tool calls：https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
- Stop reasons：https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons
- Errors：https://platform.claude.com/docs/en/api/errors
- Glossary（temperature と非決定性）：https://platform.claude.com/docs/en/about-claude/glossary
- Claude Code：settings https://code.claude.com/docs/en/settings ／ memory（CLAUDE.md）https://code.claude.com/docs/en/memory ／ hooks https://code.claude.com/docs/en/hooks ／ headless https://code.claude.com/docs/en/headless ／ skills https://code.claude.com/docs/en/skills ／ sub-agents https://code.claude.com/docs/en/sub-agents
- Agent SDK overview：https://code.claude.com/docs/en/agent-sdk/overview ／ Agent SDK hooks：https://code.claude.com/docs/en/agent-sdk/hooks
- Managed Agents（ベータ）：https://platform.claude.com/docs/en/managed-agents/overview
- MCP transports：https://modelcontextprotocol.io/specification/2025-06-18/basic/transports ／ MCP server concepts：https://modelcontextprotocol.io/docs/learn/server-concepts

> 注意：Claude の API と Claude Code は更新が速く、2026年11月時点の公式ドキュメントには、試験ガイド v1.0（2026年7月）より新しいモデルや仕様が載っています（Fable 5.1、forced tool use の制限など）。試験はガイドの範囲から出題されるので、**モデル固有の細かい数値よりも、設計判断の原則**を優先して覚えてください。
