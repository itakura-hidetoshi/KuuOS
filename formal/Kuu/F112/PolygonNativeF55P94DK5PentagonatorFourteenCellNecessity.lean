import Kuu.F112.PolygonNativeF55P94DK5FourteenCellThirteenGroupoid
import Mathlib.Tactic

/-!
# F112-P94D3AM — actual five-stage C60 K5 FOURTEEN-cell comparison

At the ORIGINAL five source-dependent F45 stages of the C60
K5 pentagonator, the genuine 13D squareExchange from AK is
a source-typed 13-cell. Its two inverse-square 13D pasting paths
were constructed in AL with exactly the same original 12D endpoints,
equal signed 13D count and unequal chosen free-group histories.

The named conservative 14D grammar cannot fill this critical pair;
an independently adjoined Type-valued 14D squareExchange does.
Their raw thirteen-cell terms are NOT equal. Equality holds only
after 14D quotienting. The signed count descends; the chosen
noncommutative history does not. All obstruction statements are
relative to the selected presentation and history observer.
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

/-- The genuine, independent 14D Type-valued comparison generator
is applied to the exact ORIGINAL five-stage 13D K5 exchange. -/
def nativeK5PentagonatorFourteenExchange :=
  NativeK5StructuralFourteenCell.squareExchange
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)

/-- Extended comparison exists, but conservative comparison does
not exist at this exact original source-dependent K5 boundary. -/
theorem nativeK5PentagonatorFourteen_relativeNecessity :
    Nonempty (NativeK5StructuralFourteenCell p
      (nativeK5PentagonatorFourteenLeftFirst t1 t2 t3 t4 t5)
      (nativeK5PentagonatorFourteenRightFirst t1 t2 t3 t4 t5)) ∧
    ¬ Nonempty (NativeK5CoreFourteenCell p
      (nativeK5PentagonatorFourteenLeftFirst t1 t2 t3 t4 t5)
      (nativeK5PentagonatorFourteenRightFirst t1 t2 t3 t4 t5)) :=
  nativeK5ThirteenSquareExchange_fourteenRelativeNecessity
    (nativeK5PentagonatorThirteenExchangeTwelve t1 t2 t3 t4 t5)

/-- Equality is ONLY in the genuine 14D quotient, not on
raw source-typed thirteen-cell terms. -/
theorem nativeK5PentagonatorFourteen_quotient_eq :
    nativeK5FourteenCellThirteenClass
      (nativeK5PentagonatorFourteenLeftFirst t1 t2 t3 t4 t5) =
    nativeK5FourteenCellThirteenClass
      (nativeK5PentagonatorFourteenRightFirst t1 t2 t3 t4 t5) :=
  nativeK5ThirteenPasting_fourteenQuotient_eq
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)

/-- Scalar observer descends to the true 14D quotient, even
though the chosen noncommutative history fails to descend. -/
theorem nativeK5PentagonatorFourteen_integerDescent :
    nativeK5FourteenCellThirteenSquareCount
      (nativeK5FourteenCellThirteenClass
        (nativeK5PentagonatorFourteenLeftFirst t1 t2 t3 t4 t5)) =
    nativeK5FourteenCellThirteenSquareCount
      (nativeK5FourteenCellThirteenClass
        (nativeK5PentagonatorFourteenRightFirst t1 t2 t3 t4 t5)) :=
  congrArg nativeK5FourteenCellThirteenSquareCount
    (nativeK5PentagonatorFourteen_quotient_eq t1 t2 t3 t4 t5)

/-- The selected free-group history cannot descend across the
genuine 14D K5 quotient. -/
def nativeK5PentagonatorFourteen_historyNoDescent :=
  nativeK5ThirteenHistoryWord_noFourteenDescent
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)
    (nativeK5PentagonatorFourteen_history_ne t1 t2 t3 t4 t5)

/-- No boundary-preserving retraction to the named conservative
14D source grammar is possible at the genuine five-stage K5 pair. -/
theorem nativeK5PentagonatorFourteen_noCoreRetraction :
    ¬ Nonempty
      (NativeK5StructuralFourteenCell p
        (nativeK5PentagonatorFourteenLeftFirst t1 t2 t3 t4 t5)
        (nativeK5PentagonatorFourteenRightFirst t1 t2 t3 t4 t5) →
       NativeK5CoreFourteenCell p
        (nativeK5PentagonatorFourteenLeftFirst t1 t2 t3 t4 t5)
        (nativeK5PentagonatorFourteenRightFirst t1 t2 t3 t4 t5)) :=
  nativeK5ThirteenSquareExchange_fourteenNoCoreRetraction
    (nativeK5PentagonatorThirteenExchangeTwelve t1 t2 t3 t4 t5)

#print axioms nativeK5PentagonatorFourteenExchange
#print axioms nativeK5PentagonatorFourteen_relativeNecessity
#print axioms nativeK5PentagonatorFourteen_quotient_eq
#print axioms nativeK5PentagonatorFourteen_integerDescent
#print axioms nativeK5PentagonatorFourteen_historyNoDescent
#print axioms nativeK5PentagonatorFourteen_noCoreRetraction

end GenuineFiveStage
end
end Kuu.F112.Physical
