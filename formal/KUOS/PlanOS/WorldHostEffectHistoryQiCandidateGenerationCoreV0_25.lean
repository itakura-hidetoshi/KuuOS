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

end PlanOS
end KUOS
