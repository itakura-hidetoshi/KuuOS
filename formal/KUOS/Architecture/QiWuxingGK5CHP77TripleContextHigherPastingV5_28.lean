import KUOS.Architecture.QiWuxingGK5CHP77UnitalCompositionCompletionV5_27

/-!
Qi v5.28: actual triple original 7D context composition, typed
pasting at v5.27 selected 12D, and explicitly selected 13D/14D
higher coherence.

No new 12D comparison constructor is assumed. The two genuinely
different triple reductions have distinct original seventh-cell
parenthesizations, and thus initially DIFFERENT raw eleventh
endpoints. A typed 12D rebracketing bridge is derived by reversing
one REAL 12D reduction and chaining with the other. No raw equality
or automatic 7D associativity is claimed.

The resulting two parallel 12D paths are raw-distinct. An independent
13D presentation adds ONE local coherence family for each of left
and right triple context (plus type-preserving inclusion of actual
v5.23 original 13D comparisons). A separate, explicitly CHOSEN 14D
presentation compares two unit-pasted versions of these 13D fillers
and includes existing v5.23 selected 14D proof values as data.

Everything is conditional on genuinely composable original 7D
contexts and an actual original 7D–11D witness packet. Old F55/P77/
GK5CG, original 6D–14D and selected v5.22–v5.27 presentations
are unchanged. Distinguish proof terms, their quotient equalities,
and authority boundaries. No global tricategorical coherence or
higher strictification is inferred.
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

/-- The old 12D comparison term is embedded through BOTH actual
retained proof constructors, v5.25 then v5.27. -/
def originalFramedTwelveToSelected (l r : W)
    {F G : FramedEleven W l r}
    (T : FramedDoubleWhiskerTwelveCell W l r F G) :
    SelectedUnitalCompositionTwelve W l r F G :=
  .previous (.previous T)

theorem originalFramedTwelveToSelected_injective (l r : W)
    {F G : FramedEleven W l r} :
    Function.Injective (fun T : FramedDoubleWhiskerTwelveCell W l r F G =>
      originalFramedTwelveToSelected l r T) := by
  intro T U h
  cases h
  rfl

/-- A *raw proof-syntax* observer: follow the first branch of
twelfth path composition to its first atomic constructor. The
result is independent of all original dependent endpoints, so
congrArg avoids illegal dependent elimination of original 7D indices.
This does NOT descend to the selected twelfth quotient. -/
def selectedTwelfthFirstAtomTag (l r : W)
    {F G : FramedEleven W l r}
    (T : SelectedUnitalCompositionTwelve W l r F G) : Nat :=
  match T with
  | .strict _ => 0
  | .previous _ => 1
  | .reverse _ => 2
  | .chain P _ => selectedTwelfthFirstAtomTag l r P
  | .whiskerLeft _ _ _ _ => 4
  | .whiskerRight _ _ _ _ => 5
  | .unitLeft _ => 6
  | .unitRight _ => 7
  | .compLeft _ _ _ => 8
  | .compRight _ _ _ => 9

section LeftTriple

variable (l r : W) {w z : W}
variable {a b c d e : PentagonAdjoinedSixCell W l r w z}
variable (u : SevenRewrite W l r a b)
variable (v : SevenRewrite W l r b c)
variable (t : SevenRewrite W l r c d)
variable (F : ContextFrameEleven W l r d e)

/-- Every level is an actual original left whisker, in original
typed six-cell boundaries, with no Eq between distinct fibers. -/
def selectedLeftTripleSource : FramedEleven W l r :=
  contextFramePack l r
    (contextFrameLeft l r u
      (contextFrameLeft l r v (contextFrameLeft l r t F)))

def selectedLeftTripleLeftTarget : FramedEleven W l r :=
  contextFramePack l r
    (contextFrameLeft l r (.trans (.trans u v) t) F)

def selectedLeftTripleRightTarget : FramedEleven W l r :=
  contextFramePack l r
    (contextFrameLeft l r (.trans u (.trans v t)) F)

/-- Reduce the inner pair first. This retains BOTH original
compLeft proof terms and transports the first under the true u context. -/
def selectedLeftTripleInnerPasting :
    SelectedUnitalCompositionTwelve W l r
      (selectedLeftTripleSource l r u v t F)
      (selectedLeftTripleRightTarget l r u v t F) :=
  .chain
    (.whiskerLeft u
      (contextFrameLeft l r v (contextFrameLeft l r t F))
      (contextFrameLeft l r (.trans v t) F)
      (.compLeft v t F))
    (.compLeft u (.trans v t) F)

/-- Reduce the outer pair first; this ends at the OTHER
parenthesized original seventh context. -/
def selectedLeftTripleOuterPasting :
    SelectedUnitalCompositionTwelve W l r
      (selectedLeftTripleSource l r u v t F)
      (selectedLeftTripleLeftTarget l r u v t F) :=
  .chain
    (.compLeft u v (contextFrameLeft l r t F))
    (.compLeft (.trans u v) t F)

/-- An ACTUAL, endpoint-compatible 12D reassociation route, derived
from the two preceding witnesses, not from a newly asserted 7D Eq. -/
def selectedLeftTripleRebracket :
    SelectedUnitalCompositionTwelve W l r
      (selectedLeftTripleLeftTarget l r u v t F)
      (selectedLeftTripleRightTarget l r u v t F) :=
  .chain (.reverse (selectedLeftTripleOuterPasting l r u v t F))
    (selectedLeftTripleInnerPasting l r u v t F)

/-- A second parallel route, explicitly exposing its reassociation
detour and the full non-cancelled original 12D proof history. -/
def selectedLeftTripleDetour :
    SelectedUnitalCompositionTwelve W l r
      (selectedLeftTripleSource l r u v t F)
      (selectedLeftTripleRightTarget l r u v t F) :=
  .chain (selectedLeftTripleOuterPasting l r u v t F)
    (selectedLeftTripleRebracket l r u v t F)

/-- Even though the two reductions agree at the new selected
QUOTIENT, their actual 12D syntax is not definitionally equal. -/
theorem selectedLeftTriple_rawDistinct :
    selectedLeftTripleInnerPasting l r u v t F ≠
      selectedLeftTripleDetour l r u v t F := by
  intro h
  have ht := congrArg (selectedTwelfthFirstAtomTag l r) h
  change (4 : Nat) = 8 at ht
  cases ht

theorem selectedLeftTriple_twoBracketClasses :
    selectedUnitalClass l r
        (selectedLeftTripleLeftTarget l r u v t F) =
      selectedUnitalClass l r
        (selectedLeftTripleRightTarget l r u v t F) :=
  Quotient.sound ⟨selectedLeftTripleRebracket l r u v t F⟩

end LeftTriple

section RightTriple

variable (l r : W) {w z : W}
variable {a b c d e : PentagonAdjoinedSixCell W l r w z}
variable (u : SevenRewrite W l r b c)
variable (v : SevenRewrite W l r c d)
variable (t : SevenRewrite W l r d e)
variable (F : ContextFrameEleven W l r a b)

/-- Right contexts are applied from the original packet outwards. -/
def selectedRightTripleSource : FramedEleven W l r :=
  contextFramePack l r
    (contextFrameRight l r
      (contextFrameRight l r (contextFrameRight l r F u) v) t)

def selectedRightTripleLeftTarget : FramedEleven W l r :=
  contextFramePack l r
    (contextFrameRight l r F (.trans (.trans u v) t))

def selectedRightTripleRightTarget : FramedEleven W l r :=
  contextFramePack l r
    (contextFrameRight l r F (.trans u (.trans v t)))

/-- Reduce v,t in the outermost contexts first, then u,(v.t). -/
def selectedRightTripleOuterPasting :
    SelectedUnitalCompositionTwelve W l r
      (selectedRightTripleSource l r u v t F)
      (selectedRightTripleRightTarget l r u v t F) :=
  .chain
    (.compRight v t (contextFrameRight l r F u))
    (.compRight u (.trans v t) F)

/-- Reduce u,v first, transporting this genuine comparison through
the last original right whisker, then compose (u.v),t. -/
def selectedRightTripleInnerPasting :
    SelectedUnitalCompositionTwelve W l r
      (selectedRightTripleSource l r u v t F)
      (selectedRightTripleLeftTarget l r u v t F) :=
  .chain
    (.whiskerRight
      (contextFrameRight l r (contextFrameRight l r F u) v)
      (contextFrameRight l r F (.trans u v))
      (.compRight u v F) t)
    (.compRight (.trans u v) t F)

def selectedRightTripleRebracket :
    SelectedUnitalCompositionTwelve W l r
      (selectedRightTripleLeftTarget l r u v t F)
      (selectedRightTripleRightTarget l r u v t F) :=
  .chain (.reverse (selectedRightTripleInnerPasting l r u v t F))
    (selectedRightTripleOuterPasting l r u v t F)

def selectedRightTripleDetour :
    SelectedUnitalCompositionTwelve W l r
      (selectedRightTripleSource l r u v t F)
      (selectedRightTripleRightTarget l r u v t F) :=
  .chain (selectedRightTripleInnerPasting l r u v t F)
    (selectedRightTripleRebracket l r u v t F)

theorem selectedRightTriple_rawDistinct :
    selectedRightTripleOuterPasting l r u v t F ≠
      selectedRightTripleDetour l r u v t F := by
  intro h
  have ht := congrArg (selectedTwelfthFirstAtomTag l r) h
  change (9 : Nat) = 5 at ht
  cases ht

theorem selectedRightTriple_twoBracketClasses :
    selectedUnitalClass l r
        (selectedRightTripleLeftTarget l r u v t F) =
      selectedUnitalClass l r
        (selectedRightTripleRightTarget l r u v t F) :=
  Quotient.sound ⟨selectedRightTripleRebracket l r u v t F⟩

end RightTriple

/-- Independent, typed THIRTEENTH presentation over ACTUAL selected
v5.27 twelfth proof terms. The new primitive families correspond to
the two authentic triple-context pasting critical pairs. Existing
v5.23 thirteenth proof values are included without changing them. -/
inductive SelectedTriplePastingThirteen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    SelectedUnitalCompositionTwelve W l r F G →
    SelectedUnitalCompositionTwelve W l r F G → Type uSix where
  | strict {F G : FramedEleven W l r}
      (P : SelectedUnitalCompositionTwelve W l r F G) :
      SelectedTriplePastingThirteen W l r P P
  | inheritedOld {F G : FramedEleven W l r}
      {P Q : FramedDoubleWhiskerTwelveCell W l r F G}
      (C : CompositionalWhiskerThirteen W l r P Q) :
      SelectedTriplePastingThirteen W l r
        (originalFramedTwelveToSelected l r P)
        (originalFramedTwelveToSelected l r Q)
  | tripleLeft {w z : W}
      {a b c d e : PentagonAdjoinedSixCell W l r w z}
      (u : SevenRewrite W l r a b)
      (v : SevenRewrite W l r b c)
      (t : SevenRewrite W l r c d)
      (F : ContextFrameEleven W l r d e) :
      SelectedTriplePastingThirteen W l r
        (selectedLeftTripleInnerPasting l r u v t F)
        (selectedLeftTripleDetour l r u v t F)
  | tripleRight {w z : W}
      {a b c d e : PentagonAdjoinedSixCell W l r w z}
      (u : SevenRewrite W l r b c)
      (v : SevenRewrite W l r c d)
      (t : SevenRewrite W l r d e)
      (F : ContextFrameEleven W l r a b) :
      SelectedTriplePastingThirteen W l r
        (selectedRightTripleOuterPasting l r u v t F)
        (selectedRightTripleDetour l r u v t F)
  | reverse {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      (C : SelectedTriplePastingThirteen W l r P Q) :
      SelectedTriplePastingThirteen W l r Q P
  | chain {F G : FramedEleven W l r}
      {P Q R : SelectedUnitalCompositionTwelve W l r F G}
      (C : SelectedTriplePastingThirteen W l r P Q)
      (D : SelectedTriplePastingThirteen W l r Q R) :
      SelectedTriplePastingThirteen W l r P R
  | prepend {F G H : FramedEleven W l r}
      (A : SelectedUnitalCompositionTwelve W l r F G)
      {P Q : SelectedUnitalCompositionTwelve W l r G H}
      (C : SelectedTriplePastingThirteen W l r P Q) :
      SelectedTriplePastingThirteen W l r (.chain A P) (.chain A Q)
  | append {F G H : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      (C : SelectedTriplePastingThirteen W l r P Q)
      (A : SelectedUnitalCompositionTwelve W l r G H) :
      SelectedTriplePastingThirteen W l r (.chain P A) (.chain Q A)
  | associator {F G H I : FramedEleven W l r}
      (A : SelectedUnitalCompositionTwelve W l r F G)
      (B : SelectedUnitalCompositionTwelve W l r G H)
      (C : SelectedUnitalCompositionTwelve W l r H I) :
      SelectedTriplePastingThirteen W l r
        (.chain (.chain A B) C) (.chain A (.chain B C))

/-- Proof-relevant 13D first-atom observer. Its value follows the
first subpath of a chain and ignores dependent original fiber indices;
it is NOT a quotient-invariant or an assertion of old raw equality. -/
def selectedThirteenFirstAtomTag (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    (C : SelectedTriplePastingThirteen W l r P Q) : Nat :=
  match C with
  | .strict _ => 0
  | .inheritedOld _ => 1
  | .tripleLeft _ _ _ _ => 2
  | .tripleRight _ _ _ _ => 3
  | .reverse _ => 4
  | .chain A _ => selectedThirteenFirstAtomTag l r A
  | .prepend _ _ => 6
  | .append _ _ => 7
  | .associator _ _ _ => 8

/-- The old selected 13D proof has a type-preserving inclusion into
the new 13D presentation. This is NOT an interpretation of all new
triple coherence as original v5.23 coherence. -/
def originalThirteenToTriple (l r : W)
    {F G : FramedEleven W l r}
    {P Q : FramedDoubleWhiskerTwelveCell W l r F G}
    (C : CompositionalWhiskerThirteen W l r P Q) :
    SelectedTriplePastingThirteen W l r
      (originalFramedTwelveToSelected l r P)
      (originalFramedTwelveToSelected l r Q) :=
  .inheritedOld C

theorem originalThirteenToTriple_injective (l r : W)
    {F G : FramedEleven W l r}
    {P Q : FramedDoubleWhiskerTwelveCell W l r F G} :
    Function.Injective
      (fun C : CompositionalWhiskerThirteen W l r P Q =>
        originalThirteenToTriple l r C) := by
  intro C D h
  cases h
  rfl

theorem selectedTripleLeft_higherWitness (l r : W) {w z : W}
    {a b c d e : PentagonAdjoinedSixCell W l r w z}
    (u : SevenRewrite W l r a b)
    (v : SevenRewrite W l r b c)
    (t : SevenRewrite W l r c d)
    (F : ContextFrameEleven W l r d e) :
    Nonempty (SelectedTriplePastingThirteen W l r
      (selectedLeftTripleInnerPasting l r u v t F)
      (selectedLeftTripleDetour l r u v t F)) ∧
    selectedLeftTripleInnerPasting l r u v t F ≠
      selectedLeftTripleDetour l r u v t F :=
  ⟨⟨.tripleLeft u v t F⟩, selectedLeftTriple_rawDistinct l r u v t F⟩

theorem selectedTripleRight_higherWitness (l r : W) {w z : W}
    {a b c d e : PentagonAdjoinedSixCell W l r w z}
    (u : SevenRewrite W l r b c)
    (v : SevenRewrite W l r c d)
    (t : SevenRewrite W l r d e)
    (F : ContextFrameEleven W l r a b) :
    Nonempty (SelectedTriplePastingThirteen W l r
      (selectedRightTripleOuterPasting l r u v t F)
      (selectedRightTripleDetour l r u v t F)) ∧
    selectedRightTripleOuterPasting l r u v t F ≠
      selectedRightTripleDetour l r u v t F :=
  ⟨⟨.tripleRight u v t F⟩, selectedRightTriple_rawDistinct l r u v t F⟩

/-- There is no equality interpretation for the new selected
13D triple comparison at ANY genuinely typed triple context. -/
theorem selectedTripleLeft_noRawEqualityInterpreter (l r : W) {w z : W}
    {a b c d e : PentagonAdjoinedSixCell W l r w z}
    (u : SevenRewrite W l r a b)
    (v : SevenRewrite W l r b c)
    (t : SevenRewrite W l r c d)
    (F : ContextFrameEleven W l r d e) :
    ¬ (∀
      (P Q : SelectedUnitalCompositionTwelve W l r
        (selectedLeftTripleSource l r u v t F)
        (selectedLeftTripleRightTarget l r u v t F)),
      SelectedTriplePastingThirteen W l r P Q → P = Q) := by
  intro interpret
  exact selectedLeftTriple_rawDistinct l r u v t F
    (interpret _ _ (.tripleLeft u v t F))

/-- The two unit-pasted 13D histories have identical typed 12D
endpoints, but distinct RAW proof terms. A selected 14D comparison
may therefore be adjoined without silently asserting Eq. -/
def tripleLeftThirteenUnitPrepend (l r : W) {w z : W}
    {a b c d e : PentagonAdjoinedSixCell W l r w z}
    (u : SevenRewrite W l r a b)
    (v : SevenRewrite W l r b c)
    (t : SevenRewrite W l r c d)
    (F : ContextFrameEleven W l r d e) :
    SelectedTriplePastingThirteen W l r
      (selectedLeftTripleInnerPasting l r u v t F)
      (selectedLeftTripleDetour l r u v t F) :=
  .chain (.strict (selectedLeftTripleInnerPasting l r u v t F))
    (.tripleLeft u v t F)

def tripleLeftThirteenUnitAppend (l r : W) {w z : W}
    {a b c d e : PentagonAdjoinedSixCell W l r w z}
    (u : SevenRewrite W l r a b)
    (v : SevenRewrite W l r b c)
    (t : SevenRewrite W l r c d)
    (F : ContextFrameEleven W l r d e) :
    SelectedTriplePastingThirteen W l r
      (selectedLeftTripleInnerPasting l r u v t F)
      (selectedLeftTripleDetour l r u v t F) :=
  .chain (.tripleLeft u v t F)
    (.strict (selectedLeftTripleDetour l r u v t F))

theorem tripleLeftThirteenUnit_rawDistinct (l r : W) {w z : W}
    {a b c d e : PentagonAdjoinedSixCell W l r w z}
    (u : SevenRewrite W l r a b)
    (v : SevenRewrite W l r b c)
    (t : SevenRewrite W l r c d)
    (F : ContextFrameEleven W l r d e) :
    tripleLeftThirteenUnitPrepend l r u v t F ≠
      tripleLeftThirteenUnitAppend l r u v t F := by
  intro h
  have ht := congrArg (selectedThirteenFirstAtomTag l r) h
  change (0 : Nat) = 2 at ht
  cases ht

def tripleRightThirteenUnitPrepend (l r : W) {w z : W}
    {a b c d e : PentagonAdjoinedSixCell W l r w z}
    (u : SevenRewrite W l r b c)
    (v : SevenRewrite W l r c d)
    (t : SevenRewrite W l r d e)
    (F : ContextFrameEleven W l r a b) :
    SelectedTriplePastingThirteen W l r
      (selectedRightTripleOuterPasting l r u v t F)
      (selectedRightTripleDetour l r u v t F) :=
  .chain (.strict (selectedRightTripleOuterPasting l r u v t F))
    (.tripleRight u v t F)

def tripleRightThirteenUnitAppend (l r : W) {w z : W}
    {a b c d e : PentagonAdjoinedSixCell W l r w z}
    (u : SevenRewrite W l r b c)
    (v : SevenRewrite W l r c d)
    (t : SevenRewrite W l r d e)
    (F : ContextFrameEleven W l r a b) :
    SelectedTriplePastingThirteen W l r
      (selectedRightTripleOuterPasting l r u v t F)
      (selectedRightTripleDetour l r u v t F) :=
  .chain (.tripleRight u v t F)
    (.strict (selectedRightTripleDetour l r u v t F))

theorem tripleRightThirteenUnit_rawDistinct (l r : W) {w z : W}
    {a b c d e : PentagonAdjoinedSixCell W l r w z}
    (u : SevenRewrite W l r b c)
    (v : SevenRewrite W l r c d)
    (t : SevenRewrite W l r d e)
    (F : ContextFrameEleven W l r a b) :
    tripleRightThirteenUnitPrepend l r u v t F ≠
      tripleRightThirteenUnitAppend l r u v t F := by
  intro h
  have ht := congrArg (selectedThirteenFirstAtomTag l r) h
  change (0 : Nat) = 3 at ht
  cases ht

/-- Explicitly selected FOURTEENTH comparison. The inherited branch
retains a genuine previous v5.23 SelectedCompositionFourteen proof;
the two new critical faces are conditional only on actual original
triple contexts, never arbitrary higher coherence. -/
inductive SelectedTriplePastingFourteen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    {P Q : SelectedUnitalCompositionTwelve W l r F G} →
    SelectedTriplePastingThirteen W l r P Q →
    SelectedTriplePastingThirteen W l r P Q → Type uSix where
  | strict {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      (C : SelectedTriplePastingThirteen W l r P Q) :
      SelectedTriplePastingFourteen W l r C C
  | inheritedOld {F G : FramedEleven W l r}
      {P Q : FramedDoubleWhiskerTwelveCell W l r F G}
      {C D : CompositionalWhiskerThirteen W l r P Q}
      (V : SelectedCompositionFourteen W l r C D) :
      SelectedTriplePastingFourteen W l r
        (originalThirteenToTriple l r C)
        (originalThirteenToTriple l r D)
  | tripleLeftUnit {w z : W}
      {a b c d e : PentagonAdjoinedSixCell W l r w z}
      (u : SevenRewrite W l r a b)
      (v : SevenRewrite W l r b c)
      (t : SevenRewrite W l r c d)
      (F : ContextFrameEleven W l r d e) :
      SelectedTriplePastingFourteen W l r
        (tripleLeftThirteenUnitPrepend l r u v t F)
        (tripleLeftThirteenUnitAppend l r u v t F)
  | tripleRightUnit {w z : W}
      {a b c d e : PentagonAdjoinedSixCell W l r w z}
      (u : SevenRewrite W l r b c)
      (v : SevenRewrite W l r c d)
      (t : SevenRewrite W l r d e)
      (F : ContextFrameEleven W l r a b) :
      SelectedTriplePastingFourteen W l r
        (tripleRightThirteenUnitPrepend l r u v t F)
        (tripleRightThirteenUnitAppend l r u v t F)
  | reverse {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedTriplePastingThirteen W l r P Q}
      (V : SelectedTriplePastingFourteen W l r C D) :
      SelectedTriplePastingFourteen W l r D C
  | chain {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D E : SelectedTriplePastingThirteen W l r P Q}
      (V : SelectedTriplePastingFourteen W l r C D)
      (X : SelectedTriplePastingFourteen W l r D E) :
      SelectedTriplePastingFourteen W l r C E

theorem selectedTripleLeftFourteen_conditionalCube (l r : W) {w z : W}
    {a b c d e : PentagonAdjoinedSixCell W l r w z}
    (u : SevenRewrite W l r a b)
    (v : SevenRewrite W l r b c)
    (t : SevenRewrite W l r c d)
    (F : ContextFrameEleven W l r d e) :
    Nonempty (SelectedTriplePastingFourteen W l r
      (tripleLeftThirteenUnitPrepend l r u v t F)
      (tripleLeftThirteenUnitAppend l r u v t F)) ∧
    tripleLeftThirteenUnitPrepend l r u v t F ≠
      tripleLeftThirteenUnitAppend l r u v t F :=
  ⟨⟨.tripleLeftUnit u v t F⟩, tripleLeftThirteenUnit_rawDistinct l r u v t F⟩

theorem selectedTripleRightFourteen_conditionalCube (l r : W) {w z : W}
    {a b c d e : PentagonAdjoinedSixCell W l r w z}
    (u : SevenRewrite W l r b c)
    (v : SevenRewrite W l r c d)
    (t : SevenRewrite W l r d e)
    (F : ContextFrameEleven W l r a b) :
    Nonempty (SelectedTriplePastingFourteen W l r
      (tripleRightThirteenUnitPrepend l r u v t F)
      (tripleRightThirteenUnitAppend l r u v t F)) ∧
    tripleRightThirteenUnitPrepend l r u v t F ≠
      tripleRightThirteenUnitAppend l r u v t F :=
  ⟨⟨.tripleRightUnit u v t F⟩, tripleRightThirteenUnit_rawDistinct l r u v t F⟩

/-- Concrete transport of an actual OLD v5.23 conditional
fourteenth comparison into the separate retained old sector. -/
def originalFourteenToTriple (l r : W)
    {F G : FramedEleven W l r}
    {P Q : FramedDoubleWhiskerTwelveCell W l r F G}
    {C D : CompositionalWhiskerThirteen W l r P Q}
    (V : SelectedCompositionFourteen W l r C D) :
    SelectedTriplePastingFourteen W l r
      (originalThirteenToTriple l r C)
      (originalThirteenToTriple l r D) :=
  .inheritedOld V

theorem originalFourteenToTriple_injective (l r : W)
    {F G : FramedEleven W l r}
    {P Q : FramedDoubleWhiskerTwelveCell W l r F G}
    {C D : CompositionalWhiskerThirteen W l r P Q} :
    Function.Injective
      (fun V : SelectedCompositionFourteen W l r C D =>
        originalFourteenToTriple l r V) := by
  intro V X h
  cases h
  rfl

/-- The existence of the selected 14D cube never asserts equality
between its different original 13D proof terms. -/
theorem selectedTripleLeftFourteen_noRawEqualityInterpreter (l r : W) {w z : W}
    {a b c d e : PentagonAdjoinedSixCell W l r w z}
    (u : SevenRewrite W l r a b)
    (v : SevenRewrite W l r b c)
    (t : SevenRewrite W l r c d)
    (F : ContextFrameEleven W l r d e) :
    ¬ (∀
      (C D : SelectedTriplePastingThirteen W l r
        (selectedLeftTripleInnerPasting l r u v t F)
        (selectedLeftTripleDetour l r u v t F)),
      SelectedTriplePastingFourteen W l r C D → C = D) := by
  intro interpret
  exact tripleLeftThirteenUnit_rawDistinct l r u v t F
    (interpret _ _ (.tripleLeftUnit u v t F))

#print axioms PentagonAdjoinedSixCell.selectedTwelfthFirstAtomTag
#print axioms PentagonAdjoinedSixCell.selectedThirteenFirstAtomTag
#print axioms PentagonAdjoinedSixCell.originalFramedTwelveToSelected
#print axioms PentagonAdjoinedSixCell.originalFramedTwelveToSelected_injective
#print axioms PentagonAdjoinedSixCell.selectedLeftTripleSource
#print axioms PentagonAdjoinedSixCell.selectedLeftTripleLeftTarget
#print axioms PentagonAdjoinedSixCell.selectedLeftTripleRightTarget
#print axioms PentagonAdjoinedSixCell.selectedLeftTripleInnerPasting
#print axioms PentagonAdjoinedSixCell.selectedLeftTripleOuterPasting
#print axioms PentagonAdjoinedSixCell.selectedLeftTripleRebracket
#print axioms PentagonAdjoinedSixCell.selectedLeftTripleDetour
#print axioms PentagonAdjoinedSixCell.selectedLeftTriple_rawDistinct
#print axioms PentagonAdjoinedSixCell.selectedLeftTriple_twoBracketClasses
#print axioms PentagonAdjoinedSixCell.selectedRightTripleSource
#print axioms PentagonAdjoinedSixCell.selectedRightTripleLeftTarget
#print axioms PentagonAdjoinedSixCell.selectedRightTripleRightTarget
#print axioms PentagonAdjoinedSixCell.selectedRightTripleOuterPasting
#print axioms PentagonAdjoinedSixCell.selectedRightTripleInnerPasting
#print axioms PentagonAdjoinedSixCell.selectedRightTripleRebracket
#print axioms PentagonAdjoinedSixCell.selectedRightTripleDetour
#print axioms PentagonAdjoinedSixCell.selectedRightTriple_rawDistinct
#print axioms PentagonAdjoinedSixCell.selectedRightTriple_twoBracketClasses
#print axioms PentagonAdjoinedSixCell.SelectedTriplePastingThirteen
#print axioms PentagonAdjoinedSixCell.originalThirteenToTriple
#print axioms PentagonAdjoinedSixCell.originalThirteenToTriple_injective
#print axioms PentagonAdjoinedSixCell.selectedTripleLeft_higherWitness
#print axioms PentagonAdjoinedSixCell.selectedTripleRight_higherWitness
#print axioms PentagonAdjoinedSixCell.selectedTripleLeft_noRawEqualityInterpreter
#print axioms PentagonAdjoinedSixCell.tripleLeftThirteenUnitPrepend
#print axioms PentagonAdjoinedSixCell.tripleLeftThirteenUnitAppend
#print axioms PentagonAdjoinedSixCell.tripleLeftThirteenUnit_rawDistinct
#print axioms PentagonAdjoinedSixCell.tripleRightThirteenUnitPrepend
#print axioms PentagonAdjoinedSixCell.tripleRightThirteenUnitAppend
#print axioms PentagonAdjoinedSixCell.tripleRightThirteenUnit_rawDistinct
#print axioms PentagonAdjoinedSixCell.SelectedTriplePastingFourteen
#print axioms PentagonAdjoinedSixCell.selectedTripleLeftFourteen_conditionalCube
#print axioms PentagonAdjoinedSixCell.selectedTripleRightFourteen_conditionalCube
#print axioms PentagonAdjoinedSixCell.originalFourteenToTriple
#print axioms PentagonAdjoinedSixCell.originalFourteenToTriple_injective
#print axioms PentagonAdjoinedSixCell.selectedTripleLeftFourteen_noRawEqualityInterpreter

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
