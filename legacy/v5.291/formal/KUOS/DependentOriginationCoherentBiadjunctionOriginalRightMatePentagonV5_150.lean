import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45PentagonTreesV5_150
import KUOS.DependentOriginationCoherentBiadjunctionBracketTreeRightMateCoherenceV5_149

namespace KUOS.DependentOriginationCoherentBiadjunctionOriginalRightMatePentagonV5_150

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
# F53-C / v5.150 — genuine ORIGINAL chosen F19 right-mate pentagon

Four arbitrary original F45 finite-bracket trees, each potentially
containing arbitrarily many ORIGINAL F45 primitive refinement stages,
yield the five exact F44 generated-exchange quotient vertices.

F53-A/B constructs both pentagon chains of original associators and
their separate symbolic Nat-depth transports. Here BOTH complete
chains survive under the ORIGINAL F19 chosen right-mate functor plus
an arbitrary honest F28 compression-kernel quotient functor.

The proof is about equality of original quotient classes and native
Type-valued primitive histories, never a new noninvertible mate
inverse or an unproved tricategorical 3-cell equality.
-/

namespace Generic

universe uB vB wB uC vC wC uE vE
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

section FourOriginalMateTrees

variable {a b : LeftMatePresentation F G}
variable {aF bF aG bG : C}
variable {x y : compressionKernelCategory aF bF aG bG}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ : Grid.Blocks a b}
variable {q₀ q₁ q₂ q₃ q₄ : Grid.Blocks x y}
variable
  (t₁ : Grid.OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : Grid.OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
  (t₃ : Grid.OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
  (t₄ : Grid.OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)
variable {T : Type uE} [Category.{vE} T]
variable (K : compressionKernelCategory aF bF aG bG ⥤ T)

/-- Actual LONG (three-edge) ORIGINAL chosen right-mate pentagon
coherence, for all four genuine F52 old F45 bracket trees. -/
theorem chosenRightMatePentagonLong :
    Grid.ExchangeClass.castDepths
      (Grid.F53Depth.long n₁ n₂ n₃ n₄)
      (Grid.F53Depth.long m₁ m₂ m₃ m₄)
      (chosenRightMateExchangeQuotientTransport F G K
        (Grid.OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄).toExchangeClass) =
    chosenRightMateExchangeQuotientTransport F G K
      (Grid.OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄).toExchangeClass := by
  calc
    _ = chosenRightMateExchangeQuotientTransport F G K
        ((Grid.OriginalF45BracketTree.castDepths
          (Grid.F53Depth.long n₁ n₂ n₃ n₄)
          (Grid.F53Depth.long m₁ m₂ m₃ m₄)
          (Grid.OriginalF45BracketTree.pentagon0
            t₁ t₂ t₃ t₄)).toExchangeClass) := by
      rw [Grid.OriginalF45BracketTree.castDepths_toExchangeClass]
      exact (Grid.ExchangeClass.mapBoth_castDepths
        (rightMateFunctor F G) K _ _ _).symm
    _ = chosenRightMateExchangeQuotientTransport F G K
        (Grid.OriginalF45BracketTree.pentagon3
          t₁ t₂ t₃ t₄).toExchangeClass :=
      congrArg (chosenRightMateExchangeQuotientTransport F G K)
        (Grid.OriginalF45BracketTree.pentagonLong t₁ t₂ t₃ t₄)

/-- Actual SHORT (two-edge) ORIGINAL chosen right-mate pentagon
coherence, with the SAME right-associated original F45 endpoint. -/
theorem chosenRightMatePentagonShort :
    Grid.ExchangeClass.castDepths
      (Grid.F53Depth.short n₁ n₂ n₃ n₄)
      (Grid.F53Depth.short m₁ m₂ m₃ m₄)
      (chosenRightMateExchangeQuotientTransport F G K
        (Grid.OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄).toExchangeClass) =
    chosenRightMateExchangeQuotientTransport F G K
      (Grid.OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄).toExchangeClass := by
  calc
    _ = chosenRightMateExchangeQuotientTransport F G K
        ((Grid.OriginalF45BracketTree.castDepths
          (Grid.F53Depth.short n₁ n₂ n₃ n₄)
          (Grid.F53Depth.short m₁ m₂ m₃ m₄)
          (Grid.OriginalF45BracketTree.pentagon0
            t₁ t₂ t₃ t₄)).toExchangeClass) := by
      rw [Grid.OriginalF45BracketTree.castDepths_toExchangeClass]
      exact (Grid.ExchangeClass.mapBoth_castDepths
        (rightMateFunctor F G) K _ _ _).symm
    _ = chosenRightMateExchangeQuotientTransport F G K
        (Grid.OriginalF45BracketTree.pentagon3
          t₁ t₂ t₃ t₄).toExchangeClass :=
      congrArg (chosenRightMateExchangeQuotientTransport F G K)
        (Grid.OriginalF45BracketTree.pentagonShort t₁ t₂ t₃ t₄)

/-- The entire ORIGINAL right-mate pentagon consists of BOTH explicit
chains with the SAME exact quotient endpoint, and agreement of BOTH
native finite-depth Nat transport witnesses. -/
theorem chosenRightMateFourfoldPentagon :
    (Grid.ExchangeClass.castDepths
      (Grid.F53Depth.long n₁ n₂ n₃ n₄)
      (Grid.F53Depth.long m₁ m₂ m₃ m₄)
      (chosenRightMateExchangeQuotientTransport F G K
        (Grid.OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄).toExchangeClass) =
     chosenRightMateExchangeQuotientTransport F G K
       (Grid.OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄).toExchangeClass) ∧
    (Grid.ExchangeClass.castDepths
      (Grid.F53Depth.short n₁ n₂ n₃ n₄)
      (Grid.F53Depth.short m₁ m₂ m₃ m₄)
      (chosenRightMateExchangeQuotientTransport F G K
        (Grid.OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄).toExchangeClass) =
     chosenRightMateExchangeQuotientTransport F G K
       (Grid.OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄).toExchangeClass) ∧
    (Grid.F53Depth.long n₁ n₂ n₃ n₄ =
      Grid.F53Depth.short n₁ n₂ n₃ n₄) ∧
    (Grid.F53Depth.long m₁ m₂ m₃ m₄ =
      Grid.F53Depth.short m₁ m₂ m₃ m₄) :=
  ⟨chosenRightMatePentagonLong F G t₁ t₂ t₃ t₄ K,
   chosenRightMatePentagonShort F G t₁ t₂ t₃ t₄ K,
   Grid.F53Depth.long_eq_short _ _ _ _,
   Grid.F53Depth.long_eq_short _ _ _ _⟩

/-- The original right mate pentagon LONG chain also preserves the
complete separately typed F19/F28 source and quotient histories. -/
theorem chosenRightMatePentagonLongHistories :
    (Grid.ExchangeClass.castDepths
      (Grid.F53Depth.long n₁ n₂ n₃ n₄)
      (Grid.F53Depth.long m₁ m₂ m₃ m₄)
      (chosenRightMateExchangeQuotientTransport F G K
        (Grid.OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄).toExchangeClass)).axisTraces =
    (chosenRightMateExchangeQuotientTransport F G K
      (Grid.OriginalF45BracketTree.pentagon3
        t₁ t₂ t₃ t₄).toExchangeClass).axisTraces :=
  congrArg Grid.ExchangeClass.axisTraces
    (chosenRightMatePentagonLong F G t₁ t₂ t₃ t₄ K)

/-- The same EXACT Type-valued original F19/F28 history result
holds for the short two-edge original right-mate pentagon route. -/
theorem chosenRightMatePentagonShortHistories :
    (Grid.ExchangeClass.castDepths
      (Grid.F53Depth.short n₁ n₂ n₃ n₄)
      (Grid.F53Depth.short m₁ m₂ m₃ m₄)
      (chosenRightMateExchangeQuotientTransport F G K
        (Grid.OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄).toExchangeClass)).axisTraces =
    (chosenRightMateExchangeQuotientTransport F G K
      (Grid.OriginalF45BracketTree.pentagon3
        t₁ t₂ t₃ t₄).toExchangeClass).axisTraces :=
  congrArg Grid.ExchangeClass.axisTraces
    (chosenRightMatePentagonShort F G t₁ t₂ t₃ t₄ K)

/-- At the final right-associated vertex, the ORIGINAL chosen F19
mate and genuine F28 functor still yield the ACTUAL selected old F45
total exchange-class route of the complete original histories. -/
theorem chosenRightMatePentagonRightNormal
    (order : Grid.OriginalF45Order) :
    chosenRightMateExchangeQuotientTransport F G K
      (Grid.OriginalF45BracketTree.pentagon3
        t₁ t₂ t₃ t₄).toExchangeClass =
    Grid.AxisTrace.originalF45OrderClass order
      (Grid.AxisTrace.mapBlocks (rightMateFunctor F G)
        (Grid.OriginalF45BracketTree.pentagon3
          t₁ t₂ t₃ t₄).axisHistories.1)
      (Grid.AxisTrace.mapBlocks K
        (Grid.OriginalF45BracketTree.pentagon3
          t₁ t₂ t₃ t₄).axisHistories.2) :=
  chosenRightMateBracketTreeNormal F G K
    (Grid.OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄) order

end FourOriginalMateTrees

#print axioms chosenRightMatePentagonLong
#print axioms chosenRightMatePentagonShort
#print axioms chosenRightMateFourfoldPentagon
#print axioms chosenRightMatePentagonLongHistories
#print axioms chosenRightMatePentagonShortHistories
#print axioms chosenRightMatePentagonRightNormal

end Generic
end
end KUOS.DependentOriginationCoherentBiadjunctionOriginalRightMatePentagonV5_150
