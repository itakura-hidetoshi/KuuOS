import KUOS.WORLD.KuuOSRepositoryCheckpointCandidateV1_09

namespace KUOS.WORLD.KuuOSRepositoryCheckpointCasContractV1_10

inductive ContractStatus where
  | none
  | ready
  | conflict
  | rejected
  deriving DecidableEq, Repr

inductive ContractReason where
  | noReadyCandidate
  | expectedOidConfirmed
  | currentOidChanged
  | invalidEvidence
  deriving DecidableEq, Repr

structure CheckpointCasContractWitness where
  candidateValid : Prop
  repositoryBindingExact : Prop
  readyCandidate : Prop
  expectedOidNonzero : Prop
  proposedOidNonzero : Prop
  oidsDistinct : Prop
  observedMatchesExpected : Prop
  status : ContractStatus
  reason : ContractReason
  compareAndSwapRequired : Bool
  checkpointNamespaceOnly : Bool
  repositoryChangeAuthorityGranted : Bool
  executionPerformed : Bool
  liveGitCommandInvoked : Bool

structure CheckpointCasContractWitness.ValidReady
    (w : CheckpointCasContractWitness) : Prop where
  candidateValid : w.candidateValid
  repositoryBindingExact : w.repositoryBindingExact
  readyCandidate : w.readyCandidate
  expectedOidNonzero : w.expectedOidNonzero
  proposedOidNonzero : w.proposedOidNonzero
  oidsDistinct : w.oidsDistinct
  observedMatchesExpected : w.observedMatchesExpected
  statusReady : w.status = ContractStatus.ready
  reasonConfirmed : w.reason = ContractReason.expectedOidConfirmed
  casRequired : w.compareAndSwapRequired = true
  namespaceOnly : w.checkpointNamespaceOnly = true
  noAuthority : w.repositoryChangeAuthorityGranted = false
  noExecution : w.executionPerformed = false
  noLiveGit : w.liveGitCommandInvoked = false

structure CheckpointCasContractWitness.ValidConflict
    (w : CheckpointCasContractWitness) : Prop where
  statusConflict : w.status = ContractStatus.conflict
  reasonChanged : w.reason = ContractReason.currentOidChanged
  casNotRequired : w.compareAndSwapRequired = false
  noAuthority : w.repositoryChangeAuthorityGranted = false
  noExecution : w.executionPerformed = false


theorem ready_contract_is_nonexecuting
    (w : CheckpointCasContractWitness)
    (h : w.ValidReady) :
    w.compareAndSwapRequired = true ∧
      w.checkpointNamespaceOnly = true ∧
      w.repositoryChangeAuthorityGranted = false ∧
      w.executionPerformed = false ∧
      w.liveGitCommandInvoked = false := by
  exact ⟨h.casRequired, h.namespaceOnly, h.noAuthority, h.noExecution, h.noLiveGit⟩


theorem ready_contract_has_distinct_nonzero_oids
    (w : CheckpointCasContractWitness)
    (h : w.ValidReady) :
    w.expectedOidNonzero ∧ w.proposedOidNonzero ∧ w.oidsDistinct := by
  exact ⟨h.expectedOidNonzero, h.proposedOidNonzero, h.oidsDistinct⟩


theorem conflict_contract_never_requests_cas
    (w : CheckpointCasContractWitness)
    (h : w.ValidConflict) :
    w.compareAndSwapRequired = false ∧
      w.repositoryChangeAuthorityGranted = false ∧
      w.executionPerformed = false := by
  exact ⟨h.casNotRequired, h.noAuthority, h.noExecution⟩

structure ContractDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_checkpoint_cas_contract
    {Input Output : Type}
    (derivation : ContractDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryCheckpointCasContractV1_10
