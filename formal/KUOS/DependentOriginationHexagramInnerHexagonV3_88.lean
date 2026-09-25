import KUOS.DependentOriginationMiddleSwitchHexagramV3_87
import Mathlib

namespace KUOS.DependentOriginationHexagramInnerHexagonV3_88

open KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83
open KUOS.DependentOriginationMiddleSwitchHexagramV3_87

set_option autoImplicit false

noncomputable section

/-!
# Hexagram crossing pattern and recursive inner hexagon v3.88

v3.87 identifies the six middle-switch scalar terms as two exact three-term
families.  This file gives those two triples the combinatorics of an abstract
hexagram inside a six-tip boundary.

The six outer tips are placed cyclically as t0,...,t5.  The first triangle
uses the even tips t0,t2,t4 and the second uses the odd tips t1,t3,t5.  Their
six star edges have the usual combinatorial crossing pattern of a convex
hexagram.

Rather than importing Euclidean coordinates, the six crossings are recorded
as pairs of one edge from each triangle.  Consecutive crossings share one star
edge, producing a closed inner six-cycle.  This is the precise combinatorial
content needed for the recursive

hexagon -> hexagram -> inner hexagon

step.  Metric similarity and scale factors are intentionally not asserted.
-/

/-- Six outer tips of an abstract hexagram, in cyclic order. -/
inductive HexagramOuterTip
  | t0 | t1 | t2 | t3 | t4 | t5
  deriving DecidableEq, Repr, Fintype

@[simp] theorem hexagramOuterTip_card :
    Fintype.card HexagramOuterTip = 6 := by
  native_decide

/-- Place the b10 triangle on the even tips and the b11 triangle on the odd
tips.  The b11 ordering is reversed relative to b10, as expected for the two
interlaced triangles of a hexagram. -/
def hexagramOuterTipToAlgebraic :
    HexagramOuterTip → MiddleSwitchHexagramTip
  | .t0 => (.b10Triangle, .a00Transport)
  | .t1 => (.b11Triangle, .a00Transport)
  | .t2 => (.b10Triangle, .middleConnector)
  | .t3 => (.b11Triangle, .a10Transport)
  | .t4 => (.b10Triangle, .a10Transport)
  | .t5 => (.b11Triangle, .middleConnector)

/-- The six geometric tip labels and the six algebraic middle-switch tip labels
are in bijection. -/
theorem hexagramOuterTipToAlgebraic_bijective :
    Function.Bijective hexagramOuterTipToAlgebraic := by
  native_decide

/-- Canonical equivalence induced by the explicit six-tip placement. -/
noncomputable def hexagramOuterTipEquivAlgebraic :
    HexagramOuterTip ≃ MiddleSwitchHexagramTip :=
  Equiv.ofBijective
    hexagramOuterTipToAlgebraic
    hexagramOuterTipToAlgebraic_bijective

/-- Six sides belonging to the two interlaced triangles. -/
inductive HexagramStarEdge
  | up0
  | up1
  | up2
  | down0
  | down1
  | down2
  deriving DecidableEq, Repr, Fintype

@[simp] theorem hexagramStarEdge_card :
    Fintype.card HexagramStarEdge = 6 := by
  native_decide

/-- Outer tip endpoints of each star edge.

The up triangle is t0-t2-t4 and the down triangle is t1-t3-t5.
-/
def hexagramStarEdgeEndpoints :
    HexagramStarEdge → HexagramOuterTip × HexagramOuterTip
  | .up0 => (.t0, .t2)
  | .up1 => (.t2, .t4)
  | .up2 => (.t4, .t0)
  | .down0 => (.t1, .t3)
  | .down1 => (.t3, .t5)
  | .down2 => (.t5, .t1)

/-- Six crossings of the two triangular edge families.

The constructors are already arranged in the cyclic order of the inner
hexagon.
-/
inductive HexagramInnerVertex
  | x0 | x1 | x2 | x3 | x4 | x5
  deriving DecidableEq, Repr, Fintype

@[simp] theorem hexagramInnerVertex_card :
    Fintype.card HexagramInnerVertex = 6 := by
  native_decide

/-- Up-triangle edge passing through each inner crossing. -/
def hexagramInnerVertexUpEdge :
    HexagramInnerVertex → HexagramStarEdge
  | .x0 => .up0
  | .x1 => .up0
  | .x2 => .up1
  | .x3 => .up1
  | .x4 => .up2
  | .x5 => .up2

/-- Down-triangle edge passing through each inner crossing. -/
def hexagramInnerVertexDownEdge :
    HexagramInnerVertex → HexagramStarEdge
  | .x0 => .down2
  | .x1 => .down0
  | .x2 => .down0
  | .x3 => .down1
  | .x4 => .down1
  | .x5 => .down2

/-- Cyclic successor on the six crossings. -/
def hexagramInnerVertexNext :
    HexagramInnerVertex → HexagramInnerVertex
  | .x0 => .x1
  | .x1 => .x2
  | .x2 => .x3
  | .x3 => .x4
  | .x4 => .x5
  | .x5 => .x0

/-- The star edge shared by one inner crossing and its successor. -/
def hexagramInnerSharedEdgeToNext :
    HexagramInnerVertex → HexagramStarEdge
  | .x0 => .up0
  | .x1 => .down0
  | .x2 => .up1
  | .x3 => .down1
  | .x4 => .up2
  | .x5 => .down2

/-- Incidence of a crossing with one of its two star edges. -/
def hexagramInnerIncident
    (x : HexagramInnerVertex)
    (e : HexagramStarEdge) : Prop :=
  e = hexagramInnerVertexUpEdge x ∨
    e = hexagramInnerVertexDownEdge x

/-- The designated shared edge is incident to the current crossing. -/
theorem hexagramInnerSharedEdge_incident_current
    (x : HexagramInnerVertex) :
    hexagramInnerIncident x
      (hexagramInnerSharedEdgeToNext x) := by
  cases x <;>
    simp [hexagramInnerIncident,
      hexagramInnerSharedEdgeToNext,
      hexagramInnerVertexUpEdge,
      hexagramInnerVertexDownEdge]

/-- The designated shared edge is also incident to the next crossing. -/
theorem hexagramInnerSharedEdge_incident_next
    (x : HexagramInnerVertex) :
    hexagramInnerIncident (hexagramInnerVertexNext x)
      (hexagramInnerSharedEdgeToNext x) := by
  cases x <;>
    simp [hexagramInnerIncident,
      hexagramInnerSharedEdgeToNext,
      hexagramInnerVertexNext,
      hexagramInnerVertexUpEdge,
      hexagramInnerVertexDownEdge]

/-- Ordered inner-hexagon boundary vertices. -/
def hexagramInnerBoundary : List HexagramInnerVertex :=
  [.x0, .x1, .x2, .x3, .x4, .x5]

@[simp] theorem hexagramInnerBoundary_length :
    hexagramInnerBoundary.length = 6 := by
  rfl

/-- The final inner vertex closes back to the first. -/
@[simp] theorem hexagramInnerBoundary_closes :
    hexagramInnerVertexNext .x5 = .x0 := by
  rfl

/-- The inner cell produced by the crossing pattern is again hexagonal at the
level of face kind. -/
def hexagramInnerFaceKind : TruncatedIcosahedralFaceKind :=
  .hexagon

@[simp] theorem hexagramInnerFaceKind_sides :
    truncatedIcosahedralFaceSides hexagramInnerFaceKind = 6 := by
  rfl

/-- The recursive inner hexagon has the same six-fold arity as the outer
hexagram refinement profile. -/
theorem hexagramInnerBoundary_matches_refinement :
    hexagramInnerBoundary.length =
      hexagramRefinement.sectors := by
  rfl

/-!
## Boundary after v3.88

The hexagram interpretation now has explicit incidence:

* six cyclic outer tips;
* two interlaced three-tip triangles;
* six star edges;
* six declared crossing pairs;
* a closed inner six-cycle whose consecutive vertices share alternating
  up/down star edges.

The algebraic six tips from v3.87 are bijective with the outer hexagram tips.
Thus the middle-switch 3 + 3 decomposition has a concrete combinatorial
hexagram carrier, and the star crossing pattern regenerates an inner hexagon.

The next theorem unit should lift the scalar values through the six-tip
equivalence and compare one recursive refinement step with the v3.86
truncated-icosahedral hexagonal face.  Only after that comparison is proved
should recursive refinement be iterated.
-/

end

end KUOS.DependentOriginationHexagramInnerHexagonV3_88
