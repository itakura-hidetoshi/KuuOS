import KUOS.Architecture.QiWuxingGK5CHP77LocalThirteenNaturalityV5_29

/-!
Qi v5.30 — genuine original seventh-cell LEFT/RIGHT mixed-context
interchange, proof-relevant 13D naturality cube, and local selected
15D unit coherence.

We do not identify the two ORIGINAL ordered raw context histories:
  L_before (R_after F)   versus   R_after (L_before F).
The original v5.18 doubleWhisker is embedded, through the ACTUAL
v5.25 and v5.27 constructors, to give an explicit 12D boundary
bridge between them. For any genuine selected 12D P, the two
mixed-context comparison routes share exact framed endpoints:
  beta_F ; R(L(P))     versus     L(R(P)) ; beta_G.
They are distinct raw selected 12D proof values; their first atom
tags are 1 versus 4. Equality holds only at the selected endpoint
quotient, not between raw path terms.

An INDEPENDENT selected 13D presentation adds exactly ONE local
mixed interchange family indexed by the true 7D contexts, their
exact six-cell boundary fibers and a selected 12D proof P. The old
contextual 13D proof values from v5.29 remain faithfully embedded.
The 13D interchange is NOT an old v5.23 13D proof.

A further independent selected 14D presentation adjoins the
natural-square family for an ACTUAL v5.29 contextual 13D proof
C : P ==> Q. Its two typed 13D sides are
  (beta_F * R(L(C))) ; I_Q
  I_P ; (L(R(C)) * beta_G).
Their underlying 12D endpoints agree exactly. The parallel raw
13D paths are distinct. All previous v5.29 selected 14D values
and the v5.23 originals are preserved injectively.

Finally a selected 15D local generator compares two unit-pasted
selected 14D histories, without asserting the old 14D raw Eq.
The old original-12D endpoint lift criterion is shown impossible
for the mixed 13D interchange (the lower route begins with tag 4,
not the old embedding tag 1). A selected quotient boundary bridge
nevertheless exists: weak compatibility does NOT restore strict
old-source evidence.

No original 6D–14D constructors, F55/P77/GK5CG sources or selected
v5.23–v5.29 proof objects are changed. No global 15D coherence,
all-presentation strictification, arbitrary lift, or new axioms.
Append-only / tighten-only / overwrite-forbidden / same-root.
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

/-- ACTUAL old framed double-whisker carried through both retained
previous constructors, not a fabricated equality of ordered proofs. -/
def selectedMixedBoundaryBridge (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F : ContextFrameEleven W l r c d)
    (after : SevenRewrite W l r d e) :
    SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r
        (contextFrameLeft l r before (contextFrameRight l r F after)))
      (contextFramePack l r
        (contextFrameRight l r (contextFrameLeft l r before F) after)) :=
  .previous (.previous (.doubleWhisker before F.H after))

/-- Apply RIGHT first and LEFT last to an actual selected 12D P. -/
def selectedMixedLeftAfterRight (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    (P : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G))
    (after : SevenRewrite W l r d e) :
    SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r
        (contextFrameLeft l r before (contextFrameRight l r F after)))
      (contextFramePack l r
        (contextFrameLeft l r before (contextFrameRight l r G after))) :=
  .whiskerLeft before (contextFrameRight l r F after)
    (contextFrameRight l r G after) (.whiskerRight F G P after)

/-- Apply LEFT first and RIGHT last to the same actual P. -/
def selectedMixedRightAfterLeft (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    (P : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G))
    (after : SevenRewrite W l r d e) :
    SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r
        (contextFrameRight l r (contextFrameLeft l r before F) after))
      (contextFramePack l r
        (contextFrameRight l r (contextFrameLeft l r before G) after)) :=
  .whiskerRight (contextFrameLeft l r before F)
    (contextFrameLeft l r before G) (.whiskerLeft before F G P) after

/-- Two genuinely typed mixed 12D routes, both L(R(F)) --> R(L(G)).
The old double-whisker bridge appears on OPPOSITE ends. -/
def selectedMixedUpperRoute (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    (P : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G))
    (after : SevenRewrite W l r d e) :
    SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r
        (contextFrameLeft l r before (contextFrameRight l r F after)))
      (contextFramePack l r
        (contextFrameRight l r (contextFrameLeft l r before G) after)) :=
  .chain (selectedMixedBoundaryBridge l r before F after)
    (selectedMixedRightAfterLeft l r before F G P after)

def selectedMixedLowerRoute (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    (P : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G))
    (after : SevenRewrite W l r d e) :
    SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r
        (contextFrameLeft l r before (contextFrameRight l r F after)))
      (contextFramePack l r
        (contextFrameRight l r (contextFrameLeft l r before G) after)) :=
  .chain (selectedMixedLeftAfterRight l r before F G P after)
    (selectedMixedBoundaryBridge l r before G after)

/-- Existing first-constructor observer yields a definite obstruction
to treating the two mixed 12D path histories as the SAME RAW value. -/
theorem selectedMixedRoutes_rawDistinct (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    (P : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G))
    (after : SevenRewrite W l r d e) :
    selectedMixedUpperRoute l r before F G P after ≠
      selectedMixedLowerRoute l r before F G P after := by
  intro h
  have ht := congrArg (selectedTwelfthFirstAtomTag l r) h
  change (1 : Nat) = 4 at ht
  cases ht

/-- Weaker quotient-level interchange is possible because an
ACTUAL original double-whisker supplies the boundary comparison. -/
theorem selectedMixedBoundary_quotientCompatible (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F : ContextFrameEleven W l r c d)
    (after : SevenRewrite W l r d e) :
    selectedUnitalClass l r
        (contextFramePack l r
          (contextFrameLeft l r before (contextFrameRight l r F after))) =
      selectedUnitalClass l r
        (contextFramePack l r
          (contextFrameRight l r (contextFrameLeft l r before F) after)) :=
  Quotient.sound ⟨selectedMixedBoundaryBridge l r before F after⟩

/-- The lower mixed route CANNOT be an old raw framed twelfth proof
value embedded by the two previous constructors (tag 1 versus 4).
This refutes a NECESSARY strict old-thirteenth lift condition. -/
theorem selectedMixedRoutes_noOriginalEndpoints (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    (P : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G))
    (after : SevenRewrite W l r d e) :
    ¬ HasOriginalTwelveEndpoints l r
      (selectedMixedUpperRoute l r before F G P after)
      (selectedMixedLowerRoute l r before F G P after) := by
  intro h
  rcases h with ⟨_U, _V, _hU, hV⟩
  have ht := congrArg (selectedTwelfthFirstAtomTag l r) hV
  change (1 : Nat) = 4 at ht
  cases ht

/-- The two opposite orders of transporting a GENUINE v5.29
contextual 13D proof C. Their raw 12D endpoints differ, so equality
between these two proof values is not even a well-typed statement. -/
def selectedMixedLeftAfterRightThirteen (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    SelectedContextualThirteen W l r
      (selectedMixedLeftAfterRight l r before F G P after)
      (selectedMixedLeftAfterRight l r before F G Q after) :=
  .whiskerLeft before (contextFrameRight l r F after)
    (contextFrameRight l r G after) (.whiskerRight F G C after)

def selectedMixedRightAfterLeftThirteen (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    SelectedContextualThirteen W l r
      (selectedMixedRightAfterLeft l r before F G P after)
      (selectedMixedRightAfterLeft l r before F G Q after) :=
  .whiskerRight (contextFrameLeft l r before F)
    (contextFrameLeft l r before G) (.whiskerLeft before F G C) after

/-- Minimal independent mixed 13D presentation. Inheritance keeps
the ENTIRE previous context-closed thirteenth Type without editing it;
the new mixed generator is restricted to a real compatible seventh
boundary and an actual chosen twelfth proof term. -/
inductive SelectedMixedInterchangerThirteen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    SelectedUnitalCompositionTwelve W l r F G →
    SelectedUnitalCompositionTwelve W l r F G → Type uSix where
  | inherited {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      (C : SelectedContextualThirteen W l r P Q) :
      SelectedMixedInterchangerThirteen W l r P Q
  | mixed {w z : W}
      {b c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      (P : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G))
      (after : SevenRewrite W l r d e) :
      SelectedMixedInterchangerThirteen W l r
        (selectedMixedUpperRoute l r before F G P after)
        (selectedMixedLowerRoute l r before F G P after)
  | strict {F G : FramedEleven W l r}
      (P : SelectedUnitalCompositionTwelve W l r F G) :
      SelectedMixedInterchangerThirteen W l r P P
  | reverse {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      (C : SelectedMixedInterchangerThirteen W l r P Q) :
      SelectedMixedInterchangerThirteen W l r Q P
  | chain {F G : FramedEleven W l r}
      {P Q R : SelectedUnitalCompositionTwelve W l r F G}
      (C : SelectedMixedInterchangerThirteen W l r P Q)
      (D : SelectedMixedInterchangerThirteen W l r Q R) :
      SelectedMixedInterchangerThirteen W l r P R
  | prepend {E F G : FramedEleven W l r}
      (A : SelectedUnitalCompositionTwelve W l r E F)
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      (C : SelectedMixedInterchangerThirteen W l r P Q) :
      SelectedMixedInterchangerThirteen W l r (.chain A P) (.chain A Q)
  | append {E F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r E F}
      (C : SelectedMixedInterchangerThirteen W l r P Q)
      (B : SelectedUnitalCompositionTwelve W l r F G) :
      SelectedMixedInterchangerThirteen W l r (.chain P B) (.chain Q B)
  | whiskerLeft {w z : W}
      {b c d : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      (C : SelectedMixedInterchangerThirteen W l r P Q) :
      SelectedMixedInterchangerThirteen W l r
        (.whiskerLeft before F G P)
        (.whiskerLeft before F G Q)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      (C : SelectedMixedInterchangerThirteen W l r P Q)
      (after : SevenRewrite W l r d e) :
      SelectedMixedInterchangerThirteen W l r
        (.whiskerRight F G P after)
        (.whiskerRight F G Q after)

/-- Raw 13D event observer: tracks the first non-chain proof
constructor, but DOES NOT descend to any selected 13D quotient. -/
def selectedMixedThirteenFirstAtomTag (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    (C : SelectedMixedInterchangerThirteen W l r P Q) : Nat :=
  match C with
  | .inherited _ => 0
  | .mixed _ _ _ _ _ => 1
  | .strict _ => 2
  | .reverse _ => 3
  | .chain C _ => selectedMixedThirteenFirstAtomTag l r C
  | .prepend _ _ => 6
  | .append _ _ => 7
  | .whiskerLeft _ _ _ _ => 8
  | .whiskerRight _ _ _ _ => 9

theorem selectedMixedThirteen_inherited_injective (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G} :
    Function.Injective (fun C : SelectedContextualThirteen W l r P Q =>
      SelectedMixedInterchangerThirteen.inherited C) := by
  intro C D h
  cases h
  rfl

/-- Actual, local mixed 13D interchanger exists, and its two 12D
boundaries are provably distinct as raw proof syntax. -/
theorem selectedMixedThirteen_interchangeWitness (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    (P : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G))
    (after : SevenRewrite W l r d e) :
    Nonempty (SelectedMixedInterchangerThirteen W l r
      (selectedMixedUpperRoute l r before F G P after)
      (selectedMixedLowerRoute l r before F G P after)) ∧
    selectedMixedUpperRoute l r before F G P after ≠
      selectedMixedLowerRoute l r before F G P after :=
  ⟨⟨.mixed before F G P after⟩,
    selectedMixedRoutes_rawDistinct l r before F G P after⟩

/-- Mixed square first route: transport C along R(L(·)), prepend
the ORIGINAL double-whisker bridge at F, then interchange at Q. -/
def selectedMixedNaturalityViaUpper (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    SelectedMixedInterchangerThirteen W l r
      (selectedMixedUpperRoute l r before F G P after)
      (selectedMixedLowerRoute l r before F G Q after) :=
  .chain
    (.prepend (selectedMixedBoundaryBridge l r before F after)
      (.inherited (selectedMixedRightAfterLeftThirteen l r before F G C after)))
    (.mixed before F G Q after)

/-- Second route: interchange at P, transport C along L(R(·)),
then append the ORIGINAL bridge at G. Its 12D endpoints are
EXACTLY those of selectedMixedNaturalityViaUpper. -/
def selectedMixedNaturalityViaLower (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    SelectedMixedInterchangerThirteen W l r
      (selectedMixedUpperRoute l r before F G P after)
      (selectedMixedLowerRoute l r before F G Q after) :=
  .chain (.mixed before F G P after)
    (.append
      (.inherited (selectedMixedLeftAfterRightThirteen l r before F G C after))
      (selectedMixedBoundaryBridge l r before G after))

/-- The two resulting mixed 13D proof paths are RAW distinct even
though they have precisely matching proof-relevant 12D endpoints. -/
theorem selectedMixedNaturality_rawDistinct (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedMixedNaturalityViaUpper l r before F G C after ≠
      selectedMixedNaturalityViaLower l r before F G C after := by
  intro h
  have ht := congrArg (selectedMixedThirteenFirstAtomTag l r) h
  change (6 : Nat) = 1 at ht
  cases ht

/-- Independent selected FOURTEENTH presentation for the actual
mixed context naturality critical pair. There is no axiom asserting
naturality for arbitrary newly adjoined 13D proof terms. -/
inductive SelectedMixedNaturalityFourteen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    {P Q : SelectedUnitalCompositionTwelve W l r F G} →
    SelectedMixedInterchangerThirteen W l r P Q →
    SelectedMixedInterchangerThirteen W l r P Q → Type uSix where
  | inherited {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedContextualThirteen W l r P Q}
      (V : SelectedNaturalityFourteen W l r C D) :
      SelectedMixedNaturalityFourteen W l r
        (.inherited C) (.inherited D)
  | criticalMixed {w z : W}
      {b c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      (C : SelectedContextualThirteen W l r P Q)
      (after : SevenRewrite W l r d e) :
      SelectedMixedNaturalityFourteen W l r
        (selectedMixedNaturalityViaUpper l r before F G C after)
        (selectedMixedNaturalityViaLower l r before F G C after)
  | strict {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      (C : SelectedMixedInterchangerThirteen W l r P Q) :
      SelectedMixedNaturalityFourteen W l r C C
  | reverse {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      (V : SelectedMixedNaturalityFourteen W l r C D) :
      SelectedMixedNaturalityFourteen W l r D C
  | chain {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D E : SelectedMixedInterchangerThirteen W l r P Q}
      (V : SelectedMixedNaturalityFourteen W l r C D)
      (X : SelectedMixedNaturalityFourteen W l r D E) :
      SelectedMixedNaturalityFourteen W l r C E
  | whiskerLeft {w z : W}
      {b c d : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      (V : SelectedMixedNaturalityFourteen W l r C D) :
      SelectedMixedNaturalityFourteen W l r
        (.whiskerLeft before F G C) (.whiskerLeft before F G D)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      (V : SelectedMixedNaturalityFourteen W l r C D)
      (after : SevenRewrite W l r d e) :
      SelectedMixedNaturalityFourteen W l r
        (.whiskerRight F G C after) (.whiskerRight F G D after)

def selectedOldNaturalityFourteenToMixed (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedContextualThirteen W l r P Q}
    (V : SelectedNaturalityFourteen W l r C D) :
    SelectedMixedNaturalityFourteen W l r (.inherited C) (.inherited D) :=
  .inherited V

theorem selectedOldNaturalityFourteenToMixed_injective (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedContextualThirteen W l r P Q} :
    Function.Injective
      (fun V : SelectedNaturalityFourteen W l r C D =>
        selectedOldNaturalityFourteenToMixed l r V) := by
  intro V X h
  cases h
  rfl

/-- Actual v5.23 selected 14D evidence remains stored through
v5.28, v5.29 and the new independent selected v5.30 14D syntax. -/
def selectedOriginalFourteenToMixed (l r : W)
    {F G : FramedEleven W l r}
    {P Q : FramedDoubleWhiskerTwelveCell W l r F G}
    {C D : CompositionalWhiskerThirteen W l r P Q}
    (V : SelectedCompositionFourteen W l r C D) :
    SelectedMixedNaturalityFourteen W l r
      (.inherited (.inherited (originalThirteenToTriple l r C)))
      (.inherited (.inherited (originalThirteenToTriple l r D))) :=
  selectedOldNaturalityFourteenToMixed l r (oldFourteenToNaturality l r V)

theorem selectedOriginalFourteenToMixed_injective (l r : W)
    {F G : FramedEleven W l r}
    {P Q : FramedDoubleWhiskerTwelveCell W l r F G}
    {C D : CompositionalWhiskerThirteen W l r P Q} :
    Function.Injective (fun V : SelectedCompositionFourteen W l r C D =>
      selectedOriginalFourteenToMixed l r V) := by
  intro V X h
  apply oldFourteenToNaturality_injective l r
  apply selectedOldNaturalityFourteenToMixed_injective l r
  exact h

theorem selectedMixedNaturality_conditionalCube (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    Nonempty (SelectedMixedNaturalityFourteen W l r
      (selectedMixedNaturalityViaUpper l r before F G C after)
      (selectedMixedNaturalityViaLower l r before F G C after)) ∧
    selectedMixedNaturalityViaUpper l r before F G C after ≠
      selectedMixedNaturalityViaLower l r before F G C after :=
  ⟨⟨.criticalMixed before F G C after⟩,
    selectedMixedNaturality_rawDistinct l r before F G C after⟩

/-- Local 14D selected comparisons transport under either genuine
original seventh-cell context action (not a raw 13D Eq). -/
theorem selectedMixedFourteen_leftStable (l r : W) {w z : W}
    {b c d : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    (V : SelectedMixedNaturalityFourteen W l r C D) :
    Nonempty (SelectedMixedNaturalityFourteen W l r
      (.whiskerLeft before F G C) (.whiskerLeft before F G D)) :=
  ⟨.whiskerLeft before F G V⟩

theorem selectedMixedFourteen_rightStable (l r : W) {w z : W}
    {c d e : PentagonAdjoinedSixCell W l r w z}
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    (V : SelectedMixedNaturalityFourteen W l r C D)
    (after : SevenRewrite W l r d e) :
    Nonempty (SelectedMixedNaturalityFourteen W l r
      (.whiskerRight F G C after) (.whiskerRight F G D after)) :=
  ⟨.whiskerRight F G V after⟩

/-- Proof-relevant 14D first-constructor observer for the independent
selected grammar. It is NOT invariant under the forthcoming 15D. -/
def selectedMixedFourteenFirstAtomTag (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    (V : SelectedMixedNaturalityFourteen W l r C D) : Nat :=
  match V with
  | .inherited _ => 0
  | .criticalMixed _ _ _ _ _ => 1
  | .strict _ => 2
  | .reverse _ => 3
  | .chain V _ => selectedMixedFourteenFirstAtomTag l r V
  | .whiskerLeft _ _ _ _ => 5
  | .whiskerRight _ _ _ _ => 6

/-- The same 14D local naturality comparison with a raw 14D
identity BEFORE it. The two unit histories are NOT definitionally
equal even though they have matching 13D endpoints. -/
def selectedMixedFourteenUnitPrepend (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    SelectedMixedNaturalityFourteen W l r
      (selectedMixedNaturalityViaUpper l r before F G C after)
      (selectedMixedNaturalityViaLower l r before F G C after) :=
  .chain (.strict (selectedMixedNaturalityViaUpper l r before F G C after))
    (.criticalMixed before F G C after)

def selectedMixedFourteenUnitAppend (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    SelectedMixedNaturalityFourteen W l r
      (selectedMixedNaturalityViaUpper l r before F G C after)
      (selectedMixedNaturalityViaLower l r before F G C after) :=
  .chain (.criticalMixed before F G C after)
    (.strict (selectedMixedNaturalityViaLower l r before F G C after))

theorem selectedMixedFourteenUnit_rawDistinct (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedMixedFourteenUnitPrepend l r before F G C after ≠
      selectedMixedFourteenUnitAppend l r before F G C after := by
  intro h
  have ht := congrArg (selectedMixedFourteenFirstAtomTag l r) h
  change (2 : Nat) = 1 at ht
  cases ht

/-- SELECTED FIFTEENTH presentation. The ONLY new nontrivial
generator is the genuine mixed naturality unit-pasting critical pair.
No old 14D equality or unrestricted 15D coherence is assumed. -/
inductive SelectedMixedCoherenceFifteen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    {P Q : SelectedUnitalCompositionTwelve W l r F G} →
    {C D : SelectedMixedInterchangerThirteen W l r P Q} →
    SelectedMixedNaturalityFourteen W l r C D →
    SelectedMixedNaturalityFourteen W l r C D → Type uSix where
  | strict {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      (V : SelectedMixedNaturalityFourteen W l r C D) :
      SelectedMixedCoherenceFifteen W l r V V
  | criticalUnit {w z : W}
      {b c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      (C : SelectedContextualThirteen W l r P Q)
      (after : SevenRewrite W l r d e) :
      SelectedMixedCoherenceFifteen W l r
        (selectedMixedFourteenUnitPrepend l r before F G C after)
        (selectedMixedFourteenUnitAppend l r before F G C after)
  | reverse {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      (T : SelectedMixedCoherenceFifteen W l r V X) :
      SelectedMixedCoherenceFifteen W l r X V
  | chain {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X Y : SelectedMixedNaturalityFourteen W l r C D}
      (T : SelectedMixedCoherenceFifteen W l r V X)
      (U : SelectedMixedCoherenceFifteen W l r X Y) :
      SelectedMixedCoherenceFifteen W l r V Y

theorem selectedMixedFifteen_conditionalUnitCube (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    Nonempty (SelectedMixedCoherenceFifteen W l r
      (selectedMixedFourteenUnitPrepend l r before F G C after)
      (selectedMixedFourteenUnitAppend l r before F G C after)) ∧
    selectedMixedFourteenUnitPrepend l r before F G C after ≠
      selectedMixedFourteenUnitAppend l r before F G C after :=
  ⟨⟨.criticalUnit before F G C after⟩,
    selectedMixedFourteenUnit_rawDistinct l r before F G C after⟩

/-- The selected 14D mixed naturality square does not imply
literal equality of its two raw 13D proof histories. -/
theorem selectedMixedFourteen_noRawEqualityInterpreter (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    ¬ (∀
      (A B : SelectedMixedInterchangerThirteen W l r
        (selectedMixedUpperRoute l r before F G P after)
        (selectedMixedLowerRoute l r before F G Q after)),
      SelectedMixedNaturalityFourteen W l r A B → A = B) := by
  intro interpret
  exact selectedMixedNaturality_rawDistinct l r before F G C after
    (interpret _ _ (.criticalMixed before F G C after))

/-- Likewise the selected 15D unit comparison never implies
literal equality of the two proof-relevant 14D construction trees. -/
theorem selectedMixedFifteen_noRawEqualityInterpreter (l r : W) {w z : W}
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
      SelectedMixedCoherenceFifteen W l r V X → V = X) := by
  intro interpret
  exact selectedMixedFourteenUnit_rawDistinct l r before F G C after
    (interpret _ _ (.criticalUnit before F G C after))

#print axioms PentagonAdjoinedSixCell.selectedMixedBoundaryBridge
#print axioms PentagonAdjoinedSixCell.selectedMixedLeftAfterRight
#print axioms PentagonAdjoinedSixCell.selectedMixedRightAfterLeft
#print axioms PentagonAdjoinedSixCell.selectedMixedUpperRoute
#print axioms PentagonAdjoinedSixCell.selectedMixedLowerRoute
#print axioms PentagonAdjoinedSixCell.selectedMixedRoutes_rawDistinct
#print axioms PentagonAdjoinedSixCell.selectedMixedBoundary_quotientCompatible
#print axioms PentagonAdjoinedSixCell.selectedMixedRoutes_noOriginalEndpoints
#print axioms PentagonAdjoinedSixCell.selectedMixedLeftAfterRightThirteen
#print axioms PentagonAdjoinedSixCell.selectedMixedRightAfterLeftThirteen
#print axioms PentagonAdjoinedSixCell.SelectedMixedInterchangerThirteen
#print axioms PentagonAdjoinedSixCell.selectedMixedThirteenFirstAtomTag
#print axioms PentagonAdjoinedSixCell.selectedMixedThirteen_inherited_injective
#print axioms PentagonAdjoinedSixCell.selectedMixedThirteen_interchangeWitness
#print axioms PentagonAdjoinedSixCell.selectedMixedNaturalityViaUpper
#print axioms PentagonAdjoinedSixCell.selectedMixedNaturalityViaLower
#print axioms PentagonAdjoinedSixCell.selectedMixedNaturality_rawDistinct
#print axioms PentagonAdjoinedSixCell.SelectedMixedNaturalityFourteen
#print axioms PentagonAdjoinedSixCell.selectedOldNaturalityFourteenToMixed
#print axioms PentagonAdjoinedSixCell.selectedOldNaturalityFourteenToMixed_injective
#print axioms PentagonAdjoinedSixCell.selectedOriginalFourteenToMixed
#print axioms PentagonAdjoinedSixCell.selectedOriginalFourteenToMixed_injective
#print axioms PentagonAdjoinedSixCell.selectedMixedNaturality_conditionalCube
#print axioms PentagonAdjoinedSixCell.selectedMixedFourteen_leftStable
#print axioms PentagonAdjoinedSixCell.selectedMixedFourteen_rightStable
#print axioms PentagonAdjoinedSixCell.selectedMixedFourteenFirstAtomTag
#print axioms PentagonAdjoinedSixCell.selectedMixedFourteenUnitPrepend
#print axioms PentagonAdjoinedSixCell.selectedMixedFourteenUnitAppend
#print axioms PentagonAdjoinedSixCell.selectedMixedFourteenUnit_rawDistinct
#print axioms PentagonAdjoinedSixCell.SelectedMixedCoherenceFifteen
#print axioms PentagonAdjoinedSixCell.selectedMixedFifteen_conditionalUnitCube
#print axioms PentagonAdjoinedSixCell.selectedMixedFourteen_noRawEqualityInterpreter
#print axioms PentagonAdjoinedSixCell.selectedMixedFifteen_noRawEqualityInterpreter

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
