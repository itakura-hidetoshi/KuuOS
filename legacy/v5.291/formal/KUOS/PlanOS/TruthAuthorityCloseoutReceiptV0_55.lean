import Mathlib
import KUOS.PlanOS.TruthAuthorityReceiptV0_54

namespace KUOS
namespace PlanOS

structure TruthAuthorityCloseoutReceiptSurface where
  sourceReceipt : TruthAuthorityReceiptSurface
  sourceBoundary : TruthAuthorityReceiptBoundary
  sourceReceiptBound : Bool
  selectedCandidateBoundToReceipt : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  truthAuthorityAuthorizationGrantPreserved : Bool
  truthAuthorityPreserved : Bool
  truthAuthorityCloseoutReceiptOnly : Bool
  truthAuthorityCycleClosed : Bool
  blockerReleaseGranted : Bool
  sourceRequired : sourceReceiptBound = true
  selectedBoundRequired : selectedCandidateBoundToReceipt = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  memoryCloseoutRequired : memoryOverwriteCloseoutPreserved = true
  cyclePreservedRequired : cycleClosedPreserved = true
  grantPreservedRequired : truthAuthorityAuthorizationGrantPreserved = true
  truthPreservedRequired : truthAuthorityPreserved = true
  closeoutOnlyRequired : truthAuthorityCloseoutReceiptOnly = true
  truthCycleClosedRequired : truthAuthorityCycleClosed = true
  blockerReleaseForbidden : blockerReleaseGranted = false

structure TruthAuthorityCloseoutReceiptBoundary where
  closeoutOwnedByPlanOS : Bool
  sourceTruthAuthorityReceiptPreserved : Bool
  selectedCandidateBoundToTruthAuthorityReceipt : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutPreserved : Bool
  cycleClosedPreserved : Bool
  truthAuthorityAuthorizationGrantPreserved : Bool
  truthAuthorityPreserved : Bool
  truthAuthorityCloseoutReceiptOnly : Bool
  truthAuthorityCycleClosed : Bool
  blockerReleaseGranted : Bool
  ownerRequired : closeoutOwnedByPlanOS = true
  sourcePreservedRequired : sourceTruthAuthorityReceiptPreserved = true
  selectedBoundRequired : selectedCandidateBoundToTruthAuthorityReceipt = true
  memoryOverwriteRequired : memoryOverwritePreserved = true
  memoryCloseoutRequired : memoryOverwriteCloseoutPreserved = true
  cyclePreservedRequired : cycleClosedPreserved = true
  grantPreservedRequired : truthAuthorityAuthorizationGrantPreserved = true
  truthPreservedRequired : truthAuthorityPreserved = true
  closeoutOnlyRequired : truthAuthorityCloseoutReceiptOnly = true
  truthCycleClosedRequired : truthAuthorityCycleClosed = true
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSTruthAuthorityCloseoutReceiptBridge where
  Digest : Type
  digestOf : TruthAuthorityCloseoutReceiptSurface → TruthAuthorityCloseoutReceiptBoundary → Nat → Digest
  surface : TruthAuthorityCloseoutReceiptSurface
  boundary : TruthAuthorityCloseoutReceiptBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  recorderNonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  recorderTruthForbidden : recorderNonAuthority.truthAuthority = false

namespace PlanOSTruthAuthorityCloseoutReceiptBridge

theorem source_receipt_records_truth_and_keeps_release_closed
    (b : PlanOSTruthAuthorityCloseoutReceiptBridge) :
    b.surface.sourceReceipt.truthAuthorityReceiptOnly = true ∧
      b.surface.sourceReceipt.truthAuthorityAuthorizationRequested = true ∧
      b.surface.sourceReceipt.truthAuthorityAuthorizationGranted = true ∧
      b.surface.sourceReceipt.truthAuthorityGranted = true ∧
      b.surface.sourceReceipt.blockerReleaseGranted = false ∧
      b.surface.sourceBoundary.truthAuthorityGranted = true ∧
      b.surface.sourceBoundary.blockerReleaseGranted = false := by
  exact ⟨b.surface.sourceReceipt.receiptOnlyRequired,
    b.surface.sourceReceipt.requestRequired,
    b.surface.sourceReceipt.authorizationRequired,
    b.surface.sourceReceipt.truthRequired,
    b.surface.sourceReceipt.blockerReleaseForbidden,
    b.surface.sourceBoundary.truthRequired,
    b.surface.sourceBoundary.blockerReleaseForbidden⟩

theorem closeout_binds_candidate_and_closes_truth_cycle_without_release
    (b : PlanOSTruthAuthorityCloseoutReceiptBridge) :
    b.surface.sourceReceiptBound = true ∧
      b.surface.selectedCandidateBoundToReceipt = true ∧
      b.surface.memoryOverwritePreserved = true ∧
      b.surface.memoryOverwriteCloseoutPreserved = true ∧
      b.surface.cycleClosedPreserved = true ∧
      b.surface.truthAuthorityAuthorizationGrantPreserved = true ∧
      b.surface.truthAuthorityPreserved = true ∧
      b.surface.truthAuthorityCloseoutReceiptOnly = true ∧
      b.surface.truthAuthorityCycleClosed = true ∧
      b.surface.blockerReleaseGranted = false ∧
      b.recorderNonAuthority.truthAuthority = false := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.memoryOverwriteRequired, b.surface.memoryCloseoutRequired,
    b.surface.cyclePreservedRequired, b.surface.grantPreservedRequired,
    b.surface.truthPreservedRequired, b.surface.closeoutOnlyRequired,
    b.surface.truthCycleClosedRequired, b.surface.blockerReleaseForbidden,
    b.recorderTruthForbidden⟩

theorem boundary_is_truth_authority_closeout_receipt_only
    (b : PlanOSTruthAuthorityCloseoutReceiptBridge) :
    b.boundary.closeoutOwnedByPlanOS = true ∧
      b.boundary.sourceTruthAuthorityReceiptPreserved = true ∧
      b.boundary.selectedCandidateBoundToTruthAuthorityReceipt = true ∧
      b.boundary.memoryOverwritePreserved = true ∧
      b.boundary.memoryOverwriteCloseoutPreserved = true ∧
      b.boundary.cycleClosedPreserved = true ∧
      b.boundary.truthAuthorityAuthorizationGrantPreserved = true ∧
      b.boundary.truthAuthorityPreserved = true ∧
      b.boundary.truthAuthorityCloseoutReceiptOnly = true ∧
      b.boundary.truthAuthorityCycleClosed = true ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.memoryOverwriteRequired,
    b.boundary.memoryCloseoutRequired, b.boundary.cyclePreservedRequired,
    b.boundary.grantPreservedRequired, b.boundary.truthPreservedRequired,
    b.boundary.closeoutOnlyRequired, b.boundary.truthCycleClosedRequired,
    b.boundary.blockerReleaseForbidden⟩

theorem history_appends_one_truth_authority_closeout_receipt
    (b : PlanOSTruthAuthorityCloseoutReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSTruthAuthorityCloseoutReceiptBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSTruthAuthorityCloseoutReceiptBridge

end PlanOS
end KUOS
