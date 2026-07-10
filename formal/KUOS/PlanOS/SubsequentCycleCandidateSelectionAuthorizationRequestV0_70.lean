import Mathlib
import KUOS.PlanOS.SubsequentCycleCandidateReviewReceiptV0_69

namespace KUOS
namespace PlanOS

structure SubsequentCycleCandidateSelectionAuthorizationRequestSurface where
  sourceReview : SubsequentCycleCandidateReviewReceiptSurface
  sourceReviewBoundary : SubsequentCycleCandidateReviewReceiptBoundary
  sourceReviewBound : Bool
  candidateSetDigestPreserved : Bool
  evaluationSetDigestPreserved : Bool
  reviewSetDigestPreserved : Bool
  candidateReviewCompletedPreserved : Bool
  selectionEligibilityPreserved : Bool
  reviewOrderIsNotSelectionPreserved : Bool
  selectionEligibleCount : Nat
  authorizationScopeBound : Bool
  authorizationConstraintsDigestBound : Bool
  subsequentCycleCandidateSelectionAuthorizationRequestOnly : Bool
  subsequentCycleCandidateSelectionAuthorizationRequested : Bool
  subsequentCycleSelectionAuthorityGranted : Bool
  subsequentCycleCandidateSelectionRequested : Bool
  subsequentCycleCandidateSelected : Bool
  subsequentCycleAdmissionRequested : Bool
  sourceRequired : sourceReviewBound = true
  candidateSetRequired : candidateSetDigestPreserved = true
  evaluationSetRequired : evaluationSetDigestPreserved = true
  reviewSetRequired : reviewSetDigestPreserved = true
  reviewCompletedRequired : candidateReviewCompletedPreserved = true
  eligibilityRequired : selectionEligibilityPreserved = true
  reviewOrderRequired : reviewOrderIsNotSelectionPreserved = true
  eligiblePositive : 0 < selectionEligibleCount
  authorizationScopeRequired : authorizationScopeBound = true
  authorizationConstraintsRequired : authorizationConstraintsDigestBound = true
  requestOnlyRequired : subsequentCycleCandidateSelectionAuthorizationRequestOnly = true
  authorizationRequestedRequired : subsequentCycleCandidateSelectionAuthorizationRequested = true
  authorityForbidden : subsequentCycleSelectionAuthorityGranted = false
  selectionRequestForbidden : subsequentCycleCandidateSelectionRequested = false
  candidateSelectionForbidden : subsequentCycleCandidateSelected = false
  admissionRequestForbidden : subsequentCycleAdmissionRequested = false

structure SubsequentCycleCandidateSelectionAuthorizationRequestBoundary where
  requestOwnedByPlanOS : Bool
  sourceCandidateReviewReceiptPreserved : Bool
  candidateReviewCompletedPreserved : Bool
  selectionEligibilityPreserved : Bool
  reviewOrderIsNotSelectionPreserved : Bool
  subsequentCycleCandidateSelectionAuthorizationRequestOnly : Bool
  subsequentCycleCandidateSelectionAuthorizationRequested : Bool
  subsequentCycleSelectionAuthorityGranted : Bool
  subsequentCycleCandidateSelectionRequested : Bool
  subsequentCycleCandidateSelected : Bool
  subsequentCycleAdmissionRequested : Bool
  ownerRequired : requestOwnedByPlanOS = true
  sourceRequired : sourceCandidateReviewReceiptPreserved = true
  reviewCompletedRequired : candidateReviewCompletedPreserved = true
  eligibilityRequired : selectionEligibilityPreserved = true
  reviewOrderRequired : reviewOrderIsNotSelectionPreserved = true
  requestOnlyRequired : subsequentCycleCandidateSelectionAuthorizationRequestOnly = true
  authorizationRequestedRequired : subsequentCycleCandidateSelectionAuthorizationRequested = true
  authorityForbidden : subsequentCycleSelectionAuthorityGranted = false
  selectionRequestForbidden : subsequentCycleCandidateSelectionRequested = false
  candidateSelectionForbidden : subsequentCycleCandidateSelected = false
  admissionRequestForbidden : subsequentCycleAdmissionRequested = false

structure PlanOSSubsequentCycleCandidateSelectionAuthorizationRequestBridge where
  surface : SubsequentCycleCandidateSelectionAuthorizationRequestSurface
  boundary : SubsequentCycleCandidateSelectionAuthorizationRequestBoundary
  historyDelta : Nat
  historyDeltaRequired : historyDelta = 1

namespace PlanOSSubsequentCycleCandidateSelectionAuthorizationRequestBridge

 theorem request_is_bounded_and_nonselective
    (b : PlanOSSubsequentCycleCandidateSelectionAuthorizationRequestBridge) :
    b.surface.sourceReviewBound = true ∧
    b.surface.candidateReviewCompletedPreserved = true ∧
    b.surface.selectionEligibilityPreserved = true ∧
    b.surface.reviewOrderIsNotSelectionPreserved = true ∧
    0 < b.surface.selectionEligibleCount ∧
    b.surface.subsequentCycleCandidateSelectionAuthorizationRequested = true ∧
    b.surface.subsequentCycleSelectionAuthorityGranted = false ∧
    b.surface.subsequentCycleCandidateSelectionRequested = false ∧
    b.surface.subsequentCycleCandidateSelected = false ∧
    b.surface.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.surface.sourceRequired, b.surface.reviewCompletedRequired,
    b.surface.eligibilityRequired, b.surface.reviewOrderRequired,
    b.surface.eligiblePositive, b.surface.authorizationRequestedRequired,
    b.surface.authorityForbidden, b.surface.selectionRequestForbidden,
    b.surface.candidateSelectionForbidden, b.surface.admissionRequestForbidden⟩

 theorem boundary_is_authorization_request_only
    (b : PlanOSSubsequentCycleCandidateSelectionAuthorizationRequestBridge) :
    b.boundary.requestOwnedByPlanOS = true ∧
    b.boundary.sourceCandidateReviewReceiptPreserved = true ∧
    b.boundary.subsequentCycleCandidateSelectionAuthorizationRequestOnly = true ∧
    b.boundary.subsequentCycleCandidateSelectionAuthorizationRequested = true ∧
    b.boundary.subsequentCycleSelectionAuthorityGranted = false ∧
    b.boundary.subsequentCycleCandidateSelectionRequested = false ∧
    b.boundary.subsequentCycleCandidateSelected = false ∧
    b.boundary.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourceRequired,
    b.boundary.requestOnlyRequired, b.boundary.authorizationRequestedRequired,
    b.boundary.authorityForbidden, b.boundary.selectionRequestForbidden,
    b.boundary.candidateSelectionForbidden, b.boundary.admissionRequestForbidden⟩

 theorem history_appends_one_request
    (b : PlanOSSubsequentCycleCandidateSelectionAuthorizationRequestBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

end PlanOSSubsequentCycleCandidateSelectionAuthorizationRequestBridge
end PlanOS
end KUOS
