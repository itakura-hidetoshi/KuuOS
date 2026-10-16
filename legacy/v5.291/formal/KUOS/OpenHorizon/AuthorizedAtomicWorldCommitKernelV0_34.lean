import Mathlib
import KUOS.OpenHorizon.VerifyOSWorldAdoptionKernelV0_33
import KUOS.OpenHorizon.TransactionalEffectReconciliationKernelV0_24

namespace KUOS.OpenHorizon

structure AuthorizedAtomicWorldCommitKernelV034 where
  verifiedDisposition : VerifyOSWorldAdoptionKernelV033
  adoptCandidateBoundExactly : Bool
  authorizationBoundExactly : Bool
  requestReconstructibleExactly : Bool
  storeIdentityBoundExactly : Bool
  rootLineageBoundExactly : Bool
  priorFragmentBoundExactly : Bool
  priorCommitBoundExactly : Bool
  expectedGenerationBoundExactly : Bool
  targetGenerationIsSuccessor : Bool
  fencingTokenStrictlyFresh : Bool
  leaseEpochNondecreasing : Bool
  localCommitAuthorizationFinite : Bool
  localCommitAuthorizationSingleUse : Bool
  openHorizonPreserved : Bool
  globalCycleLimitAbsent : Bool
  globalGenerationLimitAbsent : Bool
  globalTimeHorizonLimitAbsent : Bool
  optimisticConcurrencyMatched : Bool
  atomicReplaceCommitted : Bool
  oneAtomicStoreAndReceiptState : Bool
  appendOnlyHistoryPreserved : Bool
  immutableCommitReceipt : Bool
  rollbackReferencePreserved : Bool
  rollbackRequiresFreshAuthorization : Bool
  rollbackDeletesHistory : Bool
  sameRootPreserved : Bool
  worldCommitRecorded : Bool
  worldCommitIsTruth : Bool
  worldCommitIsCausalAttribution : Bool
  constitutionalRootRewritten : Bool
  memoryHistoryOverwritten : Bool
  automaticRollbackPerformed : Bool
  automaticMissionCompletion : Bool
  planActivationGranted : Bool
  actosInvocationGranted : Bool
  replayIdempotent : Bool
  staleGenerationRejected : Bool
  stalePriorFragmentRejected : Bool
  stalePriorCommitRejected : Bool
  staleFencingRejected : Bool
  staleLeaseEpochRejected : Bool
  candidateBindingRequired : adoptCandidateBoundExactly = true
  authorizationBindingRequired : authorizationBoundExactly = true
  requestReconstructionRequired : requestReconstructibleExactly = true
  storeBindingRequired : storeIdentityBoundExactly = true
  rootBindingRequired : rootLineageBoundExactly = true
  priorFragmentRequired : priorFragmentBoundExactly = true
  priorCommitRequired : priorCommitBoundExactly = true
  generationBindingRequired : expectedGenerationBoundExactly = true
  successorGenerationRequired : targetGenerationIsSuccessor = true
  freshFencingRequired : fencingTokenStrictlyFresh = true
  leaseEpochRequired : leaseEpochNondecreasing = true
  finiteLocalAuthorizationRequired : localCommitAuthorizationFinite = true
  singleUseRequired : localCommitAuthorizationSingleUse = true
  openHorizonRequired : openHorizonPreserved = true
  noGlobalCycleLimitRequired : globalCycleLimitAbsent = true
  noGlobalGenerationLimitRequired : globalGenerationLimitAbsent = true
  noGlobalTimeHorizonRequired : globalTimeHorizonLimitAbsent = true
  optimisticConcurrencyRequired : optimisticConcurrencyMatched = true
  atomicReplaceRequired : atomicReplaceCommitted = true
  atomicStateRequired : oneAtomicStoreAndReceiptState = true
  appendOnlyRequired : appendOnlyHistoryPreserved = true
  immutableReceiptRequired : immutableCommitReceipt = true
  rollbackReferenceRequired : rollbackReferencePreserved = true
  freshRollbackAuthorizationRequired : rollbackRequiresFreshAuthorization = true
  rollbackHistoryDeletionForbidden : rollbackDeletesHistory = false
  sameRootRequired : sameRootPreserved = true
  commitRecordRequired : worldCommitRecorded = true
  truthForbidden : worldCommitIsTruth = false
  causalAttributionForbidden : worldCommitIsCausalAttribution = false
  rootRewriteForbidden : constitutionalRootRewritten = false
  historyOverwriteForbidden : memoryHistoryOverwritten = false
  automaticRollbackForbidden : automaticRollbackPerformed = false
  automaticMissionCompletionForbidden : automaticMissionCompletion = false
  planActivationForbidden : planActivationGranted = false
  actosInvocationForbidden : actosInvocationGranted = false
  replayRequired : replayIdempotent = true
  staleGenerationRejectionRequired : staleGenerationRejected = true
  stalePriorFragmentRejectionRequired : stalePriorFragmentRejected = true
  stalePriorCommitRejectionRequired : stalePriorCommitRejected = true
  staleFencingRejectionRequired : staleFencingRejected = true
  staleLeaseRejectionRequired : staleLeaseEpochRejected = true

namespace AuthorizedAtomicWorldCommit

theorem local_commit_authorization_does_not_shrink_open_horizon
    (k : AuthorizedAtomicWorldCommitKernelV034) :
    k.localCommitAuthorizationFinite = true ∧
      k.localCommitAuthorizationSingleUse = true ∧
      k.openHorizonPreserved = true ∧
      k.globalCycleLimitAbsent = true ∧
      k.globalGenerationLimitAbsent = true ∧
      k.globalTimeHorizonLimitAbsent = true := by
  exact ⟨k.finiteLocalAuthorizationRequired,
    k.singleUseRequired,
    k.openHorizonRequired,
    k.noGlobalCycleLimitRequired,
    k.noGlobalGenerationLimitRequired,
    k.noGlobalTimeHorizonRequired⟩


theorem atomic_world_commit_preserves_history_and_root
    (k : AuthorizedAtomicWorldCommitKernelV034) :
    k.atomicReplaceCommitted = true ∧
      k.oneAtomicStoreAndReceiptState = true ∧
      k.appendOnlyHistoryPreserved = true ∧
      k.immutableCommitReceipt = true ∧
      k.sameRootPreserved = true ∧
      k.constitutionalRootRewritten = false ∧
      k.memoryHistoryOverwritten = false := by
  exact ⟨k.atomicReplaceRequired,
    k.atomicStateRequired,
    k.appendOnlyRequired,
    k.immutableReceiptRequired,
    k.sameRootRequired,
    k.rootRewriteForbidden,
    k.historyOverwriteForbidden⟩


theorem rollback_reference_is_not_automatic_history_deletion
    (k : AuthorizedAtomicWorldCommitKernelV034) :
    k.rollbackReferencePreserved = true ∧
      k.rollbackRequiresFreshAuthorization = true ∧
      k.rollbackDeletesHistory = false ∧
      k.automaticRollbackPerformed = false := by
  exact ⟨k.rollbackReferenceRequired,
    k.freshRollbackAuthorizationRequired,
    k.rollbackHistoryDeletionForbidden,
    k.automaticRollbackForbidden⟩


theorem authorized_atomic_world_commit_boundary
    (k : AuthorizedAtomicWorldCommitKernelV034) :
    k.verifiedDisposition.dispositionRemainsCandidate = true ∧
      k.verifiedDisposition.worldCommitSeparate = true ∧
      k.adoptCandidateBoundExactly = true ∧
      k.authorizationBoundExactly = true ∧
      k.requestReconstructibleExactly = true ∧
      k.storeIdentityBoundExactly = true ∧
      k.rootLineageBoundExactly = true ∧
      k.priorFragmentBoundExactly = true ∧
      k.priorCommitBoundExactly = true ∧
      k.expectedGenerationBoundExactly = true ∧
      k.targetGenerationIsSuccessor = true ∧
      k.fencingTokenStrictlyFresh = true ∧
      k.leaseEpochNondecreasing = true ∧
      k.localCommitAuthorizationFinite = true ∧
      k.localCommitAuthorizationSingleUse = true ∧
      k.openHorizonPreserved = true ∧
      k.globalCycleLimitAbsent = true ∧
      k.globalGenerationLimitAbsent = true ∧
      k.globalTimeHorizonLimitAbsent = true ∧
      k.optimisticConcurrencyMatched = true ∧
      k.atomicReplaceCommitted = true ∧
      k.oneAtomicStoreAndReceiptState = true ∧
      k.appendOnlyHistoryPreserved = true ∧
      k.immutableCommitReceipt = true ∧
      k.rollbackReferencePreserved = true ∧
      k.rollbackRequiresFreshAuthorization = true ∧
      k.rollbackDeletesHistory = false ∧
      k.sameRootPreserved = true ∧
      k.worldCommitRecorded = true ∧
      k.worldCommitIsTruth = false ∧
      k.worldCommitIsCausalAttribution = false ∧
      k.constitutionalRootRewritten = false ∧
      k.memoryHistoryOverwritten = false ∧
      k.automaticRollbackPerformed = false ∧
      k.automaticMissionCompletion = false ∧
      k.planActivationGranted = false ∧
      k.actosInvocationGranted = false ∧
      k.replayIdempotent = true ∧
      k.staleGenerationRejected = true ∧
      k.stalePriorFragmentRejected = true ∧
      k.stalePriorCommitRejected = true ∧
      k.staleFencingRejected = true ∧
      k.staleLeaseEpochRejected = true := by
  exact ⟨k.verifiedDisposition.dispositionCandidateRequired,
    k.verifiedDisposition.separateCommitRequired,
    k.candidateBindingRequired,
    k.authorizationBindingRequired,
    k.requestReconstructionRequired,
    k.storeBindingRequired,
    k.rootBindingRequired,
    k.priorFragmentRequired,
    k.priorCommitRequired,
    k.generationBindingRequired,
    k.successorGenerationRequired,
    k.freshFencingRequired,
    k.leaseEpochRequired,
    k.finiteLocalAuthorizationRequired,
    k.singleUseRequired,
    k.openHorizonRequired,
    k.noGlobalCycleLimitRequired,
    k.noGlobalGenerationLimitRequired,
    k.noGlobalTimeHorizonRequired,
    k.optimisticConcurrencyRequired,
    k.atomicReplaceRequired,
    k.atomicStateRequired,
    k.appendOnlyRequired,
    k.immutableReceiptRequired,
    k.rollbackReferenceRequired,
    k.freshRollbackAuthorizationRequired,
    k.rollbackHistoryDeletionForbidden,
    k.sameRootRequired,
    k.commitRecordRequired,
    k.truthForbidden,
    k.causalAttributionForbidden,
    k.rootRewriteForbidden,
    k.historyOverwriteForbidden,
    k.automaticRollbackForbidden,
    k.automaticMissionCompletionForbidden,
    k.planActivationForbidden,
    k.actosInvocationForbidden,
    k.replayRequired,
    k.staleGenerationRejectionRequired,
    k.stalePriorFragmentRejectionRequired,
    k.stalePriorCommitRejectionRequired,
    k.staleFencingRejectionRequired,
    k.staleLeaseRejectionRequired⟩

end AuthorizedAtomicWorldCommit

end KUOS.OpenHorizon
