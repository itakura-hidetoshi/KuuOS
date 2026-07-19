import KUOS.CodeAI.RepairCycleAdmissionConsumptionV0_1
import KUOS.CodeAI.BoundedRepairCycleOrchestrationV0_1

namespace KUOS.CodeAI.AdmissionGatedBoundedRepairCycleExecutionV0_1

inductive Disposition where
  | admittedRepairCycleVerificationPassed
  | admittedRepairCycleVerificationFailed
  | admittedRepairCycleAbortedByBudget
  deriving DecidableEq, Repr

inductive OperatingMode where
  | admissionGatedBoundedRepairCycleExecution
  deriving DecidableEq, Repr

structure ExecutionBudget where
  candidate : Nat
  providerCall : Nat
  command : Nat
  timeoutSeconds : Nat
  outputBytes : Nat
  deriving DecidableEq, Repr

structure ExecutionRegistryTransition where
  sourceRevision : Nat
  nextRevision : Nat
  sourceConsumedInputCount : Nat
  nextConsumedInputCount : Nat
  sourceLastExecutedCycleIndex : Nat
  executedCycleIndex : Nat
  inputDigestFresh : Bool
  nonceDigestFresh : Bool
  revisionStep : nextRevision = sourceRevision + 1
  countStep : nextConsumedInputCount = sourceConsumedInputCount + 1
  cycleMonotone : sourceLastExecutedCycleIndex < executedCycleIndex

structure AdmissionGatedExecutionReceipt where
  sourceAdmissionConsumptionReceiptDigest : String
  sourceExecutionInputDigest : String
  sourceConsumptionRegistryDigest : String
  sourceExecutionRegistryDigest : String
  nextExecutionRegistryDigest : String
  sourceRepairReceiptDigest : String
  sourceRegenerationReceiptDigest : String
  repairCandidateSetDigest : String
  verificationPlanDigest : String
  boundedCycleReceiptDigest : String
  selectedCandidateDigest : String
  cycleIndex : Nat
  maximumBudget : ExecutionBudget
  usedBudget : ExecutionBudget
  unusedBudget : ExecutionBudget
  disposition : Disposition
  operatingMode : OperatingMode
  routeReceiptRecorded : Bool
  admissionConsumptionReceiptVerified : Bool
  executionInputVerified : Bool
  executionInputConsumed : Bool
  executionInputReplayExcluded : Bool
  cycleExecutionNonceReplayExcluded : Bool
  consumptionRegistryCorrespondenceVerified : Bool
  executionRegistryTransitionVerified : Bool
  exactCycleLineageVerified : Bool
  exactRepositoryCommitLineageVerified : Bool
  exactRepairRegenerationCandidateLineageVerified : Bool
  exactVerificationPlanLineageVerified : Bool
  failedCandidateExcludedFromReselection : Bool
  allowedStageSetVerified : Bool
  candidateBudgetVerified : Bool
  providerCallBudgetVerified : Bool
  commandBudgetVerified : Bool
  timeoutBudgetVerified : Bool
  outputBudgetVerified : Bool
  providerInvoked : Bool
  runnerInvoked : Bool
  candidateGenerated : Bool
  candidateSelected : Bool
  isolatedPatchApplicationPerformed : Bool
  verificationExecuted : Bool
  cycleExecutionPerformed : Bool
  cycleCompleted : Bool
  cycleVerificationPassed : Bool
  cycleAbortedByBudget : Bool
  nextCycleEligible : Bool
  nextCycleAuthorityGranted : Bool
  inputRepositorySnapshotMutated : Bool
  isolatedRepositorySnapshotUpdated : Bool
  liveRepositoryPatchApplied : Bool
  repositoryMutationPerformed : Bool
  gitRefChanged : Bool
  branchCreated : Bool
  commitCreated : Bool
  pushPerformed : Bool
  pullRequestCreated : Bool
  networkAccessPerformed : Bool
  secretAccessPerformed : Bool
  mergePerformed : Bool
  deploymentPerformed : Bool
  mergeAuthorityGranted : Bool
  deploymentAuthorityGranted : Bool
  generalSuccessorStageAuthorityGranted : Bool
  executionInputConsumptionTreatedAsCorrectness : Bool
  admittedExecutionTreatedAsSuccessfulRepair : Bool
  cyclePassTreatedAsProof : Bool
  cycleFailureTreatedAsRequiredRepair : Bool
  providerOutputTreatedAsTrustedPatch : Bool
  candidateSelectionTreatedAsCorrectness : Bool
  isolatedApplicationTreatedAsLiveMutation : Bool
  verificationEvidenceTreatedAsMergeAuthority : Bool
  unusedBudgetTreatedAsReusableAuthority : Bool
  completedCycleTreatedAsUnrestrictedContinuation : Bool
  executionReceiptTreatedAsGitAuthority : Bool
  executionReceiptTreatedAsDeploymentAuthority : Bool
  executionReceiptTreatedAsGeneralSuccessorAuthority : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  candidateConservation :
    usedBudget.candidate + unusedBudget.candidate = maximumBudget.candidate
  providerCallConservation :
    usedBudget.providerCall + unusedBudget.providerCall = maximumBudget.providerCall
  commandConservation :
    usedBudget.command + unusedBudget.command = maximumBudget.command
  timeoutConservation :
    usedBudget.timeoutSeconds + unusedBudget.timeoutSeconds = maximumBudget.timeoutSeconds
  outputConservation :
    usedBudget.outputBytes + unusedBudget.outputBytes = maximumBudget.outputBytes

structure AdmissionGatedExecutionReceiptValid
    (receipt : AdmissionGatedExecutionReceipt) : Prop where
  routeRecorded : receipt.routeReceiptRecorded = true
  admissionVerified : receipt.admissionConsumptionReceiptVerified = true
  inputVerified : receipt.executionInputVerified = true
  inputConsumed : receipt.executionInputConsumed = true
  noInputReplay : receipt.executionInputReplayExcluded = true
  noNonceReplay : receipt.cycleExecutionNonceReplayExcluded = true
  consumptionRegistryCorrespondence :
    receipt.consumptionRegistryCorrespondenceVerified = true
  registryTransition : receipt.executionRegistryTransitionVerified = true
  cycleLineage : receipt.exactCycleLineageVerified = true
  repositoryCommitLineage : receipt.exactRepositoryCommitLineageVerified = true
  repairRegenerationCandidateLineage :
    receipt.exactRepairRegenerationCandidateLineageVerified = true
  verificationPlanLineage : receipt.exactVerificationPlanLineageVerified = true
  failedCandidateExcluded : receipt.failedCandidateExcludedFromReselection = true
  stageSet : receipt.allowedStageSetVerified = true
  candidateBudget : receipt.candidateBudgetVerified = true
  providerBudget : receipt.providerCallBudgetVerified = true
  commandBudget : receipt.commandBudgetVerified = true
  timeoutBudget : receipt.timeoutBudgetVerified = true
  outputBudget : receipt.outputBudgetVerified = true
  providerCalled : receipt.providerInvoked = true
  candidateProduced : receipt.candidateGenerated = true
  selected : receipt.candidateSelected = true
  isolatedApplied : receipt.isolatedPatchApplicationPerformed = true
  verificationRun : receipt.verificationExecuted = true
  cycleRun : receipt.cycleExecutionPerformed = true
  cycleDone : receipt.cycleCompleted = true
  noNextAuthority : receipt.nextCycleAuthorityGranted = false
  noInputMutation : receipt.inputRepositorySnapshotMutated = false
  isolatedSnapshotOnly : receipt.isolatedRepositorySnapshotUpdated = true
  noLivePatch : receipt.liveRepositoryPatchApplied = false
  noRepositoryMutation : receipt.repositoryMutationPerformed = false
  noGitRef : receipt.gitRefChanged = false
  noBranch : receipt.branchCreated = false
  noCommit : receipt.commitCreated = false
  noPush : receipt.pushPerformed = false
  noPullRequest : receipt.pullRequestCreated = false
  noNetwork : receipt.networkAccessPerformed = false
  noSecret : receipt.secretAccessPerformed = false
  noMerge : receipt.mergePerformed = false
  noDeployment : receipt.deploymentPerformed = false
  noMergeAuthority : receipt.mergeAuthorityGranted = false
  noDeploymentAuthority : receipt.deploymentAuthorityGranted = false
  noGeneralAuthority : receipt.generalSuccessorStageAuthorityGranted = false
  inputConsumptionNotCorrectness :
    receipt.executionInputConsumptionTreatedAsCorrectness = false
  admittedExecutionNotSuccessfulRepair :
    receipt.admittedExecutionTreatedAsSuccessfulRepair = false
  passNotProof : receipt.cyclePassTreatedAsProof = false
  failureNotRequiredRepair : receipt.cycleFailureTreatedAsRequiredRepair = false
  providerOutputNotTrustedPatch : receipt.providerOutputTreatedAsTrustedPatch = false
  selectionNotCorrectness : receipt.candidateSelectionTreatedAsCorrectness = false
  isolatedNotLiveMutation : receipt.isolatedApplicationTreatedAsLiveMutation = false
  evidenceNotMergeAuthority : receipt.verificationEvidenceTreatedAsMergeAuthority = false
  unusedBudgetNotAuthority : receipt.unusedBudgetTreatedAsReusableAuthority = false
  completedCycleNotUnrestricted :
    receipt.completedCycleTreatedAsUnrestrictedContinuation = false
  receiptNotGitAuthority : receipt.executionReceiptTreatedAsGitAuthority = false
  receiptNotDeploymentAuthority :
    receipt.executionReceiptTreatedAsDeploymentAuthority = false
  receiptNotGeneralAuthority :
    receipt.executionReceiptTreatedAsGeneralSuccessorAuthority = false
  historyReadOnly : receipt.historyReadOnly = true
  futureOnly : receipt.futureOnly = true
  inactiveReceipt : receipt.activeNow = false

structure BudgetWithin (used maximum : ExecutionBudget) : Prop where
  candidate : used.candidate ≤ maximum.candidate
  providerCall : used.providerCall ≤ maximum.providerCall
  command : used.command ≤ maximum.command
  timeoutSeconds : used.timeoutSeconds ≤ maximum.timeoutSeconds
  outputBytes : used.outputBytes ≤ maximum.outputBytes

theorem one_shot_input_is_consumed_once
    (receipt : AdmissionGatedExecutionReceipt)
    (valid : AdmissionGatedExecutionReceiptValid receipt) :
    receipt.executionInputVerified = true ∧
      receipt.executionInputConsumed = true ∧
      receipt.executionInputReplayExcluded = true ∧
      receipt.cycleExecutionNonceReplayExcluded = true := by
  exact ⟨valid.inputVerified, valid.inputConsumed, valid.noInputReplay, valid.noNonceReplay⟩

theorem admitted_cycle_executes_bounded_stages
    (receipt : AdmissionGatedExecutionReceipt)
    (valid : AdmissionGatedExecutionReceiptValid receipt) :
    receipt.providerInvoked = true ∧
      receipt.candidateGenerated = true ∧
      receipt.candidateSelected = true ∧
      receipt.isolatedPatchApplicationPerformed = true ∧
      receipt.verificationExecuted = true ∧
      receipt.cycleExecutionPerformed = true ∧
      receipt.cycleCompleted = true := by
  exact ⟨valid.providerCalled, valid.candidateProduced, valid.selected,
    valid.isolatedApplied, valid.verificationRun, valid.cycleRun, valid.cycleDone⟩

theorem all_budget_dimensions_are_bounded
    (receipt : AdmissionGatedExecutionReceipt)
    (bounded : BudgetWithin receipt.usedBudget receipt.maximumBudget) :
    receipt.usedBudget.candidate ≤ receipt.maximumBudget.candidate ∧
      receipt.usedBudget.providerCall ≤ receipt.maximumBudget.providerCall ∧
      receipt.usedBudget.command ≤ receipt.maximumBudget.command ∧
      receipt.usedBudget.timeoutSeconds ≤ receipt.maximumBudget.timeoutSeconds ∧
      receipt.usedBudget.outputBytes ≤ receipt.maximumBudget.outputBytes := by
  exact ⟨bounded.candidate, bounded.providerCall, bounded.command,
    bounded.timeoutSeconds, bounded.outputBytes⟩

theorem all_budget_dimensions_are_conserved
    (receipt : AdmissionGatedExecutionReceipt) :
    receipt.usedBudget.candidate + receipt.unusedBudget.candidate =
        receipt.maximumBudget.candidate ∧
      receipt.usedBudget.providerCall + receipt.unusedBudget.providerCall =
        receipt.maximumBudget.providerCall ∧
      receipt.usedBudget.command + receipt.unusedBudget.command =
        receipt.maximumBudget.command ∧
      receipt.usedBudget.timeoutSeconds + receipt.unusedBudget.timeoutSeconds =
        receipt.maximumBudget.timeoutSeconds ∧
      receipt.usedBudget.outputBytes + receipt.unusedBudget.outputBytes =
        receipt.maximumBudget.outputBytes := by
  exact ⟨receipt.candidateConservation, receipt.providerCallConservation,
    receipt.commandConservation, receipt.timeoutConservation,
    receipt.outputConservation⟩

theorem registry_advances_exactly_once
    (transition : ExecutionRegistryTransition) :
    transition.nextRevision = transition.sourceRevision + 1 ∧
      transition.nextConsumedInputCount = transition.sourceConsumedInputCount + 1 ∧
      transition.sourceLastExecutedCycleIndex < transition.executedCycleIndex := by
  exact ⟨transition.revisionStep, transition.countStep, transition.cycleMonotone⟩

theorem execution_has_no_live_repository_git_or_external_effect
    (receipt : AdmissionGatedExecutionReceipt)
    (valid : AdmissionGatedExecutionReceiptValid receipt) :
    receipt.inputRepositorySnapshotMutated = false ∧
      receipt.liveRepositoryPatchApplied = false ∧
      receipt.repositoryMutationPerformed = false ∧
      receipt.gitRefChanged = false ∧
      receipt.branchCreated = false ∧
      receipt.commitCreated = false ∧
      receipt.pushPerformed = false ∧
      receipt.pullRequestCreated = false ∧
      receipt.networkAccessPerformed = false ∧
      receipt.secretAccessPerformed = false ∧
      receipt.mergePerformed = false ∧
      receipt.deploymentPerformed = false := by
  exact ⟨valid.noInputMutation, valid.noLivePatch, valid.noRepositoryMutation,
    valid.noGitRef, valid.noBranch, valid.noCommit, valid.noPush,
    valid.noPullRequest, valid.noNetwork, valid.noSecret, valid.noMerge,
    valid.noDeployment⟩

theorem execution_receipt_grants_no_successor_merge_or_deployment_authority
    (receipt : AdmissionGatedExecutionReceipt)
    (valid : AdmissionGatedExecutionReceiptValid receipt) :
    receipt.nextCycleAuthorityGranted = false ∧
      receipt.mergeAuthorityGranted = false ∧
      receipt.deploymentAuthorityGranted = false ∧
      receipt.generalSuccessorStageAuthorityGranted = false := by
  exact ⟨valid.noNextAuthority, valid.noMergeAuthority,
    valid.noDeploymentAuthority, valid.noGeneralAuthority⟩

theorem execution_outcome_is_not_correctness_or_proof
    (receipt : AdmissionGatedExecutionReceipt)
    (valid : AdmissionGatedExecutionReceiptValid receipt) :
    receipt.executionInputConsumptionTreatedAsCorrectness = false ∧
      receipt.admittedExecutionTreatedAsSuccessfulRepair = false ∧
      receipt.cyclePassTreatedAsProof = false ∧
      receipt.cycleFailureTreatedAsRequiredRepair = false ∧
      receipt.providerOutputTreatedAsTrustedPatch = false ∧
      receipt.candidateSelectionTreatedAsCorrectness = false ∧
      receipt.verificationEvidenceTreatedAsMergeAuthority = false := by
  exact ⟨valid.inputConsumptionNotCorrectness,
    valid.admittedExecutionNotSuccessfulRepair, valid.passNotProof,
    valid.failureNotRequiredRepair, valid.providerOutputNotTrustedPatch,
    valid.selectionNotCorrectness, valid.evidenceNotMergeAuthority⟩

theorem unused_budget_is_not_reusable_authority
    (receipt : AdmissionGatedExecutionReceipt)
    (valid : AdmissionGatedExecutionReceiptValid receipt) :
    receipt.unusedBudgetTreatedAsReusableAuthority = false ∧
      receipt.completedCycleTreatedAsUnrestrictedContinuation = false ∧
      receipt.executionReceiptTreatedAsGitAuthority = false ∧
      receipt.executionReceiptTreatedAsDeploymentAuthority = false ∧
      receipt.executionReceiptTreatedAsGeneralSuccessorAuthority = false := by
  exact ⟨valid.unusedBudgetNotAuthority, valid.completedCycleNotUnrestricted,
    valid.receiptNotGitAuthority, valid.receiptNotDeploymentAuthority,
    valid.receiptNotGeneralAuthority⟩

end KUOS.CodeAI.AdmissionGatedBoundedRepairCycleExecutionV0_1
