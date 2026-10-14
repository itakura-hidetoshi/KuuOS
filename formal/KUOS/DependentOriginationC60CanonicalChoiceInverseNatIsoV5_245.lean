import KUOS.DependentOriginationC60ExplicitChargeQuotientSectionV5_244
import Mathlib.CategoryTheory.Functor.FullyFaithful
import Mathlib.CategoryTheory.NatIso

namespace KUOS.DependentOriginationC60CanonicalChoiceInverseNatIsoV5_245

open CategoryTheory
open KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60NativeChargeQuotientEquivalenceV5_233
open KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234
open KUOS.DependentOriginationC60QuotientTensorNaturalityV5_236
open KUOS.DependentOriginationC60MonoidalEquivalenceCompatibilityV5_238
open KUOS.DependentOriginationC60ObstructionFourGradeReductionV5_243
open KUOS.DependentOriginationC60ExplicitChargeQuotientSectionV5_244

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.245 / F91 — natural comparison of explicit and chosen F79 inverses

F90 constructed an explicit ORIGINAL F77 native quotient section of the
strict F75 two-coordinate charge functor. This section's own unit/counit
are zero-charge equality transports, but the existing F79 equivalence
uses mathlib's asEquivalence with a noncomputably selected quasi-inverse.

The two inverse functors are genuinely NATURALLY ISOMORPHIC:
each component is the faithful preimage in the ORIGINAL F77 quotient
of F90's canonical counit followed by the inverse of F79's chosen
counit. Its exact Int×Int charge is the charge of that chosen counit
inverse — which need NOT be zero. Naturality is proved by the
authentic F79 counit naturality and its FULL/FAITHFUL map, not by
silently identifying F79's chosen unit with F90's zero-charge gauge.

We also identify the actual F79 unit with the canonical F90
zero-charge unit followed by this correction component, preserving
all typed quotient Hom data and the two independent integer charges.

This compares two presentations of the PHASE-KILLING QUOTIENT only.
The original Gray exchange is nontrivial before quotienting, and the
F54/F55 raw global C60 tricategory and north -5 curvature remain
independent unsolved higher-geometric constraints.
-/

/-- An actual F75 isomorphism between the images of the EXPLICIT
F90 section and the ORIGINAL F79 chosen quasi-inverse. -/
def c60F91CounitComparisonIso (Y : C60F75StrictChargeGrade) :
    c60F77QuotientToStrictCharge.obj
        (c60F90ChargeToNativeQuotient.obj Y) ≅
      c60F77QuotientToStrictCharge.obj
        (c60F79NativeChargeEquivalence.inverse.obj Y) :=
  c60F90CanonicalCounitIso Y ≪≫
    (c60F79NativeChargeEquivalence.counitIso.app Y).symm

/-- The corresponding actual typed F77 quotient isomorphism:
lift the exact F75 counit comparison through F79's proven
full-faithful quotient-to-charge functor. -/
def c60F91ExplicitToChosenInverseIso (Y : C60F75StrictChargeGrade) :
    c60F90ChargeToNativeQuotient.obj Y ≅
      c60F79NativeChargeEquivalence.inverse.obj Y :=
  c60F77QuotientToStrictCharge.preimageIso
    (c60F91CounitComparisonIso Y)

/-- Mapping the comparison component back to the original F75
charge groupoid returns the comparison isomorphism EXACTLY. -/
theorem c60F91ExplicitToChosenInverse_map_hom
    (Y : C60F75StrictChargeGrade) :
    c60F77QuotientToStrictCharge.map
      (c60F91ExplicitToChosenInverseIso Y).hom =
      (c60F91CounitComparisonIso Y).hom := by
  change c60F77QuotientToStrictCharge.map
      (c60F77QuotientToStrictCharge.preimage
        (c60F91CounitComparisonIso Y).hom) =
      (c60F91CounitComparisonIso Y).hom
  exact c60F77QuotientToStrictCharge.map_preimage _

/-- Exact BOTH integer charges of the naturally required gauge
comparison. They are determined by the inverse of F79's chosen
counit, not assumed to be zero merely from equivalence. -/
theorem c60F91ExplicitToChosenInverse_charge
    (Y : C60F75StrictChargeGrade) :
    (c60F77QuotientToStrictCharge.map
      (c60F91ExplicitToChosenInverseIso Y).hom).charge =
      (c60F79NativeChargeEquivalence.counitIso.app Y).inv.charge := by
  rw [c60F91ExplicitToChosenInverse_map_hom]
  change ((c60F90CanonicalCounitIso Y).hom ≫
      (c60F79NativeChargeEquivalence.counitIso.app Y).inv).charge = _
  rw [c60F84Charge_comp, c60F90CanonicalCounit_charge_zero, zero_add]

/-- A bona fide Mathlib NatIso of functors on ALL original typed
F75 charge arrows, including nonzero Int×Int charges.
The proof uses the F79 counit inverse naturality and exact
faithfulness of the quotient map, not equality of chosen objects. -/
def c60F91ExplicitToChosenInverseNatIso :
    c60F90ChargeToNativeQuotient ≅
      c60F79NativeChargeEquivalence.inverse :=
  NatIso.ofComponents c60F91ExplicitToChosenInverseIso (by
    intro X Y f
    apply c60F77QuotientToStrictCharge.map_injective
    apply C60F75StrictChargeThree.ext
    have hn := congrArg C60F75StrictChargeThree.charge
      (c60F79NativeChargeEquivalence.counitInv_naturality f)
    simpa only [Functor.map_comp, c60F80QuotientThree_comp_charge,
      c60F90Section_leftMap, c60F91ExplicitToChosenInverse_charge,
      c60F84Charge_comp, Functor.comp_map, Functor.id_map]
      using hn)

/-- Actual F79 triangle compatibility: the F79 unit mapped to
F75 is precisely the inverse of the F79 chosen counit at FX. -/
theorem c60F91ChosenUnit_map_eq_counitInv
    (X : C60F77NativeQuotient) :
    c60F79NativeChargeEquivalence.functor.map
      (c60F79NativeChargeEquivalence.unitIso.app X).hom =
      (c60F79NativeChargeEquivalence.counitIso.app
        (c60F79NativeChargeEquivalence.functor.obj X)).inv := by
  let ε := c60F79NativeChargeEquivalence.counitIso.app
    (c60F79NativeChargeEquivalence.functor.obj X)
  have h := c60F79NativeChargeEquivalence.functor_unitIso_comp X
  calc
    c60F79NativeChargeEquivalence.functor.map
        (c60F79NativeChargeEquivalence.unitIso.app X).hom =
      (c60F79NativeChargeEquivalence.functor.map
        (c60F79NativeChargeEquivalence.unitIso.app X).hom ≫ ε.hom) ≫ ε.inv := by
          rw [Category.assoc, Iso.hom_inv_id, Category.comp_id]
    _ = 𝟙 _ ≫ ε.inv := by rw [h]
    _ = ε.inv := Category.id_comp _

/-- The F79 unit's actual two-integer-charge correction is the
charge of the F79 chosen counit inverse, NOT automatically zero. -/
theorem c60F91ChosenUnit_charge
    (X : C60F77NativeQuotient) :
    (c60F77QuotientToStrictCharge.map
      (c60F79NativeChargeEquivalence.unitIso.app X).hom).charge =
      (c60F79NativeChargeEquivalence.counitIso.app
        (c60F77QuotientToStrictCharge.obj X)).inv.charge := by
  exact congrArg C60F75StrictChargeThree.charge
    (c60F91ChosenUnit_map_eq_counitInv X)

/-- Both full, exact quotient-Hom gauge arrows coincide:
F79's chosen unit equals F90's ZERO-charge canonical unit,
followed by F91's NATURAL inverse comparison at the charge of X.
This provides an explicit transport bridge for F89's four classes. -/
theorem c60F91ChosenUnit_factorsThroughCanonical
    (X : C60F77NativeQuotient) :
    (c60F79NativeChargeEquivalence.unitIso.app X).hom =
      (c60F90CanonicalUnitIso X).hom ≫
        (c60F91ExplicitToChosenInverseIso
          (c60F77QuotientToStrictCharge.obj X)).hom := by
  apply c60F80QuotientThree_ext
  rw [c60F80QuotientThree_comp_charge,
    c60F90CanonicalUnit_charge_zero, zero_add]
  exact (c60F91ChosenUnit_charge X).trans
    (c60F91ExplicitToChosenInverse_charge
      (c60F77QuotientToStrictCharge.obj X)).symm

#print axioms c60F91CounitComparisonIso
#print axioms c60F91ExplicitToChosenInverseIso
#print axioms c60F91ExplicitToChosenInverse_map_hom
#print axioms c60F91ExplicitToChosenInverse_charge
#print axioms c60F91ExplicitToChosenInverseNatIso
#print axioms c60F91ChosenUnit_map_eq_counitInv
#print axioms c60F91ChosenUnit_charge
#print axioms c60F91ChosenUnit_factorsThroughCanonical

end
end KUOS.DependentOriginationC60CanonicalChoiceInverseNatIsoV5_245
