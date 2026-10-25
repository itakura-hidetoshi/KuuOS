import Kuu.F112.PolygonNativeF55P94DK5PentagonatorFourteenCellNecessity
import Kuu.F112.PolygonNativeF55P94DConservativeTowerDescent
import Mathlib.Tactic

/-!
# F112-P94D3AN — genuine source-dependent fourteen-cell nonabelian pasting

On the ORIGINAL dependent thirteen-cell boundary of a genuine Type-valued
fourteen-cell witness, compose it with its genuine thirteen-cell inverse
frame in two orders. Both composites have exactly the same original
thirteen-cell source and target. A chosen two-generator free-group history
distinguishes the raw fourteen-cell proofs, whereas signed square count
cannot distinguish them.

The argument is independent of a 15D quotient and does not add a 15D
generator. The generic conservative-tower theorem is reused at the exact
14D exchange fiber. All nonexistence results remain relative to the
explicitly named conservative grammar and its selected observer.
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

abbrev NativeK5FourteenHistoryWord := FreeGroup (Fin 2)

def nativeK5FourteenExchangeLetter : NativeK5FourteenHistoryWord :=
  FreeGroup.of (0 : Fin 2)

def nativeK5FourteenInverseFrame : NativeK5FourteenHistoryWord :=
  FreeGroup.of (1 : Fin 2)

/-- A chosen free-group observer of the ACTUAL fourteen-cell syntax.
Thirteen-cell inversion whiskering acts by B-conjugation. This observer
is not claimed to factor through a future fifteen-cell quotient. -/
def NativeK5StructuralFourteenCell.historyWord
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    {h k : NativeK5StructuralSevenCell p u v}
    {e d : NativeK5StructuralEightCell p h k}
    {q t : NativeK5StructuralNineCell p e d}
    {P Q : NativeK5StructuralTenCell p q t}
    {H K : NativeK5StructuralElevenCell p P Q}
    {U V : NativeK5StructuralTwelveCell p H K}
    {T S : NativeK5StructuralThirteenCell p U V}
    (R : NativeK5StructuralFourteenCell p T S) :
    NativeK5FourteenHistoryWord :=
  match R with
  | .core _ => 1
  | .squareExchange _ => nativeK5FourteenExchangeLetter
  | .symm X => X.historyWord⁻¹
  | .trans X Y => X.historyWord * Y.historyWord
  | .thirteenVerticalLeft X _ => X.historyWord
  | .thirteenVerticalRight _ X => X.historyWord
  | .thirteenSymmRespect X =>
      nativeK5FourteenInverseFrame * X.historyWord *
        nativeK5FourteenInverseFrame⁻¹
  | .twelveVerticalLeft X _ => X.historyWord
  | .twelveVerticalRight _ X => X.historyWord
  | .twelveSymmRespect X => X.historyWord
  | .elevenVerticalLeft X _ => X.historyWord
  | .elevenVerticalRight _ X => X.historyWord
  | .elevenSymmRespect X => X.historyWord
  | .tenVerticalLeft X _ => X.historyWord
  | .tenVerticalRight _ X => X.historyWord
  | .tenSymmRespect X => X.historyWord
  | .nineVerticalLeft X _ => X.historyWord
  | .nineVerticalRight _ X => X.historyWord
  | .nineSymmRespect X => X.historyWord
  | .eightVerticalLeft X _ => X.historyWord
  | .eightVerticalRight _ X => X.historyWord
  | .eightInverseRespect X => X.historyWord
  termination_by structural R

/-- Scalar fourteen-cell exchange count, forgetting noncommutative
word order; not a substitute for raw proof equality. -/
def NativeK5StructuralFourteenCell.squareCount
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    {h k : NativeK5StructuralSevenCell p u v}
    {e d : NativeK5StructuralEightCell p h k}
    {q t : NativeK5StructuralNineCell p e d}
    {P Q : NativeK5StructuralTenCell p q t}
    {H K : NativeK5StructuralElevenCell p P Q}
    {U V : NativeK5StructuralTwelveCell p H K}
    {T S : NativeK5StructuralThirteenCell p U V}
    (R : NativeK5StructuralFourteenCell p T S) : ℤ :=
  match R with
  | .core _ => 0
  | .squareExchange _ => 1
  | .symm X => -X.squareCount
  | .trans X Y => X.squareCount + Y.squareCount
  | .thirteenVerticalLeft X _ => X.squareCount
  | .thirteenVerticalRight _ X => X.squareCount
  | .thirteenSymmRespect X => X.squareCount
  | .twelveVerticalLeft X _ => X.squareCount
  | .twelveVerticalRight _ X => X.squareCount
  | .twelveSymmRespect X => X.squareCount
  | .elevenVerticalLeft X _ => X.squareCount
  | .elevenVerticalRight _ X => X.squareCount
  | .elevenSymmRespect X => X.squareCount
  | .tenVerticalLeft X _ => X.squareCount
  | .tenVerticalRight _ X => X.squareCount
  | .tenSymmRespect X => X.squareCount
  | .nineVerticalLeft X _ => X.squareCount
  | .nineVerticalRight _ X => X.squareCount
  | .nineSymmRespect X => X.squareCount
  | .eightVerticalLeft X _ => X.squareCount
  | .eightVerticalRight _ X => X.squareCount
  | .eightInverseRespect X => X.squareCount
  termination_by structural R

section GenuineFourteenPasting

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
variable {A B : NativeK5StructuralThirteenCell p U V}

/-- Original fourteen-cell left-first pasting, from A;A⁻¹ to B;B⁻¹
as genuinely dependent THIRTEEN-cell endpoints. -/
def nativeK5FourteenPastingLeftThenRight
    (R : NativeK5StructuralFourteenCell p A B) :
    NativeK5StructuralFourteenCell p
      (.trans A (.symm A)) (.trans B (.symm B)) :=
  .trans (.thirteenVerticalLeft R (.symm A))
    (.thirteenVerticalRight B (.thirteenSymmRespect R))

/-- Opposite fourteen-cell right-first pasting with the identical
ORIGINAL thirteen-cell source and target as left-first. -/
def nativeK5FourteenPastingRightThenLeft
    (R : NativeK5StructuralFourteenCell p A B) :
    NativeK5StructuralFourteenCell p
      (.trans A (.symm A)) (.trans B (.symm B)) :=
  .trans (.thirteenVerticalRight A (.thirteenSymmRespect R))
    (.thirteenVerticalLeft R (.symm B))

theorem nativeK5FourteenPasting_leftWord
    (R : NativeK5StructuralFourteenCell p A B) :
    (nativeK5FourteenPastingLeftThenRight R).historyWord =
      R.historyWord *
        (nativeK5FourteenInverseFrame * R.historyWord *
          nativeK5FourteenInverseFrame⁻¹) := rfl

theorem nativeK5FourteenPasting_rightWord
    (R : NativeK5StructuralFourteenCell p A B) :
    (nativeK5FourteenPastingRightThenLeft R).historyWord =
      (nativeK5FourteenInverseFrame * R.historyWord *
        nativeK5FourteenInverseFrame⁻¹) * R.historyWord := rfl

theorem nativeK5FourteenPasting_integerBlind
    (R : NativeK5StructuralFourteenCell p A B) :
    (nativeK5FourteenPastingLeftThenRight R).squareCount =
      (nativeK5FourteenPastingRightThenLeft R).squareCount := rfl

/-- The exact free-group noncommutativity established in the prior
dimension survives the original typed fourteen-cell lift. -/
theorem nativeK5FourteenExchangeFrame_noncommute :
    nativeK5FourteenExchangeLetter *
        (nativeK5FourteenInverseFrame * nativeK5FourteenExchangeLetter *
          nativeK5FourteenInverseFrame⁻¹) ≠
      (nativeK5FourteenInverseFrame * nativeK5FourteenExchangeLetter *
        nativeK5FourteenInverseFrame⁻¹) * nativeK5FourteenExchangeLetter := by
  change nativeK5ThirteenExchangeLetter *
      (nativeK5ThirteenInverseFrame * nativeK5ThirteenExchangeLetter *
        nativeK5ThirteenInverseFrame⁻¹) ≠
    (nativeK5ThirteenInverseFrame * nativeK5ThirteenExchangeLetter *
      nativeK5ThirteenInverseFrame⁻¹) * nativeK5ThirteenExchangeLetter
  exact nativeK5ThirteenExchangeFrame_noncommute

/-- The independent source-typed fourteen-cell squareExchange yields
two true fourteen-cell proofs with different free histories. -/
theorem nativeK5FourteenSquareExchange_pastingWord_ne
    (W : NativeK5StructuralThirteenCell p U V) :
    (nativeK5FourteenPastingLeftThenRight
      (NativeK5StructuralFourteenCell.squareExchange W)).historyWord ≠
    (nativeK5FourteenPastingRightThenLeft
      (NativeK5StructuralFourteenCell.squareExchange W)).historyWord := by
  change nativeK5FourteenExchangeLetter *
      (nativeK5FourteenInverseFrame * nativeK5FourteenExchangeLetter *
        nativeK5FourteenInverseFrame⁻¹) ≠
    (nativeK5FourteenInverseFrame * nativeK5FourteenExchangeLetter *
      nativeK5FourteenInverseFrame⁻¹) * nativeK5FourteenExchangeLetter
  exact nativeK5FourteenExchangeFrame_noncommute

/-- Raw fourteen-cell proof inequality, NOT a fifteen-cell quotient
comparison and NOT a statement about arbitrary higher cells. -/
theorem nativeK5FourteenSquareExchange_pastingRaw_ne
    (W : NativeK5StructuralThirteenCell p U V) :
    nativeK5FourteenPastingLeftThenRight
      (NativeK5StructuralFourteenCell.squareExchange W) ≠
    nativeK5FourteenPastingRightThenLeft
      (NativeK5StructuralFourteenCell.squareExchange W) := by
  intro heq
  exact nativeK5FourteenSquareExchange_pastingWord_ne W
    (congrArg NativeK5StructuralFourteenCell.historyWord heq)

/-- For ANY original thirteen-cell critical pair with distinct
history, no FINITE conservative closure of the ACTUAL fourteen-cell
core grammar can fill that pair. -/
theorem nativeK5Fourteen_noFiniteCoreFiller
    (W : NativeK5StructuralThirteenCell p U V)
    (hneq : (nativeK5ThirteenPastingLeftThenRight W).historyWord ≠
      (nativeK5ThirteenPastingRightThenLeft W).historyWord)
    (n : Nat) :
    ¬ Nonempty
      (NativeConservativeTower
        (fun X Y : NativeK5StructuralThirteenCell p
          (.trans U (.symm U)) (.trans V (.symm V)) =>
            NativeK5CoreFourteenCell p X Y)
        n
        (nativeK5ThirteenPastingLeftThenRight W)
        (nativeK5ThirteenPastingRightThenLeft W)) := by
  exact NativeConservativeTower.no_finite_filler
    (fun X : NativeK5StructuralThirteenCell p
      (.trans U (.symm U)) (.trans V (.symm V)) => X.historyWord)
    (fun {X Y} (proof : NativeK5CoreFourteenCell p X Y) =>
      proof.historyWord_sound)
    hneq n

/-- Independently adjoined fourteen-cell comparison cannot retract
into ANY finite conservative fourteen-cell closure at this pair. -/
theorem nativeK5Fourteen_noFiniteCoreRetraction
    (W : NativeK5StructuralThirteenCell p U V)
    (hneq : (nativeK5ThirteenPastingLeftThenRight W).historyWord ≠
      (nativeK5ThirteenPastingRightThenLeft W).historyWord)
    (n : Nat) :
    ¬ Nonempty
      (NativeK5StructuralFourteenCell p
        (nativeK5ThirteenPastingLeftThenRight W)
        (nativeK5ThirteenPastingRightThenLeft W) →
       NativeConservativeTower
        (fun X Y : NativeK5StructuralThirteenCell p
          (.trans U (.symm U)) (.trans V (.symm V)) =>
            NativeK5CoreFourteenCell p X Y)
        n
        (nativeK5ThirteenPastingLeftThenRight W)
        (nativeK5ThirteenPastingRightThenLeft W)) := by
  exact NativeConservativeTower.no_finite_retraction
    (fun X : NativeK5StructuralThirteenCell p
      (.trans U (.symm U)) (.trans V (.symm V)) => X.historyWord)
    (fun {X Y} (proof : NativeK5CoreFourteenCell p X Y) =>
      proof.historyWord_sound)
    (NativeK5StructuralFourteenCell.squareExchange W) hneq n

end GenuineFourteenPasting

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

/-- ORIGINAL source-dependent five-stage C60 K5 fourteen-cell. -/
def nativeK5PentagonatorFifteenExchangeFourteen :=
  nativeK5PentagonatorFourteenExchange t1 t2 t3 t4 t5

def nativeK5PentagonatorFifteenLeftFirst :=
  nativeK5FourteenPastingLeftThenRight
    (nativeK5PentagonatorFifteenExchangeFourteen t1 t2 t3 t4 t5)

def nativeK5PentagonatorFifteenRightFirst :=
  nativeK5FourteenPastingRightThenLeft
    (nativeK5PentagonatorFifteenExchangeFourteen t1 t2 t3 t4 t5)

theorem nativeK5PentagonatorFifteen_integerBlind :
    (nativeK5PentagonatorFifteenLeftFirst t1 t2 t3 t4 t5).squareCount =
      (nativeK5PentagonatorFifteenRightFirst t1 t2 t3 t4 t5).squareCount :=
  nativeK5FourteenPasting_integerBlind
    (nativeK5PentagonatorFifteenExchangeFourteen t1 t2 t3 t4 t5)

theorem nativeK5PentagonatorFifteen_history_ne :
    (nativeK5PentagonatorFifteenLeftFirst t1 t2 t3 t4 t5).historyWord ≠
      (nativeK5PentagonatorFifteenRightFirst t1 t2 t3 t4 t5).historyWord :=
  nativeK5FourteenSquareExchange_pastingWord_ne
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)

theorem nativeK5PentagonatorFifteen_raw_ne :
    nativeK5PentagonatorFifteenLeftFirst t1 t2 t3 t4 t5 ≠
      nativeK5PentagonatorFifteenRightFirst t1 t2 t3 t4 t5 :=
  nativeK5FourteenSquareExchange_pastingRaw_ne
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)

end GenuineFiveStage

#print axioms NativeK5StructuralFourteenCell.historyWord
#print axioms NativeK5StructuralFourteenCell.squareCount
#print axioms nativeK5FourteenPastingLeftThenRight
#print axioms nativeK5FourteenPastingRightThenLeft
#print axioms nativeK5FourteenPasting_integerBlind
#print axioms nativeK5FourteenExchangeFrame_noncommute
#print axioms nativeK5FourteenSquareExchange_pastingWord_ne
#print axioms nativeK5FourteenSquareExchange_pastingRaw_ne
#print axioms nativeK5Fourteen_noFiniteCoreFiller
#print axioms nativeK5Fourteen_noFiniteCoreRetraction
#print axioms nativeK5PentagonatorFifteen_history_ne
#print axioms nativeK5PentagonatorFifteen_raw_ne

end
end Kuu.F112.Physical
