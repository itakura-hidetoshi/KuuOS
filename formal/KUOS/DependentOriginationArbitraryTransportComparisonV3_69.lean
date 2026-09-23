import KUOS.DependentOriginationCounterComparisonObstructionV3_68

namespace KUOS.DependentOriginationArbitraryTransportComparisonV3_69

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationCoherentComparisonFactorizationV2_60
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationCounterRepresentativeIdentityV3_66
open KUOS.DependentOriginationCounterCoherentQuotientTransportV3_67
open KUOS.DependentOriginationCounterComparisonObstructionV3_68

set_option autoImplicit false

attribute [local simp]
  CategoryTheory.Bicategory.Strict.leftUnitor_eqToIso
  CategoryTheory.Bicategory.Strict.rightUnitor_eqToIso
  CategoryTheory.Bicategory.Strict.associator_eqToIso

noncomputable section

/-!
# Arbitrary-transport Stage-II comparison reduction v3.69

v3.68 proves the Stage-II comparison obstruction for the explicit coherent
quotient transport constructed in v3.67.  The only transport-specific input in
that calculation is the scalar carried by the restricted quotient compositor.

This file removes that specialization.  For an arbitrary coherent quotient
transport `T`, its compositor on the image of a raw composable pair has a
well-defined scalar in `C2`.  Strong-transformation composition coherence then
says that the raw octahedral face scalar differs from the comparison
1-coboundary by exactly this transport-compositor scalar.

Summing the eight triangular equations cancels every comparison edge scalar
twice and leaves a single exact residual equation:

```text
1 = sum of the eight quotient-compositor scalars in ZMod 2.
```

Thus any successful Stage-II comparison must force the arbitrary quotient
transport to carry precisely the nontrivial octahedral parity class.  The next
step is to truth-test whether the three coherence laws of
`CoherentQuotientTransportData` force that eight-face sum to vanish, or permit
such a nontrivial class.
-/

/-- Stage-II comparison data over an arbitrary coherent quotient transport. -/
abbrev CounterComparisonDataAt
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :=
  CoherentPresentationComparisonData
    (W := allMorphisms) counterSystem counterD T

/-- Scalar component of an arbitrary Stage-II comparison on a raw arrow. -/
noncomputable def counterComparisonScalarAt
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (C : CounterComparisonDataAt T)
    {X Y : OctahedralVertex} (f : X ⟶ Y) : C2 :=
  (C.mapIso f).hom.toNatTrans.app (SingleObj.star C2)

/-- Scalar carried by the arbitrary quotient compositor on the localization
images of two composable raw arrows. -/
noncomputable def counterTransportCompScalar
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    {X Y Z : OctahedralVertex} (f : X ⟶ Y) (g : Y ⟶ Z) : C2 :=
  (T.mapComp (allMorphisms.Q.map f) (allMorphisms.Q.map g)).hom.toNatTrans.app
    (SingleObj.star C2)

/-- Every component of an arbitrary comparison natural transformation is its
unique `C2` scalar. -/
@[simp] theorem counterComparisonMapIso_hom_app_eq_scalar_at
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (C : CounterComparisonDataAt T)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    (A : CounterFiber) :
    (C.mapIso f).hom.toNatTrans.app A =
      counterComparisonScalarAt T C f := by
  cases A
  rfl

/-- Equality transport in the restricted system is scalar-trivial for every
choice of quotient coherence. -/
@[simp] theorem counterRestricted_eqToHom_eq_one_at
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (X : OctahedralVertex)
    {A B :
      (restrictedCoherentQuotientSystem
        allMorphisms counterSystem counterD T).obj (.mk X)}
    (h : A = B) :
    (eqToHom h : A ⟶ B) = (1 : C2) := by
  subst B
  rfl

/-- The map part of the restricted quotient system is independent of the
chosen quotient coherence and remains the identity functor on `CounterFiber`. -/
@[simp] theorem counterRestrictedMap_toFunctor_eq_id_at
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    {X Y : OctahedralVertex} (f : X ⟶ Y) :
    ((restrictedCoherentQuotientSystem
        allMorphisms counterSystem counterD T).map f.toLoc).toFunctor =
      𝟭 CounterFiber := by
  rw [restrictedCoherentQuotientSystem_map]
  exact
    counterQuotientRepresentativeMap_toFunctor_eq_id
      counterD (allMorphisms.Q.map f)

/-- The identity-component naturality wrapper preserves the underlying
comparison scalar for arbitrary quotient coherence. -/
@[simp] theorem counterIdentityComponentNaturalityIso_hom_app_at
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (C : CounterComparisonDataAt T)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    (A : CounterFiber) :
    (identityComponentNaturalityIso
        allMorphisms counterSystem counterD T
        f (C.mapIso f)).hom.toNatTrans.app A =
      counterComparisonScalarAt T C f := by
  set_option backward.isDefEq.respectTransparency false in
    simp [identityComponentNaturalityIso]

/-- After removing the strict double-opposite/restriction wrappers, the
restricted-system compositor is exactly the compositor selected by `T`. -/
@[simp] theorem counterRestrictedMapComp_hom_app_star_at
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    {X Y Z : OctahedralVertex} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((restrictedCoherentQuotientSystem
        allMorphisms counterSystem counterD T).mapComp
          f.toLoc g.toLoc).hom.toNatTrans.app (SingleObj.star C2) =
      counterTransportCompScalar T f g := by
  set_option backward.isDefEq.respectTransparency false in
    simp [restrictHigherLocalizedSystem,
      coherentQuotientLocalizedHigherSystem,
      quotientLocalizationPseudofunctor,
      higherPresentationUnitFunctor,
      CategoryTheory.Pseudofunctor.comp,
      CategoryTheory.Functor.toPseudofunctor,
      CategoryTheory.pseudofunctorOfIsLocallyDiscrete,
      CategoryTheory.LocallyDiscrete.mkPseudofunctor,
      counterTransportCompScalar]

/-- Stage-II composition coherence for arbitrary `T`: the raw compositor
equals the comparison coboundary times the quotient-compositor scalar. -/
theorem counterComparisonScalar_comp_at
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (C : CounterComparisonDataAt T)
    {X Y Z : OctahedralVertex} (f : X ⟶ Y) (g : Y ⟶ Z) :
    compScalar X Y Z * counterComparisonScalarAt T C (f ≫ g) =
      counterComparisonScalarAt T C f *
        counterComparisonScalarAt T C g *
        counterTransportCompScalar T f g := by
  have h := C.naturality_comp f g
  have hNat := congrArg (fun η => η.toNatTrans) h
  have hApp := NatTrans.congr_app hNat (SingleObj.star C2)
  set_option backward.isDefEq.respectTransparency false in
    simp only [Cat.Hom₂.comp_app, Cat.whiskerLeft_app,
      Cat.whiskerRight_app, Cat.associator_hom_app,
      Cat.associator_inv_app,
      counterIdentityComponentNaturalityIso_hom_app_at,
      counterRestrictedMapComp_hom_app_star_at,
      counterSystem_mapComp_hom_app,
      counterSystem_map_morphism_eq,
      counterSystem_eqToHom_eq_one,
      counterRestricted_eqToHom_eq_one_at,
      Cat.Hom.id_map] at hApp
  have hScalar := congrArg (fun k => counterSystemHomScalar Z k) hApp
  simp only [counterSystemHomScalar_comp] at hScalar
  simp only [counterSystemHomScalar] at hScalar
  simpa only [mul_one, one_mul, mul_assoc] using hScalar

/-- Face form of the arbitrary-transport comparison equation. -/
theorem counterComparisonScalar_triangle_at
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (C : CounterComparisonDataAt T)
    {L M H : OctahedralVertex}
    (a : L ⟶ M) (b : M ⟶ H) (c : L ⟶ H) :
    compScalar L M H * counterComparisonScalarAt T C c =
      counterComparisonScalarAt T C a *
        counterComparisonScalarAt T C b *
        counterTransportCompScalar T a b := by
  have h := counterComparisonScalar_comp_at T C a b
  rw [triangle_comp_eq a b c] at h
  exact h

/-- Any successful Stage-II comparison over an arbitrary coherent quotient
transport forces the eight quotient-compositor scalars to carry the nontrivial
octahedral parity class.

This is the exact residual left after every comparison-edge scalar cancels
twice. -/
theorem counterComparison_forces_transport_faceParity
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (C : CounterComparisonDataAt T) :
    (1 : ZMod 2) =
      Multiplicative.toAdd (counterTransportCompScalar T a00 b00) +
      Multiplicative.toAdd (counterTransportCompScalar T a01 b10) +
      Multiplicative.toAdd (counterTransportCompScalar T a00 b01) +
      Multiplicative.toAdd (counterTransportCompScalar T a01 b11) +
      Multiplicative.toAdd (counterTransportCompScalar T a10 b00) +
      Multiplicative.toAdd (counterTransportCompScalar T a11 b10) +
      Multiplicative.toAdd (counterTransportCompScalar T a10 b01) +
      Multiplicative.toAdd (counterTransportCompScalar T a11 b11) := by
  have h000 := counterComparisonScalar_triangle_at T C a00 b00 c00
  have h010 := counterComparisonScalar_triangle_at T C a01 b10 c00
  have h001 := counterComparisonScalar_triangle_at T C a00 b01 c01
  have h011 := counterComparisonScalar_triangle_at T C a01 b11 c01
  have h100 := counterComparisonScalar_triangle_at T C a10 b00 c10
  have h110 := counterComparisonScalar_triangle_at T C a11 b10 c10
  have h101 := counterComparisonScalar_triangle_at T C a10 b01 c11
  have h111 := counterComparisonScalar_triangle_at T C a11 b11 c11

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
          2 * Multiplicative.toAdd (counterComparisonScalarAt T C c00) +
          2 * Multiplicative.toAdd (counterComparisonScalarAt T C c01) +
          2 * Multiplicative.toAdd (counterComparisonScalarAt T C c10) +
          2 * Multiplicative.toAdd (counterComparisonScalarAt T C c11) =
        2 * Multiplicative.toAdd (counterComparisonScalarAt T C a00) +
          2 * Multiplicative.toAdd (counterComparisonScalarAt T C a01) +
          2 * Multiplicative.toAdd (counterComparisonScalarAt T C a10) +
          2 * Multiplicative.toAdd (counterComparisonScalarAt T C a11) +
          2 * Multiplicative.toAdd (counterComparisonScalarAt T C b00) +
          2 * Multiplicative.toAdd (counterComparisonScalarAt T C b01) +
          2 * Multiplicative.toAdd (counterComparisonScalarAt T C b10) +
          2 * Multiplicative.toAdd (counterComparisonScalarAt T C b11) +
          Multiplicative.toAdd (counterTransportCompScalar T a00 b00) +
          Multiplicative.toAdd (counterTransportCompScalar T a01 b10) +
          Multiplicative.toAdd (counterTransportCompScalar T a00 b01) +
          Multiplicative.toAdd (counterTransportCompScalar T a01 b11) +
          Multiplicative.toAdd (counterTransportCompScalar T a10 b00) +
          Multiplicative.toAdd (counterTransportCompScalar T a11 b10) +
          Multiplicative.toAdd (counterTransportCompScalar T a10 b01) +
          Multiplicative.toAdd (counterTransportCompScalar T a11 b11) := by
    linear_combination
      h000' + h010' + h001' + h011' +
      h100' + h110' + h101' + h111'

  simpa only [CharTwo.two_eq_zero, zero_mul, add_zero, zero_add] using hsum

/-!
## Boundary after the first v3.69 reduction

For arbitrary coherent quotient transport `T`, existence of Stage-II comparison
data implies that the eight pulled-back quotient compositors have odd total
parity.

The decisive remaining truth test is therefore exact and transport-only:

```text
Does T.map₂_associator + T.map₂_left_unitor + T.map₂_right_unitor
force the same eight-face parity sum to be 0?
```

If yes, every coherent quotient transport fails Stage II.  If no, an explicit
coherent transport with odd parity is the legitimate alternative target.
No universal obstruction theorem is asserted in this file yet.
-/

end

end KUOS.DependentOriginationArbitraryTransportComparisonV3_69
