import KUOS.Architecture.QiWuxingGK5CHP77OrderedInheritedRootResidualV5_72

/-!
Qi v5.73 — the TRUE old18D inherited-source INNER NONASSOCIATIVE
BRACKET remains after observing ALL v5.72 quotient invariants,
including the complete ordered source-ROOT list.

The original dependent SelectedLocalEighteen proof constructors
strict, unitLeft, unitRight, reverse and chain are interpreted by
an independently named free nonassociative source-inner syntax.
This is an observation of the genuine old18D Type-valued proof,
NOT an equality or replacement of the old evidence.

An ordered list of these inner source brackets is read at genuine
inherited leaves of the original contextual raw18D proof. This
observation is proved invariant under every one of the FIVE original
selected19 comparison constructors and the SEVEN independent
new raw-congruence comparison constructors. Separate original and
new Quotient.lift descents, compatible with the old-to-new projection,
are constructed without changing either comparison Type.

Genuine same-fiber source pair, for an actual 17D N:
  Aold := chain (chain (strict N) (strict N)) (strict N)
  Bold := chain (strict N) (chain (strict N) (strict N))
  A := reverse (inherited Aold)
  B := reverse (inherited Bold)
The TRUE old18D values have the SAME root chain, but different
nonassociative inner binary bracket trees. The contextual18D raw
witnesses agree on all nine observations, BOTH complete Nat-indexed
infinite towers, complete ordered reverse-run list, unit-reduced
raw18D bracket, inherited-leaf count AND ordered inherited-root list
[chain]. Yet the new descended internal old18D bracket lists differ,
so their actual new seven-generator quotient classes differ and no
typed new19 comparison exists.

The result persists after pasting an ACTUALLY SUPPLIED source
M:J->N, only in that SAME genuinely inhabited dependent fiber.
No arbitrary heterogeneous-fiber inhabitance or global quotient
classification is claimed. Root tags and even these old18D inner
brackets need not classify full old18D source Type values. No 20D
gluing, cross-WORLD descent, philosophical identification, or action
authority. Original Type18D values, both old/new Type19 comparisons,
public root107, pinned Lean/mathlib and protected #1558 untouched.
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

/-- An independent free NONASSOCIATIVE raw syntax of ORIGINAL old18D
proof constructors, not the original dependent old18D Type itself. -/
inductive SelectedInheritedOldInnerBracket : Type where
  | oldStrict : SelectedInheritedOldInnerBracket
  | oldUnitLeft : SelectedInheritedOldInnerBracket
  | oldUnitRight : SelectedInheritedOldInnerBracket
  | oldReversed : SelectedInheritedOldInnerBracket →
      SelectedInheritedOldInnerBracket
  | oldJoined : SelectedInheritedOldInnerBracket →
      SelectedInheritedOldInnerBracket →
      SelectedInheritedOldInnerBracket
  deriving DecidableEq, Repr

/-- Structural reading of an ACTUAL old18D dependent proof, including
its internal binary bracketing. Crucially, no associativity equation
is imposed on old raw chain. Unit generators remain distinct labels. -/
def selectedLocalEighteenInnerBracket (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (A : SelectedLocalEighteen W l r J N) :
    SelectedInheritedOldInnerBracket :=
  match A with
  | .strict _ => .oldStrict
  | .unitLeft _ _ _ _ _ => .oldUnitLeft
  | .unitRight _ _ _ _ _ => .oldUnitRight
  | .reverse B =>
      .oldReversed (selectedLocalEighteenInnerBracket l r B)
  | .chain B C =>
      .oldJoined (selectedLocalEighteenInnerBracket l r B)
        (selectedLocalEighteenInnerBracket l r C)

/-- Ordered internal old18D proof syntax at ACTUAL inherited leaves
of a contextual raw18D proof. Strict raw18D identities are empty;
raw reversal and whiskering preserve the list, raw chain appends. -/
def selectedContextEighteenInheritedInnerList (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    List SelectedInheritedOldInnerBracket :=
  match M with
  | .inherited A => [selectedLocalEighteenInnerBracket l r A]
  | .whiskerLeft _ _ _ A =>
      selectedContextEighteenInheritedInnerList l r A
  | .whiskerRight _ _ A _ =>
      selectedContextEighteenInheritedInnerList l r A
  | .strict _ => []
  | .reverse A => selectedContextEighteenInheritedInnerList l r A
  | .chain A B =>
      selectedContextEighteenInheritedInnerList l r A ++
        selectedContextEighteenInheritedInnerList l r B

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- All FIVE actual OLD selected19 comparison generators preserve the
full ordered source-inner bracket list. Old unitPrepend/Append only
insert a raw contextual strict, never rewrite inherited old18D. -/
theorem selectedLocalNineteen_preservesInheritedInnerList
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenInheritedInnerList l r M =
      selectedContextEighteenInheritedInnerList l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- All SEVEN genuine NEW raw congruence comparison constructors
preserve this inner bracket list. In particular raw reversal and both
raw chain contexts use the real typed induction hypothesis. -/
theorem selectedRawCongruent_preservesInheritedInnerList
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenInheritedInnerList l r M =
      selectedContextEighteenInheritedInnerList l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesInheritedInnerList l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih => exact ih
  | rawChainRight A X ih =>
      exact congrArg
        (fun s : List SelectedInheritedOldInnerBracket =>
          s ++ selectedContextEighteenInheritedInnerList l r X) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun s : List SelectedInheritedOldInnerBracket =>
          selectedContextEighteenInheritedInnerList l r X ++ s) ih

/-- Descent into the ACTUAL seven-generator quotient, justified
by compatibility with every typed new comparison generator. -/
def selectedRawCongruentInheritedInnerListOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      List SelectedInheritedOldInnerBracket :=
  Quotient.lift (selectedContextEighteenInheritedInnerList l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesInheritedInnerList l r A)

theorem selectedRawCongruentInheritedInnerList_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentInheritedInnerListOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenInheritedInnerList l r M := rfl

/-- Independent OLD quotient descent. Do not replace the original
selected19 presentation by the new seven-generator congruence. -/
def selectedNineteenInheritedInnerListOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) →
      List SelectedInheritedOldInnerBracket :=
  Quotient.lift (selectedContextEighteenInheritedInnerList l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesInheritedInnerList l r A)

theorem selectedInheritedInnerList_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentInheritedInnerListOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenInheritedInnerListOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Genuine left-associated OLD 18D proof, not an observation proxy. -/
def selectedOldInnerLeftSource
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedLocalEighteen W l r N N :=
  .chain (.chain (.strict N) (.strict N)) (.strict N)

/-- Genuine right-associated OLD 18D proof with identical endpoints,
number of strict leaves, and ROOT constructor, but different bracketing. -/
def selectedOldInnerRightSource
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedLocalEighteen W l r N N :=
  .chain (.strict N) (.chain (.strict N) (.strict N))

def selectedOldInnerLeftValue : SelectedInheritedOldInnerBracket :=
  .oldJoined (.oldJoined .oldStrict .oldStrict) .oldStrict

def selectedOldInnerRightValue : SelectedInheritedOldInnerBracket :=
  .oldJoined .oldStrict (.oldJoined .oldStrict .oldStrict)

theorem selectedOldInner_leftValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedLocalEighteenInnerBracket l r
        (selectedOldInnerLeftSource l r N) =
      selectedOldInnerLeftValue := rfl

theorem selectedOldInner_rightValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedLocalEighteenInnerBracket l r
        (selectedOldInnerRightSource l r N) =
      selectedOldInnerRightValue := rfl

theorem selectedOldInner_valuesDistinct :
    selectedOldInnerLeftValue ≠ selectedOldInnerRightValue := by
  decide

theorem selectedOldInner_sourceShapeDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedLocalEighteenInnerBracket l r
        (selectedOldInnerLeftSource l r N) ≠
      selectedLocalEighteenInnerBracket l r
        (selectedOldInnerRightSource l r N) := by
  rw [selectedOldInner_leftValue l r N,
    selectedOldInner_rightValue l r N]
  exact selectedOldInner_valuesDistinct

/-- Both actual old18D source values have ROOT chain: v5.72
root-only observation does not identify their full source syntax. -/
theorem selectedOldInner_sourceRootEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedLocalEighteenSourceRootTag l r
        (selectedOldInnerLeftSource l r N) =
      selectedLocalEighteenSourceRootTag l r
        (selectedOldInnerRightSource l r N) := rfl

/-- A genuine contextual18D witness whose inherited OLD proof has
left-associated old18D composition, wrapped in the same raw reverse. -/
def selectedOldInnerLeftWitness
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (.inherited (selectedOldInnerLeftSource l r N))

def selectedOldInnerRightWitness
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (.inherited (selectedOldInnerRightSource l r N))

theorem selectedOldInner_leftWitnessValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedInnerList l r
        (selectedOldInnerLeftWitness l r N) =
      [selectedOldInnerLeftValue] := rfl

theorem selectedOldInner_rightWitnessValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedInnerList l r
        (selectedOldInnerRightWitness l r N) =
      [selectedOldInnerRightValue] := rfl

theorem selectedOldInner_witnessInnerDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedInnerList l r
        (selectedOldInnerLeftWitness l r N) ≠
      selectedContextEighteenInheritedInnerList l r
        (selectedOldInnerRightWitness l r N) := by
  rw [selectedOldInner_leftWitnessValue l r N,
    selectedOldInner_rightWitnessValue l r N]
  intro h
  have hc : selectedOldInnerLeftValue = selectedOldInnerRightValue :=
    (List.cons.inj h).1
  exact selectedOldInner_valuesDistinct hc

/-- Count remains one, and the ORDERED inherited source-ROOT list
is exactly [chain] for BOTH genuine 18D proof values. -/
theorem selectedOldInner_witnessCountEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedLeafCount l r
        (selectedOldInnerLeftWitness l r N) =
      selectedContextEighteenInheritedLeafCount l r
        (selectedOldInnerRightWitness l r N) := rfl

theorem selectedOldInner_witnessRootEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedRootList l r
        (selectedOldInnerLeftWitness l r N) =
      selectedContextEighteenInheritedRootList l r
        (selectedOldInnerRightWitness l r N) := rfl

/-- SAME nine observations, complete ancestral Nat->Nat tower,
complete consecutive-reversal Nat->Nat tower, ordered reverse runs,
and unit-reduced raw-context bracket of v5.70. -/
theorem selectedOldInner_witnessBaseObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentDoubleBracketInheritedCountObservation l r N N
        (selectedRawCongruentClass l r
          (selectedOldInnerLeftWitness l r N)) =
      selectedRawCongruentDoubleBracketInheritedCountObservation l r N N
        (selectedRawCongruentClass l r
          (selectedOldInnerRightWitness l r N)) := rfl

/-- The complete PREVIOUS observer with the v5.72 certified
ordered ROOT source-list component added. -/
abbrev SelectedDoubleBracketCountRootValue :=
  SelectedDoubleBracketInheritedCountValue ×
    List SelectedInheritedSourceRootTag

def selectedRawCongruentDoubleBracketCountRootObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedDoubleBracketCountRootValue :=
  fun q =>
    (selectedRawCongruentDoubleBracketInheritedCountObservation l r J N q,
      selectedRawCongruentInheritedRootListOnQuotient l r J N q)

theorem selectedOldInner_witnessFullObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentDoubleBracketCountRootObservation l r N N
        (selectedRawCongruentClass l r
          (selectedOldInnerLeftWitness l r N)) =
      selectedRawCongruentDoubleBracketCountRootObservation l r N N
        (selectedRawCongruentClass l r
          (selectedOldInnerRightWitness l r N)) := by
  exact Prod.ext (selectedOldInner_witnessBaseObservedEq l r N)
    (selectedOldInner_witnessRootEq l r N)

/-- Genuine NEW seven-generator quotient classes cannot be equal
because the independently descended inner source bracket lists differ. -/
theorem selectedOldInner_witnessClassDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentClass l r (selectedOldInnerLeftWitness l r N) ≠
      selectedRawCongruentClass l r (selectedOldInnerRightWitness l r N) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentInheritedInnerListOnQuotient l r N N) h
  change selectedContextEighteenInheritedInnerList l r
      (selectedOldInnerLeftWitness l r N) =
    selectedContextEighteenInheritedInnerList l r
      (selectedOldInnerRightWitness l r N) at hc
  exact (selectedOldInner_witnessInnerDistinct l r N) hc

theorem selectedOldInner_witnessNoComparison
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedOldInnerLeftWitness l r N)
      (selectedOldInnerRightWitness l r N)) := by
  rintro ⟨A⟩
  exact (selectedOldInner_witnessClassDistinct l r N)
    (Quotient.sound ⟨A⟩)

/-- Prefix cancellation of the genuine inherited SOURCE-INNER
BRACKET list; this is List cancellation, NOT raw proof associativity. -/
theorem selectedInheritedInnerList_prefixCancel
    (pre xs ys : List SelectedInheritedOldInnerBracket)
    (h : pre ++ xs = pre ++ ys) : xs = ys := by
  induction pre with
  | nil => simpa using h
  | cons a tail ih =>
      apply ih
      have hh : a :: (tail ++ xs) = a :: (tail ++ ys) := h
      exact (List.cons.inj hh).2

/-- Fiber extension requires an ACTUAL original M:J->N. -/
def selectedOldInnerFiberLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedOldInnerLeftWitness l r N)

def selectedOldInnerFiberRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedOldInnerRightWitness l r N)

theorem selectedOldInnerFiber_innerDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenInheritedInnerList l r
        (selectedOldInnerFiberLeft l r M) ≠
      selectedContextEighteenInheritedInnerList l r
        (selectedOldInnerFiberRight l r M) := by
  intro h
  change selectedContextEighteenInheritedInnerList l r M ++
      selectedContextEighteenInheritedInnerList l r
        (selectedOldInnerLeftWitness l r N) =
    selectedContextEighteenInheritedInnerList l r M ++
      selectedContextEighteenInheritedInnerList l r
        (selectedOldInnerRightWitness l r N) at h
  have hs := selectedInheritedInnerList_prefixCancel
    (selectedContextEighteenInheritedInnerList l r M)
    (selectedContextEighteenInheritedInnerList l r
      (selectedOldInnerLeftWitness l r N))
    (selectedContextEighteenInheritedInnerList l r
      (selectedOldInnerRightWitness l r N)) h
  exact (selectedOldInner_witnessInnerDistinct l r N) hs

theorem selectedOldInnerFiber_fullObservedEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentDoubleBracketCountRootObservation l r J N
        (selectedRawCongruentClass l r (selectedOldInnerFiberLeft l r M)) =
      selectedRawCongruentDoubleBracketCountRootObservation l r J N
        (selectedRawCongruentClass l r (selectedOldInnerFiberRight l r M)) := rfl

theorem selectedOldInnerFiber_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r (selectedOldInnerFiberLeft l r M) ≠
      selectedRawCongruentClass l r (selectedOldInnerFiberRight l r M) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentInheritedInnerListOnQuotient l r J N) h
  change selectedContextEighteenInheritedInnerList l r
      (selectedOldInnerFiberLeft l r M) =
    selectedContextEighteenInheritedInnerList l r
      (selectedOldInnerFiberRight l r M) at hc
  exact (selectedOldInnerFiber_innerDistinct l r M) hc

theorem selectedDoubleBracketCountRoot_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedRawCongruentDoubleBracketCountRootObservation l r J N) := by
  intro hinj
  exact (selectedOldInnerFiber_classDistinct l r M)
    (hinj (selectedOldInnerFiber_fullObservedEq l r M))

theorem selectedDoubleBracketCountRoot_noInnerDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode :
        SelectedDoubleBracketCountRootValue →
          List SelectedInheritedOldInnerBracket,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentDoubleBracketCountRootObservation l r J N q) =
          selectedRawCongruentInheritedInnerListOnQuotient l r J N q := by
  rintro ⟨decode, h⟩
  have hc :
      selectedRawCongruentInheritedInnerListOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedOldInnerFiberLeft l r M)) =
        selectedRawCongruentInheritedInnerListOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedOldInnerFiberRight l r M)) := by
    calc
      _ = decode (selectedRawCongruentDoubleBracketCountRootObservation l r J N
            (selectedRawCongruentClass l r (selectedOldInnerFiberLeft l r M))) :=
        (h _).symm
      _ = decode (selectedRawCongruentDoubleBracketCountRootObservation l r J N
            (selectedRawCongruentClass l r (selectedOldInnerFiberRight l r M))) :=
        congrArg decode (selectedOldInnerFiber_fullObservedEq l r M)
      _ = _ := h _
  change selectedContextEighteenInheritedInnerList l r
      (selectedOldInnerFiberLeft l r M) =
    selectedContextEighteenInheritedInnerList l r
      (selectedOldInnerFiberRight l r M) at hc
  exact (selectedOldInnerFiber_innerDistinct l r M) hc

theorem selectedDoubleBracketCountRoot_noClassDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode : SelectedDoubleBracketCountRootValue →
        Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentDoubleBracketCountRootObservation l r J N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedDoubleBracketCountRoot_notInjective l r M
  intro a b hab
  calc
    a = decode (selectedRawCongruentDoubleBracketCountRootObservation l r J N a) :=
      (h a).symm
    _ = decode (selectedRawCongruentDoubleBracketCountRootObservation l r J N b) :=
      congrArg decode hab
    _ = b := h b

theorem selectedDoubleBracketCountRoot_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentDoubleBracketCountRootObservation l r J J) :=
  selectedDoubleBracketCountRoot_notInjective l r (.strict J)

end ExactFiber

#print axioms PentagonAdjoinedSixCell.SelectedInheritedOldInnerBracket
#print axioms PentagonAdjoinedSixCell.selectedLocalEighteenInnerBracket
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenInheritedInnerList
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesInheritedInnerList
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesInheritedInnerList
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentInheritedInnerListOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentInheritedInnerList_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenInheritedInnerListOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedInheritedInnerList_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedOldInnerLeftSource
#print axioms PentagonAdjoinedSixCell.selectedOldInnerRightSource
#print axioms PentagonAdjoinedSixCell.selectedOldInnerLeftValue
#print axioms PentagonAdjoinedSixCell.selectedOldInnerRightValue
#print axioms PentagonAdjoinedSixCell.selectedOldInner_leftValue
#print axioms PentagonAdjoinedSixCell.selectedOldInner_rightValue
#print axioms PentagonAdjoinedSixCell.selectedOldInner_valuesDistinct
#print axioms PentagonAdjoinedSixCell.selectedOldInner_sourceShapeDistinct
#print axioms PentagonAdjoinedSixCell.selectedOldInner_sourceRootEq
#print axioms PentagonAdjoinedSixCell.selectedOldInnerLeftWitness
#print axioms PentagonAdjoinedSixCell.selectedOldInnerRightWitness
#print axioms PentagonAdjoinedSixCell.selectedOldInner_leftWitnessValue
#print axioms PentagonAdjoinedSixCell.selectedOldInner_rightWitnessValue
#print axioms PentagonAdjoinedSixCell.selectedOldInner_witnessInnerDistinct
#print axioms PentagonAdjoinedSixCell.selectedOldInner_witnessCountEq
#print axioms PentagonAdjoinedSixCell.selectedOldInner_witnessRootEq
#print axioms PentagonAdjoinedSixCell.selectedOldInner_witnessBaseObservedEq
#print axioms PentagonAdjoinedSixCell.SelectedDoubleBracketCountRootValue
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentDoubleBracketCountRootObservation
#print axioms PentagonAdjoinedSixCell.selectedOldInner_witnessFullObservedEq
#print axioms PentagonAdjoinedSixCell.selectedOldInner_witnessClassDistinct
#print axioms PentagonAdjoinedSixCell.selectedOldInner_witnessNoComparison
#print axioms PentagonAdjoinedSixCell.selectedInheritedInnerList_prefixCancel
#print axioms PentagonAdjoinedSixCell.selectedOldInnerFiberLeft
#print axioms PentagonAdjoinedSixCell.selectedOldInnerFiberRight
#print axioms PentagonAdjoinedSixCell.selectedOldInnerFiber_innerDistinct
#print axioms PentagonAdjoinedSixCell.selectedOldInnerFiber_fullObservedEq
#print axioms PentagonAdjoinedSixCell.selectedOldInnerFiber_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedDoubleBracketCountRoot_notInjective
#print axioms PentagonAdjoinedSixCell.selectedDoubleBracketCountRoot_noInnerDecoder
#print axioms PentagonAdjoinedSixCell.selectedDoubleBracketCountRoot_noClassDecoder
#print axioms PentagonAdjoinedSixCell.selectedDoubleBracketCountRoot_endomorphismNotInjective

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
