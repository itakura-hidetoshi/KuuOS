import Mathlib.CategoryTheory.Bicategory.NaturalTransformation.Pseudo

namespace KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleUnitV5_53

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

universe uD vD wD uB vB wB
variable {D : Type uD} [Bicategory.{wD, vD} D]
variable {B : Type uB} [Bicategory.{wB, vB} B]

-- Regression-only specification: the precomposing functor need not be strict.
example (H : Pseudofunctor D B) (R : Pseudofunctor B B)
    (eta : Pseudofunctor.StrongTrans (Pseudofunctor.id B) R) :
    Pseudofunctor.StrongTrans H (Pseudofunctor.comp H R) :=
  UnitPrecomposition.strongTrans H eta

end

end KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleUnitV5_53
