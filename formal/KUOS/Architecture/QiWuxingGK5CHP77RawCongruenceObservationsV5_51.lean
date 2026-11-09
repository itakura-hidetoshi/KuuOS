import KUOS.Architecture.QiWuxingGK5CHP77TypedRawCongruenceCompletionV5_50

/-!
Qi v5.51 — exact-fiber observables of the INDEPENDENT raw-context
congruence completion, and explicit failures of observation descent.

The FULL ordered raw 7D trace and the raw reverse-node count preserve
ALL SEVEN constructors: inherited, strict, reverse, chain,
rawReverse, rawChainRight and rawChainLeft.

The old LeftNestedCount is NOT invariant under the new completion:
a genuine original old18 witness supplies an explicit pair identified
by the NEW quotient with different nested counts. The original
typed 19D normal representative likewise does NOT descend to it.

This separates surviving observables from genuine information loss.
No old 19D comparison, typed original evidence, higher gluing,
heterogeneous whiskering, pin, root or validation branch is changed.
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

section ExactFiberObservations

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}

/-- The genuinely ordered outer-context trace survives ALL SEVEN
new Type-valued comparison constructors, not just old selected19. -/
theorem selectedRawCongruent_preservesTrace
    {J N : SelectedContextualSeventeen W l r H K}
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenTrace l r M =
      selectedContextEighteenTrace l r L := by
  induction A with
  | inherited A => exact selectedLocalNineteen_preservesEighteenTrace l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih => exact ih
  | rawChainRight A X ih =>
      exact congrArg (fun t : List Bool =>
        t ++ selectedContextEighteenTrace l r X) ih
  | rawChainLeft X A ih =>
      exact congrArg (fun t : List Bool =>
        selectedContextEighteenTrace l r X ++ t) ih

/-- Actual Quotient.lift on the NEW exact dependent fiber. -/
def selectedRawCongruentTraceOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → List Bool :=
  Quotient.lift (selectedContextEighteenTrace l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesTrace l r A)

theorem selectedRawCongruentTrace_onClass
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentTraceOnQuotient l r J N
      (selectedRawCongruentClass l r M) =
      selectedContextEighteenTrace l r M := rfl

/-- The old trace observable factors through the surjective
old-to-new map; it is not merely stable on selected representatives. -/
theorem selectedRawCongruentTrace_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentTraceOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenTraceOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- The raw reverse CONSTRUCTOR count is also invariant under all
seven new comparison constructors. Raw reverse adds one to BOTH
counts; left/right raw chain add the SAME fixed context count. -/
theorem selectedRawCongruent_preservesReverseCount
    {J N : SelectedContextualSeventeen W l r H K}
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenReverseCount l r M =
      selectedContextEighteenReverseCount l r L := by
  induction A with
  | inherited A => exact selectedLocalNineteen_preservesReverseCount l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      exact congrArg (fun n : Nat => n + 1) ih
  | rawChainRight A X ih =>
      exact congrArg (fun n : Nat =>
        n + selectedContextEighteenReverseCount l r X) ih
  | rawChainLeft X A ih =>
      exact congrArg (fun n : Nat =>
        selectedContextEighteenReverseCount l r X + n) ih

def selectedRawCongruentReverseCountOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenReverseCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesReverseCount l r A)

theorem selectedRawCongruentReverseCount_onClass
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentReverseCountOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenReverseCount l r M := rfl

/-- An exact concrete counterexample: the old nested count sees
the old unit-prepend top-level chain after a right raw context.
The new congruence identifies the two terms regardless. -/
theorem selectedRawCongruent_leftNested_changes
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    selectedContextEighteenLeftNestedCount l r
        (selectedNineteenRawRightStrict l r
          (selectedNineteenDirectUnitRaw l r M .prepend)) ≠
      selectedContextEighteenLeftNestedCount l r
        (selectedNineteenRawRightStrict l r
          (selectedNineteenDirectUnitRaw l r M .inherited)) := by
  change (1 : Nat) ≠ 0
  decide

/-- A single supplied genuine old18 witness forbids descent of the
old LeftNestedCount on this exact NEW quotient. In particular the
six-coordinate old I6 cannot silently be treated as NEW invariant. -/
theorem selectedRawCongruent_leftNested_noDescent
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    ¬ ∃ obs : Quotient (selectedRawCongruentSetoid l r J N) → Nat,
      ∀ Y : SelectedContextualEighteen W l r J N,
        obs (selectedRawCongruentClass l r Y) =
          selectedContextEighteenLeftNestedCount l r Y := by
  rintro ⟨obs, hobs⟩
  let A : SelectedContextualEighteen W l r J N :=
    selectedNineteenRawRightStrict l r
      (selectedNineteenDirectUnitRaw l r M .prepend)
  let B : SelectedContextualEighteen W l r J N :=
    selectedNineteenRawRightStrict l r
      (selectedNineteenDirectUnitRaw l r M .inherited)
  have hclass : selectedRawCongruentClass l r A =
      selectedRawCongruentClass l r B :=
    Quotient.sound ⟨selectedRawCongruent_rightStrictUnitComparison l r M⟩
  have hcount :
      selectedContextEighteenLeftNestedCount l r A =
        selectedContextEighteenLeftNestedCount l r B := by
    calc
      selectedContextEighteenLeftNestedCount l r A =
          obs (selectedRawCongruentClass l r A) := (hobs A).symm
      _ = obs (selectedRawCongruentClass l r B) := congrArg obs hclass
      _ = selectedContextEighteenLeftNestedCount l r B := hobs B
  exact (selectedRawCongruent_leftNested_changes l r M) hcount

/-- Unlike the ordered trace, the ORIGINAL 19D canonical typed
normal representative cannot descend to the NEW quotient. -/
theorem selectedRawCongruent_oldNormal_noDescent
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    ¬ ∃ obs : Quotient (selectedRawCongruentSetoid l r N J) →
        SelectedContextualEighteen W l r N J,
      ∀ Y : SelectedContextualEighteen W l r N J,
        obs (selectedRawCongruentClass l r Y) =
          selectedNineteenNormal l r Y := by
  rintro ⟨obs, hobs⟩
  let A : SelectedContextualEighteen W l r N J :=
    .reverse (selectedNineteenDirectUnitRaw l r M .prepend)
  let B : SelectedContextualEighteen W l r N J :=
    .reverse (selectedNineteenDirectUnitRaw l r M .inherited)
  have hclass : selectedRawCongruentClass l r A =
      selectedRawCongruentClass l r B :=
    Quotient.sound ⟨selectedRawCongruent_reverseUnitComparison l r M⟩
  have hnormal : selectedNineteenNormal l r A =
      selectedNineteenNormal l r B := by
    calc
      selectedNineteenNormal l r A =
          obs (selectedRawCongruentClass l r A) := (hobs A).symm
      _ = obs (selectedRawCongruentClass l r B) := congrArg obs hclass
      _ = selectedNineteenNormal l r B := hobs B
  exact (selectedNineteenRawReverse_unitObstruction l r M)
    ((selectedNineteenNormal_eq_iff_local l r A B).mp hnormal)

end ExactFiberObservations

#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesTrace
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTraceOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTrace_onClass
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTrace_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesReverseCount
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseCountOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseCount_onClass
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_leftNested_changes
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_leftNested_noDescent
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_oldNormal_noDescent

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
