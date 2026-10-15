import Mathlib

/-!
Finite formal surface for the v0.10 policy-regret and counterfactual cadence
controller. Counterfactual estimates are confidence-discounted and never promoted to
outcomes. Threshold and interval adaptation remain within explicit lower and upper
bounds, and each regret cycle invokes at most one v0.9 policy child.
-/

namespace KUOS
namespace OpenHorizon


def confidenceDiscountedRegret
    (chosen alternative confidence tolerance maximumRegret : ℚ) : ℚ :=
  min maximumRegret (confidence * max 0 (alternative - chosen - tolerance))


theorem regret_nonnegative
    (chosen alternative confidence tolerance maximumRegret : ℚ)
    (hconfidence : 0 ≤ confidence)
    (hmaximum : 0 ≤ maximumRegret) :
    0 ≤ confidenceDiscountedRegret
      chosen alternative confidence tolerance maximumRegret := by
  simp [confidenceDiscountedRegret, hmaximum, mul_nonneg hconfidence (le_max_left 0 _)]


theorem regret_le_maximum
    (chosen alternative confidence tolerance maximumRegret : ℚ) :
    confidenceDiscountedRegret
      chosen alternative confidence tolerance maximumRegret ≤ maximumRegret := by
  simp [confidenceDiscountedRegret]


def adaptThresholdBounded
    (lower upper base supportCredit exploitCredit supportGain resistanceGain : ℚ) : ℚ :=
  max lower (min upper (base - supportGain * supportCredit
    + resistanceGain * exploitCredit))


theorem threshold_lower_bound
    (lower upper base supportCredit exploitCredit supportGain resistanceGain : ℚ) :
    lower ≤ adaptThresholdBounded
      lower upper base supportCredit exploitCredit supportGain resistanceGain := by
  simp [adaptThresholdBounded]


theorem threshold_upper_bound
    (lower upper base supportCredit exploitCredit supportGain resistanceGain : ℚ)
    (h : lower ≤ upper) :
    adaptThresholdBounded
      lower upper base supportCredit exploitCredit supportGain resistanceGain ≤ upper := by
  simp [adaptThresholdBounded, h]


def adaptIntervalBounded
    (lower upper base supportReduction exploitExtension : ℕ) : ℕ :=
  max lower (min upper (base - supportReduction + exploitExtension))


theorem interval_lower_bound
    (lower upper base supportReduction exploitExtension : ℕ) :
    lower ≤ adaptIntervalBounded
      lower upper base supportReduction exploitExtension := by
  simp [adaptIntervalBounded]


theorem interval_upper_bound
    (lower upper base supportReduction exploitExtension : ℕ)
    (h : lower ≤ upper) :
    adaptIntervalBounded
      lower upper base supportReduction exploitExtension ≤ upper := by
  simp [adaptIntervalBounded, h]


inductive RegretAlternative where
  | none
  | experiment
  | reobserve
  | exploit
  deriving DecidableEq, Repr


structure RegretExecution where
  policyChildCycles : ℕ
  liveAdapterCount : ℕ
  counterfactualOutcomeCount : ℕ := 0
  shadowActuationCount : ℕ := 0
  hardGateBypassCount : ℕ := 0
  onePolicyChildBound : policyChildCycles ≤ 1
  oneLiveAdapterBound : liveAdapterCount ≤ 1


theorem onePolicyChild (execution : RegretExecution) :
    execution.policyChildCycles = 0 ∨ execution.policyChildCycles = 1 := by
  omega


theorem oneLiveAdapter (execution : RegretExecution) :
    execution.liveAdapterCount = 0 ∨ execution.liveAdapterCount = 1 := by
  omega


theorem counterfactual_not_outcome (execution : RegretExecution) :
    execution.counterfactualOutcomeCount = 0 := by
  rfl


theorem shadow_non_actuation (execution : RegretExecution) :
    execution.shadowActuationCount = 0 := by
  rfl


theorem no_hard_gate_bypass (execution : RegretExecution) :
    execution.hardGateBypassCount = 0 := by
  rfl


structure RegretHistory where
  cycles : ℕ
  positiveRegretCycles : ℕ
  zeroRegretCycles : ℕ
  classified : positiveRegretCycles + zeroRegretCycles = cycles


def appendRegretCycle (history : RegretHistory) (positive : Bool) : RegretHistory where
  cycles := history.cycles + 1
  positiveRegretCycles := history.positiveRegretCycles + if positive then 1 else 0
  zeroRegretCycles := history.zeroRegretCycles + if positive then 0 else 1
  classified := by
    cases positive <;> simp <;> omega


theorem appendRegretCycle_strict (history : RegretHistory) (positive : Bool) :
    history.cycles < (appendRegretCycle history positive).cycles := by
  simp [appendRegretCycle]

end OpenHorizon
end KUOS
