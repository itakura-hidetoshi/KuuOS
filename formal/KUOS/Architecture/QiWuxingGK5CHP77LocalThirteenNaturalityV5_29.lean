import KUOS.Architecture.QiWuxingGK5CHP77TripleContextHigherPastingV5_28

/-!
Qi v5.29 — typed pre/post pasting naturality and contextual stability
of the LOCAL selected triple-thirteenth comparisons from v5.28.

Two parallel proof-relevant 13D routes are constructed using real
selected 12D pre/post paths and the existing genuine associator:
  (A ⋆ C) ⋆ B
  alpha_P ; (A ⋆ (C ⋆ B)) ; alpha_Q⁻¹.
Their exact source and target are identical, but their RAW 13D proof
terms are provably distinct.

A fresh, independent SELECTED 13D context-closed presentation includes
the entire v5.28 proof Type and transports proofs through genuine
original 7D left/right whiskering, with matching old six-cell fibers.

A fresh SELECTED 14D presentation contains genuine v5.28/23 14D
evidence, and TWO local 14D naturality-square generators for the
actual original left and right triple-context critical pairs. The
selected 14D comparisons are closed under further typed seventh-cell
whiskering, reversal and concatenation. No general 14D square for an
arbitrary 13D proof is added.

The old v5.23 14D proof values embed with exact original 12D indices.
An explicit necessary old-12D-boundary criterion is disproved for the
new triple critical pairs using finite constructor observers, without
eliminating dependent seventh-cell indices. In particular NO lift to
an old raw 14D equality is claimed.

F55/P77/GK5CG, original 6D–14D, v5.23, v5.27 and v5.28 are untouched.
Append-only, same-root, no new axioms, no sorry.
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

/-- First genuine pasting of the selected thirteenth witness under
two arbitrary, composable selected twelfth boundary paths. -/
def selectedNaturalityDirect (l r : W)
    {E F G H : FramedEleven W l r}
    (A : SelectedUnitalCompositionTwelve W l r E F)
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    (C : SelectedTriplePastingThirteen W l r P Q)
    (B : SelectedUnitalCompositionTwelve W l r G H) :
    SelectedTriplePastingThirteen W l r
      (.chain (.chain A P) B)
      (.chain (.chain A Q) B) :=
  .append (.prepend A C) B

/-- Second genuine pasting, typed through BOTH existing 13D
associators. No raw equality of the differently bracketed 12D
endpoints is imposed. -/
def selectedNaturalityViaAssociators (l r : W)
    {E F G H : FramedEleven W l r}
    (A : SelectedUnitalCompositionTwelve W l r E F)
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    (C : SelectedTriplePastingThirteen W l r P Q)
    (B : SelectedUnitalCompositionTwelve W l r G H) :
    SelectedTriplePastingThirteen W l r
      (.chain (.chain A P) B)
      (.chain (.chain A Q) B) :=
  .chain (.associator A P B)
    (.chain (.prepend A (.append C B))
      (.reverse (.associator A Q B)))

/-- Finite 13D constructor observation proves that naturality is a
genuine coherence question, not definitional equality. -/
theorem selectedNaturality_rawDistinct (l r : W)
    {E F G H : FramedEleven W l r}
    (A : SelectedUnitalCompositionTwelve W l r E F)
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    (C : SelectedTriplePastingThirteen W l r P Q)
    (B : SelectedUnitalCompositionTwelve W l r G H) :
    selectedNaturalityDirect l r A C B ≠
      selectedNaturalityViaAssociators l r A C B := by
  intro h
  have ht := congrArg (selectedThirteenFirstAtomTag l r) h
  change (7 : Nat) = 8 at ht
  cases ht

/-- Separate proof-relevant 13D context closure. The inherited
constructor is faithful on RAW evidence; selected whiskering is only
allowed on exactly matching original six-cell boundaries. -/
inductive SelectedContextualThirteen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    SelectedUnitalCompositionTwelve W l r F G →
    SelectedUnitalCompositionTwelve W l r F G → Type uSix where
  | inherited {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      (C : SelectedTriplePastingThirteen W l r P Q) :
      SelectedContextualThirteen W l r P Q
  | whiskerLeft {w z : W}
      {b c d : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      (C : SelectedContextualThirteen W l r P Q) :
      SelectedContextualThirteen W l r
        (.whiskerLeft before F G P)
        (.whiskerLeft before F G Q)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      (C : SelectedContextualThirteen W l r P Q)
      (after : SevenRewrite W l r d e) :
      SelectedContextualThirteen W l r
        (.whiskerRight F G P after)
        (.whiskerRight F G Q after)
  | strict {F G : FramedEleven W l r}
      (P : SelectedUnitalCompositionTwelve W l r F G) :
      SelectedContextualThirteen W l r P P
  | reverse {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      (C : SelectedContextualThirteen W l r P Q) :
      SelectedContextualThirteen W l r Q P
  | chain {F G : FramedEleven W l r}
      {P Q R : SelectedUnitalCompositionTwelve W l r F G}
      (C : SelectedContextualThirteen W l r P Q)
      (D : SelectedContextualThirteen W l r Q R) :
      SelectedContextualThirteen W l r P R

theorem selectedContextual_inherited_injective (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G} :
    Function.Injective (fun C : SelectedTriplePastingThirteen W l r P Q =>
      SelectedContextualThirteen.inherited C) := by
  intro C D h
  cases h
  rfl

theorem selectedContextual_leftEvidence (l r : W) {w z : W}
    {b c d : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedTriplePastingThirteen W l r P Q) :
    Nonempty (SelectedContextualThirteen W l r
      (.whiskerLeft before F G P)
      (.whiskerLeft before F G Q)) :=
  ⟨.whiskerLeft before F G (.inherited C)⟩

theorem selectedContextual_rightEvidence (l r : W) {w z : W}
    {c d e : PentagonAdjoinedSixCell W l r w z}
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedTriplePastingThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    Nonempty (SelectedContextualThirteen W l r
      (.whiskerRight F G P after)
      (.whiskerRight F G Q after)) :=
  ⟨.whiskerRight F G (.inherited C) after⟩

/-- New selected 14D: old v5.28 comparison values are stored intact.
Only the two ACTUAL triple-context naturality-square families receive
new 14D generators, and contextual closure is explicitly chosen. -/
inductive SelectedNaturalityFourteen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    {P Q : SelectedUnitalCompositionTwelve W l r F G} →
    SelectedContextualThirteen W l r P Q →
    SelectedContextualThirteen W l r P Q → Type uSix where
  | inherited {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedTriplePastingThirteen W l r P Q}
      (V : SelectedTriplePastingFourteen W l r C D) :
      SelectedNaturalityFourteen W l r
        (.inherited C) (.inherited D)
  | localLeft {w z : W}
      {a b c d e : PentagonAdjoinedSixCell W l r w z}
      (u : SevenRewrite W l r a b)
      (v : SevenRewrite W l r b c)
      (t : SevenRewrite W l r c d)
      (F : ContextFrameEleven W l r d e)
      {E H : FramedEleven W l r}
      (A : SelectedUnitalCompositionTwelve W l r E
        (selectedLeftTripleSource l r u v t F))
      (B : SelectedUnitalCompositionTwelve W l r
        (selectedLeftTripleRightTarget l r u v t F) H) :
      SelectedNaturalityFourteen W l r
        (.inherited (selectedNaturalityDirect l r A
          (SelectedTriplePastingThirteen.tripleLeft u v t F) B))
        (.inherited (selectedNaturalityViaAssociators l r A
          (SelectedTriplePastingThirteen.tripleLeft u v t F) B))
  | localRight {w z : W}
      {a b c d e : PentagonAdjoinedSixCell W l r w z}
      (u : SevenRewrite W l r b c)
      (v : SevenRewrite W l r c d)
      (t : SevenRewrite W l r d e)
      (F : ContextFrameEleven W l r a b)
      {E H : FramedEleven W l r}
      (A : SelectedUnitalCompositionTwelve W l r E
        (selectedRightTripleSource l r u v t F))
      (B : SelectedUnitalCompositionTwelve W l r
        (selectedRightTripleRightTarget l r u v t F) H) :
      SelectedNaturalityFourteen W l r
        (.inherited (selectedNaturalityDirect l r A
          (SelectedTriplePastingThirteen.tripleRight u v t F) B))
        (.inherited (selectedNaturalityViaAssociators l r A
          (SelectedTriplePastingThirteen.tripleRight u v t F) B))
  | whiskerLeft {w z : W}
      {b c d : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      {C D : SelectedContextualThirteen W l r P Q}
      (V : SelectedNaturalityFourteen W l r C D) :
      SelectedNaturalityFourteen W l r
        (.whiskerLeft before F G C)
        (.whiskerLeft before F G D)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      {C D : SelectedContextualThirteen W l r P Q}
      (V : SelectedNaturalityFourteen W l r C D)
      (after : SevenRewrite W l r d e) :
      SelectedNaturalityFourteen W l r
        (.whiskerRight F G C after)
        (.whiskerRight F G D after)
  | strict {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      (C : SelectedContextualThirteen W l r P Q) :
      SelectedNaturalityFourteen W l r C C
  | reverse {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedContextualThirteen W l r P Q}
      (V : SelectedNaturalityFourteen W l r C D) :
      SelectedNaturalityFourteen W l r D C
  | chain {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D E : SelectedContextualThirteen W l r P Q}
      (V : SelectedNaturalityFourteen W l r C D)
      (X : SelectedNaturalityFourteen W l r D E) :
      SelectedNaturalityFourteen W l r C E

/-- Full earlier v5.28 14D history is embedded as a proof value. -/
def tripleFourteenToNaturality (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedTriplePastingThirteen W l r P Q}
    (V : SelectedTriplePastingFourteen W l r C D) :
    SelectedNaturalityFourteen W l r (.inherited C) (.inherited D) :=
  .inherited V

theorem tripleFourteenToNaturality_injective (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedTriplePastingThirteen W l r P Q} :
    Function.Injective (fun V : SelectedTriplePastingFourteen W l r C D =>
      tripleFourteenToNaturality l r V) := by
  intro V X h
  cases h
  rfl

/-- Two separate, genuine inclusions preserve a typed v5.23 14D
proof through v5.28 and then v5.29, with no proof rewriting. -/
def oldFourteenToNaturality (l r : W)
    {F G : FramedEleven W l r}
    {P Q : FramedDoubleWhiskerTwelveCell W l r F G}
    {C D : CompositionalWhiskerThirteen W l r P Q}
    (V : SelectedCompositionFourteen W l r C D) :
    SelectedNaturalityFourteen W l r
      (.inherited (originalThirteenToTriple l r C))
      (.inherited (originalThirteenToTriple l r D)) :=
  tripleFourteenToNaturality l r (originalFourteenToTriple l r V)

theorem oldFourteenToNaturality_injective (l r : W)
    {F G : FramedEleven W l r}
    {P Q : FramedDoubleWhiskerTwelveCell W l r F G}
    {C D : CompositionalWhiskerThirteen W l r P Q} :
    Function.Injective (fun V : SelectedCompositionFourteen W l r C D =>
      oldFourteenToNaturality l r V) := by
  intro V X h
  apply originalFourteenToTriple_injective l r
  apply tripleFourteenToNaturality_injective l r
  exact h

theorem selectedLocalLeft_naturality (l r : W) {w z : W}
    {a b c d e : PentagonAdjoinedSixCell W l r w z}
    (u : SevenRewrite W l r a b)
    (v : SevenRewrite W l r b c)
    (t : SevenRewrite W l r c d)
    (F : ContextFrameEleven W l r d e)
    {E H : FramedEleven W l r}
    (A : SelectedUnitalCompositionTwelve W l r E
      (selectedLeftTripleSource l r u v t F))
    (B : SelectedUnitalCompositionTwelve W l r
      (selectedLeftTripleRightTarget l r u v t F) H) :
    Nonempty (SelectedNaturalityFourteen W l r
      (.inherited (selectedNaturalityDirect l r A
        (SelectedTriplePastingThirteen.tripleLeft u v t F) B))
      (.inherited (selectedNaturalityViaAssociators l r A
        (SelectedTriplePastingThirteen.tripleLeft u v t F) B))) ∧
    selectedNaturalityDirect l r A
        (SelectedTriplePastingThirteen.tripleLeft u v t F) B ≠
      selectedNaturalityViaAssociators l r A
        (SelectedTriplePastingThirteen.tripleLeft u v t F) B :=
  ⟨⟨.localLeft u v t F A B⟩,
    selectedNaturality_rawDistinct l r A
      (SelectedTriplePastingThirteen.tripleLeft u v t F) B⟩

theorem selectedLocalRight_naturality (l r : W) {w z : W}
    {a b c d e : PentagonAdjoinedSixCell W l r w z}
    (u : SevenRewrite W l r b c)
    (v : SevenRewrite W l r c d)
    (t : SevenRewrite W l r d e)
    (F : ContextFrameEleven W l r a b)
    {E H : FramedEleven W l r}
    (A : SelectedUnitalCompositionTwelve W l r E
      (selectedRightTripleSource l r u v t F))
    (B : SelectedUnitalCompositionTwelve W l r
      (selectedRightTripleRightTarget l r u v t F) H) :
    Nonempty (SelectedNaturalityFourteen W l r
      (.inherited (selectedNaturalityDirect l r A
        (SelectedTriplePastingThirteen.tripleRight u v t F) B))
      (.inherited (selectedNaturalityViaAssociators l r A
        (SelectedTriplePastingThirteen.tripleRight u v t F) B))) ∧
    selectedNaturalityDirect l r A
        (SelectedTriplePastingThirteen.tripleRight u v t F) B ≠
      selectedNaturalityViaAssociators l r A
        (SelectedTriplePastingThirteen.tripleRight u v t F) B :=
  ⟨⟨.localRight u v t F A B⟩,
    selectedNaturality_rawDistinct l r A
      (SelectedTriplePastingThirteen.tripleRight u v t F) B⟩

/-- A selected 14D local comparison remains typed after any genuinely
matching original LEFT seventh-cell context action. -/
theorem selectedNaturality_leftStable (l r : W) {w z : W}
    {b c d : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedContextualThirteen W l r P Q}
    (V : SelectedNaturalityFourteen W l r C D) :
    Nonempty (SelectedNaturalityFourteen W l r
      (.whiskerLeft before F G C)
      (.whiskerLeft before F G D)) :=
  ⟨.whiskerLeft before F G V⟩

/-- Symmetric typed RIGHT seventh-cell context closure. -/
theorem selectedNaturality_rightStable (l r : W) {w z : W}
    {c d e : PentagonAdjoinedSixCell W l r w z}
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedContextualThirteen W l r P Q}
    (V : SelectedNaturalityFourteen W l r C D)
    (after : SevenRewrite W l r d e) :
    Nonempty (SelectedNaturalityFourteen W l r
      (.whiskerRight F G C after)
      (.whiskerRight F G D after)) :=
  ⟨.whiskerRight F G V after⟩

/-- Necessary (not sufficient) criterion for a v5.29 pair of 12D
boundaries to be the image of ACTUAL old v5.23 raw 12D proof values. -/
def HasOriginalTwelveEndpoints (l r : W)
    {F G : FramedEleven W l r}
    (P Q : SelectedUnitalCompositionTwelve W l r F G) : Prop :=
  ∃ (U V : FramedDoubleWhiskerTwelveCell W l r F G),
    originalFramedTwelveToSelected l r U = P ∧
    originalFramedTwelveToSelected l r V = Q

theorem oldFourteen_hasOriginalEndpoints (l r : W)
    {F G : FramedEleven W l r}
    {P Q : FramedDoubleWhiskerTwelveCell W l r F G}
    {C D : CompositionalWhiskerThirteen W l r P Q}
    (_V : SelectedCompositionFourteen W l r C D) :
    HasOriginalTwelveEndpoints l r
      (originalFramedTwelveToSelected l r P)
      (originalFramedTwelveToSelected l r Q) :=
  ⟨P, Q, rfl, rfl⟩

/-- The actual left triple 12D source starts with a whiskerLeft atom
(tag 4), whereas EVERY old 12D embedding starts with previous (1). -/
theorem selectedLeftTriple_noOldEndpoints (l r : W) {w z : W}
    {a b c d e : PentagonAdjoinedSixCell W l r w z}
    (u : SevenRewrite W l r a b)
    (v : SevenRewrite W l r b c)
    (t : SevenRewrite W l r c d)
    (F : ContextFrameEleven W l r d e) :
    ¬ HasOriginalTwelveEndpoints l r
      (selectedLeftTripleInnerPasting l r u v t F)
      (selectedLeftTripleDetour l r u v t F) := by
  intro h
  rcases h with ⟨U, V, hU, hV⟩
  have ht := congrArg (selectedTwelfthFirstAtomTag l r) hU
  change (1 : Nat) = 4 at ht
  cases ht

/-- Likewise the genuine right triple outer reduction starts with a
compRight atom (9), and cannot be a raw old embedded boundary (1). -/
theorem selectedRightTriple_noOldEndpoints (l r : W) {w z : W}
    {a b c d e : PentagonAdjoinedSixCell W l r w z}
    (u : SevenRewrite W l r b c)
    (v : SevenRewrite W l r c d)
    (t : SevenRewrite W l r d e)
    (F : ContextFrameEleven W l r a b) :
    ¬ HasOriginalTwelveEndpoints l r
      (selectedRightTripleOuterPasting l r u v t F)
      (selectedRightTripleDetour l r u v t F) := by
  intro h
  rcases h with ⟨U, V, hU, hV⟩
  have ht := congrArg (selectedTwelfthFirstAtomTag l r) hU
  change (1 : Nat) = 9 at ht
  cases ht

/-- A local naturality square at the new selected 14D level is not
soundly interpretable as equality of the underlying proof-relevant
13D syntax. -/
theorem selectedLocalLeft_noRawEqualityInterpreter (l r : W) {w z : W}
    {a b c d e : PentagonAdjoinedSixCell W l r w z}
    (u : SevenRewrite W l r a b)
    (v : SevenRewrite W l r b c)
    (t : SevenRewrite W l r c d)
    (F : ContextFrameEleven W l r d e)
    {E H : FramedEleven W l r}
    (A : SelectedUnitalCompositionTwelve W l r E
      (selectedLeftTripleSource l r u v t F))
    (B : SelectedUnitalCompositionTwelve W l r
      (selectedLeftTripleRightTarget l r u v t F) H) :
    ¬ (∀
      (C D : SelectedContextualThirteen W l r
        (.chain (.chain A (selectedLeftTripleInnerPasting l r u v t F)) B)
        (.chain (.chain A (selectedLeftTripleDetour l r u v t F)) B)),
      SelectedNaturalityFourteen W l r C D → C = D) := by
  intro interpret
  have h := interpret _ _ (SelectedNaturalityFourteen.localLeft u v t F A B)
  have h' := selectedContextual_inherited_injective l r h
  exact selectedNaturality_rawDistinct l r A
    (SelectedTriplePastingThirteen.tripleLeft u v t F) B h'

#print axioms PentagonAdjoinedSixCell.selectedNaturalityDirect
#print axioms PentagonAdjoinedSixCell.selectedNaturalityViaAssociators
#print axioms PentagonAdjoinedSixCell.selectedNaturality_rawDistinct
#print axioms PentagonAdjoinedSixCell.SelectedContextualThirteen
#print axioms PentagonAdjoinedSixCell.selectedContextual_inherited_injective
#print axioms PentagonAdjoinedSixCell.selectedContextual_leftEvidence
#print axioms PentagonAdjoinedSixCell.selectedContextual_rightEvidence
#print axioms PentagonAdjoinedSixCell.SelectedNaturalityFourteen
#print axioms PentagonAdjoinedSixCell.tripleFourteenToNaturality
#print axioms PentagonAdjoinedSixCell.tripleFourteenToNaturality_injective
#print axioms PentagonAdjoinedSixCell.oldFourteenToNaturality
#print axioms PentagonAdjoinedSixCell.oldFourteenToNaturality_injective
#print axioms PentagonAdjoinedSixCell.selectedLocalLeft_naturality
#print axioms PentagonAdjoinedSixCell.selectedLocalRight_naturality
#print axioms PentagonAdjoinedSixCell.selectedNaturality_leftStable
#print axioms PentagonAdjoinedSixCell.selectedNaturality_rightStable
#print axioms PentagonAdjoinedSixCell.HasOriginalTwelveEndpoints
#print axioms PentagonAdjoinedSixCell.oldFourteen_hasOriginalEndpoints
#print axioms PentagonAdjoinedSixCell.selectedLeftTriple_noOldEndpoints
#print axioms PentagonAdjoinedSixCell.selectedRightTriple_noOldEndpoints
#print axioms PentagonAdjoinedSixCell.selectedLocalLeft_noRawEqualityInterpreter

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
