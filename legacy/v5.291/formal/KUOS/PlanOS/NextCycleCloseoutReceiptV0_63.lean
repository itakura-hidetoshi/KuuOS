import Mathlib
import KUOS.PlanOS.NextCycleStartReceiptV0_62

namespace KUOS
namespace PlanOS

structure NextCycleCloseoutReceiptSurface where
  sourceStart : NextCycleStartReceiptSurface
  sourceBoundary : NextCycleStartReceiptBoundary
  sourceStartBound : Bool
  selectedCandidateBoundToStart : Bool
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
  nextCycleCloseoutReceiptOnly : Bool
  nextCycleAdmissionRequested : Bool
  nextCycleAdmissionGranted : Bool
  nextCycleStarted : Bool
  nextCycleCycleClosed : Bool
  subsequentCycleReplanRequested : Bool
  sourceRequired : sourceStartBound = true
  selectedBoundRequired : selectedCandidateBoundToStart = true
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
  closeoutOnlyRequired : nextCycleCloseoutReceiptOnly = true
  requestRequired : nextCycleAdmissionRequested = true
  admissionRequired : nextCycleAdmissionGranted = true
  nextCycleStartRequired : nextCycleStarted = true
  nextCycleCloseoutRequired : nextCycleCycleClosed = true
  subsequentReplanForbidden : subsequentCycleReplanRequested = false

structure NextCycleCloseoutReceiptBoundary where
  closeoutOwnedByPlanOS : Bool
  sourceNextCycleStartReceiptPreserved : Bool
  selectedCandidateBoundToNextCycleStartReceipt : Bool
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
  nextCycleCloseoutReceiptOnly : Bool
  nextCycleAdmissionRequested : Bool
  nextCycleAdmissionGranted : Bool
  nextCycleStarted : Bool
  nextCycleCycleClosed : Bool
  subsequentCycleReplanRequested : Bool
  ownerRequired : closeoutOwnedByPlanOS = true
  sourcePreservedRequired : sourceNextCycleStartReceiptPreserved = true
  selectedBoundRequired : selectedCandidateBoundToNextCycleStartReceipt = true
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
  closeoutOnlyRequired : nextCycleCloseoutReceiptOnly = true
  requestRequired : nextCycleAdmissionRequested = true
  admissionRequired : nextCycleAdmissionGranted = true
  nextCycleStartRequired : nextCycleStarted = true
  nextCycleCloseoutRequired : nextCycleCycleClosed = true
  subsequentReplanForbidden : subsequentCycleReplanRequested = false

structure PlanOSNextCycleCloseoutReceiptBridge where
  Digest : Type
  digestOf : NextCycleCloseoutReceiptSurface → NextCycleCloseoutReceiptBoundary → Nat → Digest
  surface : NextCycleCloseoutReceiptSurface
  boundary : NextCycleCloseoutReceiptBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  recorderNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  recorderTruthForbidden : recorderNonAuthority.truthAuthority = false

namespace PlanOSNextCycleCloseoutReceiptBridge

theorem source_start_records_started_but_open_cycle
    (b : PlanOSNextCycleCloseoutReceiptBridge) :
    b.surface.sourceStart.nextCycleStartReceiptOnly = true ∧
      b.surface.sourceStart.nextCycleStarted = true ∧
      b.surface.sourceStart.nextCycleCycleClosed = false ∧
      b.surface.sourceBoundary.nextCycleStarted = true ∧
      b.surface.sourceBoundary.nextCycleCycleClosed = false := by
  exact ⟨b.surface.sourceStart.receiptOnlyRequired,
    b.surface.sourceStart.nextCycleStartRequired,
    b.surface.sourceStart.nextCycleCloseoutForbidden,
    b.surface.sourceBoundary.nextCycleStartRequired,
    b.surface.sourceBoundary.nextCycleCloseoutForbidden⟩

theorem closeout_binds_candidate_and_preserves_prior_authority_chain
    (b : PlanOSNextCycleCloseoutReceiptBridge) :
    b.surface.sourceStartBound = true ∧
      b.surface.selectedCandidateBoundToStart = true ∧
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
      b.surface.nextCycleStartReceiptPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.memoryOverwriteRequired, b.surface.memoryCloseoutRequired,
    b.surface.cyclePreservedRequired, b.surface.truthGrantPreservedRequired,
    b.surface.truthPreservedRequired, b.surface.truthCyclePreservedRequired,
    b.surface.blockerRequestPreservedRequired, b.surface.blockerGrantPreservedRequired,
    b.surface.blockerReleasePreservedRequired, b.surface.blockerCyclePreservedRequired,
    b.surface.admissionRequestPreservedRequired, b.surface.admissionGrantPreservedRequired,
    b.surface.startReceiptPreservedRequired⟩

theorem receipt_closes_started_cycle_without_requesting_subsequent_replan
    (b : PlanOSNextCycleCloseoutReceiptBridge) :
    b.surface.nextCycleCloseoutReceiptOnly = true ∧
      b.surface.nextCycleAdmissionRequested = true ∧
      b.surface.nextCycleAdmissionGranted = true ∧
      b.surface.nextCycleStarted = true ∧
      b.surface.nextCycleCycleClosed = true ∧
      b.surface.subsequentCycleReplanRequested = false ∧
      b.boundary.nextCycleCycleClosed = true ∧
      b.boundary.subsequentCycleReplanRequested = false ∧
      b.recorderNonAuthority.truthAuthority = false := by
  exact ⟨b.surface.closeoutOnlyRequired, b.surface.requestRequired,
    b.surface.admissionRequired, b.surface.nextCycleStartRequired,
    b.surface.nextCycleCloseoutRequired, b.surface.subsequentReplanForbidden,
    b.boundary.nextCycleCloseoutRequired, b.boundary.subsequentReplanForbidden,
    b.recorderTruthForbidden⟩

theorem boundary_is_next_cycle_closeout_receipt_only
    (b : PlanOSNextCycleCloseoutReceiptBridge) :
    b.boundary.closeoutOwnedByPlanOS = true ∧
      b.boundary.sourceNextCycleStartReceiptPreserved = true ∧
      b.boundary.selectedCandidateBoundToNextCycleStartReceipt = true ∧
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
      b.boundary.nextCycleCloseoutReceiptOnly = true ∧
      b.boundary.nextCycleAdmissionRequested = true ∧
      b.boundary.nextCycleAdmissionGranted = true ∧
      b.boundary.nextCycleStarted = true ∧
      b.boundary.nextCycleCycleClosed = true ∧
      b.boundary.subsequentCycleReplanRequested = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.memoryOverwriteRequired,
    b.boundary.memoryCloseoutRequired, b.boundary.cyclePreservedRequired,
    b.boundary.truthGrantPreservedRequired, b.boundary.truthPreservedRequired,
    b.boundary.truthCyclePreservedRequired, b.boundary.blockerRequestPreservedRequired,
    b.boundary.blockerGrantPreservedRequired, b.boundary.blockerReleasePreservedRequired,
    b.boundary.blockerCyclePreservedRequired, b.boundary.admissionRequestPreservedRequired,
    b.boundary.admissionGrantPreservedRequired, b.boundary.startReceiptPreservedRequired,
    b.boundary.closeoutOnlyRequired, b.boundary.requestRequired,
    b.boundary.admissionRequired, b.boundary.nextCycleStartRequired,
    b.boundary.nextCycleCloseoutRequired, b.boundary.subsequentReplanForbidden⟩

theorem history_appends_one_next_cycle_closeout_receipt
    (b : PlanOSNextCycleCloseoutReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSNextCycleCloseoutReceiptBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSNextCycleCloseoutReceiptBridge

end PlanOS
end KUOS
