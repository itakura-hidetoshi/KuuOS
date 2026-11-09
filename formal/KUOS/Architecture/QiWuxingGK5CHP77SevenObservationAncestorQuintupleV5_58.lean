import KUOS.Architecture.QiWuxingGK5CHP77SixObservationAncestorQuadrupleV5_57

/-!
Qi v5.58 — a reverse-ancestor QUINTUPLE remains invisible to all
SEVEN certified observations of the independent v5.50 raw congruence.

Retain the actual v5.57 suffixes A and B, without changing their
Type-valued evidence. Form the genuine N-to-N terms
  L = chain (reverse A) B
  R = chain A (reverse B).
Both have empty ordered trace, total reversals 15, adjacency 4,
top reverse flag 0, ancestor pairs 31, triples 32, and quadruples 18.
Their ancestor QUINTUPLE counts are 4 and 6.

Prove the new count invariant under all five old and seven new
comparison constructors; descend separately to both quotients.
For each actual M : J -> N, right-compose M with L and R in the SAME
exact original fiber. The seven observations coincide, but the
quintuple invariant separates the new quotient classes.

No arbitrary-fiber inhabitance, cross-fiber whiskering, 20D gluing,
eight-observation completeness, or authority escalation is claimed.
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

/-- Number of ordered strictly nested chains of FIVE raw reverse
constructors. An outer reverse contributes one quintuple for each
existing ancestor QUADRUPLE. Chain adds disjoint histories.
Inherited old evidence remains an opaque, retained Type value. -/
def selectedContextEighteenReverseAncestorQuintupleCount (l r : W)
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
  | .whiskerLeft _ _ _ M =>
      selectedContextEighteenReverseAncestorQuintupleCount l r M
  | .whiskerRight _ _ M _ =>
      selectedContextEighteenReverseAncestorQuintupleCount l r M
  | .strict _ => 0
  | .reverse M =>
      selectedContextEighteenReverseAncestorQuintupleCount l r M +
        selectedContextEighteenReverseAncestorQuadrupleCount l r M
  | .chain M L =>
      selectedContextEighteenReverseAncestorQuintupleCount l r M +
        selectedContextEighteenReverseAncestorQuintupleCount l r L

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- The five original selected19 constructors preserve the new count.
The old unit constructors act only on inherited old18 evidence. -/
theorem selectedLocalNineteen_preservesReverseAncestorQuintuple
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenReverseAncestorQuintupleCount l r M =
      selectedContextEighteenReverseAncestorQuintupleCount l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- All seven independent v5.50 constructors preserve quintuple count.
The rawReverse case uses the already certified v5.57 QUADRUPLE
invariant as well as the induction hypothesis. -/
theorem selectedRawCongruent_preservesReverseAncestorQuintuple
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenReverseAncestorQuintupleCount l r M =
      selectedContextEighteenReverseAncestorQuintupleCount l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesReverseAncestorQuintuple l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      exact congrArg₂ Nat.add ih
        (selectedRawCongruent_preservesReverseAncestorQuadruple l r A)
  | rawChainRight A X ih =>
      exact congrArg
        (fun n : Nat =>
          n + selectedContextEighteenReverseAncestorQuintupleCount l r X) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun n : Nat =>
          selectedContextEighteenReverseAncestorQuintupleCount l r X + n) ih

/-- Independently justified descent to the ORIGINAL selected19 quotient. -/
def selectedNineteenReverseAncestorQuintupleOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat :=
  Quotient.lift
    (selectedContextEighteenReverseAncestorQuintupleCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesReverseAncestorQuintuple l r A)

/-- Separately certified descent to the NEW seven-constructor quotient. -/
def selectedRawCongruentReverseAncestorQuintupleOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → Nat :=
  Quotient.lift
    (selectedContextEighteenReverseAncestorQuintupleCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesReverseAncestorQuintuple l r A)

theorem selectedRawCongruentReverseAncestorQuintuple_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentReverseAncestorQuintupleOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenReverseAncestorQuintupleCount l r M := rfl

/-- Old-to-new projection factorization on every actual quotient class. -/
theorem selectedRawCongruentReverseAncestorQuintuple_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentReverseAncestorQuintupleOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenReverseAncestorQuintupleOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Reuse BOTH unchanged v5.57 suffixes, reversing the LEFT one.
This is genuine N-to-N raw evidence, not a numerical replacement. -/
def selectedSevenQuintupleSuffixLeft
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain
    (.reverse (selectedSixQuadrupleSuffixLeft l r N))
    (selectedSixQuadrupleSuffixRight l r N)

/-- Reuse the same v5.57 suffixes, reversing the RIGHT one.
The previous quadruple discrepancy moves to quintuple count. -/
def selectedSevenQuintupleSuffixRight
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain
    (selectedSixQuadrupleSuffixLeft l r N)
    (.reverse (selectedSixQuadrupleSuffixRight l r N))

/-- Exact finite certificate on the actual typed suffixes:
both have 15 reversals, 4 adjacent reversals, 31 ancestor pairs,
32 triples and 18 quadruples; quintuple counts are 4 and 6. -/
theorem selectedSevenQuintuple_suffixSignature
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseCount l r
        (selectedSevenQuintupleSuffixLeft l r N) = 15 ∧
    selectedContextEighteenReverseCount l r
        (selectedSevenQuintupleSuffixRight l r N) = 15 ∧
    selectedContextEighteenAdjacentReverseCount l r
        (selectedSevenQuintupleSuffixLeft l r N) = 4 ∧
    selectedContextEighteenAdjacentReverseCount l r
        (selectedSevenQuintupleSuffixRight l r N) = 4 ∧
    selectedContextEighteenReverseAncestryCount l r
        (selectedSevenQuintupleSuffixLeft l r N) = 31 ∧
    selectedContextEighteenReverseAncestryCount l r
        (selectedSevenQuintupleSuffixRight l r N) = 31 ∧
    selectedContextEighteenReverseAncestorTripleCount l r
        (selectedSevenQuintupleSuffixLeft l r N) = 32 ∧
    selectedContextEighteenReverseAncestorTripleCount l r
        (selectedSevenQuintupleSuffixRight l r N) = 32 ∧
    selectedContextEighteenReverseAncestorQuadrupleCount l r
        (selectedSevenQuintupleSuffixLeft l r N) = 18 ∧
    selectedContextEighteenReverseAncestorQuadrupleCount l r
        (selectedSevenQuintupleSuffixRight l r N) = 18 ∧
    selectedContextEighteenReverseAncestorQuintupleCount l r
        (selectedSevenQuintupleSuffixLeft l r N) = 4 ∧
    selectedContextEighteenReverseAncestorQuintupleCount l r
        (selectedSevenQuintupleSuffixRight l r N) = 6 := by
  exact ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

/-- Append the left suffix to the actual original M, preserving its
Type value and the exact original J-to-N boundaries. -/
def selectedSevenQuintupleLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedSevenQuintupleSuffixLeft l r N)

/-- Append the right suffix to the SAME actual original M. -/
def selectedSevenQuintupleRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedSevenQuintupleSuffixRight l r N)

/-- The actual SEVEN-component quotient observations agree:
ordered trace, reversal total, adjacency, top flag, ancestor
pairs, triples, and quadruples. -/
theorem selectedSevenQuintuple_sevenObservedEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentSixQuadrupleObservation l r J N
        (selectedRawCongruentClass l r (selectedSevenQuintupleLeft l r M)) =
      selectedRawCongruentSixQuadrupleObservation l r J N
        (selectedRawCongruentClass l r (selectedSevenQuintupleRight l r M)) := by
  rfl

/-- The eighth raw invariant detects exactly two extra quintuple
chains on the right, independently of the supplied input M. -/
theorem selectedSevenQuintuple_countDiff
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenReverseAncestorQuintupleCount l r
        (selectedSevenQuintupleRight l r M) =
      selectedContextEighteenReverseAncestorQuintupleCount l r
        (selectedSevenQuintupleLeft l r M) + 2 := by
  rfl

/-- Seven observations do not determine the NEW quotient class. -/
theorem selectedSevenQuintuple_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r (selectedSevenQuintupleLeft l r M) ≠
      selectedRawCongruentClass l r (selectedSevenQuintupleRight l r M) := by
  intro h
  have hq := congrArg
    (selectedRawCongruentReverseAncestorQuintupleOnQuotient l r J N) h
  change selectedContextEighteenReverseAncestorQuintupleCount l r
      (selectedSevenQuintupleLeft l r M) =
    selectedContextEighteenReverseAncestorQuintupleCount l r
      (selectedSevenQuintupleRight l r M) at hq
  rw [selectedSevenQuintuple_countDiff l r M] at hq
  omega

/-- No genuine Type-valued new comparison relates the chosen pair,
even with all seven contextual congruence constructors. -/
theorem selectedSevenQuintuple_noComparison
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r J N
        (selectedSevenQuintupleLeft l r M)
        (selectedSevenQuintupleRight l r M)) := by
  rintro ⟨A⟩
  exact (selectedSevenQuintuple_classDistinct l r M) (Quotient.sound ⟨A⟩)

/-- Noninjectivity on each exact original fiber supplied with an
actual M; no arbitrary J-to-N inhabitance is assumed. -/
theorem selectedRawCongruentSeven_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective (selectedRawCongruentSixQuadrupleObservation l r J N) := by
  intro hinj
  exact (selectedSevenQuintuple_classDistinct l r M)
    (hinj (selectedSevenQuintuple_sevenObservedEq l r M))

/-- No complete decoder from the seven observations recovers all
new quotient classes in an actually inhabited exact fiber. -/
theorem selectedRawCongruentSeven_noDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode : ((((((List Bool × Nat) × Nat) × Nat) × Nat) × Nat) × Nat) →
        Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentSixQuadrupleObservation l r J N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedRawCongruentSeven_notInjective l r M
  intro a b hab
  calc
    a = decode (selectedRawCongruentSixQuadrupleObservation l r J N a) :=
      (h a).symm
    _ = decode (selectedRawCongruentSixQuadrupleObservation l r J N b) :=
      congrArg decode hab
    _ = b := h b

/-- The eighth invariant itself does not factor through the previous
seven-component observation on an actually inhabited exact fiber. -/
theorem selectedRawCongruentSeven_noQuintupleDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decodeQuint : ((((((List Bool × Nat) × Nat) × Nat) × Nat) × Nat) × Nat) → Nat,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decodeQuint (selectedRawCongruentSixQuadrupleObservation l r J N q) =
          selectedRawCongruentReverseAncestorQuintupleOnQuotient l r J N q := by
  rintro ⟨decodeQuint, h⟩
  have hq :
      selectedRawCongruentReverseAncestorQuintupleOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedSevenQuintupleLeft l r M)) =
        selectedRawCongruentReverseAncestorQuintupleOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedSevenQuintupleRight l r M)) := by
    calc
      _ = decodeQuint (selectedRawCongruentSixQuadrupleObservation l r J N
            (selectedRawCongruentClass l r (selectedSevenQuintupleLeft l r M))) :=
        (h _).symm
      _ = decodeQuint (selectedRawCongruentSixQuadrupleObservation l r J N
            (selectedRawCongruentClass l r (selectedSevenQuintupleRight l r M))) :=
        congrArg decodeQuint (selectedSevenQuintuple_sevenObservedEq l r M)
      _ = _ := h _
  change selectedContextEighteenReverseAncestorQuintupleCount l r
      (selectedSevenQuintupleLeft l r M) =
    selectedContextEighteenReverseAncestorQuintupleCount l r
      (selectedSevenQuintupleRight l r M) at hq
  rw [selectedSevenQuintuple_countDiff l r M] at hq
  omega

/-- Genuine strict J supplies an actual witness for every specified
J-to-J endomorphism fiber, without an all-fiber inhabitance claim. -/
theorem selectedRawCongruentSeven_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective (selectedRawCongruentSixQuadrupleObservation l r J J) :=
  selectedRawCongruentSeven_notInjective l r (SelectedContextualEighteen.strict J)

/-- Eight independently justified quotient observations. This
definition does not assert completeness of the resulting tuple. -/
def selectedRawCongruentSevenQuintupleObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      (((((((List Bool × Nat) × Nat) × Nat) × Nat) × Nat) × Nat) × Nat) :=
  fun q =>
    (selectedRawCongruentSixQuadrupleObservation l r J N q,
      selectedRawCongruentReverseAncestorQuintupleOnQuotient l r J N q)

/-- The eighth observation distinguishes THIS explicit pair only. -/
theorem selectedRawCongruentEight_quintupleDistinguished
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentSevenQuintupleObservation l r J N
        (selectedRawCongruentClass l r (selectedSevenQuintupleLeft l r M)) ≠
      selectedRawCongruentSevenQuintupleObservation l r J N
        (selectedRawCongruentClass l r (selectedSevenQuintupleRight l r M)) := by
  intro h
  have hq := congrArg Prod.snd h
  change selectedContextEighteenReverseAncestorQuintupleCount l r
      (selectedSevenQuintupleLeft l r M) =
    selectedContextEighteenReverseAncestorQuintupleCount l r
      (selectedSevenQuintupleRight l r M) at hq
  rw [selectedSevenQuintuple_countDiff l r M] at hq
  omega

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenReverseAncestorQuintupleCount
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesReverseAncestorQuintuple
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesReverseAncestorQuintuple
#print axioms PentagonAdjoinedSixCell.selectedNineteenReverseAncestorQuintupleOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseAncestorQuintupleOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseAncestorQuintuple_onClass
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseAncestorQuintuple_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedSevenQuintupleSuffixLeft
#print axioms PentagonAdjoinedSixCell.selectedSevenQuintupleSuffixRight
#print axioms PentagonAdjoinedSixCell.selectedSevenQuintuple_suffixSignature
#print axioms PentagonAdjoinedSixCell.selectedSevenQuintupleLeft
#print axioms PentagonAdjoinedSixCell.selectedSevenQuintupleRight
#print axioms PentagonAdjoinedSixCell.selectedSevenQuintuple_sevenObservedEq
#print axioms PentagonAdjoinedSixCell.selectedSevenQuintuple_countDiff
#print axioms PentagonAdjoinedSixCell.selectedSevenQuintuple_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedSevenQuintuple_noComparison
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentSeven_notInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentSeven_noDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentSeven_noQuintupleDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentSeven_endomorphismNotInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentSevenQuintupleObservation
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentEight_quintupleDistinguished

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
