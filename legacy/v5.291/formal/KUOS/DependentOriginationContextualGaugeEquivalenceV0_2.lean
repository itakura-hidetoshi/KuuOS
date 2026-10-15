import Mathlib
import KUOS.DependentOriginationContextualGaugeTheoryV0_1

namespace KUOS.DependentOriginationContextualGaugeEquivalenceV0_2

open CategoryTheory
open KUOS.DependentOriginationContextualGaugeTheoryV0_1

universe u v w

variable {X : Type u} {Gauge : Type w}

/-!
# Contextual gauge equivalence v0.2

The v0.1 contextual-gauge layer realizes an algebraic gauge-group action as a
`Type`-valued transport functor on the action-groupoid context category.

This file identifies the correct notion of equivalence between two such fiber
realizations.  A gauge-equivariant equivalence of representation fibers induces
a natural isomorphism of the corresponding contextual transport functors.

This is still an algebraic theorem.  It does not identify smooth gauge
transformations of principal-bundle connections, curvature, or Yang--Mills
fields; those require an explicit geometric realization downstream.
-/

/--
An equivalence of two gauge representation fibers that intertwines the gauge
action pointwise.
-/
structure GaugeEquivariantEquiv
    (Gauge : Type w) (Fiber₁ Fiber₂ : Type v)
    [Group Gauge] [MulAction Gauge Fiber₁] [MulAction Gauge Fiber₂] where
  toEquiv : Fiber₁ ≃ Fiber₂
  map_smul' : ∀ (g : Gauge) (psi : Fiber₁),
    toEquiv (g • psi) = g • toEquiv psi

namespace GaugeEquivariantEquiv

variable {Fiber₁ Fiber₂ Fiber₃ : Type v}
variable [Group Gauge]
variable [MulAction Gauge Fiber₁] [MulAction Gauge Fiber₂] [MulAction Gauge Fiber₃]

@[simp] theorem map_smul
    (e : GaugeEquivariantEquiv Gauge Fiber₁ Fiber₂)
    (g : Gauge) (psi : Fiber₁) :
    e.toEquiv (g • psi) = g • e.toEquiv psi :=
  e.map_smul' g psi

/-- The identity equivalence is gauge-equivariant. -/
def refl (Gauge : Type w) (Fiber : Type v)
    [Group Gauge] [MulAction Gauge Fiber] :
    GaugeEquivariantEquiv Gauge Fiber Fiber where
  toEquiv := Equiv.refl Fiber
  map_smul' := by
    intro g psi
    rfl

/-- The inverse of a gauge-equivariant equivalence is gauge-equivariant. -/
def symm (e : GaugeEquivariantEquiv Gauge Fiber₁ Fiber₂) :
    GaugeEquivariantEquiv Gauge Fiber₂ Fiber₁ where
  toEquiv := e.toEquiv.symm
  map_smul' := by
    intro g psi
    apply e.toEquiv.injective
    simpa using (e.map_smul' g (e.toEquiv.symm psi)).symm

/-- Gauge-equivariant fiber equivalences compose. -/
def trans
    (e₁₂ : GaugeEquivariantEquiv Gauge Fiber₁ Fiber₂)
    (e₂₃ : GaugeEquivariantEquiv Gauge Fiber₂ Fiber₃) :
    GaugeEquivariantEquiv Gauge Fiber₁ Fiber₃ where
  toEquiv := e₁₂.toEquiv.trans e₂₃.toEquiv
  map_smul' := by
    intro g psi
    change e₂₃.toEquiv (e₁₂.toEquiv (g • psi)) =
      g • e₂₃.toEquiv (e₁₂.toEquiv psi)
    rw [e₁₂.map_smul', e₂₃.map_smul']

end GaugeEquivariantEquiv

/--
A gauge-equivariant equivalence of representation fibers induces a natural
isomorphism of the corresponding contextual gauge transport functors.

Naturality is exactly the equivariance square

`e (g • psi) = g • e psi`.
-/
def actionRepresentationNatIso
    {Fiber₁ Fiber₂ : Type v}
    [Group Gauge] [MulAction Gauge X]
    [MulAction Gauge Fiber₁] [MulAction Gauge Fiber₂]
    (e : GaugeEquivariantEquiv Gauge Fiber₁ Fiber₂) :
    actionRepresentationFunctor
        (X := X) (Gauge := Gauge) (Fiber := Fiber₁) ≅
      actionRepresentationFunctor
        (X := X) (Gauge := Gauge) (Fiber := Fiber₂) :=
  NatIso.ofComponents
    (fun _ => e.toEquiv.toIso)
    (by
      intro x y a
      funext psi
      exact e.map_smul' a.1 psi)

/--
The induced natural isomorphism commutes pointwise with every contextual gauge
transport map.
-/
@[simp] theorem gaugeEquivariantEquiv_transport_naturality
    {Fiber₁ Fiber₂ : Type v}
    [Group Gauge] [MulAction Gauge X]
    [MulAction Gauge Fiber₁] [MulAction Gauge Fiber₂]
    (e : GaugeEquivariantEquiv Gauge Fiber₁ Fiber₂)
    {x y : ActionContext Gauge X}
    (a : x ⟶ y) (psi : Fiber₁) :
    e.toEquiv
        ((actionRepresentationTransportSystem
          (X := X) (Gauge := Gauge) (Fiber := Fiber₁)).transport a psi) =
      (actionRepresentationTransportSystem
        (X := X) (Gauge := Gauge) (Fiber := Fiber₂)).transport a
          (e.toEquiv psi) := by
  exact e.map_smul' a.1 psi

/--
Equivariant equivalence therefore preserves the transport orbit relation in both
directions.
-/
theorem gaugeEquivariantEquiv_transport_iff
    {Fiber₁ Fiber₂ : Type v}
    [Group Gauge] [MulAction Gauge X]
    [MulAction Gauge Fiber₁] [MulAction Gauge Fiber₂]
    (e : GaugeEquivariantEquiv Gauge Fiber₁ Fiber₂)
    {x y : ActionContext Gauge X}
    (a : x ⟶ y) (psi phi : Fiber₁) :
    (actionRepresentationTransportSystem
        (X := X) (Gauge := Gauge) (Fiber := Fiber₁)).transport a psi = phi ↔
      (actionRepresentationTransportSystem
        (X := X) (Gauge := Gauge) (Fiber := Fiber₂)).transport a
          (e.toEquiv psi) = e.toEquiv phi := by
  constructor
  · intro h
    rw [← gaugeEquivariantEquiv_transport_naturality
      (X := X) (Gauge := Gauge) e a psi, h]
  · intro h
    apply e.toEquiv.injective
    rw [gaugeEquivariantEquiv_transport_naturality
      (X := X) (Gauge := Gauge) e a psi]
    exact h

end KUOS.DependentOriginationContextualGaugeEquivalenceV0_2
