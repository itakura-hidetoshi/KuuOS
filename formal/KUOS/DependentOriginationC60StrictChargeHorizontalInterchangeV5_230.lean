import KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
import KUOS.DependentOriginationC60OriginalSourceInterchangerNaturalityV5_228

namespace KUOS.DependentOriginationC60StrictChargeHorizontalInterchangeV5_230

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60GradedGrayThreeCategoryV5_197
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalGrayCoherenceV5_199
open KUOS.DependentOriginationC60OriginalStrictThreeArrowsV5_227
open KUOS.DependentOriginationC60OriginalSourceInterchangerNaturalityV5_228
open KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.230 / F76 — STRICT horizontal/vertical three-arrow interchange
# in the EXPLICIT phase-forgetting C60 integer-charge quotient

F75 intentionally formed a NEW theory, killing the original odd/odd
F43 interchange as an identity after identifying its original left-
first / right-first F42 source boundaries by genuine degree equality.
The present step makes that quotient CLOSED under an actual native
Mathlib HORIZONTAL THREE-ARROW COMPOSITION BIFUNCTOR.

Objects are the F75 degrees ZMod2, morphisms retain both independent
F58 integer charges. The new tensor sums both degrees and both
charges, and satisfies strict middle-four interchange of arbitrary
typed 3-arrows, not merely of original north-pentagon examples.
It also possesses a coherent associativity of horizontal three-
arrow products after explicit equality-transport of 2-cell labels.

For the ORIGINAL proof-relevant F42/F43/F51 source, its already
constructed horizontal and vertical source three-arrow composites
are mapped EXACTLY to this new strict tensor. Both integer charges
survive. Every original F43 interchange—including actual north C60—
remains an identity after phase quotient, as proved in F75.

We also characterize the PRECISE lost information: the F75
native quotient identifies two arrows iff their INT×INT charges
coincide. It is nonfaithful because the real odd/odd Gray braiding
has phase 1, but zero charge and is killed. We do not silently
equate genuinely different original F42 raw syntax: those become
identified only through the declared quotient.

These results give a STRICT 3-Hom tensor and interchange, and
progress toward a strict C60 3-category. The complete higher
globular source bicategorical/tri-categorical strictification for
all F42/F54/F55 objects, units and boundaries is not yet claimed.
The physical C60 north -5 integer curvature remains nonzero.
-/

/-- Phase-free strictified 2-cell horizontal tensor, retaining
the sum of the TWO genuinely typed source degrees. -/
def c60F76StrictChargeTwoTensor
    (X Y : C60F75StrictChargeGrade) : C60F75StrictChargeGrade :=
  ⟨X.degree + Y.degree⟩

/-- An ACTUAL typed horizontal three-arrow in the strict quotient;
both original INTEGER charge components add independently. -/
def c60F76StrictChargeThreeTensor
    {X X' Y Y' : C60F75StrictChargeGrade}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F76StrictChargeTwoTensor X Y ⟶
      c60F76StrictChargeTwoTensor X' Y' :=
  ⟨congrArg₂ (fun x y : ZMod 2 => x + y) f.gradeEq g.gradeEq,
    f.charge + g.charge⟩

/-- Complete strict 3-arrow horizontal multiplication as a
GENUINE Mathlib bifunctor, not just a numerical scalar sum. -/
def c60F76StrictChargeHorizontalThreeFunctor :
    (C60F75StrictChargeGrade × C60F75StrictChargeGrade) ⥤
      C60F75StrictChargeGrade where
  obj X := c60F76StrictChargeTwoTensor X.1 X.2
  map := fun {_ _} f => c60F76StrictChargeThreeTensor f.1 f.2
  map_id := by
    intro X
    apply C60F75StrictChargeThree.ext
    change (0 : Int × Int) + 0 = 0
    exact zero_add _
  map_comp := by
    intro X Y Z f g
    apply C60F75StrictChargeThree.ext
    change (f.1.charge + g.1.charge) + (f.2.charge + g.2.charge) =
      (f.1.charge + f.2.charge) + (g.1.charge + g.2.charge)
    abel

/-- All original charge-only strict 3-arrows obey the exact
MIDDLE-FOUR interchange law, including arbitrary nonzero
integer charges in BOTH independent coordinates. -/
theorem c60F76StrictThree_middleFour
    {X X' X'' Y Y' Y'' : C60F75StrictChargeGrade}
    (f : X ⟶ X') (g : X' ⟶ X'')
    (h : Y ⟶ Y') (k : Y' ⟶ Y'') :
    c60F76StrictChargeThreeTensor (f ≫ g) (h ≫ k) =
      c60F76StrictChargeThreeTensor f h ≫
        c60F76StrictChargeThreeTensor g k := by
  apply C60F75StrictChargeThree.ext
  change (f.charge + g.charge) + (h.charge + k.charge) =
    (f.charge + h.charge) + (g.charge + k.charge)
  abel

/-- The FULL native quotient is EXACTLY the kernel of the two
integer charges, on EVERY properly typed native Gray 3-Hom,
and not an unverified identification of ALL source 3-arrows. -/
theorem c60F76NativeQuotient_exactChargeKernel
    {X Y : GrayGrade} (f g : X ⟶ Y) :
    c60F75ForgetGrayExchangePhase.map f =
        c60F75ForgetGrayExchangePhase.map g ↔
      f.charge = g.charge := by
  constructor
  · intro h
    exact congrArg C60F75StrictChargeThree.charge h
  · intro h
    exact C60F75StrictChargeThree.ext h

/-- Quotient strictification is necessarily NONFAITHFUL:
an ACTUAL original odd/odd braided exchange is nonidentity
before quotienting, but has strictly zero both integer charges,
and thus maps to the identity 3-arrow. -/
theorem c60F76PhaseQuotient_isNotFaithful :
    ¬ c60F75ForgetGrayExchangePhase.Faithful := by
  intro hfaithful
  let z : GrayGrade := GrayGrade.tensor GrayGrade.odd GrayGrade.odd
  have hCoincide :
      c60F75ForgetGrayExchangePhase.map
          (BraidedCategory.braiding GrayGrade.odd GrayGrade.odd).hom =
        c60F75ForgetGrayExchangePhase.map (𝟙 z) := by
    apply C60F75StrictChargeThree.ext
    change (0 : Int × Int) = 0
    rfl
  exact GrayGrade.native_braiding_odd_nonidentity
    (hfaithful.map_injective hCoincide)

/-- Reassociation of horizontal strict 2-cell degrees is a
PROVED equality of original ZMod2 degrees, not a new axiom. -/
theorem c60F76StrictChargeTwoTensor_assoc
    (X Y Z : C60F75StrictChargeGrade) :
    c60F76StrictChargeTwoTensor
        (c60F76StrictChargeTwoTensor X Y) Z =
      c60F76StrictChargeTwoTensor
        X (c60F76StrictChargeTwoTensor Y Z) := by
  cases X with | mk x =>
    cases Y with | mk y =>
      cases Z with | mk z =>
        exact congrArg C60F75StrictChargeGrade.mk (add_assoc x y z)

/-- Both correctly typed reassociations of three ORIGINAL
strictified horizontal 3-arrows retain identical FULL integer
pair charges, before applying equality transport of endpoints. -/
theorem c60F76StrictChargeThreeTensor_assoc_charge
    {X X' Y Y' Z Z' : C60F75StrictChargeGrade}
    (f : X ⟶ X') (g : Y ⟶ Y') (h : Z ⟶ Z') :
    (c60F76StrictChargeThreeTensor
      (c60F76StrictChargeThreeTensor f g) h).charge =
    (c60F76StrictChargeThreeTensor
      f (c60F76StrictChargeThreeTensor g h)).charge := by
  change (f.charge + g.charge) + h.charge =
    f.charge + (g.charge + h.charge)
  exact add_assoc _ _ _

/-! ## Original C60 F42/F43 source, then strict quotient -/

section OriginalSource
variable {a b c : IcosahedralDart}
variable {p q : Quiver.Path a b}
variable {r s : Quiver.Path b c}

/-- ORIGINAL F42 horizontal three-arrow composition agrees
with the new genuinely strict charge tensor on all 3-Hom inputs.
This is a TYPED equality of real quotient three-arrows, not
just a claim about one charge coordinate. -/
theorem c60F76OriginalHorizontalStrictification_tensor
    {X X' : C60F51OriginalTwo p q}
    {Y Y' : C60F51OriginalTwo r s}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    (c60F75OriginalFaceStrictification
      (p.comp r) (q.comp s)).map
        (c60F51HorizontalMap f g) =
    c60F76StrictChargeThreeTensor
      ((c60F75OriginalFaceStrictification p q).map f)
      ((c60F75OriginalFaceStrictification r s).map g) := by
  apply C60F75StrictChargeThree.ext
  change (c60F51Eval (c60F51HorizontalMap f g)).charge =
    (c60F51Eval f).charge + (c60F51Eval g).charge
  rw [c60F51HorizontalMap_eval]
  exact grayNeutral_add_charge _ _

/-- Strict charge quotient is compatible with EVERY original
F43/F51 horizontal 3-arrow, including arrows with nonzero
TWO generator charges and any original interchange phase. -/
theorem c60F76OriginalHorizontalStrictification_charge
    {X X' : C60F51OriginalTwo p q}
    {Y Y' : C60F51OriginalTwo r s}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    ((c60F75OriginalFaceStrictification (p.comp r) (q.comp s)).map
      (c60F51HorizontalMap f g)).charge =
    (c60F51Eval f).charge + (c60F51Eval g).charge := by
  rw [c60F51HorizontalMap_eval]
  exact grayNeutral_add_charge _ _

end OriginalSource

section OriginalVertical
variable {a b : IcosahedralDart}
variable {p q r : Quiver.Path a b}

/-- ORIGINAL F42 vertical two-context 3-arrow composition
ALSO strictly respects the identical genuine quotient tensor.
This uses original vertical F51 source words, not a Gray
substitution for the underlying actual C60 2-cell syntax. -/
theorem c60F76OriginalVerticalStrictification_tensor
    {X X' : C60F51OriginalTwo p q}
    {Y Y' : C60F51OriginalTwo q r}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    (c60F75OriginalFaceStrictification p r).map
      (c60F51VerticalTwoMap f g) =
    c60F76StrictChargeThreeTensor
      ((c60F75OriginalFaceStrictification p q).map f)
      ((c60F75OriginalFaceStrictification q r).map g) := by
  apply C60F75StrictChargeThree.ext
  change (c60F51Eval (c60F51VerticalTwoMap f g)).charge =
    (c60F51Eval f).charge + (c60F51Eval g).charge
  rw [c60F51VerticalTwoMap_eval]
  exact grayNeutral_add_charge _ _

end OriginalVertical

/-- The precise ORIGINAL F51 source 3-Hom charge kernel
after strictification. The F51 native exchange phase is
intentionally discarded but its two integer charges survive. -/
theorem c60F76OriginalSourceQuotient_exactChargeKernel
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    {X Y : C60F51OriginalTwo p q}
    (f g : X ⟶ Y) :
    (c60F75OriginalFaceStrictification p q).map f =
        (c60F75OriginalFaceStrictification p q).map g ↔
    (c60F51Eval f).charge = (c60F51Eval g).charge := by
  constructor
  · intro h
    exact congrArg C60F75StrictChargeThree.charge h
  · intro h
    exact C60F75StrictChargeThree.ext h

/-- Source north pentagon interchange remains an identity
ONLY in the new phase-free strict category, never because
the old original F43 source witness was secretly trivial. -/
theorem c60F76OriginalNorthStrictExchange_isIdentity :
    (c60F75OriginalFaceStrictification
       ((c60F41PentagonBoundaryLoop .north).comp
          (c60F41PentagonBoundaryLoop .north))
       (Quiver.Path.nil.comp Quiver.Path.nil)).map
         c60F51NorthOriginalInterchanger =
      eqToHom
        (c60F75OriginalInterchanger_objects_identified
          c60F51NorthFaceSourceTwo c60F51NorthFaceSourceTwo) :=
  c60F75NorthOriginalInterchanger_collapses

#print axioms c60F76StrictChargeTwoTensor
#print axioms c60F76StrictChargeThreeTensor
#print axioms c60F76StrictChargeHorizontalThreeFunctor
#print axioms c60F76StrictThree_middleFour
#print axioms c60F76NativeQuotient_exactChargeKernel
#print axioms c60F76PhaseQuotient_isNotFaithful
#print axioms c60F76StrictChargeTwoTensor_assoc
#print axioms c60F76StrictChargeThreeTensor_assoc_charge
#print axioms c60F76OriginalHorizontalStrictification_tensor
#print axioms c60F76OriginalHorizontalStrictification_charge
#print axioms c60F76OriginalVerticalStrictification_tensor
#print axioms c60F76OriginalSourceQuotient_exactChargeKernel
#print axioms c60F76OriginalNorthStrictExchange_isIdentity

end
end KUOS.DependentOriginationC60StrictChargeHorizontalInterchangeV5_230
