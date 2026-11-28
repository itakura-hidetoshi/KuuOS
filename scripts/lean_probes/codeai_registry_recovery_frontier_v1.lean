/- R77: finite recovery frontier. Strict binding-set containment is not
path equivalence. Equal binding sets retain distinct route identifiers.
The result confers neither registration nor execution authority. -/
namespace KuuOSR77
open KuuOSR69 KuuOSR70 KuuOSR71 KuuOSR73 KuuOSR75 KuuOSR76
universe u v w

def frontier {ι : Type w} {β : Type u} [DecidableEq β]
    (xs : List (ι × List β)) : List (ι × List β) :=
  xs.filter (fun p => xs.all (fun q => decide (¬ q.2.toFinset < p.2.toFinset)))

theorem frontier_mem_iff {ι : Type w} {β : Type u} [DecidableEq β]
    (xs : List (ι × List β)) (p : ι × List β) :
    p ∈ frontier xs ↔ p ∈ xs ∧ ∀ q ∈ xs, ¬ q.2.toFinset < p.2.toFinset := by
  simp only [frontier, List.mem_filter, List.all_eq_true, decide_eq_true_eq]

theorem frontier_sound {ι : Type w} {β : Type u} [DecidableEq β]
    (xs : List (ι × List β)) (p : ι × List β) (hp : p ∈ frontier xs) :
    p ∈ xs :=
  ((frontier_mem_iff xs p).mp hp).1

theorem frontier_equal_survives {ι : Type w} {β : Type u} [DecidableEq β]
    (xs : List (ι × List β)) (p q : ι × List β)
    (hp : p ∈ xs) (hq : q ∈ frontier xs)
    (he : p.2.toFinset = q.2.toFinset) : p ∈ frontier xs := by
  refine (frontier_mem_iff xs p).mpr ⟨hp, ?_⟩
  intro r hr
  rw [he]
  exact ((frontier_mem_iff xs q).mp hq).2 r hr

theorem frontier_covers {ι : Type w} {β : Type u} [DecidableEq β]
    (xs : List (ι × List β)) (p : ι × List β) (hp : p ∈ xs) :
    ∃ q ∈ frontier xs, q.2.toFinset ⊆ p.2.toFinset := by
  classical
  let P : Nat → Prop := fun n =>
    ∃ q ∈ xs, q.2.toFinset ⊆ p.2.toFinset ∧ q.2.toFinset.card = n
  have hex : ∃ n, P n :=
    ⟨p.2.toFinset.card, p, hp, (fun _ h => h), rfl⟩
  obtain ⟨q, hq, hsub, hcard⟩ := Nat.find_spec hex
  refine ⟨q, (frontier_mem_iff xs q).mpr ⟨hq, ?_⟩, hsub⟩
  intro r hr hlt
  have hrs : r.2.toFinset ⊆ p.2.toFinset :=
    fun x hx => hsub ((le_of_lt hlt) hx)
  have hmin : Nat.find hex ≤ r.2.toFinset.card :=
    Nat.find_min' hex ⟨r, hr, hrs, rfl⟩
  have hless : r.2.toFinset.card < Nat.find hex := by
    rw [← hcard]
    exact Finset.card_lt_card hlt
  exact (Nat.not_lt_of_ge hmin) hless

theorem frontier_antichain {ι : Type w} {β : Type u} [DecidableEq β]
    (xs : List (ι × List β)) (p q : ι × List β)
    (hp : p ∈ frontier xs) (hq : q ∈ frontier xs) :
    ¬ q.2.toFinset < p.2.toFinset :=
  ((frontier_mem_iff xs p).mp hp).2 q (frontier_sound xs q hq)

theorem frontier_exists_iff {ι : Type w} {β : Type u} [DecidableEq β]
    (xs : List (ι × List β)) :
    (∃ p, p ∈ frontier xs) ↔ ∃ p, p ∈ xs := by
  constructor
  · rintro ⟨p, hp⟩
    exact ⟨p, frontier_sound xs p hp⟩
  · rintro ⟨p, hp⟩
    obtain ⟨q, hq, _⟩ := frontier_covers xs p hp
    exact ⟨q, hq⟩

def checkedCandidates {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α))) :
    List (ι × List (κ × Basis α)) :=
  routes.filterMap (fun r => (checkedRecoveryPlan reg r.2).map (fun bs => (r.1, bs)))

theorem checked_candidates_mem_iff {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α)))
    (p : ι × List (κ × Basis α)) :
    p ∈ checkedCandidates reg routes ↔
      ∃ r ∈ routes, r.1 = p.1 ∧ checkedRecoveryPlan reg r.2 = some p.2 := by
  rcases p with ⟨i,bs⟩
  simp only [checkedCandidates, List.mem_filterMap]
  constructor
  · rintro ⟨⟨j,req⟩,hj,he⟩
    cases h : checkedRecoveryPlan reg req with
    | none => simp [h] at he
    | some xs =>
      have hp : (j,xs) = (i,bs) := by simpa [h] using he
      have h1 : j = i := congrArg Prod.fst hp
      have h2 : xs = bs := congrArg Prod.snd hp
      exact ⟨(j,req),hj,h1,h.trans (congrArg some h2)⟩
  · rintro ⟨⟨j,req⟩,hj,hid,hplan⟩
    exact ⟨(j,req),hj,by simp [hplan,hid]⟩

def checkedFrontier {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α))) :
    List (ι × List (κ × Basis α)) :=
  frontier (checkedCandidates reg routes)

theorem checked_frontier_admits {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α)))
    (p : ι × List (κ × Basis α)) (hp : p ∈ checkedFrontier reg routes) :
    ∃ r ∈ routes, r.1 = p.1 ∧
      ∃ next, checkedBatch reg p.2 = some next ∧ CoversBindings next r.2 := by
  have hm := frontier_sound (checkedCandidates reg routes) p hp
  obtain ⟨r,hr,hid,hplan⟩ := (checked_candidates_mem_iff reg routes p).mp hm
  exact ⟨r,hr,hid,checked_plan_admits reg r.2 p.2 hplan⟩

theorem checked_frontier_covers {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α)))
    (p : ι × List (κ × Basis α)) (hp : p ∈ checkedCandidates reg routes) :
    ∃ q ∈ checkedFrontier reg routes, q.2.toFinset ⊆ p.2.toFinset :=
  frontier_covers (checkedCandidates reg routes) p hp

theorem checked_frontier_empty_iff {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α))) :
    (¬ ∃ p, p ∈ checkedFrontier reg routes) ↔
      ∀ r ∈ routes, ¬ ∃ next, RegistryExtends reg next ∧ CoversBindings next r.2 := by
  constructor
  · intro h r hr hx
    obtain ⟨bs,hbs⟩ := (checked_plan_exists_iff_extension reg r.2).mpr hx
    have hp : (r.1,bs) ∈ checkedCandidates reg routes :=
      (checked_candidates_mem_iff reg routes (r.1,bs)).mpr ⟨r,hr,rfl,hbs⟩
    obtain ⟨q,hq,_⟩ := checked_frontier_covers reg routes (r.1,bs) hp
    exact h ⟨q,hq⟩
  · intro h
    rintro ⟨p,hp⟩
    obtain ⟨r,hr,_,next,hb,hc⟩ := checked_frontier_admits reg routes p hp
    exact h r hr ⟨next,checked_batch_extends reg next p.2 hb,hc⟩

end KuuOSR77
