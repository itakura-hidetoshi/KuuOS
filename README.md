# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)
![Qi-WORLD v2.3](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/qi-world-yinyang-process-blocker-v2-3-validation.yml/badge.svg)
![WORLD v0.59](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/world-four-great-phase-dynamics-v0-59.yml/badge.svg)
![Gauge Review v0.69](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos-external-evidence-review-v069.yml/badge.svg)

**KuuOS / 空OS**は、観測、信念、記憶、計画、判断、実行、検証、学習、WORLD表現を、由来、局所文脈、履歴、所有者、有限権限へ束縛して接続する公開研究アーキテクチャです。

KuuOS is a public, governance-gated, proof-facing, non-Markovian and Qi-process-aware architecture for relational AI systems.

KuuOSは、候補、証拠、検証、権限、実行効果、記憶、数学的表現を同一視しません。

縁起、二諦、中道、和、局所性、履歴依存性、反証可能性、修復可能性を保持したまま、各層を明示的なreceipt chainで接続します。

KuuOSはproduction AGI runtimeではありません。

## 現在地

**基準日：2026年6月28日**

**機能基準：`main`のPR #874統合後、merge commit `9a848e1344e399f762813e8b78409a4c11cd92ab`**

この基準では、Gauge-Field Self-Organization v0.60からv0.69に加え、Module-BundleとMemoryOS production chainのv0.70からv0.76までが`main`へ統合されています。

| 系列 | `main`の統合済み到達点 |
|---|---|
| Core governance | v0.1 |
| Horizon Governance / Context Gauge Atlas | v0.12 / v0.13 |
| Modular Evolution Mesh | v0.1 |
| PlanOS control | v0.17 |
| Repeatable finite-cycle agent | v0.20からv0.27 |
| Qi diagnostic candidate / lineage | v0.28 / v0.29 |
| Open Horizon | v0.30からv0.34 |
| MemoryOS foundational line | v0.35、v0.37、v0.38、v0.39 |
| Qi-WORLD | v2.3 |
| Vacuum-expectation OS chain | ObserveOS、VerifyOS、LearnOS、PlanOS、DecisionOS、ActOS、WORLDのversioned bridge |
| WORLD mathematical sidecar | v0.27からv0.59 |
| Gauge-field self-organization | v0.60からv0.69 |
| Module-Bundle and MemoryOS application chain | v0.70からv0.76 |
| Lean aggregate root | `KuuOSFormal` |
| Runtime aggregate entry | `scripts/run_kuuos_runtime_full_check_v0_55.py` |
| Lean / mathlib | Lean 4、mathlib `v4.30.0-rc2` |

`run_kuuos_runtime_full_check_v0_55.py`という名称は互換性のため保持されています。

現在の実体は、v0.55以前の累積検証に加え、v0.56、v0.59、v0.60からv0.76までの統合済みruntime validatorを依存順に実行します。

名称中のv0.55は、リポジトリ全体の最新機能番号を意味しません。

## 不変境界

```text
candidate != authority
validation != truth
formal compilation != external theorem acceptance

observation != verification
verification != truth
learning != present-cycle mutation
memory != belief sovereignty
plan commit != activation
selection != execution
receipt != successor authority

local control != global constitution
local chart != global graph
curvature != veto
holonomy != sovereign memory

WORLD sidecar != exact WORLD
WORLD candidate != empirical fact
WORLD commit != truth
analytic vacuum != exact WORLD
Kū != zero vector
modular time != physical time

connection candidate != production application
application authority != performed effect
rollback != time reversal
restored payload != restored authority
```

v0.69とv0.74では、明示的なapprovalが限定されたproduction application authorityを与えます。

ただし、review関数はlive effectまたはstate writeを実行しません。

v0.75だけが、承認receiptを一度だけ消費し、MemoryOS production stateを原子的に更新します。

v0.76だけが、commit receiptとpre-commit snapshotへ束縛された補償transactionとしてpayloadを復元します。

rollback後もrevisionは前進し、消費済みapprovalは再有効化されません。

## OSの責務

| OS | 主な責務 |
|---|---|
| ObserveOS | source-bound observation ownership |
| BeliefOS | local and plural belief-state ownership |
| DecisionOS | admissible candidate selection |
| PlanOS | plan and replan synthesis |
| ActOS | exactly licensed bounded effect |
| VerifyOS | evidence-bound independent verification |
| LearnOS | future-only learning delta |
| MemoryOS | lineage、reconstruction、conditioned retrieval、read-only history source |
| WORLD | sourced representation and governed fragment storage |

```text
ObserveOS evidence != VerifyOS verdict
VerifyOS verdict != truth authority
LearnOS delta != immediate activation
DecisionOS selection != ActOS invocation
MemoryOS retrieval != PlanOS activation
WORLD intake != WORLD update
```

## 統合済みスパイン

### ガバナンスと局所文脈

KuuOSは文脈を普遍的な固定グラフへ縮約しません。

文脈は、局所チャート、局所切断、遷移、曲率、cocycle residue、holonomyとして扱います。

```text
context
→ local chart

policy state
→ local section

compatible relation
→ chart overlap

context change
→ transition function

section movement
→ parallel transport

disagreement
→ curvature / cocycle defect

path-dependent retained history
→ holonomy
```

Horizon Governance v0.12とContext Gauge Atlas v0.13は、複数時間幅、局所性、履歴依存性を保持します。

### Modular Evolution Mesh

Modular Evolution Mesh v0.1は、固定された憲法境界の周囲へ型付きmoduleを登録し、能力依存を解決し、append-only ledgerで由来を保持します。

```text
module discovery != activation
registration != execution license
dependency resolution != effect execution
ledger receipt != truth
self-organization proposal != self-modification authorization
```

### 有限サイクルとOpen Horizon

v0.20からv0.27は、再起動可能で、利用者が中断でき、資源境界を持つ反復可能な有限サイクルを構成します。

v0.30からv0.34は、局所サイクルの停止を将来可能性全体の閉鎖へ昇格させず、外部承認された観測から原子的WORLD fragment commitまでを接続します。

```text
persistent mission
→ evidence-bearing cognitive cycle
→ bounded effect
→ independent WORLD reconciliation
→ bounded learning and memory
→ checkpoint / pause / renew / terminate / handover
```

### 気のプロセスとQi-WORLD

v0.28は、複数時点の気のプロセステンソル、複数仮説、反証、不確実性、回復可能性区間を診断候補として保持します。

v0.29は、その候補をsource、mission、lineage、historyへ束縛します。

Qi-WORLD v2.3は、Qi Process TensorとCross-Cycle Blocker Theoryを陰陽相補系として接続します。

```text
Yang
= accumulable process support

Yin
= idempotent boundary occupation

coupled admissibility
= process visibility
+ continuity
+ memory continuity
+ required blockers
+ capacity
+ context
```

この構造は、気を物理的ボース粒子へ、blockerを物理的フェルミ粒子へ同一視しません。

### WORLD数学サイドカー

`main`の統合済み数学系列はv0.27からv0.59です。

```text
real Hilbert ℓ²
→ dense and self-adjoint operator bridge
→ noncommutative operator algebra
→ C*-local net
→ von Neumann bicommutant and modular theory
→ Araki relative entropy
→ Petz recovery and conditional expectation
→ Jones theory and categorical bridges
→ higher-gauge information geometry
→ quantum Bregman and variational geometry
→ log-Sobolev contraction certificates
→ OS reflection-positive completion interface
→ analytic vacuum sector
→ vacuum-expectation candidates
→ OS receipt composition
→ Kū vacuum central reference state
→ Kū vacuum information geometry
→ verified Araki calculus and OS transport
→ closed Tomita operator bridge
→ conjugate-adjoint intermediate layer
→ four-great phase dynamics
```

Leanは、宣言された仮定の下で型付き帰結を検証します。

CI成功だけでは、外部数学界での定理受理、物理実現、経験的妥当性は成立しません。

### Gauge-Field Self-Organization v0.60からv0.69

この系列は、自己組織化を無制限な自己書換えではなく、有限候補、厳格な由来、rollback、外部reviewを持つ接続改善経路として構成します。

```text
v0.60  gauge-field self-organization foundation
→ v0.61  OS-associated gauge fields and memory holonomy
→ v0.62  finite connection candidate search
→ v0.63  governed ADMIT / REJECT / DEFER review
→ v0.64  finite snapshot evaluation
→ v0.65  sealed staging package
→ v0.66  in-memory shadow materialization
→ v0.67  finite gauge-orbit validation
→ v0.68  validity-bounded evidence capsule
→ v0.69  approval-bound external evidence review
```

v0.60は、authority、audit、provenance、rollbackの保護座標を固定したまま、局所場の適応成分だけを候補化します。

v0.61は、ObserveOS、VerifyOS、MemoryOSなどの意味チャネルへ随伴場を接続し、非マルコフ履歴をholonomyとして保持します。

v0.62からv0.68は、候補探索、review、評価、sealed staging、shadow、有限ゲージ検証、evidence capsuleをlive effectなしで進めます。

v0.69は、外部reviewer、review scope、source、candidate、rollback、有限有効期間をexact digestへ束縛します。

### Module-Bundle and MemoryOS Production Chain v0.70からv0.76

v0.70以降は、自己組織化を文脈代数上の加群、意味部分加群、authority filtration、Leibniz接続、非マルコフ記憶核として再構成します。

| Version | 統合済み責務 |
|---|---|
| v0.70 | 文脈代数上のstate module、意味射影、authority filtration、有限接続変形、gauge共変性、rollback |
| v0.71 | 非可換文脈代数、内部微分、Leibniz接続、加群線形接続差、曲率の加群線形性 |
| v0.72 | read-only MemoryOS history、有限非マルコフkernel、pathwise Leibniz則、履歴依存性の有限検証 |
| v0.73 | 有限kernel familyの完全検証、gauge-invariant score、入力順序に依存しない決定的選択 |
| v0.74 | selection recordの外部review、明示的decision、限定されたproduction application authority |
| v0.75 | approvalの一回消費、compare-and-swap、原子的MemoryOS production commit |
| v0.76 | commit receiptとsnapshotに基づく単回rollback、revision単調増加、approval再有効化の禁止 |

```text
context algebra A
+ state module M
+ semantic projectors P_i
+ authority filtration F^•M
+ Leibniz connection ∇
+ read-only history h_t
+ memory kernel K
→ validated finite candidate family
→ deterministic selection
→ external review
→ one-time atomic commit
→ audited monotonic rollback
```

v0.70からv0.73はcandidate、validation、evaluation、selection evidenceを構成します。

これらはproduction stateを変更しません。

v0.74はproduction application authorityを付与できますが、状態を書き換えません。

v0.75は明示的に承認されたpayloadだけを原子的にcommitします。

v0.76は過去へ時間を戻さず、新しいrevisionとしてpre-commit payloadを復元します。

## Lean root

`formal/KuuOSFormal.lean`は、`main`に統合された形式層のaggregate rootです。

v0.69の外部evidence reviewと、v0.70からv0.76のModule-Bundle and MemoryOS chainを直接importします。

専用rootは、各versionの局所surfaceを独立に検証するため残します。

aggregate rootは、統合後のimport欠落と境界退行を検出するための厳格build surfaceです。

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

## Runtime root

`scripts/run_kuuos_runtime_full_check_v0_55.py`は、互換名を維持した累積runtime rootです。

現在は次を実行します。

```text
legacy cumulative chain through v0.54
+ Modular Evolution Mesh v0.1
+ WORLD v0.55
+ WORLD v0.56 and v0.59 validators
+ Gauge v0.60 through v0.69 validators
+ Module-Bundle and MemoryOS v0.70 through v0.76 validators
```

```bash
PYTHONPATH=. python3 scripts/run_kuuos_runtime_full_check_v0_55.py
```

このrootの成功は、統合済みruntime surfaceの再現可能な整合性receiptです。

真理、外部定理受理、臨床承認、組織承認、無制限の実行許可ではありません。

## 次の研究前線

直近の自然な次段階は、v0.75 commit receiptとv0.76 rollback receiptをVerifyOSへ渡すpost-application verificationです。

```text
commit or rollback receipt chain
→ independent VerifyOS intake
→ VERIFIED / FAILED / INDETERMINATE disposition
→ future-only LearnOS delta
→ WORLD reconciliation candidate
```

verification failureから自動rollbackしてはなりません。

fresh rollback request、権限、snapshot、ledger CAS、append-only compensationを別に要求します。

その他の優先課題は[`ROADMAP.md`](ROADMAP.md)に記載します。

## 非主張

KuuOSは現時点で次を主張しません。

- 無制限の実行権限を持つproduction AGI。
- 任意のshell、network、repository、deploymentへの包括権限。
- 単一真理へ収束する普遍的global-context graph。
- 独立した医療診断、トリアージ、治療、医療行為承認システム。
- 気が物理的粒子であることの証明。
- LeanまたはCIの成功だけによる外部定理受理。
- 完全な物理的量子Markov semigroup、正確な物理真空、正確なWORLD simulator。
- 解析的真空と形而上学的な空の同一視。
- closed Tomita operatorだけによるpolar decompositionまたは完全な相対モジュラー理論。
- 四大診断と物質元素または確定した物理相との同一視。
- 曲率最小化またはmemory return score最小化による真理獲得。
- candidate、receipt、memory、WORLD commitの自動的な権限化。
- rollbackによる承認権限または過去状態の復活。

## 最初に読む文書

```text
README.md
ROADMAP.md
GOVERNANCE.md
CONTRIBUTING.md

docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
docs/BOUNDARY_AND_NONAUTHORITY_POLICY_v0_1.md

docs/KUUOS_GAUGE_FIELD_SELF_ORGANIZATION_v0_60.md
docs/KUUOS_CONNECTION_EVIDENCE_REVIEW_v0_69.md
docs/KUUOS_MODULE_BUNDLE_SELF_ORGANIZATION_v0_70.md
docs/KUUOS_NONCOMMUTATIVE_LEIBNIZ_CONNECTION_v0_71.md
docs/KUUOS_NONMARKOV_MEMORY_CONNECTION_v0_72.md
docs/KUUOS_MEMORY_EVALUATION_v0_73.md
docs/KUUOS_MEMORY_SELECTION_REVIEW_v0_74.md
docs/KUUOS_MEMORY_COMMIT_v0_75.md
docs/KUUOS_MEMORY_ROLLBACK_v0_76.md

formal/KUOS.lean
formal/KuuOSFormal.lean
scripts/run_kuuos_runtime_full_check_v0_55.py
```

## ディレクトリ

```text
docs/         public specifications, boundaries and status documents
runtime/      bounded runtime kernels, adapters, stores and scenarios
src/          typed modular contracts, registries and orchestration surfaces
scripts/      validators and cumulative full-check entry points
tests/        runtime regression and boundary tests
formal/       Lean and mathlib-facing formal surfaces
manifests/    versioned component and validation manifests
cases/        governance and failure-mode cases
roadmap/      specialized additive research roadmaps
.github/      reproducible CI workflows
```

## 開発原則

```text
additive lineage
same-root binding for protected surfaces
append-only evidence
explicit versioning
fail closed on stale or substituted state
finite local authority
open global possibility horizon
independent observation after effect
visible uncertainty, dissent, residue and cost
no silent promotion from candidate to authority
rollback as monotonic compensation
stable main != active research branch
```

新しい層は、入力、出力、所有者、必要権限、永続化、replay、stale-state処理、validatorの射程、外部仮定、非権限境界を明記します。

## Citation, governance and rights

引用、貢献、再利用条件は、[`CITATION.cff`](CITATION.cff)、[`GOVERNANCE.md`](GOVERNANCE.md)、[`CONTRIBUTING.md`](CONTRIBUTING.md)、repository license filesを参照してください。

**空OS、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属します。**

個別のrepository artifactの再利用は、各licenseと著作者表示に従います。

Repository artifactは、臨床権限、組織権限、数学的受理、実行権限を移転しません。
