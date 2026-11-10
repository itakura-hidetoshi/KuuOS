import KUOS.Architecture.QiWuxingGK5CHP77StrictOnlyBranchShapeResidualV5_77

/-!
Qi v5.78 — complete v5.77 quotient observation is still locally
noninjective: maximal strict-only raw chain branches can occur at
different raw-reversal ancestor depths while all earlier observations
INCLUDING the nonassociative v5.77 branch-shape summary agree.

For any genuine original 17D proof N, let S = strict N and compare the
ACTUAL original contextual 18D endomorphism proofs

  A = chain (reverse (chain S S)) S
  B = chain (reverse S) (chain S S).

Both have one reversal, three strict leaves, two raw chains, the same
ordered raw-reverse/inherited event word, the same FULL pair of infinite
Nat-indexed towers, the same unit-reduced and inherited-sensitive raw
brackets, and exactly the same v5.77 maximal strict-only branch shape
[joined leaf leaf].  But A's maximal strict branch is INSIDE one raw
reversal and B's is OUTSIDE every raw reversal.

An independent dependent-Type18D structural summary retains the ordered
list of (number of raw-reversal ancestors, maximal strict-only chain
tree). It is preserved by ALL FIVE old selected19 generators and ALL
SEVEN new raw-congruence generators and descends SEPARATELY to their
actual quotients, factoring through the old-to-new projection.

The explicit new quotient values distinguish A and B. Thus even the
complete v5.77 observer has a LOCAL noninjective N -> N fiber and
neither the new depth-site summary nor quotient classes can be
reconstructed from its observations. No global completeness statement,
uninhabited arbitrary J -> N inhabitance, cross-WORLD descent, 20D
gluing or authority is claimed.

Original dependent Type18D, independent old/new Type19, fixed Lean
v4.30.0-rc2 and pinned mathlib, public root107, validation-only #1558
remain unchanged.
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

/-- Strict-only chain tree with an exact RAW reversal-ancestor depth.
A branch's depth is not its raw chain nesting depth. -/
abbrev SelectedStrictBranchReverseSite :=
  Nat × SelectedStrictOnlyChainTree

/-- Pure records the nonassociative shape of a whole raw strict-only
subproof. Sites record maximal nontrivial pure branches in order, now
paired with the number of surrounding raw reversals. -/
structure SelectedStrictBranchDepthSummary : Type where
  pure : Option SelectedStrictOnlyChainTree
  sites : List SelectedStrictBranchReverseSite
  deriving DecidableEq, Repr

/-- Joining two pure branches replaces their child-site entries with
one maximal joined branch; all other joins concatenate site lists. -/
def selectedStrictDepthSummaryJoin
    (A B : SelectedStrictBranchDepthSummary) :
    SelectedStrictBranchDepthSummary :=
  match A.pure, B.pure with
  | some x, some y =>
      ⟨some (.joined x y), [(0, .joined x y)]⟩
  | _, _ => ⟨none, A.sites ++ B.sites⟩

/-- Original whiskering is a boundary for pure strict chains, but
does not itself contribute a raw reversal ancestor. -/
def selectedStrictDepthSummaryWhisker
    (A : SelectedStrictBranchDepthSummary) :
    SelectedStrictBranchDepthSummary :=
  ⟨none, A.sites⟩

/-- A genuine raw reversal ends a pure root, and increases the
ancestor depth of every recorded internal strict-only branch. -/
def selectedStrictDepthSummaryReverse
    (A : SelectedStrictBranchDepthSummary) :
    SelectedStrictBranchDepthSummary :=
  ⟨none, A.sites.map (fun e => (e.1 + 1, e.2))⟩

/-- Read the raw reverse ancestry of maximal pure strict-only branches
from ACTUAL original dependent 18D proof values. An erasable raw
strict identity adjacent to an inherited old18D leaf is not recorded
as a nontrivial pure branch. -/
def selectedContextEighteenStrictBranchDepth (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    SelectedStrictBranchDepthSummary :=
  match M with
  | .inherited _ => ⟨none, []⟩
  | .whiskerLeft _ _ _ A =>
      selectedStrictDepthSummaryWhisker
        (selectedContextEighteenStrictBranchDepth l r A)
  | .whiskerRight _ _ A _ =>
      selectedStrictDepthSummaryWhisker
        (selectedContextEighteenStrictBranchDepth l r A)
  | .strict _ => ⟨some .leaf, []⟩
  | .reverse A =>
      selectedStrictDepthSummaryReverse
        (selectedContextEighteenStrictBranchDepth l r A)
  | .chain A B =>
      selectedStrictDepthSummaryJoin
        (selectedContextEighteenStrictBranchDepth l r A)
        (selectedContextEighteenStrictBranchDepth l r B)

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Preservation by all five ORIGINAL typed 19D generators. The
unitPrepend/unitAppend equations adjoin raw strict to an inherited
source, so neither creates a nontrivial strict-only chain. -/
theorem selectedLocalNineteen_preservesStrictBranchDepth
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenStrictBranchDepth l r M =
      selectedContextEighteenStrictBranchDepth l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- Preservation by all seven NEW raw-congruence generators, with
genuine congruence under raw reverse and each side of raw chain. -/
theorem selectedRawCongruent_preservesStrictBranchDepth
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenStrictBranchDepth l r M =
      selectedContextEighteenStrictBranchDepth l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesStrictBranchDepth l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      exact congrArg selectedStrictDepthSummaryReverse ih
  | rawChainRight A X ih =>
      exact congrArg
        (fun s : SelectedStrictBranchDepthSummary =>
          selectedStrictDepthSummaryJoin s
            (selectedContextEighteenStrictBranchDepth l r X)) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun s : SelectedStrictBranchDepthSummary =>
          selectedStrictDepthSummaryJoin
            (selectedContextEighteenStrictBranchDepth l r X) s) ih

/-- Independent ACTUAL seven-generator quotient descent. -/
def selectedRawCongruentStrictBranchDepthOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedStrictBranchDepthSummary :=
  Quotient.lift (selectedContextEighteenStrictBranchDepth l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesStrictBranchDepth l r A)

theorem selectedRawCongruentStrictBranchDepth_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentStrictBranchDepthOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenStrictBranchDepth l r M := rfl

/-- Independent ACTUAL old five-generator quotient descent. -/
def selectedNineteenStrictBranchDepthOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) →
      SelectedStrictBranchDepthSummary :=
  Quotient.lift (selectedContextEighteenStrictBranchDepth l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesStrictBranchDepth l r A)

theorem selectedStrictBranchDepth_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentStrictBranchDepthOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenStrictBranchDepthOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Two genuine ORIGINAL 18D Type values in the SAME N -> N fiber.
A maximal raw strict-only pair is under reverse on the left, and
outside reverse on the right, with the same overall raw counts. -/
def selectedStrictDepthWitnessInside
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain (.reverse (.chain (.strict N) (.strict N))) (.strict N)

def selectedStrictDepthWitnessOutside
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain (.reverse (.strict N)) (.chain (.strict N) (.strict N))

def selectedStrictDepthInsideValue : SelectedStrictBranchDepthSummary :=
  ⟨none, [(1, .joined .leaf .leaf)]⟩

def selectedStrictDepthOutsideValue : SelectedStrictBranchDepthSummary :=
  ⟨none, [(0, .joined .leaf .leaf)]⟩

theorem selectedStrictDepth_insideValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictBranchDepth l r
        (selectedStrictDepthWitnessInside l r N) =
      selectedStrictDepthInsideValue := rfl

theorem selectedStrictDepth_outsideValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictBranchDepth l r
        (selectedStrictDepthWitnessOutside l r N) =
      selectedStrictDepthOutsideValue := rfl

theorem selectedStrictDepth_valuesDistinct :
    selectedStrictDepthInsideValue ≠ selectedStrictDepthOutsideValue := by
  decide

theorem selectedStrictDepth_witnessDepthDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictBranchDepth l r
        (selectedStrictDepthWitnessInside l r N) ≠
      selectedContextEighteenStrictBranchDepth l r
        (selectedStrictDepthWitnessOutside l r N) := by
  rw [selectedStrictDepth_insideValue l r N,
    selectedStrictDepth_outsideValue l r N]
  exact selectedStrictDepth_valuesDistinct

/-- Every Nat degree of the COMPLETE ancestor tower agrees, not just
a fixed finite list. All strict-only child branches have positive
ancestor-tower counts zero, independent of raw chain association. -/
theorem selectedStrictDepth_witnessAncestorTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (degree : Nat) :
    selectedAncestorTowerCount l r degree
        (selectedStrictDepthWitnessInside l r N) =
      selectedAncestorTowerCount l r degree
        (selectedStrictDepthWitnessOutside l r N) := by
  cases degree with
  | zero => rfl
  | succ degree =>
      cases degree with
      | zero => rfl
      | succ degree => rfl

/-- The SECOND COMPLETE Nat-indexed direct reversal-run tower agrees
at all degrees, including the one raw reverse present in each term. -/
theorem selectedStrictDepth_witnessRunTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (degree : Nat) :
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedStrictDepthWitnessInside l r N) =
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedStrictDepthWitnessOutside l r N) := by
  cases degree with
  | zero => rfl
  | succ degree => rfl

/-- The ACTUAL full v5.73 quotient observation is equal, including
function extensionality of both INFINITE towers and every exact
inherited old18D root/inner bracket datum. -/
theorem selectedStrictDepth_witnessRootInnerObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentDoubleBracketCountRootInnerObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictDepthWitnessInside l r N)) =
      selectedRawCongruentDoubleBracketCountRootInnerObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictDepthWitnessOutside l r N)) := by
  have hbase :
      selectedRawCongruentFullDoubleOrderedBracketObservation l r N N
          (selectedRawCongruentClass l r
            (selectedStrictDepthWitnessInside l r N)) =
        selectedRawCongruentFullDoubleOrderedBracketObservation l r N N
          (selectedRawCongruentClass l r
            (selectedStrictDepthWitnessOutside l r N)) := by
    apply Prod.ext
    · apply Prod.ext
      · apply Prod.ext
        · apply Prod.ext
          · rfl
          · funext degree
            exact selectedStrictDepth_witnessAncestorTowerEq l r N degree
        · funext degree
          exact selectedStrictDepth_witnessRunTowerEq l r N degree
      · rfl
    · rfl
  apply Prod.ext
  · apply Prod.ext
    · apply Prod.ext
      · exact hbase
      · rfl
    · rfl
  · rfl

theorem selectedStrictDepth_insideSites
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedStrictDepthWitnessInside l r N) = [0] := rfl

theorem selectedStrictDepth_outsideSites
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedStrictDepthWitnessOutside l r N) = [0] := rfl

theorem selectedStrictDepth_insideWord
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseInheritedWord l r
        (selectedStrictDepthWitnessInside l r N) =
      [.rawReverse] := rfl

theorem selectedStrictDepth_outsideWord
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseInheritedWord l r
        (selectedStrictDepthWitnessOutside l r N) =
      [.rawReverse] := rfl

theorem selectedStrictDepth_insideSensitive
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedSensitiveBracket l r
        (selectedStrictDepthWitnessInside l r N) =
      .reversed .unit := rfl

theorem selectedStrictDepth_outsideSensitive
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedSensitiveBracket l r
        (selectedStrictDepthWitnessOutside l r N) =
      .reversed .unit := rfl

/-- The new branch DEPTH is invisible even when v5.77 adds the exact
nonassociative strict-only BRANCH SHAPE to the old observer. -/
def selectedStrictDepthSharedV577Value : SelectedStrictOnlyBranchSummary :=
  ⟨none, [.joined .leaf .leaf]⟩

theorem selectedStrictDepth_insideOldShape
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictOnlySummary l r
        (selectedStrictDepthWitnessInside l r N) =
      selectedStrictDepthSharedV577Value := rfl

theorem selectedStrictDepth_outsideOldShape
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictOnlySummary l r
        (selectedStrictDepthWitnessOutside l r N) =
      selectedStrictDepthSharedV577Value := rfl

/-- The entire v5.77 quotient observer: the COMPLETE v5.76 observer
and the independently descended v5.77 strict-only branch summary.
No earlier field is discarded or reduced to finite sampling. -/
abbrev SelectedFullV577QuotientObservationValue :=
  SelectedFullV576QuotientObservationValue ×
    SelectedStrictOnlyBranchSummary

def selectedRawCongruentFullV577QuotientObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedFullV577QuotientObservationValue :=
  fun q =>
    (selectedRawCongruentFullV576QuotientObservation l r J N q,
      selectedRawCongruentStrictOnlySummaryOnQuotient l r J N q)

/-- Same FULL v5.76 quotient observer, including true Nat-indexed
towers, reversals, old18D provenance and inherited-sensitive bracket. -/
theorem selectedStrictDepth_witnessV576ObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentFullV576QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictDepthWitnessInside l r N)) =
      selectedRawCongruentFullV576QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictDepthWitnessOutside l r N)) := by
  apply Prod.ext
  · apply Prod.ext
    · apply Prod.ext
      · exact selectedStrictDepth_witnessRootInnerObservedEq l r N
      · rfl
    · rfl
  · rfl

/-- Even the newly added v5.77 nonassociative branch summary
agrees, despite a difference in raw-reverse ANCESTOR location. -/
theorem selectedStrictDepth_witnessV577ObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentFullV577QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictDepthWitnessInside l r N)) =
      selectedRawCongruentFullV577QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictDepthWitnessOutside l r N)) := by
  apply Prod.ext
  · exact selectedStrictDepth_witnessV576ObservedEq l r N
  · rfl

/-- DISTINCT ACTUAL seven-generator quotient classes: this proof
uses independently descended depth-site summary, NOT mere syntactic
inequality of raw source values. -/
theorem selectedStrictDepth_witnessClassDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentClass l r
        (selectedStrictDepthWitnessInside l r N) ≠
      selectedRawCongruentClass l r
        (selectedStrictDepthWitnessOutside l r N) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentStrictBranchDepthOnQuotient l r N N) h
  change selectedContextEighteenStrictBranchDepth l r
      (selectedStrictDepthWitnessInside l r N) =
    selectedContextEighteenStrictBranchDepth l r
      (selectedStrictDepthWitnessOutside l r N) at hc
  exact (selectedStrictDepth_witnessDepthDistinct l r N) hc

/-- Absence of a genuine NEW typed 19D seven-generator comparison. -/
theorem selectedStrictDepth_witnessNoComparison
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedStrictDepthWitnessInside l r N)
      (selectedStrictDepthWitnessOutside l r N)) := by
  rintro ⟨A⟩
  exact (selectedStrictDepth_witnessClassDistinct l r N)
    (Quotient.sound ⟨A⟩)

/-- LOCAL noninjectivity of the COMPLETE v5.77 observer for every
actual N -> N endomorphism fiber. -/
theorem selectedStrictDepth_v577NotInjective
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentFullV577QuotientObservation l r N N) := by
  intro hinj
  exact (selectedStrictDepth_witnessClassDistinct l r N)
    (hinj (selectedStrictDepth_witnessV577ObservedEq l r N))

/-- No decoder from the complete v5.77 quotient observation can
recover the new independently descended strict branch depth sites. -/
theorem selectedStrictDepth_noDepthDecoder
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ ∃ decode :
        SelectedFullV577QuotientObservationValue →
          SelectedStrictBranchDepthSummary,
      ∀ q : Quotient (selectedRawCongruentSetoid l r N N),
        decode (selectedRawCongruentFullV577QuotientObservation
          l r N N q) =
            selectedRawCongruentStrictBranchDepthOnQuotient l r N N q := by
  rintro ⟨decode, h⟩
  have hc :
      selectedRawCongruentStrictBranchDepthOnQuotient l r N N
          (selectedRawCongruentClass l r
            (selectedStrictDepthWitnessInside l r N)) =
        selectedRawCongruentStrictBranchDepthOnQuotient l r N N
          (selectedRawCongruentClass l r
            (selectedStrictDepthWitnessOutside l r N)) := by
    calc
      _ = decode (selectedRawCongruentFullV577QuotientObservation
          l r N N (selectedRawCongruentClass l r
            (selectedStrictDepthWitnessInside l r N))) := (h _).symm
      _ = decode (selectedRawCongruentFullV577QuotientObservation
          l r N N (selectedRawCongruentClass l r
            (selectedStrictDepthWitnessOutside l r N))) :=
        congrArg decode (selectedStrictDepth_witnessV577ObservedEq l r N)
      _ = _ := h _
  change selectedContextEighteenStrictBranchDepth l r
      (selectedStrictDepthWitnessInside l r N) =
    selectedContextEighteenStrictBranchDepth l r
      (selectedStrictDepthWitnessOutside l r N) at hc
  exact (selectedStrictDepth_witnessDepthDistinct l r N) hc

/-- No quotient-class reconstruction from this local v5.77 observer. -/
theorem selectedStrictDepth_noClassDecoder
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ ∃ decode :
        SelectedFullV577QuotientObservationValue →
          Quotient (selectedRawCongruentSetoid l r N N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r N N),
        decode
            (selectedRawCongruentFullV577QuotientObservation
              l r N N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedStrictDepth_v577NotInjective l r N
  intro a b hab
  calc
    a = decode
        (selectedRawCongruentFullV577QuotientObservation
          l r N N a) := (h a).symm
    _ = decode
        (selectedRawCongruentFullV577QuotientObservation
          l r N N b) := congrArg decode hab
    _ = b := h b

end ExactFiber

#print axioms PentagonAdjoinedSixCell.SelectedStrictBranchReverseSite
#print axioms PentagonAdjoinedSixCell.SelectedStrictBranchDepthSummary
#print axioms PentagonAdjoinedSixCell.selectedStrictDepthSummaryJoin
#print axioms PentagonAdjoinedSixCell.selectedStrictDepthSummaryWhisker
#print axioms PentagonAdjoinedSixCell.selectedStrictDepthSummaryReverse
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenStrictBranchDepth
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesStrictBranchDepth
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesStrictBranchDepth
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentStrictBranchDepthOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentStrictBranchDepth_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenStrictBranchDepthOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedStrictBranchDepth_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedStrictDepthWitnessInside
#print axioms PentagonAdjoinedSixCell.selectedStrictDepthWitnessOutside
#print axioms PentagonAdjoinedSixCell.selectedStrictDepthInsideValue
#print axioms PentagonAdjoinedSixCell.selectedStrictDepthOutsideValue
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_insideValue
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_outsideValue
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_valuesDistinct
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_witnessDepthDistinct
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_witnessAncestorTowerEq
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_witnessRunTowerEq
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_witnessRootInnerObservedEq
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_insideSites
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_outsideSites
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_insideWord
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_outsideWord
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_insideSensitive
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_outsideSensitive
#print axioms PentagonAdjoinedSixCell.selectedStrictDepthSharedV577Value
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_insideOldShape
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_outsideOldShape
#print axioms PentagonAdjoinedSixCell.SelectedFullV577QuotientObservationValue
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullV577QuotientObservation
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_witnessV576ObservedEq
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_witnessV577ObservedEq
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_witnessClassDistinct
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_witnessNoComparison
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_v577NotInjective
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_noDepthDecoder
#print axioms PentagonAdjoinedSixCell.selectedStrictDepth_noClassDecoder

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
