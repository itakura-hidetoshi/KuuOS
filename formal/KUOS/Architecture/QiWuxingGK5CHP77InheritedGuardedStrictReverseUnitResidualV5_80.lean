import KUOS.Architecture.QiWuxingGK5CHP77StrictBranchChainSideResidualV5_79

/-!
Qi v5.80 — local noninjectivity even after the COMPLETE v5.79
seven-generator quotient observation, including every strict-only
maximal nontrivial branch's free shape, raw reversal-ancestor depth
and complete raw chain left/right address.

The original old selected19 unitPrepend/unitAppend compare ONLY a
raw strict identity directly adjoining an ACTUAL inherited old18D
proof. They do not declare a general unit law for arbitrary RAW
reverse terms. A coarse unit-reduced bracket cannot distinguish
a raw strict adjacent to raw reverse on the left versus on the right.

For each ACTUAL original 17D endpoint N, let S = strict N and use
the genuine dependent Type18D SAME-ENDPOINT proofs:

  A = chain (reverse S) S
  B = chain S (reverse S).

Both have the same complete v5.79 quotient observation, not merely
sampled Nat towers. Both have NO maximal nontrivial strict-only
chain branches, so the v5.77/v5.78/v5.79 refinements agree.

Introduce a separately defined inherited-guarded raw tree:
  inherited / strict / reversed / joined
which eliminates ONLY joined(strict,inherited) and
joined(inherited,strict); all other raw joins retain structure.
Preservation is proved for EVERY FIVE original typed19 generators
and EVERY SEVEN new raw congruence generators. Genuine separate
Quotient.lift constructions to both actual quotients and factorization
through the old-to-new projection are implemented.

The actual new quotient classes of A and B are DISTINCT, there is
no selectedRawCongruentNineteen Type-valued comparison, the complete
v5.79 quotient observation is locally noninjective on each GIVEN
N -> N fiber, and no guarded-tree/class decoder can exist.

This is an auxiliary observation, not an equality of dependent
source proofs or a global classification of the quotient. No
arbitrary J -> N inhabitance, all-WORLD descent, 20D gluing or
authority is claimed. Original Type18D, independent old/new
Type19D comparisons, root107, Lean/mathlib pin, and protected
validation-only PR #1558 are unchanged.
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

/-- A free nonassociative raw observation that retains a single strict
unit when it lies next to a reversed raw term, while abstracting
every ACTUAL inherited old18D leaf as one source marker. -/
inductive SelectedInheritedGuardedRawTree : Type where
  | inherited : SelectedInheritedGuardedRawTree
  | strict : SelectedInheritedGuardedRawTree
  | reversed : SelectedInheritedGuardedRawTree →
      SelectedInheritedGuardedRawTree
  | joined : SelectedInheritedGuardedRawTree →
      SelectedInheritedGuardedRawTree →
      SelectedInheritedGuardedRawTree
  deriving DecidableEq, Repr

/-- The ONLY two unit cancellations are at a direct inherited leaf.
We do not add a unit law to arbitrary reversed raw terms, and we
do not impose any raw chain associativity. -/
def selectedInheritedGuardedRawJoin :
    SelectedInheritedGuardedRawTree →
    SelectedInheritedGuardedRawTree →
    SelectedInheritedGuardedRawTree
  | .strict, .inherited => .inherited
  | .inherited, .strict => .inherited
  | A, B => .joined A B

theorem selectedInheritedGuardedRaw_unitPrepend :
    selectedInheritedGuardedRawJoin .strict .inherited =
      SelectedInheritedGuardedRawTree.inherited := rfl

theorem selectedInheritedGuardedRaw_unitAppend :
    selectedInheritedGuardedRawJoin .inherited .strict =
      SelectedInheritedGuardedRawTree.inherited := rfl

/-- In particular a raw strict to the right of a reversed raw strict
cannot be erased by the direct inherited-source unit rule. -/
theorem selectedInheritedGuardedRaw_noGeneralUnit :
    selectedInheritedGuardedRawJoin (.reversed .strict) .strict ≠
      SelectedInheritedGuardedRawTree.reversed .strict := by
  decide

/-- Read the REAL original dependent contextual18D Type value.
Whiskering retains the raw internal observer but does not invent a
unit equation outside the exact old selected19 comparison. -/
def selectedContextEighteenInheritedGuardedRaw (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    SelectedInheritedGuardedRawTree :=
  match M with
  | .inherited _ => .inherited
  | .whiskerLeft _ _ _ A =>
      selectedContextEighteenInheritedGuardedRaw l r A
  | .whiskerRight _ _ A _ =>
      selectedContextEighteenInheritedGuardedRaw l r A
  | .strict _ => .strict
  | .reverse A =>
      .reversed (selectedContextEighteenInheritedGuardedRaw l r A)
  | .chain A B =>
      selectedInheritedGuardedRawJoin
        (selectedContextEighteenInheritedGuardedRaw l r A)
        (selectedContextEighteenInheritedGuardedRaw l r B)

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- ALL FIVE genuinely original selected19 typed comparison
constructors preserve the inherited-guarded raw tree. In
unitPrepend/Append, the left and right strict nodes are truly
directly adjacent to an inherited old18D source leaf. -/
theorem selectedLocalNineteen_preservesInheritedGuardedRaw
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenInheritedGuardedRaw l r M =
      selectedContextEighteenInheritedGuardedRaw l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- ALL SEVEN genuinely new typed raw-congruence constructors
preserve the auxiliary raw tree. In particular congruence under
raw reverse and under both sides of raw chain is explicit. -/
theorem selectedRawCongruent_preservesInheritedGuardedRaw
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenInheritedGuardedRaw l r M =
      selectedContextEighteenInheritedGuardedRaw l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesInheritedGuardedRaw l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      exact congrArg SelectedInheritedGuardedRawTree.reversed ih
  | rawChainRight A X ih =>
      exact congrArg
        (fun s : SelectedInheritedGuardedRawTree =>
          selectedInheritedGuardedRawJoin s
            (selectedContextEighteenInheritedGuardedRaw l r X)) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun s : SelectedInheritedGuardedRawTree =>
          selectedInheritedGuardedRawJoin
            (selectedContextEighteenInheritedGuardedRaw l r X) s) ih

/-- Independent ACTUAL seven-generator quotient descent using true
Type-valued comparison and its setoid. -/
def selectedRawCongruentInheritedGuardedRawOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedInheritedGuardedRawTree :=
  Quotient.lift (selectedContextEighteenInheritedGuardedRaw l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesInheritedGuardedRaw l r A)

theorem selectedRawCongruentInheritedGuardedRaw_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentInheritedGuardedRawOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenInheritedGuardedRaw l r M := rfl

/-- Independently descend to the REAL old five-generator quotient,
not a proxy quotient or a silently unified comparison Type. -/
def selectedNineteenInheritedGuardedRawOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) →
      SelectedInheritedGuardedRawTree :=
  Quotient.lift (selectedContextEighteenInheritedGuardedRaw l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesInheritedGuardedRaw l r A)

/-- The old-to-new quotient projection is compatible with the two
independent descents; old/new 19D Types remain separate. -/
theorem selectedInheritedGuardedRaw_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentInheritedGuardedRawOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenInheritedGuardedRawOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Actual original dependent 18D proof values in an exact N -> N
fiber; both have ONE reversed strict and ONE other bare strict,
but the bare strict occupies a different side of the raw chain. -/
def selectedGuardedUnitWitnessLeft
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain (.reverse (.strict N)) (.strict N)

def selectedGuardedUnitWitnessRight
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain (.strict N) (.reverse (.strict N))

def selectedGuardedUnitLeftValue : SelectedInheritedGuardedRawTree :=
  .joined (.reversed .strict) .strict

def selectedGuardedUnitRightValue : SelectedInheritedGuardedRawTree :=
  .joined .strict (.reversed .strict)

theorem selectedGuardedUnit_leftValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedGuardedRaw l r
        (selectedGuardedUnitWitnessLeft l r N) =
      selectedGuardedUnitLeftValue := rfl

theorem selectedGuardedUnit_rightValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedGuardedRaw l r
        (selectedGuardedUnitWitnessRight l r N) =
      selectedGuardedUnitRightValue := rfl

theorem selectedGuardedUnit_valuesDistinct :
    selectedGuardedUnitLeftValue ≠ selectedGuardedUnitRightValue := by
  decide

theorem selectedGuardedUnit_witnessGuardedDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedGuardedRaw l r
        (selectedGuardedUnitWitnessLeft l r N) ≠
      selectedContextEighteenInheritedGuardedRaw l r
        (selectedGuardedUnitWitnessRight l r N) := by
  rw [selectedGuardedUnit_leftValue l r N,
    selectedGuardedUnit_rightValue l r N]
  exact selectedGuardedUnit_valuesDistinct

/-- COMPLETE ancestor tower: every natural degree agrees, with
no finite truncation or hidden assumption about source data. -/
theorem selectedGuardedUnit_witnessAncestorTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (degree : Nat) :
    selectedAncestorTowerCount l r degree
        (selectedGuardedUnitWitnessLeft l r N) =
      selectedAncestorTowerCount l r degree
        (selectedGuardedUnitWitnessRight l r N) := by
  cases degree with
  | zero => rfl
  | succ degree =>
      cases degree with
      | zero => rfl
      | succ degree => rfl

/-- COMPLETE direct consecutive reverse-run Nat-indexed tower. -/
theorem selectedGuardedUnit_witnessRunTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (degree : Nat) :
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedGuardedUnitWitnessLeft l r N) =
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedGuardedUnitWitnessRight l r N) := by
  cases degree with
  | zero => rfl
  | succ degree => rfl

/-- Equality of the actual v5.73 complete quotient observation.
Both infinite function-valued towers are compared using funext,
and the full inherited old18D root and inner provenance is kept. -/
theorem selectedGuardedUnit_witnessRootInnerObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentDoubleBracketCountRootInnerObservation l r N N
        (selectedRawCongruentClass l r
          (selectedGuardedUnitWitnessLeft l r N)) =
      selectedRawCongruentDoubleBracketCountRootInnerObservation l r N N
        (selectedRawCongruentClass l r
          (selectedGuardedUnitWitnessRight l r N)) := by
  have hbase :
      selectedRawCongruentFullDoubleOrderedBracketObservation l r N N
          (selectedRawCongruentClass l r
            (selectedGuardedUnitWitnessLeft l r N)) =
        selectedRawCongruentFullDoubleOrderedBracketObservation l r N N
          (selectedRawCongruentClass l r
            (selectedGuardedUnitWitnessRight l r N)) := by
    apply Prod.ext
    · apply Prod.ext
      · apply Prod.ext
        · apply Prod.ext
          · rfl
          · funext degree
            exact selectedGuardedUnit_witnessAncestorTowerEq l r N degree
        · funext degree
          exact selectedGuardedUnit_witnessRunTowerEq l r N degree
      · rfl
    · rfl
  apply Prod.ext
  · apply Prod.ext
    · apply Prod.ext
      · exact hbase
      · rfl
    · rfl
  · rfl

theorem selectedGuardedUnit_leftSites
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedGuardedUnitWitnessLeft l r N) = [0] := rfl

theorem selectedGuardedUnit_rightSites
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseSiteInheritedCounts l r
        (selectedGuardedUnitWitnessRight l r N) = [0] := rfl

theorem selectedGuardedUnit_leftWord
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseInheritedWord l r
        (selectedGuardedUnitWitnessLeft l r N) =
      [.rawReverse] := rfl

theorem selectedGuardedUnit_rightWord
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseInheritedWord l r
        (selectedGuardedUnitWitnessRight l r N) =
      [.rawReverse] := rfl

theorem selectedGuardedUnit_leftSensitive
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedSensitiveBracket l r
        (selectedGuardedUnitWitnessLeft l r N) =
      .reversed .unit := rfl

theorem selectedGuardedUnit_rightSensitive
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenInheritedSensitiveBracket l r
        (selectedGuardedUnitWitnessRight l r N) =
      .reversed .unit := rfl

/-- Both witnesses have NO nontrivial maximal strict-only branch
because every raw chain has a raw reverse on one side. -/
def selectedGuardedUnitSharedV577Shape : SelectedStrictOnlyBranchSummary :=
  ⟨none, []⟩

theorem selectedGuardedUnit_leftOldShape
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictOnlySummary l r
        (selectedGuardedUnitWitnessLeft l r N) =
      selectedGuardedUnitSharedV577Shape := rfl

theorem selectedGuardedUnit_rightOldShape
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictOnlySummary l r
        (selectedGuardedUnitWitnessRight l r N) =
      selectedGuardedUnitSharedV577Shape := rfl

def selectedGuardedUnitSharedV578Depth :
    SelectedStrictBranchDepthSummary :=
  ⟨none, []⟩

theorem selectedGuardedUnit_leftOldDepth
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictBranchDepth l r
        (selectedGuardedUnitWitnessLeft l r N) =
      selectedGuardedUnitSharedV578Depth := rfl

theorem selectedGuardedUnit_rightOldDepth
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictBranchDepth l r
        (selectedGuardedUnitWitnessRight l r N) =
      selectedGuardedUnitSharedV578Depth := rfl

def selectedGuardedUnitSharedV579Path : SelectedStrictBranchPathSummary :=
  ⟨none, []⟩

theorem selectedGuardedUnit_leftOldPath
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictBranchPath l r
        (selectedGuardedUnitWitnessLeft l r N) =
      selectedGuardedUnitSharedV579Path := rfl

theorem selectedGuardedUnit_rightOldPath
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenStrictBranchPath l r
        (selectedGuardedUnitWitnessRight l r N) =
      selectedGuardedUnitSharedV579Path := rfl

/-- The complete actual v5.79 seven-generator quotient observer
combines the complete v5.78 observer with the separately descended
maximal-branch raw-chain left/right address summary. -/
abbrev SelectedFullV579QuotientObservationValue :=
  SelectedFullV578QuotientObservationValue ×
    SelectedStrictBranchPathSummary

def selectedRawCongruentFullV579QuotientObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedFullV579QuotientObservationValue :=
  fun q =>
    (selectedRawCongruentFullV578QuotientObservation l r J N q,
      selectedRawCongruentStrictBranchPathOnQuotient l r J N q)

/-- COMPLETE actual v5.76 quotient observer equality. -/
theorem selectedGuardedUnit_witnessV576ObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentFullV576QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedGuardedUnitWitnessLeft l r N)) =
      selectedRawCongruentFullV576QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedGuardedUnitWitnessRight l r N)) := by
  apply Prod.ext
  · apply Prod.ext
    · apply Prod.ext
      · exact selectedGuardedUnit_witnessRootInnerObservedEq l r N
      · rfl
    · rfl
  · rfl

/-- COMPLETE actual v5.77 observer, including nonassociative
maximal strict-only branch shapes. -/
theorem selectedGuardedUnit_witnessV577ObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentFullV577QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedGuardedUnitWitnessLeft l r N)) =
      selectedRawCongruentFullV577QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedGuardedUnitWitnessRight l r N)) := by
  apply Prod.ext
  · exact selectedGuardedUnit_witnessV576ObservedEq l r N
  · rfl

/-- COMPLETE actual v5.78 observer including every strict-branch
reversal-ancestor depth. -/
theorem selectedGuardedUnit_witnessV578ObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentFullV578QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedGuardedUnitWitnessLeft l r N)) =
      selectedRawCongruentFullV578QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedGuardedUnitWitnessRight l r N)) := by
  apply Prod.ext
  · exact selectedGuardedUnit_witnessV577ObservedEq l r N
  · rfl

/-- COMPLETE actual v5.79 observer, including every maximal strict
branch's raw chain left/right address, also agrees. -/
theorem selectedGuardedUnit_witnessV579ObservedEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentFullV579QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedGuardedUnitWitnessLeft l r N)) =
      selectedRawCongruentFullV579QuotientObservation l r N N
        (selectedRawCongruentClass l r
          (selectedGuardedUnitWitnessRight l r N)) := by
  apply Prod.ext
  · exact selectedGuardedUnit_witnessV578ObservedEq l r N
  · rfl

/-- Genuinely DIFFERENT new seven-generator quotient classes.
The proof uses separately descended inherited-guarded tree data,
not a syntactic inequality of raw source terms. -/
theorem selectedGuardedUnit_witnessClassDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentClass l r
        (selectedGuardedUnitWitnessLeft l r N) ≠
      selectedRawCongruentClass l r
        (selectedGuardedUnitWitnessRight l r N) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentInheritedGuardedRawOnQuotient l r N N) h
  change selectedContextEighteenInheritedGuardedRaw l r
      (selectedGuardedUnitWitnessLeft l r N) =
    selectedContextEighteenInheritedGuardedRaw l r
      (selectedGuardedUnitWitnessRight l r N) at hc
  exact (selectedGuardedUnit_witnessGuardedDistinct l r N) hc

/-- There is no true new selected19 seven-generator Type-valued
comparison between the two original same-fiber proofs. -/
theorem selectedGuardedUnit_witnessNoComparison
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedGuardedUnitWitnessLeft l r N)
      (selectedGuardedUnitWitnessRight l r N)) := by
  rintro ⟨A⟩
  exact (selectedGuardedUnit_witnessClassDistinct l r N)
    (Quotient.sound ⟨A⟩)

/-- The COMPLETE v5.79 actual new seven-generator quotient observer
is noninjective in each genuinely GIVEN N -> N fiber. -/
theorem selectedGuardedUnit_v579NotInjective
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentFullV579QuotientObservation l r N N) := by
  intro hinj
  exact (selectedGuardedUnit_witnessClassDistinct l r N)
    (hinj (selectedGuardedUnit_witnessV579ObservedEq l r N))

/-- No function can recover the new guarded-raw tree invariant from
the complete v5.79 quotient observer at a genuine N -> N fiber. -/
theorem selectedGuardedUnit_noGuardedDecoder
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ ∃ decode :
        SelectedFullV579QuotientObservationValue →
          SelectedInheritedGuardedRawTree,
      ∀ q : Quotient (selectedRawCongruentSetoid l r N N),
        decode (selectedRawCongruentFullV579QuotientObservation
          l r N N q) =
            selectedRawCongruentInheritedGuardedRawOnQuotient l r N N q := by
  rintro ⟨decode, h⟩
  have hc :
      selectedRawCongruentInheritedGuardedRawOnQuotient l r N N
          (selectedRawCongruentClass l r
            (selectedGuardedUnitWitnessLeft l r N)) =
        selectedRawCongruentInheritedGuardedRawOnQuotient l r N N
          (selectedRawCongruentClass l r
            (selectedGuardedUnitWitnessRight l r N)) := by
    calc
      _ = decode (selectedRawCongruentFullV579QuotientObservation
          l r N N (selectedRawCongruentClass l r
            (selectedGuardedUnitWitnessLeft l r N))) := (h _).symm
      _ = decode (selectedRawCongruentFullV579QuotientObservation
          l r N N (selectedRawCongruentClass l r
            (selectedGuardedUnitWitnessRight l r N))) :=
        congrArg decode (selectedGuardedUnit_witnessV579ObservedEq l r N)
      _ = _ := h _
  change selectedContextEighteenInheritedGuardedRaw l r
      (selectedGuardedUnitWitnessLeft l r N) =
    selectedContextEighteenInheritedGuardedRaw l r
      (selectedGuardedUnitWitnessRight l r N) at hc
  exact (selectedGuardedUnit_witnessGuardedDistinct l r N) hc

/-- No quotient-class inverse decoder for the COMPLETE v5.79
observer of the actual new seven-generator N -> N quotient. -/
theorem selectedGuardedUnit_noClassDecoder
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ ∃ decode :
        SelectedFullV579QuotientObservationValue →
          Quotient (selectedRawCongruentSetoid l r N N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r N N),
        decode
            (selectedRawCongruentFullV579QuotientObservation
              l r N N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedGuardedUnit_v579NotInjective l r N
  intro a b hab
  calc
    a = decode
        (selectedRawCongruentFullV579QuotientObservation
          l r N N a) := (h a).symm
    _ = decode
        (selectedRawCongruentFullV579QuotientObservation
          l r N N b) := congrArg decode hab
    _ = b := h b

end ExactFiber

#print axioms PentagonAdjoinedSixCell.SelectedInheritedGuardedRawTree
#print axioms PentagonAdjoinedSixCell.selectedInheritedGuardedRawJoin
#print axioms PentagonAdjoinedSixCell.selectedInheritedGuardedRaw_unitPrepend
#print axioms PentagonAdjoinedSixCell.selectedInheritedGuardedRaw_unitAppend
#print axioms PentagonAdjoinedSixCell.selectedInheritedGuardedRaw_noGeneralUnit
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenInheritedGuardedRaw
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesInheritedGuardedRaw
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesInheritedGuardedRaw
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentInheritedGuardedRawOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentInheritedGuardedRaw_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenInheritedGuardedRawOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedInheritedGuardedRaw_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnitWitnessLeft
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnitWitnessRight
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnitLeftValue
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnitRightValue
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_leftValue
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_rightValue
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_valuesDistinct
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_witnessGuardedDistinct
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_witnessAncestorTowerEq
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_witnessRunTowerEq
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_witnessRootInnerObservedEq
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_leftSites
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_rightSites
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_leftWord
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_rightWord
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_leftSensitive
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_rightSensitive
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnitSharedV577Shape
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_leftOldShape
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_rightOldShape
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnitSharedV578Depth
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_leftOldDepth
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_rightOldDepth
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnitSharedV579Path
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_leftOldPath
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_rightOldPath
#print axioms PentagonAdjoinedSixCell.SelectedFullV579QuotientObservationValue
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullV579QuotientObservation
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_witnessV576ObservedEq
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_witnessV577ObservedEq
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_witnessV578ObservedEq
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_witnessV579ObservedEq
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_witnessClassDistinct
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_witnessNoComparison
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_v579NotInjective
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_noGuardedDecoder
#print axioms PentagonAdjoinedSixCell.selectedGuardedUnit_noClassDecoder

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
