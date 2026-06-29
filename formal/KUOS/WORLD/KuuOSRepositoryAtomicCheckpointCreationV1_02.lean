import KUOS.WORLD.KuuOSRepositoryLocalFrontierCheckpointAuthorizationV1_01

namespace KUOS.WORLD.KuuOSRepositoryAtomicCheckpointCreationV1_02

structure AtomicCheckpointCreationWitness where
  checkpointAuthorizationValid : Prop
  checkpointAuthorizationGranted : Prop
  authorizationBindingExact : Prop
  executionPolicyValid : Prop
  requestBindingExact : Prop
  executorAuthorized : Prop
  checkpointStateValid : Prop
  checkpointStateBindingExact : Prop
  checkpointStateFresh : Prop
  checkpointReferenceDirect : Prop
  checkpointReferenceNotSymbolic : Prop
  checkpointReferenceStoreSource : Prop
  checkpointWorkingTreeIgnored : Prop
  checkpointReflogIgnored : Prop
  checkpointRemoteIgnored : Prop
  checkpointAbsentBeforeCreation : Prop
  currentOidMatchesExpectedZero : Prop
  nonceRegistryValid : Prop
  nonceRegistryAuthorityExact : Prop
  nonceRegistrySnapshotBound : Prop
  nonceRegistryFresh : Prop
  nonceUnused : Prop
  nonceNotRevoked : Prop
  authorizationNotExpiredAtExecution : Prop
  executionDurationWithinPolicy : Prop
  noFutureEvidence : Prop
  compareAndSwapNonexistenceRequired : Prop
  compareAndSwapAttempted : Bool
  compareAndSwapSucceeded : Bool
  atomicNonceConsumptionRequired : Prop
  atomicCheckpointNonceTransition : Bool
  checkpointCreationTransitionCommitted : Bool
  checkpointStateMutated : Bool
  checkpointCreated : Bool
  nonceConsumed : Bool
  failurePreservedCheckpointState : Bool
  failurePreservedNonceRegistry : Bool
  checkpointOverwritePerformed : Bool
  forceUpdatePerformed : Bool
  referenceDeletePerformed : Bool
  branchUpdated : Bool
  tagUpdated : Bool
  remoteReferenceUpdated : Bool
  pushPerformed : Bool
  indexWritePerformed : Bool
  workingTreeWritePerformed : Bool
  objectDatabaseWritePerformed : Bool
  reflogWritePerformed : Bool
  signingPerformed : Bool
  liveGitCommandInvoked : Bool
  liveRepositoryMutated : Bool

structure AtomicCheckpointCreationWitness.ValidCommitted
    (w : AtomicCheckpointCreationWitness) : Prop where
  checkpointAuthorizationValid : w.checkpointAuthorizationValid
  checkpointAuthorizationGranted : w.checkpointAuthorizationGranted
  authorizationBindingExact : w.authorizationBindingExact
  executionPolicyValid : w.executionPolicyValid
  requestBindingExact : w.requestBindingExact
  executorAuthorized : w.executorAuthorized
  checkpointStateValid : w.checkpointStateValid
  checkpointStateBindingExact : w.checkpointStateBindingExact
  checkpointStateFresh : w.checkpointStateFresh
  checkpointReferenceDirect : w.checkpointReferenceDirect
  checkpointReferenceNotSymbolic : w.checkpointReferenceNotSymbolic
  checkpointReferenceStoreSource : w.checkpointReferenceStoreSource
  checkpointWorkingTreeIgnored : w.checkpointWorkingTreeIgnored
  checkpointReflogIgnored : w.checkpointReflogIgnored
  checkpointRemoteIgnored : w.checkpointRemoteIgnored
  checkpointAbsentBeforeCreation : w.checkpointAbsentBeforeCreation
  currentOidMatchesExpectedZero : w.currentOidMatchesExpectedZero
  nonceRegistryValid : w.nonceRegistryValid
  nonceRegistryAuthorityExact : w.nonceRegistryAuthorityExact
  nonceRegistrySnapshotBound : w.nonceRegistrySnapshotBound
  nonceRegistryFresh : w.nonceRegistryFresh
  nonceUnused : w.nonceUnused
  nonceNotRevoked : w.nonceNotRevoked
  authorizationNotExpiredAtExecution :
    w.authorizationNotExpiredAtExecution
  executionDurationWithinPolicy : w.executionDurationWithinPolicy
  noFutureEvidence : w.noFutureEvidence
  compareAndSwapNonexistenceRequired :
    w.compareAndSwapNonexistenceRequired
  compareAndSwapAttempted : w.compareAndSwapAttempted = true
  compareAndSwapSucceeded : w.compareAndSwapSucceeded = true
  atomicNonceConsumptionRequired : w.atomicNonceConsumptionRequired
  atomicCheckpointNonceTransition :
    w.atomicCheckpointNonceTransition = true
  checkpointCreationTransitionCommitted :
    w.checkpointCreationTransitionCommitted = true
  checkpointStateMutated : w.checkpointStateMutated = true
  checkpointCreated : w.checkpointCreated = true
  nonceConsumed : w.nonceConsumed = true
  checkpointOverwritePerformed : w.checkpointOverwritePerformed = false
  forceUpdatePerformed : w.forceUpdatePerformed = false
  referenceDeletePerformed : w.referenceDeletePerformed = false
  branchUpdated : w.branchUpdated = false
  tagUpdated : w.tagUpdated = false
  remoteReferenceUpdated : w.remoteReferenceUpdated = false
  pushPerformed : w.pushPerformed = false
  indexWritePerformed : w.indexWritePerformed = false
  workingTreeWritePerformed : w.workingTreeWritePerformed = false
  objectDatabaseWritePerformed : w.objectDatabaseWritePerformed = false
  reflogWritePerformed : w.reflogWritePerformed = false
  signingPerformed : w.signingPerformed = false
  liveGitCommandInvoked : w.liveGitCommandInvoked = false
  liveRepositoryMutated : w.liveRepositoryMutated = false

structure AtomicCheckpointCreationWitness.ValidAborted
    (w : AtomicCheckpointCreationWitness) : Prop where
  compareAndSwapSucceeded : w.compareAndSwapSucceeded = false
  atomicCheckpointNonceTransition :
    w.atomicCheckpointNonceTransition = false
  checkpointCreationTransitionCommitted :
    w.checkpointCreationTransitionCommitted = false
  checkpointStateMutated : w.checkpointStateMutated = false
  checkpointCreated : w.checkpointCreated = false
  nonceConsumed : w.nonceConsumed = false
  failurePreservedCheckpointState :
    w.failurePreservedCheckpointState = true
  failurePreservedNonceRegistry :
    w.failurePreservedNonceRegistry = true
  checkpointOverwritePerformed : w.checkpointOverwritePerformed = false
  forceUpdatePerformed : w.forceUpdatePerformed = false
  referenceDeletePerformed : w.referenceDeletePerformed = false
  branchUpdated : w.branchUpdated = false
  tagUpdated : w.tagUpdated = false
  remoteReferenceUpdated : w.remoteReferenceUpdated = false
  pushPerformed : w.pushPerformed = false
  indexWritePerformed : w.indexWritePerformed = false
  workingTreeWritePerformed : w.workingTreeWritePerformed = false
  objectDatabaseWritePerformed : w.objectDatabaseWritePerformed = false
  reflogWritePerformed : w.reflogWritePerformed = false
  signingPerformed : w.signingPerformed = false
  liveGitCommandInvoked : w.liveGitCommandInvoked = false
  liveRepositoryMutated : w.liveRepositoryMutated = false


theorem committed_creation_requires_valid_authorization_and_exact_binding
    (w : AtomicCheckpointCreationWitness)
    (h : w.ValidCommitted) :
    w.checkpointAuthorizationValid ∧
      w.checkpointAuthorizationGranted ∧
      w.authorizationBindingExact ∧
      w.executionPolicyValid ∧
      w.requestBindingExact ∧
      w.executorAuthorized := by
  exact ⟨h.checkpointAuthorizationValid,
    h.checkpointAuthorizationGranted, h.authorizationBindingExact,
    h.executionPolicyValid, h.requestBindingExact, h.executorAuthorized⟩


theorem committed_creation_requires_zero_oid_cas
    (w : AtomicCheckpointCreationWitness)
    (h : w.ValidCommitted) :
    w.checkpointAbsentBeforeCreation ∧
      w.currentOidMatchesExpectedZero ∧
      w.compareAndSwapNonexistenceRequired ∧
      w.compareAndSwapAttempted = true ∧
      w.compareAndSwapSucceeded = true := by
  exact ⟨h.checkpointAbsentBeforeCreation,
    h.currentOidMatchesExpectedZero,
    h.compareAndSwapNonexistenceRequired,
    h.compareAndSwapAttempted, h.compareAndSwapSucceeded⟩


theorem committed_creation_is_atomic_with_nonce_consumption
    (w : AtomicCheckpointCreationWitness)
    (h : w.ValidCommitted) :
    w.atomicNonceConsumptionRequired ∧
      w.atomicCheckpointNonceTransition = true ∧
      w.checkpointCreationTransitionCommitted = true ∧
      w.checkpointStateMutated = true ∧
      w.checkpointCreated = true ∧
      w.nonceConsumed = true := by
  exact ⟨h.atomicNonceConsumptionRequired,
    h.atomicCheckpointNonceTransition,
    h.checkpointCreationTransitionCommitted,
    h.checkpointStateMutated, h.checkpointCreated, h.nonceConsumed⟩


theorem aborted_creation_preserves_checkpoint_and_nonce_states
    (w : AtomicCheckpointCreationWitness)
    (h : w.ValidAborted) :
    w.compareAndSwapSucceeded = false ∧
      w.atomicCheckpointNonceTransition = false ∧
      w.checkpointCreationTransitionCommitted = false ∧
      w.checkpointStateMutated = false ∧
      w.checkpointCreated = false ∧
      w.nonceConsumed = false ∧
      w.failurePreservedCheckpointState = true ∧
      w.failurePreservedNonceRegistry = true := by
  exact ⟨h.compareAndSwapSucceeded,
    h.atomicCheckpointNonceTransition,
    h.checkpointCreationTransitionCommitted,
    h.checkpointStateMutated, h.checkpointCreated, h.nonceConsumed,
    h.failurePreservedCheckpointState,
    h.failurePreservedNonceRegistry⟩


theorem committed_creation_has_no_unrelated_repository_effect
    (w : AtomicCheckpointCreationWitness)
    (h : w.ValidCommitted) :
    w.checkpointOverwritePerformed = false ∧
      w.forceUpdatePerformed = false ∧
      w.referenceDeletePerformed = false ∧
      w.branchUpdated = false ∧ w.tagUpdated = false ∧
      w.remoteReferenceUpdated = false ∧ w.pushPerformed = false ∧
      w.indexWritePerformed = false ∧
      w.workingTreeWritePerformed = false ∧
      w.objectDatabaseWritePerformed = false ∧
      w.reflogWritePerformed = false ∧ w.signingPerformed = false := by
  exact ⟨h.checkpointOverwritePerformed, h.forceUpdatePerformed,
    h.referenceDeletePerformed, h.branchUpdated, h.tagUpdated,
    h.remoteReferenceUpdated, h.pushPerformed, h.indexWritePerformed,
    h.workingTreeWritePerformed, h.objectDatabaseWritePerformed,
    h.reflogWritePerformed, h.signingPerformed⟩


theorem modeled_creation_is_not_live_git_execution
    (w : AtomicCheckpointCreationWitness)
    (h : w.ValidCommitted) :
    w.liveGitCommandInvoked = false ∧
      w.liveRepositoryMutated = false := by
  exact ⟨h.liveGitCommandInvoked, h.liveRepositoryMutated⟩


structure AtomicCheckpointCreationDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_atomic_checkpoint_creation
    {Input Output : Type}
    (derivation : AtomicCheckpointCreationDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryAtomicCheckpointCreationV1_02
