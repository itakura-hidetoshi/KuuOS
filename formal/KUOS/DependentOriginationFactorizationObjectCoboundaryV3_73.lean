import KUOS.DependentOriginationArbitraryFactorizationScalarV3_72

namespace KUOS.DependentOriginationFactorizationObjectCoboundaryV3_73

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationCounterComparisonObstructionV3_68
open KUOS.DependentOriginationArbitraryFactorizationScalarV3_72

open scoped CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Arbitrary-factorization object coboundary v3.73

v3.72 scalarizes the StrongTrans composition law for an arbitrary
higher-localization factorization of the concrete octahedral C2 countermodel.
Unlike the canonical quotient transports of v3.68--v3.69, the edge scalar is
evaluated at an object of an arbitrary source fiber.

This file identifies the exact law governing that object dependence.

For a source-fiber morphism `u : A ⟶ B`, compare two C2 scalars:

* the image of `u` through the comparison component at the source vertex;
* the image of `F.map f u` through the comparison component at the target
  vertex.

Naturality of the StrongTrans edge isomorphism gives

```text
edge(f,B) * transported(u)
  = source(u) * edge(f,A).
```

Hence the object dependence is not an unconstrained new term.  It is a
multiplicative coboundary

```text
edge(f,B)
  = (source(u) * transported(u)^(-1)) * edge(f,A).
```

For loops `u : A ⟶ A`, that coboundary is trivial: source and transported
loop scalars agree.  Thus the remaining freedom lives only in transport between
distinct source-fiber objects.

No claim of global object-independence is made here.
-/

/-- Scalar assigned by the comparison component at one source vertex to a
source-fiber morphism. -/
noncomputable def counterFactorizationSourceScalarAt
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (X : OctahedralVertex)
    {A B :
      (restrictHigherLocalizedSystem
        allMorphisms H.lift).obj (.mk X)}
    (u : A ⟶ B) : C2 :=
  (H.comparison.app (.mk X)).toFunctor.map u

/-- Scalar assigned at the target vertex after first transporting a source
morphism through the arbitrary localized edge map. -/
noncomputable def counterFactorizationMappedSourceScalarAt
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    {A B :
      (restrictHigherLocalizedSystem
        allMorphisms H.lift).obj (.mk X)}
    (u : A ⟶ B) : C2 :=
  (H.comparison.app (.mk Y)).toFunctor.map
    (((restrictHigherLocalizedSystem
        allMorphisms H.lift).map f.toLoc).toFunctor.map u)

/-- Naturality of one arbitrary-factorization edge scalar along a source-fiber
morphism.

The multiplication order is the exact `SingleObj` scalarization of categorical
composition: `p ≫ q` becomes `q * p`. -/
theorem counterFactorizationEdgeScalarAt_naturality
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    {A B :
      (restrictHigherLocalizedSystem
        allMorphisms H.lift).obj (.mk X)}
    (u : A ⟶ B) :
    counterFactorizationEdgeScalarAt H f B *
        counterFactorizationMappedSourceScalarAt H f u =
      counterFactorizationSourceScalarAt H X u *
        counterFactorizationEdgeScalarAt H f A := by
  have h :=
    (H.comparison.naturality f.toLoc).hom.toNatTrans.naturality u
  have hScalar :=
    congrArg (fun k => counterSystemHomScalar Y k) h
  set_option backward.isDefEq.respectTransparency false in
    simp only [counterSystemHomScalar_comp,
      Cat.Hom.comp_toFunctor, Functor.comp_map,
      counterSystem_map_morphism_eq] at hScalar
  simpa only [counterSystemHomScalar,
    counterFactorizationEdgeScalarAt,
    counterFactorizationSourceScalarAt,
    counterFactorizationMappedSourceScalarAt] using hScalar

/-- The multiplicative object-transport coboundary carried by one source-fiber
morphism along one base edge. -/
noncomputable def counterFactorizationObjectCoboundaryAt
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    {A B :
      (restrictHigherLocalizedSystem
        allMorphisms H.lift).obj (.mk X)}
    (u : A ⟶ B) : C2 :=
  counterFactorizationSourceScalarAt H X u *
    (counterFactorizationMappedSourceScalarAt H f u)⁻¹

/-- Exact coboundary form of the object-dependence of an edge scalar. -/
theorem counterFactorizationEdgeScalarAt_change_object
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    {A B :
      (restrictHigherLocalizedSystem
        allMorphisms H.lift).obj (.mk X)}
    (u : A ⟶ B) :
    counterFactorizationEdgeScalarAt H f B =
      counterFactorizationObjectCoboundaryAt H f u *
        counterFactorizationEdgeScalarAt H f A := by
  have h := counterFactorizationEdgeScalarAt_naturality H f u
  calc
    counterFactorizationEdgeScalarAt H f B =
        (counterFactorizationEdgeScalarAt H f B *
            counterFactorizationMappedSourceScalarAt H f u) *
          (counterFactorizationMappedSourceScalarAt H f u)⁻¹ := by
            simp [mul_assoc]
    _ =
        (counterFactorizationSourceScalarAt H X u *
            counterFactorizationEdgeScalarAt H f A) *
          (counterFactorizationMappedSourceScalarAt H f u)⁻¹ := by
            rw [h]
    _ =
        counterFactorizationObjectCoboundaryAt H f u *
          counterFactorizationEdgeScalarAt H f A := by
            unfold counterFactorizationObjectCoboundaryAt
            ac_rfl

/-- On a source-fiber loop, the comparison component sees the same C2 scalar
before and after transport through the localized edge map. -/
theorem counterFactorizationMappedSourceScalarAt_loop_eq_source
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    {A :
      (restrictHigherLocalizedSystem
        allMorphisms H.lift).obj (.mk X)}
    (u : A ⟶ A) :
    counterFactorizationMappedSourceScalarAt H f u =
      counterFactorizationSourceScalarAt H X u := by
  have h := counterFactorizationEdgeScalarAt_naturality H f u
  let e : C2 := counterFactorizationEdgeScalarAt H f A
  let m : C2 := counterFactorizationMappedSourceScalarAt H f u
  let s : C2 := counterFactorizationSourceScalarAt H X u
  have hem : e * m = s * e := by
    simpa [e, m, s] using h
  calc
    m = e⁻¹ * (e * m) := by
          simp [← mul_assoc]
    _ = e⁻¹ * (s * e) := by
          rw [hem]
    _ = s := by
          rw [mul_comm s e, ← mul_assoc, inv_mul, one_mul]

/-- Consequently the object coboundary vanishes on loops. -/
@[simp] theorem counterFactorizationObjectCoboundaryAt_loop
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    {A :
      (restrictHigherLocalizedSystem
        allMorphisms H.lift).obj (.mk X)}
    (u : A ⟶ A) :
    counterFactorizationObjectCoboundaryAt H f u = 1 := by
  unfold counterFactorizationObjectCoboundaryAt
  rw [counterFactorizationMappedSourceScalarAt_loop_eq_source H f u]
  exact mul_inv_cancel _

/-!
## Boundary after v3.73

For arbitrary factorization data, object dependence now has the exact form

```text
edge(f,B) = delta_f(u) * edge(f,A),

delta_f(u)
  = comparison_X(u)
      * comparison_Y(F(f)u)^(-1).
```

Moreover

```text
u : A ⟶ A  =>  delta_f(u) = 1.
```

So the new freedom exposed by v3.72 is not arbitrary on automorphism loops.
The remaining question is whether the inter-object coboundaries cancel around
the octahedral eight-face sum, or whether they can absorb the raw C2 parity
class.

The next theorem unit should combine this object coboundary with the arbitrary
localized compositor term from v3.72.
-/

end

end KUOS.DependentOriginationFactorizationObjectCoboundaryV3_73
