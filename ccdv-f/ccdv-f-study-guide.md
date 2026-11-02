# CCDV-F（Claude Certified Developer – Foundations）学習ガイド ― 日本語受験用

> 作成日：2026-11-03（JST）／対象：**試験ガイド バージョン1.0（発効：2026年7月）** の出題範囲
> 2026年12月7日の改定版（改定ガイドは11月17日公開予定）は**対象外**です。11/10前後に受験するなら v1.0 で正しい。
> 表記は日本語版試験ガイドの用語に合わせ、英語原文を（ ）で併記しています。
> 「要確認」が付いた箇所は、公式情報で裏付けが取れていないか、モデルによって挙動が異なる点です。
> 模擬試験は**オリジナル問題**で、実際の試験問題ではありません（試験内容は秘密保持契約の対象）。

---

## 0. 試験概要と使い方

### 0-1. 試験概要（出典：公式試験ガイド v1.0 §5、Partner Academy FAQ）

| 項目 | 内容 |
|---|---|
| 資格 | Claude Certified Developer – Foundations |
| 試験コード | CCDV-F |
| 問題数 | 53問 |
| 出題形式 | 択一式（multiple-choice）と複数選択式（multiple-response）。**各問に選ぶ数が明記される** |
| 制限時間 | 120分（受付などを含む着席時間は約135分：FAQ） |
| 実施方法 | 監督付き。オンライン監督（OnVUE）または Pearson VUE テストセンター |
| 合格点 | スケールスコア100–1,000のうち720 |
| 受験料 | $125 USD（パートナーティアにより割引。今回はパートナー経由で無料の想定） |
| 有効期間 | 12か月（期限内なら無料の監督なしアセスメントで更新） |
| 結果 | 試験終了時に画面に表示。スコアレポートに分野別の正答率が出る（合否判定には使われない） |
| 言語 | 英語と日本語（FAQ）。**Pearson で予約するときに「日本語」を選ぶ** |
| 持ち込み | 不可。ブラウザの翻訳ツールも不可（FAQ） |
| 前提条件 | なし（推奨：ソフトウェアエンジニアリング1〜5年、Claudeなどの実務6か月以上、Python/TypeScript、REST API・CLI） |
| 予約変更 | **48時間前まで**（FAQ・Pearson）。試験ガイドには24時間とあるが、厳しい方の48時間で考える |

### 0-2. 配点表（分野ごとの推定出題数は53問×配点比率）

| 順 | 分野（日本語版ガイド） | 英語原文 | 配点 | 53問中の目安 | 本ガイドの模試 |
|---|---|---|---|---|---|
| 1 | 分野2：アプリケーションと統合 | Applications and Integration | **33.1%** | 約17〜18問 | 10問 |
| 2 | 分野5：モデルの選択と最適化 | Model Selection and Optimization | 16.8% | 約9問 | 5問 |
| 3 | 分野1：エージェントとワークフロー | Agents and Workflows | 14.7% | 約8問 | 4問 |
| 4 | 分野6：プロンプトとコンテキストのエンジニアリング | Prompt and Context Engineering | 11.0% | 約6問 | 3問 |
| 5 | 分野8：ツールとMCP | Tools and MCPs | 10.6% | 約5〜6問 | 3問 |
| 6 | 分野7：セキュリティと安全性 | Security and Safety | 8.1% | 約4問 | 3問 |
| 7 | 分野3：Claude Code | Claude Code | 3.1% | 約1〜2問 | 1問 |
| 8 | 分野4：評価、テスト、デバッグ | Eval, Testing, and Debugging | 2.6% | 約1〜2問 | 1問 |

**スキル単位の配点**（試験全体に対する割合）の上位は次のとおりです。
Claudeアプリケーションの設計 8.6%、ソフトウェアエンジニアリングの基礎 7.4%、Claude APIの仕組み 6.8%、技術的な基礎 6.1%、Claudeによるエージェントの構築 5.3%、LLMの基礎 5.2%。
**この6スキルだけで約39%を占めます。**

### 0-3. 使い方
1. 各章の「★」を最優先に読む（時間がなければ★だけ）。
2. 「ひっかけ」の表は、試験直前にもう一度読む。
3. 模擬試験（`ccdv-f-mock-exam.html`、解答と解説つき）を**65分**で解く。53問120分のペースは1問あたり約2.26分で、30問なら約68分。見直しの時間を残すために65分を目標にする。
4. 間違えた問題の分野をこのガイドで読み直す。公式の Prep Course（Partner Academy、5講座、合計774分）も並行して進めるのが理想。

### 0-4. 7日間のスケジュール（11/3〜11/9、1日2〜3時間）★

| 日付 | ★最短版（約2時間） | 余裕があれば（+1時間） |
|---|---|---|
| 11/3（火） | 第0章、第1章（分野2）前半：API・バッチ・キャッシュ | 試験ガイド（日本語版）を通読 |
| 11/4（水） | 第1章 後半：設計・構成管理・ソフトウェアエンジニアリング | Prep Course「Production-Grade Prompting, Agents & Tool Use」（209分）の前半 |
| 11/5（木） | 第2章（分野5）：LLMの基礎・effort・モデル選択・コスト | Prep Course「MSO Foundations」（57分） |
| 11/6（金） | 第3章（分野1）、第5章（分野8） | Prep Course「Claude Code, MCP & Integration」（142分） |
| 11/7（土） | 第4章（分野6）、第6章（分野7）、第7・8章（分野3・4） | Prep Course「Production Engineering, Evals & Security」（211分） |
| 11/8（日） | 模擬試験1回目（`ccdv-f-mock-exam.html`、65分）＋HTML内の解説を精読 | 弱い分野の章を読み直す |
| 11/9（月） | 間違えた問題だけ解き直す、サンプル問題、直前チェックリスト | 早めに寝る |

---
## 1. 分野2：アプリケーションと統合（Applications and Integration）33.1% ★最重要

### 1-1. Claude APIの仕組み（Claude API Mechanics）6.8% ★
**試験ガイドの範囲**：メッセージ、ツール、ストリーミング、ビジョン、思考、キャッシング、サードパーティベンダー経由の呼び出し、Messages API のデータアクセスパターン、バッチAPI、リアルタイムとバッチの選び方。

**最低限の基礎**
- Messages API は**ステートレス**。会話の履歴は毎回 `messages` に入れて送る。ロールは `user` と `assistant` が交互になる。システム指示はトップレベルの `system` に置く。
- レスポンスの `stop_reason` の主な値：`end_turn`、`max_tokens`、`stop_sequence`、`tool_use`、`pause_turn`、`refusal`、`model_context_window_exceeded`（公式「stop reasons」ページに記載あり）。
- `usage` には `input_tokens`、`output_tokens`、`cache_creation_input_tokens`、`cache_read_input_tokens` が入る。

**リアルタイムとバッチの使い分け ★**

| 観点 | Messages API（同期） | Message Batches API |
|---|---|---|
| レイテンシ | 即時。ストリーミングも可 | 非同期。多くは1時間以内、最長24時間（24時間で完了しなければ期限切れ） |
| 料金 | 通常料金 | **50%割引** |
| 上限 | — | 1バッチあたり100,000リクエストまたは256MB |
| 結果 | 即座に返る | 作成から**29日間**ダウンロード可能。**順序は保証されない → `custom_id` で照合** |
| 向いている用途 | チャット、対話型エージェント | 夜間の一括分類・要約・評価の実行 |

**プロンプトキャッシング（Prompt caching）★**
- プレフィックスは **`tools` → `system` → `messages`** の順に作られる。ある階層を変更すると、その階層と後ろの階層がすべて無効になる。
- 使い方は2つある。**自動キャッシュ**（トップレベルに `cache_control` を1つ付けると、ブレークポイントが最後のキャッシュ可能ブロックに置かれる）と、**明示的なブレークポイント**（ブロックごとに指定。最大4つ）。
- TTL は既定で5分（使うたびに無料で延長される）。1時間（`"ttl": "1h"`）も指定できる。
- 料金：書き込みは5分TTLで基本入力単価の1.25倍、1時間TTLで2倍。読み出し（ヒット）は基本単価の10%（2026年11月時点の公式ページでは、Opus 5.5 と Sonnet 5.5 は5%などモデル差あり：要確認）。
- **最小キャッシュ可能長**に満たないとキャッシュされない。**エラーは返らない**（`cache_creation_input_tokens` と `cache_read_input_tokens` がどちらも0になる）。具体的なトークン数はモデルごとに違う（要確認：公式表）。
- 振り返り（lookback）は**20ブロック**。会話が長く伸びると、前回の書き込み位置が窓の外に出てヒットしなくなることがある。そのときは途中にもブレークポイントを置く。

| ひっかけ | 正しくは |
|---|---|
| 毎回変わる部分（タイムスタンプ、ユーザー入力）の末尾にブレークポイントを置く | **変わらない部分の最後**に置く |
| ツールの並び順を毎回変えても問題ない | ツール定義を変えると**キャッシュ全体**が無効になる |
| キャッシュは短いプロンプトでも効く | 最小長未満は黙ってキャッシュされない |
| 並列の同期リクエストでコストが下がる | 単価は変わらない。安くしたいならバッチかキャッシュ |
| バッチでもキャッシュは確実にヒットする | バッチでのヒットは**ベストエフォート** |

**ストリーミング・ビジョン・思考**
- 長時間かかる応答や `504 timeout_error` には、**ストリーミング**が公式の推奨。
- ビジョン：画像を入力できる。PDF などの文書も入力できる（詳細は公式ドキュメント参照）。
- 思考：最新モデルは**適応型思考**（adaptive thinking：`thinking: {"type": "adaptive"}`。思考の量はモデルが決め、effort で調整する）。**拡張思考**（extended thinking：`thinking: {"type": "enabled", "budget_tokens": N}`）は旧来の手動方式で、Opus 4.6 と Sonnet 4.6 では非推奨、それより新しいモデルでは受け付けられない（公式のモデル概要より）。試験ガイドには両方とも出てくるので、違いを押さえておく。

**サードパーティベンダー経由（Bedrock / Google Cloud / Microsoft Foundry）**
- モデルIDの表記が異なることがある（例：Bedrock は `anthropic.` 接頭辞付き）。機能の提供状況や提供時期もプラットフォームごとに違いうる。データ所在地や課金・IAM の要件を満たしたいときの選択肢になる。

```python
# Python: Message Batches API（custom_id で照合）
import anthropic
client = anthropic.Anthropic()
MODEL = "claude-haiku-5-5"  # モデルIDは公式の Models overview で確認（要確認）
batch = client.messages.batches.create(requests=[
    {"custom_id": f"ticket-{i}",
     "params": {"model": MODEL, "max_tokens": 256,
                "messages": [{"role": "user", "content": f"分類して: {t}"}]}}
    for i, t in enumerate(["返金したい", "ログインできない"])
])
# processing_status が "ended" になったら results を取得し、custom_id で突き合わせる
```

```python
# Python: プロンプトキャッシュ（固定部分の末尾にブレークポイントを置く）
resp = client.messages.create(
    model=MODEL, max_tokens=512,
    system=[{"type": "text", "text": LONG_POLICY_TEXT,
             "cache_control": {"type": "ephemeral"}}],  # 変わらない部分の最後
    messages=[{"role": "user", "content": user_question}],  # 可変部分
)
print(resp.usage.cache_creation_input_tokens, resp.usage.cache_read_input_tokens)
```

### 1-2. Claudeアプリケーションの設計（Claude Application Design）8.6% ★スキル単位で最大
**試験ガイドの範囲**：各インターフェース（Claude Code、Desktop、claude.ai、API、SDK）でClaudeが指示をどう解釈するか、コンテンツの境界、スキーマ設計、セッションの適切な管理（セッションハイジーン）、プラグイン管理。

| インターフェース | 指示の入り口 | 押さえどころ |
|---|---|---|
| Messages API / Client SDK | `system`、`messages`、`tools` だけ | **CLAUDE.md などのファイルは自動では読まない**。必要なものはすべてリクエストに明示する |
| Claude Code（CLI など） | CLAUDE.md の階層、`.claude/rules/`、スキル、settings.json、フック | 指示（CLAUDE.md）と強制（permissions・フック）を区別する |
| Agent SDK | Claude Code と同じ仕組み。`.claude/` と `~/.claude/` から自動で読み込む（公式の SDK 概要） | 自分のプロセスに組み込んで使う |
| claude.ai / Desktop | プロジェクトの指示、アップロードしたファイルなど | 個人・チームの利用向け（詳細は要確認） |

- **コンテンツの境界**：信頼できる指示と信頼できないデータ（ユーザーの文書、Webページ、ツールの結果）を分ける。XML タグなどで区切る。
- **スキーマ設計**：ツールの `input_schema` や構造化出力のスキーマは最小限にする。必須項目・列挙型（enum）・`additionalProperties: false` を使い、説明を明確に書く。
- **セッションハイジーン**：無関係なタスクは新しいセッションで始める（Claude Code なら `/clear` など）。長いセッションでは古い文脈がドリフトの原因になる。続ける場合は要約して引き継ぐ。
- **プラグイン管理**：プラグインはスキル、エージェント、フック、MCP サーバーをまとめて配布する単位（Agent SDK 概要）。依存関係とバージョンを管理する。

| ひっかけ | 正しくは |
|---|---|
| API でも CLAUDE.md は読まれる | 読まれない（Claude Code と Agent SDK の仕組み） |
| 長い1つのセッションの方が文脈が豊富で常に有利 | 肥大化・ドリフトの原因になる。タスクごとにセッションを分ける |

### 1-3. ソフトウェアエンジニアリングの基礎（Software Engineering Foundations）7.4% ★
**試験ガイドの範囲**：REST API、JSON、非同期プログラミング、バージョン管理、SDLC への統合、コードレビュー、小規模・大規模なリファクタリング。

- **非同期処理**：同時実行数はセマフォで制限する。429 を受けたら指数バックオフで待ち、`retry-after` ヘッダーに従う。冪等性にも注意する。
- **JSON**：LLM の出力は必ず検証してからパースする（防御的なパース）。
- **バージョン管理と SDLC**：プロンプト、CLAUDE.md、`.claude/settings.json` はコードと一緒にレビューする。CI で eval を回す。
- **大規模なリファクタリング**：小さな単位に分け、テストで守りながら進める。Claude Code ならプランを立ててから実行し、差分をレビューする。

```ts
// TypeScript: 同時実行数を制限しつつ SDK の自動リトライを使う
import Anthropic from "@anthropic-ai/sdk";
const client = new Anthropic({ maxRetries: 4 }); // 既定は2回
async function runAll(items: string[], limit = 5) {
  const results: string[] = []; let i = 0;
  const worker = async () => { while (i < items.length) { const idx = i++;
    const r = await client.messages.create({ model: "claude-haiku-5-5", max_tokens: 200,
      messages: [{ role: "user", content: items[idx] }] });
    results[idx] = r.content[0].type === "text" ? r.content[0].text : ""; } };
  await Promise.all(Array.from({ length: limit }, worker));
  return results;
}
```

### 1-4. 構成管理（Configuration Management）4.1% ★
**試験ガイドの範囲**：CLAUDE.md ファイル、settings.json、モデルバージョンの固定、プロンプトのバージョン管理、プラグインの依存関係。

**Claude Code の settings.json の優先順位（上ほど強い）★**
1. 管理設定（`managed-settings.json`、MDM、サーバー管理）：個人では上書きできない
2. コマンドライン（`--settings`）
3. プロジェクトローカル（`.claude/settings.local.json`）：個人用。git には含めない
4. 共有プロジェクト（`.claude/settings.json`）：チームでコミットする
5. ユーザー（`~/.claude/settings.json`）

**CLAUDE.md の種類**

| 種類 | 場所 | 共有範囲 |
|---|---|---|
| 管理ポリシー | 例：Linux は `/etc/claude-code/CLAUDE.md` | 組織全体 |
| ユーザー | `~/.claude/CLAUDE.md` | 自分（全プロジェクト） |
| プロジェクト | `./CLAUDE.md` または `./.claude/CLAUDE.md` | チーム（コミットする） |
| ローカル | `./CLAUDE.local.md` | 自分（.gitignore に入れる） |

- `@path/to/file` で別ファイルを取り込める（インポートは最大4階層）。CLAUDE.md は1ファイル200行以内が目安（公式の memory ページ）。
- **モデルバージョンの固定**：モデルIDを設定ファイルで明示する。モデルのリリース間で互換性のない挙動変更が起こりうるので、更新前に eval で確認する。2026年11月時点の公式ページによると、4.6世代以降はモデルIDそのものが固定スナップショット。それより前の世代はエイリアスが日付付きIDを指していた（要確認：試験での扱い）。

| ひっかけ | 正しくは |
|---|---|
| 権限ルールは CLAUDE.md に書けば守られる | CLAUDE.md は**指示**。強制するなら settings.json の permissions（allow/ask/deny）か、フック |
| 個人の上書きは `.claude/settings.json` に書く | `.claude/settings.local.json` に書く |
| 環境変数はいつも settings ファイルに負ける | 環境変数は優先順位の階層には入らず、キーの組み合わせごとに決まる（例：`ANTHROPIC_MODEL` はファイルの `model` より優先） |

### 1-5. 要件の理解（Understanding Requirements）3.4% ／ 1-6. システムライフサイクル（Systems Life Cycle）2.8%
- ビジネス要件を、機能要件（何をするか）と非機能・インフラ要件（レイテンシ、コスト、データ所在地、可用性、監査）に分ける。非機能要件に応じて、モデル、バッチかリアルタイムか、提供プラットフォームを選ぶ。
- 要件は**評価可能な受け入れ基準**にしてから作る。
- ライフサイクル（開発 → 導入 → 運用 → 保守）：モデルの廃止予定（Retirement）を把握し、移行計画を立てる。監視とロールバック手順も用意する。

---

## 2. 分野5：モデルの選択と最適化（Model Selection and Optimization）16.8%

### 2-1. LLMの基礎（LLM Fundamentals）5.2% ★
**試験ガイドの範囲**：トークン、コンテキストウィンドウ、サンプリング、非決定性、次トークン生成、モデルのオプション（高速モード、拡張思考、適応型思考、エフォートレベル）、ゼロショット・シングルショット・マルチショット。

- **非決定性**：公式の用語集には「temperature を0にしても完全には決定的にならない」とある。テストは完全一致ではなく、ルーブリックやスキーマで判定し、複数回試行する。
- **コンテキストウィンドウ**：入力と出力を合わせたトークンの上限。2026年11月時点の現行モデルは1Mトークン、最大出力は128K（公式のモデル概要。試験時点の数値は要確認）。
- **`max_tokens`** は**出力**の上限で、思考も含む。入力の肥大化対策にはならない。
- **effort**（`output_config.effort`）：`low`、`medium`、`high`、`xhigh`、`max`。`low` は最も効率的（サブエージェントなどの単純なタスク向け）、`max` は最大性能。**既定値はモデルによって違う**（例：Opus 5.5 と Haiku 5.5 は `medium`、それ以外の多くは `high`。2026年11月時点）。`xhigh` に対応していないモデルもある。
- **高速モード**（fast mode）：`speed: "fast"` で、出力速度が最大2.5倍。割増料金で、対応モデルは限られる（2026年11月時点では Opus 5.5 など）。キャッシュとの関係：速度の設定を切り替えると system と messages のキャッシュが無効になる。

| ひっかけ | 正しくは |
|---|---|
| temperature 0 なら完全に決定的 | 完全には決定的にならない |
| `max_tokens` を増やせば長い入力も入る | 入力の上限はコンテキストウィンドウ。`max_tokens` は出力の上限 |
| effort は思考を有効にしたときだけのパラメータ | 応答全体のトークン消費を制御する主要なパラメータ |

### 2-2. 技術的な基礎（Technical Fundamentals）6.1% ★
**試験ガイドの範囲**：REST API をラップする SDK との統合、WebSocket。

- 公式の Client SDK は REST API のラッパー。一時的な失敗（接続エラー、429、5xx）を**既定で2回**、指数バックオフで自動リトライし、`retry-after` に従う。回数は `max_retries`（TypeScript では `maxRetries`）で変えられる。
- エラーとレスポンスには `request_id`（`request-id` ヘッダー）が付く。SDK では `_request_id` で取得できる。
- WebSocket：双方向の常時接続。音声などのリアルタイム用途で出てくる。Claude の Messages API はストリーミング（SSE）を使う。WebSocket を使う API の詳細は要確認。

### 2-3. モデルの選択とトレードオフ（Model Selection and Tradeoffs）2.7%

| ティア | 公式の位置づけ（モデル概要、2026年11月） | 典型的な用途 |
|---|---|---|
| Haiku | 大量でレイテンシに敏感なタスク（分類、抽出、ルーティング） | 前処理、ルーティング、サブエージェント |
| Sonnet | 速度と知性のバランスが最も良い | 汎用、多くの本番ワークロード |
| Opus | 長時間のエージェント的なコーディングや知識労働 | 難しい推論・コーディング |
| （Fable 5.1） | 高度な推論、長期的なエージェント作業（2026年11月時点の公式ページ） | 試験ガイド v1.0 には登場しない。要確認 |

- モデルを切り替えるときは、互換性のない挙動変更（試験ガイドに明記）がありうるので、**eval を回し直す**。effort の既定値も変わりうる。

### 2-4. コストとトークンの管理（Cost and Token Management）2.8%
- `usage` でトークンを追跡する。コストのモデル化は「入力 × 単価 + 出力 × 単価 + キャッシュの書き込み・読み出し」で行う。
- キャッシュのチェックポイント（ブレークポイント）設計、バッチの50%割引、小さいモデルへのルーティング、effort の調整、出力を短くする指示を組み合わせる。

---

## 3. 分野1：エージェントとワークフロー（Agents and Workflows）14.7%

### 3-1. エージェントアーキテクチャ（Agent Architecture）4.5% ★

| | ワークフロー | エージェント |
|---|---|---|
| 制御 | 手順をコードで固定（チェーン、ルーティング、並列化） | モデルが次の行動を決める（ツール使用ループ） |
| 向いているもの | 手順が決まっていて、再現性・監査が必要 | 手順を事前に決められない、開かれたタスク |
| コストと予測可能性 | 低コストで予測しやすい | 高コストで変動しやすい |

- **マネージャー／スーパーバイザー階層**：オーケストレーターがタスクを分解して、ワーカー（サブエージェント）に割り当てる。
- **サブエージェントの役割**：コンテキストの分離、専門化（独自のシステムプロンプトやツール制限）、独立したタスクの並列化。

### 3-2. Claudeによるエージェントの構築（Agent Construction with Claude）5.3% ★

| 選択肢 | 誰が動かすか | 特徴（公式の Agent SDK 概要） |
|---|---|---|
| Agent SDK（Python/TS） | 自分のプロセス（セルフホスト） | Claude Code のエージェントをライブラリとして組み込む。組み込みツール、権限、セッション、フック、サブエージェント、MCP |
| Claude Code CLI | 開発者の端末 | 対話的な開発や単発のタスク。`-p` でヘッドレス実行 |
| Client SDK | 自分のコード | API に直接アクセスする。ツールループは自作（または β の tool runner） |
| Managed Agents | Anthropic がホスト | ホスト型のハーネス。Anthropic 管理のクラウドサンドボックスか、セルフホストのサンドボックス。**2026年11月時点ではベータ** |

- **決定論的なアクションのためのフック**：`PreToolUse` で阻止・修正、`PostToolUse` で後処理。プロンプトの指示は確率的で、フックは確実に実行される。

```python
# Python (Agent SDK): .env への書き込みを PreToolUse フックで拒否（公式例を簡略化）
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, HookMatcher
async def protect_env(input_data, tool_use_id, context):
    if input_data["tool_input"].get("file_path", "").endswith(".env"):
        return {"hookSpecificOutput": {"hookEventName": input_data["hook_event_name"],
                "permissionDecision": "deny", "permissionDecisionReason": "no .env"}}
    return {}
options = ClaudeAgentOptions(hooks={"PreToolUse": [HookMatcher(matcher="Write|Edit", hooks=[protect_env])]})
```

### 3-3. エージェントのパターンとフレームワーク（Agent Patterns and Frameworks）4.9%
- パターン：ツール使用ループ、サブエージェント、メモリ、コンテキストウィンドウの管理。
- 抽象化フレームワーク（試験ガイドの例）：Strands、LangGraph、PydanticAI。素早く作れる反面、内部で何が起きているかが見えにくくなる（デバッグや制御が難しくなる）というトレードオフがある。各フレームワークの細かい API は出題範囲として要確認なので、深追いしない。

| ひっかけ | 正しくは |
|---|---|
| なんでもマルチエージェントにすれば品質が上がる | コストと複雑さが増える。決まった手順ならワークフロー |
| サブエージェントは親の会話を全部引き継ぐ | 独自のコンテキストで動き、要約を返す |
| サブエージェントはトークンを消費しない | 同じ利用上限に計上される |

---

## 4. 分野6：プロンプトとコンテキストのエンジニアリング（Prompt and Context Engineering）11.0%

### 4-1. プロンプトエンジニアリング（Prompt Engineering）4.6% ★
**試験ガイドの範囲**：指示の明確さ、少数ショットの例、システムとユーザーのどちらに置くか、出力の制約、コンポーネント間での指示の配置、反復的な改良、プロンプトの調整、入力のサニタイズ。
- 安定した役割・ルールは `system` に、タスクの入力や文書は `user` に置く。文書は `<document>` などのタグで区切る。
- 少数ショットの例は、多様で、期待する形式に正確に合わせる（偏った例は出力も偏らせる）。
- 反復的な改良：eval の結果を見て1か所ずつ変える。失敗例を具体的に分析する。
- 入力のサニタイズ：区切り文字を壊す入力や、制御用の文字列を処理する。

### 4-2. コンテキストエンジニアリング（Context Engineering）3.8% ★
- ドリフトと肥大化の対策：ツール出力の刈り込み（API にはツール結果をクリアするコンテキスト編集 `clear_tool_uses_20250919` がある）、コンパクション（公式では長い会話にはサーバー側のコンパクションが基本）、サブエージェントでの分離。
- Claude Code：CLAUDE.md は短く保つ。一部のファイルにだけ関係する規則は `.claude/rules/`、手順はスキルに分ける（公式の memory ページ）。

### 4-3. 出力の処理（Output Handling）2.6% ★
- **構造化出力**（JSON outputs）：`output_config.format` に `{"type": "json_schema", "schema": ...}` を指定する。SDK の `messages.parse()`（Pydantic や Zod）なら検証済みの `parsed_output` が得られる。ツール入力のスキーマを保証したいなら**厳格なツール使用**（strict tool use：`strict: true`）。
- スキーマに合っていても**中身が正しいとは限らない**。業務ルールで検証する（合計の整合性、日付の範囲など）。

```python
# Python: 構造化出力（JSON outputs）
resp = client.messages.create(
  model=MODEL, max_tokens=512,
  messages=[{"role": "user", "content": f"<invoice>{text}</invoice> から抽出"}],
  output_config={"format": {"type": "json_schema", "schema": {
     "type": "object", "additionalProperties": False,
     "properties": {"total": {"type": "number"}, "date": {"type": "string"}},
     "required": ["total", "date"]}}})
data = json.loads(resp.content[0].text)
assert data["total"] >= 0  # 業務ルールの検証を省かない
```

| ひっかけ | 正しくは |
|---|---|
| 「JSON で返して」とお願いすれば十分 | 構造化出力や厳格なツール使用を使い、さらに検証する |
| 自信のある口調の出力は正しい | 鵜呑みにしない（試験ガイドに明記） |
| 文書をシステムプロンプトに入れると安全 | 信頼できないデータは指示と分ける |

---

## 5. 分野8：ツールとMCP（Tools and MCPs）10.6%

### 5-1. ツールの実装（Tool Implementation）4.4% ★
- **クライアント側ツール**（自分のアプリが実行する。`bash` や `text_editor` など Anthropic がスキーマを定義したものも含む）と、**サーバー側ツール**（`web_search`、`web_fetch`、`code_execution`、`tool_search` など。Anthropic の基盤で実行される）。
- ループの規則 ★：`stop_reason: "tool_use"` → ツールを実行 → 次の `user` メッセージに `tool_result`（`tool_use_id` で対応付け）を**先頭**に置く。テキストはその後。tool_use の直後に別のメッセージを挟まない。失敗したら `is_error: true`。
- `tool_choice`：`auto`（既定）、`any`、`tool`（特定のツールを指定）、`none`。`disable_parallel_tool_use` で並列呼び出しを止められる。**モデルや設定によっては `any` と `tool` が使えない**（例：手動の拡張思考ではエラー。2026年11月時点の公式ページでは Opus 5.5 や Sonnet 5.5 でも400エラー。代わりに `auto` と strict を使う）。これは要確認の注意点。
- ツールの説明は「何をするか、いつ使うか、引数の意味、返り値」を具体的に書く。ツールの数と重複は最小限にする。
- 承認パターン：破壊的なツールには、人間の承認やフックを挟む。

```python
# Python: クライアント側ツールのループ（最小）
msgs = [{"role": "user", "content": "東京の天気は？"}]
while True:
    r = client.messages.create(model=MODEL, max_tokens=1024, tools=TOOLS, messages=msgs)
    msgs.append({"role": "assistant", "content": r.content})
    if r.stop_reason != "tool_use":
        break
    results = []
    for b in r.content:
        if b.type == "tool_use":
            try:
                out, err = run_tool(b.name, b.input), False
            except Exception as e:
                out, err = str(e), True
            results.append({"type": "tool_result", "tool_use_id": b.id,
                            "content": str(out), "is_error": err})
    msgs.append({"role": "user", "content": results})  # tool_result を先頭に置く
```

### 5-2. MCPサーバーの開発（MCP Server Development）2.1%
- 3つのプリミティブ：**ツール**（モデルが制御する）、**リソース**（アプリが制御する読み取り専用のデータ）、**プロンプト**（ユーザーが明示的に呼び出すテンプレート）（MCP 公式ドキュメント）。
- 標準のトランスポートは **stdio** と **Streamable HTTP**（旧 HTTP+SSE の後継）。stdio では**サーバーは stdout に MCP メッセージ以外を書いてはならない**。ログは stderr に出す。

### 5-3. エージェントのカスタマイズ（Agentic Customization）4.1% ★

| 手段 | 向いているもの | 注意 |
|---|---|---|
| 組み込みツール | 汎用的なファイル操作・シェル・Web 検索 | 任意の社内 API には自動でつながらない |
| カスタムツール | 1つのアプリ固有の関数呼び出し | アプリごとに実装・保守が必要 |
| スキル（Skills） | 手順・知識・スクリプトを `SKILL.md` にまとめ、必要なときに読み込む | `description` が自動で呼び出されるかどうかを左右する。Claude Code では `/skill-name` で明示的にも呼べる。カスタムコマンドはスキルに統合された |
| MCP | 外部システムとの接続を**複数のアプリで共有**し、独立して保守したい | サーバーの権限・認証の設計が必要 |

---

## 6. 分野7：セキュリティと安全性（Security and Safety）8.1%

### 6-1. AIアプリケーションのセキュリティ（AI Application Security）3.2% ★
- **プロンプトインジェクション**（特に、Webページ・メール・ツールの結果などに仕込まれる間接型）への対策：信頼できない入力として扱い、指示と分離する。ツールは最小権限にし、機密性の高いアクションにはフックや人間の承認を挟む。
- 効かない対策（公式サンプル問題2）：temperature を上げる、「悪意ある指示に従わないで」とお願いする、大きなモデルに変える（指示に忠実なモデルほど、かえって影響を受けやすいことがある）。
- PII：最小化、マスキング、ログに残さない、データ保持ポリシー。

### 6-2. ガードレールと安全なデプロイ（Guardrails and Safe Deployment）2.3%
- ガードレールの多層化：入力のスクリーニング → 権限の制御 → 出力の検証 → 監視。セキュアバイデザイン（プライバシー、IAM、最小権限）。

### 6-3. Claudeのフック（Claude Hooks）1.0% ★
- Claude Code の主なイベント：`SessionStart`、`UserPromptSubmit`、`PreToolUse`（実行前。ブロックできる）、`PermissionRequest`、`PostToolUse`、`PostToolUseFailure`、`Notification`、`SubagentStop`、`Stop`、`PreCompact`、`SessionEnd` など。
- **終了コード2 = ブロッキングエラー**（PreToolUse ならツール呼び出しを阻止）。JSON の `permissionDecision: "deny"` でも拒否できる。**終了コード0のときの stderr は Claude には見えない**。

```json
// .claude/settings.json（チームで共有）
{ "permissions": { "deny": ["Read(./.env)"], "allow": ["Bash(npm test)"] },
  "hooks": { "PreToolUse": [ { "matcher": "Bash",
     "hooks": [ { "type": "command", "command": ".claude/hooks/block-rm.sh" } ] } ] } }
```
（settings ファイルは厳密な JSON なので、実際にはコメントは書けない。上のコメントは説明用）

### 6-4. ID、シークレット、キーの管理（Identity, Secrets, and Key Management）1.6%
- キーは環境ごとに分ける。シークレットマネージャーか環境変数で注入する。コード、CLAUDE.md、ログ、フロントエンドには置かない。ローテーションと利用監視を行い、アクセス承認のレベルを確認する。
- 401 `authentication_error`（キーが不正・失効・期限切れ）、403 `permission_error`（そのリソースへの権限がない）。

---

## 7. 分野3：Claude Code 3.1%

### 7-1. Claude Codeの操作（Claude Code Operation）3.1%
**試験ガイドの範囲**：コアコンポーネント（ルール、スキル、コマンド、エージェント、エージェントメモリ）、機能（セッション管理、組み込み・カスタムのスラッシュコマンド、ヘッドレスモード、ストリーミングモード、自動モード）、CLAUDE.md の階層、リポジトリの初期化、settings.json の設定。

| 項目 | 押さえどころ（公式ドキュメント） |
|---|---|
| `/init` | コードベースを分析して CLAUDE.md の雛形を作る。既存のものがあれば上書きせず改善を提案する |
| CLAUDE.md の読み込み | 作業ディレクトリとその上位のものは起動時に読む。サブディレクトリのものは必要になったときに読む |
| `.claude/rules/` | ファイルの種類やパスごとに範囲を絞った規則 |
| スキル | `.claude/skills/<名前>/SKILL.md`。`.claude/commands/*.md` も引き続き動く（スキルに統合済み） |
| サブエージェント | 独自のコンテキスト、システムプロンプト、ツール制限（`tools:`、`disallowedTools:`） |
| ヘッドレスモード | `claude -p "..."`。`--output-format json`（または `stream-json`）、`--allowedTools`、`--continue`、`--bare`（自動検出をスキップ。スクリプトやCIに推奨） |
| セッション管理 | `--continue`、`--resume`、`/clear` |
| 自動モード（auto mode） | 詳細は要確認（公式の permissions のページで確認） |

注意：`-p` で `--bare` を付けないと、信頼していないフォルダでもプロジェクトのフックや `.mcp.json` が動く（公式に明記）。

---

## 8. 分野4：評価、テスト、デバッグ（Eval, Testing, and Debugging）2.6%

### 8-1. デバッグとエラー処理（Debugging and Error Handling）2.6%

| HTTP | type | 対処 |
|---|---|---|
| 400 | `invalid_request_error` | リクエストを**直す**（リトライしても無駄）。設定した支出上限に達したときも400 |
| 401 | `authentication_error` | キーを確認する |
| 403 | `permission_error` | 権限を確認する |
| 404 | `not_found_error` | パスやIDを確認する |
| 413 | `request_too_large` | サイズを減らす（Messages API は128MB、Batch は256MB） |
| 429 | `rate_limit_error` | バックオフし、`retry-after` に従う（ティアの支出上限による429には retry-after がない） |
| 500 | `api_error` | 指数バックオフでリトライ。続くなら request_id を添えて問い合わせる |
| 504 | `timeout_error` | ストリーミングを使う |
| 529 | `overloaded_error` | 一時的な過負荷。バックオフしてリトライ |

- **切り分け**：HTTP エラーや例外は統合レイヤーの問題、200 で返った内容の誤りはモデル出力（プロンプトやコンテキスト）の問題。トレース（入力・ツール呼び出し・出力のログ）で、どこで失敗したかを特定する。
- 評価（eval）：「完了」の定義をテストで作る。回帰を検出し、スキーマ検証とルーブリック採点を併用する。

---

## 9. 公式サンプル問題の要点（試験ガイド §8）

| # | 分野 | 正解の考え方 | 不正解の典型 |
|---|---|---|---|
| 1 | 分野2 | 夜間の非緊急な1万件 → **Message Batches API**（24時間以内・低コスト） | 同期の並列送信、max_tokens を下げる、むやみに最小モデルにする |
| 2 | 分野7 | Web ページの隠し指示 → **信頼できない入力として分離し、ガードレールやフックで機密性の高いアクションを防ぐ** | temperature、お願いの一文、大きなモデル |
| 3 | 分野8 | 社内の REST API を複数アプリで再利用 → **MCP サーバー** | プロンプトにハードコード、データの貼り付け、組み込みツール |

**共通する型**：「強制力のある仕組み（API の機能、フック、権限、MCP）」を選び、「お願い・ランダム性・モデルの大きさ」に頼る選択肢を外す。

---
## 10. 模擬試験（HTML版）

模擬試験（30問・解答と解説つき）は `ccdv-f-mock-exam.html` で解いてください。分野別スコアもHTML上で自動集計されます。目標時間は65分です。

---

## 11. 直前チェックリスト

### 11-1. 前日（11/9）
- [ ] Pearson の予約が**日本語**になっているか確認する（英語で予約していたら、48時間前までにキャンセルして日本語で取り直す：FAQ）
- [ ] 本人確認書類（有効期限内の政府発行の写真付きID）の**ローマ字氏名が、Pearson の登録氏名と完全に一致**しているか確認する
- [ ] オンライン受験なら：Pearson のシステムテスト、個室、机の上の片付け、外部モニターを外す。社内ネットワークなら OnVUE に必要なドメインへ通信できるか確認する
- [ ] 模擬試験で間違えた問題を解き直す。この学習ガイドの「ひっかけ」表をすべて読み直す

### 11-2. 当日
- [ ] 開始の30分前には準備を終える（着席時間は約135分）
- [ ] 時間配分：53問を120分、1問あたり約2.2分。迷った問題はフラグを付けて先に進む。最後の15〜20分で見直す
- [ ] 「○つ選択」の数を必ず確認する
- [ ] 消去法：「お願い」「temperature」「とりあえず大きなモデル」「無限リトライ」「全部をコンテキストに貼る」は、たいてい誤り

### 11-3. 頻出ひっかけの総復習（★）
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

### 11-4. 出典（2026-11-03 JST に確認）
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
