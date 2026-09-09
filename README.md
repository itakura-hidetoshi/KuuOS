# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), formally verified contextual systems, and bounded AI operation.

Its central question is not whether one representation is “the true model,” but:

> **Which structure survives justified change of context and presentation, how can local information be transported and glued coherently, and what universal property characterizes the surviving structure?**

KuuOS therefore connects:

```text
observation
context
transport
memory
WORLD representation
retrieval
planning
decision
action
re-observation
verification
provenance
authority boundaries
formal proof
```

The long-term mathematical objective is the **Dependent Origination Universality Program**. The long-term AI objective is to build systems that can move across changing representations while preserving justified invariants, exposing obstruction, and refusing to promote local success into global truth without evidence.

---

## Current canonical snapshot

**Documentation rewrite: 2026-09-10 JST**

The mathematical snapshot used for this README is canonical `main` after PR #1621:

```text
authoritative branch: main
latest theorem merge: PR #1621
latest theorem layer: v2.42
mathematical snapshot SHA: 0045c0c87c26f36ea525ef60ad26de174f2d4b3a
exact v2.42 proof head: 75470baad7642e302836988bf285a4d2e9e1bfa1
```

Pinned formal environment:

```text
Lean:    leanprover/lean4:v4.30.0-rc2
Mathlib: 5450b53e5ddc75d46418fabb605edbf36bd0beb6
```

Strict aggregate gate:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

The canonical theorem authority is the integrated `main` state at an exact SHA. A green validation-only branch, runtime receipt, model answer, retrieval result, memory summary, or old documentation snapshot does not supersede canonical theorem authority.

---

## What 空 means in KuuOS

KuuOS does **not** formalize the slogan “nothing exists.”

Its operational use of 空 (śūnyatā / emptiness) is an anti-reification discipline:

```text
no chosen presentation = intrinsic substance by default
no local observation = global truth by default
no retrieval score = entailment by default
no runtime success = WORLD truth by default
no formal encoding = philosophical uniqueness by default
no model generation = theorem authority by default
```

This is the bridge from 空 to 縁起:

```text
reified object
    ↓
context-indexed state
    +
admissible transport
    +
coherence
    +
descent / gluing
    +
obstruction
    +
presentation invariance
```

In KuuOS, **縁起 is not reduced to a graph metaphor or a single causal chain**. It is treated as relational/contextual dependence together with transport, history, compatibility, and the possibility that local data fail to glue globally.

KuuOS also maintains interpretive bridges to East Asian philosophical structures such as 陰陽, 五行, 道, 理・気, 礼, and 天人相関. Those bridges are not silently identified with one Lean structure: historical-philosophical meaning and formal categorical meaning remain distinct authority layers.

---

## Three layers of KuuOS

### 1. Philosophical layer

KuuOS uses Madhyamaka, Yogācāra, Huayan, Tiantai, and East Asian relational thought as sources of questions about non-reification, context, relation, transformation, and whole/part dependence.

### 2. Mathematical layer

The mathematical program studies contextual systems using categories, bicategories, higher coherence, descent, obstruction, localization-style factorization, scaled simplicial methods, orthogonality, and universal properties.

### 3. AI / operational layer

The AI architecture turns the same discipline into bounded behavior:

```text
observe -> represent -> retrieve -> plan -> decide -> act -> re-observe -> verify
```

with explicit provenance and authority separation at every step.

These layers inform one another, but none is allowed to impersonate another. A Lean theorem is not automatically a historical-philosophical interpretation; a runtime success is not automatically a theorem; a philosophical analogy is not automatically a mathematical identity.

---

# Mathematical program

## Parent form of dependent origination

A basic categorical presentation is a context-indexed system such as

```text
D : Context ⥤ Type
```

with functorial transport, generalized at higher levels to coherent higher transport.

The guiding parent interpretation is:

```text
Dependent origination
= context-dependent state
+ admissible transport
+ compositional / higher coherence
+ descent and obstruction
+ invariance under justified change of presentation
+ non-reification of any one presentation.
```

Groupoids, gauge actions, process theories, quantum realizations, retrieval systems, memory systems, and scaled simplicial models are specializations or realizations, not replacements for the parent notion.

---

## The universality target

The north-star construction is schematically

```text
DO(C, W, J, H)
```

where:

```text
C = context / higher-context carrier
W = presentation changes intended to become equivalences
J = descent / gluing data
H = higher-coherence data
```

with a canonical map

```text
η : C ⟶ DO(C, W, J, H)
```

and a representation theorem of the form

```text
AdmissibleContextualSystems(C, X)
  ≃
Fun(DO(C, W, J, H), X)
```

with the correct variance, factorization, essential uniqueness, coherence, and naturality.

**This final universal object and theorem are not yet proved.** No localization, stackification, quotient, fibrant replacement, or higher-categorical completion is called “the universal dependent-origination object” until the mapping property is established.

---

# Integrated higher dependent-origination formalization

The current canonical spine has advanced beyond the older “candidate universality” description. The important layers are now:

```text
v2.0   ordinary localization universal-property layer
v2.1–v2.7   W + J dependent-origination sector
v2.8   Cat-valued stack descent
v2.9   bicategorical higher stack sector
v2.10  higher-localization interface
v2.11–v2.17 strict / weak-to-strict / saturation analysis
v2.18  weak higher-localization universal property
v2.19  coherent weak higher-localization universal property
v2.20–v2.30 coherence, modification-triangle, correction,
             rigidity, extension, and arrow-equation layers
v2.31  three-stage gap decomposition
v2.32  coherent-data collapse of Stage I/II gap
v2.33  route-completeness interface
v2.34–v2.36 fixed-carrier internal-gap normalization
v2.37  split-carrier Stage III transfer
v2.38  unit-isomorphism adjunction / adjoint-equivalence route
v2.39  completed-carrier two-sided upgrade
v2.40  coherent-forward-factor sufficient route
v2.41  split <-> coherent forward <-> modification triangle exactness
v2.42  weak/coherent two-axis obstruction normal form
```

### Important boundary

The v2.0 localization is an ordinary categorical localization result. It is **not** silently reused as the final higher localization theorem.

The higher program keeps separate:

```text
W-arrow becomes an actual isomorphism in ordinary localization
```

and

```text
W-arrow is represented by the appropriate higher equivalence/coherence data.
```

---

## v2.31–v2.42: what has actually been proved

### Three-stage weak-universality gap

For a raw higher contextual system `R`, v2.31 decomposes weak universality into:

```text
Stage I   some higher localization factorization exists
Stage II  one chosen factorization receives weak factors from every competitor
Stage III essential uniqueness of those factors
```

No stage is silently assumed.

### Coherent data collapses Stage I and Stage II

Once an explicit coherent weak universal datum `U` is supplied, v2.32 shows that the remaining local weak-universality gap is Stage III.

### Fixed-carrier reflection was isolated and then normalized

v2.34–v2.36 reduce coherent route completeness to transfer of Stage III uniqueness to the fixed coherent carrier `U.chosen`.

v2.37 identifies a concrete sufficient mechanism: a one-sided split carrier comparison

```text
p : U.chosen -> C.chosen
q : C.chosen -> U.chosen
p ≫ q ≅ id_U
```

transfers Stage III uniqueness from completed carrier `C` to the fixed carrier.

v2.38 shows that a bicategorical adjunction with invertible unit, and in particular suitable adjoint-equivalence data, produces that split.

v2.39 proves that on a Stage III-completed carrier, the other side

```text
q ≫ p ≅ id_C
```

is generated by Stage III essential uniqueness, so one-sided split data upgrades to two-sided equivalence data.

### v2.40–v2.41 close the internal fixed-route gap

v2.40 proves that a single **coherent forward factor**

```text
U.chosen -> C.chosen
```

is enough to produce the fixed split, because the backward coherent factor is already supplied by `U.factor`.

v2.22 identifies coherent liftability with existence of an invertible modification triangle on the same underlying weak factor.

v2.41 proves the converse on completed carriers. Therefore:

```text
Stage III-completed C:

split comparison
    <->
coherent forward factor
    <->
weak forward factor + invertible modification triangle
```

and globally for one coherent datum:

```text
coherent route completeness
    <->
all completed carriers admit a split
    <->
all completed carriers admit a coherent forward factor
    <->
all completed carriers admit a forward modification triangle.
```

So the internal fixed-carrier reflection problem is no longer an unnamed gap: its exact two-cell obstruction is explicit.

---

## v2.42: the current exact local state space

For one coherent datum `U`, v2.42 proves that there are three logical states.

### E — existence obstruction

```text
HigherWeakEssentialUniquenessObstruction
```

means no Stage III-completed weak carrier exists.

Consequences:

```text
no v2.18 weak universal property exists
route completeness is vacuously true
```

because route completeness is an implication whose premise is weak-universal existence.

### R — fixed-route obstruction

```text
HigherFixedChosenForwardModificationTriangleObstruction
```

means a Stage III-completed carrier **does** exist, but every forward weak factor from `U.chosen` to that carrier fails the modification-triangle test.

Consequences:

```text
a v2.18 weak universal property exists
coherent route completeness fails
```

### A — alignment

```text
HigherWeakCoherentAlignment
```

means:

```text
weak universality exists
AND
fixed coherent route completeness holds.
```

The E and R states are mutually exclusive for one fixed `R,U`.

The exact local normal form is:

```text
alignment
  <-> no E and no R

not alignment
  <-> E or R
```

Relative to the still-explicit global coherent universal principle, v2.42 also proves:

```text
HigherWeakLocalizationUniversalPrinciple
AND
HigherCoherentRouteCompletenessPrinciple

<->

no HigherGlobalWeakStageIIIExistenceObstruction
AND
no HigherGlobalFixedRouteObstruction.
```

The two obstruction classes may coexist globally on different raw systems even though they are disjoint for one fixed coherent datum.

---

# What remains open

The formal spine now distinguishes several genuinely different open problems.

## 1. Coherent higher-localization existence

Still open in general:

```text
IsHigherWAdmissible W R
  ->
HasCoherentWeakHigherLocalizationUniversalProperty W R
```

The repository does not assert a global coherent universal principle unconditionally.

## 2. Weak higher-localization existence / Stage III completion

Still open in general:

```text
IsHigherWAdmissible W R
  ->
HasWeakHigherLocalizationUniversalProperty W R
```

Under coherent existence, v2.42 says the remaining existential failure is exactly Axis E.

## 3. Global fixed-route completeness

Still open in general:

```text
HigherCoherentRouteCompletenessPrinciple
```

v2.41–v2.42 identify its failure exactly with the global fixed-route modification-triangle obstruction.

## 4. General factor-coherence / correction solvability

The global principles behind arbitrary coherent lifting, modification triangles, and stored correction equations remain open. Existing results give exact normal forms and implications; they do not silently solve the equations for all factors.

## 5. General strictification and saturation

The weak-to-strict and strict-sector layers provide conditional reductions, but the general higher strictification principle and full weak-admissible saturation theorem remain open.

## 6. The final universal dependent-origination object

`DO(C,W,J,H)` and its final representation theorem remain research targets.

---

# Other integrated formal foundations

The universality program is built on, rather than replacing, earlier formal work.

## Contextual transport and higher coherence

The repository contains contextual transport, refinement, semantic descent, directed/filtered cofinal invariance, two-cell refinement coherence, bicategorical coherence, operadic/multicategorical extensions, process/causal structures, and category-of-elements realizations.

## Higher realization

The higher-categorical line includes 2-Yoneda interfaces, mapping quasicategories, global scaled Duskin nerves, scaled-horn coherence, presentation-independent kernels, and transport across bicategorical model equivalence.

## Canonical scaled weak factorization structure

For the canonical scaled attachment family `T` on `ScaledSSet`, the integrated construction includes the native weak factorization system generated by the explicit small-object route.

## Generated-presentation semantics

Presentations are not identified merely because one observable semantic slice agrees. The integrated lattice/orthogonality line distinguishes full generated presentations from terminal/fibrant-object semantics and exhibits information loss under terminal restriction.

## Fundamental-groupoid descent

The descent line packages quotient-kernel compatibility, explicit descent obstruction, and natural-isomorphism invariance. Ordinary `FundamentalGroupoid` remains the endpoint-fixed homotopy quotient / flat-like branch; arbitrary curvature-sensitive connection transport requires richer path geometry.

---

# Validation-only Lean 4.31 line

PR #1558 remains a **validation-only stacked Draft PR**.

```text
PR #1558
Draft = true
merge = forbidden
Ready-for-review = forbidden
auto-merge = forbidden
CI = compatibility evidence only
```

It must not be confused with canonical theorem advancement. Successful compatibility reconstruction may justify a later theorem-preserving port onto a clean canonical branch; PR #1558 itself is not the authority vehicle.

---

# AI realization: why this matters

KuuOS treats AI representation changes as mathematical and operational events rather than invisible implementation details.

A future agent may move among contexts such as:

```text
observation
retrieval
memory
WORLD model
tool state
goal
plan
decision
action
other agents
other foundation models
```

This leads to concrete research questions:

```text
prompt/model/index migration -> presentation transport problem
cross-model migration -> invariant-preserving transport problem
partial memory integration -> descent problem
contradictory memory/evidence -> obstruction problem
multi-agent coordination -> higher-coherence problem
local plausibility without global support -> descent-failure candidate
interoperability -> relational invariance rather than shared latent coordinates
```

The aim is not to claim that current LLMs already satisfy the final KuuOS axioms. The aim is to build an architecture in which representation change, provenance, inconsistency, and authority are first-class objects rather than hidden side effects.

---

## Adaptive Retrieval

KuuOS includes a bounded least-sufficient retrieval policy:

```text
R0 lexical
R1 lexical + bounded rewrite
R2 semantic on demand
R3 hybrid
R4 pre-embedded semantic
R5 bounded relational / GraphRAG
```

Formal policy:

```text
selected mode = least complex mode explicitly assessed as adequate
```

If adequacy is unknown, the runtime fails closed. If all modes are explicitly inadequate, the correct result is `NO_DATA` plus a next-observation target.

Authority boundaries remain:

```text
retrieval score != entailment
embedding similarity != semantic proof
GraphRAG != global ontology
retrieved evidence != verified evidence
selection != execution
```

Main surfaces:

```text
docs/KUUOS_ADAPTIVE_RETRIEVAL_POLICY_v0_1.md
docs/AdaptiveRetrieval/README.md
runtime/kuuos_adaptive_retrieval_policy_v0_1.py
formal/KUOS/Retrieval/AdaptiveRetrievalPolicyV0_1.lean
```

---

## Runtime and control plane

Canonical effect-free repository check:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

The runtime architecture includes bounded observation/verification, PlanOS, DecisionOS, MemoryOS, CodeAI, GitHub MCP durable reentry, OpenClaw integration, dependent-origination adapters, and Adaptive Retrieval.

OpenClaw remains bounded:

```text
OpenClaw = execution host + observation source
OpenClaw != truth authority
OpenClaw != WORLD commit authority
OpenClaw != automatic PlanOS completion
OpenClaw != automatic rollback proof
OpenClaw != automatic memory overwrite authority
```

The same pattern applies to every external host and model.

---

# Repository development invariants

Formal development uses exact-base branches and PR-based review.

```text
no sorry
no admit
no new axiom as theorem authority
no placeholder proof authority
no silent assumption weakening
no silent identification of unrelated carriers
no ordinary-localization substitute for higher localization
```

For exact-head CI:

```text
queued / in_progress != success
head change invalidates old CI authority
exact-head CI running => write freeze
Ready only after exact-head green
normal merge uses exact expected head SHA
post-merge authority requires fresh main + parent check + identical compare
```

---

# Fixed authority boundaries

```text
candidate != authority
validation != truth
formal compilation != external theorem acceptance
CI success != theorem meaning beyond the compiled statement

contextual transport != substance ontology
mathematical dependent origination != unique historical-philosophical interpretation
semantic descent != state descent
reversible specialization != parent dependent origination
quantum realization != parent dependent origination

same fibrant-object semantics != equal generated presentation
semantic quotient != localization until a universal property is proved
universal-carrier language != universal theorem until mapping property is proved

retrieval score != entailment
runtime receipt != WORLD truth
host success != WORLD truth
model confidence != execution authority
model output != canonical repository authority

ordinary fundamental-groupoid transport != arbitrary curvature-sensitive transport
KuuOS structural theorem != physical Yang-Mills theorem authority
```

---

# Integrated subsystem map

Subsystem versions are independent; they are not one linear maturity scale.

| Series | Integrated state | Main entry |
|---|---|---|
| Repository lineage | self-organization v0.113 | `runtime/kuuos_current_root_sequence_v0_113.py` |
| ObserveOS | v0.7 + bounded external observation | `docs/ObserveOS/README.md` |
| VerifyOS | v0.15 | `docs/VerifyOS/README.md` |
| Qi architecture | Yin-Yang Wuxing Fibonacci History Geometry v2.5 | `docs/KUUOS_QI_YINYANG_WUXING_FIBONACCI_HISTORY_GEOMETRY_v2_5.md` |
| PlanOS | v1.23 | `formal/KuuOSPlanOSV1_23.lean` |
| DecisionOS | v0.6 | `formal/KuuOSDecisionOSV0_6.lean` |
| MemoryOS | v1.00 | `formal/KuuOSMemoryOSV1_00.lean` |
| Adaptive Retrieval | least-sufficient bounded selector v0.1 | `docs/AdaptiveRetrieval/README.md` |
| CodeAI | bounded prediction/execution contract | `docs/CodeAI/README.md` |
| Higher dependent origination | v2.42 two-axis obstruction normal form | `formal/KUOS/DependentOriginationWeakCoherentTwoAxisObstructionV2_42.lean` |
| Fundamental-groupoid descent | obstruction + natural-iso invariance | `formal/KUOS/` |
| OpenClaw control plane | bounded execution/observation host | `integrations/openclaw/` |
| Lean 4.31 validation | validation-only Draft PR #1558 | non-canonical compatibility evidence |
| Repository strict Lean baseline | aggregate import | `formal/KuuOSFormal.lean` |

---

# Current frontier

The immediate formal program is now sharper than before v2.42:

1. **Coherent existence:** determine conditions under which higher admissibility produces a coherent weak universal datum.
2. **Axis E elimination:** prove or characterize existence of a Stage III-completed weak carrier.
3. **Axis R elimination:** solve or structurally eliminate the fixed-route forward-modification-triangle obstruction.
4. **Weak universality:** combine the existence and route results without hiding either axis.
5. **Minimal axiom extraction:** determine which assumptions are truly needed for contextual transport, coherence, descent, obstruction, and universality.
6. **Universal carrier:** construct `DO(C,W,J,H)` at the correct categorical level.
7. **Representation theorem:** prove factorization, essential uniqueness, naturality, and uniqueness of the universal carrier up to the appropriate equivalence.
8. **AI realization theorems:** derive nontrivial memory/retrieval/model-migration/agent invariants from the parent mathematics rather than only describing them metaphorically.

See `ROADMAP.md` for theorem-sized milestones and exit criteria.

---

## Research status

KuuOS is a research architecture. Its formal mathematics, philosophical interpretation, runtime governance, physical specializations, and AI applications have different authority boundaries.

The strongest long-term claim remains open:

> **Dependent origination may admit a universal mathematical characterization under explicit contextual, coherence, and descent hypotheses.**

The repository has now advanced far enough to state the remaining weak/coherent higher-localization gap as explicit obstruction classes rather than an unnamed promise. The next phase is therefore to eliminate or classify those obstructions and only then promote the resulting structure toward the final universality theorem.