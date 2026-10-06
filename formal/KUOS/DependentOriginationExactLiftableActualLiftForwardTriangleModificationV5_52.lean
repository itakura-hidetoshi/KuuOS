import KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51
import Mathlib.CategoryTheory.Bicategory.Modification.Pseudo

namespace KUOS.DependentOriginationExactLiftableActualLiftForwardTriangleModificationV5_52

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42

set_option autoImplicit false

noncomputable section

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

-- Regression-only specification. No successful implementation is claimed.
example :
    Pseudofunctor.StrongTrans
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).toPseudofunctor
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).toPseudofunctor :=
  actualLiftForwardTriangle (W := W) A

example :
    actualLiftForwardTriangle (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel) ≅
    Pseudofunctor.StrongTrans.id
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).toPseudofunctor :=
  actualLiftForwardTriangleModificationIso (W := W) A

end

end KUOS.DependentOriginationExactLiftableActualLiftForwardTriangleModificationV5_52
