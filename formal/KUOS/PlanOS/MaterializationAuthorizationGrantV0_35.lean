import Mathlib
import KUOS.PlanOS.MaterializationAuthorizationRequestReceiptV0_34

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS

structure MaterializationAuthorizationGrantSurface where
  sourceRequestReceipt : MaterializationAuthorizationRequestReceiptSurface
  sourceBoundary : MaterializationAuthorizationRequestReceiptBoundary
  sourceRequestReceiptBound : Bool
  selectedCandidateBoundToRequestReceipt : Bool
  materializationAuthorizationGrantOnly : Bool
  materializationAuthorizationGranted : Bool
  materializationExecuted : Bool
  activationAuthorizationGranted : Bool
  executionGranted : Bool
  truthAuthorityGranted : Bool
  sourceRequired : sourceRequestReceiptBound = true
  selectedBoundRequired : selectedCandidateBoundToRequestReceipt = true
  grantOnlyRequired : materializationAuthorizationGrantOnly = true
  authorizationGrantedRequired : materializationAuthorizationGranted = true
  materializationExecutionForbidden : materializationExecuted = false
  activationForbidden : activationAuthorizationGranted = false
  executionForbidden : executionGranted = false
  truthForbidden : truthAuthorityGranted = false

structure MaterializationAuthorizationGrantBoundary where
  grantOwnedByPlanOS : Bool
  sourceMaterializationAuthorizationRequestReceiptPreserved : Bool
  selectedCandidateBoundToRequestReceipt : Bool
  materializationAuthorizationGrantOnly : Bool
  materializationAuthorizationGranted : Bool
  materializationExecuted : Bool
  actOSInvoked : Bool
  externalCommit : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  grantOwnerRequired : grantOwnedByPlanOS = true
  sourcePreservedRequired : sourceMaterializationAuthorizationRequestReceiptPreserved = true
  selectedBoundRequired : selectedCandidateBoundToRequestReceipt = true
  grantOnlyRequired : materializationAuthorizationGrantOnly = true
  authorizationGrantedRequired : materializationAuthorizationGranted = true
  materializationExecutionForbidden : materializationExecuted = false
  invocationForbidden : actOSInvoked = false
  externalCommitForbidden : externalCommit = false
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSMaterializationAuthorizationGrantBridge where
  Digest : Type
  digestOf : MaterializationAuthorizationGrantSurface → MaterializationAuthorizationGrantBoundary → Nat → Digest
  surface : MaterializationAuthorizationGrantSurface
  boundary : MaterializationAuthorizationGrantBoundary
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

namespace PlanOSMaterializationAuthorizationGrantBridge

theorem source_request_receipt_remains_receipt_only
    (b : PlanOSMaterializationAuthorizationGrantBridge) :
    b.surface.sourceRequestReceipt.materializationAuthorizationRequestReceiptOnly = true ∧
      b.surface.sourceRequestReceipt.selectedCandidateBoundToAuthorizationRequest = true ∧
      b.surface.sourceBoundary.materializationAuthorizationRequestReceiptOnly = true ∧
      b.surface.sourceBoundary.materializationAuthorizationGranted = false ∧
      b.surface.sourceBoundary.materializationExecuted = false := by
  exact ⟨b.surface.sourceRequestReceipt.receiptOnlyRequired,
    b.surface.sourceRequestReceipt.selectedBoundRequired,
    b.surface.sourceBoundary.receiptOnlyRequired,
    b.surface.sourceBoundary.materializationAuthorizationForbidden,
    b.surface.sourceBoundary.materializationExecutionForbidden⟩

theorem grant_binds_selected_candidate_to_request_receipt
    (b : PlanOSMaterializationAuthorizationGrantBridge) :
    b.surface.sourceRequestReceiptBound = true ∧
      b.surface.selectedCandidateBoundToRequestReceipt = true ∧
      b.surface.materializationAuthorizationGrantOnly = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.grantOnlyRequired⟩

theorem grant_authorizes_materialization_but_not_execution_activation_or_truth
    (b : PlanOSMaterializationAuthorizationGrantBridge) :
    b.surface.materializationAuthorizationGranted = true ∧
      b.surface.materializationExecuted = false ∧
      b.surface.activationAuthorizationGranted = false ∧
      b.surface.executionGranted = false ∧
      b.surface.truthAuthorityGranted = false ∧
      b.nonAuthority.executionGranted = false ∧
      b.nonAuthority.truthAuthority = false := by
  exact ⟨b.surface.authorizationGrantedRequired,
    b.surface.materializationExecutionForbidden,
    b.surface.activationForbidden, b.surface.executionForbidden,
    b.surface.truthForbidden, b.executionForbidden, b.truthForbidden⟩

theorem boundary_blocks_materialization_execution_commit_memory_and_blocker_release
    (b : PlanOSMaterializationAuthorizationGrantBridge) :
    b.boundary.grantOwnedByPlanOS = true ∧
      b.boundary.sourceMaterializationAuthorizationRequestReceiptPreserved = true ∧
      b.boundary.selectedCandidateBoundToRequestReceipt = true ∧
      b.boundary.materializationAuthorizationGrantOnly = true ∧
      b.boundary.materializationAuthorizationGranted = true ∧
      b.boundary.materializationExecuted = false ∧
      b.boundary.actOSInvoked = false ∧
      b.boundary.externalCommit = false ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.grantOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.grantOnlyRequired,
    b.boundary.authorizationGrantedRequired,
    b.boundary.materializationExecutionForbidden,
    b.boundary.invocationForbidden, b.boundary.externalCommitForbidden,
    b.boundary.overwriteForbidden, b.boundary.blockerReleaseForbidden⟩

theorem history_appends_one_materialization_authorization_grant_record
    (b : PlanOSMaterializationAuthorizationGrantBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSMaterializationAuthorizationGrantBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSMaterializationAuthorizationGrantBridge

end PlanOS
end KUOS
