import KUOS.Architecture.QiWuxingGK5CHP77FiveObservationAncestorTripleV5_56

/-!
Qi v5.57 — a strictly nested reverse-ancestor QUADRUPLE remains
invisible to all SIX previously certified observations of the
independent v5.50 seven-constructor raw congruence quotient.

All original 18D Type-valued evidence, old selected19 comparisons,
independently adjoined v5.50 comparison generators, and original
16D/17D dependent boundaries remain untouched. This is a new module.

A finite raw syntax search found two genuine N-to-N suffixes each
containing SEVEN reverse constructors with the SAME adjacent count
2, reverse ancestor PAIR count 12, and ancestor TRIPLE count 10,
but different ancestor QUADRUPLE counts 3 and 5. Their outer raw
reverse flag is zero, as is the top flag of their right extensions
of an actual M : J -> N. Their ordered trace is empty.

After proving the new count survives all five original and seven
new comparison constructors, construct original/new quotient lifts
and show that the SIX-component observer cannot distinguish the
actual same-fiber pair while the seventh can.

No arbitrary fiber inhabitance, cross-fiber whiskering, 20D gluing,
seventh-observation completeness, or authority escalation is claimed.
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

/-- Number of ordered strictly nested chains of FOUR raw reverse
constructors. Adding a raw reverse introduces one quadruple for
each existing ancestor TRIPLE. Chain adds disjoint histories.
Inherited old evidence stays opaque, rather than being erased
or silently reinterpreted. -/
def selectedContextEighteenReverseAncestorQuadrupleCount (l r : W)
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
      selectedContextEighteenReverseAncestorQuadrupleCount l r M
  | .whiskerRight _ _ M _ =>
      selectedContextEighteenReverseAncestorQuadrupleCount l r M
  | .strict _ => 0
  | .reverse M =>
      selectedContextEighteenReverseAncestorQuadrupleCount l r M +
        selectedContextEighteenReverseAncestorTripleCount l r M
  | .chain M L =>
      selectedContextEighteenReverseAncestorQuadrupleCount l r M +
        selectedContextEighteenReverseAncestorQuadrupleCount l r L

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Invariance under the actual five original 19D constructors.
The two old unit constructors operate on inherited old18 proofs. -/
theorem selectedLocalNineteen_preservesReverseAncestorQuadruple
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenReverseAncestorQuadrupleCount l r M =
      selectedContextEighteenReverseAncestorQuadrupleCount l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- The new observation respects ALL seven independent v5.50
comparison constructors. The rawReverse constructor needs both
the induction hypothesis and the existing v5.56 ancestor TRIPLE
preservation; no unproved source equivalence is assumed. -/
theorem selectedRawCongruent_preservesReverseAncestorQuadruple
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenReverseAncestorQuadrupleCount l r M =
      selectedContextEighteenReverseAncestorQuadrupleCount l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesReverseAncestorQuadruple l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      exact congrArg₂ Nat.add ih
        (selectedRawCongruent_preservesReverseAncestorTriple l r A)
  | rawChainRight A X ih =>
      exact congrArg
        (fun n : Nat =>
          n + selectedContextEighteenReverseAncestorQuadrupleCount l r X) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun n : Nat =>
          selectedContextEighteenReverseAncestorQuadrupleCount l r X + n) ih

/-- Genuine lift on the ORIGINAL selected19 quotient. -/
def selectedNineteenReverseAncestorQuadrupleOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat :=
  Quotient.lift
    (selectedContextEighteenReverseAncestorQuadrupleCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesReverseAncestorQuadruple l r A)

/-- Separately certified lift on the NEW seven-constructor quotient. -/
def selectedRawCongruentReverseAncestorQuadrupleOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → Nat :=
  Quotient.lift
    (selectedContextEighteenReverseAncestorQuadrupleCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesReverseAncestorQuadruple l r A)

theorem selectedRawCongruentReverseAncestorQuadruple_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentReverseAncestorQuadrupleOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenReverseAncestorQuadrupleCount l r M := rfl

/-- Old-to-new quotient factorization holds on every actual class,
not just on chosen raw representatives. -/
theorem selectedRawCongruentReverseAncestorQuadruple_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentReverseAncestorQuadrupleOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenReverseAncestorQuadrupleOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Left genuine N-to-N suffix, displayed as
chain (reverse strict) (reverse (reverse (reverse
  (chain (reverse strict) (chain (reverse strict) (reverse strict)))))).
It contains seven raw reverse constructors in total. -/
def selectedSixQuadrupleSuffixLeft
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain
    (.reverse (.strict N))
    (.reverse (.reverse (.reverse
      (.chain
        (.reverse (.strict N))
        (.chain (.reverse (.strict N)) (.reverse (.strict N))))))

/-- Right genuine N-to-N suffix:
chain (reverse
  (chain (reverse strict)
    (chain (reverse strict)
      (reverse (reverse (reverse (chain (reverse strict) strict)))))))
  strict.
An interior strict right unit resets an adjacent-reverse flag,
but does not cancel any actual raw reversal. -/
def selectedSixQuadrupleSuffixRight
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain
    (.reverse
      (.chain
        (.reverse (.strict N))
        (.chain
          (.reverse (.strict N))
          (.reverse (.reverse (.reverse
            (.chain (.reverse (.strict N)) (.strict N)))))))
    (.strict N)

/-- Finite raw certificate on the ACTUAL typed N-to-N syntax.
Both suffixes: 7 reverse nodes, 2 adjacent, 12 ancestor PAIRS,
10 ancestor TRIPLES. Their quadruple counts are respectively 3
and 5, so the sixth previous observer loses this provenance. -/
theorem selectedSixQuadruple_suffixSignature
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenReverseCount l r
        (selectedSixQuadrupleSuffixLeft l r N) = 7 ∧
    selectedContextEighteenReverseCount l r
        (selectedSixQuadrupleSuffixRight l r N) = 7 ∧
    selectedContextEighteenAdjacentReverseCount l r
        (selectedSixQuadrupleSuffixLeft l r N) = 2 ∧
    selectedContextEighteenAdjacentReverseCount l r
        (selectedSixQuadrupleSuffixRight l r N) = 2 ∧
    selectedContextEighteenReverseAncestryCount l r
        (selectedSixQuadrupleSuffixLeft l r N) = 12 ∧
    selectedContextEighteenReverseAncestryCount l r
        (selectedSixQuadrupleSuffixRight l r N) = 12 ∧
    selectedContextEighteenReverseAncestorTripleCount l r
        (selectedSixQuadrupleSuffixLeft l r N) = 10 ∧
    selectedContextEighteenReverseAncestorTripleCount l r
        (selectedSixQuadrupleSuffixRight l r N) = 10 ∧
    selectedContextEighteenReverseAncestorQuadrupleCount l r
        (selectedSixQuadrupleSuffixLeft l r N) = 3 ∧
    selectedContextEighteenReverseAncestorQuadrupleCount l r
        (selectedSixQuadrupleSuffixRight l r N) = 5 := by
  exact ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

/-- Append the original left suffix to the genuine input M in the
SAME original exact 17D J-to-N fiber. -/
def selectedSixQuadrupleLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedSixQuadrupleSuffixLeft l r N)

/-- Append the genuinely different right suffix to the SAME M.
The input Type-valued evidence is retained byte-for-byte. -/
def selectedSixQuadrupleRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedSixQuadrupleSuffixRight l r N)

/-- Equality of the actual SIX-component observation of the new
quotient: ordered trace, reversal total, adjacency count, top
reverse flag, ancestor PAIR count, and ancestor TRIPLE count. -/
theorem selectedSixQuadruple_sixObservedEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentFiveTripleObservation l r J N
        (selectedRawCongruentClass l r (selectedSixQuadrupleLeft l r M)) =
      selectedRawCongruentFiveTripleObservation l r J N
        (selectedRawCongruentClass l r (selectedSixQuadrupleRight l r M)) := by
  rfl

/-- The seventh raw count separates these genuine proof histories.
The input M is unchanged on both sides; only the suffix differs. -/
theorem selectedSixQuadruple_countDiff
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenReverseAncestorQuadrupleCount l r
        (selectedSixQuadrupleRight l r M) =
      selectedContextEighteenReverseAncestorQuadrupleCount l r
        (selectedSixQuadrupleLeft l r M) + 2 := by
  rfl

/-- Identical six observations do not force an equality of NEW
quotient classes. This is a real quotient-class obstruction. -/
theorem selectedSixQuadruple_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r (selectedSixQuadrupleLeft l r M) ≠
      selectedRawCongruentClass l r (selectedSixQuadrupleRight l r M) := by
  intro h
  have hq := congrArg
    (selectedRawCongruentReverseAncestorQuadrupleOnQuotient l r J N) h
  change selectedContextEighteenReverseAncestorQuadrupleCount l r
      (selectedSixQuadrupleLeft l r M) =
    selectedContextEighteenReverseAncestorQuadrupleCount l r
      (selectedSixQuadrupleRight l r M) at hq
  rw [selectedSixQuadruple_countDiff l r M] at hq
  omega

/-- No genuine Type-valued v5.50 comparison can identify this pair,
not even through all seven generated contextual operations. -/
theorem selectedSixQuadruple_noComparison
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r J N
        (selectedSixQuadrupleLeft l r M)
        (selectedSixQuadrupleRight l r M)) := by
  rintro ⟨A⟩
  exact (selectedSixQuadruple_classDistinct l r M) (Quotient.sound ⟨A⟩)

/-- Noninjectivity of the actual six-observation quotient map in
every exact J-to-N fiber equipped with a given genuine raw M. -/
theorem selectedRawCongruentSix_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective (selectedRawCongruentFiveTripleObservation l r J N) := by
  intro hinj
  exact (selectedSixQuadruple_classDistinct l r M)
    (hinj (selectedSixQuadruple_sixObservedEq l r M))

/-- No complete decoder on an inhabited exact original fiber. -/
theorem selectedRawCongruentSix_noDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode : (((((List Bool × Nat) × Nat) × Nat) × Nat) × Nat) →
        Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentFiveTripleObservation l r J N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedRawCongruentSix_notInjective l r M
  intro a b hab
  calc
    a = decode (selectedRawCongruentFiveTripleObservation l r J N a) :=
      (h a).symm
    _ = decode (selectedRawCongruentFiveTripleObservation l r J N b) :=
      congrArg decode hab
    _ = b := h b

/-- The seventh invariant itself does not factor through the
six-component observer on an actually inhabited exact fiber. -/
theorem selectedRawCongruentSix_noQuadrupleDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decodeQuad : (((((List Bool × Nat) × Nat) × Nat) × Nat) × Nat) → Nat,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decodeQuad (selectedRawCongruentFiveTripleObservation l r J N q) =
          selectedRawCongruentReverseAncestorQuadrupleOnQuotient l r J N q := by
  rintro ⟨decodeQuad, h⟩
  have hq :
      selectedRawCongruentReverseAncestorQuadrupleOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedSixQuadrupleLeft l r M)) =
        selectedRawCongruentReverseAncestorQuadrupleOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedSixQuadrupleRight l r M)) := by
    calc
      _ = decodeQuad (selectedRawCongruentFiveTripleObservation l r J N
            (selectedRawCongruentClass l r (selectedSixQuadrupleLeft l r M))) :=
        (h _).symm
      _ = decodeQuad (selectedRawCongruentFiveTripleObservation l r J N
            (selectedRawCongruentClass l r (selectedSixQuadrupleRight l r M))) :=
        congrArg decodeQuad (selectedSixQuadruple_sixObservedEq l r M)
      _ = _ := h _
  change selectedContextEighteenReverseAncestorQuadrupleCount l r
      (selectedSixQuadrupleLeft l r M) =
    selectedContextEighteenReverseAncestorQuadrupleCount l r
      (selectedSixQuadrupleRight l r M) at hq
  rw [selectedSixQuadruple_countDiff l r M] at hq
  omega

/-- The genuine raw strict identity witnesses nonfaithfulness in
every specified J-to-J endomorphism fiber, with NO all-fiber claim. -/
theorem selectedRawCongruentSix_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective (selectedRawCongruentFiveTripleObservation l r J J) :=
  selectedRawCongruentSix_notInjective l r (SelectedContextualEighteen.strict J)

/-- A seventh, independently certified, quotient-level observation.
It is NOT asserted to classify the whole new quotient. -/
def selectedRawCongruentSixQuadrupleObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      ((((((List Bool × Nat) × Nat) × Nat) × Nat) × Nat) × Nat) :=
  fun q =>
    (selectedRawCongruentFiveTripleObservation l r J N q,
      selectedRawCongruentReverseAncestorQuadrupleOnQuotient l r J N q)

/-- Seventh observation separates the chosen raw pair only. -/
theorem selectedRawCongruentSeven_quadrupleDistinguished
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentSixQuadrupleObservation l r J N
        (selectedRawCongruentClass l r (selectedSixQuadrupleLeft l r M)) ≠
      selectedRawCongruentSixQuadrupleObservation l r J N
        (selectedRawCongruentClass l r (selectedSixQuadrupleRight l r M)) := by
  intro h
  have hq := congrArg Prod.snd h
  change selectedContextEighteenReverseAncestorQuadrupleCount l r
      (selectedSixQuadrupleLeft l r M) =
    selectedContextEighteenReverseAncestorQuadrupleCount l r
      (selectedSixQuadrupleRight l r M) at hq
  rw [selectedSixQuadruple_countDiff l r M] at hq
  omega

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenReverseAncestorQuadrupleCount
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesReverseAncestorQuadruple
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesReverseAncestorQuadruple
#print axioms PentagonAdjoinedSixCell.selectedNineteenReverseAncestorQuadrupleOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseAncestorQuadrupleOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseAncestorQuadruple_onClass
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseAncestorQuadruple_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedSixQuadrupleSuffixLeft
#print axioms PentagonAdjoinedSixCell.selectedSixQuadrupleSuffixRight
#print axioms PentagonAdjoinedSixCell.selectedSixQuadruple_suffixSignature
#print axioms PentagonAdjoinedSixCell.selectedSixQuadrupleLeft
#print axioms PentagonAdjoinedSixCell.selectedSixQuadrupleRight
#print axioms PentagonAdjoinedSixCell.selectedSixQuadruple_sixObservedEq
#print axioms PentagonAdjoinedSixCell.selectedSixQuadruple_countDiff
#print axioms PentagonAdjoinedSixCell.selectedSixQuadruple_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedSixQuadruple_noComparison
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentSix_notInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentSix_noDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentSix_noQuadrupleDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentSix_endomorphismNotInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentSixQuadrupleObservation
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentSeven_quadrupleDistinguished

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
