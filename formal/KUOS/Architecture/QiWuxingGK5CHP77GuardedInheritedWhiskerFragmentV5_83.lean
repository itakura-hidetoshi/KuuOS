import KUOS.Architecture.QiWuxingGK5CHP77PureStrictReverseFaithfulFragmentV5_82

/-!
Qi v5.83 — conditional, one-anchor extension of v5.82's faithful
genuine N→N pure strict/reverse/chain fragment. The SAME original
dependent contextual18D Type, independently defined old five-generator
selected19 Type and new seven-generator selected19 Type are retained.

For a GIVEN left SevenRewrite/context frame, a genuine source endpoint N,
and an independently GIVEN old selected18D proof M at the actual
left-whiskered endpoint N', form three genuine kinds of N'→N' proofs:
  (1) all v5.82 pure syntax at N',
  (2) one reverse-guarded inherited old18D source M,
  (3) one reverse-guarded genuine left-whiskering of strict N.
The two anchors are reverse-guarded so the ORIGINAL selected19 direct
strict/inherited unit generators cannot erase the anchor at a raw join.
The separately descended v5.81 whisker-placement tree distinguishes
all three classes, conditionally on exactly these supplied sources.

Both old and new TRUE quotient equality and Type-valued comparison
existence reflect syntactic equality on this small union. The complete
v5.81 observation (including both full Nat-indexed towers) is faithful
on the same restricted image. The directly unguarded inherited source
still satisfies a TRUE selected19 unit collapse; this obstruction is
retained, rather than asserting a free full inherited grammar.

No arbitrary old source/rewrite inhabitance, arbitrary whisker fiber,
global old/new 19D equivalence, full18D classification, cross-WORLD
gluing, 20D descent, or action authority is claimed. Do not change
historical definitions, tool pins, public root107, or protected #1558.
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
inductive SelectedV583GuardedFragment : Type where
  | pure : SelectedPureStrictReverseTree → SelectedV583GuardedFragment
  | inheritedGuard : SelectedV583GuardedFragment
  | leftGuard : SelectedV583GuardedFragment
  deriving DecidableEq, Repr

/-- The source bracket is fixed by the actually given old18D witness.
A source with a different old18D proof is NOT identified by this tag. -/
def selectedV583RawValue (s : SelectedInheritedOldInnerBracket) :
    SelectedV583GuardedFragment → SelectedWhiskerPlacementTree
  | .pure A => selectedPureStrictReverseRawValue A
  | .inheritedGuard => .reversed (.source s)
  | .leftGuard => .reversed (.left .strict)

/-- No v5.82 pure term contains an inherited-source top constructor. -/
theorem selectedV583Pure_neSource
    (A : SelectedPureStrictReverseTree)
    (s : SelectedInheritedOldInnerBracket) :
    selectedPureStrictReverseRawValue A ≠
      SelectedWhiskerPlacementTree.source s := by
  cases A <;> simp [selectedPureStrictReverseRawValue]

/-- No v5.82 pure term contains a top-level left-whisker constructor. -/
theorem selectedV583Pure_neLeft
    (A : SelectedPureStrictReverseTree) :
    selectedPureStrictReverseRawValue A ≠
      SelectedWhiskerPlacementTree.left .strict := by
  cases A <;> simp [selectedPureStrictReverseRawValue]

theorem selectedV583Pure_neGuardedSource
    (A : SelectedPureStrictReverseTree)
    (s : SelectedInheritedOldInnerBracket) :
    selectedPureStrictReverseRawValue A ≠
      SelectedWhiskerPlacementTree.reversed (.source s) := by
  cases A with
  | strict => simp [selectedPureStrictReverseRawValue]
  | reversed A =>
      simpa [selectedPureStrictReverseRawValue] using
        (selectedV583Pure_neSource A s)
  | joined A B => simp [selectedPureStrictReverseRawValue]

theorem selectedV583Pure_neGuardedLeft
    (A : SelectedPureStrictReverseTree) :
    selectedPureStrictReverseRawValue A ≠
      SelectedWhiskerPlacementTree.reversed (.left .strict) := by
  cases A with
  | strict => simp [selectedPureStrictReverseRawValue]
  | reversed A =>
      simpa [selectedPureStrictReverseRawValue] using
        (selectedV583Pure_neLeft A)
  | joined A B => simp [selectedPureStrictReverseRawValue]

/-- The auxiliary syntax is injectively read by the REAL v5.81
quotient-descended observer after the typed embedding below. -/
theorem selectedV583RawValue_injective
    (s : SelectedInheritedOldInnerBracket) :
    Function.Injective (selectedV583RawValue s) := by
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
          exact False.elim (selectedV583Pure_neGuardedSource A s h)
      | leftGuard =>
          exact False.elim (selectedV583Pure_neGuardedLeft A h)
  | inheritedGuard =>
      cases B with
      | pure B =>
          exact False.elim (selectedV583Pure_neGuardedSource B s h.symm)
      | inheritedGuard => rfl
      | leftGuard =>
          change SelectedWhiskerPlacementTree.reversed (.source s) =
            .reversed (.left .strict) at h
          cases h
  | leftGuard =>
      cases B with
      | pure B =>
          exact False.elim (selectedV583Pure_neGuardedLeft B h.symm)
      | inheritedGuard =>
          change SelectedWhiskerPlacementTree.reversed (.left .strict) =
            .reversed (.source s) at h
          cases h
      | leftGuard => rfl

section SuppliedExactLeftFiber

variable (l r : W)
variable {w z : W}
variable {b c d : PentagonAdjoinedSixCell W l r w z}
variable (before : SevenRewrite W l r b c)
variable (F G : ContextFrameEleven W l r c d)
variable {P Q : SelectedUnitalCompositionTwelve W l r
  (contextFramePack l r F) (contextFramePack l r G)}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}

/-- Genuine typed embedding in the ACTUAL left-whiskered 17D exact
fiber. Both the old18D source M and the SevenRewrite are parameters,
not inhabitants invented by the construction. -/
def selectedV583LeftEmbed
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N)) :
    SelectedV583GuardedFragment →
      SelectedContextualEighteen W l r
        (.whiskerLeft before F G N) (.whiskerLeft before F G N)
  | .pure A =>
      selectedPureStrictReverseEmbed l r (.whiskerLeft before F G N) A
  | .inheritedGuard => .reverse (.inherited M)
  | .leftGuard => .reverse (.whiskerLeft before F G (.strict N))

/-- Comparison with the independently defined free reading is
performed on the genuine original dependent Type18D evidence. -/
theorem selectedV583Left_observed
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N))
    (A : SelectedV583GuardedFragment) :
    selectedContextEighteenWhiskerPlacement l r
        (selectedV583LeftEmbed l r before F G N M A) =
      selectedV583RawValue (selectedLocalEighteenInnerBracket l r M) A := by
  cases A with
  | pure A =>
      exact selectedPureStrictReverse_observed l r
        (.whiskerLeft before F G N) A
  | inheritedGuard => rfl
  | leftGuard => rfl

theorem selectedV583Left_embedInjective
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N)) :
    Function.Injective (selectedV583LeftEmbed l r before F G N M) := by
  intro A B h
  have ho := congrArg (selectedContextEighteenWhiskerPlacement l r) h
  rw [selectedV583Left_observed l r before F G N M A,
    selectedV583Left_observed l r before F G N M B] at ho
  exact selectedV583RawValue_injective
    (selectedLocalEighteenInnerBracket l r M) ho

/-- Original new seven-generator quotient: local equality iff the
explicitly restricted three-branch source syntax agrees. -/
theorem selectedV583Left_newClassEq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N))
    (A B : SelectedV583GuardedFragment) :
    selectedRawCongruentClass l r
      (selectedV583LeftEmbed l r before F G N M A) =
    selectedRawCongruentClass l r
      (selectedV583LeftEmbed l r before F G N M B) ↔ A = B := by
  constructor
  · intro h
    have ho := congrArg
      (selectedRawCongruentWhiskerPlacementOnQuotient l r
        (.whiskerLeft before F G N) (.whiskerLeft before F G N)) h
    change selectedContextEighteenWhiskerPlacement l r
        (selectedV583LeftEmbed l r before F G N M A) =
      selectedContextEighteenWhiskerPlacement l r
        (selectedV583LeftEmbed l r before F G N M B) at ho
    rw [selectedV583Left_observed l r before F G N M A,
      selectedV583Left_observed l r before F G N M B] at ho
    exact selectedV583RawValue_injective
      (selectedLocalEighteenInnerBracket l r M) ho
  · rintro rfl
    rfl

/-- Independently typed OLD five-generator quotient, with the same
equality kernel ONLY on the chosen three-branch image. -/
theorem selectedV583Left_oldClassEq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N))
    (A B : SelectedV583GuardedFragment) :
    selectedNineteenClass l r
      (selectedV583LeftEmbed l r before F G N M A) =
    selectedNineteenClass l r
      (selectedV583LeftEmbed l r before F G N M B) ↔ A = B := by
  constructor
  · intro h
    have ho := congrArg
      (selectedNineteenWhiskerPlacementOnQuotient l r
        (.whiskerLeft before F G N) (.whiskerLeft before F G N)) h
    change selectedContextEighteenWhiskerPlacement l r
        (selectedV583LeftEmbed l r before F G N M A) =
      selectedContextEighteenWhiskerPlacement l r
        (selectedV583LeftEmbed l r before F G N M B) at ho
    rw [selectedV583Left_observed l r before F G N M A,
      selectedV583Left_observed l r before F G N M B] at ho
    exact selectedV583RawValue_injective
      (selectedLocalEighteenInnerBracket l r M) ho
  · rintro rfl
    rfl

theorem selectedV583Left_oldComparison_iff
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N))
    (A B : SelectedV583GuardedFragment) :
    Nonempty (SelectedLocalNineteen W l r
      (selectedV583LeftEmbed l r before F G N M A)
      (selectedV583LeftEmbed l r before F G N M B)) ↔ A = B := by
  constructor
  · rintro ⟨h⟩
    exact (selectedV583Left_oldClassEq_iff l r before F G N M A B).mp
      (Quotient.sound ⟨h⟩)
  · rintro rfl
    exact ⟨.strict (selectedV583LeftEmbed l r before F G N M A)⟩

theorem selectedV583Left_newComparison_iff
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N))
    (A B : SelectedV583GuardedFragment) :
    Nonempty (SelectedRawCongruentNineteen W l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N)
      (selectedV583LeftEmbed l r before F G N M A)
      (selectedV583LeftEmbed l r before F G N M B)) ↔ A = B := by
  constructor
  · rintro ⟨h⟩
    exact (selectedV583Left_newClassEq_iff l r before F G N M A B).mp
      (Quotient.sound ⟨h⟩)
  · rintro rfl
    exact ⟨.strict (selectedV583LeftEmbed l r before F G N M A)⟩

/-- Type19D comparison grammars are NOT identified. Existence merely
has the same kernel on the one anchored subpresentation. -/
theorem selectedV583Left_oldNewComparison_iff
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N))
    (A B : SelectedV583GuardedFragment) :
    Nonempty (SelectedLocalNineteen W l r
      (selectedV583LeftEmbed l r before F G N M A)
      (selectedV583LeftEmbed l r before F G N M B)) ↔
    Nonempty (SelectedRawCongruentNineteen W l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N)
      (selectedV583LeftEmbed l r before F G N M A)
      (selectedV583LeftEmbed l r before F G N M B)) := by
  exact (selectedV583Left_oldComparison_iff l r before F G N M A B).trans
    (selectedV583Left_newComparison_iff l r before F G N M A B).symm

/-- Full v5.81 observation: includes ALL v5.80 coordinates and both
untruncated Nat towers plus independently descended placement tree. -/
theorem selectedV583Left_fullV581Eq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N))
    (A B : SelectedV583GuardedFragment) :
    selectedRawCongruentFullV581QuotientObservation l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N)
      (selectedRawCongruentClass l r
        (selectedV583LeftEmbed l r before F G N M A)) =
    selectedRawCongruentFullV581QuotientObservation l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N)
      (selectedRawCongruentClass l r
        (selectedV583LeftEmbed l r before F G N M B)) ↔ A = B := by
  constructor
  · intro h
    have ho := congrArg Prod.snd h
    change selectedContextEighteenWhiskerPlacement l r
        (selectedV583LeftEmbed l r before F G N M A) =
      selectedContextEighteenWhiskerPlacement l r
        (selectedV583LeftEmbed l r before F G N M B) at ho
    rw [selectedV583Left_observed l r before F G N M A,
      selectedV583Left_observed l r before F G N M B] at ho
    exact selectedV583RawValue_injective
      (selectedLocalEighteenInnerBracket l r M) ho
  · rintro rfl
    rfl

/-- Why direct unguarded inherited sources cannot be freely added:
the ORIGINAL old selected19 unit is an actual comparison. -/
theorem selectedV583Left_unguardedUnitOldNew
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N)) :
    selectedNineteenClass l r
        (.chain (.strict (.whiskerLeft before F G N)) (.inherited M)) =
      selectedNineteenClass l r (.inherited M) ∧
    selectedRawCongruentClass l r
        (.chain (.strict (.whiskerLeft before F G N)) (.inherited M)) =
      selectedRawCongruentClass l r (.inherited M) := by
  constructor
  · exact Quotient.sound ⟨SelectedLocalNineteen.unitPrepend M⟩
  · exact Quotient.sound
      ⟨SelectedRawCongruentNineteen.inherited
        (SelectedLocalNineteen.unitPrepend M)⟩

/-- The two witnesses in the unit equation are actually DIFFERENT
original raw dependent 18D constructor values. -/
theorem selectedV583Left_unguardedRawDistinct
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N)) :
    (SelectedContextualEighteen.chain
        (.strict (.whiskerLeft before F G N)) (.inherited M)) ≠
      (SelectedContextualEighteen.inherited M) := by
  intro h
  cases h

end SuppliedExactLeftFiber

#print axioms PentagonAdjoinedSixCell.SelectedV583GuardedFragment
#print axioms PentagonAdjoinedSixCell.selectedV583RawValue
#print axioms PentagonAdjoinedSixCell.selectedV583Pure_neSource
#print axioms PentagonAdjoinedSixCell.selectedV583Pure_neLeft
#print axioms PentagonAdjoinedSixCell.selectedV583Pure_neGuardedSource
#print axioms PentagonAdjoinedSixCell.selectedV583Pure_neGuardedLeft
#print axioms PentagonAdjoinedSixCell.selectedV583RawValue_injective
#print axioms PentagonAdjoinedSixCell.selectedV583LeftEmbed
#print axioms PentagonAdjoinedSixCell.selectedV583Left_observed
#print axioms PentagonAdjoinedSixCell.selectedV583Left_embedInjective
#print axioms PentagonAdjoinedSixCell.selectedV583Left_newClassEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV583Left_oldClassEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV583Left_oldComparison_iff
#print axioms PentagonAdjoinedSixCell.selectedV583Left_newComparison_iff
#print axioms PentagonAdjoinedSixCell.selectedV583Left_oldNewComparison_iff
#print axioms PentagonAdjoinedSixCell.selectedV583Left_fullV581Eq_iff
#print axioms PentagonAdjoinedSixCell.selectedV583Left_unguardedUnitOldNew
#print axioms PentagonAdjoinedSixCell.selectedV583Left_unguardedRawDistinct

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
