import KUOS.DependentOriginationUnitorPartialRigidityV3_22

namespace KUOS.DependentOriginationAssociatorThreeOfFourRigidityV3_23

open CategoryTheory
open CategoryTheory.Bicategory
open Set
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherenceDefectsV2_65
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationFiveGeneratedCorrectionCoboundaryV3_00
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationQuotientDefectOrbitV3_06
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateFootprintV3_12
open KUOS.DependentOriginationUnitorPartialRigidityV3_22

universe u v uH vH

/-!
# Actual associator three-of-four rigidity v3.23

v3.22 proves an actual graph property for each unitor correction locus:
fixing the identity-gauge coordinate determines the corresponding composition
coordinate.

For an associator route at composable f, g, h, the corrected equation contains
four composition-gauge coordinates:

* gComp(f ≫ g, h);
* gComp(f, g);
* gComp(g, h);
* gComp(f, g ≫ h).

All other factors are fixed isomorphisms.  Therefore, for two gauges correcting
the same associator route, equality of any chosen three coordinates should
determine the fourth after cancellation.

This file proves one canonical orientation of that fact: if the latter three
coordinates agree, then gComp(f ≫ g, h) agrees as well.  Consequently the two
gauges agree on the entire associator footprint.

This is the associator analogue of v3.22 partial rigidity and is derived from
the concrete v2.65 associator equation, not from an abstract gluing axiom.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Inside one corrected associator locus, the first composition coordinate is
forced by equality of the other three footprint coordinates. -/
theorem associator_mapComp_fgg_h_eq_of_corrected_of_other_three_eq
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    (hQ :
      Q ∈ quotientRouteCorrectionLocus W R D (.associator f g h))
    (hQ' :
      Q' ∈ quotientRouteCorrectionLocus W R D (.associator f g h))
    (hfg : Q.mapCompGauge f g = Q'.mapCompGauge f g)
    (hgh : Q.mapCompGauge g h = Q'.mapCompGauge g h)
    (hfgh : Q.mapCompGauge f (g ≫ h) = Q'.mapCompGauge f (g ≫ h)) :
    Q.mapCompGauge (f ≫ g) h = Q'.mapCompGauge (f ≫ g) h := by
  change
    quotientAssociatorDefect W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q)
      f g h = Iso.refl _ at hQ
  change
    quotientAssociatorDefect W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q')
      f g h = Iso.refl _ at hQ'
  have hEqQ :=
    (quotientAssociatorDefect_eq_refl_iff W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q)
      f g h).1 hQ
  have hEqQ' :=
    (quotientAssociatorDefect_eq_refl_iff W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q')
      f g h).1 hQ'
  have hAdjustedFG :
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp f g =
        (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp f g := by
    simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg
        (fun q => generatedCompositionMapIso W R D f g ≪≫ q)
        hfg
  have hAdjustedGH :
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp g h =
        (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp g h := by
    simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg
        (fun q => generatedCompositionMapIso W R D g h ≪≫ q)
        hgh
  have hAdjustedFGH :
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp f (g ≫ h) =
        (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp f (g ≫ h) := by
    simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg
        (fun q => generatedCompositionMapIso W R D f (g ≫ h) ≪≫ q)
        hfgh
  have hAdjustedFGHom := congrArg Iso.hom hAdjustedFG
  have hAdjustedGHInv := congrArg Iso.inv hAdjustedGH
  have hAdjustedFGHInv := congrArg Iso.inv hAdjustedFGH
  have hComposite :
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
          (f ≫ g) h).hom ≫
          (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
            f g).hom ▷ quotientRepresentativeMap W R D h) ≫
          (α_
            (quotientRepresentativeMap W R D f)
            (quotientRepresentativeMap W R D g)
            (quotientRepresentativeMap W R D h)).hom ≫
          (quotientRepresentativeMap W R D f ◁
            ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
              g h).inv) ≫
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
            f (g ≫ h)).inv =
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
          (f ≫ g) h).hom ≫
          (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
            f g).hom ▷ quotientRepresentativeMap W R D h) ≫
          (α_
            (quotientRepresentativeMap W R D f)
            (quotientRepresentativeMap W R D g)
            (quotientRepresentativeMap W R D h)).hom ≫
          (quotientRepresentativeMap W R D f ◁
            ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
              g h).inv) ≫
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
            f (g ≫ h)).inv := by
    calc
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
          (f ≫ g) h).hom ≫
          (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
            f g).hom ▷ quotientRepresentativeMap W R D h) ≫
          (α_
            (quotientRepresentativeMap W R D f)
            (quotientRepresentativeMap W R D g)
            (quotientRepresentativeMap W R D h)).hom ≫
          (quotientRepresentativeMap W R D f ◁
            ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
              g h).inv) ≫
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
            f (g ≫ h)).inv =
          eqToHom (by simp) := hEqQ
      _ =
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
            (f ≫ g) h).hom ≫
            (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
              f g).hom ▷ quotientRepresentativeMap W R D h) ≫
            (α_
              (quotientRepresentativeMap W R D f)
              (quotientRepresentativeMap W R D g)
              (quotientRepresentativeMap W R D h)).hom ≫
            (quotientRepresentativeMap W R D f ◁
              ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
                g h).inv) ≫
            ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
              f (g ≫ h)).inv := hEqQ'.symm
      _ =
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
            (f ≫ g) h).hom ≫
            (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
              f g).hom ▷ quotientRepresentativeMap W R D h) ≫
            (α_
              (quotientRepresentativeMap W R D f)
              (quotientRepresentativeMap W R D g)
              (quotientRepresentativeMap W R D h)).hom ≫
            (quotientRepresentativeMap W R D f ◁
              ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
                g h).inv) ≫
            ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
              f (g ≫ h)).inv := by
              rw [hAdjustedFGHom, hAdjustedGHInv, hAdjustedFGHInv]
  have hAdjustedFirstHom :
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
        (f ≫ g) h).hom =
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
          (f ≫ g) h).hom := by
    apply
      (cancel_mono
        ((((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
            f g).hom ▷ quotientRepresentativeMap W R D h) ≫
          (α_
            (quotientRepresentativeMap W R D f)
            (quotientRepresentativeMap W R D g)
            (quotientRepresentativeMap W R D h)).hom ≫
          (quotientRepresentativeMap W R D f ◁
            ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
              g h).inv) ≫
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
            f (g ≫ h)).inv)).1
    simpa only [Category.assoc] using hComposite
  have hGaugeHom :
      (Q.mapCompGauge (f ≫ g) h).hom =
        (Q'.mapCompGauge (f ≫ g) h).hom := by
    apply
      (cancel_epi
        (generatedCompositionMapIso W R D (f ≫ g) h).hom).1
    simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters,
      Iso.trans_hom] using hAdjustedFirstHom
  apply Iso.ext
  exact hGaugeHom

/-- Equality of three associator footprint coordinates between two correcting
gauges forces agreement on the complete associator footprint. -/
theorem associator_agreesOnRouteState_of_corrected_of_other_three_eq
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    (hQ :
      Q ∈ quotientRouteCorrectionLocus W R D (.associator f g h))
    (hQ' :
      Q' ∈ quotientRouteCorrectionLocus W R D (.associator f g h))
    (hfg : Q.mapCompGauge f g = Q'.mapCompGauge f g)
    (hgh : Q.mapCompGauge g h = Q'.mapCompGauge g h)
    (hfgh : Q.mapCompGauge f (g ≫ h) = Q'.mapCompGauge f (g ≫ h)) :
    QuotientGaugesAgreeOnRouteState W R D Q Q' (.associator f g h) := by
  refine ⟨?_, hfg, hgh, hfgh⟩
  exact
    associator_mapComp_fgg_h_eq_of_corrected_of_other_three_eq
      W R D f g h Q Q' hQ hQ' hfg hgh hfgh

/-!
## Factorization frontier after v3.23

The actual quotient correction loci now have two concrete graph-like
properties.

Unitor routes (v3.22):
  fixed gId
      =>
  fixed corresponding gComp.

Associator routes (v3.23):
  fixed three of the four displayed gComp coordinates
      =>
  fixed remaining displayed gComp coordinate.

Thus the route loci carry substantially more structure than the abstract
cylinders used in v3.17/v3.21.  The next task is to combine these graph
constraints along the actual overlap pattern and test whether they imply the
v3.20 overlap-star-transitivity condition, first on unit-generated triangles
and then on mixed associator/unitor triangles.
-/

end KUOS.DependentOriginationAssociatorThreeOfFourRigidityV3_23
