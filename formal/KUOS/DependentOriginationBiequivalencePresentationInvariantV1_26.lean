import KUOS.DependentOriginationPresentationIndependentInvariantV1_25
import Mathlib.CategoryTheory.Bicategory.Functor.Pseudofunctor
import Mathlib.CategoryTheory.Equivalence

namespace KUOS.DependentOriginationBiequivalencePresentationInvariantV1_26

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open scoped Bicategory
open KUOS.DependentOriginationInfinityTwoYonedaV1_18
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinLocalMappingComparisonV1_23
open KUOS.DependentOriginationGlobalDuskinLocalTwoCellComparisonV1_24
open KUOS.DependentOriginationPresentationIndependentInvariantV1_25

universe u₁ u₂ v₁ v₂ w₁ w₂ z

/-!
# Biequivalence-level presentation invariance v1.26

Version 1.25 established presentation independence for two higher presentations
of the same bicategory.  Here the underlying bicategorical model may also
change.  The transport datum consists of a pseudofunctor, hom-category
equivalences whose forward functors are the pseudofunctorial hom functors, and
essential surjectivity on objects up to intrinsic adjoint equivalence.

Under Lean 4.31 the equality of the two hom functors must be treated as a
*dependent* equality on their morphism maps: their object maps are propositionally
equal, so the raw morphisms live in propositionally equal hom-types.  We expose
that fact by `HEq` and use the pinned pseudofunctor hom-functor as the canonical
endpoint-fixed representative for observable transport.
-/

/-- Whitehead-style bicategorical model-equivalence data used by the invariant layer. -/
structure BicategoricalModelEquivalence
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C] where
  forward : B ⥤ᵖ C
  homEquiv :
    ∀ X Y : B,
      (X ⟶ Y) ≌ (forward.obj X ⟶ forward.obj Y)
  homEquiv_functor :
    ∀ X Y : B,
      (homEquiv X Y).functor =
        forward.toPrelaxFunctor.mapFunctor X Y
  object_essentially_surjective :
    ∀ Z : C,
      ∃ X : B, IntrinsicObjectEquivalent (forward.obj X) Z

namespace BicategoricalModelEquivalence

variable
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)

/-- The intrinsic mapping carrier is transported by the certified hom-category equivalence. -/
def mappingInvariantEquivalence (X Y : B) :
    PresentationIndependentMappingInvariant X Y ≌
      PresentationIndependentMappingInvariant (E.forward.obj X) (E.forward.obj Y) :=
  E.homEquiv X Y

/-- The certified hom-equivalence acts on objects exactly by pseudofunctorial map. -/
@[simp] theorem homEquiv_functor_obj
    {X Y : B}
    (f : X ⟶ Y) :
    (E.homEquiv X Y).functor.obj f = E.forward.map f := by
  rw [E.homEquiv_functor X Y]
  rfl

/--
The morphism action of the certified hom-equivalence is the pseudofunctorial
`map₂`.  `HEq` is the correct equality because the two sides have endpoints
identified by `homEquiv_functor_obj`, rather than definitionally identical
endpoints.
-/
theorem homEquiv_functor_map
    {X Y : B} {f g : X ⟶ Y}
    (α : f ⟶ g) :
    HEq ((E.homEquiv X Y).functor.map α) (E.forward.map₂ α) := by
  rw [E.homEquiv_functor X Y]
  rfl

/-- Every target object is represented, up to intrinsic object equivalence, by an image object. -/
theorem targetObject_covered
    (Z : C) :
    ∃ X : B, IntrinsicObjectEquivalent (E.forward.obj X) Z :=
  E.object_essentially_surjective Z

end BicategoricalModelEquivalence

/-! ## Intrinsic one- and two-cell transport -/

/-- Transport an intrinsic 1-cell through the pseudofunctor underlying a model equivalence. -/
def transportIntrinsicOneCell
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B}
    (f : PresentationIndependentMappingInvariant X Y) :
    PresentationIndependentMappingInvariant (E.forward.obj X) (E.forward.obj Y) :=
  E.forward.map f

/-- Transport an intrinsic 2-cell through the pseudofunctor underlying a model equivalence. -/
def transportIntrinsicTwoCell
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B} {f g : X ⟶ Y}
    (α : f ⟶ g) :
    E.forward.map f ⟶ E.forward.map g :=
  E.forward.map₂ α

/--
Endpoint-fixed representative of the hom-equivalence morphism action.
The structure field `homEquiv_functor` certifies that this is precisely the
forward functor of `homEquiv`, while its type is definitionally expressed using
`E.forward.map` endpoints.
-/
def homEquivTwoCell
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B} {f g : X ⟶ Y}
    (α : f ⟶ g) :
    E.forward.map f ⟶ E.forward.map g :=
  (E.forward.toPrelaxFunctor.mapFunctor X Y).map α

/-- The equivalence presentation and pseudofunctor transport give the same intrinsic 1-cell. -/
@[simp] theorem homEquiv_transportIntrinsicOneCell_agree
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B}
    (f : X ⟶ Y) :
    (E.homEquiv X Y).functor.obj f = transportIntrinsicOneCell E f := by
  exact BicategoricalModelEquivalence.homEquiv_functor_obj E f

/-- The raw hom-equivalence map and intrinsic two-cell transport agree dependently. -/
theorem homEquiv_transportIntrinsicTwoCell_agree
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B} {f g : X ⟶ Y}
    (α : f ⟶ g) :
    HEq ((E.homEquiv X Y).functor.map α) (transportIntrinsicTwoCell E α) := by
  exact BicategoricalModelEquivalence.homEquiv_functor_map E α

/-- The endpoint-fixed hom-equivalence representative is literally pseudofunctorial `map₂`. -/
@[simp] theorem homEquivTwoCell_eq_transportIntrinsicTwoCell
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B} {f g : X ⟶ Y}
    (α : f ⟶ g) :
    homEquivTwoCell E α = transportIntrinsicTwoCell E α :=
  rfl

/-! ## Transport of local mapping presentations -/

/-- Transport a local mapping vertex through the intrinsic 1-cell carrier. -/
def transportLocalMappingVertex
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B}
    (x : MappingNerveVertex X Y) :
    MappingNerveVertex (E.forward.obj X) (E.forward.obj Y) :=
  (mappingNerveVertexEquiv (E.forward.obj X) (E.forward.obj Y)).symm
    (E.forward.map (localOneCellInvariant x))

/-- Reading the transported local vertex recovers exactly the transported intrinsic 1-cell. -/
@[simp] theorem transportLocalMappingVertex_invariant
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B}
    (x : MappingNerveVertex X Y) :
    localOneCellInvariant (transportLocalMappingVertex E x) =
      E.forward.map (localOneCellInvariant x) := by
  change
    (mappingNerveVertexEquiv (E.forward.obj X) (E.forward.obj Y))
      ((mappingNerveVertexEquiv (E.forward.obj X) (E.forward.obj Y)).symm
        (E.forward.map (localOneCellInvariant x))) =
      E.forward.map (localOneCellInvariant x)
  exact
    Equiv.apply_symm_apply
      (mappingNerveVertexEquiv (E.forward.obj X) (E.forward.obj Y))
      (E.forward.map (localOneCellInvariant x))

/-- Transport a local mapping edge through the intrinsic 2-cell carrier. -/
def transportLocalMappingEdge
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B} {f g : X ⟶ Y}
    (e : MappingNerveEdge X Y f g) :
    MappingNerveEdge
      (E.forward.obj X)
      (E.forward.obj Y)
      (E.forward.map f)
      (E.forward.map g) :=
  localMappingEdgeOfTwoMorphism
    (E.forward.map₂ (localTwoCellInvariant e))

/-- Reading the transported local edge recovers exactly the transported intrinsic 2-cell. -/
@[simp] theorem transportLocalMappingEdge_invariant
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B} {f g : X ⟶ Y}
    (e : MappingNerveEdge X Y f g) :
    localTwoCellInvariant (transportLocalMappingEdge E e) =
      E.forward.map₂ (localTwoCellInvariant e) := by
  simpa [transportLocalMappingEdge, localTwoCellInvariant] using
    (localMappingEdgeOfTwoMorphism_hom
      (α := E.forward.map₂ (localTwoCellInvariant e)))

/-! ## Universal observable independence under model replacement -/

/-- Every target-side observable of a transported intrinsic 1-cell is independent of encoding. -/
theorem oneCellObservable_modelIndependent
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B}
    {Z : Sort z}
    (Φ : (E.forward.obj X ⟶ E.forward.obj Y) → Z)
    (f : X ⟶ Y) :
    Φ ((E.homEquiv X Y).functor.obj f) =
      Φ (transportIntrinsicOneCell E f) := by
  rw [homEquiv_transportIntrinsicOneCell_agree]

/--
Every target-side observable of a transported intrinsic 2-cell is independent
of encoding.  `homEquivTwoCell` is the endpoint-fixed representative of the
certified hom-equivalence morphism action.
-/
theorem twoCellObservable_modelIndependent
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B} {f g : X ⟶ Y}
    {Z : Sort z}
    (Φ : (E.forward.map f ⟶ E.forward.map g) → Z)
    (α : f ⟶ g) :
    Φ (homEquivTwoCell E α) =
      Φ (transportIntrinsicTwoCell E α) := by
  rw [homEquivTwoCell_eq_transportIntrinsicTwoCell]

/-- Proposition-valued one-cell invariants are likewise independent of model encoding. -/
theorem oneCellPredicate_modelIndependent
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B}
    (P : (E.forward.obj X ⟶ E.forward.obj Y) → Prop)
    (f : X ⟶ Y) :
    P ((E.homEquiv X Y).functor.obj f) ↔
      P (transportIntrinsicOneCell E f) := by
  rw [homEquiv_transportIntrinsicOneCell_agree]

/-- Proposition-valued two-cell invariants are likewise independent of model encoding. -/
theorem twoCellPredicate_modelIndependent
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B} {f g : X ⟶ Y}
    (P : (E.forward.map f ⟶ E.forward.map g) → Prop)
    (α : f ⟶ g) :
    P (homEquivTwoCell E α) ↔
      P (transportIntrinsicTwoCell E α) := by
  rw [homEquivTwoCell_eq_transportIntrinsicTwoCell]

/-! ## Source global presentation to target local presentation -/

/-- A source global Duskin edge is transported to a target local mapping vertex via the intrinsic carrier. -/
def transportGlobalEdgeToTargetLocalVertex
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B}
    (e : GlobalDuskinEdgeOver B X Y) :
    MappingNerveVertex (E.forward.obj X) (E.forward.obj Y) :=
  transportLocalMappingVertex E e.toMappingVertex

/-- The cross-model edge route commutes with the intrinsic 1-cell invariant. -/
@[simp] theorem transportGlobalEdgeToTargetLocalVertex_invariant
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B}
    (e : GlobalDuskinEdgeOver B X Y) :
    localOneCellInvariant (transportGlobalEdgeToTargetLocalVertex E e) =
      E.forward.map (globalOneCellInvariant e) := by
  change
    localOneCellInvariant (transportLocalMappingVertex E e.toMappingVertex) =
      E.forward.map (globalOneCellInvariant e)
  rw [transportLocalMappingVertex_invariant]
  rw [globalEdge_localVertex_invariant_agree]

/-- A source global Duskin comparison cell is transported to a target local mapping edge. -/
def transportGlobalTriangleComparisonToTargetLocalEdge
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    (σ : DuskinSimplex B 2) :
    MappingNerveEdge
      (E.forward.obj (duskinTriangleSource σ))
      (E.forward.obj (duskinTriangleTarget σ))
      (E.forward.map (duskinTriangleCompositeArrow σ))
      (E.forward.map (duskinTriangleLongArrow σ)) :=
  transportLocalMappingEdge E (duskinComparisonMappingEdge σ)

/-- The cross-model two-cell route commutes with the intrinsic comparison cell. -/
@[simp] theorem transportGlobalTriangleComparisonToTargetLocalEdge_invariant
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    (σ : DuskinSimplex B 2) :
    localTwoCellInvariant
      (transportGlobalTriangleComparisonToTargetLocalEdge E σ) =
      E.forward.map₂ (globalTwoCellInvariant σ) := by
  change
    localTwoCellInvariant
      (transportLocalMappingEdge E (duskinComparisonMappingEdge σ)) =
      E.forward.map₂ (globalTwoCellInvariant σ)
  rw [transportLocalMappingEdge_invariant]
  rw [globalTriangle_localEdge_invariant_agree]

/-! ## Bundled theorem-level invariant certificate -/

/-- The automatic invariant consequences at the current one- and two-cell frontier. -/
structure PresentationIndependentInvariantUnderModelEquivalence
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C) : Prop where
  mapping_carriers_equivalent :
    ∀ X Y : B,
      Nonempty
        (PresentationIndependentMappingInvariant X Y ≌
          PresentationIndependentMappingInvariant
            (E.forward.obj X) (E.forward.obj Y))
  local_vertices_commute :
    ∀ {X Y : B} (x : MappingNerveVertex X Y),
      localOneCellInvariant (transportLocalMappingVertex E x) =
        E.forward.map (localOneCellInvariant x)
  local_edges_commute :
    ∀ {X Y : B} {f g : X ⟶ Y} (e : MappingNerveEdge X Y f g),
      localTwoCellInvariant (transportLocalMappingEdge E e) =
        E.forward.map₂ (localTwoCellInvariant e)
  target_objects_covered :
    ∀ Z : C,
      ∃ X : B, IntrinsicObjectEquivalent (E.forward.obj X) Z

/-- Every bicategorical model-equivalence certificate supplies the current invariant package. -/
def presentationIndependentInvariantUnderModelEquivalence
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C) :
    PresentationIndependentInvariantUnderModelEquivalence E where
  mapping_carriers_equivalent := fun X Y =>
    ⟨E.mappingInvariantEquivalence X Y⟩
  local_vertices_commute := transportLocalMappingVertex_invariant E
  local_edges_commute := transportLocalMappingEdge_invariant E
  target_objects_covered := E.targetObject_covered

/-!
The v1.26 frontier is therefore

```text
source local/global presentation
        ↓
source intrinsic bicategory
        ↓  certified hom-category equivalence / pseudofunctor
target intrinsic bicategory
        ↓
target local mapping presentation
```

The remaining global-to-global issue is the strictly-unitary normalization of
pseudofunctorial Duskin transport.  Such a normalization can only add another
presentation of the transported intrinsic data established here.
-/

end KUOS.DependentOriginationBiequivalencePresentationInvariantV1_26
