import Mathlib
import KUOS.PlanOS.ActivationAuthorizationRequestV0_37

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS

structure ActivationAuthorizationGrantSurface where
  sourceActivationRequest : ActivationAuthorizationRequestSurface
  sourceBoundary : ActivationAuthorizationRequestBoundary
  sourceActivationRequestBound : Bool
  selectedCandidateBoundToActivationRequest : Bool
  materializationExecutionPreserved : Bool
  activationAuthorizationGrantOnly : Bool
  materializationAuthorizationGranted : Bool
  materializationExecuted : Bool
  activationAuthorizationGranted : Bool
  actOSInvoked : Bool
  executionGranted : Bool
  truthAuthorityGranted : Bool
  sourceRequired : sourceActivationRequestBound = true
  selectedBoundRequired : selectedCandidateBoundToActivationRequest = true
  executionPreservedRequired : materializationExecutionPreserved = true
  grantOnlyRequired : activationAuthorizationGrantOnly = true
  materializationAuthorizationGrantedRequired : materializationAuthorizationGranted = true
  materializationExecutedRequired : materializationExecuted = true
  activationAuthorizationGrantedRequired : activationAuthorizationGranted = true
  invocationForbidden : actOSInvoked = false
  executionForbidden : executionGranted = false
  truthForbidden : truthAuthorityGranted = false

structure ActivationAuthorizationGrantBoundary where
  grantOwnedByPlanOS : Bool
  sourceActivationAuthorizationRequestPreserved : Bool
  selectedCandidateBoundToActivationRequest : Bool
  materializationExecutionPreserved : Bool
  activationAuthorizationGrantOnly : Bool
  materializationAuthorizationGranted : Bool
  materializationExecuted : Bool
  activationAuthorizationGranted : Bool
  actOSInvoked : Bool
  executionGranted : Bool
  externalCommit : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  grantOwnerRequired : grantOwnedByPlanOS = true
  sourcePreservedRequired : sourceActivationAuthorizationRequestPreserved = true
  selectedBoundRequired : selectedCandidateBoundToActivationRequest = true
  executionPreservedRequired : materializationExecutionPreserved = true
  grantOnlyRequired : activationAuthorizationGrantOnly = true
  materializationAuthorizationGrantedRequired : materializationAuthorizationGranted = true
  materializationExecutedRequired : materializationExecuted = true
  activationAuthorizationGrantedRequired : activationAuthorizationGranted = true
  invocationForbidden : actOSInvoked = false
  executionForbidden : executionGranted = false
  externalCommitForbidden : externalCommit = false
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSActivationAuthorizationGrantBridge where
  Digest : Type
  digestOf : ActivationAuthorizationGrantSurface → ActivationAuthorizationGrantBoundary → Nat → Digest
  surface : ActivationAuthorizationGrantSurface
  boundary : ActivationAuthorizationGrantBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  nonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  executionForbidden : nonAuthority.executionGranted = false
  truthForbidden : nonAuthority.truthAuthority = false
  clinicalForbidden : nonAuthority.clinicalAuthority = false
  legalForbidden : nonAuthority.legalAuthority = false
  overwriteForbidden : nonAuthority.memoryOverwrite = false

namespace PlanOSActivationAuthorizationGrantBridge

theorem source_activation_request_remains_request_only
    (b : PlanOSActivationAuthorizationGrantBridge) :
    b.surface.sourceActivationRequest.activationAuthorizationRequestOnly = true ∧
      b.surface.sourceActivationRequest.materializationAuthorizationGranted = true ∧
      b.surface.sourceActivationRequest.materializationExecuted = true ∧
      b.surface.sourceActivationRequest.activationAuthorizationGranted = false ∧
      b.surface.sourceBoundary.activationAuthorizationRequestOnly = true ∧
      b.surface.sourceBoundary.materializationAuthorizationGranted = true ∧
      b.surface.sourceBoundary.materializationExecuted = true ∧
      b.surface.sourceBoundary.activationAuthorizationGranted = false := by
  exact ⟨b.surface.sourceActivationRequest.requestOnlyRequired,
    b.surface.sourceActivationRequest.authorizationGrantedRequired,
    b.surface.sourceActivationRequest.materializationExecutedRequired,
    b.surface.sourceActivationRequest.activationForbidden,
    b.surface.sourceBoundary.requestOnlyRequired,
    b.surface.sourceBoundary.authorizationGrantedRequired,
    b.surface.sourceBoundary.materializationExecutedRequired,
    b.surface.sourceBoundary.activationForbidden⟩

theorem grant_binds_selected_candidate_to_activation_request
    (b : PlanOSActivationAuthorizationGrantBridge) :
    b.surface.sourceActivationRequestBound = true ∧
      b.surface.selectedCandidateBoundToActivationRequest = true ∧
      b.surface.materializationExecutionPreserved = true ∧
      b.surface.activationAuthorizationGrantOnly = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.executionPreservedRequired, b.surface.grantOnlyRequired⟩

theorem grant_authorizes_activation_but_not_invocation_execution_or_truth
    (b : PlanOSActivationAuthorizationGrantBridge) :
    b.surface.materializationAuthorizationGranted = true ∧
      b.surface.materializationExecuted = true ∧
      b.surface.activationAuthorizationGranted = true ∧
      b.surface.actOSInvoked = false ∧
      b.surface.executionGranted = false ∧
      b.surface.truthAuthorityGranted = false ∧
      b.nonAuthority.executionGranted = false ∧
      b.nonAuthority.truthAuthority = false := by
  exact ⟨b.surface.materializationAuthorizationGrantedRequired,
    b.surface.materializationExecutedRequired,
    b.surface.activationAuthorizationGrantedRequired,
    b.surface.invocationForbidden, b.surface.executionForbidden,
    b.surface.truthForbidden, b.executionForbidden, b.truthForbidden⟩

theorem boundary_blocks_invocation_execution_commit_memory_and_blocker_release
    (b : PlanOSActivationAuthorizationGrantBridge) :
    b.boundary.grantOwnedByPlanOS = true ∧
      b.boundary.sourceActivationAuthorizationRequestPreserved = true ∧
      b.boundary.selectedCandidateBoundToActivationRequest = true ∧
      b.boundary.materializationExecutionPreserved = true ∧
      b.boundary.activationAuthorizationGrantOnly = true ∧
      b.boundary.materializationAuthorizationGranted = true ∧
      b.boundary.materializationExecuted = true ∧
      b.boundary.activationAuthorizationGranted = true ∧
      b.boundary.actOSInvoked = false ∧
      b.boundary.executionGranted = false ∧
      b.boundary.externalCommit = false ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.grantOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.executionPreservedRequired,
    b.boundary.grantOnlyRequired, b.boundary.materializationAuthorizationGrantedRequired,
    b.boundary.materializationExecutedRequired, b.boundary.activationAuthorizationGrantedRequired,
    b.boundary.invocationForbidden, b.boundary.executionForbidden,
    b.boundary.externalCommitForbidden, b.boundary.overwriteForbidden,
    b.boundary.blockerReleaseForbidden⟩

theorem history_appends_one_activation_authorization_grant_record
    (b : PlanOSActivationAuthorizationGrantBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSActivationAuthorizationGrantBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSActivationAuthorizationGrantBridge

end PlanOS
end KUOS
