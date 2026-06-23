import Mathlib
import KUOS.DecisionOS.VacuumExpectationAdmissibleCandidateSelectionV0_4

namespace KUOS
namespace DecisionOS

structure WorldDispositionSelectionBoundary where
  sourceDispositionPreserved : Bool
  governanceReviewPreserved : Bool
  worldCommitSeparate : Bool
  freshCommitAuthorizationRequired : Bool
  freshCommitAuthorizationSupplied : Bool
  atomicCommitReady : Bool
  selectedReplanCandidateIsWorldDisposition : Bool
  selectionResolvesWorldDisposition : Bool
  dispositionRequired : sourceDispositionPreserved = true
  governanceRequired : governanceReviewPreserved = true
  separateCommitRequired : worldCommitSeparate = true
  authorizationRequired : freshCommitAuthorizationRequired = true
  authorizationNotSupplied : freshCommitAuthorizationSupplied = false
  readinessForbidden : atomicCommitReady = false
  candidateDistinctionRequired : selectedReplanCandidateIsWorldDisposition = false
  resolutionForbidden : selectionResolvesWorldDisposition = false

structure DecisionSelectionReceiptBoundary where
  receiptCommitted : Bool
  receiptImmutable : Bool
  appendOnly : Bool
  exactReplayIdempotent : Bool
  conflictingReplayAccepted : Bool
  receiptRequired : receiptCommitted = true
  immutableRequired : receiptImmutable = true
  appendOnlyRequired : appendOnly = true
  replayRequired : exactReplayIdempotent = true
  conflictingReplayForbidden : conflictingReplayAccepted = false

theorem selection_preserves_world_disposition
    (boundary : WorldDispositionSelectionBoundary) :
    boundary.sourceDispositionPreserved = true ∧
      boundary.governanceReviewPreserved = true ∧
      boundary.worldCommitSeparate = true ∧
      boundary.freshCommitAuthorizationRequired = true ∧
      boundary.freshCommitAuthorizationSupplied = false ∧
      boundary.atomicCommitReady = false ∧
      boundary.selectedReplanCandidateIsWorldDisposition = false ∧
      boundary.selectionResolvesWorldDisposition = false := by
  exact ⟨boundary.dispositionRequired, boundary.governanceRequired,
    boundary.separateCommitRequired, boundary.authorizationRequired,
    boundary.authorizationNotSupplied, boundary.readinessForbidden,
    boundary.candidateDistinctionRequired, boundary.resolutionForbidden⟩

theorem decision_selection_receipt_is_replay_safe
    (boundary : DecisionSelectionReceiptBoundary) :
    boundary.receiptCommitted = true ∧
      boundary.receiptImmutable = true ∧
      boundary.appendOnly = true ∧
      boundary.exactReplayIdempotent = true ∧
      boundary.conflictingReplayAccepted = false := by
  exact ⟨boundary.receiptRequired, boundary.immutableRequired,
    boundary.appendOnlyRequired, boundary.replayRequired,
    boundary.conflictingReplayForbidden⟩

end DecisionOS
end KUOS
