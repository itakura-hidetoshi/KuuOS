import KUOS.Architecture.QiWuxingGK5CHP77MixedBoundarySixteenV5_32

/-!
Qi v5.33: typed original lower 12D/selected 13D/14D mixed-boundary
packet, new selected 16D seventh-context closure, preserved ordered
15D history, and exact-fiber local selected 17D unit coherence.

The ORIGINAL v5.18 doubleWhisker gives the two actual 12D source
and target bridges. At actual original seventh-cell contexts, the
previously proved selected 13D interchangers and selected 14D
naturality square form an independently packaged lower-dimensional
compatibility certificate. This does NOT automatically identify the
different 14D dependent endpoints of v5.31's two exterior 15D
context orders: an unconditional mixed 16D comparison is NOT added.

An independent selected 16D grammar faithfully embeds every prior
v5.32 SelectedLocalSixteen proof value, and extends it by genuinely
typed original left/right seventh-cell context whiskering plus
strict/reverse/chain. The old v5.31 ordered List Bool history
is conserved by every new 16D constructor. We construct its
contextual 16D quotient and an exact Quotient.lift. The original
15D first-constructor tag still CANNOT descend: an inherited real
16D loop comparison sends raw first tags 0 versus 3.

Both exterior 16D context orders are independently constructed, with
fully typed old 14D/15D boundary data. Their ordered 16D proof
histories differ as finite Bool lists ([false,true] vs [true,false]),
even though event lengths match. Because the endpoints depend on
different raw whiskering order, we compare observations only;
no heterogeneously typed proof Eq or generic 17D exchange is claimed.

Finally, two explicit old local 16D unit comparisons are pasted with
16D strict witnesses on opposite ends. These are raw-distinct 16D
histories at identical original 15D endpoints. An independent
selected 17D grammar adds exactly TWO local unit-pasting critical
families, plus strict/reverse/chain; previous 16D comparisons are
not forcibly identified as raw equal. This is a selected local
coherence, not global Gray/tetracategorical coherence.

Append-only, tighten-only, overwrite-forbidden, same-root.
Original F55/P77/GK5CG, original 6D-14D, and every previous selected
12D-16D proof type remain unchanged. No new axioms or sorry.
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

/-- Full ACTUAL mixed lower-dimensional certificate at original
seventh-cell source, including two genuine 12D boundary bridges,
two genuine selected 13D interchangers and the chosen selected 14D
naturality square. The package contains NO 16D exchange. -/
structure SelectedMixedLowerHigherPacket (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (right : SevenRewrite W l r c d) : Type uSix where
  boundaries : SelectedMixedLowerBoundaryPacket l r left F G right
  atP : SelectedMixedInterchangerThirteen W l r
    (selectedMixedUpperRoute l r left F G P right)
    (selectedMixedLowerRoute l r left F G P right)
  atQ : SelectedMixedInterchangerThirteen W l r
    (selectedMixedUpperRoute l r left F G Q right)
    (selectedMixedLowerRoute l r left F G Q right)
  naturality : SelectedMixedNaturalityFourteen W l r
    (selectedMixedNaturalityViaUpper l r left F G C right)
    (selectedMixedNaturalityViaLower l r left F G C right)

/-- Assemble all LOWER comparison witnesses from actual v5.18,
v5.30 and v5.32 constructors; no new compatibility axiom. -/
def selectedMixedLowerHigherPacket (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (right : SevenRewrite W l r c d) :
    SelectedMixedLowerHigherPacket l r left F G C right :=
  ⟨selectedMixedLowerBoundaryPacket l r left F G right,
    .mixed left F G P right,
    .mixed left F G Q right,
    .criticalMixed left F G C right⟩

/-- The actual 13D/14D packet is inhabited and the two selected
13D naturality paths it compares remain RAW distinct. -/
theorem selectedMixedLowerHigherPacket_witness (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (right : SevenRewrite W l r c d) :
    Nonempty (SelectedMixedLowerHigherPacket l r left F G C right) ∧
    selectedMixedNaturalityViaUpper l r left F G C right ≠
      selectedMixedNaturalityViaLower l r left F G C right :=
  ⟨⟨selectedMixedLowerHigherPacket l r left F G C right⟩,
    selectedMixedNaturality_rawDistinct l r left F G C right⟩

/-- A chosen selected 16D contextual presentation. It embeds every
v5.32 original selected local 16D term and separately transports
16D witnesses through the TRUE old seventh-cell whiskerings. -/
inductive SelectedContextualSixteen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    {P Q : SelectedUnitalCompositionTwelve W l r F G} →
    {C D : SelectedMixedInterchangerThirteen W l r P Q} →
    {V X : SelectedMixedNaturalityFourteen W l r C D} →
    SelectedContextualFifteen W l r V X →
    SelectedContextualFifteen W l r V X → Type uSix where
  | inherited {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      (H : SelectedLocalSixteen W l r T U) :
      SelectedContextualSixteen W l r T U
  | whiskerLeft {w z : W}
      {b c d : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      (H : SelectedContextualSixteen W l r T U) :
      SelectedContextualSixteen W l r
        (.whiskerLeft before F G T)
        (.whiskerLeft before F G U)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      (H : SelectedContextualSixteen W l r T U)
      (after : SevenRewrite W l r d e) :
      SelectedContextualSixteen W l r
        (.whiskerRight F G T after)
        (.whiskerRight F G U after)
  | strict {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      (T : SelectedContextualFifteen W l r V X) :
      SelectedContextualSixteen W l r T T
  | reverse {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      (H : SelectedContextualSixteen W l r T U) :
      SelectedContextualSixteen W l r U T
  | chain {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U Z : SelectedContextualFifteen W l r V X}
      (H : SelectedContextualSixteen W l r T U)
      (K : SelectedContextualSixteen W l r U Z) :
      SelectedContextualSixteen W l r T Z

/-- Raw witness histories are stored, not mapped to raw equality. -/
def oldSixteenToContextual (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedLocalSixteen W l r T U) :
    SelectedContextualSixteen W l r T U :=
  .inherited H

theorem oldSixteenToContextual_injective (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X} :
    Function.Injective (fun H : SelectedLocalSixteen W l r T U =>
      oldSixteenToContextual l r H) := by
  intro H K h
  cases h
  rfl

theorem selectedContextualSixteen_leftStable (l r : W) {w z : W}
    {b c d : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U) :
    Nonempty (SelectedContextualSixteen W l r
      (.whiskerLeft before F G T) (.whiskerLeft before F G U)) :=
  ⟨.whiskerLeft before F G H⟩

theorem selectedContextualSixteen_rightStable (l r : W) {w z : W}
    {c d e : PentagonAdjoinedSixCell W l r w z}
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U)
    (after : SevenRewrite W l r d e) :
    Nonempty (SelectedContextualSixteen W l r
      (.whiskerRight F G T after) (.whiskerRight F G U after)) :=
  ⟨.whiskerRight F G H after⟩

/-- ALL six constructors preserve the PREVIOUS actual ordered
fifteenth-context Bool list across parallel 15D proof terms. -/
theorem selectedContextualSixteen_preservesTrace (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U) :
    selectedContextFifteenTrace l r T = selectedContextFifteenTrace l r U := by
  induction H with
  | inherited H => exact selectedSixteen_preservesTrace l r H
  | whiskerLeft before F G H ih =>
      exact congrArg (List.cons false) ih
  | whiskerRight F G H after ih =>
      exact congrArg (List.cons true) ih
  | strict T => rfl
  | reverse H ih => exact ih.symm
  | chain H K ih ih' => exact ih.trans ih'

/-- The new contextual 16D quotient is formed separately for
EXACT matching original 14D and 15D proof-dependent boundaries. -/
def selectedContextSixteenSetoid (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    (V X : SelectedMixedNaturalityFourteen W l r C D) :
    Setoid (SelectedContextualFifteen W l r V X) where
  r := fun T U => Nonempty (SelectedContextualSixteen W l r T U)
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

def selectedContextSixteenClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedContextualFifteen W l r V X) :
    Quotient (selectedContextSixteenSetoid l r V X) :=
  Quotient.mk _ T

theorem selectedContextSixteenClass_eq_iff (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T U : SelectedContextualFifteen W l r V X) :
    selectedContextSixteenClass l r T = selectedContextSixteenClass l r U ↔
      Nonempty (SelectedContextualSixteen W l r T U) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

def selectedContextSixteenTraceOnQuotient (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    (V X : SelectedMixedNaturalityFourteen W l r C D) :
    Quotient (selectedContextSixteenSetoid l r V X) → List Bool :=
  Quotient.lift (selectedContextFifteenTrace l r) (by
    intro T U h
    rcases h with ⟨H⟩
    exact selectedContextualSixteen_preservesTrace l r H)

theorem selectedContextSixteenTrace_onClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedContextualFifteen W l r V X) :
    selectedContextSixteenTraceOnQuotient l r V X
        (selectedContextSixteenClass l r T) =
      selectedContextFifteenTrace l r T :=
  rfl

/-- The genuine old local 16D unit comparison persists under
the new contextual quotient, while the underlying proof values
remain raw distinct. -/
theorem selectedContextSixteen_leftUnitClassEq (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedContextSixteenClass l r
        (selectedFifteenUnitRoundtrip l r before F G C after) =
      selectedContextSixteenClass l r
        (SelectedContextualFifteen.strict
          (selectedMixedFourteenUnitPrepend l r before F G C after)) :=
  Quotient.sound ⟨.inherited (.unitRoundtripLeft before F G C after)⟩

theorem selectedContextSixteen_noFirstTagDescent (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    ¬ (∃ g : Quotient (selectedContextSixteenSetoid l r
        (selectedMixedFourteenUnitPrepend l r before F G C after)
        (selectedMixedFourteenUnitPrepend l r before F G C after)) → Nat,
      ∀ (T : SelectedContextualFifteen W l r
        (selectedMixedFourteenUnitPrepend l r before F G C after)
        (selectedMixedFourteenUnitPrepend l r before F G C after)),
        g (selectedContextSixteenClass l r T) =
          selectedFifteenFirstAtomTag l r T) := by
  rintro ⟨g, hg⟩
  have ht : selectedFifteenFirstAtomTag l r
        (selectedFifteenUnitRoundtrip l r before F G C after) =
      selectedFifteenFirstAtomTag l r
        (SelectedContextualFifteen.strict
          (selectedMixedFourteenUnitPrepend l r before F G C after)) := by
    calc
      _ = g (selectedContextSixteenClass l r
          (selectedFifteenUnitRoundtrip l r before F G C after)) :=
        (hg _).symm
      _ = g (selectedContextSixteenClass l r
          (SelectedContextualFifteen.strict
            (selectedMixedFourteenUnitPrepend l r before F G C after))) :=
        congrArg g (selectedContextSixteen_leftUnitClassEq l r before F G C after)
      _ = _ := hg _
  change (0 : Nat) = 3 at ht
  cases ht

/-- Two genuine 16D context transports with distinct, dependent,
typed 15D source/target proof histories. -/
def selectedSixteenLeftAfterRight (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U)
    (right : SevenRewrite W l r c d) :
    SelectedContextualSixteen W l r
      (.whiskerLeft left
        (contextFrameRight l r F right)
        (contextFrameRight l r G right)
        (.whiskerRight F G T right))
      (.whiskerLeft left
        (contextFrameRight l r F right)
        (contextFrameRight l r G right)
        (.whiskerRight F G U right)) :=
  .whiskerLeft left
    (contextFrameRight l r F right)
    (contextFrameRight l r G right)
    (.whiskerRight F G H right)

def selectedSixteenRightAfterLeft (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U)
    (right : SevenRewrite W l r c d) :
    SelectedContextualSixteen W l r
      (.whiskerRight
        (contextFrameLeft l r left F)
        (contextFrameLeft l r left G)
        (.whiskerLeft left F G T) right)
      (.whiskerRight
        (contextFrameLeft l r left F)
        (contextFrameLeft l r left G)
        (.whiskerLeft left F G U) right) :=
  .whiskerRight
    (contextFrameLeft l r left F)
    (contextFrameLeft l r left G)
    (.whiskerLeft left F G H) right

/-- Raw 16D ordered context history, NOT a quotient invariant.
The inherited local 16D proof has no NEW exterior event. -/
def selectedContextSixteenTrace (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U) : List Bool :=
  match H with
  | .inherited _ => []
  | .whiskerLeft _ _ _ H => false :: selectedContextSixteenTrace l r H
  | .whiskerRight _ _ H _ => true :: selectedContextSixteenTrace l r H
  | .strict _ => []
  | .reverse H => selectedContextSixteenTrace l r H
  | .chain H K =>
      selectedContextSixteenTrace l r H ++ selectedContextSixteenTrace l r K

theorem selectedSixteenMixedTraceValues (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U)
    (right : SevenRewrite W l r c d) :
    selectedContextSixteenTrace l r
        (selectedSixteenLeftAfterRight l r left F G H right) =
          false :: true :: selectedContextSixteenTrace l r H ∧
    selectedContextSixteenTrace l r
        (selectedSixteenRightAfterLeft l r left F G H right) =
          true :: false :: selectedContextSixteenTrace l r H := by
  constructor <;> rfl

theorem selectedSixteenMixedTrace_obstruction (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U)
    (right : SevenRewrite W l r c d) :
    selectedContextSixteenTrace l r
        (selectedSixteenLeftAfterRight l r left F G H right) ≠
      selectedContextSixteenTrace l r
        (selectedSixteenRightAfterLeft l r left F G H right) := by
  intro h
  have ht : false :: true :: selectedContextSixteenTrace l r H =
      true :: false :: selectedContextSixteenTrace l r H := by
    calc
      _ = selectedContextSixteenTrace l r
            (selectedSixteenLeftAfterRight l r left F G H right) :=
          (selectedSixteenMixedTraceValues l r left F G H right).1.symm
      _ = selectedContextSixteenTrace l r
            (selectedSixteenRightAfterLeft l r left F G H right) := h
      _ = _ := (selectedSixteenMixedTraceValues l r left F G H right).2
  cases ht

theorem selectedSixteenMixedTrace_lengthEqual (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U)
    (right : SevenRewrite W l r c d) :
    (selectedContextSixteenTrace l r
      (selectedSixteenLeftAfterRight l r left F G H right)).length =
      (selectedContextSixteenTrace l r
        (selectedSixteenRightAfterLeft l r left F G H right)).length := by
  change (false :: true :: selectedContextSixteenTrace l r H).length =
    (true :: false :: selectedContextSixteenTrace l r H).length
  rfl

/-- Finite first-atom observation avoiding illegal dependent
elimination of original seventh-cell proof indices. -/
def selectedContextSixteenFirstAtomTag (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U) : Nat :=
  match H with
  | .inherited _ => 0
  | .whiskerLeft _ _ _ _ => 1
  | .whiskerRight _ _ _ _ => 2
  | .strict _ => 3
  | .reverse _ => 4
  | .chain H _ => selectedContextSixteenFirstAtomTag l r H

/-- Actual local 16D unit critical comparison preceded by an exact
16D identity, retaining both original 15D proof terms. -/
def selectedSixteenUnitPrependLeft (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    SelectedContextualSixteen W l r
      (selectedFifteenUnitRoundtrip l r before F G C after)
      (SelectedContextualFifteen.strict
        (selectedMixedFourteenUnitPrepend l r before F G C after)) :=
  .chain (.strict (selectedFifteenUnitRoundtrip l r before F G C after))
    (.inherited (.unitRoundtripLeft before F G C after))

def selectedSixteenUnitAppendLeft (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    SelectedContextualSixteen W l r
      (selectedFifteenUnitRoundtrip l r before F G C after)
      (SelectedContextualFifteen.strict
        (selectedMixedFourteenUnitPrepend l r before F G C after)) :=
  .chain (.inherited (.unitRoundtripLeft before F G C after))
    (.strict (SelectedContextualFifteen.strict
      (selectedMixedFourteenUnitPrepend l r before F G C after)))

def selectedSixteenUnitPrependRight (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    SelectedContextualSixteen W l r
      (selectedFifteenUnitReverseRoundtrip l r before F G C after)
      (SelectedContextualFifteen.strict
        (selectedMixedFourteenUnitAppend l r before F G C after)) :=
  .chain (.strict (selectedFifteenUnitReverseRoundtrip l r before F G C after))
    (.inherited (.unitRoundtripRight before F G C after))

def selectedSixteenUnitAppendRight (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    SelectedContextualSixteen W l r
      (selectedFifteenUnitReverseRoundtrip l r before F G C after)
      (SelectedContextualFifteen.strict
        (selectedMixedFourteenUnitAppend l r before F G C after)) :=
  .chain (.inherited (.unitRoundtripRight before F G C after))
    (.strict (SelectedContextualFifteen.strict
      (selectedMixedFourteenUnitAppend l r before F G C after)))

theorem selectedSixteenUnitLeft_rawDistinct (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedSixteenUnitPrependLeft l r before F G C after ≠
      selectedSixteenUnitAppendLeft l r before F G C after := by
  intro h
  have ht := congrArg (selectedContextSixteenFirstAtomTag l r) h
  change (3 : Nat) = 0 at ht
  cases ht

theorem selectedSixteenUnitRight_rawDistinct (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedSixteenUnitPrependRight l r before F G C after ≠
      selectedSixteenUnitAppendRight l r before F G C after := by
  intro h
  have ht := congrArg (selectedContextSixteenFirstAtomTag l r) h
  change (3 : Nat) = 0 at ht
  cases ht

/-- The next selected SEVENTEENTH comparison adds just two genuine
local unit-pasting critical pairs, not a global mixed interchange. -/
inductive SelectedLocalSeventeen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    {P Q : SelectedUnitalCompositionTwelve W l r F G} →
    {C D : SelectedMixedInterchangerThirteen W l r P Q} →
    {V X : SelectedMixedNaturalityFourteen W l r C D} →
    {T U : SelectedContextualFifteen W l r V X} →
    SelectedContextualSixteen W l r T U →
    SelectedContextualSixteen W l r T U → Type uSix where
  | strict {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      (H : SelectedContextualSixteen W l r T U) :
      SelectedLocalSeventeen W l r H H
  | unitLeft {w z : W}
      {b c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      (C : SelectedContextualThirteen W l r P Q)
      (after : SevenRewrite W l r d e) :
      SelectedLocalSeventeen W l r
        (selectedSixteenUnitPrependLeft l r before F G C after)
        (selectedSixteenUnitAppendLeft l r before F G C after)
  | unitRight {w z : W}
      {b c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      (C : SelectedContextualThirteen W l r P Q)
      (after : SevenRewrite W l r d e) :
      SelectedLocalSeventeen W l r
        (selectedSixteenUnitPrependRight l r before F G C after)
        (selectedSixteenUnitAppendRight l r before F G C after)
  | reverse {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      (J : SelectedLocalSeventeen W l r H K) :
      SelectedLocalSeventeen W l r K H
  | chain {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K M : SelectedContextualSixteen W l r T U}
      (J : SelectedLocalSeventeen W l r H K)
      (N : SelectedLocalSeventeen W l r K M) :
      SelectedLocalSeventeen W l r H M

theorem selectedLocalSeventeen_leftWitness (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    Nonempty (SelectedLocalSeventeen W l r
      (selectedSixteenUnitPrependLeft l r before F G C after)
      (selectedSixteenUnitAppendLeft l r before F G C after)) ∧
    selectedSixteenUnitPrependLeft l r before F G C after ≠
      selectedSixteenUnitAppendLeft l r before F G C after :=
  ⟨⟨.unitLeft before F G C after⟩,
    selectedSixteenUnitLeft_rawDistinct l r before F G C after⟩

theorem selectedLocalSeventeen_rightWitness (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    Nonempty (SelectedLocalSeventeen W l r
      (selectedSixteenUnitPrependRight l r before F G C after)
      (selectedSixteenUnitAppendRight l r before F G C after)) ∧
    selectedSixteenUnitPrependRight l r before F G C after ≠
      selectedSixteenUnitAppendRight l r before F G C after :=
  ⟨⟨.unitRight before F G C after⟩,
    selectedSixteenUnitRight_rawDistinct l r before F G C after⟩

theorem selectedLocalSeventeen_noRawEqualityInterpreter (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    ¬ (∀
      (H K : SelectedContextualSixteen W l r
        (selectedFifteenUnitRoundtrip l r before F G C after)
        (SelectedContextualFifteen.strict
          (selectedMixedFourteenUnitPrepend l r before F G C after))),
      SelectedLocalSeventeen W l r H K → H = K) := by
  intro interpret
  exact selectedSixteenUnitLeft_rawDistinct l r before F G C after
    (interpret _ _ (.unitLeft before F G C after))

#print axioms PentagonAdjoinedSixCell.SelectedMixedLowerHigherPacket
#print axioms PentagonAdjoinedSixCell.selectedMixedLowerHigherPacket
#print axioms PentagonAdjoinedSixCell.selectedMixedLowerHigherPacket_witness
#print axioms PentagonAdjoinedSixCell.SelectedContextualSixteen
#print axioms PentagonAdjoinedSixCell.oldSixteenToContextual
#print axioms PentagonAdjoinedSixCell.oldSixteenToContextual_injective
#print axioms PentagonAdjoinedSixCell.selectedContextualSixteen_leftStable
#print axioms PentagonAdjoinedSixCell.selectedContextualSixteen_rightStable
#print axioms PentagonAdjoinedSixCell.selectedContextualSixteen_preservesTrace
#print axioms PentagonAdjoinedSixCell.selectedContextSixteenSetoid
#print axioms PentagonAdjoinedSixCell.selectedContextSixteenClass
#print axioms PentagonAdjoinedSixCell.selectedContextSixteenClass_eq_iff
#print axioms PentagonAdjoinedSixCell.selectedContextSixteenTraceOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedContextSixteenTrace_onClass
#print axioms PentagonAdjoinedSixCell.selectedContextSixteen_leftUnitClassEq
#print axioms PentagonAdjoinedSixCell.selectedContextSixteen_noFirstTagDescent
#print axioms PentagonAdjoinedSixCell.selectedSixteenLeftAfterRight
#print axioms PentagonAdjoinedSixCell.selectedSixteenRightAfterLeft
#print axioms PentagonAdjoinedSixCell.selectedContextSixteenTrace
#print axioms PentagonAdjoinedSixCell.selectedSixteenMixedTraceValues
#print axioms PentagonAdjoinedSixCell.selectedSixteenMixedTrace_obstruction
#print axioms PentagonAdjoinedSixCell.selectedSixteenMixedTrace_lengthEqual
#print axioms PentagonAdjoinedSixCell.selectedContextSixteenFirstAtomTag
#print axioms PentagonAdjoinedSixCell.selectedSixteenUnitPrependLeft
#print axioms PentagonAdjoinedSixCell.selectedSixteenUnitAppendLeft
#print axioms PentagonAdjoinedSixCell.selectedSixteenUnitPrependRight
#print axioms PentagonAdjoinedSixCell.selectedSixteenUnitAppendRight
#print axioms PentagonAdjoinedSixCell.selectedSixteenUnitLeft_rawDistinct
#print axioms PentagonAdjoinedSixCell.selectedSixteenUnitRight_rawDistinct
#print axioms PentagonAdjoinedSixCell.SelectedLocalSeventeen
#print axioms PentagonAdjoinedSixCell.selectedLocalSeventeen_leftWitness
#print axioms PentagonAdjoinedSixCell.selectedLocalSeventeen_rightWitness
#print axioms PentagonAdjoinedSixCell.selectedLocalSeventeen_noRawEqualityInterpreter

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
