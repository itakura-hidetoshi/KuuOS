import KUOS.WORLD.KuuOSLifecycleStageV0_33

namespace KUOS.WORLD.KuuOSLifecycleLongTermMemoryV0_34

inductive MemoryStatus where
  | sealedForArchive
  | alert
  | rejected
  deriving DecidableEq, Repr

structure MemoryWitness where
  sourceStable : Bool
  sourceRecomputed : Bool
  targetBound : Bool
  memorySealed : Bool
  archiveBoundaryBound : Bool
  memorialReadOnly : Bool
  covenantActive : Bool
  retrievalReadOnly : Bool
  closureStillHeld : Bool
  stewardAuthorized : Bool
  status : MemoryStatus
  recordIssued : Bool
  completed : Bool
  archiveNext : Bool
  responseNext : Bool
  repositoryChanged : Bool
  externalOperationPerformed : Bool

structure MemoryWitness.ValidSealed (w : MemoryWitness) : Prop where
  sourceStable : w.sourceStable = true
  sourceRecomputed : w.sourceRecomputed = true
  targetBound : w.targetBound = true
  memorySealed : w.memorySealed = true
  archiveBoundaryBound : w.archiveBoundaryBound = true
  memorialReadOnly : w.memorialReadOnly = true
  covenantActive : w.covenantActive = true
  retrievalReadOnly : w.retrievalReadOnly = true
  closureStillHeld : w.closureStillHeld = true
  stewardAuthorized : w.stewardAuthorized = true
  statusSealed : w.status = MemoryStatus.sealedForArchive
  recordIssued : w.recordIssued = true
  completed : w.completed = true
  archiveNext : w.archiveNext = true
  responseNotNext : w.responseNext = false

structure MemoryWitness.ValidAlert (w : MemoryWitness) : Prop where
  sourceStable : w.sourceStable = true
  sourceRecomputed : w.sourceRecomputed = true
  targetBound : w.targetBound = true
  statusAlert : w.status = MemoryStatus.alert
  recordIssued : w.recordIssued = true
  completed : w.completed = true
  archiveNotNext : w.archiveNext = false
  responseNext : w.responseNext = true

structure MemoryWitness.ValidRejected (w : MemoryWitness) : Prop where
  statusRejected : w.status = MemoryStatus.rejected
  recordNotIssued : w.recordIssued = false
  completedFalse : w.completed = false
  archiveNotNext : w.archiveNext = false
  responseNotNext : w.responseNext = false

structure MemoryWitness.NoRepositoryOrExternalEffect (w : MemoryWitness) : Prop where
  repositoryChangeAbsent : w.repositoryChanged = false
  externalOperationAbsent : w.externalOperationPerformed = false

structure MemoryWitness.Valid (w : MemoryWitness) : Prop where
  caseValid : w.ValidSealed ∨ w.ValidAlert ∨ w.ValidRejected
  noEffect : w.NoRepositoryOrExternalEffect

theorem sealed_routes_only_to_archive
    (w : MemoryWitness) (h : w.ValidSealed) :
    w.archiveNext = true ∧ w.responseNext = false := by
  exact ⟨h.archiveNext, h.responseNotNext⟩

theorem alert_does_not_route_to_archive
    (w : MemoryWitness) (h : w.ValidAlert) :
    w.archiveNext = false ∧ w.responseNext = true := by
  exact ⟨h.archiveNotNext, h.responseNext⟩

theorem rejected_issues_no_memory_record
    (w : MemoryWitness) (h : w.ValidRejected) :
    w.recordIssued = false ∧ w.completed = false := by
  exact ⟨h.recordNotIssued, h.completedFalse⟩

theorem valid_memory_has_no_repository_or_external_effect
    (w : MemoryWitness) (h : w.Valid) :
    w.NoRepositoryOrExternalEffect := by
  exact h.noEffect

end KUOS.WORLD.KuuOSLifecycleLongTermMemoryV0_34
