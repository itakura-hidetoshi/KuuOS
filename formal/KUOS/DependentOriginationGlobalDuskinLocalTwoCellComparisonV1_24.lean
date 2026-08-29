import KUOS.DependentOriginationGlobalDuskinLocalMappingComparisonV1_23

namespace KUOS.DependentOriginationGlobalDuskinLocalTwoCellComparisonV1_24

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open Simplicial
open Opposite
open scoped Bicategory
open KUOS.DependentOriginationInfinityTwoYonedaV1_18
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationGlobalDuskinLocalMappingComparisonV1_23

universe u v w

/-!
# Global Duskin / local two-cell comparison v1.24

The v1.23 comparison identifies the global one-skeleton with the local mapping
nerve at degree zero, conditionally on exact edge representability.  The next
dimensional layer is automatic and does not require a reverse representability
assumption:

* a bicategorical 2-morphism `α : f ⟶ g` determines an edge of
  `mappingNerve X Y` between the vertices represented by `f` and `g`;
* for every global Duskin 2-simplex, its normal-lax comparison 2-cell

```text
σ(0→1) ≫ σ(1→2) ⟶ σ(0→2)
```

therefore determines a canonical local mapping-nerve edge;
* Mathlib's native `nerve.homEquiv` recovers exactly the original Duskin
  comparison 2-cell;
* away from simplicial degeneracies, global Duskin thinness is equivalent to
  invertibility of this recovered local mapping 2-morphism.

This is a forward two-skeleton comparison.  It still does not claim that every
local mapping edge is represented by a globally fixed-endpoint Duskin triangle,
or that the full global mapping simplicial object has already been constructed.
-/

/-! ## Local mapping edges and bicategorical 2-morphisms -/

/--
The edge space in the local mapping nerve between the vertices represented by
parallel bicategorical 1-morphisms `f,g : X ⟶ Y`.
-/
abbrev MappingNerveEdge
    {B : Type u} [Bicategory.{w, v} B]
    (X Y : B) (f g : X ⟶ Y) :=
  (mappingNerve X Y).Edge
    (CategoryTheory.nerveEquiv.symm f)
    (CategoryTheory.nerveEquiv.symm g)

/-- A bicategorical 2-morphism gives the corresponding edge in the local mapping nerve. -/
def localMappingEdgeOfTwoMorphism
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B} {f g : X ⟶ Y}
    (α : f ⟶ g) :
    MappingNerveEdge X Y f g :=
  CategoryTheory.nerve.edgeMk α

/-- Mathlib's native nerve equivalence recovers the 2-morphism used to build a local edge. -/
@[simp] theorem localMappingEdgeOfTwoMorphism_hom
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B} {f g : X ⟶ Y}
    (α : f ⟶ g) :
    CategoryTheory.nerve.homEquiv
      (localMappingEdgeOfTwoMorphism α) = α := by
  simpa [localMappingEdgeOfTwoMorphism, MappingNerveEdge] using
    (CategoryTheory.nerve.homEquiv_edgeMk α)

/-- Every fixed-endpoint edge of a local mapping nerve comes from a bicategorical 2-morphism. -/
theorem localMappingEdgeOfTwoMorphism_surjective
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B} {f g : X ⟶ Y} :
    Function.Surjective
      (localMappingEdgeOfTwoMorphism : (f ⟶ g) → MappingNerveEdge X Y f g) := by
  intro e
  obtain ⟨α, hα⟩ :=
    (CategoryTheory.nerve.edgeMk_surjective
      (C := (X ⟶ Y)) (x := f) (y := g)) e
  refine ⟨α, ?_⟩
  change CategoryTheory.nerve.edgeMk α = e
  exact hα

/-! ## The comparison edge of a global Duskin 2-simplex -/

/-- Initial vertex of a global Duskin 2-simplex. -/
def duskinTriangleSource
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2) : B :=
  σ.obj (LocallyDiscrete.mk (0 : Fin 3))

/-- Middle vertex of a global Duskin 2-simplex. -/
def duskinTriangleMiddle
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2) : B :=
  σ.obj (LocallyDiscrete.mk (1 : Fin 3))

/-- Terminal vertex of a global Duskin 2-simplex. -/
def duskinTriangleTarget
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2) : B :=
  σ.obj (LocallyDiscrete.mk (2 : Fin 3))

/-- The compositional source of the Duskin comparison 2-cell. -/
def duskinTriangleCompositeArrow
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2) :
    duskinTriangleSource σ ⟶ duskinTriangleTarget σ :=
  σ.map edge01 ≫ σ.map edge12

/-- The long edge which is the target of the Duskin comparison 2-cell. -/
def duskinTriangleLongArrow
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2) :
    duskinTriangleSource σ ⟶ duskinTriangleTarget σ :=
  σ.map (edge01 ≫ edge12)

/-- The local mapping-nerve edge corresponding to the global Duskin comparison 2-cell. -/
def duskinComparisonMappingEdge
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2) :
    MappingNerveEdge
      (duskinTriangleSource σ)
      (duskinTriangleTarget σ)
      (duskinTriangleCompositeArrow σ)
      (duskinTriangleLongArrow σ) :=
  localMappingEdgeOfTwoMorphism (duskinComparison σ)

/-- The local mapping edge remembers exactly the original normal-lax comparison cell. -/
@[simp] theorem duskinComparisonMappingEdge_hom
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2) :
    CategoryTheory.nerve.homEquiv
      (duskinComparisonMappingEdge σ) = duskinComparison σ := by
  simpa [duskinComparisonMappingEdge] using
    (localMappingEdgeOfTwoMorphism_hom (α := duskinComparison σ))

/-- Invertibility of the global comparison cell is exactly invertibility of its local image. -/
theorem duskinComparison_isIso_iff_localMappingEdge_isIso
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2) :
    IsIso (duskinComparison σ) ↔
      IsIso (CategoryTheory.nerve.homEquiv (duskinComparisonMappingEdge σ)) := by
  rw [duskinComparisonMappingEdge_hom]
  exact Iff.rfl

/-- If the local mapping 2-morphism is invertible, the global Duskin triangle is thin. -/
theorem localMappingComparisonIso_isThin
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2)
    (hiso : IsIso
      (CategoryTheory.nerve.homEquiv (duskinComparisonMappingEdge σ))) :
    (duskinScaling B).thin σ := by
  change IsIso (duskinComparison σ) ∨ IsDegenerateDuskinTwoSimplex σ
  exact Or.inl ((duskinComparison_isIso_iff_localMappingEdge_isIso σ).mpr hiso)

/--
For a nondegenerate global triangle, thinness is detected exactly by
invertibility of the corresponding local mapping 2-morphism.
-/
theorem nondegenerate_duskinThin_iff_localMappingComparisonIso
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2)
    (hnd : ¬ IsDegenerateDuskinTwoSimplex σ) :
    (duskinScaling B).thin σ ↔
      IsIso (CategoryTheory.nerve.homEquiv (duskinComparisonMappingEdge σ)) := by
  change
    (IsIso (duskinComparison σ) ∨ IsDegenerateDuskinTwoSimplex σ) ↔
      IsIso (CategoryTheory.nerve.homEquiv (duskinComparisonMappingEdge σ))
  constructor
  · intro h
    rcases h with h | h
    · exact (duskinComparison_isIso_iff_localMappingEdge_isIso σ).mp h
    · exact False.elim (hnd h)
  · intro h
    exact Or.inl ((duskinComparison_isIso_iff_localMappingEdge_isIso σ).mpr h)

/-! ## Automatic forward two-skeleton certificate -/

/--
The theorem-level forward comparison forced by every bicategory: every global
Duskin comparison cell appears as a local mapping-nerve edge, and nondegenerate
thinness is exactly local invertibility.
-/
structure GlobalDuskinLocalTwoCellForwardComparison
    (B : Type u) [Bicategory.{w, v} B] : Prop where
  comparison_recovered :
    ∀ σ : DuskinSimplex B 2,
      CategoryTheory.nerve.homEquiv
        (duskinComparisonMappingEdge σ) = duskinComparison σ
  nondegenerate_thin_detected_locally :
    ∀ σ : DuskinSimplex B 2,
      ¬ IsDegenerateDuskinTwoSimplex σ →
      ((duskinScaling B).thin σ ↔
        IsIso (CategoryTheory.nerve.homEquiv (duskinComparisonMappingEdge σ)))

/-- Every bicategory canonically supplies the forward two-cell comparison. -/
def globalDuskinLocalTwoCellForwardComparison
    (B : Type u) [Bicategory.{w, v} B] :
    GlobalDuskinLocalTwoCellForwardComparison B where
  comparison_recovered := duskinComparisonMappingEdge_hom
  nondegenerate_thin_detected_locally :=
    nondegenerate_duskinThin_iff_localMappingComparisonIso

/-!
The precise v1.24 frontier is therefore:

```text
α : f ⟶ g
  -> edge in mappingNerve(X,Y)                         -- canonical
  -> native nerve.homEquiv recovers α                  -- proved

global Duskin 2-simplex σ
  -> comparison 2-cell σ₀₁ ≫ σ₁₂ ⟶ σ₀₂
  -> canonical local mapping-nerve edge                -- proved
  -> local edge recovers exactly the comparison cell   -- proved

nondegenerate σ:
  global thinness ↔ invertibility of local 2-morphism  -- proved
```

Still open and intentionally not inferred from this forward comparison:

* reverse representability of arbitrary local mapping edges by globally
  fixed-endpoint Duskin triangles;
* construction of the full global mapping simplicial object in all degrees;
* compatibility of a full comparison with composition and the v1.22 scaled
  horn family;
* a conditional equivalence between the complete-Segal and global scaled
  Duskin presentations.
-/

end KUOS.DependentOriginationGlobalDuskinLocalTwoCellComparisonV1_24
