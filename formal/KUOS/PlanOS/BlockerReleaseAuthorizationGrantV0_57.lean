import Mathlib
import KUOS.PlanOS.BlockerReleaseAuthorizationRequestV0_56

namespace KUOS
namespace PlanOS

structure BlockerReleaseAuthorizationGrantSurface where
  sourceRequest : BlockerReleaseAuthorizationRequestSurface
  sourceBoundary : BlockerReleaseAuthorizationRequestBoundary
  sourceRequestBound : Bool
  selectedCandidateBoundToRequest : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  truthAuthorityAuthorizationGrantPreserved : Bool
  truthAuthorityPreserved : Bool
  truthAuthorityCycleClosedPreserved : Bool
  blockerReleaseAuthorizationRequestPreserved : Bool
  blockerReleaseAuthorizationGrantOnly : Bool
  blockerReleaseAuthorizationRequested : Bool
  blockerReleaseAuthorizationGranted : Bool
  blockerReleaseGranted : Bool
  sourceRequired : sourceRequestBound = true
  selectedBoundRequired : selectedCandidateBoundToRequest = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  memoryCloseoutRequired : memoryOverwriteCloseoutPreserved = true
  cyclePreservedRequired : cycleClosedPreserved = true
  truthGrantPreservedRequired : truthAuthorityAuthorizationGrantPreserved = true
  truthPreservedRequired : truthAuthorityPreserved = true
  truthCyclePreservedRequired : truthAuthorityCycleClosedPreserved = true
  requestPreservedRequired : blockerReleaseAuthorizationRequestPreserved = true
  grantOnlyRequired : blockerReleaseAuthorizationGrantOnly = true
  requestRequired : blockerReleaseAuthorizationRequested = true
  authorizationRequired : blockerReleaseAuthorizationGranted = true
  releaseForbidden : blockerReleaseGranted = false

structure BlockerReleaseAuthorizationGrantBoundary where
  grantOwnedByPlanOS : Bool
  sourceBlockerReleaseAuthorizationRequestPreserved : Bool
  selectedCandidateBoundToBlockerReleaseRequest : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  truthAuthorityAuthorizationGrantPreserved : Bool
  truthAuthorityPreserved : Bool
  truthAuthorityCycleClosedPreserved : Bool
  blockerReleaseAuthorizationRequestPreserved : Bool
  blockerReleaseAuthorizationGrantOnly : Bool
  blockerReleaseAuthorizationRequested : Bool
  blockerReleaseAuthorizationGranted : Bool
  blockerReleaseGranted : Bool
  ownerRequired : grantOwnedByPlanOS = true
  sourcePreservedRequired : sourceBlockerReleaseAuthorizationRequestPreserved = true
  selectedBoundRequired : selectedCandidateBoundToBlockerReleaseRequest = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  memoryCloseoutRequired : memoryOverwriteCloseoutPreserved = true
  cyclePreservedRequired : cycleClosedPreserved = true
  truthGrantPreservedRequired : truthAuthorityAuthorizationGrantPreserved = true
  truthPreservedRequired : truthAuthorityPreserved = true
  truthCyclePreservedRequired : truthAuthorityCycleClosedPreserved = true
  requestPreservedRequired : blockerReleaseAuthorizationRequestPreserved = true
  grantOnlyRequired : blockerReleaseAuthorizationGrantOnly = true
  requestRequired : blockerReleaseAuthorizationRequested = true
  authorizationRequired : blockerReleaseAuthorizationGranted = true
  releaseForbidden : blockerReleaseGranted = false

structure PlanOSBlockerReleaseAuthorizationGrantBridge where
  Digest : Type
  digestOf : BlockerReleaseAuthorizationGrantSurface → BlockerReleaseAuthorizationGrantBoundary → Nat → Digest
  surface : BlockerReleaseAuthorizationGrantSurface
  boundary : BlockerReleaseAuthorizationGrantBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  recorderNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  recorderTruthForbidden : recorderNonAuthority.truthAuthority = false

namespace PlanOSBlockerReleaseAuthorizationGrantBridge

theorem source_request_asks_but_does_not_grant_or_apply_release
    (b : PlanOSBlockerReleaseAuthorizationGrantBridge) :
    b.surface.sourceRequest.blockerReleaseAuthorizationRequestOnly = true ∧
      b.surface.sourceRequest.blockerReleaseAuthorizationRequested = true ∧
      b.surface.sourceRequest.blockerReleaseAuthorizationGranted = false ∧
      b.surface.sourceRequest.blockerReleaseGranted = false ∧
      b.surface.sourceBoundary.blockerReleaseAuthorizationRequested = true ∧
      b.surface.sourceBoundary.blockerReleaseAuthorizationGranted = false ∧
      b.surface.sourceBoundary.blockerReleaseGranted = false := by
  exact ⟨b.surface.sourceRequest.requestOnlyRequired,
    b.surface.sourceRequest.requestRequired,
    b.surface.sourceRequest.authorizationForbidden,
    b.surface.sourceRequest.releaseForbidden,
    b.surface.sourceBoundary.requestRequired,
    b.surface.sourceBoundary.authorizationForbidden,
    b.surface.sourceBoundary.releaseForbidden⟩

theorem grant_binds_candidate_and_preserves_closed_truth_state
    (b : PlanOSBlockerReleaseAuthorizationGrantBridge) :
    b.surface.sourceRequestBound = true ∧
      b.surface.selectedCandidateBoundToRequest = true ∧
      b.surface.memoryOverwritePreserved = true ∧
      b.surface.memoryOverwriteCloseoutPreserved = true ∧
      b.surface.cycleClosedPreserved = true ∧
      b.surface.truthAuthorityAuthorizationGrantPreserved = true ∧
      b.surface.truthAuthorityPreserved = true ∧
      b.surface.truthAuthorityCycleClosedPreserved = true ∧
      b.surface.blockerReleaseAuthorizationRequestPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.memoryOverwriteRequired, b.surface.memoryCloseoutRequired,
    b.surface.cyclePreservedRequired, b.surface.truthGrantPreservedRequired,
    b.surface.truthPreservedRequired, b.surface.truthCyclePreservedRequired,
    b.surface.requestPreservedRequired⟩

theorem grant_authorizes_but_does_not_release_blockers
    (b : PlanOSBlockerReleaseAuthorizationGrantBridge) :
    b.surface.blockerReleaseAuthorizationGrantOnly = true ∧
      b.surface.blockerReleaseAuthorizationRequested = true ∧
      b.surface.blockerReleaseAuthorizationGranted = true ∧
      b.surface.blockerReleaseGranted = false ∧
      b.boundary.blockerReleaseAuthorizationGranted = true ∧
      b.boundary.blockerReleaseGranted = false ∧
      b.recorderNonAuthority.truthAuthority = false := by
  exact ⟨b.surface.grantOnlyRequired, b.surface.requestRequired,
    b.surface.authorizationRequired, b.surface.releaseForbidden,
    b.boundary.authorizationRequired, b.boundary.releaseForbidden,
    b.recorderTruthForbidden⟩

theorem boundary_is_blocker_release_authorization_grant_only
    (b : PlanOSBlockerReleaseAuthorizationGrantBridge) :
    b.boundary.grantOwnedByPlanOS = true ∧
      b.boundary.sourceBlockerReleaseAuthorizationRequestPreserved = true ∧
      b.boundary.selectedCandidateBoundToBlockerReleaseRequest = true ∧
      b.boundary.memoryOverwritePreserved = true ∧
      b.boundary.memoryOverwriteCloseoutPreserved = true ∧
      b.boundary.cycleClosedPreserved = true ∧
      b.boundary.truthAuthorityAuthorizationGrantPreserved = true ∧
      b.boundary.truthAuthorityPreserved = true ∧
      b.boundary.truthAuthorityCycleClosedPreserved = true ∧
      b.boundary.blockerReleaseAuthorizationRequestPreserved = true ∧
      b.boundary.blockerReleaseAuthorizationGrantOnly = true ∧
      b.boundary.blockerReleaseAuthorizationRequested = true ∧
      b.boundary.blockerReleaseAuthorizationGranted = true ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.memoryOverwriteRequired,
    b.boundary.memoryCloseoutRequired, b.boundary.cyclePreservedRequired,
    b.boundary.truthGrantPreservedRequired, b.boundary.truthPreservedRequired,
    b.boundary.truthCyclePreservedRequired, b.boundary.requestPreservedRequired,
    b.boundary.grantOnlyRequired, b.boundary.requestRequired,
    b.boundary.authorizationRequired, b.boundary.releaseForbidden⟩

theorem history_appends_one_blocker_release_authorization_grant
    (b : PlanOSBlockerReleaseAuthorizationGrantBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSBlockerReleaseAuthorizationGrantBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSBlockerReleaseAuthorizationGrantBridge

end PlanOS
end KUOS
