# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS**は、観測、信念、記憶、WORLD表現、計画、判断、実行、検証、学習を、由来、局所文脈、履歴、責任主体、有限権限、検証可能なreceiptへ結び付ける公開研究アーキテクチャです。

KuuOS is a public, governance-gated, proof-facing, non-Markovian, Qi-process-aware architecture for relational AI and bounded self-evolution research.

KuuOSは、候補と権限、予測と事実、検証と真理、選択と実行、記憶と主権を同一視しません。

KuuOSはproduction AGI runtimeではありません。

## 現在地

**基準日：2026年7月11日 JST**

`main`で確認した現在の統合済み研究前線は次です。

| 面 | 統合済み到達点 | 主な入口 |
|---|---|---|
| Repository lineage | self-organization v0.113 | `runtime/kuuos_current_root_sequence_v0_113.py` |
| PlanOS | v1.02 WORLD-conditioned distribution decision handoff | `scripts/check_planos_world_conditioned_distribution_decision_handoff_certificate_kernel_v0_1.py` |
| DecisionOS | v0.6 WORLD-conditioned relational deliberation | `scripts/run_decision_os_full_checks.py` |
| WORLD dependency | KuuOS v14.0 causal WORLD state | PlanOS v1.00 WORLD binding |
| Stable integrated runtime root | repository、PlanOS、DecisionOSの三面 | `runtime/kuuos_current_check.py` |

直近の機能統合はPR #1160です。

PR #1160は、DecisionOS v0.6として、候補を単一効用へ潰さず、和、stakeholder support、relational support、dissent pressure、minority-impact risk、uncertainty burdenから関係的部分順序を構成します。

公開状態は`main`を基準とします。

未mergeの旧Draftや分岐は、rebaseと再検証を経ない限り現在のfrontierとはみなしません。

## 標準runtime root

標準入口は次です。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

このrootは次を順に実行します。

```text
repository mutationとself-organizationの累積lineage through v0.113
→ PlanOS information-geometric Qi objective line v0.91-v1.02
→ DecisionOS cumulative validation v0.1-v0.6
```

一つの検査が失敗しても残りの検査を継続し、最後に必要stepの失敗をまとめて返します。

検査面を限定する場合はprofileを指定します。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile repository
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile decisionos
```

現在のroot構成はJSONで確認できます。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py --summary
PYTHONPATH=. python3 runtime/kuuos_current_check.py --list
```

root成功は、登録されたruntime surfaceが現在のrepository内で再現可能に整合したことを示します。

root成功は、外部定理受理、経験的真理、臨床承認、組織承認、production deployment、無制限実行権限を意味しません。

## PlanOSの現在の数理線

PlanOS v0.91以降は、目標を単一の固定点ではなく、有限な将来経路上の分布として扱います。

### 情報幾何と変分更新

| Version | 内容 |
|---|---|
| v0.91 | Information-Geometric Qi Objective Kernel |
| v0.92 | KL-regularized objective distribution update |
| v0.93 | zero-temperature minimal-action support |
| v0.94 | finite-temperature concentration certificate |

権限を持たない経路には確率質量を付与しません。

同じ最小作用を持つ候補は、恣意的に一つへ縮約せず、完全な最小化supportとして保持します。

### 非マルコフ温度制御

| Version | 内容 |
|---|---|
| v0.95 | adaptive Qi temperature calibration |
| v0.96 | hysteresis and asymmetric rate limit |
| v0.97 | temperature trajectory receipt |
| v0.98 | finite-window trajectory stability certificate |

Qiは探索圧と安定化圧を条件付けますが、権限を生成しません。

履歴は非マルコフな条件として参照されますが、現在cycleの主権にはなりません。

### WORLD条件付き経路幾何

| Version | 内容 |
|---|---|
| v0.99 | Qi- and history-conditioned information metric |
| v1.00 | WORLD-conditioned projection and pullback metric |
| v1.01 | WORLD-conditioned candidate distribution update |
| v1.02 | advisory distribution decision handoff certificate |

v1.00は、各候補のPlan parameter deltaを局所WORLD Jacobianで射影し、`JᵀG_WJ`をPlan metricへ引き戻します。

persistent WORLD stateは変更せず、候補ごとのcounterfactual projectionだけを生成します。

v1.01は、Plan、Qi、history、WORLDを合わせた作用から、future-onlyな候補分布を更新します。

v1.02は、その分布、順位、lead margin、entropy、effective support、hold guardをDecisionOSへ渡します。

順位はadvisoryであり、選択権限ではありません。

## DecisionOSの現在地

DecisionOS v0.5は、PlanOS v1.02のhandoff certificateを再計算し、候補ごとのevidence intakeを検証します。

DecisionOS v0.6は、候補ごとの関係的deliberation profileを構成し、Pareto型のnon-dominated relational frontierを返します。

```text
PlanOS probability and action ranking
→ DecisionOS evidence intake
→ relational partial-order deliberation
→ relational frontier
```

この段階では候補を選択しません。

decision receipt、plan synthesis、WORLD mutation、ActOS execution permissionも生成しません。

## OSの責務

| OS | 主な責務 |
|---|---|
| ObserveOS | source-bound observation ownership |
| BeliefOS | local and plural belief-state ownership |
| DecisionOS | admissibility、evidence intake、relational deliberation、bounded selection |
| PlanOS | candidate generation、path distribution、plan and replan synthesis |
| ActOS | exactly licensed bounded effect |
| VerifyOS | evidence-bound independent verification |
| LearnOS | future-only learning delta |
| MemoryOS | lineage、reconstruction、conditioned retrieval、read-only history source |
| WORLD | sourced representation、causal state、governed fragment storage |

```text
ObserveOS evidence != VerifyOS verdict
VerifyOS verdict != truth authority
LearnOS delta != immediate activation
DecisionOS deliberation != DecisionOS selection
DecisionOS selection != ActOS invocation
PlanOS distribution != selected action
MemoryOS retrieval != PlanOS activation
WORLD projection != WORLD mutation
```

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
relational frontier != selected candidate
receipt != successor authority
receipt composition != receipt construction

WORLD candidate != empirical fact
WORLD projection != persistent WORLD update
WORLD commit != truth
Qi conditioning != authority grant
modular time != physical time

modeled repository transition != live Git mutation
local checkpoint != remote push authority
roadmap completion != successor mutation authority
active self-organization state != unbounded mutation authority
current root execution != production deployment
runtime success != external truth
README public status != authority grant
current surface CLI != authority grant
current surface index != authority grant
current surface artifact != authority grant
README surface exposure != authority grant
```

## Compatibility surface

現在の統合rootは過去の公開surfaceを置換しません。

既存のmachine-readable status lineageが参照する固定点を、互換性markerとして保持します。

| 固定点 | Versioned surface |
|---|---|
| KuuOS Current Root Execution Connection v0.65 | `kuuos_current_root_sequence_v0_65` |
| KuuOS README Public Status v0.66 | `kuuos_current_root_sequence_v0_66` |
| KuuOS README Surface Exposure v0.78 | `kuuos_current_root_sequence_v0_78` |

関連文書は次です。

```text
docs/kuuos_self_organization_active_state.md
docs/kuuos_readme_public_status_v0_66.md
docs/kuuos_readme_surface_exposure_v0_78.md
```

active-state compatibility receiptは次の境界を保持します。

```text
self_organization_active: true
execution_scope: publish_active_self_organization_state
state_publication_applied: true
```

既存のcurrent status surfaceは次です。

| Surface | Path |
|---|---|
| Stable current surface CLI | `runtime/kuuos_current_surface.py` |
| Versioned current surface entrypoint | `runtime/kuuos_current_surface_entrypoint_v0_77.py` |
| Current surface index | `status/current.surface.index.json` |
| Current surface artifact | `status/current.surface.json` |
| Current resolved status artifact | `status/current.resolved.json` |
| Current manifest | `status/current.manifest.json` |

```bash
PYTHONPATH=. python3 runtime/kuuos_current_surface.py
```

この互換surfaceはstatus reportであり、現在の研究前線を検査するcanonical rootは`runtime/kuuos_current_check.py`です。

## Repository map

| Path | 役割 |
|---|---|
| `runtime/` | executable kernels、receipts、validators、current root |
| `scripts/` | fail-closed checkersとcumulative runners |
| `formal/` | Lean theorem packagesとaggregate imports |
| `manifests/` | machine-readable package bindings |
| `status/` | historical and current-surface artifacts |
| `docs/` | versioned specifications and research notes |
| `tests/` | repository lineage and runtime unit tests |
| `.github/workflows/` | governance and subsystem validation gates |

`runtime/kuuos_current_surface.py`と`status/current.*`は、既存のstatus compatibility surfaceとして保持されています。

現在の研究前線を検査するcanonical execution surfaceは`runtime/kuuos_current_check.py`です。

## Formal surfaces

Repository-wide strict baselineは`formal/KuuOSFormal.lean`です。

最新のPlanOSとDecisionOSは、versioned aggregate moduleとして別に保持されています。

| Surface | Path |
|---|---|
| Repository strict baseline | `formal/KuuOSFormal.lean` |
| PlanOS v1.02 aggregate | `formal/KuuOS/PlanOSV102.lean` |
| DecisionOS v0.6 aggregate | `formal/KuuOSDecisionOSV0_6.lean` |

versioned aggregateが存在することと、repository-wide aggregateへ統合済みであることは区別します。

## 開発原則

変更はdedicated branchで行います。

runtime、checker、manifest、documentation、formal packageを同じ責任境界へ揃えます。

候補、証拠、検証、承認、権限、実行効果を別のartifactとして保持します。

新しいfrontierは、旧frontierを偽装して置換せず、依存関係と非同一性を明示します。

詳細な次段階は[ROADMAP.md](ROADMAP.md)に記載します。
