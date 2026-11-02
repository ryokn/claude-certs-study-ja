## 1. 分野1：エージェントアーキテクチャとオーケストレーション（Agentic Architecture & Orchestration）— 27%・約16問

最重要分野。シナリオ1（サポート）、3（マルチエージェントリサーチ）、4（開発者生産性）で横断的に出ます。

### 1.1 自律的なタスク実行のためのエージェントループ（agentic loop）を設計し実装する

**基礎**
- ループ：Claudeにリクエスト → `stop_reason` を確認 → `"tool_use"` ならツールを実行 → `tool_result` を会話履歴に追加 → 次の反復。`"end_turn"` で終了。
- ツール結果を履歴に追加するから、モデルは新しい情報を踏まえて次のアクションを**モデル主導で**決められる（事前に決めた決定木・固定のツール順序との違い）。

**現行APIの事実（Claude API ドキュメント）**
- `stop_reason` の値：`end_turn` / `max_tokens` / `stop_sequence` / `tool_use` / `pause_turn`（サーバーツールのループが反復上限に達した。応答をそのまま送り返して続行）/ `refusal` / `model_context_window_exceeded`。
- `tool_result` は対応する `tool_use` の**直後のユーザーメッセージ**に置き、その content 配列では **tool_result ブロックを先頭**に（テキストは後ろ）。`tool_use_id` で対応付け、失敗時は `is_error: true`。
- 1つの応答に複数の `tool_use`（並列ツール呼び出し）が入ることがある → 全部実行して、結果を**1つのユーザーメッセージ**にまとめて返す。

```python
# 最小のエージェントループ（Claude API / Python SDK）
messages = [{"role": "user", "content": user_input}]
while True:
    resp = client.messages.create(model=MODEL, max_tokens=2048,
                                  system=SYSTEM, tools=TOOLS, messages=messages)
    messages.append({"role": "assistant", "content": resp.content})  # 履歴に必ず追加
    if resp.stop_reason == "tool_use":
        results = []
        for b in resp.content:
            if b.type == "tool_use":
                out, err = run_tool(b.name, b.input)
                results.append({"type": "tool_result", "tool_use_id": b.id,
                                "content": out, "is_error": err})
        messages.append({"role": "user", "content": results})  # tool_result を先頭に
        continue
    break  # end_turn（max_tokens 等は別途ハンドリング）
```

**頻出ポイント / ひっかけ**
- ✅ 継続/終了は **stop_reason** で判定。
- ❌「応答に "完了" が含まれたら終了」＝**自然言語シグナルの解析**（アンチパターン）。
- ❌「反復上限◯回を**主要な**停止メカニズムにする」（安全装置として併用は可。主役にしない）。
- ❌「アシスタントの**テキストがあれば完了**」。テキストと tool_use は同じ応答に同居し得る。
- ❌ ツール結果を履歴に追加しない／前回までの履歴を送らない（APIはステートレス。毎回**完全な会話履歴**を送る＝タスク5.1）。

### 1.2 コーディネーター・サブエージェントパターン（coordinator-subagent）でオーケストレーションする

**基礎**
- **ハブアンドスポーク（hub-and-spoke）**：コーディネーターがサブエージェント間の通信・エラー処理・情報ルーティングを**すべて**管理。
- サブエージェントは**分離されたコンテキスト**で動き、コーディネーターの会話履歴を自動では継承しない。
- コーディネーターの役割：タスク分解、委任、結果の集約、**クエリの複雑さに応じて呼ぶサブエージェントを決める**。

**頻出ポイント / ひっかけ**
- ✅ 毎回全パイプラインを回さず、**必要なサブエージェントだけを動的に選択**。
- ✅ リサーチ範囲を**サブトピックや情報源の種類で分割**して重複を最小化。
- ✅ **反復的改善ループ**：統合結果の不足をコーディネーターが評価 → 的を絞ったクエリで検索/分析に再委任 → 統合を再実行（カバレッジが十分になるまで）。
- ✅ 通信は**すべてコーディネーター経由**（可観測性・一貫したエラー処理・制御された情報フロー）。
- ⚠️ **分解が狭すぎる**と網羅性が落ちる（サンプル問題7：「クリエイティブ産業」をビジュアルアートだけに分解）。下流のエージェントが正しく動いていても、**割り当て自体**が原因。
- ❌ サブエージェント同士が直接呼び合う設計（観測・エラー処理が分散）。

### 1.3 サブエージェントの呼び出し、コンテキストの受け渡し、生成（spawning）を設定する

**基礎**
- サブエージェントは **Task ツール**で生成（現行名 `Agent`）。コーディネーターの **`allowedTools` に `"Task"` が必要**。
- **AgentDefinition**：`description`（いつ使うか＝委任判断の材料・必須）、`prompt`（そのエージェントのシステムプロンプト・必須）、`tools`（ツール制限。省略時は継承）、`model` など。
- 親から子に渡るのは**Taskツールのプロンプト文字列だけ**（＋そのエージェント自身のシステムプロンプト、プロジェクトCLAUDE.md、ツール定義）。親の会話履歴・ツール結果・親のシステムプロンプトは渡らない（現行SDKドキュメント）。
- **フォーク（fork）**ベースのセッション管理：共通の分析ベースラインから異なるアプローチを探る。

```python
# Agent SDK（Python）：コーディネーター＋サブエージェント定義（現行ドキュメントの形）
options = ClaudeAgentOptions(
    allowed_tools=["Task", "Read", "Grep"],   # 試験ガイドの表記は "Task"（現行は "Agent"）
    agents={
        "web-searcher": AgentDefinition(
            description="ウェブ検索専門。最新の公開情報が必要なときに使う",
            prompt="あなたはウェブ調査担当。各発見に claim, excerpt, url, published_at を付けて返す",
            tools=["WebSearch", "WebFetch"]),
        "synthesizer": AgentDefinition(
            description="複数の調査結果を出典付きで統合する",
            prompt="受け取った claim-source の対応を保持したまま統合する",
            tools=["Read"]),
    })
```

**頻出ポイント / ひっかけ**
- ✅ 先行エージェントの**調査結果全体**を、次のサブエージェントの**プロンプトに直接**含める（例：検索結果＋文書分析を統合エージェントへ）。
- ✅ 内容と**メタデータ（URL・文書名・ページ番号）を分けた構造化形式**で渡し、出典の帰属を保持。
- ✅ **並列実行＝コーディネーターの1つの応答で複数のTask呼び出しを出す**（別々のターンに分けない）。
- ✅ コーディネーターのプロンプトは**手順の羅列ではなく、目標と品質基準**を伝える（サブエージェントが適応できる）。
- ❌「サブエージェントは親の履歴を参照できる/メモリを共有する」→ 誤り。
- ❌ 委任されない問題に「コーディネーターにも同じツールを与える」→ 逆効果。

### 1.4 強制とハンドオフのパターンで複数ステップのワークフローを実装する

**基礎**
- **プログラムによる強制（programmatic enforcement：フック、前提条件ゲート）** vs **プロンプトベースのガイダンス**。
- 決定論的な遵守が必要（例：金銭操作の前の本人確認）なとき、**プロンプト指示だけでは失敗率がゼロにならない**。
- 途中エスカレーション用の**構造化ハンドオフ**：顧客の詳細、根本原因の分析、推奨アクション。

| 判断軸 | プログラムによる強制（フック/ゲート） | プロンプト（指示・few-shot） |
|---|---|---|
| 保証 | 決定論的（必ず守られる） | 確率的（たまに破られる） |
| 使う場面 | 金銭・本人確認・コンプライアンス・不可逆操作 | 口調、判断基準、曖昧なケースの扱い |
| 例 | get_customer が検証済みIDを返すまで process_refund をブロック | 「エスカレーション基準＋few-shot」 |

**頻出ポイント / ひっかけ**
- ✅ サンプル問題1：12%で本人確認をスキップ → **プログラムによる前提条件**が正解。プロンプト強化・few-shot は確率的なので不十分、ルーティング分類器は「順序」ではなく「利用可否」の対策でズレ。
- ✅ 複数の懸案を含むリクエスト → **個別の項目に分解し、共有コンテキストで並列に調査 → 統一された回答に統合**。
- ✅ 人間の担当者は**会話記録を見られない**前提 → 顧客ID・根本原因・返金額・推奨アクションを**構造化サマリー**で渡す。

### 1.5 Agent SDK のフック（hooks）でツール呼び出しのインターセプトとデータ正規化を行う

**基礎**
- **PostToolUse**：ツール結果をモデルが処理する**前に**インターセプトして変換（正規化、トリミング）。
- **ツール呼び出しのインターセプト（PreToolUse）**：送信前の呼び出しを検査して、ポリシー違反をブロック（例：しきい値超の返金）→ 代替ワークフロー（人間へのエスカレーション）へ誘導。
- フック＝**決定論的な保証**、プロンプト＝**確率的な遵守**。

**現行SDKの事実（Agent SDK hooks ドキュメント）**
- 主なイベント：`PreToolUse`（ブロック/入力変更可）、`PostToolUse`、`PostToolUseFailure`、`UserPromptSubmit`、`Stop`、`SubagentStart`、`SubagentStop`、`PreCompact`、`PermissionRequest`、`Notification`、`SessionStart`/`SessionEnd`（後者2つはTypeScriptのみ）。
- `PreToolUse` の `hookSpecificOutput` で `permissionDecision`（`allow`/`deny`/`ask`/`defer`）、`permissionDecisionReason`（モデルに理由が伝わる）、`updatedInput`。複数フックの判定が割れたら **deny が最優先**。
- `PostToolUse` は `additionalContext`（結果に情報を追記）や `updatedToolOutput`（結果を置換）。
- matcher はツール名（`"Write|Edit"` など）。MCPツールは `mcp__<server>__<tool>`。
- Claude Code の設定ファイル版フック（コマンドフック）では **exit code 2 でブロック**（PreToolUse など、ブロック可能なイベント）。

```python
# $500超の返金をブロックしてエスカレーションへ誘導（Agent SDK / Python）
async def refund_guard(input_data, tool_use_id, context):
    amt = input_data["tool_input"].get("amount", 0)
    if amt > 500:
        return {"hookSpecificOutput": {
            "hookEventName": input_data["hook_event_name"],
            "permissionDecision": "deny",
            "permissionDecisionReason": "$500超は人間の承認が必要。escalate_to_human で引き継ぐこと"}}
    return {}  # 許可（変更なし）

options = ClaudeAgentOptions(hooks={
    "PreToolUse": [HookMatcher(matcher="mcp__support__process_refund", hooks=[refund_guard])],
    # "PostToolUse": [HookMatcher(matcher="mcp__.*", hooks=[normalize_timestamps])],  # 結果の正規化
})
```

**頻出ポイント / ひっかけ**
- ✅ 異種フォーマット（Unixタイムスタンプ、ISO 8601、数値ステータスコード）の正規化 → **PostToolUse**。
- ❌ 正規化に **PreToolUse** を選ぶ（入力側。結果は変えられない）。
- ❌ 禁止操作を **PostToolUse で事後に取り消す**（もう実行済み）。
- ❌「プロンプトを大文字・太字・繰り返しで強調」→ 確率的。

### 1.6 複雑なワークフローのためのタスク分解戦略を設計する

| | 固定の逐次パイプライン（プロンプトチェーン, prompt chaining） | 動的で適応的な分解（dynamic decomposition） |
|---|---|---|
| 向いている | 予測可能な多面的レビュー（例：ファイルごとの分析 → ファイル横断の統合パス） | オープンエンドな調査（例：レガシーに包括的なテストを追加） |
| 進め方 | 手順が事前に決まっている | 構造把握 → 影響の大きい領域特定 → 優先順位付き計画 → 発見に応じて適応 |

- ✅ 大規模コードレビューは**ファイル単位のローカル分析パス＋別途のファイル横断統合パス**（注意の分散＝attention dilution を回避）。サンプル問題12。
- ❌ 「全部まとめて1回で」「上位モデルで1パス」「3回やって多数決」。

### 1.7 セッションの状態、再開（resume）、フォーク（fork）を管理する

**基礎**
- `--resume <session-name>`：名前付きセッションの再開（Claude Code CLI。`--name`/`-n` で名前を付け、`claude --resume <name>`）。
- `fork_session`：共通の分析ベースラインから独立したブランチを作り、異なるアプローチを比較（CLIは `--fork-session` を `--resume`/`--continue` と併用。SDKはオプションで fork）。フォークは**会話履歴の分岐であってファイルシステムの分岐ではない**（現行SDKドキュメント）。
- コード変更後に再開するなら、**変更されたファイルを具体的に伝えて**的を絞った再分析。
- **古いツール結果を抱えて再開するより、構造化サマリーを注入して新規セッション**の方が信頼性が高い場合がある。

| 状況 | 選択 |
|---|---|
| 以前のコンテキストがおおむね有効、変更は一部 | **再開**＋変更ファイルを具体的に伝える |
| 以前のツール結果が大きく古くなった | **新規セッション＋構造化サマリーの注入** |
| 同じ分析から2つの戦略を比較したい | **fork_session** |

---
