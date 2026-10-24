import Kuu.F112.PolygonNativeF55P94DK5HorizontalSquarePermutation
import Mathlib.Tactic

/-!
# F112-P94D3AB — horizontal-square independence after full 6D naturality

The previous P94D3AA six-cell core lacked ALL naturality and square
generators. This extension includes ALL old conservative relations,
BOTH independent left/right 6-cell interchanger naturality generators,
and closure under symmetry, transitivity, 5-cell vertical congruence,
5-cell inverse congruence and the two typed 3-cell whiskerings.

It excludes exactly the TWO horizontal square generator FAMILIES:
horizontalTargetSquare and horizontalSourceSquare.

An exact constructorwise interpretation into the FULL P94D3Z 6D
grammar and an independent model into the nonabelian group S₃ show
that neither target- nor source-square boundary can be filled by
ANY composite of the retained relations. Both boundaries have
explicit 6-cells in the FULL grammar.

This proves simultaneous independence of the pair of square
generator families relative to the specified pre-square grammar.
It does NOT prove that each generator stays independent if the
other square generator family is adjoined; that stronger question
requires a further model.
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

/-- A fully dependent 6D presentation retaining the conservative
P94D3AA core and BOTH independent interchanger naturalities,
but neither horizontal naturality-square generator family. -/
inductive NativeK5PreSquareSixCell (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g},
      NativeK5StructuralFiveCell p alpha beta →
      NativeK5StructuralFiveCell p alpha beta →
      Type (max (max uD uE) (max vD vE)) where
  | core
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5PrenaturalitySixCell p w z) :
      NativeK5PreSquareSixCell p w z
  | interchangerLeftNaturality
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {h k : NativeF55StructuralComparison p s t}
      {alpha alpha' : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha alpha')
      (beta : NativeK5StructuralFourCell p h k) :
      NativeK5PreSquareSixCell p
        (NativeK5StructuralFiveCell.interchangerLeftPathTarget w beta)
        (NativeK5StructuralFiveCell.interchangerLeftPathSource w beta)
  | interchangerRightNaturality
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {h k : NativeF55StructuralComparison p s t}
      (alpha : NativeK5StructuralFourCell p f g)
      {beta beta' : NativeK5StructuralFourCell p h k}
      (w : NativeK5StructuralFiveCell p beta beta') :
      NativeK5PreSquareSixCell p
        (NativeK5StructuralFiveCell.interchangerRightPathTarget alpha w)
        (NativeK5StructuralFiveCell.interchangerRightPathSource alpha w)
  | symm
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5PreSquareSixCell p w z) :
      NativeK5PreSquareSixCell p z w
  | trans
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z q : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5PreSquareSixCell p w z)
      (v : NativeK5PreSquareSixCell p z q) :
      NativeK5PreSquareSixCell p w q
  | verticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta gamma : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5PreSquareSixCell p w z)
      (v : NativeK5StructuralFiveCell p beta gamma) :
      NativeK5PreSquareSixCell p (.trans w v) (.trans z v)
  | verticalRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta gamma : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta)
      {v z : NativeK5StructuralFiveCell p beta gamma}
      (u : NativeK5PreSquareSixCell p v z) :
      NativeK5PreSquareSixCell p (.trans w v) (.trans w z)
  | inverseRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5PreSquareSixCell p w z) :
      NativeK5PreSquareSixCell p (.symm w) (.symm z)
  | precompose
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      (prior : NativeF55StructuralComparison p r s)
      {f g : NativeF55StructuralComparison p s t}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5PreSquareSixCell p w z) :
      NativeK5PreSquareSixCell p (.precompose prior w) (.precompose prior z)
  | postcompose
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5PreSquareSixCell p w z)
      (suffix : NativeF55StructuralComparison p s t) :
      NativeK5PreSquareSixCell p (.postcompose w suffix) (.postcompose z suffix)

/-- Every pre-square 6-cell extends to the complete, genuinely
source-typed P94D3Z 6-cell grammar, constructor for constructor. -/
def NativeK5PreSquareSixCell.toFull
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    (u : NativeK5PreSquareSixCell p w z) :
    NativeK5StructuralSixCell p w z := by
  induction u with
  | core witness => exact witness.toFull
  | interchangerLeftNaturality w beta =>
      exact .interchangerLeftNaturality w beta
  | interchangerRightNaturality alpha w =>
      exact .interchangerRightNaturality alpha w
  | symm _ ih => exact .symm ih
  | trans _ _ ih₁ ih₂ => exact .trans ih₁ ih₂
  | verticalLeft witness suffix ih => exact .verticalLeft ih suffix
  | verticalRight lead witness ih => exact .verticalRight lead ih
  | inverseRespect witness ih => exact .inverseRespect ih
  | precompose prior witness ih => exact .precompose prior ih
  | postcompose witness suffix ih => exact .postcompose ih suffix

/-- The full pre-square grammar, including BOTH naturality
generators and arbitrary closure, preserves the S₃ group value.
The two square generators do not, in general, preserve it. -/
theorem NativeK5PreSquareSixCell.squarePerm_sound
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    (u : NativeK5PreSquareSixCell p w z) :
    w.squarePerm = z.squarePerm := by
  induction u with
  | core witness => exact witness.squarePerm_sound
  | interchangerLeftNaturality w beta =>
      exact nativeK5SquarePerm_leftNaturality_sound w beta
  | interchangerRightNaturality alpha w =>
      exact nativeK5SquarePerm_rightNaturality_sound alpha w
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂
  | verticalLeft witness suffix ih =>
      simpa only [NativeK5StructuralFiveCell.squarePerm] using
        congrArg (fun t : NativeK5SquarePerm => t * suffix.squarePerm) ih
  | verticalRight lead witness ih =>
      simpa only [NativeK5StructuralFiveCell.squarePerm] using
        congrArg (fun t : NativeK5SquarePerm => lead.squarePerm * t) ih
  | inverseRespect witness ih =>
      simpa only [NativeK5StructuralFiveCell.squarePerm] using
        congrArg (fun t : NativeK5SquarePerm => t⁻¹) ih
  | precompose prior witness ih => exact ih
  | postcompose witness suffix ih => exact ih

/-- Neither target-ordered square path can be connected in
the pre-square 6-cell grammar, even with BOTH interchanger
naturality generators already present. -/
theorem nativeK5TargetSquare_noPreSquareSixCell
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55StructuralComparison p r s)
    (h : NativeF55StructuralComparison p s t) :
    ¬ Nonempty (NativeK5PreSquareSixCell p
      (NativeK5StructuralFiveCell.targetSquareLeftThenRight
        (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h))
      (NativeK5StructuralFiveCell.targetSquareRightThenLeft
        (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h))) := by
  rintro ⟨u⟩
  exact nativeK5SquareTarget_perm_obstruction f h u.squarePerm_sound

/-- The same full independent noncommutative model obstructs
the source-ordered square, which is a distinct source-typed
F54 horizontal construction, not an equality of group words. -/
theorem nativeK5SourceSquare_noPreSquareSixCell
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55StructuralComparison p r s)
    (h : NativeF55StructuralComparison p s t) :
    ¬ Nonempty (NativeK5PreSquareSixCell p
      (NativeK5StructuralFiveCell.sourceSquareLeftThenRight
        (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h))
      (NativeK5StructuralFiveCell.sourceSquareRightThenLeft
        (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h))) := by
  rintro ⟨u⟩
  exact nativeK5SquareSource_perm_obstruction f h u.squarePerm_sound

/-- The target-ordered genuine 6D square generator fills a
boundary that ALL composites of the pre-square grammar cannot. -/
theorem nativeK5TargetSquare_newGeneratorEssential
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55StructuralComparison p r s)
    (h : NativeF55StructuralComparison p s t) :
    Nonempty (NativeK5StructuralSixCell p
      (NativeK5StructuralFiveCell.targetSquareLeftThenRight
        (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h))
      (NativeK5StructuralFiveCell.targetSquareRightThenLeft
        (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h))) ∧
    ¬ Nonempty (NativeK5PreSquareSixCell p
      (NativeK5StructuralFiveCell.targetSquareLeftThenRight
        (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h))
      (NativeK5StructuralFiveCell.targetSquareRightThenLeft
        (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h))) := by
  exact ⟨⟨.horizontalTargetSquare
    (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h)⟩,
    nativeK5TargetSquare_noPreSquareSixCell f h⟩

/-- The genuinely DIFFERENT source-ordered square generator
is likewise essential relative to that same pre-square syntax. -/
theorem nativeK5SourceSquare_newGeneratorEssential
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55StructuralComparison p r s)
    (h : NativeF55StructuralComparison p s t) :
    Nonempty (NativeK5StructuralSixCell p
      (NativeK5StructuralFiveCell.sourceSquareLeftThenRight
        (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h))
      (NativeK5StructuralFiveCell.sourceSquareRightThenLeft
        (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h))) ∧
    ¬ Nonempty (NativeK5PreSquareSixCell p
      (NativeK5StructuralFiveCell.sourceSquareLeftThenRight
        (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h))
      (NativeK5StructuralFiveCell.sourceSquareRightThenLeft
        (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h))) := by
  exact ⟨⟨.horizontalSourceSquare
    (nativeK5UnitFiveReduction f) (nativeK5RightUnitFiveReduction h)⟩,
    nativeK5SourceSquare_noPreSquareSixCell f h⟩

#print axioms NativeK5PreSquareSixCell
#print axioms NativeK5PreSquareSixCell.toFull
#print axioms NativeK5PreSquareSixCell.squarePerm_sound
#print axioms nativeK5TargetSquare_noPreSquareSixCell
#print axioms nativeK5SourceSquare_noPreSquareSixCell
#print axioms nativeK5TargetSquare_newGeneratorEssential
#print axioms nativeK5SourceSquare_newGeneratorEssential

end
end Kuu.F112.Physical
