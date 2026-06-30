import KUOS.WORLD.KuuOSCheckpointCandidateValidationV1_11

namespace KUOS.WORLD.KuuOSCheckpointEvidenceEnvelopeV1_12

inductive EnvelopeStatus where
  | ready
  | conflict
  | none
  | rejected
  deriving DecidableEq, Repr

structure EnvelopeWitness where
  contractValid : Prop
  validationValid : Prop
  candidateMatch : Prop
  repositoryMatch : Prop
  checkpointMatch : Prop
  expectedOidMatch : Prop
  proposedOidMatch : Prop
  upstreamRevalidated : Prop
  status : EnvelopeStatus
  eligible : Bool
  operationPerformed : Bool

structure EnvelopeWitness.ValidReady (w : EnvelopeWitness) : Prop where
  contractValid : w.contractValid
  validationValid : w.validationValid
  candidateMatch : w.candidateMatch
  repositoryMatch : w.repositoryMatch
  checkpointMatch : w.checkpointMatch
  expectedOidMatch : w.expectedOidMatch
  proposedOidMatch : w.proposedOidMatch
  upstreamRevalidated : w.upstreamRevalidated
  statusReady : w.status = EnvelopeStatus.ready
  eligibleTrue : w.eligible = true
  noOperation : w.operationPerformed = false

structure EnvelopeWitness.ValidConflict (w : EnvelopeWitness) : Prop where
  contractValid : w.contractValid
  validationValid : w.validationValid
  statusConflict : w.status = EnvelopeStatus.conflict
  eligibleFalse : w.eligible = false
  noOperation : w.operationPerformed = false


theorem ready_envelope_has_exact_binding
    (w : EnvelopeWitness)
    (h : w.ValidReady) :
    w.candidateMatch ∧ w.repositoryMatch ∧ w.checkpointMatch ∧
      w.expectedOidMatch ∧ w.proposedOidMatch := by
  exact ⟨h.candidateMatch, h.repositoryMatch, h.checkpointMatch,
    h.expectedOidMatch, h.proposedOidMatch⟩


theorem ready_envelope_revalidates_upstream
    (w : EnvelopeWitness)
    (h : w.ValidReady) :
    w.upstreamRevalidated := by
  exact h.upstreamRevalidated


theorem ready_envelope_is_nonoperational
    (w : EnvelopeWitness)
    (h : w.ValidReady) :
    w.eligible = true ∧ w.operationPerformed = false := by
  exact ⟨h.eligibleTrue, h.noOperation⟩


theorem conflict_envelope_is_not_eligible
    (w : EnvelopeWitness)
    (h : w.ValidConflict) :
    w.eligible = false ∧ w.operationPerformed = false := by
  exact ⟨h.eligibleFalse, h.noOperation⟩

structure EnvelopeDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_envelope
    {Input Output : Type}
    (derivation : EnvelopeDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSCheckpointEvidenceEnvelopeV1_12
