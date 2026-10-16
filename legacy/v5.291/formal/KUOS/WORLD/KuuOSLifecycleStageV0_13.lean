import KUOS.WORLD.KuuOSLifecycleStageV0_12

namespace KUOS.WORLD.KuuOSLifecycleBoundedOperationApprovalV0_13

inductive OperationApprovalStatus where
  | approvedForSeparateOperationStart
  | denied
  | rejected
  deriving DecidableEq, Repr

structure LaterStageEffects where
  operationStarted : Bool
  operationCompleted : Bool
  authorityChanged : Bool
  quiescenceStateChanged : Bool
  terminalStateChanged : Bool
  terminalMarkerWritten : Bool
  resourceRemoved : Bool
  externalOperationPerformed : Bool
  repositoryChanged : Bool

structure OperationApprovalWitness where
  sourceRecomputedValid : Bool
  sourceAuthorizationApproved : Bool
  sourceBindingValid : Bool
  routeBindingValid : Bool
  approverMandateVerified : Bool
  approverQualified : Bool
  approverIndependenceDeclared : Bool
  approverIndependentFromPriorChain : Bool
  approverIndependentFromAuthorizationDecisionMaker : Bool
  approverIndependentFromFutureOperator : Bool
  operatorAcknowledged : Bool
  executionPackageIntegrityVerified : Bool
  resourcesReserved : Bool
  rollbackReady : Bool
  monitoringReady : Bool
  abortChannelAvailable : Bool
  status : OperationApprovalStatus
  operationApprovalRecordIssued : Bool
  operationApprovalMade : Bool
  operationApproved : Bool
  operationDenied : Bool
  operationStartRequiredNext : Bool
  operationStartRouteRequiredNext : Bool
  laterEffects : LaterStageEffects

structure LaterStageEffects.NonePerformed (e : LaterStageEffects) : Prop where
  operationNotStarted : e.operationStarted = false
  operationNotCompleted : e.operationCompleted = false
  authorityNotChanged : e.authorityChanged = false
  quiescenceStateNotChanged : e.quiescenceStateChanged = false
  terminalStateNotChanged : e.terminalStateChanged = false
  terminalMarkerNotWritten : e.terminalMarkerWritten = false
  resourceNotRemoved : e.resourceRemoved = false
  externalOperationNotPerformed : e.externalOperationPerformed = false
  repositoryNotChanged : e.repositoryChanged = false

structure OperationApprovalWitness.ValidApproved
    (w : OperationApprovalWitness) : Prop where
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceAuthorizationApproved : w.sourceAuthorizationApproved = true
  sourceBindingValid : w.sourceBindingValid = true
  routeBindingValid : w.routeBindingValid = true
  approverMandateVerified : w.approverMandateVerified = true
  approverQualified : w.approverQualified = true
  approverIndependenceDeclared : w.approverIndependenceDeclared = true
  approverIndependentFromPriorChain :
    w.approverIndependentFromPriorChain = true
  approverIndependentFromAuthorizationDecisionMaker :
    w.approverIndependentFromAuthorizationDecisionMaker = true
  approverIndependentFromFutureOperator :
    w.approverIndependentFromFutureOperator = true
  operatorAcknowledged : w.operatorAcknowledged = true
  executionPackageIntegrityVerified :
    w.executionPackageIntegrityVerified = true
  resourcesReserved : w.resourcesReserved = true
  rollbackReady : w.rollbackReady = true
  monitoringReady : w.monitoringReady = true
  abortChannelAvailable : w.abortChannelAvailable = true
  statusApproved :
    w.status = OperationApprovalStatus.approvedForSeparateOperationStart
  operationApprovalRecordIssued : w.operationApprovalRecordIssued = true
  operationApprovalMade : w.operationApprovalMade = true
  operationApproved : w.operationApproved = true
  operationNotDenied : w.operationDenied = false
  operationStartRequiredNext : w.operationStartRequiredNext = true
  operationStartRouteRequiredNext : w.operationStartRouteRequiredNext = true

structure OperationApprovalWitness.ValidDenied
    (w : OperationApprovalWitness) : Prop where
  statusDenied : w.status = OperationApprovalStatus.denied
  operationApprovalRecordIssued : w.operationApprovalRecordIssued = true
  operationApprovalMade : w.operationApprovalMade = true
  operationNotApproved : w.operationApproved = false
  operationDenied : w.operationDenied = true
  operationStartNotRequiredNext : w.operationStartRequiredNext = false
  operationStartRouteNotRequiredNext :
    w.operationStartRouteRequiredNext = false

structure OperationApprovalWitness.ValidRejected
    (w : OperationApprovalWitness) : Prop where
  statusRejected : w.status = OperationApprovalStatus.rejected
  operationApprovalRecordNotIssued : w.operationApprovalRecordIssued = false
  operationApprovalNotMade : w.operationApprovalMade = false
  operationNotApproved : w.operationApproved = false
  operationNotDenied : w.operationDenied = false
  operationStartNotRequiredNext : w.operationStartRequiredNext = false
  operationStartRouteNotRequiredNext :
    w.operationStartRouteRequiredNext = false

def OperationApprovalWitness.Valid (w : OperationApprovalWitness) : Prop :=
  (w.ValidApproved ∨ w.ValidDenied ∨ w.ValidRejected) ∧
    w.laterEffects.NonePerformed

theorem approved_is_real_operation_approval
    (w : OperationApprovalWitness)
    (h : w.ValidApproved) :
    w.operationApprovalRecordIssued = true ∧
      w.operationApprovalMade = true ∧
      w.operationApproved = true := by
  exact ⟨h.operationApprovalRecordIssued,
    h.operationApprovalMade,
    h.operationApproved⟩

theorem approved_routes_only_to_separate_operation_start
    (w : OperationApprovalWitness)
    (h : w.ValidApproved) :
    w.operationStartRequiredNext = true ∧
      w.operationStartRouteRequiredNext = true := by
  exact ⟨h.operationStartRequiredNext,
    h.operationStartRouteRequiredNext⟩

theorem denied_does_not_advance
    (w : OperationApprovalWitness)
    (h : w.ValidDenied) :
    w.operationApprovalMade = true ∧
      w.operationDenied = true ∧
      w.operationStartRequiredNext = false := by
  exact ⟨h.operationApprovalMade,
    h.operationDenied,
    h.operationStartNotRequiredNext⟩

theorem rejected_issues_no_valid_approval_record
    (w : OperationApprovalWitness)
    (h : w.ValidRejected) :
    w.operationApprovalRecordIssued = false ∧
      w.operationApprovalMade = false := by
  exact ⟨h.operationApprovalRecordNotIssued,
    h.operationApprovalNotMade⟩

theorem valid_approval_performs_no_execution_or_lifecycle_effect
    (w : OperationApprovalWitness)
    (h : w.Valid) :
    w.laterEffects.NonePerformed := by
  exact h.2

structure OperationApprovalDerivation (Input Output : Type) where
  derive : Input → Output

theorem same_input_has_same_operation_approval
    {Input Output : Type}
    (derivation : OperationApprovalDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSLifecycleBoundedOperationApprovalV0_13
