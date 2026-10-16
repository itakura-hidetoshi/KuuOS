import Mathlib
import KUOS.PlanOS.NextCycleCloseoutReceiptV0_63

namespace KUOS
namespace PlanOS

structure SubsequentCycleReplanRequestSurface where
  sourceCloseout : NextCycleCloseoutReceiptSurface
  sourceBoundary : NextCycleCloseoutReceiptBoundary
  sourceCloseoutBound : Bool
  selectedCandidateBoundToCloseout : Bool
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
  nextCycleAdmissionRequested : Bool
  nextCycleAdmissionGranted : Bool
  nextCycleStarted : Bool
  nextCycleCycleClosed : Bool
  subsequentCycleReplanRequestOnly : Bool
  subsequentCycleReplanRequested : Bool
  subsequentCycleCandidateGenerationStarted : Bool
  subsequentCycleAdmissionRequested : Bool
  sourceRequired : sourceCloseoutBound = true
  selectedBoundRequired : selectedCandidateBoundToCloseout = true
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
  priorRequestRequired : nextCycleAdmissionRequested = true
  priorAdmissionRequired : nextCycleAdmissionGranted = true
  priorStartRequired : nextCycleStarted = true
  priorCloseoutRequired : nextCycleCycleClosed = true
  requestOnlyRequired : subsequentCycleReplanRequestOnly = true
  replanRequestRequired : subsequentCycleReplanRequested = true
  candidateGenerationForbidden : subsequentCycleCandidateGenerationStarted = false
  admissionRequestForbidden : subsequentCycleAdmissionRequested = false

structure SubsequentCycleReplanRequestBoundary where
  requestOwnedByPlanOS : Bool
  sourceNextCycleCloseoutReceiptPreserved : Bool
  selectedCandidateBoundToNextCycleCloseout : Bool
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
  nextCycleAdmissionRequested : Bool
  nextCycleAdmissionGranted : Bool
  nextCycleStarted : Bool
  nextCycleCycleClosed : Bool
  subsequentCycleReplanRequestOnly : Bool
  subsequentCycleReplanRequested : Bool
  subsequentCycleCandidateGenerationStarted : Bool
  subsequentCycleAdmissionRequested : Bool
  ownerRequired : requestOwnedByPlanOS = true
  sourcePreservedRequired : sourceNextCycleCloseoutReceiptPreserved = true
  selectedBoundRequired : selectedCandidateBoundToNextCycleCloseout = true
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
  priorRequestRequired : nextCycleAdmissionRequested = true
  priorAdmissionRequired : nextCycleAdmissionGranted = true
  priorStartRequired : nextCycleStarted = true
  priorCloseoutRequired : nextCycleCycleClosed = true
  requestOnlyRequired : subsequentCycleReplanRequestOnly = true
  replanRequestRequired : subsequentCycleReplanRequested = true
  candidateGenerationForbidden : subsequentCycleCandidateGenerationStarted = false
  admissionRequestForbidden : subsequentCycleAdmissionRequested = false

structure PlanOSSubsequentCycleReplanRequestBridge where
  Digest : Type
  digestOf : SubsequentCycleReplanRequestSurface → SubsequentCycleReplanRequestBoundary → Nat → Digest
  surface : SubsequentCycleReplanRequestSurface
  boundary : SubsequentCycleReplanRequestBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  recorderNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  recorderTruthForbidden : recorderNonAuthority.truthAuthority = false

namespace PlanOSSubsequentCycleReplanRequestBridge

theorem source_closeout_closes_cycle_without_replan_request
    (b : PlanOSSubsequentCycleReplanRequestBridge) :
    b.surface.sourceCloseout.nextCycleCloseoutReceiptOnly = true ∧
      b.surface.sourceCloseout.nextCycleCycleClosed = true ∧
      b.surface.sourceCloseout.subsequentCycleReplanRequested = false ∧
      b.surface.sourceBoundary.nextCycleCycleClosed = true ∧
      b.surface.sourceBoundary.subsequentCycleReplanRequested = false := by
  exact ⟨b.surface.sourceCloseout.closeoutOnlyRequired,
    b.surface.sourceCloseout.nextCycleCloseoutRequired,
    b.surface.sourceCloseout.subsequentReplanForbidden,
    b.surface.sourceBoundary.nextCycleCloseoutRequired,
    b.surface.sourceBoundary.subsequentReplanForbidden⟩

theorem request_preserves_closed_authority_and_cycle_chain
    (b : PlanOSSubsequentCycleReplanRequestBridge) :
    b.surface.sourceCloseoutBound = true ∧
      b.surface.selectedCandidateBoundToCloseout = true ∧
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
      b.surface.nextCycleCloseoutReceiptPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.memoryOverwriteRequired, b.surface.memoryCloseoutRequired,
    b.surface.cyclePreservedRequired, b.surface.truthGrantPreservedRequired,
    b.surface.truthPreservedRequired, b.surface.truthCyclePreservedRequired,
    b.surface.blockerRequestPreservedRequired, b.surface.blockerGrantPreservedRequired,
    b.surface.blockerReleasePreservedRequired, b.surface.blockerCyclePreservedRequired,
    b.surface.admissionRequestPreservedRequired, b.surface.admissionGrantPreservedRequired,
    b.surface.startReceiptPreservedRequired, b.surface.closeoutReceiptPreservedRequired⟩

theorem request_opens_replan_without_candidate_generation_or_admission
    (b : PlanOSSubsequentCycleReplanRequestBridge) :
    b.surface.nextCycleAdmissionRequested = true ∧
      b.surface.nextCycleAdmissionGranted = true ∧
      b.surface.nextCycleStarted = true ∧
      b.surface.nextCycleCycleClosed = true ∧
      b.surface.subsequentCycleReplanRequestOnly = true ∧
      b.surface.subsequentCycleReplanRequested = true ∧
      b.surface.subsequentCycleCandidateGenerationStarted = false ∧
      b.surface.subsequentCycleAdmissionRequested = false ∧
      b.recorderNonAuthority.truthAuthority = false := by
  exact ⟨b.surface.priorRequestRequired, b.surface.priorAdmissionRequired,
    b.surface.priorStartRequired, b.surface.priorCloseoutRequired,
    b.surface.requestOnlyRequired, b.surface.replanRequestRequired,
    b.surface.candidateGenerationForbidden, b.surface.admissionRequestForbidden,
    b.recorderTruthForbidden⟩

theorem boundary_is_subsequent_cycle_replan_request_only
    (b : PlanOSSubsequentCycleReplanRequestBridge) :
    b.boundary.requestOwnedByPlanOS = true ∧
      b.boundary.sourceNextCycleCloseoutReceiptPreserved = true ∧
      b.boundary.selectedCandidateBoundToNextCycleCloseout = true ∧
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
      b.boundary.nextCycleAdmissionRequested = true ∧
      b.boundary.nextCycleAdmissionGranted = true ∧
      b.boundary.nextCycleStarted = true ∧
      b.boundary.nextCycleCycleClosed = true ∧
      b.boundary.subsequentCycleReplanRequestOnly = true ∧
      b.boundary.subsequentCycleReplanRequested = true ∧
      b.boundary.subsequentCycleCandidateGenerationStarted = false ∧
      b.boundary.subsequentCycleAdmissionRequested = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.memoryOverwriteRequired,
    b.boundary.memoryCloseoutRequired, b.boundary.cyclePreservedRequired,
    b.boundary.truthGrantPreservedRequired, b.boundary.truthPreservedRequired,
    b.boundary.truthCyclePreservedRequired, b.boundary.blockerRequestPreservedRequired,
    b.boundary.blockerGrantPreservedRequired, b.boundary.blockerReleasePreservedRequired,
    b.boundary.blockerCyclePreservedRequired, b.boundary.admissionRequestPreservedRequired,
    b.boundary.admissionGrantPreservedRequired, b.boundary.startReceiptPreservedRequired,
    b.boundary.closeoutReceiptPreservedRequired, b.boundary.priorRequestRequired,
    b.boundary.priorAdmissionRequired, b.boundary.priorStartRequired,
    b.boundary.priorCloseoutRequired, b.boundary.requestOnlyRequired,
    b.boundary.replanRequestRequired, b.boundary.candidateGenerationForbidden,
    b.boundary.admissionRequestForbidden⟩

theorem history_appends_one_subsequent_cycle_replan_request
    (b : PlanOSSubsequentCycleReplanRequestBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSSubsequentCycleReplanRequestBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSSubsequentCycleReplanRequestBridge

end PlanOS
end KUOS
