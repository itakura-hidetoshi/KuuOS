import Mathlib
import KUOS.PlanOS.SubsequentCycleCandidateReviewRequestV0_68

namespace KUOS
namespace PlanOS

structure SubsequentCycleCandidateReviewReceiptSurface where
  sourceRequest : SubsequentCycleCandidateReviewRequestSurface
  sourceRequestBoundary : SubsequentCycleCandidateReviewRequestBoundary
  sourceEvaluation : SubsequentCycleCandidateEvaluationReceiptSurface
  sourceEvaluationBoundary : SubsequentCycleCandidateEvaluationReceiptBoundary
  sourceRequestBound : Bool
  sourceEvaluationBound : Bool
  requestEvaluationDigestLinked : Bool
  selectedCandidateProvenancePreserved : Bool
  candidateSetDigestPreserved : Bool
  evaluationSetDigestPreserved : Bool
  evaluationCountExactPreserved : Bool
  reviewScopePreserved : Bool
  reviewCriteriaDigestPreserved : Bool
  allMaterializedCandidatesEvaluatedPreserved : Bool
  evaluationScoreBoundsValidPreserved : Bool
  evaluationOrderNonselectionPreserved : Bool
  memoryOverwritePreserved : Bool
  truthAuthorityPreserved : Bool
  blockerReleasePreserved : Bool
  nextCycleCycleClosed : Bool
  subsequentCycleReplanRequested : Bool
  subsequentCycleCandidateGenerationStarted : Bool
  subsequentCycleCandidateSetMaterialized : Bool
  subsequentCycleCandidateEvaluationsRecorded : Bool
  subsequentCycleCandidateReviewRequested : Bool
  candidateCount : Nat
  evaluationCount : Nat
  reviewInputCount : Nat
  reviewCount : Nat
  selectionEligibleCount : Nat
  reviewSetDigestBound : Bool
  allEvaluatedCandidatesReviewed : Bool
  reviewOutcomesRecorded : Bool
  candidateReviewCompleted : Bool
  reviewOrderIsNotSelection : Bool
  selectionEligibilityRecorded : Bool
  subsequentCycleCandidateReviewReceiptOnly : Bool
  subsequentCycleSelectionAuthorityGranted : Bool
  subsequentCycleCandidateSelectionRequested : Bool
  subsequentCycleCandidateSelected : Bool
  subsequentCycleAdmissionRequested : Bool
  sourceRequestRequired : sourceRequestBound = true
  sourceEvaluationRequired : sourceEvaluationBound = true
  requestEvaluationLinkRequired : requestEvaluationDigestLinked = true
  provenanceRequired : selectedCandidateProvenancePreserved = true
  candidateSetDigestRequired : candidateSetDigestPreserved = true
  evaluationSetDigestRequired : evaluationSetDigestPreserved = true
  evaluationCountPreservedRequired : evaluationCountExactPreserved = true
  reviewScopeRequired : reviewScopePreserved = true
  reviewCriteriaRequired : reviewCriteriaDigestPreserved = true
  allCandidatesEvaluatedRequired : allMaterializedCandidatesEvaluatedPreserved = true
  scoreBoundsRequired : evaluationScoreBoundsValidPreserved = true
  evaluationOrderRequired : evaluationOrderNonselectionPreserved = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  truthAuthorityRequired : truthAuthorityPreserved = true
  blockerReleaseRequired : blockerReleasePreserved = true
  priorCloseoutRequired : nextCycleCycleClosed = true
  replanRequestedRequired : subsequentCycleReplanRequested = true
  generationStartedRequired : subsequentCycleCandidateGenerationStarted = true
  candidateSetMaterializedRequired : subsequentCycleCandidateSetMaterialized = true
  evaluationsRecordedRequired : subsequentCycleCandidateEvaluationsRecorded = true
  reviewRequestedRequired : subsequentCycleCandidateReviewRequested = true
  candidateCountPositive : 0 < candidateCount
  evaluationCountExact : evaluationCount = candidateCount
  reviewInputCountExact : reviewInputCount = evaluationCount
  reviewCountExact : reviewCount = evaluationCount
  reviewSetDigestRequired : reviewSetDigestBound = true
  allReviewedRequired : allEvaluatedCandidatesReviewed = true
  reviewOutcomesRequired : reviewOutcomesRecorded = true
  reviewCompletedRequired : candidateReviewCompleted = true
  reviewOrderNonselectionRequired : reviewOrderIsNotSelection = true
  selectionEligibilityRequired : selectionEligibilityRecorded = true
  reviewReceiptOnlyRequired : subsequentCycleCandidateReviewReceiptOnly = true
  selectionAuthorityForbidden : subsequentCycleSelectionAuthorityGranted = false
  selectionRequestForbidden : subsequentCycleCandidateSelectionRequested = false
  candidateSelectionForbidden : subsequentCycleCandidateSelected = false
  admissionRequestForbidden : subsequentCycleAdmissionRequested = false

structure SubsequentCycleCandidateReviewReceiptBoundary where
  receiptOwnedByPlanOS : Bool
  sourceCandidateReviewRequestPreserved : Bool
  sourceCandidateEvaluationReceiptPreserved : Bool
  selectedCandidateProvenancePreserved : Bool
  candidateSetDigestPreserved : Bool
  evaluationSetDigestPreserved : Bool
  evaluationCountExactPreserved : Bool
  reviewScopePreserved : Bool
  reviewCriteriaDigestPreserved : Bool
  allMaterializedCandidatesEvaluatedPreserved : Bool
  evaluationScoreBoundsValidPreserved : Bool
  evaluationOrderNonselectionPreserved : Bool
  memoryOverwritePreserved : Bool
  truthAuthorityPreserved : Bool
  blockerReleasePreserved : Bool
  nextCycleCycleClosed : Bool
  subsequentCycleReplanRequested : Bool
  subsequentCycleCandidateGenerationStarted : Bool
  subsequentCycleCandidateSetMaterialized : Bool
  subsequentCycleCandidateEvaluationsRecorded : Bool
  subsequentCycleCandidateReviewRequested : Bool
  subsequentCycleCandidateReviewReceiptOnly : Bool
  subsequentCycleAllEvaluatedCandidatesReviewed : Bool
  subsequentCycleCandidateReviewCountExact : Bool
  subsequentCycleCandidateReviewOutcomesRecorded : Bool
  subsequentCycleCandidateReviewCompleted : Bool
  subsequentCycleReviewOrderIsNotSelection : Bool
  subsequentCycleSelectionEligibilityRecorded : Bool
  subsequentCycleSelectionAuthorityGranted : Bool
  subsequentCycleCandidateSelectionRequested : Bool
  subsequentCycleCandidateSelected : Bool
  subsequentCycleAdmissionRequested : Bool
  ownerRequired : receiptOwnedByPlanOS = true
  sourceRequestRequired : sourceCandidateReviewRequestPreserved = true
  sourceEvaluationRequired : sourceCandidateEvaluationReceiptPreserved = true
  provenanceRequired : selectedCandidateProvenancePreserved = true
  candidateSetDigestRequired : candidateSetDigestPreserved = true
  evaluationSetDigestRequired : evaluationSetDigestPreserved = true
  evaluationCountRequired : evaluationCountExactPreserved = true
  reviewScopeRequired : reviewScopePreserved = true
  reviewCriteriaRequired : reviewCriteriaDigestPreserved = true
  allCandidatesEvaluatedRequired : allMaterializedCandidatesEvaluatedPreserved = true
  scoreBoundsRequired : evaluationScoreBoundsValidPreserved = true
  evaluationOrderRequired : evaluationOrderNonselectionPreserved = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  truthAuthorityRequired : truthAuthorityPreserved = true
  blockerReleaseRequired : blockerReleasePreserved = true
  priorCloseoutRequired : nextCycleCycleClosed = true
  replanRequestedRequired : subsequentCycleReplanRequested = true
  generationStartedRequired : subsequentCycleCandidateGenerationStarted = true
  candidateSetMaterializedRequired : subsequentCycleCandidateSetMaterialized = true
  evaluationsRecordedRequired : subsequentCycleCandidateEvaluationsRecorded = true
  reviewRequestedRequired : subsequentCycleCandidateReviewRequested = true
  reviewReceiptOnlyRequired : subsequentCycleCandidateReviewReceiptOnly = true
  allReviewedRequired : subsequentCycleAllEvaluatedCandidatesReviewed = true
  reviewCountRequired : subsequentCycleCandidateReviewCountExact = true
  reviewOutcomesRequired : subsequentCycleCandidateReviewOutcomesRecorded = true
  reviewCompletedRequired : subsequentCycleCandidateReviewCompleted = true
  reviewOrderRequired : subsequentCycleReviewOrderIsNotSelection = true
  selectionEligibilityRequired : subsequentCycleSelectionEligibilityRecorded = true
  selectionAuthorityForbidden : subsequentCycleSelectionAuthorityGranted = false
  selectionRequestForbidden : subsequentCycleCandidateSelectionRequested = false
  candidateSelectionForbidden : subsequentCycleCandidateSelected = false
  admissionRequestForbidden : subsequentCycleAdmissionRequested = false

structure PlanOSSubsequentCycleCandidateReviewReceiptBridge where
  Digest : Type
  digestOf : SubsequentCycleCandidateReviewReceiptSurface →
    SubsequentCycleCandidateReviewReceiptBoundary → Nat → Digest
  surface : SubsequentCycleCandidateReviewReceiptSurface
  boundary : SubsequentCycleCandidateReviewReceiptBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  recorderNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  recorderTruthForbidden : recorderNonAuthority.truthAuthority = false

namespace PlanOSSubsequentCycleCandidateReviewReceiptBridge

theorem source_request_opens_review_without_selection
    (b : PlanOSSubsequentCycleCandidateReviewReceiptBridge) :
    b.surface.sourceRequest.subsequentCycleCandidateReviewRequestOnly = true ∧
      b.surface.sourceRequest.subsequentCycleCandidateReviewRequested = true ∧
      b.surface.sourceRequest.reviewScopeBound = true ∧
      b.surface.sourceRequest.reviewCriteriaDigestBound = true ∧
      b.surface.sourceRequest.subsequentCycleSelectionAuthorityGranted = false ∧
      b.surface.sourceRequest.subsequentCycleCandidateReviewCompleted = false ∧
      b.surface.sourceRequest.subsequentCycleCandidateSelected = false ∧
      b.surface.sourceRequest.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.surface.sourceRequest.reviewRequestOnlyRequired,
    b.surface.sourceRequest.reviewRequestedRequired,
    b.surface.sourceRequest.reviewScopeRequired,
    b.surface.sourceRequest.reviewCriteriaRequired,
    b.surface.sourceRequest.selectionAuthorityForbidden,
    b.surface.sourceRequest.reviewCompletionForbidden,
    b.surface.sourceRequest.candidateSelectionForbidden,
    b.surface.sourceRequest.admissionRequestForbidden⟩

theorem source_evaluation_is_complete_exact_and_nonselective
    (b : PlanOSSubsequentCycleCandidateReviewReceiptBridge) :
    0 < b.surface.sourceEvaluation.candidateCount ∧
      b.surface.sourceEvaluation.evaluationCount = b.surface.sourceEvaluation.candidateCount ∧
      b.surface.sourceEvaluation.allMaterializedCandidatesEvaluated = true ∧
      b.surface.sourceEvaluation.evaluationScoreBoundsValid = true ∧
      b.surface.sourceEvaluation.subsequentCycleCandidateEvaluationsRecorded = true ∧
      b.surface.sourceEvaluation.subsequentCycleEvaluationOrderIsNotSelection = true ∧
      b.surface.sourceEvaluation.subsequentCycleCandidateSelected = false ∧
      b.surface.sourceEvaluation.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.surface.sourceEvaluation.candidateCountPositive,
    b.surface.sourceEvaluation.evaluationCountExact,
    b.surface.sourceEvaluation.allCandidatesEvaluatedRequired,
    b.surface.sourceEvaluation.scoreBoundsRequired,
    b.surface.sourceEvaluation.evaluationsRecordedRequired,
    b.surface.sourceEvaluation.evaluationOrderNonSelectionRequired,
    b.surface.sourceEvaluation.candidateSelectionForbidden,
    b.surface.sourceEvaluation.admissionRequestForbidden⟩

theorem review_receipt_preserves_request_evaluation_and_authority_chain
    (b : PlanOSSubsequentCycleCandidateReviewReceiptBridge) :
    b.surface.sourceRequestBound = true ∧
      b.surface.sourceEvaluationBound = true ∧
      b.surface.requestEvaluationDigestLinked = true ∧
      b.surface.selectedCandidateProvenancePreserved = true ∧
      b.surface.candidateSetDigestPreserved = true ∧
      b.surface.evaluationSetDigestPreserved = true ∧
      b.surface.evaluationCountExactPreserved = true ∧
      b.surface.reviewScopePreserved = true ∧
      b.surface.reviewCriteriaDigestPreserved = true ∧
      b.surface.allMaterializedCandidatesEvaluatedPreserved = true ∧
      b.surface.evaluationScoreBoundsValidPreserved = true ∧
      b.surface.evaluationOrderNonselectionPreserved = true ∧
      b.surface.memoryOverwritePreserved = true ∧
      b.surface.truthAuthorityPreserved = true ∧
      b.surface.blockerReleasePreserved = true ∧
      b.surface.nextCycleCycleClosed = true ∧
      b.surface.subsequentCycleReplanRequested = true ∧
      b.surface.subsequentCycleCandidateGenerationStarted = true ∧
      b.surface.subsequentCycleCandidateSetMaterialized = true ∧
      b.surface.subsequentCycleCandidateEvaluationsRecorded = true ∧
      b.surface.subsequentCycleCandidateReviewRequested = true := by
  exact ⟨b.surface.sourceRequestRequired, b.surface.sourceEvaluationRequired,
    b.surface.requestEvaluationLinkRequired, b.surface.provenanceRequired,
    b.surface.candidateSetDigestRequired, b.surface.evaluationSetDigestRequired,
    b.surface.evaluationCountPreservedRequired, b.surface.reviewScopeRequired,
    b.surface.reviewCriteriaRequired, b.surface.allCandidatesEvaluatedRequired,
    b.surface.scoreBoundsRequired, b.surface.evaluationOrderRequired,
    b.surface.memoryOverwriteRequired, b.surface.truthAuthorityRequired,
    b.surface.blockerReleaseRequired, b.surface.priorCloseoutRequired,
    b.surface.replanRequestedRequired, b.surface.generationStartedRequired,
    b.surface.candidateSetMaterializedRequired, b.surface.evaluationsRecordedRequired,
    b.surface.reviewRequestedRequired⟩

theorem review_is_complete_exact_digest_bound_without_selection
    (b : PlanOSSubsequentCycleCandidateReviewReceiptBridge) :
    0 < b.surface.candidateCount ∧
      b.surface.evaluationCount = b.surface.candidateCount ∧
      b.surface.reviewInputCount = b.surface.evaluationCount ∧
      b.surface.reviewCount = b.surface.evaluationCount ∧
      b.surface.reviewSetDigestBound = true ∧
      b.surface.allEvaluatedCandidatesReviewed = true ∧
      b.surface.reviewOutcomesRecorded = true ∧
      b.surface.candidateReviewCompleted = true ∧
      b.surface.reviewOrderIsNotSelection = true ∧
      b.surface.selectionEligibilityRecorded = true ∧
      b.surface.subsequentCycleCandidateReviewReceiptOnly = true ∧
      b.surface.subsequentCycleSelectionAuthorityGranted = false ∧
      b.surface.subsequentCycleCandidateSelectionRequested = false ∧
      b.surface.subsequentCycleCandidateSelected = false ∧
      b.surface.subsequentCycleAdmissionRequested = false ∧
      b.recorderNonAuthority.truthAuthority = false := by
  exact ⟨b.surface.candidateCountPositive, b.surface.evaluationCountExact,
    b.surface.reviewInputCountExact, b.surface.reviewCountExact,
    b.surface.reviewSetDigestRequired, b.surface.allReviewedRequired,
    b.surface.reviewOutcomesRequired, b.surface.reviewCompletedRequired,
    b.surface.reviewOrderNonselectionRequired, b.surface.selectionEligibilityRequired,
    b.surface.reviewReceiptOnlyRequired, b.surface.selectionAuthorityForbidden,
    b.surface.selectionRequestForbidden, b.surface.candidateSelectionForbidden,
    b.surface.admissionRequestForbidden, b.recorderTruthForbidden⟩

theorem boundary_is_candidate_review_receipt_only
    (b : PlanOSSubsequentCycleCandidateReviewReceiptBridge) :
    b.boundary.receiptOwnedByPlanOS = true ∧
      b.boundary.sourceCandidateReviewRequestPreserved = true ∧
      b.boundary.sourceCandidateEvaluationReceiptPreserved = true ∧
      b.boundary.selectedCandidateProvenancePreserved = true ∧
      b.boundary.candidateSetDigestPreserved = true ∧
      b.boundary.evaluationSetDigestPreserved = true ∧
      b.boundary.evaluationCountExactPreserved = true ∧
      b.boundary.reviewScopePreserved = true ∧
      b.boundary.reviewCriteriaDigestPreserved = true ∧
      b.boundary.allMaterializedCandidatesEvaluatedPreserved = true ∧
      b.boundary.evaluationScoreBoundsValidPreserved = true ∧
      b.boundary.evaluationOrderNonselectionPreserved = true ∧
      b.boundary.memoryOverwritePreserved = true ∧
      b.boundary.truthAuthorityPreserved = true ∧
      b.boundary.blockerReleasePreserved = true ∧
      b.boundary.nextCycleCycleClosed = true ∧
      b.boundary.subsequentCycleReplanRequested = true ∧
      b.boundary.subsequentCycleCandidateGenerationStarted = true ∧
      b.boundary.subsequentCycleCandidateSetMaterialized = true ∧
      b.boundary.subsequentCycleCandidateEvaluationsRecorded = true ∧
      b.boundary.subsequentCycleCandidateReviewRequested = true ∧
      b.boundary.subsequentCycleCandidateReviewReceiptOnly = true ∧
      b.boundary.subsequentCycleAllEvaluatedCandidatesReviewed = true ∧
      b.boundary.subsequentCycleCandidateReviewCountExact = true ∧
      b.boundary.subsequentCycleCandidateReviewOutcomesRecorded = true ∧
      b.boundary.subsequentCycleCandidateReviewCompleted = true ∧
      b.boundary.subsequentCycleReviewOrderIsNotSelection = true ∧
      b.boundary.subsequentCycleSelectionEligibilityRecorded = true ∧
      b.boundary.subsequentCycleSelectionAuthorityGranted = false ∧
      b.boundary.subsequentCycleCandidateSelectionRequested = false ∧
      b.boundary.subsequentCycleCandidateSelected = false ∧
      b.boundary.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourceRequestRequired,
    b.boundary.sourceEvaluationRequired, b.boundary.provenanceRequired,
    b.boundary.candidateSetDigestRequired, b.boundary.evaluationSetDigestRequired,
    b.boundary.evaluationCountRequired, b.boundary.reviewScopeRequired,
    b.boundary.reviewCriteriaRequired, b.boundary.allCandidatesEvaluatedRequired,
    b.boundary.scoreBoundsRequired, b.boundary.evaluationOrderRequired,
    b.boundary.memoryOverwriteRequired, b.boundary.truthAuthorityRequired,
    b.boundary.blockerReleaseRequired, b.boundary.priorCloseoutRequired,
    b.boundary.replanRequestedRequired, b.boundary.generationStartedRequired,
    b.boundary.candidateSetMaterializedRequired, b.boundary.evaluationsRecordedRequired,
    b.boundary.reviewRequestedRequired, b.boundary.reviewReceiptOnlyRequired,
    b.boundary.allReviewedRequired, b.boundary.reviewCountRequired,
    b.boundary.reviewOutcomesRequired, b.boundary.reviewCompletedRequired,
    b.boundary.reviewOrderRequired, b.boundary.selectionEligibilityRequired,
    b.boundary.selectionAuthorityForbidden, b.boundary.selectionRequestForbidden,
    b.boundary.candidateSelectionForbidden, b.boundary.admissionRequestForbidden⟩

theorem history_appends_one_candidate_review_receipt
    (b : PlanOSSubsequentCycleCandidateReviewReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact
    (b : PlanOSSubsequentCycleCandidateReviewReceiptBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSSubsequentCycleCandidateReviewReceiptBridge

end PlanOS
end KUOS
