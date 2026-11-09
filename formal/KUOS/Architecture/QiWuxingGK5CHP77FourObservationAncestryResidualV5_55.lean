import KUOS.Architecture.QiWuxingGK5CHP77TripleTopReverseResidualV5_54

/-!
Qi v5.55 — reverse-ancestry residual after FOUR certified observations.

Preserve the original contextual 18D proof Type, original selected19
comparison, and independent v5.50 seven-constructor raw congruence.
A NEW numerical observation counts pairs of raw reverse nodes where
one is a strict ancestor of the other, not merely adjacent reverses.
Inherited evidence is an opaque leaf, exactly as for ReverseCount.

For every supplied original M : J -> N, use the genuine raw terms
  A(M) = chain M (chain (reverse (strict N)) (reverse (strict N)))
  B(M) = selectedAdjacentReverseRight M   -- unchanged v5.47 term
       = chain M (reverse (chain (strict N) (reverse (strict N)))).
The full ordered trace, total reverse count, adjacent reverse count,
and top reverse flag all agree. The NEW ancestry count differs by one.
After proving its invariance under all SEVEN constructors, it descends
to the NEW quotient and separates these two quotient classes.

The resulting four-observation noninjectivity and decoder obstructions
are conditional on an actual witness in the specified exact J-to-N
fiber. A specified J supplies the endomorphism case through strict J.
No arbitrary fiber inhabitance, cross-fiber whiskering congruence,
20D gluing, five-observation completeness, or authority is asserted.
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

/-- Count ordered ancestor/descendant pairs of RAW reverse nodes.
An outer reverse contributes one pair for each reverse node below it.
Whiskering retains the count but does not assert any comparison between
independent fibers. The inside of inherited old evidence stays opaque. -/
def selectedContextEighteenReverseAncestryCount (l r : W)
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
  | .whiskerLeft _ _ _ M => selectedContextEighteenReverseAncestryCount l r M
  | .whiskerRight _ _ M _ => selectedContextEighteenReverseAncestryCount l r M
  | .strict _ => 0
  | .reverse M => selectedContextEighteenReverseAncestryCount l r M +
      selectedContextEighteenReverseCount l r M
  | .chain M L => selectedContextEighteenReverseAncestryCount l r M +
      selectedContextEighteenReverseAncestryCount l r L

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- All five original selected19 constructors preserve raw ancestry.
The actual unit generators operate on inherited old18 witnesses. -/
theorem selectedLocalNineteen_preservesReverseAncestry
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenReverseAncestryCount l r M =
      selectedContextEighteenReverseAncestryCount l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- Every constructor of the INDEPENDENT seven-constructor comparison
preserves ancestry. Raw reversal needs both ancestry equality and the
already certified equality of TOTAL raw reverse counts. -/
theorem selectedRawCongruent_preservesReverseAncestry
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenReverseAncestryCount l r M =
      selectedContextEighteenReverseAncestryCount l r L := by
  induction A with
  | inherited A => exact selectedLocalNineteen_preservesReverseAncestry l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      exact congrArg₂ Nat.add ih
        (selectedRawCongruent_preservesReverseCount l r A)
  | rawChainRight A X ih =>
      exact congrArg
        (fun n : Nat => n + selectedContextEighteenReverseAncestryCount l r X) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun n : Nat => selectedContextEighteenReverseAncestryCount l r X + n) ih

/-- A genuine observation of the ORIGINAL selected19 quotient. -/
def selectedNineteenReverseAncestryOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenReverseAncestryCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesReverseAncestry l r A)

/-- A separately justified lift to the coarser NEW raw-congruence
quotient; old quotient descent is not silently transferred. -/
def selectedRawCongruentReverseAncestryOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenReverseAncestryCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesReverseAncestry l r A)

theorem selectedRawCongruentReverseAncestry_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentReverseAncestryOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenReverseAncestryCount l r M := rfl

/-- Exact compatibility with the original-to-new quotient projection. -/
theorem selectedRawCongruentReverseAncestry_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentReverseAncestryOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenReverseAncestryOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Two reverse nodes in DIFFERENT branches of a genuine N-to-N
suffix. Preserve the actual input M and its complete dependent fiber. -/
def selectedFourAncestryLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (.chain (.reverse (.strict N)) (.reverse (.strict N)))

/-- Reuse the exact original v5.47 right-hand witness. Its two reverse
nodes are nonadjacent, but one is an ancestor of the other. -/
def selectedFourAncestryRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  selectedAdjacentReverseRight l r M

/-- Both quotient classes have identical FULL ordered trace, total
reverse count, adjacent count, AND top reverse flag. -/
theorem selectedFourAncestry_fourObservedEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentTripleTopReverseObservation l r J N
      (selectedRawCongruentClass l r (selectedFourAncestryLeft l r M)) =
    selectedRawCongruentTripleTopReverseObservation l r J N
      (selectedRawCongruentClass l r (selectedFourAncestryRight l r M)) := rfl

/-- The nested suffix contributes exactly ONE additional ancestral
reverse pair. The input M, whatever its own history, is unchanged. -/
theorem selectedFourAncestry_countDiff
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenReverseAncestryCount l r
        (selectedFourAncestryRight l r M) =
      selectedContextEighteenReverseAncestryCount l r
        (selectedFourAncestryLeft l r M) + 1 := rfl

/-- All four certified observations agree but the NEW classes differ. -/
theorem selectedFourAncestry_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r (selectedFourAncestryLeft l r M) ≠
      selectedRawCongruentClass l r (selectedFourAncestryRight l r M) := by
  intro h
  have hp := congrArg (selectedRawCongruentReverseAncestryOnQuotient l r J N) h
  change selectedContextEighteenReverseAncestryCount l r
      (selectedFourAncestryLeft l r M) =
    selectedContextEighteenReverseAncestryCount l r
      (selectedFourAncestryRight l r M) at hp
  rw [selectedFourAncestry_countDiff l r M] at hp
  omega

/-- There is no NEW Type-valued comparison between the actual pair. -/
theorem selectedFourAncestry_noComparison
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r J N
      (selectedFourAncestryLeft l r M) (selectedFourAncestryRight l r M)) := by
  rintro ⟨A⟩
  exact (selectedFourAncestry_classDistinct l r M) (Quotient.sound ⟨A⟩)

/-- Four-observation nonfaithfulness in each actually inhabited exact
fiber. No statement that arbitrary J-to-N fibers are inhabited. -/
theorem selectedRawCongruentFour_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedRawCongruentTripleTopReverseObservation l r J N) := by
  intro hinj
  exact (selectedFourAncestry_classDistinct l r M)
    (hinj (selectedFourAncestry_fourObservedEq l r M))

/-- No left-inverse decoder recovers all classes from the four values
in any specified exact fiber that has the given original witness M. -/
theorem selectedRawCongruentFour_noDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode : (((List Bool × Nat) × Nat) × Nat) →
        Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentTripleTopReverseObservation l r J N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedRawCongruentFour_notInjective l r M
  intro a b hab
  calc
    a = decode (selectedRawCongruentTripleTopReverseObservation l r J N a) :=
      (h a).symm
    _ = decode (selectedRawCongruentTripleTopReverseObservation l r J N b) :=
      congrArg decode hab
    _ = b := h b

/-- The ancestry observable itself is not reconstructible from the
four previous quotient observations on an actually inhabited fiber. -/
theorem selectedRawCongruentFour_noAncestryDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decodeAncestry : (((List Bool × Nat) × Nat) × Nat) → Nat,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decodeAncestry (selectedRawCongruentTripleTopReverseObservation l r J N q) =
          selectedRawCongruentReverseAncestryOnQuotient l r J N q := by
  rintro ⟨decodeAncestry, h⟩
  have hp :
      selectedRawCongruentReverseAncestryOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedFourAncestryLeft l r M)) =
        selectedRawCongruentReverseAncestryOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedFourAncestryRight l r M)) := by
    calc
      _ = decodeAncestry (selectedRawCongruentTripleTopReverseObservation l r J N
            (selectedRawCongruentClass l r (selectedFourAncestryLeft l r M))) :=
        (h _).symm
      _ = decodeAncestry (selectedRawCongruentTripleTopReverseObservation l r J N
            (selectedRawCongruentClass l r (selectedFourAncestryRight l r M))) :=
        congrArg decodeAncestry (selectedFourAncestry_fourObservedEq l r M)
      _ = _ := h _
  change selectedContextEighteenReverseAncestryCount l r
      (selectedFourAncestryLeft l r M) =
    selectedContextEighteenReverseAncestryCount l r
      (selectedFourAncestryRight l r M) at hp
  rw [selectedFourAncestry_countDiff l r M] at hp
  omega

/-- A given 17D endpoint supplies genuine strict identity evidence. -/
theorem selectedRawCongruentFour_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentTripleTopReverseObservation l r J J) :=
  selectedRawCongruentFour_notInjective l r (SelectedContextualEighteen.strict J)

/-- Add ancestry as a FIFTH independently justified observation.
This definition makes no completeness claim for the resulting tuple. -/
def selectedRawCongruentFourAncestryObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      ((((List Bool × Nat) × Nat) × Nat) × Nat) :=
  fun q =>
    (selectedRawCongruentTripleTopReverseObservation l r J N q,
      selectedRawCongruentReverseAncestryOnQuotient l r J N q)

/-- The fifth observation separates THIS explicit counterexample.
It is not a classification of every class in the new quotient. -/
theorem selectedRawCongruentFive_ancestryDistinguished
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentFourAncestryObservation l r J N
        (selectedRawCongruentClass l r (selectedFourAncestryLeft l r M)) ≠
      selectedRawCongruentFourAncestryObservation l r J N
        (selectedRawCongruentClass l r (selectedFourAncestryRight l r M)) := by
  intro h
  have hp := congrArg Prod.snd h
  change selectedContextEighteenReverseAncestryCount l r
      (selectedFourAncestryLeft l r M) =
    selectedContextEighteenReverseAncestryCount l r
      (selectedFourAncestryRight l r M) at hp
  rw [selectedFourAncestry_countDiff l r M] at hp
  omega

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenReverseAncestryCount
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesReverseAncestry
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesReverseAncestry
#print axioms PentagonAdjoinedSixCell.selectedNineteenReverseAncestryOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseAncestryOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseAncestry_onClass
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentReverseAncestry_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedFourAncestryLeft
#print axioms PentagonAdjoinedSixCell.selectedFourAncestryRight
#print axioms PentagonAdjoinedSixCell.selectedFourAncestry_fourObservedEq
#print axioms PentagonAdjoinedSixCell.selectedFourAncestry_countDiff
#print axioms PentagonAdjoinedSixCell.selectedFourAncestry_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedFourAncestry_noComparison
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFour_notInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFour_noDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFour_noAncestryDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFour_endomorphismNotInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFourAncestryObservation
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFive_ancestryDistinguished

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
