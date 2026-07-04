import KUOS.WORLD.KuuOSLifecycleStageV0_21

namespace KUOS.WORLD.KuuOSLifecycleBoundedTransitionStartV0_22

inductive TransitionStartStatus where
  | startedForSeparateCompletionReview
  | denied
  | rejected
  deriving DecidableEq, Repr

structure TransitionStartWitness where
  sourceAuthorized : Bool
  sourceRecomputedValid : Bool
  sourceStartRouteBound : Bool
  completionReviewRouteBound : Bool
  operatorAuthorityVerified : Bool
  operatorSeparated : Bool
  packageFresh : Bool
  currentStateNotStale : Bool
  targetStateStillValid : Bool
  noHoldRecoveryOrAnomaly : Bool
  status : TransitionStartStatus
  recordIssued : Bool
  startCompleted : Bool
  transitionStarted : Bool
  completionReviewRequiredNext : Bool
  completionReviewRouteRequiredNext : Bool
  restartOrReauthorizationRequiredNext : Bool
  transitionCompleted : Bool
  lifecycleTransitionPerformed : Bool
  lifecycleStateChanged : Bool
  repositoryEffectPerformed : Bool

structure TransitionStartWitness.ValidStarted
    (w : TransitionStartWitness) : Prop where
  sourceAuthorized : w.sourceAuthorized = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceStartRouteBound : w.sourceStartRouteBound = true
  completionReviewRouteBound : w.completionReviewRouteBound = true
  operatorAuthorityVerified : w.operatorAuthorityVerified = true
  operatorSeparated : w.operatorSeparated = true
  packageFresh : w.packageFresh = true
  currentStateNotStale : w.currentStateNotStale = true
  targetStateStillValid : w.targetStateStillValid = true
  noHoldRecoveryOrAnomaly : w.noHoldRecoveryOrAnomaly = true
  statusStarted :
    w.status = TransitionStartStatus.startedForSeparateCompletionReview
  recordIssued : w.recordIssued = true
  startCompleted : w.startCompleted = true
  transitionStarted : w.transitionStarted = true
  completionReviewRequiredNext : w.completionReviewRequiredNext = true
  completionReviewRouteRequiredNext : w.completionReviewRouteRequiredNext = true
  restartOrReauthorizationNotRequiredNext :
    w.restartOrReauthorizationRequiredNext = false

structure TransitionStartWitness.ValidDenied
    (w : TransitionStartWitness) : Prop where
  sourceAuthorized : w.sourceAuthorized = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceStartRouteBound : w.sourceStartRouteBound = true
  statusDenied : w.status = TransitionStartStatus.denied
  recordIssued : w.recordIssued = true
  startCompleted : w.startCompleted = true
  transitionNotStarted : w.transitionStarted = false
  completionReviewNotRequiredNext :
    w.completionReviewRequiredNext = false
  completionReviewRouteNotRequiredNext :
    w.completionReviewRouteRequiredNext = false
  restartOrReauthorizationRequiredNext :
    w.restartOrReauthorizationRequiredNext = true

structure TransitionStartWitness.ValidRejected
    (w : TransitionStartWitness) : Prop where
  statusRejected : w.status = TransitionStartStatus.rejected
  recordNotIssued : w.recordIssued = false
  startNotCompleted : w.startCompleted = false
  transitionNotStarted : w.transitionStarted = false
  completionReviewNotRequiredNext :
    w.completionReviewRequiredNext = false
  completionReviewRouteNotRequiredNext :
    w.completionReviewRouteRequiredNext = false
  restartOrReauthorizationNotRequiredNext :
    w.restartOrReauthorizationRequiredNext = false

structure TransitionStartWitness.NoCompletionOrMutation
    (w : TransitionStartWitness) : Prop where
  completionAbsent : w.transitionCompleted = false
  performedAbsent : w.lifecycleTransitionPerformed = false
  lifecycleStateUnchanged : w.lifecycleStateChanged = false
  repositoryEffectAbsent : w.repositoryEffectPerformed = false

structure TransitionStartWitness.Valid
    (w : TransitionStartWitness) : Prop where
  caseValid :
    w.ValidStarted ∨ w.ValidDenied ∨ w.ValidRejected
  noCompletionOrMutation : w.NoCompletionOrMutation

theorem started_routes_only_to_completion_review
    (w : TransitionStartWitness) (h : w.ValidStarted) :
    w.transitionStarted = true ∧
      w.completionReviewRequiredNext = true ∧
      w.completionReviewRouteRequiredNext = true := by
  exact ⟨h.transitionStarted, h.completionReviewRequiredNext,
    h.completionReviewRouteRequiredNext⟩

theorem denied_does_not_route_to_completion_review
    (w : TransitionStartWitness) (h : w.ValidDenied) :
    w.transitionStarted = false ∧
      w.completionReviewRequiredNext = false ∧
      w.restartOrReauthorizationRequiredNext = true := by
  exact ⟨h.transitionNotStarted, h.completionReviewNotRequiredNext,
    h.restartOrReauthorizationRequiredNext⟩

theorem rejected_issues_no_record
    (w : TransitionStartWitness) (h : w.ValidRejected) :
    w.recordIssued = false ∧ w.startCompleted = false := by
  exact ⟨h.recordNotIssued, h.startNotCompleted⟩

theorem valid_start_has_no_completion_or_mutation
    (w : TransitionStartWitness) (h : w.Valid) :
    w.NoCompletionOrMutation := by
  exact h.noCompletionOrMutation

end KUOS.WORLD.KuuOSLifecycleBoundedTransitionStartV0_22
