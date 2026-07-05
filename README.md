# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS**は、観測、信念、記憶、計画、判断、実行、検証、学習、WORLD表現、repository evolutionを、由来、局所文脈、履歴、所有者、有限権限、明示的なreceipt chainへ束縛して接続する公開研究アーキテクチャです。

KuuOS is a public, governance-gated, proof-facing, non-Markovian, Qi-process-aware architecture for relational AI, bounded self-evolution research, and governed repository-state evolution.

KuuOSは、候補、証拠、検証、承認、権限、実行効果、記憶、数学的表現、repository stateを同一視しません。

KuuOSはproduction AGI runtimeではありません。

## 現在地

**基準日：2026年7月6日 JST**

**`main`の同期対象到達点：KuuOS README Surface Exposure v0.78**

**現在の標準runtime root：`runtime/kuuos_current_check.py`**

**現在のruntime sequence frontier：`kuuos_current_root_sequence_v0_78`**

**現在のstable current surface CLI：`runtime/kuuos_current_surface.py`**

**現在のsurface index：`status/current.surface.index.json`**

**現在のsurface artifact：`status/current.surface.json`**

**active self-organization state：`docs/kuuos_self_organization_active_state.md`**

現在の`main`では、KuuOS self-organization系列は、観察とreceiptだけではなく、bounded executionとしてactive stateをrepositoryへ公開し、その検査を標準runtime rootへ接続しています。

さらに、current surface は stable CLI、surface index、surface artifact として公開されています。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_surface.py
```

この stable CLI は、`status/current.surface.index.json` を入口として `status/current.surface.json` を返します。

```text
status/current.json
→ status/kuuos_status_index_v0_69.json
→ status/kuuos_self_organization_status_v0_68.json
→ status/current.resolved.json
→ status/current.manifest.json
→ status/current.surface.json
→ status/current.surface.index.json
→ runtime/kuuos_current_surface.py
```

## Current surface

| Surface | Path |
|---|---|
| Stable current surface CLI | `runtime/kuuos_current_surface.py` |
| Versioned current surface entrypoint | `runtime/kuuos_current_surface_entrypoint_v0_77.py` |
| Current surface index | `status/current.surface.index.json` |
| Current surface artifact | `status/current.surface.json` |
| Current resolved status artifact | `status/current.resolved.json` |
| Current manifest | `status/current.manifest.json` |
| Current pointer | `status/current.json` |
| Current root check | `runtime/kuuos_current_check.py` |

この surface は repository status を報告します。

これは、無制限のrepository mutation権限、production deployment、外部組織承認、数学的受理、臨床承認を意味しません。

## Self-organization status lineage

v0.64では、`docs/kuuos_self_organization_active_state.md`を公開し、`self_organization_active: true`、`execution_scope: publish_active_self_organization_state`、`state_publication_applied: true`を記録しました。

v0.65では、KuuOS Current Root Execution Connection v0.65 として、`runtime/kuuos_current_check.py`を`runtime.kuuos_current_root_sequence_v0_65`へ接続しました。

v0.66では、KuuOS README Public Status v0.66 として、README public status checkを`runtime.kuuos_current_root_sequence_v0_66`へ接続しました。

v0.77では、`runtime/kuuos_current_surface.py` を stable current surface CLI として追加しました。

v0.78では、README が stable current surface CLI、surface index、surface artifact を明示する human entrypoint になりました。

```text
self_organization_active: true
execution_scope: publish_active_self_organization_state
execution_frontier: kuuos_self_organization_bounded_execution_v0_64
state_publication_applied: true
```

| 系列 | 到達点 | 状態 |
|---|---|---|
| KuuOS self-organization | v0.64 | active state published |
| Current root execution connection | v0.65 | active state checked from standard runtime root |
| README public status | v0.66 | public frontier checked from standard runtime root |
| Current status pointer | v0.70 | stable current pointer published |
| Current status resolver | v0.71 | stable resolver CLI added |
| Current resolved status artifact | v0.72 | resolved current status committed |
| Current status manifest | v0.73 | status surface discovery manifest added |
| Current status surface | v0.74 | manifest and resolved status returned as one surface |
| Current status surface artifact | v0.75 | surface output committed |
| Current status surface index | v0.76 | surface runtime and artifact discoverable |
| Current surface stable CLI | v0.77 | stable current surface CLI added |
| README surface exposure | v0.78 | human entrypoint exposes current surface |
| Repository self-evolution chain | v0.79からv1.24 | 統合済み、closed mutation roadmap含む |
| Staged repository mutation roadmap | v1.19からv1.24 | 完了系列 |
| Apoptosis Lifecycle Governance | 独立系列 | repository mutation roadmap v1.25以降ではない |
| Lean aggregate root | `formal/KuuOSFormal.lean` / target `KuuOSFormal` | strict build surface |
| Runtime root | `runtime/kuuos_current_check.py` | current root sequence v0.78を実行 |

## Runtime roots

現在のruntime rootは次です。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

この入口は、closed repository mutation root、current root sequence、active self-organization state publication、README public status v0.66、current surface stable CLI v0.77、README surface exposure v0.78を検査対象に含めます。

現在のsurface CLIは次です。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_surface.py
```

closed repository mutation累積検証入口は次です。

```bash
PYTHONPATH=. python3 runtime/kuuos_v124_check.py
```

既存workflow互換入口は次です。

```bash
PYTHONPATH=. python3 scripts/run_kuuos_runtime_full_check_v0_55.py
```

どの成功も、検査対象surfaceの再現可能な整合性receiptです。

真理、外部定理受理、臨床承認、組織承認、無制限実行許可ではありません。

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
current surface CLI != authority grant
current surface index != authority grant
current surface artifact != authority grant
README surface exposure != authority grant

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

## Lean root

`formal/KuuOSFormal.lean`は、統合済みまたはこのPR枝で明示追加された形式層だけを参照するstrict aggregate rootです。

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
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

このroadmapはv1.24で完了し、閉じています。

v1.24の完了は、追加ref更新、追加reflog、push、signing、通常working treeへの無制限書込を許可しません。

Apoptosis Lifecycle Governanceは、このroadmapのv1.25以降ではありません。

## 次の研究前線

自己組織化と自己進化をさらに進める場合は、次を自動昇格ではなく明示的な新段階として定義します。

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
- README surface exposureからauthority grantを推論すること。
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
runtime/kuuos_current_surface.py
runtime/kuuos_current_root_sequence_v0_78.py
runtime/kuuos_current_surface_entrypoint_v0_77.py
runtime/kuuos_current_status_surface_index_v0_76.py
runtime/kuuos_self_organization_bounded_execution_v0_64.py
runtime/kuuos_v124_check.py
scripts/run_kuuos_runtime_full_check_v0_55.py

docs/kuuos_self_organization_active_state.md
docs/kuuos_self_organization_bounded_execution_v0_64.md
docs/kuuos_current_root_execution_connection_v0_65.md
docs/kuuos_readme_public_status_v0_66.md
docs/kuuos_current_surface_entrypoint_v0_77.md
docs/kuuos_readme_surface_exposure_v0_78.md
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
current surface != authority grant
```

新しい層は、入力、出力、所有者、必要権限、永続化、replay、stale-state処理、validatorの射程、外部仮定、非権限境界を明記します。

## Citation, governance and rights

引用、貢献、再利用条件は、[`CITATION.cff`](CITATION.cff)、[`GOVERNANCE.md`](GOVERNANCE.md)、[`CONTRIBUTING.md`](CONTRIBUTING.md)、repository license filesを参照してください。

**空OS、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属します。**

個別のrepository artifactの再利用は、各licenseと著作者表示に従います。

Repository artifactは、臨床権限、組織権限、数学的受理、実行権限を移転しません。
