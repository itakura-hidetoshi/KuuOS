import Mathlib
import KUOS.PlanOS.NextCycleSessionBootstrapV0_15

namespace KUOS.PlanOS

inductive LeaseMonitorRoute where
  | continue
  | revalidate
  | renewOrEscalate
  | rerotateRequired
  deriving DecidableEq

structure LeaseMonitorRoot where
  nextTick : Nat
  sessionActive : Bool

structure LeaseMonitorResult where
  tickIndex : Nat
  hasAnomaly : Bool
  suspended : Bool
  planProgressAllowed : Bool
  terminal : Bool
  route : LeaseMonitorRoute
  executionGranted : Bool
  hostAccessGranted : Bool
  memoryOverwrite : Bool


def leaseMonitorAdmissible
    (root : LeaseMonitorRoot)
    (result : LeaseMonitorResult) : Prop :=
  root.sessionActive = true ∧
  result.tickIndex = root.nextTick ∧
  ((result.hasAnomaly = false ∧
      result.suspended = false ∧
      result.planProgressAllowed = true ∧
      result.terminal = false ∧
      result.route = LeaseMonitorRoute.continue) ∨
    (result.hasAnomaly = true ∧
      result.suspended = true ∧
      result.planProgressAllowed = false ∧
      result.terminal = true ∧
      result.route ≠ LeaseMonitorRoute.continue)) ∧
  result.executionGranted = false ∧
  result.hostAccessGranted = false ∧
  result.memoryOverwrite = false


theorem admissible_monitor_requires_active_session
    (root : LeaseMonitorRoot)
    (result : LeaseMonitorResult)
    (h : leaseMonitorAdmissible root result) :
    root.sessionActive = true := by
  exact h.1


theorem admissible_monitor_uses_next_tick
    (root : LeaseMonitorRoot)
    (result : LeaseMonitorResult)
    (h : leaseMonitorAdmissible root result) :
    result.tickIndex = root.nextTick := by
  exact h.2.1


theorem healthy_monitor_allows_plan_progress
    (root : LeaseMonitorRoot)
    (result : LeaseMonitorResult)
    (h : leaseMonitorAdmissible root result)
    (healthy : result.hasAnomaly = false) :
    result.suspended = false ∧
    result.planProgressAllowed = true ∧
    result.terminal = false ∧
    result.route = LeaseMonitorRoute.continue := by
  rcases h.2.2.1 with hHealthy | hSuspended
  · exact ⟨hHealthy.2.1, hHealthy.2.2.1, hHealthy.2.2.2.1, hHealthy.2.2.2.2⟩
  · simp_all


theorem anomalous_monitor_suspends_session
    (root : LeaseMonitorRoot)
    (result : LeaseMonitorResult)
    (h : leaseMonitorAdmissible root result)
    (anomalous : result.hasAnomaly = true) :
    result.suspended = true ∧
    result.planProgressAllowed = false ∧
    result.terminal = true ∧
    result.route ≠ LeaseMonitorRoute.continue := by
  rcases h.2.2.1 with hHealthy | hSuspended
  · simp_all
  · exact ⟨hSuspended.2.1, hSuspended.2.2.1,
      hSuspended.2.2.2.1, hSuspended.2.2.2.2⟩


theorem suspended_monitor_blocks_plan_progress
    (root : LeaseMonitorRoot)
    (result : LeaseMonitorResult)
    (h : leaseMonitorAdmissible root result)
    (suspended : result.suspended = true) :
    result.planProgressAllowed = false := by
  rcases h.2.2.1 with hHealthy | hSuspended
  · simp_all
  · exact hSuspended.2.2.1


theorem lease_monitor_grants_no_authority
    (root : LeaseMonitorRoot)
    (result : LeaseMonitorResult)
    (h : leaseMonitorAdmissible root result) :
    result.executionGranted = false ∧
    result.hostAccessGranted = false ∧
    result.memoryOverwrite = false := by
  exact h.2.2.2

end KUOS.PlanOS
