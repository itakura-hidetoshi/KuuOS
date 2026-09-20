# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, and bounded AI operation.

Its central question is:

> **Which structure survives justified changes of context and presentation, how can local information be transported and glued coherently, what obstructs that gluing, and which universal property characterizes the invariant content?**

KuuOS connects philosophy, mathematics, formal proof, and AI systems engineering while keeping their authority layers distinct.

---

## Authority snapshot — 2026-09-20 JST

### Canonical repository state

```text
canonical branch:
  main

main observed before this docs-only refresh:
  c9df819bfecad44888ce5d260055152da4ace9c3

latest theorem layer integrated into main:
  v2.68

v2.68 merge:
  PR #1650
  merge commit d9a4b4e070382f35b342f7505b09d35481f7e0c6

exact validated v2.68 proof head:
  5addad2ba75e526ba0595b37b972a3b3fb2972bb

exact-head governance:
  KuuOS PR Governance Gate #1887
  completed / success
```

The current `main` pointer is newer than the v2.68 theorem merge because infrastructure and governance changes were merged afterward. The integrated theorem baseline remains v2.68 until a later theorem PR is normally merged.

### Active theorem frontier

The active higher dependent-origination theorem frontier is PR **#1651**:

```text
PR:
  #1651
  Truth-test weak admissibility with octahedral generated holonomy v2.69

branch:
  formal/dependent-origination-generated-holonomy-countermodel-v269

current exact theorem head:
  2ef1a04733eab445848381bffe72eccff5d5f2b3

v2.95 checkpoint compare against the pre-docs main above:
  behind = 0
  ahead  = 514

current theorem layer:
  v2.95

exact-head governance:
  KuuOS PR Governance Gate #2425
  completed / success
```

PR #1651 remains **Draft / open / unmerged**. Therefore v2.69–v2.95 are validated theorem artifacts on the Draft branch, not yet canonical merged theorem authority on `main`.

Pinned formal environment:

```text
Lean:    leanprover/lean4:v4.30.0-rc2
Mathlib: 5450b53e5ddc75d46418fabb605edbf36bd0beb6
```

Strict aggregate validation uses:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

Repository authority is not inferred from model memory, prose summaries, queued CI, validation-only branches, runtime receipts, retrieval scores, or philosophical analogy.

---

# What 空 means in KuuOS

KuuOS does **not** formalize 空 as the slogan “nothing exists.” Its operational role is anti-reification:

```text
chosen presentation != intrinsic substance
local observation    != global truth
retrieval score      != entailment
runtime success      != WORLD truth
formal encoding      != unique philosophical interpretation
model generation     != theorem authority
```

The bridge from 空 to 縁起 is not erasure of structure. It is refusal to absolutize one representation while retaining the relations and coherence required to transport between representations:

```text
context-indexed state
+ admissible transport
+ compositional / higher coherence
+ descent and gluing
+ obstruction
+ presentation invariance
+ provenance and authority boundaries
```

KuuOS keeps interpretive bridges to Madhyamaka, Yogācāra, Huayan, Tiantai, 陰陽, 五行, 道, 理・気, 礼, and 天人相関. These are not silently identified with one mathematical formalism.

---

# Three layers

## 1. Philosophical layer

The philosophical layer studies relation, dependence, context, transformation, compatibility, and non-reification without collapsing one presentation into intrinsic substance.

## 2. Mathematical layer

The mathematical layer studies contextual systems using categories, bicategories, pseudofunctors, localization-style factorization, higher coherence, descent, gauge freedom, holonomy, obstruction, semantic quotients, and universal properties.

## 3. AI / operational layer

The operational layer applies the same discipline to bounded systems:

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

with provenance and authority separation throughout.

---

# Dependent Origination Universality Program

The north-star construction is schematically:

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

with a canonical map:

```text
η : C ⟶ DO(C, W, J, H)
```

and a target mapping property of the form:

```text
AdmissibleContextualSystems(C, X)
  ≃
Fun(DO(C, W, J, H), X)
```

with the correct higher-categorical variance, factorization, essential uniqueness, coherence, naturality, and descent compatibility.

**The final universal object and representation theorem are not yet proved.**

No localization, quotient, completion, stackification, or semantic reduction is called the universal dependent-origination object until the required mapping property is formally established.

---

# Integrated formal spine through v2.68

The theorem line integrated into `main` currently reaches v2.68.

```text
v2.0       ordinary localization universal-property layer
v2.1–2.7   W + J dependent-origination sector
v2.8       Cat-valued stack descent
v2.9       bicategorical higher stack sector
v2.10      HigherLocalizationFactorization interface
v2.11–17   strict / weak-to-strict / saturation analysis
v2.18–19   weak and coherent weak higher-localization universality
v2.20–30   modification triangles, correction, rigidity, extension,
            and arrow-equation coherence
v2.31–41   weak-universality gaps, normalization, split/adjunction routes
v2.42      E/R/A two-axis obstruction normal form
v2.43–54   structural sufficient routes eliminating local E/R obstructions
v2.55      restricted Track A1 existence when W is already base-isomorphic
v2.56      pointwise W adjoint-equivalence data
v2.57      free localization-path evaluator
v2.58      local Iso existence for quotient-equal paths
v2.59–60   exact five-law quotient/comparison coherence package
v2.61      simultaneous pointwise local choices
v2.62–64   thinness / automorphism-thin sufficient sectors
v2.65      five automorphism-valued coherence defects
v2.66      gauge-orbit normal form
v2.67      retained relation 2-cells and relation-loop holonomy
v2.68      fully generated localization 2-cells and generated holonomy
```

The principal integrated v2.68 theorem is:

```text
GeneratedHolonomyTrivial W R D
  ->
HasHigherLocalizationFactorization (W := W) R
```

and, in admissibility-shaped form:

```text
IsHigherWAdmissible W R
+ GeneratedHolonomyTrivial W R D_adm
  ->
HasHigherLocalizationFactorization (W := W) R
```

v2.68 deliberately did **not** assume that weak admissibility itself forces generated holonomy to vanish.

---

# Draft frontier v2.69–v2.95

PR #1651 performs that truth test and then develops a correction / obstruction semantics around the resulting nontrivial holonomy.

## v2.69 — octahedral countermodel

v2.69 constructs a six-object octahedral `S^0 * S^0 * S^0` contextual system with a one-object `C2 = Multiplicative (ZMod 2)` target groupoid and a single nontrivial central compositor.

It proves that weak all-morphism admissibility does **not** force the global generated-holonomy condition used by v2.68.

Important boundary:

```text
weak admissibility
  -/-> GeneratedHolonomyTrivial
```

This does **not** prove:

```text
weak admissibility
  -/-> HigherLocalizationFactorization
```

Generated-holonomy triviality is a proved sufficient condition for factorization; its necessity is not established.

## v2.70–v2.81 — filtered correction and realizability

```text
v2.70  filtered obstruction core
v2.71  finite correction gain
v2.72  flat completion boundary
v2.73  filtered generated holonomy
v2.74  explicit correction realization
v2.75  ordered sector correction
v2.76  bounded-loss filtration algebra
v2.77  cofinal correction schedules
v2.78  tower realization + residual stability
v2.79  relative corrective descent
v2.80  generated-holonomy correctability classification
v2.81  concrete octahedral correctability bridge
```

The key conceptual separation is:

```text
nontrivial / non-flat holonomy
!=
hard obstruction
```

A defect may remain non-flat while still lying in the image of an admissible correction mechanism.

## v2.82–v2.90 — correction authority and extensional power

```text
v2.82  explicit non-flat yet correctable separation
v2.83  correction-authority refinement
v2.84  restricted correction authority gap
v2.85  reflexive-only concrete authority gap
v2.86  heterogeneous authority morphisms
v2.87  correction-image equivalence
v2.88  extensional correction-power preorder / equality
v2.89  presentation-free reachability profile
v2.90  strict correction-power inequality
```

The authority lesson is formal:

```text
hard obstruction is relative to licensed correction power
```

Widening authority preserves correctability and can remove a hard obstruction. Equal reachable correction images yield the same correctability / hard-obstruction classification even when parameter presentations differ.

## v2.91–v2.95 — semantic completion

```text
v2.91  canonical functional realization of any reachability profile
v2.92  semantic reflection of correction power into explicit authority transport
v2.93  finite join / meet lattice of correction power
v2.94  arbitrary-family suprema / infima
v2.95  bottom / top / complement and the constructive-classical Boolean boundary
```

v2.95 makes the logic boundary explicit.

Constructive results include:

```text
bottom
top
complement reachability
complement antitonicity
C ∧ complement(C) = bottom
```

Classical excluded middle is used for:

```text
C ∨ complement(C) = top
double complement = C
```

This keeps Boolean behavior from being silently assumed inside the constructive correction-power lattice.

---

# Current mathematical picture

The current theorem-backed picture is:

```text
weak W-admissibility
        |
        v
pointwise adjoint equivalences
        |
        v
generated localization 2-cell semantics
        |
        v
generated holonomy
        |
        +-------------------------------+
        |                               |
        | trivial                       | nontrivial
        v                               v
v2.68 sufficient route            v2.69 countermodel
to factorization                        |
                                        v
                              filtered / corrective semantics
                                        |
                                        v
                              authority-relative obstruction
                                        |
                                        v
                              correction-power preorder
                                        |
                                        v
                              reachability semantics
                                        |
                                        v
                              complete lattice / complement
                                  [Draft through v2.95]
```

The remaining Stage-I question is no longer whether weak admissibility forces holonomy triviality; v2.69 answers that negatively.

The open question is instead:

> **What exact additional structure, correction principle, or higher carrier is necessary and sufficient for factorization when generated holonomy is nontrivial?**

---

# What remains open

## A1. General higher-localization factorization

Still open:

```text
IsHigherWAdmissible W R
  ->
HasHigherLocalizationFactorization W R
```

The route through universal generated-holonomy triviality is no longer available in general because of v2.69.

The next task is to decide whether:

```text
nontrivial generated holonomy
+ suitable correction/descent structure
  ->
factorization
```

or whether the correct general carrier must retain additional bicategorical / untruncated information.

## A2. Coherent Stage-II universality

Still open:

```text
IsHigherWAdmissible W R
  ->
HasCoherentWeakHigherLocalizationUniversalProperty W R
```

Factorization is Stage I; it is not the final universal property.

## Axis E / Axis R

The v2.42 E/R/A decomposition and v2.43–54 sufficient elimination results remain active after Stage-I existence is settled.

## Final dependent-origination universal object

`DO(C,W,J,H)` and its representation theorem remain research targets.

See [ROADMAP.md](ROADMAP.md) for theorem-sized milestones.

---

# Why this matters for AI

KuuOS treats representation change as an explicit event rather than an invisible implementation detail.

```text
model / prompt / index migration
  -> presentation transport

cross-model continuity
  -> invariant-preserving transport

partial memory integration
  -> descent / gluing

contradictory evidence
  -> obstruction

multi-agent coordination
  -> higher coherence

multiple valid transformation histories
  -> path dependence / holonomy

different remediation permissions
  -> authority-relative correction power
```

The v2.83–v2.95 correction-power line is especially relevant operationally: whether an observed discrepancy is “hard” depends on which interventions are actually authorized, and equivalent intervention capabilities should be compared by reachable effects rather than by implementation-specific parameter names.

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

If adequacy is unknown, the runtime fails closed. If all modes are explicitly inadequate, the appropriate result is `NO_DATA` plus a next-observation target.

Authority boundaries remain:

```text
retrieval score      != entailment
embedding similarity != semantic proof
GraphRAG              != global ontology
retrieved evidence    != verified evidence
selection             != execution
```

---

# Runtime and control plane

Canonical effect-free repository check:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

The runtime architecture includes bounded observation / verification, PlanOS, DecisionOS, MemoryOS, CodeAI, GitHub MCP durable reentry, dependent-origination adapters, and Adaptive Retrieval.

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

PR **#1558** remains separate from canonical theorem advancement.

```text
PR #1558 = validation-only
Draft = true
merge = forbidden
Ready-for-review = forbidden
auto-merge = forbidden
CI = compatibility evidence only
```

Any useful proof engineering from that line must be ported theorem-preservingly to an authorized theorem branch.

---

# Repository development invariants

```text
no sorry
no admit
no new axiom as theorem authority
no placeholder proof authority
no silent assumption weakening
no silent identification of unrelated carriers
no Classical.choice => coherence inference
no validation result promoted beyond its exact head
```

Exact-SHA discipline:

```text
queued / in_progress != success
head change invalidates old CI authority
exact-head CI is authoritative only for that head
normal merge requires fresh gate
post-merge authority requires fresh main verification
```

---

# Fixed authority boundaries

```text
candidate != authority
formal compilation != philosophical uniqueness
runtime receipt != WORLD truth
model output != canonical repository authority

same quotient arrow != same retained 2-dimensional derivation
local Nonempty Iso != coherent descent
pointwise inverse choice != pseudofunctor coherence
gauge equivalence != zero obstruction
non-flat != hard obstruction
hard obstruction != authority-independent property
equal parameter syntax != equal correction power
different parameter syntax != different correction power

semantic quotient != localization until a universal property is proved
universal-carrier language != universal theorem until mapping property is proved
```

---

# Current research sentence

As of the validated v2.95 Draft frontier, KuuOS has moved past the question “does weak admissibility force generated holonomy to vanish?” The answer is **no**.

The current question is:

> **How should nontrivial generated holonomy be transported, corrected, or retained so that the exact boundary between correctable defect, hard obstruction, and genuine failure of higher-localization factorization becomes necessary-and-sufficient rather than merely sufficient?**
