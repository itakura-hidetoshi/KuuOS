import Mathlib
import KUOS.WORLD.KuuOSAuthorizedMemoryApplicationV0_75

/-!
# KuuOS memory rollback v0.76

Rollback is a forward audit transaction. It restores the pre-commit kernel and
connection payload while advancing both production and rollback-ledger
revisions. The consumed approval remains consumed.
-/

namespace KUOS.WORLD.KuuOSMemoryRollbackV0_76

structure RollbackLedger where
  digest : String
  revision : ℕ
  consumedCommit : String → Prop

structure CommitEvidence where
  receiptDigest : String
  beforeStateDigest : String
  afterStateDigest : String
  beforeRevision : ℕ
  afterRevision : ℕ
  sourceKernelDigest : String
  selectedKernelDigest : String
  selectedConnectionDigest : String
  rollbackTargetDigest : String
  reviewReceiptDigest : String
  appliedAtEpoch : ℕ
  committed : Prop
  atomicCommit : Prop

structure RollbackState where
  stateDigest : String
  previousStateDigest : String
  revision : ℕ
  kernelDigest : String
  connectionDigest : String
  baseConnectionDigest : String
  approvalConsumed : String → Prop

structure RollbackRequest where
  expectedStateDigest : String
  expectedStateRevision : ℕ
  expectedLedgerDigest : String
  expectedLedgerRevision : ℕ
  commitReceiptDigest : String
  snapshotStateDigest : String
  snapshotKernelDigest : String
  snapshotConnectionDigest : String
  rollbackEpoch : ℕ

structure RollbackResult where
  currentState : RollbackState
  snapshotState : RollbackState
  restoredState : RollbackState
  beforeLedger : RollbackLedger
  afterLedger : RollbackLedger
  request : RollbackRequest
  commitEvidence : CommitEvidence
  committed : Prop
  atomicCommit : Prop
  stateWritePerformed : Prop
  liveApplicationPerformed : Prop
  permissionExpansionPerformed : Prop
  approvalReenabled : Prop

structure RollbackResult.Valid (result : RollbackResult) : Prop where
  commitWasCommitted : result.commitEvidence.committed
  commitWasAtomic : result.commitEvidence.atomicCommit
  commitBinding :
    result.request.commitReceiptDigest = result.commitEvidence.receiptDigest
  currentStateCAS :
    result.request.expectedStateDigest = result.currentState.stateDigest
  currentRevisionCAS :
    result.request.expectedStateRevision = result.currentState.revision
  ledgerDigestCAS :
    result.request.expectedLedgerDigest = result.beforeLedger.digest
  ledgerRevisionCAS :
    result.request.expectedLedgerRevision = result.beforeLedger.revision
  snapshotRequestBinding :
    result.request.snapshotStateDigest = result.snapshotState.stateDigest
  snapshotKernelRequestBinding :
    result.request.snapshotKernelDigest = result.snapshotState.kernelDigest
  snapshotConnectionRequestBinding :
    result.request.snapshotConnectionDigest =
      result.snapshotState.connectionDigest
  currentMatchesCommit :
    result.currentState.stateDigest = result.commitEvidence.afterStateDigest
  currentRevisionMatchesCommit :
    result.currentState.revision = result.commitEvidence.afterRevision
  snapshotMatchesCommit :
    result.snapshotState.stateDigest = result.commitEvidence.beforeStateDigest
  snapshotRevisionMatchesCommit :
    result.snapshotState.revision = result.commitEvidence.beforeRevision
  currentStateChain :
    result.currentState.previousStateDigest = result.snapshotState.stateDigest
  rollbackTargetBinding :
    result.snapshotState.kernelDigest = result.commitEvidence.rollbackTargetDigest
  sourceKernelBinding :
    result.snapshotState.kernelDigest = result.commitEvidence.sourceKernelDigest
  selectedKernelWasCurrent :
    result.currentState.kernelDigest = result.commitEvidence.selectedKernelDigest
  selectedConnectionWasCurrent :
    result.currentState.connectionDigest =
      result.commitEvidence.selectedConnectionDigest
  baseConnectionPreserved :
    result.snapshotState.baseConnectionDigest =
      result.currentState.baseConnectionDigest
  rollbackAfterCommit :
    result.commitEvidence.appliedAtEpoch ≤ result.request.rollbackEpoch
  rollbackUnused :
    ¬ result.beforeLedger.consumedCommit result.commitEvidence.receiptDigest
  rollbackConsumed :
    result.afterLedger.consumedCommit result.commitEvidence.receiptDigest
  ledgerRevisionSuccessor :
    result.afterLedger.revision = result.beforeLedger.revision + 1
  productionRevisionSuccessor :
    result.restoredState.revision = result.currentState.revision + 1
  restoredStateChain :
    result.restoredState.previousStateDigest = result.currentState.stateDigest
  kernelRestored :
    result.restoredState.kernelDigest = result.snapshotState.kernelDigest
  connectionRestored :
    result.restoredState.connectionDigest = result.snapshotState.connectionDigest
  restoredBaseConnection :
    result.restoredState.baseConnectionDigest =
      result.snapshotState.baseConnectionDigest
  currentApprovalConsumed :
    result.currentState.approvalConsumed result.commitEvidence.reviewReceiptDigest
  approvalStillConsumed :
    result.restoredState.approvalConsumed result.commitEvidence.reviewReceiptDigest
  committed : result.committed
  atomicCommit : result.atomicCommit
  stateWritePerformed : result.stateWritePerformed
  liveApplicationPerformed : result.liveApplicationPerformed
  noPermissionExpansion : ¬ result.permissionExpansionPerformed
  approvalNotReenabled : ¬ result.approvalReenabled

theorem valid_rollback_restores_payload
    (result : RollbackResult)
    (h : result.Valid) :
    result.restoredState.kernelDigest = result.snapshotState.kernelDigest ∧
      result.restoredState.connectionDigest =
        result.snapshotState.connectionDigest := by
  exact ⟨h.kernelRestored, h.connectionRestored⟩

theorem valid_rollback_advances_revisions
    (result : RollbackResult)
    (h : result.Valid) :
    result.restoredState.revision = result.currentState.revision + 1 ∧
      result.afterLedger.revision = result.beforeLedger.revision + 1 := by
  exact ⟨h.productionRevisionSuccessor, h.ledgerRevisionSuccessor⟩

theorem valid_rollback_preserves_state_chain
    (result : RollbackResult)
    (h : result.Valid) :
    result.currentState.previousStateDigest = result.snapshotState.stateDigest ∧
      result.restoredState.previousStateDigest =
        result.currentState.stateDigest := by
  exact ⟨h.currentStateChain, h.restoredStateChain⟩

theorem valid_rollback_is_single_use
    (result : RollbackResult)
    (h : result.Valid) :
    (¬ result.beforeLedger.consumedCommit result.commitEvidence.receiptDigest) ∧
      result.afterLedger.consumedCommit result.commitEvidence.receiptDigest := by
  exact ⟨h.rollbackUnused, h.rollbackConsumed⟩

theorem valid_rollback_does_not_reenable_approval
    (result : RollbackResult)
    (h : result.Valid) :
    result.currentState.approvalConsumed result.commitEvidence.reviewReceiptDigest ∧
      result.restoredState.approvalConsumed result.commitEvidence.reviewReceiptDigest ∧
      ¬ result.approvalReenabled := by
  exact ⟨h.currentApprovalConsumed, h.approvalStillConsumed,
    h.approvalNotReenabled⟩

theorem valid_rollback_is_atomic_compensation
    (result : RollbackResult)
    (h : result.Valid) :
    result.committed ∧ result.atomicCommit ∧
      result.stateWritePerformed ∧ result.liveApplicationPerformed ∧
      ¬ result.permissionExpansionPerformed := by
  exact ⟨h.committed, h.atomicCommit, h.stateWritePerformed,
    h.liveApplicationPerformed, h.noPermissionExpansion⟩

end KUOS.WORLD.KuuOSMemoryRollbackV0_76
