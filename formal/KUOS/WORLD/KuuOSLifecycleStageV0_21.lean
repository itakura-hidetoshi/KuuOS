import KUOS.WORLD.KuuOSLifecycleStageV0_20

namespace KUOS.WORLD.KuuOSLifecycleBoundedTransitionStartAuthorizationV0_21

inductive StartAuthorizationStatus where
  | authorizedForSeparateStart
  | denied
  | rejected
  deriving DecidableEq, Repr

structure StartAuthorizationWitness where
  sourceApproved : Bool
  sourceRecomputedValid : Bool
  sourceRouteBound : Bool
  startRouteBound : Bool
  authorizerAuthorityVerified : Bool
  authorizerSeparated : Bool
  packageFresh : Bool
  currentStateNotStale : Bool
  targetStateStillValid : Bool
  noHoldRecoveryOrAnomaly : Bool
  status : StartAuthorizationStatus
  recordIssued : Bool
  authorizationCompleted : Bool
  startAuthorized : Bool
  startRequiredNext : Bool
  startRouteRequiredNext : Bool
  reauthorizationOrReapprovalRequiredNext : Bool
  transitionStarted : Bool
  transitionCompleted : Bool
  lifecycleStateChanged : Bool
  repositoryEffectPerformed : Bool

structure StartAuthorizationWitness.ValidAuthorized
    (w : StartAuthorizationWitness) : Prop where
  sourceApproved : w.sourceApproved = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceRouteBound : w.sourceRouteBound = true
  startRouteBound : w.startRouteBound = true
  authorizerAuthorityVerified : w.authorizerAuthorityVerified = true
  authorizerSeparated : w.authorizerSeparated = true
  packageFresh : w.packageFresh = true
  currentStateNotStale : w.currentStateNotStale = true
  targetStateStillValid : w.targetStateStillValid = true
  noHoldRecoveryOrAnomaly : w.noHoldRecoveryOrAnomaly = true
  statusAuthorized :
    w.status = StartAuthorizationStatus.authorizedForSeparateStart
  recordIssued : w.recordIssued = true
  authorizationCompleted : w.authorizationCompleted = true
  startAuthorized : w.startAuthorized = true
  startRequiredNext : w.startRequiredNext = true
  startRouteRequiredNext : w.startRouteRequiredNext = true
  reauthorizationNotRequiredNext :
    w.reauthorizationOrReapprovalRequiredNext = false

structure StartAuthorizationWitness.ValidDenied
    (w : StartAuthorizationWitness) : Prop where
  sourceApproved : w.sourceApproved = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceRouteBound : w.sourceRouteBound = true
  statusDenied : w.status = StartAuthorizationStatus.denied
  recordIssued : w.recordIssued = true
  authorizationCompleted : w.authorizationCompleted = true
  startNotAuthorized : w.startAuthorized = false
  startNotRequiredNext : w.startRequiredNext = false
  startRouteNotRequiredNext : w.startRouteRequiredNext = false
  reauthorizationOrReapprovalRequiredNext :
    w.reauthorizationOrReapprovalRequiredNext = true

structure StartAuthorizationWitness.ValidRejected
    (w : StartAuthorizationWitness) : Prop where
  statusRejected : w.status = StartAuthorizationStatus.rejected
  recordNotIssued : w.recordIssued = false
  authorizationNotCompleted : w.authorizationCompleted = false
  startNotAuthorized : w.startAuthorized = false
  startNotRequiredNext : w.startRequiredNext = false
  startRouteNotRequiredNext : w.startRouteRequiredNext = false
  reauthorizationNotRequiredNext :
    w.reauthorizationOrReapprovalRequiredNext = false

structure StartAuthorizationWitness.NoEffects
    (w : StartAuthorizationWitness) : Prop where
  startAbsent : w.transitionStarted = false
  completionAbsent : w.transitionCompleted = false
  lifecycleStateUnchanged : w.lifecycleStateChanged = false
  repositoryEffectAbsent : w.repositoryEffectPerformed = false

structure StartAuthorizationWitness.Valid
    (w : StartAuthorizationWitness) : Prop where
  caseValid :
    w.ValidAuthorized ∨ w.ValidDenied ∨ w.ValidRejected
  noEffects : w.NoEffects

theorem authorized_routes_only_to_separate_start
    (w : StartAuthorizationWitness) (h : w.ValidAuthorized) :
    w.startAuthorized = true ∧
      w.startRequiredNext = true ∧
      w.startRouteRequiredNext = true := by
  exact ⟨h.startAuthorized, h.startRequiredNext,
    h.startRouteRequiredNext⟩

theorem denied_does_not_route_to_start
    (w : StartAuthorizationWitness) (h : w.ValidDenied) :
    w.startAuthorized = false ∧
      w.startRequiredNext = false ∧
      w.reauthorizationOrReapprovalRequiredNext = true := by
  exact ⟨h.startNotAuthorized, h.startNotRequiredNext,
    h.reauthorizationOrReapprovalRequiredNext⟩

theorem rejected_issues_no_record
    (w : StartAuthorizationWitness) (h : w.ValidRejected) :
    w.recordIssued = false ∧ w.authorizationCompleted = false := by
  exact ⟨h.recordNotIssued, h.authorizationNotCompleted⟩

theorem valid_start_authorization_has_no_effects
    (w : StartAuthorizationWitness) (h : w.Valid) : w.NoEffects := by
  exact h.noEffects

end KUOS.WORLD.KuuOSLifecycleBoundedTransitionStartAuthorizationV0_21
