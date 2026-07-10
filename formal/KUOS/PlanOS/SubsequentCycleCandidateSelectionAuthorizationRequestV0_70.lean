import Mathlib
import KUOS.PlanOS.SubsequentCycleCandidateReviewReceiptV0_69

namespace KUOS
namespace PlanOS

structure SubsequentCycleCandidateSelectionAuthorizationRequestSurface where
  sourceReview : SubsequentCycleCandidateReviewReceiptSurface
  sourceBoundary : SubsequentCycleCandidateReviewReceiptBoundary
  sourceReceiptBound : Bool
  selectedCandidateProvenancePreserved : Bool
  candidateSetDigestPreserved : Bool
  evaluationSetDigestPreserved : Bool
  reviewSetDigestPreserved : Bool
  reviewCountExactPreserved : Bool
  candidateReviewCompletedPreserved : Bool
  selectionEligibilityPreserved : Bool
  selectionEligibleSetNonempty : Bool
  memoryOverwritePreserved : Bool
  truthAuthorityPreserved : Bool
  blockerReleasePreserved : Bool
  nextCycleCycleClosed : Bool
  subsequentCycleReplanRequested : Bool
  subsequentCycleCandidateGenerationStarted : Bool
  subsequentCycleCandidateSetMaterialized : Bool
  subsequentCycleCandidateEvaluationsRecorded : Bool
  subsequentCycleCandidateReviewRequested : Bool
  subsequentCycleCandidateReviewCompleted : Bool
  candidateCount : Nat
  evaluationCount : Nat
  reviewCount : Nat
  selectionEligibleCount : Nat
  selectionEligibleSetDigestBound : Bool
  selectionScopeBound : Bool
  selectionPolicyDigestBound : Bool
  candidateSelectionAuthorizationRequestOnly : Bool
  candidateSelectionAuthorizationRequested : Bool
  selectionAuthorityGranted : Bool
  candidateSelectionRequested : Bool
  candidateSelected : Bool
  admissionRequested : Bool
  sourceRequired : sourceReceiptBound = true
  provenanceRequired : selectedCandidateProvenancePreserved = true
  candidateSetDigestRequired : candidateSetDigestPreserved = true
  evaluationSetDigestRequired : evaluationSetDigestPreserved = true
  reviewSetDigestRequired : reviewSetDigestPreserved = true
  reviewCountRequired : reviewCountExactPreserved = true
  reviewCompletedRequired : candidateReviewCompletedPreserved = true
  eligibilityRequired : selectionEligibilityPreserved = true
  eligibleSetNonemptyRequired : selectionEligibleSetNonempty = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  truthAuthorityRequired : truthAuthorityPreserved = true
  blockerReleaseRequired : blockerReleasePreserved = true
  closeoutRequired : nextCycleCycleClosed = true
  replanRequired : subsequentCycleReplanRequested = true
  generationRequired : subsequentCycleCandidateGenerationStarted = true
  materializationRequired : subsequentCycleCandidateSetMaterialized = true
  evaluationsRequired : subsequentCycleCandidateEvaluationsRecorded = true
  reviewRequestedRequired : subsequentCycleCandidateReviewRequested = true
  reviewCompletedChainRequired : subsequentCycleCandidateReviewCompleted = true
  candidateCountPositive : 0 < candidateCount
  evaluationCountExact : evaluationCount = candidateCount
  reviewCountExact : reviewCount = evaluationCount
  eligibleCountPositive : 0 < selectionEligibleCount
  eligibleCountBounded : selectionEligibleCount ≤ reviewCount
  eligibleSetDigestRequired : selectionEligibleSetDigestBound = true
  selectionScopeRequired : selectionScopeBound = true
  selectionPolicyRequired : selectionPolicyDigestBound = true
  requestOnlyRequired : candidateSelectionAuthorizationRequestOnly = true
  authorizationRequestedRequired : candidateSelectionAuthorizationRequested = true
  authorityGrantForbidden : selectionAuthorityGranted = false
  selectionRequestForbidden : candidateSelectionRequested = false
  candidateSelectionForbidden : candidateSelected = false
  admissionRequestForbidden : admissionRequested = false

structure SubsequentCycleCandidateSelectionAuthorizationRequestBoundary where
  requestOwnedByPlanOS : Bool
  sourceCandidateReviewReceiptPreserved : Bool
  selectedCandidateProvenancePreserved : Bool
  candidateSetDigestPreserved : Bool
  evaluationSetDigestPreserved : Bool
  reviewSetDigestPreserved : Bool
  reviewCountExactPreserved : Bool
  candidateReviewCompletedPreserved : Bool
  selectionEligibilityPreserved : Bool
  selectionEligibleSetNonempty : Bool
  memoryOverwritePreserved : Bool
  truthAuthorityPreserved : Bool
  blockerReleasePreserved : Bool
  nextCycleCycleClosed : Bool
  subsequentCycleReplanRequested : Bool
  subsequentCycleCandidateGenerationStarted : Bool
  subsequentCycleCandidateSetMaterialized : Bool
  subsequentCycleCandidateEvaluationsRecorded : Bool
  subsequentCycleCandidateReviewRequested : Bool
  subsequentCycleCandidateReviewCompleted : Bool
  subsequentCycleCandidateSelectionAuthorizationRequestOnly : Bool
  subsequentCycleCandidateSelectionAuthorizationRequested : Bool
  subsequentCycleSelectionScopeBound : Bool
  subsequentCycleSelectionPolicyDigestBound : Bool
  subsequentCycleSelectionAuthorityGranted : Bool
  subsequentCycleCandidateSelectionRequested : Bool
  subsequentCycleCandidateSelected : Bool
  subsequentCycleAdmissionRequested : Bool
  ownerRequired : requestOwnedByPlanOS = true
  sourceRequired : sourceCandidateReviewReceiptPreserved = true
  provenanceRequired : selectedCandidateProvenancePreserved = true
  candidateSetDigestRequired : candidateSetDigestPreserved = true
  evaluationSetDigestRequired : evaluationSetDigestPreserved = true
  reviewSetDigestRequired : reviewSetDigestPreserved = true
  reviewCountRequired : reviewCountExactPreserved = true
  reviewCompletedRequired : candidateReviewCompletedPreserved = true
  eligibilityRequired : selectionEligibilityPreserved = true
  eligibleSetRequired : selectionEligibleSetNonempty = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  truthAuthorityRequired : truthAuthorityPreserved = true
  blockerReleaseRequired : blockerReleasePreserved = true
  closeoutRequired : nextCycleCycleClosed = true
  replanRequired : subsequentCycleReplanRequested = true
  generationRequired : subsequentCycleCandidateGenerationStarted = true
  materializationRequired : subsequentCycleCandidateSetMaterialized = true
  evaluationsRequired : subsequentCycleCandidateEvaluationsRecorded = true
  reviewRequestedRequired : subsequentCycleCandidateReviewRequested = true
  reviewCompletedChainRequired : subsequentCycleCandidateReviewCompleted = true
  requestOnlyRequired : subsequentCycleCandidateSelectionAuthorizationRequestOnly = true
  authorizationRequestedRequired : subsequentCycleCandidateSelectionAuthorizationRequested = true
  selectionScopeRequired : subsequentCycleSelectionScopeBound = true
  selectionPolicyRequired : subsequentCycleSelectionPolicyDigestBound = true
  authorityGrantForbidden : subsequentCycleSelectionAuthorityGranted = false
  selectionRequestForbidden : subsequentCycleCandidateSelectionRequested = false
  candidateSelectionForbidden : subsequentCycleCandidateSelected = false
  admissionRequestForbidden : subsequentCycleAdmissionRequested = false

structure PlanOSSubsequentCycleCandidateSelectionAuthorizationRequestBridge where
  Digest : Type
  digestOf : SubsequentCycleCandidateSelectionAuthorizationRequestSurface →
    SubsequentCycleCandidateSelectionAuthorizationRequestBoundary → Nat → Digest
  surface : SubsequentCycleCandidateSelectionAuthorizationRequestSurface
  boundary : SubsequentCycleCandidateSelectionAuthorizationRequestBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  requesterNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  requesterTruthForbidden : requesterNonAuthority.truthAuthority = false

namespace PlanOSSubsequentCycleCandidateSelectionAuthorizationRequestBridge

theorem source_review_is_complete_without_selection
    (b : PlanOSSubsequentCycleCandidateSelectionAuthorizationRequestBridge) :
    b.surface.sourceReview.candidateReviewCompleted = true ∧
      b.surface.sourceReview.selectionEligibilityRecorded = true ∧
      b.surface.sourceReview.subsequentCycleSelectionAuthorityGranted = false ∧
      b.surface.sourceReview.subsequentCycleCandidateSelectionRequested = false ∧
      b.surface.sourceReview.subsequentCycleCandidateSelected = false ∧
      b.surface.sourceReview.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.surface.sourceReview.reviewCompletedRequired,
    b.surface.sourceReview.selectionEligibilityRequired,
    b.surface.sourceReview.selectionAuthorityForbidden,
    b.surface.sourceReview.selectionRequestForbidden,
    b.surface.sourceReview.candidateSelectionForbidden,
    b.surface.sourceReview.admissionRequestForbidden⟩

theorem request_preserves_review_and_authority_chain
    (b : PlanOSSubsequentCycleCandidateSelectionAuthorizationRequestBridge) :
    b.surface.sourceReceiptBound = true ∧
      b.surface.selectedCandidateProvenancePreserved = true ∧
      b.surface.candidateSetDigestPreserved = true ∧
      b.surface.evaluationSetDigestPreserved = true ∧
      b.surface.reviewSetDigestPreserved = true ∧
      b.surface.reviewCountExactPreserved = true ∧
      b.surface.candidateReviewCompletedPreserved = true ∧
      b.surface.selectionEligibilityPreserved = true ∧
      b.surface.selectionEligibleSetNonempty = true ∧
      b.surface.memoryOverwritePreserved = true ∧
      b.surface.truthAuthorityPreserved = true ∧
      b.surface.blockerReleasePreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.provenanceRequired,
    b.surface.candidateSetDigestRequired, b.surface.evaluationSetDigestRequired,
    b.surface.reviewSetDigestRequired, b.surface.reviewCountRequired,
    b.surface.reviewCompletedRequired, b.surface.eligibilityRequired,
    b.surface.eligibleSetNonemptyRequired, b.surface.memoryOverwriteRequired,
    b.surface.truthAuthorityRequired, b.surface.blockerReleaseRequired⟩

theorem request_is_bounded_and_does_not_select
    (b : PlanOSSubsequentCycleCandidateSelectionAuthorizationRequestBridge) :
    0 < b.surface.candidateCount ∧
      b.surface.evaluationCount = b.surface.candidateCount ∧
      b.surface.reviewCount = b.surface.evaluationCount ∧
      0 < b.surface.selectionEligibleCount ∧
      b.surface.selectionEligibleCount ≤ b.surface.reviewCount ∧
      b.surface.selectionEligibleSetDigestBound = true ∧
      b.surface.selectionScopeBound = true ∧
      b.surface.selectionPolicyDigestBound = true ∧
      b.surface.candidateSelectionAuthorizationRequestOnly = true ∧
      b.surface.candidateSelectionAuthorizationRequested = true ∧
      b.surface.selectionAuthorityGranted = false ∧
      b.surface.candidateSelectionRequested = false ∧
      b.surface.candidateSelected = false ∧
      b.surface.admissionRequested = false ∧
      b.requesterNonAuthority.truthAuthority = false := by
  exact ⟨b.surface.candidateCountPositive, b.surface.evaluationCountExact,
    b.surface.reviewCountExact, b.surface.eligibleCountPositive,
    b.surface.eligibleCountBounded, b.surface.eligibleSetDigestRequired,
    b.surface.selectionScopeRequired, b.surface.selectionPolicyRequired,
    b.surface.requestOnlyRequired, b.surface.authorizationRequestedRequired,
    b.surface.authorityGrantForbidden, b.surface.selectionRequestForbidden,
    b.surface.candidateSelectionForbidden, b.surface.admissionRequestForbidden,
    b.requesterTruthForbidden⟩

theorem boundary_is_selection_authorization_request_only
    (b : PlanOSSubsequentCycleCandidateSelectionAuthorizationRequestBridge) :
    b.boundary.requestOwnedByPlanOS = true ∧
      b.boundary.sourceCandidateReviewReceiptPreserved = true ∧
      b.boundary.candidateReviewCompletedPreserved = true ∧
      b.boundary.selectionEligibilityPreserved = true ∧
      b.boundary.selectionEligibleSetNonempty = true ∧
      b.boundary.subsequentCycleCandidateSelectionAuthorizationRequestOnly = true ∧
      b.boundary.subsequentCycleCandidateSelectionAuthorizationRequested = true ∧
      b.boundary.subsequentCycleSelectionScopeBound = true ∧
      b.boundary.subsequentCycleSelectionPolicyDigestBound = true ∧
      b.boundary.subsequentCycleSelectionAuthorityGranted = false ∧
      b.boundary.subsequentCycleCandidateSelectionRequested = false ∧
      b.boundary.subsequentCycleCandidateSelected = false ∧
      b.boundary.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourceRequired,
    b.boundary.reviewCompletedRequired, b.boundary.eligibilityRequired,
    b.boundary.eligibleSetRequired, b.boundary.requestOnlyRequired,
    b.boundary.authorizationRequestedRequired, b.boundary.selectionScopeRequired,
    b.boundary.selectionPolicyRequired, b.boundary.authorityGrantForbidden,
    b.boundary.selectionRequestForbidden, b.boundary.candidateSelectionForbidden,
    b.boundary.admissionRequestForbidden⟩

theorem history_appends_one_selection_authorization_request
    (b : PlanOSSubsequentCycleCandidateSelectionAuthorizationRequestBridge) :
    b.historyDelta = 1 := by exact b.historyDeltaRequired

theorem digest_is_exact
    (b : PlanOSSubsequentCycleCandidateSelectionAuthorizationRequestBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by exact b.digestExact

end PlanOSSubsequentCycleCandidateSelectionAuthorizationRequestBridge
end PlanOS
end KUOS
