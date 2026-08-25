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

Version 1.25 established presentation independence for two different higher
presentations of the same bicategory.  The next structural step is to allow the
underlying bicategorical model itself to change.

The invariant is still not a chosen nerve.  It is the intrinsic bicategorical
carrier.  A change of model is represented by Whitehead-style biequivalence
data:

* a native Mathlib pseudofunctor `F : B ⥤ᵖ C`;
* for every `X,Y : B`, an equivalence of hom-categories

```text
B(X,Y) ≌ C(FX,FY)
```

whose forward functor is exactly the native hom-functor induced by `F`;
* essential surjectivity on objects up to bicategorical adjoint equivalence.

This is sufficient to prove that intrinsic mapping data and every observable
factoring through that data transport independently of the chosen bicategorical
model.  It also gives a canonical route from a source global Duskin edge or
comparison cell to the target local mapping nerve without requiring a direct
map between the two global Duskin nerves.

That distinction is deliberate.  A general pseudofunctor need not be strictly
unitary, whereas the current global Duskin presentation uses strictly unitary
normal-lax simplices.  Direct global-to-global transport therefore requires a
separate normalization theorem.  The intrinsic invariant does not.
-/

/-! ## Whitehead-style bicategorical model equivalence data -/

/--
Concrete biequivalence data adequate for presentation-independent transport.

The local equivalences are required to agree exactly with the native hom-functors
of the pseudofunctor.  Thus the categorical equivalences are not unrelated
witnesses: they certify that the actual action of `forward` is locally an
equivalence.
-/
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

/-- The certified hom-equivalence acts on morphisms exactly by pseudofunctorial `map₂`. -/
@[simp] theorem homEquiv_functor_map
    {X Y : B} {f g : X ⟶ Y}
    (α : f ⟶ g) :
    (E.homEquiv X Y).functor.map α = E.forward.map₂ α := by
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

/-- The equivalence presentation and the pseudofunctor transport give the same intrinsic 1-cell. -/
@[simp] theorem homEquiv_transportIntrinsicOneCell_agree
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B}
    (f : X ⟶ Y) :
    (E.homEquiv X Y).functor.obj f = transportIntrinsicOneCell E f := by
  exact E.homEquiv_functor_obj f

/-- The equivalence presentation and the pseudofunctor transport give the same intrinsic 2-cell. -/
@[simp] theorem homEquiv_transportIntrinsicTwoCell_agree
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B} {f g : X ⟶ Y}
    (α : f ⟶ g) :
    (E.homEquiv X Y).functor.map α = transportIntrinsicTwoCell E α := by
  exact E.homEquiv_functor_map α

/-! ## Transport of local mapping presentations -/

/--
Transport a local mapping-nerve vertex by first reading its intrinsic 1-cell,
transporting that 1-cell, then re-encoding it as a target local vertex.
-/
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

/--
Transport a local mapping edge by reading the intrinsic 2-cell, applying
`map₂`, and using the native nerve edge constructor in the target hom-category.
-/
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

/-- Every target-side observable of a transported intrinsic 2-cell is independent of encoding. -/
theorem twoCellObservable_modelIndependent
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    {X Y : B} {f g : X ⟶ Y}
    {Z : Sort z}
    (Φ : (E.forward.map f ⟶ E.forward.map g) → Z)
    (α : f ⟶ g) :
    Φ ((E.homEquiv X Y).functor.map α) =
      Φ (transportIntrinsicTwoCell E α) := by
  rw [homEquiv_transportIntrinsicTwoCell_agree]

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
    P ((E.homEquiv X Y).functor.map α) ↔
      P (transportIntrinsicTwoCell E α) := by
  rw [homEquiv_transportIntrinsicTwoCell_agree]

/-! ## Source global presentation to target local presentation -/

/--
A source global Duskin edge is transported to a target local mapping vertex via
the intrinsic carrier.  No target global Duskin simplex is needed.
-/
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
  rw [transportLocalMappingVertex_invariant]
  rw [globalEdge_localVertex_invariant_agree]

/--
A source global Duskin comparison cell is transported to a target local mapping
edge through the intrinsic 2-cell carrier.
-/
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
  rw [transportLocalMappingEdge_invariant]
  rw [globalTriangle_localEdge_invariant_agree]

/-! ## Bundled theorem-level invariant certificate -/

/--
The automatic invariant consequences of Whitehead-style bicategorical model
equivalence data at the current one- and two-cell frontier.
-/
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

/-- Every bicategorical model-equivalence certificate canonically supplies the current invariant package. -/
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
        ↓  hom-category equivalence induced by native pseudofunctor
target intrinsic bicategory
        ↓
target local mapping presentation
```

and every square above commutes in dimensions one and two.

The remaining global-to-global issue is now sharply isolated: construct a
strictly-unitary normalization of pseudofunctorial Duskin transport and prove
that it induces the same intrinsic map.  That future normalization cannot
change the invariant established here; it can only provide another presentation
of the same transported intrinsic data.
-/

end KUOS.DependentOriginationBiequivalencePresentationInvariantV1_26
