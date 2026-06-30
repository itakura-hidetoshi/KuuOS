import KUOS.WORLD.KuuOSRepositoryCheckpointCasContractV1_10

namespace KUOS.WORLD.KuuOSRepositoryCheckpointCandidateRevalidationV1_11

inductive ReceiptStatus where
  | valid
  | rejected
  deriving DecidableEq, Repr

inductive ReceiptReason where
  | fullV109RevalidationPassed
  | candidateStale
  | invalidEvidence
  deriving DecidableEq, Repr

structure CandidateRevalidationWitness where
  completeV109RevalidationPassed : Prop
  repositoryBindingExact : Prop
  candidateFresh : Prop
  status : ReceiptStatus
  reason : ReceiptReason
  repositoryChangeAuthorityGranted : Bool
  executionPerformed : Bool
  liveGitCommandInvoked : Bool

structure CandidateRevalidationWitness.Valid
    (w : CandidateRevalidationWitness) : Prop where
  completeReplay : w.completeV109RevalidationPassed
  bindingExact : w.repositoryBindingExact
  candidateFresh : w.candidateFresh
  statusValid : w.status = ReceiptStatus.valid
  reasonPassed : w.reason = ReceiptReason.fullV109RevalidationPassed
  noAuthority : w.repositoryChangeAuthorityGranted = false
  noExecution : w.executionPerformed = false
  noLiveGit : w.liveGitCommandInvoked = false

structure CandidateRevalidationWitness.ValidStaleRejection
    (w : CandidateRevalidationWitness) : Prop where
  completeReplay : w.completeV109RevalidationPassed
  bindingExact : w.repositoryBindingExact
  candidateNotFresh : ¬ w.candidateFresh
  statusRejected : w.status = ReceiptStatus.rejected
  reasonStale : w.reason = ReceiptReason.candidateStale
  noAuthority : w.repositoryChangeAuthorityGranted = false
  noExecution : w.executionPerformed = false

structure CandidateRevalidationWitness.ValidInvalidRejection
    (w : CandidateRevalidationWitness) : Prop where
  statusRejected : w.status = ReceiptStatus.rejected
  reasonInvalid : w.reason = ReceiptReason.invalidEvidence
  noAuthority : w.repositoryChangeAuthorityGranted = false
  noExecution : w.executionPerformed = false
  noLiveGit : w.liveGitCommandInvoked = false


theorem valid_receipt_requires_complete_replay
    (w : CandidateRevalidationWitness)
    (h : w.Valid) :
    w.completeV109RevalidationPassed ∧
      w.repositoryBindingExact ∧
      w.candidateFresh := by
  exact ⟨h.completeReplay, h.bindingExact, h.candidateFresh⟩


theorem valid_receipt_is_nonexecuting
    (w : CandidateRevalidationWitness)
    (h : w.Valid) :
    w.repositoryChangeAuthorityGranted = false ∧
      w.executionPerformed = false ∧
      w.liveGitCommandInvoked = false := by
  exact ⟨h.noAuthority, h.noExecution, h.noLiveGit⟩


theorem stale_receipt_preserves_replay_without_authority
    (w : CandidateRevalidationWitness)
    (h : w.ValidStaleRejection) :
    w.completeV109RevalidationPassed ∧
      w.status = ReceiptStatus.rejected ∧
      w.repositoryChangeAuthorityGranted = false ∧
      w.executionPerformed = false := by
  exact ⟨h.completeReplay, h.statusRejected, h.noAuthority, h.noExecution⟩

structure RevalidationDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_revalidation_receipt
    {Input Output : Type}
    (derivation : RevalidationDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryCheckpointCandidateRevalidationV1_11
