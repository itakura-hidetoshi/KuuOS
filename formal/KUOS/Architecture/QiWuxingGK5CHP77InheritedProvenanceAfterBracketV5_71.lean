import KUOS.Architecture.QiWuxingGK5CHP77UnitReducedBracketShapeResidualV5_70

/-!
Qi v5.71 — genuine strict/inherited provenance obstruction AFTER the
complete nine-observer, double infinite tower, ordered run-list, AND
unit-reduced nonassociative bracket observation.

The original selected19 unit-pasting generators insert/delete raw
strict identities next to an ORIGINAL inherited old18D proof. Thus a
raw strict-node count cannot descend even to the new seven-generator
quotient. In contrast, the number of genuine inherited old18D leaves
is preserved by all FIVE old and all SEVEN new comparison generators
and descends separately to both original quotients. Whiskering and
raw reverse/chain act by the original dependent proof constructors;
no independent 18D inhabitant is invented.

An explicit, genuinely inhabited 17D endomorphism fiber has:
  A = reverse (strict N)
  B = reverse (inherited (SelectedLocalEighteen.strict N)).
The full v5.70 observer INCLUDING the unit-reduced bracket tree has
exactly the same value for A and B, but the invariant inherited-leaf
counts are 0 and 1. Right pasting after any ACTUALLY SUPPLIED original
M:J->N yields a same-fiber noninjectivity and no decoder.

The invariant records only the presence of inherited source leaves,
not equality of arbitrary old18D evidence nor the whole strict history.
It proves neither global completeness nor 20D gluing. Old Type18D,
old/new Type19 independence, public root107, pinned Lean/mathlib,
and validation-only PR #1558 are unchanged.
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

/-- Count actual ORIGINAL inherited old18D source leaves in genuine
dependent raw18D syntax. Strict units do not contribute. -/
def selectedContextEighteenInheritedLeafCount (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) : Nat :=
  match M with
  | .inherited _ => 1
  | .whiskerLeft _ _ _ A =>
      selectedContextEighteenInheritedLeafCount l r A
  | .whiskerRight _ _ A _ =>
      selectedContextEighteenInheritedLeafCount l r A
  | .strict _ => 0
  | .reverse A => selectedContextEighteenInheritedLeafCount l r A
  | .chain A B =>
      selectedContextEighteenInheritedLeafCount l r A +
        selectedContextEighteenInheritedLeafCount l r B

/-- A deliberately RAW strict-node observer. This will be proved
NOT compatible with original selected19 unit-pasting comparisons. -/
def selectedContextEighteenStrictNodeCount (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) : Nat :=
  match M with
  | .inherited _ => 0
  | .whiskerLeft _ _ _ A =>
      selectedContextEighteenStrictNodeCount l r A
  | .whiskerRight _ _ A _ =>
      selectedContextEighteenStrictNodeCount l r A
  | .strict _ => 1
  | .reverse A => selectedContextEighteenStrictNodeCount l r A
  | .chain A B =>
      selectedContextEighteenStrictNodeCount l r A +
        selectedContextEighteenStrictNodeCount l r B

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- The old unit insertions are neutral for inherited LEAVES,
although they change the count of strict raw nodes. -/
theorem selectedLocalNineteen_preservesInheritedLeafCount
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenInheritedLeafCount l r M =
      selectedContextEighteenInheritedLeafCount l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- Check ALL SEVEN independent new typed19 comparison constructors,
including genuine raw reverse and both raw chain contexts. -/
theorem selectedRawCongruent_preservesInheritedLeafCount
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenInheritedLeafCount l r M =
      selectedContextEighteenInheritedLeafCount l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesInheritedLeafCount l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih => exact ih
  | rawChainRight A X ih =>
      exact congrArg
        (fun n : Nat => n + selectedContextEighteenInheritedLeafCount l r X) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun n : Nat => selectedContextEighteenInheritedLeafCount l r X + n) ih

/-- A new well-defined observable ON THE ACTUAL SEVEN-GENERATOR QUOTIENT. -/
def selectedRawCongruentInheritedLeafCountOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenInheritedLeafCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesInheritedLeafCount l r A)

theorem selectedRawCongruentInheritedLeafCount_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentInheritedLeafCountOnQuotient l r J N
      (selectedRawCongruentClass l r M) =
        selectedContextEighteenInheritedLeafCount l r M := rfl

/-- The OLD quotient has its own independent descent. -/
def selectedNineteenInheritedLeafCountOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenInheritedLeafCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesInheritedLeafCount l r A)

theorem selectedInheritedLeafCount_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentInheritedLeafCountOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenInheritedLeafCountOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Strict raw node count changes under a GENUINE original old19
comparison; it therefore must NOT be promoted as a quotient invariant. -/
theorem selectedStrictNodeCount_unitPrependDifferent
    (M : SelectedLocalEighteen W l r J N) :
    selectedContextEighteenStrictNodeCount l r
        (SelectedContextualEighteen.chain
          (.strict J) (.inherited M)) ≠
      selectedContextEighteenStrictNodeCount l r
        (SelectedContextualEighteen.inherited M) := by
  decide

/-- Original unitPrepend comparison forbids even the NEW quotient
from decoding the raw strict-node count. -/
theorem selectedStrictNodeCount_noNewQuotientDescent
    (M : SelectedLocalEighteen W l r J N) :
    ¬ ∃ decode : Quotient (selectedRawCongruentSetoid l r J N) → Nat,
      ∀ X : SelectedContextualEighteen W l r J N,
        decode (selectedRawCongruentClass l r X) =
          selectedContextEighteenStrictNodeCount l r X := by
  rintro ⟨decode, h⟩
  let A : SelectedContextualEighteen W l r J N :=
    .chain (.strict J) (.inherited M)
  let B : SelectedContextualEighteen W l r J N := .inherited M
  have hclass : selectedRawCongruentClass l r A =
      selectedRawCongruentClass l r B :=
    Quotient.sound ⟨.inherited (.unitPrepend M)⟩
  have hcount :
      selectedContextEighteenStrictNodeCount l r A =
        selectedContextEighteenStrictNodeCount l r B := by
    calc
      _ = decode (selectedRawCongruentClass l r A) := (h A).symm
      _ = decode (selectedRawCongruentClass l r B) :=
        congrArg decode hclass
      _ = _ := h B
  exact (selectedStrictNodeCount_unitPrependDifferent l r M) hcount

/-- A genuine raw-reverse loop over the strict 18D identity. -/
def selectedProvenanceStrictSpine
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (.strict N)

/-- A genuine raw-reverse loop over an inherited ORIGINAL local18D
strict identity, not an invented proof of arbitrary heterogeneous endpoints. -/
def selectedProvenanceInheritedSpine
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (.inherited (SelectedLocalEighteen.strict N))

theorem selectedProvenance_strictValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedLeafCount l r
        (selectedProvenanceStrictSpine l r N) = 0 := rfl

theorem selectedProvenance_inheritedValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedLeafCount l r
        (selectedProvenanceInheritedSpine l r N) = 1 := rfl

theorem selectedProvenance_spineCountDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedLeafCount l r
        (selectedProvenanceStrictSpine l r N) ≠
      selectedContextEighteenInheritedLeafCount l r
        (selectedProvenanceInheritedSpine l r N) := by
  decide

/-- Both witnesses reduce to the SAME unary reversed unit bracket. -/
theorem selectedProvenance_spineBracketEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenUnitReducedBracket l r
        (selectedProvenanceStrictSpine l r N) =
      selectedContextEighteenUnitReducedBracket l r
        (selectedProvenanceInheritedSpine l r N) := rfl

/-- Same nine observers, entire ancestor tower, entire reverse-run
tower and FULL ORDERED raw-run list, not a finite truncation. -/
theorem selectedProvenance_spineFullObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentFullDoubleOrderedObservation l r N N
        (selectedRawCongruentClass l r
          (selectedProvenanceStrictSpine l r N)) =
      selectedRawCongruentFullDoubleOrderedObservation l r N N
        (selectedRawCongruentClass l r
          (selectedProvenanceInheritedSpine l r N)) := by
  rfl

/-- Exact composite of the previous COMPLETE observer with v5.70's
separately descended nonassociative unit-reduced bracket observer. -/
abbrev SelectedFullDoubleOrderedBracketValue :=
  ((((selectedRawNineObservationValue × (Nat → Nat)) ×
      (Nat → Nat)) × List Nat) × SelectedRawUnitReducedBracket)

def selectedRawCongruentFullDoubleOrderedBracketObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedFullDoubleOrderedBracketValue :=
  fun q => (selectedRawCongruentFullDoubleOrderedObservation l r J N q,
    selectedRawCongruentUnitReducedBracketOnQuotient l r J N q)

theorem selectedProvenance_spineJointObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentFullDoubleOrderedBracketObservation l r N N
        (selectedRawCongruentClass l r
          (selectedProvenanceStrictSpine l r N)) =
      selectedRawCongruentFullDoubleOrderedBracketObservation l r N N
        (selectedRawCongruentClass l r
          (selectedProvenanceInheritedSpine l r N)) := by
  exact Prod.ext
    (selectedProvenance_spineFullObservedEq l r N)
    (selectedProvenance_spineBracketEq l r N)

/-- Even the true new7 quotient classes differ, certified by
independent inherited-leaf descent rather than by raw syntax alone. -/
theorem selectedProvenance_spineClassDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentClass l r (selectedProvenanceStrictSpine l r N) ≠
      selectedRawCongruentClass l r (selectedProvenanceInheritedSpine l r N) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentInheritedLeafCountOnQuotient l r N N) h
  change selectedContextEighteenInheritedLeafCount l r
      (selectedProvenanceStrictSpine l r N) =
    selectedContextEighteenInheritedLeafCount l r
      (selectedProvenanceInheritedSpine l r N) at hc
  exact (selectedProvenance_spineCountDistinct l r N) hc

theorem selectedProvenance_spineNoComparison
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedProvenanceStrictSpine l r N)
      (selectedProvenanceInheritedSpine l r N)) := by
  rintro ⟨A⟩
  exact (selectedProvenance_spineClassDistinct l r N)
    (Quotient.sound ⟨A⟩)

/-- The following conditional transport uses a PROVIDED genuine
original dependent M:J->N, not arbitrary existence of source fibers. -/
def selectedProvenanceFiberStrict
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedProvenanceStrictSpine l r N)

def selectedProvenanceFiberInherited
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedProvenanceInheritedSpine l r N)

theorem selectedProvenanceFiber_countDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenInheritedLeafCount l r
        (selectedProvenanceFiberStrict l r M) ≠
      selectedContextEighteenInheritedLeafCount l r
        (selectedProvenanceFiberInherited l r M) := by
  change selectedContextEighteenInheritedLeafCount l r M + 0 ≠
    selectedContextEighteenInheritedLeafCount l r M + 1
  exact Nat.ne_of_lt (Nat.lt_succ_self _)

/-- The common source prefix contributes the same raw observer data
to both genuinely typed same-fiber suffixes. -/
theorem selectedProvenanceFiber_jointObservedEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentFullDoubleOrderedBracketObservation l r J N
        (selectedRawCongruentClass l r (selectedProvenanceFiberStrict l r M)) =
      selectedRawCongruentFullDoubleOrderedBracketObservation l r J N
        (selectedRawCongruentClass l r
          (selectedProvenanceFiberInherited l r M)) := by
  rfl

theorem selectedProvenanceFiber_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r (selectedProvenanceFiberStrict l r M) ≠
      selectedRawCongruentClass l r (selectedProvenanceFiberInherited l r M) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentInheritedLeafCountOnQuotient l r J N) h
  change selectedContextEighteenInheritedLeafCount l r
      (selectedProvenanceFiberStrict l r M) =
    selectedContextEighteenInheritedLeafCount l r
      (selectedProvenanceFiberInherited l r M) at hc
  exact (selectedProvenanceFiber_countDistinct l r M) hc

theorem selectedFullDoubleOrderedBracket_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedRawCongruentFullDoubleOrderedBracketObservation l r J N) := by
  intro hinj
  exact (selectedProvenanceFiber_classDistinct l r M)
    (hinj (selectedProvenanceFiber_jointObservedEq l r M))

theorem selectedFullDoubleOrderedBracket_noInheritedDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode : SelectedFullDoubleOrderedBracketValue → Nat,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentFullDoubleOrderedBracketObservation l r J N q) =
          selectedRawCongruentInheritedLeafCountOnQuotient l r J N q := by
  rintro ⟨decode, h⟩
  have hc :
      selectedRawCongruentInheritedLeafCountOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedProvenanceFiberStrict l r M)) =
        selectedRawCongruentInheritedLeafCountOnQuotient l r J N
          (selectedRawCongruentClass l r
            (selectedProvenanceFiberInherited l r M)) := by
    calc
      _ = decode (selectedRawCongruentFullDoubleOrderedBracketObservation l r J N
            (selectedRawCongruentClass l r (selectedProvenanceFiberStrict l r M))) :=
        (h _).symm
      _ = decode (selectedRawCongruentFullDoubleOrderedBracketObservation l r J N
            (selectedRawCongruentClass l r
              (selectedProvenanceFiberInherited l r M))) :=
        congrArg decode (selectedProvenanceFiber_jointObservedEq l r M)
      _ = _ := h _
  change selectedContextEighteenInheritedLeafCount l r
      (selectedProvenanceFiberStrict l r M) =
    selectedContextEighteenInheritedLeafCount l r
      (selectedProvenanceFiberInherited l r M) at hc
  exact (selectedProvenanceFiber_countDistinct l r M) hc

theorem selectedFullDoubleOrderedBracket_noClassDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode : SelectedFullDoubleOrderedBracketValue →
        Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentFullDoubleOrderedBracketObservation l r J N q) =
          q := by
  rintro ⟨decode, h⟩
  apply selectedFullDoubleOrderedBracket_notInjective l r M
  intro a b hab
  calc
    a = decode (selectedRawCongruentFullDoubleOrderedBracketObservation l r J N a) :=
      (h a).symm
    _ = decode (selectedRawCongruentFullDoubleOrderedBracketObservation l r J N b) :=
      congrArg decode hab
    _ = b := h b

theorem selectedFullDoubleOrderedBracket_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentFullDoubleOrderedBracketObservation l r J J) :=
  selectedFullDoubleOrderedBracket_notInjective l r (.strict J)

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenInheritedLeafCount
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenStrictNodeCount
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesInheritedLeafCount
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesInheritedLeafCount
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentInheritedLeafCountOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentInheritedLeafCount_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenInheritedLeafCountOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedInheritedLeafCount_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedStrictNodeCount_unitPrependDifferent
#print axioms PentagonAdjoinedSixCell.selectedStrictNodeCount_noNewQuotientDescent
#print axioms PentagonAdjoinedSixCell.selectedProvenanceStrictSpine
#print axioms PentagonAdjoinedSixCell.selectedProvenanceInheritedSpine
#print axioms PentagonAdjoinedSixCell.selectedProvenance_strictValue
#print axioms PentagonAdjoinedSixCell.selectedProvenance_inheritedValue
#print axioms PentagonAdjoinedSixCell.selectedProvenance_spineCountDistinct
#print axioms PentagonAdjoinedSixCell.selectedProvenance_spineBracketEq
#print axioms PentagonAdjoinedSixCell.selectedProvenance_spineFullObservedEq
#print axioms PentagonAdjoinedSixCell.SelectedFullDoubleOrderedBracketValue
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullDoubleOrderedBracketObservation
#print axioms PentagonAdjoinedSixCell.selectedProvenance_spineJointObservedEq
#print axioms PentagonAdjoinedSixCell.selectedProvenance_spineClassDistinct
#print axioms PentagonAdjoinedSixCell.selectedProvenance_spineNoComparison
#print axioms PentagonAdjoinedSixCell.selectedProvenanceFiberStrict
#print axioms PentagonAdjoinedSixCell.selectedProvenanceFiberInherited
#print axioms PentagonAdjoinedSixCell.selectedProvenanceFiber_countDistinct
#print axioms PentagonAdjoinedSixCell.selectedProvenanceFiber_jointObservedEq
#print axioms PentagonAdjoinedSixCell.selectedProvenanceFiber_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedFullDoubleOrderedBracket_notInjective
#print axioms PentagonAdjoinedSixCell.selectedFullDoubleOrderedBracket_noInheritedDecoder
#print axioms PentagonAdjoinedSixCell.selectedFullDoubleOrderedBracket_noClassDecoder
#print axioms PentagonAdjoinedSixCell.selectedFullDoubleOrderedBracket_endomorphismNotInjective

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
