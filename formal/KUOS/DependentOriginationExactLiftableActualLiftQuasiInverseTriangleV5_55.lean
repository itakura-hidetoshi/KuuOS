import KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleCounitV5_54

namespace KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleV5_55

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48

set_option autoImplicit false

noncomputable section

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

-- Regression specification: the actual two factors must form a named native triangle.
example : Pseudofunctor.StrongTrans
    (B := ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (C := ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (actualLiftQuasiInversePseudofunctor (W := W) A)
    (actualLiftQuasiInversePseudofunctor (W := W) A) :=
  actualLiftQuasiInverseTriangle (W := W) A

end

end KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleV5_55
