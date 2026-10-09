import KUOS.DependentOriginationReverseSwallowtailPointwiseBoundaryV5_96

namespace KUOS.DependentOriginationReverseConjugationFourCellV5_98

open CategoryTheory
open scoped CategoryTheory.Bicategory
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51

set_option autoImplicit false
set_option maxHeartbeats 500000
noncomputable section

/-!
# Genuine reverse four-cell and its triangle components (v5.98)

The F4 target/counit interchanger specializes to two distinct original
adjoint equivalences e : a ≌ x and d : b ≌ a, with no equality between
their chosen object presentations. The original strict F.mapComp becomes
the existing identity comparison, not an additional coherence axiom.

This file exposes both sides of the remaining F4 equation using native
ConjugationUnit/ConjugationCounit cells and the left triangle of e.
These are genuine typed bicategorical calculations, not replacements
of the original G or triangulator data. It does NOT assert F4.
-/

universe uB vB wB

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b x : B}

/-- The original target counit-centered interchanger, with nontrivial
source equivalence d and target equivalence e retained separately. -/
def reverseConjugationFourCell
    (e : Bicategory.Equivalence a x)
    (d : Bicategory.Equivalence b a) :
    (d.inv ≫ d.hom) ≫ e.hom ≅
      (d.inv ≫ (Conjugation.homFunctor d e).obj e.hom) ≫ e.hom :=
  (α_ d.inv d.hom e.hom) ≪≫
    Bicategory.whiskerLeftIso d.inv
      (ConjugationCounit.naturalityIso d e e.hom).symm ≪≫
    (α_ d.inv ((Conjugation.homFunctor d e).obj e.hom) e.hom).symm

/-- Expanded hom of exactly the original counit four-cell, without
strictifying the conjugation image or using a triangle identity. -/
theorem reverseConjugationFourCell_hom
    (e : Bicategory.Equivalence a x)
    (d : Bicategory.Equivalence b a) :
    (reverseConjugationFourCell e d).hom =
      (α_ d.inv d.hom e.hom).hom ≫
        (d.inv ◁ (ConjugationCounit.naturalityIso d e e.hom).inv) ≫
          (α_ d.inv ((Conjugation.homFunctor d e).obj e.hom) e.hom).inv :=
  rfl

/-- The unchanged reverse contraction inverse inserts the actual old
unit and its old pseudonaturality; right whiskering by the original
counit component preserves all three factors in this exact order. -/
theorem reverseConjugationTriangle_whiskerRight_expanded
    (e : Bicategory.Equivalence a x)
    (d : Bicategory.Equivalence b a) :
    (d.counit.hom ≫ (ConjugationTriangle.quasiInverseIso e d).inv) ▷ e.hom =
      (d.counit.hom ▷ e.hom) ≫
        ((e.unit.hom ▷ e.hom) ≫
          ((ConjugationUnit.naturalityIso d e e.hom).hom ▷ e.hom)) := by
  rw [ConjugationTriangle.quasiInverseIso_inv,
    Bicategory.comp_whiskerRight, Bicategory.comp_whiskerRight]

/-- The fixed equivalence's genuine left triangle identifies insertion
of its unit before e.hom with insertion of its inverse counit after
e.hom. This is a consequence of e.left_triangle_hom, not a new
mate/coherence axiom. -/
theorem leftTriangle_unit_vs_inverseCounit
    (e : Bicategory.Equivalence a x) :
    (e.unit.hom ▷ e.hom) ≫ (α_ e.hom e.inv e.hom).hom =
      (λ_ e.hom).hom ≫
        ((ρ_ e.hom).inv ≫ (e.hom ◁ e.counit.inv)) := by
  have hleft :
      (e.unit.hom ▷ e.hom) ≫ (α_ e.hom e.inv e.hom).hom ≫
          (e.hom ◁ e.counit.hom) =
        (λ_ e.hom).hom ≫ (ρ_ e.hom).inv := by
    calc
      _ = Bicategory.leftZigzag e.unit.hom e.counit.hom := by
        dsimp only [Bicategory.leftZigzag]
        bicategory
      _ = _ := e.left_triangle_hom
  have h := congrArg (fun k => k ≫ (e.hom ◁ e.counit.inv)) hleft
  simpa only [Category.assoc, Bicategory.whiskerLeft_hom_inv,
    Category.comp_id] using h

#print axioms reverseConjugationFourCell
#print axioms reverseConjugationFourCell_hom
#print axioms reverseConjugationTriangle_whiskerRight_expanded
#print axioms leftTriangle_unit_vs_inverseCounit

end

end KUOS.DependentOriginationReverseConjugationFourCellV5_98
