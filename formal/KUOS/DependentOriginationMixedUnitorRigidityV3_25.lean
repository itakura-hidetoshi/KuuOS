import KUOS.DependentOriginationUnitorStarTransitivityV3_24

namespace KUOS.DependentOriginationMixedUnitorRigidityV3_25

open CategoryTheory
open CategoryTheory.Bicategory
open Set
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
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
open KUOS.DependentOriginationPairwiseFiniteExtensionV3_15
open KUOS.DependentOriginationUnitorPartialRigidityV3_22
open KUOS.DependentOriginationUnitorStarTransitivityV3_24

universe u v uH vH uB vB wB

/-!
# Actual mixed unitor rigidity v3.25

v3.24 closes homogeneous left/left/left and right/right/right stars sharing one
identity coordinate.  The remaining unitor interaction is mixed left/right.

At the only nontrivial mixed composition overlap, both route morphisms are the
identity.  The left and right defect equations then differ only by the two
canonical ways of contracting an invertible 2-cell

  A : P ≅ 𝟙

against the left and right unitors.  Bicategory coherence forces those two
contractions to coincide.  The proof below uses only left- and right-unitor
naturality, whisker exchange, unitors_equal, and cancellation by A.

Thus no new abstract correlation axiom is introduced.
-/

/-- An invertible 2-cell from a 1-cell to the identity has the same left and
right contraction. -/
theorem isoToIdentity_whisker_unitor_balance
    {B : Type uB} [Bicategory.{wB, vB} B]
    {a : B} (P : a ⟶ a) (A : P ≅ 𝟙 a) :
    (A.hom ▷ P) ≫ (λ_ P).hom =
      (P ◁ A.hom) ≫ (ρ_ P).hom := by
  apply (cancel_mono A.hom).1
  calc
    ((A.hom ▷ P) ≫ (λ_ P).hom) ≫ A.hom =
        (A.hom ▷ P) ≫
          ((𝟙 a ◁ A.hom) ≫ (λ_ (𝟙 a)).hom) := by
            rw [Category.assoc, ← leftUnitor_naturality]
    _ =
        ((A.hom ▷ P) ≫ (𝟙 a ◁ A.hom)) ≫
          (λ_ (𝟙 a)).hom := by
            simp only [Category.assoc]
    _ =
        ((P ◁ A.hom) ≫ (A.hom ▷ 𝟙 a)) ≫
          (λ_ (𝟙 a)).hom := by
            rw [whisker_exchange]
    _ =
        ((P ◁ A.hom) ≫ (A.hom ▷ 𝟙 a)) ≫
          (ρ_ (𝟙 a)).hom := by
            rw [unitors_equal]
    _ =
        (P ◁ A.hom) ≫
          ((A.hom ▷ 𝟙 a) ≫ (ρ_ (𝟙 a)).hom) := by
            simp only [Category.assoc]
    _ =
        (P ◁ A.hom) ≫ ((ρ_ P).hom ≫ A.hom) := by
            rw [rightUnitor_naturality]
    _ = ((P ◁ A.hom) ≫ (ρ_ P).hom) ≫ A.hom := by
            simp only [Category.assoc]

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- At the identity morphism, a correcting left-unitor gauge and a correcting
right-unitor gauge with the same identity-gauge coordinate must also have the
same composition-gauge coordinate. -/
theorem mixedUnitor_identity_mapCompGauge_eq_of_corrected_of_mapIdGauge_eq
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (X : W.Localization)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    (hQ :
      Q ∈ quotientRouteCorrectionLocus W R D (.leftUnitor (𝟙 X)))
    (hQ' :
      Q' ∈ quotientRouteCorrectionLocus W R D (.rightUnitor (𝟙 X)))
    (hId : Q.mapIdGauge X = Q'.mapIdGauge X) :
    Q.mapCompGauge (𝟙 X) (𝟙 X) =
      Q'.mapCompGauge (𝟙 X) (𝟙 X) := by
  change
    quotientLeftUnitorDefect W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q) (𝟙 X) =
        Iso.refl _ at hQ
  change
    quotientRightUnitorDefect W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q') (𝟙 X) =
        Iso.refl _ at hQ'
  have hEqQ :=
    (quotientLeftUnitorDefect_eq_refl_iff W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q) (𝟙 X)).1 hQ
  have hEqQ' :=
    (quotientRightUnitorDefect_eq_refl_iff W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q') (𝟙 X)).1 hQ'
  have hAdjustedId :
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId X =
        (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapId X := by
    simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg
        (fun q => generatedIdentityMapIso W R D X ≪≫ q)
        hId
  have hAdjustedIdHom := congrArg Iso.hom hAdjustedId
  have hSuffix :
      (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId X).hom ▷
          quotientRepresentativeMap W R D (𝟙 X)) ≫
          (λ_ (quotientRepresentativeMap W R D (𝟙 X))).hom =
        (quotientRepresentativeMap W R D (𝟙 X) ◁
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId X).hom) ≫
          (ρ_ (quotientRepresentativeMap W R D (𝟙 X))).hom := by
    exact
      isoToIdentity_whisker_unitor_balance
        (quotientRepresentativeMap W R D (𝟙 X))
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId X)
  have hComposite :
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
          (𝟙 X) (𝟙 X)).hom ≫
          ((((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId X).hom ▷
            quotientRepresentativeMap W R D (𝟙 X)) ≫
          (λ_ (quotientRepresentativeMap W R D (𝟙 X))).hom) =
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
          (𝟙 X) (𝟙 X)).hom ≫
          ((((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId X).hom ▷
            quotientRepresentativeMap W R D (𝟙 X)) ≫
          (λ_ (quotientRepresentativeMap W R D (𝟙 X))).hom) := by
    calc
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
          (𝟙 X) (𝟙 X)).hom ≫
          ((((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId X).hom ▷
            quotientRepresentativeMap W R D (𝟙 X)) ≫
          (λ_ (quotientRepresentativeMap W R D (𝟙 X))).hom) =
          eqToHom (by simp) := by
            simpa only [Category.assoc] using hEqQ
      _ =
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
            (𝟙 X) (𝟙 X)).hom ≫
            ((quotientRepresentativeMap W R D (𝟙 X) ◁
              ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapId X).hom) ≫
            (ρ_ (quotientRepresentativeMap W R D (𝟙 X))).hom) := by
              simpa only [Category.assoc] using hEqQ'.symm
      _ =
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
            (𝟙 X) (𝟙 X)).hom ≫
            ((quotientRepresentativeMap W R D (𝟙 X) ◁
              ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId X).hom) ≫
            (ρ_ (quotientRepresentativeMap W R D (𝟙 X))).hom) := by
              rw [hAdjustedIdHom]
      _ =
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
            (𝟙 X) (𝟙 X)).hom ≫
            ((((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId X).hom ▷
              quotientRepresentativeMap W R D (𝟙 X)) ≫
            (λ_ (quotientRepresentativeMap W R D (𝟙 X))).hom) := by
              rw [hSuffix]
  have hAdjustedCompHom :
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
        (𝟙 X) (𝟙 X)).hom =
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
          (𝟙 X) (𝟙 X)).hom := by
    apply
      (cancel_mono
        ((((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId X).hom ▷
            quotientRepresentativeMap W R D (𝟙 X)) ≫
          (λ_ (quotientRepresentativeMap W R D (𝟙 X))).hom)).1
    simpa only [Category.assoc] using hComposite
  have hGaugeHom :
      (Q.mapCompGauge (𝟙 X) (𝟙 X)).hom =
        (Q'.mapCompGauge (𝟙 X) (𝟙 X)).hom := by
    apply
      (cancel_epi
        (generatedCompositionMapIso W R D (𝟙 X) (𝟙 X)).hom).1
    simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters,
      Iso.trans_hom] using hAdjustedCompHom
  apply Iso.ext
  exact hGaugeHom

/-- A correcting left-unitor and a correcting right-unitor that share the same
identity coordinate agree on every literal overlap coordinate once that
identity-gauge value agrees. -/
theorem leftUnitor_rightUnitor_agreeOnRouteFootprintOverlap_of_corrected_of_mapIdGauge_eq
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : Z ⟶ X)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    (hQ : Q ∈ quotientRouteCorrectionLocus W R D (.leftUnitor f))
    (hQ' : Q' ∈ quotientRouteCorrectionLocus W R D (.rightUnitor g))
    (hId : Q.mapIdGauge X = Q'.mapIdGauge X) :
    AgreeOnRouteFootprintOverlap W R D
      (.leftUnitor f) (.rightUnitor g) Q Q' := by
  intro c hc hc'
  simp only [RouteFootprintContains] at hc hc'
  rcases hc with hc | hc
  · subst c
    rcases hc' with hc' | hc'
    · cases hc'
      simpa [quotientGaugeCoordinateValue] using
        mixedUnitor_identity_mapCompGauge_eq_of_corrected_of_mapIdGauge_eq
          W R D X Q Q' hQ hQ' hId
    · cases hc'
  · subst c
    rcases hc' with hc' | hc'
    · cases hc'
    · cases hc'
      simpa [quotientGaugeCoordinateValue] using hId

/-- Symmetric orientation of the mixed-unitor overlap theorem. -/
theorem rightUnitor_leftUnitor_agreeOnRouteFootprintOverlap_of_corrected_of_mapIdGauge_eq
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization}
    (f : Y ⟶ X) (g : X ⟶ Z)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    (hQ : Q ∈ quotientRouteCorrectionLocus W R D (.rightUnitor f))
    (hQ' : Q' ∈ quotientRouteCorrectionLocus W R D (.leftUnitor g))
    (hId : Q.mapIdGauge X = Q'.mapIdGauge X) :
    AgreeOnRouteFootprintOverlap W R D
      (.rightUnitor f) (.leftUnitor g) Q Q' := by
  apply
    (agreeOnRouteFootprintOverlap_symm W R D
      (.leftUnitor g) (.rightUnitor f) Q' Q).1
  exact
    leftUnitor_rightUnitor_agreeOnRouteFootprintOverlap_of_corrected_of_mapIdGauge_eq
      W R D g f Q' Q hQ' hQ hId.symm

/-- A left-unitor anchor with one left and one right endpoint closes the mixed
endpoint edge whenever all three routes share the same identity coordinate. -/
theorem leftUnitorAnchor_mixed_overlapStar_triangle
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : X ⟶ Z) (h : T ⟶ X)
    (Qs Qt Qu : GeneratedQuotientGaugeParameters W R D)
    (hQt : Qt ∈ quotientRouteCorrectionLocus W R D (.leftUnitor g))
    (hQu : Qu ∈ quotientRouteCorrectionLocus W R D (.rightUnitor h))
    (hst : AgreeOnRouteFootprintOverlap W R D
      (.leftUnitor f) (.leftUnitor g) Qs Qt)
    (hsu : AgreeOnRouteFootprintOverlap W R D
      (.leftUnitor f) (.rightUnitor h) Qs Qu) :
    AgreeOnRouteFootprintOverlap W R D
      (.leftUnitor g) (.rightUnitor h) Qt Qu := by
  have hstId : Qs.mapIdGauge X = Qt.mapIdGauge X := by
    simpa [quotientGaugeCoordinateValue] using
      hst (.identity X)
        (by simp [RouteFootprintContains])
        (by simp [RouteFootprintContains])
  have hsuId : Qs.mapIdGauge X = Qu.mapIdGauge X := by
    simpa [quotientGaugeCoordinateValue] using
      hsu (.identity X)
        (by simp [RouteFootprintContains])
        (by simp [RouteFootprintContains])
  exact
    leftUnitor_rightUnitor_agreeOnRouteFootprintOverlap_of_corrected_of_mapIdGauge_eq
      W R D g h Qt Qu hQt hQu (hstId.symm.trans hsuId)

/-- A right-unitor anchor with one left and one right endpoint closes the mixed
endpoint edge whenever all three routes share the same identity coordinate. -/
theorem rightUnitorAnchor_mixed_overlapStar_triangle
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z T : W.Localization}
    (f : Y ⟶ X) (g : X ⟶ Z) (h : T ⟶ X)
    (Qs Qt Qu : GeneratedQuotientGaugeParameters W R D)
    (hQt : Qt ∈ quotientRouteCorrectionLocus W R D (.leftUnitor g))
    (hQu : Qu ∈ quotientRouteCorrectionLocus W R D (.rightUnitor h))
    (hst : AgreeOnRouteFootprintOverlap W R D
      (.rightUnitor f) (.leftUnitor g) Qs Qt)
    (hsu : AgreeOnRouteFootprintOverlap W R D
      (.rightUnitor f) (.rightUnitor h) Qs Qu) :
    AgreeOnRouteFootprintOverlap W R D
      (.leftUnitor g) (.rightUnitor h) Qt Qu := by
  have hstId : Qs.mapIdGauge X = Qt.mapIdGauge X := by
    simpa [quotientGaugeCoordinateValue] using
      hst (.identity X)
        (by simp [RouteFootprintContains])
        (by simp [RouteFootprintContains])
  have hsuId : Qs.mapIdGauge X = Qu.mapIdGauge X := by
    simpa [quotientGaugeCoordinateValue] using
      hsu (.identity X)
        (by simp [RouteFootprintContains])
        (by simp [RouteFootprintContains])
  exact
    leftUnitor_rightUnitor_agreeOnRouteFootprintOverlap_of_corrected_of_mapIdGauge_eq
      W R D g h Qt Qu hQt hQu (hstId.symm.trans hsuId)

/-!
## Frontier after v3.25

Together v3.24 and v3.25 close every unitor triangle whose three route
footprints meet on one common identity coordinate: homogeneous left and right
stars, and either anchor orientation with mixed endpoints.

The mixed case is not an extra rigidity assumption.  Its missing composition
edge is forced by the actual left/right correction equations plus bicategory
unit coherence.

The next genuinely new incidence pattern is therefore associator + unitor.
There the shared coordinates are composition gauges, and v3.23's associator
three-of-four law must propagate them across a triangle.
-/

end KUOS.DependentOriginationMixedUnitorRigidityV3_25
