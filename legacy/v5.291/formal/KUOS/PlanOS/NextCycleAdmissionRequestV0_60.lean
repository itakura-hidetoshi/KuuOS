import Mathlib
import KUOS.PlanOS.BlockerReleaseCloseoutReceiptV0_59

namespace KUOS
namespace PlanOS

structure NextCycleAdmissionRequestSurface where
  sourceCloseout : BlockerReleaseCloseoutSurface
  sourceBoundary : BlockerReleaseCloseoutBoundary
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
  nextCycleAdmissionRequestOnly : Bool
  nextCycleAdmissionRequested : Bool
  nextCycleAdmissionGranted : Bool
  nextCycleStarted : Bool
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
  requestOnlyRequired : nextCycleAdmissionRequestOnly = true
  requestRequired : nextCycleAdmissionRequested = true
  admissionForbidden : nextCycleAdmissionGranted = false
  nextCycleStartForbidden : nextCycleStarted = false

structure NextCycleAdmissionRequestBoundary where
  requestOwnedByPlanOS : Bool
  sourceBlockerReleaseCloseoutPreserved : Bool
  selectedCandidateBoundToBlockerReleaseCloseout : Bool
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
  nextCycleAdmissionRequestOnly : Bool
  nextCycleAdmissionRequested : Bool
  nextCycleAdmissionGranted : Bool
  nextCycleStarted : Bool
  ownerRequired : requestOwnedByPlanOS = true
  sourcePreservedRequired : sourceBlockerReleaseCloseoutPreserved = true
  selectedBoundRequired : selectedCandidateBoundToBlockerReleaseCloseout = true
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
  requestOnlyRequired : nextCycleAdmissionRequestOnly = true
  requestRequired : nextCycleAdmissionRequested = true
  admissionForbidden : nextCycleAdmissionGranted = false
  nextCycleStartForbidden : nextCycleStarted = false

structure PlanOSNextCycleAdmissionRequestBridge where
  Digest : Type
  digestOf : NextCycleAdmissionRequestSurface → NextCycleAdmissionRequestBoundary → Nat → Digest
  surface : NextCycleAdmissionRequestSurface
  boundary : NextCycleAdmissionRequestBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  recorderNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  recorderTruthForbidden : recorderNonAuthority.truthAuthority = false

namespace PlanOSNextCycleAdmissionRequestBridge

theorem source_closeout_closes_release_cycle_but_does_not_request_admission
    (b : PlanOSNextCycleAdmissionRequestBridge) :
    b.surface.sourceCloseout.blockerReleaseCloseoutReceiptOnly = true ∧
      b.surface.sourceCloseout.blockerReleaseCycleClosed = true ∧
      b.surface.sourceCloseout.nextCycleAdmissionRequested = false ∧
      b.surface.sourceBoundary.blockerReleaseCycleClosed = true ∧
      b.surface.sourceBoundary.nextCycleAdmissionRequested = false := by
  exact ⟨b.surface.sourceCloseout.closeoutOnlyRequired,
    b.surface.sourceCloseout.releaseCycleClosedRequired,
    b.surface.sourceCloseout.nextCycleAdmissionForbidden,
    b.surface.sourceBoundary.releaseCycleClosedRequired,
    b.surface.sourceBoundary.nextCycleAdmissionForbidden⟩

theorem request_binds_candidate_and_preserves_closed_prior_cycle
    (b : PlanOSNextCycleAdmissionRequestBridge) :
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
      b.surface.blockerReleaseCycleClosedPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.memoryOverwriteRequired, b.surface.memoryCloseoutRequired,
    b.surface.cyclePreservedRequired, b.surface.truthGrantPreservedRequired,
    b.surface.truthPreservedRequired, b.surface.truthCyclePreservedRequired,
    b.surface.blockerRequestPreservedRequired, b.surface.blockerGrantPreservedRequired,
    b.surface.blockerReleasePreservedRequired, b.surface.blockerCyclePreservedRequired⟩

theorem request_opens_admission_request_but_not_grant_or_start
    (b : PlanOSNextCycleAdmissionRequestBridge) :
    b.surface.nextCycleAdmissionRequestOnly = true ∧
      b.surface.nextCycleAdmissionRequested = true ∧
      b.surface.nextCycleAdmissionGranted = false ∧
      b.surface.nextCycleStarted = false ∧
      b.boundary.nextCycleAdmissionRequested = true ∧
      b.boundary.nextCycleAdmissionGranted = false ∧
      b.boundary.nextCycleStarted = false ∧
      b.recorderNonAuthority.truthAuthority = false := by
  exact ⟨b.surface.requestOnlyRequired, b.surface.requestRequired,
    b.surface.admissionForbidden, b.surface.nextCycleStartForbidden,
    b.boundary.requestRequired, b.boundary.admissionForbidden,
    b.boundary.nextCycleStartForbidden, b.recorderTruthForbidden⟩

theorem boundary_is_next_cycle_admission_request_only
    (b : PlanOSNextCycleAdmissionRequestBridge) :
    b.boundary.requestOwnedByPlanOS = true ∧
      b.boundary.sourceBlockerReleaseCloseoutPreserved = true ∧
      b.boundary.selectedCandidateBoundToBlockerReleaseCloseout = true ∧
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
      b.boundary.nextCycleAdmissionRequestOnly = true ∧
      b.boundary.nextCycleAdmissionRequested = true ∧
      b.boundary.nextCycleAdmissionGranted = false ∧
      b.boundary.nextCycleStarted = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.memoryOverwriteRequired,
    b.boundary.memoryCloseoutRequired, b.boundary.cyclePreservedRequired,
    b.boundary.truthGrantPreservedRequired, b.boundary.truthPreservedRequired,
    b.boundary.truthCyclePreservedRequired, b.boundary.blockerRequestPreservedRequired,
    b.boundary.blockerGrantPreservedRequired, b.boundary.blockerReleasePreservedRequired,
    b.boundary.blockerCyclePreservedRequired, b.boundary.requestOnlyRequired,
    b.boundary.requestRequired, b.boundary.admissionForbidden,
    b.boundary.nextCycleStartForbidden⟩

theorem history_appends_one_next_cycle_admission_request
    (b : PlanOSNextCycleAdmissionRequestBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSNextCycleAdmissionRequestBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSNextCycleAdmissionRequestBridge

end PlanOS
end KUOS
