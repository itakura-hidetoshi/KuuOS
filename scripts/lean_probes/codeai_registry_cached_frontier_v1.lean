/- R79: refresh a complete cached route-plan inventory by inspecting only
previously missing bindings. None is preserved under a genuine extension.
The exact comparison is in binding-set representation, not ordered binding
list representation. The old route order, IDs and None rows are retained.
No live registration, proof-search completeness, or action authority. -/
namespace KuuOSR79
open KuuOSR69 KuuOSR72 KuuOSR75 KuuOSR76 KuuOSR77 KuuOSR78
universe u v w

def refreshPlan {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (next : κ → Option (Basis α)) (oldPlan : Option (List (κ × Basis α))) :
    Option (Finset (κ × Basis α)) :=
  match oldPlan with
  | none => none
  | some bs =>
    if compatibilityCheck next bs = true then
      some (bs.toFinset.filter (fun b => next b.1 = none))
    else none

theorem cached_compatibility_iff {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (req bs : List (κ × Basis α))
    (he : RegistryExtends reg next) (hp : checkedRecoveryPlan reg req = some bs) :
    Compatible next bs ↔ Compatible next req := by
  obtain ⟨hc,_,hb⟩ := (checked_plan_some_iff reg req bs).mp hp
  constructor
  · intro h b hm
    rcases hc b hm with hn | hs
    · apply h b
      rw [hb]
      exact (minimal_batch_mem reg req b).mpr ⟨hm,hn⟩
    · exact Or.inr (he b.1 b.2 hs)
  · intro h b hm
    apply h b
    rw [hb] at hm
    exact ((minimal_batch_mem reg req b).mp hm).1

theorem refresh_none {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α] (next : κ → Option (Basis α)) :
    refreshPlan next none = none := rfl

theorem refresh_plan_exact {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (req : List (κ × Basis α))
    (he : RegistryExtends reg next) :
    refreshPlan next (checkedRecoveryPlan reg req) =
      (checkedRecoveryPlan next req).map List.toFinset := by
  cases ho : checkedRecoveryPlan reg req with
  | none =>
    have hn := checked_plan_none_mono reg next req he ho
    exact (congrArg (fun p : Option (List (κ × Basis α)) => p.map List.toFinset) hn).symm
  | some bs =>
    have hcons := ((checked_plan_some_iff reg req bs).mp ho).2.1
    by_cases hc : compatibilityCheck next bs = true
    · have hcomp := (cached_compatibility_iff reg next req bs he ho).mp
        ((compatibility_check_iff next bs).mp hc)
      have hn : checkedRecoveryPlan next req = some (minimalBatch next req) :=
        (checked_plan_some_iff next req (minimalBatch next req)).mpr ⟨hcomp,hcons,rfl⟩
      have hs : bs.toFinset.filter (fun b => next b.1 = none) =
          (minimalBatch next req).toFinset := by
        ext b
        simp only [Finset.mem_filter, List.mem_toFinset]
        exact (checked_plan_residual reg next req bs (minimalBatch next req) he ho hn b).symm
      simp [refreshPlan,hc,hn,hs]
    · have hnc : ¬ Compatible next req := fun h =>
        hc ((compatibility_check_iff next bs).mpr
          ((cached_compatibility_iff reg next req bs he ho).mpr h))
      have hn : checkedRecoveryPlan next req = none := by
        cases hp : checkedRecoveryPlan next req with
        | none => rfl
        | some bp => exact False.elim (hnc ((checked_plan_some_iff next req bp).mp hp).1)
      simp [refreshPlan,hc,hn]

def cacheRoutes {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α))) :
    List (ι × Option (List (κ × Basis α))) :=
  routes.map (fun r => (r.1, checkedRecoveryPlan reg r.2))

def setRoutePlans {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α))) :
    List (ι × Option (Finset (κ × Basis α))) :=
  routes.map (fun r => (r.1, (checkedRecoveryPlan reg r.2).map List.toFinset))

def refreshCached {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (next : κ → Option (Basis α)) (cache : List (ι × Option (List (κ × Basis α)))) :
    List (ι × Option (Finset (κ × Basis α))) :=
  cache.map (fun r => (r.1, refreshPlan next r.2))

theorem refresh_cache_exact {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α)))
    (he : RegistryExtends reg next) :
    refreshCached next (cacheRoutes reg routes) = setRoutePlans next routes := by
  induction routes with
  | nil => rfl
  | cons r rs ih =>
    change (r.1, refreshPlan next (checkedRecoveryPlan reg r.2)) ::
      refreshCached next (cacheRoutes reg rs) =
      (r.1, (checkedRecoveryPlan next r.2).map List.toFinset) ::
      setRoutePlans next rs
    rw [refresh_plan_exact reg next r.2 he, ih]

def presentPlans {ι : Type w} {β : Type u}
    (rows : List (ι × Option (Finset β))) : List (ι × Finset β) :=
  rows.filterMap (fun p => p.2.map (fun s => (p.1,s)))

def setFrontier {ι : Type w} {β : Type u} [DecidableEq β]
    (xs : List (ι × Finset β)) : List (ι × Finset β) :=
  xs.filter (fun p => xs.all (fun q => decide (¬ q.2 < p.2)))

theorem set_frontier_mem_iff {ι : Type w} {β : Type u} [DecidableEq β]
    (xs : List (ι × Finset β)) (p : ι × Finset β) :
    p ∈ setFrontier xs ↔ p ∈ xs ∧ ∀ q ∈ xs, ¬ q.2 < p.2 := by
  simp only [setFrontier, List.mem_filter, List.all_eq_true, decide_eq_true_eq]

def refreshFrontier {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (next : κ → Option (Basis α)) (cache : List (ι × Option (List (κ × Basis α)))) :
    List (ι × Finset (κ × Basis α)) :=
  setFrontier (presentPlans (refreshCached next cache))

def freshSetFrontier {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α))) :
    List (ι × Finset (κ × Basis α)) :=
  setFrontier (presentPlans (setRoutePlans reg routes))

theorem refresh_frontier_exact {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α)))
    (he : RegistryExtends reg next) :
    refreshFrontier next (cacheRoutes reg routes) = freshSetFrontier next routes :=
  congrArg (fun xs => setFrontier (presentPlans xs))
    (refresh_cache_exact reg next routes he)

end KuuOSR79
