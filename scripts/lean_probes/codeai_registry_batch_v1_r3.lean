/- R73: checked atomic batches of fresh registry bindings.
No write to a live registry is implied by this pure candidate function.
Failure returns no candidate; prior receipts and historical HOLDs persist. -/
namespace KuuOSR73
open KuuOSR67 KuuOSR68 KuuOSR69 KuuOSR70 KuuOSR71 KuuOSR72
universe u v

def checkedBatch {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α] :
    (κ → Option (Basis α)) → List (κ × Basis α) → Option (κ → Option (Basis α))
  | reg, [] => some reg
  | reg, b :: tail =>
      match checkedInsert reg b.1 b.2 with
      | none => none
      | some mid => checkedBatch mid tail

theorem checked_batch_nil {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) :
    checkedBatch reg [] = some reg := rfl

theorem checked_batch_cons {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (b : κ × Basis α) (tail : List (κ × Basis α))
    (h : reg b.1 = none) :
    checkedBatch reg (b :: tail) = checkedBatch (setBinding reg b.1 b.2) tail := by
  rw [checkedBatch, checked_insert_fresh reg b.1 b.2 h]

theorem checked_batch_extends {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (bs : List (κ × Basis α))
    (hs : checkedBatch reg bs = some next) : RegistryExtends reg next := by
  induction bs generalizing reg with
  | nil =>
      have he : reg = next := Option.some.inj hs
      subst next
      exact extends_refl reg
  | cons b tail ih =>
      unfold checkedBatch at hs
      cases hm : checkedInsert reg b.1 b.2 with
      | none =>
          rw [hm] at hs
          cases hs
      | some mid =>
          rw [hm] at hs
          exact extends_trans reg mid next (checked_insert_sound reg mid b.1 b.2 hm).2.1
            (ih mid hs)

theorem checked_batch_contains {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (bs : List (κ × Basis α))
    (hs : checkedBatch reg bs = some next) (b : κ × Basis α) (hb : b ∈ bs) :
    next b.1 = some b.2 := by
  induction bs generalizing reg with
  | nil => cases hb
  | cons a tail ih =>
      unfold checkedBatch at hs
      cases hm : checkedInsert reg a.1 a.2 with
      | none =>
          rw [hm] at hs
          cases hs
      | some mid =>
          rw [hm] at hs
          rcases List.mem_cons.mp hb with he | ht
          · subst b
            exact checked_batch_extends mid next tail hs a.1 a.2
              (checked_insert_sound reg mid a.1 a.2 hm).2.2
          · exact ih mid hs ht

theorem checked_batch_reject_present {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (bs : List (κ × Basis α))
    (b : κ × Basis α) (hb : b ∈ bs) (G : Basis α) (h : reg b.1 = some G) :
    checkedBatch reg bs = none := by
  induction bs generalizing reg with
  | nil => cases hb
  | cons a tail ih =>
      unfold checkedBatch
      cases hm : checkedInsert reg a.1 a.2 with
      | none => rfl
      | some mid =>
          rcases List.mem_cons.mp hb with he | ht
          · subst b
            have impossible : (none : Option (Basis α)) = some G :=
              (checked_insert_sound reg mid a.1 a.2 hm).1.symm.trans h
            cases impossible
          · exact ih mid ht ((checked_insert_sound reg mid a.1 a.2 hm).2.1 b.1 G h)

theorem checked_batch_reject_duplicate_head {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (a b : κ × Basis α) (tail : List (κ × Basis α))
    (hb : b ∈ tail) (he : a.1 = b.1) :
    checkedBatch reg (a :: tail) = none := by
  unfold checkedBatch
  cases hm : checkedInsert reg a.1 a.2 with
  | none => rfl
  | some mid =>
      have h : mid b.1 = some a.2 := by
        rw [← he]
        exact (checked_insert_sound reg mid a.1 a.2 hm).2.2
      exact checked_batch_reject_present mid tail b hb a.2 h

theorem checked_batch_append {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (xs ys : List (κ × Basis α)) :
    checkedBatch reg (xs ++ ys) =
      (checkedBatch reg xs).bind (fun mid => checkedBatch mid ys) := by
  induction xs generalizing reg with
  | nil => rfl
  | cons a tail ih =>
      change checkedBatch reg (a :: (tail ++ ys)) =
        (checkedBatch reg (a :: tail)).bind (fun mid => checkedBatch mid ys)
      cases hm : checkedInsert reg a.1 a.2 with
      | none =>
          have hl : checkedBatch reg (a :: (tail ++ ys)) = none := by
            rw [checkedBatch, hm]
          have hr : checkedBatch reg (a :: tail) = none := by
            rw [checkedBatch, hm]
          rw [hl, hr]
          exact (Option.bind_none (fun mid : κ → Option (Basis α) => checkedBatch mid ys)).symm
      | some mid =>
          have hl : checkedBatch reg (a :: (tail ++ ys)) = checkedBatch mid (tail ++ ys) := by
            rw [checkedBatch, hm]
          have hr : checkedBatch reg (a :: tail) = checkedBatch mid tail := by
            rw [checkedBatch, hm]
          rw [hl, hr]
          exact ih mid

theorem checked_batch_preserves_path {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (bs : List (κ × Basis α))
    (k l : κ) (F H : Basis α) (path : List (TaggedStep κ α)) (P : Delta α)
    (hb : checkedBatch reg bs = some next)
    (hp : checkedRegisteredPath reg k l F H path = some P) :
    checkedRegisteredPath next k l F H path = some P :=
  checked_registered_mono reg next k l F H path P (checked_batch_extends reg next bs hb) hp

theorem checked_batch_recovers_identity {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (bs : List (κ × Basis α)) (k : κ) (F : Basis α)
    (hb : checkedBatch reg bs = some next) (hm : (k,F) ∈ bs) (hf : reg k = none) :
    checkedRegisteredPath reg k k F F [] = none ∧
      checkedRegisteredPath next k k F F [] = some ((∅ : Basis α), (∅ : Basis α)) := by
  refine ⟨(unknown_key_alias reg k F hf).2, ?_⟩
  have h := checked_batch_contains reg next bs hb (k,F) hm
  calc
    _ = some (F \ F, F \ F) :=
      checked_registered_of_checks next k k F F [] _ h h rfl
        (checked_tagged_exact k k F F [] rfl rfl)
    _ = _ := by simp

theorem checked_batch_two_fresh {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (k l : κ) (F G : Basis α)
    (hk : reg k = none) (hl : reg l = none) (hne : l ≠ k) :
    checkedBatch reg [(k,F),(l,G)] = some (setBinding (setBinding reg k F) l G) := by
  have hl' : setBinding reg k F l = none := by
    unfold setBinding
    exact (if_neg hne).trans hl
  rw [checked_batch_cons reg (k,F) [(l,G)] hk,
    checked_batch_cons (setBinding reg k F) (l,G) [] hl']
  rfl

end KuuOSR73
