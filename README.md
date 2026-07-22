# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS**は、観測、信念、記憶、WORLD表現、計画、判断、実行、検証、学習を、由来、局所文脈、履歴、責任主体、有限権限、検証可能なreceiptへ結び付ける公開研究アーキテクチャです。

KuuOS is a public, governance-gated, proof-facing, non-Markovian and relational AI research architecture. It separates candidates from authority, evidence from truth, validation from acceptance, and selection from execution.

## 現在地

**基準日：2026年7月23日 JST**

authoritative branchは`main`です。現在の統合済みHEADは`083ee7ef65d53bd1a8e231c73b82e4946dd1eaf7`、最新の機能統合はPR #1341 **Baseline-versus-CodeAI and Ablation Comparison v0.1**です。

PR #1342 **CodeAI Frozen Cohort Prediction-Pack and Execution-Shard Contract v0.1**はDraftです。`main`へ未統合であり、current rootの統合済みfrontierとは区別します。

| 面 | 統合済み到達点 | 主な入口 |
|---|---|---|
| Repository lineage | self-organization v0.113 | `runtime/kuuos_current_root_sequence_v0_113.py` |
| ObserveOS | v0.7 sequential epistemic observability envelope | `docs/ObserveOS/README.md` |
| VerifyOS | v0.15 read-only outcome disposition handoff | `docs/VerifyOS/README.md` |
| PlanOS | v1.23 finite Physical Quantum Qi coherence kernel and partial dephasing | `formal/KuuOSPlanOSV1_23.lean` |
| DecisionOS | v0.6 WORLD-conditioned relational deliberation | `formal/KuuOSDecisionOSV0_6.lean` |
| MemoryOS | v1.00 finite bounded closed-support lattice | `formal/KuuOSMemoryOSV1_00.lean` |
| CodeAI | external benchmark comparison preregistration v0.1 | `docs/KUUOS_CODEAI_BASELINE_VERSUS_CODEAI_ABLATION_COMPARISON_v0_1.md` |
| Repository formal baseline | strict aggregate import | `formal/KuuOSFormal.lean` |
| Canonical runtime root | repository、PlanOS、DecisionOS、MemoryOS、CodeAI current frontier | `runtime/kuuos_current_check.py` |

subsystem versionは独立しています。ObserveOS v0.7、VerifyOS v0.15、PlanOS v1.23、DecisionOS v0.6、MemoryOS v1.00、self-organization v0.113、CodeAI各v0.1 stageを、一つの直線的version番号として扱いません。

## CodeAIの現在の評価frontier

`main`には、外部一般benchmarkを扱う次の系列が統合されています。

```text
SWE-bench Verified protocol and adapter
→ exact external corpus acquisition and freeze receipt
→ evaluator-only gold-patch environment smoke validation
→ bounded non-gold official harness execution
→ aggregate result and process-evidence ingestion
→ baseline-versus-CodeAI and ablation comparison preregistration
```

現在までに確認された外部実行は、固定された1件のengineering smoke sampleです。

```text
instance: sympy__sympy-20590
patch applied: true
evaluation completed: true
resolved: false
FAIL_TO_PASS: 0 success / 1 failure
PASS_TO_PASS: 21 success / 0 failure
execution errors: 0
```

この`0/1`は観測済みevidenceとして保持されます。CodeAI全体の性能推定、正しさ、一般化、優越性を意味しません。

PR #1341は、1つのbaseline、CodeAI full、3つのablation、共通holdout、事前固定metric、欠測・実行失敗の扱いをpreregisterしました。比較は未完了です。PR #1342は、その比較を実行可能にするfrozen cohort、prediction pack、external-only shard contractを提案していますが、まだ`main`の事実ではありません。

## Canonical runtime root

標準入口は次です。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

current rootはrun-all-then-decideです。一つのstepが失敗しても残りを実行し、必要stepの失敗を最後に集約します。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py --summary
PYTHONPATH=. python3 runtime/kuuos_current_check.py --list

PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile repository
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile decisionos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile memoryos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile codeai
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile all
```

| Profile | 検査面 |
|---|---|
| `repository` | repository mutationとself-organizationの累積lineage |
| `planos` | PlanOS v0.91-v1.23 active frontier |
| `decisionos` | DecisionOS v0.1-v0.6 cumulative validation |
| `memoryos` | MemoryOS v0.40-v1.00 active frontier |
| `codeai` | PR #1341のcomparison preregistrationと直接predecessor regression |
| `all` | 上記すべて |

ObserveOS v0.7とVerifyOS v0.13-v0.15は、各専用workflow、Evidence Cycle累積runner、versioned formal aggregateで独立検証します。current root成功は、登録されたrepository内surfaceがそのrevisionで再現可能に整合したことを示します。外部定理受理、経験的真理、臨床承認、組織承認、production deployment、無制限実行権限を意味しません。

## Formal validation

Lean toolchainと依存はrepositoryに固定されています。

```bash
lake update
lake exe cache get
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

CodeAI comparison frontierだけをstrict buildする場合は次です。

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSCodeAIBaselineVersusCodeAIAblationComparisonV0_1
```

formal compilationはrepository内の定義と定理が固定toolchainで検査されたことを示します。外部査読、経験的妥当性、運用承認を代替しません。

## Legacy compatibility status surface

現行のsource of truthは`runtime/kuuos_current_check.py`です。次のlegacy identifiersとstable entrypointは、self-organization lineageおよび既存status consumerとの後方互換性のため保持します。

```text
KuuOS README Public Status v0.66
kuuos_current_root_sequence_v0_66
docs/kuuos_self_organization_active_state.md
```

| Surface | Path |
|---|---|
| Stable current surface CLI | `runtime/kuuos_current_surface.py` |
| Versioned current surface entrypoint | `runtime/kuuos_current_surface_entrypoint_v0_77.py` |
| Current surface index | `status/current.surface.index.json` |
| Current surface artifact | `status/current.surface.json` |
| Current resolved status artifact | `status/current.resolved.json` |
| Current manifest | `status/current.manifest.json` |

これらは互換・履歴surfaceであり、CodeAIを含むcanonical runtime rootの代替ではありません。

## Repository map

| Path | 役割 |
|---|---|
| `runtime/` | executable kernels、receipts、validators、canonical current root |
| `scripts/` | fail-closed checkers、fixture projection、cumulative runners |
| `formal/` | Lean theorem packagesとaggregate imports |
| `manifests/` | machine-readable package bindings |
| `examples/` | deterministic reference projections |
| `status/` | historical and compatibility status artifacts |
| `docs/` | versioned specifications and subsystem indexes |
| `tests/` | runtime、binding、tamper、boundary、regression tests |
| `.github/workflows/` | governance and subsystem validation gates |

主要なsubsystem index:

- `docs/ObserveOS/README.md`
- `docs/VerifyOS/README.md`
- `docs/CodeAI/README.md`
- `ROADMAP.md`

## 開発原則

変更はexact `main` SHAからdedicated branchを作り、通常はDraft PRとして提出します。CI判断にはcompleted run、job、step、artifact、logだけを使い、queuedまたはin-progressを成功・失敗の確定証拠にしません。

runtime、checker、manifest、documentation、formal packageを同じ責任境界へ揃えます。候補、証拠、検証、承認、権限、実行効果は別artifactとして保持し、後続権限をreceiptから自動生成しません。

## 固定境界

```text
candidate != authority
validation != truth
formal compilation != external theorem acceptance
CI success != correctness or performance

observation != verification
verification outcome != truth
passed != WORLD adoption
failed != WORLD rejection
indeterminate != evidence deletion
disposition candidate != WORLD mutation
selection != execution
receipt != successor authority

aggregate benchmark evidence != raw gold evidence
one measured sample != population performance
preregistration != completed comparison
external harness completion != issue resolution
patch application != correctness
benchmark result != repository mutation authority

memory != belief sovereignty
closure fixed point != empirical truth
lattice structure != ranking
WORLD candidate != empirical fact
WORLD intake != WORLD update
Qi conditioning != authority grant
modular time != physical time

modeled repository transition != live Git mutation
current root success != production deployment
README public status != authority grant
```

詳細な次段階と更新条件は[ROADMAP.md](ROADMAP.md)に記載します。
