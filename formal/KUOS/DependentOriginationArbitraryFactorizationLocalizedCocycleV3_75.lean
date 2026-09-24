import KUOS.DependentOriginationArbitraryFactorizationParityV3_74

namespace KUOS.DependentOriginationArbitraryFactorizationLocalizedCocycleV3_75

open CategoryTheory
open CategoryTheory.Bicategory
open Opposite
open KUOS.DependentOriginationPresentationUniversalityV2_0
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationCounterComparisonObstructionV3_68
open KUOS.DependentOriginationArbitraryFactorizationScalarV3_72
open KUOS.DependentOriginationFactorizationObjectCoboundaryV3_73
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74

set_option autoImplicit false

attribute [local simp]
  CategoryTheory.Bicategory.Strict.leftUnitor_eqToIso
  CategoryTheory.Bicategory.Strict.rightUnitor_eqToIso
  CategoryTheory.Bicategory.Strict.associator_eqToIso
  CategoryTheory.PrelaxFunctor.map₂_eqToHom
  CategoryTheory.eqToHom_map
  CategoryTheory.Cat.eqToHom_app

noncomputable section

/-!
# Arbitrary-factorization localized compositor cocycle v3.75

v3.74 reduces the raw octahedral odd class to four explicit inter-object
coboundaries plus eight compositor scalars of the arbitrary localized lift.

The next required step is not another raw-face calculation.  The middle switch
used in v3.69 is a genuine localization arrow, so the compositor of an arbitrary
factorization must first be exposed on the whole localization, not only after
restriction back to raw arrows.

This file therefore takes an arbitrary

```text
H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem
```

and views `H.lift` directly as a pseudofunctor on the ordinary localization by
precomposing with Mathlib's double-opposite functor.  Its map-compositor is then
scalarized only after mapping the exact Cat component through the comparison
functor at a raw endpoint.

For a composable localization triple

```text
X --f--> Y --g--> Z --h--> Q(T)
```

the pseudofunctor associator gives the exact additive balance

```text
comp(fg,h,A) + transported_h(comp(f,g,A))
  =
comp(g,h,F(f)A) + comp(f,gh,A)
```

in `ZMod 2`.

The transported term is intentionally retained.  Removing it prematurely would
repeat the forbidden object-independence step from v3.72-v3.73.  This equation
is the localization-level input needed to pair the v3.74 residual across
`counterMiddleSwitch`.
-/

/-- The arbitrary localized lift, viewed on the ordinary localization rather
than on its double opposite. -/
noncomputable def counterFactorizationLocalizationView
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem) :
    Pseudofunctor
      (LocallyDiscrete allMorphisms.Localization) Cat :=
  Pseudofunctor.comp
    (opOp allMorphisms.Localization).toPseudofunctor
    H.lift

/-- Fiber of the localization-level view at one localization object. -/
abbrev CounterFactorizationLocalizedFiber
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (X : allMorphisms.Localization) :=
  (counterFactorizationLocalizationView H).obj (.mk X)

/-- A raw vertex seen through the localization-level view has the same source
fiber as the already-used restricted factorization. -/
@[simp] theorem counterFactorizationLocalizationView_obj_Q
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (X : OctahedralVertex) :
    CounterFactorizationLocalizedFiber H (allMorphisms.Q.obj X) =
      CounterFactorizationFiber H X := by
  rfl

/-- Propagate an object along an arbitrary localization arrow. -/
noncomputable def counterFactorizationLocalizedPropagatedObject
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y : allMorphisms.Localization} (f : X ⟶ Y)
    (A : CounterFactorizationLocalizedFiber H X) :
    CounterFactorizationLocalizedFiber H Y :=
  ((counterFactorizationLocalizationView H).map f.toLoc).toFunctor.obj A

/-- Image in the raw C2 target of one localization-level compositor component,
provided the endpoint is the localization image of a raw octahedral vertex. -/
noncomputable def counterFactorizationLocalizedCompImageScalarAt
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X Y : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ allMorphisms.Q.obj T)
    (A : CounterFactorizationLocalizedFiber H X) : C2 :=
  (H.comparison.app (.mk T)).toFunctor.map
    (((counterFactorizationLocalizationView H).mapComp
      f.toLoc g.toLoc).hom.toNatTrans.app A)

/-- Additive form of the localization-level compositor scalar. -/
noncomputable def counterFactorizationLocalizedCompAddAt
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X Y : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ allMorphisms.Q.obj T)
    (A : CounterFactorizationLocalizedFiber H X) : ZMod 2 :=
  Multiplicative.toAdd
    (counterFactorizationLocalizedCompImageScalarAt H T f g A)

/-- The first compositor in an associator equation lives at the intermediate
endpoint.  After whiskering by the third localization arrow, map it forward and
only then apply the endpoint comparison functor. -/
noncomputable def counterFactorizationLocalizedTransportedCompImageScalarAt
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X Y Z : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (h : Z ⟶ allMorphisms.Q.obj T)
    (A : CounterFactorizationLocalizedFiber H X) : C2 :=
  (H.comparison.app (.mk T)).toFunctor.map
    (((counterFactorizationLocalizationView H).map h.toLoc).toFunctor.map
      (((counterFactorizationLocalizationView H).mapComp
        f.toLoc g.toLoc).hom.toNatTrans.app A))

/-- Additive form of the transported intermediate compositor. -/
noncomputable def counterFactorizationLocalizedTransportedCompAddAt
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X Y Z : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (h : Z ⟶ allMorphisms.Q.obj T)
    (A : CounterFactorizationLocalizedFiber H X) : ZMod 2 :=
  Multiplicative.toAdd
    (counterFactorizationLocalizedTransportedCompImageScalarAt
      H T f g h A)

/-- After endpoint comparison, the inverse compositor component carries the
inverse C2 scalar.  The proof stays entirely in the exact endpoint fiber before
group cancellation is invoked. -/
@[simp] theorem counterFactorizationLocalizedComp_inv_image_eq_inv
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X Y : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ allMorphisms.Q.obj T)
    (A : CounterFactorizationLocalizedFiber H X) :
    (H.comparison.app (.mk T)).toFunctor.map
        (((counterFactorizationLocalizationView H).mapComp
          f.toLoc g.toLoc).inv.toNatTrans.app A) =
      (counterFactorizationLocalizedCompImageScalarAt H T f g A)⁻¹ := by
  let invScalar : C2 :=
    (H.comparison.app (.mk T)).toFunctor.map
      (((counterFactorizationLocalizationView H).mapComp
        f.toLoc g.toLoc).inv.toNatTrans.app A)
  change invScalar =
    (counterFactorizationLocalizedCompImageScalarAt H T f g A)⁻¹
  let P := (H.comparison.app (.mk T)).toFunctor
  let e :=
    (counterFactorizationLocalizationView H).mapComp
      f.toLoc g.toLoc
  have hCat :=
    Cat.Hom.inv_hom_id_toNatTrans_app e A
  have hMapCatRaw :=
    congrArg (fun k => P.map k) hCat
  have hMapCat :
      P.map (e.inv.toNatTrans.app A) ≫
          P.map (e.hom.toNatTrans.app A) =
        𝟙 _ := by
    calc
      P.map (e.inv.toNatTrans.app A) ≫
          P.map (e.hom.toNatTrans.app A) =
        P.map
          (e.inv.toNatTrans.app A ≫
            e.hom.toNatTrans.app A) :=
          (P.map_comp _ _).symm
      _ = P.map (𝟙 _) := hMapCatRaw
      _ = 𝟙 _ := P.map_id _
  have hScalar :=
    congrArg (fun k => counterSystemHomScalar T k) hMapCat
  have hMul :
      counterFactorizationLocalizedCompImageScalarAt H T f g A *
          invScalar = (1 : C2) := by
    simpa only [P, e,
      counterFactorizationLocalizedCompImageScalarAt,
      invScalar,
      counterSystemHomScalar_comp,
      counterSystemHomScalar,
      SingleObj.id_as_one] using hScalar
  exact eq_inv_of_mul_eq_one_right hMul

/-- Localization-level associator coherence after exact Cat-component
scalarization.

The crucial second term is the compositor on `f,g` after transport by `h`.
It is not replaced by a fixed-object scalar. -/
theorem counterFactorizationLocalizedCompAdd_cocycle
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X Y Z : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (h : Z ⟶ allMorphisms.Q.obj T)
    (A : CounterFactorizationLocalizedFiber H X) :
    counterFactorizationLocalizedCompAddAt H T (f ≫ g) h A +
        counterFactorizationLocalizedTransportedCompAddAt
          H T f g h A =
      counterFactorizationLocalizedCompAddAt H T g h
          (counterFactorizationLocalizedPropagatedObject H f A) +
        counterFactorizationLocalizedCompAddAt H T f (g ≫ h) A := by
  let F := counterFactorizationLocalizationView H
  have hAssoc := F.map₂_associator f.toLoc g.toLoc h.toLoc
  simp only [← Quiver.Hom.comp_toLoc] at hAssoc
  have hNat := congrArg (fun η => η.toNatTrans) hAssoc
  have hApp := NatTrans.congr_app hNat A
  have hMapped :=
    congrArg
      (fun k => (H.comparison.app (.mk T)).toFunctor.map k)
      hApp
  have hScalar :=
    congrArg (fun k => counterSystemHomScalar T k) hMapped
  set_option backward.isDefEq.respectTransparency false in
    simp only [F,
      Functor.map_comp, Functor.map_id,
      counterSystemHomScalar_comp,
      counterSystemHomScalar,
      CategoryTheory.Bicategory.Strict.associator_eqToIso,
      eqToIso.hom,
      CategoryTheory.PrelaxFunctor.map₂_eqToHom,
      CategoryTheory.Cat.eqToHom_app,
      CategoryTheory.eqToHom_map,
      Cat.Hom₂.comp_app,
      Cat.whiskerLeft_app,
      Cat.whiskerRight_app,
      Cat.associator_hom_app,
      counterSystem_eqToHom_eq_one,
      counterFactorizationLocalizedCompImageScalarAt,
      counterFactorizationLocalizedTransportedCompImageScalarAt,
      counterFactorizationLocalizedPropagatedObject,
      counterFactorizationLocalizedComp_inv_image_eq_inv,
      SingleObj.id_as_one,
      mul_one, one_mul, mul_assoc] at hScalar
  have hMul :
      (counterFactorizationLocalizedCompImageScalarAt H T f (g ≫ h) A)⁻¹ *
          (counterFactorizationLocalizedCompImageScalarAt H T g h
            (counterFactorizationLocalizedPropagatedObject H f A))⁻¹ *
          counterFactorizationLocalizedTransportedCompImageScalarAt
            H T f g h A *
          counterFactorizationLocalizedCompImageScalarAt
            H T (f ≫ g) h A =
        (1 : C2) := by
    exact hScalar.symm
  have hAdd := congrArg (@Multiplicative.toAdd (ZMod 2)) hMul
  simp only [toAdd_mul, toAdd_inv, toAdd_one, CharTwo.neg_eq] at hAdd
  have hPair :
      (counterFactorizationLocalizedCompAddAt H T (f ≫ g) h A +
        counterFactorizationLocalizedTransportedCompAddAt
          H T f g h A) +
        (counterFactorizationLocalizedCompAddAt H T g h
          (counterFactorizationLocalizedPropagatedObject H f A) +
        counterFactorizationLocalizedCompAddAt H T f (g ≫ h) A) = 0 := by
    unfold counterFactorizationLocalizedCompAddAt
    unfold counterFactorizationLocalizedTransportedCompAddAt
    linear_combination hAdd
  exact CharTwo.add_eq_zero.mp hPair

/-!
## Boundary after v3.75

The arbitrary localized lift now has a genuine localization-level C2
associator balance, without choosing a canonical quotient transport and without
discarding source-object transport.

The next theorem unit can specialize this equation to the four triples

```text
Q(a00), counterMiddleSwitch, Q(b10)
Q(a00), counterMiddleSwitch, Q(b11)
Q(a10), counterMiddleSwitch, Q(b10)
Q(a10), counterMiddleSwitch, Q(b11)
```

and use the exact localization equalities from v3.69.  What remains to be
checked is how the two transported intermediate-compositor terms correspond to
the four v3.74 connector coboundaries.

That is the decisive cancellation-versus-absorption boundary.
-/

end

end KUOS.DependentOriginationArbitraryFactorizationLocalizedCocycleV3_75
