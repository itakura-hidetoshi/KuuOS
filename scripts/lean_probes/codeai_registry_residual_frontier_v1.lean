/- R78: residual candidates under append-only registry extension.
A missing binding may become supplied, or a route may become obstructed.
No previously impossible route becomes possible under a genuine extension.
Recompute the frontier over all retained route requirements, not just
the old frontier. No registration or execution authority follows. -/
namespace KuuOSR78
open KuuOSR69 KuuOSR72 KuuOSR73 KuuOSR75 KuuOSR76 KuuOSR77
universe u v w

theorem extension_empty_back {κ : Type v} {α : Type u}
    (reg next : κ → Option (Basis α)) (he : RegistryExtends reg next)
    (k : κ) (hn : next k = none) : reg k = none := by
  cases hr : reg k with
  | none => rfl
  | some F =>
    have impossible : (none : Option (Basis α)) = some F := hn.symm.trans (he k F hr)
    cases impossible

theorem minimal_batch_residual {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (req : List (κ × Basis α))
    (he : RegistryExtends reg next) (b : κ × Basis α) :
    b ∈ minimalBatch next req ↔ b ∈ minimalBatch reg req ∧ next b.1 = none := by
  simp only [minimal_batch_mem]
  constructor
  · rintro ⟨hm,hn⟩
    exact ⟨⟨hm,extension_empty_back reg next he b.1 hn⟩,hn⟩
  · rintro ⟨⟨hm,_⟩,hn⟩
    exact ⟨hm,hn⟩

theorem checked_plan_none_mono {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (req : List (κ × Basis α))
    (he : RegistryExtends reg next) (hp : checkedRecoveryPlan reg req = none) :
    checkedRecoveryPlan next req = none := by
  apply (checked_plan_none_iff_no_extension next req).mpr
  rintro ⟨last,h1,h2⟩
  exact ((checked_plan_none_iff_no_extension reg req).mp hp)
    ⟨last,extends_trans reg next last he h1,h2⟩

theorem checked_plan_residual {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (req oldPlan newPlan : List (κ × Basis α))
    (he : RegistryExtends reg next) (hp : checkedRecoveryPlan reg req = some oldPlan)
    (hn : checkedRecoveryPlan next req = some newPlan) (b : κ × Basis α) :
    b ∈ newPlan ↔ b ∈ oldPlan ∧ next b.1 = none := by
  have ho := ((checked_plan_some_iff reg req oldPlan).mp hp).2.2
  have hh := ((checked_plan_some_iff next req newPlan).mp hn).2.2
  rw [ho,hh]
  exact minimal_batch_residual reg next req he b

theorem checked_plan_ancestor {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (req newPlan : List (κ × Basis α))
    (he : RegistryExtends reg next) (hp : checkedRecoveryPlan next req = some newPlan) :
    ∃ oldPlan, checkedRecoveryPlan reg req = some oldPlan ∧
      ∀ b, b ∈ newPlan ↔ b ∈ oldPlan ∧ next b.1 = none := by
  cases hr : checkedRecoveryPlan reg req with
  | none =>
    have hn := checked_plan_none_mono reg next req he hr
    rw [hn] at hp
    cases hp
  | some bs =>
    exact ⟨bs,rfl,checked_plan_residual reg next req bs newPlan he hr hp⟩

theorem candidate_residual {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α)))
    (he : RegistryExtends reg next) (p : ι × List (κ × Basis α))
    (hp : p ∈ checkedCandidates next routes) :
    ∃ q ∈ checkedCandidates reg routes, q.1 = p.1 ∧
      ∀ b, b ∈ p.2 ↔ b ∈ q.2 ∧ next b.1 = none := by
  obtain ⟨r,hr,hid,hplan⟩ := (checked_candidates_mem_iff next routes p).mp hp
  obtain ⟨bs,hs,hres⟩ := checked_plan_ancestor reg next r.2 p.2 he hplan
  exact ⟨(r.1,bs),(checked_candidates_mem_iff reg routes (r.1,bs)).mpr
    ⟨r,hr,rfl,hs⟩,hid,hres⟩

theorem frontier_residual {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α)))
    (he : RegistryExtends reg next) (p : ι × List (κ × Basis α))
    (hp : p ∈ checkedFrontier next routes) :
    ∃ q ∈ checkedCandidates reg routes, q.1 = p.1 ∧
      ∀ b, b ∈ p.2 ↔ b ∈ q.2 ∧ next b.1 = none :=
  candidate_residual reg next routes he p (frontier_sound (checkedCandidates next routes) p hp)

theorem frontier_empty_mono {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α)))
    (he : RegistryExtends reg next) (hp : ¬ ∃ p, p ∈ checkedFrontier reg routes) :
    ¬ ∃ p, p ∈ checkedFrontier next routes := by
  apply (checked_frontier_empty_iff next routes).mpr
  intro r hr hx
  obtain ⟨last,h1,h2⟩ := hx
  exact ((checked_frontier_empty_iff reg routes).mp hp) r hr
    ⟨last,extends_trans reg next last he h1,h2⟩

theorem subset_residual {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α))
    (reqA reqB oldA oldB newA newB : List (κ × Basis α))
    (he : RegistryExtends reg next)
    (ha : checkedRecoveryPlan reg reqA = some oldA)
    (hb : checkedRecoveryPlan reg reqB = some oldB)
    (hna : checkedRecoveryPlan next reqA = some newA)
    (hnb : checkedRecoveryPlan next reqB = some newB)
    (hsub : ∀ b ∈ oldA, b ∈ oldB) : ∀ b ∈ newA, b ∈ newB := by
  intro b hm
  have h := (checked_plan_residual reg next reqA oldA newA he ha hna b).mp hm
  exact (checked_plan_residual reg next reqB oldB newB he hb hnb b).mpr ⟨hsub b h.1,h.2⟩

/- A concrete counterexample to pruning history: with two initially
recoverable routes, the dominated route becomes tied after a fresh binding.
Both routes must be considered again. -/
theorem old_frontier_not_sufficient :
    let e : Basis Nat := ∅
    let reg : Nat → Option (Basis Nat) := fun _ => none
    let next := setBinding reg 1 e
    let routes : List (Nat × List (Nat × Basis Nat)) := [(0,[(0,e),(1,e)]),(1,[(0,e)])]
    (checkedFrontier reg routes).map Prod.fst = [1] ∧
      (checkedFrontier next routes).map Prod.fst = [0,1] := by
  decide

end KuuOSR78
