import Kuu.F112.PolygonNativeF55P94DK5SingleSquareMutualDerivation
import Mathlib.Tactic

/-!
# F112-P94D3AC — minimal one-square coherence at genuine C60 K5

Use the ACTUAL five F45 stages and their independently generated
Type-valued K5 pentagonator. The target-only 6-cell grammar fills
the SOURCE square of two distinct five-cell unit reductions of that
pentagonator, and the source-only grammar fills the TARGET square.

The PRE-SQUARE grammar of P94D3AB, even including both independent
6D naturality generators, fills NEITHER. Thus a horizontal square
family is necessary, but EITHER target or source family is sufficient.
Both full-grammar six-cell existence relations agree with either
single-family construction (P94D3AC generic source theorem).

The result does not assert literal equality of raw 6D proof terms
or any old P92B descent, global strict 3/n, or (∞,3)-hyperdescent.
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

/-- Authentic K5 independent 4D pentagonator: target-only
6D presentation constructs the formally omitted SOURCE square. -/
theorem nativeK5Pentagonator_targetOnlyFillsSourceSquare :
    Nonempty (NativeK5SquarePolicySixCell true false p
      (NativeK5StructuralFiveCell.sourceSquareLeftThenRight
        (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
        (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)))
      (NativeK5StructuralFiveCell.sourceSquareRightThenLeft
        (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
        (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)))) :=
  ⟨nativeK5TargetOnly_generatesSourceSquare
    (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
    (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))⟩

/-- The converse is genuine too: source-only square grammar
constructs the formerly primitive TARGET square on the same
physical five-stage pentagonator and 5D unit-change boundaries. -/
theorem nativeK5Pentagonator_sourceOnlyFillsTargetSquare :
    Nonempty (NativeK5SquarePolicySixCell false true p
      (NativeK5StructuralFiveCell.targetSquareLeftThenRight
        (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
        (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)))
      (NativeK5StructuralFiveCell.targetSquareRightThenLeft
        (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
        (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)))) :=
  ⟨nativeK5SourceOnly_generatesTargetSquare
    (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
    (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))⟩

/-- Explicitly contrast SINGLE-family sufficiency with
NO-family impossibility on the actual dependent K5 pentagonator.
The exclusion is proved by P94D3AB's noncommutative S₃ observer,
not asserted by an added axiom. -/
theorem nativeK5Pentagonator_oneSquareFamilyMinimal :
    Nonempty (NativeK5SquarePolicySixCell true false p
      (NativeK5StructuralFiveCell.sourceSquareLeftThenRight
        (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
        (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)))
      (NativeK5StructuralFiveCell.sourceSquareRightThenLeft
        (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
        (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)))) ∧
    Nonempty (NativeK5SquarePolicySixCell false true p
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
        (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)))) ∧
    ¬ Nonempty (NativeK5PreSquareSixCell p
      (NativeK5StructuralFiveCell.sourceSquareLeftThenRight
        (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
        (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)))
      (NativeK5StructuralFiveCell.sourceSquareRightThenLeft
        (.verticalLeftUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
        (.verticalRightUnit (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)))) := by
  exact ⟨nativeK5Pentagonator_targetOnlyFillsSourceSquare t1 t2 t3 t4 t5,
    nativeK5Pentagonator_sourceOnlyFillsTargetSquare t1 t2 t3 t4 t5,
    (nativeK5Pentagonator_targetSquareIndependence t1 t2 t3 t4 t5).2,
    (nativeK5Pentagonator_sourceSquareIndependence t1 t2 t3 t4 t5).2⟩

#print axioms nativeK5Pentagonator_targetOnlyFillsSourceSquare
#print axioms nativeK5Pentagonator_sourceOnlyFillsTargetSquare
#print axioms nativeK5Pentagonator_oneSquareFamilyMinimal

end GenuineFiveStage
end
end Kuu.F112.Physical
