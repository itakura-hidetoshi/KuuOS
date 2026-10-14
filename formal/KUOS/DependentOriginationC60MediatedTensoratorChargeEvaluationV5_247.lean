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

#print axioms c60F93CounitInvCharge
#print axioms c60F93CounitHomCharge
#print axioms c60F93TransportedForwardMuCharge
#print axioms c60F93DirectForwardDeltaChargeZero
#print axioms c60F93DirectInverseMuChargeBalance

end
end KUOS.DependentOriginationC60MediatedTensoratorChargeEvaluationV5_247
