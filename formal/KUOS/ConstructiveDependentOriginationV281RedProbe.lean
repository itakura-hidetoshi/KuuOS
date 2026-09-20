import KUOS.DependentOriginationCountermodelCorrectabilityBridgeV2_81

namespace KUOS.DependentOriginationCountermodelCorrectabilityBridgeV2_81

open CategoryTheory
open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredGeneratedHolonomyV2_73
open KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69

example
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    (F : ObstructionFiltration
      ((freePathEvaluator allMorphisms counterSystem D).map
          (rawPath a00 ≫ rawPath b00) ≅
       (freePathEvaluator allMorphisms counterSystem D).map
          (rawPath a00 ≫ rawPath b00)))
    (hsep : F.SeparatedAt (Iso.refl _)) :
    ¬ FilteredGeneratedHolonomyFlat
      allMorphisms counterSystem D F counterGeneratedLoop :=
  counterGeneratedLoop_not_flat_of_separated D F hsep

end KUOS.DependentOriginationCountermodelCorrectabilityBridgeV2_81
