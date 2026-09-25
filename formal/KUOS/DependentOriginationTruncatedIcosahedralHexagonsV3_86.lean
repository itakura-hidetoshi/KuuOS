import KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
import Mathlib

namespace KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86

open KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85

set_option autoImplicit false

noncomputable section

/-!
# Truncated-icosahedral hexagonal cycles v3.86

v3.85 constructs the 90-edge truncated-icosahedral 1-skeleton and the twelve
closed pentagonal boundaries.  This file constructs the twenty hexagonal
boundaries coming from the original icosahedral triangular faces.

Orientation is made explicit because a triangular face traverses some original
edges in the direction opposite to the endpoint ordering chosen in v3.84.
Each hexagon alternates

around -- cross -- around -- cross -- around -- cross

and carries six proved endpoint matchings, including the final closure.

This is the first theorem unit in which the hexagonal face is an actual cyclic
incidence object rather than only a face label or a numerical arity.  No
identification with the v3.82 six scalar terms is made yet.
-/

/-- An orientation on one truncated-icosahedral edge. -/
inductive OrientedTruncatedIcosahedralEdge
  | forward (e : TruncatedIcosahedralEdge)
  | reverse (e : TruncatedIcosahedralEdge)
  deriving DecidableEq, Repr

/-- Forget orientation. -/
def OrientedTruncatedIcosahedralEdge.edge :
    OrientedTruncatedIcosahedralEdge → TruncatedIcosahedralEdge
  | .forward e => e
  | .reverse e => e

/-- Source dart of an oriented truncated edge. -/
def OrientedTruncatedIcosahedralEdge.source :
    OrientedTruncatedIcosahedralEdge → IcosahedralDart
  | .forward e => (truncatedIcosahedralEdgeEndpoints e).1
  | .reverse e => (truncatedIcosahedralEdgeEndpoints e).2

/-- Target dart of an oriented truncated edge. -/
def OrientedTruncatedIcosahedralEdge.target :
    OrientedTruncatedIcosahedralEdge → IcosahedralDart
  | .forward e => (truncatedIcosahedralEdgeEndpoints e).2
  | .reverse e => (truncatedIcosahedralEdgeEndpoints e).1

@[simp] theorem oriented_forward_cross_source
    (e : IcosahedralEdge) :
    (OrientedTruncatedIcosahedralEdge.forward
      (.cross e)).source = .first e := rfl

@[simp] theorem oriented_forward_cross_target
    (e : IcosahedralEdge) :
    (OrientedTruncatedIcosahedralEdge.forward
      (.cross e)).target = .second e := rfl

@[simp] theorem oriented_reverse_cross_source
    (e : IcosahedralEdge) :
    (OrientedTruncatedIcosahedralEdge.reverse
      (.cross e)).source = .second e := rfl

@[simp] theorem oriented_reverse_cross_target
    (e : IcosahedralEdge) :
    (OrientedTruncatedIcosahedralEdge.reverse
      (.cross e)).target = .first e := rfl

@[simp] theorem oriented_forward_around_source
    (v : IcosahedralVertex) (s : PentagonalSlot) :
    (OrientedTruncatedIcosahedralEdge.forward
      (.around ⟨v, s⟩)).source =
      icosahedralIncidentDartAt v s := rfl

@[simp] theorem oriented_forward_around_target
    (v : IcosahedralVertex) (s : PentagonalSlot) :
    (OrientedTruncatedIcosahedralEdge.forward
      (.around ⟨v, s⟩)).target =
      icosahedralIncidentDartAt v (pentagonalSlotNext s) := rfl

@[simp] theorem oriented_reverse_around_source
    (v : IcosahedralVertex) (s : PentagonalSlot) :
    (OrientedTruncatedIcosahedralEdge.reverse
      (.around ⟨v, s⟩)).source =
      icosahedralIncidentDartAt v (pentagonalSlotNext s) := rfl

@[simp] theorem oriented_reverse_around_target
    (v : IcosahedralVertex) (s : PentagonalSlot) :
    (OrientedTruncatedIcosahedralEdge.reverse
      (.around ⟨v, s⟩)).target =
      icosahedralIncidentDartAt v s := rfl

/-- Six explicitly oriented edges with all cyclic endpoint incidences proved. -/
structure OrientedHexagonCycle where
  e0 : OrientedTruncatedIcosahedralEdge
  e1 : OrientedTruncatedIcosahedralEdge
  e2 : OrientedTruncatedIcosahedralEdge
  e3 : OrientedTruncatedIcosahedralEdge
  e4 : OrientedTruncatedIcosahedralEdge
  e5 : OrientedTruncatedIcosahedralEdge
  h01 : e0.target = e1.source
  h12 : e1.target = e2.source
  h23 : e2.target = e3.source
  h34 : e3.target = e4.source
  h45 : e4.target = e5.source
  h50 : e5.target = e0.source

/-- The six oriented edges as an ordered boundary list. -/
def OrientedHexagonCycle.edges
    (C : OrientedHexagonCycle) :
    List OrientedTruncatedIcosahedralEdge :=
  [C.e0, C.e1, C.e2, C.e3, C.e4, C.e5]

@[simp] theorem OrientedHexagonCycle_edges_length
    (C : OrientedHexagonCycle) :
    C.edges.length = 6 := by
  rfl

/-- Edge-family label, used to expose the alternating around/cross pattern. -/
inductive TruncatedIcosahedralEdgeFamily
  | around
  | cross
  deriving DecidableEq, Repr

/-- Family of an unoriented truncated edge. -/
def truncatedIcosahedralEdgeFamily :
    TruncatedIcosahedralEdge → TruncatedIcosahedralEdgeFamily
  | .around _ => .around
  | .cross _ => .cross

/-- Family of an oriented truncated edge. -/
def OrientedTruncatedIcosahedralEdge.family
    (e : OrientedTruncatedIcosahedralEdge) :
    TruncatedIcosahedralEdgeFamily :=
  truncatedIcosahedralEdgeFamily e.edge

/-- The hexagonal boundary obtained from one original triangular face. -/
def truncatedIcosahedralHexagonCycle :
    IcosahedralFace → OrientedHexagonCycle
  | .top i =>
      {
        e0 := .forward
          (.around ⟨.north, pentagonalSlotOfIndex i⟩)
        e1 := .forward (.cross (.northSpoke (i + 1)))
        e2 := .reverse (.around ⟨.upper (i + 1), .s4⟩)
        e3 := .reverse (.cross (.upperRing i))
        e4 := .reverse (.around ⟨.upper i, .s0⟩)
        e5 := .reverse (.cross (.northSpoke i))
        h01 := by
          simp [icosahedralIncidentDartAt, pentagonalSlotIndex_next]
        h12 := by
          simp [icosahedralIncidentDartAt]
        h23 := by
          simp [icosahedralIncidentDartAt]
        h34 := by
          simp [icosahedralIncidentDartAt]
        h45 := by
          simp [icosahedralIncidentDartAt]
        h50 := by
          simp [icosahedralIncidentDartAt]
      }
  | .bottom i =>
      {
        e0 := .forward
          (.around ⟨.south, pentagonalSlotOfIndex i⟩)
        e1 := .forward (.cross (.southSpoke (i + 1)))
        e2 := .reverse (.around ⟨.lower (i + 1), .s4⟩)
        e3 := .reverse (.cross (.lowerRing i))
        e4 := .reverse (.around ⟨.lower i, .s0⟩)
        e5 := .reverse (.cross (.southSpoke i))
        h01 := by
          simp [icosahedralIncidentDartAt, pentagonalSlotIndex_next]
        h12 := by
          simp [icosahedralIncidentDartAt]
        h23 := by
          simp [icosahedralIncidentDartAt]
        h34 := by
          simp [icosahedralIncidentDartAt]
        h45 := by
          simp [icosahedralIncidentDartAt]
        h50 := by
          simp [icosahedralIncidentDartAt]
      }
  | .beltUpper i =>
      {
        e0 := .forward (.around ⟨.upper i, .s1⟩)
        e1 := .forward (.cross (.crossAligned i))
        e2 := .reverse (.around ⟨.lower i, .s2⟩)
        e3 := .reverse (.cross (.crossShifted i))
        e4 := .forward (.around ⟨.upper (i + 1), .s3⟩)
        e5 := .reverse (.cross (.upperRing i))
        h01 := by
          simp [icosahedralIncidentDartAt]
        h12 := by
          simp [icosahedralIncidentDartAt]
        h23 := by
          simp [icosahedralIncidentDartAt]
        h34 := by
          simp [icosahedralIncidentDartAt]
        h45 := by
          simp [icosahedralIncidentDartAt]
        h50 := by
          simp [icosahedralIncidentDartAt]
      }
  | .beltLower i =>
      {
        e0 := .reverse (.around ⟨.upper (i + 1), .s2⟩)
        e1 := .forward (.cross (.crossAligned (i + 1)))
        e2 := .forward (.around ⟨.lower (i + 1), .s3⟩)
        e3 := .reverse (.cross (.lowerRing i))
        e4 := .forward (.around ⟨.lower i, .s1⟩)
        e5 := .reverse (.cross (.crossShifted i))
        h01 := by
          simp [icosahedralIncidentDartAt]
        h12 := by
          simp [icosahedralIncidentDartAt]
        h23 := by
          simp [icosahedralIncidentDartAt]
        h34 := by
          simp [icosahedralIncidentDartAt]
        h45 := by
          simp [icosahedralIncidentDartAt]
        h50 := by
          simp [icosahedralIncidentDartAt]
      }

/-- Every triangle-origin face now has six actual oriented boundary edges. -/
@[simp] theorem truncatedIcosahedralHexagonCycle_length
    (f : IcosahedralFace) :
    (truncatedIcosahedralHexagonCycle f).edges.length = 6 := by
  rfl

/-- The six-edge cycle alternates around and cross families. -/
theorem truncatedIcosahedralHexagonCycle_family_pattern
    (f : IcosahedralFace) :
    ((truncatedIcosahedralHexagonCycle f).e0.family,
      (truncatedIcosahedralHexagonCycle f).e1.family,
      (truncatedIcosahedralHexagonCycle f).e2.family,
      (truncatedIcosahedralHexagonCycle f).e3.family,
      (truncatedIcosahedralHexagonCycle f).e4.family,
      (truncatedIcosahedralHexagonCycle f).e5.family) =
    (.around, .cross, .around, .cross, .around, .cross) := by
  cases f <;> rfl

/-- There are exactly twenty explicit hexagonal cycles, one for each original
icosahedral triangular face. -/
theorem truncatedIcosahedral_hexagon_cycle_count :
    Fintype.card IcosahedralFace =
      truncatedIcosahedralFaceMultiplicity .hexagon := by
  native_decide

/-- The actual cyclic boundary has the same arity as the v3.82 middle-switch
six-term expression.

Unlike the arity statement in v3.83, the left side now comes from a proved
closed incidence cycle.  This still does not identify individual scalar terms
with individual boundary edges.
-/
theorem truncatedIcosahedralHexagonCycle_matches_middleSwitchSixTerm_arity
    (f : IcosahedralFace) :
    (truncatedIcosahedralHexagonCycle f).edges.length =
      middleSwitchSixTermArity := by
  rfl

/-!
## Boundary after v3.86

The truncated-icosahedral carrier now contains both genuine face types:

* twelve closed pentagonal five-cycles from v3.85;
* twenty closed oriented hexagonal six-cycles from this file.

Each hexagon is incidence-derived from one original icosahedral triangle and
alternates three around edges with three cross edges.  Its boundary arity is
six, matching the v3.82 scalar expression, but no term-by-term identification
has yet been assumed.

The next theorem unit should define a six-position index and expose the v3.82
six-term expression as an indexed family.  Only then should one propose and
verify a position-by-position map from scalar terms to one oriented hexagonal
cycle.  Cyclic compatibility, not cardinality alone, is the next obstruction
boundary.
-/

end

end KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
