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

  have hAdjustedRHom := congrArg Iso.hom hAdjustedR
  have hAdjustedLHom := congrArg Iso.hom hAdjustedL

  let eA :
      quotientRepresentativeMap W R D ((f ≫ 𝟙 Y) ≫ g) ⟶
        quotientRepresentativeMap W R D (f ≫ (𝟙 Y ≫ g)) :=
    eqToHom (by simp)
  let eR :
      quotientRepresentativeMap W R D (f ≫ 𝟙 Y) ⟶ F :=
    eqToHom (by simp [F])
  let eL :
      quotientRepresentativeMap W R D (𝟙 Y ≫ g) ⟶ G :=
    eqToHom (by simp [G])

  change
    (S.mapComp (f ≫ 𝟙 Y) g).hom ≫
          (S.mapComp f (𝟙 Y)).hom ▷ G ≫
          (α_ F P G).hom ≫
          F ◁ (S.mapComp (𝟙 Y) g).inv ≫
          (S.mapComp f (𝟙 Y ≫ g)).inv =
        eA at hA
  change
    (T.mapComp f (𝟙 Y)).hom ≫
          F ◁ (T.mapId Y).hom ≫
          (ρ_ F).hom =
        eR at hR
  change
    (U.mapComp (𝟙 Y) g).hom ≫
          (U.mapId Y).hom ▷ G ≫
          (λ_ G).hom =
        eL at hL

  /- The two outer composition witnesses in the unit-degenerate associator
  are the same dependent mapComp coordinate after transporting along
  f≫𝟙=f and 𝟙≫g=g.  The resulting eqToHom square is pure transport
  bookkeeping; no coherence hypothesis on S is used here. -/
  have hOuterTransport :
      (S.mapComp (f ≫ 𝟙 Y) g).inv ≫
          eA ≫
          (S.mapComp f (𝟙 Y ≫ g)).hom ≫
          F ◁ eL =
        eR ▷ G := by
    dsimp [eA, eR, eL, F, G]
    simp only [Category.comp_id, Category.id_comp, eqToHom_refl,
      Iso.inv_hom_id_assoc]

  have hAssocBridge :
      (S.mapComp f (𝟙 Y)).hom ▷ G ≫ (α_ F P G).hom =
        (S.mapComp (f ≫ 𝟙 Y) g).inv ≫
          eA ≫
          (S.mapComp f (𝟙 Y ≫ g)).hom ≫
          F ◁ (S.mapComp (𝟙 Y) g).hom := by
    calc
      (S.mapComp f (𝟙 Y)).hom ▷ G ≫ (α_ F P G).hom =
          (S.mapComp (f ≫ 𝟙 Y) g).inv ≫
            ((S.mapComp (f ≫ 𝟙 Y) g).hom ≫
              (S.mapComp f (𝟙 Y)).hom ▷ G ≫
              (α_ F P G).hom ≫
              F ◁ (S.mapComp (𝟙 Y) g).inv ≫
              (S.mapComp f (𝟙 Y ≫ g)).inv) ≫
            (S.mapComp f (𝟙 Y ≫ g)).hom ≫
            F ◁ (S.mapComp (𝟙 Y) g).hom := by
              simp
      _ =
          (S.mapComp (f ≫ 𝟙 Y) g).inv ≫
            eA ≫
            (S.mapComp f (𝟙 Y ≫ g)).hom ≫
            F ◁ (S.mapComp (𝟙 Y) g).hom := by
              have h :=
                congrArg
                  (fun k =>
                    (S.mapComp (f ≫ 𝟙 Y) g).inv ≫
                      k ≫
                      (S.mapComp f (𝟙 Y ≫ g)).hom ≫
                      F ◁ (S.mapComp (𝟙 Y) g).hom)
                  hA
              simpa only [Category.assoc] using h

  have hRnormalized :
      (S.mapComp f (𝟙 Y)).hom ≫
          F ◁ (T.mapId Y).hom ≫
          (ρ_ F).hom =
        eR := by
    calc
      (S.mapComp f (𝟙 Y)).hom ≫
          F ◁ (T.mapId Y).hom ≫
          (ρ_ F).hom =
          (T.mapComp f (𝟙 Y)).hom ≫
            F ◁ (T.mapId Y).hom ≫
            (ρ_ F).hom := by
              rw [hAdjustedRHom]
      _ = eR := hR

  have hLnormalized :
      (S.mapComp (𝟙 Y) g).hom ≫
          (U.mapId Y).hom ▷ G ≫
          (λ_ G).hom =
        eL := by
    calc
      (S.mapComp (𝟙 Y) g).hom ≫
          (U.mapId Y).hom ▷ G ≫
          (λ_ G).hom =
          (U.mapComp (𝟙 Y) g).hom ≫
            (U.mapId Y).hom ▷ G ≫
            (λ_ G).hom := by
              rw [hAdjustedLHom]
      _ = eL := hL

  have hRwhisk :
      ((S.mapComp f (𝟙 Y)).hom ▷ G) ≫
          ((F ◁ (T.mapId Y).hom) ▷ G) ≫
          ((ρ_ F).hom ▷ G) =
        eR ▷ G := by
    have h := congrArg (fun η => η ▷ G) hRnormalized
    simpa only [comp_whiskerRight, Category.assoc] using h

  have hLwhisk :
      F ◁ (S.mapComp (𝟙 Y) g).hom ≫
          F ◁ ((U.mapId Y).hom ▷ G) ≫
          F ◁ (λ_ G).hom =
        F ◁ eL := by
    have h := congrArg (fun η => F ◁ η) hLnormalized
    simpa only [whiskerLeft_comp, Category.assoc] using h

  have hTriangle :
      (ρ_ F).hom ▷ G =
        (α_ F (𝟙 _) G).hom ≫ F ◁ (λ_ G).hom :=
    (triangle_assoc_comp_left F G).symm

  have hNaturality :
      ((F ◁ (T.mapId Y).hom) ▷ G) ≫
          (α_ F (𝟙 _) G).hom =
        (α_ F P G).hom ≫
          F ◁ ((T.mapId Y).hom ▷ G) := by
    simpa only [P] using
      associator_naturality_middle F (T.mapId Y).hom G

  have hStructural :
      ((F ◁ (T.mapId Y).hom) ▷ G) ≫ ((ρ_ F).hom ▷ G) =
        (α_ F P G).hom ≫
          F ◁ ((T.mapId Y).hom ▷ G) ≫
          F ◁ (λ_ G).hom := by
    calc
      ((F ◁ (T.mapId Y).hom) ▷ G) ≫ ((ρ_ F).hom ▷ G) =
          ((F ◁ (T.mapId Y).hom) ▷ G) ≫
            ((α_ F (𝟙 _) G).hom ≫ F ◁ (λ_ G).hom) := by
              rw [hTriangle]
      _ =
          (((F ◁ (T.mapId Y).hom) ▷ G) ≫
            (α_ F (𝟙 _) G).hom) ≫
            F ◁ (λ_ G).hom := by
              simp only [Category.assoc]
      _ =
          ((α_ F P G).hom ≫
            F ◁ ((T.mapId Y).hom ▷ G)) ≫
            F ◁ (λ_ G).hom := by
              exact congrArg
                (fun k => k ≫ F ◁ (λ_ G).hom)
                hNaturality
      _ =
          (α_ F P G).hom ≫
            F ◁ ((T.mapId Y).hom ▷ G) ≫
            F ◁ (λ_ G).hom := by
              simp only [Category.assoc]

  have hRightNormalized :
      (S.mapComp f (𝟙 Y)).hom ▷ G ≫
          (α_ F P G).hom ≫
          F ◁ ((T.mapId Y).hom ▷ G) ≫
          F ◁ (λ_ G).hom =
        eR ▷ G := by
    have h :=
      congrArg
        (fun k => ((S.mapComp f (𝟙 Y)).hom ▷ G) ≫ k)
        hStructural.symm
    calc
      (S.mapComp f (𝟙 Y)).hom ▷ G ≫
          (α_ F P G).hom ≫
          F ◁ ((T.mapId Y).hom ▷ G) ≫
          F ◁ (λ_ G).hom =
          (S.mapComp f (𝟙 Y)).hom ▷ G ≫
            ((F ◁ (T.mapId Y).hom) ▷ G) ≫
            ((ρ_ F).hom ▷ G) := by
              simpa only [Category.assoc] using h
      _ = eR ▷ G := hRwhisk

  have hRightViaAssociator :
      (S.mapComp (f ≫ 𝟙 Y) g).inv ≫
          eA ≫
          (S.mapComp f (𝟙 Y ≫ g)).hom ≫
          F ◁ (S.mapComp (𝟙 Y) g).hom ≫
          F ◁ ((T.mapId Y).hom ▷ G) ≫
          F ◁ (λ_ G).hom =
        eR ▷ G := by
    have hBridgeExtended :=
      congrArg
        (fun k =>
          k ≫ F ◁ ((T.mapId Y).hom ▷ G) ≫
            F ◁ (λ_ G).hom)
        hAssocBridge
    calc
      (S.mapComp (f ≫ 𝟙 Y) g).inv ≫
          eA ≫
          (S.mapComp f (𝟙 Y ≫ g)).hom ≫
          F ◁ (S.mapComp (𝟙 Y) g).hom ≫
          F ◁ ((T.mapId Y).hom ▷ G) ≫
          F ◁ (λ_ G).hom =
          ((S.mapComp f (𝟙 Y)).hom ▷ G ≫
            (α_ F P G).hom) ≫
            F ◁ ((T.mapId Y).hom ▷ G) ≫
            F ◁ (λ_ G).hom := by
              simpa only [Category.assoc] using hBridgeExtended.symm
      _ = eR ▷ G := by
            simpa only [Category.assoc] using hRightNormalized

  have hLeftViaTransport :
      (S.mapComp (f ≫ 𝟙 Y) g).inv ≫
          eA ≫
          (S.mapComp f (𝟙 Y ≫ g)).hom ≫
          F ◁ (S.mapComp (𝟙 Y) g).hom ≫
          F ◁ ((U.mapId Y).hom ▷ G) ≫
          F ◁ (λ_ G).hom =
        eR ▷ G := by
    let pre :=
      (S.mapComp (f ≫ 𝟙 Y) g).inv ≫
        eA ≫
        (S.mapComp f (𝟙 Y ≫ g)).hom
    have hLeftExtended :=
      congrArg (fun k => pre ≫ k) hLwhisk
    calc
      (S.mapComp (f ≫ 𝟙 Y) g).inv ≫
          eA ≫
          (S.mapComp f (𝟙 Y ≫ g)).hom ≫
          F ◁ (S.mapComp (𝟙 Y) g).hom ≫
          F ◁ ((U.mapId Y).hom ▷ G) ≫
          F ◁ (λ_ G).hom =
          pre ≫ (F ◁ eL) := by
              simpa only [pre, Category.assoc] using hLeftExtended
      _ = eR ▷ G := by
            simpa only [pre, Category.assoc] using hOuterTransport

  have hBoth := hRightViaAssociator.trans hLeftViaTransport.symm

  apply
    (cancel_epi
      ((S.mapComp (f ≫ 𝟙 Y) g).inv ≫
        eA ≫
        (S.mapComp f (𝟙 Y ≫ g)).hom ≫
        F ◁ (S.mapComp (𝟙 Y) g).hom)).1
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
