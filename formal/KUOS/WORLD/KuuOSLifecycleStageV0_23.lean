import KUOS.WORLD.KuuOSLifecycleStageV0_22

namespace KUOS.WORLD.KuuOSLifecycleBoundedTransitionCompletionReviewV0_23

inductive CompletionReviewStatus where
  | approvedForSeparateCompletion
  | denied
  | rejected
  deriving DecidableEq, Repr

structure CompletionReviewWitness where
  sourceStarted : Bool
  sourceRecomputedValid : Bool
  sourceCompletionReviewRouteBound : Bool
  completionRouteBound : Bool
  reviewerAuthorityVerified : Bool
  reviewerSeparated : Bool
  completionEvidenceValid : Bool
  packageFresh : Bool
  currentStateNotStale : Bool
  targetStateStillValid : Bool
  noHoldRecoveryOrAnomaly : Bool
  status : CompletionReviewStatus
  recordIssued : Bool
  reviewCompleted : Bool
  reviewApproved : Bool
  completionRequiredNext : Bool
  completionRouteRequiredNext : Bool
  replanRequiredNext : Bool
  transitionCompleted : Bool
  lifecycleTransitionPerformed : Bool
  lifecycleStateChanged : Bool
  repositoryEffectPerformed : Bool

structure CompletionReviewWitness.ValidApproved
    (w : CompletionReviewWitness) : Prop where
  sourceStarted : w.sourceStarted = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceCompletionReviewRouteBound : w.sourceCompletionReviewRouteBound = true
  completionRouteBound : w.completionRouteBound = true
  reviewerAuthorityVerified : w.reviewerAuthorityVerified = true
  reviewerSeparated : w.reviewerSeparated = true
  completionEvidenceValid : w.completionEvidenceValid = true
  packageFresh : w.packageFresh = true
  currentStateNotStale : w.currentStateNotStale = true
  targetStateStillValid : w.targetStateStillValid = true
  noHoldRecoveryOrAnomaly : w.noHoldRecoveryOrAnomaly = true
  statusApproved :
    w.status = CompletionReviewStatus.approvedForSeparateCompletion
  recordIssued : w.recordIssued = true
  reviewCompleted : w.reviewCompleted = true
  reviewApproved : w.reviewApproved = true
  completionRequiredNext : w.completionRequiredNext = true
  completionRouteRequiredNext : w.completionRouteRequiredNext = true
  replanNotRequiredNext : w.replanRequiredNext = false

structure CompletionReviewWitness.ValidDenied
    (w : CompletionReviewWitness) : Prop where
  sourceStarted : w.sourceStarted = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceCompletionReviewRouteBound : w.sourceCompletionReviewRouteBound = true
  statusDenied : w.status = CompletionReviewStatus.denied
  recordIssued : w.recordIssued = true
  reviewCompleted : w.reviewCompleted = true
  reviewNotApproved : w.reviewApproved = false
  completionNotRequiredNext : w.completionRequiredNext = false
  completionRouteNotRequiredNext : w.completionRouteRequiredNext = false
  replanRequiredNext : w.replanRequiredNext = true

structure CompletionReviewWitness.ValidRejected
    (w : CompletionReviewWitness) : Prop where
  statusRejected : w.status = CompletionReviewStatus.rejected
  recordNotIssued : w.recordIssued = false
  reviewNotCompleted : w.reviewCompleted = false
  reviewNotApproved : w.reviewApproved = false
  completionNotRequiredNext : w.completionRequiredNext = false
  completionRouteNotRequiredNext : w.completionRouteRequiredNext = false
  replanNotRequiredNext : w.replanRequiredNext = false

structure CompletionReviewWitness.NoCompletionOrMutation
    (w : CompletionReviewWitness) : Prop where
  completionAbsent : w.transitionCompleted = false
  performedAbsent : w.lifecycleTransitionPerformed = false
  lifecycleStateUnchanged : w.lifecycleStateChanged = false
  repositoryEffectAbsent : w.repositoryEffectPerformed = false

structure CompletionReviewWitness.Valid
    (w : CompletionReviewWitness) : Prop where
  caseValid :
    w.ValidApproved ∨ w.ValidDenied ∨ w.ValidRejected
  noCompletionOrMutation : w.NoCompletionOrMutation

theorem approved_routes_only_to_separate_completion
    (w : CompletionReviewWitness) (h : w.ValidApproved) :
    w.reviewApproved = true ∧
      w.completionRequiredNext = true ∧
      w.completionRouteRequiredNext = true := by
  exact ⟨h.reviewApproved, h.completionRequiredNext,
    h.completionRouteRequiredNext⟩

theorem denied_does_not_route_to_completion
    (w : CompletionReviewWitness) (h : w.ValidDenied) :
    w.reviewApproved = false ∧
      w.completionRequiredNext = false ∧
      w.replanRequiredNext = true := by
  exact ⟨h.reviewNotApproved, h.completionNotRequiredNext,
    h.replanRequiredNext⟩

theorem rejected_issues_no_record
    (w : CompletionReviewWitness) (h : w.ValidRejected) :
    w.recordIssued = false ∧ w.reviewCompleted = false := by
  exact ⟨h.recordNotIssued, h.reviewNotCompleted⟩

theorem valid_review_has_no_completion_or_mutation
    (w : CompletionReviewWitness) (h : w.Valid) :
    w.NoCompletionOrMutation := by
  exact h.noCompletionOrMutation

end KUOS.WORLD.KuuOSLifecycleBoundedTransitionCompletionReviewV0_23
