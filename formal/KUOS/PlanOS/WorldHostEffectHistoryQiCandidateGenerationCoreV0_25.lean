import Mathlib
import KUOS.PlanOS.VacuumExpectationHistoryQiCandidateGenerationV0_19

namespace KUOS
namespace PlanOS

structure WorldDispositionGenerationBoundary where
  sourceDispositionPreserved : Bool
  governanceReviewPreserved : Bool
  worldCommitSeparate : Bool
  freshCommitAuthorizationRequired : Bool
  freshCommitAuthorizationSupplied : Bool
  atomicCommitReady : Bool
  generatedCandidateIsWorldDisposition : Bool
  generationResolvesWorldDisposition : Bool
  dispositionRequired : sourceDispositionPreserved = true
  governanceRequired : governanceReviewPreserved = true
  separateCommitRequired : worldCommitSeparate = true
  authorizationRequired : freshCommitAuthorizationRequired = true
  authorizationNotSupplied : freshCommitAuthorizationSupplied = false
  readinessForbidden : atomicCommitReady = false
  candidateDistinctionRequired : generatedCandidateIsWorldDisposition = false
  resolutionForbidden : generationResolvesWorldDisposition = false

structure CandidateGenerationReceiptBoundary where
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

theorem world_generation_preserves_disposition_candidate
    (boundary : WorldDispositionGenerationBoundary) :
    boundary.sourceDispositionPreserved = true ∧
      boundary.governanceReviewPreserved = true ∧
      boundary.worldCommitSeparate = true ∧
      boundary.freshCommitAuthorizationRequired = true ∧
      boundary.freshCommitAuthorizationSupplied = false ∧
      boundary.atomicCommitReady = false ∧
      boundary.generatedCandidateIsWorldDisposition = false ∧
      boundary.generationResolvesWorldDisposition = false := by
  exact ⟨boundary.dispositionRequired, boundary.governanceRequired,
    boundary.separateCommitRequired, boundary.authorizationRequired,
    boundary.authorizationNotSupplied, boundary.readinessForbidden,
    boundary.candidateDistinctionRequired, boundary.resolutionForbidden⟩

theorem generation_receipt_is_replay_safe
    (boundary : CandidateGenerationReceiptBoundary) :
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
