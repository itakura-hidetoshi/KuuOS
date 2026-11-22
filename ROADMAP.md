# KuuOS / 空OS — Research ROADMAP

**現行研究地図（GitHub MCP観測：2026-11-22 JST）**

この文書は、新旧の「次段」を時系列に積み上げた履歴ではなく、**canonical mainに採用された範囲、独立CIで認証された範囲、開いている研究PR、未解決obstruction、次の受入条件**を同時に読むためのロードマップです。

- 正本：[`main` @ `7783385afd17`](https://github.com/itakura-hidetoshi/KuuOS/commit/7783385afd17de3b4f8953aa373ef619f5d9cc9b)
- 形式環境：Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`
- 保護：[PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) はDraft・OPEN・未マージ
- 経過記録：[ROADMAPの旧全文](docs/history/ROADMAP-THROUGH-20261121.md)、[READMEの旧全文](docs/history/README-THROUGH-20261121.md)（元Git blobの完全保存）

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

### 1.2 CodeAI v0.61研究系とLean→Python v0.61ランタイム

次の3PRは、固定Leanでの候補検証から元Pythonの2段階private追記の検査・adapterまで、**研究コードとしてmainへ統合済み**。

| 統合PR | 内容 | 統合コミット／認証 |
| --- | --- | --- |
| [#3623](https://github.com/itakura-hidetoshi/KuuOS/pull/3623) | モデル提供A/B/C候補、実CodeAIカーネル、直接Lean・実Lean MCP・別runner8宣言公理監査、候補Cの失敗診断拘束、Memory v0.2 HOLD | [`21add81e`](https://github.com/itakura-hidetoshi/KuuOS/commit/21add81e8e039553ab2f697ef8d3da1588887651)；[専用CI #44960507603](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44960507603) 3/3 SUCCESS、[Governance #44960507526](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44960507526) attempt 3 SUCCESS |
| [#3625](https://github.com/itakura-hidetoshi/KuuOS/pull/3625) | v0.53実SQLite、v0.58 tagged fork、v0.60の元監査による6経路2段階追記・不一致の回帰試験 | [`0dca3cc8`](https://github.com/itakura-hidetoshi/KuuOS/commit/0dca3cc8a69ef523946a9ad4e07d0cc8f7394925)；[Governance #44968469873](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44968469873) SUCCESS、16/16 CodeAIテスト |
| [#3626](https://github.com/itakura-hidetoshi/KuuOS/pull/3626) | [2段階private追記Python adapter](runtime/kuuos_lean_python_two_stage_private_append_v0_61.py)：元v0.60監査を第1段、第2段、初期→最終で照合し中間観測不一致・改変を拒否 | [`7783385a`](https://github.com/itakura-hidetoshi/KuuOS/commit/7783385afd17de3b4f8953aa373ef619f5d9cc9b)；[Governance #44974469696](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44974469696) SUCCESS、23/23 CodeAIテスト |

**未認証の境界：** A/Bの近接したtacticを独立した数学的戦略と見なさない。Cのlintは修復成功にしない。独立検証器v0.2は実行したが4系統・独立した組織／検証者／prompt／test／Memory来歴がなく`blocked`。そのため`verified_useful` Memory昇格はHOLDであり、モデルの重み更新も実施していない。Lean v0.61の完全な本番形式モジュールと、元Python runtimeとの一般的な意味保存証明も**NO_DATA**。研究ソースがmainに存在することはこれらの命題の認証にはならない。

### 1.3 Qi／高次縁起の段階的形式化

真正raw／Type値、依存endpoint、比較、quotient、局所compatibility、obstructionを段階的に追跡する。例：[Qi v5.96の形式記録](docs/formal/Qi-v5_96-mixed-strict-unit-provenance-obstruction-verified-20261111.md)および[統合済PR #3520](https://github.com/itakura-hidetoshi/KuuOS/pull/3520)。

- **局所成功の条件は残す。** 元の表示／証拠を後段の商同値へ逆流させない。
- **反例の射程を限定する。** 特定境界の非忠実性は、すべての型付き境界の非存在を意味しない。
- **数学と命名層を区別する。** 空・縁起・二諦・中道との関連づけは解釈でありLeanの証明結論ではない。

## 2. 開いている研究PRと直接の作業

### Track A — KuuOS-native CodeAI v0.61の次段階

**実装PR #3623／#3625／#3626はMERGED。** 各PRの指定HEAD・指定ジョブでのCI成功と、[README](README.md)・上記1.2の統合記録を参照する。以下は**未認証条件**であり、mainマージによって解消したとは扱わない。

1. 候補A/Bがモデルから提供された近接全文であることを保ち、別の生成戦略・独立した検証者／組織／session／methodの真正な来歴を取得する。現在の2候補を独立した2つの数学的証明手法とは称しない。
2. 元Lean Cの`simpa only` 2件について、実ログ・source SHAに拘束された負の診断を維持。静的Typed Error Classificationの別証拠を満たさない限り、修復成功・学習成功として登録しない。
3. 正式な4系統（Type/Formal、Behavioral/Regression、Adversarial/Falsification、Maintainability/Static）の**個別発行受領書**を、同一source/candidate/contextと独立した検証者・組織・test/prompt/Memory来歴へ紐付ける。Python回帰テスト16/23件SUCCESSは、独立発行者の証明書と同一ではない。
4. [`evaluate_independent_verifier_ensemble`](runtime/kuuos_codeai_independent_verifier_ensemble_v0_2.py)を実受領書で再評価し、未充足の間は`blocked`／HOLDを保持。受領書の真正性・時間・依存条件を満たした場合に限り、その対象subtaskだけの`verified_useful` Memory再利用を別ゲートで審査する。
5. 既存CodeAIのtyped repair、bounded cycle、独立公理監査、専門ルーティングの間で、失敗理由・修復履歴・再検証結果を版固定で渡し、未証明の自律学習やモデル重み更新を主張しない。
6. v0.61の`.lean.txt`候補を**正式Leanモジュールに採用する別PR**は、元の完全な型・imports・依存署名・固定mathlib API、公理監査、採用後Strict Lean／sourceとtest-mergeの来歴を独立に認証すること。現行mainのPython adapterとの完全精密化はさらに別の証明義務とする。

**禁止条件：** 4系統独立性未成立での`verified_useful`、旧版Memoryの無条件転用、形式証明からの自動execution authority、未認証候補を全KuuOSの真理とみなすこと。

### Track B — Dependent Origination v1.x（元の型付き証拠・endpoint RLP）

**修復PR [#3555](https://github.com/itakura-hidetoshi/KuuOS/pull/3555)**：Draft／OPEN／未マージ。観測HEAD `70a8489ee23a2c7569d923b5325c35ea405b6b3c`。

- mainには[`DependentOriginationGeneratedPresentationPosetalReflectionV1_83.lean`](formal/KUOS/DependentOriginationGeneratedPresentationPosetalReflectionV1_83.lean)等の形式ソースが存在する。しかし**ソースの存在 ≠ PR上の修正版の全体独立認証**。
- 当該HEADの[Public Proof Roots CI #44969721638](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44969721638)は**completed／SUCCESS**。他にも個別SUCCESSはあるが、PR全体のGovernance・採用後Lean認証を独立に確認するまでは全体を認証済みとしない。
- v1.83のgenerated-presentation posetal reflection、真正endpointのLeibniz／anodyne比較、Type-(A)/(B)/(C)の幾何条件、forward endpoint RLPを、**元Lean全文／imports／dependent signatures／固定mathlib API**から判定する。
- 仮定を緩めた別命題、単なる名称変更、`True`の再包装、形式的な空虚witnessによって元の要求を満たしたと称しない。
- 特定presentationにおける局所的構成と、全fiberでの一般構成、既存のobstructionを明確に分ける。

**次の受入条件：** CodeAI候補を実固定Lean／実Lean MCPで検査し、個別宣言の独立公理監査、公開root全体のStrict Lean、Governance、正確な採用HEADの再認証をすべて通す。その前のマージは禁止。

### Track C — Lean→Pythonの実OSへの接続

**現行の正本進捗：v0.60のLean/Pythonと、v0.61の条件付きPython adapterがmainへ採用済。** 課題は証明を単純にPythonへ書き写すことではなく、**元Lean命題と元Python OS処理の対応関係**を構成し、差異が出る地点を明示すること。

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

**履歴保存について**：元の相対リンクが必要な場合は[2026-11-21時点の元README](https://github.com/itakura-hidetoshi/KuuOS/blob/ac5f7db4425e7d377abce8cadee676b4e34341a4/README.md)・[2026-11-21時点の元ROADMAP](https://github.com/itakura-hidetoshi/KuuOS/blob/ac5f7db4425e7d377abce8cadee676b4e34341a4/ROADMAP.md)で読めます。以前のREADME／ROADMAPは研究の長いappend-only記録であり、古い時点の「最新」「次段」などを含みます。その元バイト列を、それぞれ[README履歴](docs/history/README-THROUGH-20261121.md)と[ROADMAP履歴](docs/history/ROADMAP-THROUGH-20261121.md)へ**同じGit blob SHAのまま**保存しました。これらは歴史的証拠の索引であり、この文書の現行認証表を上書きしません。
