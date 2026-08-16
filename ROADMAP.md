# KuuOS / 空OS Roadmap

**基準日：2026年8月16日 JST**

この Roadmap は、`main` に統合済みの事実、canonical runtime root、専用 formal/CI authority、live 再検証、条件付き次段階を分離します。queued / in-progress CI、未merge branch、将来構想を current baseline へ混ぜません。

## 状態分類

| 表記 | 意味 |
|---|---|
| 統合済み | authoritative `main` に存在する |
| Current root | `runtime/kuuos_current_check.py` から deterministic / effect-free に検証される |
| Formal integrated | strict Lean theorem surface が `main` に統合済み |
| 専用CI | subsystem 固有 workflow で runtime / tests / formal package を検証する |
| Live verified | separately authorized live transaction が completed evidence で閉じた |
| Live再検証待ち | 実装は統合済みだが、その revision に対する fresh live transaction が未完了 |
| 条件付き候補 | authority / topology / evidence / scope の追加定義が必要 |
| Frozen boundary | append-only / tighten-only / overwrite-forbidden / same-root を維持する責任境界 |

## Authoritative baseline

```text
branch: main
baseline commit: 382c82dfb347bd323f3406e6893ca30c0b58be4f
latest integrated functional PR: #1390
integrated frontier: complete-overlap action-groupoid Cech semantic descent v0.1
current-frontier successor Draft: none designated
```

PR #1390 は exact base `main@9ba2e3aa9ca22b5349a72b0864ad3157ea45a455`、fixed head `39a39ea5a4c0c8dbd865c7d18bcc8b6f440cc2e8` で Governance Gate と strict Lean validation が completed / success となった後、merge commit `382c82dfb347bd323f3406e6893ca30c0b58be4f` として統合されました。

The moving `main` HEAD and a subsystem milestone are not interchangeable. A documentation/governance sync may advance `main` without changing mathematical authority; a new formal theorem must not be represented as integrated before its merge actually lands.

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
| Gauge-invariant dependent origination formal | dense descent → orbit quotient → action groupoid/isotropy → complete-overlap Cech descent | Formal integrated through #1390 |
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

The `architecture` profile covers the integrated v2.4 local-real Yin-Yang package and the focused v2.5 Wuxing/Fibonacci-history package.

The `dependent_origination` profile covers the executable/spec local-to-global descent contract introduced in #1386. The theorem-only stages #1387-#1390 remain under strict Lean / dedicated CI authority; the runtime root records their integrated metadata but does not replace Lean compilation with Python tests.

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

This stage imports a structural lesson from the `4d-mass-gap` gauge-invariance route but does not inherit physical Yang-Mills theorem authority.

### Stage B — formal dense descent (#1387)

With an explicit continuous global semantic extension and dense union of local realization images, Mathlib's continuous identity principle proves global gauge invariance.

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

The descended orbit-level semantic map is unique. The coarse quotient proves representative-independence but forgets stabilizers, isotropy, holonomy, curvature, and higher descent data.

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

### Stage E — complete-overlap groupoid Cech descent (#1390)

Integrated #1390 adds:

```text
local presentations x_i
transition arrows g_ij : x_i -> x_j
identity transitions
exact cocycle g_jk * g_ij = g_ik
CechSemanticCompatible
unique glued semantic value
orbit-level semantics
cross-scale compatibility
```

It sits beside the existing concrete theorem `MemoryOSGlobalWordCechDescentV0_82`: the older theorem gives four-root normalized-word transport algebra, while #1390 extracts a generic action-groupoid semantic gluing layer.

Frozen boundary:

```text
complete-overlap semantic gluing
!= arbitrary open-cover descent
!= arbitrary site/sheaf descent
!= existence of a global X-valued section
!= quotient-stack authority
!= higher descent
!= holonomy or curvature reconstruction
```

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

### 1. Keep the three canonical public/current surfaces synchronized

README, ROADMAP, and `runtime/kuuos_current_check.py` must advance as one responsibility boundary after a functional theorem merge.

Required invariants:

- exact integrated milestone commit and PR;
- no unmerged Draft represented as integrated;
- current Draft fields are `null` when no successor is designated;
- Qi v2.5 remains in the architecture profile;
- dependent-origination runtime/formal authority remains separated;
- legacy self-organization public-status markers remain present;
- completed CI only is used to finalize the public surface.

### 2. Strengthen Cech descent additively

Safe next formal stages are conditional, not implied by #1390:

- introduce an actual indexed cover / overlap structure rather than complete-overlap shorthand;
- distinguish pairwise overlap, triple-overlap cocycle, and global section existence;
- formulate refinement maps and refinement compatibility;
- retain transition arrows and cocycle under refinement;
- prove semantic gluing across an actual cover before introducing sheaf/stack terminology;
- only formulate quotient-stack or higher-descent claims after the required categorical/topological structure exists.

Do not jump directly from complete-overlap semantic gluing to arbitrary-site or higher-stack authority.

### 3. Perform fresh GitHub MCP v1.1 live verification when explicitly authorized

Use then-current exact `main` SHA and a fresh nonce. Inspect only completed run/job/step/artifact/log evidence. Preserve compensation as failed closeout, not success.

### 4. Materialize the CodeAI frozen cohort

From the integrated #1342 contract:

- materialize the pinned shared holdout;
- generate authentic prediction packs for all cohorts;
- bind prediction source, model/configuration, pipeline variant, and candidate digest;
- HOLD/BLOCK missingness, duplicate reuse, leakage, or cross-cohort contamination;
- separate generation authority from evaluation authority;
- establish shard readiness by independent receipt.

### 5. External-only shard execution and balanced comparison

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
