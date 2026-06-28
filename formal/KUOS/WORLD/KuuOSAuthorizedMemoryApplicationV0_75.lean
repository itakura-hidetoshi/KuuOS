import Mathlib
import KUOS.WORLD.KuuOSMemorySelectionReviewV0_74

/-!
# KuuOS authorized memory application v0.75

A valid v0.74 approval is consumed once by a compare-and-swap application.
The production revision advances exactly once, the selected memory kernel is
installed atomically, and the rollback target remains the pre-commit kernel.
-/

namespace KUOS.WORLD.KuuOSAuthorizedMemoryApplicationV0_75

structure ProductionState where
  stateDigest : String
  revision : ℕ
  baseConnectionDigest : String
  currentKernelDigest : String
  currentConnectionDigest : String
  consumedApproval : String → Prop

structure Approval where
  receiptDigest : String
  approved : Prop
  applicationAuthority : Prop
  baseConnectionDigest : String
  sourceKernelDigest : String
  selectedKernelDigest : String
  selectedConnectionDigest : String
  rollbackTargetDigest : String
  validFromEpoch : ℕ
  validUntilEpoch : ℕ
  decidedAtEpoch : ℕ

structure ApplicationRequest where
  expectedStateDigest : String
  expectedRevision : ℕ
  approvalDigest : String
  sourceKernelDigest : String
  selectedKernelDigest : String
  selectedConnectionDigest : String
  rollbackTargetDigest : String
  applyEpoch : ℕ

structure ApplicationResult where
  beforeState : ProductionState
  afterState : ProductionState
  request : ApplicationRequest
  approval : Approval
  committed : Prop
  atomicCommit : Prop
  stateWritePerformed : Prop
  liveApplicationPerformed : Prop
  permissionExpansionPerformed : Prop
  rollbackTargetReplaced : Prop

structure ApplicationResult.Valid (result : ApplicationResult) : Prop where
  approvalApproved : result.approval.approved
  approvalAuthority : result.approval.applicationAuthority
  approvalBinding : result.request.approvalDigest = result.approval.receiptDigest
  stateDigestCAS :
    result.request.expectedStateDigest = result.beforeState.stateDigest
  revisionCAS : result.request.expectedRevision = result.beforeState.revision
  baseConnectionBinding :
    result.approval.baseConnectionDigest =
      result.beforeState.baseConnectionDigest
  sourceKernelCAS :
    result.request.sourceKernelDigest = result.beforeState.currentKernelDigest
  approvalSourceBinding :
    result.approval.sourceKernelDigest = result.beforeState.currentKernelDigest
  selectedKernelBinding :
    result.request.selectedKernelDigest = result.approval.selectedKernelDigest
  selectedConnectionBinding :
    result.request.selectedConnectionDigest =
      result.approval.selectedConnectionDigest
  rollbackRequestBinding :
    result.request.rollbackTargetDigest = result.beforeState.currentKernelDigest
  rollbackApprovalBinding :
    result.approval.rollbackTargetDigest = result.beforeState.currentKernelDigest
  withinValidityWindow :
    result.approval.validFromEpoch ≤ result.request.applyEpoch ∧
      result.request.applyEpoch ≤ result.approval.validUntilEpoch
  afterDecision : result.approval.decidedAtEpoch ≤ result.request.applyEpoch
  authorityUnused :
    ¬ result.beforeState.consumedApproval result.approval.receiptDigest
  revisionSuccessor :
    result.afterState.revision = result.beforeState.revision + 1
  baseConnectionPreserved :
    result.afterState.baseConnectionDigest =
      result.beforeState.baseConnectionDigest
  selectedKernelInstalled :
    result.afterState.currentKernelDigest = result.approval.selectedKernelDigest
  selectedConnectionInstalled :
    result.afterState.currentConnectionDigest =
      result.approval.selectedConnectionDigest
  authorityConsumed :
    result.afterState.consumedApproval result.approval.receiptDigest
  committed : result.committed
  atomicCommit : result.atomicCommit
  stateWritePerformed : result.stateWritePerformed
  liveApplicationPerformed : result.liveApplicationPerformed
  noPermissionExpansion : ¬ result.permissionExpansionPerformed
  rollbackTargetPreserved : ¬ result.rollbackTargetReplaced

theorem valid_application_advances_revision_once
    (result : ApplicationResult)
    (h : result.Valid) :
    result.afterState.revision = result.beforeState.revision + 1 := by
  exact h.revisionSuccessor

theorem valid_application_installs_exact_selection
    (result : ApplicationResult)
    (h : result.Valid) :
    result.afterState.currentKernelDigest = result.approval.selectedKernelDigest ∧
      result.afterState.currentConnectionDigest =
        result.approval.selectedConnectionDigest := by
  exact ⟨h.selectedKernelInstalled, h.selectedConnectionInstalled⟩

theorem valid_application_preserves_base_connection
    (result : ApplicationResult)
    (h : result.Valid) :
    result.approval.baseConnectionDigest =
        result.beforeState.baseConnectionDigest ∧
      result.afterState.baseConnectionDigest =
        result.beforeState.baseConnectionDigest := by
  exact ⟨h.baseConnectionBinding, h.baseConnectionPreserved⟩

theorem valid_application_consumes_authority_once
    (result : ApplicationResult)
    (h : result.Valid) :
    (¬ result.beforeState.consumedApproval result.approval.receiptDigest) ∧
      result.afterState.consumedApproval result.approval.receiptDigest := by
  exact ⟨h.authorityUnused, h.authorityConsumed⟩

theorem valid_application_preserves_rollback_target
    (result : ApplicationResult)
    (h : result.Valid) :
    result.request.rollbackTargetDigest = result.beforeState.currentKernelDigest ∧
      result.approval.rollbackTargetDigest =
        result.beforeState.currentKernelDigest := by
  exact ⟨h.rollbackRequestBinding, h.rollbackApprovalBinding⟩

theorem valid_application_is_atomic_authorized_write
    (result : ApplicationResult)
    (h : result.Valid) :
    result.committed ∧ result.atomicCommit ∧
      result.stateWritePerformed ∧ result.liveApplicationPerformed ∧
      ¬ result.permissionExpansionPerformed ∧
      ¬ result.rollbackTargetReplaced := by
  exact ⟨h.committed, h.atomicCommit, h.stateWritePerformed,
    h.liveApplicationPerformed, h.noPermissionExpansion,
    h.rollbackTargetPreserved⟩

end KUOS.WORLD.KuuOSAuthorizedMemoryApplicationV0_75
