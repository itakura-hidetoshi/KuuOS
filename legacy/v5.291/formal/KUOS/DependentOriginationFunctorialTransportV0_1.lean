import Mathlib

namespace KUOS.DependentOriginationFunctorialTransportV0_1

open CategoryTheory

universe u v w y

/--
A dependent-origination transport system is a state-valued functor on a category
of contexts.  Objects are conditioned presentations/contexts; morphisms are
admissible relations; `state.map` is transport along those relations.

The functor laws are the mathematical core of the transport reading of 縁起:
identity relations act trivially and transport along a composite relation is the
composition of the corresponding transports.
-/
structure FunctorialTransportSystem
    (Context : Type u) [Category.{v} Context] where
  state : Context ⥤ Type w

namespace FunctorialTransportSystem

variable {Context : Type u} [Category.{v} Context]

/-- Transport a state along one admissible context morphism. -/
def transport
    (D : FunctorialTransportSystem Context)
    {X Z : Context} (f : X ⟶ Z) :
    D.state.obj X → D.state.obj Z :=
  D.state.map f

/-- Identity context change leaves every state unchanged. -/
@[simp] theorem transport_id_apply
    (D : FunctorialTransportSystem Context)
    (X : Context) (x : D.state.obj X) :
    D.transport (𝟙 X) x = x := by
  simpa [transport] using congrFun (D.state.map_id X) x

/-- Transport along a composite relation is composition of transports. -/
theorem transport_comp_apply
    (D : FunctorialTransportSystem Context)
    {X Y Z : Context}
    (f : X ⟶ Y) (g : Y ⟶ Z) (x : D.state.obj X) :
    D.transport (f ≫ g) x =
      D.transport g (D.transport f x) := by
  simpa [transport] using congrFun (D.state.map_comp f g) x

/--
A semantic/readout layer invariant under admissible transport.

This is the elementwise form of a map from the state functor to constant
semantics: presentation may change, while the invariant semantic value does not.
-/
structure InvariantReadout
    (D : FunctorialTransportSystem Context)
    (Semantic : Type y) where
  readout : (X : Context) → D.state.obj X → Semantic
  transport_invariant :
    ∀ {X Z : Context} (f : X ⟶ Z) (x : D.state.obj X),
      readout Z (D.transport f x) = readout X x

namespace InvariantReadout

variable {D : FunctorialTransportSystem Context}
variable {Semantic : Type y}

/-- Invariant meaning is unchanged along a two-step dependent-origination path. -/
theorem readout_comp
    (R : InvariantReadout D Semantic)
    {X Y Z : Context}
    (f : X ⟶ Y) (g : Y ⟶ Z) (x : D.state.obj X) :
    R.readout Z (D.transport g (D.transport f x)) =
      R.readout X x := by
  rw [← D.transport_comp_apply f g x]
  exact R.transport_invariant (f ≫ g) x

end InvariantReadout

end FunctorialTransportSystem

/--
One-object/additive specialization of functorial transport.

This is the algebraic surface needed for Euclidean positive-time transfer:
`transport 0 = id` and `transport (s+t) = transport s ∘ transport t`.
No invertibility is assumed, so contraction semigroups and irreversible updates
fit here, unlike a groupoid-only formulation.
-/
structure AdditiveEndoTransport
    (Time : Type u) [AddMonoid Time]
    (State : Type v) where
  transport : Time → State → State
  transport_zero : ∀ x : State, transport 0 x = x
  transport_add : ∀ (s t : Time) (x : State),
    transport (s + t) x = transport s (transport t x)

namespace AdditiveEndoTransport

variable {Time : Type u} [AddMonoid Time]
variable {State : Type v}

/-- Time zero is the identity transport. -/
@[simp] theorem zero_apply
    (T : AdditiveEndoTransport Time State) (x : State) :
    T.transport 0 x = x :=
  T.transport_zero x

/-- Additive composition is the one-object form of functorial composition. -/
theorem add_apply
    (T : AdditiveEndoTransport Time State)
    (s t : Time) (x : State) :
    T.transport (s + t) x = T.transport s (T.transport t x) :=
  T.transport_add s t x

end AdditiveEndoTransport

/--
Norm-contractive additive transport, matching the structural level of an OS
positive-time contraction semigroup before specifying its generator.
-/
structure ContractiveAdditiveEndoTransport
    (Time : Type u) [AddMonoid Time]
    (State : Type v) [SeminormedAddCommGroup State]
    extends AdditiveEndoTransport Time State where
  norm_transport_le : ∀ (t : Time) (x : State),
    ‖transport t x‖ ≤ ‖x‖

/--
A distinguished vacuum/reference state fixed by every contractive transport.
This is the minimal KuuOS-side interface needed to align the generic transport
spine with OS transfer-operator semantics without importing the physical repo.
-/
structure VacuumContractiveAdditiveEndoTransport
    (Time : Type u) [AddMonoid Time]
    (State : Type v) [SeminormedAddCommGroup State]
    extends ContractiveAdditiveEndoTransport Time State where
  vacuum : State
  vacuum_fixed : ∀ t : Time, transport t vacuum = vacuum

end KUOS.DependentOriginationFunctorialTransportV0_1
