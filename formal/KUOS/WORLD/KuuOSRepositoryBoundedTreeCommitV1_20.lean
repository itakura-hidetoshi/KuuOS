import KUOS.WORLD.KuuOSRepositoryBoundedBlobV1_19

namespace KUOS.WORLD.KuuOSRepositoryBoundedTreeCommitV1_20

structure Witness where
  authorized : Prop
  exactCandidate : Prop
  referencedObjectsExact : Prop
  treesChanged : Bool
  commitChanged : Bool
  refsChanged : Bool
  indexChanged : Bool
  workingTreeChanged : Bool
  reflogChanged : Bool
  pushed : Bool
  signed : Bool
  reused : Bool

structure Witness.ValidNew (w : Witness) : Prop where
  authorized : w.authorized
  exactCandidate : w.exactCandidate
  referencedObjectsExact : w.referencedObjectsExact
  treesChanged : w.treesChanged = true
  commitChanged : w.commitChanged = true
  refsUnchanged : w.refsChanged = false
  indexUnchanged : w.indexChanged = false
  workingTreeUnchanged : w.workingTreeChanged = false
  reflogUnchanged : w.reflogChanged = false
  notPushed : w.pushed = false
  notSigned : w.signed = false
  notReused : w.reused = false

structure Witness.ValidReuse (w : Witness) : Prop where
  reused : w.reused = true
  treesUnchanged : w.treesChanged = false
  commitUnchanged : w.commitChanged = false
  refsUnchanged : w.refsChanged = false
  indexUnchanged : w.indexChanged = false
  workingTreeUnchanged : w.workingTreeChanged = false
  reflogUnchanged : w.reflogChanged = false
  notPushed : w.pushed = false
  notSigned : w.signed = false


theorem new_tree_commit_objects_are_exact_and_scoped
    (w : Witness)
    (h : w.ValidNew) :
    w.authorized ∧ w.exactCandidate ∧ w.referencedObjectsExact ∧
      w.treesChanged = true ∧ w.commitChanged = true ∧
      w.refsChanged = false ∧ w.indexChanged = false ∧
      w.workingTreeChanged = false ∧ w.reflogChanged = false ∧
      w.pushed = false ∧ w.signed = false := by
  exact ⟨h.authorized, h.exactCandidate, h.referencedObjectsExact,
    h.treesChanged, h.commitChanged, h.refsUnchanged, h.indexUnchanged,
    h.workingTreeUnchanged, h.reflogUnchanged, h.notPushed, h.notSigned⟩


theorem reuse_changes_no_repository_surface
    (w : Witness)
    (h : w.ValidReuse) :
    w.treesChanged = false ∧ w.commitChanged = false ∧
      w.refsChanged = false ∧ w.indexChanged = false ∧
      w.workingTreeChanged = false ∧ w.reflogChanged = false ∧
      w.pushed = false ∧ w.signed = false := by
  exact ⟨h.treesUnchanged, h.commitUnchanged, h.refsUnchanged,
    h.indexUnchanged, h.workingTreeUnchanged, h.reflogUnchanged,
    h.notPushed, h.notSigned⟩

end KUOS.WORLD.KuuOSRepositoryBoundedTreeCommitV1_20
