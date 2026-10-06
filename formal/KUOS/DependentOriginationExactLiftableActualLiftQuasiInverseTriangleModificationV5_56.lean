import KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleV5_55
import Mathlib.CategoryTheory.Bicategory.Modification.Pseudo

namespace KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleModificationV5_56

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleV5_55

set_option autoImplicit false

noncomputable section

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b x y p q : B}

-- Regression specification: the old contraction must be natural for the
-- actual five-isomorphism paste, with all four equivalences independent.
example (ex : Bicategory.Equivalence a x) (ey : Bicategory.Equivalence b y)
    (dx : Bicategory.Equivalence p a) (dy : Bicategory.Equivalence q b)
    (f : x ⟶ y) :
    (Conjugation.homFunctor ex ey).obj f ◁ (ConjugationTriangle.quasiInverseIso ey dy).hom ≫
        (ρ_ ((Conjugation.homFunctor ex ey).obj f)).hom ≫
        (λ_ ((Conjugation.homFunctor ex ey).obj f)).inv =
      (BackwardTriangle.naturalityIso ex ey dx dy f).hom ≫
        (ConjugationTriangle.quasiInverseIso ex dx).hom ▷
          (Conjugation.homFunctor ex ey).obj f :=
  BackwardTriangleCoherence.naturality ex ey dx dy f

end

end KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleModificationV5_56
