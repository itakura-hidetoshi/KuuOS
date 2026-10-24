import KUOS.Architecture.QiWuxingCyclicGroupPathsV3_1
import Kuu.F112.PolygonBoundary
import Mathlib.Tactic

/-!
# Qi v3.4 — REAL C60 pentagonal five-phase GAUGE, not a graph presentation

Replace the historical five-vertex pentagram-quiver model as the
FORWARD physical five-phase presentation by the existing faithful
ZMod 5 group action. Each of the original twelve pentagon charts
chooses a phase frame. The 5 original physical slots/darts are
permuted by local gauge translations; NO physical vertex or edge
is created, deleted or identified.

相生 is gauge-covariant translation by 1 and 相剋 by 2,
and these remain genuinely different primitive histories in
the existing Qi v3.1 free-typed source, even when two generation
steps have the same phase readout as one control step.

The historical v5.169 quiver results remain mathematical history;
no Gray import, graph adjacency masquerading as a higher cell,
new logical axiom, sorry or admit is used in this gauge replacement.
-/

namespace KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical
set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- Independent local frame at each of the twelve ACTUAL C60
pentagons (one for each original icosahedral vertex). -/
abbrev NativeC60FivePhaseGauge := Vertex → FivePhase

/-- Apply the Qi group action to one of the FIVE ORIGINAL
physical C60 sectors, without building any quiver. -/
def nativeC60GaugeSlot
    (frame : NativeC60FivePhaseGauge)
    (v : Vertex) (phase : FivePhase) : Slot :=
  ringSlot (rotation (frame v) phase)

/-- The genuine physical dart occupying the chosen phase chart. -/
def nativeC60GaugeDart
    (frame : NativeC60FivePhaseGauge)
    (v : Vertex) (phase : FivePhase) : Dart :=
  incidentDart v (nativeC60GaugeSlot frame v phase)

/-- Actual physical sector index after gauge rotation. -/
theorem nativeC60GaugeSlot_index
    (frame : NativeC60FivePhaseGauge)
    (v : Vertex) (phase : FivePhase) :
    slotIndex (nativeC60GaugeSlot frame v phase) =
      rotation (frame v) phase := by
  exact slotIndex_ringSlot _

/-- The gauge chart is a genuine permutation of FIVE original
physical slots, rather than an artificial directed K5 relation. -/
theorem nativeC60GaugeSlot_injective
    (frame : NativeC60FivePhaseGauge)
    (v : Vertex) :
    Function.Injective (nativeC60GaugeSlot frame v) := by
  intro x y hxy
  have h := congrArg slotIndex hxy
  rw [nativeC60GaugeSlot_index, nativeC60GaugeSlot_index] at h
  exact (rotation (frame v)).injective h

/-- A zero-frame chart is the original verified C60 cyclic slot. -/
theorem nativeC60GaugeSlot_zero
    (v : Vertex) (phase : FivePhase) :
    nativeC60GaugeSlot (fun _ => 0) v phase = ringSlot phase := by
  simp [nativeC60GaugeSlot, rotation]

/-- Successive local gauge changes are EXACTLY the group action
composition, not a path in a graph. -/
theorem nativeC60GaugeSlot_comp
    (g h : NativeC60FivePhaseGauge)
    (v : Vertex) (phase : FivePhase) :
    nativeC60GaugeSlot (fun x => g x + h x) v phase =
      nativeC60GaugeSlot h v (rotation (g v) phase) := by
  simp [nativeC60GaugeSlot, rotation, add_assoc]

/-- Gauge covariance of 相生 as a translation on the exact
pentagonal sector index. This preserves the five-sector geometry. -/
theorem nativeC60GaugeSheng_index
    (frame : NativeC60FivePhaseGauge)
    (v : Vertex) (phase : FivePhase) :
    slotIndex (nativeC60GaugeSlot frame v (generationPhase phase)) =
      slotIndex (nativeC60GaugeSlot frame v phase) + 1 := by
  rw [nativeC60GaugeSlot_index, nativeC60GaugeSlot_index]
  change (phase + 1) + frame v = phase + frame v + 1
  abel

/-- Gauge covariance of 相剋 as translation by TWO, distinct
from a one-step generation even after choosing a new chart. -/
theorem nativeC60GaugeKe_index
    (frame : NativeC60FivePhaseGauge)
    (v : Vertex) (phase : FivePhase) :
    slotIndex (nativeC60GaugeSlot frame v (controlPhase phase)) =
      slotIndex (nativeC60GaugeSlot frame v phase) + 2 := by
  rw [nativeC60GaugeSlot_index, nativeC60GaugeSlot_index]
  change (phase + 2) + frame v = phase + frame v + 2
  abel

/-- Both phase actions coexist in the same real C60 chart but
their generator rotations do not collapse to one another. -/
theorem nativeC60Gauge_sheng_ke_distinct :
    rotation (1 : FivePhase) ≠ rotation (2 : FivePhase) :=
  rotation_generation_ne_control

/-- Exact injectivity of the existing original C60 five-slot index. -/
theorem nativeC60SlotIndex_injective : Function.Injective slotIndex := by
  decide

/-- The full five-sector local physical chart is still a
permutation, with no missing or additional dart slots. -/
theorem nativeC60GaugeSlot_surjective
    (frame : NativeC60FivePhaseGauge)
    (v : Vertex) :
    Function.Surjective (nativeC60GaugeSlot frame v) := by
  intro s
  refine ⟨(rotation (frame v)).symm (slotIndex s), ?_⟩
  apply nativeC60SlotIndex_injective
  rw [nativeC60GaugeSlot_index]
  simpa using (rotation (frame v)).apply_symm_apply (slotIndex s)

#print axioms nativeC60GaugeSlot_index
#print axioms nativeC60GaugeSlot_injective
#print axioms nativeC60GaugeSlot_zero
#print axioms nativeC60GaugeSlot_comp
#print axioms nativeC60GaugeSheng_index
#print axioms nativeC60GaugeKe_index
#print axioms nativeC60Gauge_sheng_ke_distinct
#print axioms nativeC60SlotIndex_injective
#print axioms nativeC60GaugeSlot_surjective

end
end KUOS.Architecture.WuxingCyclicPaths
