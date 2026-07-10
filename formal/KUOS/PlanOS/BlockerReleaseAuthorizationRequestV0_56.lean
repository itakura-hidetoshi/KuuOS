import Mathlib
import KUOS.PlanOS.TruthAuthorityCloseoutReceiptV0_55

namespace KUOS
namespace PlanOS

structure BlockerReleaseAuthorizationRequestSurface where
  sourceCloseout : TruthAuthorityCloseoutReceiptSurface
  sourceBoundary : TruthAuthorityCloseoutReceiptBoundary
  sourceCloseoutBound : Bool
  selectedCandidateBoundToTruthAuthorityCloseout : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  truthAuthorityAuthorizationGrantPreserved : Bool
  truthAuthorityPreserved : Bool
  truthAuthorityCycleClosedPreserved : Bool
  blockerReleaseAuthorizationRequestOnly : Bool
  blockerReleaseAuthorizationRequested : Bool
  blockerReleaseAuthorizationGranted : Bool
  blockerReleaseGranted : Bool
  sourceRequired : sourceCloseoutBound = true
  selectedBoundRequired : selectedCandidateBoundToTruthAuthorityCloseout = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  memoryCloseoutRequired : memoryOverwriteCloseoutPreserved = true
  cyclePreservedRequired : cycleClosedPreserved = true
  truthGrantPreservedRequired : truthAuthorityAuthorizationGrantPreserved = true
  truthPreservedRequired : truthAuthorityPreserved = true
  truthCyclePreservedRequired : truthAuthorityCycleClosedPreserved = true
  requestOnlyRequired : blockerReleaseAuthorizationRequestOnly = true
  requestRequired : blockerReleaseAuthorizationRequested = true
  authorizationForbidden : blockerReleaseAuthorizationGranted = false
  releaseForbidden : blockerReleaseGranted = false

structure BlockerReleaseAuthorizationRequestBoundary where
  requestOwnedByPlanOS : Bool
  sourceTruthAuthorityCloseoutPreserved : Bool
  selectedCandidateBoundToTruthAuthorityCloseout : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  truthAuthorityAuthorizationGrantPreserved : Bool
  truthAuthorityPreserved : Bool
  truthAuthorityCycleClosedPreserved : Bool
  blockerReleaseAuthorizationRequestOnly : Bool
  blockerReleaseAuthorizationRequested : Bool
  blockerReleaseAuthorizationGranted : Bool
  blockerReleaseGranted : Bool
  ownerRequired : requestOwnedByPlanOS = true
  sourcePreservedRequired : sourceTruthAuthorityCloseoutPreserved = true
  selectedBoundRequired : selectedCandidateBoundToTruthAuthorityCloseout = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  memoryCloseoutRequired : memoryOverwriteCloseoutPreserved = true
  cyclePreservedRequired : cycleClosedPreserved = true
  truthGrantPreservedRequired : truthAuthorityAuthorizationGrantPreserved = true
  truthPreservedRequired : truthAuthorityPreserved = true
  truthCyclePreservedRequired : truthAuthorityCycleClosedPreserved = true
  requestOnlyRequired : blockerReleaseAuthorizationRequestOnly = true
  requestRequired : blockerReleaseAuthorizationRequested = true
  authorizationForbidden : blockerReleaseAuthorizationGranted = false
  releaseForbidden : blockerReleaseGranted = false

structure PlanOSBlockerReleaseAuthorizationRequestBridge where
  Digest : Type
  digestOf : BlockerReleaseAuthorizationRequestSurface → BlockerReleaseAuthorizationRequestBoundary → Nat → Digest
  surface : BlockerReleaseAuthorizationRequestSurface
  boundary : BlockerReleaseAuthorizationRequestBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  recorderNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  recorderTruthForbidden : recorderNonAuthority.truthAuthority = false

namespace PlanOSBlockerReleaseAuthorizationRequestBridge

theorem source_closeout_preserves_truth_and_keeps_release_closed
    (b : PlanOSBlockerReleaseAuthorizationRequestBridge) :
    b.surface.sourceCloseout.truthAuthorityPreserved = true ∧
      b.surface.sourceCloseout.truthAuthorityCloseoutReceiptOnly = true ∧
      b.surface.sourceCloseout.truthAuthorityCycleClosed = true ∧
      b.surface.sourceCloseout.blockerReleaseGranted = false ∧
      b.surface.sourceBoundary.truthAuthorityPreserved = true ∧
      b.surface.sourceBoundary.truthAuthorityCycleClosed = true ∧
      b.surface.sourceBoundary.blockerReleaseGranted = false := by
  exact ⟨b.surface.sourceCloseout.truthPreservedRequired,
    b.surface.sourceCloseout.closeoutOnlyRequired,
    b.surface.sourceCloseout.truthCycleClosedRequired,
    b.surface.sourceCloseout.blockerReleaseForbidden,
    b.surface.sourceBoundary.truthPreservedRequired,
    b.surface.sourceBoundary.truthCycleClosedRequired,
    b.surface.sourceBoundary.blockerReleaseForbidden⟩

theorem request_binds_candidate_and_preserves_closed_truth_state
    (b : PlanOSBlockerReleaseAuthorizationRequestBridge) :
    b.surface.sourceCloseoutBound = true ∧
      b.surface.selectedCandidateBoundToTruthAuthorityCloseout = true ∧
      b.surface.memoryOverwritePreserved = true ∧
      b.surface.memoryOverwriteCloseoutPreserved = true ∧
      b.surface.cycleClosedPreserved = true ∧
      b.surface.truthAuthorityAuthorizationGrantPreserved = true ∧
      b.surface.truthAuthorityPreserved = true ∧
      b.surface.truthAuthorityCycleClosedPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.memoryOverwriteRequired, b.surface.memoryCloseoutRequired,
    b.surface.cyclePreservedRequired, b.surface.truthGrantPreservedRequired,
    b.surface.truthPreservedRequired, b.surface.truthCyclePreservedRequired⟩

theorem request_asks_blocker_release_but_does_not_grant_or_apply_it
    (b : PlanOSBlockerReleaseAuthorizationRequestBridge) :
    b.surface.blockerReleaseAuthorizationRequestOnly = true ∧
      b.surface.blockerReleaseAuthorizationRequested = true ∧
      b.surface.blockerReleaseAuthorizationGranted = false ∧
      b.surface.blockerReleaseGranted = false ∧
      b.boundary.blockerReleaseAuthorizationRequested = true ∧
      b.boundary.blockerReleaseAuthorizationGranted = false ∧
      b.boundary.blockerReleaseGranted = false ∧
      b.recorderNonAuthority.truthAuthority = false := by
  exact ⟨b.surface.requestOnlyRequired, b.surface.requestRequired,
    b.surface.authorizationForbidden, b.surface.releaseForbidden,
    b.boundary.requestRequired, b.boundary.authorizationForbidden,
    b.boundary.releaseForbidden, b.recorderTruthForbidden⟩

theorem boundary_is_blocker_release_authorization_request_only
    (b : PlanOSBlockerReleaseAuthorizationRequestBridge) :
    b.boundary.requestOwnedByPlanOS = true ∧
      b.boundary.sourceTruthAuthorityCloseoutPreserved = true ∧
      b.boundary.selectedCandidateBoundToTruthAuthorityCloseout = true ∧
      b.boundary.memoryOverwritePreserved = true ∧
      b.boundary.memoryOverwriteCloseoutPreserved = true ∧
      b.boundary.cycleClosedPreserved = true ∧
      b.boundary.truthAuthorityAuthorizationGrantPreserved = true ∧
      b.boundary.truthAuthorityPreserved = true ∧
      b.boundary.truthAuthorityCycleClosedPreserved = true ∧
      b.boundary.blockerReleaseAuthorizationRequestOnly = true ∧
      b.boundary.blockerReleaseAuthorizationRequested = true ∧
      b.boundary.blockerReleaseAuthorizationGranted = false ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.memoryOverwriteRequired,
    b.boundary.memoryCloseoutRequired, b.boundary.cyclePreservedRequired,
    b.boundary.truthGrantPreservedRequired, b.boundary.truthPreservedRequired,
    b.boundary.truthCyclePreservedRequired, b.boundary.requestOnlyRequired,
    b.boundary.requestRequired, b.boundary.authorizationForbidden,
    b.boundary.releaseForbidden⟩

theorem history_appends_one_blocker_release_authorization_request
    (b : PlanOSBlockerReleaseAuthorizationRequestBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSBlockerReleaseAuthorizationRequestBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSBlockerReleaseAuthorizationRequestBridge

end PlanOS
end KUOS
