# KuuOS / 空OS Roadmap

**Theorem baseline: 2026-09-26 JST · integrated through v4.40**

This roadmap records proved results, authority boundaries, theorem-sized exit criteria, and the next formal steps. It is subordinate to fresh GitHub theorem authority.

## 0. Authority and canonical state

Repository:

~~~text
itakura-hidetoshi/KuuOS
~~~

Canonical branch:

~~~text
main
~~~

Current theorem-bearing baseline:

~~~text
c16b0f105cfb5df45ac2044e51b9744d59a3982d
~~~

Latest theorem-bearing merge:

~~~text
PR #1834
Bundle exact Stage-II geometric fractal certificate v4.40
~~~

Validated v4.40 head:

~~~text
bc86cf1d5e734d8117577c9cb5fed56e364f12ca
~~~

Exact-head governance run:

~~~text
36236264821
completed / success
~~~

Authority order:

~~~text
1. fresh exact GitHub canonical SHA
2. formal Lean theorem artifacts at that SHA
3. README / ROADMAP
4. exact-head CI/runtime receipts
5. history / memory
~~~

Pinned formal environment:

~~~text
Lean    leanprover/lean4:v4.30.0-rc2
Mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6
~~~

A docs-only merge may advance `main` beyond the theorem-bearing baseline without changing mathematical authority.

Protected Lean 4.31 validation-only PR:

~~~text
#1558
open
Draft = true
merged = false
head = 3a09839782ea82661ddbf8e13a0fd08e893079b4
base = validation/lean431-v131-explicit-E-v6
base SHA = 624f04110390bb97b187f212ac1dfd55b1f24077
~~~

#1558 remains outside theorem authority and must not be merged, marked Ready for review, or auto-merged.

## 1. Long-range target

The long-range target remains a dependent-origination carrier with a genuine mapping property:

~~~text
eta : C ⟶ DO(C, W, J, H)

AdmissibleContextualSystems(C, X)
  ≃ Fun(DO(C, W, J, H), X)
~~~

Required ingredients include:

- correct higher variance;
- coherent factorization;
- essential uniqueness;
- naturality;
- descent compatibility;
- presentation invariance;
- explicit obstruction/correction semantics;
- explicit separation between theorem authority and runtime/operational authority.

A quotient, recursive carrier, inverse limit, metric fractal, or obstruction witness is not promoted to the final universal object without the required mapping property.

## 2. Closed obstruction spine — v4.00 through v4.12

### v4.00 — abstract nonfactorization

The concrete finite octahedral C2 countermodel satisfies:

~~~lean
IsEmpty
  (HigherLocalizationFactorization
    (W := allMorphisms) counterSystem)
~~~

No arbitrary factorization can absorb the countermodel.

### v4.01–v4.07 — weak principles, sufficient sectors, and authority boundary

Weak allMorphisms-admissibility does not imply arbitrary higher-localization factorization.

The countermodel lies outside the earlier positive thin/trivial sectors. Nonidentity invertible isotropy is explicit, the five-defect obstruction is gauge-independent, and objects indexed by a hypothetical factorization are vacuous on `counterSystem`.

Recursive work therefore proceeds from pre-factorization data.

### v4.08–v4.12 — exact Stage-II obstruction

The exact operational sequence is:

~~~text
coherent quotient transport               EXISTS
quotient coboundary solution               EXISTS
comparison-gauge / presentation lift       IMPOSSIBLE
full generated correction                  IMPOSSIBLE
HigherLocalizationFactorization            IMPOSSIBLE
~~~

For every coherent quotient transport:

~~~text
omega(T) = 1 in ZMod 2
~~~

Any successful comparison would force `omega(T)=0`.

## 3. Finite carrier and incidence geometry — v4.13 through v4.22

### v4.13–v4.19

Proved:

- pentagram/hexagram parity contrast;
- uniform global cancellation;
- an explicit eight-label Stage-II parity carrier;
- global capacity for eight labels;
- local one-star capacity obstruction;
- an incidence-compatible placement whose middle-switch mates land on adjacent pentagon/hexagon seed faces with opposite face kinds.

### v4.20–v4.22

The actual Stage-II scalar values are pushed through the incidence placement with source provenance.

Orientation is formalized in two layers:

~~~text
mod 2:
  forward = reverse

integer lift:
  forward = +1
  reverse = -1
~~~

The integer representative reduces to the original mod-2 value while retaining orientation-sensitive nonzero mismatch.

## 4. Recursive transport and inverse limit — v4.23 through v4.27

### v4.23 — one recursive central-cell step

Each globally placed seed face is refined independently to its central child.

### v4.24 — all finite depths

For every depth:

~~~text
root provenance stable
face kind stable
boundary arity stable
orientation stable
integer representative stable
total stable
mismatch stable
mod-2 mismatch = omega(T) = 1
~~~

### v4.25 — coherent finite-depth tower

Strict restriction maps preserve the representative, total, and mismatch.

### v4.26 — set-theoretic inverse limit

The supported compatible-section carrier satisfies:

~~~text
OctahedralStageIIParityFace
  ≃
StageIIFiniteDepthInverseLimit
~~~

Every inverse-limit point has one unique source label.

### v4.27 — middle-switch involution

The source mate involution transports to the inverse limit and remains:

- involutive;
- injective;
- fixed-point-free;
- opposite-kind;
- opposite-orientation;
- compatible with every finite depth.

## 5. Metric phase — v4.28 through v4.32

### v4.28 — rigid current carrier has dimension zero

The current inverse-limit carrier contains exactly eight points.

Therefore, for every extended metric structure:

~~~text
dimH XInfinityCurrent = 0
~~~

Key boundary:

~~~text
re-metrize the same finite carrier
  !=>
positive Hausdorff dimension
~~~

### v4.29 — ambient branch carrier has dimension one

A genuine new carrier is formed by retaining one nondegenerate real interval per inverse-limit point:

~~~text
dimH XInfinityBranch = 1
~~~

Positive dimension comes from new branch freedom.

### v4.30 — geometric Cantor skeleton

Each branch receives a translated classical ternary Cantor fiber.

Proved:

- compactness of every fiber;
- compactness and closedness of the global carrier;
- nonemptiness;
- exact ternary two-child self-similarity;
- inclusion in the dimension-one ambient branch carrier.

### v4.31 — Hausdorff metric convergence

The finite-depth approximants satisfy:

~~~text
d_H(X_n, X_infinity) <= 3^(-n)
d_H(X_n, X_infinity) -> 0
~~~

This is genuine Hausdorff convergence of sets.

### v4.32 — original geometric fractal-limit certificate

The v4.32 certificate packages:

- ambient Hausdorff dimension (1);
- compact / closed / nonempty limit topology;
- ambient inclusion;
- branchwise self-similarity;
- explicit Hausdorff-distance rate;
- Hausdorff convergence.

At v4.32 the exact Cantor dimension was intentionally left open.

## 6. Exact Cantor dimension program — v4.33 through v4.40

This phase is now complete.

### v4.33 — binary Cantor source has dimension one

Using mathlib's `PiNat` metric:

~~~text
dimH (Set.univ : Set (Nat -> Bool)) = 1
~~~

The lower bound uses a 1-Lipschitz binary positional expansion onto ([0,1]). The upper bound uses canonical binary-cylinder covers.

### v4.34 — critical exponent algebra

Define:

~~~text
s = logb 3 2
  = log 2 / log 3
~~~

Proved:

~~~text
0 < s < 1
3^s = 2
s * logb 2 3 = 1
(logb 2 3)^(-1) = s
1 < logb 2 3
~~~

### v4.35 — canonical coding and common-prefix estimate

The explicit binary-to-ternary (0/2) digit map is identified with mathlib's canonical Cantor equivalence.

Proved:

~~~text
binaryToTernaryCantor injective
range binaryToTernaryCantor = cantorSet

common prefix length n
  -> dist(F x, F y) <= 3^(-n)
~~~

### v4.36 — forward Hölder transport

With:

~~~text
alpha = logb 2 3
~~~

prove:

~~~text
((1/2)^n)^alpha = (1/3)^n
HolderWith 1 alpha binaryToTernaryCantor
~~~

Hence:

~~~text
dimH cantorSet <= s
~~~

### v4.37 — inverse Hölder transport

The first differing digit gives:

~~~text
first difference at n
  -> 3^(-(n+1)) <= dist(F x, F y)
~~~

The inverse code on the Cantor subtype is:

~~~text
HolderWith 2 s cantorSetToBinary
~~~

Hence:

~~~text
s <= dimH cantorSet
~~~

### v4.38 — exact classical Cantor dimension

Close:

~~~text
dimH cantorSet = s
dimH cantorSet = ENNReal.ofReal (log 2 / log 3)
(dimH cantorSet).toReal = log 2 / log 3
~~~

This is a theorem obtained from quantitative forward and inverse transport, not from self-similarity alone.

### v4.39 — exact Stage-II geometric dimension

Stage-II branch translation is an isometry.

Therefore:

~~~text
forall x,
  dimH (stageIIGeometricCantorFiber x) = s
~~~

Using `dimH_iUnion` over the finite branch-index type:

~~~text
dimH XInfinityGeometricFractal = s
(dimH XInfinityGeometricFractal).toReal
  = log 2 / log 3
~~~

Also:

~~~text
dimH XInfinityGeometricFractal
  < dimH XInfinityBranch
  = 1
~~~

### v4.40 — exact geometric-fractal certificate

The v4.32 certificate remains unchanged and is embedded as `legacy`.

The additive v4.40 certificate adds:

~~~text
exact dimension of every branch fiber
exact dimension of the full geometric limit
real logarithmic dimension value
strict dimension gap below the ambient carrier
~~~

This closes the original exact-Cantor-dimension program.

## 7. Current formal frontier — finite approximants and dimension jump

The next question is not the dimension of the limit; that is now closed. The next question is the dimension of the **finite-depth approximants**.

### v4.41 — finite prefix factorization and zero-dimensional approximants

The definition:

~~~text
stageIICantorPartial n t
  = sum of the first n ternary digit terms
~~~

depends only on a finite prefix.

The preferred formal route is to factor it through a finite code type, for example:

~~~text
Fin n -> Fin 3
~~~

or, more sharply, the subtype of allowed (0/2) Cantor prefixes.

Required exit facts:

~~~text
(stageIIGeometricApproxFiber n x).Finite

(XInfinityGeometricApprox n).Finite

dimH (stageIIGeometricApproxFiber n x) = 0

dimH (XInfinityGeometricApprox n) = 0
~~~

The final dimension proof should use:

~~~text
Set.Finite.dimH_zero
~~~

after the finite-image theorem is established.

Do not argue informally that "there are only finitely many prefixes"; expose the finite factorization in Lean.

### v4.42 — concrete Hausdorff-limit dimension jump

Combine v4.31, v4.39, and v4.41:

~~~text
forall n,
  dimH (XInfinityGeometricApprox n) = 0

hausdorffDist
  (XInfinityGeometricApprox n)
  XInfinityGeometricFractal
    <= 3^(-n)

hausdorffDist (...) -> 0

dimH XInfinityGeometricFractal
  = log 2 / log 3
  > 0
~~~

Exit criterion: one theorem/certificate recording that these zero-dimensional finite approximants converge in Hausdorff distance to a positive-dimensional limit.

This is a concrete internal example of non-continuity of Hausdorff dimension under Hausdorff convergence.

## 8. Candidate later metric/fractal questions

Only after v4.41–v4.42 should the next quantitative direction be selected.

Candidate theorem-sized programs:

### M1 — critical Hausdorff measure

Investigate whether the development can prove nonzero/finite critical (s)-dimensional Hausdorff measure for the classical or translated Cantor carrier.

No such claim is current authority.

### M2 — middle-switch geometry

Ask whether the v4.27 middle-switch involution extends canonically from branch indices to the Cantor fibers or to the full geometric limit.

Required before promotion:

- explicit map;
- preservation of Cantor membership;
- involution theorem;
- metric/topological behavior;
- compatibility with branch provenance.

### M3 — orientation as geometric symmetry

Ask whether the integer orientation lift from v4.22 can act by a genuine geometric symmetry on branch fibers.

### M4 — obstruction class on the metric limit

Investigate whether the Stage-II obstruction induces a nontrivial cocycle or other invariant on the limiting fractal geometry.

### M5 — presentation invariance

Separate coordinate choices such as branch offsets from invariant metric/fractal content.

None of M1–M5 is currently proved.

## 9. Return to the Dependent Origination Universality Program

The recursive/fractal spine remains evidence and infrastructure, not the final universality theorem.

Long-range tasks still include:

1. define the candidate universal object with explicit variance;
2. construct the unit / comparison map;
3. state the exact class of admissible contextual systems;
4. prove existence of factorization in the positive sector;
5. prove essential uniqueness;
6. prove naturality;
7. prove descent compatibility;
8. state presentation invariance precisely;
9. locate the octahedral obstruction within the final universal-property framework;
10. preserve the authority distinction between mathematical truth, formal validation, and runtime operation.

## 10. Positive sufficient-condition program remains valid

The octahedral counterexample does not invalidate positive results under stronger hypotheses.

Still-valid sufficient sectors include:

- fiber hom-thinness;
- fiber functor 2-thinness;
- fiber functor iso-thinness;
- thin fiber cores;
- trivial automorphism groups;
- canonical five-defect gauge trivialization;
- other explicit coherence / separation / descent hypotheses.

The general question remains:

> Which minimal additional hypotheses exclude the octahedral obstruction while retaining useful nontrivial models?

## 11. Proof-engineering constraints

### P1 — fresh authority

Re-observe exact current branch and SHA before branch creation, writes, CI judgment, and merge.

### P2 — exact-head CI

Every write invalidates previous-head receipts. Merge only the currently validated head SHA.

### P3 — imports and namespaces

Importing a module does not open its namespace. Filenames are not namespace names.

### P4 — local attributes

Imported local simp attributes and local instances do not propagate.

### P5 — expected types

Give tactic terms explicit expected types when elaboration is delicate.

### P6 — rewrite discipline

Broad `rw` or `simp` can rewrite the wrong occurrence or normalize in an unexpected direction.

Prefer:

~~~text
typed local equality
calc
congrArg
funext
simpa only
~~~

when target selection matters.

### P7 — commutativity is not an arbitrary rewrite oracle

Do not expect:

~~~text
simp [add_comm]
~~~

to orient every commutative expression in the direction desired by the proof.

For equality between functions whose bodies differ by commutativity, establish the function equality explicitly with `funext` and then rewrite.

### P8 — semantic facts use semantic lemmas

Do not expect simplification to prove semantic inequalities such as nonnegativity of real powers.

Use the corresponding theorem, e.g. `Real.rpow_nonneg` or `Real.zero_rpow_nonneg`.

### P9 — equality composition

Lean 4 uses:

~~~text
Eq.trans
h₁.trans h₂
~~~

Do not assume non-existent variants such as `Eq.trans'`.

### P10 — definitional equality is narrow

Mathematically equal forms need not be definitionally equal.

Examples include:

~~~text
1 / 2
vs
2^(-1)

Nat scalar action  n • a
vs
multiplication      (n : α) * a

explicit coding
vs
subtype value of an equivalence
~~~

Use theorem-level conversions rather than forcing `change` when definitional equality is absent.

### P11 — instance discipline

Do not shadow existing measurable-space instances or introduce avoidable instance diamonds.

### P12 — dependent transport

Prefer `eqToIso` / `eqToHom` when transporting dependent categorical data.

### P13 — authority boundary

Runtime success, docs-only CI, stale receipts, and history are not theorem authority.

## 12. No-go rules

Do not promote these implications without theorem support:

~~~text
weak admissibility -> HigherLocalizationFactorization
weak admissibility -> weak universal property

nontrivial holonomy -> quotient transport failure
one bad gauge -> every gauge fails

local pentagram odd parity -> global obstruction
uniform cancellation -> all nonuniform transports cancel
capacity embedding -> semantic transport
incidence placement -> canonicality

finite combinatorial recursion -> metric fractal theorem

finite eight-point inverse limit + arbitrary new metric
  -> positive Hausdorff dimension

positive-dimensional interval branching
  -> exact Cantor dimension

Cantor self-similarity alone
  -> dimH = log 2 / log 3

Hausdorff convergence alone
  -> preservation or continuity of Hausdorff dimension

finite approximants converging in Hausdorff distance
  -> approximant dimensions converge to limit dimension

runtime success -> theorem authority
docs-only CI -> theorem validation
history / memory -> fresh GitHub authority
~~~

The exact Cantor dimension is now established independently by quantitative Hölder transport, so the no-go rule concerning self-similarity remains conceptually important.

## 13. Verification commands

Focused current theorem targets:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationAbstractNonfactorizationV4_00

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationStageIIObstructionClassV4_12

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationStageIISetTheoreticInverseLimitV4_26

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationStageIICurrentHausdorffDimensionZeroV4_28

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationStageIIBranchingPositiveHausdorffV4_29

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

## 14. Current completion boundary

Canonically proved:

~~~text
v4.00
abstract nonfactorization

v4.01-v4.12
weak-principle failure, isotropy, gauge independence,
exact comparison-lift obstruction, omega(T)=1

v4.13-v4.22
finite parity carrier, incidence-compatible placement,
scalar pushforward, mod-2 orientation collapse,
integer orientation-sensitive lift

v4.23-v4.27
recursive preservation at every finite depth,
coherent tower, inverse limit, middle-switch involution

v4.28
rigid current inverse-limit dimH = 0

v4.29
ambient branch carrier dimH = 1

v4.30-v4.32
compact self-similar Cantor geometry,
Hausdorff-metric convergence,
legacy geometric fractal-limit certificate

v4.33
binary Cantor source dimH = 1

v4.34
critical exponent s = log 2 / log 3
and exact scale algebra

v4.35-v4.37
explicit binary/ternary coding,
forward Hölder transport,
inverse separation and inverse Hölder transport

v4.38
exact classical cantorSet dimension
= log 2 / log 3

v4.39
exact translated branch-fiber dimension
and exact global Stage-II geometric Cantor dimension

v4.40
additive exact geometric-fractal certificate
preserving v4.32 as legacy
~~~

Immediate open theorem:

~~~text
prove every finite-depth geometric approximant is finite
and therefore Hausdorff-dimension zero
~~~

Next synthesis after that:

~~~text
zero-dimensional X_n
  --Hausdorff distance -> 0-->
positive-dimensional X_infinity

dimH X_infinity = log 2 / log 3
~~~
