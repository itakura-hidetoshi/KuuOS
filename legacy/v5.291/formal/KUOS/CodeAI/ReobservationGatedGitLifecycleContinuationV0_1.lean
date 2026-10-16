import KUOS.CodeAI.AutonomousGitEffectReobservationV0_1

namespace KUOS.CodeAI.ReobservationGatedGitLifecycleContinuationV0_1

open KUOS.CodeAI.AutonomousGitLifecycleEnvelopeV0_1
open KUOS.CodeAI.AutonomousGitEffectReobservationV0_1

structure ReobservationGatedContinuationReceipt where
  sourceReobservationReceiptDigest : String
  sourceLifecycleStateDigest : String
  delegatedLifecycleStateDigest : String
  continuationRequestDigest : String
  continuationPolicyDigest : String
  sourceRegistryDigest : String
  nextRegistryDigest : String
  continuationEvidenceDigest : String
  lifecycleId : String
  repositoryFullName : String
  sourceRegistryRevision : Nat
  nextRegistryRevision : Nat
  sourceConsumedCount : Nat
  nextConsumedCount : Nat
  sourceReobservationReceiptVerified : Bool
  sourceReobservationEvidenceVerified : Bool
  sourceLifecycleStateVerified : Bool
  sourceReobservationReceiptConsumed : Bool
  continuationNonceConsumed : Bool
  registryAdvancedOnce : Bool
  exactlyOneLifecycleEvaluation : Bool
  stateProjectionPerformed : Bool
  stateProjectionFactualFieldsChanged : Bool
  delegatedLifecycleReceiptIssued : Bool
  oneEffectLeaseIssued : Bool
  automaticEffectExecutionPerformed : Bool
  reobservationStateTreatedAsAuthority : Bool
  checksTreatedAsCorrectnessProof : Bool
  mergeTreatedAsTruth : Bool
  generalGitAuthorityGranted : Bool
  generalSuccessorStageAuthorityGranted : Bool
  deploymentAuthorityGranted : Bool
  secretAccessAuthorityGranted : Bool
  historyReadOnly : Bool
  activeNow : Bool
  registryRevisionStep : nextRegistryRevision = sourceRegistryRevision + 1
  consumedCountStep : nextConsumedCount = sourceConsumedCount + 1

structure ReobservationGatedContinuationReceiptValid
    (receipt : ReobservationGatedContinuationReceipt) : Prop where
  reobservationReceiptVerified :
    receipt.sourceReobservationReceiptVerified = true
  reobservationEvidenceVerified :
    receipt.sourceReobservationEvidenceVerified = true
  lifecycleStateVerified : receipt.sourceLifecycleStateVerified = true
  reobservationReceiptConsumed :
    receipt.sourceReobservationReceiptConsumed = true
  nonceConsumed : receipt.continuationNonceConsumed = true
  registryAdvanced : receipt.registryAdvancedOnce = true
  exactlyOneEvaluation : receipt.exactlyOneLifecycleEvaluation = true
  noFactualProjectionChange :
    receipt.stateProjectionFactualFieldsChanged = false
  delegatedReceiptIssued : receipt.delegatedLifecycleReceiptIssued = true
  noAutomaticExecution : receipt.automaticEffectExecutionPerformed = false
  stateNotAuthority : receipt.reobservationStateTreatedAsAuthority = false
  checksNotCorrectness : receipt.checksTreatedAsCorrectnessProof = false
  mergeNotTruth : receipt.mergeTreatedAsTruth = false
  noGeneralGitAuthority : receipt.generalGitAuthorityGranted = false
  noGeneralSuccessor : receipt.generalSuccessorStageAuthorityGranted = false
  noDeploymentAuthority : receipt.deploymentAuthorityGranted = false
  noSecretAuthority : receipt.secretAccessAuthorityGranted = false
  historyReadOnly : receipt.historyReadOnly = true

structure ReobservationGatedGitLifecycleContinuationEnvelope where
  sourceReobservationReceipt : GitEffectReobservationReceipt
  sourceReobservationReceiptValid :
    GitEffectReobservationReceiptValid sourceReobservationReceipt
  delegatedLifecycleReceipt : AutonomousGitLifecycleReceipt
  delegatedLifecycleReceiptValid :
    AutonomousGitLifecycleReceiptValid delegatedLifecycleReceipt
  receipt : ReobservationGatedContinuationReceipt
  receiptValid : ReobservationGatedContinuationReceiptValid receipt
  lifecycleBound : receipt.lifecycleId = delegatedLifecycleReceipt.lifecycleId
  repositoryBound :
    receipt.repositoryFullName = delegatedLifecycleReceipt.repositoryFullName
  leaseBound :
    receipt.oneEffectLeaseIssued = delegatedLifecycleReceipt.executionLeaseIssued
  activeBound : receipt.activeNow = delegatedLifecycleReceipt.activeNow

 theorem continuation_consumes_one_reobservation_receipt_and_nonce
    (receipt : ReobservationGatedContinuationReceipt)
    (valid : ReobservationGatedContinuationReceiptValid receipt) :
    receipt.sourceReobservationReceiptConsumed = true ∧
      receipt.continuationNonceConsumed = true ∧
      receipt.exactlyOneLifecycleEvaluation = true ∧
      receipt.nextRegistryRevision = receipt.sourceRegistryRevision + 1 ∧
      receipt.nextConsumedCount = receipt.sourceConsumedCount + 1 := by
  exact ⟨valid.reobservationReceiptConsumed, valid.nonceConsumed,
    valid.exactlyOneEvaluation, receipt.registryRevisionStep,
    receipt.consumedCountStep⟩

 theorem state_projection_changes_no_factual_field
    (receipt : ReobservationGatedContinuationReceipt)
    (valid : ReobservationGatedContinuationReceiptValid receipt) :
    receipt.stateProjectionFactualFieldsChanged = false := by
  exact valid.noFactualProjectionChange

 theorem continuation_performs_no_effect
    (receipt : ReobservationGatedContinuationReceipt)
    (valid : ReobservationGatedContinuationReceiptValid receipt) :
    receipt.automaticEffectExecutionPerformed = false ∧
      receipt.deploymentAuthorityGranted = false ∧
      receipt.secretAccessAuthorityGranted = false := by
  exact ⟨valid.noAutomaticExecution, valid.noDeploymentAuthority,
    valid.noSecretAuthority⟩

 theorem fresh_state_is_not_itself_authority
    (receipt : ReobservationGatedContinuationReceipt)
    (valid : ReobservationGatedContinuationReceiptValid receipt) :
    receipt.reobservationStateTreatedAsAuthority = false ∧
      receipt.generalGitAuthorityGranted = false ∧
      receipt.generalSuccessorStageAuthorityGranted = false := by
  exact ⟨valid.stateNotAuthority, valid.noGeneralGitAuthority,
    valid.noGeneralSuccessor⟩

 theorem delegated_lease_is_exactly_lifecycle_owned
    (envelope : ReobservationGatedGitLifecycleContinuationEnvelope) :
    envelope.receipt.oneEffectLeaseIssued =
        envelope.delegatedLifecycleReceipt.executionLeaseIssued ∧
      envelope.receipt.activeNow = envelope.delegatedLifecycleReceipt.activeNow := by
  exact ⟨envelope.leaseBound, envelope.activeBound⟩

 theorem continuation_is_neither_correctness_nor_truth
    (receipt : ReobservationGatedContinuationReceipt)
    (valid : ReobservationGatedContinuationReceiptValid receipt) :
    receipt.checksTreatedAsCorrectnessProof = false ∧
      receipt.mergeTreatedAsTruth = false := by
  exact ⟨valid.checksNotCorrectness, valid.mergeNotTruth⟩

 theorem continuation_is_bound_to_delegated_lifecycle
    (envelope : ReobservationGatedGitLifecycleContinuationEnvelope) :
    envelope.receipt.lifecycleId =
        envelope.delegatedLifecycleReceipt.lifecycleId ∧
      envelope.receipt.repositoryFullName =
        envelope.delegatedLifecycleReceipt.repositoryFullName := by
  exact ⟨envelope.lifecycleBound, envelope.repositoryBound⟩

end KUOS.CodeAI.ReobservationGatedGitLifecycleContinuationV0_1
