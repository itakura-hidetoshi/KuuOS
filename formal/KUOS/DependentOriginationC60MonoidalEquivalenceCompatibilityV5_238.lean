import KUOS.DependentOriginationC60DirectQuotientMonoidalV5_237
import Mathlib.CategoryTheory.Monoidal.Functor
import Mathlib.CategoryTheory.Monoidal.Transport

namespace KUOS.DependentOriginationC60MonoidalEquivalenceCompatibilityV5_238

open CategoryTheory
open scoped CategoryTheory.MonoidalCategory
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
open KUOS.DependentOriginationC60StrictChargeHorizontalInterchangeV5_230
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60NativeChargeQuotientEquivalenceV5_233
open KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234
open KUOS.DependentOriginationC60NativeQuotientMonoidalCoherenceV5_235
open KUOS.DependentOriginationC60QuotientTensorNaturalityV5_236
open KUOS.DependentOriginationC60DirectQuotientMonoidalV5_237

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.238 / F84 — genuine monoidal structure compatibility

F81 makes the genuine F77 phase quotient a monoidal category by
transport along the F79 category equivalence to F75.
F83 INDEPENDENTLY makes the same quotient a monoidal category by
F80's actual representative-descended Hom tensor with zero-charge
eqToIso associator and unitors, proving pentagon and triangle.

It is invalid to have two unrelated competing MonoidalCategory
instances on an untagged same type: distinguish the direct theory
by this explicit type synonym, and give it precisely F83's proved
monoidal laws. The original F81 transported quotient remains intact.

We then prove that the ACTUAL F79 charge-quotient functor out of
the direct monoidal quotient preserves the tensor, its unit,
associator and both unitors. The proof retains BOTH integer charges
and is on real Mathlib quotient Hom types, not chosen representatives.
We upgrade this to a Mathlib monoidal equivalence, rather than
confusing an isomorphism of tensor bifunctors with a monoidal
equivalence. F82 separately supplies the natural comparison to
the original F81 transported tensor.

This is a statement about the *phase quotient*, not a claim that the
unchanged F42/F54/F55 original higher-gluing 3-category is strict
or that north C60 geometric integer curvature -5 vanishes.
-/

/-- Explicitly distinguish the independently constructed F83
monoidal quotient from F81's transported monoidal quotient. -/
def C60F84DirectQuotient := C60F77NativeQuotient

instance c60F84DirectQuotientCategory : Category C60F84DirectQuotient :=
  inferInstanceAs (Category C60F77NativeQuotient)

instance c60F84DirectQuotientMonoidalStruct :
    MonoidalCategoryStruct C60F84DirectQuotient :=
  c60F83DirectMonoidalStruct

instance c60F84DirectQuotientMonoidal :
    MonoidalCategory C60F84DirectQuotient :=
  c60F83DirectMonoidalCategory

/-- The authentic original F79 quotient functor, now typed as
a functor from the separately packaged F83 DIRECT monoidal source. -/
def c60F84DirectToCharge :
    C60F84DirectQuotient ⥤ C60F75StrictChargeGrade :=
  c60F77QuotientToStrictCharge

/-- The original F79 genuine category equivalence between the
direct quotient and F75 is retained, not replaced by a surjective
numerical map. -/
def c60F84DirectChargeEquivalence :
    C60F84DirectQuotient ≌ C60F75StrictChargeGrade :=
  c60F79NativeChargeEquivalence

/-- Direct quotient horizontally tensors exactly to the
F75 integer-charge tensor ON BOTH HOM COORDINATES. -/
theorem c60F84DirectToCharge_map_tensor
    {X X' Y Y' : C60F84DirectQuotient}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F84DirectToCharge.map (f ⊗ₘ g) =
      c60F84DirectToCharge.map f ⊗ₘ
        c60F84DirectToCharge.map g := by
  exact c60F80QuotientTensor_chargeFunctor f g

/-- The genuine strict identity tensor unit, not an assumed
unit isomorphism changing one or both integer charges. -/
theorem c60F84DirectToCharge_unit :
    c60F84DirectToCharge.obj
      (𝟙_ C60F84DirectQuotient) =
        (𝟙_ C60F75StrictChargeGrade) := rfl

/-- The F79 functor sends the actual F83 associator to F75's
actual F81 associator. Both have zero of BOTH charges. -/
theorem c60F84DirectToCharge_map_associator
    (X Y Z : C60F84DirectQuotient) :
    c60F84DirectToCharge.map (α_ X Y Z).hom =
      (α_ (c60F84DirectToCharge.obj X)
          (c60F84DirectToCharge.obj Y)
          (c60F84DirectToCharge.obj Z)).hom := by
  apply C60F75StrictChargeThree.ext
  exact c60F83DirectAssociator_charge X Y Z

/-- Preservation of both independent charges through the
F83/F81 left unitor. -/
theorem c60F84DirectToCharge_map_leftUnitor
    (X : C60F84DirectQuotient) :
    c60F84DirectToCharge.map (λ_ X).hom =
      (λ_ (c60F84DirectToCharge.obj X)).hom := by
  apply C60F75StrictChargeThree.ext
  exact c60F83DirectLeftUnitor_charge X

/-- Preservation of both independent charges through the
F83/F81 right unitor. -/
theorem c60F84DirectToCharge_map_rightUnitor
    (X : C60F84DirectQuotient) :
    c60F84DirectToCharge.map (ρ_ X).hom =
      (ρ_ (c60F84DirectToCharge.obj X)).hom := by
  apply C60F75StrictChargeThree.ext
  exact c60F83DirectRightUnitor_charge X

/-- A genuine Mathlib strong monoidal compatibility certificate,
with *identity* comparison isomorphisms because the F79 map
preserves all direct quotient tensor and unit objects exactly. -/
def c60F84DirectToChargeCoreMonoidal :
    c60F84DirectToCharge.CoreMonoidal where
  εIso := Iso.refl _
  μIso := fun _ _ => Iso.refl _
  μIso_hom_natural_left := by
    intro X Y f Z
    simpa using (c60F84DirectToCharge_map_tensor f (𝟙 Z)).symm
  μIso_hom_natural_right := by
    intro X Y Z f
    simpa using (c60F84DirectToCharge_map_tensor (𝟙 X) f).symm
  associativity := by
    intro X Y Z
    simpa using (c60F84DirectToCharge_map_associator X Y Z).symm
  left_unitality := by
    intro X
    simpa using (c60F84DirectToCharge_map_leftUnitor X).symm
  right_unitality := by
    intro X
    simpa using (c60F84DirectToCharge_map_rightUnitor X).symm

/-- The proven strong monoidal F79 quotient functor, with ALL
naturality, associativity and both unit compatibilities,
as a full Mathlib Functor.Monoidal structure. -/
@[implicit_reducible]
def c60F84DirectToChargeMonoidal :
    c60F84DirectToCharge.Monoidal :=
  c60F84DirectToChargeCoreMonoidal.toMonoidal

/-- Put the independently verified direct strong monoidal
structure on the ACTUAL forward leg of the F79 equivalence. -/
@[implicit_reducible]
def c60F84DirectChargeEquivalenceForwardMonoidal :
    c60F84DirectChargeEquivalence.functor.Monoidal := by
  exact c60F84DirectToChargeMonoidal

/-- The original categorical equivalence, now with both its
forward and quasi-inverse promoted to coherent monoidal functors. -/
@[implicit_reducible]
def c60F84DirectChargeEquivalenceInverseMonoidal :
    letI : c60F84DirectChargeEquivalence.functor.Monoidal :=
      c60F84DirectChargeEquivalenceForwardMonoidal
    c60F84DirectChargeEquivalence.inverse.Monoidal := by
  letI : c60F84DirectChargeEquivalence.functor.Monoidal :=
    c60F84DirectChargeEquivalenceForwardMonoidal
  exact c60F84DirectChargeEquivalence.inverseMonoidal

/-- The underlying F79 category equivalence is a genuine
Mathlib MONOIDAL equivalence of the F83 direct quotient and F75. -/
def c60F84DirectChargeMonoidalEquivalence :
    letI : c60F84DirectChargeEquivalence.functor.Monoidal :=
      c60F84DirectChargeEquivalenceForwardMonoidal
    letI : c60F84DirectChargeEquivalence.inverse.Monoidal :=
      c60F84DirectChargeEquivalenceInverseMonoidal
    c60F84DirectChargeEquivalence.IsMonoidal := by
  letI : c60F84DirectChargeEquivalence.functor.Monoidal :=
    c60F84DirectChargeEquivalenceForwardMonoidal
  letI : c60F84DirectChargeEquivalence.inverse.Monoidal :=
    c60F84DirectChargeEquivalenceInverseMonoidal
  infer_instance

#print axioms c60F84DirectToCharge_map_tensor
#print axioms c60F84DirectToCharge_unit
#print axioms c60F84DirectToCharge_map_associator
#print axioms c60F84DirectToCharge_map_leftUnitor
#print axioms c60F84DirectToCharge_map_rightUnitor
#print axioms c60F84DirectToChargeCoreMonoidal
#print axioms c60F84DirectToChargeMonoidal
#print axioms c60F84DirectChargeEquivalenceForwardMonoidal
#print axioms c60F84DirectChargeEquivalenceInverseMonoidal
#print axioms c60F84DirectChargeMonoidalEquivalence

end
end KUOS.DependentOriginationC60MonoidalEquivalenceCompatibilityV5_238
