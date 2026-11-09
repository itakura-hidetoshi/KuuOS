import KUOS.Architecture.QiWuxingGK5CHP77JointObservationResidualV5_53

/-!
Qi v5.54 — residual top-reverse obstruction after three jointly
certified observables in the independent raw-congruence quotient.

The v5.53 three-component observable (ordered trace, total raw
reverse-node count, adjacent raw reverse-node count) does NOT classify
the v5.50 quotient even over an inhabited exact 17D endpoint fiber.

For every actual raw M : J -> N, compare the genuine constructors
  A(M) = reverse (reverse M)
  B(M) = chain (reverse (reverse M)) (strict N).
The third observable agrees, as do the first two. But the already
certified seven-constructor-invariant TOP reverse flag is 1 on A(M)
and 0 on B(M); hence the quotient classes differ. Consequently the
triple observer admits neither an injection certificate nor a
global class decoder on any specified inhabited exact fiber, and
the top-reverse flag cannot be reconstructed from the triple.

No old 18D/19D Type-valued proofs, raw syntax, selected19 generator,
new v5.50 comparison, import, public root, or pin is modified.
This is an independent NEW theorem module. No classification by four
observables, arbitrary fiber inhabitance, heterogeneous whiskering,
cross-fiber gluing, or global authority is claimed.
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

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- An unchanged genuine raw double reversal, in the SAME exact J-to-N
fiber as the given original evidence M. -/
def selectedTripleResidualLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .reverse (.reverse M)

/-- The genuine right-strict extension of the double reverse. The
original 19D unit-append constructor is restricted to INHERITED raw
proofs; it does not identify this raw double reverse with its extension. -/
def selectedTripleResidualRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain (selectedTripleResidualLeft l r M) (.strict N)

/-- Both terms have exactly the same COMPLETE ordered raw trace. -/
theorem selectedTripleResidual_traceEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenTrace l r (selectedTripleResidualLeft l r M) =
      selectedContextEighteenTrace l r (selectedTripleResidualRight l r M) := by
  change selectedContextEighteenTrace l r M =
    selectedContextEighteenTrace l r M ++ []
  simp

/-- The two genuine raw syntaxes contain exactly the same number of
raw reverse constructors. No cancellation or associativity is assumed. -/
theorem selectedTripleResidual_reverseCountEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenReverseCount l r (selectedTripleResidualLeft l r M) =
      selectedContextEighteenReverseCount l r (selectedTripleResidualRight l r M) := by
  rfl

/-- Adding a strict right identity does not introduce an ADJACENT
raw reverse pair. Both sides retain the same adjacency counter. -/
theorem selectedTripleResidual_adjacentCountEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenAdjacentReverseCount l r
        (selectedTripleResidualLeft l r M) =
      selectedContextEighteenAdjacentReverseCount l r
        (selectedTripleResidualRight l r M) := by
  rfl

/-- The fourth, ALREADY QUOTIENT-INVARIANT flag detects a genuine
difference in the outermost raw syntax of these two proofs. -/
theorem selectedTripleResidual_leftTopReverse
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenTopReverseFlag l r
      (selectedTripleResidualLeft l r M) = 1 := by
  rfl

theorem selectedTripleResidual_rightTopReverse
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenTopReverseFlag l r
      (selectedTripleResidualRight l r M) = 0 := by
  rfl

/-- Genuine equality of ALL THREE quotient-level observations, not
merely a coincidence between informal raw-feature vectors. -/
theorem selectedTripleResidual_threeObservedEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentTraceReverseAdjacentObservation l r J N
      (selectedRawCongruentClass l r (selectedTripleResidualLeft l r M)) =
    selectedRawCongruentTraceReverseAdjacentObservation l r J N
      (selectedRawCongruentClass l r (selectedTripleResidualRight l r M)) := by
  apply Prod.ext
  · apply Prod.ext
    · exact selectedTripleResidual_traceEq l r M
    · exact selectedTripleResidual_reverseCountEq l r M
  · exact selectedTripleResidual_adjacentCountEq l r M

/-- Despite the identical triple, the two classes are DISTINCT in
the NEW v5.50 quotient, because top reverse is stable under ALL seven
comparison constructors (certified in v5.53). -/
theorem selectedTripleResidual_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r (selectedTripleResidualLeft l r M) ≠
      selectedRawCongruentClass l r (selectedTripleResidualRight l r M) := by
  intro h
  have hf := congrArg (selectedRawCongruentTopReverseOnQuotient l r J N) h
  change selectedContextEighteenTopReverseFlag l r
      (selectedTripleResidualLeft l r M) =
    selectedContextEighteenTopReverseFlag l r
      (selectedTripleResidualRight l r M) at hf
  rw [selectedTripleResidual_leftTopReverse l r M,
    selectedTripleResidual_rightTopReverse l r M] at hf
  cases hf

/-- In particular, no Type-valued NEW comparison can join these
genuine 18D witnesses even after contextual raw congruence closure. -/
theorem selectedTripleResidual_noComparison
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r J N
      (selectedTripleResidualLeft l r M)
      (selectedTripleResidualRight l r M)) := by
  rintro ⟨A⟩
  exact (selectedTripleResidual_classDistinct l r M) (Quotient.sound ⟨A⟩)

/-- The triple observer is NOT faithful on any exact J-to-N fiber
for which an actual original raw 18D proof M is supplied. -/
theorem selectedRawCongruentTriple_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedRawCongruentTraceReverseAdjacentObservation l r J N) := by
  intro hinj
  exact (selectedTripleResidual_classDistinct l r M)
    (hinj (selectedTripleResidual_threeObservedEq l r M))

/-- No all-class decoding function from the triple can be a left
inverse, on any inhabited exact original 17D endpoint fiber. -/
theorem selectedRawCongruentTriple_noDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode : ((List Bool × Nat) × Nat) →
        Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentTraceReverseAdjacentObservation l r J N q) =
          q := by
  rintro ⟨decode, h⟩
  apply selectedRawCongruentTriple_notInjective l r M
  intro a b hab
  calc
    a = decode (selectedRawCongruentTraceReverseAdjacentObservation l r J N a) :=
      (h a).symm
    _ = decode (selectedRawCongruentTraceReverseAdjacentObservation l r J N b) :=
      congrArg decode hab
    _ = b := h b

/-- Even the QUOTIENT-INVARIANT top reverse flag is NOT a function
of the three observations on an inhabited exact fiber. -/
theorem selectedRawCongruentTriple_noTopFlagDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decodeFlag : ((List Bool × Nat) × Nat) → Nat,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decodeFlag (selectedRawCongruentTraceReverseAdjacentObservation l r J N q) =
          selectedRawCongruentTopReverseOnQuotient l r J N q := by
  rintro ⟨decodeFlag, h⟩
  have hf :
      selectedRawCongruentTopReverseOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedTripleResidualLeft l r M)) =
        selectedRawCongruentTopReverseOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedTripleResidualRight l r M)) := by
    calc
      _ = decodeFlag (selectedRawCongruentTraceReverseAdjacentObservation l r J N
            (selectedRawCongruentClass l r (selectedTripleResidualLeft l r M))) :=
        (h _).symm
      _ = decodeFlag (selectedRawCongruentTraceReverseAdjacentObservation l r J N
            (selectedRawCongruentClass l r (selectedTripleResidualRight l r M))) :=
        congrArg decodeFlag (selectedTripleResidual_threeObservedEq l r M)
      _ = _ := h _
  change selectedContextEighteenTopReverseFlag l r
      (selectedTripleResidualLeft l r M) =
    selectedContextEighteenTopReverseFlag l r
      (selectedTripleResidualRight l r M) at hf
  rw [selectedTripleResidual_leftTopReverse l r M,
    selectedTripleResidual_rightTopReverse l r M] at hf
  cases hf

/-- A specified 17D endpoint supplies a genuine raw strict identity,
so triple nonfaithfulness holds on every such ENDOMORPHISM fiber. -/
theorem selectedRawCongruentTriple_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentTraceReverseAdjacentObservation l r J J) :=
  selectedRawCongruentTriple_notInjective l r (SelectedContextualEighteen.strict J)

/-- A fourth certified observation separates THIS raw counterexample,
without suggesting any global completeness of four observations. -/
def selectedRawCongruentTripleTopReverseObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      (((List Bool × Nat) × Nat) × Nat) :=
  fun q =>
    (selectedRawCongruentTraceReverseAdjacentObservation l r J N q,
      selectedRawCongruentTopReverseOnQuotient l r J N q)

theorem selectedRawCongruentFour_residualDistinguished
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentTripleTopReverseObservation l r J N
        (selectedRawCongruentClass l r (selectedTripleResidualLeft l r M)) ≠
      selectedRawCongruentTripleTopReverseObservation l r J N
        (selectedRawCongruentClass l r (selectedTripleResidualRight l r M)) := by
  intro h
  have hf := congrArg Prod.snd h
  change selectedContextEighteenTopReverseFlag l r
      (selectedTripleResidualLeft l r M) =
    selectedContextEighteenTopReverseFlag l r
      (selectedTripleResidualRight l r M) at hf
  rw [selectedTripleResidual_leftTopReverse l r M,
    selectedTripleResidual_rightTopReverse l r M] at hf
  cases hf

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedTripleResidualLeft
#print axioms PentagonAdjoinedSixCell.selectedTripleResidualRight
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_traceEq
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_reverseCountEq
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_adjacentCountEq
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_leftTopReverse
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_rightTopReverse
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_threeObservedEq
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_noComparison
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTriple_notInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTriple_noDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTriple_noTopFlagDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTriple_endomorphismNotInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTripleTopReverseObservation
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFour_residualDistinguished

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
