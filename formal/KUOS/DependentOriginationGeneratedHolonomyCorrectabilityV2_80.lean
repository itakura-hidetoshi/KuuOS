import KUOS.DependentOriginationCorrectionRealizationV2_74
import KUOS.DependentOriginationFilteredGeneratedHolonomyV2_73

namespace KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80

open CategoryTheory
open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationFilteredGeneratedHolonomyV2_73

universe u v uH vH s q m

variable {Context : Type u} [Category.{v} Context]

/-!
# Generated-holonomy correctability v2.80

A generated localization-loop holonomy may be nontrivial or non-flat while
still lying in an explicitly supplied correction image. Hard obstruction is a
strictly stronger classification: it requires explicit absence of a correction
witness.

This layer therefore keeps three notions separate:

* filtered flatness/non-flatness,
* correctability/robust correctability,
* hard obstruction.

No theorem derives hard obstruction merely from nontriviality or non-flatness.
-/

/-- The evaluated holonomy of a generated loop lies in an explicit correction
image at the supplied state. -/
def GeneratedHolonomyCorrectable
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    {State : Type s} {Param : Type q}
    (C : CorrectionRealization State Param
      ((freePathEvaluator W R D).map p ≅
        (freePathEvaluator W R D).map p))
    (x : State)
    (gamma : GeneratedLocalizationLoop W p) : Prop :=
  C.CorrectableAt x (generatedHolonomy W R D gamma)

/-- The evaluated generated holonomy has an explicit robust correction witness
at the supplied margin. -/
def GeneratedHolonomyRobustlyCorrectable
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    {State : Type s} {Param : Type q}
    (C : CorrectionRealization State Param
      ((freePathEvaluator W R D).map p ≅
        (freePathEvaluator W R D).map p))
    {Margin : Type m} [Preorder Margin]
    (RC : RobustCorrectionData C Margin)
    (mu : Margin)
    (x : State)
    (gamma : GeneratedLocalizationLoop W p) : Prop :=
  RC.robustAt mu x (generatedHolonomy W R D gamma)

/-- Hard generated-holonomy obstruction means explicit failure of correction
image membership at the supplied state. -/
def GeneratedHolonomyHardObstruction
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    {State : Type s} {Param : Type q}
    (C : CorrectionRealization State Param
      ((freePathEvaluator W R D).map p ≅
        (freePathEvaluator W R D).map p))
    (x : State)
    (gamma : GeneratedLocalizationLoop W p) : Prop :=
  C.HardObstructionAt x (generatedHolonomy W R D gamma)

/-- Robust generated-holonomy correctability gives ordinary correctability. -/
theorem generatedHolonomy_correctable_of_robust
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    {State : Type s} {Param : Type q}
    (C : CorrectionRealization State Param
      ((freePathEvaluator W R D).map p ≅
        (freePathEvaluator W R D).map p))
    {Margin : Type m} [Preorder Margin]
    (RC : RobustCorrectionData C Margin)
    (mu : Margin)
    (x : State)
    (gamma : GeneratedLocalizationLoop W p)
    (h :
      GeneratedHolonomyRobustlyCorrectable
        W R D C RC mu x gamma) :
    GeneratedHolonomyCorrectable W R D C x gamma :=
  RC.correctableAt h

/-- Nontrivial generated holonomy is non-flat under an explicit filtration
separated at the reflexive automorphism. This is a flatness statement only. -/
theorem generatedHolonomy_not_flat_of_ne_of_separatedAt
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    (F : ObstructionFiltration
      ((freePathEvaluator W R D).map p ≅
        (freePathEvaluator W R D).map p))
    (gamma : GeneratedLocalizationLoop W p)
    (hsep : F.SeparatedAt (Iso.refl _))
    (hne : generatedHolonomy W R D gamma ≠ Iso.refl _) :
    ¬ FilteredGeneratedHolonomyFlat W R D F gamma := by
  exact F.not_flat_of_ne_of_separatedAt hsep hne

/-- Explicit uncorrectability packages as a hard generated-holonomy
obstruction. No nontriviality or non-flatness premise supplies this evidence. -/
theorem generatedHolonomy_hard_of_uncorrectable
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    {State : Type s} {Param : Type q}
    (C : CorrectionRealization State Param
      ((freePathEvaluator W R D).map p ≅
        (freePathEvaluator W R D).map p))
    (x : State)
    (gamma : GeneratedLocalizationLoop W p)
    (h : ¬ GeneratedHolonomyCorrectable W R D C x gamma) :
    GeneratedHolonomyHardObstruction W R D C x gamma :=
  h

end KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80
