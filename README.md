# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS**は、観測、信念、記憶、計画、判断、実行、検証、学習、WORLD表現、repository evolutionを、由来、局所文脈、履歴、所有者、有限権限、明示的なreceipt chainへ束縛して接続する公開研究アーキテクチャです。

KuuOS is a public, governance-gated, proof-facing, non-Markovian, Qi-process-aware architecture for relational AI, bounded self-evolution research, and read-only lifecycle governance.

KuuOSは、候補、証拠、検証、承認、権限、実行効果、記憶、数学的表現、repository stateを同一視しません。

KuuOSはproduction AGI runtimeではありません。

## 現在地

**基準日：2026年7月5日 JST**

**`main`の統合済み到達点：Lifecycle Stage v0.35**

**`main`の最新merge commit：`a650a8f419512679eb218d2f23401f8508c6f2b7`**

**現在のDraft frontier：PR #991、Lifecycle Completion v0.36**

**Draft branch：`codex/lifecycle-final-closure-v0-36`**

**Draft head：`e0332f1b5337cdd9ffcc2f3a73ec11b6f635adf4` before this documentation synchronization**

現在の`main`は、closed repository mutation roadmap v1.19からv1.24を完了した後、独立したread-only Apoptosis Lifecycle Governance系列をv0.35まで統合しています。

PR #991はv0.36のDraftであり、merge前は`main`の統合済み機能として扱いません。

この枝では、README、ROADMAP、CITATION、Lake package version、current runtime rootをv0.36 frontierへ同期します。

| 系列 | 到達点 | 状態 |
|---|---|---|
| Core governance | v0.1 | Frozen boundary |
| Horizon Governance / Context Gauge Atlas | v0.12 / v0.13 | 統合済み |
| Modular Evolution Mesh | v0.1 | 統合済み |
| PlanOS control | v0.17 | 統合済み |
| Finite-cycle agent | v0.20からv0.27 | 統合済み |
| Qi diagnostic candidate / lineage | v0.28 / v0.29 | 統合済み |
| Open Horizon | v0.30からv0.34 | 統合済み |
| MemoryOS foundational line | v0.35、v0.37、v0.38、v0.39 | 統合済み |
| Qi-WORLD | v2.3 | 統合済み |
| WORLD mathematical sidecar | v0.27からv0.59 | 統合済み、継続検証 |
| Gauge-field self-organization | v0.60からv0.69 | 統合済み、継続検証 |
| Module-Bundle and MemoryOS application | v0.70からv0.76 | 統合済み、継続検証 |
| v0.77 proposals | 未統合 | current rootへ含めない |
| Self-organizing improvement loop | v0.78 | 統合済み、継続検証 |
| Repository self-evolution chain | v0.79からv1.24 | 統合済み、継続検証 |
| Staged repository mutation roadmap | v1.19からv1.24 | 完了系列 |
| Checkpoint recovery proposal | v0.1 | 独立した非mutation系列 |
| Apoptosis Lifecycle Governance | v0.1からv0.35 | `main`へ統合済み |
| Lifecycle Completion | v0.36 | PR #991 Draft frontier |
| Lean aggregate root | `formal/KuuOSFormal.lean` / target `KuuOSFormal` | strict build surface |
| Current runtime root on this branch | `runtime/kuuos_current_check.py` | v1.24 repository rootとv0.36 lifecycle testを束ねる |
| Closed repository mutation runtime root | `runtime/kuuos_v124_check.py` | v1.24 cumulative mutation surface |
| Legacy compatibility runtime root | `scripts/run_kuuos_runtime_full_check_v0_55.py` | v1.02 compatibility surface |
| Lean / mathlib | Lean 4、mathlib `v4.30.0-rc2` | fixed toolchain |
| Lake package version | `0.36.0` | v0.36 lifecycle frontier alignment |

`run_kuuos_runtime_full_check_v0_55.py`という名称は既存workflowとの互換性のため保持しています。

このlegacy compatibility rootはv1.02までの従来系列を検証します。

v1.03からv1.24までを含むclosed repository mutation累積検証入口は`runtime/kuuos_v124_check.py`です。

現在の作業枝における統合入口は`runtime/kuuos_current_check.py`です。

この入口は、closed repository mutation rootを実行した後、v0.36 lifecycle completionのfocused unit testを実行します。

## 固定境界

```text
candidate != authority
validation != truth
formal compilation != external theorem acceptance

observation != verification
verification != truth
learning != present-cycle mutation
memory != belief sovereignty
selection != execution
receipt != successor authority
receipt composition != receipt construction

local control != global constitution
local chart != global graph
curvature != veto
holonomy != sovereign memory

WORLD sidecar != exact WORLD
WORLD candidate != empirical fact
WORLD commit != truth
WORLD intake != WORLD update
analytic vacuum != exact WORLD
Kū != zero vector
modular time != physical time

connection candidate != production application
application authority != performed effect
rollback != time reversal
restored payload != restored authority

modeled repository transition != live Git mutation
object candidate != object materialization
reference authorization != reference update
checkpoint authorization != checkpoint creation
checkpoint creation != checkpoint overwrite
checkpoint reflog record != checkpoint reference update
dedicated index != canonical index
sandbox reflection != repository-root working-tree write
local checkpoint != push authority
roadmap completion != successor mutation authority

Apoptosis Lifecycle Governance != repository mutation roadmap v1.25
lifecycle observation != lifecycle authorization
lifecycle authorization != lifecycle execution
lifecycle execution != repository mutation
lifecycle archive != memory sovereignty
lifecycle completion != successor route
terminal completion != future authority inheritance
```

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

## 統合済みアーキテクチャ

### 局所文脈と有限サイクル

KuuOSは文脈を普遍的な固定グラフへ縮約しません。

文脈は、局所チャート、局所切断、遷移、曲率、cocycle residue、holonomyとして扱います。

有限サイクルは、mission binding、観測、複数信念、semantic planning、独立検証、bounded memory、effect reconciliation、checkpoint、restart recoveryを接続します。

局所サイクルの停止は、将来可能性全体の閉鎖を意味しません。

### Qi-WORLDとMemoryOS

Qi Process Tensorは、複数時点のprocess、複数仮説、反証、不確実性、回復可能性区間を候補として保持します。

Qi-WORLD v2.3は、process supportとboundary occupationを陰陽相補系として接続します。

この構造は、気を物理的ボース粒子へ、blockerを物理的フェルミ粒子へ同一視しません。

MemoryOSは、履歴をtruth、belief sovereignty、PlanOS activation、ActOS authorityへ自動昇格させません。

### WORLD数学サイドカー

統合済み数学系列はv0.27からv0.59です。

```text
real Hilbert ℓ²
→ dense and self-adjoint operator bridge
→ noncommutative operator algebra
→ C*-local net
→ von Neumann and modular theory
→ Araki relative entropy
→ Petz recovery and conditional expectation
→ Jones theory and categorical bridges
→ higher-gauge information geometry
→ quantum Bregman and variational geometry
→ log-Sobolev contraction certificates
→ OS reflection-positive completion interface
→ analytic vacuum sector
→ vacuum-expectation observation candidate
→ ObserveOS evidence intake
→ host-effect atomic commit intake
→ OS receipt composition
→ Kū vacuum central reference state
→ Kū vacuum information geometry
→ closed Tomita operator bridge
→ conjugate-adjoint intermediate layer
→ four-great phase dynamics
```

Leanは、宣言された仮定の下で型付き帰結を検証します。

CI成功だけでは、外部数学界での定理受理、物理実現、経験的妥当性は成立しません。

### Gauge、Module-Bundle、MemoryOS application

v0.60からv0.69は、有限候補、由来、rollback、外部reviewを持つ接続改善経路を構成します。

v0.70からv0.76は、文脈代数上の加群、意味部分加群、authority filtration、Leibniz接続、非マルコフ記憶核、有限評価、外部review、単回commit、monotonic rollbackを接続します。

v0.76の後に統合された正式系列はv0.78です。

v0.77提案の内容を、統合済み機能として推論してはなりません。

## Repository self-evolution chain

v0.78以降は、KuuOS自身のrepositoryを研究対象として扱います。

各段階は有限で、source-boundで、replay可能で、fail closedです。

### 構造整合からcheckpointモデルまで

| Version | 責務 |
|---|---|
| v0.78 | bounded self-organizing improvement loopとsupervisor |
| v0.79からv0.86 | repository alignment、normal form、preservation、revision、merge、frontier certificate |
| v0.87からv0.92 | portfolio、shadow、admission、external approval、application authorization、modeled application |
| v0.93からv0.98 | Git object candidate、object authorizationとreceipt、reference authorization、modeled CAS、execution receipt |
| v0.99からv1.02 | stability、local finality、checkpoint authorization、modeled checkpoint creation |
| v1.03からv1.18 | checkpoint receipt、workspace、stability、repair routing、namespace、CAS authorization、live checkpoint reference CAS |

### 完了した段階的repository mutation roadmap

| Version | 許可された限定効果 |
|---|---|
| v1.19 | 単一blobのobject database書込 |
| v1.20 | 限定tree objectとcommit objectの構築 |
| v1.21 | 構築済みcommitのcheckpoint refへのCAS公開 |
| v1.22 | checkpoint専用indexへの限定書込 |
| v1.23 | repository内sandbox working treeへの限定反映 |
| v1.24 | checkpoint専用reflogへの正確な一件記録 |

```text
bounded blob write
→ limited tree and commit construction
→ checkpoint-reference CAS publication
→ dedicated alternate index
→ repository-local sandbox reflection
→ exact checkpoint-dedicated reflog record
```

このroadmapはv1.24で完了し、閉じています。

v1.24の完了は、追加ref更新、追加reflog、push、signing、通常working treeへの無制限書込を許可しません。

Apoptosis Lifecycle Governanceは、このroadmapのv1.25以降ではありません。

## Apoptosis Lifecycle Governance

Apoptosis Lifecycle Governanceは、repository mutation roadmap v1.19からv1.24とは独立したread-only lifecycle-governance系列です。

この系列は、観測、候補化、依存review、authority review、quiescence、external review、独立承認、bounded execution preparation、review、request、decision、operation、result、closure、memory、archive、completionを段階的に分離します。

現在の`main`はv0.35までを統合しています。

PR #991のv0.36は、v0.35のready recordだけを受け取り、terminal lifecycle completion recordを発行するDraft frontierです。

v0.36のCOMPLETEはfollowing lifecycle routeを許可しません。

v0.36のALERTは有効なrecordを発行しますが、terminalにはなりません。

v0.36のREJECTEDは有効recordを発行しません。

v0.36はrepositoryを変更せず、外部操作を実行しません。

## Lean root

`formal/KuuOSFormal.lean`は、統合済みまたはこのPR枝で明示追加された形式層だけを参照するstrict aggregate rootです。

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

専用rootは各versionの局所surfaceを検証します。

aggregate rootはimport欠落、未統合moduleの混入、依存順の破綻、境界退行を検出します。

## Runtime roots

現在の作業枝におけるruntime rootは次です。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

この入口は、closed repository mutation rootとv0.36 lifecycle completion focused checkを束ねます。

closed repository mutation累積検証入口は次です。

```bash
PYTHONPATH=. python3 runtime/kuuos_v124_check.py
```

この入口はv1.24から先行runtimeへ依存順に遡り、focused tests、guards、effect accountingを検証します。

v0.36のfocused checkは次です。

```bash
python3 -m unittest tests.test_kuuos_lifecycle_completion_v0_36
```

既存workflow互換入口は次です。

```bash
PYTHONPATH=. python3 scripts/run_kuuos_runtime_full_check_v0_55.py
```

この互換入口はlegacy cumulative surfaceをv1.02まで検証します。

どの成功も、検査対象surfaceの再現可能な整合性receiptです。

真理、外部定理受理、臨床承認、組織承認、無制限実行許可ではありません。

## 次の研究前線

v0.36がterminal completionとしてmergeされる場合、同じlifecycle routeの次段階を自動開始しません。

completion後に必要な活動は、post-terminal observation、long-term preservation、external handover、retention、revocation、delete authority、または新しい独立系列として定義します。

新しいmutation機能を提案する場合は、v1.24の続番ではなく、新しい独立系列として次を定義します。

- authority owner。
- policy。
- request。
- result。
- effect accounting。
- Lean boundary。
- CI registry。
- abort preservationまたはcompensation contract。
- 既存権限から昇格しないことを示す非権限境界。

## 非主張

KuuOSは現時点で次を主張しません。

- 無制限の実行権限を持つproduction AGI。
- 任意のshell、network、repository、deploymentへの包括権限。
- 単一真理へ収束する普遍的global-context graph。
- 独立した医療診断、トリアージ、治療、医療行為承認システム。
- 気が物理的粒子であることの証明。
- LeanまたはCIの成功だけによる外部定理受理。
- 完全な物理的量子Markov semigroup、正確な物理真空、正確なWORLD simulator。
- rollbackによる承認権限または過去状態の復活。
- repository candidate、authorization、modeled transition、receiptの自動的なlive effect化。
- checkpoint権限からoverwrite、delete、push、signing権限への昇格。
- v1.24完了から後続mutation authorityへの自動昇格。
- Apoptosis Lifecycle Governanceをrepository mutation roadmap v1.25以降として扱うこと。
- terminal lifecycle completionからsuccessor lifecycle routeを推論すること。
- closed unmerged proposalを`main`の機能として扱うこと。

## 最初に読む文書

```text
README.md
ROADMAP.md
GOVERNANCE.md
CONTRIBUTING.md

formal/KUOS.lean
formal/KuuOSFormal.lean
runtime/kuuos_current_check.py
runtime/kuuos_v124_check.py
scripts/run_kuuos_runtime_full_check_v0_55.py

docs/lifecycle_completion_v0_36.md
runtime/kuuos_lifecycle_governance_completion_v0_36.py
formal/KUOS/WORLD/KuuOSLifecycleStageV0_36.lean
manifests/kuuos_lifecycle_completion_v0_36.json
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
modeled transition != live mutation
merged artifact != closed proposal
completed roadmap != inherited future authority
terminal lifecycle completion != successor route
```

新しい層は、入力、出力、所有者、必要権限、永続化、replay、stale-state処理、validatorの射程、外部仮定、非権限境界を明記します。

## Citation, governance and rights

引用、貢献、再利用条件は、[`CITATION.cff`](CITATION.cff)、[`GOVERNANCE.md`](GOVERNANCE.md)、[`CONTRIBUTING.md`](CONTRIBUTING.md)、repository license filesを参照してください。

**空OS、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属します。**

個別のrepository artifactの再利用は、各licenseと著作者表示に従います。

Repository artifactは、臨床権限、組織権限、数学的受理、実行権限を移転しません。
