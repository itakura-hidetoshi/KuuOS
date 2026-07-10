import Mathlib
import KUOS.PlanOS.MemoryOverwriteCloseoutReceiptV0_51

namespace KUOS
namespace PlanOS

structure TruthAuthorityAuthorizationRequestSurface where
  sourceCloseout : MemoryOverwriteCloseoutReceiptSurface
  sourceBoundary : MemoryOverwriteCloseoutReceiptBoundary
  sourceCloseoutBound : Bool
  selectedCandidateBoundToCloseout : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  truthAuthorityAuthorizationRequestOnly : Bool
  truthAuthorityAuthorizationRequested : Bool
  truthAuthorityAuthorizationGranted : Bool
  truthAuthorityGranted : Bool
  blockerReleaseGranted : Bool
  sourceRequired : sourceCloseoutBound = true
  selectedBoundRequired : selectedCandidateBoundToCloseout = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  closeoutPreservedRequired : memoryOverwriteCloseoutPreserved = true
  cycleClosedRequired : cycleClosedPreserved = true
  requestOnlyRequired : truthAuthorityAuthorizationRequestOnly = true
  requestRequired : truthAuthorityAuthorizationRequested = true
  authorizationForbidden : truthAuthorityAuthorizationGranted = false
  truthForbidden : truthAuthorityGranted = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure TruthAuthorityAuthorizationRequestBoundary where
  requestOwnedByPlanOS : Bool
  sourceMemoryOverwriteCloseoutPreserved : Bool
  selectedCandidateBoundToMemoryOverwriteCloseout : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  truthAuthorityAuthorizationRequestOnly : Bool
  truthAuthorityAuthorizationRequested : Bool
  truthAuthorityAuthorizationGranted : Bool
  truthAuthorityGranted : Bool
  blockerReleaseGranted : Bool
  requestOwnerRequired : requestOwnedByPlanOS = true
  sourcePreservedRequired : sourceMemoryOverwriteCloseoutPreserved = true
  selectedBoundRequired : selectedCandidateBoundToMemoryOverwriteCloseout = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  closeoutPreservedRequired : memoryOverwriteCloseoutPreserved = true
  cycleClosedRequired : cycleClosedPreserved = true
  requestOnlyRequired : truthAuthorityAuthorizationRequestOnly = true
  requestRequired : truthAuthorityAuthorizationRequested = true
  authorizationForbidden : truthAuthorityAuthorizationGranted = false
  truthForbidden : truthAuthorityGranted = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSTruthAuthorityAuthorizationRequestBridge where
  Digest : Type
  digestOf : TruthAuthorityAuthorizationRequestSurface → TruthAuthorityAuthorizationRequestBoundary → Nat → Digest
  surface : TruthAuthorityAuthorizationRequestSurface
  boundary : TruthAuthorityAuthorizationRequestBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  nonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  truthForbidden : nonAuthority.truthAuthority = false

namespace PlanOSTruthAuthorityAuthorizationRequestBridge

theorem source_closeout_preserves_memory_overwrite_and_keeps_truth_and_release_closed
    (b : PlanOSTruthAuthorityAuthorizationRequestBridge) :
    b.surface.sourceCloseout.memoryOverwritePreserved = true ∧
      b.surface.sourceCloseout.closeoutReceiptOnly = true ∧
      b.surface.sourceCloseout.cycleClosed = true ∧
      b.surface.sourceCloseout.truthAuthorityGranted = false ∧
      b.surface.sourceCloseout.blockerReleaseGranted = false ∧
      b.surface.sourceBoundary.memoryOverwritePreserved = true ∧
      b.surface.sourceBoundary.memoryOverwriteCloseoutReceiptOnly = true ∧
      b.surface.sourceBoundary.cycleClosed = true ∧
      b.surface.sourceBoundary.blockerReleaseGranted = false := by
  exact ⟨b.surface.sourceCloseout.overwriteRequired,
    b.surface.sourceCloseout.closeoutOnlyRequired,
    b.surface.sourceCloseout.cycleClosedRequired,
    b.surface.sourceCloseout.truthForbidden,
    b.surface.sourceCloseout.blockerReleaseForbidden,
    b.surface.sourceBoundary.overwriteRequired,
    b.surface.sourceBoundary.closeoutOnlyRequired,
    b.surface.sourceBoundary.cycleClosedRequired,
    b.surface.sourceBoundary.blockerReleaseForbidden⟩

theorem request_binds_candidate_and_preserves_memory_closeout_state
    (b : PlanOSTruthAuthorityAuthorizationRequestBridge) :
    b.surface.sourceCloseoutBound = true ∧
      b.surface.selectedCandidateBoundToCloseout = true ∧
      b.surface.memoryOverwritePreserved = true ∧
      b.surface.memoryOverwriteCloseoutPreserved = true ∧
      b.surface.cycleClosedPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.memoryOverwriteRequired, b.surface.closeoutPreservedRequired,
    b.surface.cycleClosedRequired⟩

theorem request_asks_truth_authority_but_does_not_grant_truth_or_blocker_release
    (b : PlanOSTruthAuthorityAuthorizationRequestBridge) :
    b.surface.truthAuthorityAuthorizationRequestOnly = true ∧
      b.surface.truthAuthorityAuthorizationRequested = true ∧
      b.surface.truthAuthorityAuthorizationGranted = false ∧
      b.surface.truthAuthorityGranted = false ∧
      b.surface.blockerReleaseGranted = false ∧
      b.boundary.truthAuthorityAuthorizationGranted = false ∧
      b.boundary.truthAuthorityGranted = false ∧
      b.boundary.blockerReleaseGranted = false ∧
      b.nonAuthority.truthAuthority = false := by
  exact ⟨b.surface.requestOnlyRequired,
    b.surface.requestRequired,
    b.surface.authorizationForbidden,
    b.surface.truthForbidden,
    b.surface.blockerReleaseForbidden,
    b.boundary.authorizationForbidden,
    b.boundary.truthForbidden,
    b.boundary.blockerReleaseForbidden,
    b.truthForbidden⟩

theorem boundary_preserves_truth_authority_authorization_request_only
    (b : PlanOSTruthAuthorityAuthorizationRequestBridge) :
    b.boundary.requestOwnedByPlanOS = true ∧
      b.boundary.sourceMemoryOverwriteCloseoutPreserved = true ∧
      b.boundary.selectedCandidateBoundToMemoryOverwriteCloseout = true ∧
      b.boundary.memoryOverwritePreserved = true ∧
      b.boundary.memoryOverwriteCloseoutPreserved = true ∧
      b.boundary.cycleClosedPreserved = true ∧
      b.boundary.truthAuthorityAuthorizationRequestOnly = true ∧
      b.boundary.truthAuthorityAuthorizationRequested = true ∧
      b.boundary.truthAuthorityAuthorizationGranted = false ∧
      b.boundary.truthAuthorityGranted = false := by
  exact ⟨b.boundary.requestOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.memoryOverwriteRequired,
    b.boundary.closeoutPreservedRequired, b.boundary.cycleClosedRequired,
    b.boundary.requestOnlyRequired, b.boundary.requestRequired,
    b.boundary.authorizationForbidden, b.boundary.truthForbidden⟩

theorem history_appends_one_truth_authority_authorization_request_record
    (b : PlanOSTruthAuthorityAuthorizationRequestBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSTruthAuthorityAuthorizationRequestBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSTruthAuthorityAuthorizationRequestBridge

end PlanOS
end KUOS
