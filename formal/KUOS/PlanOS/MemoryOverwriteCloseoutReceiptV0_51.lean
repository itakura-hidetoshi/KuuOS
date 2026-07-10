import Mathlib
import KUOS.PlanOS.MemoryOverwriteReceiptV0_50

namespace KUOS
namespace PlanOS

structure MemoryOverwriteCloseoutReceiptSurface where
  sourceReceipt : MemoryOverwriteReceiptSurface
  sourceBoundary : MemoryOverwriteReceiptBoundary
  sourceReceiptBound : Bool
  selectedCandidateBoundToReceipt : Bool
  memoryOverwritePreserved : Bool
  closeoutReceiptOnly : Bool
  cycleClosed : Bool
  truthAuthorityGranted : Bool
  blockerReleaseGranted : Bool
  sourceRequired : sourceReceiptBound = true
  selectedBoundRequired : selectedCandidateBoundToReceipt = true
  overwriteRequired : memoryOverwritePreserved = true
  closeoutOnlyRequired : closeoutReceiptOnly = true
  cycleClosedRequired : cycleClosed = true
  truthForbidden : truthAuthorityGranted = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure MemoryOverwriteCloseoutReceiptBoundary where
  closeoutOwnedByPlanOS : Bool
  sourceMemoryOverwriteReceiptPreserved : Bool
  selectedCandidateBoundToMemoryOverwriteReceipt : Bool
  memoryOverwritePreserved : Bool
  memoryOverwriteCloseoutReceiptOnly : Bool
  cycleClosed : Bool
  blockerReleaseGranted : Bool
  ownerRequired : closeoutOwnedByPlanOS = true
  sourcePreservedRequired : sourceMemoryOverwriteReceiptPreserved = true
  selectedBoundRequired : selectedCandidateBoundToMemoryOverwriteReceipt = true
  overwriteRequired : memoryOverwritePreserved = true
  closeoutOnlyRequired : memoryOverwriteCloseoutReceiptOnly = true
  cycleClosedRequired : cycleClosed = true
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSMemoryOverwriteCloseoutReceiptBridge where
  Digest : Type
  digestOf : MemoryOverwriteCloseoutReceiptSurface → MemoryOverwriteCloseoutReceiptBoundary → Nat → Digest
  surface : MemoryOverwriteCloseoutReceiptSurface
  boundary : MemoryOverwriteCloseoutReceiptBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  nonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  truthForbidden : nonAuthority.truthAuthority = false

namespace PlanOSMemoryOverwriteCloseoutReceiptBridge

theorem source_receipt_records_memory_overwrite_and_keeps_truth_and_release_closed
    (b : PlanOSMemoryOverwriteCloseoutReceiptBridge) :
    b.surface.sourceReceipt.memoryOverwriteReceiptOnly = true ∧
      b.surface.sourceReceipt.memoryOverwriteGranted = true ∧
      b.surface.sourceReceipt.truthAuthorityGranted = false ∧
      b.surface.sourceReceipt.blockerReleaseGranted = false ∧
      b.surface.sourceBoundary.memoryOverwrite = true ∧
      b.surface.sourceBoundary.blockerReleaseGranted = false := by
  exact ⟨b.surface.sourceReceipt.receiptOnlyRequired,
    b.surface.sourceReceipt.overwriteRequired,
    b.surface.sourceReceipt.truthForbidden,
    b.surface.sourceReceipt.blockerReleaseForbidden,
    b.surface.sourceBoundary.overwriteRequired,
    b.surface.sourceBoundary.blockerReleaseForbidden⟩

theorem closeout_binds_candidate_and_closes_memory_cycle_without_new_authority
    (b : PlanOSMemoryOverwriteCloseoutReceiptBridge) :
    b.surface.sourceReceiptBound = true ∧
      b.surface.selectedCandidateBoundToReceipt = true ∧
      b.surface.memoryOverwritePreserved = true ∧
      b.surface.closeoutReceiptOnly = true ∧
      b.surface.cycleClosed = true ∧
      b.surface.truthAuthorityGranted = false ∧
      b.surface.blockerReleaseGranted = false ∧
      b.nonAuthority.truthAuthority = false := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.overwriteRequired, b.surface.closeoutOnlyRequired,
    b.surface.cycleClosedRequired, b.surface.truthForbidden,
    b.surface.blockerReleaseForbidden, b.truthForbidden⟩

theorem boundary_is_memory_overwrite_closeout_receipt_only
    (b : PlanOSMemoryOverwriteCloseoutReceiptBridge) :
    b.boundary.closeoutOwnedByPlanOS = true ∧
      b.boundary.sourceMemoryOverwriteReceiptPreserved = true ∧
      b.boundary.selectedCandidateBoundToMemoryOverwriteReceipt = true ∧
      b.boundary.memoryOverwritePreserved = true ∧
      b.boundary.memoryOverwriteCloseoutReceiptOnly = true ∧
      b.boundary.cycleClosed = true ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.overwriteRequired,
    b.boundary.closeoutOnlyRequired, b.boundary.cycleClosedRequired,
    b.boundary.blockerReleaseForbidden⟩

theorem history_appends_one_closeout_receipt
    (b : PlanOSMemoryOverwriteCloseoutReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSMemoryOverwriteCloseoutReceiptBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSMemoryOverwriteCloseoutReceiptBridge

end PlanOS
end KUOS
