import Mathlib
import KUOS.PlanOS.SelectedCandidateSynthesisReceiptV0_31

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS

structure SelectedCandidateMaterializationPreflightSurface where
  sourceReceipt : SelectedCandidateSynthesisReceiptSurface
  sourceBoundary : SelectedCandidateSynthesisReceiptBoundary
  sourceReceiptBound : Bool
  selectedCandidateBoundToSynthesisReceipt : Bool
  materializationPreflightOnly : Bool
  materializationAuthorizationGranted : Bool
  materializationExecuted : Bool
  activationAuthorizationGranted : Bool
  executionGranted : Bool
  truthAuthorityGranted : Bool
  sourceRequired : sourceReceiptBound = true
  selectedBoundRequired : selectedCandidateBoundToSynthesisReceipt = true
  preflightOnlyRequired : materializationPreflightOnly = true
  materializationAuthorizationForbidden : materializationAuthorizationGranted = false
  materializationExecutionForbidden : materializationExecuted = false
  activationForbidden : activationAuthorizationGranted = false
  executionForbidden : executionGranted = false
  truthForbidden : truthAuthorityGranted = false

structure SelectedCandidateMaterializationPreflightBoundary where
  preflightOwnedByPlanOS : Bool
  sourceSynthesisReceiptPreserved : Bool
  selectedCandidateBoundToSynthesisReceipt : Bool
  materializationPreflightOnly : Bool
  materializationAuthorizationGranted : Bool
  materializationExecuted : Bool
  actOSInvoked : Bool
  externalCommit : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  preflightOwnerRequired : preflightOwnedByPlanOS = true
  sourcePreservedRequired : sourceSynthesisReceiptPreserved = true
  selectedBoundRequired : selectedCandidateBoundToSynthesisReceipt = true
  preflightOnlyRequired : materializationPreflightOnly = true
  materializationAuthorizationForbidden : materializationAuthorizationGranted = false
  materializationExecutionForbidden : materializationExecuted = false
  invocationForbidden : actOSInvoked = false
  externalCommitForbidden : externalCommit = false
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSSelectedCandidateMaterializationPreflightBridge where
  Digest : Type
  digestOf : SelectedCandidateMaterializationPreflightSurface → SelectedCandidateMaterializationPreflightBoundary → Nat → Digest
  surface : SelectedCandidateMaterializationPreflightSurface
  boundary : SelectedCandidateMaterializationPreflightBoundary
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

namespace PlanOSSelectedCandidateMaterializationPreflightBridge

theorem source_receipt_remains_synthesis_receipt_only
    (b : PlanOSSelectedCandidateMaterializationPreflightBridge) :
    b.surface.sourceReceipt.synthesisReceiptOnly = true ∧
      b.surface.sourceReceipt.selectedCandidateBoundToRequest = true ∧
      b.surface.sourceBoundary.synthesisReceiptOnly = true ∧
      b.surface.sourceBoundary.materializationGranted = false := by
  exact ⟨b.surface.sourceReceipt.receiptOnlyRequired,
    b.surface.sourceReceipt.selectedBoundRequired,
    b.surface.sourceBoundary.receiptOnlyRequired,
    b.surface.sourceBoundary.materializationForbidden⟩

theorem preflight_binds_selected_candidate_to_synthesis_receipt
    (b : PlanOSSelectedCandidateMaterializationPreflightBridge) :
    b.surface.sourceReceiptBound = true ∧
      b.surface.selectedCandidateBoundToSynthesisReceipt = true ∧
      b.surface.materializationPreflightOnly = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.preflightOnlyRequired⟩

theorem preflight_grants_no_materialization_activation_execution_or_truth
    (b : PlanOSSelectedCandidateMaterializationPreflightBridge) :
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
    (b : PlanOSSelectedCandidateMaterializationPreflightBridge) :
    b.boundary.preflightOwnedByPlanOS = true ∧
      b.boundary.sourceSynthesisReceiptPreserved = true ∧
      b.boundary.selectedCandidateBoundToSynthesisReceipt = true ∧
      b.boundary.materializationPreflightOnly = true ∧
      b.boundary.materializationAuthorizationGranted = false ∧
      b.boundary.materializationExecuted = false ∧
      b.boundary.actOSInvoked = false ∧
      b.boundary.externalCommit = false ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.preflightOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.preflightOnlyRequired,
    b.boundary.materializationAuthorizationForbidden,
    b.boundary.materializationExecutionForbidden,
    b.boundary.invocationForbidden, b.boundary.externalCommitForbidden,
    b.boundary.overwriteForbidden, b.boundary.blockerReleaseForbidden⟩

theorem history_appends_one_materialization_preflight_record
    (b : PlanOSSelectedCandidateMaterializationPreflightBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSSelectedCandidateMaterializationPreflightBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSSelectedCandidateMaterializationPreflightBridge

end PlanOS
end KUOS
