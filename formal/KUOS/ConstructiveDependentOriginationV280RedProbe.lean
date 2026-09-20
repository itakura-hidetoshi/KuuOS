import KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80

namespace KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80

open CategoryTheory
open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationFilteredGeneratedHolonomyV2_73

universe u v uH vH s q

variable {Context : Type u} [Category.{v} Context]

example
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    (F : ObstructionFiltration
      ((freePathEvaluator W R D).map p ≅
        (freePathEvaluator W R D).map p))
    (gamma : GeneratedLocalizationLoop W p)
    (hsep : F.SeparatedAt (Iso.refl _))
    (hne : generatedHolonomy W R D gamma ≠ Iso.refl _) :
    ¬ FilteredGeneratedHolonomyFlat W R D F gamma :=
  generatedHolonomy_not_flat_of_ne_of_separatedAt W R D F gamma hsep hne

example
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context))
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
  generatedHolonomy_hard_of_uncorrectable W R D C x gamma h

end KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80
