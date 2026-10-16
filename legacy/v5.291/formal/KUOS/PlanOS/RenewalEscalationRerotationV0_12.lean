import Mathlib
import KUOS.PlanOS.BoundedRenewalGovernanceV0_11

namespace KUOS.PlanOS

inductive EscalationRoute where
  | deny
  | humanHandover
  | reRotate
  deriving DecidableEq

structure EscalationRoot where
  currentOwner : Nat
  currentEpoch : Nat
  escalationRequired : Bool

structure EscalationDecision where
  route : EscalationRoute
  targetOwner : Nat
  nextEpoch : Nat
  humanAccepted : Bool
  oldLeaseClosed : Bool
  newV09Required : Bool
  continuationGranted : Bool


def escalationDecisionAdmissible
    (root : EscalationRoot)
    (decision : EscalationDecision) : Prop :=
  root.escalationRequired = true ∧
  decision.oldLeaseClosed = true ∧
  match decision.route with
  | EscalationRoute.deny =>
      decision.continuationGranted = false ∧
      decision.newV09Required = false
  | EscalationRoute.humanHandover =>
      decision.targetOwner ≠ root.currentOwner ∧
      decision.humanAccepted = true ∧
      decision.continuationGranted = false ∧
      decision.newV09Required = false
  | EscalationRoute.reRotate =>
      decision.targetOwner = root.currentOwner ∧
      decision.nextEpoch = root.currentEpoch + 1 ∧
      decision.newV09Required = true ∧
      decision.continuationGranted = true


theorem admissible_decision_closes_old_lease
    (root : EscalationRoot)
    (decision : EscalationDecision)
    (h : escalationDecisionAdmissible root decision) :
    decision.oldLeaseClosed = true := by
  exact h.2.1


theorem deny_grants_no_continuation
    (root : EscalationRoot)
    (decision : EscalationDecision)
    (route : decision.route = EscalationRoute.deny)
    (h : escalationDecisionAdmissible root decision) :
    decision.continuationGranted = false := by
  rcases h with ⟨_, _, hroute⟩
  rw [route] at hroute
  exact hroute.1


theorem handover_requires_distinct_owner
    (root : EscalationRoot)
    (decision : EscalationDecision)
    (route : decision.route = EscalationRoute.humanHandover)
    (h : escalationDecisionAdmissible root decision) :
    decision.targetOwner ≠ root.currentOwner := by
  rcases h with ⟨_, _, hroute⟩
  rw [route] at hroute
  exact hroute.1


theorem handover_requires_human_acceptance
    (root : EscalationRoot)
    (decision : EscalationDecision)
    (route : decision.route = EscalationRoute.humanHandover)
    (h : escalationDecisionAdmissible root decision) :
    decision.humanAccepted = true := by
  rcases h with ⟨_, _, hroute⟩
  rw [route] at hroute
  exact hroute.2.1


theorem rerotation_strictly_increases_epoch
    (root : EscalationRoot)
    (decision : EscalationDecision)
    (route : decision.route = EscalationRoute.reRotate)
    (h : escalationDecisionAdmissible root decision) :
    decision.nextEpoch = root.currentEpoch + 1 := by
  rcases h with ⟨_, _, hroute⟩
  rw [route] at hroute
  exact hroute.2.1


theorem rerotation_requires_new_v09_chain
    (root : EscalationRoot)
    (decision : EscalationDecision)
    (route : decision.route = EscalationRoute.reRotate)
    (h : escalationDecisionAdmissible root decision) :
    decision.newV09Required = true := by
  rcases h with ⟨_, _, hroute⟩
  rw [route] at hroute
  exact hroute.2.2.1

structure EscalationAuthorityBoundary where
  executionGranted : Bool
  hostAccessGranted : Bool
  memoryOverwrite : Bool
  noExecution : executionGranted = false
  noHostAccess : hostAccessGranted = false
  noOverwrite : memoryOverwrite = false


theorem escalation_decision_grants_no_authority
    (boundary : EscalationAuthorityBoundary) :
    boundary.executionGranted = false ∧
    boundary.hostAccessGranted = false ∧
    boundary.memoryOverwrite = false := by
  exact ⟨boundary.noExecution, boundary.noHostAccess, boundary.noOverwrite⟩

end KUOS.PlanOS
