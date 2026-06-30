import KUOS.WORLD.KuuOSCheckpointCandidateValidationV1_11

namespace KUOS.WORLD.KuuOSRepositoryCheckpointValidatedCasIntakeV1_12

inductive IntakeStatus where
  | ready
  | conflict
  | rejected
  deriving DecidableEq, Repr

structure ValidatedCasIntakeWitness where
  validationReceiptValid : Prop
  upstreamChainRevalidated : Prop
  contractValid : Prop
  candidateBindingExact : Prop
  repositoryBindingExact : Prop
  checkpointBindingExact : Prop
  oidBindingExact : Prop
  status : IntakeStatus
  compareAndSwapRequired : Bool
  repositoryChangeAuthorityGranted : Bool
  executionPerformed : Bool
  liveGitCommandInvoked : Bool

structure ValidatedCasIntakeWitness.ValidReady
    (w : ValidatedCasIntakeWitness) : Prop where
  validationReceiptValid : w.validationReceiptValid
  upstreamChainRevalidated : w.upstreamChainRevalidated
  contractValid : w.contractValid
  candidateBindingExact : w.candidateBindingExact
  repositoryBindingExact : w.repositoryBindingExact
  checkpointBindingExact : w.checkpointBindingExact
  oidBindingExact : w.oidBindingExact
  statusReady : w.status = IntakeStatus.ready
  casRequired : w.compareAndSwapRequired = true
  noAuthority : w.repositoryChangeAuthorityGranted = false
  noExecution : w.executionPerformed = false
  noLiveGit : w.liveGitCommandInvoked = false

structure ValidatedCasIntakeWitness.ValidConflict
    (w : ValidatedCasIntakeWitness) : Prop where
  validationReceiptValid : w.validationReceiptValid
  upstreamChainRevalidated : w.upstreamChainRevalidated
  contractValid : w.contractValid
  candidateBindingExact : w.candidateBindingExact
  repositoryBindingExact : w.repositoryBindingExact
  checkpointBindingExact : w.checkpointBindingExact
  oidBindingExact : w.oidBindingExact
  statusConflict : w.status = IntakeStatus.conflict
  casNotRequired : w.compareAndSwapRequired = false
  noAuthority : w.repositoryChangeAuthorityGranted = false
  noExecution : w.executionPerformed = false
  noLiveGit : w.liveGitCommandInvoked = false


theorem ready_intake_has_complete_validated_binding
    (w : ValidatedCasIntakeWitness)
    (h : w.ValidReady) :
    w.validationReceiptValid ∧ w.upstreamChainRevalidated ∧
      w.contractValid ∧ w.candidateBindingExact ∧
      w.repositoryBindingExact ∧ w.checkpointBindingExact ∧
      w.oidBindingExact := by
  exact ⟨h.validationReceiptValid, h.upstreamChainRevalidated,
    h.contractValid, h.candidateBindingExact, h.repositoryBindingExact,
    h.checkpointBindingExact, h.oidBindingExact⟩


theorem ready_intake_is_nonexecuting
    (w : ValidatedCasIntakeWitness)
    (h : w.ValidReady) :
    w.compareAndSwapRequired = true ∧
      w.repositoryChangeAuthorityGranted = false ∧
      w.executionPerformed = false ∧
      w.liveGitCommandInvoked = false := by
  exact ⟨h.casRequired, h.noAuthority, h.noExecution, h.noLiveGit⟩


theorem conflict_intake_never_requests_cas
    (w : ValidatedCasIntakeWitness)
    (h : w.ValidConflict) :
    w.compareAndSwapRequired = false ∧
      w.repositoryChangeAuthorityGranted = false ∧
      w.executionPerformed = false ∧
      w.liveGitCommandInvoked = false := by
  exact ⟨h.casNotRequired, h.noAuthority, h.noExecution, h.noLiveGit⟩

structure IntakeDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_validated_cas_intake
    {Input Output : Type}
    (derivation : IntakeDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryCheckpointValidatedCasIntakeV1_12
