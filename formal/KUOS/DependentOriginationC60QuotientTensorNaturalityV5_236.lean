import KUOS.DependentOriginationC60NativeQuotientMonoidalCoherenceV5_235
import Mathlib.CategoryTheory.Monoidal.Category

namespace KUOS.DependentOriginationC60QuotientTensorNaturalityV5_236

open CategoryTheory
open scoped CategoryTheory.MonoidalCategory
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
open KUOS.DependentOriginationC60StrictChargeHorizontalInterchangeV5_230
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60NativeChargeQuotientEquivalenceV5_233
open KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234
open KUOS.DependentOriginationC60NativeQuotientMonoidalCoherenceV5_235

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.236 / F82 — real naturality of the quotient tensor comparison

F80 constructed the ACTUAL horizontal three-arrow bifunctor on the
Mathlib quotient Hom sets, with independent representative proofs,
strict middle-four interchange and preservation of Int x Int charges.
F81 gave the F77 quotient a Mathlib MonoidalCategory by transporting
the F75 charge-only monoidal structure along the genuine F79 category
equivalence, and established a comparison ISO on quotient objects.

The current theorem is stronger: the original componentwise
comparison assembles into an ACTUAL Mathlib NATURAL ISOMORPHISM
between the transported tensor bifunctor and the original F80
quotient tensor bifunctor. Naturality is proved for ALL real
QUOTIENT three-arrows, not merely native representatives or charges.
We use the native F79 equivalence unit naturality and the proven
F80 charge-tensor preservation to connect the two constructions.

We additionally establish independent associator, left-unit and
right-unit naturality for the F80 direct quotient tensor using
proved F80 object equalities, exact charge extinction on
eqToHom, and F79 faithfulness. These are typed real quotient Hom
equalities, not merely numerical similarities.

This neither recovers the intentionally killed original exchange
phase nor claims global strictness for unquotiented F42/F54/F55.
-/

/-- The REAL transported monoidal tensor is an actual Mathlib
bifunctor, to be compared to the independent F80 quotient Hom
bifunctor, not identified with it definitionally. -/
def c60F82TransportedTensorFunctor :
    (C60F77NativeQuotient × C60F77NativeQuotient) ⥤
      C60F77NativeQuotient :=
  MonoidalCategory.tensor C60F77NativeQuotient

/-- Exact map identity: the transported tensor on any pair of
ACTUAL quotient 3-arrows is the inverse-equivalence image of
the F79 charge image of the original F80 quotient tensor.
The equality is on real, dependent, quotient-Hom types. -/
theorem c60F82TransportedTensor_map_eq
    {X X' Y Y' : C60F77NativeQuotient}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    f ⊗ₘ g =
      (c60F79NativeChargeEquivalence.functor ⋙
        c60F79NativeChargeEquivalence.inverse).map
        (c60F80QuotientThreeTensor f g) := by
  change
    c60F79NativeChargeEquivalence.inverse.map
      (c60F76StrictChargeThreeTensor
        (c60F77QuotientToStrictCharge.map f)
        (c60F77QuotientToStrictCharge.map g)) =
    c60F79NativeChargeEquivalence.inverse.map
      (c60F77QuotientToStrictCharge.map
        (c60F80QuotientThreeTensor f g))
  rw [c60F80QuotientTensor_chargeFunctor f g]

/-- The F81 canonical componentwise comparison is NATURAL:
the transported tensor 3-arrow, followed by the comparison at
the target, equals the comparison at the source followed by
the original-representative F80 horizontal 3-arrow. -/
theorem c60F82TransportedVsF80_naturality
    {X X' Y Y' : C60F77NativeQuotient}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    (f ⊗ₘ g) ≫
      (c60F81TransportedVsOriginalQuotientTensorIso X' Y').hom =
    (c60F81TransportedVsOriginalQuotientTensorIso X Y).hom ≫
      c60F80QuotientThreeTensor f g := by
  rw [c60F82TransportedTensor_map_eq f g]
  exact
    c60F79NativeChargeEquivalence.unitIso.inv.naturality
      (c60F80QuotientThreeTensor f g)

/-- A genuine Mathlib NATURAL ISOMORPHISM between the transported
tensor functor and F80's directly descended quotient tensor.
This is a single natural comparison for ALL pairs of 3-arrows;
it is not just an object-indexed family of isomorphisms. -/
def c60F82TransportedVsF80TensorNatIso :
    c60F82TransportedTensorFunctor ≅
      c60F80QuotientHorizontalThreeFunctor :=
  NatIso.ofComponents
    (fun Z => c60F81TransportedVsOriginalQuotientTensorIso Z.1 Z.2)
    (by
      intro X Y f
      exact c60F82TransportedVsF80_naturality f.1 f.2)

/-- The natural isomorphism has exactly the original F81
source-object component, rather than inventing a replacement. -/
theorem c60F82TransportedVsF80TensorNatIso_hom_app
    (X Y : C60F77NativeQuotient) :
    c60F82TransportedVsF80TensorNatIso.hom.app (X, Y) =
      (c60F81TransportedVsOriginalQuotientTensorIso X Y).hom := rfl

/-- Naturality remains an exact equality after two genuine
sequential quotient 3-arrow transitions in BOTH inputs. -/
theorem c60F82TransportedVsF80_twoStage
    {X₀ X₁ X₂ Y₀ Y₁ Y₂ : C60F77NativeQuotient}
    (f : X₀ ⟶ X₁) (g : X₁ ⟶ X₂)
    (h : Y₀ ⟶ Y₁) (k : Y₁ ⟶ Y₂) :
    ((f ⊗ₘ h) ≫ (g ⊗ₘ k)) ≫
      (c60F81TransportedVsOriginalQuotientTensorIso X₂ Y₂).hom =
    (c60F81TransportedVsOriginalQuotientTensorIso X₀ Y₀).hom ≫
      (c60F80QuotientThreeTensor f h ≫
        c60F80QuotientThreeTensor g k) := by
  calc
    ((f ⊗ₘ h) ≫ (g ⊗ₘ k)) ≫
        (c60F81TransportedVsOriginalQuotientTensorIso X₂ Y₂).hom =
      (f ⊗ₘ h) ≫
        ((g ⊗ₘ k) ≫
          (c60F81TransportedVsOriginalQuotientTensorIso X₂ Y₂).hom) := by
        rw [Category.assoc]
    _ = (f ⊗ₘ h) ≫
        ((c60F81TransportedVsOriginalQuotientTensorIso X₁ Y₁).hom ≫
          c60F80QuotientThreeTensor g k) := by
          rw [c60F82TransportedVsF80_naturality g k]
    _ = ((f ⊗ₘ h) ≫
        (c60F81TransportedVsOriginalQuotientTensorIso X₁ Y₁).hom) ≫
          c60F80QuotientThreeTensor g k := by
          rw [Category.assoc]
    _ = ((c60F81TransportedVsOriginalQuotientTensorIso X₀ Y₀).hom ≫
        c60F80QuotientThreeTensor f h) ≫
          c60F80QuotientThreeTensor g k := by
          rw [c60F82TransportedVsF80_naturality f h]
    _ = (c60F81TransportedVsOriginalQuotientTensorIso X₀ Y₀).hom ≫
        (c60F80QuotientThreeTensor f h ≫
          c60F80QuotientThreeTensor g k) :=
          Category.assoc _ _ _

/-! Direct F80 coherence on the ACTUAL quotient, independently
of F81 transported monoidal associator and unitors. -/

/-- Equality transport between F80 quotient 2-cell objects
has zero BOTH F58 integer charges. This follows from the
actual F77 quotient functor, not from a new coherence axiom. -/
@[simp] theorem c60F82Quotient_eqToHom_charge_zero
    {X Y : C60F77NativeQuotient} (h : X = Y) :
    (c60F77QuotientToStrictCharge.map (eqToHom h : X ⟶ Y)).charge =
      (0 : Int × Int) := by
  cases h
  exact c60F80QuotientThree_id_charge X

/-- The independent F80 directly descended tensor satisfies
NATURALITY OF ITS ACTUAL OBJECT ASSOCIATOR on EVERY typed
quotient three-arrow, including nonzero integral charges. -/
theorem c60F82F80Associator_naturality
    {X X' Y Y' Z Z' : C60F77NativeQuotient}
    (f : X ⟶ X') (g : Y ⟶ Y') (h : Z ⟶ Z') :
    c60F80QuotientThreeTensor
        (c60F80QuotientThreeTensor f g) h ≫
      eqToHom (c60F80QuotientTwoTensor_assoc X' Y' Z') =
    eqToHom (c60F80QuotientTwoTensor_assoc X Y Z) ≫
      c60F80QuotientThreeTensor
        f (c60F80QuotientThreeTensor g h) := by
  apply c60F80QuotientThree_ext
  simp only [c60F80QuotientThree_comp_charge,
    c60F80QuotientThreeTensor_charge,
    c60F82Quotient_eqToHom_charge_zero]
  abel

/-- Left unit transport for the F80 direct quotient tensor is
natural for all actual quotient three-arrows. -/
theorem c60F82F80LeftUnitor_naturality
    {X Y : C60F77NativeQuotient} (f : X ⟶ Y) :
    c60F80QuotientThreeTensor (𝟙 c60F80QuotientTwoUnit) f ≫
      eqToHom (c60F80QuotientTwoTensor_leftUnit Y) =
    eqToHom (c60F80QuotientTwoTensor_leftUnit X) ≫ f := by
  apply c60F80QuotientThree_ext
  simp only [c60F80QuotientThree_comp_charge,
    c60F80QuotientThreeTensor_charge,
    c60F82Quotient_eqToHom_charge_zero,
    c60F80QuotientThree_id_charge]
  abel

/-- Right unit transport for the F80 direct quotient tensor is
natural for all actual quotient three-arrows. -/
theorem c60F82F80RightUnitor_naturality
    {X Y : C60F77NativeQuotient} (f : X ⟶ Y) :
    c60F80QuotientThreeTensor f (𝟙 c60F80QuotientTwoUnit) ≫
      eqToHom (c60F80QuotientTwoTensor_rightUnit Y) =
    eqToHom (c60F80QuotientTwoTensor_rightUnit X) ≫ f := by
  apply c60F80QuotientThree_ext
  simp only [c60F80QuotientThree_comp_charge,
    c60F80QuotientThreeTensor_charge,
    c60F82Quotient_eqToHom_charge_zero,
    c60F80QuotientThree_id_charge]
  abel

#print axioms c60F82TransportedTensor_map_eq
#print axioms c60F82TransportedVsF80_naturality
#print axioms c60F82TransportedVsF80TensorNatIso
#print axioms c60F82TransportedVsF80TensorNatIso_hom_app
#print axioms c60F82TransportedVsF80_twoStage
#print axioms c60F82Quotient_eqToHom_charge_zero
#print axioms c60F82F80Associator_naturality
#print axioms c60F82F80LeftUnitor_naturality
#print axioms c60F82F80RightUnitor_naturality

end
end KUOS.DependentOriginationC60QuotientTensorNaturalityV5_236
