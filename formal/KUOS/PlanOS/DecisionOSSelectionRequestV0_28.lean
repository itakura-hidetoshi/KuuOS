import Mathlib
import KUOS.PlanOS.DecisionReviewIntakeV0_27

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS

structure DecisionOSSelectionRequestSurface where
  sourceIntake : DecisionReviewIntakeSurface
  sourceBoundary : DecisionReviewIntakeBoundary
  sourceIntakeBound : Bool
  selectionRequestOnly : Bool
  requestedCandidateIdsBound : Bool
  probeCandidatesMarked : Bool
  barrierCandidatesExcluded : Bool
  selectionOwnedByDecisionOS : Bool
  selectableByPlanOSHere : Bool
  selectedCandidateCommitted : Bool
  decisionMade : Bool
  decisionReceiptIssued : Bool
  activationAuthorizationGranted : Bool
  executionGranted : Bool
  truthAuthorityGranted : Bool
  sourceRequired : sourceIntakeBound = true
  requestOnlyRequired : selectionRequestOnly = true
  requestedIdsRequired : requestedCandidateIdsBound = true
  probeMarkedRequired : probeCandidatesMarked = true
  barrierExcludedRequired : barrierCandidatesExcluded = true
  decisionOwnerRequired : selectionOwnedByDecisionOS = true
  planSelectionForbidden : selectableByPlanOSHere = false
  selectionCommitForbidden : selectedCandidateCommitted = false
  decisionForbidden : decisionMade = false
  decisionReceiptForbidden : decisionReceiptIssued = false
  activationForbidden : activationAuthorizationGranted = false
  executionForbidden : executionGranted = false
  truthForbidden : truthAuthorityGranted = false

structure DecisionOSSelectionRequestBoundary where
  requestOwnedByPlanOS : Bool
  selectionOwnedByDecisionOS : Bool
  selectionRequestOnly : Bool
  reviewIntakePreserved : Bool
  probeCandidatesMarkedNotSelected : Bool
  barrierCandidatesExcluded : Bool
  candidateSelectionAuthorityGranted : Bool
  selectedCandidateCommitted : Bool
  decisionReceiptIssued : Bool
  actOSInvoked : Bool
  externalCommit : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  requestOwnerRequired : requestOwnedByPlanOS = true
  decisionOwnerRequired : selectionOwnedByDecisionOS = true
  requestOnlyRequired : selectionRequestOnly = true
  reviewPreservedRequired : reviewIntakePreserved = true
  probeMarkedRequired : probeCandidatesMarkedNotSelected = true
  barrierExcludedRequired : barrierCandidatesExcluded = true
  selectionAuthorityForbidden : candidateSelectionAuthorityGranted = false
  selectionCommitForbidden : selectedCandidateCommitted = false
  decisionReceiptForbidden : decisionReceiptIssued = false
  invocationForbidden : actOSInvoked = false
  externalCommitForbidden : externalCommit = false
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSDecisionOSSelectionRequestBridge where
  Digest : Type
  digestOf : DecisionOSSelectionRequestSurface → DecisionOSSelectionRequestBoundary → Nat → Digest
  surface : DecisionOSSelectionRequestSurface
  boundary : DecisionOSSelectionRequestBoundary
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

namespace PlanOSDecisionOSSelectionRequestBridge

theorem source_intake_remains_review_input_only (b : PlanOSDecisionOSSelectionRequestBridge) :
    b.surface.sourceIntake.decisionReviewInputOnly = true ∧
      b.surface.sourceIntake.reviewOwnedByDecisionOS = true ∧
      b.surface.sourceBoundary.decisionReviewInputOnly = true ∧
      b.surface.sourceBoundary.selectedCandidateCommitted = false ∧
      b.surface.sourceBoundary.decisionReceiptIssued = false := by
  exact ⟨b.surface.sourceIntake.inputOnlyRequired,
    b.surface.sourceIntake.decisionOwnerRequired,
    b.surface.sourceBoundary.inputOnlyRequired,
    b.surface.sourceBoundary.selectionCommitForbidden,
    b.surface.sourceBoundary.decisionReceiptForbidden⟩

theorem request_is_selection_request_only (b : PlanOSDecisionOSSelectionRequestBridge) :
    b.surface.sourceIntakeBound = true ∧
      b.surface.selectionRequestOnly = true ∧
      b.surface.requestedCandidateIdsBound = true ∧
      b.surface.probeCandidatesMarked = true ∧
      b.surface.barrierCandidatesExcluded = true ∧
      b.surface.selectionOwnedByDecisionOS = true := by
  exact ⟨b.surface.sourceRequired, b.surface.requestOnlyRequired,
    b.surface.requestedIdsRequired, b.surface.probeMarkedRequired,
    b.surface.barrierExcludedRequired, b.surface.decisionOwnerRequired⟩

theorem request_grants_no_selection_decision_activation_execution_or_truth
    (b : PlanOSDecisionOSSelectionRequestBridge) :
    b.surface.selectableByPlanOSHere = false ∧
      b.surface.selectedCandidateCommitted = false ∧
      b.surface.decisionMade = false ∧
      b.surface.decisionReceiptIssued = false ∧
      b.surface.activationAuthorizationGranted = false ∧
      b.surface.executionGranted = false ∧
      b.surface.truthAuthorityGranted = false ∧
      b.nonAuthority.executionGranted = false ∧
      b.nonAuthority.truthAuthority = false := by
  exact ⟨b.surface.planSelectionForbidden, b.surface.selectionCommitForbidden,
    b.surface.decisionForbidden, b.surface.decisionReceiptForbidden,
    b.surface.activationForbidden, b.surface.executionForbidden,
    b.surface.truthForbidden, b.executionForbidden, b.truthForbidden⟩

theorem boundary_blocks_commit_memory_and_blocker_release
    (b : PlanOSDecisionOSSelectionRequestBridge) :
    b.boundary.requestOwnedByPlanOS = true ∧
      b.boundary.selectionOwnedByDecisionOS = true ∧
      b.boundary.selectionRequestOnly = true ∧
      b.boundary.reviewIntakePreserved = true ∧
      b.boundary.probeCandidatesMarkedNotSelected = true ∧
      b.boundary.barrierCandidatesExcluded = true ∧
      b.boundary.candidateSelectionAuthorityGranted = false ∧
      b.boundary.selectedCandidateCommitted = false ∧
      b.boundary.decisionReceiptIssued = false ∧
      b.boundary.actOSInvoked = false ∧
      b.boundary.externalCommit = false ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.requestOwnerRequired, b.boundary.decisionOwnerRequired,
    b.boundary.requestOnlyRequired, b.boundary.reviewPreservedRequired,
    b.boundary.probeMarkedRequired, b.boundary.barrierExcludedRequired,
    b.boundary.selectionAuthorityForbidden, b.boundary.selectionCommitForbidden,
    b.boundary.decisionReceiptForbidden, b.boundary.invocationForbidden,
    b.boundary.externalCommitForbidden, b.boundary.overwriteForbidden,
    b.boundary.blockerReleaseForbidden⟩

theorem history_appends_one_selection_request_record (b : PlanOSDecisionOSSelectionRequestBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSDecisionOSSelectionRequestBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSDecisionOSSelectionRequestBridge

end PlanOS
end KUOS
