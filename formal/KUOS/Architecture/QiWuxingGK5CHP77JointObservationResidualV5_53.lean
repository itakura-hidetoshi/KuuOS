import KUOS.Architecture.QiWuxingGK5CHP77RawCongruenceDoubleReverseObstructionV5_52

/-!
Qi v5.53 — joint-observation residual in the independent v5.50
raw-context congruence quotient. This is a NEW proof module.

A concrete original v5.47 pair has identical full ordered trace
and total raw reverse-node count. It remains distinct in the NEW
seven-constructor quotient because a separate, genuine invariant,
the adjacent raw reverse count, survives ALL seven constructors.

The top-reverse flag is proved invariant to establish closure of the
adjacent count under raw reversal. No old 19D proof is altered or
identified by fiat. The joint observer is not made faithful by
discarding the surviving adjacent-reversal obstruction.

All conclusions are within the indicated original 16D fiber and
typed 17D endpoints. No all-fiber inhabitance, cross-fiber whiskering,
global gluing, or full quotient classification is asserted.
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

/-- True top-of-syntax reverse flag, 1 for raw reverse, 0 otherwise.
The full old top tag is not claimed to descend. -/
def selectedContextEighteenTopReverseFlag
    (M : SelectedContextualEighteen W l r J N) : Nat :=
  if selectedContextEighteenTopTag l r M = 4 then 1 else 0

/-- The original 19D five constructors preserve only the TOP REVERSE
flag, not the complete raw top tag. In unit pasting, both old raw
tops are NON-reverse (chain and inherited). -/
theorem selectedLocalNineteen_preservesTopReverseFlag
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenTopReverseFlag l r M =
      selectedContextEighteenTopReverseFlag l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- The top-reverse flag respects all SEVEN NEW constructors:
inherited, strict, reverse, chain, rawReverse, rawChainRight,
rawChainLeft. A raw reversal sets the flag to 1 on both sides,
while raw left/right composition sets it to 0 on both sides. -/
theorem selectedRawCongruent_preservesTopReverseFlag
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenTopReverseFlag l r M =
      selectedContextEighteenTopReverseFlag l r L := by
  induction A with
  | inherited A => exact selectedLocalNineteen_preservesTopReverseFlag l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih => rfl
  | rawChainRight A X ih => rfl
  | rawChainLeft X A ih => rfl

/-- The adjacent-reverse count genuinely survives all seven new
comparison constructors. The potentially nontrivial rawReverse
case requires BOTH the previous adjacent count equality and the
newly certified top-reverse-flag equality. -/
theorem selectedRawCongruent_preservesAdjacentReverseCount
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenAdjacentReverseCount l r M =
      selectedContextEighteenAdjacentReverseCount l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesAdjacentReverseCount l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      change selectedContextEighteenAdjacentReverseCount l r _ +
          selectedContextEighteenTopReverseFlag l r _ =
        selectedContextEighteenAdjacentReverseCount l r _ +
          selectedContextEighteenTopReverseFlag l r _
      exact congrArg₂ Nat.add ih
        (selectedRawCongruent_preservesTopReverseFlag l r A)
  | rawChainRight A X ih =>
      exact congrArg
        (fun n : Nat => n + selectedContextEighteenAdjacentReverseCount l r X) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun n : Nat => selectedContextEighteenAdjacentReverseCount l r X + n) ih

/-- The top-reverse flag descends to the newly generated quotient. -/
def selectedRawCongruentTopReverseOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenTopReverseFlag l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesTopReverseFlag l r A)

/-- The adjacent reverse count also genuinely descends to the NEW
quotient, rather than being borrowed from the finer old quotient. -/
def selectedRawCongruentAdjacentReverseOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenAdjacentReverseCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesAdjacentReverseCount l r A)

theorem selectedRawCongruentAdjacentReverse_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentAdjacentReverseOnQuotient l r J N
      (selectedRawCongruentClass l r M) =
        selectedContextEighteenAdjacentReverseCount l r M := rfl

/-- Compatibility with the old original quotient: its adjacent
reverse observable factors EXACTLY through the old-to-new projection. -/
theorem selectedRawCongruentAdjacentReverse_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentAdjacentReverseOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenAdjacentReverseOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- The exact ordered trace and actual total raw reverse count
as a two-component observation of the NEW quotient. -/
def selectedRawCongruentTraceReverseObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → List Bool × Nat :=
  fun q =>
    (selectedRawCongruentTraceOnQuotient l r J N q,
      selectedRawCongruentReverseCountOnQuotient l r J N q)

theorem selectedRawCongruentTraceReverse_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentTraceReverseObservation l r J N
        (selectedRawCongruentClass l r M) =
      (selectedContextEighteenTrace l r M,
        selectedContextEighteenReverseCount l r M) := rfl

/-- The joint observation is compatible with the old quotient map,
without assuming that the old six coordinates all descend. -/
theorem selectedRawCongruentTraceReverse_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentTraceReverseObservation l r J N
        (selectedRawCongruentProject l r J N q) =
      (selectedNineteenTraceOnQuotient l r J N q,
        selectedNineteenReverseCountOnQuotient l r J N q) := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Reuse TWO original v5.47 raw terms; they have identical
ordered trace and total raw reverse count even on the NEW quotient. -/
theorem selectedRawCongruentTraceReverse_adjacentEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentTraceReverseObservation l r J N
      (selectedRawCongruentClass l r (selectedAdjacentReverseLeft l r M)) =
    selectedRawCongruentTraceReverseObservation l r J N
      (selectedRawCongruentClass l r (selectedAdjacentReverseRight l r M)) := by
  apply Prod.ext
  · exact selectedAdjacentReverse_trace l r M
  · rfl

/-- The NEW quotient retains the v5.47 adjacency obstruction. The
same ordered trace and total reverse count do not erase adjacency. -/
theorem selectedRawCongruent_adjacent_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r (selectedAdjacentReverseLeft l r M) ≠
      selectedRawCongruentClass l r (selectedAdjacentReverseRight l r M) := by
  intro h
  have hc := congrArg (selectedRawCongruentAdjacentReverseOnQuotient l r J N) h
  change selectedContextEighteenAdjacentReverseCount l r
      (selectedAdjacentReverseLeft l r M) =
    selectedContextEighteenAdjacentReverseCount l r
      (selectedAdjacentReverseRight l r M) at hc
  rw [selectedAdjacentReverse_countDiff l r M] at hc
  omega

/-- No NEW Type-valued 19D comparison exists between these two raw
histories, even after the v5.50 context congruence completion. -/
theorem selectedRawCongruent_adjacent_noComparison
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r J N
      (selectedAdjacentReverseLeft l r M)
      (selectedAdjacentReverseRight l r M)) := by
  rintro ⟨A⟩
  exact (selectedRawCongruent_adjacent_classDistinct l r M)
    (Quotient.sound ⟨A⟩)

/-- A chosen genuine raw witness disproves JOINT faithfulness,
not just ordered-trace faithfulness. -/
theorem selectedRawCongruentTraceReverse_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective (selectedRawCongruentTraceReverseObservation l r J N) := by
  intro hinj
  exact (selectedRawCongruent_adjacent_classDistinct l r M)
    (hinj (selectedRawCongruentTraceReverse_adjacentEq l r M))

/-- No all-class decoder from the two-component joint observation
exists in an actual inhabited J-to-N fiber. -/
theorem selectedRawCongruentTraceReverse_noDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode : List Bool × Nat →
        Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentTraceReverseObservation l r J N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedRawCongruentTraceReverse_notInjective l r M
  intro a b hab
  calc
    a = decode (selectedRawCongruentTraceReverseObservation l r J N a) :=
      (h a).symm
    _ = decode (selectedRawCongruentTraceReverseObservation l r J N b) :=
      congrArg decode hab
    _ = b := h b

/-- A specified 17D endpoint J supplies strict raw identity, hence
the joint pair is non-faithful on J-to-J, without needing any
inhabitance assertion for arbitrary distinct J and N. -/
theorem selectedRawCongruentTraceReverse_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective (selectedRawCongruentTraceReverseObservation l r J J) :=
  selectedRawCongruentTraceReverse_notInjective l r
    (SelectedContextualEighteen.strict J)

/-- An explicit third, independently certified adjacent count
does separate THIS pair. No global triple-classification is claimed. -/
def selectedRawCongruentTraceReverseAdjacentObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      (List Bool × Nat) × Nat :=
  fun q => (selectedRawCongruentTraceReverseObservation l r J N q,
    selectedRawCongruentAdjacentReverseOnQuotient l r J N q)

theorem selectedRawCongruentTriple_adjacentDistinguished
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentTraceReverseAdjacentObservation l r J N
      (selectedRawCongruentClass l r (selectedAdjacentReverseLeft l r M)) ≠
    selectedRawCongruentTraceReverseAdjacentObservation l r J N
      (selectedRawCongruentClass l r (selectedAdjacentReverseRight l r M)) := by
  intro h
  have hc := congrArg Prod.snd h
  change selectedContextEighteenAdjacentReverseCount l r
      (selectedAdjacentReverseLeft l r M) =
    selectedContextEighteenAdjacentReverseCount l r
      (selectedAdjacentReverseRight l r M) at hc
  rw [selectedAdjacentReverse_countDiff l r M] at hc
  omega

/-- Original six raw numbers are STILL equal for this concrete
pair. Their equality is not an assertion that old I6 descends to
the NEW quotient (v5.51 showed a component fails to descend). -/
theorem selectedRawCongruent_adjacent_rawSixEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenSix l r (selectedAdjacentReverseLeft l r M) =
      selectedContextEighteenSix l r (selectedAdjacentReverseRight l r M) :=
  selectedAdjacentReverse_rawSixEq l r M

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenTopReverseFlag
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesTopReverseFlag
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesTopReverseFlag
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesAdjacentReverseCount
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTopReverseOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentAdjacentReverseOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentAdjacentReverse_onClass
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentAdjacentReverse_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTraceReverseObservation
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTraceReverse_onClass
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTraceReverse_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTraceReverse_adjacentEq
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_adjacent_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_adjacent_noComparison
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTraceReverse_notInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTraceReverse_noDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTraceReverse_endomorphismNotInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTraceReverseAdjacentObservation
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTriple_adjacentDistinguished
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_adjacent_rawSixEq

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
