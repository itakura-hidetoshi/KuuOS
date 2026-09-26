# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, correction, recursive carriers, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

Its central mathematical question is:

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, what obstructs that process, and which universal property characterizes the invariant content?

Philosophical interpretation, mathematical presentation, formal proof, runtime validation, and operational authority are related but deliberately kept as distinct evidence classes.

## Canonical theorem snapshot — 2026-09-26 JST

| Item | Current reference |
| --- | --- |
| Canonical branch | **main** |
| Current theorem-bearing baseline | **4752f516cf4f6eaf01599751576b70e00002b2a0** |
| Canonical theorem frontier | **v4.34 — Cantor critical exponent algebra** |
| Latest theorem-bearing merge | PR #1827, Formalize Cantor critical exponent v4.34 |
| v4.34 validated PR head | **ab5367b51b872f67ea6d73ff05947f51d601420d** |
| v4.34 exact-head governance run | **36222915576**, completed / success |
| Lean | **leanprover/lean4:v4.30.0-rc2** |
| Mathlib | **5450b53e5ddc75d46418fabb605edbf36bd0beb6** |

The theorem authority order is fixed:

~~~text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > exact-head CI receipts
  > history / memory
~~~

A documentation-only merge may advance main beyond the theorem-bearing baseline without changing mathematical authority. Always re-observe the exact current main SHA before theorem work.

The separate Lean 4.31 validation-only PR **#1558** remains **open / Draft / unmerged** at head:

~~~text
3a09839782ea82661ddbf8e13a0fd08e893079b4
~~~

It is outside theorem authority and must not be merged, marked Ready for review, or auto-merged.

## What 空 means here

空 is not treated as “nothing exists.” Its operational role is non-reification: a presentation can be useful without being intrinsic, unique, or globally authoritative.

~~~text
chosen presentation != intrinsic substance
local observation != global truth
runtime success != WORLD truth
formal encoding != unique philosophical interpretation
model generation != theorem authority
~~~

The bridge from 空 to 縁起 keeps context, relations, admissible transport, higher coherence, descent, obstruction, correction, recursive presentation, and authority explicit.

## Current mathematical status

The finite octahedral C2 truth test is closed at the abstract factorization level.

### v4.00 — abstract nonfactorization

KuuOS proves:

~~~lean
IsEmpty
  (HigherLocalizationFactorization
    (W := allMorphisms) counterSystem)
~~~

The concrete finite octahedral countermodel admits no HigherLocalizationFactorization at all.

The later recursive/fractal program therefore does not replace a missing nonfactorization theorem. It transports and analyzes an obstruction that is already proved.

### v4.01–v4.12 — exact obstruction location

The integrated result is:

~~~text
weak admissibility                         EXISTS
coherent quotient transport               EXISTS
quotient three-face coboundary             SOLVABLE
comparison / presentation lift             IMPOSSIBLE
full five-face correction                  IMPOSSIBLE
HigherLocalizationFactorization            IMPOSSIBLE
~~~

v4.12 extracts the transport-independent Stage-II scalar class:

~~~text
omega(T) = 1 in ZMod 2
~~~

for every coherent quotient transport T. Any successful comparison would force omega(T)=0.

## v4.13–v4.19 — finite carrier and incidence geometry

- **v4.13:** pentagram/hexagram parity contrast: 5·omega = omega, 6·omega = 0.
- **v4.14:** uniform global transport over the 12 pentagons and 20 hexagons cancels.
- **v4.15:** a nonuniform singleton support can preserve omega algebraically, but arbitrary support is not canonical.
- **v4.16:** an explicit eight-label Stage-II parity carrier is constructed.
- **v4.17:** eight labels inject globally into the 12 pentagonal seed faces.
- **v4.18:** one local pentagram or hexagram is too small to carry all eight labels injectively.
- **v4.19:** an injective global placement exists whose middle-switch mate pairs land on genuine adjacent pentagon–hexagon seed faces with opposite face kinds.

## v4.20–v4.27 — obstruction transport to an inverse limit

### v4.20 — incidence pushforward

The actual Stage-II scalar values are pushed along the v4.19 incidence embedding with source provenance. The pushed mismatch reduces to the v4.12 obstruction.

### v4.21 — orientation signs collapse mod 2

Forward/reverse orientation is introduced, and the sign-only distinction is proved to collapse in ZMod 2.

### v4.22 — integer orientation lift

Orientation is lifted to integer representatives with forward = +1 and reverse = -1. Reduction mod 2 recovers the v4.20 scalar, while the integer mismatch remains nonzero.

### v4.23 — one recursive central-cell step

Each of the eight globally placed seed faces is refined independently. The construction respects the v4.18 local-capacity obstruction and never forces all eight labels into one local star.

### v4.24 — every finite depth

Using the v3.90 face-kind stability theorem, v4.24 proves at every natural-number depth:

- distinct root-parent provenance;
- stable face kind and arity;
- stable orientation;
- stable integer representative;
- depth-invariant total and mismatch;
- mod-2 reduction equal to omega(T)=1.

### v4.25 — coherent finite-depth tower

The depth-indexed central cells are packaged with strict restriction maps. Restriction preserves the representative, total, and mismatch.

### v4.26 — set-theoretic inverse limit

The infinite supported compatible-section carrier is defined and shown to satisfy:

~~~text
OctahedralStageIIParityFace
  ≃
StageIIFiniteDepthInverseLimit
~~~

Every inverse-limit point has one unique source label. The inverse-limit obstruction equals every finite-depth value and remains nonzero.

### v4.27 — middle-switch involution on the inverse limit

The v4.19 mate involution is transported across the v4.26 equivalence. It remains involutive, injective, fixed-point-free, and preserves the pentagon–hexagon mate semantics at every finite depth.

## v4.28–v4.32 — Hausdorff dimension, topology, metric convergence, and a geometric fractal limit

The formal development now contains genuine metric statements.

### v4.28 — the rigid current carrier has dimension zero

The v4.26 inverse-limit carrier has exactly eight points. Therefore, for every extended metric structure on it:

~~~text
dimH XInfinityCurrent = 0
~~~

This is intrinsic finiteness, not a special-metric artifact.

### v4.29 — a positive-dimensional branching carrier

Each current carrier point is thickened by a nondegenerate real unit segment. The resulting branch carrier satisfies:

~~~text
dimH XInfinityBranch = 1
0 < dimH XInfinityBranch
~~~

Positive dimension appears because genuine continuous branch freedom has been added.

### v4.30 — translated Cantor geometry

Each branch contains a translated copy of the classical ternary Cantor set. The global geometric carrier is a finite union of eight such fibers.

Proved:

- compactness of each fiber;
- compactness and closedness of the global carrier;
- nonemptiness;
- exact two-child ternary self-similarity on every branch;
- inclusion in the v4.29 ambient branch carrier.

### v4.31 — Hausdorff metric convergence

Finite ternary approximants satisfy:

~~~text
dist(approx_n, limit) <= 3^(-n)
hausdorffDist(X_n, X_infinity) <= 3^(-n)
hausdorffDist(X_n, X_infinity) -> 0
~~~

This is convergence of sets in Hausdorff distance.

### v4.32 — geometric fractal-limit certificate

v4.32 bundles:

- exact ambient branch dimension 1;
- compact / closed / nonempty limit topology;
- inclusion of the fractal limit in the branch carrier;
- exact branchwise Cantor self-similarity;
- explicit Hausdorff-distance rate;
- Hausdorff metric convergence.

The geometric Cantor limit itself currently has the proved bound:

~~~text
dimH XInfinityGeometricFractal <= 1
~~~

The exact Cantor value is deliberately not inferred from self-similarity alone.

## v4.33–v4.34 — exact Cantor-dimension preparation

### v4.33 — binary Cantor space has exact Hausdorff dimension one

Using mathlib’s PiNat metric on Nat → Bool, v4.33 proves:

~~~text
dimH (Set.univ : Set (Nat -> Bool)) = 1
~~~

The lower bound comes from a 1-Lipschitz binary expansion onto the real unit interval.

The upper bound comes from the canonical length-n binary-cylinder cover:

~~~text
number of cylinders = 2^n
diameter of each    <= 2^(-n)
total 1-dimensional cover cost <= 1
~~~

together with a Hausdorff-measure liminf bound.

### v4.34 — critical Cantor exponent algebra

Define:

~~~text
s = logb 3 2 = log 2 / log 3
~~~

v4.34 proves:

~~~text
0 < s < 1
3^s = 2
s * logb 2 3 = 1
(logb 2 3)^(-1) = s
~~~

This closes the real-number scaling algebra required for the quantitative coding argument. It does not yet prove the exact Hausdorff dimension of the real Cantor set.

## Current exact frontier

Canonically proved after v4.34:

~~~text
octahedral C2 truth test:
  no HigherLocalizationFactorization

Stage-II obstruction:
  transport-independent omega(T) = 1 in ZMod 2

recursive carrier:
  one-step preservation
  every finite-depth preservation
  coherent restriction tower
  set-theoretic inverse limit
  fixed-point-free middle-switch involution

current inverse-limit carrier:
  8 points
  Hausdorff dimension 0 for every extended metric structure

branch carrier:
  Hausdorff dimension exactly 1

geometric Cantor carrier:
  compact
  closed
  nonempty
  exact branchwise ternary self-similarity
  Hausdorff-distance approximants with rate <= 3^(-n)
  Hausdorff convergence
  Hausdorff dimension <= 1

binary Cantor source space:
  Hausdorff dimension exactly 1

critical exponent:
  s = log 2 / log 3
  0 < s < 1
  exact binary/ternary scale identities
~~~

Not yet proved:

~~~text
dimH cantorSet = log 2 / log 3

exact quantitative Hölder bounds for:
  binary code -> ternary Cantor geometry
  ternary Cantor geometry -> binary code

dimH of each translated Cantor branch = log 2 / log 3
dimH XInfinityGeometricFractal = log 2 / log 3

the final dependent-origination universal object / representation theorem
~~~

## Immediate next theorem sequence

### v4.35 — Cantor coding prefix and separation estimates

Prove typed quantitative bounds connecting the first differing binary digit with Euclidean distance between the corresponding ternary Cantor points.

Exit criterion:

~~~text
common prefix n
  -> ternary distance <= 3^(-n)

first difference n
  -> explicit ternary separation lower bound
~~~

### v4.36 — forward Hölder transport and upper dimension bound

Prove the binary-to-ternary coding map is Hölder with the scale exponent logb 2 3, then derive:

~~~text
dimH cantorSet <= logb 3 2
~~~

### v4.37 — inverse Hölder transport and lower dimension bound

Prove the inverse coding map on cantorSet is Hölder with exponent logb 3 2, then derive:

~~~text
logb 3 2 <= dimH cantorSet
~~~

### v4.38 — exact Cantor dimension

Close:

~~~text
dimH cantorSet = logb 3 2 = log 2 / log 3
~~~

Then transport the value through branch translations and the finite branch union.

## Long-range Dependent Origination Universality Program

The long-range target remains an explicitly constructed carrier with a genuine mapping property:

~~~text
eta : C ⟶ DO(C, W, J, H)

AdmissibleContextualSystems(C, X)
  ≃ Fun(DO(C, W, J, H), X)
~~~

with correct higher variance, coherent factorization, essential uniqueness, naturality, descent compatibility, presentation invariance, and explicit obstruction/correction semantics.

The current fractal construction is a formally validated recursive/metric carrier program. It is not yet the final universal object.

## Proof-engineering rules retained

Recent v4.x work reinforces these rules:

- **Fresh GitHub authority first.**
- **Import is not open.**
- **Module/file names are not namespace names.**
- **Local attributes remain local.**
- **Keep autoImplicit false.**
- **Reserved words are not ordinary identifiers.** Prefer semantic names over escaped keywords.
- **Do not rely on broad rw occurrence selection.** Prefer typed equalities, calc, congrArg, or simpa only.
- **Definitional equality is narrower than mathematical equality.** Use theorem-level conversions for division/inverse, casts, and scalar actions.
- **Nat scalar action is not definitionally multiplication.** Normalize with nsmul_eq_mul where appropriate.
- **Do not shadow existing measurable-space instances.** Instance diamonds can change theorem types.
- **Give tactic terms expected types.**
- **Use eqToIso / eqToHom for dependent transport.**
- **Keep categorical composition until the dependent carrier is fixed.**
- **Every code change invalidates old-head CI receipts.**
- **Merge only the validated current head SHA.**

## No-go implications

Do not promote these implications without theorem support:

~~~text
weak admissibility -> HigherLocalizationFactorization
one bad gauge -> every gauge fails
local pentagram odd parity -> global obstruction
capacity embedding -> canonical semantic transport

finite recursive combinatorics -> metric fractal theorem

eight-point inverse limit + new metric
  -> positive Hausdorff dimension
  [false: the set remains finite]

positive-dimensional segment branch carrier
  -> exact Cantor dimension

Cantor self-similarity + Hausdorff convergence
  -> dimH cantorSet = log 2 / log 3

dimH binary Cantor space = 1
  -> exact ternary Cantor dimension
  [requires quantitative Hölder transport]

runtime success -> theorem authority
docs-only CI -> theorem validation
history / memory -> fresh GitHub authority
~~~

## Reproduction

Focused theorem targets:

~~~bash
lake -KleanArgs=-DwarningAsError=true   -KleanArgs=-DsorryAsError=true   build KUOS.DependentOriginationAbstractNonfactorizationV4_00

lake -KleanArgs=-DwarningAsError=true   -KleanArgs=-DsorryAsError=true   build KUOS.DependentOriginationStageIIObstructionClassV4_12

lake -KleanArgs=-DwarningAsError=true   -KleanArgs=-DsorryAsError=true   build KUOS.DependentOriginationMiddleSwitchPairIncidenceV4_19

lake -KleanArgs=-DwarningAsError=true   -KleanArgs=-DsorryAsError=true   build KUOS.DependentOriginationStageIISetTheoreticInverseLimitV4_26

lake -KleanArgs=-DwarningAsError=true   -KleanArgs=-DsorryAsError=true   build KUOS.DependentOriginationStageIICurrentHausdorffDimensionZeroV4_28

lake -KleanArgs=-DwarningAsError=true   -KleanArgs=-DsorryAsError=true   build KUOS.DependentOriginationStageIIBranchingPositiveHausdorffV4_29

lake -KleanArgs=-DwarningAsError=true   -KleanArgs=-DsorryAsError=true   build KUOS.DependentOriginationStageIIGeometricFractalLimitV4_32

lake -KleanArgs=-DwarningAsError=true   -KleanArgs=-DsorryAsError=true   build KUOS.DependentOriginationBinaryCantorHausdorffDimensionV4_33

lake -KleanArgs=-DwarningAsError=true   -KleanArgs=-DsorryAsError=true   build KUOS.DependentOriginationCantorCriticalExponentV4_34
~~~

Aggregate formal target:

~~~bash
lake -KleanArgs=-DwarningAsError=true   -KleanArgs=-DsorryAsError=true   build KuuOSFormal
~~~

Runtime validation remains separate:

~~~bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

A runtime result is not a theorem. A docs-only gate is not theorem validation. A CI receipt applies only to its recorded exact head.

## Current research sentence

**KuuOS now carries the proved transport-independent Stage-II obstruction from the finite octahedral countermodel through an incidence-compatible truncated-icosahedral carrier, every finite central-cell refinement depth, and a rigid set-theoretic inverse limit. That rigid inverse limit is finite and therefore Hausdorff-dimension zero; adding genuine branch freedom produces a dimension-one ambient carrier, inside which translated Cantor fibers form a compact, closed, exactly self-similar geometric limit reached by explicit Hausdorff-metric convergence. The current v4.33–v4.34 frontier normalizes the binary Cantor source at Hausdorff dimension one and proves the critical exponent algebra s = log 2 / log 3. The next theorem work is the quantitative Hölder transport needed to prove the real Cantor limit itself has exact Hausdorff dimension s, without inferring that value from self-similarity alone.**
