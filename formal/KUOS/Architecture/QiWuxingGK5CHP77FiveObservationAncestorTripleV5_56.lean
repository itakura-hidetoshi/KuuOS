import KUOS.Architecture.QiWuxingGK5CHP77FourObservationAncestryResidualV5_55

/-!
Qi v5.56 — residual ancestor-TRIPLE obstruction after FIVE
independently certified observations in the v5.50 raw-congruence quotient.

The original dependent 18D evidence, original selected19 comparison,
and the independently generated seven-constructor raw comparison
are UNCHANGED. Define a new count of strictly nested ordered TRIPLES
of raw reverse nodes, beyond the already certified ancestry PAIR count.
Inherited evidence remains an opaque leaf.

For each actual M : J -> N, append two genuine strict N -> N raw suffixes.
The suffixes both have total reverse nodes 6, adjacent reverse pairs 3,
reverse ancestor/descendant pairs 11 and top-reverse flag 1. Their
nested reverse TRIPLE counts are 8 and 10, respectively. Appending
them to M yields the SAME five old quotient observations, but different
new triple counts. The difference survives ALL seven new comparison
constructors, so the new quotient classes remain different.

No five-observation quotient classification is assumed or derived.
The sixth independent observation distinguishes the specified pair only.
No arbitrary-fiber inhabitance, heterogeneous whiskering, 20D gluing,
or authority escalation is asserted.
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

/-- Ordered chains of THREE distinct raw reverse ancestors. An
outer raw reverse adds one triple for every inner reverse ancestry
PAIR, while chaining adds disjoint histories. Nothing is inferred
about the internal syntax of an inherited old 18D proof. -/
def selectedContextEighteenReverseAncestorTripleCount (l r : W)
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
  | .whiskerLeft _ _ _ M => selectedContextEighteenReverseAncestorTripleCount l r M
  | .whiskerRight _ _ M _ => selectedContextEighteenReverseAncestorTripleCount l r M
  | .strict _ => 0
  | .reverse M =>
      selectedContextEighteenReverseAncestorTripleCount l r M +
        selectedContextEighteenReverseAncestryCount l r M
  | .chain M L =>
      selectedContextEighteenReverseAncestorTripleCount l r M +
        selectedContextEighteenReverseAncestorTripleCount l r L

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- All five ORIGINAL comparison constructors preserve the count.
The old selected19 unit generators only act on inherited witnesses. -/
theorem selectedLocalNineteen_preservesReverseAncestorTriple
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenReverseAncestorTripleCount l r M =
      selectedContextEighteenReverseAncestorTripleCount l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- All SEVEN v5.50 new congruence constructors preserve triple
ancestry. The rawReverse case requires both this IH and the
previously proved v5.55 reverse-ancestry PAIR preservation. -/
theorem selectedRawCongruent_preservesReverseAncestorTriple
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenReverseAncestorTripleCount l r M =
      selectedContextEighteenReverseAncestorTripleCount l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesReverseAncestorTriple l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      exact congrArg₂ Nat.add ih
        (selectedRawCongruent_preservesReverseAncestry l r A)
  | rawChainRight A X ih =>
      exact congrArg
        (fun n : Nat => n + selectedContextEighteenReverseAncestorTripleCount l r X) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun n : Nat => selectedContextEighteenReverseAncestorTripleCount l r X + n) ih

/-- Genuine descent to the ORIGINAL finer selected19 quotient. -/
def selectedNineteenReverseAncestorTripleOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenReverseAncestorTripleCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesReverseAncestorTriple l r A)

/-- A SEPARATELY justified lift to the NEW quotient. Old-quotient
descent is not silently asserted to survive a coarser relation. -/
def selectedRawCongruentReverseAncestorTripleOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenReverseAncestorTripleCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesReverseAncestorTriple l r A)

theorem selectedRawCongruentReverseAncestorTriple_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentReverseAncestorTripleOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenReverseAncestorTripleCount l r M := rfl

/-- Exact compatibility with the original-to-new quotient projection. -/
theorem selectedRawCongruentReverseAncestorTriple_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentReverseAncestorTripleOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenReverseAncestorTripleOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Suffix shape R(R(C(R(R(S)),R(R(S)))) has six reverse
nodes, three adjacent reverse pairs, eleven ancestor PAIRS,
and eight ancestor TRIPLES. All reverse/chain values are genuine. -/
def selectedFiveAncestorTripleLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M
    (.reverse (.reverse
      (.chain
        (.reverse (.reverse (.strict N)))
        (.reverse (.reverse (.strict N))))))

/-- Suffix R(C(R(S),R(R(R(R(S)))))) also has reverse count 6,
adjacent count 3 and ancestor-pair count 11, but TEN triples.
The original witness M is retained without any modification. -/
def selectedFiveAncestorTripleRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M
    (.reverse
      (.chain
        (.reverse (.strict N))
        (.reverse (.reverse (.reverse (.reverse (.strict N)))))))

/-- All FIVE existing quotient-level observations agree: complete
ordered trace, reverse count, adjacency, top flag, ancestry PAIRS. -/
theorem selectedFiveAncestorTriple_fiveObservedEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentFourAncestryObservation l r J N
        (selectedRawCongruentClass l r (selectedFiveAncestorTripleLeft l r M)) =
      selectedRawCongruentFourAncestryObservation l r J N
        (selectedRawCongruentClass l r (selectedFiveAncestorTripleRight l r M)) := by
  rfl

/-- The sixth raw invariant detects two extra nested reverse
ancestor TRIPLES on the right, independent of the supplied M. -/
theorem selectedFiveAncestorTriple_countDiff
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenReverseAncestorTripleCount l r
        (selectedFiveAncestorTripleRight l r M) =
      selectedContextEighteenReverseAncestorTripleCount l r
        (selectedFiveAncestorTripleLeft l r M) + 2 := by
  rfl

/-- Five observation equality does NOT imply equality in the
separately defined v5.50 raw congruence quotient. -/
theorem selectedFiveAncestorTriple_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r (selectedFiveAncestorTripleLeft l r M) ≠
      selectedRawCongruentClass l r (selectedFiveAncestorTripleRight l r M) := by
  intro h
  have ht := congrArg
    (selectedRawCongruentReverseAncestorTripleOnQuotient l r J N) h
  change selectedContextEighteenReverseAncestorTripleCount l r
      (selectedFiveAncestorTripleLeft l r M) =
    selectedContextEighteenReverseAncestorTripleCount l r
      (selectedFiveAncestorTripleRight l r M) at ht
  rw [selectedFiveAncestorTriple_countDiff l r M] at ht
  omega

/-- No actual Type-valued NEW 19D comparison relates this pair. -/
theorem selectedFiveAncestorTriple_noComparison
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r J N
      (selectedFiveAncestorTripleLeft l r M)
      (selectedFiveAncestorTripleRight l r M)) := by
  rintro ⟨A⟩
  exact (selectedFiveAncestorTriple_classDistinct l r M) (Quotient.sound ⟨A⟩)

/-- The five-observation quotient map is not faithful in each
specified J-to-N fiber supplied with a genuine raw 18D witness M. -/
theorem selectedRawCongruentFive_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective (selectedRawCongruentFourAncestryObservation l r J N) := by
  intro hinj
  exact (selectedFiveAncestorTriple_classDistinct l r M)
    (hinj (selectedFiveAncestorTriple_fiveObservedEq l r M))

/-- No total left inverse can reconstruct all quotient classes from
the five numerical and trace observations in an inhabited exact fiber. -/
theorem selectedRawCongruentFive_noDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode : ((((List Bool × Nat) × Nat) × Nat) × Nat) →
        Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentFourAncestryObservation l r J N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedRawCongruentFive_notInjective l r M
  intro a b hab
  calc
    a = decode (selectedRawCongruentFourAncestryObservation l r J N a) :=
      (h a).symm
    _ = decode (selectedRawCongruentFourAncestryObservation l r J N b) :=
      congrArg decode hab
    _ = b := h b

/-- The new triple ancestry observable itself is not reconstructible
from the prior five quotient observables in an inhabited fiber. -/
theorem selectedRawCongruentFive_noTripleDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decodeTriple : ((((List Bool × Nat) × Nat) × Nat) × Nat) → Nat,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decodeTriple (selectedRawCongruentFourAncestryObservation l r J N q) =
          selectedRawCongruentReverseAncestorTripleOnQuotient l r J N q := by
  rintro ⟨decodeTriple, h⟩
  have ht :
      selectedRawCongruentReverseAncestorTripleOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedFiveAncestorTripleLeft l r M)) =
        selectedRawCongruentReverseAncestorTripleOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedFiveAncestorTripleRight l r M)) := by
    calc
      _ = decodeTriple (selectedRawCongruentFourAncestryObservation l r J N
            (selectedRawCongruentClass l r (selectedFiveAncestorTripleLeft l r M))) :=
        (h _).symm
      _ = decodeTriple (selectedRawCongruentFourAncestryObservation l r J N
            (selectedRawCongruentClass l r (selectedFiveAncestorTripleRight l r M))) :=
        congrArg decodeTriple (selectedFiveAncestorTriple_fiveObservedEq l r M)
      _ = _ := h _
  change selectedContextEighteenReverseAncestorTripleCount l r
      (selectedFiveAncestorTripleLeft l r M) =
    selectedContextEighteenReverseAncestorTripleCount l r
      (selectedFiveAncestorTripleRight l r M) at ht
  rw [selectedFiveAncestorTriple_countDiff l r M] at ht
  omega

/-- Genuine raw strict J supplies a witness for every specified
17D endomorphism J-to-J fiber, without asserting arbitrary J-to-N
inhabitance. -/
theorem selectedRawCongruentFive_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective (selectedRawCongruentFourAncestryObservation l r J J) :=
  selectedRawCongruentFive_notInjective l r (SelectedContextualEighteen.strict J)

/-- Six independently validated quotient observables. Nothing here
establishes injectivity or completeness of this larger tuple. -/
def selectedRawCongruentFiveTripleObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      (((((List Bool × Nat) × Nat) × Nat) × Nat) × Nat) :=
  fun q =>
    (selectedRawCongruentFourAncestryObservation l r J N q,
      selectedRawCongruentReverseAncestorTripleOnQuotient l r J N q)

/-- The sixth observation distinguishes THIS explicit counterexample,
without an assertion of global quotient completeness. -/
theorem selectedRawCongruentSix_tripleDistinguished
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentFiveTripleObservation l r J N
        (selectedRawCongruentClass l r (selectedFiveAncestorTripleLeft l r M)) ≠
      selectedRawCongruentFiveTripleObservation l r J N
        (selectedRawCongruentClass l r (selectedFiveAncestorTripleRight l r M)) := by
  intro h
  have ht := congrArg Prod.snd h
  change selectedContextEighteenReverseAncestorTripleCount l r
      (selectedFiveAncestorTripleLeft l r M) =
    selectedContextEighteenReverseAncestorTripleCount l r
      (selectedFiveAncestorTripleRight l r M) at ht
  rw [selectedFiveAncestorTriple_countDiff l r M] at ht
  omega

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenReverseAncestorTripleCount
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesReverseAncestorTriple
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesReverseAncestorTriple
#print axioms PentagonAdjoinedSixCell.selectedNineteenReverseAncestorTripleOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseAncestorTripleOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseAncestorTriple_onClass
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseAncestorTriple_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedFiveAncestorTripleLeft
#print axioms PentagonAdjoinedSixCell.selectedFiveAncestorTripleRight
#print axioms PentagonAdjoinedSixCell.selectedFiveAncestorTriple_fiveObservedEq
#print axioms PentagonAdjoinedSixCell.selectedFiveAncestorTriple_countDiff
#print axioms PentagonAdjoinedSixCell.selectedFiveAncestorTriple_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedFiveAncestorTriple_noComparison
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFive_notInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFive_noDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFive_noTripleDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFive_endomorphismNotInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFiveTripleObservation
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentSix_tripleDistinguished

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
