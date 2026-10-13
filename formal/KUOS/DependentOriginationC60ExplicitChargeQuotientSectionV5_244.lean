import KUOS.DependentOriginationC60ObstructionFourGradeReductionV5_243

namespace KUOS.DependentOriginationC60ExplicitChargeQuotientSectionV5_244

open CategoryTheory
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60NativeChargeQuotientEquivalenceV5_233
open KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234
open KUOS.DependentOriginationC60QuotientTensorNaturalityV5_236
open KUOS.DependentOriginationC60ObstructionFourGradeReductionV5_243

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.244 / F90 — explicit zero-phase section of the ACTUAL F77 quotient

F89 reduced the F85/F82 obstruction to exactly four ZMod2-grade
pairs, but their numerical values still depend on the genuinely
constructed F79 equivalence unit and monoidal inverse construction.
The existing F79 equivalence uses Mathlib's asEquivalence and its
choice of essential-image witnesses; it is not sound to equate its
unit to a zero-charge unit by reflexivity.

Instead of replacing the established equivalence, F90 builds a
NEW, EXPLICIT functor from the original F75 typed integer-charge
groupoid into the actual F77 Mathlib quotient:
* canonical object at each original ZMod2 grade;
* for EVERY typed F75 arrow, the ORIGINAL Gray three-arrow of
  that charge and zero exchange phase, then F77 projection;
* exact identity and composition, preserving both integer charges;
* zero-charge objectwise roundtrip comparisons.

This is a concrete reference gauge in which later equivalence
comparison may be carried out without postulating that the
existing F79 noncomputable unit has zero charge.
The unmodified original Gray odd/odd interchange remains nontrivial
BEFORE the explicit phase-killing quotient. C60 north curvature -5
and the raw F54/F55 global mixed higher gluing remain separate.
-/

/-- A phase-zero native arrow with EXACTLY the two F75 charges,
between canonical native objects at the same source/target grades. -/
def c60F90PhaseZeroNative
    {X Y : C60F75StrictChargeGrade}
    (f : X ⟶ Y) :
    (⟨X.degree⟩ : GrayGrade) ⟶ (⟨Y.degree⟩ : GrayGrade) :=
  ⟨f.gradeEq, f.charge, 0⟩

/-- The concrete section acts on ORIGINAL F77 quotient Hom sets
by projecting a fully typed phase-zero Gray three-arrow. -/
def c60F90SectionMap
    {X Y : C60F75StrictChargeGrade} (f : X ⟶ Y) :
    c60F89CanonicalGrade X.degree ⟶
      c60F89CanonicalGrade Y.degree :=
  c60F77Projection.map (c60F90PhaseZeroNative f)

/-- Exact two-coordinate charge preservation, independently of
the F79 choice of its noncomputable quasi-inverse. -/
theorem c60F90SectionMap_charge
    {X Y : C60F75StrictChargeGrade} (f : X ⟶ Y) :
    (c60F77QuotientToStrictCharge.map
      (c60F90SectionMap f)).charge = f.charge := rfl

/-- Identity preservation by genuine Faithfulness of the original
F77 quotient-to-F75 functor. -/
theorem c60F90SectionMap_id (X : C60F75StrictChargeGrade) :
    c60F90SectionMap (𝟙 X) =
      𝟙 (c60F89CanonicalGrade X.degree) := by
  apply c60F80QuotientThree_ext
  change (0 : Int × Int) = 0
  rfl

/-- Vertical composition preservation on ALL F75 charge arrows;
both integer coordinates and source/target grade proofs survive. -/
theorem c60F90SectionMap_comp
    {X Y Z : C60F75StrictChargeGrade}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    c60F90SectionMap (f ≫ g) =
      c60F90SectionMap f ≫ c60F90SectionMap g := by
  apply c60F80QuotientThree_ext
  simp only [c60F80QuotientThree_comp_charge, c60F90SectionMap_charge]
  rfl

/-- The canonical phase-zero, two-integer-charge preserving
FUNCTOR to the original (not a replacement) F77 quotient category. -/
def c60F90ChargeToNativeQuotient :
    C60F75StrictChargeGrade ⥤ C60F77NativeQuotient where
  obj X := c60F89CanonicalGrade X.degree
  map := fun {_ _} f => c60F90SectionMap f
  map_id := c60F90SectionMap_id
  map_comp := fun f g => c60F90SectionMap_comp f g

/-- The F79 forward functor recovers every original strict-charge
grade object ON THE NOSE after the concrete canonical section. -/
theorem c60F90Section_leftObj
    (X : C60F75StrictChargeGrade) :
    c60F77QuotientToStrictCharge.obj
      (c60F90ChargeToNativeQuotient.obj X) = X := by
  cases X
  rfl

/-- The forward functor recovers exactly the ORIGINAL typed
F75 morphism from the chosen phase-zero F77 representative. -/
theorem c60F90Section_leftMap
    {X Y : C60F75StrictChargeGrade}
    (f : X ⟶ Y) :
    c60F77QuotientToStrictCharge.map
      (c60F90ChargeToNativeQuotient.map f) = f := by
  apply C60F75StrictChargeThree.ext
  exact c60F90SectionMap_charge f

/-- The concrete section reconstructs the original F77 quotient
object, not merely an isomorphic numerical parity label. -/
theorem c60F90Section_rightObj
    (X : C60F77NativeQuotient) :
    c60F90ChargeToNativeQuotient.obj
      (c60F77QuotientToStrictCharge.obj X) = X := by
  rcases X with ⟨⟨d⟩⟩
  rfl

/-- Faithfulness of the ORIGINAL F79 quotient-to-charge functor
makes the chosen zero-phase section inverse on EVERY genuine
quotient three-Hom, including those with nonzero integer charges. -/
theorem c60F90Section_rightMap
    {X Y : C60F77NativeQuotient}
    (f : X ⟶ Y) :
    c60F90ChargeToNativeQuotient.map
      (c60F77QuotientToStrictCharge.map f) = f := by
  rcases X with ⟨⟨x⟩⟩
  rcases Y with ⟨⟨y⟩⟩
  apply c60F80QuotientThree_ext
  rfl

/-- The canonical native roundtrip identity has ZERO of BOTH
integer charges: it is proof-by-equality, not a chosen F79 unit. -/
def c60F90CanonicalUnitIso
    (X : C60F77NativeQuotient) :
    X ≅ c60F90ChargeToNativeQuotient.obj
      (c60F77QuotientToStrictCharge.obj X) :=
  eqToIso (c60F90Section_rightObj X).symm

theorem c60F90CanonicalUnit_charge_zero
    (X : C60F77NativeQuotient) :
    (c60F77QuotientToStrictCharge.map
      (c60F90CanonicalUnitIso X).hom).charge =
      (0 : Int × Int) := by
  exact c60F82Quotient_eqToHom_charge_zero
    (c60F90Section_rightObj X).symm

/-- The canonical charge-groupoid roundtrip likewise has
zero charge and uses NO arbitrary essential-image isomorphism. -/
def c60F90CanonicalCounitIso
    (X : C60F75StrictChargeGrade) :
    c60F77QuotientToStrictCharge.obj
      (c60F90ChargeToNativeQuotient.obj X) ≅ X :=
  eqToIso (c60F90Section_leftObj X)

theorem c60F90CanonicalCounit_charge_zero
    (X : C60F75StrictChargeGrade) :
    (c60F90CanonicalCounitIso X).hom.charge =
      (0 : Int × Int) :=
  C60F75StrictChargeThree.eqToHom_charge_zero
    (c60F90Section_leftObj X)

#print axioms c60F90PhaseZeroNative
#print axioms c60F90SectionMap_charge
#print axioms c60F90SectionMap_id
#print axioms c60F90SectionMap_comp
#print axioms c60F90ChargeToNativeQuotient
#print axioms c60F90Section_leftObj
#print axioms c60F90Section_leftMap
#print axioms c60F90Section_rightObj
#print axioms c60F90Section_rightMap
#print axioms c60F90CanonicalUnitIso
#print axioms c60F90CanonicalUnit_charge_zero
#print axioms c60F90CanonicalCounit_charge_zero

end
end KUOS.DependentOriginationC60ExplicitChargeQuotientSectionV5_244
