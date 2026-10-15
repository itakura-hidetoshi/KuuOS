import Mathlib
import KUOS.ObserveOS.OpenClawGatewayEventHintV0_4

namespace KUOS
namespace ObserveOS

structure OpenClawSupervisorReadinessBoundary where
  pluginRuntimeHooksInspected : Bool
  controlHealthy : Bool
  freshGatewayHelloObserved : Bool
  initialAuditReconciliationComplete : Bool
  closedLoopReady : Bool
  hooksRequired : pluginRuntimeHooksInspected = true
  controlRequired : controlHealthy = true
  helloRequired : freshGatewayHelloObserved = true
  auditRequired : initialAuditReconciliationComplete = true
  readinessDefinition :
    closedLoopReady =
      (pluginRuntimeHooksInspected && controlHealthy &&
        freshGatewayHelloObserved && initialAuditReconciliationComplete)

theorem openclaw_supervisor_readiness_requires_all_layers
    (boundary : OpenClawSupervisorReadinessBoundary) :
    boundary.closedLoopReady = true := by
  rw [boundary.readinessDefinition]
  simp [boundary.hooksRequired, boundary.controlRequired, boundary.helloRequired,
    boundary.auditRequired]


structure OpenClawSupervisorAuthorityBoundary where
  truthGranted : Bool
  verificationGranted : Bool
  effectPermissionGranted : Bool
  memoryOverwrite : Bool
  planCompletionGranted : Bool
  rollbackProofGranted : Bool
  truthForbidden : truthGranted = false
  verificationForbidden : verificationGranted = false
  effectPermissionForbidden : effectPermissionGranted = false
  overwriteForbidden : memoryOverwrite = false
  planCompletionForbidden : planCompletionGranted = false
  rollbackProofForbidden : rollbackProofGranted = false

def OpenClawSupervisorAuthorityBoundary.toObserveNonAuthority
    (boundary : OpenClawSupervisorAuthorityBoundary) : NonAuthorityBoundary where
  truthGranted := boundary.truthGranted
  verificationGranted := boundary.verificationGranted
  effectPermissionGranted := boundary.effectPermissionGranted
  memoryOverwrite := boundary.memoryOverwrite
  truthForbidden := boundary.truthForbidden
  verificationForbidden := boundary.verificationForbidden
  effectPermissionForbidden := boundary.effectPermissionForbidden
  overwriteForbidden := boundary.overwriteForbidden

theorem openclaw_supervisor_ready_grants_no_new_authority
    (boundary : OpenClawSupervisorAuthorityBoundary) :
    boundary.truthGranted = false ∧
      boundary.verificationGranted = false ∧
      boundary.effectPermissionGranted = false ∧
      boundary.memoryOverwrite = false := by
  exact observe_lineage_envelope_grants_no_new_authority
    (OpenClawSupervisorAuthorityBoundary.toObserveNonAuthority boundary)

theorem openclaw_supervisor_ready_does_not_complete_plan_or_prove_rollback
    (boundary : OpenClawSupervisorAuthorityBoundary) :
    boundary.planCompletionGranted = false ∧ boundary.rollbackProofGranted = false := by
  exact ⟨boundary.planCompletionForbidden, boundary.rollbackProofForbidden⟩


structure OpenClawSupervisorFailureBoundary where
  requiredComponentFailed : Bool
  closedLoopReady : Bool
  policyServiceStopped : Bool
  failureObserved : requiredComponentFailed = true
  readyRevoked : requiredComponentFailed = true → closedLoopReady = false
  policyStopRequired : requiredComponentFailed = true → policyServiceStopped = true

theorem openclaw_supervisor_component_failure_revokes_ready_claim
    (boundary : OpenClawSupervisorFailureBoundary) :
    boundary.closedLoopReady = false ∧ boundary.policyServiceStopped = true := by
  exact ⟨boundary.readyRevoked boundary.failureObserved,
    boundary.policyStopRequired boundary.failureObserved⟩


structure OpenClawSupervisorInstallBoundary where
  installRequested : Bool
  explicitApproval : Bool
  configMutationPerformed : Bool
  requestObserved : installRequested = true
  mutationRequiresApproval : configMutationPerformed = true → explicitApproval = true
  requestedMutationPerformed : installRequested = true → configMutationPerformed = true

theorem openclaw_supervisor_install_requires_explicit_approval
    (boundary : OpenClawSupervisorInstallBoundary) :
    boundary.explicitApproval = true := by
  exact boundary.mutationRequiresApproval (boundary.requestedMutationPerformed boundary.requestObserved)

end ObserveOS
end KUOS
