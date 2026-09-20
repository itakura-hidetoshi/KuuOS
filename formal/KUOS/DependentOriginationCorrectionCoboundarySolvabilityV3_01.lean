import KUOS.DependentOriginationFiveGeneratedCorrectionCoboundaryV3_00

namespace KUOS.DependentOriginationCorrectionCoboundarySolvabilityV3_01

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationPointwiseGeneralWChoiceV2_61
open KUOS.DependentOriginationCoherenceDefectsV2_65
open KUOS.DependentOriginationGaugeObstructionV2_66
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationFiveGeneratedCorrectionCoboundaryV3_00

universe u v uH vH

/-!
# Solvability of the generated correction coboundary v3.01

v3.00 gives a constructive sufficient route from three lower-dimensional gauge
families and five explicit coboundary equations to higher-localization
factorization.  The next question is whether this coboundary language loses any
of the already identified coherent-data obstruction.

It does not.

Every pointwise v2.61 choice determines a unique normal-form gauge from the
canonical generated pointwise choice by the right quotient
`generated⁻¹ * target`.  Right-composing the generated witnesses with these
three gauge families recovers the target pointwise choice.  Hence every
zero-five-defect representative can be presented as a v3.00 generated
correction coboundary.

The main equivalence is therefore

```text
GeneratedCorrectionCoboundarySolvable
        ↔
∃ pointwise choice with FiveCoherenceDefectsTrivial
        ↔
HasCoherentGeneralWFactorizationData.
```

This is an exact characterization of the coherent-data obstruction.  It is not
claimed to characterize every possible `HasHigherLocalizationFactorization`,
because the converse from arbitrary factorization to the chosen coherent-data
package has not been proved.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Existence of one compatible lower-dimensional gauge whose five induced
faces satisfy the v3.00 coboundary equations. -/
def GeneratedCorrectionCoboundarySolvable
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  ∃ G : GeneratedPointwiseGaugeParameters W R D,
    FiveGeneratedCorrectionCoboundary W R D G

/-- Normal-form gauge parameters from the canonical generated pointwise choice
to an arbitrary target pointwise choice. -/
noncomputable def generatedGaugeParametersToChoice
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D) :
    GeneratedPointwiseGaugeParameters W R D where
  mapIdGauge X :=
    (generatedIdentityMapIso W R D X).symm ≪≫ L.mapId X
  mapCompGauge f g :=
    (generatedCompositionMapIso W R D f g).symm ≪≫ L.mapComp f g
  mapIsoGauge f :=
    (generatedPresentationMapIso W R D f).symm ≪≫ L.mapIso f

@[simp]
theorem gaugeAdjusted_toChoice_mapId
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    (X : W.Localization) :
    (gaugeAdjustedGeneratedPointwiseChoice W R D
      (generatedGaugeParametersToChoice W R D L)).mapId X =
      L.mapId X := by
  simp [gaugeAdjustedGeneratedPointwiseChoice,
    generatedGaugeParametersToChoice, Category.assoc]

@[simp]
theorem gaugeAdjusted_toChoice_mapComp
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    (gaugeAdjustedGeneratedPointwiseChoice W R D
      (generatedGaugeParametersToChoice W R D L)).mapComp f g =
      L.mapComp f g := by
  simp [gaugeAdjustedGeneratedPointwiseChoice,
    generatedGaugeParametersToChoice, Category.assoc]

@[simp]
theorem gaugeAdjusted_toChoice_mapIso
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    {X Y : Context} (f : X ⟶ Y) :
    (gaugeAdjustedGeneratedPointwiseChoice W R D
      (generatedGaugeParametersToChoice W R D L)).mapIso f =
      L.mapIso f := by
  simp [gaugeAdjustedGeneratedPointwiseChoice,
    generatedGaugeParametersToChoice, Category.assoc]

/-- The normal-form gauge adjustment recovers the entire target pointwise
choice, not only each family separately. -/
theorem gaugeAdjustedGeneratedPointwiseChoice_toChoice_eq
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D) :
    gaugeAdjustedGeneratedPointwiseChoice W R D
        (generatedGaugeParametersToChoice W R D L) =
      L := by
  apply PointwiseGeneralWChoiceData.ext
  · funext X
    exact gaugeAdjusted_toChoice_mapId W R D L X
  · funext X Y Z f g
    exact gaugeAdjusted_toChoice_mapComp W R D L f g
  · funext X Y f
    exact gaugeAdjusted_toChoice_mapIso W R D L f

/-- The three quotient coherence equations of any zero-defect target choice are
the quotient part of a generated gauge coboundary in normal form. -/
noncomputable def generatedGaugeQuotientCoboundaryToChoice
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    (hQ : QuotientTransportDefectsTrivial W R D L) :
    GeneratedGaugeQuotientCoboundary W R D
      (generatedGaugeParametersToChoice W R D L) where
  associator f g h := by
    simpa only [gaugeAdjusted_toChoice_mapComp] using
      (quotientAssociatorDefect_eq_refl_iff W R D L f g h).1
        (hQ.associator f g h)
  leftUnitor f := by
    simpa only [gaugeAdjusted_toChoice_mapComp,
      gaugeAdjusted_toChoice_mapId] using
      (quotientLeftUnitorDefect_eq_refl_iff W R D L f).1
        (hQ.leftUnitor f)
  rightUnitor f := by
    simpa only [gaugeAdjusted_toChoice_mapComp,
      gaugeAdjusted_toChoice_mapId] using
      (quotientRightUnitorDefect_eq_refl_iff W R D L f).1
        (hQ.rightUnitor f)

/-- Every pointwise zero-five-defect representative has a v3.00 coboundary
presentation based at the canonical generated pointwise choice. -/
noncomputable def fiveGeneratedCorrectionCoboundaryToChoice
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    (h : FiveCoherenceDefectsTrivial W R D L) :
    FiveGeneratedCorrectionCoboundary W R D
      (generatedGaugeParametersToChoice W R D L) := by
  let hQ : QuotientTransportDefectsTrivial W R D L := Classical.choose h
  let hC : ComparisonDefectsTrivial W R D L hQ := Classical.choose_spec h
  let Hq : GeneratedGaugeQuotientCoboundary W R D
      (generatedGaugeParametersToChoice W R D L) :=
    generatedGaugeQuotientCoboundaryToChoice W R D L hQ
  let hQ' :=
    generatedGaugeQuotientDefectsTrivial W R D
      (generatedGaugeParametersToChoice W R D L) Hq
  have hhQ : hQ' = hQ := Subsingleton.elim _ _
  refine
    { quotient := Hq
      comparisonIdentity := ?_
      comparisonComposition := ?_ }
  · intro X
    change
      let L' := gaugeAdjustedGeneratedPointwiseChoice W R D
        (generatedGaugeParametersToChoice W R D L)
      let q' := generatedGaugeQuotientDefectsTrivial W R D
        (generatedGaugeParametersToChoice W R D L) Hq
      let T := coherentQuotientTransportDataOfTrivialDefects W R D L' q'
      (comparisonNaturalityIsoOfTrivialTransportDefects W R D L' q' (𝟙 X)).hom ≫
          (𝟙 (R.obj (.mk X))) ◁ (R.mapId (.mk X)).hom =
        ((restrictedCoherentQuotientSystem W R D T).mapId (.mk X)).hom ▷
            (𝟙 (R.obj (.mk X))) ≫
          (λ_ (𝟙 (R.obj (.mk X)))).hom ≫
          (ρ_ (𝟙 (R.obj (.mk X)))).inv
    rw [gaugeAdjustedGeneratedPointwiseChoice_toChoice_eq W R D L]
    rw [show generatedGaugeQuotientDefectsTrivial W R D
        (generatedGaugeParametersToChoice W R D L) Hq = hQ by
      exact Subsingleton.elim _ _]
    exact
      (comparisonIdentityDefect_eq_refl_iff W R D L hQ X).1
        (hC.identity X)
  · intro X Y Z f g
    change
      let L' := gaugeAdjustedGeneratedPointwiseChoice W R D
        (generatedGaugeParametersToChoice W R D L)
      let q' := generatedGaugeQuotientDefectsTrivial W R D
        (generatedGaugeParametersToChoice W R D L) Hq
      let T := coherentQuotientTransportDataOfTrivialDefects W R D L' q'
      (comparisonNaturalityIsoOfTrivialTransportDefects W R D L' q' (f ≫ g)).hom ≫
          (𝟙 (R.obj (.mk X))) ◁ (R.mapComp f.toLoc g.toLoc).hom =
        ((restrictedCoherentQuotientSystem W R D T).mapComp
            f.toLoc g.toLoc).hom ▷ (𝟙 (R.obj (.mk Z))) ≫
          (α_ _ _ _).hom ≫
          (restrictedCoherentQuotientSystem W R D T).map f.toLoc ◁
            (comparisonNaturalityIsoOfTrivialTransportDefects W R D L' q' g).hom ≫
          (α_ _ _ _).inv ≫
          (comparisonNaturalityIsoOfTrivialTransportDefects W R D L' q' f).hom ▷
            R.map g.toLoc ≫
          (α_ _ _ _).hom
    rw [gaugeAdjustedGeneratedPointwiseChoice_toChoice_eq W R D L]
    rw [show generatedGaugeQuotientDefectsTrivial W R D
        (generatedGaugeParametersToChoice W R D L) Hq = hQ by
      exact Subsingleton.elim _ _]
    exact
      (comparisonCompositionDefect_eq_refl_iff W R D L hQ f g).1
        (hC.composition f g)

/-- Solvability of the explicit v3.00 coboundary is exactly existence of a
pointwise representative on which all five coherence defects vanish. -/
theorem generatedCorrectionCoboundarySolvable_iff_exists_fiveTrivialDefects
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    GeneratedCorrectionCoboundarySolvable W R D ↔
      ∃ L : PointwiseGeneralWChoiceData (W := W) R D,
        FiveCoherenceDefectsTrivial W R D L := by
  constructor
  · rintro ⟨G, H⟩
    exact
      ⟨gaugeAdjustedGeneratedPointwiseChoice W R D G,
        fiveCoherenceDefectsTrivial_of_fiveGeneratedCorrectionCoboundary
          W R D G H⟩
  · rintro ⟨L, hL⟩
    exact
      ⟨generatedGaugeParametersToChoice W R D L,
        fiveGeneratedCorrectionCoboundaryToChoice W R D L hL⟩

/-- Main v3.01 characterization: the generated correction coboundary is exactly
the coherent general-W extension obstruction already isolated in v2.66. -/
theorem generatedCorrectionCoboundarySolvable_iff_hasCoherentGeneralWFactorizationData
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    GeneratedCorrectionCoboundarySolvable W R D ↔
      HasCoherentGeneralWFactorizationData W R D := by
  rw [generatedCorrectionCoboundarySolvable_iff_exists_fiveTrivialDefects W R D]
  exact
    (hasCoherentGeneralWFactorizationData_iff_exists_fiveTrivialDefects
      W R D).symm

/-- In particular, coboundary solvability gives factorization through the exact
coherent-data route. -/
theorem hasHigherLocalizationFactorization_of_generatedCorrectionCoboundarySolvable
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (h : GeneratedCorrectionCoboundarySolvable W R D) :
    HasHigherLocalizationFactorization (W := W) R := by
  have hC : HasCoherentGeneralWFactorizationData W R D :=
    (generatedCorrectionCoboundarySolvable_iff_hasCoherentGeneralWFactorizationData
      W R D).1 h
  exact
    hasHigherLocalizationFactorization_of_hasCoherentGeneralWFactorizationData
      W R D hC

/-!
## Boundary fixed by v3.01

The v2.69--v3.00 correction line has now been identified exactly with the
v2.66 coherent-data obstruction:

```text
five generated route corrections
arise from one lower-dimensional gauge coboundary
        ↔
some pointwise choice has zero five defects
        ↔
HasCoherentGeneralWFactorizationData.
```

Thus the remaining Stage-I question is no longer whether the correction language
is expressive enough.  It is exactly the existence question for the coboundary.

The next theorem unit should study the obstruction to solving the five equations
from weak admissibility itself.  A productive split is:

1. isolate the first three quotient equations as a nonabelian 2-coboundary
   problem for `gComp/gId`;
2. conditional on that solution, isolate the two comparison equations as the
   residual `gIso` lifting problem;
3. determine whether either residual is forced to vanish by the generated
   localization relations, or whether a genuinely 2-dimensional carrier is
   needed.

No converse from arbitrary `HasHigherLocalizationFactorization` to coherent
general-W data is asserted.
-/

end KUOS.DependentOriginationCorrectionCoboundarySolvabilityV3_01
