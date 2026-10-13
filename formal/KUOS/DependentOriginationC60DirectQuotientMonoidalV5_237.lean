import KUOS.DependentOriginationC60QuotientTensorNaturalityV5_236
import Mathlib.CategoryTheory.Monoidal.Category

namespace KUOS.DependentOriginationC60DirectQuotientMonoidalV5_237

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

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.237 / F83: INDEPENDENT genuine monoidal structure on the F77 quotient

F80 defined a genuine tensor on the original Gray-phase quotient
Hom sets via Quot.liftOn₂, proving independence of BOTH choices
of original three-arrow representative, functoriality and the strict
middle-four law, with BOTH Int × Int charges retained.
F81 separately transported the F75 monoidal category along the F79
categorical equivalence. F82 proved the natural iso comparing the
TRANSPORTED tensor with the actual DIRECT quotient tensor, and
associator/unitor naturality of the latter.

F83 constructs a wholly INDEPENDENT Mathlib MonoidalCategory using
the DIRECT F80 quotient tensor as its ACTUAL tensorHom and tensorObj.
The associator, left and right unitors are actual equivalences from
Lean-proved original F80 ZMod2 degree equalities (eqToIso), not
postulated charge-zero morphisms or transport along an equivalence.
All of Mathlib's remaining coherence obligations (composition,
identity, associator naturality, unit naturality, pentagon and
triangle) are proved ON THE ACTUAL QUOTIENT HOM-SETS, using
F79 faithfulness and two-coordinate integral charge calculations.

To avoid silently replacing F81's existing global monoidal instance,
F83's alternative full instance is carried as an EXPLICIT
MonoidalCategory definition and locally installed when needed.
The directly constructed tensor bifunctor is identified with F80,
and F82 gives a genuine natural iso from F81's transported tensor.

This is an honest monoidal structure on a phase-killing 3-Hom
quotient category, not a strictification theorem for every raw
F42/F54/F55 original C60 higher composition. The original odd/odd
exchange is nonidentity pre-quotient; north C60 curvature -5
and both independent physical integer charges remain preserved.
-/

/-- ORIGINAL F80 associativity of 2-cell degree objects gives a
real invertible arrow of the Mathlib phase-killing quotient. -/
def c60F83DirectAssociator
    (X Y Z : C60F77NativeQuotient) :
    c60F80QuotientTwoTensor
      (c60F80QuotientTwoTensor X Y) Z ≅
        c60F80QuotientTwoTensor
          X (c60F80QuotientTwoTensor Y Z) :=
  eqToIso (c60F80QuotientTwoTensor_assoc X Y Z)

/-- The F80 original zero-degree horizontal unit has a genuine
invertible left-unitor from the original proven degree identity. -/
def c60F83DirectLeftUnitor
    (X : C60F77NativeQuotient) :
    c60F80QuotientTwoTensor c60F80QuotientTwoUnit X ≅ X :=
  eqToIso (c60F80QuotientTwoTensor_leftUnit X)

/-- The independently proved right unitor is also an actual
Mathlib Iso on the F77 quotient, not a F75-only arrow. -/
def c60F83DirectRightUnitor
    (X : C60F77NativeQuotient) :
    c60F80QuotientTwoTensor X c60F80QuotientTwoUnit ≅ X :=
  eqToIso (c60F80QuotientTwoTensor_rightUnit X)

/-- A NEW, independent monoidal STRUCTURE using the genuine original
F80 quotient horizontal composition, NOT the transported F81
monoidal structure. This is kept explicit to avoid double instances. -/
def c60F83DirectMonoidalStruct :
    MonoidalCategoryStruct C60F77NativeQuotient where
  tensorObj := c60F80QuotientTwoTensor
  whiskerLeft := by
    intro X Y Z f
    exact c60F80QuotientThreeTensor (𝟙 X) f
  whiskerRight := by
    intro X Y f Z
    exact c60F80QuotientThreeTensor f (𝟙 Z)
  tensorHom := by
    intro X Y Z W f g
    exact c60F80QuotientThreeTensor f g
  tensorUnit := c60F80QuotientTwoUnit
  associator := c60F83DirectAssociator
  leftUnitor := c60F83DirectLeftUnitor
  rightUnitor := c60F83DirectRightUnitor

/-- FULL Mathlib monoidal lawfulness proved DIRECTLY on the real
F77 quotient three-Hom sets. Crucially:
* original F80 quotient tensor is used on EVERY Hom;
* F82 provides actual associator/left/right naturality;
* the pentagon and triangle are exact quotient 3-arrow equations,
  proved by F79 Faithful+charge=0, not granted by F81 transport.
No global competing instance is introduced. -/
def c60F83DirectMonoidalCategory :
    MonoidalCategory C60F77NativeQuotient := by
  letI : MonoidalCategoryStruct C60F77NativeQuotient :=
    c60F83DirectMonoidalStruct
  exact
    MonoidalCategory.ofTensorHom
      (id_tensorHom_id := by
        intro X Y
        exact c60F80QuotientThreeTensor_id X Y)
      (id_tensorHom := by
        intro X Y Z f
        rfl)
      (tensorHom_id := by
        intro X Y f Z
        rfl)
      (tensorHom_comp_tensorHom := by
        intro X Y Z U V W f g h k
        exact (c60F80QuotientThreeTensor_middleFour f h g k).symm)
      (associator_naturality := by
        intro X X' Y Y' Z Z' f g h
        exact c60F82F80Associator_naturality f g h)
      (leftUnitor_naturality := by
        intro X Y f
        exact c60F82F80LeftUnitor_naturality f)
      (rightUnitor_naturality := by
        intro X Y f
        exact c60F82F80RightUnitor_naturality f)
      (pentagon := by
        intro W X Y Z
        apply c60F80QuotientThree_ext
        simp only [c60F80QuotientThree_comp_charge,
          c60F80QuotientThreeTensor_charge,
          c60F82Quotient_eqToHom_charge_zero,
          c60F80QuotientThree_id_charge]
        abel)
      (triangle := by
        intro X Y
        apply c60F80QuotientThree_ext
        simp only [c60F80QuotientThree_comp_charge,
          c60F80QuotientThreeTensor_charge,
          c60F82Quotient_eqToHom_charge_zero,
          c60F80QuotientThree_id_charge]
        abel)

/-- The strict original F80 tensor, seen as the Mathlib tensor
bifunctor of this EXPLICIT separately proved direct monoidal
structure. It is not the old F81 transported bifunctor. -/
def c60F83DirectTensorBifunctor :
    (C60F77NativeQuotient × C60F77NativeQuotient) ⥤
      C60F77NativeQuotient :=
  letI : MonoidalCategory C60F77NativeQuotient :=
    c60F83DirectMonoidalCategory
  MonoidalCategory.tensor C60F77NativeQuotient

/-- Proof, on the level of ACTUAL category bifunctors, that
the full monoidal tensor constructed independently by F83 is
the F80 representative-descended quotient tensor exactly. -/
theorem c60F83DirectTensorBifunctor_eqF80 :
    c60F83DirectTensorBifunctor =
      c60F80QuotientHorizontalThreeFunctor := by
  rfl

/-- The F82 natural comparison now compares TWO bona fide
monoidal tensor BIFUNCTORS, rather than a transported
monoidal tensor with an unstructured horizontal operation. -/
def c60F83TransportedVsDirectTensorNatIso :
    c60F82TransportedTensorFunctor ≅
      c60F83DirectTensorBifunctor := by
  rw [c60F83DirectTensorBifunctor_eqF80]
  exact c60F82TransportedVsF80TensorNatIso

/-- This fully verified independent monoidal category preserves
the original F80 middle-four interchange on ALL quotient 3-Homs,
including nonzero pairwise independent charge components. -/
theorem c60F83DirectMonoidal_interchange
    {X X' X'' Y Y' Y'' : C60F77NativeQuotient}
    (f : X ⟶ X') (g : X' ⟶ X'')
    (h : Y ⟶ Y') (k : Y' ⟶ Y'') :
    c60F80QuotientThreeTensor (f ≫ g) (h ≫ k) =
      c60F80QuotientThreeTensor f h ≫
        c60F80QuotientThreeTensor g k :=
  c60F80QuotientThreeTensor_middleFour f g h k

#print axioms c60F83DirectAssociator
#print axioms c60F83DirectLeftUnitor
#print axioms c60F83DirectRightUnitor
#print axioms c60F83DirectMonoidalStruct
#print axioms c60F83DirectMonoidalCategory
#print axioms c60F83DirectTensorBifunctor
#print axioms c60F83DirectTensorBifunctor_eqF80
#print axioms c60F83TransportedVsDirectTensorNatIso
#print axioms c60F83DirectMonoidal_interchange

end
end KUOS.DependentOriginationC60DirectQuotientMonoidalV5_237
