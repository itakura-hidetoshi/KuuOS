# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, correction, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

Its central mathematical question is:

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, what obstructs that process, and which universal property characterizes the invariant content?

Philosophical interpretation, mathematical presentation, formal proof, runtime validation, and operational authority are related but deliberately kept as distinct evidence classes.

## Canonical theorem snapshot — 2026-09-25 JST

| Item | Current reference |
| --- | --- |
| Canonical branch | `main` |
| Current theorem-bearing baseline | `c63c20c8f7726d45ac419a4d4b6a8b794e54f1db` |
| Canonical theorem frontier | **v4.19 — middle-switch pair incidence on the truncated-icosahedral seed carrier** |
| Latest theorem-bearing merge | [PR #1807](https://github.com/itakura-hidetoshi/KuuOS/pull/1807) |
| v4.19 validated PR head | `dc19c0d738c853dc648e54f12709387953031203` |
| v4.19 merge commit | `c63c20c8f7726d45ac419a4d4b6a8b794e54f1db` |
| v4.19 exact-head governance run | [36145319284](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/36145319284), completed / success |
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

The separate Lean 4.31 validation-only PR **#1558** remains **open / Draft / unmerged** at head `3a09839782ea82661ddbf8e13a0fd08e893079b4`. It is outside theorem authority and must not be merged, marked Ready for review, or auto-merged.

## What 空 means here

空 is not treated as “nothing exists.” Its operational role is non-reification: a presentation can be useful without being intrinsic, unique, or globally authoritative.

```text
chosen presentation != intrinsic substance
local observation != global truth
retrieval score != entailment
runtime success != WORLD truth
formal encoding != unique philosophical interpretation
model generation != theorem authority
```

The bridge from 空 to 縁起 keeps context, relations, admissible transport, higher coherence, descent, obstruction, correction, and authority explicit.

## Current mathematical status

The finite octahedral `C2` truth test is no longer an open search for abstract nonfactorization.

**v4.00 closes the direct arbitrary-factorization problem:**

```lean
IsEmpty
  (HigherLocalizationFactorization
    (W := allMorphisms) counterSystem)
```

Equivalently:

```text
the concrete octahedral C2 countermodel
admits no HigherLocalizationFactorization at all
```

This is stronger than the earlier canonical five-law counterexample. The proof passes through the direct arbitrary-factorization parity line, including object-coboundary reduction, localized compositor coherence, middle-switch transport, raw/full-localization compositor comparison, and essential-surjectivity extraction of source-fiber objects.

Consequently, the current truncated-icosahedral program is a **carrier/refinement analysis of an already-proved obstruction**, not a substitute for a missing nonfactorization theorem.

## v4.00–v4.11 — abstract nonfactorization and exact Stage-II location

The integrated spine is:

```text
v4.00  abstract nonfactorization:
       HigherLocalizationFactorization counterSystem is empty

v4.01  weak allMorphisms-admissibility does not imply
       arbitrary higher-localization factorization

v4.02  weak higher-localization existence and weak universal principles
       are false on the finite octahedral truth-test context

v4.03  the v2.31 gap decomposition fails already at Stage I

v4.04  the countermodel lies outside all earlier thin / iso-thin /
       canonical-gauge-trivializable sufficient sectors

v4.05  the residual invertible isotropy is explicit:
       zeta is a nonidentity fiber automorphism and a nonidentity
       functor-level invertible 2-cell

v4.06  the five-defect obstruction is gauge-independent:
       every pointwise-choice gauge orbit misses the zero-defect locus

v4.07  post-factorization H-indexed scalar/seam constructions are
       vacuous for counterSystem because no such H exists

v4.08  the generated five-face correction coboundary is unsolvable

v4.09  every solved quotient gauge has no comparison-gauge lift

v4.10  the quotient stage really is solvable for counterD,
       while the comparison lift is impossible

v4.11  the original coherent-presentation obstruction and the
       generated comparison-gauge obstruction are two operational
       presentations of the same transport-independent Stage-II failure
```

The exact location is therefore:

```text
coherent quotient transport          EXISTS
quotient three-face coboundary       SOLVABLE
comparison / presentation lift       IMPOSSIBLE
full five-face correction            IMPOSSIBLE
HigherLocalizationFactorization      IMPOSSIBLE
```

## v4.12 — transport-independent scalar obstruction class

Source:

```text
formal/KUOS/DependentOriginationStageIIObstructionClassV4_12.lean
```

For every coherent quotient transport `T`, v4.12 extracts a scalar Stage-II obstruction:

```text
omega(T) = 1  in ZMod 2
```

while any successful comparison would force:

```text
omega(T) = 0
```

Thus `omega` is a pre-factorization, transport-independent obstruction representative. This is the scalar class used by the current recursive carrier program.

## v4.13–v4.15 — local parity and the failure of uniform global transport

The truncated-icosahedral carrier has pentagram-like five-crossing and hexagram-like six-crossing local refinements.

v4.13 proves the uniform mod-2 contrast:

```text
pentagram: 5 * omega = omega
hexagram:  6 * omega = 0
```

v4.14 then proves that **uniform face-type transport over the whole truncated icosahedron vanishes**:

```text
12 pentagonal contributions -> even -> 0
20 hexagonal contributions   -> 0
global uniform total         -> 0
```

Therefore local five-versus-six parity is not by itself a global obstruction theorem.

v4.15 shows that a nonuniform singleton face support can preserve `omega` algebraically, but an arbitrary selected face is not yet authority-bearing or canonical.

## v4.16–v4.19 — explicit finite carrier and incidence-compatible embedding

v4.16 builds an explicit eight-element carrier for the octahedral Stage-II parity data.

v4.17 proves that all eight labels inject into the 12 pentagonal seed faces of the truncated icosahedron. Capacity is therefore sufficient globally.

v4.18 proves a sharp local obstruction:

```text
8 source parity labels
  cannot inject into
one pentagram crossing set  (5)
or
one hexagram crossing set   (6)
```

So faithful one-to-one transport cannot live inside one local recursive star.

v4.19 advances beyond cardinality. It constructs an injective global placement of all eight Stage-II parity labels such that each middle-switch mate pair lands on a genuine **pentagon–hexagon adjacent incidence** and the two mates have opposite face kinds.

The current frontier is therefore not “can eight labels fit?” It is:

> Can the Stage-II obstruction itself canonically select such an incidence-compatible placement, with the correct orientation/scalar pushforward, and can that class be shown to survive recursive refinement?

## Current exact frontier after v4.19

Proved:

```text
1. abstract nonfactorization of the finite C2 countermodel

2. weak admissibility does not force higher-localization factorization

3. the quotient carrier exists coherently

4. the obstruction is exactly at the comparison-lift stage

5. the Stage-II obstruction has a transport-independent ZMod-2 scalar class

6. uniform pentagram/hexagram transport is locally odd/even but globally zero

7. nonuniform support can preserve the class algebraically

8. the eight source parity labels admit a global seed-face embedding

9. no one local star can carry all eight labels injectively

10. an incidence-compatible global embedding exists in which every
    middle-switch mate pair lands on a pentagon–hexagon adjacency
```

Not yet proved:

```text
the v4.19 placement is canonical or uniquely selected by the obstruction

the eight source scalar values push forward with a proved orientation/sign rule

the pair-incidence placement induces a nonzero global cocycle on the seed carrier

recursive pentagram/hexagram refinement preserves that obstruction class

a metric fractal limit or metric self-similarity theorem

the final dependent-origination universal object / representation theorem
```

The immediate theorem frontier should stay on **authority-bearing carrier transport**, not return to post-factorization scalar data whose `H` parameter is impossible for `counterSystem`.

## Current carrier picture

The present geometry is combinatorial/incidence-theoretic:

```text
octahedral Stage-II obstruction
  -> eight labeled parity faces
  -> global truncated-icosahedral seed carrier
  -> middle-switch mate pairing
  -> pentagon–hexagon adjacent placements
  -> future recursive refinement transport
```

This is a theorem about finite carrier structure and incidence compatibility. It is **not yet** a theorem of Euclidean embedding, scale invariance, Hausdorff dimension, metric fractality, or an infinite recursive limit.

## Long-range Dependent Origination Universality Program

The long-range target remains an explicitly constructed carrier with a genuine mapping property, schematically:

```text
eta : C ⟶ DO(C, W, J, H)

AdmissibleContextualSystems(C, X)
  ≃ Fun(DO(C, W, J, H), X)
```

with correct higher variance, coherent factorization, essential uniqueness, naturality, descent compatibility, presentation invariance, and explicit obstruction/correction semantics.

The current finite countermodel proves that weak arrowwise admissibility alone is insufficient. Any positive general theorem must impose additional coherence, thinness, separating, descent, or other hypotheses strong enough to avoid the v4.00 obstruction.

**The final universal object and representation theorem are not yet proved.**

## Proof-engineering rules retained

Recent v4.x work reinforces these rules:

- **Fresh GitHub authority first.** Re-observe `main` before theorem work.
- **Import is not open.** Open the defining namespace or qualify declarations.
- **Module/file names are not namespace names.**
- **Local attributes are local.** An imported `@[local simp]` set is not inherited.
- **Keep `autoImplicit false`.**
- **Give tactic terms expected types.** Do not place an untyped `by ...` term in function position.
- **Reduce structure projections before `ac_rfl`.**
- **Use `eqToIso` / `eqToHom` for dependent transport.**
- **Use the categorical-to-scalar pipeline:** `Cat.Hom₂` → `NatTrans` → component → exact fiber → scalar.
- **Do not multiply abstract dependent Hom values.** Keep categorical composition until the carrier is fixed.
- **Remember `SingleObj`:** `f ≫ g = g * f`.
- **Separate ordinary ring algebra from characteristic-two simplification.**
- **Every code change invalidates old-head CI receipts.**
- **Merge only with the validated current head SHA.**

## No-go implications

Do not promote the following without theorem support:

```text
weak admissibility -> HigherLocalizationFactorization
weak admissibility -> weak localization universal property

nontrivial generated holonomy -> quotient transport failure
one bad fixed gauge -> every gauge fails

local pentagram odd parity -> nonzero global truncated-icosahedral obstruction
uniform local support -> global obstruction preservation
cardinality injection -> semantic / authority-bearing transport

v4.15 arbitrary singleton support -> canonical distinguished support
v4.17 capacity embedding -> canonical carrier map
v4.19 incidence-compatible placement -> canonical placement
pair adjacency -> recursive obstruction preservation

combinatorial recursion -> metric fractal theorem
runtime success -> theorem authority
docs-only CI -> theorem validation
history / memory -> fresh GitHub authority
```

## Reproduction

Focused current theorem targets:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationAbstractNonfactorizationV4_00

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationStageIIObstructionClassV4_12

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationLocalStarCapacityObstructionV4_18

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationMiddleSwitchPairIncidenceV4_19
```

Current v4.19 validation:

```text
validated PR head
dc19c0d738c853dc648e54f12709387953031203

governance run
36145319284

theorem merge
c63c20c8f7726d45ac419a4d4b6a8b794e54f1db
```

Aggregate formal target remains separate:

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

**The finite octahedral `C2` truth test is now closed at the abstract factorization level: v4.00 proves that no `HigherLocalizationFactorization` exists, while v4.10–v4.12 localize the surviving pre-factorization obstruction exactly at the transport-independent Stage-II comparison lift and extract its nonzero `ZMod 2` class. The current v4.13–v4.19 program studies how that already-proved class can be carried by the truncated-icosahedral recursive geometry: uniform transport cancels globally, one local star is too small for all eight labels, but an injective global placement exists in which every middle-switch mate pair lands on a genuine pentagon–hexagon incidence. The next theorem must make that placement authority-bearing and prove the correct scalar/orientation pushforward before any recursive-preservation claim is promoted.**
