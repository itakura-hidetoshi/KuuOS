import Mathlib

namespace KUOS.CodeAI.IntentRepositoryObservationEnvelopeV0_1

inductive Disposition where
  | intentRepositoryObservationSupported
  | intentProvenanceRepairRequired
  | repositoryIdentityRepairRequired
  | repositorySnapshotRepairRequired
  | pathAccountingRepairRequired
  | baselineEvidenceRepairRequired
  | observationWindowRepairRequired
  | observationReplayConflictRejected
  | repositoryMutationRejected
  | authorityEscalationRejected
  | intentClarificationHold
  | unsupportedToolchainAbstained
  | ownershipHandoverRequired
  | partialObservationDegraded
  deriving DecidableEq, Repr

inductive OperatingMode where
  | readOnly
  | hold
  | degradedReadOnly
  | abstain
  | handover
  | rejected
  deriving DecidableEq, Repr

structure IntentRepositoryObservationReceipt where
  intentPacketDigest : String
  repositoryObservationDigest : String
  observationPolicyDigest : String
  intentId : String
  intentRevision : String
  sourceActorId : String
  authorityOwnerId : String
  repositoryFullName : String
  sourceCommitSha : String
  resultingCommitSha : String
  sourceBranch : String
  treeDigest : String
  observedPathCount : Nat
  unavailablePathCount : Nat
  declaredPathCount : Nat
  baselineChecksComplete : Bool
  disposition : Disposition
  operatingMode : OperatingMode
  routeReceiptRecorded : Bool
  codeaiProfileReady : Bool
  clarificationRequired : Bool
  reobservationRequired : Bool
  abstained : Bool
  handoverRequired : Bool
  repositoryObservationReadOnly : Bool
  codeChangeCandidateCreated : Bool
  executionLeaseIssued : Bool
  repositoryMutationPerformed : Bool
  gitRefChanged : Bool
  branchCreated : Bool
  commitCreated : Bool
  pushPerformed : Bool
  pullRequestCreated : Bool
  mergePerformed : Bool
  deploymentPerformed : Bool
  secretAccessPerformed : Bool
  selectionAuthorityGranted : Bool
  executionAuthorityGranted : Bool
  mergeAuthorityGranted : Bool
  deploymentAuthorityGranted : Bool
  secretAccessAuthorityGranted : Bool
  intentTreatedAsTruth : Bool
  repositoryObservationTreatedAsRepositoryTruth : Bool
  validationTreatedAsCorrectnessProof : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  pathAccounting : observedPathCount + unavailablePathCount = declaredPathCount
  sourceCommitUnchanged : resultingCommitSha = sourceCommitSha
  supportedRoute :
    disposition = .intentRepositoryObservationSupported →
      operatingMode = .readOnly ∧
        routeReceiptRecorded = true ∧
        codeaiProfileReady = true ∧
        clarificationRequired = false ∧
        reobservationRequired = false ∧
        abstained = false ∧
        handoverRequired = false
  nonSupportedNotReady :
    disposition ≠ .intentRepositoryObservationSupported →
      codeaiProfileReady = false
  holdRoute :
    disposition = .intentClarificationHold →
      operatingMode = .hold ∧ clarificationRequired = true
  degradedRoute :
    disposition = .partialObservationDegraded →
      operatingMode = .degradedReadOnly ∧ reobservationRequired = true
  abstainRoute :
    disposition = .unsupportedToolchainAbstained →
      operatingMode = .abstain ∧ abstained = true
  handoverRoute :
    disposition = .ownershipHandoverRequired →
      operatingMode = .handover ∧ handoverRequired = true

structure IntentRepositoryObservationReceiptValid
    (receipt : IntentRepositoryObservationReceipt) : Prop where
  routeRecorded : receipt.routeReceiptRecorded = true
  repositoryReadOnly : receipt.repositoryObservationReadOnly = true
  noCodeCandidate : receipt.codeChangeCandidateCreated = false
  noExecutionLease : receipt.executionLeaseIssued = false
  noRepositoryMutation : receipt.repositoryMutationPerformed = false
  noGitRefChange : receipt.gitRefChanged = false
  noBranchCreation : receipt.branchCreated = false
  noCommitCreation : receipt.commitCreated = false
  noPush : receipt.pushPerformed = false
  noPullRequest : receipt.pullRequestCreated = false
  noMerge : receipt.mergePerformed = false
  noDeployment : receipt.deploymentPerformed = false
  noSecretAccess : receipt.secretAccessPerformed = false
  noSelectionAuthority : receipt.selectionAuthorityGranted = false
  noExecutionAuthority : receipt.executionAuthorityGranted = false
  noMergeAuthority : receipt.mergeAuthorityGranted = false
  noDeploymentAuthority : receipt.deploymentAuthorityGranted = false
  noSecretAccessAuthority : receipt.secretAccessAuthorityGranted = false
  intentNotTruth : receipt.intentTreatedAsTruth = false
  repositoryObservationNotTruth :
    receipt.repositoryObservationTreatedAsRepositoryTruth = false
  validationNotCorrectnessProof :
    receipt.validationTreatedAsCorrectnessProof = false
  historyReadOnly : receipt.historyReadOnly = true
  futureOnly : receipt.futureOnly = true
  inactiveNow : receipt.activeNow = false

theorem declared_paths_are_exact
    (receipt : IntentRepositoryObservationReceipt) :
    receipt.observedPathCount + receipt.unavailablePathCount =
      receipt.declaredPathCount := by
  exact receipt.pathAccounting

theorem source_commit_is_preserved
    (receipt : IntentRepositoryObservationReceipt) :
    receipt.resultingCommitSha = receipt.sourceCommitSha := by
  exact receipt.sourceCommitUnchanged

theorem supported_is_read_only_and_not_successor_authority
    (receipt : IntentRepositoryObservationReceipt)
    (valid : IntentRepositoryObservationReceiptValid receipt)
    (supported : receipt.disposition =
      .intentRepositoryObservationSupported) :
    receipt.operatingMode = .readOnly ∧
      receipt.codeaiProfileReady = true ∧
      receipt.repositoryObservationReadOnly = true ∧
      receipt.codeChangeCandidateCreated = false ∧
      receipt.executionLeaseIssued = false ∧
      receipt.repositoryMutationPerformed = false ∧
      receipt.selectionAuthorityGranted = false ∧
      receipt.executionAuthorityGranted = false := by
  rcases receipt.supportedRoute supported with
    ⟨mode, _, ready, _, _, _, _⟩
  exact ⟨mode, ready, valid.repositoryReadOnly, valid.noCodeCandidate,
    valid.noExecutionLease, valid.noRepositoryMutation,
    valid.noSelectionAuthority, valid.noExecutionAuthority⟩

theorem observation_has_no_repository_effect
    (receipt : IntentRepositoryObservationReceipt)
    (valid : IntentRepositoryObservationReceiptValid receipt) :
    receipt.repositoryMutationPerformed = false ∧
      receipt.gitRefChanged = false ∧
      receipt.branchCreated = false ∧
      receipt.commitCreated = false ∧
      receipt.pushPerformed = false ∧
      receipt.pullRequestCreated = false ∧
      receipt.mergePerformed = false ∧
      receipt.deploymentPerformed = false ∧
      receipt.secretAccessPerformed = false := by
  exact ⟨valid.noRepositoryMutation, valid.noGitRefChange,
    valid.noBranchCreation, valid.noCommitCreation, valid.noPush,
    valid.noPullRequest, valid.noMerge, valid.noDeployment,
    valid.noSecretAccess⟩

theorem observation_grants_no_authority
    (receipt : IntentRepositoryObservationReceipt)
    (valid : IntentRepositoryObservationReceiptValid receipt) :
    receipt.selectionAuthorityGranted = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.mergeAuthorityGranted = false ∧
      receipt.deploymentAuthorityGranted = false ∧
      receipt.secretAccessAuthorityGranted = false := by
  exact ⟨valid.noSelectionAuthority, valid.noExecutionAuthority,
    valid.noMergeAuthority, valid.noDeploymentAuthority,
    valid.noSecretAccessAuthority⟩

theorem observation_claims_neither_truth_nor_correctness
    (receipt : IntentRepositoryObservationReceipt)
    (valid : IntentRepositoryObservationReceiptValid receipt) :
    receipt.intentTreatedAsTruth = false ∧
      receipt.repositoryObservationTreatedAsRepositoryTruth = false ∧
      receipt.validationTreatedAsCorrectnessProof = false := by
  exact ⟨valid.intentNotTruth, valid.repositoryObservationNotTruth,
    valid.validationNotCorrectnessProof⟩

theorem hold_is_first_class
    (receipt : IntentRepositoryObservationReceipt)
    (route : receipt.disposition = .intentClarificationHold) :
    receipt.operatingMode = .hold ∧
      receipt.clarificationRequired = true ∧
      receipt.codeaiProfileReady = false := by
  rcases receipt.holdRoute route with ⟨mode, clarification⟩
  have notSupported : receipt.disposition ≠
      .intentRepositoryObservationSupported := by
    intro contradiction
    rw [route] at contradiction
    contradiction
  exact ⟨mode, clarification, receipt.nonSupportedNotReady notSupported⟩

theorem degraded_abstain_and_handover_are_distinct
    (receipt : IntentRepositoryObservationReceipt) :
    (receipt.disposition = .partialObservationDegraded →
      receipt.operatingMode = .degradedReadOnly ∧
        receipt.reobservationRequired = true) ∧
    (receipt.disposition = .unsupportedToolchainAbstained →
      receipt.operatingMode = .abstain ∧ receipt.abstained = true) ∧
    (receipt.disposition = .ownershipHandoverRequired →
      receipt.operatingMode = .handover ∧ receipt.handoverRequired = true) := by
  exact ⟨receipt.degradedRoute, receipt.abstainRoute, receipt.handoverRoute⟩

end KUOS.CodeAI.IntentRepositoryObservationEnvelopeV0_1
