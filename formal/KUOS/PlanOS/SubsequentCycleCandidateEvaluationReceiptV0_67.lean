import Mathlib
import KUOS.PlanOS.SubsequentCycleCandidateSetMaterializationReceiptV0_66

namespace KUOS
namespace PlanOS

structure SubsequentCycleCandidateEvaluationReceiptSurface where
  sourceMaterialization : SubsequentCycleCandidateSetMaterializationReceiptSurface
  sourceBoundary : SubsequentCycleCandidateSetMaterializationReceiptBoundary
  sourceReceiptBound : Bool
  selectedCandidateProvenancePreserved : Bool
  candidateSetDigestPreserved : Bool
  candidateSetNonemptyPreserved : Bool
  candidateIdsUniquePreserved : Bool
  memoryOverwritePreserved : Bool
  truthAuthorityPreserved : Bool
  blockerReleasePreserved : Bool
  nextCycleCycleClosed : Bool
  subsequentCycleReplanRequested : Bool
  subsequentCycleCandidateGenerationStarted : Bool
  subsequentCycleCandidateSetMaterialized : Bool
  candidateCount : Nat
  evaluationInputCount : Nat
  evaluationCount : Nat
  evaluationSetDigestBound : Bool
  allMaterializedCandidatesEvaluated : Bool
  evaluationScoreBoundsValid : Bool
  subsequentCycleCandidateEvaluationReceiptOnly : Bool
  subsequentCycleCandidateEvaluationsRecorded : Bool
  subsequentCycleEvaluationOrderIsNotSelection : Bool
  subsequentCycleCandidateReviewRequested : Bool
  subsequentCycleCandidateSelected : Bool
  subsequentCycleAdmissionRequested : Bool
  sourceRequired : sourceReceiptBound = true
  provenanceRequired : selectedCandidateProvenancePreserved = true
  candidateSetDigestRequired : candidateSetDigestPreserved = true
  candidateSetNonemptyRequired : candidateSetNonemptyPreserved = true
  candidateIdsUniqueRequired : candidateIdsUniquePreserved = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  truthAuthorityRequired : truthAuthorityPreserved = true
  blockerReleaseRequired : blockerReleasePreserved = true
  priorCloseoutRequired : nextCycleCycleClosed = true
  replanRequestedRequired : subsequentCycleReplanRequested = true
  generationStartedRequired : subsequentCycleCandidateGenerationStarted = true
  candidateSetMaterializedRequired : subsequentCycleCandidateSetMaterialized = true
  candidateCountPositive : 0 < candidateCount
  evaluationInputCountExact : evaluationInputCount = candidateCount
  evaluationCountExact : evaluationCount = candidateCount
  evaluationSetDigestRequired : evaluationSetDigestBound = true
  allCandidatesEvaluatedRequired : allMaterializedCandidatesEvaluated = true
  scoreBoundsRequired : evaluationScoreBoundsValid = true
  evaluationOnlyRequired : subsequentCycleCandidateEvaluationReceiptOnly = true
  evaluationsRecordedRequired : subsequentCycleCandidateEvaluationsRecorded = true
  evaluationOrderNonSelectionRequired : subsequentCycleEvaluationOrderIsNotSelection = true
  candidateReviewForbidden : subsequentCycleCandidateReviewRequested = false
  candidateSelectionForbidden : subsequentCycleCandidateSelected = false
  admissionRequestForbidden : subsequentCycleAdmissionRequested = false

structure SubsequentCycleCandidateEvaluationReceiptBoundary where
  receiptOwnedByPlanOS : Bool
  sourceCandidateSetMaterializationReceiptPreserved : Bool
  selectedCandidateProvenancePreserved : Bool
  candidateSetDigestPreserved : Bool
  candidateSetNonemptyPreserved : Bool
  candidateIdsUniquePreserved : Bool
  memoryOverwritePreserved : Bool
  truthAuthorityPreserved : Bool
  blockerReleasePreserved : Bool
  nextCycleCycleClosed : Bool
  subsequentCycleReplanRequested : Bool
  subsequentCycleCandidateGenerationStarted : Bool
  subsequentCycleCandidateSetMaterialized : Bool
  subsequentCycleCandidateEvaluationReceiptOnly : Bool
  subsequentCycleAllMaterializedCandidatesEvaluated : Bool
  subsequentCycleCandidateEvaluationCountExact : Bool
  subsequentCycleCandidateEvaluationScoreBoundsValid : Bool
  subsequentCycleCandidateEvaluationsRecorded : Bool
  subsequentCycleEvaluationOrderIsNotSelection : Bool
  subsequentCycleCandidateReviewRequested : Bool
  subsequentCycleCandidateSelected : Bool
  subsequentCycleAdmissionRequested : Bool
  ownerRequired : receiptOwnedByPlanOS = true
  sourcePreservedRequired : sourceCandidateSetMaterializationReceiptPreserved = true
  provenanceRequired : selectedCandidateProvenancePreserved = true
  candidateSetDigestRequired : candidateSetDigestPreserved = true
  candidateSetNonemptyRequired : candidateSetNonemptyPreserved = true
  candidateIdsUniqueRequired : candidateIdsUniquePreserved = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  truthAuthorityRequired : truthAuthorityPreserved = true
  blockerReleaseRequired : blockerReleasePreserved = true
  priorCloseoutRequired : nextCycleCycleClosed = true
  replanRequestedRequired : subsequentCycleReplanRequested = true
  generationStartedRequired : subsequentCycleCandidateGenerationStarted = true
  candidateSetMaterializedRequired : subsequentCycleCandidateSetMaterialized = true
  evaluationOnlyRequired : subsequentCycleCandidateEvaluationReceiptOnly = true
  allCandidatesEvaluatedRequired : subsequentCycleAllMaterializedCandidatesEvaluated = true
  evaluationCountExactRequired : subsequentCycleCandidateEvaluationCountExact = true
  scoreBoundsRequired : subsequentCycleCandidateEvaluationScoreBoundsValid = true
  evaluationsRecordedRequired : subsequentCycleCandidateEvaluationsRecorded = true
  evaluationOrderNonSelectionRequired : subsequentCycleEvaluationOrderIsNotSelection = true
  candidateReviewForbidden : subsequentCycleCandidateReviewRequested = false
  candidateSelectionForbidden : subsequentCycleCandidateSelected = false
  admissionRequestForbidden : subsequentCycleAdmissionRequested = false

structure PlanOSSubsequentCycleCandidateEvaluationReceiptBridge where
  Digest : Type
  digestOf : SubsequentCycleCandidateEvaluationReceiptSurface →
    SubsequentCycleCandidateEvaluationReceiptBoundary → Nat → Digest
  surface : SubsequentCycleCandidateEvaluationReceiptSurface
  boundary : SubsequentCycleCandidateEvaluationReceiptBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  recorderNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  recorderTruthForbidden : recorderNonAuthority.truthAuthority = false

namespace PlanOSSubsequentCycleCandidateEvaluationReceiptBridge

theorem source_materializes_nonempty_unique_set_without_selection
    (b : PlanOSSubsequentCycleCandidateEvaluationReceiptBridge) :
    b.surface.sourceMaterialization.subsequentCycleCandidateSetMaterializationReceiptOnly = true ∧
      b.surface.sourceMaterialization.subsequentCycleCandidateSetMaterialized = true ∧
      0 < b.surface.sourceMaterialization.candidateCount ∧
      b.surface.sourceMaterialization.candidateIdsUnique = true ∧
      b.surface.sourceMaterialization.subsequentCycleCandidateSelected = false ∧
      b.surface.sourceMaterialization.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.surface.sourceMaterialization.materializationOnlyRequired,
    b.surface.sourceMaterialization.candidateSetMaterializedRequired,
    b.surface.sourceMaterialization.candidateCountPositive,
    b.surface.sourceMaterialization.candidateIdsUniqueRequired,
    b.surface.sourceMaterialization.candidateSelectionForbidden,
    b.surface.sourceMaterialization.admissionRequestForbidden⟩

theorem evaluation_preserves_candidate_set_and_authority_chain
    (b : PlanOSSubsequentCycleCandidateEvaluationReceiptBridge) :
    b.surface.sourceReceiptBound = true ∧
      b.surface.selectedCandidateProvenancePreserved = true ∧
      b.surface.candidateSetDigestPreserved = true ∧
      b.surface.candidateSetNonemptyPreserved = true ∧
      b.surface.candidateIdsUniquePreserved = true ∧
      b.surface.memoryOverwritePreserved = true ∧
      b.surface.truthAuthorityPreserved = true ∧
      b.surface.blockerReleasePreserved = true ∧
      b.surface.nextCycleCycleClosed = true ∧
      b.surface.subsequentCycleReplanRequested = true ∧
      b.surface.subsequentCycleCandidateGenerationStarted = true ∧
      b.surface.subsequentCycleCandidateSetMaterialized = true := by
  exact ⟨b.surface.sourceRequired, b.surface.provenanceRequired,
    b.surface.candidateSetDigestRequired, b.surface.candidateSetNonemptyRequired,
    b.surface.candidateIdsUniqueRequired, b.surface.memoryOverwriteRequired,
    b.surface.truthAuthorityRequired, b.surface.blockerReleaseRequired,
    b.surface.priorCloseoutRequired, b.surface.replanRequestedRequired,
    b.surface.generationStartedRequired, b.surface.candidateSetMaterializedRequired⟩

theorem evaluation_is_complete_exact_bounded_and_digest_bound
    (b : PlanOSSubsequentCycleCandidateEvaluationReceiptBridge) :
    0 < b.surface.candidateCount ∧
      b.surface.evaluationInputCount = b.surface.candidateCount ∧
      b.surface.evaluationCount = b.surface.candidateCount ∧
      b.surface.evaluationSetDigestBound = true ∧
      b.surface.allMaterializedCandidatesEvaluated = true ∧
      b.surface.evaluationScoreBoundsValid = true := by
  exact ⟨b.surface.candidateCountPositive, b.surface.evaluationInputCountExact,
    b.surface.evaluationCountExact, b.surface.evaluationSetDigestRequired,
    b.surface.allCandidatesEvaluatedRequired, b.surface.scoreBoundsRequired⟩

theorem receipt_records_evaluations_without_review_selection_or_admission
    (b : PlanOSSubsequentCycleCandidateEvaluationReceiptBridge) :
    b.surface.subsequentCycleCandidateEvaluationReceiptOnly = true ∧
      b.surface.subsequentCycleCandidateEvaluationsRecorded = true ∧
      b.surface.subsequentCycleEvaluationOrderIsNotSelection = true ∧
      b.surface.subsequentCycleCandidateReviewRequested = false ∧
      b.surface.subsequentCycleCandidateSelected = false ∧
      b.surface.subsequentCycleAdmissionRequested = false ∧
      b.recorderNonAuthority.truthAuthority = false := by
  exact ⟨b.surface.evaluationOnlyRequired, b.surface.evaluationsRecordedRequired,
    b.surface.evaluationOrderNonSelectionRequired, b.surface.candidateReviewForbidden,
    b.surface.candidateSelectionForbidden, b.surface.admissionRequestForbidden,
    b.recorderTruthForbidden⟩

theorem boundary_is_candidate_evaluation_receipt_only
    (b : PlanOSSubsequentCycleCandidateEvaluationReceiptBridge) :
    b.boundary.receiptOwnedByPlanOS = true ∧
      b.boundary.sourceCandidateSetMaterializationReceiptPreserved = true ∧
      b.boundary.selectedCandidateProvenancePreserved = true ∧
      b.boundary.candidateSetDigestPreserved = true ∧
      b.boundary.candidateSetNonemptyPreserved = true ∧
      b.boundary.candidateIdsUniquePreserved = true ∧
      b.boundary.memoryOverwritePreserved = true ∧
      b.boundary.truthAuthorityPreserved = true ∧
      b.boundary.blockerReleasePreserved = true ∧
      b.boundary.nextCycleCycleClosed = true ∧
      b.boundary.subsequentCycleReplanRequested = true ∧
      b.boundary.subsequentCycleCandidateGenerationStarted = true ∧
      b.boundary.subsequentCycleCandidateSetMaterialized = true ∧
      b.boundary.subsequentCycleCandidateEvaluationReceiptOnly = true ∧
      b.boundary.subsequentCycleAllMaterializedCandidatesEvaluated = true ∧
      b.boundary.subsequentCycleCandidateEvaluationCountExact = true ∧
      b.boundary.subsequentCycleCandidateEvaluationScoreBoundsValid = true ∧
      b.boundary.subsequentCycleCandidateEvaluationsRecorded = true ∧
      b.boundary.subsequentCycleEvaluationOrderIsNotSelection = true ∧
      b.boundary.subsequentCycleCandidateReviewRequested = false ∧
      b.boundary.subsequentCycleCandidateSelected = false ∧
      b.boundary.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.provenanceRequired, b.boundary.candidateSetDigestRequired,
    b.boundary.candidateSetNonemptyRequired, b.boundary.candidateIdsUniqueRequired,
    b.boundary.memoryOverwriteRequired, b.boundary.truthAuthorityRequired,
    b.boundary.blockerReleaseRequired, b.boundary.priorCloseoutRequired,
    b.boundary.replanRequestedRequired, b.boundary.generationStartedRequired,
    b.boundary.candidateSetMaterializedRequired, b.boundary.evaluationOnlyRequired,
    b.boundary.allCandidatesEvaluatedRequired, b.boundary.evaluationCountExactRequired,
    b.boundary.scoreBoundsRequired, b.boundary.evaluationsRecordedRequired,
    b.boundary.evaluationOrderNonSelectionRequired, b.boundary.candidateReviewForbidden,
    b.boundary.candidateSelectionForbidden, b.boundary.admissionRequestForbidden⟩

theorem history_appends_one_candidate_evaluation_receipt
    (b : PlanOSSubsequentCycleCandidateEvaluationReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact
    (b : PlanOSSubsequentCycleCandidateEvaluationReceiptBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSSubsequentCycleCandidateEvaluationReceiptBridge

end PlanOS
end KUOS
