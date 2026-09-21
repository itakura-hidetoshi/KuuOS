import KUOS.DependentOriginationCylinderLocalityCountermodelV3_21

namespace KUOS.DependentOriginationAssociatorLeadingRigidityV3_23

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

universe u v uH vH

/-!
# Actual associator leading-coordinate rigidity v3.23

The concrete corrected associator equation at a composable triple f,g,h uses
four quotient composition-gauge coordinates:

* gComp(f ≫ g, h);
* gComp(f, g);
* gComp(g, h);
* gComp(f, g ≫ h).

All intervening structural factors are invertible.  Therefore, inside one
associator correction locus, fixing the latter three coordinates forces the
leading coordinate gComp(f ≫ g, h).

This file proves that statement directly from the v2.65 associator defect
equation by cancellation.  Thus an associator correction locus is graph-like
over three of its four footprint coordinates.

No global correlation or star-transitivity claim is made here.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- For a fixed corrected associator route, equality of the three trailing
composition-gauge coordinates forces equality of the leading coordinate. -/
theorem associator_leading_mapCompGauge_eq_of_corrected_of_trailing_eq
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
    (hfgh :
      Q.mapCompGauge f (g ≫ h) =
        Q'.mapCompGauge f (g ≫ h)) :
    Q.mapCompGauge (f ≫ g) h =
      Q'.mapCompGauge (f ≫ g) h := by
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
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
          f (g ≫ h) =
        (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
          f (g ≫ h) := by
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
  have hAdjustedLeadingHom :
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
      Iso.trans_hom] using hAdjustedLeadingHom
  apply Iso.ext
  exact hGaugeHom

/-- Two correcting gauges which agree on the three trailing coordinates agree
on the entire associator footprint. -/
theorem associator_agreesOnRouteState_of_corrected_of_trailing_eq
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
    (hfgh :
      Q.mapCompGauge f (g ≫ h) =
        Q'.mapCompGauge f (g ≫ h)) :
    QuotientGaugesAgreeOnRouteState W R D Q Q' (.associator f g h) := by
  refine ⟨?_, hfg, hgh, hfgh⟩
  exact
    associator_leading_mapCompGauge_eq_of_corrected_of_trailing_eq
      W R D f g h Q Q' hQ hQ' hfg hgh hfgh

/-!
## Factorization frontier after v3.23

The concrete route equations now exhibit graph structure in both route types:

* unitor loci: gId fixes the corresponding unitor gComp coordinate;
* associator loci: three trailing gComp coordinates fix the leading gComp
  coordinate.

Thus the actual correction loci are substantially more structured than the
arbitrary Boolean cylinders used by the v3.17/v3.21 countermodels.

The next task is to combine these local graph laws across literal footprint
overlaps and test whether they imply the v3.20 triangle-closing property for
specific families of route-state triangles.  Associator/unitor triangles are
the first nontrivial case.
-/

end KUOS.DependentOriginationAssociatorLeadingRigidityV3_23
