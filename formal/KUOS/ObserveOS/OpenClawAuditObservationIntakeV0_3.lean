import Mathlib
import KUOS.ObserveOS.ReplanLineageObservationEnvelopeV0_2

namespace KUOS
namespace ObserveOS

structure OpenClawAuditSourceBoundary where
  metadataOnly : Bool
  bestEffortSource : Bool
  absenceProvesNonOccurrence : Bool
  metadataRequired : metadataOnly = true
  bestEffortRequired : bestEffortSource = true
  absenceProofForbidden : absenceProvesNonOccurrence = false

theorem openclaw_audit_source_is_metadata_only_best_effort
    (boundary : OpenClawAuditSourceBoundary) :
    boundary.metadataOnly = true ∧
      boundary.bestEffortSource = true ∧
      boundary.absenceProvesNonOccurrence = false := by
  exact ⟨boundary.metadataRequired, boundary.bestEffortRequired,
    boundary.absenceProofForbidden⟩


structure OpenClawAuditIntakeBoundary where
  candidateRecorded : Bool
  observeCommitPerformed : Bool
  verificationCreated : Bool
  verificationRequired : Bool
  memoryOverwrite : Bool
  candidateRequired : candidateRecorded = true
  observeCommitForbidden : observeCommitPerformed = false
  verificationCreationForbidden : verificationCreated = false
  verificationDebtRequired : verificationRequired = true
  memoryOverwriteForbidden : memoryOverwrite = false

theorem openclaw_audit_candidate_is_not_observe_commit
    (boundary : OpenClawAuditIntakeBoundary) :
    boundary.candidateRecorded = true ∧
      boundary.observeCommitPerformed = false ∧
      boundary.verificationCreated = false ∧
      boundary.verificationRequired = true := by
  exact ⟨boundary.candidateRequired, boundary.observeCommitForbidden,
    boundary.verificationCreationForbidden, boundary.verificationDebtRequired⟩

theorem openclaw_audit_intake_does_not_overwrite_memory
    (boundary : OpenClawAuditIntakeBoundary) :
    boundary.memoryOverwrite = false := by
  exact boundary.memoryOverwriteForbidden


structure OpenClawHostStatusAuthorityBoundary where
  truthGranted : Bool
  verificationGranted : Bool
  effectPermissionGranted : Bool
  memoryOverwrite : Bool
  planCompletionGranted : Bool
  rollbackProofGranted : Bool
  truthForbidden : truthGranted = false
  verificationForbidden : verificationGranted = false
  effectPermissionForbidden : effectPermissionGranted = false
  memoryOverwriteForbidden : memoryOverwrite = false
  planCompletionForbidden : planCompletionGranted = false
  rollbackProofForbidden : rollbackProofGranted = false

def OpenClawHostStatusAuthorityBoundary.toObserveNonAuthority
    (boundary : OpenClawHostStatusAuthorityBoundary) : NonAuthorityBoundary where
  truthGranted := boundary.truthGranted
  verificationGranted := boundary.verificationGranted
  effectPermissionGranted := boundary.effectPermissionGranted
  memoryOverwrite := boundary.memoryOverwrite
  truthForbidden := boundary.truthForbidden
  verificationForbidden := boundary.verificationForbidden
  effectPermissionForbidden := boundary.effectPermissionForbidden
  overwriteForbidden := boundary.memoryOverwriteForbidden

theorem openclaw_host_status_grants_no_observe_authority
    (boundary : OpenClawHostStatusAuthorityBoundary) :
    boundary.truthGranted = false ∧
      boundary.verificationGranted = false ∧
      boundary.effectPermissionGranted = false ∧
      boundary.memoryOverwrite = false := by
  exact observe_lineage_envelope_grants_no_new_authority
    (OpenClawHostStatusAuthorityBoundary.toObserveNonAuthority boundary)

theorem openclaw_host_status_does_not_complete_plan_or_prove_rollback
    (boundary : OpenClawHostStatusAuthorityBoundary) :
    boundary.planCompletionGranted = false ∧
      boundary.rollbackProofGranted = false := by
  exact ⟨boundary.planCompletionForbidden, boundary.rollbackProofForbidden⟩


structure OpenClawAuditCheckpointBoundary where
  partialWindow : Bool
  checkpointAdvanced : Bool
  resumeCursorStored : Bool
  partialImpliesNoAdvance : partialWindow = true → checkpointAdvanced = false
  partialImpliesResume : partialWindow = true → resumeCursorStored = true

theorem partial_openclaw_audit_window_preserves_old_checkpoint
    (boundary : OpenClawAuditCheckpointBoundary)
    (partial : boundary.partialWindow = true) :
    boundary.checkpointAdvanced = false ∧
      boundary.resumeCursorStored = true := by
  exact ⟨boundary.partialImpliesNoAdvance partial, boundary.partialImpliesResume partial⟩

end ObserveOS
end KUOS
