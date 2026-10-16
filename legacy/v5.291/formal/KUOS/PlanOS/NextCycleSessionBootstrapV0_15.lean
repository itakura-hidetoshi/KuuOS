import Mathlib
import KUOS.PlanOS.MaterializedChainActivationV0_14

namespace KUOS.PlanOS

structure ActivationConsumptionRoot where
  owner : Nat
  epoch : Nat
  activeFromCycle : Nat
  activationReady : Bool
  materializationBound : Bool

structure PlanControlSession where
  owner : Nat
  epoch : Nat
  cycle : Nat
  planPhase : Bool
  bindPhase : Bool
  leaseMonitorStarted : Bool
  leaseDeadlineAfterStart : Bool
  eventIndex : Nat
  planVersion : Nat
  stepCount : Nat
  activationConsumed : Bool
  singleUse : Bool
  executionGranted : Bool
  hostAccessGranted : Bool
  memoryOverwrite : Bool


def sessionBootstrapAdmissible
    (root : ActivationConsumptionRoot)
    (session : PlanControlSession) : Prop :=
  root.activationReady = true ∧
  root.materializationBound = true ∧
  session.owner = root.owner ∧
  session.epoch = root.epoch ∧
  session.cycle = root.activeFromCycle ∧
  session.planPhase = true ∧
  session.bindPhase = true ∧
  session.leaseMonitorStarted = true ∧
  session.leaseDeadlineAfterStart = true ∧
  session.eventIndex = 0 ∧
  session.planVersion = 0 ∧
  session.stepCount = 0 ∧
  session.activationConsumed = true ∧
  session.singleUse = true ∧
  session.executionGranted = false ∧
  session.hostAccessGranted = false ∧
  session.memoryOverwrite = false


theorem admissible_session_requires_activation_and_materialization
    (root : ActivationConsumptionRoot)
    (session : PlanControlSession)
    (h : sessionBootstrapAdmissible root session) :
    root.activationReady = true ∧ root.materializationBound = true := by
  exact ⟨h.1, h.2.1⟩


theorem admissible_session_preserves_owner_epoch
    (root : ActivationConsumptionRoot)
    (session : PlanControlSession)
    (h : sessionBootstrapAdmissible root session) :
    session.owner = root.owner ∧ session.epoch = root.epoch := by
  rcases h with ⟨_, _, hOwner, hEpoch, _⟩
  exact ⟨hOwner, hEpoch⟩


theorem admissible_session_uses_active_cycle
    (root : ActivationConsumptionRoot)
    (session : PlanControlSession)
    (h : sessionBootstrapAdmissible root session) :
    session.cycle = root.activeFromCycle := by
  rcases h with ⟨_, _, _, _, hCycle, _⟩
  exact hCycle


theorem admissible_session_starts_plan_bind
    (root : ActivationConsumptionRoot)
    (session : PlanControlSession)
    (h : sessionBootstrapAdmissible root session) :
    session.planPhase = true ∧ session.bindPhase = true := by
  rcases h with ⟨_, _, _, _, _, hPlan, hBind, _⟩
  exact ⟨hPlan, hBind⟩


theorem admissible_session_starts_lease_monitor
    (root : ActivationConsumptionRoot)
    (session : PlanControlSession)
    (h : sessionBootstrapAdmissible root session) :
    session.leaseMonitorStarted = true ∧
    session.leaseDeadlineAfterStart = true := by
  rcases h with ⟨_, _, _, _, _, _, _, hMonitor, hDeadline, _⟩
  exact ⟨hMonitor, hDeadline⟩


theorem admissible_session_has_empty_initial_plan
    (root : ActivationConsumptionRoot)
    (session : PlanControlSession)
    (h : sessionBootstrapAdmissible root session) :
    session.eventIndex = 0 ∧
    session.planVersion = 0 ∧
    session.stepCount = 0 := by
  rcases h with ⟨_, _, _, _, _, _, _, _, _, hEvent, hVersion, hSteps, _⟩
  exact ⟨hEvent, hVersion, hSteps⟩


theorem admissible_session_consumes_activation_once
    (root : ActivationConsumptionRoot)
    (session : PlanControlSession)
    (h : sessionBootstrapAdmissible root session) :
    session.activationConsumed = true ∧ session.singleUse = true := by
  rcases h with ⟨_, _, _, _, _, _, _, _, _, _, _, _, hConsumed, hSingle, _⟩
  exact ⟨hConsumed, hSingle⟩


theorem session_bootstrap_grants_no_authority
    (root : ActivationConsumptionRoot)
    (session : PlanControlSession)
    (h : sessionBootstrapAdmissible root session) :
    session.executionGranted = false ∧
    session.hostAccessGranted = false ∧
    session.memoryOverwrite = false := by
  rcases h with ⟨_, _, _, _, _, _, _, _, _, _, _, _, _, _, hExec, hHost, hOverwrite⟩
  exact ⟨hExec, hHost, hOverwrite⟩

end KUOS.PlanOS
