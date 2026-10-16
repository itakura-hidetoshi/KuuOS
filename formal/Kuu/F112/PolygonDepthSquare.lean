import Kuu.F112.PolygonDepthPentagon

/-!
# F112-E7E / genuine C60 dual-depth disjoint-rotation square

E7D proved a complete, correctly globular F55-shaped pentagon
3-generator on genuine four C60 sectors in the independent dual-Nat
depth source (at the canonical zero-depth specialization).

This file proves the OTHER independent basic F55-shaped 3-generator:
two disjoint contextual binary reassociations, left-first and
right-first, on SIX genuine polygon sectors. Their dependent raw
routes are distinct, their exact E7B erasures match E6A's two
original bracket square routes, and the actual E6B nine-constructor
disjointSquare raw term produces a correctly typed E7C 3-arrow.
The complete E6C integer/phase shadow remains nontrivial.

Zero-depth specialization makes the two original Nat associativity
casts computationally canonical; it does not identify distinct
physical polygon sectors, raw routes, or the old historical F55 source.

Historical F19/F28 Blocks, arbitrary nonzero-depth five/six-sector
pasting and original F55/E6 equivalence are NOT claimed.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
noncomputable section

/-- First perform the left associator on one disjoint triple,
then the right associator on another; both retain original
C60 sectors and BOTH independent natural depth axes. -/
def polygonZeroDepthSquareLeftFirst {p : Polygon}
    (a b c d e f : PolygonDepthTree p 0 0) :
    PolygonDepthRoute p
      (.node (.node (.node a b) c) (.node (.node d e) f))
      (.node (.node a (.node b c)) (.node d (.node e f))) :=
  .trans
    (.leftContext (.assoc a b c) (.node (.node d e) f))
    (.rightContext (.node a (.node b c)) (.assoc d e f))

/-- The genuinely different right-first order of two disjoint
original rotations on the SAME six typed physical sector leaves. -/
def polygonZeroDepthSquareRightFirst {p : Polygon}
    (a b c d e f : PolygonDepthTree p 0 0) :
    PolygonDepthRoute p
      (.node (.node (.node a b) c) (.node (.node d e) f))
      (.node (.node a (.node b c)) (.node d (.node e f))) :=
  .trans
    (.rightContext (.node (.node a b) c) (.assoc d e f))
    (.leftContext (.assoc a b c) (.node d (.node e f)))

theorem polygonZeroDepthSquareLeftFirst_count {p : Polygon}
    (a b c d e f : PolygonDepthTree p 0 0) :
    (polygonZeroDepthSquareLeftFirst a b c d e f).rotationCount = 2 := by
  rfl

theorem polygonZeroDepthSquareRightFirst_count {p : Polygon}
    (a b c d e f : PolygonDepthTree p 0 0) :
    (polygonZeroDepthSquareRightFirst a b c d e f).rotationCount = 2 := by
  rfl

/-- The original E6A left-first source is preserved as the EXACT
typed erasure of the new dual-depth raw route, not just its count. -/
theorem polygonZeroDepthSquareLeftFirst_erased {p : Polygon}
    (a b c d e f : PolygonDepthTree p 0 0) :
    (polygonZeroDepthSquareLeftFirst a b c d e f).toBracketRoute =
      polygonBracketSquareLeftFirst
        (PolygonBracketRotation.assoc a.erase b.erase c.erase)
        (PolygonBracketRotation.assoc d.erase e.erase f.erase) := by
  rfl

/-- Exact erasure of the other contextual order, keeping its
original two-step source grammar and six actual physical sectors. -/
theorem polygonZeroDepthSquareRightFirst_erased {p : Polygon}
    (a b c d e f : PolygonDepthTree p 0 0) :
    (polygonZeroDepthSquareRightFirst a b c d e f).toBracketRoute =
      polygonBracketSquareRightFirst
        (PolygonBracketRotation.assoc a.erase b.erase c.erase)
        (PolygonBracketRotation.assoc d.erase e.erase f.erase) := by
  rfl

/-- Even though both have two actual rotations and common endpoints,
the two dependent source proof trees do NOT become raw equal. -/
theorem polygonZeroDepthSquareLeft_ne_right {p : Polygon}
    (a b c d e f : PolygonDepthTree p 0 0) :
    polygonZeroDepthSquareLeftFirst a b c d e f ≠
      polygonZeroDepthSquareRightFirst a b c d e f := by
  intro h
  have hraw := congrArg PolygonDepthRoute.toBracketRoute h
  rw [polygonZeroDepthSquareLeftFirst_erased,
    polygonZeroDepthSquareRightFirst_erased] at hraw
  exact (polygonBracketSquareLeft_ne_right
    (PolygonBracketRotation.assoc a.erase b.erase c.erase)
    (PolygonBracketRotation.assoc d.erase e.erase f.erase)) hraw

/-- The original independent E6B F55-like disjointSquare 3-PROOF
matches our two EXACT dependent source route boundaries. -/
def polygonZeroDepthSquareRawCell {p : Polygon}
    (a b c d e f : PolygonDepthTree p 0 0) :
    PolygonBracketCell p
      (polygonZeroDepthSquareLeftFirst a b c d e f).toBracketRoute
      (polygonZeroDepthSquareRightFirst a b c d e f).toBracketRoute := by
  rw [polygonZeroDepthSquareLeftFirst_erased,
    polygonZeroDepthSquareRightFirst_erased]
  exact .disjointSquare
    (PolygonBracketRotation.assoc a.erase b.erase c.erase)
    (PolygonBracketRotation.assoc d.erase e.erase f.erase)

/-- A genuinely source-grounded, proof-relevant 3-Hom on the typed
two-axis rotation routes, not a phase-only or numerical-grade lift. -/
def polygonZeroDepthSquareThreeHom {p : Polygon}
    (a b c d e f : PolygonDepthTree p 0 0) :
    PolygonDepthThreeHom
      (polygonZeroDepthSquareLeftFirst a b c d e f)
      (polygonZeroDepthSquareRightFirst a b c d e f) :=
  polygonDepthThreeOf (polygonZeroDepthSquareRawCell a b c d e f)

/-- The actual six original boundary sectors of a true C60 hexagon
give SIX different geometrical leaf indices in the same source. -/
def polygonZeroDepthHexagonLeaf (t : Triangle) (i : Fin 6) :
    PolygonDepthTree (.hexagon t) 0 0 :=
  polygonZeroDepthLeaf (.hexagon t)
    ⟨i, by simp [polygonSideCount]⟩

/-- Concrete northern top C60 hexagon disjoint-rotation 3-cell:
real physical sector indices 0,1,2 and 3,4,5 are disjoint. -/
def northTopHexagonZeroDepthSquare :
    PolygonDepthThreeHom
      (polygonZeroDepthSquareLeftFirst
        (polygonZeroDepthHexagonLeaf (.top 0) 0)
        (polygonZeroDepthHexagonLeaf (.top 0) 1)
        (polygonZeroDepthHexagonLeaf (.top 0) 2)
        (polygonZeroDepthHexagonLeaf (.top 0) 3)
        (polygonZeroDepthHexagonLeaf (.top 0) 4)
        (polygonZeroDepthHexagonLeaf (.top 0) 5))
      (polygonZeroDepthSquareRightFirst
        (polygonZeroDepthHexagonLeaf (.top 0) 0)
        (polygonZeroDepthHexagonLeaf (.top 0) 1)
        (polygonZeroDepthHexagonLeaf (.top 0) 2)
        (polygonZeroDepthHexagonLeaf (.top 0) 3)
        (polygonZeroDepthHexagonLeaf (.top 0) 4)
        (polygonZeroDepthHexagonLeaf (.top 0) 5)) :=
  polygonZeroDepthSquareThreeHom _ _ _ _ _ _

/-- Its independently defined exchange phase is NONZERO even
though the two raw routes have the same physical endpoints. -/
theorem northTopHexagonZeroDepthSquare_phase_nonzero :
    (polygonDepthThreeEval northTopHexagonZeroDepthSquare).2 ≠
      (0 : ZMod 2) := by
  decide

/-- This genuine source-grounded square retains the second native
integer generator charge ONE, not an erased flat/Boolean proxy. -/
theorem northTopHexagonZeroDepthSquare_charge :
    (polygonDepthThreeEval northTopHexagonZeroDepthSquare).1.2 =
      (1 : Int) := by
  rfl

#print axioms polygonZeroDepthSquareLeftFirst_count
#print axioms polygonZeroDepthSquareRightFirst_count
#print axioms polygonZeroDepthSquareLeftFirst_erased
#print axioms polygonZeroDepthSquareRightFirst_erased
#print axioms polygonZeroDepthSquareLeft_ne_right
#print axioms polygonZeroDepthSquareRawCell
#print axioms polygonZeroDepthSquareThreeHom
#print axioms northTopHexagonZeroDepthSquare_phase_nonzero
#print axioms northTopHexagonZeroDepthSquare_charge
end
end Kuu.F112.Physical
