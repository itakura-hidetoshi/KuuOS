import KUOS.WORLD.KuuOSRepositoryCheckpointNamespaceGateV1_08

namespace KUOS.WORLD.KuuOSRepositoryCheckpointCandidateV1_09

inductive CandidateStatus where
  | none
  | ready
  | rejected
  deriving DecidableEq, Repr

inductive CandidateReason where
  | cleanNoop
  | creationRouteAvailable
  | checkpointInterfaceRequired
  | invalidEvidence
  deriving DecidableEq, Repr

structure CheckpointCandidateWitness where
  gateDecisionValid : Prop
  repositoryBindingExact : Prop
  gateDecisionFresh : Prop
  status : CandidateStatus
  reason : CandidateReason
  currentOidNonzero : Prop
  proposedOidNonzero : Prop
  oidsDistinct : Prop
  dedicatedCheckpointInterfaceRequired : Bool

structure CheckpointCandidateWitness.ValidReady
    (w : CheckpointCandidateWitness) : Prop where
  gateDecisionValid : w.gateDecisionValid
  repositoryBindingExact : w.repositoryBindingExact
  gateDecisionFresh : w.gateDecisionFresh
  statusReady : w.status = CandidateStatus.ready
  reasonInterfaceRequired :
    w.reason = CandidateReason.checkpointInterfaceRequired
  currentOidNonzero : w.currentOidNonzero
  proposedOidNonzero : w.proposedOidNonzero
  oidsDistinct : w.oidsDistinct
  dedicatedRequired : w.dedicatedCheckpointInterfaceRequired = true

structure CheckpointCandidateWitness.ValidNone
    (w : CheckpointCandidateWitness) : Prop where
  statusNone : w.status = CandidateStatus.none
  reasonExistingRoute :
    w.reason = CandidateReason.cleanNoop ∨
      w.reason = CandidateReason.creationRouteAvailable
  dedicatedRequired : w.dedicatedCheckpointInterfaceRequired = false

structure CheckpointCandidateWitness.ValidRejected
    (w : CheckpointCandidateWitness) : Prop where
  statusRejected : w.status = CandidateStatus.rejected
  reasonInvalid : w.reason = CandidateReason.invalidEvidence
  dedicatedRequired : w.dedicatedCheckpointInterfaceRequired = false


theorem ready_candidate_has_distinct_nonzero_oids
    (w : CheckpointCandidateWitness)
    (h : w.ValidReady) :
    w.currentOidNonzero ∧ w.proposedOidNonzero ∧ w.oidsDistinct := by
  exact ⟨h.currentOidNonzero, h.proposedOidNonzero, h.oidsDistinct⟩


theorem ready_candidate_marks_dedicated_interface
    (w : CheckpointCandidateWitness)
    (h : w.ValidReady) :
    w.status = CandidateStatus.ready ∧
      w.reason = CandidateReason.checkpointInterfaceRequired ∧
      w.dedicatedCheckpointInterfaceRequired = true := by
  exact ⟨h.statusReady, h.reasonInterfaceRequired, h.dedicatedRequired⟩


structure CandidateDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_checkpoint_candidate
    {Input Output : Type}
    (derivation : CandidateDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryCheckpointCandidateV1_09
