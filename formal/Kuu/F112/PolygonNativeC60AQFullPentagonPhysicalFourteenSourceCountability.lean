import Mathlib.Tactic.DeriveCountable
import Kuu.F112.PolygonBracketRoutes
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalFifteenSyntaxCountability

/-!
# F112-P94D3GE — finite original C60 geometry and actual raw syntax are Countable

The original true C60 finite geometry has existing Fintype witnesses:
60 Dart vertices, 90 Edge cells, 32 Polygon faces, and 182 Site cells.
Their Countable instances are *derived*, not postulated.

Original C60 incidence Hom (a preorder Hom) is subsingleton.
Original proof-relevant finite Zigzag paths have a countable unbounded
finite constructor syntax over these actual C60 sites. The same
countability propagates to F54-shaped binary polygon bracket trees,
elementary rotations, and original finite routes, all retaining
the typed boundary sector and route history.

Crucial authority boundary: the original K5 14D Type-valued family
is NOT simply Site, Zigzag or PolygonBracketRoute. Its constructors
store independent 7D–13D source typed proofs and arbitrary category
D/E objects and Hom. The initial direct 14D deriveCountable attempt
correctly failed on those missing Type-valued Countable instances.
Nothing below turns that mathematical obstruction into an axiom.
The next source step must construct Countable for those actual lower
original proof types under exact countable input-category assumptions.

No overwrite of any original C60 physical definition; independent
Kuu and strict Kuu remain separate presentations, 107 public roots,
no Gray reintroduction, and no invented 19D filling.
Pinned Lean v4.30.0-rc2 and mathlib exact hash.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- Actual 60 original C60 truncated dart vertices are Countable.
This follows from the existing Fintype, not a new smallness axiom. -/
theorem nativeC60GEPhysicalDart_countable : Countable Dart := inferInstance

/-- Actual 90 original C60 edges are Countable. -/
theorem nativeC60GEPhysicalEdge_countable : Countable Edge := inferInstance

/-- Actual 32 original C60 pentagon/hexagon faces are Countable. -/
theorem nativeC60GEPhysicalPolygon_countable : Countable Polygon := inferInstance

/-- All 182 actual original C60 incidence sites are Countable. -/
theorem nativeC60GEPhysicalSite_countable : Countable Site := inferInstance

/-- The disjoint union of original 60/90/32 physical C60 cells
is Countable, with each cell's distinct summand retained. -/
theorem nativeC60GEPhysicalCellSum_countable :
    Countable (Dart ⊕ Edge ⊕ Polygon) := inferInstance

/-- Each original incidence-category Hom on the finite C60
preorder is at most one proof, and hence Countable. This is
about the ACTUAL physical Site category, not arbitrary D/E Hom. -/
theorem nativeC60GEPhysicalIncidenceHom_countable (s t : Site) :
    Countable (s ⟶ t) := inferInstance

/- True physical incidence zigzags are FINITE proof-bearing
forward/reverse paths. A finite alphabet of actual C60 sites
gives Countable paths even though path lengths are unbounded. -/
deriving instance Countable for Zigzag

/-- Every indexed ORIGINAL raw C60 Zigzag fiber is Countable. -/
theorem nativeC60GEPhysicalZigzag_countable (s t : Site) :
    Countable (Zigzag s t) := inferInstance

/-- The original raw zigzag total (both actual dependent endpoints
retained) is Countable. This is NOT an observer quotient. -/
theorem nativeC60GEPhysicalZigzagTotal_countable :
    Countable (Σ s : Site, Σ t : Site, Zigzag s t) := inferInstance

/-- The genuine physical pentagonal or hexagonal side index
is a subtype of Fin 6, so is Countable. -/
theorem nativeC60GEPolygonBoundarySector_countable (p : Polygon) :
    Countable (PolygonBoundarySector p) := inferInstance

/- Original finite bracket trees on a genuine C60 polygon have
Countable recursive syntax, retaining exact source sectors. -/
deriving instance Countable for PolygonBracketTree

theorem nativeC60GEPolygonBracketTree_countable (p : Polygon) :
    Countable (PolygonBracketTree p) := inferInstance

/- Genuine F54-shaped contextual elementary associations keep
their dependent original bracket-tree source/target indices. -/
deriving instance Countable for PolygonBracketRotation

/- Finite route syntax, including ident, trans and both contexts. -/
deriving instance Countable for PolygonBracketRoute

theorem nativeC60GEPolygonBracketRoute_countable
    (p : Polygon) (a b : PolygonBracketTree p) :
    Countable (PolygonBracketRoute p a b) := inferInstance

/-- Every original dependent C60 bracket route fiber can be
stored with its exact pair of original proof-relevant trees. -/
theorem nativeC60GEPolygonBracketRouteTotal_countable (p : Polygon) :
    Countable (Σ a : PolygonBracketTree p,
      Σ b : PolygonBracketTree p, PolygonBracketRoute p a b) :=
  inferInstance

#print axioms nativeC60GEPhysicalDart_countable
#print axioms nativeC60GEPhysicalEdge_countable
#print axioms nativeC60GEPhysicalPolygon_countable
#print axioms nativeC60GEPhysicalSite_countable
#print axioms nativeC60GEPhysicalCellSum_countable
#print axioms nativeC60GEPhysicalIncidenceHom_countable
#print axioms nativeC60GEPhysicalZigzag_countable
#print axioms nativeC60GEPhysicalZigzagTotal_countable
#print axioms nativeC60GEPolygonBoundarySector_countable
#print axioms nativeC60GEPolygonBracketTree_countable
#print axioms nativeC60GEPolygonBracketRoute_countable
#print axioms nativeC60GEPolygonBracketRouteTotal_countable

end
end Kuu.F112.Physical
