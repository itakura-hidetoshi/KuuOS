import Mathlib
import KUOS.PlanOS.NextCycleAdmissionGrantV0_61

namespace KUOS
namespace PlanOS

structure NextCycleStartReceiptSurface where
  sourceGrant : NextCycleAdmissionGrantSurface
  sourceBoundary : NextCycleAdmissionGrantBoundary
  sourceGrantBound : Bool
  selectedCandidateBoundToGrant : Bool
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
  nextCycleStartReceiptOnly : Bool
  nextCycleAdmissionRequested : Bool
  nextCycleAdmissionGranted : Bool
  nextCycleStarted : Bool
  nextCycleCycleClosed : Bool
  sourceRequired : sourceGrantBound = true
  selectedBoundRequired : selectedCandidateBoundToGrant = true
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
  receiptOnlyRequired : nextCycleStartReceiptOnly = true
  requestRequired : nextCycleAdmissionRequested = true
  admissionRequired : nextCycleAdmissionGranted = true
  nextCycleStartRequired : nextCycleStarted = true
  nextCycleCloseoutForbidden : nextCycleCycleClosed = false

structure NextCycleStartReceiptBoundary where
  receiptOwnedByPlanOS : Bool
  sourceNextCycleAdmissionGrantPreserved : Bool
  selectedCandidateBoundToNextCycleAdmissionGrant : Bool
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
  nextCycleStartReceiptOnly : Bool
  nextCycleAdmissionRequested : Bool
  nextCycleAdmissionGranted : Bool
  nextCycleStarted : Bool
  nextCycleCycleClosed : Bool
  ownerRequired : receiptOwnedByPlanOS = true
  sourcePreservedRequired : sourceNextCycleAdmissionGrantPreserved = true
  selectedBoundRequired : selectedCandidateBoundToNextCycleAdmissionGrant = true
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
  receiptOnlyRequired : nextCycleStartReceiptOnly = true
  requestRequired : nextCycleAdmissionRequested = true
  admissionRequired : nextCycleAdmissionGranted = true
  nextCycleStartRequired : nextCycleStarted = true
  nextCycleCloseoutForbidden : nextCycleCycleClosed = false

structure PlanOSNextCycleStartReceiptBridge where
  Digest : Type
  digestOf : NextCycleStartReceiptSurface → NextCycleStartReceiptBoundary → Nat → Digest
  surface : NextCycleStartReceiptSurface
  boundary : NextCycleStartReceiptBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  recorderNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  recorderTruthForbidden : recorderNonAuthority.truthAuthority = false

namespace PlanOSNextCycleStartReceiptBridge

theorem source_grant_authorizes_admission_but_does_not_start_cycle
    (b : PlanOSNextCycleStartReceiptBridge) :
    b.surface.sourceGrant.nextCycleAdmissionGrantOnly = true ∧
      b.surface.sourceGrant.nextCycleAdmissionRequested = true ∧
      b.surface.sourceGrant.nextCycleAdmissionGranted = true ∧
      b.surface.sourceGrant.nextCycleStarted = false ∧
      b.surface.sourceBoundary.nextCycleAdmissionGranted = true ∧
      b.surface.sourceBoundary.nextCycleStarted = false := by
  exact ⟨b.surface.sourceGrant.grantOnlyRequired,
    b.surface.sourceGrant.requestRequired,
    b.surface.sourceGrant.admissionRequired,
    b.surface.sourceGrant.nextCycleStartForbidden,
    b.surface.sourceBoundary.admissionRequired,
    b.surface.sourceBoundary.nextCycleStartForbidden⟩

theorem start_receipt_binds_candidate_and_preserves_prior_closeouts
    (b : PlanOSNextCycleStartReceiptBridge) :
    b.surface.sourceGrantBound = true ∧
      b.surface.selectedCandidateBoundToGrant = true ∧
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
      b.surface.nextCycleAdmissionGrantPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.memoryOverwriteRequired, b.surface.memoryCloseoutRequired,
    b.surface.cyclePreservedRequired, b.surface.truthGrantPreservedRequired,
    b.surface.truthPreservedRequired, b.surface.truthCyclePreservedRequired,
    b.surface.blockerRequestPreservedRequired, b.surface.blockerGrantPreservedRequired,
    b.surface.blockerReleasePreservedRequired, b.surface.blockerCyclePreservedRequired,
    b.surface.admissionRequestPreservedRequired, b.surface.admissionGrantPreservedRequired⟩

theorem receipt_starts_next_cycle_without_closing_it
    (b : PlanOSNextCycleStartReceiptBridge) :
    b.surface.nextCycleStartReceiptOnly = true ∧
      b.surface.nextCycleAdmissionRequested = true ∧
      b.surface.nextCycleAdmissionGranted = true ∧
      b.surface.nextCycleStarted = true ∧
      b.surface.nextCycleCycleClosed = false ∧
      b.boundary.nextCycleStarted = true ∧
      b.boundary.nextCycleCycleClosed = false ∧
      b.recorderNonAuthority.truthAuthority = false := by
  exact ⟨b.surface.receiptOnlyRequired, b.surface.requestRequired,
    b.surface.admissionRequired, b.surface.nextCycleStartRequired,
    b.surface.nextCycleCloseoutForbidden, b.boundary.nextCycleStartRequired,
    b.boundary.nextCycleCloseoutForbidden, b.recorderTruthForbidden⟩

theorem boundary_is_next_cycle_start_receipt_only
    (b : PlanOSNextCycleStartReceiptBridge) :
    b.boundary.receiptOwnedByPlanOS = true ∧
      b.boundary.sourceNextCycleAdmissionGrantPreserved = true ∧
      b.boundary.selectedCandidateBoundToNextCycleAdmissionGrant = true ∧
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
      b.boundary.nextCycleStartReceiptOnly = true ∧
      b.boundary.nextCycleAdmissionRequested = true ∧
      b.boundary.nextCycleAdmissionGranted = true ∧
      b.boundary.nextCycleStarted = true ∧
      b.boundary.nextCycleCycleClosed = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.memoryOverwriteRequired,
    b.boundary.memoryCloseoutRequired, b.boundary.cyclePreservedRequired,
    b.boundary.truthGrantPreservedRequired, b.boundary.truthPreservedRequired,
    b.boundary.truthCyclePreservedRequired, b.boundary.blockerRequestPreservedRequired,
    b.boundary.blockerGrantPreservedRequired, b.boundary.blockerReleasePreservedRequired,
    b.boundary.blockerCyclePreservedRequired, b.boundary.admissionRequestPreservedRequired,
    b.boundary.admissionGrantPreservedRequired, b.boundary.receiptOnlyRequired,
    b.boundary.requestRequired, b.boundary.admissionRequired,
    b.boundary.nextCycleStartRequired, b.boundary.nextCycleCloseoutForbidden⟩

theorem history_appends_one_next_cycle_start_receipt
    (b : PlanOSNextCycleStartReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSNextCycleStartReceiptBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSNextCycleStartReceiptBridge

end PlanOS
end KUOS
