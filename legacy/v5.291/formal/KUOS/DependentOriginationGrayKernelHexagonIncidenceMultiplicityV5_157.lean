import KUOS.DependentOriginationGrayKernelHexagonSixCellPastingV5_157

namespace KUOS.DependentOriginationGrayKernelHexagonIncidenceMultiplicityV5_157

open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationTruncatedIcosahedralKernelHexagonCyclesV5_157
open KUOS.DependentOriginationTruncatedIcosahedralCrossHexagonFlagSquaresV5_157

set_option autoImplicit false
noncomputable section

/-!
# F59-F5 / v5.157 — actual edge-by-edge C60 hexagon boundary multiplicities

F59-F3 constructed NEW kernel-clean oriented six-edge hexagons at all
twenty original triangle faces. F59-F4 constructed native higher-cell
pastes of all six original F55 square labels for each hexagon.

Here we prove the stronger combinatorial incidence fact, directly
on the ORIGINAL C60 edge/hexagon carriers, not on integer charges:
each original around/pentagon-hexagon edge occurs in EXACTLY ONE of
the twenty hexagonal boundary lists, while each original cross/
hexagon-hexagon edge occurs in EXACTLY TWO such lists.

Consequently the entire hexagon-boundary multiset counts all sixty
around edges once and all thirty cross edges twice: 60+2*30=120
literal edge occurrences in the original finite geometric carrier.

The proofs use finite kernel reduction of explicit edge faces, cycle
orientation and five-slot conversion constructed in F59-F3. In
particular this is NOT deduced from F59-F4's integer generator-charge
equality, which by itself cannot force individual incidence counts.

No assumption that source F55 paths paste globally or that a
historic Stage-II obstruction equals any new exchange phase.
-/

/-- The REAL unoriented six-edge boundary of a given original C60
hexagon, obtained by forgetting orientation of its new trusted cycle. -/
def kernelC60HexagonBoundaryEdges
    (face : IcosahedralFace) : List TruncatedIcosahedralEdge :=
  (kernelCertifiedHexagonCycle face).edges.map
    OrientedTruncatedIcosahedralEdge.edge

theorem kernelC60HexagonBoundaryEdges_length
    (face : IcosahedralFace) :
    (kernelC60HexagonBoundaryEdges face).length = 6 := by
  rfl

/-- Number of occurrences of a SPECIFIC genuine C60 edge among
ALL TWENTY real hexagonal boundary lists. This is geometric
multiplicity, not an additive representation of a higher cell. -/
def kernelC60HexagonEdgeMultiplicity
    (edge : TruncatedIcosahedralEdge) : Nat :=
  ∑ face : IcosahedralFace,
    (kernelC60HexagonBoundaryEdges face).count edge

/-- Each of the original SIXTY pentagon-to-hexagon around edges
occurs exactly ONCE as an unoriented hexagon boundary edge. -/
theorem kernelC60AroundEdge_hexagonMultiplicity :
    ∀ edge : TruncatedIcosahedralAroundEdge,
      kernelC60HexagonEdgeMultiplicity (.around edge) = 1 := by
  decide

/-- Each of the original THIRTY hexagon-to-hexagon cross edges
is shared by exactly TWO different hexagonal boundary cycles.
No double counting is assumed: it is checked against all twenty
actual original triangle faces and the six physical edges each. -/
theorem kernelC60CrossEdge_hexagonMultiplicity :
    ∀ edge : IcosahedralEdge,
      kernelC60HexagonEdgeMultiplicity (.cross edge) = 2 := by
  decide

/-- Full *edgewise* incidence law. This accounts for exactly the
120 hexagon boundary edge occurrences identified separately by
native F59-F4 higher-cell aggregation. -/
theorem kernelC60EveryEdge_exactHexagonMultiplicity
    (edge : TruncatedIcosahedralEdge) :
    kernelC60HexagonEdgeMultiplicity edge =
      match edge with
      | .around _ => 1
      | .cross _ => 2 := by
  cases edge with
  | around a => exact kernelC60AroundEdge_hexagonMultiplicity a
  | cross e => exact kernelC60CrossEdge_hexagonMultiplicity e

/-- Every original hexagon boundary has six physical edge
occurrences; summing the lengths over all twenty hexagons gives 120. -/
theorem kernelC60AllHexagonBoundaryEdgeOccurrences :
    (∑ face : IcosahedralFace,
      (kernelC60HexagonBoundaryEdges face).length) = 120 := by
  simp only [kernelC60HexagonBoundaryEdges_length]
  simp only [Finset.sum_const, Finset.card_univ,
    kernelCertifiedHexagonCycle_twenty]
  decide

#print axioms kernelC60HexagonBoundaryEdges_length
#print axioms kernelC60HexagonEdgeMultiplicity
#print axioms kernelC60AroundEdge_hexagonMultiplicity
#print axioms kernelC60CrossEdge_hexagonMultiplicity
#print axioms kernelC60EveryEdge_exactHexagonMultiplicity
#print axioms kernelC60AllHexagonBoundaryEdgeOccurrences

end
end KUOS.DependentOriginationGrayKernelHexagonIncidenceMultiplicityV5_157
