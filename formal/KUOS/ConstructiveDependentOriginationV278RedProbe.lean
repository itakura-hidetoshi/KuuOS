import KUOS.DependentOriginationResidualStabilityV2_78

namespace KUOS.DependentOriginationResidualStabilityV2_78

open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationCorrectionGainV2_71
open KUOS.DependentOriginationCofinalCorrectionV2_77
open KUOS.DependentOriginationTowerRealizationV2_78

universe u v

variable
    {State : Type u} {D : Type v}
    {F : ObstructionFiltration D}
    {P : ResidualProblem State D}
    {Step : State → State → Prop}
    {g : Nat → Nat}
    (T : CofinalCorrectionTower F P Step g)
    (Approx : Nat → State → State → Prop)
    (L : TowerRealization T Approx)

example
    (S : ResidualStabilityTransfer T Approx L) :
    F.Flat (P.residual L.limitState) :=
  (realized_invariant_and_flat F P T Approx L S).2

end KUOS.DependentOriginationResidualStabilityV2_78
