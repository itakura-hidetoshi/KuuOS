import KUOS.WORLD.KuuOSRepositoryReferenceUpdateV0_96

namespace KUOS.WORLD.KuuOSRepositoryAtomicReferenceUpdateV0_97

structure AtomicReferenceUpdateWitness where
  repositoryBound : Prop
  referenceBound : Prop
  oldOidBound : Prop
  newOidBound : Prop
  authorizationValid : Prop
  authorizationGranted : Prop
  compareAndSwapRequired : Prop
  compareAndSwapSucceeded : Prop
  nonceUnusedBefore : Prop
  nonceConsumedAfter : Prop
  atomicReferenceNonceTransition : Prop
  committed : Bool
  aborted : Bool
  failurePreservedReferenceState : Bool
  failurePreservedNonceRegistry : Bool
  forceUpdatePerformed : Bool
  referenceDeletePerformed : Bool
  headUpdated : Bool
  tagUpdated : Bool
  remoteReferenceUpdated : Bool
  pushPerformed : Bool
  indexWritePerformed : Bool
  workingTreeWritePerformed : Bool
  objectDatabaseWritePerformed : Bool
  signingPerformed : Bool
  liveGitCommandInvoked : Bool
  liveRepositoryMutated : Bool

structure AtomicReferenceUpdateWitness.ValidCommitted
    (w : AtomicReferenceUpdateWitness) : Prop where
  repositoryBound : w.repositoryBound
  referenceBound : w.referenceBound
  oldOidBound : w.oldOidBound
  newOidBound : w.newOidBound
  authorizationValid : w.authorizationValid
  authorizationGranted : w.authorizationGranted
  compareAndSwapRequired : w.compareAndSwapRequired
  compareAndSwapSucceeded : w.compareAndSwapSucceeded
  nonceUnusedBefore : w.nonceUnusedBefore
  nonceConsumedAfter : w.nonceConsumedAfter
  atomicReferenceNonceTransition : w.atomicReferenceNonceTransition
  committed : w.committed = true
  aborted : w.aborted = false
  forceUpdatePerformed : w.forceUpdatePerformed = false
  referenceDeletePerformed : w.referenceDeletePerformed = false
  headUpdated : w.headUpdated = false
  tagUpdated : w.tagUpdated = false
  remoteReferenceUpdated : w.remoteReferenceUpdated = false
  pushPerformed : w.pushPerformed = false
  indexWritePerformed : w.indexWritePerformed = false
  workingTreeWritePerformed : w.workingTreeWritePerformed = false
  objectDatabaseWritePerformed : w.objectDatabaseWritePerformed = false
  signingPerformed : w.signingPerformed = false
  liveGitCommandInvoked : w.liveGitCommandInvoked = false
  liveRepositoryMutated : w.liveRepositoryMutated = false

structure AtomicReferenceUpdateWitness.ValidAborted
    (w : AtomicReferenceUpdateWitness) : Prop where
  committed : w.committed = false
  aborted : w.aborted = true
  failurePreservedReferenceState : w.failurePreservedReferenceState = true
  failurePreservedNonceRegistry : w.failurePreservedNonceRegistry = true
  forceUpdatePerformed : w.forceUpdatePerformed = false
  referenceDeletePerformed : w.referenceDeletePerformed = false
  pushPerformed : w.pushPerformed = false
  liveGitCommandInvoked : w.liveGitCommandInvoked = false
  liveRepositoryMutated : w.liveRepositoryMutated = false


theorem committed_binds_exact_repository_reference_and_oids
    (w : AtomicReferenceUpdateWitness)
    (h : w.ValidCommitted) :
    w.repositoryBound ∧ w.referenceBound ∧ w.oldOidBound ∧ w.newOidBound := by
  exact ⟨h.repositoryBound, h.referenceBound, h.oldOidBound, h.newOidBound⟩


theorem committed_requires_valid_authorization
    (w : AtomicReferenceUpdateWitness)
    (h : w.ValidCommitted) :
    w.authorizationValid ∧ w.authorizationGranted := by
  exact ⟨h.authorizationValid, h.authorizationGranted⟩


theorem committed_is_atomic_compare_and_swap_with_nonce_consumption
    (w : AtomicReferenceUpdateWitness)
    (h : w.ValidCommitted) :
    w.compareAndSwapRequired ∧ w.compareAndSwapSucceeded ∧
      w.nonceUnusedBefore ∧ w.nonceConsumedAfter ∧
      w.atomicReferenceNonceTransition := by
  exact ⟨h.compareAndSwapRequired, h.compareAndSwapSucceeded,
    h.nonceUnusedBefore, h.nonceConsumedAfter,
    h.atomicReferenceNonceTransition⟩


theorem aborted_preserves_reference_and_nonce_registry
    (w : AtomicReferenceUpdateWitness)
    (h : w.ValidAborted) :
    w.failurePreservedReferenceState = true ∧
      w.failurePreservedNonceRegistry = true := by
  exact ⟨h.failurePreservedReferenceState, h.failurePreservedNonceRegistry⟩


theorem committed_grants_no_force_delete_push_or_unrelated_effect
    (w : AtomicReferenceUpdateWitness)
    (h : w.ValidCommitted) :
    w.forceUpdatePerformed = false ∧
      w.referenceDeletePerformed = false ∧
      w.headUpdated = false ∧ w.tagUpdated = false ∧
      w.remoteReferenceUpdated = false ∧ w.pushPerformed = false ∧
      w.indexWritePerformed = false ∧
      w.workingTreeWritePerformed = false ∧
      w.objectDatabaseWritePerformed = false ∧
      w.signingPerformed = false := by
  exact ⟨h.forceUpdatePerformed, h.referenceDeletePerformed,
    h.headUpdated, h.tagUpdated, h.remoteReferenceUpdated,
    h.pushPerformed, h.indexWritePerformed, h.workingTreeWritePerformed,
    h.objectDatabaseWritePerformed, h.signingPerformed⟩


theorem committed_is_not_live_git_execution
    (w : AtomicReferenceUpdateWitness)
    (h : w.ValidCommitted) :
    w.liveGitCommandInvoked = false ∧ w.liveRepositoryMutated = false := by
  exact ⟨h.liveGitCommandInvoked, h.liveRepositoryMutated⟩


structure AtomicReferenceUpdateDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_atomic_reference_update
    {Input Output : Type}
    (derivation : AtomicReferenceUpdateDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryAtomicReferenceUpdateV0_97
