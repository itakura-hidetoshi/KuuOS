import KUOS.WORLD.KuuOSLifecycleStageV0_23

namespace KUOS.WORLD.KuuOSLifecycleBoundedTransitionCompletionV0_24

inductive TransitionCompletionStatus where
  | completedForSeparateStateAdoption
  | denied
  | rejected
  deriving DecidableEq, Repr

structure TransitionCompletionWitness where
  sourceApproved : Bool
  sourceRecomputedValid : Bool
  sourceCompletionRouteBound : Bool
  stateAdoptionRouteBound : Bool
  completionOperatorAuthorityVerified : Bool
  completionOperatorSeparated : Bool
  completionReceiptValid : Bool
  packageFresh : Bool
  currentStateNotStale : Bool
  targetStateStillValid : Bool
  noHoldRecoveryOrAnomaly : Bool
  status : TransitionCompletionStatus
  recordIssued : Bool
  completionRecordCompleted : Bool
  transitionCompleted : Bool
  stateAdoptionRequiredNext : Bool
  stateAdoptionRouteRequiredNext : Bool
  recompletionOrReplanRequiredNext : Bool
  lifecycleTransitionPerformed : Bool
  lifecycleStateChanged : Bool
  repositoryEffectPerformed : Bool

structure TransitionCompletionWitness.ValidCompleted
    (w : TransitionCompletionWitness) : Prop where
  sourceApproved : w.sourceApproved = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceCompletionRouteBound : w.sourceCompletionRouteBound = true
  stateAdoptionRouteBound : w.stateAdoptionRouteBound = true
  completionOperatorAuthorityVerified :
    w.completionOperatorAuthorityVerified = true
  completionOperatorSeparated : w.completionOperatorSeparated = true
  completionReceiptValid : w.completionReceiptValid = true
  packageFresh : w.packageFresh = true
  currentStateNotStale : w.currentStateNotStale = true
  targetStateStillValid : w.targetStateStillValid = true
  noHoldRecoveryOrAnomaly : w.noHoldRecoveryOrAnomaly = true
  statusCompleted :
    w.status = TransitionCompletionStatus.completedForSeparateStateAdoption
  recordIssued : w.recordIssued = true
  completionRecordCompleted : w.completionRecordCompleted = true
  transitionCompleted : w.transitionCompleted = true
  stateAdoptionRequiredNext : w.stateAdoptionRequiredNext = true
  stateAdoptionRouteRequiredNext : w.stateAdoptionRouteRequiredNext = true
  recompletionOrReplanNotRequiredNext :
    w.recompletionOrReplanRequiredNext = false

structure TransitionCompletionWitness.ValidDenied
    (w : TransitionCompletionWitness) : Prop where
  sourceApproved : w.sourceApproved = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceCompletionRouteBound : w.sourceCompletionRouteBound = true
  statusDenied : w.status = TransitionCompletionStatus.denied
  recordIssued : w.recordIssued = true
  completionRecordCompleted : w.completionRecordCompleted = true
  transitionNotCompleted : w.transitionCompleted = false
  stateAdoptionNotRequiredNext : w.stateAdoptionRequiredNext = false
  stateAdoptionRouteNotRequiredNext :
    w.stateAdoptionRouteRequiredNext = false
  recompletionOrReplanRequiredNext :
    w.recompletionOrReplanRequiredNext = true

structure TransitionCompletionWitness.ValidRejected
    (w : TransitionCompletionWitness) : Prop where
  statusRejected : w.status = TransitionCompletionStatus.rejected
  recordNotIssued : w.recordIssued = false
  completionRecordNotCompleted : w.completionRecordCompleted = false
  transitionNotCompleted : w.transitionCompleted = false
  stateAdoptionNotRequiredNext : w.stateAdoptionRequiredNext = false
  stateAdoptionRouteNotRequiredNext :
    w.stateAdoptionRouteRequiredNext = false
  recompletionOrReplanNotRequiredNext :
    w.recompletionOrReplanRequiredNext = false

structure TransitionCompletionWitness.NoStateOrRepositoryMutation
    (w : TransitionCompletionWitness) : Prop where
  performedAbsent : w.lifecycleTransitionPerformed = false
  lifecycleStateUnchanged : w.lifecycleStateChanged = false
  repositoryEffectAbsent : w.repositoryEffectPerformed = false

structure TransitionCompletionWitness.Valid
    (w : TransitionCompletionWitness) : Prop where
  caseValid :
    w.ValidCompleted ∨ w.ValidDenied ∨ w.ValidRejected
  noStateOrRepositoryMutation : w.NoStateOrRepositoryMutation

theorem completed_routes_only_to_state_adoption
    (w : TransitionCompletionWitness) (h : w.ValidCompleted) :
    w.transitionCompleted = true ∧
      w.stateAdoptionRequiredNext = true ∧
      w.stateAdoptionRouteRequiredNext = true := by
  exact ⟨h.transitionCompleted, h.stateAdoptionRequiredNext,
    h.stateAdoptionRouteRequiredNext⟩

theorem denied_does_not_route_to_state_adoption
    (w : TransitionCompletionWitness) (h : w.ValidDenied) :
    w.transitionCompleted = false ∧
      w.stateAdoptionRequiredNext = false ∧
      w.recompletionOrReplanRequiredNext = true := by
  exact ⟨h.transitionNotCompleted, h.stateAdoptionNotRequiredNext,
    h.recompletionOrReplanRequiredNext⟩

theorem rejected_issues_no_record
    (w : TransitionCompletionWitness) (h : w.ValidRejected) :
    w.recordIssued = false ∧ w.completionRecordCompleted = false := by
  exact ⟨h.recordNotIssued, h.completionRecordNotCompleted⟩

theorem valid_completion_has_no_state_or_repository_mutation
    (w : TransitionCompletionWitness) (h : w.Valid) :
    w.NoStateOrRepositoryMutation := by
  exact h.noStateOrRepositoryMutation

end KUOS.WORLD.KuuOSLifecycleBoundedTransitionCompletionV0_24
