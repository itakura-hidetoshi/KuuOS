import KUOS.Architecture.QiWuxingGK5CHP77GuardedInheritedWhiskerFragmentV5_83

/-!
Qi v5.84 — genuine RIGHT-whiskered guarded local faithfulness and
TWO-SOURCE internal-bracket separation, without identifying different
dependent 17D fibers.

We retain the original dependent contextual18D Type and the independently
typed old five-generator and new seven-generator selected19 comparisons.
For an ACTUALLY GIVEN right context F/G, after : SevenRewrite and 17D
endpoint N, and a SEPARATELY GIVEN old18D proof M in the exact right-
whiskered endpoint N'→N' fiber, embed the same three restricted branches:
pure strict/reverse/chain at N', reverse(inherited M), and
reverse(whiskerRight F G (strict N) after). The independent v5.81
quotient-descended placement tree reflects equality on this image.

With TWO separately supplied old18D values M,L in that very same fiber,
inequality of their independently observed inherited inner-bracket trees
is a sufficient witness for different old/new genuine quotient classes
and absence of original typed 19D comparisons. Equality of the brackets
alone is explicitly NOT sufficient to identify the original proofs.

The original unguarded strict/inherited unit law remains an actual
old/new quotient collapse: the raw 18D values are different. No
right-to-left WORLD/17D fiber transport, 20D gluing, arbitrary M, arbitrary
SevenRewrite, global quotient classification or action authority is
claimed. All historical Type definitions, Lean/mathlib pins, public root107
and protected validation PR #1558 remain unchanged.
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

/-- A THREE-BRANCH local fragment, not free closure under arbitrary
unprotected inherited leaves or whiskering operations. -/
inductive SelectedV584RightGuardedFragment : Type where
  | pure : SelectedPureStrictReverseTree → SelectedV584RightGuardedFragment
  | inheritedGuard : SelectedV584RightGuardedFragment
  | rightGuard : SelectedV584RightGuardedFragment
  deriving DecidableEq, Repr

/-- The source bracket is fixed by the actually given old18D witness.
A source with a different old18D proof is NOT identified by this tag. -/
def selectedV584RawValue (s : SelectedInheritedOldInnerBracket) :
    SelectedV584RightGuardedFragment → SelectedWhiskerPlacementTree
  | .pure A => selectedPureStrictReverseRawValue A
  | .inheritedGuard => .reversed (.source s)
  | .rightGuard => .reversed (.right .strict)

/-- No v5.82 pure term contains an inherited-source top constructor. -/
theorem selectedV584Pure_neSource
    (A : SelectedPureStrictReverseTree)
    (s : SelectedInheritedOldInnerBracket) :
    selectedPureStrictReverseRawValue A ≠
      SelectedWhiskerPlacementTree.source s := by
  cases A <;> simp [selectedPureStrictReverseRawValue]

/-- No v5.82 pure term contains a top-level right-whisker constructor. -/
theorem selectedV584Pure_neRight
    (A : SelectedPureStrictReverseTree) :
    selectedPureStrictReverseRawValue A ≠
      SelectedWhiskerPlacementTree.right .strict := by
  cases A <;> simp [selectedPureStrictReverseRawValue]

theorem selectedV584Pure_neGuardedSource
    (A : SelectedPureStrictReverseTree)
    (s : SelectedInheritedOldInnerBracket) :
    selectedPureStrictReverseRawValue A ≠
      SelectedWhiskerPlacementTree.reversed (.source s) := by
  cases A with
  | strict => simp [selectedPureStrictReverseRawValue]
  | reversed A =>
      simpa [selectedPureStrictReverseRawValue] using
        (selectedV584Pure_neSource A s)
  | joined A B => simp [selectedPureStrictReverseRawValue]

theorem selectedV584Pure_neGuardedRight
    (A : SelectedPureStrictReverseTree) :
    selectedPureStrictReverseRawValue A ≠
      SelectedWhiskerPlacementTree.reversed (.right .strict) := by
  cases A with
  | strict => simp [selectedPureStrictReverseRawValue]
  | reversed A =>
      simpa [selectedPureStrictReverseRawValue] using
        (selectedV584Pure_neRight A)
  | joined A B => simp [selectedPureStrictReverseRawValue]

/-- The auxiliary syntax is injectively read by the REAL v5.81
quotient-descended observer after the typed embedding below. -/
theorem selectedV584RawValue_injective
    (s : SelectedInheritedOldInnerBracket) :
    Function.Injective (selectedV584RawValue s) := by
  intro A B h
  cases A with
  | pure A =>
      cases B with
      | pure B =>
          have hp : selectedPureStrictReverseRawValue A =
              selectedPureStrictReverseRawValue B := h
          have heq := selectedPureStrictReverseRawValue_injective hp
          cases heq
          rfl
      | inheritedGuard =>
          exact False.elim (selectedV584Pure_neGuardedSource A s h)
      | rightGuard =>
          exact False.elim (selectedV584Pure_neGuardedRight A h)
  | inheritedGuard =>
      cases B with
      | pure B =>
          exact False.elim (selectedV584Pure_neGuardedSource B s h.symm)
      | inheritedGuard => rfl
      | rightGuard =>
          change SelectedWhiskerPlacementTree.reversed (.source s) =
            .reversed (.right .strict) at h
          cases h
  | rightGuard =>
      cases B with
      | pure B =>
          exact False.elim (selectedV584Pure_neGuardedRight B h.symm)
      | inheritedGuard =>
          change SelectedWhiskerPlacementTree.reversed (.right .strict) =
            .reversed (.source s) at h
          cases h
      | rightGuard => rfl

section SuppliedExactRightFiber

variable (l r : W)
variable {w z : W}
variable {c d e : PentagonAdjoinedSixCell W l r w z}
variable (F G : ContextFrameEleven W l r c d)
variable (after : SevenRewrite W l r d e)
variable {P Q : SelectedUnitalCompositionTwelve W l r
  (contextFramePack l r F) (contextFramePack l r G)}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}

/-- Genuine typed embedding in the ACTUAL right-whiskered 17D exact
fiber. Both the old18D source M and the SevenRewrite are parameters,
not inhabitants invented by the construction. -/
def selectedV584RightEmbed
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)) :
    SelectedV584RightGuardedFragment →
      SelectedContextualEighteen W l r
        (.whiskerRight F G N after) (.whiskerRight F G N after)
  | .pure A =>
      selectedPureStrictReverseEmbed l r (.whiskerRight F G N after) A
  | .inheritedGuard => .reverse (.inherited M)
  | .rightGuard => .reverse (.whiskerRight F G (.strict N) after)

/-- Comparison with the independently defined free reading is
performed on the genuine original dependent Type18D evidence. -/
theorem selectedV584Right_observed
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (A : SelectedV584RightGuardedFragment) :
    selectedContextEighteenWhiskerPlacement l r
        (selectedV584RightEmbed l r F G after N M A) =
      selectedV584RawValue (selectedLocalEighteenInnerBracket l r M) A := by
  cases A with
  | pure A =>
      exact selectedPureStrictReverse_observed l r
        (.whiskerRight F G N after) A
  | inheritedGuard => rfl
  | rightGuard => rfl

theorem selectedV584Right_embedInjective
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)) :
    Function.Injective (selectedV584RightEmbed l r F G after N M) := by
  intro A B h
  have ho := congrArg (selectedContextEighteenWhiskerPlacement l r) h
  rw [selectedV584Right_observed l r F G after N M A,
    selectedV584Right_observed l r F G after N M B] at ho
  exact selectedV584RawValue_injective
    (selectedLocalEighteenInnerBracket l r M) ho

/-- Original new seven-generator quotient: local equality iff the
explicitly restricted three-branch source syntax agrees. -/
theorem selectedV584Right_newClassEq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (A B : SelectedV584RightGuardedFragment) :
    selectedRawCongruentClass l r
      (selectedV584RightEmbed l r F G after N M A) =
    selectedRawCongruentClass l r
      (selectedV584RightEmbed l r F G after N M B) ↔ A = B := by
  constructor
  · intro h
    have ho := congrArg
      (selectedRawCongruentWhiskerPlacementOnQuotient l r
        (.whiskerRight F G N after) (.whiskerRight F G N after)) h
    change selectedContextEighteenWhiskerPlacement l r
        (selectedV584RightEmbed l r F G after N M A) =
      selectedContextEighteenWhiskerPlacement l r
        (selectedV584RightEmbed l r F G after N M B) at ho
    rw [selectedV584Right_observed l r F G after N M A,
      selectedV584Right_observed l r F G after N M B] at ho
    exact selectedV584RawValue_injective
      (selectedLocalEighteenInnerBracket l r M) ho
  · rintro rfl
    rfl

/-- Independently typed OLD five-generator quotient, with the same
equality kernel ONLY on the chosen three-branch image. -/
theorem selectedV584Right_oldClassEq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (A B : SelectedV584RightGuardedFragment) :
    selectedNineteenClass l r
      (selectedV584RightEmbed l r F G after N M A) =
    selectedNineteenClass l r
      (selectedV584RightEmbed l r F G after N M B) ↔ A = B := by
  constructor
  · intro h
    have ho := congrArg
      (selectedNineteenWhiskerPlacementOnQuotient l r
        (.whiskerRight F G N after) (.whiskerRight F G N after)) h
    change selectedContextEighteenWhiskerPlacement l r
        (selectedV584RightEmbed l r F G after N M A) =
      selectedContextEighteenWhiskerPlacement l r
        (selectedV584RightEmbed l r F G after N M B) at ho
    rw [selectedV584Right_observed l r F G after N M A,
      selectedV584Right_observed l r F G after N M B] at ho
    exact selectedV584RawValue_injective
      (selectedLocalEighteenInnerBracket l r M) ho
  · rintro rfl
    rfl

theorem selectedV584Right_oldComparison_iff
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (A B : SelectedV584RightGuardedFragment) :
    Nonempty (SelectedLocalNineteen W l r
      (selectedV584RightEmbed l r F G after N M A)
      (selectedV584RightEmbed l r F G after N M B)) ↔ A = B := by
  constructor
  · rintro ⟨h⟩
    exact (selectedV584Right_oldClassEq_iff l r F G after N M A B).mp
      (Quotient.sound ⟨h⟩)
  · rintro rfl
    exact ⟨.strict (selectedV584RightEmbed l r F G after N M A)⟩

theorem selectedV584Right_newComparison_iff
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (A B : SelectedV584RightGuardedFragment) :
    Nonempty (SelectedRawCongruentNineteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)
      (selectedV584RightEmbed l r F G after N M A)
      (selectedV584RightEmbed l r F G after N M B)) ↔ A = B := by
  constructor
  · rintro ⟨h⟩
    exact (selectedV584Right_newClassEq_iff l r F G after N M A B).mp
      (Quotient.sound ⟨h⟩)
  · rintro rfl
    exact ⟨.strict (selectedV584RightEmbed l r F G after N M A)⟩

/-- Type19D comparison grammars are NOT identified. Existence merely
has the same kernel on the one anchored subpresentation. -/
theorem selectedV584Right_oldNewComparison_iff
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (A B : SelectedV584RightGuardedFragment) :
    Nonempty (SelectedLocalNineteen W l r
      (selectedV584RightEmbed l r F G after N M A)
      (selectedV584RightEmbed l r F G after N M B)) ↔
    Nonempty (SelectedRawCongruentNineteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)
      (selectedV584RightEmbed l r F G after N M A)
      (selectedV584RightEmbed l r F G after N M B)) := by
  exact (selectedV584Right_oldComparison_iff l r F G after N M A B).trans
    (selectedV584Right_newComparison_iff l r F G after N M A B).symm

/-- Full v5.81 observation: includes ALL v5.80 coordinates and both
untruncated Nat towers plus independently descended placement tree. -/
theorem selectedV584Right_fullV581Eq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (A B : SelectedV584RightGuardedFragment) :
    selectedRawCongruentFullV581QuotientObservation l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)
      (selectedRawCongruentClass l r
        (selectedV584RightEmbed l r F G after N M A)) =
    selectedRawCongruentFullV581QuotientObservation l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)
      (selectedRawCongruentClass l r
        (selectedV584RightEmbed l r F G after N M B)) ↔ A = B := by
  constructor
  · intro h
    have ho := congrArg Prod.snd h
    change selectedContextEighteenWhiskerPlacement l r
        (selectedV584RightEmbed l r F G after N M A) =
      selectedContextEighteenWhiskerPlacement l r
        (selectedV584RightEmbed l r F G after N M B) at ho
    rw [selectedV584Right_observed l r F G after N M A,
      selectedV584Right_observed l r F G after N M B] at ho
    exact selectedV584RawValue_injective
      (selectedLocalEighteenInnerBracket l r M) ho
  · rintro rfl
    rfl

/-- Why direct unguarded inherited sources cannot be freely added:
the ORIGINAL old selected19 unit is an actual comparison. -/
theorem selectedV584Right_unguardedUnitOldNew
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)) :
    selectedNineteenClass l r
        (.chain (.strict (.whiskerRight F G N after)) (.inherited M)) =
      selectedNineteenClass l r (.inherited M) ∧
    selectedRawCongruentClass l r
        (.chain (.strict (.whiskerRight F G N after)) (.inherited M)) =
      selectedRawCongruentClass l r (.inherited M) := by
  constructor
  · exact Quotient.sound ⟨SelectedLocalNineteen.unitPrepend M⟩
  · exact Quotient.sound
      ⟨SelectedRawCongruentNineteen.inherited
        (SelectedLocalNineteen.unitPrepend M)⟩

/-- The two witnesses in the unit equation are actually DIFFERENT
original raw dependent 18D constructor values. -/
theorem selectedV584Right_unguardedRawDistinct
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)) :
    (SelectedContextualEighteen.chain
        (.strict (.whiskerRight F G N after)) (.inherited M)) ≠
      (SelectedContextualEighteen.inherited M) := by
  intro h
  cases h


/-- One direction only: quotient equality forces equality of the
independently observed genuine inherited old18D internal brackets.
There is NO converse from observational equality alone. -/
theorem selectedV584Right_twoSourceOldClassEq_impliesBracketEq
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (h : selectedNineteenClass l r
        (SelectedContextualEighteen.inherited M) =
      selectedNineteenClass l r
        (SelectedContextualEighteen.inherited L)) :
    selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L := by
  have ho := congrArg
    (selectedNineteenWhiskerPlacementOnQuotient l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)) h
  change SelectedWhiskerPlacementTree.source
      (selectedLocalEighteenInnerBracket l r M) =
    SelectedWhiskerPlacementTree.source
      (selectedLocalEighteenInnerBracket l r L) at ho
  injection ho with hbr

theorem selectedV584Right_twoSourceNewClassEq_impliesBracketEq
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (h : selectedRawCongruentClass l r
        (SelectedContextualEighteen.inherited M) =
      selectedRawCongruentClass l r
        (SelectedContextualEighteen.inherited L)) :
    selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L := by
  have ho := congrArg
    (selectedRawCongruentWhiskerPlacementOnQuotient l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)) h
  change SelectedWhiskerPlacementTree.source
      (selectedLocalEighteenInnerBracket l r M) =
    SelectedWhiskerPlacementTree.source
      (selectedLocalEighteenInnerBracket l r L) at ho
  injection ho with hbr

/-- Proven obstruction: different old18D bracket observations cannot
be glued into one old or new quotient class in this genuine fiber. -/
theorem selectedV584Right_twoSourceClassDistinct
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (hdiff : selectedLocalEighteenInnerBracket l r M ≠
      selectedLocalEighteenInnerBracket l r L) :
    selectedNineteenClass l r
        (SelectedContextualEighteen.inherited M) ≠
      selectedNineteenClass l r
        (SelectedContextualEighteen.inherited L) ∧
    selectedRawCongruentClass l r
        (SelectedContextualEighteen.inherited M) ≠
      selectedRawCongruentClass l r
        (SelectedContextualEighteen.inherited L) := by
  constructor
  · intro h
    exact hdiff
      (selectedV584Right_twoSourceOldClassEq_impliesBracketEq
        l r F G after N M L h)
  · intro h
    exact hdiff
      (selectedV584Right_twoSourceNewClassEq_impliesBracketEq
        l r F G after N M L h)

/-- The ORIGINAL old Type19D and the independent new Type19D cannot
witness a comparison when the two given source brackets differ. -/
theorem selectedV584Right_twoSourceNoComparison
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (hdiff : selectedLocalEighteenInnerBracket l r M ≠
      selectedLocalEighteenInnerBracket l r L) :
    ¬ Nonempty (SelectedLocalNineteen W l r
        (SelectedContextualEighteen.inherited M)
        (SelectedContextualEighteen.inherited L)) ∧
    ¬ Nonempty (SelectedRawCongruentNineteen W l r
        (.whiskerRight F G N after) (.whiskerRight F G N after)
        (SelectedContextualEighteen.inherited M)
        (SelectedContextualEighteen.inherited L)) := by
  obtain ⟨ho, hn⟩ :=
    selectedV584Right_twoSourceClassDistinct l r F G after N M L hdiff
  constructor
  · rintro ⟨h⟩
    exact ho (Quotient.sound ⟨h⟩)
  · rintro ⟨h⟩
    exact hn (Quotient.sound ⟨h⟩)

/-- The same bracket-separation witness persists under ONE raw
reverse guard in the ORIGINAL new seven-generator quotient. -/
theorem selectedV584Right_twoGuardedSourcesNewDistinct
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (hdiff : selectedLocalEighteenInnerBracket l r M ≠
      selectedLocalEighteenInnerBracket l r L) :
    selectedRawCongruentClass l r
        (SelectedContextualEighteen.reverse (.inherited M)) ≠
      selectedRawCongruentClass l r
        (SelectedContextualEighteen.reverse (.inherited L)) := by
  intro h
  have ho := congrArg
    (selectedRawCongruentWhiskerPlacementOnQuotient l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)) h
  change SelectedWhiskerPlacementTree.reversed
      (.source (selectedLocalEighteenInnerBracket l r M)) =
    SelectedWhiskerPlacementTree.reversed
      (.source (selectedLocalEighteenInnerBracket l r L)) at ho
  injection ho with hinner
  injection hinner with hbr
  exact hdiff hbr

/-- The true ORIGINAL unit-append rule also collapses the raw
strict-next-to-inherited source (in both real selected19 quotients).
This is a second explicitly retained obstruction to free closure. -/
theorem selectedV584Right_unguardedAppendOldNew
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)) :
    selectedNineteenClass l r
        (.chain (.inherited M)
          (.strict (.whiskerRight F G N after))) =
      selectedNineteenClass l r (.inherited M) ∧
    selectedRawCongruentClass l r
        (.chain (.inherited M)
          (.strict (.whiskerRight F G N after))) =
      selectedRawCongruentClass l r (.inherited M) := by
  constructor
  · exact Quotient.sound ⟨SelectedLocalNineteen.unitAppend M⟩
  · exact Quotient.sound
      ⟨SelectedRawCongruentNineteen.inherited
        (SelectedLocalNineteen.unitAppend M)⟩

/-- Despite the original genuine unit-append quotient collapse, the
two raw dependent 18D constructor values are not definitionally equal. -/
theorem selectedV584Right_unguardedAppendRawDistinct
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)) :
    (SelectedContextualEighteen.chain (.inherited M)
      (.strict (.whiskerRight F G N after))) ≠
      (SelectedContextualEighteen.inherited M) := by
  intro h
  cases h

end SuppliedExactRightFiber

#print axioms PentagonAdjoinedSixCell.SelectedV584RightGuardedFragment
#print axioms PentagonAdjoinedSixCell.selectedV584RawValue
#print axioms PentagonAdjoinedSixCell.selectedV584Pure_neSource
#print axioms PentagonAdjoinedSixCell.selectedV584Pure_neRight
#print axioms PentagonAdjoinedSixCell.selectedV584Pure_neGuardedSource
#print axioms PentagonAdjoinedSixCell.selectedV584Pure_neGuardedRight
#print axioms PentagonAdjoinedSixCell.selectedV584RawValue_injective
#print axioms PentagonAdjoinedSixCell.selectedV584RightEmbed
#print axioms PentagonAdjoinedSixCell.selectedV584Right_observed
#print axioms PentagonAdjoinedSixCell.selectedV584Right_embedInjective
#print axioms PentagonAdjoinedSixCell.selectedV584Right_newClassEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV584Right_oldClassEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV584Right_oldComparison_iff
#print axioms PentagonAdjoinedSixCell.selectedV584Right_newComparison_iff
#print axioms PentagonAdjoinedSixCell.selectedV584Right_oldNewComparison_iff
#print axioms PentagonAdjoinedSixCell.selectedV584Right_fullV581Eq_iff
#print axioms PentagonAdjoinedSixCell.selectedV584Right_unguardedUnitOldNew
#print axioms PentagonAdjoinedSixCell.selectedV584Right_unguardedRawDistinct

#print axioms PentagonAdjoinedSixCell.selectedV584Right_twoSourceOldClassEq_impliesBracketEq
#print axioms PentagonAdjoinedSixCell.selectedV584Right_twoSourceNewClassEq_impliesBracketEq
#print axioms PentagonAdjoinedSixCell.selectedV584Right_twoSourceClassDistinct
#print axioms PentagonAdjoinedSixCell.selectedV584Right_twoSourceNoComparison
#print axioms PentagonAdjoinedSixCell.selectedV584Right_twoGuardedSourcesNewDistinct
#print axioms PentagonAdjoinedSixCell.selectedV584Right_unguardedAppendOldNew
#print axioms PentagonAdjoinedSixCell.selectedV584Right_unguardedAppendRawDistinct

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
