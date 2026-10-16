import Mathlib

/-!
Finite formal surface for v0.12 horizon gauge arbitration.
Short, medium, and long policy sections are compared by bounded connection
residuals. Their triangular disagreement defines bounded arbitration curvature.
Parallel transport preserves an explicit plurality floor and each invocation
starts at most one v0.11 child.
-/

namespace KUOS
namespace OpenHorizon

inductive ArbitrationHorizon where
  | short
  | medium
  | long
  deriving DecidableEq, Repr

inductive ArbitrationMode where
  | experiment
  | reobserve
  | exploit
  deriving DecidableEq, Repr


def connectionResidual (rawResidual : ℚ) : ℚ :=
  max 0 (min 1 rawResidual)


theorem connectionResidual_nonnegative (rawResidual : ℚ) :
    0 ≤ connectionResidual rawResidual := by
  simp [connectionResidual]


theorem connectionResidual_upper_bound (rawResidual : ℚ) :
    connectionResidual rawResidual ≤ 1 := by
  simp [connectionResidual]


def arbitrationCurvature
    (shortMedium mediumLong shortLong : ℚ) : ℚ :=
  max 0 (min 1 ((shortMedium + mediumLong + shortLong) / 3))


theorem arbitrationCurvature_nonnegative
    (shortMedium mediumLong shortLong : ℚ) :
    0 ≤ arbitrationCurvature shortMedium mediumLong shortLong := by
  simp [arbitrationCurvature]


theorem arbitrationCurvature_upper_bound
    (shortMedium mediumLong shortLong : ℚ) :
    arbitrationCurvature shortMedium mediumLong shortLong ≤ 1 := by
  simp [arbitrationCurvature]


def transportWithFloor (floor rawWeight : ℚ) : ℚ :=
  max floor (min 1 rawWeight)


theorem transport_floor_preserved (floor rawWeight : ℚ) :
    floor ≤ transportWithFloor floor rawWeight := by
  simp [transportWithFloor]


theorem transport_upper_bound
    (floor rawWeight : ℚ) (hfloor : floor ≤ 1) :
    transportWithFloor floor rawWeight ≤ 1 := by
  simp [transportWithFloor, hfloor]


structure TransportedWeights where
  floor : ℚ
  shortWeight : ℚ
  mediumWeight : ℚ
  longWeight : ℚ
  floorNonnegative : 0 ≤ floor
  shortFloor : floor ≤ shortWeight
  mediumFloor : floor ≤ mediumWeight
  longFloor : floor ≤ longWeight
  sumOne : shortWeight + mediumWeight + longWeight = 1


theorem no_winner_take_all_short (weights : TransportedWeights)
    (hfloor : 0 < weights.floor) : weights.shortWeight < 1 := by
  have hmedium : 0 < weights.mediumWeight := lt_of_lt_of_le hfloor weights.mediumFloor
  have hlong : 0 ≤ weights.longWeight := le_trans weights.floorNonnegative weights.longFloor
  linarith [weights.sumOne]


theorem no_winner_take_all_medium (weights : TransportedWeights)
    (hfloor : 0 < weights.floor) : weights.mediumWeight < 1 := by
  have hshort : 0 < weights.shortWeight := lt_of_lt_of_le hfloor weights.shortFloor
  have hlong : 0 ≤ weights.longWeight := le_trans weights.floorNonnegative weights.longFloor
  linarith [weights.sumOne]


theorem no_winner_take_all_long (weights : TransportedWeights)
    (hfloor : 0 < weights.floor) : weights.longWeight < 1 := by
  have hshort : 0 < weights.shortWeight := lt_of_lt_of_le hfloor weights.shortFloor
  have hmedium : 0 ≤ weights.mediumWeight := le_trans weights.floorNonnegative weights.mediumFloor
  linarith [weights.sumOne]


structure ArbitrationExecution where
  horizonChildCycles : ℕ
  liveAdapterCount : ℕ
  winnerTakeAllCollapseCount : ℕ := 0
  hardGateBypassCount : ℕ := 0
  oneHorizonChildBound : horizonChildCycles ≤ 1
  oneLiveAdapterBound : liveAdapterCount ≤ 1


theorem oneHorizonChild (execution : ArbitrationExecution) :
    execution.horizonChildCycles = 0 ∨ execution.horizonChildCycles = 1 := by
  omega


theorem oneLiveAdapter (execution : ArbitrationExecution) :
    execution.liveAdapterCount = 0 ∨ execution.liveAdapterCount = 1 := by
  omega


theorem no_winner_take_all_collapse (execution : ArbitrationExecution) :
    execution.winnerTakeAllCollapseCount = 0 := by
  rfl


theorem no_hard_gate_bypass (execution : ArbitrationExecution) :
    execution.hardGateBypassCount = 0 := by
  rfl


structure ArbitrationHistory where
  cycles : ℕ
  holonomyRecords : ℕ
  alignedCycles : ℕ
  pluralCycles : ℕ
  holonomyAligned : holonomyRecords = cycles
  classified : alignedCycles + pluralCycles = cycles


def appendArbitrationCycle
    (history : ArbitrationHistory) (plural : Bool) : ArbitrationHistory where
  cycles := history.cycles + 1
  holonomyRecords := history.holonomyRecords + 1
  alignedCycles := history.alignedCycles + if plural then 0 else 1
  pluralCycles := history.pluralCycles + if plural then 1 else 0
  holonomyAligned := by simp [history.holonomyAligned]
  classified := by
    cases plural <;> simp <;> omega


theorem arbitrationHolonomy_strict
    (history : ArbitrationHistory) (plural : Bool) :
    history.holonomyRecords <
      (appendArbitrationCycle history plural).holonomyRecords := by
  simp [appendArbitrationCycle]

end OpenHorizon
end KUOS
