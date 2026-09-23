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
open KUOS.DependentOriginationCounterRepresentativeIdentityV3_66
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

/-- Every raw fiber object is definitionally the same one-object C2 category.
Keeping this reduction as an explicit simp lemma lets component-level
`eqToHom` terms normalize without unfolding the whole counter pseudofunctor. -/
@[simp] theorem counterSystem_obj_eq_counterFiber
    (X : OctahedralVertex) :
    counterSystem.obj (.mk X) = Cat.of CounterFiber := by
  rfl

/-- Equality transport in the one-object C2 fiber is always the unit scalar. -/
@[simp] theorem counterFiber_eqToHom_eq_one
    {A B : CounterFiber} (h : A = B) :
    (eqToHom h : A ⟶ B) = (1 : C2) := by
  subst B
  rfl

/-- Equality transport inside a raw counterSystem fiber is the unit C2
morphism.  This formulation matches the dependent category parameter directly,
so simp need not rewrite the ambient Cat object first. -/
@[simp] theorem counterSystem_eqToHom_eq_one
    (X : OctahedralVertex)
    {A B : counterSystem.obj (.mk X)} (h : A = B) :
    (eqToHom h : A ⟶ B) = (1 : C2) := by
  subst B
  rfl

/-- The same normalization for an object of the restricted quotient-stage
system. -/
@[simp] theorem counterRestricted_eqToHom_eq_one
    (X : OctahedralVertex)
    {A B :
      (restrictedCoherentQuotientSystem
        allMorphisms counterSystem counterD
        counterD_coherentQuotientTransportData).obj (.mk X)}
    (h : A = B) :
    (eqToHom h : A ⟶ B) = (1 : C2) := by
  subst B
  rfl

/-- Read any morphism in the one-object counter fiber as its underlying C2
scalar.  Keeping this as a named map lets us transport an equality of dependent
fiber morphisms into the monoid without asking simp to recognize the ambient
Cat object syntactically. -/
def counterFiberHomScalar
    {A B : CounterFiber} (p : A ⟶ B) : C2 :=
  p

/-- Scalarization reverses categorical composition exactly as dictated by the
SingleObj category structure. -/
theorem counterFiberHomScalar_comp
    {A B D : CounterFiber} (p : A ⟶ B) (q : B ⟶ D) :
    counterFiberHomScalar (p ≫ q) =
      counterFiberHomScalar q * counterFiberHomScalar p := by
  rfl

/-- Every component of a comparison natural transformation is the same scalar,
because CounterFiber has only one object. -/
@[simp] theorem counterComparisonMapIso_hom_app_eq_scalar
    (C : CounterComparisonData)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    (A : CounterFiber) :
    (C.mapIso f).hom.toNatTrans.app A =
      counterComparisonScalar C f := by
  cases A
  rfl

/-- Every raw counterSystem functor fixes every C2 morphism. -/
@[simp] theorem counterSystem_map_morphism_eq
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    {A B : CounterFiber} (x : A ⟶ B) :
    (counterSystem.map f.toLoc).toFunctor.map x = x := by
  rw [counterSystem_map_toFunctor]
  rfl


/-- Every raw arrow of the restricted v3.67 quotient system still acts by the
identity functor.  This is the v3.66 representative collapse transported only
through the already-proved restriction map formula, avoiding expansion of the
whole pseudofunctor composition. -/
@[simp] theorem counterRestrictedMap_toFunctor_eq_id
    {X Y : OctahedralVertex} (f : X ⟶ Y) :
    ((restrictedCoherentQuotientSystem
        allMorphisms counterSystem counterD
        counterD_coherentQuotientTransportData).map f.toLoc).toFunctor =
      𝟭 CounterFiber := by
  rw [restrictedCoherentQuotientSystem_map]
  exact
    counterQuotientRepresentativeMap_toFunctor_eq_id
      counterD (allMorphisms.Q.map f)

/-- The raw compositor contributes exactly the finite C2 face scalar. -/
@[simp] theorem counterSystem_mapComp_hom_app
    {X Y Z : OctahedralVertex} (f : X ⟶ Y) (g : Y ⟶ Z)
    (A : CounterFiber) :
    (counterSystem.mapComp f.toLoc g.toLoc).hom.toNatTrans.app A =
      compScalar X Y Z := by
  cases A
  exact counterMapComp_hom_app_star X Y Z

/-- The identity-component naturality wrapper does not alter the scalar carried
by the chosen comparison map. -/
@[simp] theorem counterIdentityComponentNaturalityIso_hom_app
    (C : CounterComparisonData)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    (A : CounterFiber) :
    (identityComponentNaturalityIso
        allMorphisms counterSystem counterD
        counterD_coherentQuotientTransportData
        f (C.mapIso f)).hom.toNatTrans.app A =
      counterComparisonScalar C f := by
  set_option backward.isDefEq.respectTransparency false in
    simp [identityComponentNaturalityIso]

/-- The compositor of the restricted v3.67 quotient system is scalar-trivial.
Only this local structural computation unfolds the pseudofunctor-composition
wrappers; downstream scalar algebra uses the lemma as a black box. -/
@[simp] theorem counterRestrictedMapComp_hom_app_star
    {X Y Z : OctahedralVertex} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((restrictedCoherentQuotientSystem
        allMorphisms counterSystem counterD
        counterD_coherentQuotientTransportData).mapComp
          f.toLoc g.toLoc).hom.toNatTrans.app (SingleObj.star C2) =
      eqToHom (by
        change (_ : CounterFiber) = _
        exact Subsingleton.elim _ _) := by
  set_option backward.isDefEq.respectTransparency false in
    simp [restrictHigherLocalizedSystem,
      coherentQuotientLocalizedHigherSystem,
      quotientLocalizationPseudofunctor,
      higherPresentationUnitFunctor,
      CategoryTheory.Pseudofunctor.comp,
      CategoryTheory.Functor.toPseudofunctor,
      CategoryTheory.pseudofunctorOfIsLocallyDiscrete,
      CategoryTheory.LocallyDiscrete.mkPseudofunctor,
      counterD_coherentQuotientTransportData,
      counterQuotientMapComp]

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
    simp only [Cat.Hom₂.comp_app, Cat.whiskerLeft_app,
      Cat.whiskerRight_app, Cat.associator_hom_app,
      Cat.associator_inv_app,
      counterIdentityComponentNaturalityIso_hom_app,
      counterRestrictedMapComp_hom_app_star,
      counterSystem_mapComp_hom_app,
      counterSystem_map_morphism_eq,
      counterSystem_eqToHom_eq_one,
      counterRestricted_eqToHom_eq_one,
      Cat.Hom.id_map] at hApp
  have hScalar := congrArg (fun k => counterFiberHomScalar k) hApp
  simp only [counterFiberHomScalar_comp] at hScalar
  simp only [counterFiberHomScalar] at hScalar
  simpa only [mul_one, one_mul] using hScalar

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

  have hsum :
      (1 : ZMod 2) +
          2 * Multiplicative.toAdd (counterComparisonScalar C c00) +
          2 * Multiplicative.toAdd (counterComparisonScalar C c01) +
          2 * Multiplicative.toAdd (counterComparisonScalar C c10) +
          2 * Multiplicative.toAdd (counterComparisonScalar C c11) =
        2 * Multiplicative.toAdd (counterComparisonScalar C a00) +
          2 * Multiplicative.toAdd (counterComparisonScalar C a01) +
          2 * Multiplicative.toAdd (counterComparisonScalar C a10) +
          2 * Multiplicative.toAdd (counterComparisonScalar C a11) +
          2 * Multiplicative.toAdd (counterComparisonScalar C b00) +
          2 * Multiplicative.toAdd (counterComparisonScalar C b01) +
          2 * Multiplicative.toAdd (counterComparisonScalar C b10) +
          2 * Multiplicative.toAdd (counterComparisonScalar C b11) := by
    linear_combination
      h000' + h010' + h001' + h011' +
      h100' + h110' + h101' + h111'
  have hzero : (1 : ZMod 2) = 0 := by
    simpa only [CharTwo.two_eq_zero, zero_mul, add_zero, zero_add] using hsum
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
