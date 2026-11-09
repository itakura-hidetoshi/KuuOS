import KUOS.Architecture.QiWuxingGK5CHP77RawCongruenceObservationsV5_51

/-!
Qi v5.52 — residual raw-reversal obstruction in the INDEPENDENT
v5.50 congruence quotient, and infinitely many classes in one exact
ordered-trace fiber.

Use the v5.51 seven-constructor reverse-count invariant and the
ORIGINAL v5.43 double raw reverse. Descended raw reversal is not an
involution or a right inverse for descended raw chain. Iterating two
raw reversals retains the supplied original proof and its dependent
endpoints, keeps its complete ordered trace, and adds exactly 2*n
reverse nodes. This gives a Nat embedding into its fixed trace fiber.

The original 18D/19D proof Types and both comparison presentations
are unchanged. No new comparison/cancellation constructor, choice
of a witness in an empty fiber, heterogeneous whiskering or higher
gluing is introduced. The two regression contracts are retained.
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

/-- Raw reversal preserves the full ordered trace on the NEW quotient. -/
theorem selectedRawCongruentReverse_trace
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedRawCongruentSetoid l r J N)) :
    selectedRawCongruentTraceOnQuotient l r N J
        (selectedRawCongruentReverse l r J N q) =
      selectedRawCongruentTraceOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Descended raw reversal adds one genuine raw reverse node.
This is not an assumption of inverse cancellation. -/
theorem selectedRawCongruentReverse_count
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedRawCongruentSetoid l r J N)) :
    selectedRawCongruentReverseCountOnQuotient l r N J
        (selectedRawCongruentReverse l r J N q) =
      selectedRawCongruentReverseCountOnQuotient l r J N q + 1 := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Both quotient arguments retain their original typed endpoints. -/
theorem selectedRawCongruentChain_count
    (J N S : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedRawCongruentSetoid l r J N))
    (p : Quotient (selectedRawCongruentSetoid l r N S)) :
    selectedRawCongruentReverseCountOnQuotient l r J S
        (selectedRawCongruentChain l r J N S q p) =
      selectedRawCongruentReverseCountOnQuotient l r J N q +
        selectedRawCongruentReverseCountOnQuotient l r N S p := by
  induction q using Quotient.inductionOn with
  | _ M =>
      induction p using Quotient.inductionOn with
      | _ L => rfl

/-- The new raw congruence does NOT cancel a double raw reversal,
even though the complete ordered traces are identical. -/
theorem selectedRawCongruent_doubleReverse_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r M ≠
      selectedRawCongruentClass l r
        (selectedContextEighteenDoubleReverse l r M) := by
  intro h
  have hc := congrArg (selectedRawCongruentReverseCountOnQuotient l r J N) h
  change selectedContextEighteenReverseCount l r M =
    selectedContextEighteenReverseCount l r
      (selectedContextEighteenDoubleReverse l r M) at hc
  rw [selectedContextEighteenDoubleReverse_reverseCount l r M] at hc
  omega

/-- The obstruction is to an actual NEW Type-valued comparison,
not only to equality in the original, finer selected19 quotient. -/
theorem selectedRawCongruent_doubleReverse_noComparison
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r J N M
      (selectedContextEighteenDoubleReverse l r M)) := by
  rintro ⟨A⟩
  exact selectedRawCongruent_doubleReverse_classDistinct l r M
    (Quotient.sound ⟨A⟩)

/-- At every actually supplied quotient point, the TWO descended
raw reverse operations do not return that point. Empty fibers are
not populated by this statement. -/
theorem selectedRawCongruent_doubleReverse_noFixedPoint
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedRawCongruentSetoid l r J N)) :
    selectedRawCongruentReverse l r N J
        (selectedRawCongruentReverse l r J N q) ≠ q := by
  induction q using Quotient.inductionOn with
  | _ M =>
      change selectedRawCongruentClass l r
          (selectedContextEighteenDoubleReverse l r M) ≠
        selectedRawCongruentClass l r M
      intro h
      exact selectedRawCongruent_doubleReverse_classDistinct l r M h.symm

/-- Well-defined raw reversal is NOT a right inverse for the
specified descended raw chain and specified strict raw identity.
No assertion about every other possible algebraic structure is made. -/
theorem selectedRawCongruent_rawRightInverse_obstruction
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedRawCongruentSetoid l r J N)) :
    selectedRawCongruentChain l r J N J q
        (selectedRawCongruentReverse l r J N q) ≠
      selectedRawCongruentClass l r (SelectedContextualEighteen.strict J) := by
  intro h
  have hc := congrArg (selectedRawCongruentReverseCountOnQuotient l r J J) h
  rw [selectedRawCongruentChain_count,
    selectedRawCongruentReverse_count] at hc
  change selectedRawCongruentReverseCountOnQuotient l r J N q +
    (selectedRawCongruentReverseCountOnQuotient l r J N q + 1) = 0 at hc
  omega

/-- Repeated DOUBLE raw reversals of the supplied genuine witness.
Every value remains in the same exact J-to-N dependent fiber. -/
def selectedRawCongruentDoubleReverseIter
    (M : SelectedContextualEighteen W l r J N) :
    Nat → SelectedContextualEighteen W l r J N
  | 0 => M
  | n + 1 => selectedContextEighteenDoubleReverse l r
      (selectedRawCongruentDoubleReverseIter M n)

/-- Every member has the SAME full ordered exterior trace. -/
theorem selectedRawCongruentDoubleReverseIter_trace
    (M : SelectedContextualEighteen W l r J N) (n : Nat) :
    selectedContextEighteenTrace l r
        (selectedRawCongruentDoubleReverseIter l r M n) =
      selectedContextEighteenTrace l r M := by
  induction n with
  | zero => rfl
  | succ n ih =>
      exact (selectedContextEighteenDoubleReverse_trace l r
        (selectedRawCongruentDoubleReverseIter l r M n)).trans ih

/-- Exact unbounded reverse-count growth, without changing M. -/
theorem selectedRawCongruentDoubleReverseIter_count
    (M : SelectedContextualEighteen W l r J N) (n : Nat) :
    selectedContextEighteenReverseCount l r
        (selectedRawCongruentDoubleReverseIter l r M n) =
      selectedContextEighteenReverseCount l r M + 2 * n := by
  induction n with
  | zero => rfl
  | succ n ih =>
      change selectedContextEighteenReverseCount l r
          (selectedContextEighteenDoubleReverse l r
            (selectedRawCongruentDoubleReverseIter l r M n)) =
        selectedContextEighteenReverseCount l r M + 2 * (n + 1)
      rw [selectedContextEighteenDoubleReverse_reverseCount, ih]
      omega

/-- The NEW quotient, not only the old quotient, distinguishes
all Nat-indexed iterates in this supplied inhabited exact fiber. -/
theorem selectedRawCongruentDoubleReverseIter_classInjective
    (M : SelectedContextualEighteen W l r J N) :
    Function.Injective (fun n : Nat => selectedRawCongruentClass l r
      (selectedRawCongruentDoubleReverseIter l r M n)) := by
  intro m n h
  have hc := congrArg (selectedRawCongruentReverseCountOnQuotient l r J N) h
  change selectedContextEighteenReverseCount l r
      (selectedRawCongruentDoubleReverseIter l r M m) =
    selectedContextEighteenReverseCount l r
      (selectedRawCongruentDoubleReverseIter l r M n) at hc
  rw [selectedRawCongruentDoubleReverseIter_count,
    selectedRawCongruentDoubleReverseIter_count] at hc
  omega

/-- An exact classification for THIS constructed family only.
The backwards direction builds an actual strict comparison. -/
theorem selectedRawCongruentDoubleReverseIter_comparison_iff
    (M : SelectedContextualEighteen W l r J N) (m n : Nat) :
    Nonempty (SelectedRawCongruentNineteen W l r J N
      (selectedRawCongruentDoubleReverseIter l r M m)
      (selectedRawCongruentDoubleReverseIter l r M n)) ↔ m = n := by
  constructor
  · rintro ⟨A⟩
    exact selectedRawCongruentDoubleReverseIter_classInjective l r M
      (Quotient.sound ⟨A⟩)
  · rintro rfl
    exact ⟨.strict _⟩

/-- A genuine Nat embedding into ONE fixed ordered-trace fiber
of the NEW quotient. This proves infinitely many different classes
there, not countability or a classification of the whole quotient. -/
def selectedRawCongruentTraceFiberEmbedding
    (M : SelectedContextualEighteen W l r J N) :
    Nat ↪ {q : Quotient (selectedRawCongruentSetoid l r J N) //
      selectedRawCongruentTraceOnQuotient l r J N q =
        selectedContextEighteenTrace l r M} where
  toFun n := ⟨selectedRawCongruentClass l r
    (selectedRawCongruentDoubleReverseIter l r M n),
    selectedRawCongruentDoubleReverseIter_trace l r M n⟩
  inj' := by
    intro m n h
    exact selectedRawCongruentDoubleReverseIter_classInjective l r M
      (congrArg Subtype.val h)

/-- The actual strict raw identity supplies a witness for each
specified J-to-J fiber. Its empty trace fiber is already infinite;
this does not assert an inhabitant between arbitrary J and N. -/
def selectedRawCongruentEmptyTraceEmbedding
    (J : SelectedContextualSeventeen W l r H K) :
    Nat ↪ {q : Quotient (selectedRawCongruentSetoid l r J J) //
      selectedRawCongruentTraceOnQuotient l r J J q = []} :=
  selectedRawCongruentTraceFiberEmbedding l r
    (SelectedContextualEighteen.strict J)

/-- Trace descent is not trace faithfulness in the NEW quotient. -/
theorem selectedRawCongruentTrace_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective (selectedRawCongruentTraceOnQuotient l r J N) := by
  intro hinj
  exact selectedRawCongruent_doubleReverse_classDistinct l r M
    (hinj (show selectedRawCongruentTraceOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedRawCongruentTraceOnQuotient l r J N
        (selectedRawCongruentClass l r
          (selectedContextEighteenDoubleReverse l r M)) from rfl))

/-- No decoder of ordered trace can recover ALL classes in this
supplied inhabited fiber, even after the v5.50 coarsening. -/
theorem selectedRawCongruentTrace_noClassDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode : List Bool → Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentTraceOnQuotient l r J N q) = q := by
  rintro ⟨decode, hd⟩
  apply selectedRawCongruentTrace_notInjective l r M
  intro a b hab
  calc
    a = decode (selectedRawCongruentTraceOnQuotient l r J N a) := (hd a).symm
    _ = decode (selectedRawCongruentTraceOnQuotient l r J N b) :=
      congrArg decode hab
    _ = b := hd b

/-- Regression: two raw reversals do NOT cancel in the NEW quotient. -/
example (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r M ≠
      selectedRawCongruentClass l r (selectedContextEighteenDoubleReverse l r M) := by
  exact selectedRawCongruent_doubleReverse_classDistinct l r M

/-- Regression: no Type-valued NEW comparison can witness that cancellation. -/
example (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r J N M
      (selectedContextEighteenDoubleReverse l r M)) := by
  exact selectedRawCongruent_doubleReverse_noComparison l r M

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverse_trace
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverse_count
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentChain_count
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_doubleReverse_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_doubleReverse_noComparison
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_doubleReverse_noFixedPoint
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_rawRightInverse_obstruction
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentDoubleReverseIter
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentDoubleReverseIter_trace
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentDoubleReverseIter_count
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentDoubleReverseIter_classInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentDoubleReverseIter_comparison_iff
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTraceFiberEmbedding
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentEmptyTraceEmbedding
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTrace_notInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTrace_noClassDecoder

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
