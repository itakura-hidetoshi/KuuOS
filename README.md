# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS**は、観測、信念、記憶、計画、判断、実行、検証、学習、WORLD表現、repository evolutionを、由来、局所文脈、履歴、所有者、有限権限、明示的なreceipt chainへ束縛して接続する公開研究アーキテクチャです。

KuuOS is a public, governance-gated, proof-facing, non-Markovian, Qi-process-aware architecture for relational AI, bounded self-evolution research, and governed repository-state evolution.

KuuOSは、候補、証拠、検証、承認、権限、実行効果、記憶、数学的表現、repository stateを同一視しません。

KuuOSはproduction AGI runtimeではありません。

## 現在地

**基準日：2026年7月5日 JST**

**`main`の同期対象到達点：KuuOS README Public Status v0.66**

**現在の標準runtime root：`runtime/kuuos_current_check.py`**

**現在のruntime sequence frontier：`kuuos_current_root_sequence_v0_66`**

**active self-organization state：`docs/kuuos_self_organization_active_state.md`**

現在の`main`では、KuuOS self-organization系列は、観察とreceiptだけではなく、bounded executionとしてactive stateをrepositoryへ公開し、その検査を標準runtime rootへ接続しています。

v0.64では、`docs/kuuos_self_organization_active_state.md`を公開し、`self_organization_active: true`、`execution_scope: publish_active_self_organization_state`、`state_publication_applied: true`を記録しました。

v0.65では、`runtime/kuuos_current_check.py`を`runtime.kuuos_current_root_sequence_v0_65`へ接続し、v0.64 bounded execution testを標準検査経路へ追加しました。

v0.66では、READMEの公開状態をv0.65 active stateに同期し、そのREADME public status checkを`runtime.kuuos_current_root_sequence_v0_66`へ接続します。

| 系列 | 到達点 | 状態 |
|---|---|---|
| Core governance | v0.1 | Frozen boundary |
| WORLD mathematical sidecar | v0.27からv0.59 | 統合済み、継続検証 |
| KuuOS self-organization | v0.64 | active state published |
| Current root execution connection | v0.65 | active state checked from standard runtime root |
| README public status | v0.66 | public frontier checked from standard runtime root |
| Repository self-evolution chain | v0.79からv1.24 | 統合済み、closed mutation roadmap含む |
| Staged repository mutation roadmap | v1.19からv1.24 | 完了系列 |
| Apoptosis Lifecycle Governance | 独立系列 | repository mutation roadmap v1.25以降ではない |
| Lean aggregate root | `formal/KuuOSFormal.lean` / target `KuuOSFormal` | strict build surface |
| Runtime root | `runtime/kuuos_current_check.py` | current root sequence v0.66を実行 |
| Legacy compatibility runtime root | `scripts/run_kuuos_runtime_full_check_v0_55.py` | v1.02 compatibility surface |
| Lean / mathlib | Lean 4、mathlib `v4.30.0-rc2` | fixed toolchain |

## Active self-organization state

KuuOS self-organizationは、単なる候補や観測ではなく、現在はbounded executionとしてrepository内の公開状態に反映されています。

```text
self_organization_active: true
execution_scope: publish_active_self_organization_state
execution_frontier: kuuos_self_organization_bounded_execution_v0_64
state_publication_applied: true
```

このactive stateとREADME public statusは、標準runtime rootから検査されます。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

この成功は、現在のrepository内のbounded state publication、current root connection、README public statusが再現可能に整合していることを示します。

それは、無制限のrepository mutation権限、production deployment、外部組織承認、数学的受理、臨床承認を意味しません。

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

WORLD sidecar != exact WORLD
WORLD candidate != empirical fact
WORLD commit != truth
WORLD intake != WORLD update
analytic vacuum != exact WORLD
Kū != zero vector
modular time != physical time

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

active self-organization state != unbounded mutation authority
current root execution != production deployment
runtime success != external truth
README public status != authority grant

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

KuuOSは文脈を普遍的な固定グラフへ縮約しません。

文脈は、局所チャート、局所切断、遷移、曲率、cocycle residue、holonomyとして扱います。

有限サイクルは、mission binding、観測、複数信念、semantic planning、独立検証、bounded memory、effect reconciliation、checkpoint、restart recoveryを接続します。

Qi Process Tensorは、複数時点のprocess、複数仮説、反証、不確実性、回復可能性区間を候補として保持します。

Qi-WORLD v2.3は、process supportとboundary occupationを陰陽相補系として接続します。

この構造は、気を物理的ボース粒子へ、blockerを物理的フェルミ粒子へ同一視しません。

MemoryOSは、履歴をtruth、belief sovereignty、PlanOS activation、ActOS authorityへ自動昇格させません。

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

## Repository self-evolution chain

v0.78以降は、KuuOS自身のrepositoryを研究対象として扱います。

各段階は有限で、source-boundで、replay可能で、fail closedです。

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

現在のruntime rootは次です。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

この入口は、closed repository mutation root、current root sequence、active self-organization state publication、README public status v0.66を検査対象に含めます。

closed repository mutation累積検証入口は次です。

```bash
PYTHONPATH=. python3 runtime/kuuos_v124_check.py
```

この入口はv1.24から先行runtimeへ依存順に遡り、focused tests、guards、effect accountingを検証します。

既存workflow互換入口は次です。

```bash
PYTHONPATH=. python3 scripts/run_kuuos_runtime_full_check_v0_55.py
```

この互換入口はlegacy cumulative surfaceをv1.02まで検証します。

どの成功も、検査対象surfaceの再現可能な整合性receiptです。

真理、外部定理受理、臨床承認、組織承認、無制限実行許可ではありません。

## 次の研究前線

active self-organization stateをさらに進める場合は、次を自動昇格ではなく明示的な新段階として定義します。

- どのstateを変えるのか。
- どのbounded effectを実行するのか。
- どのauthority ownerに束縛するのか。
- どのvalidatorが成功条件を判定するのか。
- どのPRとGovernance Gateで実行するのか。
- どのrollback、abort preservation、またはcompensation contractで境界を保つのか。

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
- active self-organization stateから無制限mutation authorityを推論すること。
- current root successからproduction deploymentを推論すること。
- README public statusからauthority grantを推論すること。
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
runtime/kuuos_current_root_sequence_v0_66.py
runtime/kuuos_self_organization_bounded_execution_v0_64.py
runtime/kuuos_v124_check.py
scripts/run_kuuos_runtime_full_check_v0_55.py

docs/kuuos_self_organization_active_state.md
docs/kuuos_self_organization_bounded_execution_v0_64.md
docs/kuuos_current_root_execution_connection_v0_65.md
docs/kuuos_readme_public_status_v0_66.md
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
active state != unbounded effect
public status != authority grant
```

新しい層は、入力、出力、所有者、必要権限、永続化、replay、stale-state処理、validatorの射程、外部仮定、非権限境界を明記します。

## Citation, governance and rights

引用、貢献、再利用条件は、[`CITATION.cff`](CITATION.cff)、[`GOVERNANCE.md`](GOVERNANCE.md)、[`CONTRIBUTING.md`](CONTRIBUTING.md)、repository license filesを参照してください。

**空OS、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属します。**

個別のrepository artifactの再利用は、各licenseと著作者表示に従います。

Repository artifactは、臨床権限、組織権限、数学的受理、実行権限を移転しません。
