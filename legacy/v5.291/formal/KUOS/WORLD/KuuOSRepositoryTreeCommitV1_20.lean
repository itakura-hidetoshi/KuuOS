import KUOS.WORLD.KuuOSRepositoryBoundedBlobV1_19

namespace KUOS.WORLD.KuuOSRepositoryTreeCommitV1_20

structure Witness where
  exactTree : Prop
  exactCommit : Prop
  treeChanged : Bool
  commitChanged : Bool
  elsewhereChanged : Bool

structure Witness.Valid (w : Witness) : Prop where
  exactTree : w.exactTree
  exactCommit : w.exactCommit
  changed : w.treeChanged = true ∨ w.commitChanged = true
  elsewhereUnchanged : w.elsewhereChanged = false


theorem exact_objects_are_scoped
    (w : Witness)
    (h : w.Valid) :
    w.exactTree ∧ w.exactCommit ∧
      (w.treeChanged = true ∨ w.commitChanged = true) ∧
      w.elsewhereChanged = false := by
  exact ⟨h.exactTree, h.exactCommit, h.changed, h.elsewhereUnchanged⟩

end KUOS.WORLD.KuuOSRepositoryTreeCommitV1_20
