/- R69: checked finite paths of reversible basis patches.
The net delta is a projection, not the path. Every supplied source, target,
and local difference is checked. No action or publication authority follows. -/
namespace KuuOSR69
open KuuOSR67 KuuOSR68
universe u

abbrev Basis (α : Type u) := Finset (Finset α)
abbrev Delta (α : Type u) := Basis α × Basis α

structure PatchStep (α : Type u) where
  source : Basis α
  target : Basis α
  retired : Basis α
  introduced : Basis α

def PathValid {α : Type u} [DecidableEq α] :
    Basis α → Basis α → List (PatchStep α) → Prop
  | F, H, [] => F = H
  | F, H, s :: tail =>
      F = s.source ∧
      checkedBoundPatch F s.target s.retired s.introduced = some s.target ∧
      PathValid s.target H tail

def checkedPath {α : Type u} [DecidableEq α] :
    Basis α → Basis α → List (PatchStep α) → Option (Delta α)
  | F, H, [] => if F = H then some (∅, ∅) else none
  | F, H, s :: tail =>
      if F = s.source ∧
          checkedBoundPatch F s.target s.retired s.introduced = some s.target then
        match checkedPath s.target H tail with
        | none => none
        | some p => some (composeDelta s.retired s.introduced p.1 p.2)
      else none

theorem checked_path_exact {α : Type u} [DecidableEq α]
    (F H : Basis α) (path : List (PatchStep α)) (h : PathValid F H path) :
    checkedPath F H path = some (F \ H, H \ F) := by
  induction path generalizing F with
  | nil =>
      have he : F = H := h
      subst H
      unfold checkedPath
      calc
        _ = some ((∅ : Basis α), (∅ : Basis α)) := if_pos (rfl : F = F)
        _ = _ := by simp
  | cons s tail ih =>
      have hv : F = s.source ∧
          checkedBoundPatch F s.target s.retired s.introduced = some s.target ∧
          PathValid s.target H tail := h
      have hc : F = s.source ∧
          checkedBoundPatch F s.target s.retired s.introduced = some s.target :=
        ⟨hv.1, hv.2.1⟩
      have hb := bound_sound F s.target s.retired s.introduced hv.2.1
      have ht := ih s.target hv.2.2
      calc
        _ = some (composeDelta s.retired s.introduced (s.target \ H) (H \ s.target)) := by
          rw [checkedPath, if_pos hc, ht]
        _ = _ := congrArg some
          (compose_valid_exact F s.target H s.retired s.introduced
            (s.target \ H) (H \ s.target) hb.1 hb.2
            (actual_patch_valid s.target H) (apply_diff_exact s.target H))

theorem checked_path_sound {α : Type u} [DecidableEq α]
    (F H : Basis α) (path : List (PatchStep α)) (P : Delta α)
    (hs : checkedPath F H path = some P) : PathValid F H path := by
  induction path generalizing F P with
  | nil =>
      unfold checkedPath at hs
      by_cases he : F = H
      · exact he
      · rw [if_neg he] at hs
        cases hs
  | cons s tail ih =>
      unfold checkedPath at hs
      by_cases hc : F = s.source ∧
          checkedBoundPatch F s.target s.retired s.introduced = some s.target
      · rw [if_pos hc] at hs
        cases ht : checkedPath s.target H tail with
        | none =>
            rw [ht] at hs
            cases hs
        | some q =>
            exact ⟨hc.1, hc.2, ih s.target q ht⟩
      · rw [if_neg hc] at hs
        cases hs

theorem checked_path_iff {α : Type u} [DecidableEq α]
    (F H : Basis α) (path : List (PatchStep α)) (P : Delta α) :
    checkedPath F H path = some P ↔ PathValid F H path ∧ P = (F \ H, H \ F) := by
  constructor
  · intro hs
    have hv := checked_path_sound F H path P hs
    exact ⟨hv, Option.some.inj (hs.symm.trans (checked_path_exact F H path hv))⟩
  · rintro ⟨hv, rfl⟩
    exact checked_path_exact F H path hv

theorem checked_path_replay {α : Type u} [DecidableEq α]
    (F H : Basis α) (path : List (PatchStep α)) (P : Delta α)
    (hs : checkedPath F H path = some P) :
    checkedBoundPatch F H P.1 P.2 = some H ∧
      checkedBoundPatch H F P.2 P.1 = some F := by
  have he := ((checked_path_iff F H path P).mp hs).2
  subst P
  exact ⟨checked_bound_exact F H, checked_bound_exact H F⟩

theorem path_append_valid {α : Type u} [DecidableEq α]
    (F G H : Basis α) (xs ys : List (PatchStep α))
    (hx : PathValid F G xs) (hy : PathValid G H ys) :
    PathValid F H (xs ++ ys) := by
  induction xs generalizing F with
  | nil =>
      have he : F = G := hx
      subst F
      exact hy
  | cons s tail ih =>
      have hv : F = s.source ∧
          checkedBoundPatch F s.target s.retired s.introduced = some s.target ∧
          PathValid s.target G tail := hx
      exact ⟨hv.1, hv.2.1, ih s.target hv.2.2⟩

theorem checked_path_append_composes {α : Type u} [DecidableEq α]
    (F G H : Basis α) (xs ys : List (PatchStep α)) (P Q : Delta α)
    (hx : checkedPath F G xs = some P) (hy : checkedPath G H ys = some Q) :
    checkedPath F H (xs ++ ys) = some (composeDelta P.1 P.2 Q.1 Q.2) := by
  obtain ⟨vx, ex⟩ := (checked_path_iff F G xs P).mp hx
  obtain ⟨vy, ey⟩ := (checked_path_iff G H ys Q).mp hy
  subst P
  subst Q
  exact (checked_path_exact F H (xs ++ ys) (path_append_valid F G H xs ys vx vy)).trans
    (congrArg some (compose_diff_exact F G H)).symm

theorem checked_reject_source {α : Type u} [DecidableEq α]
    (F H : Basis α) (s : PatchStep α) (tail : List (PatchStep α))
    (h : F ≠ s.source) : checkedPath F H (s :: tail) = none := by
  unfold checkedPath
  exact if_neg (fun hc => h hc.1)

theorem checked_reject_step {α : Type u} [DecidableEq α]
    (F H : Basis α) (s : PatchStep α) (tail : List (PatchStep α))
    (h : checkedBoundPatch F s.target s.retired s.introduced ≠ some s.target) :
    checkedPath F H (s :: tail) = none := by
  unfold checkedPath
  exact if_neg (fun hc => h hc.2)

theorem checked_reject_empty {α : Type u} [DecidableEq α]
    (F H : Basis α) (h : F ≠ H) : checkedPath F H [] = none := by
  unfold checkedPath
  exact if_neg h

theorem checked_reject_tail {α : Type u} [DecidableEq α]
    (F H : Basis α) (s : PatchStep α) (tail : List (PatchStep α))
    (h : checkedPath s.target H tail = none) :
    checkedPath F H (s :: tail) = none := by
  unfold checkedPath
  by_cases hc : F = s.source ∧
      checkedBoundPatch F s.target s.retired s.introduced = some s.target
  · rw [if_pos hc, h]
  · exact if_neg hc

def canonicalStep {α : Type u} [DecidableEq α] (F G : Basis α) : PatchStep α :=
  ⟨F, G, F \ G, G \ F⟩

def canonicalWalk {α : Type u} [DecidableEq α] : Basis α → List (Basis α) → List (PatchStep α)
  | _, [] => []
  | F, G :: tail => canonicalStep F G :: canonicalWalk G tail

def walkEnd {α : Type u} : Basis α → List (Basis α) → Basis α
  | F, [] => F
  | _, G :: tail => walkEnd G tail

theorem canonical_walk_valid {α : Type u} [DecidableEq α]
    (F : Basis α) (ends : List (Basis α)) :
    PathValid F (walkEnd F ends) (canonicalWalk F ends) := by
  induction ends generalizing F with
  | nil => rfl
  | cons G tail ih =>
      exact ⟨rfl, checked_bound_exact F G, ih G⟩

theorem canonical_walk_exact {α : Type u} [DecidableEq α]
    (F : Basis α) (ends : List (Basis α)) :
    checkedPath F (walkEnd F ends) (canonicalWalk F ends) =
      some (F \ walkEnd F ends, walkEnd F ends \ F) :=
  checked_path_exact F (walkEnd F ends) (canonicalWalk F ends) (canonical_walk_valid F ends)

-- Empty and nonempty histories can have exactly the same checked net delta.
theorem net_history_collision {α : Type u} [DecidableEq α]
    (F G : Basis α) :
    checkedPath F F [] = checkedPath F F (canonicalWalk F [G, F]) ∧
      ([] : List (PatchStep α)) ≠ canonicalWalk F [G, F] := by
  refine ⟨(canonical_walk_exact F []).trans (canonical_walk_exact F [G, F]).symm, ?_⟩
  change ([] : List (PatchStep α)) ≠ [canonicalStep F G, canonicalStep G F]
  simp

end KuuOSR69
