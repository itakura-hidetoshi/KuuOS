/- R63 finite obstruction basis completeness. Appended to the exact R62 replay.
The basis concerns the supplied indexed family, not all possible proofs.
Empty operational inventories are HOLD; the general mathematical lemma also
allows an empty finite index type (whose transversal is vacuously empty). -/
namespace KuuOSR63
open KuuOSR62
universe u v

def Blocks {α : Type u} {ι : Type v} (deps : ι → α → Prop)
    (S : Finset α) : Prop :=
  ∀ i, Hits (fun x => x ∈ S) (deps i)

def MinimalFor {α : Type u} (P : Finset α → Prop) (S : Finset α) : Prop :=
  P S ∧ ∀ T : Finset α, T ⊆ S → P T → S ⊆ T

def MinimalCut {α : Type u} {ι : Type v} (deps : ι → α → Prop)
    (S : Finset α) : Prop := MinimalFor (Blocks deps) S

def MinimalBasis {α : Type u} {ι : Type v} (deps : ι → α → Prop)
    (C : α → Prop) : Prop :=
  ∃ S : Finset α, MinimalCut deps S ∧ ∀ x, C x ↔ x ∈ S

theorem exists_minimal_subset {α : Type u} (P : Finset α → Prop)
    (S : Finset α) (h : P S) :
    ∃ T : Finset α, T ⊆ S ∧ MinimalFor P T := by
  classical
  refine (Finset.strongInductionOn
    (p := fun Q : Finset α => P Q → ∃ T : Finset α, T ⊆ Q ∧ MinimalFor P T)
    S ?_) h
  intro Q ih hQ
  by_cases hm : ∀ T : Finset α, T ⊆ Q → P T → Q ⊆ T
  · exact ⟨Q, by intro x hx; exact hx, hQ, hm⟩
  · have hex : ∃ T : Finset α, T ⊆ Q ∧ P T ∧ ¬ Q ⊆ T := by
      by_contra hn
      apply hm
      intro T ht hT
      by_contra hqt
      exact hn ⟨T, ht, hT, hqt⟩
    obtain ⟨T, ht, hT, hnot⟩ := hex
    have hne : T ≠ Q := by
      intro he
      subst T
      apply hnot
      intro x hx
      exact hx
    obtain ⟨M, hmt, hmin⟩ := ih T
      (Finset.ssubset_iff_subset_ne.mpr ⟨ht, hne⟩) hT
    exact ⟨M, fun hx => ht (hmt hx), hmin⟩

-- Extract at most one witness per route, even for an infinite dependency type.
theorem finite_witness_cut {α : Type u} {ι : Type v} [Fintype ι]
    (deps : ι → α → Prop) (U : α → Prop) (h : ∀ i, Hits U (deps i)) :
    ∃ S : Finset α, Included (fun x => x ∈ S) U ∧
      Blocks deps S ∧ S.card ≤ Fintype.card ι := by
  classical
  let f : ι → α := fun i => Classical.choose (h i)
  have hf (i : ι) : U (f i) ∧ deps i (f i) := Classical.choose_spec (h i)
  refine ⟨Finset.univ.image f, ?_, ?_, ?_⟩
  · intro x hx
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hx
    exact (hf i).1
  · intro i
    exact ⟨f i, Finset.mem_image_of_mem f (Finset.mem_univ i), (hf i).2⟩
  · calc
      (Finset.univ.image f).card ≤ (Finset.univ : Finset ι).card := Finset.card_image_le
      _ = Fintype.card ι := Finset.card_univ

theorem exists_minimal_cut {α : Type u} {ι : Type v} [Fintype ι]
    (deps : ι → α → Prop) (U : α → Prop) (h : ∀ i, Hits U (deps i)) :
    ∃ S : Finset α, Included (fun x => x ∈ S) U ∧ MinimalCut deps S := by
  obtain ⟨S, hs, hb, _⟩ := finite_witness_cut deps U h
  obtain ⟨T, ht, hm⟩ := exists_minimal_subset (Blocks deps) S hb
  exact ⟨T, fun x hx => hs x (ht hx), hm⟩

theorem finite_basis_complete {α : Type u} {ι : Type v} [Fintype ι]
    (deps : ι → α → Prop) (U : α → Prop) :
    (∀ i, Hits U (deps i)) ↔ ∃ C, MinimalBasis deps C ∧ Included C U := by
  constructor
  · intro h
    obtain ⟨S, hs, hm⟩ := exists_minimal_cut deps U h
    exact ⟨fun x => x ∈ S, ⟨S, hm, fun _ => Iff.rfl⟩, hs⟩
  · rintro ⟨C, ⟨S, hm, he⟩, hsub⟩ i
    obtain ⟨x, hx, hd⟩ := hm.1 i
    exact ⟨x, hsub x ((he x).mpr hx), hd⟩

theorem minimal_cut_card_le {α : Type u} {ι : Type v} [Fintype ι]
    (deps : ι → α → Prop) (S : Finset α) (hm : MinimalCut deps S) :
    S.card ≤ Fintype.card ι := by
  obtain ⟨T, ht, hb, hcard⟩ := finite_witness_cut deps (fun x => x ∈ S) hm.1
  have hts : T ⊆ S := by
    intro x hx
    exact ht x hx
  exact (Finset.card_le_card (hm.2 T hts hb)).trans hcard

theorem finite_recovery_duality {α : Type u} {ι : Type v} [Fintype ι]
    (deps : ι → α → Prop) (D R : α → Prop) :
    (∃ i, Eligible (Residual D R) (deps i)) ↔
      ∀ C, MinimalBasis deps C → Included C D → Hits R C :=
  family_recovery_iff_break_complete_basis deps (MinimalBasis deps) D R
    (finite_basis_complete deps)

-- Exact characterization of the inclusion-minimal two-route cuts.
theorem two_minimal_form {α : Type u} [DecidableEq α]
    (A B : α → Prop) (S : Finset α) :
    MinimalFor (fun C => Hits (fun x => x ∈ C) A ∧ Hits (fun x => x ∈ C) B) S ↔
      (∃ x, A x ∧ B x ∧ S = {x}) ∨
      (∃ x y, A x ∧ ¬ B x ∧ B y ∧ ¬ A y ∧ S = {x, y}) := by
  constructor
  · rintro ⟨hb, hm⟩
    rcases (two_blocked_iff_basis (fun x => x ∈ S) A B).mp hb with
      ⟨x, hx, ha, hB⟩ | ⟨x, y, hx, ha, hnb, hy, hB, hna⟩
    · have hs : ({x} : Finset α) ⊆ S := by
        intro z hz
        rw [Finset.mem_singleton] at hz
        subst z
        exact hx
      have hr := hm {x} hs ⟨⟨x, by simp, ha⟩, ⟨x, by simp, hB⟩⟩
      exact Or.inl ⟨x, ha, hB, Finset.ext (fun z => ⟨fun hz => hr hz, fun hz => hs hz⟩)⟩
    · have hs : ({x, y} : Finset α) ⊆ S := by
        intro z hz
        rcases Finset.mem_insert.mp hz with h | h
        · subst z
          exact hx
        · rw [Finset.mem_singleton] at h
          subst z
          exact hy
      have hr := hm {x, y} hs ⟨⟨x, by simp, ha⟩, ⟨y, by simp, hB⟩⟩
      exact Or.inr ⟨x, y, ha, hnb, hB, hna,
        Finset.ext (fun z => ⟨fun hz => hr hz, fun hz => hs hz⟩)⟩
  · rintro (⟨x, ha, hb, rfl⟩ | ⟨x, y, ha, hnb, hb, hna, rfl⟩)
    · refine ⟨⟨⟨x, by simp, ha⟩, ⟨x, by simp, hb⟩⟩, ?_⟩
      rintro T hs ⟨⟨z, hz, _⟩, _⟩ w hw
      have hzx := Finset.mem_singleton.mp (hs hz)
      have hwx := Finset.mem_singleton.mp hw
      rw [hwx, ← hzx]
      exact hz
    · refine ⟨⟨⟨x, by simp, ha⟩, ⟨y, by simp, hb⟩⟩, ?_⟩
      rintro T hs ⟨⟨a, hat, haa⟩, ⟨b, hbt, hbb⟩⟩ z hz
      have hax : a = x := by
        rcases Finset.mem_insert.mp (hs hat) with h | h
        · exact h
        · have he := Finset.mem_singleton.mp h
          exact False.elim (hna (he ▸ haa))
      have hby : b = y := by
        rcases Finset.mem_insert.mp (hs hbt) with h | h
        · exact False.elim (hnb (h ▸ hbb))
        · exact Finset.mem_singleton.mp h
      rcases Finset.mem_insert.mp hz with h | h
      · rw [h, ← hax]
        exact hat
      · rw [Finset.mem_singleton.mp h, ← hby]
        exact hbt

-- Computable list representation for the actual R60 ledger. Natural
-- identifiers are a bijective encoding of the recorded dependency strings.
def pairCut (x y : Nat) : List Nat := if x ≤ y then [x, y] else [y, x]
def oneCuts (a : List Nat) : List (List Nat) := a.map (fun x => [x])
def twoCuts (a b : List Nat) : List (List Nat) :=
  (a.filter (fun x => decide (x ∈ b))).map (fun x => [x]) ++
    (a.filter (fun x => decide (x ∉ b))).flatMap
      (fun x => (b.filter (fun y => decide (y ∉ a))).map (pairCut x))

def ListedBasis (cuts : List (List Nat)) (C : Nat → Prop) : Prop :=
  ∃ l ∈ cuts, ∀ x, C x ↔ x ∈ l

theorem mem_pair_cut (x y z : Nat) : z ∈ pairCut x y ↔ z = x ∨ z = y := by
  by_cases h : x ≤ y
  · simp [pairCut, h]
  · simp [pairCut, h, or_comm]

theorem listed_iff (cuts : List (List Nat)) (U : Nat → Prop) :
    (∃ C, ListedBasis cuts C ∧ Included C U) ↔
      ∃ l ∈ cuts, ∀ x ∈ l, U x := by
  constructor
  · rintro ⟨C, ⟨l, hl, he⟩, hs⟩
    exact ⟨l, hl, fun x hx => hs x ((he x).mpr hx)⟩
  · rintro ⟨l, hl, hs⟩
    exact ⟨fun x => x ∈ l, ⟨l, hl, fun _ => Iff.rfl⟩, hs⟩

theorem one_cuts_complete (a : List Nat) (U : Nat → Prop) :
    Hits U (fun x => x ∈ a) ↔ ∃ C, ListedBasis (oneCuts a) C ∧ Included C U := by
  rw [listed_iff]
  constructor
  · rintro ⟨x, hu, ha⟩
    refine ⟨[x], List.mem_map.mpr ⟨x, ha, rfl⟩, ?_⟩
    intro y hy
    have he : y = x := by simpa using hy
    rw [he]
    exact hu
  · rintro ⟨l, hl, hu⟩
    obtain ⟨x, hx, rfl⟩ := List.mem_map.mp hl
    exact ⟨x, hu x (by simp), hx⟩

theorem two_cuts_complete (a b : List Nat) (U : Nat → Prop) :
    (Hits U (fun x => x ∈ a) ∧ Hits U (fun x => x ∈ b)) ↔
      ∃ C, ListedBasis (twoCuts a b) C ∧ Included C U := by
  rw [listed_iff, two_blocked_iff_basis]
  constructor
  · rintro (⟨x, hu, ha, hb⟩ | ⟨x, y, hux, ha, hnb, huy, hb, hna⟩)
    · refine ⟨[x], ?_, ?_⟩
      · simp only [twoCuts, List.mem_append, List.mem_map, List.mem_filter,
          List.mem_flatMap, decide_eq_true_eq]
        exact Or.inl ⟨x, ⟨ha, hb⟩, rfl⟩
      · intro z hz
        have he : z = x := by simpa using hz
        rw [he]
        exact hu
    · refine ⟨pairCut x y, ?_, ?_⟩
      · simp only [twoCuts, List.mem_append, List.mem_map, List.mem_filter,
          List.mem_flatMap, decide_eq_true_eq]
        exact Or.inr ⟨x, ⟨ha, hnb⟩, y, ⟨hb, hna⟩, rfl⟩
      · intro z hz
        rcases (mem_pair_cut x y z).mp hz with h | h
        · rw [h]; exact hux
        · rw [h]; exact huy
  · rintro ⟨l, hl, hu⟩
    simp only [twoCuts, List.mem_append, List.mem_map, List.mem_filter,
      List.mem_flatMap, decide_eq_true_eq] at hl
    rcases hl with ⟨x, ⟨ha, hb⟩, rfl⟩ | ⟨x, ⟨ha, hnb⟩, y, ⟨hb, hna⟩, rfl⟩
    · exact Or.inl ⟨x, hu x (by simp), ha, hb⟩
    · exact Or.inr ⟨x, y, hu x ((mem_pair_cut x y x).mpr (Or.inl rfl)), ha, hnb,
        hu y ((mem_pair_cut x y y).mpr (Or.inr rfl)), hb, hna⟩

def SingleDeps (a : List Nat) (_ : Unit) (x : Nat) : Prop := x ∈ a
def DoubleDeps (a b : List Nat) (i : Bool) (x : Nat) : Prop :=
  if i then x ∈ b else x ∈ a

theorem single_family_basis (a : List Nat) (U : Nat → Prop) :
    (∀ i, Hits U (SingleDeps a i)) ↔
      ∃ C, ListedBasis (oneCuts a) C ∧ Included C U := by
  refine Iff.trans ?_ (one_cuts_complete a U)
  exact ⟨fun h => h (), fun h i => by cases i; exact h⟩

theorem double_family_basis (a b : List Nat) (U : Nat → Prop) :
    (∀ i, Hits U (DoubleDeps a b i)) ↔
      ∃ C, ListedBasis (twoCuts a b) C ∧ Included C U := by
  refine Iff.trans ?_ (two_cuts_complete a b U)
  constructor
  · intro h
    exact ⟨h false, h true⟩
  · rintro ⟨ha, hb⟩ i
    cases i
    · exact ha
    · exact hb

end KuuOSR63
