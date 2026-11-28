/- R68: endpoint-checked composition of reversible obstruction-basis patches.
The compressed net delta is not a replacement for the original path record.
No action authority follows from finite-set equality. -/
namespace KuuOSR68
open KuuOSR67
universe u

def composeRemoved {α : Type u} [DecidableEq α]
    (R₁ N₁ R₂ N₂ : Finset (Finset α)) : Finset (Finset α) :=
  (R₁ \ N₂) ∪ (R₂ \ N₁)

def composeAdded {α : Type u} [DecidableEq α]
    (R₁ N₁ R₂ N₂ : Finset (Finset α)) : Finset (Finset α) :=
  (N₂ \ R₁) ∪ (N₁ \ R₂)

def composeDelta {α : Type u} [DecidableEq α]
    (R₁ N₁ R₂ N₂ : Finset (Finset α)) :
    Finset (Finset α) × Finset (Finset α) :=
  (composeRemoved R₁ N₁ R₂ N₂, composeAdded R₁ N₁ R₂ N₂)

theorem compose_removed_exact {α : Type u} [DecidableEq α]
    (F G H : Finset (Finset α)) :
    composeRemoved (F \ G) (G \ F) (G \ H) (H \ G) = F \ H := by
  apply Finset.ext
  intro x
  simp only [composeRemoved, Finset.mem_union, Finset.mem_sdiff]
  by_cases hf : x ∈ F <;> by_cases hg : x ∈ G <;> by_cases hh : x ∈ H <;>
    simp [hf, hg, hh]

theorem compose_added_exact {α : Type u} [DecidableEq α]
    (F G H : Finset (Finset α)) :
    composeAdded (F \ G) (G \ F) (G \ H) (H \ G) = H \ F := by
  apply Finset.ext
  intro x
  simp only [composeAdded, Finset.mem_union, Finset.mem_sdiff]
  by_cases hf : x ∈ F <;> by_cases hg : x ∈ G <;> by_cases hh : x ∈ H <;>
    simp [hf, hg, hh]

theorem compose_diff_exact {α : Type u} [DecidableEq α]
    (F G H : Finset (Finset α)) :
    composeDelta (F \ G) (G \ F) (G \ H) (H \ G) = (F \ H, H \ F) :=
  congrArg₂ Prod.mk (compose_removed_exact F G H) (compose_added_exact F G H)

theorem compose_valid_exact {α : Type u} [DecidableEq α]
    (F G H R₁ N₁ R₂ N₂ : Finset (Finset α))
    (h₁ : PatchValid F R₁ N₁) (e₁ : applyPatch F R₁ N₁ = G)
    (h₂ : PatchValid G R₂ N₂) (e₂ : applyPatch G R₂ N₂ = H) :
    composeDelta R₁ N₁ R₂ N₂ = (F \ H, H \ F) := by
  obtain ⟨hr₁, hn₁⟩ := patch_unique F G R₁ N₁ h₁ e₁
  obtain ⟨hr₂, hn₂⟩ := patch_unique G H R₂ N₂ h₂ e₂
  subst R₁
  subst N₁
  subst R₂
  subst N₂
  exact compose_diff_exact F G H

theorem bound_sound {α : Type u} [DecidableEq α]
    (F G R N : Finset (Finset α))
    (hs : checkedBoundPatch F G R N = some G) :
    PatchValid F R N ∧ applyPatch F R N = G := by
  unfold checkedBoundPatch at hs
  by_cases hv : (R ⊆ F ∧ ∀ x ∈ N, x ∉ F) ∧ applyPatch F R N = G
  · exact hv
  · have he : (none : Option (Finset (Finset α))) = some G :=
      (if_neg hv).symm.trans hs
    cases he

-- Two independently supplied middle endpoints must actually agree.
def checkedCompose {α : Type u} [DecidableEq α]
    (F G J H R₁ N₁ R₂ N₂ : Finset (Finset α)) :
    Option (Finset (Finset α) × Finset (Finset α)) :=
  if G = J ∧ checkedBoundPatch F G R₁ N₁ = some G ∧
      checkedBoundPatch J H R₂ N₂ = some H
  then some (composeDelta R₁ N₁ R₂ N₂) else none

theorem checked_compose_exact {α : Type u} [DecidableEq α]
    (F G H R₁ N₁ R₂ N₂ : Finset (Finset α))
    (h₁ : checkedBoundPatch F G R₁ N₁ = some G)
    (h₂ : checkedBoundPatch G H R₂ N₂ = some H) :
    checkedCompose F G G H R₁ N₁ R₂ N₂ = some (F \ H, H \ F) := by
  have hv₁ := bound_sound F G R₁ N₁ h₁
  have hv₂ := bound_sound G H R₂ N₂ h₂
  unfold checkedCompose
  calc
    _ = some (composeDelta R₁ N₁ R₂ N₂) := if_pos ⟨rfl, h₁, h₂⟩
    _ = some (F \ H, H \ F) :=
      congrArg some (compose_valid_exact F G H R₁ N₁ R₂ N₂ hv₁.1 hv₁.2 hv₂.1 hv₂.2)

theorem checked_reject_middle {α : Type u} [DecidableEq α]
    (F G J H R₁ N₁ R₂ N₂ : Finset (Finset α)) (h : G ≠ J) :
    checkedCompose F G J H R₁ N₁ R₂ N₂ = none := by
  unfold checkedCompose
  exact if_neg (fun hv => h hv.1)

theorem checked_reject_first {α : Type u} [DecidableEq α]
    (F G J H R₁ N₁ R₂ N₂ : Finset (Finset α))
    (h : checkedBoundPatch F G R₁ N₁ ≠ some G) :
    checkedCompose F G J H R₁ N₁ R₂ N₂ = none := by
  unfold checkedCompose
  exact if_neg (fun hv => h hv.2.1)

theorem checked_reject_second {α : Type u} [DecidableEq α]
    (F G J H R₁ N₁ R₂ N₂ : Finset (Finset α))
    (h : checkedBoundPatch J H R₂ N₂ ≠ some H) :
    checkedCompose F G J H R₁ N₁ R₂ N₂ = none := by
  unfold checkedCompose
  exact if_neg (fun hv => h hv.2.2)

theorem checked_compose_sound {α : Type u} [DecidableEq α]
    (F G J H R₁ N₁ R₂ N₂ : Finset (Finset α))
    (P : Finset (Finset α) × Finset (Finset α))
    (hs : checkedCompose F G J H R₁ N₁ R₂ N₂ = some P) :
    G = J ∧ P = (F \ H, H \ F) := by
  have hv : G = J ∧ checkedBoundPatch F G R₁ N₁ = some G ∧
      checkedBoundPatch J H R₂ N₂ = some H := by
    by_contra hn
    unfold checkedCompose at hs
    have he : (none : Option (Finset (Finset α) × Finset (Finset α))) = some P :=
      (if_neg hn).symm.trans hs
    cases he
  obtain ⟨he, h₁, h₂⟩ := hv
  subst J
  exact ⟨rfl, Option.some.inj (hs.symm.trans (checked_compose_exact F G H R₁ N₁ R₂ N₂ h₁ h₂))⟩

theorem checked_compose_replay {α : Type u} [DecidableEq α]
    (F G J H R₁ N₁ R₂ N₂ : Finset (Finset α))
    (P : Finset (Finset α) × Finset (Finset α))
    (hs : checkedCompose F G J H R₁ N₁ R₂ N₂ = some P) :
    checkedBoundPatch F H P.1 P.2 = some H ∧
      checkedBoundPatch H F P.2 P.1 = some F := by
  have he := (checked_compose_sound F G J H R₁ N₁ R₂ N₂ P hs).2
  subst P
  exact ⟨checked_bound_exact F H, checked_bound_exact H F⟩

theorem compose_three_associative {α : Type u} [DecidableEq α]
    (F G H J : Finset (Finset α)) :
    composeDelta (composeDelta (F \ G) (G \ F) (G \ H) (H \ G)).1
      (composeDelta (F \ G) (G \ F) (G \ H) (H \ G)).2 (H \ J) (J \ H) =
    composeDelta (F \ G) (G \ F)
      (composeDelta (G \ H) (H \ G) (H \ J) (J \ H)).1
      (composeDelta (G \ H) (H \ G) (H \ J) (J \ H)).2 := by
  calc
    _ = composeDelta (F \ H) (H \ F) (H \ J) (J \ H) :=
      congrArg (fun p => composeDelta p.1 p.2 (H \ J) (J \ H)) (compose_diff_exact F G H)
    _ = (F \ J, J \ F) := compose_diff_exact F H J
    _ = composeDelta (F \ G) (G \ F) (G \ J) (J \ G) :=
      (compose_diff_exact F G J).symm
    _ = _ :=
      (congrArg (fun p => composeDelta (F \ G) (G \ F) p.1 p.2) (compose_diff_exact G H J)).symm

theorem checked_compose_cycle {α : Type u} [DecidableEq α]
    (F G : Finset (Finset α)) :
    checkedCompose F G G F (F \ G) (G \ F) (G \ F) (F \ G) =
      some ((∅ : Finset (Finset α)), (∅ : Finset (Finset α))) := by
  calc
    _ = some (F \ F, F \ F) :=
      checked_compose_exact F G F (F \ G) (G \ F) (G \ F) (F \ G)
        (checked_bound_exact F G) (checked_bound_exact G F)
    _ = _ := by simp

end KuuOSR68
