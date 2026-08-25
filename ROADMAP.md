# KuuOS / 空OS Roadmap

**基準日：2026年8月25日 JST**

この Roadmap は、authoritative `main` に統合済みの事実、canonical runtime root、strict Lean formal authority、live 再検証、条件付き次段階を分離します。queued / in-progress CI、未merge branch、将来構想を current baseline へ混ぜません。

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
functional milestone commit: 79e6d48029700fc3c998d28c87db069b3120bdab
latest integrated functional PR: #1420
parent formal frontier: filtered categorical cofinal dependent-origination semantics v1.4
downstream quantum specialization: integrated through #1415
runtime dependent-origination executable surface: #1386 adapter v0.1
current-frontier successor Draft: none designated
```

PR #1420 は exact base `main@3825d14c74afe51b1da7ce6a61819e909a6d0172`、fixed head `dc72e4dc022688002f8b99ab00acedef27b65211` で Governance Gate、Strict Lean formal validation、exact `Run selected Lean check` が completed / success となった後、normal merge commit `79e6d48029700fc3c998d28c87db069b3120bdab` として統合されました。

A later documentation/governance sync may advance the moving `main` HEAD without changing this functional milestone. Formal theorem authority is never inferred from an unmerged branch.

## Integrated subsystem map

| 系列 | 到達点 | 状態 |
|---|---|---|
| Core governance | v0.1 | Frozen boundary |
| Horizon / Context Gauge | v0.12 / v0.13 | 統合済み |
| Finite-cycle agent | v0.20-v0.27 | 統合済み |
| Qi diagnostic lineage | v0.28 / v0.29 | 統合済み |
| Qi-WORLD | v2.3 | 統合済み |
| Qi local-real Yin-Yang geometry | v2.4 | 統合済み、Current root |
| Qi Wuxing/Fibonacci history geometry | v2.5 | 統合済み、Current root + 専用CI |
| Causal WORLD model | v14.0 | read-only dependency |
| Repository self-organization root | v0.113 | 統合済み、Current root |
| ObserveOS | v0.7 | 統合済み、専用CI |
| VerifyOS | v0.15 | 統合済み、専用CI |
| PlanOS | v1.23 | 統合済み、Current root |
| DecisionOS | v0.6 | 統合済み、Current root |
| MemoryOS | v1.00 | 統合済み、Current root |
| CodeAI external benchmark | frozen cohort / prediction-pack / execution-shard contract v0.1 | 統合済み、Current root |
| GitHub MCP official-server bridge | v1.1 parent cross-observation | 統合済み、Current root |
| Dependent origination runtime | gauge-invariant local-to-global adapter v0.1 (#1386) | 統合済み、Current root |
| Dependent origination parent formal | filtered categorical cofinal semantics v1.4 (#1420) | Formal integrated |
| Dependent origination quantum specialization | Choi / CPTP / instruments / comb / tester / dual recursion through #1415 | Formal integrated, downstream |
| Repository strict Lean baseline | `formal/KuuOSFormal.lean` | 継続検証 |

Subsystem versions remain independent; they are not one linear maturity scale.

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

The root remains deterministic and effect-free. It must not perform live GitHub writes, workflow dispatch, benchmark execution, Docker evaluation, external artifact acquisition, or gold-material access.

The `dependent_origination` runtime profile still validates the executable/spec local-to-global descent contract introduced in #1386. The formal theorem line from #1387 through #1420 remains strict Lean authority. The runtime root records that integrated frontier in metadata but does not pretend that Python runtime checks prove the theorem surface.

## Dependent-origination architecture: current status

### Parent layer — contextual transport

The parent mathematical object is a state-valued functor on a context category.

```text
Context --D--> Type
```

Morphisms are admissible relations/context changes and induce transport. Identity and composition laws are the core of dependent origination at this level. No groupoid, quantum, topology, site, sheaf, or physical assumption is required.

### Specializations already integrated

```text
groupoid / gauge / Cech
    reversible presentation-change specialization

finite transfer words / semigroup
    one-object irreversible specialization

history / free category / memory-lifted state
    ordered-history specialization

process tensor / Choi / CPTP / comb / instruments
    explicit operational and quantum specialization
```

The specializations do not redefine the parent.

## Formal milestone spine

### Phase 0 — pre-parent gauge/descent line (#1386-#1390)

This line established runtime doctrine, dense semantic descent, orbit quotient semantics, action-groupoid/isotropy structure, and complete-overlap groupoid Čech semantic gluing.

It remains valid as a reversible/gauge specialization, but it is no longer the parent definition of dependent origination.

### Phase 1 — generic transport and dynamic specializations (#1400-#1407)

Integrated milestones:

```text
#1400  FunctorialTransportSystem parent
#1401  exponential gap transport/readout decay specialization
#1402  linear transfer connected-readout decay
#1403  finite transfer words
#1404  history-sensitive transport
#1405  free-history category realization
#1406  explicit memory-lifted history transport
#1407  operational non-Markov process-tensor bridge
```

### Phase 2 — quantum realization (#1408-#1415)

Integrated downstream specialization:

```text
#1408  finite-dimensional Choi/comb representation
#1409  Choi PSD <-> Mathlib complete positivity
#1410  native CPTP composition and finite Choi words
#1411  instruments / Born histories / comb normalization
#1412  arbitrary multi-slot Choi contraction = joint Born law
#1413  open-comb operational history sensitivity
#1414  quantum tester probability law
#1415  causal tester normalization <-> dual recursive normalization
```

Frozen boundary:

```text
quantum realization != parent dependent origination
open-comb response != probability without tester normalization
physical Yang-Mills theorem authority remains external to KuuOS
```

### Phase 3 — restore and deepen the parent (#1416-#1420)

```text
#1416  contextual core v1.0
       context reindexing
       system hom/equivalence
       groupoid reversibility only as specialization

#1417  contextual descent v1.1
       root -> local -> common refinement
       overlap compatibility
       explicit state descent
       semantic descent without state descent

#1418  refinement transitivity v1.2
       refinement-of-refinement flattening
       exact nested-state-descent equivalence
       semantic transitivity

#1419  directed cofinal semantics v1.3
       preorder-directed refinement nets
       coherent state families
       order-cofinal semantic equivalence

#1420  filtered categorical cofinal semantics v1.4
       arbitrary indexing category
       common future objects
       eventual coequalization of parallel arrows
       coherent rooted diagram
       exact full/cofinal semantic equivalence
```

Current parent aggregate:

```text
formal/KUOS/DependentOriginationCoreSpineV1_4.lean
```

Current parent frontier:

```text
formal/KUOS/DependentOriginationFilteredCofinalCategoryV1_4.lean
```

## Current theorem boundary

The strongest current parent-level semantic statement is:

```text
coherent filtered contextual diagram
+ transport-invariant readout
=> one unique semantic value
```

and for an objectwise cofinal indexing functor:

```text
full filtered-diagram semantic descent
<->
cofinal-subsystem semantic descent
```

This does **not** imply:

```text
one root state exists
categorical colimit exists
objectwise cofinality is already Mathlib Functor.Final
Grothendieck topology exists
sheaf/stack descent holds
```

Root-state recovery continues to require explicit state-separation hypotheses.

## Priority order

### 1. Keep README / ROADMAP / runtime root synchronized

These three surfaces form one public/current responsibility boundary after functional theorem merges.

Required invariants:

- exact functional milestone commit and PR;
- no unmerged mathematical Draft represented as integrated;
- current Draft fields remain `null` unless a formal successor is explicitly designated;
- runtime executable authority and strict Lean authority remain separated;
- legacy self-organization compatibility markers are not silently deleted;
- completed CI only is used to finalize a public surface.

### 2. Relate explicit cofinality to standard categorical finality — conditionally

v1.4 uses an explicit objectwise cofinal indexing condition. A safe next formal unit is to connect it to standard category-theoretic finality only after the necessary comma-category connectedness/nonemptiness hypotheses are stated.

Target shape:

```text
explicit KuuOS cofinal witness
+ required connectivity data
=> standard final/cofinal functor certificate
=> semantic invariance transported through the standard theorem
```

Do not rename the current objectwise condition as a full Mathlib final-functor theorem before proving the missing structure.

### 3. Add an optional universal semantic carrier only after its universal property exists

A colimit-like or quotient-like semantic carrier may be introduced as an **optional specialization** after an actual universal property is formalized.

Required boundary:

```text
unique invariant readout value on each coherent diagram
!=
a constructed categorical colimit object
```

### 4. Bridge reversible Čech/groupoid work into the contextual parent

The older #1388-#1390 line should be related to the v1.x parent by explicit bridge theorems:

- action groupoid as a context category;
- groupoid transport as automatically reversible;
- Čech transition/cocycle data as a reversible refinement specialization;
- semantic gluing as an instance of parent-level semantic descent when hypotheses match.

The bridge must preserve the fact that the parent is not groupoid-only.

### 5. Bridge history/memory and quantum lines downward from the parent

Safe next bridges:

```text
free-history category -> contextual parent
memory-lifted state -> history specialization
process tensor -> explicit operational realization
quantum Choi/comb -> explicit finite-dimensional realization
```

No downstream realization may silently promote new assumptions into the parent structure.

### 6. Runtime metadata validation

The current runtime root should remain effect-free. A future deterministic checker may verify that declared parent-frontier files and milestone metadata exist and agree, but it must not substitute Python existence checks for Lean theorem compilation.

### 7. GitHub MCP fresh live verification when explicitly authorized

Use then-current exact `main` SHA and a fresh nonce. Inspect only completed run/job/step/artifact/log evidence. Compensation remains failed closeout evidence, never success.

### 8. Materialize the CodeAI frozen cohort

From the integrated contract:

- materialize the pinned shared holdout;
- generate authentic prediction packs for all cohorts;
- bind prediction source, model/configuration, pipeline variant, and candidate digest;
- HOLD/BLOCK missingness, duplicate reuse, leakage, or cross-cohort contamination;
- separate generation authority from evaluation authority;
- establish shard readiness independently.

### 9. External-only shard execution and balanced comparison

- use the pinned official harness/environment;
- preserve shard-level failures instead of silently excluding them;
- keep raw gold/evaluation material outside ordinary current-root surfaces;
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

contextual transport != substance ontology
semantic descent != state descent
semantic invariance != presentation immobility
cofinal semantic invariance != root-state existence
filtered indexing != categorical colimit
objectwise cofinality != standard final-functor theorem
groupoid specialization != parent dependent origination
quantum realization != parent dependent origination
KuuOS structural theorem != physical Yang-Mills theorem authority

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
overwrite-forbidden where frozen
same-root where theorem/receipt requires it
exact-base Draft-first
completed-CI evidence only
```

These are status criteria, not decorative documentation conventions.
