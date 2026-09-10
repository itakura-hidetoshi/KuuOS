import KUOS.DependentOriginationGeneratedHolonomyCountermodelLoopV2_69

namespace KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69

open CategoryTheory
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68

/-- RED test for the distinguished generated route: its evaluated 2-cell has
`zeta` as the component at the unique object of the countermodel fiber. -/
theorem counterDirectRoute_hom_app_star :
    ((generatedLocalization2CellEvaluationIso
        allMorphisms counterSystem counterD counterDirectRoute).hom.toNatTrans.app
      (SingleObj.star C2)) = zeta := by
  rfl

end KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
