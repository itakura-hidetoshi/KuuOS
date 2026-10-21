import KuuOSFormal.HistoricalF36F40BridgeP47

/-!
# F112-P48 — genuine original C60 face boundary localization

P47 identified the exact obstruction to descending the historical original
F42 face-source quotient into the independent F69 localization: all 32
ACTUAL original F41 5/6-sided physical boundary loops must map to identity.

We prove the two independent preliminary facts needed for its discharge:
  * in any face-star of the ACTUAL independent C60 incidence site,
    a true dart→edge←dart two-leg morphism is compatible with the face
    spokes after genuine Gabriel–Zisman localization;
  * all the actual old F41 polygonal boundary paths traverse only
    physical edges incident with their actual, geometrically matched
    independent polygon, including reverse-oriented historical hexagons.

Neither raw paths nor type-valued face generators are identified by fiat.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry
namespace ActualF47

open CategoryTheory
open Kuu.F112.Physical
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- A general localization statement about genuine incidence spans:
u→w←v with w→z commutes with both u→z and v→z after
inverting the original incidence arrows. No raw path cancellation. -/
theorem p48_localized_incidence_span_cone
    {u v w z : Site}
    (hu : u ≤ w) (hv : v ≤ w) (hw : w ≤ z) :
    zigzagToLocalization
      (Kuu.F112.Physical.Zigzag.forward hu
        (.backward hv (.nil v))) ≫
      siteLocalizationQ.map (homOfLE (le_trans hv hw)) =
        siteLocalizationQ.map (homOfLE (le_trans hu hw)) := by
  let B : siteLocalizationQ.obj v ≅ siteLocalizationQ.obj w :=
    Localization.Construction.wIso
      (W := (⊤ : MorphismProperty Site))
      (homOfLE hv) (by trivial)
  have hvz :
      B.hom ≫ siteLocalizationQ.map (homOfLE hw) =
        siteLocalizationQ.map (homOfLE (le_trans hv hw)) := by
    change siteLocalizationQ.map (homOfLE hv) ≫
      siteLocalizationQ.map (homOfLE hw) = _
    rw [← siteLocalizationQ.map_comp]
    exact congrArg siteLocalizationQ.map (Subsingleton.elim _ _)
  have huz :
      siteLocalizationQ.map (homOfLE hu) ≫
        siteLocalizationQ.map (homOfLE hw) =
      siteLocalizationQ.map (homOfLE (le_trans hu hw)) := by
    rw [← siteLocalizationQ.map_comp]
    exact congrArg siteLocalizationQ.map (Subsingleton.elim _ _)
  change siteLocalizationQ.map (homOfLE hu) ≫ (B.inv ≫ 𝟙 _) ≫
    siteLocalizationQ.map (homOfLE (le_trans hv hw)) = _
  simp only [Category.comp_id]
  rw [← hvz, ← Category.assoc B.inv B.hom,
    B.inv_hom_id, Category.id_comp]
  exact huz

/-- Select the ACTUAL physical C60 edge of each original, genuinely
oriented, historical F41 quiver-arrow generator. -/
def p48_originalArrowNativeEdge {a b : IcosahedralDart} (f : a ⟶ b) :
    Edge :=
  edgeEquiv.symm f.1.edge

/-- The old C60 free path has ONLY real physical edges on the chosen
independent polygon; this Boolean evaluator traverses the complete
actual source word with all historical reverse-edge orientations. -/
def p48_originalPathWithinPolygon (face : Polygon) :
    {a b : IcosahedralDart} → Quiver.Path a b → Bool
  | _, _, .nil => true
  | _, _, .cons prior f =>
      p48_originalPathWithinPolygon face prior &&
        decide (edgeOnFace (p48_originalArrowNativeEdge f) face)

/-- All 32 ACTUAL original pentagon/hexagon source boundary loops,
including the historically reversed hexagonal orientation, use ONLY
edges incident to their exact matching independent C60 polygon. -/
theorem p48_allOriginalFaceBoundaries_incident :
    ∀ face : TruncatedIcosahedralSeedFace,
      p48_originalPathWithinPolygon (polygonEquiv.symm face)
        (c60F41PhysicalFaceBoundaryLoop face).2 = true := by
  intro face
  cases face with
  | aroundVertex v =>
      cases v with
      | north => decide +kernel
      | south => decide +kernel
      | upper i =>
          revert i
          decide +kernel
      | lower i =>
          revert i
          decide +kernel
  | fromTriangle t =>
      cases t with
      | top i =>
          revert i
          decide +kernel
      | bottom i =>
          revert i
          decide +kernel
      | beltUpper i =>
          revert i
          decide +kernel
      | beltLower i =>
          revert i
          decide +kernel

/-- The true original F41 base dart of EVERY physical pentagon and
hexagon belongs to the corresponding independent Kuu polygon. This
does not assert that the old and new cyclic start indices coincide. -/
theorem p48_allOriginalFaceBases_incident :
    ∀ face : TruncatedIcosahedralSeedFace,
      dartOnFace
        (dartEquiv.symm (c60F41PhysicalFaceBoundaryLoop face).1)
        (polygonEquiv.symm face) := by
  intro face
  cases face with
  | aroundVertex v =>
      cases v with
      | north => decide +kernel
      | south => decide +kernel
      | upper i =>
          revert i
          decide +kernel
      | lower i =>
          revert i
          decide +kernel
  | fromTriangle t =>
      cases t with
      | top i =>
          revert i
          decide +kernel
      | bottom i =>
          revert i
          decide +kernel
      | beltUpper i =>
          revert i
          decide +kernel
      | beltLower i =>
          revert i
          decide +kernel

#print axioms p48_localized_incidence_span_cone
#print axioms p48_originalArrowNativeEdge
#print axioms p48_originalPathWithinPolygon
#print axioms p48_allOriginalFaceBoundaries_incident
#print axioms p48_allOriginalFaceBases_incident

end
end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
