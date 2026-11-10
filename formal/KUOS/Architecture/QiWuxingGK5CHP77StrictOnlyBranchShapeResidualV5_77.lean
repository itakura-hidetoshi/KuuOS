import KUOS.Architecture.QiWuxingGK5CHP77InheritedSensitiveBracketResidualV5_76

/-!
Qi v5.77 — even after adding v5.76's inherited-sensitive
NONASSOCIATIVE source bracket, the COMPLETE quotient observer does not
record the internal shape of a pure RAW STRICT-ONLY chain hidden
beneath a raw reverse.

A strict-only chain fragment is NOT the same as an erasable strict unit
next to a genuine inherited(old18) source leaf. The original selected19
five-generator unit rules only insert or remove raw strict identities
adjoining actual inherited old18 proofs; they do NOT impose a general
associativity equation for a strictly raw chain.

Define an independent structural SUMMARY for every original dependent
contextual18D proof. It records (1) an optional whole-subproof
strict-only nonassociative tree, and (2) an ordered list of maximal
strict-only chain trees with at least one raw chain node. Single
strict identities do not appear as maximal nontrivial branch events.
Its typed preservation for all five original and seven new selected19
comparison constructors is proved, followed by SEPARATE original/new
Quotient.lift descents and old-to-new projection factorization.

For a genuine original 17D endpoint N:
  S = strict N
  A = reverse (chain (chain S S) S)
  B = reverse (chain S (chain S S))
are actual 18D dependent proof values in exactly the N -> N fiber.
The original nine, both COMPLETE Nat-indexed infinite towers,
ordered reversal run list, unit-reduced nonassociative raw bracket,
inherited-leaf count, ordered old18D roots and COMPLETE old18D
internal brackets, ordered reversal-site inherited-leaf counts,
reverse/inherited event word, and inherited-sensitive bracket from
v5.76 ALL AGREE. But the independently descended summary preserves
a left-associated versus right-associated strict-only branch.

This proves genuinely distinct seven-generator quotient classes,
absence of a typed new19 comparison, and LOCAL noninjectivity and
decoder obstructions for v5.76's entire observer in a true N -> N
endomorphism fiber. No assertion of arbitrary J -> N inhabitance,
global quotient completeness, 20D gluing, cross-WORLD descent,
philosophical identity or action authority. Original dependent Type18D,
separate old/new typed19, root107, fixed Lean/mathlib and validation-only
PR #1558 remain unchanged.
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

/-- Free NONASSOCIATIVE shapes for a maximal original raw strict-only
chain. This is an auxiliary presentation and not an equality in the
source dependent Type18D. -/
inductive SelectedStrictOnlyChainTree : Type where
  | leaf : SelectedStrictOnlyChainTree
  | joined : SelectedStrictOnlyChainTree →
      SelectedStrictOnlyChainTree → SelectedStrictOnlyChainTree
  deriving DecidableEq, Repr

/-- The first component distinguishes subproofs wholly made from
raw strict identities and raw chains. The second remembers ordered
maximal NONTRIVIAL such strict-only chains occurring anywhere. -/
structure SelectedStrictOnlyBranchSummary : Type where
  pure : Option SelectedStrictOnlyChainTree
  branches : List SelectedStrictOnlyChainTree
  deriving DecidableEq, Repr

/-- At a raw chain of two pure strict-only children, record ONE maximal
shape; otherwise concatenate the independent nontrivial histories.
The previously recorded child subchains remain represented inside
the maximal joined tree, not forgotten. -/
def selectedStrictOnlySummaryJoin
    (A B : SelectedStrictOnlyBranchSummary) :
    SelectedStrictOnlyBranchSummary :=
  match A.pure, B.pure with
  | some x, some y =>
      ⟨some (.joined x y), [.joined x y]⟩
  | _, _ => ⟨none, A.branches ++ B.branches⟩

/-- Raw reversal or original whiskering ends a pure strict-only
ROOT, but retains every internal strict-chain witness. -/
def selectedStrictOnlySummaryBoundary
    (A : SelectedStrictOnlyBranchSummary) :
    SelectedStrictOnlyBranchSummary :=
  ⟨none, A.branches⟩

/-- Structural reading of ACTUAL dependent contextual18D proof values.
Original old18D inherited leaves and erasable raw strict units are
handled differently, preventing an incorrect quotient observation
based merely on the number of raw strict constructors. -/
def selectedContextEighteenStrictOnlySummary (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    SelectedStrictOnlyBranchSummary :=
  match M with
  | .inherited _ => ⟨none, []⟩
  | .whiskerLeft _ _ _ A =>
      selectedStrictOnlySummaryBoundary
        (selectedContextEighteenStrictOnlySummary l r A)
  | .whiskerRight _ _ A _ =>
      selectedStrictOnlySummaryBoundary
        (selectedContextEighteenStrictOnlySummary l r A)
  | .strict _ => ⟨some .leaf, []⟩
  | .reverse A =>
      selectedStrictOnlySummaryBoundary
        (selectedContextEighteenStrictOnlySummary l r A)
  | .chain A B =>
      selectedStrictOnlySummaryJoin
        (selectedContextEighteenStrictOnlySummary l r A)
        (selectedContextEighteenStrictOnlySummary l r B)

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Genuine OLD five-generator preservation. In particular the
unitPrepend/unitAppend constructors compare an actual inherited leaf
to raw chain(strict,inherited) or chain(inherited,strict); NEITHER
side contains a pure strict-only CHAIN. General strict-only chain
reassociation is not an old comparison generator. -/
theorem selectedLocalNineteen_preservesStrictOnlySummary
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenStrictOnlySummary l r M =
      selectedContextEighteenStrictOnlySummary l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- The distinct SEVEN new typed raw-congruence constructors preserve
the ENTIRE summary. Genuine rawReverse and rawChainLeft/Right use
the corresponding actual structural operation; no associativity
axiom is added to the original 18D dependent Type. -/
theorem selectedRawCongruent_preservesStrictOnlySummary
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenStrictOnlySummary l r M =
      selectedContextEighteenStrictOnlySummary l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesStrictOnlySummary l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      exact congrArg selectedStrictOnlySummaryBoundary ih
  | rawChainRight A X ih =>
      exact congrArg
        (fun s : SelectedStrictOnlyBranchSummary =>
          selectedStrictOnlySummaryJoin s
            (selectedContextEighteenStrictOnlySummary l r X)) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun s : SelectedStrictOnlyBranchSummary =>
          selectedStrictOnlySummaryJoin
            (selectedContextEighteenStrictOnlySummary l r X) s) ih

/-- ACTUAL seven-generator quotient descent using the Type-valued
comparison witnesses, not a proxy relation on syntax strings. -/
def selectedRawCongruentStrictOnlySummaryOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedStrictOnlyBranchSummary :=
  Quotient.lift (selectedContextEighteenStrictOnlySummary l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesStrictOnlySummary l r A)

theorem selectedRawCongruentStrictOnlySummary_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentStrictOnlySummaryOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenStrictOnlySummary l r M := rfl

/-- Separate genuine OLD five-generator quotient descent. The
independent old and new Type-valued comparison relations are not
identified. -/
def selectedNineteenStrictOnlySummaryOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) →
      SelectedStrictOnlyBranchSummary :=
  Quotient.lift (selectedContextEighteenStrictOnlySummary l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesStrictOnlySummary l r A)

theorem selectedStrictOnlySummary_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentStrictOnlySummaryOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenStrictOnlySummaryOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Two ORIGINAL raw strict-only chain trees with identical 17D
endpoints, three true strict leaves and two raw chain nodes each. -/
def selectedStrictOnlyLeftSource
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain (.chain (.strict N) (.strict N)) (.strict N)

def selectedStrictOnlyRightSource
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain (.strict N) (.chain (.strict N) (.strict N))

/-- Keep the two different strict-only raw chain shapes beneath the
same genuine outer raw reversal in the ACTUAL original Type18D. -/
def selectedStrictOnlyWitnessLeft
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (selectedStrictOnlyLeftSource l r N)

def selectedStrictOnlyWitnessRight
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (selectedStrictOnlyRightSource l r N)

/-- These independent free trees retain genuine raw chain brackets
even where previously certified event words and unit-reduced
brackets erased all strict-only source details. -/
def selectedStrictOnlyLeftValue : SelectedStrictOnlyBranchSummary :=
  ⟨none, [.joined (.joined .leaf .leaf) .leaf]⟩

def selectedStrictOnlyRightValue : SelectedStrictOnlyBranchSummary :=
  ⟨none, [.joined .leaf (.joined .leaf .leaf)]⟩

theorem selectedStrictOnly_leftValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictOnlySummary l r
        (selectedStrictOnlyWitnessLeft l r N) =
      selectedStrictOnlyLeftValue := rfl

theorem selectedStrictOnly_rightValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictOnlySummary l r
        (selectedStrictOnlyWitnessRight l r N) =
      selectedStrictOnlyRightValue := rfl

theorem selectedStrictOnly_valuesDistinct :
    selectedStrictOnlyLeftValue ≠ selectedStrictOnlyRightValue := by
  decide

theorem selectedStrictOnly_witnessSummaryDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictOnlySummary l r
        (selectedStrictOnlyWitnessLeft l r N) ≠
      selectedContextEighteenStrictOnlySummary l r
        (selectedStrictOnlyWitnessRight l r N) := by
  rw [selectedStrictOnly_leftValue l r N,
    selectedStrictOnly_rightValue l r N]
  exact selectedStrictOnly_valuesDistinct

/-- ALL Nat degrees of the real ancestor tower coincide, even
though the source strict-only raw chain ASSOCIATIONS do not.
Nothing is inferred about equality of raw Type18D terms. -/
theorem selectedStrictOnly_witnessAncestorTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (degree : Nat) :
    selectedAncestorTowerCount l r degree
        (selectedStrictOnlyWitnessLeft l r N) =
      selectedAncestorTowerCount l r degree
        (selectedStrictOnlyWitnessRight l r N) := by
  cases degree with
  | zero => rfl
  | succ degree =>
      cases degree with
      | zero => rfl
      | succ degree => rfl

/-- The entire second Nat-indexed direct reverse-run histogram also
coincides, with one outermost reversal and no adjacent pair. -/
theorem selectedStrictOnly_witnessRunTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (degree : Nat) :
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedStrictOnlyWitnessLeft l r N) =
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedStrictOnlyWitnessRight l r N) := by
  cases degree with
  | zero => rfl
  | succ degree => rfl

/-- COMPLETE v5.73 quotient observation equality including the
function-valued BOTH infinite towers and the full ordered old18D
internal source-bracket list. Functional extensionality is EXPLICIT,
not replaced by finite sample agreement. -/
theorem selectedStrictOnly_witnessRootInnerObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentDoubleBracketCountRootInnerObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictOnlyWitnessLeft l r N)) =
      selectedRawCongruentDoubleBracketCountRootInnerObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictOnlyWitnessRight l r N)) := by
  have hbase :
      selectedRawCongruentFullDoubleOrderedBracketObservation l r N N
          (selectedRawCongruentClass l r
            (selectedStrictOnlyWitnessLeft l r N)) =
        selectedRawCongruentFullDoubleOrderedBracketObservation l r N N
          (selectedRawCongruentClass l r
            (selectedStrictOnlyWitnessRight l r N)) := by
    apply Prod.ext
    · apply Prod.ext
      · apply Prod.ext
        · apply Prod.ext
          · rfl
          · funext degree
            exact selectedStrictOnly_witnessAncestorTowerEq l r N degree
        · funext degree
          exact selectedStrictOnly_witnessRunTowerEq l r N degree
      · rfl
    · rfl
  apply Prod.ext
  · apply Prod.ext
    · apply Prod.ext
      · exact hbase
      · rfl
    · rfl
  · rfl

theorem selectedStrictOnly_leftSites
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedStrictOnlyWitnessLeft l r N) = [0] := rfl

theorem selectedStrictOnly_rightSites
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedStrictOnlyWitnessRight l r N) = [0] := rfl

theorem selectedStrictOnly_leftWord
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseInheritedWord l r
        (selectedStrictOnlyWitnessLeft l r N) =
      [.rawReverse] := rfl

theorem selectedStrictOnly_rightWord
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseInheritedWord l r
        (selectedStrictOnlyWitnessRight l r N) =
      [.rawReverse] := rfl

theorem selectedStrictOnly_leftSensitive
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedSensitiveBracket l r
        (selectedStrictOnlyWitnessLeft l r N) =
      .reversed .unit := rfl

theorem selectedStrictOnly_rightSensitive
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedSensitiveBracket l r
        (selectedStrictOnlyWitnessRight l r N) =
      .reversed .unit := rfl

/-- Add the REAL, separately descended v5.76 inherited-sensitive
bracket to the COMPLETE previous v5.75 quotient observation. -/
abbrev SelectedFullV576QuotientObservationValue :=
  SelectedDoubleBracketCountRootInnerSitesWordValue ×
    SelectedInheritedSensitiveRawBracket

def selectedRawCongruentFullV576QuotientObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedFullV576QuotientObservationValue :=
  fun q =>
    (selectedRawCongruentDoubleBracketCountRootInnerSitesWordObservation
      l r J N q,
      selectedRawCongruentInheritedSensitiveBracketOnQuotient l r J N q)

/-- Even the COMPLETE v5.76 actual quotient observer agrees on the
two true same-fiber source proof values. The new independent strict
branch summary is NOT silently included in the previous observer. -/
theorem selectedStrictOnly_witnessFullObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentFullV576QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictOnlyWitnessLeft l r N)) =
      selectedRawCongruentFullV576QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictOnlyWitnessRight l r N)) := by
  apply Prod.ext
  · apply Prod.ext
    · apply Prod.ext
      · exact selectedStrictOnly_witnessRootInnerObservedEq l r N
      · rfl
    · rfl
  · rfl

/-- ACTUAL seven-generator quotient classes are DISTINCT since the
independent strict-only shape has a genuine quotient descent. Raw
syntax mismatch alone is not a proof of quotient inequivalence. -/
theorem selectedStrictOnly_witnessClassDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentClass l r
        (selectedStrictOnlyWitnessLeft l r N) ≠
      selectedRawCongruentClass l r
        (selectedStrictOnlyWitnessRight l r N) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentStrictOnlySummaryOnQuotient l r N N) h
  change selectedContextEighteenStrictOnlySummary l r
      (selectedStrictOnlyWitnessLeft l r N) =
    selectedContextEighteenStrictOnlySummary l r
      (selectedStrictOnlyWitnessRight l r N) at hc
  exact (selectedStrictOnly_witnessSummaryDistinct l r N) hc

/-- No genuine seven-generator Type-valued comparison between these
two original same-endpoint 18D proof values. -/
theorem selectedStrictOnly_witnessNoComparison
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedStrictOnlyWitnessLeft l r N)
      (selectedStrictOnlyWitnessRight l r N)) := by
  rintro ⟨A⟩
  exact (selectedStrictOnly_witnessClassDistinct l r N)
    (Quotient.sound ⟨A⟩)

/-- The entire V5.76 actual quotient observation is NONINJECTIVE in
each genuinely inhabited original endomorphism N -> N fiber. -/
theorem selectedStrictOnly_v576NotInjective
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentFullV576QuotientObservation l r N N) := by
  intro hinj
  exact (selectedStrictOnly_witnessClassDistinct l r N)
    (hinj (selectedStrictOnly_witnessFullObservedEq l r N))

/-- No decoder can reconstruct the new independently descended strict
branch summary from the ENTIRE v5.76 quotient observer. -/
theorem selectedStrictOnly_noSummaryDecoder
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ ∃ decode :
        SelectedFullV576QuotientObservationValue →
          SelectedStrictOnlyBranchSummary,
      ∀ q : Quotient (selectedRawCongruentSetoid l r N N),
        decode (selectedRawCongruentFullV576QuotientObservation
          l r N N q) =
            selectedRawCongruentStrictOnlySummaryOnQuotient l r N N q := by
  rintro ⟨decode, h⟩
  have hc :
      selectedRawCongruentStrictOnlySummaryOnQuotient l r N N
          (selectedRawCongruentClass l r
            (selectedStrictOnlyWitnessLeft l r N)) =
        selectedRawCongruentStrictOnlySummaryOnQuotient l r N N
          (selectedRawCongruentClass l r
            (selectedStrictOnlyWitnessRight l r N)) := by
    calc
      _ = decode (selectedRawCongruentFullV576QuotientObservation
          l r N N (selectedRawCongruentClass l r
            (selectedStrictOnlyWitnessLeft l r N))) := (h _).symm
      _ = decode (selectedRawCongruentFullV576QuotientObservation
          l r N N (selectedRawCongruentClass l r
            (selectedStrictOnlyWitnessRight l r N))) :=
        congrArg decode (selectedStrictOnly_witnessFullObservedEq l r N)
      _ = _ := h _
  change selectedContextEighteenStrictOnlySummary l r
      (selectedStrictOnlyWitnessLeft l r N) =
    selectedContextEighteenStrictOnlySummary l r
      (selectedStrictOnlyWitnessRight l r N) at hc
  exact (selectedStrictOnly_witnessSummaryDistinct l r N) hc

/-- No quotient-class decoder exists for the preceding complete
v5.76 observation on the ACTUAL N -> N endomorphism quotient. -/
theorem selectedStrictOnly_noClassDecoder
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ ∃ decode :
        SelectedFullV576QuotientObservationValue →
          Quotient (selectedRawCongruentSetoid l r N N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r N N),
        decode
            (selectedRawCongruentFullV576QuotientObservation
              l r N N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedStrictOnly_v576NotInjective l r N
  intro a b hab
  calc
    a = decode
        (selectedRawCongruentFullV576QuotientObservation
          l r N N a) := (h a).symm
    _ = decode
        (selectedRawCongruentFullV576QuotientObservation
          l r N N b) := congrArg decode hab
    _ = b := h b

end ExactFiber

#print axioms PentagonAdjoinedSixCell.SelectedStrictOnlyChainTree
#print axioms PentagonAdjoinedSixCell.SelectedStrictOnlyBranchSummary
#print axioms PentagonAdjoinedSixCell.selectedStrictOnlySummaryJoin
#print axioms PentagonAdjoinedSixCell.selectedStrictOnlySummaryBoundary
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenStrictOnlySummary
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesStrictOnlySummary
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesStrictOnlySummary
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentStrictOnlySummaryOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentStrictOnlySummary_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenStrictOnlySummaryOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedStrictOnlySummary_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedStrictOnlyLeftSource
#print axioms PentagonAdjoinedSixCell.selectedStrictOnlyRightSource
#print axioms PentagonAdjoinedSixCell.selectedStrictOnlyWitnessLeft
#print axioms PentagonAdjoinedSixCell.selectedStrictOnlyWitnessRight
#print axioms PentagonAdjoinedSixCell.selectedStrictOnlyLeftValue
#print axioms PentagonAdjoinedSixCell.selectedStrictOnlyRightValue
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_leftValue
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_rightValue
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_valuesDistinct
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_witnessSummaryDistinct
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_witnessAncestorTowerEq
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_witnessRunTowerEq
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_witnessRootInnerObservedEq
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_leftSites
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_rightSites
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_leftWord
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_rightWord
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_leftSensitive
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_rightSensitive
#print axioms PentagonAdjoinedSixCell.SelectedFullV576QuotientObservationValue
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullV576QuotientObservation
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_witnessFullObservedEq
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_witnessClassDistinct
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_witnessNoComparison
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_v576NotInjective
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_noSummaryDecoder
#print axioms PentagonAdjoinedSixCell.selectedStrictOnly_noClassDecoder

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
