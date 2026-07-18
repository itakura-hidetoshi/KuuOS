import KUOS.CodeAI.AutonomousTrajectorySynthesisEnvelopeV0_1

namespace KUOS.CodeAI.AutonomousGitLifecycleEnvelopeV0_1

open KUOS.CodeAI.AutonomousTrajectorySynthesisEnvelopeV0_1

inductive EffectPhase where
  | localCommit
  | pushBranch
  | createPullRequest
  | markPullRequestReady
  | awaitRequiredChecks
  | mergePullRequest
  | complete
  | none
  deriving DecidableEq, Repr

inductive Disposition where
  | autonomousLocalCommitAuthorized
  | autonomousBranchPushAuthorized
  | autonomousPullRequestCreationAuthorized
  | autonomousPullRequestReadinessAuthorized
  | requiredChecksPendingHold
  | requiredChecksFailedDegraded
  | pullRequestMergeGateHold
  | autonomousPullRequestMergeAuthorized
  | autonomousGitLifecycleCompleted
  | sourceTrajectoryReceiptRepairRequired
  | gitLifecycleProvenanceRepairRequired
  | gitLifecycleStateEvidenceRepairRequired
  | gitLifecycleCorrespondenceRepairRequired
  | gitLifecycleWindowRepairRequired
  | gitLifecycleReplayConflictRejected
  | unsupportedGitLifecycleScopeAbstained
  | destructiveGitEffectRejected
  | humanHandoverDeferred
  | gitLifecycleStateRepairRequired
  deriving DecidableEq, Repr

inductive OperatingMode where
  | localGitEffectAuthorized
  | remoteGitEffectAuthorized
  | pullRequestEffectAuthorized
  | mergeEffectAuthorized
  | awaitingRequiredChecks
  | degradedAutonomy
  | completed
  | hold
  | abstain
  | rejected
  deriving DecidableEq, Repr

structure AutonomousGitLifecycleReceipt where
  sourceTrajectoryReceiptDigest : String
  gitLifecycleRequestDigest : String
  gitLifecycleStateDigest : String
  gitLifecyclePolicyDigest : String
  lifecycleId : String
  repositoryFullName : String
  sourceCommitSha : String
  baseBranch : String
  headBranch : String
  remoteName : String
  mergeMethod : String
  nextEffectPhase : EffectPhase
  disposition : Disposition
  operatingMode : OperatingMode
  routeReceiptRecorded : Bool
  executionLeaseIssued : Bool
  localCommitAuthorityGranted : Bool
  pushAuthorityGranted : Bool
  pullRequestAuthorityGranted : Bool
  pullRequestReadinessAuthorityGranted : Bool
  mergeAuthorityGranted : Bool
  checksWaitRequired : Bool
  humanHandoverDeferred : Bool
  effectExecutionPerformedByKernel : Bool
  localCommitCreatedObserved : Bool
  branchPushedObserved : Bool
  pullRequestCreatedObserved : Bool
  pullRequestDraftObserved : Bool
  requiredChecksObserved : Bool
  allRequiredChecksSuccessful : Bool
  noPendingChecks : Bool
  noFailedChecks : Bool
  mergeableObserved : Bool
  noUnresolvedBlockers : Bool
  headShaPinned : Bool
  mergePerformedObserved : Bool
  forcePushPerformed : Bool
  remoteBranchDeleted : Bool
  adminMergeBypassUsed : Bool
  humanHandoverPerformed : Bool
  externalAuthorityHandoverPerformed : Bool
  deploymentAuthorityGranted : Bool
  deploymentPerformed : Bool
  secretAccessAuthorityGranted : Bool
  secretAccessPerformed : Bool
  sourceReceiptTreatedAsGitAuthority : Bool
  checksTreatedAsCorrectnessProof : Bool
  mergeTreatedAsTruth : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  localCommitRoute :
    disposition = .autonomousLocalCommitAuthorized →
      operatingMode = .localGitEffectAuthorized ∧
        nextEffectPhase = .localCommit ∧
        executionLeaseIssued = true ∧
        localCommitAuthorityGranted = true ∧
        pushAuthorityGranted = false ∧
        pullRequestAuthorityGranted = false ∧
        pullRequestReadinessAuthorityGranted = false ∧
        mergeAuthorityGranted = false
  pushRoute :
    disposition = .autonomousBranchPushAuthorized →
      operatingMode = .remoteGitEffectAuthorized ∧
        nextEffectPhase = .pushBranch ∧
        executionLeaseIssued = true ∧
        localCommitCreatedObserved = true ∧
        localCommitAuthorityGranted = false ∧
        pushAuthorityGranted = true ∧
        pullRequestAuthorityGranted = false ∧
        pullRequestReadinessAuthorityGranted = false ∧
        mergeAuthorityGranted = false
  pullRequestRoute :
    disposition = .autonomousPullRequestCreationAuthorized →
      operatingMode = .pullRequestEffectAuthorized ∧
        nextEffectPhase = .createPullRequest ∧
        executionLeaseIssued = true ∧
        branchPushedObserved = true ∧
        pullRequestAuthorityGranted = true ∧
        localCommitAuthorityGranted = false ∧
        pushAuthorityGranted = false ∧
        pullRequestReadinessAuthorityGranted = false ∧
        mergeAuthorityGranted = false
  readinessRoute :
    disposition = .autonomousPullRequestReadinessAuthorized →
      operatingMode = .pullRequestEffectAuthorized ∧
        nextEffectPhase = .markPullRequestReady ∧
        executionLeaseIssued = true ∧
        pullRequestCreatedObserved = true ∧
        pullRequestDraftObserved = true ∧
        pullRequestReadinessAuthorityGranted = true ∧
        localCommitAuthorityGranted = false ∧
        pushAuthorityGranted = false ∧
        pullRequestAuthorityGranted = false ∧
        mergeAuthorityGranted = false
  mergeRoute :
    disposition = .autonomousPullRequestMergeAuthorized →
      operatingMode = .mergeEffectAuthorized ∧
        nextEffectPhase = .mergePullRequest ∧
        executionLeaseIssued = true ∧
        pullRequestCreatedObserved = true ∧
        pullRequestDraftObserved = false ∧
        requiredChecksObserved = true ∧
        allRequiredChecksSuccessful = true ∧
        noPendingChecks = true ∧
        noFailedChecks = true ∧
        mergeableObserved = true ∧
        noUnresolvedBlockers = true ∧
        headShaPinned = true ∧
        mergeAuthorityGranted = true ∧
        localCommitAuthorityGranted = false ∧
        pushAuthorityGranted = false ∧
        pullRequestAuthorityGranted = false ∧
        pullRequestReadinessAuthorityGranted = false
  completedRoute :
    disposition = .autonomousGitLifecycleCompleted →
      operatingMode = .completed ∧
        nextEffectPhase = .complete ∧
        executionLeaseIssued = false ∧
        mergePerformedObserved = true ∧
        activeNow = false
  handoverDeferredRoute :
    disposition = .humanHandoverDeferred →
      operatingMode = .hold ∧
        nextEffectPhase = .none ∧
        executionLeaseIssued = false ∧
        humanHandoverDeferred = true

structure AutonomousGitLifecycleReceiptValid
    (receipt : AutonomousGitLifecycleReceipt) : Prop where
  routeRecorded : receipt.routeReceiptRecorded = true
  noKernelExecution : receipt.effectExecutionPerformedByKernel = false
  noForcePush : receipt.forcePushPerformed = false
  noRemoteBranchDeletion : receipt.remoteBranchDeleted = false
  noAdminMergeBypass : receipt.adminMergeBypassUsed = false
  noHumanHandover : receipt.humanHandoverPerformed = false
  noExternalAuthorityHandover :
    receipt.externalAuthorityHandoverPerformed = false
  noDeploymentAuthority : receipt.deploymentAuthorityGranted = false
  noDeployment : receipt.deploymentPerformed = false
  noSecretAuthority : receipt.secretAccessAuthorityGranted = false
  noSecretAccess : receipt.secretAccessPerformed = false
  sourceNotGitAuthority : receipt.sourceReceiptTreatedAsGitAuthority = false
  checksNotCorrectness : receipt.checksTreatedAsCorrectnessProof = false
  mergeNotTruth : receipt.mergeTreatedAsTruth = false
  historyReadOnly : receipt.historyReadOnly = true

structure AutonomousGitLifecycleEnvelope where
  sourceReceipt : AutonomousTrajectoryReceipt
  sourceReceiptValid : AutonomousTrajectoryReceiptValid sourceReceipt
  sourceReceiptSupported :
    sourceReceipt.disposition = .autonomousDeliberationCandidateSynthesized
  receipt : AutonomousGitLifecycleReceipt
  receiptValid : AutonomousGitLifecycleReceiptValid receipt
  repositoryBound : receipt.repositoryFullName = sourceReceipt.repositoryFullName
  sourceCommitBound : receipt.sourceCommitSha = sourceReceipt.sourceCommitSha

theorem lifecycle_is_bound_to_deliberation_trajectory
    (envelope : AutonomousGitLifecycleEnvelope) :
    envelope.receipt.repositoryFullName =
        envelope.sourceReceipt.repositoryFullName ∧
      envelope.receipt.sourceCommitSha =
        envelope.sourceReceipt.sourceCommitSha ∧
      envelope.sourceReceipt.disposition =
        .autonomousDeliberationCandidateSynthesized := by
  exact ⟨envelope.repositoryBound, envelope.sourceCommitBound,
    envelope.sourceReceiptSupported⟩

theorem source_trajectory_is_not_git_authority
    (receipt : AutonomousGitLifecycleReceipt)
    (valid : AutonomousGitLifecycleReceiptValid receipt) :
    receipt.sourceReceiptTreatedAsGitAuthority = false ∧
      receipt.effectExecutionPerformedByKernel = false := by
  exact ⟨valid.sourceNotGitAuthority, valid.noKernelExecution⟩

theorem local_commit_authority_is_one_effect
    (receipt : AutonomousGitLifecycleReceipt)
    (route : receipt.disposition = .autonomousLocalCommitAuthorized) :
    receipt.localCommitAuthorityGranted = true ∧
      receipt.pushAuthorityGranted = false ∧
      receipt.pullRequestAuthorityGranted = false ∧
      receipt.pullRequestReadinessAuthorityGranted = false ∧
      receipt.mergeAuthorityGranted = false := by
  rcases receipt.localCommitRoute route with
    ⟨_, _, _, localAuth, push, pr, ready, merge⟩
  exact ⟨localAuth, push, pr, ready, merge⟩

theorem push_requires_observed_commit_and_grants_only_push
    (receipt : AutonomousGitLifecycleReceipt)
    (route : receipt.disposition = .autonomousBranchPushAuthorized) :
    receipt.localCommitCreatedObserved = true ∧
      receipt.pushAuthorityGranted = true ∧
      receipt.localCommitAuthorityGranted = false ∧
      receipt.pullRequestAuthorityGranted = false ∧
      receipt.mergeAuthorityGranted = false := by
  rcases receipt.pushRoute route with
    ⟨_, _, _, commit, localAuth, push, pr, _, merge⟩
  exact ⟨commit, push, localAuth, pr, merge⟩

theorem pull_request_requires_observed_push
    (receipt : AutonomousGitLifecycleReceipt)
    (route :
      receipt.disposition = .autonomousPullRequestCreationAuthorized) :
    receipt.branchPushedObserved = true ∧
      receipt.pullRequestAuthorityGranted = true ∧
      receipt.pushAuthorityGranted = false ∧
      receipt.mergeAuthorityGranted = false := by
  rcases receipt.pullRequestRoute route with
    ⟨_, _, _, pushed, pr, _, push, _, merge⟩
  exact ⟨pushed, pr, push, merge⟩

theorem merge_requires_complete_gate_and_grants_only_merge
    (receipt : AutonomousGitLifecycleReceipt)
    (route : receipt.disposition = .autonomousPullRequestMergeAuthorized) :
    receipt.pullRequestCreatedObserved = true ∧
      receipt.pullRequestDraftObserved = false ∧
      receipt.requiredChecksObserved = true ∧
      receipt.allRequiredChecksSuccessful = true ∧
      receipt.noPendingChecks = true ∧
      receipt.noFailedChecks = true ∧
      receipt.mergeableObserved = true ∧
      receipt.noUnresolvedBlockers = true ∧
      receipt.headShaPinned = true ∧
      receipt.mergeAuthorityGranted = true ∧
      receipt.localCommitAuthorityGranted = false ∧
      receipt.pushAuthorityGranted = false ∧
      receipt.pullRequestAuthorityGranted = false := by
  rcases receipt.mergeRoute route with
    ⟨_, _, _, pr, draft, checks, successful, pending, failed,
      mergeable, blockers, pinned, merge, localAuth, push, prAuth, _⟩
  exact ⟨pr, draft, checks, successful, pending, failed,
    mergeable, blockers, pinned, merge, localAuth, push, prAuth⟩

theorem completed_lifecycle_issues_no_new_lease
    (receipt : AutonomousGitLifecycleReceipt)
    (route : receipt.disposition = .autonomousGitLifecycleCompleted) :
    receipt.operatingMode = .completed ∧
      receipt.nextEffectPhase = .complete ∧
      receipt.executionLeaseIssued = false ∧
      receipt.mergePerformedObserved = true ∧
      receipt.activeNow = false := by
  exact receipt.completedRoute route

theorem destructive_and_external_effects_remain_excluded
    (receipt : AutonomousGitLifecycleReceipt)
    (valid : AutonomousGitLifecycleReceiptValid receipt) :
    receipt.forcePushPerformed = false ∧
      receipt.remoteBranchDeleted = false ∧
      receipt.adminMergeBypassUsed = false ∧
      receipt.deploymentPerformed = false ∧
      receipt.secretAccessPerformed = false := by
  exact ⟨valid.noForcePush, valid.noRemoteBranchDeletion,
    valid.noAdminMergeBypass, valid.noDeployment, valid.noSecretAccess⟩

theorem human_handover_is_deferred_not_performed
    (receipt : AutonomousGitLifecycleReceipt)
    (valid : AutonomousGitLifecycleReceiptValid receipt)
    (route : receipt.disposition = .humanHandoverDeferred) :
    receipt.operatingMode = .hold ∧
      receipt.humanHandoverDeferred = true ∧
      receipt.humanHandoverPerformed = false ∧
      receipt.externalAuthorityHandoverPerformed = false := by
  rcases receipt.handoverDeferredRoute route with
    ⟨mode, _, _, deferred⟩
  exact ⟨mode, deferred, valid.noHumanHandover,
    valid.noExternalAuthorityHandover⟩

theorem checks_and_merge_claim_neither_correctness_nor_truth
    (receipt : AutonomousGitLifecycleReceipt)
    (valid : AutonomousGitLifecycleReceiptValid receipt) :
    receipt.checksTreatedAsCorrectnessProof = false ∧
      receipt.mergeTreatedAsTruth = false := by
  exact ⟨valid.checksNotCorrectness, valid.mergeNotTruth⟩

end KUOS.CodeAI.AutonomousGitLifecycleEnvelopeV0_1
