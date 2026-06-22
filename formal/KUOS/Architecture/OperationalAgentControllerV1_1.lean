import Mathlib
import KUOS.Architecture.AdaptiveAgentReferenceArchitectureV1_0

namespace KUOS.Architecture.OperationalAgentControllerV1_1

/--
The operational controller authorizes one staged adapter invocation only through
an explicit conjunction.  No individual field is sovereign execution authority.
-/
structure AuthorizationGate where
  adaptiveStateValid : Prop
  adaptiveStateActive : Prop
  planStage : Prop
  leasedAuthority : Prop
  activeSession : Prop
  ownerLineageSessionBound : Prop
  capabilityActive : Prop
  capabilityEpochFresh : Prop
  adapterKindMatches : Prop
  operationResourceAllowed : Prop
  effectBelowCeiling : Prop
  finiteLeaseValid : Prop
  intentNotReplayed : Prop
  hostLicenseBound : Prop
  noExternalCommitRequest : Prop

abbrev Authorized (gate : AuthorizationGate) : Prop :=
  gate.adaptiveStateValid ∧
  gate.adaptiveStateActive ∧
  gate.planStage ∧
  gate.leasedAuthority ∧
  gate.activeSession ∧
  gate.ownerLineageSessionBound ∧
  gate.capabilityActive ∧
  gate.capabilityEpochFresh ∧
  gate.adapterKindMatches ∧
  gate.operationResourceAllowed ∧
  gate.effectBelowCeiling ∧
  gate.finiteLeaseValid ∧
  gate.intentNotReplayed ∧
  gate.hostLicenseBound ∧
  gate.noExternalCommitRequest

structure ClosedCycleBoundary where
  adapterResultNotTruth : Prop
  independentObservationRequired : Prop
  verificationNotRootRewrite : Prop
  learningFutureOnly : Prop
  currentCycleNotMutatedByLearning : Prop
  receiptNotSuccessorAuthority : Prop
  externalCommitNotPerformed : Prop

abbrev SafeClosedCycle (boundary : ClosedCycleBoundary) : Prop :=
  boundary.adapterResultNotTruth ∧
  boundary.independentObservationRequired ∧
  boundary.verificationNotRootRewrite ∧
  boundary.learningFutureOnly ∧
  boundary.currentCycleNotMutatedByLearning ∧
  boundary.receiptNotSuccessorAuthority ∧
  boundary.externalCommitNotPerformed


theorem authorized_implies_active_capability
    (gate : AuthorizationGate) (authorized : Authorized gate) :
    gate.capabilityActive := by
  aesop


theorem authorized_implies_fresh_capability_epoch
    (gate : AuthorizationGate) (authorized : Authorized gate) :
    gate.capabilityEpochFresh := by
  aesop


theorem authorized_implies_finite_valid_lease
    (gate : AuthorizationGate) (authorized : Authorized gate) :
    gate.finiteLeaseValid := by
  aesop


theorem external_commit_request_blocks_authorization
    (gate : AuthorizationGate)
    (requested : ¬ gate.noExternalCommitRequest) :
    ¬ Authorized gate := by
  aesop


theorem stale_epoch_blocks_authorization
    (gate : AuthorizationGate)
    (stale : ¬ gate.capabilityEpochFresh) :
    ¬ Authorized gate := by
  aesop


theorem replay_blocks_authorization
    (gate : AuthorizationGate)
    (replayed : ¬ gate.intentNotReplayed) :
    ¬ Authorized gate := by
  aesop


theorem safe_closed_cycle_preserves_external_noncommit
    (boundary : ClosedCycleBoundary)
    (safe : SafeClosedCycle boundary) :
    boundary.externalCommitNotPerformed := by
  aesop


theorem safe_closed_cycle_preserves_future_only_learning
    (boundary : ClosedCycleBoundary)
    (safe : SafeClosedCycle boundary) :
    boundary.learningFutureOnly ∧
      boundary.currentCycleNotMutatedByLearning := by
  aesop

end KUOS.Architecture.OperationalAgentControllerV1_1
