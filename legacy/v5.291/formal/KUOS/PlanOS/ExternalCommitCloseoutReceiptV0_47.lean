import Mathlib
import KUOS.PlanOS.ExternalCommitReceiptV0_46

namespace KUOS
namespace PlanOS

structure ExternalCommitCloseoutReceiptSurface where
  sourceReceipt : ExternalCommitReceiptSurface
  sourceBoundary : ExternalCommitReceiptBoundary
  sourceReceiptBound : Bool
  selectedCandidateBoundToReceipt : Bool
  externalCommitPreserved : Bool
  closeoutReceiptOnly : Bool
  cycleClosed : Bool
  truthAuthorityGranted : Bool
  memoryOverwriteGranted : Bool
  blockerReleaseGranted : Bool
  sourceRequired : sourceReceiptBound = true
  selectedBoundRequired : selectedCandidateBoundToReceipt = true
  externalCommitRequired : externalCommitPreserved = true
  closeoutOnlyRequired : closeoutReceiptOnly = true
  cycleClosedRequired : cycleClosed = true
  truthForbidden : truthAuthorityGranted = false
  overwriteForbidden : memoryOverwriteGranted = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure ExternalCommitCloseoutReceiptBoundary where
  closeoutOwnedByPlanOS : Bool
  sourceExternalCommitReceiptPreserved : Bool
  selectedCandidateBoundToExternalCommitReceipt : Bool
  externalCommitPreserved : Bool
  externalCommitCloseoutReceiptOnly : Bool
  cycleClosed : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  ownerRequired : closeoutOwnedByPlanOS = true
  sourcePreservedRequired : sourceExternalCommitReceiptPreserved = true
  selectedBoundRequired : selectedCandidateBoundToExternalCommitReceipt = true
  externalCommitRequired : externalCommitPreserved = true
  closeoutOnlyRequired : externalCommitCloseoutReceiptOnly = true
  cycleClosedRequired : cycleClosed = true
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSExternalCommitCloseoutReceiptBridge where
  Digest : Type
  digestOf : ExternalCommitCloseoutReceiptSurface → ExternalCommitCloseoutReceiptBoundary → Nat → Digest
  surface : ExternalCommitCloseoutReceiptSurface
  boundary : ExternalCommitCloseoutReceiptBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  nonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  truthForbidden : nonAuthority.truthAuthority = false
  overwriteForbidden : nonAuthority.memoryOverwrite = false

namespace PlanOSExternalCommitCloseoutReceiptBridge

theorem source_receipt_records_external_commit_and_keeps_authority_closed
    (b : PlanOSExternalCommitCloseoutReceiptBridge) :
    b.surface.sourceReceipt.externalCommitReceiptOnly = true ∧
      b.surface.sourceReceipt.externalCommitGranted = true ∧
      b.surface.sourceReceipt.truthAuthorityGranted = false ∧
      b.surface.sourceReceipt.memoryOverwriteGranted = false ∧
      b.surface.sourceBoundary.externalCommitGranted = true ∧
      b.surface.sourceBoundary.memoryOverwrite = false ∧
      b.surface.sourceBoundary.blockerReleaseGranted = false := by
  exact ⟨b.surface.sourceReceipt.externalCommitReceiptOnlyRequired,
    b.surface.sourceReceipt.externalCommitRequired,
    b.surface.sourceReceipt.truthForbidden,
    b.surface.sourceReceipt.memoryOverwriteForbidden,
    b.surface.sourceBoundary.externalCommitRequired,
    b.surface.sourceBoundary.overwriteForbidden,
    b.surface.sourceBoundary.blockerReleaseForbidden⟩

theorem closeout_binds_candidate_and_closes_cycle_without_new_authority
    (b : PlanOSExternalCommitCloseoutReceiptBridge) :
    b.surface.sourceReceiptBound = true ∧
      b.surface.selectedCandidateBoundToReceipt = true ∧
      b.surface.externalCommitPreserved = true ∧
      b.surface.closeoutReceiptOnly = true ∧
      b.surface.cycleClosed = true ∧
      b.surface.truthAuthorityGranted = false ∧
      b.surface.memoryOverwriteGranted = false ∧
      b.surface.blockerReleaseGranted = false ∧
      b.nonAuthority.truthAuthority = false ∧
      b.nonAuthority.memoryOverwrite = false := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.externalCommitRequired, b.surface.closeoutOnlyRequired,
    b.surface.cycleClosedRequired, b.surface.truthForbidden,
    b.surface.overwriteForbidden, b.surface.blockerReleaseForbidden,
    b.truthForbidden, b.overwriteForbidden⟩

theorem boundary_is_external_commit_closeout_receipt_only
    (b : PlanOSExternalCommitCloseoutReceiptBridge) :
    b.boundary.closeoutOwnedByPlanOS = true ∧
      b.boundary.sourceExternalCommitReceiptPreserved = true ∧
      b.boundary.selectedCandidateBoundToExternalCommitReceipt = true ∧
      b.boundary.externalCommitPreserved = true ∧
      b.boundary.externalCommitCloseoutReceiptOnly = true ∧
      b.boundary.cycleClosed = true ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.ownerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.externalCommitRequired,
    b.boundary.closeoutOnlyRequired, b.boundary.cycleClosedRequired,
    b.boundary.overwriteForbidden, b.boundary.blockerReleaseForbidden⟩

theorem history_appends_one_closeout_receipt
    (b : PlanOSExternalCommitCloseoutReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSExternalCommitCloseoutReceiptBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSExternalCommitCloseoutReceiptBridge

end PlanOS
end KUOS
