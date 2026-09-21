import KUOS.DependentOriginationMixedUnitorRigidityV3_25

namespace KUOS.DependentOriginationAssociatorUnitorTriangleV3_26

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
open KUOS.DependentOriginationAssociatorThreeOfFourRigidityV3_23
open KUOS.DependentOriginationMixedUnitorRigidityV3_25

universe u v uH vH

/-!
# Associator-unitor triangle residual v3.26

For composable localization morphisms

  f : X ⟶ Y,  g : Y ⟶ Z,

the unit-generated associator state

  associator f (𝟙 Y) g

meets the right-unitor state at f in the composition coordinate
gComp(f, 𝟙 Y), and meets the left-unitor state at g in
gComp(𝟙 Y, g).

The actual corrected associator equation, together with the two corrected
unitor equations and the bicategory triangle identity, forces the two endpoint
identity witnesses to agree after sandwiching by the representative maps of f
and g.

This is the exact unconditional conclusion.  In a general bicategory,
whiskering need not be faithful, so equality after sandwiching does not by
itself imply equality of the raw identity-gauge coordinate.  We therefore
isolate the minimal local separation property needed to lift this residual
equality back to the literal gId(Y) coordinate and hence close the overlap-star
triangle.

No global faithfulness hypothesis and no abstract gluing axiom is introduced.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Local separation of 2-cells from the representative of the identity to the
actual identity after left/right sandwiching by the representative maps of f
and g. -/
def UnitIdentitySandwichSeparating
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) : Prop :=
  ∀
    (η θ :
      quotientRepresentativeMap W R D (𝟙 Y) ⟶
        𝟙 (R.obj (.mk Y.as.obj))),
    ((quotientRepresentativeMap W R D f ◁ η) ▷
        quotientRepresentativeMap W R D g) =
      ((quotientRepresentativeMap W R D f ◁ θ) ▷
        quotientRepresentativeMap W R D g) →
    η = θ

/-- The actual associator/right-unitor/left-unitor correction triangle forces
the endpoint adjusted identity witnesses to agree after sandwiching.

This is the unconditional triangle residual; no faithfulness assumption is
used. -/
theorem associator_right_left_triangle_adjusted_mapId_sandwich_eq
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (Qs Qt Qu : GeneratedQuotientGaugeParameters W R D)
    (hQs :
      Qs ∈ quotientRouteCorrectionLocus W R D
        (.associator f (𝟙 Y) g))
    (hQt :
      Qt ∈ quotientRouteCorrectionLocus W R D (.rightUnitor f))
    (hQu :
      Qu ∈ quotientRouteCorrectionLocus W R D (.leftUnitor g))
    (hRightComp :
      Qs.mapCompGauge f (𝟙 Y) = Qt.mapCompGauge f (𝟙 Y))
    (hLeftComp :
      Qs.mapCompGauge (𝟙 Y) g = Qu.mapCompGauge (𝟙 Y) g) :
    ((quotientRepresentativeMap W R D f ◁
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt).mapId Y).hom) ▷
      quotientRepresentativeMap W R D g) =
    ((quotientRepresentativeMap W R D f ◁
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu).mapId Y).hom) ▷
      quotientRepresentativeMap W R D g) := by
  change
    quotientAssociatorDefect W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qs)
      f (𝟙 Y) g = Iso.refl _ at hQs
  change
    quotientRightUnitorDefect W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt)
      f = Iso.refl _ at hQt
  change
    quotientLeftUnitorDefect W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu)
      g = Iso.refl _ at hQu

  have hAssoc0 :=
    (quotientAssociatorDefect_eq_refl_iff W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qs)
      f (𝟙 Y) g).1 hQs
  have hRight0 :=
    (quotientRightUnitorDefect_eq_refl_iff W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt)
      f).1 hQt
  have hLeft0 :=
    (quotientLeftUnitorDefect_eq_refl_iff W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu)
      g).1 hQu

  have hAdjustedRightComp :
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qs).mapComp
          f (𝟙 Y) =
        (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt).mapComp
          f (𝟙 Y) := by
    simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg
        (fun q => generatedCompositionMapIso W R D f (𝟙 Y) ≪≫ q)
        hRightComp

  have hAdjustedLeftComp :
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qs).mapComp
          (𝟙 Y) g =
        (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu).mapComp
          (𝟙 Y) g := by
    simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg
        (fun q => generatedCompositionMapIso W R D (𝟙 Y) g ≪≫ q)
        hLeftComp

  have hAdjustedRightCompHom := congrArg Iso.hom hAdjustedRightComp
  have hAdjustedLeftCompHom := congrArg Iso.hom hAdjustedLeftComp

  have hAssoc :
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qs).mapComp
          f g).hom ≫
        (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qs).mapComp
          f (𝟙 Y)).hom ▷ quotientRepresentativeMap W R D g) ≫
        (α_
          (quotientRepresentativeMap W R D f)
          (quotientRepresentativeMap W R D (𝟙 Y))
          (quotientRepresentativeMap W R D g)).hom ≫
        (quotientRepresentativeMap W R D f ◁
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qs).mapComp
            (𝟙 Y) g).inv) ≫
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qs).mapComp
          f g).inv =
        𝟙 _ := by
    simpa using hAssoc0

  have hAssocMiddle :
      (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qs).mapComp
          f (𝟙 Y)).hom ▷ quotientRepresentativeMap W R D g) ≫
        (α_
          (quotientRepresentativeMap W R D f)
          (quotientRepresentativeMap W R D (𝟙 Y))
          (quotientRepresentativeMap W R D g)).hom ≫
        (quotientRepresentativeMap W R D f ◁
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qs).mapComp
            (𝟙 Y) g).inv) =
        𝟙 _ := by
    apply
      (cancel_epi
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qs).mapComp
          f g).hom).1
    apply
      (cancel_mono
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qs).mapComp
          f g).inv).1
    simpa only [Category.assoc, Iso.hom_inv_id, Category.comp_id] using hAssoc

  have hCompBridge :
      (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt).mapComp
          f (𝟙 Y)).hom ▷ quotientRepresentativeMap W R D g) ≫
        (α_
          (quotientRepresentativeMap W R D f)
          (quotientRepresentativeMap W R D (𝟙 Y))
          (quotientRepresentativeMap W R D g)).hom =
        quotientRepresentativeMap W R D f ◁
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu).mapComp
            (𝟙 Y) g).hom := by
    apply
      (cancel_mono
        (quotientRepresentativeMap W R D f ◁
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu).mapComp
            (𝟙 Y) g).inv)).1
    rw [← hAdjustedRightCompHom, ← congrArg Iso.inv hAdjustedLeftComp]
    simpa only [Category.assoc, whiskerLeft_hom_inv, Category.comp_id] using
      hAssocMiddle

  have hRight :
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt).mapComp
          f (𝟙 Y)).hom ≫
        (quotientRepresentativeMap W R D f ◁
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt).mapId
            Y).hom) ≫
        (ρ_ (quotientRepresentativeMap W R D f)).hom =
        𝟙 _ := by
    simpa using hRight0

  have hLeft :
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu).mapComp
          (𝟙 Y) g).hom ≫
        (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu).mapId
            Y).hom ▷ quotientRepresentativeMap W R D g) ≫
        (λ_ (quotientRepresentativeMap W R D g)).hom =
        𝟙 _ := by
    simpa using hLeft0

  have hRightWhiskered :
      (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt).mapComp
          f (𝟙 Y)).hom ▷ quotientRepresentativeMap W R D g) ≫
        ((quotientRepresentativeMap W R D f ◁
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt).mapId
            Y).hom) ▷ quotientRepresentativeMap W R D g) ≫
        ((ρ_ (quotientRepresentativeMap W R D f)).hom ▷
          quotientRepresentativeMap W R D g) =
        𝟙 _ := by
    simpa only [comp_whiskerRight, id_whiskerRight, Category.assoc] using
      congrArg
        (fun η => η ▷ quotientRepresentativeMap W R D g)
        hRight

  have hLeftWhiskered :
      (quotientRepresentativeMap W R D f ◁
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu).mapComp
          (𝟙 Y) g).hom) ≫
        (quotientRepresentativeMap W R D f ◁
          (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu).mapId
            Y).hom ▷ quotientRepresentativeMap W R D g)) ≫
        (quotientRepresentativeMap W R D f ◁
          (λ_ (quotientRepresentativeMap W R D g)).hom) =
        𝟙 _ := by
    simpa only [whiskerLeft_comp, whiskerLeft_id, Category.assoc] using
      congrArg
        (fun η => quotientRepresentativeMap W R D f ◁ η)
        hLeft

  have hLeftNormal :
      (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt).mapComp
          f (𝟙 Y)).hom ▷ quotientRepresentativeMap W R D g) ≫
        ((quotientRepresentativeMap W R D f ◁
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu).mapId
            Y).hom) ▷ quotientRepresentativeMap W R D g) ≫
        ((ρ_ (quotientRepresentativeMap W R D f)).hom ▷
          quotientRepresentativeMap W R D g) =
        𝟙 _ := by
    calc
      (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt).mapComp
          f (𝟙 Y)).hom ▷ quotientRepresentativeMap W R D g) ≫
        ((quotientRepresentativeMap W R D f ◁
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu).mapId
            Y).hom) ▷ quotientRepresentativeMap W R D g) ≫
        ((ρ_ (quotientRepresentativeMap W R D f)).hom ▷
          quotientRepresentativeMap W R D g) =
        (quotientRepresentativeMap W R D f ◁
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu).mapComp
            (𝟙 Y) g).hom) ≫
        (quotientRepresentativeMap W R D f ◁
          (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu).mapId
            Y).hom ▷ quotientRepresentativeMap W R D g)) ≫
        (quotientRepresentativeMap W R D f ◁
          (λ_ (quotientRepresentativeMap W R D g)).hom) := by
            rw [← hCompBridge]
            simp only [Category.assoc]
            rw [← associator_naturality_middle]
            simpa only [Category.assoc] using
              triangle_assoc_comp_left
                (quotientRepresentativeMap W R D f)
                (quotientRepresentativeMap W R D g)
      _ = 𝟙 _ := hLeftWhiskered

  apply
    (cancel_epi
      (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt).mapComp
        f (𝟙 Y)).hom ▷ quotientRepresentativeMap W R D g)).1
  apply
    (cancel_mono
      ((ρ_ (quotientRepresentativeMap W R D f)).hom ▷
        quotientRepresentativeMap W R D g)).1
  calc
    (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt).mapComp
        f (𝟙 Y)).hom ▷ quotientRepresentativeMap W R D g) ≫
      ((quotientRepresentativeMap W R D f ◁
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt).mapId
          Y).hom) ▷ quotientRepresentativeMap W R D g) ≫
      ((ρ_ (quotientRepresentativeMap W R D f)).hom ▷
        quotientRepresentativeMap W R D g) =
      𝟙 _ := hRightWhiskered
    _ =
    (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt).mapComp
        f (𝟙 Y)).hom ▷ quotientRepresentativeMap W R D g) ≫
      ((quotientRepresentativeMap W R D f ◁
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu).mapId
          Y).hom) ▷ quotientRepresentativeMap W R D g) ≫
      ((ρ_ (quotientRepresentativeMap W R D f)).hom ▷
        quotientRepresentativeMap W R D g) := hLeftNormal.symm

/-- Under local sandwich separation, the triangle residual lifts to equality of
the literal endpoint identity-gauge coordinate. -/
theorem associator_right_left_triangle_mapIdGauge_eq_of_sandwichSeparating
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (Qs Qt Qu : GeneratedQuotientGaugeParameters W R D)
    (hQs :
      Qs ∈ quotientRouteCorrectionLocus W R D
        (.associator f (𝟙 Y) g))
    (hQt :
      Qt ∈ quotientRouteCorrectionLocus W R D (.rightUnitor f))
    (hQu :
      Qu ∈ quotientRouteCorrectionLocus W R D (.leftUnitor g))
    (hRightComp :
      Qs.mapCompGauge f (𝟙 Y) = Qt.mapCompGauge f (𝟙 Y))
    (hLeftComp :
      Qs.mapCompGauge (𝟙 Y) g = Qu.mapCompGauge (𝟙 Y) g)
    (hSep : UnitIdentitySandwichSeparating W R D f g) :
    Qt.mapIdGauge Y = Qu.mapIdGauge Y := by
  have hSandwich :=
    associator_right_left_triangle_adjusted_mapId_sandwich_eq
      W R D f g Qs Qt Qu hQs hQt hQu hRightComp hLeftComp
  have hAdjustedIdHom :
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt).mapId Y).hom =
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu).mapId Y).hom :=
    hSep _ _ hSandwich
  have hGaugeHom :
      (Qt.mapIdGauge Y).hom = (Qu.mapIdGauge Y).hom := by
    apply (cancel_epi (generatedIdentityMapIso W R D Y).hom).1
    simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters,
      Iso.trans_hom] using hAdjustedIdHom
  apply Iso.ext
  exact hGaugeHom

/-- The actual associator anchor closes the right/left endpoint edge whenever
the one remaining unit-sandwich residual is locally separating. -/
theorem associatorAnchor_rightLeft_overlapStar_triangle_of_sandwichSeparating
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (Qs Qt Qu : GeneratedQuotientGaugeParameters W R D)
    (hQs :
      Qs ∈ quotientRouteCorrectionLocus W R D
        (.associator f (𝟙 Y) g))
    (hQt :
      Qt ∈ quotientRouteCorrectionLocus W R D (.rightUnitor f))
    (hQu :
      Qu ∈ quotientRouteCorrectionLocus W R D (.leftUnitor g))
    (hst :
      AgreeOnRouteFootprintOverlap W R D
        (.associator f (𝟙 Y) g) (.rightUnitor f) Qs Qt)
    (hsu :
      AgreeOnRouteFootprintOverlap W R D
        (.associator f (𝟙 Y) g) (.leftUnitor g) Qs Qu)
    (hSep : UnitIdentitySandwichSeparating W R D f g) :
    AgreeOnRouteFootprintOverlap W R D
      (.rightUnitor f) (.leftUnitor g) Qt Qu := by
  have hRightComp :
      Qs.mapCompGauge f (𝟙 Y) = Qt.mapCompGauge f (𝟙 Y) := by
    simpa [quotientGaugeCoordinateValue] using
      hst (.composition f (𝟙 Y))
        (by simp [RouteFootprintContains])
        (by simp [RouteFootprintContains])
  have hLeftComp :
      Qs.mapCompGauge (𝟙 Y) g = Qu.mapCompGauge (𝟙 Y) g := by
    simpa [quotientGaugeCoordinateValue] using
      hsu (.composition (𝟙 Y) g)
        (by simp [RouteFootprintContains])
        (by simp [RouteFootprintContains])
  have hId :=
    associator_right_left_triangle_mapIdGauge_eq_of_sandwichSeparating
      W R D f g Qs Qt Qu hQs hQt hQu hRightComp hLeftComp hSep
  exact
    rightUnitor_leftUnitor_agreeOnRouteFootprintOverlap_of_corrected_of_mapIdGauge_eq
      W R D f g Qt Qu hQt hQu hId

/-!
## Frontier after v3.26

The first genuine associator/unitor triangle does not collapse directly to the
unconditional v3.20 star-transitivity law.

What the concrete coherence equations force is:

  endpoint gId witnesses agree after F ◁ (-) ▷ G.

Thus the remaining obstruction is no longer an arbitrary correlation gap.  It
is a precise local kernel of the sandwich whiskering action on the identity
2-cell space.

If that local action separates the two identity witnesses, the actual
right/left endpoint overlap closes and v3.20 holds on this triangle.

The next truth-test should determine whether this sandwich-separation property
follows from existing KuuOS target structure in relevant cases, or whether a
concrete bicategory countermodel exhibits a nontrivial kernel.
-/

end KUOS.DependentOriginationAssociatorUnitorTriangleV3_26
