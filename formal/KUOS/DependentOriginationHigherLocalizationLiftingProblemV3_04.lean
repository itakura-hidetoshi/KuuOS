import KUOS.DependentOriginationQuotientGaugeIndependenceV3_03

namespace KUOS.DependentOriginationHigherLocalizationLiftingProblemV3_04

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFiveGeneratedCorrectionCoboundaryV3_00
open KUOS.DependentOriginationCorrectionCoboundarySolvabilityV3_01
open KUOS.DependentOriginationCoboundaryStageSplitV3_02
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03

universe u v uH vH

/-!
# Higher-localization lifting problem v3.04

The v2.69 countermodel showed that weak admissibility does not force global
generated holonomy to vanish.  The correction program v2.70--v2.95 then
separated nontrivial holonomy from genuine hard obstruction.  v2.96--v3.03
returned that semantic correction theory to the five coherence equations
actually consumed by higher-localization factorization and split their
coboundary into two stages.

This file makes the return to the original factorization problem explicit.

After a quotient gauge `Q` solves the first three equations, the remaining
unknown is only the comparison gauge family

```text
gIso(f) : R.map f ≅ R.map f.
```

Extending `Q` by such a family produces a full generated pointwise gauge.  The
residual two comparison equations are therefore a genuine lifting problem over
the solved quotient carrier.

The resulting exact obstruction route is

```text
weak W-admissibility
        |
        v
pointwise W-adjoint equivalences
        |
        v
choose Q = (gId,gComp)
        |
        | three quotient coboundary equations
        v
quotient pseudofunctor carrier
        |
        | lift by gIso
        v
two comparison residual equations
        |
        v
five-face generated coboundary
        |
        v
coherent general-W factorization data
        |
        v
HigherLocalizationFactorization.
```

Thus v2.69--v2.95 no longer point toward global holonomy triviality.  Their
factorization-relevant content is exactly whether correction power can solve
this staged quotient/comparison lifting problem.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The only gauge family not fixed after quotient-stage descent. -/
abbrev GeneratedComparisonGaugeFamily
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)) :=
  ∀ {X Y : Context} (f : X ⟶ Y),
    R.map f.toLoc ≅ R.map f.toLoc

/-- Extending the quotient projection of a full gauge by its original
comparison family recovers that gauge exactly. -/
theorem extend_quotientGaugeParameters_mapIso_eq
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (G : GeneratedPointwiseGaugeParameters W R D) :
    extendGeneratedQuotientGaugeParameters W R D
        (quotientGaugeParametersOfPointwiseGauge W R D G)
        (fun f => G.mapIsoGauge f) =
      G := by
  cases G
  rfl

/-- A quotient-only coboundary solution canonically supplies the quotient
coboundary proof for every extension by a comparison gauge family. -/
def generatedGaugeQuotientCoboundaryOfExtension
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hQ : GeneratedQuotientGaugeCoboundary W R D Q)
    (gIso : GeneratedComparisonGaugeFamily R) :
    GeneratedGaugeQuotientCoboundary W R D
      (extendGeneratedQuotientGaugeParameters W R D Q gIso) := by
  apply
    generatedGaugeQuotientCoboundary_of_generatedQuotientGaugeCoboundary
      W R D
      (extendGeneratedQuotientGaugeParameters W R D Q gIso)
  simpa [quotientGaugeParametersOfPointwiseGauge,
    extendGeneratedQuotientGaugeParameters] using hQ

/-- For fixed solved quotient data, one comparison gauge family is a lift when
it solves exactly the two residual comparison equations. -/
def GeneratedComparisonGaugeLift
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hQ : GeneratedQuotientGaugeCoboundary W R D Q)
    (gIso : GeneratedComparisonGaugeFamily R) : Prop :=
  GeneratedComparisonCoboundaryResidual W R D
    (extendGeneratedQuotientGaugeParameters W R D Q gIso)
    (generatedGaugeQuotientCoboundaryOfExtension W R D Q hQ gIso)

/-- The second-stage obstruction over a fixed solved quotient gauge. -/
def GeneratedComparisonGaugeLiftSolvable
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hQ : GeneratedQuotientGaugeCoboundary W R D Q) : Prop :=
  ∃ gIso : GeneratedComparisonGaugeFamily R,
    GeneratedComparisonGaugeLift W R D Q hQ gIso

/-- On a fixed quotient solution, the full five-face coboundary for one
extension is exactly the comparison-gauge lifting condition. -/
theorem fiveGeneratedCorrectionCoboundary_extension_iff_comparisonGaugeLift
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hQ : GeneratedQuotientGaugeCoboundary W R D Q)
    (gIso : GeneratedComparisonGaugeFamily R) :
    FiveGeneratedCorrectionCoboundary W R D
        (extendGeneratedQuotientGaugeParameters W R D Q gIso) ↔
      GeneratedComparisonGaugeLift W R D Q hQ gIso := by
  let G := extendGeneratedQuotientGaugeParameters W R D Q gIso
  let hQG : GeneratedGaugeQuotientCoboundary W R D G :=
    generatedGaugeQuotientCoboundaryOfExtension W R D Q hQ gIso
  constructor
  · intro H
    have hC :
        GeneratedComparisonCoboundaryResidual W R D G H.quotient :=
      { comparisonIdentity := H.comparisonIdentity
        comparisonComposition := H.comparisonComposition }
    have hp : H.quotient = hQG := Subsingleton.elim _ _
    simpa [GeneratedComparisonGaugeLift, G, hQG, hp] using hC
  · intro hLift
    have hC :
        GeneratedComparisonCoboundaryResidual W R D G hQG := by
      simpa [GeneratedComparisonGaugeLift, G, hQG] using hLift
    exact
      (fiveGeneratedCorrectionCoboundary_iff_quotient_and_comparisonResidual
        W R D G).2 ⟨hQG, hC⟩

/-- Exact existence-level reformulation of the coherent-data obstruction as a
minimal quotient solution followed by a comparison-gauge lift. -/
theorem generatedCorrectionCoboundarySolvable_iff_quotient_and_comparisonLift
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    GeneratedCorrectionCoboundarySolvable W R D ↔
      ∃ Q : GeneratedQuotientGaugeParameters W R D,
        ∃ hQ : GeneratedQuotientGaugeCoboundary W R D Q,
          GeneratedComparisonGaugeLiftSolvable W R D Q hQ := by
  constructor
  · rintro ⟨G, H⟩
    let Q := quotientGaugeParametersOfPointwiseGauge W R D G
    let hQ : GeneratedQuotientGaugeCoboundary W R D Q :=
      generatedQuotientGaugeCoboundary_of_generatedGaugeQuotientCoboundary
        W R D G H.quotient
    refine ⟨Q, hQ, ?_⟩
    let gIso : GeneratedComparisonGaugeFamily R := fun f => G.mapIsoGauge f
    refine ⟨gIso, ?_⟩
    have hG :
        extendGeneratedQuotientGaugeParameters W R D Q gIso = G := by
      exact extend_quotientGaugeParameters_mapIso_eq W R D G
    have hFull :
        FiveGeneratedCorrectionCoboundary W R D
          (extendGeneratedQuotientGaugeParameters W R D Q gIso) := by
      simpa [hG] using H
    exact
      (fiveGeneratedCorrectionCoboundary_extension_iff_comparisonGaugeLift
        W R D Q hQ gIso).1 hFull
  · rintro ⟨Q, hQ, gIso, hLift⟩
    refine
      ⟨extendGeneratedQuotientGaugeParameters W R D Q gIso, ?_⟩
    exact
      (fiveGeneratedCorrectionCoboundary_extension_iff_comparisonGaugeLift
        W R D Q hQ gIso).2 hLift

/-- The coherent general-W factorization package has the same staged lifting
characterization. -/
theorem hasCoherentGeneralWFactorizationData_iff_quotient_and_comparisonLift
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    HasCoherentGeneralWFactorizationData W R D ↔
      ∃ Q : GeneratedQuotientGaugeParameters W R D,
        ∃ hQ : GeneratedQuotientGaugeCoboundary W R D Q,
          GeneratedComparisonGaugeLiftSolvable W R D Q hQ := by
  rw [←
    generatedCorrectionCoboundarySolvable_iff_hasCoherentGeneralWFactorizationData
      W R D]
  exact generatedCorrectionCoboundarySolvable_iff_quotient_and_comparisonLift
    W R D

/-- Direct return to the original v2.10 problem: solving the quotient stage and
then the comparison lifting problem is sufficient for genuine
higher-localization factorization. -/
theorem hasHigherLocalizationFactorization_of_quotient_and_comparisonLift
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hQ : GeneratedQuotientGaugeCoboundary W R D Q)
    (hLift : GeneratedComparisonGaugeLiftSolvable W R D Q hQ) :
    HasHigherLocalizationFactorization (W := W) R := by
  have hCob : GeneratedCorrectionCoboundarySolvable W R D :=
    (generatedCorrectionCoboundarySolvable_iff_quotient_and_comparisonLift
      W R D).2 ⟨Q, hQ, hLift⟩
  exact
    hasHigherLocalizationFactorization_of_generatedCorrectionCoboundarySolvable
      W R D hCob

/-- Weak-admissibility-shaped endpoint.  The unresolved theorem is now exactly
the existence of a quotient solution and a comparison lift for the canonical
pointwise adjoint-equivalence data. -/
theorem hasHigherLocalizationFactorization_of_admissible_quotient_and_comparisonLift
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (hR : IsHigherWAdmissible W R)
    (Q : GeneratedQuotientGaugeParameters W R
      (pointwiseWAdjointEquivalenceDataOfAdmissible W hR))
    (hQ : GeneratedQuotientGaugeCoboundary W R
      (pointwiseWAdjointEquivalenceDataOfAdmissible W hR) Q)
    (hLift :
      GeneratedComparisonGaugeLiftSolvable W R
        (pointwiseWAdjointEquivalenceDataOfAdmissible W hR) Q hQ) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_quotient_and_comparisonLift
    W R (pointwiseWAdjointEquivalenceDataOfAdmissible W hR) Q hQ hLift

/-!
## Factorization frontier after v3.04

The v2.69--v2.95 correction theory is now attached directly to the original
higher-localization factorization problem without reintroducing the false
global-holonomy target.

The remaining existence question is precisely

```text
IsHigherWAdmissible W R
        ?
        v
∃ Q, GeneratedQuotientGaugeCoboundary Q
     ∧ comparison gauge lift over Q.
```

If that staged lift exists, genuine `HasHigherLocalizationFactorization`
follows.  What is not proved is that weak admissibility automatically makes
either obstruction vanish, nor that every arbitrary factorization must arise
from this chosen generated normal form.
-/

end KUOS.DependentOriginationHigherLocalizationLiftingProblemV3_04
