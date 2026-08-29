import Mathlib.CategoryTheory.Enriched.Basic
import KUOS.DependentOriginationCoreSpineV1_12

namespace KUOS.DependentOriginationEnrichedContextV1_13

open CategoryTheory
open MonoidalCategory
open KUOS.DependentOriginationFunctorialTransportV0_1

universe u v w x y

/-!
# Enriched contextual dependent origination v1.13

The parent dependent-origination core records whether a composable contextual
transport exists and how it acts on states.  This layer adds an orthogonal
"relation texture" axis using Mathlib's native enriched-category API.

For a monoidal category `V`, the relation from `X` to `Y` is represented by the
`V`-object

```text
X ⟶[V] Y.
```

An ordinary contextual arrow is explicitly realized as a generalized element
of that hom object.  Identity and composition are required to agree with the
native enriched identity and enriched composition maps.

This does not replace the ordinary parent category.  It decorates its arrows
with a chosen `V`-valued relation structure, allowing later specializations in
which homs carry order, metric, linear, probabilistic, or other monoidal data.
-/

/--
An ordinary dependent-origination transport system together with a native
`V`-enriched texture on its context category.

`liftHom` says how each ordinary contextual transport is represented as a
`𝟙_ V`-shaped generalized element of the enriched hom object.
-/
structure EnrichedDependentOriginationSystem
    (V : Type v) [Category.{w} V] [MonoidalCategory V]
    (Context : Type u) [Category.{x} Context] [EnrichedCategory V Context] where
  base : FunctorialTransportSystem.{u, x, y} Context
  liftHom : forall {X Y : Context},
    (X ⟶ Y) -> (𝟙_ V ⟶ X ⟶[V] Y)
  lift_id : forall X : Context,
    liftHom (𝟙 X) = eId V X
  lift_comp : forall {X Y Z : Context}
    (f : X ⟶ Y) (g : Y ⟶ Z),
    liftHom (f ≫ g) =
      ((λ_ (𝟙_ V)).inv ≫ (liftHom f ⊗ₘ liftHom g)) ≫
        eComp V X Y Z

namespace EnrichedDependentOriginationSystem

/-- The enriched hom object is the texture carried by a contextual relation. -/
abbrev HomTexture
    {V : Type v} [Category.{w} V] [MonoidalCategory V]
    {Context : Type u} [Category.{x} Context] [EnrichedCategory V Context]
    (E : EnrichedDependentOriginationSystem V Context)
    (X Y : Context) : V :=
  X ⟶[V] Y

/-- Ordinary identity transport is represented by the native enriched identity. -/
theorem enriched_identity
    {V : Type v} [Category.{w} V] [MonoidalCategory V]
    {Context : Type u} [Category.{x} Context] [EnrichedCategory V Context]
    (E : EnrichedDependentOriginationSystem V Context)
    (X : Context) :
    E.liftHom (𝟙 X) = eId V X :=
  E.lift_id X

/-- Ordinary sequential composition is represented by native enriched composition. -/
theorem enriched_composition
    {V : Type v} [Category.{w} V] [MonoidalCategory V]
    {Context : Type u} [Category.{x} Context] [EnrichedCategory V Context]
    (E : EnrichedDependentOriginationSystem V Context)
    {X Y Z : Context}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    E.liftHom (f ≫ g) =
      ((λ_ (𝟙_ V)).inv ≫ (E.liftHom f ⊗ₘ E.liftHom g)) ≫
        eComp V X Y Z :=
  E.lift_comp f g

/-- The old state transport law remains exactly the parent functor law. -/
theorem state_transport_composition
    {V : Type v} [Category.{w} V] [MonoidalCategory V]
    {Context : Type u} [Category.{x} Context] [EnrichedCategory V Context]
    (E : EnrichedDependentOriginationSystem V Context)
    {X Y Z : Context}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (s : E.base.state.obj X) :
    E.base.transport (f ≫ g) s =
      E.base.transport g (E.base.transport f s) :=
  E.base.transport_comp_apply f g s

end EnrichedDependentOriginationSystem

/-- Every ordinary category has the canonical `Type`-enrichment from Mathlib. -/
@[reducible] def ordinaryTypeEnrichment
    (Context : Type u) [Category.{x} Context] :
    EnrichedCategory (Type x) Context :=
  enrichedCategoryTypeOfCategory Context

/-!
The structural boundary is:

```text
ordinary contextual transport
  + chosen V-enrichment
  + ordinary-arrow generalized-element realization
  = enriched dependent-origination relation texture.
```

No particular choice of `V` is forced by the parent theory, and enrichment does
not imply causality, stack descent, or higher homotopy coherence by itself.
-/

end KUOS.DependentOriginationEnrichedContextV1_13
