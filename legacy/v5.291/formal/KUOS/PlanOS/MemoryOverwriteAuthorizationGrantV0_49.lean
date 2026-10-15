import Mathlib
import KUOS.PlanOS.MemoryOverwriteAuthorizationRequestV0_48

namespace KUOS
namespace PlanOS

structure MemoryOverwriteAuthorizationGrantSurface where
  sourceRequest : MemoryOverwriteAuthorizationRequestSurface
  sourceBoundary : MemoryOverwriteAuthorizationRequestBoundary
  sourceRequestBound : Bool
  selectedCandidateBoundToRequest : Bool
  externalCommitPreserved : Bool
  externalCommitCloseoutPreserved : Bool
  memoryOverwriteAuthorizationGrantOnly : Bool
  memoryOverwriteAuthorizationRequested : Bool
  memoryOverwriteAuthorizationGranted : Bool
  memoryOverwriteGranted : Bool
  truthAuthorityGranted : Bool
  blockerReleaseGranted : Bool
  sourceRequired : sourceRequestBound = true
  selectedBoundRequired : selectedCandidateBoundToRequest = true
  externalCommitRequired : externalCommitPreserved = true
  closeoutRequired : externalCommitCloseoutPreserved = true
  grantOnlyRequired : memoryOverwriteAuthorizationGrantOnly = true
  requestRequired : memoryOverwriteAuthorizationRequested = true
  authorizationRequired : memoryOverwriteAuthorizationGranted = true
  overwriteForbidden : memoryOverwriteGranted = false
  truthForbidden : truthAuthorityGranted = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure MemoryOverwriteAuthorizationGrantBoundary where
  grantOwnedByPlanOS : Bool
  sourceMemoryOverwriteAuthorizationRequestPreserved : Bool
  selectedCandidateBoundToMemoryOverwriteRequest : Bool
  externalCommitPreserved : Bool
  externalCommitCloseoutPreserved : Bool
  memoryOverwriteAuthorizationGrantOnly : Bool
  memoryOverwriteAuthorizationRequested : Bool
  memoryOverwriteAuthorizationGranted : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  grantOwnerRequired : grantOwnedByPlanOS = true
  sourcePreservedRequired : sourceMemoryOverwriteAuthorizationRequestPreserved = true
  selectedBoundRequired : selectedCandidateBoundToMemoryOverwriteRequest = true
  externalCommitRequired : externalCommitPreserved = true
  closeoutRequired : externalCommitCloseoutPreserved = true
  grantOnlyRequired : memoryOverwriteAuthorizationGrantOnly = true
  requestRequired : memoryOverwriteAuthorizationRequested = true
  authorizationRequired : memoryOverwriteAuthorizationGranted = true
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSMemoryOverwriteAuthorizationGrantBridge where
  Digest : Type
  digestOf : MemoryOverwriteAuthorizationGrantSurface → MemoryOverwriteAuthorizationGrantBoundary → Nat → Digest
  surface : MemoryOverwriteAuthorizationGrantSurface
  boundary : MemoryOverwriteAuthorizationGrantBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  nonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  truthForbidden : nonAuthority.truthAuthority = false
  overwriteForbidden : nonAuthority.memoryOverwrite = false

namespace PlanOSMemoryOverwriteAuthorizationGrantBridge

theorem source_request_asks_but_does_not_grant_memory_overwrite
    (b : PlanOSMemoryOverwriteAuthorizationGrantBridge) :
    b.surface.sourceRequest.memoryOverwriteAuthorizationRequestOnly = true ∧
      b.surface.sourceRequest.memoryOverwriteAuthorizationRequested = true ∧
      b.surface.sourceRequest.memoryOverwriteAuthorizationGranted = false ∧
      b.surface.sourceRequest.memoryOverwriteGranted = false ∧
      b.surface.sourceBoundary.memoryOverwriteAuthorizationRequested = true ∧
      b.surface.sourceBoundary.memoryOverwriteAuthorizationGranted = false ∧
      b.surface.sourceBoundary.memoryOverwrite = false := by
  exact ⟨b.surface.sourceRequest.requestOnlyRequired,
    b.surface.sourceRequest.requestRequired,
    b.surface.sourceRequest.authorizationForbidden,
    b.surface.sourceRequest.overwriteForbidden,
    b.surface.sourceBoundary.requestRequired,
    b.surface.sourceBoundary.authorizationForbidden,
    b.surface.sourceBoundary.overwriteForbidden⟩

theorem grant_binds_candidate_and_preserves_external_commit_state
    (b : PlanOSMemoryOverwriteAuthorizationGrantBridge) :
    b.surface.sourceRequestBound = true ∧
      b.surface.selectedCandidateBoundToRequest = true ∧
      b.surface.externalCommitPreserved = true ∧
      b.surface.externalCommitCloseoutPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.externalCommitRequired, b.surface.closeoutRequired⟩

theorem grant_authorizes_but_does_not_apply_memory_or_grant_truth_or_blocker_release
    (b : PlanOSMemoryOverwriteAuthorizationGrantBridge) :
    b.surface.memoryOverwriteAuthorizationGrantOnly = true ∧
      b.surface.memoryOverwriteAuthorizationRequested = true ∧
      b.surface.memoryOverwriteAuthorizationGranted = true ∧
      b.surface.memoryOverwriteGranted = false ∧
      b.surface.truthAuthorityGranted = false ∧
      b.surface.blockerReleaseGranted = false ∧
      b.boundary.memoryOverwriteAuthorizationGranted = true ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false ∧
      b.nonAuthority.truthAuthority = false ∧
      b.nonAuthority.memoryOverwrite = false := by
  exact ⟨b.surface.grantOnlyRequired, b.surface.requestRequired,
    b.surface.authorizationRequired, b.surface.overwriteForbidden,
    b.surface.truthForbidden, b.surface.blockerReleaseForbidden,
    b.boundary.authorizationRequired, b.boundary.overwriteForbidden,
    b.boundary.blockerReleaseForbidden, b.truthForbidden,
    b.overwriteForbidden⟩

theorem boundary_preserves_memory_overwrite_authorization_grant_only
    (b : PlanOSMemoryOverwriteAuthorizationGrantBridge) :
    b.boundary.grantOwnedByPlanOS = true ∧
      b.boundary.sourceMemoryOverwriteAuthorizationRequestPreserved = true ∧
      b.boundary.selectedCandidateBoundToMemoryOverwriteRequest = true ∧
      b.boundary.externalCommitPreserved = true ∧
      b.boundary.externalCommitCloseoutPreserved = true ∧
      b.boundary.memoryOverwriteAuthorizationGrantOnly = true ∧
      b.boundary.memoryOverwriteAuthorizationRequested = true ∧
      b.boundary.memoryOverwriteAuthorizationGranted = true ∧
      b.boundary.memoryOverwrite = false := by
  exact ⟨b.boundary.grantOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.externalCommitRequired,
    b.boundary.closeoutRequired, b.boundary.grantOnlyRequired,
    b.boundary.requestRequired, b.boundary.authorizationRequired,
    b.boundary.overwriteForbidden⟩

theorem history_appends_one_memory_overwrite_authorization_grant_record
    (b : PlanOSMemoryOverwriteAuthorizationGrantBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSMemoryOverwriteAuthorizationGrantBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSMemoryOverwriteAuthorizationGrantBridge

end PlanOS
end KUOS
