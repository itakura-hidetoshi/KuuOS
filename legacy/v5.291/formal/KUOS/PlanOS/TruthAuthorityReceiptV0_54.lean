import Mathlib
import KUOS.PlanOS.TruthAuthorityAuthorizationGrantV0_53

namespace KUOS
namespace PlanOS

structure TruthAuthorityReceiptSurface where
  sourceGrant : TruthAuthorityAuthorizationGrantSurface
  sourceBoundary : TruthAuthorityAuthorizationGrantBoundary
  sourceGrantBound : Bool
  selectedCandidateBoundToGrant : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  truthAuthorityAuthorizationGrantPreserved : Bool
  truthAuthorityReceiptOnly : Bool
  truthAuthorityAuthorizationRequested : Bool
  truthAuthorityAuthorizationGranted : Bool
  truthAuthorityGranted : Bool
  blockerReleaseGranted : Bool
  sourceRequired : sourceGrantBound = true
  selectedBoundRequired : selectedCandidateBoundToGrant = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  closeoutPreservedRequired : memoryOverwriteCloseoutPreserved = true
  cycleClosedRequired : cycleClosedPreserved = true
  grantPreservedRequired : truthAuthorityAuthorizationGrantPreserved = true
  receiptOnlyRequired : truthAuthorityReceiptOnly = true
  requestRequired : truthAuthorityAuthorizationRequested = true
  authorizationRequired : truthAuthorityAuthorizationGranted = true
  truthRequired : truthAuthorityGranted = true
  blockerReleaseForbidden : blockerReleaseGranted = false

structure TruthAuthorityReceiptBoundary where
  receiptOwnedByPlanOS : Bool
  sourceTruthAuthorityAuthorizationGrantPreserved : Bool
  selectedCandidateBoundToTruthAuthorityGrant : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  truthAuthorityAuthorizationGrantPreserved : Bool
  truthAuthorityReceiptOnly : Bool
  truthAuthorityAuthorizationRequested : Bool
  truthAuthorityAuthorizationGranted : Bool
  truthAuthorityGranted : Bool
  blockerReleaseGranted : Bool
  receiptOwnerRequired : receiptOwnedByPlanOS = true
  sourcePreservedRequired : sourceTruthAuthorityAuthorizationGrantPreserved = true
  selectedBoundRequired : selectedCandidateBoundToTruthAuthorityGrant = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  closeoutPreservedRequired : memoryOverwriteCloseoutPreserved = true
  cycleClosedRequired : cycleClosedPreserved = true
  grantPreservedRequired : truthAuthorityAuthorizationGrantPreserved = true
  receiptOnlyRequired : truthAuthorityReceiptOnly = true
  requestRequired : truthAuthorityAuthorizationRequested = true
  authorizationRequired : truthAuthorityAuthorizationGranted = true
  truthRequired : truthAuthorityGranted = true
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSTruthAuthorityReceiptBridge where
  Digest : Type
  digestOf : TruthAuthorityReceiptSurface → TruthAuthorityReceiptBoundary → Nat → Digest
  surface : TruthAuthorityReceiptSurface
  boundary : TruthAuthorityReceiptBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  recorderNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  recorderTruthForbidden : recorderNonAuthority.truthAuthority = false

namespace PlanOSTruthAuthorityReceiptBridge

theorem source_grant_authorizes_but_does_not_apply_truth_authority
    (b : PlanOSTruthAuthorityReceiptBridge) :
    b.surface.sourceGrant.truthAuthorityAuthorizationGrantOnly = true ∧
      b.surface.sourceGrant.truthAuthorityAuthorizationRequested = true ∧
      b.surface.sourceGrant.truthAuthorityAuthorizationGranted = true ∧
      b.surface.sourceGrant.truthAuthorityGranted = false ∧
      b.surface.sourceGrant.blockerReleaseGranted = false ∧
      b.surface.sourceBoundary.truthAuthorityAuthorizationGranted = true ∧
      b.surface.sourceBoundary.truthAuthorityGranted = false ∧
      b.surface.sourceBoundary.blockerReleaseGranted = false := by
  exact ⟨b.surface.sourceGrant.grantOnlyRequired,
    b.surface.sourceGrant.requestRequired,
    b.surface.sourceGrant.authorizationRequired,
    b.surface.sourceGrant.truthForbidden,
    b.surface.sourceGrant.blockerReleaseForbidden,
    b.surface.sourceBoundary.authorizationRequired,
    b.surface.sourceBoundary.truthForbidden,
    b.surface.sourceBoundary.blockerReleaseForbidden⟩

theorem receipt_binds_candidate_and_preserves_authorized_state
    (b : PlanOSTruthAuthorityReceiptBridge) :
    b.surface.sourceGrantBound = true ∧
      b.surface.selectedCandidateBoundToGrant = true ∧
      b.surface.memoryOverwritePreserved = true ∧
      b.surface.memoryOverwriteCloseoutPreserved = true ∧
      b.surface.cycleClosedPreserved = true ∧
      b.surface.truthAuthorityAuthorizationGrantPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.memoryOverwriteRequired, b.surface.closeoutPreservedRequired,
    b.surface.cycleClosedRequired, b.surface.grantPreservedRequired⟩

theorem receipt_records_truth_authority_but_not_blocker_release
    (b : PlanOSTruthAuthorityReceiptBridge) :
    b.surface.truthAuthorityReceiptOnly = true ∧
      b.surface.truthAuthorityAuthorizationRequested = true ∧
      b.surface.truthAuthorityAuthorizationGranted = true ∧
      b.surface.truthAuthorityGranted = true ∧
      b.surface.blockerReleaseGranted = false ∧
      b.boundary.truthAuthorityAuthorizationGranted = true ∧
      b.boundary.truthAuthorityGranted = true ∧
      b.boundary.blockerReleaseGranted = false ∧
      b.recorderNonAuthority.truthAuthority = false := by
  exact ⟨b.surface.receiptOnlyRequired, b.surface.requestRequired,
    b.surface.authorizationRequired, b.surface.truthRequired,
    b.surface.blockerReleaseForbidden, b.boundary.authorizationRequired,
    b.boundary.truthRequired, b.boundary.blockerReleaseForbidden,
    b.recorderTruthForbidden⟩

theorem boundary_preserves_truth_authority_receipt_only
    (b : PlanOSTruthAuthorityReceiptBridge) :
    b.boundary.receiptOwnedByPlanOS = true ∧
      b.boundary.sourceTruthAuthorityAuthorizationGrantPreserved = true ∧
      b.boundary.selectedCandidateBoundToTruthAuthorityGrant = true ∧
      b.boundary.memoryOverwritePreserved = true ∧
      b.boundary.memoryOverwriteCloseoutPreserved = true ∧
      b.boundary.cycleClosedPreserved = true ∧
      b.boundary.truthAuthorityAuthorizationGrantPreserved = true ∧
      b.boundary.truthAuthorityReceiptOnly = true ∧
      b.boundary.truthAuthorityAuthorizationRequested = true ∧
      b.boundary.truthAuthorityAuthorizationGranted = true ∧
      b.boundary.truthAuthorityGranted = true := by
  exact ⟨b.boundary.receiptOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.memoryOverwriteRequired,
    b.boundary.closeoutPreservedRequired, b.boundary.cycleClosedRequired,
    b.boundary.grantPreservedRequired, b.boundary.receiptOnlyRequired,
    b.boundary.requestRequired, b.boundary.authorizationRequired,
    b.boundary.truthRequired⟩

theorem history_appends_one_truth_authority_receipt_record
    (b : PlanOSTruthAuthorityReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSTruthAuthorityReceiptBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSTruthAuthorityReceiptBridge

end PlanOS
end KUOS
