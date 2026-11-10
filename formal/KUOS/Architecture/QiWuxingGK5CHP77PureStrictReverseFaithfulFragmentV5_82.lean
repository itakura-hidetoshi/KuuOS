import KUOS.Architecture.QiWuxingGK5CHP77WhiskerReversePlacementResidualV5_81

/-!
Qi v5.82 — conditional faithful classification on the ORIGINAL
strict/reverse/raw-chain endomorphism fragment of genuine dependent
contextual18D evidence, using the separately descended Qi v5.81
whisker-placement tree.

For each GIVEN genuine 17D endpoint N, a free three-constructor
presentation generates ACTUAL original contextual18D Type values
of type N→N. No raw inherited old18D source, left/right whisker,
or heterogeneous endpoint is added to THIS fragment.

The original five-generator selected19 comparison and the independent
seven-generator raw-congruence selected19 comparison have exactly
the same equality kernel on this fragment: each comparison exists
iff the free strict/reverse/raw-chain syntax is definitionally equal.
The actual new and old quotient CLASS mappings are injective on
this fragment. The complete v5.81 quotient observation, including
v5.80's full two Nat-indexed infinite towers and all independently
verified earlier coordinates, reflects equality for these embedded
genuine proof values.

This is conditional faithfulness on one explicit presentation, NOT
an injectivity result for all contextual18D proof values, not an
equivalence of the ORIGINAL old/new 19D comparison Types, and not
global quotient classification, arbitrary J→N inhabitance or
cross-WORLD/20D gluing. Fixed Lean/mathlib, root107, protected
#1558 and all historical definitions remain unmodified.
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

/-- A freely generated LOCAL presentation, with no inherited or whisker
constructors. This is not an equality or replacement of original 18D. -/
inductive SelectedPureStrictReverseTree : Type where
  | strict : SelectedPureStrictReverseTree
  | reversed : SelectedPureStrictReverseTree → SelectedPureStrictReverseTree
  | joined : SelectedPureStrictReverseTree →
      SelectedPureStrictReverseTree → SelectedPureStrictReverseTree
  deriving DecidableEq, Repr

/-- Independent syntax interpretation in the Qi v5.81 free tree.
Unlike the original 19D unit rule, no raw strict is removed here,
because no genuine inherited source leaf occurs in this fragment. -/
def selectedPureStrictReverseRawValue :
    SelectedPureStrictReverseTree → SelectedWhiskerPlacementTree
  | .strict => .strict
  | .reversed A => .reversed (selectedPureStrictReverseRawValue A)
  | .joined A B =>
      .joined (selectedPureStrictReverseRawValue A)
        (selectedPureStrictReverseRawValue B)

/-- In the pure strict fragment, inherited-source cancellation
cannot fire, even under an arbitrary raw reversed/joined subtree. -/
theorem selectedPureStrictReverseRawValue_join
    (A B : SelectedPureStrictReverseTree) :
    selectedWhiskerPlacementJoin
        (selectedPureStrictReverseRawValue A)
        (selectedPureStrictReverseRawValue B) =
      .joined (selectedPureStrictReverseRawValue A)
        (selectedPureStrictReverseRawValue B) := by
  cases A <;> cases B <;> rfl

/-- A total auxiliary decoder. The arbitrary values on source/whisker
constructors are NOT claims of an inverse on full contextual18D. -/
def selectedPureStrictReverseDecode :
    SelectedWhiskerPlacementTree → SelectedPureStrictReverseTree
  | .strict => .strict
  | .source _ => .strict
  | .left _ => .strict
  | .right _ => .strict
  | .reversed A => .reversed (selectedPureStrictReverseDecode A)
  | .joined A B =>
      .joined (selectedPureStrictReverseDecode A)
        (selectedPureStrictReverseDecode B)

/-- This decoder is a left inverse ONLY on the pure strict/reverse
fragment's explicitly interpreted free trees. -/
theorem selectedPureStrictReverseDecode_value
    (A : SelectedPureStrictReverseTree) :
    selectedPureStrictReverseDecode
        (selectedPureStrictReverseRawValue A) = A := by
  induction A with
  | strict => rfl
  | reversed A ih =>
      exact congrArg SelectedPureStrictReverseTree.reversed ih
  | joined A B ih ih' =>
      exact congrArg₂ SelectedPureStrictReverseTree.joined ih ih'

theorem selectedPureStrictReverseRawValue_injective :
    Function.Injective selectedPureStrictReverseRawValue := by
  intro A B h
  have hd := congrArg selectedPureStrictReverseDecode h
  simpa only [selectedPureStrictReverseDecode_value] using hd

section GenuineExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}

/-- Every local term is embedded in ACTUAL original dependent
contextual18D evidence with endpoints N→N, not merely a proxy tree. -/
def selectedPureStrictReverseEmbed
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedPureStrictReverseTree →
      SelectedContextualEighteen W l r N N
  | .strict => .strict N
  | .reversed A => .reverse (selectedPureStrictReverseEmbed N A)
  | .joined A B =>
      .chain (selectedPureStrictReverseEmbed N A)
        (selectedPureStrictReverseEmbed N B)

/-- Verify that the already-certified v5.81 observer on the ACTUAL
dependent Type18D proof agrees with the independently defined free
syntax interpretation. Source-unit cancellation does not fire. -/
theorem selectedPureStrictReverse_observed
    (N : SelectedContextualSeventeen W l r H K)
    (A : SelectedPureStrictReverseTree) :
    selectedContextEighteenWhiskerPlacement l r
        (selectedPureStrictReverseEmbed N A) =
      selectedPureStrictReverseRawValue A := by
  induction A with
  | strict => rfl
  | reversed A ih =>
      exact congrArg SelectedWhiskerPlacementTree.reversed ih
  | joined A B ih ih' =>
      change selectedWhiskerPlacementJoin
          (selectedContextEighteenWhiskerPlacement l r
            (selectedPureStrictReverseEmbed N A))
          (selectedContextEighteenWhiskerPlacement l r
            (selectedPureStrictReverseEmbed N B)) =
        SelectedWhiskerPlacementTree.joined
          (selectedPureStrictReverseRawValue A)
          (selectedPureStrictReverseRawValue B)
      rw [ih, ih', selectedPureStrictReverseRawValue_join]

/-- Reflection of equality of TRUE original 18D proof values, only
for the explicitly generated pure strict endomorphism fragment. -/
theorem selectedPureStrictReverse_embedInjective
    (N : SelectedContextualSeventeen W l r H K) :
    Function.Injective (selectedPureStrictReverseEmbed N) := by
  intro A B h
  have ho := congrArg
    (selectedContextEighteenWhiskerPlacement l r) h
  rw [selectedPureStrictReverse_observed l r N A,
    selectedPureStrictReverse_observed l r N B] at ho
  exact selectedPureStrictReverseRawValue_injective ho

/-- The genuine NEW seven-generator quotient class equals another
embedded pure class IFF the original local syntactic values agree. -/
theorem selectedPureStrictReverse_newClassEq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedPureStrictReverseTree) :
    selectedRawCongruentClass l r
        (selectedPureStrictReverseEmbed N A) =
      selectedRawCongruentClass l r
        (selectedPureStrictReverseEmbed N B) ↔ A = B := by
  constructor
  · intro h
    have ho := congrArg
      (selectedRawCongruentWhiskerPlacementOnQuotient l r N N) h
    change selectedContextEighteenWhiskerPlacement l r
        (selectedPureStrictReverseEmbed N A) =
      selectedContextEighteenWhiskerPlacement l r
        (selectedPureStrictReverseEmbed N B) at ho
    rw [selectedPureStrictReverse_observed l r N A,
      selectedPureStrictReverse_observed l r N B] at ho
    exact selectedPureStrictReverseRawValue_injective ho
  · rintro rfl
    rfl

/-- The independently defined genuine OLD five-generator quotient
obeys the same exact kernel on this pure raw fragment. -/
theorem selectedPureStrictReverse_oldClassEq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedPureStrictReverseTree) :
    selectedNineteenClass l r
        (selectedPureStrictReverseEmbed N A) =
      selectedNineteenClass l r
        (selectedPureStrictReverseEmbed N B) ↔ A = B := by
  constructor
  · intro h
    have ho := congrArg
      (selectedNineteenWhiskerPlacementOnQuotient l r N N) h
    change selectedContextEighteenWhiskerPlacement l r
        (selectedPureStrictReverseEmbed N A) =
      selectedContextEighteenWhiskerPlacement l r
        (selectedPureStrictReverseEmbed N B) at ho
    rw [selectedPureStrictReverse_observed l r N A,
      selectedPureStrictReverse_observed l r N B] at ho
    exact selectedPureStrictReverseRawValue_injective ho
  · rintro rfl
    rfl

theorem selectedPureStrictReverse_newClassesInjective
    (N : SelectedContextualSeventeen W l r H K) :
    Function.Injective
      (fun A : SelectedPureStrictReverseTree =>
        selectedRawCongruentClass l r
          (selectedPureStrictReverseEmbed N A)) := by
  intro A B h
  exact (selectedPureStrictReverse_newClassEq_iff l r N A B).mp h

theorem selectedPureStrictReverse_oldClassesInjective
    (N : SelectedContextualSeventeen W l r H K) :
    Function.Injective
      (fun A : SelectedPureStrictReverseTree =>
        selectedNineteenClass l r
          (selectedPureStrictReverseEmbed N A)) := by
  intro A B h
  exact (selectedPureStrictReverse_oldClassEq_iff l r N A B).mp h

/-- In the genuine selected19 Type-valued OLD comparison, the local
strict fragment is classified by literal free syntax equality. -/
theorem selectedPureStrictReverse_oldComparison_iff
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedPureStrictReverseTree) :
    Nonempty (SelectedLocalNineteen W l r
      (selectedPureStrictReverseEmbed N A)
      (selectedPureStrictReverseEmbed N B)) ↔ A = B := by
  constructor
  · rintro ⟨h⟩
    exact (selectedPureStrictReverse_oldClassEq_iff l r N A B).mp
      (Quotient.sound ⟨h⟩)
  · rintro rfl
    exact ⟨.strict (selectedPureStrictReverseEmbed N A)⟩

/-- In the separate NEW selected19 comparison Type, the identical
pure fragment is also classified by free syntax equality. -/
theorem selectedPureStrictReverse_newComparison_iff
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedPureStrictReverseTree) :
    Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedPureStrictReverseEmbed N A)
      (selectedPureStrictReverseEmbed N B)) ↔ A = B := by
  constructor
  · rintro ⟨h⟩
    exact (selectedPureStrictReverse_newClassEq_iff l r N A B).mp
      (Quotient.sound ⟨h⟩)
  · rintro rfl
    exact ⟨.strict (selectedPureStrictReverseEmbed N A)⟩

/-- The added raw-congruence generators do NOT collapse any new class
inside the embedded pure strict/reverse/chain subpresentation.
This does NOT identify the old and new Type19D comparison families. -/
theorem selectedPureStrictReverse_oldNewComparison_iff
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedPureStrictReverseTree) :
    Nonempty (SelectedLocalNineteen W l r
      (selectedPureStrictReverseEmbed N A)
      (selectedPureStrictReverseEmbed N B)) ↔
    Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedPureStrictReverseEmbed N A)
      (selectedPureStrictReverseEmbed N B)) := by
  constructor
  · rintro ⟨h⟩
    exact ⟨.inherited h⟩
  · intro h
    exact (selectedPureStrictReverse_oldComparison_iff l r N A B).mpr
      ((selectedPureStrictReverse_newComparison_iff l r N A B).mp h)

/-- Exactly on the pure fragment, the old-to-new quotient projection
reflects equality of its concrete original dependent class images. -/
theorem selectedPureStrictReverse_oldNewClassEq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedPureStrictReverseTree) :
    (selectedNineteenClass l r
        (selectedPureStrictReverseEmbed N A) =
      selectedNineteenClass l r
        (selectedPureStrictReverseEmbed N B)) ↔
    (selectedRawCongruentClass l r
        (selectedPureStrictReverseEmbed N A) =
      selectedRawCongruentClass l r
        (selectedPureStrictReverseEmbed N B)) := by
  exact (selectedPureStrictReverse_oldClassEq_iff l r N A B).trans
    (selectedPureStrictReverse_newClassEq_iff l r N A B).symm

end GenuineExactFiber

/-- Accumulated v5.81 FULL quotient observation, including every old
v5.80 coordinate plus independently descended whisker-placement tree.
This is not a global faithful invariant on arbitrary original proofs. -/
abbrev SelectedFullV581QuotientObservationValue :=
  SelectedFullV580QuotientObservationValue × SelectedWhiskerPlacementTree

section FullObservation

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}

/-- TRUE quotient map: v5.80 complete new quotient observation
paired with v5.81 independently quotient-descended local tree. -/
def selectedRawCongruentFullV581QuotientObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedFullV581QuotientObservationValue :=
  fun q =>
    (selectedRawCongruentFullV580QuotientObservation l r J N q,
      selectedRawCongruentWhiskerPlacementOnQuotient l r J N q)

/-- The full v5.81 observation DOES reflect equality of genuine
quotient class images on the embedded pure strict-only subpresentation. -/
theorem selectedPureStrictReverse_fullV581Eq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedPureStrictReverseTree) :
    selectedRawCongruentFullV581QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedPureStrictReverseEmbed N A)) =
      selectedRawCongruentFullV581QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedPureStrictReverseEmbed N B)) ↔ A = B := by
  constructor
  · intro h
    have ho := congrArg Prod.snd h
    change selectedContextEighteenWhiskerPlacement l r
        (selectedPureStrictReverseEmbed N A) =
      selectedContextEighteenWhiskerPlacement l r
        (selectedPureStrictReverseEmbed N B) at ho
    rw [selectedPureStrictReverse_observed l r N A,
      selectedPureStrictReverse_observed l r N B] at ho
    exact selectedPureStrictReverseRawValue_injective ho
  · rintro rfl
    rfl

theorem selectedPureStrictReverse_fullV581Injective
    (N : SelectedContextualSeventeen W l r H K) :
    Function.Injective
      (fun A : SelectedPureStrictReverseTree =>
        selectedRawCongruentFullV581QuotientObservation l r N N
          (selectedRawCongruentClass l r
            (selectedPureStrictReverseEmbed N A))) := by
  intro A B h
  exact (selectedPureStrictReverse_fullV581Eq_iff l r N A B).mp h

end FullObservation

#print axioms PentagonAdjoinedSixCell.SelectedPureStrictReverseTree
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverseRawValue
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverseRawValue_join
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverseDecode
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverseDecode_value
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverseRawValue_injective
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverseEmbed
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverse_observed
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverse_embedInjective
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverse_newClassEq_iff
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverse_oldClassEq_iff
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverse_newClassesInjective
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverse_oldClassesInjective
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverse_oldComparison_iff
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverse_newComparison_iff
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverse_oldNewComparison_iff
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverse_oldNewClassEq_iff
#print axioms PentagonAdjoinedSixCell.SelectedFullV581QuotientObservationValue
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullV581QuotientObservation
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverse_fullV581Eq_iff
#print axioms PentagonAdjoinedSixCell.selectedPureStrictReverse_fullV581Injective

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
