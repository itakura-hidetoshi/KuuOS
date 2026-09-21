import KUOS.DependentOriginationCofinalCorrectionV2_77

namespace KUOS.DependentOriginationTowerRealizationV2_78

open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationCorrectionGainV2_71
open KUOS.DependentOriginationCofinalCorrectionV2_77

universe u v

/-!
# Tower realization v2.78

A formal cofinal correction tower and an actually realized state are distinct
objects. This module records only realization data: a limit state, preservation
of the exact invariant, and an explicit approximation relation.

No residual flatness theorem is present in this module.
-/

/-- An actual state realizing a supplied formal cofinal correction tower,
together with explicit approximation evidence indexed by the tower's certified
order schedule. -/
structure TowerRealization
    {State : Type u} {D : Type v}
    {F : ObstructionFiltration D}
    {P : ResidualProblem State D}
    {Step : State → State → Prop}
    {g : ℕ → ℕ}
    (T : CofinalCorrectionTower F P Step g)
    (Approx : ℕ → State → State → Prop) where
  limitState : State
  invariant_limit : P.invariant limitState
  approximation :
    ∀ j, Approx (g j) (T.state j) limitState

end KUOS.DependentOriginationTowerRealizationV2_78
