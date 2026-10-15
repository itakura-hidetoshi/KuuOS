import Mathlib
import KUOS.PlanOS.BlockerReleaseAuthorizationGrantV0_57

namespace KUOS
namespace PlanOS

structure BlockerReleaseReceiptSurface where
  sourceGrant : BlockerReleaseAuthorizationGrantSurface
  sourceBoundary : BlockerReleaseAuthorizationGrantBoundary
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
  blockerReleaseReceiptOnly : Bool
  blockerReleaseAuthorizationRequested : Bool
  blockerReleaseAuthorizationGranted : Bool
  blockerReleaseGranted : Bool
  blockerReleaseCycleClosed : Bool
  sourceRequired : sourceGrantBound = true
  selectedBoundRequired : selectedCandidateBoundToGrant = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  memoryCloseoutRequired : memoryOverwriteCloseoutPreserved = true
  cyclePreservedRequired : cycleClosedPreserved = true
  truthGrantPreservedRequired : truthAuthorityAuthorizationGrantPreserved = true
  truthPreservedRequired : truthAuthorityPreserved = true
  truthCyclePreservedRequired : truthAuthorityCycleClosedPreserved = true
  requestPreservedRequired : blockerReleaseAuthorizationRequestPreserved = true
  grantPreservedRequired : blockerReleaseAuthorizationGrantPreserved = true
  receiptOnlyRequired : blockerReleaseReceiptOnly = true
  requestRequired : blockerReleaseAuthorizationRequested = true
  authorizationRequired : blockerReleaseAuthorizationGranted = true
  releaseRequired : blockerReleaseGranted = true
  cycleOpenRequired : blockerReleaseCycleClosed = false

structure BlockerReleaseReceiptBoundary where
  receiptOwnedByPlanOS : Bool
  sourceBlockerReleaseAuthorizationGrantPreserved : Bool
  selectedCandidateBoundToBlockerReleaseGrant : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  truthAuthorityAuthorizationGrantPreserved : Bool
  truthAuthorityPreserved : Bool
  truthAuthorityCycleClosedPreserved : Bool
  blockerReleaseAuthorizationRequestPreserved : Bool
  blockerReleaseAuthorizationGrantPreserved : Bool
  blockerReleaseReceiptOnly : Bool
  blockerReleaseAuthorizationRequested : Bool
  blockerReleaseAuthorizationGranted : Bool
  blockerReleaseGranted : Bool
  blockerReleaseCycleClosed : Bool
  ownerRequired : receiptOwnedByPlanOS = true
  sourcePreservedRequired : sourceBlockerReleaseAuthorizationGrantPreserved = true
  selectedBoundRequired : selectedCandidateBoundToBlockerReleaseGrant = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  memoryCloseoutRequired : memoryOverwriteCloseoutPreserved = true
  cyclePreservedRequired : cycleClosedPreserved = true
  truthGrantPreservedRequired : truthAuthorityAuthorizationGrantPreserved = true
  truthPreservedRequired : truthAuthorityPreserved = true
  truthCyclePreservedRequired : truthAuthorityCycleClosedPreserved = true
  requestPreservedRequired : blockerReleaseAuthorizationRequestPreserved = true
  grantPreservedRequired : blockerReleaseAuthorizationGrantPreserved = true
  receiptOnlyRequired : blockerReleaseReceiptOnly = true
  requestRequired : blockerReleaseAuthorizationRequested = true
  authorizationRequired : blockerReleaseAuthorizationGranted = true
  releaseRequired : blockerReleaseGranted = true
  cycleOpenRequired : blockerReleaseCycleClosed = false

structure PlanOSBlockerReleaseReceiptBridge where
  Digest : Type
  digestOf : BlockerReleaseReceiptSurface → BlockerReleaseReceiptBoundary → Nat → Digest
  surface : BlockerReleaseReceiptSurface
  boundary : BlockerReleaseReceiptBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  recorderNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  recorderTruthForbidden : recorderNonAuthority.truthAuthority = false

namespace PlanOSBlockerReleaseReceiptBridge

theorem source_grant_authorizes_but_does_not_release_blockers
    (b : PlanOSBlockerReleaseReceiptBridge) :
    b.surface.sourceGrant.blockerReleaseAuthorizationGrantOnly = true ∧
      b.surface.sourceGrant.blockerReleaseAuthorizationRequested = true ∧
      b.surface.sourceGrant.blockerReleaseAuthorizationGranted = true ∧
      b.surface.sourceGrant.blockerReleaseGranted = false ∧
      b.surface.sourceBoundary.blockerReleaseAuthorizationGranted = true ∧
      b.surface.sourceBoundary.blockerReleaseGranted = false := by
  exact ⟨b.surface.sourceGrant.grantOnlyRequired,
    b.surface.sourceGrant.requestRequired,
    b.surface.sourceGrant.authorizationRequired,
    b.surface.sourceGrant.releaseForbidden,
    b.surface.sourceBoundary.authorizationRequired,
    b.surface.sourceBoundary.releaseForbidden⟩

theorem receipt_binds_candidate_and_preserves_authorized_state
    (b : PlanOSBlockerReleaseReceiptBridge) :
    b.surface.sourceGrantBound = true ∧
      b.surface.selectedCandidateBoundToGrant = true ∧
      b.surface.memoryOverwritePreserved = true ∧
      b.surface.memoryOverwriteCloseoutPreserved = true ∧
      b.surface.cycleClosedPreserved = true ∧
      b.surface.truthAuthorityAuthorizationGrantPreserved = true ∧
      b.surface.truthAuthorityPreserved = true ∧
      b.surface.truthAuthorityCycleClosedPreserved = true ∧
      b.surface.blockerReleaseAuthorizationRequestPreserved = true ∧
      b.surface.blockerReleaseAuthorizationGrantPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.memoryOverwriteRequired, b.surface.memoryCloseoutRequired,
    b.surface.cyclePreservedRequired, b.surface.truthGrantPreservedRequired,
    b.surface.truthPreservedRequired, b.surface.truthCyclePreservedRequired,
    b.surface.requestPreservedRequired, b.surface.grantPreservedRequired⟩

theorem receipt_records_blocker_release_but_keeps_cycle_open
    (b : PlanOSBlockerReleaseReceiptBridge) :
    b.surface.blockerReleaseReceiptOnly = true ∧
      b.surface.blockerReleaseAuthorizationRequested = true ∧
      b.surface.blockerReleaseAuthorizationGranted = true ∧
      b.surface.blockerReleaseGranted = true ∧
      b.surface.blockerReleaseCycleClosed = false ∧
      b.boundary.blockerReleaseAuthorizationGranted = true ∧
      b.boundary.blockerReleaseGranted = true ∧
      b.boundary.blockerReleaseCycleClosed = false ∧
      b.recorderNonAuthority.truthAuthority = false := by
  exact ⟨b.surface.receiptOnlyRequired, b.surface.requestRequired,
    b.surface.authorizationRequired, b.surface.releaseRequired,
    b.surface.cycleOpenRequired, b.boundary.authorizationRequired,
    b.boundary.releaseRequired, b.boundary.cycleOpenRequired,
    b.recorderTruthForbidden⟩

theorem boundary_preserves_blocker_release_receipt_only
    (b : PlanOSBlockerReleaseReceiptBridge) :
    b.boundary.receiptOwnedByPlanOS = true ∧
      b.boundary.sourceBlockerReleaseAuthorizationGrantPreserved = true ∧
      b.boundary.selectedCandidateBoundToBlockerReleaseGrant = true ∧
      b.boundary.memoryOverwritePreserved = true ∧
      b.boundary.memoryOverwriteCloseoutPreserved = true ∧
      b.boundary.cycleClosedPreserved = true ∧
      b.boundary.truthAuthorityAuthorizationGrantPreserved = true ∧
      b.boundary.truthAuthorityPreserved = true ∧
      b.boundary.truthAuthorityCycleClosedPreserved = true ∧
      b.boundary.blockerReleaseAuthorizationRequestPreserved = true ∧
      b.boundary.blockerReleaseAuthorizationGrantPreserved = true ∧
      b.boundary.blockerReleaseReceiptOnly = true ∧
      b.boundary.blockerReleaseAuthorizationRequested = true ∧
      b.boundary.blockerReleaseAuthorizationGranted = true ∧
      b.boundary.blockerReleaseGranted = true ∧
      b.boundary.blockerReleaseCycleClosed = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.memoryOverwriteRequired,
    b.boundary.memoryCloseoutRequired, b.boundary.cyclePreservedRequired,
    b.boundary.truthGrantPreservedRequired, b.boundary.truthPreservedRequired,
    b.boundary.truthCyclePreservedRequired, b.boundary.requestPreservedRequired,
    b.boundary.grantPreservedRequired, b.boundary.receiptOnlyRequired,
    b.boundary.requestRequired, b.boundary.authorizationRequired,
    b.boundary.releaseRequired, b.boundary.cycleOpenRequired⟩

theorem history_appends_one_blocker_release_receipt_record
    (b : PlanOSBlockerReleaseReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSBlockerReleaseReceiptBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSBlockerReleaseReceiptBridge

end PlanOS
end KUOS
