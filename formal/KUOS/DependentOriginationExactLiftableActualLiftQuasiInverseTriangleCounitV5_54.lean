import Mathlib.CategoryTheory.Bicategory.NaturalTransformation.Pseudo

namespace KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleCounitV5_54

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

-- Regression specification: postcompose a counit by an arbitrary, non-strict H.
example (H : Pseudofunctor B C) (R : Pseudofunctor B B)
    (eps : Pseudofunctor.StrongTrans R (Pseudofunctor.id B)) :
    Pseudofunctor.StrongTrans (Pseudofunctor.comp R H) H :=
  CounitPostcomposition.strongTrans H eps

end

end KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleCounitV5_54
