import KUOS.DependentOriginationFunctorialTransportV0_1
import KUOS.GaugeInvariantDependentOriginationGroupoidCechDescentV0_1

namespace KUOS.GaugeInvariantDependentOriginationFunctorialTransportBridgeV0_1

open KUOS.GaugeInvariantDependentOriginationActionGroupoidV0_1
open KUOS.GaugeInvariantDependentOriginationGroupoidCechDescentV0_1

universe u v w t

variable {X : Type u} {Y : Type v} {Gauge : Type w} {Index : Type t}

/--
The existing action-groupoid Čech layer supplies the identity law required by
the reversible branch of functorial dependent-origination transport.
-/
theorem action_groupoid_cech_transport_identity
    [Group Gauge] [MulAction Gauge X]
    (datum : ActionGroupoidCechDatum Gauge X Index)
    (i : Index) :
    datum.transition i i =
      ActionArrow.id (Gauge := Gauge) (datum.object i) :=
  datum.transition_self i

/--
The existing exact Čech cocycle is precisely the composition law for reversible
transport: first `i → j`, then `j → k`, equals the direct transport `i → k`.
-/
theorem action_groupoid_cech_transport_composition
    [Group Gauge] [MulAction Gauge X]
    (datum : ActionGroupoidCechDatum Gauge X Index)
    (i j k : Index) :
    ActionArrow.comp (datum.transition i j) (datum.transition j k) =
      datum.transition i k :=
  datum.transition_cocycle i j k

/--
Arrow-constant semantics on the existing action groupoid is exactly the
transport-invariant semantic condition on the gauge/Čech specialization.
-/
theorem action_groupoid_cech_semantics_transport_invariant
    [Group Gauge] [MulAction Gauge X]
    (datum : ActionGroupoidCechDatum Gauge X Index)
    (semantic : X → Y)
    (hArrow : ∀ {x y : X}, ActionArrow (Gauge := Gauge) x y →
      semantic y = semantic x) :
    CechSemanticCompatible datum semantic :=
  cechSemanticCompatible_of_arrow_constancy datum semantic hArrow

/--
For a nonempty Čech presentation, transport-invariant semantics has one unique
glued value.  This keeps the existing gauge theorem as the reversible
specialization of the broader functorial transport spine.
-/
theorem action_groupoid_cech_unique_glued_transport_semantics
    [Group Gauge] [MulAction Gauge X] [Nonempty Index]
    (datum : ActionGroupoidCechDatum Gauge X Index)
    (semantic : X → Y)
    (hArrow : ∀ {x y : X}, ActionArrow (Gauge := Gauge) x y →
      semantic y = semantic x) :
    ∃! y : Y, ∀ i : Index, semantic (datum.object i) = y :=
  existsUnique_gluedSemantic_of_arrow_constancy datum semantic hArrow

end KUOS.GaugeInvariantDependentOriginationFunctorialTransportBridgeV0_1
