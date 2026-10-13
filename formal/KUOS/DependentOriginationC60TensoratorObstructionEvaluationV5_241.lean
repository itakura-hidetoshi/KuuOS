import KUOS.DependentOriginationC60TensoratorComparisonObstructionV5_240
import Mathlib.CategoryTheory.Monoidal.Transport

namespace KUOS.DependentOriginationC60TensoratorObstructionEvaluationV5_241

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

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.241 / F87 — exact source expansion of the F86 tensorator obstruction

F86 isolated Ω = μ_F85 ≫ β_F82 and proved that Ω = id iff both
Int×Int charge coordinates vanish. The latter is an independent
condition; F85 monoidal equivalence does NOT, by itself, imply it.

Here we expose the F85 identity tensorator as its REAL defining
Mathlib transport construction:
  μ_Id(X,Y) =
    (η_X ⊗direct η_Y) ≫ μ_mediated(X,Y) ≫ η^{-1}_{X⊗transport Y}.
The η is the ACTUAL F79 category-equivalence unit and mediated
strong monoidality comes from the genuine F81/F84 legs. This yields
an exact formula for Ω on quotient Hom sets, not only an abstract
conditional. Neither an artificial vanishing obstruction nor an
additional axiom is introduced.
-/

/-- Explicitly install the genuine strong monoidal structure used
in the ORIGINAL F85 mediated charge-factorization construction. -/
@[implicit_reducible]
def c60F87MediatedMonoidal :
    c60F85TransportedDirectEquivalence.functor.Monoidal :=
  c60F85TransportedDirectForwardMonoidal

/-- Source-exact tensorator formula from pinned Mathlib:
the identity comparison is the F79 unit on both inputs, followed
by the mediated F81/F84 strong tensorator, then the inverse unit
at the ACTUAL transported quotient tensor object. -/
theorem c60F87IdentityTensorator_transport_formula
    (X Y : C60F85TransportedQuotient) :
    letI : c60F85TransportedDirectEquivalence.functor.Monoidal :=
      c60F87MediatedMonoidal
    (c60F86F85IdentityTensoratorIso X Y).hom =
      (c60F85MediatedToIdentityNatIso.inv.app X ⊗ₘ
        c60F85MediatedToIdentityNatIso.inv.app Y) ≫
      Functor.LaxMonoidal.μ
        c60F85TransportedDirectEquivalence.functor X Y ≫
      c60F85MediatedToIdentityNatIso.hom.app (X ⊗ Y) := by
  letI : c60F85TransportedDirectEquivalence.functor.Monoidal :=
    c60F87MediatedMonoidal
  exact Functor.Monoidal.transport_μ c60F85MediatedToIdentityNatIso X Y

/-- Independently: F82's opposite comparison is EXACTLY the
original genuine F79 unit Iso at the direct F80 tensor object. -/
theorem c60F87F82Inverse_is_F79_unit
    (X Y : C60F85TransportedQuotient) :
    (c60F86F82CanonicalInverseTensorIso X Y).hom =
      c60F79NativeChargeEquivalence.unitIso.hom.app
        (c60F80QuotientTwoTensor X Y) := rfl

/-- Full, typed F87 obstruction decomposition on actual
Mathlib F77 quotient Hom sets: no unjustified equality of
the two independently constructed tensorators. -/
theorem c60F87Obstruction_hom_transport_formula
    (X Y : C60F85TransportedQuotient) :
    letI : c60F85TransportedDirectEquivalence.functor.Monoidal :=
      c60F87MediatedMonoidal
    (c60F86TensoratorObstructionIso X Y).hom =
      ((c60F85MediatedToIdentityNatIso.inv.app X ⊗ₘ
          c60F85MediatedToIdentityNatIso.inv.app Y) ≫
        Functor.LaxMonoidal.μ
          c60F85TransportedDirectEquivalence.functor X Y ≫
        c60F85MediatedToIdentityNatIso.hom.app (X ⊗ Y)) ≫
      (c60F81TransportedVsOriginalQuotientTensorIso X Y).hom := by
  letI : c60F85TransportedDirectEquivalence.functor.Monoidal :=
    c60F87MediatedMonoidal
  rw [c60F86TensoratorObstruction_hom]
  exact congrArg
    (fun h => h ≫ (c60F81TransportedVsOriginalQuotientTensorIso X Y).hom)
    (c60F87IdentityTensorator_transport_formula X Y)

/-- The residual two-coordinate charge is the sum of four truly
typed quotient-Hom contributions: tensor of the F79 units, the
F81/F84 mediated μ, its F79 unit inverse, and F82's comparison.
This is a computable interface for subsequent vanishing analysis. -/
theorem c60F87Obstruction_charge_transport_formula
    (X Y : C60F85TransportedQuotient) :
    letI : c60F85TransportedDirectEquivalence.functor.Monoidal :=
      c60F87MediatedMonoidal
    (c60F77QuotientToStrictCharge.map
      (c60F86TensoratorObstructionIso X Y).hom).charge =
      (c60F77QuotientToStrictCharge.map
        (c60F85MediatedToIdentityNatIso.inv.app X ⊗ₘ
          c60F85MediatedToIdentityNatIso.inv.app Y)).charge +
      (c60F77QuotientToStrictCharge.map
        (Functor.LaxMonoidal.μ
          c60F85TransportedDirectEquivalence.functor X Y)).charge +
      (c60F77QuotientToStrictCharge.map
        (c60F85MediatedToIdentityNatIso.hom.app (X ⊗ Y))).charge +
      (c60F77QuotientToStrictCharge.map
        (c60F81TransportedVsOriginalQuotientTensorIso X Y).hom).charge := by
  letI : c60F85TransportedDirectEquivalence.functor.Monoidal :=
    c60F87MediatedMonoidal
  rw [c60F86TensoratorObstruction_charge]
  rw [c60F87IdentityTensorator_transport_formula]
  abel

#print axioms c60F87MediatedMonoidal
#print axioms c60F87IdentityTensorator_transport_formula
#print axioms c60F87F82Inverse_is_F79_unit
#print axioms c60F87Obstruction_hom_transport_formula
#print axioms c60F87Obstruction_charge_transport_formula

end
end KUOS.DependentOriginationC60TensoratorObstructionEvaluationV5_241
