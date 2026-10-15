import Mathlib
import KUOS.PlanOS.DecisionOSSelectionReceiptIntakeV0_29

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS

structure SelectedCandidateSynthesisRequestSurface where
  sourceIntake : DecisionOSSelectionReceiptIntakeSurface
  sourceBoundary : DecisionOSSelectionReceiptIntakeBoundary
  sourceIntakeBound : Bool
  selectedCandidateBoundToIntake : Bool
  synthesisRequestOnly : Bool
  materializationGranted : Bool
  activationAuthorizationGranted : Bool
  executionGranted : Bool
  truthAuthorityGranted : Bool
  sourceRequired : sourceIntakeBound = true
  selectedBoundRequired : selectedCandidateBoundToIntake = true
  requestOnlyRequired : synthesisRequestOnly = true
  materializationForbidden : materializationGranted = false
  activationForbidden : activationAuthorizationGranted = false
  executionForbidden : executionGranted = false
  truthForbidden : truthAuthorityGranted = false

structure SelectedCandidateSynthesisRequestBoundary where
  requestOwnedByPlanOS : Bool
  sourceSelectionReceiptIntakePreserved : Bool
  selectedCandidateBoundToIntake : Bool
  synthesisRequestOnly : Bool
  materializationGranted : Bool
  actOSInvoked : Bool
  externalCommit : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  requestOwnerRequired : requestOwnedByPlanOS = true
  sourcePreservedRequired : sourceSelectionReceiptIntakePreserved = true
  selectedBoundRequired : selectedCandidateBoundToIntake = true
  requestOnlyRequired : synthesisRequestOnly = true
  materializationForbidden : materializationGranted = false
  invocationForbidden : actOSInvoked = false
  externalCommitForbidden : externalCommit = false
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSSelectedCandidateSynthesisRequestBridge where
  Digest : Type
  digestOf : SelectedCandidateSynthesisRequestSurface → SelectedCandidateSynthesisRequestBoundary → Nat → Digest
  surface : SelectedCandidateSynthesisRequestSurface
  boundary : SelectedCandidateSynthesisRequestBoundary
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

namespace PlanOSSelectedCandidateSynthesisRequestBridge

theorem source_intake_remains_receipt_intake_only
    (b : PlanOSSelectedCandidateSynthesisRequestBridge) :
    b.surface.sourceIntake.selectionReceiptIntakeOnly = true ∧
      b.surface.sourceIntake.selectedCandidateBoundToRequest = true ∧
      b.surface.sourceBoundary.selectionReceiptIntakeOnly = true ∧
      b.surface.sourceBoundary.selectedCandidateCommittedHere = false ∧
      b.surface.sourceBoundary.planSynthesisGranted = false := by
  exact ⟨b.surface.sourceIntake.intakeOnlyRequired,
    b.surface.sourceIntake.selectedBoundRequired,
    b.surface.sourceBoundary.intakeOnlyRequired,
    b.surface.sourceBoundary.selectionCommitForbidden,
    b.surface.sourceBoundary.synthesisForbidden⟩

theorem request_binds_selected_candidate_to_intake
    (b : PlanOSSelectedCandidateSynthesisRequestBridge) :
    b.surface.sourceIntakeBound = true ∧
      b.surface.selectedCandidateBoundToIntake = true ∧
      b.surface.synthesisRequestOnly = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.requestOnlyRequired⟩

theorem request_grants_no_materialization_activation_execution_or_truth
    (b : PlanOSSelectedCandidateSynthesisRequestBridge) :
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
    (b : PlanOSSelectedCandidateSynthesisRequestBridge) :
    b.boundary.requestOwnedByPlanOS = true ∧
      b.boundary.sourceSelectionReceiptIntakePreserved = true ∧
      b.boundary.selectedCandidateBoundToIntake = true ∧
      b.boundary.synthesisRequestOnly = true ∧
      b.boundary.materializationGranted = false ∧
      b.boundary.actOSInvoked = false ∧
      b.boundary.externalCommit = false ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.requestOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.requestOnlyRequired,
    b.boundary.materializationForbidden, b.boundary.invocationForbidden,
    b.boundary.externalCommitForbidden, b.boundary.overwriteForbidden,
    b.boundary.blockerReleaseForbidden⟩

theorem history_appends_one_synthesis_request_record
    (b : PlanOSSelectedCandidateSynthesisRequestBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSSelectedCandidateSynthesisRequestBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSSelectedCandidateSynthesisRequestBridge

end PlanOS
end KUOS
