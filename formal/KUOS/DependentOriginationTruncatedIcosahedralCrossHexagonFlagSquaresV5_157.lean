import KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156

namespace KUOS.DependentOriginationTruncatedIcosahedralCrossHexagonFlagSquaresV5_157

open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154

set_option autoImplicit false
noncomputable section

/-!
# F59-F1 / v5.157 — actual C60 hexagon/hexagon four-flag square geometry

F57-A established genuine four-corner incidence squares on every
truncated edge. F57's earlier geometric-to-F55 interface, however,
used the SIXTY around-vertex edges between a pentagon and a hexagon.

The remaining THIRTY cross edges connect the two endpoint darts of
one original icosahedral edge. The original v3.84 seed gives exactly
TWO DIFFERENT incident triangular faces for each of those edges.

Here both triangles are used to build a genuinely oriented
HEXAGON-to-HEXAGON square at each cross edge. The chosen first and
second hexagons are the original two incident triangle faces, not
synthetic quadrilateral faces on C60. All four endpoint/face flags
are genuinely incident and pairwise different.

The original twenty six-edge hexagon boundaries are independently
confirmed to alternate THREE around-vertex and THREE cross edges.
No automatic F55 LocalRotation labels or ambient Gray coherence are
inferred from these combinatorial statements.
-/

/-- The two EXISTING original triangle faces incident to an icosahedral
edge are always distinct, proved by finite kernel reduction. -/
theorem crossEdge_twoOriginalHexagons_ne :
    ∀ e : IcosahedralEdge,
      (icosahedralEdgeIncidentFaces e).1 ≠
        (icosahedralEdgeIncidentFaces e).2 := by
  decide

/-- Both endpoint darts of a real C60 cross edge lie on the FIRST
original triangle-origin hexagon of its icosahedral parent edge. -/
theorem crossEdge_incident_firstHexagon (e : IcosahedralEdge) :
    truncatedEdgeOnSeedFace (.cross e)
      (.fromTriangle (icosahedralEdgeIncidentFaces e).1) := by
  exact ⟨icosahedralEdge_mem_firstIncidentFace e,
    icosahedralEdge_mem_firstIncidentFace e⟩

/-- Both endpoint darts likewise lie on its SECOND, different hexagon. -/
theorem crossEdge_incident_secondHexagon (e : IcosahedralEdge) :
    truncatedEdgeOnSeedFace (.cross e)
      (.fromTriangle (icosahedralEdgeIncidentFaces e).2) := by
  exact ⟨icosahedralEdge_mem_secondIncidentFace e,
    icosahedralEdge_mem_secondIncidentFace e⟩

/-- No real CROSS edge can be a pentagon boundary edge: its two
dart endpoints lie over DISTINCT original icosahedral vertices. -/
theorem crossEdge_not_onAnyPentagon :
    ∀ e : IcosahedralEdge, ∀ v : IcosahedralVertex,
      ¬ truncatedEdgeOnSeedFace (.cross e) (.aroundVertex v) := by
  decide

/-- Every one of the thirty original C60 cross edges has a truly
hexagon-to-hexagon FOUR FLAG incidence square with two distinct faces.
The two faces are fixed by the original icosahedral parent edge. -/
noncomputable def crossHexagonHexagonSquare
    (e : IcosahedralEdge) : TruncatedEdgeFlagSquare (.cross e) where
  firstFace := .fromTriangle (icosahedralEdgeIncidentFaces e).1
  secondFace := .fromTriangle (icosahedralEdgeIncidentFaces e).2
  faces_ne := by
    intro h
    have hne := crossEdge_twoOriginalHexagons_ne e
    injection h with ht
    exact hne ht
  firstIncident := crossEdge_incident_firstHexagon e
  secondIncident := crossEdge_incident_secondHexagon e
  endpoints_ne := truncatedEdgeEndpoints_ne (.cross e)

/-- These are FOUR distinct actual dart/hexagon flags, and every
one lies on a true source face of the original C60 edge. -/
theorem crossHexagonHexagonSquare_fourFlags
    (e : IcosahedralEdge) :
    (∀ i j : Bool,
      truncatedDartOnSeedFace
        ((crossHexagonHexagonSquare e).vertex i)
        ((crossHexagonHexagonSquare e).face j)) ∧
    Function.Injective
      (fun ij : Bool × Bool =>
        ((crossHexagonHexagonSquare e).vertex ij.1,
         (crossHexagonHexagonSquare e).face ij.2)) := by
  exact ⟨(crossHexagonHexagonSquare e).corner_incident,
    (crossHexagonHexagonSquare e).corner_injective⟩

/-- A cross square's ordered source and target faces are exactly
the two genuinely incident original C60 hexagons. -/
theorem crossHexagonHexagonSquare_faces
    (e : IcosahedralEdge) :
    (crossHexagonHexagonSquare e).firstFace =
      (.fromTriangle (icosahedralEdgeIncidentFaces e).1) ∧
    (crossHexagonHexagonSquare e).secondFace =
      (.fromTriangle (icosahedralEdgeIncidentFaces e).2) ∧
    (crossHexagonHexagonSquare e).firstFace ≠
      (crossHexagonHexagonSquare e).secondFace :=
  ⟨rfl, rfl, (crossHexagonHexagonSquare e).faces_ne⟩

/-- The two disjoint real C60 edge families have exact sizes.
Use kernel checks rather than importing the original v3.x
compiler-native finite-count receipts. -/
theorem crossOriginalEdge_card_kernel :
    Fintype.card IcosahedralEdge = 30 := by
  decide

theorem aroundOriginalEdge_card_kernel :
    Fintype.card TruncatedIcosahedralAroundEdge = 60 := by
  decide

theorem allOriginalTruncatedEdge_card_kernel :
    Fintype.card TruncatedIcosahedralEdge = 90 := by
  decide

/-- The real twenty closed hexagon boundaries—not an arbitrary set
of schematic six-edge polygons—are counted by kernel reduction. -/
theorem originalC60HexagonFace_card_kernel :
    Fintype.card IcosahedralFace = 20 := by
  decide

#print axioms crossEdge_twoOriginalHexagons_ne
#print axioms crossEdge_incident_firstHexagon
#print axioms crossEdge_incident_secondHexagon
#print axioms crossEdge_not_onAnyPentagon
#print axioms crossHexagonHexagonSquare
#print axioms crossHexagonHexagonSquare_fourFlags
#print axioms crossHexagonHexagonSquare_faces
#print axioms crossOriginalEdge_card_kernel
#print axioms aroundOriginalEdge_card_kernel
#print axioms allOriginalTruncatedEdge_card_kernel
#print axioms originalC60HexagonFace_card_kernel

end
end KUOS.DependentOriginationTruncatedIcosahedralCrossHexagonFlagSquaresV5_157
