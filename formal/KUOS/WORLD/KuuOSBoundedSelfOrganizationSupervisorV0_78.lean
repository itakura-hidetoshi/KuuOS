import Mathlib
import KUOS.WORLD.KuuOSSelfOrganizingImprovementLoopV0_78

namespace KUOS.WORLD.KuuOSBoundedSelfOrganizationSupervisorV0_78

inductive StopReason where
  | noChange
  | reobservationRollback
  | maxCycles
  deriving DecidableEq

structure Supervisor where
  cycleCount : ℕ
  maxCycles : ℕ
  stopReason : StopReason
  cycleLineageBound : Prop
  nextStateFeedsNextCycle : Prop
  stopsOnNoChange : Prop
  stopsOnRollback : Prop
  approvalInputAbsent : Prop
  executionBounded : Prop
  hostStateUnchanged : Prop

structure Supervisor.Valid (supervisor : Supervisor) : Prop where
  positiveBound : 0 < supervisor.maxCycles
  countWithinBound : supervisor.cycleCount ≤ supervisor.maxCycles
  cycleLineageBound : supervisor.cycleLineageBound
  nextStateFeedsNextCycle : supervisor.nextStateFeedsNextCycle
  stopsOnNoChange : supervisor.stopsOnNoChange
  stopsOnRollback : supervisor.stopsOnRollback
  approvalInputAbsent : supervisor.approvalInputAbsent
  executionBounded : supervisor.executionBounded
  hostStateUnchanged : supervisor.hostStateUnchanged

theorem valid_supervisor_has_finite_bound
    (supervisor : Supervisor)
    (h : supervisor.Valid) :
    0 < supervisor.maxCycles ∧
      supervisor.cycleCount ≤ supervisor.maxCycles := by
  exact ⟨h.positiveBound, h.countWithinBound⟩

theorem valid_supervisor_closes_cycle_lineage
    (supervisor : Supervisor)
    (h : supervisor.Valid) :
    supervisor.cycleLineageBound ∧
      supervisor.nextStateFeedsNextCycle ∧
      supervisor.stopsOnNoChange ∧
      supervisor.stopsOnRollback := by
  exact ⟨h.cycleLineageBound, h.nextStateFeedsNextCycle,
    h.stopsOnNoChange, h.stopsOnRollback⟩

theorem valid_supervisor_is_internal_and_bounded
    (supervisor : Supervisor)
    (h : supervisor.Valid) :
    supervisor.approvalInputAbsent ∧
      supervisor.executionBounded ∧
      supervisor.hostStateUnchanged := by
  exact ⟨h.approvalInputAbsent, h.executionBounded,
    h.hostStateUnchanged⟩

end KUOS.WORLD.KuuOSBoundedSelfOrganizationSupervisorV0_78
