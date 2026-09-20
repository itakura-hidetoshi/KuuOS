import KUOS.DependentOriginationCorrectionToFactorizationV2_96
import KUOS.DependentOriginationGeneratedCoherenceRoutesV2_68
import KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80

namespace KUOS.DependentOriginationCorrectedGeneratedRouteV2_97

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationGeneratedCoherenceRoutesV2_68
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80

universe u v uH vH s q

/-!
# Corrected generated-route equality v2.97

v2.96 reconnects correction power to Stage-I factorization once the reachable
correction image meets the zero-five-defect locus.  The remaining problem is to
lift generated-holonomy correctability to such a coherent correction.

This file establishes the first nontrivial step of that lift.

For two generated localization derivations `alpha` and `beta` with common
endpoints, their difference loop has holonomy

```text
E(alpha)^(-1) * E(beta).
```

Therefore, if that difference-loop holonomy lies in a correction image, an
admissible correction parameter can be postcomposed with `E(alpha)` to obtain
`E(beta)` exactly:

```text
E(alpha) * correction = E(beta).
```

This is stronger than merely labeling the loop "correctable": it produces an
explicit corrected route equality.

The file also names the five difference loops underlying the exact v2.68
coherence route pairs: associativity, left unit, right unit, comparison
identity, and comparison composition.  The next obligation is global: decide
when corrections of these five families assemble into one pointwise-choice
gauge rather than five unrelated local repairs.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Explicit witness that a correction parameter repairs one generated-route
comparison.  The correction acts at the common target of the two evaluated
routes. -/
structure CorrectedGeneratedRouteWitness
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p r : X ⟶ Y}
    (alpha beta : GeneratedLocalization2Cell W p r)
    {State : Type s} {Param : Type q}
    (C : CorrectionRealization State Param
      ((freePathEvaluator W R D).map r ≅
        (freePathEvaluator W R D).map r))
    (x : State) where
  parameter : Param
  admissible : C.admissible x parameter
  corrected_evaluation :
    generatedLocalization2CellEvaluationIso W R D alpha ≪≫
        C.effect x parameter =
      generatedLocalization2CellEvaluationIso W R D beta

/-- Correctability of the difference-loop holonomy produces an exact corrected
route equality. -/
noncomputable def correctedGeneratedRouteWitness_of_correctable
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p r : X ⟶ Y}
    (alpha beta : GeneratedLocalization2Cell W p r)
    {State : Type s} {Param : Type q}
    (C : CorrectionRealization State Param
      ((freePathEvaluator W R D).map r ≅
        (freePathEvaluator W R D).map r))
    (x : State)
    (h :
      GeneratedHolonomyCorrectable W R D C x
        (generatedLocalization2CellDifference W alpha beta)) :
    CorrectedGeneratedRouteWitness W R D alpha beta C x := by
  rcases h with ⟨c, hc, heffect⟩
  refine
    { parameter := c
      admissible := hc
      corrected_evaluation := ?_ }
  rw [heffect, generatedLocalization2CellDifference_holonomy]
  apply Iso.ext
  simp [Iso.trans_hom, Category.assoc]

/-- Proposition-level form: a generated route pair is correction-repairable
exactly when the difference-loop holonomy is reachable by the supplied
authority. -/
def GeneratedRouteCorrectionReachable
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p r : X ⟶ Y}
    (alpha beta : GeneratedLocalization2Cell W p r)
    {State : Type s} {Param : Type q}
    (C : CorrectionRealization State Param
      ((freePathEvaluator W R D).map r ≅
        (freePathEvaluator W R D).map r))
    (x : State) : Prop :=
  GeneratedHolonomyCorrectable W R D C x
    (generatedLocalization2CellDifference W alpha beta)

/-- Reachability of a route correction always has an explicit repaired-route
witness. -/
theorem nonempty_correctedGeneratedRouteWitness_of_reachable
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p r : X ⟶ Y}
    (alpha beta : GeneratedLocalization2Cell W p r)
    {State : Type s} {Param : Type q}
    (C : CorrectionRealization State Param
      ((freePathEvaluator W R D).map r ≅
        (freePathEvaluator W R D).map r))
    (x : State)
    (h : GeneratedRouteCorrectionReachable W R D alpha beta C x) :
    Nonempty (CorrectedGeneratedRouteWitness W R D alpha beta C x) :=
  ⟨correctedGeneratedRouteWitness_of_correctable
    W R D alpha beta C x h⟩

/-! ## The five generated coherence difference loops -/

/-- Difference loop measuring the generated associativity route comparison. -/
noncomputable def generatedQuotientAssociatorDifferenceLoop
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) :
    GeneratedLocalizationLoop W (Quot.out (f ≫ (g ≫ h))) :=
  generatedLocalization2CellDifference W
    (generatedQuotientAssociatorRoute W f g h)
    (generatedQuotientAssociatorDirect W f g h)

/-- Difference loop measuring the generated left-unit route comparison. -/
noncomputable def generatedQuotientLeftUnitorDifferenceLoop
    {X Y : W.Localization} (f : X ⟶ Y) :
    GeneratedLocalizationLoop W (Quot.out f) :=
  generatedLocalization2CellDifference W
    (generatedQuotientLeftUnitorRoute W f)
    (generatedQuotientLeftUnitorDirect W f)

/-- Difference loop measuring the generated right-unit route comparison. -/
noncomputable def generatedQuotientRightUnitorDifferenceLoop
    {X Y : W.Localization} (f : X ⟶ Y) :
    GeneratedLocalizationLoop W (Quot.out f) :=
  generatedLocalization2CellDifference W
    (generatedQuotientRightUnitorRoute W f)
    (generatedQuotientRightUnitorDirect W f)

/-- Difference loop measuring the generated identity-comparison route pair. -/
noncomputable def generatedComparisonIdentityDifferenceLoop
    (X : Context) :
    GeneratedLocalizationLoop W (𝟙 _) :=
  generatedLocalization2CellDifference W
    (generatedComparisonIdentityRawRoute W X)
    (generatedComparisonIdentityQuotientRoute W X)

/-- Difference loop measuring the generated composition-comparison route pair. -/
noncomputable def generatedComparisonCompositionDifferenceLoop
    {X Y Z : Context} (f : X ⟶ Y) (g : Y ⟶ Z) :
    GeneratedLocalizationLoop W
      (Localization.Construction.ψ₁ W f ≫
        Localization.Construction.ψ₁ W g) :=
  generatedLocalization2CellDifference W
    (generatedComparisonCompositionRawRoute W f g)
    (generatedComparisonCompositionQuotientRoute W f g)

/-! ## Named holonomy identities for the five loops -/

/-- The associativity difference-loop holonomy is exactly the right quotient of
the direct route evaluation by the long route evaluation. -/
theorem generatedQuotientAssociatorDifferenceLoop_holonomy
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) :
    generatedHolonomy W R D
        (generatedQuotientAssociatorDifferenceLoop W f g h) =
      (generatedLocalization2CellEvaluationIso W R D
        (generatedQuotientAssociatorRoute W f g h)).symm ≪≫
      generatedLocalization2CellEvaluationIso W R D
        (generatedQuotientAssociatorDirect W f g h) := by
  rfl

/-- The left-unit difference-loop holonomy is the corresponding route defect. -/
theorem generatedQuotientLeftUnitorDifferenceLoop_holonomy
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : W.Localization} (f : X ⟶ Y) :
    generatedHolonomy W R D
        (generatedQuotientLeftUnitorDifferenceLoop W f) =
      (generatedLocalization2CellEvaluationIso W R D
        (generatedQuotientLeftUnitorRoute W f)).symm ≪≫
      generatedLocalization2CellEvaluationIso W R D
        (generatedQuotientLeftUnitorDirect W f) := by
  rfl

/-- The right-unit difference-loop holonomy is the corresponding route defect. -/
theorem generatedQuotientRightUnitorDifferenceLoop_holonomy
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : W.Localization} (f : X ⟶ Y) :
    generatedHolonomy W R D
        (generatedQuotientRightUnitorDifferenceLoop W f) =
      (generatedLocalization2CellEvaluationIso W R D
        (generatedQuotientRightUnitorRoute W f)).symm ≪≫
      generatedLocalization2CellEvaluationIso W R D
        (generatedQuotientRightUnitorDirect W f) := by
  rfl

/-- The comparison-identity difference-loop holonomy is its route defect. -/
theorem generatedComparisonIdentityDifferenceLoop_holonomy
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (X : Context) :
    generatedHolonomy W R D
        (generatedComparisonIdentityDifferenceLoop W X) =
      (generatedLocalization2CellEvaluationIso W R D
        (generatedComparisonIdentityRawRoute W X)).symm ≪≫
      generatedLocalization2CellEvaluationIso W R D
        (generatedComparisonIdentityQuotientRoute W X) := by
  rfl

/-- The comparison-composition difference-loop holonomy is its route defect. -/
theorem generatedComparisonCompositionDifferenceLoop_holonomy
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : Context} (f : X ⟶ Y) (g : Y ⟶ Z) :
    generatedHolonomy W R D
        (generatedComparisonCompositionDifferenceLoop W f g) =
      (generatedLocalization2CellEvaluationIso W R D
        (generatedComparisonCompositionRawRoute W f g)).symm ≪≫
      generatedLocalization2CellEvaluationIso W R D
        (generatedComparisonCompositionQuotientRoute W f g) := by
  rfl

/-!
## Boundary fixed by v2.97

There is now a theorem-level bridge

```text
GeneratedHolonomyCorrectable
        |
        v
admissible correction parameter c
        |
        v
E(alpha) * c = E(beta)
```

for an arbitrary generated route pair, and the five exact v2.68 coherence route
pairs have named difference loops.

What is still not justified is the global inference

```text
all five route families individually correction-repairable
        -/->
one PointwiseChoiceGauge whose target has FiveCoherenceDefectsTrivial.
```

That is the next coherence problem.  A successful theorem must express the
compatibility equations tying the five local correction families together; if
those equations cannot be satisfied in general, that failure is evidence that
ordinary localization has discarded essential 2-dimensional data.
-/

end KUOS.DependentOriginationCorrectedGeneratedRouteV2_97
