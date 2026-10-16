import Mathlib
import KUOS.PlanOS.BlockerReleaseReceiptV0_58

namespace KUOS
namespace PlanOS

structure BlockerReleaseCloseoutSurface where
  sourceReceipt : BlockerReleaseReceiptSurface
  sourceBoundary : BlockerReleaseReceiptBoundary
  sourceReceiptBound : Bool
  selectedCandidateBoundToReceipt : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  truthAuthorityAuthorizationGrantPreserved : Bool
  truthAuthorityPreserved : Bool
  truthAuthorityCycleClosedPreserved : Bool
  blockerReleaseAuthorizationRequestPreserved : Bool
  blockerReleaseAuthorizationGrantPreserved : Bool
  blockerReleasePreserved : Bool
  blockerReleaseCloseoutReceiptOnly : Bool
  blockerReleaseCycleClosed : Bool
  nextCycleAdmissionRequested : Bool
  sourceRequired : sourceReceiptBound = true
  selectedBoundRequired : selectedCandidateBoundToReceipt = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  memoryCloseoutRequired : memoryOverwriteCloseoutPreserved = true
  cyclePreservedRequired : cycleClosedPreserved = true
  truthGrantPreservedRequired : truthAuthorityAuthorizationGrantPreserved = true
  truthPreservedRequired : truthAuthorityPreserved = true
  truthCyclePreservedRequired : truthAuthorityCycleClosedPreserved = true
  requestPreservedRequired : blockerReleaseAuthorizationRequestPreserved = true
  grantPreservedRequired : blockerReleaseAuthorizationGrantPreserved = true
  releasePreservedRequired : blockerReleasePreserved = true
  closeoutOnlyRequired : blockerReleaseCloseoutReceiptOnly = true
  releaseCycleClosedRequired : blockerReleaseCycleClosed = true
  nextCycleAdmissionForbidden : nextCycleAdmissionRequested = false

structure BlockerReleaseCloseoutBoundary where
  closeoutOwnedByPlanOS : Bool
  sourceBlockerReleaseReceiptPreserved : Bool
  selectedCandidateBoundToBlockerReleaseReceipt : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  truthAuthorityAuthorizationGrantPreserved : Bool
  truthAuthorityPreserved : Bool
  truthAuthorityCycleClosedPreserved : Bool
  blockerReleaseAuthorizationRequestPreserved : Bool
  blockerReleaseAuthorizationGrantPreserved : Bool
  blockerReleasePreserved : Bool
  blockerReleaseCloseoutReceiptOnly : Bool
  blockerReleaseCycleClosed : Bool
  nextCycleAdmissionRequested : Bool
  ownerRequired : closeoutOwnedByPlanOS = true
  sourcePreservedRequired : sourceBlockerReleaseReceiptPreserved = true
  selectedBoundRequired : selectedCandidateBoundToBlockerReleaseReceipt = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  memoryCloseoutRequired : memoryOverwriteCloseoutPreserved = true
  cyclePreservedRequired : cycleClosedPreserved = true
  truthGrantPreservedRequired : truthAuthorityAuthorizationGrantPreserved = true
  truthPreservedRequired : truthAuthorityPreserved = true
  truthCyclePreservedRequired : truthAuthorityCycleClosedPreserved = true
  requestPreservedRequired : blockerReleaseAuthorizationRequestPreserved = true
  grantPreservedRequired : blockerReleaseAuthorizationGrantPreserved = true
  releasePreservedRequired : blockerReleasePreserved = true
  closeoutOnlyRequired : blockerReleaseCloseoutReceiptOnly = true
  releaseCycleClosedRequired : blockerReleaseCycleClosed = true
  nextCycleAdmissionForbidden : nextCycleAdmissionRequested = false

structure PlanOSBlockerReleaseCloseoutBridge where
  Digest : Type
  digestOf : BlockerReleaseCloseoutSurface → BlockerReleaseCloseoutBoundary → Nat → Digest
  surface : BlockerReleaseCloseoutSurface
  boundary : BlockerReleaseCloseoutBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  recorderNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  recorderTruthForbidden : recorderNonAuthority.truthAuthority = false

namespace PlanOSBlockerReleaseCloseoutBridge

theorem source_receipt_records_release_but_keeps_cycle_open
    (b : PlanOSBlockerReleaseCloseoutBridge) :
    b.surface.sourceReceipt.blockerReleaseReceiptOnly = true ∧
      b.surface.sourceReceipt.blockerReleaseAuthorizationRequested = true ∧
      b.surface.sourceReceipt.blockerReleaseAuthorizationGranted = true ∧
      b.surface.sourceReceipt.blockerReleaseGranted = true ∧
      b.surface.sourceReceipt.blockerReleaseCycleClosed = false ∧
      b.surface.sourceBoundary.blockerReleaseGranted = true ∧
      b.surface.sourceBoundary.blockerReleaseCycleClosed = false := by
  exact ⟨b.surface.sourceReceipt.receiptOnlyRequired,
    b.surface.sourceReceipt.requestRequired,
    b.surface.sourceReceipt.authorizationRequired,
    b.surface.sourceReceipt.releaseRequired,
    b.surface.sourceReceipt.cycleOpenRequired,
    b.surface.sourceBoundary.releaseRequired,
    b.surface.sourceBoundary.cycleOpenRequired⟩

theorem closeout_binds_candidate_and_preserves_release_state
    (b : PlanOSBlockerReleaseCloseoutBridge) :
    b.surface.sourceReceiptBound = true ∧
      b.surface.selectedCandidateBoundToReceipt = true ∧
      b.surface.memoryOverwritePreserved = true ∧
      b.surface.memoryOverwriteCloseoutPreserved = true ∧
      b.surface.cycleClosedPreserved = true ∧
      b.surface.truthAuthorityAuthorizationGrantPreserved = true ∧
      b.surface.truthAuthorityPreserved = true ∧
      b.surface.truthAuthorityCycleClosedPreserved = true ∧
      b.surface.blockerReleaseAuthorizationRequestPreserved = true ∧
      b.surface.blockerReleaseAuthorizationGrantPreserved = true ∧
      b.surface.blockerReleasePreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.memoryOverwriteRequired, b.surface.memoryCloseoutRequired,
    b.surface.cyclePreservedRequired, b.surface.truthGrantPreservedRequired,
    b.surface.truthPreservedRequired, b.surface.truthCyclePreservedRequired,
    b.surface.requestPreservedRequired, b.surface.grantPreservedRequired,
    b.surface.releasePreservedRequired⟩

theorem closeout_closes_release_cycle_without_opening_next_admission
    (b : PlanOSBlockerReleaseCloseoutBridge) :
    b.surface.blockerReleaseCloseoutReceiptOnly = true ∧
      b.surface.blockerReleaseCycleClosed = true ∧
      b.surface.nextCycleAdmissionRequested = false ∧
      b.boundary.blockerReleaseCycleClosed = true ∧
      b.boundary.nextCycleAdmissionRequested = false ∧
      b.recorderNonAuthority.truthAuthority = false := by
  exact ⟨b.surface.closeoutOnlyRequired,
    b.surface.releaseCycleClosedRequired,
    b.surface.nextCycleAdmissionForbidden,
    b.boundary.releaseCycleClosedRequired,
    b.boundary.nextCycleAdmissionForbidden,
    b.recorderTruthForbidden⟩

theorem boundary_preserves_blocker_release_closeout_only
    (b : PlanOSBlockerReleaseCloseoutBridge) :
    b.boundary.closeoutOwnedByPlanOS = true ∧
      b.boundary.sourceBlockerReleaseReceiptPreserved = true ∧
      b.boundary.selectedCandidateBoundToBlockerReleaseReceipt = true ∧
      b.boundary.memoryOverwritePreserved = true ∧
      b.boundary.memoryOverwriteCloseoutPreserved = true ∧
      b.boundary.cycleClosedPreserved = true ∧
      b.boundary.truthAuthorityAuthorizationGrantPreserved = true ∧
      b.boundary.truthAuthorityPreserved = true ∧
      b.boundary.truthAuthorityCycleClosedPreserved = true ∧
      b.boundary.blockerReleaseAuthorizationRequestPreserved = true ∧
      b.boundary.blockerReleaseAuthorizationGrantPreserved = true ∧
      b.boundary.blockerReleasePreserved = true ∧
      b.boundary.blockerReleaseCloseoutReceiptOnly = true ∧
      b.boundary.blockerReleaseCycleClosed = true ∧
      b.boundary.nextCycleAdmissionRequested = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.memoryOverwriteRequired,
    b.boundary.memoryCloseoutRequired, b.boundary.cyclePreservedRequired,
    b.boundary.truthGrantPreservedRequired, b.boundary.truthPreservedRequired,
    b.boundary.truthCyclePreservedRequired, b.boundary.requestPreservedRequired,
    b.boundary.grantPreservedRequired, b.boundary.releasePreservedRequired,
    b.boundary.closeoutOnlyRequired, b.boundary.releaseCycleClosedRequired,
    b.boundary.nextCycleAdmissionForbidden⟩

theorem history_appends_one_blocker_release_closeout_record
    (b : PlanOSBlockerReleaseCloseoutBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSBlockerReleaseCloseoutBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSBlockerReleaseCloseoutBridge

end PlanOS
end KUOS
