import KUOS.CodeAI.AutonomousGitEffectExecutionV0_1

namespace KUOS.CodeAI.AutonomousGitEffectReobservationV0_1

open KUOS.CodeAI.AutonomousGitLifecycleEnvelopeV0_1
open KUOS.CodeAI.AutonomousGitEffectExecutionV0_1

inductive ReobservationDisposition where
  | completed
  | failed
  | evidenceQuarantined
  deriving DecidableEq, Repr

structure GitEffectReobservationReceipt where
  sourceLifecycleReceiptDigest : String
  sourceExecutionReceiptDigest : String
  sourceExecutionEvidenceDigest : String
  reobservationRequestDigest : String
  reobservationPolicyDigest : String
  sourceRegistryDigest : String
  nextRegistryDigest : String
  reobservationEvidenceDigest : String
  lifecycleStateDigest : String
  lifecycleId : String
  reobservationId : String
  repositoryFullName : String
  effectPhase : EffectPhase
  sourceExecutionDisposition : ExecutionDisposition
  disposition : ReobservationDisposition
  sourceRegistryRevision : Nat
  nextRegistryRevision : Nat
  sourceConsumedCount : Nat
  nextConsumedCount : Nat
  routeReceiptRecorded : Bool
  sourceLifecycleReceiptVerified : Bool
  sourceExecutionReceiptVerified : Bool
  sourceExecutionEvidenceVerified : Bool
  sourceExecutionReceiptConsumedForReobservation : Bool
  reobservationNonceConsumed : Bool
  registryAdvancedOnce : Bool
  exactlyOneAdapterInvocation : Bool
  adapterEvidenceValid : Bool
  lifecycleStateCorrespondenceConfirmed : Bool
  sourceEffectCorrespondenceConfirmed : Bool
  freshLifecycleStateIssued : Bool
  reobservationFailureRecorded : Bool
  evidenceQuarantined : Bool
  networkAccessed : Bool
  secretMaterialRead : Bool
  gitWritePerformed : Bool
  deploymentPerformed : Bool
  effectExecutionPerformed : Bool
  automaticSuccessorEffectAuthorityGranted : Bool
  generalGitAuthorityGranted : Bool
  generalSuccessorStageAuthorityGranted : Bool
  observationTreatedAsCorrectness : Bool
  mergeTreatedAsTruth : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  registryRevisionStep : nextRegistryRevision = sourceRegistryRevision + 1
  consumedCountStep : nextConsumedCount = sourceConsumedCount + 1
  completedIssuesFreshState :
    disposition = .completed → freshLifecycleStateIssued = true
  failedIssuesNoState :
    disposition = .failed → freshLifecycleStateIssued = false
  quarantinedIssuesNoState :
    disposition = .evidenceQuarantined → freshLifecycleStateIssued = false

structure GitEffectReobservationReceiptValid
    (receipt : GitEffectReobservationReceipt) : Prop where
  routeRecorded : receipt.routeReceiptRecorded = true
  lifecycleVerified : receipt.sourceLifecycleReceiptVerified = true
  executionReceiptVerified : receipt.sourceExecutionReceiptVerified = true
  executionEvidenceVerified : receipt.sourceExecutionEvidenceVerified = true
  executionReceiptConsumed :
    receipt.sourceExecutionReceiptConsumedForReobservation = true
  nonceConsumed : receipt.reobservationNonceConsumed = true
  registryAdvanced : receipt.registryAdvancedOnce = true
  exactlyOneInvocation : receipt.exactlyOneAdapterInvocation = true
  noNetwork : receipt.networkAccessed = false
  noSecretRead : receipt.secretMaterialRead = false
  noGitWrite : receipt.gitWritePerformed = false
  noDeployment : receipt.deploymentPerformed = false
  noEffectExecution : receipt.effectExecutionPerformed = false
  noAutomaticSuccessor :
    receipt.automaticSuccessorEffectAuthorityGranted = false
  noGeneralGitAuthority : receipt.generalGitAuthorityGranted = false
  noGeneralSuccessor : receipt.generalSuccessorStageAuthorityGranted = false
  observationNotCorrectness :
    receipt.observationTreatedAsCorrectness = false
  mergeNotTruth : receipt.mergeTreatedAsTruth = false
  historyReadOnly : receipt.historyReadOnly = true
  notFutureOnly : receipt.futureOnly = false
  inactive : receipt.activeNow = false

structure AutonomousGitEffectReobservationEnvelope where
  sourceLifecycleReceipt : AutonomousGitLifecycleReceipt
  sourceLifecycleReceiptValid :
    AutonomousGitLifecycleReceiptValid sourceLifecycleReceipt
  sourceExecutionReceipt : GitEffectExecutionReceipt
  sourceExecutionReceiptValid :
    GitEffectExecutionReceiptValid sourceExecutionReceipt
  receipt : GitEffectReobservationReceipt
  receiptValid : GitEffectReobservationReceiptValid receipt
  lifecycleBound : receipt.lifecycleId = sourceLifecycleReceipt.lifecycleId
  repositoryBound :
    receipt.repositoryFullName = sourceLifecycleReceipt.repositoryFullName
  phaseBound : receipt.effectPhase = sourceExecutionReceipt.effectPhase

theorem reobservation_consumes_one_execution_receipt_and_nonce
    (receipt : GitEffectReobservationReceipt)
    (valid : GitEffectReobservationReceiptValid receipt) :
    receipt.sourceExecutionReceiptConsumedForReobservation = true ∧
      receipt.reobservationNonceConsumed = true ∧
      receipt.exactlyOneAdapterInvocation = true ∧
      receipt.nextRegistryRevision = receipt.sourceRegistryRevision + 1 ∧
      receipt.nextConsumedCount = receipt.sourceConsumedCount + 1 := by
  exact ⟨valid.executionReceiptConsumed, valid.nonceConsumed,
    valid.exactlyOneInvocation, receipt.registryRevisionStep,
    receipt.consumedCountStep⟩

theorem completed_reobservation_issues_fresh_state
    (receipt : GitEffectReobservationReceipt)
    (completed : receipt.disposition = .completed) :
    receipt.freshLifecycleStateIssued = true := by
  exact receipt.completedIssuesFreshState completed

theorem failed_or_quarantined_reobservation_issues_no_state
    (receipt : GitEffectReobservationReceipt)
    (failedOrQuarantined :
      receipt.disposition = .failed ∨
        receipt.disposition = .evidenceQuarantined) :
    receipt.freshLifecycleStateIssued = false := by
  rcases failedOrQuarantined with failed | quarantined
  · exact receipt.failedIssuesNoState failed
  · exact receipt.quarantinedIssuesNoState quarantined

theorem reobservation_performs_no_effect
    (receipt : GitEffectReobservationReceipt)
    (valid : GitEffectReobservationReceiptValid receipt) :
    receipt.networkAccessed = false ∧
      receipt.secretMaterialRead = false ∧
      receipt.gitWritePerformed = false ∧
      receipt.deploymentPerformed = false ∧
      receipt.effectExecutionPerformed = false := by
  exact ⟨valid.noNetwork, valid.noSecretRead, valid.noGitWrite,
    valid.noDeployment, valid.noEffectExecution⟩

theorem fresh_state_grants_no_successor_authority
    (receipt : GitEffectReobservationReceipt)
    (valid : GitEffectReobservationReceiptValid receipt) :
    receipt.automaticSuccessorEffectAuthorityGranted = false ∧
      receipt.generalGitAuthorityGranted = false ∧
      receipt.generalSuccessorStageAuthorityGranted = false ∧
      receipt.activeNow = false := by
  exact ⟨valid.noAutomaticSuccessor, valid.noGeneralGitAuthority,
    valid.noGeneralSuccessor, valid.inactive⟩

theorem reobservation_is_bound_to_source_lineage
    (envelope : AutonomousGitEffectReobservationEnvelope) :
    envelope.receipt.lifecycleId =
        envelope.sourceLifecycleReceipt.lifecycleId ∧
      envelope.receipt.repositoryFullName =
        envelope.sourceLifecycleReceipt.repositoryFullName ∧
      envelope.receipt.effectPhase =
        envelope.sourceExecutionReceipt.effectPhase := by
  exact ⟨envelope.lifecycleBound, envelope.repositoryBound,
    envelope.phaseBound⟩

theorem observation_is_neither_correctness_nor_truth
    (receipt : GitEffectReobservationReceipt)
    (valid : GitEffectReobservationReceiptValid receipt) :
    receipt.observationTreatedAsCorrectness = false ∧
      receipt.mergeTreatedAsTruth = false := by
  exact ⟨valid.observationNotCorrectness, valid.mergeNotTruth⟩

end KUOS.CodeAI.AutonomousGitEffectReobservationV0_1
