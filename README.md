# KuuOS / 空OS

**AIが生成した答えをそのまま正しいものとせず、条件・元証拠・証明・反証・権限を区別して、検証可能な範囲だけを採用する研究プロジェクト。**

KuuOSは、空・縁起・二諦・中道をAIの推論と行為の規律として実装する。Lean 4による形式化、Python runtime、各OSの条件付き接続、証明検索・修復・再利用を行うKuuOS-native CodeAIを同一リポジトリで研究している。LLMの確率的生成を排除するのではなく、生成を検証と採用から分離する。

> **研究スナップショット：2026-11-27 JST（GitHub MCP観測）**  
> 検証対象の正本：[`main` @ `e1d754e8e0fc`](https://github.com/itakura-hidetoshi/KuuOS/commit/e1d754e8e0fc9382001a2e698751aa11d4272b84)。  
> 研究ブランチ：[`research/codeai-nogo-memory-v1-20261126`](https://github.com/itakura-hidetoshi/KuuOS/tree/research/codeai-nogo-memory-v1-20261126)。R28まで限定範囲で独立認証済み（2026-11-27 07:19 JST）。研究成果はmainへ未統合。  
> この文書のHEADは観測対象のHEADと区別する。R28の受領書は上記の旧観測正本に拘束される。文書更新でmain HEADが変わった後の研究再開には、同一proof scope・依存・来歴の照合と新HEADに対応する受入検証が必要である。最新の実状態はGitHubのソース・CI・受領書を再観測する。

[ROADMAP.md](ROADMAP.md) は受入条件と未解決問題を示す。過去の記録は削除せず、[2026-11-22版README](docs/history/README-SNAPSHOT-20261122.md)・[同ROADMAP](docs/history/ROADMAP-SNAPSHOT-20261122.md)および[それ以前のREADME](docs/history/README-THROUGH-20261121.md)・[ROADMAP](docs/history/ROADMAP-THROUGH-20261121.md)に保存する。

## 1. 何に使うのか

| 課題 | KuuOSで研究する方法 | 現時点の射程 |
| --- | --- | --- |
| AIのハルシネーション・根拠のない一般化 | 観測と推論を分離し、正の証拠・No-Go・未確認を区別。結論に必要な条件と元の来歴を残す | 一般LLMのハルシネーション消滅を証明したわけではない |
| 数学・形式証明の研究 | 既存定理・完全型・依存関係を検索し、未解決の前提だけを探索。Leanで実際の証明項を検査し独立CIで再認証 | 現在のCodeAI研究は対象範囲を固定した実験。任意の数学の完全自動証明は未認証 |
| 同じ計算・証明の繰返し | 版固定の失敗記憶、証明DAG、コンパイル済み証明カプセル、型付き再利用、認証済みLean成果物の共有 | キャッシュ一致や類似度だけでは証明を採用しない |
| 局所情報からの大域判断 | compatibility、貼合・降下、obstructionを条件付きで形式化 | 一つのpresentationや観測から全体を実体化しない |
| エージェントの意思決定・行為 | MemoryOS、BeliefOS、DecisionOS、VerifyOS、PlanOS、ActOS、ObserveOS等の接続と権限を区別 | 証明の成立は現実世界への実行許可ではない |

関連する応用研究として、[4d-mass-gap](https://github.com/itakura-hidetoshi/4d-mass-gap) ではYang–Mills質量ギャップに関する形式数学研究を別正本で進める。これはKuuOSの研究経路を難しい数学へ適用する実験であり、ミレニアム問題の解決を宣言するものではない。

## 2. 四基盤と形式数学

| 基盤 | 運用の意味 | 数学的な研究対象 |
| --- | --- | --- |
| 空 | 出力・証明・記憶・WORLD・presentationを自己権威化しない | 型、証拠、関係的意味論、同値と不変量 |
| 縁起 | 条件・端点・依存・元Type値・変換履歴を保存する | 依存型、高次圏論、層、局所化、降下、ホモトピー |
| 二諦 | 数学的成立・runtime観測・行為権限を別の層で扱う | 型付き意味論、精密化、証明と実行の境界 |
| 中道 | 未確認を捏造して採用せず、根拠のない全面否定もしない | 三状態の証拠、条件付き決定、obstruction |

この対応づけは[Fourfold Core](docs/KUOS_FOURFOLD_CORE_v0_1.md)・[Core Charter](docs/KUOS_CORE_CHARTER_v0_1.md)の**命名・解釈層**であり、Leanが仏教思想そのものを証明したことにはならない。縁起の一般理論はC60以前から存在し、C60・五行・曼荼羅等は重要な具体的presentationであって、一般理論の唯一の根拠ではない。

### 具体例：局所的に正しくても、大域化できるとは限らない

[ScopedGluing.lean](formal/Kuu/LivingEngi/ScopedGluing.lean) は、通常の関数の層において被覆条件の下で局所compatibilityと大域切断の存在を対応させ、重なり上の不一致から大域化の不存在を証明する。[SourceAwareOverlapDescentCriterion.lean](formal/Kuu/LivingEngi/SourceAwareOverlapDescentCriterion.lean) は選択した観測の貼合に加え、元atlasの重なり上のfiber忠実性を必要とする条件を定式化する。元の値を消した商で観測が一致しても、元の値が一致するとは限らない。

この数学をAIの研究規律へ接続する際は、正確な命題Pの証明がある状態、¬Pの証明がある状態、どちらも未確認の状態を区別する。検索の失敗、タイムアウト、エラーは¬Pの証明ではない。

`Preference ⇏ Descent ⇏ Authority`。選好・条件付き貼合・正式採用・行為権限は別の判定である。

## 3. 現在の正本と研究成果（区別して読む）

### A. canonical mainに存在する成果

| 系統 | 正本の状態 | 保持する境界 |
| --- | --- | --- |
| Lean→Python | [PR #3622](https://github.com/itakura-hidetoshi/KuuOS/pull/3622) v0.60、[PR #3626](https://github.com/itakura-hidetoshi/KuuOS/pull/3626) v0.61 Python adapter、[PR #3628](https://github.com/itakura-hidetoshi/KuuOS/pull/3628) 元候補Aと同一blobの[8宣言Leanモジュール](formal/KUOS/Architecture/LeanPythonTwoStagePrivateAppendModelCandidateAV0_61.lean)がMERGED | v0.61の公開root import [PR #3629](https://github.com/itakura-hidetoshi/KuuOS/pull/3629) はDraft・OPEN。全OSのLean↔Python一般精密化は未証明 |
| CodeAI v0.61検証基盤 | [PR #3623](https://github.com/itakura-hidetoshi/KuuOS/pull/3623)・[PR #3625](https://github.com/itakura-hidetoshi/KuuOS/pull/3625)・[PR #3626](https://github.com/itakura-hidetoshi/KuuOS/pull/3626) MERGED、[PR #3630](https://github.com/itakura-hidetoshi/KuuOS/pull/3630) 実Lean MCPの`simpa`位置特定修復 | 4系統独立検証・独立発行者・`verified_useful` Memory昇格の条件は別。旧HOLDを無条件に解除しない |
| CodeAI 既存証明検索 v0.3〜v0.5 | [PR #3638](https://github.com/itakura-hidetoshi/KuuOS/pull/3638) 必須既存証明照合、[PR #3639](https://github.com/itakura-hidetoshi/KuuOS/pull/3639) exact-tree全ソース字句索引、[PR #3640](https://github.com/itakura-hidetoshi/KuuOS/pull/3640) 3宣言カーネル記憶、[PR #3641](https://github.com/itakura-hidetoshi/KuuOS/pull/3641) 10宣言追加・合計13宣言の版固定記憶 | 選択された完全型・直接証明参照の記憶であり、完全な推移依存閉包・意味検索・新規性証明ではない |
| 認証済みLean共有キャッシュ | [PR #3643](https://github.com/itakura-hidetoshi/KuuOS/pull/3643)・[PR #3644](https://github.com/itakura-hidetoshi/KuuOS/pull/3644) MERGED。正本由来の固定proof scopeと成果物digestを検証して別PR・別runnerへ再利用 | 同一scopeを越えた無条件再利用は禁止。miss・期限切れ・不一致は通常のStrict Leanへ戻す |
| Qi v5.99・F112 | [PR #3631](https://github.com/itakura-hidetoshi/KuuOS/pull/3631) [v5.99真正C60 gaugeと元18D sourceの橋](formal/KUOS/Architecture/QiWuxingGK5CHP77C60GaugeOriginalSourceBridgeV5_99.lean)、[PR #3632](https://github.com/itakura-hidetoshi/KuuOS/pull/3632)・[PR #3633](https://github.com/itakura-hidetoshi/KuuOS/pull/3633)・[PR #3636](https://github.com/itakura-hidetoshi/KuuOS/pull/3636) 真正north C60・五行・K5境界の条件付き橋と[元F45五段階の実構成](formal/Kuu/F112/PolygonNativeC60NorthWuxingK5ActualFiveStageGauge.lean)がMERGED | 三つのgaugeを同一視しない。公開root追加 [PR #3635](https://github.com/itakura-hidetoshi/KuuOS/pull/3635) とphase↔sector同値 [PR #3637](https://github.com/itakura-hidetoshi/KuuOS/pull/3637) はDraft・OPEN。14-cell全体・高次大域降下の新規認証を主張しない |

[正本v0.5の実装](runtime/kuuos_codeai_prior_proof_kernel_memory_v0_5.py)・[研究受付ゲート](runtime/kuuos_codeai_prior_proof_kernel_research_gate_v0_5.py)・[v0.5証拠記録](docs/CodeAI/PRIOR_PROOF_KERNEL_MEMORY_v0_5.md)。正本のfull runtime [CI #45711044342](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45711044342) とsharded Governance [CI #45711044643](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45711044643) は観測した正本HEADでSUCCESS。これは全workflowが常に成功するという意味ではない。

### B. CodeAI次世代研究：R7〜R28（main未統合）

研究ブランチでは、既存Leanソースの字句検索から、コンパイル済み`.olean`の完全型・証明を直接読む方式へ拡張している。

| 段階 | 認証された範囲・状態 |
| --- | --- |
| R7 | 分割収集・独立集約 [CI #45774874136](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45774874136) SUCCESS。型構造索引47,705件、対象2,815モジュール中2,120観測、695 HOLD。完全型取得済み2,390件、否定構造候補5,558件（反証可能性の索引であり全てが任意の目標に適用できるわけではない） |
| R17〜R22 | 再帰的前提探索、複数前提AND–OR、定理名を指定しない最上位探索、閉じた証明DAGと特殊化部分証明共有。例：R20 [CI #45811079734](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45811079734)、R22 R2 [CI #45882835148](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45882835148) |
| R23〜R25 | コンパイル済み証明カプセル、来歴固定登録簿、目標の完全型・`isDefEq`に基づく正・負の型付き再利用。R25 [CI #45896476614](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45896476614)：4新規証明項・6監査、2目標HOLD |
| R26 R2 | [CI #45898216584](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45898216584) SUCCESS。再帰探索途中の前提にカプセル・No-Goを適用。17宣言監査、正の3経路、該当経路だけの遮断、代替経路保持 |
| R27 R2 | [研究HEAD `4b3889aa3f5b`](https://github.com/itakura-hidetoshi/KuuOS/commit/4b3889aa3f5bb2c287721b772c4e9b580326cc5a)、[CI #45901313851](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45901313851) SUCCESS。5候補（正3・負2）、7種類の閉じた目標、24宣言監査、再探索比較キャッシュヒット35回、カプセル再構築0・外部provider呼出し0 |
| R28 | [研究HEAD `c05a986ecd57`](https://github.com/itakura-hidetoshi/KuuOS/commit/c05a986ecd571a1b00da255a7552ee8a54b4a709)、[CI #45902979815](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45902979815) SUCCESS。7件の記憶を別runnerへ同一バイトで移送し、新しい8目標中6件を型付き再適用（正4・負2）、11宣言監査、HOLD2件。候補比較探索・最上位探索・カプセル再構築・外部provider呼出し各0。改変・再ハッシュ・scope／登録簿／live型変更の5拒否試験成功 |

**上記は研究ブランチの限定実験であり、mainの本番機構と同一ではない。** 既存の真正native C60 F55由来の値を使うR25〜R28の主要例はBool添字・Unit基底の抽象二局所モデルであり、C60の幾何学的被覆を証明するものではない。全探索、任意の依存型、全No-Goの網羅、異なるLean版への移送、外部モデルによる自律生成の性能は未認証。比較キャッシュは証明そのものではない。

### C. その他の開いた研究

- 高次縁起v1.x：[PR #3555](https://github.com/itakura-hidetoshi/KuuOS/pull/3555) Draft・OPEN（観測HEAD `a637438ceebd`）。型付きDuskin輸送・scaling・endpoint RLPの個別認証はPR全体の採用を意味しない。[PR #3548](https://github.com/itakura-hidetoshi/KuuOS/pull/3548) はv1.111のvalidation-only。
- [PR #3637](https://github.com/itakura-hidetoshi/KuuOS/pull/3637)：真正ZMod5 phase↔五つの元north F45物理sectorの同値。[CI #45251598224](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45251598224) SUCCESS、6宣言の限定認証。mainには未統合。
- 保護[PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558)：Lean 4.31 validation-only、Draft・OPEN、変更・マージ禁止。

## 4. CodeAIの運用構造

```text
要求・対象WORLD・元の型・正本HEAD
  → 既存証明とNo-Goの検索（字句索引／完全型／依存）
  → 型付き適用・前提のAND–OR探索・証明DAG
  → 認証済み証明カプセルと版固定記憶を照合
  → 未解決部分だけ候補生成・修復
  → GitHub隔離Sandboxで固定Lean直接検証
  → 実Lean MCPで診断・ゴール・公理監査
  → Sandbox GREENの場合のみ別runner独立CI
  → 公開root・Governance・採用権限
  → 再観測・append-only記憶
```

上図はmainの既存機構と研究段階R7〜R28を結びつける**設計図**であり、全機能を単一汎用経路として正式採用したことを意味しない。

CodeAIの学習はモデル重みの更新ではなく、証拠・失敗・修復・版・依存・検証履歴を保存し、再利用条件の下で適用することを指す。実際に独立認証された負の証明は、対応する条件下の経路だけを遮断する。探索失敗だけで他の経路を消さない。

## 5. 各OSの役割

| 層 | 役割 |
| --- | --- |
| MemoryOS / Plural / Wa | 文脈・元証拠・履歴・異なるpresentation・版固定記憶 |
| BeliefOS | 証拠付き信念・不確実性の更新 |
| DecisionOS / VerifyOS | 評価・選択・型／来歴／監査条件を検証 |
| PlanOS | 条件付き計画とobstruction |
| ActOS / ObserveOS | 許可された作用・結果の独立観測 |
| LearnOS / CodeAI | 証明検索、候補生成、修復、限定的な学習記憶 |
| Qi・陰陽五行・曼荼羅等 | 複数の関係的・有限・高次モデルと比較 |

これは機能設計の見取り図であり、全接続について形式精密化が証明済みという主張ではない。

## 6. 固定環境と認証規律

| 項目 | 値 |
| --- | --- |
| 正本 | `main` |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| proof scope（観測正本） | `2d9d0c313b6f7d8e4df0900fd0977324999a4200c1ed3c1adb178706370dbd6b` |
| Strict Lean | `-DwarningAsError=true` / `-DsorryAsError=true` |
| 公理監査 | 指定宣言の実ログで標準3公理 `propext`、`Classical.choice`、`Quot.sound` の範囲のみ。新規公理・sorry禁止 |
| 保護 | append-only / tighten-only / overwrite-forbidden / same-root、保護PR #1558維持 |

[公開Lean root](formal/KuuOSFormal.lean) の標準検証：

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
```

正本成果物の再利用は[認証済みcache実装](scripts/ci_verified_lean_project_cache_v1.py)で来歴・依存・scopeを確認する。正本publisher [CI #45615980980](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45615980980) は10,433/10,433 Lean工程を通過し、別runner [CI #45700676928](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45700676928) は同一認証artifactを復元して同じStrict Lake検査を4.74秒で完了した（[PR #3644](https://github.com/itakura-hidetoshi/KuuOS/pull/3644) の記録に限定した測定値）。新規・変更Leanの検証を省略する保証ではない。

## 7. 読み方・参加・著作権

まず[四基盤](docs/KUOS_FOURFOLD_CORE_v0_1.md)・[ROADMAP](ROADMAP.md)、次に[Lean形式ソース](formal/)・[runtime](runtime/)・[実験と検査](scripts/)・[テスト](tests/)を読む。各研究の証拠は対象HEADのLean定理・依存・実CIログを優先し、[CONTRIBUTING.md](CONTRIBUTING.md)と[AGENTS.md](AGENTS.md)の規律に従う。

研究・設計：**Hidetoshi Itakura（板倉英俊）**。著作権・ライセンスは各ファイルの表示と[LICENSE](LICENSE)（Apache License 2.0）を参照。

**English overview:** KuuOS is a research project for evidence-bound AI reasoning, contextual dependency, typed proof reuse, explicit obstructions, and separated action authority. Its Lean formal results concern specified mathematical structures, not the truth of Buddhist philosophy. Canonical main includes a selected version-bound CodeAI kernel-memory system and verified cross-PR Lean artifact reuse. The separate R7–R28 research series studies typed proof and No-Go retrieval, AND–OR premise search, proof capsules, and portable recall; R28 is independently verified in its bounded research scope (seven memory records, six newly checked applications, two HOLD outcomes, eleven audited declarations and byte-identical memory transport). General automatic theorem proving, complete semantic search, blanket hallucination elimination, and execution authority are not claimed.
