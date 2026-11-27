/- R64: executable finite witness-product enumerator with certified reduction.
The list is the supplied route inventory, not an exhaustive repository search.
The mathematical empty-family case is distinguished from operational HOLD. -/
namespace KuuOSR64
open KuuOSR62 KuuOSR63
universe u

def Covers {α : Type u} (routes : List (Finset α)) (U : α → Prop) : Prop :=
  ∀ A ∈ routes, Hits U (fun x => x ∈ A)

def witnessCuts {α : Type u} [DecidableEq α] :
    List (Finset α) → Finset (Finset α)
  | [] => {∅}
  | A :: rest => (witnessCuts rest).biUnion (fun S => A.image (fun x => insert x S))

def reduceCuts {α : Type u} [DecidableEq α]
    (F : Finset (Finset α)) : Finset (Finset α) :=
  F.filter (fun S => ∀ T ∈ F, T ⊆ S → S ⊆ T)

def finiteBasis {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) : Finset (Finset α) :=
  reduceCuts (witnessCuts routes)

theorem witness_sound {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) (S : Finset α) (hs : S ∈ witnessCuts routes) :
    Covers routes (fun x => x ∈ S) := by
  induction routes generalizing S with
  | nil =>
      intro A hA
      simp at hA
  | cons A rest ih =>
      simp only [witnessCuts] at hs
      obtain ⟨T, ht, himage⟩ := Finset.mem_biUnion.mp hs
      obtain ⟨x, hx, hEq⟩ := Finset.mem_image.mp himage
      subst S
      intro B hB
      rcases List.mem_cons.mp hB with he | hr
      · subst B
        exact ⟨x, Finset.mem_insert_self x T, hx⟩
      · obtain ⟨y, hy, hBy⟩ := ih T ht B hr
        exact ⟨y, Finset.mem_insert_of_mem hy, hBy⟩

theorem witness_complete {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) (U : α → Prop) (h : Covers routes U) :
    ∃ S ∈ witnessCuts routes, Included (fun x => x ∈ S) U := by
  induction routes with
  | nil =>
      refine ⟨∅, ?_, ?_⟩
      · simp [witnessCuts]
      · intro x hx
        simp at hx
  | cons A rest ih =>
      have ha : Hits U (fun x => x ∈ A) := h A (by simp)
      obtain ⟨x, hu, hx⟩ := ha
      have hr : Covers rest U := fun B hb => h B (List.mem_cons_of_mem A hb)
      obtain ⟨T, ht, htu⟩ := ih hr
      refine ⟨insert x T, ?_, ?_⟩
      · apply Finset.mem_biUnion.mpr
        exact ⟨T, ht, Finset.mem_image.mpr ⟨x, hx, rfl⟩⟩
      · intro y hy
        rcases Finset.mem_insert.mp hy with he | hm
        · rw [he]
          exact hu
        · exact htu y hm

theorem witness_card_le {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) (S : Finset α) (hs : S ∈ witnessCuts routes) :
    S.card ≤ routes.length := by
  induction routes generalizing S with
  | nil =>
      have he : S = ∅ := Finset.mem_singleton.mp hs
      subst S
      simp
  | cons A rest ih =>
      simp only [witnessCuts] at hs
      obtain ⟨T, ht, himage⟩ := Finset.mem_biUnion.mp hs
      obtain ⟨x, _, he⟩ := Finset.mem_image.mp himage
      subst S
      exact (Finset.card_insert_le x T).trans (Nat.add_le_add_right (ih T ht) 1)

theorem mem_reduced_iff {α : Type u} [DecidableEq α]
    (F : Finset (Finset α)) (S : Finset α) :
    S ∈ reduceCuts F ↔ S ∈ F ∧ ∀ T ∈ F, T ⊆ S → S ⊆ T := by
  exact Finset.mem_filter

theorem mem_finite_basis {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) (S : Finset α) :
    S ∈ finiteBasis routes ↔ MinimalFor (fun T => Covers routes (fun x => x ∈ T)) S := by
  rw [finiteBasis, mem_reduced_iff]
  constructor
  · rintro ⟨hs, hm⟩
    refine ⟨witness_sound routes S hs, ?_⟩
    intro T hTS hT
    obtain ⟨C, hc, hct⟩ := witness_complete routes (fun x => x ∈ T) hT
    have hCS : C ⊆ S := by
      intro x hx
      exact hTS (hct x hx)
    have hSC := hm C hc hCS
    intro x hx
    exact hct x (hSC hx)
  · intro hm
    obtain ⟨C, hc, hcs⟩ := witness_complete routes (fun x => x ∈ S) hm.1
    have hCS : C ⊆ S := by
      intro x hx
      exact hcs x hx
    have hSC := hm.2 C hCS (witness_sound routes C hc)
    have he : C = S := Finset.ext (fun x => ⟨fun hx => hCS hx, fun hx => hSC hx⟩)
    subst C
    exact ⟨hc, fun T hT hTS => hm.2 T hTS (witness_sound routes T hT)⟩

theorem enumerator_complete {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) (U : α → Prop) :
    Covers routes U ↔ ∃ S ∈ finiteBasis routes, Included (fun x => x ∈ S) U := by
  constructor
  · intro h
    obtain ⟨T, ht, htu⟩ := witness_complete routes U h
    obtain ⟨S, hs, hm⟩ := exists_minimal_subset
      (fun C => Covers routes (fun x => x ∈ C)) T (witness_sound routes T ht)
    exact ⟨S, (mem_finite_basis routes S).mpr hm, fun x hx => htu x (hs hx)⟩
  · rintro ⟨S, hs, hsu⟩ A hA
    have hm := (mem_finite_basis routes S).mp hs
    obtain ⟨x, hx, ha⟩ := hm.1 A hA
    exact ⟨x, hsu x hx, ha⟩

theorem basis_antichain {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) (S T : Finset α)
    (hs : S ∈ finiteBasis routes) (ht : T ∈ finiteBasis routes) (hst : S ⊆ T) :
    S = T := by
  have hS := (mem_finite_basis routes S).mp hs
  have hT := (mem_finite_basis routes T).mp ht
  have hts := hT.2 S hst hS.1
  exact Finset.ext (fun x => ⟨fun hx => hst hx, fun hx => hts hx⟩)

theorem enumerated_cut_card_le {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) (S : Finset α) (hs : S ∈ finiteBasis routes) :
    S.card ≤ routes.length := by
  have hw := ((mem_reduced_iff (witnessCuts routes) S).mp hs).1
  exact witness_card_le routes S hw

-- Each member of a minimal cut has a route it alone blocks.
theorem private_route_witness {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) (S : Finset α) (hs : S ∈ finiteBasis routes)
    (x : α) (hx : x ∈ S) :
    ∃ A ∈ routes, x ∈ A ∧ ∀ y ∈ S, y ∈ A → y = x := by
  classical
  have hm := (mem_finite_basis routes S).mp hs
  have hno : ¬ Covers routes (fun y => y ∈ S.erase x) := by
    intro h
    have hsub := hm.2 (S.erase x) (Finset.erase_subset x S) h
    exact Finset.notMem_erase x S (hsub hx)
  have hex : ∃ A ∈ routes, ¬ Hits (fun y => y ∈ S.erase x) (fun y => y ∈ A) := by
    by_contra hn
    apply hno
    intro A ha
    by_contra hA
    exact hn ⟨A, ha, hA⟩
  obtain ⟨A, ha, hA⟩ := hex
  obtain ⟨z, hz, hza⟩ := hm.1 A ha
  have he : z = x := by
    by_contra hne
    exact hA ⟨z, Finset.mem_erase.mpr ⟨hne, hz⟩, hza⟩
  refine ⟨A, ha, ?_, ?_⟩
  · rw [← he]
    exact hza
  · intro y hy hya
    by_contra hne
    exact hA ⟨y, Finset.mem_erase.mpr ⟨hne, hy⟩, hya⟩

def EnumeratedBasis {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) (C : α → Prop) : Prop :=
  ∃ S ∈ finiteBasis routes, ∀ x, C x ↔ x ∈ S

def routeDeps {α : Type u} (routes : List (Finset α))
    (i : {A : Finset α // A ∈ routes}) (x : α) : Prop := x ∈ i.val

theorem complete_certificate {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) (U : α → Prop) :
    (∀ i, Hits U (routeDeps routes i)) ↔
      ∃ C, EnumeratedBasis routes C ∧ Included C U := by
  constructor
  · intro h
    have hc : Covers routes U := fun A ha => h ⟨A, ha⟩
    obtain ⟨S, hs, hsu⟩ := (enumerator_complete routes U).mp hc
    exact ⟨fun x => x ∈ S, ⟨S, hs, fun _ => Iff.rfl⟩, hsu⟩
  · rintro ⟨C, ⟨S, hs, he⟩, hcu⟩ i
    have hm := (mem_finite_basis routes S).mp hs
    obtain ⟨x, hx, ha⟩ := hm.1 i.val i.property
    exact ⟨x, hcu x ((he x).mpr hx), ha⟩

theorem enumerated_recovery_duality {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) (D R : α → Prop) :
    (∃ i, Eligible (Residual D R) (routeDeps routes i)) ↔
      ∀ C, EnumeratedBasis routes C → Included C D → Hits R C :=
  family_recovery_iff_break_complete_basis (routeDeps routes)
    (EnumeratedBasis routes) D R (complete_certificate routes)

-- Exact specialization to the already certified two-route classification.
theorem two_route_enumeration_exact {α : Type u} [DecidableEq α]
    (A B S : Finset α) :
    S ∈ finiteBasis [A, B] ↔
      (∃ x, x ∈ A ∧ x ∈ B ∧ S = {x}) ∨
      (∃ x y, x ∈ A ∧ x ∉ B ∧ y ∈ B ∧ y ∉ A ∧ S = {x, y}) := by
  have he : (fun C : Finset α => Covers [A, B] (fun x => x ∈ C)) =
      (fun C : Finset α => Hits (fun x => x ∈ C) (fun x => x ∈ A) ∧
        Hits (fun x => x ∈ C) (fun x => x ∈ B)) := by
    funext C
    apply propext
    constructor
    · intro h
      exact ⟨h A (by simp), h B (by simp)⟩
    · rintro ⟨ha, hb⟩ X hX
      simp only [List.mem_cons, List.mem_singleton] at hX
      rcases hX with h | h
      · subst X
        exact ha
      · subst X
        exact hb
  rw [mem_finite_basis, he]
  exact two_minimal_form (fun x => x ∈ A) (fun x => x ∈ B) S

def admitBasis {α : Type u} [DecidableEq α]
    (routes : List (Finset α)) : Option (Finset (Finset α)) :=
  if routes.isEmpty || routes.any (fun A => decide (A = ∅)) then none
  else some (finiteBasis routes)

theorem operational_empty_routes_hold {α : Type u} [DecidableEq α] :
    admitBasis ([] : List (Finset α)) = none := rfl

theorem operational_empty_dependency_hold {α : Type u} [DecidableEq α]
    (rest : List (Finset α)) : admitBasis ((∅ : Finset α) :: rest) = none := by
  simp [admitBasis]

-- Closed executable tests, without native_decide or untrusted oracle axioms.
def routes3 : List (Finset Nat) := [{0, 1}, {1, 2}, {0, 2}]
def routes4 : List (Finset Nat) := [{0, 1}, {0, 2}, {0, 3}, {0, 4}]

theorem triangle_basis_exact :
    finiteBasis routes3 = ({{0, 1}, {0, 2}, {1, 2}} : Finset (Finset Nat)) := by decide

theorem four_route_basis_exact :
    finiteBasis routes4 = ({{0}, {1, 2, 3, 4}} : Finset (Finset Nat)) := by decide

theorem empty_math_family :
    finiteBasis ([] : List (Finset Nat)) = ({∅} : Finset (Finset Nat)) := by decide

theorem empty_math_dependency :
    finiteBasis ([∅] : List (Finset Nat)) = ∅ := by decide

end KuuOSR64
