import KUOS.WORLD.KuuOSRepositoryCheckpointCreationReceiptV1_03

namespace KUOS.WORLD.KuuOSRepositoryCheckpointStabilityV1_04

inductive CheckpointStabilityFailure where
  | none
  | evidenceInvalid
  | checkpointLost
  | checkpointSubstituted
  | checkpointNameConflict
  | checkpointObjectUnreachable
  | checkpointUnstableWindow
  deriving DecidableEq, Repr

structure CheckpointStabilityWitness where
  creationReceiptValid : Prop
  creationReceiptCommitted : Prop
  evidenceBindingExact : Prop
  delayedReferenceDirect : Prop
  delayedReferencePresent : Prop
  delayedOidExact : Prop
  objectReachable : Prop
  checkpointNameUnique : Prop
  stabilityIntervalBounded : Prop
  observationSequenceOrdered : Prop
  noFutureEvidence : Prop
  immutableByDefault : Prop
  failure : CheckpointStabilityFailure
  stabilityConfirmed : Bool
  checkpointOverwriteAuthorized : Bool
  checkpointDeleteAuthorized : Bool
  forceUpdateAuthorized : Bool
  restoreAuthorized : Bool
  recoveryAuthorized : Bool
  remoteUpdateAuthorized : Bool
  pushAuthorized : Bool
  referenceMutationPerformed : Bool
  objectWritePerformed : Bool
  liveGitCommandInvoked : Bool
  liveRepositoryMutated : Bool

structure CheckpointStabilityWitness.ValidStable
    (w : CheckpointStabilityWitness) : Prop where
  creationReceiptValid : w.creationReceiptValid
  creationReceiptCommitted : w.creationReceiptCommitted
  evidenceBindingExact : w.evidenceBindingExact
  delayedReferenceDirect : w.delayedReferenceDirect
  delayedReferencePresent : w.delayedReferencePresent
  delayedOidExact : w.delayedOidExact
  objectReachable : w.objectReachable
  checkpointNameUnique : w.checkpointNameUnique
  stabilityIntervalBounded : w.stabilityIntervalBounded
  observationSequenceOrdered : w.observationSequenceOrdered
  noFutureEvidence : w.noFutureEvidence
  immutableByDefault : w.immutableByDefault
  failureNone : w.failure = CheckpointStabilityFailure.none
  stabilityConfirmed : w.stabilityConfirmed = true
  checkpointOverwriteAuthorized : w.checkpointOverwriteAuthorized = false
  checkpointDeleteAuthorized : w.checkpointDeleteAuthorized = false
  forceUpdateAuthorized : w.forceUpdateAuthorized = false
  restoreAuthorized : w.restoreAuthorized = false
  recoveryAuthorized : w.recoveryAuthorized = false
  remoteUpdateAuthorized : w.remoteUpdateAuthorized = false
  pushAuthorized : w.pushAuthorized = false
  referenceMutationPerformed : w.referenceMutationPerformed = false
  objectWritePerformed : w.objectWritePerformed = false
  liveGitCommandInvoked : w.liveGitCommandInvoked = false
  liveRepositoryMutated : w.liveRepositoryMutated = false

structure CheckpointStabilityWitness.ValidFailure
    (w : CheckpointStabilityWitness) : Prop where
  failurePresent : w.failure ≠ CheckpointStabilityFailure.none
  stabilityRejected : w.stabilityConfirmed = false
  restoreAuthorized : w.restoreAuthorized = false
  recoveryAuthorized : w.recoveryAuthorized = false
  forceUpdateAuthorized : w.forceUpdateAuthorized = false
  checkpointDeleteAuthorized : w.checkpointDeleteAuthorized = false
  liveGitCommandInvoked : w.liveGitCommandInvoked = false
  liveRepositoryMutated : w.liveRepositoryMutated = false


theorem stable_checkpoint_requires_exact_delayed_evidence
    (w : CheckpointStabilityWitness)
    (h : w.ValidStable) :
    w.creationReceiptValid ∧
      w.creationReceiptCommitted ∧
      w.evidenceBindingExact ∧
      w.delayedReferenceDirect ∧
      w.delayedReferencePresent ∧
      w.delayedOidExact ∧
      w.objectReachable ∧
      w.checkpointNameUnique := by
  exact ⟨h.creationReceiptValid, h.creationReceiptCommitted,
    h.evidenceBindingExact, h.delayedReferenceDirect,
    h.delayedReferencePresent, h.delayedOidExact,
    h.objectReachable, h.checkpointNameUnique⟩


theorem stable_checkpoint_is_immutable_by_default
    (w : CheckpointStabilityWitness)
    (h : w.ValidStable) :
    w.immutableByDefault ∧
      w.checkpointOverwriteAuthorized = false ∧
      w.checkpointDeleteAuthorized = false ∧
      w.forceUpdateAuthorized = false := by
  exact ⟨h.immutableByDefault, h.checkpointOverwriteAuthorized,
    h.checkpointDeleteAuthorized, h.forceUpdateAuthorized⟩


theorem stability_failure_does_not_authorize_recovery
    (w : CheckpointStabilityWitness)
    (h : w.ValidFailure) :
    w.restoreAuthorized = false ∧
      w.recoveryAuthorized = false ∧
      w.forceUpdateAuthorized = false ∧
      w.checkpointDeleteAuthorized = false := by
  exact ⟨h.restoreAuthorized, h.recoveryAuthorized,
    h.forceUpdateAuthorized, h.checkpointDeleteAuthorized⟩


theorem stability_verification_performs_no_repository_mutation
    (w : CheckpointStabilityWitness)
    (h : w.ValidStable) :
    w.referenceMutationPerformed = false ∧
      w.objectWritePerformed = false ∧
      w.liveGitCommandInvoked = false ∧
      w.liveRepositoryMutated = false := by
  exact ⟨h.referenceMutationPerformed, h.objectWritePerformed,
    h.liveGitCommandInvoked, h.liveRepositoryMutated⟩


structure CheckpointStabilityDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_checkpoint_stability_certificate
    {Input Output : Type}
    (derivation : CheckpointStabilityDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryCheckpointStabilityV1_04
