import KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
import Mathlib

namespace KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85

open KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84

set_option autoImplicit false

/-!
# Truncated-icosahedral edges and pentagonal cycles v3.85

v3.84 constructs truncated vertices as darts of an explicit regular
icosahedral incidence seed.  This file constructs the 90 truncated edges.

There are two edge families:

* 30 cross edges, one across every original icosahedral edge, pairing its two
  endpoint darts;
* 60 around-vertex edges, five around each original icosahedral vertex,
  joining consecutive incident darts in cyclic order.

The cyclic order is written explicitly for the north pole, south pole, upper
ring, and lower ring vertices.  This makes every vertex-origin truncation face
an actual closed five-edge cycle rather than only a face label.

The hexagonal boundaries associated to original triangular faces are left to
the next theorem unit.
-/

/-- Five cyclic slots around an original degree-five icosahedral vertex. -/
inductive PentagonalSlot
  | s0
  | s1
  | s2
  | s3
  | s4
  deriving DecidableEq, Repr, Fintype

@[simp] theorem pentagonalSlot_card :
    Fintype.card PentagonalSlot = 5 := by
  native_decide

/-- Convert the five slots to the ZMod 5 ring index when needed. -/
def pentagonalSlotIndex : PentagonalSlot → IcosahedralRingIndex
  | .s0 => 0
  | .s1 => 1
  | .s2 => 2
  | .s3 => 3
  | .s4 => 4

/-- Cyclic successor of a pentagonal slot. -/
def pentagonalSlotNext : PentagonalSlot → PentagonalSlot
  | .s0 => .s1
  | .s1 => .s2
  | .s2 => .s3
  | .s3 => .s4
  | .s4 => .s0

/-- The slot-index map is a bijection with ZMod 5. -/
theorem pentagonalSlotIndex_bijective :
    Function.Bijective pentagonalSlotIndex := by
  native_decide

/-- Canonical finite equivalence between cyclic pentagonal slots and ZMod 5. -/
noncomputable def pentagonalSlotEquiv :
    PentagonalSlot ≃ IcosahedralRingIndex :=
  Equiv.ofBijective pentagonalSlotIndex pentagonalSlotIndex_bijective

/-- Recover the pentagonal slot carrying a prescribed ZMod 5 index. -/
noncomputable def pentagonalSlotOfIndex
    (i : IcosahedralRingIndex) : PentagonalSlot :=
  pentagonalSlotEquiv.symm i

@[simp] theorem pentagonalSlotIndex_ofIndex
    (i : IcosahedralRingIndex) :
    pentagonalSlotIndex (pentagonalSlotOfIndex i) = i := by
  change pentagonalSlotEquiv (pentagonalSlotEquiv.symm i) = i
  exact pentagonalSlotEquiv.apply_symm_apply i

/-- Cyclic slot successor is exactly addition by one on the ZMod 5 index. -/
theorem pentagonalSlotIndex_next
    (s : PentagonalSlot) :
    pentagonalSlotIndex (pentagonalSlotNext s) =
      pentagonalSlotIndex s + 1 := by
  cases s <;> native_decide

/-- Pulling an index back to a slot commutes with cyclic successor. -/
theorem pentagonalSlotOfIndex_add_one
    (i : IcosahedralRingIndex) :
    pentagonalSlotOfIndex (i + 1) =
      pentagonalSlotNext (pentagonalSlotOfIndex i) := by
  apply pentagonalSlotIndex_bijective.1
  rw [pentagonalSlotIndex_ofIndex, pentagonalSlotIndex_next,
    pentagonalSlotIndex_ofIndex]

/-- The five incident darts around each original icosahedral vertex, in cyclic
order.

For upper and lower ring vertices, the order is chosen so that consecutive
darts bound one original triangular face. -/
def icosahedralIncidentDartAt :
    IcosahedralVertex → PentagonalSlot → IcosahedralDart
  | .north, s =>
      .first (.northSpoke (pentagonalSlotIndex s))
  | .south, s =>
      .first (.southSpoke (pentagonalSlotIndex s))
  | .upper i, .s0 =>
      .second (.northSpoke i)
  | .upper i, .s1 =>
      .first (.upperRing i)
  | .upper i, .s2 =>
      .first (.crossAligned i)
  | .upper i, .s3 =>
      .first (.crossShifted (i - 1))
  | .upper i, .s4 =>
      .second (.upperRing (i - 1))
  | .lower i, .s0 =>
      .second (.southSpoke i)
  | .lower i, .s1 =>
      .first (.lowerRing i)
  | .lower i, .s2 =>
      .second (.crossShifted i)
  | .lower i, .s3 =>
      .second (.crossAligned i)
  | .lower i, .s4 =>
      .second (.lowerRing (i - 1))

/-- Every listed incident dart is based at the vertex whose cyclic list it
belongs to. -/
theorem icosahedralIncidentDartAt_endpoint
    (v : IcosahedralVertex) (s : PentagonalSlot) :
    (icosahedralIncidentDartAt v s).endpoint = v := by
  cases v <;> cases s <;>
    simp [icosahedralIncidentDartAt, pentagonalSlotIndex,
      IcosahedralDart.endpoint, icosahedralEdgeEndpoints]

/-- One of the five around-vertex edges at an original icosahedral vertex. -/
structure TruncatedIcosahedralAroundEdge where
  center : IcosahedralVertex
  slot : PentagonalSlot
  deriving DecidableEq, Repr, Fintype

@[simp] theorem truncatedIcosahedralAroundEdge_card :
    Fintype.card TruncatedIcosahedralAroundEdge = 60 := by
  native_decide

/-- The two dart endpoints of an around-vertex edge. -/
def truncatedIcosahedralAroundEdgeEndpoints
    (a : TruncatedIcosahedralAroundEdge) :
    IcosahedralDart × IcosahedralDart :=
  (icosahedralIncidentDartAt a.center a.slot,
    icosahedralIncidentDartAt a.center (pentagonalSlotNext a.slot))

/-- Both endpoints of an around-vertex edge lie over its center vertex. -/
theorem truncatedIcosahedralAroundEdge_first_endpoint_center
    (a : TruncatedIcosahedralAroundEdge) :
    (truncatedIcosahedralAroundEdgeEndpoints a).1.endpoint =
      a.center := by
  exact icosahedralIncidentDartAt_endpoint a.center a.slot

/-- Both endpoints of an around-vertex edge lie over its center vertex. -/
theorem truncatedIcosahedralAroundEdge_second_endpoint_center
    (a : TruncatedIcosahedralAroundEdge) :
    (truncatedIcosahedralAroundEdgeEndpoints a).2.endpoint =
      a.center := by
  exact
    icosahedralIncidentDartAt_endpoint
      a.center (pentagonalSlotNext a.slot)

/-- All 90 edges of the truncated icosahedron.

A cross edge remembers an original icosahedral edge.  An around edge remembers
one consecutive pair in the cyclic dart order around an original vertex.
-/
inductive TruncatedIcosahedralEdge
  | cross (e : IcosahedralEdge)
  | around (a : TruncatedIcosahedralAroundEdge)
  deriving DecidableEq, Repr, Fintype

/-- Dart endpoints of every truncated edge. -/
def truncatedIcosahedralEdgeEndpoints :
    TruncatedIcosahedralEdge → IcosahedralDart × IcosahedralDart
  | .cross e => (.first e, .second e)
  | .around a => truncatedIcosahedralAroundEdgeEndpoints a

@[simp] theorem truncatedIcosahedralEdge_card :
    Fintype.card TruncatedIcosahedralEdge = 90 := by
  native_decide

/-- The explicit edge type recovers the global edge count from v3.83. -/
theorem truncatedIcosahedralEdge_card_eq_global :
    Fintype.card TruncatedIcosahedralEdge =
      truncatedIcosahedralEdgeCount := by
  native_decide

/-- A cross edge really pairs the two darts of one original edge. -/
@[simp] theorem truncatedIcosahedralEdgeEndpoints_cross
    (e : IcosahedralEdge) :
    truncatedIcosahedralEdgeEndpoints (.cross e) =
      (.first e, .second e) := rfl

/-- Consecutive around edges share the expected cyclic dart endpoint. -/
theorem truncatedIcosahedralAroundEdge_consecutive
    (v : IcosahedralVertex) (s : PentagonalSlot) :
    (truncatedIcosahedralEdgeEndpoints
        (.around ⟨v, s⟩)).2 =
      (truncatedIcosahedralEdgeEndpoints
        (.around ⟨v, pentagonalSlotNext s⟩)).1 := by
  rfl

/-- Five around edges forming the pentagon created by truncating one original
icosahedral vertex. -/
def truncatedIcosahedralPentagonBoundary
    (v : IcosahedralVertex) :
    List TruncatedIcosahedralEdge :=
  [
    .around ⟨v, .s0⟩,
    .around ⟨v, .s1⟩,
    .around ⟨v, .s2⟩,
    .around ⟨v, .s3⟩,
    .around ⟨v, .s4⟩
  ]

@[simp] theorem truncatedIcosahedralPentagonBoundary_length
    (v : IcosahedralVertex) :
    (truncatedIcosahedralPentagonBoundary v).length = 5 := by
  rfl

/-- The last around edge closes back to the first dart of the pentagon. -/
theorem truncatedIcosahedralPentagonBoundary_closes
    (v : IcosahedralVertex) :
    (truncatedIcosahedralEdgeEndpoints
        (.around ⟨v, .s4⟩)).2 =
      (truncatedIcosahedralEdgeEndpoints
        (.around ⟨v, .s0⟩)).1 := by
  rfl

/-- Every edge of a vertex-origin pentagon is an around-vertex edge centered
at that same original vertex. -/
theorem truncatedIcosahedralPentagonBoundary_center
    (v : IcosahedralVertex)
    (e : TruncatedIcosahedralEdge)
    (he : e ∈ truncatedIcosahedralPentagonBoundary v) :
    ∃ s : PentagonalSlot, e = .around ⟨v, s⟩ := by
  simp [truncatedIcosahedralPentagonBoundary] at he
  rcases he with h | h | h | h | h
  · exact ⟨.s0, h⟩
  · exact ⟨.s1, h⟩
  · exact ⟨.s2, h⟩
  · exact ⟨.s3, h⟩
  · exact ⟨.s4, h⟩

/-!
## Boundary after v3.85

The truncated-icosahedral 1-skeleton is now explicit:

* 60 truncated vertices from v3.84;
* 30 cross edges pairing the darts of original edges;
* 60 around-vertex edges generated by degree-five cyclic dart orders;
* 90 edges in total;
* each of the 12 vertex-origin faces has an explicit closed five-edge boundary.

The next theorem unit should construct, for every original triangular face,
the alternating six-edge cycle

around -- cross -- around -- cross -- around -- cross

that becomes its truncated hexagon.  That will make both face types actual
cycles and will provide the incidence object needed before mapping the v3.82
six scalar terms onto a hexagonal coherence boundary.
-/

end KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
