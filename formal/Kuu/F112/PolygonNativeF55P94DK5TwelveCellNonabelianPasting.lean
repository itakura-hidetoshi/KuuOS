import Kuu.F112.PolygonNativeF55P94DK5PentagonatorTwelveCellNecessity
import Mathlib.Tactic

/-!
# F112-P94D3AJ — genuine source-dependent 12D inverse-square pasting

At the exact original 11D boundaries of a Type-valued structural 12-cell W,
construct two different source-typed 12-cell double-whiskering paths with
identical original 11D endpoints. An explicitly CHOSEN free-group history
distinguishes their raw proof terms even though the signed generator counter
agrees. This is a relative noncommutative obstruction, not an absolute
higher-coherence or 13-cell existence theorem.
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

abbrev NativeK5TwelveHistoryWord := FreeGroup (Fin 2)

def nativeK5TwelveExchangeLetter : NativeK5TwelveHistoryWord :=
  FreeGroup.of (0 : Fin 2)

def nativeK5TwelveInverseFrame : NativeK5TwelveHistoryWord :=
  FreeGroup.of (1 : Fin 2)

/-- The *chosen*, order-sensitive free history of ORIGINAL 12-cell syntax.
The original 11D inversion-congruence acts by B-conjugation. -/
def NativeK5StructuralTwelveCell.historyWord
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
    (W : NativeK5StructuralTwelveCell p H K) :
    NativeK5TwelveHistoryWord :=
  match W with
  | .core _ => 1
  | .squareExchange _ => nativeK5TwelveExchangeLetter
  | .symm S => S.historyWord⁻¹
  | .trans S T => S.historyWord * T.historyWord
  | .elevenVerticalLeft S _ => S.historyWord
  | .elevenVerticalRight _ S => S.historyWord
  | .elevenSymmRespect S =>
      nativeK5TwelveInverseFrame * S.historyWord *
        nativeK5TwelveInverseFrame⁻¹
  | .tenVerticalLeft S _ => S.historyWord
  | .tenVerticalRight _ S => S.historyWord
  | .tenSymmRespect S => S.historyWord
  | .nineVerticalLeft S _ => S.historyWord
  | .nineVerticalRight _ S => S.historyWord
  | .nineSymmRespect S => S.historyWord
  | .eightVerticalLeft S _ => S.historyWord
  | .eightVerticalRight _ S => S.historyWord
  | .eightInverseRespect S => S.historyWord

/-- Signed 12D square-exchange count. The chosen frame is invisible here. -/
def NativeK5StructuralTwelveCell.squareCount
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
    (W : NativeK5StructuralTwelveCell p H K) : ℤ :=
  match W with
  | .core _ => 0
  | .squareExchange _ => 1
  | .symm S => -S.squareCount
  | .trans S T => S.squareCount + T.squareCount
  | .elevenVerticalLeft S _ => S.squareCount
  | .elevenVerticalRight _ S => S.squareCount
  | .elevenSymmRespect S => S.squareCount
  | .tenVerticalLeft S _ => S.squareCount
  | .tenVerticalRight _ S => S.squareCount
  | .tenSymmRespect S => S.squareCount
  | .nineVerticalLeft S _ => S.squareCount
  | .nineVerticalRight _ S => S.squareCount
  | .nineSymmRespect S => S.squareCount
  | .eightVerticalLeft S _ => S.squareCount
  | .eightVerticalRight _ S => S.squareCount
  | .eightInverseRespect S => S.squareCount

/-- First actual 12-cell order: update an original 11D proof, then
its ORIGINAL 11D inverse. Both endpoints retain their dependent types. -/
def nativeK5TwelvePastingLeftThenRight
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
    (W : NativeK5StructuralTwelveCell p H K) :
    NativeK5StructuralTwelveCell p
      (.trans H (.symm H)) (.trans K (.symm K)) :=
  .trans (.elevenVerticalLeft W (.symm H))
    (.elevenVerticalRight K (.elevenSymmRespect W))

/-- The opposite genuine 12D pasting, with exactly the same source
and target ORIGINAL 11D witnesses as the first pasting. -/
def nativeK5TwelvePastingRightThenLeft
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
    (W : NativeK5StructuralTwelveCell p H K) :
    NativeK5StructuralTwelveCell p
      (.trans H (.symm H)) (.trans K (.symm K)) :=
  .trans (.elevenVerticalRight H (.elevenSymmRespect W))
    (.elevenVerticalLeft W (.symm K))

theorem nativeK5TwelvePasting_leftWord
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
    (W : NativeK5StructuralTwelveCell p H K) :
    (nativeK5TwelvePastingLeftThenRight W).historyWord =
      W.historyWord *
        (nativeK5TwelveInverseFrame * W.historyWord *
          nativeK5TwelveInverseFrame⁻¹) := rfl

theorem nativeK5TwelvePasting_rightWord
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
    (W : NativeK5StructuralTwelveCell p H K) :
    (nativeK5TwelvePastingRightThenLeft W).historyWord =
      (nativeK5TwelveInverseFrame * W.historyWord *
        nativeK5TwelveInverseFrame⁻¹) * W.historyWord := rfl

theorem nativeK5TwelvePasting_integerBlind
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
    (W : NativeK5StructuralTwelveCell p H K) :
    (nativeK5TwelvePastingLeftThenRight W).squareCount =
      (nativeK5TwelvePastingRightThenLeft W).squareCount := rfl

/-- The same S₃-certified free-group obstruction is reused at the
12D stage; no new logical axiom is introduced. -/
theorem nativeK5TwelveExchangeFrame_noncommute :
    nativeK5TwelveExchangeLetter *
        (nativeK5TwelveInverseFrame * nativeK5TwelveExchangeLetter *
          nativeK5TwelveInverseFrame⁻¹) ≠
      (nativeK5TwelveInverseFrame * nativeK5TwelveExchangeLetter *
          nativeK5TwelveInverseFrame⁻¹) * nativeK5TwelveExchangeLetter := by
  change nativeK5ElevenExchangeLetter *
      (nativeK5ElevenInverseFrame * nativeK5ElevenExchangeLetter *
        nativeK5ElevenInverseFrame⁻¹) ≠
    (nativeK5ElevenInverseFrame * nativeK5ElevenExchangeLetter *
      nativeK5ElevenInverseFrame⁻¹) * nativeK5ElevenExchangeLetter
  exact nativeK5ElevenExchangeFrame_noncommute

/-- A genuine 12D square generator produces distinct ordered histories. -/
theorem nativeK5TwelveSquareExchange_pastingWord_ne
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
    (H : NativeK5StructuralElevenCell p P Q) :
    (nativeK5TwelvePastingLeftThenRight
      (NativeK5StructuralTwelveCell.squareExchange H)).historyWord ≠
    (nativeK5TwelvePastingRightThenLeft
      (NativeK5StructuralTwelveCell.squareExchange H)).historyWord := by
  change nativeK5TwelveExchangeLetter *
      (nativeK5TwelveInverseFrame * nativeK5TwelveExchangeLetter *
        nativeK5TwelveInverseFrame⁻¹) ≠
    (nativeK5TwelveInverseFrame * nativeK5TwelveExchangeLetter *
      nativeK5TwelveInverseFrame⁻¹) * nativeK5TwelveExchangeLetter
  exact nativeK5TwelveExchangeFrame_noncommute

/-- Different free histories distinguish RAW dependent 12-cell terms. -/
theorem nativeK5TwelveSquareExchange_pastingRaw_ne
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
    (H : NativeK5StructuralElevenCell p P Q) :
    nativeK5TwelvePastingLeftThenRight
      (NativeK5StructuralTwelveCell.squareExchange H) ≠
    nativeK5TwelvePastingRightThenLeft
      (NativeK5StructuralTwelveCell.squareExchange H) := by
  intro h
  exact nativeK5TwelveSquareExchange_pastingWord_ne H
    (congrArg NativeK5StructuralTwelveCell.historyWord h)

/-- The actual C60 five-stage K₅ 11D comparison produces a 12D
critical pair. The two paths have the same original dependent 11D
endpoints, but are not equal as raw 12D proof terms. -/
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

def nativeK5PentagonatorThirteenExchangeTwelve :=
  NativeK5StructuralTwelveCell.squareExchange
    (nativeK5PentagonatorTwelveExchangeEleven t1 t2 t3 t4 t5)

def nativeK5PentagonatorThirteenLeftFirst :=
  nativeK5TwelvePastingLeftThenRight
    (nativeK5PentagonatorThirteenExchangeTwelve t1 t2 t3 t4 t5)

def nativeK5PentagonatorThirteenRightFirst :=
  nativeK5TwelvePastingRightThenLeft
    (nativeK5PentagonatorThirteenExchangeTwelve t1 t2 t3 t4 t5)

theorem nativeK5PentagonatorThirteen_integerBlind :
    (nativeK5PentagonatorThirteenLeftFirst t1 t2 t3 t4 t5).squareCount =
      (nativeK5PentagonatorThirteenRightFirst t1 t2 t3 t4 t5).squareCount :=
  nativeK5TwelvePasting_integerBlind
    (nativeK5PentagonatorThirteenExchangeTwelve t1 t2 t3 t4 t5)

theorem nativeK5PentagonatorThirteen_history_ne :
    (nativeK5PentagonatorThirteenLeftFirst t1 t2 t3 t4 t5).historyWord ≠
      (nativeK5PentagonatorThirteenRightFirst t1 t2 t3 t4 t5).historyWord :=
  nativeK5TwelveSquareExchange_pastingWord_ne
    (nativeK5PentagonatorTwelveExchangeEleven t1 t2 t3 t4 t5)

theorem nativeK5PentagonatorThirteen_raw_ne :
    nativeK5PentagonatorThirteenLeftFirst t1 t2 t3 t4 t5 ≠
      nativeK5PentagonatorThirteenRightFirst t1 t2 t3 t4 t5 :=
  nativeK5TwelveSquareExchange_pastingRaw_ne
    (nativeK5PentagonatorTwelveExchangeEleven t1 t2 t3 t4 t5)

end GenuineFiveStage

#print axioms NativeK5StructuralTwelveCell.historyWord
#print axioms NativeK5StructuralTwelveCell.squareCount
#print axioms nativeK5TwelvePastingLeftThenRight
#print axioms nativeK5TwelvePastingRightThenLeft
#print axioms nativeK5TwelvePasting_integerBlind
#print axioms nativeK5TwelveExchangeFrame_noncommute
#print axioms nativeK5TwelveSquareExchange_pastingWord_ne
#print axioms nativeK5TwelveSquareExchange_pastingRaw_ne
#print axioms nativeK5PentagonatorThirteen_history_ne
#print axioms nativeK5PentagonatorThirteen_raw_ne

end
end Kuu.F112.Physical
