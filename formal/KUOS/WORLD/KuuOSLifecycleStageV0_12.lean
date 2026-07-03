import KUOS.WORLD.KuuOSLifecycleStageV0_11

namespace KUOS.WORLD.KuuOSLifecycleBoundedAuthorizationDecisionV0_12

inductive AuthorizationStatus where
  | approvedForSeparateOperationApproval
  | denied
  | rejected
  deriving DecidableEq, Repr

structure LaterStageEffects where
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

structure AuthorizationDecisionWitness where
  sourceRecomputedValid : Bool
  sourceReviewClear : Bool
  sourceBindingValid : Bool
  designatedDecisionMakerBindingValid : Bool
  decisionMakerMandateVerified : Bool
  decisionMakerQualified : Bool
  decisionMakerIndependenceDeclared : Bool
  decisionMakerIndependentFromPriorChain : Bool
  decisionMakerIndependentFromRequester : Bool
  decisionMakerIndependentFromSourceReviewer : Bool
  decisionMakerIndependentFromFutureOperator : Bool
  conflictDisclosureComplete : Bool
  materialConflictPresent : Bool
  jurisdictionVerified : Bool
  quorumSatisfied : Bool
  reasonedDecisionComplete : Bool
  proportionalitySatisfied : Bool
  lessRestrictiveAlternativesExhausted : Bool
  irreversibilityReviewComplete : Bool
  humanImpactReviewComplete : Bool
  scopeBindingValid : Bool
  packageSafetyValid : Bool
  sourceFresh : Bool
  decisionFresh : Bool
  operationApprovalRouteAvailable : Bool
  appealRouteAvailable : Bool
  dissentRouteAvailable : Bool
  minorityOpinionRecorded : Bool
  status : AuthorizationStatus
  authorizationDecisionRecordIssued : Bool
  authorizationDecisionMade : Bool
  authorizationApproved : Bool
  authorizationDenied : Bool
  operationApprovalRequiredNext : Bool
  operationApprovalRouteRequiredNext : Bool
  laterEffects : LaterStageEffects

structure LaterStageEffects.NonePerformed (e : LaterStageEffects) : Prop where
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

structure AuthorizationDecisionWitness.ValidApproved
    (w : AuthorizationDecisionWitness) : Prop where
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceReviewClear : w.sourceReviewClear = true
  sourceBindingValid : w.sourceBindingValid = true
  designatedDecisionMakerBindingValid :
    w.designatedDecisionMakerBindingValid = true
  decisionMakerMandateVerified : w.decisionMakerMandateVerified = true
  decisionMakerQualified : w.decisionMakerQualified = true
  decisionMakerIndependenceDeclared :
    w.decisionMakerIndependenceDeclared = true
  decisionMakerIndependentFromPriorChain :
    w.decisionMakerIndependentFromPriorChain = true
  decisionMakerIndependentFromRequester :
    w.decisionMakerIndependentFromRequester = true
  decisionMakerIndependentFromSourceReviewer :
    w.decisionMakerIndependentFromSourceReviewer = true
  decisionMakerIndependentFromFutureOperator :
    w.decisionMakerIndependentFromFutureOperator = true
  conflictDisclosureComplete : w.conflictDisclosureComplete = true
  materialConflictAbsent : w.materialConflictPresent = false
  jurisdictionVerified : w.jurisdictionVerified = true
  quorumSatisfied : w.quorumSatisfied = true
  reasonedDecisionComplete : w.reasonedDecisionComplete = true
  proportionalitySatisfied : w.proportionalitySatisfied = true
  lessRestrictiveAlternativesExhausted :
    w.lessRestrictiveAlternativesExhausted = true
  irreversibilityReviewComplete : w.irreversibilityReviewComplete = true
  humanImpactReviewComplete : w.humanImpactReviewComplete = true
  scopeBindingValid : w.scopeBindingValid = true
  packageSafetyValid : w.packageSafetyValid = true
  sourceFresh : w.sourceFresh = true
  decisionFresh : w.decisionFresh = true
  operationApprovalRouteAvailable : w.operationApprovalRouteAvailable = true
  appealRouteAvailable : w.appealRouteAvailable = true
  dissentRouteAvailable : w.dissentRouteAvailable = true
  minorityOpinionRecorded : w.minorityOpinionRecorded = true
  statusApproved :
    w.status = AuthorizationStatus.approvedForSeparateOperationApproval
  authorizationDecisionRecordIssued :
    w.authorizationDecisionRecordIssued = true
  authorizationDecisionMade : w.authorizationDecisionMade = true
  authorizationApproved : w.authorizationApproved = true
  authorizationNotDenied : w.authorizationDenied = false
  operationApprovalRequiredNext : w.operationApprovalRequiredNext = true
  operationApprovalRouteRequiredNext :
    w.operationApprovalRouteRequiredNext = true

structure AuthorizationDecisionWitness.ValidDenied
    (w : AuthorizationDecisionWitness) : Prop where
  statusDenied : w.status = AuthorizationStatus.denied
  authorizationDecisionRecordIssued :
    w.authorizationDecisionRecordIssued = true
  authorizationDecisionMade : w.authorizationDecisionMade = true
  authorizationNotApproved : w.authorizationApproved = false
  authorizationDenied : w.authorizationDenied = true
  operationApprovalNotRequiredNext :
    w.operationApprovalRequiredNext = false
  operationApprovalRouteNotRequiredNext :
    w.operationApprovalRouteRequiredNext = false

structure AuthorizationDecisionWitness.ValidRejected
    (w : AuthorizationDecisionWitness) : Prop where
  statusRejected : w.status = AuthorizationStatus.rejected
  authorizationDecisionRecordNotIssued :
    w.authorizationDecisionRecordIssued = false
  authorizationDecisionNotMade : w.authorizationDecisionMade = false
  authorizationNotApproved : w.authorizationApproved = false
  authorizationNotDenied : w.authorizationDenied = false
  operationApprovalNotRequiredNext :
    w.operationApprovalRequiredNext = false
  operationApprovalRouteNotRequiredNext :
    w.operationApprovalRouteRequiredNext = false

def AuthorizationDecisionWitness.Valid
    (w : AuthorizationDecisionWitness) : Prop :=
  (w.ValidApproved ∨ w.ValidDenied ∨ w.ValidRejected) ∧
    w.laterEffects.NonePerformed

theorem approved_is_authorization_decision_only
    (w : AuthorizationDecisionWitness)
    (h : w.ValidApproved) :
    w.authorizationDecisionRecordIssued = true ∧
      w.authorizationDecisionMade = true ∧
      w.authorizationApproved = true := by
  exact ⟨h.authorizationDecisionRecordIssued,
    h.authorizationDecisionMade,
    h.authorizationApproved⟩

theorem approved_routes_only_to_separate_operation_approval
    (w : AuthorizationDecisionWitness)
    (h : w.ValidApproved) :
    w.operationApprovalRequiredNext = true ∧
      w.operationApprovalRouteRequiredNext = true := by
  exact ⟨h.operationApprovalRequiredNext,
    h.operationApprovalRouteRequiredNext⟩

theorem approved_preserves_role_separation
    (w : AuthorizationDecisionWitness)
    (h : w.ValidApproved) :
    w.decisionMakerIndependentFromRequester = true ∧
      w.decisionMakerIndependentFromSourceReviewer = true ∧
      w.decisionMakerIndependentFromFutureOperator = true := by
  exact ⟨h.decisionMakerIndependentFromRequester,
    h.decisionMakerIndependentFromSourceReviewer,
    h.decisionMakerIndependentFromFutureOperator⟩

theorem denied_does_not_advance
    (w : AuthorizationDecisionWitness)
    (h : w.ValidDenied) :
    w.authorizationDecisionMade = true ∧
      w.authorizationDenied = true ∧
      w.operationApprovalRequiredNext = false := by
  exact ⟨h.authorizationDecisionMade,
    h.authorizationDenied,
    h.operationApprovalNotRequiredNext⟩

theorem rejected_issues_no_valid_decision_record
    (w : AuthorizationDecisionWitness)
    (h : w.ValidRejected) :
    w.authorizationDecisionRecordIssued = false ∧
      w.authorizationDecisionMade = false := by
  exact ⟨h.authorizationDecisionRecordNotIssued,
    h.authorizationDecisionNotMade⟩

theorem valid_authorization_performs_no_operation_or_lifecycle_effect
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
