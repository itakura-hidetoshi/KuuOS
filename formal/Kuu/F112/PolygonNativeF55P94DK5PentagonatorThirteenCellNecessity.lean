import Kuu.F112.PolygonNativeF55P94DK5ThirteenCellTwelveGroupoid
import Mathlib.Tactic

/-!
# F112-P94D3AK — genuine C60 K5 thirteen-cell comparison

Specialize the 13D comparison to the exact five ORIGINAL F45 stages
and independent Type-valued K5 pentagonator. The two original
dependent 12D inverse-square paths have equal 11D endpoints
and equal integer charges, but unequal noncommutative histories.
An independent 13D Type-valued squareExchange identifies their
12D classes. The chosen conservative 13D grammar cannot compare
them, relative to the explicitly selected free-group observer.

No arbitrary higher coherence, old P92B complete descent,
global strict 3/n or (∞,3)-hyperdescent is claimed.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section GenuineFiveStage

variable {p : Polygon} {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
variable
  (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
  (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
  (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
  (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
  (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)

/-- The new genuine Type-valued 13D comparison at the ORIGINAL
K5 12D critical pair; not an equality of distinct raw 12D terms. -/
def nativeK5PentagonatorThirteenExchange :=
  NativeK5StructuralThirteenCell.squareExchange
    (nativeK5PentagonatorThirteenExchangeTwelve t1 t2 t3 t4 t5)

/-- Explicit non-conservative nature of original 13D exchange,
relative to the named conservative 13D grammar. -/
theorem nativeK5PentagonatorThirteen_relativeNecessity :
    Nonempty (NativeK5StructuralThirteenCell p
      (nativeK5PentagonatorThirteenLeftFirst t1 t2 t3 t4 t5)
      (nativeK5PentagonatorThirteenRightFirst t1 t2 t3 t4 t5)) ∧
    ¬ Nonempty (NativeK5CoreThirteenCell p
      (nativeK5PentagonatorThirteenLeftFirst t1 t2 t3 t4 t5)
      (nativeK5PentagonatorThirteenRightFirst t1 t2 t3 t4 t5)) :=
  nativeK5TwelveSquareExchange_thirteenRelativeNecessity
    (nativeK5PentagonatorTwelveExchangeEleven t1 t2 t3 t4 t5)

/-- Quotient equality comes ONLY from an original genuine 13D
typed witness, not from raw equality of 12D proof terms. -/
theorem nativeK5PentagonatorThirteen_quotient_eq :
    nativeK5ThirteenCellTwelveClass
      (nativeK5PentagonatorThirteenLeftFirst t1 t2 t3 t4 t5) =
    nativeK5ThirteenCellTwelveClass
      (nativeK5PentagonatorThirteenRightFirst t1 t2 t3 t4 t5) :=
  nativeK5TwelvePasting_thirteenQuotient_eq
    (nativeK5PentagonatorThirteenExchangeTwelve t1 t2 t3 t4 t5)

/-- The signed integer observer descends, and cannot distinguish
the two original C60 12D pasting orders after 13D quotienting. -/
theorem nativeK5PentagonatorThirteen_integerDescent :
    nativeK5ThirteenCellTwelveSquareCount
      (nativeK5ThirteenCellTwelveClass
        (nativeK5PentagonatorThirteenLeftFirst t1 t2 t3 t4 t5)) =
    nativeK5ThirteenCellTwelveSquareCount
      (nativeK5ThirteenCellTwelveClass
        (nativeK5PentagonatorThirteenRightFirst t1 t2 t3 t4 t5)) :=
  congrArg nativeK5ThirteenCellTwelveSquareCount
    (nativeK5PentagonatorThirteen_quotient_eq t1 t2 t3 t4 t5)

/-- The chosen free-group history fails the exact 13D descent
criterion even though the signed 12D count descends. -/
def nativeK5PentagonatorThirteen_historyNoDescent :=
  nativeK5TwelveHistoryWord_noThirteenDescent
    (nativeK5PentagonatorThirteenExchangeTwelve t1 t2 t3 t4 t5)
    (nativeK5PentagonatorThirteen_history_ne t1 t2 t3 t4 t5)

/-- A boundary-preserving retraction of the extended source
grammar back to the conservative 13D grammar cannot exist. -/
theorem nativeK5PentagonatorThirteen_noCoreRetraction :
    ¬ Nonempty
      (NativeK5StructuralThirteenCell p
        (nativeK5PentagonatorThirteenLeftFirst t1 t2 t3 t4 t5)
        (nativeK5PentagonatorThirteenRightFirst t1 t2 t3 t4 t5) →
       NativeK5CoreThirteenCell p
        (nativeK5PentagonatorThirteenLeftFirst t1 t2 t3 t4 t5)
        (nativeK5PentagonatorThirteenRightFirst t1 t2 t3 t4 t5)) :=
  nativeK5TwelveSquareExchange_thirteenNoCoreRetraction
    (nativeK5PentagonatorTwelveExchangeEleven t1 t2 t3 t4 t5)

#print axioms nativeK5PentagonatorThirteenExchange
#print axioms nativeK5PentagonatorThirteen_relativeNecessity
#print axioms nativeK5PentagonatorThirteen_quotient_eq
#print axioms nativeK5PentagonatorThirteen_integerDescent
#print axioms nativeK5PentagonatorThirteen_historyNoDescent
#print axioms nativeK5PentagonatorThirteen_noCoreRetraction

end GenuineFiveStage
end
end Kuu.F112.Physical
