import KUOS.DependentOriginationPentagramInnerPentagonV3_89
import Mathlib

namespace KUOS.DependentOriginationTruncatedIcosahedralRecursiveRefinementV3_90

open KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83
open KUOS.DependentOriginationHexagramInnerHexagonV3_88
open KUOS.DependentOriginationPentagramInnerPentagonV3_89

set_option autoImplicit false

/-!
# Face-kind-indexed recursive star refinement v3.90

v3.88 and v3.89 construct explicit incidence-level recursive star refinements
for the two face kinds of the truncated icosahedron:

* hexagon -> hexagram -> inner hexagon;
* pentagon -> pentagram -> inner pentagon.

This file packages both constructions into one face-kind-indexed operator and
proves that one refinement step preserves the local 5.6.6 signature.

Only combinatorial face kind and boundary arity are propagated.  Metric scale,
Euclidean realization, and infinite-limit convergence remain outside the
statement.
-/

/-- Explicit inner boundary length produced by one star-refinement step. -/
def truncatedIcosahedralRecursiveInnerBoundaryLength :
    TruncatedIcosahedralFaceKind → Nat
  | .pentagon => pentagramInnerBoundary.length
  | .hexagon => hexagramInnerBoundary.length

/-- Explicit inner face kind produced by one star-refinement step. -/
def truncatedIcosahedralRecursiveInnerFaceKind :
    TruncatedIcosahedralFaceKind → TruncatedIcosahedralFaceKind
  | .pentagon => pentagramInnerFaceKind
  | .hexagon => hexagramInnerFaceKind

/-- One recursive refinement step preserves face kind. -/
@[simp] theorem truncatedIcosahedralRecursiveInnerFaceKind_eq
    (k : TruncatedIcosahedralFaceKind) :
    truncatedIcosahedralRecursiveInnerFaceKind k = k := by
  cases k <;> rfl

/-- One recursive refinement step regenerates the same boundary arity. -/
@[simp] theorem truncatedIcosahedralRecursiveInnerBoundaryLength_eq
    (k : TruncatedIcosahedralFaceKind) :
    truncatedIcosahedralRecursiveInnerBoundaryLength k =
      truncatedIcosahedralFaceSides k := by
  cases k <;> rfl

/-- The explicit recursive refinement agrees with the abstract sector count
introduced in v3.83. -/
theorem truncatedIcosahedralRecursiveInnerBoundaryLength_eq_starSectors
    (k : TruncatedIcosahedralFaceKind) :
    truncatedIcosahedralRecursiveInnerBoundaryLength k =
      (match k with
        | .pentagon => pentagramRefinement
        | .hexagon => hexagramRefinement).sectors := by
  cases k <;> rfl

/-- Package the explicit inner-cell data produced by one refinement step. -/
structure RecursiveStarCell where
  outer : TruncatedIcosahedralFaceKind
  inner : TruncatedIcosahedralFaceKind
  innerBoundaryLength : Nat
  inner_eq_outer : inner = outer
  boundary_eq_outerSides :
    innerBoundaryLength = truncatedIcosahedralFaceSides outer

/-- Face-kind-indexed explicit recursive cell. -/
def truncatedIcosahedralRecursiveStarCell
    (k : TruncatedIcosahedralFaceKind) :
    RecursiveStarCell where
  outer := k
  inner := truncatedIcosahedralRecursiveInnerFaceKind k
  innerBoundaryLength :=
    truncatedIcosahedralRecursiveInnerBoundaryLength k
  inner_eq_outer :=
    truncatedIcosahedralRecursiveInnerFaceKind_eq k
  boundary_eq_outerSides :=
    truncatedIcosahedralRecursiveInnerBoundaryLength_eq k

/-- Refinement attached to one local face slot of the 5.6.6 vertex figure. -/
def truncatedIcosahedralLocalRecursiveStarCell
    (s : TruncatedIcosahedralVertexSlot) :
    RecursiveStarCell :=
  truncatedIcosahedralRecursiveStarCell
    (truncatedIcosahedralLocalFaceKind s)

/-- The refined inner face at every local slot has the same kind as the
original local face. -/
theorem truncatedIcosahedralLocalRecursiveStarCell_kind_preserved
    (s : TruncatedIcosahedralVertexSlot) :
    (truncatedIcosahedralLocalRecursiveStarCell s).inner =
      truncatedIcosahedralLocalFaceKind s := by
  exact
    (truncatedIcosahedralLocalRecursiveStarCell s).inner_eq_outer

/-- The refined inner boundary at every local slot has exactly the original
face arity. -/
theorem truncatedIcosahedralLocalRecursiveStarCell_arity_preserved
    (s : TruncatedIcosahedralVertexSlot) :
    (truncatedIcosahedralLocalRecursiveStarCell s).innerBoundaryLength =
      truncatedIcosahedralFaceSides
        (truncatedIcosahedralLocalFaceKind s) := by
  exact
    (truncatedIcosahedralLocalRecursiveStarCell s).boundary_eq_outerSides

/-- One simultaneous refinement step preserves the local 5.6.6 arity
signature exactly. -/
theorem truncatedIcosahedralLocalRecursiveStarCell_566 :
    ((truncatedIcosahedralLocalRecursiveStarCell
        .pentagonal).innerBoundaryLength,
      (truncatedIcosahedralLocalRecursiveStarCell
        .hexagonalLeft).innerBoundaryLength,
      (truncatedIcosahedralLocalRecursiveStarCell
        .hexagonalRight).innerBoundaryLength) =
    (5, 6, 6) := by
  rfl

/-- The corresponding face-kind signature is also preserved exactly. -/
theorem truncatedIcosahedralLocalRecursiveStarCell_kind_signature :
    ((truncatedIcosahedralLocalRecursiveStarCell
        .pentagonal).inner,
      (truncatedIcosahedralLocalRecursiveStarCell
        .hexagonalLeft).inner,
      (truncatedIcosahedralLocalRecursiveStarCell
        .hexagonalRight).inner) =
    (.pentagon, .hexagon, .hexagon) := by
  rfl

/-- Iterate only the face-kind component of the recursive refinement.

Because each explicit inner cell has the same kind as its parent, every finite
iteration is definitionally stable after proof reduction.
-/
def truncatedIcosahedralRecursiveFaceKind :
    Nat → TruncatedIcosahedralFaceKind →
      TruncatedIcosahedralFaceKind
  | 0, k => k
  | Nat.succ n, k =>
      truncatedIcosahedralRecursiveInnerFaceKind
        (truncatedIcosahedralRecursiveFaceKind n k)

@[simp] theorem truncatedIcosahedralRecursiveFaceKind_eq
    (depth : Nat) (k : TruncatedIcosahedralFaceKind) :
    truncatedIcosahedralRecursiveFaceKind depth k = k := by
  induction depth with
  | zero =>
      rfl
  | succ depth ih =>
      simp [truncatedIcosahedralRecursiveFaceKind, ih]

/-- Hence every finite recursive depth preserves the pentagonal or hexagonal
boundary arity. -/
theorem truncatedIcosahedralRecursiveFaceKind_arity
    (depth : Nat) (k : TruncatedIcosahedralFaceKind) :
    truncatedIcosahedralFaceSides
        (truncatedIcosahedralRecursiveFaceKind depth k) =
      truncatedIcosahedralFaceSides k := by
  rw [truncatedIcosahedralRecursiveFaceKind_eq]

/-!
## Boundary after v3.90

The truncated-icosahedral carrier now has a single combinatorial recursive
refinement operator covering both face types.

One refinement step, and therefore every finite iteration at the level of face
kind, preserves:

* pentagon as pentagon with arity five;
* hexagon as hexagon with arity six;
* the local truncated-icosahedral signature 5.6.6.

Together with v3.87, the hexagonal refinement is not merely combinatorial:
its six outer tips are already in bijection with the exact two-triangle
3 + 3 decomposition of the v3.82 middle-switch scalar residual.

The next mathematical question is no longer whether a self-similar
truncated-icosahedral carrier exists.  The remaining task is to transport the
actual scalar/coherence data through one refinement step and test whether the
inner pentagon/hexagon carries the same obstruction class, a trivial class, or
a new explicit descent obstruction.
-/

end KUOS.DependentOriginationTruncatedIcosahedralRecursiveRefinementV3_90
