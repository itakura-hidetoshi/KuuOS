import KuuOSFormal.HistoricalF36F40BridgeP52

/-!
# F112-P53 — genuine old hexagonal source words without assumptions

The historical F41 hexagon is a dependent six-step Quiver.Path.
Its type casts enforce the actual six endpoint incidences, but do
not alter the underlying oriented physical edge codes. We record
that fact separately, then compute the genuine old path word.
This removes P52's remaining assumption, rather than introducing
a replacement face loop or a new axiom.

The conclusion is the true old F42 face-category quotient functor
into the independent F69 localization. The F54/F55 higher cells,
their interchanger, and global 3-descent remain separate work.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry
namespace ActualF47

open CategoryTheory
open Kuu.F112.Physical
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- Reindexing the source of a genuine historical quiver path
preserves its entire ordered list of true physical edge codes. -/
@[simp] theorem p53_edgeWord_eqmpr_source
    {a b c : IcosahedralDart} (h : a = b)
    (p : Quiver.Path b c) :
    p51_oldPathPhysicalEdges
        (Eq.mpr (congrArg
          (fun x : IcosahedralDart => Quiver.Path x c) h) p) =
      p51_oldPathPhysicalEdges p := by
  cases h
  rfl

/-- Reindexing the target of a genuine historical quiver path
preserves its entire ordered list of true physical edge codes. -/
@[simp] theorem p53_edgeWord_eqmp_target
    {a b c : IcosahedralDart} (h : b = c)
    (p : Quiver.Path a b) :
    p51_oldPathPhysicalEdges
        (Eq.mp (congrArg
          (fun x : IcosahedralDart => Quiver.Path a x) h) p) =
      p51_oldPathPhysicalEdges p := by
  cases h
  rfl

/-- Every historical F41 six-edge hexagon path has exactly the
same ordered physical edge word as its genuine oriented polygonal
cycle, at the actual historical base dart and in its true orientation.
No premise is needed for any of the twenty triangles. -/
theorem p53_allOriginalHexagonWordsExact :
    p52_allOriginalHexagonWordsExact := by
  intro t
  simp [c60F41HexagonBoundaryLoop,
    p51_oldPathPhysicalEdges_comp,
    p51_oriented_single_edge_word,
    p53_edgeWord_eqmpr_source,
    p53_edgeWord_eqmp_target,
    OrientedHexagonCycle.edges,
    List.append_assoc]

/-- All thirty-two original F41/F42 physical face relations now
localize unconditionally to the independent F69 physical site. -/
theorem p53_allOriginalFacesLocalize :
    historicalF42AllOriginalFacesLocalize :=
  p52_allOriginalFacesLocalize_of_hexagonWords
    p53_allOriginalHexagonWordsExact

/-- Unconditional functor from the actual historical F42
face-relation path quotient to the independent F69 localization. -/
def p53_originalF42QuotientToLocalization :
    C60F42FaceRelationPathCategory ⥤ PhysicalLocalization :=
  p52_originalF42QuotientToLocalization
    p53_allOriginalHexagonWordsExact

/-- The unconditional quotient functor recovers the original
historical localization map on every finite old Quiver.Path. -/
theorem p53_originalF42Quotient_factor :
    CategoryTheory.Quotient.functor c60F42OriginalFaceHomRel ⋙
        p53_originalF42QuotientToLocalization =
      historicalOldPathsToLocalization :=
  p52_originalF42Quotient_factor
    p53_allOriginalHexagonWordsExact

#print axioms p53_edgeWord_eqmpr_source
#print axioms p53_edgeWord_eqmp_target
#print axioms p53_allOriginalHexagonWordsExact
#print axioms p53_allOriginalFacesLocalize
#print axioms p53_originalF42QuotientToLocalization
#print axioms p53_originalF42Quotient_factor

end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
