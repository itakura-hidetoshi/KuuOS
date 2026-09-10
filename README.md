# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for **dependent origination (縁起)**, formally verified contextual systems, and bounded AI operation.

Its central question is:

> **Which structure survives justified changes of context and presentation, how can local information be transported and glued coherently, what obstructs that gluing, and which universal property characterizes the invariant content?**

KuuOS treats this as one connected program spanning philosophy, mathematics, formal proof, and AI systems engineering while keeping their authority layers distinct.

---

## Current theorem-bearing baseline

**Documentation state: 2026-09-10 JST**

The latest theorem-bearing canonical merge represented by this document is:

```text
authoritative theorem branch: main
latest theorem-bearing merge: PR #1635
latest theorem layer: v2.55
last theorem-bearing canonical SHA:
  ef03967b028e531be997941ca8205969391dce35
exact validated v2.55 proof head:
  93b210c11aefea70ece7fadd37b212d0ed604e18
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

A later documentation-only commit may advance the `main` SHA without changing this theorem baseline. The theorem authority is always the integrated canonical repository state together with the exact theorem-bearing provenance, not a model answer, memory, runtime receipt, validation-only branch, or old documentation snapshot.

---

# What 空 means in KuuOS

KuuOS does **not** formalize 空 as the slogan “nothing exists.” Its operational use is an anti-reification discipline:

```text
no chosen presentation = intrinsic substance by default
no local observation   = global truth by default
no retrieval score     = entailment by default
no runtime success     = WORLD truth by default
no formal encoding     = philosophical uniqueness by default
no model generation    = theorem authority by default
```

The bridge from 空 to 縁起 is therefore not erasure of structure but refusal to absolutize one presentation:

```text
context-indexed state
+ admissible transport
+ compositional / higher coherence
+ descent and gluing
+ obstruction
+ presentation invariance
+ provenance and authority boundaries
```

In KuuOS, **縁起 is not reduced to a graph metaphor or a single causal chain**. It is treated as relational and contextual dependence together with transport, history, compatibility, higher coherence, descent, and the possibility of genuine obstruction.

KuuOS also maintains interpretive bridges to Madhyamaka, Yogācāra, Huayan, Tiantai, and East Asian structures such as 陰陽, 五行, 道, 理・気, 礼, and 天人相関. These are not silently identified with one Lean definition. Historical-philosophical interpretation, mathematical structure, and AI implementation remain distinct layers.

---

# Three layers of KuuOS

## 1. Philosophical layer

The philosophical layer asks how to reason without reifying a local representation into an intrinsic substance. It emphasizes relation, context, transformation, dependence, compatibility, and the limits of any one viewpoint.

## 2. Mathematical layer

The mathematical layer studies contextual systems using categories, bicategories, higher coherence, localization-style factorization, descent, obstruction, orthogonality, scaled simplicial methods, and universal properties.

## 3. AI / operational layer

The AI layer turns the same discipline into bounded behavior:

```text
observe
  -> represent
  -> retrieve
  -> plan
  -> decide
  -> act
  -> re-observe
  -> verify
```

with provenance and authority separation at every step.

The layers inform one another but none impersonates another:

```text
philosophical analogy != mathematical identity
Lean theorem           != unique historical interpretation
runtime success        != theorem
model confidence       != execution authority
retrieved evidence     != verified evidence
```

---

# Dependent Origination Universality Program

A parent categorical presentation is a context-indexed system such as

```text
D : Context ⥤ Type
```

or, at the higher level, a Cat-valued pseudofunctor with coherent transport.

The guiding parent interpretation is:

```text
Dependent origination
= context-dependent state
+ admissible transport
+ higher coherence
+ descent and obstruction
+ invariance under justified presentation change
+ non-reification of any one presentation.
```

The north-star construction is schematically:

```text
DO(C, W, J, H)
```

where

```text
C = context / higher-context carrier
W = presentation changes intended to become equivalences
J = descent / gluing data
H = required higher-coherence data
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

**The final universal object and representation theorem are not yet proved.** No localization, stackification, quotient, fibrant replacement, or higher completion is called the universal dependent-origination object until its mapping property is established.

---

# Current formal spine

The integrated higher dependent-origination line now reaches **v2.55**.

```text
v2.0       ordinary localization universal-property layer
v2.1–2.7   W + J dependent-origination sector
v2.8       Cat-valued stack descent
v2.9       bicategorical higher stack sector
v2.10      higher-localization factorization interface
v2.11–17   strict / weak-to-strict / saturation analysis
v2.18      weak higher-localization universal property
v2.19      coherent weak higher-localization universal property
v2.20–30   modification triangles, correction, rigidity,
            extension, and arrow-equation coherence
v2.31      three-stage weak-universality gap
v2.32–36   coherent-data and fixed-carrier normalization
v2.37–41   split / adjunction / coherent-forward exactness
v2.42      E/R/A two-axis obstruction normal form
v2.43–54   structural sufficient routes eliminating local E/R
v2.55      restricted Track A1 factorization-existence theorem
```

The crucial distinction is that **v2.43–54 and v2.55 solve different kinds of problems**.

---

# v2.42 — exact weak/coherent obstruction normal form

For one coherent datum `U`, v2.42 isolates three states.

```text
E — HigherWeakEssentialUniquenessObstruction
    no Stage III-completed weak carrier exists

R — HigherFixedChosenForwardModificationTriangleObstruction
    a completed weak carrier exists, but the fixed coherent
    forward route fails

A — HigherWeakCoherentAlignment
    weak universality exists and the fixed coherent route is complete
```

Locally:

```text
alignment     <-> no E and no R
not alignment <-> E or R
```

The E and R states are mutually exclusive for one fixed coherent datum. Global witnesses may occur on different raw systems.

This did **not** prove a general coherent existence principle; it made the remaining failure modes explicit.

---

# v2.43–v2.54 — structural obstruction elimination

Once coherent universal data are already available, the repository now contains several theorem-backed sufficient mechanisms for eliminating the local E/R obstruction.

## Base-side rigidity

```text
v2.43  concrete Discrete I base
v2.44  arbitrary [CategoryTheory.IsDiscrete Context]
```

Base discreteness makes the stored naturality problem collapse to identity coherence.

## Target / local 2-cell rigidity

```text
v2.45  whole raw fiber thin
v2.46  exact stored Cat 2-cell hom is Subsingleton
v2.47  pointwise component homs are Subsingleton
v2.48  full image-envelope subcategory is thin
```

v2.47 is the key local criterion:

```text
(∀ Z, Subsingleton (F.obj Z ⟶ G.obj Z))
  ->
Subsingleton (F ⟶ G)
```

which converts componentwise uniqueness into uniqueness of the relevant Cat 2-cell.

## Cancellation and probe-family routes

```text
v2.49  common epi / mono cancellation detector
v2.50  global separating / coseparating family
v2.51  shared EffectiveEpiFamily probe family
```

These are independent sufficient routes into the v2.47 pointwise criterion; the repository does not assert unsupported equivalences among them.

## Standard Mathlib detector routes

```text
v2.52  single IsSeparator / IsCoseparator object
v2.53  IsDetector + equalizers, or IsCodetector + coequalizers
v2.54  detecting family + equalizers,
        or codetecting family + coequalizers
```

v2.54 is the family-level structural endpoint of this sequence. The equalizer/coequalizer hypotheses are retained rather than silently weakened.

### What v2.43–54 do not prove

They do not by themselves construct coherent universal data or solve general higher-localization existence. They are conditional **obstruction-elimination mechanisms**, not replacements for Track A existence.

---

# v2.55 — first restricted Track A1 existence sector

v2.55 returns to the more primitive factorization-existence problem.

Assume:

```text
W ≤ MorphismProperty.isomorphisms Context
```

Then the identity functor on `Context` is already a localization at `W`, so the canonical localization carrier is equivalent to `Context`. The proof transports an **arbitrary raw Cat-valued pseudofunctor** along that base equivalence, constructs the localized pseudofunctor directly, and builds the comparison from the canonical localization triangle.

The theorem is:

```text
W ≤ isomorphisms(Context)
  ->
HasHigherLocalizationFactorization W R
```

for arbitrary raw `R`.

This matters because it gives a genuine higher-localization factorization existence result **without assuming a strict presentation model** in this restricted sector.

But the boundary is equally important:

```text
NOT proved:
IsHigherWAdmissible W R
  ->
HasHigherLocalizationFactorization W R
```

for general `W`.

v2.55 does not replace an arbitrary equivalence-valued pseudofunctor by an ordinary functor, does not establish a general bicategorical localization theorem, and does not prove coherent weak universality or the final `DO(C,W,J,H)` theorem.

---

# What remains open

The present frontier is now sharper.

## A1. General higher-localization factorization existence

Open in general:

```text
IsHigherWAdmissible W R
  ->
HasHigherLocalizationFactorization W R
```

v2.55 solves only the sector where every `W`-arrow was already an isomorphism in the base.

The next useful step should move beyond that trivial-localization sector by making the **coherent inversion data for equivalence-valued `R.map f`** explicit, rather than hiding the problem in a global strictification principle.

## A2. Coherent universal-data existence

Still open:

```text
IsHigherWAdmissible W R
  ->
HasCoherentWeakHigherLocalizationUniversalProperty W R
```

Factorization alone is not yet Stage II coherent universality.

## Axis E — Stage III existence

The general existence of a Stage III-completed carrier remains open. v2.43–54 provide strong sufficient uniqueness mechanisms once their structural hypotheses and coherent datum are present, but do not prove those hypotheses universally.

## Axis R — fixed coherent route

General correction/modification-triangle solvability remains open. v2.37–42 give its exact normal form; v2.43–54 eliminate it under several structural rigidity conditions.

## General strictification and saturation

The strict-sector reductions remain conditional. The repository does not assume a global theorem turning every weakly admissible pseudofunctor into a strict ordinary presentation model.

## Final universal dependent-origination theorem

`DO(C,W,J,H)` and its representation theorem remain research targets.

See [`ROADMAP.md`](ROADMAP.md) for theorem-sized milestones and exit criteria.

---

# Why this matters for AI

KuuOS treats representation change as an explicit event rather than an invisible implementation detail.

The mathematical vocabulary motivates concrete AI engineering questions:

```text
model / prompt / index migration
  -> presentation transport problem

cross-model continuity
  -> invariant-preserving transport problem

partial memory integration
  -> descent / gluing problem

contradictory memory or evidence
  -> obstruction problem

multi-agent coordination
  -> higher-coherence problem

local plausibility without global support
  -> descent-failure candidate

interoperability
  -> relational invariance, not assumed shared latent coordinates
```

The aim is not to claim that present LLMs already satisfy the final KuuOS axioms. The aim is to build systems in which context, provenance, representation change, inconsistency, verification, and authority are first-class objects.

A model migration should therefore be treated schematically as

```text
old presentation
  -> invariant packet
  -> transport
  -> semantic validation
  -> stress validation
  -> canary
  -> promotion or rollback
```

rather than copying one model's prose or hidden state and calling that continuity.

---

# Adaptive Retrieval

KuuOS includes a bounded least-sufficient retrieval policy:

```text
R0 lexical
R1 lexical + bounded rewrite
R2 semantic on demand
R3 hybrid
R4 pre-embedded semantic
R5 bounded relational / GraphRAG
```

Policy:

```text
selected mode = least complex mode explicitly assessed as adequate
```

If adequacy is unknown, the runtime fails closed. If all modes are explicitly inadequate, the appropriate result is `NO_DATA` together with a next-observation target.

Authority boundaries:

```text
retrieval score     != entailment
embedding similarity != semantic proof
GraphRAG             != global ontology
retrieved evidence   != verified evidence
selection            != execution
```

Main surfaces:

```text
docs/KUUOS_ADAPTIVE_RETRIEVAL_POLICY_v0_1.md
docs/AdaptiveRetrieval/README.md
runtime/kuuos_adaptive_retrieval_policy_v0_1.py
formal/KUOS/Retrieval/AdaptiveRetrievalPolicyV0_1.lean
```

---

# Runtime and control plane

Canonical effect-free repository check:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

The runtime architecture includes bounded observation/verification, PlanOS, DecisionOS, MemoryOS, CodeAI, GitHub MCP durable reentry, OpenClaw integration, dependent-origination adapters, and Adaptive Retrieval.

External hosts remain bounded:

```text
execution host != truth authority
observation source != WORLD commit authority
host success != PlanOS completion
host success != rollback proof
host success != memory overwrite authority
```

---

# Validation-only Lean 4.31 line

PR **#1558** remains a validation-only stacked Draft PR.

```text
PR #1558
Draft = true
merge = forbidden
Ready-for-review = forbidden
auto-merge = forbidden
CI = compatibility evidence only
```

It must not be confused with canonical theorem advancement. Any proof engineering worth preserving must be ported theorem-preservingly onto a fresh canonical branch; PR #1558 itself is not the authority vehicle.

---

# Repository development invariants

Formal development uses exact-base branches and PR-based validation.

```text
no sorry
no admit
no new axiom as theorem authority
no placeholder proof authority
no silent assumption weakening
no silent identification of unrelated carriers
no ordinary-localization substitute for the general higher theorem
```

Exact-SHA discipline:

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
validation != theorem meaning beyond the compiled statement
formal compilation != external theorem acceptance

contextual transport != substance ontology
mathematical dependent origination != unique historical-philosophical interpretation
quantum realization != parent dependent origination

same fibrant-object semantics != equal generated presentation
semantic quotient != localization until a universal property is proved
universal-carrier language != universal theorem until mapping property is proved

retrieval score != entailment
runtime receipt != WORLD truth
model output != canonical repository authority
model confidence != execution authority

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
| Higher dependent origination | v2.55 restricted A1 existence; v2.42 E/R/A normal form; v2.43–54 structural eliminators | `formal/KUOS/DependentOriginationIsoClassHigherLocalizationExistenceV2_55.lean` |
| Fundamental-groupoid descent | obstruction + natural-iso invariance | `formal/KUOS/` |
| OpenClaw control plane | bounded execution/observation host | `integrations/openclaw/` |
| Lean 4.31 validation | validation-only Draft PR #1558 | non-canonical compatibility evidence |
| Repository strict Lean baseline | aggregate import | `formal/KuuOSFormal.lean` |

---

# Immediate frontier

The next phase should prioritize theorem-bearing progress that crosses the remaining logical boundaries rather than accumulating synonymous interfaces.

```text
1. Generalize Track A1 beyond W ≤ isomorphisms.
2. Isolate minimal coherent inversion data for equivalence-valued W-images.
3. Construct coherent Stage II universal data from explicit hypotheses.
4. Apply or derive structural hypotheses that eliminate Axis E and Axis R.
5. Extract a smaller theorem-backed dependent-origination axiom package.
6. Determine the categorical level forced by those axioms.
7. Construct DO(C,W,J,H).
8. Prove the representation theorem.
9. Derive nontrivial AI migration / memory / retrieval / multi-agent invariants
   from the parent mathematics.
```

---

## Research status

KuuOS is a research architecture. Its formal mathematics, philosophical interpretation, runtime governance, physical specializations, and AI applications have different authority boundaries.

The strongest long-term claim remains open:

> **Dependent origination may admit a universal mathematical characterization under explicit contextual, coherence, presentation-invariance, and descent hypotheses.**

The current formal advantage is that the gap is no longer a single vague promise. v2.42 identifies the weak/coherent obstruction axes, v2.43–54 provide concrete structural mechanisms that eliminate them, and v2.55 establishes the first restricted arbitrary-pseudofunctor factorization-existence sector without invoking a strict presentation model. The next task is to carry that existence mechanism beyond the isomorphism-only base sector while preserving higher-equivalence semantics.
