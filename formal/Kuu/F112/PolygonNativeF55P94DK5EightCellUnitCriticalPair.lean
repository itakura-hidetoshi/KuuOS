import Kuu.F112.PolygonNativeF55P94DK5PentagonatorEightCellNecessity
import Kuu.F112.PolygonNativeF55P94DK5HorizontalSquarePermutation
import Mathlib.GroupTheory.FreeGroup.Basic
import Mathlib.Tactic

/-!
# F112-P94D3AF — two original typed eight-cell unit-normalization paths

From the P94D3AE original Type-valued EIGHT-cell syntax, take any
genuine seven-cell h : u ⇒ v. The raw seven-cell expression
  ((id_u ⋅ h) ⋅ id_v)
normalizes to h in TWO different genuine eight-cell pasting orders:

  left-unit in the first subword, then right-unit;
  right-unit on the outer expression, then left-unit.

The paths have exactly identical dependent 7D boundaries and
the same signed integer unit count (2). But a FreeGroup on TWO
independent symbols records opposite orderings. Its S₃ evaluation
certifies noncommutativity without collapsing to abelian charge.

The chosen word observer is over the ORIGINAL 8D syntax, not a
claim that the proposed 9D comparison is already derivable.
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

abbrev NativeK5EightUnitWord := FreeGroup (Fin 2)

def nativeK5EightUnitLeftLetter : NativeK5EightUnitWord :=
  FreeGroup.of (0 : Fin 2)

def nativeK5EightUnitRightLetter : NativeK5EightUnitWord :=
  FreeGroup.of (1 : Fin 2)

/-- The unquotiented old CORE eight-cell constructor history, as
the universal word in left/right 7D unit-normalization symbols.
Other structural eight-cell constructors are neutral or transport
the entire original ordered word. -/
def NativeK5CoreEightCell.unitWord
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
    (e : NativeK5CoreEightCell p h k) : NativeK5EightUnitWord :=
  match e with
  | .refl _ => 1
  | .symm e => e.unitWord⁻¹
  | .trans e d => e.unitWord * d.unitWord
  | .sevenAssoc _ _ _ => 1
  | .sevenLeftUnit _ => nativeK5EightUnitLeftLetter
  | .sevenRightUnit _ => nativeK5EightUnitRightLetter
  | .sevenInverseLeft _ => 1
  | .sevenInverseRight _ => 1
  | .sevenVerticalLeft e _ => e.unitWord
  | .sevenVerticalRight _ e => e.unitWord
  | .sevenSymmRespect e => e.unitWord
  | .sixVerticalLeft e _ => e.unitWord
  | .sixVerticalRight _ e => e.unitWord
  | .sixInverseRespect e => e.unitWord
  | .fiveVerticalLeft e _ => e.unitWord
  | .fiveVerticalRight _ e => e.unitWord
  | .fiveInverseRespect e => e.unitWord
  | .precompose _ e => e.unitWord
  | .postcompose e _ => e.unitWord

/-- Extend the same word observer to genuine P94D3AE EIGHT-cell
syntax, including its independent squareExchange. The latter
has no unit-normalization letter in this selected observer. -/
def NativeK5StructuralEightCell.unitWord
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
    (e : NativeK5StructuralEightCell p h k) : NativeK5EightUnitWord :=
  match e with
  | .core e => e.unitWord
  | .squareExchange _ => 1
  | .symm e => e.unitWord⁻¹
  | .trans e d => e.unitWord * d.unitWord

/-- Scalar unit count is the abelian shadow of the word grammar.
It discards both the order and which of the two unit laws occurred. -/
def NativeK5CoreEightCell.unitCount
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
    (e : NativeK5CoreEightCell p h k) : ℤ :=
  match e with
  | .refl _ => 0
  | .symm e => -e.unitCount
  | .trans e d => e.unitCount + d.unitCount
  | .sevenAssoc _ _ _ => 0
  | .sevenLeftUnit _ => 1
  | .sevenRightUnit _ => 1
  | .sevenInverseLeft _ => 0
  | .sevenInverseRight _ => 0
  | .sevenVerticalLeft e _ => e.unitCount
  | .sevenVerticalRight _ e => e.unitCount
  | .sevenSymmRespect e => e.unitCount
  | .sixVerticalLeft e _ => e.unitCount
  | .sixVerticalRight _ e => e.unitCount
  | .sixInverseRespect e => e.unitCount
  | .fiveVerticalLeft e _ => e.unitCount
  | .fiveVerticalRight _ e => e.unitCount
  | .fiveInverseRespect e => e.unitCount
  | .precompose _ e => e.unitCount
  | .postcompose e _ => e.unitCount

def NativeK5StructuralEightCell.unitCount
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
    (e : NativeK5StructuralEightCell p h k) : ℤ :=
  match e with
  | .core e => e.unitCount
  | .squareExchange _ => 0
  | .symm e => -e.unitCount
  | .trans e d => e.unitCount + d.unitCount

section CriticalPair

variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {alpha beta : NativeK5StructuralFourCell p f g}
variable {w z : NativeK5StructuralFiveCell p alpha beta}
variable {u v : NativeK5StructuralSixCell p w z}

/-- Normalize the LEFT unit in the inner seven-cell composite first. -/
def nativeK5EightUnitLeftFirst
    (h : NativeK5StructuralSevenCell p u v) :
    NativeK5StructuralEightCell p
      (.trans (.trans (.core (.refl u)) h) (.core (.refl v))) h :=
  .trans
    (.core (.sevenVerticalLeft (.sevenLeftUnit h) (.core (.refl v))))
    (.core (.sevenRightUnit h))

/-- Normalize the RIGHT unit on the outer seven-cell expression
first, then normalize the left unit. This is a distinct 8-cell
proof with EXACT same dependent seven-cell boundaries. -/
def nativeK5EightUnitRightFirst
    (h : NativeK5StructuralSevenCell p u v) :
    NativeK5StructuralEightCell p
      (.trans (.trans (.core (.refl u)) h) (.core (.refl v))) h :=
  .trans
    (.core (.sevenRightUnit (.trans (.core (.refl u)) h)))
    (.core (.sevenLeftUnit h))

theorem nativeK5EightUnitLeftFirst_word
    (h : NativeK5StructuralSevenCell p u v) :
    (nativeK5EightUnitLeftFirst h).unitWord =
      nativeK5EightUnitLeftLetter * nativeK5EightUnitRightLetter := rfl

theorem nativeK5EightUnitRightFirst_word
    (h : NativeK5StructuralSevenCell p u v) :
    (nativeK5EightUnitRightFirst h).unitWord =
      nativeK5EightUnitRightLetter * nativeK5EightUnitLeftLetter := rfl

theorem nativeK5EightUnitPair_sameInteger
    (h : NativeK5StructuralSevenCell p u v) :
    (nativeK5EightUnitLeftFirst h).unitCount = 2 ∧
    (nativeK5EightUnitRightFirst h).unitCount = 2 := by
  exact ⟨rfl, rfl⟩

end CriticalPair

/-- A single finite S₃ evaluation detects a genuine inequality of
two distinct universal FREE-GROUP words; no claim that this
finite group is the universal history invariant is made. -/
def nativeK5EightUnitWordToS3 : NativeK5EightUnitWord →* NativeK5SquarePerm :=
  FreeGroup.lift (fun b : Fin 2 =>
    if b = 0 then nativeK5SquareLeftGenerator else nativeK5SquareRightGenerator)

theorem nativeK5EightUnitWordToS3_left :
    nativeK5EightUnitWordToS3 nativeK5EightUnitLeftLetter =
      nativeK5SquareLeftGenerator := by
  simp [nativeK5EightUnitWordToS3, nativeK5EightUnitLeftLetter]

theorem nativeK5EightUnitWordToS3_right :
    nativeK5EightUnitWordToS3 nativeK5EightUnitRightLetter =
      nativeK5SquareRightGenerator := by
  simp [nativeK5EightUnitWordToS3, nativeK5EightUnitRightLetter]

theorem nativeK5EightUnitLetters_noncommute :
    nativeK5EightUnitLeftLetter * nativeK5EightUnitRightLetter ≠
      nativeK5EightUnitRightLetter * nativeK5EightUnitLeftLetter := by
  intro h
  have hh := congrArg nativeK5EightUnitWordToS3 h
  simp only [map_mul, nativeK5EightUnitWordToS3_left,
    nativeK5EightUnitWordToS3_right] at hh
  exact nativeK5SquareGenerators_noncommute hh

theorem nativeK5EightUnitPair_word_ne
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
    (nativeK5EightUnitLeftFirst h).unitWord ≠
      (nativeK5EightUnitRightFirst h).unitWord := by
  rw [nativeK5EightUnitLeftFirst_word,
    nativeK5EightUnitRightFirst_word]
  exact nativeK5EightUnitLetters_noncommute

theorem nativeK5EightUnitPair_raw_ne
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
    nativeK5EightUnitLeftFirst h ≠
      nativeK5EightUnitRightFirst h := by
  intro eq
  exact nativeK5EightUnitPair_word_ne h
    (congrArg NativeK5StructuralEightCell.unitWord eq)

#print axioms NativeK5CoreEightCell.unitWord
#print axioms NativeK5StructuralEightCell.unitWord
#print axioms NativeK5CoreEightCell.unitCount
#print axioms NativeK5StructuralEightCell.unitCount
#print axioms nativeK5EightUnitLeftFirst
#print axioms nativeK5EightUnitRightFirst
#print axioms nativeK5EightUnitPair_sameInteger
#print axioms nativeK5EightUnitWordToS3
#print axioms nativeK5EightUnitLetters_noncommute
#print axioms nativeK5EightUnitPair_word_ne
#print axioms nativeK5EightUnitPair_raw_ne

end
end Kuu.F112.Physical
