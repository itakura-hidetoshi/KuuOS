import KUOS.DependentOriginationCorrectionCoboundarySolvabilityV3_01

namespace KUOS.DependentOriginationCoboundaryStageSplitV3_02

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherenceDefectsV2_65
open KUOS.DependentOriginationFiveGeneratedCorrectionCoboundaryV3_00
open KUOS.DependentOriginationCorrectionCoboundarySolvabilityV3_01

universe u v uH vH

/-!
# Two-stage split of the generated correction coboundary v3.02

v3.00 writes the five required correction faces as one explicit coboundary.
v3.01 proves that solvability of this coboundary is exactly the coherent-data
obstruction already isolated in v2.66.

The five equations have an intrinsic dependency order:

1. associativity, left unit, and right unit first construct the quotient
   pseudofunctor;
2. only after that carrier exists do the comparison identity and comparison
   composition equations make sense.

This file exposes that dependency as an exact logical split.  For a fixed
candidate lower-dimensional gauge G we define the residual comparison
coboundary above a chosen solution of the first three quotient equations, and
prove

```text
FiveGeneratedCorrectionCoboundary G
  ↔
∃ hQ : GeneratedGaugeQuotientCoboundary G,
  GeneratedComparisonCoboundaryResidual G hQ.
```

At the existence level this gives a genuine obstruction filtration:

```text
full coboundary solvable
        ->
quotient coboundary solvable
        ->
comparison residual remains.
```

The reverse first arrow is deliberately not asserted: solving the first three
faces need not solve the last two.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The two comparison equations remaining after the first three quotient
coboundary equations have produced a genuine quotient pseudofunctor. -/
structure GeneratedComparisonCoboundaryResidual
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (G : GeneratedPointwiseGaugeParameters W R D)
    (hQ : GeneratedGaugeQuotientCoboundary W R D G) : Prop where
  comparisonIdentity :
    ∀ X : Context,
      let L := gaugeAdjustedGeneratedPointwiseChoice W R D G
      let q := generatedGaugeQuotientDefectsTrivial W R D G hQ
      let T := coherentQuotientTransportDataOfTrivialDefects W R D L q
      (comparisonNaturalityIsoOfTrivialTransportDefects W R D L q (𝟙 X)).hom ≫
          (𝟙 (R.obj (.mk X))) ◁ (R.mapId (.mk X)).hom =
        ((restrictedCoherentQuotientSystem W R D T).mapId (.mk X)).hom ▷
            (𝟙 (R.obj (.mk X))) ≫
          (λ_ (𝟙 (R.obj (.mk X)))).hom ≫
          (ρ_ (𝟙 (R.obj (.mk X)))).inv
  comparisonComposition :
    ∀ {X Y Z : Context} (f : X ⟶ Y) (g : Y ⟶ Z),
      let L := gaugeAdjustedGeneratedPointwiseChoice W R D G
      let q := generatedGaugeQuotientDefectsTrivial W R D G hQ
      let T := coherentQuotientTransportDataOfTrivialDefects W R D L q
      (comparisonNaturalityIsoOfTrivialTransportDefects W R D L q (f ≫ g)).hom ≫
          (𝟙 (R.obj (.mk X))) ◁ (R.mapComp f.toLoc g.toLoc).hom =
        ((restrictedCoherentQuotientSystem W R D T).mapComp
            f.toLoc g.toLoc).hom ▷ (𝟙 (R.obj (.mk Z))) ≫
          (α_ _ _ _).hom ≫
          (restrictedCoherentQuotientSystem W R D T).map f.toLoc ◁
            (comparisonNaturalityIsoOfTrivialTransportDefects W R D L q g).hom ≫
          (α_ _ _ _).inv ≫
          (comparisonNaturalityIsoOfTrivialTransportDefects W R D L q f).hom ▷
            R.map g.toLoc ≫
          (α_ _ _ _).hom

/-- For a fixed candidate gauge, the v3.00 five-face coboundary is exactly the
first-three quotient solution plus the residual two comparison equations. -/
theorem fiveGeneratedCorrectionCoboundary_iff_quotient_and_comparisonResidual
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (G : GeneratedPointwiseGaugeParameters W R D) :
    FiveGeneratedCorrectionCoboundary W R D G ↔
      ∃ hQ : GeneratedGaugeQuotientCoboundary W R D G,
        GeneratedComparisonCoboundaryResidual W R D G hQ := by
  constructor
  · intro H
    refine ⟨H.quotient, ?_⟩
    exact
      { comparisonIdentity := H.comparisonIdentity
        comparisonComposition := H.comparisonComposition }
  · rintro ⟨hQ, hC⟩
    exact
      { quotient := hQ
        comparisonIdentity := hC.comparisonIdentity
        comparisonComposition := hC.comparisonComposition }

/-- Solvability of the first three quotient faces, without assuming that the
comparison residual can be lifted. -/
def GeneratedQuotientCoboundarySolvable
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  ∃ G : GeneratedPointwiseGaugeParameters W R D,
    GeneratedGaugeQuotientCoboundary W R D G

/-- Full generated coboundary solvability always implies solvability of the
first three quotient faces. -/
theorem generatedQuotientCoboundarySolvable_of_generatedCorrectionCoboundarySolvable
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (h : GeneratedCorrectionCoboundarySolvable W R D) :
    GeneratedQuotientCoboundarySolvable W R D := by
  rcases h with ⟨G, H⟩
  exact ⟨G, H.quotient⟩

/-- Exact existence-level stage split.  The residual comparison problem is
indexed by the actual quotient-coboundary witness, reflecting the fact that the
comparison equations are defined only after the quotient carrier has been
constructed. -/
theorem generatedCorrectionCoboundarySolvable_iff_twoStage
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    GeneratedCorrectionCoboundarySolvable W R D ↔
      ∃ G : GeneratedPointwiseGaugeParameters W R D,
        ∃ hQ : GeneratedGaugeQuotientCoboundary W R D G,
          GeneratedComparisonCoboundaryResidual W R D G hQ := by
  constructor
  · rintro ⟨G, H⟩
    refine ⟨G, ?_⟩
    exact
      (fiveGeneratedCorrectionCoboundary_iff_quotient_and_comparisonResidual
        W R D G).1 H
  · rintro ⟨G, hQ, hC⟩
    refine ⟨G, ?_⟩
    exact
      (fiveGeneratedCorrectionCoboundary_iff_quotient_and_comparisonResidual
        W R D G).2 ⟨hQ, hC⟩

/-- Coherent general-W data therefore have the same exact two-stage
characterization. -/
theorem hasCoherentGeneralWFactorizationData_iff_twoStageCoboundary
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    HasCoherentGeneralWFactorizationData W R D ↔
      ∃ G : GeneratedPointwiseGaugeParameters W R D,
        ∃ hQ : GeneratedGaugeQuotientCoboundary W R D G,
          GeneratedComparisonCoboundaryResidual W R D G hQ := by
  rw [← generatedCorrectionCoboundarySolvable_iff_hasCoherentGeneralWFactorizationData
    W R D]
  exact generatedCorrectionCoboundarySolvable_iff_twoStage W R D

/-!
## Boundary fixed by v3.02

The obstruction is now filtered rather than presented as one undifferentiated
five-equation package:

```text
gId / gComp / gIso
        |
        v
three quotient coboundary equations
        |
        v
actual quotient pseudofunctor carrier
        |
        v
two comparison residual equations
        |
        v
coherent general-W factorization data.
```

This identifies two distinct places where weak admissibility might fail to close
Stage I.

The next theorem unit should remove the irrelevant gIso dependence from the
first stage explicitly: prove that GeneratedGaugeQuotientCoboundary depends only
on mapIdGauge and mapCompGauge, then define a quotient-only gauge parameter
space.  After that, the residual comparison obstruction can be studied as the
actual lifting problem for mapIsoGauge.

No implication from quotient-stage solvability alone to full factorization is
introduced.
-/

end KUOS.DependentOriginationCoboundaryStageSplitV3_02
