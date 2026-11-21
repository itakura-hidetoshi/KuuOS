# KuuOS / 空OS — Research ROADMAP

**現行研究地図（GitHub MCP観測：2026-11-22 JST）**

この文書は、新旧の「次段」を時系列に積み上げた履歴ではなく、**canonical mainに採用された範囲、独立CIで認証された範囲、開いている研究PR、未解決obstruction、次の受入条件**を同時に読むためのロードマップです。

- 正本：[`main` @ `ac5f7db4425e`](https://github.com/itakura-hidetoshi/KuuOS/commit/ac5f7db4425e7d377abce8cadee676b4e34341a4)
- 形式環境：Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`
- 保護：[PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) はDraft・OPEN・未マージ
- 経過記録：[ROADMAPの旧全文](ROADMAP-HISTORY-THROUGH-20261121.md)、[READMEの旧全文](README-HISTORY-THROUGH-20261121.md)（元Git blobの完全保存）

## 0. 認証状態の語彙

| 状態 | この文書で意味すること | 意味しないこと |
| --- | --- | --- |
| **MERGED / canonical** | 指定PRがmainへ統合され、ソースが正本に存在 | その先の数学的・現実的主張まで自動証明 |
| **LOCAL VERIFIED** | 指定環境・指定ファイル・指定宣言で検証成功 | 別HEAD、全公開root、独立組織の検証 |
| **CI CERTIFIED (scoped)** | 同一HEADで指定workflow/jobと明記した公理監査がSUCCESS | 宣言外の全体命題、Memory昇格、merge権限 |
| **HOLD / BLOCKED** | 必要条件の検証結果不足により採用・学習・行為を保留 | 不可能性の数学的証明 |
| **PROVED IMPOSSIBLE (scoped)** | Lean等で定式化された仮定・特定構造内の反例／不存在を証明 | すべてのpresentationについての一般不可能性 |
| **NO_DATA** | 真正な根拠や独立観測がない | 成功にも失敗にも読み替えない |

最重要規則は`Preference ⇏ Descent ⇏ Authority`。候補の選好・局所的貼合・形式検証・運用権限は**別のゲート**です。

## 1. 採用済み（canonical main）

### 1.1 Lean→Python v0.60 — 共通祖先、private追記、obstruction保存

[PR #3622](https://github.com/itakura-hidetoshi/KuuOS/pull/3622)は**MERGED**。現在のmain HEADはこの統合を含みます。

- 形式化：[`LeanPythonTaggedPrivateAppendInvarianceV0_60.lean`](formal/KUOS/Architecture/LeanPythonTaggedPrivateAppendInvarianceV0_60.lean)
- 共通祖先が同じ2枝に、古いprivate値を保つ明示仮定の下で追加のprivate観測を追記する。
- old shared／private観測を保ち、重なりのcompatibilityとobstructionが追記前後で変わらないことを定式化する。
- 対応するPython側の監査・回帰は、元のOSの実行権限ではなく、**指定されたsource境界の局所的監査**である。

**未証明：** 全OSのLean↔Python双方向意味保存、元の全PlanOS出力の外部真正性、実worldとの同一性、無条件のexecution authority。

### 1.2 Qi／高次縁起の段階的形式化

真正raw／Type値、依存endpoint、比較、quotient、局所compatibility、obstructionを段階的に追跡する。例：[Qi v5.96の形式記録](docs/formal/Qi-v5_96-mixed-strict-unit-provenance-obstruction-verified-20261111.md)および[統合済PR #3520](https://github.com/itakura-hidetoshi/KuuOS/pull/3520)。

- **局所成功の条件は残す。** 元の表示／証拠を後段の商同値へ逆流させない。
- **反例の射程を限定する。** 特定境界の非忠実性は、すべての型付き境界の非存在を意味しない。
- **数学と命名層を区別する。** 空・縁起・二諦・中道との関連づけは解釈でありLeanの証明結論ではない。

## 2. 開いている研究PRと直接の作業

### Track A — KuuOS-native CodeAI v0.61

**研究PR [#3623](https://github.com/itakura-hidetoshi/KuuOS/pull/3623)**：Draft／OPEN／未マージ。研究HEAD `6dee9e0792ca435373a8e22641023b031718ad4b`。

**2026-11-22の同一HEAD認証：**

| 検証 | 実測 | 判定 |
| --- | --- | --- |
| CodeAI候補生成・直接Lean・実Lean MCP | [CI #44950277004](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44950277004)の第1job | SUCCESS |
| 別runnerによる候補A/Bの8宣言ずつのLean・公理監査 | 同runの第2job | SUCCESS（指定範囲） |
| 版固定Subtask Memoryとv0.2独立評価器を実際に実行 | 同runの第3job | SUCCESS：**`blocked`／HOLDを確認** |
| PR Governance | [CI #44950276948](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44950276948) | **30/30 SUCCESS** |
| 4系統独立検証・検証者／組織／prompt来歴の真正性 | 証拠不足 | **NO_DATA** |
| `verified_useful` Memory再利用／正式Lean採用／マージ | 独立性条件未充足 | **HOLD** |

専用CIで生じたElan HTTP 403は、既存のSHA-256検証付き固定Lean bootstrapへ切り替えて修復された。Lean／mathlib pin・証明本文・公理監査条件は変更していない。

**次の実装・認証条件（順序付き）：**

1. 3候補がモデルから事前提供された全文であることを保持し、**ライブCodeAI生成**の達成と混同しない。
2. A/Bは1箇所のtacticが異なる近接候補であり、**数学的に独立した2戦略**という主張は保留。異なる生成来歴・方法・独立検証を実際に得る。
3. Cの2件の`simp/simpa`厳格lintを、全ソース・imports・型付き原因を確認した独立Typed Error Classificationで評価する。失敗候補から成功Memoryを作らない。
4. Behavioral/Regression、Adversarial/Falsification、Maintainability/Staticを独立した証拠経路で試験し、Type/Formalと合わせて4系統・独立主体・環境・追跡可能な証拠パケットを揃える。
5. `evaluate_independent_verifier_ensemble`の実受領書を同一source／candidate／版へ結び、失敗時`BLOCKED`のまま保持。すべての条件が通った場合のみ、**その対象subtask**に限ってMemory昇格を改めて審査する。
6. 型付き候補再生成・bounded repair・trajectory-specialist routingを実CodeAI kernelと接続して試験する。モデル重み更新を実装したと称さない。
7. **別PRで**v0.61 Leanソースの正式採用を審査する場合は、採用後HEADの全依存・全公理を再認証し、source／test-merge tree一致を確認する。

**禁止条件：** 現時点での`verified_useful`発行、旧版Memoryの無条件転用、PR #3623のマージ、形式証明から自動的にexecution authorityを発行すること。

### Track B — Dependent Origination v1.x（元の型付き証拠・endpoint RLP）

**修復PR [#3555](https://github.com/itakura-hidetoshi/KuuOS/pull/3555)**：Draft／OPEN／未マージ。観測HEAD `cae0b90098e8528a13994b0b074493fc810146b3`。

- mainには[`DependentOriginationGeneratedPresentationPosetalReflectionV1_83.lean`](formal/KUOS/DependentOriginationGeneratedPresentationPosetalReflectionV1_83.lean)等の形式ソースが存在する。しかし**ソースの存在 ≠ PR上の修正版の全体独立認証**。
- 当該HEADの[Public Proof Roots CI #44955916210](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44955916210)は**completed／FAILURE**。関連する他の修復ゲートにもFAILUREや進行中のものがある。PR全体を認証済みにしてはならない。
- v1.83のgenerated-presentation posetal reflection、真正endpointのLeibniz／anodyne比較、Type-(A)/(B)/(C)の幾何条件、forward endpoint RLPを、**元Lean全文／imports／dependent signatures／固定mathlib API**から判定する。
- 仮定を緩めた別命題、単なる名称変更、`True`の再包装、形式的な空虚witnessによって元の要求を満たしたと称しない。
- 特定presentationにおける局所的構成と、全fiberでの一般構成、既存のobstructionを明確に分ける。

**次の受入条件：** CodeAI候補を実固定Lean／実Lean MCPで検査し、個別宣言の独立公理監査、公開root全体のStrict Lean、Governance、正確な採用HEADの再認証をすべて通す。その前のマージは禁止。

### Track C — Lean→Pythonの実OSへの接続

**現行の正本進捗：v0.60採用済。** 課題は証明を単純にPythonへ書き写すことではなく、**元Lean命題と元Python OS処理の対応関係**を構成し、差異が出る地点を明示すること。

| 優先する接続 | 必要な証拠 | 現状の注意点 |
| --- | --- | --- |
| MemoryOS / Plural / Wa → BeliefOS | source／型／時点／版に結びつく履歴 | 類似・要約一致だけでは元の証拠は回復しない |
| DecisionOS → VerifyOS → PlanOS | 元の型付き受領書・6経路等の局所条件・Python原本での境界試験 | 局所的simulationから全体意味保存を結論しない |
| PlanOS → ActOS → ObserveOS | 計画、許可、実行、効果、再観測の別証拠 | 受理 ≠ 実行 ≠ 効果 ≠ 認証 |
| LearnOS / CodeAI → MemoryOS | exact version／dependency／subtask／holdout独立性 | 4系統不足で昇格HOLDを維持 |

**受入条件：** Lean形式条件、Python runtimeの対応箇所、独立テスト、元のsource SHA、反例／obstruction、許可の有無を1対1に記録する。対応が証明できない箇所は`NO_DATA`を保持する。

## 3. インフラ／認証の研究課題

- **固定版の導入**：Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。Elan latestの取得失敗を依存pin変更で回避しない。署名済みとは称さず、公式release assetのSHA-256／size照合を行う。
- **時間・メモリ・キャッシュ**：依存閉包・`.olean`再利用・project build cacheを調査するが、再ビルドの省略を証明したことにしない。heartbeat panicや75分timeoutは**実行障害**として記録し、定理の証明／反証と混同しない。
- **Lean4ソースの修復**：CI指摘行だけでなく変更Lean全文、importと依存署名、固定mathlib API、elaboration failureの構造原因を読む。
- **CI release gate**：`workflow completed`、`job completed`、Lean stepの実ログ、指定宣言`#print axioms`、`sorryAx`禁止、ソース／テストマージのGit tree一致。スコープを指定した`SUCCESS`のみ認める。
- **Docs-only**：README／ROADMAPの説明変更を、追加したLean定理の形式認証とみなさない。コードへの変更がない場合、不要な全体Strict Leanを無条件には起動しない。
- **保護**：append-only／tighten-only／overwrite-forbidden／same-root、保護PR #1558をDraft／OPENで維持。マージ権限はCI受領書と区別する。

## 4. 研究の長期課題（未認証を含む）

- 型付きpresentationを横断する互換性・降下・obstructionの**必要十分条件**と、条件付きの大域貼合。
- 高次のwhiskering／coherence／endpoint RLPで、局所witnessと全域自然性・構成可能性の差を埋める。
- 各OSのLean→Python意味保存を、指定された操作・型・保存量から拡張する。外部worldや現実行為への権限は独立の許可経路を要求する。
- CodeAIの検証4系統・独立主体・学習Memoryの発行者認証・再観測をつなぎ、**根拠に応じた有限の再利用**を可能にする。

これらは研究目標であって、全KuuOS完成・AIの無条件自律実行・数学的／哲学的な絶対的正しさの宣言ではありません。

## 5. 不変条件と更新手順

1. GitHub MCPで**現行main・対象PR HEAD・保護PR #1558**を観測して対象と根拠を固定。
2. Leanの命題・元Type値・依存仮定・元runtimeの効果を守り、必要なら新しい別presentationや新規モジュールへ追記する。
3. 局所的な成功／失敗／未実行を区別し、`NO_DATA`とobstructionを残す。
4. 変更HEADに対して必要な独立CI・Governance・公理監査・source/test-merge tree一致を再実行する。
5. 修復結果のMemoryへの昇格、正式Lean採用、正本マージ、外部行為を**別々の権限判定**とする。
6. 結果を再観測してこの冒頭スナップショットを更新する。古いCIのSUCCESSを新HEADへ移してはならない。

**一次根拠**は現在の[main](https://github.com/itakura-hidetoshi/KuuOS/tree/main)、[形式ソース](formal/)、指定PRのHEADとCIジョブログです。説明文書・過去の時系列・モデル出力は、それらの代わりにはなりません。

---

**履歴保存について**：以前のREADME／ROADMAPは研究の長いappend-only記録であり、古い時点の「最新」「次段」などを含みます。その元バイト列を、それぞれ[README履歴](README-HISTORY-THROUGH-20261121.md)と[ROADMAP履歴](ROADMAP-HISTORY-THROUGH-20261121.md)へ**同じGit blob SHAのまま**保存しました。これらは歴史的証拠の索引であり、この文書の現行認証表を上書きしません。
