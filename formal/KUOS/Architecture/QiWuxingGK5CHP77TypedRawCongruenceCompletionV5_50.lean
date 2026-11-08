import KUOS.Architecture.QiWuxingGK5CHP77ContextCongruenceGatesV5_49

/-!
Qi v5.50 — independent free typed raw-context congruence completion
of the ORIGINAL selected19 comparison in a fixed original sixteenth
fiber, including all typed seventeenth endpoints.

The old selected19 proof Type, its quotient, all original 18D proof
constructors and its raw-context non-descent obstructions are UNCHANGED.
A different, explicitly named 19D presentation is freely generated
from actual original 19D comparisons together with contextual raw
reverse, raw left-chain and raw right-chain stability.

Its new quotient admits typed reverse and binary raw chain descent;
an old->new quotient map is onto, but is NOT injective in each fiber
equipped with an actual old18 proof witness at its reverse endpoints.
No assertion is made about full 7D whiskering, global coherence, or
existence of raw proofs in every fiber.

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

/-- A SEPARATE Type-valued congruence presentation, NOT a modification
or alias of the original selected19 comparison. All constructors
preserve genuine dependent 17D boundaries. -/
inductive SelectedRawCongruentNineteen
    (W : Type uSix) (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U} :
    (J N : SelectedContextualSeventeen W l r H K) →
    SelectedContextualEighteen W l r J N →
    SelectedContextualEighteen W l r J N → Type uSix where
  | inherited {J N : SelectedContextualSeventeen W l r H K}
      {M L : SelectedContextualEighteen W l r J N}
      (A : SelectedLocalNineteen W l r M L) :
      SelectedRawCongruentNineteen W l r J N M L
  | strict {J N : SelectedContextualSeventeen W l r H K}
      (M : SelectedContextualEighteen W l r J N) :
      SelectedRawCongruentNineteen W l r J N M M
  | reverse {J N : SelectedContextualSeventeen W l r H K}
      {M L : SelectedContextualEighteen W l r J N}
      (A : SelectedRawCongruentNineteen W l r J N M L) :
      SelectedRawCongruentNineteen W l r J N L M
  | chain {J N : SelectedContextualSeventeen W l r H K}
      {M L S : SelectedContextualEighteen W l r J N}
      (A : SelectedRawCongruentNineteen W l r J N M L)
      (B : SelectedRawCongruentNineteen W l r J N L S) :
      SelectedRawCongruentNineteen W l r J N M S
  | rawReverse {J N : SelectedContextualSeventeen W l r H K}
      {M L : SelectedContextualEighteen W l r J N}
      (A : SelectedRawCongruentNineteen W l r J N M L) :
      SelectedRawCongruentNineteen W l r N J
        (SelectedContextualEighteen.reverse M)
        (SelectedContextualEighteen.reverse L)
  | rawChainRight {J N S : SelectedContextualSeventeen W l r H K}
      {M L : SelectedContextualEighteen W l r J N}
      (A : SelectedRawCongruentNineteen W l r J N M L)
      (X : SelectedContextualEighteen W l r N S) :
      SelectedRawCongruentNineteen W l r J S
        (SelectedContextualEighteen.chain M X)
        (SelectedContextualEighteen.chain L X)
  | rawChainLeft {J N S : SelectedContextualSeventeen W l r H K}
      (X : SelectedContextualEighteen W l r J N)
      {M L : SelectedContextualEighteen W l r N S}
      (A : SelectedRawCongruentNineteen W l r N S M L) :
      SelectedRawCongruentNineteen W l r J S
        (SelectedContextualEighteen.chain X M)
        (SelectedContextualEighteen.chain X L)

section FreeClosure

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}

/-- The original comparison maps to the NEW Type-valued family. -/
def selectedRawCongruent_inherit
    {J N : SelectedContextualSeventeen W l r H K}
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    SelectedRawCongruentNineteen W l r J N M L :=
  .inherited A

/-- The smallest independent context-closed equivalence is certified
by induction into EVERY relation that retains original comparisons,
equivalence, and the three specified raw-context operations.
This is a universal *minimality* certificate, not a global
faithfulness or a new equation in the old presentation. -/
theorem selectedRawCongruent_minimal
    (R : ∀ J N : SelectedContextualSeventeen W l r H K,
      SelectedContextualEighteen W l r J N →
      SelectedContextualEighteen W l r J N → Prop)
    (hOld : ∀ {J N : SelectedContextualSeventeen W l r H K}
      {M L : SelectedContextualEighteen W l r J N},
      SelectedLocalNineteen W l r M L → R J N M L)
    (hRefl : ∀ {J N : SelectedContextualSeventeen W l r H K}
      (M : SelectedContextualEighteen W l r J N), R J N M M)
    (hSymm : ∀ {J N : SelectedContextualSeventeen W l r H K}
      {M L : SelectedContextualEighteen W l r J N},
      R J N M L → R J N L M)
    (hTrans : ∀ {J N : SelectedContextualSeventeen W l r H K}
      {M L S : SelectedContextualEighteen W l r J N},
      R J N M L → R J N L S → R J N M S)
    (hRawReverse : ∀ {J N : SelectedContextualSeventeen W l r H K}
      {M L : SelectedContextualEighteen W l r J N},
      R J N M L →
        R N J (SelectedContextualEighteen.reverse M)
              (SelectedContextualEighteen.reverse L))
    (hRawRight : ∀ {J N S : SelectedContextualSeventeen W l r H K}
      {M L : SelectedContextualEighteen W l r J N},
      R J N M L → (X : SelectedContextualEighteen W l r N S) →
        R J S (SelectedContextualEighteen.chain M X)
              (SelectedContextualEighteen.chain L X))
    (hRawLeft : ∀ {J N S : SelectedContextualSeventeen W l r H K}
      (X : SelectedContextualEighteen W l r J N)
      {M L : SelectedContextualEighteen W l r N S},
      R N S M L →
        R J S (SelectedContextualEighteen.chain X M)
              (SelectedContextualEighteen.chain X L))
    {J N : SelectedContextualSeventeen W l r H K}
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    R J N M L := by
  induction A with
  | inherited A => exact hOld A
  | strict M => exact hRefl M
  | reverse A ih => exact hSymm ih
  | chain A B ih ih' => exact hTrans ih ih'
  | rawReverse A ih => exact hRawReverse ih
  | rawChainRight A X ih => exact hRawRight ih X
  | rawChainLeft X A ih => exact hRawLeft X ih

/-- A new exact-fiber quotient. It is NOT the previous selected19
quotient; the latter can distinguish presentations collapsed here. -/
def selectedRawCongruentSetoid
    (J N : SelectedContextualSeventeen W l r H K) :
    Setoid (SelectedContextualEighteen W l r J N) where
  r := fun M L => Nonempty (SelectedRawCongruentNineteen W l r J N M L)
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

def selectedRawCongruentClass
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    Quotient (selectedRawCongruentSetoid l r J N) :=
  Quotient.mk _ M

/-- The free congruence quotient identifies ONLY what the new
Type-valued grammar supports, no implicit global gluing. -/
theorem selectedRawCongruentClass_eq_iff
    {J N : SelectedContextualSeventeen W l r H K}
    (M L : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r M =
      selectedRawCongruentClass l r L ↔
        Nonempty (SelectedRawCongruentNineteen W l r J N M L) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- The ORIGINAL quotient projects onto the separate context-closed
quotient; the original proof values are preserved in the source. -/
def selectedRawCongruentProject
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) →
    Quotient (selectedRawCongruentSetoid l r J N) :=
  Quotient.lift
    (selectedRawCongruentClass l r)
    (by
      intro M L h
      rcases h with ⟨A⟩
      exact Quotient.sound ⟨.inherited A⟩)

theorem selectedRawCongruentProject_onClass
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentProject l r J N (selectedNineteenClass l r M) =
      selectedRawCongruentClass l r M :=
  rfl

theorem selectedRawCongruentProject_surjective
    (J N : SelectedContextualSeventeen W l r H K) :
    Function.Surjective (selectedRawCongruentProject l r J N) := by
  intro q
  induction q using Quotient.inductionOn with
  | _ M =>
      exact ⟨selectedNineteenClass l r M, rfl⟩

/-- Raw reverse now genuinely descends to the SEPARATE completion;
unlike the original selected19 quotient no raw reverse congruence
is assumed or inferred silently. -/
def selectedRawCongruentReverse
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
    Quotient (selectedRawCongruentSetoid l r N J) :=
  Quotient.lift
    (fun M => selectedRawCongruentClass l r
      (SelectedContextualEighteen.reverse M))
    (by
      intro M L h
      rcases h with ⟨A⟩
      exact Quotient.sound ⟨.rawReverse A⟩)

theorem selectedRawCongruentReverse_onClass
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentReverse l r J N
        (selectedRawCongruentClass l r M) =
      selectedRawCongruentClass l r (SelectedContextualEighteen.reverse M) :=
  rfl

/-- Binary typed raw chain descends in BOTH arguments, precisely
because we freely adjoined distinct left and right chain congruence
generators. No cross-17D whiskering is added. -/
def selectedRawCongruentChain
    (J N S : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
    Quotient (selectedRawCongruentSetoid l r N S) →
    Quotient (selectedRawCongruentSetoid l r J S) :=
  Quotient.lift
    (fun M =>
      Quotient.lift
        (fun X => selectedRawCongruentClass l r
          (SelectedContextualEighteen.chain M X))
        (by
          intro X Y h
          rcases h with ⟨A⟩
          exact Quotient.sound ⟨.rawChainLeft M A⟩))
    (by
      intro M L h
      rcases h with ⟨A⟩
      funext q
      induction q using Quotient.inductionOn with
      | _ X =>
          exact Quotient.sound ⟨.rawChainRight A X⟩)

theorem selectedRawCongruentChain_onClass
    {J N S : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N)
    (X : SelectedContextualEighteen W l r N S) :
    selectedRawCongruentChain l r J N S
        (selectedRawCongruentClass l r M)
        (selectedRawCongruentClass l r X) =
      selectedRawCongruentClass l r (SelectedContextualEighteen.chain M X) :=
  rfl

/-- Old 19D cannot perform this comparison; the new independent
comparison is an actual, typed contextual certificate. -/
def selectedRawCongruent_reverseUnitComparison
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    SelectedRawCongruentNineteen W l r N J
      (SelectedContextualEighteen.reverse
        (selectedNineteenDirectUnitRaw l r M .prepend))
      (SelectedContextualEighteen.reverse
        (selectedNineteenDirectUnitRaw l r M .inherited)) :=
  .rawReverse (.inherited (selectedNineteenDirectUnitComparison l r M
    .prepend .inherited))

def selectedRawCongruent_rightStrictUnitComparison
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    SelectedRawCongruentNineteen W l r J N
      (selectedNineteenRawRightStrict l r
        (selectedNineteenDirectUnitRaw l r M .prepend))
      (selectedNineteenRawRightStrict l r
        (selectedNineteenDirectUnitRaw l r M .inherited)) :=
  .rawChainRight
    (.inherited (selectedNineteenDirectUnitComparison l r M
      .prepend .inherited))
    (SelectedContextualEighteen.strict N)

def selectedRawCongruent_leftStrictUnitComparison
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    SelectedRawCongruentNineteen W l r J N
      (selectedNineteenRawLeftStrict l r
        (selectedNineteenDirectUnitRaw l r M .prepend))
      (selectedNineteenRawLeftStrict l r
        (selectedNineteenDirectUnitRaw l r M .inherited)) :=
  .rawChainLeft
    (SelectedContextualEighteen.strict J)
    (.inherited (selectedNineteenDirectUnitComparison l r M
      .prepend .inherited))

/-- The new completion LOSES original selected19 class distinctions:
the old non-descent witness is now identified after raw reverse. -/
theorem selectedRawCongruentProject_noninjective_reverse
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    ¬ Function.Injective (selectedRawCongruentProject l r N J) := by
  intro hinj
  have hNew :
      selectedRawCongruentProject l r N J
          (selectedNineteenClass l r
            (SelectedContextualEighteen.reverse
              (selectedNineteenDirectUnitRaw l r M .prepend))) =
        selectedRawCongruentProject l r N J
          (selectedNineteenClass l r
            (SelectedContextualEighteen.reverse
              (selectedNineteenDirectUnitRaw l r M .inherited))) := by
    change selectedRawCongruentClass l r
        (SelectedContextualEighteen.reverse
          (selectedNineteenDirectUnitRaw l r M .prepend)) =
      selectedRawCongruentClass l r
        (SelectedContextualEighteen.reverse
          (selectedNineteenDirectUnitRaw l r M .inherited))
    exact Quotient.sound ⟨selectedRawCongruent_reverseUnitComparison l r M⟩
  have hOld := hinj hNew
  exact selectedNineteenRawReverse_unitObstruction l r M
    (Quotient.exact hOld)

/-- Right-chain context also witnesses strict coarsening. -/
theorem selectedRawCongruentProject_noninjective_right
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    ¬ Function.Injective (selectedRawCongruentProject l r J N) := by
  intro hinj
  have hNew :
      selectedRawCongruentProject l r J N
          (selectedNineteenClass l r
            (selectedNineteenRawRightStrict l r
              (selectedNineteenDirectUnitRaw l r M .prepend))) =
        selectedRawCongruentProject l r J N
          (selectedNineteenClass l r
            (selectedNineteenRawRightStrict l r
              (selectedNineteenDirectUnitRaw l r M .inherited))) := by
    change selectedRawCongruentClass l r
        (selectedNineteenRawRightStrict l r
          (selectedNineteenDirectUnitRaw l r M .prepend)) =
      selectedRawCongruentClass l r
        (selectedNineteenRawRightStrict l r
          (selectedNineteenDirectUnitRaw l r M .inherited))
    exact Quotient.sound ⟨selectedRawCongruent_rightStrictUnitComparison l r M⟩
  have hOld := hinj hNew
  exact selectedNineteenRawRightStrict_unitObstruction l r M
    (Quotient.exact hOld)

/-- Left-chain context also witnesses strict coarsening. -/
theorem selectedRawCongruentProject_noninjective_left
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    ¬ Function.Injective (selectedRawCongruentProject l r J N) := by
  intro hinj
  have hNew :
      selectedRawCongruentProject l r J N
          (selectedNineteenClass l r
            (selectedNineteenRawLeftStrict l r
              (selectedNineteenDirectUnitRaw l r M .prepend))) =
        selectedRawCongruentProject l r J N
          (selectedNineteenClass l r
            (selectedNineteenRawLeftStrict l r
              (selectedNineteenDirectUnitRaw l r M .inherited))) := by
    change selectedRawCongruentClass l r
        (selectedNineteenRawLeftStrict l r
          (selectedNineteenDirectUnitRaw l r M .prepend)) =
      selectedRawCongruentClass l r
        (selectedNineteenRawLeftStrict l r
          (selectedNineteenDirectUnitRaw l r M .inherited))
    exact Quotient.sound ⟨selectedRawCongruent_leftStrictUnitComparison l r M⟩
  have hOld := hinj hNew
  exact selectedNineteenRawLeftStrict_unitObstruction l r M
    (Quotient.exact hOld)

end FreeClosure

#print axioms PentagonAdjoinedSixCell.SelectedRawCongruentNineteen
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_inherit
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_minimal
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentSetoid
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentClass
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentClass_eq_iff
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentProject
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentProject_onClass
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentProject_surjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverse
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverse_onClass
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentChain
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentChain_onClass
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_reverseUnitComparison
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_rightStrictUnitComparison
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_leftStrictUnitComparison
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentProject_noninjective_reverse
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentProject_noninjective_right
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentProject_noninjective_left

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
