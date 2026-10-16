import Kuu.F112.PolygonRotationNaturality

/-!
# F112-E5A / independent proof-relevant rotation 3-cells

This construction starts from the genuine C60 typed E4 rotation 2-squares.
A physical generator is assigned its OWN independent integer coordinate
(labelled by the ACTUAL polygon and the two certified boundary indices).
We retain the unquotiented Type-valued E4 2-source: no two raw proof trees
are identified by the degree map.

We construct a typed 3-Hom as the kernel equality of this explicit
generator-degree evaluation. Vertical composition, whiskering,
horizontal composition and interchange are PROVED, using additive
commutativity and actual E4 source boundaries, rather than assumed as
laws in an axiomatized 3-category. The 3-Homs form a THIN category,
while the underlying E4 two-cells remain distinct raw inhabitants.

This is a newly defined INDEPENDENT degree-kernel 3-Hom, NOT the
original historical F55 PresentedCell, its integer/phase evaluator,
or its nonlift/curvature/Gray exchange semantics. In particular this
does not prove completeness of F112 or any old-F55 comparison.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

/-- One independent coordinate for EACH actual polygon/basepoint pair.
The index depends on the genuine C60 polygon, not on a proxy Bool. -/
abbrev RotationGeneratorLabel := Polygon × Nat × Nat
abbrev RotationGeneratorDegree := RotationGeneratorLabel → Int

def rotationGeneratorUnit (p : Polygon) (k l : Nat) :
    RotationGeneratorDegree :=
  fun j => if j = (p, k, l) then 1 else 0

/-- Evaluator on the genuinely proof-relevant E4 2-square grammar.
The degree is additive only by DEFINITION of this new evaluation,
not by any historical phase/charge theorem. -/
def PolygonRotationSquare.degree
    {s t : Site} {q r : Zigzag s t}
    (c : PolygonRotationSquare q r) : RotationGeneratorDegree :=
  match c with
  | .ident _ => fun _ => 0
  | .physical p k l _ _ => rotationGeneratorUnit p k l
  | .inverse c => fun j => -c.degree j
  | .vertical c d => fun j => c.degree j + d.degree j
  | .leftContext _ c => c.degree
  | .rightContext c _ => c.degree

/-- A properly globular Type-valued kernel 3-Hom. Both source and
target are actual E4 2-cell witnesses with EXACTLY the same pair of
original raw Zigzag 1-boundaries. -/
structure PolygonRotationThreeCell
    {s t : Site} {q r : Zigzag s t}
    (a b : PolygonRotationSquare q r) : Type where
  degree_eq : a.degree = b.degree

/-- At this degree-kernel LEVEL the 3-Homs are thin; this is NOT an
assertion of equality of the original Type-valued raw two-source. -/
instance polygonRotationThreeCell_subsingleton
    {s t : Site} {q r : Zigzag s t}
    {a b : PolygonRotationSquare q r} :
    Subsingleton (PolygonRotationThreeCell a b) := by
  constructor
  intro x y
  cases x
  cases y
  rfl

def PolygonRotationThreeCell.ident
    {s t : Site} {q r : Zigzag s t}
    (a : PolygonRotationSquare q r) :
    PolygonRotationThreeCell a a :=
  ⟨rfl⟩

def PolygonRotationThreeCell.inverse
    {s t : Site} {q r : Zigzag s t}
    {a b : PolygonRotationSquare q r}
    (f : PolygonRotationThreeCell a b) :
    PolygonRotationThreeCell b a :=
  ⟨f.degree_eq.symm⟩

def PolygonRotationThreeCell.vertical
    {s t : Site} {q r : Zigzag s t}
    {a b c : PolygonRotationSquare q r}
    (f : PolygonRotationThreeCell a b)
    (g : PolygonRotationThreeCell b c) :
    PolygonRotationThreeCell a c :=
  ⟨f.degree_eq.trans g.degree_eq⟩

/-- The original E4 raw two-cells are OBJECTS, and their exact
integer-generator-kernel comparisons are categorical 3-arrows.
The unit and associativity follow by proof irrelevance of the
degree equality: no category law is stipulated as an axiom. -/
instance polygonRotationThreeHomCategory
    {s t : Site} (q r : Zigzag s t) :
    Category (PolygonRotationSquare q r) where
  Hom := PolygonRotationThreeCell
  id := PolygonRotationThreeCell.ident
  comp := PolygonRotationThreeCell.vertical
  id_comp := by
    intro a b f
    exact Subsingleton.elim _ _
  comp_id := by
    intro a b f
    exact Subsingleton.elim _ _
  assoc := by
    intro a b c d f g h
    exact Subsingleton.elim _ _

/-- A genuine original F69 word on the LEFT changes neither the
physical generator nor the kernel equality. -/
def PolygonRotationThreeCell.leftContext
    {s t u : Site} (h : Zigzag s t)
    {q r : Zigzag t u} {a b : PolygonRotationSquare q r}
    (f : PolygonRotationThreeCell a b) :
    PolygonRotationThreeCell
      (PolygonRotationSquare.leftContext h a)
      (PolygonRotationSquare.leftContext h b) :=
  ⟨f.degree_eq⟩

/-- The RIGHT raw physical context enjoys the same proved compatibility. -/
def PolygonRotationThreeCell.rightContext
    {s t u : Site} {q r : Zigzag s t}
    {a b : PolygonRotationSquare q r}
    (f : PolygonRotationThreeCell a b) (h : Zigzag t u) :
    PolygonRotationThreeCell
      (PolygonRotationSquare.rightContext a h)
      (PolygonRotationSquare.rightContext b h) :=
  ⟨f.degree_eq⟩

/-- First act on the left original Zigzag interval, THEN on the
right interval: an actual typed E4 pasting expression. -/
def polygonRotationLeftFirst
    {s t u : Site} {q r : Zigzag s t} {v w : Zigzag t u}
    (a : PolygonRotationSquare q r)
    (b : PolygonRotationSquare v w) :
    PolygonRotationSquare (append q v) (append r w) :=
  .vertical (.rightContext a v) (.leftContext r b)

/-- The other physically typed ordering of the very SAME E4 squares. -/
def polygonRotationRightFirst
    {s t u : Site} {q r : Zigzag s t} {v w : Zigzag t u}
    (a : PolygonRotationSquare q r)
    (b : PolygonRotationSquare v w) :
    PolygonRotationSquare (append q v) (append r w) :=
  .vertical (.leftContext q b) (.rightContext a w)

/-- E5-A interchange: both pasted source trees have identical
independently indexed generator degrees, PROVED by integer addition
commutativity (not an imported or axiomatized Gray exchange law). -/
theorem polygonRotationInterchange_degree
    {s t u : Site} {q r : Zigzag s t} {v w : Zigzag t u}
    (a : PolygonRotationSquare q r)
    (b : PolygonRotationSquare v w) :
    (polygonRotationLeftFirst a b).degree =
      (polygonRotationRightFirst a b).degree := by
  funext j
  change a.degree j + b.degree j = b.degree j + a.degree j
  exact add_comm _ _

def polygonRotationInterchange
    {s t u : Site} {q r : Zigzag s t} {v w : Zigzag t u}
    (a : PolygonRotationSquare q r)
    (b : PolygonRotationSquare v w) :
    PolygonRotationThreeCell
      (polygonRotationLeftFirst a b)
      (polygonRotationRightFirst a b) :=
  ⟨polygonRotationInterchange_degree a b⟩

/-- The leading constructor can be inspected without eliminating
the dependent endpoint equations of a raw 2-square. -/
def PolygonRotationSquare.contextTag
    {s t : Site} {q r : Zigzag s t}
    (a : PolygonRotationSquare q r) : Nat :=
  match a with
  | .leftContext _ _ => 1
  | .rightContext _ _ => 2
  | _ => 0

/-- Detect which of the two genuinely different raw whiskerings
begins a vertical paste, independently of the indexed endpoints. -/
def PolygonRotationSquare.firstPastingTag
    {s t : Site} {q r : Zigzag s t}
    (a : PolygonRotationSquare q r) : Nat :=
  match a with
  | .vertical c _ => c.contextTag
  | _ => 0

/-- The two E4 SOURCE pasting words are NOT identical.
The explicit E5 comparison above is really a 3-cell between
different raw two-proof trees, rather than raw proof irrelevance. -/
theorem polygonRotationInterchange_raw_ne
    {s t u : Site} {q r : Zigzag s t} {v w : Zigzag t u}
    (a : PolygonRotationSquare q r)
    (b : PolygonRotationSquare v w) :
    polygonRotationLeftFirst a b ≠ polygonRotationRightFirst a b := by
  intro h
  have ht := congrArg PolygonRotationSquare.firstPastingTag h
  change (2 : Nat) = 1 at ht
  exact (by decide : (2 : Nat) ≠ 1) ht

/-- Horizontal composition of 3-cells is derived from equality of
their two independently indexed generator degrees. -/
def PolygonRotationThreeCell.horizontal
    {s t u : Site} {q r : Zigzag s t} {v w : Zigzag t u}
    {a a' : PolygonRotationSquare q r}
    {b b' : PolygonRotationSquare v w}
    (f : PolygonRotationThreeCell a a')
    (g : PolygonRotationThreeCell b b') :
    PolygonRotationThreeCell
      (polygonRotationLeftFirst a b)
      (polygonRotationLeftFirst a' b') := by
  refine ⟨?_⟩
  funext j
  change a.degree j + b.degree j = a'.degree j + b'.degree j
  rw [congrFun f.degree_eq j, congrFun g.degree_eq j]

/-- The strict horizontal/vertical 3-cell interchange law in the
degree-kernel 3-Hom is a theorem of the constructed category. -/
theorem PolygonRotationThreeCell.horizontal_vertical_interchange
    {s t u : Site} {q r : Zigzag s t} {v w : Zigzag t u}
    {a₀ a₁ a₂ : PolygonRotationSquare q r}
    {b₀ b₁ b₂ : PolygonRotationSquare v w}
    (f : PolygonRotationThreeCell a₀ a₁)
    (f' : PolygonRotationThreeCell a₁ a₂)
    (g : PolygonRotationThreeCell b₀ b₁)
    (g' : PolygonRotationThreeCell b₁ b₂) :
    PolygonRotationThreeCell.horizontal
        (PolygonRotationThreeCell.vertical f f')
        (PolygonRotationThreeCell.vertical g g') =
      PolygonRotationThreeCell.vertical
        (PolygonRotationThreeCell.horizontal f g)
        (PolygonRotationThreeCell.horizontal f' g') := by
  exact Subsingleton.elim _ _

/-- Actual north pentagon E4 proof terms have a canonical new
degree-kernel 3-morphism between two provably different raw terms. -/
def northPentagonRotationUnitThreeCell :
    PolygonRotationThreeCell
      (polygonRotationSquare (.pentagon .north) 0 1
        (by decide) (by decide))
      (polygonRotationSquareWithUnit (.pentagon .north) 0 1
        (by decide) (by decide)) := by
  refine ⟨?_⟩
  funext j
  change rotationGeneratorUnit (.pentagon .north) 0 1 j =
    (0 : Int) + rotationGeneratorUnit (.pentagon .north) 0 1 j
  simp

#print axioms PolygonRotationSquare.degree
#print axioms polygonRotationThreeHomCategory
#print axioms polygonRotationInterchange_degree
#print axioms polygonRotationInterchange
#print axioms polygonRotationInterchange_raw_ne
#print axioms PolygonRotationThreeCell.horizontal_vertical_interchange
#print axioms northPentagonRotationUnitThreeCell
end
end Kuu.F112.Physical
