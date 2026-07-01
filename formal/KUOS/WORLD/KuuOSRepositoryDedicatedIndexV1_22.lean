import KUOS.WORLD.KuuOSRepositoryConstructedCommitPublicationV1_21

namespace KUOS.WORLD.KuuOSRepositoryDedicatedIndexV1_22

structure Witness where
  exactDedicatedIndex : Prop
  dedicatedIndexChanged : Bool
  canonicalIndexChanged : Bool
  objectDatabaseChanged : Bool
  referenceChanged : Bool
  workingTreeChanged : Bool
  reflogChanged : Bool

structure Witness.Valid (w : Witness) : Prop where
  exactDedicatedIndex : w.exactDedicatedIndex
  dedicatedIndexChanged : w.dedicatedIndexChanged = true
  canonicalIndexUnchanged : w.canonicalIndexChanged = false
  objectDatabaseUnchanged : w.objectDatabaseChanged = false
  referenceUnchanged : w.referenceChanged = false
  workingTreeUnchanged : w.workingTreeChanged = false
  reflogUnchanged : w.reflogChanged = false


theorem dedicated_index_write_is_scoped
    (w : Witness)
    (h : w.Valid) :
    w.exactDedicatedIndex ∧
      w.dedicatedIndexChanged = true ∧
      w.canonicalIndexChanged = false ∧
      w.objectDatabaseChanged = false ∧
      w.referenceChanged = false ∧
      w.workingTreeChanged = false ∧
      w.reflogChanged = false := by
  exact ⟨h.exactDedicatedIndex, h.dedicatedIndexChanged,
    h.canonicalIndexUnchanged, h.objectDatabaseUnchanged,
    h.referenceUnchanged, h.workingTreeUnchanged, h.reflogUnchanged⟩

end KUOS.WORLD.KuuOSRepositoryDedicatedIndexV1_22
