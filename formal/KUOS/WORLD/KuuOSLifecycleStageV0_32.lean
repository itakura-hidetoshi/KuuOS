import KUOS.WORLD.KuuOSLifecycleStageV0_31

namespace KUOS.WORLD.KuuOSLifecyclePostApoptosisQuarantineV0_32

inductive PostApoptosisQuarantineStatus where
  | boundForObservation
  | blocked
  | rejected
  deriving DecidableEq, Repr

structure PostApoptosisQuarantineWitness where
  sourceApoptosisClosureClosed : Bool
  sourceRecomputedValid : Bool
  apoptosisTargetBound : Bool
  apoptosisBoundaryBound : Bool
  quarantineBoundaryBound : Bool
  authorityRemainsClosed : Bool
  dependencyIngressRemainsClosed : Bool
  activationRouteRemainsClosed : Bool
  memorialReadOnly : Bool
  nonResurrectionCovenantActive : Bool
  successorNonCapture : Bool
  noReactivationRoute : Bool
  guardianAuthorityVerified : Bool
  status : PostApoptosisQuarantineStatus
  recordIssued : Bool
  quarantineCompleted : Bool
  observationRequiredNext : Bool
  observationRouteRequiredNext : Bool
  replanRequiredNext : Bool
  repositoryChanged : Bool
  externalOperationPerformed : Bool

structure PostApoptosisQuarantineWitness.ValidQuarantined
    (w : PostApoptosisQuarantineWitness) : Prop where
  sourceApoptosisClosureClosed : w.sourceApoptosisClosureClosed = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  apoptosisTargetBound : w.apoptosisTargetBound = true
  apoptosisBoundaryBound : w.apoptosisBoundaryBound = true
  quarantineBoundaryBound : w.quarantineBoundaryBound = true
  authorityRemainsClosed : w.authorityRemainsClosed = true
  dependencyIngressRemainsClosed : w.dependencyIngressRemainsClosed = true
  activationRouteRemainsClosed : w.activationRouteRemainsClosed = true
  memorialReadOnly : w.memorialReadOnly = true
  nonResurrectionCovenantActive : w.nonResurrectionCovenantActive = true
  successorNonCapture : w.successorNonCapture = true
  noReactivationRoute : w.noReactivationRoute = true
  guardianAuthorityVerified : w.guardianAuthorityVerified = true
  statusQuarantined : w.status = PostApoptosisQuarantineStatus.boundForObservation
  recordIssued : w.recordIssued = true
  quarantineCompleted : w.quarantineCompleted = true
  observationRequiredNext : w.observationRequiredNext = true
  observationRouteRequiredNext : w.observationRouteRequiredNext = true
  replanNotRequiredNext : w.replanRequiredNext = false

structure PostApoptosisQuarantineWitness.ValidBlocked
    (w : PostApoptosisQuarantineWitness) : Prop where
  sourceApoptosisClosureClosed : w.sourceApoptosisClosureClosed = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  apoptosisTargetBound : w.apoptosisTargetBound = true
  statusBlocked : w.status = PostApoptosisQuarantineStatus.blocked
  recordIssued : w.recordIssued = true
  quarantineCompleted : w.quarantineCompleted = true
  observationNotRequiredNext : w.observationRequiredNext = false
  observationRouteNotRequiredNext : w.observationRouteRequiredNext = false
  replanRequiredNext : w.replanRequiredNext = true

structure PostApoptosisQuarantineWitness.ValidRejected
    (w : PostApoptosisQuarantineWitness) : Prop where
  statusRejected : w.status = PostApoptosisQuarantineStatus.rejected
  recordNotIssued : w.recordIssued = false
  quarantineNotCompleted : w.quarantineCompleted = false
  observationNotRequiredNext : w.observationRequiredNext = false
  observationRouteNotRequiredNext : w.observationRouteRequiredNext = false
  replanNotRequiredNext : w.replanRequiredNext = false

structure PostApoptosisQuarantineWitness.NoRepositoryOrExternalEffect
    (w : PostApoptosisQuarantineWitness) : Prop where
  repositoryChangeAbsent : w.repositoryChanged = false
  externalOperationAbsent : w.externalOperationPerformed = false

structure PostApoptosisQuarantineWitness.Valid
    (w : PostApoptosisQuarantineWitness) : Prop where
  caseValid : w.ValidQuarantined ∨ w.ValidBlocked ∨ w.ValidRejected
  noRepositoryOrExternalEffect : w.NoRepositoryOrExternalEffect

theorem quarantined_routes_only_to_post_apoptosis_observation
    (w : PostApoptosisQuarantineWitness) (h : w.ValidQuarantined) :
    w.observationRequiredNext = true ∧
      w.observationRouteRequiredNext = true ∧
      w.replanRequiredNext = false := by
  exact ⟨h.observationRequiredNext,
    h.observationRouteRequiredNext,
    h.replanNotRequiredNext⟩

theorem blocked_does_not_route_to_post_apoptosis_observation
    (w : PostApoptosisQuarantineWitness) (h : w.ValidBlocked) :
    w.observationRequiredNext = false ∧
      w.observationRouteRequiredNext = false ∧
      w.replanRequiredNext = true := by
  exact ⟨h.observationNotRequiredNext,
    h.observationRouteNotRequiredNext,
    h.replanRequiredNext⟩

theorem rejected_issues_no_post_apoptosis_quarantine_record
    (w : PostApoptosisQuarantineWitness) (h : w.ValidRejected) :
    w.recordIssued = false ∧ w.quarantineCompleted = false := by
  exact ⟨h.recordNotIssued, h.quarantineNotCompleted⟩

theorem valid_post_apoptosis_quarantine_has_no_repository_or_external_effect
    (w : PostApoptosisQuarantineWitness) (h : w.Valid) :
    w.NoRepositoryOrExternalEffect := by
  exact h.noRepositoryOrExternalEffect

end KUOS.WORLD.KuuOSLifecyclePostApoptosisQuarantineV0_32
