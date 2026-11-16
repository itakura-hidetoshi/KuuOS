import KUOS.DependentOriginationDoubleDeloopingTypeAFourCocycleCompletionV1_111

namespace KUOS.DependentOriginationDoubleDeloopingTypeAAllDimensionsV1_112

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101
open KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102
open KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105
open KUOS.DependentOriginationDoubleDeloopingTypeAFourCocycleCompletionV1_111

set_option maxHeartbeats 2000000

/-!
Full degree-by-degree type-(A) completion for the concrete additive B^2 Nat
scaled Duskin nerve. Degree 2: zero cocycle, degree 3: both explicit
completions, degree 4: the independently certified actual four-horn lift,
degrees >=5: the actual visible cocycle. All constructors carry the original
horn map. This is a proof only of the STANDARD type-(A) generator family,
not forward endpoint pushout-products, arbitrary fibrancy or global descent.
-/

/-- The genuine fixed 2, 3, 4 and >=5 fillers cover every admissible
standard inner type-(A) horn, with the exact source map given. -/
theorem natDoubleDelooping_typeA_every_horn_cocycle_completion :
    HasAllStandardTypeAHornCocycleCompletions := by
  intro g f
  rcases g with ⟨n, i, hi0, hiN⟩
  have hLeft : 0 < i.val := (Fin.lt_def).mp hi0
  have hRight : i.val < n := (Fin.lt_def).mp hiN
  have hMin : 2 ≤ n := by omega
  by_cases hHigh : 5 ≤ n
  · exact natTypeAHigh_cocycle_completion ⟨n, i, hi0, hiN⟩ hHigh f
  have hCases : n = 2 ∨ n = 3 ∨ n = 4 := by omega
  rcases hCases with hTwo | hThree | hFour
  · subst n
    have hIdx : i = (1 : Fin 3) := by
      fin_cases i <;> simp_all
    subst i
    exact natTypeATwo_zero_cocycle_completion f
  · subst n
    have hIdx : i = (1 : Fin 4) ∨ i = (2 : Fin 4) := by
      fin_cases i <;> simp_all
    rcases hIdx with hOne | hTwo
    · subst i
      exact natTypeAThreeI1_cocycle_completion f
    · subst i
      exact natTypeAThreeI2_cocycle_completion f
  · subst n
    exact ⟨natTypeAFourCocycleCompletion i hi0 hiN f⟩

/-- Every actual standard type-(A) horn map has an explicitly realized
scaled simplex lift whose composite equals its original horn map. -/
theorem natDoubleDelooping_typeA_every_horn_actual_lift
    (g : StandardTypeAHornGeneratorIndex)
    (f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin) :
    ∃ t : standardTypeAScaledSimplex g ⟶ natDoubleDeloopingScaledDuskin,
      standardTypeAScaledHornGeneratorHom g ≫ t = f := by
  rcases natDoubleDelooping_typeA_every_horn_cocycle_completion g f with ⟨K⟩
  exact ⟨K.toLift, K.toLift_fac⟩

/-- Every standard type-(A) generator has literal RLP against terminal B²ℕ. -/
theorem natDoubleDelooping_typeA_every_generator_rlp
    (g : StandardTypeAHornGeneratorIndex) :
    HasLiftingProperty (standardTypeAScaledHornGeneratorHom g)
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  exact natDoubleDelooping_hasLiftingProperty_standardTypeA_of_cocycleCompletions
    g (fun f => natDoubleDelooping_typeA_every_horn_cocycle_completion g f)

/-- Terminal B²ℕ lies in the right orthogonal of the COMPLETE STANDARD
type-(A) scaled inner-horn generator family, not an endpoint product family. -/
theorem natDoubleDelooping_typeA_full_standard_rlp :
    (standardTypeAScaledHornGenerators : MorphismProperty ScaledSSet).rlp
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  exact natDoubleDelooping_standardTypeA_rlp_of_cocycleCompletions
    natDoubleDelooping_typeA_every_horn_cocycle_completion

end KUOS.DependentOriginationDoubleDeloopingTypeAAllDimensionsV1_112
