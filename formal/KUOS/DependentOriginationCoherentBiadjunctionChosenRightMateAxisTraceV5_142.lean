import KUOS.DependentOriginationCoherentBiadjunctionAxisTraceRealizationV5_142
import KUOS.DependentOriginationCoherentBiadjunctionActualLiftExchangeQuotientV5_141

namespace KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateAxisTraceV5_142

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionProofRelevantAxisTracesV5_142
open KUOS.DependentOriginationCoherentBiadjunctionFunctorialAxisTraceDescentV5_142
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientMateCoherenceV5_141.Generic
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic

set_option autoImplicit false
noncomputable section

/-!
# F45-D / v5.142 — actual chosen right mate respects both extracted histories

The first original axis is the F19 category of chosen StrongTrans
modifications; the other is the actual F28 compression-kernel quotient
category. Their types and their original categorical evaluations
remain SEPARATE.

The genuine F19 right-mate functor transports the full generated
exchange class as in F44. F45 proves it additionally transports the
two Type-valued original axis histories exactly: extracting before
transport and transporting before extraction form a strict commuting
square at the level of these independent Type-level step sequences.

The original F25/F33 mate boundaries, F35 hexagon, source eta and
target epsilon, and G-side potentially noninvertible forward mapId
and mapComp comparisons are all unchanged.
-/

namespace Generic

universe uB vB wB uC vC wC uE vE
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- Genuine functorial transport by the ORIGINAL F19 chosen right
mate commutes with extracting BOTH Type-valued F19/F28 histories
from the F44 generated exchange quotient. -/
theorem chosenRightMateAxisTraceNaturality
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (exchange : Grid.ExchangeClass n m modsA modsB pqA pqB) :
    (chosenRightMateExchangeQuotientTransport F G K exchange).axisTraces =
      (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) exchange.axisTraces.1,
       Grid.AxisTrace.mapBlocks K exchange.axisTraces.2) :=
  Grid.ExchangeClass.axisTraces_mapBoth (rightMateFunctor F G) K exchange

/-- The FIRST genuine chosen right mate axis independently retains
its entire original primitive-step derivation (not merely a
composite equation after a full two-axis shuffle). -/
def chosenRightMateModificationAxisTrace
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat}
    (exchange : Grid.ExchangeClass n m modsA modsB pqA pqB) :
    Grid.AxisTrace n
      (Grid.mapBlocks (rightMateFunctor F G) modsA)
      (Grid.mapBlocks (rightMateFunctor F G) modsB) :=
  Grid.AxisTrace.mapBlocks (rightMateFunctor F G) exchange.axisTraces.1

/-- The original F19 chosen right mate preserves its native
categorical Hom evaluation by the ACTUAL transported axis history. -/
theorem chosenRightMateModificationAxis_composite_eq
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat}
    (exchange : Grid.ExchangeClass n m modsA modsB pqA pqB) :
    (Grid.mapBlocks (rightMateFunctor F G) modsA).composite =
      (Grid.mapBlocks (rightMateFunctor F G) modsB).composite :=
  (chosenRightMateModificationAxisTrace F G exchange).toTrace.composite_eq

#print axioms chosenRightMateAxisTraceNaturality
#print axioms chosenRightMateModificationAxisTrace
#print axioms chosenRightMateModificationAxis_composite_eq

end Generic
end

end KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateAxisTraceV5_142
