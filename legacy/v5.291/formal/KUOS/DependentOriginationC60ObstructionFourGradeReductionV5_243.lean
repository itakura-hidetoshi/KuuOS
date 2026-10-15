import KUOS.DependentOriginationC60DirectTransportObstructionChargeV5_242
import Mathlib.Tactic.FinCases

namespace KUOS.DependentOriginationC60ObstructionFourGradeReductionV5_243

open CategoryTheory
open scoped CategoryTheory.MonoidalCategory
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60NativeChargeQuotientEquivalenceV5_233
open KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234
open KUOS.DependentOriginationC60NativeQuotientMonoidalCoherenceV5_235
open KUOS.DependentOriginationC60QuotientTensorNaturalityV5_236
open KUOS.DependentOriginationC60DirectQuotientMonoidalV5_237
open KUOS.DependentOriginationC60MonoidalEquivalenceCompatibilityV5_238
open KUOS.DependentOriginationC60TransportedDirectMonoidalEquivalenceV5_239
open KUOS.DependentOriginationC60TensoratorComparisonObstructionV5_240
open KUOS.DependentOriginationC60TensoratorObstructionEvaluationV5_241
open KUOS.DependentOriginationC60DirectTransportObstructionChargeV5_242

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.243 / F89 — four-grade reduction of the actual F85/F82 obstruction

F88 decomposed the F86 obstruction on ACTUAL F77 quotient Hom sets
into four exact Int×Int charge contributions, without proving they
vanish. F86 also proved the obstruction commutes with EVERY F80
original-representative horizontal tensor of quotient 3-arrows.

Crucially, the original F77 quotient category has two connected
components given by its ZMod2 grade. Arbitrary integer charge-bearing
three-arrows connect any two objects of the SAME grade; the original
exchange phase is erased only after passing through F77.

We now prove that the FULL Int×Int obstruction is CONSTANT along
every pair of same-grade object transitions. Thus it depends ONLY
on the pair of ZMod2 grades and its vanishing for ALL quotient
two-cell inputs is mathematically equivalent to checking exactly
FOUR canonical input pairs: (0,0), (0,1), (1,0), (1,1).

This is a genuine finite reduction, not a proof that the four
values are zero. They remain explicit unresolved components.
-/

/-- The actual F77 obstruction projected to BOTH original integer
charges, not a replacement by an untyped numerical model. -/
def c60F89ObstructionCharge
    (X Y : C60F77NativeQuotient) : Int × Int :=
  (c60F77QuotientToStrictCharge.map
    (c60F86TensoratorObstructionIso X Y).hom).charge

/-- Naturality on the actual quotient Hom sets implies that the
integer obstruction cannot change when either input is connected
by a real typed quotient three-arrow. No assumption of zero charge
on these connecting arrows is necessary. -/
theorem c60F89ObstructionCharge_natural
    {X X' Y Y' : C60F77NativeQuotient}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F89ObstructionCharge X Y =
      c60F89ObstructionCharge X' Y' := by
  have hn := c60F86TensoratorObstruction_natural f g
  have hc := congrArg
    (fun (h : c60F80QuotientTwoTensor X Y ⟶
        c60F80QuotientTwoTensor X' Y') =>
      (c60F77QuotientToStrictCharge.map h).charge) hn
  simp only [c60F80QuotientThree_comp_charge,
    c60F80QuotientThreeTensor_charge] at hc
  change
    ((c60F77QuotientToStrictCharge.map f).charge +
      (c60F77QuotientToStrictCharge.map g).charge) +
        c60F89ObstructionCharge X' Y' =
    c60F89ObstructionCharge X Y +
      ((c60F77QuotientToStrictCharge.map f).charge +
        (c60F77QuotientToStrictCharge.map g).charge) at hc
  have hh :
      ((c60F77QuotientToStrictCharge.map f).charge +
        (c60F77QuotientToStrictCharge.map g).charge) +
          c60F89ObstructionCharge X' Y' =
      ((c60F77QuotientToStrictCharge.map f).charge +
        (c60F77QuotientToStrictCharge.map g).charge) +
          c60F89ObstructionCharge X Y := by
    calc
      _ = c60F89ObstructionCharge X Y +
          ((c60F77QuotientToStrictCharge.map f).charge +
            (c60F77QuotientToStrictCharge.map g).charge) := hc
      _ = _ := add_comm _ _
  exact (add_left_cancel hh).symm

/-- A canonical REAL quotient object at either ZMod2 degree. -/
def c60F89CanonicalGrade (d : ZMod 2) : C60F77NativeQuotient :=
  ⟨⟨d⟩⟩

/-- Every genuine quotient object connects to the canonical object
of the SAME original Gray degree, using an actual native phase-zero,
two-charge-zero three-arrow under the F77 quotient projection. -/
def c60F89GradeConnection
    (X : C60F77NativeQuotient) :
    X ⟶ c60F89CanonicalGrade X.as.degree :=
  c60F77Projection.map
    (⟨rfl, (0 : Int × Int), (0 : ZMod 2)⟩ :
      X.as ⟶ (⟨X.as.degree⟩ : GrayGrade))

/-- The connecting three-arrow has zero of BOTH integer charges,
without identifying the original nontrivial exchange before F77. -/
theorem c60F89GradeConnection_charge
    (X : C60F77NativeQuotient) :
    (c60F77QuotientToStrictCharge.map
      (c60F89GradeConnection X)).charge =
        (0 : Int × Int) := rfl

/-- The full obstruction on arbitrary quotient two-cell inputs equals
the obstruction on the two canonical representatives of their GRADES.
The reduction is a theorem on original typed quotient Hom sets. -/
theorem c60F89ObstructionCharge_eq_canonical
    (X Y : C60F77NativeQuotient) :
    c60F89ObstructionCharge X Y =
      c60F89ObstructionCharge
        (c60F89CanonicalGrade X.as.degree)
        (c60F89CanonicalGrade Y.as.degree) :=
  c60F89ObstructionCharge_natural
    (c60F89GradeConnection X) (c60F89GradeConnection Y)

/-- EXACT table of the four residual independent Z² charges:
the entries may be nonzero until they are calculated from the
F79/F84 unit and mediated tensorator in a subsequent front. -/
def c60F89GradePairCharge (d e : ZMod 2) : Int × Int :=
  c60F89ObstructionCharge
    (c60F89CanonicalGrade d) (c60F89CanonicalGrade e)

/-- Every obstruction charge factors through the actual four-element
Cartesian product of two original ZMod2 object grades. -/
theorem c60F89ObstructionCharge_factorsThroughGrade
    (X Y : C60F77NativeQuotient) :
    c60F89ObstructionCharge X Y =
      c60F89GradePairCharge X.as.degree Y.as.degree :=
  c60F89ObstructionCharge_eq_canonical X Y

/-- The global Ω=id condition reduces EXACTLY to four finite
integer charge checks; no one of those checks is silently assumed. -/
theorem c60F89AllTensoratorsEqual_iff_fourGradeChargesZero :
    (∀ X Y : C60F77NativeQuotient,
       (c60F86F85IdentityTensoratorIso X Y).hom =
         (c60F81TransportedVsOriginalQuotientTensorIso X Y).inv) ↔
      c60F89GradePairCharge 0 0 = (0 : Int × Int) ∧
      c60F89GradePairCharge 0 1 = (0 : Int × Int) ∧
      c60F89GradePairCharge 1 0 = (0 : Int × Int) ∧
      c60F89GradePairCharge 1 1 = (0 : Int × Int) := by
  constructor
  · intro h
    exact ⟨(c60F86TensoratorObstruction_components_zero_iff _ _).mp (h _ _),
      (c60F86TensoratorObstruction_components_zero_iff _ _).mp (h _ _),
      (c60F86TensoratorObstruction_components_zero_iff _ _).mp (h _ _),
      (c60F86TensoratorObstruction_components_zero_iff _ _).mp (h _ _)⟩
  · rintro ⟨h00, h01, h10, h11⟩ X Y
    apply (c60F86TensoratorObstruction_components_zero_iff X Y).mpr
    change c60F89ObstructionCharge X Y = (0 : Int × Int)
    rw [c60F89ObstructionCharge_factorsThroughGrade]
    have hf : ∀ d e : ZMod 2,
        c60F89GradePairCharge d e = (0 : Int × Int) := by
      intro d e
      fin_cases d <;> fin_cases e <;> assumption
    exact hf X.as.degree Y.as.degree

#print axioms c60F89ObstructionCharge
#print axioms c60F89ObstructionCharge_natural
#print axioms c60F89CanonicalGrade
#print axioms c60F89GradeConnection
#print axioms c60F89GradeConnection_charge
#print axioms c60F89ObstructionCharge_eq_canonical
#print axioms c60F89GradePairCharge
#print axioms c60F89ObstructionCharge_factorsThroughGrade
#print axioms c60F89AllTensoratorsEqual_iff_fourGradeChargesZero

end
end KUOS.DependentOriginationC60ObstructionFourGradeReductionV5_243
