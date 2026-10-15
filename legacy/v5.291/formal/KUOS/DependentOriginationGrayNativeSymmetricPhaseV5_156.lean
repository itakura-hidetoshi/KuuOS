import KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156

namespace KUOS.DependentOriginationGrayNativeSymmetricPhaseV5_156

open CategoryTheory
open scoped CategoryTheory.MonoidalCategory
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156

set_option autoImplicit false
noncomputable section

/-!
# F59-D / v5.156 — native nontrivial but symmetric Gray braiding

The proven F59-C Mathlib BraidedCategory on the genuinely independent
graded 3-cell groupoid has phase(a,b)=a*b in ZMod 2. Its double
exchange therefore has phase a*b+b*a=2*a*b=0, even though the
individual odd/odd exchange is NOT the identity and has a nonzero
phase invisible to F58's original Int×Int higher-generator charge.

This file upgrades the ACTUAL fixed F59-C braiding to Mathlib's
native SymmetricCategory by a full symmetry proof, and establishes
that the F58 projection from native parallel 3-morphisms is not
injective. It does not assert the unrestricted external Gray-category
of the original F/G/eta/epsilon nor identify the old Stage-II omega.
-/

/-- Exact native mathlib symmetric refinement of the F59-C braiding.
No new braiding is substituted: it reuses the originally proven
nonidentity odd/odd Gray interchanger and its two actual hexagons. -/
instance : SymmetricCategory GrayGrade where
  toBraidedCategory := instBraidedCategoryGrayGrade
  symmetry := by
    intro X Y
    apply GradedThreeCell.ext
    · change (0 : Int × Int) + (0 : Int × Int) = (0 : Int × Int)
      exact zero_add _
    · change X.degree * Y.degree + Y.degree * X.degree = (0 : ZMod 2)
      have htwo : (2 : ZMod 2) = 0 := by decide
      calc
        X.degree * Y.degree + Y.degree * X.degree =
            (2 : ZMod 2) * (X.degree * Y.degree) := by ring
        _ = 0 := by rw [htwo, zero_mul]

/-- Native categorical involutivity of EVERY graded Gray
interchanger, with no collapse of the individual 3-cell. -/
theorem GrayGrade.native_braiding_twice_is_identity
    (X Y : GrayGrade) :
    (BraidedCategory.braiding X Y).hom ≫
      (BraidedCategory.braiding Y X).hom =
        (𝟙 (X ⊗ Y)) :=
  SymmetricCategory.symmetry X Y

/-- Stronger local statement: the odd/odd exchange is individually
nonidentity, but its double exchange is a genuine identity 3-cell
under the actual mathlib Category instance. -/
theorem GrayGrade.native_odd_exchange_nontrivial_involutive :
    (BraidedCategory.braiding GrayGrade.odd GrayGrade.odd).hom ≠
      (𝟙 (GrayGrade.tensor GrayGrade.odd GrayGrade.odd)) ∧
    (BraidedCategory.braiding GrayGrade.odd GrayGrade.odd).hom ≫
      (BraidedCategory.braiding GrayGrade.odd GrayGrade.odd).hom =
        (𝟙 (GrayGrade.tensor GrayGrade.odd GrayGrade.odd)) := by
  exact ⟨GrayGrade.native_braiding_odd_nonidentity,
    GrayGrade.native_braiding_twice_is_identity _ _⟩

/-- The original F58 integer-charge projection is not injective
even on ONE native Gray 3-morphism homset: the old charge cannot
distinguish the nonidentity odd/odd braiding from identity.
The additional F59 phase is necessary for this distinction. -/
theorem GrayGrade.native_F58_charge_projection_not_injective :
    ¬ Function.Injective
        (fun f :
          (GrayGrade.tensor GrayGrade.odd GrayGrade.odd) ⟶
            (GrayGrade.tensor GrayGrade.odd GrayGrade.odd) =>
          f.toHigherCharge) := by
  intro hinj
  apply GrayGrade.native_braiding_odd_nonidentity
  apply hinj
  rfl

#print axioms instSymmetricCategoryGrayGrade
#print axioms GrayGrade.native_braiding_twice_is_identity
#print axioms GrayGrade.native_odd_exchange_nontrivial_involutive
#print axioms GrayGrade.native_F58_charge_projection_not_injective

end
end KUOS.DependentOriginationGrayNativeSymmetricPhaseV5_156
