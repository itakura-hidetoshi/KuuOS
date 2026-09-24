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


/-! ## Quotient-compositor cocycle on the localization -/

/-- Scalar of the arbitrary quotient compositor for arbitrary localization
arrows, not only arrows coming directly from the raw octahedral category. -/
noncomputable def counterTransportCompScalarLoc
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    {X Y Z : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) : C2 :=
  (T.mapComp f g).hom.toNatTrans.app (SingleObj.star C2)

/-- The hom component of an arbitrary quotient compositor is its unique scalar
at every object of the one-object counter fiber. -/
@[simp] theorem counterTransportMapComp_hom_app_eq_scalarLoc
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    {X Y Z : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (A : CounterFiber) :
    (T.mapComp f g).hom.toNatTrans.app A =
      counterTransportCompScalarLoc T f g := by
  cases A
  rfl

/-- The inverse component carries the inverse scalar. -/
@[simp] theorem counterTransportMapComp_inv_app_eq_inv_scalarLoc
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    {X Y Z : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (A : CounterFiber) :
    (T.mapComp f g).inv.toNatTrans.app A =
      (counterTransportCompScalarLoc T f g)⁻¹ := by
  cases A
  let invScalar : C2 :=
    (T.mapComp f g).inv.toNatTrans.app (SingleObj.star C2)
  change invScalar = (counterTransportCompScalarLoc T f g)⁻¹
  apply eq_inv_of_mul_eq_one_right
  dsimp [invScalar]
  simpa only [counterTransportCompScalarLoc, SingleObj.comp_as_mul,
    SingleObj.id_as_one] using
    (Cat.Hom.inv_hom_id_toNatTrans_app
      (T.mapComp f g) (SingleObj.star C2))

/-- Every quotient representative functor acts trivially on C2 morphisms. -/
@[simp] theorem counterQuotientRepresentativeMap_map_morphism_eq_at
    {X Y : allMorphisms.Localization} (f : X ⟶ Y)
    {A B : CounterFiber} (x : A ⟶ B) :
    (quotientRepresentativeMap
      allMorphisms counterSystem counterD f).toFunctor.map x = x := by
  rw [counterQuotientRepresentativeMap_toFunctor_eq_id]
  rfl

/-- The associator coherence law for an arbitrary coherent quotient transport
is exactly the additive 2-cocycle equation for its C2 compositor scalar. -/
theorem counterTransportCompScalarLoc_cocycle
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    {X Y Z K : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ K) :
    Multiplicative.toAdd
        (counterTransportCompScalarLoc T (f ≫ g) h) +
      Multiplicative.toAdd (counterTransportCompScalarLoc T f g) =
    Multiplicative.toAdd (counterTransportCompScalarLoc T g h) +
      Multiplicative.toAdd
        (counterTransportCompScalarLoc T f (g ≫ h)) := by
  have hAssoc := T.map₂_associator f g h
  have hNat := congrArg (fun η => η.toNatTrans) hAssoc
  have hApp := NatTrans.congr_app hNat (SingleObj.star C2)
  set_option backward.isDefEq.respectTransparency false in
    simp only [Cat.Hom₂.comp_app, Cat.whiskerLeft_app,
      Cat.whiskerRight_app, Cat.associator_hom_app,
      Cat.eqToHom_app,
      counterTransportMapComp_hom_app_eq_scalarLoc,
      counterTransportMapComp_inv_app_eq_inv_scalarLoc,
      counterQuotientRepresentativeMap_map_morphism_eq_at,
      counterSystem_eqToHom_eq_one] at hApp
  have hMul :
      (counterTransportCompScalarLoc T f (g ≫ h))⁻¹ *
          (counterTransportCompScalarLoc T g h)⁻¹ *
          counterTransportCompScalarLoc T f g *
          counterTransportCompScalarLoc T (f ≫ g) h =
        (1 : C2) := by
    simpa only [SingleObj.comp_as_mul, SingleObj.id_as_one,
      one_mul, mul_one, mul_assoc] using hApp
  have hAdd := congrArg (@Multiplicative.toAdd (ZMod 2)) hMul
  simp at hAdd
  have hPair :
      (Multiplicative.toAdd
          (counterTransportCompScalarLoc T (f ≫ g) h) +
        Multiplicative.toAdd (counterTransportCompScalarLoc T f g)) +
        (Multiplicative.toAdd (counterTransportCompScalarLoc T g h) +
          Multiplicative.toAdd
            (counterTransportCompScalarLoc T f (g ≫ h))) = 0 := by
    linear_combination hAdd
  exact CharTwo.add_eq_zero.mp hPair

/-! ## A middle switch in the localization -/

/-- The middle edge used to build the localization switch is admissible. -/
theorem b10_mem_allMorphisms : allMorphisms b10 := by
  trivial

/-- The lower edge used for explicit cancellation below is admissible. -/
theorem a00_mem_allMorphisms_v369 : allMorphisms a00 := by
  trivial

/-- A localization arrow switching M0 to M1 through H0.  It uses the direct
M0 -> H0 edge followed by the inverse of M1 -> H0. -/
noncomputable def counterMiddleSwitch :
    allMorphisms.Q.obj M0 ⟶ allMorphisms.Q.obj M1 :=
  allMorphisms.Q.map b00 ≫
    CategoryTheory.Localization.Construction.wInv
      (W := allMorphisms) b10 b10_mem_allMorphisms

/-- Syntactic hom-inverse law for b10, stated with the exact Q.map/wInv
presentation used by counterMiddleSwitch. -/
@[simp] theorem counterB10_comp_wInv :
    allMorphisms.Q.map b10 ≫
        CategoryTheory.Localization.Construction.wInv
          (W := allMorphisms) b10 b10_mem_allMorphisms =
      𝟙 (allMorphisms.Q.obj M1) := by
  exact
    (CategoryTheory.Localization.Construction.wIso
      (W := allMorphisms) b10 b10_mem_allMorphisms).hom_inv_id

/-- Syntactic inverse-hom law for b10. -/
@[simp] theorem counterWInv_b10_comp :
    CategoryTheory.Localization.Construction.wInv
          (W := allMorphisms) b10 b10_mem_allMorphisms ≫
        allMorphisms.Q.map b10 =
      𝟙 (allMorphisms.Q.obj H0) := by
  exact
    (CategoryTheory.Localization.Construction.wIso
      (W := allMorphisms) b10 b10_mem_allMorphisms).inv_hom_id

/-- Syntactic inverse-hom law for a00 used to cancel a common prefix. -/
@[simp] theorem counterWInv_a00_comp :
    CategoryTheory.Localization.Construction.wInv
          (W := allMorphisms) a00 a00_mem_allMorphisms_v369 ≫
        allMorphisms.Q.map a00 =
      𝟙 (allMorphisms.Q.obj M0) := by
  exact
    (CategoryTheory.Localization.Construction.wIso
      (W := allMorphisms) a00 a00_mem_allMorphisms_v369).inv_hom_id

/-- Raw triangular equality transported by the localization functor. -/
theorem counterLocalization_map_triangle
    {L M H : OctahedralVertex}
    (a : L ⟶ M) (b : M ⟶ H) (c : L ⟶ H) :
    allMorphisms.Q.map a ≫ allMorphisms.Q.map b =
      allMorphisms.Q.map c := by
  have h :=
    congrArg (fun k => allMorphisms.Q.map k)
      (triangle_comp_eq a b c)
  simpa only [Functor.map_comp] using h

/-- The M0 -> M1 switch carries the L0 -> M0 edge to L0 -> M1. -/
theorem counterA00_comp_middleSwitch :
    allMorphisms.Q.map a00 ≫ counterMiddleSwitch =
      allMorphisms.Q.map a01 := by
  unfold counterMiddleSwitch
  rw [← Category.assoc]
  rw [counterLocalization_map_triangle a00 b00 c00]
  rw [← counterLocalization_map_triangle a01 b10 c00]
  rw [Category.assoc]
  rw [counterB10_comp_wInv]
  rw [Category.comp_id]

/-- The same switch carries the L1 -> M0 edge to L1 -> M1. -/
theorem counterA10_comp_middleSwitch :
    allMorphisms.Q.map a10 ≫ counterMiddleSwitch =
      allMorphisms.Q.map a11 := by
  unfold counterMiddleSwitch
  rw [← Category.assoc]
  rw [counterLocalization_map_triangle a10 b00 c10]
  rw [← counterLocalization_map_triangle a11 b10 c10]
  rw [Category.assoc]
  rw [counterB10_comp_wInv]
  rw [Category.comp_id]

/-- Postcomposing the middle switch with b10 recovers b00. -/
theorem counterMiddleSwitch_comp_b10 :
    counterMiddleSwitch ≫ allMorphisms.Q.map b10 =
      allMorphisms.Q.map b00 := by
  unfold counterMiddleSwitch
  rw [Category.assoc]
  rw [counterWInv_b10_comp]
  rw [Category.comp_id]

/-- Postcomposing the same switch with b11 recovers b01.  The proof first
checks the equality after precomposition by Q(a00), then cancels Q(a00) by its
explicit localization inverse. -/
theorem counterMiddleSwitch_comp_b11 :
    counterMiddleSwitch ≫ allMorphisms.Q.map b11 =
      allMorphisms.Q.map b01 := by
  have hpre :
      allMorphisms.Q.map a00 ≫
          (counterMiddleSwitch ≫ allMorphisms.Q.map b11) =
        allMorphisms.Q.map a00 ≫ allMorphisms.Q.map b01 := by
    calc
      allMorphisms.Q.map a00 ≫
          (counterMiddleSwitch ≫ allMorphisms.Q.map b11) =
          (allMorphisms.Q.map a00 ≫ counterMiddleSwitch) ≫
            allMorphisms.Q.map b11 := by
              rw [Category.assoc]
      _ = allMorphisms.Q.map a01 ≫ allMorphisms.Q.map b11 := by
            rw [counterA00_comp_middleSwitch]
      _ = allMorphisms.Q.map c01 :=
            counterLocalization_map_triangle a01 b11 c01
      _ = allMorphisms.Q.map a00 ≫ allMorphisms.Q.map b01 :=
            (counterLocalization_map_triangle a00 b01 c01).symm
  have hcancel := congrArg
    (fun k =>
      CategoryTheory.Localization.Construction.wInv
          (W := allMorphisms) a00 a00_mem_allMorphisms_v369 ≫ k)
    hpre
  simpa only [← Category.assoc, counterWInv_a00_comp,
    Category.id_comp] using hcancel

/-! ## The transport parity is forced to vanish -/

/-- One associator cocycle equation pairs the two octahedral faces adjacent
across a chosen middle switch. -/
theorem counterTransport_facePair_balance
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    {X Y₀ Y₁ Z : allMorphisms.Localization}
    (a₀ : X ⟶ Y₀) (p : Y₀ ⟶ Y₁) (b₁ : Y₁ ⟶ Z)
    (a₁ : X ⟶ Y₁) (b₀ : Y₀ ⟶ Z)
    (ha : a₀ ≫ p = a₁) (hb : p ≫ b₁ = b₀) :
    Multiplicative.toAdd (counterTransportCompScalarLoc T a₁ b₁) +
        Multiplicative.toAdd (counterTransportCompScalarLoc T a₀ p) =
      Multiplicative.toAdd (counterTransportCompScalarLoc T p b₁) +
        Multiplicative.toAdd (counterTransportCompScalarLoc T a₀ b₀) := by
  simpa only [ha, hb] using
    (counterTransportCompScalarLoc_cocycle T a₀ p b₁)

/-- The sum of all eight quotient-compositor scalars on the octahedral faces is
zero for every coherent quotient transport.  This is the transport-independent
half of the Stage-II obstruction. -/
theorem counterTransport_faceParity_even
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    Multiplicative.toAdd (counterTransportCompScalar T a00 b00) +
      Multiplicative.toAdd (counterTransportCompScalar T a01 b10) +
      Multiplicative.toAdd (counterTransportCompScalar T a00 b01) +
      Multiplicative.toAdd (counterTransportCompScalar T a01 b11) +
      Multiplicative.toAdd (counterTransportCompScalar T a10 b00) +
      Multiplicative.toAdd (counterTransportCompScalar T a11 b10) +
      Multiplicative.toAdd (counterTransportCompScalar T a10 b01) +
      Multiplicative.toAdd (counterTransportCompScalar T a11 b11) = 0 := by
  have h00 :=
    counterTransport_facePair_balance T
      (allMorphisms.Q.map a00) counterMiddleSwitch
      (allMorphisms.Q.map b10)
      (allMorphisms.Q.map a01) (allMorphisms.Q.map b00)
      counterA00_comp_middleSwitch counterMiddleSwitch_comp_b10
  have h01 :=
    counterTransport_facePair_balance T
      (allMorphisms.Q.map a00) counterMiddleSwitch
      (allMorphisms.Q.map b11)
      (allMorphisms.Q.map a01) (allMorphisms.Q.map b01)
      counterA00_comp_middleSwitch counterMiddleSwitch_comp_b11
  have h10 :=
    counterTransport_facePair_balance T
      (allMorphisms.Q.map a10) counterMiddleSwitch
      (allMorphisms.Q.map b10)
      (allMorphisms.Q.map a11) (allMorphisms.Q.map b00)
      counterA10_comp_middleSwitch counterMiddleSwitch_comp_b10
  have h11 :=
    counterTransport_facePair_balance T
      (allMorphisms.Q.map a10) counterMiddleSwitch
      (allMorphisms.Q.map b11)
      (allMorphisms.Q.map a11) (allMorphisms.Q.map b01)
      counterA10_comp_middleSwitch counterMiddleSwitch_comp_b11

  let A : ZMod 2 :=
    Multiplicative.toAdd
        (counterTransportCompScalarLoc T
          (allMorphisms.Q.map a01) (allMorphisms.Q.map b10)) +
      Multiplicative.toAdd
        (counterTransportCompScalarLoc T
          (allMorphisms.Q.map a01) (allMorphisms.Q.map b11)) +
      Multiplicative.toAdd
        (counterTransportCompScalarLoc T
          (allMorphisms.Q.map a11) (allMorphisms.Q.map b10)) +
      Multiplicative.toAdd
        (counterTransportCompScalarLoc T
          (allMorphisms.Q.map a11) (allMorphisms.Q.map b11))
  let D : ZMod 2 :=
    Multiplicative.toAdd
        (counterTransportCompScalarLoc T
          (allMorphisms.Q.map a00) (allMorphisms.Q.map b00)) +
      Multiplicative.toAdd
        (counterTransportCompScalarLoc T
          (allMorphisms.Q.map a00) (allMorphisms.Q.map b01)) +
      Multiplicative.toAdd
        (counterTransportCompScalarLoc T
          (allMorphisms.Q.map a10) (allMorphisms.Q.map b00)) +
      Multiplicative.toAdd
        (counterTransportCompScalarLoc T
          (allMorphisms.Q.map a10) (allMorphisms.Q.map b01))

  have hAD : A = D := by
    dsimp [A, D]
    have hsum :
        Multiplicative.toAdd
              (counterTransportCompScalarLoc T
                (allMorphisms.Q.map a01) (allMorphisms.Q.map b10)) +
            Multiplicative.toAdd
              (counterTransportCompScalarLoc T
                (allMorphisms.Q.map a01) (allMorphisms.Q.map b11)) +
            Multiplicative.toAdd
              (counterTransportCompScalarLoc T
                (allMorphisms.Q.map a11) (allMorphisms.Q.map b10)) +
            Multiplicative.toAdd
              (counterTransportCompScalarLoc T
                (allMorphisms.Q.map a11) (allMorphisms.Q.map b11)) +
            2 * Multiplicative.toAdd
              (counterTransportCompScalarLoc T
                (allMorphisms.Q.map a00) counterMiddleSwitch) +
            2 * Multiplicative.toAdd
              (counterTransportCompScalarLoc T
                (allMorphisms.Q.map a10) counterMiddleSwitch) =
          2 * Multiplicative.toAdd
              (counterTransportCompScalarLoc T
                counterMiddleSwitch (allMorphisms.Q.map b10)) +
            2 * Multiplicative.toAdd
              (counterTransportCompScalarLoc T
                counterMiddleSwitch (allMorphisms.Q.map b11)) +
            Multiplicative.toAdd
              (counterTransportCompScalarLoc T
                (allMorphisms.Q.map a00) (allMorphisms.Q.map b00)) +
            Multiplicative.toAdd
              (counterTransportCompScalarLoc T
                (allMorphisms.Q.map a00) (allMorphisms.Q.map b01)) +
            Multiplicative.toAdd
              (counterTransportCompScalarLoc T
                (allMorphisms.Q.map a10) (allMorphisms.Q.map b00)) +
            Multiplicative.toAdd
              (counterTransportCompScalarLoc T
                (allMorphisms.Q.map a10) (allMorphisms.Q.map b01)) := by
      linear_combination h00 + h01 + h10 + h11
    simpa only [CharTwo.two_eq_zero, zero_mul, add_zero, zero_add] using hsum

  have hTotalLoc : D + A = 0 := by
    rw [← hAD]
    exact CharTwo.add_self_eq_zero A

  dsimp [D, A] at hTotalLoc
  have hTargetLoc :
      Multiplicative.toAdd
          (counterTransportCompScalarLoc T
            (allMorphisms.Q.map a00) (allMorphisms.Q.map b00)) +
        Multiplicative.toAdd
          (counterTransportCompScalarLoc T
            (allMorphisms.Q.map a01) (allMorphisms.Q.map b10)) +
        Multiplicative.toAdd
          (counterTransportCompScalarLoc T
            (allMorphisms.Q.map a00) (allMorphisms.Q.map b01)) +
        Multiplicative.toAdd
          (counterTransportCompScalarLoc T
            (allMorphisms.Q.map a01) (allMorphisms.Q.map b11)) +
        Multiplicative.toAdd
          (counterTransportCompScalarLoc T
            (allMorphisms.Q.map a10) (allMorphisms.Q.map b00)) +
        Multiplicative.toAdd
          (counterTransportCompScalarLoc T
            (allMorphisms.Q.map a11) (allMorphisms.Q.map b10)) +
        Multiplicative.toAdd
          (counterTransportCompScalarLoc T
            (allMorphisms.Q.map a10) (allMorphisms.Q.map b01)) +
        Multiplicative.toAdd
          (counterTransportCompScalarLoc T
            (allMorphisms.Q.map a11) (allMorphisms.Q.map b11)) = 0 := by
    linear_combination hTotalLoc
  simpa only [counterTransportCompScalar, counterTransportCompScalarLoc] using
    hTargetLoc

/-- Canonical v3.69 theorem: no coherent quotient transport on the concrete C2
countermodel admits a Stage-II coherent presentation comparison. -/
theorem counterD_noCoherentPresentationComparison_for_all_transports :
    ∀ T : CoherentQuotientTransportData
        (W := allMorphisms) counterSystem counterD,
      ¬ HasCoherentPresentationComparisonData
          allMorphisms counterSystem counterD T := by
  intro T hComparison
  rcases hComparison with ⟨C⟩
  have hOdd := counterComparison_forces_transport_faceParity T C
  have hEven := counterTransport_faceParity_even T
  exact one_ne_zero (hOdd.trans hEven)

/-- The Stage-I coherent quotient carrier exists, but every such carrier fails
the Stage-II comparison in the concrete truth test. -/
theorem counterD_stageI_exists_but_every_stageII_comparison_fails :
    HasCoherentQuotientTransportData
        allMorphisms counterSystem counterD ∧
      (∀ T : CoherentQuotientTransportData
          (W := allMorphisms) counterSystem counterD,
        ¬ HasCoherentPresentationComparisonData
            allMorphisms counterSystem counterD T) := by
  exact ⟨counterD_hasCoherentQuotientTransportData,
    counterD_noCoherentPresentationComparison_for_all_transports⟩

/-- Consequently the exact five-law package built from the canonical pointwise
datum is empty.  This does not by itself assert that every possible
HigherLocalizationFactorization is impossible; that still requires a separate
necessity/bridge theorem. -/
theorem counterD_not_hasCoherentGeneralWFactorizationData :
    ¬ HasCoherentGeneralWFactorizationData
        allMorphisms counterSystem counterD := by
  rintro ⟨H⟩
  exact
    (counterD_noCoherentPresentationComparison_for_all_transports H.transport)
      ⟨H.comparison⟩

/-!
## Boundary after v3.69

For the concrete octahedral C2 truth test the Stage-II obstruction is now
transport-independent.

For every coherent quotient transport `T`:

* its compositor scalar satisfies the associator 2-cocycle equation;
* a single localization middle switch pairs the eight octahedral faces;
* the total quotient-compositor parity is therefore zero in `ZMod 2`;
* any Stage-II coherent presentation comparison would force that same parity
  to be one;
* hence no coherent quotient transport admits such a comparison.

Thus Stage I still exists, while Stage II fails for every coherent quotient
transport based on the canonical pointwise datum `counterD`.

This still does not identify `HasCoherentGeneralWFactorizationData` with the
full abstract `HasHigherLocalizationFactorization` interface.  No global
non-factorization or universality claim is made without a separate exact bridge
theorem.
-/

end

end KUOS.DependentOriginationArbitraryTransportComparisonV3_69
