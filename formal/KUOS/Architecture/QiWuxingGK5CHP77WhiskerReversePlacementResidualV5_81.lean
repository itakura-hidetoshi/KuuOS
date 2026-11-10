import KUOS.Architecture.QiWuxingGK5CHP77InheritedGuardedStrictReverseUnitResidualV5_80

/-!
Qi v5.81 — actual dependent contextual18D whiskering/reversal PLACEMENT residual.

The original 18D external List Bool trace already records left and right
whiskering; the new claim is NOT that whiskering can be freely ignored.
Instead a supplied true SevenRewrite, pair of context frames, and a true
17D endpoint N form TWO genuine SAME-FIBER contextual18D proofs:

  left:
  A = whiskerLeft before F G (reverse (strict N))
  B = reverse (whiskerLeft before F G (strict N))

  right:
  A = whiskerRight F G (reverse (strict N)) after
  B = reverse (whiskerRight F G (strict N) after).

Each pair has the SAME actual external whiskering word and the SAME
complete v5.80 quotient observation, including both full Nat-indexed
towers, source provenance, inherited source inner brackets, strict-only
branch paths, and inherited-guarded raw tree. But whiskering is placed
on opposite sides of a raw reversal.

An independent free NONASSOCIATIVE observer of original 18D constructs
distinguishes left/right whisker placement and retains actual inherited
old18D *internal bracket syntax*. Its only unit reductions are those
allowed by the original selected19 comparison: direct strict adjacent
to a genuine inherited old18D source leaf. All FIVE original and all
SEVEN new comparison generators preserve this observer. It descends
independently to both real quotients and factors through the old-to-new
projection; forgetting whiskering and source brackets recovers the
v5.80 inherited-guarded observer.

The left/right concrete examples give genuine new-quotient inequality,
absence of typed selected19 comparisons and local noninjectivity of the
complete v5.80 observer ONLY when the required original context/frame/
SevenRewrite evidence is SUPPLIED. No arbitrary rewriting inhabitance,
total quotient classification, across-WORLD descent, 20D gluing or
semantic authority. Old18D/19D comparison Types remain unchanged,
public root107 untouched, pin unchanged, protected #1558 untouched.
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

/-- Independent free, NONASSOCIATIVE syntax. A source carries only
the observed inner-bracket of a real dependent old18D value, NOT an
equality of those values. Whiskering is a position-sensitive wrapper. -/
inductive SelectedWhiskerPlacementTree : Type where
  | source : SelectedInheritedOldInnerBracket → SelectedWhiskerPlacementTree
  | strict : SelectedWhiskerPlacementTree
  | left : SelectedWhiskerPlacementTree → SelectedWhiskerPlacementTree
  | right : SelectedWhiskerPlacementTree → SelectedWhiskerPlacementTree
  | reversed : SelectedWhiskerPlacementTree → SelectedWhiskerPlacementTree
  | joined : SelectedWhiskerPlacementTree →
      SelectedWhiskerPlacementTree → SelectedWhiskerPlacementTree
  deriving DecidableEq, Repr

/-- Do NOT erase a strict next to arbitrary raw reverse, whisker, or
composite. The original five-generator selected19 unit rules apply
ONLY when its immediate neighbor is inherited old18D evidence. -/
def selectedWhiskerPlacementJoin :
    SelectedWhiskerPlacementTree →
    SelectedWhiskerPlacementTree →
    SelectedWhiskerPlacementTree
  | .strict, .source s => .source s
  | .source s, .strict => .source s
  | A, B => .joined A B

theorem selectedWhiskerPlacement_unitPrepend
    (s : SelectedInheritedOldInnerBracket) :
    selectedWhiskerPlacementJoin .strict (.source s) = .source s := rfl

theorem selectedWhiskerPlacement_unitAppend
    (s : SelectedInheritedOldInnerBracket) :
    selectedWhiskerPlacementJoin (.source s) .strict = .source s := rfl

theorem selectedWhiskerPlacement_noRawWhiskerUnit :
    selectedWhiskerPlacementJoin .strict (.left .strict) ≠
      SelectedWhiskerPlacementTree.left .strict := by
  decide

/-- Structural observation on the ACTUAL original contextual18D
Type-valued proof. Internal inherited old18D shape is only observed;
its genuine Type value, endpoints and higher evidence are unchanged. -/
def selectedContextEighteenWhiskerPlacement (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    SelectedWhiskerPlacementTree :=
  match M with
  | .inherited A => .source (selectedLocalEighteenInnerBracket l r A)
  | .whiskerLeft _ _ _ A =>
      .left (selectedContextEighteenWhiskerPlacement l r A)
  | .whiskerRight _ _ A _ =>
      .right (selectedContextEighteenWhiskerPlacement l r A)
  | .strict _ => .strict
  | .reverse A =>
      .reversed (selectedContextEighteenWhiskerPlacement l r A)
  | .chain A B =>
      selectedWhiskerPlacementJoin
        (selectedContextEighteenWhiskerPlacement l r A)
        (selectedContextEighteenWhiskerPlacement l r B)

/-- Project the new observation to the established v5.80 observer.
Whisker wrappers and old source internal brackets are intentionally
forgotten; old inherited-guarded JOIN normalization remains in force. -/
def selectedWhiskerPlacementForget :
    SelectedWhiskerPlacementTree → SelectedInheritedGuardedRawTree
  | .source _ => .inherited
  | .strict => .strict
  | .left A => selectedWhiskerPlacementForget A
  | .right A => selectedWhiskerPlacementForget A
  | .reversed A => .reversed (selectedWhiskerPlacementForget A)
  | .joined A B =>
      selectedInheritedGuardedRawJoin
        (selectedWhiskerPlacementForget A)
        (selectedWhiskerPlacementForget B)

theorem selectedWhiskerPlacementForget_join
    (A B : SelectedWhiskerPlacementTree) :
    selectedWhiskerPlacementForget (selectedWhiskerPlacementJoin A B) =
      selectedInheritedGuardedRawJoin
        (selectedWhiskerPlacementForget A)
        (selectedWhiskerPlacementForget B) := by
  cases A <;> cases B <;> rfl

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Every one of the FIVE ORIGINAL typed selected19 generators. -/
theorem selectedLocalNineteen_preservesWhiskerPlacement
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenWhiskerPlacement l r M =
      selectedContextEighteenWhiskerPlacement l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- Every one of the SEVEN NEW typed raw-congruence generators. -/
theorem selectedRawCongruent_preservesWhiskerPlacement
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenWhiskerPlacement l r M =
      selectedContextEighteenWhiskerPlacement l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesWhiskerPlacement l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      exact congrArg SelectedWhiskerPlacementTree.reversed ih
  | rawChainRight A X ih =>
      exact congrArg
        (fun s : SelectedWhiskerPlacementTree =>
          selectedWhiskerPlacementJoin s
            (selectedContextEighteenWhiskerPlacement l r X)) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun s : SelectedWhiskerPlacementTree =>
          selectedWhiskerPlacementJoin
            (selectedContextEighteenWhiskerPlacement l r X) s) ih

/-- Real new seven-generator quotient descent, not a proxy. -/
def selectedRawCongruentWhiskerPlacementOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedWhiskerPlacementTree :=
  Quotient.lift (selectedContextEighteenWhiskerPlacement l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesWhiskerPlacement l r A)

theorem selectedRawCongruentWhiskerPlacement_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentWhiskerPlacementOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenWhiskerPlacement l r M := rfl

/-- Distinct original five-generator quotient descent. -/
def selectedNineteenWhiskerPlacementOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) →
      SelectedWhiskerPlacementTree :=
  Quotient.lift (selectedContextEighteenWhiskerPlacement l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesWhiskerPlacement l r A)

/-- Factoring through the genuine old-to-new projection does NOT
silently unify the two independent comparison Types. -/
theorem selectedWhiskerPlacement_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentWhiskerPlacementOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenWhiskerPlacementOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Complete structural projection of the new observable back to
the certified v5.80 inherited-guarded raw observation. -/
theorem selectedWhiskerPlacement_forgetRaw
    (M : SelectedContextualEighteen W l r J N) :
    selectedWhiskerPlacementForget
        (selectedContextEighteenWhiskerPlacement l r M) =
      selectedContextEighteenInheritedGuardedRaw l r M := by
  induction M with
  | inherited A => rfl
  | whiskerLeft before F G M ih => exact ih
  | whiskerRight F G M after ih => exact ih
  | strict J => rfl
  | reverse M ih =>
      exact congrArg SelectedInheritedGuardedRawTree.reversed ih
  | chain M L ih ih' =>
      change selectedWhiskerPlacementForget
          (selectedWhiskerPlacementJoin
            (selectedContextEighteenWhiskerPlacement l r M)
            (selectedContextEighteenWhiskerPlacement l r L)) =
        selectedInheritedGuardedRawJoin
          (selectedContextEighteenInheritedGuardedRaw l r M)
          (selectedContextEighteenInheritedGuardedRaw l r L)
      rw [selectedWhiskerPlacementForget_join, ih, ih']

/-- Actual new quotient factorization of the v5.80 raw observer. -/
theorem selectedWhiskerPlacement_forgetOnQuotient
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedRawCongruentSetoid l r J N)) :
    selectedWhiskerPlacementForget
        (selectedRawCongruentWhiskerPlacementOnQuotient l r J N q) =
      selectedRawCongruentInheritedGuardedRawOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => exact selectedWhiskerPlacement_forgetRaw l r M

end ExactFiber

/-- Actual COMPLETE v5.80 seven-generator quotient observation,
combining the full v5.79 observation and the new v5.80 tree. -/
abbrev SelectedFullV580QuotientObservationValue :=
  SelectedFullV579QuotientObservationValue ×
    SelectedInheritedGuardedRawTree

section CompleteFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}

/-- The complete prior observation, not a hand-picked finite subset. -/
def selectedRawCongruentFullV580QuotientObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedFullV580QuotientObservationValue :=
  fun q =>
    (selectedRawCongruentFullV579QuotientObservation l r J N q,
      selectedRawCongruentInheritedGuardedRawOnQuotient l r J N q)

end CompleteFiber

/-- Independent source and whisker placement cannot commute merely
because the coarse v5.80 tree erases the whisker wrapper. -/
theorem selectedWhiskerPlacement_leftReverseDistinct :
    SelectedWhiskerPlacementTree.left (.reversed .strict) ≠
      .reversed (.left .strict) := by
  decide

theorem selectedWhiskerPlacement_rightReverseDistinct :
    SelectedWhiskerPlacementTree.right (.reversed .strict) ≠
      .reversed (.right .strict) := by
  decide

section LeftWhiskerFiber

variable (l r : W)
variable {w z : W}
variable {b c d : PentagonAdjoinedSixCell W l r w z}
variable (before : SevenRewrite W l r b c)
variable (F G : ContextFrameEleven W l r c d)
variable {P Q : SelectedUnitalCompositionTwelve W l r
  (contextFramePack l r F) (contextFramePack l r G)}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}

/-- A supplied typed left-whiskering surrounds one raw reverse. -/
def selectedWhiskerLeftInside
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N) :=
  .whiskerLeft before F G (.reverse (.strict N))

/-- One raw reverse instead surrounds the supplied typed whiskering. -/
def selectedWhiskerLeftOutside
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N) :=
  .reverse (.whiskerLeft before F G (.strict N))

theorem selectedWhiskerLeft_insideValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenWhiskerPlacement l r
        (selectedWhiskerLeftInside l r before F G N) =
      SelectedWhiskerPlacementTree.left (.reversed .strict) := rfl

theorem selectedWhiskerLeft_outsideValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenWhiskerPlacement l r
        (selectedWhiskerLeftOutside l r before F G N) =
      SelectedWhiskerPlacementTree.reversed (.left .strict) := rfl

/-- Both original 18D terms have the same TRUE external seven-cell
whiskering trace, including its left direction (not an erased trace). -/
theorem selectedWhiskerLeft_sameExternalTrace
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenTrace l r (selectedWhiskerLeftInside l r before F G N) =
      selectedContextEighteenTrace l r (selectedWhiskerLeftOutside l r before F G N) := rfl

/-- Complete v5.80 observation, including FULL Nat-indexed towers,
old18D provenance, reverse-site order, strict-only branch path and
inherited-guarded raw tree, fails to detect placement. -/
theorem selectedWhiskerLeft_sameFullV580
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentFullV580QuotientObservation l r (.whiskerLeft before F G N) (.whiskerLeft before F G N)
        (selectedRawCongruentClass l r
        (selectedWhiskerLeftInside l r before F G N)) =
      selectedRawCongruentFullV580QuotientObservation l r (.whiskerLeft before F G N) (.whiskerLeft before F G N)
        (selectedRawCongruentClass l r
        (selectedWhiskerLeftOutside l r before F G N)) := by
  have hbase :
      selectedRawCongruentFullDoubleOrderedBracketObservation l r (.whiskerLeft before F G N) (.whiskerLeft before F G N)
          (selectedRawCongruentClass l r
        (selectedWhiskerLeftInside l r before F G N)) =
        selectedRawCongruentFullDoubleOrderedBracketObservation l r (.whiskerLeft before F G N) (.whiskerLeft before F G N)
          (selectedRawCongruentClass l r
        (selectedWhiskerLeftOutside l r before F G N)) := by
    apply Prod.ext
    · apply Prod.ext
      · apply Prod.ext
        · apply Prod.ext
          · rfl
          · funext degree
            cases degree with
            | zero => rfl
            | succ degree => rfl
        · funext degree
          cases degree with
          | zero => rfl
          | succ degree => rfl
      · rfl
    · rfl
  have hroot :
      selectedRawCongruentDoubleBracketCountRootInnerObservation l r (.whiskerLeft before F G N) (.whiskerLeft before F G N)
          (selectedRawCongruentClass l r
        (selectedWhiskerLeftInside l r before F G N)) =
        selectedRawCongruentDoubleBracketCountRootInnerObservation l r (.whiskerLeft before F G N) (.whiskerLeft before F G N)
          (selectedRawCongruentClass l r
        (selectedWhiskerLeftOutside l r before F G N)) := by
    apply Prod.ext
    · apply Prod.ext
      · apply Prod.ext
        · exact hbase
        · rfl
      · rfl
    · rfl
  have h576 :
      selectedRawCongruentFullV576QuotientObservation l r (.whiskerLeft before F G N) (.whiskerLeft before F G N)
          (selectedRawCongruentClass l r
        (selectedWhiskerLeftInside l r before F G N)) =
        selectedRawCongruentFullV576QuotientObservation l r (.whiskerLeft before F G N) (.whiskerLeft before F G N)
          (selectedRawCongruentClass l r
        (selectedWhiskerLeftOutside l r before F G N)) := by
    apply Prod.ext
    · apply Prod.ext
      · apply Prod.ext
        · exact hroot
        · rfl
      · rfl
    · rfl
  apply Prod.ext
  · apply Prod.ext
    · apply Prod.ext
      · apply Prod.ext
        · exact h576
        · rfl
      · rfl
    · rfl
  · rfl

/-- Certified only after Lean checks: two different actual source
proofs in the exact SAME genuinely supplied whiskered N -> N fiber. -/
theorem selectedWhiskerLeft_classDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    (selectedRawCongruentClass l r
        (selectedWhiskerLeftInside l r before F G N)) ≠ (selectedRawCongruentClass l r
        (selectedWhiskerLeftOutside l r before F G N)) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentWhiskerPlacementOnQuotient l r (.whiskerLeft before F G N) (.whiskerLeft before F G N)) h
  change selectedContextEighteenWhiskerPlacement l r
      (selectedWhiskerLeftInside l r before F G N) =
    selectedContextEighteenWhiskerPlacement l r
      (selectedWhiskerLeftOutside l r before F G N) at hc
  rw [selectedWhiskerLeft_insideValue l r before F G N,
    selectedWhiskerLeft_outsideValue l r before F G N] at hc
  exact selectedWhiskerPlacement_leftReverseDistinct hc

/-- No ACTUAL new seven-generator typed selected19 comparison. -/
theorem selectedWhiskerLeft_noComparison
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r
      (.whiskerLeft before F G N) (.whiskerLeft before F G N)
      (selectedWhiskerLeftInside l r before F G N)
      (selectedWhiskerLeftOutside l r before F G N)) := by
  rintro ⟨A⟩
  exact (selectedWhiskerLeft_classDistinct l r before F G N)
    (Quotient.sound ⟨A⟩)

/-- The COMPLETE v5.80 observer is noninjective in each genuinely
given typed left-whiskered N -> N fiber; no inhabitance is fabricated. -/
theorem selectedWhiskerLeft_v580NotInjective
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentFullV580QuotientObservation l r (.whiskerLeft before F G N) (.whiskerLeft before F G N)) := by
  intro hinj
  exact (selectedWhiskerLeft_classDistinct l r before F G N)
    (hinj (selectedWhiskerLeft_sameFullV580 l r before F G N))

/-- No decoder of new quotient classes from the FULL v5.80 observer. -/
theorem selectedWhiskerLeft_noClassDecoder
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ ∃ decode :
        SelectedFullV580QuotientObservationValue →
          Quotient (selectedRawCongruentSetoid l r (.whiskerLeft before F G N) (.whiskerLeft before F G N)),
        ∀ q : Quotient (selectedRawCongruentSetoid l r (.whiskerLeft before F G N) (.whiskerLeft before F G N)),
          decode (selectedRawCongruentFullV580QuotientObservation
            l r (.whiskerLeft before F G N) (.whiskerLeft before F G N) q) = q := by
  rintro ⟨decode, h⟩
  apply selectedWhiskerLeft_v580NotInjective l r before F G N
  intro a b hab
  calc
    a = decode
        (selectedRawCongruentFullV580QuotientObservation
          l r (.whiskerLeft before F G N) (.whiskerLeft before F G N) a) := (h a).symm
    _ = decode
        (selectedRawCongruentFullV580QuotientObservation
          l r (.whiskerLeft before F G N) (.whiskerLeft before F G N) b) := congrArg decode hab
    _ = b := h b

end LeftWhiskerFiber

section RightWhiskerFiber

variable (l r : W)
variable {w z : W}
variable {c d e : PentagonAdjoinedSixCell W l r w z}
variable (F G : ContextFrameEleven W l r c d)
variable (after : SevenRewrite W l r d e)
variable {P Q : SelectedUnitalCompositionTwelve W l r
  (contextFramePack l r F) (contextFramePack l r G)}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}

/-- A supplied typed right-whiskering surrounds one raw reverse. -/
def selectedWhiskerRightInside
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after) :=
  .whiskerRight F G (.reverse (.strict N)) after

/-- One raw reverse instead surrounds the supplied typed whiskering. -/
def selectedWhiskerRightOutside
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after) :=
  .reverse (.whiskerRight F G (.strict N) after)

theorem selectedWhiskerRight_insideValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenWhiskerPlacement l r
        (selectedWhiskerRightInside l r F G after N) =
      SelectedWhiskerPlacementTree.right (.reversed .strict) := rfl

theorem selectedWhiskerRight_outsideValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenWhiskerPlacement l r
        (selectedWhiskerRightOutside l r F G after N) =
      SelectedWhiskerPlacementTree.reversed (.right .strict) := rfl

/-- Both original 18D terms have the same TRUE external seven-cell
whiskering trace, including its right direction (not an erased trace). -/
theorem selectedWhiskerRight_sameExternalTrace
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenTrace l r (selectedWhiskerRightInside l r F G after N) =
      selectedContextEighteenTrace l r (selectedWhiskerRightOutside l r F G after N) := rfl

/-- Complete v5.80 observation, including FULL Nat-indexed towers,
old18D provenance, reverse-site order, strict-only branch path and
inherited-guarded raw tree, fails to detect placement. -/
theorem selectedWhiskerRight_sameFullV580
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentFullV580QuotientObservation l r (.whiskerRight F G N after) (.whiskerRight F G N after)
        (selectedRawCongruentClass l r
        (selectedWhiskerRightInside l r F G after N)) =
      selectedRawCongruentFullV580QuotientObservation l r (.whiskerRight F G N after) (.whiskerRight F G N after)
        (selectedRawCongruentClass l r
        (selectedWhiskerRightOutside l r F G after N)) := by
  have hbase :
      selectedRawCongruentFullDoubleOrderedBracketObservation l r (.whiskerRight F G N after) (.whiskerRight F G N after)
          (selectedRawCongruentClass l r
        (selectedWhiskerRightInside l r F G after N)) =
        selectedRawCongruentFullDoubleOrderedBracketObservation l r (.whiskerRight F G N after) (.whiskerRight F G N after)
          (selectedRawCongruentClass l r
        (selectedWhiskerRightOutside l r F G after N)) := by
    apply Prod.ext
    · apply Prod.ext
      · apply Prod.ext
        · apply Prod.ext
          · rfl
          · funext degree
            cases degree with
            | zero => rfl
            | succ degree => rfl
        · funext degree
          cases degree with
          | zero => rfl
          | succ degree => rfl
      · rfl
    · rfl
  have hroot :
      selectedRawCongruentDoubleBracketCountRootInnerObservation l r (.whiskerRight F G N after) (.whiskerRight F G N after)
          (selectedRawCongruentClass l r
        (selectedWhiskerRightInside l r F G after N)) =
        selectedRawCongruentDoubleBracketCountRootInnerObservation l r (.whiskerRight F G N after) (.whiskerRight F G N after)
          (selectedRawCongruentClass l r
        (selectedWhiskerRightOutside l r F G after N)) := by
    apply Prod.ext
    · apply Prod.ext
      · apply Prod.ext
        · exact hbase
        · rfl
      · rfl
    · rfl
  have h576 :
      selectedRawCongruentFullV576QuotientObservation l r (.whiskerRight F G N after) (.whiskerRight F G N after)
          (selectedRawCongruentClass l r
        (selectedWhiskerRightInside l r F G after N)) =
        selectedRawCongruentFullV576QuotientObservation l r (.whiskerRight F G N after) (.whiskerRight F G N after)
          (selectedRawCongruentClass l r
        (selectedWhiskerRightOutside l r F G after N)) := by
    apply Prod.ext
    · apply Prod.ext
      · apply Prod.ext
        · exact hroot
        · rfl
      · rfl
    · rfl
  apply Prod.ext
  · apply Prod.ext
    · apply Prod.ext
      · apply Prod.ext
        · exact h576
        · rfl
      · rfl
    · rfl
  · rfl

/-- Certified only after Lean checks: two different actual source
proofs in the exact SAME genuinely supplied whiskered N -> N fiber. -/
theorem selectedWhiskerRight_classDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    (selectedRawCongruentClass l r
        (selectedWhiskerRightInside l r F G after N)) ≠ (selectedRawCongruentClass l r
        (selectedWhiskerRightOutside l r F G after N)) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentWhiskerPlacementOnQuotient l r (.whiskerRight F G N after) (.whiskerRight F G N after)) h
  change selectedContextEighteenWhiskerPlacement l r
      (selectedWhiskerRightInside l r F G after N) =
    selectedContextEighteenWhiskerPlacement l r
      (selectedWhiskerRightOutside l r F G after N) at hc
  rw [selectedWhiskerRight_insideValue l r F G after N,
    selectedWhiskerRight_outsideValue l r F G after N] at hc
  exact selectedWhiskerPlacement_rightReverseDistinct hc

/-- No ACTUAL new seven-generator typed selected19 comparison. -/
theorem selectedWhiskerRight_noComparison
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)
      (selectedWhiskerRightInside l r F G after N)
      (selectedWhiskerRightOutside l r F G after N)) := by
  rintro ⟨A⟩
  exact (selectedWhiskerRight_classDistinct l r F G after N)
    (Quotient.sound ⟨A⟩)

/-- The COMPLETE v5.80 observer is noninjective in each genuinely
given typed right-whiskered N -> N fiber; no inhabitance is fabricated. -/
theorem selectedWhiskerRight_v580NotInjective
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentFullV580QuotientObservation l r (.whiskerRight F G N after) (.whiskerRight F G N after)) := by
  intro hinj
  exact (selectedWhiskerRight_classDistinct l r F G after N)
    (hinj (selectedWhiskerRight_sameFullV580 l r F G after N))

/-- No decoder of new quotient classes from the FULL v5.80 observer. -/
theorem selectedWhiskerRight_noClassDecoder
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ ∃ decode :
        SelectedFullV580QuotientObservationValue →
          Quotient (selectedRawCongruentSetoid l r (.whiskerRight F G N after) (.whiskerRight F G N after)),
        ∀ q : Quotient (selectedRawCongruentSetoid l r (.whiskerRight F G N after) (.whiskerRight F G N after)),
          decode (selectedRawCongruentFullV580QuotientObservation
            l r (.whiskerRight F G N after) (.whiskerRight F G N after) q) = q := by
  rintro ⟨decode, h⟩
  apply selectedWhiskerRight_v580NotInjective l r F G after N
  intro a b hab
  calc
    a = decode
        (selectedRawCongruentFullV580QuotientObservation
          l r (.whiskerRight F G N after) (.whiskerRight F G N after) a) := (h a).symm
    _ = decode
        (selectedRawCongruentFullV580QuotientObservation
          l r (.whiskerRight F G N after) (.whiskerRight F G N after) b) := congrArg decode hab
    _ = b := h b

end RightWhiskerFiber

#print axioms PentagonAdjoinedSixCell.SelectedWhiskerPlacementTree
#print axioms PentagonAdjoinedSixCell.selectedWhiskerPlacementJoin
#print axioms PentagonAdjoinedSixCell.selectedWhiskerPlacement_unitPrepend
#print axioms PentagonAdjoinedSixCell.selectedWhiskerPlacement_unitAppend
#print axioms PentagonAdjoinedSixCell.selectedWhiskerPlacement_noRawWhiskerUnit
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenWhiskerPlacement
#print axioms PentagonAdjoinedSixCell.selectedWhiskerPlacementForget
#print axioms PentagonAdjoinedSixCell.selectedWhiskerPlacementForget_join
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesWhiskerPlacement
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesWhiskerPlacement
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentWhiskerPlacementOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentWhiskerPlacement_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenWhiskerPlacementOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedWhiskerPlacement_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedWhiskerPlacement_forgetRaw
#print axioms PentagonAdjoinedSixCell.selectedWhiskerPlacement_forgetOnQuotient
#print axioms PentagonAdjoinedSixCell.SelectedFullV580QuotientObservationValue
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullV580QuotientObservation
#print axioms PentagonAdjoinedSixCell.selectedWhiskerPlacement_leftReverseDistinct
#print axioms PentagonAdjoinedSixCell.selectedWhiskerPlacement_rightReverseDistinct
#print axioms PentagonAdjoinedSixCell.selectedWhiskerLeftInside
#print axioms PentagonAdjoinedSixCell.selectedWhiskerLeftOutside
#print axioms PentagonAdjoinedSixCell.selectedWhiskerLeft_insideValue
#print axioms PentagonAdjoinedSixCell.selectedWhiskerLeft_outsideValue
#print axioms PentagonAdjoinedSixCell.selectedWhiskerLeft_sameExternalTrace
#print axioms PentagonAdjoinedSixCell.selectedWhiskerLeft_sameFullV580
#print axioms PentagonAdjoinedSixCell.selectedWhiskerLeft_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedWhiskerLeft_noComparison
#print axioms PentagonAdjoinedSixCell.selectedWhiskerLeft_v580NotInjective
#print axioms PentagonAdjoinedSixCell.selectedWhiskerLeft_noClassDecoder
#print axioms PentagonAdjoinedSixCell.selectedWhiskerRightInside
#print axioms PentagonAdjoinedSixCell.selectedWhiskerRightOutside
#print axioms PentagonAdjoinedSixCell.selectedWhiskerRight_insideValue
#print axioms PentagonAdjoinedSixCell.selectedWhiskerRight_outsideValue
#print axioms PentagonAdjoinedSixCell.selectedWhiskerRight_sameExternalTrace
#print axioms PentagonAdjoinedSixCell.selectedWhiskerRight_sameFullV580
#print axioms PentagonAdjoinedSixCell.selectedWhiskerRight_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedWhiskerRight_noComparison
#print axioms PentagonAdjoinedSixCell.selectedWhiskerRight_v580NotInjective
#print axioms PentagonAdjoinedSixCell.selectedWhiskerRight_noClassDecoder

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
