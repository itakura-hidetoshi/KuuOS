import KUOS.DependentOriginationCoherentBiadjunctionBracketTreeRegroupingV5_149
import KUOS.DependentOriginationCoherentBiadjunctionArbitraryFiniteRightMateV5_148

namespace KUOS.DependentOriginationCoherentBiadjunctionBracketTreeRightMateCoherenceV5_149

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientMateCoherenceV5_141.Generic
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryFiniteRightMateV5_148.Generic

set_option autoImplicit false
noncomputable section

/-!
# F52-C / v5.149 — original chosen right mates respect ALL finite parentheses

An arbitrary parenthesized genuine original F45 execution can contain
unboundedly many FINITE stages in an arbitrary binary tree. F52-A
establishes F44 quotient associativity up to the two dependent natural
number depth transports; F52-B proves compatibility with the
historical F51 snoc-list presentation and arbitrary separate functors.

Here the ORIGINAL chosen F19 right-mate functor and any independent
genuine F28 quotient-category functor preserve that whole binary
execution, its arbitrary tree reassociation, its total original
Type-valued axis histories, and its canonical order-selected total
F45 path. Nothing is identified merely from equality of Hom arrows.

Original source η / target ε and forward potentially noninvertible
G.toOplax comparisons are unchanged.
-/

namespace Generic

universe uB vB wB uC vC wC uE vE
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- An arbitrary genuinely BINARY-PARENTHESIZED original F45 run
transports through the original F19 chosen right-mate functor plus any
independent genuine F28 quotient-category functor, with all internal
bracketed original steps and all stage order choices retained. -/
theorem chosenRightMateBracketTreeNaturality
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (tree : Grid.OriginalF45BracketTree n m modsA pqA modsB pqB) :
    chosenRightMateExchangeQuotientTransport F G K
        tree.toExchangeClass =
      (Grid.OriginalF45BracketTree.mapBoth (rightMateFunctor F G) K
         tree).toExchangeClass :=
  Grid.OriginalF45BracketTree.mapBoth_toExchangeClass
    (rightMateFunctor F G) K tree

/-- A whole binary-parenthesized old F45 execution, transported by the
real chosen F19 mate and separately by any real F28 quotient functor,
equals ANY ORIGINAL order-selected total F45 route on its transported
complete typed primitive histories. -/
theorem chosenRightMateBracketTreeNormal
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (tree : Grid.OriginalF45BracketTree n m modsA pqA modsB pqB)
    (order : Grid.OriginalF45Order) :
    chosenRightMateExchangeQuotientTransport F G K
        tree.toExchangeClass =
      Grid.AxisTrace.originalF45OrderClass order
        (Grid.AxisTrace.mapBlocks (rightMateFunctor F G)
          tree.axisHistories.1)
        (Grid.AxisTrace.mapBlocks K tree.axisHistories.2) := by
  calc
    chosenRightMateExchangeQuotientTransport F G K
        tree.toExchangeClass =
      (Grid.OriginalF45BracketTree.mapBoth (rightMateFunctor F G) K
        tree).toExchangeClass :=
      chosenRightMateBracketTreeNaturality F G K tree
    _ = Grid.AxisTrace.originalF45OrderClass order
          (Grid.OriginalF45BracketTree.mapBoth
            (rightMateFunctor F G) K tree).axisHistories.1
          (Grid.OriginalF45BracketTree.mapBoth
            (rightMateFunctor F G) K tree).axisHistories.2 :=
      Grid.OriginalF45BracketTree.toExchangeClass_eq_originalF45 _ order
    _ = Grid.AxisTrace.originalF45OrderClass order
          (Grid.AxisTrace.mapBlocks (rightMateFunctor F G)
            tree.axisHistories.1)
          (Grid.AxisTrace.mapBlocks K tree.axisHistories.2) := by
      rw [Grid.OriginalF45BracketTree.mapBoth_axisHistories]

/-- The old F51 left-associated finite-stage list and its F52
binary-tree embedding give EXACTLY the SAME ORIGINAL chosen right-mate
exchange class. This is a genuinely finite-stage regrouping theorem,
not an equality of evaluated endpoint categorical Hom arrows. -/
theorem chosenRightMateStageChainBracketTree
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
      stages.toBracketTree.toExchangeClass =
    chosenRightMateExchangeQuotientTransport F G K
      stages.toExchangeClass :=
  congrArg (chosenRightMateExchangeQuotientTransport F G K)
    (Grid.OriginalF45Stages.toBracketTree_toExchangeClass stages)

/-- Genuine chosen original right mate coherence for changing the
PARENTHESES of three arbitrary subtrees, each itself with an
arbitrary finite number of original F45 stages. The two actual depth
casts are retained explicitly, so there is no false definitional
associativity claim for variable natural-number depths. -/
theorem chosenRightMateBracketTreeReassociate
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {n n' n'' m m' m'' : Nat}
    {modsA modsM modsN modsB : Grid.Blocks a b}
    {pqA pqM pqN pqB : Grid.Blocks x y}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (first : Grid.OriginalF45BracketTree n m modsA pqA modsM pqM)
    (second : Grid.OriginalF45BracketTree n' m' modsM pqM modsN pqN)
    (third : Grid.OriginalF45BracketTree n'' m'' modsN pqN modsB pqB) :
    chosenRightMateExchangeQuotientTransport F G K
      (Grid.OriginalF45BracketTree.castDepths
        (Nat.add_assoc n n' n'') (Nat.add_assoc m m' m'')
        (Grid.OriginalF45BracketTree.node
          (Grid.OriginalF45BracketTree.node first second) third)).toExchangeClass =
    chosenRightMateExchangeQuotientTransport F G K
      (Grid.OriginalF45BracketTree.node first
        (Grid.OriginalF45BracketTree.node second third)).toExchangeClass :=
  congrArg (chosenRightMateExchangeQuotientTransport F G K)
    (Grid.OriginalF45BracketTree.reassociate first second third)

/-- The entire bracketed original F45 run preserves BOTH original
categorical mate-side and quotient-side Hom composite equalities
after genuine chosen right-mate transport. -/
theorem chosenRightMateBracketTreeComposites
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (tree : Grid.OriginalF45BracketTree n m modsA pqA modsB pqB) :
    (Grid.mapBlocks (rightMateFunctor F G) modsA).composite =
      (Grid.mapBlocks (rightMateFunctor F G) modsB).composite ∧
    (Grid.mapBlocks K pqA).composite = (Grid.mapBlocks K pqB).composite :=
  (chosenRightMateExchangeQuotientTransport F G K
    tree.toExchangeClass).composites

/-- Exact full Type-valued history preservation by chosen F19 right
mate after ANY binary parenthesization of genuinely independent
original F19/F28 primitive histories. -/
theorem chosenRightMateBracketTreeHistories
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (tree : Grid.OriginalF45BracketTree n m modsA pqA modsB pqB) :
    (chosenRightMateExchangeQuotientTransport F G K
      tree.toExchangeClass).axisTraces =
      (Grid.AxisTrace.mapBlocks (rightMateFunctor F G)
        tree.axisHistories.1,
       Grid.AxisTrace.mapBlocks K tree.axisHistories.2) := by
  calc
    (chosenRightMateExchangeQuotientTransport F G K
      tree.toExchangeClass).axisTraces =
      (Grid.AxisTrace.mapBlocks (rightMateFunctor F G)
        tree.toExchangeClass.axisTraces.1,
       Grid.AxisTrace.mapBlocks K tree.toExchangeClass.axisTraces.2) :=
      Grid.ExchangeClass.axisTraces_mapBoth (rightMateFunctor F G) K _
    _ = (Grid.AxisTrace.mapBlocks (rightMateFunctor F G)
           tree.axisHistories.1,
         Grid.AxisTrace.mapBlocks K tree.axisHistories.2) := by
      rw [Grid.OriginalF45BracketTree.toExchangeClass_axisTraces]

#print axioms chosenRightMateBracketTreeNaturality
#print axioms chosenRightMateBracketTreeNormal
#print axioms chosenRightMateStageChainBracketTree
#print axioms chosenRightMateBracketTreeReassociate
#print axioms chosenRightMateBracketTreeComposites
#print axioms chosenRightMateBracketTreeHistories

end Generic
end
end KUOS.DependentOriginationCoherentBiadjunctionBracketTreeRightMateCoherenceV5_149
