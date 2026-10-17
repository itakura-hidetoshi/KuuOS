import Kuu.F112.Physical
import Mathlib.CategoryTheory.Groupoid.FreeGroupoidOfCategory
import Mathlib.CategoryTheory.Localization.Predicate

/-!
# Independent F112 / authentic C60 incidence zigzags

The original C60 incidence category has only genuine original arrows.
The *separate* zigzag category freely adjoins forward and formally reversed
legs. A backtrack is nonempty at the raw source and can become an identity
only after a separately constructed exact localization quotient.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

/-- Distinct category of original physical sites with *formal* zigzag arrows. -/
structure ZigzagSite where
  site : Site

/-- Every leg is evidence of a genuine original physical incidence. -/
inductive Zigzag : Site → Site → Type where
  | nil (s : Site) : Zigzag s s
  | forward {s t u : Site} (h : s ≤ t) (rest : Zigzag t u) : Zigzag s u
  | backward {s t u : Site} (h : t ≤ s) (rest : Zigzag t u) : Zigzag s u

def append {s t u : Site} (p : Zigzag s t) (q : Zigzag t u) : Zigzag s u :=
  match p with
  | .nil _ => q
  | .forward h rest => .forward h (append rest q)
  | .backward h rest => .backward h (append rest q)

theorem append_nil_right {s t : Site} (p : Zigzag s t) :
    append p (.nil t) = p := by
  induction p with
  | nil _ => rfl
  | forward h rest ih =>
      change Zigzag.forward h (append rest (.nil _)) = Zigzag.forward h rest
      rw [ih]
  | backward h rest ih =>
      change Zigzag.backward h (append rest (.nil _)) = Zigzag.backward h rest
      rw [ih]

theorem append_assoc {s t u v : Site}
    (p : Zigzag s t) (q : Zigzag t u) (r : Zigzag u v) :
    append (append p q) r = append p (append q r) := by
  induction p with
  | nil _ => rfl
  | forward h rest ih =>
      change Zigzag.forward h (append (append rest q) r) =
        Zigzag.forward h (append rest (append q r))
      rw [ih]
  | backward h rest ih =>
      change Zigzag.backward h (append (append rest q) r) =
        Zigzag.backward h (append rest (append q r))
      rw [ih]

/-- Raw forward/reverse paths form a category WITHOUT path cancellation. -/
instance : Category ZigzagSite where
  Hom X Y := Zigzag X.site Y.site
  id X := .nil X.site
  comp f g := append f g
  id_comp := by intro X Y f; rfl
  comp_id := by intro X Y f; exact append_nil_right f
  assoc := by intro W X Y Z f g h; exact append_assoc f g h

/-- Exactly one existing physical incidence arrow as a forward leg. -/
def forward {s t : Site} (f : s ⟶ t) : Zigzag s t :=
  .forward (leOfHom f) (.nil t)

/-- Its reverse is a NEW formal leg, not a morphism of the original Site. -/
def backward {s t : Site} (f : s ⟶ t) : Zigzag t s :=
  .backward (leOfHom f) (.nil s)

/-- A forward/backward round trip is NOT syntactically the empty path. -/
theorem backtrack_ne_nil {s t : Site} (f : s ⟶ t) :
    append (forward f) (backward f) ≠ Zigzag.nil s := by
  intro h
  cases h


/-- The real 360 flag sites choose actual endpoints of original physical
edges, and their own existing polygonal faces. -/
def flagVertex (e : Edge) (i : Bool) : Dart :=
  if i then (edgeEndpoints e).2 else (edgeEndpoints e).1

theorem flag_vertex_edge (e : Edge) (i : Bool) :
    Site.vertex (flagVertex e i) ≤ Site.edge e := by
  change incidence (Site.vertex (flagVertex e i)) (Site.edge e)
  cases i <;> simp [flagVertex, incidence]

theorem flag_edge_face (e : Edge) (j : Bool) :
    Site.edge e ≤ Site.face (faceAt e j) :=
  each_edge_on_faces e j

/-- The source zigzag keeps both genuine physical incidence legs of a real
C60 triangle, with the actual dart, edge and polygon at their typed boundaries. -/
def flagRawTwoStep (e : Edge) (i j : Bool) :
    Zigzag (Site.vertex (flagVertex e i)) (Site.face (faceAt e j)) :=
  .forward (flag_vertex_edge e i)
    (.forward (flag_edge_face e j) (.nil _))

/-- The real F69 diagonal is a DIFFERENT raw word using the actually
proved transitive physical incidence, not a synthetic bypass. -/
def flagRawDiagonal (e : Edge) (i j : Bool) :
    Zigzag (Site.vertex (flagVertex e i)) (Site.face (faceAt e j)) :=
  .forward (le_trans (flag_vertex_edge e i) (flag_edge_face e j)) (.nil _)

/-- Different numbers of source generators do not become equal before a
specified quotient. This is the raw physical F112-12 obstruction. -/
theorem flagRawTwoStep_ne_diagonal (e : Edge) (i j : Bool) :
    flagRawTwoStep e i j ≠ flagRawDiagonal e i j := by
  intro h
  cases h

/-- A genuinely *new* groupoid completion of the original C60 category. -/
abbrev PhysicalFreeGroupoid := FreeGroupoid Site

theorem physicalFreeGroupoid_isLocalization :
    (FreeGroupoid.of Site).IsLocalization (⊤ : MorphismProperty Site) := by
  infer_instance

abbrev PhysicalLocalization := (⊤ : MorphismProperty Site).Localization

/-- Canonical equivalence by the native Mathlib localization theorem. -/
def physicalFreeGroupoidEquivalence :
    PhysicalFreeGroupoid ≌ PhysicalLocalization :=
  Localization.uniq (FreeGroupoid.of Site)
    ((⊤ : MorphismProperty Site).Q)
    (⊤ : MorphismProperty Site)

def physicalGroupoidComparison :
    (FreeGroupoid.of Site) ⋙ physicalFreeGroupoidEquivalence.functor ≅
      ((⊤ : MorphismProperty Site).Q) :=
  Localization.compUniqFunctor (FreeGroupoid.of Site)
    ((⊤ : MorphismProperty Site).Q)
    (⊤ : MorphismProperty Site)

#print axioms append_nil_right
#print axioms append_assoc
#print axioms backtrack_ne_nil
#print axioms flag_vertex_edge
#print axioms flag_edge_face
#print axioms flagRawTwoStep_ne_diagonal
#print axioms physicalFreeGroupoid_isLocalization
#print axioms physicalFreeGroupoidEquivalence
#print axioms physicalGroupoidComparison
end
end Kuu.F112.Physical
