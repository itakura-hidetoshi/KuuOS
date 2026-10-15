import KUOS.WORLD.KuuOSLifecycleStageV0_32

namespace KUOS.WORLD.KuuOSLifecyclePostApoptosisObservationV0_33

inductive ObservationStatus where
  | stableForLongTermMemory
  | alert
  | rejected
  deriving DecidableEq, Repr

structure ObservationWitness where
  sourceQuarantined : Bool
  sourceRecomputed : Bool
  targetBound : Bool
  quarantineBoundaryBound : Bool
  closureStillHeld : Bool
  memorialReadOnly : Bool
  covenantActive : Bool
  noReactivationRoute : Bool
  noBoundaryDrift : Bool
  observerAuthorized : Bool
  status : ObservationStatus
  recordIssued : Bool
  completed : Bool
  longTermMemoryNext : Bool
  responseNext : Bool
  repositoryChanged : Bool
  externalOperationPerformed : Bool

structure ObservationWitness.ValidStable (w : ObservationWitness) : Prop where
  sourceQuarantined : w.sourceQuarantined = true
  sourceRecomputed : w.sourceRecomputed = true
  targetBound : w.targetBound = true
  quarantineBoundaryBound : w.quarantineBoundaryBound = true
  closureStillHeld : w.closureStillHeld = true
  memorialReadOnly : w.memorialReadOnly = true
  covenantActive : w.covenantActive = true
  noReactivationRoute : w.noReactivationRoute = true
  noBoundaryDrift : w.noBoundaryDrift = true
  observerAuthorized : w.observerAuthorized = true
  statusStable : w.status = ObservationStatus.stableForLongTermMemory
  recordIssued : w.recordIssued = true
  completed : w.completed = true
  longTermMemoryNext : w.longTermMemoryNext = true
  responseNotNext : w.responseNext = false

structure ObservationWitness.ValidAlert (w : ObservationWitness) : Prop where
  sourceQuarantined : w.sourceQuarantined = true
  sourceRecomputed : w.sourceRecomputed = true
  targetBound : w.targetBound = true
  statusAlert : w.status = ObservationStatus.alert
  recordIssued : w.recordIssued = true
  completed : w.completed = true
  longTermMemoryNotNext : w.longTermMemoryNext = false
  responseNext : w.responseNext = true

structure ObservationWitness.ValidRejected (w : ObservationWitness) : Prop where
  statusRejected : w.status = ObservationStatus.rejected
  recordNotIssued : w.recordIssued = false
  completedFalse : w.completed = false
  longTermMemoryNotNext : w.longTermMemoryNext = false
  responseNotNext : w.responseNext = false

structure ObservationWitness.NoRepositoryOrExternalEffect (w : ObservationWitness) : Prop where
  repositoryChangeAbsent : w.repositoryChanged = false
  externalOperationAbsent : w.externalOperationPerformed = false

structure ObservationWitness.Valid (w : ObservationWitness) : Prop where
  caseValid : w.ValidStable ∨ w.ValidAlert ∨ w.ValidRejected
  noEffect : w.NoRepositoryOrExternalEffect

theorem stable_routes_only_to_long_term_memory
    (w : ObservationWitness) (h : w.ValidStable) :
    w.longTermMemoryNext = true ∧ w.responseNext = false := by
  exact ⟨h.longTermMemoryNext, h.responseNotNext⟩

theorem alert_does_not_route_to_long_term_memory
    (w : ObservationWitness) (h : w.ValidAlert) :
    w.longTermMemoryNext = false ∧ w.responseNext = true := by
  exact ⟨h.longTermMemoryNotNext, h.responseNext⟩

theorem rejected_issues_no_observation_record
    (w : ObservationWitness) (h : w.ValidRejected) :
    w.recordIssued = false ∧ w.completed = false := by
  exact ⟨h.recordNotIssued, h.completedFalse⟩

theorem valid_observation_has_no_repository_or_external_effect
    (w : ObservationWitness) (h : w.Valid) :
    w.NoRepositoryOrExternalEffect := by
  exact h.noEffect

end KUOS.WORLD.KuuOSLifecyclePostApoptosisObservationV0_33
