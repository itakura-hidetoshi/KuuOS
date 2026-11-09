import KUOS.Architecture.QiWuxingGK5CHP77EightObservationSixthAncestorResidualV5_61

/-!
Qi v5.62 — GENUINE nine-observation collision with a seventh
reverse-ancestor residual in the original exact dependent 16D/17D fiber.

The already-certified Qi v5.61 loop pair has all eight independent
quotient observations equal, tower coordinates C0..C5 equal, and C6
different by exactly +2. We move one further reverse from the left
suffix to the right suffix in the original raw 18D Type, and prove:
* equal original trace, adjacency, top reverse flag, and C1..C5;
* equal newly added ninth C6 quotient observation;
* exact C7 residual +2, preserving true quotient class inequality;
* noninjectivity of the actual nine-observer and failure of a C7 decoder;
* a tenth C7 coordinate distinguishes THIS pair, not all classes.

A source top-tag compatibility proof is essential: the two v5.60
suffixes are chains and hence both have top flag zero. No assumption
about an arbitrary heterogeneous fiber is made; an actual M:J→N is
required, while J→J is inhabited by the genuine strict constructor.

No global ten-observer completeness, all-n family, or 20D descent.
All old proof values, old/new comparisons, source imports, root107,
pins and protected PR #1558 remain untouched.
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

/-- The THIRD genuine pair of N→N raw loops is a further swap of
a reversal on the v5.60 pair. No numerical or quotient surrogate. -/
def selectedNineTowerShiftLeft
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  selectedAncestorShiftLeft l r N
    (selectedEightTowerShiftLeft l r N)
    (selectedEightTowerShiftRight l r N)

def selectedNineTowerShiftRight
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  selectedAncestorShiftRight l r N
    (selectedEightTowerShiftLeft l r N)
    (selectedEightTowerShiftRight l r N)

/-- All C0..C6 values of the third pair agree. This uses only the
certified C0..C5 equality of the previous pair, not an invented C6
assumption on that pair. -/
theorem selectedNineTowerShift_prefix
    (N : SelectedContextualSeventeen W l r H K) :
    ∀ k ≤ 6,
      selectedAncestorTowerCount l r k (selectedNineTowerShiftLeft l r N) =
        selectedAncestorTowerCount l r k (selectedNineTowerShiftRight l r N) := by
  intro k hk
  exact selectedAncestorShift_prefixCompatible l r 6 N
    (selectedEightTowerShiftLeft l r N)
    (selectedEightTowerShiftRight l r N)
    (by
      intro j hj
      exact (selectedEightTowerShift_residualGate l r N).1 j (by omega))
    k hk

/-- Abstract exact gap transport at arbitrary natural level, proved
on actual typed original raw proofs. Never unfold the large suffixes. -/
theorem selectedAncestorShift_exactTwoGap (n : Nat)
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualEighteen W l r N N)
    (h : selectedAncestorTowerCount l r n B =
      selectedAncestorTowerCount l r n A + 2) :
    selectedAncestorTowerCount l r (n + 1)
        (selectedAncestorShiftRight l r N A B) =
      selectedAncestorTowerCount l r (n + 1)
        (selectedAncestorShiftLeft l r N A B) + 2 := by
  change
    selectedAncestorTowerCount l r (n + 1) A +
      (selectedAncestorTowerCount l r (n + 1) B +
        selectedAncestorTowerCount l r n B) =
      (selectedAncestorTowerCount l r (n + 1) A +
        selectedAncestorTowerCount l r n A +
        selectedAncestorTowerCount l r (n + 1) B) + 2
  rw [h]
  omega

/-- The next, seventh, raw ancestor count differs by EXACTLY two
on the certified original N→N proof values. -/
theorem selectedNineTowerShift_seventhGap
    (N : SelectedContextualSeventeen W l r H K) :
    selectedAncestorTowerCount l r 7 (selectedNineTowerShiftRight l r N) =
      selectedAncestorTowerCount l r 7 (selectedNineTowerShiftLeft l r N) + 2 :=
  selectedAncestorShift_exactTwoGap l r 6 N
    (selectedEightTowerShiftLeft l r N)
    (selectedEightTowerShiftRight l r N)
    (selectedEightTowerShift_sixthGap l r N)

/-- Unlike an arbitrary pair of loops, BOTH v5.60 source loops
are visibly raw chains, so the exact top-flag compatibility gate
for the adjacent-reversal observation is satisfied. -/
theorem selectedEightTowerShift_bothTopZero
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenTopReverseFlag l r (selectedEightTowerShiftLeft l r N) = 0 ∧
      selectedContextEighteenTopReverseFlag l r (selectedEightTowerShiftRight l r N) = 0 := by
  exact ⟨rfl, rfl⟩

/-- All actual EIGHT independent raw invariants agree on the new
third-shift pair, as well as its C6 coordinate. The fifth-count
bridges from v5.60 are pointwise identities on the original 18D Type. -/
theorem selectedNineTowerShift_eightSignature
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawEightSignature l r
      (selectedNineTowerShiftLeft l r N)
      (selectedNineTowerShiftRight l r N) := by
  let A : SelectedContextualEighteen W l r N N :=
    selectedEightTowerShiftLeft l r N
  let B : SelectedContextualEighteen W l r N N :=
    selectedEightTowerShiftRight l r N
  let X : SelectedContextualEighteen W l r N N :=
    selectedNineTowerShiftLeft l r N
  let Y : SelectedContextualEighteen W l r N N :=
    selectedNineTowerShiftRight l r N
  have hprefix : ∀ k ≤ 6,
      selectedAncestorTowerCount l r k X =
        selectedAncestorTowerCount l r k Y :=
    selectedNineTowerShift_prefix l r N
  have hAB : selectedContextEighteenTopReverseFlag l r A =
      selectedContextEighteenTopReverseFlag l r B := by
    rcases selectedEightTowerShift_bothTopZero l r N with ⟨hA, hB⟩
    exact hA.trans hB.symm
  have hTrace : selectedContextEighteenTrace l r X =
      selectedContextEighteenTrace l r Y :=
    selectedAncestorShift_traceEq l r N A B
  have hAdjacent : selectedContextEighteenAdjacentReverseCount l r X =
      selectedContextEighteenAdjacentReverseCount l r Y :=
    selectedAncestorShift_adjacentIfTopEq l r N A B hAB
  have hTop : selectedContextEighteenTopReverseFlag l r X =
      selectedContextEighteenTopReverseFlag l r Y := by
    rcases selectedAncestorShift_bothTopZero l r N A B with ⟨hx, hy⟩
    exact hx.trans hy.symm
  have hReverse : selectedContextEighteenReverseCount l r X =
      selectedContextEighteenReverseCount l r Y :=
    (selectedAncestorTower_eqReverseCount l r X).symm.trans
      ((hprefix 1 (by omega)).trans (selectedAncestorTower_eqReverseCount l r Y))
  have hPair : selectedContextEighteenReverseAncestryCount l r X =
      selectedContextEighteenReverseAncestryCount l r Y :=
    (selectedAncestorTower_eqAncestryCount l r X).symm.trans
      ((hprefix 2 (by omega)).trans (selectedAncestorTower_eqAncestryCount l r Y))
  have hTriple : selectedContextEighteenReverseAncestorTripleCount l r X =
      selectedContextEighteenReverseAncestorTripleCount l r Y :=
    (selectedAncestorTower_eqAncestorTripleCount l r X).symm.trans
      ((hprefix 3 (by omega)).trans (selectedAncestorTower_eqAncestorTripleCount l r Y))
  have hQuadruple : selectedContextEighteenReverseAncestorQuadrupleCount l r X =
      selectedContextEighteenReverseAncestorQuadrupleCount l r Y :=
    (selectedAncestorTower_eqAncestorQuadrupleCount l r X).symm.trans
      ((hprefix 4 (by omega)).trans (selectedAncestorTower_eqAncestorQuadrupleCount l r Y))
  have hQuintuple : selectedContextEighteenReverseAncestorQuintupleCount l r X =
      selectedContextEighteenReverseAncestorQuintupleCount l r Y :=
    (selectedAncestorTower_eqAncestorQuintupleCount l r X).symm.trans
      ((hprefix 5 (by omega)).trans (selectedAncestorTower_eqAncestorQuintupleCount l r Y))
  exact ⟨hTrace, hReverse, hAdjacent, hTop,
    hPair, hTriple, hQuadruple, hQuintuple⟩

/-- An existing genuine M:J→N carries both loops into that SAME
dependent fiber, without claiming every heterogenous fiber inhabited. -/
def selectedNineTowerFiberLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedNineTowerShiftLeft l r N)

def selectedNineTowerFiberRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedNineTowerShiftRight l r N)

/-- Right concatenation preserves all eight real observations. -/
theorem selectedNineTowerFiber_eightSignature
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawEightSignature l r
      (selectedNineTowerFiberLeft l r M)
      (selectedNineTowerFiberRight l r M) :=
  selectedRawEightSignature_rightChain l r M
    (selectedNineTowerShiftLeft l r N)
    (selectedNineTowerShiftRight l r N)
    (selectedNineTowerShift_eightSignature l r N)

/-- The true ninth observable C6 is also equal in the original fiber. -/
theorem selectedNineTowerFiber_sixthEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedAncestorTowerCount l r 6 (selectedNineTowerFiberLeft l r M) =
      selectedAncestorTowerCount l r 6 (selectedNineTowerFiberRight l r M) := by
  change selectedAncestorTowerCount l r 6 M +
      selectedAncestorTowerCount l r 6 (selectedNineTowerShiftLeft l r N) =
    selectedAncestorTowerCount l r 6 M +
      selectedAncestorTowerCount l r 6 (selectedNineTowerShiftRight l r N)
  exact congrArg
    (fun x : Nat => selectedAncestorTowerCount l r 6 M + x)
    (selectedNineTowerShift_prefix l r N 6 (by omega))

/-- Yet the seventh count is exactly 2 larger on the right. -/
theorem selectedNineTowerFiber_seventhGap
    (M : SelectedContextualEighteen W l r J N) :
    selectedAncestorTowerCount l r 7 (selectedNineTowerFiberRight l r M) =
      selectedAncestorTowerCount l r 7 (selectedNineTowerFiberLeft l r M) + 2 := by
  change selectedAncestorTowerCount l r 7 M +
      selectedAncestorTowerCount l r 7 (selectedNineTowerShiftRight l r N) =
    (selectedAncestorTowerCount l r 7 M +
      selectedAncestorTowerCount l r 7 (selectedNineTowerShiftLeft l r N)) + 2
  rw [selectedNineTowerShift_seventhGap l r N]
  omega

/-- The genuine new seven-constructor quotient classes are distinct
in every supplied actual dependent J→N fiber. -/
theorem selectedNineTowerFiber_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r (selectedNineTowerFiberLeft l r M) ≠
      selectedRawCongruentClass l r (selectedNineTowerFiberRight l r M) := by
  intro h
  have hc := congrArg (selectedAncestorTowerOnNewQuotient l r 7 J N) h
  change selectedAncestorTowerCount l r 7 (selectedNineTowerFiberLeft l r M) =
    selectedAncestorTowerCount l r 7 (selectedNineTowerFiberRight l r M) at hc
  rw [selectedNineTowerFiber_seventhGap l r M] at hc
  omega

/-- The actual NINE-component observer from v5.61 agrees on two
distinct original raw quotient classes; its ninth C6 is not lost. -/
theorem selectedNineTowerFiber_nineObservedEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentNineObservation l r J N
        (selectedRawCongruentClass l r (selectedNineTowerFiberLeft l r M)) =
      selectedRawCongruentNineObservation l r J N
        (selectedRawCongruentClass l r (selectedNineTowerFiberRight l r M)) := by
  apply Prod.ext
  · exact selectedRawEightSignature_toObservation l r
      (selectedNineTowerFiberLeft l r M)
      (selectedNineTowerFiberRight l r M)
      (selectedNineTowerFiber_eightSignature l r M)
  · change selectedAncestorTowerCount l r 6 (selectedNineTowerFiberLeft l r M) =
      selectedAncestorTowerCount l r 6 (selectedNineTowerFiberRight l r M)
    exact selectedNineTowerFiber_sixthEq l r M

/-- Nine certified quotient measurements are not globally injective
on any specified original fiber carrying one genuine raw M:J→N. -/
theorem selectedRawCongruentNine_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective (selectedRawCongruentNineObservation l r J N) := by
  intro hinj
  exact (selectedNineTowerFiber_classDistinct l r M)
    (hinj (selectedNineTowerFiber_nineObservedEq l r M))

/-- A genuine strict J→J raw proof gives a witness in EVERY
specified endomorphism fiber, and nowhere else is inhabitance assumed. -/
theorem selectedRawCongruentNine_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective (selectedRawCongruentNineObservation l r J J) :=
  selectedRawCongruentNine_notInjective l r
    (SelectedContextualEighteen.strict J)

/-- The codomain is merely an alias of the already-established
ninth observer type: no new comparison or quotient is introduced. -/
abbrev selectedRawNineObservationValue : Type :=
  ((((((((List Bool × Nat) × Nat) × Nat) × Nat) × Nat) × Nat) × Nat) × Nat)

/-- No deterministic C7 recovery from NINE observations on any
actual raw fiber; the proof uses the certified +2 C7 residual. -/
theorem selectedRawCongruentNine_noSeventhDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decodeSeven : selectedRawNineObservationValue → Nat,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decodeSeven (selectedRawCongruentNineObservation l r J N q) =
          selectedAncestorTowerOnNewQuotient l r 7 J N q := by
  rintro ⟨decodeSeven, h⟩
  have hc :
      selectedAncestorTowerOnNewQuotient l r 7 J N
          (selectedRawCongruentClass l r (selectedNineTowerFiberLeft l r M)) =
        selectedAncestorTowerOnNewQuotient l r 7 J N
          (selectedRawCongruentClass l r (selectedNineTowerFiberRight l r M)) := by
    calc
      _ = decodeSeven (selectedRawCongruentNineObservation l r J N
            (selectedRawCongruentClass l r (selectedNineTowerFiberLeft l r M))) :=
        (h _).symm
      _ = decodeSeven (selectedRawCongruentNineObservation l r J N
            (selectedRawCongruentClass l r (selectedNineTowerFiberRight l r M))) :=
        congrArg decodeSeven (selectedNineTowerFiber_nineObservedEq l r M)
      _ = _ := h _
  change selectedAncestorTowerCount l r 7 (selectedNineTowerFiberLeft l r M) =
    selectedAncestorTowerCount l r 7 (selectedNineTowerFiberRight l r M) at hc
  rw [selectedNineTowerFiber_seventhGap l r M] at hc
  omega

/-- A TENTH quotient coordinate C7, independently descended using
the existing tower theorem. Its injection on the full quotient is
NOT claimed. -/
def selectedRawCongruentTenObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      selectedRawNineObservationValue × Nat :=
  fun q => (selectedRawCongruentNineObservation l r J N q,
    selectedAncestorTowerOnNewQuotient l r 7 J N q)

/-- Ten observations distinguish this SPECIFIC typed witness pair,
not an unproved globally complete representation. -/
theorem selectedRawCongruentTen_seventhDistinguished
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentTenObservation l r J N
        (selectedRawCongruentClass l r (selectedNineTowerFiberLeft l r M)) ≠
      selectedRawCongruentTenObservation l r J N
        (selectedRawCongruentClass l r (selectedNineTowerFiberRight l r M)) := by
  intro h
  have hc := congrArg Prod.snd h
  change selectedAncestorTowerCount l r 7 (selectedNineTowerFiberLeft l r M) =
    selectedAncestorTowerCount l r 7 (selectedNineTowerFiberRight l r M) at hc
  rw [selectedNineTowerFiber_seventhGap l r M] at hc
  omega

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedNineTowerShiftLeft
#print axioms PentagonAdjoinedSixCell.selectedNineTowerShiftRight
#print axioms PentagonAdjoinedSixCell.selectedNineTowerShift_prefix
#print axioms PentagonAdjoinedSixCell.selectedAncestorShift_exactTwoGap
#print axioms PentagonAdjoinedSixCell.selectedNineTowerShift_seventhGap
#print axioms PentagonAdjoinedSixCell.selectedEightTowerShift_bothTopZero
#print axioms PentagonAdjoinedSixCell.selectedNineTowerShift_eightSignature
#print axioms PentagonAdjoinedSixCell.selectedNineTowerFiberLeft
#print axioms PentagonAdjoinedSixCell.selectedNineTowerFiberRight
#print axioms PentagonAdjoinedSixCell.selectedNineTowerFiber_eightSignature
#print axioms PentagonAdjoinedSixCell.selectedNineTowerFiber_sixthEq
#print axioms PentagonAdjoinedSixCell.selectedNineTowerFiber_seventhGap
#print axioms PentagonAdjoinedSixCell.selectedNineTowerFiber_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedNineTowerFiber_nineObservedEq
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentNine_notInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentNine_endomorphismNotInjective
#print axioms PentagonAdjoinedSixCell.selectedRawNineObservationValue
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentNine_noSeventhDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTenObservation
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTen_seventhDistinguished

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
