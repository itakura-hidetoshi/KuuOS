import KUOS.Architecture.QiWuxingGK5CHP77PrimitiveUnitPayloadFaithfulnessV5_97

/-!
Qi v5.98 — reversed one-unit sources with genuine nonassociative
unit-free strict/reverse/chain contexts.

An ACTUAL original primitive unit source M : SelectedLocalEighteen J N
is joined on the left or right to a genuine unit-free old18D
endomorphism. The unit-free endomorphism is obtained from the already
certified v5.88 grammar: arbitrary nonassociative strict, reversed,
and joined nodes, not merely the linear strict padding of v5.94.
The entire genuine raw old18D composite is then reversed, preserving
the original dependent indices N -> J.

The v5.73 nonassociative original inner bracket records where the
unit-free tree was placed and its complete shape. The v5.92 full
original dependent Sigma unit history retains the original primitive
unit source as an ACTUAL payload, not an untyped side label.

On either SAME-ORIENTATION reversed-context family, equality of the
JOINT bracket and full typed history is equivalent to equality of
both the unit-free context tree and the actual primitive unit source.
These are genuine raw-equality reflection theorems in one fixed
raw17D J,N fiber. Mixed left/right contexts have DIFFERENT brackets
and genuine raw values even when their full typed histories agree.

This is a local, single-primitive-unit-fragment theorem. It does not
claim arbitrary original one-unit old18D source reconstruction,
same-bracket source collision existence or impossibility, global old/new
selected19 quotients, cross-fiber descent, or WORLD/20D authority.
The unresolved original v5.93 existence stays NO_DATA.

No original dependent Type definitions, five/seven comparison relations,
Lean/mathlib pins, root107, or protected PR #1558 are changed.
append-only / tighten-only / overwrite-forbidden / same-root.
-/

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uSix

namespace KUOS.Architecture.WuxingPentagonUnified
namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell

variable {W : Type uSix}

section GenuineReversedUnitFreeContext

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable (J N : SelectedContextualSeventeen W l r H K)

/-- Every actual old18D proof embedded from the full v5.88
unit-free nonassociative grammar has an empty ORIGINAL v5.92
dependent unit payload history, even with nested reverse/chain. -/
theorem selectedV598UnitFree_historyNil
    (S : SelectedContextualSeventeen W l r H K)
    (t : SelectedV588UnitFreeTerm) :
    selectedV592OriginalUnitHistory l r
      (selectedV588UnitFreeRawEmbed l r S t) = [] := by
  induction t with
  | strict => rfl
  | reversed t ih =>
      simpa only [selectedV588UnitFreeRawEmbed,
        selectedV592OriginalUnitHistory] using ih
  | joined t u ihT ihU =>
      simp only [selectedV588UnitFreeRawEmbed,
        selectedV592OriginalUnitHistory, ihT, ihU, List.nil_append]

/-- Actual original N -> J raw proof, with an arbitrary original
unit-free J -> J source on the LEFT of the original unit proof. -/
def selectedV598ReverseLeftContext
    (t : SelectedV588UnitFreeTerm)
    (M : SelectedLocalEighteen W l r J N) :
    SelectedLocalEighteen W l r N J :=
  .reverse (.chain (selectedV588UnitFreeRawEmbed l r J t) M)

/-- Actual original N -> J raw proof, with an arbitrary original
unit-free N -> N source on the RIGHT of the original unit proof. -/
def selectedV598ReverseRightContext
    (t : SelectedV588UnitFreeTerm)
    (M : SelectedLocalEighteen W l r J N) :
    SelectedLocalEighteen W l r N J :=
  .reverse (.chain M (selectedV588UnitFreeRawEmbed l r N t))

/-- Existing v5.73 bracket observation records the entire left
unit-free context, its nonassociative brackets, AND the outer reverse. -/
theorem selectedV598ReverseLeft_bracket
    (t : SelectedV588UnitFreeTerm)
    (M : SelectedLocalEighteen W l r J N) :
    selectedLocalEighteenInnerBracket l r
      (selectedV598ReverseLeftContext l r J N t M) =
        .oldReversed (.oldJoined
          (selectedV588UnitFreeBracket t)
          (selectedLocalEighteenInnerBracket l r M)) := by
  change SelectedInheritedOldInnerBracket.oldReversed
      (.oldJoined
        (selectedLocalEighteenInnerBracket l r
          (selectedV588UnitFreeRawEmbed l r J t))
        (selectedLocalEighteenInnerBracket l r M)) =
      .oldReversed (.oldJoined
        (selectedV588UnitFreeBracket t)
        (selectedLocalEighteenInnerBracket l r M))
  rw [selectedV588UnitFreeRaw_observed l r J t]

theorem selectedV598ReverseRight_bracket
    (t : SelectedV588UnitFreeTerm)
    (M : SelectedLocalEighteen W l r J N) :
    selectedLocalEighteenInnerBracket l r
      (selectedV598ReverseRightContext l r J N t M) =
        .oldReversed (.oldJoined
          (selectedLocalEighteenInnerBracket l r M)
          (selectedV588UnitFreeBracket t)) := by
  change SelectedInheritedOldInnerBracket.oldReversed
      (.oldJoined
        (selectedLocalEighteenInnerBracket l r M)
        (selectedLocalEighteenInnerBracket l r
          (selectedV588UnitFreeRawEmbed l r N t))) =
      .oldReversed (.oldJoined
        (selectedLocalEighteenInnerBracket l r M)
        (selectedV588UnitFreeBracket t))
  rw [selectedV588UnitFreeRaw_observed l r N t]

/-- Arbitrary nested strict/reverse/chain context does NOT change
the complete original v5.92 Sigma payload history on the left. -/
theorem selectedV598ReverseLeft_history
    (t : SelectedV588UnitFreeTerm)
    (M : SelectedLocalEighteen W l r J N) :
    selectedV592OriginalUnitHistory l r
      (selectedV598ReverseLeftContext l r J N t M) =
        selectedV592OriginalUnitHistory l r M := by
  change selectedV592OriginalUnitHistory l r
      (selectedV588UnitFreeRawEmbed l r J t) ++
        selectedV592OriginalUnitHistory l r M =
      selectedV592OriginalUnitHistory l r M
  rw [selectedV598UnitFree_historyNil l r J t]
  rfl

theorem selectedV598ReverseRight_history
    (t : SelectedV588UnitFreeTerm)
    (M : SelectedLocalEighteen W l r J N) :
    selectedV592OriginalUnitHistory l r
      (selectedV598ReverseRightContext l r J N t M) =
        selectedV592OriginalUnitHistory l r M := by
  change selectedV592OriginalUnitHistory l r M ++
      selectedV592OriginalUnitHistory l r
        (selectedV588UnitFreeRawEmbed l r N t) =
      selectedV592OriginalUnitHistory l r M
  rw [selectedV598UnitFree_historyNil l r N t]
  simp only [List.append_nil]

/-- The constructions have exactly ONE genuine original unit
for every original primitive leaf, regardless of context complexity. -/
theorem selectedV598ReverseLeft_oneUnit
    (t : SelectedV588UnitFreeTerm)
    (M : SelectedLocalEighteen W l r J N)
    (hM : selectedV597OriginalPrimitiveUnit l r M) :
    selectedV589OriginalUnitCount l r
      (selectedV598ReverseLeftContext l r J N t M) = 1 := by
  calc
    selectedV589OriginalUnitCount l r
        (selectedV598ReverseLeftContext l r J N t M) =
      (selectedV592OriginalUnitHistory l r
        (selectedV598ReverseLeftContext l r J N t M)).length :=
      (selectedV592OriginalUnitHistory_length l r
        (selectedV598ReverseLeftContext l r J N t M)).symm
    _ = (selectedV592OriginalUnitHistory l r M).length :=
      congrArg List.length (selectedV598ReverseLeft_history l r J N t M)
    _ = selectedV589OriginalUnitCount l r M :=
      selectedV592OriginalUnitHistory_length l r M
    _ = 1 := selectedV597Primitive_unitCountOne l r J N M hM

theorem selectedV598ReverseRight_oneUnit
    (t : SelectedV588UnitFreeTerm)
    (M : SelectedLocalEighteen W l r J N)
    (hM : selectedV597OriginalPrimitiveUnit l r M) :
    selectedV589OriginalUnitCount l r
      (selectedV598ReverseRightContext l r J N t M) = 1 := by
  calc
    selectedV589OriginalUnitCount l r
        (selectedV598ReverseRightContext l r J N t M) =
      (selectedV592OriginalUnitHistory l r
        (selectedV598ReverseRightContext l r J N t M)).length :=
      (selectedV592OriginalUnitHistory_length l r
        (selectedV598ReverseRightContext l r J N t M)).symm
    _ = (selectedV592OriginalUnitHistory l r M).length :=
      congrArg List.length (selectedV598ReverseRight_history l r J N t M)
    _ = selectedV589OriginalUnitCount l r M :=
      selectedV592OriginalUnitHistory_length l r M
    _ = 1 := selectedV597Primitive_unitCountOne l r J N M hM

/-- Local exact reconstruction: for genuine reversed LEFT contexts,
joint equality of the original inner bracket and full dependent unit
payload history is equivalent to equality of the ENTIRE unit-free
context tree AND equality of the genuine original primitive source.
No quotient or cross-fiber proof transport is used. -/
theorem selectedV598ReverseLeft_jointEq_iff
    (M L : SelectedLocalEighteen W l r J N)
    (hM : selectedV597OriginalPrimitiveUnit l r M)
    (hL : selectedV597OriginalPrimitiveUnit l r L)
    (t u : SelectedV588UnitFreeTerm) :
    ((selectedLocalEighteenInnerBracket l r
        (selectedV598ReverseLeftContext l r J N t M) =
      selectedLocalEighteenInnerBracket l r
        (selectedV598ReverseLeftContext l r J N u L)) ∧
     (selectedV592OriginalUnitHistory l r
        (selectedV598ReverseLeftContext l r J N t M) =
      selectedV592OriginalUnitHistory l r
        (selectedV598ReverseLeftContext l r J N u L))) ↔
      (t = u ∧ M = L) := by
  constructor
  · rintro ⟨hb, hh⟩
    have htreeBracket :
        selectedV588UnitFreeBracket t =
          selectedV588UnitFreeBracket u := by
      rw [selectedV598ReverseLeft_bracket l r J N t M,
        selectedV598ReverseLeft_bracket l r J N u L] at hb
      injection hb with hj
      injection hj with ht hunitBracket
      exact ht
    have hhistory :
        selectedV592OriginalUnitHistory l r M =
          selectedV592OriginalUnitHistory l r L := by
      rwa [selectedV598ReverseLeft_history l r J N t M,
        selectedV598ReverseLeft_history l r J N u L] at hh
    exact ⟨selectedV588UnitFreeBracket_injective htreeBracket,
      (selectedV597Primitive_historyEq_iff_rawEq
        l r J N M L hM hL).mp hhistory⟩
  · rintro ⟨rfl, rfl⟩
    exact ⟨rfl, rfl⟩

theorem selectedV598ReverseRight_jointEq_iff
    (M L : SelectedLocalEighteen W l r J N)
    (hM : selectedV597OriginalPrimitiveUnit l r M)
    (hL : selectedV597OriginalPrimitiveUnit l r L)
    (t u : SelectedV588UnitFreeTerm) :
    ((selectedLocalEighteenInnerBracket l r
        (selectedV598ReverseRightContext l r J N t M) =
      selectedLocalEighteenInnerBracket l r
        (selectedV598ReverseRightContext l r J N u L)) ∧
     (selectedV592OriginalUnitHistory l r
        (selectedV598ReverseRightContext l r J N t M) =
      selectedV592OriginalUnitHistory l r
        (selectedV598ReverseRightContext l r J N u L))) ↔
      (t = u ∧ M = L) := by
  constructor
  · rintro ⟨hb, hh⟩
    have htreeBracket :
        selectedV588UnitFreeBracket t =
          selectedV588UnitFreeBracket u := by
      rw [selectedV598ReverseRight_bracket l r J N t M,
        selectedV598ReverseRight_bracket l r J N u L] at hb
      injection hb with hj
      injection hj with hunitBracket ht
      exact ht
    have hhistory :
        selectedV592OriginalUnitHistory l r M =
          selectedV592OriginalUnitHistory l r L := by
      rwa [selectedV598ReverseRight_history l r J N t M,
        selectedV598ReverseRight_history l r J N u L] at hh
    exact ⟨selectedV588UnitFreeBracket_injective htreeBracket,
      (selectedV597Primitive_historyEq_iff_rawEq
        l r J N M L hM hL).mp hhistory⟩
  · rintro ⟨rfl, rfl⟩
    exact ⟨rfl, rfl⟩

/-- FULL original raw equality, not mere equality of observation
proxies or of a 19D quotient. -/
theorem selectedV598ReverseLeft_rawEq_iff
    (M L : SelectedLocalEighteen W l r J N)
    (hM : selectedV597OriginalPrimitiveUnit l r M)
    (hL : selectedV597OriginalPrimitiveUnit l r L)
    (t u : SelectedV588UnitFreeTerm) :
    (selectedV598ReverseLeftContext l r J N t M =
      selectedV598ReverseLeftContext l r J N u L) ↔
        (t = u ∧ M = L) := by
  constructor
  · intro hraw
    apply (selectedV598ReverseLeft_jointEq_iff
      l r J N M L hM hL t u).mp
    exact ⟨congrArg (selectedLocalEighteenInnerBracket l r) hraw,
      congrArg (selectedV592OriginalUnitHistory l r) hraw⟩
  · rintro ⟨rfl, rfl⟩
    rfl

theorem selectedV598ReverseRight_rawEq_iff
    (M L : SelectedLocalEighteen W l r J N)
    (hM : selectedV597OriginalPrimitiveUnit l r M)
    (hL : selectedV597OriginalPrimitiveUnit l r L)
    (t u : SelectedV588UnitFreeTerm) :
    (selectedV598ReverseRightContext l r J N t M =
      selectedV598ReverseRightContext l r J N u L) ↔
        (t = u ∧ M = L) := by
  constructor
  · intro hraw
    apply (selectedV598ReverseRight_jointEq_iff
      l r J N M L hM hL t u).mp
    exact ⟨congrArg (selectedLocalEighteenInnerBracket l r) hraw,
      congrArg (selectedV592OriginalUnitHistory l r) hraw⟩
  · rintro ⟨rfl, rfl⟩
    rfl

/-- Unlike the common-orientation reconstructions, an original
unit-free context on the LEFT cannot have the same genuine
nonassociative bracket as any original unit-free context on the
RIGHT of a primitive unit leaf: zero unit leaves versus one. -/
theorem selectedV598Mixed_bracketNe
    (M L : SelectedLocalEighteen W l r J N)
    (hL : selectedV597OriginalPrimitiveUnit l r L)
    (t u : SelectedV588UnitFreeTerm) :
    selectedLocalEighteenInnerBracket l r
        (selectedV598ReverseLeftContext l r J N t M) ≠
      selectedLocalEighteenInnerBracket l r
        (selectedV598ReverseRightContext l r J N u L) := by
  intro hb
  rw [selectedV598ReverseLeft_bracket l r J N t M,
    selectedV598ReverseRight_bracket l r J N u L] at hb
  injection hb with hj
  injection hj with hleft hright
  have hzero :
      selectedV588InnerUnitCount (selectedV588UnitFreeBracket t) = 0 :=
    selectedV588UnitFree_hasZeroUnits t
  have hone :
      selectedV588InnerUnitCount
        (selectedLocalEighteenInnerBracket l r L) = 1 := by
    rcases hL with h | h
    · rw [h]
      rfl
    · rw [h]
      rfl
  have hc := congrArg selectedV588InnerUnitCount hleft
  rw [hzero, hone] at hc
  exact Nat.zero_ne_one hc

theorem selectedV598Mixed_rawNe
    (M L : SelectedLocalEighteen W l r J N)
    (hL : selectedV597OriginalPrimitiveUnit l r L)
    (t u : SelectedV588UnitFreeTerm) :
    selectedV598ReverseLeftContext l r J N t M ≠
      selectedV598ReverseRightContext l r J N u L := by
  intro hraw
  exact (selectedV598Mixed_bracketNe l r J N M L hL t u)
    (congrArg (selectedLocalEighteenInnerBracket l r) hraw)

/-- In the cross-orientation case, full typed unit-history equality
still reconstructs only the ORIGINAL primitive payload, not the
different outer raw tree shapes. -/
theorem selectedV598Mixed_historyEq_iff_sourceEq
    (M L : SelectedLocalEighteen W l r J N)
    (hM : selectedV597OriginalPrimitiveUnit l r M)
    (hL : selectedV597OriginalPrimitiveUnit l r L)
    (t u : SelectedV588UnitFreeTerm) :
    (selectedV592OriginalUnitHistory l r
        (selectedV598ReverseLeftContext l r J N t M) =
      selectedV592OriginalUnitHistory l r
        (selectedV598ReverseRightContext l r J N u L)) ↔
      M = L := by
  rw [selectedV598ReverseLeft_history l r J N t M,
    selectedV598ReverseRight_history l r J N u L]
  exact selectedV597Primitive_historyEq_iff_rawEq
    l r J N M L hM hL

/-- Exact conditional gap for the genuine 1-unit reversed raw
proofs. No claim is made that a primitive unit source exists in
an arbitrary uninhabited fiber. -/
theorem selectedV598Mixed_samePrimitive_historyGap
    (M : SelectedLocalEighteen W l r J N)
    (hM : selectedV597OriginalPrimitiveUnit l r M)
    (t u : SelectedV588UnitFreeTerm) :
    (selectedV592OriginalUnitHistory l r
        (selectedV598ReverseLeftContext l r J N t M) =
      selectedV592OriginalUnitHistory l r
        (selectedV598ReverseRightContext l r J N u M)) ∧
    (selectedLocalEighteenInnerBracket l r
        (selectedV598ReverseLeftContext l r J N t M) ≠
      selectedLocalEighteenInnerBracket l r
        (selectedV598ReverseRightContext l r J N u M)) ∧
    (selectedV598ReverseLeftContext l r J N t M ≠
      selectedV598ReverseRightContext l r J N u M) := by
  exact ⟨(selectedV598Mixed_historyEq_iff_sourceEq
      l r J N M M hM hM t u).mpr rfl,
    selectedV598Mixed_bracketNe l r J N M M hM t u,
    selectedV598Mixed_rawNe l r J N M M hM t u⟩

end GenuineReversedUnitFreeContext

#print axioms PentagonAdjoinedSixCell.selectedV598UnitFree_historyNil
#print axioms PentagonAdjoinedSixCell.selectedV598ReverseLeftContext
#print axioms PentagonAdjoinedSixCell.selectedV598ReverseRightContext
#print axioms PentagonAdjoinedSixCell.selectedV598ReverseLeft_bracket
#print axioms PentagonAdjoinedSixCell.selectedV598ReverseRight_bracket
#print axioms PentagonAdjoinedSixCell.selectedV598ReverseLeft_history
#print axioms PentagonAdjoinedSixCell.selectedV598ReverseRight_history
#print axioms PentagonAdjoinedSixCell.selectedV598ReverseLeft_oneUnit
#print axioms PentagonAdjoinedSixCell.selectedV598ReverseRight_oneUnit
#print axioms PentagonAdjoinedSixCell.selectedV598ReverseLeft_jointEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV598ReverseRight_jointEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV598ReverseLeft_rawEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV598ReverseRight_rawEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV598Mixed_bracketNe
#print axioms PentagonAdjoinedSixCell.selectedV598Mixed_rawNe
#print axioms PentagonAdjoinedSixCell.selectedV598Mixed_historyEq_iff_sourceEq
#print axioms PentagonAdjoinedSixCell.selectedV598Mixed_samePrimitive_historyGap

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
