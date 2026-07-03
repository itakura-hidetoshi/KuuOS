import KUOS.WORLD.KuuOSLifecycleBoundedRequestV0_10

namespace KUOS.WORLD.KuuOSLifecycleBoundedDecisionReviewV0_11

inductive ReviewStatus where
  | clearForAuthorizationDecision
  | blocked
  | rejected
  deriving DecidableEq, Repr

structure LaterStageEffects where
  authorizationDecisionMade : Bool
  operationApproved : Bool
  operationStarted : Bool
  operationCompleted : Bool
  authorityChanged : Bool
  quiescenceStateChanged : Bool
  terminalStateChanged : Bool
  terminalMarkerWritten : Bool
  resourceRemoved : Bool
  externalOperationPerformed : Bool
  repositoryChanged : Bool

structure DecisionReviewWitness where
  sourceRecomputedValid : Bool
  sourceRequestIssued : Bool
  sourceBindingValid : Bool
  reviewerQualified : Bool
  reviewerIndependentFromPriorChain : Bool
  reviewerIndependentFromRequester : Bool
  reviewerIndependentFromAuthorizationDecisionMaker : Bool
  reviewerIndependentFromFutureOperator : Bool
  authorizationDecisionMakerSeparatedFromOperator : Bool
  conflictDisclosureComplete : Bool
  materialConflictPresent : Bool
  scopeBindingValid : Bool
  packageSafetyValid : Bool
  sourceFresh : Bool
  reviewFresh : Bool
  authorizationRouteAvailable : Bool
  appealRouteAvailable : Bool
  dissentRouteAvailable : Bool
  minorityOpinionRecorded : Bool
  status : ReviewStatus
  reviewRecordIssued : Bool
  reviewCompleted : Bool
  clearForAuthorizationDecision : Bool
  authorizationDecisionRequiredNext : Bool
  laterEffects : LaterStageEffects

structure LaterStageEffects.NonePerformed (e : LaterStageEffects) : Prop where
  authorizationDecisionNotMade : e.authorizationDecisionMade = false
  operationNotApproved : e.operationApproved = false
  operationNotStarted : e.operationStarted = false
  operationNotCompleted : e.operationCompleted = false
  authorityNotChanged : e.authorityChanged = false
  quiescenceStateNotChanged : e.quiescenceStateChanged = false
  terminalStateNotChanged : e.terminalStateChanged = false
  terminalMarkerNotWritten : e.terminalMarkerWritten = false
  resourceNotRemoved : e.resourceRemoved = false
  externalOperationNotPerformed : e.externalOperationPerformed = false
  repositoryNotChanged : e.repositoryChanged = false

structure DecisionReviewWitness.ValidClear (w : DecisionReviewWitness) : Prop where
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceRequestIssued : w.sourceRequestIssued = true
  sourceBindingValid : w.sourceBindingValid = true
  reviewerQualified : w.reviewerQualified = true
  reviewerIndependentFromPriorChain : w.reviewerIndependentFromPriorChain = true
  reviewerIndependentFromRequester : w.reviewerIndependentFromRequester = true
  reviewerIndependentFromAuthorizationDecisionMaker :
    w.reviewerIndependentFromAuthorizationDecisionMaker = true
  reviewerIndependentFromFutureOperator :
    w.reviewerIndependentFromFutureOperator = true
  authorizationDecisionMakerSeparatedFromOperator :
    w.authorizationDecisionMakerSeparatedFromOperator = true
  conflictDisclosureComplete : w.conflictDisclosureComplete = true
  materialConflictAbsent : w.materialConflictPresent = false
  scopeBindingValid : w.scopeBindingValid = true
  packageSafetyValid : w.packageSafetyValid = true
  sourceFresh : w.sourceFresh = true
  reviewFresh : w.reviewFresh = true
  authorizationRouteAvailable : w.authorizationRouteAvailable = true
  appealRouteAvailable : w.appealRouteAvailable = true
  dissentRouteAvailable : w.dissentRouteAvailable = true
  minorityOpinionRecorded : w.minorityOpinionRecorded = true
  statusClear : w.status = ReviewStatus.clearForAuthorizationDecision
  reviewRecordIssued : w.reviewRecordIssued = true
  reviewCompleted : w.reviewCompleted = true
  clearForAuthorizationDecision : w.clearForAuthorizationDecision = true
  authorizationDecisionRequiredNext : w.authorizationDecisionRequiredNext = true

structure DecisionReviewWitness.ValidBlocked (w : DecisionReviewWitness) : Prop where
  statusBlocked : w.status = ReviewStatus.blocked
  reviewRecordIssued : w.reviewRecordIssued = true
  reviewCompleted : w.reviewCompleted = true
  notClearForAuthorizationDecision : w.clearForAuthorizationDecision = false
  authorizationDecisionNotRequiredNext :
    w.authorizationDecisionRequiredNext = false

structure DecisionReviewWitness.ValidRejected (w : DecisionReviewWitness) : Prop where
  statusRejected : w.status = ReviewStatus.rejected
  reviewRecordNotIssued : w.reviewRecordIssued = false
  reviewNotCompleted : w.reviewCompleted = false
  notClearForAuthorizationDecision : w.clearForAuthorizationDecision = false
  authorizationDecisionNotRequiredNext :
    w.authorizationDecisionRequiredNext = false

def DecisionReviewWitness.Valid (w : DecisionReviewWitness) : Prop :=
  (w.ValidClear ∨ w.ValidBlocked ∨ w.ValidRejected) ∧
    w.laterEffects.NonePerformed

theorem clear_routes_only_to_separate_authorization_decision
    (w : DecisionReviewWitness)
    (h : w.ValidClear) :
    w.clearForAuthorizationDecision = true ∧
      w.authorizationDecisionRequiredNext = true := by
  exact ⟨h.clearForAuthorizationDecision, h.authorizationDecisionRequiredNext⟩

theorem clear_preserves_role_separation
    (w : DecisionReviewWitness)
    (h : w.ValidClear) :
    w.reviewerIndependentFromRequester = true ∧
      w.reviewerIndependentFromAuthorizationDecisionMaker = true ∧
      w.reviewerIndependentFromFutureOperator = true ∧
      w.authorizationDecisionMakerSeparatedFromOperator = true := by
  exact ⟨h.reviewerIndependentFromRequester,
    h.reviewerIndependentFromAuthorizationDecisionMaker,
    h.reviewerIndependentFromFutureOperator,
    h.authorizationDecisionMakerSeparatedFromOperator⟩

theorem blocked_does_not_clear_review
    (w : DecisionReviewWitness)
    (h : w.ValidBlocked) :
    w.clearForAuthorizationDecision = false ∧
      w.authorizationDecisionRequiredNext = false := by
  exact ⟨h.notClearForAuthorizationDecision,
    h.authorizationDecisionNotRequiredNext⟩

theorem rejected_issues_no_valid_review_record
    (w : DecisionReviewWitness)
    (h : w.ValidRejected) :
    w.reviewRecordIssued = false := by
  exact h.reviewRecordNotIssued

theorem valid_review_performs_no_later_effect
    (w : DecisionReviewWitness)
    (h : w.Valid) :
    w.laterEffects.NonePerformed := by
  exact h.2

structure ReviewDerivation (Input Output : Type) where
  derive : Input → Output

theorem same_input_has_same_review
    {Input Output : Type}
    (derivation : ReviewDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSLifecycleBoundedDecisionReviewV0_11
