# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS**は、観測、信念、記憶、計画、判断、実行、検証、学習、WORLD表現、repository evolutionを、由来、局所文脈、履歴、所有者、有限権限、明示的なreceipt chainへ束縛して接続する公開研究アーキテクチャです。

KuuOS is a public, governance-gated, proof-facing, non-Markovian, Qi-process-aware architecture for relational AI and bounded self-evolution research.

KuuOSは、候補、証拠、検証、承認、権限、実行効果、記憶、数学的表現、repository stateを同一視しません。

KuuOSはproduction AGI runtimeではありません。

## 現在地

**基準日：2026年7月2日**

**文書化対象の機能frontier：PR #948、KuuOS Repository Checkpoint Reflog v1.24**

**frontier merge commit：`1cb1b472527e70330f5387732d5d8f39fdbeffb5`**

現在の`main`は、MemoryOS applicationとrollbackのv0.76から、self-organizing improvement v0.78、repository self-evolution v0.79からv1.24へ進んでいます。

v0.77のauthority-role topologyとpost-transition verificationは提案枝として作成されましたが、`main`へは統合されていません。

したがって、正式なLean rootとruntime rootはv0.77を含めません。

| 系列 | `main`の統合済み到達点 |
|---|---|
| Core governance | v0.1 |
| Horizon Governance / Context Gauge Atlas | v0.12 / v0.13 |
| Modular Evolution Mesh | v0.1 |
| PlanOS control | v0.17 |
| Finite-cycle agent | v0.20からv0.27 |
| Qi diagnostic candidate / lineage | v0.28 / v0.29 |
| Open Horizon | v0.30からv0.34 |
| MemoryOS foundational line | v0.35、v0.37、v0.38、v0.39 |
| Qi-WORLD | v2.3 |
| WORLD mathematical sidecar | v0.27からv0.59 |
| Gauge-field self-organization | v0.60からv0.69 |
| Module-Bundle and MemoryOS application | v0.70からv0.76 |
| v0.77 proposals | 未統合 |
| Self-organizing improvement loop | v0.78 |
| Repository self-evolution chain | v0.79からv1.24 |
| Lean aggregate root | `formal/KuuOSFormal.lean` / target `KuuOSFormal` |
| Current repository runtime root | `runtime/kuuos_v124_check.py` |
| Legacy compatibility runtime root | `scripts/run_kuuos_runtime_full_check_v0_55.py` |
| Lean / mathlib | Lean 4、mathlib `v4.30.0-rc2` |

`run_kuuos_runtime_full_check_v0_55.py`という名称は既存workflowとの互換性のため保持しています。

このlegacy compatibility rootはv1.02までの従来系列を検証します。

v1.03からv1.24までを含む現在のrepository mutation累積検証入口は`runtime/kuuos_v124_check.py`です。

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

### Checkpoint receiptとCAS準備

| Version | 責務 |
|---|---|
| v1.03 | checkpoint creation receipt |
| v1.04 | checkpoint evolution workspace |
| v1.05 | checkpoint stability |
| v1.06 | checkpoint discrepancy review |
| v1.07 | checkpoint repair routing |
| v1.08 | checkpoint namespace gate |
| v1.09 | checkpoint candidate |
| v1.10 | checkpoint CAS contract |
| v1.11 | checkpoint candidate validation |
| v1.12 | validated CAS intake |
| v1.13 | CAS coherence |
| v1.14 | CAS authorization request |
| v1.15 | CAS authorization decision |
| v1.16 | atomic modeled CAS transition |
| v1.17 | live Git preflight |
| v1.18 | bounded live checkpoint ref CAS |

### 段階的repository mutation roadmap

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

## v1.24の正確な意味

v1.24は、v1.21で受理されたcheckpoint ref遷移を、v1.23 sandbox reflectionの完了後にcheckpoint専用reflogへ一件だけ記録します。

対象namespaceは`refs/kuuos/checkpoints/`に限定されます。

現在のcheckpoint refは変更しません。

完全一致する既存一件はGit書込を行わず再利用します。

一文字でも異なる既存reflogは拒否し、上書きも追記も行いません。

成功時に変更を許す面は、対象checkpoint reflogの専用経路だけです。

```text
checkpoint reflog write
!= reference update
!= object write
!= index write
!= working-tree write
!= push
!= signing
```

詳細は[`docs/KUUOS_REPOSITORY_CHECKPOINT_REFLOG_v1_24.md`](docs/KUUOS_REPOSITORY_CHECKPOINT_REFLOG_v1_24.md)を参照してください。

## Lean root

`formal/KuuOSFormal.lean`は、`main`へ統合済みの形式層だけを参照するstrict aggregate rootです。

MemoryOS系列はv0.76までをimportし、その後はv0.78からv1.24のrepository self-evolution系列をimportします。

未統合のv0.77 modulesはimportしません。

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

専用rootは各versionの局所surfaceを検証します。

aggregate rootはimport欠落、未統合moduleの混入、依存順の破綻、境界退行を検出します。

## Runtime roots

現在のrepository mutation累積検証入口は次です。

```bash
PYTHONPATH=. python3 runtime/kuuos_v124_check.py
```

この入口はv1.24から先行runtimeへ依存順に遡り、focused tests、guards、effect accountingを検証します。

既存workflow互換入口は次です。

```bash
PYTHONPATH=. python3 scripts/run_kuuos_runtime_full_check_v0_55.py
```

この互換入口はlegacy cumulative surfaceをv1.02まで検証します。

どちらの成功も、検査対象surfaceの再現可能な整合性receiptです。

真理、外部定理受理、臨床承認、組織承認、無制限実行許可ではありません。

## v1.24受入記録

PR #948の固定headは`f99a4abd259b3b310cb96c77dbfccb742657d2f1`です。

KuuOS PR Governance Gate Run #370は成功しました。

最終auditはexpected checks 108件、収集結果108件、failed checks 0件、missing receipts 0件でした。

PR #948はmerge commit `1cb1b472527e70330f5387732d5d8f39fdbeffb5`として`main`へ統合されました。

## 次の研究前線

v1.24の次にv1.25 mutationを自動開始しません。

新しいmutation機能を提案する場合は、既存roadmapの継続ではなく、新しい独立系列として次を定義します。

- authority owner。
- policy。
- request。
- result。
- effect accounting。
- Lean boundary。
- CI registry。
- abort preservationまたはcompensation contract。
- 既存権限から昇格しないことを示す非権限境界。

非mutationの次期研究候補には、checkpoint recovery proposal、retentionとrevocation、delete authorityの分離、ActOS一般の実行後観測検証、MemoryOS、WORLD数学frontierがあります。

詳細は[`ROADMAP.md`](ROADMAP.md)に記載します。

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
- closed unmerged proposalを`main`の機能として扱うこと。

## 最初に読む文書

```text
README.md
ROADMAP.md
GOVERNANCE.md
CONTRIBUTING.md

formal/KUOS.lean
formal/KuuOSFormal.lean
runtime/kuuos_v124_check.py
scripts/run_kuuos_runtime_full_check_v0_55.py

docs/KUUOS_REPOSITORY_CHECKPOINT_REFLOG_v1_24.md
formal/KuuOSRepositoryV1_24.lean
manifests/kuuos_repository_checkpoint_reflog_v124.json
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
```

新しい層は、入力、出力、所有者、必要権限、永続化、replay、stale-state処理、validatorの射程、外部仮定、非権限境界を明記します。

## Citation, governance and rights

引用、貢献、再利用条件は、[`CITATION.cff`](CITATION.cff)、[`GOVERNANCE.md`](GOVERNANCE.md)、[`CONTRIBUTING.md`](CONTRIBUTING.md)、repository license filesを参照してください。

**空OS、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属します。**

個別のrepository artifactの再利用は、各licenseと著作者表示に従います。

Repository artifactは、臨床権限、組織権限、数学的受理、実行権限を移転しません。
