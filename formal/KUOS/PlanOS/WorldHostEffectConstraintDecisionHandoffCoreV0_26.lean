import Mathlib
import KUOS.PlanOS.VacuumExpectationHysteresisConstraintDecisionHandoffV0_20

namespace KUOS
namespace PlanOS

structure WorldDispositionConstraintBoundary where
  sourceDispositionPreserved : Bool
  governanceReviewPreserved : Bool
  worldCommitSeparate : Bool
  freshCommitAuthorizationRequired : Bool
  freshCommitAuthorizationSupplied : Bool
  atomicCommitReady : Bool
  forwardedCandidateIsWorldDisposition : Bool
  handoffResolvesWorldDisposition : Bool
  dispositionRequired : sourceDispositionPreserved = true
  governanceRequired : governanceReviewPreserved = true
  separateCommitRequired : worldCommitSeparate = true
  authorizationRequired : freshCommitAuthorizationRequired = true
  authorizationNotSupplied : freshCommitAuthorizationSupplied = false
  readinessForbidden : atomicCommitReady = false
  candidateDistinctionRequired : forwardedCandidateIsWorldDisposition = false
  resolutionForbidden : handoffResolvesWorldDisposition = false

structure ConstraintHandoffReceiptBoundary where
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

theorem constraint_handoff_preserves_world_disposition
    (boundary : WorldDispositionConstraintBoundary) :
    boundary.sourceDispositionPreserved = true ∧
      boundary.governanceReviewPreserved = true ∧
      boundary.worldCommitSeparate = true ∧
      boundary.freshCommitAuthorizationRequired = true ∧
      boundary.freshCommitAuthorizationSupplied = false ∧
      boundary.atomicCommitReady = false ∧
      boundary.forwardedCandidateIsWorldDisposition = false ∧
      boundary.handoffResolvesWorldDisposition = false := by
  exact ⟨boundary.dispositionRequired, boundary.governanceRequired,
    boundary.separateCommitRequired, boundary.authorizationRequired,
    boundary.authorizationNotSupplied, boundary.readinessForbidden,
    boundary.candidateDistinctionRequired, boundary.resolutionForbidden⟩

theorem constraint_handoff_receipt_is_replay_safe
    (boundary : ConstraintHandoffReceiptBoundary) :
    boundary.receiptCommitted = true ∧
      boundary.receiptImmutable = true ∧
      boundary.appendOnly = true ∧
      boundary.exactReplayIdempotent = true ∧
      boundary.conflictingReplayAccepted = false := by
  exact ⟨boundary.receiptRequired, boundary.immutableRequired,
    boundary.appendOnlyRequired, boundary.replayRequired,
    boundary.conflictingReplayForbidden⟩

end PlanOS
end KUOS
