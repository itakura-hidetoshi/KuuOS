import KUOS.WORLD.KuuOSLifecycleStageV0_34

namespace KUOS.WORLD.KuuOSLifecycleStageV0_35

inductive StoreStatus where
  | boundForFinal
  | alert
  | rejected
  deriving DecidableEq, Repr

structure StoreWitness where
  sourceSealed : Bool
  sourceRecomputed : Bool
  targetBound : Bool
  storeBound : Bool
  memorySealHeld : Bool
  memorialReadOnly : Bool
  covenantActive : Bool
  retrievalReadOnly : Bool
  stewardAuthorized : Bool
  status : StoreStatus
  recordIssued : Bool
  completed : Bool
  finalNext : Bool
  responseNext : Bool
  repositoryChanged : Bool
  externalOperationPerformed : Bool

structure StoreWitness.ValidStored (w : StoreWitness) : Prop where
  sourceSealed : w.sourceSealed = true
  sourceRecomputed : w.sourceRecomputed = true
  targetBound : w.targetBound = true
  storeBound : w.storeBound = true
  memorySealHeld : w.memorySealHeld = true
  memorialReadOnly : w.memorialReadOnly = true
  covenantActive : w.covenantActive = true
  retrievalReadOnly : w.retrievalReadOnly = true
  stewardAuthorized : w.stewardAuthorized = true
  statusStored : w.status = StoreStatus.boundForFinal
  recordIssued : w.recordIssued = true
  completed : w.completed = true
  finalNext : w.finalNext = true
  responseNotNext : w.responseNext = false

structure StoreWitness.ValidAlert (w : StoreWitness) : Prop where
  sourceSealed : w.sourceSealed = true
  sourceRecomputed : w.sourceRecomputed = true
  targetBound : w.targetBound = true
  statusAlert : w.status = StoreStatus.alert
  recordIssued : w.recordIssued = true
  completed : w.completed = true
  finalNotNext : w.finalNext = false
  responseNext : w.responseNext = true

structure StoreWitness.ValidRejected (w : StoreWitness) : Prop where
  statusRejected : w.status = StoreStatus.rejected
  recordNotIssued : w.recordIssued = false
  completedFalse : w.completed = false
  finalNotNext : w.finalNext = false
  responseNotNext : w.responseNext = false

structure StoreWitness.NoEffect (w : StoreWitness) : Prop where
  repositoryChangeAbsent : w.repositoryChanged = false
  externalOperationAbsent : w.externalOperationPerformed = false

structure StoreWitness.Valid (w : StoreWitness) : Prop where
  caseValid : w.ValidStored ∨ w.ValidAlert ∨ w.ValidRejected
  noEffect : w.NoEffect

theorem stored_routes_only_to_final
    (w : StoreWitness) (h : w.ValidStored) :
    w.finalNext = true ∧ w.responseNext = false := by
  exact ⟨h.finalNext, h.responseNotNext⟩

theorem alert_does_not_route_to_final
    (w : StoreWitness) (h : w.ValidAlert) :
    w.finalNext = false ∧ w.responseNext = true := by
  exact ⟨h.finalNotNext, h.responseNext⟩

theorem rejected_issues_no_record
    (w : StoreWitness) (h : w.ValidRejected) :
    w.recordIssued = false ∧ w.completed = false := by
  exact ⟨h.recordNotIssued, h.completedFalse⟩

theorem valid_has_no_effect
    (w : StoreWitness) (h : w.Valid) :
    w.NoEffect := by
  exact h.noEffect

end KUOS.WORLD.KuuOSLifecycleStageV0_35
