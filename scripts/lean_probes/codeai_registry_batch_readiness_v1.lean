/- R74: characterize admissible fresh batches and permutation invariance.
Only the candidate registry is order-independent; receipt and execution
history must still be retained. No live registration authority follows. -/
namespace KuuOSR74
open KuuOSR67 KuuOSR68 KuuOSR69 KuuOSR70 KuuOSR71 KuuOSR72 KuuOSR73
universe u v

def BatchReady {κ : Type v} {α : Type u}
    (reg : κ → Option (Basis α)) (bs : List (κ × Basis α)) : Prop :=
  (∀ b ∈ bs, reg b.1 = none) ∧ (bs.map Prod.fst).Nodup

def batchReadyCheck {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (bs : List (κ × Basis α)) : Bool :=
  bs.all (fun b => decide (reg b.1 = none)) && decide ((bs.map Prod.fst).Nodup)

theorem batch_ready_check_iff {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (bs : List (κ × Basis α)) :
    batchReadyCheck reg bs = true ↔ BatchReady reg bs := by
  simp only [batchReadyCheck, BatchReady, Bool.and_eq_true, List.all_eq_true, decide_eq_true_eq]

theorem batch_ready_tail {κ : Type v} {α : Type u} [DecidableEq κ]
    (reg : κ → Option (Basis α)) (a : κ × Basis α) (tail : List (κ × Basis α))
    (h : BatchReady reg (a :: tail)) :
    BatchReady (setBinding reg a.1 a.2) tail := by
  have hn : (a.1 :: tail.map Prod.fst).Nodup := h.2
  obtain ⟨hn, hd⟩ := List.nodup_cons.mp hn
  refine ⟨?_, hd⟩
  intro b hb
  have hne : b.1 ≠ a.1 := by
    intro he
    exact hn (List.mem_map.mpr ⟨b,hb,he⟩)
  unfold setBinding
  exact (if_neg hne).trans (h.1 b (List.mem_cons.mpr (Or.inr hb)))

theorem checked_batch_ready {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (bs : List (κ × Basis α))
    (hs : checkedBatch reg bs = some next) : BatchReady reg bs := by
  induction bs generalizing reg with
  | nil =>
      refine ⟨?_, List.nodup_nil⟩
      intro b hb
      cases hb
  | cons a tail ih =>
      have hf : ∀ b ∈ a :: tail, reg b.1 = none := by
        intro b hb
        cases he : reg b.1 with
        | none => rfl
        | some G =>
            have hbad := checked_batch_reject_present reg (a :: tail) b hb G he
            have impossible : (none : Option (κ → Option (Basis α))) = some next :=
              hbad.symm.trans hs
            cases impossible
      have hn : a.1 ∉ tail.map Prod.fst := by
        intro hm
        obtain ⟨b,hb,he⟩ := List.mem_map.mp hm
        have hbad := checked_batch_reject_duplicate_head reg a b tail hb he.symm
        have impossible : (none : Option (κ → Option (Basis α))) = some next :=
          hbad.symm.trans hs
        cases impossible
      have ht : checkedBatch (setBinding reg a.1 a.2) tail = some next :=
        (checked_batch_cons reg a tail (hf a List.mem_cons_self)).symm.trans hs
      have hr := ih (setBinding reg a.1 a.2) ht
      refine ⟨hf, ?_⟩
      change (a.1 :: tail.map Prod.fst).Nodup
      exact List.nodup_cons.mpr ⟨hn,hr.2⟩

theorem checked_batch_exists {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (bs : List (κ × Basis α))
    (h : BatchReady reg bs) : ∃ next, checkedBatch reg bs = some next := by
  induction bs generalizing reg with
  | nil => exact ⟨reg, checked_batch_nil reg⟩
  | cons a tail ih =>
      obtain ⟨next, ht⟩ := ih (setBinding reg a.1 a.2) (batch_ready_tail reg a tail h)
      exact ⟨next, (checked_batch_cons reg a tail (h.1 a List.mem_cons_self)).trans ht⟩

theorem checked_batch_success_iff {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (bs : List (κ × Basis α)) :
    (∃ next, checkedBatch reg bs = some next) ↔ BatchReady reg bs := by
  constructor
  · rintro ⟨next,hs⟩
    exact checked_batch_ready reg next bs hs
  · exact checked_batch_exists reg bs

theorem checked_batch_frame {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (bs : List (κ × Basis α)) (k : κ)
    (hs : checkedBatch reg bs = some next) (ha : ∀ b ∈ bs, k ≠ b.1) :
    next k = reg k := by
  induction bs generalizing reg with
  | nil =>
      have he : reg = next := Option.some.inj hs
      subst next
      rfl
  | cons a tail ih =>
      have hr := checked_batch_ready reg next (a :: tail) hs
      have ht : checkedBatch (setBinding reg a.1 a.2) tail = some next :=
        (checked_batch_cons reg a tail (hr.1 a List.mem_cons_self)).symm.trans hs
      calc
        next k = setBinding reg a.1 a.2 k :=
          ih (setBinding reg a.1 a.2) ht (fun b hb => ha b (List.mem_cons.mpr (Or.inr hb)))
        _ = reg k := by
          unfold setBinding
          exact if_neg (ha a List.mem_cons_self)

theorem batch_ready_perm {κ : Type v} {α : Type u}
    (reg : κ → Option (Basis α)) (xs ys : List (κ × Basis α))
    (hp : List.Perm xs ys) (hr : BatchReady reg xs) : BatchReady reg ys :=
  ⟨fun b hb => hr.1 b (hp.mem_iff.mpr hb), (hp.map Prod.fst).nodup_iff.mp hr.2⟩

theorem checked_batch_same_graph {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg X Y : κ → Option (Basis α)) (xs ys : List (κ × Basis α))
    (hg : ∀ b, b ∈ xs ↔ b ∈ ys)
    (hx : checkedBatch reg xs = some X) (hy : checkedBatch reg ys = some Y) :
    X = Y := by
  funext k
  classical
  by_cases hm : ∃ b ∈ xs, b.1 = k
  · obtain ⟨b,hb,he⟩ := hm
    have hX := checked_batch_contains reg X xs hx b hb
    have hY := checked_batch_contains reg Y ys hy b ((hg b).mp hb)
    rw [← he]
    exact hX.trans hY.symm
  · have ha : ∀ b ∈ xs, k ≠ b.1 := by
      intro b hb he
      exact hm ⟨b,hb,he.symm⟩
    have hb : ∀ b ∈ ys, k ≠ b.1 :=
      fun b hb => ha b ((hg b).mpr hb)
    exact (checked_batch_frame reg X xs k hx ha).trans
      (checked_batch_frame reg Y ys k hy hb).symm

theorem checked_batch_perm {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (xs ys : List (κ × Basis α)) (hp : List.Perm xs ys) :
    checkedBatch reg xs = checkedBatch reg ys := by
  cases hx : checkedBatch reg xs with
  | none =>
      cases hy : checkedBatch reg ys with
      | none => rfl
      | some Y =>
          have hr := batch_ready_perm reg ys xs hp.symm (checked_batch_ready reg Y ys hy)
          obtain ⟨X,hX⟩ := checked_batch_exists reg xs hr
          have impossible : (none : Option (κ → Option (Basis α))) = some X :=
            hx.symm.trans hX
          cases impossible
  | some X =>
      have hr := batch_ready_perm reg xs ys hp (checked_batch_ready reg X xs hx)
      obtain ⟨Y,hY⟩ := checked_batch_exists reg ys hr
      have he := checked_batch_same_graph reg X Y xs ys (fun b => hp.mem_iff) hx hY
      exact (congrArg some he).trans hY.symm

theorem checked_batch_hold_iff {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (bs : List (κ × Basis α)) :
    checkedBatch reg bs = none ↔ ¬ BatchReady reg bs := by
  constructor
  · intro hn hr
    obtain ⟨next,hs⟩ := checked_batch_exists reg bs hr
    have impossible : (none : Option (κ → Option (Basis α))) = some next :=
      hn.symm.trans hs
    cases impossible
  · intro hn
    cases hs : checkedBatch reg bs with
    | none => rfl
    | some next => exact False.elim (hn (checked_batch_ready reg next bs hs))

end KuuOSR74
