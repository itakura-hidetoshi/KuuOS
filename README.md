# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS**は、観測、信念、記憶、計画、判断、実行、検証、学習、WORLD表現、repository evolutionを、由来、局所文脈、履歴、所有者、有限権限、明示的なreceipt chainへ束縛して接続する公開研究アーキテクチャです。

KuuOS is a public, governance-gated, proof-facing, non-Markovian, Qi-process-aware architecture for relational AI, bounded self-evolution research, and governed repository-state evolution.

KuuOSは、候補、証拠、検証、承認、権限、実行効果、記憶、数学的表現、repository stateを同一視しません。

KuuOSはproduction AGI runtimeではありません。

## 現在地

**基準日：2026年7月7日 JST**

**`main`の統合済み到達点：self-organization candidate receipt v0.91**

**現在のDraft frontier：PR #1052、self-organization selection policy v0.92**

**Draft branch：`feature-selection-policy-v0-92`**

**現在の標準runtime root：`runtime/kuuos_current_check.py`**

**現在のruntime sequence frontier：`kuuos_current_root_sequence_v0_92`**

v0.91では、v0.90 candidate queueの4候補をreceiptとして固定し、v0.92をselection policy stageとして指名しました。

v0.92では、`status/self_organization_selection_policy_v0_92.json`をpolicy-only artifactとして追加し、候補選択の規則だけを記録します。

v0.92は、selection execution、repository mutation、runtime effectを許可しません。

この枝では、標準runtime rootが`runtime.kuuos_current_root_sequence_v0_92`を読み、v0.92 validatorとcurrent-root sequence testまでを実行します。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
PYTHONPATH=. python3 runtime/kuuos_self_organization_selection_policy_v0_92.py
PYTHONPATH=. python3 -m unittest tests.test_kuuos_self_organization_selection_policy_v0_92
PYTHONPATH=. python3 -m unittest tests.test_kuuos_current_root_sequence_v0_92
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
| Current root sequence | `runtime/kuuos_current_root_sequence_v0_92.py` |
| Current Draft artifact | `status/self_organization_selection_policy_v0_92.json` |

この surface はrepository statusを報告します。

これは、無制限のrepository mutation権限、production deployment、外部組織承認、数学的受理、臨床承認を意味しません。

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

## Self-organization lineage

| Version | 状態 | 境界 |
|---|---|---|
| v0.64 | active state published | `docs/kuuos_self_organization_active_state.md` |
| v0.65 | KuuOS Current Root Execution Connection v0.65 | `kuuos_current_root_sequence_v0_65` |
| v0.66 | KuuOS README Public Status v0.66 | `kuuos_current_root_sequence_v0_66` / `docs/kuuos_readme_public_status_v0_66.md` |
| v0.67 | self-organization status CLI | status reporting only |
| v0.68 | committed status snapshot | snapshot is not authority |
| v0.69 | status index | index is not canonical sovereignty |
| v0.70 | stable current pointer | pointer is not truth |
| v0.71 | stable current resolver | resolution is not authority grant |
| v0.72 | resolved status artifact | artifact is not external validation |
| v0.73 | current status manifest | manifest is not authority grant |
| v0.74 | current status surface runtime | surface is status report |
| v0.75 | committed current surface artifact | committed surface is not execution license |
| v0.76 | current surface index | index is not authority grant |
| v0.77 | stable current surface CLI | CLI is not authority grant |
| v0.78 | KuuOS README Surface Exposure v0.78 | `kuuos_current_root_sequence_v0_78` / `docs/kuuos_readme_surface_exposure_v0_78.md` |
| v0.79 | candidate queue | proposal-only |
| v0.80 | candidate receipt | receipt-only |
| v0.81 | selection policy | policy-only |
| v0.82 | selected next action | recorded selection only |
| v0.83 | execution plan | plan-only |
| v0.84 | next request | request-only |
| v0.85 | review packet | review-only |
| v0.86 | bounded-action transition | review loop closed |
| v0.87 | bounded repository change | bounded change artifact |
| v0.88 | completion receipt | receipt-only |
| v0.89 | next cycle seed | seed-only |
| v0.90 | candidate queue | proposal-only |
| v0.91 | candidate receipt | receipt-only |
| v0.92 | selection policy | Draft PR #1052、policy-only |

```text
self_organization_active: true
execution_scope: publish_active_self_organization_state
execution_frontier: kuuos_self_organization_bounded_execution_v0_64
state_publication_applied: true
```

## Runtime roots

現在のruntime rootは次です。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

この入口は、closed repository mutation root、current root sequence、active self-organization state publication、README public status v0.66、current surface stable CLI v0.77、README surface exposure v0.78、self-organization v0.79-v0.92系列を検査対象に含めます。

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
selection policy != selection execution
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
current surface CLI != authority grant
current surface index != authority grant
current surface artifact != authority grant
README surface exposure != authority grant
selection policy artifact != authority grant

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
