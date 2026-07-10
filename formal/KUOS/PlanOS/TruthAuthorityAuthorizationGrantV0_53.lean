import Mathlib
import KUOS.PlanOS.TruthAuthorityAuthorizationRequestV0_52

namespace KUOS
namespace PlanOS

structure TruthAuthorityAuthorizationGrantSurface where
  sourceRequest : TruthAuthorityAuthorizationRequestSurface
  sourceBoundary : TruthAuthorityAuthorizationRequestBoundary
  sourceRequestBound : Bool
  selectedCandidateBoundToRequest : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  truthAuthorityAuthorizationGrantOnly : Bool
  truthAuthorityAuthorizationRequested : Bool
  truthAuthorityAuthorizationGranted : Bool
  truthAuthorityGranted : Bool
  blockerReleaseGranted : Bool
  sourceRequired : sourceRequestBound = true
  selectedBoundRequired : selectedCandidateBoundToRequest = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  closeoutPreservedRequired : memoryOverwriteCloseoutPreserved = true
  cycleClosedRequired : cycleClosedPreserved = true
  grantOnlyRequired : truthAuthorityAuthorizationGrantOnly = true
  requestRequired : truthAuthorityAuthorizationRequested = true
  authorizationRequired : truthAuthorityAuthorizationGranted = true
  truthForbidden : truthAuthorityGranted = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure TruthAuthorityAuthorizationGrantBoundary where
  grantOwnedByPlanOS : Bool
  sourceTruthAuthorityAuthorizationRequestPreserved : Bool
  selectedCandidateBoundToTruthAuthorityRequest : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  truthAuthorityAuthorizationGrantOnly : Bool
  truthAuthorityAuthorizationRequested : Bool
  truthAuthorityAuthorizationGranted : Bool
  truthAuthorityGranted : Bool
  blockerReleaseGranted : Bool
  grantOwnerRequired : grantOwnedByPlanOS = true
  sourcePreservedRequired : sourceTruthAuthorityAuthorizationRequestPreserved = true
  selectedBoundRequired : selectedCandidateBoundToTruthAuthorityRequest = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  closeoutPreservedRequired : memoryOverwriteCloseoutPreserved = true
  cycleClosedRequired : cycleClosedPreserved = true
  grantOnlyRequired : truthAuthorityAuthorizationGrantOnly = true
  requestRequired : truthAuthorityAuthorizationRequested = true
  authorizationRequired : truthAuthorityAuthorizationGranted = true
  truthForbidden : truthAuthorityGranted = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSTruthAuthorityAuthorizationGrantBridge where
  Digest : Type
  digestOf : TruthAuthorityAuthorizationGrantSurface → TruthAuthorityAuthorizationGrantBoundary → Nat → Digest
  surface : TruthAuthorityAuthorizationGrantSurface
  boundary : TruthAuthorityAuthorizationGrantBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  nonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  truthForbidden : nonAuthority.truthAuthority = false

namespace PlanOSTruthAuthorityAuthorizationGrantBridge

theorem source_request_asks_but_does_not_grant_truth_authority
    (b : PlanOSTruthAuthorityAuthorizationGrantBridge) :
    b.surface.sourceRequest.truthAuthorityAuthorizationRequestOnly = true ∧
      b.surface.sourceRequest.truthAuthorityAuthorizationRequested = true ∧
      b.surface.sourceRequest.truthAuthorityAuthorizationGranted = false ∧
      b.surface.sourceRequest.truthAuthorityGranted = false ∧
      b.surface.sourceRequest.blockerReleaseGranted = false ∧
      b.surface.sourceBoundary.truthAuthorityAuthorizationRequested = true ∧
      b.surface.sourceBoundary.truthAuthorityAuthorizationGranted = false ∧
      b.surface.sourceBoundary.truthAuthorityGranted = false ∧
      b.surface.sourceBoundary.blockerReleaseGranted = false := by
  exact ⟨b.surface.sourceRequest.requestOnlyRequired,
    b.surface.sourceRequest.requestRequired,
    b.surface.sourceRequest.authorizationForbidden,
    b.surface.sourceRequest.truthForbidden,
    b.surface.sourceRequest.blockerReleaseForbidden,
    b.surface.sourceBoundary.requestRequired,
    b.surface.sourceBoundary.authorizationForbidden,
    b.surface.sourceBoundary.truthForbidden,
    b.surface.sourceBoundary.blockerReleaseForbidden⟩

theorem grant_binds_candidate_and_preserves_memory_closeout_state
    (b : PlanOSTruthAuthorityAuthorizationGrantBridge) :
    b.surface.sourceRequestBound = true ∧
      b.surface.selectedCandidateBoundToRequest = true ∧
      b.surface.memoryOverwritePreserved = true ∧
      b.surface.memoryOverwriteCloseoutPreserved = true ∧
      b.surface.cycleClosedPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.memoryOverwriteRequired, b.surface.closeoutPreservedRequired,
    b.surface.cycleClosedRequired⟩

theorem grant_authorizes_but_does_not_apply_truth_or_release_blockers
    (b : PlanOSTruthAuthorityAuthorizationGrantBridge) :
    b.surface.truthAuthorityAuthorizationGrantOnly = true ∧
      b.surface.truthAuthorityAuthorizationRequested = true ∧
      b.surface.truthAuthorityAuthorizationGranted = true ∧
      b.surface.truthAuthorityGranted = false ∧
      b.surface.blockerReleaseGranted = false ∧
      b.boundary.truthAuthorityAuthorizationGranted = true ∧
      b.boundary.truthAuthorityGranted = false ∧
      b.boundary.blockerReleaseGranted = false ∧
      b.nonAuthority.truthAuthority = false := by
  exact ⟨b.surface.grantOnlyRequired, b.surface.requestRequired,
    b.surface.authorizationRequired, b.surface.truthForbidden,
    b.surface.blockerReleaseForbidden, b.boundary.authorizationRequired,
    b.boundary.truthForbidden, b.boundary.blockerReleaseForbidden,
    b.truthForbidden⟩

theorem boundary_preserves_truth_authority_authorization_grant_only
    (b : PlanOSTruthAuthorityAuthorizationGrantBridge) :
    b.boundary.grantOwnedByPlanOS = true ∧
      b.boundary.sourceTruthAuthorityAuthorizationRequestPreserved = true ∧
      b.boundary.selectedCandidateBoundToTruthAuthorityRequest = true ∧
      b.boundary.memoryOverwritePreserved = true ∧
      b.boundary.memoryOverwriteCloseoutPreserved = true ∧
      b.boundary.cycleClosedPreserved = true ∧
      b.boundary.truthAuthorityAuthorizationGrantOnly = true ∧
      b.boundary.truthAuthorityAuthorizationRequested = true ∧
      b.boundary.truthAuthorityAuthorizationGranted = true ∧
      b.boundary.truthAuthorityGranted = false := by
  exact ⟨b.boundary.grantOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.memoryOverwriteRequired,
    b.boundary.closeoutPreservedRequired, b.boundary.cycleClosedRequired,
    b.boundary.grantOnlyRequired, b.boundary.requestRequired,
    b.boundary.authorizationRequired, b.boundary.truthForbidden⟩

theorem history_appends_one_truth_authority_authorization_grant_record
    (b : PlanOSTruthAuthorityAuthorizationGrantBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSTruthAuthorityAuthorizationGrantBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSTruthAuthorityAuthorizationGrantBridge

end PlanOS
end KUOS
