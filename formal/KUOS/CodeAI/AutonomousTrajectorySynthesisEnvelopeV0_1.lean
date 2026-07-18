import KUOS.CodeAI.IndependentVerificationEnvelopeV0_1

namespace KUOS.CodeAI.AutonomousTrajectorySynthesisEnvelopeV0_1

open KUOS.CodeAI.IndependentVerificationEnvelopeV0_1

inductive NextInternalStep where
  | deliberationCandidate
  | repairCandidate
  | reverificationCandidate
  | notGenerated
  deriving DecidableEq, Repr

inductive Disposition where
  | autonomousDeliberationCandidateSynthesized
  | autonomousRepairCandidateSynthesized
  | autonomousReverificationCandidateSynthesized
  | sourceVerificationReceiptRepairRequired
  | trajectoryProvenanceRepairRequired
  | trajectoryCorrespondenceRepairRequired
  | trajectoryWindowRepairRequired
  | trajectoryReplayConflictRejected
  | repositoryOrGitEffectRequestRejected
  | authorityEscalationRejected
  | externalHandoverDeferred
  | unsupportedTrajectoryFormatAbstained
  | trajectoryBudgetRejected
  | verificationOutcomePolicyRepairRequired
  deriving DecidableEq, Repr

inductive OperatingMode where
  | autonomousReadOnly
  | autonomousRepair
  | degradedAutonomy
  | hold
  | abstain
  | rejected
  deriving DecidableEq, Repr

structure AutonomousTrajectoryReceipt where
  sourceVerificationReceiptDigest : String
  sourceCandidateReceiptDigest : String
  trajectoryRequestDigest : String
  trajectoryPolicyDigest : String
  candidatePatchDigest : String
  patchArtifactDigest : String
  verificationEvidenceDigest : String
  repositoryFullName : String
  sourceCommitSha : String
  resultingCommitSha : String
  verificationOutcome : VerificationOutcome
  trajectoryStepCount : Nat
  nextInternalStep : NextInternalStep
  disposition : Disposition
  operatingMode : OperatingMode
  routeReceiptRecorded : Bool
  trajectorySynthesizedByKernel : Bool
  trajectoryReadOnly : Bool
  trajectoryCompleteForAvailableReceipts : Bool
  fullIntentLineageReconstructed : Bool
  autonomousDeliberationCandidateGenerated : Bool
  autonomousRepairCandidateGenerated : Bool
  autonomousReverificationCandidateGenerated : Bool
  clarificationRequired : Bool
  evidenceDegraded : Bool
  abstained : Bool
  externalHandoverDeferred : Bool
  humanHandoverPerformed : Bool
  externalAuthorityHandoverPerformed : Bool
  candidateSelected : Bool
  patchGenerated : Bool
  patchApplied : Bool
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
  trajectoryTreatedAsTruth : Bool
  autonomousCandidateTreatedAsAuthority : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  sourceCommitUnchanged : resultingCommitSha = sourceCommitSha
  deliberationRoute :
    disposition = .autonomousDeliberationCandidateSynthesized →
      operatingMode = .autonomousReadOnly ∧
        verificationOutcome = .passed ∧
        nextInternalStep = .deliberationCandidate ∧
        trajectorySynthesizedByKernel = true ∧
        trajectoryCompleteForAvailableReceipts = true ∧
        trajectoryStepCount = 2 ∧
        autonomousDeliberationCandidateGenerated = true
  repairRoute :
    disposition = .autonomousRepairCandidateSynthesized →
      operatingMode = .autonomousRepair ∧
        verificationOutcome = .failed ∧
        nextInternalStep = .repairCandidate ∧
        trajectorySynthesizedByKernel = true ∧
        trajectoryCompleteForAvailableReceipts = true ∧
        trajectoryStepCount = 2 ∧
        autonomousRepairCandidateGenerated = true
  reverificationRoute :
    disposition = .autonomousReverificationCandidateSynthesized →
      operatingMode = .degradedAutonomy ∧
        verificationOutcome = .inconclusive ∧
        nextInternalStep = .reverificationCandidate ∧
        trajectorySynthesizedByKernel = true ∧
        trajectoryCompleteForAvailableReceipts = true ∧
        trajectoryStepCount = 2 ∧
        autonomousReverificationCandidateGenerated = true ∧
        evidenceDegraded = true
  handoverDeferredRoute :
    disposition = .externalHandoverDeferred →
      operatingMode = .hold ∧
        externalHandoverDeferred = true ∧
        clarificationRequired = true ∧
        trajectorySynthesizedByKernel = false ∧
        nextInternalStep = .notGenerated
  abstainRoute :
    disposition = .unsupportedTrajectoryFormatAbstained →
      operatingMode = .abstain ∧ abstained = true

structure AutonomousTrajectoryReceiptValid
    (receipt : AutonomousTrajectoryReceipt) : Prop where
  routeRecorded : receipt.routeReceiptRecorded = true
  trajectoryReadOnly : receipt.trajectoryReadOnly = true
  noFullIntentReconstruction : receipt.fullIntentLineageReconstructed = false
  noHumanHandover : receipt.humanHandoverPerformed = false
  noExternalAuthorityHandover :
    receipt.externalAuthorityHandoverPerformed = false
  noSelection : receipt.candidateSelected = false
  noPatchGeneration : receipt.patchGenerated = false
  noApplication : receipt.patchApplied = false
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
  sourceNotSuccessorAuthority :
    receipt.sourceReceiptTreatedAsSuccessorAuthority = false
  trajectoryNotTruth : receipt.trajectoryTreatedAsTruth = false
  candidateNotAuthority : receipt.autonomousCandidateTreatedAsAuthority = false
  historyReadOnly : receipt.historyReadOnly = true
  futureOnly : receipt.futureOnly = true
  inactiveNow : receipt.activeNow = false

def SupportedSourceDisposition
    (disposition :
      KUOS.CodeAI.IndependentVerificationEnvelopeV0_1.Disposition) : Prop :=
  disposition = .independentVerificationPassed ∨
    disposition = .independentVerificationFailed ∨
    disposition = .verificationInconclusiveHold ∨
    disposition = .verificationInconclusiveDegraded

structure AutonomousTrajectoryEnvelope where
  sourceReceipt : IndependentVerificationReceipt
  sourceReceiptValid : IndependentVerificationReceiptValid sourceReceipt
  sourceReceiptSupported : SupportedSourceDisposition sourceReceipt.disposition
  receipt : AutonomousTrajectoryReceipt
  receiptValid : AutonomousTrajectoryReceiptValid receipt
  candidateBound : receipt.candidatePatchDigest = sourceReceipt.candidatePatchDigest
  patchBound : receipt.patchArtifactDigest = sourceReceipt.patchArtifactDigest
  repositoryBound : receipt.repositoryFullName = sourceReceipt.repositoryFullName
  sourceCommitBound : receipt.sourceCommitSha = sourceReceipt.sourceCommitSha
  verificationOutcomeBound :
    sourceReceipt.verificationOutcome = some receipt.verificationOutcome

theorem source_commit_is_preserved (receipt : AutonomousTrajectoryReceipt) :
    receipt.resultingCommitSha = receipt.sourceCommitSha := by
  exact receipt.sourceCommitUnchanged

theorem trajectory_is_bound_to_supported_verification
    (envelope : AutonomousTrajectoryEnvelope) :
    envelope.receipt.candidatePatchDigest =
        envelope.sourceReceipt.candidatePatchDigest ∧
      envelope.receipt.patchArtifactDigest =
        envelope.sourceReceipt.patchArtifactDigest ∧
      envelope.receipt.repositoryFullName =
        envelope.sourceReceipt.repositoryFullName ∧
      envelope.receipt.sourceCommitSha =
        envelope.sourceReceipt.sourceCommitSha ∧
      envelope.sourceReceipt.verificationOutcome =
        some envelope.receipt.verificationOutcome ∧
      SupportedSourceDisposition envelope.sourceReceipt.disposition := by
  exact ⟨envelope.candidateBound, envelope.patchBound,
    envelope.repositoryBound, envelope.sourceCommitBound,
    envelope.verificationOutcomeBound, envelope.sourceReceiptSupported⟩

theorem passed_maps_to_deliberation_without_selection
    (receipt : AutonomousTrajectoryReceipt)
    (valid : AutonomousTrajectoryReceiptValid receipt)
    (route :
      receipt.disposition = .autonomousDeliberationCandidateSynthesized) :
    receipt.operatingMode = .autonomousReadOnly ∧
      receipt.verificationOutcome = .passed ∧
      receipt.nextInternalStep = .deliberationCandidate ∧
      receipt.trajectoryStepCount = 2 ∧
      receipt.candidateSelected = false ∧
      receipt.executionAuthorityGranted = false := by
  rcases receipt.deliberationRoute route with
    ⟨mode, outcome, next, _, _, steps, _⟩
  exact ⟨mode, outcome, next, steps, valid.noSelection,
    valid.noExecutionAuthority⟩

theorem failed_maps_to_repair_without_patch_generation
    (receipt : AutonomousTrajectoryReceipt)
    (valid : AutonomousTrajectoryReceiptValid receipt)
    (route : receipt.disposition = .autonomousRepairCandidateSynthesized) :
    receipt.operatingMode = .autonomousRepair ∧
      receipt.verificationOutcome = .failed ∧
      receipt.nextInternalStep = .repairCandidate ∧
      receipt.patchGenerated = false ∧
      receipt.patchApplied = false := by
  rcases receipt.repairRoute route with ⟨mode, outcome, next, _, _, _, _⟩
  exact ⟨mode, outcome, next, valid.noPatchGeneration, valid.noApplication⟩

theorem inconclusive_maps_to_reverification_without_execution
    (receipt : AutonomousTrajectoryReceipt)
    (valid : AutonomousTrajectoryReceiptValid receipt)
    (route :
      receipt.disposition = .autonomousReverificationCandidateSynthesized) :
    receipt.operatingMode = .degradedAutonomy ∧
      receipt.verificationOutcome = .inconclusive ∧
      receipt.nextInternalStep = .reverificationCandidate ∧
      receipt.evidenceDegraded = true ∧
      receipt.executionLeaseIssued = false ∧
      receipt.repositoryMutationPerformed = false := by
  rcases receipt.reverificationRoute route with
    ⟨mode, outcome, next, _, _, _, _, degraded⟩
  exact ⟨mode, outcome, next, degraded, valid.noExecutionLease,
    valid.noRepositoryMutation⟩

theorem external_handover_is_deferred_not_performed
    (receipt : AutonomousTrajectoryReceipt)
    (valid : AutonomousTrajectoryReceiptValid receipt)
    (route : receipt.disposition = .externalHandoverDeferred) :
    receipt.operatingMode = .hold ∧
      receipt.externalHandoverDeferred = true ∧
      receipt.humanHandoverPerformed = false ∧
      receipt.externalAuthorityHandoverPerformed = false ∧
      receipt.trajectorySynthesizedByKernel = false := by
  rcases receipt.handoverDeferredRoute route with
    ⟨mode, deferred, _, synthesized, _⟩
  exact ⟨mode, deferred, valid.noHumanHandover,
    valid.noExternalAuthorityHandover, synthesized⟩

theorem trajectory_has_no_repository_effect
    (receipt : AutonomousTrajectoryReceipt)
    (valid : AutonomousTrajectoryReceiptValid receipt) :
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

theorem trajectory_grants_no_authority
    (receipt : AutonomousTrajectoryReceipt)
    (valid : AutonomousTrajectoryReceiptValid receipt) :
    receipt.selectionAuthorityGranted = false ∧
      receipt.verificationAuthorityGranted = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.mergeAuthorityGranted = false ∧
      receipt.deploymentAuthorityGranted = false ∧
      receipt.secretAccessAuthorityGranted = false := by
  exact ⟨valid.noSelectionAuthority, valid.noVerificationAuthority,
    valid.noExecutionAuthority, valid.noMergeAuthority,
    valid.noDeploymentAuthority, valid.noSecretAccessAuthority⟩

theorem trajectory_claims_neither_truth_nor_successor_authority
    (receipt : AutonomousTrajectoryReceipt)
    (valid : AutonomousTrajectoryReceiptValid receipt) :
    receipt.fullIntentLineageReconstructed = false ∧
      receipt.sourceReceiptTreatedAsSuccessorAuthority = false ∧
      receipt.trajectoryTreatedAsTruth = false ∧
      receipt.autonomousCandidateTreatedAsAuthority = false := by
  exact ⟨valid.noFullIntentReconstruction, valid.sourceNotSuccessorAuthority,
    valid.trajectoryNotTruth, valid.candidateNotAuthority⟩

end KUOS.CodeAI.AutonomousTrajectorySynthesisEnvelopeV0_1
