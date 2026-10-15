import Mathlib
import KUOS.PlanOS.ExternalCommitCloseoutReceiptV0_47

namespace KUOS
namespace PlanOS

structure MemoryOverwriteAuthorizationRequestSurface where
  sourceCloseout : ExternalCommitCloseoutReceiptSurface
  sourceBoundary : ExternalCommitCloseoutReceiptBoundary
  sourceCloseoutBound : Bool
  selectedCandidateBoundToCloseout : Bool
  externalCommitPreserved : Bool
  externalCommitCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  memoryOverwriteAuthorizationRequestOnly : Bool
  memoryOverwriteAuthorizationRequested : Bool
  memoryOverwriteAuthorizationGranted : Bool
  memoryOverwriteGranted : Bool
  truthAuthorityGranted : Bool
  blockerReleaseGranted : Bool
  sourceRequired : sourceCloseoutBound = true
  selectedBoundRequired : selectedCandidateBoundToCloseout = true
  externalCommitRequired : externalCommitPreserved = true
  closeoutPreservedRequired : externalCommitCloseoutPreserved = true
  cycleClosedRequired : cycleClosedPreserved = true
  requestOnlyRequired : memoryOverwriteAuthorizationRequestOnly = true
  requestRequired : memoryOverwriteAuthorizationRequested = true
  authorizationForbidden : memoryOverwriteAuthorizationGranted = false
  overwriteForbidden : memoryOverwriteGranted = false
  truthForbidden : truthAuthorityGranted = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure MemoryOverwriteAuthorizationRequestBoundary where
  requestOwnedByPlanOS : Bool
  sourceExternalCommitCloseoutPreserved : Bool
  selectedCandidateBoundToExternalCommitCloseout : Bool
  externalCommitPreserved : Bool
  externalCommitCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  memoryOverwriteAuthorizationRequestOnly : Bool
  memoryOverwriteAuthorizationRequested : Bool
  memoryOverwriteAuthorizationGranted : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  requestOwnerRequired : requestOwnedByPlanOS = true
  sourcePreservedRequired : sourceExternalCommitCloseoutPreserved = true
  selectedBoundRequired : selectedCandidateBoundToExternalCommitCloseout = true
  externalCommitRequired : externalCommitPreserved = true
  closeoutPreservedRequired : externalCommitCloseoutPreserved = true
  cycleClosedRequired : cycleClosedPreserved = true
  requestOnlyRequired : memoryOverwriteAuthorizationRequestOnly = true
  requestRequired : memoryOverwriteAuthorizationRequested = true
  authorizationForbidden : memoryOverwriteAuthorizationGranted = false
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSMemoryOverwriteAuthorizationRequestBridge where
  Digest : Type
  digestOf : MemoryOverwriteAuthorizationRequestSurface → MemoryOverwriteAuthorizationRequestBoundary → Nat → Digest
  surface : MemoryOverwriteAuthorizationRequestSurface
  boundary : MemoryOverwriteAuthorizationRequestBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  nonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  truthForbidden : nonAuthority.truthAuthority = false
  overwriteForbidden : nonAuthority.memoryOverwrite = false

namespace PlanOSMemoryOverwriteAuthorizationRequestBridge

theorem source_closeout_preserves_external_commit_and_keeps_authority_closed
    (b : PlanOSMemoryOverwriteAuthorizationRequestBridge) :
    b.surface.sourceCloseout.externalCommitPreserved = true ∧
      b.surface.sourceCloseout.cycleClosed = true ∧
      b.surface.sourceCloseout.memoryOverwriteGranted = false ∧
      b.surface.sourceCloseout.truthAuthorityGranted = false ∧
      b.surface.sourceBoundary.externalCommitPreserved = true ∧
      b.surface.sourceBoundary.cycleClosed = true ∧
      b.surface.sourceBoundary.memoryOverwrite = false ∧
      b.surface.sourceBoundary.blockerReleaseGranted = false := by
  exact ⟨b.surface.sourceCloseout.externalCommitRequired,
    b.surface.sourceCloseout.cycleClosedRequired,
    b.surface.sourceCloseout.overwriteForbidden,
    b.surface.sourceCloseout.truthForbidden,
    b.surface.sourceBoundary.externalCommitRequired,
    b.surface.sourceBoundary.cycleClosedRequired,
    b.surface.sourceBoundary.overwriteForbidden,
    b.surface.sourceBoundary.blockerReleaseForbidden⟩

theorem request_binds_candidate_and_preserves_closeout_state
    (b : PlanOSMemoryOverwriteAuthorizationRequestBridge) :
    b.surface.sourceCloseoutBound = true ∧
      b.surface.selectedCandidateBoundToCloseout = true ∧
      b.surface.externalCommitPreserved = true ∧
      b.surface.externalCommitCloseoutPreserved = true ∧
      b.surface.cycleClosedPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.externalCommitRequired, b.surface.closeoutPreservedRequired,
    b.surface.cycleClosedRequired⟩

theorem request_asks_memory_overwrite_but_does_not_grant_overwrite_truth_or_blocker_release
    (b : PlanOSMemoryOverwriteAuthorizationRequestBridge) :
    b.surface.memoryOverwriteAuthorizationRequestOnly = true ∧
      b.surface.memoryOverwriteAuthorizationRequested = true ∧
      b.surface.memoryOverwriteAuthorizationGranted = false ∧
      b.surface.memoryOverwriteGranted = false ∧
      b.surface.truthAuthorityGranted = false ∧
      b.surface.blockerReleaseGranted = false ∧
      b.boundary.memoryOverwriteAuthorizationGranted = false ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false ∧
      b.nonAuthority.truthAuthority = false ∧
      b.nonAuthority.memoryOverwrite = false := by
  exact ⟨b.surface.requestOnlyRequired,
    b.surface.requestRequired,
    b.surface.authorizationForbidden,
    b.surface.overwriteForbidden,
    b.surface.truthForbidden,
    b.surface.blockerReleaseForbidden,
    b.boundary.authorizationForbidden,
    b.boundary.overwriteForbidden,
    b.boundary.blockerReleaseForbidden,
    b.truthForbidden,
    b.overwriteForbidden⟩

theorem boundary_preserves_memory_overwrite_authorization_request_only
    (b : PlanOSMemoryOverwriteAuthorizationRequestBridge) :
    b.boundary.requestOwnedByPlanOS = true ∧
      b.boundary.sourceExternalCommitCloseoutPreserved = true ∧
      b.boundary.selectedCandidateBoundToExternalCommitCloseout = true ∧
      b.boundary.externalCommitPreserved = true ∧
      b.boundary.externalCommitCloseoutPreserved = true ∧
      b.boundary.cycleClosedPreserved = true ∧
      b.boundary.memoryOverwriteAuthorizationRequestOnly = true ∧
      b.boundary.memoryOverwriteAuthorizationRequested = true ∧
      b.boundary.memoryOverwriteAuthorizationGranted = false ∧
      b.boundary.memoryOverwrite = false := by
  exact ⟨b.boundary.requestOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.externalCommitRequired,
    b.boundary.closeoutPreservedRequired, b.boundary.cycleClosedRequired,
    b.boundary.requestOnlyRequired, b.boundary.requestRequired,
    b.boundary.authorizationForbidden, b.boundary.overwriteForbidden⟩

theorem history_appends_one_memory_overwrite_authorization_request_record
    (b : PlanOSMemoryOverwriteAuthorizationRequestBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSMemoryOverwriteAuthorizationRequestBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSMemoryOverwriteAuthorizationRequestBridge

end PlanOS
end KUOS
