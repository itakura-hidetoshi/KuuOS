import KUOS.Architecture.QiWuxingGK5CHP77MixedContextNaturalityCubeV5_30

/-!
Qi v5.31: independently SELECTED context-closed fifteenth comparison,
faithful retention of v5.30 raw 15D proofs, actual original seventh-
cell left/right transport, and a local fourteenth-quotient descent gate.

The old 15D mixed-unit critical comparison is not altered.  We give
a new selected 15D grammar with precisely two additional 7D context
transport constructors (plus strict/reverse/chain), each requiring
the actual original sixth-boundary matching packet.  No equality
between the underlying fourteenth proof trees is assumed.

For any compatible true exterior seventh left/right contexts, the two
possible 15D transport orders are constructed independently.  Their
14D boundaries are generally different proof-relevant Type indices,
so a cross-order raw Eq would be ill typed.  A finite Bool-list
observer nevertheless distinguishes their ordered witness histories:
[false,true] versus [true,false], even though the histories have the
same length.  No phantom 16D interchange is adjoined.

A setoid on ORIGINAL selected v5.30 fourteen-cell proof objects is
then induced by the independent context-closed 15D grammar.  This
gives exact quotient equality iff an actual typed selected 15D
comparison exists.  The original local 15D criticalUnit yields an
explicit equality of two raw-distinct 14D proof classes.  Any
observable that preserves all selected 15D comparisons descends,
but the old raw first-constructor tag demonstrably does NOT descend.

The new presentation retains every v5.30 raw 15D value injectively.
No old raw 14D Eq, universal 16D coherence, arbitrary extension
to incompatible boundaries, or proof-independent strictification.
F55/P77/GK5CG, all original 6D-14D source proofs, and all previous
selected presentations are untouched.  Append-only / tighten-only /
overwrite-forbidden / same-root.  No new axioms, no sorry.
-/

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uSix uObs

namespace KUOS.Architecture.WuxingPentagonUnified
namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell

variable {W : Type uSix}

/-- Independent, proof-relevant FIFTEENTH grammar with actual
original 7D contextual stability.  The old selected v5.30 proof
value is retained as an unmodified constructor argument. -/
inductive SelectedContextualFifteen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    {P Q : SelectedUnitalCompositionTwelve W l r F G} →
    {C D : SelectedMixedInterchangerThirteen W l r P Q} →
    SelectedMixedNaturalityFourteen W l r C D →
    SelectedMixedNaturalityFourteen W l r C D → Type uSix where
  | inherited {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      (T : SelectedMixedCoherenceFifteen W l r V X) :
      SelectedContextualFifteen W l r V X
  | whiskerLeft {w z : W}
      {b c d : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      (T : SelectedContextualFifteen W l r V X) :
      SelectedContextualFifteen W l r
        (.whiskerLeft before F G V)
        (.whiskerLeft before F G X)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      (T : SelectedContextualFifteen W l r V X)
      (after : SevenRewrite W l r d e) :
      SelectedContextualFifteen W l r
        (.whiskerRight F G V after)
        (.whiskerRight F G X after)
  | strict {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      (V : SelectedMixedNaturalityFourteen W l r C D) :
      SelectedContextualFifteen W l r V V
  | reverse {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      (T : SelectedContextualFifteen W l r V X) :
      SelectedContextualFifteen W l r X V
  | chain {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X Y : SelectedMixedNaturalityFourteen W l r C D}
      (T : SelectedContextualFifteen W l r V X)
      (U : SelectedContextualFifteen W l r X Y) :
      SelectedContextualFifteen W l r V Y

/-- Old FIFTEENTH evidence is retained INJECTIVELY as raw data. -/
def oldFifteenToContextual (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedMixedCoherenceFifteen W l r V X) :
    SelectedContextualFifteen W l r V X :=
  .inherited T

theorem oldFifteenToContextual_injective (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D} :
    Function.Injective
      (fun T : SelectedMixedCoherenceFifteen W l r V X =>
        oldFifteenToContextual l r T) := by
  intro T U h
  cases h
  rfl

/-- True original left context action on selected 15D witnesses. -/
theorem selectedFifteen_leftStable (l r : W) {w z : W}
    {b c d : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedContextualFifteen W l r V X) :
    Nonempty (SelectedContextualFifteen W l r
      (.whiskerLeft before F G V) (.whiskerLeft before F G X)) :=
  ⟨.whiskerLeft before F G T⟩

/-- True original right context action on selected 15D witnesses. -/
theorem selectedFifteen_rightStable (l r : W) {w z : W}
    {c d e : PentagonAdjoinedSixCell W l r w z}
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedContextualFifteen W l r V X)
    (after : SevenRewrite W l r d e) :
    Nonempty (SelectedContextualFifteen W l r
      (.whiskerRight F G V after) (.whiskerRight F G X after)) :=
  ⟨.whiskerRight F G T after⟩

/-- An actual old v5.30 selected 15D critical-unit proof is
represented without replacing either original raw 14D proof value. -/
def selectedFifteenContextualUnit (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    SelectedContextualFifteen W l r
      (selectedMixedFourteenUnitPrepend l r before F G C after)
      (selectedMixedFourteenUnitAppend l r before F G C after) :=
  .inherited (.criticalUnit before F G C after)

/-- One actual two-stage 15D loop, not a raw identity of proof trees. -/
def selectedFifteenUnitRoundtrip (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    SelectedContextualFifteen W l r
      (selectedMixedFourteenUnitPrepend l r before F G C after)
      (selectedMixedFourteenUnitPrepend l r before F G C after) :=
  .chain (selectedFifteenContextualUnit l r before F G C after)
    (.reverse (selectedFifteenContextualUnit l r before F G C after))

/-- Typed setoid on parallel FOURTEENTH proof values, generated by
actual, selected context-closed FIFTEENTH evidence. -/
def selectedContextFifteenSetoid (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    (C D : SelectedMixedInterchangerThirteen W l r P Q) :
    Setoid (SelectedMixedNaturalityFourteen W l r C D) where
  r := fun V X => Nonempty (SelectedContextualFifteen W l r V X)
  iseqv := by
    constructor
    · intro V
      exact ⟨.strict V⟩
    · intro V X h
      rcases h with ⟨T⟩
      exact ⟨.reverse T⟩
    · intro V X Y h h'
      rcases h with ⟨T⟩
      rcases h' with ⟨U⟩
      exact ⟨.chain T U⟩

def selectedContextFifteenClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    (V : SelectedMixedNaturalityFourteen W l r C D) :
    Quotient (selectedContextFifteenSetoid l r C D) :=
  Quotient.mk _ V

theorem selectedContextFifteenClass_eq_iff (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    (V X : SelectedMixedNaturalityFourteen W l r C D) :
    selectedContextFifteenClass l r V =
      selectedContextFifteenClass l r X ↔
      Nonempty (SelectedContextualFifteen W l r V X) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- An observer descends *exactly when* it is constant on the
chosen FIFTEENTH comparison relation. This is a conditional lift,
not automatic descent of arbitrary raw historical data. -/
def selectedContextFifteenQuotientLift (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {A : Type uObs}
    (obs : SelectedMixedNaturalityFourteen W l r C D → A)
    (compatible : ∀ (V X : SelectedMixedNaturalityFourteen W l r C D),
      SelectedContextualFifteen W l r V X → obs V = obs X) :
    Quotient (selectedContextFifteenSetoid l r C D) → A :=
  Quotient.lift obs (by
    intro V X h
    rcases h with ⟨T⟩
    exact compatible V X T)

theorem selectedContextFifteenQuotientLift_onClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {A : Type uObs}
    (obs : SelectedMixedNaturalityFourteen W l r C D → A)
    (compatible : ∀ (V X : SelectedMixedNaturalityFourteen W l r C D),
      SelectedContextualFifteen W l r V X → obs V = obs X)
    (V : SelectedMixedNaturalityFourteen W l r C D) :
    selectedContextFifteenQuotientLift l r obs compatible
      (selectedContextFifteenClass l r V) = obs V :=
  rfl

/-- The genuine selected 15D unit filler identifies the two
raw-distinct 14D proof TERMS only in this new 14D quotient. -/
theorem selectedContextFifteen_unitClassEq (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedContextFifteenClass l r
      (selectedMixedFourteenUnitPrepend l r before F G C after) =
    selectedContextFifteenClass l r
      (selectedMixedFourteenUnitAppend l r before F G C after) :=
  Quotient.sound ⟨selectedFifteenContextualUnit l r before F G C after⟩

/-- Source raw FOURTEENTH first-atom tags DO NOT descend to this
selected quotient: the actual local 15D unit relates tag 2 to tag 1.
This is a proved obstruction, not a missing proof or a new axiom. -/
theorem selectedContextFifteen_noFirstTagDescent (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    ¬ (∃ g : Quotient (selectedContextFifteenSetoid l r
        (selectedMixedNaturalityViaUpper l r before F G C after)
        (selectedMixedNaturalityViaLower l r before F G C after)) → Nat,
      ∀ (V : SelectedMixedNaturalityFourteen W l r
        (selectedMixedNaturalityViaUpper l r before F G C after)
        (selectedMixedNaturalityViaLower l r before F G C after)),
        g (selectedContextFifteenClass l r V) =
          selectedMixedFourteenFirstAtomTag l r V) := by
  rintro ⟨g, hg⟩
  have htag : selectedMixedFourteenFirstAtomTag l r
        (selectedMixedFourteenUnitPrepend l r before F G C after) =
      selectedMixedFourteenFirstAtomTag l r
        (selectedMixedFourteenUnitAppend l r before F G C after) := by
    calc
      _ = g (selectedContextFifteenClass l r
          (selectedMixedFourteenUnitPrepend l r before F G C after)) :=
        (hg _).symm
      _ = g (selectedContextFifteenClass l r
          (selectedMixedFourteenUnitAppend l r before F G C after)) :=
        congrArg g (selectedContextFifteen_unitClassEq l r before F G C after)
      _ = _ := hg _
  change (2 : Nat) = 1 at htag
  cases htag

/-- A raw FIFTEENTH proof-history observer, not a quotient observer.
false means an outer left action, true an outer right action.
The inherited old proof has no *new* outer context events. -/
def selectedContextFifteenTrace (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedContextualFifteen W l r V X) : List Bool :=
  match T with
  | .inherited _ => []
  | .whiskerLeft _ _ _ T => false :: selectedContextFifteenTrace l r T
  | .whiskerRight _ _ T _ => true :: selectedContextFifteenTrace l r T
  | .strict _ => []
  | .reverse T => selectedContextFifteenTrace l r T
  | .chain T U =>
      selectedContextFifteenTrace l r T ++ selectedContextFifteenTrace l r U

/-- Genuine exterior actions in the order RIGHT THEN LEFT.  Every
14D endpoint is produced from the actual old original six-fiber. -/
def selectedFifteenLeftAfterRight (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedContextualFifteen W l r V X)
    (right : SevenRewrite W l r c d) :
    SelectedContextualFifteen W l r
      (.whiskerLeft left
        (contextFrameRight l r F right)
        (contextFrameRight l r G right)
        (.whiskerRight F G V right))
      (.whiskerLeft left
        (contextFrameRight l r F right)
        (contextFrameRight l r G right)
        (.whiskerRight F G X right)) :=
  .whiskerLeft left
    (contextFrameRight l r F right)
    (contextFrameRight l r G right)
    (.whiskerRight F G T right)

/-- Genuine exterior actions in the order LEFT THEN RIGHT. Its 14D
endpoints are independently indexed; equality with the previous
raw 15D term is intentionally NOT asserted. -/
def selectedFifteenRightAfterLeft (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedContextualFifteen W l r V X)
    (right : SevenRewrite W l r c d) :
    SelectedContextualFifteen W l r
      (.whiskerRight
        (contextFrameLeft l r left F)
        (contextFrameLeft l r left G)
        (.whiskerLeft left F G V) right)
      (.whiskerRight
        (contextFrameLeft l r left F)
        (contextFrameLeft l r left G)
        (.whiskerLeft left F G X) right) :=
  .whiskerRight
    (contextFrameLeft l r left F)
    (contextFrameLeft l r left G)
    (.whiskerLeft left F G T) right

/-- A fully typed pair of mixed-context transport witnesses with
different 15D history.  The comparison is on finite raw OBSERVATIONS,
not an ill-typed equality between different proof fibers. -/
theorem selectedFifteenMixedTraceValues (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedContextualFifteen W l r V X)
    (right : SevenRewrite W l r c d) :
    selectedContextFifteenTrace l r
        (selectedFifteenLeftAfterRight l r left F G T right) =
          false :: true :: selectedContextFifteenTrace l r T ∧
    selectedContextFifteenTrace l r
        (selectedFifteenRightAfterLeft l r left F G T right) =
          true :: false :: selectedContextFifteenTrace l r T := by
  constructor <;> rfl

theorem selectedFifteenMixedTrace_obstruction (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedContextualFifteen W l r V X)
    (right : SevenRewrite W l r c d) :
    selectedContextFifteenTrace l r
        (selectedFifteenLeftAfterRight l r left F G T right) ≠
      selectedContextFifteenTrace l r
        (selectedFifteenRightAfterLeft l r left F G T right) := by
  intro h
  have ht : false :: true :: selectedContextFifteenTrace l r T =
      true :: false :: selectedContextFifteenTrace l r T := by
    calc
      _ = selectedContextFifteenTrace l r
            (selectedFifteenLeftAfterRight l r left F G T right) :=
          (selectedFifteenMixedTraceValues l r left F G T right).1.symm
      _ = selectedContextFifteenTrace l r
            (selectedFifteenRightAfterLeft l r left F G T right) := h
      _ = _ := (selectedFifteenMixedTraceValues l r left F G T right).2
  cases ht

theorem selectedFifteenMixedTrace_lengthEqual (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T : SelectedContextualFifteen W l r V X)
    (right : SevenRewrite W l r c d) :
    (selectedContextFifteenTrace l r
        (selectedFifteenLeftAfterRight l r left F G T right)).length =
      (selectedContextFifteenTrace l r
        (selectedFifteenRightAfterLeft l r left F G T right)).length := by
  change (false :: true :: selectedContextFifteenTrace l r T).length =
    (true :: false :: selectedContextFifteenTrace l r T).length
  rfl

/-- Even after freely adjoining strict/reversal/concatenation,
the FIFTEENTH comparison remains distinct from literal raw 14D Eq. -/
theorem selectedFifteen_noRawEqualityInterpreter (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    ¬ (∀
      (V X : SelectedMixedNaturalityFourteen W l r
        (selectedMixedNaturalityViaUpper l r before F G C after)
        (selectedMixedNaturalityViaLower l r before F G C after)),
      SelectedContextualFifteen W l r V X → V = X) := by
  intro interpret
  exact selectedMixedFourteenUnit_rawDistinct l r before F G C after
    (interpret _ _ (selectedFifteenContextualUnit l r before F G C after))

#print axioms PentagonAdjoinedSixCell.SelectedContextualFifteen
#print axioms PentagonAdjoinedSixCell.oldFifteenToContextual
#print axioms PentagonAdjoinedSixCell.oldFifteenToContextual_injective
#print axioms PentagonAdjoinedSixCell.selectedFifteen_leftStable
#print axioms PentagonAdjoinedSixCell.selectedFifteen_rightStable
#print axioms PentagonAdjoinedSixCell.selectedFifteenContextualUnit
#print axioms PentagonAdjoinedSixCell.selectedFifteenUnitRoundtrip
#print axioms PentagonAdjoinedSixCell.selectedContextFifteenSetoid
#print axioms PentagonAdjoinedSixCell.selectedContextFifteenClass
#print axioms PentagonAdjoinedSixCell.selectedContextFifteenClass_eq_iff
#print axioms PentagonAdjoinedSixCell.selectedContextFifteenQuotientLift
#print axioms PentagonAdjoinedSixCell.selectedContextFifteenQuotientLift_onClass
#print axioms PentagonAdjoinedSixCell.selectedContextFifteen_unitClassEq
#print axioms PentagonAdjoinedSixCell.selectedContextFifteen_noFirstTagDescent
#print axioms PentagonAdjoinedSixCell.selectedContextFifteenTrace
#print axioms PentagonAdjoinedSixCell.selectedFifteenLeftAfterRight
#print axioms PentagonAdjoinedSixCell.selectedFifteenRightAfterLeft
#print axioms PentagonAdjoinedSixCell.selectedFifteenMixedTraceValues
#print axioms PentagonAdjoinedSixCell.selectedFifteenMixedTrace_obstruction
#print axioms PentagonAdjoinedSixCell.selectedFifteenMixedTrace_lengthEqual
#print axioms PentagonAdjoinedSixCell.selectedFifteen_noRawEqualityInterpreter

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
