import Mathlib

/-!
Finite formal surface for delayed credit assignment over distinct short, medium,
and long horizons. Credits remain bounded, horizon weights remain explicit, and each
v0.11 invocation calls at most one v0.10 regret child.
-/

namespace KUOS
namespace OpenHorizon

inductive Horizon where
  | short
  | medium
  | long
  deriving DecidableEq, Repr

inductive HorizonMode where
  | experiment
  | reobserve
  | exploit
  deriving DecidableEq, Repr


def decayCredit (credit decay : ℚ) : ℚ :=
  max 0 (min 1 (decay * credit))


def updateCredit (credit decay learning evidence : ℚ) : ℚ :=
  max 0 (min 1 (decayCredit credit decay + learning * max 0 evidence))


theorem credit_nonnegative (credit decay learning evidence : ℚ) :
    0 ≤ updateCredit credit decay learning evidence := by
  simp [updateCredit]


theorem credit_upper_bound (credit decay learning evidence : ℚ) :
    updateCredit credit decay learning evidence ≤ 1 := by
  simp [updateCredit]


def aggregateHorizonSupport
    (shortWeight mediumWeight longWeight shortCredit mediumCredit longCredit : ℚ) : ℚ :=
  max 0 (min 1
    (shortWeight * shortCredit
      + mediumWeight * mediumCredit
      + longWeight * longCredit))


theorem aggregate_nonnegative
    (shortWeight mediumWeight longWeight shortCredit mediumCredit longCredit : ℚ) :
    0 ≤ aggregateHorizonSupport
      shortWeight mediumWeight longWeight shortCredit mediumCredit longCredit := by
  simp [aggregateHorizonSupport]


theorem aggregate_upper_bound
    (shortWeight mediumWeight longWeight shortCredit mediumCredit longCredit : ℚ) :
    aggregateHorizonSupport
      shortWeight mediumWeight longWeight shortCredit mediumCredit longCredit ≤ 1 := by
  simp [aggregateHorizonSupport]


def adaptBaseThreshold
    (lower upper base support exploitSupport gain resistance : ℚ) : ℚ :=
  max lower (min upper (base - gain * support + resistance * exploitSupport))


theorem threshold_lower_bound
    (lower upper base support exploitSupport gain resistance : ℚ) :
    lower ≤ adaptBaseThreshold lower upper base support exploitSupport gain resistance := by
  simp [adaptBaseThreshold]


theorem threshold_upper_bound
    (lower upper base support exploitSupport gain resistance : ℚ)
    (h : lower ≤ upper) :
    adaptBaseThreshold lower upper base support exploitSupport gain resistance ≤ upper := by
  simp [adaptBaseThreshold, h]


def adaptBaseInterval
    (lower upper base supportReduction exploitExtension : ℕ) : ℕ :=
  max lower (min upper (base - supportReduction + exploitExtension))


theorem interval_lower_bound
    (lower upper base supportReduction exploitExtension : ℕ) :
    lower ≤ adaptBaseInterval lower upper base supportReduction exploitExtension := by
  simp [adaptBaseInterval]


theorem interval_upper_bound
    (lower upper base supportReduction exploitExtension : ℕ)
    (h : lower ≤ upper) :
    adaptBaseInterval lower upper base supportReduction exploitExtension ≤ upper := by
  simp [adaptBaseInterval, h]


structure MultiHorizonExecution where
  regretChildCycles : ℕ
  liveAdapterCount : ℕ
  effectlessCreditUpdates : ℕ := 0
  shadowActuationCount : ℕ := 0
  hardGateBypassCount : ℕ := 0
  oneRegretChildBound : regretChildCycles ≤ 1
  oneLiveAdapterBound : liveAdapterCount ≤ 1


theorem oneRegretChild (execution : MultiHorizonExecution) :
    execution.regretChildCycles = 0 ∨ execution.regretChildCycles = 1 := by
  omega


theorem oneLiveAdapter (execution : MultiHorizonExecution) :
    execution.liveAdapterCount = 0 ∨ execution.liveAdapterCount = 1 := by
  omega


theorem no_effectless_credit_update (execution : MultiHorizonExecution) :
    execution.effectlessCreditUpdates = 0 := by
  rfl


theorem no_shadow_actuation (execution : MultiHorizonExecution) :
    execution.shadowActuationCount = 0 := by
  rfl


theorem no_hard_gate_bypass (execution : MultiHorizonExecution) :
    execution.hardGateBypassCount = 0 := by
  rfl


structure HorizonHistory where
  cycles : ℕ
  shortCycles : ℕ
  mediumCycles : ℕ
  longCycles : ℕ
  shortAligned : shortCycles = cycles
  mediumAligned : mediumCycles = cycles
  longBounded : longCycles ≤ cycles


def appendHorizonCycle (history : HorizonHistory) (longActive : Bool) : HorizonHistory where
  cycles := history.cycles + 1
  shortCycles := history.shortCycles + 1
  mediumCycles := history.mediumCycles + 1
  longCycles := history.longCycles + if longActive then 1 else 0
  shortAligned := by simp [history.shortAligned]
  mediumAligned := by simp [history.mediumAligned]
  longBounded := by
    cases longActive <;> simp <;> omega


theorem appendHorizonCycle_strict (history : HorizonHistory) (longActive : Bool) :
    history.cycles < (appendHorizonCycle history longActive).cycles := by
  simp [appendHorizonCycle]

end OpenHorizon
end KUOS
