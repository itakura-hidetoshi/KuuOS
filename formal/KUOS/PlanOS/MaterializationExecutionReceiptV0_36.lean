import Mathlib
import KUOS.PlanOS.MaterializationAuthorizationGrantV0_35

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS

structure MaterializationExecutionReceiptSurface where
  sourceAuthorizationGrant : MaterializationAuthorizationGrantSurface
  sourceBoundary : MaterializationAuthorizationGrantBoundary
  sourceAuthorizationGrantBound : Bool
  selectedCandidateBoundToAuthorizationGrant : Bool
  materializationAuthorizationGrantPreserved : Bool
  materializationExecutionReceiptOnly : Bool
  materializationAuthorizationGranted : Bool
  materializationExecuted : Bool
  activationAuthorizationGranted : Bool
  executionGranted : Bool
  truthAuthorityGranted : Bool
  sourceRequired : sourceAuthorizationGrantBound = true
  selectedBoundRequired : selectedCandidateBoundToAuthorizationGrant = true
  grantPreservedRequired : materializationAuthorizationGrantPreserved = true
  receiptOnlyRequired : materializationExecutionReceiptOnly = true
  authorizationGrantedRequired : materializationAuthorizationGranted = true
  materializationExecutedRequired : materializationExecuted = true
  activationForbidden : activationAuthorizationGranted = false
  executionForbidden : executionGranted = false
  truthForbidden : truthAuthorityGranted = false

structure MaterializationExecutionReceiptBoundary where
  receiptOwnedByPlanOS : Bool
  sourceMaterializationAuthorizationGrantPreserved : Bool
  selectedCandidateBoundToAuthorizationGrant : Bool
  materializationAuthorizationGrantPreserved : Bool
  materializationExecutionReceiptOnly : Bool
  materializationAuthorizationGranted : Bool
  materializationExecuted : Bool
  activationAuthorizationGranted : Bool
  actOSInvoked : Bool
  externalCommit : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  receiptOwnerRequired : receiptOwnedByPlanOS = true
  sourcePreservedRequired : sourceMaterializationAuthorizationGrantPreserved = true
  selectedBoundRequired : selectedCandidateBoundToAuthorizationGrant = true
  grantPreservedRequired : materializationAuthorizationGrantPreserved = true
  receiptOnlyRequired : materializationExecutionReceiptOnly = true
  authorizationGrantedRequired : materializationAuthorizationGranted = true
  materializationExecutedRequired : materializationExecuted = true
  activationForbidden : activationAuthorizationGranted = false
  invocationForbidden : actOSInvoked = false
  externalCommitForbidden : externalCommit = false
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSMaterializationExecutionReceiptBridge where
  Digest : Type
  digestOf : MaterializationExecutionReceiptSurface → MaterializationExecutionReceiptBoundary → Nat → Digest
  surface : MaterializationExecutionReceiptSurface
  boundary : MaterializationExecutionReceiptBoundary
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

namespace PlanOSMaterializationExecutionReceiptBridge

theorem source_authorization_grant_remains_grant_only
    (b : PlanOSMaterializationExecutionReceiptBridge) :
    b.surface.sourceAuthorizationGrant.materializationAuthorizationGrantOnly = true ∧
      b.surface.sourceAuthorizationGrant.materializationAuthorizationGranted = true ∧
      b.surface.sourceAuthorizationGrant.materializationExecuted = false ∧
      b.surface.sourceBoundary.materializationAuthorizationGrantOnly = true ∧
      b.surface.sourceBoundary.materializationAuthorizationGranted = true ∧
      b.surface.sourceBoundary.materializationExecuted = false := by
  exact ⟨b.surface.sourceAuthorizationGrant.grantOnlyRequired,
    b.surface.sourceAuthorizationGrant.authorizationGrantedRequired,
    b.surface.sourceAuthorizationGrant.materializationExecutionForbidden,
    b.surface.sourceBoundary.grantOnlyRequired,
    b.surface.sourceBoundary.authorizationGrantedRequired,
    b.surface.sourceBoundary.materializationExecutionForbidden⟩

theorem receipt_binds_selected_candidate_to_authorization_grant
    (b : PlanOSMaterializationExecutionReceiptBridge) :
    b.surface.sourceAuthorizationGrantBound = true ∧
      b.surface.selectedCandidateBoundToAuthorizationGrant = true ∧
      b.surface.materializationAuthorizationGrantPreserved = true ∧
      b.surface.materializationExecutionReceiptOnly = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.grantPreservedRequired, b.surface.receiptOnlyRequired⟩

theorem receipt_records_materialization_execution_but_not_activation_or_truth
    (b : PlanOSMaterializationExecutionReceiptBridge) :
    b.surface.materializationAuthorizationGranted = true ∧
      b.surface.materializationExecuted = true ∧
      b.surface.activationAuthorizationGranted = false ∧
      b.surface.executionGranted = false ∧
      b.surface.truthAuthorityGranted = false ∧
      b.nonAuthority.executionGranted = false ∧
      b.nonAuthority.truthAuthority = false := by
  exact ⟨b.surface.authorizationGrantedRequired,
    b.surface.materializationExecutedRequired,
    b.surface.activationForbidden, b.surface.executionForbidden,
    b.surface.truthForbidden, b.executionForbidden, b.truthForbidden⟩

theorem boundary_blocks_activation_commit_memory_and_blocker_release
    (b : PlanOSMaterializationExecutionReceiptBridge) :
    b.boundary.receiptOwnedByPlanOS = true ∧
      b.boundary.sourceMaterializationAuthorizationGrantPreserved = true ∧
      b.boundary.selectedCandidateBoundToAuthorizationGrant = true ∧
      b.boundary.materializationAuthorizationGrantPreserved = true ∧
      b.boundary.materializationExecutionReceiptOnly = true ∧
      b.boundary.materializationAuthorizationGranted = true ∧
      b.boundary.materializationExecuted = true ∧
      b.boundary.activationAuthorizationGranted = false ∧
      b.boundary.actOSInvoked = false ∧
      b.boundary.externalCommit = false ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.receiptOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.grantPreservedRequired,
    b.boundary.receiptOnlyRequired, b.boundary.authorizationGrantedRequired,
    b.boundary.materializationExecutedRequired, b.boundary.activationForbidden,
    b.boundary.invocationForbidden, b.boundary.externalCommitForbidden,
    b.boundary.overwriteForbidden, b.boundary.blockerReleaseForbidden⟩

theorem history_appends_one_materialization_execution_receipt_record
    (b : PlanOSMaterializationExecutionReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSMaterializationExecutionReceiptBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSMaterializationExecutionReceiptBridge

end PlanOS
end KUOS
