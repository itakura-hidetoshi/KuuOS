/- R81: finite registry-extension chains, with a complete ordered route cache.
The chain predicate is a proof obligation, not an authentication mechanism.
Only the endpoint cache and frontier are identified; the histories are not. -/
namespace KuuOSR81
open KuuOSR69 KuuOSR72 KuuOSR79 KuuOSR80
universe u v w

def RegistryChain {κ : Type v} {α : Type u}
    (reg : κ → Option (Basis α)) : List (κ → Option (Basis α)) → Prop
  | [] => True
  | next :: tail => RegistryExtends reg next ∧ RegistryChain next tail

def chainEnd {κ : Type v} {α : Type u}
    (reg : κ → Option (Basis α)) : List (κ → Option (Basis α)) → (κ → Option (Basis α))
  | [] => reg
  | next :: tail => chainEnd next tail

def refreshChain {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (cache : List (ι × Option (Finset (κ × Basis α)))) :
    List (κ → Option (Basis α)) → List (ι × Option (Finset (κ × Basis α)))
  | [] => cache
  | next :: tail => refreshChain (refreshSetCache next cache) tail

theorem chain_end_extends {κ : Type v} {α : Type u}
    (reg : κ → Option (Basis α)) (updates : List (κ → Option (Basis α)))
    (h : RegistryChain reg updates) : RegistryExtends reg (chainEnd reg updates) := by
  induction updates generalizing reg with
  | nil => exact fun k b hb => hb
  | cons next tail ih =>
    change RegistryExtends reg next ∧ RegistryChain next tail at h
    change RegistryExtends reg (chainEnd next tail)
    exact extends_trans reg next (chainEnd next tail) h.1 (ih next h.2)

theorem chain_end_append {κ : Type v} {α : Type u}
    (reg : κ → Option (Basis α)) (xs ys : List (κ → Option (Basis α))) :
    chainEnd reg (xs ++ ys) = chainEnd (chainEnd reg xs) ys := by
  induction xs generalizing reg with
  | nil => rfl
  | cons next tail ih =>
    change chainEnd next (tail ++ ys) = chainEnd (chainEnd next tail) ys
    exact ih next

theorem refresh_chain_append {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (cache : List (ι × Option (Finset (κ × Basis α))))
    (xs ys : List (κ → Option (Basis α))) :
    refreshChain cache (xs ++ ys) = refreshChain (refreshChain cache xs) ys := by
  induction xs generalizing cache with
  | nil => rfl
  | cons next tail ih =>
    change refreshChain (refreshSetCache next cache) (tail ++ ys) =
      refreshChain (refreshChain (refreshSetCache next cache) tail) ys
    exact ih (refreshSetCache next cache)

theorem refresh_chain_exact {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α)))
    (updates : List (κ → Option (Basis α))) (h : RegistryChain reg updates) :
    refreshChain (setRoutePlans reg routes) updates = setRoutePlans (chainEnd reg updates) routes := by
  induction updates generalizing reg with
  | nil => rfl
  | cons next tail ih =>
    change RegistryExtends reg next ∧ RegistryChain next tail at h
    change refreshChain (refreshSetCache next (setRoutePlans reg routes)) tail =
      setRoutePlans (chainEnd next tail) routes
    rw [refresh_set_cache_exact reg next routes h.1]
    exact ih next h.2

theorem refresh_chain_one_shot {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α)))
    (updates : List (κ → Option (Basis α))) (h : RegistryChain reg updates) :
    refreshChain (setRoutePlans reg routes) updates =
      refreshSetCache (chainEnd reg updates) (setRoutePlans reg routes) :=
  (refresh_chain_exact reg routes updates h).trans
    (refresh_set_cache_exact reg (chainEnd reg updates) routes (chain_end_extends reg updates h)).symm

theorem refresh_chain_frontier_exact {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (routes : List (ι × List (κ × Basis α)))
    (updates : List (κ → Option (Basis α))) (h : RegistryChain reg updates) :
    setFrontier (presentPlans (refreshChain (setRoutePlans reg routes) updates)) =
      freshSetFrontier (chainEnd reg updates) routes :=
  congrArg (fun xs => setFrontier (presentPlans xs)) (refresh_chain_exact reg routes updates h)

end KuuOSR81
