import Kuu.F112.PolygonNativeF55P94DK5PentagonatorThirteenCellNecessity
import Kuu.F112.PolygonNativeF55P94DConservativeTowerDescent
import Mathlib.Tactic

/-!
# F112-P94D3AL — genuine 13D noncommutative inverse-square pasting

Start with ORIGINAL Type-valued 13-cell proofs, not a 3D graph
or a strictification surrogate. Construct two dependent 13D
double-whiskering paths at exactly the same ORIGINAL 12D endpoints.
A chosen two-letter free-group observer separates the raw terms,
while the signed 13D square count cannot. The five-stage original
C60 K5 physical boundary is included.

AL also connects the prior 13D conservative grammar to the
dimension-independent finite-closure theorem: NONE of its finite
conservative closures can fill the original 12D exchange pair,
although independently adjoined genuine 13D comparisons can.
This is a grammar-relative statement, not arbitrary higher coherence,
complete P92B descent or global strict 3/n.
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

abbrev NativeK5ThirteenHistoryWord := FreeGroup (Fin 2)

def nativeK5ThirteenExchangeLetter : NativeK5ThirteenHistoryWord :=
  FreeGroup.of (0 : Fin 2)

def nativeK5ThirteenInverseFrame : NativeK5ThirteenHistoryWord :=
  FreeGroup.of (1 : Fin 2)

/-- Chosen universal free-group observer of genuine original 13D
proof syntax. The inversion-respect constructor for genuine 12D
witnesses acts by selected B-conjugation. -/
def NativeK5StructuralThirteenCell.historyWord
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
    (T : NativeK5StructuralThirteenCell p U V) :
    NativeK5ThirteenHistoryWord :=
  match T with
  | .core _ => 1
  | .squareExchange _ => nativeK5ThirteenExchangeLetter
  | .symm X => X.historyWord⁻¹
  | .trans X Y => X.historyWord * Y.historyWord
  | .twelveVerticalLeft X _ => X.historyWord
  | .twelveVerticalRight _ X => X.historyWord
  | .twelveSymmRespect X =>
      nativeK5ThirteenInverseFrame * X.historyWord *
        nativeK5ThirteenInverseFrame⁻¹
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

/-- Scalar signed 13D generator count, forgetting word order. -/
def NativeK5StructuralThirteenCell.squareCount
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
    (T : NativeK5StructuralThirteenCell p U V) : ℤ :=
  match T with
  | .core _ => 0
  | .squareExchange _ => 1
  | .symm X => -X.squareCount
  | .trans X Y => X.squareCount + Y.squareCount
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

/-- Genuine dependent 13D left-first pasting, between ORIGINAL
12D witnesses (U;U⁻¹) and (V;V⁻¹). -/
def nativeK5ThirteenPastingLeftThenRight
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
    (T : NativeK5StructuralThirteenCell p U V) :
    NativeK5StructuralThirteenCell p
      (.trans U (.symm U)) (.trans V (.symm V)) :=
  .trans (.twelveVerticalLeft T (.symm U))
    (.twelveVerticalRight V (.twelveSymmRespect T))

/-- Opposite genuine dependent 13D right-first pasting, same
EXACT ORIGINAL 12D source and target as the first. -/
def nativeK5ThirteenPastingRightThenLeft
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
    (T : NativeK5StructuralThirteenCell p U V) :
    NativeK5StructuralThirteenCell p
      (.trans U (.symm U)) (.trans V (.symm V)) :=
  .trans (.twelveVerticalRight U (.twelveSymmRespect T))
    (.twelveVerticalLeft T (.symm V))

theorem nativeK5ThirteenPasting_leftWord
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
    (T : NativeK5StructuralThirteenCell p U V) :
    (nativeK5ThirteenPastingLeftThenRight T).historyWord =
      T.historyWord *
        (nativeK5ThirteenInverseFrame * T.historyWord *
          nativeK5ThirteenInverseFrame⁻¹) := rfl

theorem nativeK5ThirteenPasting_rightWord
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
    (T : NativeK5StructuralThirteenCell p U V) :
    (nativeK5ThirteenPastingRightThenLeft T).historyWord =
      (nativeK5ThirteenInverseFrame * T.historyWord *
        nativeK5ThirteenInverseFrame⁻¹) * T.historyWord := rfl

theorem nativeK5ThirteenPasting_integerBlind
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
    (T : NativeK5StructuralThirteenCell p U V) :
    (nativeK5ThirteenPastingLeftThenRight T).squareCount =
      (nativeK5ThirteenPastingRightThenLeft T).squareCount := rfl

/-- The previously certified genuine S3 free-group witness is
reused, without new axioms or assuming commutative history. -/
theorem nativeK5ThirteenExchangeFrame_noncommute :
    nativeK5ThirteenExchangeLetter *
        (nativeK5ThirteenInverseFrame * nativeK5ThirteenExchangeLetter *
          nativeK5ThirteenInverseFrame⁻¹) ≠
      (nativeK5ThirteenInverseFrame * nativeK5ThirteenExchangeLetter *
          nativeK5ThirteenInverseFrame⁻¹) * nativeK5ThirteenExchangeLetter := by
  change nativeK5TwelveExchangeLetter *
      (nativeK5TwelveInverseFrame * nativeK5TwelveExchangeLetter *
        nativeK5TwelveInverseFrame⁻¹) ≠
    (nativeK5TwelveInverseFrame * nativeK5TwelveExchangeLetter *
      nativeK5TwelveInverseFrame⁻¹) * nativeK5TwelveExchangeLetter
  exact nativeK5TwelveExchangeFrame_noncommute

/-- Genuine independent 13D squareExchange produces two
original 13D paths with different chosen free-group histories. -/
theorem nativeK5ThirteenSquareExchange_pastingWord_ne
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
    (T : NativeK5StructuralTwelveCell p U V) :
    (nativeK5ThirteenPastingLeftThenRight
      (NativeK5StructuralThirteenCell.squareExchange T)).historyWord ≠
    (nativeK5ThirteenPastingRightThenLeft
      (NativeK5StructuralThirteenCell.squareExchange T)).historyWord := by
  change nativeK5ThirteenExchangeLetter *
      (nativeK5ThirteenInverseFrame * nativeK5ThirteenExchangeLetter *
        nativeK5ThirteenInverseFrame⁻¹) ≠
    (nativeK5ThirteenInverseFrame * nativeK5ThirteenExchangeLetter *
      nativeK5ThirteenInverseFrame⁻¹) * nativeK5ThirteenExchangeLetter
  exact nativeK5ThirteenExchangeFrame_noncommute

/-- Distinct free histories prove inequality of the true raw
source-dependent 13D proof terms; no 14D quotient is assumed. -/
theorem nativeK5ThirteenSquareExchange_pastingRaw_ne
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
    (T : NativeK5StructuralTwelveCell p U V) :
    nativeK5ThirteenPastingLeftThenRight
      (NativeK5StructuralThirteenCell.squareExchange T) ≠
    nativeK5ThirteenPastingRightThenLeft
      (NativeK5StructuralThirteenCell.squareExchange T) := by
  intro h
  exact nativeK5ThirteenSquareExchange_pastingWord_ne T
    (congrArg NativeK5StructuralThirteenCell.historyWord h)



/-- No finite number of purely conservative coherence operations
can connect the exact ORIGINAL 12D inverse-square critical pair
arising from an original independent 12D squareExchange.
The witness types remain the actual source-dependent boundary fiber. -/
theorem nativeK5Thirteen_noFiniteCoreFiller
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
    (X : NativeK5StructuralElevenCell p P Q)
    (n : Nat) :
    ¬ Nonempty
      (NativeConservativeTower
        (fun U V : NativeK5StructuralTwelveCell p
          (.trans (nativeK5ElevenPastingLeftThenRight X)
            (.symm (nativeK5ElevenPastingLeftThenRight X)))
          (.trans (nativeK5ElevenPastingRightThenLeft X)
            (.symm (nativeK5ElevenPastingRightThenLeft X))) =>
          NativeK5CoreThirteenCell p U V)
        n
        (nativeK5TwelvePastingLeftThenRight
          (NativeK5StructuralTwelveCell.squareExchange X))
        (nativeK5TwelvePastingRightThenLeft
          (NativeK5StructuralTwelveCell.squareExchange X))) := by
  exact NativeConservativeTower.no_finite_filler
    (fun U : NativeK5StructuralTwelveCell p
      (.trans (nativeK5ElevenPastingLeftThenRight X)
        (.symm (nativeK5ElevenPastingLeftThenRight X)))
      (.trans (nativeK5ElevenPastingRightThenLeft X)
        (.symm (nativeK5ElevenPastingRightThenLeft X))) => U.historyWord)
    (fun {U V} (h : NativeK5CoreThirteenCell p U V) =>
      h.historyWord_sound)
    (nativeK5TwelveSquareExchange_pastingWord_ne X)
    n

/-- The independent genuine 13D square gives an actual new
comparison, but cannot retract into ANY finite core closure. -/
theorem nativeK5Thirteen_noFiniteCoreRetraction
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
    (X : NativeK5StructuralElevenCell p P Q)
    (n : Nat) :
    ¬ Nonempty
      (NativeK5StructuralThirteenCell p
        (nativeK5TwelvePastingLeftThenRight
          (NativeK5StructuralTwelveCell.squareExchange X))
        (nativeK5TwelvePastingRightThenLeft
          (NativeK5StructuralTwelveCell.squareExchange X)) →
       NativeConservativeTower
        (fun U V : NativeK5StructuralTwelveCell p
          (.trans (nativeK5ElevenPastingLeftThenRight X)
            (.symm (nativeK5ElevenPastingLeftThenRight X)))
          (.trans (nativeK5ElevenPastingRightThenLeft X)
            (.symm (nativeK5ElevenPastingRightThenLeft X))) =>
          NativeK5CoreThirteenCell p U V)
        n
        (nativeK5TwelvePastingLeftThenRight
          (NativeK5StructuralTwelveCell.squareExchange X))
        (nativeK5TwelvePastingRightThenLeft
          (NativeK5StructuralTwelveCell.squareExchange X))) := by
  rintro ⟨retract⟩
  exact nativeK5Thirteen_noFiniteCoreFiller X n
    ⟨retract (NativeK5StructuralThirteenCell.squareExchange
       (NativeK5StructuralTwelveCell.squareExchange X))⟩

/-- In contrast, the actual 13D quotient admits integer descent
but rejects this chosen noncommutative history. -/
theorem nativeK5Thirteen_originObserverSeparation
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
    (X : NativeK5StructuralElevenCell p P Q) :
    (∃ F : NativeK5ThirteenCellTwelveClasses
      (.trans (nativeK5ElevenPastingLeftThenRight X)
        (.symm (nativeK5ElevenPastingLeftThenRight X)))
      (.trans (nativeK5ElevenPastingRightThenLeft X)
        (.symm (nativeK5ElevenPastingRightThenLeft X))) → ℤ,
      ∀ U, F (nativeK5ThirteenCellTwelveClass U) = U.squareCount) ∧
    ¬ ∃ G : NativeK5ThirteenCellTwelveClasses
      (.trans (nativeK5ElevenPastingLeftThenRight X)
        (.symm (nativeK5ElevenPastingLeftThenRight X)))
      (.trans (nativeK5ElevenPastingRightThenLeft X)
        (.symm (nativeK5ElevenPastingRightThenLeft X))) → NativeK5TwelveHistoryWord,
      ∀ U, G (nativeK5ThirteenCellTwelveClass U) = U.historyWord := by
  constructor
  · exact ⟨nativeK5ThirteenCellTwelveSquareCount, fun _ => rfl⟩
  · exact nativeK5TwelveHistoryWord_noThirteenDescent
      (NativeK5StructuralTwelveCell.squareExchange X)
      (nativeK5TwelveSquareExchange_pastingWord_ne X)

/- Specialization of the new 14D critical pair to the five actual
original F45 stages of the C60 K5 pentagonator. No 14D filler is
adjoined or asserted in AL. -/
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

/-- Independent original 13D K5 comparison (AK) as real input. -/
def nativeK5PentagonatorFourteenExchangeThirteen :=
  nativeK5PentagonatorThirteenExchange t1 t2 t3 t4 t5

def nativeK5PentagonatorFourteenLeftFirst :=
  nativeK5ThirteenPastingLeftThenRight
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)

def nativeK5PentagonatorFourteenRightFirst :=
  nativeK5ThirteenPastingRightThenLeft
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)

theorem nativeK5PentagonatorFourteen_integerBlind :
    (nativeK5PentagonatorFourteenLeftFirst t1 t2 t3 t4 t5).squareCount =
    (nativeK5PentagonatorFourteenRightFirst t1 t2 t3 t4 t5).squareCount :=
  nativeK5ThirteenPasting_integerBlind
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)

theorem nativeK5PentagonatorFourteen_history_ne :
    (nativeK5PentagonatorFourteenLeftFirst t1 t2 t3 t4 t5).historyWord ≠
    (nativeK5PentagonatorFourteenRightFirst t1 t2 t3 t4 t5).historyWord :=
  nativeK5ThirteenSquareExchange_pastingWord_ne
    (nativeK5PentagonatorThirteenExchangeTwelve t1 t2 t3 t4 t5)

theorem nativeK5PentagonatorFourteen_raw_ne :
    nativeK5PentagonatorFourteenLeftFirst t1 t2 t3 t4 t5 ≠
    nativeK5PentagonatorFourteenRightFirst t1 t2 t3 t4 t5 :=
  nativeK5ThirteenSquareExchange_pastingRaw_ne
    (nativeK5PentagonatorThirteenExchangeTwelve t1 t2 t3 t4 t5)

end GenuineFiveStage

#print axioms NativeK5StructuralThirteenCell.historyWord
#print axioms NativeK5StructuralThirteenCell.squareCount
#print axioms nativeK5ThirteenPastingLeftThenRight
#print axioms nativeK5ThirteenPastingRightThenLeft
#print axioms nativeK5ThirteenPasting_integerBlind
#print axioms nativeK5ThirteenExchangeFrame_noncommute
#print axioms nativeK5ThirteenSquareExchange_pastingWord_ne
#print axioms nativeK5ThirteenSquareExchange_pastingRaw_ne
#print axioms nativeK5Thirteen_noFiniteCoreFiller
#print axioms nativeK5Thirteen_noFiniteCoreRetraction
#print axioms nativeK5Thirteen_originObserverSeparation
#print axioms nativeK5PentagonatorFourteen_history_ne
#print axioms nativeK5PentagonatorFourteen_raw_ne

end
end Kuu.F112.Physical
