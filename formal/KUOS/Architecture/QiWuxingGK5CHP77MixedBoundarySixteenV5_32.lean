import KUOS.Architecture.QiWuxingGK5CHP77ContextualFifteenDescentV5_31

/-!
Qi v5.32 — exact lower-boundary certificates for ordered 15D
contexts, genuinely typed local selected 16D unit-roundtrip
comparisons, and selective trace descent at the 16D quotient.

The original v5.31 mixed seventh-cell transports L(R(T)) and
R(L(T)) do NOT have definitionally matching FOURTEENTH endpoints.
We never invent an ill-typed raw equality or an unconditional 16D
interchanger between them.  Instead, an ACTUAL original v5.18
double-whisker, embedded through v5.25/v5.27, produces a full
two-sided 12D boundary-bridge packet for their underlying 11D
source/target.  This is a necessary LOWER-DIMENSIONAL compatibility
certificate, not an unearned 14D/15D higher interchange.

For parallel, exactly typed v5.31 selected fifteenth witnesses we
construct the next genuine local critical pair: a forward-and-back
old unit 15D proof versus its reflexive 15D proof, and symmetrically
a backward-and-forward loop.  Both 15D loops are RAW distinct from
reflexivity, certified by their constructor tags.  An INDEPENDENT,
explicitly SELECTED 16D grammar adjoins only these two LOCAL
unit-loop comparisons (plus strict/reverse/chain).  No global 16D
coherence, mixed-order 16D interchange or strictification follows.

The resulting 15D quotient preserves the ordered List Bool trace
as a valid observable; an exact Quotient.lift is constructed and
proved on classes.  The raw 15D FIRST-CONSTRUCTOR tag, conversely,
does NOT descend because the selected 16D local unit generator
relates raw tags 0 and 3.  The 16D trace quotient still distinguishes
the TWO independently indexed mixed-context transport histories
[false,true]++trace(T) and [true,false]++trace(T), whereas the number
of left and right events is identical.  The comparison is via a
COMMON observable codomain, never illicit equality of proofs
from different dependent Type indices.

All old F55/P77/GK5CG, original 6D-14D proof sources, and all
earlier selected presentations remain unchanged.  Append-only,
tighten-only, same-root, no new axioms, no sorry.
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

/-- The original seventh-cell mixed exterior order has two GENUINE
v5.18/v5.27 bridges at the 11D source and target.  The packet
certifies lower-boundary compatibility, NOT a 16D equivalence. -/
structure SelectedMixedLowerBoundaryPacket (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    (right : SevenRewrite W l r c d) : Type uSix where
  source :
    SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r
        (contextFrameLeft l r left (contextFrameRight l r F right)))
      (contextFramePack l r
        (contextFrameRight l r (contextFrameLeft l r left F) right))
  target :
    SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r
        (contextFrameLeft l r left (contextFrameRight l r G right)))
      (contextFramePack l r
        (contextFrameRight l r (contextFrameLeft l r left G) right))

/-- Construct BOTH lower bridges from the ACTUAL prior double-whisker
proof constructor; there is no bridge postulate or new 12D rule. -/
def selectedMixedLowerBoundaryPacket (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    (right : SevenRewrite W l r c d) :
    SelectedMixedLowerBoundaryPacket l r left F G right :=
  ⟨selectedMixedBoundaryBridge l r left F right,
    selectedMixedBoundaryBridge l r left G right⟩

theorem selectedMixedLowerBoundaryQuotients (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    (right : SevenRewrite W l r c d) :
    selectedUnitalClass l r
        (contextFramePack l r
          (contextFrameLeft l r left (contextFrameRight l r F right))) =
      selectedUnitalClass l r
        (contextFramePack l r
          (contextFrameRight l r (contextFrameLeft l r left F) right)) ∧
    selectedUnitalClass l r
        (contextFramePack l r
          (contextFrameLeft l r left (contextFrameRight l r G right))) =
      selectedUnitalClass l r
        (contextFramePack l r
          (contextFrameRight l r (contextFrameLeft l r left G) right)) :=
  ⟨Quotient.sound ⟨(selectedMixedLowerBoundaryPacket l r left F G right).source⟩,
    Quotient.sound ⟨(selectedMixedLowerBoundaryPacket l r left F G right).target⟩⟩

/-- Count the two kinds of outer context actions while FORGETTING
their order.  This is NOT the fully faithful List Bool history. -/
def selectedFifteenTraceCounts (xs : List Bool) : Nat × Nat :=
  ((xs.filter (fun b => b = false)).length,
    (xs.filter (fun b => b = true)).length)

/-- Both actually typed mixed-context 15D transports carry one new
left and one new right action, regardless of their order. -/
theorem selectedFifteenMixedCountsEqual (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedContextualFifteen W l r V X)
    (right : SevenRewrite W l r c d) :
    selectedFifteenTraceCounts
        (selectedContextFifteenTrace l r
          (selectedFifteenLeftAfterRight l r left F G T right)) =
      selectedFifteenTraceCounts
        (selectedContextFifteenTrace l r
          (selectedFifteenRightAfterLeft l r left F G T right)) := by
  simp only [selectedFifteenTraceCounts]
  rw [(selectedFifteenMixedTraceValues l r left F G T right).1]
  rw [(selectedFifteenMixedTraceValues l r left F G T right).2]
  simp

/-- Coarse event counts agree while fine proof-order observations
do NOT agree: equality of lengths was already proved in v5.31. -/
theorem selectedFifteenMixedCoarseFineSeparation (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedContextualFifteen W l r V X)
    (right : SevenRewrite W l r c d) :
    selectedFifteenTraceCounts
        (selectedContextFifteenTrace l r
          (selectedFifteenLeftAfterRight l r left F G T right)) =
      selectedFifteenTraceCounts
        (selectedContextFifteenTrace l r
          (selectedFifteenRightAfterLeft l r left F G T right)) ∧
    selectedContextFifteenTrace l r
        (selectedFifteenLeftAfterRight l r left F G T right) ≠
      selectedContextFifteenTrace l r
        (selectedFifteenRightAfterLeft l r left F G T right) :=
  ⟨selectedFifteenMixedCountsEqual l r left F G T right,
    selectedFifteenMixedTrace_obstruction l r left F G T right⟩

/-- Close the original v5.30 unit critical cell in the OPPOSITE
direction, retaining the original v5.31 witnessed comparison. -/
def selectedFifteenUnitReverseRoundtrip (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    SelectedContextualFifteen W l r
      (selectedMixedFourteenUnitAppend l r before F G C after)
      (selectedMixedFourteenUnitAppend l r before F G C after) :=
  .chain
    (.reverse (selectedFifteenContextualUnit l r before F G C after))
    (selectedFifteenContextualUnit l r before F G C after)

/-- RAW 15D first atomic constructor, which is not a quotient
observer.  It ignores dependent historical indices but preserves
the choice between a real 15D roundtrip and a strict witness. -/
def selectedFifteenFirstAtomTag (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedContextualFifteen W l r V X) : Nat :=
  match T with
  | .inherited _ => 0
  | .whiskerLeft _ _ _ _ => 1
  | .whiskerRight _ _ _ _ => 2
  | .strict _ => 3
  | .reverse _ => 4
  | .chain T _ => selectedFifteenFirstAtomTag l r T

theorem selectedFifteenUnitRoundtrip_rawDistinct (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedFifteenUnitRoundtrip l r before F G C after ≠
      SelectedContextualFifteen.strict
        (selectedMixedFourteenUnitPrepend l r before F G C after) := by
  intro h
  have ht := congrArg (selectedFifteenFirstAtomTag l r) h
  change (0 : Nat) = 3 at ht
  cases ht

theorem selectedFifteenReverseRoundtrip_rawDistinct (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedFifteenUnitReverseRoundtrip l r before F G C after ≠
      SelectedContextualFifteen.strict
        (selectedMixedFourteenUnitAppend l r before F G C after) := by
  intro h
  have ht := congrArg (selectedFifteenFirstAtomTag l r) h
  change (4 : Nat) = 3 at ht
  cases ht

/-- The fine outer-order trace is BLIND to these old unit loops:
both loops and strict 15D witnesses contain no new outer context
whiskerings, despite being distinct RAW proof objects. -/
theorem selectedFifteenUnitRoundtrip_traceBlind (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedContextFifteenTrace l r
        (selectedFifteenUnitRoundtrip l r before F G C after) =
      selectedContextFifteenTrace l r
        (SelectedContextualFifteen.strict
          (selectedMixedFourteenUnitPrepend l r before F G C after)) :=
  rfl

theorem selectedFifteenReverseRoundtrip_traceBlind (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedContextFifteenTrace l r
        (selectedFifteenUnitReverseRoundtrip l r before F G C after) =
      selectedContextFifteenTrace l r
        (SelectedContextualFifteen.strict
          (selectedMixedFourteenUnitAppend l r before F G C after)) :=
  rfl

/-- Independent, explicitly SELECTED sixteen-cell comparison on
PARALLEL 15D proof terms at EXACTLY MATCHING original 14D endpoints.
Only the two genuine local unit-roundtrip families are adjoined.
Crucially there is no constructor for L(R(T)) versus R(L(T))
when their full dependent 14D boundaries differ. -/
inductive SelectedLocalSixteen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    {P Q : SelectedUnitalCompositionTwelve W l r F G} →
    {C D : SelectedMixedInterchangerThirteen W l r P Q} →
    {V X : SelectedMixedNaturalityFourteen W l r C D} →
    SelectedContextualFifteen W l r V X →
    SelectedContextualFifteen W l r V X → Type uSix where
  | strict {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      (T : SelectedContextualFifteen W l r V X) :
      SelectedLocalSixteen W l r T T
  | unitRoundtripLeft {w z : W}
      {b c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      (C : SelectedContextualThirteen W l r P Q)
      (after : SevenRewrite W l r d e) :
      SelectedLocalSixteen W l r
        (selectedFifteenUnitRoundtrip l r before F G C after)
        (SelectedContextualFifteen.strict
          (selectedMixedFourteenUnitPrepend l r before F G C after))
  | unitRoundtripRight {w z : W}
      {b c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      (C : SelectedContextualThirteen W l r P Q)
      (after : SevenRewrite W l r d e) :
      SelectedLocalSixteen W l r
        (selectedFifteenUnitReverseRoundtrip l r before F G C after)
        (SelectedContextualFifteen.strict
          (selectedMixedFourteenUnitAppend l r before F G C after))
  | reverse {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      (H : SelectedLocalSixteen W l r T U) :
      SelectedLocalSixteen W l r U T
  | chain {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U Z : SelectedContextualFifteen W l r V X}
      (H : SelectedLocalSixteen W l r T U)
      (K : SelectedLocalSixteen W l r U Z) :
      SelectedLocalSixteen W l r T Z

/-- Nontrivial strictly typed 16D local comparisons coexist with
explicit non-equality of the underlying raw 15D witnesses. -/
theorem selectedSixteenLeftUnitWitness (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    Nonempty (SelectedLocalSixteen W l r
      (selectedFifteenUnitRoundtrip l r before F G C after)
      (SelectedContextualFifteen.strict
        (selectedMixedFourteenUnitPrepend l r before F G C after))) ∧
    selectedFifteenUnitRoundtrip l r before F G C after ≠
      SelectedContextualFifteen.strict
        (selectedMixedFourteenUnitPrepend l r before F G C after) :=
  ⟨⟨.unitRoundtripLeft before F G C after⟩,
    selectedFifteenUnitRoundtrip_rawDistinct l r before F G C after⟩

theorem selectedSixteenRightUnitWitness (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    Nonempty (SelectedLocalSixteen W l r
      (selectedFifteenUnitReverseRoundtrip l r before F G C after)
      (SelectedContextualFifteen.strict
        (selectedMixedFourteenUnitAppend l r before F G C after))) ∧
    selectedFifteenUnitReverseRoundtrip l r before F G C after ≠
      SelectedContextualFifteen.strict
        (selectedMixedFourteenUnitAppend l r before F G C after) :=
  ⟨⟨.unitRoundtripRight before F G C after⟩,
    selectedFifteenReverseRoundtrip_rawDistinct l r before F G C after⟩

/-- The selected 16D grammar PRESERVES the genuine v5.31 outer
context order trace across its five constructors.  This is a
nontrivial invariance that the raw FIRST-CONSTRUCTOR tag lacks. -/
theorem selectedSixteen_preservesTrace (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedLocalSixteen W l r T U) :
    selectedContextFifteenTrace l r T = selectedContextFifteenTrace l r U := by
  induction H with
  | strict T => rfl
  | unitRoundtripLeft before F G C after => rfl
  | unitRoundtripRight before F G C after => rfl
  | reverse H ih => exact ih.symm
  | chain H K ih ih' => exact ih.trans ih'

/-- A NEW quotient of parallel FIFTEENTH proofs by the explicit
LOCAL selected 16D presentation.  The quotient is distinct from
v5.31's quotient of FOURTEENTH proofs by selected 15D. -/
def selectedSixteenSetoid (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    (V X : SelectedMixedNaturalityFourteen W l r C D) :
    Setoid (SelectedContextualFifteen W l r V X) where
  r := fun T U => Nonempty (SelectedLocalSixteen W l r T U)
  iseqv := by
    constructor
    · intro T
      exact ⟨.strict T⟩
    · intro T U h
      rcases h with ⟨H⟩
      exact ⟨.reverse H⟩
    · intro T U Z h h'
      rcases h with ⟨H⟩
      rcases h' with ⟨K⟩
      exact ⟨.chain H K⟩

def selectedSixteenClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedContextualFifteen W l r V X) :
    Quotient (selectedSixteenSetoid l r V X) :=
  Quotient.mk _ T

theorem selectedSixteenClass_eq_iff (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T U : SelectedContextualFifteen W l r V X) :
    selectedSixteenClass l r T = selectedSixteenClass l r U ↔
      Nonempty (SelectedLocalSixteen W l r T U) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- The entire ordered Bool list DESCENDS into the local 16D
quotient because all new 16D generators preserve it. -/
def selectedSixteenTraceOnQuotient (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    (V X : SelectedMixedNaturalityFourteen W l r C D) :
    Quotient (selectedSixteenSetoid l r V X) → List Bool :=
  Quotient.lift (selectedContextFifteenTrace l r) (by
    intro T U h
    rcases h with ⟨H⟩
    exact selectedSixteen_preservesTrace l r H)

theorem selectedSixteenTrace_onClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedContextualFifteen W l r V X) :
    selectedSixteenTraceOnQuotient l r V X (selectedSixteenClass l r T) =
      selectedContextFifteenTrace l r T :=
  rfl

/-- Actual selected local 16D witnesses identify proof loops with
their 15D strict identities only at the NEW quotient level. -/
theorem selectedSixteenLeftUnitClassEq (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedSixteenClass l r
        (selectedFifteenUnitRoundtrip l r before F G C after) =
      selectedSixteenClass l r
        (SelectedContextualFifteen.strict
          (selectedMixedFourteenUnitPrepend l r before F G C after)) :=
  Quotient.sound ⟨SelectedLocalSixteen.unitRoundtripLeft before F G C after⟩

theorem selectedSixteenRightUnitClassEq (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedSixteenClass l r
        (selectedFifteenUnitReverseRoundtrip l r before F G C after) =
      selectedSixteenClass l r
        (SelectedContextualFifteen.strict
          (selectedMixedFourteenUnitAppend l r before F G C after)) :=
  Quotient.sound ⟨SelectedLocalSixteen.unitRoundtripRight before F G C after⟩

/-- Raw 15D atomic constructor tag cannot descend through the
new 16D quotient: a proven nontrivial local loop has tag 0 but
its quotient-identical strict witness has tag 3. -/
theorem selectedSixteen_noFirstTagDescent (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    ¬ (∃ g : Quotient (selectedSixteenSetoid l r
        (selectedMixedFourteenUnitPrepend l r before F G C after)
        (selectedMixedFourteenUnitPrepend l r before F G C after)) → Nat,
      ∀ (T : SelectedContextualFifteen W l r
        (selectedMixedFourteenUnitPrepend l r before F G C after)
        (selectedMixedFourteenUnitPrepend l r before F G C after)),
        g (selectedSixteenClass l r T) =
          selectedFifteenFirstAtomTag l r T) := by
  rintro ⟨g, hg⟩
  have ht : selectedFifteenFirstAtomTag l r
      (selectedFifteenUnitRoundtrip l r before F G C after) =
      selectedFifteenFirstAtomTag l r
        (SelectedContextualFifteen.strict
          (selectedMixedFourteenUnitPrepend l r before F G C after)) := by
    calc
      _ = g (selectedSixteenClass l r
            (selectedFifteenUnitRoundtrip l r before F G C after)) :=
          (hg _).symm
      _ = g (selectedSixteenClass l r
            (SelectedContextualFifteen.strict
              (selectedMixedFourteenUnitPrepend l r before F G C after))) :=
          congrArg g (selectedSixteenLeftUnitClassEq l r before F G C after)
      _ = _ := hg _
  change (0 : Nat) = 3 at ht
  cases ht

/-- The fine ordered external 15D history remains distinguishable
AFTER local 16D unit quotient, in a common List Bool observation
space.  The two terms themselves are still in DIFFERENT dependent
14D-indexed fibers and are NOT asserted to be equal or comparable
by any invented global 16D witness. -/
theorem selectedSixteenMixedOrderTraceObstruction (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedContextualFifteen W l r V X)
    (right : SevenRewrite W l r c d) :
    selectedSixteenTraceOnQuotient l r _ _
        (selectedSixteenClass l r
          (selectedFifteenLeftAfterRight l r left F G T right)) ≠
      selectedSixteenTraceOnQuotient l r _ _
        (selectedSixteenClass l r
          (selectedFifteenRightAfterLeft l r left F G T right)) := by
  change
    selectedContextFifteenTrace l r
        (selectedFifteenLeftAfterRight l r left F G T right) ≠
      selectedContextFifteenTrace l r
        (selectedFifteenRightAfterLeft l r left F G T right)
  exact selectedFifteenMixedTrace_obstruction l r left F G T right

theorem selectedSixteenMixedOrderCountAgreement (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedContextualFifteen W l r V X)
    (right : SevenRewrite W l r c d) :
    selectedFifteenTraceCounts
        (selectedSixteenTraceOnQuotient l r _ _
          (selectedSixteenClass l r
            (selectedFifteenLeftAfterRight l r left F G T right))) =
      selectedFifteenTraceCounts
        (selectedSixteenTraceOnQuotient l r _ _
          (selectedSixteenClass l r
            (selectedFifteenRightAfterLeft l r left F G T right))) := by
  change
    selectedFifteenTraceCounts
        (selectedContextFifteenTrace l r
          (selectedFifteenLeftAfterRight l r left F G T right)) =
      selectedFifteenTraceCounts
        (selectedContextFifteenTrace l r
          (selectedFifteenRightAfterLeft l r left F G T right))
  exact selectedFifteenMixedCountsEqual l r left F G T right

/-- A selected local 16D unit comparison is not an interpreter
into strict equality of arbitrary raw 15D proof terms. -/
theorem selectedSixteen_noRawEqualityInterpreter (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    ¬ (∀
      (T U : SelectedContextualFifteen W l r
        (selectedMixedFourteenUnitPrepend l r before F G C after)
        (selectedMixedFourteenUnitPrepend l r before F G C after)),
      SelectedLocalSixteen W l r T U → T = U) := by
  intro interpret
  exact selectedFifteenUnitRoundtrip_rawDistinct l r before F G C after
    (interpret _ _ (.unitRoundtripLeft before F G C after))

#print axioms PentagonAdjoinedSixCell.SelectedMixedLowerBoundaryPacket
#print axioms PentagonAdjoinedSixCell.selectedMixedLowerBoundaryPacket
#print axioms PentagonAdjoinedSixCell.selectedMixedLowerBoundaryQuotients
#print axioms PentagonAdjoinedSixCell.selectedFifteenTraceCounts
#print axioms PentagonAdjoinedSixCell.selectedFifteenMixedCountsEqual
#print axioms PentagonAdjoinedSixCell.selectedFifteenMixedCoarseFineSeparation
#print axioms PentagonAdjoinedSixCell.selectedFifteenUnitReverseRoundtrip
#print axioms PentagonAdjoinedSixCell.selectedFifteenFirstAtomTag
#print axioms PentagonAdjoinedSixCell.selectedFifteenUnitRoundtrip_rawDistinct
#print axioms PentagonAdjoinedSixCell.selectedFifteenReverseRoundtrip_rawDistinct
#print axioms PentagonAdjoinedSixCell.selectedFifteenUnitRoundtrip_traceBlind
#print axioms PentagonAdjoinedSixCell.selectedFifteenReverseRoundtrip_traceBlind
#print axioms PentagonAdjoinedSixCell.SelectedLocalSixteen
#print axioms PentagonAdjoinedSixCell.selectedSixteenLeftUnitWitness
#print axioms PentagonAdjoinedSixCell.selectedSixteenRightUnitWitness
#print axioms PentagonAdjoinedSixCell.selectedSixteen_preservesTrace
#print axioms PentagonAdjoinedSixCell.selectedSixteenSetoid
#print axioms PentagonAdjoinedSixCell.selectedSixteenClass
#print axioms PentagonAdjoinedSixCell.selectedSixteenClass_eq_iff
#print axioms PentagonAdjoinedSixCell.selectedSixteenTraceOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedSixteenTrace_onClass
#print axioms PentagonAdjoinedSixCell.selectedSixteenLeftUnitClassEq
#print axioms PentagonAdjoinedSixCell.selectedSixteenRightUnitClassEq
#print axioms PentagonAdjoinedSixCell.selectedSixteen_noFirstTagDescent
#print axioms PentagonAdjoinedSixCell.selectedSixteenMixedOrderTraceObstruction
#print axioms PentagonAdjoinedSixCell.selectedSixteenMixedOrderCountAgreement
#print axioms PentagonAdjoinedSixCell.selectedSixteen_noRawEqualityInterpreter

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
