import KUOS.Architecture.QiWuxingGK5CHP77SevenObservationAncestorQuintupleV5_58

/-!
Qi v5.59 — natural-index reverse-ancestor tower and conditional
one-step obstruction transport, in the ORIGINAL exact 16D/17D fiber.

No replacement of the old18 Type values, the old selected19 proof
presentation, or the independent seven-generator v5.50 congruence.
The n=0 tower coordinate is a constant seed 1 (NOT a reverse count).
For every n+1, a raw reverse adds the previous coordinate, and
raw chains add their two histories. Inherited old18 is opaque.

A mismatch at level n can be transported to level n+1 by moving
one raw reverse from the left suffix to the right suffix, while
every coordinate up through n agrees if all preceding coordinates
agreed before the move. Both suffixes inhabit one genuine N-to-N
fiber, and quotient separation uses the genuine new comparison.

This theorem is conditional on an actually supplied base pair.
No universal nonempty-fiber, specific n=8 counterexample,
infinite-family witness, 20D gluing or authority claim.
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

/-- One raw-syntax fold for the next reverse-ancestor level.
The prior level is a genuinely indexed function of old18 evidence. -/
def selectedAncestorTowerStep (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (prev : ∀ {J N : SelectedContextualSeventeen W l r H K},
      SelectedContextualEighteen W l r J N → Nat)
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) : Nat :=
  match M with
  | .inherited _ => 0
  | .whiskerLeft _ _ _ M => selectedAncestorTowerStep l r prev M
  | .whiskerRight _ _ M _ => selectedAncestorTowerStep l r prev M
  | .strict _ => 0
  | .reverse M => selectedAncestorTowerStep l r prev M + prev M
  | .chain M L =>
      selectedAncestorTowerStep l r prev M +
        selectedAncestorTowerStep l r prev L

/-- A natural-indexed raw ancestor tower. Its artificial level zero
is 1 on any raw proof; level one counts reversals, higher levels
count successively nested reverse ancestry. -/
def selectedAncestorTowerCount (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U} :
    Nat → (∀ {J N : SelectedContextualSeventeen W l r H K},
      SelectedContextualEighteen W l r J N → Nat)
  | 0 => fun _ => 1
  | n + 1 =>
      selectedAncestorTowerStep l r (selectedAncestorTowerCount l r n)

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Every old selected19 comparison preserves any one-step fold.
Unit relations are confined to opaque inherited old18 leaves. -/
theorem selectedAncestorTowerStep_preservesOld
    (prev : ∀ {J' N' : SelectedContextualSeventeen W l r H K},
      SelectedContextualEighteen W l r J' N' → Nat)
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedAncestorTowerStep l r prev M =
      selectedAncestorTowerStep l r prev L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- If the previous level descends through the new comparison,
then the next fold does too. This checks all seven constructors,
including typed rawReverse and both typed raw-chain contexts. -/
theorem selectedAncestorTowerStep_preservesNew
    (prev : ∀ {J' N' : SelectedContextualSeventeen W l r H K},
      SelectedContextualEighteen W l r J' N' → Nat)
    (hprev : ∀ {J' N' : SelectedContextualSeventeen W l r H K}
      {M' L' : SelectedContextualEighteen W l r J' N'},
      SelectedRawCongruentNineteen W l r J' N' M' L' →
        prev M' = prev L')
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedAncestorTowerStep l r prev M =
      selectedAncestorTowerStep l r prev L := by
  induction A with
  | inherited A => exact selectedAncestorTowerStep_preservesOld l r prev A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih => exact congrArg₂ Nat.add ih (hprev A)
  | rawChainRight A X ih =>
      exact congrArg
        (fun n : Nat => n + selectedAncestorTowerStep l r prev X) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun n : Nat => selectedAncestorTowerStep l r prev X + n) ih

/-- All tower coordinates are original-selected19 invariants. -/
theorem selectedAncestorTower_preservesOld
    (n : Nat) {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedAncestorTowerCount l r n M =
      selectedAncestorTowerCount l r n L := by
  cases n with
  | zero => rfl
  | succ n =>
      exact selectedAncestorTowerStep_preservesOld l r
        (selectedAncestorTowerCount l r n) A

/-- All tower coordinates are independently invariant for the NEW
seven-constructor comparison, with no change to its generators. -/
theorem selectedAncestorTower_preservesNew (n : Nat) :
    ∀ {J' N' : SelectedContextualSeventeen W l r H K}
      {M L : SelectedContextualEighteen W l r J' N'},
      SelectedRawCongruentNineteen W l r J' N' M L →
        selectedAncestorTowerCount l r n M =
          selectedAncestorTowerCount l r n L := by
  induction n with
  | zero =>
      intro J' N' M L A
      rfl
  | succ n ih =>
      intro J' N' M L A
      exact selectedAncestorTowerStep_preservesNew l r
        (selectedAncestorTowerCount l r n)
        (by
          intro J'' N'' M' L' A'
          exact ih A') A

/-- Every natural-indexed tower count descends separately to
the original selected19 quotient. -/
def selectedAncestorTowerOnOldQuotient (n : Nat)
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat :=
  Quotient.lift (selectedAncestorTowerCount l r n) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedAncestorTower_preservesOld l r n A)

/-- Every tower count also descends through the independent new
seven-constructor raw congruence. -/
def selectedAncestorTowerOnNewQuotient (n : Nat)
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → Nat :=
  Quotient.lift (selectedAncestorTowerCount l r n) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedAncestorTower_preservesNew l r n A)

/-- The two independently justified quotient counts factor through
the old-to-new quotient projection on every old quotient class. -/
theorem selectedAncestorTower_factorsOld (n : Nat)
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedAncestorTowerOnNewQuotient l r n J N
        (selectedRawCongruentProject l r J N q) =
      selectedAncestorTowerOnOldQuotient l r n J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Both sides are GENUINE dependent N-to-N raw proofs. -/
def selectedAncestorShiftLeft
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualEighteen W l r N N) :
    SelectedContextualEighteen W l r N N :=
  .chain (.reverse A) B

def selectedAncestorShiftRight
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualEighteen W l r N N) :
    SelectedContextualEighteen W l r N N :=
  .chain A (.reverse B)

/-- If the two old levels agree at n, reversing opposite suffixes
makes their next level equal. This is a conditional compatibility
result, not the unproved existence of the required base witnesses. -/
theorem selectedAncestorShift_equalNext (n : Nat)
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualEighteen W l r N N)
    (h : selectedAncestorTowerCount l r n A =
      selectedAncestorTowerCount l r n B) :
    selectedAncestorTowerCount l r (n + 1)
        (selectedAncestorShiftLeft l r N A B) =
      selectedAncestorTowerCount l r (n + 1)
        (selectedAncestorShiftRight l r N A B) := by
  change
    (selectedAncestorTowerCount l r (n + 1) A +
        selectedAncestorTowerCount l r n A) +
        selectedAncestorTowerCount l r (n + 1) B =
      selectedAncestorTowerCount l r (n + 1) A +
        (selectedAncestorTowerCount l r (n + 1) B +
          selectedAncestorTowerCount l r n B)
  omega

/-- A true mismatch at level n is pushed one level higher by the
same shift, without identifying the underlying Type-valued proofs. -/
theorem selectedAncestorShift_unequalNext (n : Nat)
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualEighteen W l r N N)
    (h : selectedAncestorTowerCount l r n A ≠
      selectedAncestorTowerCount l r n B) :
    selectedAncestorTowerCount l r (n + 1)
        (selectedAncestorShiftLeft l r N A B) ≠
      selectedAncestorTowerCount l r (n + 1)
        (selectedAncestorShiftRight l r N A B) := by
  intro hshift
  have heq : selectedAncestorTowerCount l r n A =
      selectedAncestorTowerCount l r n B := by
    have hs :
        (selectedAncestorTowerCount l r (n + 1) A +
          selectedAncestorTowerCount l r n A) +
          selectedAncestorTowerCount l r (n + 1) B =
        selectedAncestorTowerCount l r (n + 1) A +
          (selectedAncestorTowerCount l r (n + 1) B +
            selectedAncestorTowerCount l r n B) := by
      exact hshift
    omega
  exact h heq

/-- Every finite tower prefix is preserved if the preceding prefix
was compatible; the new gap can remain at the next coordinate. -/
theorem selectedAncestorShift_prefixCompatible (n : Nat)
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualEighteen W l r N N)
    (h : ∀ k < n, selectedAncestorTowerCount l r k A =
      selectedAncestorTowerCount l r k B) :
    ∀ k ≤ n,
      selectedAncestorTowerCount l r k
          (selectedAncestorShiftLeft l r N A B) =
        selectedAncestorTowerCount l r k
          (selectedAncestorShiftRight l r N A B) := by
  intro k hk
  cases k with
  | zero => rfl
  | succ j =>
      exact selectedAncestorShift_equalNext l r j N A B
        (h j (by omega))

/-- Any actual n-level discrepancy produces two distinct new-quotient
classes at level n+1, with no Type-valued comparison between them. -/
theorem selectedAncestorShift_noNewComparison (n : Nat)
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualEighteen W l r N N)
    (h : selectedAncestorTowerCount l r n A ≠
      selectedAncestorTowerCount l r n B) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
        (selectedAncestorShiftLeft l r N A B)
        (selectedAncestorShiftRight l r N A B)) := by
  rintro ⟨comparison⟩
  exact (selectedAncestorShift_unequalNext l r n N A B h)
    (selectedAncestorTower_preservesNew l r (n + 1) comparison)

/-- Conditional finite-prefix obstruction: local equality of all
tower coordinates below n does not license class identification
when the first unequal count at n is retained as a witness. -/
theorem selectedAncestorShift_residualGate (n : Nat)
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualEighteen W l r N N)
    (hEq : ∀ k < n, selectedAncestorTowerCount l r k A =
      selectedAncestorTowerCount l r k B)
    (hNe : selectedAncestorTowerCount l r n A ≠
      selectedAncestorTowerCount l r n B) :
    (∀ k ≤ n,
      selectedAncestorTowerCount l r k
          (selectedAncestorShiftLeft l r N A B) =
        selectedAncestorTowerCount l r k
          (selectedAncestorShiftRight l r N A B)) ∧
      ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
        (selectedAncestorShiftLeft l r N A B)
        (selectedAncestorShiftRight l r N A B)) :=
  ⟨selectedAncestorShift_prefixCompatible l r n N A B hEq,
   selectedAncestorShift_noNewComparison l r n N A B hNe⟩

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedAncestorTowerStep
#print axioms PentagonAdjoinedSixCell.selectedAncestorTowerCount
#print axioms PentagonAdjoinedSixCell.selectedAncestorTowerStep_preservesOld
#print axioms PentagonAdjoinedSixCell.selectedAncestorTowerStep_preservesNew
#print axioms PentagonAdjoinedSixCell.selectedAncestorTower_preservesOld
#print axioms PentagonAdjoinedSixCell.selectedAncestorTower_preservesNew
#print axioms PentagonAdjoinedSixCell.selectedAncestorTowerOnOldQuotient
#print axioms PentagonAdjoinedSixCell.selectedAncestorTowerOnNewQuotient
#print axioms PentagonAdjoinedSixCell.selectedAncestorTower_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedAncestorShiftLeft
#print axioms PentagonAdjoinedSixCell.selectedAncestorShiftRight
#print axioms PentagonAdjoinedSixCell.selectedAncestorShift_equalNext
#print axioms PentagonAdjoinedSixCell.selectedAncestorShift_unequalNext
#print axioms PentagonAdjoinedSixCell.selectedAncestorShift_prefixCompatible
#print axioms PentagonAdjoinedSixCell.selectedAncestorShift_noNewComparison
#print axioms PentagonAdjoinedSixCell.selectedAncestorShift_residualGate

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
