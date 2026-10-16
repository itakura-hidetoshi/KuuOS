import KUOS.CodeAI.BoundedAutonomousGitLifecycleLoopOrchestrationV0_1

namespace KUOS.CodeAI.DurableGitLifecycleLoopCheckpointPersistenceV0_1

open KUOS.CodeAI.BoundedAutonomousGitLifecycleLoopOrchestrationV0_1

inductive PersistenceDisposition where
  | persisted
  | compareAndSwapConflict
  | failed
  | evidenceQuarantined
  deriving DecidableEq, Repr

structure DurableCheckpointPersistenceReceipt where
  sourceLoopReceiptDigest : String
  sourceLoopEvidenceDigest : String
  persistenceRequestDigest : String
  persistencePolicyDigest : String
  sourcePersistenceRegistryDigest : String
  nextPersistenceRegistryDigest : String
  sourceStoreStateDigest : String
  nextStoreStateDigest : String
  checkpointEnvelopeDigest : String
  persistenceEvidenceDigest : String
  checkpointId : String
  loopId : String
  lifecycleId : String
  repositoryFullName : String
  disposition : PersistenceDisposition
  sourceRegistryRevision : Nat
  nextRegistryRevision : Nat
  sourceAttemptCount : Nat
  nextAttemptCount : Nat
  sourceSuccessCount : Nat
  nextSuccessCount : Nat
  sourceStoreRevision : Nat
  nextStoreRevision : Nat
  routeReceiptRecorded : Bool
  sourceLoopReceiptVerified : Bool
  sourceLoopEvidenceVerified : Bool
  sourceBundleCorrespondenceConfirmed : Bool
  persistenceNonceConsumed : Bool
  persistenceRegistryAdvancedOnce : Bool
  adapterInvokedOnce : Bool
  atomicCompareAndSwapAttempted : Bool
  atomicCompareAndSwapSucceeded : Bool
  checkpointPersisted : Bool
  checkpointOverwritePerformed : Bool
  checkpointDeletePerformed : Bool
  networkAccessed : Bool
  secretMaterialRead : Bool
  gitEffectPerformed : Bool
  loopReexecuted : Bool
  resumeInputIssued : Bool
  automaticResumptionPerformed : Bool
  adapterAcknowledgementTreatedAsDurableTruth : Bool
  checkpointTreatedAsResumptionAuthority : Bool
  generalGitAuthorityGranted : Bool
  generalSuccessorStageAuthorityGranted : Bool
  activeNow : Bool
  registryRevisionStep : nextRegistryRevision = sourceRegistryRevision + 1
  attemptCountStep : nextAttemptCount = sourceAttemptCount + 1
  committedStoreStep :
    disposition = .persisted → nextStoreRevision = sourceStoreRevision + 1
  committedSuccessStep :
    disposition = .persisted → nextSuccessCount = sourceSuccessCount + 1
  nonCommittedStoreStable :
    disposition ≠ .persisted → nextStoreRevision = sourceStoreRevision
  nonCommittedSuccessStable :
    disposition ≠ .persisted → nextSuccessCount = sourceSuccessCount

structure DurableCheckpointPersistenceReceiptValid
    (receipt : DurableCheckpointPersistenceReceipt) : Prop where
  routeRecorded : receipt.routeReceiptRecorded = true
  loopReceiptVerified : receipt.sourceLoopReceiptVerified = true
  loopEvidenceVerified : receipt.sourceLoopEvidenceVerified = true
  correspondenceConfirmed : receipt.sourceBundleCorrespondenceConfirmed = true
  nonceConsumed : receipt.persistenceNonceConsumed = true
  registryAdvanced : receipt.persistenceRegistryAdvancedOnce = true
  adapterInvoked : receipt.adapterInvokedOnce = true
  noOverwrite : receipt.checkpointOverwritePerformed = false
  noDelete : receipt.checkpointDeletePerformed = false
  noNetwork : receipt.networkAccessed = false
  noSecretRead : receipt.secretMaterialRead = false
  noGitEffect : receipt.gitEffectPerformed = false
  noLoopExecution : receipt.loopReexecuted = false
  noResumeInput : receipt.resumeInputIssued = false
  noAutomaticResumption : receipt.automaticResumptionPerformed = false
  adapterAckNotTruth : receipt.adapterAcknowledgementTreatedAsDurableTruth = false
  checkpointNotResumeAuthority : receipt.checkpointTreatedAsResumptionAuthority = false
  noGeneralGitAuthority : receipt.generalGitAuthorityGranted = false
  noGeneralSuccessor : receipt.generalSuccessorStageAuthorityGranted = false
  inactive : receipt.activeNow = false

structure DurableCheckpointPersistenceEnvelope where
  loopReceipt : BoundedGitLifecycleLoopReceipt
  loopReceiptValid : BoundedGitLifecycleLoopReceiptValid loopReceipt
  receipt : DurableCheckpointPersistenceReceipt
  receiptValid : DurableCheckpointPersistenceReceiptValid receipt
  loopBound : receipt.loopId = loopReceipt.loopId
  lifecycleBound : receipt.lifecycleId = loopReceipt.lifecycleId
  repositoryBound : receipt.repositoryFullName = loopReceipt.repositoryFullName

 theorem persistence_registry_advances_exactly_once
    (receipt : DurableCheckpointPersistenceReceipt) :
    receipt.nextRegistryRevision = receipt.sourceRegistryRevision + 1 ∧
      receipt.nextAttemptCount = receipt.sourceAttemptCount + 1 := by
  exact ⟨receipt.registryRevisionStep, receipt.attemptCountStep⟩

 theorem committed_checkpoint_advances_store_and_success_count
    (receipt : DurableCheckpointPersistenceReceipt)
    (committed : receipt.disposition = .persisted) :
    receipt.nextStoreRevision = receipt.sourceStoreRevision + 1 ∧
      receipt.nextSuccessCount = receipt.sourceSuccessCount + 1 := by
  exact ⟨receipt.committedStoreStep committed,
    receipt.committedSuccessStep committed⟩

 theorem non_committed_checkpoint_preserves_store_and_success_count
    (receipt : DurableCheckpointPersistenceReceipt)
    (notCommitted : receipt.disposition ≠ .persisted) :
    receipt.nextStoreRevision = receipt.sourceStoreRevision ∧
      receipt.nextSuccessCount = receipt.sourceSuccessCount := by
  exact ⟨receipt.nonCommittedStoreStable notCommitted,
    receipt.nonCommittedSuccessStable notCommitted⟩

 theorem persistence_performs_no_external_or_destructive_effects
    (receipt : DurableCheckpointPersistenceReceipt)
    (valid : DurableCheckpointPersistenceReceiptValid receipt) :
    receipt.checkpointOverwritePerformed = false ∧
      receipt.checkpointDeletePerformed = false ∧
      receipt.networkAccessed = false ∧
      receipt.secretMaterialRead = false ∧
      receipt.gitEffectPerformed = false ∧
      receipt.loopReexecuted = false := by
  exact ⟨valid.noOverwrite, valid.noDelete, valid.noNetwork,
    valid.noSecretRead, valid.noGitEffect, valid.noLoopExecution⟩

 theorem persistence_grants_no_resumption_or_general_authority
    (receipt : DurableCheckpointPersistenceReceipt)
    (valid : DurableCheckpointPersistenceReceiptValid receipt) :
    receipt.resumeInputIssued = false ∧
      receipt.automaticResumptionPerformed = false ∧
      receipt.checkpointTreatedAsResumptionAuthority = false ∧
      receipt.generalGitAuthorityGranted = false ∧
      receipt.generalSuccessorStageAuthorityGranted = false ∧
      receipt.activeNow = false := by
  exact ⟨valid.noResumeInput, valid.noAutomaticResumption,
    valid.checkpointNotResumeAuthority, valid.noGeneralGitAuthority,
    valid.noGeneralSuccessor, valid.inactive⟩

 theorem adapter_acknowledgement_is_not_durable_truth
    (receipt : DurableCheckpointPersistenceReceipt)
    (valid : DurableCheckpointPersistenceReceiptValid receipt) :
    receipt.adapterAcknowledgementTreatedAsDurableTruth = false := by
  exact valid.adapterAckNotTruth

 theorem persistence_is_bound_to_source_loop
    (envelope : DurableCheckpointPersistenceEnvelope) :
    envelope.receipt.loopId = envelope.loopReceipt.loopId ∧
      envelope.receipt.lifecycleId = envelope.loopReceipt.lifecycleId ∧
      envelope.receipt.repositoryFullName = envelope.loopReceipt.repositoryFullName := by
  exact ⟨envelope.loopBound, envelope.lifecycleBound, envelope.repositoryBound⟩

end KUOS.CodeAI.DurableGitLifecycleLoopCheckpointPersistenceV0_1
