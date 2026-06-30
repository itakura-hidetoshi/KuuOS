import KUOS.WORLD.KuuOSRepositoryCheckpointCasContractV1_10

namespace KUOS.WORLD.KuuOSCheckpointCandidateValidationV1_11

inductive ValidationStatus where
  | valid
  | rejected
  deriving DecidableEq, Repr

structure ValidationWitness where
  upstreamChainRevalidated : Prop
  readyCandidate : Prop
  repositoryMatches : Prop
  checkpointMatches : Prop
  distinctNonzeroOids : Prop
  status : ValidationStatus
  operationPerformed : Bool

structure ValidationWitness.Valid (w : ValidationWitness) : Prop where
  upstreamChainRevalidated : w.upstreamChainRevalidated
  readyCandidate : w.readyCandidate
  repositoryMatches : w.repositoryMatches
  checkpointMatches : w.checkpointMatches
  distinctNonzeroOids : w.distinctNonzeroOids
  statusValid : w.status = ValidationStatus.valid
  noOperation : w.operationPerformed = false


theorem valid_validation_is_nonoperational
    (w : ValidationWitness)
    (h : w.Valid) :
    w.operationPerformed = false := by
  exact h.noOperation


theorem valid_validation_replays_upstream_chain
    (w : ValidationWitness)
    (h : w.Valid) :
    w.upstreamChainRevalidated := by
  exact h.upstreamChainRevalidated


theorem valid_validation_has_all_bindings
    (w : ValidationWitness)
    (h : w.Valid) :
    w.upstreamChainRevalidated ∧ w.readyCandidate ∧ w.repositoryMatches ∧
      w.checkpointMatches ∧ w.distinctNonzeroOids := by
  exact ⟨h.upstreamChainRevalidated, h.readyCandidate, h.repositoryMatches,
    h.checkpointMatches, h.distinctNonzeroOids⟩

structure ValidationDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_validation
    {Input Output : Type}
    (derivation : ValidationDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSCheckpointCandidateValidationV1_11
