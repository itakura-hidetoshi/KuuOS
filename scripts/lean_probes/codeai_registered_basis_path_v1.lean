/- R71: registered key-to-basis binding in checked paths.
The registry is a supplied finite observation, not an authentication or
action-authority oracle. Unknown registration is an admission failure. -/
namespace KuuOSR71
open KuuOSR67 KuuOSR68 KuuOSR69 KuuOSR70
universe u v

def RegisteredSteps {κ : Type v} {α : Type u}
    (reg : κ → Option (Basis α)) : List (TaggedStep κ α) → Prop
  | [] => True
  | s :: tail =>
      reg s.sourceKey = some s.patch.source ∧
      reg s.targetKey = some s.patch.target ∧ RegisteredSteps reg tail

def registryCheck {κ : Type v} {α : Type u} [DecidableEq α]
    (reg : κ → Option (Basis α)) : List (TaggedStep κ α) → Bool
  | [] => true
  | s :: tail =>
      if reg s.sourceKey = some s.patch.source ∧ reg s.targetKey = some s.patch.target
      then registryCheck reg tail else false

def RegistryValid {κ : Type v} {α : Type u} (reg : κ → Option (Basis α))
    (k l : κ) (F H : Basis α) (path : List (TaggedStep κ α)) : Prop :=
  reg k = some F ∧ reg l = some H ∧ RegisteredSteps reg path

def checkedRegisteredPath {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (k l : κ) (F H : Basis α)
    (path : List (TaggedStep κ α)) : Option (Delta α) :=
  if reg k = some F ∧ reg l = some H ∧ registryCheck reg path = true
  then checkedTaggedPath k l F H path else none

theorem registry_check_iff {κ : Type v} {α : Type u} [DecidableEq α]
    (reg : κ → Option (Basis α)) (path : List (TaggedStep κ α)) :
    registryCheck reg path = true ↔ RegisteredSteps reg path := by
  induction path with
  | nil =>
      change true = true ↔ True
      exact ⟨fun _ => True.intro, fun _ => rfl⟩
  | cons s tail ih =>
      change (if reg s.sourceKey = some s.patch.source ∧ reg s.targetKey = some s.patch.target
        then registryCheck reg tail else false) = true ↔
        (reg s.sourceKey = some s.patch.source ∧ reg s.targetKey = some s.patch.target ∧ RegisteredSteps reg tail)
      by_cases hc : reg s.sourceKey = some s.patch.source ∧ reg s.targetKey = some s.patch.target
      · rw [if_pos hc, ih]
        exact ⟨fun ht => ⟨hc.1, hc.2, ht⟩, fun ht => ht.2.2⟩
      · rw [if_neg hc]
        constructor
        · intro hf
          cases hf
        · intro ht
          exact False.elim (hc ⟨ht.1, ht.2.1⟩)

theorem registered_steps_append {κ : Type v} {α : Type u}
    (reg : κ → Option (Basis α)) (xs ys : List (TaggedStep κ α))
    (hx : RegisteredSteps reg xs) (hy : RegisteredSteps reg ys) :
    RegisteredSteps reg (xs ++ ys) := by
  induction xs with
  | nil => exact hy
  | cons s tail ih =>
      have hv : reg s.sourceKey = some s.patch.source ∧
          reg s.targetKey = some s.patch.target ∧ RegisteredSteps reg tail := hx
      exact ⟨hv.1, hv.2.1, ih hv.2.2⟩

theorem registered_step_mem {κ : Type v} {α : Type u}
    (reg : κ → Option (Basis α)) (path : List (TaggedStep κ α))
    (hv : RegisteredSteps reg path) (s : TaggedStep κ α) (hs : s ∈ path) :
    reg s.sourceKey = some s.patch.source ∧ reg s.targetKey = some s.patch.target := by
  induction path with
  | nil => cases hs
  | cons t tail ih =>
      have h : reg t.sourceKey = some t.patch.source ∧
          reg t.targetKey = some t.patch.target ∧ RegisteredSteps reg tail := hv
      rcases List.mem_cons.mp hs with he | hm
      · subst s
        exact ⟨h.1, h.2.1⟩
      · exact ih h.2.2 hm

theorem checked_registered_iff {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (k l : κ) (F H : Basis α)
    (path : List (TaggedStep κ α)) (P : Delta α) :
    checkedRegisteredPath reg k l F H path = some P ↔
      RegistryValid reg k l F H path ∧ KeysValid k l path ∧
      PathValid F H (path.map TaggedStep.patch) ∧ P = (F \ H, H \ F) := by
  unfold checkedRegisteredPath
  by_cases hc : reg k = some F ∧ reg l = some H ∧ registryCheck reg path = true
  · rw [if_pos hc]
    constructor
    · intro hs
      have hv := (checked_tagged_iff k l F H path P).mp hs
      exact ⟨⟨hc.1, hc.2.1, (registry_check_iff reg path).mp hc.2.2⟩, hv.1, hv.2.1, hv.2.2⟩
    · intro hv
      exact (checked_tagged_iff k l F H path P).mpr hv.2
  · rw [if_neg hc]
    constructor
    · intro hs
      cases hs
    · intro hv
      exact False.elim (hc ⟨hv.1.1, hv.1.2.1, (registry_check_iff reg path).mpr hv.1.2.2⟩)

theorem checked_registered_of_checks {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (k l : κ) (F H : Basis α)
    (path : List (TaggedStep κ α)) (P : Delta α)
    (hf : reg k = some F) (hh : reg l = some H) (hr : registryCheck reg path = true)
    (hs : checkedTaggedPath k l F H path = some P) :
    checkedRegisteredPath reg k l F H path = some P := by
  unfold checkedRegisteredPath
  exact (if_pos ⟨hf, hh, hr⟩).trans hs

theorem checked_registered_projection {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (k l : κ) (F H : Basis α)
    (path : List (TaggedStep κ α)) (P : Delta α)
    (hs : checkedRegisteredPath reg k l F H path = some P) :
    checkedTaggedPath k l F H path = some P :=
  (checked_tagged_iff k l F H path P).mpr ((checked_registered_iff reg k l F H path P).mp hs).2

theorem checked_registered_reject_source {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (k l : κ) (F H : Basis α)
    (path : List (TaggedStep κ α)) (h : reg k ≠ some F) :
    checkedRegisteredPath reg k l F H path = none := by
  unfold checkedRegisteredPath
  exact if_neg (fun hc => h hc.1)

theorem checked_registered_reject_target {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (k l : κ) (F H : Basis α)
    (path : List (TaggedStep κ α)) (h : reg l ≠ some H) :
    checkedRegisteredPath reg k l F H path = none := by
  unfold checkedRegisteredPath
  exact if_neg (fun hc => h hc.2.1)

theorem checked_registered_reject_steps {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (k l : κ) (F H : Basis α)
    (path : List (TaggedStep κ α)) (h : ¬ RegisteredSteps reg path) :
    checkedRegisteredPath reg k l F H path = none := by
  unfold checkedRegisteredPath
  exact if_neg (fun hc => h ((registry_check_iff reg path).mp hc.2.2))

theorem registered_binding_unique {κ : Type v} {α : Type u}
    (reg : κ → Option (Basis α)) (k : κ) (F G : Basis α)
    (hf : reg k = some F) (hg : reg k = some G) : F = G :=
  Option.some.inj (hf.symm.trans hg)

theorem checked_registered_append {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (k l m : κ) (F G H : Basis α)
    (xs ys : List (TaggedStep κ α)) (P Q : Delta α)
    (hx : checkedRegisteredPath reg k l F G xs = some P)
    (hy : checkedRegisteredPath reg l m G H ys = some Q) :
    checkedRegisteredPath reg k m F H (xs ++ ys) = some (composeDelta P.1 P.2 Q.1 Q.2) := by
  have rx := ((checked_registered_iff reg k l F G xs P).mp hx).1
  have ry := ((checked_registered_iff reg l m G H ys Q).mp hy).1
  exact checked_registered_of_checks reg k m F H (xs ++ ys) _ rx.1 ry.2.1
    ((registry_check_iff reg (xs ++ ys)).mpr (registered_steps_append reg xs ys rx.2.2 ry.2.2))
    (checked_tagged_append k l m F G H xs ys P Q
      (checked_registered_projection reg k l F G xs P hx)
      (checked_registered_projection reg l m G H ys Q hy))

theorem checked_registered_replay {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (k l : κ) (F H : Basis α)
    (path : List (TaggedStep κ α)) (P : Delta α)
    (hs : checkedRegisteredPath reg k l F H path = some P) :
    checkedBoundPatch F H P.1 P.2 = some H ∧ checkedBoundPatch H F P.2 P.1 = some F :=
  checked_tagged_replay k l F H path P (checked_registered_projection reg k l F H path P hs)

theorem unknown_key_alias {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (k : κ) (F : Basis α) (h : reg k = none) :
    checkedTaggedPath k k F F [] = some ((∅ : Basis α), (∅ : Basis α)) ∧
      checkedRegisteredPath reg k k F F [] = none := by
  have hn : reg k ≠ some F := by
    intro he
    have hh : (none : Option (Basis α)) = some F := h.symm.trans he
    cases hh
  refine ⟨?_, checked_registered_reject_source reg k k F F [] hn⟩
  calc
    _ = some (F \ F, F \ F) := checked_tagged_exact k k F F [] rfl rfl
    _ = _ := by simp

end KuuOSR71
