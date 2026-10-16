import KUOS.DependentOriginationTowerRealizationV2_78

namespace KUOS.DependentOriginationResidualStabilityV2_78

open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration
open KUOS.DependentOriginationCorrectionGainV2_71
open KUOS.DependentOriginationCofinalCorrectionV2_77
open KUOS.DependentOriginationTowerRealizationV2_78

universe u v

/-!
# Residual stability transfer v2.78

A realized state inherits flat residual only through an explicit stability
principle transferring sufficiently strong finite-stage residual order through
the approximation relation. The transfer exposes its fixed filtration loss.
-/

/-- Explicit fixed-loss transfer from a sufficiently strong tower stage to the
residual of the realized state. -/
structure ResidualStabilityTransfer
    {State : Type u} {D : Type v}
    {F : ObstructionFiltration D}
    {P : ResidualProblem State D}
    {Step : State → State → Prop}
    {g : ℕ → ℕ}
    (T : CofinalCorrectionTower F P Step g)
    (Approx : ℕ → State → State → Prop)
    (L : TowerRealization T Approx) where
  loss : ℕ
  transfer :
    ∀ n j,
      n + loss ≤ g j →
      F.OrderAtLeast (g j) (P.residual (T.state j)) →
      Approx (g j) (T.state j) L.limitState →
      F.OrderAtLeast n (P.residual L.limitState)

/-- Cofinality absorbs the fixed stability loss, so explicit realization plus
residual stability gives a flat realized residual. -/
theorem realized_invariant_and_flat
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    {Step : State → State → Prop}
    {g : ℕ → ℕ}
    (T : CofinalCorrectionTower F P Step g)
    (Approx : ℕ → State → State → Prop)
    (L : TowerRealization T Approx)
    (S : ResidualStabilityTransfer T Approx L) :
    P.invariant L.limitState ∧
      F.Flat (P.residual L.limitState) := by
  refine ⟨L.invariant_limit, ?_⟩
  intro n
  obtain ⟨j, hj⟩ :=
    cofinalOrderSchedule_add_loss T.cofinal S.loss n
  exact S.transfer n j hj (T.order j) (L.approximation j)

/-- Exact residual identity follows only after adding separatedness at the
chosen exact defect. -/
theorem realized_residual_eq_of_separatedAt
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    {Step : State → State → Prop}
    {g : ℕ → ℕ}
    (T : CofinalCorrectionTower F P Step g)
    (Approx : ℕ → State → State → Prop)
    (L : TowerRealization T Approx)
    (S : ResidualStabilityTransfer T Approx L)
    {e : D}
    (hsep : F.SeparatedAt e) :
    P.residual L.limitState = e := by
  exact F.flat_eq_of_separatedAt hsep
    (realized_invariant_and_flat F P T Approx L S).2

end KUOS.DependentOriginationResidualStabilityV2_78
