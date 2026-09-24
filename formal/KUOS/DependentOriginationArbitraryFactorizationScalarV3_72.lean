import KUOS.DependentOriginationFactorizationNecessityBoundaryV3_71

namespace KUOS.DependentOriginationArbitraryFactorizationScalarV3_72

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationCounterComparisonObstructionV3_68
open KUOS.DependentOriginationFactorizationNecessityBoundaryV3_71

open scoped CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Arbitrary-factorization component scalar v3.72

v3.71 shows that canonical normalization is not a weaker bridge: for the
countermodel it is already equivalent to abstract nonfactorization.

This file therefore works directly with an arbitrary

```text
H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem.
```

The target raw fibers are still `CounterFiber = SingleObj C2`, so every
component of the StrongTrans naturality isomorphism has a literal C2 scalar.
The localized lift, however, may have arbitrary source fibers.  Consequently
the composition law is object-dependent.

For an object `A` of the source fiber at `X`, define

* the edge scalar from `H.comparison.naturality f` at `A`;
* the image in C2 of the source compositor at `A`.

Mathlib's native
`Pseudofunctor.StrongTrans.naturality_comp_hom_app` then gives the exact
composition equation.  The crucial difference from v3.69 is that the scalar
for the second edge `g` is evaluated at the propagated object
`F.map f A`, not at a fixed chosen object of the middle fiber.

This is the precise obstruction to repeating the v3.69 eight-face cancellation
without an additional object-transport/presentation-invariance theorem.
-/

/-- Scalar of one arbitrary factorization-comparison naturality component,
evaluated at a chosen object of the source fiber. -/
noncomputable def counterFactorizationEdgeScalarAt
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    (A :
      (restrictHigherLocalizedSystem
        allMorphisms H.lift).obj (.mk X)) : C2 :=
  (H.comparison.naturality f.toLoc).hom.toNatTrans.app A

/-- The source localized compositor, after applying the target comparison
component at the endpoint, becomes a C2 scalar. -/
noncomputable def counterFactorizationLiftCompImageScalarAt
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y Z : OctahedralVertex} (f : X ⟶ Y) (g : Y ⟶ Z)
    (A :
      (restrictHigherLocalizedSystem
        allMorphisms H.lift).obj (.mk X)) : C2 :=
  (H.comparison.app (.mk Z)).toFunctor.map
    (((restrictHigherLocalizedSystem
        allMorphisms H.lift).mapComp
          f.toLoc g.toLoc).hom.toNatTrans.app A)

/-- The inverse raw compositor contributes the inverse finite C2 face scalar. -/
@[simp] theorem counterSystem_mapComp_inv_app
    {X Y Z : OctahedralVertex} (f : X ⟶ Y) (g : Y ⟶ Z)
    (A : CounterFiber) :
    (counterSystem.mapComp f.toLoc g.toLoc).inv.toNatTrans.app A =
      (compScalar X Y Z)⁻¹ := by
  cases A
  apply eq_inv_of_mul_eq_one_right
  simpa only [counterSystem_mapComp_hom_app,
    SingleObj.comp_as_mul, SingleObj.id_as_one] using
    (Cat.Hom.inv_hom_id_toNatTrans_app
      (counterSystem.mapComp f.toLoc g.toLoc)
      (SingleObj.star C2))

/-- Exact object-dependent StrongTrans composition equation for an arbitrary
higher-localization factorization of the concrete C2 countermodel.

The second edge is evaluated at the propagated middle-fiber object.  This is
the information that disappears in the identity-fiber quotient transports of
v3.68-v3.69, and it is exactly what must be controlled before a global parity
cancellation can be asserted for arbitrary abstract factorizations. -/
theorem counterFactorizationEdgeScalarAt_comp
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y Z : OctahedralVertex} (f : X ⟶ Y) (g : Y ⟶ Z)
    (A :
      (restrictHigherLocalizedSystem
        allMorphisms H.lift).obj (.mk X)) :
    counterFactorizationEdgeScalarAt H (f ≫ g) A =
      (compScalar X Y Z)⁻¹ *
        counterFactorizationEdgeScalarAt H f A *
        counterFactorizationEdgeScalarAt H g
          (((restrictHigherLocalizedSystem
              allMorphisms H.lift).map f.toLoc).toFunctor.obj A) *
        counterFactorizationLiftCompImageScalarAt H f g A := by
  have h :=
    Pseudofunctor.StrongTrans.naturality_comp_hom_app
      H.comparison f.toLoc g.toLoc A
  rw [← Quiver.Hom.comp_toLoc] at h
  set_option backward.isDefEq.respectTransparency false in
    simpa only [counterFactorizationEdgeScalarAt,
      counterFactorizationLiftCompImageScalarAt,
      counterSystem_map_morphism_eq,
      counterSystem_eqToHom_eq_one,
      counterSystem_mapComp_inv_app,
      SingleObj.comp_as_mul,
      one_mul, mul_one, mul_assoc] using h

/-!
## Boundary after v3.72

For arbitrary `H`, Stage-II composition is now scalarized without canonical
quotient transport:

```text
edge(fg, A)
  = rawFace(f,g)^(-1)
      * edge(f, A)
      * edge(g, F(f)A)
      * image(sourceCompositor(f,g,A)).
```

The v3.69 cancellation used one scalar per base edge because every relevant
source fiber was literally `SingleObj C2` and every representative map was the
identity functor.

For arbitrary `H`, two new freedoms are explicit:

1. edge scalars depend on the source-fiber object;
2. the arbitrary localized lift contributes its own compositor scalar after
   transport through the comparison equivalence.

Therefore the next truth test must control both terms.  A legitimate next
target is either:

* prove object-independence plus even total compositor parity from the fact that
  `H.lift` is defined on the localization; or
* construct an explicit localized lift whose object-dependent/compositor terms
  absorb the raw octahedral C2 class.

No global nonfactorization conclusion is made here.
-/

end

end KUOS.DependentOriginationArbitraryFactorizationScalarV3_72
