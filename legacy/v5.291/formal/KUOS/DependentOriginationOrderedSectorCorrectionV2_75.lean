import KUOS.DependentOriginationCorrectionRealizationV2_74

namespace KUOS.DependentOriginationOrderedSectorCorrectionV2_75

universe u

/-!
# Ordered sector correction v2.75

A correction cycle may act on several residual sectors in a prescribed finite
order. Each selected correction improves its active sector while preserving
all other sectors at whatever order has already been established.

The selected corrector and schedule are explicit data. This layer derives no
canonical corrector from existential correctability and constructs no infinite
iteration.
-/

/-- Independent sector predicates indexed by required filtration/order level. -/
structure SectorOrderData (State : Type u) (r : ℕ) where
  good : Fin r → ℕ → State → Prop
  weaken :
    ∀ i {m n : ℕ} {x : State},
      m ≤ n → good i n x → good i m x

/-- A selected finite-sector correction mechanism. -/
structure OrderedSectorCorrector
    {State : Type u} {r : ℕ}
    (S : SectorOrderData State r)
    (Invariant : State → Prop)
    (Step : Fin r → State → State → Prop)
    (δ : ℕ) where
  correct : Fin r → State → State
  step : ∀ i x, Step i x (correct i x)
  invariant :
    ∀ i x, Invariant x → Invariant (correct i x)
  gain :
    ∀ i x n,
      Invariant x →
      S.good i n x →
      S.good i (n + δ) (correct i x)
  preserve_other :
    ∀ i j m x,
      j ≠ i →
      S.good j m x →
      S.good j m (correct i x)

namespace OrderedSectorCorrector

variable
    {State : Type u} {r δ : ℕ}
    {S : SectorOrderData State r}
    {Invariant : State → Prop}
    {Step : Fin r → State → State → Prop}

/-- Execute an explicit finite list of sector corrections from left to right. -/
def runSchedule
    (C : OrderedSectorCorrector S Invariant Step δ) :
    List (Fin r) → State → State
  | [], x => x
  | i :: is, x => runSchedule C is (C.correct i x)

/-- Every selected correction preserves the exact invariant. -/
theorem runSchedule_invariant
    (C : OrderedSectorCorrector S Invariant Step δ)
    (schedule : List (Fin r)) {x : State}
    (hx : Invariant x) :
    Invariant (C.runSchedule schedule x) := by
  induction schedule generalizing x with
  | nil =>
      simpa [runSchedule] using hx
  | cons i is ih =>
      simp only [runSchedule]
      exact ih (C.invariant i x hx)

/-- If a sector is absent from the remaining schedule, its currently certified
order is preserved through every remaining correction. -/
theorem runSchedule_preserves_not_mem
    (C : OrderedSectorCorrector S Invariant Step δ)
    (schedule : List (Fin r))
    {j : Fin r} {m : ℕ} {x : State}
    (hj : j ∉ schedule)
    (hgood : S.good j m x) :
    S.good j m (C.runSchedule schedule x) := by
  induction schedule generalizing x with
  | nil =>
      simpa [runSchedule] using hgood
  | cons i is ih =>
      have hji : j ≠ i := by
        intro h
        subst i
        exact hj (by simp)
      have hjtail : j ∉ is := by
        intro h
        exact hj (by simp [h])
      simp only [runSchedule]
      exact ih hjtail (C.preserve_other i j m x hji hgood)

/-- In a duplicate-free schedule, a sector that occurs in the schedule reaches
the one-cycle improved order and retains it through all later corrections. -/
theorem runSchedule_gain_of_mem
    (C : OrderedSectorCorrector S Invariant Step δ)
    (schedule : List (Fin r))
    (hnodup : schedule.Nodup)
    {x : State} {n : ℕ}
    (hxinv : Invariant x)
    (hxbase : ∀ j, S.good j n x)
    {j : Fin r}
    (hj : j ∈ schedule) :
    S.good j (n + δ) (C.runSchedule schedule x) := by
  induction schedule generalizing x with
  | nil =>
      simp at hj
  | cons i is ih =>
      have hitail : i ∉ is := (List.nodup_cons.mp hnodup).1
      have htailnodup : is.Nodup := (List.nodup_cons.mp hnodup).2
      have hx1inv : Invariant (C.correct i x) :=
        C.invariant i x hxinv
      have hx1base : ∀ k, S.good k n (C.correct i x) := by
        intro k
        by_cases hki : k = i
        · subst k
          exact S.weaken i (by omega)
            (C.gain i x n hxinv (hxbase i))
        · exact C.preserve_other i k n x hki (hxbase k)
      simp only [runSchedule]
      by_cases hji : j = i
      · subst j
        exact C.runSchedule_preserves_not_mem is hitail
          (C.gain i x n hxinv (hxbase i))
      · have hjtail : j ∈ is := by
          simpa [hji] using hj
        exact ih htailnodup hx1inv hx1base hjtail

/-- A duplicate-free schedule covering every sector raises every sector by the
same certified one-cycle gain. -/
theorem runFullCycle_order
    (C : OrderedSectorCorrector S Invariant Step δ)
    (schedule : List (Fin r))
    (hnodup : schedule.Nodup)
    {x : State} {n : ℕ}
    (hxinv : Invariant x)
    (hcover : ∀ j, j ∈ schedule)
    (hxbase : ∀ j, S.good j n x) :
    ∀ j, S.good j (n + δ) (C.runSchedule schedule x) := by
  intro j
  exact C.runSchedule_gain_of_mem schedule hnodup hxinv hxbase (hcover j)

end OrderedSectorCorrector

end KUOS.DependentOriginationOrderedSectorCorrectionV2_75
