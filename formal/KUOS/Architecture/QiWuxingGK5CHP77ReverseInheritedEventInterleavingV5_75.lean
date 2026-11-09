import KUOS.Architecture.QiWuxingGK5CHP77ReverseSiteInheritedOrderResidualV5_74

/-!
Qi v5.75 — a LOCAL quotient-level identification obstruction still
survives after adding v5.74's COMPLETE ordered per-reversal-site
inherited-leaf counts to its full previously certified observation.

The new independent raw contextual18D reading is the ordered EVENT
WORD of actual raw reverse constructors and genuine inherited old18D
leaves. Contextual strict units contribute no event; original source
proofs remain Type-valued and are not substituted by their event words.

For any ACTUAL original 17D endpoint N, define original same-fiber
contextual18D proofs
  A = chain (reverse (strict N)) (inherited (old18.strict N))
  B = chain (inherited (old18.strict N)) (reverse (strict N)).
They have identical full nine-observer signature, BOTH complete Nat
towers, raw reverse-run list, raw unit-reduced nonassociative bracket,
inherited count, original old18D root list and COMPLETE old18D inner
source-bracket list. Moreover, the full ordered v5.74 reverse-site
inherited count list is [0] for BOTH original witnesses.

Their genuine ordered event words differ:
  E(A) = [rawReverse, inherited]
  E(B) = [inherited, rawReverse].
The event word is separately preserved by every original five-typed
and every new seven-typed 19D comparison constructor, with independent
Quotient.lift descents and projection factorization. The two actual
new quotient classes differ; no corresponding seven-generator typed
comparison exists. This shows local noninjectivity AFTER adding the
v5.74 site list, rather than merely a raw syntax inequality.

No assertion of arbitrary heterogeneous-fiber inhabitation, global
quotient classification, 20D gluing, cross-WORLD descent, proof of
a philosophical equivalence, or execution authority is made.
Maintain original Type18D, independent old/new 19D presentations,
public root107, pinned Lean/mathlib and protected PR #1558.
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

/-- The two independently named events observed here. They are
not constructors of the original source dependent Type values. -/
inductive SelectedReverseInheritedEvent : Type where
  | rawReverse : SelectedReverseInheritedEvent
  | inherited : SelectedReverseInheritedEvent
  deriving DecidableEq, Repr

/-- Exact left-to-right event order of genuine inherited old18D
leaves and raw reversal constructors. Original contextual strict
units are invisible because they are erasable by selected19 unit
pasting. Whiskering keeps the internal history in its original order.
No bracket associativity or source Type equality is assumed. -/
def selectedContextEighteenReverseInheritedWord (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    List SelectedReverseInheritedEvent :=
  match M with
  | .inherited _ => [.inherited]
  | .whiskerLeft _ _ _ A =>
      selectedContextEighteenReverseInheritedWord l r A
  | .whiskerRight _ _ A _ =>
      selectedContextEighteenReverseInheritedWord l r A
  | .strict _ => []
  | .reverse A =>
      .rawReverse :: selectedContextEighteenReverseInheritedWord l r A
  | .chain A B =>
      selectedContextEighteenReverseInheritedWord l r A ++
        selectedContextEighteenReverseInheritedWord l r B

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Preservation for ALL FIVE ORIGINAL selected19 Type generators.
Only raw strict units disappear; genuine inherited leaves remain. -/
theorem selectedLocalNineteen_preservesReverseInheritedWord
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenReverseInheritedWord l r M =
      selectedContextEighteenReverseInheritedWord l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- Preservation for ALL SEVEN independent new raw congruence
generators. Unlike an unordered event count, the induction also
checks genuine rawReverse and both rawChain context closures. -/
theorem selectedRawCongruent_preservesReverseInheritedWord
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenReverseInheritedWord l r M =
      selectedContextEighteenReverseInheritedWord l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesReverseInheritedWord l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      exact congrArg
        (fun s : List SelectedReverseInheritedEvent =>
          SelectedReverseInheritedEvent.rawReverse :: s) ih
  | rawChainRight A X ih =>
      exact congrArg
        (fun s : List SelectedReverseInheritedEvent =>
          s ++ selectedContextEighteenReverseInheritedWord l r X) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun s : List SelectedReverseInheritedEvent =>
          selectedContextEighteenReverseInheritedWord l r X ++ s) ih

/-- Certified descent target: the ACTUAL seven-generator dependent
same-fiber quotient, not a newly postulated equivalence relation. -/
def selectedRawCongruentReverseInheritedWordOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      List SelectedReverseInheritedEvent :=
  Quotient.lift (selectedContextEighteenReverseInheritedWord l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesReverseInheritedWord l r A)

theorem selectedRawCongruentReverseInheritedWord_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentReverseInheritedWordOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenReverseInheritedWord l r M := rfl

/-- Independent original five-generator quotient descent. -/
def selectedNineteenReverseInheritedWordOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) →
      List SelectedReverseInheritedEvent :=
  Quotient.lift (selectedContextEighteenReverseInheritedWord l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesReverseInheritedWord l r A)

/-- Compatibility with original-to-new projection follows only
after BOTH independent descents are established. -/
theorem selectedReverseInheritedWord_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentReverseInheritedWordOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenReverseInheritedWordOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Original contextual18D values in an ACTUAL same-endpoint 17D
fiber, retaining a genuine inherited old18D strict proof. -/
def selectedReverseInheritedWitnessLeft
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain (.reverse (.strict N)) (.inherited (.strict N))

def selectedReverseInheritedWitnessRight
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain (.inherited (.strict N)) (.reverse (.strict N))

theorem selectedReverseInherited_leftWord
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseInheritedWord l r
        (selectedReverseInheritedWitnessLeft l r N) =
      [.rawReverse, .inherited] := rfl

theorem selectedReverseInherited_rightWord
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseInheritedWord l r
        (selectedReverseInheritedWitnessRight l r N) =
      [.inherited, .rawReverse] := rfl

theorem selectedReverseInherited_wordValuesDistinct :
    ([SelectedReverseInheritedEvent.rawReverse,
      SelectedReverseInheritedEvent.inherited] :
        List SelectedReverseInheritedEvent) ≠
      [SelectedReverseInheritedEvent.inherited,
        SelectedReverseInheritedEvent.rawReverse] := by
  decide

theorem selectedReverseInherited_witnessWordDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseInheritedWord l r
        (selectedReverseInheritedWitnessLeft l r N) ≠
      selectedContextEighteenReverseInheritedWord l r
        (selectedReverseInheritedWitnessRight l r N) := by
  rw [selectedReverseInherited_leftWord l r N,
      selectedReverseInherited_rightWord l r N]
  exact selectedReverseInherited_wordValuesDistinct

/-- BOTH original proofs have the identical complete v5.74 ordered
reversal-site inherited-leaf count list [0]; this is not a loss of
the original old18D inherited evidence. -/
theorem selectedReverseInherited_leftSites
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedReverseInheritedWitnessLeft l r N) = [0] := rfl

theorem selectedReverseInherited_rightSites
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedReverseInheritedWitnessRight l r N) = [0] := rfl

/-- Equality of EVERY degree of the untruncated ancestor tower.
The two raw chains differ in the syntactic order of a zero summand.
Split the actual degree before simplification; do not use an
unsupported definitional equality of Nat addition. -/
theorem selectedReverseInherited_witnessAncestorTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (degree : Nat) :
    selectedAncestorTowerCount l r degree
        (selectedReverseInheritedWitnessLeft l r N) =
      selectedAncestorTowerCount l r degree
        (selectedReverseInheritedWitnessRight l r N) := by
  cases degree with
  | zero => rfl
  | succ degree =>
      cases degree with
      | zero => rfl
      | succ degree => rfl

/-- Every degree of the independent direct consecutive-reversal-run
count tower agrees: a single nonnested reverse contributes exactly
at degree zero, irrespective of its relative inherited-leaf order. -/
theorem selectedReverseInherited_witnessRunTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (degree : Nat) :
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedReverseInheritedWitnessLeft l r N) =
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedReverseInheritedWitnessRight l r N) := by
  cases degree with
  | zero => rfl
  | succ degree => rfl

/-- Original nine observables, TWO untruncated infinite Nat towers,
ordered raw reverse runs, nonassociative unit-reduced bracket,
inherited old18D leaf count, ordered root list and FULL ordered
inner source-bracket list of v5.73 all coincide.
Crucially, the tower functions use extensional equality rather
than a false claim of definitional equality under swapped Nat sums. -/
theorem selectedReverseInherited_witnessRootInnerObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentDoubleBracketCountRootInnerObservation l r N N
        (selectedRawCongruentClass l r
          (selectedReverseInheritedWitnessLeft l r N)) =
      selectedRawCongruentDoubleBracketCountRootInnerObservation l r N N
        (selectedRawCongruentClass l r
          (selectedReverseInheritedWitnessRight l r N)) := by
  have hbase :
      selectedRawCongruentFullDoubleOrderedBracketObservation l r N N
          (selectedRawCongruentClass l r
            (selectedReverseInheritedWitnessLeft l r N)) =
        selectedRawCongruentFullDoubleOrderedBracketObservation l r N N
          (selectedRawCongruentClass l r
            (selectedReverseInheritedWitnessRight l r N)) := by
    apply Prod.ext
    · apply Prod.ext
      · apply Prod.ext
        · apply Prod.ext
          · rfl
          · funext degree
            exact selectedReverseInherited_witnessAncestorTowerEq l r N degree
        · funext degree
          exact selectedReverseInherited_witnessRunTowerEq l r N degree
      · rfl
    · rfl
  apply Prod.ext
  · apply Prod.ext
    · apply Prod.ext
      · exact hbase
      · rfl
    · rfl
  · rfl

/-- Complete site-list equality on the original quotient, NOT a
raw construction claimed to be equal in the source Type. -/
theorem selectedReverseInherited_witnessSiteObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentReverseSiteInheritedCountsOnQuotient l r N N
        (selectedRawCongruentClass l r
          (selectedReverseInheritedWitnessLeft l r N)) =
      selectedRawCongruentReverseSiteInheritedCountsOnQuotient l r N N
        (selectedRawCongruentClass l r
          (selectedReverseInheritedWitnessRight l r N)) := rfl

/-- The COMPLETE v5.74 quotient observation, now explicitly
augmented by the v5.74 ordered reversal-site inherited counts. -/
abbrev SelectedDoubleBracketCountRootInnerSitesValue :=
  SelectedDoubleBracketCountRootInnerValue × List Nat

def selectedRawCongruentDoubleBracketCountRootInnerSitesObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedDoubleBracketCountRootInnerSitesValue :=
  fun q =>
    (selectedRawCongruentDoubleBracketCountRootInnerObservation l r J N q,
      selectedRawCongruentReverseSiteInheritedCountsOnQuotient l r J N q)

theorem selectedReverseInherited_witnessFullObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentDoubleBracketCountRootInnerSitesObservation l r N N
        (selectedRawCongruentClass l r
          (selectedReverseInheritedWitnessLeft l r N)) =
      selectedRawCongruentDoubleBracketCountRootInnerSitesObservation l r N N
        (selectedRawCongruentClass l r
          (selectedReverseInheritedWitnessRight l r N)) := by
  exact Prod.ext
    (selectedReverseInherited_witnessRootInnerObservedEq l r N)
    (selectedReverseInherited_witnessSiteObservedEq l r N)

/-- Distinct actual seven-generator quotient classes, justified by
the independently descended event word, not a raw inequality. -/
theorem selectedReverseInherited_witnessClassDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentClass l r
        (selectedReverseInheritedWitnessLeft l r N) ≠
      selectedRawCongruentClass l r
        (selectedReverseInheritedWitnessRight l r N) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentReverseInheritedWordOnQuotient l r N N) h
  change selectedContextEighteenReverseInheritedWord l r
      (selectedReverseInheritedWitnessLeft l r N) =
    selectedContextEighteenReverseInheritedWord l r
      (selectedReverseInheritedWitnessRight l r N) at hc
  exact (selectedReverseInherited_witnessWordDistinct l r N) hc

/-- No actual new typed19 comparison exists in this exact fiber. -/
theorem selectedReverseInherited_witnessNoComparison
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedReverseInheritedWitnessLeft l r N)
      (selectedReverseInheritedWitnessRight l r N)) := by
  rintro ⟨A⟩
  exact (selectedReverseInherited_witnessClassDistinct l r N)
    (Quotient.sound ⟨A⟩)

/-- The entire v5.74 quotient observation is noninjective in each
ACTUALLY inhabited same-endpoint 17D endomorphism fiber. -/
theorem selectedReverseInherited_v574NotInjective
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentDoubleBracketCountRootInnerSitesObservation
        l r N N) := by
  intro hinj
  exact (selectedReverseInherited_witnessClassDistinct l r N)
    (hinj (selectedReverseInherited_witnessFullObservedEq l r N))

/-- No global decoder of ordered interleaving from the complete
previous v5.74 observer on the genuine endomorphism quotient. -/
theorem selectedReverseInherited_noWordDecoder
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ ∃ decode :
        SelectedDoubleBracketCountRootInnerSitesValue →
          List SelectedReverseInheritedEvent,
      ∀ q : Quotient (selectedRawCongruentSetoid l r N N),
        decode
            (selectedRawCongruentDoubleBracketCountRootInnerSitesObservation
              l r N N q) =
          selectedRawCongruentReverseInheritedWordOnQuotient
            l r N N q := by
  rintro ⟨decode, h⟩
  have hc :
      selectedRawCongruentReverseInheritedWordOnQuotient l r N N
          (selectedRawCongruentClass l r
            (selectedReverseInheritedWitnessLeft l r N)) =
        selectedRawCongruentReverseInheritedWordOnQuotient l r N N
          (selectedRawCongruentClass l r
            (selectedReverseInheritedWitnessRight l r N)) := by
    calc
      _ = decode
          (selectedRawCongruentDoubleBracketCountRootInnerSitesObservation
            l r N N (selectedRawCongruentClass l r
              (selectedReverseInheritedWitnessLeft l r N))) := (h _).symm
      _ = decode
          (selectedRawCongruentDoubleBracketCountRootInnerSitesObservation
            l r N N (selectedRawCongruentClass l r
              (selectedReverseInheritedWitnessRight l r N))) :=
        congrArg decode (selectedReverseInherited_witnessFullObservedEq l r N)
      _ = _ := h _
  change selectedContextEighteenReverseInheritedWord l r
      (selectedReverseInheritedWitnessLeft l r N) =
    selectedContextEighteenReverseInheritedWord l r
      (selectedReverseInheritedWitnessRight l r N) at hc
  exact (selectedReverseInherited_witnessWordDistinct l r N) hc

/-- No quotient-class inverse decoder follows from adding the FULL
v5.74 ordered per-site counts to the previous complete signature. -/
theorem selectedReverseInherited_noClassDecoder
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ ∃ decode :
        SelectedDoubleBracketCountRootInnerSitesValue →
          Quotient (selectedRawCongruentSetoid l r N N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r N N),
        decode
            (selectedRawCongruentDoubleBracketCountRootInnerSitesObservation
              l r N N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedReverseInherited_v574NotInjective l r N
  intro a b hab
  calc
    a = decode
        (selectedRawCongruentDoubleBracketCountRootInnerSitesObservation
          l r N N a) := (h a).symm
    _ = decode
        (selectedRawCongruentDoubleBracketCountRootInnerSitesObservation
          l r N N b) := congrArg decode hab
    _ = b := h b

end ExactFiber

#print axioms PentagonAdjoinedSixCell.SelectedReverseInheritedEvent
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenReverseInheritedWord
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesReverseInheritedWord
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesReverseInheritedWord
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseInheritedWordOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseInheritedWord_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenReverseInheritedWordOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedReverseInheritedWord_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedReverseInheritedWitnessLeft
#print axioms PentagonAdjoinedSixCell.selectedReverseInheritedWitnessRight
#print axioms PentagonAdjoinedSixCell.selectedReverseInherited_leftWord
#print axioms PentagonAdjoinedSixCell.selectedReverseInherited_rightWord
#print axioms PentagonAdjoinedSixCell.selectedReverseInherited_wordValuesDistinct
#print axioms PentagonAdjoinedSixCell.selectedReverseInherited_witnessWordDistinct
#print axioms PentagonAdjoinedSixCell.selectedReverseInherited_leftSites
#print axioms PentagonAdjoinedSixCell.selectedReverseInherited_rightSites
#print axioms PentagonAdjoinedSixCell.selectedReverseInherited_witnessAncestorTowerEq
#print axioms PentagonAdjoinedSixCell.selectedReverseInherited_witnessRunTowerEq
#print axioms PentagonAdjoinedSixCell.selectedReverseInherited_witnessRootInnerObservedEq
#print axioms PentagonAdjoinedSixCell.selectedReverseInherited_witnessSiteObservedEq
#print axioms PentagonAdjoinedSixCell.SelectedDoubleBracketCountRootInnerSitesValue
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentDoubleBracketCountRootInnerSitesObservation
#print axioms PentagonAdjoinedSixCell.selectedReverseInherited_witnessFullObservedEq
#print axioms PentagonAdjoinedSixCell.selectedReverseInherited_witnessClassDistinct
#print axioms PentagonAdjoinedSixCell.selectedReverseInherited_witnessNoComparison
#print axioms PentagonAdjoinedSixCell.selectedReverseInherited_v574NotInjective
#print axioms PentagonAdjoinedSixCell.selectedReverseInherited_noWordDecoder
#print axioms PentagonAdjoinedSixCell.selectedReverseInherited_noClassDecoder

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
