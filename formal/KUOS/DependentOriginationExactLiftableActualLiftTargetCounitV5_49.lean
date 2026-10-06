import KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
import KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42
import Mathlib.CategoryTheory.Bicategory.NaturalTransformation.Pseudo

namespace KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48

set_option autoImplicit false

noncomputable section

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

-- Regression specification: the new result must inhabit the native StrongTrans
-- for the actual v5.42/v5.48 pair, not an unrelated old roundtrip.
example : Pseudofunctor.StrongTrans
    (Pseudofunctor.comp
      (actualLiftQuasiInversePseudofunctor (W := W) A)
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor)
    (Pseudofunctor.id
      (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)) :=
  actualLiftTargetRoundtripCounit (W := W) A

end

end KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
