import Mathlib
import KUOS.PlanOS.SubsequentCycleCandidateGenerationStartReceiptV0_65

namespace KUOS
namespace PlanOS

structure SubsequentCycleCandidateSetMaterializationReceiptSurface where
  sourceStart : SubsequentCycleCandidateGenerationStartReceiptSurface
  sourceBoundary : SubsequentCycleCandidateGenerationStartReceiptBoundary
  sourceStartBound : Bool
  selectedCandidateProvenanceBound : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  truthAuthorityAuthorizationGrantPreserved : Bool
  truthAuthorityPreserved : Bool
  truthAuthorityCycleClosedPreserved : Bool
  blockerReleaseAuthorizationRequestPreserved : Bool
  blockerReleaseAuthorizationGrantPreserved : Bool
  blockerReleasePreserved : Bool
  blockerReleaseCycleClosedPreserved : Bool
  nextCycleAdmissionRequestPreserved : Bool
  nextCycleAdmissionGrantPreserved : Bool
  nextCycleStartReceiptPreserved : Bool
  nextCycleCloseoutReceiptPreserved : Bool
  subsequentCycleReplanRequestPreserved : Bool
  candidateGenerationStartReceiptPreserved : Bool
  nextCycleCycleClosed : Bool
  subsequentCycleReplanRequested : Bool
  subsequentCycleCandidateGenerationStarted : Bool
  candidateInputCount : Nat
  candidateCount : Nat
  candidateSetDigestBound : Bool
  candidateIdsUnique : Bool
  subsequentCycleCandidateSetMaterializationReceiptOnly : Bool
  subsequentCycleCandidateSetMaterialized : Bool
  subsequentCycleCandidateSelected : Bool
  subsequentCycleAdmissionRequested : Bool
  sourceRequired : sourceStartBound = true
  provenanceRequired : selectedCandidateProvenanceBound = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  memoryCloseoutRequired : memoryOverwriteCloseoutPreserved = true
  cyclePreservedRequired : cycleClosedPreserved = true
  truthGrantPreservedRequired : truthAuthorityAuthorizationGrantPreserved = true
  truthPreservedRequired : truthAuthorityPreserved = true
  truthCyclePreservedRequired : truthAuthorityCycleClosedPreserved = true
  blockerRequestPreservedRequired : blockerReleaseAuthorizationRequestPreserved = true
  blockerGrantPreservedRequired : blockerReleaseAuthorizationGrantPreserved = true
  blockerReleasePreservedRequired : blockerReleasePreserved = true
  blockerCyclePreservedRequired : blockerReleaseCycleClosedPreserved = true
  admissionRequestPreservedRequired : nextCycleAdmissionRequestPreserved = true
  admissionGrantPreservedRequired : nextCycleAdmissionGrantPreserved = true
  startReceiptPreservedRequired : nextCycleStartReceiptPreserved = true
  closeoutReceiptPreservedRequired : nextCycleCloseoutReceiptPreserved = true
  replanRequestPreservedRequired : subsequentCycleReplanRequestPreserved = true
  generationStartPreservedRequired : candidateGenerationStartReceiptPreserved = true
  priorCloseoutRequired : nextCycleCycleClosed = true
  replanRequestedRequired : subsequentCycleReplanRequested = true
  generationStartedRequired : subsequentCycleCandidateGenerationStarted = true
  candidateCountExact : candidateCount = candidateInputCount
  candidateCountPositive : 0 < candidateCount
  candidateSetDigestRequired : candidateSetDigestBound = true
  candidateIdsUniqueRequired : candidateIdsUnique = true
  materializationOnlyRequired : subsequentCycleCandidateSetMaterializationReceiptOnly = true
  candidateSetMaterializedRequired : subsequentCycleCandidateSetMaterialized = true
  candidateSelectionForbidden : subsequentCycleCandidateSelected = false
  admissionRequestForbidden : subsequentCycleAdmissionRequested = false

structure SubsequentCycleCandidateSetMaterializationReceiptBoundary where
  receiptOwnedByPlanOS : Bool
  sourceCandidateGenerationStartReceiptPreserved : Bool
  selectedCandidateProvenanceBoundToGenerationStart : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  truthAuthorityAuthorizationGrantPreserved : Bool
  truthAuthorityPreserved : Bool
  truthAuthorityCycleClosedPreserved : Bool
  blockerReleaseAuthorizationRequestPreserved : Bool
  blockerReleaseAuthorizationGrantPreserved : Bool
  blockerReleasePreserved : Bool
  blockerReleaseCycleClosedPreserved : Bool
  nextCycleAdmissionRequestPreserved : Bool
  nextCycleAdmissionGrantPreserved : Bool
  nextCycleStartReceiptPreserved : Bool
  nextCycleCloseoutReceiptPreserved : Bool
  subsequentCycleReplanRequestPreserved : Bool
  candidateGenerationStartReceiptPreserved : Bool
  nextCycleCycleClosed : Bool
  subsequentCycleReplanRequested : Bool
  subsequentCycleCandidateGenerationStarted : Bool
  subsequentCycleCandidateSetMaterializationReceiptOnly : Bool
  subsequentCycleCandidateSetMaterialized : Bool
  subsequentCycleCandidateSetNonempty : Bool
  subsequentCycleCandidateIdsUnique : Bool
  subsequentCycleCandidateSelected : Bool
  subsequentCycleAdmissionRequested : Bool
  ownerRequired : receiptOwnedByPlanOS = true
  sourcePreservedRequired : sourceCandidateGenerationStartReceiptPreserved = true
  provenanceRequired : selectedCandidateProvenanceBoundToGenerationStart = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  memoryCloseoutRequired : memoryOverwriteCloseoutPreserved = true
  cyclePreservedRequired : cycleClosedPreserved = true
  truthGrantPreservedRequired : truthAuthorityAuthorizationGrantPreserved = true
  truthPreservedRequired : truthAuthorityPreserved = true
  truthCyclePreservedRequired : truthAuthorityCycleClosedPreserved = true
  blockerRequestPreservedRequired : blockerReleaseAuthorizationRequestPreserved = true
  blockerGrantPreservedRequired : blockerReleaseAuthorizationGrantPreserved = true
  blockerReleasePreservedRequired : blockerReleasePreserved = true
  blockerCyclePreservedRequired : blockerReleaseCycleClosedPreserved = true
  admissionRequestPreservedRequired : nextCycleAdmissionRequestPreserved = true
  admissionGrantPreservedRequired : nextCycleAdmissionGrantPreserved = true
  startReceiptPreservedRequired : nextCycleStartReceiptPreserved = true
  closeoutReceiptPreservedRequired : nextCycleCloseoutReceiptPreserved = true
  replanRequestPreservedRequired : subsequentCycleReplanRequestPreserved = true
  generationStartPreservedRequired : candidateGenerationStartReceiptPreserved = true
  priorCloseoutRequired : nextCycleCycleClosed = true
  replanRequestedRequired : subsequentCycleReplanRequested = true
  generationStartedRequired : subsequentCycleCandidateGenerationStarted = true
  materializationOnlyRequired : subsequentCycleCandidateSetMaterializationReceiptOnly = true
  candidateSetMaterializedRequired : subsequentCycleCandidateSetMaterialized = true
  candidateSetNonemptyRequired : subsequentCycleCandidateSetNonempty = true
  candidateIdsUniqueRequired : subsequentCycleCandidateIdsUnique = true
  candidateSelectionForbidden : subsequentCycleCandidateSelected = false
  admissionRequestForbidden : subsequentCycleAdmissionRequested = false

structure PlanOSSubsequentCycleCandidateSetMaterializationReceiptBridge where
  Digest : Type
  digestOf : SubsequentCycleCandidateSetMaterializationReceiptSurface →
    SubsequentCycleCandidateSetMaterializationReceiptBoundary → Nat → Digest
  surface : SubsequentCycleCandidateSetMaterializationReceiptSurface
  boundary : SubsequentCycleCandidateSetMaterializationReceiptBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  recorderNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  recorderTruthForbidden : recorderNonAuthority.truthAuthority = false

namespace PlanOSSubsequentCycleCandidateSetMaterializationReceiptBridge

theorem source_start_records_generation_without_materialized_set
    (b : PlanOSSubsequentCycleCandidateSetMaterializationReceiptBridge) :
    b.surface.sourceStart.subsequentCycleCandidateGenerationStartReceiptOnly = true ∧
      b.surface.sourceStart.subsequentCycleCandidateGenerationStarted = true ∧
      b.surface.sourceStart.subsequentCycleCandidateSetMaterialized = false ∧
      b.surface.sourceStart.subsequentCycleCandidateSelected = false ∧
      b.surface.sourceStart.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.surface.sourceStart.startReceiptOnlyRequired,
    b.surface.sourceStart.candidateGenerationStartRequired,
    b.surface.sourceStart.candidateSetMaterializationForbidden,
    b.surface.sourceStart.candidateSelectionForbidden,
    b.surface.sourceStart.admissionRequestForbidden⟩

theorem materialization_preserves_closed_authority_and_generation_chain
    (b : PlanOSSubsequentCycleCandidateSetMaterializationReceiptBridge) :
    b.surface.sourceStartBound = true ∧
      b.surface.selectedCandidateProvenanceBound = true ∧
      b.surface.memoryOverwritePreserved = true ∧
      b.surface.memoryOverwriteCloseoutPreserved = true ∧
      b.surface.cycleClosedPreserved = true ∧
      b.surface.truthAuthorityAuthorizationGrantPreserved = true ∧
      b.surface.truthAuthorityPreserved = true ∧
      b.surface.truthAuthorityCycleClosedPreserved = true ∧
      b.surface.blockerReleaseAuthorizationRequestPreserved = true ∧
      b.surface.blockerReleaseAuthorizationGrantPreserved = true ∧
      b.surface.blockerReleasePreserved = true ∧
      b.surface.blockerReleaseCycleClosedPreserved = true ∧
      b.surface.nextCycleAdmissionRequestPreserved = true ∧
      b.surface.nextCycleAdmissionGrantPreserved = true ∧
      b.surface.nextCycleStartReceiptPreserved = true ∧
      b.surface.nextCycleCloseoutReceiptPreserved = true ∧
      b.surface.subsequentCycleReplanRequestPreserved = true ∧
      b.surface.candidateGenerationStartReceiptPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.provenanceRequired,
    b.surface.memoryOverwriteRequired, b.surface.memoryCloseoutRequired,
    b.surface.cyclePreservedRequired, b.surface.truthGrantPreservedRequired,
    b.surface.truthPreservedRequired, b.surface.truthCyclePreservedRequired,
    b.surface.blockerRequestPreservedRequired, b.surface.blockerGrantPreservedRequired,
    b.surface.blockerReleasePreservedRequired, b.surface.blockerCyclePreservedRequired,
    b.surface.admissionRequestPreservedRequired, b.surface.admissionGrantPreservedRequired,
    b.surface.startReceiptPreservedRequired, b.surface.closeoutReceiptPreservedRequired,
    b.surface.replanRequestPreservedRequired, b.surface.generationStartPreservedRequired⟩

theorem candidate_set_is_nonempty_exact_and_digest_bound
    (b : PlanOSSubsequentCycleCandidateSetMaterializationReceiptBridge) :
    b.surface.candidateCount = b.surface.candidateInputCount ∧
      0 < b.surface.candidateCount ∧
      b.surface.candidateSetDigestBound = true ∧
      b.surface.candidateIdsUnique = true := by
  exact ⟨b.surface.candidateCountExact, b.surface.candidateCountPositive,
    b.surface.candidateSetDigestRequired, b.surface.candidateIdsUniqueRequired⟩

theorem receipt_materializes_candidate_set_without_selection_or_admission
    (b : PlanOSSubsequentCycleCandidateSetMaterializationReceiptBridge) :
    b.surface.nextCycleCycleClosed = true ∧
      b.surface.subsequentCycleReplanRequested = true ∧
      b.surface.subsequentCycleCandidateGenerationStarted = true ∧
      b.surface.subsequentCycleCandidateSetMaterializationReceiptOnly = true ∧
      b.surface.subsequentCycleCandidateSetMaterialized = true ∧
      b.surface.subsequentCycleCandidateSelected = false ∧
      b.surface.subsequentCycleAdmissionRequested = false ∧
      b.recorderNonAuthority.truthAuthority = false := by
  exact ⟨b.surface.priorCloseoutRequired, b.surface.replanRequestedRequired,
    b.surface.generationStartedRequired, b.surface.materializationOnlyRequired,
    b.surface.candidateSetMaterializedRequired, b.surface.candidateSelectionForbidden,
    b.surface.admissionRequestForbidden, b.recorderTruthForbidden⟩

theorem boundary_is_candidate_set_materialization_receipt_only
    (b : PlanOSSubsequentCycleCandidateSetMaterializationReceiptBridge) :
    b.boundary.receiptOwnedByPlanOS = true ∧
      b.boundary.sourceCandidateGenerationStartReceiptPreserved = true ∧
      b.boundary.selectedCandidateProvenanceBoundToGenerationStart = true ∧
      b.boundary.memoryOverwritePreserved = true ∧
      b.boundary.memoryOverwriteCloseoutPreserved = true ∧
      b.boundary.cycleClosedPreserved = true ∧
      b.boundary.truthAuthorityAuthorizationGrantPreserved = true ∧
      b.boundary.truthAuthorityPreserved = true ∧
      b.boundary.truthAuthorityCycleClosedPreserved = true ∧
      b.boundary.blockerReleaseAuthorizationRequestPreserved = true ∧
      b.boundary.blockerReleaseAuthorizationGrantPreserved = true ∧
      b.boundary.blockerReleasePreserved = true ∧
      b.boundary.blockerReleaseCycleClosedPreserved = true ∧
      b.boundary.nextCycleAdmissionRequestPreserved = true ∧
      b.boundary.nextCycleAdmissionGrantPreserved = true ∧
      b.boundary.nextCycleStartReceiptPreserved = true ∧
      b.boundary.nextCycleCloseoutReceiptPreserved = true ∧
      b.boundary.subsequentCycleReplanRequestPreserved = true ∧
      b.boundary.candidateGenerationStartReceiptPreserved = true ∧
      b.boundary.nextCycleCycleClosed = true ∧
      b.boundary.subsequentCycleReplanRequested = true ∧
      b.boundary.subsequentCycleCandidateGenerationStarted = true ∧
      b.boundary.subsequentCycleCandidateSetMaterializationReceiptOnly = true ∧
      b.boundary.subsequentCycleCandidateSetMaterialized = true ∧
      b.boundary.subsequentCycleCandidateSetNonempty = true ∧
      b.boundary.subsequentCycleCandidateIdsUnique = true ∧
      b.boundary.subsequentCycleCandidateSelected = false ∧
      b.boundary.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.provenanceRequired, b.boundary.memoryOverwriteRequired,
    b.boundary.memoryCloseoutRequired, b.boundary.cyclePreservedRequired,
    b.boundary.truthGrantPreservedRequired, b.boundary.truthPreservedRequired,
    b.boundary.truthCyclePreservedRequired, b.boundary.blockerRequestPreservedRequired,
    b.boundary.blockerGrantPreservedRequired, b.boundary.blockerReleasePreservedRequired,
    b.boundary.blockerCyclePreservedRequired, b.boundary.admissionRequestPreservedRequired,
    b.boundary.admissionGrantPreservedRequired, b.boundary.startReceiptPreservedRequired,
    b.boundary.closeoutReceiptPreservedRequired, b.boundary.replanRequestPreservedRequired,
    b.boundary.generationStartPreservedRequired, b.boundary.priorCloseoutRequired,
    b.boundary.replanRequestedRequired, b.boundary.generationStartedRequired,
    b.boundary.materializationOnlyRequired, b.boundary.candidateSetMaterializedRequired,
    b.boundary.candidateSetNonemptyRequired, b.boundary.candidateIdsUniqueRequired,
    b.boundary.candidateSelectionForbidden, b.boundary.admissionRequestForbidden⟩

theorem history_appends_one_candidate_set_materialization_receipt
    (b : PlanOSSubsequentCycleCandidateSetMaterializationReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact
    (b : PlanOSSubsequentCycleCandidateSetMaterializationReceiptBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSSubsequentCycleCandidateSetMaterializationReceiptBridge

end PlanOS
end KUOS
