import KUOS.Architecture.QiWuxingGK5CHP77SeventeenQuotientTraceGateV5_34

/-!
Qi v5.35 — true original seventh-context closure of the selected
seventeenth comparison, constructive adjacent-order trace-swap
certificate, and exactly typed selected local eighteenth unit cell.

The v5.34 trace-RESPECTING LR/RL mixed higher gluing gate is proved
empty and remains empty. Here we replace this impossible trace
equality demand with a PROOF-RELEVANT finite adjacent swap:
  false :: true :: history  ==>  true :: false :: history.
The swap is a certificate about observations in a COMMON codomain,
NOT an equality between heterogeneously dependent 16D proof values,
NOT a newly postulated 17D exchange, and NOT a universal
trace-changing gluing of the original source proof types.

The full v5.33 original 12D/selected 13D/14D compatibility packet
is retained with the typed swap. The finite witness is
constructible from existing original seventh contexts and the actual
double-whisker lower certificates. The adjacent interchange keeps
the numbers of left and right context events, while necessarily
changing their order. Hence both a positive trace-change
certificate and the old negative trace-preserving gate theorem
hold under exactly the same contextual hypotheses.

An INDEPENDENT selected contextual 17D presentation faithfully
embeds all genuine v5.33 raw 17D proof values and transports
17D evidence through true matching original seventh-cell left and
right contexts. The ordered raw16D exterior trace is invariant
under all its constructors and therefore descends through its
own contextual 17D quotient. The raw 16D FIRST constructor tag,
by contrast, does NOT descend, witnessed by the actual old
17D unit critical pair (tags 3 versus 0).

Finally two exactly typed 17D unit-pasting critical pairs built from
the actual v5.33 selected local 17D units admit a newly selected
18D comparison. Their raw 17D proof terms remain unequal. No
unconditional 18D mixed exchange and no Gray/tetracategorical
coherence are asserted.

Append-only / tighten-only / overwrite-forbidden / same-root.
Original F55/P77/GK5CG, all original 6D–14D sources and the
prior v5.23–v5.34 selected proof Types remain UNCHANGED.
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

/-- The first SELECTED 17D context closure.  Old raw proof values
are stored as the inherited constructor, and the two context actions
require the ACTUAL original matching 7D boundary, not a fabricated
heterogeneous proof equality. -/
inductive SelectedContextualSeventeen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    {P Q : SelectedUnitalCompositionTwelve W l r F G} →
    {C D : SelectedMixedInterchangerThirteen W l r P Q} →
    {V X : SelectedMixedNaturalityFourteen W l r C D} →
    {T U : SelectedContextualFifteen W l r V X} →
    SelectedContextualSixteen W l r T U →
    SelectedContextualSixteen W l r T U → Type uSix where
  | inherited {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      (J : SelectedLocalSeventeen W l r H K) :
      SelectedContextualSeventeen W l r H K
  | whiskerLeft {w z : W}
      {b c d : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      (J : SelectedContextualSeventeen W l r H K) :
      SelectedContextualSeventeen W l r
        (.whiskerLeft before F G H)
        (.whiskerLeft before F G K)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      (J : SelectedContextualSeventeen W l r H K)
      (after : SevenRewrite W l r d e) :
      SelectedContextualSeventeen W l r
        (.whiskerRight F G H after)
        (.whiskerRight F G K after)
  | strict {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      (H : SelectedContextualSixteen W l r T U) :
      SelectedContextualSeventeen W l r H H
  | reverse {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      (J : SelectedContextualSeventeen W l r H K) :
      SelectedContextualSeventeen W l r K H
  | chain {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K M : SelectedContextualSixteen W l r T U}
      (J : SelectedContextualSeventeen W l r H K)
      (N : SelectedContextualSeventeen W l r K M) :
      SelectedContextualSeventeen W l r H M

/-- Retain every old v5.33 selected 17D proof as an unmodified
dependent Type value, not an arbitrary lifting principle. -/
def oldSeventeenToContextual (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedLocalSeventeen W l r H K) :
    SelectedContextualSeventeen W l r H K :=
  .inherited J

theorem oldSeventeenToContextual_injective (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U} :
    Function.Injective (fun J : SelectedLocalSeventeen W l r H K =>
      oldSeventeenToContextual l r J) := by
  intro J N h
  cases h
  rfl

theorem selectedContextualSeventeen_leftStable (l r : W) {w z : W}
    {b c d : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedContextualSeventeen W l r H K) :
    Nonempty (SelectedContextualSeventeen W l r
      (.whiskerLeft before F G H) (.whiskerLeft before F G K)) :=
  ⟨.whiskerLeft before F G J⟩

theorem selectedContextualSeventeen_rightStable (l r : W) {w z : W}
    {c d e : PentagonAdjoinedSixCell W l r w z}
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedContextualSeventeen W l r H K)
    (after : SevenRewrite W l r d e) :
    Nonempty (SelectedContextualSeventeen W l r
      (.whiskerRight F G H after) (.whiskerRight F G K after)) :=
  ⟨.whiskerRight F G J after⟩

/-- All six selected 17D context-closed proof constructors preserve
the PREVIOUS full ordered exterior trace of raw16D witnesses. -/
theorem selectedContextualSeventeen_preservesSixteenTrace (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedContextualSeventeen W l r H K) :
    selectedContextSixteenTrace l r H = selectedContextSixteenTrace l r K := by
  induction J with
  | inherited J => exact selectedSeventeen_preservesSixteenTrace l r J
  | whiskerLeft before F G J ih =>
      exact congrArg (List.cons false) ih
  | whiskerRight F G J after ih =>
      exact congrArg (List.cons true) ih
  | strict H => rfl
  | reverse J ih => exact ih.symm
  | chain J N ih ih' => exact ih.trans ih'

/-- A DISTINCT context-closed quotient of parallel SIXTEENTH raw
proof values by actual context-closed SEVENTEENTH evidence. -/
def selectedContextSeventeenSetoid (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T U : SelectedContextualFifteen W l r V X) :
    Setoid (SelectedContextualSixteen W l r T U) where
  r := fun H K => Nonempty (SelectedContextualSeventeen W l r H K)
  iseqv := by
    constructor
    · intro H
      exact ⟨.strict H⟩
    · intro H K h
      rcases h with ⟨J⟩
      exact ⟨.reverse J⟩
    · intro H K M h h'
      rcases h with ⟨J⟩
      rcases h' with ⟨N⟩
      exact ⟨.chain J N⟩

def selectedContextSeventeenClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U) :
    Quotient (selectedContextSeventeenSetoid l r T U) :=
  Quotient.mk _ H

theorem selectedContextSeventeenClass_eq_iff (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H K : SelectedContextualSixteen W l r T U) :
    selectedContextSeventeenClass l r H =
      selectedContextSeventeenClass l r K ↔
        Nonempty (SelectedContextualSeventeen W l r H K) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

def selectedContextSeventeenTraceOnQuotient (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T U : SelectedContextualFifteen W l r V X) :
    Quotient (selectedContextSeventeenSetoid l r T U) → List Bool :=
  Quotient.lift (selectedContextSixteenTrace l r) (by
    intro H K h
    rcases h with ⟨J⟩
    exact selectedContextualSeventeen_preservesSixteenTrace l r J)

theorem selectedContextSeventeenTrace_onClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U) :
    selectedContextSeventeenTraceOnQuotient l r T U
        (selectedContextSeventeenClass l r H) =
      selectedContextSixteenTrace l r H :=
  rfl

theorem selectedContextSeventeen_inheritedUnit_classEq (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedContextSeventeenClass l r
        (selectedSixteenUnitPrependLeft l r before F G C after) =
      selectedContextSeventeenClass l r
        (selectedSixteenUnitAppendLeft l r before F G C after) :=
  Quotient.sound ⟨.inherited (.unitLeft before F G C after)⟩

theorem selectedContextSeventeen_noFirstTagDescent (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    ¬ (∃ g : Quotient (selectedContextSeventeenSetoid l r
        (selectedFifteenUnitRoundtrip l r before F G C after)
        (SelectedContextualFifteen.strict
          (selectedMixedFourteenUnitPrepend l r before F G C after))) → Nat,
      ∀ (H : SelectedContextualSixteen W l r
        (selectedFifteenUnitRoundtrip l r before F G C after)
        (SelectedContextualFifteen.strict
          (selectedMixedFourteenUnitPrepend l r before F G C after))),
        g (selectedContextSeventeenClass l r H) =
          selectedContextSixteenFirstAtomTag l r H) := by
  rintro ⟨g, hg⟩
  have ht : selectedContextSixteenFirstAtomTag l r
        (selectedSixteenUnitPrependLeft l r before F G C after) =
      selectedContextSixteenFirstAtomTag l r
        (selectedSixteenUnitAppendLeft l r before F G C after) := by
    calc
      _ = g (selectedContextSeventeenClass l r
          (selectedSixteenUnitPrependLeft l r before F G C after)) :=
        (hg _).symm
      _ = g (selectedContextSeventeenClass l r
          (selectedSixteenUnitAppendLeft l r before F G C after)) :=
        congrArg g
          (selectedContextSeventeen_inheritedUnit_classEq l r before F G C after)
      _ = _ := hg _
  change (3 : Nat) = 0 at ht
  cases ht

/-- A proof-relevant SINGLE ADJACENT SWAP of the first two
OUTER original seventh-context events. Both lists are observations,
NOT raw 16D proof objects. Crucially no automatic 18D comparison
constructor is created between different dependent fibers. -/
inductive SelectedOuterAdjacentSwap :
    List Bool → List Bool → Type where
  | leftRightToRightLeft (tail : List Bool) :
      SelectedOuterAdjacentSwap
        (false :: true :: tail) (true :: false :: tail)
  | rightLeftToLeftRight (tail : List Bool) :
      SelectedOuterAdjacentSwap
        (true :: false :: tail) (false :: true :: tail)

/-- The genuinely typed v5.33 mixed SIXTEENTH transports admit
an EXPLICIT adjacent swap of their independently observed traces. -/
def selectedMixedOuterAdjacentSwap (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {I J : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r I J}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U)
    (right : SevenRewrite W l r c d) :
    SelectedOuterAdjacentSwap
      (selectedContextSixteenTrace l r
        (selectedSixteenLeftAfterRight l r left F G H right))
      (selectedContextSixteenTrace l r
        (selectedSixteenRightAfterLeft l r left F G H right)) := by
  change SelectedOuterAdjacentSwap
    (false :: true :: selectedContextSixteenTrace l r H)
    (true :: false :: selectedContextSixteenTrace l r H)
  exact .leftRightToRightLeft _

/-- The local permitted trace-change is NOT a trace equivalence:
both Boolean observations are provably different. -/
theorem selectedAdjacentSwap_changesTrace (tail : List Bool) :
    false :: true :: tail ≠ true :: false :: tail := by
  intro h
  cases h

/-- Unlike equality of ordered traces, the trace-level adjacent
swap preserves the NUMBER of left and right events. -/
theorem selectedAdjacentSwap_preservesCounts (tail : List Bool) :
    selectedFifteenTraceCounts (false :: true :: tail) =
      selectedFifteenTraceCounts (true :: false :: tail) := by
  simp [selectedFifteenTraceCounts]

/-- POSITIVE, constructive trace-changing mixed mediation DATA:
the actual original lower 12D/selected13D/14D packet is present,
and the two separately typed high-context observables are linked
by one explicit adjacent order swap, with equal event counts.
This is a compatibility certificate in an OBSERVATION space, not an
unproved high-dimensional original comparison cell. -/
structure SelectedMixedTraceChangingCertificate (l r : W)
    {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    {I J : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r I J}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U)
    (right : SevenRewrite W l r c d) : Type uSix where
  lower : SelectedMixedLowerHigherPacket l r left F G C right
  swap : SelectedOuterAdjacentSwap
    (selectedContextSixteenTrace l r
      (selectedSixteenLeftAfterRight l r left F G H right))
    (selectedContextSixteenTrace l r
      (selectedSixteenRightAfterLeft l r left F G H right))
  counts :
    selectedFifteenTraceCounts
        (selectedContextSixteenTrace l r
          (selectedSixteenLeftAfterRight l r left F G H right)) =
      selectedFifteenTraceCounts
        (selectedContextSixteenTrace l r
          (selectedSixteenRightAfterLeft l r left F G H right))

/-- Construct a real mixed trace CHANGE certificate using only the
previously proved original lower packet and the explicit swapped
finite observations. No new axiom or high-cell is assumed. -/
def selectedMixedTraceChangingCertificate (l r : W)
    {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    {I J : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r I J}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U)
    (right : SevenRewrite W l r c d) :
    SelectedMixedTraceChangingCertificate l r left F G C H right :=
  ⟨selectedMixedLowerHigherPacket l r left F G C right,
    selectedMixedOuterAdjacentSwap l r left F G H right,
    by
      change selectedFifteenTraceCounts
        (false :: true :: selectedContextSixteenTrace l r H) =
        selectedFifteenTraceCounts
          (true :: false :: selectedContextSixteenTrace l r H)
      exact selectedAdjacentSwap_preservesCounts _⟩

/-- The CONSTRUCTIVE adjacent-swap compatibility and the already
proved IMPOSSIBLE exact-trace compatibility coexist, without
false equivalence of the heterogeneous proof source types. -/
theorem selectedMixedTraceChange_possible_strictTraceImpossible (l r : W)
    {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    {I J : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r I J}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U)
    (right : SevenRewrite W l r c d) :
    Nonempty (SelectedMixedTraceChangingCertificate l r
      left F G C H right) ∧
    ¬ Nonempty (SelectedMixedTraceRespectingHigherGate l r
      left F G C H right) :=
  ⟨⟨selectedMixedTraceChangingCertificate l r left F G C H right⟩,
    selectedMixedTraceRespectingHigherGate_empty l r left F G C H right⟩

/-- Raw 17D witness syntax observer. The old 17D proof object is
retained by inherited and is not collapsed to equality. -/
def selectedContextSeventeenFirstAtomTag (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedContextualSeventeen W l r H K) : Nat :=
  match J with
  | .inherited _ => 0
  | .whiskerLeft _ _ _ _ => 1
  | .whiskerRight _ _ _ _ => 2
  | .strict _ => 3
  | .reverse _ => 4
  | .chain J _ => selectedContextSeventeenFirstAtomTag l r J

/-- The genuine old selected 17D UNIT comparison with an exact
17D identity BEFORE it. -/
def selectedSeventeenUnitPrependLeft (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    SelectedContextualSeventeen W l r
      (selectedSixteenUnitPrependLeft l r before F G C after)
      (selectedSixteenUnitAppendLeft l r before F G C after) :=
  .chain (.strict (selectedSixteenUnitPrependLeft l r before F G C after))
    (.inherited (.unitLeft before F G C after))

def selectedSeventeenUnitAppendLeft (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    SelectedContextualSeventeen W l r
      (selectedSixteenUnitPrependLeft l r before F G C after)
      (selectedSixteenUnitAppendLeft l r before F G C after) :=
  .chain (.inherited (.unitLeft before F G C after))
    (.strict (selectedSixteenUnitAppendLeft l r before F G C after))

def selectedSeventeenUnitPrependRight (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    SelectedContextualSeventeen W l r
      (selectedSixteenUnitPrependRight l r before F G C after)
      (selectedSixteenUnitAppendRight l r before F G C after) :=
  .chain (.strict (selectedSixteenUnitPrependRight l r before F G C after))
    (.inherited (.unitRight before F G C after))

def selectedSeventeenUnitAppendRight (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    SelectedContextualSeventeen W l r
      (selectedSixteenUnitPrependRight l r before F G C after)
      (selectedSixteenUnitAppendRight l r before F G C after) :=
  .chain (.inherited (.unitRight before F G C after))
    (.strict (selectedSixteenUnitAppendRight l r before F G C after))

theorem selectedSeventeenUnitLeft_rawDistinct (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedSeventeenUnitPrependLeft l r before F G C after ≠
      selectedSeventeenUnitAppendLeft l r before F G C after := by
  intro h
  have ht := congrArg (selectedContextSeventeenFirstAtomTag l r) h
  change (3 : Nat) = 0 at ht
  cases ht

theorem selectedSeventeenUnitRight_rawDistinct (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedSeventeenUnitPrependRight l r before F G C after ≠
      selectedSeventeenUnitAppendRight l r before F G C after := by
  intro h
  have ht := congrArg (selectedContextSeventeenFirstAtomTag l r) h
  change (3 : Nat) = 0 at ht
  cases ht

/-- Only two strictly matching true local 17D UNIT-pasting
critical pairs are newly selected at 18D. Never a generic mixed
exchange between differently indexed high-dimensional fibers. -/
inductive SelectedLocalEighteen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    {P Q : SelectedUnitalCompositionTwelve W l r F G} →
    {C D : SelectedMixedInterchangerThirteen W l r P Q} →
    {V X : SelectedMixedNaturalityFourteen W l r C D} →
    {T U : SelectedContextualFifteen W l r V X} →
    {H K : SelectedContextualSixteen W l r T U} →
    SelectedContextualSeventeen W l r H K →
    SelectedContextualSeventeen W l r H K → Type uSix where
  | strict {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      (J : SelectedContextualSeventeen W l r H K) :
      SelectedLocalEighteen W l r J J
  | unitLeft {w z : W}
      {b c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      (C : SelectedContextualThirteen W l r P Q)
      (after : SevenRewrite W l r d e) :
      SelectedLocalEighteen W l r
        (selectedSeventeenUnitPrependLeft l r before F G C after)
        (selectedSeventeenUnitAppendLeft l r before F G C after)
  | unitRight {w z : W}
      {b c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      (C : SelectedContextualThirteen W l r P Q)
      (after : SevenRewrite W l r d e) :
      SelectedLocalEighteen W l r
        (selectedSeventeenUnitPrependRight l r before F G C after)
        (selectedSeventeenUnitAppendRight l r before F G C after)
  | reverse {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      {J N : SelectedContextualSeventeen W l r H K}
      (M : SelectedLocalEighteen W l r J N) :
      SelectedLocalEighteen W l r N J
  | chain {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      {J N M : SelectedContextualSeventeen W l r H K}
      (A : SelectedLocalEighteen W l r J N)
      (B : SelectedLocalEighteen W l r N M) :
      SelectedLocalEighteen W l r J M

theorem selectedLocalEighteen_leftWitness (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    Nonempty (SelectedLocalEighteen W l r
      (selectedSeventeenUnitPrependLeft l r before F G C after)
      (selectedSeventeenUnitAppendLeft l r before F G C after)) ∧
    selectedSeventeenUnitPrependLeft l r before F G C after ≠
      selectedSeventeenUnitAppendLeft l r before F G C after :=
  ⟨⟨.unitLeft before F G C after⟩,
    selectedSeventeenUnitLeft_rawDistinct l r before F G C after⟩

theorem selectedLocalEighteen_rightWitness (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    Nonempty (SelectedLocalEighteen W l r
      (selectedSeventeenUnitPrependRight l r before F G C after)
      (selectedSeventeenUnitAppendRight l r before F G C after)) ∧
    selectedSeventeenUnitPrependRight l r before F G C after ≠
      selectedSeventeenUnitAppendRight l r before F G C after :=
  ⟨⟨.unitRight before F G C after⟩,
    selectedSeventeenUnitRight_rawDistinct l r before F G C after⟩

theorem selectedLocalEighteen_noRawEqualityInterpreter (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    ¬ (∀
      (J K : SelectedContextualSeventeen W l r
        (selectedSixteenUnitPrependLeft l r before F G C after)
        (selectedSixteenUnitAppendLeft l r before F G C after)),
      SelectedLocalEighteen W l r J K → J = K) := by
  intro interpret
  exact selectedSeventeenUnitLeft_rawDistinct l r before F G C after
    (interpret _ _ (.unitLeft before F G C after))

#print axioms PentagonAdjoinedSixCell.SelectedContextualSeventeen
#print axioms PentagonAdjoinedSixCell.oldSeventeenToContextual
#print axioms PentagonAdjoinedSixCell.oldSeventeenToContextual_injective
#print axioms PentagonAdjoinedSixCell.selectedContextualSeventeen_leftStable
#print axioms PentagonAdjoinedSixCell.selectedContextualSeventeen_rightStable
#print axioms PentagonAdjoinedSixCell.selectedContextualSeventeen_preservesSixteenTrace
#print axioms PentagonAdjoinedSixCell.selectedContextSeventeenSetoid
#print axioms PentagonAdjoinedSixCell.selectedContextSeventeenClass
#print axioms PentagonAdjoinedSixCell.selectedContextSeventeenClass_eq_iff
#print axioms PentagonAdjoinedSixCell.selectedContextSeventeenTraceOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedContextSeventeenTrace_onClass
#print axioms PentagonAdjoinedSixCell.selectedContextSeventeen_inheritedUnit_classEq
#print axioms PentagonAdjoinedSixCell.selectedContextSeventeen_noFirstTagDescent
#print axioms PentagonAdjoinedSixCell.SelectedOuterAdjacentSwap
#print axioms PentagonAdjoinedSixCell.selectedMixedOuterAdjacentSwap
#print axioms PentagonAdjoinedSixCell.selectedAdjacentSwap_changesTrace
#print axioms PentagonAdjoinedSixCell.selectedAdjacentSwap_preservesCounts
#print axioms PentagonAdjoinedSixCell.SelectedMixedTraceChangingCertificate
#print axioms PentagonAdjoinedSixCell.selectedMixedTraceChangingCertificate
#print axioms PentagonAdjoinedSixCell.selectedMixedTraceChange_possible_strictTraceImpossible
#print axioms PentagonAdjoinedSixCell.selectedContextSeventeenFirstAtomTag
#print axioms PentagonAdjoinedSixCell.selectedSeventeenUnitPrependLeft
#print axioms PentagonAdjoinedSixCell.selectedSeventeenUnitAppendLeft
#print axioms PentagonAdjoinedSixCell.selectedSeventeenUnitPrependRight
#print axioms PentagonAdjoinedSixCell.selectedSeventeenUnitAppendRight
#print axioms PentagonAdjoinedSixCell.selectedSeventeenUnitLeft_rawDistinct
#print axioms PentagonAdjoinedSixCell.selectedSeventeenUnitRight_rawDistinct
#print axioms PentagonAdjoinedSixCell.SelectedLocalEighteen
#print axioms PentagonAdjoinedSixCell.selectedLocalEighteen_leftWitness
#print axioms PentagonAdjoinedSixCell.selectedLocalEighteen_rightWitness
#print axioms PentagonAdjoinedSixCell.selectedLocalEighteen_noRawEqualityInterpreter

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
