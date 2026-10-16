import Mathlib
import KUOS.ObserveOS.OpenClawSupervisorSerializationV0_5

namespace KUOS
namespace ObserveOS

structure OpenClawAuditCrossProcessSerializationBoundary where
  supervisorIntakeUsesDataDirLock : Bool
  manualIntakeUsesDataDirLock : Bool
  statusUsesDataDirLock : Bool
  ledgerCheckpointMutationInsideLock : Bool
  oneWriterWhileLockHeld : Bool
  supervisorRequired : supervisorIntakeUsesDataDirLock = true
  manualRequired : manualIntakeUsesDataDirLock = true
  statusRequired : statusUsesDataDirLock = true
  mutationRequired : ledgerCheckpointMutationInsideLock = true
  writerRequired : oneWriterWhileLockHeld = true

theorem openclaw_audit_public_entrypoints_share_cross_process_lock
    (boundary : OpenClawAuditCrossProcessSerializationBoundary) :
    boundary.supervisorIntakeUsesDataDirLock = true ∧
      boundary.manualIntakeUsesDataDirLock = true ∧
      boundary.statusUsesDataDirLock = true ∧
      boundary.ledgerCheckpointMutationInsideLock = true ∧
      boundary.oneWriterWhileLockHeld = true := by
  exact ⟨boundary.supervisorRequired, boundary.manualRequired,
    boundary.statusRequired, boundary.mutationRequired, boundary.writerRequired⟩


structure OpenClawAuditLockAuthorityBoundary where
  truthGranted : Bool
  verificationGranted : Bool
  effectPermissionGranted : Bool
  memoryOverwrite : Bool
  planCompletionGranted : Bool
  rollbackProofGranted : Bool
  truthForbidden : truthGranted = false
  verificationForbidden : verificationGranted = false
  effectPermissionForbidden : effectPermissionGranted = false
  overwriteForbidden : memoryOverwrite = false
  planCompletionForbidden : planCompletionGranted = false
  rollbackProofForbidden : rollbackProofGranted = false

def OpenClawAuditLockAuthorityBoundary.toObserveNonAuthority
    (boundary : OpenClawAuditLockAuthorityBoundary) : NonAuthorityBoundary where
  truthGranted := boundary.truthGranted
  verificationGranted := boundary.verificationGranted
  effectPermissionGranted := boundary.effectPermissionGranted
  memoryOverwrite := boundary.memoryOverwrite
  truthForbidden := boundary.truthForbidden
  verificationForbidden := boundary.verificationForbidden
  effectPermissionForbidden := boundary.effectPermissionForbidden
  overwriteForbidden := boundary.overwriteForbidden

theorem openclaw_audit_cross_process_lock_grants_no_new_authority
    (boundary : OpenClawAuditLockAuthorityBoundary) :
    boundary.truthGranted = false ∧
      boundary.verificationGranted = false ∧
      boundary.effectPermissionGranted = false ∧
      boundary.memoryOverwrite = false := by
  exact observe_lineage_envelope_grants_no_new_authority
    (OpenClawAuditLockAuthorityBoundary.toObserveNonAuthority boundary)

theorem openclaw_audit_cross_process_lock_does_not_complete_plan_or_prove_rollback
    (boundary : OpenClawAuditLockAuthorityBoundary) :
    boundary.planCompletionGranted = false ∧ boundary.rollbackProofGranted = false := by
  exact ⟨boundary.planCompletionForbidden, boundary.rollbackProofForbidden⟩

end ObserveOS
end KUOS
