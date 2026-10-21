import KuuOSFormal.HistoricalF36F40BridgeP50

/-!
# F112-P51 — all genuinely oriented original C60 hexagon sources

The remaining original F42->independent-F69 premise after P50 is the
old F41 genuine 20-hexagon boundary PATH, not merely a numerical six
or the independent polygonRawLoop.

Here each genuinely typed old quiver arrow is inspected via its TRUE
unoriented physical edge code, and its membership in a real polygon
is interpreted through the original/independent incidence equivalence.

P48 has established the oriented original hexagon 6-edge list agrees
exactly with the separately kernel-certified 6-edge list, including
reversed edges. P49 proves support of old paths is stable under
composition; P50 gives localization of any genuine supported old loop.

We preserve this full old source and never construct artificial face
2-cells or import Gray into the independent Kuu core.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry
namespace ActualF47

open CategoryTheory
open Kuu.F112.Physical
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60AllThirtyTwoFaceCycleV5_158

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- The actual physical edge sequence of any genuine old C60 free
Quiver.Path: unlike \`Quiver.Path.toList\`, this tracks arrow *codes*
and keeps multiple arrows between the same two physical darts. -/
def p51_oldPathPhysicalEdges {a b : IcosahedralDart}
    (p : Quiver.Path a b) : List TruncatedIcosahedralEdge :=
  match p with
  | .nil => []
  | .cons prior f =>
      p51_oldPathPhysicalEdges prior ++ [f.1.edge]

/-- Exact edge-word concatenation, independent of any representative
or equality of vertices in the genuine 60-object old quiver. -/
theorem p51_oldPathPhysicalEdges_comp
    {a b c : IcosahedralDart}
    (p : Quiver.Path a b) (q : Quiver.Path b c) :
    p51_oldPathPhysicalEdges (p.comp q) =
      p51_oldPathPhysicalEdges p ++ p51_oldPathPhysicalEdges q := by
  induction q with
  | nil => simp [p51_oldPathPhysicalEdges]
  | cons q f ih =>
      rw [Quiver.Path.comp_cons]
      simp only [p51_oldPathPhysicalEdges, ih, List.append_assoc]

/-- A single genuine old F41 oriented edge keeps its underlying
physical edge code exactly, including on reversed arrows. -/
theorem p51_oriented_single_edge_word
    (oe : OrientedTruncatedIcosahedralEdge) :
    p51_oldPathPhysicalEdges (c60F41OrientedPath oe) = [oe.edge] := by
  cases oe with
  | forward old =>
      change p51_oldPathPhysicalEdges
        ((c60F41ForwardArrow old).toPath) = [old]
      simp [p51_oldPathPhysicalEdges, Quiver.Hom.toPath]
  | reverse old =>
      change p51_oldPathPhysicalEdges
        ((c60F41ReverseArrow old).toPath) = [old]
      simp [p51_oldPathPhysicalEdges, Quiver.Hom.toPath]

/-- The P48 Boolean source-path incidence predicate equals the
all-edges-on-face finite Boolean check, for EVERY historical source
Quiver.Path and its true old physical edge word. -/
theorem p51_oldPathWithinPolygon_eq_all :
    ∀ {a b : IcosahedralDart} (p : Quiver.Path a b)
      (face : Polygon),
      p48_originalPathWithinPolygon face p =
        (p51_oldPathPhysicalEdges p).all
          (fun old => decide (edgeOnFace (edgeEquiv.symm old) face)) := by
  intro a b p
  induction p with
  | nil =>
      intro face
      simp [p48_originalPathWithinPolygon, p51_oldPathPhysicalEdges]
  | cons p f ih =>
      intro face
      simp only [p48_originalPathWithinPolygon, p51_oldPathPhysicalEdges,
        List.all_append, List.all_cons, List.all_nil, Bool.and_true,
        p48_originalArrowNativeEdge, ih] <;> rfl

/-- Each actual historical oriented hexagon side is on the very
original C60 physical hexagon, regardless of traversal direction.
The original Type-valued oriented generator remains unmodified. -/
theorem p51_actual_hexagon_oriented_step_support
    (t : IcosahedralFace) (oe : OrientedTruncatedIcosahedralEdge)
    (h : oe ∈ (truncatedIcosahedralHexagonCycle t).edges) :
    p48_originalPathWithinPolygon
      (polygonEquiv.symm (.fromTriangle t))
      (c60F41OrientedPath oe) = true := by
  rw [p51_oldPathWithinPolygon_eq_all,
    p51_oriented_single_edge_word]
  cases oe with
  | forward old =>
      simpa [OrientedTruncatedIcosahedralEdge.edge] using
        (decide_eq_true
          (p48_allOriginalHexagonOrientedEdges_incident t (.forward old) h))
  | reverse old =>
      simpa [OrientedTruncatedIcosahedralEdge.edge] using
        (decide_eq_true
          (p48_allOriginalHexagonOrientedEdges_incident t (.reverse old) h))

/-- Every original C60 hexagon's complete ORDERED SIX edge codes
are genuine edge-on-polygon incidences. This uses actual P48 geometry,
not a replacement generated face word or numerical proxy. -/
theorem p51_all_six_original_hexagon_edges_supported
    (t : IcosahedralFace) :
    ((truncatedIcosahedralHexagonCycle t).edges.map
        OrientedTruncatedIcosahedralEdge.edge).all
          (fun old =>
            decide (edgeOnFace (edgeEquiv.symm old)
              (polygonEquiv.symm (.fromTriangle t)))) = true := by
  rw [List.all_eq_true]
  intro e he
  obtain ⟨oe, hoe, hcode⟩ := List.mem_map.mp he
  subst e
  exact decide_eq_true
    (p48_allOriginalHexagonOrientedEdges_incident t oe hoe)

/-- A finite original hexagonal source path is F69-face-supported
as soon as its certified true old 6-edge word agrees with the true
oriented F41 geometric hexagon word. This separates the remaining
source-path computation issue from the already proved geometry. -/
theorem p51_original_hexagon_support_of_exact_edge_word
    (t : IcosahedralFace)
    (hword :
      p51_oldPathPhysicalEdges (c60F41HexagonBoundaryLoop t) =
        (truncatedIcosahedralHexagonCycle t).edges.map
          OrientedTruncatedIcosahedralEdge.edge) :
    p48_originalPathWithinPolygon
      (polygonEquiv.symm (.fromTriangle t))
      (c60F41HexagonBoundaryLoop t) = true := by
  rw [p51_oldPathWithinPolygon_eq_all, hword]
  exact p51_all_six_original_hexagon_edges_supported t

#print axioms p51_oldPathPhysicalEdges
#print axioms p51_oldPathPhysicalEdges_comp
#print axioms p51_oriented_single_edge_word
#print axioms p51_oldPathWithinPolygon_eq_all
#print axioms p51_actual_hexagon_oriented_step_support
#print axioms p51_all_six_original_hexagon_edges_supported
#print axioms p51_original_hexagon_support_of_exact_edge_word

end
end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
