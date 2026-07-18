import KUOS.CodeAI.CandidatePatchEnvelopeV0_1

namespace KUOS.CodeAI.AutonomousUnifiedDiffCandidatesV0_1

open KUOS.CodeAI.CandidatePatchEnvelopeV0_1

inductive Disposition where
  | autonomousUnifiedDiffCandidatesSynthesized
  | noSupportedUnifiedDiffCandidate
  deriving DecidableEq, Repr

inductive OperatingMode where
  | proposalOnly
  deriving DecidableEq, Repr

structure AutonomousUnifiedDiffCandidatesReceipt where
  sourceObservationReceiptDigest : String
  candidatePolicyDigest : String
  repositorySnapshotDigest : String
  proposalSetDigest : String
  generatedCandidateCount : Nat
  generatedCandidateIds : List String
  generatedCandidateDigests : List String
  generatedPatchArtifactDigests : List String
  rejectedProposalCount : Nat
  rejectionIssues : List String
  disposition : Disposition
  operatingMode : OperatingMode
  routeReceiptRecorded : Bool
  repositorySnapshotReadOnly : Bool
  structuredEditsConsumed : Bool
  unifiedDiffCandidatesGeneratedByKernel : Bool
  candidateRankingGeneratedByKernel : Bool
  candidateSelected : Bool
  verificationLeaseIssued : Bool
  executionLeaseIssued : Bool
  patchApplied : Bool
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
  generatedCandidateTreatedAsCorrect : Bool
  validationTreatedAsCorrectnessProof : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  candidateCountExact : generatedCandidateCount = generatedCandidateIds.length
  candidateDigestCountExact :
    generatedCandidateCount = generatedCandidateDigests.length
  artifactDigestCountExact :
    generatedCandidateCount = generatedPatchArtifactDigests.length
  supportedRoute :
    disposition = .autonomousUnifiedDiffCandidatesSynthesized →
      operatingMode = .proposalOnly ∧
        routeReceiptRecorded = true ∧
        repositorySnapshotReadOnly = true ∧
        structuredEditsConsumed = true ∧
        unifiedDiffCandidatesGeneratedByKernel = true ∧
        candidateRankingGeneratedByKernel = true
  emptyRoute :
    disposition = .noSupportedUnifiedDiffCandidate →
      generatedCandidateCount = 0 ∧
        unifiedDiffCandidatesGeneratedByKernel = false

structure AutonomousUnifiedDiffCandidatesReceiptValid
    (receipt : AutonomousUnifiedDiffCandidatesReceipt) : Prop where
  routeRecorded : receipt.routeReceiptRecorded = true
  snapshotReadOnly : receipt.repositorySnapshotReadOnly = true
  noSelection : receipt.candidateSelected = false
  noVerificationLease : receipt.verificationLeaseIssued = false
  noExecutionLease : receipt.executionLeaseIssued = false
  noPatchApplication : receipt.patchApplied = false
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
  generatedCandidateNotCorrectness :
    receipt.generatedCandidateTreatedAsCorrect = false
  validationNotCorrectnessProof :
    receipt.validationTreatedAsCorrectnessProof = false
  historyReadOnly : receipt.historyReadOnly = true
  futureOnly : receipt.futureOnly = true
  inactiveNow : receipt.activeNow = false

structure AutonomousUnifiedDiffCandidatePortfolio where
  synthesisReceipt : AutonomousUnifiedDiffCandidatesReceipt
  synthesisReceiptValid :
    AutonomousUnifiedDiffCandidatesReceiptValid synthesisReceipt
  candidateReceipts : List CandidatePatchReceipt
  candidateCountBound :
    synthesisReceipt.generatedCandidateCount = candidateReceipts.length
  allCandidatesSupported :
    ∀ receipt ∈ candidateReceipts,
      receipt.disposition = .candidatePatchSupported

theorem candidate_counts_are_exact
    (receipt : AutonomousUnifiedDiffCandidatesReceipt) :
    receipt.generatedCandidateCount = receipt.generatedCandidateIds.length ∧
      receipt.generatedCandidateCount = receipt.generatedCandidateDigests.length ∧
      receipt.generatedCandidateCount =
        receipt.generatedPatchArtifactDigests.length := by
  exact ⟨receipt.candidateCountExact, receipt.candidateDigestCountExact,
    receipt.artifactDigestCountExact⟩

theorem generated_portfolio_has_no_repository_effect
    (receipt : AutonomousUnifiedDiffCandidatesReceipt)
    (valid : AutonomousUnifiedDiffCandidatesReceiptValid receipt) :
    receipt.patchApplied = false ∧
      receipt.repositoryMutationPerformed = false ∧
      receipt.gitRefChanged = false ∧
      receipt.branchCreated = false ∧
      receipt.commitCreated = false ∧
      receipt.pushPerformed = false ∧
      receipt.pullRequestCreated = false ∧
      receipt.mergePerformed = false ∧
      receipt.deploymentPerformed = false ∧
      receipt.secretAccessPerformed = false := by
  exact ⟨valid.noPatchApplication, valid.noRepositoryMutation,
    valid.noGitRefChange, valid.noBranchCreation, valid.noCommitCreation,
    valid.noPush, valid.noPullRequest, valid.noMerge, valid.noDeployment,
    valid.noSecretAccess⟩

theorem ranking_is_not_selection
    (receipt : AutonomousUnifiedDiffCandidatesReceipt)
    (valid : AutonomousUnifiedDiffCandidatesReceiptValid receipt) :
    receipt.candidateSelected = false ∧
      receipt.selectionAuthorityGranted = false ∧
      receipt.executionAuthorityGranted = false := by
  exact ⟨valid.noSelection, valid.noSelectionAuthority,
    valid.noExecutionAuthority⟩

theorem generated_candidates_are_supported_proposals
    (portfolio : AutonomousUnifiedDiffCandidatePortfolio) :
    portfolio.synthesisReceipt.generatedCandidateCount =
        portfolio.candidateReceipts.length ∧
      ∀ receipt ∈ portfolio.candidateReceipts,
        receipt.disposition = .candidatePatchSupported := by
  exact ⟨portfolio.candidateCountBound, portfolio.allCandidatesSupported⟩

theorem synthesis_claims_neither_correctness_nor_authority
    (receipt : AutonomousUnifiedDiffCandidatesReceipt)
    (valid : AutonomousUnifiedDiffCandidatesReceiptValid receipt) :
    receipt.generatedCandidateTreatedAsCorrect = false ∧
      receipt.validationTreatedAsCorrectnessProof = false ∧
      receipt.verificationAuthorityGranted = false ∧
      receipt.mergeAuthorityGranted = false ∧
      receipt.deploymentAuthorityGranted = false ∧
      receipt.secretAccessAuthorityGranted = false := by
  exact ⟨valid.generatedCandidateNotCorrectness,
    valid.validationNotCorrectnessProof, valid.noVerificationAuthority,
    valid.noMergeAuthority, valid.noDeploymentAuthority,
    valid.noSecretAccessAuthority⟩

end KUOS.CodeAI.AutonomousUnifiedDiffCandidatesV0_1
