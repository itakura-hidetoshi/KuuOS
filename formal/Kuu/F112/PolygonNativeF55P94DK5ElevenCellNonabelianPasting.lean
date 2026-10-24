import Kuu.F112.PolygonNativeF55P94DK5PentagonatorElevenCellNecessity
import Mathlib.Tactic

/-!
# F112-P94D3AI — original source-dependent 11D inverse-square pasting

At the EXACT original 10D boundaries of an independently adjoined
Type-valued 11D comparison H, construct TWO genuinely typed
11-cell paths: first update the original 10D term, then its inverse,
or perform the same changes in the opposite order.

An explicit FREE GROUP on two letters assigns generator A to the
original 11D squareExchange, and interprets original 10D symmetry
congruence as conjugation by the independently named frame B.
This is a CHOSEN syntax observer, not canonical intrinsic holonomy.

The original raw 11D paths have the same 10D boundaries and same
abelian signed square generator charge, yet distinct noncommutative
group words.  One S₃ evaluation certifies the free-word inequality.
No existing 12-cell relation is assumed here.
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

abbrev NativeK5ElevenHistoryWord := FreeGroup (Fin 2)

def nativeK5ElevenExchangeLetter : NativeK5ElevenHistoryWord :=
  FreeGroup.of (0 : Fin 2)

def nativeK5ElevenInverseFrame : NativeK5ElevenHistoryWord :=
  FreeGroup.of (1 : Fin 2)

/-- Order-sensitive universal-word observer on FULL original
11-cell proof syntax. Inverting the original 10D comparison
acts by inner conjugation by the selected frame. -/
def NativeK5StructuralElevenCell.historyWord
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
    NativeK5ElevenHistoryWord :=
  match H with
  | .core _ => 1
  | .squareExchange _ => nativeK5ElevenExchangeLetter
  | .symm S => S.historyWord⁻¹
  | .trans S T => S.historyWord * T.historyWord
  | .tenVerticalLeft S _ => S.historyWord
  | .tenVerticalRight _ S => S.historyWord
  | .tenSymmRespect S =>
      nativeK5ElevenInverseFrame * S.historyWord *
        nativeK5ElevenInverseFrame⁻¹
  | .nineVerticalLeft S _ => S.historyWord
  | .nineVerticalRight _ S => S.historyWord
  | .nineSymmRespect S => S.historyWord
  | .eightVerticalLeft S _ => S.historyWord
  | .eightVerticalRight _ S => S.historyWord
  | .eightInverseRespect S => S.historyWord

/-- Coarse signed eleven-cell square-exchange counter.  It
forgets which order produced the pasting. -/
def NativeK5StructuralElevenCell.squareCount
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
    (H : NativeK5StructuralElevenCell p P Q) : ℤ :=
  match H with
  | .core _ => 0
  | .squareExchange _ => 1
  | .symm S => -S.squareCount
  | .trans S T => S.squareCount + T.squareCount
  | .tenVerticalLeft S _ => S.squareCount
  | .tenVerticalRight _ S => S.squareCount
  | .tenSymmRespect S => S.squareCount
  | .nineVerticalLeft S _ => S.squareCount
  | .nineVerticalRight _ S => S.squareCount
  | .nineSymmRespect S => S.squareCount
  | .eightVerticalLeft S _ => S.squareCount
  | .eightVerticalRight _ S => S.squareCount
  | .eightInverseRespect S => S.squareCount

/-- The first Type-valued 11D pasting order from a genuine 11D
comparison between two ORIGINAL 10D witness terms. -/
def nativeK5ElevenPastingLeftThenRight
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
    NativeK5StructuralElevenCell p
      (.trans P (.symm P)) (.trans Q (.symm Q)) :=
  .trans (.tenVerticalLeft H (.symm P))
    (.tenVerticalRight Q (.tenSymmRespect H))

/-- The second genuine source-dependent 11D pasting, with the
EXACT same original 10D source and target as the first. -/
def nativeK5ElevenPastingRightThenLeft
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
    NativeK5StructuralElevenCell p
      (.trans P (.symm P)) (.trans Q (.symm Q)) :=
  .trans (.tenVerticalRight P (.tenSymmRespect H))
    (.tenVerticalLeft H (.symm Q))

theorem nativeK5ElevenPasting_leftWord
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
    (nativeK5ElevenPastingLeftThenRight H).historyWord =
      H.historyWord *
        (nativeK5ElevenInverseFrame * H.historyWord *
          nativeK5ElevenInverseFrame⁻¹) := rfl

theorem nativeK5ElevenPasting_rightWord
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
    (nativeK5ElevenPastingRightThenLeft H).historyWord =
      (nativeK5ElevenInverseFrame * H.historyWord *
          nativeK5ElevenInverseFrame⁻¹) * H.historyWord := rfl

theorem nativeK5ElevenPasting_integerBlind
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
    (nativeK5ElevenPastingLeftThenRight H).squareCount =
      (nativeK5ElevenPastingRightThenLeft H).squareCount := rfl

/-- Noncommutation in the universal two-generator FREE GROUP,
certified via the previous explicit S₃ evaluation. -/
theorem nativeK5ElevenExchangeFrame_noncommute :
    nativeK5ElevenExchangeLetter *
        (nativeK5ElevenInverseFrame * nativeK5ElevenExchangeLetter *
          nativeK5ElevenInverseFrame⁻¹) ≠
      (nativeK5ElevenInverseFrame * nativeK5ElevenExchangeLetter *
          nativeK5ElevenInverseFrame⁻¹) * nativeK5ElevenExchangeLetter := by
  change nativeK5TenExchangeLetter *
      (nativeK5TenInverseFrame * nativeK5TenExchangeLetter *
        nativeK5TenInverseFrame⁻¹) ≠
    (nativeK5TenInverseFrame * nativeK5TenExchangeLetter *
      nativeK5TenInverseFrame⁻¹) * nativeK5TenExchangeLetter
  exact nativeK5TenExchangeFrame_noncommute

/-- The original 11D exchange yields two genuinely different
eleven-cell histories despite equal signed square count. -/
theorem nativeK5ElevenSquareExchange_pastingWord_ne
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
    (P : NativeK5StructuralTenCell p q t) :
    (nativeK5ElevenPastingLeftThenRight
      (NativeK5StructuralElevenCell.squareExchange P)).historyWord ≠
    (nativeK5ElevenPastingRightThenLeft
      (NativeK5StructuralElevenCell.squareExchange P)).historyWord := by
  change nativeK5ElevenExchangeLetter *
      (nativeK5ElevenInverseFrame * nativeK5ElevenExchangeLetter *
        nativeK5ElevenInverseFrame⁻¹) ≠
    (nativeK5ElevenInverseFrame * nativeK5ElevenExchangeLetter *
      nativeK5ElevenInverseFrame⁻¹) * nativeK5ElevenExchangeLetter
  exact nativeK5ElevenExchangeFrame_noncommute

/-- Distinct noncommutative word shadows prove distinct RAW
Type-valued original eleven-cell proof terms. -/
theorem nativeK5ElevenSquareExchange_pastingRaw_ne
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
    (P : NativeK5StructuralTenCell p q t) :
    nativeK5ElevenPastingLeftThenRight
      (NativeK5StructuralElevenCell.squareExchange P) ≠
    nativeK5ElevenPastingRightThenLeft
      (NativeK5StructuralElevenCell.squareExchange P) := by
  intro heq
  exact nativeK5ElevenSquareExchange_pastingWord_ne P
    (congrArg NativeK5StructuralElevenCell.historyWord heq)

#print axioms NativeK5StructuralElevenCell.historyWord
#print axioms NativeK5StructuralElevenCell.squareCount
#print axioms nativeK5ElevenPastingLeftThenRight
#print axioms nativeK5ElevenPastingRightThenLeft
#print axioms nativeK5ElevenPasting_leftWord
#print axioms nativeK5ElevenPasting_rightWord
#print axioms nativeK5ElevenPasting_integerBlind
#print axioms nativeK5ElevenExchangeFrame_noncommute
#print axioms nativeK5ElevenSquareExchange_pastingWord_ne
#print axioms nativeK5ElevenSquareExchange_pastingRaw_ne

end
end Kuu.F112.Physical
