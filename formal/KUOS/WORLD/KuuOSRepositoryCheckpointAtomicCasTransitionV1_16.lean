import KUOS.WORLD.KuuOSRepositoryCheckpointCasAuthorizationDecisionV1_15

namespace KUOS.WORLD.KuuOSRepositoryCheckpointAtomicCasTransitionV1_16

inductive TransitionStatus where
  | committed
  | aborted
  deriving DecidableEq, Repr

structure AtomicCasTransitionWitness where
  authorizationValid : Prop
  authorizationGranted : Prop
  authorizationBindingExact : Prop
  transitionPolicyValid : Prop
  transitionRequestValid : Prop
  transitionRequestBindingExact : Prop
  executorAuthorized : Prop
  referenceStateValid : Prop
  referenceStateBindingExact : Prop
  referenceStateFresh : Prop
  currentOidMatchesExpected : Prop
  nonceRegistryValid : Prop
  nonceRegistryBound : Prop
  nonceRegistryFresh : Prop
  nonceUnused : Prop
  nonceNotRevoked : Prop
  authorizationNotExpired : Prop
  executionDurationWithinPolicy : Prop
  noFutureEvidence : Prop
  status : TransitionStatus
  compareAndSwapAttempted : Bool
  compareAndSwapSucceeded : Bool
  atomicReferenceNonceTransition : Bool
  modeledReferenceStateMutated : Bool
  modeledNonceRegistryMutated : Bool
  nonceConsumed : Bool
  sourceReferenceStatePreserved : Bool
  sourceNonceRegistryPreserved : Bool
  liveGitCommandInvoked : Bool
  liveRepositoryMutated : Bool

structure AtomicCasTransitionWitness.ValidCommitted
    (w : AtomicCasTransitionWitness) : Prop where
  authorizationValid : w.authorizationValid
  authorizationGranted : w.authorizationGranted
  authorizationBindingExact : w.authorizationBindingExact
  transitionPolicyValid : w.transitionPolicyValid
  transitionRequestValid : w.transitionRequestValid
  transitionRequestBindingExact : w.transitionRequestBindingExact
  executorAuthorized : w.executorAuthorized
  referenceStateValid : w.referenceStateValid
  referenceStateBindingExact : w.referenceStateBindingExact
  referenceStateFresh : w.referenceStateFresh
  currentOidMatchesExpected : w.currentOidMatchesExpected
  nonceRegistryValid : w.nonceRegistryValid
  nonceRegistryBound : w.nonceRegistryBound
  nonceRegistryFresh : w.nonceRegistryFresh
  nonceUnused : w.nonceUnused
  nonceNotRevoked : w.nonceNotRevoked
  authorizationNotExpired : w.authorizationNotExpired
  executionDurationWithinPolicy : w.executionDurationWithinPolicy
  noFutureEvidence : w.noFutureEvidence
  statusCommitted : w.status = TransitionStatus.committed
  casAttempted : w.compareAndSwapAttempted = true
  casSucceeded : w.compareAndSwapSucceeded = true
  atomicTransition : w.atomicReferenceNonceTransition = true
  referenceMutated : w.modeledReferenceStateMutated = true
  nonceRegistryMutated : w.modeledNonceRegistryMutated = true
  nonceConsumed : w.nonceConsumed = true
  noLiveGit : w.liveGitCommandInvoked = false
  noLiveMutation : w.liveRepositoryMutated = false

structure AtomicCasTransitionWitness.ValidAborted
    (w : AtomicCasTransitionWitness) : Prop where
  statusAborted : w.status = TransitionStatus.aborted
  casNotSucceeded : w.compareAndSwapSucceeded = false
  noAtomicTransition : w.atomicReferenceNonceTransition = false
  referenceNotMutated : w.modeledReferenceStateMutated = false
  nonceRegistryNotMutated : w.modeledNonceRegistryMutated = false
  nonceNotConsumed : w.nonceConsumed = false
  referencePreserved : w.sourceReferenceStatePreserved = true
  nonceRegistryPreserved : w.sourceNonceRegistryPreserved = true
  noLiveGit : w.liveGitCommandInvoked = false
  noLiveMutation : w.liveRepositoryMutated = false


theorem committed_transition_has_complete_preconditions
    (w : AtomicCasTransitionWitness)
    (h : w.ValidCommitted) :
    w.authorizationValid ∧ w.authorizationGranted ∧
      w.authorizationBindingExact ∧ w.transitionPolicyValid ∧
      w.transitionRequestValid ∧ w.transitionRequestBindingExact ∧
      w.executorAuthorized ∧ w.referenceStateValid ∧
      w.referenceStateBindingExact ∧ w.referenceStateFresh ∧
      w.currentOidMatchesExpected ∧ w.nonceRegistryValid ∧
      w.nonceRegistryBound ∧ w.nonceRegistryFresh ∧
      w.nonceUnused ∧ w.nonceNotRevoked ∧
      w.authorizationNotExpired ∧ w.executionDurationWithinPolicy ∧
      w.noFutureEvidence := by
  exact ⟨h.authorizationValid, h.authorizationGranted,
    h.authorizationBindingExact, h.transitionPolicyValid,
    h.transitionRequestValid, h.transitionRequestBindingExact,
    h.executorAuthorized, h.referenceStateValid,
    h.referenceStateBindingExact, h.referenceStateFresh,
    h.currentOidMatchesExpected, h.nonceRegistryValid,
    h.nonceRegistryBound, h.nonceRegistryFresh, h.nonceUnused,
    h.nonceNotRevoked, h.authorizationNotExpired,
    h.executionDurationWithinPolicy, h.noFutureEvidence⟩


theorem committed_transition_is_atomic_and_model_only
    (w : AtomicCasTransitionWitness)
    (h : w.ValidCommitted) :
    w.compareAndSwapAttempted = true ∧
      w.compareAndSwapSucceeded = true ∧
      w.atomicReferenceNonceTransition = true ∧
      w.modeledReferenceStateMutated = true ∧
      w.modeledNonceRegistryMutated = true ∧
      w.nonceConsumed = true ∧
      w.liveGitCommandInvoked = false ∧
      w.liveRepositoryMutated = false := by
  exact ⟨h.casAttempted, h.casSucceeded, h.atomicTransition,
    h.referenceMutated, h.nonceRegistryMutated, h.nonceConsumed,
    h.noLiveGit, h.noLiveMutation⟩


theorem aborted_transition_preserves_both_source_states
    (w : AtomicCasTransitionWitness)
    (h : w.ValidAborted) :
    w.compareAndSwapSucceeded = false ∧
      w.atomicReferenceNonceTransition = false ∧
      w.modeledReferenceStateMutated = false ∧
      w.modeledNonceRegistryMutated = false ∧
      w.nonceConsumed = false ∧
      w.sourceReferenceStatePreserved = true ∧
      w.sourceNonceRegistryPreserved = true ∧
      w.liveGitCommandInvoked = false ∧
      w.liveRepositoryMutated = false := by
  exact ⟨h.casNotSucceeded, h.noAtomicTransition,
    h.referenceNotMutated, h.nonceRegistryNotMutated,
    h.nonceNotConsumed, h.referencePreserved,
    h.nonceRegistryPreserved, h.noLiveGit, h.noLiveMutation⟩

structure TransitionDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_atomic_cas_transition
    {Input Output : Type}
    (derivation : TransitionDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryCheckpointAtomicCasTransitionV1_16
