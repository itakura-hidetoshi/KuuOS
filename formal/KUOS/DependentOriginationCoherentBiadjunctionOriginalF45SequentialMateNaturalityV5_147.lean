import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45SequentialCoherenceV5_147
import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45OrderedMatesV5_146

namespace KUOS.DependentOriginationCoherentBiadjunctionOriginalF45SequentialMateNaturalityV5_147

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientMateCoherenceV5_141.Generic
open KUOS.DependentOriginationCoherentBiadjunctionOriginalF45OrderedMatesV5_146.Generic

set_option autoImplicit false
noncomputable section

/-!
# F50-B / v5.147 — chosen right-mate sequential functoriality

F49 handles an actual original F45 route at one finite depth; F50-A
proves the genuinely stronger serial execution law for arbitrary two
successive actual original F45 routes in the F44 *generated* exchange
quotient with exact per-axis depths and ANY original order selection.

Here the ORIGINAL F19 chosen right-mate functor and an arbitrary
honest F28 compression-kernel quotient-category functor preserve this
sequential composition. No G.toOplax comparison cell is inverted or
replaced and no F19/F28 Hom type is identified.

The full original mate/hexagon, nonstrict mapId/mapComp and actualLift
source η/target ε boundaries are subsequently specialized to these
two consecutive ORIGINAL F45 refinement histories, not merely to a
fresh independent F46 normal form.
-/

namespace Generic

universe uB vB wB uC vC wC uE vE
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- The ORIGINAL chosen F19 right-mate functor with an independent
F28 genuine quotient functor preserves an arbitrary two-stage
generated F44 exchange-class concatenation ON THE NOSE. -/
theorem chosenRightMateExchangeQuotientTransport_append
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsM modsB : Grid.Blocks a b}
    {pqA pqM pqB : Grid.Blocks x y}
    {n m n' m' : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (h : Grid.ExchangeClass n m modsA modsM pqA pqM)
    (k : Grid.ExchangeClass n' m' modsM modsB pqM pqB) :
    chosenRightMateExchangeQuotientTransport F G K
        (KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid.ExchangeClass.append h k) =
      KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid.ExchangeClass.append
        (chosenRightMateExchangeQuotientTransport F G K h)
        (chosenRightMateExchangeQuotientTransport F G K k) :=
  Grid.ExchangeClass.mapBoth_append (rightMateFunctor F G) K h k

/-- Complete two-stage ORIGINAL F45 route naturality of the genuine
chosen right mate. Even if first, second, and total execution orders
are all different, their complete transported native F19/F28 histories
are exactly the concatenation of the separately transported histories,
with original F19/F28 primitive steps and counts retained. -/
theorem chosenRightMateOriginalF45SequentialNormal
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsM modsB : Grid.Blocks a b}
    {pqA pqM pqB : Grid.Blocks x y}
    {n m n' m' : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (first second whole : Grid.OriginalF45Order)
    (hm₁ : Grid.AxisTrace n modsA modsM)
    (hm₂ : Grid.AxisTrace n' modsM modsB)
    (hc₁ : Grid.AxisTrace m pqA pqM)
    (hc₂ : Grid.AxisTrace m' pqM pqB) :
    chosenRightMateExchangeQuotientTransport F G K
      (KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid.ExchangeClass.append
        (Grid.AxisTrace.originalF45OrderClass first hm₁ hc₁)
        (Grid.AxisTrace.originalF45OrderClass second hm₂ hc₂)) =
    Grid.AxisTrace.originalF45OrderClass whole
      (Grid.AxisTrace.append
        (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) hm₁)
        (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) hm₂))
      (Grid.AxisTrace.append
        (Grid.AxisTrace.mapBlocks K hc₁)
        (Grid.AxisTrace.mapBlocks K hc₂)) :=
  Grid.AxisTrace.originalF45OrderClass_append_mapBoth
    (rightMateFunctor F G) K first second whole hm₁ hm₂ hc₁ hc₂

/-- Sequential original F45 right-mate transport is insensitive to
changing either stage's actual ORIGINAL ordered F45 implementation:
the two sequences have identical complete original axis histories,
hence identical generated exchange classes on the mate side. -/
theorem chosenRightMateOriginalF45SequentialOrderIndependent
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsM modsB : Grid.Blocks a b}
    {pqA pqM pqB : Grid.Blocks x y}
    {n m n' m' : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (first₁ first₂ second₁ second₂ : Grid.OriginalF45Order)
    (hm₁ : Grid.AxisTrace n modsA modsM)
    (hm₂ : Grid.AxisTrace n' modsM modsB)
    (hc₁ : Grid.AxisTrace m pqA pqM)
    (hc₂ : Grid.AxisTrace m' pqM pqB) :
    chosenRightMateExchangeQuotientTransport F G K
      (KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid.ExchangeClass.append
        (Grid.AxisTrace.originalF45OrderClass first₁ hm₁ hc₁)
        (Grid.AxisTrace.originalF45OrderClass second₁ hm₂ hc₂)) =
    chosenRightMateExchangeQuotientTransport F G K
      (KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid.ExchangeClass.append
        (Grid.AxisTrace.originalF45OrderClass first₂ hm₁ hc₁)
        (Grid.AxisTrace.originalF45OrderClass second₂ hm₂ hc₂)) := by
  exact congrArg (chosenRightMateExchangeQuotientTransport F G K)
    (by
      calc
        KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid.ExchangeClass.append
            (Grid.AxisTrace.originalF45OrderClass first₁ hm₁ hc₁)
            (Grid.AxisTrace.originalF45OrderClass second₁ hm₂ hc₂) =
          Grid.AxisTrace.originalF45OrderClass first₁
            (Grid.AxisTrace.append hm₁ hm₂)
            (Grid.AxisTrace.append hc₁ hc₂) :=
          Grid.AxisTrace.originalF45OrderClass_append
            first₁ second₁ first₁ hm₁ hm₂ hc₁ hc₂
        _ = Grid.AxisTrace.originalF45OrderClass first₂
              (Grid.AxisTrace.append hm₁ hm₂)
              (Grid.AxisTrace.append hc₁ hc₂) :=
          Grid.AxisTrace.originalF45OrderClass_independent
            first₁ first₂ _ _
        _ = KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid.ExchangeClass.append
              (Grid.AxisTrace.originalF45OrderClass first₂ hm₁ hc₁)
              (Grid.AxisTrace.originalF45OrderClass second₂ hm₂ hc₂) :=
          (Grid.AxisTrace.originalF45OrderClass_append
            first₂ second₂ first₂ hm₁ hm₂ hc₁ hc₂).symm)

/-- Exact original categorical mate Hom-composite consequence of TWO
sequential ORIGINAL F45 mixed primitive refinements, prior to
evaluating original η / ε or the four-stage mixed hexagon. -/
theorem chosenRightMateOriginalF45SequentialComposites
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsM modsB : Grid.Blocks a b}
    {pqA pqM pqB : Grid.Blocks x y}
    {n m n' m' : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (first second : Grid.OriginalF45Order)
    (hm₁ : Grid.AxisTrace n modsA modsM)
    (hm₂ : Grid.AxisTrace n' modsM modsB)
    (hc₁ : Grid.AxisTrace m pqA pqM)
    (hc₂ : Grid.AxisTrace m' pqM pqB) :
    (Grid.mapBlocks (rightMateFunctor F G) modsA).composite =
      (Grid.mapBlocks (rightMateFunctor F G) modsB).composite ∧
    (Grid.mapBlocks K pqA).composite = (Grid.mapBlocks K pqB).composite :=
  (chosenRightMateExchangeQuotientTransport F G K
    (KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid.ExchangeClass.append
      (Grid.AxisTrace.originalF45OrderClass first hm₁ hc₁)
      (Grid.AxisTrace.originalF45OrderClass second hm₂ hc₂))).composites

#print axioms chosenRightMateExchangeQuotientTransport_append
#print axioms chosenRightMateOriginalF45SequentialNormal
#print axioms chosenRightMateOriginalF45SequentialOrderIndependent
#print axioms chosenRightMateOriginalF45SequentialComposites

end Generic
end
end KUOS.DependentOriginationCoherentBiadjunctionOriginalF45SequentialMateNaturalityV5_147
