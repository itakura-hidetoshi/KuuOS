import KUOS.WORLD.KuuOSRepositoryConstructedCommitPublicationV1_21

namespace KUOS.WORLD.KuuOSRepositoryCheckpointReflogV1_24

structure Witness where
  exactCheckpointReflog : Prop
  checkpointReflogChanged : Bool
  otherReflogChanged : Bool
  referenceChanged : Bool
  objectDatabaseChanged : Bool
  indexChanged : Bool
  workingTreeChanged : Bool

structure Witness.Valid (w : Witness) : Prop where
  exactCheckpointReflog : w.exactCheckpointReflog
  checkpointReflogChanged : w.checkpointReflogChanged = true
  otherReflogUnchanged : w.otherReflogChanged = false
  referenceUnchanged : w.referenceChanged = false
  objectDatabaseUnchanged : w.objectDatabaseChanged = false
  indexUnchanged : w.indexChanged = false
  workingTreeUnchanged : w.workingTreeChanged = false


theorem checkpoint_reflog_write_is_scoped
    (w : Witness)
    (h : w.Valid) :
    w.exactCheckpointReflog ∧
      w.checkpointReflogChanged = true ∧
      w.otherReflogChanged = false ∧
      w.referenceChanged = false ∧
      w.objectDatabaseChanged = false ∧
      w.indexChanged = false ∧
      w.workingTreeChanged = false := by
  exact ⟨h.exactCheckpointReflog, h.checkpointReflogChanged,
    h.otherReflogUnchanged, h.referenceUnchanged,
    h.objectDatabaseUnchanged, h.indexUnchanged,
    h.workingTreeUnchanged⟩

end KUOS.WORLD.KuuOSRepositoryCheckpointReflogV1_24
