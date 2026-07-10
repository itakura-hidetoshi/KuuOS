import Mathlib
import KUOS.PlanOS.MemoryOverwriteAuthorizationGrantV0_49

namespace KUOS
namespace PlanOS

structure MemoryOverwriteReceiptSurface where
  sourceGrant : MemoryOverwriteAuthorizationGrantSurface
  sourceBoundary : MemoryOverwriteAuthorizationGrantBoundary
  sourceGrantBound : Bool
  selectedCandidateBoundToGrant : Bool
  externalCommitPreserved : Bool
  externalCommitCloseoutPreserved : Bool
  memoryOverwriteAuthorizationGrantPreserved : Bool
  memoryOverwriteReceiptOnly : Bool
  memoryOverwriteAuthorizationRequested : Bool
  memoryOverwriteAuthorizationGranted : Bool
  memoryOverwriteGranted : Bool
  truthAuthorityGranted : Bool
  blockerReleaseGranted : Bool
  sourceRequired : sourceGrantBound = true
  selectedBoundRequired : selectedCandidateBoundToGrant = true
  externalCommitRequired : externalCommitPreserved = true
  closeoutRequired : externalCommitCloseoutPreserved = true
  grantPreservedRequired : memoryOverwriteAuthorizationGrantPreserved = true
  receiptOnlyRequired : memoryOverwriteReceiptOnly = true
  requestRequired : memoryOverwriteAuthorizationRequested = true
  authorizationRequired : memoryOverwriteAuthorizationGranted = true
  overwriteRequired : memoryOverwriteGranted = true
  truthForbidden : truthAuthorityGranted = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure MemoryOverwriteReceiptBoundary where
  receiptOwnedByPlanOS : Bool
  sourceMemoryOverwriteAuthorizationGrantPreserved : Bool
  selectedCandidateBoundToMemoryOverwriteGrant : Bool
  externalCommitPreserved : Bool
  externalCommitCloseoutPreserved : Bool
  memoryOverwriteAuthorizationGrantPreserved : Bool
  memoryOverwriteReceiptOnly : Bool
  memoryOverwriteAuthorizationRequested : Bool
  memoryOverwriteAuthorizationGranted : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  receiptOwnerRequired : receiptOwnedByPlanOS = true
  sourcePreservedRequired : sourceMemoryOverwriteAuthorizationGrantPreserved = true
  selectedBoundRequired : selectedCandidateBoundToMemoryOverwriteGrant = true
  externalCommitRequired : externalCommitPreserved = true
  closeoutRequired : externalCommitCloseoutPreserved = true
  grantPreservedRequired : memoryOverwriteAuthorizationGrantPreserved = true
  receiptOnlyRequired : memoryOverwriteReceiptOnly = true
  requestRequired : memoryOverwriteAuthorizationRequested = true
  authorizationRequired : memoryOverwriteAuthorizationGranted = true
  overwriteRequired : memoryOverwrite = true
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSMemoryOverwriteReceiptBridge where
  Digest : Type
  digestOf : MemoryOverwriteReceiptSurface → MemoryOverwriteReceiptBoundary → Nat → Digest
  surface : MemoryOverwriteReceiptSurface
  boundary : MemoryOverwriteReceiptBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  nonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  truthForbidden : nonAuthority.truthAuthority = false

namespace PlanOSMemoryOverwriteReceiptBridge

theorem source_grant_authorizes_but_does_not_apply_memory
    (b : PlanOSMemoryOverwriteReceiptBridge) :
    b.surface.sourceGrant.memoryOverwriteAuthorizationGrantOnly = true ∧
      b.surface.sourceGrant.memoryOverwriteAuthorizationGranted = true ∧
      b.surface.sourceGrant.memoryOverwriteGranted = false ∧
      b.surface.sourceGrant.truthAuthorityGranted = false ∧
      b.surface.sourceBoundary.memoryOverwriteAuthorizationGranted = true ∧
      b.surface.sourceBoundary.memoryOverwrite = false ∧
      b.surface.sourceBoundary.blockerReleaseGranted = false := by
  exact ⟨b.surface.sourceGrant.grantOnlyRequired,
    b.surface.sourceGrant.authorizationRequired,
    b.surface.sourceGrant.overwriteForbidden,
    b.surface.sourceGrant.truthForbidden,
    b.surface.sourceBoundary.authorizationRequired,
    b.surface.sourceBoundary.overwriteForbidden,
    b.surface.sourceBoundary.blockerReleaseForbidden⟩

theorem receipt_binds_candidate_and_preserves_authorized_state
    (b : PlanOSMemoryOverwriteReceiptBridge) :
    b.surface.sourceGrantBound = true ∧
      b.surface.selectedCandidateBoundToGrant = true ∧
      b.surface.externalCommitPreserved = true ∧
      b.surface.externalCommitCloseoutPreserved = true ∧
      b.surface.memoryOverwriteAuthorizationGrantPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.externalCommitRequired, b.surface.closeoutRequired,
    b.surface.grantPreservedRequired⟩

theorem receipt_records_memory_overwrite_but_not_truth_or_blocker_release
    (b : PlanOSMemoryOverwriteReceiptBridge) :
    b.surface.memoryOverwriteReceiptOnly = true ∧
      b.surface.memoryOverwriteAuthorizationRequested = true ∧
      b.surface.memoryOverwriteAuthorizationGranted = true ∧
      b.surface.memoryOverwriteGranted = true ∧
      b.surface.truthAuthorityGranted = false ∧
      b.surface.blockerReleaseGranted = false ∧
      b.boundary.memoryOverwriteAuthorizationGranted = true ∧
      b.boundary.memoryOverwrite = true ∧
      b.boundary.blockerReleaseGranted = false ∧
      b.nonAuthority.truthAuthority = false := by
  exact ⟨b.surface.receiptOnlyRequired,
    b.surface.requestRequired,
    b.surface.authorizationRequired,
    b.surface.overwriteRequired,
    b.surface.truthForbidden,
    b.surface.blockerReleaseForbidden,
    b.boundary.authorizationRequired,
    b.boundary.overwriteRequired,
    b.boundary.blockerReleaseForbidden,
    b.truthForbidden⟩

theorem boundary_preserves_memory_overwrite_receipt_only
    (b : PlanOSMemoryOverwriteReceiptBridge) :
    b.boundary.receiptOwnedByPlanOS = true ∧
      b.boundary.sourceMemoryOverwriteAuthorizationGrantPreserved = true ∧
      b.boundary.selectedCandidateBoundToMemoryOverwriteGrant = true ∧
      b.boundary.memoryOverwriteAuthorizationGrantPreserved = true ∧
      b.boundary.memoryOverwriteReceiptOnly = true ∧
      b.boundary.memoryOverwriteAuthorizationRequested = true ∧
      b.boundary.memoryOverwriteAuthorizationGranted = true ∧
      b.boundary.memoryOverwrite = true := by
  exact ⟨b.boundary.receiptOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.grantPreservedRequired,
    b.boundary.receiptOnlyRequired, b.boundary.requestRequired,
    b.boundary.authorizationRequired, b.boundary.overwriteRequired⟩

theorem history_appends_one_memory_overwrite_receipt_record
    (b : PlanOSMemoryOverwriteReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSMemoryOverwriteReceiptBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSMemoryOverwriteReceiptBridge

end PlanOS
end KUOS
