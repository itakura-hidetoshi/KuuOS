import KUOS.DependentOriginationCylinderLocalityCountermodelV3_21

namespace KUOS.DependentOriginationUnitorPartialRigidityV3_22

open CategoryTheory
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

universe u v uH vH

/-!
# Actual unitor partial rigidity v3.22

v3.21 shows that footprint locality alone cannot close the witness-correlation
gap.  We therefore return to the concrete quotient coherence equations.

For a left-unitor route at f : X ⟶ Y, the corrected equation contains exactly
two variable quotient-gauge coordinates:

* gComp(𝟙 X, f);
* gId(X).

All remaining factors are fixed isomorphisms.  Hence, inside the left-unitor
correction locus, once gId(X) is fixed, cancellation forces gComp(𝟙 X, f) to be
unique.

The same argument applies to a right-unitor route: fixing gId(Y) forces
gComp(f, 𝟙 Y).

This is an actual route-equation theorem, not an abstract gluing hypothesis.
It provides the first concrete partial rigidity needed for the post-v3.21
correlation problem.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- For a fixed corrected left-unitor route, equality of the identity-gauge
coordinate forces equality of the composition-gauge coordinate. -/
theorem leftUnitor_mapCompGauge_eq_of_corrected_of_mapIdGauge_eq
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : W.Localization}
    (f : X ⟶ Y)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    (hQ :
      Q ∈ quotientRouteCorrectionLocus W R D (.leftUnitor f))
    (hQ' :
      Q' ∈ quotientRouteCorrectionLocus W R D (.leftUnitor f))
    (hId : Q.mapIdGauge X = Q'.mapIdGauge X) :
    Q.mapCompGauge (𝟙 X) f = Q'.mapCompGauge (𝟙 X) f := by
  change
    quotientLeftUnitorDefect W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q) f =
        Iso.refl _ at hQ
  change
    quotientLeftUnitorDefect W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q') f =
        Iso.refl _ at hQ'
  have hEqQ :=
    (quotientLeftUnitorDefect_eq_refl_iff W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q) f).1 hQ
  have hEqQ' :=
    (quotientLeftUnitorDefect_eq_refl_iff W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q') f).1 hQ'
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
  have hComposite :
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
          (𝟙 X) f).hom ≫
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId X).hom ▷
            quotientRepresentativeMap W R D f ≫
          (λ_ (quotientRepresentativeMap W R D f)).hom =
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
          (𝟙 X) f).hom ≫
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId X).hom ▷
            quotientRepresentativeMap W R D f ≫
          (λ_ (quotientRepresentativeMap W R D f)).hom := by
    calc
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
          (𝟙 X) f).hom ≫
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId X).hom ▷
            quotientRepresentativeMap W R D f ≫
          (λ_ (quotientRepresentativeMap W R D f)).hom =
          eqToHom (by simp) := hEqQ
      _ =
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
            (𝟙 X) f).hom ≫
            ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapId X).hom ▷
              quotientRepresentativeMap W R D f ≫
            (λ_ (quotientRepresentativeMap W R D f)).hom := hEqQ'.symm
      _ =
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
            (𝟙 X) f).hom ≫
            ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId X).hom ▷
              quotientRepresentativeMap W R D f ≫
            (λ_ (quotientRepresentativeMap W R D f)).hom := by
            rw [hAdjustedIdHom]
  have hAdjustedCompHom :
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
        (𝟙 X) f).hom =
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
          (𝟙 X) f).hom := by
    apply
      (cancel_mono
        (((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId X).hom ▷
            quotientRepresentativeMap W R D f ≫
          (λ_ (quotientRepresentativeMap W R D f)).hom)).1
    simpa only [Category.assoc] using hComposite
  have hGaugeHom :
      (Q.mapCompGauge (𝟙 X) f).hom =
        (Q'.mapCompGauge (𝟙 X) f).hom := by
    apply
      (cancel_epi
        (generatedCompositionMapIso W R D (𝟙 X) f).hom).1
    simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters,
      Iso.trans_hom] using hAdjustedCompHom
  apply Iso.ext
  exact hGaugeHom

/-- Thus two correcting gauges with the same left-unitor identity coordinate
agree on the entire left-unitor footprint. -/
theorem leftUnitor_agreesOnRouteState_of_corrected_of_mapIdGauge_eq
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : W.Localization}
    (f : X ⟶ Y)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    (hQ :
      Q ∈ quotientRouteCorrectionLocus W R D (.leftUnitor f))
    (hQ' :
      Q' ∈ quotientRouteCorrectionLocus W R D (.leftUnitor f))
    (hId : Q.mapIdGauge X = Q'.mapIdGauge X) :
    QuotientGaugesAgreeOnRouteState W R D Q Q' (.leftUnitor f) := by
  constructor
  · exact
      leftUnitor_mapCompGauge_eq_of_corrected_of_mapIdGauge_eq
        W R D f Q Q' hQ hQ' hId
  · exact hId

/-- For a fixed corrected right-unitor route, equality of the identity-gauge
coordinate forces equality of the composition-gauge coordinate. -/
theorem rightUnitor_mapCompGauge_eq_of_corrected_of_mapIdGauge_eq
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : W.Localization}
    (f : X ⟶ Y)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    (hQ :
      Q ∈ quotientRouteCorrectionLocus W R D (.rightUnitor f))
    (hQ' :
      Q' ∈ quotientRouteCorrectionLocus W R D (.rightUnitor f))
    (hId : Q.mapIdGauge Y = Q'.mapIdGauge Y) :
    Q.mapCompGauge f (𝟙 Y) = Q'.mapCompGauge f (𝟙 Y) := by
  change
    quotientRightUnitorDefect W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q) f =
        Iso.refl _ at hQ
  change
    quotientRightUnitorDefect W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q') f =
        Iso.refl _ at hQ'
  have hEqQ :=
    (quotientRightUnitorDefect_eq_refl_iff W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q) f).1 hQ
  have hEqQ' :=
    (quotientRightUnitorDefect_eq_refl_iff W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q') f).1 hQ'
  have hAdjustedId :
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId Y =
        (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapId Y := by
    simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg
        (fun q => generatedIdentityMapIso W R D Y ≪≫ q)
        hId
  have hAdjustedIdHom := congrArg Iso.hom hAdjustedId
  have hComposite :
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
          f (𝟙 Y)).hom ≫
          quotientRepresentativeMap W R D f ◁
            ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId Y).hom ≫
          (ρ_ (quotientRepresentativeMap W R D f)).hom =
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
          f (𝟙 Y)).hom ≫
          quotientRepresentativeMap W R D f ◁
            ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId Y).hom ≫
          (ρ_ (quotientRepresentativeMap W R D f)).hom := by
    calc
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
          f (𝟙 Y)).hom ≫
          quotientRepresentativeMap W R D f ◁
            ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId Y).hom ≫
          (ρ_ (quotientRepresentativeMap W R D f)).hom =
          eqToHom (by simp) := hEqQ
      _ =
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
            f (𝟙 Y)).hom ≫
            quotientRepresentativeMap W R D f ◁
              ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapId Y).hom ≫
            (ρ_ (quotientRepresentativeMap W R D f)).hom := hEqQ'.symm
      _ =
          ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
            f (𝟙 Y)).hom ≫
            quotientRepresentativeMap W R D f ◁
              ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId Y).hom ≫
            (ρ_ (quotientRepresentativeMap W R D f)).hom := by
            rw [hAdjustedIdHom]
  have hAdjustedCompHom :
      ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp
        f (𝟙 Y)).hom =
        ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp
          f (𝟙 Y)).hom := by
    apply
      (cancel_mono
        (quotientRepresentativeMap W R D f ◁
            ((quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId Y).hom ≫
          (ρ_ (quotientRepresentativeMap W R D f)).hom)).1
    simpa only [Category.assoc] using hComposite
  have hGaugeHom :
      (Q.mapCompGauge f (𝟙 Y)).hom =
        (Q'.mapCompGauge f (𝟙 Y)).hom := by
    apply
      (cancel_epi
        (generatedCompositionMapIso W R D f (𝟙 Y)).hom).1
    simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters,
      Iso.trans_hom] using hAdjustedCompHom
  apply Iso.ext
  exact hGaugeHom

/-- Thus two correcting gauges with the same right-unitor identity coordinate
agree on the entire right-unitor footprint. -/
theorem rightUnitor_agreesOnRouteState_of_corrected_of_mapIdGauge_eq
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : W.Localization}
    (f : X ⟶ Y)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    (hQ :
      Q ∈ quotientRouteCorrectionLocus W R D (.rightUnitor f))
    (hQ' :
      Q' ∈ quotientRouteCorrectionLocus W R D (.rightUnitor f))
    (hId : Q.mapIdGauge Y = Q'.mapIdGauge Y) :
    QuotientGaugesAgreeOnRouteState W R D Q Q' (.rightUnitor f) := by
  constructor
  · exact
      rightUnitor_mapCompGauge_eq_of_corrected_of_mapIdGauge_eq
        W R D f Q Q' hQ hQ' hId
  · exact hId

/-!
## Factorization frontier after v3.22

The post-v3.21 analysis has now entered the actual quotient equations.

For each individual unitor correction locus:

  fixed gId coordinate
      =>
  unique corresponding gComp coordinate.

So the unitor loci are not arbitrary two-coordinate cylinders.  They are
graphs over their identity-gauge coordinate, at least at the level of the
footprint values relevant to correctness.

This is weaker than full shared-coordinate rigidity and does not yet prove
global witness correlation.  The next route-specific task is to propagate
these graph constraints across overlaps:

1. left/left and right/right unitor overlaps sharing one identity coordinate;
2. mixed left/right unitor overlaps;
3. associator/unitor overlaps, where the associator equation may transport
   composition-gauge values between different unitor graph constraints.

That is the concrete route toward testing v3.20 star transitivity.
-/

end KUOS.DependentOriginationUnitorPartialRigidityV3_22
