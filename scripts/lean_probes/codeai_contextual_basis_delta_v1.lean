/- R66: exact contextual obstruction-basis deltas.
A route addition can reuse a certified basis; deleting a route need not be
invertible from the basis alone. No operational policy is modified. -/
namespace KuuOSR66
open KuuOSR62 KuuOSR63 KuuOSR64 KuuOSR65
universe u

def updateBasis {α : Type u} [DecidableEq α]
    (A : Finset α) (F : Finset (Finset α)) : Finset (Finset α) :=
  reduceCuts (extendCuts A F)

theorem update_eq {α : Type u} [DecidableEq α]
    (A : Finset α) (rest : List (Finset α)) :
    updateBasis A (incrementalBasis rest) = incrementalBasis (A :: rest) := rfl

theorem retained_iff_hits {α : Type u} [DecidableEq α]
    (A : Finset α) (rest : List (Finset α)) (S : Finset α)
    (hold : S ∈ incrementalBasis rest) :
    S ∈ incrementalBasis (A :: rest) ↔ Hits (fun x => x ∈ S) (fun x => x ∈ A) := by
  have hm := (incremental_exact rest S).mp hold
  constructor
  · intro hn
    exact ((incremental_exact (A :: rest) S).mp hn).1 A (List.mem_cons_self)
  · intro hh
    apply (incremental_exact (A :: rest) S).mpr
    refine ⟨?_, ?_⟩
    · intro B hB
      rcases List.mem_cons.mp hB with he | hr
      · subst B
        exact hh
      · exact hm.1 B hr
    · intro T hTS hT
      exact hm.2 T hTS (fun B hB => hT B (List.mem_cons_of_mem A hB))

theorem retained_eq_filter {α : Type u} [DecidableEq α]
    (A : Finset α) (rest : List (Finset α)) :
    incrementalBasis rest ∩ incrementalBasis (A :: rest) =
      (incrementalBasis rest).filter (fun S => ∃ x ∈ S, x ∈ A) := by
  apply Finset.ext
  intro S
  constructor
  · intro h
    obtain ⟨ho, hn⟩ := Finset.mem_inter.mp h
    exact Finset.mem_filter.mpr ⟨ho, (retained_iff_hits A rest S ho).mp hn⟩
  · intro h
    obtain ⟨ho, hh⟩ := Finset.mem_filter.mp h
    exact Finset.mem_inter.mpr ⟨ho, (retained_iff_hits A rest S ho).mpr hh⟩

theorem retired_iff_misses {α : Type u} [DecidableEq α]
    (A : Finset α) (rest : List (Finset α)) (S : Finset α) :
    S ∈ incrementalBasis rest \ incrementalBasis (A :: rest) ↔
      S ∈ incrementalBasis rest ∧ ¬ Hits (fun x => x ∈ S) (fun x => x ∈ A) := by
  constructor
  · intro h
    obtain ⟨ho, hn⟩ := Finset.mem_sdiff.mp h
    exact ⟨ho, fun hh => hn ((retained_iff_hits A rest S ho).mpr hh)⟩
  · rintro ⟨ho, hm⟩
    exact Finset.mem_sdiff.mpr ⟨ho, fun hn => hm ((retained_iff_hits A rest S ho).mp hn)⟩

theorem new_cut_origin {α : Type u} [DecidableEq α]
    (A : Finset α) (rest : List (Finset α)) (S : Finset α)
    (hs : S ∈ incrementalBasis (A :: rest) \ incrementalBasis rest) :
    ∃ T ∈ incrementalBasis rest, ∃ x ∈ A,
      ¬ Hits (fun y => y ∈ T) (fun y => y ∈ A) ∧ S = insert x T := by
  obtain ⟨hn, ho⟩ := Finset.mem_sdiff.mp hs
  have hr : S ∈ reduceCuts (extendCuts A (incrementalBasis rest)) := hn
  have he := ((mem_reduced_iff (extendCuts A (incrementalBasis rest)) S).mp hr).1
  unfold extendCuts at he
  obtain ⟨T, ht, hb⟩ := Finset.mem_biUnion.mp he
  by_cases h : ∃ x ∈ T, x ∈ A
  · rw [if_pos h] at hb
    have hst : S = T := Finset.mem_singleton.mp hb
    subst S
    exact False.elim (ho ht)
  · rw [if_neg h] at hb
    obtain ⟨x, hx, heq⟩ := Finset.mem_image.mp hb
    exact ⟨T, ht, x, hx, h, heq.symm⟩

theorem reconstruct_new {α : Type u} [DecidableEq α]
    (F G : Finset (Finset α)) : (F ∩ G) ∪ (G \ F) = G := by
  apply Finset.ext
  intro S
  simp only [Finset.mem_union, Finset.mem_inter, Finset.mem_sdiff]
  constructor
  · rintro (⟨_, hg⟩ | ⟨hg, _⟩)
    · exact hg
    · exact hg
  · intro hg
    by_cases hf : S ∈ F
    · exact Or.inl ⟨hf, hg⟩
    · exact Or.inr ⟨hg, hf⟩

theorem reconstruct_old {α : Type u} [DecidableEq α]
    (F G : Finset (Finset α)) : (F ∩ G) ∪ (F \ G) = F := by
  apply Finset.ext
  intro S
  simp only [Finset.mem_union, Finset.mem_inter, Finset.mem_sdiff]
  constructor
  · rintro (⟨hf, _⟩ | ⟨hf, _⟩)
    · exact hf
    · exact hf
  · intro hf
    by_cases hg : S ∈ G
    · exact Or.inl ⟨hf, hg⟩
    · exact Or.inr ⟨hf, hg⟩

theorem basis_congr_membership {α : Type u} [DecidableEq α]
    (rs ts : List (Finset α)) (h : ∀ A, A ∈ rs ↔ A ∈ ts) :
    incrementalBasis rs = incrementalBasis ts := by
  have hp : (fun T : Finset α => Covers rs (fun x => x ∈ T)) =
      (fun T : Finset α => Covers ts (fun x => x ∈ T)) := by
    funext T
    apply propext
    constructor
    · intro hc A ha
      exact hc A ((h A).mpr ha)
    · intro hc A ha
      exact hc A ((h A).mp ha)
  apply Finset.ext
  intro S
  have hmin : MinimalFor (fun T : Finset α => Covers rs (fun x => x ∈ T)) S ↔
      MinimalFor (fun T : Finset α => Covers ts (fun x => x ∈ T)) S := by
    rw [hp]
  exact (incremental_exact rs S).trans (hmin.trans (incremental_exact ts S).symm)

theorem swap_basis {α : Type u} [DecidableEq α] (A B : Finset α) :
    incrementalBasis [A, B] = incrementalBasis [B, A] := by
  apply basis_congr_membership
  intro X
  simp [or_comm]

-- A certified basis discards information needed by a later route deletion.
def deletionRoute : Finset Nat := {0}
def deletionLeft : List (Finset Nat) := [{0, 1}]
def deletionRight : List (Finset Nat) := [{0, 2}]

theorem deletion_collision :
    incrementalBasis (deletionRoute :: deletionLeft) =
      incrementalBasis (deletionRoute :: deletionRight) := by decide

theorem deletion_distinct :
    incrementalBasis deletionLeft ≠ incrementalBasis deletionRight := by decide

theorem deletion_no_inverse :
    ¬ ∃ recover : Finset Nat → Finset (Finset Nat) → Finset (Finset Nat),
      ∀ (A : Finset Nat) (rest : List (Finset Nat)),
        recover A (incrementalBasis (A :: rest)) = incrementalBasis rest := by
  rintro ⟨recover, h⟩
  have hl := h deletionRoute deletionLeft
  have hr := h deletionRoute deletionRight
  have he := congrArg (recover deletionRoute) deletion_collision
  exact deletion_distinct (hl.symm.trans (he.trans hr))

end KuuOSR66
