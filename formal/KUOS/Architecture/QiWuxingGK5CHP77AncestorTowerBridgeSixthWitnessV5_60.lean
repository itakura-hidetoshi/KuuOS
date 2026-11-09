import KUOS.Architecture.QiWuxingGK5CHP77AncestorTowerConditionalShiftV5_59

/-!
Qi v5.60 — exact typed equivalence of C1..C5 reverse-ancestor tower
with the five INDEPENDENTLY pre-existing certified raw proof counts.

Unlike name-based or numerical identification, each equality is
proved by structural induction over ALL six constructors of the
original 18D dependent Type, including both contextual whiskerings.
Old source, all independent comparisons, original Type evidence and
the 16D/17D fibers are not modified. The old/new quintuple quotient
maps match the tower C5 by independently justified Quotient.inductionOn.

The certified v5.58 N-to-N suffixes have tower values
(C1,C2,C3,C4,C5)=(15,31,32,18,4) and (15,31,32,18,6).
The v5.59 conditional shift is then instantiated at n=5, yielding
a new, ACTUAL typed N-to-N pair equal through C5 but differing by
exactly two in C6. No assertion is made yet that all eight OTHER
observation components of the resulting pair agree.

No arbitrary J-to-N inhabitance, cross-fiber comparison or 20D gluing.
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

/-- A genuine pointwise identity on ALL original dependent 18D evidence,
including raw left/right whiskering and opaque inherited proof leaves. -/
theorem selectedAncestorTower_eqReverseCount
    (M : SelectedContextualEighteen W l r J N) :
    selectedAncestorTowerCount l r 1 M =
      selectedContextEighteenReverseCount l r M := by
  induction M with
  | inherited M => rfl
  | whiskerLeft before F G M ih => exact ih
  | whiskerRight F G M after ih => exact ih
  | strict J => rfl
  | reverse M ih =>
      change selectedAncestorTowerCount l r 1 M +
          selectedAncestorTowerCount l r 0 M =
        selectedContextEighteenReverseCount l r M + 1
      rw [ih, selectedAncestorTower_zero l r M]
  | chain M L ih ih' =>
      change selectedAncestorTowerCount l r 1 M +
          selectedAncestorTowerCount l r 1 L =
        selectedContextEighteenReverseCount l r M + selectedContextEighteenReverseCount l r L
      rw [ih, ih']

/-- A genuine pointwise identity on ALL original dependent 18D evidence,
including raw left/right whiskering and opaque inherited proof leaves. -/
theorem selectedAncestorTower_eqAncestryCount
    (M : SelectedContextualEighteen W l r J N) :
    selectedAncestorTowerCount l r 2 M =
      selectedContextEighteenReverseAncestryCount l r M := by
  induction M with
  | inherited M => rfl
  | whiskerLeft before F G M ih => exact ih
  | whiskerRight F G M after ih => exact ih
  | strict J => rfl
  | reverse M ih =>
      change selectedAncestorTowerCount l r 2 M +
          selectedAncestorTowerCount l r 1 M =
        selectedContextEighteenReverseAncestryCount l r M + selectedContextEighteenReverseCount l r M
      rw [ih, selectedAncestorTower_eqReverseCount l r M]
  | chain M L ih ih' =>
      change selectedAncestorTowerCount l r 2 M +
          selectedAncestorTowerCount l r 2 L =
        selectedContextEighteenReverseAncestryCount l r M + selectedContextEighteenReverseAncestryCount l r L
      rw [ih, ih']

/-- A genuine pointwise identity on ALL original dependent 18D evidence,
including raw left/right whiskering and opaque inherited proof leaves. -/
theorem selectedAncestorTower_eqAncestorTripleCount
    (M : SelectedContextualEighteen W l r J N) :
    selectedAncestorTowerCount l r 3 M =
      selectedContextEighteenReverseAncestorTripleCount l r M := by
  induction M with
  | inherited M => rfl
  | whiskerLeft before F G M ih => exact ih
  | whiskerRight F G M after ih => exact ih
  | strict J => rfl
  | reverse M ih =>
      change selectedAncestorTowerCount l r 3 M +
          selectedAncestorTowerCount l r 2 M =
        selectedContextEighteenReverseAncestorTripleCount l r M + selectedContextEighteenReverseAncestryCount l r M
      rw [ih, selectedAncestorTower_eqAncestryCount l r M]
  | chain M L ih ih' =>
      change selectedAncestorTowerCount l r 3 M +
          selectedAncestorTowerCount l r 3 L =
        selectedContextEighteenReverseAncestorTripleCount l r M + selectedContextEighteenReverseAncestorTripleCount l r L
      rw [ih, ih']

/-- A genuine pointwise identity on ALL original dependent 18D evidence,
including raw left/right whiskering and opaque inherited proof leaves. -/
theorem selectedAncestorTower_eqAncestorQuadrupleCount
    (M : SelectedContextualEighteen W l r J N) :
    selectedAncestorTowerCount l r 4 M =
      selectedContextEighteenReverseAncestorQuadrupleCount l r M := by
  induction M with
  | inherited M => rfl
  | whiskerLeft before F G M ih => exact ih
  | whiskerRight F G M after ih => exact ih
  | strict J => rfl
  | reverse M ih =>
      change selectedAncestorTowerCount l r 4 M +
          selectedAncestorTowerCount l r 3 M =
        selectedContextEighteenReverseAncestorQuadrupleCount l r M + selectedContextEighteenReverseAncestorTripleCount l r M
      rw [ih, selectedAncestorTower_eqAncestorTripleCount l r M]
  | chain M L ih ih' =>
      change selectedAncestorTowerCount l r 4 M +
          selectedAncestorTowerCount l r 4 L =
        selectedContextEighteenReverseAncestorQuadrupleCount l r M + selectedContextEighteenReverseAncestorQuadrupleCount l r L
      rw [ih, ih']

/-- A genuine pointwise identity on ALL original dependent 18D evidence,
including raw left/right whiskering and opaque inherited proof leaves. -/
theorem selectedAncestorTower_eqAncestorQuintupleCount
    (M : SelectedContextualEighteen W l r J N) :
    selectedAncestorTowerCount l r 5 M =
      selectedContextEighteenReverseAncestorQuintupleCount l r M := by
  induction M with
  | inherited M => rfl
  | whiskerLeft before F G M ih => exact ih
  | whiskerRight F G M after ih => exact ih
  | strict J => rfl
  | reverse M ih =>
      change selectedAncestorTowerCount l r 5 M +
          selectedAncestorTowerCount l r 4 M =
        selectedContextEighteenReverseAncestorQuintupleCount l r M + selectedContextEighteenReverseAncestorQuadrupleCount l r M
      rw [ih, selectedAncestorTower_eqAncestorQuadrupleCount l r M]
  | chain M L ih ih' =>
      change selectedAncestorTowerCount l r 5 M +
          selectedAncestorTowerCount l r 5 L =
        selectedContextEighteenReverseAncestorQuintupleCount l r M + selectedContextEighteenReverseAncestorQuintupleCount l r L
      rw [ih, ih']

/-- The numerical C5 quotient observer agrees with the independent
v5.58 quintuple quotient observer on every genuinely new class. -/
theorem selectedAncestorTower_v558NewQuotientBridge
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedRawCongruentSetoid l r J N)) :
    selectedAncestorTowerOnNewQuotient l r 5 J N q =
      selectedRawCongruentReverseAncestorQuintupleOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => exact selectedAncestorTower_eqAncestorQuintupleCount l r M

/-- An independent bridge on the ORIGINAL selected19 quotient. -/
theorem selectedAncestorTower_v558OldQuotientBridge
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedAncestorTowerOnOldQuotient l r 5 J N q =
      selectedNineteenReverseAncestorQuintupleOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => exact selectedAncestorTower_eqAncestorQuintupleCount l r M

/-- The genuinely typed v5.58 loop witnesses, not newly imagined
numerical classes, realize the indicated five levels of the tower. -/
theorem selectedSevenQuintuple_towerSuffixSignature
    (N : SelectedContextualSeventeen W l r H K) :
    selectedAncestorTowerCount l r 1
        (selectedSevenQuintupleSuffixLeft l r N) = 15 ∧
    selectedAncestorTowerCount l r 1
        (selectedSevenQuintupleSuffixRight l r N) = 15 ∧
    selectedAncestorTowerCount l r 2
        (selectedSevenQuintupleSuffixLeft l r N) = 31 ∧
    selectedAncestorTowerCount l r 2
        (selectedSevenQuintupleSuffixRight l r N) = 31 ∧
    selectedAncestorTowerCount l r 3
        (selectedSevenQuintupleSuffixLeft l r N) = 32 ∧
    selectedAncestorTowerCount l r 3
        (selectedSevenQuintupleSuffixRight l r N) = 32 ∧
    selectedAncestorTowerCount l r 4
        (selectedSevenQuintupleSuffixLeft l r N) = 18 ∧
    selectedAncestorTowerCount l r 4
        (selectedSevenQuintupleSuffixRight l r N) = 18 ∧
    selectedAncestorTowerCount l r 5
        (selectedSevenQuintupleSuffixLeft l r N) = 4 ∧
    selectedAncestorTowerCount l r 5
        (selectedSevenQuintupleSuffixRight l r N) = 6 := by
  rcases selectedSevenQuintuple_suffixSignature l r N with
    ⟨hRL, hRR, _, _, hPL, hPR, hTL, hTR, hQL, hQR, hFL, hFR⟩
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · exact (selectedAncestorTower_eqReverseCount l r
        (selectedSevenQuintupleSuffixLeft l r N)).trans hRL
  · exact (selectedAncestorTower_eqReverseCount l r
        (selectedSevenQuintupleSuffixRight l r N)).trans hRR
  · exact (selectedAncestorTower_eqAncestryCount l r
        (selectedSevenQuintupleSuffixLeft l r N)).trans hPL
  · exact (selectedAncestorTower_eqAncestryCount l r
        (selectedSevenQuintupleSuffixRight l r N)).trans hPR
  · exact (selectedAncestorTower_eqAncestorTripleCount l r
        (selectedSevenQuintupleSuffixLeft l r N)).trans hTL
  · exact (selectedAncestorTower_eqAncestorTripleCount l r
        (selectedSevenQuintupleSuffixRight l r N)).trans hTR
  · exact (selectedAncestorTower_eqAncestorQuadrupleCount l r
        (selectedSevenQuintupleSuffixLeft l r N)).trans hQL
  · exact (selectedAncestorTower_eqAncestorQuadrupleCount l r
        (selectedSevenQuintupleSuffixRight l r N)).trans hQR
  · exact (selectedAncestorTower_eqAncestorQuintupleCount l r
        (selectedSevenQuintupleSuffixLeft l r N)).trans hFL
  · exact (selectedAncestorTower_eqAncestorQuintupleCount l r
        (selectedSevenQuintupleSuffixRight l r N)).trans hFR

/-- The original v5.58 pair is identical at all four preceding
tower levels, but separates at C5. This is a specific witness for
the hypotheses of the general v5.59 conditional shift. -/
theorem selectedSevenQuintuple_towerFirstGap
    (N : SelectedContextualSeventeen W l r H K) :
    (∀ k < 5,
      selectedAncestorTowerCount l r k
          (selectedSevenQuintupleSuffixLeft l r N) =
        selectedAncestorTowerCount l r k
          (selectedSevenQuintupleSuffixRight l r N)) ∧
      selectedAncestorTowerCount l r 5
          (selectedSevenQuintupleSuffixLeft l r N) ≠
        selectedAncestorTowerCount l r 5
          (selectedSevenQuintupleSuffixRight l r N) := by
  rcases selectedSevenQuintuple_towerSuffixSignature l r N with
    ⟨h1L, h1R, h2L, h2R, h3L, h3R, h4L, h4R, h5L, h5R⟩
  constructor
  · intro k hk
    have hchoices : k = 0 ∨ k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 := by
      omega
    rcases hchoices with h0 | h1 | h2 | h3 | h4
    · subst k
      exact (selectedAncestorTower_zero l r
        (selectedSevenQuintupleSuffixLeft l r N)).trans
        (selectedAncestorTower_zero l r
          (selectedSevenQuintupleSuffixRight l r N)).symm
    · subst k
      exact h1L.trans h1R.symm
    · subst k
      exact h2L.trans h2R.symm
    · subst k
      exact h3L.trans h3R.symm
    · subst k
      exact h4L.trans h4R.symm
  · intro heq
    rw [h5L, h5R] at heq
    omega

/-- Exact raw, same-endpoint loop pair obtained by a second swap of
one reversal: it is not an asserted comparison between fibers. -/
def selectedEightTowerShiftLeft
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  selectedAncestorShiftLeft l r N
    (selectedSevenQuintupleSuffixLeft l r N)
    (selectedSevenQuintupleSuffixRight l r N)

def selectedEightTowerShiftRight
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  selectedAncestorShiftRight l r N
    (selectedSevenQuintupleSuffixLeft l r N)
    (selectedSevenQuintupleSuffixRight l r N)

/-- On every explicitly supplied N, these two ACTUAL raw loops have
all coordinates C0..C5 equal, yet genuine typed congruence does not
relate them (the sixth level has a certified residual mismatch). -/
theorem selectedEightTowerShift_residualGate
    (N : SelectedContextualSeventeen W l r H K) :
    (∀ k ≤ 5,
      selectedAncestorTowerCount l r k (selectedEightTowerShiftLeft l r N) =
        selectedAncestorTowerCount l r k (selectedEightTowerShiftRight l r N)) ∧
      ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
          (selectedEightTowerShiftLeft l r N)
          (selectedEightTowerShiftRight l r N)) := by
  rcases selectedSevenQuintuple_towerFirstGap l r N with ⟨hEq, hNe⟩
  exact selectedAncestorShift_residualGate l r 5 N
    (selectedSevenQuintupleSuffixLeft l r N)
    (selectedSevenQuintupleSuffixRight l r N) hEq hNe

/-- The new sixth ancestor-chain gap is exactly TWO, not merely
nonzero. The two old v5.58 quintuple suffix certificates are reused. -/
theorem selectedEightTowerShift_sixthGap
    (N : SelectedContextualSeventeen W l r H K) :
    selectedAncestorTowerCount l r 6 (selectedEightTowerShiftRight l r N) =
      selectedAncestorTowerCount l r 6 (selectedEightTowerShiftLeft l r N) + 2 := by
  rcases selectedSevenQuintuple_towerSuffixSignature l r N with
    ⟨_, _, _, _, _, _, _, _, h5L, h5R⟩
  change
    (selectedAncestorTowerCount l r 6 (selectedSevenQuintupleSuffixLeft l r N) +
      selectedAncestorTowerCount l r 6 (selectedSevenQuintupleSuffixRight l r N) +
        selectedAncestorTowerCount l r 5 (selectedSevenQuintupleSuffixRight l r N)) =
      (selectedAncestorTowerCount l r 6 (selectedSevenQuintupleSuffixLeft l r N) +
        selectedAncestorTowerCount l r 5 (selectedSevenQuintupleSuffixLeft l r N) +
        selectedAncestorTowerCount l r 6 (selectedSevenQuintupleSuffixRight l r N)) + 2
  rw [h5L, h5R]
  omega

/-- Real old18 proof M:J→N extends the same N-loop witness to its
ORIGINAL exact dependent J→N fiber without inventing inhabitants. -/
def selectedEightTowerFiberLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedEightTowerShiftLeft l r N)

def selectedEightTowerFiberRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedEightTowerShiftRight l r N)

/-- Every supplied original M yields C6 residual +2 in the same
J→N exact original 16D/17D fiber, not merely a numerical surrogate. -/
theorem selectedEightTowerFiber_sixthGap
    (M : SelectedContextualEighteen W l r J N) :
    selectedAncestorTowerCount l r 6 (selectedEightTowerFiberRight l r M) =
      selectedAncestorTowerCount l r 6 (selectedEightTowerFiberLeft l r M) + 2 := by
  change selectedAncestorTowerCount l r 6 M +
    selectedAncestorTowerCount l r 6 (selectedEightTowerShiftRight l r N) =
      (selectedAncestorTowerCount l r 6 M +
        selectedAncestorTowerCount l r 6 (selectedEightTowerShiftLeft l r N)) + 2
  rw [selectedEightTowerShift_sixthGap l r N]
  omega

/-- The true quotient classes are distinct in any supplied original
J→N fiber, even though all tower coordinates C0..C5 agree. -/
theorem selectedEightTowerFiber_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r (selectedEightTowerFiberLeft l r M) ≠
      selectedRawCongruentClass l r (selectedEightTowerFiberRight l r M) := by
  intro h
  have hc := congrArg
    (selectedAncestorTowerOnNewQuotient l r 6 J N) h
  change selectedAncestorTowerCount l r 6
      (selectedEightTowerFiberLeft l r M) =
    selectedAncestorTowerCount l r 6
      (selectedEightTowerFiberRight l r M) at hc
  rw [selectedEightTowerFiber_sixthGap l r M] at hc
  omega

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedAncestorTower_eqReverseCount
#print axioms PentagonAdjoinedSixCell.selectedAncestorTower_eqAncestryCount
#print axioms PentagonAdjoinedSixCell.selectedAncestorTower_eqAncestorTripleCount
#print axioms PentagonAdjoinedSixCell.selectedAncestorTower_eqAncestorQuadrupleCount
#print axioms PentagonAdjoinedSixCell.selectedAncestorTower_eqAncestorQuintupleCount
#print axioms PentagonAdjoinedSixCell.selectedAncestorTower_v558NewQuotientBridge
#print axioms PentagonAdjoinedSixCell.selectedAncestorTower_v558OldQuotientBridge
#print axioms PentagonAdjoinedSixCell.selectedSevenQuintuple_towerSuffixSignature
#print axioms PentagonAdjoinedSixCell.selectedSevenQuintuple_towerFirstGap
#print axioms PentagonAdjoinedSixCell.selectedEightTowerShiftLeft
#print axioms PentagonAdjoinedSixCell.selectedEightTowerShiftRight
#print axioms PentagonAdjoinedSixCell.selectedEightTowerShift_residualGate
#print axioms PentagonAdjoinedSixCell.selectedEightTowerShift_sixthGap
#print axioms PentagonAdjoinedSixCell.selectedEightTowerFiberLeft
#print axioms PentagonAdjoinedSixCell.selectedEightTowerFiberRight
#print axioms PentagonAdjoinedSixCell.selectedEightTowerFiber_sixthGap
#print axioms PentagonAdjoinedSixCell.selectedEightTowerFiber_classDistinct

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
