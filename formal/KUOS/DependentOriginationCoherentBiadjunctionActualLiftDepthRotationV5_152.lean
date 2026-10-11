import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45DepthRotationMatesV5_152
import KUOS.DependentOriginationCoherentBiadjunctionActualLiftBracketTreeV5_149

namespace KUOS.DependentOriginationCoherentBiadjunctionActualLiftRotationV5_152

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138
open KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140
open KUOS.DependentOriginationCoherentBiadjunctionActualLiftDoubleBracketedHexagonV5_136
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RotationMatesV5_152.Generic
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
# F55-C3 / v5.152 — real original actual source η and target ε on
typed depth-aware F55 finite rotation routes

F55-C1 proves independent two-index F19/F28 depth equalities, genuine
F44 generated exchange quotient invariance, and both COMPLETE original
native typed axis histories of all F55-A paths. F55-C2 transports
those verified results through the unchanged chosen F19 right-mate
functor paired with any honest F28 kernel quotient functor.

We now specialize this theorem to the ACTUAL ORIGINAL source η
(id vs source roundtrip) and target ε (target roundtrip vs id) of
the fixed original coherent actual-lift KuuOS carrier. Nothing is
strictified or reselected; potentially noninvertible G.toOplax
comparison cells are not assigned fictitious inverses.

This remains a certified F44 *endpoint* interpretation of Type-valued
F55 rotations, not unrestricted external tricategorical 3-cell
coherence or presentation-independent descent.
-/

universe u v uH vH uW uP uT vT
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The ACTUAL ORIGINAL source η chosen right mate identifies the
two genuine F44 exchange quotient classes of ANY finite local F45
associativity-rotation chain. Original G-side comparison directions
are left untouched. -/
theorem actualLiftSourceEtaDepthRotationRoute
    {aF bF aG bG : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks
      (actualLiftSourceChosenMatePresentation (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceChosenMatePresentation (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))}
    {pqA pqB : Grid.Blocks x y}
    {n n' m m' : Nat}
    {before : Grid.OriginalF45BracketTree n m modsA pqA modsB pqB}
    {after : Grid.OriginalF45BracketTree n' m' modsA pqA modsB pqB}
    (route : Grid.OriginalF45BracketTree.DepthRotationRoute before after)
    {T : Type uT} [Category.{vT} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T) :
    chosenRightMateExchangeQuotientTransport
      (Pseudofunctor.id
        (ActualLiftSource.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel))
      (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      K (Grid.OriginalF45BracketTree.castDepths
        route.depthEq.1 route.depthEq.2 before).toExchangeClass =
    chosenRightMateExchangeQuotientTransport
      (Pseudofunctor.id
        (ActualLiftSource.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel))
      (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      K after.toExchangeClass :=
  chosenRightMateDepthRotationRoute
    (Pseudofunctor.id
      (ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) K route

/-- The ACTUAL ORIGINAL target ε chosen right mate similarly
preserves the genuinely typed F44 class under ANY finite F54 local
rotation path, with the real target roundtrip orientation retained. -/
theorem actualLiftTargetEpsilonDepthRotationRoute
    {aF bF aG bG : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks
      (actualLiftTargetChosenMatePresentation (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetChosenMatePresentation (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))}
    {pqA pqB : Grid.Blocks x y}
    {n n' m m' : Nat}
    {before : Grid.OriginalF45BracketTree n m modsA pqA modsB pqB}
    {after : Grid.OriginalF45BracketTree n' m' modsA pqA modsB pqB}
    (route : Grid.OriginalF45BracketTree.DepthRotationRoute before after)
    {T : Type uT} [Category.{vT} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T) :
    chosenRightMateExchangeQuotientTransport
      (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (Pseudofunctor.id
        (ActualLiftTarget.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel))
      K (Grid.OriginalF45BracketTree.castDepths
        route.depthEq.1 route.depthEq.2 before).toExchangeClass =
    chosenRightMateExchangeQuotientTransport
      (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (Pseudofunctor.id
        (ActualLiftTarget.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel))
      K after.toExchangeClass :=
  chosenRightMateDepthRotationRoute
    (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (Pseudofunctor.id
      (ActualLiftTarget.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)) K route

#print axioms actualLiftSourceEtaDepthRotationRoute
#print axioms actualLiftTargetEpsilonDepthRotationRoute

end
end KUOS.DependentOriginationCoherentBiadjunctionActualLiftRotationV5_152
