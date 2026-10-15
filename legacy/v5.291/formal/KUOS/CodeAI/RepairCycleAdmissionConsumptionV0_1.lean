import KUOS.CodeAI.RepairCycleContinuationAdmissionV0_1

namespace KUOS.CodeAI.RepairCycleAdmissionConsumptionV0_1

inductive Disposition where
  | repairCycleAdmissionConsumed
  deriving DecidableEq, Repr

inductive OperatingMode where
  | repairCycleAdmissionConsumption
  deriving DecidableEq, Repr

structure RepairCycleExecutionInput where
  sourceAdmissionReceiptDigest : String
  sourceCycleReceiptDigest : String
  sourceSelectedCandidateDigest : String
  sourceRepairReceiptDigest : String
  sourceRegenerationReceiptDigest : String
  repairCandidateSetDigest : String
  verificationPlanDigest : String
  cycleIndex : Nat
  executionSessionId : String
  executionNonceDigest : String
  consumerActorId : String
  maximumCandidateCount : Nat
  maximumProviderCallCount : Nat
  maximumCommandCount : Nat
  maximumTotalTimeoutSeconds : Nat
  maximumTotalOutputBytes : Nat
  sourceAdmissionConsumed : Bool
  oneCycleOnly : Bool
  oneShot : Bool
  executionInputActive : Bool
  executionInputReusable : Bool
  executionInputConsumed : Bool
  boundedCycleExecutionAuthorityGranted : Bool
  candidateGenerationAuthorityGranted : Bool
  candidateSelectionAuthorityGranted : Bool
  isolatedPatchApplicationAuthorityGranted : Bool
  verificationExecutionAuthorityGranted : Bool
  automaticExecutionAuthorityGranted : Bool
  networkAccessAuthorityGranted : Bool
  secretAccessAuthorityGranted : Bool
  liveRepositoryAccessAuthorityGranted : Bool
  gitOperationsAuthorityGranted : Bool
  mergeAuthorityGranted : Bool
  deploymentAuthorityGranted : Bool
  generalSuccessorStageAuthorityGranted : Bool
  cycleExecutionPerformed : Bool
  providerInvoked : Bool
  runnerInvoked : Bool
  candidateGenerated : Bool
  candidateSelected : Bool
  patchApplied : Bool
  verificationExecuted : Bool
  repositoryMutationPerformed : Bool
  gitRefChanged : Bool
  networkAccessPerformed : Bool
  secretAccessPerformed : Bool
  mergePerformed : Bool
  deploymentPerformed : Bool

structure AdmissionConsumptionReceipt where
  sourceAdmissionReceiptDigest : String
  sourceCycleReceiptDigest : String
  sourceSelectedCandidateDigest : String
  consumptionRequestDigest : String
  consumptionPolicyDigest : String
  sourceConsumptionRegistryDigest : String
  nextConsumptionRegistryDigest : String
  executionInputDigest : String
  admittedCycleIndex : Nat
  executionCycleIndex : Nat
  sourceRegistryRevision : Nat
  nextRegistryRevision : Nat
  sourceConsumedAdmissionCount : Nat
  nextConsumedAdmissionCount : Nat
  reservedCandidate : Nat
  executionCandidateBudget : Nat
  reservedProviderCall : Nat
  executionProviderCallBudget : Nat
  reservedCommand : Nat
  executionCommandBudget : Nat
  reservedTimeoutSeconds : Nat
  executionTimeoutSecondsBudget : Nat
  reservedOutputBytes : Nat
  executionOutputBytesBudget : Nat
  disposition : Disposition
  operatingMode : OperatingMode
  routeReceiptRecorded : Bool
  sourceAdmissionVerified : Bool
  sourceAdmissionConsumed : Bool
  admissionReplayExcluded : Bool
  executionNonceReplayExcluded : Bool
  registryTransitionVerified : Bool
  exactlyOneExecutionInputIssued : Bool
  boundedBudgetMappingVerified : Bool
  consumptionAuthorityGranted : Bool
  boundedCycleExecutionAuthorityGranted : Bool
  automaticExecutionAuthorityGranted : Bool
  generalSuccessorStageAuthorityGranted : Bool
  cycleExecutionPerformed : Bool
  providerInvoked : Bool
  runnerInvoked : Bool
  candidateGenerated : Bool
  candidateSelected : Bool
  patchApplied : Bool
  verificationExecuted : Bool
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
  consumptionTreatedAsExecution : Bool
  consumptionTreatedAsCorrectness : Bool
  reservedBudgetTreatedAsConsumedBudget : Bool
  executionInputTreatedAsSuccess : Bool
  registryReceiptTreatedAsExternalAtomicPersistence : Bool
  oneShotInputTreatedAsReusableCapability : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  cycleCorrespondence : executionCycleIndex = admittedCycleIndex
  registryRevisionStep : nextRegistryRevision = sourceRegistryRevision + 1
  consumedCountStep : nextConsumedAdmissionCount = sourceConsumedAdmissionCount + 1
  candidateBudgetCorrespondence : executionCandidateBudget = reservedCandidate
  providerBudgetCorrespondence : executionProviderCallBudget = reservedProviderCall
  commandBudgetCorrespondence : executionCommandBudget = reservedCommand
  timeoutBudgetCorrespondence : executionTimeoutSecondsBudget = reservedTimeoutSeconds
  outputBudgetCorrespondence : executionOutputBytesBudget = reservedOutputBytes

structure RepairCycleExecutionInputValid
    (input : RepairCycleExecutionInput) : Prop where
  sourceConsumed : input.sourceAdmissionConsumed = true
  oneCycle : input.oneCycleOnly = true
  oneShot : input.oneShot = true
  active : input.executionInputActive = true
  nonReusable : input.executionInputReusable = false
  notConsumed : input.executionInputConsumed = false
  boundedAuthority : input.boundedCycleExecutionAuthorityGranted = true
  generationAuthority : input.candidateGenerationAuthorityGranted = true
  selectionAuthority : input.candidateSelectionAuthorityGranted = true
  isolatedApplicationAuthority :
    input.isolatedPatchApplicationAuthorityGranted = true
  verificationAuthority : input.verificationExecutionAuthorityGranted = true
  noAutomaticAuthority : input.automaticExecutionAuthorityGranted = false
  noNetworkAuthority : input.networkAccessAuthorityGranted = false
  noSecretAuthority : input.secretAccessAuthorityGranted = false
  noLiveRepositoryAuthority : input.liveRepositoryAccessAuthorityGranted = false
  noGitAuthority : input.gitOperationsAuthorityGranted = false
  noMergeAuthority : input.mergeAuthorityGranted = false
  noDeploymentAuthority : input.deploymentAuthorityGranted = false
  noGeneralAuthority : input.generalSuccessorStageAuthorityGranted = false
  noCycleExecution : input.cycleExecutionPerformed = false
  noProvider : input.providerInvoked = false
  noRunner : input.runnerInvoked = false
  noGeneration : input.candidateGenerated = false
  noSelection : input.candidateSelected = false
  noPatch : input.patchApplied = false
  noVerification : input.verificationExecuted = false
  noRepositoryMutation : input.repositoryMutationPerformed = false
  noGitRefChange : input.gitRefChanged = false
  noNetwork : input.networkAccessPerformed = false
  noSecret : input.secretAccessPerformed = false
  noMerge : input.mergePerformed = false
  noDeployment : input.deploymentPerformed = false

structure AdmissionConsumptionReceiptValid
    (receipt : AdmissionConsumptionReceipt) : Prop where
  routeRecorded : receipt.routeReceiptRecorded = true
  sourceVerified : receipt.sourceAdmissionVerified = true
  sourceConsumed : receipt.sourceAdmissionConsumed = true
  noAdmissionReplay : receipt.admissionReplayExcluded = true
  noNonceReplay : receipt.executionNonceReplayExcluded = true
  registryTransition : receipt.registryTransitionVerified = true
  exactlyOneInput : receipt.exactlyOneExecutionInputIssued = true
  budgetMapping : receipt.boundedBudgetMappingVerified = true
  consumptionAuthority : receipt.consumptionAuthorityGranted = true
  boundedExecutionAuthority : receipt.boundedCycleExecutionAuthorityGranted = true
  noAutomaticAuthority : receipt.automaticExecutionAuthorityGranted = false
  noGeneralAuthority : receipt.generalSuccessorStageAuthorityGranted = false
  noCycleExecution : receipt.cycleExecutionPerformed = false
  noProvider : receipt.providerInvoked = false
  noRunner : receipt.runnerInvoked = false
  noGeneration : receipt.candidateGenerated = false
  noSelection : receipt.candidateSelected = false
  noPatch : receipt.patchApplied = false
  noVerification : receipt.verificationExecuted = false
  noRepositoryMutation : receipt.repositoryMutationPerformed = false
  noGitRefChange : receipt.gitRefChanged = false
  noBranch : receipt.branchCreated = false
  noCommit : receipt.commitCreated = false
  noPush : receipt.pushPerformed = false
  noPullRequest : receipt.pullRequestCreated = false
  noNetwork : receipt.networkAccessPerformed = false
  noSecret : receipt.secretAccessPerformed = false
  noMerge : receipt.mergePerformed = false
  noDeployment : receipt.deploymentPerformed = false
  consumptionNotExecution : receipt.consumptionTreatedAsExecution = false
  consumptionNotCorrectness : receipt.consumptionTreatedAsCorrectness = false
  reservationNotConsumption : receipt.reservedBudgetTreatedAsConsumedBudget = false
  inputNotSuccess : receipt.executionInputTreatedAsSuccess = false
  registryReceiptNotPersistence :
    receipt.registryReceiptTreatedAsExternalAtomicPersistence = false
  oneShotNotReusable : receipt.oneShotInputTreatedAsReusableCapability = false
  historyReadOnly : receipt.historyReadOnly = true
  futureOnly : receipt.futureOnly = true
  inactiveReceipt : receipt.activeNow = false

theorem consumed_admission_issues_exactly_one_bounded_input
    (receipt : AdmissionConsumptionReceipt)
    (valid : AdmissionConsumptionReceiptValid receipt) :
    receipt.sourceAdmissionConsumed = true ∧
      receipt.admissionReplayExcluded = true ∧
      receipt.executionNonceReplayExcluded = true ∧
      receipt.exactlyOneExecutionInputIssued = true ∧
      receipt.boundedCycleExecutionAuthorityGranted = true := by
  exact ⟨valid.sourceConsumed, valid.noAdmissionReplay, valid.noNonceReplay,
    valid.exactlyOneInput, valid.boundedExecutionAuthority⟩

theorem execution_input_is_active_nonreusable_and_unconsumed
    (input : RepairCycleExecutionInput)
    (valid : RepairCycleExecutionInputValid input) :
    input.executionInputActive = true ∧
      input.executionInputReusable = false ∧
      input.executionInputConsumed = false ∧
      input.oneCycleOnly = true ∧
      input.oneShot = true := by
  exact ⟨valid.active, valid.nonReusable, valid.notConsumed, valid.oneCycle,
    valid.oneShot⟩

theorem execution_cycle_matches_admitted_cycle
    (receipt : AdmissionConsumptionReceipt) :
    receipt.executionCycleIndex = receipt.admittedCycleIndex := by
  exact receipt.cycleCorrespondence

theorem registry_advances_once
    (receipt : AdmissionConsumptionReceipt) :
    receipt.nextRegistryRevision = receipt.sourceRegistryRevision + 1 ∧
      receipt.nextConsumedAdmissionCount =
        receipt.sourceConsumedAdmissionCount + 1 := by
  exact ⟨receipt.registryRevisionStep, receipt.consumedCountStep⟩

theorem all_reserved_budgets_map_exactly
    (receipt : AdmissionConsumptionReceipt) :
    receipt.executionCandidateBudget = receipt.reservedCandidate ∧
      receipt.executionProviderCallBudget = receipt.reservedProviderCall ∧
      receipt.executionCommandBudget = receipt.reservedCommand ∧
      receipt.executionTimeoutSecondsBudget = receipt.reservedTimeoutSeconds ∧
      receipt.executionOutputBytesBudget = receipt.reservedOutputBytes := by
  exact ⟨receipt.candidateBudgetCorrespondence,
    receipt.providerBudgetCorrespondence,
    receipt.commandBudgetCorrespondence,
    receipt.timeoutBudgetCorrespondence,
    receipt.outputBudgetCorrespondence⟩

theorem consumption_does_not_execute_cycle
    (receipt : AdmissionConsumptionReceipt)
    (valid : AdmissionConsumptionReceiptValid receipt) :
    receipt.cycleExecutionPerformed = false ∧
      receipt.providerInvoked = false ∧
      receipt.runnerInvoked = false ∧
      receipt.candidateGenerated = false ∧
      receipt.candidateSelected = false ∧
      receipt.patchApplied = false ∧
      receipt.verificationExecuted = false := by
  exact ⟨valid.noCycleExecution, valid.noProvider, valid.noRunner,
    valid.noGeneration, valid.noSelection, valid.noPatch, valid.noVerification⟩

theorem execution_input_performs_no_cycle_action
    (input : RepairCycleExecutionInput)
    (valid : RepairCycleExecutionInputValid input) :
    input.cycleExecutionPerformed = false ∧
      input.providerInvoked = false ∧
      input.runnerInvoked = false ∧
      input.candidateGenerated = false ∧
      input.candidateSelected = false ∧
      input.patchApplied = false ∧
      input.verificationExecuted = false := by
  exact ⟨valid.noCycleExecution, valid.noProvider, valid.noRunner,
    valid.noGeneration, valid.noSelection, valid.noPatch, valid.noVerification⟩

theorem consumption_has_no_live_repository_git_or_external_effect
    (receipt : AdmissionConsumptionReceipt)
    (valid : AdmissionConsumptionReceiptValid receipt) :
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
  exact ⟨valid.noRepositoryMutation, valid.noGitRefChange, valid.noBranch,
    valid.noCommit, valid.noPush, valid.noPullRequest, valid.noNetwork,
    valid.noSecret, valid.noMerge, valid.noDeployment⟩

theorem bounded_input_grants_no_automatic_or_general_authority
    (input : RepairCycleExecutionInput)
    (valid : RepairCycleExecutionInputValid input) :
    input.automaticExecutionAuthorityGranted = false ∧
      input.networkAccessAuthorityGranted = false ∧
      input.secretAccessAuthorityGranted = false ∧
      input.liveRepositoryAccessAuthorityGranted = false ∧
      input.gitOperationsAuthorityGranted = false ∧
      input.mergeAuthorityGranted = false ∧
      input.deploymentAuthorityGranted = false ∧
      input.generalSuccessorStageAuthorityGranted = false := by
  exact ⟨valid.noAutomaticAuthority, valid.noNetworkAuthority,
    valid.noSecretAuthority, valid.noLiveRepositoryAuthority,
    valid.noGitAuthority, valid.noMergeAuthority,
    valid.noDeploymentAuthority, valid.noGeneralAuthority⟩

theorem consumption_is_not_execution_correctness_persistence_or_success
    (receipt : AdmissionConsumptionReceipt)
    (valid : AdmissionConsumptionReceiptValid receipt) :
    receipt.consumptionTreatedAsExecution = false ∧
      receipt.consumptionTreatedAsCorrectness = false ∧
      receipt.reservedBudgetTreatedAsConsumedBudget = false ∧
      receipt.executionInputTreatedAsSuccess = false ∧
      receipt.registryReceiptTreatedAsExternalAtomicPersistence = false ∧
      receipt.oneShotInputTreatedAsReusableCapability = false := by
  exact ⟨valid.consumptionNotExecution, valid.consumptionNotCorrectness,
    valid.reservationNotConsumption, valid.inputNotSuccess,
    valid.registryReceiptNotPersistence, valid.oneShotNotReusable⟩

end KUOS.CodeAI.RepairCycleAdmissionConsumptionV0_1
