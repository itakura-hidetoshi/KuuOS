import KUOS.Architecture.QiWuxingGK5CHP77StrictBranchReverseDepthResidualV5_78

/-!
Qi v5.79 — the COMPLETE v5.78 actual seven-generator quotient
observation remains locally noninjective. Even after tracking each
maximal nontrivial strict-only branch's free NONASSOCIATIVE TREE and
the count of its surrounding RAW reversal ancestors, the ordered
LEFT/RIGHT chain address of that branch is still independent data.

For each genuine original 17D proof N, let S := strict N. Consider
the two ACTUAL original contextual 18D endomorphism proofs

  A = chain (chain S S) (reverse S)
  B = chain (reverse S) (chain S S).

The original nine observations, BOTH untruncated Nat-indexed towers,
ordered runs, unit-reduced and inherited-sensitive raw brackets,
old18D inherited-source provenance, v5.74 ordered reverse-site
counts, v5.75 ordered event word, v5.77 maximal strict-only branch
shape, and v5.78 ordered reversal-depth branch summary ALL AGREE.

The new independent Type18D observer records ordered maximal pure
strict-only branch addresses in the ambient raw-chain syntax tree
as lists of left/right steps together with each free branch tree.
Both sources contain a maximal branch (joined leaf leaf) at raw
reversal depth ZERO, but its outer raw-chain address is respectively
[left] and [right].

This observer preserves all FIVE genuine old selected19 and all
SEVEN new raw-congruence selected19 constructors; two independent
Quotient.lift descents and old-to-new projection factorization
follow. Actual new seven-generator quotient classes differ, no
typed new 19D comparison exists, and the full v5.78 observation
is noninjective in each GIVEN N -> N fiber, with no branch-address
or quotient-class decoder.

NO claim of arbitrary J -> N inhabitance, global quotient
completeness, 20D gluing, cross-WORLD descent, or philosophy-to-
mathematics identity/authority. Original Type18D, independent
old/new Type19, public root107, pinned Lean/mathlib, and protected
validation-only PR #1558 are unchanged. Append-only, tighten-only,
overwrite-forbidden, same-root.
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

/-- Raw chain location is independent of the number of raw reversals
surrounding a strict-only branch. Left/right are PATH STEPS, not
new comparison generators or source Type equations. -/
inductive SelectedStrictChainSide : Type where
  | left : SelectedStrictChainSide
  | right : SelectedStrictChainSide
  deriving DecidableEq, Repr

/-- Ordered ambient raw chain path (outermost first) and the free
nonassociative shape of a maximal nontrivial strict-only chain. -/
abbrev SelectedStrictBranchPath :=
  List SelectedStrictChainSide × SelectedStrictOnlyChainTree

structure SelectedStrictBranchPathSummary : Type where
  pure : Option SelectedStrictOnlyChainTree
  sites : List SelectedStrictBranchPath
  deriving DecidableEq, Repr

/-- Two pure strict-only children yield a single maximal branch.
Otherwise, each previously identified branch acquires the genuine
left/right child address of this raw chain; no arbitrary reassociation
of genuine raw chain syntax is imposed. -/
def selectedStrictPathSummaryJoin
    (A B : SelectedStrictBranchPathSummary) :
    SelectedStrictBranchPathSummary :=
  match A.pure, B.pure with
  | some x, some y =>
      ⟨some (.joined x y), [([], .joined x y)]⟩
  | _, _ =>
      ⟨none,
        A.sites.map (fun e => (SelectedStrictChainSide.left :: e.1, e.2)) ++
        B.sites.map (fun e => (SelectedStrictChainSide.right :: e.1, e.2))⟩

/-- Raw reverse and original whiskering both close pure strict-only
roots but do NOT insert fictitious raw-chain left/right steps. -/
def selectedStrictPathSummaryBoundary
    (A : SelectedStrictBranchPathSummary) :
    SelectedStrictBranchPathSummary :=
  ⟨none, A.sites⟩

/-- Structural observer on ACTUAL original dependent contextual18D
proof values. An erasable strict unit inserted immediately next to
a true inherited old18D leaf never forms a pure nontrivial branch. -/
def selectedContextEighteenStrictBranchPath (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    SelectedStrictBranchPathSummary :=
  match M with
  | .inherited _ => ⟨none, []⟩
  | .whiskerLeft _ _ _ A =>
      selectedStrictPathSummaryBoundary
        (selectedContextEighteenStrictBranchPath l r A)
  | .whiskerRight _ _ A _ =>
      selectedStrictPathSummaryBoundary
        (selectedContextEighteenStrictBranchPath l r A)
  | .strict _ => ⟨some .leaf, []⟩
  | .reverse A =>
      selectedStrictPathSummaryBoundary
        (selectedContextEighteenStrictBranchPath l r A)
  | .chain A B =>
      selectedStrictPathSummaryJoin
        (selectedContextEighteenStrictBranchPath l r A)
        (selectedContextEighteenStrictBranchPath l r B)

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Actual preservation under all FIVE original typed selected19
comparison generators. The original unit rules concern inherited
source leaves; they do not erase or reassociate pure strict chains. -/
theorem selectedLocalNineteen_preservesStrictBranchPath
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenStrictBranchPath l r M =
      selectedContextEighteenStrictBranchPath l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- Preserve the full left/right path summary under ALL SEVEN
genuine new typed raw-congruence 19D comparison constructors. -/
theorem selectedRawCongruent_preservesStrictBranchPath
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenStrictBranchPath l r M =
      selectedContextEighteenStrictBranchPath l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesStrictBranchPath l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      exact congrArg selectedStrictPathSummaryBoundary ih
  | rawChainRight A X ih =>
      exact congrArg
        (fun s : SelectedStrictBranchPathSummary =>
          selectedStrictPathSummaryJoin s
            (selectedContextEighteenStrictBranchPath l r X)) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun s : SelectedStrictBranchPathSummary =>
          selectedStrictPathSummaryJoin
            (selectedContextEighteenStrictBranchPath l r X) s) ih

/-- Independent ACTUAL new seven-generator quotient descent,
not a syntactic proxy equivalence or fabricated equality of Types. -/
def selectedRawCongruentStrictBranchPathOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedStrictBranchPathSummary :=
  Quotient.lift (selectedContextEighteenStrictBranchPath l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesStrictBranchPath l r A)

theorem selectedRawCongruentStrictBranchPath_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentStrictBranchPathOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenStrictBranchPath l r M := rfl

/-- Separate genuine original five-generator quotient descent. -/
def selectedNineteenStrictBranchPathOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) →
      SelectedStrictBranchPathSummary :=
  Quotient.lift (selectedContextEighteenStrictBranchPath l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesStrictBranchPath l r A)

/-- Old-to-new quotient projection preserves the independent
path summary without identifying the old/new comparison Types. -/
theorem selectedStrictBranchPath_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentStrictBranchPathOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenStrictBranchPathOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Two genuinely original dependent Type18D witnesses in exactly
the SAME N -> N fiber, distinguished by an outer raw-chain side. -/
def selectedStrictPathWitnessLeft
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain (.chain (.strict N) (.strict N)) (.reverse (.strict N))

def selectedStrictPathWitnessRight
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain (.reverse (.strict N)) (.chain (.strict N) (.strict N))

def selectedStrictPathLeftValue : SelectedStrictBranchPathSummary :=
  ⟨none, [([.left], .joined .leaf .leaf)]⟩

def selectedStrictPathRightValue : SelectedStrictBranchPathSummary :=
  ⟨none, [([.right], .joined .leaf .leaf)]⟩

theorem selectedStrictPath_leftValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictBranchPath l r
        (selectedStrictPathWitnessLeft l r N) =
      selectedStrictPathLeftValue := rfl

theorem selectedStrictPath_rightValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictBranchPath l r
        (selectedStrictPathWitnessRight l r N) =
      selectedStrictPathRightValue := rfl

theorem selectedStrictPath_valuesDistinct :
    selectedStrictPathLeftValue ≠ selectedStrictPathRightValue := by
  decide

theorem selectedStrictPath_witnessPathDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictBranchPath l r
        (selectedStrictPathWitnessLeft l r N) ≠
      selectedContextEighteenStrictBranchPath l r
        (selectedStrictPathWitnessRight l r N) := by
  rw [selectedStrictPath_leftValue l r N,
    selectedStrictPath_rightValue l r N]
  exact selectedStrictPath_valuesDistinct

/-- COMPLETE infinite ancestor towers agree for ALL Nat degrees;
the raw reverse contains a strict unit and one independent
nontrivial pure strict branch is merely in a different raw-chain
side. -/
theorem selectedStrictPath_witnessAncestorTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (degree : Nat) :
    selectedAncestorTowerCount l r degree
        (selectedStrictPathWitnessLeft l r N) =
      selectedAncestorTowerCount l r degree
        (selectedStrictPathWitnessRight l r N) := by
  cases degree with
  | zero => rfl
  | succ degree =>
      cases degree with
      | zero => rfl
      | succ degree => rfl

/-- COMPLETE direct raw consecutive-reversal run-count towers agree
for all degrees (not merely a finite prefix). -/
theorem selectedStrictPath_witnessRunTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (degree : Nat) :
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedStrictPathWitnessLeft l r N) =
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedStrictPathWitnessRight l r N) := by
  cases degree with
  | zero => rfl
  | succ degree => rfl

/-- Equality of the COMPLETE v5.73 quotient observation, including
full function-valued Nat towers and entire old18D source-provenance
lists; the two infinite function equalities use funext. -/
theorem selectedStrictPath_witnessRootInnerObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentDoubleBracketCountRootInnerObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictPathWitnessLeft l r N)) =
      selectedRawCongruentDoubleBracketCountRootInnerObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictPathWitnessRight l r N)) := by
  have hbase :
      selectedRawCongruentFullDoubleOrderedBracketObservation l r N N
          (selectedRawCongruentClass l r
            (selectedStrictPathWitnessLeft l r N)) =
        selectedRawCongruentFullDoubleOrderedBracketObservation l r N N
          (selectedRawCongruentClass l r
            (selectedStrictPathWitnessRight l r N)) := by
    apply Prod.ext
    · apply Prod.ext
      · apply Prod.ext
        · apply Prod.ext
          · rfl
          · funext degree
            exact selectedStrictPath_witnessAncestorTowerEq l r N degree
        · funext degree
          exact selectedStrictPath_witnessRunTowerEq l r N degree
      · rfl
    · rfl
  apply Prod.ext
  · apply Prod.ext
    · apply Prod.ext
      · exact hbase
      · rfl
    · rfl
  · rfl

theorem selectedStrictPath_leftSites
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedStrictPathWitnessLeft l r N) = [0] := rfl

theorem selectedStrictPath_rightSites
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedStrictPathWitnessRight l r N) = [0] := rfl

theorem selectedStrictPath_leftWord
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseInheritedWord l r
        (selectedStrictPathWitnessLeft l r N) =
      [.rawReverse] := rfl

theorem selectedStrictPath_rightWord
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseInheritedWord l r
        (selectedStrictPathWitnessRight l r N) =
      [.rawReverse] := rfl

theorem selectedStrictPath_leftSensitive
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedSensitiveBracket l r
        (selectedStrictPathWitnessLeft l r N) =
      .reversed .unit := rfl

theorem selectedStrictPath_rightSensitive
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedSensitiveBracket l r
        (selectedStrictPathWitnessRight l r N) =
      .reversed .unit := rfl

def selectedStrictPathSharedV577Shape : SelectedStrictOnlyBranchSummary :=
  ⟨none, [.joined .leaf .leaf]⟩

theorem selectedStrictPath_leftOldShape
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictOnlySummary l r
        (selectedStrictPathWitnessLeft l r N) =
      selectedStrictPathSharedV577Shape := rfl

theorem selectedStrictPath_rightOldShape
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictOnlySummary l r
        (selectedStrictPathWitnessRight l r N) =
      selectedStrictPathSharedV577Shape := rfl

/-- The full new v5.78 statistic ALSO agrees, including all raw
reversal ancestor counts of every ordered maximal strict branch. -/
def selectedStrictPathSharedV578Depth : SelectedStrictBranchDepthSummary :=
  ⟨none, [(0, .joined .leaf .leaf)]⟩

theorem selectedStrictPath_leftOldDepth
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictBranchDepth l r
        (selectedStrictPathWitnessLeft l r N) =
      selectedStrictPathSharedV578Depth := rfl

theorem selectedStrictPath_rightOldDepth
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictBranchDepth l r
        (selectedStrictPathWitnessRight l r N) =
      selectedStrictPathSharedV578Depth := rfl

/-- The COMPLETE v5.78 actual new seven-generator quotient
observation includes every previous component, NOT a finite
sample nor an observer dropping an earlier provenance statistic. -/
abbrev SelectedFullV578QuotientObservationValue :=
  SelectedFullV577QuotientObservationValue ×
    SelectedStrictBranchDepthSummary

def selectedRawCongruentFullV578QuotientObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedFullV578QuotientObservationValue :=
  fun q =>
    (selectedRawCongruentFullV577QuotientObservation l r J N q,
      selectedRawCongruentStrictBranchDepthOnQuotient l r J N q)

/-- Equality of the whole v5.76 actual quotient observation. -/
theorem selectedStrictPath_witnessV576ObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentFullV576QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictPathWitnessLeft l r N)) =
      selectedRawCongruentFullV576QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictPathWitnessRight l r N)) := by
  apply Prod.ext
  · apply Prod.ext
    · apply Prod.ext
      · exact selectedStrictPath_witnessRootInnerObservedEq l r N
      · rfl
    · rfl
  · rfl

/-- Full v5.77 observation equality, including entire v5.76
observer and v5.77 independent strict-only free branch trees. -/
theorem selectedStrictPath_witnessV577ObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentFullV577QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictPathWitnessLeft l r N)) =
      selectedRawCongruentFullV577QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictPathWitnessRight l r N)) := by
  apply Prod.ext
  · exact selectedStrictPath_witnessV576ObservedEq l r N
  · rfl

/-- Equal full v5.78 observer, now including independently descended
nonassociative branch-tree/RAW reversal-ancestor depth information. -/
theorem selectedStrictPath_witnessV578ObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentFullV578QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictPathWitnessLeft l r N)) =
      selectedRawCongruentFullV578QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedStrictPathWitnessRight l r N)) := by
  apply Prod.ext
  · exact selectedStrictPath_witnessV577ObservedEq l r N
  · rfl

/-- The actual new seven-generator quotient classes are DISTINCT,
by an independently descended true Type18D path invariant, not
by comparing raw syntax strings. -/
theorem selectedStrictPath_witnessClassDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentClass l r
        (selectedStrictPathWitnessLeft l r N) ≠
      selectedRawCongruentClass l r
        (selectedStrictPathWitnessRight l r N) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentStrictBranchPathOnQuotient l r N N) h
  change selectedContextEighteenStrictBranchPath l r
      (selectedStrictPathWitnessLeft l r N) =
    selectedContextEighteenStrictBranchPath l r
      (selectedStrictPathWitnessRight l r N) at hc
  exact (selectedStrictPath_witnessPathDistinct l r N) hc

/-- No genuine NEW selected19 Type-valued comparison. -/
theorem selectedStrictPath_witnessNoComparison
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedStrictPathWitnessLeft l r N)
      (selectedStrictPathWitnessRight l r N)) := by
  rintro ⟨A⟩
  exact (selectedStrictPath_witnessClassDistinct l r N)
    (Quotient.sound ⟨A⟩)

/-- LOCAL noninjectivity of full v5.78 observer on the actual
new seven-generator quotient of each GIVEN N -> N endomorphism
fiber, not an arbitrary uninhabited distinct-endpoint fiber. -/
theorem selectedStrictPath_v578NotInjective
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentFullV578QuotientObservation l r N N) := by
  intro hinj
  exact (selectedStrictPath_witnessClassDistinct l r N)
    (hinj (selectedStrictPath_witnessV578ObservedEq l r N))

/-- There is no decoder that reconstructs the independent true
left/right chain address observer from the complete v5.78 quotient
observation at a genuine N -> N fiber. -/
theorem selectedStrictPath_noPathDecoder
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ ∃ decode :
        SelectedFullV578QuotientObservationValue →
          SelectedStrictBranchPathSummary,
      ∀ q : Quotient (selectedRawCongruentSetoid l r N N),
        decode (selectedRawCongruentFullV578QuotientObservation
          l r N N q) =
            selectedRawCongruentStrictBranchPathOnQuotient l r N N q := by
  rintro ⟨decode, h⟩
  have hc :
      selectedRawCongruentStrictBranchPathOnQuotient l r N N
          (selectedRawCongruentClass l r
            (selectedStrictPathWitnessLeft l r N)) =
        selectedRawCongruentStrictBranchPathOnQuotient l r N N
          (selectedRawCongruentClass l r
            (selectedStrictPathWitnessRight l r N)) := by
    calc
      _ = decode (selectedRawCongruentFullV578QuotientObservation
          l r N N (selectedRawCongruentClass l r
            (selectedStrictPathWitnessLeft l r N))) := (h _).symm
      _ = decode (selectedRawCongruentFullV578QuotientObservation
          l r N N (selectedRawCongruentClass l r
            (selectedStrictPathWitnessRight l r N))) :=
        congrArg decode (selectedStrictPath_witnessV578ObservedEq l r N)
      _ = _ := h _
  change selectedContextEighteenStrictBranchPath l r
      (selectedStrictPathWitnessLeft l r N) =
    selectedContextEighteenStrictBranchPath l r
      (selectedStrictPathWitnessRight l r N) at hc
  exact (selectedStrictPath_witnessPathDistinct l r N) hc

/-- No decoder can recover ACTUAL new quotient classes from the
complete v5.78 observer in this one genuine endomorphism fiber. -/
theorem selectedStrictPath_noClassDecoder
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ ∃ decode :
        SelectedFullV578QuotientObservationValue →
          Quotient (selectedRawCongruentSetoid l r N N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r N N),
        decode
            (selectedRawCongruentFullV578QuotientObservation
              l r N N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedStrictPath_v578NotInjective l r N
  intro a b hab
  calc
    a = decode
        (selectedRawCongruentFullV578QuotientObservation
          l r N N a) := (h a).symm
    _ = decode
        (selectedRawCongruentFullV578QuotientObservation
          l r N N b) := congrArg decode hab
    _ = b := h b

end ExactFiber

#print axioms PentagonAdjoinedSixCell.SelectedStrictChainSide
#print axioms PentagonAdjoinedSixCell.SelectedStrictBranchPath
#print axioms PentagonAdjoinedSixCell.SelectedStrictBranchPathSummary
#print axioms PentagonAdjoinedSixCell.selectedStrictPathSummaryJoin
#print axioms PentagonAdjoinedSixCell.selectedStrictPathSummaryBoundary
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenStrictBranchPath
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesStrictBranchPath
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesStrictBranchPath
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentStrictBranchPathOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentStrictBranchPath_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenStrictBranchPathOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedStrictBranchPath_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedStrictPathWitnessLeft
#print axioms PentagonAdjoinedSixCell.selectedStrictPathWitnessRight
#print axioms PentagonAdjoinedSixCell.selectedStrictPathLeftValue
#print axioms PentagonAdjoinedSixCell.selectedStrictPathRightValue
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_leftValue
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_rightValue
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_valuesDistinct
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_witnessPathDistinct
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_witnessAncestorTowerEq
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_witnessRunTowerEq
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_witnessRootInnerObservedEq
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_leftSites
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_rightSites
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_leftWord
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_rightWord
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_leftSensitive
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_rightSensitive
#print axioms PentagonAdjoinedSixCell.selectedStrictPathSharedV577Shape
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_leftOldShape
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_rightOldShape
#print axioms PentagonAdjoinedSixCell.selectedStrictPathSharedV578Depth
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_leftOldDepth
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_rightOldDepth
#print axioms PentagonAdjoinedSixCell.SelectedFullV578QuotientObservationValue
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullV578QuotientObservation
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_witnessV576ObservedEq
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_witnessV577ObservedEq
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_witnessV578ObservedEq
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_witnessClassDistinct
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_witnessNoComparison
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_v578NotInjective
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_noPathDecoder
#print axioms PentagonAdjoinedSixCell.selectedStrictPath_noClassDecoder

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
