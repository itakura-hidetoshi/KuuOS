import KUOS.CodeAI.CandidatePatchEnvelopeV0_1

namespace KUOS.CodeAI.IndependentVerificationEnvelopeV0_1

open KUOS.CodeAI.CandidatePatchEnvelopeV0_1

inductive VerificationOutcome where
  | passed
  | failed
  | inconclusive
  deriving DecidableEq, Repr

inductive Disposition where
  | independentVerificationPassed
  | independentVerificationFailed
  | sourceCandidateReceiptRepairRequired
  | verificationProvenanceRepairRequired
  | verifierIndependenceRepairRequired
  | verificationCorrespondenceRepairRequired
  | evidenceIntegrityRepairRequired
  | checkAccountingRepairRequired
  | verificationWindowRepairRequired
  | verificationReplayConflictRejected
  | repositoryMutationRejected
  | authorityEscalationRejected
  | unsupportedVerificationProfileAbstained
  | mandatoryEvidenceHold
  | verificationProtocolRepairRequired
  | verificationOutcomeRepairRequired
  | verificationFindingHandoverRequired
  | verificationInconclusiveHold
  | verificationInconclusiveDegraded
  deriving DecidableEq, Repr

inductive OperatingMode where
  | verifiedPass
  | verifiedFail
  | hold
  | degradedVerification
  | abstain
  | handover
  | rejected
  deriving DecidableEq, Repr

structure IndependentVerificationReceipt where
  sourceCandidateReceiptDigest : String
  candidatePatchDigest : String
  patchArtifactDigest : String
  verificationEvidenceDigest : String
  verificationPolicyDigest : String
  verificationId : String
  verifierId : String
  reviewerId : String
  candidateId : String
  repositoryFullName : String
  sourceCommitSha : String
  resultingCommitSha : String
  declaredCheckCount : Nat
  passedCheckCount : Nat
  failedCheckCount : Nat
  skippedCheckCount : Nat
  disposition : Disposition
  operatingMode : OperatingMode
  verificationOutcome : Option VerificationOutcome
  routeReceiptRecorded : Bool
  verificationCompleted : Bool
  verificationDebtOpen : Bool
  reverificationRequired : Bool
  candidateVerificationPassed : Bool
  candidateVerificationFailed : Bool
  evidenceDegraded : Bool
  clarificationRequired : Bool
  abstained : Bool
  handoverRequired : Bool
  externalIsolatedVerificationReported : Bool
  verificationExecutionPerformedByKernel : Bool
  candidateSelected : Bool
  candidateApplied : Bool
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
  sourceReceiptTreatedAsVerificationAuthority : Bool
  verificationTreatedAsTruth : Bool
  passedTreatedAsCorrectnessProof : Bool
  failedTreatedAsRejectionAuthority : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  sourceCommitUnchanged : resultingCommitSha = sourceCommitSha
  passedRoute :
    disposition = .independentVerificationPassed →
      operatingMode = .verifiedPass ∧
        verificationOutcome = some .passed ∧
        routeReceiptRecorded = true ∧
        verificationCompleted = true ∧
        verificationDebtOpen = false ∧
        reverificationRequired = false ∧
        candidateVerificationPassed = true ∧
        candidateVerificationFailed = false
  failedRoute :
    disposition = .independentVerificationFailed →
      operatingMode = .verifiedFail ∧
        verificationOutcome = some .failed ∧
        routeReceiptRecorded = true ∧
        verificationCompleted = true ∧
        verificationDebtOpen = false ∧
        reverificationRequired = false ∧
        candidateVerificationPassed = false ∧
        candidateVerificationFailed = true
  inconclusiveHoldRoute :
    disposition = .verificationInconclusiveHold →
      operatingMode = .hold ∧
        verificationOutcome = some .inconclusive ∧
        verificationCompleted = true ∧
        verificationDebtOpen = true ∧
        reverificationRequired = true ∧
        clarificationRequired = true
  inconclusiveDegradedRoute :
    disposition = .verificationInconclusiveDegraded →
      operatingMode = .degradedVerification ∧
        verificationOutcome = some .inconclusive ∧
        verificationCompleted = true ∧
        verificationDebtOpen = true ∧
        reverificationRequired = true ∧
        evidenceDegraded = true
  mandatoryHoldRoute :
    disposition = .mandatoryEvidenceHold →
      operatingMode = .hold ∧ clarificationRequired = true
  abstainRoute :
    disposition = .unsupportedVerificationProfileAbstained →
      operatingMode = .abstain ∧ abstained = true
  handoverRoute :
    disposition = .verificationFindingHandoverRequired →
      operatingMode = .handover ∧ handoverRequired = true

structure IndependentVerificationReceiptValid
    (receipt : IndependentVerificationReceipt) : Prop where
  routeRecorded : receipt.routeReceiptRecorded = true
  noKernelExecution : receipt.verificationExecutionPerformedByKernel = false
  noSelection : receipt.candidateSelected = false
  noApplication : receipt.candidateApplied = false
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
  sourceNotVerificationAuthority :
    receipt.sourceReceiptTreatedAsVerificationAuthority = false
  verificationNotTruth : receipt.verificationTreatedAsTruth = false
  passedNotCorrectness : receipt.passedTreatedAsCorrectnessProof = false
  failedNotRejectionAuthority :
    receipt.failedTreatedAsRejectionAuthority = false
  historyReadOnly : receipt.historyReadOnly = true
  futureOnly : receipt.futureOnly = true
  inactiveNow : receipt.activeNow = false

structure IndependentVerificationEnvelope where
  sourceReceipt : CandidatePatchReceipt
  sourceReceiptValid : CandidatePatchReceiptValid sourceReceipt
  sourceReceiptSupported : sourceReceipt.disposition = .candidatePatchSupported
  receipt : IndependentVerificationReceipt
  receiptValid : IndependentVerificationReceiptValid receipt
  candidateBound : receipt.candidatePatchDigest = sourceReceipt.candidatePatchDigest
  patchBound : receipt.patchArtifactDigest = sourceReceipt.patchArtifactDigest
  repositoryBound : receipt.repositoryFullName = sourceReceipt.repositoryFullName
  sourceCommitBound : receipt.sourceCommitSha = sourceReceipt.sourceCommitSha

theorem source_commit_is_preserved (receipt : IndependentVerificationReceipt) :
    receipt.resultingCommitSha = receipt.sourceCommitSha := by
  exact receipt.sourceCommitUnchanged

theorem verification_is_bound_to_supported_candidate
    (envelope : IndependentVerificationEnvelope) :
    envelope.receipt.candidatePatchDigest =
        envelope.sourceReceipt.candidatePatchDigest ∧
      envelope.receipt.patchArtifactDigest =
        envelope.sourceReceipt.patchArtifactDigest ∧
      envelope.receipt.repositoryFullName =
        envelope.sourceReceipt.repositoryFullName ∧
      envelope.receipt.sourceCommitSha =
        envelope.sourceReceipt.sourceCommitSha ∧
      envelope.sourceReceipt.disposition = .candidatePatchSupported := by
  exact ⟨envelope.candidateBound, envelope.patchBound,
    envelope.repositoryBound, envelope.sourceCommitBound,
    envelope.sourceReceiptSupported⟩

theorem passed_closes_debt_without_correctness_authority
    (receipt : IndependentVerificationReceipt)
    (valid : IndependentVerificationReceiptValid receipt)
    (route : receipt.disposition = .independentVerificationPassed) :
    receipt.operatingMode = .verifiedPass ∧
      receipt.verificationOutcome = some .passed ∧
      receipt.verificationCompleted = true ∧
      receipt.verificationDebtOpen = false ∧
      receipt.candidateVerificationPassed = true ∧
      receipt.passedTreatedAsCorrectnessProof = false ∧
      receipt.executionAuthorityGranted = false := by
  rcases receipt.passedRoute route with
    ⟨mode, outcome, _, completed, debt, _, passed, _⟩
  exact ⟨mode, outcome, completed, debt, passed,
    valid.passedNotCorrectness, valid.noExecutionAuthority⟩

theorem failed_closes_debt_without_rejection_authority
    (receipt : IndependentVerificationReceipt)
    (valid : IndependentVerificationReceiptValid receipt)
    (route : receipt.disposition = .independentVerificationFailed) :
    receipt.operatingMode = .verifiedFail ∧
      receipt.verificationOutcome = some .failed ∧
      receipt.verificationCompleted = true ∧
      receipt.verificationDebtOpen = false ∧
      receipt.candidateVerificationFailed = true ∧
      receipt.failedTreatedAsRejectionAuthority = false ∧
      receipt.candidateApplied = false := by
  rcases receipt.failedRoute route with
    ⟨mode, outcome, _, completed, debt, _, _, failed⟩
  exact ⟨mode, outcome, completed, debt, failed,
    valid.failedNotRejectionAuthority, valid.noApplication⟩

theorem inconclusive_preserves_debt
    (receipt : IndependentVerificationReceipt) :
    (receipt.disposition = .verificationInconclusiveHold →
      receipt.verificationOutcome = some .inconclusive ∧
        receipt.verificationDebtOpen = true ∧
        receipt.reverificationRequired = true) ∧
    (receipt.disposition = .verificationInconclusiveDegraded →
      receipt.verificationOutcome = some .inconclusive ∧
        receipt.verificationDebtOpen = true ∧
        receipt.reverificationRequired = true) := by
  constructor
  · intro route
    rcases receipt.inconclusiveHoldRoute route with
      ⟨_, outcome, _, debt, reverify, _⟩
    exact ⟨outcome, debt, reverify⟩
  · intro route
    rcases receipt.inconclusiveDegradedRoute route with
      ⟨_, outcome, _, debt, reverify, _⟩
    exact ⟨outcome, debt, reverify⟩

theorem verification_has_no_repository_effect
    (receipt : IndependentVerificationReceipt)
    (valid : IndependentVerificationReceiptValid receipt) :
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

theorem verification_grants_no_authority
    (receipt : IndependentVerificationReceipt)
    (valid : IndependentVerificationReceiptValid receipt) :
    receipt.selectionAuthorityGranted = false ∧
      receipt.verificationAuthorityGranted = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.mergeAuthorityGranted = false ∧
      receipt.deploymentAuthorityGranted = false ∧
      receipt.secretAccessAuthorityGranted = false := by
  exact ⟨valid.noSelectionAuthority, valid.noVerificationAuthority,
    valid.noExecutionAuthority, valid.noMergeAuthority,
    valid.noDeploymentAuthority, valid.noSecretAccessAuthority⟩

theorem verification_claims_neither_truth_nor_outcome_authority
    (receipt : IndependentVerificationReceipt)
    (valid : IndependentVerificationReceiptValid receipt) :
    receipt.sourceReceiptTreatedAsVerificationAuthority = false ∧
      receipt.verificationTreatedAsTruth = false ∧
      receipt.passedTreatedAsCorrectnessProof = false ∧
      receipt.failedTreatedAsRejectionAuthority = false := by
  exact ⟨valid.sourceNotVerificationAuthority, valid.verificationNotTruth,
    valid.passedNotCorrectness, valid.failedNotRejectionAuthority⟩

theorem hold_degrade_abstain_and_handover_are_distinct
    (receipt : IndependentVerificationReceipt) :
    (receipt.disposition = .mandatoryEvidenceHold →
      receipt.operatingMode = .hold ∧ receipt.clarificationRequired = true) ∧
    (receipt.disposition = .verificationInconclusiveDegraded →
      receipt.operatingMode = .degradedVerification ∧
        receipt.evidenceDegraded = true) ∧
    (receipt.disposition = .unsupportedVerificationProfileAbstained →
      receipt.operatingMode = .abstain ∧ receipt.abstained = true) ∧
    (receipt.disposition = .verificationFindingHandoverRequired →
      receipt.operatingMode = .handover ∧ receipt.handoverRequired = true) := by
  exact ⟨receipt.mandatoryHoldRoute,
    fun route => ⟨(receipt.inconclusiveDegradedRoute route).1,
      (receipt.inconclusiveDegradedRoute route).2.2.2.2.2⟩,
    receipt.abstainRoute, receipt.handoverRoute⟩

end KUOS.CodeAI.IndependentVerificationEnvelopeV0_1
