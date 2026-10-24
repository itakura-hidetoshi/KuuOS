import Kuu.F112.PolygonNativeF55P94DK5TypedNineCellUnitObstruction
import Mathlib.Tactic

/-!
# F112-P94D3AG — genuine nine-cell inverse-square critical pair

A genuine NINE-cell q : e ⇒ d between original dependent EIGHT-cell
evidence induces two distinct NINE-cell pastings between the same
EIGHT-cell boundaries (e · e⁻¹) and (d · d⁻¹).  Each path first
updates one EIGHT-cell component and then the other, using the
original source-typed 9D verticalLeft/verticalRight and
inverseRespect constructors.

An order-sensitive FREE GROUP on two letters observes:
 * the genuine independent 9D unitDiamond constructor (letter A);
 * inversion of the original 8D comparison, transported by
   conjugation with the independent formal frame B.
Core 9D constructors have neutral history.  This is explicitly a
chosen *syntactic representation*, not a unique intrinsic holonomy.

For an actual unitDiamond generator the two 9D paths have identical
signed integer charge but incompatible noncommutative free words.
A finite S₃ evaluation witnesses that LR != RL in the free group.
This is the source-dependent boundary for a potential independent
TENTH-cell square exchange.
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

/-- Keep the free-group carrier from the preceding eight-cell
word observer, but assign its generators NEW nine-cell meanings. -/
abbrev NativeK5NineHistoryWord := FreeGroup (Fin 2)

def nativeK5NineDiamondLetter : NativeK5NineHistoryWord :=
  FreeGroup.of (0 : Fin 2)

def nativeK5NineFrameLetter : NativeK5NineHistoryWord :=
  FreeGroup.of (1 : Fin 2)

/-- Syntactic, dependency-preserving 9D universal-word observer.
Inverse-respect along original 8D evidence is deliberately
interpreted by the inner automorphism conj_B. -/
def NativeK5StructuralNineCell.historyWord
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
    (q : NativeK5StructuralNineCell p e d) : NativeK5NineHistoryWord :=
  match q with
  | .core _ => 1
  | .unitDiamond _ => nativeK5NineDiamondLetter
  | .symm q => q.historyWord⁻¹
  | .trans q z => q.historyWord * z.historyWord
  | .verticalLeft q _ => q.historyWord
  | .verticalRight _ q => q.historyWord
  | .inverseRespect q =>
      nativeK5NineFrameLetter * q.historyWord * nativeK5NineFrameLetter⁻¹

/-- Abelian count of nine-cell comparison generators; this forgets
both the ordered history and the chosen inversion frame. -/
def NativeK5StructuralNineCell.diamondCount
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
    (q : NativeK5StructuralNineCell p e d) : ℤ :=
  match q with
  | .core _ => 0
  | .unitDiamond _ => 1
  | .symm q => -q.diamondCount
  | .trans q z => q.diamondCount + z.diamondCount
  | .verticalLeft q _ => q.diamondCount
  | .verticalRight _ q => q.diamondCount
  | .inverseRespect q => q.diamondCount

/-- The first actual nine-cell double-whiskering path:
update the original 8D witness, then its 8D inverse. -/
def nativeK5NinePastingLeftThenRight
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
    NativeK5StructuralNineCell p
      (.trans e (.symm e)) (.trans d (.symm d)) :=
  .trans (.verticalLeft q (.symm e))
    (.verticalRight d (.inverseRespect q))

/-- The opposing nine-cell pasting path has the same original
EIGHT-cell endpoints, but performs the inversion component first. -/
def nativeK5NinePastingRightThenLeft
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
    NativeK5StructuralNineCell p
      (.trans e (.symm e)) (.trans d (.symm d)) :=
  .trans (.verticalRight e (.inverseRespect q))
    (.verticalLeft q (.symm d))

theorem nativeK5NinePasting_leftWord
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
    (nativeK5NinePastingLeftThenRight q).historyWord =
      q.historyWord * (nativeK5NineFrameLetter * q.historyWord *
        nativeK5NineFrameLetter⁻¹) := rfl

theorem nativeK5NinePasting_rightWord
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
    (nativeK5NinePastingRightThenLeft q).historyWord =
      (nativeK5NineFrameLetter * q.historyWord *
        nativeK5NineFrameLetter⁻¹) * q.historyWord := rfl

/-- In both orders, the integer shadow counts exactly two
occurrences of the same genuine 9D generator. -/
theorem nativeK5NinePasting_integerBlind
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
    (nativeK5NinePastingLeftThenRight q).diamondCount =
      (nativeK5NinePastingRightThenLeft q).diamondCount := rfl

/-- Use the existing mathlib FreeGroup S₃ evaluation to certify
that the conjugate of A by B does not commute with A. -/
theorem nativeK5NineLetters_conjugateNoncommute :
    nativeK5NineDiamondLetter *
        (nativeK5NineFrameLetter * nativeK5NineDiamondLetter *
          nativeK5NineFrameLetter⁻¹) ≠
      (nativeK5NineFrameLetter * nativeK5NineDiamondLetter *
          nativeK5NineFrameLetter⁻¹) * nativeK5NineDiamondLetter := by
  intro heq
  have hs := congrArg nativeK5EightUnitWordToS3 heq
  simp only [map_mul, map_inv,
    nativeK5EightUnitWordToS3_left,
    nativeK5EightUnitWordToS3_right] at hs
  have hneq :
      nativeK5SquareLeftGenerator *
          (nativeK5SquareRightGenerator * nativeK5SquareLeftGenerator *
            nativeK5SquareRightGenerator⁻¹) ≠
        (nativeK5SquareRightGenerator * nativeK5SquareLeftGenerator *
            nativeK5SquareRightGenerator⁻¹) * nativeK5SquareLeftGenerator := by
    unfold nativeK5SquareLeftGenerator nativeK5SquareRightGenerator
    decide
  exact hneq hs

/-- Apply the two fully typed paths to the NEW independently
generated genuine NINE-cell unitDiamond h. Their raw 9D evidence
has different noncommutative histories despite equal charge. -/
theorem nativeK5NineUnitDiamond_pastingWord_ne
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    (h : NativeK5StructuralSevenCell p u v) :
    (nativeK5NinePastingLeftThenRight
      (NativeK5StructuralNineCell.unitDiamond h)).historyWord ≠
    (nativeK5NinePastingRightThenLeft
      (NativeK5StructuralNineCell.unitDiamond h)).historyWord := by
  change nativeK5NineDiamondLetter *
      (nativeK5NineFrameLetter * nativeK5NineDiamondLetter *
        nativeK5NineFrameLetter⁻¹) ≠
      (nativeK5NineFrameLetter * nativeK5NineDiamondLetter *
        nativeK5NineFrameLetter⁻¹) * nativeK5NineDiamondLetter
  exact nativeK5NineLetters_conjugateNoncommute

theorem nativeK5NineUnitDiamond_pastingRaw_ne
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    (h : NativeK5StructuralSevenCell p u v) :
    nativeK5NinePastingLeftThenRight
        (NativeK5StructuralNineCell.unitDiamond h) ≠
      nativeK5NinePastingRightThenLeft
        (NativeK5StructuralNineCell.unitDiamond h) := by
  intro hraw
  exact nativeK5NineUnitDiamond_pastingWord_ne h
    (congrArg NativeK5StructuralNineCell.historyWord hraw)

#print axioms NativeK5StructuralNineCell.historyWord
#print axioms NativeK5StructuralNineCell.diamondCount
#print axioms nativeK5NinePastingLeftThenRight
#print axioms nativeK5NinePastingRightThenLeft
#print axioms nativeK5NinePasting_leftWord
#print axioms nativeK5NinePasting_rightWord
#print axioms nativeK5NinePasting_integerBlind
#print axioms nativeK5NineLetters_conjugateNoncommute
#print axioms nativeK5NineUnitDiamond_pastingWord_ne
#print axioms nativeK5NineUnitDiamond_pastingRaw_ne

end
end Kuu.F112.Physical
