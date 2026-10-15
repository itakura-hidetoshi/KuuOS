import Mathlib
import KUOS.PlanOS.SelectedCandidateSynthesisRequestV0_30

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS

structure SelectedCandidateSynthesisReceiptSurface where
  sourceRequest : SelectedCandidateSynthesisRequestSurface
  sourceBoundary : SelectedCandidateSynthesisRequestBoundary
  sourceRequestBound : Bool
  selectedCandidateBoundToRequest : Bool
  synthesisReceiptOnly : Bool
  materializationGranted : Bool
  activationAuthorizationGranted : Bool
  executionGranted : Bool
  truthAuthorityGranted : Bool
  sourceRequired : sourceRequestBound = true
  selectedBoundRequired : selectedCandidateBoundToRequest = true
  receiptOnlyRequired : synthesisReceiptOnly = true
  materializationForbidden : materializationGranted = false
  activationForbidden : activationAuthorizationGranted = false
  executionForbidden : executionGranted = false
  truthForbidden : truthAuthorityGranted = false

structure SelectedCandidateSynthesisReceiptBoundary where
  receiptOwnedByPlanOS : Bool
  sourceSynthesisRequestPreserved : Bool
  selectedCandidateBoundToRequest : Bool
  synthesisReceiptOnly : Bool
  materializationGranted : Bool
  actOSInvoked : Bool
  externalCommit : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  receiptOwnerRequired : receiptOwnedByPlanOS = true
  sourcePreservedRequired : sourceSynthesisRequestPreserved = true
  selectedBoundRequired : selectedCandidateBoundToRequest = true
  receiptOnlyRequired : synthesisReceiptOnly = true
  materializationForbidden : materializationGranted = false
  invocationForbidden : actOSInvoked = false
  externalCommitForbidden : externalCommit = false
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSSelectedCandidateSynthesisReceiptBridge where
  Digest : Type
  digestOf : SelectedCandidateSynthesisReceiptSurface → SelectedCandidateSynthesisReceiptBoundary → Nat → Digest
  surface : SelectedCandidateSynthesisReceiptSurface
  boundary : SelectedCandidateSynthesisReceiptBoundary
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

namespace PlanOSSelectedCandidateSynthesisReceiptBridge

theorem source_request_remains_synthesis_request_only
    (b : PlanOSSelectedCandidateSynthesisReceiptBridge) :
    b.surface.sourceRequest.synthesisRequestOnly = true ∧
      b.surface.sourceRequest.selectedCandidateBoundToIntake = true ∧
      b.surface.sourceBoundary.synthesisRequestOnly = true ∧
      b.surface.sourceBoundary.materializationGranted = false ∧
      b.surface.sourceBoundary.actOSInvoked = false := by
  exact ⟨b.surface.sourceRequest.requestOnlyRequired,
    b.surface.sourceRequest.selectedBoundRequired,
    b.surface.sourceBoundary.requestOnlyRequired,
    b.surface.sourceBoundary.materializationForbidden,
    b.surface.sourceBoundary.invocationForbidden⟩

theorem receipt_binds_selected_candidate_to_request
    (b : PlanOSSelectedCandidateSynthesisReceiptBridge) :
    b.surface.sourceRequestBound = true ∧
      b.surface.selectedCandidateBoundToRequest = true ∧
      b.surface.synthesisReceiptOnly = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.receiptOnlyRequired⟩

theorem receipt_grants_no_materialization_activation_execution_or_truth
    (b : PlanOSSelectedCandidateSynthesisReceiptBridge) :
    b.surface.materializationGranted = false ∧
      b.surface.activationAuthorizationGranted = false ∧
      b.surface.executionGranted = false ∧
      b.surface.truthAuthorityGranted = false ∧
      b.nonAuthority.executionGranted = false ∧
      b.nonAuthority.truthAuthority = false := by
  exact ⟨b.surface.materializationForbidden, b.surface.activationForbidden,
    b.surface.executionForbidden, b.surface.truthForbidden,
    b.executionForbidden, b.truthForbidden⟩

theorem boundary_blocks_materialization_commit_memory_and_blocker_release
    (b : PlanOSSelectedCandidateSynthesisReceiptBridge) :
    b.boundary.receiptOwnedByPlanOS = true ∧
      b.boundary.sourceSynthesisRequestPreserved = true ∧
      b.boundary.selectedCandidateBoundToRequest = true ∧
      b.boundary.synthesisReceiptOnly = true ∧
      b.boundary.materializationGranted = false ∧
      b.boundary.actOSInvoked = false ∧
      b.boundary.externalCommit = false ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.receiptOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.receiptOnlyRequired,
    b.boundary.materializationForbidden, b.boundary.invocationForbidden,
    b.boundary.externalCommitForbidden, b.boundary.overwriteForbidden,
    b.boundary.blockerReleaseForbidden⟩

theorem history_appends_one_synthesis_receipt_record
    (b : PlanOSSelectedCandidateSynthesisReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSSelectedCandidateSynthesisReceiptBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSSelectedCandidateSynthesisReceiptBridge

end PlanOS
end KUOS
