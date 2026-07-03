import KUOS.WORLD.KuuOSLifecycleStageV0_11

namespace KUOS.WORLD.KuuOSLifecycleBoundedAuthorizationDecisionV0_12

inductive AuthorizationStatus where
  | approved
  | denied
  | rejected
  deriving DecidableEq, Repr

structure LaterExecutionEffects where
  operationStarted : Bool
  operationCompleted : Bool
  authorityChanged : Bool
  quiescenceStateChanged : Bool
  terminalStateChanged : Bool
  terminalMarkerWritten : Bool
  resourceRemoved : Bool
  externalOperationPerformed : Bool
  repositoryChanged : Bool

structure AuthorizationDecisionWitness where
  sourceRecomputedValid : Bool
  sourceReviewClear : Bool
  sourceBindingValid : Bool
  authorityMandated : Bool
  authorityQualified : Bool
  authorityIndependentFromPriorChain : Bool
  authorityIndependentFromDecisionReviewer : Bool
  authorityIndependentFromRequester : Bool
  authoritySeparatedFromFutureOperator : Bool
  jurisdictionValid : Bool
  quorumValid : Bool
  reasonedDecisionComplete : Bool
  proportionalitySatisfied : Bool
  lessRestrictiveAlternativesExhausted : Bool
  irreversibilityReviewComplete : Bool
  humanImpactReviewComplete : Bool
  packageSafetyValid : Bool
  appealRouteAvailable : Bool
  dissentRouteAvailable : Bool
  minorityOpinionRecorded : Bool
  status : AuthorizationStatus
  decisionRecordIssued : Bool
  authorizationDecisionMade : Bool
  operationApproved : Bool
  operationStartRequiredNext : Bool
  laterEffects : LaterExecutionEffects

structure LaterExecutionEffects.NonePerformed (e : LaterExecutionEffects) : Prop where
  operationNotStarted : e.operationStarted = false
  operationNotCompleted : e.operationCompleted = false
  authorityNotChanged : e.authorityChanged = false
  quiescenceStateNotChanged : e.quiescenceStateChanged = false
  terminalStateNotChanged : e.terminalStateChanged = false
  terminalMarkerNotWritten : e.terminalMarkerWritten = false
  resourceNotRemoved : e.resourceRemoved = false
  externalOperationNotPerformed : e.externalOperationPerformed = false
  repositoryNotChanged : e.repositoryChanged = false

structure AuthorizationDecisionWitness.ValidApproved
    (w : AuthorizationDecisionWitness) : Prop where
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceReviewClear : w.sourceReviewClear = true
  sourceBindingValid : w.sourceBindingValid = true
  authorityMandated : w.authorityMandated = true
  authorityQualified : w.authorityQualified = true
  authorityIndependentFromPriorChain :
    w.authorityIndependentFromPriorChain = true
  authorityIndependentFromDecisionReviewer :
    w.authorityIndependentFromDecisionReviewer = true
  authorityIndependentFromRequester :
    w.authorityIndependentFromRequester = true
  authoritySeparatedFromFutureOperator :
    w.authoritySeparatedFromFutureOperator = true
  jurisdictionValid : w.jurisdictionValid = true
  quorumValid : w.quorumValid = true
  reasonedDecisionComplete : w.reasonedDecisionComplete = true
  proportionalitySatisfied : w.proportionalitySatisfied = true
  lessRestrictiveAlternativesExhausted :
    w.lessRestrictiveAlternativesExhausted = true
  irreversibilityReviewComplete : w.irreversibilityReviewComplete = true
  humanImpactReviewComplete : w.humanImpactReviewComplete = true
  packageSafetyValid : w.packageSafetyValid = true
  appealRouteAvailable : w.appealRouteAvailable = true
  dissentRouteAvailable : w.dissentRouteAvailable = true
  minorityOpinionRecorded : w.minorityOpinionRecorded = true
  statusApproved : w.status = AuthorizationStatus.approved
  decisionRecordIssued : w.decisionRecordIssued = true
  authorizationDecisionMade : w.authorizationDecisionMade = true
  operationApproved : w.operationApproved = true
  operationStartRequiredNext : w.operationStartRequiredNext = true

structure AuthorizationDecisionWitness.ValidDenied
    (w : AuthorizationDecisionWitness) : Prop where
  statusDenied : w.status = AuthorizationStatus.denied
  decisionRecordIssued : w.decisionRecordIssued = true
  authorizationDecisionMade : w.authorizationDecisionMade = true
  operationNotApproved : w.operationApproved = false
  operationStartNotRequired : w.operationStartRequiredNext = false

structure AuthorizationDecisionWitness.ValidRejected
    (w : AuthorizationDecisionWitness) : Prop where
  statusRejected : w.status = AuthorizationStatus.rejected
  decisionRecordNotIssued : w.decisionRecordIssued = false
  authorizationDecisionNotMade : w.authorizationDecisionMade = false
  operationNotApproved : w.operationApproved = false
  operationStartNotRequired : w.operationStartRequiredNext = false

def AuthorizationDecisionWitness.Valid (w : AuthorizationDecisionWitness) : Prop :=
  (w.ValidApproved ∨ w.ValidDenied ∨ w.ValidRejected) ∧
    w.laterEffects.NonePerformed

theorem approved_makes_authorization_decision_and_approves_operation
    (w : AuthorizationDecisionWitness)
    (h : w.ValidApproved) :
    w.authorizationDecisionMade = true ∧ w.operationApproved = true := by
  exact ⟨h.authorizationDecisionMade, h.operationApproved⟩

theorem approved_routes_to_separate_operation_start
    (w : AuthorizationDecisionWitness)
    (h : w.ValidApproved)
    (hLater : w.laterEffects.NonePerformed) :
    w.operationStartRequiredNext = true ∧
      w.laterEffects.operationStarted = false := by
  exact ⟨h.operationStartRequiredNext, hLater.operationNotStarted⟩

theorem denied_is_decision_without_operation_approval
    (w : AuthorizationDecisionWitness)
    (h : w.ValidDenied) :
    w.authorizationDecisionMade = true ∧ w.operationApproved = false := by
  exact ⟨h.authorizationDecisionMade, h.operationNotApproved⟩

theorem rejected_issues_no_authorization_decision
    (w : AuthorizationDecisionWitness)
    (h : w.ValidRejected) :
    w.decisionRecordIssued = false ∧ w.authorizationDecisionMade = false := by
  exact ⟨h.decisionRecordNotIssued, h.authorizationDecisionNotMade⟩

theorem valid_decision_performs_no_later_execution_effect
    (w : AuthorizationDecisionWitness)
    (h : w.Valid) :
    w.laterEffects.NonePerformed := by
  exact h.2

structure AuthorizationDerivation (Input Output : Type) where
  derive : Input → Output

theorem same_input_has_same_authorization_decision
    {Input Output : Type}
    (derivation : AuthorizationDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSLifecycleBoundedAuthorizationDecisionV0_12
