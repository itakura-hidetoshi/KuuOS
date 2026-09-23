import KUOS.DependentOriginationCounterCoherentQuotientTransportV3_67
import Mathlib.Tactic.LinearCombination

namespace KUOS.DependentOriginationCounterComparisonObstructionV3_68

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationCoherentComparisonFactorizationV2_60
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationCounterCoherentQuotientTransportV3_67

set_option autoImplicit false

attribute [local simp]
  CategoryTheory.Bicategory.Strict.leftUnitor_eqToIso
  CategoryTheory.Bicategory.Strict.rightUnitor_eqToIso
  CategoryTheory.Bicategory.Strict.associator_eqToIso

noncomputable section

/-!
# Stage-II comparison obstruction for the canonical counter quotient transport v3.68

v3.67 constructs an explicit coherent quotient transport for the octahedral C2
countermodel.  This file truth-tests the remaining Stage-II comparison back to
the raw pseudofunctor.

Every raw and quotient 1-cell acts by the identity functor on the one-object C2
fiber.  Therefore a presentation-comparison 2-isomorphism on a raw arrow has a
single scalar component in C2.  The StrongTrans composition law says that these
edge scalars form a 1-cochain whose coboundary equals the raw compositor scalar.

On the eight triangular faces of the octahedron, summing those equations in
ZMod 2 cancels every edge scalar twice.  The seven untwisted faces contribute
zero, while the distinguished L0-M0-H0 face contributes one.  This yields
1 = 0 in ZMod 2, a contradiction.

The conclusion is deliberately relative to the explicit coherent quotient
transport constructed in v3.67.  It does not yet say that every possible
coherent quotient transport or every quotient gauge has the same Stage-II
obstruction.
-/

abbrev CounterComparisonData :=
  CoherentPresentationComparisonData
    (W := allMorphisms) counterSystem counterD
      counterD_coherentQuotientTransportData

/-- Scalar component of a comparison 2-isomorphism at the unique object of the
countermodel fiber. -/
noncomputable def counterComparisonScalar
    (C : CounterComparisonData)
    {X Y : OctahedralVertex} (f : X ⟶ Y) : C2 :=
  (C.mapIso f).hom.toNatTrans.app (SingleObj.star C2)

/-- Stage-II composition coherence becomes the scalar coboundary equation. -/
theorem counterComparisonScalar_comp
    (C : CounterComparisonData)
    {X Y Z : OctahedralVertex} (f : X ⟶ Y) (g : Y ⟶ Z) :
    compScalar X Y Z * counterComparisonScalar C (f ≫ g) =
      counterComparisonScalar C f * counterComparisonScalar C g := by
  have h := C.naturality_comp f g
  have hNat := congrArg (fun η => η.toNatTrans) h
  have hApp := NatTrans.congr_app hNat (SingleObj.star C2)
  set_option backward.isDefEq.respectTransparency false in
    simpa [counterComparisonScalar,
      identityComponentNaturalityIso,
      restrictedCoherentQuotientSystem,
      coherentQuotientLocalizedHigherSystem,
      quotientLocalizationPseudofunctor,
      higherPresentationUnitFunctor,
      CategoryTheory.Pseudofunctor.comp,
      CategoryTheory.Functor.toPseudofunctor,
      CategoryTheory.pseudofunctorOfIsLocallyDiscrete,
      counterD_coherentQuotientTransportData,
      counterQuotientMapId, counterQuotientMapComp,
      counterQuotientRepresentativeMap_toFunctor_eq_id,
      counterSystem] using hApp

/-- On an octahedral triangular face, replace the composite arrow by the named
direct lower-to-upper edge. -/
theorem counterComparisonScalar_triangle
    (C : CounterComparisonData)
    {L M H : OctahedralVertex}
    (a : L ⟶ M) (b : M ⟶ H) (c : L ⟶ H) :
    compScalar L M H * counterComparisonScalar C c =
      counterComparisonScalar C a * counterComparisonScalar C b := by
  have h := counterComparisonScalar_comp C a b
  rw [triangle_comp_eq a b c] at h
  exact h

/-- The eight face equations cannot be solved simultaneously: their mod-2 sum
would force the nontrivial C2 scalar to be trivial. -/
theorem not_counterComparisonData :
    ¬ Nonempty CounterComparisonData := by
  rintro ⟨C⟩
  have h000 := counterComparisonScalar_triangle C a00 b00 c00
  have h010 := counterComparisonScalar_triangle C a01 b10 c00
  have h001 := counterComparisonScalar_triangle C a00 b01 c01
  have h011 := counterComparisonScalar_triangle C a01 b11 c01
  have h100 := counterComparisonScalar_triangle C a10 b00 c10
  have h110 := counterComparisonScalar_triangle C a11 b10 c10
  have h101 := counterComparisonScalar_triangle C a10 b01 c11
  have h111 := counterComparisonScalar_triangle C a11 b11 c11

  have h000' := congrArg (@Multiplicative.toAdd (ZMod 2)) h000
  have h010' := congrArg (@Multiplicative.toAdd (ZMod 2)) h010
  have h001' := congrArg (@Multiplicative.toAdd (ZMod 2)) h001
  have h011' := congrArg (@Multiplicative.toAdd (ZMod 2)) h011
  have h100' := congrArg (@Multiplicative.toAdd (ZMod 2)) h100
  have h110' := congrArg (@Multiplicative.toAdd (ZMod 2)) h110
  have h101' := congrArg (@Multiplicative.toAdd (ZMod 2)) h101
  have h111' := congrArg (@Multiplicative.toAdd (ZMod 2)) h111

  simp [zeta] at h000' h010' h001' h011' h100' h110' h101' h111'

  have hzero : (1 : ZMod 2) = 0 := by
    linear_combination
      h000' + h010' + h001' + h011' +
      h100' + h110' + h101' + h111'
  exact one_ne_zero hzero

/-- The explicit coherent quotient transport of v3.67 admits no coherent
presentation comparison back to the raw twisted counterSystem. -/
theorem counterD_not_hasCoherentPresentationComparisonData :
    ¬ HasCoherentPresentationComparisonData
      allMorphisms counterSystem counterD
        counterD_coherentQuotientTransportData := by
  exact not_counterComparisonData

/-!
## Boundary after v3.68

For the explicit v3.67 quotient transport:

* Stage I succeeds: coherent quotient transport exists;
* Stage II fails: no coherent presentation comparison exists.

Thus the raw octahedral twist survives after the 1-cell quotient assignment and
after quotient pseudofunctor coherence have both been solved.  In this
presentation it is exactly a comparison-lift obstruction.

This is still a transport-specific Stage-II theorem.  The next stronger target
is gauge independence: decide whether every coherent quotient transport /
every common quotient gauge has the same comparison obstruction, or whether a
different quotient coherence can absorb the raw C2 2-cocycle.
-/

end

end KUOS.DependentOriginationCounterComparisonObstructionV3_68
