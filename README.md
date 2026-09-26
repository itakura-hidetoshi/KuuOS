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
| Current theorem-bearing baseline | **c16b0f105cfb5df45ac2044e51b9744d59a3982d** |
| Canonical theorem frontier | **v4.40 — exact Stage-II geometric fractal certificate** |
| Latest theorem-bearing merge | **PR #1834**, Bundle exact Stage-II geometric fractal certificate v4.40 |
| v4.40 validated PR head | **bc86cf1d5e734d8117577c9cb5fed56e364f12ca** |
| v4.40 exact-head governance run | **36236264821**, completed / success |
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

A documentation-only merge may advance `main` beyond the theorem-bearing baseline without changing mathematical authority. The theorem-bearing baseline above therefore remains the reference even if README / ROADMAP are subsequently merged by a docs-only PR.

The separate Lean 4.31 validation-only PR **#1558** remains:

~~~text
open
Draft = true
merged = false
head = 3a09839782ea82661ddbf8e13a0fd08e893079b4
base = validation/lean431-v131-explicit-E-v6
base SHA = 624f04110390bb97b187f212ac1dfd55b1f24077
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

The current theorem spine is now closed from the finite octahedral obstruction through an exact-dimension Stage-II Cantor fractal certificate.

### v4.00–v4.12 — abstract nonfactorization and exact obstruction

KuuOS proves for the concrete finite octahedral C2 countermodel:

~~~lean
IsEmpty
  (HigherLocalizationFactorization
    (W := allMorphisms) counterSystem)
~~~

The exact operational picture is:

~~~text
weak admissibility                         EXISTS
coherent quotient transport               EXISTS
quotient three-face coboundary             SOLVABLE
comparison / presentation lift             IMPOSSIBLE
full generated correction                  IMPOSSIBLE
HigherLocalizationFactorization            IMPOSSIBLE
~~~

v4.12 extracts the transport-independent Stage-II scalar class

~~~text
omega(T) = 1 in ZMod 2
~~~

for every coherent quotient transport `T). Any successful comparison would force `omega(T)=0`.

### v4.13–v4.22 — finite carrier, incidence geometry, and orientation lift

The obstruction is placed on an explicit eight-label Stage-II carrier and transported through an incidence-compatible truncated-icosahedral placement.

Proved highlights:

- pentagram/hexagram parity contrast;
- global uniform cancellation versus local odd parity;
- eight-label global capacity and one-star local-capacity obstruction;
- middle-switch mates placed on adjacent opposite-kind seed faces;
- actual Stage-II scalar values pushed with source provenance;
- orientation signs collapse mod 2;
- an integer lift records forward (+1) and reverse (-1) while reducing mod 2 to the original class.

### v4.23–v4.27 — recursive transport and inverse limit

The Stage-II representative is transported through recursive central-cell refinements.

At every finite depth:

~~~text
source provenance stable
face kind stable
boundary arity stable
orientation stable
integer representative stable
total stable
mismatch stable
mod-2 mismatch = omega(T) = 1
~~~

The depth-indexed cells form a coherent restriction tower. Its supported set-theoretic inverse limit satisfies:

~~~text
OctahedralStageIIParityFace
  ≃
StageIIFiniteDepthInverseLimit
~~~

Hence every compatible inverse-limit point has a unique source label. The middle-switch involution transports to the inverse limit and remains involutive, injective, fixed-point-free, opposite-kind, and opposite-orientation.

## v4.28–v4.32 — metric and geometric phase

### v4.28 — rigid inverse-limit carrier has dimension zero

The current inverse-limit carrier has exactly eight points, so for every extended metric structure:

~~~text
dimH XInfinityCurrent = 0
~~~

This is an intrinsic finiteness result, not a metric artifact.

### v4.29 — ambient branching carrier has dimension one

Each of the eight current points is thickened by a nondegenerate real interval:

~~~text
dimH XInfinityBranch = 1
0 < dimH XInfinityBranch
~~~

Positive Hausdorff dimension appears only after genuine branch freedom is added.

### v4.30 — translated ternary Cantor geometry

Each Stage-II branch carries a translated copy of the classical ternary Cantor set.

The global geometric carrier is:

~~~text
XInfinityGeometricFractal
  = ⋃ x, stageIIGeometricCantorFiber x
~~~

Proved:

- compactness of every translated fiber;
- compactness, closedness, and nonemptiness of the global carrier;
- exact two-child ternary self-similarity branchwise;
- inclusion in the dimension-one ambient branch carrier.

### v4.31 — Hausdorff metric convergence

Finite ternary approximants satisfy:

~~~text
dist(approx_n, limit) <= 3^(-n)
hausdorffDist(X_n, X_infinity) <= 3^(-n)
hausdorffDist(X_n, X_infinity) -> 0
~~~

This is genuine set convergence in Hausdorff distance.

### v4.32 — original geometric fractal-limit certificate

v4.32 packages:

- ambient branch dimension (1);
- compact / closed / nonempty topology;
- inclusion in the ambient branch carrier;
- exact branchwise ternary self-similarity;
- explicit Hausdorff-distance rate;
- Hausdorff metric convergence.

At v4.32 the exact Cantor dimension was intentionally *not* inferred from self-similarity alone.

## v4.33–v4.40 — exact Cantor dimension and exact Stage-II fractal certificate

### v4.33 — normalized binary Cantor source has exact dimension one

Using mathlib's `PiNat` metric on `Nat → Bool`:

~~~text
dimH (Set.univ : Set (Nat -> Bool)) = 1
~~~

The lower bound is obtained from a 1-Lipschitz binary expansion onto the real unit interval. The upper bound uses the canonical length-(n) binary-cylinder cover.

### v4.34 — critical Cantor exponent algebra

Define:

~~~text
s = logb 3 2 = log 2 / log 3
~~~

Proved:

~~~text
0 < s < 1
3^s = 2
s * logb 2 3 = 1
(logb 2 3)^(-1) = s
1 < logb 2 3
~~~

### v4.35 — canonical binary-to-ternary coding and prefix estimate

The explicit (0/2)-digit ternary code is identified with mathlib's canonical Cantor equivalence.

Proved:

~~~text
binaryToTernaryCantor is injective
range binaryToTernaryCantor = cantorSet
common binary prefix of length n
  -> dist(real Cantor images) <= 3^(-n)
~~~

### v4.36 — forward Hölder transport

For the forward exponent

~~~text
alpha = logb 2 3
~~~

the exact scale identity is formalized:

~~~text
((1/2)^n)^alpha = (1/3)^n
~~~

and the canonical code is proved:

~~~text
HolderWith 1 alpha binaryToTernaryCantor
~~~

Hence:

~~~text
dimH cantorSet <= s
~~~

### v4.37 — inverse Hölder transport and lower dimension bound

The first differing binary digit gives a genuine ternary separation estimate:

~~~text
first difference at n
  -> 3^(-(n+1)) <= dist(real Cantor images)
~~~

The inverse code on the Cantor-set subtype is then proved Hölder with coefficient (2) and exponent (s):

~~~text
HolderWith 2 s cantorSetToBinary
~~~

Hence:

~~~text
s <= dimH cantorSet
~~~

### v4.38 — exact classical ternary Cantor dimension

The matching inequalities close the exact theorem:

~~~text
dimH cantorSet = s
dimH cantorSet = ENNReal.ofReal (log 2 / log 3)
(dimH cantorSet).toReal = log 2 / log 3
~~~

Thus the classical value is formally proved, not imported from self-similarity.

### v4.39 — exact dimension of every Stage-II Cantor fiber and the global union

Translation by the Stage-II branch offset is proved to be an isometry. Therefore every translated fiber has the classical exact dimension:

~~~text
dimH (stageIIGeometricCantorFiber x) = s
~~~

Using `dimH_iUnion` over the finite eight-branch index type:

~~~text
dimH XInfinityGeometricFractal = s
(dimH XInfinityGeometricFractal).toReal = log 2 / log 3
~~~

The geometric carrier is strictly lower-dimensional than its ambient branch carrier:

~~~text
dimH XInfinityGeometricFractal
  < dimH XInfinityBranch
  = 1
~~~

### v4.40 — additive exact geometric fractal certificate

The original v4.32 certificate is preserved unchanged as a `legacy` field.

The v4.40 certificate adds:

- exact dimension of every translated Cantor fiber;
- exact dimension of the full geometric carrier;
- the real value (log 2 / log 3);
- strict dimension drop below the ambient branch carrier.

Thus one authority-bearing object now carries both the original topology/metric convergence package and the exact Cantor dimension.

## Current exact frontier

Canonically proved through v4.40:

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
  exactly 8 points
  Hausdorff dimension 0 for every extended metric structure

ambient branch carrier:
  Hausdorff dimension exactly 1

classical ternary Cantor set:
  dimH = logb 3 2 = log 2 / log 3

geometric Stage-II Cantor carrier:
  compact
  closed
  nonempty
  exact branchwise ternary self-similarity
  Hausdorff-distance rate <= 3^(-n)
  Hausdorff convergence
  every translated branch fiber has exact dimension log 2 / log 3
  global eight-branch union has exact dimension log 2 / log 3
  strict dimension drop below ambient dimension 1

exact v4.40 certificate:
  preserves the v4.32 certificate as legacy
  adds exact fiber/global dimension
  adds real logarithmic value
  adds strict ambient dimension gap
~~~

## Immediate next theorem sequence

The exact Cantor-dimension program is complete. The natural next quantitative question concerns the **finite-depth approximants themselves**.

### v4.41 — finite-depth approximants are finite and zero-dimensional

The definition

~~~text
stageIICantorPartial n t
~~~

uses only the first (n) ternary digits. The next theorem unit should factor this construction through a finite prefix type such as `Fin n → Fin 3` (or the corresponding allowed (0/2)-digit subtype).

Target facts:

~~~text
(stageIIGeometricApproxFiber n x).Finite
(XInfinityGeometricApprox n).Finite

dimH (stageIIGeometricApproxFiber n x) = 0
dimH (XInfinityGeometricApprox n) = 0
~~~

The proof should use finiteness of prefix codes plus `Set.Finite.dimH_zero`, not a cardinality argument external to Lean.

### v4.42 — Hausdorff-limit dimension jump

Combine v4.31, v4.39, and v4.41 into a single theorem:

~~~text
forall n,
  dimH (XInfinityGeometricApprox n) = 0

hausdorffDist (XInfinityGeometricApprox n)
  XInfinityGeometricFractal <= 3^(-n)

hausdorffDist (...) -> 0

dimH XInfinityGeometricFractal
  = log 2 / log 3
  > 0
~~~

This records explicitly that Hausdorff dimension need not be continuous under Hausdorff convergence in this concrete Stage-II construction.

### After v4.42

Possible theorem-sized continuations include:

1. quantitative critical Hausdorff-measure information for the Cantor limit;
2. extension of the middle-switch involution to the Cantor branch geometry;
3. interaction between the integer orientation lift and geometric symmetries;
4. a cocycle or obstruction class on the metric limit;
5. presentation invariance of the metric/fractal data;
6. integration of the recursive/fractal carrier into the long-range dependent-origination universal-property program.

These are open directions, not current theorems.

## Long-range Dependent Origination Universality Program

The long-range target remains an explicitly constructed carrier with a genuine mapping property:

~~~text
eta : C ⟶ DO(C, W, J, H)

AdmissibleContextualSystems(C, X)
  ≃ Fun(DO(C, W, J, H), X)
~~~

with correct higher variance, coherent factorization, essential uniqueness, naturality, descent compatibility, presentation invariance, and explicit obstruction/correction semantics.

The current recursive/fractal construction is a formally validated carrier program. It is not yet the final universal object.

## Proof-engineering rules retained

Recent v4.x work reinforces these rules:

- **Fresh GitHub authority first.**
- **Every code change invalidates old-head CI receipts.**
- **Merge only the validated current head SHA.**
- **Import is not open.**
- **Module/file names are not namespace names.**
- **Local attributes remain local.**
- **Keep `autoImplicit false`.**
- **Give tactic terms expected types when elaboration is delicate.**
- **Definitional equality is narrower than mathematical equality.**
- **Prefer typed local equalities, `calc`, `congrArg`, `funext`, and `simpa only` when rewrite targets matter.**
- **Do not rely on broad `simp` to choose the direction of commutative rewrites.** For function equality, prove the function equality explicitly with `funext`.
- **Use semantic lemmas for semantic facts.** For example, real-`rpow` nonnegativity should use the corresponding theorem rather than expecting `simp` to derive it.
- **Use standard equality composition.** Lean 4 provides `Eq.trans` / `h₁.trans h₂`; do not assume non-existent variants such as `Eq.trans'`.
- **Nat scalar action is not definitionally multiplication.** Normalize with `nsmul_eq_mul` where appropriate.
- **Do not shadow existing measurable-space instances.** Instance diamonds can change theorem types.
- **Use `eqToIso` / `eqToHom` for dependent transport.**
- **Keep categorical composition until the dependent carrier is fixed.**

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

Cantor self-similarity alone
  -> dimH = log 2 / log 3

Hausdorff convergence alone
  -> preservation or continuity of Hausdorff dimension

runtime success -> theorem authority
docs-only CI -> theorem validation
history / memory -> fresh GitHub authority
~~~

The exact Cantor dimension is now proved by quantitative forward and inverse Hölder transport; it is not an exception to these no-go rules.

## Reproduction

Focused theorem targets:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationAbstractNonfactorizationV4_00

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationStageIIObstructionClassV4_12

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationStageIISetTheoreticInverseLimitV4_26

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationStageIICurrentHausdorffDimensionZeroV4_28

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationStageIIGeometricFractalLimitV4_32

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationBinaryCantorHausdorffDimensionV4_33

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationCantorCriticalExponentV4_34

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationCantorCodingPrefixV4_35

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationCantorForwardHolderV4_36

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationCantorInverseHolderV4_37

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationCantorExactDimensionV4_38

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationStageIIExactCantorDimensionV4_39

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationStageIIExactFractalCertificateV4_40
~~~

Aggregate formal target:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
~~~

Runtime validation remains separate:

~~~bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

A runtime result is not a theorem. A docs-only gate is not theorem validation. A CI receipt applies only to its recorded exact head.

## Current research sentence

**KuuOS now carries the proved transport-independent Stage-II obstruction from the finite octahedral countermodel through an incidence-compatible carrier, every finite recursive refinement depth, and a rigid eight-point inverse limit. Genuine branch freedom produces a dimension-one ambient carrier. Inside it, eight translated ternary Cantor fibers form a compact, closed, exactly self-similar Hausdorff-metric limit. The binary/ternary coding has now been quantitatively formalized in both directions, proving the classical and Stage-II geometric Cantor dimension exactly as `log 2 / log 3`. v4.40 bundles this exact value together with the earlier topology, self-similarity, inclusion, convergence rate, and Hausdorff convergence while preserving the v4.32 certificate unchanged. The next formal frontier is the finite-depth side of the same geometry: prove each approximant is finite and zero-dimensional, then formalize the concrete jump from zero-dimensional approximants to a positive-dimensional Hausdorff limit.**
