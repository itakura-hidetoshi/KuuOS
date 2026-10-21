import KuuOSFormal.HistoricalF36F40BridgeP51

/-!
# F112-P52 — exact twenty-hexagon source-word descent criterion

P50 closes all 12 genuinely historical pentagonal F41/F42 relators.
P51 identifies the true original 20 hexagon six-edge *source-word*
comparison, preserving orientation and the actual base dart.

Here we prove that precisely this remaining explicit geometric word
comparison is SUFFICIENT to discharge the 32-face P47 localization
obstruction and construct the actual original F42 quotient functor.
This is conditional until the word equality is independently proved.
No assumption is introduced as an axiom.
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
noncomputable section

/-- The remaining exact original six-edge physical-source word
identity for each actual historical icosahedral triangle. -/
def p52_allOriginalHexagonWordsExact : Prop :=
  ∀ t : IcosahedralFace,
    p51_oldPathPhysicalEdges (c60F41HexagonBoundaryLoop t) =
      (truncatedIcosahedralHexagonCycle t).edges.map
        OrientedTruncatedIcosahedralEdge.edge

/-- The complete original 20 hexagon face relators localize to
identity provided their genuine old source words match the already
verified oriented physical hexagon cycles. -/
theorem p52_allOriginalHexagonFacesLocalize
    (hwords : p52_allOriginalHexagonWordsExact)
    (t : IcosahedralFace) :
    historicalOldPathsToLocalization.map
        (c60F41PhysicalFaceBoundaryLoop (.fromTriangle t)).2 =
      historicalOldPathsToLocalization.map
        (Quiver.Path.nil :
          Quiver.Path (c60F41PhysicalFaceBoundaryLoop (.fromTriangle t)).1
            (c60F41PhysicalFaceBoundaryLoop (.fromTriangle t)).1) :=
  p50_original_hexagon_F42_boundary_of_actual_source t
    (p51_original_hexagon_support_of_exact_edge_word t (hwords t))

/-- ALL 32 genuine historical F41 polygonal face relators become
sound in independent F69 localization under the exact original
20 hexagon source-word identity, with the 12 pentagons already
unconditionally proved in P50. -/
theorem p52_allOriginalFacesLocalize_of_hexagonWords
    (hwords : p52_allOriginalHexagonWordsExact) :
    historicalF42AllOriginalFacesLocalize := by
  intro face
  cases face with
  | aroundVertex v =>
      exact p50_original_pentagon_F42_boundary_sound v
  | fromTriangle t =>
      exact p52_allOriginalHexagonFacesLocalize hwords t

/-- The original F42 face-relation quotient now has a genuine
Mathlib functor to independent F69 physical localization,
conditional ONLY on the exact original 20 hexagon source words.
This does not identify raw old and new paths or higher 2/3-cells. -/
def p52_originalF42QuotientToLocalization
    (hwords : p52_allOriginalHexagonWordsExact) :
    C60F42FaceRelationPathCategory ⥤ PhysicalLocalization :=
  historicalF42FaceQuotientToLocalization
    (p52_allOriginalFacesLocalize_of_hexagonWords hwords)

/-- Exact factorization on ALL original Quiver.Path words,
rather than merely the chosen 32 generating physical faces. -/
theorem p52_originalF42Quotient_factor
    (hwords : p52_allOriginalHexagonWordsExact) :
    CategoryTheory.Quotient.functor c60F42OriginalFaceHomRel ⋙
      p52_originalF42QuotientToLocalization hwords =
        historicalOldPathsToLocalization :=
  historicalF42FaceQuotient_factors
    (p52_allOriginalFacesLocalize_of_hexagonWords hwords)

#print axioms p52_allOriginalHexagonWordsExact
#print axioms p52_allOriginalHexagonFacesLocalize
#print axioms p52_allOriginalFacesLocalize_of_hexagonWords
#print axioms p52_originalF42QuotientToLocalization
#print axioms p52_originalF42Quotient_factor

end
end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
