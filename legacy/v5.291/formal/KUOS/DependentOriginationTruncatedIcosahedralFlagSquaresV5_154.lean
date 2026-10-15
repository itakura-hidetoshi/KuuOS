import KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86

namespace KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154

open KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86

set_option autoImplicit false
noncomputable section

/-!
# F57-A / v5.154 — actual C60 edge-flag incidence squares for higher pasting

The earlier v3.83–v3.90 original KuuOS truncated-icosahedral
formalization already contains a real 60-vertex/90-edge/32-face
5.6.6 incidence carrier, all twelve actual closed five-edge
pentagonal boundaries and all twenty six-edge hexagonal boundaries.

The ordinary C60 surface has NO quadrilateral faces. A legitimate
geometric SQUARE for higher pasting must therefore be constructed
in a different, explicitly defined incidence presentation, not
invented as a quadrilateral face of the original 1-skeleton.

For each of the original ninety truncated edges, there are exactly
two DISTINCT endpoint darts and two DISTINCT incident polygonal
faces. The four vertex–face flags form a genuine nondegenerate
K_{2,2} incidence square in the vertex/face bipartite flag graph.
An around-vertex truncated edge lies between a genuine original
pentagonal face and a genuine original hexagonal face. Thus each
actual closed pentagon boundary can be equipped with five
consecutive edge-local incidence square witnesses.

These are concrete finite geometric square/Pentagon PASTING
CARRIERS. No automatic semantic assignment of a C60 incidence
edge to an F55 original F45 LocalRotation or external Gray 3-cell
is claimed: those are separate typed, path-sensitive F57 tasks.
-/

/-- One actual truncated-icosahedral dart is on a face exactly if its
original endpoint lies on the vertex-origin pentagon, or its original
icosahedral edge belongs to the triangle-origin hexagon. A triangle
contains two darts for each of its three edges. -/
def truncatedDartOnSeedFace
    (d : IcosahedralDart) :
    TruncatedIcosahedralSeedFace → Prop
  | .aroundVertex v => d.endpoint = v
  | .fromTriangle t => d.edge ∈ icosahedralFaceEdges t

/-- Genuine computable Decidable instances for the old finite
face-incidence predicates. These are used by kernel-reduced `decide`,
not by `native_decide` or its compiler-trust axiom. -/
instance (d : IcosahedralDart) (f : TruncatedIcosahedralSeedFace) :
    Decidable (truncatedDartOnSeedFace d f) := by
  cases f with
  | aroundVertex v =>
      change Decidable (d.endpoint = v)
      infer_instance
  | fromTriangle t =>
      change Decidable (d.edge ∈ icosahedralFaceEdges t)
      infer_instance

/-- A genuine truncated edge belongs to a seed face if BOTH of its
actual endpoint darts lie on that face. This is the precise local
edge/face incidence relation for the original C60 construction. -/
def truncatedEdgeOnSeedFace
    (e : TruncatedIcosahedralEdge)
    (f : TruncatedIcosahedralSeedFace) : Prop :=
  truncatedDartOnSeedFace (truncatedIcosahedralEdgeEndpoints e).1 f ∧
    truncatedDartOnSeedFace (truncatedIcosahedralEdgeEndpoints e).2 f

instance (e : TruncatedIcosahedralEdge)
    (f : TruncatedIcosahedralSeedFace) :
    Decidable (truncatedEdgeOnSeedFace e f) := by
  unfold truncatedEdgeOnSeedFace
  infer_instance

/-- Executable finite list of all faces adjacent to a truncated edge,
not a merely asserted global combinatorial incidence count. -/
def truncatedEdgeIncidentFaceSet
    (e : TruncatedIcosahedralEdge) :
    Finset TruncatedIcosahedralSeedFace :=
  Finset.univ.filter (fun f => truncatedEdgeOnSeedFace e f)

/-- All ninety REAL truncated edges each have exactly two incident
polygonal faces, checked on the existing full finite incidence seed. -/
theorem truncatedEdgeIncidentFaceSet_card :
    ∀ e : TruncatedIcosahedralEdge,
      (truncatedEdgeIncidentFaceSet e).card = 2 := by
  decide

/-- Every genuine truncated edge has two different endpoint darts,
including each of the thirty cross and sixty around-vertex edges. -/
theorem truncatedEdgeEndpoints_ne :
    ∀ e : TruncatedIcosahedralEdge,
      (truncatedIcosahedralEdgeEndpoints e).1 ≠
        (truncatedIcosahedralEdgeEndpoints e).2 := by
  decide

/-- Every genuine truncated edge has two distinct faces which are
each incident at BOTH endpoint darts. This supplies actual four
maximal flags at each C60 edge, not just an arithmetic 4×90 count. -/
theorem truncatedEdgeTwoIncidentFaces :
    ∀ e : TruncatedIcosahedralEdge,
      ∃ firstFace secondFace : TruncatedIcosahedralSeedFace,
        firstFace ≠ secondFace ∧
        truncatedEdgeOnSeedFace e firstFace ∧
        truncatedEdgeOnSeedFace e secondFace := by
  intro e
  classical
  obtain ⟨f₀, f₁, hne, hfaces⟩ :=
    Finset.card_eq_two.mp (truncatedEdgeIncidentFaceSet_card e)
  have h₀ : f₀ ∈ truncatedEdgeIncidentFaceSet e := by
    rw [hfaces]
    simp
  have h₁ : f₁ ∈ truncatedEdgeIncidentFaceSet e := by
    rw [hfaces]
    simp
  exact ⟨f₀, f₁, hne,
    (Finset.mem_filter.mp h₀).2, (Finset.mem_filter.mp h₁).2⟩

/-- A REAL incidence square around an actual C60 edge:
two different endpoint vertices times two different incident faces.
All four vertex/face incidences are explicitly certified. -/
structure TruncatedEdgeFlagSquare
    (e : TruncatedIcosahedralEdge) where
  firstFace : TruncatedIcosahedralSeedFace
  secondFace : TruncatedIcosahedralSeedFace
  faces_ne : firstFace ≠ secondFace
  firstIncident : truncatedEdgeOnSeedFace e firstFace
  secondIncident : truncatedEdgeOnSeedFace e secondFace
  endpoints_ne :
    (truncatedIcosahedralEdgeEndpoints e).1 ≠
      (truncatedIcosahedralEdgeEndpoints e).2

/-- Construct a genuine nondegenerate edge incidence square from
the EXISTING ninety-edge combinatorial C60 model. -/
noncomputable def truncatedEdgeFlagSquare
    (e : TruncatedIcosahedralEdge) : TruncatedEdgeFlagSquare e :=
  let f₀ := Classical.choose (truncatedEdgeTwoIncidentFaces e)
  let hf₀ := Classical.choose_spec (truncatedEdgeTwoIncidentFaces e)
  let f₁ := Classical.choose hf₀
  let hf₁ := Classical.choose_spec hf₀
  {
    firstFace := f₀
    secondFace := f₁
    faces_ne := hf₁.1
    firstIncident := hf₁.2.1
    secondIncident := hf₁.2.2
    endpoints_ne := truncatedEdgeEndpoints_ne e
  }

/-- One of two ACTUAL vertex corners of the fixed edge. -/
def TruncatedEdgeFlagSquare.vertex
    {e : TruncatedIcosahedralEdge}
    (_square : TruncatedEdgeFlagSquare e) : Bool → IcosahedralDart
  | false => (truncatedIcosahedralEdgeEndpoints e).1
  | true => (truncatedIcosahedralEdgeEndpoints e).2

/-- One of two ACTUAL adjacent polygonal faces. -/
def TruncatedEdgeFlagSquare.face
    {e : TruncatedIcosahedralEdge}
    (square : TruncatedEdgeFlagSquare e) :
    Bool → TruncatedIcosahedralSeedFace
  | false => square.firstFace
  | true => square.secondFace

/-- The four corner flags are each genuinely incident in the
original C60 truncated-icosahedral finite face lattice. -/
theorem TruncatedEdgeFlagSquare.corner_incident
    {e : TruncatedIcosahedralEdge}
    (square : TruncatedEdgeFlagSquare e)
    (i j : Bool) :
    truncatedDartOnSeedFace (square.vertex i) (square.face j) := by
  cases i with
  | false =>
      cases j with
      | false => exact square.firstIncident.1
      | true => exact square.secondIncident.1
  | true =>
      cases j with
      | false => exact square.firstIncident.2
      | true => exact square.secondIncident.2

/-- The four REAL flags in the C60 incidence square are pairwise
distinct. Their square is NOT an invented four-sided C60 face. -/
theorem TruncatedEdgeFlagSquare.corner_injective
    {e : TruncatedIcosahedralEdge}
    (square : TruncatedEdgeFlagSquare e) :
    Function.Injective
      (fun ij : Bool × Bool => (square.vertex ij.1, square.face ij.2)) := by
  intro ⟨i, j⟩ ⟨k, l⟩ h
  have hv := congrArg Prod.fst h
  have hf := congrArg Prod.snd h
  have hn := square.endpoints_ne
  have hm := square.faces_ne
  cases i <;> cases j <;> cases k <;> cases l <;>
    simp_all [TruncatedEdgeFlagSquare.vertex, TruncatedEdgeFlagSquare.face]

/-- EVERY around-vertex truncated edge lies on the exact original
pentagonal face centered at that vertex; both endpoint darts
are supported by the original v3.85 cyclic incidence theorems. -/
theorem aroundEdge_incident_pentagon
    (a : TruncatedIcosahedralAroundEdge) :
    truncatedEdgeOnSeedFace (.around a) (.aroundVertex a.center) := by
  exact ⟨truncatedIcosahedralAroundEdge_first_endpoint_center a,
    truncatedIcosahedralAroundEdge_second_endpoint_center a⟩

/-- Every one of the sixty around-vertex edges lies ALSO on an
actual triangle-origin hexagon. Hence this is really an adjacent
pentagon/hexagon shared boundary, not just a geometric analogy. -/
theorem aroundEdge_incident_hexagon :
    ∀ a : TruncatedIcosahedralAroundEdge,
      ∃ t : IcosahedralFace,
        truncatedEdgeOnSeedFace (.around a) (.fromTriangle t) := by
  decide

/-- The edge-local square next to a pentagon is constructed with
FIRST face exactly the original pentagon, and SECOND face exactly
the neighboring original hexagon. This makes the gluing orientation
explicit instead of using an arbitrary unordered pair of faces. -/
noncomputable def aroundPentagonHexagonSquare
    (a : TruncatedIcosahedralAroundEdge) :
    TruncatedEdgeFlagSquare (.around a) :=
  let t := Classical.choose (aroundEdge_incident_hexagon a)
  let ht := Classical.choose_spec (aroundEdge_incident_hexagon a)
  {
    firstFace := .aroundVertex a.center
    secondFace := .fromTriangle t
    faces_ne := by intro h; cases h
    firstIncident := aroundEdge_incident_pentagon a
    secondIncident := ht
    endpoints_ne := truncatedEdgeEndpoints_ne (.around a)
  }

/-- Each of the original twelve ACTUAL five-edge pentagon boundaries
has a genuine adjacent geometric four-flag square on EACH boundary
edge, sharing exactly that pentagonal face. -/
theorem pentagonBoundary_edge_has_square
    (v : IcosahedralVertex)
    (e : TruncatedIcosahedralEdge)
    (he : e ∈ truncatedIcosahedralPentagonBoundary v) :
    ∃ square : TruncatedEdgeFlagSquare e,
      square.firstFace = .aroundVertex v := by
  obtain ⟨slot, heq⟩ :=
    truncatedIcosahedralPentagonBoundary_center v e he
  subst e
  exact ⟨aroundPentagonHexagonSquare ⟨v, slot⟩, rfl⟩

/-- Existing original pentagonal face boundaries have EXACTLY five
actual edges; their cyclic closing edge is already proved at v3.85. -/
theorem pentagonBoundary_five_edges
    (v : IcosahedralVertex) :
    (truncatedIcosahedralPentagonBoundary v).length = 5 :=
  truncatedIcosahedralPentagonBoundary_length v

#print axioms truncatedEdgeIncidentFaceSet_card
#print axioms truncatedEdgeEndpoints_ne
#print axioms truncatedEdgeTwoIncidentFaces
#print axioms TruncatedEdgeFlagSquare
#print axioms truncatedEdgeFlagSquare
#print axioms TruncatedEdgeFlagSquare.corner_incident
#print axioms TruncatedEdgeFlagSquare.corner_injective
#print axioms aroundEdge_incident_pentagon
#print axioms aroundEdge_incident_hexagon
#print axioms aroundPentagonHexagonSquare
#print axioms pentagonBoundary_edge_has_square
#print axioms pentagonBoundary_five_edges

end
end KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
