import Kuu.F112.PolygonDisk

/-!
# F112-D3 / finite independent proof-relevant F42 polygon source atlas

A source presentation of a real C60 polygon consists of:
  1. an independently indexed TWO-source proof term for each real side
     (5 for a pentagon; 6 for a hexagon), and
  2. a separately sound typed face disk witness on its entire 10/12-leg
     original raw zigzag boundary.

The full 32-polygon atlas is not reduced to an arbitrary Boolean site:
all 90 original physical edges occur on exactly their TWO ACTUAL
neighboring pentagons/hexagons in the concrete boundary enumerations.
This new source does not claim equivalence with frozen old F42, F54,
F55 or the F47 mixed source.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000
noncomputable section

/-- Genuine sides indexed by their actual pentagonal or hexagonal arity. -/
abbrev PolygonBoundarySector (p : Polygon) :=
  {i : Fin 6 // i.val < polygonSideCount p}

/-- The new proof source has EXACTLY five or six independent sectors. -/
theorem polygonBoundarySector_card (p : Polygon) :
    Fintype.card (PolygonBoundarySector p) = polygonSideCount p := by
  cases p with
  | pentagon v =>
      change Fintype.card {i : Fin 6 // i.val < 5} = 5
      decide
  | hexagon t =>
      change Fintype.card {i : Fin 6 // i.val < 6} = 6
      decide

/-- Direct finite verification, over 90 original edges and all 32 real
faces, of the EXACT neighboring polygon pair. No fabricated face
and no coincidental observation relation is permitted. -/
theorem originalEdge_polygonBoundary_iff :
    ∀ (e : Edge) (p : Polygon),
      e ∈ polygonBoundaryEdges p ↔
        p = faceAt e false ∨ p = faceAt e true := by
  decide

/-- Consequently each physical edge occurs in exactly TWO polygon
boundaries, and these are precisely its declared actual neighboring faces. -/
theorem everyPhysicalEdge_boundaryMultiplicity :
    ∀ e : Edge,
      (Finset.univ.filter
        (fun p : Polygon => e ∈ polygonBoundaryEdges p)).card = 2 := by
  decide

/-- The number of original polygon-side presentations is 180:
12*5 + 20*6 = 2*90, without assuming this as a symbolic axiom. -/
theorem allPolygonBoundarySector_card :
    Fintype.card (Σ p : Polygon, PolygonBoundarySector p) = 180 := by
  decide

/-- The NEW independent physical F42 source-data package.
Every sector contains a raw Type-valued proof tree, not a Prop.
The polygon-wide disk 2-source is backed by the separately proved
F112-D2 cone telescope, without identifying raw words with equality. -/
structure PolygonSourcePresentation (p : Polygon) where
  sector :
    (i : Fin 6) → (hi : i.val < polygonSideCount p) →
      PolygonFanRewrite (polygonRawSide p i hi) (polygonConeRawSide p i hi)
  disk :
    PolygonDiskRewrite (polygonRawLoop p)
      (Zigzag.nil (Site.vertex (cyclicBoundaryDart p 0)))

/-- The real family of independent side witnesses and the sound disk. -/
def canonicalPolygonSource (p : Polygon) : PolygonSourcePresentation p where
  sector := fun i hi => polygonFanSector p i hi
  disk := polygonDiskProof p

/-- A provably different *raw* presentation: preserve the same real
physical sites but insert independent syntactic units in the witnesses.
No proof irrelevance is imposed on the entire polygon source atlas. -/
def unitPrefixedPolygonSource (p : Polygon) : PolygonSourcePresentation p where
  sector := fun i hi => polygonFanSectorWithUnit p i hi
  disk := .vertical (.ident (polygonRawLoop p)) (polygonDiskProof p)

/-- All 32 physical polygons have at least two distinct raw higher
source presentations above the SAME 5/6-sided original geometry. -/
theorem canonicalPolygonSource_ne_withUnit (p : Polygon) :
    canonicalPolygonSource p ≠ unitPrefixedPolygonSource p := by
  intro h
  let i : Fin 6 := ⟨0, by decide⟩
  have hi : i.val < polygonSideCount p := by
    cases p <;> simp [i, polygonSideCount]
  have hs := congrArg (fun S : PolygonSourcePresentation p => S.sector i hi) h
  exact (polygonFanSector_ne_withUnit p i hi) hs

/-- Any inhabitant of the typed real physical source presentation,
not only the canonical one, is sound sectorwise in the original
Gabriel-Zisman localization. -/
theorem PolygonSourcePresentation.sector_localized_sound
    {p : Polygon} (S : PolygonSourcePresentation p)
    (i : Fin 6) (hi : i.val < polygonSideCount p) :
    zigzagToLocalization (polygonRawSide p i hi) =
      zigzagToLocalization (polygonConeRawSide p i hi) :=
  (S.sector i hi).localized_sound

/-- The actual 5/6-side boundary disk contained in each
proof-relevant polygon presentation is sound in the localization. -/
theorem PolygonSourcePresentation.disk_localized_sound
    {p : Polygon} (S : PolygonSourcePresentation p) :
    zigzagToLocalization (polygonRawLoop p) = 𝟙 _ := by
  simpa only [zigzagToLocalization] using S.disk.localized_sound

/-- This is an atlas on every one of the genuine 32 original physical
polygon sites, not merely on the north example or on a proxy. -/
def canonicalC60PolygonSourceAtlas :
    (p : Polygon) → PolygonSourcePresentation p :=
  canonicalPolygonSource

def northPentagonSource : PolygonSourcePresentation (.pentagon .north) :=
  canonicalPolygonSource (.pentagon .north)

theorem northPentagonSource_distinct :
    northPentagonSource ≠ unitPrefixedPolygonSource (.pentagon .north) :=
  canonicalPolygonSource_ne_withUnit (.pentagon .north)

#print axioms polygonBoundarySector_card
#print axioms originalEdge_polygonBoundary_iff
#print axioms everyPhysicalEdge_boundaryMultiplicity
#print axioms allPolygonBoundarySector_card
#print axioms canonicalPolygonSource_ne_withUnit
#print axioms PolygonSourcePresentation.sector_localized_sound
#print axioms PolygonSourcePresentation.disk_localized_sound
#print axioms canonicalC60PolygonSourceAtlas
#print axioms northPentagonSource_distinct
end
end Kuu.F112.Physical
