import KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83
import Mathlib

namespace KUOS.DependentOriginationIcosahedralTruncationSeedV3_84

open KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83

set_option autoImplicit false

/-!
# Icosahedral truncation seed v3.84

v3.83 records the truncated-icosahedral numerical and recursive star-refinement
profile.  This file replaces the purely numerical 5.6.6 signature by explicit
finite incidence data.

The regular icosahedron is presented as

* north and south poles;
* an upper 5-cycle U_i;
* a lower 5-cycle L_i;

with i in ZMod 5.  Six edge families give 30 edges and four triangular face
families give 20 faces.  Every edge is assigned its two incident triangles.

A vertex of the truncated icosahedron is then represented by a dart: one of
the two ends of an original icosahedral edge.  Hence there are 60 darts.  The
faces created by truncation are represented by

* one pentagon around each original icosahedral vertex;
* one hexagon from each original triangular face.

For every dart, the local truncated face triple is constructed from incidence:
the pentagon associated to its endpoint and the two hexagons associated to the
two original triangles incident to its edge.  Thus the 5.6.6 local signature
is now incidence-derived rather than only numerically postulated.

This remains combinatorial.  Euclidean coordinates and metric regularity are
not used.
-/

/-- Cyclic index for the two pentagonal rings. -/
abbrev IcosahedralRingIndex := ZMod 5

/-- Twelve vertices of the regular icosahedron. -/
inductive IcosahedralVertex
  | north
  | south
  | upper (i : IcosahedralRingIndex)
  | lower (i : IcosahedralRingIndex)
  deriving DecidableEq, Repr, Fintype

/-- Thirty edges in six cyclic families. -/
inductive IcosahedralEdge
  | northSpoke (i : IcosahedralRingIndex)
  | southSpoke (i : IcosahedralRingIndex)
  | upperRing (i : IcosahedralRingIndex)
  | lowerRing (i : IcosahedralRingIndex)
  | crossAligned (i : IcosahedralRingIndex)
  | crossShifted (i : IcosahedralRingIndex)
  deriving DecidableEq, Repr, Fintype

/-- Twenty triangular faces in four cyclic families. -/
inductive IcosahedralFace
  | top (i : IcosahedralRingIndex)
  | bottom (i : IcosahedralRingIndex)
  | beltUpper (i : IcosahedralRingIndex)
  | beltLower (i : IcosahedralRingIndex)
  deriving DecidableEq, Repr, Fintype

@[simp] theorem icosahedralVertex_card :
    Fintype.card IcosahedralVertex = 12 := by
  native_decide

@[simp] theorem icosahedralEdge_card :
    Fintype.card IcosahedralEdge = 30 := by
  native_decide

@[simp] theorem icosahedralFace_card :
    Fintype.card IcosahedralFace = 20 := by
  native_decide

/-- Ordered endpoints of every edge.  The order is used only to define the two
dart constructors below; the underlying edge is still combinatorial. -/
def icosahedralEdgeEndpoints :
    IcosahedralEdge → IcosahedralVertex × IcosahedralVertex
  | .northSpoke i => (.north, .upper i)
  | .southSpoke i => (.south, .lower i)
  | .upperRing i => (.upper i, .upper (i + 1))
  | .lowerRing i => (.lower i, .lower (i + 1))
  | .crossAligned i => (.upper i, .lower i)
  | .crossShifted i => (.upper (i + 1), .lower i)

/-- Boundary vertices of each triangular face. -/
def icosahedralFaceVertices :
    IcosahedralFace → List IcosahedralVertex
  | .top i =>
      [.north, .upper i, .upper (i + 1)]
  | .bottom i =>
      [.south, .lower i, .lower (i + 1)]
  | .beltUpper i =>
      [.upper i, .upper (i + 1), .lower i]
  | .beltLower i =>
      [.upper (i + 1), .lower i, .lower (i + 1)]

@[simp] theorem icosahedralFaceVertices_length
    (f : IcosahedralFace) :
    (icosahedralFaceVertices f).length = 3 := by
  cases f <;> rfl

/-- Boundary edges of each triangular face. -/
def icosahedralFaceEdges :
    IcosahedralFace → List IcosahedralEdge
  | .top i =>
      [.northSpoke i, .upperRing i, .northSpoke (i + 1)]
  | .bottom i =>
      [.southSpoke i, .lowerRing i, .southSpoke (i + 1)]
  | .beltUpper i =>
      [.upperRing i, .crossShifted i, .crossAligned i]
  | .beltLower i =>
      [.crossShifted i, .lowerRing i, .crossAligned (i + 1)]

@[simp] theorem icosahedralFaceEdges_length
    (f : IcosahedralFace) :
    (icosahedralFaceEdges f).length = 3 := by
  cases f <;> rfl

/-- The two triangles incident to each original icosahedral edge. -/
def icosahedralEdgeIncidentFaces :
    IcosahedralEdge → IcosahedralFace × IcosahedralFace
  | .northSpoke i => (.top i, .top (i - 1))
  | .southSpoke i => (.bottom i, .bottom (i - 1))
  | .upperRing i => (.top i, .beltUpper i)
  | .lowerRing i => (.bottom i, .beltLower i)
  | .crossAligned i => (.beltUpper i, .beltLower (i - 1))
  | .crossShifted i => (.beltUpper i, .beltLower i)

/-- Every edge occurs in the boundary list of its first declared incident
triangle. -/
theorem icosahedralEdge_mem_firstIncidentFace
    (e : IcosahedralEdge) :
    e ∈ icosahedralFaceEdges (icosahedralEdgeIncidentFaces e).1 := by
  cases e <;>
    simp [icosahedralFaceEdges, icosahedralEdgeIncidentFaces]

/-- Every edge occurs in the boundary list of its second declared incident
triangle. -/
theorem icosahedralEdge_mem_secondIncidentFace
    (e : IcosahedralEdge) :
    e ∈ icosahedralFaceEdges (icosahedralEdgeIncidentFaces e).2 := by
  cases e <;>
    simp [icosahedralFaceEdges, icosahedralEdgeIncidentFaces]

/-- A dart is one selected endpoint of an icosahedral edge.

Under truncation, darts become the vertices of the truncated icosahedron. -/
inductive IcosahedralDart
  | first (e : IcosahedralEdge)
  | second (e : IcosahedralEdge)
  deriving DecidableEq, Repr, Fintype

/-- Forget the selected endpoint. -/
def IcosahedralDart.edge : IcosahedralDart → IcosahedralEdge
  | .first e => e
  | .second e => e

/-- The original icosahedral vertex at which the dart is based. -/
def IcosahedralDart.endpoint : IcosahedralDart → IcosahedralVertex
  | .first e => (icosahedralEdgeEndpoints e).1
  | .second e => (icosahedralEdgeEndpoints e).2

@[simp] theorem icosahedralDart_card :
    Fintype.card IcosahedralDart = 60 := by
  native_decide

/-- The 60 darts recover the global truncated-icosahedral vertex count from
v3.83. -/
theorem icosahedralDart_card_eq_truncatedVertexCount :
    Fintype.card IcosahedralDart =
      truncatedIcosahedralVertexCount := by
  native_decide

/-- Faces created by truncating the regular icosahedron.

An original vertex creates a pentagon; an original triangle becomes a
hexagon. -/
inductive TruncatedIcosahedralSeedFace
  | aroundVertex (v : IcosahedralVertex)
  | fromTriangle (f : IcosahedralFace)
  deriving DecidableEq, Repr, Fintype

/-- Face kind forced by the truncation origin. -/
def truncatedIcosahedralSeedFaceKind :
    TruncatedIcosahedralSeedFace → TruncatedIcosahedralFaceKind
  | .aroundVertex _ => .pentagon
  | .fromTriangle _ => .hexagon

@[simp] theorem truncatedIcosahedralSeedFace_card :
    Fintype.card TruncatedIcosahedralSeedFace = 32 := by
  native_decide

/-- The 32 truncation-origin faces recover the global face count from v3.83. -/
theorem truncatedIcosahedralSeedFace_card_eq_global :
    Fintype.card TruncatedIcosahedralSeedFace =
      truncatedIcosahedralFaceCount := by
  native_decide

/-- Finite set of seed faces of one face kind. -/
def truncatedIcosahedralSeedFacesOfKind
    (k : TruncatedIcosahedralFaceKind) :
    Finset TruncatedIcosahedralSeedFace :=
  Finset.univ.filter
    (fun f => truncatedIcosahedralSeedFaceKind f = k)

@[simp] theorem truncatedIcosahedralSeedFacesOfKind_pentagon_card :
    (truncatedIcosahedralSeedFacesOfKind .pentagon).card = 12 := by
  native_decide

@[simp] theorem truncatedIcosahedralSeedFacesOfKind_hexagon_card :
    (truncatedIcosahedralSeedFacesOfKind .hexagon).card = 20 := by
  native_decide

/-- The three truncated faces meeting at one dart.

The pentagon is determined by the selected original endpoint.  The two
hexagons are determined by the two original triangles incident to the
underlying edge. -/
structure TruncatedIcosahedralDartLocalFaces where
  pentagon : TruncatedIcosahedralSeedFace
  hexagonLeft : TruncatedIcosahedralSeedFace
  hexagonRight : TruncatedIcosahedralSeedFace

/-- Incidence-derived local face triple around a truncated vertex. -/
def truncatedIcosahedralDartLocalFaces
    (d : IcosahedralDart) :
    TruncatedIcosahedralDartLocalFaces :=
  let incident := icosahedralEdgeIncidentFaces d.edge
  {
    pentagon := .aroundVertex d.endpoint
    hexagonLeft := .fromTriangle incident.1
    hexagonRight := .fromTriangle incident.2
  }

@[simp] theorem truncatedIcosahedralDartLocalFaces_pentagon_kind
    (d : IcosahedralDart) :
    truncatedIcosahedralSeedFaceKind
        (truncatedIcosahedralDartLocalFaces d).pentagon =
      .pentagon := by
  rfl

@[simp] theorem truncatedIcosahedralDartLocalFaces_hexagonLeft_kind
    (d : IcosahedralDart) :
    truncatedIcosahedralSeedFaceKind
        (truncatedIcosahedralDartLocalFaces d).hexagonLeft =
      .hexagon := by
  rfl

@[simp] theorem truncatedIcosahedralDartLocalFaces_hexagonRight_kind
    (d : IcosahedralDart) :
    truncatedIcosahedralSeedFaceKind
        (truncatedIcosahedralDartLocalFaces d).hexagonRight =
      .hexagon := by
  rfl

/-- The first local face has arity five. -/
theorem truncatedIcosahedralDartLocalFaces_pentagon_arity
    (d : IcosahedralDart) :
    truncatedIcosahedralFaceSides
        (truncatedIcosahedralSeedFaceKind
          (truncatedIcosahedralDartLocalFaces d).pentagon) =
      5 := by
  simp

/-- The second local face has arity six. -/
theorem truncatedIcosahedralDartLocalFaces_hexagonLeft_arity
    (d : IcosahedralDart) :
    truncatedIcosahedralFaceSides
        (truncatedIcosahedralSeedFaceKind
          (truncatedIcosahedralDartLocalFaces d).hexagonLeft) =
      6 := by
  simp

/-- The third local face has arity six. -/
theorem truncatedIcosahedralDartLocalFaces_hexagonRight_arity
    (d : IcosahedralDart) :
    truncatedIcosahedralFaceSides
        (truncatedIcosahedralSeedFaceKind
          (truncatedIcosahedralDartLocalFaces d).hexagonRight) =
      6 := by
  simp

/-!
## Boundary after v3.84

The truncated-icosahedral carrier now has an explicit regular-icosahedral
truncation seed:

* 12 original vertices, 30 original edges, 20 original triangles;
* an explicit pair of incident triangles for each original edge;
* 60 darts, hence 60 truncated vertices;
* 12 vertex-origin pentagons and 20 triangle-origin hexagons;
* for every dart, an incidence-derived local face signature 5.6.6.

The next unit should construct the 90 truncated edges.  There are two natural
families:

* 30 cross-edge connections pairing the two darts of each original edge;
* 60 around-vertex connections joining consecutive darts in the cyclic order
  around each original icosahedral vertex.

Once these edges are explicit, the pentagonal and hexagonal boundary cycles
can be stated as actual finite cycles rather than only face labels.
-/

end KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
