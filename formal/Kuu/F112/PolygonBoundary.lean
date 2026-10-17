import Kuu.F112.FaceRewrite
import Mathlib.Data.Bool.AllAny

/-!
# F112-B / genuine closed C60 polygon boundaries

This independent, proof-carrying boundary layer enumerates all twelve
original-vertex pentagons and all twenty original-triangle hexagons.
It uses the real old-edge darts and C60 edges from Physical, with no
square-face or Gray proxy. Cyclic adjacency is checked in BOTH
orientations, because an undirected physical edge may be traversed
opposite its chosen dart orientation.

Each 5- or 6-side boundary is verified closed, with distinct actual
vertices/edges and the same genuine polygon incident to every side.
The attached Type-valued corner reductions are distinct raw source
witnesses; this is NOT yet the old F42 complete pasted 2-source,
the F54 rotations, or the F55 3-cell coherence.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000

/-- A concrete inverse of the five physical slots; not an added polygon label. -/
def ringSlot (i : Ring) : Slot :=
  if i = 0 then .s0
  else if i = 1 then .s1
  else if i = 2 then .s2
  else if i = 3 then .s3
  else .s4

theorem slotIndex_ringSlot : ∀ i : Ring, slotIndex (ringSlot i) = i := by
  decide

def polygonSideCount : Polygon → Nat
  | .pentagon _ => 5
  | .hexagon _ => 6

/-- Five successive genuine around-vertex edges; or three actual cross
edges alternating with three actual corner edges of an old triangle. -/
def polygonBoundaryEdges : Polygon → List Edge
  | .pentagon v =>
      [.around ⟨v, .s0⟩, .around ⟨v, .s1⟩,
       .around ⟨v, .s2⟩, .around ⟨v, .s3⟩,
       .around ⟨v, .s4⟩]
  | .hexagon (.top i) =>
      [.cross (.northSpoke i),
       .around ⟨.upper i, .s0⟩,
       .cross (.upperRing i),
       .around ⟨.upper (i + 1), .s4⟩,
       .cross (.northSpoke (i + 1)),
       .around ⟨.north, ringSlot i⟩]
  | .hexagon (.bottom i) =>
      [.cross (.southSpoke i),
       .around ⟨.lower i, .s0⟩,
       .cross (.lowerRing i),
       .around ⟨.lower (i + 1), .s4⟩,
       .cross (.southSpoke (i + 1)),
       .around ⟨.south, ringSlot i⟩]
  | .hexagon (.beltUpper i) =>
      [.cross (.upperRing i),
       .around ⟨.upper (i + 1), .s3⟩,
       .cross (.crossShifted i),
       .around ⟨.lower i, .s2⟩,
       .cross (.crossAligned i),
       .around ⟨.upper i, .s1⟩]
  | .hexagon (.beltLower i) =>
      [.cross (.crossShifted i),
       .around ⟨.lower i, .s1⟩,
       .cross (.lowerRing i),
       .around ⟨.lower (i + 1), .s3⟩,
       .cross (.crossAligned (i + 1)),
       .around ⟨.upper (i + 1), .s2⟩]

/-- The corresponding real dart at each successive corner; the final edge
returns from the last dart to the FIRST dart rather than to a new site. -/
def polygonBoundaryDarts : Polygon → List Dart
  | .pentagon v =>
      [incidentDart v .s0, incidentDart v .s1,
       incidentDart v .s2, incidentDart v .s3,
       incidentDart v .s4]
  | .hexagon (.top i) =>
      [.first (.northSpoke i), .second (.northSpoke i),
       .first (.upperRing i), .second (.upperRing i),
       .second (.northSpoke (i + 1)), .first (.northSpoke (i + 1))]
  | .hexagon (.bottom i) =>
      [.first (.southSpoke i), .second (.southSpoke i),
       .first (.lowerRing i), .second (.lowerRing i),
       .second (.southSpoke (i + 1)), .first (.southSpoke (i + 1))]
  | .hexagon (.beltUpper i) =>
      [.first (.upperRing i), .second (.upperRing i),
       .first (.crossShifted i), .second (.crossShifted i),
       .second (.crossAligned i), .first (.crossAligned i)]
  | .hexagon (.beltLower i) =>
      [.first (.crossShifted i), .second (.crossShifted i),
       .first (.lowerRing i), .second (.lowerRing i),
       .second (.crossAligned (i + 1)), .first (.crossAligned (i + 1))]

/-- Includes the explicit last-to-first adjacency of a closed face. -/
def polygonCyclicDarts (p : Polygon) : List (Dart × Dart) :=
  (polygonBoundaryDarts p).zip
    ((polygonBoundaryDarts p).drop 1 ++ (polygonBoundaryDarts p).take 1)

/-- An actual C60 edge joins two physical darts, independent of the chosen
orientation of the old icosahedral dart and of its around-vertex ordering. -/
def edgeJoins (e : Edge) (v w : Dart) : Prop :=
  edgeEndpoints e = (v, w) ∨ edgeEndpoints e = (w, v)

/-- Explicitly expose computable endpoint-pair equality and disjunction
to the finite boundary verifier; unfolding a def is not automatic for
typeclass instance synthesis. -/
instance edgeJoins_decidable (e : Edge) (v w : Dart) :
    Decidable (edgeJoins e v w) := by
  unfold edgeJoins
  infer_instance

/-- Edge-to-polygon incidence is a finite, COMPUTABLE physical
proposition; use its constructor cases rather than classical choice. -/
instance edgeOnFace_decidable (e : Edge) (p : Polygon) :
    Decidable (edgeOnFace e p) := by
  cases e <;> cases p <;> dsimp [edgeOnFace] <;> infer_instance

/-- Exact finite proposition checked on every one of the 32 genuine
polygons: lengths, no repeated sides/corners, actual adjacency, actual
incidence of EACH edge with the ORIGINAL face, and cyclic closure. -/
def polygonBoundaryValid (p : Polygon) : Prop :=
  (polygonBoundaryEdges p).length = polygonSideCount p ∧
  (polygonBoundaryDarts p).length = polygonSideCount p ∧
  (polygonBoundaryEdges p).Nodup ∧
  (polygonBoundaryDarts p).Nodup ∧
  ((polygonBoundaryEdges p).zip (polygonCyclicDarts p)).all
    (fun x => decide (edgeJoins x.1 x.2.1 x.2.2 ∧ edgeOnFace x.1 p)) = true

instance polygonBoundaryValid_decidable (p : Polygon) :
    Decidable (polygonBoundaryValid p) := by
  unfold polygonBoundaryValid
  infer_instance

theorem everyPentagonBoundary :
    ∀ v : Vertex, polygonBoundaryValid (.pentagon v) := by
  decide

theorem everyHexagonBoundary :
    ∀ t : Triangle, polygonBoundaryValid (.hexagon t) := by
  decide

/-- All real C60 polygons have complete, non-repeating, genuinely
incidental closed boundaries of precisely 5 or 6 actual edges. -/
theorem polygonBoundary_valid (p : Polygon) : polygonBoundaryValid p := by
  cases p with
  | pentagon v => exact everyPentagonBoundary v
  | hexagon t => exact everyHexagonBoundary t

theorem pentagonBoundary_five (v : Vertex) :
    (polygonBoundaryEdges (.pentagon v)).length = 5 :=
  (polygonBoundary_valid (.pentagon v)).1

theorem hexagonBoundary_six (t : Triangle) :
    (polygonBoundaryEdges (.hexagon t)).length = 6 :=
  (polygonBoundary_valid (.hexagon t)).1

/-- Choose only the REAL face of a real boundary edge. The two faces
of an around-edge are still the original distinct pentagon and hexagon. -/
def boundaryFaceSide (e : Edge) (p : Polygon) : Bool :=
  if faceAt e false = p then false else true

def boundaryFaceChoicesValid (p : Polygon) : Prop :=
  (polygonBoundaryEdges p).all
    (fun e => decide (faceAt e (boundaryFaceSide e p) = p)) = true

instance boundaryFaceChoicesValid_decidable (p : Polygon) :
    Decidable (boundaryFaceChoicesValid p) := by
  unfold boundaryFaceChoicesValid
  infer_instance

theorem everyPentagonFaceChoice :
    ∀ v : Vertex, boundaryFaceChoicesValid (.pentagon v) := by
  decide

theorem everyHexagonFaceChoice :
    ∀ t : Triangle, boundaryFaceChoicesValid (.hexagon t) := by
  decide

theorem boundaryFaceChoices_valid (p : Polygon) :
    boundaryFaceChoicesValid p := by
  cases p with
  | pentagon v => exact everyPentagonFaceChoice v
  | hexagon t => exact everyHexagonFaceChoice t

theorem aroundEdge_faces_distinct (v : Vertex) (s : Slot) :
    faceAt (.around ⟨v, s⟩) false ≠
      faceAt (.around ⟨v, s⟩) true := by
  intro h
  cases h

/-- Every traversed physical edge has the two genuine original
dart-to-edge incidences, including when the boundary orientation reverses. -/
theorem edgeJoins_start (e : Edge) (v w : Dart)
    (h : edgeJoins e v w) : Site.vertex v ≤ Site.edge e := by
  change v = (edgeEndpoints e).1 ∨ v = (edgeEndpoints e).2
  rcases h with h | h
  · exact Or.inl (congrArg Prod.fst h).symm
  · exact Or.inr (congrArg Prod.snd h).symm

theorem edgeJoins_finish (e : Edge) (v w : Dart)
    (h : edgeJoins e v w) : Site.vertex w ≤ Site.edge e := by
  change w = (edgeEndpoints e).1 ∨ w = (edgeEndpoints e).2
  rcases h with h | h
  · exact Or.inr (congrArg Prod.snd h).symm
  · exact Or.inl (congrArg Prod.fst h).symm

/-- A side of a polygon is a TWO-leg original physical F69 RAW path;
the original Site is not given a fabricated dart-to-dart arrow. -/
def rawBoundaryStep (e : Edge) (v w : Dart)
    (h : edgeJoins e v w) :
    Zigzag (Site.vertex v) (Site.vertex w) :=
  .forward (edgeJoins_start e v w h)
    (.backward (edgeJoins_finish e v w h) (.nil _))

/-- Extract a PROPOSITIONAL edge incidence and actual cyclic endpoint
join from the computably certified original polygon. This result is usable
as a dependent witness in subsequent F42 source pasting. -/
theorem polygonBoundary_segment_real (p : Polygon)
    (x : Edge × (Dart × Dart))
    (hx : x ∈ (polygonBoundaryEdges p).zip (polygonCyclicDarts p)) :
    edgeJoins x.1 x.2.1 x.2.2 ∧ edgeOnFace x.1 p := by
  have hall :
      ((polygonBoundaryEdges p).zip (polygonCyclicDarts p)).all
        (fun y => decide (edgeJoins y.1 y.2.1 y.2.2 ∧ edgeOnFace y.1 p)) =
          true :=
    (polygonBoundary_valid p).2.2.2.2
  exact (List.all_iff_forall_prop.mp hall) x hx

/-- Every enumerated side selects the specified true polygon itself,
not an arbitrary adjacent label or an observationally collapsed face. -/
theorem boundaryFaceSide_real (p : Polygon) (e : Edge)
    (he : e ∈ polygonBoundaryEdges p) :
    faceAt e (boundaryFaceSide e p) = p :=
  (List.all_iff_forall_prop.mp (boundaryFaceChoices_valid p)) e he

/-- Genuine proof-bearing raw F69 zigzag along ANY of the verified
five/six polygon sides, with both real dart endpoints fixed in the type. -/
def polygonBoundary_rawStep (p : Polygon)
    (x : Edge × (Dart × Dart))
    (hx : x ∈ (polygonBoundaryEdges p).zip (polygonCyclicDarts p)) :
    Zigzag (Site.vertex x.2.1) (Site.vertex x.2.2) :=
  rawBoundaryStep x.1 x.2.1 x.2.2 (polygonBoundary_segment_real p x hx).1

/-- Two genuinely different polygons meet every real C60 physical edge.
In particular adjacent F42 source presentations must never be identified. -/
theorem everyPhysicalEdge_two_distinct_faces :
    ∀ e : Edge, faceAt e false ≠ faceAt e true := by
  decide

/-- Independent Type-valued corner presentations on ALL five or six
genuine sides of the specified polygon. No polygon is identified with
its adjacent face, and the raw proof trees are not quotiented here. -/
def polygonCornerRewrites (p : Polygon) (i : Bool) :
    List (Σ e : Edge, FaceRewrite
      (flagRawTwoStep e i (boundaryFaceSide e p))
      (flagRawDiagonal e i (boundaryFaceSide e p))) :=
  (polygonBoundaryEdges p).map
    (fun e => ⟨e, flagFaceRewrite e i (boundaryFaceSide e p)⟩)

theorem polygonCornerRewrites_length (p : Polygon) (i : Bool) :
    (polygonCornerRewrites p i).length = polygonSideCount p := by
  simpa only [polygonCornerRewrites, List.length_map]
    using (polygonBoundary_valid p).1

#print axioms slotIndex_ringSlot
#print axioms everyPentagonBoundary
#print axioms everyHexagonBoundary
#print axioms polygonBoundary_valid
#print axioms boundaryFaceChoices_valid
#print axioms aroundEdge_faces_distinct
#print axioms edgeJoins_start
#print axioms edgeJoins_finish
#print axioms rawBoundaryStep
#print axioms polygonBoundary_segment_real
#print axioms boundaryFaceSide_real
#print axioms polygonBoundary_rawStep
#print axioms everyPhysicalEdge_two_distinct_faces
#print axioms polygonCornerRewrites_length
end Kuu.F112.Physical
