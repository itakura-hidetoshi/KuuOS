import KUOS.Architecture.QiWuxingGK5CHP77ReverseInheritedEventInterleavingV5_75

/-!
Qi v5.76 — after observing the entire independently descended
v5.75 reverse/inherited EVENT WORD, the nonassociative PARENTHESIZATION
of genuine inherited source leaves together with raw reversals still
carries a separate exact-fiber quotient invariant.

An independent free unit-reduced raw bracket now keeps each ACTUAL
inherited old18D leaf as a nonunit source atom, in contrast to the
v5.70 bracket observer that erased inherited leaves as units.
The original dependent 18D evidence and the independent five- and
seven-constructor typed19 comparisons are NOT replaced or altered.

For every genuine 17D endpoint N, let
  I = inherited (SelectedLocalEighteen.strict N)
  R = reverse (strict N)
  A = chain (chain I R) I
  B = chain I (chain R I).
Both raw18D terms inhabit exactly N -> N. The complete previous
v5.75 observer agrees: original nine, BOTH untruncated Nat -> Nat
towers, ordered reverse-run list, nonassociative v5.70 unit-reduced
raw bracket, inherited count, ordered old18D root and FULL inner
bracket lists, ordered v5.74 reversal-site inherited counts, and
the full ordered v5.75 reverse/inherited event word [I,R,I].

The new inherited-sensitive bracket does NOT identify their two
association trees. It is preserved by all five old and seven new
typed19 generators, independently descends to both real quotients,
and factors through the old-to-new quotient projection. Therefore
the two real seven-generator quotient classes are distinct,
without asserting mere raw syntax inequality suffices.

No uninhabited heterogeneous fiber is populated. This proves
local endomorphism-fiber noninjectivity of the v5.75 observation,
not all-fiber or global quotient completeness, universal 20D
gluing, cross-WORLD descent, philosophical equivalence or authority.
Original Type-valued old18D proofs, independent typed19 comparisons,
root107, pinned Lean/mathlib and validation-only #1558 untouched.
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

/-- An independent, free, NONASSOCIATIVE raw bracket interpretation.
Raw strict is a unit; a real inherited old18D leaf is NOT a unit.
A source atom is not an equality of arbitrary old18D Type values. -/
inductive SelectedInheritedSensitiveRawBracket : Type where
  | unit : SelectedInheritedSensitiveRawBracket
  | source : SelectedInheritedSensitiveRawBracket
  | reversed : SelectedInheritedSensitiveRawBracket →
      SelectedInheritedSensitiveRawBracket
  | joined : SelectedInheritedSensitiveRawBracket →
      SelectedInheritedSensitiveRawBracket →
      SelectedInheritedSensitiveRawBracket
  deriving DecidableEq, Repr

/-- Eliminate only genuinely erasable raw strict units, preserving
association between every remaining raw reversal and source atom. -/
def selectedInheritedSensitiveBracketJoin :
    SelectedInheritedSensitiveRawBracket →
    SelectedInheritedSensitiveRawBracket →
    SelectedInheritedSensitiveRawBracket
  | .unit, B => B
  | A, .unit => A
  | A, B => .joined A B

/-- Read the original dependent contextual18D source, NOT a proxy.
v5.70's coarser unit-reduced bracket sends inherited old18D to a
unit; the present independent bracket instead retains that leaf. -/
def selectedContextEighteenInheritedSensitiveBracket (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    SelectedInheritedSensitiveRawBracket :=
  match M with
  | .inherited _ => .source
  | .whiskerLeft _ _ _ A =>
      selectedContextEighteenInheritedSensitiveBracket l r A
  | .whiskerRight _ _ A _ =>
      selectedContextEighteenInheritedSensitiveBracket l r A
  | .strict _ => .unit
  | .reverse A =>
      .reversed (selectedContextEighteenInheritedSensitiveBracket l r A)
  | .chain A B =>
      selectedInheritedSensitiveBracketJoin
        (selectedContextEighteenInheritedSensitiveBracket l r A)
        (selectedContextEighteenInheritedSensitiveBracket l r B)

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Compatibility with the actual FIVE original old selected19
comparison constructors, including genuine inherited-source unit
prepend/append operations; neither is general chain associativity. -/
theorem selectedLocalNineteen_preservesInheritedSensitiveBracket
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenInheritedSensitiveBracket l r M =
      selectedContextEighteenInheritedSensitiveBracket l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- Compatibility with ALL SEVEN new typed raw-congruence generators.
Both real raw chain contexts and genuine raw reversal are checked
without assuming any unwanted associativity of the source Type. -/
theorem selectedRawCongruent_preservesInheritedSensitiveBracket
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenInheritedSensitiveBracket l r M =
      selectedContextEighteenInheritedSensitiveBracket l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesInheritedSensitiveBracket l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      exact congrArg SelectedInheritedSensitiveRawBracket.reversed ih
  | rawChainRight A X ih =>
      exact congrArg
        (fun s : SelectedInheritedSensitiveRawBracket =>
          selectedInheritedSensitiveBracketJoin s
            (selectedContextEighteenInheritedSensitiveBracket l r X)) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun s : SelectedInheritedSensitiveRawBracket =>
          selectedInheritedSensitiveBracketJoin
            (selectedContextEighteenInheritedSensitiveBracket l r X) s) ih

/-- Actual seven-generator quotient descent, using the typed
preservation proof rather than choosing raw representatives. -/
def selectedRawCongruentInheritedSensitiveBracketOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedInheritedSensitiveRawBracket :=
  Quotient.lift (selectedContextEighteenInheritedSensitiveBracket l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesInheritedSensitiveBracket l r A)

theorem selectedRawCongruentInheritedSensitiveBracket_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentInheritedSensitiveBracketOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenInheritedSensitiveBracket l r M := rfl

/-- Independently descend to the ACTUAL old five-generator quotient. -/
def selectedNineteenInheritedSensitiveBracketOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) →
      SelectedInheritedSensitiveRawBracket :=
  Quotient.lift (selectedContextEighteenInheritedSensitiveBracket l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesInheritedSensitiveBracket l r A)

/-- Independent old and new quotient descents agree on the original
old-to-new projection; they are not claims of equal comparison Types. -/
theorem selectedInheritedSensitiveBracket_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentInheritedSensitiveBracketOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenInheritedSensitiveBracketOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Genuine ORIGINAL inherited old18D strict and raw reverse loops
in one fixed N -> N dependent fiber. -/
def selectedInheritedSensitiveSourceLoop
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .inherited (.strict N)

def selectedInheritedSensitiveReverseLoop
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (.strict N)

/-- Original left-associated raw contextual18D witness (I R) I. -/
def selectedInheritedSensitiveWitnessLeft
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain
    (.chain (selectedInheritedSensitiveSourceLoop l r N)
      (selectedInheritedSensitiveReverseLoop l r N))
    (selectedInheritedSensitiveSourceLoop l r N)

/-- Original right-associated witness I (R I), same dependent fiber. -/
def selectedInheritedSensitiveWitnessRight
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain (selectedInheritedSensitiveSourceLoop l r N)
    (.chain (selectedInheritedSensitiveReverseLoop l r N)
      (selectedInheritedSensitiveSourceLoop l r N))

/-- These are independent FREE brackets, not equalities of Type values.
They differ in the genuine raw chain parenthesization retained between
two inherited-source atoms and one reversal. -/
def selectedInheritedSensitiveLeftValue :
    SelectedInheritedSensitiveRawBracket :=
  .joined (.joined .source (.reversed .unit)) .source

def selectedInheritedSensitiveRightValue :
    SelectedInheritedSensitiveRawBracket :=
  .joined .source (.joined (.reversed .unit) .source)

theorem selectedInheritedSensitive_leftValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedSensitiveBracket l r
        (selectedInheritedSensitiveWitnessLeft l r N) =
      selectedInheritedSensitiveLeftValue := rfl

theorem selectedInheritedSensitive_rightValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedSensitiveBracket l r
        (selectedInheritedSensitiveWitnessRight l r N) =
      selectedInheritedSensitiveRightValue := rfl

theorem selectedInheritedSensitive_valuesDistinct :
    selectedInheritedSensitiveLeftValue ≠
      selectedInheritedSensitiveRightValue := by
  decide

theorem selectedInheritedSensitive_witnessBracketDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedSensitiveBracket l r
        (selectedInheritedSensitiveWitnessLeft l r N) ≠
      selectedContextEighteenInheritedSensitiveBracket l r
        (selectedInheritedSensitiveWitnessRight l r N) := by
  rw [selectedInheritedSensitive_leftValue l r N,
    selectedInheritedSensitive_rightValue l r N]
  exact selectedInheritedSensitive_valuesDistinct

/-- Every degree of the COMPLETE original ancestor tower agrees.
Only associativity of numerical Nat addition is used; no raw18D
chain-associativity equality or proof-value rewrite is assumed. -/
theorem selectedInheritedSensitive_witnessAncestorTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (degree : Nat) :
    selectedAncestorTowerCount l r degree
        (selectedInheritedSensitiveWitnessLeft l r N) =
      selectedAncestorTowerCount l r degree
        (selectedInheritedSensitiveWitnessRight l r N) := by
  cases degree with
  | zero => rfl
  | succ d =>
      change
        (selectedAncestorTowerCount l r (d + 1)
            (selectedInheritedSensitiveSourceLoop l r N) +
          selectedAncestorTowerCount l r (d + 1)
            (selectedInheritedSensitiveReverseLoop l r N)) +
          selectedAncestorTowerCount l r (d + 1)
            (selectedInheritedSensitiveSourceLoop l r N) =
        selectedAncestorTowerCount l r (d + 1)
            (selectedInheritedSensitiveSourceLoop l r N) +
          (selectedAncestorTowerCount l r (d + 1)
              (selectedInheritedSensitiveReverseLoop l r N) +
            selectedAncestorTowerCount l r (d + 1)
              (selectedInheritedSensitiveSourceLoop l r N))
      exact Nat.add_assoc _ _ _

/-- All degrees of the COMPLETE direct raw consecutive-reversal tower
also agree, again without imposing associativity on original proofs. -/
theorem selectedInheritedSensitive_witnessRunTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (degree : Nat) :
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedInheritedSensitiveWitnessLeft l r N) =
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedInheritedSensitiveWitnessRight l r N) := by
  change
    (selectedContextEighteenConsecutiveRunCount l r degree
        (selectedInheritedSensitiveSourceLoop l r N) +
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedInheritedSensitiveReverseLoop l r N)) +
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedInheritedSensitiveSourceLoop l r N) =
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedInheritedSensitiveSourceLoop l r N) +
      (selectedContextEighteenConsecutiveRunCount l r degree
        (selectedInheritedSensitiveReverseLoop l r N) +
       selectedContextEighteenConsecutiveRunCount l r degree
        (selectedInheritedSensitiveSourceLoop l r N))
  exact Nat.add_assoc _ _ _

/-- The entire v5.73 joint observer, including both untruncated
function-valued towers, matches on the true association pair.
The full function-valued equality is proved extensionally. -/
theorem selectedInheritedSensitive_witnessRootInnerObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentDoubleBracketCountRootInnerObservation l r N N
        (selectedRawCongruentClass l r
          (selectedInheritedSensitiveWitnessLeft l r N)) =
      selectedRawCongruentDoubleBracketCountRootInnerObservation l r N N
        (selectedRawCongruentClass l r
          (selectedInheritedSensitiveWitnessRight l r N)) := by
  have hbase :
      selectedRawCongruentFullDoubleOrderedBracketObservation l r N N
          (selectedRawCongruentClass l r
            (selectedInheritedSensitiveWitnessLeft l r N)) =
        selectedRawCongruentFullDoubleOrderedBracketObservation l r N N
          (selectedRawCongruentClass l r
            (selectedInheritedSensitiveWitnessRight l r N)) := by
    apply Prod.ext
    · apply Prod.ext
      · apply Prod.ext
        · apply Prod.ext
          · rfl
          · funext degree
            exact selectedInheritedSensitive_witnessAncestorTowerEq l r N degree
        · funext degree
          exact selectedInheritedSensitive_witnessRunTowerEq l r N degree
      · rfl
    · rfl
  apply Prod.ext
  · apply Prod.ext
    · apply Prod.ext
      · exact hbase
      · rfl
    · rfl
  · rfl

/-- The complete v5.74 ordered reversal-site count is [0] for both
genuine raw terms, including their true inherited old18D leaves. -/
theorem selectedInheritedSensitive_leftSites
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedInheritedSensitiveWitnessLeft l r N) = [0] := rfl

theorem selectedInheritedSensitive_rightSites
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedInheritedSensitiveWitnessRight l r N) = [0] := rfl

/-- The COMPLETE v5.75 ordered raw reversal/inherited event WORD is
[I, R, I] for both genuinely different parenthesizations. -/
theorem selectedInheritedSensitive_leftWord
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseInheritedWord l r
        (selectedInheritedSensitiveWitnessLeft l r N) =
      [.inherited, .rawReverse, .inherited] := rfl

theorem selectedInheritedSensitive_rightWord
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseInheritedWord l r
        (selectedInheritedSensitiveWitnessRight l r N) =
      [.inherited, .rawReverse, .inherited] := rfl

/-- Augment the COMPLETE v5.74 joint quotient observer by the
independently descended full v5.75 event word; no finite sampling. -/
abbrev SelectedDoubleBracketCountRootInnerSitesWordValue :=
  SelectedDoubleBracketCountRootInnerSitesValue ×
    List SelectedReverseInheritedEvent

def selectedRawCongruentDoubleBracketCountRootInnerSitesWordObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedDoubleBracketCountRootInnerSitesWordValue :=
  fun q =>
    (selectedRawCongruentDoubleBracketCountRootInnerSitesObservation l r J N q,
      selectedRawCongruentReverseInheritedWordOnQuotient l r J N q)

/-- Same genuine quotient observation through ALL v5.75 components,
including the full inherited-source inner brackets and the full
new event word; only the independently descended new bracket differs. -/
theorem selectedInheritedSensitive_witnessFullObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentDoubleBracketCountRootInnerSitesWordObservation l r N N
        (selectedRawCongruentClass l r
          (selectedInheritedSensitiveWitnessLeft l r N)) =
      selectedRawCongruentDoubleBracketCountRootInnerSitesWordObservation l r N N
        (selectedRawCongruentClass l r
          (selectedInheritedSensitiveWitnessRight l r N)) := by
  apply Prod.ext
  · apply Prod.ext
    · exact selectedInheritedSensitive_witnessRootInnerObservedEq l r N
    · rfl
  · rfl

/-- GENUINE seven-generator quotient classes are unequal. This uses
the actual separately DESCENDED bracket, not raw constructor
inequality as a substitute for the typed comparison relation. -/
theorem selectedInheritedSensitive_witnessClassDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentClass l r
        (selectedInheritedSensitiveWitnessLeft l r N) ≠
      selectedRawCongruentClass l r
        (selectedInheritedSensitiveWitnessRight l r N) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentInheritedSensitiveBracketOnQuotient l r N N) h
  change selectedContextEighteenInheritedSensitiveBracket l r
      (selectedInheritedSensitiveWitnessLeft l r N) =
    selectedContextEighteenInheritedSensitiveBracket l r
      (selectedInheritedSensitiveWitnessRight l r N) at hc
  exact (selectedInheritedSensitive_witnessBracketDistinct l r N) hc

/-- No actual seven-generator Type-valued 19D comparison of these
two genuine original contextual18D values exists. -/
theorem selectedInheritedSensitive_witnessNoComparison
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedInheritedSensitiveWitnessLeft l r N)
      (selectedInheritedSensitiveWitnessRight l r N)) := by
  rintro ⟨A⟩
  exact (selectedInheritedSensitive_witnessClassDistinct l r N)
    (Quotient.sound ⟨A⟩)

/-- The COMPLETE v5.75 quotient observer is noninjective on every
genuinely inhabited ORIGINAL 17D endomorphism fiber N -> N. -/
theorem selectedInheritedSensitive_v575NotInjective
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentDoubleBracketCountRootInnerSitesWordObservation
        l r N N) := by
  intro hinj
  exact (selectedInheritedSensitive_witnessClassDistinct l r N)
    (hinj (selectedInheritedSensitive_witnessFullObservedEq l r N))

/-- The full previous v5.75 observation cannot decode the new
independently descended source-sensitive association bracket. -/
theorem selectedInheritedSensitive_noBracketDecoder
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ ∃ decode :
        SelectedDoubleBracketCountRootInnerSitesWordValue →
          SelectedInheritedSensitiveRawBracket,
      ∀ q : Quotient (selectedRawCongruentSetoid l r N N),
        decode
            (selectedRawCongruentDoubleBracketCountRootInnerSitesWordObservation
              l r N N q) =
          selectedRawCongruentInheritedSensitiveBracketOnQuotient
            l r N N q := by
  rintro ⟨decode, h⟩
  have hc :
      selectedRawCongruentInheritedSensitiveBracketOnQuotient l r N N
          (selectedRawCongruentClass l r
            (selectedInheritedSensitiveWitnessLeft l r N)) =
        selectedRawCongruentInheritedSensitiveBracketOnQuotient l r N N
          (selectedRawCongruentClass l r
            (selectedInheritedSensitiveWitnessRight l r N)) := by
    calc
      _ = decode
          (selectedRawCongruentDoubleBracketCountRootInnerSitesWordObservation
            l r N N (selectedRawCongruentClass l r
              (selectedInheritedSensitiveWitnessLeft l r N))) := (h _).symm
      _ = decode
          (selectedRawCongruentDoubleBracketCountRootInnerSitesWordObservation
            l r N N (selectedRawCongruentClass l r
              (selectedInheritedSensitiveWitnessRight l r N))) :=
        congrArg decode (selectedInheritedSensitive_witnessFullObservedEq l r N)
      _ = _ := h _
  change selectedContextEighteenInheritedSensitiveBracket l r
      (selectedInheritedSensitiveWitnessLeft l r N) =
    selectedContextEighteenInheritedSensitiveBracket l r
      (selectedInheritedSensitiveWitnessRight l r N) at hc
  exact (selectedInheritedSensitive_witnessBracketDistinct l r N) hc

/-- The full v5.75 observation admits no inverse decoder for all
actual new quotient classes in a genuine N -> N endomorphism fiber. -/
theorem selectedInheritedSensitive_noClassDecoder
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ ∃ decode :
        SelectedDoubleBracketCountRootInnerSitesWordValue →
          Quotient (selectedRawCongruentSetoid l r N N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r N N),
        decode
            (selectedRawCongruentDoubleBracketCountRootInnerSitesWordObservation
              l r N N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedInheritedSensitive_v575NotInjective l r N
  intro a b hab
  calc
    a = decode
        (selectedRawCongruentDoubleBracketCountRootInnerSitesWordObservation
          l r N N a) := (h a).symm
    _ = decode
        (selectedRawCongruentDoubleBracketCountRootInnerSitesWordObservation
          l r N N b) := congrArg decode hab
    _ = b := h b

end ExactFiber

#print axioms PentagonAdjoinedSixCell.SelectedInheritedSensitiveRawBracket
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitiveBracketJoin
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenInheritedSensitiveBracket
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesInheritedSensitiveBracket
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesInheritedSensitiveBracket
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentInheritedSensitiveBracketOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentInheritedSensitiveBracket_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenInheritedSensitiveBracketOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitiveBracket_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitiveSourceLoop
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitiveReverseLoop
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitiveWitnessLeft
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitiveWitnessRight
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitiveLeftValue
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitiveRightValue
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitive_leftValue
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitive_rightValue
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitive_valuesDistinct
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitive_witnessBracketDistinct
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitive_witnessAncestorTowerEq
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitive_witnessRunTowerEq
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitive_witnessRootInnerObservedEq
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitive_leftSites
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitive_rightSites
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitive_leftWord
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitive_rightWord
#print axioms PentagonAdjoinedSixCell.SelectedDoubleBracketCountRootInnerSitesWordValue
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentDoubleBracketCountRootInnerSitesWordObservation
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitive_witnessFullObservedEq
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitive_witnessClassDistinct
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitive_witnessNoComparison
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitive_v575NotInjective
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitive_noBracketDecoder
#print axioms PentagonAdjoinedSixCell.selectedInheritedSensitive_noClassDecoder

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
