import Mathlib
import KUOS.PlanOS.MaterializationAuthorizationRequestV0_33

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS

structure MaterializationAuthorizationRequestReceiptSurface where
  sourceRequest : MaterializationAuthorizationRequestSurface
  sourceBoundary : MaterializationAuthorizationRequestBoundary
  sourceRequestBound : Bool
  selectedCandidateBoundToAuthorizationRequest : Bool
  materializationAuthorizationRequestReceiptOnly : Bool
  materializationAuthorizationGranted : Bool
  materializationExecuted : Bool
  activationAuthorizationGranted : Bool
  executionGranted : Bool
  truthAuthorityGranted : Bool
  sourceRequired : sourceRequestBound = true
  selectedBoundRequired : selectedCandidateBoundToAuthorizationRequest = true
  receiptOnlyRequired : materializationAuthorizationRequestReceiptOnly = true
  materializationAuthorizationForbidden : materializationAuthorizationGranted = false
  materializationExecutionForbidden : materializationExecuted = false
  activationForbidden : activationAuthorizationGranted = false
  executionForbidden : executionGranted = false
  truthForbidden : truthAuthorityGranted = false

structure MaterializationAuthorizationRequestReceiptBoundary where
  receiptOwnedByPlanOS : Bool
  sourceMaterializationAuthorizationRequestPreserved : Bool
  selectedCandidateBoundToAuthorizationRequest : Bool
  materializationAuthorizationRequestReceiptOnly : Bool
  materializationAuthorizationGranted : Bool
  materializationExecuted : Bool
  actOSInvoked : Bool
  externalCommit : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  receiptOwnerRequired : receiptOwnedByPlanOS = true
  sourcePreservedRequired : sourceMaterializationAuthorizationRequestPreserved = true
  selectedBoundRequired : selectedCandidateBoundToAuthorizationRequest = true
  receiptOnlyRequired : materializationAuthorizationRequestReceiptOnly = true
  materializationAuthorizationForbidden : materializationAuthorizationGranted = false
  materializationExecutionForbidden : materializationExecuted = false
  invocationForbidden : actOSInvoked = false
  externalCommitForbidden : externalCommit = false
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSMaterializationAuthorizationRequestReceiptBridge where
  Digest : Type
  digestOf : MaterializationAuthorizationRequestReceiptSurface → MaterializationAuthorizationRequestReceiptBoundary → Nat → Digest
  surface : MaterializationAuthorizationRequestReceiptSurface
  boundary : MaterializationAuthorizationRequestReceiptBoundary
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

namespace PlanOSMaterializationAuthorizationRequestReceiptBridge

theorem source_request_remains_request_only
    (b : PlanOSMaterializationAuthorizationRequestReceiptBridge) :
    b.surface.sourceRequest.materializationAuthorizationRequestOnly = true ∧
      b.surface.sourceRequest.selectedCandidateBoundToPreflight = true ∧
      b.surface.sourceBoundary.materializationAuthorizationRequestOnly = true ∧
      b.surface.sourceBoundary.materializationAuthorizationGranted = false ∧
      b.surface.sourceBoundary.materializationExecuted = false := by
  exact ⟨b.surface.sourceRequest.requestOnlyRequired,
    b.surface.sourceRequest.selectedBoundRequired,
    b.surface.sourceBoundary.requestOnlyRequired,
    b.surface.sourceBoundary.materializationAuthorizationForbidden,
    b.surface.sourceBoundary.materializationExecutionForbidden⟩

theorem receipt_binds_selected_candidate_to_authorization_request
    (b : PlanOSMaterializationAuthorizationRequestReceiptBridge) :
    b.surface.sourceRequestBound = true ∧
      b.surface.selectedCandidateBoundToAuthorizationRequest = true ∧
      b.surface.materializationAuthorizationRequestReceiptOnly = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.receiptOnlyRequired⟩

theorem receipt_grants_no_authorization_execution_activation_or_truth
    (b : PlanOSMaterializationAuthorizationRequestReceiptBridge) :
    b.surface.materializationAuthorizationGranted = false ∧
      b.surface.materializationExecuted = false ∧
      b.surface.activationAuthorizationGranted = false ∧
      b.surface.executionGranted = false ∧
      b.surface.truthAuthorityGranted = false ∧
      b.nonAuthority.executionGranted = false ∧
      b.nonAuthority.truthAuthority = false := by
  exact ⟨b.surface.materializationAuthorizationForbidden,
    b.surface.materializationExecutionForbidden,
    b.surface.activationForbidden, b.surface.executionForbidden,
    b.surface.truthForbidden, b.executionForbidden, b.truthForbidden⟩

theorem boundary_blocks_materialization_execution_commit_memory_and_blocker_release
    (b : PlanOSMaterializationAuthorizationRequestReceiptBridge) :
    b.boundary.receiptOwnedByPlanOS = true ∧
      b.boundary.sourceMaterializationAuthorizationRequestPreserved = true ∧
      b.boundary.selectedCandidateBoundToAuthorizationRequest = true ∧
      b.boundary.materializationAuthorizationRequestReceiptOnly = true ∧
      b.boundary.materializationAuthorizationGranted = false ∧
      b.boundary.materializationExecuted = false ∧
      b.boundary.actOSInvoked = false ∧
      b.boundary.externalCommit = false ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.receiptOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.receiptOnlyRequired,
    b.boundary.materializationAuthorizationForbidden,
    b.boundary.materializationExecutionForbidden,
    b.boundary.invocationForbidden, b.boundary.externalCommitForbidden,
    b.boundary.overwriteForbidden, b.boundary.blockerReleaseForbidden⟩

theorem history_appends_one_authorization_request_receipt_record
    (b : PlanOSMaterializationAuthorizationRequestReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSMaterializationAuthorizationRequestReceiptBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSMaterializationAuthorizationRequestReceiptBridge

end PlanOS
end KUOS
