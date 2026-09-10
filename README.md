# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for **dependent origination (縁起)**, formally verified contextual systems, higher-coherence / obstruction theory, and bounded AI operation.

Its central question is:

> **Which structure survives justified changes of context and presentation, how can local information be transported and glued coherently, what obstructs that gluing, and which universal property characterizes the invariant content?**

KuuOS treats philosophy, mathematics, formal proof, and AI systems engineering as connected but **not interchangeable authority layers**.

---

## Current theorem-bearing baseline

**Documentation state: 2026-09-10 JST**

The latest theorem-bearing canonical merge represented here is:

```text
authoritative theorem branch: main
latest theorem-bearing merge: PR #1648
latest theorem layer: v2.67
last theorem-bearing canonical SHA:
  da0c3f185bf7808a1f3dc3c5facb4c8d388e1226
exact validated v2.67 proof head:
  95e9e16ae5c79574bea1d3cd31a27d014273ab9b
exact-head governance CI:
  KuuOS PR Governance Gate #1880 = completed / success
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

A documentation-only merge may advance `main` beyond the theorem-bearing SHA above. In that case the theorem baseline remains the exact integrated theorem merge named here until another theorem-bearing PR is merged.

Repository authority is not inferred from model memory, prose summaries, queued CI, validation-only branches, runtime receipts, retrieval scores, or philosophical analogy.

---

# What 空 means in KuuOS

KuuOS does **not** formalize 空 as the slogan “nothing exists.” Its operational role is an anti-reification discipline:

```text
chosen presentation != intrinsic substance
local observation    != global truth
retrieval score      != entailment
runtime success      != WORLD truth
formal encoding      != unique philosophical interpretation
model generation     != theorem authority
```

The bridge from 空 to 縁起 is therefore not erasure of structure. It is refusal to absolutize one representation while retaining the relations and coherence needed to transport between representations:

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

KuuOS also maintains interpretive bridges to Madhyamaka, Yogācāra, Huayan, Tiantai, and East Asian structures such as 陰陽, 五行, 道, 理・気, 礼, and 天人相関. These bridges are not silent mathematical identifications: historical-philosophical interpretation, formal mathematics, and AI implementation remain distinct presentations.

---

# Three layers of KuuOS

## 1. Philosophical layer

The philosophical layer asks how to reason without turning a local representation into an intrinsic substance. It emphasizes relation, context, transformation, dependence, compatibility, and the limits of any one viewpoint.

## 2. Mathematical layer

The mathematical layer studies contextual systems using categories, bicategories, pseudofunctors, localization-style factorization, higher coherence, descent, obstruction, gauge freedom, relation holonomy, orthogonality, scaled simplicial methods, and universal properties.

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

At the higher level, KuuOS studies Cat-valued contextual systems represented by pseudofunctors and asks how they behave under admissible changes of presentation.

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

**The final universal object and representation theorem are not yet proved.** No localization, stackification, quotient, fibrant replacement, or higher completion is called the universal dependent-origination object until the required mapping property is established.

---

# Current formal spine

The integrated higher dependent-origination line now reaches **v2.67**.

```text
v2.0       ordinary localization universal-property layer
v2.1–2.7   W + J dependent-origination sector
v2.8       Cat-valued stack descent
v2.9       bicategorical higher stack sector
v2.10      HigherLocalizationFactorization interface
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
v2.55      restricted Track A1 existence: W already base-isomorphisms
v2.56      pointwise W adjoint-equivalence data from weak admissibility
v2.57      free localization-path evaluator
v2.58      quotient-equal paths have nonempty evaluation isomorphisms
v2.59      exact coherent quotient-transport interface
v2.60      five-law coherent general-W factorization package
v2.61      unconditional simultaneous pointwise local choices
v2.62      fiber-functor 2-thin sufficient theorem
v2.63      fiber-hom thin sufficient theorem
v2.64      invertible-2-cell / fiber-core / automorphism-thin sharpening
v2.65      five explicit automorphism-valued coherence defects
v2.66      gauge-orbit normal form and canonical gauge obstruction
v2.67      untruncated relation 2-cells and relation-loop holonomy
```

The main advance after v2.55 is that the general-`W` problem is no longer described merely as “missing coherence.” The repository now exposes a concrete chain from local equivalence data to an explicit gauge/holonomy obstruction.

---

# General-W factorization: what is already proved

Let `R` be a raw Cat-valued higher contextual system and let `W` be the class of presentation changes intended to become equivalences.

The still-open unrestricted implication is:

```text
IsHigherWAdmissible W R
  ->
HasHigherLocalizationFactorization W R
```

The repository does **not** claim this theorem yet. Instead it has now decomposed the problem into exact layers.

## v2.56 — pointwise adjoint equivalences

Weak admissibility says each `R.map f`, for `f ∈ W`, is an equivalence of categories. v2.56 converts this into chosen pointwise adjoint-equivalence data using the actual Mathlib equivalence structure.

Thus the obstruction is **not** the existence of individual inverse functors.

## v2.57 — free-path evaluation

The formal localization quiver has ordinary arrows and formal inverses. v2.57 evaluates free paths in this quiver into `Cat`, using `R.map` on ordinary arrows and the chosen inverse on formal `W`-inverses.

Thus the obstruction is **not** evaluation of individual free paths.

## v2.58 — quotient-equal paths are locally isomorphic

If two free paths become equal in the ordinary Mathlib localization quotient, v2.58 proves that their evaluations are naturally isomorphic:

```text
localized equality of p and q
  ->
Nonempty (eval p ≅ eval q)
```

This proves local existence, not coherent global choice.

## v2.59–v2.60 — exact five-law coherence frontier

Using `Quot.out`, v2.59 fixes one representative for each localized arrow. To turn the representative assignment into a pseudofunctor, exactly three coherence equations are isolated:

```text
1. associativity
2. left unit
3. right unit
```

v2.60 adds the identity-component strong comparison back to the original `R`, whose remaining coherence is exactly:

```text
4. comparison identity
5. comparison composition
```

A complete five-law package constructs a genuine v2.10 `HigherLocalizationFactorization`.

## v2.61 — the local-choice space is inhabited

The individual `mapId`, `mapComp`, and `mapIso` witness types are all inhabited. A simultaneous pointwise choice can therefore always be made once v2.56 data are available.

No theorem infers coherence from `Classical.choice`.

## v2.62–v2.64 — proved sufficient sectors

The five laws become automatic under explicit thinness conditions.

The sequence sharpens from arbitrary 2-cell uniqueness to the invertible part only:

```text
fiber hom thin
  -> trivial fiber automorphisms
  -> fiber core thin
  -> relevant functor-iso thin
  -> five-law coherence
  -> HigherLocalizationFactorization
```

The sharp lesson is that the possible general obstruction lives in **invertible 2-dimensional isotropy**, not in arbitrary noninvertible natural transformations.

---

# v2.65 — five explicit automorphism-valued defects

For two parallel invertible 2-cells `η` and `θ`, v2.65 uses the defect

```text
δ(η, θ) = η⁻¹ θ
```

so that

```text
δ(η, θ) = 1  <->  η = θ.
```

The three quotient-pseudofunctor equations and two comparison equations therefore become five explicit automorphism-valued defects:

```text
δ_assoc
δ_left
δ_right
δ_comparison_id
δ_comparison_comp
```

Their simultaneous vanishing reconstructs the coherent v2.60 package and hence the genuine higher-localization factorization.

This turns an abstract coherence request into a concrete obstruction problem.

---

# v2.66 — gauge independence of the obstruction

The pointwise witnesses themselves are not intrinsic: any two valid local choices differ by target automorphisms.

v2.66 packages this as an explicit gauge action and proves that **all pointwise choices lie in one gauge orbit**.

It also proves the converse direction: every coherent v2.60 package projects to pointwise data whose five v2.65 defects vanish.

Therefore:

```text
HasCoherentGeneralWFactorizationData W R D
  <->
∃ L, FiveCoherenceDefectsTrivial W R D L
```

and, after basing at the canonical v2.61 pointwise choice:

```text
HasCoherentGeneralWFactorizationData W R D
  <->
CanonicalGeneralWGaugeTrivializable W R D.
```

Thus the remaining obstruction is **choice-independent at the level of the gauge orbit**.

Weak admissibility alone has not yet been proved to force this gauge obstruction to vanish.

---

# v2.67 — untruncated relation 2-cells and holonomy

Mathlib's ordinary localization is constructed by quotienting the path category by a propositionally truncated equivalence relation generated from:

```text
id
comp
Winv₁
Winv₂
```

with closure under composition and equivalence generation.

For ordinary 1-categorical localization this is exactly appropriate. For a Cat-valued pseudofunctor, however, different derivations of the same quotient equality may carry different invertible 2-dimensional information.

v2.67 therefore introduces a **Type-valued retained relation 2-cell**:

```text
LocalizationRelation2Cell W p q
```

with actual derivation constructors and an erasure back to the ordinary propositionally truncated localization equality.

Every retained relation 2-cell is evaluated to an actual natural isomorphism between free-path evaluations.

For two derivations

```text
α β : p ⇒ q
```

their difference loop is

```text
α⁻¹ · β : p ⇒ p
```

and its evaluation is a relation-loop holonomy automorphism.

The key theorem is:

```text
eval α = eval β
  <->
holonomy(α⁻¹ · β) = 1.
```

Globally v2.67 proves:

```text
EvaluationHolonomyTrivial W R D
  <->
Relation2CellEvaluationPathIndependent W R D.
```

The previously known v2.64 invertible-2-cell-thin sectors force this holonomy to vanish automatically.

### Boundary of v2.67

v2.67 is intentionally not the end of the general-`W` problem.

Its retained outer derivation is Type-valued, but the embedded Mathlib `CompClosure` witness is still proposition-valued and therefore still hides which generating relation was whiskered by which left/right paths. The base relation evaluation is correspondingly not yet the fully canonical generated 2-cell semantics needed to identify the five v2.65 defects with explicit generator-level loops.

That is the immediate next formal frontier.

---

# Current dependency graph

The theorem-backed general-`W` chain is now:

```text
IsHigherWAdmissible W R
        |
        v
pointwise W adjoint-equivalence data                    [v2.56]
        |
        v
free-path evaluator                                     [v2.57]
        |
        v
quotient-equal paths have local evaluation Iso          [v2.58]
        |
        +------------------------------+
        |                              |
        v                              v
pointwise local choices            retained relation 2-cells
        [v2.61]                         [v2.67]
        |                              |
        v                              v
five automorphism defects          relation-loop holonomy
        [v2.65]                         [v2.67]
        |                              |
        v                              v
single gauge orbit                 path independence
        [v2.66]                  <-> trivial holonomy
        |                              |
        +--------------+---------------+
                       |
                       v
      [CURRENT FRONTIER: identify generated relation
       holonomy with the five coherence defects]
                       |
                       v
        coherent general-W factorization data
                       |
                       v
        HigherLocalizationFactorization W R
```

The thinness results v2.62–64 enter as proved sufficient routes that kill the relevant automorphism/holonomy obstruction.

---

# Immediate next mathematical unit

The next layer should not add another arbitrary thinness hypothesis. It should remove the remaining proposition-level opacity in the relation syntax.

The planned generated 2-cell presentation retains, as Type-valued constructors:

```text
base generators:
  id
  comp
  Winv₁
  Winv₂

congruence generation:
  left whiskering
  right whiskering

2-cell closure:
  refl
  symm
  trans
```

Its evaluation should be defined recursively and canonically from:

```text
R.mapId
R.mapComp
chosen W-adjoint-equivalence unit/counit
functorial whiskering
vertical composition
```

rather than by choosing an arbitrary isomorphism supplied by a propositionally truncated relation witness.

The first major exit theorem is intended to have the form:

```text
GeneratedHolonomyTrivial W R D
  ->
HasHigherLocalizationFactorization W R.
```

The decisive research question after that is:

```text
Does IsHigherWAdmissible W R force GeneratedHolonomyTrivial W R D?
```

There are two legitimate outcomes:

```text
YES:
  prove unrestricted general-W factorization.

NO:
  construct an explicit 2-monodromy / cocycle countermodel,
  characterize the additional higher localization datum exactly,
  and replace ordinary 1-localization by the appropriate untruncated
  or bicategorical presentation where required.
```

KuuOS will not assume the positive answer in advance.

---

# Earlier obstruction structure remains active

The v2.42 E/R/A normal form remains part of the later universality program.

For one coherent datum `U`:

```text
E — HigherWeakEssentialUniquenessObstruction
R — HigherFixedChosenForwardModificationTriangleObstruction
A — HigherWeakCoherentAlignment
```

with:

```text
alignment     <-> no E and no R
not alignment <-> E or R
```

v2.43–54 provide several theorem-backed sufficient mechanisms for eliminating these later-stage obstructions once the required coherent universal datum exists.

These results do **not** replace the current Track A1 existence problem.

---

# What remains open

## A1. Unrestricted higher-localization factorization

Still open:

```text
IsHigherWAdmissible W R
  ->
HasHigherLocalizationFactorization W R
```

Unlike the old v2.55-era roadmap, the missing structure is now sharply identified by v2.65–67 as an automorphism-valued gauge / relation-holonomy problem.

## A2. Coherent universal-data existence

Still open:

```text
IsHigherWAdmissible W R
  ->
HasCoherentWeakHigherLocalizationUniversalProperty W R
```

Factorization is Stage I. It is not yet coherent Stage II universality.

## Axis E — Stage III existence

General essential uniqueness remains open. v2.43–54 provide structural sufficient routes, not a universal existence theorem.

## Axis R — fixed coherent route

General correction / modification-triangle solvability remains open. v2.37–42 give its exact normal form; v2.43–54 eliminate it under explicit rigidity hypotheses.

## General strictification

Strictification remains a possible theorem route, not an axiom. KuuOS does not silently replace a weak equivalence-valued pseudofunctor by an unrelated ordinary functor.

## Final dependent-origination universal object

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

multiple valid transformation histories
  -> path-independence / holonomy problem

local plausibility without global support
  -> descent-failure candidate

interoperability
  -> relational invariance, not assumed shared latent coordinates
```

The aim is not to claim that present LLMs already satisfy the final KuuOS axioms. The aim is to build systems in which context, provenance, representation change, inconsistency, verification, authority, and failure of coherence are first-class objects.

A model migration should therefore be treated schematically as:

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
retrieval score      != entailment
embedding similarity != semantic proof
GraphRAG              != global ontology
retrieved evidence    != verified evidence
selection             != execution
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
no arbitrary Classical.choice => coherence inference
no ordinary-localization substitute for the general higher theorem
```

Exact-SHA discipline:

```text
queued / in_progress != success
head change invalidates old CI authority
exact-head CI running => write freeze
Ready only after exact-head green
normal merge uses exact expected head SHA
post-merge authority requires fresh main verification
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

same quotient arrow != automatically same retained 2-dimensional derivation
local Nonempty Iso != coherent descent
pointwise inverse choice != pseudofunctor coherence
gauge equivalence != automatic zero obstruction
ordinary 1-localization != automatically sufficient for arbitrary 2-monodromy

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

# Current research sentence

As of v2.67, the central formal question is no longer “can individual `W`-equivalences be inverted?” They can. It is:

> **When ordinary localization identifies two presentation paths, is the Cat-valued evaluation independent of the retained 2-dimensional derivation, and if not, what higher localization data exactly records the resulting holonomy?**

That question is now represented in Lean by explicit gauge defects and relation-loop holonomy rather than by an unspecified coherence gap.
