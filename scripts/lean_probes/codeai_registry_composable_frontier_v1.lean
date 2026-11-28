/- R80: closed set-cache refresh and composition under registry extensions.
All rows (including none), route order, and IDs remain in the cache.
No list order of bindings, arbitrary-cache correctness, or live authority. -/
namespace KuuOSR80
open KuuOSR69 KuuOSR72 KuuOSR76 KuuOSR77 KuuOSR79
universe u v w

def SetCompatible {κ : Type v} {α : Type u}
    (next : κ → Option (Basis α)) (bs : Finset (κ × Basis α)) : Prop :=
  ∀ b ∈ bs, next b.1 = none ∨ next b.1 = some b.2

def refreshSetPlan {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (next : κ → Option (Basis α)) (oldPlan : Option (Finset (κ × Basis α))) :
    Option (Finset (κ × Basis α)) :=
  match oldPlan with
  | none => none
  | some bs =>
    if ∀ b ∈ bs, next b.1 = none ∨ next b.1 = some b.2 then
      some (bs.filter (fun b => next b.1 = none))
    else none

theorem set_compatibility_iff {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (next : κ → Option (Basis α)) (bs : List (κ × Basis α)) :
    SetCompatible next bs.toFinset ↔ compatibilityCheck next bs = true := by
  constructor
  · intro h
    apply (compatibility_check_iff next bs).mpr
    intro b hb
    exact h b (List.mem_toFinset.mpr hb)
  · intro h b hb
    exact (compatibility_check_iff next bs).mp h b (List.mem_toFinset.mp hb)

theorem refresh_set_plan_bridge {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (next : κ → Option (Basis α)) (oldPlan : Option (List (κ × Basis α))) :
    refreshSetPlan next (oldPlan.map List.toFinset) = refreshPlan next oldPlan := by
  cases oldPlan with
  | none => rfl
  | some bs =>
    by_cases h : compatibilityCheck next bs = true
    · have hp : SetCompatible next bs.toFinset := (set_compatibility_iff next bs).mpr h
      change (if ∀ b ∈ bs.toFinset, next b.1 = none ∨ next b.1 = some b.2 then
        some (bs.toFinset.filter (fun b => next b.1 = none)) else none) =
        (if compatibilityCheck next bs = true then
          some (bs.toFinset.filter (fun b => next b.1 = none)) else none)
      rw [if_pos hp,if_pos h]
    · have hp : ¬ SetCompatible next bs.toFinset := fun hc =>
        h ((set_compatibility_iff next bs).mp hc)
      change (if ∀ b ∈ bs.toFinset, next b.1 = none ∨ next b.1 = some b.2 then
        some (bs.toFinset.filter (fun b => next b.1 = none)) else none) =
        (if compatibilityCheck next bs = true then
          some (bs.toFinset.filter (fun b => next b.1 = none)) else none)
      rw [if_neg hp,if_neg h]

theorem refresh_set_plan_exact {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (req : List (κ × Basis α))
    (he : RegistryExtends reg next) :
    refreshSetPlan next ((checkedRecoveryPlan reg req).map List.toFinset) =
      (checkedRecoveryPlan next req).map List.toFinset :=
  (refresh_set_plan_bridge next (checkedRecoveryPlan reg req)).trans
    (refresh_plan_exact reg next req he)

def refreshSetCache {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (next : κ → Option (Basis α)) (cache : List (ι × Option (Finset (κ × Basis α)))) :
    List (ι × Option (Finset (κ × Basis α))) :=
  cache.map (fun r => (r.1, refreshSetPlan next r.2))

theorem refresh_set_cache_exact {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α)))
    (he : RegistryExtends reg next) :
    refreshSetCache next (setRoutePlans reg routes) = setRoutePlans next routes := by
  induction routes with
  | nil => rfl
  | cons r rs ih =>
    change (r.1, refreshSetPlan next ((checkedRecoveryPlan reg r.2).map List.toFinset)) ::
      refreshSetCache next (setRoutePlans reg rs) =
      (r.1, (checkedRecoveryPlan next r.2).map List.toFinset) ::
      setRoutePlans next rs
    rw [refresh_set_plan_exact reg next r.2 he, ih]

theorem refresh_set_cache_chain {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg mid last : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α)))
    (h₁ : RegistryExtends reg mid) (h₂ : RegistryExtends mid last) :
    refreshSetCache last (refreshSetCache mid (setRoutePlans reg routes)) =
      refreshSetCache last (setRoutePlans reg routes) := by
  calc
    _ = refreshSetCache last (setRoutePlans mid routes) :=
      congrArg (refreshSetCache last) (refresh_set_cache_exact reg mid routes h₁)
    _ = setRoutePlans last routes := refresh_set_cache_exact mid last routes h₂
    _ = _ := (refresh_set_cache_exact reg last routes (extends_trans reg mid last h₁ h₂)).symm

theorem refresh_set_frontier_chain {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg mid last : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α)))
    (h₁ : RegistryExtends reg mid) (h₂ : RegistryExtends mid last) :
    setFrontier (presentPlans (refreshSetCache last (refreshCached mid (cacheRoutes reg routes)))) =
      freshSetFrontier last routes := by
  have h : refreshSetCache last (refreshCached mid (cacheRoutes reg routes)) =
      setRoutePlans last routes :=
    (congrArg (refreshSetCache last) (refresh_cache_exact reg mid routes h₁)).trans
      (refresh_set_cache_exact mid last routes h₂)
  exact congrArg (fun xs => setFrontier (presentPlans xs)) h

end KuuOSR80
