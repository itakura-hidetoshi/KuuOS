import KUOS.WORLD.KuuOSLifecycleStageV0_14

namespace KUOS.WORLD.KuuOSLifecycleBoundedOperationCompletionV0_15

inductive OperationCompletionStatus where
  | completedForSeparatePostOperationReview
  | denied
  | rejected
  deriving DecidableEq, Repr

structure PostCompletionEffects where
  authorityChanged : Bool
  quiescenceStateChanged : Bool
  terminalStateChanged : Bool
  terminalMarkerWritten : Bool
  resourceRemoved : Bool
  externalOperationPerformed : Bool
  repositoryChanged : Bool

structure OperationCompletionWitness where
  sourceRecomputedValid : Bool
  sourceOperationStarted : Bool
  sourceBindingValid : Bool
  completionReviewerBindingValid : Bool
  routeBindingValid : Bool
  completionReviewerSeparatedFromOperator : Bool
  completionReviewerMandateVerified : Bool
  completionReviewerQualified : Bool
  completionReviewerIdentityConfirmed : Bool
  completionReady : Bool
  executionFinished : Bool
  executionResultIntegrityVerified : Bool
  allScopeItemsAccounted : Bool
  allReversibleStepsAccounted : Bool
  protectedResourcesIntact : Bool
  protectedCoreIntact : Bool
  resourceReservationsReleased : Bool
  monitoringCompleted : Bool
  evidenceCaptureCompleted : Bool
  status : OperationCompletionStatus
  operationStarted : Bool
  operationCompletionRecordIssued : Bool
  operationCompletionDecisionMade : Bool
  operationCompleted : Bool
  operationCompletionDenied : Bool
  postOperationReviewRequiredNext : Bool
  postOperationReviewRouteRequiredNext : Bool
  operationRecoveryRequiredNext : Bool
  operationRecoveryRouteRequiredNext : Bool
  postCompletionEffects : PostCompletionEffects

structure PostCompletionEffects.NonePerformed
    (e : PostCompletionEffects) : Prop where
  authorityNotChanged : e.authorityChanged = false
  quiescenceStateNotChanged : e.quiescenceStateChanged = false
  terminalStateNotChanged : e.terminalStateChanged = false
  terminalMarkerNotWritten : e.terminalMarkerWritten = false
  resourceNotRemoved : e.resourceRemoved = false
  externalOperationNotPerformed :
    e.externalOperationPerformed = false
  repositoryNotChanged : e.repositoryChanged = false

structure OperationCompletionWitness.ValidCompleted
    (w : OperationCompletionWitness) : Prop where
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceOperationStarted : w.sourceOperationStarted = true
  sourceBindingValid : w.sourceBindingValid = true
  completionReviewerBindingValid :
    w.completionReviewerBindingValid = true
  routeBindingValid : w.routeBindingValid = true
  completionReviewerSeparatedFromOperator :
    w.completionReviewerSeparatedFromOperator = true
  completionReviewerMandateVerified :
    w.completionReviewerMandateVerified = true
  completionReviewerQualified :
    w.completionReviewerQualified = true
  completionReviewerIdentityConfirmed :
    w.completionReviewerIdentityConfirmed = true
  completionReady : w.completionReady = true
  executionFinished : w.executionFinished = true
  executionResultIntegrityVerified :
    w.executionResultIntegrityVerified = true
  allScopeItemsAccounted : w.allScopeItemsAccounted = true
  allReversibleStepsAccounted :
    w.allReversibleStepsAccounted = true
  protectedResourcesIntact : w.protectedResourcesIntact = true
  protectedCoreIntact : w.protectedCoreIntact = true
  resourceReservationsReleased :
    w.resourceReservationsReleased = true
  monitoringCompleted : w.monitoringCompleted = true
  evidenceCaptureCompleted : w.evidenceCaptureCompleted = true
  statusCompleted :
    w.status =
      OperationCompletionStatus.completedForSeparatePostOperationReview
  operationStarted : w.operationStarted = true
  operationCompletionRecordIssued :
    w.operationCompletionRecordIssued = true
  operationCompletionDecisionMade :
    w.operationCompletionDecisionMade = true
  operationCompleted : w.operationCompleted = true
  operationCompletionNotDenied :
    w.operationCompletionDenied = false
  postOperationReviewRequiredNext :
    w.postOperationReviewRequiredNext = true
  postOperationReviewRouteRequiredNext :
    w.postOperationReviewRouteRequiredNext = true
  operationRecoveryNotRequiredNext :
    w.operationRecoveryRequiredNext = false
  operationRecoveryRouteNotRequiredNext :
    w.operationRecoveryRouteRequiredNext = false

structure OperationCompletionWitness.ValidDenied
    (w : OperationCompletionWitness) : Prop where
  statusDenied : w.status = OperationCompletionStatus.denied
  operationStarted : w.operationStarted = true
  operationCompletionRecordIssued :
    w.operationCompletionRecordIssued = true
  operationCompletionDecisionMade :
    w.operationCompletionDecisionMade = true
  operationNotCompleted : w.operationCompleted = false
  operationCompletionDenied :
    w.operationCompletionDenied = true
  postOperationReviewNotRequiredNext :
    w.postOperationReviewRequiredNext = false
  postOperationReviewRouteNotRequiredNext :
    w.postOperationReviewRouteRequiredNext = false
  operationRecoveryRequiredNext :
    w.operationRecoveryRequiredNext = true
  operationRecoveryRouteRequiredNext :
    w.operationRecoveryRouteRequiredNext = true

structure OperationCompletionWitness.ValidRejected
    (w : OperationCompletionWitness) : Prop where
  statusRejected : w.status = OperationCompletionStatus.rejected
  operationCompletionRecordNotIssued :
    w.operationCompletionRecordIssued = false
  operationCompletionDecisionNotMade :
    w.operationCompletionDecisionMade = false
  operationNotCompleted : w.operationCompleted = false
  operationCompletionNotDenied :
    w.operationCompletionDenied = false
  postOperationReviewNotRequiredNext :
    w.postOperationReviewRequiredNext = false
  postOperationReviewRouteNotRequiredNext :
    w.postOperationReviewRouteRequiredNext = false
  operationRecoveryNotRequiredNext :
    w.operationRecoveryRequiredNext = false
  operationRecoveryRouteNotRequiredNext :
    w.operationRecoveryRouteRequiredNext = false

def OperationCompletionWitness.Valid
    (w : OperationCompletionWitness) : Prop :=
  (w.ValidCompleted ∨ w.ValidDenied ∨ w.ValidRejected) ∧
    w.postCompletionEffects.NonePerformed

theorem completed_is_real_operation_completion
    (w : OperationCompletionWitness)
    (h : w.ValidCompleted) :
    w.operationStarted = true ∧
      w.operationCompletionRecordIssued = true ∧
      w.operationCompletionDecisionMade = true ∧
      w.operationCompleted = true := by
  exact ⟨h.operationStarted,
    h.operationCompletionRecordIssued,
    h.operationCompletionDecisionMade,
    h.operationCompleted⟩

theorem completed_routes_only_to_separate_post_operation_review
    (w : OperationCompletionWitness)
    (h : w.ValidCompleted) :
    w.postOperationReviewRequiredNext = true ∧
      w.postOperationReviewRouteRequiredNext = true ∧
      w.operationRecoveryRequiredNext = false := by
  exact ⟨h.postOperationReviewRequiredNext,
    h.postOperationReviewRouteRequiredNext,
    h.operationRecoveryNotRequiredNext⟩

theorem denied_routes_to_separate_recovery
    (w : OperationCompletionWitness)
    (h : w.ValidDenied) :
    w.operationCompleted = false ∧
      w.operationCompletionDenied = true ∧
      w.operationRecoveryRequiredNext = true ∧
      w.operationRecoveryRouteRequiredNext = true := by
  exact ⟨h.operationNotCompleted,
    h.operationCompletionDenied,
    h.operationRecoveryRequiredNext,
    h.operationRecoveryRouteRequiredNext⟩

theorem rejected_issues_no_valid_completion_record
    (w : OperationCompletionWitness)
    (h : w.ValidRejected) :
    w.operationCompletionRecordIssued = false ∧
      w.operationCompletionDecisionMade = false ∧
      w.operationCompleted = false := by
  exact ⟨h.operationCompletionRecordNotIssued,
    h.operationCompletionDecisionNotMade,
    h.operationNotCompleted⟩

theorem valid_completion_performs_no_lifecycle_or_repository_effect
    (w : OperationCompletionWitness)
    (h : w.Valid) :
    w.postCompletionEffects.NonePerformed := by
  exact h.2

structure OperationCompletionDerivation
    (Input Output : Type) where
  derive : Input → Output

theorem same_input_has_same_operation_completion
    {Input Output : Type}
    (derivation : OperationCompletionDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSLifecycleBoundedOperationCompletionV0_15
