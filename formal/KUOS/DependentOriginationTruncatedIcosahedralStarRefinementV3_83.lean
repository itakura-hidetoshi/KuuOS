import KUOS.DependentOriginationMiddleSwitchSixTermExpansionV3_82
import Mathlib

namespace KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83

set_option autoImplicit false

/-!
# Truncated-icosahedral star-refinement profile v3.83

v3.82 closes the scalar-aligned M1 residual into a six-term expression.  The
present file begins the polyhedral stage without identifying that expression
prematurely with a cyclic hexagon boundary.

The first carrier datum is the combinatorial profile of the truncated
icosahedron:

* 60 vertices;
* 90 edges;
* 12 pentagonal faces;
* 20 hexagonal faces;
* local vertex figure 5.6.6.

The barycentric face-poset carrier therefore has 60 + 90 + 32 = 182 cells and
360 maximal vertex-edge-face flags.

The pentagonal and hexagonal faces are also equipped with a deliberately
minimal recursive star-refinement profile:

* pentagram refinement: five triangular sectors plus an inner pentagon;
* hexagram refinement: six triangular sectors plus an inner hexagon.

Only the combinatorial self-similarity is recorded here.  No Euclidean scale
factor, golden-ratio metric statement, or geometric realization is assumed.

The six sectors of the hexagram profile have the same arity as the six terms
proved in v3.82.  This file records that arity match only; it does not yet
identify the six v3.82 scalar terms with the boundary of a cyclic hexagonal
coherence cell.  That incidence theorem is a later obligation.
-/

/-- The two face types of the truncated icosahedron. -/
inductive TruncatedIcosahedralFaceKind
  | pentagon
  | hexagon
  deriving DecidableEq, Repr, Fintype

/-- Number of boundary sides of each face type. -/
def truncatedIcosahedralFaceSides :
    TruncatedIcosahedralFaceKind → Nat
  | .pentagon => 5
  | .hexagon => 6

/-- Number of faces of each type. -/
def truncatedIcosahedralFaceMultiplicity :
    TruncatedIcosahedralFaceKind → Nat
  | .pentagon => 12
  | .hexagon => 20

/-- Global combinatorial counts. -/
def truncatedIcosahedralVertexCount : Nat := 60
def truncatedIcosahedralEdgeCount : Nat := 90
def truncatedIcosahedralFaceCount : Nat := 32

@[simp] theorem truncatedIcosahedralFaceSides_pentagon :
    truncatedIcosahedralFaceSides .pentagon = 5 := rfl

@[simp] theorem truncatedIcosahedralFaceSides_hexagon :
    truncatedIcosahedralFaceSides .hexagon = 6 := rfl

@[simp] theorem truncatedIcosahedralFaceMultiplicity_pentagon :
    truncatedIcosahedralFaceMultiplicity .pentagon = 12 := rfl

@[simp] theorem truncatedIcosahedralFaceMultiplicity_hexagon :
    truncatedIcosahedralFaceMultiplicity .hexagon = 20 := rfl

/-- The 12 pentagons and 20 hexagons account for all 32 faces. -/
theorem truncatedIcosahedral_face_partition :
    truncatedIcosahedralFaceMultiplicity .pentagon +
        truncatedIcosahedralFaceMultiplicity .hexagon =
      truncatedIcosahedralFaceCount := by
  norm_num [truncatedIcosahedralFaceMultiplicity,
    truncatedIcosahedralFaceCount]

/-- Euler's relation, written subtraction-free over Nat. -/
theorem truncatedIcosahedral_euler_relation :
    truncatedIcosahedralVertexCount + truncatedIcosahedralFaceCount =
      truncatedIcosahedralEdgeCount + 2 := by
  norm_num [truncatedIcosahedralVertexCount,
    truncatedIcosahedralEdgeCount, truncatedIcosahedralFaceCount]

/-- Counting face-edge incidences gives twice the edge count. -/
theorem truncatedIcosahedral_face_edge_incidence :
    truncatedIcosahedralFaceMultiplicity .pentagon *
          truncatedIcosahedralFaceSides .pentagon +
        truncatedIcosahedralFaceMultiplicity .hexagon *
          truncatedIcosahedralFaceSides .hexagon =
      2 * truncatedIcosahedralEdgeCount := by
  norm_num [truncatedIcosahedralFaceMultiplicity,
    truncatedIcosahedralFaceSides, truncatedIcosahedralEdgeCount]

/-- Every vertex lies on exactly one pentagon at the level of incidence
counts: 12 * 5 = 60. -/
theorem truncatedIcosahedral_pentagon_vertex_incidence :
    truncatedIcosahedralFaceMultiplicity .pentagon *
        truncatedIcosahedralFaceSides .pentagon =
      truncatedIcosahedralVertexCount := by
  norm_num [truncatedIcosahedralFaceMultiplicity,
    truncatedIcosahedralFaceSides, truncatedIcosahedralVertexCount]

/-- Every vertex lies on exactly two hexagons at the level of incidence
counts: 20 * 6 = 2 * 60. -/
theorem truncatedIcosahedral_hexagon_vertex_incidence :
    truncatedIcosahedralFaceMultiplicity .hexagon *
        truncatedIcosahedralFaceSides .hexagon =
      2 * truncatedIcosahedralVertexCount := by
  norm_num [truncatedIcosahedralFaceMultiplicity,
    truncatedIcosahedralFaceSides, truncatedIcosahedralVertexCount]

/-- Number of cells in the rank-three face-poset profile:
vertices + edges + faces. -/
def truncatedIcosahedralBarycentricObjectCount : Nat :=
  truncatedIcosahedralVertexCount +
    truncatedIcosahedralEdgeCount +
    truncatedIcosahedralFaceCount

@[simp] theorem truncatedIcosahedralBarycentricObjectCount_eq :
    truncatedIcosahedralBarycentricObjectCount = 182 := by
  norm_num [truncatedIcosahedralBarycentricObjectCount,
    truncatedIcosahedralVertexCount, truncatedIcosahedralEdgeCount,
    truncatedIcosahedralFaceCount]

/-- A maximal barycentric flag is vertex < edge < face.  Each n-gonal face
contributes 2n such flags. -/
def truncatedIcosahedralMaximalFlagCount : Nat :=
  truncatedIcosahedralFaceMultiplicity .pentagon *
      (2 * truncatedIcosahedralFaceSides .pentagon) +
    truncatedIcosahedralFaceMultiplicity .hexagon *
      (2 * truncatedIcosahedralFaceSides .hexagon)

@[simp] theorem truncatedIcosahedralMaximalFlagCount_eq :
    truncatedIcosahedralMaximalFlagCount = 360 := by
  norm_num [truncatedIcosahedralMaximalFlagCount,
    truncatedIcosahedralFaceMultiplicity, truncatedIcosahedralFaceSides]

/-- The same 360 maximal flags are obtained as four flags per edge:
two endpoints times two incident faces. -/
theorem truncatedIcosahedralMaximalFlagCount_eq_four_mul_edges :
    truncatedIcosahedralMaximalFlagCount =
      4 * truncatedIcosahedralEdgeCount := by
  norm_num [truncatedIcosahedralMaximalFlagCount,
    truncatedIcosahedralFaceMultiplicity, truncatedIcosahedralFaceSides,
    truncatedIcosahedralEdgeCount]

/-- Combinatorial star refinement of one polygonal face.

sectors records the outer triangular sectors visible after drawing the star;
inner records the central face type.  The two proof fields isolate exactly the
self-similar information needed later: the sector count equals the outer
arity and the central face has the same kind as the outer face.
-/
structure StarRefinementProfile where
  outer : TruncatedIcosahedralFaceKind
  sectors : Nat
  inner : TruncatedIcosahedralFaceKind
  sectors_eq_sides :
    sectors = truncatedIcosahedralFaceSides outer
  inner_eq_outer : inner = outer

/-- Pentagon with an inscribed pentagram: five sectors and an inner pentagon. -/
def pentagramRefinement : StarRefinementProfile where
  outer := .pentagon
  sectors := 5
  inner := .pentagon
  sectors_eq_sides := rfl
  inner_eq_outer := rfl

/-- Hexagon with an inscribed hexagram: six sectors and an inner hexagon. -/
def hexagramRefinement : StarRefinementProfile where
  outer := .hexagon
  sectors := 6
  inner := .hexagon
  sectors_eq_sides := rfl
  inner_eq_outer := rfl

@[simp] theorem pentagramRefinement_sectors :
    pentagramRefinement.sectors = 5 := rfl

@[simp] theorem pentagramRefinement_inner :
    pentagramRefinement.inner = .pentagon := rfl

@[simp] theorem hexagramRefinement_sectors :
    hexagramRefinement.sectors = 6 := rfl

@[simp] theorem hexagramRefinement_inner :
    hexagramRefinement.inner = .hexagon := rfl

/-- Number of triangular sectors accumulated after repeatedly refining only the
central same-kind face for depth layers.  Metric scale is intentionally not
part of this datum. -/
def starRefinementTriangleCount
    (P : StarRefinementProfile) (depth : Nat) : Nat :=
  depth * P.sectors

@[simp] theorem starRefinementTriangleCount_zero
    (P : StarRefinementProfile) :
    starRefinementTriangleCount P 0 = 0 := by
  simp [starRefinementTriangleCount]

@[simp] theorem starRefinementTriangleCount_succ
    (P : StarRefinementProfile) (depth : Nat) :
    starRefinementTriangleCount P (Nat.succ depth) =
      starRefinementTriangleCount P depth + P.sectors := by
  simp [starRefinementTriangleCount, Nat.succ_mul]

@[simp] theorem pentagramRefinement_triangleCount
    (depth : Nat) :
    starRefinementTriangleCount pentagramRefinement depth =
      depth * 5 := rfl

@[simp] theorem hexagramRefinement_triangleCount
    (depth : Nat) :
    starRefinementTriangleCount hexagramRefinement depth =
      depth * 6 := rfl

/-- The three local face slots at every truncated-icosahedral vertex. -/
inductive TruncatedIcosahedralVertexSlot
  | pentagonal
  | hexagonalLeft
  | hexagonalRight
  deriving DecidableEq, Repr, Fintype

/-- The 5.6.6 vertex figure as face kinds. -/
def truncatedIcosahedralLocalFaceKind :
    TruncatedIcosahedralVertexSlot → TruncatedIcosahedralFaceKind
  | .pentagonal => .pentagon
  | .hexagonalLeft => .hexagon
  | .hexagonalRight => .hexagon

/-- Each local face slot carries its natural star refinement. -/
def truncatedIcosahedralLocalStarRefinement :
    TruncatedIcosahedralVertexSlot → StarRefinementProfile
  | .pentagonal => pentagramRefinement
  | .hexagonalLeft => hexagramRefinement
  | .hexagonalRight => hexagramRefinement

/-- Star refinement preserves the local 5.6.6 face kind. -/
theorem truncatedIcosahedralLocalStarRefinement_inner_same
    (s : TruncatedIcosahedralVertexSlot) :
    (truncatedIcosahedralLocalStarRefinement s).inner =
      truncatedIcosahedralLocalFaceKind s := by
  cases s <;> rfl

/-- The number of star sectors is exactly the arity of the corresponding local
5.6.6 face. -/
theorem truncatedIcosahedralLocalStarRefinement_sector_arity
    (s : TruncatedIcosahedralVertexSlot) :
    (truncatedIcosahedralLocalStarRefinement s).sectors =
      truncatedIcosahedralFaceSides
        (truncatedIcosahedralLocalFaceKind s) := by
  cases s <;> rfl

/-- Arity of the closed scalar expression obtained in v3.82.  This is a
bookkeeping constant, not yet a geometric incidence theorem. -/
def middleSwitchSixTermArity : Nat := 6

/-- The hexagram refinement has the same arity as the v3.82 six-term
middle-switch expression.

This theorem intentionally asserts only equality of natural numbers.  The
later carrier theorem must still prove a cyclic ordering and incidence map
before the six scalar terms may be called a hexagonal boundary.
-/
theorem hexagramRefinement_matches_middleSwitchSixTerm_arity :
    hexagramRefinement.sectors = middleSwitchSixTermArity := by
  rfl

/-!
## Boundary after v3.83

The truncated-icosahedral direction now has a formal combinatorial profile:

* global counts satisfy Euler and face-edge incidence;
* the rank-three barycentric profile has 182 cells and 360 maximal flags;
* the local vertex figure is represented as pentagon + hexagon + hexagon;
* pentagram and hexagram refinements preserve their central face kind;
* the hexagram sector count is numerically compatible with the v3.82
  six-term middle-switch expression.

The next theorem unit should construct actual incidence data rather than add
more numerical identities.  In particular it should realize a finite
rank-three face poset whose maximal chains are vertex-edge-face flags, and then
define a candidate map from the six v3.82 terms to one cyclic hexagonal
refinement boundary.  Only after that map is proved incidence-compatible
should a genuine truncated-icosahedral obstruction theorem be stated.
-/

end KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83
