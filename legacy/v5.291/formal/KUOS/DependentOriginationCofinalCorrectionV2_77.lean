import KUOS.DependentOriginationCorrectionGainV2_71

namespace KUOS.DependentOriginationCofinalCorrectionV2_77

open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration
open KUOS.DependentOriginationCorrectionGainV2_71

universe u v

/-!
# Cofinal correction schedules v2.77

A correction history need not improve its certified filtration order
monotonically. For flatness arguments with fixed losses it is enough, at this
layer, to record that arbitrarily large certified orders occur somewhere in
the supplied tower.

This module therefore uses an unbounded/cofinal schedule rather than eventual
domination. Existence of the infinite tower remains explicit data.
-/

/-- The schedule reaches arbitrarily large certified orders. It need not be
monotone and need not eventually remain above a fixed bound. -/
def CofinalOrderSchedule (g : ℕ → ℕ) : Prop :=
  ∀ N, ∃ j, N ≤ g j

/-- Cofinality can absorb any explicitly fixed finite loss at the stage
selection step. -/
theorem cofinalOrderSchedule_add_loss
    {g : ℕ → ℕ}
    (hg : CofinalOrderSchedule g)
    (loss N : ℕ) :
    ∃ j, N + loss ≤ g j :=
  hg (N + loss)

/-- Explicit infinite correction history carrying a cofinal order schedule.
This structure is data; it is not constructed from finite correction gain. -/
structure CofinalCorrectionTower
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    (Step : State → State → Prop)
    (g : ℕ → ℕ) where
  state : ℕ → State
  invariant : ∀ j, P.invariant (state j)
  step : ∀ j, Step (state j) (state (j + 1))
  order : ∀ j, F.OrderAtLeast (g j) (P.residual (state j))
  cofinal : CofinalOrderSchedule g

namespace CofinalCorrectionTower

/-- Every requested finite obstruction order is attained at some stage. -/
theorem exists_stage_orderAtLeast
    {State : Type u} {D : Type v}
    {F : ObstructionFiltration D}
    {P : ResidualProblem State D}
    {Step : State → State → Prop}
    {g : ℕ → ℕ}
    (T : CofinalCorrectionTower F P Step g)
    (N : ℕ) :
    ∃ j, F.OrderAtLeast N (P.residual (T.state j)) := by
  obtain ⟨j, hj⟩ := T.cofinal N
  exact ⟨j, F.orderAtLeast_mono hj (T.order j)⟩

/-- For a fixed loss, choose a stage whose certified order dominates the
requested output order plus that loss. -/
theorem exists_stage_orderAtLeast_with_loss
    {State : Type u} {D : Type v}
    {F : ObstructionFiltration D}
    {P : ResidualProblem State D}
    {Step : State → State → Prop}
    {g : ℕ → ℕ}
    (T : CofinalCorrectionTower F P Step g)
    (loss N : ℕ) :
    ∃ j,
      N + loss ≤ g j ∧
      F.OrderAtLeast (g j) (P.residual (T.state j)) := by
  obtain ⟨j, hj⟩ := cofinalOrderSchedule_add_loss T.cofinal loss N
  exact ⟨j, hj, T.order j⟩

end CofinalCorrectionTower

end KUOS.DependentOriginationCofinalCorrectionV2_77
