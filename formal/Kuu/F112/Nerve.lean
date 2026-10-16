import Kuu.F112.Zigzag
import Mathlib.AlgebraicTopology.SimplicialSet.Nerve
import Mathlib.AlgebraicTopology.Quasicategory.StrictSegal

/-!
# Native nerve of the independently reconstructed 60/90/32 C60 incidence

This is the genuine category nerve of physical cell incidence, with all
360 original endpoint-edge-polygon two-simplices. A strict Segal nerve
is a quasicategory, but this does not give an original F42/F54/F55
proof-relevant (infinity,3)-category or global effective descent.
-/

namespace Kuu.F112.Physical
open CategoryTheory Simplicial
set_option autoImplicit false

def incidenceNerve : SSet := CategoryTheory.nerve Site

theorem incidenceNerve_quasicategory :
    SSet.Quasicategory incidenceNerve :=
  SSet.StrictSegal.quasicategory (CategoryTheory.Nerve.strictSegal Site)

/-- Each actual endpoint-face choice selects a true original physical
vertex-edge-face two-simplex, without inserting a new square cell. -/
def actualFlag (i : Edge × (Bool × Bool)) :
    ComposableArrows Site 2 :=
  flagTriangle i.1 i.2.1 i.2.2

theorem actualFlag_distinct (i : Edge × (Bool × Bool)) :
    Site.vertex (if i.2.1 then (edgeEndpoints i.1).2 else (edgeEndpoints i.1).1) ≠
      Site.edge i.1 ∧
    Site.edge i.1 ≠ Site.face (faceAt i.1 i.2.2) :=
  flagTriangle_distinct i.1 i.2.1 i.2.2

/-- Direct physical endpoint-to-face incidence follows from the actual
two original incidence legs and their proved composition law. -/
theorem flag_vertex_face_incidence (e : Edge) (i j : Bool) :
    Site.vertex (if i then (edgeEndpoints e).2 else (edgeEndpoints e).1) ≤
      Site.face (faceAt e j) := by
  have h1 : Site.vertex (if i then (edgeEndpoints e).2 else (edgeEndpoints e).1) ≤
      Site.edge e := by
    change incidence _ _
    cases i <;> simp [incidence]
  have h2 : Site.edge e ≤ Site.face (faceAt e j) :=
    each_edge_on_faces e j
  exact le_trans h1 h2


/-- The two authentic incidence legs compose to the original single
vertex-to-polygon diagonal in the *physical incidence nerve*, even though
their raw zigzag words remain unequal until a declared quotient. -/
theorem flagNerve_diagonal (e : Edge) (i j : Bool) :
    (ConcreteCategory.hom (incidenceNerve.δ 1))
      (flagTriangle e i j) =
    ComposableArrows.mk₁
      (homOfLE (flag_vertex_face_incidence e i j)) := by
  change
    (ConcreteCategory.hom ((CategoryTheory.nerve Site).δ 1))
      (ComposableArrows.mk₂
        (homOfLE (flag_vertex_edge e i))
        (homOfLE (flag_edge_face e j))) =
    ComposableArrows.mk₁
      (homOfLE (flag_vertex_face_incidence e i j))
  rw [CategoryTheory.nerve.δ₁_mk₂_eq]
  exact congrArg ComposableArrows.mk₁ (Subsingleton.elim _ _)

#print axioms incidenceNerve_quasicategory
#print axioms actualFlag_distinct
#print axioms flag_vertex_face_incidence
#print axioms flagNerve_diagonal
end Kuu.F112.Physical
