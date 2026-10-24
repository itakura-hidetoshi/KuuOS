import Kuu.F112.PolygonNativeF55P94DK5PreNaturalitySixCellObstruction
import Mathlib.Tactic

/-!
# F112-P94D3AA — PHYSICAL five-stage K5 pentagonator higher obstruction

Specialize the generic six-dimensional left/right naturality
independence theorem to the ACTUALLY CONSTRUCTED C60 five-stage
F45 global K5 reoriented nine-face Type-valued 3-cell and
independent pentagonator Type-valued 4-cell.

Both concrete 6D interchanger naturality boundaries:
- possess an ACTUAL Type-valued 6-cell in the NEW P94D3Z syntax;
- possess NO Type-valued 6-cell generated solely by the conservative
  pre-naturality core (even after units, inverses, associativity,
  vertical 6-cell composition and all original typed 3-whiskerings).

This is an exact source witness, not a formal K5 graph word, a
generic Peiffer equality, or a theorem of old P92B.
Gray/non-genuine relations are not introduced.
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

/-- A genuinely typed K5 4-cell pentagonator follows the left
unit reduction of its ACTUAL nine-face 3-cell source.
A full new 6-cell exists; a conservative 6D-core proof does not.
This obstruction is independent of the old mod-three and Peiffer
observations, which survive unchanged. -/
theorem nativeK5Pentagonator_leftSixCellIndependence :
    Nonempty (NativeK5StructuralSixCell p
      (NativeK5StructuralFiveCell.interchangerLeftPathTarget
        (nativeK5UnitFiveReduction
          (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5))
        (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
      (NativeK5StructuralFiveCell.interchangerLeftPathSource
        (nativeK5UnitFiveReduction
          (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5))
        (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))) ∧
    ¬ Nonempty (NativeK5PrenaturalitySixCell p
      (NativeK5StructuralFiveCell.interchangerLeftPathTarget
        (nativeK5UnitFiveReduction
          (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5))
        (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
      (NativeK5StructuralFiveCell.interchangerLeftPathSource
        (nativeK5UnitFiveReduction
          (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5))
        (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))) :=
  nativeK5LeftNaturality_newGeneratorEssential
    (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5)
    (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)

/-- The SAME genuinely typed pentagonator participates in the
RIGHT naturality obstruction: its following 3-cell is the
authentic structural identity at the global K5 F54 base route. -/
theorem nativeK5Pentagonator_rightSixCellIndependence :
    Nonempty (NativeK5StructuralSixCell p
      (NativeK5StructuralFiveCell.interchangerRightPathTarget
        (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)
        (nativeK5UnitFiveReduction
          (nativeK5ReorientedStructuralIdentity t1 t2 t3 t4 t5)))
      (NativeK5StructuralFiveCell.interchangerRightPathSource
        (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)
        (nativeK5UnitFiveReduction
          (nativeK5ReorientedStructuralIdentity t1 t2 t3 t4 t5)))) ∧
    ¬ Nonempty (NativeK5PrenaturalitySixCell p
      (NativeK5StructuralFiveCell.interchangerRightPathTarget
        (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)
        (nativeK5UnitFiveReduction
          (nativeK5ReorientedStructuralIdentity t1 t2 t3 t4 t5)))
      (NativeK5StructuralFiveCell.interchangerRightPathSource
        (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)
        (nativeK5UnitFiveReduction
          (nativeK5ReorientedStructuralIdentity t1 t2 t3 t4 t5)))) :=
  nativeK5RightNaturality_newGeneratorEssential
    (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)
    (nativeK5ReorientedStructuralIdentity t1 t2 t3 t4 t5)

/-- The refined source-shape charge of these genuine nine-face
K5 left 5-cell naturality paths is 0 vs 1. This is the concrete
computable obstruction behind the preceding source proof. -/
theorem nativeK5Pentagonator_leftShapeCharge :
    (NativeK5StructuralFiveCell.interchangerLeftPathTarget
        (nativeK5UnitFiveReduction
          (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5))
        (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)).shapeCharge true = 0 ∧
    (NativeK5StructuralFiveCell.interchangerLeftPathSource
        (nativeK5UnitFiveReduction
          (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5))
        (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)).shapeCharge true = 1 :=
  nativeK5LeftNaturality_shapeCounts
    (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5)
    (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)

#print axioms nativeK5Pentagonator_leftSixCellIndependence
#print axioms nativeK5Pentagonator_rightSixCellIndependence
#print axioms nativeK5Pentagonator_leftShapeCharge

end GenuineFiveStage
end
end Kuu.F112.Physical
