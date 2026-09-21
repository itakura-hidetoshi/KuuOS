import KUOS.DependentOriginationMixedUnitorRigidityV3_25

namespace KUOS.DependentOriginationAssociatorUnitorTriangleResidualV3_26

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
open KUOS.DependentOriginationAssociatorThreeOfFourRigidityV3_23
open KUOS.DependentOriginationMixedUnitorRigidityV3_25

universe u v uH vH

/-!
# Associator-unitor triangle residual v3.26

The first genuinely mixed incidence triangle is

* associator f (𝟙 Y) g;
* right unitor f;
* left unitor g.

The associator anchor overlaps the two unitor endpoints in the two composition
coordinates gComp(f,𝟙 Y) and gComp(𝟙 Y,g).  The endpoints themselves share only
the identity coordinate gId(Y).

The actual three corrected equations, together with the bicategory triangle
identity, force the two endpoint identity corrections to agree after double
whiskering by the representative 1-cells of f and g.  This is the exact
residual left after v3.23-v3.25: no new abstract gluing axiom is inserted.

If that double-whiskering map is injective on the relevant 2-cell hom-set, the
residual vanishes and the actual overlap-star triangle closes.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Concrete local separation condition for the middle identity correction.
It asks only that double whiskering by the two representative 1-cells separate
2-cells from the representative of 𝟙 Y to the bicategorical identity. -/
def MiddleIdentityWhiskerSeparating
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) : Prop :=
  Function.Injective
    (fun η :
        quotientRepresentativeMap W R D (𝟙 Y) ⟶
          𝟙 (R.obj (.mk Y.as.obj)) =>
      quotientRepresentativeMap W R D f ◁
        (η ▷ quotientRepresentativeMap W R D g))

/-- The three actual correction equations around the associator/right-unitor/
left-unitor triangle force equality of the two endpoint identity maps after
double whiskering. -/
theorem associator_unitor_triangle_doubleWhisker_mapId_eq
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
    (hst : AgreeOnRouteFootprintOverlap W R D
      (.associator f (𝟙 Y) g) (.rightUnitor f) Qs Qt)
    (hsu : AgreeOnRouteFootprintOverlap W R D
      (.associator f (𝟙 Y) g) (.leftUnitor g) Qs Qu) :
    quotientRepresentativeMap W R D f ◁
        (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt).mapId Y).hom ▷
          quotientRepresentativeMap W R D g) =
      quotientRepresentativeMap W R D f ◁
        (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu).mapId Y).hom ▷
          quotientRepresentativeMap W R D g) := by
  let F := quotientRepresentativeMap W R D f
  let P := quotientRepresentativeMap W R D (𝟙 Y)
  let G := quotientRepresentativeMap W R D g
  let S := quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qs
  let T := quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt
  let U := quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu

  have hstComp :
      Qs.mapCompGauge f (𝟙 Y) = Qt.mapCompGauge f (𝟙 Y) := by
    simpa [quotientGaugeCoordinateValue] using
      hst (.composition f (𝟙 Y))
        (by simp [RouteFootprintContains])
        (by simp [RouteFootprintContains])
  have hsuComp :
      Qs.mapCompGauge (𝟙 Y) g = Qu.mapCompGauge (𝟙 Y) g := by
    simpa [quotientGaugeCoordinateValue] using
      hsu (.composition (𝟙 Y) g)
        (by simp [RouteFootprintContains])
        (by simp [RouteFootprintContains])

  have hAdjustedR : S.mapComp f (𝟙 Y) = T.mapComp f (𝟙 Y) := by
    simpa [S, T, quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg
        (fun q => generatedCompositionMapIso W R D f (𝟙 Y) ≪≫ q)
        hstComp
  have hAdjustedL : S.mapComp (𝟙 Y) g = U.mapComp (𝟙 Y) g := by
    simpa [S, U, quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg
        (fun q => generatedCompositionMapIso W R D (𝟙 Y) g ≪≫ q)
        hsuComp

  change
    quotientAssociatorDefect W R D S f (𝟙 Y) g = Iso.refl _ at hQs
  change
    quotientRightUnitorDefect W R D T f = Iso.refl _ at hQt
  change
    quotientLeftUnitorDefect W R D U g = Iso.refl _ at hQu
  have hA :=
    (quotientAssociatorDefect_eq_refl_iff W R D S f (𝟙 Y) g).1 hQs
  have hR :=
    (quotientRightUnitorDefect_eq_refl_iff W R D T f).1 hQt
  have hL :=
    (quotientLeftUnitorDefect_eq_refl_iff W R D U g).1 hQu

  have hMiddle :
      (S.mapComp f (𝟙 Y)).hom ▷ G ≫
          (α_ F P G).hom ≫
          F ◁ (S.mapComp (𝟙 Y) g).inv =
        𝟙 (F ≫ G) := by
    apply (cancel_epi (S.mapComp f g).hom).1
    apply (cancel_mono (S.mapComp f g).inv).1
    simpa [F, P, G, S, Category.assoc] using hA

  have hAssocBridge :
      (S.mapComp f (𝟙 Y)).hom ▷ G ≫ (α_ F P G).hom =
        F ◁ (S.mapComp (𝟙 Y) g).hom := by
    apply (cancel_mono (F ◁ (S.mapComp (𝟙 Y) g).inv)).1
    simpa [Category.assoc] using hMiddle

  have hR' :
      (S.mapComp f (𝟙 Y)).hom ≫
          F ◁ (T.mapId Y).hom ≫
          (ρ_ F).hom =
        𝟙 F := by
    simpa [F, S, T, Category.assoc,
      congrArg Iso.hom hAdjustedR] using hR

  have hL' :
      (S.mapComp (𝟙 Y) g).hom ≫
          (U.mapId Y).hom ▷ G ≫
          (λ_ G).hom =
        𝟙 G := by
    simpa [G, S, U, Category.assoc,
      congrArg Iso.hom hAdjustedL] using hL

  have hRwhisk :
      ((S.mapComp f (𝟙 Y)).hom ▷ G) ≫
          ((F ◁ (T.mapId Y).hom) ▷ G) ≫
          ((ρ_ F).hom ▷ G) =
        𝟙 (F ≫ G) := by
    have h := congrArg (fun η => η ▷ G) hR'
    simpa [comp_whiskerRight, Category.assoc] using h

  have hLwhisk :
      F ◁ (S.mapComp (𝟙 Y) g).hom ≫
          F ◁ ((U.mapId Y).hom ▷ G) ≫
          F ◁ (λ_ G).hom =
        𝟙 (F ≫ G) := by
    have h := congrArg (fun η => F ◁ η) hL'
    simpa [whiskerLeft_comp, Category.assoc] using h

  have hStructural :
      ((F ◁ (T.mapId Y).hom) ▷ G) ≫ ((ρ_ F).hom ▷ G) =
        (α_ F P G).hom ≫
          F ◁ ((T.mapId Y).hom ▷ G) ≫
          F ◁ (λ_ G).hom := by
    rw [← triangle F G]
    rw [Category.assoc,
      associator_naturality_middle F (T.mapId Y).hom G]
    simp only [Category.assoc, whiskerLeft_comp]

  have hRnormalized :
      F ◁ (S.mapComp (𝟙 Y) g).hom ≫
          F ◁ ((T.mapId Y).hom ▷ G) ≫
          F ◁ (λ_ G).hom =
        𝟙 (F ≫ G) := by
    calc
      F ◁ (S.mapComp (𝟙 Y) g).hom ≫
          F ◁ ((T.mapId Y).hom ▷ G) ≫
          F ◁ (λ_ G).hom =
          ((S.mapComp f (𝟙 Y)).hom ▷ G) ≫
            (α_ F P G).hom ≫
            F ◁ ((T.mapId Y).hom ▷ G) ≫
            F ◁ (λ_ G).hom := by
              rw [hAssocBridge]
      _ =
          ((S.mapComp f (𝟙 Y)).hom ▷ G) ≫
            ((F ◁ (T.mapId Y).hom) ▷ G) ≫
            ((ρ_ F).hom ▷ G) := by
              rw [hStructural]
      _ = 𝟙 (F ≫ G) := hRwhisk

  have hBoth :
      F ◁ (S.mapComp (𝟙 Y) g).hom ≫
          F ◁ ((T.mapId Y).hom ▷ G) ≫
          F ◁ (λ_ G).hom =
        F ◁ (S.mapComp (𝟙 Y) g).hom ≫
          F ◁ ((U.mapId Y).hom ▷ G) ≫
          F ◁ (λ_ G).hom :=
    hRnormalized.trans hLwhisk.symm

  apply (cancel_epi (F ◁ (S.mapComp (𝟙 Y) g).hom)).1
  apply (cancel_mono (F ◁ (λ_ G).hom)).1
  simpa only [Category.assoc] using hBoth

/-- Under the exact local separation condition exposed above, the mixed
associator/unitor star triangle closes on the actual endpoint overlap. -/
theorem associatorAnchor_unitor_overlapStar_triangle_of_separating
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
    (hst : AgreeOnRouteFootprintOverlap W R D
      (.associator f (𝟙 Y) g) (.rightUnitor f) Qs Qt)
    (hsu : AgreeOnRouteFootprintOverlap W R D
      (.associator f (𝟙 Y) g) (.leftUnitor g) Qs Qu)
    (hsep : MiddleIdentityWhiskerSeparating W R D f g) :
    AgreeOnRouteFootprintOverlap W R D
      (.rightUnitor f) (.leftUnitor g) Qt Qu := by
  have hDouble :=
    associator_unitor_triangle_doubleWhisker_mapId_eq
      W R D f g Qs Qt Qu hQs hQt hQu hst hsu
  have hAdjustedIdHom :
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt).mapId Y).hom =
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu).mapId Y).hom := by
    exact hsep hDouble
  have hAdjustedId :
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qt).mapId Y =
        (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Qu).mapId Y := by
    apply Iso.ext
    exact hAdjustedIdHom
  have hGaugeIdHom :
      (Qt.mapIdGauge Y).hom = (Qu.mapIdGauge Y).hom := by
    apply (cancel_epi (generatedIdentityMapIso W R D Y).hom).1
    simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters,
      Iso.trans_hom] using congrArg Iso.hom hAdjustedId
  have hGaugeId : Qt.mapIdGauge Y = Qu.mapIdGauge Y := by
    apply Iso.ext
    exact hGaugeIdHom
  exact
    rightUnitor_leftUnitor_agreeOnRouteFootprintOverlap_of_corrected_of_mapIdGauge_eq
      W R D f g Qt Qu hQt hQu hGaugeId

/-!
## Frontier after v3.26

The associator/unitor triangle does not, in a completely arbitrary bicategory,
force literal equality of the middle identity correction merely from the three
coherence equations.  What the equations force without extra assumptions is
the double-whiskered equality proved above.

Thus the remaining obstruction is now localized precisely in the kernel of

  η ↦ F ◁ (η ▷ G).

When this local action separates 2-cells, the v3.20 star edge closes.  The next
truth-test is therefore whether the generated localization bicategory supplies
this separation on the relevant representative 1-cells, or whether a concrete
countermodel can retain a nontrivial kernel.
-/

end KUOS.DependentOriginationAssociatorUnitorTriangleResidualV3_26
