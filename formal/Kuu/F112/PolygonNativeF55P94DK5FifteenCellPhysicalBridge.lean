import Kuu.F112.PolygonNativeF55P94DK5FourteenCellNonabelianPasting
import Kuu.F112.PolygonNativeF55P94DObserverFifteenCellDescent
import Mathlib.Tactic

/-!
# F112-P94D3AO — original C60 K5 source-dependent fifteen-cell bridge

Instantiate the universal Type-valued observer-conservative 15D
presentation at the EXACT ORIGINAL source-dependent fourteen-cell fiber.
The raw 14D witnesses are the genuinely distinct left-first/right-first
inverse-square pastings of the actual original fourteen-cell generator.

Use the previously proved noncommutative free-history separation and
integer blindness, not assumed equalities. The separately ADJOINED
Type-valued 15D squareExchange makes their 15D classes equal; raw terms
remain unequal. Finite conservative closure and no-retraction are
presentation-relative to the named MAXIMAL observer-conservative grammar.

This file does not claim that the observer-conservative grammar is the
complete original geometric fifteen-cell grammar, or arbitrary
higher coherence, old P92B descent, global strict 3/n or hyperdescent.
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

section OriginalFourteenCellFiber

variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {alpha beta : NativeK5StructuralFourCell p f g}
variable {w z : NativeK5StructuralFiveCell p alpha beta}
variable {u v : NativeK5StructuralSixCell p w z}
variable {h k : NativeK5StructuralSevenCell p u v}
variable {e d : NativeK5StructuralEightCell p h k}
variable {q t : NativeK5StructuralNineCell p e d}
variable {P Q : NativeK5StructuralTenCell p q t}
variable {H K : NativeK5StructuralElevenCell p P Q}
variable {U V : NativeK5StructuralTwelveCell p H K}

/-- EXACT original thirteen-cell boundaries for both pastings:
there is no graph or type-erasing strictification in this carrier. -/
abbrev NativeK5FifteenFourteenFiber
    (W : NativeK5StructuralThirteenCell p U V) :=
  NativeK5StructuralFourteenCell p
    (.trans (nativeK5ThirteenPastingLeftThenRight W)
      (.symm (nativeK5ThirteenPastingLeftThenRight W)))
    (.trans (nativeK5ThirteenPastingRightThenLeft W)
      (.symm (nativeK5ThirteenPastingRightThenLeft W)))

/-- First true raw fourteen-cell pasting of the independent 14D exchange. -/
def nativeK5FifteenCriticalLeft
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeK5FifteenFourteenFiber W :=
  nativeK5FourteenPastingLeftThenRight
    (NativeK5StructuralFourteenCell.squareExchange W)

/-- Second true raw fourteen-cell pasting, SAME thirteen-cell boundaries. -/
def nativeK5FifteenCriticalRight
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeK5FifteenFourteenFiber W :=
  nativeK5FourteenPastingRightThenLeft
    (NativeK5StructuralFourteenCell.squareExchange W)

/-- Name the exact original 14-cell free-word observer once.
This abbreviation retains the unmodified source-dependent fiber. -/
abbrev nativeK5FifteenHistoryObserver
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeK5FifteenFourteenFiber W → NativeK5FourteenHistoryWord :=
  fun R => R.historyWord

/-- The independent signed observer on the same exact 14-cell fiber. -/
abbrev nativeK5FifteenChargeObserver
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeK5FifteenFourteenFiber W → ℤ :=
  fun R => R.squareCount

/-- Source-dependent fifteen-cell conservative grammar on original 14D proofs.
Its observer-compatibility atom is explicit and maximal. -/
abbrev NativeK5FifteenCorePresentation
    (W : NativeK5StructuralThirteenCell p U V)
    (X Y : NativeK5FifteenFourteenFiber W) :=
  NativeObserverCoreFifteenCell
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W) X Y

/-- Extended, genuine Type-valued 15D syntax on the exact original fiber.
Its new squareExchange is an independent constructor, not raw equality. -/
abbrev NativeK5FifteenExtendedPresentation
    (W : NativeK5StructuralThirteenCell p U V)
    (X Y : NativeK5FifteenFourteenFiber W) :=
  NativeObserverExtendedFifteenCell
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5FifteenCriticalLeft W)
    (nativeK5FifteenCriticalRight W) X Y

/-- Independent fifteen-cell comparison between the two actual original
fourteen-cell witnesses. Integer blindness is its explicit charge evidence. -/
def nativeK5FifteenSquareExchange
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeK5FifteenExtendedPresentation W
      (nativeK5FifteenCriticalLeft W)
      (nativeK5FifteenCriticalRight W) :=
  .squareExchange
    (nativeK5FourteenPasting_integerBlind
      (NativeK5StructuralFourteenCell.squareExchange W))

/-- The two original fourteen-cell witnesses remain distinct before
quotienting. The added fifteen-cell comparison is NOT a raw equality. -/
theorem nativeK5Fifteen_raw_ne
    (W : NativeK5StructuralThirteenCell p U V) :
    nativeK5FifteenCriticalLeft W ≠ nativeK5FifteenCriticalRight W := by
  exact nativeK5FourteenSquareExchange_pastingRaw_ne W

/-- The extended 15D evidence exists and the maximal conservative
observer grammar cannot fill the SAME original boundary. -/
theorem nativeK5Fifteen_relativeNecessity
    (W : NativeK5StructuralThirteenCell p U V) :
    Nonempty (NativeK5FifteenExtendedPresentation W
      (nativeK5FifteenCriticalLeft W)
      (nativeK5FifteenCriticalRight W)) ∧
    ¬ Nonempty (NativeK5FifteenCorePresentation W
      (nativeK5FifteenCriticalLeft W)
      (nativeK5FifteenCriticalRight W)) := by
  constructor
  · exact ⟨nativeK5FifteenSquareExchange W⟩
  · rintro ⟨h⟩
    exact (nativeK5FourteenSquareExchange_pastingWord_ne W)
      h.history_sound

/-- No FINITE conservative observer closure bridges the original 14D pair. -/
theorem nativeK5Fifteen_noFiniteCoreFiller
    (W : NativeK5StructuralThirteenCell p U V)
    (depth : Nat) :
    ¬ Nonempty (NativeConservativeTower
      (NativeK5FifteenCorePresentation W)
      depth
      (nativeK5FifteenCriticalLeft W)
      (nativeK5FifteenCriticalRight W)) :=
  nativeObserverFifteen_noFiniteCoreFiller
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5FourteenSquareExchange_pastingWord_ne W) depth

/-- Independently generated fifteen-cell evidence cannot be retracted
to any finite stage of the specifically named conservative grammar. -/
theorem nativeK5Fifteen_noFiniteCoreRetraction
    (W : NativeK5StructuralThirteenCell p U V)
    (depth : Nat) :
    ¬ Nonempty
      (NativeK5FifteenExtendedPresentation W
         (nativeK5FifteenCriticalLeft W)
         (nativeK5FifteenCriticalRight W) →
       NativeConservativeTower (NativeK5FifteenCorePresentation W)
         depth (nativeK5FifteenCriticalLeft W)
         (nativeK5FifteenCriticalRight W)) :=
  nativeObserverFifteen_noFiniteCoreRetraction
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5FifteenCriticalLeft W)
    (nativeK5FifteenCriticalRight W)
    (nativeK5FourteenPasting_integerBlind
      (NativeK5StructuralFourteenCell.squareExchange W))
    (nativeK5FourteenSquareExchange_pastingWord_ne W) depth

/-- Local 15D quotient of ORIGINAL raw fourteen-cell evidence. -/
abbrev NativeK5FifteenFourteenClasses
    (W : NativeK5StructuralThirteenCell p U V) :=
  NativeObserverFifteenClasses
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5FifteenCriticalLeft W)
    (nativeK5FifteenCriticalRight W)

def nativeK5FifteenClass
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    NativeK5FifteenFourteenClasses W :=
  Quotient.mk _ R

/-- Equality is ONLY at the independent fifteen-cell quotient level. -/
theorem nativeK5Fifteen_quotient_eq
    (W : NativeK5StructuralThirteenCell p U V) :
    nativeK5FifteenClass W (nativeK5FifteenCriticalLeft W) =
    nativeK5FifteenClass W (nativeK5FifteenCriticalRight W) :=
  nativeObserverFifteen_square_quotient_eq
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5FifteenCriticalLeft W)
    (nativeK5FifteenCriticalRight W)
    (nativeK5FourteenPasting_integerBlind
      (NativeK5StructuralFourteenCell.squareExchange W))

/-- Signed original fourteen-cell square count descends along 15D. -/
def nativeK5FifteenCharge
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeK5FifteenFourteenClasses W → ℤ :=
  nativeObserverFifteenCharge
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5FifteenCriticalLeft W)
    (nativeK5FifteenCriticalRight W)

theorem nativeK5Fifteen_chargeDescent
    (W : NativeK5StructuralThirteenCell p U V) :
    nativeK5FifteenCharge W
      (nativeK5FifteenClass W (nativeK5FifteenCriticalLeft W)) =
    nativeK5FifteenCharge W
      (nativeK5FifteenClass W (nativeK5FifteenCriticalRight W)) :=
  congrArg (nativeK5FifteenCharge W) (nativeK5Fifteen_quotient_eq W)

/-- The original nonabelian free-word observer has NO factorization
through this chosen fifteen-cell quotient. -/
theorem nativeK5Fifteen_historyNoDescent
    (W : NativeK5StructuralThirteenCell p U V) :
    ¬ ∃ F : NativeK5FifteenFourteenClasses W → NativeK5FourteenHistoryWord,
      ∀ R : NativeK5FifteenFourteenFiber W,
        F (nativeK5FifteenClass W R) = R.historyWord :=
  nativeObserverFifteen_history_noDescent
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5FifteenCriticalLeft W)
    (nativeK5FifteenCriticalRight W)
    (nativeK5FourteenPasting_integerBlind
      (NativeK5StructuralFourteenCell.squareExchange W))
    (nativeK5FourteenSquareExchange_pastingWord_ne W)

end OriginalFourteenCellFiber

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

/-- Specialize the observer-based fifteen-cell relative necessity
to the five actual source-dependent C60 F45 K5 stages. -/
theorem nativeK5PentagonatorFifteen_relativeNecessity :
    Nonempty (NativeK5FifteenExtendedPresentation
      (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)
      (nativeK5PentagonatorFifteenLeftFirst t1 t2 t3 t4 t5)
      (nativeK5PentagonatorFifteenRightFirst t1 t2 t3 t4 t5)) ∧
    ¬ Nonempty (NativeK5FifteenCorePresentation
      (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)
      (nativeK5PentagonatorFifteenLeftFirst t1 t2 t3 t4 t5)
      (nativeK5PentagonatorFifteenRightFirst t1 t2 t3 t4 t5)) :=
  nativeK5Fifteen_relativeNecessity
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)

theorem nativeK5PentagonatorFifteen_quotient_eq :
    nativeK5FifteenClass
      (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)
      (nativeK5PentagonatorFifteenLeftFirst t1 t2 t3 t4 t5) =
    nativeK5FifteenClass
      (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)
      (nativeK5PentagonatorFifteenRightFirst t1 t2 t3 t4 t5) :=
  nativeK5Fifteen_quotient_eq
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)

theorem nativeK5PentagonatorFifteen_historyNoDescent :
    ¬ ∃ F : NativeK5FifteenFourteenClasses
        (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5) →
          NativeK5FourteenHistoryWord,
      ∀ R : NativeK5FifteenFourteenFiber
        (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5),
        F (nativeK5FifteenClass
          (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)
          R) = R.historyWord :=
  nativeK5Fifteen_historyNoDescent
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)

end GenuineFiveStage

#print axioms NativeK5FifteenFourteenFiber
#print axioms nativeK5FifteenCriticalLeft
#print axioms nativeK5FifteenCriticalRight
#print axioms nativeK5FifteenHistoryObserver
#print axioms nativeK5FifteenChargeObserver
#print axioms NativeK5FifteenCorePresentation
#print axioms NativeK5FifteenExtendedPresentation
#print axioms nativeK5FifteenSquareExchange
#print axioms nativeK5Fifteen_raw_ne
#print axioms nativeK5Fifteen_relativeNecessity
#print axioms nativeK5Fifteen_noFiniteCoreFiller
#print axioms nativeK5Fifteen_noFiniteCoreRetraction
#print axioms NativeK5FifteenFourteenClasses
#print axioms nativeK5Fifteen_quotient_eq
#print axioms nativeK5FifteenCharge
#print axioms nativeK5Fifteen_chargeDescent
#print axioms nativeK5Fifteen_historyNoDescent
#print axioms nativeK5PentagonatorFifteen_relativeNecessity
#print axioms nativeK5PentagonatorFifteen_quotient_eq
#print axioms nativeK5PentagonatorFifteen_historyNoDescent

end
end Kuu.F112.Physical
