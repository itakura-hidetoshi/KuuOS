import KUOS.CodeAI.AutonomousIsolatedCandidateApplicationV0_1

namespace KUOS.CodeAI.AutonomousVerificationExecutionV0_1

inductive Disposition where
  | verificationExecutionCompleted
  | verificationExecutionCompletedWithFailures
  | verificationExecutionAbortedByRuntimeBudget
  deriving DecidableEq, Repr

inductive OperatingMode where
  | boundedIsolatedVerificationExecution
  deriving DecidableEq, Repr

structure AutonomousVerificationExecutionReceipt where
  sourceCandidateReceiptDigest : String
  sourceApplicationReceiptDigest : String
  candidateDigest : String
  patchArtifactDigest : String
  sourceRepositorySnapshotDigest : String
  resultingRepositorySnapshotDigest : String
  verificationPlanDigest : String
  executionRequestDigest : String
  executionPolicyDigest : String
  evidenceBundleDigest : String
  independentVerificationEvidenceDigest : String
  declaredCheckCount : Nat
  passedCheckCount : Nat
  failedCheckCount : Nat
  timedOutCheckCount : Nat
  runnerExceptionCheckCount : Nat
  disposition : Disposition
  operatingMode : OperatingMode
  routeReceiptRecorded : Bool
  sourceCorrespondenceVerified : Bool
  applicationCorrespondenceVerified : Bool
  resultingSnapshotVerified : Bool
  verificationPlanVerified : Bool
  executionPolicyEvaluated : Bool
  boundedRunnerInvocationPerformed : Bool
  independentVerificationEvidenceProjected : Bool
  inputRepositorySnapshotMutated : Bool
  liveRepositoryAccessPerformed : Bool
  liveRepositoryPatchApplied : Bool
  repositoryMutationPerformed : Bool
  gitRefChanged : Bool
  branchCreated : Bool
  commitCreated : Bool
  pushPerformed : Bool
  pullRequestCreated : Bool
  mergePerformed : Bool
  deploymentPerformed : Bool
  secretAccessPerformed : Bool
  networkAccessPerformed : Bool
  selectionAuthorityGranted : Bool
  verificationAuthorityGranted : Bool
  executionAuthorityGranted : Bool
  mergeAuthorityGranted : Bool
  deploymentAuthorityGranted : Bool
  secretAccessAuthorityGranted : Bool
  successorStageAuthorityGranted : Bool
  executionTreatedAsCorrectness : Bool
  testsPassingTreatedAsProof : Bool
  verificationEvidenceTreatedAsMergeAuthority : Bool
  runnerExceptionTreatedAsSuccess : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  checkAccounting : passedCheckCount + failedCheckCount = declaredCheckCount
  timeoutBound : timedOutCheckCount ≤ failedCheckCount
  runnerExceptionBound : runnerExceptionCheckCount ≤ failedCheckCount

structure AutonomousVerificationExecutionReceiptValid
    (receipt : AutonomousVerificationExecutionReceipt) : Prop where
  routeRecorded : receipt.routeReceiptRecorded = true
  sourceCorrespondence : receipt.sourceCorrespondenceVerified = true
  applicationCorrespondence : receipt.applicationCorrespondenceVerified = true
  resultingSnapshot : receipt.resultingSnapshotVerified = true
  planVerified : receipt.verificationPlanVerified = true
  policyEvaluated : receipt.executionPolicyEvaluated = true
  runnerInvoked : receipt.boundedRunnerInvocationPerformed = true
  evidenceProjected : receipt.independentVerificationEvidenceProjected = true
  inputSnapshotImmutable : receipt.inputRepositorySnapshotMutated = false
  noLiveRepositoryAccess : receipt.liveRepositoryAccessPerformed = false
  noLivePatch : receipt.liveRepositoryPatchApplied = false
  noRepositoryMutation : receipt.repositoryMutationPerformed = false
  noGitRefChange : receipt.gitRefChanged = false
  noBranchCreation : receipt.branchCreated = false
  noCommitCreation : receipt.commitCreated = false
  noPush : receipt.pushPerformed = false
  noPullRequest : receipt.pullRequestCreated = false
  noMerge : receipt.mergePerformed = false
  noDeployment : receipt.deploymentPerformed = false
  noSecretAccess : receipt.secretAccessPerformed = false
  noNetworkAccess : receipt.networkAccessPerformed = false
  noSelectionAuthority : receipt.selectionAuthorityGranted = false
  noVerificationAuthority : receipt.verificationAuthorityGranted = false
  noExecutionAuthority : receipt.executionAuthorityGranted = false
  noMergeAuthority : receipt.mergeAuthorityGranted = false
  noDeploymentAuthority : receipt.deploymentAuthorityGranted = false
  noSecretAuthority : receipt.secretAccessAuthorityGranted = false
  noSuccessorAuthority : receipt.successorStageAuthorityGranted = false
  executionNotCorrectness : receipt.executionTreatedAsCorrectness = false
  testsNotProof : receipt.testsPassingTreatedAsProof = false
  evidenceNotMergeAuthority : receipt.verificationEvidenceTreatedAsMergeAuthority = false
  exceptionNotSuccess : receipt.runnerExceptionTreatedAsSuccess = false
  historyReadOnly : receipt.historyReadOnly = true
  futureOnly : receipt.futureOnly = true
  inactiveNow : receipt.activeNow = false

theorem bounded_execution_has_exact_pass_fail_accounting
    (receipt : AutonomousVerificationExecutionReceipt) :
    receipt.passedCheckCount + receipt.failedCheckCount = receipt.declaredCheckCount := by
  exact receipt.checkAccounting

theorem bounded_execution_has_no_live_repository_or_git_effect
    (receipt : AutonomousVerificationExecutionReceipt)
    (valid : AutonomousVerificationExecutionReceiptValid receipt) :
    receipt.inputRepositorySnapshotMutated = false ∧
      receipt.liveRepositoryAccessPerformed = false ∧
      receipt.liveRepositoryPatchApplied = false ∧
      receipt.repositoryMutationPerformed = false ∧
      receipt.gitRefChanged = false ∧
      receipt.branchCreated = false ∧
      receipt.commitCreated = false ∧
      receipt.pushPerformed = false ∧
      receipt.pullRequestCreated = false ∧
      receipt.mergePerformed = false := by
  exact ⟨valid.inputSnapshotImmutable, valid.noLiveRepositoryAccess,
    valid.noLivePatch, valid.noRepositoryMutation, valid.noGitRefChange,
    valid.noBranchCreation, valid.noCommitCreation, valid.noPush,
    valid.noPullRequest, valid.noMerge⟩

theorem bounded_execution_has_no_network_secret_or_deployment_effect
    (receipt : AutonomousVerificationExecutionReceipt)
    (valid : AutonomousVerificationExecutionReceiptValid receipt) :
    receipt.networkAccessPerformed = false ∧
      receipt.secretAccessPerformed = false ∧
      receipt.deploymentPerformed = false := by
  exact ⟨valid.noNetworkAccess, valid.noSecretAccess, valid.noDeployment⟩

theorem bounded_execution_grants_no_successor_authority
    (receipt : AutonomousVerificationExecutionReceipt)
    (valid : AutonomousVerificationExecutionReceiptValid receipt) :
    receipt.selectionAuthorityGranted = false ∧
      receipt.verificationAuthorityGranted = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.mergeAuthorityGranted = false ∧
      receipt.deploymentAuthorityGranted = false ∧
      receipt.secretAccessAuthorityGranted = false ∧
      receipt.successorStageAuthorityGranted = false := by
  exact ⟨valid.noSelectionAuthority, valid.noVerificationAuthority,
    valid.noExecutionAuthority, valid.noMergeAuthority,
    valid.noDeploymentAuthority, valid.noSecretAuthority,
    valid.noSuccessorAuthority⟩

theorem execution_evidence_is_not_correctness_or_merge_authority
    (receipt : AutonomousVerificationExecutionReceipt)
    (valid : AutonomousVerificationExecutionReceiptValid receipt) :
    receipt.executionTreatedAsCorrectness = false ∧
      receipt.testsPassingTreatedAsProof = false ∧
      receipt.verificationEvidenceTreatedAsMergeAuthority = false ∧
      receipt.runnerExceptionTreatedAsSuccess = false := by
  exact ⟨valid.executionNotCorrectness, valid.testsNotProof,
    valid.evidenceNotMergeAuthority, valid.exceptionNotSuccess⟩

theorem timeout_and_runner_exception_counts_are_failed_evidence
    (receipt : AutonomousVerificationExecutionReceipt) :
    receipt.timedOutCheckCount ≤ receipt.failedCheckCount ∧
      receipt.runnerExceptionCheckCount ≤ receipt.failedCheckCount := by
  exact ⟨receipt.timeoutBound, receipt.runnerExceptionBound⟩

end KUOS.CodeAI.AutonomousVerificationExecutionV0_1
