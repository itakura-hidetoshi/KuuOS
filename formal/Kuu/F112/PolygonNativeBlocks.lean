import Kuu.F112.NativeBlocks

/-!
# F112-E7J / genuine C60 incidence-site categorical Blocks on 180 sides

E7I separately reconstructs the original-shaped two-level grammar of
finite native categorical paths and block subdivisions over ANY
category. We now instantiate it on the ORIGINAL 60/90/32 C60 Site
incidence category rather than on proxy Bool tags or sector names.

For EVERY real side of every physical pentagon/hexagon, there is an
actual original vertex -> edge -> polygon incidence chain. Another
existing original Site arrow goes directly vertex -> polygon by
proved transitivity. We represent them as TWO truly distinct native
arrow words, with TWO vs ONE independent block subdivisions.

Their original categorical composites agree in the genuine thin
C60 incidence category, but their unquotiented path lengths and raw
block counts do NOT coincide. This is precisely why a comparison
at categorical evaluation alone cannot recover original F19/F28
proof-relevant Blocks.

The two blocks axes here are a NEW C60 independent structural model,
not yet the old F19 StrongTrans.Modification and F28 quotient
AxisTrace; those native primitive histories still need a typed bridge.
No old KUOS, Gray, F51 or F77 import is used.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

/-- An actual arrow from the source DART to its true physical
C60 boundary EDGE, certified by original geometric incidence. -/
def polygonSectorVertexEdgeHom (p : Polygon)
    (i : PolygonBoundarySector p) :
    Site.vertex (cyclicBoundaryDart p i.1.val) ⟶
      Site.edge (cyclicBoundaryEdge p i.1.val) :=
  homOfLE (edgeJoins_start
    (cyclicBoundaryEdge p i.1.val)
    (cyclicBoundaryDart p i.1.val)
    (cyclicBoundaryDart p (i.1.val + 1))
    (cyclicBoundarySide_real p i.1 i.2).1)

/-- An actual original F69 incidence arrow from that SAME physical
edge to its actually incident polygon, not to a fabricated face. -/
def polygonSectorEdgeFaceHom (p : Polygon)
    (i : PolygonBoundarySector p) :
    Site.edge (cyclicBoundaryEdge p i.1.val) ⟶ Site.face p :=
  homOfLE (cyclicBoundarySide_real p i.1 i.2).2.1

/-- A genuine two-arrow original C60 categorical path, retaining
the intermediate 90-edge site as a separately typed vertex. -/
def polygonSectorNativeTwoStep (p : Polygon)
    (i : PolygonBoundarySector p) :
    KuuNativePath (Site.vertex (cyclicBoundaryDart p i.1.val))
      (Site.face p) :=
  .snoc
    (KuuNativePath.single (polygonSectorVertexEdgeHom p i))
    (polygonSectorEdgeFaceHom p i)

/-- A DIFFERENT one-arrow native path from the same real source
vertex directly to the same real polygon, by original composition. -/
def polygonSectorNativeDiagonal (p : Polygon)
    (i : PolygonBoundarySector p) :
    KuuNativePath (Site.vertex (cyclicBoundaryDart p i.1.val))
      (Site.face p) :=
  KuuNativePath.single
    (polygonSectorVertexEdgeHom p i ≫ polygonSectorEdgeFaceHom p i)

/-- Two separate categorical block segments, preserving the true
intermediate original physical edge and BOTH original arrows. -/
def polygonSectorTwoBlocks (p : Polygon)
    (i : PolygonBoundarySector p) :
    KuuNativeBlocks (Site.vertex (cyclicBoundaryDart p i.1.val))
      (Site.face p) :=
  .snoc
    (.snoc (.empty _)
      (KuuNativePath.single (polygonSectorVertexEdgeHom p i)))
    (KuuNativePath.single (polygonSectorEdgeFaceHom p i))

/-- One original categorical arrow as ONE subdivision block.
This is source syntax distinct from the two-edge presentation. -/
def polygonSectorOneBlock (p : Polygon)
    (i : PolygonBoundarySector p) :
    KuuNativeBlocks (Site.vertex (cyclicBoundaryDart p i.1.val))
      (Site.face p) :=
  KuuNativeBlocks.singleton (polygonSectorNativeDiagonal p i)

/-- The physical first axis flattens to the EXACT actual
vertex->edge->face native two-step word, without raw cancellation. -/
theorem polygonSectorTwoBlocks_flatten (p : Polygon)
    (i : PolygonBoundarySector p) :
    (polygonSectorTwoBlocks p i).flatten =
      polygonSectorNativeTwoStep p i := by
  simp only [polygonSectorTwoBlocks, polygonSectorNativeTwoStep,
    KuuNativeBlocks.flatten, KuuNativePath.append,
    KuuNativePath.single]

/-- The physical second axis flattens to precisely the actual
direct incidence arrow, with no invented new original Site Hom. -/
theorem polygonSectorOneBlock_flatten (p : Polygon)
    (i : PolygonBoundarySector p) :
    (polygonSectorOneBlock p i).flatten =
      polygonSectorNativeDiagonal p i := by
  simp only [polygonSectorOneBlock, polygonSectorNativeDiagonal,
    KuuNativeBlocks.singleton, KuuNativeBlocks.flatten,
    KuuNativePath.append]

/-- The two original paths retain two and one independent REAL
categorical arrow steps, respectively, before any quotient. -/
theorem polygonSectorTwoStep_length (p : Polygon)
    (i : PolygonBoundarySector p) :
    (polygonSectorNativeTwoStep p i).length = 2 := by
  rfl

theorem polygonSectorDiagonal_length (p : Polygon)
    (i : PolygonBoundarySector p) :
    (polygonSectorNativeDiagonal p i).length = 1 := by
  rfl

/-- The physical vertex-edge-polygon path is NOT the diagonal
as original finite category path syntax for ANY real C60 sector. -/
theorem polygonSectorTwoStep_ne_diagonal (p : Polygon)
    (i : PolygonBoundarySector p) :
    polygonSectorNativeTwoStep p i ≠
      polygonSectorNativeDiagonal p i := by
  intro h
  have hc := congrArg KuuNativePath.length h
  rw [polygonSectorTwoStep_length,
    polygonSectorDiagonal_length] at hc
  exact (by decide : (2 : Nat) ≠ 1) hc

/-- The original F40-style independent block subdivisions contain
precisely two vs one physical block; both are genuine C60 paths. -/
theorem polygonSectorTwoBlocks_count (p : Polygon)
    (i : PolygonBoundarySector p) :
    (polygonSectorTwoBlocks p i).blockCount = 2 := by
  rfl

theorem polygonSectorOneBlock_count (p : Polygon)
    (i : PolygonBoundarySector p) :
    (polygonSectorOneBlock p i).blockCount = 1 := by
  rfl

theorem polygonSectorTwoBlocks_ne_oneBlock (p : Polygon)
    (i : PolygonBoundarySector p) :
    polygonSectorTwoBlocks p i ≠ polygonSectorOneBlock p i := by
  intro h
  have hc := congrArg KuuNativeBlocks.blockCount h
  rw [polygonSectorTwoBlocks_count, polygonSectorOneBlock_count] at hc
  exact (by decide : (2 : Nat) ≠ 1) hc

/-- The original C60 category is the REAL incidence partial order:
each Hom is a subsingleton, so the two paths evaluate to the same
existing original morphism WITHOUT IDENTIFYING their raw path terms. -/
theorem polygonSectorNative_composite_eq (p : Polygon)
    (i : PolygonBoundarySector p) :
    (polygonSectorNativeTwoStep p i).composite =
      (polygonSectorNativeDiagonal p i).composite :=
  Subsingleton.elim _ _

theorem polygonSectorBlocks_composite_eq (p : Polygon)
    (i : PolygonBoundarySector p) :
    (polygonSectorTwoBlocks p i).composite =
      (polygonSectorOneBlock p i).composite :=
  Subsingleton.elim _ _

/-- Two genuinely independent, proof-carrying original C60 block
axes, each with its own raw finite-path partition and a PROVED
comparison in the original Site category. -/
structure PolygonNativeDualAxisFrame (p : Polygon)
    (i : PolygonBoundarySector p) where
  firstAxis :
    KuuNativeBlocks
      (Site.vertex (cyclicBoundaryDart p i.1.val)) (Site.face p)
  secondAxis :
    KuuNativeBlocks
      (Site.vertex (cyclicBoundaryDart p i.1.val)) (Site.face p)
  sameComposite : firstAxis.composite = secondAxis.composite

/-- The canonical two-axis physical frame at EVERY original
polygon sector, with no Bool proxy and no imported old F55. -/
def canonicalPolygonNativeDualAxisFrame (p : Polygon)
    (i : PolygonBoundarySector p) :
    PolygonNativeDualAxisFrame p i where
  firstAxis := polygonSectorTwoBlocks p i
  secondAxis := polygonSectorOneBlock p i
  sameComposite := polygonSectorBlocks_composite_eq p i

/-- A frame on all 180 actual C60 polygon-side occurrences:
its two source block partitions are explicitly NONIDENTICAL. -/
theorem canonicalPolygonNativeDualAxisFrame_distinct (p : Polygon)
    (i : PolygonBoundarySector p) :
    (canonicalPolygonNativeDualAxisFrame p i).firstAxis ≠
      (canonicalPolygonNativeDualAxisFrame p i).secondAxis :=
  polygonSectorTwoBlocks_ne_oneBlock p i

/-- Concrete original north C60 pentagon first sector, retaining
original 90-edge intermediate Site, source dart and real face. -/
def northPentagonNativeDualAxisFrame :
    PolygonNativeDualAxisFrame (.pentagon .north)
      (firstFourPolygonSector (.pentagon .north) 0) :=
  canonicalPolygonNativeDualAxisFrame (.pentagon .north)
    (firstFourPolygonSector (.pentagon .north) 0)

theorem northPentagonNativeDualAxisFrame_distinct :
    northPentagonNativeDualAxisFrame.firstAxis ≠
      northPentagonNativeDualAxisFrame.secondAxis :=
  canonicalPolygonNativeDualAxisFrame_distinct _ _

#print axioms polygonSectorTwoBlocks_flatten
#print axioms polygonSectorOneBlock_flatten
#print axioms polygonSectorTwoStep_ne_diagonal
#print axioms polygonSectorTwoBlocks_ne_oneBlock
#print axioms polygonSectorNative_composite_eq
#print axioms polygonSectorBlocks_composite_eq
#print axioms canonicalPolygonNativeDualAxisFrame_distinct
#print axioms northPentagonNativeDualAxisFrame_distinct
end
end Kuu.F112.Physical
