import KUOS.DependentOriginationTruncatedIcosahedralActualEtaEpsilonV5_155
import KUOS.DependentOriginationTruncatedIcosahedralOriginalChosenMateChargeV5_155

namespace KUOS.DependentOriginationTruncatedIcosahedralActualSquareV5_155

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationTruncatedIcosahedralPentagonRotationBridgeV5_154
open KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationTruncatedIcosahedralActualEtaEpsilonV5_155
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138
open KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140
open KUOS.DependentOriginationCoherentBiadjunctionActualLiftDoubleBracketedHexagonV5_136
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationCoherentBiadjunctionActualLiftRotationV5_152
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientMateCoherenceV5_141.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113

set_option autoImplicit false
noncomputable section

/-!
# F58-D / v5.155 — actual original source η/target ε on C60 flag squares

F58-A independently interprets the original F55 square generator as
(0,1) in the integer-charge target; F58-B proves genuine original
chosen F19 right-mate F44 endpoint preservation on any depth-aware
route between the two disjoint-rotation square corners. F58-C
specialized the *pentagon* interpretation to true actual source η
and target ε. Here the square counterpart is made equally explicit.

For ANY actual original pair of F54 disjoint local-rotation witnesses,
the two genuine original F55 square orders are retained as separate
Type-valued finite routes. Alongside a real v3.84/v3.85/F57-A C60
pentagon-to-hexagon shared-edge four-flag incidence square we prove:

  * actual source η: original id -> actual source roundtrip;
  * actual target ε: actual target roundtrip -> original id;
  * original chosen F19 right-mate F44 preservation after BOTH
    F19/F28 Nat-depth transports for ALL parallel finite routes;
  * BOTH original F55 square orders have exactly two real F54 steps;
  * complete native F19/F28 typed axis histories of all such routes;
  * independent F58-A square generator-charge (0,1).

The C60 square is a four-corner *incidence square*, not an invented
quadrilateral surface face. Choosing the two original F54 rotations
is explicit; the C60 geometric edge by itself does not select them.
We neither invert any potentially noninvertible G.toOplax cell nor
claim a general Gray/tricategorical 3-cell realization.
-/

universe u v uH vH uW uP uT vT
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The ACTUAL ORIGINAL source η (id -> actual source roundtrip) preserves the
genuine chosen right-mate F44 boundary for ANY original finite F55
square route, both original F19/F28 histories, and the independent
nonzero higher square charge over a REAL C60 pentagon/hexagon edge. -/
theorem actualLiftSourceEtaC60FlagSquare
    {aF bF aG bG : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    {x y : compressionKernelCategory aF bF aG bG}
    {p₀ p₁ p₂ : Grid.Blocks
      (actualLiftSourceChosenMatePresentation (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceChosenMatePresentation (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))}
    {q₀ q₁ q₂ : Grid.Blocks x y}
    {n m n' m' : Nat}
    {leftBefore leftAfter : Grid.OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {rightBefore rightAfter : Grid.OriginalF45BracketTree n' m' p₁ q₁ p₂ q₂}
    (edge : TruncatedIcosahedralAroundEdge)
    (left : Grid.OriginalF45BracketTree.LocalRotation leftBefore leftAfter)
    (right : Grid.OriginalF45BracketTree.LocalRotation rightBefore rightAfter)
    {T : Type uT} [Category.{vT} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T) :
    truncatedEdgeOnSeedFace (.around edge) (.aroundVertex edge.center) ∧
    (∀ route : Grid.OriginalF45BracketTree.DepthRotationRoute
      (Grid.OriginalF45BracketTree.node leftBefore rightBefore)
      (Grid.OriginalF45BracketTree.node leftAfter rightAfter),
      chosenRightMateExchangeQuotientTransport
        (Pseudofunctor.id
          (ActualLiftSource.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel))
        (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
          (W := W) A (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))
        K (Grid.OriginalF45BracketTree.castDepths
          route.depthEq.1 route.depthEq.2
          (Grid.OriginalF45BracketTree.node leftBefore rightBefore)).toExchangeClass =
      chosenRightMateExchangeQuotientTransport
        (Pseudofunctor.id
          (ActualLiftSource.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel))
        (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
          (W := W) A (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))
        K (Grid.OriginalF45BracketTree.node leftAfter rightAfter).toExchangeClass) ∧
    ((Grid.OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst
          left right).rotationCount = 2 ∧
     (Grid.OriginalF45BracketTree.DepthRotationRoute.squareRightFirst
          left right).rotationCount = 2) ∧
    (∀ route : Grid.OriginalF45BracketTree.DepthRotationRoute
      (Grid.OriginalF45BracketTree.node leftBefore rightBefore)
      (Grid.OriginalF45BracketTree.node leftAfter rightAfter),
      (Grid.OriginalF45BracketTree.castDepths
        route.depthEq.1 route.depthEq.2
        (Grid.OriginalF45BracketTree.node leftBefore rightBefore)).axisHistories =
      (Grid.OriginalF45BracketTree.node leftAfter rightAfter).axisHistories) ∧
    (OriginalC60FlagSquareWithF55Generator.canonical
      edge left right).squareCell.interpret
      (KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155.OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
        (D := LeftMatePresentation
          (Pseudofunctor.id
          (ActualLiftSource.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel))
          (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
          (W := W) A (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)))
        (E := compressionKernelCategory aF bF aG bG)) =
        ((0 : Int), (1 : Int)) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · exact aroundEdge_incident_pentagon edge
  · intro route
    exact actualLiftSourceEtaDepthRotationRoute W A route K
  · exact ⟨Grid.OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst_count
      left right,
      Grid.OriginalF45BracketTree.DepthRotationRoute.squareRightFirst_count
        left right⟩
  · intro route
    exact route.axisHistories_eq
  · exact originalC60FlagSquare_generatorCharge edge left right


/-- The ACTUAL ORIGINAL target ε (actual target roundtrip -> id) preserves the
genuine chosen right-mate F44 boundary for ANY original finite F55
square route, both original F19/F28 histories, and the independent
nonzero higher square charge over a REAL C60 pentagon/hexagon edge. -/
theorem actualLiftTargetEpsilonC60FlagSquare
    {aF bF aG bG : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    {x y : compressionKernelCategory aF bF aG bG}
    {p₀ p₁ p₂ : Grid.Blocks
      (actualLiftTargetChosenMatePresentation (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetChosenMatePresentation (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))}
    {q₀ q₁ q₂ : Grid.Blocks x y}
    {n m n' m' : Nat}
    {leftBefore leftAfter : Grid.OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {rightBefore rightAfter : Grid.OriginalF45BracketTree n' m' p₁ q₁ p₂ q₂}
    (edge : TruncatedIcosahedralAroundEdge)
    (left : Grid.OriginalF45BracketTree.LocalRotation leftBefore leftAfter)
    (right : Grid.OriginalF45BracketTree.LocalRotation rightBefore rightAfter)
    {T : Type uT} [Category.{vT} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T) :
    truncatedEdgeOnSeedFace (.around edge) (.aroundVertex edge.center) ∧
    (∀ route : Grid.OriginalF45BracketTree.DepthRotationRoute
      (Grid.OriginalF45BracketTree.node leftBefore rightBefore)
      (Grid.OriginalF45BracketTree.node leftAfter rightAfter),
      chosenRightMateExchangeQuotientTransport
        (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
          (W := W) A (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))
        (Pseudofunctor.id
          (ActualLiftTarget.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel))
        K (Grid.OriginalF45BracketTree.castDepths
          route.depthEq.1 route.depthEq.2
          (Grid.OriginalF45BracketTree.node leftBefore rightBefore)).toExchangeClass =
      chosenRightMateExchangeQuotientTransport
        (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
          (W := W) A (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))
        (Pseudofunctor.id
          (ActualLiftTarget.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel))
        K (Grid.OriginalF45BracketTree.node leftAfter rightAfter).toExchangeClass) ∧
    ((Grid.OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst
          left right).rotationCount = 2 ∧
     (Grid.OriginalF45BracketTree.DepthRotationRoute.squareRightFirst
          left right).rotationCount = 2) ∧
    (∀ route : Grid.OriginalF45BracketTree.DepthRotationRoute
      (Grid.OriginalF45BracketTree.node leftBefore rightBefore)
      (Grid.OriginalF45BracketTree.node leftAfter rightAfter),
      (Grid.OriginalF45BracketTree.castDepths
        route.depthEq.1 route.depthEq.2
        (Grid.OriginalF45BracketTree.node leftBefore rightBefore)).axisHistories =
      (Grid.OriginalF45BracketTree.node leftAfter rightAfter).axisHistories) ∧
    (OriginalC60FlagSquareWithF55Generator.canonical
      edge left right).squareCell.interpret
      (KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155.OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
        (D := LeftMatePresentation
          (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
          (W := W) A (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))
          (Pseudofunctor.id
          (ActualLiftTarget.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel)))
        (E := compressionKernelCategory aF bF aG bG)) =
        ((0 : Int), (1 : Int)) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · exact aroundEdge_incident_pentagon edge
  · intro route
    exact actualLiftTargetEpsilonDepthRotationRoute W A route K
  · exact ⟨Grid.OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst_count
      left right,
      Grid.OriginalF45BracketTree.DepthRotationRoute.squareRightFirst_count
        left right⟩
  · intro route
    exact route.axisHistories_eq
  · exact originalC60FlagSquare_generatorCharge edge left right


#print axioms actualLiftSourceEtaC60FlagSquare
#print axioms actualLiftTargetEpsilonC60FlagSquare

end
end KUOS.DependentOriginationTruncatedIcosahedralActualSquareV5_155
