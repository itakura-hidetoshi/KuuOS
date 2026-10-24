import Kuu.F112.PolygonNativeF55P94DK5PreSquareSixCellObstruction
import Mathlib.Tactic

/-!
# F112-P94D3AB — genuine five-stage K5 pentagonator square obstruction

The preceding results chose unit reductions of structural identity
four-cells. Here the reductions act on arbitrary genuine Type-valued
4-cells, then explicitly on the INDEPENDENT 4D pentagonator of the
actual C60 five-stage F45 K5 nine-face cycle.

Both genuinely dependent target- and source-ordered square boundaries
admit 6D fillers in the complete new P94D3Z grammar, and neither
admits any 6D filler in the conservative grammar EXTENDED BY BOTH
interchanger naturality generators.

The obstruction is the two distinct compositions of (0 1) and
(1 2) in S₃. It is independent of the integer interchanger charge,
its earlier refined shape charge and the four-cell Peiffer image.

No descent to pre-existing P92B or global strict 3/n category,
and no hyperdescent result, is asserted.
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

section GenuineFourCellSquare

variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {h k : NativeF55StructuralComparison p s t}

/-- The independent TARGET square generator is necessary even
when the two genuine 5D unit changes act on arbitrary original
source-typed four-cells, not merely on identity four-cells. -/
theorem nativeK5TargetSquare_fourCellIndependence
    (alpha : NativeK5StructuralFourCell p f g)
    (beta : NativeK5StructuralFourCell p h k) :
    Nonempty (NativeK5StructuralSixCell p
      (NativeK5StructuralFiveCell.targetSquareLeftThenRight
        (.verticalLeftUnit alpha) (.verticalRightUnit beta))
      (NativeK5StructuralFiveCell.targetSquareRightThenLeft
        (.verticalLeftUnit alpha) (.verticalRightUnit beta))) ∧
    ¬ Nonempty (NativeK5PreSquareSixCell p
      (NativeK5StructuralFiveCell.targetSquareLeftThenRight
        (.verticalLeftUnit alpha) (.verticalRightUnit beta))
      (NativeK5StructuralFiveCell.targetSquareRightThenLeft
        (.verticalLeftUnit alpha) (.verticalRightUnit beta))) := by
  refine ⟨⟨NativeK5StructuralSixCell.horizontalTargetSquare
    (.verticalLeftUnit alpha) (.verticalRightUnit beta)⟩, ?_⟩
  rintro ⟨u⟩
  have hperm := u.squarePerm_sound
  change nativeK5SquareLeftGenerator * nativeK5SquareRightGenerator =
    nativeK5SquareRightGenerator * nativeK5SquareLeftGenerator at hperm
  exact nativeK5SquareGenerators_noncommute hperm

/-- The SOURCE-ordered horizontal square has an independent
obstruction on the SAME pair of arbitrary Type-valued four-cells. -/
theorem nativeK5SourceSquare_fourCellIndependence
    (alpha : NativeK5StructuralFourCell p f g)
    (beta : NativeK5StructuralFourCell p h k) :
    Nonempty (NativeK5StructuralSixCell p
      (NativeK5StructuralFiveCell.sourceSquareLeftThenRight
        (.verticalLeftUnit alpha) (.verticalRightUnit beta))
      (NativeK5StructuralFiveCell.sourceSquareRightThenLeft
        (.verticalLeftUnit alpha) (.verticalRightUnit beta))) ∧
    ¬ Nonempty (NativeK5PreSquareSixCell p
      (NativeK5StructuralFiveCell.sourceSquareLeftThenRight
        (.verticalLeftUnit alpha) (.verticalRightUnit beta))
      (NativeK5StructuralFiveCell.sourceSquareRightThenLeft
        (.verticalLeftUnit alpha) (.verticalRightUnit beta))) := by
  refine ⟨⟨NativeK5StructuralSixCell.horizontalSourceSquare
    (.verticalLeftUnit alpha) (.verticalRightUnit beta)⟩, ?_⟩
  rintro ⟨u⟩
  have hperm := u.squarePerm_sound
  change nativeK5SquareLeftGenerator * nativeK5SquareRightGenerator =
    nativeK5SquareRightGenerator * nativeK5SquareLeftGenerator at hperm
  exact nativeK5SquareGenerators_noncommute hperm

end GenuineFourCellSquare

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

/-- The ACTUAL independently generated K5 pentagonator is used
twice as the input of the two distinct five-cell unit changes.
Both orders of TARGET-horizontal pasting have a full 6-cell, and
NO conservative-plus-both-naturality 6-cell. -/
theorem nativeK5Pentagonator_targetSquareIndependence :
    Nonempty (NativeK5StructuralSixCell p
      (NativeK5StructuralFiveCell.targetSquareLeftThenRight
        (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
        (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)))
      (NativeK5StructuralFiveCell.targetSquareRightThenLeft
        (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
        (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)))) ∧
    ¬ Nonempty (NativeK5PreSquareSixCell p
      (NativeK5StructuralFiveCell.targetSquareLeftThenRight
        (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
        (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)))
      (NativeK5StructuralFiveCell.targetSquareRightThenLeft
        (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
        (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)))) :=
  nativeK5TargetSquare_fourCellIndependence
    (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)
    (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)

/-- The alternative SOURCE-horizontal pasting on that SAME
genuine five-stage pentagonator also requires a square generator,
despite retaining both 6D left and right naturalities. -/
theorem nativeK5Pentagonator_sourceSquareIndependence :
    Nonempty (NativeK5StructuralSixCell p
      (NativeK5StructuralFiveCell.sourceSquareLeftThenRight
        (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
        (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)))
      (NativeK5StructuralFiveCell.sourceSquareRightThenLeft
        (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
        (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)))) ∧
    ¬ Nonempty (NativeK5PreSquareSixCell p
      (NativeK5StructuralFiveCell.sourceSquareLeftThenRight
        (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
        (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)))
      (NativeK5StructuralFiveCell.sourceSquareRightThenLeft
        (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
        (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)))) :=
  nativeK5SourceSquare_fourCellIndependence
    (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)
    (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)

#print axioms nativeK5TargetSquare_fourCellIndependence
#print axioms nativeK5SourceSquare_fourCellIndependence
#print axioms nativeK5Pentagonator_targetSquareIndependence
#print axioms nativeK5Pentagonator_sourceSquareIndependence

end GenuineFiveStage
end
end Kuu.F112.Physical
