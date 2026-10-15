import KUOS.WORLD.KuuOSRepositoryTreeCommitV1_20

namespace KUOS.WORLD.KuuOSRepositoryConstructedCommitPublicationV1_21

structure Witness where
  exactConstructedCommit : Prop
  referenceChanged : Bool
  objectDatabaseChangedNow : Bool
  indexChanged : Bool
  workingTreeChanged : Bool
  reflogChanged : Bool

structure Witness.ValidPublication (w : Witness) : Prop where
  exactConstructedCommit : w.exactConstructedCommit
  referenceChanged : w.referenceChanged = true
  objectDatabaseUnchangedNow : w.objectDatabaseChangedNow = false
  indexUnchanged : w.indexChanged = false
  workingTreeUnchanged : w.workingTreeChanged = false
  reflogUnchanged : w.reflogChanged = false


theorem publication_changes_only_checkpoint_reference
    (w : Witness)
    (h : w.ValidPublication) :
    w.exactConstructedCommit ∧
      w.referenceChanged = true ∧
      w.objectDatabaseChangedNow = false ∧
      w.indexChanged = false ∧
      w.workingTreeChanged = false ∧
      w.reflogChanged = false := by
  exact ⟨h.exactConstructedCommit, h.referenceChanged,
    h.objectDatabaseUnchangedNow, h.indexUnchanged,
    h.workingTreeUnchanged, h.reflogUnchanged⟩

end KUOS.WORLD.KuuOSRepositoryConstructedCommitPublicationV1_21
