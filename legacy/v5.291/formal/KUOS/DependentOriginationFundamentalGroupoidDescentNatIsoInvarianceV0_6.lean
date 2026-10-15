import Mathlib
import KUOS.DependentOriginationFundamentalGroupoidDescentObstructionV0_5

namespace KUOS.DependentOriginationFundamentalGroupoidDescentNatIsoInvarianceV0_6

open CategoryTheory
open KUOS.DependentOriginationContextualGaugeTheoryV0_1
open KUOS.DependentOriginationContextualGaugeEquivalenceV0_2
open KUOS.DependentOriginationFundamentalGroupoidTransportV0_4
open KUOS.DependentOriginationFundamentalGroupoidDescentObstructionV0_5

universe u v w z

/-!
# Fundamental-groupoid descent is invariant under transport natural isomorphism v0.6

The v0.5 layer identifies a necessary morphism-kernel condition for a finer
transport to descend through a quotient

`Q : P ⥤ FundamentalGroupoid Base`

and packages concrete violations as descent obstructions.

This file proves that those notions depend only on the natural-isomorphism
class of the fine transport functor.  If

`e : S₁ ≅ S₂`,

then parallel fine arrows have equal `S₁`-transport maps exactly when they have
equal `S₂`-transport maps.  Consequently quotient-kernel compatibility,
quotient-kernel obstruction, and existence of a fundamental-groupoid descent
presentation are all invariant under replacement of the transport by a
naturally isomorphic presentation.

The final section applies this to the existing contextual gauge spine:
a gauge-equivariant equivalence of representation fibers induces the required
natural isomorphism, so fundamental-groupoid descent and its kernel obstruction
are unchanged by that gauge-equivariant change of fiber presentation.

This remains a categorical transport theorem.  It does not construct smooth
parallel transport, a thin-path groupoid, curvature, a Yang--Mills action,
quantization, a Hamiltonian, a continuum limit, or a mass gap.
-/

variable {P : Type u} [Category P]
variable {Base : Type w} [TopologicalSpace Base]
variable {Q : P ⥤ FundamentalGroupoid Base}
variable {S₁ S₂ : P ⥤ Type v}

/--
Equality of transport maps on parallel arrows is preserved by a natural
isomorphism of transport functors.
-/
theorem map_eq_of_natIso
    (e : S₁ ≅ S₂)
    {a b : P} (f g : a ⟶ b)
    (h : S₁.map f = S₁.map g) :
    S₂.map f = S₂.map g := by
  apply (cancel_epi (e.hom.app a)).1
  calc
    e.hom.app a ≫ S₂.map f = S₁.map f ≫ e.hom.app b :=
      (e.hom.naturality f).symm
    _ = S₁.map g ≫ e.hom.app b := by rw [h]
    _ = e.hom.app a ≫ S₂.map g :=
      e.hom.naturality g

/--
Parallel-arrow transport equality is therefore exactly invariant under natural
isomorphism of the fine transport presentation.
-/
theorem map_eq_iff_natIso
    (e : S₁ ≅ S₂)
    {a b : P} (f g : a ⟶ b) :
    S₁.map f = S₁.map g ↔ S₂.map f = S₂.map g := by
  constructor
  · exact map_eq_of_natIso e f g
  · exact map_eq_of_natIso e.symm f g

/-- Quotient-kernel compatibility depends only on the natural-isomorphism class. -/
theorem quotientKernelCompatible_iff_natIso
    (e : S₁ ≅ S₂) :
    QuotientKernelCompatible Q S₁ ↔ QuotientKernelCompatible Q S₂ := by
  constructor
  · intro h a b f g hQ
    exact map_eq_of_natIso e f g (h f g hQ)
  · intro h a b f g hQ
    exact map_eq_of_natIso e.symm f g (h f g hQ)

/--
A concrete quotient-kernel obstruction is likewise invariant under natural
isomorphism of transport presentations.
-/
theorem hasQuotientKernelObstruction_iff_natIso
    (e : S₁ ≅ S₂) :
    HasQuotientKernelObstruction Q S₁ ↔
      HasQuotientKernelObstruction Q S₂ := by
  constructor
  · rintro ⟨a, b, f, g, hQ, hneq⟩
    refine ⟨a, b, f, g, hQ, ?_⟩
    intro h₂
    exact hneq ((map_eq_iff_natIso e f g).2 h₂)
  · rintro ⟨a, b, f, g, hQ, hneq⟩
    refine ⟨a, b, f, g, hQ, ?_⟩
    intro h₁
    exact hneq ((map_eq_iff_natIso e f g).1 h₁)

namespace FundamentalDescent

/--
Transport a fundamental-groupoid descent witness across a natural isomorphism
of fine transport functors, without changing the quotient transport itself.
-/
def transportNatIso
    (D : FundamentalDescent Q S₁)
    (e : S₁ ≅ S₂) :
    FundamentalDescent Q S₂ where
  quotientTransport := D.quotientTransport
  comparison := e.symm.trans D.comparison

end FundamentalDescent

/--
Existence of a fundamental-groupoid descent presentation is invariant under
natural isomorphism of the fine transport.
-/
theorem fundamentalDescent_nonempty_iff_natIso
    (e : S₁ ≅ S₂) :
    Nonempty (FundamentalDescent Q S₁) ↔
      Nonempty (FundamentalDescent Q S₂) := by
  constructor
  · rintro ⟨D⟩
    exact ⟨D.transportNatIso e⟩
  · rintro ⟨D⟩
    exact ⟨D.transportNatIso e.symm⟩

/-- Non-descent is also invariant under natural isomorphism. -/
theorem noFundamentalDescent_iff_natIso
    (e : S₁ ≅ S₂) :
    (¬ Nonempty (FundamentalDescent Q S₁)) ↔
      (¬ Nonempty (FundamentalDescent Q S₂)) :=
  not_congr (fundamentalDescent_nonempty_iff_natIso e)

/-! ## Contextual gauge specialization -/

variable {Rep : Type u} {Gauge : Type z}
variable {Fiber₁ Fiber₂ : Type v}
variable [Group Gauge] [MulAction Gauge Rep]
variable [MulAction Gauge Fiber₁] [MulAction Gauge Fiber₂]
variable {QGauge : ActionContext Gauge Rep ⥤ FundamentalGroupoid Base}

/--
Gauge-equivariantly equivalent representation fibers have equivalent
fundamental-groupoid descent existence for every chosen quotient from the
action context.
-/
theorem actionRepresentation_fundamentalDescent_nonempty_iff
    (e : GaugeEquivariantEquiv Gauge Fiber₁ Fiber₂) :
    Nonempty
        (FundamentalDescent QGauge
          (actionRepresentationFunctor
            (X := Rep) (Gauge := Gauge) (Fiber := Fiber₁))) ↔
      Nonempty
        (FundamentalDescent QGauge
          (actionRepresentationFunctor
            (X := Rep) (Gauge := Gauge) (Fiber := Fiber₂))) :=
  fundamentalDescent_nonempty_iff_natIso
    (Q := QGauge)
    (actionRepresentationNatIso
      (X := Rep) (Gauge := Gauge) e)

/--
The quotient-kernel obstruction is unchanged by a gauge-equivariant change of
representation fiber.
-/
theorem actionRepresentation_obstruction_iff
    (e : GaugeEquivariantEquiv Gauge Fiber₁ Fiber₂) :
    HasQuotientKernelObstruction QGauge
        (actionRepresentationFunctor
          (X := Rep) (Gauge := Gauge) (Fiber := Fiber₁)) ↔
      HasQuotientKernelObstruction QGauge
        (actionRepresentationFunctor
          (X := Rep) (Gauge := Gauge) (Fiber := Fiber₂)) :=
  hasQuotientKernelObstruction_iff_natIso
    (Q := QGauge)
    (actionRepresentationNatIso
      (X := Rep) (Gauge := Gauge) e)

end KUOS.DependentOriginationFundamentalGroupoidDescentNatIsoInvarianceV0_6
