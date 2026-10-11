import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RotationMatesV5_151
import KUOS.DependentOriginationCoherentBiadjunctionActualLiftBracketTreeV5_149

namespace KUOS.DependentOriginationCoherentBiadjunctionActualLiftRotationV5_151

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RotationMatesV5_151.Generic
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
# F54-E / v5.151 — actual source η and target ε on real finite rotation chains

F54-A/C constructs genuine Type-valued contextual associativity
rotations of actual ORIGINAL F45 binary refinement trees; F54-B
constructs actual finite paths of such moves and their reversals.

This file specializes F54-D's original chosen right-mate theorem to
the ACTUAL ORIGINAL source-unit η and target-counit ε pseudofunctors
on their respective native actual-lift categories. The chosen
original η/ε data are not reselected, strictified or modified.

The equalities hold at the ORIGINAL chosen mate's complete F44
exchange-class level, not merely on endpoint categorical Hom arrows.
The F52-D six source/target original general, mapId and mapComp mate
boundary statements can therefore be instantiated at both ends of
each actual rotation chain without replacing noninvertible G-side
lax comparisons by invented inverses.

No general external tricategorical 3-cell law is asserted.
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
theorem actualLiftSourceEtaFiniteRotation
    {aF bF aG bG : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks
      (actualLiftSourceChosenMatePresentation (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceChosenMatePresentation (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat}
    {before after : Grid.OriginalF45BracketTree n m modsA pqA modsB pqB}
    (chain : Grid.OriginalF45BracketTree.RotationChain before after)
    {T : Type uT} [Category.{vT} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T) :
    chosenRightMateExchangeQuotientTransport
      (Pseudofunctor.id
        (ActualLiftSource.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel))
      (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      K before.toExchangeClass =
    chosenRightMateExchangeQuotientTransport
      (Pseudofunctor.id
        (ActualLiftSource.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel))
      (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      K after.toExchangeClass :=
  chosenRightMateFiniteRotationChain
    (Pseudofunctor.id
      (ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) K chain

/-- The ACTUAL ORIGINAL target ε chosen right mate similarly
preserves the genuinely typed F44 class under ANY finite F54 local
rotation path, with the real target roundtrip orientation retained. -/
theorem actualLiftTargetEpsilonFiniteRotation
    {aF bF aG bG : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks
      (actualLiftTargetChosenMatePresentation (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetChosenMatePresentation (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat}
    {before after : Grid.OriginalF45BracketTree n m modsA pqA modsB pqB}
    (chain : Grid.OriginalF45BracketTree.RotationChain before after)
    {T : Type uT} [Category.{vT} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T) :
    chosenRightMateExchangeQuotientTransport
      (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (Pseudofunctor.id
        (ActualLiftTarget.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel))
      K before.toExchangeClass =
    chosenRightMateExchangeQuotientTransport
      (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (Pseudofunctor.id
        (ActualLiftTarget.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel))
      K after.toExchangeClass :=
  chosenRightMateFiniteRotationChain
    (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (Pseudofunctor.id
      (ActualLiftTarget.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)) K chain

#print axioms actualLiftSourceEtaFiniteRotation
#print axioms actualLiftTargetEpsilonFiniteRotation

end
end KUOS.DependentOriginationCoherentBiadjunctionActualLiftRotationV5_151
