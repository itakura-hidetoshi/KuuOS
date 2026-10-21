import KuuOSFormal.HistoricalF36F40BridgeP49

/-!
# F112-P50 — genuine old C60 pentagonal F42 generators localize

P49 proves actual source-path cone compatibility on any true C60 face,
without equating original Quiver.Path with independent raw Zigzag.
We now derive an unconditional one-face loop contraction AFTER actual
Gabriel–Zisman localization, using the inverse of the genuine incidence
dart→face map, and apply it to the twelve ORIGINAL historical five-edge
pentagons (real F41 paths). All old hexagon orientation obligations remain
explicit and are not disguised by the independent polygonRawLoop.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry
namespace ActualF47

open CategoryTheory
open Kuu.F112.Physical
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- For ANY original source Quiver.Path loop whose actual physical edges
remain on a single true polygon and whose original base dart belongs
to that polygon, the OLD path's F69 localization is the identity.

This uses P49's exact SOURCE path cone and the concrete Mathlib
Gabriel–Zisman inverse of the genuine base-dart-to-face incidence.
The OLD raw nonempty loop is NOT identified with nil in free paths. -/
theorem p50_old_supported_loop_localizes
    {a : IcosahedralDart} (p : Quiver.Path a a) (face : Polygon)
    (hp : p48_originalPathWithinPolygon face p = true)
    (ha : Site.vertex (dartEquiv.symm a) ≤ Site.face face) :
    historicalOldPathsToLocalization.map p = 𝟙 _ := by
  let A : siteLocalizationQ.obj (Site.vertex (dartEquiv.symm a)) ≅
      siteLocalizationQ.obj (Site.face face) :=
    Localization.Construction.wIso
      (W := (⊤ : MorphismProperty Site)) (homOfLE ha) (by trivial)
  have h := p49_old_path_localized_cone p face hp ha ha
  change historicalOldPathsToLocalization.map p ≫ A.hom = A.hom at h
  have hh := congrArg (fun f => f ≫ A.inv) h
  simpa only [Category.assoc, A.hom_inv_id,
    Category.id_comp, Category.comp_id] using hh

/-- Every ACTUAL original v3.85 historical C60 pentagon's full
five-arrow, based F41 source Quiver.Path stays entirely inside
its truly matched Kuu original pentagonal face. True old words,
not a separately constructed replacement boundary. -/
theorem p50_all_original_pentagons_supported :
    ∀ v : IcosahedralVertex,
      p48_originalPathWithinPolygon
          (polygonEquiv.symm (.aroundVertex v))
          (c60F41PentagonBoundaryLoop v) = true := by
  intro v
  cases v with
  | north => decide +kernel
  | south => decide +kernel
  | upper i =>
      revert i
      decide +kernel
  | lower i =>
      revert i
      decide +kernel

/-- The source dart of each original 5-step pentagon is genuinely
on its independent same pentagon, with no false base-point shift. -/
theorem p50_original_pentagon_base_supported (v : IcosahedralVertex) :
    Site.vertex
        (dartEquiv.symm (icosahedralIncidentDartAt v .s0)) ≤
      Site.face (polygonEquiv.symm (.aroundVertex v)) := by
  change dartOnFace
    (dartEquiv.symm (icosahedralIncidentDartAt v .s0))
    (polygonEquiv.symm (.aroundVertex v))
  exact p48_allOriginalFaceBases_incident (.aroundVertex v)

/-- UNCONDITIONAL localization of all original historical five-edge
F41 physical pentagon boundaries, with the original actual based
Quiver.Path retained, rather than replacing it with a native raw loop. -/
theorem p50_all_original_pentagon_loops_localize :
    ∀ v : IcosahedralVertex,
      historicalOldPathsToLocalization.map
          (c60F41PentagonBoundaryLoop v) = 𝟙 _ := by
  intro v
  exact p50_old_supported_loop_localizes
    (c60F41PentagonBoundaryLoop v)
    (polygonEquiv.symm (.aroundVertex v))
    (p50_all_original_pentagons_supported v)
    (p50_original_pentagon_base_supported v)

/-- This is the exact OLD F42 primitive-face boundary equality on
all TWELVE real original C60 pentagons, at the original base dart.
No condition remains for this pentagonal family. -/
theorem p50_original_pentagon_F42_boundary_sound
    (v : IcosahedralVertex) :
    historicalOldPathsToLocalization.map
        (c60F41PhysicalFaceBoundaryLoop (.aroundVertex v)).2 =
    historicalOldPathsToLocalization.map
      (Quiver.Path.nil :
        Quiver.Path (c60F41PhysicalFaceBoundaryLoop (.aroundVertex v)).1
          (c60F41PhysicalFaceBoundaryLoop (.aroundVertex v)).1) := by
  have hl := p50_all_original_pentagon_loops_localize v
  change historicalOldPathsToLocalization.map
      (c60F41PentagonBoundaryLoop v) =
      historicalOldPathsToLocalization.map
        (Quiver.Path.nil : Quiver.Path
          (icosahedralIncidentDartAt v .s0)
          (icosahedralIncidentDartAt v .s0))
  rw [hl]
  exact (historicalOldPathsToLocalization.map_id _).symm

/-- The identical proven category-theoretic loop-cone mechanism
isolates the ONLY remaining source-geometry obligation for each
actual historical 6-edge hexagon: every oriented old step must stay
within its true original face. It is not assumed as an axiom. -/
theorem p50_original_hexagon_F42_boundary_of_actual_source
    (t : IcosahedralFace)
    (hactual :
      p48_originalPathWithinPolygon
        (polygonEquiv.symm (.fromTriangle t))
        (c60F41HexagonBoundaryLoop t) = true) :
    historicalOldPathsToLocalization.map
        (c60F41PhysicalFaceBoundaryLoop (.fromTriangle t)).2 =
    historicalOldPathsToLocalization.map
      (Quiver.Path.nil :
        Quiver.Path (c60F41PhysicalFaceBoundaryLoop (.fromTriangle t)).1
          (c60F41PhysicalFaceBoundaryLoop (.fromTriangle t)).1) := by
  have ha : Site.vertex
        (dartEquiv.symm (truncatedIcosahedralHexagonCycle t).e0.source) ≤
      Site.face (polygonEquiv.symm (.fromTriangle t)) := by
    change dartOnFace
      (dartEquiv.symm (truncatedIcosahedralHexagonCycle t).e0.source)
      (polygonEquiv.symm (.fromTriangle t))
    exact p48_allOriginalFaceBases_incident (.fromTriangle t)
  have hc := p50_old_supported_loop_localizes
    (c60F41HexagonBoundaryLoop t)
    (polygonEquiv.symm (.fromTriangle t)) hactual ha
  change historicalOldPathsToLocalization.map
      (c60F41HexagonBoundaryLoop t) =
    historicalOldPathsToLocalization.map
      (Quiver.Path.nil : Quiver.Path
        (truncatedIcosahedralHexagonCycle t).e0.source
        (truncatedIcosahedralHexagonCycle t).e0.source)
  rw [hc]
  exact (historicalOldPathsToLocalization.map_id _).symm

#print axioms p50_old_supported_loop_localizes
#print axioms p50_all_original_pentagons_supported
#print axioms p50_original_pentagon_base_supported
#print axioms p50_all_original_pentagon_loops_localize
#print axioms p50_original_pentagon_F42_boundary_sound
#print axioms p50_original_hexagon_F42_boundary_of_actual_source

end
end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
