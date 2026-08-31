import Mathlib
import KUOS.DependentOriginationFunctorialTransportV0_1
import KUOS.GaugeInvariantDependentOriginationActionGroupoidV0_1
import KUOS.DependentOriginationTwoCellCoherenceV1_5

namespace KUOS.DependentOriginationContextualGaugeTheoryV0_1

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.GaugeInvariantDependentOriginationActionGroupoidV0_1
open KUOS.DependentOriginationTwoCellCoherenceV1_5

universe u v w y

variable {X : Type u} {Gauge : Type w}

/-!
# Contextual gauge theory v0.1

This file places the already formalized KuuOS action-groupoid gauge layer inside
its more general dependent-origination transport spine.

The precise theorem boundary is algebraic:

* an action groupoid becomes an actual Mathlib category of gauge contexts;
* a group action on a fiber gives a `Type`-valued transport functor;
* every such gauge transport has an explicit inverse;
* a gauge-invariant semantic map becomes an invariant KuuOS readout;
* the existing two-cell layer supplies the higher-coherence interface for
  set-truncated realizations.

This does not yet identify a smooth principal-bundle connection, curvature form,
Yang--Mills action, or quantization.  Those are downstream realizations.
-/

/--
A wrapper turning a gauge action groupoid into a genuine category of contexts.
The objects are representatives in `X`; a morphism `x ⟶ y` is an explicit gauge
transformation carrying `x` to `y`.
-/
def ActionContext (Gauge : Type w) (X : Type u) := X

namespace ActionContext

instance [Group Gauge] [MulAction Gauge X] :
    Category.{w} (ActionContext Gauge X) where
  Hom x y := ActionArrow (Gauge := Gauge) x y
  id x := ActionArrow.id (Gauge := Gauge) x
  comp f g := ActionArrow.comp f g
  id_comp f := ActionArrow.comp_id_source f
  comp_id f := ActionArrow.comp_id_target f
  assoc f g h := ActionArrow.comp_assoc f g h

end ActionContext

/--
A representation of the gauge group on `Fiber` defines a state-valued functor on
the action-groupoid context category.  The map attached to an arrow is the
corresponding gauge action on the fiber.
-/
def actionRepresentationFunctor
    {Fiber : Type v}
    [Group Gauge] [MulAction Gauge X] [MulAction Gauge Fiber] :
    ActionContext Gauge X ⥤ Type v where
  obj _ := Fiber
  map f := fun psi => f.1 • psi
  map_id := by
    intro x
    funext psi
    simp [ActionArrow.id]
  map_comp := by
    intro x y z f g
    funext psi
    simp [ActionArrow.comp, mul_smul]

/--
The ordinary algebraic action-groupoid gauge representation is therefore a
KuuOS functorial dependent-origination transport system.
-/
def actionRepresentationTransportSystem
    {Fiber : Type v}
    [Group Gauge] [MulAction Gauge X] [MulAction Gauge Fiber] :
    FunctorialTransportSystem (ActionContext Gauge X) where
  state := actionRepresentationFunctor (X := X) (Gauge := Gauge) (Fiber := Fiber)

@[simp] theorem actionRepresentation_transport_apply
    {Fiber : Type v}
    [Group Gauge] [MulAction Gauge X] [MulAction Gauge Fiber]
    {x y : ActionContext Gauge X}
    (a : x ⟶ y) (psi : Fiber) :
    (actionRepresentationTransportSystem
      (X := X) (Gauge := Gauge) (Fiber := Fiber)).transport a psi =
      a.1 • psi :=
  rfl

/-- Gauge transport is reversible: transport by the inverse arrow undoes it. -/
@[simp] theorem actionRepresentation_inverse_transport_apply
    {Fiber : Type v}
    [Group Gauge] [MulAction Gauge X] [MulAction Gauge Fiber]
    {x y : ActionContext Gauge X}
    (a : x ⟶ y) (psi : Fiber) :
    (actionRepresentationTransportSystem
      (X := X) (Gauge := Gauge) (Fiber := Fiber)).transport
        (ActionArrow.inv a)
        ((actionRepresentationTransportSystem
          (X := X) (Gauge := Gauge) (Fiber := Fiber)).transport a psi) = psi := by
  simp [actionRepresentationTransportSystem, actionRepresentationFunctor,
    FunctorialTransportSystem.transport, ActionArrow.inv, smul_smul]

/-- Gauge transport followed by its inverse also acts as the identity. -/
@[simp] theorem actionRepresentation_transport_inverse_apply
    {Fiber : Type v}
    [Group Gauge] [MulAction Gauge X] [MulAction Gauge Fiber]
    {x y : ActionContext Gauge X}
    (a : x ⟶ y) (psi : Fiber) :
    (actionRepresentationTransportSystem
      (X := X) (Gauge := Gauge) (Fiber := Fiber)).transport a
        ((actionRepresentationTransportSystem
          (X := X) (Gauge := Gauge) (Fiber := Fiber)).transport
            (ActionArrow.inv a) psi) = psi := by
  simp [actionRepresentationTransportSystem, actionRepresentationFunctor,
    FunctorialTransportSystem.transport, ActionArrow.inv, smul_smul]

/-- Every action-groupoid transport map is bijective. -/
theorem actionRepresentation_transport_bijective
    {Fiber : Type v}
    [Group Gauge] [MulAction Gauge X] [MulAction Gauge Fiber]
    {x y : ActionContext Gauge X}
    (a : x ⟶ y) :
    Function.Bijective
      ((actionRepresentationTransportSystem
        (X := X) (Gauge := Gauge) (Fiber := Fiber)).transport a) := by
  constructor
  · intro p q hpq
    have h := congrArg
      (fun z =>
        (actionRepresentationTransportSystem
          (X := X) (Gauge := Gauge) (Fiber := Fiber)).transport
            (ActionArrow.inv a) z)
      hpq
    simpa using h
  · intro psi
    refine ⟨
      (actionRepresentationTransportSystem
        (X := X) (Gauge := Gauge) (Fiber := Fiber)).transport
          (ActionArrow.inv a) psi, ?_⟩
    simp

/--
An ordinary gauge-invariant semantic map on the representation fiber becomes an
`InvariantReadout` on the KuuOS contextual transport system.
-/
def invariantReadoutOfActionGaugeInvariant
    {Fiber : Type v} {Semantic : Type y}
    [Group Gauge] [MulAction Gauge X] [MulAction Gauge Fiber]
    (semantic : Fiber → Semantic)
    (hInvariant : ∀ (g : Gauge) (psi : Fiber),
      semantic (g • psi) = semantic psi) :
    FunctorialTransportSystem.InvariantReadout
      (actionRepresentationTransportSystem
        (X := X) (Gauge := Gauge) (Fiber := Fiber)) Semantic where
  readout := fun _ => semantic
  transport_invariant := by
    intro x z a psi
    exact hInvariant a.1 psi

/--
A higher contextual two-cell acts trivially after choosing the existing
set-truncated realization.  This is the precise v0.1 higher-gauge interface:
source paths may retain two-cell data while the present `Type`-valued transport
forgets that distinction.
-/
theorem higherContextualGaugeCell_transport_eq
    {Context : Type u} [Category.{w} Context]
    (D : FunctorialTransportSystem Context)
    (H : Refinement2CellStructure Context)
    (T : SetTruncatedTwoRealization D H)
    {A B : Context} {f g : A ⟶ B}
    (alpha : H.cell f g) :
    D.transport f = D.transport g :=
  T.respectsCell alpha

/-- Consequently, any state has equal set-truncated transport along related paths. -/
theorem higherContextualGaugeCell_transport_apply_eq
    {Context : Type u} [Category.{w} Context]
    (D : FunctorialTransportSystem Context)
    (H : Refinement2CellStructure Context)
    (T : SetTruncatedTwoRealization D H)
    {A B : Context} {f g : A ⟶ B}
    (alpha : H.cell f g)
    (state : D.state.obj A) :
    D.transport f state = D.transport g state := by
  exact congrFun (higherContextualGaugeCell_transport_eq D H T alpha) state

end KUOS.DependentOriginationContextualGaugeTheoryV0_1
