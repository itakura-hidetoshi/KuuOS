import Kuu.F112.PolygonNativeF55P94DK5TypedSixCellChargeAndGroupoid
import Mathlib.Tactic

/-!
# F112-P94D3AA — free five-cell interchanger shape observers

P94D3Z's signed charge counts every independent 5D interchanger
equally. Here construct a STRICTLY FINER source/target-dependent
signed observer on genuine Type-valued five-cell syntax.

Unlike the old integer Peiffer or 5D signed charge, its independent
two axes distinguish whether the FIRST or SECOND genuine source
four-cell was a vertical composite at each 5D interchanger.

The explicit unit-reduction 5-cell changes that four-cell shape.
Hence there are two real parallel 5D naturality paths with:
 * the SAME endpoints;
 * the SAME old signed interchanger charge 1;
 * DIFFERENT first/second shape charges 0 and 1;
 * therefore no possible raw Type equality between those paths.

This is a theorem about exact OLD P94D3Y free Type syntax, not an
invented equality of Peiffer images, and does not yet assert
absence of a 6-cell in a separate presentation.
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

/-- Observation of the CONSTRUCTOR of a genuinely Type-valued
four-cell, not an observation of its Peiffer or C60 shadow. -/
def NativeK5StructuralFourCell.isVerticalComposite
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    (alpha : NativeK5StructuralFourCell p f g) : Bool :=
  match alpha with
  | .trans _ _ => true
  | _ => false

/-- A signed 5D *shape* charge, selecting the FIRST or SECOND
four-cell input of each independent interchanger generator.
Unlike P94D3Z's total interchanger charge this remembers source
constructor shape. It is an observer of OLD Type-valued syntax. -/
def NativeK5StructuralFiveCell.shapeCharge
    (selectFirst : Bool)
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    (w : NativeK5StructuralFiveCell p alpha beta) : ℤ :=
  match w with
  | .refl _ => 0
  | .symm v => -v.shapeCharge selectFirst
  | .trans v z => v.shapeCharge selectFirst + z.shapeCharge selectFirst
  | .verticalLeft v _ => v.shapeCharge selectFirst
  | .verticalRight _ v => v.shapeCharge selectFirst
  | .verticalAssoc _ _ _ => 0
  | .verticalLeftUnit _ => 0
  | .verticalRightUnit _ => 0
  | .inverseLeft _ => 0
  | .inverseRight _ => 0
  | .inverseRespect v => -v.shapeCharge selectFirst
  | .interchanger left right =>
      if (if selectFirst then left.isVerticalComposite
          else right.isVerticalComposite) then 1 else 0
  | .precompose _ v => v.shapeCharge selectFirst
  | .postcompose v _ => v.shapeCharge selectFirst

/-- A genuine 5D LEFT UNIT reduction in the OLD Type-valued
four-cell grammar: composite fourth-dimensional source to
primitive reflexivity. -/
def nativeK5UnitFiveReduction
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55StructuralComparison p r s) :
    NativeK5StructuralFiveCell p
      (.trans (.refl f) (.refl f)) (.refl f) :=
  .verticalLeftUnit (.refl f)

/-- The first shape charge distinguishes two genuine FIVE-cell
naturality paths even though both have the same boundaries. -/
theorem nativeK5LeftNaturality_shapeCounts
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55StructuralComparison p r s)
    {h k : NativeF55StructuralComparison p s t}
    (beta : NativeK5StructuralFourCell p h k) :
    (NativeK5StructuralFiveCell.interchangerLeftPathTarget
        (nativeK5UnitFiveReduction f) beta).shapeCharge true = 0 ∧
    (NativeK5StructuralFiveCell.interchangerLeftPathSource
        (nativeK5UnitFiveReduction f) beta).shapeCharge true = 1 :=
  ⟨rfl, rfl⟩

/-- The second shape charge independently detects RIGHT naturality
at the five-cell unit-reduction boundary. -/
theorem nativeK5RightNaturality_shapeCounts
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    (alpha : NativeK5StructuralFourCell p f g)
    (h : NativeF55StructuralComparison p s t) :
    (NativeK5StructuralFiveCell.interchangerRightPathTarget
        alpha (nativeK5UnitFiveReduction h)).shapeCharge false = 0 ∧
    (NativeK5StructuralFiveCell.interchangerRightPathSource
        alpha (nativeK5UnitFiveReduction h)).shapeCharge false = 1 :=
  ⟨rfl, rfl⟩

/-- Both genuinely distinct left-naturalities still have the SAME
coarse total signed 5D interchanger charge! -/
theorem nativeK5LeftNaturality_equalCoarseCharge
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55StructuralComparison p r s)
    {h k : NativeF55StructuralComparison p s t}
    (beta : NativeK5StructuralFourCell p h k) :
    (NativeK5StructuralFiveCell.interchangerLeftPathTarget
        (nativeK5UnitFiveReduction f) beta).interchangerCharge =
    (NativeK5StructuralFiveCell.interchangerLeftPathSource
        (nativeK5UnitFiveReduction f) beta).interchangerCharge := rfl

/-- Direct proof that the two authentic parallel FIVE-cell proof
terms are NOT equal in the previous unquotiented free syntax. -/
theorem nativeK5LeftNaturality_raw_ne
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55StructuralComparison p r s)
    {h k : NativeF55StructuralComparison p s t}
    (beta : NativeK5StructuralFourCell p h k) :
    NativeK5StructuralFiveCell.interchangerLeftPathTarget
        (nativeK5UnitFiveReduction f) beta ≠
    NativeK5StructuralFiveCell.interchangerLeftPathSource
        (nativeK5UnitFiveReduction f) beta := by
  intro heq
  have h := congrArg
    (fun v => NativeK5StructuralFiveCell.shapeCharge true v) heq
  change (0 : ℤ) = 1 at h
  norm_num at h

/-- The RIGHT naturality similarly fails equality as raw Type-valued
five-cell evidence, irrespective of full Peiffer image equality. -/
theorem nativeK5RightNaturality_raw_ne
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    (alpha : NativeK5StructuralFourCell p f g)
    (h : NativeF55StructuralComparison p s t) :
    NativeK5StructuralFiveCell.interchangerRightPathTarget
        alpha (nativeK5UnitFiveReduction h) ≠
    NativeK5StructuralFiveCell.interchangerRightPathSource
        alpha (nativeK5UnitFiveReduction h) := by
  intro heq
  have hneq := congrArg
    (fun v => NativeK5StructuralFiveCell.shapeCharge false v) heq
  change (0 : ℤ) = 1 at hneq
  norm_num at hneq

#print axioms NativeK5StructuralFourCell.isVerticalComposite
#print axioms NativeK5StructuralFiveCell.shapeCharge
#print axioms nativeK5UnitFiveReduction
#print axioms nativeK5LeftNaturality_shapeCounts
#print axioms nativeK5RightNaturality_shapeCounts
#print axioms nativeK5LeftNaturality_equalCoarseCharge
#print axioms nativeK5LeftNaturality_raw_ne
#print axioms nativeK5RightNaturality_raw_ne

end
end Kuu.F112.Physical
