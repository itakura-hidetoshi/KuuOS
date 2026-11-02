import KUOS.Architecture.QiWuxingGK5AEOriginalPhiReturnV3_8
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AFClosedWholePentagonInterchange
import Mathlib.Tactic

/-!
Qi v3.9 / F112-P94D3GK5AF — true physical/categorical
comparison boundary and source-history obstruction.

Genuine C60 around Edge/Dart endpoints and the two independently
constructed Mathlib whole NatIso pentagon routes coexist over the
ORIGINAL Qi FivePhase = ZMod 5 gauge. Both reverse-oriented categorical
edges, 04 and 43, have a genuine physical edge with swapped endpoints:
no comparison pretending that they follow the positive physical
dart orientation can exist.

A second independent obstruction uses the ACTUAL v3.1 free typed
five-phase histories: two different generation/control orderings
share the same phase displacement AND event count. Any observation
factoring through the shift, even after adjoining the original C60
physical endpoint pair and both whole NatIso pentagon routes, is
nonfaithful and has no inverse reconstruction of raw histories.
This is NOT a no-go against all possible comparison data or higher
fillers: extra history-sensitive data remains an explicit obligation.

Kernel-checked 5 = 0, rather than the historical v2.5
native_decide convenience lemma; no new axioms, sorry or source
quotients. Qi imports independent Kuu, never the reverse.
Pinned Lean v4.30.0-rc2/mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, canonical main, same public root107;
protected #1558 Draft/open/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
open KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe vC uC uT

/-- Distinct genuine local slots have distinct genuine incident C60
darts, for ALL twelve original icosahedral vertices. -/
private theorem fivefoldOriginalIncidentDart_injective :
    ∀ v : Vertex, Function.Injective (incidentDart v) := by
  decide

/-- Thus the actual Qi gauge into ORIGINAL physical C60 darts
is injective on the common five-phase carrier. -/
theorem fivefoldOriginalDart_phase_injective
    (frame : NativeC60FivePhaseGauge) (v : Vertex) :
    Function.Injective (nativeC60GaugeDart frame v) := by
  intro p q h
  apply nativeC60GaugeSlot_injective frame v
  exact fivefoldOriginalIncidentDart_injective v h

/-- A categorical edge whose direction opposes the physical positive
cycle has REAL physical endpoints in the reversed order. -/
theorem fivefoldGK5AFReversedPhysicalEndpoints
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (edge : FivefoldEdge)
    (hrev : fivefoldFrom edge = fivefoldFoot edge + 1 ∧
      fivefoldTo edge = fivefoldFoot edge) :
    edgeEndpoints (fivefoldPhysicalEdge frame v edge) =
      (nativeC60GaugeDart frame v (fivefoldTo edge),
       nativeC60GaugeDart frame v (fivefoldFrom edge)) := by
  rw [fivefoldPhysicalEdge, fivefoldSide_endpoints]
  rw [hrev.1, hrev.2]

/-- Precise orientation obstruction: such an edge cannot have
the categorical source/target as its FORWARD physical dart pair.
This is proved from actual C60 dart injectivity and 0 != 1 in ZMod 5. -/
theorem fivefoldGK5AFNoForwardPhysicalComparison
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (edge : FivefoldEdge)
    (hrev : fivefoldFrom edge = fivefoldFoot edge + 1 ∧
      fivefoldTo edge = fivefoldFoot edge) :
    ¬ edgeEndpoints (fivefoldPhysicalEdge frame v edge) =
      (nativeC60GaugeDart frame v (fivefoldFrom edge),
       nativeC60GaugeDart frame v (fivefoldTo edge)) := by
  intro hforward
  have hfront :
      nativeC60GaugeDart frame v (fivefoldFoot edge) =
        nativeC60GaugeDart frame v (fivefoldFoot edge + 1) := by
    have hfirst := congrArg Prod.fst hforward
    simpa [fivefoldPhysicalEdge, fivefoldSide_endpoints, hrev.1] using hfirst
  have hphase := (fivefoldOriginalDart_phase_injective frame v) hfront
  have h01 : (0 : FivefoldIndex) = 1 := by
    have hshift : fivefoldFoot edge + (0 : FivefoldIndex) =
        fivefoldFoot edge + 1 := by
      simpa only [add_zero] using hphase
    exact add_left_cancel hshift
  exact (by decide : (0 : FivefoldIndex) ≠ 1) h01

/-- Both actual GK5 pentagon edges 04 and 43 have the necessary
physical reversal and each rejects a forward-orientation comparison. -/
theorem fivefoldGK5AFBothReverseObstructions
    (frame : NativeC60FivePhaseGauge) (v : Vertex) :
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame v .e04) =
      (nativeC60GaugeDart frame v (fivefoldFrom .e04),
       nativeC60GaugeDart frame v (fivefoldTo .e04))) ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame v .e43) =
      (nativeC60GaugeDart frame v (fivefoldFrom .e43),
       nativeC60GaugeDart frame v (fivefoldTo .e43))) := by
  constructor
  · exact fivefoldGK5AFNoForwardPhysicalComparison frame v .e04
      ⟨fivefoldPhaseTwoReversedEdges.1, rfl⟩
  · exact fivefoldGK5AFNoForwardPhysicalComparison frame v .e43
      ⟨fivefoldPhaseTwoReversedEdges.2, rfl⟩

/-- A concrete C60 physical endpoint/history readout generated
solely by the existing v3.1 phase displacement and event count.
It is NOT the raw free typed path. -/
def fivefoldGK5AFPhysicalHistoryReadout
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (p : FivefoldIndex) (shift : WuxingShift) :
    (Dart × Dart) × WuxingShift :=
  ((nativeC60GaugeDart frame v p,
    nativeC60GaugeDart frame v (rotation shift.1 p)), shift)

/-- Universal history obstruction: even phase displacement PLUS
event count cannot recover the order of the two real primitive
generation/control histories. No observation factoring through the
existing shift can be injective on these original typed paths. -/
theorem fivefoldGK5AFHistoryFactor_noFaithfulReturn
    (p : FivefoldIndex) {T : Type uT}
    (readout : WuxingShift → T) :
    ¬ Function.Injective
      (fun path : Quiver.Path p
        (generationPhase (generationPhase (generationPhase p))) =>
          readout (pathShift path)) := by
  intro hfaithful
  have hsame := congrArg readout (mixed_typed_paths_same_shift p)
  exact mixed_typed_paths_distinct p (hfaithful hsame)

/-- Even the PAIR of genuine whole pentagon NatIso values cannot
recover missing original free-path order when appended to the
physical C60 Dart pair, phase displacement and event count.
Both whole NatIso components are actual GK5AF terms; no higher
source Type-valued witness is replaced by an observation. -/
theorem fivefoldGK5AFPhysicalWholePhiHistory_obstruction
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (p : FivefoldIndex)
    {C D E F G : Slot → Cat.{vC,uC}}
    (e₁ : ∀ s : Slot, C s ≌ D s)
    (e₂ : ∀ s : Slot, D s ≌ E s)
    (e₃ : ∀ s : Slot, E s ≌ F s)
    (e₄ : ∀ s : Slot, F s ≌ G s)
    {i j : FivefoldIndex}
    (t : NativeGK5DTypedTree (fivefoldPhaseCategory frame v C) i j) :
    ¬ Function.Injective
      (fun path : Quiver.Path p
        (generationPhase (generationPhase (generationPhase p))) =>
        (fivefoldGK5AFPhysicalHistoryReadout frame v p (pathShift path),
         (nativeGK5AFLongPath
           (fivefoldPhaseEquivalence frame v e₁)
           (fivefoldPhaseEquivalence frame v e₂)
           (fivefoldPhaseEquivalence frame v e₃)
           (fivefoldPhaseEquivalence frame v e₄)
           (nativeGK5DTreeComposite t),
          nativeGK5AFShortPath
           (fivefoldPhaseEquivalence frame v e₁)
           (fivefoldPhaseEquivalence frame v e₂)
           (fivefoldPhaseEquivalence frame v e₃)
           (fivefoldPhaseEquivalence frame v e₄)
           (nativeGK5DTreeComposite t)))) := by
  exact fivefoldGK5AFHistoryFactor_noFaithfulReturn p
    (fun shift : WuxingShift =>
      (fivefoldGK5AFPhysicalHistoryReadout frame v p shift,
       (nativeGK5AFLongPath
         (fivefoldPhaseEquivalence frame v e₁)
         (fivefoldPhaseEquivalence frame v e₂)
         (fivefoldPhaseEquivalence frame v e₃)
         (fivefoldPhaseEquivalence frame v e₄)
         (nativeGK5DTreeComposite t),
        nativeGK5AFShortPath
         (fivefoldPhaseEquivalence frame v e₁)
         (fivefoldPhaseEquivalence frame v e₂)
         (fivefoldPhaseEquivalence frame v e₃)
         (fivefoldPhaseEquivalence frame v e₄)
         (nativeGK5DTreeComposite t))))

#print axioms fivefoldOriginalDart_phase_injective
#print axioms fivefoldGK5AFReversedPhysicalEndpoints
#print axioms fivefoldGK5AFNoForwardPhysicalComparison
#print axioms fivefoldGK5AFBothReverseObstructions
#print axioms fivefoldGK5AFHistoryFactor_noFaithfulReturn
#print axioms fivefoldGK5AFPhysicalWholePhiHistory_obstruction

end
end KUOS.Architecture.WuxingPentagonUnified
