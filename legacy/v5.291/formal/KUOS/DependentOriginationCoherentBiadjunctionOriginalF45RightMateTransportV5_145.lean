import KUOS.DependentOriginationCoherentBiadjunctionF45TransportedHistoryReconciliationV5_145
import KUOS.DependentOriginationCoherentBiadjunctionOriginalMateNormalHistoriesV5_144

namespace KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RightMateTransportV5_145

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientMateCoherenceV5_141.Generic
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateNormalFormV5_143.Generic
open KUOS.DependentOriginationCoherentBiadjunctionOriginalMateNormalHistoriesV5_144.Generic

set_option autoImplicit false
noncomputable section

/-!
# F48-C / v5.145 — ORIGINAL F45 routes under genuine chosen right mates

F48-A/B eliminates the hitherto unresolved Eq.mp/Nat.zero_add
presentation difference of the actual old F45 Type-valued
modificationFirst/comparisonFirst paths and proves they retain
the exact same original F19 and F28 primitive histories.

F46's complete generated exchange characterization now identifies
both old routes with the independently constructed F47 native
normal paths, with no new exchange of same-axis steps.

This file connects this concrete result to the ORIGINAL F19 chosen
right-mate functor and a separate honest F28 compression-kernel
quotient-category functor. Original η, ε, F.mapId/F.mapComp ISOs,
and G.toOplax's potentially noninvertible forward comparisons remain
unchanged: F47's six actual source/target results apply to the
exact original histories extracted here.
-/

namespace Generic

universe uB vB wB uC vC wC uE vE
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- The TWO actual original F45 ordered routes, including their
Nat.zero_add Eq.mp casts, become the SAME original chosen-right-mate
exchange class under separate genuine F19/F28 category functors. -/
theorem chosenRightMateOriginalF45OrdersAgree
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat} {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (hm : Grid.AxisTrace n modsA modsB)
    (hc : Grid.AxisTrace m pqA pqB) :
    Grid.ExchangeClass.mapBoth (rightMateFunctor F G) K
      (Grid.AxisTrace.modificationFirst hm hc).toClass =
    Grid.ExchangeClass.mapBoth (rightMateFunctor F G) K
      (Grid.AxisTrace.comparisonFirst hm hc).toClass :=
  congrArg (Grid.ExchangeClass.mapBoth (rightMateFunctor F G) K)
    (Grid.AxisTrace.originalF45Orders_class_eq hm hc)

/-- ORIGINAL F45 F19-first path, not a new replacement route:
its genuine chosen right-mate transport has the complete F46
F28-first canonical history-pair classification. -/
theorem chosenRightMateOriginalF45ModificationFirstNormal
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat} {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (hm : Grid.AxisTrace n modsA modsB)
    (hc : Grid.AxisTrace m pqA pqB) :
    chosenRightMateExchangeQuotientTransport F G K
      (Grid.AxisTrace.toModificationFirstClass hm hc) =
    Grid.AxisTrace.pairToClass
      (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) hm,
       Grid.AxisTrace.mapBlocks K hc) := by
  calc
    chosenRightMateExchangeQuotientTransport F G K
        (Grid.AxisTrace.toModificationFirstClass hm hc) =
      chosenRightMateExchangeQuotientTransport F G K
        (Grid.AxisTrace.modificationNormal hm hc).toClass :=
      congrArg (chosenRightMateExchangeQuotientTransport F G K)
        (Grid.AxisTrace.originalF45_modificationFirst_eq_normalClass hm hc)
    _ = Grid.AxisTrace.pairToClass
          (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) hm,
           Grid.AxisTrace.mapBlocks K hc) :=
      chosenRightMateF19FirstNormalHistories F G K hm hc

/-- The SAME classification for the actual, OLD F45 F28-first path:
no new G-side inverse or cross-category Hom identification occurs. -/
theorem chosenRightMateOriginalF45ComparisonFirstNormal
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat} {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (hm : Grid.AxisTrace n modsA modsB)
    (hc : Grid.AxisTrace m pqA pqB) :
    chosenRightMateExchangeQuotientTransport F G K
      (Grid.AxisTrace.toComparisonFirstClass hm hc) =
    Grid.AxisTrace.pairToClass
      (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) hm,
       Grid.AxisTrace.mapBlocks K hc) := by
  calc
    chosenRightMateExchangeQuotientTransport F G K
        (Grid.AxisTrace.toComparisonFirstClass hm hc) =
      chosenRightMateExchangeQuotientTransport F G K
        (Grid.AxisTrace.toModificationFirstClass hm hc) :=
      congrArg (chosenRightMateExchangeQuotientTransport F G K)
        (Grid.AxisTrace.originalF45Orders_class_eq hm hc).symm
    _ = Grid.AxisTrace.pairToClass
          (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) hm,
           Grid.AxisTrace.mapBlocks K hc) :=
      chosenRightMateOriginalF45ModificationFirstNormal F G K hm hc

#print axioms chosenRightMateOriginalF45OrdersAgree
#print axioms chosenRightMateOriginalF45ModificationFirstNormal
#print axioms chosenRightMateOriginalF45ComparisonFirstNormal

end Generic
end
end KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RightMateTransportV5_145
