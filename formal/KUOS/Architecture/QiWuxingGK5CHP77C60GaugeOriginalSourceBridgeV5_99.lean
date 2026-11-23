import KUOS.Architecture.QiWuxingGK5CHP77ReversedUnitFreeContextFaithfulnessV5_98
import KUOS.Architecture.QiWuxingNativeC60GaugeV3_4

/-!
Qi v5.99 — authentic C60 five-phase gauge shadow of original old18D
one-unit proof contexts, with a certified local faithfulness boundary.

The physical side is the EXISTING C60 twelve-pentagon atlas:
Vertex, Slot, Dart, Edge and NativeC60FivePhaseGauge.
The source side is the EXISTING genuine dependent old18D:
SelectedLocalEighteen, original v5.73 internal bracket, original v5.92
Sigma unit payloads, and the certified v5.98 reverse/chain contexts.

A deliberately EXPLICIT observation map takes the number of strict
leaves in a genuine unit-free nonassociative context modulo five.
It selects a real C60 pentagonal physical slot, dart and around-edge
via the existing five-phase local gauge. The map is not claimed to
be the unique or canonical physical interpretation of an old18D
proof. Gauge changes must be paired with the corresponding phase
coordinate shift to preserve the actual physical incidence objects.

The C60 physical slot/edge alone IS NOT faithful to old18D evidence:
a strict leaf and a reversed strict leaf have the same five-phase
charge but distinct original raw reverse/chain values. In contrast,
within the v5.98 primitive-unit-plus-unit-free-context fragment,
the C60 physical observation JOINED with exact original bracket
and full original typed Sigma payload history reflects both
unit-free context and actual original primitive raw proof equality.

The explicit reduction to a physical C60 sector is a chosen model
map, not a descent of every original old18D proof, nor an assertion
that C60 physical Edge equals categorical NatIso or F55 Hom.
The unrestricted v5.93 same-bracket/different-raw one-unit source
existence remains NO_DATA. No 19D old/new quotient comparison,
cross-fiber identification, global curved incidence repair, or
WORLD/20D gluing is inferred.

Pinned Lean/mathlib, root107, original source Types, and protected
PR #1558 remain unchanged.
append-only / tighten-only / overwrite-forbidden / same-root.
-/

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uSix

namespace KUOS.Architecture.WuxingPentagonUnified
namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell

open KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical

variable {W : Type uSix}

/-- An EXPLICIT map from original v5.88 unit-free context syntax
to the EXISTING physical Qi/C60 five-phase carrier.
It intentionally forgets more than the full old18D bracket. -/
def selectedV599C60ContextPhase (t : SelectedV588UnitFreeTerm) :
    FivePhase :=
  (selectedV594InnerStrictCount (selectedV588UnitFreeBracket t) :
    FivePhase)

/-- ACTUAL C60 pentagonal sector at one existing vertex chart. -/
def selectedV599C60PhysicalSlot
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (t : SelectedV588UnitFreeTerm) : Slot :=
  nativeC60GaugeSlot frame v (selectedV599C60ContextPhase t)

/-- ACTUAL original physical dart at the five-phase sector. -/
def selectedV599C60PhysicalDart
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (t : SelectedV588UnitFreeTerm) : Dart :=
  nativeC60GaugeDart frame v (selectedV599C60ContextPhase t)

/-- ACTUAL C60 around-edge, not a surrogate graph path. -/
/-- Physical C60 five-sector around-edge of the CHOSEN phase. -/
def selectedV599C60SideAt
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (p : FivePhase) : Edge :=
  .around ⟨v, nativeC60GaugeSlot frame v p⟩

def selectedV599C60PhysicalSide
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (t : SelectedV588UnitFreeTerm) : Edge :=
  selectedV599C60SideAt frame v (selectedV599C60ContextPhase t)

/-- A local change of C60 pentagonal coordinate frame. -/
def selectedV599C60GaugeShift
    (frame delta : NativeC60FivePhaseGauge) :
    NativeC60FivePhaseGauge :=
  fun v => frame v + delta v

/-- Coordinate compensation of a chosen phase by the local gauge. -/
def selectedV599C60Rephase
    (delta : NativeC60FivePhaseGauge) (v : Vertex)
    (p : FivePhase) : FivePhase :=
  p - delta v

/-- Genuine physical Slot covariance under change of the local
C60 gauge frame and inverse change of the phase coordinate. -/
theorem selectedV599C60GaugeSlot_covariant
    (frame delta : NativeC60FivePhaseGauge)
    (v : Vertex) (p : FivePhase) :
    nativeC60GaugeSlot (selectedV599C60GaugeShift frame delta) v
        (selectedV599C60Rephase delta v p) =
      nativeC60GaugeSlot frame v p := by
  apply nativeC60SlotIndex_injective
  rw [nativeC60GaugeSlot_index, nativeC60GaugeSlot_index]
  change (p - delta v) + (frame v + delta v) = p + frame v
  abel

/-- The same covariance holds for the ACTUAL native C60 dart. -/
theorem selectedV599C60GaugeDart_covariant
    (frame delta : NativeC60FivePhaseGauge)
    (v : Vertex) (p : FivePhase) :
    nativeC60GaugeDart (selectedV599C60GaugeShift frame delta) v
        (selectedV599C60Rephase delta v p) =
      nativeC60GaugeDart frame v p := by
  change incidentDart v
      (nativeC60GaugeSlot (selectedV599C60GaugeShift frame delta)
        v (selectedV599C60Rephase delta v p)) =
    incidentDart v (nativeC60GaugeSlot frame v p)
  rw [selectedV599C60GaugeSlot_covariant frame delta v p]

/-- The physical C60 around-edge is unchanged by a compensated
gauge coordinate shift; this is genuine physical incidence. -/
theorem selectedV599C60GaugeSide_covariant
    (frame delta : NativeC60FivePhaseGauge)
    (v : Vertex) (p : FivePhase) :
    selectedV599C60SideAt (selectedV599C60GaugeShift frame delta) v
        (selectedV599C60Rephase delta v p) =
      selectedV599C60SideAt frame v p := by
  unfold selectedV599C60SideAt
  rw [selectedV599C60GaugeSlot_covariant frame delta v p]

/-- The old18D context chooses an ACTUAL physical C60 around-edge
whose endpoints are the two genuine incident darts. -/
theorem selectedV599C60ContextSide_endpoints
    (frame : NativeC60FivePhaseGauge)
    (v : Vertex) (t : SelectedV588UnitFreeTerm) :
    edgeEndpoints (selectedV599C60PhysicalSide frame v t) =
      (selectedV599C60PhysicalDart frame v t,
       incidentDart v (slotNext (selectedV599C60PhysicalSlot frame v t))) := by
  rfl

/-- This chosen five-phase shadow is NOT injective on old18D
context shapes: strict and reversed strict have the same phase. -/
theorem selectedV599C60Phase_strict_reverse_same :
    selectedV599C60ContextPhase .strict =
      selectedV599C60ContextPhase (.reversed .strict) := rfl

/-- The contexts remain different original free syntax even
though their physical five-phase charge is identical. -/
theorem selectedV599C60Strict_reverse_distinct :
    (SelectedV588UnitFreeTerm.strict) ≠
      .reversed .strict := by
  decide

section OriginalDependentUnitC60Bridge

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable (J N : SelectedContextualSeventeen W l r H K)

/-- One precise interface between an actual physical C60 sector+edge
and the SAME genuine original old18D reversed raw proof observations.
It retains original bracket and FULL Sigma typed unit payload.
No quotienting, no graph replacement, and no source Type equality
between physical and categorical objects is introduced. -/
def selectedV599C60OriginalJointObservation
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (t : SelectedV588UnitFreeTerm)
    (M : SelectedLocalEighteen W l r J N) :
    (Slot × Edge) ×
      (SelectedInheritedOldInnerBracket ×
        List (SelectedV592OriginalUnitAtom l r H K)) :=
  ⟨⟨selectedV599C60PhysicalSlot frame v t,
      selectedV599C60PhysicalSide frame v t⟩,
    ⟨selectedLocalEighteenInnerBracket l r
        (selectedV598ReverseLeftContext l r J N t M),
      selectedV592OriginalUnitHistory l r
        (selectedV598ReverseLeftContext l r J N t M)⟩⟩

/-- The physical C60 observation PLUS both original proof
observations is jointly faithful on the certified restricted
v5.98 fragment, in the SAME genuine original 17D fiber. -/
theorem selectedV599C60OriginalJointObservation_eq_iff
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (M L : SelectedLocalEighteen W l r J N)
    (hM : selectedV597OriginalPrimitiveUnit l r M)
    (hL : selectedV597OriginalPrimitiveUnit l r L)
    (t u : SelectedV588UnitFreeTerm) :
    (selectedV599C60OriginalJointObservation l r J N frame v t M =
      selectedV599C60OriginalJointObservation l r J N frame v u L) ↔
      (t = u ∧ M = L) := by
  constructor
  · intro h
    have hb := congrArg (fun x => x.2.1) h
    have hh := congrArg (fun x => x.2.2) h
    exact (selectedV598ReverseLeft_jointEq_iff
      l r J N M L hM hL t u).mp ⟨hb, hh⟩
  · rintro ⟨rfl, rfl⟩
    rfl

/-- Reframing the C60 physical part of the observation does not
change the ACTUAL physical incidence or original proof evidence. -/
def selectedV599C60CompensatedJointObservation
    (frame delta : NativeC60FivePhaseGauge) (v : Vertex)
    (t : SelectedV588UnitFreeTerm)
    (M : SelectedLocalEighteen W l r J N) :
    (Slot × Edge) ×
      (SelectedInheritedOldInnerBracket ×
        List (SelectedV592OriginalUnitAtom l r H K)) :=
  ⟨⟨nativeC60GaugeSlot (selectedV599C60GaugeShift frame delta) v
        (selectedV599C60Rephase delta v (selectedV599C60ContextPhase t)),
      selectedV599C60SideAt (selectedV599C60GaugeShift frame delta) v
        (selectedV599C60Rephase delta v (selectedV599C60ContextPhase t))⟩,
    ⟨selectedLocalEighteenInnerBracket l r
        (selectedV598ReverseLeftContext l r J N t M),
      selectedV592OriginalUnitHistory l r
        (selectedV598ReverseLeftContext l r J N t M)⟩⟩

/-- Real C60 gauge covariance and original old18D typed provenance
glue exactly at the explicitly chosen LOCAL interface. -/
theorem selectedV599C60Compensated_jointEq
    (frame delta : NativeC60FivePhaseGauge) (v : Vertex)
    (t : SelectedV588UnitFreeTerm)
    (M : SelectedLocalEighteen W l r J N) :
    selectedV599C60CompensatedJointObservation
        l r J N frame delta v t M =
      selectedV599C60OriginalJointObservation l r J N frame v t M := by
  unfold selectedV599C60CompensatedJointObservation
    selectedV599C60OriginalJointObservation
    selectedV599C60PhysicalSlot selectedV599C60PhysicalSide
  rw [selectedV599C60GaugeSlot_covariant frame delta v
        (selectedV599C60ContextPhase t),
      selectedV599C60GaugeSide_covariant frame delta v
        (selectedV599C60ContextPhase t)]

/-- Even under DIFFERENT local C60 gauge transformations, the
compensated source/observation correspondence remains faithful
when the real primitive unit witnesses are fixed. -/
theorem selectedV599C60Compensated_jointEq_iff
    (frame delta eps : NativeC60FivePhaseGauge) (v : Vertex)
    (M L : SelectedLocalEighteen W l r J N)
    (hM : selectedV597OriginalPrimitiveUnit l r M)
    (hL : selectedV597OriginalPrimitiveUnit l r L)
    (t u : SelectedV588UnitFreeTerm) :
    (selectedV599C60CompensatedJointObservation
        l r J N frame delta v t M =
      selectedV599C60CompensatedJointObservation
        l r J N frame eps v u L) ↔ (t = u ∧ M = L) := by
  rw [selectedV599C60Compensated_jointEq l r J N frame delta v t M,
    selectedV599C60Compensated_jointEq l r J N frame eps v u L]
  exact selectedV599C60OriginalJointObservation_eq_iff
    l r J N frame v M L hM hL t u

/-- Concrete obstruction: a single original genuine primitive
old18D unit proof admits TWO distinct original reversed raw values
with the SAME physical C60 Slot, SAME actual physical C60 Edge and
SAME FULL typed original unit payload history. The source bracket,
however, is different. This is a conditional theorem at the
supplied genuine J->N primitive unit; no global inhabitance claim. -/
theorem selectedV599C60PhysicalShadow_notRawFaithful
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (M : SelectedLocalEighteen W l r J N)
    (hM : selectedV597OriginalPrimitiveUnit l r M) :
    (selectedV599C60PhysicalSlot frame v .strict =
      selectedV599C60PhysicalSlot frame v (.reversed .strict)) ∧
    (selectedV599C60PhysicalSide frame v .strict =
      selectedV599C60PhysicalSide frame v (.reversed .strict)) ∧
    (selectedV592OriginalUnitHistory l r
        (selectedV598ReverseLeftContext l r J N .strict M) =
      selectedV592OriginalUnitHistory l r
        (selectedV598ReverseLeftContext l r J N (.reversed .strict) M)) ∧
    (selectedLocalEighteenInnerBracket l r
        (selectedV598ReverseLeftContext l r J N .strict M) ≠
      selectedLocalEighteenInnerBracket l r
        (selectedV598ReverseLeftContext l r J N (.reversed .strict) M)) ∧
    (selectedV598ReverseLeftContext l r J N .strict M ≠
      selectedV598ReverseLeftContext l r J N (.reversed .strict) M) := by
  have hp := selectedV599C60Phase_strict_reverse_same
  have hs :
      selectedV599C60PhysicalSlot frame v .strict =
        selectedV599C60PhysicalSlot frame v (.reversed .strict) := by
    exact congrArg (nativeC60GaugeSlot frame v) hp
  have he :
      selectedV599C60PhysicalSide frame v .strict =
        selectedV599C60PhysicalSide frame v (.reversed .strict) := by
    exact congrArg (selectedV599C60SideAt frame v) hp
  have hh :
      selectedV592OriginalUnitHistory l r
          (selectedV598ReverseLeftContext l r J N .strict M) =
        selectedV592OriginalUnitHistory l r
          (selectedV598ReverseLeftContext l r J N (.reversed .strict) M) := by
    rw [selectedV598ReverseLeft_history,
      selectedV598ReverseLeft_history]
  have hb :
      selectedLocalEighteenInnerBracket l r
          (selectedV598ReverseLeftContext l r J N .strict M) ≠
        selectedLocalEighteenInnerBracket l r
          (selectedV598ReverseLeftContext l r J N (.reversed .strict) M) := by
    intro hbr
    have hdecode :=
      (selectedV598ReverseLeft_jointEq_iff
        l r J N M M hM hM .strict (.reversed .strict)).mp ⟨hbr, hh⟩
    exact selectedV599C60Strict_reverse_distinct hdecode.1
  have hraw :
      selectedV598ReverseLeftContext l r J N .strict M ≠
        selectedV598ReverseLeftContext l r J N (.reversed .strict) M := by
    intro h
    exact hb (congrArg (selectedLocalEighteenInnerBracket l r) h)
  exact ⟨hs, he, hh, hb, hraw⟩

end OriginalDependentUnitC60Bridge

#print axioms PentagonAdjoinedSixCell.selectedV599C60ContextPhase
#print axioms PentagonAdjoinedSixCell.selectedV599C60PhysicalSlot
#print axioms PentagonAdjoinedSixCell.selectedV599C60PhysicalDart
#print axioms PentagonAdjoinedSixCell.selectedV599C60SideAt
#print axioms PentagonAdjoinedSixCell.selectedV599C60PhysicalSide
#print axioms PentagonAdjoinedSixCell.selectedV599C60GaugeShift
#print axioms PentagonAdjoinedSixCell.selectedV599C60Rephase
#print axioms PentagonAdjoinedSixCell.selectedV599C60GaugeSlot_covariant
#print axioms PentagonAdjoinedSixCell.selectedV599C60GaugeDart_covariant
#print axioms PentagonAdjoinedSixCell.selectedV599C60GaugeSide_covariant
#print axioms PentagonAdjoinedSixCell.selectedV599C60ContextSide_endpoints
#print axioms PentagonAdjoinedSixCell.selectedV599C60Phase_strict_reverse_same
#print axioms PentagonAdjoinedSixCell.selectedV599C60Strict_reverse_distinct
#print axioms PentagonAdjoinedSixCell.selectedV599C60OriginalJointObservation
#print axioms PentagonAdjoinedSixCell.selectedV599C60OriginalJointObservation_eq_iff
#print axioms PentagonAdjoinedSixCell.selectedV599C60CompensatedJointObservation
#print axioms PentagonAdjoinedSixCell.selectedV599C60Compensated_jointEq
#print axioms PentagonAdjoinedSixCell.selectedV599C60Compensated_jointEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV599C60PhysicalShadow_notRawFaithful

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
