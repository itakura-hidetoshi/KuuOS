import KUOS.DependentOriginationCoherentBiadjunctionExchangeNormalFormNaturalityV5_143
import KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateAxisTraceV5_142

namespace KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateNormalFormV5_143

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientMateCoherenceV5_141.Generic
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateAxisTraceV5_142.Generic

set_option autoImplicit false
noncomputable section

/-!
# F46-E / v5.143 — normalization of the ORIGINAL chosen right-mate transport

The first axis remains the native F19 chosen right-mate presentation
category. The second remains the actual F28 compression-kernel quotient
category. We never identify their Hom types, replace them by F26
comparison chains, or change the original source η, target ε, chosen
objectwise adjunctions, F-side comparison ISOs, or G-side potentially
noninvertible lax comparison cells.

Every F44 exchange class is precisely represented by its two original
F45 histories. Applying the original chosen right-mate functor and a
separate genuine F28 functor yields EXACTLY the F46 canonical class
of those independently transported histories.
-/

namespace Generic

universe uB vB wB uC vC wC uE vE
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- Fully proof-relevant canonical normal form of the ORIGINAL F19
chosen right-mate transport and a separate F28 quotient functor. -/
theorem chosenRightMateExchangeNormalForm
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (exchange : Grid.ExchangeClass n m modsA modsB pqA pqB) :
    chosenRightMateExchangeQuotientTransport F G K exchange =
      Grid.AxisTrace.pairToClass
        (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) exchange.axisTraces.1,
         Grid.AxisTrace.mapBlocks K exchange.axisTraces.2) := by
  apply (Grid.ExchangeClass.axisTraceEquiv
    (ma := Grid.mapBlocks (rightMateFunctor F G) modsA)
    (mb := Grid.mapBlocks (rightMateFunctor F G) modsB)
    (pa := Grid.mapBlocks K pqA)
    (pb := Grid.mapBlocks K pqB)
    (n := n) (m := m)).injective
  calc
    (chosenRightMateExchangeQuotientTransport F G K exchange).axisTraces =
        (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) exchange.axisTraces.1,
         Grid.AxisTrace.mapBlocks K exchange.axisTraces.2) :=
      chosenRightMateAxisTraceNaturality F G K exchange
    _ = (Grid.AxisTrace.pairToClass
          (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) exchange.axisTraces.1,
           Grid.AxisTrace.mapBlocks K exchange.axisTraces.2)).axisTraces :=
      (Grid.AxisTrace.pairToClass_axisTraces _).symm

/-- The F46 normal form represents the same genuine original
F19/F28 exchange class and hence preserves both native categorical
composites before ANY mate/hexagon boundary comparison is evaluated. -/
theorem chosenRightMateExchangeNormalForm_composites
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (exchange : Grid.ExchangeClass n m modsA modsB pqA pqB) :
    (Grid.mapBlocks (rightMateFunctor F G) modsA).composite =
      (Grid.mapBlocks (rightMateFunctor F G) modsB).composite ∧
    (Grid.mapBlocks K pqA).composite = (Grid.mapBlocks K pqB).composite :=
  (chosenRightMateExchangeQuotientTransport F G K exchange).composites

#print axioms chosenRightMateExchangeNormalForm
#print axioms chosenRightMateExchangeNormalForm_composites

end Generic
end
end KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateNormalFormV5_143
