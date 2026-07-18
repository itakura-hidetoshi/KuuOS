import KUOS.CodeAI.IntentRepositoryObservationEnvelopeV0_1

namespace KUOS.CodeAI.CandidatePatchEnvelopeV0_1

open KUOS.CodeAI.IntentRepositoryObservationEnvelopeV0_1

inductive Disposition where
  | candidatePatchSupported
  | sourceObservationReceiptRepairRequired
  | candidateProvenanceRepairRequired
  | repositoryCorrespondenceRepairRequired
  | patchArtifactRepairRequired
  | candidateWindowRepairRequired
  | candidateReplayConflictRejected
  | repositoryMutationRejected
  | authorityEscalationRejected
  | unsupportedPatchFormatAbstained
  | patchSyntaxRepairRequired
  | pathAccountingRepairRequired
  | candidateScopeViolationRejected
  | candidateBudgetExceededRejected
  | candidateClarificationHold
  | riskOwnershipHandoverRequired
  | candidateEvidenceRepairRequired
  | candidateEvidenceDegraded
  deriving DecidableEq, Repr

inductive OperatingMode where
  | proposalOnly
  | hold
  | degradedProposal
  | abstain
  | handover
  | rejected
  deriving DecidableEq, Repr

structure CandidatePatchReceipt where
  sourceObservationReceiptDigest : String
  candidatePatchDigest : String
  candidatePolicyDigest : String
  intentPacketDigest : String
  candidateId : String
  candidateRevision : String
  producerId : String
  repositoryFullName : String
  sourceCommitSha : String
  resultingCommitSha : String
  patchFormat : String
  patchArtifactDigest : String
  patchSizeBytes : Nat
  changedPathCount : Nat
  addedPathCount : Nat
  modifiedPathCount : Nat
  deletedPathCount : Nat
  renamedPathCount : Nat
  declaredChangeCount : Nat
  disposition : Disposition
  operatingMode : OperatingMode
  routeReceiptRecorded : Bool
  candidatePatchArtifactParsed : Bool
  candidatePatchRecorded : Bool
  candidatePatchReady : Bool
  clarificationRequired : Bool
  evidenceDegraded : Bool
  abstained : Bool
  handoverRequired : Bool
  patchCandidateOnly : Bool
  candidateGeneratedByKernel : Bool
  candidateSelected : Bool
  verificationLeaseIssued : Bool
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
  verificationAuthorityGranted : Bool
  executionAuthorityGranted : Bool
  mergeAuthorityGranted : Bool
  deploymentAuthorityGranted : Bool
  secretAccessAuthorityGranted : Bool
  sourceReceiptTreatedAsSuccessorAuthority : Bool
  candidateTreatedAsCorrect : Bool
  validationTreatedAsCorrectnessProof : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  changedPathAccounting : changedPathCount = declaredChangeCount
  sourceCommitUnchanged : resultingCommitSha = sourceCommitSha
  supportedRoute :
    disposition = .candidatePatchSupported →
      operatingMode = .proposalOnly ∧
        routeReceiptRecorded = true ∧
        candidatePatchArtifactParsed = true ∧
        candidatePatchRecorded = true ∧
        candidatePatchReady = true ∧
        clarificationRequired = false ∧
        evidenceDegraded = false ∧
        abstained = false ∧
        handoverRequired = false
  nonSupportedNotReady :
    disposition ≠ .candidatePatchSupported → candidatePatchReady = false
  holdRoute :
    disposition = .candidateClarificationHold →
      operatingMode = .hold ∧ clarificationRequired = true
  degradedRoute :
    disposition = .candidateEvidenceDegraded →
      operatingMode = .degradedProposal ∧ evidenceDegraded = true
  abstainRoute :
    disposition = .unsupportedPatchFormatAbstained →
      operatingMode = .abstain ∧ abstained = true
  handoverRoute :
    disposition = .riskOwnershipHandoverRequired →
      operatingMode = .handover ∧ handoverRequired = true

structure CandidatePatchReceiptValid (receipt : CandidatePatchReceipt) : Prop where
  routeRecorded : receipt.routeReceiptRecorded = true
  candidateRecorded : receipt.candidatePatchRecorded = true
  proposalOnly : receipt.patchCandidateOnly = true
  noKernelGeneration : receipt.candidateGeneratedByKernel = false
  noSelection : receipt.candidateSelected = false
  noVerificationLease : receipt.verificationLeaseIssued = false
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
  noVerificationAuthority : receipt.verificationAuthorityGranted = false
  noExecutionAuthority : receipt.executionAuthorityGranted = false
  noMergeAuthority : receipt.mergeAuthorityGranted = false
  noDeploymentAuthority : receipt.deploymentAuthorityGranted = false
  noSecretAccessAuthority : receipt.secretAccessAuthorityGranted = false
  sourceReceiptNotAuthority :
    receipt.sourceReceiptTreatedAsSuccessorAuthority = false
  candidateNotCorrectness : receipt.candidateTreatedAsCorrect = false
  validationNotCorrectnessProof :
    receipt.validationTreatedAsCorrectnessProof = false
  historyReadOnly : receipt.historyReadOnly = true
  futureOnly : receipt.futureOnly = true
  inactiveNow : receipt.activeNow = false

structure CandidatePatchEnvelope where
  sourceReceipt : IntentRepositoryObservationReceipt
  sourceReceiptValid : IntentRepositoryObservationReceiptValid sourceReceipt
  sourceReceiptSupported :
    sourceReceipt.disposition = .intentRepositoryObservationSupported
  receipt : CandidatePatchReceipt
  receiptValid : CandidatePatchReceiptValid receipt
  intentBound : receipt.intentPacketDigest = sourceReceipt.intentPacketDigest
  repositoryBound : receipt.repositoryFullName = sourceReceipt.repositoryFullName
  sourceCommitBound : receipt.sourceCommitSha = sourceReceipt.sourceCommitSha

theorem changed_paths_are_exact (receipt : CandidatePatchReceipt) :
    receipt.changedPathCount = receipt.declaredChangeCount := by
  exact receipt.changedPathAccounting

theorem source_commit_is_preserved (receipt : CandidatePatchReceipt) :
    receipt.resultingCommitSha = receipt.sourceCommitSha := by
  exact receipt.sourceCommitUnchanged

theorem candidate_is_bound_to_supported_source
    (envelope : CandidatePatchEnvelope) :
    envelope.receipt.intentPacketDigest =
        envelope.sourceReceipt.intentPacketDigest ∧
      envelope.receipt.repositoryFullName =
        envelope.sourceReceipt.repositoryFullName ∧
      envelope.receipt.sourceCommitSha =
        envelope.sourceReceipt.sourceCommitSha ∧
      envelope.sourceReceipt.disposition =
        .intentRepositoryObservationSupported := by
  exact ⟨envelope.intentBound, envelope.repositoryBound,
    envelope.sourceCommitBound, envelope.sourceReceiptSupported⟩

theorem supported_is_proposal_only_and_not_selected
    (receipt : CandidatePatchReceipt)
    (valid : CandidatePatchReceiptValid receipt)
    (supported : receipt.disposition = .candidatePatchSupported) :
    receipt.operatingMode = .proposalOnly ∧
      receipt.candidatePatchArtifactParsed = true ∧
      receipt.candidatePatchRecorded = true ∧
      receipt.candidatePatchReady = true ∧
      receipt.patchCandidateOnly = true ∧
      receipt.candidateSelected = false ∧
      receipt.verificationLeaseIssued = false ∧
      receipt.executionLeaseIssued = false := by
  rcases receipt.supportedRoute supported with
    ⟨mode, _, parsed, recorded, ready, _, _, _, _⟩
  exact ⟨mode, parsed, recorded, ready, valid.proposalOnly,
    valid.noSelection, valid.noVerificationLease, valid.noExecutionLease⟩

theorem candidate_has_no_repository_effect
    (receipt : CandidatePatchReceipt)
    (valid : CandidatePatchReceiptValid receipt) :
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

theorem candidate_grants_no_authority
    (receipt : CandidatePatchReceipt)
    (valid : CandidatePatchReceiptValid receipt) :
    receipt.selectionAuthorityGranted = false ∧
      receipt.verificationAuthorityGranted = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.mergeAuthorityGranted = false ∧
      receipt.deploymentAuthorityGranted = false ∧
      receipt.secretAccessAuthorityGranted = false := by
  exact ⟨valid.noSelectionAuthority, valid.noVerificationAuthority,
    valid.noExecutionAuthority, valid.noMergeAuthority,
    valid.noDeploymentAuthority, valid.noSecretAccessAuthority⟩

theorem candidate_claims_neither_successor_authority_nor_correctness
    (receipt : CandidatePatchReceipt)
    (valid : CandidatePatchReceiptValid receipt) :
    receipt.sourceReceiptTreatedAsSuccessorAuthority = false ∧
      receipt.candidateTreatedAsCorrect = false ∧
      receipt.validationTreatedAsCorrectnessProof = false := by
  exact ⟨valid.sourceReceiptNotAuthority, valid.candidateNotCorrectness,
    valid.validationNotCorrectnessProof⟩

theorem hold_is_first_class
    (receipt : CandidatePatchReceipt)
    (route : receipt.disposition = .candidateClarificationHold) :
    receipt.operatingMode = .hold ∧
      receipt.clarificationRequired = true ∧
      receipt.candidatePatchReady = false := by
  rcases receipt.holdRoute route with ⟨mode, clarification⟩
  have notSupported : receipt.disposition ≠ .candidatePatchSupported := by
    intro contradiction
    rw [route] at contradiction
    contradiction
  exact ⟨mode, clarification, receipt.nonSupportedNotReady notSupported⟩

theorem degraded_abstain_and_handover_are_distinct
    (receipt : CandidatePatchReceipt) :
    (receipt.disposition = .candidateEvidenceDegraded →
      receipt.operatingMode = .degradedProposal ∧
        receipt.evidenceDegraded = true) ∧
    (receipt.disposition = .unsupportedPatchFormatAbstained →
      receipt.operatingMode = .abstain ∧ receipt.abstained = true) ∧
    (receipt.disposition = .riskOwnershipHandoverRequired →
      receipt.operatingMode = .handover ∧
        receipt.handoverRequired = true) := by
  exact ⟨receipt.degradedRoute, receipt.abstainRoute,
    receipt.handoverRoute⟩

end KUOS.CodeAI.CandidatePatchEnvelopeV0_1
