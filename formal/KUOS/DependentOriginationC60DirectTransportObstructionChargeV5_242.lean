import KUOS.DependentOriginationC60TensoratorObstructionEvaluationV5_241

namespace KUOS.DependentOriginationC60DirectTransportObstructionChargeV5_242

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
open KUOS.DependentOriginationC60TensoratorObstructionEvaluationV5_241

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.242 / F88 — typed F80 direct/ F81 transported comparison

F87 proved a genuine quotient-Hom identity for the difference
Ω = μ_F85 ≫ β_F82, but naïve 4-summand charge expressions
silently selected the F81 transported MonoidalCategory structure
rather than the F83 DIRECT tensor on the same underlying type.

Here we explicitly type each of the FOUR arrows on actual F77
quotient Hom sets, using F80's original representative-descended
horizontal three-arrow operation on the first factor.
No use of an ambiguous F81/F83 global tensor instance is
needed in the charge calculations. We apply F80's verified
functoriality and exact two-coordinate charge rules to the resulting
fourfold composite. We do NOT infer Ω = identity from coherence
alone and do NOT erase the original nontrivial Gray interchange.
-/

/-- F79 unit components tensorized with the ACTUAL F80 quotient
horizontal tensor, rather than an ambiguous untagged `⊗ₘ`. -/
def c60F88DirectUnitPair
    (X Y : C60F85TransportedQuotient) :
    c60F80QuotientTwoTensor X Y ⟶
      c60F80QuotientTwoTensor
        (c60F85TransportedDirectEquivalence.functor.obj X)
        (c60F85TransportedDirectEquivalence.functor.obj Y) :=
  c60F80QuotientThreeTensor
    (c60F85MediatedToIdentityNatIso.inv.app X)
    (c60F85MediatedToIdentityNatIso.inv.app Y)

/-- The F85 mediated strong-monoidal tensor comparison,
with the F83 directly descended product as source and F81's
transported product as the argument of the target functor. -/
def c60F88MediatedMu
    (X Y : C60F85TransportedQuotient) :
    c60F80QuotientTwoTensor
      (c60F85TransportedDirectEquivalence.functor.obj X)
      (c60F85TransportedDirectEquivalence.functor.obj Y) ⟶
    c60F85TransportedDirectEquivalence.functor.obj
      (c60F82TransportedTensorFunctor.obj (X, Y)) := by
  letI : c60F85TransportedDirectEquivalence.functor.Monoidal :=
    c60F87MediatedMonoidal
  exact Functor.LaxMonoidal.μ
    c60F85TransportedDirectEquivalence.functor X Y

/-- The exact inverse F79 unit that transports the mediated
tensor back to the identity functor at F81's transported tensor. -/
def c60F88MediatedBack
    (X Y : C60F85TransportedQuotient) :
    c60F85TransportedDirectEquivalence.functor.obj
      (c60F82TransportedTensorFunctor.obj (X, Y)) ⟶
    c60F82TransportedTensorFunctor.obj (X, Y) :=
  c60F85MediatedToIdentityNatIso.hom.app
    (c60F82TransportedTensorFunctor.obj (X, Y))

/-- The ORIGINAL F82 comparison `β`, from the transported
monoidal product to the original F80 direct quotient product. -/
def c60F88OriginalBeta
    (X Y : C60F85TransportedQuotient) :
    c60F82TransportedTensorFunctor.obj (X, Y) ⟶
      c60F80QuotientTwoTensor X Y :=
  (c60F81TransportedVsOriginalQuotientTensorIso X Y).hom

/-- Four independent, type-correct morphisms composed in the
ORIGINAL actual Mathlib F77 quotient Hom category. -/
def c60F88FourFactorComposite
    (X Y : C60F85TransportedQuotient) :
    c60F80QuotientTwoTensor X Y ⟶
      c60F80QuotientTwoTensor X Y :=
  ((c60F88DirectUnitPair X Y ≫ c60F88MediatedMu X Y) ≫
    c60F88MediatedBack X Y) ≫ c60F88OriginalBeta X Y

/-- The explicitly typed direct unit tensor is the exact F83
tensorHom selected by the F87 transport formula. -/
theorem c60F88DirectUnitPair_is_F83_tensor
    (X Y : C60F85TransportedQuotient) :
    letI : c60F85TransportedDirectEquivalence.functor.Monoidal :=
      c60F87MediatedMonoidal
    c60F88DirectUnitPair X Y =
      (c60F85MediatedToIdentityNatIso.inv.app X ⊗ₘ
        c60F85MediatedToIdentityNatIso.inv.app Y) := by
  rfl

/-- The FOUR physical quotient arrows are precisely F87's actual
obstruction, not merely a numerical proxy. -/
theorem c60F88FourFactorComposite_eq_obstruction
    (X Y : C60F85TransportedQuotient) :
    c60F88FourFactorComposite X Y =
      (c60F86TensoratorObstructionIso X Y).hom := by
  letI : c60F85TransportedDirectEquivalence.functor.Monoidal :=
    c60F87MediatedMonoidal
  simpa only [c60F88FourFactorComposite, c60F88DirectUnitPair,
    c60F88MediatedMu, c60F88MediatedBack, c60F88OriginalBeta,
    Category.assoc] using
      (c60F87Obstruction_hom_transport_formula X Y).symm

/-- The pair of original F79 unit components has EXACTLY the
sum of both Int×Int charges in the direct quotient. -/
theorem c60F88DirectUnitPair_charge
    (X Y : C60F85TransportedQuotient) :
    (c60F77QuotientToStrictCharge.map
      (c60F88DirectUnitPair X Y)).charge =
      (c60F77QuotientToStrictCharge.map
        (c60F85MediatedToIdentityNatIso.inv.app X)).charge +
      (c60F77QuotientToStrictCharge.map
        (c60F85MediatedToIdentityNatIso.inv.app Y)).charge :=
  c60F80QuotientThreeTensor_charge _ _

/-- The F86/F87 obstruction charge is EXACTLY the fourfold sum
of four separately typed F77 quotient arrows. The two integer
coordinates are conserved; no collapse is assumed. -/
theorem c60F88Obstruction_charge_fourFactors
    (X Y : C60F85TransportedQuotient) :
    (c60F77QuotientToStrictCharge.map
      (c60F86TensoratorObstructionIso X Y).hom).charge =
      (c60F77QuotientToStrictCharge.map
        (c60F88DirectUnitPair X Y)).charge +
      (c60F77QuotientToStrictCharge.map
        (c60F88MediatedMu X Y)).charge +
      (c60F77QuotientToStrictCharge.map
        (c60F88MediatedBack X Y)).charge +
      (c60F77QuotientToStrictCharge.map
        (c60F88OriginalBeta X Y)).charge := by
  rw [← c60F88FourFactorComposite_eq_obstruction X Y]
  unfold c60F88FourFactorComposite
  simp only [c60F80QuotientThree_comp_charge]

/-- A fully typed FIVE-summand version resolving the first
horizontal F80 tensor into its two independent unit charges. -/
theorem c60F88Obstruction_charge_fiveFactors
    (X Y : C60F85TransportedQuotient) :
    (c60F77QuotientToStrictCharge.map
      (c60F86TensoratorObstructionIso X Y).hom).charge =
      (c60F77QuotientToStrictCharge.map
        (c60F85MediatedToIdentityNatIso.inv.app X)).charge +
      (c60F77QuotientToStrictCharge.map
        (c60F85MediatedToIdentityNatIso.inv.app Y)).charge +
      (c60F77QuotientToStrictCharge.map
        (c60F88MediatedMu X Y)).charge +
      (c60F77QuotientToStrictCharge.map
        (c60F88MediatedBack X Y)).charge +
      (c60F77QuotientToStrictCharge.map
        (c60F88OriginalBeta X Y)).charge := by
  rw [c60F88Obstruction_charge_fourFactors,
    c60F88DirectUnitPair_charge]

/-- An EXACT necessary and sufficient condition to identify
the F85 and F82 tensorators by the charge sum of genuinely typed
F79/F84/F82 quotient arrows. Zero is NOT assumed. -/
theorem c60F88Tensorator_eq_F82_iff_charge_fourFactors_zero
    (X Y : C60F85TransportedQuotient) :
    (c60F86F85IdentityTensoratorIso X Y).hom =
        (c60F81TransportedVsOriginalQuotientTensorIso X Y).inv ↔
      (c60F77QuotientToStrictCharge.map
        (c60F88DirectUnitPair X Y)).charge +
      (c60F77QuotientToStrictCharge.map
        (c60F88MediatedMu X Y)).charge +
      (c60F77QuotientToStrictCharge.map
        (c60F88MediatedBack X Y)).charge +
      (c60F77QuotientToStrictCharge.map
        (c60F88OriginalBeta X Y)).charge =
        (0 : Int × Int) := by
  rw [c60F86TensoratorObstruction_components_zero_iff,
    c60F88Obstruction_charge_fourFactors]

#print axioms c60F88DirectUnitPair
#print axioms c60F88MediatedMu
#print axioms c60F88MediatedBack
#print axioms c60F88OriginalBeta
#print axioms c60F88FourFactorComposite
#print axioms c60F88DirectUnitPair_is_F83_tensor
#print axioms c60F88FourFactorComposite_eq_obstruction
#print axioms c60F88DirectUnitPair_charge
#print axioms c60F88Obstruction_charge_fourFactors
#print axioms c60F88Obstruction_charge_fiveFactors
#print axioms c60F88Tensorator_eq_F82_iff_charge_fourFactors_zero

end
end KUOS.DependentOriginationC60DirectTransportObstructionChargeV5_242
