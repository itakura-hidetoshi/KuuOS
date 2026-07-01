import KUOS.WORLD.KuuOSRepositoryCheckpointLiveRefCasV1_18

namespace KUOS.WORLD.KuuOSRepositoryBoundedBlobV1_19

structure Witness where
  authorized : Prop
  exactPayload : Prop
  exactCandidate : Prop
  blobChanged : Bool
  elsewhereChanged : Bool
  reused : Bool

structure Witness.ValidNew (w : Witness) : Prop where
  authorized : w.authorized
  exactPayload : w.exactPayload
  exactCandidate : w.exactCandidate
  blobChanged : w.blobChanged = true
  elsewhereUnchanged : w.elsewhereChanged = false
  notReused : w.reused = false

structure Witness.ValidReuse (w : Witness) : Prop where
  reused : w.reused = true
  blobUnchanged : w.blobChanged = false
  elsewhereUnchanged : w.elsewhereChanged = false


theorem new_blob_is_exact_and_scoped
    (w : Witness)
    (h : w.ValidNew) :
    w.authorized ∧ w.exactPayload ∧ w.exactCandidate ∧
      w.blobChanged = true ∧ w.elsewhereChanged = false := by
  exact ⟨h.authorized, h.exactPayload, h.exactCandidate,
    h.blobChanged, h.elsewhereUnchanged⟩


theorem reuse_changes_nothing
    (w : Witness)
    (h : w.ValidReuse) :
    w.blobChanged = false ∧ w.elsewhereChanged = false := by
  exact ⟨h.blobUnchanged, h.elsewhereUnchanged⟩

end KUOS.WORLD.KuuOSRepositoryBoundedBlobV1_19
