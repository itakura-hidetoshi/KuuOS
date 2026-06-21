# KuuOS / 空OS Roadmap

**Baseline date: 2026-06-21**

This roadmap replaces the former v0.12–v0.13-centered orientation with the current multi-spine state of the repository.

KuuOS now has five concurrently maintained public lanes:

```text
A. governance and local-context gauge architecture
B. OS responsibility and bounded finite-cycle operation
C. Qi process history and diagnostic-candidate projection
D. Qi-WORLD externally licensed closed-cycle materialization
E. WORLD read-only mathematical and formal sidecar
```

The goal is not unrestricted autonomy. The goal is a system in which every candidate, state transition, proof surface, memory record, licensed effect and WORLD representation knows its source, scope, owner, boundary and stop condition.

---

## 0. Fixed non-collapse boundary

The following remain fixed unless a later, explicit, reviewed release changes them:

```text
candidate != authority
validation != truth
CI pass != external theorem acceptance
observation != intervention license
belief state != fact
DecisionOS selection != execution
PlanOS replan != activation
LearnOS delta != present action
ActOS receipt != successor authority
closed-cycle receipt != next-cycle start
memory persistence != belief sovereignty
diagnostic candidate != final diagnosis
recovery-window interval != healing guarantee
red flag != automatic triage
WORLD sidecar != exact WORLD
finite analytic certificate != physical realization
local chart != global graph node
curvature != veto
holonomy != sovereign memory
```

All roadmap phases preserve:

```text
append-only lineage
exact source and digest binding
fresh authority where execution is involved
finite cost, time, steps and resource lease
foreground pause / terminate / handover
independent post-effect observation
replay idempotence and stale-state rejection
visible uncertainty, dissent, residue and counterevidence
medical-modality neutrality
proof-status separation
```

---

## 1. Current public baseline

| Lane | Current baseline | Status |
|---|---|---|
| Core governance | v0.1 public governance and boundary documents | active, maintained |
| Horizon/context gauge | Horizon v0.12 + Context Gauge Atlas v0.13 | implemented baseline |
| PlanOS | Qi-conditioned non-Markov Replan v0.2 | implemented and merged |
| Autonomous-agent completion | v0.20–v0.27 finite-cycle continuity | implemented and merged |
| Qi diagnostic candidate | v0.28 recovery-window layer | implemented and merged |
| Qi-WORLD | v2.2 concrete third licensed cycle | implemented and merged |
| WORLD | v0.48 finite log-Sobolev, contraction and mixing bridge | implemented and merged |
| Formal root | `KuuOSFormal` | strict Lean build surface |
| Central runtime | `run_kuuos_runtime_full_check_v0_48.py` | active regression root |

---

## 2. Completed foundations

### 2.1 Public governance and validation

**Status: complete baseline; ongoing maintenance**

Completed:

- public core governance, non-authority and medical-modality-neutral boundaries;
- validator tier separation and anti-loop governance;
- manifests, cases, receipts and reproducible GitHub Actions;
- finite audit and repair-oriented outcomes;
- separation of validation, theorem status, clinical authority and execution authority.

Maintenance requirement:

```text
No merged runtime or formal layer may leave README, ROADMAP,
the formal root or the central runtime full check materially stale.
```

### 2.2 Horizon and context gauge architecture

**Status: implemented baseline**

Completed:

```text
short / medium / long horizon sections
  -> connection residuals
  -> bounded arbitration curvature
  -> plurality-preserving transport
  -> one bounded child cycle
  -> effect-grounded outcome
  -> replay-safe holonomy
```

and:

```text
context chart
  -> overlap eligibility
  -> local-section parallel transport
  -> atlas curvature and cocycle defect
  -> chart-local state and holonomy
```

Future work is composition maturity, not conversion into a global graph.

### 2.3 OS ownership and Replan

**Status: implemented**

The responsibility boundary is now explicit:

```text
ObserveOS observes
BeliefOS maintains local/plural belief
DecisionOS selects an admissible candidate
PlanOS synthesizes plans and replans
ActOS executes only under an exact license
VerifyOS evaluates independent evidence
LearnOS records future-only deltas
MemoryOS preserves lineage and reconstruction
```

PlanOS v0.2 is the owner of Replan synthesis. No separate ReplanOS is planned.

### 2.4 Finite-cycle autonomous-agent completion

**Status: implemented through v0.27**

The v0.20–v0.26 contracts are composed into:

```text
restart-safe
user-interruptible
resource-bounded
repeatable finite-cycle
autonomous-agent kernel
```

Completed capabilities include:

- persistent mission binding;
- observation and plural belief state;
- semantic planning and independent verification;
- bounded learning and cognitive memory;
- transactional intended-versus-observed effect reconciliation;
- wake-up, foreground control and resource admission;
- governed change management;
- exact checkpoints, append-only ledger replay and snapshot repair;
- process-restart and host-restart recovery;
- explicit finite renewal followed by explicit resume.

This is repeatable continuity, not an unbounded cycle.

### 2.5 Qi recovery-window diagnostic candidate

**Status: implemented through v0.28**

Completed:

- multi-time Qi Process Tensor history;
- plural diagnostic hypotheses;
- support, counterevidence, uncertainty and source traces;
- bounded recovery-window interval;
- separation of severity from irreversibility;
- open-future preservation after negative response;
- clinician-review handoff for declared red flags;
- append-only replay-safe candidate ledger;
- formal non-authority boundaries.

This lane does not generate treatment, triage or final diagnosis.

### 2.6 Qi-WORLD licensed-cycle materialization

**Status: concrete three-cycle chain completed at v2.2**

Completed path:

```text
first licensed effect and native closure
  -> immutable closed-cycle receipt
  -> fresh successor authority intake
  -> second licensed cycle
  -> verified two-cycle prefix
  -> fresh third authority / approval / host license
  -> explicit single-use discharge
  -> concrete third ActOS effect
  -> native ObserveOS / VerifyOS / LearnOS / PlanOS closure
  -> immutable third receipt
  -> append-only three-cycle chain
```

The cycle count is three. No fourth cycle is started or implied.

### 2.7 WORLD mathematical sidecar

**Status: implemented through v0.48**

The current typed spine is:

```text
real Hilbert ℓ²
-> dense/self-adjoint operator bridge
-> noncommutative operator algebra
-> C*-local net
-> von Neumann and modular theory
-> Araki relative entropy
-> Petz recovery and conditional expectation
-> Jones basic construction and Jones tower
-> standard invariant, Q-system and fusion-category bridges
-> module category, tube/center and categorical IndraNet
-> higher-gauge information geometry
-> Araki-Petz quantum information geometry
-> dual-affine / Bregman projections
-> geodesic / mirror-descent / free-energy certificates
-> gradient-flow / JKO / entropy-production certificates
-> finite log-Sobolev contraction and mixing bounds
```

The runtime validates read-only, hash-bound receipts. It does not execute these mathematical structures or update WORLD.

---

## 3. Immediate priorities

### Priority 1 — Keep public orientation synchronized

**Status: active**

Tasks:

- keep README, ROADMAP, formal root and central full check aligned;
- maintain a compact current-baseline table;
- remove obsolete language that makes v0.13 appear to be the overall frontier;
- link each current lane to its primary specification, manifest, validator and Lean module;
- distinguish implemented, assumed, externally receipted and planned statements.

Acceptance:

```text
A first-time reviewer can identify the current frontier in under five minutes
without reading historical addenda.
```

### Priority 2 — Consolidate the v0.20–v0.28 agent status

**Status: next documentation and integration task**

Tasks:

- publish one current status document covering v0.20 through v0.28;
- bind v0.28 candidate reports explicitly to v0.27 checkpoints and lineage;
- preserve multiple reports without source-packet substitution;
- expose a compact validation matrix for every lower contract;
- clarify which failures lead to HOLD, REOBSERVE, REVIEW, TERMINATE or HANDOVER;
- keep diagnostic review routes separate from treatment and ActOS routes.

Acceptance:

```text
Every v0.28 report has an exact v0.27 source,
plural hypotheses remain visible,
and no diagnostic route grants action authority.
```

### Priority 3 — Generalize Qi-WORLD finite licensed-cycle construction

**Status: next formal/runtime frontier**

Goal:

```text
concrete three-cycle evidence
  -> reusable exact successor-cycle constructor
  -> arbitrary finite-prefix theorem
  -> concrete receipt binding for each new cycle
```

Tasks:

- generalize the v2.2 third-cycle constructor to a finite successor-cycle schema;
- preserve exact predecessor receipt and ordinal binding;
- require fresh external authority, human approval and host license for every effectful cycle;
- keep freshness qualification separate from explicit single-use discharge;
- preserve immutable closed prefixes;
- prove that an `n`-cycle receipt chain grants no `(n+1)`-cycle authority;
- add failure cases for authority reuse, skipped ordinal, altered prefix, stale plan basis and substituted native closure;
- retain explicit stop, hold and handover states.

Acceptance:

```text
for every finite prefix:
  exact predecessor binding
  + fresh authority
  + one explicit discharge
  + one concrete effect
  + native closure
  + immutable append
  + no automatic successor activation
```

### Priority 4 — Strengthen WORLD v0.48 proof status

**Status: parallel mathematical track**

Tasks:

- replace supplied finite certificate fields with derived mathlib theorems when hypotheses are sufficient;
- state external analytic receipts next to every finite Lean-direct result;
- separate finite recursive iteration from continuous-time semigroup claims;
- formalize contraction-factor iteration, equilibrium separation and mixing bounds as reusable lemmas;
- improve links between spectral gap, log-Sobolev and hypercontractive receipts without asserting equivalence prematurely;
- preserve higher-gauge covariance and multi-WORLD noncollapse;
- keep runtime read-only.

Acceptance:

```text
Every WORLD theorem is visibly classified as:
Lean-derived / hypothesis-supplied / external analytic receipt / future target.
```

### Priority 5 — Unified validation and release matrix

**Status: next infrastructure task**

Publish a matrix with:

```text
component
version
source files
manifest
validator
tests
Lean module
formal-root registration
workflow
failure classes
non-authority boundary
```

Required failure classes include:

- stale digest;
- replay duplication;
- substituted source packet;
- authority reuse;
- host-license mismatch;
- skipped phase or cycle ordinal;
- memory-root overwrite attempt;
- local-to-global context collapse;
- diagnostic finality promotion;
- WORLD physical-realization overclaim.

---

## 4. Near-term parallel tracks

### 4.1 Context Gauge Atlas composition

- direct versus composed transition functions;
- triple-overlap cocycle checks;
- path-sensitive holonomy comparison;
- chart aging and reobservation without lineage deletion;
- explicit proof that chart composition does not create a universal route.

### 4.2 MemoryOS and process-history integration

- connect scar, relapse, recovery and return-to-context history to chart-local transport;
- preserve individual lineage during collective reconstruction;
- prevent memory consolidation from erasing cocycle residue or uncertainty;
- distinguish memory reconstruction from belief promotion;
- integrate v0.27 checkpoints and v0.28 process histories without root overwrite.

### 4.3 Governed change management maturity

- strengthen rollback evidence and independent closure;
- preserve permanent forbidden-action categories;
- maintain bounded canary scope and finite deployment authorization;
- separate change review from ActOS deployment;
- add explicit expiry and post-deployment observation requirements.

### 4.4 Reviewer experience

- Japanese-first orientation with precise English technical names;
- compact architecture diagrams;
- current-versus-historical version map;
- “what a pass does not mean” callouts;
- direct links from roadmap items to validators and formal modules.

---

## 5. Medium-term research directions

### 5.1 Finite licensed autonomy theorem family

Develop a reusable theorem family for:

```text
finite mission prefix
finite resource lease
finite authority inventory
finite effect chain
append-only evidence
foreground interruption
restart recovery
no inherited successor authority
```

The target is mathematically explicit finite continuity, not an unbounded autonomous license.

### 5.2 WORLD-to-OS read-only observation bridge

Explore a bridge in which WORLD sidecar quantities can become typed observation candidates while preserving:

```text
WORLD representation != fact
sidecar quantity != control objective
low free energy != permission
mixing certificate != intervention recommendation
```

No WORLD formal result should directly activate PlanOS or ActOS.

### 5.3 Stronger proof discharge

For formal structures that currently carry external claim/proof receipt fields:

- identify minimal hypotheses;
- derive the finite consequence directly in Lean;
- isolate genuinely analytic or physical existence claims;
- keep theorem statements stable under stronger future discharge;
- avoid equating formal compilation with external mathematical acceptance.

### 5.4 Public reproducibility

- pinned Lean/mathlib toolchain;
- stdlib-only Python validators where practical;
- deterministic fixtures;
- exact hash/digest documentation;
- machine-readable release index;
- versioned evidence bundles.

---

## 6. Long-term direction

KuuOS is moving toward a public architecture where:

```text
claims know their support
observations know their source
beliefs know their uncertainty
sections know their chart
transitions know their overlap
memories know their lineage
plans know their owner and activation boundary
actions know their exact license
effects know their independent observation
learning knows it is future-only
receipts know they are evidence rather than authority
proofs know their formal and external status
WORLD representations know they are read-only sidecars
governance knows when to stop, hold, repair or hand over
```

The long-term target is not “more freedom for the agent.”  
It is **more exact relational continuity without authority collapse**.

---

## 7. Current priority summary

```text
1. Keep README/ROADMAP/formal root/full check synchronized.
2. Consolidate v0.20-v0.28 into one current public status and validation matrix.
3. Generalize Qi-WORLD v2.2 from a concrete third cycle to arbitrary finite prefixes.
4. Prove no finite closed chain grants automatic successor authority.
5. Strengthen WORLD v0.48 by replacing supplied certificates with derived theorems where possible.
6. Keep finite iteration separate from continuous-time and physical claims.
7. Integrate MemoryOS and Qi history without belief or root sovereignty.
8. Mature gauge-atlas composition without introducing global graph semantics.
9. Preserve foreground control, finite resources, explicit renewal and handover.
10. Keep diagnostic candidates, clinical authority, theorem status and execution authority separate.
```
