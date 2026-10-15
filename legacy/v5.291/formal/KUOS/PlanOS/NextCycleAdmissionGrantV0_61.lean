import Mathlib
import KUOS.PlanOS.NextCycleAdmissionRequestV0_60

namespace KUOS
namespace PlanOS

structure NextCycleAdmissionGrantSurface where
  sourceRequest : NextCycleAdmissionRequestSurface
  sourceBoundary : NextCycleAdmissionRequestBoundary
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
  nextCycleAdmissionGrantOnly : Bool
  nextCycleAdmissionRequested : Bool
  nextCycleAdmissionGranted : Bool
  nextCycleStarted : Bool
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
  grantOnlyRequired : nextCycleAdmissionGrantOnly = true
  requestRequired : nextCycleAdmissionRequested = true
  admissionRequired : nextCycleAdmissionGranted = true
  nextCycleStartForbidden : nextCycleStarted = false

structure NextCycleAdmissionGrantBoundary where
  grantOwnedByPlanOS : Bool
  sourceNextCycleAdmissionRequestPreserved : Bool
  selectedCandidateBoundToNextCycleAdmissionRequest : Bool
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
  nextCycleAdmissionGrantOnly : Bool
  nextCycleAdmissionRequested : Bool
  nextCycleAdmissionGranted : Bool
  nextCycleStarted : Bool
  ownerRequired : grantOwnedByPlanOS = true
  sourcePreservedRequired : sourceNextCycleAdmissionRequestPreserved = true
  selectedBoundRequired : selectedCandidateBoundToNextCycleAdmissionRequest = true
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
  grantOnlyRequired : nextCycleAdmissionGrantOnly = true
  requestRequired : nextCycleAdmissionRequested = true
  admissionRequired : nextCycleAdmissionGranted = true
  nextCycleStartForbidden : nextCycleStarted = false

structure PlanOSNextCycleAdmissionGrantBridge where
  Digest : Type
  digestOf : NextCycleAdmissionGrantSurface → NextCycleAdmissionGrantBoundary → Nat → Digest
  surface : NextCycleAdmissionGrantSurface
  boundary : NextCycleAdmissionGrantBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  recorderNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  recorderTruthForbidden : recorderNonAuthority.truthAuthority = false

namespace PlanOSNextCycleAdmissionGrantBridge

theorem source_request_requests_admission_but_does_not_grant_or_start
    (b : PlanOSNextCycleAdmissionGrantBridge) :
    b.surface.sourceRequest.nextCycleAdmissionRequestOnly = true ∧
      b.surface.sourceRequest.nextCycleAdmissionRequested = true ∧
      b.surface.sourceRequest.nextCycleAdmissionGranted = false ∧
      b.surface.sourceRequest.nextCycleStarted = false ∧
      b.surface.sourceBoundary.nextCycleAdmissionRequested = true ∧
      b.surface.sourceBoundary.nextCycleAdmissionGranted = false ∧
      b.surface.sourceBoundary.nextCycleStarted = false := by
  exact ⟨b.surface.sourceRequest.requestOnlyRequired,
    b.surface.sourceRequest.requestRequired,
    b.surface.sourceRequest.admissionForbidden,
    b.surface.sourceRequest.nextCycleStartForbidden,
    b.surface.sourceBoundary.requestRequired,
    b.surface.sourceBoundary.admissionForbidden,
    b.surface.sourceBoundary.nextCycleStartForbidden⟩

theorem grant_binds_candidate_and_preserves_closed_prior_cycle
    (b : PlanOSNextCycleAdmissionGrantBridge) :
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
      b.surface.nextCycleAdmissionRequestPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.memoryOverwriteRequired, b.surface.memoryCloseoutRequired,
    b.surface.cyclePreservedRequired, b.surface.truthGrantPreservedRequired,
    b.surface.truthPreservedRequired, b.surface.truthCyclePreservedRequired,
    b.surface.blockerRequestPreservedRequired, b.surface.blockerGrantPreservedRequired,
    b.surface.blockerReleasePreservedRequired, b.surface.blockerCyclePreservedRequired,
    b.surface.admissionRequestPreservedRequired⟩

theorem grant_authorizes_admission_without_starting_next_cycle
    (b : PlanOSNextCycleAdmissionGrantBridge) :
    b.surface.nextCycleAdmissionGrantOnly = true ∧
      b.surface.nextCycleAdmissionRequested = true ∧
      b.surface.nextCycleAdmissionGranted = true ∧
      b.surface.nextCycleStarted = false ∧
      b.boundary.nextCycleAdmissionRequested = true ∧
      b.boundary.nextCycleAdmissionGranted = true ∧
      b.boundary.nextCycleStarted = false ∧
      b.recorderNonAuthority.truthAuthority = false := by
  exact ⟨b.surface.grantOnlyRequired, b.surface.requestRequired,
    b.surface.admissionRequired, b.surface.nextCycleStartForbidden,
    b.boundary.requestRequired, b.boundary.admissionRequired,
    b.boundary.nextCycleStartForbidden, b.recorderTruthForbidden⟩

theorem boundary_is_next_cycle_admission_grant_only
    (b : PlanOSNextCycleAdmissionGrantBridge) :
    b.boundary.grantOwnedByPlanOS = true ∧
      b.boundary.sourceNextCycleAdmissionRequestPreserved = true ∧
      b.boundary.selectedCandidateBoundToNextCycleAdmissionRequest = true ∧
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
      b.boundary.nextCycleAdmissionGrantOnly = true ∧
      b.boundary.nextCycleAdmissionRequested = true ∧
      b.boundary.nextCycleAdmissionGranted = true ∧
      b.boundary.nextCycleStarted = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.memoryOverwriteRequired,
    b.boundary.memoryCloseoutRequired, b.boundary.cyclePreservedRequired,
    b.boundary.truthGrantPreservedRequired, b.boundary.truthPreservedRequired,
    b.boundary.truthCyclePreservedRequired, b.boundary.blockerRequestPreservedRequired,
    b.boundary.blockerGrantPreservedRequired, b.boundary.blockerReleasePreservedRequired,
    b.boundary.blockerCyclePreservedRequired, b.boundary.admissionRequestPreservedRequired,
    b.boundary.grantOnlyRequired, b.boundary.requestRequired,
    b.boundary.admissionRequired, b.boundary.nextCycleStartForbidden⟩

theorem history_appends_one_next_cycle_admission_grant
    (b : PlanOSNextCycleAdmissionGrantBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSNextCycleAdmissionGrantBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSNextCycleAdmissionGrantBridge

end PlanOS
end KUOS
