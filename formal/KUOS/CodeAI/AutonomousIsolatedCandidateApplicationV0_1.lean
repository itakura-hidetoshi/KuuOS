import KUOS.CodeAI.AutonomousCandidatePortfolioSelectionV0_1

namespace KUOS.CodeAI.AutonomousIsolatedCandidateApplicationV0_1

inductive Disposition where
  | selectedCandidateIsolatedSnapshotMaterialized
  deriving DecidableEq, Repr

inductive OperatingMode where
  | isolatedMaterializationOnly
  deriving DecidableEq, Repr

structure AutonomousIsolatedCandidateApplicationReceipt where
  sourceSelectionReceiptDigest : String
  sourceCandidateReceiptDigest : String
  selectedCandidateDigest : String
  selectedPatchArtifactDigest : String
  applicationRequestDigest : String
  applicationPolicyDigest : String
  sourceRepositorySnapshotDigest : String
  resultingRepositorySnapshotDigest : String
  sourcePathCount : Nat
  resultingPathCount : Nat
  changedPathCount : Nat
  changedPaths : List String
  addedPaths : List String
  modifiedPaths : List String
  deletedPaths : List String
  disposition : Disposition
  operatingMode : OperatingMode
  routeReceiptRecorded : Bool
  applicationPolicyEvaluated : Bool
  sourceSnapshotVerified : Bool
  selectionCorrespondenceVerified : Bool
  candidateCorrespondenceVerified : Bool
  patchArtifactParsed : Bool
  exactChangedPathAccountingVerified : Bool
  isolatedPatchApplied : Bool
  isolatedSnapshotMaterialized : Bool
  verificationWorkspaceReady : Bool
  inputRepositorySnapshotMutated : Bool
  liveRepositoryPatchApplied : Bool
  liveRepositoryFilesChangedByKernel : Bool
  repositoryMutationPerformed : Bool
  gitRefChanged : Bool
  branchCreated : Bool
  commitCreated : Bool
  pushPerformed : Bool
  pullRequestCreated : Bool
  mergePerformed : Bool
  deploymentPerformed : Bool
  secretAccessPerformed : Bool
  verificationExecuted : Bool
  verificationLeaseIssued : Bool
  executionLeaseIssued : Bool
  successorApplicationAuthorityGranted : Bool
  verificationAuthorityGranted : Bool
  executionAuthorityGranted : Bool
  mergeAuthorityGranted : Bool
  deploymentAuthorityGranted : Bool
  secretAccessAuthorityGranted : Bool
  selectedCandidateTreatedAsCorrect : Bool
  applicationTreatedAsVerification : Bool
  materializationTreatedAsCorrectnessProof : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  changedPathCountExact : changedPathCount = changedPaths.length
  changedPathPartitionBound :
    addedPaths.length + modifiedPaths.length + deletedPaths.length = changedPathCount
  materializedRoute :
    disposition = .selectedCandidateIsolatedSnapshotMaterialized →
      operatingMode = .isolatedMaterializationOnly ∧
        routeReceiptRecorded = true ∧
        applicationPolicyEvaluated = true ∧
        sourceSnapshotVerified = true ∧
        selectionCorrespondenceVerified = true ∧
        candidateCorrespondenceVerified = true ∧
        patchArtifactParsed = true ∧
        exactChangedPathAccountingVerified = true ∧
        isolatedPatchApplied = true ∧
        isolatedSnapshotMaterialized = true ∧
        verificationWorkspaceReady = true

structure AutonomousIsolatedCandidateApplicationReceiptValid
    (receipt : AutonomousIsolatedCandidateApplicationReceipt) : Prop where
  routeRecorded : receipt.routeReceiptRecorded = true
  policyEvaluated : receipt.applicationPolicyEvaluated = true
  sourceVerified : receipt.sourceSnapshotVerified = true
  selectionCorrespondence : receipt.selectionCorrespondenceVerified = true
  candidateCorrespondence : receipt.candidateCorrespondenceVerified = true
  patchParsed : receipt.patchArtifactParsed = true
  exactAccounting : receipt.exactChangedPathAccountingVerified = true
  isolatedApplied : receipt.isolatedPatchApplied = true
  isolatedMaterialized : receipt.isolatedSnapshotMaterialized = true
  workspaceReady : receipt.verificationWorkspaceReady = true
  inputSnapshotImmutable : receipt.inputRepositorySnapshotMutated = false
  noLivePatchApplication : receipt.liveRepositoryPatchApplied = false
  noLiveFileMutation : receipt.liveRepositoryFilesChangedByKernel = false
  noRepositoryMutation : receipt.repositoryMutationPerformed = false
  noGitRefChange : receipt.gitRefChanged = false
  noBranchCreation : receipt.branchCreated = false
  noCommitCreation : receipt.commitCreated = false
  noPush : receipt.pushPerformed = false
  noPullRequest : receipt.pullRequestCreated = false
  noMerge : receipt.mergePerformed = false
  noDeployment : receipt.deploymentPerformed = false
  noSecretAccess : receipt.secretAccessPerformed = false
  noVerificationExecution : receipt.verificationExecuted = false
  noVerificationLease : receipt.verificationLeaseIssued = false
  noExecutionLease : receipt.executionLeaseIssued = false
  noSuccessorApplicationAuthority : receipt.successorApplicationAuthorityGranted = false
  noVerificationAuthority : receipt.verificationAuthorityGranted = false
  noExecutionAuthority : receipt.executionAuthorityGranted = false
  noMergeAuthority : receipt.mergeAuthorityGranted = false
  noDeploymentAuthority : receipt.deploymentAuthorityGranted = false
  noSecretAccessAuthority : receipt.secretAccessAuthorityGranted = false
  candidateNotCorrectness : receipt.selectedCandidateTreatedAsCorrect = false
  applicationNotVerification : receipt.applicationTreatedAsVerification = false
  materializationNotProof : receipt.materializationTreatedAsCorrectnessProof = false
  historyReadOnly : receipt.historyReadOnly = true
  futureOnly : receipt.futureOnly = true
  inactiveNow : receipt.activeNow = false

theorem materialized_route_prepares_one_isolated_workspace
    (receipt : AutonomousIsolatedCandidateApplicationReceipt)
    (route : receipt.disposition = .selectedCandidateIsolatedSnapshotMaterialized) :
    receipt.isolatedPatchApplied = true ∧
      receipt.isolatedSnapshotMaterialized = true ∧
      receipt.verificationWorkspaceReady = true := by
  have h := receipt.materializedRoute route
  exact ⟨h.2.2.2.2.2.2.2.2.1, h.2.2.2.2.2.2.2.2.2.1,
    h.2.2.2.2.2.2.2.2.2.2⟩

theorem isolated_application_has_no_live_repository_or_git_effect
    (receipt : AutonomousIsolatedCandidateApplicationReceipt)
    (valid : AutonomousIsolatedCandidateApplicationReceiptValid receipt) :
    receipt.inputRepositorySnapshotMutated = false ∧
      receipt.liveRepositoryPatchApplied = false ∧
      receipt.liveRepositoryFilesChangedByKernel = false ∧
      receipt.repositoryMutationPerformed = false ∧
      receipt.gitRefChanged = false ∧
      receipt.branchCreated = false ∧
      receipt.commitCreated = false ∧
      receipt.pushPerformed = false ∧
      receipt.pullRequestCreated = false ∧
      receipt.mergePerformed = false := by
  exact ⟨valid.inputSnapshotImmutable, valid.noLivePatchApplication,
    valid.noLiveFileMutation, valid.noRepositoryMutation, valid.noGitRefChange,
    valid.noBranchCreation, valid.noCommitCreation, valid.noPush,
    valid.noPullRequest, valid.noMerge⟩

theorem isolated_application_grants_no_successor_authority
    (receipt : AutonomousIsolatedCandidateApplicationReceipt)
    (valid : AutonomousIsolatedCandidateApplicationReceiptValid receipt) :
    receipt.successorApplicationAuthorityGranted = false ∧
      receipt.verificationAuthorityGranted = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.mergeAuthorityGranted = false ∧
      receipt.deploymentAuthorityGranted = false ∧
      receipt.secretAccessAuthorityGranted = false := by
  exact ⟨valid.noSuccessorApplicationAuthority, valid.noVerificationAuthority,
    valid.noExecutionAuthority, valid.noMergeAuthority,
    valid.noDeploymentAuthority, valid.noSecretAccessAuthority⟩

theorem materialization_is_neither_verification_nor_correctness
    (receipt : AutonomousIsolatedCandidateApplicationReceipt)
    (valid : AutonomousIsolatedCandidateApplicationReceiptValid receipt) :
    receipt.verificationExecuted = false ∧
      receipt.verificationLeaseIssued = false ∧
      receipt.executionLeaseIssued = false ∧
      receipt.selectedCandidateTreatedAsCorrect = false ∧
      receipt.applicationTreatedAsVerification = false ∧
      receipt.materializationTreatedAsCorrectnessProof = false := by
  exact ⟨valid.noVerificationExecution, valid.noVerificationLease,
    valid.noExecutionLease, valid.candidateNotCorrectness,
    valid.applicationNotVerification, valid.materializationNotProof⟩

end KUOS.CodeAI.AutonomousIsolatedCandidateApplicationV0_1
