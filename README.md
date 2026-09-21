# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, and bounded AI operation.

Its central question is:

> **Which structure survives justified changes of context and presentation, how can local information be transported and glued coherently, what obstructs that gluing, and which universal property characterizes the invariant content?**

KuuOS connects philosophy, mathematics, formal proof, and AI systems engineering while keeping their authority layers distinct.

---

## Authority snapshot — 2026-09-21 JST

### Canonical repository state

```text
canonical branch:
  main

main observed before this docs-only refresh:
  2eed09b900a5e82390ae17ad2d46f4b283b184bd

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

The active higher dependent-origination / higher-localization theorem frontier is PR **#1651**:

```text
PR:
  #1651
  Truth-test weak admissibility with octahedral generated holonomy v2.69

branch:
  formal/dependent-origination-generated-holonomy-countermodel-v269

latest validated theorem-bearing head before this docs refresh:
  77337a3a5e65871a2426c9e8abfec6623be0b9ab

fresh compare against current main:
  behind = 0
  ahead  = 557

current validated theorem layer:
  v3.14

exact-head governance:
  KuuOS PR Governance Gate #2469
  completed / success

exact-head receipts:
  chatgpt-ci-receipt/KuuOS Strict Lean formal validation = success
  chatgpt-ci-receipt/KuuOS exact-head terminal = success
```

PR #1651 remains **Draft / open / unmerged**. Therefore v2.69–v3.14 are validated theorem artifacts on the Draft branch, not yet canonical merged theorem authority on `main`.

The authority boundary is important but the mathematics is continuous: v2.69 does not start an unrelated program. It truth-tests the v2.68 sufficient condition and then, from v2.96 onward, reconnects the correction analysis to the same `HigherLocalizationFactorization` problem.

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

# Integrated formal spine through v2.68, with Draft continuation through v3.14

The theorem line integrated into `main` currently reaches v2.68. The long-running Draft PR #1651 continues **the same Stage-I mathematical spine** from v2.69 through v3.14.

The authority layers differ:

```text
v2.0–v2.68
  = merged canonical theorem authority on main

v2.69–v3.14
  = exact-head validated Draft theorem authority on PR #1651
```

but there is no mathematical discontinuity at the boundary.

## Canonical integrated segment: v2.0–v2.68

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
v2.42      E/R/A obstruction normal form
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

v2.68 deliberately leaves open whether weak admissibility itself forces generated holonomy triviality.

## The bridge at v2.69: truth-test, not a new branch of mathematics

v2.69 answers that open question negatively with the octahedral countermodel:

```text
IsHigherWAdmissible W R
  -/->
GeneratedHolonomyTrivial W R D_adm
```

This does **not** refute factorization. It removes one sufficient route as a universal explanation:

```text
weak admissibility
  -/-> generated holonomy triviality

but still possibly

weak admissibility
  -> factorization
```

through a more general correction / gluing mechanism.

That is why the Draft frontier belongs directly after v2.68 in the same spine.

## Draft continuation I: v2.70–v2.95 — analyze what nontrivial holonomy means

v2.70–v2.95 develop filtered correction, realizability, authority-relative obstruction, extensional correction power, reachability semantics, lattice structure, and the constructive/classical Boolean boundary.

```text
v2.70–2.81
  filtered obstruction / correction realization / correctability

v2.82–2.87
  correction authority and authority morphisms

v2.88–2.92
  extensional correction power and reachability profiles

v2.93–2.95
  finite/arbitrary lattice operations, bottom/top/complement,
  constructive-classical boundary
```

This part is upstream obstruction analysis. It determines why

```text
∀ route state s, ∃ correction Q_s
```

cannot by itself provide the coherent shared witness required by higher localization.

## Draft continuation II: v2.96–v3.04 — return correction semantics to factorization

Beginning at v2.96, the Draft line explicitly returns to the original `HigherLocalizationFactorization` problem:

```text
v2.96  correction semantics -> factorization interface
v2.97  corrected generated-route equations
v2.98  five coherence routes are the relevant finite interface
v2.99  generated correction gauge normal form
v3.00  five corrections = one compatible gauge coboundary
v3.01  coboundary solvability <-> coherent general-W factorization data
v3.02  five equations split into:
          3 quotient equations
        + 2 comparison equations
v3.03  quotient stage depends only on gId / gComp, not gIso
v3.04  quotient solution + comparison lift
          -> genuine HigherLocalizationFactorization
```

So v2.70–v2.95 are not an abandoned side theory. They become the semantic upstream of the factorization obstruction that is made concrete from v2.96 onward.

## Draft continuation III: v3.05–v3.14 — localize the first factorization obstruction

The first-stage quotient obstruction is then progressively identified:

```text
v3.05
  quotient gauge coboundary solvability
  <-> coherent quotient transport

v3.06
  quotient defects viewed as a gauge-orbit intersection problem

v3.07
  only three quotient route families matter:
    associator / left unitor / right unitor

v3.08
  one compatible quotient correction must solve all three families

v3.09
  exact quantifier gap:
    ∀s ∃Q_s
      versus
    ∃Q ∀s

v3.10
  joint correction power records witness correlation

v3.11
  correction loci L_s:
    statewise correction  <-> each L_s nonempty
    joint correction      <-> total intersection nonempty

v3.12
  every L_s depends only on a finite gId/gComp coordinate footprint;
  global correction becomes finite-footprint amalgamation

v3.13
  global amalgamation -> pairwise overlap compatibility;
  shared gId/gComp coordinates become explicit necessary gluing equations

v3.14
  quotient gauge coordinates are normalized by dependent coordinate keys;
  pairwise common-extension compatibility implies equality on every literally
  shared footprint coordinate
```

The currently validated quotient-stage frontier is therefore:

```text
IsHigherWAdmissible W R
        |
        v
pointwise W-adjoint equivalence D
        |
        v
three quotient coherence route families
        |
        v
statewise correction loci L_s
        |
        v
finite coordinate footprints
        |
        v
shared-coordinate overlap compatibility
        |
        v
pairwise extension / global amalgamation problem   <- current frontier
        |
        v
one global quotient gauge Q
        |
        v
CoherentQuotientTransportData
        |
        v
comparison gIso lift
        |
        v
HasHigherLocalizationFactorization
```

Thus the integrated v2.68 theorem and the Draft v2.69–v3.14 line should be read as one connected argument:

```text
v2.68:
  trivial generated holonomy is sufficient

v2.69:
  weak admissibility does not force that sufficient condition

v2.70–v2.95:
  analyze correction and authority semantics

v2.96–v3.04:
  reconnect correction to exact factorization data

v3.05–v3.14:
  reduce the first unresolved factorization obstruction to
  finite dependent-coordinate gluing
```

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

As of the validated v3.14 Draft frontier, KuuOS has moved beyond the v2.69 truth-test and reconnected the correction program to the original higher-localization factorization problem.

The current first-stage question is now concrete:

> **Can statewise local correcting quotient gauges whose finite dependent coordinate footprints agree on overlaps be extended and globally amalgamated into one quotient gauge, and if not, what exact higher-order gluing obstruction remains?**
