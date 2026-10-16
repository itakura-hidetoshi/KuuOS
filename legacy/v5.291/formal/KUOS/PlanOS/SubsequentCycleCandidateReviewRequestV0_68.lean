import Mathlib
import KUOS.PlanOS.SubsequentCycleCandidateEvaluationReceiptV0_67

namespace KUOS
namespace PlanOS

structure SubsequentCycleCandidateReviewRequestSurface where
  sourceEvaluation : SubsequentCycleCandidateEvaluationReceiptSurface
  sourceBoundary : SubsequentCycleCandidateEvaluationReceiptBoundary
  sourceReceiptBound : Bool
  selectedCandidateProvenancePreserved : Bool
  candidateSetDigestPreserved : Bool
  evaluationSetDigestPreserved : Bool
  evaluationCountExactPreserved : Bool
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
  candidateCount : Nat
  evaluationCount : Nat
  reviewScopeBound : Bool
  reviewCriteriaDigestBound : Bool
  subsequentCycleCandidateReviewRequestOnly : Bool
  subsequentCycleCandidateReviewRequested : Bool
  subsequentCycleSelectionAuthorityGranted : Bool
  subsequentCycleCandidateReviewCompleted : Bool
  subsequentCycleCandidateSelected : Bool
  subsequentCycleAdmissionRequested : Bool
  sourceRequired : sourceReceiptBound = true
  provenanceRequired : selectedCandidateProvenancePreserved = true
  candidateSetDigestRequired : candidateSetDigestPreserved = true
  evaluationSetDigestRequired : evaluationSetDigestPreserved = true
  evaluationCountExactRequired : evaluationCountExactPreserved = true
  allCandidatesEvaluatedRequired : allMaterializedCandidatesEvaluatedPreserved = true
  scoreBoundsRequired : evaluationScoreBoundsValidPreserved = true
  evaluationOrderNonselectionRequired : evaluationOrderNonselectionPreserved = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  truthAuthorityRequired : truthAuthorityPreserved = true
  blockerReleaseRequired : blockerReleasePreserved = true
  priorCloseoutRequired : nextCycleCycleClosed = true
  replanRequestedRequired : subsequentCycleReplanRequested = true
  generationStartedRequired : subsequentCycleCandidateGenerationStarted = true
  candidateSetMaterializedRequired : subsequentCycleCandidateSetMaterialized = true
  evaluationsRecordedRequired : subsequentCycleCandidateEvaluationsRecorded = true
  candidateCountPositive : 0 < candidateCount
  evaluationCountExact : evaluationCount = candidateCount
  reviewScopeRequired : reviewScopeBound = true
  reviewCriteriaRequired : reviewCriteriaDigestBound = true
  reviewRequestOnlyRequired : subsequentCycleCandidateReviewRequestOnly = true
  reviewRequestedRequired : subsequentCycleCandidateReviewRequested = true
  selectionAuthorityForbidden : subsequentCycleSelectionAuthorityGranted = false
  reviewCompletionForbidden : subsequentCycleCandidateReviewCompleted = false
  candidateSelectionForbidden : subsequentCycleCandidateSelected = false
  admissionRequestForbidden : subsequentCycleAdmissionRequested = false

structure SubsequentCycleCandidateReviewRequestBoundary where
  requestOwnedByPlanOS : Bool
  sourceCandidateEvaluationReceiptPreserved : Bool
  selectedCandidateProvenancePreserved : Bool
  candidateSetDigestPreserved : Bool
  evaluationSetDigestPreserved : Bool
  evaluationCountExactPreserved : Bool
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
  subsequentCycleCandidateReviewRequestOnly : Bool
  subsequentCycleCandidateReviewRequested : Bool
  subsequentCycleReviewScopeBound : Bool
  subsequentCycleReviewCriteriaDigestBound : Bool
  subsequentCycleSelectionAuthorityGranted : Bool
  subsequentCycleCandidateReviewCompleted : Bool
  subsequentCycleCandidateSelected : Bool
  subsequentCycleAdmissionRequested : Bool
  ownerRequired : requestOwnedByPlanOS = true
  sourcePreservedRequired : sourceCandidateEvaluationReceiptPreserved = true
  provenanceRequired : selectedCandidateProvenancePreserved = true
  candidateSetDigestRequired : candidateSetDigestPreserved = true
  evaluationSetDigestRequired : evaluationSetDigestPreserved = true
  evaluationCountExactRequired : evaluationCountExactPreserved = true
  allCandidatesEvaluatedRequired : allMaterializedCandidatesEvaluatedPreserved = true
  scoreBoundsRequired : evaluationScoreBoundsValidPreserved = true
  evaluationOrderNonselectionRequired : evaluationOrderNonselectionPreserved = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  truthAuthorityRequired : truthAuthorityPreserved = true
  blockerReleaseRequired : blockerReleasePreserved = true
  priorCloseoutRequired : nextCycleCycleClosed = true
  replanRequestedRequired : subsequentCycleReplanRequested = true
  generationStartedRequired : subsequentCycleCandidateGenerationStarted = true
  candidateSetMaterializedRequired : subsequentCycleCandidateSetMaterialized = true
  evaluationsRecordedRequired : subsequentCycleCandidateEvaluationsRecorded = true
  reviewRequestOnlyRequired : subsequentCycleCandidateReviewRequestOnly = true
  reviewRequestedRequired : subsequentCycleCandidateReviewRequested = true
  reviewScopeRequired : subsequentCycleReviewScopeBound = true
  reviewCriteriaRequired : subsequentCycleReviewCriteriaDigestBound = true
  selectionAuthorityForbidden : subsequentCycleSelectionAuthorityGranted = false
  reviewCompletionForbidden : subsequentCycleCandidateReviewCompleted = false
  candidateSelectionForbidden : subsequentCycleCandidateSelected = false
  admissionRequestForbidden : subsequentCycleAdmissionRequested = false

structure PlanOSSubsequentCycleCandidateReviewRequestBridge where
  Digest : Type
  digestOf : SubsequentCycleCandidateReviewRequestSurface →
    SubsequentCycleCandidateReviewRequestBoundary → Nat → Digest
  surface : SubsequentCycleCandidateReviewRequestSurface
  boundary : SubsequentCycleCandidateReviewRequestBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  requesterNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  requesterTruthForbidden : requesterNonAuthority.truthAuthority = false

namespace PlanOSSubsequentCycleCandidateReviewRequestBridge

theorem source_records_complete_evaluations_without_review_or_selection
    (b : PlanOSSubsequentCycleCandidateReviewRequestBridge) :
    b.surface.sourceEvaluation.subsequentCycleCandidateEvaluationReceiptOnly = true ∧
      b.surface.sourceEvaluation.allMaterializedCandidatesEvaluated = true ∧
      b.surface.sourceEvaluation.evaluationCount = b.surface.sourceEvaluation.candidateCount ∧
      b.surface.sourceEvaluation.evaluationScoreBoundsValid = true ∧
      b.surface.sourceEvaluation.subsequentCycleEvaluationOrderIsNotSelection = true ∧
      b.surface.sourceEvaluation.subsequentCycleCandidateReviewRequested = false ∧
      b.surface.sourceEvaluation.subsequentCycleCandidateSelected = false ∧
      b.surface.sourceEvaluation.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.surface.sourceEvaluation.evaluationOnlyRequired,
    b.surface.sourceEvaluation.allCandidatesEvaluatedRequired,
    b.surface.sourceEvaluation.evaluationCountExact,
    b.surface.sourceEvaluation.scoreBoundsRequired,
    b.surface.sourceEvaluation.evaluationOrderNonSelectionRequired,
    b.surface.sourceEvaluation.candidateReviewForbidden,
    b.surface.sourceEvaluation.candidateSelectionForbidden,
    b.surface.sourceEvaluation.admissionRequestForbidden⟩

theorem review_request_preserves_evaluation_and_authority_chain
    (b : PlanOSSubsequentCycleCandidateReviewRequestBridge) :
    b.surface.sourceReceiptBound = true ∧
      b.surface.selectedCandidateProvenancePreserved = true ∧
      b.surface.candidateSetDigestPreserved = true ∧
      b.surface.evaluationSetDigestPreserved = true ∧
      b.surface.evaluationCountExactPreserved = true ∧
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
      b.surface.subsequentCycleCandidateEvaluationsRecorded = true := by
  exact ⟨b.surface.sourceRequired, b.surface.provenanceRequired,
    b.surface.candidateSetDigestRequired, b.surface.evaluationSetDigestRequired,
    b.surface.evaluationCountExactRequired, b.surface.allCandidatesEvaluatedRequired,
    b.surface.scoreBoundsRequired, b.surface.evaluationOrderNonselectionRequired,
    b.surface.memoryOverwriteRequired, b.surface.truthAuthorityRequired,
    b.surface.blockerReleaseRequired, b.surface.priorCloseoutRequired,
    b.surface.replanRequestedRequired, b.surface.generationStartedRequired,
    b.surface.candidateSetMaterializedRequired, b.surface.evaluationsRecordedRequired⟩

theorem request_binds_review_scope_without_selection_authority
    (b : PlanOSSubsequentCycleCandidateReviewRequestBridge) :
    0 < b.surface.candidateCount ∧
      b.surface.evaluationCount = b.surface.candidateCount ∧
      b.surface.reviewScopeBound = true ∧
      b.surface.reviewCriteriaDigestBound = true ∧
      b.surface.subsequentCycleCandidateReviewRequestOnly = true ∧
      b.surface.subsequentCycleCandidateReviewRequested = true ∧
      b.surface.subsequentCycleSelectionAuthorityGranted = false ∧
      b.surface.subsequentCycleCandidateReviewCompleted = false ∧
      b.surface.subsequentCycleCandidateSelected = false ∧
      b.surface.subsequentCycleAdmissionRequested = false ∧
      b.requesterNonAuthority.truthAuthority = false := by
  exact ⟨b.surface.candidateCountPositive, b.surface.evaluationCountExact,
    b.surface.reviewScopeRequired, b.surface.reviewCriteriaRequired,
    b.surface.reviewRequestOnlyRequired, b.surface.reviewRequestedRequired,
    b.surface.selectionAuthorityForbidden, b.surface.reviewCompletionForbidden,
    b.surface.candidateSelectionForbidden, b.surface.admissionRequestForbidden,
    b.requesterTruthForbidden⟩

theorem boundary_is_candidate_review_request_only
    (b : PlanOSSubsequentCycleCandidateReviewRequestBridge) :
    b.boundary.requestOwnedByPlanOS = true ∧
      b.boundary.sourceCandidateEvaluationReceiptPreserved = true ∧
      b.boundary.selectedCandidateProvenancePreserved = true ∧
      b.boundary.candidateSetDigestPreserved = true ∧
      b.boundary.evaluationSetDigestPreserved = true ∧
      b.boundary.evaluationCountExactPreserved = true ∧
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
      b.boundary.subsequentCycleCandidateReviewRequestOnly = true ∧
      b.boundary.subsequentCycleCandidateReviewRequested = true ∧
      b.boundary.subsequentCycleReviewScopeBound = true ∧
      b.boundary.subsequentCycleReviewCriteriaDigestBound = true ∧
      b.boundary.subsequentCycleSelectionAuthorityGranted = false ∧
      b.boundary.subsequentCycleCandidateReviewCompleted = false ∧
      b.boundary.subsequentCycleCandidateSelected = false ∧
      b.boundary.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.provenanceRequired, b.boundary.candidateSetDigestRequired,
    b.boundary.evaluationSetDigestRequired, b.boundary.evaluationCountExactRequired,
    b.boundary.allCandidatesEvaluatedRequired, b.boundary.scoreBoundsRequired,
    b.boundary.evaluationOrderNonselectionRequired, b.boundary.memoryOverwriteRequired,
    b.boundary.truthAuthorityRequired, b.boundary.blockerReleaseRequired,
    b.boundary.priorCloseoutRequired, b.boundary.replanRequestedRequired,
    b.boundary.generationStartedRequired, b.boundary.candidateSetMaterializedRequired,
    b.boundary.evaluationsRecordedRequired, b.boundary.reviewRequestOnlyRequired,
    b.boundary.reviewRequestedRequired, b.boundary.reviewScopeRequired,
    b.boundary.reviewCriteriaRequired, b.boundary.selectionAuthorityForbidden,
    b.boundary.reviewCompletionForbidden, b.boundary.candidateSelectionForbidden,
    b.boundary.admissionRequestForbidden⟩

theorem history_appends_one_candidate_review_request
    (b : PlanOSSubsequentCycleCandidateReviewRequestBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact
    (b : PlanOSSubsequentCycleCandidateReviewRequestBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSSubsequentCycleCandidateReviewRequestBridge

end PlanOS
end KUOS
