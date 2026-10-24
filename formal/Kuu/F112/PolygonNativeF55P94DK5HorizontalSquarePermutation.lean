import Kuu.F112.PolygonNativeF55P94DK5PentagonatorSixCellNecessity
import Mathlib.Tactic

/-!
# F112-P94D3AB — noncommutative five-cell square observer

The integral interchanger charge and its two refined shape charges
cannot see the ORDER of two independent five-cell changes in a
horizontal naturality square. We interpret the OLD, source-typed
free five-cell syntax in the NONCOMMUTATIVE group S₃.

The 5D left- and right-unit constructors receive distinct,
noncommuting transpositions; ordinary five-cell interchangers
receive the identity permutation. The remaining constructors
are interpreted by group multiplication, inverse and functorial
transport.

Every P94D3AA conservative six-cell relation is sound for this
observer. Both independent left/right 6D naturality relations are
ALSO sound. But the two orders of the target and source square
carry distinct permutations, even when their ordinary signed
interchanger and refined shape charges both vanish.

This is a sound model for a strictly specified presentation, not
a claim about the old P92B or all higher presentations.
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

abbrev NativeK5SquarePerm := Equiv.Perm (Fin 3)

/-- The genuine 5D left-unit constructor is represented by (0 1). -/
def nativeK5SquareLeftGenerator : NativeK5SquarePerm :=
  Equiv.swap (0 : Fin 3) 1

/-- The genuine 5D right-unit constructor is represented by (1 2). -/
def nativeK5SquareRightGenerator : NativeK5SquarePerm :=
  Equiv.swap (1 : Fin 3) 2

/-- The two independent unit generators genuinely fail to commute
in S₃; the obstruction is NOT an abelian integer charge. -/
theorem nativeK5SquareGenerators_noncommute :
    nativeK5SquareLeftGenerator * nativeK5SquareRightGenerator ≠
      nativeK5SquareRightGenerator * nativeK5SquareLeftGenerator := by
  unfold nativeK5SquareLeftGenerator nativeK5SquareRightGenerator
  decide

/-- Noncommutative, dependency-respecting observation of the
exact OLD, freely generated, Type-valued five-cell syntax. -/
def NativeK5StructuralFiveCell.squarePerm
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    (w : NativeK5StructuralFiveCell p alpha beta) : NativeK5SquarePerm :=
  match w with
  | .refl _ => 1
  | .symm v => v.squarePerm⁻¹
  | .trans v z => v.squarePerm * z.squarePerm
  | .verticalLeft v _ => v.squarePerm
  | .verticalRight _ v => v.squarePerm
  | .verticalAssoc _ _ _ => 1
  | .verticalLeftUnit _ => nativeK5SquareLeftGenerator
  | .verticalRightUnit _ => nativeK5SquareRightGenerator
  | .inverseLeft _ => 1
  | .inverseRight _ => 1
  | .inverseRespect v => v.squarePerm⁻¹
  | .interchanger _ _ => 1
  | .precompose _ v => v.squarePerm
  | .postcompose v _ => v.squarePerm

/-- All conservative 6D relations preserve the NONCOMMUTATIVE
permutation observer. In particular, no abelianization or
syntactic equality of distinct Type-valued 5-cells is used. -/
theorem NativeK5PrenaturalitySixCell.squarePerm_sound
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    (u : NativeK5PrenaturalitySixCell p w z) :
    w.squarePerm = z.squarePerm := by
  induction u with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂
  | verticalLeft witness suffix ih =>
      simpa only [NativeK5StructuralFiveCell.squarePerm] using
        congrArg (fun t : NativeK5SquarePerm => t * suffix.squarePerm) ih
  | verticalRight lead witness ih =>
      simpa only [NativeK5StructuralFiveCell.squarePerm] using
        congrArg (fun t : NativeK5SquarePerm => lead.squarePerm * t) ih
  | verticalAssoc a b c =>
      change (a.squarePerm * b.squarePerm) * c.squarePerm =
        a.squarePerm * (b.squarePerm * c.squarePerm)
      exact mul_assoc _ _ _
  | verticalLeftUnit _ => simp [NativeK5StructuralFiveCell.squarePerm]
  | verticalRightUnit _ => simp [NativeK5StructuralFiveCell.squarePerm]
  | inverseLeft _ => simp [NativeK5StructuralFiveCell.squarePerm]
  | inverseRight _ => simp [NativeK5StructuralFiveCell.squarePerm]
  | inverseRespect witness ih =>
      simpa only [NativeK5StructuralFiveCell.squarePerm] using
        congrArg (fun t : NativeK5SquarePerm => t⁻¹) ih
  | precompose _ witness ih => exact ih
  | postcompose witness _ ih => exact ih

/-- Even AFTER adding left naturality, the S₃ observer is sound:
the independent interchanger itself maps to the neutral element. -/
theorem nativeK5SquarePerm_leftNaturality_sound
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {h k : NativeF55StructuralComparison p s t}
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (beta : NativeK5StructuralFourCell p h k) :
    (NativeK5StructuralFiveCell.interchangerLeftPathTarget w beta).squarePerm =
      (NativeK5StructuralFiveCell.interchangerLeftPathSource w beta).squarePerm := by
  change w.squarePerm * 1 = 1 * w.squarePerm
  simp

/-- Right naturality is also sound for the SAME S₃ observer. -/
theorem nativeK5SquarePerm_rightNaturality_sound
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {h k : NativeF55StructuralComparison p s t}
    (alpha : NativeK5StructuralFourCell p f g)
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p beta beta') :
    (NativeK5StructuralFiveCell.interchangerRightPathTarget alpha w).squarePerm =
      (NativeK5StructuralFiveCell.interchangerRightPathSource alpha w).squarePerm := by
  change w.squarePerm * 1 = 1 * w.squarePerm
  simp

/-- A second ACTUAL five-cell unit reduction, independent from
the pre-existing left unit reduction. -/
def nativeK5RightUnitFiveReduction
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55StructuralComparison p r s) :
    NativeK5StructuralFiveCell p
      (.trans (.refl f) (.refl f)) (.refl f) :=
  .verticalRightUnit (.refl f)

/-- The two possible target-ordered square paths yield *different*
actual S₃ group elements, even though they have common dependent
four-cell endpoints. -/
theorem nativeK5SquareTarget_perm_obstruction
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55StructuralComparison p r s)
    (h : NativeF55StructuralComparison p s t) :
    (NativeK5StructuralFiveCell.targetSquareLeftThenRight
      (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h)).squarePerm ≠
    (NativeK5StructuralFiveCell.targetSquareRightThenLeft
      (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h)).squarePerm := by
  change nativeK5SquareLeftGenerator * nativeK5SquareRightGenerator ≠
    nativeK5SquareRightGenerator * nativeK5SquareLeftGenerator
  exact nativeK5SquareGenerators_noncommute

/-- The *alternative source-ordered* genuine horizontal square
independently has exactly the same noncommutative obstruction. -/
theorem nativeK5SquareSource_perm_obstruction
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55StructuralComparison p r s)
    (h : NativeF55StructuralComparison p s t) :
    (NativeK5StructuralFiveCell.sourceSquareLeftThenRight
      (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h)).squarePerm ≠
    (NativeK5StructuralFiveCell.sourceSquareRightThenLeft
      (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h)).squarePerm := by
  change nativeK5SquareLeftGenerator * nativeK5SquareRightGenerator ≠
    nativeK5SquareRightGenerator * nativeK5SquareLeftGenerator
  exact nativeK5SquareGenerators_noncommute

#print axioms nativeK5SquareGenerators_noncommute
#print axioms NativeK5StructuralFiveCell.squarePerm
#print axioms NativeK5PrenaturalitySixCell.squarePerm_sound
#print axioms nativeK5SquarePerm_leftNaturality_sound
#print axioms nativeK5SquarePerm_rightNaturality_sound
#print axioms nativeK5RightUnitFiveReduction
#print axioms nativeK5SquareTarget_perm_obstruction
#print axioms nativeK5SquareSource_perm_obstruction

end
end Kuu.F112.Physical
