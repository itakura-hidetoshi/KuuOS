# KuuOS / 空OS Roadmap

**Theorem baseline: 2026-09-27 JST · integrated through v4.50**

This roadmap records proved results, authority boundaries, theorem-sized exit criteria, and the next formal steps. It is subordinate to fresh GitHub theorem authority.

# 0. Authority and canonical state

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
5b55a205baeba7c3f8dfbb09ade21fa5e5b5304c
~~~

Latest theorem-bearing merge:

~~~text
PR #1847
Define exact higher dependent-origination presentation sector v4.50
~~~

Companion v4.50 merge:

~~~text
PR #1846
Define exact higher dependent-origination admissible sector v4.50
merge commit = 9b60b3ec2835f99896da07439f08d4c06752f1ed
~~~

Authority order:

~~~text
1. fresh exact GitHub canonical SHA
2. formal Lean theorem artifacts at that SHA
3. README / ROADMAP
4. CI/runtime receipts
5. history / memory
~~~

Pinned formal environment:

~~~text
Lean    leanprover/lean4:v4.30.0-rc2
Mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6
~~~

A code-changing head requires fresh validation. A byte-identical theorem replay onto an independent newer base may reuse already validated theorem content after explicit blob/diff verification.

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

# 1. Long-range target

The long-range target remains a dependent-origination carrier with a genuine mapping property:

~~~text
eta : C -> DO(C,W,J,H)

AdmissibleContextualSystems(C,X)
  ≃
Fun(DO(C,W,J,H),X)
~~~

Required ingredients include:

- correct higher variance;
- coherent localization/factorization;
- stack descent;
- exact presentation class;
- presentation invariance;
- essential uniqueness;
- naturality;
- explicit obstruction/correction semantics;
- explicit authority separation.

A quotient, recursive carrier, inverse limit, metric fractal, or obstruction witness is not promoted to the final universal object without this mapping property.

# 2. Closed obstruction spine — v4.00 through v4.12

## v4.00 — arbitrary higher nonfactorization

The concrete finite octahedral C2 countermodel satisfies:

~~~lean
IsEmpty
  (HigherLocalizationFactorization
    (W := allMorphisms) counterSystem)
~~~

This is arbitrary nonfactorization, not merely failure of one gauge or one canonical correction.

## v4.01 — weak admissibility is insufficient

The same countermodel satisfies:

~~~text
IsHigherWAdmissible allMorphisms counterSystem
~~~

but has no HigherLocalizationFactorization.

Therefore:

~~~text
weak W-admissibility
  !=>
higher localization factorization
~~~

This remains a permanent no-go boundary for the general theory.

## v4.02–v4.11 — exact location of the comparison obstruction

The development separates:

~~~text
coherent quotient transport       EXISTS
quotient coboundary solution       EXISTS
comparison lift                    FAILS
full correction                    FAILS
~~~

The obstruction is transport/gauge independent.

## v4.12 — exact Stage-II class

For every coherent quotient transport:

~~~text
omega(T) = 1 in ZMod 2
~~~

Any successful comparison would force omega(T)=0.

This class becomes the invariant tracked through the later concrete carrier program.

# 3. Finite carrier and recursive transport — v4.13 through v4.27

Proved:

- explicit eight-label Stage-II parity carrier;
- incidence-compatible truncated-icosahedral placement;
- global capacity and local one-star obstruction;
- adjacent opposite-kind middle-switch mates;
- scalar pushforward with source provenance;
- integer orientation lift;
- recursive central-cell preservation at every finite depth;
- coherent restriction tower;
- set-theoretic inverse limit;
- source-label equivalence;
- fixed-point-free middle-switch involution.

The supported inverse limit satisfies:

~~~text
OctahedralStageIIParityFace
  ≃
StageIIFiniteDepthInverseLimit
~~~

# 4. Metric and exact Cantor program — v4.28 through v4.42

This program is closed.

## v4.28 — rigid carrier dimension zero

The current inverse-limit carrier has exactly eight points:

~~~text
dimH XInfinityCurrent = 0
~~~

for every extended metric structure.

## v4.29 — genuine branch freedom gives dimension one

~~~text
dimH XInfinityBranch = 1
~~~

Positive dimension comes from new branch freedom, not from re-metrizing a finite set.

## v4.30–v4.32 — geometric Cantor carrier and Hausdorff convergence

Each branch carries a translated ternary Cantor set.

Proved:

- compactness;
- closedness;
- nonemptiness;
- exact branchwise self-similarity;
- ambient inclusion;
- explicit Hausdorff-distance rate;
- Hausdorff convergence.

## v4.33–v4.40 — exact dimension

The critical exponent is:

~~~text
s = logb 3 2
  = log 2 / log 3
~~~

Forward and inverse Hölder transport prove:

~~~text
dimH cantorSet = s

forall x,
  dimH (stageIIGeometricCantorFiber x) = s

dimH XInfinityGeometricFractal = s

dimH XInfinityGeometricFractal
  < dimH XInfinityBranch
  = 1
~~~

v4.40 packages this exact dimension together with the earlier v4.32 topology/metric certificate.

## v4.41 — finite approximants are zero-dimensional

Finite-prefix factorization yields:

~~~text
(stageIIGeometricApproxFiber n x).Finite
(XInfinityGeometricApprox n).Finite

dimH (stageIIGeometricApproxFiber n x) = 0
dimH (XInfinityGeometricApprox n) = 0
~~~

## v4.42 — concrete dimension jump

The finite approximants converge in Hausdorff distance to a positive-dimensional limit:

~~~text
forall n,
  dimH X_n = 0

d_H(X_n, X_infinity) <= 3^(-n)

d_H(X_n, X_infinity) -> 0

dimH X_infinity = log 2 / log 3 > 0
~~~

This closes the finite-approximant side of the geometric program.

# 5. Geometric middle-switch and orbit descent — v4.43 through v4.48

This program is also closed as a concrete verification spine.

## v4.43 — tagged geometric lift

The branchwise middle-switch is an explicit real translation, an isometry, continuous, fiber-preserving, involutive in mate pairs, and fixed-point-free.

A tagged geometric carrier retains branch provenance and finite-depth orientation data.

## v4.44 — bare-carrier descent

Offset separation plus Cantor coordinates in [0,1] imply:

~~~text
distinct branch fibers are disjoint
every bare point has one unique branch
~~~

Therefore tagged and bare carriers are equivalent and the middle-switch descends.

## v4.45 — homeomorphism

Distinct fibers are at real distance at least one. Hence the branch selector is locally constant and the descended middle-switch is a fixed-point-free self-homeomorphism.

## v4.46 — orientation transport

For every p and depth n:

~~~text
O(M p,n) = flip(O(p,n))
epsilon(M p,n) = -epsilon(p,n)
~~~

but modulo two:

~~~text
[epsilon(M p,n)]_2 = [epsilon(p,n)]_2 = 1
~~~

## v4.47 — exact orbit quotient

Every orbit is exactly:

~~~text
{p, M p}
~~~

and:

~~~text
[p] = [q]
  <-> q = p or q = M p
~~~

The quotient has the exact invariant-semantic factorization property.

## v4.48 — obstruction and orientation descent

The existing Stage-II obstruction descends to the orbit quotient and remains:

~~~text
omega_geo(T,q) = 1 != 0
~~~

The integer orientation semantic does not descend, while its mod-2 reduction descends uniquely.

This is the concrete prototype for the later presentation-general theorem.

# 6. Return to general dependent origination — v4.49

v4.49 removes Stage-II and geometry from the primary theorem.

For arbitrary presentation type P, setoid S, semantic target Y, and map:

~~~text
semantic : P -> Y
~~~

define:

~~~text
IsPresentationInvariant
HasPresentationQuotientFactorization
HasPresentationDescentObstruction
~~~

Then prove:

~~~text
HasPresentationQuotientFactorization S semantic
  <->
IsPresentationInvariant S semantic
~~~

with unique descended semantic, and:

~~~text
not HasPresentationQuotientFactorization S semantic
  <->
HasPresentationDescentObstruction S semantic
~~~

This is the current 0-level universal descent theorem.

The Stage-II integer/mod-2 dichotomy appears only as a specialization.

# 7. Exact Cat-valued positive sector — v4.50

v4.50 is the current theorem frontier.

The objective is to identify the systems for which a genuine localized stack presentation actually exists.

## v4.50A — exact higher admissible sector

A raw higher contextual system R is represented by:

~~~text
X : HigherStackObject
comparison : restrict(X) -> R
comparison components are equivalences
~~~

Existence is equivalent to:

~~~text
HasHigherStackLocalizationFactorization
~~~

Therefore exact higher admissibility implies:

~~~text
HasHigherLocalizationFactorization
IsHigherWAdmissible
~~~

## v4.50B — exact higher presentation sector

The same positive sector is presented directly with the higher carrier:

~~~text
X in DO₂(C,W,A)

restrict(X) -> R
pointwise-equivalence comparison
~~~

Existence is equivalent to:

~~~text
HigherStackLocalizationFactorization
~~~

and to:

~~~text
HigherLocalizationFactorization
  + actual stack descent of the chosen lift
~~~

The resulting hierarchy is:

~~~text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
~~~

The reverse direction from weak W-admissibility fails in general.

For every refinement atlas, counterSystem is weakly admissible but excluded from the exact positive sector.

# 8. Immediate frontier — v4.51

The next theorem unit should be **presentation-change closure of the exact sector**.

Use the existing directed structure:

~~~text
HigherPointwiseEquivalenceComparison R S
~~~

from v2.17.

Target theorem:

~~~text
R has exact DO₂ presentation
R --pointwise-equivalence comparison--> S
-----------------------------------------
S has exact DO₂ presentation
~~~

Preferred construction:

1. keep the localized stack carrier fixed;
2. compose its comparison to R with the comparison R -> S;
3. use pointwise composition of equivalences;
4. retain the original stack witness unchanged.

Exit criteria:

~~~text
ExactPresentation R
  ->
HigherPointwiseEquivalenceComparison R S
  ->
ExactPresentation S
~~~

and an existence-level theorem for membership in the exact positive sector.

This is the Cat-valued analogue of v4.49 presentation invariance.

# 9. v4.52 — comparison between exact presentations

Given two exact presentations of the same raw system:

~~~text
P : ExactPresentation R
Q : ExactPresentation R
~~~

construct the available comparison data between their localized stack carriers.

The theorem must distinguish carefully between:

- existence of a directed comparison;
- pointwise equivalence;
- pseudonatural equivalence;
- equivalence inside DO₂;
- uniqueness up to modification.

Do not collapse these levels.

Exit criterion: one explicit comparison interface whose hypotheses are actually proved.

# 10. v4.53+ — essential uniqueness and naturality

The genuine universality obligations after comparison existence are:

1. essential uniqueness of exact presentations;
2. coherence of comparison composition;
3. naturality in R;
4. compatibility with descent;
5. presentation invariance;
6. compatibility with obstruction/correction semantics;
7. final classification/mapping property.

The target remains:

~~~text
eta : C -> DO(C,W,J,H)

AdmissibleContextualSystems(C,X)
  ≃
Fun(DO(C,W,J,H),X)
~~~

No equivalence is to be asserted before essential uniqueness and naturality are formalized.

# 11. Positive sufficient-condition program

The octahedral counterexample does not invalidate positive results under stronger hypotheses.

Known sufficient routes include:

- fiber hom-thinness;
- fiber functor 2-thinness;
- fiber functor iso-thinness;
- thin fiber cores;
- trivial automorphism groups;
- canonical five-defect gauge trivialization;
- generated correction reachability;
- strict presentation models;
- other explicit coherence/separation/descent hypotheses.

The general question remains:

> Which minimal additional hypotheses characterize the largest useful exact positive sector while excluding the octahedral obstruction?

# 12. Proof-engineering constraints

## P1 — fresh authority

Re-observe exact current branch and SHA before theorem work, writes, merge judgment, and documentation update.

## P2 — validation discipline

A code-changing head requires fresh validation.

A byte-identical replay onto an independent newer base may reuse already validated theorem content after checking:

~~~text
old blob = new blob
ahead/behind relation understood
no conflicting theorem changes
~~~

## P3 — import is not open

Importing a module makes declarations available but does not open its namespace.

## P4 — scoped notation is local

Scoped notation and scoped instances do not propagate through imports.

In particular, strong-transformation hom notation requires:

~~~lean
open scoped CategoryTheory.Pseudofunctor.StrongTrans
~~~

in the file that uses it.

## P5 — structure syntax

Prefer explicit term-style structure construction.

Inside tactic mode:

~~~lean
let x : T :=
  { field1 := ...
    field2 := ... }
~~~

Do not use declaration-style where syntax as though tactic let accepted it.

## P6 — autoImplicit

Keep:

~~~lean
set_option autoImplicit false
~~~

Name-resolution failures should not silently become implicit variables.

## P7 — definitional equality

Do not force change across merely theorem-level equalities.

Use theorem-level conversion, typed local equalities, calc, congrArg, funext, and simpa only.

## P8 — typeclass discipline

Do not shadow imported canonical instances or create avoidable diamonds.

## P9 — dependent transport

Prefer eqToIso / eqToHom for dependent categorical transport.

## P10 — authority boundary

Runtime success, docs-only CI, stale receipts, and history are not theorem authority.

# 13. No-go rules

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

finite combinatorial recursion
  -> metric fractal theorem

finite inverse limit + new metric
  -> positive Hausdorff dimension

Cantor self-similarity alone
  -> exact Cantor dimension

Hausdorff convergence alone
  -> continuity of Hausdorff dimension

two exact presentations
  -> essential uniqueness

pointwise equivalence
  -> equivalence in DO₂

runtime success
  -> theorem authority
~~~

# 14. Verification commands

Focused current theorem targets:

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

# 15. Current completion boundary

Canonically proved:

~~~text
v4.00-v4.12
  abstract nonfactorization
  weak-admissibility insufficiency
  exact Stage-II obstruction omega(T)=1

v4.13-v4.27
  finite carrier
  incidence geometry
  recursive transport
  inverse limit
  middle-switch involution

v4.28-v4.40
  metric carrier
  exact Cantor geometry
  dimH = log 2 / log 3

v4.41-v4.42
  finite zero-dimensional approximants
  Hausdorff-limit dimension jump

v4.43-v4.48
  geometric middle-switch
  bare homeomorphism
  orientation transport
  free two-point orbit quotient
  obstruction descent
  integer non-descent / mod-2 unique descent

v4.49
  abstract presentation descent
  quotient factorization iff invariance
  no factorization iff explicit obstruction

v4.50
  exact higher admissible sector
  exact DO₂ presentation sector
  equivalence with stack-localization factorization
  exact sector implies weak W-admissibility
  octahedral countermodel excluded
~~~

Immediate open theorem:

~~~text
prove exact positive-sector closure under
HigherPointwiseEquivalenceComparison
~~~

Then:

~~~text
construct comparison between two exact presentations
  ->
prove essential uniqueness
  ->
prove naturality
  ->
assemble the final dependent-origination universality theorem
~~~
