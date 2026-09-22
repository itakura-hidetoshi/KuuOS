import KUOS.DependentOriginationAssociatorUnitorBoundaryReductionV3_36
import Mathlib.Logic.Function.Basic

namespace KUOS.DependentOriginationFreshAssociatorCompletionV3_37

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationCoherenceDefectsV2_65
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationQuotientDefectOrbitV3_06
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateFootprintV3_12
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationPairwiseFiniteExtensionV3_15
open KUOS.DependentOriginationAssociatorThreeOfFourRigidityV3_23
open KUOS.DependentOriginationUnitorWitnessCorrelationV3_35
open KUOS.DependentOriginationAssociatorUnitorBoundaryReductionV3_36

universe u v uH vH

set_option autoImplicit false

/-!
# Unique local associator completion at a fresh coordinate v3.37

v3.36 separates the unitor boundary from the remaining associator coordinates.
This layer constructs a local correcting witness, rather than merely reducing
the tests on an already selected family.

Write the actual associator equation as L0.hom followed by B.hom = tau.hom.
Here B is the invertible suffix determined by the other three composition
coordinates, and tau is the equality transport of source associativity.
The required adjusted leading isomorphism is tau followed by B inverse.
Its gauge relative to the canonical leading isomorphism K is therefore
K inverse followed by tau followed by B inverse.

Mathlib's dependent Function.update changes exactly the leading coordinate.
The three other coordinate keys must be different from that key; otherwise
changing the leading value also changes the suffix. Under this freshness
condition the update corrects the route and is the unique one-coordinate
correction. If the leading key is outside the v3.36 unitor boundary, every
unitor footprint and every existing unitor correction is preserved.

The middle-identity triangle fails freshness, as proved below. Thus this
construction does not bypass its separation/correlation problem.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The leading key is different from each of the three suffix keys.
No distinctness among the suffix keys themselves is required. -/
def FreshAssociatorLeadingCoordinate
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) : Prop :=
  QuotientGaugeCoordinate.composition f g ≠ .composition (f ≫ g) h ∧
  QuotientGaugeCoordinate.composition g h ≠ .composition (f ≫ g) h ∧
  QuotientGaugeCoordinate.composition f (g ≫ h) ≠ .composition (f ≫ g) h

/-- In the genuine middle-identity triangle the leading and trailing keys
coincide. Its earlier separation hypotheses cannot be removed by this update. -/
theorem not_freshAssociatorLeadingCoordinate_middle_identity
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ¬ FreshAssociatorLeadingCoordinate W f (𝟙 Y) g := by
  intro H
  exact H.2.2 (by simp only [Category.id_comp, Category.comp_id])

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- Replace one dependent gauge coordinate using Mathlib's dependent update. -/
noncomputable def quotientGaugeUpdate
    (Q : GeneratedQuotientGaugeParameters W R D)
    (c : QuotientGaugeCoordinate W) (value : QuotientGaugeCoordinateFiber W R D c) :
    GeneratedQuotientGaugeParameters W R D := by
  classical
  let values := Function.update (quotientGaugeCoordinateValue W R D Q) c value
  exact
    { mapIdGauge := fun X => values (.identity X)
      mapCompGauge := fun f g => values (.composition f g) }

/-- The updated coordinate contains precisely the requested value. -/
theorem quotientGaugeUpdate_value_self
    (Q : GeneratedQuotientGaugeParameters W R D)
    (c : QuotientGaugeCoordinate W) (value : QuotientGaugeCoordinateFiber W R D c) :
    quotientGaugeCoordinateValue W R D (quotientGaugeUpdate W R D Q c value) c =
      value := by
  classical
  -- Fix the domain and dependent family before eliminating the coordinate key.
  have hUpdate :
      Function.update (quotientGaugeCoordinateValue W R D Q) c value c = value :=
    Function.update_self c value (quotientGaugeCoordinateValue W R D Q)
  cases c <;> exact hUpdate

/-- All other coordinates are literally unchanged, including dependent fibers. -/
theorem quotientGaugeUpdate_value_of_ne
    (Q : GeneratedQuotientGaugeParameters W R D)
    (c : QuotientGaugeCoordinate W) (value : QuotientGaugeCoordinateFiber W R D c)
    (d : QuotientGaugeCoordinate W) (hd : d ≠ c) :
    quotientGaugeCoordinateValue W R D (quotientGaugeUpdate W R D Q c value) d =
      quotientGaugeCoordinateValue W R D Q d := by
  classical
  cases d <;> exact Function.update_of_ne hd value (quotientGaugeCoordinateValue W R D Q)

/-- A route not inspecting the changed coordinate retains its entire footprint. -/
theorem quotientGaugeUpdate_agrees_of_not_mem
    (Q : GeneratedQuotientGaugeParameters W R D)
    (c : QuotientGaugeCoordinate W) (value : QuotientGaugeCoordinateFiber W R D c)
    (s : ThreeQuotientRouteState W) (hs : ¬ RouteFootprintContains W s c) :
    QuotientGaugesAgreeOnRouteState W R D
      (quotientGaugeUpdate W R D Q c value) Q s := by
  apply quotientGaugesAgreeOnRouteState_of_coordinateValue_eq W R D
  intro d hd
  exact quotientGaugeUpdate_value_of_ne W R D Q c value d
    (fun hdc => hs (hdc ▸ hd))

/-- Reuse actual footprint locality to preserve correction of every untouched route. -/
theorem quotientGaugeUpdate_mem_locus_iff_of_not_mem
    (Q : GeneratedQuotientGaugeParameters W R D)
    (c : QuotientGaugeCoordinate W) (value : QuotientGaugeCoordinateFiber W R D c)
    (s : ThreeQuotientRouteState W) (hs : ¬ RouteFootprintContains W s c) :
    quotientGaugeUpdate W R D Q c value ∈ quotientRouteCorrectionLocus W R D s ↔
      Q ∈ quotientRouteCorrectionLocus W R D s := by
  exact quotientRouteCorrectedBy_congr_of_agreesOnRouteState W R D
    (quotientGaugeUpdate W R D Q c value) Q s
    (quotientGaugeUpdate_agrees_of_not_mem W R D Q c value s hs)

/-- The invertible suffix in the existing v2.65 associator equation. Keeping it
as one Iso avoids reconstructing invertibility of a long 2-cell expression. -/
noncomputable def associatorSuffixIso
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y Z T : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) :
    (quotientRepresentativeMap W R D (f ≫ g) ≫ quotientRepresentativeMap W R D h) ≅
      quotientRepresentativeMap W R D (f ≫ (g ≫ h)) :=
  whiskerRightIso
    ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp f g)
    (quotientRepresentativeMap W R D h) ≪≫
  ((α_ (quotientRepresentativeMap W R D f)
      (quotientRepresentativeMap W R D g) (quotientRepresentativeMap W R D h)) ≪≫
    (whiskerLeftIso (quotientRepresentativeMap W R D f)
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp g h).symm ≪≫
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp f (g ≫ h)).symm))

/-- Source associativity gives equality transport, not a strict evaluation law. -/
noncomputable def associatorSourceTransportIso
    {X Y Z T : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) :
    quotientRepresentativeMap W R D ((f ≫ g) ≫ h) ≅
      quotientRepresentativeMap W R D (f ≫ (g ≫ h)) :=
  eqToIso (by rw [Category.assoc])

/-- Solve the leading gauge using the canonical leading isomorphism and the
unchanged suffix. This definition alone does not assert freshness. -/
noncomputable def associatorLeadingGaugeValue
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y Z T : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) :
    QuotientGaugeCoordinateFiber W R D (.composition (f ≫ g) h) :=
  (generatedCompositionMapIso W R D (f ≫ g) h).symm ≪≫
    (associatorSourceTransportIso W R D f g h ≪≫
      (associatorSuffixIso W R D Q f g h).symm)

/-- Cancellation of the canonical leading isomorphism gives the solved prefix. -/
theorem associatorLeadingGaugeValue_fac
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y Z T : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) :
    (generatedCompositionMapIso W R D (f ≫ g) h).hom ≫
        (associatorLeadingGaugeValue W R D Q f g h).hom =
      (associatorSourceTransportIso W R D f g h ≪≫
        (associatorSuffixIso W R D Q f g h).symm).hom := by
  simp only [associatorLeadingGaugeValue, Iso.trans_hom, Iso.symm_hom,
    Iso.hom_inv_id_assoc]

/-- Apply the solved leading value to the actual full quotient-gauge family. -/
noncomputable def completeAssociatorLeading
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y Z T : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) :
    GeneratedQuotientGaugeParameters W R D :=
  quotientGaugeUpdate W R D Q (.composition (f ≫ g) h)
    (associatorLeadingGaugeValue W R D Q f g h)

private theorem adjustedMapComp_congr
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z)
    (H : Q.mapCompGauge f g = Q'.mapCompGauge f g) :
    (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp f g =
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp f g := by
  change generatedCompositionMapIso W R D f g ≪≫ Q.mapCompGauge f g =
    generatedCompositionMapIso W R D f g ≪≫ Q'.mapCompGauge f g
  rw [H]

/-- With three noncolliding suffix keys, the single update satisfies the actual
associator equation. There is no assumed correcting witness in the input. -/
theorem completeAssociatorLeading_corrected
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y Z T : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T)
    (hFresh : FreshAssociatorLeadingCoordinate W f g h) :
    completeAssociatorLeading W R D Q f g h ∈
      quotientRouteCorrectionLocus W R D (.associator f g h) := by
  let Q' := completeAssociatorLeading W R D Q f g h
  have hfg : Q'.mapCompGauge f g = Q.mapCompGauge f g :=
    quotientGaugeUpdate_value_of_ne W R D Q (.composition (f ≫ g) h)
      (associatorLeadingGaugeValue W R D Q f g h) (.composition f g) hFresh.1
  have hgh : Q'.mapCompGauge g h = Q.mapCompGauge g h :=
    quotientGaugeUpdate_value_of_ne W R D Q (.composition (f ≫ g) h)
      (associatorLeadingGaugeValue W R D Q f g h) (.composition g h) hFresh.2.1
  have hfgh : Q'.mapCompGauge f (g ≫ h) = Q.mapCompGauge f (g ≫ h) :=
    quotientGaugeUpdate_value_of_ne W R D Q (.composition (f ≫ g) h)
      (associatorLeadingGaugeValue W R D Q f g h) (.composition f (g ≫ h)) hFresh.2.2
  have hfg' := adjustedMapComp_congr W R D Q' Q f g hfg
  have hgh' := adjustedMapComp_congr W R D Q' Q g h hgh
  have hfgh' := adjustedMapComp_congr W R D Q' Q f (g ≫ h) hfgh
  have hSuffix : associatorSuffixIso W R D Q' f g h =
      associatorSuffixIso W R D Q f g h := by
    unfold associatorSuffixIso
    rw [hfg', hgh', hfgh']
  have hAt : Q'.mapCompGauge (f ≫ g) h = associatorLeadingGaugeValue W R D Q f g h :=
    quotientGaugeUpdate_value_self W R D Q (.composition (f ≫ g) h)
      (associatorLeadingGaugeValue W R D Q f g h)
  have hPrefix :
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp (f ≫ g) h).hom =
        (associatorSourceTransportIso W R D f g h ≪≫
          (associatorSuffixIso W R D Q f g h).symm).hom := by
    change (generatedCompositionMapIso W R D (f ≫ g) h).hom ≫
      (Q'.mapCompGauge (f ≫ g) h).hom = _
    rw [hAt]
    exact associatorLeadingGaugeValue_fac W R D Q f g h
  change quotientAssociatorDefect W R D
    (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q') f g h = Iso.refl _
  apply (quotientAssociatorDefect_eq_refl_iff W R D
    (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q') f g h).2
  change ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp (f ≫ g) h).hom ≫
      (associatorSuffixIso W R D Q' f g h).hom =
    (associatorSourceTransportIso W R D f g h).hom
  rw [hPrefix, hSuffix]
  simp only [Iso.trans_hom, Iso.symm_hom, Category.assoc, Iso.inv_hom_id, Category.comp_id]

/-- The solved value is the unique possible correction when only the leading
coordinate may change. Uniqueness reuses the concrete v3.23 rigidity theorem. -/
theorem existsUnique_associatorLeadingCorrection
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y Z T : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T)
    (hFresh : FreshAssociatorLeadingCoordinate W f g h) :
    ∃! value : QuotientGaugeCoordinateFiber W R D (.composition (f ≫ g) h),
      quotientGaugeUpdate W R D Q (.composition (f ≫ g) h) value ∈
        quotientRouteCorrectionLocus W R D (.associator f g h) := by
  let value := associatorLeadingGaugeValue W R D Q f g h
  have hDone := completeAssociatorLeading_corrected W R D Q f g h hFresh
  refine ⟨value, hDone, ?_⟩
  intro candidate hCandidate
  have hOther (d : QuotientGaugeCoordinate W) (hd : d ≠ .composition (f ≫ g) h) :
      quotientGaugeCoordinateValue W R D
          (quotientGaugeUpdate W R D Q (.composition (f ≫ g) h) candidate) d =
        quotientGaugeCoordinateValue W R D
          (quotientGaugeUpdate W R D Q (.composition (f ≫ g) h) value) d :=
    (quotientGaugeUpdate_value_of_ne W R D Q (.composition (f ≫ g) h) candidate d hd).trans
      (quotientGaugeUpdate_value_of_ne W R D Q (.composition (f ≫ g) h) value d hd).symm
  have hEq := associator_mapComp_fgg_h_eq_of_corrected_of_other_three_eq
    W R D f g h
    (quotientGaugeUpdate W R D Q (.composition (f ≫ g) h) candidate)
    (quotientGaugeUpdate W R D Q (.composition (f ≫ g) h) value)
    hCandidate hDone
    (hOther (.composition f g) hFresh.1)
    (hOther (.composition g h) hFresh.2.1)
    (hOther (.composition f (g ≫ h)) hFresh.2.2)
  exact (quotientGaugeUpdate_value_self W R D Q (.composition (f ≫ g) h) candidate).symm.trans
    (hEq.trans (quotientGaugeUpdate_value_self W R D Q (.composition (f ≫ g) h) value))

/-- An interior leading update leaves every visible unitor-boundary value fixed. -/
theorem completeAssociatorLeading_boundary_value_eq
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y Z T : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T)
    (hInterior : ¬ UnitorVisibleCoordinate W (.composition (f ≫ g) h))
    (c : QuotientGaugeCoordinate W) (hc : UnitorVisibleCoordinate W c) :
    quotientGaugeCoordinateValue W R D (completeAssociatorLeading W R D Q f g h) c =
      quotientGaugeCoordinateValue W R D Q c := by
  exact quotientGaugeUpdate_value_of_ne W R D Q (.composition (f ≫ g) h)
    (associatorLeadingGaugeValue W R D Q f g h) c
    (fun hcc => hInterior (hcc ▸ hc))

/-- Every unitor footprint, not merely its correction truth value, is preserved. -/
theorem completeAssociatorLeading_agrees_on_unitors
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y Z T : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T)
    (hInterior : ¬ UnitorVisibleCoordinate W (.composition (f ≫ g) h))
    {A : W.Localization} (s : UnitorRouteAt W A) :
    QuotientGaugesAgreeOnRouteState W R D
      (completeAssociatorLeading W R D Q f g h) Q (unitorRouteState W s) := by
  exact quotientGaugeUpdate_agrees_of_not_mem W R D Q (.composition (f ≫ g) h)
    (associatorLeadingGaugeValue W R D Q f g h) (unitorRouteState W s)
    (fun hs => hInterior (unitorVisibleCoordinate_of_mem W s (.composition (f ≫ g) h) hs))

/-- In particular, all previously corrected unitors stay corrected. -/
theorem completeAssociatorLeading_unitor_corrected_iff
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y Z T : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T)
    (hInterior : ¬ UnitorVisibleCoordinate W (.composition (f ≫ g) h))
    {A : W.Localization} (s : UnitorRouteAt W A) :
    completeAssociatorLeading W R D Q f g h ∈
        quotientRouteCorrectionLocus W R D (unitorRouteState W s) ↔
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s) := by
  exact quotientRouteCorrectedBy_congr_of_agreesOnRouteState W R D
    (completeAssociatorLeading W R D Q f g h) Q (unitorRouteState W s)
    (completeAssociatorLeading_agrees_on_unitors W R D Q f g h hInterior s)

/-!
## Boundary

The new result is local existence and unique one-coordinate completion under
explicit key freshness. Boundary preservation additionally requires that the
changed key is not unitor-visible. The original gauge need not already correct
the target associator, and no new gluing or separation assumption is inserted.

Overlapping associator routes can still inspect the changed key. The generic
untouched-route theorem applies only when that key is absent from their actual
footprints. No simultaneous solution of all associator equations follows yet.
In particular the middle-identity incidence is explicitly outside freshness.
Fixed W/R/D, all earlier mixed-triangle hypotheses, comparison coherence,
general Stage I, Stage II and final universality retain their existing scope.
-/

end KUOS.DependentOriginationFreshAssociatorCompletionV3_37
