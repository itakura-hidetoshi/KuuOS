import KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49

namespace KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48

set_option autoImplicit false

noncomputable section

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

-- Regression specification: the unit must belong to the actual v5.42/v5.48
-- pair, in the source direction, without replacing either pseudofunctor.
example : Pseudofunctor.StrongTrans
    (Pseudofunctor.id
      (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    (Pseudofunctor.comp
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor
      (actualLiftQuasiInversePseudofunctor (W := W) A)) :=
  actualLiftSourceRoundtripUnit (W := W) A

end

end KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
