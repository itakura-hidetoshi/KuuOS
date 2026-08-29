import KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22

namespace KUOS.DependentOriginationGlobalDuskinLocalMappingComparisonV1_23

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open Simplicial
open Opposite
open scoped Bicategory
open KUOS.DependentOriginationInfinityTwoYonedaV1_18
open KUOS.DependentOriginationCompleteSegalInfinityTwoV1_20
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22

universe u v w

/-!
# Global Duskin / local mapping comparison v1.23

The v1.22 frontier separates automatic low-dimensional Duskin coherence from
extra scaled-horn fibrancy data.  The next comparison problem is local/global:
for fixed objects `X,Y`, the local 2-Yoneda presentation uses the nerve
`N(B(X,Y))`, whereas the global presentation stores 1-morphisms as 1-simplices
of the single Duskin nerve.

This file closes the first exact layer of that comparison without claiming a
full mapping-object equivalence.

* the 0-simplices of `mappingNerve X Y` are identified with 1-morphisms
  `X ⟶ Y` using Mathlib's native `CategoryTheory.nerveEquiv`;
* every global Duskin 1-simplex with endpoints identified with `X,Y` extracts a
  canonical 1-morphism `X ⟶ Y` and therefore a canonical local mapping vertex;
* exact representability of all such global edges by local vertices is isolated
  as explicit additional data;
* bicategorical adjoint-equivalence edges are connected to the v1.20
  `ObjectUnivalence` path space.

The full statement

```text
global Duskin mapping object(X,Y) ≃ N(B(X,Y))
```

is deliberately not asserted here: constructing the left-hand simplicial
mapping object and proving compatibility in every simplicial degree remain a
separate theorem.
-/

/-! ## Local mapping vertices -/

/-- The 0-simplices of the local mapping nerve `N(B(X,Y))`. -/
abbrev MappingNerveVertex
    {B : Type u} [Bicategory.{w, v} B]
    (X Y : B) :=
  (mappingNerve X Y).obj (op ⦋0⦌)

/--
Mathlib's native nerve equivalence identifies local mapping vertices exactly
with bicategorical 1-morphisms.
-/
def mappingNerveVertexEquiv
    {B : Type u} [Bicategory.{w, v} B]
    (X Y : B) :
    MappingNerveVertex X Y ≃ (X ⟶ Y) :=
  CategoryTheory.nerveEquiv

/-! ## Fixed-endpoint global Duskin edges -/

/-- The source object of a global Duskin 1-simplex. -/
def duskinEdgeSource
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 1) : B :=
  σ.obj (LocallyDiscrete.mk (0 : Fin 2))

/-- The target object of a global Duskin 1-simplex. -/
def duskinEdgeTarget
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 1) : B :=
  σ.obj (LocallyDiscrete.mk (1 : Fin 2))

/-- The principal 1-morphism carried by a global Duskin 1-simplex. -/
def duskinEdgeArrow
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 1) :
    duskinEdgeSource σ ⟶ duskinEdgeTarget σ :=
  σ.map edge01One

/--
A global Duskin edge whose two endpoint objects have been identified with
specified objects `X,Y`.
-/
structure GlobalDuskinEdgeOver
    (B : Type u) [Bicategory.{w, v} B]
    (X Y : B) where
  simplex : DuskinSimplex B 1
  source_eq : duskinEdgeSource simplex = X
  target_eq : duskinEdgeTarget simplex = Y

namespace GlobalDuskinEdgeOver

/-- Extract the underlying bicategorical 1-morphism from a fixed-endpoint global edge. -/
def toArrow
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (e : GlobalDuskinEdgeOver B X Y) : X ⟶ Y := by
  rcases e with ⟨σ, rfl, rfl⟩
  exact duskinEdgeArrow σ

/-- Send a fixed-endpoint global Duskin edge to the corresponding local mapping vertex. -/
def toMappingVertex
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (e : GlobalDuskinEdgeOver B X Y) :
    MappingNerveVertex X Y :=
  (mappingNerveVertexEquiv X Y).symm e.toArrow

/-- The local nerve equivalence recovers exactly the arrow extracted from the global edge. -/
@[simp] theorem mappingNerveVertexEquiv_toMappingVertex
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (e : GlobalDuskinEdgeOver B X Y) :
    mappingNerveVertexEquiv X Y e.toMappingVertex = e.toArrow := by
  exact Equiv.apply_symm_apply _ _

end GlobalDuskinEdgeOver

/-! ## Exact one-skeleton representability boundary -/

/--
Exact representability of the fixed-endpoint global edge type by local mapping
vertices.

This is additional comparison data.  It is intentionally not inferred merely
from the existence of a bicategory: proving it by constructing and classifying
normal-lax walking-arrow functors is a separate theorem.
-/
structure GlobalDuskinEdgeRepresentability
    (B : Type u) [Bicategory.{w, v} B]
    (X Y : B) where
  inverse : MappingNerveVertex X Y → GlobalDuskinEdgeOver B X Y
  left_inv :
    ∀ e : GlobalDuskinEdgeOver B X Y,
      inverse e.toMappingVertex = e
  right_inv :
    ∀ x : MappingNerveVertex X Y,
      (inverse x).toMappingVertex = x

/-- Representability packages an actual equivalence at the fixed-endpoint one-skeleton. -/
def globalDuskinEdgeEquivMappingVertex
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (R : GlobalDuskinEdgeRepresentability B X Y) :
    GlobalDuskinEdgeOver B X Y ≃ MappingNerveVertex X Y where
  toFun := GlobalDuskinEdgeOver.toMappingVertex
  invFun := R.inverse
  left_inv := R.left_inv
  right_inv := R.right_inv

/-- A simultaneous one-skeleton comparison for every ordered pair of objects. -/
structure GlobalDuskinLocalOneSkeletonComparison
    (B : Type u) [Bicategory.{w, v} B] where
  edge_representability :
    ∀ X Y : B, GlobalDuskinEdgeRepresentability B X Y

/-- Re-export the fixed-endpoint equivalence from a global one-skeleton comparison. -/
def GlobalDuskinLocalOneSkeletonComparison.edgeEquiv
    {B : Type u} [Bicategory.{w, v} B]
    (C : GlobalDuskinLocalOneSkeletonComparison B)
    (X Y : B) :
    GlobalDuskinEdgeOver B X Y ≃ MappingNerveVertex X Y :=
  globalDuskinEdgeEquivMappingVertex (C.edge_representability X Y)

/-! ## Adjoint-equivalence edges and object univalence -/

/--
A fixed-endpoint global Duskin edge is an equivalence edge when its extracted
1-morphism is the forward morphism of a native bicategorical adjoint
equivalence.
-/
def IsGlobalDuskinEquivalenceEdge
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (e : GlobalDuskinEdgeOver B X Y) : Prop :=
  ∃ q : X ≌ Y, q.hom = e.toArrow

/-- Under edge representability, every adjoint equivalence has a representing global edge. -/
def globalEdgeOfEquivalence
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (R : GlobalDuskinEdgeRepresentability B X Y)
    (q : X ≌ Y) :
    GlobalDuskinEdgeOver B X Y :=
  R.inverse ((mappingNerveVertexEquiv X Y).symm q.hom)

/-- The edge representing an adjoint equivalence extracts exactly its forward 1-morphism. -/
theorem globalEdgeOfEquivalence_toArrow
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (R : GlobalDuskinEdgeRepresentability B X Y)
    (q : X ≌ Y) :
    (globalEdgeOfEquivalence R q).toArrow = q.hom := by
  calc
    (globalEdgeOfEquivalence R q).toArrow =
        mappingNerveVertexEquiv X Y
          (globalEdgeOfEquivalence R q).toMappingVertex := by
      symm
      exact GlobalDuskinEdgeOver.mappingNerveVertexEquiv_toMappingVertex _
    _ = mappingNerveVertexEquiv X Y
          ((mappingNerveVertexEquiv X Y).symm q.hom) := by
      change
        mappingNerveVertexEquiv X Y
            ((R.inverse ((mappingNerveVertexEquiv X Y).symm q.hom)).toMappingVertex) =
          mappingNerveVertexEquiv X Y
            ((mappingNerveVertexEquiv X Y).symm q.hom)
      exact congrArg (mappingNerveVertexEquiv X Y)
        (R.right_inv ((mappingNerveVertexEquiv X Y).symm q.hom))
    _ = q.hom := by
      exact Equiv.apply_symm_apply _ _

/-- Hence every represented adjoint equivalence is a global Duskin equivalence edge. -/
theorem globalEdgeOfEquivalence_isEquivalenceEdge
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (R : GlobalDuskinEdgeRepresentability B X Y)
    (q : X ≌ Y) :
    IsGlobalDuskinEquivalenceEdge (globalEdgeOfEquivalence R q) := by
  exact ⟨q, (globalEdgeOfEquivalence_toArrow R q).symm⟩

/--
Object univalence converts a global Duskin equivalence edge into an object path.
The chosen adjoint equivalence is the witness carried by the edge predicate.
-/
def pathOfGlobalDuskinEquivalenceEdge
    {B : Type u} [Bicategory.{w, v} B]
    (U : ObjectUnivalence B)
    {X Y : B}
    (e : GlobalDuskinEdgeOver B X Y)
    (he : IsGlobalDuskinEquivalenceEdge e) : X = Y :=
  (U.pathEquiv X Y).symm he.choose

/-- The univalence image of the recovered path has exactly the original global edge arrow. -/
theorem pathEquiv_hom_pathOfGlobalDuskinEquivalenceEdge
    {B : Type u} [Bicategory.{w, v} B]
    (U : ObjectUnivalence B)
    {X Y : B}
    (e : GlobalDuskinEdgeOver B X Y)
    (he : IsGlobalDuskinEquivalenceEdge e) :
    (U.pathEquiv X Y (pathOfGlobalDuskinEquivalenceEdge U e he)).hom = e.toArrow := by
  rw [Equiv.apply_symm_apply]
  exact he.choose_spec

/--
Conversely, under edge representability an object path gives a global Duskin
edge representing the adjoint equivalence selected by object univalence.
-/
def globalEdgeOfPath
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (R : GlobalDuskinEdgeRepresentability B X Y)
    (U : ObjectUnivalence B)
    (p : X = Y) :
    GlobalDuskinEdgeOver B X Y :=
  globalEdgeOfEquivalence R (U.pathEquiv X Y p)

/-- The path-generated global edge carries exactly the univalence equivalence hom. -/
theorem globalEdgeOfPath_toArrow
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (R : GlobalDuskinEdgeRepresentability B X Y)
    (U : ObjectUnivalence B)
    (p : X = Y) :
    (globalEdgeOfPath R U p).toArrow = (U.pathEquiv X Y p).hom := by
  exact globalEdgeOfEquivalence_toArrow R (U.pathEquiv X Y p)

/-- Every path-generated represented edge is a global Duskin equivalence edge. -/
theorem globalEdgeOfPath_isEquivalenceEdge
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (R : GlobalDuskinEdgeRepresentability B X Y)
    (U : ObjectUnivalence B)
    (p : X = Y) :
    IsGlobalDuskinEquivalenceEdge (globalEdgeOfPath R U p) := by
  exact globalEdgeOfEquivalence_isEquivalenceEdge R (U.pathEquiv X Y p)

/-!
The precise frontier after v1.23 is therefore:

```text
mappingNerve(X,Y)_0 ≃ (X ⟶ Y)                         -- native Mathlib nerveEquiv
fixed-endpoint global Duskin edge -> (X ⟶ Y)           -- proved extraction
fixed-endpoint global Duskin edge -> mapping vertex     -- proved

GlobalDuskinEdgeRepresentability(X,Y)
  -> global edge type ≃ mappingNerve(X,Y)_0             -- proved conditionally

ObjectUnivalence B
  + represented adjoint-equivalence edge
  <-> object-path-facing data at the one-skeleton        -- proved interfaces
```

Still open, and not silently implied by the one-skeleton result:

* construction of a simplicial global mapping object from the Duskin nerve;
* comparison with `mappingNerve X Y` in all simplicial degrees;
* compatibility with composition, scaling, and the v1.22 horn family;
* a conditional equivalence of the full local complete-Segal and global scaled
  Duskin presentations.
-/

end KUOS.DependentOriginationGlobalDuskinLocalMappingComparisonV1_23
