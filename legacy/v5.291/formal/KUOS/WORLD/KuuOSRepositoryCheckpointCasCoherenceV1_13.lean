import KUOS.WORLD.KuuOSRepositoryCheckpointValidatedCasIntakeV1_12

namespace KUOS.WORLD.KuuOSRepositoryCheckpointCasCoherenceV1_13

inductive CoherenceStatus where
  | ready
  | conflict
  | rejected
  deriving DecidableEq, Repr

structure CasCoherenceWitness where
  contractDigestValid : Prop
  contractLocalCoherence : Prop
  intakeDigestValid : Prop
  intakeLocalCoherence : Prop
  exactContractIntakeBinding : Prop
  status : CoherenceStatus
  compareAndSwapRequired : Bool
  repositoryChangeAuthorityGranted : Bool
  executionPerformed : Bool
  liveGitCommandInvoked : Bool

structure CasCoherenceWitness.ValidReady
    (w : CasCoherenceWitness) : Prop where
  contractDigestValid : w.contractDigestValid
  contractLocalCoherence : w.contractLocalCoherence
  intakeDigestValid : w.intakeDigestValid
  intakeLocalCoherence : w.intakeLocalCoherence
  exactContractIntakeBinding : w.exactContractIntakeBinding
  statusReady : w.status = CoherenceStatus.ready
  casRequired : w.compareAndSwapRequired = true
  noAuthority : w.repositoryChangeAuthorityGranted = false
  noExecution : w.executionPerformed = false
  noLiveGit : w.liveGitCommandInvoked = false

structure CasCoherenceWitness.ValidConflict
    (w : CasCoherenceWitness) : Prop where
  contractDigestValid : w.contractDigestValid
  contractLocalCoherence : w.contractLocalCoherence
  intakeDigestValid : w.intakeDigestValid
  intakeLocalCoherence : w.intakeLocalCoherence
  exactContractIntakeBinding : w.exactContractIntakeBinding
  statusConflict : w.status = CoherenceStatus.conflict
  casNotRequired : w.compareAndSwapRequired = false
  noAuthority : w.repositoryChangeAuthorityGranted = false
  noExecution : w.executionPerformed = false
  noLiveGit : w.liveGitCommandInvoked = false


theorem ready_receipt_has_complete_coherence
    (w : CasCoherenceWitness)
    (h : w.ValidReady) :
    w.contractDigestValid ∧ w.contractLocalCoherence ∧
      w.intakeDigestValid ∧ w.intakeLocalCoherence ∧
      w.exactContractIntakeBinding := by
  exact ⟨h.contractDigestValid, h.contractLocalCoherence,
    h.intakeDigestValid, h.intakeLocalCoherence,
    h.exactContractIntakeBinding⟩


theorem ready_receipt_is_nonexecuting
    (w : CasCoherenceWitness)
    (h : w.ValidReady) :
    w.compareAndSwapRequired = true ∧
      w.repositoryChangeAuthorityGranted = false ∧
      w.executionPerformed = false ∧
      w.liveGitCommandInvoked = false := by
  exact ⟨h.casRequired, h.noAuthority, h.noExecution, h.noLiveGit⟩


theorem conflict_receipt_has_complete_coherence
    (w : CasCoherenceWitness)
    (h : w.ValidConflict) :
    w.contractDigestValid ∧ w.contractLocalCoherence ∧
      w.intakeDigestValid ∧ w.intakeLocalCoherence ∧
      w.exactContractIntakeBinding := by
  exact ⟨h.contractDigestValid, h.contractLocalCoherence,
    h.intakeDigestValid, h.intakeLocalCoherence,
    h.exactContractIntakeBinding⟩


theorem conflict_receipt_never_requests_cas
    (w : CasCoherenceWitness)
    (h : w.ValidConflict) :
    w.compareAndSwapRequired = false ∧
      w.repositoryChangeAuthorityGranted = false ∧
      w.executionPerformed = false ∧
      w.liveGitCommandInvoked = false := by
  exact ⟨h.casNotRequired, h.noAuthority, h.noExecution, h.noLiveGit⟩

structure CoherenceDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_coherence_receipt
    {Input Output : Type}
    (derivation : CoherenceDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryCheckpointCasCoherenceV1_13
