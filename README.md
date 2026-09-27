# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, correction, recursive carriers, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

Its central mathematical question is:

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, what obstructs that process, and which universal property characterizes the invariant content?

Philosophical interpretation, mathematical presentation, formal proof, runtime validation, and operational authority are related but deliberately kept as distinct evidence classes.

## Canonical theorem snapshot — 2026-09-27 JST

| Item | Current reference |
| --- | --- |
| Canonical branch | **main** |
| Current theorem-bearing baseline | **5b55a205baeba7c3f8dfbb09ade21fa5e5b5304c** |
| Canonical theorem frontier | **v4.50 — exact higher dependent-origination positive sector** |
| Latest theorem-bearing merge | **PR #1847**, exact higher presentation sector v4.50 |
| Companion v4.50 merge | **PR #1846**, exact higher admissible sector v4.50 |
| Lean | **leanprover/lean4:v4.30.0-rc2** |
| Mathlib | **5450b53e5ddc75d46418fabb605edbf36bd0beb6** |

The theorem authority order is fixed:

~~~text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > CI/runtime receipts
  > history / memory
~~~

A code-changing head requires fresh validation. A byte-identical theorem replay onto an independent newer base may reuse the already validated theorem content after explicit blob and diff verification.

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

# Current mathematical status

The theorem spine now has a closed concrete verification program and an active general universality program:

~~~text
finite obstruction truth test
  -> recursive / geometric carrier verification
  -> presentation descent abstraction
  -> Cat-valued exact positive sector
  -> next: presentation-change invariance and essential uniqueness
~~~

## v4.00–v4.12 — abstract nonfactorization and exact Stage-II obstruction

For the concrete finite octahedral C2 countermodel, KuuOS proves:

~~~lean
IsEmpty
  (HigherLocalizationFactorization
    (W := allMorphisms) counterSystem)
~~~

The exact operational picture is:

~~~text
weak W-admissibility                     EXISTS
coherent quotient transport              EXISTS
quotient coboundary solution             EXISTS
comparison / presentation lift           IMPOSSIBLE
full generated correction                IMPOSSIBLE
HigherLocalizationFactorization          IMPOSSIBLE
~~~

v4.12 extracts the transport-independent class

~~~text
omega(T) = 1 in ZMod 2
~~~

for every coherent quotient transport T. Any successful comparison would force the incompatible value 0.

This is the core obstruction boundary used by the later general theory.

## v4.13–v4.27 — finite carrier, incidence geometry, recursion, inverse limit

The Stage-II class is placed on an explicit eight-label carrier and transported through incidence-compatible truncated-icosahedral geometry.

The development proves:

- pentagram/hexagram parity contrast;
- global uniform cancellation versus local odd parity;
- an eight-label global capacity theorem;
- a one-star local-capacity obstruction;
- middle-switch mates on adjacent pentagon/hexagon seed faces;
- scalar pushforward with source provenance;
- mod-2 orientation collapse;
- an integer orientation lift with forward +1 and reverse -1;
- preservation through every finite recursive central-cell depth;
- a coherent restriction tower;
- a set-theoretic inverse limit;
- a fixed-point-free middle-switch involution on that inverse limit.

The supported inverse limit satisfies:

~~~text
OctahedralStageIIParityFace
  ≃
StageIIFiniteDepthInverseLimit
~~~

so every compatible point has one unique source label.

## v4.28–v4.40 — metric and exact Cantor geometry

The rigid inverse-limit carrier has exactly eight points, hence:

~~~text
dimH XInfinityCurrent = 0
~~~

for every extended metric structure.

Positive dimension appears only after genuine new branch freedom is added:

~~~text
dimH XInfinityBranch = 1
~~~

Each branch then carries a translated ternary Cantor fiber. The global geometric carrier is:

~~~text
XInfinityGeometricFractal
  = ⋃ x, stageIIGeometricCantorFiber x
~~~

Proved properties include:

- compactness, closedness, nonemptiness;
- branchwise exact ternary two-child self-similarity;
- inclusion in the dimension-one ambient branch carrier;
- explicit Hausdorff-distance rate <= 3^(-n);
- Hausdorff convergence of finite approximants;
- exact classical ternary Cantor dimension;
- exact translated Stage-II fiber dimension;
- exact global geometric dimension.

The exact value is formally proved by quantitative forward and inverse Hölder transport:

~~~text
s = logb 3 2 = log 2 / log 3

dimH cantorSet = s

forall x,
  dimH (stageIIGeometricCantorFiber x) = s

dimH XInfinityGeometricFractal = s

dimH XInfinityGeometricFractal
  < dimH XInfinityBranch
  = 1
~~~

The v4.40 certificate preserves the earlier v4.32 topology/metric certificate as a legacy field and adds the exact dimensions.

## v4.41–v4.42 — finite approximants and Hausdorff-limit dimension jump

v4.41 factors finite approximants through finite prefix data and proves:

~~~text
(stageIIGeometricApproxFiber n x).Finite
(XInfinityGeometricApprox n).Finite

dimH (stageIIGeometricApproxFiber n x) = 0
dimH (XInfinityGeometricApprox n) = 0
~~~

v4.42 combines this with the v4.31 convergence and v4.39 exact limit dimension:

~~~text
forall n,
  dimH (XInfinityGeometricApprox n) = 0

hausdorffDist
  (XInfinityGeometricApprox n)
  XInfinityGeometricFractal
    <= 3^(-n)

hausdorffDist (...) -> 0

0 < dimH XInfinityGeometricFractal
dimH XInfinityGeometricFractal
  = log 2 / log 3
~~~

This is a concrete internal example in which Hausdorff dimension is not continuous under Hausdorff convergence.

## v4.43–v4.48 — geometric middle-switch, quotient, and descent

### v4.43 — tagged geometric symmetry

For each branch, the map

~~~text
y |-> y + (offset(mate x) - offset x)
~~~

is an isometry and continuous, sends the complete Cantor fiber exactly to its mate fiber, and composes with the mate translation to the identity.

A provenance-preserving tagged carrier receives a global involutive, injective, fixed-point-free middle-switch retaining finite-depth orientation data.

### v4.44 — descent to the bare real carrier

Distinct branch offsets are separated by at least two while Cantor coordinates lie in [0,1]. Therefore:

~~~text
distinct branch fibers are disjoint
every bare geometric point has one unique branch
~~~

The tagged and bare geometric carriers are equivalent, and the middle-switch descends to an actual involution of the bare carrier.

### v4.45 — self-homeomorphism

Different branch fibers are quantitatively separated by distance at least one.

The branch selector is locally constant, so the descended map is locally one fixed translation. Hence the bare middle-switch is continuous and packages as a fixed-point-free self-homeomorphism.

### v4.46 — orientation semantics on the homeomorphism

For every point p and finite depth n:

~~~text
O(M p,n) = flip(O(p,n))

epsilon(M p,n) = -epsilon(p,n)
~~~

while modulo two:

~~~text
[epsilon(M p,n)]_2
  = [epsilon(p,n)]_2
  = 1
~~~

The same homeomorphism retains opposite inner kind and pentagon-hexagon parent adjacency.

### v4.47 — exact two-point orbit quotient

The free involution defines a setoid and quotient. Every orbit is exactly:

~~~text
{p, M p}
~~~

with distinct representatives, and:

~~~text
[p] = [q]
  <-> q = p or q = M p
~~~

A semantic map factors uniquely through the orbit quotient exactly when it is middle-switch invariant.

### v4.48 — obstruction and orientation descent

Two complementary v4.48 theorem units are integrated.

The existing Stage-II obstruction descends to the geometric orbit quotient and remains:

~~~text
omega_geo(T,q) = 1 != 0
~~~

independent of coherent transport and representative.

The integer orientation semantic does not descend:

~~~text
epsilon(M p,n) = -epsilon(p,n)
epsilon(p,n) != 0
~~~

whereas the mod-2 orientation semantic descends uniquely and is identically one.

Thus the orbit quotient separates sign-sensitive integral information from the sign-blind mod-2 obstruction class.

# Return to the general dependent-origination program

The geometric development is now a validated instance and stress test, not the definition of the general theory.

## v4.49 — abstract presentation descent

For arbitrary presentation type P, setoid S, target Y, and semantic map

~~~text
semantic : P -> Y
~~~

define presentation invariance, quotient factorization, and explicit descent obstruction.

KuuOS proves:

~~~text
HasPresentationQuotientFactorization S semantic
  <->
IsPresentationInvariant S semantic
~~~

with a unique descended semantic, and:

~~~text
not HasPresentationQuotientFactorization S semantic
  <->
HasPresentationDescentObstruction S semantic
~~~

where an obstruction is an identified pair of presentations receiving unequal values.

The Stage-II integer/mod-2 dichotomy is recovered as a specialization.

## v4.50 — exact higher dependent-origination positive sector

v4.50 lifts the v4.49 pattern back to the Cat-valued higher theory.

Two complementary carrier-first interfaces are now integrated.

### Exact higher admissible sector

A raw higher contextual system is exactly dependent-origination admissible when it is represented by:

~~~text
X : HigherStackObject
comparison : restrict(X) -> R
comparison components are equivalences
~~~

Existence is equivalent to:

~~~text
HasHigherStackLocalizationFactorization
~~~

and therefore implies both:

~~~text
HasHigherLocalizationFactorization
IsHigherWAdmissible
~~~

### Exact higher presentation sector

The same positive sector is expressed directly with an object of the higher carrier:

~~~text
X in DO₂(C,W,A)
restrict(X) -> R
pointwise-equivalence comparison
~~~

This is again equivalent to:

~~~text
HigherStackLocalizationFactorization
~~~

or equivalently:

~~~text
HigherLocalizationFactorization
  + actual stack descent of the chosen lift
~~~

The hierarchy is now explicit:

~~~text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
~~~

The reverse implication from weak admissibility is false in general.

For every refinement atlas, the octahedral countermodel is weakly admissible but has no exact DO₂ presentation.

# Current exact frontier

Canonically integrated through v4.50:

~~~text
A. obstruction truth test
   no HigherLocalizationFactorization for counterSystem
   omega(T) = 1 in ZMod 2

B. recursive and geometric verification
   finite carrier
   recursive tower
   inverse limit
   exact Cantor geometry
   dimH = log 2 / log 3
   zero-dimensional approximants
   Hausdorff-limit dimension jump
   geometric middle-switch homeomorphism
   exact free two-point orbit quotient

C. descent semantics
   integral orientation does not descend
   mod-2 orientation descends uniquely
   Stage-II obstruction descends and remains nonzero

D. presentation-general theorem
   quotient factorization
     <-> presentation invariance
   no factorization
     <-> explicit descent obstruction

E. Cat-valued exact positive sector
   exact DO₂ presentation
     <-> HigherStackLocalizationFactorization
     <-> HigherLocalizationFactorization + stack descent
   exact sector -> weak W-admissibility
   counterSystem excluded from exact sector
~~~

# Immediate next theorem sequence

The formal spine has deliberately returned to general dependent origination.

## v4.51 — presentation-change closure of the exact sector

Use the existing HigherPointwiseEquivalenceComparison from v2.17.

Target:

~~~text
R --pointwise equivalence--> S

R has exact DO₂ presentation
  ->
S has exact DO₂ presentation
~~~

The localized stack carrier should remain fixed while the comparison back to the raw system is composed.

This is the Cat-valued analogue of v4.49 presentation invariance.

## v4.52 — comparison between two exact presentations

For two exact presentations of the same raw system, construct comparison data expressing their essential agreement.

Do not assert uniqueness before the required higher comparison/coherence theorem is present.

## v4.53+ — essential uniqueness and naturality

The next genuine universal-property obligations are:

1. essential uniqueness of exact presentations;
2. naturality in the raw contextual system;
3. compatibility with stack descent;
4. presentation invariance at the higher level;
5. integration of explicit obstruction/correction semantics;
6. eventual classification/mapping-property statement.

The target remains:

~~~text
eta : C -> DO(C,W,J,H)

AdmissibleContextualSystems(C,X)
  ≃
Fun(DO(C,W,J,H),X)
~~~

with correct higher variance and coherent uniqueness.

# Proof-engineering rules

- **Fresh GitHub authority first.**
- **A code-changing head requires fresh validation.**
- **A byte-identical replay onto an independent base may reuse validated theorem content after explicit blob/diff verification.**
- **Import does not open a namespace.**
- **Scoped notation and scoped instances do not propagate through imports.**
- **Strong-transformation hom notation requires the StrongTrans scope to be opened explicitly.**
- **Module/file names are not namespace names.**
- **Keep autoImplicit false.**
- **Use term-style structure construction deliberately.**
- **Inside tactic mode, prefer let x : T := { ... } rather than declaration-style where.**
- **Definitional equality is narrower than mathematical equality.**
- **Use theorem-level conversions instead of forcing change.**
- **Prefer typed local equalities, calc, congrArg, funext, and simpa only when rewrite targets matter.**
- **Do not shadow important typeclass instances.**
- **Use eqToIso / eqToHom for dependent transport.**
- **Runtime success and docs-only CI are not theorem authority.**

# No-go implications

Do not promote these implications without theorem support:

~~~text
weak W-admissibility
  -> HigherLocalizationFactorization

weak W-admissibility
  -> exact DO₂ presentation

one bad gauge
  -> every gauge fails

local odd parity
  -> global obstruction

capacity embedding
  -> canonical semantic transport

finite combinatorial recursion
  -> metric fractal theorem

finite inverse limit + new metric
  -> positive Hausdorff dimension

Cantor self-similarity alone
  -> exact Cantor dimension

Hausdorff convergence alone
  -> continuity of Hausdorff dimension

existence of two exact presentations
  -> essential uniqueness

runtime success
  -> theorem authority
~~~

# Reproduction

Focused theorem targets:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationAbstractNonfactorizationV4_00
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationStageIIObstructionClassV4_12
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationStageIIExactFractalCertificateV4_40
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationStageIIFiniteApproxDimensionV4_41
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationStageIIHausdorffDimensionJumpV4_42
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationStageIIBareMiddleSwitchHomeomorphV4_45
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationStageIIGeometricOrbitQuotientV4_47
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationAbstractPresentationDescentV4_49
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationExactHigherAdmissibleV4_50
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationExactHigherPresentationSectorV4_50
~~~

Aggregate formal target:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
~~~

Runtime validation remains separate:

~~~bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

# Current research sentence

**KuuOS has returned from the concrete Stage-II geometric program to the general dependent-origination universality program. The finite octahedral countermodel supplies a proved transport-independent obstruction; the recursive/Cantor development supplies a validated geometric stress test through an exact free orbit quotient; v4.49 abstracts descent to arbitrary presentation quotients; and v4.50 identifies the exact Cat-valued positive sector with actual DO₂ stack presentations equipped with pointwise-equivalence comparison. The immediate frontier is higher presentation invariance, comparison between exact presentations, and ultimately essential uniqueness and naturality of the dependent-origination universal object.**
