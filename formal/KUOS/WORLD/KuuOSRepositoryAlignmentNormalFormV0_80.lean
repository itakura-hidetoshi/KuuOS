import Mathlib

namespace KUOS.WORLD.KuuOSRepositoryAlignmentNormalFormV0_80

structure AlignmentStep where
  sourceScore : Nat
  targetScore : Nat

structure AlignmentStep.Valid (step : AlignmentStep) : Prop where
  strictDescent : step.targetScore < step.sourceScore

structure NormalFormWitness where
  finiteStateSpace : Prop
  allStepsStrict : Prop
  allTerminalsFixed : Prop
  uniqueTerminal : Prop
  deterministicTraceMatches : Prop

structure NormalFormWitness.Valid (witness : NormalFormWitness) : Prop where
  finiteStateSpace : witness.finiteStateSpace
  allStepsStrict : witness.allStepsStrict
  allTerminalsFixed : witness.allTerminalsFixed
  uniqueTerminal : witness.uniqueTerminal
  deterministicTraceMatches : witness.deterministicTraceMatches

theorem valid_step_strictly_decreases
    (step : AlignmentStep)
    (h : step.Valid) :
    step.targetScore < step.sourceScore := by
  exact h.strictDescent

theorem strict_descent_is_not_reflexive
    (score : Nat) :
    ¬ score < score := by
  exact Nat.lt_irrefl score

theorem opposite_strict_steps_are_impossible
    {first second : Nat}
    (hForward : second < first) :
    ¬ first < second := by
  exact Nat.not_lt_of_ge (Nat.le_of_lt hForward)

theorem valid_normal_form_witness
    (witness : NormalFormWitness)
    (h : witness.Valid) :
    witness.finiteStateSpace ∧
      witness.allStepsStrict ∧
      witness.allTerminalsFixed ∧
      witness.uniqueTerminal ∧
      witness.deterministicTraceMatches := by
  exact ⟨h.finiteStateSpace, h.allStepsStrict,
    h.allTerminalsFixed, h.uniqueTerminal,
    h.deterministicTraceMatches⟩

end KUOS.WORLD.KuuOSRepositoryAlignmentNormalFormV0_80
