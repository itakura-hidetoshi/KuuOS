import KUOS.DependentOriginationTruncatedIcosahedralOriginalChosenMateChargeV5_155
import KUOS.DependentOriginationCoherentBiadjunctionActualLiftDepthRotationV5_152

namespace KUOS.DependentOriginationTruncatedIcosahedralActualEtaEpsilonV5_155

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationTruncatedIcosahedralPentagonRotationBridgeV5_154
open KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155
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
# F58-C / v5.155 — original actual source η and target ε at C60 pentagons

F57-A–D constructs ACTUAL C60 5-edge pentagon boundaries with cyclic
four-flag geometric-square collar gluing and five genuine F55 signed
original F45 associativity rotation path witnesses. F58-A gives a
separate additive Type-valued higher target distinguishing pentagon
and square generator charges; F58-B pairs this authentic geometry
with the ORIGINAL F19 chosen right mate and independent F28 quotient.

We specialize both independently chosen original actual-lift
roundtrips: source η uses id → source roundtrip, and target ε uses
target roundtrip → id. For EACH concrete original C60 pentagon,
all five original geometric boundary edges stay incident to that
pentagon, any original double-F19/F28-depth pentagon endpoint
rotation route preserves the actual-lift chosen mate F44 quotient,
and the independent genuine C60 pentagon-generator charge is (1,0).

The named argument `D` of the independent `HigherCellTarget.generatorCharge`
is the TYPE of objects of the original `LeftMatePresentation F G`
category. It is NOT `actualLiftSourceChosenMatePresentation` or
`actualLiftTargetChosenMatePresentation`, which are particular OBJECTS
of that category. The two original pseudofunctor directions differ;
therefore both source and target specializations name the correct
`LeftMatePresentation` type and preserve their honest orientation.

These do NOT claim a Gray/tricategorical 3-cell realization,
presentation-independent descent, or that any potentially
noninvertible G.toOplax comparison has an inverse.
-/

universe u v uH vH uW uP uT vT
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The ORIGINAL actual source η (id then actual source roundtrip) on all
genuine C60 five-edge pentagon side witnesses, with two independent
Nat-depth transports and nonzero pentagon generator charge. -/
theorem actualLiftSourceEtaC60Pentagon
    {aF bF aG bG : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    {x y : compressionKernelCategory aF bF aG bG}
    {p₀ p₁ p₂ p₃ p₄ : Grid.Blocks
      (actualLiftSourceChosenMatePresentation (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceChosenMatePresentation (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))}
    {q₀ q₁ q₂ q₃ q₄ : Grid.Blocks x y}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    (t₁ : Grid.OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : Grid.OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : Grid.OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : Grid.OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)
    (v : IcosahedralVertex)
    {T : Type uT} [Category.{vT} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T) :
    (∀ s : PentagonalSlot,
      ((originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v).sides s).incidenceSquare.firstFace =
        TruncatedIcosahedralSeedFace.aroundVertex v) ∧
    (∀ route : Grid.OriginalF45BracketTree.DepthRotationRoute
        (Grid.OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄)
        (Grid.OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄),
      chosenRightMateExchangeQuotientTransport
        (Pseudofunctor.id
        (ActualLiftSource.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel))
        (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
        K (Grid.OriginalF45BracketTree.castDepths
          route.depthEq.1 route.depthEq.2
          (Grid.OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄)).toExchangeClass =
      chosenRightMateExchangeQuotientTransport
        (Pseudofunctor.id
        (ActualLiftSource.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel))
        (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
        K (Grid.OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄).toExchangeClass) ∧
    (OriginalF45C60PentagonPasting.interpret
      t₁ t₂ t₃ t₄
      (originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v)
      (KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155.OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
        (D := LeftMatePresentation
          (Pseudofunctor.id
            (ActualLiftSource.{u, v, uH, vH, uW, uP}
              (W := W) A WorldLabel PresentationLabel))
          (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
            (W := W) A (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)))
        (E := compressionKernelCategory aF bF aG bG))) =
        ((1 : Int), (0 : Int)) := by
  refine ⟨?_, ?_, ?_⟩
  · intro s
    exact ((originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v).sides s).pentagonFace
  · intro route
    exact actualLiftSourceEtaDepthRotationRoute W A route K
  · exact originalC60Pentagon_generatorCharge t₁ t₂ t₃ t₄ v


/-- The ORIGINAL actual target ε (actual target roundtrip then id) on all
genuine C60 five-edge pentagon side witnesses, with two independent
Nat-depth transports and nonzero pentagon generator charge. -/
theorem actualLiftTargetEpsilonC60Pentagon
    {aF bF aG bG : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    {x y : compressionKernelCategory aF bF aG bG}
    {p₀ p₁ p₂ p₃ p₄ : Grid.Blocks
      (actualLiftTargetChosenMatePresentation (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetChosenMatePresentation (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))}
    {q₀ q₁ q₂ q₃ q₄ : Grid.Blocks x y}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    (t₁ : Grid.OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : Grid.OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : Grid.OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : Grid.OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)
    (v : IcosahedralVertex)
    {T : Type uT} [Category.{vT} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T) :
    (∀ s : PentagonalSlot,
      ((originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v).sides s).incidenceSquare.firstFace =
        TruncatedIcosahedralSeedFace.aroundVertex v) ∧
    (∀ route : Grid.OriginalF45BracketTree.DepthRotationRoute
        (Grid.OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄)
        (Grid.OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄),
      chosenRightMateExchangeQuotientTransport
        (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
        (Pseudofunctor.id
        (ActualLiftTarget.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel))
        K (Grid.OriginalF45BracketTree.castDepths
          route.depthEq.1 route.depthEq.2
          (Grid.OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄)).toExchangeClass =
      chosenRightMateExchangeQuotientTransport
        (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
        (Pseudofunctor.id
        (ActualLiftTarget.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel))
        K (Grid.OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄).toExchangeClass) ∧
    (OriginalF45C60PentagonPasting.interpret
      t₁ t₂ t₃ t₄
      (originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v)
      (KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155.OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
        (D := LeftMatePresentation
          (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
            (W := W) A (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel))
          (Pseudofunctor.id
            (ActualLiftTarget.{u, v, uH, vH, uW, uP}
              (W := W) A WorldLabel PresentationLabel)))
        (E := compressionKernelCategory aF bF aG bG))) =
        ((1 : Int), (0 : Int)) := by
  refine ⟨?_, ?_, ?_⟩
  · intro s
    exact ((originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v).sides s).pentagonFace
  · intro route
    exact actualLiftTargetEpsilonDepthRotationRoute W A route K
  · exact originalC60Pentagon_generatorCharge t₁ t₂ t₃ t₄ v


#print axioms actualLiftSourceEtaC60Pentagon
#print axioms actualLiftTargetEpsilonC60Pentagon

end
end KUOS.DependentOriginationTruncatedIcosahedralActualEtaEpsilonV5_155
