import KUOS.Architecture.QiWuxingGK5CHP77InheritedProvenanceAfterBracketV5_71

/-!
Qi v5.72 — even after adding the number of actual inherited old18D
leaves to the complete v5.71 observer, the ORDER of their SOURCE ROOT
constructors can remain undetermined in a genuine dependent fiber.

The actual ORIGINAL SelectedLocalEighteen proof Type has five raw
constructors: strict, unitLeft, unitRight, reverse, chain. A new
independent five-tag reading of the ROOT constructor is performed only
on a genuinely supplied inherited old18D evidence leaf. A second
structural recursion over ORIGINAL contextual 18D raw evidence reads
the ordered list of these tags. The list is preserved by ALL FIVE
old selected19 and ALL SEVEN new raw-congruence generators. Separate
old/new Quotient.lift constructions and exact projection factorization
are proved, with NO new comparison generators.

Concrete original true 17D endomorphism N->N:
  X = reverse (inherited (SelectedLocalEighteen.strict N))
  Y = reverse (inherited
        (SelectedLocalEighteen.chain
          (SelectedLocalEighteen.strict N)
          (SelectedLocalEighteen.strict N)))
  A = chain X Y
  B = chain Y X

The original nine observations, complete ancestor tower (Nat->Nat),
complete direct-reverse-run tower (Nat->Nat), ordered raw-run list,
nonassociative unit-reduced bracket tree, and inherited-leaf COUNT
all agree. The new invariant ordered source-root lists are
[strict, chain] and [chain, strict], hence distinguish actual new
seven-generator quotient classes. With any ACTUALLY SUPPLIED original
M:J->N, common-prefix cancellation preserves this obstruction within
that same dependent fiber; no heterogeneous source inhabitance is
invented.

ROOT TAGS do not reconstruct arbitrary original old18D values, even
if the tags are equal, and this local noninjectivity does not classify
the quotient or prove global 20D gluing, all-WORLD descent or action
authority. Original proof Type values, both old/new typed19
presentations, public root107, fixed Lean/mathlib and protected
validation-only #1558 remain unchanged.
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

/-- A separate finite label of the TOP constructor of a truly supplied
old18D dependent proof. No two original proofs are identified. -/
inductive SelectedInheritedSourceRootTag where
  | strict
  | unitLeft
  | unitRight
  | reverse
  | chain
  deriving DecidableEq, Repr

/-- Read the top raw constructor of an actual old selected 18D proof;
no attempt is made to compare inhabitants of unrelated fibers. -/
def selectedLocalEighteenSourceRootTag (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    SelectedInheritedSourceRootTag :=
  match M with
  | .strict _ => .strict
  | .unitLeft _ _ _ _ => .unitLeft
  | .unitRight _ _ _ _ => .unitRight
  | .reverse _ => .reverse
  | .chain _ _ => .chain

/-- Ordered provenance of genuinely inherited old18D SOURCE ROOTS
inside original contextual raw18D proofs. Raw strict contributes no
inherited leaf; raw reverse/whiskering retain order; raw chain
concatenates, without assuming associativity of original raw proofs. -/
def selectedContextEighteenInheritedRootList (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    List SelectedInheritedSourceRootTag :=
  match M with
  | .inherited A => [selectedLocalEighteenSourceRootTag l r A]
  | .whiskerLeft _ _ _ A =>
      selectedContextEighteenInheritedRootList l r A
  | .whiskerRight _ _ A _ =>
      selectedContextEighteenInheritedRootList l r A
  | .strict _ => []
  | .reverse A => selectedContextEighteenInheritedRootList l r A
  | .chain A B =>
      selectedContextEighteenInheritedRootList l r A ++
        selectedContextEighteenInheritedRootList l r B

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Each of the five ORIGINAL old selected19 comparison generators
preserves the entire ordered inherited SOURCE-ROOT tag sequence. The
unit insertions delete only raw strict units, not inherited leaves. -/
theorem selectedLocalNineteen_preservesInheritedRootList
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenInheritedRootList l r M =
      selectedContextEighteenInheritedRootList l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- All SEVEN NEW typed19 comparison constructors preserve the
ordered inherited source-root tag list, including raw reverse and
BOTH true raw chain contextual congruences. -/
theorem selectedRawCongruent_preservesInheritedRootList
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenInheritedRootList l r M =
      selectedContextEighteenInheritedRootList l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesInheritedRootList l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih => exact ih
  | rawChainRight A X ih =>
      exact congrArg
        (fun s : List SelectedInheritedSourceRootTag =>
          s ++ selectedContextEighteenInheritedRootList l r X) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun s : List SelectedInheritedSourceRootTag =>
          selectedContextEighteenInheritedRootList l r X ++ s) ih

/-- This root-order observation descends to the ACTUAL seven-generator
19D quotient by witnessed compatibility, not preference. -/
def selectedRawCongruentInheritedRootListOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      List SelectedInheritedSourceRootTag :=
  Quotient.lift (selectedContextEighteenInheritedRootList l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesInheritedRootList l r A)

theorem selectedRawCongruentInheritedRootList_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentInheritedRootListOnQuotient l r J N
      (selectedRawCongruentClass l r M) =
        selectedContextEighteenInheritedRootList l r M := rfl

/-- Separate OLD selected19 quotient descent without identifying
old and new independent typed19 comparison presentations. -/
def selectedNineteenInheritedRootListOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) →
      List SelectedInheritedSourceRootTag :=
  Quotient.lift (selectedContextEighteenInheritedRootList l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesInheritedRootList l r A)

theorem selectedInheritedRootList_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentInheritedRootListOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenInheritedRootListOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- An actual original old18D strict identity of fixed 17D boundary. -/
def selectedInheritedOldStrict
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedLocalEighteen W l r N N :=
  .strict N

/-- An actual, distinctly CONSTRUCTED old18D proof with the SAME
dependent endpoints, using raw old18D composition, not a proxy. -/
def selectedInheritedOldChain
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedLocalEighteen W l r N N :=
  .chain (.strict N) (.strict N)

/-- Both source proofs are wrapped in the same original raw18D
inherited/reverse constructors; the hidden original proof differs. -/
def selectedInheritedStrictLoop
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (.inherited (selectedInheritedOldStrict l r N))

def selectedInheritedChainLoop
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (.inherited (selectedInheritedOldChain l r N))

/-- The same TWO inherited leaves occur in opposite raw chain order,
with precisely matching genuine original 17D endpoints. -/
def selectedInheritedOrderWitnessLeft
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain (selectedInheritedStrictLoop l r N)
    (selectedInheritedChainLoop l r N)

def selectedInheritedOrderWitnessRight
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain (selectedInheritedChainLoop l r N)
    (selectedInheritedStrictLoop l r N)

theorem selectedInheritedOrder_leftRootValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedRootList l r
        (selectedInheritedOrderWitnessLeft l r N) =
      [SelectedInheritedSourceRootTag.strict,
        SelectedInheritedSourceRootTag.chain] := rfl

theorem selectedInheritedOrder_rightRootValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedRootList l r
        (selectedInheritedOrderWitnessRight l r N) =
      [SelectedInheritedSourceRootTag.chain,
        SelectedInheritedSourceRootTag.strict] := rfl

theorem selectedInheritedOrder_rootValuesDistinct :
    ([SelectedInheritedSourceRootTag.strict,
        SelectedInheritedSourceRootTag.chain] :
        List SelectedInheritedSourceRootTag) ≠
      [SelectedInheritedSourceRootTag.chain,
        SelectedInheritedSourceRootTag.strict] := by
  decide

theorem selectedInheritedOrder_witnessRootDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedRootList l r
        (selectedInheritedOrderWitnessLeft l r N) ≠
      selectedContextEighteenInheritedRootList l r
        (selectedInheritedOrderWitnessRight l r N) := by
  rw [selectedInheritedOrder_leftRootValue l r N,
    selectedInheritedOrder_rightRootValue l r N]
  exact selectedInheritedOrder_rootValuesDistinct

/-- Both actual old18D proofs contribute exactly ONE inherited leaf
each. No count difference is used for this new obstruction. -/
theorem selectedInheritedOrder_witnessCountEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedLeafCount l r
        (selectedInheritedOrderWitnessLeft l r N) =
      selectedContextEighteenInheritedLeafCount l r
        (selectedInheritedOrderWitnessRight l r N) := rfl

/-- Even the full v5.71 nine + BOTH complete Nat-indexed towers +
ordered run list + nonassociative unit-reduced bracket observer
cannot distinguish the original two different old18D source orders. -/
theorem selectedInheritedOrder_witnessBaseObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentFullDoubleOrderedBracketObservation l r N N
        (selectedRawCongruentClass l r
          (selectedInheritedOrderWitnessLeft l r N)) =
      selectedRawCongruentFullDoubleOrderedBracketObservation l r N N
        (selectedRawCongruentClass l r
          (selectedInheritedOrderWitnessRight l r N)) := rfl

/-- The complete observation AFTER adding the certified v5.71 count. -/
abbrev SelectedDoubleBracketInheritedCountValue :=
  SelectedFullDoubleOrderedBracketValue × Nat

def selectedRawCongruentDoubleBracketInheritedCountObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedDoubleBracketInheritedCountValue :=
  fun q => (selectedRawCongruentFullDoubleOrderedBracketObservation l r J N q,
    selectedRawCongruentInheritedLeafCountOnQuotient l r J N q)

theorem selectedInheritedOrder_witnessAugmentedObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentDoubleBracketInheritedCountObservation l r N N
        (selectedRawCongruentClass l r
          (selectedInheritedOrderWitnessLeft l r N)) =
      selectedRawCongruentDoubleBracketInheritedCountObservation l r N N
        (selectedRawCongruentClass l r
          (selectedInheritedOrderWitnessRight l r N)) := by
  exact Prod.ext (selectedInheritedOrder_witnessBaseObservedEq l r N)
    (selectedInheritedOrder_witnessCountEq l r N)

theorem selectedInheritedOrder_witnessClassDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentClass l r
        (selectedInheritedOrderWitnessLeft l r N) ≠
      selectedRawCongruentClass l r
        (selectedInheritedOrderWitnessRight l r N) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentInheritedRootListOnQuotient l r N N) h
  change selectedContextEighteenInheritedRootList l r
      (selectedInheritedOrderWitnessLeft l r N) =
    selectedContextEighteenInheritedRootList l r
      (selectedInheritedOrderWitnessRight l r N) at hc
  exact (selectedInheritedOrder_witnessRootDistinct l r N) hc

theorem selectedInheritedOrder_witnessNoComparison
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedInheritedOrderWitnessLeft l r N)
      (selectedInheritedOrderWitnessRight l r N)) := by
  rintro ⟨A⟩
  exact (selectedInheritedOrder_witnessClassDistinct l r N)
    (Quotient.sound ⟨A⟩)

/-- Exact left-list-prefix cancellation; use no raw18D
associativity and do not identify the original proof values. -/
theorem selectedInheritedRootList_prefixCancel
    (pre xs ys : List SelectedInheritedSourceRootTag)
    (h : pre ++ xs = pre ++ ys) : xs = ys := by
  induction pre with
  | nil => simpa using h
  | cons a tail ih =>
      apply ih
      have hh : a :: (tail ++ xs) = a :: (tail ++ ys) := h
      exact (List.cons.inj hh).2

/-- A source M:J->N MUST be provided. Composing with the two
endomorphism witnesses is done only in its original exact fiber. -/
def selectedInheritedOrderFiberLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedInheritedOrderWitnessLeft l r N)

def selectedInheritedOrderFiberRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedInheritedOrderWitnessRight l r N)

theorem selectedInheritedOrderFiber_rootDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenInheritedRootList l r
        (selectedInheritedOrderFiberLeft l r M) ≠
      selectedContextEighteenInheritedRootList l r
        (selectedInheritedOrderFiberRight l r M) := by
  intro h
  change selectedContextEighteenInheritedRootList l r M ++
      selectedContextEighteenInheritedRootList l r
        (selectedInheritedOrderWitnessLeft l r N) =
    selectedContextEighteenInheritedRootList l r M ++
      selectedContextEighteenInheritedRootList l r
        (selectedInheritedOrderWitnessRight l r N) at h
  have hs := selectedInheritedRootList_prefixCancel
    (selectedContextEighteenInheritedRootList l r M)
    (selectedContextEighteenInheritedRootList l r
      (selectedInheritedOrderWitnessLeft l r N))
    (selectedContextEighteenInheritedRootList l r
      (selectedInheritedOrderWitnessRight l r N)) h
  exact (selectedInheritedOrder_witnessRootDistinct l r N) hs

/-- Both entire old observers and the newly added inherited COUNT
remain equal after composition with the ACTUAL original prefix M. -/
theorem selectedInheritedOrderFiber_jointObservedEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentDoubleBracketInheritedCountObservation l r J N
        (selectedRawCongruentClass l r
          (selectedInheritedOrderFiberLeft l r M)) =
      selectedRawCongruentDoubleBracketInheritedCountObservation l r J N
        (selectedRawCongruentClass l r
          (selectedInheritedOrderFiberRight l r M)) := rfl

theorem selectedInheritedOrderFiber_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r (selectedInheritedOrderFiberLeft l r M) ≠
      selectedRawCongruentClass l r (selectedInheritedOrderFiberRight l r M) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentInheritedRootListOnQuotient l r J N) h
  change selectedContextEighteenInheritedRootList l r
      (selectedInheritedOrderFiberLeft l r M) =
    selectedContextEighteenInheritedRootList l r
      (selectedInheritedOrderFiberRight l r M) at hc
  exact (selectedInheritedOrderFiber_rootDistinct l r M) hc

theorem selectedDoubleBracketInheritedCount_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedRawCongruentDoubleBracketInheritedCountObservation l r J N) := by
  intro hinj
  exact (selectedInheritedOrderFiber_classDistinct l r M)
    (hinj (selectedInheritedOrderFiber_jointObservedEq l r M))

theorem selectedDoubleBracketInheritedCount_noRootDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode :
        SelectedDoubleBracketInheritedCountValue →
          List SelectedInheritedSourceRootTag,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentDoubleBracketInheritedCountObservation l r J N q) =
          selectedRawCongruentInheritedRootListOnQuotient l r J N q := by
  rintro ⟨decode, h⟩
  have hc :
      selectedRawCongruentInheritedRootListOnQuotient l r J N
          (selectedRawCongruentClass l r
            (selectedInheritedOrderFiberLeft l r M)) =
        selectedRawCongruentInheritedRootListOnQuotient l r J N
          (selectedRawCongruentClass l r
            (selectedInheritedOrderFiberRight l r M)) := by
    calc
      _ = decode (selectedRawCongruentDoubleBracketInheritedCountObservation l r J N
            (selectedRawCongruentClass l r
              (selectedInheritedOrderFiberLeft l r M))) :=
        (h _).symm
      _ = decode (selectedRawCongruentDoubleBracketInheritedCountObservation l r J N
            (selectedRawCongruentClass l r
              (selectedInheritedOrderFiberRight l r M))) :=
        congrArg decode (selectedInheritedOrderFiber_jointObservedEq l r M)
      _ = _ := h _
  change selectedContextEighteenInheritedRootList l r
      (selectedInheritedOrderFiberLeft l r M) =
    selectedContextEighteenInheritedRootList l r
      (selectedInheritedOrderFiberRight l r M) at hc
  exact (selectedInheritedOrderFiber_rootDistinct l r M) hc

theorem selectedDoubleBracketInheritedCount_noClassDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode :
        SelectedDoubleBracketInheritedCountValue →
          Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentDoubleBracketInheritedCountObservation l r J N q) =
          q := by
  rintro ⟨decode, h⟩
  apply selectedDoubleBracketInheritedCount_notInjective l r M
  intro a b hab
  calc
    a = decode (selectedRawCongruentDoubleBracketInheritedCountObservation l r J N a) :=
      (h a).symm
    _ = decode (selectedRawCongruentDoubleBracketInheritedCountObservation l r J N b) :=
      congrArg decode hab
    _ = b := h b

theorem selectedDoubleBracketInheritedCount_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentDoubleBracketInheritedCountObservation l r J J) :=
  selectedDoubleBracketInheritedCount_notInjective l r (.strict J)

end ExactFiber

#print axioms PentagonAdjoinedSixCell.SelectedInheritedSourceRootTag
#print axioms PentagonAdjoinedSixCell.selectedLocalEighteenSourceRootTag
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenInheritedRootList
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesInheritedRootList
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesInheritedRootList
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentInheritedRootListOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentInheritedRootList_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenInheritedRootListOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedInheritedRootList_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedInheritedOldStrict
#print axioms PentagonAdjoinedSixCell.selectedInheritedOldChain
#print axioms PentagonAdjoinedSixCell.selectedInheritedStrictLoop
#print axioms PentagonAdjoinedSixCell.selectedInheritedChainLoop
#print axioms PentagonAdjoinedSixCell.selectedInheritedOrderWitnessLeft
#print axioms PentagonAdjoinedSixCell.selectedInheritedOrderWitnessRight
#print axioms PentagonAdjoinedSixCell.selectedInheritedOrder_leftRootValue
#print axioms PentagonAdjoinedSixCell.selectedInheritedOrder_rightRootValue
#print axioms PentagonAdjoinedSixCell.selectedInheritedOrder_rootValuesDistinct
#print axioms PentagonAdjoinedSixCell.selectedInheritedOrder_witnessRootDistinct
#print axioms PentagonAdjoinedSixCell.selectedInheritedOrder_witnessCountEq
#print axioms PentagonAdjoinedSixCell.selectedInheritedOrder_witnessBaseObservedEq
#print axioms PentagonAdjoinedSixCell.SelectedDoubleBracketInheritedCountValue
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentDoubleBracketInheritedCountObservation
#print axioms PentagonAdjoinedSixCell.selectedInheritedOrder_witnessAugmentedObservedEq
#print axioms PentagonAdjoinedSixCell.selectedInheritedOrder_witnessClassDistinct
#print axioms PentagonAdjoinedSixCell.selectedInheritedOrder_witnessNoComparison
#print axioms PentagonAdjoinedSixCell.selectedInheritedRootList_prefixCancel
#print axioms PentagonAdjoinedSixCell.selectedInheritedOrderFiberLeft
#print axioms PentagonAdjoinedSixCell.selectedInheritedOrderFiberRight
#print axioms PentagonAdjoinedSixCell.selectedInheritedOrderFiber_rootDistinct
#print axioms PentagonAdjoinedSixCell.selectedInheritedOrderFiber_jointObservedEq
#print axioms PentagonAdjoinedSixCell.selectedInheritedOrderFiber_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedDoubleBracketInheritedCount_notInjective
#print axioms PentagonAdjoinedSixCell.selectedDoubleBracketInheritedCount_noRootDecoder
#print axioms PentagonAdjoinedSixCell.selectedDoubleBracketInheritedCount_noClassDecoder
#print axioms PentagonAdjoinedSixCell.selectedDoubleBracketInheritedCount_endomorphismNotInjective

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
