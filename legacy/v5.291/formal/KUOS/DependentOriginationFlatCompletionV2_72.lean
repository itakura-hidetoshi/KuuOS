import KUOS.DependentOriginationCorrectionGainV2_71

namespace KUOS.DependentOriginationFlatCompletionV2_72

open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration
open KUOS.DependentOriginationCorrectionGainV2_71

universe u v

/-!
# Flat completion / limit descent v2.72

This layer accepts an explicit infinite correction history and an explicit
limit-transfer datum. It does not derive an infinite history from the finite
existence theorem of v2.71 and does not assume any topology or completeness.
-/

/-- An explicit infinite correction history with exact invariant preservation
and certified linearly improving residual order. -/
structure FilteredCorrectionTower
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    (Step : State → State → Prop)
    (δ n₀ : ℕ) where
  state : ℕ → State
  invariant : ∀ n, P.invariant (state n)
  step : ∀ n, Step (state n) (state (n + 1))
  order : ∀ n,
    F.OrderAtLeast (n₀ + n * δ) (P.residual (state n))

namespace FilteredCorrectionTower

/-- Positive linear gain implies that every fixed filtration level is reached
and then retained by all sufficiently late stages of the explicit tower. -/
theorem eventually_orderAtLeast
    {State : Type u} {D : Type v}
    {F : ObstructionFiltration D}
    {P : ResidualProblem State D}
    {Step : State → State → Prop}
    {δ n₀ : ℕ}
    (T : FilteredCorrectionTower F P Step δ n₀)
    (hδ : 0 < δ) (k : ℕ) :
    ∃ N, ∀ n ≥ N,
      F.OrderAtLeast k (P.residual (T.state n)) := by
  refine ⟨k, ?_⟩
  intro n hn
  have hδ1 : 1 ≤ δ := hδ
  have hmul : n ≤ n * δ := by
    simpa using Nat.mul_le_mul_left n hδ1
  have hk : k ≤ n₀ + n * δ := by
    omega
  exact F.orderAtLeast_mono hk (T.order n)

end FilteredCorrectionTower

/-- Explicit authority boundary from an asymptotic correction history to one
actual completed state. No generic existence of this datum is asserted. -/
structure ResidualLimitData
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    {Step : State → State → Prop} {δ n₀ : ℕ}
    (T : FilteredCorrectionTower F P Step δ n₀) where
  limitState : State
  invariant_limit : P.invariant limitState
  level_limit :
    ∀ k,
      (∃ N, ∀ n ≥ N,
        F.OrderAtLeast k (P.residual (T.state n))) →
      F.OrderAtLeast k (P.residual limitState)

/-- An explicit positive-gain tower plus an explicit level-transfer limit datum
produces an exact-invariant state whose residual is flat. -/
theorem limit_invariant_and_flat
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    {Step : State → State → Prop} {δ n₀ : ℕ}
    (T : FilteredCorrectionTower F P Step δ n₀)
    (L : ResidualLimitData F P T)
    (hδ : 0 < δ) :
    P.invariant L.limitState ∧
      F.Flat (P.residual L.limitState) := by
  refine ⟨L.invariant_limit, ?_⟩
  intro k
  exact L.level_limit k (T.eventually_orderAtLeast hδ k)

/-- Exact residual triviality is obtained only after adding separatedness at a
distinguished exact defect. -/
theorem limit_residual_eq_of_separatedAt
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    {Step : State → State → Prop} {δ n₀ : ℕ}
    (T : FilteredCorrectionTower F P Step δ n₀)
    (L : ResidualLimitData F P T)
    (hδ : 0 < δ)
    {e : D}
    (hsep : F.SeparatedAt e) :
    P.residual L.limitState = e := by
  exact F.flat_eq_of_separatedAt hsep
    (limit_invariant_and_flat F P T L hδ).2

end KUOS.DependentOriginationFlatCompletionV2_72
