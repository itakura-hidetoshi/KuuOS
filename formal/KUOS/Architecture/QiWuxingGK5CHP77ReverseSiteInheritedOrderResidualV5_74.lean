import KUOS.Architecture.QiWuxingGK5CHP77OldInheritedInnerBracketResidualV5_73

/-!
Qi v5.74 — even after observing the COMPLETE v5.73 quotient signature,
the ordered distribution of genuine inherited old18D source leaves
among raw reversal SITES can remain invisible.

An independent observation of actual contextual18D dependent proofs
records, at each raw `reverse A` constructor, the true number of
`inherited(old18)` leaves inside its immediate original child `A`.
The ordered list of these site counts is preserved by the FIVE
original selected19 and ALL SEVEN new raw-congruence comparison
generators. It descends independently to both genuine quotients
and factors under the existing old-to-new quotient projection.
The relevant root and internal source Type values are NOT erased.

For any genuinely supplied original 17D endpoint N:
  R = reverse (strict N)
  I = reverse (inherited (SelectedLocalEighteen.strict N))
  A = chain R I
  B = chain I R
are ORIGINAL contextual18D dependent proof values in N->N.
The nine original observations, the complete Nat->Nat ancestor
tower and complete Nat->Nat direct reversal-run tower, the ordered
raw reversal-run list, the nonassociative unit-reduced contextual
bracket, inherited leaf count, ordered old18D root-tag list, and
ordered old18D FULL INNER BRACKET list all coincide.
Nevertheless the new reversal-site inherited-count lists are
[0,1] and [1,0] and thus distinguish actual new quotient classes.

Pasting a genuinely supplied original source M:J->N preserves the
obstruction in that exact fiber. The completed v5.73 signature is
noninjective there and cannot globally decode the new invariant
or all quotient classes. This is LOCAL: no uninhabited heterogeneous
fiber is silently populated, no free source equality, no global
quotient classification, 20D gluing, universal-WORLD descent,
philosophical proof or execution authority is claimed.

Original old18D Type-valued evidence, independent original/new
typed19 presentations, pinned Lean/mathlib, public root107 and
protected validation-only #1558 remain unchanged.
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

/-- At every ACTUAL raw reverse constructor, record the number of
truly inherited old18D leaves inside that constructor's original
immediate child. This new ORDERED list distinguishes relative
placement of strict-origin and inherited-origin reversal sites.
The original dependent Type18D evidence is not replaced. -/
def selectedContextEighteenReverseSiteInheritedCounts (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) : List Nat :=
  match M with
  | .inherited _ => []
  | .whiskerLeft _ _ _ A =>
      selectedContextEighteenReverseSiteInheritedCounts l r A
  | .whiskerRight _ _ A _ =>
      selectedContextEighteenReverseSiteInheritedCounts l r A
  | .strict _ => []
  | .reverse A =>
      selectedContextEighteenInheritedLeafCount l r A ::
        selectedContextEighteenReverseSiteInheritedCounts l r A
  | .chain A B =>
      selectedContextEighteenReverseSiteInheritedCounts l r A ++
        selectedContextEighteenReverseSiteInheritedCounts l r B

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- All FIVE original Type-valued 19D comparison generators preserve
the ordered reversal-site inherited-count list. Original unit
insertions delete raw strict nodes without erasing inherited leaves
or changing the number of inherited leaves in any enclosing reversal. -/
theorem selectedLocalNineteen_preservesReverseSiteInheritedCounts
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenReverseSiteInheritedCounts l r M =
      selectedContextEighteenReverseSiteInheritedCounts l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- All SEVEN independently typed new raw congruence generators
preserve the site list. Raw reverse requires BOTH compatibility of
the already certified genuine inherited-leaf count (v5.71) AND
the induction hypothesis for all deeper reversal sites. -/
theorem selectedRawCongruent_preservesReverseSiteInheritedCounts
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenReverseSiteInheritedCounts l r M =
      selectedContextEighteenReverseSiteInheritedCounts l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesReverseSiteInheritedCounts l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      exact congrArg₂ List.cons
        (selectedRawCongruent_preservesInheritedLeafCount l r A) ih
  | rawChainRight A X ih =>
      exact congrArg
        (fun s : List Nat =>
          s ++ selectedContextEighteenReverseSiteInheritedCounts l r X) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun s : List Nat =>
          selectedContextEighteenReverseSiteInheritedCounts l r X ++ s) ih

/-- Independent descent onto the ACTUAL new seven-generator quotient. -/
def selectedRawCongruentReverseSiteInheritedCountsOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → List Nat :=
  Quotient.lift (selectedContextEighteenReverseSiteInheritedCounts l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesReverseSiteInheritedCounts l r A)

theorem selectedRawCongruentReverseSiteInheritedCounts_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentReverseSiteInheritedCountsOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenReverseSiteInheritedCounts l r M := rfl

/-- Separate descent of the same original raw18D observation to
the INDEPENDENT original five-generator selected19 quotient. -/
def selectedNineteenReverseSiteInheritedCountsOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → List Nat :=
  Quotient.lift (selectedContextEighteenReverseSiteInheritedCounts l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesReverseSiteInheritedCounts l r A)

theorem selectedReverseSiteInheritedCounts_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentReverseSiteInheritedCountsOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenReverseSiteInheritedCountsOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Actual original same-fiber endomorphism raw18D proofs.
Each source leaf is a genuine strict 17D identity or an actual
inherited old18D Type-valued strict identity. -/
def selectedReverseSiteWitnessLeft
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain
    (selectedProvenanceStrictSpine l r N)
    (selectedProvenanceInheritedSpine l r N)

def selectedReverseSiteWitnessRight
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain
    (selectedProvenanceInheritedSpine l r N)
    (selectedProvenanceStrictSpine l r N)

theorem selectedReverseSite_leftValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedReverseSiteWitnessLeft l r N) = [0, 1] := rfl

theorem selectedReverseSite_rightValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedReverseSiteWitnessRight l r N) = [1, 0] := rfl

theorem selectedReverseSite_valuesDistinct :
    ([0, 1] : List Nat) ≠ [1, 0] := by
  decide

theorem selectedReverseSite_witnessSitesDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedReverseSiteWitnessLeft l r N) ≠
      selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedReverseSiteWitnessRight l r N) := by
  rw [selectedReverseSite_leftValue l r N,
    selectedReverseSite_rightValue l r N]
  exact selectedReverseSite_valuesDistinct

/-- SAME complete previous v5.73 observation: nine old observables,
complete ancestor Nat->Nat tower, complete consecutive-reverse
Nat->Nat tower, ordered raw run-list, unit-reduced nonassociative raw
bracket, inherited-leaf count, ordered old18D root tags.
No finite sampling replaces either complete infinite tower. -/
theorem selectedReverseSite_witnessRootObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentDoubleBracketCountRootObservation l r N N
        (selectedRawCongruentClass l r
          (selectedReverseSiteWitnessLeft l r N)) =
      selectedRawCongruentDoubleBracketCountRootObservation l r N N
        (selectedRawCongruentClass l r
          (selectedReverseSiteWitnessRight l r N)) := rfl

/-- Even v5.73's COMPLETE ordered original old18D INNER
NONASSOCIATIVE bracket list coincides: both are [oldStrict]. -/
theorem selectedReverseSite_witnessInnerObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentInheritedInnerListOnQuotient l r N N
        (selectedRawCongruentClass l r
          (selectedReverseSiteWitnessLeft l r N)) =
      selectedRawCongruentInheritedInnerListOnQuotient l r N N
        (selectedRawCongruentClass l r
          (selectedReverseSiteWitnessRight l r N)) := rfl

/-- Actual v5.73 complete quotient observer augmented by the
independently descended old18D INNER source bracket list. -/
abbrev SelectedDoubleBracketCountRootInnerValue :=
  SelectedDoubleBracketCountRootValue ×
    List SelectedInheritedOldInnerBracket

def selectedRawCongruentDoubleBracketCountRootInnerObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedDoubleBracketCountRootInnerValue :=
  fun q => (selectedRawCongruentDoubleBracketCountRootObservation l r J N q,
    selectedRawCongruentInheritedInnerListOnQuotient l r J N q)

theorem selectedReverseSite_witnessFullObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentDoubleBracketCountRootInnerObservation l r N N
        (selectedRawCongruentClass l r
          (selectedReverseSiteWitnessLeft l r N)) =
      selectedRawCongruentDoubleBracketCountRootInnerObservation l r N N
        (selectedRawCongruentClass l r
          (selectedReverseSiteWitnessRight l r N)) := by
  exact Prod.ext
    (selectedReverseSite_witnessRootObservedEq l r N)
    (selectedReverseSite_witnessInnerObservedEq l r N)

/-- The true seven-generator new quotient classes remain DISTINCT.
The proof applies the actual independently descended new invariant
to a putative class equality, not raw syntax inequality alone. -/
theorem selectedReverseSite_witnessClassDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentClass l r
        (selectedReverseSiteWitnessLeft l r N) ≠
      selectedRawCongruentClass l r
        (selectedReverseSiteWitnessRight l r N) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentReverseSiteInheritedCountsOnQuotient l r N N) h
  change selectedContextEighteenReverseSiteInheritedCounts l r
      (selectedReverseSiteWitnessLeft l r N) =
    selectedContextEighteenReverseSiteInheritedCounts l r
      (selectedReverseSiteWitnessRight l r N) at hc
  exact (selectedReverseSite_witnessSitesDistinct l r N) hc

/-- There is no actual Type-valued seven-generator comparison
of the two real raw18D source witnesses. -/
theorem selectedReverseSite_witnessNoComparison
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedReverseSiteWitnessLeft l r N)
      (selectedReverseSiteWitnessRight l r N)) := by
  rintro ⟨A⟩
  exact (selectedReverseSite_witnessClassDistinct l r N)
    (Quotient.sound ⟨A⟩)

/-- Genuine source M:J->N is an EXPLICIT input, not manufactured
for an arbitrary empty heterogeneous dependent fiber. -/
def selectedReverseSiteFiberLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedReverseSiteWitnessLeft l r N)

def selectedReverseSiteFiberRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedReverseSiteWitnessRight l r N)

/-- The two complete original signatures remain identical under a
genuinely supplied same-fiber left prefix. -/
theorem selectedReverseSiteFiber_fullObservedEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentDoubleBracketCountRootInnerObservation l r J N
        (selectedRawCongruentClass l r
          (selectedReverseSiteFiberLeft l r M)) =
      selectedRawCongruentDoubleBracketCountRootInnerObservation l r J N
        (selectedRawCongruentClass l r
          (selectedReverseSiteFiberRight l r M)) := rfl

/-- The NEW reverse-site list differs even after prefixing
an arbitrary actual raw18D source. Cancel the SAME Nat-list prefix. -/
theorem selectedReverseSiteFiber_sitesDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedReverseSiteFiberLeft l r M) ≠
      selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedReverseSiteFiberRight l r M) := by
  intro h
  change selectedContextEighteenReverseSiteInheritedCounts l r M ++
      selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedReverseSiteWitnessLeft l r N) =
    selectedContextEighteenReverseSiteInheritedCounts l r M ++
      selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedReverseSiteWitnessRight l r N) at h
  have hc := selectedOrderedRunList_prefixCancel
    (selectedContextEighteenReverseSiteInheritedCounts l r M)
    (selectedContextEighteenReverseSiteInheritedCounts l r
      (selectedReverseSiteWitnessLeft l r N))
    (selectedContextEighteenReverseSiteInheritedCounts l r
      (selectedReverseSiteWitnessRight l r N)) h
  exact (selectedReverseSite_witnessSitesDistinct l r N) hc

theorem selectedReverseSiteFiber_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r
        (selectedReverseSiteFiberLeft l r M) ≠
      selectedRawCongruentClass l r
        (selectedReverseSiteFiberRight l r M) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentReverseSiteInheritedCountsOnQuotient l r J N) h
  change selectedContextEighteenReverseSiteInheritedCounts l r
      (selectedReverseSiteFiberLeft l r M) =
    selectedContextEighteenReverseSiteInheritedCounts l r
      (selectedReverseSiteFiberRight l r M) at hc
  exact (selectedReverseSiteFiber_sitesDistinct l r M) hc

theorem selectedDoubleBracketCountRootInner_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedRawCongruentDoubleBracketCountRootInnerObservation l r J N) := by
  intro hinj
  exact (selectedReverseSiteFiber_classDistinct l r M)
    (hinj (selectedReverseSiteFiber_fullObservedEq l r M))

theorem selectedDoubleBracketCountRootInner_noSiteDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode :
        SelectedDoubleBracketCountRootInnerValue → List Nat,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode
            (selectedRawCongruentDoubleBracketCountRootInnerObservation
              l r J N q) =
          selectedRawCongruentReverseSiteInheritedCountsOnQuotient
            l r J N q := by
  rintro ⟨decode, h⟩
  have hc :
      selectedRawCongruentReverseSiteInheritedCountsOnQuotient l r J N
          (selectedRawCongruentClass l r
            (selectedReverseSiteFiberLeft l r M)) =
        selectedRawCongruentReverseSiteInheritedCountsOnQuotient l r J N
          (selectedRawCongruentClass l r
            (selectedReverseSiteFiberRight l r M)) := by
    calc
      _ = decode
          (selectedRawCongruentDoubleBracketCountRootInnerObservation
            l r J N (selectedRawCongruentClass l r
              (selectedReverseSiteFiberLeft l r M))) := (h _).symm
      _ = decode
          (selectedRawCongruentDoubleBracketCountRootInnerObservation
            l r J N (selectedRawCongruentClass l r
              (selectedReverseSiteFiberRight l r M))) :=
        congrArg decode (selectedReverseSiteFiber_fullObservedEq l r M)
      _ = _ := h _
  change selectedContextEighteenReverseSiteInheritedCounts l r
      (selectedReverseSiteFiberLeft l r M) =
    selectedContextEighteenReverseSiteInheritedCounts l r
      (selectedReverseSiteFiberRight l r M) at hc
  exact (selectedReverseSiteFiber_sitesDistinct l r M) hc

theorem selectedDoubleBracketCountRootInner_noClassDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode :
        SelectedDoubleBracketCountRootInnerValue →
          Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode
            (selectedRawCongruentDoubleBracketCountRootInnerObservation
              l r J N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedDoubleBracketCountRootInner_notInjective l r M
  intro a b hab
  calc
    a = decode
        (selectedRawCongruentDoubleBracketCountRootInnerObservation
          l r J N a) := (h a).symm
    _ = decode
        (selectedRawCongruentDoubleBracketCountRootInnerObservation
          l r J N b) := congrArg decode hab
    _ = b := h b

theorem selectedDoubleBracketCountRootInner_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentDoubleBracketCountRootInnerObservation l r J J) :=
  selectedDoubleBracketCountRootInner_notInjective l r (.strict J)

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenReverseSiteInheritedCounts
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesReverseSiteInheritedCounts
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesReverseSiteInheritedCounts
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseSiteInheritedCountsOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseSiteInheritedCounts_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenReverseSiteInheritedCountsOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedReverseSiteInheritedCounts_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedReverseSiteWitnessLeft
#print axioms PentagonAdjoinedSixCell.selectedReverseSiteWitnessRight
#print axioms PentagonAdjoinedSixCell.selectedReverseSite_leftValue
#print axioms PentagonAdjoinedSixCell.selectedReverseSite_rightValue
#print axioms PentagonAdjoinedSixCell.selectedReverseSite_valuesDistinct
#print axioms PentagonAdjoinedSixCell.selectedReverseSite_witnessSitesDistinct
#print axioms PentagonAdjoinedSixCell.selectedReverseSite_witnessRootObservedEq
#print axioms PentagonAdjoinedSixCell.selectedReverseSite_witnessInnerObservedEq
#print axioms PentagonAdjoinedSixCell.SelectedDoubleBracketCountRootInnerValue
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentDoubleBracketCountRootInnerObservation
#print axioms PentagonAdjoinedSixCell.selectedReverseSite_witnessFullObservedEq
#print axioms PentagonAdjoinedSixCell.selectedReverseSite_witnessClassDistinct
#print axioms PentagonAdjoinedSixCell.selectedReverseSite_witnessNoComparison
#print axioms PentagonAdjoinedSixCell.selectedReverseSiteFiberLeft
#print axioms PentagonAdjoinedSixCell.selectedReverseSiteFiberRight
#print axioms PentagonAdjoinedSixCell.selectedReverseSiteFiber_fullObservedEq
#print axioms PentagonAdjoinedSixCell.selectedReverseSiteFiber_sitesDistinct
#print axioms PentagonAdjoinedSixCell.selectedReverseSiteFiber_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedDoubleBracketCountRootInner_notInjective
#print axioms PentagonAdjoinedSixCell.selectedDoubleBracketCountRootInner_noSiteDecoder
#print axioms PentagonAdjoinedSixCell.selectedDoubleBracketCountRootInner_noClassDecoder
#print axioms PentagonAdjoinedSixCell.selectedDoubleBracketCountRootInner_endomorphismNotInjective

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
