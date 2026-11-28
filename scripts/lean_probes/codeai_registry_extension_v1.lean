/- R72: append-only registry extension and conditional recovery.
A checked insertion does not authenticate the supplied binding. Historical
admission and failure receipts remain attached to the old registry. -/
namespace KuuOSR72
open KuuOSR67 KuuOSR68 KuuOSR69 KuuOSR70 KuuOSR71
universe u v

def RegistryExtends {κ : Type v} {α : Type u}
    (reg next : κ → Option (Basis α)) : Prop :=
  ∀ k F, reg k = some F → next k = some F

theorem extends_refl {κ : Type v} {α : Type u} (reg : κ → Option (Basis α)) :
    RegistryExtends reg reg := fun _ _ h => h

theorem extends_trans {κ : Type v} {α : Type u}
    (reg mid next : κ → Option (Basis α))
    (h₁ : RegistryExtends reg mid) (h₂ : RegistryExtends mid next) :
    RegistryExtends reg next := fun k F h => h₂ k F (h₁ k F h)

theorem registered_steps_mono {κ : Type v} {α : Type u}
    (reg next : κ → Option (Basis α)) (path : List (TaggedStep κ α))
    (he : RegistryExtends reg next) (hs : RegisteredSteps reg path) :
    RegisteredSteps next path := by
  induction path with
  | nil => exact True.intro
  | cons s tail ih =>
      have hv : reg s.sourceKey = some s.patch.source ∧
          reg s.targetKey = some s.patch.target ∧ RegisteredSteps reg tail := hs
      exact ⟨he s.sourceKey s.patch.source hv.1, he s.targetKey s.patch.target hv.2.1, ih hv.2.2⟩

theorem registry_valid_mono {κ : Type v} {α : Type u}
    (reg next : κ → Option (Basis α)) (k l : κ) (F H : Basis α)
    (path : List (TaggedStep κ α)) (he : RegistryExtends reg next)
    (hv : RegistryValid reg k l F H path) : RegistryValid next k l F H path :=
  ⟨he k F hv.1, he l H hv.2.1, registered_steps_mono reg next path he hv.2.2⟩

theorem checked_registered_mono {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (k l : κ) (F H : Basis α)
    (path : List (TaggedStep κ α)) (P : Delta α)
    (he : RegistryExtends reg next) (hs : checkedRegisteredPath reg k l F H path = some P) :
    checkedRegisteredPath next k l F H path = some P := by
  have hv := (checked_registered_iff reg k l F H path P).mp hs
  exact (checked_registered_iff next k l F H path P).mpr
    ⟨registry_valid_mono reg next k l F H path he hv.1, hv.2⟩

theorem recovery_iff_of_tagged {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (k l : κ) (F H : Basis α)
    (path : List (TaggedStep κ α)) (P : Delta α)
    (ht : checkedTaggedPath k l F H path = some P) :
    checkedRegisteredPath reg k l F H path = some P ↔ RegistryValid reg k l F H path := by
  constructor
  · intro hs
    exact ((checked_registered_iff reg k l F H path P).mp hs).1
  · intro hv
    exact checked_registered_of_checks reg k l F H path P hv.1 hv.2.1
      ((registry_check_iff reg path).mpr hv.2.2) ht

-- An unchecked candidate. It is not admitted merely because it is computable.
def setBinding {κ : Type v} {α : Type u} [DecidableEq κ]
    (reg : κ → Option (Basis α)) (k : κ) (F : Basis α) (x : κ) : Option (Basis α) :=
  if x = k then some F else reg x

def checkedInsert {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (k : κ) (F : Basis α) :
    Option (κ → Option (Basis α)) :=
  if reg k = none then some (setBinding reg k F) else none

theorem set_binding_here {κ : Type v} {α : Type u} [DecidableEq κ]
    (reg : κ → Option (Basis α)) (k : κ) (F : Basis α) :
    setBinding reg k F k = some F := by
  unfold setBinding
  exact if_pos (rfl : k = k)

theorem fresh_binding_extends {κ : Type v} {α : Type u} [DecidableEq κ]
    (reg : κ → Option (Basis α)) (k : κ) (F : Basis α) (h : reg k = none) :
    RegistryExtends reg (setBinding reg k F) := by
  intro x G hg
  by_cases he : x = k
  · subst x
    have impossible : (none : Option (Basis α)) = some G := h.symm.trans hg
    cases impossible
  · unfold setBinding
    exact (if_neg he).trans hg

theorem checked_insert_fresh {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (k : κ) (F : Basis α) (h : reg k = none) :
    checkedInsert reg k F = some (setBinding reg k F) := by
  unfold checkedInsert
  exact if_pos h

theorem checked_insert_sound {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (k : κ) (F : Basis α)
    (hs : checkedInsert reg k F = some next) :
    reg k = none ∧ RegistryExtends reg next ∧ next k = some F := by
  unfold checkedInsert at hs
  by_cases h : reg k = none
  · rw [if_pos h] at hs
    have he := Option.some.inj hs
    subst next
    exact ⟨h, fresh_binding_extends reg k F h, set_binding_here reg k F⟩
  · rw [if_neg h] at hs
    cases hs

theorem checked_insert_reject_present {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (k : κ) (F G : Basis α) (h : reg k = some G) :
    checkedInsert reg k F = none := by
  unfold checkedInsert
  apply if_neg
  intro he
  have impossible : (some G : Option (Basis α)) = none := h.symm.trans he
  cases impossible

theorem conflicting_rebind_not_extension {κ : Type v} {α : Type u} [DecidableEq κ]
    (reg : κ → Option (Basis α)) (k : κ) (F G : Basis α)
    (h : reg k = some G) (hne : G ≠ F) :
    ¬ RegistryExtends reg (setBinding reg k F) := by
  intro he
  exact hne (registered_binding_unique (setBinding reg k F) k G F
    (he k G h) (set_binding_here reg k F))

theorem fresh_identity_recovery {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (k : κ) (F : Basis α) (h : reg k = none) :
    checkedRegisteredPath reg k k F F [] = none ∧
      checkedRegisteredPath (setBinding reg k F) k k F F [] =
        some ((∅ : Basis α), (∅ : Basis α)) := by
  refine ⟨(unknown_key_alias reg k F h).2, ?_⟩
  have hb := set_binding_here reg k F
  calc
    _ = some (F \ F, F \ F) :=
      checked_registered_of_checks (setBinding reg k F) k k F F [] _ hb hb rfl
        (checked_tagged_exact k k F F [] rfl rfl)
    _ = _ := by simp

end KuuOSR72
