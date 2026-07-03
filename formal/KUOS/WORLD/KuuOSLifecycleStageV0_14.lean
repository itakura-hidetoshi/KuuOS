import KUOS.WORLD.KuuOSLifecycleStageV0_13

namespace KUOS.WORLD.KuuOSLifecycleBoundedOperationStartV0_14

inductive OperationStartStatus where
  | startedForSeparateOperationCompletion
  | denied
  | rejected
  deriving DecidableEq, Repr

structure LaterStageEffects where
  operationCompleted : Bool
  authorityChanged : Bool
  quiescenceStateChanged : Bool
  terminalStateChanged : Bool
  terminalMarkerWritten : Bool
  resourceRemoved : Bool
  externalOperationPerformed : Bool
  repositoryChanged : Bool

structure OperationStartWitness where
  sourceRecomputedValid : Bool
  sourceOperationApprovalApproved : Bool
  sourceBindingValid : Bool
  operatorBindingValid : Bool
  routeBindingValid : Bool
  operatorSeparatedFromApprover : Bool
  operatorMandateVerified : Bool
  operatorQualified : Bool
  operatorIdentityConfirmed : Bool
  operatorReady : Bool
  executionPackageIntegrityReconfirmed : Bool
  resourcesReservedReconfirmed : Bool
  rollbackReadyReconfirmed : Bool
  monitoringReadyReconfirmed : Bool
  abortChannelReconfirmed : Bool
  status : OperationStartStatus
  operationStartRecordIssued : Bool
  operationStartDecisionMade : Bool
  operationStarted : Bool
  operationStartDenied : Bool
  operationCompletionRequiredNext : Bool
  operationCompletionRouteRequiredNext : Bool
  laterEffects : LaterStageEffects

structure LaterStageEffects.NonePerformed (e : LaterStageEffects) : Prop where
  operationNotCompleted : e.operationCompleted = false
  authorityNotChanged : e.authorityChanged = false
  quiescenceStateNotChanged : e.quiescenceStateChanged = false
  terminalStateNotChanged : e.terminalStateChanged = false
  terminalMarkerNotWritten : e.terminalMarkerWritten = false
  resourceNotRemoved : e.resourceRemoved = false
  externalOperationNotPerformed : e.externalOperationPerformed = false
  repositoryNotChanged : e.repositoryChanged = false

structure OperationStartWitness.ValidStarted
    (w : OperationStartWitness) : Prop where
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceOperationApprovalApproved : w.sourceOperationApprovalApproved = true
  sourceBindingValid : w.sourceBindingValid = true
  operatorBindingValid : w.operatorBindingValid = true
  routeBindingValid : w.routeBindingValid = true
  operatorSeparatedFromApprover : w.operatorSeparatedFromApprover = true
  operatorMandateVerified : w.operatorMandateVerified = true
  operatorQualified : w.operatorQualified = true
  operatorIdentityConfirmed : w.operatorIdentityConfirmed = true
  operatorReady : w.operatorReady = true
  executionPackageIntegrityReconfirmed :
    w.executionPackageIntegrityReconfirmed = true
  resourcesReservedReconfirmed : w.resourcesReservedReconfirmed = true
  rollbackReadyReconfirmed : w.rollbackReadyReconfirmed = true
  monitoringReadyReconfirmed : w.monitoringReadyReconfirmed = true
  abortChannelReconfirmed : w.abortChannelReconfirmed = true
  statusStarted :
    w.status = OperationStartStatus.startedForSeparateOperationCompletion
  operationStartRecordIssued : w.operationStartRecordIssued = true
  operationStartDecisionMade : w.operationStartDecisionMade = true
  operationStarted : w.operationStarted = true
  operationStartNotDenied : w.operationStartDenied = false
  operationCompletionRequiredNext : w.operationCompletionRequiredNext = true
  operationCompletionRouteRequiredNext :
    w.operationCompletionRouteRequiredNext = true

structure OperationStartWitness.ValidDenied
    (w : OperationStartWitness) : Prop where
  statusDenied : w.status = OperationStartStatus.denied
  operationStartRecordIssued : w.operationStartRecordIssued = true
  operationStartDecisionMade : w.operationStartDecisionMade = true
  operationNotStarted : w.operationStarted = false
  operationStartDenied : w.operationStartDenied = true
  operationCompletionNotRequiredNext :
    w.operationCompletionRequiredNext = false
  operationCompletionRouteNotRequiredNext :
    w.operationCompletionRouteRequiredNext = false

structure OperationStartWitness.ValidRejected
    (w : OperationStartWitness) : Prop where
  statusRejected : w.status = OperationStartStatus.rejected
  operationStartRecordNotIssued : w.operationStartRecordIssued = false
  operationStartDecisionNotMade : w.operationStartDecisionMade = false
  operationNotStarted : w.operationStarted = false
  operationStartNotDenied : w.operationStartDenied = false
  operationCompletionNotRequiredNext :
    w.operationCompletionRequiredNext = false
  operationCompletionRouteNotRequiredNext :
    w.operationCompletionRouteRequiredNext = false

def OperationStartWitness.Valid (w : OperationStartWitness) : Prop :=
  (w.ValidStarted ∨ w.ValidDenied ∨ w.ValidRejected) ∧
    w.laterEffects.NonePerformed

theorem started_is_real_operation_start
    (w : OperationStartWitness)
    (h : w.ValidStarted) :
    w.operationStartRecordIssued = true ∧
      w.operationStartDecisionMade = true ∧
      w.operationStarted = true := by
  exact ⟨h.operationStartRecordIssued,
    h.operationStartDecisionMade,
    h.operationStarted⟩

theorem started_routes_only_to_separate_operation_completion
    (w : OperationStartWitness)
    (h : w.ValidStarted) :
    w.operationCompletionRequiredNext = true ∧
      w.operationCompletionRouteRequiredNext = true := by
  exact ⟨h.operationCompletionRequiredNext,
    h.operationCompletionRouteRequiredNext⟩

theorem denied_does_not_start
    (w : OperationStartWitness)
    (h : w.ValidDenied) :
    w.operationStartDecisionMade = true ∧
      w.operationStartDenied = true ∧
      w.operationStarted = false := by
  exact ⟨h.operationStartDecisionMade,
    h.operationStartDenied,
    h.operationNotStarted⟩

theorem rejected_issues_no_valid_start_record
    (w : OperationStartWitness)
    (h : w.ValidRejected) :
    w.operationStartRecordIssued = false ∧
      w.operationStartDecisionMade = false := by
  exact ⟨h.operationStartRecordNotIssued,
    h.operationStartDecisionNotMade⟩

theorem valid_start_performs_no_completion_or_lifecycle_effect
    (w : OperationStartWitness)
    (h : w.Valid) :
    w.laterEffects.NonePerformed := by
  exact h.2

structure OperationStartDerivation (Input Output : Type) where
  derive : Input → Output

theorem same_input_has_same_operation_start
    {Input Output : Type}
    (derivation : OperationStartDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSLifecycleBoundedOperationStartV0_14
