import Kuu.F112.KernelEquivalence

/-!
# F112 / genuinely witnessed physical C60 cross-edge zigzags

An overlap between DISTINCT old physical edges exists only with an actual
original 60/90/32 site incident to both. A selected real common original
polygon or dart yields precisely TWO oriented legs in the raw Site zigzag.
The genuine old Site poset is NOT extended with direct edge-to-edge arrows.
All finite chains of independently witnessed overlaps remain typed.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

def star (e : Edge) (s : Site) : Prop :=
  s ≤ Site.edge e ∨ Site.edge e ≤ s

/-- Proof-carrying *actual physical* overlap between different C60 edges. -/
structure SharedSite (e f : Edge) where
  distinct : e ≠ f
  common : Site
  first : star e common
  second : star f common

/-- Moving from one original physical edge to an actual common original
cell requires only a formal reversal when the original order runs backward. -/
def edgeToCommon (e : Edge) (s : Site) (h : star e s) :
    Zigzag (Site.edge e) s := by
  classical
  by_cases hs : s ≤ Site.edge e
  · exact .backward hs (.nil s)
  · exact .forward (h.resolve_left hs) (.nil s)

def commonToEdge (e : Edge) (s : Site) (h : star e s) :
    Zigzag s (Site.edge e) := by
  classical
  by_cases hs : s ≤ Site.edge e
  · exact .forward hs (.nil _)
  · exact .backward (h.resolve_left hs) (.nil _)

/-- Exactly the two original incidence legs via the witnessed common site. -/
def crossEdgeRaw {e f : Edge} (W : SharedSite e f) :
    Zigzag (Site.edge e) (Site.edge f) :=
  append (edgeToCommon e W.common W.first)
    (commonToEdge f W.common W.second)

/-- No direct arrow between DIFFERENT original physical edge sites exists
in the authentic physical incidence category, despite their raw zigzag. -/
theorem no_original_direct_edge_arrow {e f : Edge} (hne : e ≠ f) :
    ¬ Nonempty (Site.edge e ⟶ Site.edge f) := by
  rintro ⟨g⟩
  have h := leOfHom g
  change incidence (Site.edge e) (Site.edge f) at h
  exact hne h

/-- A concrete distinct-edge witness at the actual north pentagon: two
different around-vertex edges share its genuinely constructed face. -/
def northPentagonOverlap :
    SharedSite
      (.around ⟨.north, .s0⟩)
      (.around ⟨.north, .s1⟩) where
  distinct := by decide
  common := Site.face (Polygon.pentagon .north)
  first := Or.inr (by
    change edgeOnFace (Edge.around ⟨Vertex.north, Slot.s0⟩)
      (Polygon.pentagon Vertex.north)
    rfl)
  second := Or.inr (by
    change edgeOnFace (Edge.around ⟨Vertex.north, Slot.s1⟩)
      (Polygon.pentagon Vertex.north)
    rfl)

theorem northPentagonOriginalArrow_absent :
    ¬ Nonempty
      ((Site.edge (.around ⟨.north, .s0⟩)) ⟶
        (Site.edge (.around ⟨.north, .s1⟩))) :=
  no_original_direct_edge_arrow northPentagonOverlap.distinct

/-- A formal reverse arrow *already exists* in the raw Zigzag category.
A site-preserving functor to the unlocalized original incidence poset would
therefore fabricate the forbidden reverse physical incidence. -/
theorem no_site_preserving_raw_to_original
    (F : ZigzagSite ⥤ Site)
    (hF : ∀ s : Site, F.obj ⟨s⟩ = s) : False := by
  let e : Edge := .cross (.northSpoke 0)
  let v : Dart := flagVertex e false
  have hv : Site.vertex v ≤ Site.edge e := flag_vertex_edge e false
  have rev : (⟨Site.edge e⟩ : ZigzagSite) ⟶
      (⟨Site.vertex v⟩ : ZigzagSite) :=
    backward (homOfLE hv)
  have h := leOfHom (F.map rev)
  rw [hF (Site.edge e), hF (Site.vertex v)] at h
  change False at h
  exact h

/-- Only actual physically witnessed overlaps become generating arrows.
Composing arbitrary overlap witnesses requires the freely generated path
category and does NOT invent new arrows of the original Site category. -/
instance : Quiver Edge := ⟨SharedSite⟩

def witnessedOverlapPrefunctor : Edge ⥤q ZigzagSite where
  obj e := ⟨Site.edge e⟩
  map := fun {_ _} w => crossEdgeRaw w

def witnessedOverlapPaths : Paths Edge ⥤ ZigzagSite :=
  Paths.lift witnessedOverlapPrefunctor

/-- Physical overlap paths factor into the genuine ORIGINAL incidence
localization by previously proved genuine finite zigzag interpretation. -/
def witnessedPathLocalization : Paths Edge ⥤ PhysicalLocalization :=
  witnessedOverlapPaths ⋙ zigzagLocalizationFunctor

#print axioms no_original_direct_edge_arrow
#print axioms northPentagonOverlap
#print axioms northPentagonOriginalArrow_absent
#print axioms no_site_preserving_raw_to_original
#print axioms witnessedOverlapPaths
#print axioms witnessedPathLocalization
end
end Kuu.F112.Physical
