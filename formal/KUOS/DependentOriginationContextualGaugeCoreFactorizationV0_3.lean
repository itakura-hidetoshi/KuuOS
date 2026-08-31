import Mathlib
import KUOS.DependentOriginationContextualCoreV1_0
import KUOS.DependentOriginationContextualGaugeEquivalenceV0_2

namespace KUOS.DependentOriginationContextualGaugeCoreFactorizationV0_3

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationContextualGaugeTheoryV0_1
open KUOS.DependentOriginationContextualGaugeEquivalenceV0_2
open KUOS.GaugeInvariantDependentOriginationActionGroupoidV0_1

universe u v w z

variable {X : Type u} {Gauge : Type w}

/-!
# Contextual gauge core factorization v0.3

The parent KuuOS dependent-origination structure remains a `Type`-valued functor
on an arbitrary category of contexts, so irreversible transport is still allowed.

For a groupoid context, however, every context morphism is invertible.  Mathlib
therefore lets the state functor factor canonically through `Core (Type)`, the
groupoid whose morphisms are type isomorphisms.  This file makes that categorical
landing zone explicit and then specializes it to the action-groupoid gauge layer.

Thus the hierarchy is now formalized as

```
general contextual transport : Context ⥤ Type
reversible contextual transport : GroupoidContext ⥤ Core (Type)
action-groupoid gauge transport : ActionContext Gauge X ⥤ Core (Type)
```

This remains algebraic.  It does not identify a smooth principal-bundle
connection or parallel transport.  In particular, no claim is made that a
non-flat connection factors through the ordinary fundamental groupoid.
-/

/-! ## Generic reversible contextual transport -/

namespace FunctorialTransportSystem

variable {Context : Type u} [Groupoid.{v} Context]

/--
A dependent-origination state functor on a groupoid context canonically lands in
the core of `Type`: every contextual transport map is recorded together with its
inverse as an actual categorical isomorphism.
-/
noncomputable def coreStateFunctor
    (D : FunctorialTransportSystem Context) :
    Context ⥤ Core (Type z) :=
  Core.functorToCore D.state

@[simp] theorem coreStateFunctor_obj_of
    (D : FunctorialTransportSystem Context)
    (A : Context) :
    (coreStateFunctor D).obj A |>.of = D.state.obj A :=
  rfl

@[simp] theorem coreStateFunctor_map_iso_hom
    (D : FunctorialTransportSystem Context)
    {A B : Context} (f : A ⟶ B) :
    ((coreStateFunctor D).map f).iso.hom = D.state.map f :=
  rfl

/-- Forgetting the explicit isomorphism witness recovers the original state functor. -/
noncomputable def coreStateFactorizationIso
    (D : FunctorialTransportSystem Context) :
    coreStateFunctor D ⋙ Core.inclusion (Type z) ≅ D.state :=
  Iso.refl _

/-- In a reversible context every state-map morphism is an isomorphism in `Type`. -/
theorem stateMap_isIso
    (D : FunctorialTransportSystem Context)
    {A B : Context} (f : A ⟶ B) :
    IsIso (D.state.map f) := by
  infer_instance

end FunctorialTransportSystem

/-! ## The action context is genuinely a groupoid -/

namespace ActionContext

/--
The category introduced in v0.1 is not merely groupoid-like: its explicit
`ActionArrow.inv` supplies a Mathlib `Groupoid` instance.
-/
instance [Group Gauge] [MulAction Gauge X] :
    Groupoid.{w} (ActionContext Gauge X) where
  inv := fun a => ActionArrow.inv a
  inv_comp := by
    intro x y a
    exact ActionArrow.inv_comp a
  comp_inv := by
    intro x y a
    exact ActionArrow.comp_inv a

@[simp] theorem groupoid_inv_eq_actionArrow_inv
    [Group Gauge] [MulAction Gauge X]
    {x y : ActionContext Gauge X}
    (a : x ⟶ y) :
    Groupoid.inv a = ActionArrow.inv a :=
  rfl

end ActionContext

/-! ## Gauge representation as a `Core (Type)`-valued functor -/

/--
An algebraic gauge representation is a reversible dependent-origination
transport functor whose true categorical codomain can be tightened from `Type`
to `Core (Type)`.
-/
noncomputable def actionRepresentationCoreFunctor
    {Fiber : Type v}
    [Group Gauge] [MulAction Gauge X] [MulAction Gauge Fiber] :
    ActionContext Gauge X ⥤ Core (Type v) :=
  FunctorialTransportSystem.coreStateFunctor
    (actionRepresentationTransportSystem
      (X := X) (Gauge := Gauge) (Fiber := Fiber))

@[simp] theorem actionRepresentationCoreFunctor_obj_of
    {Fiber : Type v}
    [Group Gauge] [MulAction Gauge X] [MulAction Gauge Fiber]
    (x : ActionContext Gauge X) :
    (actionRepresentationCoreFunctor
      (X := X) (Gauge := Gauge) (Fiber := Fiber)).obj x |>.of = Fiber :=
  rfl

@[simp] theorem actionRepresentationCoreFunctor_map_iso_hom_apply
    {Fiber : Type v}
    [Group Gauge] [MulAction Gauge X] [MulAction Gauge Fiber]
    {x y : ActionContext Gauge X}
    (a : x ⟶ y) (psi : Fiber) :
    ((actionRepresentationCoreFunctor
      (X := X) (Gauge := Gauge) (Fiber := Fiber)).map a).iso.hom psi =
      a.1 • psi :=
  rfl

/--
Forgetting `Core (Type)` recovers exactly the v0.1 `Type`-valued gauge transport
functor, now with reversibility carried categorically rather than only as a
pointwise bijectivity theorem.
-/
noncomputable def actionRepresentationCoreFactorizationIso
    {Fiber : Type v}
    [Group Gauge] [MulAction Gauge X] [MulAction Gauge Fiber] :
    actionRepresentationCoreFunctor
        (X := X) (Gauge := Gauge) (Fiber := Fiber) ⋙
      Core.inclusion (Type v) ≅
    actionRepresentationFunctor
        (X := X) (Gauge := Gauge) (Fiber := Fiber) :=
  FunctorialTransportSystem.coreStateFactorizationIso
    (actionRepresentationTransportSystem
      (X := X) (Gauge := Gauge) (Fiber := Fiber))

/-- Every gauge-representation transport map is an isomorphism in `Type`. -/
theorem actionRepresentation_map_isIso
    {Fiber : Type v}
    [Group Gauge] [MulAction Gauge X] [MulAction Gauge Fiber]
    {x y : ActionContext Gauge X}
    (a : x ⟶ y) :
    IsIso
      ((actionRepresentationFunctor
        (X := X) (Gauge := Gauge) (Fiber := Fiber)).map a) := by
  infer_instance

end KUOS.DependentOriginationContextualGaugeCoreFactorizationV0_3
