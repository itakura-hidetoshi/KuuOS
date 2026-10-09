import KUOS.DependentOriginationReverseConjugationFourCellV5_98

namespace KUOS.DependentOriginationReverseConjugationFourCellTriangleV5_99

open CategoryTheory
open scoped CategoryTheory.Bicategory
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51
open KUOS.DependentOriginationReverseConjugationFourCellV5_98

set_option autoImplicit false
set_option maxHeartbeats 600000
noncomputable section

/-!
# Exact reverse counit four-cell / triangle contraction coherence (v5.99)

The generic reverse F4 four-cell is built from the original ConjugationCounit
naturality, and its target triangulator contraction side from d.counit,
e.unit and the original ConjugationUnit naturality. The only non-structural
comparison is the stored e.left_triangle_hom.

The two equivalences e : a ≌ x, d : b ≌ a remain DISTINCT.
This theorem attempts the actual generic F4 equality, not an alternate
definition of the residual. No sorry/admit/new axiom or strictification.
-/

universe uB vB wB

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b x : B}

/-- The genuine equivalence's left triangle, explicitly solved for the
unit's right-whiskering. The inverse of the associator is composed on
the right, never hidden in a strictness assumption. -/
theorem leftTriangle_unit_whiskerRight_normal
    (e : Bicategory.Equivalence a x) :
    (e.unit.hom ▷ e.hom) =
      (λ_ e.hom).hom ≫
        ((ρ_ e.hom).inv ≫
          ((e.hom ◁ e.counit.inv) ≫
            (α_ e.hom e.inv e.hom).inv)) := by
  have h := congrArg
    (fun t => t ≫ (α_ e.hom e.inv e.hom).inv)
    (leftTriangle_unit_vs_inverseCounit e)
  simpa only [Category.assoc, Iso.hom_inv_id, Category.comp_id] using h

/-- The genuine reverse four-cell is exactly the unchanged forward
contraction followed by the *inverse* original reverse contraction,
right whiskered by the original target counit. If proved, this is
the generic mathematical kernel needed to discharge F4. -/
theorem reverseConjugationFourCell_cancelled
    (e : Bicategory.Equivalence a x)
    (d : Bicategory.Equivalence b a) :
    (reverseConjugationFourCell e d).hom =
      (d.counit.hom ≫
        (ConjugationTriangle.quasiInverseIso e d).inv) ▷ e.hom := by
  rw [reverseConjugationTriangle_whiskerRight_expanded]
  rw [leftTriangle_unit_whiskerRight_normal]
  simp only [reverseConjugationFourCell_hom]
  dsimp [ConjugationUnit.naturalityIso,
    ConjugationCounit.naturalityIso,
    Conjugation.homFunctor]
  bicategory

#print axioms leftTriangle_unit_whiskerRight_normal
#print axioms reverseConjugationFourCell_cancelled

end

end KUOS.DependentOriginationReverseConjugationFourCellTriangleV5_99
