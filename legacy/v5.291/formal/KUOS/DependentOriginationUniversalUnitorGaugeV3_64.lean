import KUOS.DependentOriginationOctahedralInversePairV3_63

namespace KUOS.DependentOriginationUniversalUnitorGaugeV3_64

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationCoherenceDefectsV2_65
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationFiveGeneratedCorrectionCoboundaryV3_00
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationQuotientDefectOrbitV3_06
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateFootprintV3_12
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationUnitorWitnessCorrelationV3_35
open KUOS.DependentOriginationAssociatorUnitorBoundaryReductionV3_36
open KUOS.DependentOriginationFreshAssociatorCompletionV3_37
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
open KUOS.DependentOriginationGroupoidHolonomySeparationV3_58
open KUOS.DependentOriginationInversePairBoundaryObstructionV3_55
open KUOS.DependentOriginationNontrivialSuffixObstructionV3_60
open KUOS.DependentOriginationOctahedralInversePairV3_63

universe u v uH vH

set_option autoImplicit false

noncomputable section

/-!
# Universal common-unitor gauge v3.64

v3.60 still takes one fixed quotient gauge correcting every left/right unitor
as an explicit input.  The preceding incidence analysis suggests that this
input is not genuinely obstructed.

For a fixed seed gauge Q, a left-unitor equation inspects exactly

  gComp(1_X,f), gId(X),

and a right-unitor equation inspects exactly

  gComp(f,1_Y), gId(Y).

Keep every gId coordinate fixed.  Each individual unitor equation can then be
solved by changing only its gComp coordinate: cancel the canonical generated
composition comparison, insert the equality transport from 1≫f=f or f≫1=f,
and invert the remaining mapId-plus-unitor suffix.

All local solutions therefore retain the same mapId family.  The v3.24/v3.25
unitor rigidity already proves that corrected unitors with the same mapId
coordinate agree on every actual overlap.  v3.35 and v3.38 can consequently
glue these local solutions into one fixed gauge correcting all unitors.

This file truth-tests that construction directly.  If it succeeds, the common
unitor gauge is no longer an additional hypothesis of the concrete v3.60
countermodel route.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- Inert seed gauge used only to obtain one initial value in every dependent
coordinate fiber. -/
noncomputable def neutralQuotientGauge :
    GeneratedQuotientGaugeParameters W R D where
  mapIdGauge := fun _ => Iso.refl _
  mapCompGauge := fun _ _ => Iso.refl _

/-! ## Solve one left unitor while preserving all identity coordinates -/

/-- The part of the left-unitor equation after its composition comparison. -/
noncomputable def leftUnitorSuffixIso
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y : W.Localization} (f : X ⟶ Y) :
    (quotientRepresentativeMap W R D (𝟙 X) ≫
        quotientRepresentativeMap W R D f) ≅
      quotientRepresentativeMap W R D f :=
  whiskerRightIso
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId X)
      (quotientRepresentativeMap W R D f) ≪≫
    λ_ (quotientRepresentativeMap W R D f)

/-- Equality transport induced by the source law 1≫f=f. -/
noncomputable def leftUnitorSourceTransportIso
    {X Y : W.Localization} (f : X ⟶ Y) :
    quotientRepresentativeMap W R D ((𝟙 X) ≫ f) ≅
      quotientRepresentativeMap W R D f :=
  eqToIso (by rw [Category.id_comp])

/-- Exact gComp value that solves the selected left-unitor equation while
leaving gId fixed. -/
noncomputable def leftUnitorGaugeValue
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y : W.Localization} (f : X ⟶ Y) :
    QuotientGaugeCoordinateFiber W R D (.composition (𝟙 X) f) :=
  (generatedCompositionMapIso W R D (𝟙 X) f).symm ≪≫
    (leftUnitorSourceTransportIso W R D f ≪≫
      (leftUnitorSuffixIso W R D Q f).symm)

theorem leftUnitorGaugeValue_fac
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y : W.Localization} (f : X ⟶ Y) :
    (generatedCompositionMapIso W R D (𝟙 X) f).hom ≫
        (leftUnitorGaugeValue W R D Q f).hom =
      (leftUnitorSourceTransportIso W R D f ≪≫
        (leftUnitorSuffixIso W R D Q f).symm).hom := by
  simp only [leftUnitorGaugeValue, Iso.trans_hom, Iso.symm_hom,
    Iso.hom_inv_id_assoc]

/-- Update exactly the left-unit composition coordinate. -/
noncomputable def completeLeftUnitor
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y : W.Localization} (f : X ⟶ Y) :
    GeneratedQuotientGaugeParameters W R D :=
  quotientGaugeUpdate W R D Q (.composition (𝟙 X) f)
    (leftUnitorGaugeValue W R D Q f)

theorem completeLeftUnitor_mapCompGauge
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y : W.Localization} (f : X ⟶ Y) :
    (completeLeftUnitor W R D Q f).mapCompGauge (𝟙 X) f =
      leftUnitorGaugeValue W R D Q f := by
  simpa [quotientGaugeCoordinateValue] using
    (quotientGaugeUpdate_value_self
      W R D Q (.composition (𝟙 X) f) (leftUnitorGaugeValue W R D Q f))

theorem completeLeftUnitor_mapIdGauge
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y : W.Localization} (f : X ⟶ Y)
    (A : W.Localization) :
    (completeLeftUnitor W R D Q f).mapIdGauge A = Q.mapIdGauge A := by
  simpa [quotientGaugeCoordinateValue] using
    (quotientGaugeUpdate_value_of_ne
      W R D Q (.composition (𝟙 X) f) (leftUnitorGaugeValue W R D Q f)
      (.identity A) (by intro h; cases h))

/-- The one-coordinate update really corrects the selected left unitor. -/
theorem completeLeftUnitor_corrected
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y : W.Localization} (f : X ⟶ Y) :
    completeLeftUnitor W R D Q f ∈
      quotientRouteCorrectionLocus W R D (.leftUnitor f) := by
  let Q' := completeLeftUnitor W R D Q f
  let L := quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q
  let L' := quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q'
  change quotientLeftUnitorDefect W R D L' f = Iso.refl _
  apply (quotientLeftUnitorDefect_eq_refl_iff W R D L' f).2
  have hComp :
      L'.mapComp (𝟙 X) f =
        leftUnitorSourceTransportIso W R D f ≪≫
          (leftUnitorSuffixIso W R D Q f).symm := by
    apply Iso.ext
    change
      (generatedCompositionMapIso W R D (𝟙 X) f).hom ≫
          (Q'.mapCompGauge (𝟙 X) f).hom =
        (leftUnitorSourceTransportIso W R D f ≪≫
          (leftUnitorSuffixIso W R D Q f).symm).hom
    rw [show Q'.mapCompGauge (𝟙 X) f =
        leftUnitorGaugeValue W R D Q f by
      simpa [Q'] using completeLeftUnitor_mapCompGauge W R D Q f]
    exact leftUnitorGaugeValue_fac W R D Q f
  have hId : L'.mapId X = L.mapId X := by
    change
      generatedIdentityMapIso W R D X ≪≫ Q'.mapIdGauge X =
        generatedIdentityMapIso W R D X ≪≫ Q.mapIdGauge X
    rw [show Q'.mapIdGauge X = Q.mapIdGauge X by
      simpa [Q'] using completeLeftUnitor_mapIdGauge W R D Q f X]
  have hSuffix :
      leftUnitorSuffixIso W R D Q' f =
        leftUnitorSuffixIso W R D Q f := by
    unfold leftUnitorSuffixIso
    rw [hId]
  change
    (L'.mapComp (𝟙 X) f).hom ≫
        (leftUnitorSuffixIso W R D Q' f).hom =
      (leftUnitorSourceTransportIso W R D f).hom
  rw [hComp, hSuffix]
  simp only [Iso.trans_hom, Iso.symm_hom, Category.assoc,
    Iso.inv_hom_id, Category.comp_id]

/-! ## Solve one right unitor while preserving all identity coordinates -/

/-- The part of the right-unitor equation after its composition comparison. -/
noncomputable def rightUnitorSuffixIso
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y : W.Localization} (f : X ⟶ Y) :
    (quotientRepresentativeMap W R D f ≫
        quotientRepresentativeMap W R D (𝟙 Y)) ≅
      quotientRepresentativeMap W R D f :=
  whiskerLeftIso
      (quotientRepresentativeMap W R D f)
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId Y) ≪≫
    ρ_ (quotientRepresentativeMap W R D f)

/-- Equality transport induced by the source law f≫1=f. -/
noncomputable def rightUnitorSourceTransportIso
    {X Y : W.Localization} (f : X ⟶ Y) :
    quotientRepresentativeMap W R D (f ≫ 𝟙 Y) ≅
      quotientRepresentativeMap W R D f :=
  eqToIso (by rw [Category.comp_id])

/-- Exact gComp value that solves the selected right-unitor equation while
leaving gId fixed. -/
noncomputable def rightUnitorGaugeValue
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y : W.Localization} (f : X ⟶ Y) :
    QuotientGaugeCoordinateFiber W R D (.composition f (𝟙 Y)) :=
  (generatedCompositionMapIso W R D f (𝟙 Y)).symm ≪≫
    (rightUnitorSourceTransportIso W R D f ≪≫
      (rightUnitorSuffixIso W R D Q f).symm)

theorem rightUnitorGaugeValue_fac
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y : W.Localization} (f : X ⟶ Y) :
    (generatedCompositionMapIso W R D f (𝟙 Y)).hom ≫
        (rightUnitorGaugeValue W R D Q f).hom =
      (rightUnitorSourceTransportIso W R D f ≪≫
        (rightUnitorSuffixIso W R D Q f).symm).hom := by
  simp only [rightUnitorGaugeValue, Iso.trans_hom, Iso.symm_hom,
    Iso.hom_inv_id_assoc]

/-- Update exactly the right-unit composition coordinate. -/
noncomputable def completeRightUnitor
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y : W.Localization} (f : X ⟶ Y) :
    GeneratedQuotientGaugeParameters W R D :=
  quotientGaugeUpdate W R D Q (.composition f (𝟙 Y))
    (rightUnitorGaugeValue W R D Q f)

theorem completeRightUnitor_mapCompGauge
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y : W.Localization} (f : X ⟶ Y) :
    (completeRightUnitor W R D Q f).mapCompGauge f (𝟙 Y) =
      rightUnitorGaugeValue W R D Q f := by
  simpa [quotientGaugeCoordinateValue] using
    (quotientGaugeUpdate_value_self
      W R D Q (.composition f (𝟙 Y)) (rightUnitorGaugeValue W R D Q f))

theorem completeRightUnitor_mapIdGauge
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y : W.Localization} (f : X ⟶ Y)
    (A : W.Localization) :
    (completeRightUnitor W R D Q f).mapIdGauge A = Q.mapIdGauge A := by
  simpa [quotientGaugeCoordinateValue] using
    (quotientGaugeUpdate_value_of_ne
      W R D Q (.composition f (𝟙 Y)) (rightUnitorGaugeValue W R D Q f)
      (.identity A) (by intro h; cases h))

/-- The one-coordinate update really corrects the selected right unitor. -/
theorem completeRightUnitor_corrected
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y : W.Localization} (f : X ⟶ Y) :
    completeRightUnitor W R D Q f ∈
      quotientRouteCorrectionLocus W R D (.rightUnitor f) := by
  let Q' := completeRightUnitor W R D Q f
  let L := quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q
  let L' := quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q'
  change quotientRightUnitorDefect W R D L' f = Iso.refl _
  apply (quotientRightUnitorDefect_eq_refl_iff W R D L' f).2
  have hComp :
      L'.mapComp f (𝟙 Y) =
        rightUnitorSourceTransportIso W R D f ≪≫
          (rightUnitorSuffixIso W R D Q f).symm := by
    apply Iso.ext
    change
      (generatedCompositionMapIso W R D f (𝟙 Y)).hom ≫
          (Q'.mapCompGauge f (𝟙 Y)).hom =
        (rightUnitorSourceTransportIso W R D f ≪≫
          (rightUnitorSuffixIso W R D Q f).symm).hom
    rw [show Q'.mapCompGauge f (𝟙 Y) =
        rightUnitorGaugeValue W R D Q f by
      simpa [Q'] using completeRightUnitor_mapCompGauge W R D Q f]
    exact rightUnitorGaugeValue_fac W R D Q f
  have hId : L'.mapId Y = L.mapId Y := by
    change
      generatedIdentityMapIso W R D Y ≪≫ Q'.mapIdGauge Y =
        generatedIdentityMapIso W R D Y ≪≫ Q.mapIdGauge Y
    rw [show Q'.mapIdGauge Y = Q.mapIdGauge Y by
      simpa [Q'] using completeRightUnitor_mapIdGauge W R D Q f Y]
  have hSuffix :
      rightUnitorSuffixIso W R D Q' f =
        rightUnitorSuffixIso W R D Q f := by
    unfold rightUnitorSuffixIso
    rw [hId]
  change
    (L'.mapComp f (𝟙 Y)).hom ≫
        (rightUnitorSuffixIso W R D Q' f).hom =
      (rightUnitorSourceTransportIso W R D f).hom
  rw [hComp, hSuffix]
  simp only [Iso.trans_hom, Iso.symm_hom, Category.assoc,
    Iso.inv_hom_id, Category.comp_id]

/-! ## Correlate all local unitor solutions and glue them -/

/-- Choose the solved local gauge for one unitor route, always from the same
seed Q. -/
noncomputable def locallyCorrectedUnitorGauge
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X : W.Localization} :
    UnitorRouteAt W X → GeneratedQuotientGaugeParameters W R D
  | .left f => completeLeftUnitor W R D Q f
  | .right f => completeRightUnitor W R D Q f

theorem locallyCorrectedUnitorGauge_corrected
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X : W.Localization} (s : UnitorRouteAt W X) :
    locallyCorrectedUnitorGauge W R D Q s ∈
      quotientRouteCorrectionLocus W R D (unitorRouteState W s) := by
  cases s with
  | left f => exact completeLeftUnitor_corrected W R D Q f
  | right f => exact completeRightUnitor_corrected W R D Q f

theorem locallyCorrectedUnitorGauge_mapIdGauge
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X : W.Localization} (s : UnitorRouteAt W X)
    (A : W.Localization) :
    (locallyCorrectedUnitorGauge W R D Q s).mapIdGauge A =
      Q.mapIdGauge A := by
  cases s with
  | left f => exact completeLeftUnitor_mapIdGauge W R D Q f A
  | right f => exact completeRightUnitor_mapIdGauge W R D Q f A

/-- Any two local unitor solutions agree on their actual overlap.  If an
overlap exists, v3.35 first identifies their anchor objects; their mapId values
then agree because every local solver preserved the common seed family. -/
theorem locallyCorrectedUnitorGauge_pairwise
    (Q : GeneratedQuotientGaugeParameters W R D) :
    ∀ X Y (s : UnitorRouteAt W X) (t : UnitorRouteAt W Y),
      AgreeOnRouteFootprintOverlap W R D
        (unitorRouteState W s) (unitorRouteState W t)
        (locallyCorrectedUnitorGauge W R D Q s)
        (locallyCorrectedUnitorGauge W R D Q t) := by
  intro X Y s t c hsc htc
  have hXY : X = Y :=
    unitor_objects_eq_of_shared_coordinate W s t c hsc htc
  subst Y
  have hId :
      (locallyCorrectedUnitorGauge W R D Q s).mapIdGauge X =
        (locallyCorrectedUnitorGauge W R D Q t).mapIdGauge X := by
    rw [locallyCorrectedUnitorGauge_mapIdGauge,
      locallyCorrectedUnitorGauge_mapIdGauge]
  exact
    unitor_overlap_of_corrected_of_mapIdGauge_eq
      W R D s t
      (locallyCorrectedUnitorGauge W R D Q s)
      (locallyCorrectedUnitorGauge W R D Q t)
      (locallyCorrectedUnitorGauge_corrected W R D Q s)
      (locallyCorrectedUnitorGauge_corrected W R D Q t)
      hId c hsc htc

/-- Every seed gauge can therefore be replaced by one fixed gauge correcting
all left and right unitors simultaneously. -/
theorem exists_commonUnitorGauge_from_seed
    (Q : GeneratedQuotientGaugeParameters W R D) :
    ∃ Q' : GeneratedQuotientGaugeParameters W R D,
      ∀ X (s : UnitorRouteAt W X),
        Q' ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s) := by
  let U : (X : W.Localization) →
      UnitorRouteAt W X → GeneratedQuotientGaugeParameters W R D :=
    fun _ s => locallyCorrectedUnitorGauge W R D Q s
  let F : ThreeQuotientRouteState W → GeneratedQuotientGaugeParameters W R D :=
    extendUnitorFamily W R D U
  have hUnit : UnitorRestrictionPairwise W R D F := by
    intro X Y s t
    change AgreeOnRouteFootprintOverlap W R D
      (unitorRouteState W s) (unitorRouteState W t)
      (extendUnitorFamily W R D U (unitorRouteState W s))
      (extendUnitorFamily W R D U (unitorRouteState W t))
    rw [extendUnitorFamily_unitor, extendUnitorFamily_unitor]
    exact locallyCorrectedUnitorGauge_pairwise W R D Q X Y s t
  have hCorrect : ∀ X (s : UnitorRouteAt W X),
      F (unitorRouteState W s) ∈
        quotientRouteCorrectionLocus W R D (unitorRouteState W s) := by
    intro X s
    change extendUnitorFamily W R D U (unitorRouteState W s) ∈
      quotientRouteCorrectionLocus W R D (unitorRouteState W s)
    rw [extendUnitorFamily_unitor]
    exact locallyCorrectedUnitorGauge_corrected W R D Q s
  exact
    ⟨unitorSeedGauge W R D F,
      fun X s => unitorSeedGauge_corrected W R D F hUnit hCorrect s⟩

/-- In particular, common unitor correction requires no hypothesis beyond the
existing quotient-gauge carrier. -/
theorem exists_commonUnitorGauge :
    ∃ Q : GeneratedQuotientGaugeParameters W R D,
      ∀ X (s : UnitorRouteAt W X),
        Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s) := by
  exact exists_commonUnitorGauge_from_seed W R D
    (neutralQuotientGauge W R D)

/-! ## Concrete v2.69 consequence -/

/-- The octahedral C2 model therefore satisfies the last formerly explicit
common-unitor premise of v3.60. -/
theorem counterSystem_exists_commonUnitorGauge :
    ∃ Q : GeneratedQuotientGaugeParameters
        allMorphisms counterSystem counterD,
      ∀ X (s : UnitorRouteAt allMorphisms X),
        Q ∈ quotientRouteCorrectionLocus
          allMorphisms counterSystem counterD (unitorRouteState allMorphisms s) :=
  exists_commonUnitorGauge allMorphisms counterSystem counterD

/-- Concrete exact fixed-gauge inverse-pair obstruction in the v2.69 model.

This combines:
* v3.61: the exact gComp(f,g) dependent fiber is Nontrivial;
* v3.62/v3.63: an explicit object-separated inverse-pair fresh-boundary task;
* v3.58: allMorphisms has both source-complement families;
* v3.64 above: one fixed gauge corrects every unitor.

The conclusion is existence of one fixed gauge preserving every unitor while
failing the selected exact associator leading compatibility.  It is not an
uncorrectability theorem. -/
theorem counterSystem_exists_exactInversePairFreshBoundaryObstruction :
    ∃ Q' : GeneratedQuotientGaugeParameters
        allMorphisms counterSystem counterD,
      (∀ X (s : UnitorRouteAt allMorphisms X),
        Q' ∈ quotientRouteCorrectionLocus
          allMorphisms counterSystem counterD (unitorRouteState allMorphisms s)) ∧
      InversePairFreshBoundaryLeadingObstruction
        allMorphisms counterSystem counterD Q'
        ({ X := counterX, Y := counterY, Z := counterX, T := counterT,
           f := counterInversePairForward,
           g := counterInversePairBackward,
           h := counterInversePairThird } : AssociatorTask allMorphisms) := by
  rcases counterSystem_exists_commonUnitorGauge with ⟨Q, hUnit⟩
  letI : Nontrivial
      (QuotientGaugeCoordinateFiber
        allMorphisms counterSystem counterD
        (.composition counterInversePairForward counterInversePairBackward)) :=
    counterInversePairTask_fgFiber_nontrivial
  exact
    exists_inversePairFreshBoundaryObstruction_of_nontrivial_isolated_fg_of_sourceComplements
      allMorphisms counterSystem counterD
      counterInversePairForward counterInversePairBackward counterInversePairThird
      counterInversePairForward_comp_backward
      counterInversePairBackward_comp_forward
      Q
      counterInversePairTask_geometry.1
      counterInversePairTask_geometry.2.2
      hUnit
      allMorphisms_hasLeftWCompositeComplements
      allMorphisms_hasRightWCompositeComplements

/-!
## Boundary after v3.64

If the theorems above compile under the pinned Lean/Mathlib toolchain, the
common-unitor premise is not an independent obstruction: unitor equations are
always simultaneously gauge-solvable by one-coordinate completion and actual
overlap gluing.

For the concrete v2.69 C2 model, v3.61-v3.64 then provide an explicit existence
theorem for a fixed gauge carrying the exact v3.55
InversePairFreshBoundaryLeadingObstruction.

This still does not prove uncorrectability, universal nonvanishing, weak
admissibility implies full coherent factorization, or final Stage I/II
universality.  It sharpens the truth test by locating a genuine fixed-gauge
associator failure after all unitors have been solved.
-/

end

end KUOS.DependentOriginationUniversalUnitorGaugeV3_64
