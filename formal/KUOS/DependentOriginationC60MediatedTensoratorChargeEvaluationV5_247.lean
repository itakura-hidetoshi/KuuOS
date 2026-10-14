import KUOS.DependentOriginationC60ObstructionGaugeCoboundaryV5_246
import Mathlib.CategoryTheory.Monoidal.Functor
import Mathlib.CategoryTheory.Monoidal.Transport

namespace KUOS.DependentOriginationC60MediatedTensoratorChargeEvaluationV5_247

open CategoryTheory
open scoped CategoryTheory.MonoidalCategory
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
open KUOS.DependentOriginationC60ObstructionGaugeCoboundaryV5_246

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.247 / F93 — evaluation of actual transported and inverse
monoidal comparison charges

F92 separated q(d,e) into a selected F79 counit gauge coboundary
and the genuinely transported F85 mediated comparison. Here we
evaluate the F84 inverse-monodial tensorator and F81 transported
forward tensorator separately from PINNED Mathlib, retaining
the original two independent Int × Int charges. An arbitrary
categorical equivalence does NOT license a zero-charge unit.

These calculations live in the actual F77 quotient, after
the independently nontrivial Gray odd/odd interchange phase
has been explicitly erased, and not on the raw F54/F55 source.
-/

/-- The inverse of the ORIGINAL F79 counit on any strict-charge
grade carries exactly the F91-selected integer 1-cochain. -/
theorem c60F93CounitInvCharge
    (Y : C60F75StrictChargeGrade) :
    (c60F79NativeChargeEquivalence.counitIso.app Y).inv.charge =
      c60F92GaugeGrade Y.degree := by
  rcases Y with ⟨d⟩
  exact (c60F92ChosenGauge_eq_counitInv
    (c60F89CanonicalGrade d)).symm

/-- The ORIGINAL F79 counit is the charge negative of its inverse.
We use the actual F75 categorical iso equation. -/
theorem c60F93CounitHomCharge
    (Y : C60F75StrictChargeGrade) :
    (c60F79NativeChargeEquivalence.counitIso.app Y).hom.charge =
      -c60F92GaugeGrade Y.degree := by
  have hzero := congrArg C60F75StrictChargeThree.charge
    (Iso.hom_inv_id (c60F79NativeChargeEquivalence.counitIso.app Y))
  simp only [c60F84Charge_comp, c60F84Charge_id] at hzero
  rw [c60F93CounitInvCharge] at hzero
  calc
    (c60F79NativeChargeEquivalence.counitIso.app Y).hom.charge =
      ((c60F79NativeChargeEquivalence.counitIso.app Y).hom.charge +
        c60F92GaugeGrade Y.degree) +
          -c60F92GaugeGrade Y.degree := by abel
    _ = -c60F92GaugeGrade Y.degree := by rw [hzero, zero_add]

/-- The F81 transported quotient uses the original F79 counit
INVERSE as the forward charge-functor's strong tensorator;
this follows from the actual Mathlib induced monoidal structure. -/
theorem c60F93TransportedForwardMuCharge
    (X Y : C60F85TransportedQuotient) :
    letI : c60F85TransportedToCharge.functor.Monoidal :=
      c60F85TransportedToChargeForwardMonoidal
    (Functor.LaxMonoidal.μ c60F85TransportedToCharge.functor X Y).charge =
      c60F92ChosenGaugeCharge (c60F80QuotientTwoTensor X Y) := by
  letI : c60F85TransportedToCharge.functor.Monoidal :=
    c60F85TransportedToChargeForwardMonoidal
  change
    (c60F79NativeChargeEquivalence.counitIso.app
      (c60F77QuotientToStrictCharge.obj
        (c60F80QuotientTwoTensor X Y))).inv.charge =
      c60F92ChosenGaugeCharge (c60F80QuotientTwoTensor X Y)
  exact (c60F92ChosenGauge_eq_counitInv
    (c60F80QuotientTwoTensor X Y)).symm

/-- F84's actual strong forward functor has inverse tensorator
literally the identity on the original strict charge groupoid. -/
theorem c60F93DirectForwardDeltaChargeZero
    (X Y : C60F84DirectQuotient) :
    letI : c60F84DirectChargeEquivalence.functor.Monoidal :=
      c60F84DirectChargeEquivalenceForwardMonoidal
    (Functor.OplaxMonoidal.δ
      c60F84DirectChargeEquivalence.functor X Y).charge =
        (0 : Int × Int) := by
  letI : c60F84DirectChargeEquivalence.functor.Monoidal :=
    c60F84DirectChargeEquivalenceForwardMonoidal
  have hμ :
      (Functor.LaxMonoidal.μ
        c60F84DirectChargeEquivalence.functor X Y).charge =
          (0 : Int × Int) := by
    rfl
  have h := congrArg C60F75StrictChargeThree.charge
    (Functor.Monoidal.μ_δ
      c60F84DirectChargeEquivalence.functor X Y)
  simp only [c60F84Charge_comp, c60F84Charge_id] at h
  rw [hμ, zero_add] at h
  exact h

/-- The genuine inverse F84 monoidal comparison satisfies exactly
the unit/counit balance from Mathlib's monoidal equivalence law;
its source and target are typed F75 charge morphisms. -/
theorem c60F93DirectInverseMuChargeBalance
    (A B : C60F75StrictChargeGrade) :
    letI : c60F84DirectChargeEquivalence.functor.Monoidal :=
      c60F84DirectChargeEquivalenceForwardMonoidal
    letI : c60F84DirectChargeEquivalence.inverse.Monoidal :=
      c60F84DirectChargeEquivalenceInverseMonoidal
    letI : c60F84DirectChargeEquivalence.IsMonoidal :=
      c60F84DirectChargeMonoidalEquivalence
    (c60F84DirectChargeEquivalence.functor.map
      (Functor.LaxMonoidal.μ c60F84DirectChargeEquivalence.inverse A B)).charge +
        (c60F84DirectChargeEquivalence.counitIso.app (A ⊗ B)).hom.charge =
      (c60F84DirectChargeEquivalence.counitIso.app A).hom.charge +
        (c60F84DirectChargeEquivalence.counitIso.app B).hom.charge := by
  letI : c60F84DirectChargeEquivalence.functor.Monoidal :=
    c60F84DirectChargeEquivalenceForwardMonoidal
  letI : c60F84DirectChargeEquivalence.inverse.Monoidal :=
    c60F84DirectChargeEquivalenceInverseMonoidal
  letI : c60F84DirectChargeEquivalence.IsMonoidal :=
    c60F84DirectChargeMonoidalEquivalence
  have h :=
    c60F84DirectChargeEquivalence.functor_map_μ_inverse_comp_counitIso_hom_app_tensor
      A B
  have hc := congrArg C60F75StrictChargeThree.charge h
  simp only [c60F84Charge_comp, c60F84Charge_tensor,
    c60F93DirectForwardDeltaChargeZero, zero_add] at hc
  exact hc


/-- Mathlib's genuine strong inverse tensorator carries the
EXACT selected-unit defect t(A+B) - t(A) - t(B), not a
freely specified extra integer charge. -/
theorem c60F93DirectInverseMu_charge
    (A B : C60F75StrictChargeGrade) :
    letI : c60F84DirectChargeEquivalence.functor.Monoidal :=
      c60F84DirectChargeEquivalenceForwardMonoidal
    letI : c60F84DirectChargeEquivalence.inverse.Monoidal :=
      c60F84DirectChargeEquivalenceInverseMonoidal
    (c60F84DirectChargeEquivalence.functor.map
      (Functor.LaxMonoidal.μ
        c60F84DirectChargeEquivalence.inverse A B)).charge =
      c60F92GaugeGrade (A.degree + B.degree) -
        c60F92GaugeGrade A.degree - c60F92GaugeGrade B.degree := by
  letI : c60F84DirectChargeEquivalence.functor.Monoidal :=
    c60F84DirectChargeEquivalenceForwardMonoidal
  letI : c60F84DirectChargeEquivalence.inverse.Monoidal :=
    c60F84DirectChargeEquivalenceInverseMonoidal
  letI : c60F84DirectChargeEquivalence.IsMonoidal :=
    c60F84DirectChargeMonoidalEquivalence
  have hb := c60F93DirectInverseMuChargeBalance A B
  change
    (c60F84DirectChargeEquivalence.functor.map
      (Functor.LaxMonoidal.μ
        c60F84DirectChargeEquivalence.inverse A B)).charge +
        (c60F79NativeChargeEquivalence.counitIso.app (A ⊗ B)).hom.charge =
      (c60F79NativeChargeEquivalence.counitIso.app A).hom.charge +
        (c60F79NativeChargeEquivalence.counitIso.app B).hom.charge at hb
  rw [c60F93CounitHomCharge (A ⊗ B),
    c60F93CounitHomCharge A,
    c60F93CounitHomCharge B] at hb
  change
    (c60F84DirectChargeEquivalence.functor.map
      (Functor.LaxMonoidal.μ
        c60F84DirectChargeEquivalence.inverse A B)).charge +
        -c60F92GaugeGrade (A.degree + B.degree) =
      -c60F92GaugeGrade A.degree -
        c60F92GaugeGrade B.degree at hb
  calc
    (c60F84DirectChargeEquivalence.functor.map
        (Functor.LaxMonoidal.μ
          c60F84DirectChargeEquivalence.inverse A B)).charge =
      ((c60F84DirectChargeEquivalence.functor.map
        (Functor.LaxMonoidal.μ
          c60F84DirectChargeEquivalence.inverse A B)).charge +
        -c60F92GaugeGrade (A.degree + B.degree)) +
        c60F92GaugeGrade (A.degree + B.degree) := by abel
    _ = (-c60F92GaugeGrade A.degree -
          c60F92GaugeGrade B.degree) +
        c60F92GaugeGrade (A.degree + B.degree) := by rw [hb]
    _ = c60F92GaugeGrade (A.degree + B.degree) -
          c60F92GaugeGrade A.degree -
          c60F92GaugeGrade B.degree := by abel

/-- The original F79 *chosen* inverse preserves BOTH integer
charges of every actual F75 typed arrow, even though its
objectwise natural unit may have nonzero charge. -/
theorem c60F93ChosenInverse_map_preservesCharge
    {A B : C60F75StrictChargeGrade} (f : A ⟶ B) :
    (c60F79NativeChargeEquivalence.functor.map
      (c60F79NativeChargeEquivalence.inverse.map f)).charge =
      f.charge := by
  have hc := congrArg C60F75StrictChargeThree.charge
    (c60F79NativeChargeEquivalence.fun_inv_map A B f)
  simp only [c60F84Charge_comp] at hc
  change
    (c60F79NativeChargeEquivalence.functor.map
      (c60F79NativeChargeEquivalence.inverse.map f)).charge =
        (c60F79NativeChargeEquivalence.counitIso.app A).hom.charge +
          (f.charge +
            (c60F79NativeChargeEquivalence.counitIso.app B).inv.charge) at hc
  rw [c60F93CounitHomCharge A, c60F93CounitInvCharge B] at hc
  have hd : A.degree = B.degree := f.gradeEq
  rw [hd] at hc
  calc
    (c60F79NativeChargeEquivalence.functor.map
      (c60F79NativeChargeEquivalence.inverse.map f)).charge =
       -c60F92GaugeGrade B.degree + f.charge +
         c60F92GaugeGrade B.degree := by
           simpa only [add_assoc] using hc
    _ = f.charge := by abel


/-- The F85 mediated MONOIDAL tensorator really is the composite
of the transported forward F81 leg and F84's inverse leg, with
the original actual quotient-Hom source and target retained. -/
theorem c60F93MediatedMu_composition
    (X Y : C60F85TransportedQuotient) :
    letI : c60F85TransportedToCharge.functor.Monoidal :=
      c60F85TransportedToChargeForwardMonoidal
    letI : c60F85ChargeToDirect.functor.Monoidal :=
      c60F85ChargeToDirectForwardMonoidal
    c60F88MediatedMu X Y =
      (Functor.LaxMonoidal.μ c60F85ChargeToDirect.functor
          (c60F85TransportedToCharge.functor.obj X)
          (c60F85TransportedToCharge.functor.obj Y)) ≫
        c60F85ChargeToDirect.functor.map
          (Functor.LaxMonoidal.μ
            c60F85TransportedToCharge.functor X Y) := by
  letI : c60F85TransportedToCharge.functor.Monoidal :=
    c60F85TransportedToChargeForwardMonoidal
  letI : c60F85ChargeToDirect.functor.Monoidal :=
    c60F85ChargeToDirectForwardMonoidal
  change
    (Functor.LaxMonoidal.μ
      (c60F85TransportedToCharge.functor ⋙
        c60F85ChargeToDirect.functor) X Y) = _
  rfl

/-- Exact charge evaluation of the composite mediated monoidal
tensorator: F84 inverse charge plus the transported forward
tensorator charge, without introducing a new gauge. -/
theorem c60F93MediatedCharge_composition
    (X Y : C60F85TransportedQuotient) :
    letI : c60F85TransportedToCharge.functor.Monoidal :=
      c60F85TransportedToChargeForwardMonoidal
    letI : c60F85ChargeToDirect.functor.Monoidal :=
      c60F85ChargeToDirectForwardMonoidal
    c60F92MediatedCharge X Y =
      (c60F84DirectChargeEquivalence.functor.map
        (Functor.LaxMonoidal.μ c60F85ChargeToDirect.functor
          (c60F85TransportedToCharge.functor.obj X)
          (c60F85TransportedToCharge.functor.obj Y))).charge +
      (Functor.LaxMonoidal.μ
        c60F85TransportedToCharge.functor X Y).charge := by
  letI : c60F85TransportedToCharge.functor.Monoidal :=
    c60F85TransportedToChargeForwardMonoidal
  letI : c60F85ChargeToDirect.functor.Monoidal :=
    c60F85ChargeToDirectForwardMonoidal
  unfold c60F92MediatedCharge
  rw [c60F93MediatedMu_composition X Y]
  have hcomp := c60F80QuotientThree_comp_charge
    (Functor.LaxMonoidal.μ c60F85ChargeToDirect.functor
      (c60F85TransportedToCharge.functor.obj X)
      (c60F85TransportedToCharge.functor.obj Y))
    (c60F85ChargeToDirect.functor.map
      (Functor.LaxMonoidal.μ c60F85TransportedToCharge.functor X Y))
  have h := c60F93ChosenInverse_map_preservesCharge
    (Functor.LaxMonoidal.μ
      c60F85TransportedToCharge.functor X Y)
  exact hcomp.trans (congrArg
    (fun q : Int × Int =>
      (c60F84DirectChargeEquivalence.functor.map
        (Functor.LaxMonoidal.μ c60F85ChargeToDirect.functor
          (c60F85TransportedToCharge.functor.obj X)
          (c60F85TransportedToCharge.functor.obj Y))).charge + q) h)


/-- COMPLETE evaluation of the actual F85-mediated strong
monoidal tensorator. The exact selected gauge appears TWICE at
the product grade, and negatively at both input grades, as forced
by the ORIGINAL F81 transport and F84 inverse-monodial coherence. -/
theorem c60F93MediatedCharge_evaluated
    (X Y : C60F85TransportedQuotient) :
    c60F92MediatedCharge X Y =
      c60F92ChosenGaugeCharge (c60F80QuotientTwoTensor X Y) -
        c60F92ChosenGaugeCharge X - c60F92ChosenGaugeCharge Y +
        c60F92ChosenGaugeCharge (c60F80QuotientTwoTensor X Y) := by
  letI : c60F85TransportedToCharge.functor.Monoidal :=
    c60F85TransportedToChargeForwardMonoidal
  letI : c60F85ChargeToDirect.functor.Monoidal :=
    c60F85ChargeToDirectForwardMonoidal
  rw [c60F93MediatedCharge_composition X Y]
  have hInverse :
      (c60F84DirectChargeEquivalence.functor.map
        (Functor.LaxMonoidal.μ c60F85ChargeToDirect.functor
          (c60F85TransportedToCharge.functor.obj X)
          (c60F85TransportedToCharge.functor.obj Y))).charge =
        c60F92GaugeGrade
          ((c60F85TransportedToCharge.functor.obj X).degree +
           (c60F85TransportedToCharge.functor.obj Y).degree) -
        c60F92GaugeGrade
          (c60F85TransportedToCharge.functor.obj X).degree -
        c60F92GaugeGrade
          (c60F85TransportedToCharge.functor.obj Y).degree := by
    change
      (c60F84DirectChargeEquivalence.functor.map
        (Functor.LaxMonoidal.μ
          c60F84DirectChargeEquivalence.inverse
          (c60F85TransportedToCharge.functor.obj X)
          (c60F85TransportedToCharge.functor.obj Y))).charge = _
    exact c60F93DirectInverseMu_charge _ _
  rw [hInverse, c60F93TransportedForwardMuCharge X Y]
  have hX := c60F92GaugeCharge_factorsThroughGrade X
  have hY := c60F92GaugeCharge_factorsThroughGrade Y
  have hXY :=
    c60F92GaugeCharge_factorsThroughGrade
      (c60F80QuotientTwoTensor X Y)
  rw [hX, hY, hXY]
  change
    (c60F92GaugeGrade (X.as.degree + Y.as.degree) -
        c60F92GaugeGrade X.as.degree -
        c60F92GaugeGrade Y.as.degree) +
      c60F92GaugeGrade (X.as.degree + Y.as.degree) =
    c60F92GaugeGrade (X.as.degree + Y.as.degree) -
        c60F92GaugeGrade X.as.degree -
        c60F92GaugeGrade Y.as.degree +
      c60F92GaugeGrade (X.as.degree + Y.as.degree)
  rfl

/-- F92's full gauge-corrected F85/F82 obstruction actually
vanishes IN BOTH independent INTEGER CHARGE COORDINATES.
This is a theorem about the PHASE-QUOTIENT's explicitly chosen
monoidal structures; it says nothing about restoring the
original nontrivial raw Gray exchange. -/
theorem c60F93ObstructionCharge_zero
    (X Y : C60F77NativeQuotient) :
    c60F89ObstructionCharge X Y = (0 : Int × Int) := by
  rw [c60F92Obstruction_charge_gauge_expansion,
    c60F92TransportedTensorObj_eq_direct,
    c60F93MediatedCharge_evaluated]
  abel

/-- The ORIGINAL F85 strong monoidal IDENTITY tensorator is
COMPONENTWISE the inverse of the independently proved F82
natural tensor comparison on EVERY true F77 quotient pair.
F86's potential obstruction has been discharged WITHOUT
assuming any cancellation or quotient of F58 charges. -/
theorem c60F93AllTensorators_agree :
    ∀ X Y : C60F77NativeQuotient,
      (c60F86F85IdentityTensoratorIso X Y).hom =
        (c60F81TransportedVsOriginalQuotientTensorIso X Y).inv := by
  intro X Y
  apply (c60F86TensoratorObstruction_components_zero_iff X Y).mpr
  exact c60F93ObstructionCharge_zero X Y

/-- Consequently all four original F89 parity-pair obstruction
charges are zero as a theorem, not merely a four-case hypothesis. -/
theorem c60F93AllFourGradeObstructions_zero :
    c60F89GradePairCharge 0 0 = (0 : Int × Int) ∧
    c60F89GradePairCharge 0 1 = (0 : Int × Int) ∧
    c60F89GradePairCharge 1 0 = (0 : Int × Int) ∧
    c60F89GradePairCharge 1 1 = (0 : Int × Int) :=
  c60F89AllTensoratorsEqual_iff_fourGradeChargesZero.mp
    c60F93AllTensorators_agree

#print axioms c60F93MediatedCharge_evaluated
#print axioms c60F93ObstructionCharge_zero
#print axioms c60F93AllTensorators_agree
#print axioms c60F93AllFourGradeObstructions_zero

#print axioms c60F93MediatedMu_composition
#print axioms c60F93MediatedCharge_composition

#print axioms c60F93DirectInverseMu_charge
#print axioms c60F93ChosenInverse_map_preservesCharge
#print axioms c60F93CounitInvCharge
#print axioms c60F93CounitHomCharge
#print axioms c60F93TransportedForwardMuCharge
#print axioms c60F93DirectForwardDeltaChargeZero
#print axioms c60F93DirectInverseMuChargeBalance

end
end KUOS.DependentOriginationC60MediatedTensoratorChargeEvaluationV5_247
