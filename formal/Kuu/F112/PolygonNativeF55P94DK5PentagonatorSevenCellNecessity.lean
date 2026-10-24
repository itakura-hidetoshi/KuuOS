import Kuu.F112.PolygonNativeF55P94DK5SevenCellSixGroupoid
import Mathlib.Tactic

/-!
# F112-P94D3AD — physical C60 five-stage K5 seven-cell necessity

Specialize the independent genuine 7D square comparison generators
to the ACTUAL five F45 stages of the C60 K5 nine-face 3D
reoriented cycle and INDEPENDENT Type-valued 4D pentagonator.

The two input 5D unit changes are actual free five-cell proofs
applied to that genuine pentagonator, not formal graph words.

Both pairs of SIX-cell fillers have:
  * identical dependent five-cell endpoints;
  * different signed target/source six-cell provenance;
  * NO conservative SEVEN-cell proof;
  * an ACTUAL seven-cell in the independently extended grammar;
  * equal coarse total six-cell square-generator provenance.
These are relative source-typed higher proofs, not descent to the
old P92B, full 7D pasting uniqueness, global strict 3/n, or
(∞,3)-hyperdescent.
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

/-- Actual pentagonator: primitive horizontal target square. -/
def nativeK5PentagonatorSevenTargetDirect :=
  nativeK5SixTargetSquareDirect
    (NativeK5StructuralFiveCell.verticalLeftUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
    (NativeK5StructuralFiveCell.verticalRightUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))

/-- Same dependent 5D target-square boundary, but the 6D proof
comes from the SOURCE square and the two naturality cubes. -/
def nativeK5PentagonatorSevenTargetViaSource :=
  nativeK5SixTargetSquareViaSource
    (NativeK5StructuralFiveCell.verticalLeftUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
    (NativeK5StructuralFiveCell.verticalRightUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))

/-- Actual pentagonator: primitive horizontal source square. -/
def nativeK5PentagonatorSevenSourceDirect :=
  nativeK5SixSourceSquareDirect
    (NativeK5StructuralFiveCell.verticalLeftUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
    (NativeK5StructuralFiveCell.verticalRightUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))

/-- Same dependent 5D source-square boundary; this witness is
derived instead from the TARGET 6D square generator. -/
def nativeK5PentagonatorSevenSourceViaTarget :=
  nativeK5SixSourceSquareViaTarget
    (NativeK5StructuralFiveCell.verticalLeftUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
    (NativeK5StructuralFiveCell.verticalRightUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))

/-- Genuine physical K5 comparison necessity on TARGET 6D
square witnesses, with full source-typed 7D witness existence. -/
theorem nativeK5Pentagonator_targetSevenCellIndependence :
    Nonempty (NativeK5StructuralSevenCell p
      (nativeK5PentagonatorSevenTargetDirect t1 t2 t3 t4 t5)
      (nativeK5PentagonatorSevenTargetViaSource t1 t2 t3 t4 t5)) ∧
    ¬ Nonempty (NativeK5CoreSevenCell p
      (nativeK5PentagonatorSevenTargetDirect t1 t2 t3 t4 t5)
      (nativeK5PentagonatorSevenTargetViaSource t1 t2 t3 t4 t5)) :=
  nativeK5TargetComparison_newSevenGeneratorEssential
    (NativeK5StructuralFiveCell.verticalLeftUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
    (NativeK5StructuralFiveCell.verticalRightUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))

/-- The complementary SOURCE 7D comparison on the same genuine
K5 pentagonator cannot be derived by any core 7D constructor. -/
theorem nativeK5Pentagonator_sourceSevenCellIndependence :
    Nonempty (NativeK5StructuralSevenCell p
      (nativeK5PentagonatorSevenSourceDirect t1 t2 t3 t4 t5)
      (nativeK5PentagonatorSevenSourceViaTarget t1 t2 t3 t4 t5)) ∧
    ¬ Nonempty (NativeK5CoreSevenCell p
      (nativeK5PentagonatorSevenSourceDirect t1 t2 t3 t4 t5)
      (nativeK5PentagonatorSevenSourceViaTarget t1 t2 t3 t4 t5)) :=
  nativeK5SourceComparison_newSevenGeneratorEssential
    (NativeK5StructuralFiveCell.verticalLeftUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
    (NativeK5StructuralFiveCell.verticalRightUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))

/-- Even the genuine C60 K5 physical pentagonator changes only
the FINE 6D square provenance: each pair has total charge 1.
This total does NOT imply a 7D core witness exists. -/
theorem nativeK5Pentagonator_targetSevenTotalCharge :
    (nativeK5PentagonatorSevenTargetDirect t1 t2 t3 t4 t5).totalSquareProvenance = 1 ∧
    (nativeK5PentagonatorSevenTargetViaSource t1 t2 t3 t4 t5).totalSquareProvenance = 1 := by
  exact ⟨rfl, rfl⟩

/-- The original SOURCE-square witness pair has the SAME total
signed 6D provenance 1 despite distinct actual 6D constructor
histories, with independent 7D comparison required. -/
theorem nativeK5Pentagonator_sourceSevenTotalCharge :
    (nativeK5PentagonatorSevenSourceDirect t1 t2 t3 t4 t5).totalSquareProvenance = 1 ∧
    (nativeK5PentagonatorSevenSourceViaTarget t1 t2 t3 t4 t5).totalSquareProvenance = 1 := by
  exact ⟨rfl, rfl⟩

/-- If the NEW full 7D comparison were forced to descend
BOUNDARY-PRESERVING into the explicit conservative 7D core,
it would contradict the actual C60 K5 fine-provenance obstruction.
No assertion is made about unconstructed old P92B 7D carriers. -/
theorem nativeK5Pentagonator_targetCoreSevenNoRetraction :
    ¬ (NativeK5StructuralSevenCell p
      (nativeK5PentagonatorSevenTargetDirect t1 t2 t3 t4 t5)
      (nativeK5PentagonatorSevenTargetViaSource t1 t2 t3 t4 t5) →
      NativeK5CoreSevenCell p
        (nativeK5PentagonatorSevenTargetDirect t1 t2 t3 t4 t5)
        (nativeK5PentagonatorSevenTargetViaSource t1 t2 t3 t4 t5)) := by
  intro transport
  obtain ⟨⟨seven⟩, noCore⟩ :=
    nativeK5Pentagonator_targetSevenCellIndependence t1 t2 t3 t4 t5
  exact noCore ⟨transport seven⟩

#print axioms nativeK5PentagonatorSevenTargetDirect
#print axioms nativeK5PentagonatorSevenTargetViaSource
#print axioms nativeK5PentagonatorSevenSourceDirect
#print axioms nativeK5PentagonatorSevenSourceViaTarget
#print axioms nativeK5Pentagonator_targetSevenCellIndependence
#print axioms nativeK5Pentagonator_sourceSevenCellIndependence
#print axioms nativeK5Pentagonator_targetSevenTotalCharge
#print axioms nativeK5Pentagonator_sourceSevenTotalCharge
#print axioms nativeK5Pentagonator_targetCoreSevenNoRetraction

end GenuineFiveStage
end
end Kuu.F112.Physical
