import KUOS.Architecture.QiWuxingGK5CHP77OriginalRoundTripCollisionReductionV5_93

/-!
Qi v5.94 — genuine SAME-FIBER original old18D strict padding families.

A source M:J->N of the original dependent five-constructor old18D Type
has arbitrarily many distinct original raw proof terms in the SAME J->N
fiber, obtained by adding original strict identities at either endpoint.
No unit law is imposed on the raw chain constructor.

* Each family preserves the true original v5.89 unit count.
* The entire ordered v5.92 dependent ORIGINAL unit-atom history,
  including all raw17D endpoints and before/F/G/C/after parameter
  values, is identical for all members of each family.
* A new independently defined strict-atom count of the ACTUAL v5.73
  inner-bracket tree increases by exactly the prefix/suffix length.
* Consequently each of the two Nat-indexed source maps is injective,
  even though its unit payload history is CONSTANT.
* For genuine one-unit left/right sources, two distinct 1-unit proofs
  live in the SAME raw J->N fiber, agree in typed payload history but
  have DIFFERENT v5.73 inner-bracket fingerprints.

This is a positive infinite-family history-observer obstruction, NOT
a same-bracket/different-raw collision. It neither constructs nor
refutes the unverified one-unit-source ambiguity from v5.93.

No source, original 19D generator, type, or quotient is modified;
no across-fiber gluing or WORLD/20D authority is asserted.
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

/-- Independently count the genuine original STRICT leaf labels
in the v5.73 nonassociative old18D inner-bracket observation,
while retaining all reverse and binary-chain syntactic positions. -/
def selectedV594InnerStrictCount :
    SelectedInheritedOldInnerBracket → Nat
  | .oldStrict => 1
  | .oldUnitLeft => 0
  | .oldUnitRight => 0
  | .oldReversed b => selectedV594InnerStrictCount b
  | .oldJoined a b =>
      selectedV594InnerStrictCount a + selectedV594InnerStrictCount b

/-- Original raw old18D construction using n genuinely typed
strict J identities on the LEFT. The raw endpoints remain J->N. -/
def selectedV594StrictPrefix (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {N : SelectedContextualSeventeen W l r H K}
    (J : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r J N) :
    Nat → SelectedLocalEighteen W l r J N
  | 0 => M
  | n + 1 =>
      .chain (.strict J) (selectedV594StrictPrefix l r J M n)

/-- Original raw old18D construction using n genuinely typed
strict N identities on the RIGHT, in the SAME J->N fiber. -/
def selectedV594StrictSuffix (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J : SelectedContextualSeventeen W l r H K}
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r J N) :
    Nat → SelectedLocalEighteen W l r J N
  | 0 => M
  | n + 1 =>
      .chain (selectedV594StrictSuffix l r N M n) (.strict N)

section GenuineIndexedSource

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable (J N : SelectedContextualSeventeen W l r H K)
variable (M : SelectedLocalEighteen W l r J N)

/-- Prefixing any number of original stricts does not add unit
constructors, for ANY original source, including unit-bearing ones. -/
theorem selectedV594Prefix_unitCount (n : Nat) :
    selectedV589OriginalUnitCount l r
        (selectedV594StrictPrefix l r J M n) =
      selectedV589OriginalUnitCount l r M := by
  induction n with
  | zero => rfl
  | succ n ih =>
      change 0 +
        selectedV589OriginalUnitCount l r
          (selectedV594StrictPrefix l r J M n) =
        selectedV589OriginalUnitCount l r M
      simpa only [Nat.zero_add] using ih

theorem selectedV594Suffix_unitCount (n : Nat) :
    selectedV589OriginalUnitCount l r
        (selectedV594StrictSuffix l r N M n) =
      selectedV589OriginalUnitCount l r M := by
  induction n with
  | zero => rfl
  | succ n ih =>
      change
        selectedV589OriginalUnitCount l r
          (selectedV594StrictSuffix l r N M n) + 0 =
        selectedV589OriginalUnitCount l r M
      simpa only [Nat.add_zero] using ih

/-- Complete typed original unit-atom payload history is unchanged.
This includes exact ORIGINAL source/target endpoints of all unit atoms. -/
theorem selectedV594Prefix_unitHistory (n : Nat) :
    selectedV592OriginalUnitHistory l r
        (selectedV594StrictPrefix l r J M n) =
      selectedV592OriginalUnitHistory l r M := by
  induction n with
  | zero => rfl
  | succ n ih =>
      change [] ++ selectedV592OriginalUnitHistory l r
          (selectedV594StrictPrefix l r J M n) =
        selectedV592OriginalUnitHistory l r M
      simpa only [List.nil_append] using ih

theorem selectedV594Suffix_unitHistory (n : Nat) :
    selectedV592OriginalUnitHistory l r
        (selectedV594StrictSuffix l r N M n) =
      selectedV592OriginalUnitHistory l r M := by
  induction n with
  | zero => rfl
  | succ n ih =>
      change selectedV592OriginalUnitHistory l r
          (selectedV594StrictSuffix l r N M n) ++ [] =
        selectedV592OriginalUnitHistory l r M
      simpa only [List.append_nil] using ih

/-- The actual original v5.73 inner-bracket fingerprint has a
strict-leaf count increasing precisely by prefix length n. -/
theorem selectedV594Prefix_innerStrictCount (n : Nat) :
    selectedV594InnerStrictCount
        (selectedLocalEighteenInnerBracket l r
          (selectedV594StrictPrefix l r J M n)) =
      n + selectedV594InnerStrictCount
        (selectedLocalEighteenInnerBracket l r M) := by
  induction n with
  | zero =>
      simpa only [selectedV594StrictPrefix, Nat.zero_add]
  | succ n ih =>
      change 1 + selectedV594InnerStrictCount
          (selectedLocalEighteenInnerBracket l r
            (selectedV594StrictPrefix l r J M n)) =
        (n + 1) +
          selectedV594InnerStrictCount
            (selectedLocalEighteenInnerBracket l r M)
      omega

theorem selectedV594Suffix_innerStrictCount (n : Nat) :
    selectedV594InnerStrictCount
        (selectedLocalEighteenInnerBracket l r
          (selectedV594StrictSuffix l r N M n)) =
      n + selectedV594InnerStrictCount
        (selectedLocalEighteenInnerBracket l r M) := by
  induction n with
  | zero =>
      simpa only [selectedV594StrictSuffix, Nat.zero_add]
  | succ n ih =>
      change selectedV594InnerStrictCount
          (selectedLocalEighteenInnerBracket l r
            (selectedV594StrictSuffix l r N M n)) + 1 =
        (n + 1) +
          selectedV594InnerStrictCount
            (selectedLocalEighteenInnerBracket l r M)
      omega

/-- The strict-count factor of the EXISTING bracket observer
separates all distinct prefix indices inside this one exact fiber.
No raw idempotence/unit law or quotient equality is invoked. -/
theorem selectedV594Prefix_injective :
    Function.Injective (fun n : Nat =>
      selectedV594StrictPrefix l r J M n) := by
  intro m n h
  have hc := congrArg
    (fun A : SelectedLocalEighteen W l r J N =>
      selectedV594InnerStrictCount
        (selectedLocalEighteenInnerBracket l r A)) h
  change selectedV594InnerStrictCount
      (selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J M m)) =
    selectedV594InnerStrictCount
      (selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J M n)) at hc
  rw [selectedV594Prefix_innerStrictCount l r J N M m,
    selectedV594Prefix_innerStrictCount l r J N M n] at hc
  omega

theorem selectedV594Suffix_injective :
    Function.Injective (fun n : Nat =>
      selectedV594StrictSuffix l r N M n) := by
  intro m n h
  have hc := congrArg
    (fun A : SelectedLocalEighteen W l r J N =>
      selectedV594InnerStrictCount
        (selectedLocalEighteenInnerBracket l r A)) h
  change selectedV594InnerStrictCount
      (selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N M m)) =
    selectedV594InnerStrictCount
      (selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N M n)) at hc
  rw [selectedV594Suffix_innerStrictCount l r J N M m,
    selectedV594Suffix_innerStrictCount l r J N M n] at hc
  omega

/-- For all distinct indices, FULL typed original unit payload
histories coincide even though original fingerprints differ and
the actual raw old18D Type values are unequal, IN THE SAME FIBER. -/
theorem selectedV594Prefix_observerGap
    (m n : Nat) (hne : m ≠ n) :
    selectedV592OriginalUnitHistory l r
        (selectedV594StrictPrefix l r J M m) =
      selectedV592OriginalUnitHistory l r
        (selectedV594StrictPrefix l r J M n) ∧
    selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J M m) ≠
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J M n) ∧
    selectedV594StrictPrefix l r J M m ≠
      selectedV594StrictPrefix l r J M n := by
  refine ⟨(selectedV594Prefix_unitHistory l r J N M m).trans
    (selectedV594Prefix_unitHistory l r J N M n).symm, ?_, ?_⟩
  · intro hbr
    have hc := congrArg selectedV594InnerStrictCount hbr
    rw [selectedV594Prefix_innerStrictCount l r J N M m,
      selectedV594Prefix_innerStrictCount l r J N M n] at hc
    exact hne (by omega)
  · intro hraw
    exact hne (selectedV594Prefix_injective l r J N M hraw)

theorem selectedV594Suffix_observerGap
    (m n : Nat) (hne : m ≠ n) :
    selectedV592OriginalUnitHistory l r
        (selectedV594StrictSuffix l r N M m) =
      selectedV592OriginalUnitHistory l r
        (selectedV594StrictSuffix l r N M n) ∧
    selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N M m) ≠
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N M n) ∧
    selectedV594StrictSuffix l r N M m ≠
      selectedV594StrictSuffix l r N M n := by
  refine ⟨(selectedV594Suffix_unitHistory l r J N M m).trans
    (selectedV594Suffix_unitHistory l r J N M n).symm, ?_, ?_⟩
  · intro hbr
    have hc := congrArg selectedV594InnerStrictCount hbr
    rw [selectedV594Suffix_innerStrictCount l r J N M m,
      selectedV594Suffix_innerStrictCount l r J N M n] at hc
    exact hne (by omega)
  · intro hraw
    exact hne (selectedV594Suffix_injective l r J N M hraw)

/-- Two independently chosen prefix/suffix indices share the
COMPLETE original typed unit payload history, with the fixed
source's raw17D endpoint indices preserved in both constructions. -/
theorem selectedV594PrefixSuffix_sameHistory (m n : Nat) :
    selectedV592OriginalUnitHistory l r
        (selectedV594StrictPrefix l r J M m) =
      selectedV592OriginalUnitHistory l r
        (selectedV594StrictSuffix l r N M n) :=
  (selectedV594Prefix_unitHistory l r J N M m).trans
    (selectedV594Suffix_unitHistory l r J N M n).symm

/-- One genuine source unit remains exactly one under arbitrary
strict prefix and suffix insertion; this is NOT sufficient to
create an equal-bracket/different-raw source collision. -/
theorem selectedV594OneUnitAllStrictPadding
    (hone : selectedV589OriginalUnitCount l r M = 1)
    (m n : Nat) :
    selectedV589OriginalUnitCount l r
        (selectedV594StrictPrefix l r J M m) = 1 ∧
    selectedV589OriginalUnitCount l r
        (selectedV594StrictSuffix l r N M n) = 1 := by
  exact ⟨(selectedV594Prefix_unitCount l r J N M m).trans hone,
    (selectedV594Suffix_unitCount l r J N M n).trans hone⟩

end GenuineIndexedSource

section ActualOriginalUnitParameters

variable (l r : W)
variable {w z : W}
variable {b c d e : PentagonAdjoinedSixCell W l r w z}
variable (before : SevenRewrite W l r b c)
variable (F G : ContextFrameEleven W l r c d)
variable {P Q : SelectedUnitalCompositionTwelve W l r
  (contextFramePack l r F) (contextFramePack l r G)}
variable (C : SelectedContextualThirteen W l r P Q)
variable (after : SevenRewrite W l r d e)

/-- Genuine ORIGINAL left-unit source: strict before versus strict
after form two actually different raw old18D J->N proofs with
exactly ONE original unit each and the SAME full original
unit parameter history. Their inner-bracket fingerprints DIFFER. -/
theorem selectedV594ActualLeftOneUnitStrictPlacementGap :
    let J := selectedSeventeenUnitPrependLeft l r before F G C after
    let N := selectedSeventeenUnitAppendLeft l r before F G C after
    let U := SelectedLocalEighteen.unitLeft before F G C after
    let A := selectedV594StrictPrefix l r J U 1
    let B := selectedV594StrictSuffix l r N U 1
    selectedV592OriginalUnitHistory l r A =
      selectedV592OriginalUnitHistory l r B ∧
    selectedLocalEighteenInnerBracket l r A ≠
      selectedLocalEighteenInnerBracket l r B ∧
    selectedV589OriginalUnitCount l r A = 1 ∧
    selectedV589OriginalUnitCount l r B = 1 ∧
    A ≠ B := by
  dsimp only
  have hh := selectedV594PrefixSuffix_sameHistory l r
    (selectedSeventeenUnitPrependLeft l r before F G C after)
    (selectedSeventeenUnitAppendLeft l r before F G C after)
    (SelectedLocalEighteen.unitLeft before F G C after) 1 1
  have hb :
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r
          (selectedSeventeenUnitPrependLeft l r before F G C after)
          (SelectedLocalEighteen.unitLeft before F G C after) 1) ≠
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r
          (selectedSeventeenUnitAppendLeft l r before F G C after)
          (SelectedLocalEighteen.unitLeft before F G C after) 1) := by
    change SelectedInheritedOldInnerBracket.oldJoined
        .oldStrict .oldUnitLeft ≠
      .oldJoined .oldUnitLeft .oldStrict
    decide
  refine ⟨hh, hb, ?_, ?_, ?_⟩
  · rfl
  · rfl
  · intro heq
    exact hb (congrArg (selectedLocalEighteenInnerBracket l r) heq)

/-- The independent genuine ORIGINAL right-unit source exhibits
the same one-unit same-fiber history-observation gap. -/
theorem selectedV594ActualRightOneUnitStrictPlacementGap :
    let J := selectedSeventeenUnitPrependRight l r before F G C after
    let N := selectedSeventeenUnitAppendRight l r before F G C after
    let U := SelectedLocalEighteen.unitRight before F G C after
    let A := selectedV594StrictPrefix l r J U 1
    let B := selectedV594StrictSuffix l r N U 1
    selectedV592OriginalUnitHistory l r A =
      selectedV592OriginalUnitHistory l r B ∧
    selectedLocalEighteenInnerBracket l r A ≠
      selectedLocalEighteenInnerBracket l r B ∧
    selectedV589OriginalUnitCount l r A = 1 ∧
    selectedV589OriginalUnitCount l r B = 1 ∧
    A ≠ B := by
  dsimp only
  have hh := selectedV594PrefixSuffix_sameHistory l r
    (selectedSeventeenUnitPrependRight l r before F G C after)
    (selectedSeventeenUnitAppendRight l r before F G C after)
    (SelectedLocalEighteen.unitRight before F G C after) 1 1
  have hb :
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r
          (selectedSeventeenUnitPrependRight l r before F G C after)
          (SelectedLocalEighteen.unitRight before F G C after) 1) ≠
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r
          (selectedSeventeenUnitAppendRight l r before F G C after)
          (SelectedLocalEighteen.unitRight before F G C after) 1) := by
    change SelectedInheritedOldInnerBracket.oldJoined
        .oldStrict .oldUnitRight ≠
      .oldJoined .oldUnitRight .oldStrict
    decide
  refine ⟨hh, hb, ?_, ?_, ?_⟩
  · rfl
  · rfl
  · intro heq
    exact hb (congrArg (selectedLocalEighteenInnerBracket l r) heq)

end ActualOriginalUnitParameters

#print axioms PentagonAdjoinedSixCell.selectedV594InnerStrictCount
#print axioms PentagonAdjoinedSixCell.selectedV594StrictPrefix
#print axioms PentagonAdjoinedSixCell.selectedV594StrictSuffix
#print axioms PentagonAdjoinedSixCell.selectedV594Prefix_unitCount
#print axioms PentagonAdjoinedSixCell.selectedV594Suffix_unitCount
#print axioms PentagonAdjoinedSixCell.selectedV594Prefix_unitHistory
#print axioms PentagonAdjoinedSixCell.selectedV594Suffix_unitHistory
#print axioms PentagonAdjoinedSixCell.selectedV594Prefix_innerStrictCount
#print axioms PentagonAdjoinedSixCell.selectedV594Suffix_innerStrictCount
#print axioms PentagonAdjoinedSixCell.selectedV594Prefix_injective
#print axioms PentagonAdjoinedSixCell.selectedV594Suffix_injective
#print axioms PentagonAdjoinedSixCell.selectedV594Prefix_observerGap
#print axioms PentagonAdjoinedSixCell.selectedV594Suffix_observerGap
#print axioms PentagonAdjoinedSixCell.selectedV594PrefixSuffix_sameHistory
#print axioms PentagonAdjoinedSixCell.selectedV594OneUnitAllStrictPadding
#print axioms PentagonAdjoinedSixCell.selectedV594ActualLeftOneUnitStrictPlacementGap
#print axioms PentagonAdjoinedSixCell.selectedV594ActualRightOneUnitStrictPlacementGap

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
