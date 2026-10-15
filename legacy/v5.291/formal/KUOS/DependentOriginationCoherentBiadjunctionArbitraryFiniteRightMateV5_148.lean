import KUOS.DependentOriginationCoherentBiadjunctionArbitraryFiniteOriginalF45StagesV5_148
import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45SequentialMateNaturalityV5_147

namespace KUOS.DependentOriginationCoherentBiadjunctionArbitraryFiniteRightMateV5_148

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientMateCoherenceV5_141.Generic

set_option autoImplicit false
noncomputable section

/-!
# F51-C / v5.148 — the ORIGINAL chosen right mate of ANY finite F45 run

F51-B is a real inductive Type-valued carrier of arbitrarily many
finite ORIGINAL F45 execution stages, each with its own order choice
and complete actual F19 and F28 native refinement histories.

We transport the WHOLE truly concatenated F44 generated exchange
class by the ORIGINAL chosen F19 right-mate functor plus a completely
independent genuine F28 compression-kernel quotient-category functor.
We then prove that this agrees with transporting EVERY individual
original stage and its proof-relevant histories first.

Using the F46/F51 exact finite-stage classification, the transported
whole run is exactly any original F45 order-selected final route
with the transported concatenated histories and exact depths.

No global finite bound is imposed on the number of stages, and no
original η/ε, F.mapId/F.mapComp ISO or G.toOplax noninvertible forward
comparison is modified or inverted.
-/

namespace Generic

universe uB vB wB uC vC wC uE vE
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- The chosen ORIGINAL F19 right mate acts stage-by-stage on an
ARBITRARY number of actual OLD F45 execution stages. The target
is the very same native F44 generated exchange quotient. -/
theorem chosenRightMateArbitraryFiniteStages
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (stages : Grid.OriginalF45Stages n m modsA pqA modsB pqB) :
    chosenRightMateExchangeQuotientTransport F G K
        stages.toExchangeClass =
      (Grid.OriginalF45Stages.mapBoth (rightMateFunctor F G) K stages).toExchangeClass :=
  Grid.OriginalF45Stages.mapBoth_toExchangeClass (rightMateFunctor F G) K stages

/-- Exact arbitrary-finite-length native mate refinement:
every actual entire old F45 finite run has the SAME transported
F19/F28 Type-valued primitive histories regardless of its historical
per-stage order choices, and equals any selected old F45 total order. -/
theorem chosenRightMateArbitraryFiniteNormal
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (stages : Grid.OriginalF45Stages n m modsA pqA modsB pqB)
    (order : Grid.OriginalF45Order) :
    chosenRightMateExchangeQuotientTransport F G K
        stages.toExchangeClass =
      Grid.AxisTrace.originalF45OrderClass order
        (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) stages.axisHistories.1)
        (Grid.AxisTrace.mapBlocks K stages.axisHistories.2) := by
  calc
    chosenRightMateExchangeQuotientTransport F G K
        stages.toExchangeClass =
      (Grid.OriginalF45Stages.mapBoth (rightMateFunctor F G) K stages).toExchangeClass :=
      chosenRightMateArbitraryFiniteStages F G K stages
    _ = Grid.AxisTrace.originalF45OrderClass order
          (Grid.OriginalF45Stages.mapBoth
            (rightMateFunctor F G) K stages).axisHistories.1
          (Grid.OriginalF45Stages.mapBoth
            (rightMateFunctor F G) K stages).axisHistories.2 :=
      Grid.OriginalF45Stages.toExchangeClass_eq_originalF45 _ order
    _ = Grid.AxisTrace.originalF45OrderClass order
          (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) stages.axisHistories.1)
          (Grid.AxisTrace.mapBlocks K stages.axisHistories.2) := by
      rw [Grid.OriginalF45Stages.mapBoth_axisHistories]

/-- The original independent F19 and F28 categorical Hom evaluations
survive an ARBITRARY finite number of original F45 refinement stages
under the ORIGINAL chosen F19 mate and any genuine F28 quotient functor. -/
theorem chosenRightMateArbitraryFiniteComposites
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (stages : Grid.OriginalF45Stages n m modsA pqA modsB pqB) :
    (Grid.mapBlocks (rightMateFunctor F G) modsA).composite =
      (Grid.mapBlocks (rightMateFunctor F G) modsB).composite ∧
    (Grid.mapBlocks K pqA).composite = (Grid.mapBlocks K pqB).composite :=
  (chosenRightMateExchangeQuotientTransport F G K
    stages.toExchangeClass).composites

/-- The genuine chosen right mate preserves any finite F45 original
run's two-axis depth information as a COMPLETE Type-valued pair,
rather than only as an equality of original categorical arrows. -/
theorem chosenRightMateArbitraryFiniteHistories
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (stages : Grid.OriginalF45Stages n m modsA pqA modsB pqB) :
    (chosenRightMateExchangeQuotientTransport F G K
       stages.toExchangeClass).axisTraces =
      (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) stages.axisHistories.1,
       Grid.AxisTrace.mapBlocks K stages.axisHistories.2) := by
  calc
    (chosenRightMateExchangeQuotientTransport F G K
       stages.toExchangeClass).axisTraces =
      (Grid.AxisTrace.mapBlocks (rightMateFunctor F G)
         stages.toExchangeClass.axisTraces.1,
       Grid.AxisTrace.mapBlocks K
         stages.toExchangeClass.axisTraces.2) :=
      Grid.ExchangeClass.axisTraces_mapBoth (rightMateFunctor F G) K _
    _ = (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) stages.axisHistories.1,
         Grid.AxisTrace.mapBlocks K stages.axisHistories.2) := by
      rw [Grid.OriginalF45Stages.toExchangeClass_axisTraces]

#print axioms chosenRightMateArbitraryFiniteStages
#print axioms chosenRightMateArbitraryFiniteNormal
#print axioms chosenRightMateArbitraryFiniteComposites
#print axioms chosenRightMateArbitraryFiniteHistories

end Generic
end
end KUOS.DependentOriginationCoherentBiadjunctionArbitraryFiniteRightMateV5_148
