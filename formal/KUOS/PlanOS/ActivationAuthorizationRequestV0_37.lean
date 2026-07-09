import Mathlib
import KUOS.PlanOS.MaterializationExecutionReceiptV0_36

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS

structure ActivationAuthorizationRequestSurface where
  sourceExecutionReceipt : MaterializationExecutionReceiptSurface
  sourceBoundary : MaterializationExecutionReceiptBoundary
  sourceExecutionReceiptBound : Bool
  selectedCandidateBoundToExecutionReceipt : Bool
  materializationExecutionPreserved : Bool
  activationAuthorizationRequestOnly : Bool
  materializationAuthorizationGranted : Bool
  materializationExecuted : Bool
  activationAuthorizationGranted : Bool
  actOSInvoked : Bool
  executionGranted : Bool
  truthAuthorityGranted : Bool
  sourceRequired : sourceExecutionReceiptBound = true
  selectedBoundRequired : selectedCandidateBoundToExecutionReceipt = true
  executionPreservedRequired : materializationExecutionPreserved = true
  requestOnlyRequired : activationAuthorizationRequestOnly = true
  authorizationGrantedRequired : materializationAuthorizationGranted = true
  materializationExecutedRequired : materializationExecuted = true
  activationForbidden : activationAuthorizationGranted = false
  invocationForbidden : actOSInvoked = false
  executionForbidden : executionGranted = false
  truthForbidden : truthAuthorityGranted = false

structure ActivationAuthorizationRequestBoundary where
  requestOwnedByPlanOS : Bool
  sourceMaterializationExecutionReceiptPreserved : Bool
  selectedCandidateBoundToExecutionReceipt : Bool
  materializationExecutionPreserved : Bool
  activationAuthorizationRequestOnly : Bool
  materializationAuthorizationGranted : Bool
  materializationExecuted : Bool
  activationAuthorizationGranted : Bool
  actOSInvoked : Bool
  executionGranted : Bool
  externalCommit : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  requestOwnerRequired : requestOwnedByPlanOS = true
  sourcePreservedRequired : sourceMaterializationExecutionReceiptPreserved = true
  selectedBoundRequired : selectedCandidateBoundToExecutionReceipt = true
  executionPreservedRequired : materializationExecutionPreserved = true
  requestOnlyRequired : activationAuthorizationRequestOnly = true
  authorizationGrantedRequired : materializationAuthorizationGranted = true
  materializationExecutedRequired : materializationExecuted = true
  activationForbidden : activationAuthorizationGranted = false
  invocationForbidden : actOSInvoked = false
  executionForbidden : executionGranted = false
  externalCommitForbidden : externalCommit = false
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSActivationAuthorizationRequestBridge where
  Digest : Type
  digestOf : ActivationAuthorizationRequestSurface → ActivationAuthorizationRequestBoundary → Nat → Digest
  surface : ActivationAuthorizationRequestSurface
  boundary : ActivationAuthorizationRequestBoundary
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

namespace PlanOSActivationAuthorizationRequestBridge

theorem source_execution_receipt_records_materialization_only
    (b : PlanOSActivationAuthorizationRequestBridge) :
    b.surface.sourceExecutionReceipt.materializationExecutionReceiptOnly = true ∧
      b.surface.sourceExecutionReceipt.materializationAuthorizationGranted = true ∧
      b.surface.sourceExecutionReceipt.materializationExecuted = true ∧
      b.surface.sourceExecutionReceipt.activationAuthorizationGranted = false ∧
      b.surface.sourceBoundary.materializationExecutionReceiptOnly = true ∧
      b.surface.sourceBoundary.materializationAuthorizationGranted = true ∧
      b.surface.sourceBoundary.materializationExecuted = true ∧
      b.surface.sourceBoundary.activationAuthorizationGranted = false := by
  exact ⟨b.surface.sourceExecutionReceipt.receiptOnlyRequired,
    b.surface.sourceExecutionReceipt.authorizationGrantedRequired,
    b.surface.sourceExecutionReceipt.materializationExecutedRequired,
    b.surface.sourceExecutionReceipt.activationForbidden,
    b.surface.sourceBoundary.receiptOnlyRequired,
    b.surface.sourceBoundary.authorizationGrantedRequired,
    b.surface.sourceBoundary.materializationExecutedRequired,
    b.surface.sourceBoundary.activationForbidden⟩

theorem request_binds_selected_candidate_to_execution_receipt
    (b : PlanOSActivationAuthorizationRequestBridge) :
    b.surface.sourceExecutionReceiptBound = true ∧
      b.surface.selectedCandidateBoundToExecutionReceipt = true ∧
      b.surface.materializationExecutionPreserved = true ∧
      b.surface.activationAuthorizationRequestOnly = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.executionPreservedRequired, b.surface.requestOnlyRequired⟩

theorem request_preserves_materialization_without_activation_or_execution
    (b : PlanOSActivationAuthorizationRequestBridge) :
    b.surface.materializationAuthorizationGranted = true ∧
      b.surface.materializationExecuted = true ∧
      b.surface.activationAuthorizationGranted = false ∧
      b.surface.actOSInvoked = false ∧
      b.surface.executionGranted = false ∧
      b.surface.truthAuthorityGranted = false ∧
      b.nonAuthority.executionGranted = false ∧
      b.nonAuthority.truthAuthority = false := by
  exact ⟨b.surface.authorizationGrantedRequired,
    b.surface.materializationExecutedRequired,
    b.surface.activationForbidden, b.surface.invocationForbidden,
    b.surface.executionForbidden, b.surface.truthForbidden,
    b.executionForbidden, b.truthForbidden⟩

theorem boundary_blocks_activation_invocation_commit_memory_and_blocker_release
    (b : PlanOSActivationAuthorizationRequestBridge) :
    b.boundary.requestOwnedByPlanOS = true ∧
      b.boundary.sourceMaterializationExecutionReceiptPreserved = true ∧
      b.boundary.selectedCandidateBoundToExecutionReceipt = true ∧
      b.boundary.materializationExecutionPreserved = true ∧
      b.boundary.activationAuthorizationRequestOnly = true ∧
      b.boundary.materializationAuthorizationGranted = true ∧
      b.boundary.materializationExecuted = true ∧
      b.boundary.activationAuthorizationGranted = false ∧
      b.boundary.actOSInvoked = false ∧
      b.boundary.executionGranted = false ∧
      b.boundary.externalCommit = false ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.requestOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.executionPreservedRequired,
    b.boundary.requestOnlyRequired, b.boundary.authorizationGrantedRequired,
    b.boundary.materializationExecutedRequired, b.boundary.activationForbidden,
    b.boundary.invocationForbidden, b.boundary.executionForbidden,
    b.boundary.externalCommitForbidden, b.boundary.overwriteForbidden,
    b.boundary.blockerReleaseForbidden⟩

theorem history_appends_one_activation_authorization_request_record
    (b : PlanOSActivationAuthorizationRequestBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSActivationAuthorizationRequestBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSActivationAuthorizationRequestBridge

end PlanOS
end KUOS
