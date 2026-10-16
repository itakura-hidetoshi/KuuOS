import KUOS.CodeAI.DurableGitLifecycleLoopCheckpointPersistenceV0_1

namespace KUOS.CodeAI.DurableGitLifecycleLoopResumptionAdmissionV0_1

open KUOS.CodeAI.DurableGitLifecycleLoopCheckpointPersistenceV0_1

inductive ResumptionAdmissionDisposition where
  | admitted
  | checkpointUnavailable
  | readFailed
  | readEvidenceQuarantined
  deriving DecidableEq, Repr

structure DurableGitLifecycleLoopResumeInput where
  checkpointId : String
  checkpointEnvelopeDigest : String
  sourcePersistenceReceiptDigest : String
  loopId : String
  lifecycleId : String
  repositoryFullName : String
  priorEffectCount : Nat
  priorMaximumEffectCount : Nat
  resumeEffectBudget : Nat
  resumeExecutionCommandBudget : Nat
  resumeExecutionOutputBytes : Nat
  futureOnly : Bool
  activeNow : Bool
  loopExecutionAuthorized : Bool
  gitEffectAuthorized : Bool
  automaticResumptionAuthorized : Bool
  generalSuccessorStageAuthorityGranted : Bool
  priorEffectCountBound : priorEffectCount ≤ priorMaximumEffectCount

structure ResumptionAdmissionReceipt where
  sourcePersistenceReceiptDigest : String
  checkpointId : String
  repositoryFullName : String
  disposition : ResumptionAdmissionDisposition
  sourceRegistryRevision : Nat
  nextRegistryRevision : Nat
  sourceAttemptCount : Nat
  nextAttemptCount : Nat
  sourceSuccessCount : Nat
  nextSuccessCount : Nat
  checkpointReadVerified : Bool
  resumeInputIssued : Bool
  loopExecutionPerformed : Bool
  gitEffectPerformed : Bool
  automaticResumptionPerformed : Bool
  networkAccessed : Bool
  secretMaterialRead : Bool
  generalGitAuthorityGranted : Bool
  generalSuccessorStageAuthorityGranted : Bool
  futureOnly : Bool
  activeNow : Bool
  registryStep : nextRegistryRevision = sourceRegistryRevision + 1
  attemptStep : nextAttemptCount = sourceAttemptCount + 1
  admittedStep :
    disposition = .admitted → nextSuccessCount = sourceSuccessCount + 1
  nonAdmittedStep :
    disposition ≠ .admitted → nextSuccessCount = sourceSuccessCount

structure ResumptionAdmissionReceiptValid (receipt : ResumptionAdmissionReceipt) : Prop where
  noLoopExecution : receipt.loopExecutionPerformed = false
  noGitEffect : receipt.gitEffectPerformed = false
  noAutomaticResumption : receipt.automaticResumptionPerformed = false
  noNetwork : receipt.networkAccessed = false
  noSecretRead : receipt.secretMaterialRead = false
  noGeneralGitAuthority : receipt.generalGitAuthorityGranted = false
  noGeneralSuccessor : receipt.generalSuccessorStageAuthorityGranted = false
  futureOnly : receipt.futureOnly = true
  inactive : receipt.activeNow = false
  admittedIffVerifiedAndIssued :
    receipt.disposition = .admitted ↔
      receipt.checkpointReadVerified = true ∧ receipt.resumeInputIssued = true

structure ResumptionAdmissionEnvelope where
  persistenceReceipt : DurableCheckpointPersistenceReceipt
  persistenceReceiptValid :
    DurableCheckpointPersistenceReceiptValid persistenceReceipt
  persistenceReceiptDigest : String
  receipt : ResumptionAdmissionReceipt
  receiptValid : ResumptionAdmissionReceiptValid receipt
  sourceReceiptBound :
    receipt.sourcePersistenceReceiptDigest = persistenceReceiptDigest
  checkpointBound : receipt.checkpointId = persistenceReceipt.checkpointId
  repositoryBound :
    receipt.repositoryFullName = persistenceReceipt.repositoryFullName

theorem registry_advances_exactly_once (receipt : ResumptionAdmissionReceipt) :
    receipt.nextRegistryRevision = receipt.sourceRegistryRevision + 1 ∧
      receipt.nextAttemptCount = receipt.sourceAttemptCount + 1 := by
  exact ⟨receipt.registryStep, receipt.attemptStep⟩

theorem admitted_read_issues_future_only_input
    (receipt : ResumptionAdmissionReceipt)
    (valid : ResumptionAdmissionReceiptValid receipt)
    (admitted : receipt.disposition = .admitted) :
    receipt.checkpointReadVerified = true ∧
      receipt.resumeInputIssued = true ∧
      receipt.futureOnly = true ∧ receipt.activeNow = false := by
  have h := (valid.admittedIffVerifiedAndIssued).mp admitted
  exact ⟨h.1, h.2, valid.futureOnly, valid.inactive⟩

theorem non_admitted_preserves_success_count
    (receipt : ResumptionAdmissionReceipt)
    (notAdmitted : receipt.disposition ≠ .admitted) :
    receipt.nextSuccessCount = receipt.sourceSuccessCount := by
  exact receipt.nonAdmittedStep notAdmitted

theorem admission_performs_no_active_effect
    (receipt : ResumptionAdmissionReceipt)
    (valid : ResumptionAdmissionReceiptValid receipt) :
    receipt.loopExecutionPerformed = false ∧
      receipt.gitEffectPerformed = false ∧
      receipt.automaticResumptionPerformed = false ∧
      receipt.activeNow = false := by
  exact ⟨valid.noLoopExecution, valid.noGitEffect,
    valid.noAutomaticResumption, valid.inactive⟩

theorem admission_is_bound_to_checkpoint
    (envelope : ResumptionAdmissionEnvelope) :
    envelope.receipt.sourcePersistenceReceiptDigest =
        envelope.persistenceReceiptDigest ∧
      envelope.receipt.checkpointId = envelope.persistenceReceipt.checkpointId ∧
      envelope.receipt.repositoryFullName =
        envelope.persistenceReceipt.repositoryFullName := by
  exact ⟨envelope.sourceReceiptBound, envelope.checkpointBound,
    envelope.repositoryBound⟩

end KUOS.CodeAI.DurableGitLifecycleLoopResumptionAdmissionV0_1
