import KUOS.DependentOriginationHigherLocalizationLiftingProblemV3_04

namespace KUOS.DependentOriginationQuotientTransportObstructionV3_05

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationFiveGeneratedCorrectionCoboundaryV3_00
open KUOS.DependentOriginationCoboundaryStageSplitV3_02
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationHigherLocalizationLiftingProblemV3_04

universe u v uH vH

/-!
# Quotient-stage obstruction equals coherent quotient transport v3.05

v3.04 returned the v2.69--v2.95 correction frontier to the original
higher-localization factorization problem as two consecutive stages:

1. solve the quotient gauge coboundary in `gId/gComp`;
2. lift a comparison gauge `gIso` over that solution.

The first stage is still written in correction coordinates.  This file removes
that presentation layer.

A solved quotient gauge determines exactly one set of coherent `mapId` and
`mapComp` witnesses, hence a genuine v2.59 `CoherentQuotientTransportData`.
Conversely every coherent quotient transport differs from the canonical
generated witnesses by unique right gauge automorphisms

```text
gId   = generatedMapId^{-1}   * T.mapId
gComp = generatedMapComp^{-1} * T.mapComp.
```

Those automorphisms solve the quotient coboundary because the three equations
are precisely the pseudofunctor coherence laws already carried by `T`.

Therefore

```text
GeneratedQuotientGaugeCoboundarySolvable
        ↔
HasCoherentQuotientTransportData.
```

The first obstruction is thus not a new correction-theoretic object.  It is
exactly the original v2.59 existence problem for the localized pseudofunctor
carrier.  The only obstruction remaining after such a carrier is chosen is the
comparison lift of v3.04.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Normal-form quotient gauge measuring a coherent transport against the
canonical generated identity/composition witnesses. -/
noncomputable def generatedQuotientGaugeParametersOfCoherentTransport
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D) :
    GeneratedQuotientGaugeParameters W R D where
  mapIdGauge X :=
    (generatedIdentityMapIso W R D X).symm ≪≫ T.mapId X
  mapCompGauge f g :=
    (generatedCompositionMapIso W R D f g).symm ≪≫ T.mapComp f g

/-- Adjusting the canonical generated identity witness by the normal-form
quotient gauge recovers the coherent transport identity witness. -/
@[simp]
theorem gaugeAdjusted_coherentTransport_mapId
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D)
    (X : W.Localization) :
    (gaugeAdjustedGeneratedPointwiseChoice W R D
      (canonicalPointwiseGaugeOfQuotientGauge W R D
        (generatedQuotientGaugeParametersOfCoherentTransport W R D T))).mapId X =
      T.mapId X := by
  change
    generatedIdentityMapIso W R D X ≪≫
        ((generatedIdentityMapIso W R D X).symm ≪≫ T.mapId X) =
      T.mapId X
  exact Iso.self_symm_id_assoc _ _

/-- The same normal form recovers the coherent composition witness. -/
@[simp]
theorem gaugeAdjusted_coherentTransport_mapComp
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D)
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    (gaugeAdjustedGeneratedPointwiseChoice W R D
      (canonicalPointwiseGaugeOfQuotientGauge W R D
        (generatedQuotientGaugeParametersOfCoherentTransport W R D T))).mapComp f g =
      T.mapComp f g := by
  change
    generatedCompositionMapIso W R D f g ≪≫
        ((generatedCompositionMapIso W R D f g).symm ≪≫ T.mapComp f g) =
      T.mapComp f g
  exact Iso.self_symm_id_assoc _ _

/-- Every coherent quotient transport yields a solution of the minimal
quotient-gauge coboundary. -/
noncomputable def generatedQuotientGaugeCoboundaryOfCoherentTransport
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D) :
    GeneratedQuotientGaugeCoboundary W R D
      (generatedQuotientGaugeParametersOfCoherentTransport W R D T) := by
  change
    GeneratedGaugeQuotientCoboundary W R D
      (canonicalPointwiseGaugeOfQuotientGauge W R D
        (generatedQuotientGaugeParametersOfCoherentTransport W R D T))
  refine
    { associator := ?_
      leftUnitor := ?_
      rightUnitor := ?_ }
  · intro X Y Z K f g h
    simpa only [gaugeAdjusted_coherentTransport_mapComp] using
      (T.map₂_associator f g h)
  · intro X Y f
    simpa only
      [gaugeAdjusted_coherentTransport_mapId,
       gaugeAdjusted_coherentTransport_mapComp] using
      (T.map₂_left_unitor f)
  · intro X Y f
    simpa only
      [gaugeAdjusted_coherentTransport_mapId,
       gaugeAdjusted_coherentTransport_mapComp] using
      (T.map₂_right_unitor f)

/-- A solved quotient gauge directly constructs the genuine v2.59 coherent
quotient transport; there is no additional hidden first-stage datum. -/
noncomputable def coherentQuotientTransportDataOfGeneratedQuotientGaugeCoboundary
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hQ : GeneratedQuotientGaugeCoboundary W R D Q) :
    CoherentQuotientTransportData (W := W) R D where
  mapId :=
    (gaugeAdjustedGeneratedPointwiseChoice W R D
      (canonicalPointwiseGaugeOfQuotientGauge W R D Q)).mapId
  mapComp :=
    (gaugeAdjustedGeneratedPointwiseChoice W R D
      (canonicalPointwiseGaugeOfQuotientGauge W R D Q)).mapComp
  map₂_associator := by
    intro X Y Z K f g h
    exact hQ.associator f g h
  map₂_left_unitor := by
    intro X Y f
    exact hQ.leftUnitor f
  map₂_right_unitor := by
    intro X Y f
    exact hQ.rightUnitor f

/-- Main first-stage characterization: quotient-gauge solvability is exactly
existence of coherent quotient transport in the original v2.59 sense. -/
theorem generatedQuotientGaugeCoboundarySolvable_iff_hasCoherentQuotientTransportData
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    GeneratedQuotientGaugeCoboundarySolvable W R D ↔
      HasCoherentQuotientTransportData W R D := by
  constructor
  · rintro ⟨Q, hQ⟩
    exact
      ⟨coherentQuotientTransportDataOfGeneratedQuotientGaugeCoboundary
        W R D Q hQ⟩
  · rintro ⟨T⟩
    exact
      ⟨generatedQuotientGaugeParametersOfCoherentTransport W R D T,
        generatedQuotientGaugeCoboundaryOfCoherentTransport W R D T⟩

/-- Equivalently, the v3.02 full-gauge first stage is exactly the v2.59
coherent-transport existence problem. -/
theorem generatedQuotientCoboundarySolvable_iff_hasCoherentQuotientTransportData
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    GeneratedQuotientCoboundarySolvable W R D ↔
      HasCoherentQuotientTransportData W R D := by
  rw [generatedQuotientCoboundarySolvable_iff_quotientGaugeCoboundarySolvable
    W R D]
  exact
    generatedQuotientGaugeCoboundarySolvable_iff_hasCoherentQuotientTransportData
      W R D

/-- Solving the first correction stage therefore constructs an actual localized
higher-system carrier, not merely formal gauge data. -/
theorem hasLocalizedHigherSystem_of_generatedQuotientGaugeCoboundarySolvable
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (h : GeneratedQuotientGaugeCoboundarySolvable W R D) :
    Nonempty
      (KUOS.DependentOriginationHigherStackDescentV2_8.HigherLocalizedDescentSystem.{u, v, uH, vH}
        (W := W)) := by
  apply hasLocalizedHigherSystem_of_coherentQuotientTransport W R D
  exact
    (generatedQuotientGaugeCoboundarySolvable_iff_hasCoherentQuotientTransportData
      W R D).1 h

/-- The residual factorization problem can now be stated over an actual coherent
quotient transport rather than over abstract quotient-gauge coordinates. -/
def GeneratedComparisonLiftOverCoherentTransport
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D) : Prop :=
  GeneratedComparisonGaugeLiftSolvable W R D
    (generatedQuotientGaugeParametersOfCoherentTransport W R D T)
    (generatedQuotientGaugeCoboundaryOfCoherentTransport W R D T)

/-- Once a coherent quotient carrier is present, solving only its residual
comparison lift is sufficient for genuine higher-localization factorization. -/
theorem hasHigherLocalizationFactorization_of_coherentTransport_and_comparisonLift
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D)
    (hLift : GeneratedComparisonLiftOverCoherentTransport W R D T) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_quotient_and_comparisonLift
    W R D
    (generatedQuotientGaugeParametersOfCoherentTransport W R D T)
    (generatedQuotientGaugeCoboundaryOfCoherentTransport W R D T)
    hLift

/-!
## Factorization frontier after v3.05

The first stage has returned completely to the original higher-localization
language:

```text
IsHigherWAdmissible W R
        |
        v
pointwise adjoint-equivalence data D
        |
        ?  first obstruction
        v
CoherentQuotientTransportData W R D
        |
        v
actual localized pseudofunctor carrier
        |
        ?  residual comparison lift
        v
HigherLocalizationFactorization.
```

The correction coordinates `gId/gComp` are now proved to be a normal-form
presentation of the v2.59 coherent transport problem, not an additional
mathematical obstruction.

The next question is correspondingly sharper: determine whether weak
admissibility forces coherent quotient transport, or identify the precise
automorphism-valued obstruction to that existence.  Only after the first stage
is resolved does the comparison-lift obstruction remain.
-/

end KUOS.DependentOriginationQuotientTransportObstructionV3_05
