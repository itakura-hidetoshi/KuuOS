import Kuu.F112.PolygonNativeF55P94DK5PentagonatorTenCellNecessity
import Mathlib.Tactic

/-!
# F112-P94D3AH — genuine ten-cell inverse-square pasting

For every original source-typed TEN-cell Q between parallel NINE-cell
evidence q and t, the original 10D congruence constructors give
TWO distinct paths relating the SAME dependent 9D boundaries
    q · q⁻¹    and    t · t⁻¹.
They first change the left or right component, respectively, of the
original nine-cell composition. No raw equality is assumed.

The explicit free-group history on TEN-cell proof syntax assigns
letter A to the NEW P94D3AG 10D squareExchange and interprets
9D inverse-respect by conjugation with formal frame B. It is a
CHOSEN syntactic observer, not a model-independent holonomy.
An elementary S₃ quotient detects that A and B A B⁻¹ do not commute.

An abelian comparison count forgets this difference; all witnesses
and their dependent boundaries remain in the original Type-valued
higher-cell presentation.
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

abbrev NativeK5TenHistoryWord := FreeGroup (Fin 2)

def nativeK5TenExchangeLetter : NativeK5TenHistoryWord :=
  FreeGroup.of (0 : Fin 2)

def nativeK5TenInverseFrame : NativeK5TenHistoryWord :=
  FreeGroup.of (1 : Fin 2)

/-- Recursive history of ALL old original ten-cell constructors.
The original nine-cell inverse-respect congruence acts by the
chosen noncommutative inner automorphism A ↦ B A B⁻¹.
No extra 11-cell coherence is imposed here. -/
def NativeK5StructuralTenCell.historyWord
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
    (Q : NativeK5StructuralTenCell p q t) : NativeK5TenHistoryWord :=
  match Q with
  | .core _ => 1
  | .squareExchange _ => nativeK5TenExchangeLetter
  | .symm P => P.historyWord⁻¹
  | .trans P R => P.historyWord * R.historyWord
  | .nineVerticalLeft P _ => P.historyWord
  | .nineVerticalRight _ P => P.historyWord
  | .nineSymmRespect P =>
      nativeK5TenInverseFrame * P.historyWord * nativeK5TenInverseFrame⁻¹
  | .eightVerticalLeft P _ => P.historyWord
  | .eightVerticalRight _ P => P.historyWord
  | .eightInverseRespect P => P.historyWord

/-- Signed coarse integer count of the primitive 10D exchange.
It retains the number of generators but forgets their ordered
nonabelian history, including the inverse-frame conjugation. -/
def NativeK5StructuralTenCell.exchangeCount
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
    (Q : NativeK5StructuralTenCell p q t) : ℤ :=
  match Q with
  | .core _ => 0
  | .squareExchange _ => 1
  | .symm P => -P.exchangeCount
  | .trans P R => P.exchangeCount + R.exchangeCount
  | .nineVerticalLeft P _ => P.exchangeCount
  | .nineVerticalRight _ P => P.exchangeCount
  | .nineSymmRespect P => P.exchangeCount
  | .eightVerticalLeft P _ => P.exchangeCount
  | .eightVerticalRight _ P => P.exchangeCount
  | .eightInverseRespect P => P.exchangeCount

/-- First original Type-valued ten-cell pasting: update the
left NINE-cell component and then its formal nine-cell inverse. -/
def nativeK5TenPastingLeftThenRight
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
    (Q : NativeK5StructuralTenCell p q t) :
    NativeK5StructuralTenCell p
      (.trans q (.symm q)) (.trans t (.symm t)) :=
  .trans (.nineVerticalLeft Q (.symm q))
    (.nineVerticalRight t (.nineSymmRespect Q))

/-- Second original ten-cell pasting, right component first.
It has IDENTICAL dependent nine-cell endpoints, independently
of any equality or quotienting of the 10D proof terms. -/
def nativeK5TenPastingRightThenLeft
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
    (Q : NativeK5StructuralTenCell p q t) :
    NativeK5StructuralTenCell p
      (.trans q (.symm q)) (.trans t (.symm t)) :=
  .trans (.nineVerticalRight q (.nineSymmRespect Q))
    (.nineVerticalLeft Q (.symm t))

/-- Exact noncommutative histories of the genuine two pastings. -/
theorem nativeK5TenPasting_leftWord
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
    (Q : NativeK5StructuralTenCell p q t) :
    (nativeK5TenPastingLeftThenRight Q).historyWord =
      Q.historyWord *
        (nativeK5TenInverseFrame * Q.historyWord *
          nativeK5TenInverseFrame⁻¹) := rfl

theorem nativeK5TenPasting_rightWord
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
    (Q : NativeK5StructuralTenCell p q t) :
    (nativeK5TenPastingRightThenLeft Q).historyWord =
      (nativeK5TenInverseFrame * Q.historyWord *
          nativeK5TenInverseFrame⁻¹) * Q.historyWord := rfl

theorem nativeK5TenPasting_integerBlind
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
    (Q : NativeK5StructuralTenCell p q t) :
    (nativeK5TenPastingLeftThenRight Q).exchangeCount =
      (nativeK5TenPastingRightThenLeft Q).exchangeCount := rfl

/-- Nontrivial commutator in the FREE group, witnessed by the
nonabelian S₃ representation already certified at P94D3AG. -/
theorem nativeK5TenExchangeFrame_noncommute :
    nativeK5TenExchangeLetter *
        (nativeK5TenInverseFrame * nativeK5TenExchangeLetter *
          nativeK5TenInverseFrame⁻¹) ≠
      (nativeK5TenInverseFrame * nativeK5TenExchangeLetter *
          nativeK5TenInverseFrame⁻¹) * nativeK5TenExchangeLetter := by
  change nativeK5NineDiamondLetter *
      (nativeK5NineFrameLetter * nativeK5NineDiamondLetter *
        nativeK5NineFrameLetter⁻¹) ≠
    (nativeK5NineFrameLetter * nativeK5NineDiamondLetter *
        nativeK5NineFrameLetter⁻¹) * nativeK5NineDiamondLetter
  exact nativeK5NineLetters_conjugateNoncommute

/-- Substitute the ORIGINAL independent 10-cell squareExchange
into both dependent 10D pastings: their selected free-group
histories differ although their integer charges agree. -/
theorem nativeK5TenSquareExchange_pastingWord_ne
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
    (q : NativeK5StructuralNineCell p e d) :
    (nativeK5TenPastingLeftThenRight
      (NativeK5StructuralTenCell.squareExchange q)).historyWord ≠
    (nativeK5TenPastingRightThenLeft
      (NativeK5StructuralTenCell.squareExchange q)).historyWord := by
  change nativeK5TenExchangeLetter *
      (nativeK5TenInverseFrame * nativeK5TenExchangeLetter *
        nativeK5TenInverseFrame⁻¹) ≠
      (nativeK5TenInverseFrame * nativeK5TenExchangeLetter *
        nativeK5TenInverseFrame⁻¹) * nativeK5TenExchangeLetter
  exact nativeK5TenExchangeFrame_noncommute

/-- Same typed nine-cell endpoints do NOT imply equality of the
two freely generated raw TEN-cell witnesses. -/
theorem nativeK5TenSquareExchange_pastingRaw_ne
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
    (q : NativeK5StructuralNineCell p e d) :
    nativeK5TenPastingLeftThenRight
        (NativeK5StructuralTenCell.squareExchange q) ≠
      nativeK5TenPastingRightThenLeft
        (NativeK5StructuralTenCell.squareExchange q) := by
  intro heq
  exact nativeK5TenSquareExchange_pastingWord_ne q
    (congrArg NativeK5StructuralTenCell.historyWord heq)

#print axioms NativeK5StructuralTenCell.historyWord
#print axioms NativeK5StructuralTenCell.exchangeCount
#print axioms nativeK5TenPastingLeftThenRight
#print axioms nativeK5TenPastingRightThenLeft
#print axioms nativeK5TenPasting_leftWord
#print axioms nativeK5TenPasting_rightWord
#print axioms nativeK5TenPasting_integerBlind
#print axioms nativeK5TenExchangeFrame_noncommute
#print axioms nativeK5TenSquareExchange_pastingWord_ne
#print axioms nativeK5TenSquareExchange_pastingRaw_ne

end
end Kuu.F112.Physical
