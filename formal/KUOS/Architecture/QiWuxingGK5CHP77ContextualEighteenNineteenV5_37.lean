import KUOS.Architecture.QiWuxingGK5CHP77OuterSwapEighteenQuotientV5_36

/-!
Qi v5.37 — exact seventh-context closure of actual selected 18D
proofs, fine trace descent and a deliberately LOCAL selected 19D
unit-pasting comparison.

The original v5.35 local 18D Type-valued proofs are embedded as raw
constructors of an INDEPENDENT new 18D context-closed presentation.
Only ACTUAL matching original 7D boundaries permit left/right
whiskering. All six constructors preserve the complete ordered
outer 17D context trace, which therefore descends through a new
exact-fiber quotient. The two genuinely old 18D unit comparisons
still identify distinct raw 17D first tags only at quotient level.

On raw context-closed 18D proof SYNTAX, the ordered history of
external seventh-cell whiskerings is independently observed.
Two local 19D unit-pasting generators compare an inherited old
18D witness with insertion of a strict 18D identity on its left
or right. They act ONLY at exactly matching 17D endpoints and
are closed by strict, reverse and chain. Their quotient preserves
the full outer 18D trace but cannot preserve the first constructor
tag, because the old Type-valued inherited term and the newly
unit-pasted term are raw-distinct.

No heterogeneous 18D interchange, cross-fiber 19D gluing, raw
proof equality, unconditional mixed coherence, or silent
strengthening of observation-level swap authority is asserted.
All original F55/P77/GK5CG, original 6D–14D and prior independent
selected proofs through v5.36 are unchanged.
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

/-- Separate contextual presentation for genuine v5.35 selected 18D
proof values. No heterogeneous source equality is imposed. -/
inductive SelectedContextualEighteen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    {P Q : SelectedUnitalCompositionTwelve W l r F G} →
    {C D : SelectedMixedInterchangerThirteen W l r P Q} →
    {V X : SelectedMixedNaturalityFourteen W l r C D} →
    {T U : SelectedContextualFifteen W l r V X} →
    {H K : SelectedContextualSixteen W l r T U} →
    SelectedContextualSeventeen W l r H K →
    SelectedContextualSeventeen W l r H K → Type uSix where
  | inherited {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      {J N : SelectedContextualSeventeen W l r H K}
      (M : SelectedLocalEighteen W l r J N) :
      SelectedContextualEighteen W l r J N
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
      {J N : SelectedContextualSeventeen W l r H K}
      (M : SelectedContextualEighteen W l r J N) :
      SelectedContextualEighteen W l r
        (.whiskerLeft before F G J)
        (.whiskerLeft before F G N)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (F G : ContextFrameEleven W l r c d)
      {P Q : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      {J N : SelectedContextualSeventeen W l r H K}
      (M : SelectedContextualEighteen W l r J N)
      (after : SevenRewrite W l r d e) :
      SelectedContextualEighteen W l r
        (.whiskerRight F G J after)
        (.whiskerRight F G N after)
  | strict {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      (J : SelectedContextualSeventeen W l r H K) :
      SelectedContextualEighteen W l r J J
  | reverse {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      {J N : SelectedContextualSeventeen W l r H K}
      (M : SelectedContextualEighteen W l r J N) :
      SelectedContextualEighteen W l r N J
  | chain {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      {J N S : SelectedContextualSeventeen W l r H K}
      (M : SelectedContextualEighteen W l r J N)
      (L : SelectedContextualEighteen W l r N S) :
      SelectedContextualEighteen W l r J S

/-- Preserve every previous true selected 18D proof as an unmodified
dependent value under a new, injective constructor. -/
def oldEighteenToContextual (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .inherited M

theorem oldEighteenToContextual_injective (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K} :
    Function.Injective (fun M : SelectedLocalEighteen W l r J N =>
      oldEighteenToContextual l r M) := by
  intro M L h
  cases h
  rfl

/-- True left contextual stability requires matching original
seven-cell boundaries and BOTH actual 17D endpoints. -/
theorem selectedContextualEighteen_leftStable (l r : W) {w z : W}
    {b c d : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    Nonempty (SelectedContextualEighteen W l r
      (.whiskerLeft before F G J) (.whiskerLeft before F G N)) :=
  ⟨.whiskerLeft before F G M⟩

theorem selectedContextualEighteen_rightStable (l r : W) {w z : W}
    {c d e : PentagonAdjoinedSixCell W l r w z}
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N)
    (after : SevenRewrite W l r d e) :
    Nonempty (SelectedContextualEighteen W l r
      (.whiskerRight F G J after) (.whiskerRight F G N after)) :=
  ⟨.whiskerRight F G M after⟩

/-- All SIX genuine 18D context-closed constructors preserve the
ordered exterior raw 17D trace, not only event counts. -/
theorem selectedContextualEighteen_preservesSeventeenTrace (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextSeventeenTrace l r J =
      selectedContextSeventeenTrace l r N := by
  induction M with
  | inherited M => exact selectedEighteen_preservesSeventeenTrace l r M
  | whiskerLeft before F G M ih =>
      exact congrArg (List.cons false) ih
  | whiskerRight F G M after ih =>
      exact congrArg (List.cons true) ih
  | strict J => rfl
  | reverse M ih => exact ih.symm
  | chain M L ih ih' => exact ih.trans ih'

/-- New exact-fiber contextual 18D quotient, NOT the older v5.36
local 18D quotient and NOT the observation-only swap quotient. -/
def selectedContextEighteenSetoid (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H K : SelectedContextualSixteen W l r T U) :
    Setoid (SelectedContextualSeventeen W l r H K) where
  r := fun J N => Nonempty (SelectedContextualEighteen W l r J N)
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

def selectedContextEighteenClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedContextEighteenSetoid l r H K) :=
  Quotient.mk _ J

theorem selectedContextEighteenClass_eq_iff (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenClass l r J =
      selectedContextEighteenClass l r N ↔
        Nonempty (SelectedContextualEighteen W l r J N) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- Complete ordered raw 17D context history descends through the
new contextual 18D quotient by a proved compatibility equation. -/
def selectedContextEighteenTraceOnQuotient (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H K : SelectedContextualSixteen W l r T U) :
    Quotient (selectedContextEighteenSetoid l r H K) → List Bool :=
  Quotient.lift (selectedContextSeventeenTrace l r) (by
    intro J N h
    rcases h with ⟨M⟩
    exact selectedContextualEighteen_preservesSeventeenTrace l r M)

theorem selectedContextEighteenTrace_onClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenTraceOnQuotient l r H K
        (selectedContextEighteenClass l r J) =
      selectedContextSeventeenTrace l r J :=
  rfl

/-- Ordered external 7D context history of the raw 18D PROOF term
itself; old inherited 18D Type values remain intact. -/
def selectedContextEighteenTrace (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) : List Bool :=
  match M with
  | .inherited _ => []
  | .whiskerLeft _ _ _ M => false :: selectedContextEighteenTrace l r M
  | .whiskerRight _ _ M _ => true :: selectedContextEighteenTrace l r M
  | .strict _ => []
  | .reverse M => selectedContextEighteenTrace l r M
  | .chain M L =>
      selectedContextEighteenTrace l r M ++ selectedContextEighteenTrace l r L

/-- Tag only the topmost raw 18D constructor. It is not a global
invariant and must NOT be silently quotiented. -/
def selectedContextEighteenTopTag (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) : Nat :=
  match M with
  | .inherited _ => 0
  | .whiskerLeft _ _ _ _ => 1
  | .whiskerRight _ _ _ _ => 2
  | .strict _ => 3
  | .reverse _ => 4
  | .chain _ _ => 5

/-- Independent selected 19D coherence, restricted to unit
pasting of ACTUAL old selected 18D evidence in ONE exact 17D fiber.
No mixed or heterogeneous 19D exchange generator is introduced. -/
inductive SelectedLocalNineteen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    {P Q : SelectedUnitalCompositionTwelve W l r F G} →
    {C D : SelectedMixedInterchangerThirteen W l r P Q} →
    {V X : SelectedMixedNaturalityFourteen W l r C D} →
    {T U : SelectedContextualFifteen W l r V X} →
    {H K : SelectedContextualSixteen W l r T U} →
    {J N : SelectedContextualSeventeen W l r H K} →
    SelectedContextualEighteen W l r J N →
    SelectedContextualEighteen W l r J N → Type uSix where
  | strict {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      {J N : SelectedContextualSeventeen W l r H K}
      (M : SelectedContextualEighteen W l r J N) :
      SelectedLocalNineteen W l r M M
  | unitPrepend {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      {J N : SelectedContextualSeventeen W l r H K}
      (M : SelectedLocalEighteen W l r J N) :
      SelectedLocalNineteen W l r
        (.chain (.strict J) (.inherited M))
        (.inherited M)
  | unitAppend {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      {J N : SelectedContextualSeventeen W l r H K}
      (M : SelectedLocalEighteen W l r J N) :
      SelectedLocalNineteen W l r
        (.chain (.inherited M) (.strict N))
        (.inherited M)
  | reverse {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      {J N : SelectedContextualSeventeen W l r H K}
      {M L : SelectedContextualEighteen W l r J N}
      (A : SelectedLocalNineteen W l r M L) :
      SelectedLocalNineteen W l r L M
  | chain {F G : FramedEleven W l r}
      {P Q : SelectedUnitalCompositionTwelve W l r F G}
      {C D : SelectedMixedInterchangerThirteen W l r P Q}
      {V X : SelectedMixedNaturalityFourteen W l r C D}
      {T U : SelectedContextualFifteen W l r V X}
      {H K : SelectedContextualSixteen W l r T U}
      {J N : SelectedContextualSeventeen W l r H K}
      {M L S : SelectedContextualEighteen W l r J N}
      (A : SelectedLocalNineteen W l r M L)
      (B : SelectedLocalNineteen W l r L S) :
      SelectedLocalNineteen W l r M S

/-- Unit pasting does not add an exterior seventh-cell event.
Every selected 19D constructor respects the FULL raw 18D trace. -/
theorem selectedLocalNineteen_preservesEighteenTrace (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenTrace l r M =
      selectedContextEighteenTrace l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- Exact-fiber 19D quotient: source 18D terms remain available,
and only actual selected 19D proof comparisons are used. -/
def selectedNineteenSetoid (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J N : SelectedContextualSeventeen W l r H K) :
    Setoid (SelectedContextualEighteen W l r J N) where
  r := fun M L => Nonempty (SelectedLocalNineteen W l r M L)
  iseqv := by
    constructor
    · intro M
      exact ⟨.strict M⟩
    · intro M L h
      rcases h with ⟨A⟩
      exact ⟨.reverse A⟩
    · intro M L S h h'
      rcases h with ⟨A⟩
      rcases h' with ⟨B⟩
      exact ⟨.chain A B⟩

def selectedNineteenClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    Quotient (selectedNineteenSetoid l r J N) :=
  Quotient.mk _ M

theorem selectedNineteenClass_eq_iff (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M L : SelectedContextualEighteen W l r J N) :
    selectedNineteenClass l r M = selectedNineteenClass l r L ↔
      Nonempty (SelectedLocalNineteen W l r M L) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- Fine ordered 18D source context trace descends through 19D
unit coherence, by a genuine proof for every grammar constructor. -/
def selectedNineteenTraceOnQuotient (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → List Bool :=
  Quotient.lift (selectedContextEighteenTrace l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesEighteenTrace l r A)

theorem selectedNineteenTrace_onClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenTraceOnQuotient l r J N
        (selectedNineteenClass l r M) =
      selectedContextEighteenTrace l r M :=
  rfl

/-- The chosen 19D left unit comparison identifies a real
inherited 18D value and its strict-left pasting, not their raw Eq. -/
theorem selectedNineteenUnitPrepend_classEq (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    selectedNineteenClass l r
        (SelectedContextualEighteen.chain
          (SelectedContextualEighteen.strict J) (.inherited M)) =
      selectedNineteenClass l r (.inherited M) :=
  Quotient.sound ⟨.unitPrepend M⟩

theorem selectedNineteenUnitAppend_classEq (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    selectedNineteenClass l r
        (SelectedContextualEighteen.chain
          (.inherited M) (SelectedContextualEighteen.strict N)) =
      selectedNineteenClass l r (.inherited M) :=
  Quotient.sound ⟨.unitAppend M⟩

/-- The new selected 19D left unit critical pair is raw-distinct
because its visible top constructors are chain (5) and inherited (0). -/
theorem selectedNineteenUnitPrepend_rawDistinct (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    (SelectedContextualEighteen.chain
        (SelectedContextualEighteen.strict J) (.inherited M)) ≠
      (SelectedContextualEighteen.inherited M) := by
  intro h
  have ht := congrArg (selectedContextEighteenTopTag l r) h
  change (5 : Nat) = 0 at ht
  cases ht

/-- Source 18D term equality cannot be reconstructed from even
the strictest exact-fiber selected 19D unit comparison. -/
theorem selectedNineteen_noRawEqualityInterpreter (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    ¬ (∀ A B : SelectedContextualEighteen W l r J N,
      SelectedLocalNineteen W l r A B → A = B) := by
  intro interpret
  exact selectedNineteenUnitPrepend_rawDistinct l r M
    (interpret _ _ (.unitPrepend M))

/-- The top raw constructor tag does not descend through this 19D
quotient: the quotient identifies 5 and 0, not their raw values. -/
theorem selectedNineteen_noTopTagDescent (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    ¬ (∃ g : Quotient (selectedNineteenSetoid l r J N) → Nat,
      ∀ A : SelectedContextualEighteen W l r J N,
        g (selectedNineteenClass l r A) =
          selectedContextEighteenTopTag l r A) := by
  rintro ⟨g, hg⟩
  have ht : selectedContextEighteenTopTag l r
      (SelectedContextualEighteen.chain
        (SelectedContextualEighteen.strict J) (.inherited M)) =
    selectedContextEighteenTopTag l r
      (SelectedContextualEighteen.inherited M) := by
    calc
      _ = g (selectedNineteenClass l r
          (SelectedContextualEighteen.chain
            (SelectedContextualEighteen.strict J) (.inherited M))) :=
        (hg _).symm
      _ = g (selectedNineteenClass l r
          (SelectedContextualEighteen.inherited M)) :=
        congrArg g (selectedNineteenUnitPrepend_classEq l r M)
      _ = _ := hg _
  change (5 : Nat) = 0 at ht
  cases ht

#print axioms PentagonAdjoinedSixCell.SelectedContextualEighteen
#print axioms PentagonAdjoinedSixCell.oldEighteenToContextual
#print axioms PentagonAdjoinedSixCell.oldEighteenToContextual_injective
#print axioms PentagonAdjoinedSixCell.selectedContextualEighteen_leftStable
#print axioms PentagonAdjoinedSixCell.selectedContextualEighteen_rightStable
#print axioms PentagonAdjoinedSixCell.selectedContextualEighteen_preservesSeventeenTrace
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenSetoid
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenClass
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenClass_eq_iff
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenTraceOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenTrace_onClass
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenTrace
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenTopTag
#print axioms PentagonAdjoinedSixCell.SelectedLocalNineteen
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesEighteenTrace
#print axioms PentagonAdjoinedSixCell.selectedNineteenSetoid
#print axioms PentagonAdjoinedSixCell.selectedNineteenClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenClass_eq_iff
#print axioms PentagonAdjoinedSixCell.selectedNineteenTraceOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedNineteenTrace_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenUnitPrepend_classEq
#print axioms PentagonAdjoinedSixCell.selectedNineteenUnitAppend_classEq
#print axioms PentagonAdjoinedSixCell.selectedNineteenUnitPrepend_rawDistinct
#print axioms PentagonAdjoinedSixCell.selectedNineteen_noRawEqualityInterpreter
#print axioms PentagonAdjoinedSixCell.selectedNineteen_noTopTagDescent

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
