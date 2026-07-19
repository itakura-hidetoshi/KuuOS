import KUOS.CodeAI.AutonomousGitLifecycleEnvelopeV0_1

namespace KUOS.CodeAI.AutonomousGitEffectExecutionV0_1

open KUOS.CodeAI.AutonomousGitLifecycleEnvelopeV0_1

inductive ExecutionDisposition where
  | completed
  | failed
  | evidenceQuarantined
  deriving DecidableEq, Repr

inductive ExecutionMode where
  | boundedLocalGitEffectExecution
  | boundedRemoteGitEffectExecution
  | boundedPullRequestEffectExecution
  | boundedMergeEffectExecution
  deriving DecidableEq, Repr

structure GitEffectExecutionReceipt where
  sourceLifecycleReceiptDigest : String
  executionRequestDigest : String
  executionPolicyDigest : String
  sourceRegistryDigest : String
  nextRegistryDigest : String
  executionEvidenceDigest : String
  lifecycleId : String
  executionId : String
  repositoryFullName : String
  effectPhase : EffectPhase
  disposition : ExecutionDisposition
  operatingMode : ExecutionMode
  sourceRegistryRevision : Nat
  nextRegistryRevision : Nat
  sourceConsumedCount : Nat
  nextConsumedCount : Nat
  performedEffectCount : Nat
  routeReceiptRecorded : Bool
  sourceOneEffectLeaseVerified : Bool
  sourceOneEffectLeaseConsumed : Bool
  executionNonceConsumed : Bool
  registryAdvancedOnce : Bool
  exactlyOneAdapterInvocation : Bool
  adapterEvidenceValid : Bool
  effectCompletionConfirmed : Bool
  effectFailureRecorded : Bool
  evidenceQuarantined : Bool
  reobservationRequired : Bool
  localCommitPerformed : Bool
  pushPerformed : Bool
  pullRequestCreated : Bool
  pullRequestMarkedReady : Bool
  mergePerformed : Bool
  sourceMergeGateComplete : Bool
  sourceHeadShaPinned : Bool
  adapterHeadShaPinned : Bool
  forcePushPerformed : Bool
  remoteBranchDeleted : Bool
  adminMergeBypassUsed : Bool
  deploymentPerformed : Bool
  secretMaterialRead : Bool
  tokenMaterialEmitted : Bool
  opaqueTokenUsed : Bool
  automaticSuccessorEffectAuthorityGranted : Bool
  generalGitAuthorityGranted : Bool
  generalSuccessorStageAuthorityGranted : Bool
  effectCompletionTreatedAsCorrectness : Bool
  mergeTreatedAsTruth : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  registryRevisionStep : nextRegistryRevision = sourceRegistryRevision + 1
  consumedCountStep : nextConsumedCount = sourceConsumedCount + 1
  phaseSupported :
    effectPhase = .localCommit ∨
      effectPhase = .pushBranch ∨
      effectPhase = .createPullRequest ∨
      effectPhase = .markPullRequestReady ∨
      effectPhase = .mergePullRequest
  completedEffectCount :
    effectCompletionConfirmed = true → performedEffectCount = 1
  incompleteEffectCount :
    effectCompletionConfirmed = false → performedEffectCount = 0
  localCommitCorrespondence :
    localCommitPerformed = true →
      effectPhase = .localCommit ∧
        pushPerformed = false ∧
        pullRequestCreated = false ∧
        pullRequestMarkedReady = false ∧
        mergePerformed = false
  pushCorrespondence :
    pushPerformed = true →
      effectPhase = .pushBranch ∧
        localCommitPerformed = false ∧
        pullRequestCreated = false ∧
        pullRequestMarkedReady = false ∧
        mergePerformed = false
  pullRequestCorrespondence :
    pullRequestCreated = true →
      effectPhase = .createPullRequest ∧
        localCommitPerformed = false ∧
        pushPerformed = false ∧
        pullRequestMarkedReady = false ∧
        mergePerformed = false
  readinessCorrespondence :
    pullRequestMarkedReady = true →
      effectPhase = .markPullRequestReady ∧
        localCommitPerformed = false ∧
        pushPerformed = false ∧
        pullRequestCreated = false ∧
        mergePerformed = false
  mergeCorrespondence :
    mergePerformed = true →
      effectPhase = .mergePullRequest ∧
        sourceMergeGateComplete = true ∧
        sourceHeadShaPinned = true ∧
        adapterHeadShaPinned = true ∧
        localCommitPerformed = false ∧
        pushPerformed = false ∧
        pullRequestCreated = false ∧
        pullRequestMarkedReady = false

structure GitEffectExecutionReceiptValid
    (receipt : GitEffectExecutionReceipt) : Prop where
  routeRecorded : receipt.routeReceiptRecorded = true
  sourceLeaseVerified : receipt.sourceOneEffectLeaseVerified = true
  sourceLeaseConsumed : receipt.sourceOneEffectLeaseConsumed = true
  nonceConsumed : receipt.executionNonceConsumed = true
  registryAdvanced : receipt.registryAdvancedOnce = true
  exactlyOneInvocation : receipt.exactlyOneAdapterInvocation = true
  noForcePush : receipt.forcePushPerformed = false
  noRemoteBranchDeletion : receipt.remoteBranchDeleted = false
  noAdminMergeBypass : receipt.adminMergeBypassUsed = false
  noDeployment : receipt.deploymentPerformed = false
  noSecretRead : receipt.secretMaterialRead = false
  noTokenEmission : receipt.tokenMaterialEmitted = false
  noAutomaticSuccessor :
    receipt.automaticSuccessorEffectAuthorityGranted = false
  noGeneralGitAuthority : receipt.generalGitAuthorityGranted = false
  noGeneralSuccessor : receipt.generalSuccessorStageAuthorityGranted = false
  completionNotCorrectness :
    receipt.effectCompletionTreatedAsCorrectness = false
  mergeNotTruth : receipt.mergeTreatedAsTruth = false
  historyReadOnly : receipt.historyReadOnly = true
  notFutureOnly : receipt.futureOnly = false
  inactive : receipt.activeNow = false

structure AutonomousGitEffectExecutionEnvelope where
  sourceReceipt : AutonomousGitLifecycleReceipt
  sourceReceiptValid : AutonomousGitLifecycleReceiptValid sourceReceipt
  sourceLeaseIssued : sourceReceipt.executionLeaseIssued = true
  sourceActive : sourceReceipt.activeNow = true
  receipt : GitEffectExecutionReceipt
  receiptValid : GitEffectExecutionReceiptValid receipt
  repositoryBound : receipt.repositoryFullName = sourceReceipt.repositoryFullName
  lifecycleBound : receipt.lifecycleId = sourceReceipt.lifecycleId
  phaseBound : receipt.effectPhase = sourceReceipt.nextEffectPhase

theorem execution_consumes_one_lease_and_one_nonce
    (receipt : GitEffectExecutionReceipt)
    (valid : GitEffectExecutionReceiptValid receipt) :
    receipt.sourceOneEffectLeaseConsumed = true ∧
      receipt.executionNonceConsumed = true ∧
      receipt.exactlyOneAdapterInvocation = true ∧
      receipt.nextRegistryRevision = receipt.sourceRegistryRevision + 1 ∧
      receipt.nextConsumedCount = receipt.sourceConsumedCount + 1 := by
  exact ⟨valid.sourceLeaseConsumed, valid.nonceConsumed,
    valid.exactlyOneInvocation, receipt.registryRevisionStep,
    receipt.consumedCountStep⟩

theorem completed_execution_records_exactly_one_effect
    (receipt : GitEffectExecutionReceipt)
    (completed : receipt.effectCompletionConfirmed = true) :
    receipt.performedEffectCount = 1 := by
  exact receipt.completedEffectCount completed

theorem failed_or_quarantined_execution_records_no_confirmed_effect
    (receipt : GitEffectExecutionReceipt)
    (incomplete : receipt.effectCompletionConfirmed = false) :
    receipt.performedEffectCount = 0 := by
  exact receipt.incompleteEffectCount incomplete

theorem merge_requires_source_gate_and_double_head_pin
    (receipt : GitEffectExecutionReceipt)
    (merged : receipt.mergePerformed = true) :
    receipt.effectPhase = .mergePullRequest ∧
      receipt.sourceMergeGateComplete = true ∧
      receipt.sourceHeadShaPinned = true ∧
      receipt.adapterHeadShaPinned = true := by
  rcases receipt.mergeCorrespondence merged with
    ⟨phase, gate, sourcePin, adapterPin, _, _, _, _⟩
  exact ⟨phase, gate, sourcePin, adapterPin⟩

theorem destructive_and_secret_effects_remain_excluded
    (receipt : GitEffectExecutionReceipt)
    (valid : GitEffectExecutionReceiptValid receipt) :
    receipt.forcePushPerformed = false ∧
      receipt.remoteBranchDeleted = false ∧
      receipt.adminMergeBypassUsed = false ∧
      receipt.deploymentPerformed = false ∧
      receipt.secretMaterialRead = false ∧
      receipt.tokenMaterialEmitted = false := by
  exact ⟨valid.noForcePush, valid.noRemoteBranchDeletion,
    valid.noAdminMergeBypass, valid.noDeployment, valid.noSecretRead,
    valid.noTokenEmission⟩

theorem execution_grants_no_automatic_or_general_successor_authority
    (receipt : GitEffectExecutionReceipt)
    (valid : GitEffectExecutionReceiptValid receipt) :
    receipt.automaticSuccessorEffectAuthorityGranted = false ∧
      receipt.generalGitAuthorityGranted = false ∧
      receipt.generalSuccessorStageAuthorityGranted = false ∧
      receipt.activeNow = false := by
  exact ⟨valid.noAutomaticSuccessor, valid.noGeneralGitAuthority,
    valid.noGeneralSuccessor, valid.inactive⟩

theorem execution_is_bound_to_source_lifecycle_lease
    (envelope : AutonomousGitEffectExecutionEnvelope) :
    envelope.sourceReceipt.executionLeaseIssued = true ∧
      envelope.sourceReceipt.activeNow = true ∧
      envelope.receipt.repositoryFullName =
        envelope.sourceReceipt.repositoryFullName ∧
      envelope.receipt.lifecycleId = envelope.sourceReceipt.lifecycleId ∧
      envelope.receipt.effectPhase = envelope.sourceReceipt.nextEffectPhase := by
  exact ⟨envelope.sourceLeaseIssued, envelope.sourceActive,
    envelope.repositoryBound, envelope.lifecycleBound, envelope.phaseBound⟩

theorem completion_is_neither_correctness_nor_truth
    (receipt : GitEffectExecutionReceipt)
    (valid : GitEffectExecutionReceiptValid receipt) :
    receipt.effectCompletionTreatedAsCorrectness = false ∧
      receipt.mergeTreatedAsTruth = false := by
  exact ⟨valid.completionNotCorrectness, valid.mergeNotTruth⟩

end KUOS.CodeAI.AutonomousGitEffectExecutionV0_1
