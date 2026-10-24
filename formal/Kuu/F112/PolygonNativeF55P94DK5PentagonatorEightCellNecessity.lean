import Kuu.F112.PolygonNativeF55P94DK5TypedEightCellInterchange
import Mathlib.Tactic

/-!
# F112-P94D3AE — actual C60 five-stage K₅ typed eight-cell obstruction

Apply genuine higher source-typed eight-cell syntax to the REAL five
F45 stages, the previously formalized independent Type-valued K₅
pentagonator, and its two genuine unit-change five-cell witnesses.

The independent target seven-cell comparison generates TWO different
7D pasting histories between the EXACT same dependent six-cell
boundaries. These histories have the same ADDITIVE seven-cell charge,
yet are different in the S₃-valued observer.

Consequently they have no conservative 8D filler in the stated core,
while an independent Type-valued squareExchange 8-cell fills them.
This proves a relative necessity only; no claim of old P92B
descent, all-pasting coherence, or global strict 3/n is made.
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

/-- ACTUAL primitive 7-cell comparing alternative six-cell proofs
on the genuine five-stage C60 K₅ pentagonator. No graph-word
shortcut: each input is an existing Type-valued five-cell term. -/
def nativeK5PentagonatorEightTargetSeven :
    NativeK5StructuralSevenCell p
      (nativeK5PentagonatorSevenTargetDirect t1 t2 t3 t4 t5)
      (nativeK5PentagonatorSevenTargetViaSource t1 t2 t3 t4 t5) :=
  .targetComparison
    (NativeK5StructuralFiveCell.verticalLeftUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
    (NativeK5StructuralFiveCell.verticalRightUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))

/-- At the genuine pentagonator the two pasting histories have
exactly the SAME abelian integer comparison charge. -/
theorem nativeK5PentagonatorEight_abelianBlind :
    (nativeK5SevenPastingLeftThenRight
      (nativeK5PentagonatorEightTargetSeven t1 t2 t3 t4 t5)).comparisonCharge =
    (nativeK5SevenPastingRightThenLeft
      (nativeK5PentagonatorEightTargetSeven t1 t2 t3 t4 t5)).comparisonCharge :=
  nativeK5SevenPasting_abelianBlind _

/-- The same two authentic pentagonator pastings are nonetheless
distinguished by S₃ history: failure of an integer-only observer. -/
theorem nativeK5PentagonatorEight_history_ne :
    (nativeK5SevenPastingLeftThenRight
      (nativeK5PentagonatorEightTargetSeven t1 t2 t3 t4 t5)).historyGroup ≠
    (nativeK5SevenPastingRightThenLeft
      (nativeK5PentagonatorEightTargetSeven t1 t2 t3 t4 t5)).historyGroup :=
  nativeK5TargetSevenPasting_history_ne
    (NativeK5StructuralFiveCell.verticalLeftUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
    (NativeK5StructuralFiveCell.verticalRightUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))

/-- Physical C60 K₅ specialization of the independent genuine 8D
square-exchange comparison and its conservative-history obstruction. -/
theorem nativeK5PentagonatorEight_relativeNecessity :
    Nonempty (NativeK5StructuralEightCell p
      (nativeK5SevenPastingLeftThenRight
        (nativeK5PentagonatorEightTargetSeven t1 t2 t3 t4 t5))
      (nativeK5SevenPastingRightThenLeft
        (nativeK5PentagonatorEightTargetSeven t1 t2 t3 t4 t5))) ∧
    ¬ Nonempty (NativeK5CoreEightCell p
      (nativeK5SevenPastingLeftThenRight
        (nativeK5PentagonatorEightTargetSeven t1 t2 t3 t4 t5))
      (nativeK5SevenPastingRightThenLeft
        (nativeK5PentagonatorEightTargetSeven t1 t2 t3 t4 t5))) :=
  nativeK5TargetEightSquare_relativeNecessity
    (NativeK5StructuralFiveCell.verticalLeftUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
    (NativeK5StructuralFiveCell.verticalRightUnit
      (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))

/-- A boundary-preserving retraction from the new genuine physical
8D comparison to the specified conservative 8D grammar cannot
exist. This is NOT yet a retraction obstruction into P92B. -/
theorem nativeK5PentagonatorEight_coreNoRetraction :
    ¬ Nonempty
      (NativeK5StructuralEightCell p
        (nativeK5SevenPastingLeftThenRight
          (nativeK5PentagonatorEightTargetSeven t1 t2 t3 t4 t5))
        (nativeK5SevenPastingRightThenLeft
          (nativeK5PentagonatorEightTargetSeven t1 t2 t3 t4 t5)) →
       NativeK5CoreEightCell p
        (nativeK5SevenPastingLeftThenRight
          (nativeK5PentagonatorEightTargetSeven t1 t2 t3 t4 t5))
        (nativeK5SevenPastingRightThenLeft
          (nativeK5PentagonatorEightTargetSeven t1 t2 t3 t4 t5))) := by
  rintro ⟨retract⟩
  obtain ⟨⟨exchange⟩, noCore⟩ :=
    nativeK5PentagonatorEight_relativeNecessity t1 t2 t3 t4 t5
  exact noCore ⟨retract exchange⟩

#print axioms nativeK5PentagonatorEightTargetSeven
#print axioms nativeK5PentagonatorEight_abelianBlind
#print axioms nativeK5PentagonatorEight_history_ne
#print axioms nativeK5PentagonatorEight_relativeNecessity
#print axioms nativeK5PentagonatorEight_coreNoRetraction

end GenuineFiveStage
end
end Kuu.F112.Physical
