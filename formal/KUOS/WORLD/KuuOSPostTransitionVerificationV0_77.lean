import Mathlib
import KUOS.WORLD.KuuOSMemoryRollbackV0_76

/-!
# KuuOS post-transition verification v0.77

This layer verifies observed production state after a v0.75 commit or v0.76
rollback. Verification is record-only and performs no state mutation.
-/

namespace KUOS.WORLD.KuuOSPostTransitionVerificationV0_77

inductive TransitionKind where
  | commit
  | rollback
  deriving DecidableEq

structure VerificationRecord where
  transitionKind : TransitionKind
  exactStateBinding : Prop
  exactPayloadBinding : Prop
  revisionSuccessor : Prop
  stateChainPreserved : Prop
  authorityConsumptionPreserved : Prop
  ledgerBindingPreserved : Prop
  recordOnly : Prop
  writesDisabled : Prop
  liveApplicationDisabled : Prop
  permissionExpansionDisabled : Prop

structure VerificationRecord.Valid (record : VerificationRecord) : Prop where
  exactStateBinding : record.exactStateBinding
  exactPayloadBinding : record.exactPayloadBinding
  revisionSuccessor : record.revisionSuccessor
  stateChainPreserved : record.stateChainPreserved
  authorityConsumptionPreserved : record.authorityConsumptionPreserved
  ledgerBindingPreserved : record.ledgerBindingPreserved
  recordOnly : record.recordOnly
  writesDisabled : record.writesDisabled
  liveApplicationDisabled : record.liveApplicationDisabled
  permissionExpansionDisabled : record.permissionExpansionDisabled

structure CommitObservation where
  receiptAfterStateDigest : String
  observedStateDigest : String
  receiptAfterRevision : ℕ
  observedRevision : ℕ
  receiptBeforeRevision : ℕ
  receiptSelectedKernelDigest : String
  observedKernelDigest : String
  receiptSelectedConnectionDigest : String
  observedConnectionDigest : String
  receiptBeforeStateDigest : String
  observedPreviousStateDigest : String
  authorityConsumed : Prop

structure CommitObservation.Valid (observation : CommitObservation) : Prop where
  stateDigest :
    observation.receiptAfterStateDigest = observation.observedStateDigest
  stateRevision :
    observation.receiptAfterRevision = observation.observedRevision
  revisionSuccessor :
    observation.receiptAfterRevision = observation.receiptBeforeRevision + 1
  kernelDigest :
    observation.receiptSelectedKernelDigest = observation.observedKernelDigest
  connectionDigest :
    observation.receiptSelectedConnectionDigest =
      observation.observedConnectionDigest
  stateChain :
    observation.observedPreviousStateDigest = observation.receiptBeforeStateDigest
  authorityConsumed : observation.authorityConsumed

structure RollbackObservation where
  rollbackAfterStateDigest : String
  observedStateDigest : String
  rollbackAfterRevision : ℕ
  observedRevision : ℕ
  rollbackBeforeRevision : ℕ
  rollbackRestoredKernelDigest : String
  observedKernelDigest : String
  rollbackRestoredConnectionDigest : String
  observedConnectionDigest : String
  rollbackBeforeStateDigest : String
  commitAfterStateDigest : String
  commitAfterRevision : ℕ
  observedPreviousStateDigest : String
  rollbackAfterLedgerDigest : String
  observedLedgerDigest : String
  rollbackAfterLedgerRevision : ℕ
  observedLedgerRevision : ℕ
  rollbackBeforeLedgerRevision : ℕ
  authorityConsumed : Prop
  commitRecordedInLedger : Prop

structure RollbackObservation.Valid (observation : RollbackObservation) : Prop where
  stateDigest :
    observation.rollbackAfterStateDigest = observation.observedStateDigest
  stateRevision :
    observation.rollbackAfterRevision = observation.observedRevision
  revisionSuccessor :
    observation.rollbackAfterRevision = observation.rollbackBeforeRevision + 1
  kernelDigest :
    observation.rollbackRestoredKernelDigest = observation.observedKernelDigest
  connectionDigest :
    observation.rollbackRestoredConnectionDigest =
      observation.observedConnectionDigest
  stateChain :
    observation.observedPreviousStateDigest = observation.rollbackBeforeStateDigest
  commitRollbackChain :
    observation.rollbackBeforeStateDigest = observation.commitAfterStateDigest
  commitRollbackRevision :
    observation.rollbackBeforeRevision = observation.commitAfterRevision
  ledgerDigest :
    observation.rollbackAfterLedgerDigest = observation.observedLedgerDigest
  ledgerRevision :
    observation.rollbackAfterLedgerRevision = observation.observedLedgerRevision
  ledgerRevisionSuccessor :
    observation.rollbackAfterLedgerRevision =
      observation.rollbackBeforeLedgerRevision + 1
  authorityConsumed : observation.authorityConsumed
  commitRecordedInLedger : observation.commitRecordedInLedger

theorem valid_commit_observation_binds_state_and_payload
    (observation : CommitObservation)
    (h : observation.Valid) :
    observation.receiptAfterStateDigest = observation.observedStateDigest ∧
      observation.receiptSelectedKernelDigest = observation.observedKernelDigest ∧
      observation.receiptSelectedConnectionDigest =
        observation.observedConnectionDigest := by
  exact ⟨h.stateDigest, h.kernelDigest, h.connectionDigest⟩

theorem valid_rollback_observation_binds_state_and_ledger
    (observation : RollbackObservation)
    (h : observation.Valid) :
    observation.rollbackAfterStateDigest = observation.observedStateDigest ∧
      observation.rollbackAfterLedgerDigest = observation.observedLedgerDigest ∧
      observation.rollbackAfterLedgerRevision = observation.observedLedgerRevision := by
  exact ⟨h.stateDigest, h.ledgerDigest, h.ledgerRevision⟩

theorem valid_rollback_observation_preserves_transition_chain
    (observation : RollbackObservation)
    (h : observation.Valid) :
    observation.observedPreviousStateDigest = observation.rollbackBeforeStateDigest ∧
      observation.rollbackBeforeStateDigest = observation.commitAfterStateDigest ∧
      observation.rollbackBeforeRevision = observation.commitAfterRevision := by
  exact ⟨h.stateChain, h.commitRollbackChain, h.commitRollbackRevision⟩

theorem valid_verification_is_record_only
    (record : VerificationRecord)
    (h : record.Valid) :
    record.recordOnly ∧ record.writesDisabled ∧
      record.liveApplicationDisabled ∧
      record.permissionExpansionDisabled := by
  exact ⟨h.recordOnly, h.writesDisabled,
    h.liveApplicationDisabled, h.permissionExpansionDisabled⟩

end KUOS.WORLD.KuuOSPostTransitionVerificationV0_77
