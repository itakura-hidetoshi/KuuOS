import Kuu.F112.PolygonNativeC60NorthPhaseSectorEquiv
import Mathlib.Tactic

/-!
# Genuine C60 five phases select the ORIGINAL north polygon darts and edges

The already verified \`FivePhase ≃ north-C60 PolygonBoundarySector\`
is sharpened from a finite-carrier correspondence to source-exact
original C60 incidence geometry. Each of its five images selects
the old polygon boundary DART and EDGE of the same original north
pentagon, not a K5 quiver edge or an artificially introduced face.

This does not equate Qi phase changes with physical gauge coboundaries
or noncommutative K5 higher-cell changes. No global descent is asserted.
-/

namespace Kuu.F112.Physical

open KUOS.Architecture
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- At each of the five actual C60 north slots, the F45 physical-sector
coordinate selects precisely the existing original polygon-boundary dart. -/
theorem northK5OriginalDartOfSlot (s : Slot) :
    cyclicBoundaryDart (.pentagon .north) (northK5SectorOfSlot s).1.val =
      incidentDart .north s := by
  cases s <;> decide

/-- The same original physical sector denotes the corresponding genuine
C60 around-edge, not a graph proxy. -/
theorem northK5OriginalEdgeOfSlot (s : Slot) :
    (polygonBoundaryEdges (.pentagon .north)).getD
      (northK5SectorOfSlot s).1.val (.around ⟨.north, .s0⟩) =
        .around ⟨.north, s⟩ := by
  cases s <;> decide

/-- Under ANY chosen Qi chart frame, phase p's actual source index is
the ORIGINAL north C60 incidence dart, not merely a formal ZMod5 label. -/
theorem northK5OriginalDartOfPhase
    (frame : NativeC60FivePhaseGauge) (phase : FivePhase) :
    cyclicBoundaryDart (.pentagon .north)
      (northK5PhaseSectorEquiv frame phase).1.val =
        nativeC60GaugeDart frame .north phase := by
  change cyclicBoundaryDart (.pentagon .north)
    (northK5SectorOfSlot (nativeC60GaugeSlot frame .north phase)).1.val =
      incidentDart .north (nativeC60GaugeSlot frame .north phase)
  exact northK5OriginalDartOfSlot _

/-- The same Qi chart selects the existing ORIGINAL physical C60 edge.
The old incidence endpoints and cyclic order remain source-owned. -/
theorem northK5OriginalEdgeOfPhase
    (frame : NativeC60FivePhaseGauge) (phase : FivePhase) :
    (polygonBoundaryEdges (.pentagon .north)).getD
      (northK5PhaseSectorEquiv frame phase).1.val
      (.around ⟨.north, .s0⟩) =
        .around ⟨.north, nativeC60GaugeSlot frame .north phase⟩ := by
  change (polygonBoundaryEdges (.pentagon .north)).getD
    (northK5SectorOfSlot (nativeC60GaugeSlot frame .north phase)).1.val
    (.around ⟨.north, .s0⟩) =
      .around ⟨.north, nativeC60GaugeSlot frame .north phase⟩
  exact northK5OriginalEdgeOfSlot _

#print axioms northK5OriginalDartOfSlot
#print axioms northK5OriginalEdgeOfSlot
#print axioms northK5OriginalDartOfPhase
#print axioms northK5OriginalEdgeOfPhase

end
end Kuu.F112.Physical
