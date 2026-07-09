import Mathlib
import KUOS.PlanOS.DecisionOSSelectionRequestV0_28

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS

structure DecisionOSSelectionReceiptIntakeSurface where
  sourceRequest : DecisionOSSelectionRequestSurface
  sourceBoundary : DecisionOSSelectionRequestBoundary
  sourceRequestBound : Bool
  decisionOSSelectionReceiptBound : Bool
  selectedCandidateBoundToRequest : Bool
  selectionReceiptIntakeOnly : Bool
  selectionReceiptOwnedByDecisionOS : Bool
  selectedCandidateCommittedHere : Bool
  planSynthesisGranted : Bool
  activationAuthorizationGranted : Bool
  executionGranted : Bool
  truthAuthorityGranted : Bool
  sourceRequired : sourceRequestBound = true
  decisionReceiptRequired : decisionOSSelectionReceiptBound = true
  selectedBoundRequired : selectedCandidateBoundToRequest = true
  intakeOnlyRequired : selectionReceiptIntakeOnly = true
  decisionOwnerRequired : selectionReceiptOwnedByDecisionOS = true
  selectedCommitForbidden : selectedCandidateCommittedHere = false
  synthesisForbidden : planSynthesisGranted = false
  activationForbidden : activationAuthorizationGranted = false
  executionForbidden : executionGranted = false
  truthForbidden : truthAuthorityGranted = false

structure DecisionOSSelectionReceiptIntakeBoundary where
  intakeOwnedByPlanOS : Bool
  selectionReceiptOwnedByDecisionOS : Bool
  selectionReceiptIntakeOnly : Bool
  selectedCandidateBoundToRequest : Bool
  selectedCandidateCommittedHere : Bool
  planSynthesisGranted : Bool
  actOSInvoked : Bool
  externalCommit : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  intakeOwnerRequired : intakeOwnedByPlanOS = true
  receiptOwnerRequired : selectionReceiptOwnedByDecisionOS = true
  intakeOnlyRequired : selectionReceiptIntakeOnly = true
  selectedBoundRequired : selectedCandidateBoundToRequest = true
  selectionCommitForbidden : selectedCandidateCommittedHere = false
  synthesisForbidden : planSynthesisGranted = false
  invocationForbidden : actOSInvoked = false
  externalCommitForbidden : externalCommit = false
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSDecisionOSSelectionReceiptIntakeBridge where
  Digest : Type
  digestOf : DecisionOSSelectionReceiptIntakeSurface → DecisionOSSelectionReceiptIntakeBoundary → Nat → Digest
  surface : DecisionOSSelectionReceiptIntakeSurface
  boundary : DecisionOSSelectionReceiptIntakeBoundary
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

namespace PlanOSDecisionOSSelectionReceiptIntakeBridge

theorem source_request_remains_selection_request_only
    (b : PlanOSDecisionOSSelectionReceiptIntakeBridge) :
    b.surface.sourceRequest.selectionRequestOnly = true ∧
      b.surface.sourceRequest.selectionOwnedByDecisionOS = true ∧
      b.surface.sourceBoundary.selectionRequestOnly = true ∧
      b.surface.sourceBoundary.candidateSelectionAuthorityGranted = false ∧
      b.surface.sourceBoundary.selectedCandidateCommitted = false := by
  exact ⟨b.surface.sourceRequest.requestOnlyRequired,
    b.surface.sourceRequest.decisionOwnerRequired,
    b.surface.sourceBoundary.requestOnlyRequired,
    b.surface.sourceBoundary.selectionAuthorityForbidden,
    b.surface.sourceBoundary.selectionCommitForbidden⟩

theorem intake_binds_decisionos_selection_to_request
    (b : PlanOSDecisionOSSelectionReceiptIntakeBridge) :
    b.surface.sourceRequestBound = true ∧
      b.surface.decisionOSSelectionReceiptBound = true ∧
      b.surface.selectedCandidateBoundToRequest = true ∧
      b.surface.selectionReceiptIntakeOnly = true ∧
      b.surface.selectionReceiptOwnedByDecisionOS = true := by
  exact ⟨b.surface.sourceRequired, b.surface.decisionReceiptRequired,
    b.surface.selectedBoundRequired, b.surface.intakeOnlyRequired,
    b.surface.decisionOwnerRequired⟩

theorem intake_grants_no_commit_synthesis_activation_execution_or_truth
    (b : PlanOSDecisionOSSelectionReceiptIntakeBridge) :
    b.surface.selectedCandidateCommittedHere = false ∧
      b.surface.planSynthesisGranted = false ∧
      b.surface.activationAuthorizationGranted = false ∧
      b.surface.executionGranted = false ∧
      b.surface.truthAuthorityGranted = false ∧
      b.nonAuthority.executionGranted = false ∧
      b.nonAuthority.truthAuthority = false := by
  exact ⟨b.surface.selectedCommitForbidden, b.surface.synthesisForbidden,
    b.surface.activationForbidden, b.surface.executionForbidden,
    b.surface.truthForbidden, b.executionForbidden, b.truthForbidden⟩

theorem boundary_blocks_plan_synthesis_commit_memory_and_blocker_release
    (b : PlanOSDecisionOSSelectionReceiptIntakeBridge) :
    b.boundary.intakeOwnedByPlanOS = true ∧
      b.boundary.selectionReceiptOwnedByDecisionOS = true ∧
      b.boundary.selectionReceiptIntakeOnly = true ∧
      b.boundary.selectedCandidateBoundToRequest = true ∧
      b.boundary.selectedCandidateCommittedHere = false ∧
      b.boundary.planSynthesisGranted = false ∧
      b.boundary.actOSInvoked = false ∧
      b.boundary.externalCommit = false ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.intakeOwnerRequired, b.boundary.receiptOwnerRequired,
    b.boundary.intakeOnlyRequired, b.boundary.selectedBoundRequired,
    b.boundary.selectionCommitForbidden, b.boundary.synthesisForbidden,
    b.boundary.invocationForbidden, b.boundary.externalCommitForbidden,
    b.boundary.overwriteForbidden, b.boundary.blockerReleaseForbidden⟩

theorem history_appends_one_selection_receipt_intake_record
    (b : PlanOSDecisionOSSelectionReceiptIntakeBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSDecisionOSSelectionReceiptIntakeBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSDecisionOSSelectionReceiptIntakeBridge

end PlanOS
end KUOS
