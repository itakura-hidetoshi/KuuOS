import Kuu.F112.TotalChange
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.DeriveFintype
import Mathlib.CategoryTheory.Category.Preorder
import Mathlib.CategoryTheory.ComposableArrows.Basic

/-!
# F112 / independent C60 truncation and physical incidence seed

All constructors are the actual combinatorial icosahedral truncation:
12 original vertices, 30 original edges, 20 triangles; vertices of C60
are darts of those edges. The 90 C60 edges are 30 cross-dart edges and
60 consecutive around-vertex darts. The 32 actual polygon sites are
12 old-vertex pentagons and 20 old-triangle hexagons.

No historical F51/F55/Gray module, adjoined square-face, or Bool proxy
for the global physical incidence category is used.
-/
namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000

abbrev Ring := ZMod 5

inductive Vertex where
  | north | south | upper (i : Ring) | lower (i : Ring)
  deriving DecidableEq, Fintype

inductive OrigEdge where
  | northSpoke (i : Ring) | southSpoke (i : Ring)
  | upperRing (i : Ring) | lowerRing (i : Ring)
  | crossAligned (i : Ring) | crossShifted (i : Ring)
  deriving DecidableEq, Fintype

inductive Triangle where
  | top (i : Ring) | bottom (i : Ring)
  | beltUpper (i : Ring) | beltLower (i : Ring)
  deriving DecidableEq, Fintype

/-- Original oriented-edge endpoint data, independent of any observation. -/
def endpoints : OrigEdge → Vertex × Vertex
  | .northSpoke i => (.north, .upper i)
  | .southSpoke i => (.south, .lower i)
  | .upperRing i => (.upper i, .upper (i + 1))
  | .lowerRing i => (.lower i, .lower (i + 1))
  | .crossAligned i => (.upper i, .lower i)
  | .crossShifted i => (.upper (i + 1), .lower i)

/-- The original triangle boundaries; the resulting C60 faces remain polygonal. -/
def triangleEdges : Triangle → List OrigEdge
  | .top i => [.northSpoke i, .upperRing i, .northSpoke (i + 1)]
  | .bottom i => [.southSpoke i, .lowerRing i, .southSpoke (i + 1)]
  | .beltUpper i => [.upperRing i, .crossShifted i, .crossAligned i]
  | .beltLower i => [.crossShifted i, .lowerRing i, .crossAligned (i + 1)]

/-- The two original triangles incident to each of the 30 old edges. -/
def incidentFaces : OrigEdge → Triangle × Triangle
  | .northSpoke i => (.top i, .top (i - 1))
  | .southSpoke i => (.bottom i, .bottom (i - 1))
  | .upperRing i => (.top i, .beltUpper i)
  | .lowerRing i => (.bottom i, .beltLower i)
  | .crossAligned i => (.beltUpper i, .beltLower (i - 1))
  | .crossShifted i => (.beltUpper i, .beltLower i)

inductive Dart where
  | first (e : OrigEdge) | second (e : OrigEdge)
  deriving DecidableEq, Fintype

def Dart.edge : Dart → OrigEdge
  | .first e => e | .second e => e

def Dart.endpoint : Dart → Vertex
  | .first e => (endpoints e).1 | .second e => (endpoints e).2

inductive Polygon where
  | pentagon (v : Vertex) | hexagon (t : Triangle)
  deriving DecidableEq, Fintype

inductive Slot where
  | s0 | s1 | s2 | s3 | s4
  deriving DecidableEq, Fintype

def slotIndex : Slot → Ring
  | .s0 => 0 | .s1 => 1 | .s2 => 2 | .s3 => 3 | .s4 => 4

def slotNext : Slot → Slot
  | .s0 => .s1 | .s1 => .s2 | .s2 => .s3 | .s3 => .s4 | .s4 => .s0

/-- Cyclic lists of real incident darts at each old icosahedral vertex. -/
def incidentDart : Vertex → Slot → Dart
  | .north, s => .first (.northSpoke (slotIndex s))
  | .south, s => .first (.southSpoke (slotIndex s))
  | .upper i, .s0 => .second (.northSpoke i)
  | .upper i, .s1 => .first (.upperRing i)
  | .upper i, .s2 => .first (.crossAligned i)
  | .upper i, .s3 => .first (.crossShifted (i - 1))
  | .upper i, .s4 => .second (.upperRing (i - 1))
  | .lower i, .s0 => .second (.southSpoke i)
  | .lower i, .s1 => .first (.lowerRing i)
  | .lower i, .s2 => .second (.crossShifted i)
  | .lower i, .s3 => .second (.crossAligned i)
  | .lower i, .s4 => .second (.lowerRing (i - 1))

structure AroundEdge where
  center : Vertex
  slot : Slot
  deriving DecidableEq, Fintype

def aroundEndpoints (a : AroundEdge) : Dart × Dart :=
  (incidentDart a.center a.slot,
   incidentDart a.center (slotNext a.slot))

inductive Edge where
  | cross (e : OrigEdge) | around (a : AroundEdge)
  deriving DecidableEq, Fintype

def edgeEndpoints : Edge → Dart × Dart
  | .cross e => (.first e, .second e)
  | .around a => aroundEndpoints a

/-- The old triangular face between adjacent darts at a true vertex. -/
def cornerTriangle : Vertex → Slot → Triangle
  | .north, s => .top (slotIndex s)
  | .south, s => .bottom (slotIndex s)
  | .upper i, .s0 => .top i
  | .upper i, .s1 => .beltUpper i
  | .upper i, .s2 => .beltLower (i - 1)
  | .upper i, .s3 => .beltUpper (i - 1)
  | .upper i, .s4 => .top (i - 1)
  | .lower i, .s0 => .bottom i
  | .lower i, .s1 => .beltLower i
  | .lower i, .s2 => .beltUpper i
  | .lower i, .s3 => .beltLower (i - 1)
  | .lower i, .s4 => .bottom (i - 1)

/-- Both authentic polygons at an edge; never a fabricated square face. -/
def faceAt : Edge → Bool → Polygon
  | .cross e, false => .hexagon (incidentFaces e).1
  | .cross e, true => .hexagon (incidentFaces e).2
  | .around a, false => .pentagon a.center
  | .around a, true => .hexagon (cornerTriangle a.center a.slot)

/-- Actual polygonal incidence, derived from original triangles and darts. -/
def dartOnFace (d : Dart) : Polygon → Prop
  | .pentagon v => d.endpoint = v
  | .hexagon t => d.edge ∈ triangleEdges t

def edgeOnFace (e : Edge) (f : Polygon) : Prop :=
  match e, f with
  | .cross o, .hexagon t => o ∈ triangleEdges t
  | .around a, .pentagon v => a.center = v
  | .around a, .hexagon t =>
      (aroundEndpoints a).1.edge ∈ triangleEdges t ∧
      (aroundEndpoints a).2.edge ∈ triangleEdges t
  | _, _ => False

/-- The two declared real C60 polygon sites are incident to their edge. -/
theorem each_edge_on_faces :
    ∀ (e : Edge) (side : Bool), edgeOnFace e (faceAt e side) := by
  intro e side
  cases e with
  | cross e =>
    cases e <;> cases side <;>
      simp [edgeOnFace, faceAt, incidentFaces, triangleEdges]
  | around a =>
    rcases a with ⟨v, s⟩
    cases v <;> cases s <;> cases side <;>
      simp [edgeOnFace, faceAt, cornerTriangle, aroundEndpoints,
        incidentDart, Dart.edge, triangleEdges, slotIndex]

/-- Actual endpoint dart belongs to its selected polygon. -/
theorem incidentDart_endpoint :
    ∀ (v : Vertex) (s : Slot), (incidentDart v s).endpoint = v := by
  decide

/-- Any edge-to-face incidence has both dart endpoints on that face. -/
theorem edgeFace_endpoints (e : Edge) (f : Polygon) (h : edgeOnFace e f) :
    dartOnFace (edgeEndpoints e).1 f ∧ dartOnFace (edgeEndpoints e).2 f := by
  cases e with
  | cross old =>
    cases f with
    | pentagon v => cases h
    | hexagon tri => exact ⟨h, h⟩
  | around a =>
    cases f with
    | pentagon v =>
      change a.center = v at h
      subst v
      exact ⟨incidentDart_endpoint a.center a.slot,
        incidentDart_endpoint a.center (slotNext a.slot)⟩
    | hexagon tri => exact h

/-- Real original 60/90/32 cell sites, not an arbitrary rank-two replacement. -/
inductive Site where
  | vertex (d : Dart) | edge (e : Edge) | face (f : Polygon)
  deriving DecidableEq, Fintype

/-- Original direction: dart to incident edge to incident polygon (and dart
straight to incident polygon); diagonal coherence will follow from transitivity. -/
def incidence : Site → Site → Prop
  | .vertex v, .vertex w => v = w
  | .vertex v, .edge e => v = (edgeEndpoints e).1 ∨ v = (edgeEndpoints e).2
  | .vertex v, .face f => dartOnFace v f
  | .edge e, .edge e' => e = e'
  | .edge e, .face f => edgeOnFace e f
  | .face f, .face f' => f = f'
  | _, _ => False

instance : PartialOrder Site where
  le := incidence
  le_refl := by
    intro x
    cases x <;> simp [incidence]
  le_trans := by
    intro a b c hab hbc
    cases a <;> cases b <;> cases c <;>
      simp_all [incidence]
    case vertex.edge.face v e f =>
      rcases hab with hv | hv
      · simpa only [hv] using (edgeFace_endpoints e f hbc).1
      · simpa only [hv] using (edgeFace_endpoints e f hbc).2
  le_antisymm := by
    intro a b hab hba
    cases a <;> cases b <;> simp_all [incidence]

/-- Count the actual constructed finite sites rather than postulating 182. -/
theorem vertex_card : Fintype.card Dart = 60 := by decide

theorem edge_card : Fintype.card Edge = 90 := by decide

theorem face_card : Fintype.card Polygon = 32 := by decide

theorem site_card : Fintype.card Site = 182 := by decide

theorem flag_card : Fintype.card (Edge × (Bool × Bool)) = 360 := by decide

/-- All 360 flags have composable actual incidence arrows. -/
def flagTriangle (e : Edge) (endpointSide faceSide : Bool) :
    ComposableArrows Site 2 :=
  let v := if endpointSide then (edgeEndpoints e).2 else (edgeEndpoints e).1
  let f := faceAt e faceSide
  ComposableArrows.mk₂
    (homOfLE (show Site.vertex v ≤ .edge e from by
      change incidence (Site.vertex v) (.edge e)
      cases endpointSide <;> simp [v, incidence]))
    (homOfLE (show Site.edge e ≤ .face f from each_edge_on_faces e faceSide))

/-- Every physical flag has a vertex-edge-face triangle with distinct ranks. -/
theorem flagTriangle_distinct (e : Edge) (i j : Bool) :
    Site.vertex (if i then (edgeEndpoints e).2 else (edgeEndpoints e).1) ≠
      Site.edge e ∧
    Site.edge e ≠ Site.face (faceAt e j) := by
  constructor <;> intro h <;> cases h

#print axioms each_edge_on_faces
#print axioms incidentDart_endpoint
#print axioms edgeFace_endpoints
#print axioms vertex_card
#print axioms edge_card
#print axioms face_card
#print axioms site_card
#print axioms flag_card
#print axioms flagTriangle
end Kuu.F112.Physical
