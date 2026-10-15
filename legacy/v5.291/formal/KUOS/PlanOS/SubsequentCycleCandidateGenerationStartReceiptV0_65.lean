import Mathlib
import KUOS.PlanOS.SubsequentCycleReplanRequestV0_64

namespace KUOS
namespace PlanOS

structure SubsequentCycleCandidateGenerationStartReceiptSurface where
  sourceRequest : SubsequentCycleReplanRequestSurface
  sourceBoundary : SubsequentCycleReplanRequestBoundary
  sourceRequestBound : Bool
  selectedCandidateBoundToRequest : Bool
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
  nextCycleAdmissionRequested : Bool
  nextCycleAdmissionGranted : Bool
  nextCycleStarted : Bool
  nextCycleCycleClosed : Bool
  subsequentCycleReplanRequested : Bool
  subsequentCycleCandidateGenerationStartReceiptOnly : Bool
  subsequentCycleCandidateGenerationStarted : Bool
  subsequentCycleCandidateSetMaterialized : Bool
  subsequentCycleCandidateSelected : Bool
  subsequentCycleAdmissionRequested : Bool
  sourceRequired : sourceRequestBound = true
  selectedBoundRequired : selectedCandidateBoundToRequest = true
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
  priorRequestRequired : nextCycleAdmissionRequested = true
  priorAdmissionRequired : nextCycleAdmissionGranted = true
  priorStartRequired : nextCycleStarted = true
  priorCloseoutRequired : nextCycleCycleClosed = true
  replanRequestedRequired : subsequentCycleReplanRequested = true
  startReceiptOnlyRequired : subsequentCycleCandidateGenerationStartReceiptOnly = true
  candidateGenerationStartRequired : subsequentCycleCandidateGenerationStarted = true
  candidateSetMaterializationForbidden : subsequentCycleCandidateSetMaterialized = false
  candidateSelectionForbidden : subsequentCycleCandidateSelected = false
  admissionRequestForbidden : subsequentCycleAdmissionRequested = false

structure SubsequentCycleCandidateGenerationStartReceiptBoundary where
  receiptOwnedByPlanOS : Bool
  sourceSubsequentCycleReplanRequestPreserved : Bool
  selectedCandidateBoundToReplanRequest : Bool
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
  nextCycleAdmissionRequested : Bool
  nextCycleAdmissionGranted : Bool
  nextCycleStarted : Bool
  nextCycleCycleClosed : Bool
  subsequentCycleReplanRequested : Bool
  subsequentCycleCandidateGenerationStartReceiptOnly : Bool
  subsequentCycleCandidateGenerationStarted : Bool
  subsequentCycleCandidateSetMaterialized : Bool
  subsequentCycleCandidateSelected : Bool
  subsequentCycleAdmissionRequested : Bool
  ownerRequired : receiptOwnedByPlanOS = true
  sourcePreservedRequired : sourceSubsequentCycleReplanRequestPreserved = true
  selectedBoundRequired : selectedCandidateBoundToReplanRequest = true
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
  priorRequestRequired : nextCycleAdmissionRequested = true
  priorAdmissionRequired : nextCycleAdmissionGranted = true
  priorStartRequired : nextCycleStarted = true
  priorCloseoutRequired : nextCycleCycleClosed = true
  replanRequestedRequired : subsequentCycleReplanRequested = true
  startReceiptOnlyRequired : subsequentCycleCandidateGenerationStartReceiptOnly = true
  candidateGenerationStartRequired : subsequentCycleCandidateGenerationStarted = true
  candidateSetMaterializationForbidden : subsequentCycleCandidateSetMaterialized = false
  candidateSelectionForbidden : subsequentCycleCandidateSelected = false
  admissionRequestForbidden : subsequentCycleAdmissionRequested = false

structure PlanOSSubsequentCycleCandidateGenerationStartReceiptBridge where
  Digest : Type
  digestOf : SubsequentCycleCandidateGenerationStartReceiptSurface →
    SubsequentCycleCandidateGenerationStartReceiptBoundary → Nat → Digest
  surface : SubsequentCycleCandidateGenerationStartReceiptSurface
  boundary : SubsequentCycleCandidateGenerationStartReceiptBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  recorderNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  recorderTruthForbidden : recorderNonAuthority.truthAuthority = false

namespace PlanOSSubsequentCycleCandidateGenerationStartReceiptBridge

theorem source_request_opens_replan_without_candidate_generation
    (b : PlanOSSubsequentCycleCandidateGenerationStartReceiptBridge) :
    b.surface.sourceRequest.subsequentCycleReplanRequestOnly = true ∧
      b.surface.sourceRequest.subsequentCycleReplanRequested = true ∧
      b.surface.sourceRequest.subsequentCycleCandidateGenerationStarted = false ∧
      b.surface.sourceRequest.subsequentCycleAdmissionRequested = false ∧
      b.surface.sourceBoundary.subsequentCycleCandidateGenerationStarted = false ∧
      b.surface.sourceBoundary.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.surface.sourceRequest.requestOnlyRequired,
    b.surface.sourceRequest.replanRequestRequired,
    b.surface.sourceRequest.candidateGenerationForbidden,
    b.surface.sourceRequest.admissionRequestForbidden,
    b.surface.sourceBoundary.candidateGenerationForbidden,
    b.surface.sourceBoundary.admissionRequestForbidden⟩

theorem start_receipt_preserves_closed_authority_and_cycle_chain
    (b : PlanOSSubsequentCycleCandidateGenerationStartReceiptBridge) :
    b.surface.sourceRequestBound = true ∧
      b.surface.selectedCandidateBoundToRequest = true ∧
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
      b.surface.subsequentCycleReplanRequestPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.memoryOverwriteRequired, b.surface.memoryCloseoutRequired,
    b.surface.cyclePreservedRequired, b.surface.truthGrantPreservedRequired,
    b.surface.truthPreservedRequired, b.surface.truthCyclePreservedRequired,
    b.surface.blockerRequestPreservedRequired, b.surface.blockerGrantPreservedRequired,
    b.surface.blockerReleasePreservedRequired, b.surface.blockerCyclePreservedRequired,
    b.surface.admissionRequestPreservedRequired, b.surface.admissionGrantPreservedRequired,
    b.surface.startReceiptPreservedRequired, b.surface.closeoutReceiptPreservedRequired,
    b.surface.replanRequestPreservedRequired⟩

theorem receipt_starts_candidate_generation_without_materialization_selection_or_admission
    (b : PlanOSSubsequentCycleCandidateGenerationStartReceiptBridge) :
    b.surface.nextCycleAdmissionRequested = true ∧
      b.surface.nextCycleAdmissionGranted = true ∧
      b.surface.nextCycleStarted = true ∧
      b.surface.nextCycleCycleClosed = true ∧
      b.surface.subsequentCycleReplanRequested = true ∧
      b.surface.subsequentCycleCandidateGenerationStartReceiptOnly = true ∧
      b.surface.subsequentCycleCandidateGenerationStarted = true ∧
      b.surface.subsequentCycleCandidateSetMaterialized = false ∧
      b.surface.subsequentCycleCandidateSelected = false ∧
      b.surface.subsequentCycleAdmissionRequested = false ∧
      b.recorderNonAuthority.truthAuthority = false := by
  exact ⟨b.surface.priorRequestRequired, b.surface.priorAdmissionRequired,
    b.surface.priorStartRequired, b.surface.priorCloseoutRequired,
    b.surface.replanRequestedRequired, b.surface.startReceiptOnlyRequired,
    b.surface.candidateGenerationStartRequired,
    b.surface.candidateSetMaterializationForbidden,
    b.surface.candidateSelectionForbidden, b.surface.admissionRequestForbidden,
    b.recorderTruthForbidden⟩

theorem boundary_is_candidate_generation_start_receipt_only
    (b : PlanOSSubsequentCycleCandidateGenerationStartReceiptBridge) :
    b.boundary.receiptOwnedByPlanOS = true ∧
      b.boundary.sourceSubsequentCycleReplanRequestPreserved = true ∧
      b.boundary.selectedCandidateBoundToReplanRequest = true ∧
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
      b.boundary.nextCycleAdmissionRequested = true ∧
      b.boundary.nextCycleAdmissionGranted = true ∧
      b.boundary.nextCycleStarted = true ∧
      b.boundary.nextCycleCycleClosed = true ∧
      b.boundary.subsequentCycleReplanRequested = true ∧
      b.boundary.subsequentCycleCandidateGenerationStartReceiptOnly = true ∧
      b.boundary.subsequentCycleCandidateGenerationStarted = true ∧
      b.boundary.subsequentCycleCandidateSetMaterialized = false ∧
      b.boundary.subsequentCycleCandidateSelected = false ∧
      b.boundary.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.memoryOverwriteRequired,
    b.boundary.memoryCloseoutRequired, b.boundary.cyclePreservedRequired,
    b.boundary.truthGrantPreservedRequired, b.boundary.truthPreservedRequired,
    b.boundary.truthCyclePreservedRequired, b.boundary.blockerRequestPreservedRequired,
    b.boundary.blockerGrantPreservedRequired, b.boundary.blockerReleasePreservedRequired,
    b.boundary.blockerCyclePreservedRequired, b.boundary.admissionRequestPreservedRequired,
    b.boundary.admissionGrantPreservedRequired, b.boundary.startReceiptPreservedRequired,
    b.boundary.closeoutReceiptPreservedRequired, b.boundary.replanRequestPreservedRequired,
    b.boundary.priorRequestRequired, b.boundary.priorAdmissionRequired,
    b.boundary.priorStartRequired, b.boundary.priorCloseoutRequired,
    b.boundary.replanRequestedRequired, b.boundary.startReceiptOnlyRequired,
    b.boundary.candidateGenerationStartRequired,
    b.boundary.candidateSetMaterializationForbidden,
    b.boundary.candidateSelectionForbidden, b.boundary.admissionRequestForbidden⟩

theorem history_appends_one_candidate_generation_start_receipt
    (b : PlanOSSubsequentCycleCandidateGenerationStartReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact
    (b : PlanOSSubsequentCycleCandidateGenerationStartReceiptBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSSubsequentCycleCandidateGenerationStartReceiptBridge

end PlanOS
end KUOS
