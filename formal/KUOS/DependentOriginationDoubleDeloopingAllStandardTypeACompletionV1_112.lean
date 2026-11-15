import KUOS.DependentOriginationDoubleDeloopingTypeAFourCocycleCompletionV1_111

namespace KUOS.DependentOriginationDoubleDeloopingAllStandardTypeACompletionV1_112

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100
open KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101
open KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102
open KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105
open KUOS.DependentOriginationDoubleDeloopingTypeAFourCocycleCompletionV1_111

set_option maxHeartbeats 2000000

/-!
All concrete standard type-(A) horn lifts into the additive double delooping:
n = 2 from v1.102; n = 3 from v1.102; n = 4 from v1.111;
n >= 5 from v1.103. This does not assert scaled type-(C) RLP,
forward endpoint RLP, global fibrancy, or an unverified descent to main.
-/

/-- Every actual scaled type-(A) inner horn has an explicit arithmetic
cocycle completion, by its proven geometric dimension case. -/
theorem natDoubleDelooping_allStandardTypeA_completions :
    HasAllStandardTypeAHornCocycleCompletions := by
  intro g f
  cases g with
  | mk n i hi0 hiLast =>
    have hleft : 0 < i.val := (Fin.lt_def).mp hi0
    have hright : i.val < n := by simpa using (Fin.lt_def).mp hiLast
    by_cases hn2 : n = 2
    · subst n
      fin_cases i <;> simp_all
      exact natTypeATwo_zero_cocycle_completion f
    · by_cases hn3 : n = 3
      · subst n
        fin_cases i <;> simp_all
        · exact natTypeAThreeI1_cocycle_completion f
        · exact natTypeAThreeI2_cocycle_completion f
      · by_cases hn4 : n = 4
        · subst n
          exact natTypeAFourCocycleCompletion_nonempty i hi0 hiLast f
        · have hn5 : 5 ≤ n := by omega
          exact natTypeAHigh_cocycle_completion ⟨n, i, hi0, hiLast⟩ hn5 f

/-- Concrete additive double delooping has RLP against every literal
standard type-(A) scaled horn inclusion, not just four-dimensional ones. -/
theorem natDoubleDelooping_allStandardTypeA_rlp :
    (standardTypeAScaledHornGenerators : MorphismProperty ScaledSSet).rlp
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  exact natDoubleDelooping_standardTypeA_rlp_of_cocycleCompletions
    natDoubleDelooping_allStandardTypeA_completions

end KUOS.DependentOriginationDoubleDeloopingAllStandardTypeACompletionV1_112
