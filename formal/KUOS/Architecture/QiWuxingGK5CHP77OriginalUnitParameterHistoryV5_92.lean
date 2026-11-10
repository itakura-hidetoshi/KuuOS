import KUOS.Architecture.QiWuxingGK5CHP77SingleUnitLoopThresholdV5_91

/-!
Qi v5.92 — ORIGINAL dependent old18D unit-parameter payload history.

This module does not change the genuine old18D proof type, the old five
or new seven selected19 comparison relations, or any existing definition.
It observes genuine unitLeft/unitRight source atoms in the original
dependent Type (including their original before/frame/comparison/after
parameters and their exact raw17D source/target indices), rather than
replacing them with an untyped left/right tag.

The payload history is deliberately distinct from the v5.73 ordered,
nonassociative internal bracket observation:
* reverse and chain preserve/concatenate the ordered original unit
  payloads;
* the forward/backward two-unit roundtrips contain the SAME ordered
  original unit payloads, while their brackets have opposite ordering
  and their genuine outer raw17D endpoint fibers are distinct;
* even INSIDE ONE actual raw17D loop fiber, inserting a genuine
  strict before versus after the same two-unit roundtrip preserves
  the full ordered unit payload history but changes its old18D
  nonassociative bracket. The two raw old18D proofs are distinct.

This is a certified HISTORY non-faithfulness witness, NOT a
same-fiber INNER-BRACKET fingerprint collision. The existence of
same-fiber raw-distinct equal-bracket old18D source evidence remains
NO_DATA. Source parameters and raw endpoints never undergo an
unlicensed global identification or transport.

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

/-- A genuinely typed ORIGINAL old18D source, carrying both exact
raw17D endpoints. When inserted by the unit-history reader below,
the source is an original unitLeft or unitRight constructor itself:
its dependent before/F/G/C/after parameters are not replaced by
a string, side tag, quotient, or reconstructed surrogate. -/
def SelectedV592OriginalUnitAtom (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H K : SelectedContextualSixteen W l r T U) : Type uSix :=
  Σ J : SelectedContextualSeventeen W l r H K,
    Σ N : SelectedContextualSeventeen W l r H K,
      SelectedLocalEighteen W l r J N

/-- Read the actual original unit generators as fully typed payloads.
Raw reversal does NOT rewrite the original payload, and raw chain
retains the left-to-right order. The outer syntax/parenthesization
is intentionally observed separately by the existing v5.73 bracket. -/
def selectedV592OriginalUnitHistory (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    List (SelectedV592OriginalUnitAtom l r H K) :=
  match M with
  | .strict _ => []
  | .unitLeft before F G C after =>
      [⟨_, ⟨_, .unitLeft before F G C after⟩⟩]
  | .unitRight before F G C after =>
      [⟨_, ⟨_, .unitRight before F G C after⟩⟩]
  | .reverse A => selectedV592OriginalUnitHistory l r A
  | .chain A B =>
      selectedV592OriginalUnitHistory l r A ++
        selectedV592OriginalUnitHistory l r B

section OriginalTypedSource

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- The number of retained genuine unit-payload occurrences is
EXACTLY the separately certified v5.89 original unit count, for
the ENTIRE original dependent old18D Type, not merely a fragment. -/
theorem selectedV592OriginalUnitHistory_length
    (M : SelectedLocalEighteen W l r J N) :
    (selectedV592OriginalUnitHistory l r M).length =
      selectedV589OriginalUnitCount l r M := by
  induction M with
  | strict _ => rfl
  | unitLeft _ _ _ _ _ => rfl
  | unitRight _ _ _ _ _ => rfl
  | reverse A ih =>
      simpa only [selectedV592OriginalUnitHistory,
        selectedV589OriginalUnitCount] using ih
  | chain A B ihA ihB =>
      simp only [selectedV592OriginalUnitHistory, List.length_append,
        selectedV589OriginalUnitCount, ihA, ihB]

/-- Original reversal retains the typed unit payloads. This does
NOT assert any reverse identity for original raw old18D proofs. -/
theorem selectedV592OriginalUnitHistory_reverse
    (M : SelectedLocalEighteen W l r J N) :
    selectedV592OriginalUnitHistory l r
        (SelectedLocalEighteen.reverse M) =
      selectedV592OriginalUnitHistory l r M := rfl

/-- Original chain concatenates exact typed payloads, preserving
their supplied ordering and the genuine intermediate endpoint. -/
theorem selectedV592OriginalUnitHistory_chain
    {S : SelectedContextualSeventeen W l r H K}
    (A : SelectedLocalEighteen W l r J S)
    (B : SelectedLocalEighteen W l r S N) :
    selectedV592OriginalUnitHistory l r
        (SelectedLocalEighteen.chain A B) =
      selectedV592OriginalUnitHistory l r A ++
        selectedV592OriginalUnitHistory l r B := rfl

/-- Both actual roundtrip loops retain the original source unit
payload history twice, without simplifying raw reverse. -/
theorem selectedV592ForwardRoundTrip_unitHistory
    (M : SelectedLocalEighteen W l r J N) :
    selectedV592OriginalUnitHistory l r
        (selectedV591ForwardRoundTrip l r M) =
      selectedV592OriginalUnitHistory l r M ++
        selectedV592OriginalUnitHistory l r M := rfl

theorem selectedV592BackwardRoundTrip_unitHistory
    (M : SelectedLocalEighteen W l r J N) :
    selectedV592OriginalUnitHistory l r
        (selectedV591BackwardRoundTrip l r M) =
      selectedV592OriginalUnitHistory l r M ++
        selectedV592OriginalUnitHistory l r M := rfl

/-- A history-only observer cannot distinguish the forward and
backward original roundtrips, although they generally inhabit
DIFFERENT original raw17D fibers. -/
theorem selectedV592RoundTrips_sameUnitHistory
    (M : SelectedLocalEighteen W l r J N) :
    selectedV592OriginalUnitHistory l r
        (selectedV591ForwardRoundTrip l r M) =
      selectedV592OriginalUnitHistory l r
        (selectedV591BackwardRoundTrip l r M) := rfl

/-- The genuinely dependent two-unit forward/backward loops from
a one-unit original witness each retain exactly two original
unit payloads. The v5.91 raw17D endpoint inequality remains. -/
theorem selectedV592OneUnitRoundTrips_historyLength
    (M : SelectedLocalEighteen W l r J N)
    (hone : selectedV589OriginalUnitCount l r M = 1) :
    J ≠ N ∧
    (selectedV592OriginalUnitHistory l r
      (selectedV591ForwardRoundTrip l r M)).length = 2 ∧
    (selectedV592OriginalUnitHistory l r
      (selectedV591BackwardRoundTrip l r M)).length = 2 := by
  have h := selectedV591SingleUnitSourceRoundTrips l r M hone
  exact ⟨h.1,
    (selectedV592OriginalUnitHistory_length l r
      (selectedV591ForwardRoundTrip l r M)).trans h.2.1,
    (selectedV592OriginalUnitHistory_length l r
      (selectedV591BackwardRoundTrip l r M)).trans h.2.2⟩

/-- Genuine same-fiber raw loop with an original strict on the
LEFT of an entire source M; raw strict has no unit payload. -/
def selectedV592LoopStrictBefore
    (S : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r S S) :
    SelectedLocalEighteen W l r S S :=
  .chain (.strict S) M

/-- Genuine same-fiber raw loop with original strict on RIGHT.
No unit law or associativity equality is imposed. -/
def selectedV592LoopStrictAfter
    (S : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r S S) :
    SelectedLocalEighteen W l r S S :=
  .chain M (.strict S)

/-- The FULL typed original unit payload history fails to see
the placement of a strict at the boundary of the SAME genuine
raw17D S->S fiber. -/
theorem selectedV592StrictPlacement_sameUnitHistory
    (S : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r S S) :
    selectedV592OriginalUnitHistory l r
        (selectedV592LoopStrictBefore l r S M) =
      selectedV592OriginalUnitHistory l r
        (selectedV592LoopStrictAfter l r S M) := by
  simp [selectedV592LoopStrictBefore, selectedV592LoopStrictAfter,
    selectedV592OriginalUnitHistory]

/-- The two same-fiber strict placements retain the same ACTUAL
original unit count, without declaring the source proofs equal. -/
theorem selectedV592StrictPlacement_unitCounts
    (S : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r S S) :
    selectedV589OriginalUnitCount l r
        (selectedV592LoopStrictBefore l r S M) =
          selectedV589OriginalUnitCount l r M ∧
    selectedV589OriginalUnitCount l r
        (selectedV592LoopStrictAfter l r S M) =
          selectedV589OriginalUnitCount l r M := by
  simp [selectedV592LoopStrictBefore, selectedV592LoopStrictAfter,
    selectedV589OriginalUnitCount]

end OriginalTypedSource

section ActualUnitParameters

variable (l r : W)
variable {w z : W}
variable {b c d e : PentagonAdjoinedSixCell W l r w z}
variable (before : SevenRewrite W l r b c)
variable (F G : ContextFrameEleven W l r c d)
variable {P Q : SelectedUnitalCompositionTwelve W l r
  (contextFramePack l r F) (contextFramePack l r G)}
variable (C : SelectedContextualThirteen W l r P Q)
variable (after : SevenRewrite W l r d e)

/-- The original left-unit generator retains its FULL typed payload
twice in the genuine forward two-unit loop. Same-fiber insertion of
strict on opposite sides of that roundtrip yields:
  identical full typed unit-payload histories;
  distinct NONASSOCIATIVE old18D bracket observations;
  exactly two genuine unit occurrences on each side;
  distinct original old18D proof values in ONE exact start fiber.
This is NOT a same-bracket collision. -/
theorem selectedV592ActualLeftTwoUnitSameFiberHistoryGap :
    let S := selectedSeventeenUnitPrependLeft l r before F G C after
    let U := SelectedLocalEighteen.unitLeft before F G C after
    let R := selectedV591ForwardRoundTrip l r U
    let A := selectedV592LoopStrictBefore l r S R
    let B := selectedV592LoopStrictAfter l r S R
    selectedV592OriginalUnitHistory l r A =
      selectedV592OriginalUnitHistory l r B ∧
    selectedLocalEighteenInnerBracket l r A ≠
      selectedLocalEighteenInnerBracket l r B ∧
    selectedV589OriginalUnitCount l r A = 2 ∧
    selectedV589OriginalUnitCount l r B = 2 ∧
    A ≠ B := by
  dsimp only
  have hh := selectedV592StrictPlacement_sameUnitHistory l r
    (selectedSeventeenUnitPrependLeft l r before F G C after)
    (selectedV591ForwardRoundTrip l r
      (SelectedLocalEighteen.unitLeft before F G C after))
  have hb :
      selectedLocalEighteenInnerBracket l r
        (selectedV592LoopStrictBefore l r
          (selectedSeventeenUnitPrependLeft l r before F G C after)
          (selectedV591ForwardRoundTrip l r
            (SelectedLocalEighteen.unitLeft before F G C after))) ≠
      selectedLocalEighteenInnerBracket l r
        (selectedV592LoopStrictAfter l r
          (selectedSeventeenUnitPrependLeft l r before F G C after)
          (selectedV591ForwardRoundTrip l r
            (SelectedLocalEighteen.unitLeft before F G C after))) := by
    decide
  refine ⟨hh, hb, ?_, ?_, ?_⟩
  · decide
  · decide
  · intro heq
    exact hb (congrArg (selectedLocalEighteenInnerBracket l r) heq)

/-- The independent actual RIGHT-unit generator has the same
same-fiber history/bracket separation, retaining its own actual
unitRight parameter payloads and never identifying left with right. -/
theorem selectedV592ActualRightTwoUnitSameFiberHistoryGap :
    let S := selectedSeventeenUnitPrependRight l r before F G C after
    let U := SelectedLocalEighteen.unitRight before F G C after
    let R := selectedV591ForwardRoundTrip l r U
    let A := selectedV592LoopStrictBefore l r S R
    let B := selectedV592LoopStrictAfter l r S R
    selectedV592OriginalUnitHistory l r A =
      selectedV592OriginalUnitHistory l r B ∧
    selectedLocalEighteenInnerBracket l r A ≠
      selectedLocalEighteenInnerBracket l r B ∧
    selectedV589OriginalUnitCount l r A = 2 ∧
    selectedV589OriginalUnitCount l r B = 2 ∧
    A ≠ B := by
  dsimp only
  have hh := selectedV592StrictPlacement_sameUnitHistory l r
    (selectedSeventeenUnitPrependRight l r before F G C after)
    (selectedV591ForwardRoundTrip l r
      (SelectedLocalEighteen.unitRight before F G C after))
  have hb :
      selectedLocalEighteenInnerBracket l r
        (selectedV592LoopStrictBefore l r
          (selectedSeventeenUnitPrependRight l r before F G C after)
          (selectedV591ForwardRoundTrip l r
            (SelectedLocalEighteen.unitRight before F G C after))) ≠
      selectedLocalEighteenInnerBracket l r
        (selectedV592LoopStrictAfter l r
          (selectedSeventeenUnitPrependRight l r before F G C after)
          (selectedV591ForwardRoundTrip l r
            (SelectedLocalEighteen.unitRight before F G C after))) := by
    decide
  refine ⟨hh, hb, ?_, ?_, ?_⟩
  · decide
  · decide
  · intro heq
    exact hb (congrArg (selectedLocalEighteenInnerBracket l r) heq)

end ActualUnitParameters

#print axioms PentagonAdjoinedSixCell.SelectedV592OriginalUnitAtom
#print axioms PentagonAdjoinedSixCell.selectedV592OriginalUnitHistory
#print axioms PentagonAdjoinedSixCell.selectedV592OriginalUnitHistory_length
#print axioms PentagonAdjoinedSixCell.selectedV592OriginalUnitHistory_reverse
#print axioms PentagonAdjoinedSixCell.selectedV592OriginalUnitHistory_chain
#print axioms PentagonAdjoinedSixCell.selectedV592ForwardRoundTrip_unitHistory
#print axioms PentagonAdjoinedSixCell.selectedV592BackwardRoundTrip_unitHistory
#print axioms PentagonAdjoinedSixCell.selectedV592RoundTrips_sameUnitHistory
#print axioms PentagonAdjoinedSixCell.selectedV592OneUnitRoundTrips_historyLength
#print axioms PentagonAdjoinedSixCell.selectedV592LoopStrictBefore
#print axioms PentagonAdjoinedSixCell.selectedV592LoopStrictAfter
#print axioms PentagonAdjoinedSixCell.selectedV592StrictPlacement_sameUnitHistory
#print axioms PentagonAdjoinedSixCell.selectedV592StrictPlacement_unitCounts
#print axioms PentagonAdjoinedSixCell.selectedV592ActualLeftTwoUnitSameFiberHistoryGap
#print axioms PentagonAdjoinedSixCell.selectedV592ActualRightTwoUnitSameFiberHistoryGap

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
