import KUOS.DependentOriginationCountermodelCorrectabilityBridgeV2_81

namespace KUOS.DependentOriginationCountermodelCorrectabilityBridgeV2_81

open CategoryTheory
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredGeneratedHolonomyV2_73
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69

example
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    (F : ObstructionFiltration (CounterHolonomyCarrier D))
    (hsep : F.SeparatedAt (Iso.refl _)) :
    ¬ FilteredGeneratedHolonomyFlat
      allMorphisms counterSystem D F counterGeneratedLoop :=
  counterGeneratedLoop_not_flat_of_separated D F hsep

end KUOS.DependentOriginationCountermodelCorrectabilityBridgeV2_81
