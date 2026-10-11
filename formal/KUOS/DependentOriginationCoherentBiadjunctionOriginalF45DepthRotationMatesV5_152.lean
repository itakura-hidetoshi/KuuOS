import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45DepthRotationInvariantsV5_152
import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RotationMatesV5_151

namespace KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RotationMatesV5_152

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientMateCoherenceV5_141.Generic
open KUOS.DependentOriginationCoherentBiadjunctionBracketTreeRightMateCoherenceV5_149.Generic

set_option autoImplicit false
noncomputable section

/-!
# F55-C2 / v5.152 — original chosen mate on genuine depth-bridged F55 routes

Unlike F54's fixed-index RotationChain, the original F55
DepthRotationRoute stores its actual F54 rotation witnesses with BOTH
original independently typed F19 and F28 Nat-depth transports. F55-C1
proves the complete genuine F44 endpoint and history preservation
through all path constructors, including contextual whiskering,
concatenation, and both original pentagon and square paths.

We transport THESE proved results along the ORIGINAL chosen F19
right-mate functor and an arbitrary independently honest functor on
the genuinely distinct F28 compression-kernel quotient category.
Original source/target pseudofunctors, nonstrict comparators and the
direction of potentially noninvertible G.toOplax cells are unchanged.

The F55-B PresentedCell is a free Type-valued path-cell presentation:
these statements certify its two physical endpoint F44 invariants,
not an identification with external tricategorical 3-morphisms.
-/

namespace Generic

universe uB vB wB uC vC wC uE vE
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- The original chosen F19 mate and actual independent F28 quotient
transport an arbitrary F55 indexed original-rotation route to equal
F44 exchange classes, AFTER BOTH original separate Nat-depth casts. -/
theorem chosenRightMateDepthRotationRoute
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {ma mb : Grid.Blocks a b}
    {pa pb : Grid.Blocks x y}
    {n n' m m' : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    {before : Grid.OriginalF45BracketTree n m ma pa mb pb}
    {after : Grid.OriginalF45BracketTree n' m' ma pa mb pb}
    (route : Grid.OriginalF45BracketTree.DepthRotationRoute before after) :
    chosenRightMateExchangeQuotientTransport F G K
      (Grid.OriginalF45BracketTree.castDepths
        route.depthEq.1 route.depthEq.2 before).toExchangeClass =
    chosenRightMateExchangeQuotientTransport F G K
      after.toExchangeClass := by
  apply congrArg (chosenRightMateExchangeQuotientTransport F G K)
  exact (Grid.OriginalF45BracketTree.castDepths_toExchangeClass
    route.depthEq.1 route.depthEq.2 before).trans route.toExchangeClass_eq

/-- Independent original depth transports genuinely COMMUTE with
BOTH chosen original mate and arbitrary honest F28 quotient functors.
No cross-identification of the two axes or inversion of lax cells. -/
theorem chosenRightMateDepthRotationRoute_castCommutes
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {ma mb : Grid.Blocks a b}
    {pa pb : Grid.Blocks x y}
    {n n' m m' : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    {before : Grid.OriginalF45BracketTree n m ma pa mb pb}
    {after : Grid.OriginalF45BracketTree n' m' ma pa mb pb}
    (route : Grid.OriginalF45BracketTree.DepthRotationRoute before after) :
    chosenRightMateExchangeQuotientTransport F G K
      (Grid.ExchangeClass.castDepths
        route.depthEq.1 route.depthEq.2 before.toExchangeClass) =
    Grid.ExchangeClass.castDepths route.depthEq.1 route.depthEq.2
      (chosenRightMateExchangeQuotientTransport F G K
        before.toExchangeClass) := by
  exact Grid.ExchangeClass.mapBoth_castDepths
    (rightMateFunctor F G) K
    route.depthEq.1 route.depthEq.2 before.toExchangeClass

/-- The original chosen F19 mate and separately genuine F28 quotient
functors preserve BOTH COMPLETE typed primitive histories after the
actual F55 double-depth transports, not just evaluation of Hom
composites or mere numbers of rotations. -/
theorem chosenRightMateDepthRotationRoute_histories
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {ma mb : Grid.Blocks a b}
    {pa pb : Grid.Blocks x y}
    {n n' m m' : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    {before : Grid.OriginalF45BracketTree n m ma pa mb pb}
    {after : Grid.OriginalF45BracketTree n' m' ma pa mb pb}
    (route : Grid.OriginalF45BracketTree.DepthRotationRoute before after) :
    (Grid.AxisTrace.mapBlocks (rightMateFunctor F G)
        (Grid.OriginalF45BracketTree.castDepths
          route.depthEq.1 route.depthEq.2 before).axisHistories.1,
     Grid.AxisTrace.mapBlocks K
        (Grid.OriginalF45BracketTree.castDepths
          route.depthEq.1 route.depthEq.2 before).axisHistories.2) =
    (Grid.AxisTrace.mapBlocks (rightMateFunctor F G)
        after.axisHistories.1,
     Grid.AxisTrace.mapBlocks K after.axisHistories.2) := by
  exact congrArg
    (fun pair =>
      (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) pair.1,
       Grid.AxisTrace.mapBlocks K pair.2))
    route.axisHistories_eq

/-- The F44 quotient itself retains both full typed native histories
after chosen F19 mate and independent F28 quotient transport of any
cast-indexed original F55 route. -/
theorem chosenRightMateDepthRotationRoute_classHistories
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {ma mb : Grid.Blocks a b}
    {pa pb : Grid.Blocks x y}
    {n n' m m' : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    {before : Grid.OriginalF45BracketTree n m ma pa mb pb}
    {after : Grid.OriginalF45BracketTree n' m' ma pa mb pb}
    (route : Grid.OriginalF45BracketTree.DepthRotationRoute before after) :
    (chosenRightMateExchangeQuotientTransport F G K
      (Grid.OriginalF45BracketTree.castDepths
        route.depthEq.1 route.depthEq.2 before).toExchangeClass).axisTraces =
    (chosenRightMateExchangeQuotientTransport F G K
      after.toExchangeClass).axisTraces :=
  congrArg Grid.ExchangeClass.axisTraces
    (chosenRightMateDepthRotationRoute F G K route)

/-- The actual F55-B presented higher cell keeps BOTH distinct
concrete routes and certifies their separate original chosen-mate
F44 boundary equalities. The Type-valued presented cell is never
silently replaced with equality of the two raw route constructors. -/
theorem chosenRightMatePresentedRotationCell
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {ma mb : Grid.Blocks a b}
    {pa pb : Grid.Blocks x y}
    {n n' m m' : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    {before : Grid.OriginalF45BracketTree n m ma pa mb pb}
    {after : Grid.OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : Grid.OriginalF45BracketTree.DepthRotationRoute before after}
    (_cell : Grid.OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    (chosenRightMateExchangeQuotientTransport F G K
      (Grid.OriginalF45BracketTree.castDepths
        r.depthEq.1 r.depthEq.2 before).toExchangeClass =
     chosenRightMateExchangeQuotientTransport F G K after.toExchangeClass)
    ∧
    (chosenRightMateExchangeQuotientTransport F G K
      (Grid.OriginalF45BracketTree.castDepths
        s.depthEq.1 s.depthEq.2 before).toExchangeClass =
     chosenRightMateExchangeQuotientTransport F G K after.toExchangeClass) :=
  ⟨chosenRightMateDepthRotationRoute F G K r,
   chosenRightMateDepthRotationRoute F G K s⟩

#print axioms chosenRightMateDepthRotationRoute
#print axioms chosenRightMateDepthRotationRoute_castCommutes
#print axioms chosenRightMateDepthRotationRoute_histories
#print axioms chosenRightMateDepthRotationRoute_classHistories
#print axioms chosenRightMatePresentedRotationCell

end Generic
end
end KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RotationMatesV5_152
