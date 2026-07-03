import KUOS.WORLD.KuuOSLifecycleStageV0_15

namespace KUOS.WORLD.KuuOSLifecycleBoundedPostOperationReviewV0_16

inductive PostOperationReviewStatus where
  | reviewedForSeparateLifecycleTransitionReview
  | denied
  | rejected
  deriving DecidableEq, Repr

structure PostReviewEffects where
  authorityChanged : Bool
  quiescenceStateChanged : Bool
  terminalStateChanged : Bool
  terminalMarkerWritten : Bool
  resourceRemoved : Bool
  externalOperationPerformed : Bool
  repositoryChanged : Bool

structure PostOperationReviewWitness where
  sourceRecomputedValid : Bool
  sourceOperationCompleted : Bool
  sourceBindingValid : Bool
  reviewerBindingValid : Bool
  routeBindingValid : Bool
  reviewerSeparatedFromCompletionReviewer : Bool
  reviewerSeparatedFromPriorActors : Bool
  reviewerOrganizationSeparated : Bool
  reviewerMandateVerified : Bool
  reviewerQualified : Bool
  reviewerIdentityConfirmed : Bool
  reviewReady : Bool
  intendedResultMatchesObserved : Bool
  targetPostStateVerified : Bool
  collateralEffectsAbsent : Bool
  protectedResourcesIntact : Bool
  protectedCoreIntact : Bool
  monitoringEvidenceSufficient : Bool
  completionEvidenceSufficient : Bool
  unresolvedAnomalyPresent : Bool
  rollbackRequired : Bool
  recoveryRequired : Bool
  status : PostOperationReviewStatus
  operationCompleted : Bool
  postOperationReviewRecordIssued : Bool
  postOperationReviewDecisionMade : Bool
  postOperationReviewCompleted : Bool
  postOperationReviewDenied : Bool
  lifecycleTransitionReviewRequiredNext : Bool
  lifecycleTransitionReviewRouteRequiredNext : Bool
  operationRecoveryAssessmentRequiredNext : Bool
  operationRecoveryAssessmentRouteRequiredNext : Bool
  postReviewEffects : PostReviewEffects

structure PostReviewEffects.NonePerformed
    (e : PostReviewEffects) : Prop where
  authorityNotChanged : e.authorityChanged = false
  quiescenceStateNotChanged : e.quiescenceStateChanged = false
  terminalStateNotChanged : e.terminalStateChanged = false
  terminalMarkerNotWritten : e.terminalMarkerWritten = false
  resourceNotRemoved : e.resourceRemoved = false
  externalOperationNotPerformed :
    e.externalOperationPerformed = false
  repositoryNotChanged : e.repositoryChanged = false

structure PostOperationReviewWitness.ValidReviewed
    (w : PostOperationReviewWitness) : Prop where
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceOperationCompleted : w.sourceOperationCompleted = true
  sourceBindingValid : w.sourceBindingValid = true
  reviewerBindingValid : w.reviewerBindingValid = true
  routeBindingValid : w.routeBindingValid = true
  reviewerSeparatedFromCompletionReviewer :
    w.reviewerSeparatedFromCompletionReviewer = true
  reviewerSeparatedFromPriorActors :
    w.reviewerSeparatedFromPriorActors = true
  reviewerOrganizationSeparated :
    w.reviewerOrganizationSeparated = true
  reviewerMandateVerified : w.reviewerMandateVerified = true
  reviewerQualified : w.reviewerQualified = true
  reviewerIdentityConfirmed : w.reviewerIdentityConfirmed = true
  reviewReady : w.reviewReady = true
  intendedResultMatchesObserved :
    w.intendedResultMatchesObserved = true
  targetPostStateVerified : w.targetPostStateVerified = true
  collateralEffectsAbsent : w.collateralEffectsAbsent = true
  protectedResourcesIntact : w.protectedResourcesIntact = true
  protectedCoreIntact : w.protectedCoreIntact = true
  monitoringEvidenceSufficient :
    w.monitoringEvidenceSufficient = true
  completionEvidenceSufficient :
    w.completionEvidenceSufficient = true
  unresolvedAnomalyAbsent : w.unresolvedAnomalyPresent = false
  rollbackNotRequired : w.rollbackRequired = false
  recoveryNotRequired : w.recoveryRequired = false
  statusReviewed :
    w.status =
      PostOperationReviewStatus.reviewedForSeparateLifecycleTransitionReview
  operationCompleted : w.operationCompleted = true
  postOperationReviewRecordIssued :
    w.postOperationReviewRecordIssued = true
  postOperationReviewDecisionMade :
    w.postOperationReviewDecisionMade = true
  postOperationReviewCompleted :
    w.postOperationReviewCompleted = true
  postOperationReviewNotDenied :
    w.postOperationReviewDenied = false
  lifecycleTransitionReviewRequiredNext :
    w.lifecycleTransitionReviewRequiredNext = true
  lifecycleTransitionReviewRouteRequiredNext :
    w.lifecycleTransitionReviewRouteRequiredNext = true
  operationRecoveryAssessmentNotRequiredNext :
    w.operationRecoveryAssessmentRequiredNext = false
  operationRecoveryAssessmentRouteNotRequiredNext :
    w.operationRecoveryAssessmentRouteRequiredNext = false

structure PostOperationReviewWitness.ValidDenied
    (w : PostOperationReviewWitness) : Prop where
  statusDenied : w.status = PostOperationReviewStatus.denied
  operationCompleted : w.operationCompleted = true
  postOperationReviewRecordIssued :
    w.postOperationReviewRecordIssued = true
  postOperationReviewDecisionMade :
    w.postOperationReviewDecisionMade = true
  postOperationReviewNotCompleted :
    w.postOperationReviewCompleted = false
  postOperationReviewDenied :
    w.postOperationReviewDenied = true
  lifecycleTransitionReviewNotRequiredNext :
    w.lifecycleTransitionReviewRequiredNext = false
  lifecycleTransitionReviewRouteNotRequiredNext :
    w.lifecycleTransitionReviewRouteRequiredNext = false
  operationRecoveryAssessmentRequiredNext :
    w.operationRecoveryAssessmentRequiredNext = true
  operationRecoveryAssessmentRouteRequiredNext :
    w.operationRecoveryAssessmentRouteRequiredNext = true

structure PostOperationReviewWitness.ValidRejected
    (w : PostOperationReviewWitness) : Prop where
  statusRejected : w.status = PostOperationReviewStatus.rejected
  postOperationReviewRecordNotIssued :
    w.postOperationReviewRecordIssued = false
  postOperationReviewDecisionNotMade :
    w.postOperationReviewDecisionMade = false
  postOperationReviewNotCompleted :
    w.postOperationReviewCompleted = false
  postOperationReviewNotDenied :
    w.postOperationReviewDenied = false
  lifecycleTransitionReviewNotRequiredNext :
    w.lifecycleTransitionReviewRequiredNext = false
  lifecycleTransitionReviewRouteNotRequiredNext :
    w.lifecycleTransitionReviewRouteRequiredNext = false
  operationRecoveryAssessmentNotRequiredNext :
    w.operationRecoveryAssessmentRequiredNext = false
  operationRecoveryAssessmentRouteNotRequiredNext :
    w.operationRecoveryAssessmentRouteRequiredNext = false

def PostOperationReviewWitness.Valid
    (w : PostOperationReviewWitness) : Prop :=
  (w.ValidReviewed ∨ w.ValidDenied ∨ w.ValidRejected) ∧
    w.postReviewEffects.NonePerformed

theorem reviewed_requires_real_operation_completion
    (w : PostOperationReviewWitness)
    (h : w.ValidReviewed) :
    w.sourceOperationCompleted = true ∧
      w.operationCompleted = true ∧
      w.postOperationReviewRecordIssued = true ∧
      w.postOperationReviewCompleted = true := by
  exact ⟨h.sourceOperationCompleted,
    h.operationCompleted,
    h.postOperationReviewRecordIssued,
    h.postOperationReviewCompleted⟩

theorem reviewed_routes_only_to_separate_lifecycle_transition_review
    (w : PostOperationReviewWitness)
    (h : w.ValidReviewed) :
    w.lifecycleTransitionReviewRequiredNext = true ∧
      w.lifecycleTransitionReviewRouteRequiredNext = true ∧
      w.operationRecoveryAssessmentRequiredNext = false := by
  exact ⟨h.lifecycleTransitionReviewRequiredNext,
    h.lifecycleTransitionReviewRouteRequiredNext,
    h.operationRecoveryAssessmentNotRequiredNext⟩

theorem denied_routes_to_separate_operation_recovery_assessment
    (w : PostOperationReviewWitness)
    (h : w.ValidDenied) :
    w.postOperationReviewCompleted = false ∧
      w.postOperationReviewDenied = true ∧
      w.operationRecoveryAssessmentRequiredNext = true ∧
      w.operationRecoveryAssessmentRouteRequiredNext = true := by
  exact ⟨h.postOperationReviewNotCompleted,
    h.postOperationReviewDenied,
    h.operationRecoveryAssessmentRequiredNext,
    h.operationRecoveryAssessmentRouteRequiredNext⟩

theorem rejected_issues_no_valid_post_operation_review_record
    (w : PostOperationReviewWitness)
    (h : w.ValidRejected) :
    w.postOperationReviewRecordIssued = false ∧
      w.postOperationReviewDecisionMade = false ∧
      w.postOperationReviewCompleted = false := by
  exact ⟨h.postOperationReviewRecordNotIssued,
    h.postOperationReviewDecisionNotMade,
    h.postOperationReviewNotCompleted⟩

theorem valid_review_performs_no_lifecycle_or_repository_effect
    (w : PostOperationReviewWitness)
    (h : w.Valid) :
    w.postReviewEffects.NonePerformed := by
  exact h.2

structure PostOperationReviewDerivation
    (Input Output : Type) where
  derive : Input → Output

theorem same_input_has_same_post_operation_review
    {Input Output : Type}
    (derivation : PostOperationReviewDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSLifecycleBoundedPostOperationReviewV0_16
