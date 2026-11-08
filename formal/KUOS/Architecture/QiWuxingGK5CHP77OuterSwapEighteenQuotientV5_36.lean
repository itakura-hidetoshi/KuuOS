import KUOS.Architecture.QiWuxingGK5CHP77ContextualSeventeenTraceSwapV5_35

/-!
Qi v5.36 — finite adjacent-swap observation quotient and exact-fiber
selected 18D quotient, with two different authority boundaries.

The ACTUAL v5.35 `SelectedOuterAdjacentSwap` compares only opposite
orders of exterior left/right seventh-cell EVENTS in `List Bool`.
We close that concrete witness under finite prefixing, reflection,
transitive composition and identity. This builds a proof-relevant
equivalence relation on OBSERVATIONS, not a new higher source cell.
The resulting quotient preserves the counts of left/right events,
but destroys literal ordered List Bool equality. A genuine
double-whisker-derived v5.33 12D–14D packet accompanies each
LR/RL swap. The old trace-preserving higher gate is STILL empty;
the distinct trace-changing observation certificate survives.

Separately, we form a *new* quotient of truly parallel raw 17D
proofs by the v5.35 selected local 18D grammar. Every selected 18D
generator preserves the ordered exterior 17D context trace; this
fine trace therefore descends through the selected 18D quotient.
The first-constructor tag of a raw 17D proof does NOT descend,
as the actual local 18D unit-pasting critical comparison joins
two raw-distinct terms (first atoms 3 and 0).

On the genuinely typed 17D left-after-right and right-after-left
exterior transports, 18D-quotient fine traces are different as
COMMON List Bool values, though each side lives in its OWN exact
16D-dependent quotient. However their images in the **coarser
finite SWAP quotient of observations** are equal. This strictly
separates source authority, selected higher-cell quotient, and
the independently chosen observation-level coarsening.

No cross-fiber 18D interchange, raw Type equality, global
coherence, implicit weakening, or trace-preserving mixed gluing
is postulated. All original F55/P77/GK5CG, old 6D–14D, and every
v5.23–v5.35 selected proof source are untouched. Append-only /
tighten-only / overwrite-forbidden / same-root. No new axioms/sorry.
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

/-- Contextual closure of the EXACT v5.35 adjacent swap in the
SHARED finite observation Type `List Bool`. This is not an
unrestricted 18D source comparison. -/
inductive SelectedOuterSwapClosure : List Bool → List Bool → Type where
  | strict (xs : List Bool) :
      SelectedOuterSwapClosure xs xs
  | observed {xs ys : List Bool}
      (a : SelectedOuterAdjacentSwap xs ys) :
      SelectedOuterSwapClosure xs ys
  | prefix (b : Bool) {xs ys : List Bool}
      (h : SelectedOuterSwapClosure xs ys) :
      SelectedOuterSwapClosure (b :: xs) (b :: ys)
  | reverse {xs ys : List Bool}
      (h : SelectedOuterSwapClosure xs ys) :
      SelectedOuterSwapClosure ys xs
  | chain {xs ys zs : List Bool}
      (h : SelectedOuterSwapClosure xs ys)
      (k : SelectedOuterSwapClosure ys zs) :
      SelectedOuterSwapClosure xs zs

/-- The coarse two-component event count is invariant under EVERY
generator of finite adjacent-swap closure. -/
theorem selectedOuterSwapClosure_preservesCounts
    {xs ys : List Bool}
    (h : SelectedOuterSwapClosure xs ys) :
    selectedFifteenTraceCounts xs = selectedFifteenTraceCounts ys := by
  induction h with
  | strict xs => rfl
  | observed a =>
      cases a with
      | leftRightToRightLeft tail =>
          exact selectedAdjacentSwap_preservesCounts tail
      | rightLeftToLeftRight tail =>
          exact (selectedAdjacentSwap_preservesCounts tail).symm
  | prefix b h ih =>
      cases b with
      | false =>
          have hh := congrArg (fun p : Nat × Nat => (p.1 + 1, p.2)) ih
          simpa [selectedFifteenTraceCounts] using hh
      | true =>
          have hh := congrArg (fun p : Nat × Nat => (p.1, p.2 + 1)) ih
          simpa [selectedFifteenTraceCounts] using hh
  | reverse h ih => exact ih.symm
  | chain h k ih ih' => exact ih.trans ih'

/-- A separately chosen setoid on FINITE ORDER OBSERVATIONS. -/
def selectedOuterSwapSetoid : Setoid (List Bool) where
  r := fun xs ys => Nonempty (SelectedOuterSwapClosure xs ys)
  iseqv := by
    constructor
    · intro xs
      exact ⟨.strict xs⟩
    · intro xs ys h
      rcases h with ⟨a⟩
      exact ⟨.reverse a⟩
    · intro xs ys zs h k
      rcases h with ⟨a⟩
      rcases k with ⟨b⟩
      exact ⟨.chain a b⟩

def selectedOuterSwapClass (xs : List Bool) :
    Quotient selectedOuterSwapSetoid :=
  Quotient.mk _ xs

theorem selectedOuterSwapClass_eq_iff (xs ys : List Bool) :
    selectedOuterSwapClass xs = selectedOuterSwapClass ys ↔
      Nonempty (SelectedOuterSwapClosure xs ys) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- A concrete adjacent swap identifies opposite LR/RL order
observations in the NEW quotient but does not make them raw equal. -/
theorem selectedOuterSwap_headClassEq (tail : List Bool) :
    selectedOuterSwapClass (false :: true :: tail) =
      selectedOuterSwapClass (true :: false :: tail) :=
  Quotient.sound ⟨.observed (.leftRightToRightLeft tail)⟩

/-- Adding an identical finite prefix preserves proof-relevant swap
comparison and therefore its chosen observation quotient equality. -/
theorem selectedOuterSwap_prefixClassEq (b : Bool) {xs ys : List Bool}
    (h : selectedOuterSwapClass xs = selectedOuterSwapClass ys) :
    selectedOuterSwapClass (b :: xs) =
      selectedOuterSwapClass (b :: ys) := by
  have hw : Nonempty (SelectedOuterSwapClosure xs ys) :=
    (selectedOuterSwapClass_eq_iff xs ys).mp h
  rcases hw with ⟨w⟩
  exact Quotient.sound ⟨.prefix b w⟩

/-- Event counts descend: the selected finite adjacent swap keeps
one left and one right event while forgetting their order. -/
def selectedOuterSwapCountsOnQuotient :
    Quotient selectedOuterSwapSetoid → Nat × Nat :=
  Quotient.lift selectedFifteenTraceCounts (by
    intro xs ys h
    rcases h with ⟨a⟩
    exact selectedOuterSwapClosure_preservesCounts a)

theorem selectedOuterSwapCounts_onClass (xs : List Bool) :
    selectedOuterSwapCountsOnQuotient (selectedOuterSwapClass xs) =
      selectedFifteenTraceCounts xs :=
  rfl

/-- The observation quotient is nonfaithful: true adjacent swap
classes agree even though the underlying Bool list does NOT. -/
theorem selectedOuterSwap_projectionNotInjective :
    ¬ Function.Injective selectedOuterSwapClass := by
  intro inj
  exact selectedAdjacentSwap_changesTrace []
    (inj (selectedOuterSwap_headClassEq []))

/-- Literal ordered raw trace does NOT descend through the separate
adjacent-swap quotient. This is not in conflict with its descent
through the v5.34/35 selected 17D quotient, which uses a DIFFERENT
equivalence relation. -/
theorem selectedOuterSwap_noRawTraceDescent :
    ¬ (∃ g : Quotient selectedOuterSwapSetoid → List Bool,
      ∀ xs : List Bool, g (selectedOuterSwapClass xs) = xs) := by
  rintro ⟨g, hg⟩
  have h : false :: true :: ([] : List Bool) =
      true :: false :: ([] : List Bool) := by
    calc
      _ = g (selectedOuterSwapClass (false :: true :: [])) :=
        (hg _).symm
      _ = g (selectedOuterSwapClass (true :: false :: [])) :=
        congrArg g (selectedOuterSwap_headClassEq [])
      _ = _ := hg _
  exact selectedAdjacentSwap_changesTrace [] h

/-- The ACTUAL v5.35 lower 12D–14D packet and the trace swap
transport into the observational quotient without a new original
mixed 18D equality. -/
theorem selectedMixedTraceChange_swapClassEq (l r : W) {w z : W}
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
    selectedOuterSwapClass
        (selectedContextSixteenTrace l r
          (selectedSixteenLeftAfterRight l r left F G H right)) =
      selectedOuterSwapClass
        (selectedContextSixteenTrace l r
          (selectedSixteenRightAfterLeft l r left F G H right)) := by
  change selectedOuterSwapClass
      (false :: true :: selectedContextSixteenTrace l r H) =
        selectedOuterSwapClass
          (true :: false :: selectedContextSixteenTrace l r H)
  exact selectedOuterSwap_headClassEq _

/-- This is the *precise* distinction: the finite trace-swap is
available as an OBSERVATION comparison; the v5.34 strict trace gate
is not. No heterogeneous source-level comparison is inferred. -/
theorem selectedMixedSwapCoarseCompatible_strictGateImpossible (l r : W)
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
    Nonempty (SelectedMixedLowerHigherPacket l r left F G C right) ∧
    selectedOuterSwapClass
        (selectedContextSixteenTrace l r
          (selectedSixteenLeftAfterRight l r left F G H right)) =
      selectedOuterSwapClass
        (selectedContextSixteenTrace l r
          (selectedSixteenRightAfterLeft l r left F G H right)) ∧
    ¬ Nonempty (SelectedMixedTraceRespectingHigherGate l r
      left F G C H right) :=
  ⟨⟨selectedMixedLowerHigherPacket l r left F G C right⟩,
    selectedMixedTraceChange_swapClassEq l r left F G C H right,
    selectedMixedTraceRespectingHigherGate_empty l r left F G C H right⟩

/-- A finite ordered trace for the *raw 17D syntax itself*.
This does NOT erase inherited v5.33 17D proof values or equate
heterogeneous dependent 16D fibers. -/
def selectedContextSeventeenTrace (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedContextualSeventeen W l r H K) : List Bool :=
  match J with
  | .inherited _ => []
  | .whiskerLeft _ _ _ J => false :: selectedContextSeventeenTrace l r J
  | .whiskerRight _ _ J _ => true :: selectedContextSeventeenTrace l r J
  | .strict _ => []
  | .reverse J => selectedContextSeventeenTrace l r J
  | .chain J K =>
      selectedContextSeventeenTrace l r J ++ selectedContextSeventeenTrace l r K

/-- Every v5.35 exact-fiber SELECTED 18D comparison preserves the
external 17D context trace, including both actual local unit cells. -/
theorem selectedEighteen_preservesSeventeenTrace (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    selectedContextSeventeenTrace l r J =
      selectedContextSeventeenTrace l r N := by
  induction M with
  | strict J => rfl
  | unitLeft before F G C after => rfl
  | unitRight before F G C after => rfl
  | reverse M ih => exact ih.symm
  | chain M N ih ih' => exact ih.trans ih'

/-- Separately typed quotient of parallel SEVENTEENTH proof values
by actual selected local EIGHTEENTH comparison evidence. -/
def selectedEighteenSetoid (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H K : SelectedContextualSixteen W l r T U) :
    Setoid (SelectedContextualSeventeen W l r H K) where
  r := fun J N => Nonempty (SelectedLocalEighteen W l r J N)
  iseqv := by
    constructor
    · intro J
      exact ⟨.strict J⟩
    · intro J N h
      rcases h with ⟨M⟩
      exact ⟨.reverse M⟩
    · intro J N S h h'
      rcases h with ⟨M⟩
      rcases h' with ⟨L⟩
      exact ⟨.chain M L⟩

def selectedEighteenClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedEighteenSetoid l r H K) :=
  Quotient.mk _ J

theorem selectedEighteenClass_eq_iff (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J N : SelectedContextualSeventeen W l r H K) :
    selectedEighteenClass l r J = selectedEighteenClass l r N ↔
      Nonempty (SelectedLocalEighteen W l r J N) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- The fine ordered 17D trace is an exact Quotient.lift through
the chosen local 18D relation and has an exact on-class formula. -/
def selectedEighteenTraceOnQuotient (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H K : SelectedContextualSixteen W l r T U) :
    Quotient (selectedEighteenSetoid l r H K) → List Bool :=
  Quotient.lift (selectedContextSeventeenTrace l r) (by
    intro J N h
    rcases h with ⟨M⟩
    exact selectedEighteen_preservesSeventeenTrace l r M)

theorem selectedEighteenTrace_onClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedContextualSeventeen W l r H K) :
    selectedEighteenTraceOnQuotient l r H K
        (selectedEighteenClass l r J) =
      selectedContextSeventeenTrace l r J :=
  rfl

/-- A local 18D generator identifies raw-distinct v5.35 17D
unit-pasting histories in the new quotient (not raw Eq). -/
theorem selectedEighteenLeftUnit_classEq (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedEighteenClass l r
        (selectedSeventeenUnitPrependLeft l r before F G C after) =
      selectedEighteenClass l r
        (selectedSeventeenUnitAppendLeft l r before F G C after) :=
  Quotient.sound ⟨.unitLeft before F G C after⟩

theorem selectedEighteenRightUnit_classEq (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedEighteenClass l r
        (selectedSeventeenUnitPrependRight l r before F G C after) =
      selectedEighteenClass l r
        (selectedSeventeenUnitAppendRight l r before F G C after) :=
  Quotient.sound ⟨.unitRight before F G C after⟩

/-- The new selected 18D projection is noninjective at actual
original seventh-context indices. -/
theorem selectedEighteen_projectionNotInjective (l r : W)
    {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    ¬ Function.Injective (fun J : SelectedContextualSeventeen W l r
      (selectedSixteenUnitPrependLeft l r before F G C after)
      (selectedSixteenUnitAppendLeft l r before F G C after) =>
      selectedEighteenClass l r J) := by
  intro injective
  exact selectedSeventeenUnitLeft_rawDistinct l r before F G C after
    (injective (selectedEighteenLeftUnit_classEq l r before F G C after))

/-- Raw 17D first-constructor tag does not survive the selected
18D unit quotient: it distinguishes tag3 from tag0 while the
source 17D terms have equal 18D quotient classes. -/
theorem selectedEighteen_noFirstTagDescent (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    ¬ (∃ g : Quotient (selectedEighteenSetoid l r
        (selectedSixteenUnitPrependLeft l r before F G C after)
        (selectedSixteenUnitAppendLeft l r before F G C after)) → Nat,
      ∀ J : SelectedContextualSeventeen W l r
        (selectedSixteenUnitPrependLeft l r before F G C after)
        (selectedSixteenUnitAppendLeft l r before F G C after),
        g (selectedEighteenClass l r J) =
          selectedContextSeventeenFirstAtomTag l r J) := by
  rintro ⟨g, hg⟩
  have ht : selectedContextSeventeenFirstAtomTag l r
      (selectedSeventeenUnitPrependLeft l r before F G C after) =
        selectedContextSeventeenFirstAtomTag l r
          (selectedSeventeenUnitAppendLeft l r before F G C after) := by
    calc
      _ = g (selectedEighteenClass l r
          (selectedSeventeenUnitPrependLeft l r before F G C after)) :=
        (hg _).symm
      _ = g (selectedEighteenClass l r
          (selectedSeventeenUnitAppendLeft l r before F G C after)) :=
        congrArg g (selectedEighteenLeftUnit_classEq l r before F G C after)
      _ = _ := hg _
  change (3 : Nat) = 0 at ht
  cases ht

/-- The TWO original seventh-context transport orders acting on
a true selected 17D comparison. Their 16D/17D dependent indices
may differ; the outputs stay independently typed. -/
def selectedSeventeenLeftAfterRight (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedContextualSeventeen W l r H K)
    (right : SevenRewrite W l r c d) :
    SelectedContextualSeventeen W l r
      (.whiskerLeft left
        (contextFrameRight l r F right)
        (contextFrameRight l r G right)
        (.whiskerRight F G H right))
      (.whiskerLeft left
        (contextFrameRight l r F right)
        (contextFrameRight l r G right)
        (.whiskerRight F G K right)) :=
  .whiskerLeft left
    (contextFrameRight l r F right)
    (contextFrameRight l r G right)
    (.whiskerRight F G J right)

def selectedSeventeenRightAfterLeft (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedContextualSeventeen W l r H K)
    (right : SevenRewrite W l r c d) :
    SelectedContextualSeventeen W l r
      (.whiskerRight
        (contextFrameLeft l r left F)
        (contextFrameLeft l r left G)
        (.whiskerLeft left F G H) right)
      (.whiskerRight
        (contextFrameLeft l r left F)
        (contextFrameLeft l r left G)
        (.whiskerLeft left F G K) right) :=
  .whiskerRight
    (contextFrameLeft l r left F)
    (contextFrameLeft l r left G)
    (.whiskerLeft left F G J) right

/-- Both typed mixed 17D transports retain their order as actual
finite raw 17D observations. -/
theorem selectedSeventeenMixedTraceValues (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedContextualSeventeen W l r H K)
    (right : SevenRewrite W l r c d) :
    selectedContextSeventeenTrace l r
        (selectedSeventeenLeftAfterRight l r left F G J right) =
          false :: true :: selectedContextSeventeenTrace l r J ∧
    selectedContextSeventeenTrace l r
        (selectedSeventeenRightAfterLeft l r left F G J right) =
          true :: false :: selectedContextSeventeenTrace l r J := by
  constructor <;> rfl

/-- After taking SEPARATELY TYPED local 18D quotients, ordered
traces remain different as values in the COMMON List Bool codomain. -/
theorem selectedEighteenMixedOrder_fineTraceDistinct (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedContextualSeventeen W l r H K)
    (right : SevenRewrite W l r c d) :
    selectedEighteenTraceOnQuotient l r _ _
        (selectedEighteenClass l r
          (selectedSeventeenLeftAfterRight l r left F G J right)) ≠
      selectedEighteenTraceOnQuotient l r _ _
        (selectedEighteenClass l r
          (selectedSeventeenRightAfterLeft l r left F G J right)) := by
  change false :: true :: selectedContextSeventeenTrace l r J ≠
    true :: false :: selectedContextSeventeenTrace l r J
  exact selectedAdjacentSwap_changesTrace _

/-- Although the fine 18D-quotient trace values are DISTINCT, their
images in the *coarser observation swap quotient* agree. The
equality is between two values of a SHARED observation quotient,
not between the original heterogeneous 17D proofs. -/
theorem selectedEighteenMixedOrder_swapObservationsAgree (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedContextualSeventeen W l r H K)
    (right : SevenRewrite W l r c d) :
    selectedOuterSwapClass
      (selectedEighteenTraceOnQuotient l r _ _
        (selectedEighteenClass l r
          (selectedSeventeenLeftAfterRight l r left F G J right))) =
    selectedOuterSwapClass
      (selectedEighteenTraceOnQuotient l r _ _
        (selectedEighteenClass l r
          (selectedSeventeenRightAfterLeft l r left F G J right))) := by
  change selectedOuterSwapClass
      (false :: true :: selectedContextSeventeenTrace l r J) =
        selectedOuterSwapClass
          (true :: false :: selectedContextSeventeenTrace l r J)
  exact selectedOuterSwap_headClassEq _

theorem selectedEighteenMixedOrder_coarseCountsAgree (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedContextualSeventeen W l r H K)
    (right : SevenRewrite W l r c d) :
    selectedOuterSwapCountsOnQuotient
      (selectedOuterSwapClass
        (selectedEighteenTraceOnQuotient l r _ _
          (selectedEighteenClass l r
            (selectedSeventeenLeftAfterRight l r left F G J right)))) =
    selectedOuterSwapCountsOnQuotient
      (selectedOuterSwapClass
        (selectedEighteenTraceOnQuotient l r _ _
          (selectedEighteenClass l r
            (selectedSeventeenRightAfterLeft l r left F G J right)))) := by
  exact congrArg selectedOuterSwapCountsOnQuotient
    (selectedEighteenMixedOrder_swapObservationsAgree l r left F G J right)

#print axioms PentagonAdjoinedSixCell.SelectedOuterSwapClosure
#print axioms PentagonAdjoinedSixCell.selectedOuterSwapClosure_preservesCounts
#print axioms PentagonAdjoinedSixCell.selectedOuterSwapSetoid
#print axioms PentagonAdjoinedSixCell.selectedOuterSwapClass
#print axioms PentagonAdjoinedSixCell.selectedOuterSwapClass_eq_iff
#print axioms PentagonAdjoinedSixCell.selectedOuterSwap_headClassEq
#print axioms PentagonAdjoinedSixCell.selectedOuterSwap_prefixClassEq
#print axioms PentagonAdjoinedSixCell.selectedOuterSwapCountsOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedOuterSwapCounts_onClass
#print axioms PentagonAdjoinedSixCell.selectedOuterSwap_projectionNotInjective
#print axioms PentagonAdjoinedSixCell.selectedOuterSwap_noRawTraceDescent
#print axioms PentagonAdjoinedSixCell.selectedMixedTraceChange_swapClassEq
#print axioms PentagonAdjoinedSixCell.selectedMixedSwapCoarseCompatible_strictGateImpossible
#print axioms PentagonAdjoinedSixCell.selectedContextSeventeenTrace
#print axioms PentagonAdjoinedSixCell.selectedEighteen_preservesSeventeenTrace
#print axioms PentagonAdjoinedSixCell.selectedEighteenSetoid
#print axioms PentagonAdjoinedSixCell.selectedEighteenClass
#print axioms PentagonAdjoinedSixCell.selectedEighteenClass_eq_iff
#print axioms PentagonAdjoinedSixCell.selectedEighteenTraceOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedEighteenTrace_onClass
#print axioms PentagonAdjoinedSixCell.selectedEighteenLeftUnit_classEq
#print axioms PentagonAdjoinedSixCell.selectedEighteenRightUnit_classEq
#print axioms PentagonAdjoinedSixCell.selectedEighteen_projectionNotInjective
#print axioms PentagonAdjoinedSixCell.selectedEighteen_noFirstTagDescent
#print axioms PentagonAdjoinedSixCell.selectedSeventeenLeftAfterRight
#print axioms PentagonAdjoinedSixCell.selectedSeventeenRightAfterLeft
#print axioms PentagonAdjoinedSixCell.selectedSeventeenMixedTraceValues
#print axioms PentagonAdjoinedSixCell.selectedEighteenMixedOrder_fineTraceDistinct
#print axioms PentagonAdjoinedSixCell.selectedEighteenMixedOrder_swapObservationsAgree
#print axioms PentagonAdjoinedSixCell.selectedEighteenMixedOrder_coarseCountsAgree

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
