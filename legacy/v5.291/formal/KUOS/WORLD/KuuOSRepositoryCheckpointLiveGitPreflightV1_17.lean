import KUOS.WORLD.KuuOSRepositoryCheckpointAtomicCasTransitionV1_16

namespace KUOS.WORLD.KuuOSRepositoryCheckpointLiveGitPreflightV1_17

inductive PreflightStatus where
  | ready
  | rejected
  | error
  deriving DecidableEq, Repr

structure LiveGitPreflightWitness where
  transitionValid : Prop
  transitionCommitted : Prop
  transitionBindingExact : Prop
  repositoryPathValid : Prop
  repositoryRootResolved : Prop
  gitDirectoryResolved : Prop
  repositoryNonBare : Prop
  checkpointReferenceValid : Prop
  checkpointReferenceExists : Prop
  checkpointReferenceDirect : Prop
  observedOidMatchesExpected : Prop
  expectedObjectExists : Prop
  proposedObjectExists : Prop
  commandPolicyValid : Prop
  allCommandsBounded : Prop
  allCommandsReadOnly : Prop
  optionalLocksDisabled : Prop
  shellUsed : Bool
  status : PreflightStatus
  liveGitCommandInvoked : Bool
  liveRepositoryMutated : Bool
  objectDatabaseWritePerformed : Bool
  indexWritePerformed : Bool
  workingTreeWritePerformed : Bool
  reflogWritePerformed : Bool

structure LiveGitPreflightWitness.ValidReady
    (w : LiveGitPreflightWitness) : Prop where
  transitionValid : w.transitionValid
  transitionCommitted : w.transitionCommitted
  transitionBindingExact : w.transitionBindingExact
  repositoryPathValid : w.repositoryPathValid
  repositoryRootResolved : w.repositoryRootResolved
  gitDirectoryResolved : w.gitDirectoryResolved
  repositoryNonBare : w.repositoryNonBare
  checkpointReferenceValid : w.checkpointReferenceValid
  checkpointReferenceExists : w.checkpointReferenceExists
  checkpointReferenceDirect : w.checkpointReferenceDirect
  observedOidMatchesExpected : w.observedOidMatchesExpected
  expectedObjectExists : w.expectedObjectExists
  proposedObjectExists : w.proposedObjectExists
  commandPolicyValid : w.commandPolicyValid
  allCommandsBounded : w.allCommandsBounded
  allCommandsReadOnly : w.allCommandsReadOnly
  optionalLocksDisabled : w.optionalLocksDisabled
  statusReady : w.status = PreflightStatus.ready
  noShell : w.shellUsed = false
  liveGitInvoked : w.liveGitCommandInvoked = true
  noLiveMutation : w.liveRepositoryMutated = false
  noObjectWrite : w.objectDatabaseWritePerformed = false
  noIndexWrite : w.indexWritePerformed = false
  noWorkingTreeWrite : w.workingTreeWritePerformed = false
  noReflogWrite : w.reflogWritePerformed = false


theorem ready_preflight_has_complete_live_observation
    (w : LiveGitPreflightWitness)
    (h : w.ValidReady) :
    w.transitionValid ∧ w.transitionCommitted ∧
      w.transitionBindingExact ∧ w.repositoryPathValid ∧
      w.repositoryRootResolved ∧ w.gitDirectoryResolved ∧
      w.repositoryNonBare ∧ w.checkpointReferenceValid ∧
      w.checkpointReferenceExists ∧ w.checkpointReferenceDirect ∧
      w.observedOidMatchesExpected ∧ w.expectedObjectExists ∧
      w.proposedObjectExists ∧ w.commandPolicyValid ∧
      w.allCommandsBounded ∧ w.allCommandsReadOnly ∧
      w.optionalLocksDisabled := by
  exact ⟨h.transitionValid, h.transitionCommitted,
    h.transitionBindingExact, h.repositoryPathValid,
    h.repositoryRootResolved, h.gitDirectoryResolved,
    h.repositoryNonBare, h.checkpointReferenceValid,
    h.checkpointReferenceExists, h.checkpointReferenceDirect,
    h.observedOidMatchesExpected, h.expectedObjectExists,
    h.proposedObjectExists, h.commandPolicyValid,
    h.allCommandsBounded, h.allCommandsReadOnly,
    h.optionalLocksDisabled⟩


theorem ready_preflight_invokes_git_without_write_capability
    (w : LiveGitPreflightWitness)
    (h : w.ValidReady) :
    w.shellUsed = false ∧
      w.liveGitCommandInvoked = true ∧
      w.liveRepositoryMutated = false ∧
      w.objectDatabaseWritePerformed = false ∧
      w.indexWritePerformed = false ∧
      w.workingTreeWritePerformed = false ∧
      w.reflogWritePerformed = false := by
  exact ⟨h.noShell, h.liveGitInvoked, h.noLiveMutation,
    h.noObjectWrite, h.noIndexWrite, h.noWorkingTreeWrite,
    h.noReflogWrite⟩

structure PreflightDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_live_git_preflight
    {Input Output : Type}
    (derivation : PreflightDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryCheckpointLiveGitPreflightV1_17
