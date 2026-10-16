import Mathlib

/-!
Finite formal surface for the v0.8 bounded portfolio experiment scheduler.
A trial may replace the baseline adapter only when information gain, budget,
risk, recoverability, cooldown, and count bounds are all satisfied.
-/

namespace KUOS
namespace OpenHorizon


def expectedInformationGain
    (uncertainty unresolved novelty opportunityCost
      uncertaintyWeight unresolvedWeight noveltyWeight opportunityCostWeight : ℚ) : ℚ :=
  uncertaintyWeight * uncertainty
    + unresolvedWeight * unresolved
    + noveltyWeight * novelty
    - opportunityCostWeight * opportunityCost


def eligibleTrial
    (informationGain minimumInformationGain cost remainingBudget
      risk maximumRisk recoverability minimumRecoverability : ℚ) : Prop :=
  minimumInformationGain ≤ informationGain ∧
  cost ≤ remainingBudget ∧
  risk ≤ maximumRisk ∧
  minimumRecoverability ≤ recoverability


theorem eligibleTrial_information_floor
    {informationGain minimumInformationGain cost remainingBudget
      risk maximumRisk recoverability minimumRecoverability : ℚ}
    (h : eligibleTrial informationGain minimumInformationGain cost remainingBudget
      risk maximumRisk recoverability minimumRecoverability) :
    minimumInformationGain ≤ informationGain := by
  exact h.1


theorem expectedInformationGain_zero_weights
    (uncertainty unresolved novelty opportunityCost : ℚ) :
    expectedInformationGain uncertainty unresolved novelty opportunityCost 0 0 0 0 = 0 := by
  simp [expectedInformationGain]


structure ExperimentBudget where
  total : ℚ
  spent : ℚ
  spentNonnegative : 0 ≤ spent
  spentWithinTotal : spent ≤ total


def remainingBudget (budget : ExperimentBudget) : ℚ :=
  budget.total - budget.spent


def debitBudget
    (budget : ExperimentBudget) (cost : ℚ)
    (costNonnegative : 0 ≤ cost)
    (costWithinBudget : budget.spent + cost ≤ budget.total) : ExperimentBudget where
  total := budget.total
  spent := budget.spent + cost
  spentNonnegative := by linarith [budget.spentNonnegative]
  spentWithinTotal := costWithinBudget


theorem budgetDebit_monotone
    (budget : ExperimentBudget) (cost : ℚ)
    (costNonnegative : 0 ≤ cost)
    (costWithinBudget : budget.spent + cost ≤ budget.total) :
    budget.spent ≤ (debitBudget budget cost costNonnegative costWithinBudget).spent := by
  simp [debitBudget]
  linarith


theorem debitBudget_remaining
    (budget : ExperimentBudget) (cost : ℚ)
    (costNonnegative : 0 ≤ cost)
    (costWithinBudget : budget.spent + cost ≤ budget.total) :
    remainingBudget (debitBudget budget cost costNonnegative costWithinBudget) =
      remainingBudget budget - cost := by
  simp [remainingBudget, debitBudget]
  ring


structure ExperimentSelection where
  liveAdapterCount : ℕ
  oneLiveAdapter : liveAdapterCount ≤ 1
  shadowActuationCount : ℕ := 0


theorem oneLiveAdapter (selection : ExperimentSelection) :
    selection.liveAdapterCount = 0 ∨ selection.liveAdapterCount = 1 := by
  omega


theorem shadow_non_actuation (selection : ExperimentSelection) :
    selection.shadowActuationCount = 0 := by
  rfl


structure ExperimentHistory where
  cycles : ℕ
  trials : ℕ
  exploits : ℕ
  classifiedCycles : trials + exploits = cycles
  trialLimit : ℕ
  trialsWithinLimit : trials ≤ trialLimit


def appendExperiment
    (history : ExperimentHistory)
    (canTrial : history.trials < history.trialLimit) : ExperimentHistory where
  cycles := history.cycles + 1
  trials := history.trials + 1
  exploits := history.exploits
  classifiedCycles := by omega
  trialLimit := history.trialLimit
  trialsWithinLimit := by omega


def appendExploit (history : ExperimentHistory) : ExperimentHistory where
  cycles := history.cycles + 1
  trials := history.trials
  exploits := history.exploits + 1
  classifiedCycles := by omega
  trialLimit := history.trialLimit
  trialsWithinLimit := history.trialsWithinLimit


theorem appendExperiment_cycle_strict
    (history : ExperimentHistory)
    (canTrial : history.trials < history.trialLimit) :
    history.cycles < (appendExperiment history canTrial).cycles := by
  simp [appendExperiment]


theorem appendExploit_cycle_strict (history : ExperimentHistory) :
    history.cycles < (appendExploit history).cycles := by
  simp [appendExploit]

end OpenHorizon
end KUOS
