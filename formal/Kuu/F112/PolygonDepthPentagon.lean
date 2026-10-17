import Kuu.F112.PolygonDepthThreeComparison

/-!
# F112-E7D / physically based double-depth pentagon 3-cell

E7B proves that genuine C60-sector double-Nat-depth bracket routes
erase to original independent E6A raw rotation routes, preserving
every primitive step. E7C constructs the exact typed 3-Hom comparison.

Here we realize BOTH F54-shaped routes through the associahedron
pentagon on four ACTUAL ordered C60 sectors of one polygon, using
depth (0,0) at each leaf. Zero depths are chosen only to make the
two independently proved Nat associativity casts definitionally
canonical; the physically distinct sector witnesses remain intact.

The two original raw routes have 3 and 2 elementary rotations.
The typed E7B erasures are proved to be the EXACT E6A long/short
words, enabling the independently given E6B pentagon generator to
be transported to an authentic, correctly globular E7C 3-arrow.
This is a SOURCE-LEVEL witness, not equality by numerical charge
and not a claim about historical Blocks or old F55 source equivalence.

The extension from these zero-depth physical witnesses to arbitrary
independent Nat weights, with all old F19/F28 depth casts and F55
coherence, remains a separate open problem.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
noncomputable section

/-- One certified REAL polygon sector with zero initial depths.
The two axes are still separate type indices. -/
def polygonZeroDepthLeaf (p : Polygon) (i : PolygonBoundarySector p) :
    PolygonDepthTree p 0 0 :=
  polygonDepthLeafAt p i 0 0

/-- A physical boundary sector among the first four real sides. -/
def polygonZeroDepthPhysicalLeaf (p : Polygon) (i : Fin 4) :
    PolygonDepthTree p 0 0 :=
  polygonZeroDepthLeaf p (firstFourPolygonSector p i)

/-- Genuine dependent THREE-rotation path between correctly typed
binary brackets on four physical-sector-carrying depth trees. -/
def polygonZeroDepthPentagonLong {p : Polygon}
    (a b c d : PolygonDepthTree p 0 0) :
    PolygonDepthRoute p
      (.node (.node (.node a b) c) d)
      (.node a (.node b (.node c d))) :=
  .trans
    (.trans
      (.leftContext (.assoc a b c) d)
      (.assoc a (.node b c) d))
    (.rightContext a (.assoc b c d))

/-- The alternative original TWO-rotation path, exactly parallel
to the three-rotation path at both DEPENDENT depth endpoints. -/
def polygonZeroDepthPentagonShort {p : Polygon}
    (a b c d : PolygonDepthTree p 0 0) :
    PolygonDepthRoute p
      (.node (.node (.node a b) c) d)
      (.node a (.node b (.node c d))) :=
  .trans
    (.assoc (.node a b) c d)
    (.assoc a b (.node c d))

theorem polygonZeroDepthPentagonLong_count {p : Polygon}
    (a b c d : PolygonDepthTree p 0 0) :
    (polygonZeroDepthPentagonLong a b c d).rotationCount = 3 := by
  rfl

theorem polygonZeroDepthPentagonShort_count {p : Polygon}
    (a b c d : PolygonDepthTree p 0 0) :
    (polygonZeroDepthPentagonShort a b c d).rotationCount = 2 := by
  rfl

/-- Raw proof relevance survives both explicit Nat axes. No
identity or shortcut silently identifies the different routes. -/
theorem polygonZeroDepthPentagonLong_ne_short {p : Polygon}
    (a b c d : PolygonDepthTree p 0 0) :
    polygonZeroDepthPentagonLong a b c d ≠
      polygonZeroDepthPentagonShort a b c d := by
  intro h
  have hc := congrArg PolygonDepthRoute.rotationCount h
  rw [polygonZeroDepthPentagonLong_count,
    polygonZeroDepthPentagonShort_count] at hc
  exact (by decide : (3 : Nat) ≠ 2) hc

/-- The three-step dependent route erases to the EXACT original
E6A freely generated sector bracket route, not merely a same-count
or same-charge proxy. -/
theorem polygonZeroDepthPentagonLong_erased {p : Polygon}
    (a b c d : PolygonDepthTree p 0 0) :
    (polygonZeroDepthPentagonLong a b c d).toBracketRoute =
      polygonBracketPentagonLong a.erase b.erase c.erase d.erase := by
  rfl

/-- The two-step dependent route erases to exactly its ORIGINAL
E6A short bracket-route proof tree. -/
theorem polygonZeroDepthPentagonShort_erased {p : Polygon}
    (a b c d : PolygonDepthTree p 0 0) :
    (polygonZeroDepthPentagonShort a b c d).toBracketRoute =
      polygonBracketPentagonShort a.erase b.erase c.erase d.erase := by
  rfl

/-- An ACTUAL E6B raw pentagon 3-source term on the exact erasures
of our two distinct, correctly typed E7B routes. This is not
constructed merely from the fact that both have some common grade. -/
def polygonZeroDepthPentagonRawCell {p : Polygon}
    (a b c d : PolygonDepthTree p 0 0) :
    PolygonBracketCell p
      (polygonZeroDepthPentagonLong a b c d).toBracketRoute
      (polygonZeroDepthPentagonShort a b c d).toBracketRoute := by
  rw [polygonZeroDepthPentagonLong_erased,
    polygonZeroDepthPentagonShort_erased]
  exact .pentagon a.erase b.erase c.erase d.erase

/-- Its honest E7C typed 3-Hom arrow: both dual-depth endpoint
trees are exactly those of the two verified physical E7B routes. -/
def polygonZeroDepthPentagonThreeHom {p : Polygon}
    (a b c d : PolygonDepthTree p 0 0) :
    PolygonDepthThreeHom
      (polygonZeroDepthPentagonLong a b c d)
      (polygonZeroDepthPentagonShort a b c d) :=
  polygonDepthThreeOf (polygonZeroDepthPentagonRawCell a b c d)

/-- The SAME genuine C60 north pentagon has four original
consecutive sector witnesses at depth (0,0) in BOTH axes. -/
def northZeroDepthPentagonThreeHom :
    PolygonDepthThreeHom
      (polygonZeroDepthPentagonLong
        (polygonZeroDepthPhysicalLeaf (.pentagon .north) 0)
        (polygonZeroDepthPhysicalLeaf (.pentagon .north) 1)
        (polygonZeroDepthPhysicalLeaf (.pentagon .north) 2)
        (polygonZeroDepthPhysicalLeaf (.pentagon .north) 3))
      (polygonZeroDepthPentagonShort
        (polygonZeroDepthPhysicalLeaf (.pentagon .north) 0)
        (polygonZeroDepthPhysicalLeaf (.pentagon .north) 1)
        (polygonZeroDepthPhysicalLeaf (.pentagon .north) 2)
        (polygonZeroDepthPhysicalLeaf (.pentagon .north) 3)) :=
  polygonZeroDepthPentagonThreeHom _ _ _ _

/-- Unlike a unit, this truly constructed raw C60 pentagon
generator has the nonzero FIRST native charge coordinate. -/
theorem northZeroDepthPentagonThreeHom_charge :
    (polygonDepthThreeEval northZeroDepthPentagonThreeHom).1.1 =
      (1 : Int) := by
  rfl

#print axioms polygonZeroDepthPentagonLong
#print axioms polygonZeroDepthPentagonShort
#print axioms polygonZeroDepthPentagonLong_count
#print axioms polygonZeroDepthPentagonShort_count
#print axioms polygonZeroDepthPentagonLong_ne_short
#print axioms polygonZeroDepthPentagonLong_erased
#print axioms polygonZeroDepthPentagonShort_erased
#print axioms polygonZeroDepthPentagonRawCell
#print axioms polygonZeroDepthPentagonThreeHom
#print axioms northZeroDepthPentagonThreeHom_charge
end
end Kuu.F112.Physical
