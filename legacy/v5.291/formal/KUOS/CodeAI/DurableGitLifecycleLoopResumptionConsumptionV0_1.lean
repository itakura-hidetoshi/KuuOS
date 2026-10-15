import KUOS.CodeAI.DurableGitLifecycleLoopResumptionAdmissionV0_1

namespace KUOS.CodeAI.DurableGitLifecycleLoopResumptionConsumptionV0_1

open KUOS.CodeAI.DurableGitLifecycleLoopResumptionAdmissionV0_1

structure DurableGitLifecycleLoopExecutionInput where
  sourceResumptionReceiptDigest : String
  sourceResumptionEvidenceDigest : String
  sourceResumptionRegistryDigest : String
  sourceResumeInputDigest : String
  checkpointId : String
  checkpointEnvelopeDigest : String
  loopId : String
  lifecycleId : String
  repositoryFullName : String
  priorEffectCount : Nat
  priorMaximumEffectCount : Nat
  resumeEffectBudget : Nat
  resumeExecutionCommandBudget : Nat
  resumeExecutionOutputBytes : Nat
  oneShot : Bool
  reusable : Bool
  activeNow : Bool
  loopExecutionAuthorized : Bool
  directGitEffectAuthorized : Bool
  automaticExecutionAuthorized : Bool
  networkAccessAuthorized : Bool
  secretMaterialReadAuthorized : Bool
  generalGitAuthorityGranted : Bool
  generalSuccessorStageAuthorityGranted : Bool
  priorEffectCountBound : priorEffectCount ≤ priorMaximumEffectCount

structure ResumptionConsumptionReceipt where
  sourceResumptionReceiptDigest : String
  sourceResumeInputDigest : String
  executionInputDigest : String
  checkpointId : String
  repositoryFullName : String
  sourceRegistryRevision : Nat
  nextRegistryRevision : Nat
  sourceSuccessCount : Nat
  nextSuccessCount : Nat
  sourceHistoryLength : Nat
  nextHistoryLength : Nat
  sourceResumptionBundleVerified : Bool
  sourceResumeInputVerified : Bool
  consumptionNonceConsumed : Bool
  resumeInputConsumed : Bool
  executionInputIssued : Bool
  executionInputOneShot : Bool
  executionInputReusable : Bool
  executionInputActive : Bool
  loopExecutionAuthorizedForSuccessor : Bool
  directGitEffectAuthorized : Bool
  automaticExecutionAuthorized : Bool
  loopExecutionPerformed : Bool
  gitEffectPerformed : Bool
  automaticResumptionPerformed : Bool
  networkAccessed : Bool
  secretMaterialRead : Bool
  generalGitAuthorityGranted : Bool
  generalSuccessorStageAuthorityGranted : Bool
  registryStep : nextRegistryRevision = sourceRegistryRevision + 1
  successStep : nextSuccessCount = sourceSuccessCount + 1
  historyStep : nextHistoryLength = sourceHistoryLength + 1

structure ResumptionConsumptionReceiptValid
    (receipt : ResumptionConsumptionReceipt) : Prop where
  sourceBundleVerified : receipt.sourceResumptionBundleVerified = true
  sourceInputVerified : receipt.sourceResumeInputVerified = true
  nonceConsumed : receipt.consumptionNonceConsumed = true
  inputConsumed : receipt.resumeInputConsumed = true
  executionInputIssued : receipt.executionInputIssued = true
  executionInputOneShot : receipt.executionInputOneShot = true
  executionInputNonReusable : receipt.executionInputReusable = false
  executionInputActive : receipt.executionInputActive = true
  boundedLoopAuthority : receipt.loopExecutionAuthorizedForSuccessor = true
  noDirectGitAuthority : receipt.directGitEffectAuthorized = false
  noAutomaticExecution : receipt.automaticExecutionAuthorized = false
  noLoopExecutionDuringConsumption : receipt.loopExecutionPerformed = false
  noGitEffectDuringConsumption : receipt.gitEffectPerformed = false
  noAutomaticResumption : receipt.automaticResumptionPerformed = false
  noNetwork : receipt.networkAccessed = false
  noSecretRead : receipt.secretMaterialRead = false
  noGeneralGitAuthority : receipt.generalGitAuthorityGranted = false
  noGeneralSuccessor : receipt.generalSuccessorStageAuthorityGranted = false

structure ResumptionConsumptionEnvelope where
  sourceAdmissionReceipt : ResumptionAdmissionReceipt
  sourceAdmissionReceiptValid :
    ResumptionAdmissionReceiptValid sourceAdmissionReceipt
  sourceAdmissionReceiptDigest : String
  sourceResumeInput : DurableGitLifecycleLoopResumeInput
  sourceResumeInputDigest : String
  executionInput : DurableGitLifecycleLoopExecutionInput
  receipt : ResumptionConsumptionReceipt
  receiptValid : ResumptionConsumptionReceiptValid receipt
  sourceReceiptBound :
    receipt.sourceResumptionReceiptDigest = sourceAdmissionReceiptDigest
  sourceInputBound :
    receipt.sourceResumeInputDigest = sourceResumeInputDigest
  checkpointBound :
    receipt.checkpointId = sourceResumeInput.checkpointId
  repositoryBound :
    receipt.repositoryFullName = sourceResumeInput.repositoryFullName
  executionCheckpointBound :
    executionInput.checkpointId = sourceResumeInput.checkpointId
  executionRepositoryBound :
    executionInput.repositoryFullName = sourceResumeInput.repositoryFullName

theorem registry_and_histories_advance_exactly_once
    (receipt : ResumptionConsumptionReceipt) :
    receipt.nextRegistryRevision = receipt.sourceRegistryRevision + 1 ∧
      receipt.nextSuccessCount = receipt.sourceSuccessCount + 1 ∧
      receipt.nextHistoryLength = receipt.sourceHistoryLength + 1 := by
  exact ⟨receipt.registryStep, receipt.successStep, receipt.historyStep⟩

theorem consumption_issues_active_one_shot_input
    (receipt : ResumptionConsumptionReceipt)
    (valid : ResumptionConsumptionReceiptValid receipt) :
    receipt.executionInputIssued = true ∧
      receipt.executionInputOneShot = true ∧
      receipt.executionInputReusable = false ∧
      receipt.executionInputActive = true ∧
      receipt.loopExecutionAuthorizedForSuccessor = true := by
  exact ⟨valid.executionInputIssued, valid.executionInputOneShot,
    valid.executionInputNonReusable, valid.executionInputActive,
    valid.boundedLoopAuthority⟩

theorem consumption_performs_no_effect
    (receipt : ResumptionConsumptionReceipt)
    (valid : ResumptionConsumptionReceiptValid receipt) :
    receipt.loopExecutionPerformed = false ∧
      receipt.gitEffectPerformed = false ∧
      receipt.automaticResumptionPerformed = false ∧
      receipt.networkAccessed = false ∧
      receipt.secretMaterialRead = false := by
  exact ⟨valid.noLoopExecutionDuringConsumption,
    valid.noGitEffectDuringConsumption, valid.noAutomaticResumption,
    valid.noNetwork, valid.noSecretRead⟩

theorem active_input_is_not_direct_git_or_general_authority
    (receipt : ResumptionConsumptionReceipt)
    (valid : ResumptionConsumptionReceiptValid receipt) :
    receipt.directGitEffectAuthorized = false ∧
      receipt.automaticExecutionAuthorized = false ∧
      receipt.generalGitAuthorityGranted = false ∧
      receipt.generalSuccessorStageAuthorityGranted = false := by
  exact ⟨valid.noDirectGitAuthority, valid.noAutomaticExecution,
    valid.noGeneralGitAuthority, valid.noGeneralSuccessor⟩

theorem consumption_is_bound_to_admitted_checkpoint
    (envelope : ResumptionConsumptionEnvelope) :
    envelope.receipt.sourceResumptionReceiptDigest =
        envelope.sourceAdmissionReceiptDigest ∧
      envelope.receipt.sourceResumeInputDigest =
        envelope.sourceResumeInputDigest ∧
      envelope.receipt.checkpointId =
        envelope.sourceResumeInput.checkpointId ∧
      envelope.executionInput.checkpointId =
        envelope.sourceResumeInput.checkpointId ∧
      envelope.executionInput.repositoryFullName =
        envelope.sourceResumeInput.repositoryFullName := by
  exact ⟨envelope.sourceReceiptBound, envelope.sourceInputBound,
    envelope.checkpointBound, envelope.executionCheckpointBound,
    envelope.executionRepositoryBound⟩

end KUOS.CodeAI.DurableGitLifecycleLoopResumptionConsumptionV0_1
