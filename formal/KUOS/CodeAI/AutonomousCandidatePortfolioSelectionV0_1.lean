import KUOS.CodeAI.AutonomousUnifiedDiffCandidatesV0_1

namespace KUOS.CodeAI.AutonomousCandidatePortfolioSelectionV0_1

open KUOS.CodeAI.AutonomousUnifiedDiffCandidatesV0_1

inductive Disposition where
  | candidateSelectedForIndependentVerification
  | noAdmissibleCandidateForIndependentVerification
  deriving DecidableEq, Repr

inductive OperatingMode where
  | selectionOnly
  deriving DecidableEq, Repr

structure AutonomousCandidatePortfolioSelectionReceipt where
  sourcePortfolioReceiptDigest : String
  selectionRequestDigest : String
  selectionPolicyDigest : String
  evaluatedCandidateCount : Nat
  evaluatedCandidateIds : List String
  admissibleCandidateCount : Nat
  admissibleCandidateIds : List String
  selectedCandidateCount : Nat
  selectedCandidateIds : List String
  disposition : Disposition
  operatingMode : OperatingMode
  routeReceiptRecorded : Bool
  selectionPolicyEvaluated : Bool
  candidateSelected : Bool
  selectedForIndependentVerification : Bool
  selectionPerformedByKernel : Bool
  selectionAuthorityConsumedByKernel : Bool
  successorSelectionAuthorityGranted : Bool
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
  verificationAuthorityGranted : Bool
  executionAuthorityGranted : Bool
  mergeAuthorityGranted : Bool
  deploymentAuthorityGranted : Bool
  secretAccessAuthorityGranted : Bool
  selectedCandidateTreatedAsCorrect : Bool
  rankingTreatedAsCorrectnessProof : Bool
  selectionTreatedAsVerification : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  evaluatedCountExact : evaluatedCandidateCount = evaluatedCandidateIds.length
  admissibleCountExact : admissibleCandidateCount = admissibleCandidateIds.length
  selectedCountExact : selectedCandidateCount = selectedCandidateIds.length
  selectedAtMostOne : selectedCandidateCount ≤ 1
  admissibleBound : admissibleCandidateCount ≤ evaluatedCandidateCount
  selectedBound : selectedCandidateCount ≤ admissibleCandidateCount
  selectedRoute :
    disposition = .candidateSelectedForIndependentVerification →
      operatingMode = .selectionOnly ∧
        routeReceiptRecorded = true ∧
        selectionPolicyEvaluated = true ∧
        selectedCandidateCount = 1 ∧
        candidateSelected = true ∧
        selectedForIndependentVerification = true ∧
        selectionPerformedByKernel = true ∧
        selectionAuthorityConsumedByKernel = true
  emptyRoute :
    disposition = .noAdmissibleCandidateForIndependentVerification →
      admissibleCandidateCount = 0 ∧
        selectedCandidateCount = 0 ∧
        candidateSelected = false ∧
        selectionPerformedByKernel = false

structure AutonomousCandidatePortfolioSelectionReceiptValid
    (receipt : AutonomousCandidatePortfolioSelectionReceipt) : Prop where
  routeRecorded : receipt.routeReceiptRecorded = true
  policyEvaluated : receipt.selectionPolicyEvaluated = true
  noSuccessorSelectionAuthority :
    receipt.successorSelectionAuthorityGranted = false
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
  noVerificationAuthority : receipt.verificationAuthorityGranted = false
  noExecutionAuthority : receipt.executionAuthorityGranted = false
  noMergeAuthority : receipt.mergeAuthorityGranted = false
  noDeploymentAuthority : receipt.deploymentAuthorityGranted = false
  noSecretAccessAuthority : receipt.secretAccessAuthorityGranted = false
  selectedCandidateNotCorrectness :
    receipt.selectedCandidateTreatedAsCorrect = false
  rankingNotCorrectnessProof :
    receipt.rankingTreatedAsCorrectnessProof = false
  selectionNotVerification : receipt.selectionTreatedAsVerification = false
  historyReadOnly : receipt.historyReadOnly = true
  futureOnly : receipt.futureOnly = true
  inactiveNow : receipt.activeNow = false

structure AutonomousCandidatePortfolioSelection where
  sourcePortfolio : AutonomousUnifiedDiffCandidatePortfolio
  selectionReceipt : AutonomousCandidatePortfolioSelectionReceipt
  selectionReceiptValid :
    AutonomousCandidatePortfolioSelectionReceiptValid selectionReceipt
  evaluatedPortfolioBound :
    selectionReceipt.evaluatedCandidateCount =
      sourcePortfolio.synthesisReceipt.generatedCandidateCount

 theorem selected_route_is_singleton
    (receipt : AutonomousCandidatePortfolioSelectionReceipt)
    (route : receipt.disposition =
      .candidateSelectedForIndependentVerification) :
    receipt.selectedCandidateCount = 1 ∧
      receipt.candidateSelected = true ∧
      receipt.selectedForIndependentVerification = true := by
  have h := receipt.selectedRoute route
  exact ⟨h.2.2.2.1, h.2.2.2.2.1, h.2.2.2.2.2.1⟩

theorem selected_count_is_bounded
    (receipt : AutonomousCandidatePortfolioSelectionReceipt) :
    receipt.selectedCandidateCount ≤ receipt.evaluatedCandidateCount := by
  exact Nat.le_trans receipt.selectedBound receipt.admissibleBound

theorem no_admissible_candidate_selects_none
    (receipt : AutonomousCandidatePortfolioSelectionReceipt)
    (route : receipt.disposition =
      .noAdmissibleCandidateForIndependentVerification) :
    receipt.admissibleCandidateCount = 0 ∧
      receipt.selectedCandidateCount = 0 ∧
      receipt.candidateSelected = false := by
  have h := receipt.emptyRoute route
  exact ⟨h.1, h.2.1, h.2.2.1⟩

theorem selection_grants_no_successor_authority
    (receipt : AutonomousCandidatePortfolioSelectionReceipt)
    (valid : AutonomousCandidatePortfolioSelectionReceiptValid receipt) :
    receipt.successorSelectionAuthorityGranted = false ∧
      receipt.verificationAuthorityGranted = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.mergeAuthorityGranted = false ∧
      receipt.deploymentAuthorityGranted = false ∧
      receipt.secretAccessAuthorityGranted = false := by
  exact ⟨valid.noSuccessorSelectionAuthority, valid.noVerificationAuthority,
    valid.noExecutionAuthority, valid.noMergeAuthority,
    valid.noDeploymentAuthority, valid.noSecretAccessAuthority⟩

theorem selection_has_no_repository_effect
    (receipt : AutonomousCandidatePortfolioSelectionReceipt)
    (valid : AutonomousCandidatePortfolioSelectionReceiptValid receipt) :
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

theorem selected_candidate_is_neither_correct_nor_verified
    (receipt : AutonomousCandidatePortfolioSelectionReceipt)
    (valid : AutonomousCandidatePortfolioSelectionReceiptValid receipt) :
    receipt.selectedCandidateTreatedAsCorrect = false ∧
      receipt.rankingTreatedAsCorrectnessProof = false ∧
      receipt.selectionTreatedAsVerification = false ∧
      receipt.verificationLeaseIssued = false ∧
      receipt.executionLeaseIssued = false := by
  exact ⟨valid.selectedCandidateNotCorrectness,
    valid.rankingNotCorrectnessProof, valid.selectionNotVerification,
    valid.noVerificationLease, valid.noExecutionLease⟩

end KUOS.CodeAI.AutonomousCandidatePortfolioSelectionV0_1
