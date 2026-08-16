# KuuOS / 空OS Roadmap

**基準日：2026年8月16日 JST**

この Roadmap は、`main` に統合済みの事実、canonical runtime root、専用 formal/CI authority、未統合 Draft、条件付き次段階を分離します。queued / in-progress CI、未merge branch、将来構想を current baseline へ混ぜません。

## 状態分類

| 表記 | 意味 |
|---|---|
| 統合済み | authoritative `main` に存在する |
| Current root | `runtime/kuuos_current_check.py` から deterministic / effect-free に検証される |
| Formal integrated | strict Lean theorem surface が `main` に統合済み |
| 専用CI | subsystem 固有 workflow で runtime / tests / formal package を検証する |
| Live verified | separately authorized live transaction が completed evidence で閉じた |
| Live再検証待ち | 実装は統合済みだが、その revision に対する fresh live transaction が未完了 |
| Draft frontier | exact-base branch 上にあり、未統合 |
| 条件付き候補 | authority / topology / evidence / scope の追加定義が必要 |
| Frozen boundary | append-only / tighten-only / overwrite-forbidden / same-root を維持する責任境界 |

## Authoritative baseline

```text
branch: main
baseline commit: 9ba2e3aa9ca22b5349a72b0864ad3157ea45a455
latest integrated functional PR: #1389
integrated frontier: dependent-origination action groupoid / isotropy v0.1
current successor Draft: #1390
Draft base: main@9ba2e3aa9ca22b5349a72b0864ad3157ea45a455
Draft head at baseline inspection: 39a39ea5a4c0c8dbd865c7d18bcc8b6f440cc2e8
```

The moving `main` HEAD and a subsystem milestone are not interchangeable. A later documentation/governance merge may advance `main` without changing mathematical authority; conversely a new formal merge must not be represented as integrated before it actually lands.

## Integrated subsystem map

| 系列 | 到達点 | 状態 |
|---|---|---|
| Core governance | v0.1 | Frozen boundary |
| Horizon / Context Gauge | v0.12 / v0.13 | 統合済み、継続検証 |
| Finite-cycle agent | v0.20-v0.27 | 統合済み |
| Qi diagnostic lineage | v0.28 / v0.29 | 統合済み |
| Qi-WORLD | v2.3 | 統合済み |
| Qi local-real Yin-Yang geometry | v2.4 | 統合済み、Current root |
| Qi Wuxing/Fibonacci history geometry | v2.5 | 統合済み、Current root + 専用CI |
| Causal WORLD model | v14.0 | read-only dependency |
| Repository mutation | v1.24 | 完了系列 |
| Apoptosis Lifecycle Governance | v0.1-v0.36 | 独立完了系列 |
| Repository self-organization root | v0.113 | 統合済み、Current root |
| ObserveOS | v0.7 | 統合済み、専用CI |
| VerifyOS | v0.13-v0.15 | 統合済み、専用CI |
| PlanOS | v0.91-v1.23 | 統合済み、Current root |
| DecisionOS | v0.1-v0.6 | 統合済み、Current root |
| MemoryOS | v0.40-v1.00 | 統合済み、Current root |
| CodeAI external benchmark | frozen cohort / prediction-pack / execution-shard contract | 統合済み、Current root |
| GitHub MCP official-server bridge | v0.1-v1.1 | 統合済み、Current root |
| Gauge-invariant dependent origination runtime | local-to-global descent v0.1 | 統合済み、Current root |
| Gauge-invariant dependent origination formal | dense descent → orbit quotient → action groupoid/isotropy | Formal integrated through #1389 |
| Groupoid Cech semantic descent | complete-overlap v0.1 | Draft #1390 |
| Repository strict Lean baseline | `formal/KuuOSFormal.lean` | 継続検証 |

Subsystem versions remain independent; they are not one maturity scale.

## Canonical runtime root

Standard entrypoint:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

Profiles:

```text
repository
architecture
planos
decisionos
memoryos
codeai
github_mcp
dependent_origination
all
```

The `architecture` profile now covers the integrated v2.4 local-real Yin-Yang package and the focused v2.5 Wuxing/Fibonacci-history package.

The `dependent_origination` profile covers the executable/spec local-to-global descent contract introduced in #1386. The theorem-only stages #1387-#1389 remain under strict Lean / dedicated CI authority; the runtime root records their metadata but does not replace Lean compilation with Python tests.

The root remains effect-free. It must not perform live GitHub writes, workflow dispatch, benchmark execution, Docker evaluation, external artifact acquisition, or gold-material access.

## Qi architecture frontier

PR #1385 integrated Qi Yin-Yang Wuxing Fibonacci History Geometry v2.5 from the clean CI reset branch.

Core algebraic model:

```text
s^5 = 1
tau^2 = 1 + tau
X = s tensor tau
X^5 = 1 tensor (3 + 5 tau)
```

Interpretation:

```text
Wuxing phase = Z5 current-phase coordinate
Yin-Yang = local orientation / real-structure reversal
Fibonacci sector = history fiber not reducible to current phase
golden ratio = positive history-growth eigenvalue
```

Frozen non-overclaims:

```text
classical Wuxing != historically identical to SU(2)_3
Qi != anyon / particle
phase return != history erasure
log(phi) != clinical severity or thermodynamic entropy claim
```

## Dependent-origination theorem spine

### Stage A — runtime/spec descent contract (#1386)

Integrated obligations:

```text
no privileged gauge representative
semantic invariance distinct from presentation equivariance
exact same-root local/global readout
equivariant realization/interpolation
local gauge invariance
dense local-to-global coverage when density route is used
continuous global extension witness remains explicit
cross-scale compatibility is generated only after exact global readout exists
append-only / tighten-only / overwrite-forbidden
```

This stage imports a structural lesson from the current `4d-mass-gap` gauge-invariance route but does not inherit physical Yang-Mills theorem authority.

### Stage B — formal dense descent (#1387)

With an explicit continuous global semantic extension and dense union of local realization images, Mathlib's continuous identity principle is used to prove global gauge invariance.

Integrated results include:

```text
crossScaleCompatible_of_globalReadout
semantic_invariant_of_dense_local_realization
continuous_globalReadout_unique_of_dense
semantic_eq_of_gauge_related
dense_descent_invariance_and_compatibility
```

Critical boundary:

```text
density + cross-scale compatibility
!=
existence of a continuous global extension
```

### Stage C — coarse orbit quotient (#1388)

Global semantic invariance is converted to its universal-property form:

```text
X -> X/G -> Semantic
```

The descended orbit-level semantic map is unique. This proves representative-independence at the coarse quotient level.

Critical boundary: the coarse quotient forgets stabilizers, isotropy, holonomy, curvature, and higher descent data.

### Stage D — action groupoid and isotropy (#1389)

The action groupoid retains actual transformation arrows:

```text
ActionArrow x y := { g : Gauge // g • x = y }
```

Integrated formal content includes identity, composition, inverses, arrow constancy of invariant semantics, isotropy/stabilizer equivalence, and conjugation transport of isotropy along arrows.

Conceptual refinement:

```text
G ⋉ X --0-truncation--> X/G
```

The quotient carries invariant semantic value; the action groupoid retains relational presentation structure.

### Stage E — complete-overlap groupoid Cech descent (#1390, Draft)

Draft #1390 adds local presentations, exact transition arrows, identity transitions, exact cocycle composition, and unique chart-independent semantic gluing over a complete-overlap abstraction.

It must remain explicitly weaker than:

```text
arbitrary open-cover descent
arbitrary site/sheaf descent
existence of a global X-valued section
quotient-stack authority
higher descent
holonomy or curvature reconstruction
```

Do not promote #1390 into the integrated baseline until its fixed final head has completed required validation and is merged.

## GitHub MCP live state

The v0.4-v0.9 reversible live stages have completed evidence in their respective scopes. v1.0-v1.0.2 exposed a stable service-surface asymmetry: downward nested hierarchy could be observed exactly while direct nested `get_parent` remained null throughout the bounded window. Each failed transaction was compensated from the leaf edge and residual hierarchy was not accepted as success.

v1.1 keeps a short direct read, then cross-observes exact parent metadata through official MCP reads when needed. Removal requires direct null observation. The implementation is integrated; a fresh live verification is operationally separate from deterministic current-root validation.

## CodeAI evaluation state

Integrated contract:

```text
shared holdout slots: 100
cohorts: baseline / CodeAI full / 3 ablations
shards per cohort: 10
samples per shard: 10
total external-only shards: 50
```

Still incomplete:

```text
external shared-holdout materialization
authentic prediction packs complete
execution shards ready
external comparison execution
balanced comparison completed
performance claim approved
```

A single observed non-gold sample remains only sample-level evidence.

## Priority order

### 1. Close Draft #1390 without weakening the boundary

Required before integration:

- fixed final head;
- exact base relationship understood;
- completed/success required CI only;
- strict Lean validation on the actual final head;
- mergeability;
- review and unresolved-thread audit;
- no duplicate same-series active PR;
- no theorem-statement weakening to accommodate CI or infrastructure behavior.

If #1390 integrates, the next public-surface synchronization should advance the baseline only after the merge commit is authoritative.

### 2. Strengthen Cech descent additively

Safe next stages after #1390 are conditional, not implied:

- introduce an actual cover/index structure rather than complete-overlap shorthand;
- distinguish overlap existence from global section existence;
- state refinement compatibility explicitly;
- retain arrows/cocycle under refinement;
- formulate sheaf/stack-like semantics only after the required categorical/topological structure exists;
- keep semantic gluing distinct from reconstruction of a global `X`-valued representative.

No jump directly from complete-overlap semantic gluing to quotient-stack or higher-stack claims.

### 3. Keep README / ROADMAP / runtime root synchronized

Treat these three files as one public/current responsibility boundary:

- baseline date and exact integrated milestone;
- current Draft metadata;
- Qi v2.5 architecture status;
- dependent-origination runtime/formal split;
- profile list and deterministic step membership;
- frozen non-overclaims.

### 4. Perform fresh GitHub MCP v1.1 live verification when explicitly authorized

Use then-current exact `main` SHA and a fresh nonce. Inspect only completed run/job/step/artifact/log evidence. Preserve compensation as failed closeout, not success.

### 5. Materialize the CodeAI frozen cohort

From the integrated #1342 contract:

- materialize the pinned shared holdout;
- generate authentic prediction packs for all cohorts;
- bind prediction source, model/configuration, pipeline variant, and candidate digest;
- HOLD/BLOCK missingness, duplicate reuse, leakage, or cross-cohort contamination;
- separate generation authority from evaluation authority;
- establish shard readiness by independent receipt.

### 6. External-only shard execution and balanced comparison

- use the pinned official harness/environment;
- preserve shard-level failures instead of silently excluding them;
- keep raw gold/evaluation material outside ordinary current-root surfaces;
- use resolved rate as the preregistered primary metric only after cohort completeness;
- retain FAIL_TO_PASS, PASS_TO_PASS, execution-valid-rate, error-rate, uncertainty, and failure distribution;
- keep comparison completion separate from performance-claim approval.

## Frozen boundaries

The following remain tighten-only unless a new versioned authority root explicitly supersedes them:

```text
candidate != authority
observation != verification
validation != truth
formal compilation != external theorem acceptance
receipt != successor authority
selection != execution

semantic invariance != presentation immobility
density + compatibility != global-extension existence
coarse quotient != retained isotropy
action groupoid != quotient stack
Cech semantic gluing != global X-valued section
complete overlap != arbitrary cover
KuuOS gauge descent != physical Yang-Mills theorem authority

write accepted != effect verified
compensation != success
MCP write capability != Git authority

one benchmark sample != population performance
contract admitted != execution ready
comparison complete != performance claim approved
```

## Governance rule

Repository evolution at the current frontier remains:

```text
append-only
tighten-only
overwrite-forbidden
same-root where the theorem/receipt requires it
exact-base Draft-first
completed-CI evidence only
```

These are status criteria, not decorative documentation conventions.
