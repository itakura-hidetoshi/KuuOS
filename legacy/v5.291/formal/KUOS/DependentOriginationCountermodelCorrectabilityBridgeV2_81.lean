import KUOS.DependentOriginationGeneratedHolonomyCountermodelEvaluationV2_69
import KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80

namespace KUOS.DependentOriginationCountermodelCorrectabilityBridgeV2_81

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredGeneratedHolonomyV2_73
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69

universe s q m

/-!
# Concrete countermodel correctability bridge v2.81

The octahedral v2.69 truth test supplies a concrete generated loop whose
holonomy is nontrivial. The v2.80 layer distinguishes non-flatness from
uncorrectability.

This bridge makes that distinction explicit on the concrete countermodel:

* nontrivial holonomy plus separatedness gives non-flatness;
* a robust correction witness may coexist with that non-flatness;
* hard obstruction additionally requires an explicit uncorrectability witness.

No theorem in this file derives uncorrectability from nontriviality or
non-flatness.
-/

/-- The automorphism carrier of the distinguished octahedral generated loop. -/
abbrev CounterHolonomyCarrier
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :=
  ((freePathEvaluator allMorphisms counterSystem D).map
      (rawPath a00 ≫ rawPath b00) ≅
   (freePathEvaluator allMorphisms counterSystem D).map
      (rawPath a00 ≫ rawPath b00))

/-- The concrete v2.69 nontrivial generated loop is non-flat under every
filtration separated at the reflexive automorphism. -/
theorem counterGeneratedLoop_not_flat_of_separated
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    (F : ObstructionFiltration (CounterHolonomyCarrier D))
    (hsep : F.SeparatedAt (Iso.refl _)) :
    ¬ FilteredGeneratedHolonomyFlat
      allMorphisms counterSystem D F counterGeneratedLoop := by
  exact generatedHolonomy_not_flat_of_ne_of_separatedAt
    allMorphisms counterSystem D F counterGeneratedLoop hsep
    (counterGeneratedLoop_holonomy_ne_refl D)

/-- The canonical pointwise datum selected from weak admissibility inherits the
same concrete non-flatness conclusion under separatedness. -/
theorem counterCanonicalGeneratedLoop_not_flat_of_separated
    (F : ObstructionFiltration (CounterHolonomyCarrier counterD))
    (hsep : F.SeparatedAt (Iso.refl _)) :
    ¬ FilteredGeneratedHolonomyFlat
      allMorphisms counterSystem counterD F counterGeneratedLoop :=
  counterGeneratedLoop_not_flat_of_separated counterD F hsep

/-- A robust correction witness may coexist with the concrete countermodel's
non-flat holonomy. This theorem deliberately demonstrates that non-flatness
does not imply uncorrectability. -/
theorem counterGeneratedLoop_correctable_and_not_flat_of_robust_separated
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    (F : ObstructionFiltration (CounterHolonomyCarrier D))
    (hsep : F.SeparatedAt (Iso.refl _))
    {State : Type s} {Param : Type q}
    (C : CorrectionRealization State Param (CounterHolonomyCarrier D))
    {Margin : Type m} [Preorder Margin]
    (RC : RobustCorrectionData C Margin)
    (mu : Margin)
    (x : State)
    (hrob :
      GeneratedHolonomyRobustlyCorrectable
        allMorphisms counterSystem D C RC mu x counterGeneratedLoop) :
    GeneratedHolonomyCorrectable
        allMorphisms counterSystem D C x counterGeneratedLoop ∧
      ¬ FilteredGeneratedHolonomyFlat
        allMorphisms counterSystem D F counterGeneratedLoop := by
  constructor
  · exact generatedHolonomy_correctable_of_robust
      allMorphisms counterSystem D C RC mu x counterGeneratedLoop hrob
  · exact counterGeneratedLoop_not_flat_of_separated D F hsep

/-- The same concrete loop becomes a hard obstruction only after an independent
uncorrectability witness is supplied. -/
theorem counterGeneratedLoop_hard_and_not_flat_of_separated_uncorrectable
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    (F : ObstructionFiltration (CounterHolonomyCarrier D))
    (hsep : F.SeparatedAt (Iso.refl _))
    {State : Type s} {Param : Type q}
    (C : CorrectionRealization State Param (CounterHolonomyCarrier D))
    (x : State)
    (huncorrectable :
      ¬ GeneratedHolonomyCorrectable
        allMorphisms counterSystem D C x counterGeneratedLoop) :
    GeneratedHolonomyHardObstruction
        allMorphisms counterSystem D C x counterGeneratedLoop ∧
      ¬ FilteredGeneratedHolonomyFlat
        allMorphisms counterSystem D F counterGeneratedLoop := by
  constructor
  · exact generatedHolonomy_hard_of_uncorrectable
      allMorphisms counterSystem D C x counterGeneratedLoop huncorrectable
  · exact counterGeneratedLoop_not_flat_of_separated D F hsep

end KUOS.DependentOriginationCountermodelCorrectabilityBridgeV2_81
