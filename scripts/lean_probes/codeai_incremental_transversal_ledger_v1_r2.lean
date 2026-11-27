/- R65: incremental minimal transversal enumeration.
Every step retains already hitting candidates, extends only the others,
and removes supersets. The reference semantics is the certified R64 basis.
The actual ledger is replayed separately by the verifier. -/
namespace KuuOSR65
open KuuOSR62 KuuOSR63 KuuOSR64
universe u

def extendCuts {α : Type u} [DecidableEq α]
    (A : Finset α) (F : Finset (Finset α)) : Finset (Finset α) :=
  F.biUnion (fun S => if ∃ x ∈ S, x ∈ A then {S}
    else A.image (fun x => insert x S))

def incrementalBasis {α : Type u} [DecidableEq α] :
    List (Finset α) → Finset (Finset α)
  | [] => finiteBasis []
  | A :: rest => reduceCuts (extendCuts A (incrementalBasis rest))

theorem extend_sound {α : Type u} [DecidableEq α]
    (A : Finset α) (rest : List (Finset α)) (S : Finset α)
    (hs : S ∈ extendCuts A (finiteBasis rest)) :
    Covers (A :: rest) (fun x => x ∈ S) := by
  unfold extendCuts at hs
  obtain ⟨T, ht, hbranch⟩ := Finset.mem_biUnion.mp hs
  have htCov := ((mem_finite_basis rest T).mp ht).1
  by_cases h : ∃ x ∈ T, x ∈ A
  · rw [if_pos h] at hbranch
    have he : S = T := Finset.mem_singleton.mp hbranch
    subst S
    intro B hB
    rcases List.mem_cons.mp hB with he | hr
    · subst B
      exact h
    · exact htCov B hr
  · rw [if_neg h] at hbranch
    obtain ⟨x, hx, he⟩ := Finset.mem_image.mp hbranch
    subst S
    intro B hB
    rcases List.mem_cons.mp hB with he | hr
    · subst B
      exact ⟨x, Finset.mem_insert_self x T, hx⟩
    · obtain ⟨y, hy, hBy⟩ := htCov B hr
      exact ⟨y, Finset.mem_insert_of_mem hy, hBy⟩

theorem extend_complete {α : Type u} [DecidableEq α]
    (A : Finset α) (rest : List (Finset α)) (S : Finset α)
    (hs : Covers (A :: rest) (fun x => x ∈ S)) :
    ∃ T ∈ extendCuts A (finiteBasis rest), T ⊆ S := by
  have hrest : Covers rest (fun x => x ∈ S) :=
    fun B hb => hs B (List.mem_cons_of_mem A hb)
  obtain ⟨T, ht, hts⟩ := (enumerator_complete rest (fun x => x ∈ S)).mp hrest
  have ha : Hits (fun x => x ∈ S) (fun x => x ∈ A) := hs A (by simp)
  by_cases h : ∃ x ∈ T, x ∈ A
  · refine ⟨T, ?_, ?_⟩
    · unfold extendCuts
      apply Finset.mem_biUnion.mpr
      refine ⟨T, ht, ?_⟩
      rw [if_pos h]
      exact Finset.mem_singleton.mpr rfl
    · intro y hy
      exact hts y hy
  · obtain ⟨x, hx, hxa⟩ := ha
    refine ⟨insert x T, ?_, ?_⟩
    · unfold extendCuts
      apply Finset.mem_biUnion.mpr
      refine ⟨T, ht, ?_⟩
      rw [if_neg h]
      exact Finset.mem_image.mpr ⟨x, hxa, rfl⟩
    · intro y hy
      rcases Finset.mem_insert.mp hy with he | hm
      · rw [he]
        exact hx
      · exact hts y hm

theorem reduce_exact {α : Type u} [DecidableEq α]
    (F : Finset (Finset α)) (P : Finset α → Prop)
    (hSound : ∀ S ∈ F, P S)
    (hComplete : ∀ S, P S → ∃ T ∈ F, T ⊆ S)
    (S : Finset α) :
    S ∈ reduceCuts F ↔ MinimalFor P S := by
  rw [mem_reduced_iff]
  constructor
  · rintro ⟨hs, hm⟩
    refine ⟨hSound S hs, ?_⟩
    intro T hTS hT
    obtain ⟨C, hc, hCT⟩ := hComplete T hT
    have hCS : C ⊆ S := by
      intro x hx
      exact hTS (hCT hx)
    have hSC := hm C hc hCS
    intro x hx
    exact hCT (hSC hx)
  · intro hm
    obtain ⟨C, hc, hCS⟩ := hComplete S hm.1
    have hSC := hm.2 C hCS (hSound C hc)
    have he : C = S := Finset.ext (fun x => ⟨fun hx => hCS hx, fun hx => hSC hx⟩)
    subst C
    exact ⟨hc, fun T hT hTS => hm.2 T hTS (hSound T hT)⟩

theorem incremental_eq_reference {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) :
    incrementalBasis routes = finiteBasis routes := by
  induction routes with
  | nil => rfl
  | cons A rest ih =>
      rw [incrementalBasis, ih]
      apply Finset.ext
      intro S
      exact (reduce_exact (extendCuts A (finiteBasis rest))
        (fun T => Covers (A :: rest) (fun x => x ∈ T))
        (extend_sound A rest) (extend_complete A rest) S).trans
        (mem_finite_basis (A :: rest) S).symm

theorem incremental_exact {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) (S : Finset α) :
    S ∈ incrementalBasis routes ↔
      MinimalFor (fun T => Covers routes (fun x => x ∈ T)) S := by
  rw [incremental_eq_reference]
  exact mem_finite_basis routes S

theorem incremental_recovery_duality {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) (D R : α → Prop) :
    (∃ i, Eligible (Residual D R) (routeDeps routes i)) ↔
      ∀ C, (∃ S ∈ incrementalBasis routes, ∀ x, C x ↔ x ∈ S) →
        Included C D → Hits R C := by
  rw [incremental_eq_reference]
  exact enumerated_recovery_duality routes D R

-- The operational wrapper never upgrades an empty inventory into evidence.
def admitIncremental {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) : Option (Finset (Finset α)) :=
  if routes.isEmpty || routes.any (fun A => decide (A = ∅)) then none
  else some (incrementalBasis routes)

theorem operational_equivalence {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) :
    admitIncremental routes = admitBasis routes := by
  unfold admitIncremental admitBasis
  rw [incremental_eq_reference]

theorem singleton_basis_form {α : Type u} [DecidableEq α]
    (A S : Finset α) :
    S ∈ finiteBasis [A] ↔ ∃ x, x ∈ A ∧ S = {x} := by
  rw [mem_finite_basis]
  constructor
  · intro hm
    obtain ⟨x, hx, ha⟩ := hm.1 A (by simp)
    have hsub : ({x} : Finset α) ⊆ S := by
      intro y hy
      have he := Finset.mem_singleton.mp hy
      rw [he]
      exact hx
    have hcov : Covers [A] (fun y => y ∈ ({x} : Finset α)) := by
      intro B hb
      have he := List.mem_singleton.mp hb
      subst B
      exact ⟨x, Finset.mem_singleton.mpr rfl, ha⟩
    have hrev := hm.2 {x} hsub hcov
    exact ⟨x, ha, Finset.ext (fun y => ⟨fun hy => hrev hy, fun hy => hsub hy⟩)⟩
  · rintro ⟨x, hx, rfl⟩
    refine ⟨?_, ?_⟩
    · intro B hb
      have he := List.mem_singleton.mp hb
      subst B
      exact ⟨x, Finset.mem_singleton.mpr rfl, hx⟩
    · intro T ht hc
      obtain ⟨y, hy, _⟩ := hc A (by simp)
      have he := Finset.mem_singleton.mp (ht hy)
      intro z hz
      have hez := Finset.mem_singleton.mp hz
      rw [hez, ← he]
      exact hy

theorem pair_list_to_finset (x y : Nat) :
    (pairCut x y).toFinset = ({x, y} : Finset Nat) := by
  apply Finset.ext
  intro z
  have hl : z ∈ (pairCut x y).toFinset ↔ z = x ∨ z = y :=
    List.mem_toFinset.trans (mem_pair_cut x y z)
  have hr : z ∈ ({x, y} : Finset Nat) ↔ z = x ∨ z = y :=
    Finset.mem_insert.trans (or_congr Iff.rfl Finset.mem_singleton)
  exact hl.trans hr.symm

theorem one_list_reference (a : List Nat) :
    incrementalBasis [a.toFinset] = ((oneCuts a).map List.toFinset).toFinset := by
  apply Finset.ext
  intro S
  rw [incremental_eq_reference, singleton_basis_form]
  simp only [List.mem_toFinset, oneCuts, List.mem_map]
  constructor
  · rintro ⟨x, hx, rfl⟩
    exact ⟨[x], ⟨x, hx, rfl⟩, by simp⟩
  · rintro ⟨l, ⟨x, hx, rfl⟩, he⟩
    exact ⟨x, hx, by simpa using he.symm⟩

theorem two_list_reference (a b : List Nat) :
    incrementalBasis [a.toFinset, b.toFinset] = ((twoCuts a b).map List.toFinset).toFinset := by
  apply Finset.ext
  intro S
  rw [incremental_eq_reference, two_route_enumeration_exact]
  simp only [List.mem_toFinset, List.mem_map, twoCuts, List.mem_append,
    List.mem_filter, List.mem_flatMap, decide_eq_true_eq]
  constructor
  · rintro (⟨x, ha, hb, rfl⟩ | ⟨x, y, ha, hnb, hb, hna, rfl⟩)
    · exact ⟨[x], Or.inl ⟨x, ⟨ha, hb⟩, rfl⟩, by simp⟩
    · exact ⟨pairCut x y, Or.inr ⟨x, ⟨ha, hnb⟩, y, ⟨hb, hna⟩, rfl⟩,
        pair_list_to_finset x y⟩
  · rintro ⟨l, hl, he⟩
    rcases hl with ⟨x, ⟨ha, hb⟩, rfl⟩ | ⟨x, ⟨ha, hnb⟩, y, ⟨hb, hna⟩, rfl⟩
    · exact Or.inl ⟨x, ha, hb, by simpa using he.symm⟩
    · exact Or.inr ⟨x, y, ha, hnb, hb, hna, he.symm.trans (pair_list_to_finset x y)⟩

-- Executable observations, not proof oracles. The formal exactness above
-- connects the actual ledger to the independently certified R63 equations.
def stageCandidateCounts {α : Type u} [DecidableEq α] :
    List (Finset α) → List Nat
  | [] => []
  | A :: rest => (extendCuts A (incrementalBasis rest)).card :: stageCandidateCounts rest

theorem incremental_triangle :
    incrementalBasis routes3 = ({{0, 1}, {0, 2}, {1, 2}} : Finset (Finset Nat)) := by
  rw [incremental_eq_reference]
  exact triangle_basis_exact

theorem incremental_four_routes :
    incrementalBasis routes4 = ({{0}, {1, 2, 3, 4}} : Finset (Finset Nat)) := by
  rw [incremental_eq_reference]
  exact four_route_basis_exact

end KuuOSR65
