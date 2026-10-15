import KUOS.DependentOriginationC60CanonicalChoiceInverseNatIsoV5_245
import Mathlib.Tactic.Abel

namespace KUOS.DependentOriginationC60ObstructionGaugeCoboundaryV5_246

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
open KUOS.DependentOriginationC60DirectTransportObstructionChargeV5_242
open KUOS.DependentOriginationC60ObstructionFourGradeReductionV5_243
open KUOS.DependentOriginationC60CanonicalChoiceInverseNatIsoV5_245

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.246 / F92 — exact gauge-coboundary decomposition of F89's four obstructions

F89 identified four independent Int × Int obstruction values, one per
(ZMod 2)² grade pair. F90 supplied a canonical zero-phase section and
F91 compared it NATURALLY to the genuinely selected F79 quasi-inverse.

Here the F91 choice-dependent UNIT is an explicit 1-cochain t(d).
Using the F88 genuine four/five-factor typed quotient-Hom decomposition
and the F86 comparison naturality, we prove that the obstruction is

    q(d,e) = δt(d,e) + ρ(d,e),
    δt(d,e) = t(d) + t(e) - t(d+e),
    ρ(d,e) = m(d,e) - t(d+e),

where m is the real F85 mediated strong monoidal tensorator charge.
The chosen-counit gauge is NOT assumed zero. We also verify δt is a
normalized-in-the-cohomological-sense 2-COBOUNDARY with the genuine
cocycle equality (not necessarily zero when one grade is zero).
The residual ρ is an explicitly defined correction, NOT asserted to
be individually gauge invariant or zero. The four q values may
continue to carry an obstruction after separating these terms.

No new axiom, sorry, nontrivial raw Gray phase collapse before F77,
or claim that the original F54/F55 global C60 source is a strict 3-category.
The independent C60 north -5 signed curvature is untouched.
-/

/-- F79's actual selected unit charge, in BOTH original integers. -/
def c60F92ChosenGaugeCharge (X : C60F77NativeQuotient) : Int × Int :=
  (c60F77QuotientToStrictCharge.map
    (c60F79NativeChargeEquivalence.unitIso.app X).hom).charge

/-- Exactly F91's comparison to F90's zero-phase section:
the gauge is the charge of the F79 CHOSEN counit inverse. -/
theorem c60F92ChosenGauge_eq_counitInv
    (X : C60F77NativeQuotient) :
    c60F92ChosenGaugeCharge X =
      (c60F79NativeChargeEquivalence.counitIso.app
        (c60F77QuotientToStrictCharge.obj X)).inv.charge :=
  c60F91ChosenUnit_charge X

/-- The inverse of F79's unit has the NEGATIVE of its exact
two-coordinate charge. This uses the actual quotient Hom composition
and the invertibility theorem, not a new choice-free normalization. -/
theorem c60F92ChosenGaugeInverse_charge
    (X : C60F77NativeQuotient) :
    (c60F77QuotientToStrictCharge.map
      (c60F79NativeChargeEquivalence.unitIso.app X).inv).charge =
      -c60F92ChosenGaugeCharge X := by
  have hzero :
      (c60F77QuotientToStrictCharge.map
        ((c60F79NativeChargeEquivalence.unitIso.app X).hom ≫
          (c60F79NativeChargeEquivalence.unitIso.app X).inv)).charge =
        (0 : Int × Int) := by
    rw [Iso.hom_inv_id]
    exact c60F80QuotientThree_id_charge X
  have hsum :
      c60F92ChosenGaugeCharge X +
        (c60F77QuotientToStrictCharge.map
          (c60F79NativeChargeEquivalence.unitIso.app X).inv).charge =
        (0 : Int × Int) := by
    simpa only [c60F80QuotientThree_comp_charge,
      c60F92ChosenGaugeCharge] using hzero
  calc
    (c60F77QuotientToStrictCharge.map
        (c60F79NativeChargeEquivalence.unitIso.app X).inv).charge =
      (-c60F92ChosenGaugeCharge X + c60F92ChosenGaugeCharge X) +
        (c60F77QuotientToStrictCharge.map
          (c60F79NativeChargeEquivalence.unitIso.app X).inv).charge := by simp
    _ = -c60F92ChosenGaugeCharge X +
        (c60F92ChosenGaugeCharge X +
          (c60F77QuotientToStrictCharge.map
            (c60F79NativeChargeEquivalence.unitIso.app X).inv).charge) := by
          rw [add_assoc]
    _ = -c60F92ChosenGaugeCharge X := by rw [hsum, add_zero]

/-- The F88 input unit really is F79's chosen unit, with no
assumption that the two original charges vanish. -/
theorem c60F92F88InputUnit_charge (X : C60F77NativeQuotient) :
    (c60F77QuotientToStrictCharge.map
      (c60F85MediatedToIdentityNatIso.inv.app X)).charge =
      c60F92ChosenGaugeCharge X := rfl

/-- F88's mediator-to-identity comparison at the transported tensor
is the inverse F79 selected unit and therefore carries -t. -/
theorem c60F92F88MediatedBack_charge
    (X Y : C60F77NativeQuotient) :
    (c60F77QuotientToStrictCharge.map
      (c60F88MediatedBack X Y)).charge =
      -c60F92ChosenGaugeCharge
        (c60F82TransportedTensorFunctor.obj (X, Y)) := by
  change
    (c60F77QuotientToStrictCharge.map
      (c60F79NativeChargeEquivalence.unitIso.app
        (c60F82TransportedTensorFunctor.obj (X, Y))).inv).charge =
      -c60F92ChosenGaugeCharge _
  exact c60F92ChosenGaugeInverse_charge _

/-- F82's original beta is ALSO an inverse unit, this time at the
F80 DIRECT tensor object, not the transported tensor object. -/
theorem c60F92F88OriginalBeta_charge
    (X Y : C60F77NativeQuotient) :
    (c60F77QuotientToStrictCharge.map
      (c60F88OriginalBeta X Y)).charge =
      -c60F92ChosenGaugeCharge (c60F80QuotientTwoTensor X Y) := by
  change
    (c60F77QuotientToStrictCharge.map
      (c60F79NativeChargeEquivalence.unitIso.app
        (c60F80QuotientTwoTensor X Y)).inv).charge =
      -c60F92ChosenGaugeCharge _
  exact c60F92ChosenGaugeInverse_charge _

/-- The unmodified F85 mediated monoidal tensorator's ACTUAL
Int×Int charge on typed F77 quotient Hom data. -/
def c60F92MediatedCharge (X Y : C60F77NativeQuotient) : Int × Int :=
  (c60F77QuotientToStrictCharge.map (c60F88MediatedMu X Y)).charge

/-- Exact five-factor formula in terms of the chosen gauge t and
the original F85 mediated tensorator m, with NO vanishing assumptions. -/
theorem c60F92Obstruction_charge_gauge_expansion
    (X Y : C60F77NativeQuotient) :
    c60F89ObstructionCharge X Y =
      c60F92ChosenGaugeCharge X + c60F92ChosenGaugeCharge Y +
        c60F92MediatedCharge X Y +
        (-c60F92ChosenGaugeCharge (c60F82TransportedTensorFunctor.obj (X, Y))) +
        (-c60F92ChosenGaugeCharge (c60F80QuotientTwoTensor X Y)) := by
  unfold c60F89ObstructionCharge
  rw [c60F88Obstruction_charge_fiveFactors]
  rw [c60F92F88InputUnit_charge X,
    c60F92F88InputUnit_charge Y,
    c60F92F88MediatedBack_charge X Y,
    c60F92F88OriginalBeta_charge X Y]
  rfl

/-- In this very specific F77 quotient category, a typed three-arrow
forces equality of its TWO grade objects: both wrappers have exactly
the same ZMod2 degree. Nontrivial INTEGER CHARGES can still remain. -/
theorem c60F92Object_eq_of_hom
    {X Y : C60F77NativeQuotient} (f : X ⟶ Y) : X = Y := by
  have hdegree : X.as.degree = Y.as.degree :=
    (c60F77QuotientToStrictCharge.map f).gradeEq
  rcases X with ⟨⟨x⟩⟩
  rcases Y with ⟨⟨y⟩⟩
  change x = y at hdegree
  cases hdegree
  rfl

/-- F82's comparison proves that the transported tensor object
and the F80 direct tensor object are EQUAL in this skeleton.
This does NOT say that the F82 comparison ARROW is identity. -/
theorem c60F92TransportedTensorObj_eq_direct
    (X Y : C60F77NativeQuotient) :
    c60F82TransportedTensorFunctor.obj (X, Y) =
      c60F80QuotientTwoTensor X Y :=
  c60F92Object_eq_of_hom (c60F88OriginalBeta X Y)

/-- A genuine explicit additive one-cochain on the original F77
grade objects; its values are not assumed zero. -/
def c60F92GaugeGrade (d : ZMod 2) : Int × Int :=
  c60F92ChosenGaugeCharge (c60F89CanonicalGrade d)

/-- Every selected-unit charge equals the one-cochain of its
original ZMod2 grade, without needing an unproved choice of section. -/
theorem c60F92GaugeCharge_factorsThroughGrade
    (X : C60F77NativeQuotient) :
    c60F92ChosenGaugeCharge X = c60F92GaugeGrade X.as.degree := by
  rcases X with ⟨⟨d⟩⟩
  rfl

/-- The gauge at each degree is exactly the natural F91
comparison between the concrete F90 section and F79's choice. -/
theorem c60F92GaugeGrade_eq_F91Comparison (d : ZMod 2) :
    c60F92GaugeGrade d =
      (c60F77QuotientToStrictCharge.map
        (c60F91ExplicitToChosenInverseIso
          (c60F77QuotientToStrictCharge.obj
            (c60F89CanonicalGrade d))).hom).charge := by
  exact (c60F92ChosenGauge_eq_counitInv
    (c60F89CanonicalGrade d)).trans
      (c60F91ExplicitToChosenInverse_charge
        (c60F77QuotientToStrictCharge.obj
          (c60F89CanonicalGrade d))).symm

/-- The degree of the direct F80 tensor is the genuine additive
grade and not the independent integer charge or C60 curvature. -/
theorem c60F92DirectTensor_canonicalGrades (d e : ZMod 2) :
    c60F80QuotientTwoTensor (c60F89CanonicalGrade d)
      (c60F89CanonicalGrade e) = c60F89CanonicalGrade (d + e) := rfl

/-- The full obstruction splits into a 1-cochain coboundary and
the *remaining* mediated correction. Neither summand is assumed
zero or separately gauge invariant. -/
def c60F92GaugeCoboundary (X Y : C60F77NativeQuotient) : Int × Int :=
  c60F92ChosenGaugeCharge X + c60F92ChosenGaugeCharge Y -
    c60F92ChosenGaugeCharge (c60F80QuotientTwoTensor X Y)

def c60F92MediatedCorrection (X Y : C60F77NativeQuotient) : Int × Int :=
  c60F92MediatedCharge X Y -
    c60F92ChosenGaugeCharge (c60F80QuotientTwoTensor X Y)

/-- Actual quotient obstruction: exact gauge 2-coboundary plus
the leftover mediated-monoidal correction (not assumed zero). -/
theorem c60F92Obstruction_gauge_coboundary_decomposition
    (X Y : C60F77NativeQuotient) :
    c60F89ObstructionCharge X Y =
      c60F92GaugeCoboundary X Y + c60F92MediatedCorrection X Y := by
  rw [c60F92Obstruction_charge_gauge_expansion,
    c60F92TransportedTensorObj_eq_direct]
  dsimp [c60F92GaugeCoboundary, c60F92MediatedCorrection]
  abel

/-- Explicit F89 four-value gauge cochain, coboundary and
mediated comparison restricted to actual canonical grade objects. -/
def c60F92GaugeCoboundaryGrade (d e : ZMod 2) : Int × Int :=
  c60F92GaugeGrade d + c60F92GaugeGrade e - c60F92GaugeGrade (d + e)

def c60F92MediatedGradeCharge (d e : ZMod 2) : Int × Int :=
  c60F92MediatedCharge (c60F89CanonicalGrade d) (c60F89CanonicalGrade e)

def c60F92MediatedCorrectionGrade (d e : ZMod 2) : Int × Int :=
  c60F92MediatedGradeCharge d e - c60F92GaugeGrade (d + e)

/-- Exact F89 q(d,e) = δt(d,e) + ρ(d,e) on all four parity pairs. -/
theorem c60F92GradeObstruction_coboundary_plus_correction
    (d e : ZMod 2) :
    c60F89GradePairCharge d e =
      c60F92GaugeCoboundaryGrade d e +
        c60F92MediatedCorrectionGrade d e := by
  exact c60F92Obstruction_gauge_coboundary_decomposition
    (c60F89CanonicalGrade d) (c60F89CanonicalGrade e)

/-- The gauge contribution is an EXACT additive 2-cocycle:
it is a coboundary of the F91 natural comparison 1-cochain. -/
theorem c60F92GaugeCoboundaryGrade_cocycle
    (d e f : ZMod 2) :
    c60F92GaugeCoboundaryGrade d e +
        c60F92GaugeCoboundaryGrade (d + e) f =
      c60F92GaugeCoboundaryGrade e f +
        c60F92GaugeCoboundaryGrade d (e + f) := by
  dsimp [c60F92GaugeCoboundaryGrade]
  rw [add_assoc d e f]
  abel

/-- Original F89 global tensorator equality is equivalent to four
GAUGE-CORRECTED integer conditions; no conditions are claimed true. -/
theorem c60F92AllTensoratorsEqual_iff_fourGaugeCorrectedZero :
    (∀ X Y : C60F77NativeQuotient,
       (c60F86F85IdentityTensoratorIso X Y).hom =
         (c60F81TransportedVsOriginalQuotientTensorIso X Y).inv) ↔
      c60F92GaugeCoboundaryGrade 0 0 +
          c60F92MediatedCorrectionGrade 0 0 = (0 : Int × Int) ∧
      c60F92GaugeCoboundaryGrade 0 1 +
          c60F92MediatedCorrectionGrade 0 1 = (0 : Int × Int) ∧
      c60F92GaugeCoboundaryGrade 1 0 +
          c60F92MediatedCorrectionGrade 1 0 = (0 : Int × Int) ∧
      c60F92GaugeCoboundaryGrade 1 1 +
          c60F92MediatedCorrectionGrade 1 1 = (0 : Int × Int) := by
  simpa only [c60F92GradeObstruction_coboundary_plus_correction] using
    c60F89AllTensoratorsEqual_iff_fourGradeChargesZero

#print axioms c60F92ChosenGaugeCharge
#print axioms c60F92ChosenGauge_eq_counitInv
#print axioms c60F92ChosenGaugeInverse_charge
#print axioms c60F92F88InputUnit_charge
#print axioms c60F92F88MediatedBack_charge
#print axioms c60F92F88OriginalBeta_charge
#print axioms c60F92MediatedCharge
#print axioms c60F92Obstruction_charge_gauge_expansion
#print axioms c60F92Object_eq_of_hom
#print axioms c60F92TransportedTensorObj_eq_direct
#print axioms c60F92GaugeGrade
#print axioms c60F92GaugeCharge_factorsThroughGrade
#print axioms c60F92GaugeGrade_eq_F91Comparison
#print axioms c60F92DirectTensor_canonicalGrades
#print axioms c60F92Obstruction_gauge_coboundary_decomposition
#print axioms c60F92GradeObstruction_coboundary_plus_correction
#print axioms c60F92GaugeCoboundaryGrade_cocycle
#print axioms c60F92AllTensoratorsEqual_iff_fourGaugeCorrectedZero

end
end KUOS.DependentOriginationC60ObstructionGaugeCoboundaryV5_246
