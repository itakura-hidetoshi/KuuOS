import KUOS.WORLD.KuuOSLifecycleReviewV0_9

namespace KUOS.WORLD.KuuOSLifecycleBoundedRequestV0_10

inductive RequestStatus where
  | issuedForDecisionReview
  | blocked
  | rejected
  deriving DecidableEq, Repr

structure LaterStageEffects where
  decisionMade : Bool
  operationStarted : Bool
  operationCompleted : Bool
  lifecycleEffectPerformed : Bool
  repositoryChanged : Bool

structure RequestWitness where
  sourceRecomputedValid : Bool
  sourceReviewClear : Bool
  sourceBindingValid : Bool
  requesterQualified : Bool
  requesterIndependentFromPriorChain : Bool
  requesterIndependentFromDecisionAuthority : Bool
  requesterIndependentFromFutureOperator : Bool
  authorityOperatorSeparated : Bool
  conflictDisclosureComplete : Bool
  materialConflictPresent : Bool
  scopeBindingValid : Bool
  scopeBounded : Bool
  resourcesAllowed : Bool
  protectedResourcesExcluded : Bool
  reversibleOnly : Bool
  rollbackVerified : Bool
  recoveryVerified : Bool
  stopConditionsComplete : Bool
  abortRouteAvailable : Bool
  humanOversightAvailable : Bool
  monitoringComplete : Bool
  evidenceCaptureComplete : Bool
  simulationVerified : Bool
  windowValid : Bool
  protectedCoreExcluded : Bool
  institutionalHoldActive : Bool
  emergencyStateActive : Bool
  sourceFresh : Bool
  requestFresh : Bool
  decisionRouteAvailable : Bool
  appealRouteAvailable : Bool
  dissentRouteAvailable : Bool
  status : RequestStatus
  requestRecordIssued : Bool
  boundedRequestIssued : Bool
  readyForDecisionReview : Bool
  decisionReviewRequiredNext : Bool
  laterEffects : LaterStageEffects

structure LaterStageEffects.NonePerformed (e : LaterStageEffects) : Prop where
  decisionNotMade : e.decisionMade = false
  operationNotStarted : e.operationStarted = false
  operationNotCompleted : e.operationCompleted = false
  lifecycleEffectNotPerformed : e.lifecycleEffectPerformed = false
  repositoryNotChanged : e.repositoryChanged = false

structure RequestWitness.ValidIssued (w : RequestWitness) : Prop where
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceReviewClear : w.sourceReviewClear = true
  sourceBindingValid : w.sourceBindingValid = true
  requesterQualified : w.requesterQualified = true
  requesterIndependentFromPriorChain :
    w.requesterIndependentFromPriorChain = true
  requesterIndependentFromDecisionAuthority :
    w.requesterIndependentFromDecisionAuthority = true
  requesterIndependentFromFutureOperator :
    w.requesterIndependentFromFutureOperator = true
  authorityOperatorSeparated : w.authorityOperatorSeparated = true
  conflictDisclosureComplete : w.conflictDisclosureComplete = true
  materialConflictAbsent : w.materialConflictPresent = false
  scopeBindingValid : w.scopeBindingValid = true
  scopeBounded : w.scopeBounded = true
  resourcesAllowed : w.resourcesAllowed = true
  protectedResourcesExcluded : w.protectedResourcesExcluded = true
  reversibleOnly : w.reversibleOnly = true
  rollbackVerified : w.rollbackVerified = true
  recoveryVerified : w.recoveryVerified = true
  stopConditionsComplete : w.stopConditionsComplete = true
  abortRouteAvailable : w.abortRouteAvailable = true
  humanOversightAvailable : w.humanOversightAvailable = true
  monitoringComplete : w.monitoringComplete = true
  evidenceCaptureComplete : w.evidenceCaptureComplete = true
  simulationVerified : w.simulationVerified = true
  windowValid : w.windowValid = true
  protectedCoreExcluded : w.protectedCoreExcluded = true
  institutionalHoldAbsent : w.institutionalHoldActive = false
  emergencyStateAbsent : w.emergencyStateActive = false
  sourceFresh : w.sourceFresh = true
  requestFresh : w.requestFresh = true
  decisionRouteAvailable : w.decisionRouteAvailable = true
  appealRouteAvailable : w.appealRouteAvailable = true
  dissentRouteAvailable : w.dissentRouteAvailable = true
  statusIssued : w.status = RequestStatus.issuedForDecisionReview
  requestRecordIssued : w.requestRecordIssued = true
  boundedRequestIssued : w.boundedRequestIssued = true
  readyForDecisionReview : w.readyForDecisionReview = true
  decisionReviewRequiredNext : w.decisionReviewRequiredNext = true

structure RequestWitness.ValidBlocked (w : RequestWitness) : Prop where
  statusBlocked : w.status = RequestStatus.blocked
  requestRecordIssued : w.requestRecordIssued = true
  boundedRequestNotIssued : w.boundedRequestIssued = false
  notReadyForDecisionReview : w.readyForDecisionReview = false
  decisionReviewNotRequiredNext : w.decisionReviewRequiredNext = false

structure RequestWitness.ValidRejected (w : RequestWitness) : Prop where
  statusRejected : w.status = RequestStatus.rejected
  requestRecordNotIssued : w.requestRecordIssued = false
  boundedRequestNotIssued : w.boundedRequestIssued = false
  notReadyForDecisionReview : w.readyForDecisionReview = false
  decisionReviewNotRequiredNext : w.decisionReviewRequiredNext = false

def RequestWitness.Valid (w : RequestWitness) : Prop :=
  (w.ValidIssued ∨ w.ValidBlocked ∨ w.ValidRejected) ∧
    w.laterEffects.NonePerformed

theorem issued_routes_only_to_decision_review
    (w : RequestWitness)
    (h : w.ValidIssued) :
    w.boundedRequestIssued = true ∧
      w.readyForDecisionReview = true ∧
      w.decisionReviewRequiredNext = true := by
  exact ⟨h.boundedRequestIssued, h.readyForDecisionReview,
    h.decisionReviewRequiredNext⟩

theorem issued_preserves_role_separation
    (w : RequestWitness)
    (h : w.ValidIssued) :
    w.requesterIndependentFromDecisionAuthority = true ∧
      w.requesterIndependentFromFutureOperator = true ∧
      w.authorityOperatorSeparated = true := by
  exact ⟨h.requesterIndependentFromDecisionAuthority,
    h.requesterIndependentFromFutureOperator,
    h.authorityOperatorSeparated⟩

theorem blocked_does_not_issue_request
    (w : RequestWitness)
    (h : w.ValidBlocked) :
    w.boundedRequestIssued = false ∧
      w.readyForDecisionReview = false := by
  exact ⟨h.boundedRequestNotIssued, h.notReadyForDecisionReview⟩

theorem rejected_issues_no_valid_record
    (w : RequestWitness)
    (h : w.ValidRejected) :
    w.requestRecordIssued = false := by
  exact h.requestRecordNotIssued

theorem valid_request_performs_no_later_effect
    (w : RequestWitness)
    (h : w.Valid) :
    w.laterEffects.NonePerformed := by
  exact h.2

structure RequestDerivation (Input Output : Type) where
  derive : Input → Output

theorem same_input_has_same_request
    {Input Output : Type}
    (derivation : RequestDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSLifecycleBoundedRequestV0_10
