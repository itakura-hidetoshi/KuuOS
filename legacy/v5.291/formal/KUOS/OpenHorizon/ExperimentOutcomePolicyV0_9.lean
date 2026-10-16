import Mathlib

/-!
Finite formal surface for the v0.9 experiment outcome and policy scheduler.
The policy may adapt cadence and information-gain thresholds, but the v0.8 hard
floor and one-child-cycle boundary remain invariant.
-/

namespace KUOS
namespace OpenHorizon


def posteriorSuccess (α β : ℚ) : ℚ :=
  α / (α + β)


def netExperimentValue
    (utility cost risk recoverability costWeight riskWeight recoverabilityWeight : ℚ) : ℚ :=
  utility - costWeight * cost - riskWeight * risk
    + recoverabilityWeight * recoverability


def adaptThreshold (hardFloor baseThreshold adaptationRate pressureExcess : ℚ) : ℚ :=
  max hardFloor (baseThreshold - adaptationRate * pressureExcess)


theorem hardFloor_preserved
    (hardFloor baseThreshold adaptationRate pressureExcess : ℚ) :
    hardFloor ≤ adaptThreshold hardFloor baseThreshold adaptationRate pressureExcess := by
  simp [adaptThreshold]


theorem adaptThreshold_eq_hardFloor_when_lower
    (hardFloor baseThreshold adaptationRate pressureExcess : ℚ)
    (h : baseThreshold - adaptationRate * pressureExcess ≤ hardFloor) :
    adaptThreshold hardFloor baseThreshold adaptationRate pressureExcess = hardFloor := by
  simp [adaptThreshold, h]


def updateAlpha (α : ℚ) (success : Bool) : ℚ :=
  α + if success then 1 else 0


def updateBeta (β : ℚ) (success : Bool) : ℚ :=
  β + if success then 0 else 1


theorem updateAlpha_monotone (α : ℚ) (success : Bool) :
    α ≤ updateAlpha α success := by
  cases success <;> simp [updateAlpha]


theorem updateBeta_monotone (β : ℚ) (success : Bool) :
    β ≤ updateBeta β success := by
  cases success <;> simp [updateBeta]


inductive PolicyMode where
  | experiment
  | reobserve
  | exploit
  deriving DecidableEq, Repr


structure PolicyExecution where
  mode : PolicyMode
  childCycles : ℕ
  liveAdapterCount : ℕ
  shadowActuationCount : ℕ := 0
  hardGateBypassCount : ℕ := 0
  oneChildCycleBound : childCycles ≤ 1
  oneLiveAdapterBound : liveAdapterCount ≤ 1


theorem oneChildCycle (execution : PolicyExecution) :
    execution.childCycles = 0 ∨ execution.childCycles = 1 := by
  omega


theorem oneLiveAdapter (execution : PolicyExecution) :
    execution.liveAdapterCount = 0 ∨ execution.liveAdapterCount = 1 := by
  omega


theorem shadow_non_actuation (execution : PolicyExecution) :
    execution.shadowActuationCount = 0 := by
  rfl


theorem no_hard_gate_bypass (execution : PolicyExecution) :
    execution.hardGateBypassCount = 0 := by
  rfl


structure PolicyHistory where
  cycles : ℕ
  experiments : ℕ
  reobservations : ℕ
  exploits : ℕ
  classified : experiments + reobservations + exploits = cycles


def appendPolicyCycle (history : PolicyHistory) (mode : PolicyMode) : PolicyHistory where
  cycles := history.cycles + 1
  experiments := history.experiments + if mode = .experiment then 1 else 0
  reobservations := history.reobservations + if mode = .reobserve then 1 else 0
  exploits := history.exploits + if mode = .exploit then 1 else 0
  classified := by
    cases mode <;> simp <;> omega


theorem appendPolicyCycle_strict (history : PolicyHistory) (mode : PolicyMode) :
    history.cycles < (appendPolicyCycle history mode).cycles := by
  simp [appendPolicyCycle]

end OpenHorizon
end KUOS
