# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, correction, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

Its central mathematical question is:

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, what obstructs that process, and which universal property characterizes the invariant content?

Philosophical interpretation, mathematical presentation, formal proof, runtime validation, and operational authority are related but deliberately kept as distinct evidence classes.

## Canonical theorem snapshot — 2026-09-24 JST

| Item | Current reference |
| --- | --- |
| Canonical branch | `main` |
| Current theorem-bearing baseline | `0066169d5e25320015e2a485be7d3a449b5c107d` |
| Canonical theorem frontier | **v3.73 — arbitrary-factorization object coboundary** |
| Latest theorem-bearing merge | [PR #1760](https://github.com/itakura-hidetoshi/KuuOS/pull/1760) |
| v3.73 merge commit | `0066169d5e25320015e2a485be7d3a449b5c107d` |
| Validated v3.73 PR head | `459e9bee357f610d7b1e360ad568c3d86ff2066b` |
| v3.73 exact-head governance run | [35968840745](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35968840745), completed / success |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| Mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

Theorem authority is fixed:

```text
fresh exact canonical GitHub SHA
  > formal Lean artifacts at that SHA
  > README / ROADMAP
  > exact-head CI receipts
  > history / memory
```

A documentation-only merge may advance `main` beyond the theorem-bearing baseline without changing mathematical authority. Re-observe the exact current `main` SHA before theorem work.

The separate Lean 4.31 validation-only PR **#1558** remains **open / Draft / unmerged** and outside theorem authority. It must not be merged, marked Ready for review, or auto-merged.

## What 空 means here

空 is not treated as “nothing exists.” Its operational role is non-reification: a useful presentation may be locally effective without being intrinsic, unique, or globally authoritative.

```text
chosen presentation != intrinsic substance
local observation != global truth
retrieval score != entailment
runtime success != WORLD truth
formal encoding != unique philosophical interpretation
model generation != theorem authority
```

The bridge from 空 to 縁起 keeps context, relations, admissible transport, higher coherence, descent, obstruction, correction, and authority explicit.

## Current concrete mathematical spine

The octahedral `C2` truth test now separates four levels:

```text
A. quotient representative 1-cells
B. quotient pseudofunctor coherence
C. coherent presentation comparison for the canonical pointwise datum
D. arbitrary HigherLocalizationFactorization data
```

The integrated result is:

```text
v3.66  selected quotient representative 1-cells collapse to identity

v3.67  a fully coherent quotient transport exists

v3.68  the explicit v3.67 transport has no Stage-II comparison

v3.69  every coherent quotient transport for the canonical pointwise datum
       fails Stage-II comparison

v3.70  weak admissibility does not imply canonical five-law /
       generated-coboundary solvability

v3.71  a canonical-normalization bridge is not a weaker shortcut:
       for the countermodel it is equivalent to abstract nonfactorization

v3.72  arbitrary HigherLocalizationFactorization composition is scalarized
       directly, exposing object dependence and a localized-lift compositor term

v3.73  the object dependence is an explicit multiplicative coboundary;
       that coboundary is trivial on source-fiber loops
```

The decisive frontier is therefore no longer quotient-transport independence. It is the **direct arbitrary-factorization parity problem**.

## v3.66–v3.67 — quotient stage closes positively

v3.66 proves that every selected quotient representative 1-cell in the concrete `C2` model is literally the identity Cat 1-cell.

v3.67 then constructs explicit

```lean
CoherentQuotientTransportData
  (W := allMorphisms) counterSystem counterD
```

and proves:

```text
HasCoherentQuotientTransportData
ThreeQuotientRoutesJointlyCorrectable
(commonQuotientRouteCorrectionLocus ...).Nonempty
```

Thus:

```text
nontrivial generated holonomy
  !=>
quotient-stage incoherence
```

and the earlier fixed-gauge failure is genuinely gauge-specific.

## v3.68–v3.69 — Stage-II obstruction becomes transport-independent

v3.68 proves the octahedral `ZMod 2` parity contradiction for the explicit v3.67 quotient transport.

v3.69 removes that specialization.

For arbitrary

```lean
T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD
```

the Stage-II face equation contains both comparison-edge scalars and the compositor scalar selected by `T`. The associator coherence of `T`, together with the localization middle-switch argument, forces the total eight-face transport-compositor parity to vanish.

Any successful Stage-II comparison would force the same total parity to be `1`.

Therefore v3.69 proves:

```lean
counterD_noCoherentPresentationComparison_for_all_transports
```

and hence:

```text
Stage-I coherent quotient transport exists
and
every coherent quotient transport for counterD fails Stage-II comparison
```

It also proves:

```lean
counterD_not_hasCoherentGeneralWFactorizationData
```

for the canonical pointwise datum `counterD`.

This still does **not** prove that every abstract `HigherLocalizationFactorization` is impossible.

## v3.70 — weak admissibility does not force the canonical five-law package

v3.70 returns the v3.69 obstruction to the weak-admissibility boundary.

For the concrete octahedral `C2` model:

```text
IsHigherWAdmissible allMorphisms counterSystem
```

holds, but the canonical pointwise datum admits neither:

```text
HasCoherentGeneralWFactorizationData
```

nor:

```text
GeneratedCorrectionCoboundarySolvable
```

Thus weak admissibility alone does not imply success of the canonical v2.56–v3.04 five-law construction route.

This is a counterexample to that canonical route, not yet to the larger abstract factorization interface.

## v3.71 — the normalization bridge is logically circular

For any arbitrary factorization

```lean
H : HigherLocalizationFactorization (W := W) R
```

v3.71 decomposes it into:

```text
H.lift
  -> tautological factorization of restrict(H.lift)

H.comparison
  -> pointwise-equivalence comparison
     restrict(H.lift) --> R
```

For the concrete countermodel it then proves:

```text
every abstract factorization canonically normalizes to five-law data
  <->
no abstract HigherLocalizationFactorization exists
```

Therefore “prove normalization first, then deduce nonfactorization” is circular here. The arbitrary factorization must be analyzed directly, or the parity obstruction must be transported by an independently proved presentation-invariance theorem.

## v3.72 — direct scalarization of arbitrary factorization

v3.72 works directly with:

```lean
H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem
```

For a source-fiber object `A`, StrongTrans composition coherence becomes:

```text
edge(fg, A)
  = rawFace(f,g)^(-1)
      * edge(f, A)
      * edge(g, F(f)A)
      * image(sourceCompositor(f,g,A))
```

Two freedoms absent from the canonical quotient calculation are now explicit:

1. edge scalars depend on source-fiber objects;
2. the arbitrary localized lift contributes its own compositor scalar.

So the v3.69 octahedral cancellation cannot simply be copied to arbitrary factorization data.

## v3.73 — object dependence is a coboundary

For a source-fiber morphism `u : A ⟶ B`, v3.73 proves:

```text
edge(f,B) * transported(u)
  =
source(u) * edge(f,A)
```

and therefore:

```text
edge(f,B)
  =
delta_f(u) * edge(f,A)

delta_f(u)
  =
source(u) * transported(u)^(-1)
```

This identifies object dependence as an explicit multiplicative coboundary.

For loops:

```text
u : A ⟶ A
```

the transported and source loop scalars coincide, so:

```text
delta_f(u) = 1
```

Hence the remaining freedom is not arbitrary on automorphism loops. What remains unresolved is the inter-object contribution together with the arbitrary localized compositor term.

## Exact next frontier — v3.74

The next theorem unit should combine the two residual terms exposed by v3.72–v3.73:

```text
object-change coboundary
+
localized-lift compositor contribution
```

The direct truth test is:

```text
Does their total contribution cancel around the octahedral eight-face sum?

or

Can an explicit arbitrary localized lift use them to absorb
the raw nontrivial C2 parity class?
```

Both outcomes remain mathematically legitimate.

A useful route is:

1. choose compatible source objects along the octahedral edges;
2. rewrite every edge scalar change using the v3.73 object coboundary;
3. insert the v3.72 arbitrary-factorization composition equation on all eight faces;
4. use pseudofunctor associator/unit coherence of `H.lift`;
5. isolate the total inter-object and compositor contribution;
6. either prove it is parity-trivial or construct an absorbing example.

Only after this direct truth test can one assert or refute:

```text
¬ HasHigherLocalizationFactorization
    (W := allMorphisms) counterSystem
```

## Exact logical boundary

Currently proved:

```text
all coherent quotient transports for counterD fail Stage-II comparison

weak admissibility does not force canonical five-law solvability

canonical-normalization of arbitrary factorization is not an independent bridge

arbitrary factorization composition admits an exact object-dependent scalar law

object dependence is a coboundary and is loop-trivial
```

Not yet proved:

```text
no arbitrary HigherLocalizationFactorization exists

the v3.73 inter-object coboundaries cancel globally

the arbitrary localized-lift compositor contribution is parity-trivial

the final higher-localization universal object exists

the final representation theorem exists
```

## Dependent Origination Universality Program

The long-range target remains an explicitly constructed carrier, schematically:

```text
eta : C ⟶ DO(C, W, J, H)

AdmissibleContextualSystems(C, X)
  ≃ Fun(DO(C, W, J, H), X)
```

with correct higher variance, coherent factorization, essential uniqueness, naturality, descent compatibility, presentation invariance, and explicit obstruction/correction semantics.

**The final universal object and representation theorem are not yet proved.**

## Proof-engineering lessons retained

Recent v3.69–v3.73 work reinforces these rules:

- **Import is not open.** Open the defining namespace or qualify declarations.
- **Scoped instances matter.** For StrongTrans identity/category structure, use `open scoped CategoryTheory.Pseudofunctor.StrongTrans`.
- **Keep `autoImplicit false`.**
- **Use `eqToIso` / `eqToHom` for dependent transport.**
- **Work in layers:** `Cat.Hom₂` → `NatTrans` → component → exact target fiber → scalar.
- **Do not multiply abstract dependent Hom values.** Keep `≫` until the carrier is fixed.
- **Remember `SingleObj`:** `f ≫ g = g * f`.
- **Scalarize exact fibers explicitly.** The helper `counterSystemHomScalar` is used to preserve dependent typing while exposing `C2`.
- **Use canonical group lemmas.** Prefer `inv_mul_cancel_left`, `mul_inv_cancel`, etc. over hand-written cancellation rewrites.
- **Localize broad unfolding.** Use helper lemmas downstream.
- **Separate ring algebra from characteristic-two simplification.**
- **Every code change invalidates old-head CI receipts.**
- **Merge only with the validated current head SHA.**

## No-go implications

Do not promote the following without a theorem:

```text
import -> namespace opened
Classical.choice -> coherence
local Nonempty Iso -> coherent global choice

weak admissibility -> canonical five-law solvability
weak admissibility -> generated holonomy triviality

nontrivial generated holonomy -> quotient-stage incoherence
groupoid localization -> trivial holonomy
representative equivalence -> coherent quotient transport

one bad fixed gauge -> every gauge fails
identity quotient representatives -> quotient coherence automatic

v3.67 coherent quotient transport -> Stage-II comparison exists

v3.69 all coherent quotient transports fail Stage II for counterD
  -> no arbitrary HigherLocalizationFactorization

canonical-normalization bridge
  -> a weaker intermediate theorem
  (for this countermodel it is equivalent to nonfactorization)

v3.73 loop-trivial object coboundary
  -> global object-independence

v3.72/v3.73 scalar reductions
  -> final octahedral parity contradiction for arbitrary H

Stage-I factorization -> Stage-II universality
docs-only CI -> theorem validation
runtime success -> theorem authority
memory/history -> fresh GitHub authority
```

## Reproduction

Focused current theorem targets:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationArbitraryTransportComparisonV3_69

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationCanonicalFiveLawCounterexampleV3_70

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationFactorizationNecessityBoundaryV3_71

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationArbitraryFactorizationScalarV3_72

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationFactorizationObjectCoboundaryV3_73
```

Current v3.73 validation:

```text
validated PR head
459e9bee357f610d7b1e360ad568c3d86ff2066b

governance run
35968840745

theorem merge
0066169d5e25320015e2a485be7d3a449b5c107d
```

The aggregate formal target remains separate:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

Runtime validation remains separate:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

A runtime result is not a theorem. A docs-only gate is not theorem validation. A CI receipt applies only to its recorded exact head.

## Current research sentence

**The concrete octahedral `C2` truth test has progressed beyond transport-specific obstruction: v3.69 proves that every coherent quotient transport for the canonical pointwise datum fails Stage-II comparison; v3.70 shows weak admissibility does not force canonical five-law solvability; v3.71 prevents a circular normalization shortcut; v3.72 directly scalarizes arbitrary factorization coherence; and v3.73 proves that its source-object dependence is an explicit coboundary that vanishes on loops. The next decisive step is to combine the inter-object coboundary with the arbitrary localized-lift compositor and determine whether their global eight-face contribution must vanish or can absorb the raw C2 parity class.**
