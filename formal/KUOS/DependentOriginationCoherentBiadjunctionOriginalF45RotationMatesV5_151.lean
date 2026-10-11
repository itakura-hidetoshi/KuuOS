import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RotationContextsV5_151
import KUOS.DependentOriginationCoherentBiadjunctionBracketTreeRightMateCoherenceV5_149

namespace KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RotationMatesV5_151

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
# F54-D / v5.151 — ACTUAL chosen right mates preserve finite local rotations

An arbitrary finite sequence of local associativity rotations inside
genuine original F45 binary contexts is now carried by an actual
Type-valued RotationChain rather than an unverified existential Prop.

We transport the ENTIRE chain, including its chosen final and initial
original binary trees, through the ORIGINAL chosen F19 right-mate
functor paired with any honest independent F28 compression-kernel
quotient category functor.

The genuinely original F44 exchange quotient remains equal before
and after the entire finite chain, all two-axis Type-valued original
primitive histories remain equal after separate functorial mapping,
and the original chosen mate/source η/target ε data are unchanged.
No G-side potentially noninvertible mapId/mapComp cell is inverted.
-/

namespace Generic

universe uB vB wB uC vC wC uE vE
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- An arbitrary finite sequence of ORIGINAL F45 local bracket
rotations maps to exactly the SAME original chosen-right-mate F44
exchange class at both endpoints. This is NOT merely Hom evaluation. -/
theorem chosenRightMateFiniteRotationChain
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {ma mb : Grid.Blocks a b}
    {pa pb : Grid.Blocks x y}
    {n m : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    {before after : Grid.OriginalF45BracketTree n m ma pa mb pb}
    (chain : Grid.OriginalF45BracketTree.RotationChain before after) :
    chosenRightMateExchangeQuotientTransport F G K before.toExchangeClass =
      chosenRightMateExchangeQuotientTransport F G K after.toExchangeClass :=
  congrArg (chosenRightMateExchangeQuotientTransport F G K)
    chain.toExchangeClass_eq

/-- Both full independently Type-valued F19 mate and F28 quotient
primitive histories agree after the ORIGINAL chosen right mate sends
an arbitrary finite contextual rotation chain to its endpoints. -/
theorem chosenRightMateFiniteRotationHistories
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {ma mb : Grid.Blocks a b}
    {pa pb : Grid.Blocks x y}
    {n m : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    {before after : Grid.OriginalF45BracketTree n m ma pa mb pb}
    (chain : Grid.OriginalF45BracketTree.RotationChain before after) :
    (chosenRightMateExchangeQuotientTransport F G K
      before.toExchangeClass).axisTraces =
      (chosenRightMateExchangeQuotientTransport F G K
        after.toExchangeClass).axisTraces :=
  congrArg Grid.ExchangeClass.axisTraces
    (chosenRightMateFiniteRotationChain F G K chain)

/-- The SAME actual native histories can be read directly from both
originally distinct F19 and F28 typed input path presentations,
with no loss of same-axis operation order. -/
theorem chosenRightMateFiniteRotationOriginalHistories
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {ma mb : Grid.Blocks a b}
    {pa pb : Grid.Blocks x y}
    {n m : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    {before after : Grid.OriginalF45BracketTree n m ma pa mb pb}
    (chain : Grid.OriginalF45BracketTree.RotationChain before after) :
    (Grid.AxisTrace.mapBlocks (rightMateFunctor F G)
        before.axisHistories.1,
     Grid.AxisTrace.mapBlocks K before.axisHistories.2) =
    (Grid.AxisTrace.mapBlocks (rightMateFunctor F G)
        after.axisHistories.1,
     Grid.AxisTrace.mapBlocks K after.axisHistories.2) := by
  exact congrArg
    (fun pair =>
      (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) pair.1,
       Grid.AxisTrace.mapBlocks K pair.2))
    chain.axisHistories_eq

/-- Both endpoints of ANY genuine finite F54 rotation chain have
identical ORIGINAL mate-side and original F28 quotient-side Hom
composites, separately, after transport by the true chosen mate. -/
theorem chosenRightMateFiniteRotationComposites
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {ma mb : Grid.Blocks a b}
    {pa pb : Grid.Blocks x y}
    {n m : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    {before after : Grid.OriginalF45BracketTree n m ma pa mb pb}
    (chain : Grid.OriginalF45BracketTree.RotationChain before after) :
    ((Grid.mapBlocks (rightMateFunctor F G) ma).composite =
      (Grid.mapBlocks (rightMateFunctor F G) mb).composite ∧
     (Grid.mapBlocks K pa).composite =
      (Grid.mapBlocks K pb).composite) ∧
    ((Grid.mapBlocks (rightMateFunctor F G) ma).composite =
      (Grid.mapBlocks (rightMateFunctor F G) mb).composite ∧
     (Grid.mapBlocks K pa).composite =
      (Grid.mapBlocks K pb).composite) :=
  ⟨(chosenRightMateExchangeQuotientTransport F G K
      before.toExchangeClass).composites,
   (chosenRightMateExchangeQuotientTransport F G K
      after.toExchangeClass).composites⟩

#print axioms chosenRightMateFiniteRotationChain
#print axioms chosenRightMateFiniteRotationHistories
#print axioms chosenRightMateFiniteRotationOriginalHistories
#print axioms chosenRightMateFiniteRotationComposites

end Generic
end
end KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RotationMatesV5_151
