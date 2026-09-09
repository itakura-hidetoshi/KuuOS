import KUOS.DependentOriginationCoherentStageIIIGapCollapseV2_32

namespace KUOS.DependentOriginationStageIIIRouteCompletenessV2_33

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationFactorCoherenceLiftingV2_21
open KUOS.DependentOriginationModificationTriangleNormalFormV2_22
open KUOS.DependentOriginationStoredTriangleCorrectionV2_26
open KUOS.DependentOriginationWeakHigherLocalizationGapDecompositionV2_31
open KUOS.DependentOriginationCoherentStageIIIGapCollapseV2_32

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Stage-III route completeness v2.33

The v2.32 layer proved that, once one coherent v2.19 universal datum `U` is
explicitly supplied, the v2.31 Stage I and Stage II obstructions disappear and
the whole local weak-universality gap collapses to Stage III.  It also proved
the one-way transport

```text
Stage III essential-uniqueness obstruction
        ->
factor-coherence obstruction
        ->
modification-triangle obstruction
        ->
stored-triangle correction obstruction.
```

The converse was deliberately not asserted.  Failure of the correction route
for a particular coherent datum `U` does not exclude a different v2.18
universal candidate.

This file isolates the exact additional hypothesis needed to close that gap.
The hypothesis is not rigidity and not an extra localization axiom.  It is a
route-completeness/reflection statement:

```text
if the raw system already has some v2.18 weak universal property,
then that universality can be reflected back into correction lifting
for this same coherent datum U.
```

Under this hypothesis the Stage III, factor-coherence, modification-triangle,
and stored-correction obstructions are all equivalent.  More strongly, the
route-completeness proposition itself is equivalent to that exact obstruction
collapse, so it is logically minimal at the present interface.

Globally, a coherent v2.19 universal principle plus route completeness makes
the v2.18 weak universal principle equivalent to the global stored-correction
principle, and therefore also makes Stage III completion equivalent to that
correction principle.

No route-completeness principle is asserted unconditionally.  No converse is
obtained from v2.27 rigidity or v2.29/v2.30 pointwise extension hypotheses;
those classify different moduli/coherence questions and are intentionally kept
separate here.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Local completeness of the chosen coherent correction route relative to the
full v2.18 weak universal property.

The implication is deliberately from *some* v2.18 universal property on `R`
to correction lifting for the fixed coherent datum `U`.  This is exactly the
missing converse content left open in v2.32. -/
def HigherCoherentRouteCompleteness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  HasWeakHigherLocalizationUniversalProperty (W := W) R →
    HigherStoredTriangleTargetCorrectionLifting (W := W) U

/-- The same route-completeness condition may be stated at the v2.21
factor-coherence layer. -/
theorem higherCoherentRouteCompleteness_iff_factorCoherenceRoute
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherCoherentRouteCompleteness (W := W) U ↔
      (HasWeakHigherLocalizationUniversalProperty (W := W) R →
        HigherFactorCoherenceLifting (W := W) U) := by
  constructor
  · intro hRoute hUniversal
    have hCorrection : HigherStoredTriangleTargetCorrectionLifting (W := W) U :=
      hRoute hUniversal
    have hTriangle : HigherFactorModificationTriangleLifting (W := W) U :=
      (higherStoredTriangleCorrectionLifting_iff_modificationTriangleLifting
        (W := W) U).mp hCorrection
    exact
      (higherFactorCoherenceLifting_iff_modificationTriangleLifting
        (W := W) U).mpr hTriangle
  · intro hRoute hUniversal
    have hFactor : HigherFactorCoherenceLifting (W := W) U :=
      hRoute hUniversal
    have hTriangle : HigherFactorModificationTriangleLifting (W := W) U :=
      (higherFactorCoherenceLifting_iff_modificationTriangleLifting
        (W := W) U).mp hFactor
    exact
      (higherStoredTriangleCorrectionLifting_iff_modificationTriangleLifting
        (W := W) U).mpr hTriangle

/-- Equivalently, route completeness says that any explicit correction
obstruction reflects to failure of the full v2.18 weak universal property. -/
theorem higherCoherentRouteCompleteness_iff_correctionObstructionReflectsNonuniversality
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherCoherentRouteCompleteness (W := W) U ↔
      (HigherStoredTriangleTargetCorrectionObstruction (W := W) U →
        ¬ HasWeakHigherLocalizationUniversalProperty (W := W) R) := by
  constructor
  · intro hRoute hObstruction hUniversal
    have hLifting : HigherStoredTriangleTargetCorrectionLifting (W := W) U :=
      hRoute hUniversal
    exact
      ((higherStoredTriangleCorrectionLifting_iff_no_obstruction
        (W := W) U).mp hLifting) hObstruction
  · intro hReflect hUniversal
    apply
      (higherStoredTriangleCorrectionLifting_iff_no_obstruction
        (W := W) U).mpr
    intro hObstruction
    exact (hReflect hObstruction) hUniversal

/-- Under route completeness, the v2.26 correction obstruction is not merely a
consequence of Stage III failure: it is exactly Stage III failure. -/
theorem higherStoredTriangleCorrectionObstruction_iff_essentialUniquenessObstruction_of_routeCompleteness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hRoute : HigherCoherentRouteCompleteness (W := W) U) :
    HigherStoredTriangleTargetCorrectionObstruction (W := W) U ↔
      HigherWeakEssentialUniquenessObstruction (W := W) R := by
  constructor
  · intro hCorrection
    have hNoUniversal : ¬ HasWeakHigherLocalizationUniversalProperty (W := W) R :=
      ((higherCoherentRouteCompleteness_iff_correctionObstructionReflectsNonuniversality
        (W := W) U).mp hRoute) hCorrection
    exact
      (not_hasWeakHigherLocalizationUniversalProperty_iff_essentialUniquenessObstruction_of_coherent
        (W := W) U).mp hNoUniversal
  · intro hStageIII
    exact
      higherStoredTriangleCorrectionObstruction_of_essentialUniquenessObstruction
        (W := W) U hStageIII

/-- The v2.22 modification-triangle obstruction therefore has the same exact
Stage III normal form under route completeness. -/
theorem higherFactorModificationTriangleObstruction_iff_essentialUniquenessObstruction_of_routeCompleteness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hRoute : HigherCoherentRouteCompleteness (W := W) U) :
    HigherFactorModificationTriangleObstruction (W := W) U ↔
      HigherWeakEssentialUniquenessObstruction (W := W) R := by
  calc
    HigherFactorModificationTriangleObstruction (W := W) U ↔
        HigherStoredTriangleTargetCorrectionObstruction (W := W) U :=
      (higherStoredTriangleCorrectionObstruction_iff_modificationTriangleObstruction
        (W := W) U).symm
    _ ↔ HigherWeakEssentialUniquenessObstruction (W := W) R :=
      higherStoredTriangleCorrectionObstruction_iff_essentialUniquenessObstruction_of_routeCompleteness
        (W := W) U hRoute

/-- Likewise the v2.21 factor-coherence obstruction is exactly Stage III under
route completeness. -/
theorem higherFactorCoherenceObstruction_iff_essentialUniquenessObstruction_of_routeCompleteness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hRoute : HigherCoherentRouteCompleteness (W := W) U) :
    HigherFactorCoherenceObstruction (W := W) U ↔
      HigherWeakEssentialUniquenessObstruction (W := W) R := by
  calc
    HigherFactorCoherenceObstruction (W := W) U ↔
        HigherFactorModificationTriangleObstruction (W := W) U :=
      higherFactorCoherenceObstruction_iff_modificationTriangleObstruction
        (W := W) U
    _ ↔ HigherWeakEssentialUniquenessObstruction (W := W) R :=
      higherFactorModificationTriangleObstruction_iff_essentialUniquenessObstruction_of_routeCompleteness
        (W := W) U hRoute

/-- Minimality theorem: at the present interfaces, route completeness is
*equivalent* to exact identification of the stored-correction obstruction with
Stage III.

Thus v2.33 does not merely provide one sufficient extra assumption; it
characterizes the missing assumption propositionally. -/
theorem higherCoherentRouteCompleteness_iff_exactStageIIICorrectionCollapse
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherCoherentRouteCompleteness (W := W) U ↔
      (HigherStoredTriangleTargetCorrectionObstruction (W := W) U ↔
        HigherWeakEssentialUniquenessObstruction (W := W) R) := by
  constructor
  · intro hRoute
    exact
      higherStoredTriangleCorrectionObstruction_iff_essentialUniquenessObstruction_of_routeCompleteness
        (W := W) U hRoute
  · intro hExact
    apply
      (higherCoherentRouteCompleteness_iff_correctionObstructionReflectsNonuniversality
        (W := W) U).mpr
    intro hCorrection
    have hStageIII : HigherWeakEssentialUniquenessObstruction (W := W) R :=
      hExact.mp hCorrection
    exact
      (not_hasWeakHigherLocalizationUniversalProperty_iff_essentialUniquenessObstruction_of_coherent
        (W := W) U).mpr hStageIII

/-- The same minimality statement may be read at the v2.21 factor-coherence
obstruction layer. -/
theorem higherCoherentRouteCompleteness_iff_exactStageIIIFactorCoherenceCollapse
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherCoherentRouteCompleteness (W := W) U ↔
      (HigherFactorCoherenceObstruction (W := W) U ↔
        HigherWeakEssentialUniquenessObstruction (W := W) R) := by
  constructor
  · intro hRoute
    exact
      higherFactorCoherenceObstruction_iff_essentialUniquenessObstruction_of_routeCompleteness
        (W := W) U hRoute
  · intro hExact
    apply
      (higherCoherentRouteCompleteness_iff_exactStageIIICorrectionCollapse
        (W := W) U).mpr
    calc
      HigherStoredTriangleTargetCorrectionObstruction (W := W) U ↔
          HigherFactorModificationTriangleObstruction (W := W) U :=
        higherStoredTriangleCorrectionObstruction_iff_modificationTriangleObstruction
          (W := W) U
      _ ↔ HigherFactorCoherenceObstruction (W := W) U :=
        (higherFactorCoherenceObstruction_iff_modificationTriangleObstruction
          (W := W) U).symm
      _ ↔ HigherWeakEssentialUniquenessObstruction (W := W) R := hExact

/-- Global route completeness over every coherent v2.19 universal datum.  This
is an explicit principle, not an axiom. -/
def HigherCoherentRouteCompletenessPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherCoherentRouteCompleteness (W := W) U

/-- Global minimality: route completeness is exactly the assertion that every
coherent datum identifies correction obstruction with Stage III obstruction. -/
theorem higherCoherentRouteCompletenessPrinciple_iff_exactStageIIICorrectionCollapse :
    HigherCoherentRouteCompletenessPrinciple
        (W := W) (uH := uH) (vH := vH) ↔
      ∀ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
        (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
        HigherStoredTriangleTargetCorrectionObstruction (W := W) U ↔
          HigherWeakEssentialUniquenessObstruction (W := W) R := by
  constructor
  · intro hRoute R U
    exact
      (higherCoherentRouteCompleteness_iff_exactStageIIICorrectionCollapse
        (W := W) U).mp (hRoute R U)
  · intro hExact R U
    exact
      (higherCoherentRouteCompleteness_iff_exactStageIIICorrectionCollapse
        (W := W) U).mpr (hExact R U)

/-- With a coherent v2.19 universal principle and global route completeness,
the full v2.18 weak universal principle is exactly the global stored-correction
principle. -/
theorem higherWeakLocalizationUniversalPrinciple_iff_storedTriangleCorrectionPrinciple_of_coherent_and_routeCompleteness
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH))
    (hRoute : HigherCoherentRouteCompletenessPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherWeakLocalizationUniversalPrinciple
        (W := W) (uH := uH) (vH := vH) ↔
      HigherStoredTriangleTargetCorrectionPrinciple
        (W := W) (uH := uH) (vH := vH) := by
  constructor
  · intro hUniversal R U
    have hR : IsHigherWAdmissible W R :=
      hasCoherentWeakHigherLocalizationUniversalProperty_isHigherWAdmissible W ⟨U⟩
    exact hRoute R U (hUniversal R hR)
  · intro hCorrection R hR
    rcases hCoherent R hR with ⟨U⟩
    have hLifting : HigherStoredTriangleTargetCorrectionLifting (W := W) U :=
      hCorrection R U
    have hNoObstruction :
        ¬ HigherStoredTriangleTargetCorrectionObstruction (W := W) U :=
      (higherStoredTriangleCorrectionLifting_iff_no_obstruction
        (W := W) U).mp hLifting
    exact
      hasWeakHigherLocalizationUniversalProperty_of_no_storedTriangleCorrectionObstruction
        (W := W) U hNoObstruction

/-- Consequently, relative to coherent v2.19 existence and route completeness,
Stage III completion itself is exactly the global correction-solvability
principle. -/
theorem higherWeakEssentialUniquenessCompletion_iff_storedTriangleCorrectionPrinciple_of_coherent_and_routeCompleteness
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH))
    (hRoute : HigherCoherentRouteCompletenessPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherWeakEssentialUniquenessCompletion
        (W := W) (uH := uH) (vH := vH) ↔
      HigherStoredTriangleTargetCorrectionPrinciple
        (W := W) (uH := uH) (vH := vH) := by
  calc
    HigherWeakEssentialUniquenessCompletion
        (W := W) (uH := uH) (vH := vH) ↔
      HigherWeakLocalizationUniversalPrinciple
        (W := W) (uH := uH) (vH := vH) :=
      (higherWeakLocalizationUniversalPrinciple_iff_essentialUniquenessCompletion_of_coherent
        (W := W) hCoherent).symm
    _ ↔ HigherStoredTriangleTargetCorrectionPrinciple
        (W := W) (uH := uH) (vH := vH) :=
      higherWeakLocalizationUniversalPrinciple_iff_storedTriangleCorrectionPrinciple_of_coherent_and_routeCompleteness
        (W := W) hCoherent hRoute

/-!
The v2.33 boundary is therefore exact:

```text
coherent datum U
      +
route completeness for U
      |
      v
Stage III obstruction
  <-> factor-coherence obstruction
  <-> modification-triangle obstruction
  <-> stored-triangle correction obstruction.
```

Moreover:

```text
route completeness for U
  <->
(stored-correction obstruction <-> Stage III obstruction).
```

So the extra hypothesis is not merely sufficient; within the present
interfaces it is precisely the missing logical content needed to turn the
v2.32 one-way route into an equivalence.

This does not identify correction existence with v2.27 uniqueness/rigidity, and
it does not infer any v2.30 arrowwise equation obstruction without its own
extension hypotheses.
-/

end KUOS.DependentOriginationStageIIIRouteCompletenessV2_33
