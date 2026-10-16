import Mathlib
import KUOS.PlanOS.LeaseMonitorSuspensionV0_16

namespace KUOS.PlanOS

inductive SuspensionRecoveryRoute where
  | revalidate
  | renewOrEscalate
  | rerotateRequired
  deriving DecidableEq

inductive SuspensionRecoveryTarget where
  | revalidationIntake
  | v11RenewalReview
  | v12Escalation
  | v12Rerotation
  deriving DecidableEq

structure SuspensionRecoveryRoot where
  suspended : Bool
  terminal : Bool
  route : SuspensionRecoveryRoute
  renewalEligibleForAll : Bool

structure SuspensionRecoveryHandoff where
  target : SuspensionRecoveryTarget
  oldSessionClosed : Bool
  oldSessionResumeAllowed : Bool
  newLineageRequired : Bool
  newActivationRequired : Bool
  newSessionRequired : Bool
  executionGranted : Bool
  hostAccessGranted : Bool
  memoryOverwrite : Bool


def recoveryTargetAdmissible
    (root : SuspensionRecoveryRoot)
    (handoff : SuspensionRecoveryHandoff) : Prop :=
  match root.route with
  | SuspensionRecoveryRoute.revalidate =>
      handoff.target = SuspensionRecoveryTarget.revalidationIntake
  | SuspensionRecoveryRoute.renewOrEscalate =>
      if root.renewalEligibleForAll then
        handoff.target = SuspensionRecoveryTarget.v11RenewalReview
      else
        handoff.target = SuspensionRecoveryTarget.v12Escalation
  | SuspensionRecoveryRoute.rerotateRequired =>
      handoff.target = SuspensionRecoveryTarget.v12Rerotation


def suspensionRecoveryAdmissible
    (root : SuspensionRecoveryRoot)
    (handoff : SuspensionRecoveryHandoff) : Prop :=
  root.suspended = true ∧
  root.terminal = true ∧
  recoveryTargetAdmissible root handoff ∧
  handoff.oldSessionClosed = true ∧
  handoff.oldSessionResumeAllowed = false ∧
  handoff.newLineageRequired = true ∧
  handoff.newActivationRequired = true ∧
  handoff.newSessionRequired = true ∧
  handoff.executionGranted = false ∧
  handoff.hostAccessGranted = false ∧
  handoff.memoryOverwrite = false


theorem recovery_requires_terminal_suspension
    (root : SuspensionRecoveryRoot)
    (handoff : SuspensionRecoveryHandoff)
    (h : suspensionRecoveryAdmissible root handoff) :
    root.suspended = true ∧ root.terminal = true := by
  exact ⟨h.1, h.2.1⟩


theorem revalidation_route_targets_revalidation
    (root : SuspensionRecoveryRoot)
    (handoff : SuspensionRecoveryHandoff)
    (route : root.route = SuspensionRecoveryRoute.revalidate)
    (h : suspensionRecoveryAdmissible root handoff) :
    handoff.target = SuspensionRecoveryTarget.revalidationIntake := by
  have htarget := h.2.2.1
  simp [recoveryTargetAdmissible, route] at htarget
  exact htarget


theorem eligible_renewal_route_targets_v11
    (root : SuspensionRecoveryRoot)
    (handoff : SuspensionRecoveryHandoff)
    (route : root.route = SuspensionRecoveryRoute.renewOrEscalate)
    (eligible : root.renewalEligibleForAll = true)
    (h : suspensionRecoveryAdmissible root handoff) :
    handoff.target = SuspensionRecoveryTarget.v11RenewalReview := by
  have htarget := h.2.2.1
  simp [recoveryTargetAdmissible, route, eligible] at htarget
  exact htarget


theorem ineligible_renewal_route_targets_v12_escalation
    (root : SuspensionRecoveryRoot)
    (handoff : SuspensionRecoveryHandoff)
    (route : root.route = SuspensionRecoveryRoute.renewOrEscalate)
    (ineligible : root.renewalEligibleForAll = false)
    (h : suspensionRecoveryAdmissible root handoff) :
    handoff.target = SuspensionRecoveryTarget.v12Escalation := by
  have htarget := h.2.2.1
  simp [recoveryTargetAdmissible, route, ineligible] at htarget
  exact htarget


theorem rerotation_route_targets_v12_rerotation
    (root : SuspensionRecoveryRoot)
    (handoff : SuspensionRecoveryHandoff)
    (route : root.route = SuspensionRecoveryRoute.rerotateRequired)
    (h : suspensionRecoveryAdmissible root handoff) :
    handoff.target = SuspensionRecoveryTarget.v12Rerotation := by
  have htarget := h.2.2.1
  simp [recoveryTargetAdmissible, route] at htarget
  exact htarget


theorem recovery_closes_old_session_without_resume
    (root : SuspensionRecoveryRoot)
    (handoff : SuspensionRecoveryHandoff)
    (h : suspensionRecoveryAdmissible root handoff) :
    handoff.oldSessionClosed = true ∧
    handoff.oldSessionResumeAllowed = false := by
  exact ⟨h.2.2.2.1, h.2.2.2.2.1⟩


theorem recovery_requires_new_lineage_activation_and_session
    (root : SuspensionRecoveryRoot)
    (handoff : SuspensionRecoveryHandoff)
    (h : suspensionRecoveryAdmissible root handoff) :
    handoff.newLineageRequired = true ∧
    handoff.newActivationRequired = true ∧
    handoff.newSessionRequired = true := by
  exact ⟨h.2.2.2.2.2.1,
    h.2.2.2.2.2.2.1,
    h.2.2.2.2.2.2.2.1⟩


theorem suspension_recovery_router_grants_no_authority
    (root : SuspensionRecoveryRoot)
    (handoff : SuspensionRecoveryHandoff)
    (h : suspensionRecoveryAdmissible root handoff) :
    handoff.executionGranted = false ∧
    handoff.hostAccessGranted = false ∧
    handoff.memoryOverwrite = false := by
  exact ⟨h.2.2.2.2.2.2.2.2.1,
    h.2.2.2.2.2.2.2.2.2.1,
    h.2.2.2.2.2.2.2.2.2.2⟩

end KUOS.PlanOS
