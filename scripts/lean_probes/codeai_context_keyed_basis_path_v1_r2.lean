/- R70: context-keyed checked paths.
Keys and mathematical endpoints are checked independently. A key is a
supplied identity, not a proof of authentication or permission. -/
namespace KuuOSR70
open KuuOSR67 KuuOSR68 KuuOSR69
universe u v

structure TaggedStep (κ : Type v) (α : Type u) where
  sourceKey : κ
  targetKey : κ
  patch : PatchStep α

def KeysValid {κ : Type v} {α : Type u} :
    κ → κ → List (TaggedStep κ α) → Prop
  | k, l, [] => k = l
  | k, l, s :: tail => k = s.sourceKey ∧ KeysValid s.targetKey l tail

def keyCheck {κ : Type v} {α : Type u} [DecidableEq κ] :
    κ → κ → List (TaggedStep κ α) → Bool
  | k, l, [] => decide (k = l)
  | k, l, s :: tail =>
      if k = s.sourceKey then keyCheck s.targetKey l tail else false

def checkedTaggedPath {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (k l : κ) (F H : Basis α) (path : List (TaggedStep κ α)) : Option (Delta α) :=
  if keyCheck k l path = true then checkedPath F H (path.map TaggedStep.patch) else none

theorem key_check_iff {κ : Type v} {α : Type u} [DecidableEq κ]
    (k l : κ) (path : List (TaggedStep κ α)) :
    keyCheck k l path = true ↔ KeysValid k l path := by
  induction path generalizing k with
  | nil =>
      change decide (k = l) = true ↔ k = l
      exact ⟨of_decide_eq_true (p := k = l), decide_eq_true (p := k = l)⟩
  | cons s tail ih =>
      change (if k = s.sourceKey then keyCheck s.targetKey l tail else false) = true ↔
        (k = s.sourceKey ∧ KeysValid s.targetKey l tail)
      by_cases he : k = s.sourceKey
      · rw [if_pos he, ih s.targetKey]
        exact ⟨fun hv => ⟨he, hv⟩, fun hv => hv.2⟩
      · rw [if_neg he]
        constructor
        · intro hf
          cases hf
        · intro hv
          exact False.elim (he hv.1)

theorem checked_tagged_iff {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (k l : κ) (F H : Basis α) (path : List (TaggedStep κ α)) (P : Delta α) :
    checkedTaggedPath k l F H path = some P ↔
      KeysValid k l path ∧ PathValid F H (path.map TaggedStep.patch) ∧ P = (F \ H, H \ F) := by
  unfold checkedTaggedPath
  by_cases hc : keyCheck k l path = true
  · rw [if_pos hc]
    have hk := (key_check_iff k l path).mp hc
    constructor
    · intro hp
      have hh := (checked_path_iff F H (path.map TaggedStep.patch) P).mp hp
      exact ⟨hk, hh.1, hh.2⟩
    · rintro ⟨_, hv, he⟩
      exact (checked_path_iff F H (path.map TaggedStep.patch) P).mpr ⟨hv, he⟩
  · rw [if_neg hc]
    constructor
    · intro hs
      cases hs
    · intro hv
      exact False.elim (hc ((key_check_iff k l path).mpr hv.1))

theorem checked_tagged_exact {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (k l : κ) (F H : Basis α) (path : List (TaggedStep κ α))
    (hk : KeysValid k l path) (hp : PathValid F H (path.map TaggedStep.patch)) :
    checkedTaggedPath k l F H path = some (F \ H, H \ F) :=
  (checked_tagged_iff k l F H path (F \ H, H \ F)).mpr ⟨hk, hp, rfl⟩

theorem checked_tagged_projection {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (k l : κ) (F H : Basis α) (path : List (TaggedStep κ α)) (P : Delta α)
    (hs : checkedTaggedPath k l F H path = some P) :
    checkedPath F H (path.map TaggedStep.patch) = some P := by
  have hv := (checked_tagged_iff k l F H path P).mp hs
  exact (checked_path_iff F H (path.map TaggedStep.patch) P).mpr ⟨hv.2.1, hv.2.2⟩

theorem checked_tagged_reject_keys {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (k l : κ) (F H : Basis α) (path : List (TaggedStep κ α))
    (hk : ¬ KeysValid k l path) : checkedTaggedPath k l F H path = none := by
  unfold checkedTaggedPath
  exact if_neg (fun h => hk ((key_check_iff k l path).mp h))

theorem checked_tagged_reject_source {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (k l : κ) (F H : Basis α) (s : TaggedStep κ α) (tail : List (TaggedStep κ α))
    (hk : k ≠ s.sourceKey) : checkedTaggedPath k l F H (s :: tail) = none :=
  checked_tagged_reject_keys k l F H (s :: tail) (fun hv => hk hv.1)

theorem equal_basis_wrong_key {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (k l : κ) (F : Basis α) (hk : k ≠ l) :
    checkedPath F F [] = some ((∅ : Basis α), (∅ : Basis α)) ∧
    checkedTaggedPath k l F F [] = none := by
  refine ⟨?_, checked_tagged_reject_keys k l F F [] hk⟩
  calc
    _ = some (F \ F, F \ F) := checked_path_exact F F [] rfl
    _ = _ := by simp

theorem keys_append_valid {κ : Type v} {α : Type u}
    (k l m : κ) (xs ys : List (TaggedStep κ α))
    (hx : KeysValid k l xs) (hy : KeysValid l m ys) : KeysValid k m (xs ++ ys) := by
  induction xs generalizing k with
  | nil =>
      have he : k = l := hx
      subst k
      exact hy
  | cons s tail ih =>
      have hv : k = s.sourceKey ∧ KeysValid s.targetKey l tail := hx
      exact ⟨hv.1, ih s.targetKey hv.2⟩

theorem checked_tagged_append {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (k l m : κ) (F G H : Basis α) (xs ys : List (TaggedStep κ α)) (P Q : Delta α)
    (hx : checkedTaggedPath k l F G xs = some P)
    (hy : checkedTaggedPath l m G H ys = some Q) :
    checkedTaggedPath k m F H (xs ++ ys) = some (composeDelta P.1 P.2 Q.1 Q.2) := by
  obtain ⟨kx, px, ex⟩ := (checked_tagged_iff k l F G xs P).mp hx
  obtain ⟨ky, py, ey⟩ := (checked_tagged_iff l m G H ys Q).mp hy
  subst P
  subst Q
  have hk := keys_append_valid k l m xs ys kx ky
  have hp : PathValid F H ((xs ++ ys).map TaggedStep.patch) := by
    rw [List.map_append]
    exact path_append_valid F G H (xs.map TaggedStep.patch) (ys.map TaggedStep.patch) px py
  exact (checked_tagged_exact k m F H (xs ++ ys) hk hp).trans
    (congrArg some (compose_diff_exact F G H)).symm

def taggedWalk {κ : Type v} {α : Type u} [DecidableEq α] :
    (κ × Basis α) → List (κ × Basis α) → List (TaggedStep κ α)
  | _, [] => []
  | F, G :: tail => ⟨F.1, G.1, canonicalStep F.2 G.2⟩ :: taggedWalk G tail

def taggedEnd {κ : Type v} {α : Type u} :
    (κ × Basis α) → List (κ × Basis α) → (κ × Basis α)
  | F, [] => F
  | _, G :: tail => taggedEnd G tail

theorem tagged_walk_valid {κ : Type v} {α : Type u} [DecidableEq α]
    (F : κ × Basis α) (ends : List (κ × Basis α)) :
    KeysValid F.1 (taggedEnd F ends).1 (taggedWalk F ends) ∧
    PathValid F.2 (taggedEnd F ends).2 ((taggedWalk F ends).map TaggedStep.patch) := by
  induction ends generalizing F with
  | nil => exact ⟨rfl, rfl⟩
  | cons G tail ih =>
      have hv := ih G
      exact ⟨⟨rfl, hv.1⟩, ⟨rfl, checked_bound_exact F.2 G.2, hv.2⟩⟩

theorem tagged_walk_exact {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (F : κ × Basis α) (ends : List (κ × Basis α)) :
    checkedTaggedPath F.1 (taggedEnd F ends).1 F.2 (taggedEnd F ends).2 (taggedWalk F ends) =
      some (F.2 \ (taggedEnd F ends).2, (taggedEnd F ends).2 \ F.2) :=
  checked_tagged_exact F.1 (taggedEnd F ends).1 F.2 (taggedEnd F ends).2 (taggedWalk F ends)
    (tagged_walk_valid F ends).1 (tagged_walk_valid F ends).2

theorem checked_tagged_replay {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (k l : κ) (F H : Basis α) (path : List (TaggedStep κ α)) (P : Delta α)
    (hs : checkedTaggedPath k l F H path = some P) :
    checkedBoundPatch F H P.1 P.2 = some H ∧ checkedBoundPatch H F P.2 P.1 = some F :=
  checked_path_replay F H (path.map TaggedStep.patch) P (checked_tagged_projection k l F H path P hs)

end KuuOSR70
