import KUOS.Architecture.QiWuxingGK5CHP77TypedNineteenBoundaryTransportV5_39

/-!
Qi v5.40 — rigorous separation of mere cross-fiber boundary
EXISTENCE from the faithfulness of 19D comparison transport.

The conditional v5.39 boundary structure permits a degenerate
constant raw transport: for each genuine original 18D witness,
the selected RL witness is available, and every local 19D
comparison can be sent to its actual strict identity. Therefore
the v5.39 anchored boundary is inhabited in this precise, purely
CONSTANT, information-erasing sense. This is NOT a genuine faithful
dependent exchange or an original heterogeneous 20D cell.

For the actual LR witness, construct a second raw 18D witness
in the SAME source fiber by explicit chain/reverse/chain.
Its ordered exterior history is triple the original length.
The genuine selected 19D unit comparisons preserve that full
history; thus the two source 19D classes are unequal, while
the constant cross-fiber quotient map identifies them.

A separate proof-relevant comparison REFLECTION certificate
has an injective descended quotient map. The explicit constant
boundary fails that condition. No universal faithful certificate
is asserted to exist. Previous v5.39 conditional coarse
compatibility is not silently inherited by the constant map.

All older F55/P77/GK5CG, selected 6D–19D witnesses and
v5.39 sources remain untouched. Public root107, pinned
Lean/mathlib, and protected #1558 remain unchanged.
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

section MixedBoundary

variable (l r : W) {w z : W}
variable {a b c d : PentagonAdjoinedSixCell W l r w z}
variable (left : SevenRewrite W l r a b)
variable (F G : ContextFrameEleven W l r b c)
variable {P Q : SelectedUnitalCompositionTwelve W l r
  (contextFramePack l r F) (contextFramePack l r G)}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable (J N : SelectedContextualSeventeen W l r H K)
variable (right : SevenRewrite W l r c d)

/-- Construct a fully typed cross-fiber transport by sending
EVERY source 18D proof term to the same original, genuinely typed
RL 18D proof value. This is deliberately NONFAITHFUL. -/
def selectedMixedConstantBoundary
    (M : SelectedContextualEighteen W l r J N) :
    SelectedMixedNineteenBoundary l r left F G J N right where
  rawTransport := fun _ => selectedEighteenRightAfterLeft l r left F G M right
  localTransport := by
    intro X Y A
    exact .strict _

/-- The anchoring 19D comparison is the actual reflexive selected
19D witness on the original RL proof. No postulated comparison. -/
def selectedMixedConstantAnchored
    (M : SelectedContextualEighteen W l r J N) :
    SelectedMixedNineteenAnchored l r left F G J N right M where
  boundary := selectedMixedConstantBoundary l r left F G J N right M
  chosenComparison := by
    change SelectedLocalNineteen W l r
      (selectedEighteenRightAfterLeft l r left F G M right)
      (selectedEighteenRightAfterLeft l r left F G M right)
    exact .strict _

/-- An anchored v5.39 certificate exists for each actual original
18D value, BUT this constructed one is constant and nonfaithful. -/
theorem selectedMixedConstantAnchored_nonempty
    (M : SelectedContextualEighteen W l r J N) :
    Nonempty (SelectedMixedNineteenAnchored
      l r left F G J N right M) :=
  ⟨selectedMixedConstantAnchored l r left F G J N right M⟩

/-- The conditional v5.39 descent of the constructed constant
certificate is itself constant on ALL source 19D quotient classes. -/
theorem selectedMixedConstantDescend_all
    (M : SelectedContextualEighteen W l r J N)
    (q : selectedMixedLeftNineteenQuot l r left F G J N right) :
    selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedConstantBoundary l r left F G J N right M) q =
      selectedNineteenClass l r
        (selectedEighteenRightAfterLeft l r left F G M right) := by
  refine Quotient.inductionOn q ?_
  intro X
  rfl

/-- Genuine same-source-fiber loop, followed by the same 18D
witness again. Uses only old chain and reverse constructors. -/
def selectedMixedLeftRoundtripAmplify
    (X : selectedMixedLeftNineteenRaw l r left F G J N right) :
    selectedMixedLeftNineteenRaw l r left F G J N right :=
  .chain (.chain X (.reverse X)) X

/-- The raw 18D history of this explicit source-fiber roundtrip
contains three copies of the original, ordered, complete history. -/
theorem selectedMixedLeftRoundtrip_traceLength
    (X : selectedMixedLeftNineteenRaw l r left F G J N right) :
    (selectedContextEighteenTrace l r
      (selectedMixedLeftRoundtripAmplify l r left F G J N right X)).length =
        (selectedContextEighteenTrace l r X).length +
        (selectedContextEighteenTrace l r X).length +
        (selectedContextEighteenTrace l r X).length := by
  change ((selectedContextEighteenTrace l r X ++
      selectedContextEighteenTrace l r X) ++
      selectedContextEighteenTrace l r X).length =
        (selectedContextEighteenTrace l r X).length +
        (selectedContextEighteenTrace l r X).length +
        (selectedContextEighteenTrace l r X).length
  simp only [List.length_append]

/-- The actual LR witness has two visible outer events, so it
differs in complete ordered history from its own triple roundtrip. -/
theorem selectedMixedLeftRoundtrip_traceDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenTrace l r
        (selectedEighteenLeftAfterRight l r left F G M right) ≠
      selectedContextEighteenTrace l r
        (selectedMixedLeftRoundtripAmplify l r left F G J N right
          (selectedEighteenLeftAfterRight l r left F G M right)) := by
  have hpos :
      0 < (selectedContextEighteenTrace l r
        (selectedEighteenLeftAfterRight l r left F G M right)).length := by
    rw [(selectedEighteenMixedTraceValues l r left F G M right).1]
    simp
  intro heq
  have hlen := congrArg List.length heq
  rw [selectedMixedLeftRoundtrip_traceLength l r left F G J N right
    (selectedEighteenLeftAfterRight l r left F G M right)] at hlen
  omega

/-- The two genuinely different raw 18D histories cannot be
identified in the SAME exact-source 19D quotient: its full
List Bool trace is a proved quotient invariant. -/
theorem selectedMixedLeftRoundtrip_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenClass l r
        (selectedEighteenLeftAfterRight l r left F G M right) ≠
      selectedNineteenClass l r
        (selectedMixedLeftRoundtripAmplify l r left F G J N right
          (selectedEighteenLeftAfterRight l r left F G M right)) := by
  intro heq
  have hTrace := congrArg
    (selectedNineteenTraceOnQuotient l r _ _) heq
  exact (selectedMixedLeftRoundtrip_traceDistinct
    l r left F G J N right M) hTrace

/-- Hence the actual v5.39 constant quotient map collapses TWO
PROVEN DISTINCT source 19D classes. Its failure of injectivity
does not rely on any hypothetical higher-cell inhabitant. -/
theorem selectedMixedConstantDescend_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedConstantBoundary l r left F G J N right M)) := by
  intro hinj
  apply selectedMixedLeftRoundtrip_classDistinct l r left F G J N right M
  apply hinj
  exact (selectedMixedConstantDescend_all l r left F G J N right M _).trans
    (selectedMixedConstantDescend_all l r left F G J N right M _).symm

/-- Additional Type-valued comparison reflection is a stricter
authority condition than v5.39's proof-relevant comparison
preservation. No inhabitant of this structure is assumed. -/
structure SelectedMixedNineteenFaithfulBoundary : Type uSix where
  boundary : SelectedMixedNineteenBoundary l r left F G J N right
  reflectLocal :
    ∀ {X Y : selectedMixedLeftNineteenRaw l r left F G J N right},
      SelectedLocalNineteen W l r
        (boundary.rawTransport X) (boundary.rawTransport Y) →
      SelectedLocalNineteen W l r X Y

/-- Reflection of all genuine selected local 19D comparisons
ensures injectivity of the derived cross-fiber QUOTIENT map.
It does not assert raw function injectivity or raw source equality. -/
theorem selectedMixedFaithfulDescend_injective
    (B : SelectedMixedNineteenFaithfulBoundary
      l r left F G J N right) :
    Function.Injective
      (selectedMixedBoundaryDescend l r left F G J N right
        B.boundary) := by
  intro q₁ q₂ heq
  induction q₁ using Quotient.inductionOn with
  | _ X =>
      induction q₂ using Quotient.inductionOn with
      | _ Y =>
          change selectedNineteenClass l r
              (B.boundary.rawTransport X) =
            selectedNineteenClass l r
              (B.boundary.rawTransport Y) at heq
          rcases Quotient.exact heq with ⟨A⟩
          exact Quotient.sound ⟨B.reflectLocal A⟩

/-- The explicit constant boundary cannot reflect all genuine
selected 19D comparisons: that would identify the already
distinct LR source classes of the actual roundtrip. -/
theorem selectedMixedConstantBoundary_noReflection
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (∀ {X Y : selectedMixedLeftNineteenRaw l r left F G J N right},
      SelectedLocalNineteen W l r
        ((selectedMixedConstantBoundary l r left F G J N right M).rawTransport X)
        ((selectedMixedConstantBoundary l r left F G J N right M).rawTransport Y) →
      SelectedLocalNineteen W l r X Y) := by
  rintro ⟨hReflect⟩
  have A : SelectedLocalNineteen W l r
      (selectedEighteenLeftAfterRight l r left F G M right)
      (selectedMixedLeftRoundtripAmplify l r left F G J N right
        (selectedEighteenLeftAfterRight l r left F G M right)) := by
    apply hReflect
      (X := selectedEighteenLeftAfterRight l r left F G M right)
      (Y := selectedMixedLeftRoundtripAmplify l r left F G J N right
        (selectedEighteenLeftAfterRight l r left F G M right))
    exact .strict _
  exact (selectedMixedLeftRoundtrip_classDistinct
    l r left F G J N right M) (Quotient.sound ⟨A⟩)

/-- There cannot be a comparison-reflecting certificate whose
underlying boundary IS the explicit constant transport. -/
theorem selectedMixedFaithful_notConstant
    (M : SelectedContextualEighteen W l r J N)
    (B : SelectedMixedNineteenFaithfulBoundary
      l r left F G J N right) :
    B.boundary ≠ selectedMixedConstantBoundary
      l r left F G J N right M := by
  intro h
  have hi := selectedMixedFaithfulDescend_injective
    l r left F G J N right B
  rw [h] at hi
  exact (selectedMixedConstantDescend_notInjective
    l r left F G J N right M) hi

end MixedBoundary

#print axioms PentagonAdjoinedSixCell.selectedMixedConstantBoundary
#print axioms PentagonAdjoinedSixCell.selectedMixedConstantAnchored
#print axioms PentagonAdjoinedSixCell.selectedMixedConstantAnchored_nonempty
#print axioms PentagonAdjoinedSixCell.selectedMixedConstantDescend_all
#print axioms PentagonAdjoinedSixCell.selectedMixedLeftRoundtripAmplify
#print axioms PentagonAdjoinedSixCell.selectedMixedLeftRoundtrip_traceLength
#print axioms PentagonAdjoinedSixCell.selectedMixedLeftRoundtrip_traceDistinct
#print axioms PentagonAdjoinedSixCell.selectedMixedLeftRoundtrip_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedMixedConstantDescend_notInjective
#print axioms PentagonAdjoinedSixCell.SelectedMixedNineteenFaithfulBoundary
#print axioms PentagonAdjoinedSixCell.selectedMixedFaithfulDescend_injective
#print axioms PentagonAdjoinedSixCell.selectedMixedConstantBoundary_noReflection
#print axioms PentagonAdjoinedSixCell.selectedMixedFaithful_notConstant

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
