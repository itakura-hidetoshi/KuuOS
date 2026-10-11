import KUOS.DependentOriginationTruncatedIcosahedralHigherGeneratorChargeV5_155
import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45DepthRotationMatesV5_152

namespace KUOS.DependentOriginationTruncatedIcosahedralHigherMatesV5_155

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationTruncatedIcosahedralPentagonRotationBridgeV5_154
open KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientMateCoherenceV5_141.Generic
open KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RotationMatesV5_152.Generic

set_option autoImplicit false
noncomputable section

/-!
# F58-B / v5.155 — genuine C60 geometry plus original chosen right-mate boundary

F57-A–D now contains a REAL C60 five-edge pentagon with a cyclic
collar of four-flag vertex/face incidence squares, five ACTUAL
proof-relevant F55 finite associativity paths and true flag-corner
gluing. F58-A defines an independent nonzero integer-pair target
for actual pentagon and square higher generators.

Here we preserve, SIMULTANEOUSLY at the same genuine C60 patch:
 (1) the original geometric pentagon incidence at all five sides,
 (2) F19's ORIGINAL chosen right-mate F44 exchange-quotient equality
     for ANY double-depth-aware route between original F55 pentagon
     endpoints, and
 (3) the nonzero independent F58-A pentagon-generator charge.
A second theorem does this for real C60 square incidence and the
original chosen mate of both F55 local-rotation square paths.

The original F19 chosen right-mate functor and honest separate F28
compression-kernel quotient functor are never replaced or confused;
no inverse of potentially noninvertible G.toOplax cells is claimed.
The integer-pair model is not a universal tricategorical 3-cell.
-/

namespace Generic

universe uB vB wB uC vC wC uT vT
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- On every REAL C60 pentagon, all five existing edge-local flag
squares carry the original pentagon face; ANY actual F55 original
depth-aware route across the corresponding five bracketed vertices
preserves the genuine chosen right-mate F44 quotient, while the
nonzero F58 independent pentagon charge remains retained. -/
theorem originalC60PentagonChosenMateAndCharge
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {p₀ p₁ p₂ p₃ p₄ : Grid.Blocks a b}
    {q₀ q₁ q₂ q₃ q₄ : Grid.Blocks x y}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {T : Type uT} [Category.{vT} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (t₁ : Grid.OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : Grid.OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : Grid.OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : Grid.OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)
    (v : IcosahedralVertex) :
    (∀ s : PentagonalSlot,
      ((originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v).sides s).incidenceSquare.firstFace =
        TruncatedIcosahedralSeedFace.aroundVertex v) ∧
    (∀ route : Grid.OriginalF45BracketTree.DepthRotationRoute
        (Grid.OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄)
        (Grid.OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄),
      chosenRightMateExchangeQuotientTransport F G K
        (Grid.OriginalF45BracketTree.castDepths
          route.depthEq.1 route.depthEq.2
          (Grid.OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄)).toExchangeClass =
      chosenRightMateExchangeQuotientTransport F G K
        (Grid.OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄).toExchangeClass) ∧
    (OriginalF45C60PentagonPasting.interpret
      t₁ t₂ t₃ t₄
      (originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v)
      (KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155.OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
        (D := LeftMatePresentation F G)
        (E := compressionKernelCategory aF bF aG bG))) =
      ((1 : Int), (0 : Int)) := by
  refine ⟨?_, ?_, ?_⟩
  · intro s
    exact ((originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v).sides s).pentagonFace
  · intro route
    exact chosenRightMateDepthRotationRoute F G K route
  · exact originalC60Pentagon_generatorCharge t₁ t₂ t₃ t₄ v

/-- The *real* C60 pentagon still distinguishes the THREE original
rotation route from the TWO original rotation route even after
original chosen-mate boundary compatibility. Their raw witnesses
are not made equal merely because F44 quotient classes agree. -/
theorem originalC60PentagonTypedRoutes_distinct
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {p₀ p₁ p₂ p₃ p₄ : Grid.Blocks a b}
    {q₀ q₁ q₂ q₃ q₄ : Grid.Blocks x y}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    (t₁ : Grid.OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : Grid.OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : Grid.OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : Grid.OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)
    (v : IcosahedralVertex) :
    Grid.OriginalF45BracketTree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄ ≠
      Grid.OriginalF45BracketTree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄ ∧
    (OriginalF45C60PentagonPasting.interpret
      t₁ t₂ t₃ t₄
      (originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v)
      (KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155.OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
        (D := LeftMatePresentation F G)
        (E := compressionKernelCategory aF bF aG bG))) ≠
      (0 : Int × Int) := by
  exact ⟨Grid.OriginalF45BracketTree.DepthRotationRoute.pentagonLong_ne_short
      t₁ t₂ t₃ t₄,
    originalC60Pentagon_generatorCharge_ne_zero t₁ t₂ t₃ t₄ v⟩

/-- Real C60 pentagon/hexagon shared-edge geometry and ANY indexed
original F55 depth-aware square path share the same honest
chosen right-mate F44 endpoint equality. In particular this applies
to BOTH original F55 independent local-rotation square orders,
without a fake universal 3-cell inversion. -/
theorem originalC60FlagSquareChosenMateAndCharge
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {p₀ p₁ p₂ : Grid.Blocks a b}
    {q₀ q₁ q₂ : Grid.Blocks x y}
    {n m n' m' : Nat}
    {leftBefore leftAfter :
      Grid.OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {rightBefore rightAfter :
      Grid.OriginalF45BracketTree n' m' p₁ q₁ p₂ q₂}
    {T : Type uT} [Category.{vT} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (edge : TruncatedIcosahedralAroundEdge)
    (left : Grid.OriginalF45BracketTree.LocalRotation leftBefore leftAfter)
    (right : Grid.OriginalF45BracketTree.LocalRotation rightBefore rightAfter) :
    truncatedEdgeOnSeedFace (.around edge) (.aroundVertex edge.center) ∧
    (∀ route : Grid.OriginalF45BracketTree.DepthRotationRoute
      (Grid.OriginalF45BracketTree.node leftBefore rightBefore)
      (Grid.OriginalF45BracketTree.node leftAfter rightAfter),
      chosenRightMateExchangeQuotientTransport F G K
        (Grid.OriginalF45BracketTree.castDepths
          route.depthEq.1 route.depthEq.2
          (Grid.OriginalF45BracketTree.node leftBefore rightBefore)).toExchangeClass =
      chosenRightMateExchangeQuotientTransport F G K
        (Grid.OriginalF45BracketTree.node leftAfter rightAfter).toExchangeClass) ∧
    (OriginalC60FlagSquareWithF55Generator.canonical
      edge left right).squareCell.interpret
        (KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155.OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
          (D := LeftMatePresentation F G)
          (E := compressionKernelCategory aF bF aG bG)) =
        ((0 : Int), (1 : Int)) := by
  refine ⟨?_, ?_, ?_⟩
  · exact aroundEdge_incident_pentagon edge
  · intro route
    exact chosenRightMateDepthRotationRoute F G K route
  · exact originalC60FlagSquare_generatorCharge edge left right

#print axioms originalC60PentagonChosenMateAndCharge
#print axioms originalC60PentagonTypedRoutes_distinct
#print axioms originalC60FlagSquareChosenMateAndCharge

end Generic
end
end KUOS.DependentOriginationTruncatedIcosahedralHigherMatesV5_155
