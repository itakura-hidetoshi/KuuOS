/- R67: reversible finite obstruction-basis patches.
A checked patch validates the set difference and, separately, an expected
endpoint. Mathematical reconstruction is not execution authority.
The R66 deletion obstruction is retained, not bypassed. -/
namespace KuuOSR67
open KuuOSR62 KuuOSR63 KuuOSR64 KuuOSR65 KuuOSR66
universe u

def PatchValid {α : Type u} [DecidableEq α]
    (F R N : Finset (Finset α)) : Prop :=
  R ⊆ F ∧ ∀ x ∈ N, x ∉ F

def applyPatch {α : Type u} [DecidableEq α]
    (F R N : Finset (Finset α)) : Finset (Finset α) := (F \ R) ∪ N

def checkedPatch {α : Type u} [DecidableEq α]
    (F R N : Finset (Finset α)) : Option (Finset (Finset α)) :=
  if R ⊆ F ∧ ∀ x ∈ N, x ∉ F then some (applyPatch F R N) else none

def checkedBoundPatch {α : Type u} [DecidableEq α]
    (F G R N : Finset (Finset α)) : Option (Finset (Finset α)) :=
  if (R ⊆ F ∧ ∀ x ∈ N, x ∉ F) ∧ applyPatch F R N = G
  then some G else none

theorem patch_retired {α : Type u} [DecidableEq α]
    (F R N : Finset (Finset α)) (h : PatchValid F R N) :
    F \ applyPatch F R N = R := by
  apply Finset.ext
  intro x
  constructor
  · intro hx
    obtain ⟨hf, hn⟩ := Finset.mem_sdiff.mp hx
    by_contra hr
    exact hn (Finset.mem_union.mpr (Or.inl (Finset.mem_sdiff.mpr ⟨hf, hr⟩)))
  · intro hr
    refine Finset.mem_sdiff.mpr ⟨h.1 hr, ?_⟩
    intro hg
    rcases Finset.mem_union.mp hg with hd | hn
    · exact (Finset.mem_sdiff.mp hd).2 hr
    · exact h.2 x hn (h.1 hr)

theorem patch_introduced {α : Type u} [DecidableEq α]
    (F R N : Finset (Finset α)) (h : PatchValid F R N) :
    applyPatch F R N \ F = N := by
  apply Finset.ext
  intro x
  constructor
  · intro hx
    obtain ⟨hg, hf⟩ := Finset.mem_sdiff.mp hx
    rcases Finset.mem_union.mp hg with hd | hn
    · exact False.elim (hf (Finset.mem_sdiff.mp hd).1)
    · exact hn
  · intro hn
    exact Finset.mem_sdiff.mpr ⟨Finset.mem_union.mpr (Or.inr hn), h.2 x hn⟩

theorem reverse_valid {α : Type u} [DecidableEq α]
    (F R N : Finset (Finset α)) (h : PatchValid F R N) :
    PatchValid (applyPatch F R N) N R := by
  refine ⟨?_, ?_⟩
  · intro x hx
    exact Finset.mem_union.mpr (Or.inr hx)
  · intro x hx
    have hx' : x ∈ F \ applyPatch F R N := (patch_retired F R N h).symm ▸ hx
    exact (Finset.mem_sdiff.mp hx').2

theorem actual_patch_valid {α : Type u} [DecidableEq α]
    (F G : Finset (Finset α)) : PatchValid F (F \ G) (G \ F) := by
  refine ⟨?_, ?_⟩
  · intro x hx
    exact (Finset.mem_sdiff.mp hx).1
  · intro x hx
    exact (Finset.mem_sdiff.mp hx).2

theorem keep_eq_inter {α : Type u} [DecidableEq α]
    (F G : Finset (Finset α)) : F \ (F \ G) = F ∩ G := by
  apply Finset.ext
  intro x
  constructor
  · intro hx
    obtain ⟨hf, hn⟩ := Finset.mem_sdiff.mp hx
    refine Finset.mem_inter.mpr ⟨hf, ?_⟩
    by_contra hg
    exact hn (Finset.mem_sdiff.mpr ⟨hf, hg⟩)
  · intro hx
    obtain ⟨hf, hg⟩ := Finset.mem_inter.mp hx
    exact Finset.mem_sdiff.mpr ⟨hf, fun hn => (Finset.mem_sdiff.mp hn).2 hg⟩

theorem apply_diff_exact {α : Type u} [DecidableEq α]
    (F G : Finset (Finset α)) : applyPatch F (F \ G) (G \ F) = G := by
  unfold applyPatch
  rw [keep_eq_inter]
  exact reconstruct_new F G

theorem rollback_exact {α : Type u} [DecidableEq α]
    (F R N : Finset (Finset α)) (h : PatchValid F R N) :
    applyPatch (applyPatch F R N) N R = F := by
  calc
    _ = applyPatch (applyPatch F R N) (applyPatch F R N \ F)
          (F \ applyPatch F R N) :=
        congrArg₂ (applyPatch (applyPatch F R N))
          (patch_introduced F R N h).symm (patch_retired F R N h).symm
    _ = F := apply_diff_exact (applyPatch F R N) F

theorem patch_unique {α : Type u} [DecidableEq α]
    (F G R N : Finset (Finset α)) (h : PatchValid F R N)
    (he : applyPatch F R N = G) : R = F \ G ∧ N = G \ F := by
  subst G
  exact ⟨(patch_retired F R N h).symm, (patch_introduced F R N h).symm⟩

theorem checked_diff_exact {α : Type u} [DecidableEq α]
    (F G : Finset (Finset α)) : checkedPatch F (F \ G) (G \ F) = some G := by
  unfold checkedPatch
  rw [if_pos (actual_patch_valid F G)]
  exact congrArg some (apply_diff_exact F G)

theorem checked_roundtrip {α : Type u} [DecidableEq α]
    (F R N : Finset (Finset α)) (h : PatchValid F R N) :
    checkedPatch (applyPatch F R N) N R = some F := by
  unfold checkedPatch
  rw [if_pos (reverse_valid F R N h)]
  exact congrArg some (rollback_exact F R N h)

theorem checked_reject_missing {α : Type u} [DecidableEq α]
    (F R N : Finset (Finset α)) (x : Finset α) (hr : x ∈ R) (hf : x ∉ F) :
    checkedPatch F R N = none := by
  unfold checkedPatch
  exact if_neg (fun h => hf (h.1 hr))

theorem checked_reject_overlap {α : Type u} [DecidableEq α]
    (F R N : Finset (Finset α)) (x : Finset α) (hn : x ∈ N) (hf : x ∈ F) :
    checkedPatch F R N = none := by
  unfold checkedPatch
  exact if_neg (fun h => h.2 x hn hf)

theorem checked_bound_exact {α : Type u} [DecidableEq α]
    (F G : Finset (Finset α)) :
    checkedBoundPatch F G (F \ G) (G \ F) = some G := by
  unfold checkedBoundPatch
  exact if_pos ⟨actual_patch_valid F G, apply_diff_exact F G⟩

theorem checked_bound_reject_wrong {α : Type u} [DecidableEq α]
    (F G R N : Finset (Finset α)) (h : applyPatch F R N ≠ G) :
    checkedBoundPatch F G R N = none := by
  unfold checkedBoundPatch
  exact if_neg (fun hh => h hh.2)

end KuuOSR67
