# KuuOS / 空OS Roadmap

**Theorem baseline: 2026-09-29 JST · integrated through v4.66**

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
ef3edcfcb4a15b89eff1f87f5007d11111659f50
~~~

Latest theorem-bearing merge:

~~~text
PR #1900
Prove compatible source unitors v4.66
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

A code-changing head requires fresh validation. Runtime success, docs-only CI, stale receipts, and history are not theorem authority.

Protected Lean 4.31 validation-only PR:

~~~text
#1558
open
Draft = true
merged = false
~~~

It remains outside theorem authority and must not be merged, marked Ready for review, or auto-merged.

# 1. Long-range target

The long-range target remains a dependent-origination carrier with a genuine higher mapping property:

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
- a source bicategory encoding mapping-compatible raw and DO₂ data;
- a realization pseudofunctor;
- explicit obstruction/correction semantics;
- explicit authority separation.

A quotient, recursive carrier, inverse limit, metric fractal, obstruction witness, or local bicategory fragment is not promoted to the final universal object without the required mapping property.

# 2. Closed obstruction spine — v4.00 through v4.12

The finite octahedral C2 countermodel proves that weak admissibility alone is not enough.

~~~text
weak W-admissibility                     EXISTS
coherent quotient transport              EXISTS
quotient coboundary solution             EXISTS
comparison / presentation lift           IMPOSSIBLE
HigherLocalizationFactorization          IMPOSSIBLE
~~~

v4.12 extracts the transport-independent class

~~~text
omega(T) = 1 in ZMod 2
~~~

for every coherent quotient transport T.

Permanent no-go boundary:

~~~text
weak W-admissibility
  !=>
HigherLocalizationFactorization
~~~

# 3. Closed concrete verification spine — v4.13 through v4.48

The finite obstruction is transported through:

- an explicit eight-label carrier;
- truncated-icosahedral incidence geometry;
- recursive finite-depth carriers;
- a coherent inverse limit;
- a fixed-point-free middle-switch;
- translated ternary Cantor fibers;
- exact Hausdorff dimension;
- finite zero-dimensional approximants;
- a Hausdorff-limit dimension jump;
- a bare-carrier self-homeomorphism;
- exact two-point orbit quotients;
- integer-orientation non-descent;
- mod-2 unique descent;
- descent of the nonzero Stage-II obstruction.

The exact geometric dimension is:

~~~text
dimH XInfinityGeometricFractal
  = log 2 / log 3
~~~

This program is a validated stress test for the general theory, not the general definition of dependent origination.

# 4. Presentation-general descent — v4.49

For arbitrary presentation data:

~~~text
HasPresentationQuotientFactorization
  <-> IsPresentationInvariant

not HasPresentationQuotientFactorization
  <-> HasPresentationDescentObstruction
~~~

The Stage-II integer/mod-2 dichotomy is recovered as a specialization.

This closes the 0-level presentation-descent abstraction.

# 5. Exact Cat-valued positive sector — v4.50

An exact higher presentation consists of:

~~~text
X in DO₂(C,W,A)
comparison : restrict(X) -> R
comparison components are equivalences
~~~

The exact sector is equivalent to the existence of a higher stack-localization factorization and satisfies:

~~~text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
~~~

The reverse implication from weak W-admissibility is false in general.

# 6. Presentation invariance and universal-target layer — v4.51 through v4.56

## v4.51 — exact presentation invariance

Given:

~~~text
R has an exact DO₂ presentation
R --pointwise-equivalence comparison--> S
~~~

the same DO₂ carrier gives an exact presentation of S after postcomposition of the comparison.

Two directed comparisons in opposite directions imply equivalence of exact-presentability propositions.

## v4.52 — exact-presentation comparison hierarchy

For two exact presentations P and Q of the same raw system, the canonical datum is a common-target cospan with pointwise-equivalence legs.

The formal development distinguishes:

~~~text
canonical cospan
< coherent directed comparison
< pseudonatural equivalence
< equivalence in DO₂
< uniqueness up to modification
~~~

No stronger level is inferred without the relevant hypotheses.

## v4.53 — chosen exact universal target

Under:

~~~text
U : coherent weak higher-localization universal property
hStack : chosen lift satisfies stack descent
~~~

the chosen exact presentation is a coherent universal target among exact presentations.

Exit theorem already proved:

~~~text
every exact presentation factors coherently into Q
any two such factors are invertibly modification-isomorphic
~~~

This is conditional essential uniqueness; the hypotheses are explicit.

## v4.54 — mutual coherent uniqueness

Two exact coherent universal targets Q₁ and Q₂ of the same raw system admit:

~~~text
Q₁ -> Q₂
Q₂ -> Q₁
~~~

with both composites modification-isomorphic to the corresponding coherent identities.

The theorem intentionally stops short of a DO₂ equivalence.

## v4.55 — naturality under coherent raw equivalence

A coherent two-sided equivalence of raw higher contextual systems transports exact coherent universal targets while preserving their DO₂ carrier.

This closes the naturality layer required by the roadmap before equivalence-level promotion.

## v4.56 — DO₂ adjoint equivalence

Mutual coherent uniqueness is promoted to a genuine Mathlib Bicategory.Equivalence in DO₂.

Proved scope:

~~~text
exact coherent universal target
  -> unique up to DO₂ adjoint equivalence
~~~

Not proved:

~~~text
arbitrary exact presentation
  -> arbitrary exact presentation equivalence
~~~

# 7. Exact universal mapping source — v4.57 through v4.66

This is the active theorem program.

The objective is to construct a genuine source bicategory whose objects, 1-cells, and 2-cells remember exactly the compatibility required for realization into DO₂.

## v4.57 — source objects and 1-cells

A source object records:

~~~text
raw higher contextual system R
exact DO₂ presentation Q_R
coherent universal-target witness for Q_R
~~~

A mapping 1-cell X -> Y records:

~~~text
raw StrongTrans eta
DO₂ 1-cell F
invertible comparison square

restrict(F) ; c_Y  ≅  c_X ; eta
~~~

Identity and composition are formalized.

## v4.58 — compatible 2-cells

A 2-cell f ==> g records:

~~~text
raw modification
DO₂ modification
comparison-square compatibility equation
~~~

This is the exact 2-cell interface required by the eventual source bicategory.

## v4.59 — identity and vertical composition

Restriction preserves identity modifications and vertical composition.

Compatible source 2-cells are closed under identity and vertical composition.

## v4.60 — hom categories

For every pair of source objects, mapping 1-cells and compatible 2-cells form a genuine category.

The raw and DO₂ projections become functors on each hom category.

## v4.61 — restriction preserves whiskering

Restriction along the presentation unit preserves native Mathlib left and right whiskering of modifications.

This supplies the remaining presentation-boundary API needed for horizontal structure.

## v4.62 — left whiskering

Construct:

~~~text
f ◁ eta
~~~

for source 1-cell f and compatible 2-cell eta.

The raw and DO₂ components are the native Mathlib left whiskerings.

## v4.63 — right whiskering

Construct:

~~~text
eta ▷ k
~~~

with an independently validated right-whiskering pasting law.

## v4.64 — horizontal composition and interchange

Construct horizontal composition of compatible 2-cells and prove:

- equality of the two canonical whiskering presentations;
- horizontal identity;
- horizontal compatibility with vertical composition;
- the full horizontal/vertical interchange law.

At this point the local 2-cell calculus is functorial.

## v4.65 — source associator

Construct the compatible associator for mapping-property 1-cell composition.

Stable proof architecture:

~~~text
pure bicategory pasting
  -> component expansion
  -> dependent wrapper
~~~

The raw and DO₂ components are native Mathlib associators.

## v4.66 — source left and right unitors

Construct:

~~~text
lambda_f : id ; f ==> f
rho_f    : f ; id ==> f
~~~

with raw and DO₂ components equal to the native Mathlib unitors.

The final GREEN proof again uses:

~~~text
private pure pasting
  -> private component normal form
  -> small dependent wrapper
~~~

The v4.66 exact-head validation completed successfully before PR #1900 was merged.

# 8. Current completion boundary

Canonically proved through v4.66:

~~~text
obstruction:
  arbitrary nonfactorization for the octahedral countermodel
  weak-admissibility insufficiency
  transport-independent omega(T)=1

geometry:
  finite carrier
  recursive tower
  inverse limit
  exact Cantor geometry
  Hausdorff-dimension jump
  middle-switch homeomorphism
  exact orbit quotient
  obstruction / orientation descent

general presentation semantics:
  quotient factorization iff invariance
  nonfactorization iff explicit obstruction

exact Cat-valued universality:
  exact DO₂ positive sector
  directed presentation invariance
  comparison hierarchy
  conditional essential uniqueness
  mutual coherent uniqueness
  naturality under coherent raw equivalence
  DO₂ adjoint equivalence of exact universal targets

mapping source:
  1-cells
  compatible 2-cells
  vertical composition
  hom categories
  left/right whiskering
  horizontal composition
  interchange
  associator hom
  left/right unitor homs
~~~

What is not yet installed is the full source Bicategory instance.

# 9. Immediate frontier — structural isomorphisms

The next theorem-sized obligation is to internalize inverse structural 2-cells and package the existing hom-level structure as isomorphisms.

## Proposed v4.67

Targets:

~~~text
associatorInv
leftUnitorInv
rightUnitorInv

associatorIso
leftUnitorIso
rightUnitorIso
~~~

Exit criteria:

1. inverse 2-cells satisfy the same mapping-source compatibility interface;
2. vertical composites with the existing hom cells equal identity 2-cells;
3. raw projection is the native Mathlib structural inverse;
4. DO₂ projection is the native Mathlib structural inverse;
5. isomorphisms are packaged in the v4.60 hom categories.

Do not install a Bicategory instance before these inverse laws are closed.

# 10. Next frontier — pentagon and triangle

## Proposed v4.68

Prove the coherence laws componentwise.

Preferred proof architecture:

~~~text
source 2-cell equality
  -> v4.60 extensionality
  -> raw component equality
  -> DO₂ component equality
  -> native Mathlib pentagon / triangle
~~~

Exit criteria:

~~~text
pentagon law
triangle law
~~~

No new presentation-level hypotheses should be needed.

# 11. Source bicategory assembly

## Proposed v4.69

Assemble:

- objects;
- 1-cells;
- hom categories;
- horizontal composition;
- left/right whiskering;
- associator Iso;
- left/right unitor Iso;
- pentagon;
- triangle;

into a genuine Mathlib Bicategory instance.

The source bicategory must remain in the exact universal sector; weakly admissible systems without exact presentation data are not silently admitted.

# 12. Realization pseudofunctor

## Proposed v4.70+

The evident projection

~~~text
source object     |-> chosen DO₂ carrier
mapping 1-cell    |-> lift
mapping 2-cell    |-> lift modification
~~~

should be promoted to a pseudofunctor.

Required coherence:

- preservation of identities;
- preservation of composition;
- compatibility with source associator and unitors;
- exact agreement with the already formalized hom-category projection functors.

This is the realization layer needed before a final mapping/classification theorem can be stated cleanly.

# 13. Final universality obligations

After the source bicategory and realization pseudofunctor are installed, the remaining high-level obligations are:

1. formulate the exact mapping-property statement with correct variance;
2. prove existence of realization/factor maps from the universal-target data;
3. prove coherent essential uniqueness at the mapping level;
4. prove naturality;
5. integrate the explicit obstruction/correction semantics;
6. state the strongest justified classification theorem.

Target shape remains schematic:

~~~text
eta : C -> DO(C,W,J,H)

AdmissibleContextualSystems(C,X)
  ≃
Fun(DO(C,W,J,H),X)
~~~

No final equivalence is to be asserted before the mapping-level coherence is formalized.

# 14. Positive sufficient-condition program

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
- explicit coherence/separation/descent hypotheses.

The general question remains:

> Which minimal additional hypotheses characterize the largest useful exact positive sector while excluding the octahedral obstruction?

# 15. Proof-engineering constraints

## P1 — fresh authority

Re-observe exact current branch and SHA before theorem work, writes, merge judgment, and documentation update.

## P2 — validation discipline

A code-changing head requires fresh validation.

A byte-identical theorem replay onto an independent newer base may reuse already validated theorem content only after explicit blob/diff verification.

## P3 — import is not open

Importing a module makes declarations available but does not open its namespace.

## P4 — scoped notation is local

Scoped notation and scoped instances do not propagate through imports.

StrongTrans notation must be opened explicitly where used.

## P5 — autoImplicit

Keep:

~~~lean
set_option autoImplicit false
~~~

## P6 — pure algebra before dependent wrappers

Structural bicategory algebra should be proved in a pure ambient bicategory before dependent presentation data is introduced.

This is now the preferred architecture after v4.62–v4.66.

## P7 — component-first dependent proofs

When a global equality of StrongTrans or induced-bicategory wrappers causes expensive elaboration or hidden transport, descend to components first.

Prefer:

~~~text
pure theorem
  -> component theorem
  -> wrapper constructor
~~~

## P8 — simplifier discipline

Use targeted simp only for non-terminal normalization.

Do not rely on broad non-terminal simp when the surrounding goal contains dependent categorical structure.

If a rewrite target occurs inside a type that depends on that term, ordinary rw may produce an ill-typed motive; use component APIs, congrArg/extensionality, or an appropriate dependent rewriting strategy instead.

## P9 — definitional equality

Do not force change across theorem-level equalities.

Prefer:

- typed local equalities;
- congrArg;
- extensionality;
- calc;
- targeted simpa only;
- small constructor-level projection lemmas.

## P10 — private/public boundary

Do not expose private helper definitions through public theorem types.

Pure implementation pastings and their normal forms should remain private unless they are intended as stable repository API.

## P11 — typeclass discipline

Do not shadow imported canonical instances or create avoidable diamonds.

## P12 — dependent transport

Use eqToIso / eqToHom when genuine dependent transport is required.

## P13 — authority boundary

Runtime success, docs-only CI, stale receipts, and historical summaries are not theorem authority.

# 16. No-go rules

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

two arbitrary exact presentations
  -> equivalence in DO₂

mutual coherent comparison
  -> final natural mapping property

mapping-source hom categories
  -> source bicategory

associator hom + unitor homs
  -> structural isomorphisms

structural isomorphisms
  -> bicategory
  without pentagon and triangle

runtime success
  -> theorem authority
~~~

# 17. Verification commands

Focused theorem targets:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationAbstractNonfactorizationV4_00

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationStageIIObstructionClassV4_12

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationAbstractPresentationDescentV4_49

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationExactHigherPresentationSectorV4_50

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationExactHigherPresentationInvarianceV4_51

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationExactUniversalTargetDO2EquivalenceV4_56

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationExactUniversalMappingMorphismV4_57

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationExactUniversalMappingHorizontalV4_64

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationExactUniversalMappingAssociatorV4_65

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.DependentOriginationExactUniversalMappingUnitorsV4_66
~~~

Aggregate formal target:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
~~~

Runtime validation remains separate:

~~~bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

# 18. Current research boundary

The repository has moved beyond object-level exact presentation existence.

The current frontier is:

~~~text
exact universal objects
  -> presentation invariance
  -> essential uniqueness
  -> naturality
  -> DO₂ equivalence
  -> mapping-compatible 1-cells
  -> mapping-compatible 2-cells
  -> hom categories
  -> whiskering
  -> horizontal interchange
  -> associator
  -> left/right unitors
  -> NEXT: structural inverses and Iso packaging
  -> pentagon / triangle
  -> source bicategory
  -> realization pseudofunctor
  -> final dependent-origination mapping property
~~~
