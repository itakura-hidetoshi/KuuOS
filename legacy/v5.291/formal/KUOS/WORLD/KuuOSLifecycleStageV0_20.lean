import KUOS.WORLD.KuuOSLifecycleStageV0_19

namespace KUOS.WORLD.KuuOSLifecycleBoundedTransitionApprovalV0_20

inductive ApprovalStatus where
  | approvedForSeparateStartAuthorization
  | denied
  | rejected
  deriving DecidableEq, Repr

structure ApprovalWitness where
  sourcePrepared : Bool
  sourceRecomputedValid : Bool
  packageRouteBound : Bool
  approvalRouteRecomputed : Bool
  approverAuthorityVerified : Bool
  approverSeparated : Bool
  packageFresh : Bool
  currentStateNotStale : Bool
  targetStateStillValid : Bool
  noHoldRecoveryOrAnomaly : Bool
  status : ApprovalStatus
  recordIssued : Bool
  approvalCompleted : Bool
  packageApproved : Bool
  startAuthorizationRequiredNext : Bool
  startAuthorizationRouteRequiredNext : Bool
  reapprovalOrRepreparationRequiredNext : Bool
  transitionStartAuthorized : Bool
  transitionStarted : Bool
  transitionCompleted : Bool
  lifecycleStateChanged : Bool
  repositoryEffectPerformed : Bool

structure ApprovalWitness.ValidApproved (w : ApprovalWitness) : Prop where
  sourcePrepared : w.sourcePrepared = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  packageRouteBound : w.packageRouteBound = true
  approvalRouteRecomputed : w.approvalRouteRecomputed = true
  approverAuthorityVerified : w.approverAuthorityVerified = true
  approverSeparated : w.approverSeparated = true
  packageFresh : w.packageFresh = true
  currentStateNotStale : w.currentStateNotStale = true
  targetStateStillValid : w.targetStateStillValid = true
  noHoldRecoveryOrAnomaly : w.noHoldRecoveryOrAnomaly = true
  statusApproved :
    w.status = ApprovalStatus.approvedForSeparateStartAuthorization
  recordIssued : w.recordIssued = true
  approvalCompleted : w.approvalCompleted = true
  packageApproved : w.packageApproved = true
  startAuthorizationRequiredNext :
    w.startAuthorizationRequiredNext = true
  startAuthorizationRouteRequiredNext :
    w.startAuthorizationRouteRequiredNext = true
  reapprovalNotRequiredNext :
    w.reapprovalOrRepreparationRequiredNext = false

structure ApprovalWitness.ValidDenied (w : ApprovalWitness) : Prop where
  sourcePrepared : w.sourcePrepared = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  packageRouteBound : w.packageRouteBound = true
  statusDenied : w.status = ApprovalStatus.denied
  recordIssued : w.recordIssued = true
  approvalCompleted : w.approvalCompleted = true
  packageNotApproved : w.packageApproved = false
  startAuthorizationNotRequiredNext :
    w.startAuthorizationRequiredNext = false
  startAuthorizationRouteNotRequiredNext :
    w.startAuthorizationRouteRequiredNext = false
  reapprovalOrRepreparationRequiredNext :
    w.reapprovalOrRepreparationRequiredNext = true

structure ApprovalWitness.ValidRejected (w : ApprovalWitness) : Prop where
  statusRejected : w.status = ApprovalStatus.rejected
  recordNotIssued : w.recordIssued = false
  approvalNotCompleted : w.approvalCompleted = false
  packageNotApproved : w.packageApproved = false
  startAuthorizationNotRequiredNext :
    w.startAuthorizationRequiredNext = false
  startAuthorizationRouteNotRequiredNext :
    w.startAuthorizationRouteRequiredNext = false
  reapprovalNotRequiredNext :
    w.reapprovalOrRepreparationRequiredNext = false

structure ApprovalWitness.NoEffects (w : ApprovalWitness) : Prop where
  startAuthorizationAbsent : w.transitionStartAuthorized = false
  startAbsent : w.transitionStarted = false
  completionAbsent : w.transitionCompleted = false
  lifecycleStateUnchanged : w.lifecycleStateChanged = false
  repositoryEffectAbsent : w.repositoryEffectPerformed = false

structure ApprovalWitness.Valid (w : ApprovalWitness) : Prop where
  caseValid : w.ValidApproved ∨ w.ValidDenied ∨ w.ValidRejected
  noEffects : w.NoEffects

theorem approved_routes_only_to_start_authorization
    (w : ApprovalWitness) (h : w.ValidApproved) :
    w.packageApproved = true ∧
      w.startAuthorizationRequiredNext = true ∧
      w.startAuthorizationRouteRequiredNext = true := by
  exact ⟨h.packageApproved, h.startAuthorizationRequiredNext,
    h.startAuthorizationRouteRequiredNext⟩

theorem denied_does_not_route_to_start_authorization
    (w : ApprovalWitness) (h : w.ValidDenied) :
    w.packageApproved = false ∧
      w.startAuthorizationRequiredNext = false ∧
      w.reapprovalOrRepreparationRequiredNext = true := by
  exact ⟨h.packageNotApproved, h.startAuthorizationNotRequiredNext,
    h.reapprovalOrRepreparationRequiredNext⟩

theorem rejected_issues_no_record
    (w : ApprovalWitness) (h : w.ValidRejected) :
    w.recordIssued = false ∧ w.approvalCompleted = false := by
  exact ⟨h.recordNotIssued, h.approvalNotCompleted⟩

theorem valid_approval_has_no_effects
    (w : ApprovalWitness) (h : w.Valid) : w.NoEffects := by
  exact h.noEffects

structure ApprovalDerivation (Input Output : Type) where
  derive : Input → Output

theorem same_input_same_approval
    {Input Output : Type}
    (d : ApprovalDerivation Input Output)
    (left right : Input)
    (h : left = right) : d.derive left = d.derive right := by
  exact congrArg d.derive h

end KUOS.WORLD.KuuOSLifecycleBoundedTransitionApprovalV0_20
