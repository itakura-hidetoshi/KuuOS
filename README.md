# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** は、観測・文脈・信念・記憶・WORLD表現・計画・判断・実行・再観測・検証・学習を、provenance、履歴、責任主体、有限権限、content address、検証可能な receipt に結び付ける公開研究アーキテクチャです。

KuuOS is a public, governance-gated, proof-facing, non-Markovian and relational AI research architecture. It keeps candidates separate from authority, evidence separate from truth, validation separate from acceptance, and selection separate from execution.

## 現在地

**基準日：2026年8月16日 JST**

Authoritative branch は `main` です。この公開面が表す統合済み functional baseline は:

```text
main: 9ba2e3aa9ca22b5349a72b0864ad3157ea45a455
latest integrated functional PR: #1389
frontier: dependent-origination action groupoid with retained isotropy
```

現在の successor は Draft PR #1390 **Glue dependent-origination semantics over groupoid Cech data** です。#1390 は `main@9ba2e3aa...` を exact base とする未統合 frontier であり、completed validation と merge が成立するまでは current baseline に含めません。

| 面 | 統合済み到達点 | 主な入口 |
|---|---|---|
| Repository lineage | self-organization v0.113 | `runtime/kuuos_current_root_sequence_v0_113.py` |
| ObserveOS | v0.7 sequential epistemic observability envelope | `docs/ObserveOS/README.md` |
| VerifyOS | v0.15 read-only outcome disposition handoff | `docs/VerifyOS/README.md` |
| Qi architecture | Qi Yin–Yang Wuxing Fibonacci History Geometry v2.5 | `docs/KUUOS_QI_YINYANG_WUXING_FIBONACCI_HISTORY_GEOMETRY_v2_5.md` |
| PlanOS | v1.23 finite Physical Quantum Qi coherence kernel and partial dephasing | `formal/KuuOSPlanOSV1_23.lean` |
| DecisionOS | v0.6 WORLD-conditioned relational deliberation | `formal/KuuOSDecisionOSV0_6.lean` |
| MemoryOS | v1.00 finite bounded closed-support lattice | `formal/KuuOSMemoryOSV1_00.lean` |
| CodeAI | frozen cohort / prediction-pack / execution-shard contract v0.1 | `docs/KUUOS_CODEAI_FROZEN_COHORT_PREDICTION_PACK_EXECUTION_SHARD_CONTRACT_v0_1.md` |
| GitHub MCP | sub-issue chain parent cross-observation v1.1 | `runtime/kuuos_github_mcp_sub_issue_chain_parent_cross_observation_v1_1.py` |
| Dependent origination runtime | gauge-invariant local-to-global descent v0.1 | `runtime/kuuos_gauge_invariant_dependent_origination_descent_v0_1.py` |
| Dependent origination formal | action groupoid / isotropy v0.1 | `formal/KUOS/GaugeInvariantDependentOriginationActionGroupoidV0_1.lean` |
| Repository formal baseline | strict aggregate import | `formal/KuuOSFormal.lean` |
| Canonical runtime root | integrated deterministic current surface | `runtime/kuuos_current_check.py` |

Subsystem versions are independent. ObserveOS v0.7, VerifyOS v0.15, Qi v2.5, PlanOS v1.23, DecisionOS v0.6, MemoryOS v1.00, repository self-organization v0.113, CodeAI v0.1 stages, GitHub MCP v0.1-v1.1, and dependent-origination v0.1 are not one linear maturity scale.

## Dependent origination / gauge descent frontier

The current mathematical spine is additive and tighten-only:

```text
PR #1386
runtime/spec doctrine for gauge-invariant local-to-global dependent origination

PR #1387
dense local realization
+ equivariance
+ local gauge invariance
+ explicit continuous global semantic extension
=> global semantic gauge invariance
=> cross-scale compatibility
=> uniqueness on a dense carrier

PR #1388
global gauge invariance
<=> factorization through the coarse gauge-orbit quotient
=> unique orbit-level semantics

PR #1389
action groupoid G ⋉ X
=> actual transformation arrows are retained
=> isotropy is identified with stabilizer data
=> isotropy transports along arrows by conjugation
=> coarse orbit projection is recognized as a 0-truncation that forgets isotropy

Draft PR #1390
complete-overlap action-groupoid Cech data
=> exact transition arrows and cocycle
=> chart-independent semantic compatibility
=> unique glued semantic value
```

KuuOS reading:

```text
空   = no representative or chart has independent semantic authority
縁起 = local conditioned appearances are related by explicit transport/arrows/cocycle
二諦 = invariant conventional structure is not promoted to ultimate substance
中道 = neither coordinate reification nor erasure of relational structure
```

The distinction is deliberate:

```text
semantic meaning        -> gauge invariant
presentation / carrier  -> may transform equivariantly
```

The formal chain does **not** infer existence of a continuous global semantic extension from density plus compatibility. That extension remains an explicit obligation. The coarse orbit quotient does not retain isotropy, holonomy, curvature, sheaf gluing, or higher descent data; the action-groupoid layer restores arrows and isotropy only. Draft #1390 is a complete-overlap Cech abstraction, not yet an arbitrary-open-cover, arbitrary-site, quotient-stack, or global `X`-valued-section theorem.

The motivating physical proof pattern is imported structurally from `itakura-hidetoshi/4d-mass-gap`, but KuuOS does not thereby acquire physical Yang–Mills theorem authority.

## Qi architecture v2.5

Qi Yin–Yang Wuxing Fibonacci History Geometry v2.5 is an additive layer over v2.4.

```text
s^5 = 1
tau^2 = 1 + tau
X = s tensor tau
X^5 = 1 tensor (3 + 5 tau)
```

The core statement is:

```text
phase can return while history does not return.
```

`Z5` is used as a cyclic phase coordinate for Wuxing; Fibonacci fusion is a history fiber; the golden ratio is the positive growth eigenvalue of that history recursion. The layer does not identify classical Wuxing historically or physically with `SU(2)_3`, does not claim biological Fibonacci anyons, and does not identify Qi with a particle or anyon.

## GitHub MCP frontier

The official `github/github-mcp-server` is treated as a bounded adapter under KuuOS authority rather than an unrestricted source of authority.

```text
v0.1 transport / discovery / bounded admission
→ v0.2 write-capable authority adapter
→ v0.3 independent post-write reobservation
→ v0.4 reversible live Issue canary
→ v0.5 / v0.5.1 workflow dispatch and immutable image digest
→ v0.6 reversible repository-label transaction
→ v0.7-v0.7.2 reversible Issue–Label binding
→ v0.8 reversible sub-issue binding
→ v0.9 bidirectional hierarchy verification
→ v1.0 three-level root → child → grandchild chain
→ v1.0.1 / v1.0.2 bounded parent reobservation
→ v1.1 nested-parent cross-observation
```

The v1.0-v1.0.2 live runs established an important service-surface boundary: the downward child→grandchild relation could be exact while the grandchild direct `issue_read(get_parent)` remained null across the bounded window. v1.1 therefore cross-observes the child-side `has_parent` / `parent_issue_url` and independently reads the expected parent before synthesizing the existing exact-parent shape. Removal still requires direct null observation. Compensation is recovery evidence, never VERIFIED success.

## CodeAI evaluation frontier

The external benchmark line has reached the frozen cohort / prediction-pack / execution-shard contract:

```text
SWE-bench Verified protocol
→ pinned corpus freeze
→ evaluator-only gold environment smoke
→ bounded non-gold official harness execution
→ aggregate result/process-evidence ingestion
→ baseline vs CodeAI + ablation preregistration
→ frozen cohort / prediction-pack / execution-shard contract
```

PR #1342 fixes a shared 100-slot holdout ledger, baseline / CodeAI full / three ablations, ten shards per cohort, and fifty external-only shards in total. Authentic prediction packs, shard readiness, full external comparison, and any performance claim remain incomplete.

One fixed non-gold engineering smoke sample has been observed; it is evidence for that sample only and is not a population-level performance claim.

## Canonical runtime root

Standard entrypoint:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

The root is run-all-then-decide: one failed required step does not prevent the remaining bounded checks from running, and required failures are aggregated at the end.

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py --summary
PYTHONPATH=. python3 runtime/kuuos_current_check.py --list

PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile repository
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile architecture
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile decisionos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile memoryos
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile codeai
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile github_mcp
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile dependent_origination
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile all
```

| Profile | Bounded validation surface |
|---|---|
| `repository` | repository mutation and self-organization lineage |
| `architecture` | Qi v2.4 plus integrated v2.5 deterministic package checks |
| `planos` | PlanOS v0.91-v1.23 |
| `decisionos` | DecisionOS v0.1-v0.6 |
| `memoryos` | MemoryOS v0.40-v1.00 |
| `codeai` | #1342 contract, #1341 comparison projection, direct regressions |
| `github_mcp` | v1.0 chain contract and v1.1 cross-observation |
| `dependent_origination` | integrated runtime/spec local-to-global descent contract |
| `all` | all profiles above |

The canonical root is deterministic and effect-free. It does not perform live GitHub writes, workflow dispatch, external benchmark execution, external artifact acquisition, or gold-material access. The latest dependent-origination theorem layers (#1387-#1389) remain strict Lean / dedicated-CI authority; the runtime root records their integrated frontier but does not pretend that Python checks substitute for Lean compilation.

## Formal validation

Lean toolchain and dependencies are repository-pinned.

```bash
lake update
lake exe cache get
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

Focused Qi v2.5 validation:

```bash
PYTHONPATH=. python3 scripts/check_qi_yinyang_wuxing_fibonacci_history_geometry_v2_5.py
PYTHONPATH=. python3 -m unittest -v tests.test_qi_yinyang_wuxing_fibonacci_history_geometry_v2_5
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.Architecture.QiYinYangWuxingFibonacciHistoryGeometryV2_5
```

Formal compilation proves only the repository theorem surface under the pinned toolchain. It does not substitute for external theorem acceptance, empirical validity, clinical approval, organizational approval, production deployment, or live-service behavior.

## Legacy compatibility status surface

The current source of truth is `runtime/kuuos_current_check.py`, but the following historical identifiers remain present because the self-organization status lineage validates them as backward-compatible public-status markers:

```text
KuuOS README Public Status v0.66
kuuos_current_root_sequence_v0_66
docs/kuuos_self_organization_active_state.md
README public status != authority grant
```

These identifiers are compatibility markers only. They do not replace the canonical runtime root and do not grant execution or mutation authority.

## Repository map

| Path | Role |
|---|---|
| `runtime/` | executable kernels, receipts, validators, canonical current root |
| `scripts/` | fail-closed checkers and cumulative runners |
| `formal/` | Lean theorem packages and aggregate roots |
| `specs/` | machine-readable / reviewable contracts |
| `manifests/` | package bindings and content-addressed declarations |
| `examples/` | deterministic reference projections |
| `status/` | historical and compatibility status artifacts |
| `docs/` | versioned theory, doctrine, subsystem indexes |
| `tests/` | runtime, tamper, boundary, and regression tests |
| `.github/workflows/` | governance, focused validation, separately authorized live gates |

Major subsystem indexes:

- `docs/ObserveOS/README.md`
- `docs/VerifyOS/README.md`
- `docs/CodeAI/README.md`
- `ROADMAP.md`

## Development invariants

Normal changes begin from an exact `main` SHA on a dedicated branch and usually enter as Draft PRs. Only completed runs/jobs/steps/artifacts/logs are final CI evidence; queued or in-progress state is not success or failure evidence. Do not weaken theorem statements or authority contracts to conceal infrastructure or service-surface behavior.

Repository evolution remains append-only or tighten-only at frozen boundaries. Overwrite of accepted roots is forbidden unless a versioned migration explicitly creates a new authority root. Same-root readout requirements remain explicit wherever a theorem or receipt depends on them.

## Fixed boundaries

```text
candidate != authority
validation != truth
formal compilation != external theorem acceptance
CI success != correctness or performance

observation != verification
verification outcome != truth
selection != execution
receipt != successor authority

semantic invariance != presentation immobility
density + compatibility != existence of a global continuous extension
coarse orbit quotient != retained isotropy
action groupoid != quotient stack
complete-overlap Cech data != arbitrary-site descent
KuuOS gauge descent != physical Yang-Mills theorem authority

MCP configured != tool discovered
tool discovered != operation admitted
operation admitted != effect verified
write accepted != verified closeout
compensation != success
MCP write capability != Git authority

one benchmark sample != population performance
preregistration != completed comparison
contract admitted != prediction packs complete
contract admitted != execution shards ready
```

## Safety / research status

KuuOS is a research architecture. Repository-local validation establishes bounded consistency of the represented artifact set; it does not establish medical efficacy, legal authority, autonomous operational authority, physical truth, or universal external-service guarantees.
