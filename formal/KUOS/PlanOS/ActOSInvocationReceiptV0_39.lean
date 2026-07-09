import Mathlib
import KUOS.PlanOS.ActivationAuthorizationGrantV0_38

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS

structure ActOSInvocationReceiptSurface where
  sourceActivationGrant : ActivationAuthorizationGrantSurface
  sourceBoundary : ActivationAuthorizationGrantBoundary
  sourceActivationGrantBound : Bool
  selectedCandidateBoundToActivationGrant : Bool
  materializationExecutionPreserved : Bool
  activationAuthorizationPreserved : Bool
  actOSInvocationReceiptOnly : Bool
  materializationAuthorizationGranted : Bool
  materializationExecuted : Bool
  activationAuthorizationGranted : Bool
  actOSInvoked : Bool
  executionGranted : Bool
  truthAuthorityGranted : Bool
  sourceRequired : sourceActivationGrantBound = true
  selectedBoundRequired : selectedCandidateBoundToActivationGrant = true
  executionPreservedRequired : materializationExecutionPreserved = true
  activationPreservedRequired : activationAuthorizationPreserved = true
  receiptOnlyRequired : actOSInvocationReceiptOnly = true
  materializationAuthorizationGrantedRequired : materializationAuthorizationGranted = true
  materializationExecutedRequired : materializationExecuted = true
  activationAuthorizationGrantedRequired : activationAuthorizationGranted = true
  invocationRequired : actOSInvoked = true
  executionForbidden : executionGranted = false
  truthForbidden : truthAuthorityGranted = false

structure ActOSInvocationReceiptBoundary where
  receiptOwnedByPlanOS : Bool
  sourceActivationAuthorizationGrantPreserved : Bool
  selectedCandidateBoundToActivationGrant : Bool
  materializationExecutionPreserved : Bool
  activationAuthorizationPreserved : Bool
  actOSInvocationReceiptOnly : Bool
  materializationAuthorizationGranted : Bool
  materializationExecuted : Bool
  activationAuthorizationGranted : Bool
  actOSInvoked : Bool
  executionGranted : Bool
  externalCommit : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  receiptOwnerRequired : receiptOwnedByPlanOS = true
  sourcePreservedRequired : sourceActivationAuthorizationGrantPreserved = true
  selectedBoundRequired : selectedCandidateBoundToActivationGrant = true
  executionPreservedRequired : materializationExecutionPreserved = true
  activationPreservedRequired : activationAuthorizationPreserved = true
  receiptOnlyRequired : actOSInvocationReceiptOnly = true
  materializationAuthorizationGrantedRequired : materializationAuthorizationGranted = true
  materializationExecutedRequired : materializationExecuted = true
  activationAuthorizationGrantedRequired : activationAuthorizationGranted = true
  invocationRequired : actOSInvoked = true
  executionForbidden : executionGranted = false
  externalCommitForbidden : externalCommit = false
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSActOSInvocationReceiptBridge where
  Digest : Type
  digestOf : ActOSInvocationReceiptSurface → ActOSInvocationReceiptBoundary → Nat → Digest
  surface : ActOSInvocationReceiptSurface
  boundary : ActOSInvocationReceiptBoundary
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

namespace PlanOSActOSInvocationReceiptBridge

theorem source_activation_grant_authorizes_activation_only
    (b : PlanOSActOSInvocationReceiptBridge) :
    b.surface.sourceActivationGrant.activationAuthorizationGrantOnly = true ∧
      b.surface.sourceActivationGrant.materializationAuthorizationGranted = true ∧
      b.surface.sourceActivationGrant.materializationExecuted = true ∧
      b.surface.sourceActivationGrant.activationAuthorizationGranted = true ∧
      b.surface.sourceActivationGrant.actOSInvoked = false ∧
      b.surface.sourceBoundary.activationAuthorizationGrantOnly = true ∧
      b.surface.sourceBoundary.activationAuthorizationGranted = true ∧
      b.surface.sourceBoundary.actOSInvoked = false := by
  exact ⟨b.surface.sourceActivationGrant.grantOnlyRequired,
    b.surface.sourceActivationGrant.materializationAuthorizationGrantedRequired,
    b.surface.sourceActivationGrant.materializationExecutedRequired,
    b.surface.sourceActivationGrant.activationAuthorizationGrantedRequired,
    b.surface.sourceActivationGrant.invocationForbidden,
    b.surface.sourceBoundary.grantOnlyRequired,
    b.surface.sourceBoundary.activationAuthorizationGrantedRequired,
    b.surface.sourceBoundary.invocationForbidden⟩

theorem receipt_binds_selected_candidate_to_activation_grant
    (b : PlanOSActOSInvocationReceiptBridge) :
    b.surface.sourceActivationGrantBound = true ∧
      b.surface.selectedCandidateBoundToActivationGrant = true ∧
      b.surface.materializationExecutionPreserved = true ∧
      b.surface.activationAuthorizationPreserved = true ∧
      b.surface.actOSInvocationReceiptOnly = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.executionPreservedRequired, b.surface.activationPreservedRequired,
    b.surface.receiptOnlyRequired⟩

theorem receipt_records_invocation_but_not_execution_or_truth
    (b : PlanOSActOSInvocationReceiptBridge) :
    b.surface.materializationAuthorizationGranted = true ∧
      b.surface.materializationExecuted = true ∧
      b.surface.activationAuthorizationGranted = true ∧
      b.surface.actOSInvoked = true ∧
      b.surface.executionGranted = false ∧
      b.surface.truthAuthorityGranted = false ∧
      b.nonAuthority.executionGranted = false ∧
      b.nonAuthority.truthAuthority = false := by
  exact ⟨b.surface.materializationAuthorizationGrantedRequired,
    b.surface.materializationExecutedRequired,
    b.surface.activationAuthorizationGrantedRequired,
    b.surface.invocationRequired, b.surface.executionForbidden,
    b.surface.truthForbidden, b.executionForbidden, b.truthForbidden⟩

theorem boundary_blocks_execution_commit_memory_and_blocker_release
    (b : PlanOSActOSInvocationReceiptBridge) :
    b.boundary.receiptOwnedByPlanOS = true ∧
      b.boundary.sourceActivationAuthorizationGrantPreserved = true ∧
      b.boundary.selectedCandidateBoundToActivationGrant = true ∧
      b.boundary.materializationExecutionPreserved = true ∧
      b.boundary.activationAuthorizationPreserved = true ∧
      b.boundary.actOSInvocationReceiptOnly = true ∧
      b.boundary.materializationAuthorizationGranted = true ∧
      b.boundary.materializationExecuted = true ∧
      b.boundary.activationAuthorizationGranted = true ∧
      b.boundary.actOSInvoked = true ∧
      b.boundary.executionGranted = false ∧
      b.boundary.externalCommit = false ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.receiptOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.executionPreservedRequired,
    b.boundary.activationPreservedRequired, b.boundary.receiptOnlyRequired,
    b.boundary.materializationAuthorizationGrantedRequired,
    b.boundary.materializationExecutedRequired,
    b.boundary.activationAuthorizationGrantedRequired,
    b.boundary.invocationRequired, b.boundary.executionForbidden,
    b.boundary.externalCommitForbidden, b.boundary.overwriteForbidden,
    b.boundary.blockerReleaseForbidden⟩

theorem history_appends_one_actos_invocation_receipt_record
    (b : PlanOSActOSInvocationReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSActOSInvocationReceiptBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSActOSInvocationReceiptBridge

end PlanOS
end KUOS
