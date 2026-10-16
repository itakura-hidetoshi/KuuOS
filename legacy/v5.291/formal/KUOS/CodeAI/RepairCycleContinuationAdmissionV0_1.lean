import KUOS.CodeAI.BoundedRepairCycleOrchestrationV0_1

namespace KUOS.CodeAI.RepairCycleContinuationAdmissionV0_1

inductive Disposition where
  | nextRepairCycleAdmitted
  deriving DecidableEq, Repr

inductive OperatingMode where
  | repairCycleContinuationAdmission
  deriving DecidableEq, Repr

structure ContinuationAdmissionReceipt where
  sourceCycleReceiptDigest : String
  sourceSelectedCandidateDigest : String
  continuationRequestDigest : String
  continuationPolicyDigest : String
  budgetLedgerDigest : String
  currentCycleIndex : Nat
  admittedCycleIndex : Nat
  maximumCycleCount : Nat
  reservedCandidate : Nat
  remainingCandidateBeforeReservation : Nat
  remainingCandidateAfterReservation : Nat
  reservedProviderCall : Nat
  remainingProviderCallBeforeReservation : Nat
  remainingProviderCallAfterReservation : Nat
  reservedCommand : Nat
  remainingCommandBeforeReservation : Nat
  remainingCommandAfterReservation : Nat
  reservedTimeoutSeconds : Nat
  remainingTimeoutSecondsBeforeReservation : Nat
  remainingTimeoutSecondsAfterReservation : Nat
  reservedOutputBytes : Nat
  remainingOutputBytesBeforeReservation : Nat
  remainingOutputBytesAfterReservation : Nat
  disposition : Disposition
  operatingMode : OperatingMode
  routeReceiptRecorded : Bool
  sourceCycleLineageVerified : Bool
  cycleSequenceVerified : Bool
  remainingBudgetVerified : Bool
  exactlyOneNextCycleAdmitted : Bool
  continuationAdmissionAuthorityGranted : Bool
  admissionReusable : Bool
  admissionConsumed : Bool
  automaticNextCycleStarted : Bool
  cycleExecutionPerformed : Bool
  runnerInvoked : Bool
  candidateGenerated : Bool
  candidateSelected : Bool
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
  networkAccessPerformed : Bool
  selectionAuthorityGranted : Bool
  verificationAuthorityGranted : Bool
  executionAuthorityGranted : Bool
  automaticExecutionAuthorityGranted : Bool
  mergeAuthorityGranted : Bool
  deploymentAuthorityGranted : Bool
  secretAccessAuthorityGranted : Bool
  generalSuccessorStageAuthorityGranted : Bool
  admissionTreatedAsExecution : Bool
  admissionTreatedAsCorrectness : Bool
  remainingBudgetTreatedAsSafeOutcome : Bool
  sequenceMatchTreatedAsSuccess : Bool
  oneCycleAdmissionTreatedAsReusableCapability : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  exactSuccessor : admittedCycleIndex = currentCycleIndex + 1
  admittedCycleBound : admittedCycleIndex ≤ maximumCycleCount
  candidateReservationBound : reservedCandidate ≤ remainingCandidateBeforeReservation
  candidateConservation :
    remainingCandidateAfterReservation + reservedCandidate =
      remainingCandidateBeforeReservation
  providerReservationBound :
    reservedProviderCall ≤ remainingProviderCallBeforeReservation
  providerConservation :
    remainingProviderCallAfterReservation + reservedProviderCall =
      remainingProviderCallBeforeReservation
  commandReservationBound : reservedCommand ≤ remainingCommandBeforeReservation
  commandConservation :
    remainingCommandAfterReservation + reservedCommand =
      remainingCommandBeforeReservation
  timeoutReservationBound :
    reservedTimeoutSeconds ≤ remainingTimeoutSecondsBeforeReservation
  timeoutConservation :
    remainingTimeoutSecondsAfterReservation + reservedTimeoutSeconds =
      remainingTimeoutSecondsBeforeReservation
  outputReservationBound : reservedOutputBytes ≤ remainingOutputBytesBeforeReservation
  outputConservation :
    remainingOutputBytesAfterReservation + reservedOutputBytes =
      remainingOutputBytesBeforeReservation

structure ContinuationAdmissionReceiptValid
    (receipt : ContinuationAdmissionReceipt) : Prop where
  routeRecorded : receipt.routeReceiptRecorded = true
  sourceLineage : receipt.sourceCycleLineageVerified = true
  sequenceVerified : receipt.cycleSequenceVerified = true
  budgetVerified : receipt.remainingBudgetVerified = true
  exactlyOneCycle : receipt.exactlyOneNextCycleAdmitted = true
  boundedAdmissionAuthority : receipt.continuationAdmissionAuthorityGranted = true
  nonReusable : receipt.admissionReusable = false
  notConsumed : receipt.admissionConsumed = false
  noAutomaticStart : receipt.automaticNextCycleStarted = false
  noCycleExecution : receipt.cycleExecutionPerformed = false
  noRunner : receipt.runnerInvoked = false
  noGeneration : receipt.candidateGenerated = false
  noSelection : receipt.candidateSelected = false
  noPatch : receipt.patchApplied = false
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
  noAutomaticExecutionAuthority : receipt.automaticExecutionAuthorityGranted = false
  noMergeAuthority : receipt.mergeAuthorityGranted = false
  noDeploymentAuthority : receipt.deploymentAuthorityGranted = false
  noSecretAuthority : receipt.secretAccessAuthorityGranted = false
  noGeneralSuccessorAuthority : receipt.generalSuccessorStageAuthorityGranted = false
  admissionNotExecution : receipt.admissionTreatedAsExecution = false
  admissionNotCorrectness : receipt.admissionTreatedAsCorrectness = false
  remainingBudgetNotSafeOutcome : receipt.remainingBudgetTreatedAsSafeOutcome = false
  sequenceNotSuccess : receipt.sequenceMatchTreatedAsSuccess = false
  oneCycleNotReusable :
    receipt.oneCycleAdmissionTreatedAsReusableCapability = false
  historyReadOnly : receipt.historyReadOnly = true
  futureOnly : receipt.futureOnly = true
  inactiveNow : receipt.activeNow = false

theorem admitted_cycle_is_exact_successor
    (receipt : ContinuationAdmissionReceipt) :
    receipt.admittedCycleIndex = receipt.currentCycleIndex + 1 := by
  exact receipt.exactSuccessor

theorem admitted_cycle_remains_within_cycle_limit
    (receipt : ContinuationAdmissionReceipt) :
    receipt.admittedCycleIndex ≤ receipt.maximumCycleCount := by
  exact receipt.admittedCycleBound

theorem one_cycle_admission_is_nonreusable_and_inactive
    (receipt : ContinuationAdmissionReceipt)
    (valid : ContinuationAdmissionReceiptValid receipt) :
    receipt.admissionReusable = false ∧
      receipt.admissionConsumed = false ∧
      receipt.automaticNextCycleStarted = false ∧
      receipt.activeNow = false := by
  exact ⟨valid.nonReusable, valid.notConsumed, valid.noAutomaticStart,
    valid.inactiveNow⟩

theorem continuation_admission_does_not_execute_cycle
    (receipt : ContinuationAdmissionReceipt)
    (valid : ContinuationAdmissionReceiptValid receipt) :
    receipt.cycleExecutionPerformed = false ∧
      receipt.runnerInvoked = false ∧
      receipt.candidateGenerated = false ∧
      receipt.candidateSelected = false ∧
      receipt.patchApplied = false := by
  exact ⟨valid.noCycleExecution, valid.noRunner, valid.noGeneration,
    valid.noSelection, valid.noPatch⟩

theorem continuation_admission_has_no_live_repository_or_git_effect
    (receipt : ContinuationAdmissionReceipt)
    (valid : ContinuationAdmissionReceiptValid receipt) :
    receipt.repositoryMutationPerformed = false ∧
      receipt.gitRefChanged = false ∧
      receipt.branchCreated = false ∧
      receipt.commitCreated = false ∧
      receipt.pushPerformed = false ∧
      receipt.pullRequestCreated = false ∧
      receipt.mergePerformed = false := by
  exact ⟨valid.noRepositoryMutation, valid.noGitRefChange,
    valid.noBranchCreation, valid.noCommitCreation, valid.noPush,
    valid.noPullRequest, valid.noMerge⟩

theorem continuation_admission_has_no_network_secret_or_deployment_effect
    (receipt : ContinuationAdmissionReceipt)
    (valid : ContinuationAdmissionReceiptValid receipt) :
    receipt.networkAccessPerformed = false ∧
      receipt.secretAccessPerformed = false ∧
      receipt.deploymentPerformed = false := by
  exact ⟨valid.noNetworkAccess, valid.noSecretAccess, valid.noDeployment⟩

theorem continuation_admission_grants_no_execution_or_general_authority
    (receipt : ContinuationAdmissionReceipt)
    (valid : ContinuationAdmissionReceiptValid receipt) :
    receipt.selectionAuthorityGranted = false ∧
      receipt.verificationAuthorityGranted = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.automaticExecutionAuthorityGranted = false ∧
      receipt.mergeAuthorityGranted = false ∧
      receipt.deploymentAuthorityGranted = false ∧
      receipt.secretAccessAuthorityGranted = false ∧
      receipt.generalSuccessorStageAuthorityGranted = false := by
  exact ⟨valid.noSelectionAuthority, valid.noVerificationAuthority,
    valid.noExecutionAuthority, valid.noAutomaticExecutionAuthority,
    valid.noMergeAuthority, valid.noDeploymentAuthority,
    valid.noSecretAuthority, valid.noGeneralSuccessorAuthority⟩

theorem candidate_budget_is_conserved
    (receipt : ContinuationAdmissionReceipt) :
    receipt.remainingCandidateAfterReservation + receipt.reservedCandidate =
      receipt.remainingCandidateBeforeReservation := by
  exact receipt.candidateConservation

theorem provider_budget_is_conserved
    (receipt : ContinuationAdmissionReceipt) :
    receipt.remainingProviderCallAfterReservation + receipt.reservedProviderCall =
      receipt.remainingProviderCallBeforeReservation := by
  exact receipt.providerConservation

theorem command_budget_is_conserved
    (receipt : ContinuationAdmissionReceipt) :
    receipt.remainingCommandAfterReservation + receipt.reservedCommand =
      receipt.remainingCommandBeforeReservation := by
  exact receipt.commandConservation

theorem timeout_budget_is_conserved
    (receipt : ContinuationAdmissionReceipt) :
    receipt.remainingTimeoutSecondsAfterReservation + receipt.reservedTimeoutSeconds =
      receipt.remainingTimeoutSecondsBeforeReservation := by
  exact receipt.timeoutConservation

theorem output_budget_is_conserved
    (receipt : ContinuationAdmissionReceipt) :
    receipt.remainingOutputBytesAfterReservation + receipt.reservedOutputBytes =
      receipt.remainingOutputBytesBeforeReservation := by
  exact receipt.outputConservation

theorem admission_is_not_execution_correctness_or_success
    (receipt : ContinuationAdmissionReceipt)
    (valid : ContinuationAdmissionReceiptValid receipt) :
    receipt.admissionTreatedAsExecution = false ∧
      receipt.admissionTreatedAsCorrectness = false ∧
      receipt.remainingBudgetTreatedAsSafeOutcome = false ∧
      receipt.sequenceMatchTreatedAsSuccess = false ∧
      receipt.oneCycleAdmissionTreatedAsReusableCapability = false := by
  exact ⟨valid.admissionNotExecution, valid.admissionNotCorrectness,
    valid.remainingBudgetNotSafeOutcome, valid.sequenceNotSuccess,
    valid.oneCycleNotReusable⟩

end KUOS.CodeAI.RepairCycleContinuationAdmissionV0_1
