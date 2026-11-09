import KUOS.Architecture.QiWuxingGK5CHP77NineObservationSeventhAncestorResidualV5_62

/-!
Qi v5.63 — a genuine Nat-indexed finite-prefix obstruction family,
not merely the conditional shift theorem from v5.59.

Starting from the actual typed N→N Qi v5.62 witness pair, recursively
move one raw reverse between the left and right suffixes at EACH step.
All constructed values remain in the original dependent 18D Type.
For every natural n, original nine measurements plus n further
ancestor-tower coordinates C7..C(6+n) agree on two quotient classes;
the next coordinate C(7+n) differs by exactly two. The original ordered
trace, reverse count, adjacency, top flag, and C1..C5 remain certified
by typed proofs, with the required actual top-flag equality proved.

Every supplied original M:J→N transports the pair to that same exact
fiber. For every n there is a REAL collision for the specified finite
observer (not just an abstract conditional statement); the specified
J→J fiber uses a genuine strict proof.

The result is NOT an assertion of completeness/incompleteness for
arbitrary unrelated observers, global all-WORLD gluing, or all
heterogeneous fiber inhabitance. Source 18D evidence, the original old19
and independent new seven-constructor comparison, root107, pins, and
protected validation PR #1558 remain unchanged.

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

/-- A NAT-indexed pair of original, dependent, genuinely typed 18D
proofs, not numerical surrogates or newly postulated inhabitants.
The seed n=0 is the certified third-shift C7 witness from v5.62. -/
def selectedFiniteTowerPair
    (N : SelectedContextualSeventeen W l r H K) :
    Nat →
      (SelectedContextualEighteen W l r N N ×
        SelectedContextualEighteen W l r N N)
  | 0 =>
      (selectedNineTowerShiftLeft l r N, selectedNineTowerShiftRight l r N)
  | n + 1 =>
      let p := selectedFiniteTowerPair l r N n
      (selectedAncestorShiftLeft l r N p.1 p.2,
        selectedAncestorShiftRight l r N p.1 p.2)

def selectedFiniteTowerLeft
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    SelectedContextualEighteen W l r N N :=
  (selectedFiniteTowerPair l r N n).1

def selectedFiniteTowerRight
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    SelectedContextualEighteen W l r N N :=
  (selectedFiniteTowerPair l r N n).2

/-- Every finite prefix C0..C(6+n) agrees on this specific genuinely
constructed N→N pair, for ALL n. This is the inductive upgrade to
the conditional v5.59 shift compatibility theorem. -/
theorem selectedFiniteTower_prefix
    (N : SelectedContextualSeventeen W l r H K) :
    ∀ n : Nat, ∀ k ≤ n + 6,
      selectedAncestorTowerCount l r k (selectedFiniteTowerLeft l r N n) =
        selectedAncestorTowerCount l r k (selectedFiniteTowerRight l r N n) := by
  intro n
  induction n with
  | zero =>
      intro k hk
      exact selectedNineTowerShift_prefix l r N k (by omega)
  | succ n ih =>
      intro k hk
      have hp : ∀ j < n + 7,
          selectedAncestorTowerCount l r j (selectedFiniteTowerLeft l r N n) =
            selectedAncestorTowerCount l r j (selectedFiniteTowerRight l r N n) := by
        intro j hj
        exact ih j (by omega)
      change
        selectedAncestorTowerCount l r k
          (selectedAncestorShiftLeft l r N
            (selectedFiniteTowerLeft l r N n)
            (selectedFiniteTowerRight l r N n)) =
          selectedAncestorTowerCount l r k
            (selectedAncestorShiftRight l r N
              (selectedFiniteTowerLeft l r N n)
              (selectedFiniteTowerRight l r N n))
      exact selectedAncestorShift_prefixCompatible l r (n + 7) N
        (selectedFiniteTowerLeft l r N n)
        (selectedFiniteTowerRight l r N n) hp k (by omega)

/-- The first unmatched tower coordinate is EXACTLY +2, at degree
7+n for every n, on the original dependent 18D evidence. -/
theorem selectedFiniteTower_nextGap
    (N : SelectedContextualSeventeen W l r H K) :
    ∀ n : Nat,
      selectedAncestorTowerCount l r (n + 7) (selectedFiniteTowerRight l r N n) =
        selectedAncestorTowerCount l r (n + 7) (selectedFiniteTowerLeft l r N n) + 2 := by
  intro n
  induction n with
  | zero =>
      exact selectedNineTowerShift_seventhGap l r N
  | succ n ih =>
      change
        selectedAncestorTowerCount l r ((n + 7) + 1)
            (selectedAncestorShiftRight l r N
              (selectedFiniteTowerLeft l r N n)
              (selectedFiniteTowerRight l r N n)) =
          selectedAncestorTowerCount l r ((n + 7) + 1)
              (selectedAncestorShiftLeft l r N
                (selectedFiniteTowerLeft l r N n)
                (selectedFiniteTowerRight l r N n)) + 2
      exact selectedAncestorShift_exactTwoGap l r (n + 7) N
        (selectedFiniteTowerLeft l r N n)
        (selectedFiniteTowerRight l r N n) ih

/-- Both members always have the actual outer constructor chain,
including the initial v5.62 pair. Top-reverse gate equality is not
silently assumed at any induction step. -/
theorem selectedFiniteTower_topZero
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    selectedContextEighteenTopReverseFlag l r (selectedFiniteTowerLeft l r N n) = 0 ∧
      selectedContextEighteenTopReverseFlag l r (selectedFiniteTowerRight l r N n) = 0 := by
  cases n with
  | zero => exact ⟨rfl, rfl⟩
  | succ n => exact ⟨rfl, rfl⟩

/-- A reusable typed local compatibility theorem: C0..C4 equality
before a shift plus actual top-flag equality implies equality of ALL
eight original quotient-invariant raw observations after the shift.
No cross-fiber or numerical surrogate identification. -/
theorem selectedAncestorShift_eightSignatureOfPrefix
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualEighteen W l r N N)
    (hPrefix : ∀ k ≤ 4,
      selectedAncestorTowerCount l r k A =
        selectedAncestorTowerCount l r k B)
    (hTop : selectedContextEighteenTopReverseFlag l r A =
      selectedContextEighteenTopReverseFlag l r B) :
    selectedRawEightSignature l r
      (selectedAncestorShiftLeft l r N A B)
      (selectedAncestorShiftRight l r N A B) := by
  let X : SelectedContextualEighteen W l r N N :=
    selectedAncestorShiftLeft l r N A B
  let Y : SelectedContextualEighteen W l r N N :=
    selectedAncestorShiftRight l r N A B
  have hShift : ∀ k ≤ 5,
      selectedAncestorTowerCount l r k X =
        selectedAncestorTowerCount l r k Y := by
    intro k hk
    exact selectedAncestorShift_prefixCompatible l r 5 N A B
      (by
        intro j hj
        exact hPrefix j (by omega)) k hk
  have hTrace : selectedContextEighteenTrace l r X =
      selectedContextEighteenTrace l r Y :=
    selectedAncestorShift_traceEq l r N A B
  have hAdjacent : selectedContextEighteenAdjacentReverseCount l r X =
      selectedContextEighteenAdjacentReverseCount l r Y :=
    selectedAncestorShift_adjacentIfTopEq l r N A B hTop
  have hTopNew : selectedContextEighteenTopReverseFlag l r X =
      selectedContextEighteenTopReverseFlag l r Y := by
    rcases selectedAncestorShift_bothTopZero l r N A B with ⟨hx, hy⟩
    exact hx.trans hy.symm
  have hReverse : selectedContextEighteenReverseCount l r X =
      selectedContextEighteenReverseCount l r Y :=
    (selectedAncestorTower_eqReverseCount l r X).symm.trans
      ((hShift 1 (by omega)).trans (selectedAncestorTower_eqReverseCount l r Y))
  have hPair : selectedContextEighteenReverseAncestryCount l r X =
      selectedContextEighteenReverseAncestryCount l r Y :=
    (selectedAncestorTower_eqAncestryCount l r X).symm.trans
      ((hShift 2 (by omega)).trans (selectedAncestorTower_eqAncestryCount l r Y))
  have hTriple : selectedContextEighteenReverseAncestorTripleCount l r X =
      selectedContextEighteenReverseAncestorTripleCount l r Y :=
    (selectedAncestorTower_eqAncestorTripleCount l r X).symm.trans
      ((hShift 3 (by omega)).trans (selectedAncestorTower_eqAncestorTripleCount l r Y))
  have hQuadruple : selectedContextEighteenReverseAncestorQuadrupleCount l r X =
      selectedContextEighteenReverseAncestorQuadrupleCount l r Y :=
    (selectedAncestorTower_eqAncestorQuadrupleCount l r X).symm.trans
      ((hShift 4 (by omega)).trans (selectedAncestorTower_eqAncestorQuadrupleCount l r Y))
  have hQuintuple : selectedContextEighteenReverseAncestorQuintupleCount l r X =
      selectedContextEighteenReverseAncestorQuintupleCount l r Y :=
    (selectedAncestorTower_eqAncestorQuintupleCount l r X).symm.trans
      ((hShift 5 (by omega)).trans (selectedAncestorTower_eqAncestorQuintupleCount l r Y))
  exact ⟨hTrace, hReverse, hAdjacent, hTopNew,
    hPair, hTriple, hQuadruple, hQuintuple⟩

/-- The original eight observations remain identical in the actual
Nat-indexed pair for every n, not just the seed case. -/
theorem selectedFiniteTower_eightSignature
    (N : SelectedContextualSeventeen W l r H K) :
    ∀ n : Nat,
      selectedRawEightSignature l r
        (selectedFiniteTowerLeft l r N n)
        (selectedFiniteTowerRight l r N n) := by
  intro n
  cases n with
  | zero =>
      exact selectedNineTowerShift_eightSignature l r N
  | succ n =>
      have hp : ∀ k ≤ 4,
          selectedAncestorTowerCount l r k (selectedFiniteTowerLeft l r N n) =
            selectedAncestorTowerCount l r k (selectedFiniteTowerRight l r N n) := by
        intro k hk
        exact selectedFiniteTower_prefix l r N n k (by omega)
      have ht : selectedContextEighteenTopReverseFlag l r
            (selectedFiniteTowerLeft l r N n) =
          selectedContextEighteenTopReverseFlag l r
            (selectedFiniteTowerRight l r N n) := by
        rcases selectedFiniteTower_topZero l r N n with ⟨hl, hr⟩
        exact hl.trans hr.symm
      change selectedRawEightSignature l r
        (selectedAncestorShiftLeft l r N
          (selectedFiniteTowerLeft l r N n)
          (selectedFiniteTowerRight l r N n))
        (selectedAncestorShiftRight l r N
          (selectedFiniteTowerLeft l r N n)
          (selectedFiniteTowerRight l r N n))
      exact selectedAncestorShift_eightSignatureOfPrefix l r N
        (selectedFiniteTowerLeft l r N n)
        (selectedFiniteTowerRight l r N n) hp ht

/-- Original M:J→N carries the entire Nat family into precisely the
same original dependent fiber, without constructing arbitrary M. -/
def selectedFiniteTowerFiberLeft (n : Nat)
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedFiniteTowerLeft l r N n)

def selectedFiniteTowerFiberRight (n : Nat)
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedFiniteTowerRight l r N n)

/-- Right concatenation preserves the whole finite C0..C(6+n)
prefix inside any truly supplied exact J→N fiber. -/
theorem selectedFiniteTowerFiber_prefix (n : Nat)
    (M : SelectedContextualEighteen W l r J N) :
    ∀ k ≤ n + 6,
      selectedAncestorTowerCount l r k (selectedFiniteTowerFiberLeft l r n M) =
        selectedAncestorTowerCount l r k (selectedFiniteTowerFiberRight l r n M) := by
  intro k hk
  cases k with
  | zero => rfl
  | succ j =>
      change selectedAncestorTowerCount l r (j + 1) M +
          selectedAncestorTowerCount l r (j + 1) (selectedFiniteTowerLeft l r N n) =
        selectedAncestorTowerCount l r (j + 1) M +
          selectedAncestorTowerCount l r (j + 1) (selectedFiniteTowerRight l r N n)
      exact congrArg
        (fun x : Nat => selectedAncestorTowerCount l r (j + 1) M + x)
        (selectedFiniteTower_prefix l r N n (j + 1) (by omega))

/-- The first unobserved coordinate continues to differ by +2 in
the SAME exact J→N fiber for all n and all actually supplied M. -/
theorem selectedFiniteTowerFiber_nextGap (n : Nat)
    (M : SelectedContextualEighteen W l r J N) :
    selectedAncestorTowerCount l r (n + 7) (selectedFiniteTowerFiberRight l r n M) =
      selectedAncestorTowerCount l r (n + 7) (selectedFiniteTowerFiberLeft l r n M) + 2 := by
  change selectedAncestorTowerCount l r (n + 7) M +
      selectedAncestorTowerCount l r (n + 7) (selectedFiniteTowerRight l r N n) =
    (selectedAncestorTowerCount l r (n + 7) M +
      selectedAncestorTowerCount l r (n + 7) (selectedFiniteTowerLeft l r N n)) + 2
  rw [selectedFiniteTower_nextGap l r N n]
  omega

/-- Original eight raw observations also agree after transport to
an actual heterogeneous fiber M:J→N, without assuming its existence. -/
theorem selectedFiniteTowerFiber_eightSignature (n : Nat)
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawEightSignature l r
      (selectedFiniteTowerFiberLeft l r n M)
      (selectedFiniteTowerFiberRight l r n M) :=
  selectedRawEightSignature_rightChain l r M
    (selectedFiniteTowerLeft l r N n)
    (selectedFiniteTowerRight l r N n)
    (selectedFiniteTower_eightSignature l r N n)

/-- All nine EXISTING independent new quotient measurements agree
on the genuine same-fiber pair, for every natural n. -/
theorem selectedFiniteTowerFiber_nineObservedEq (n : Nat)
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentNineObservation l r J N
        (selectedRawCongruentClass l r (selectedFiniteTowerFiberLeft l r n M)) =
      selectedRawCongruentNineObservation l r J N
        (selectedRawCongruentClass l r (selectedFiniteTowerFiberRight l r n M)) := by
  apply Prod.ext
  · exact selectedRawEightSignature_toObservation l r
      (selectedFiniteTowerFiberLeft l r n M)
      (selectedFiniteTowerFiberRight l r n M)
      (selectedFiniteTowerFiber_eightSignature l r n M)
  · change selectedAncestorTowerCount l r 6 (selectedFiniteTowerFiberLeft l r n M) =
      selectedAncestorTowerCount l r 6 (selectedFiniteTowerFiberRight l r n M)
    exact selectedFiniteTowerFiber_prefix l r n M 6 (by omega)

/-- True new seven-generator quotient classes are DISTINCT for
every n in every actually inhabited exact original 17D fiber. -/
theorem selectedFiniteTowerFiber_classDistinct (n : Nat)
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r (selectedFiniteTowerFiberLeft l r n M) ≠
      selectedRawCongruentClass l r (selectedFiniteTowerFiberRight l r n M) := by
  intro h
  have hc := congrArg
    (selectedAncestorTowerOnNewQuotient l r (n + 7) J N) h
  change selectedAncestorTowerCount l r (n + 7) (selectedFiniteTowerFiberLeft l r n M) =
    selectedAncestorTowerCount l r (n + 7) (selectedFiniteTowerFiberRight l r n M) at hc
  rw [selectedFiniteTowerFiber_nextGap l r n M] at hc
  omega

/-- The actual ninth observer extended by ANY finite number n of
additional successive quotient observables C7..C(6+n), not by
unverified or unrelated statistics. Fin n retains the finite index. -/
def selectedRawCongruentFiniteTowerObservation (n : Nat)
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      selectedRawNineObservationValue × (Fin n → Nat) :=
  fun q =>
    (selectedRawCongruentNineObservation l r J N q,
      fun i => selectedAncestorTowerOnNewQuotient l r (7 + i.val) J N q)

/-- For EACH finite n, the full actual (nine+n)-coordinate
observation equals on the two original same-fiber quotient classes. -/
theorem selectedFiniteTowerFiber_observedEq (n : Nat)
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentFiniteTowerObservation l r n J N
        (selectedRawCongruentClass l r (selectedFiniteTowerFiberLeft l r n M)) =
      selectedRawCongruentFiniteTowerObservation l r n J N
        (selectedRawCongruentClass l r (selectedFiniteTowerFiberRight l r n M)) := by
  apply Prod.ext
  · exact selectedFiniteTowerFiber_nineObservedEq l r n M
  · funext i
    change selectedAncestorTowerCount l r (7 + i.val)
        (selectedFiniteTowerFiberLeft l r n M) =
      selectedAncestorTowerCount l r (7 + i.val)
        (selectedFiniteTowerFiberRight l r n M)
    exact selectedFiniteTowerFiber_prefix l r n M (7 + i.val) (by
      have hi := i.isLt
      omega)

/-- An UNCONDITIONAL uniformly indexed family of actual collisions
FOR EACH explicitly supplied original fiber witness M. This does not
assert arbitrary heterogeneous J→N fibers are inhabited. -/
theorem selectedRawCongruentFiniteTower_notInjective (n : Nat)
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedRawCongruentFiniteTowerObservation l r n J N) := by
  intro hinj
  exact (selectedFiniteTowerFiber_classDistinct l r n M)
    (hinj (selectedFiniteTowerFiber_observedEq l r n M))

/-- All specified endomorphism fibers have an actual strict identity.
Thus for every n the finite observation is noninjective in J→J. -/
theorem selectedRawCongruentFiniteTower_endomorphismNotInjective (n : Nat)
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentFiniteTowerObservation l r n J J) :=
  selectedRawCongruentFiniteTower_notInjective l r n
    (SelectedContextualEighteen.strict J)

/-- No exact decoder of the next tower count C(7+n) from the
(nine+n) concrete observations on an actually supplied raw fiber. -/
theorem selectedRawCongruentFiniteTower_noNextDecoder (n : Nat)
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode :
        (selectedRawNineObservationValue × (Fin n → Nat)) → Nat,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentFiniteTowerObservation l r n J N q) =
          selectedAncestorTowerOnNewQuotient l r (n + 7) J N q := by
  rintro ⟨decode, h⟩
  have hc :
      selectedAncestorTowerOnNewQuotient l r (n + 7) J N
          (selectedRawCongruentClass l r (selectedFiniteTowerFiberLeft l r n M)) =
        selectedAncestorTowerOnNewQuotient l r (n + 7) J N
          (selectedRawCongruentClass l r (selectedFiniteTowerFiberRight l r n M)) := by
    calc
      _ = decode (selectedRawCongruentFiniteTowerObservation l r n J N
            (selectedRawCongruentClass l r (selectedFiniteTowerFiberLeft l r n M))) :=
        (h _).symm
      _ = decode (selectedRawCongruentFiniteTowerObservation l r n J N
            (selectedRawCongruentClass l r (selectedFiniteTowerFiberRight l r n M))) :=
        congrArg decode (selectedFiniteTowerFiber_observedEq l r n M)
      _ = _ := h _
  change selectedAncestorTowerCount l r (n + 7) (selectedFiniteTowerFiberLeft l r n M) =
    selectedAncestorTowerCount l r (n + 7) (selectedFiniteTowerFiberRight l r n M) at hc
  rw [selectedFiniteTowerFiber_nextGap l r n M] at hc
  omega

/-- In particular, no full class reconstruction from any of these
finite observations; the obstruction is a genuine pair of classes. -/
theorem selectedRawCongruentFiniteTower_noClassDecoder (n : Nat)
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode :
        (selectedRawNineObservationValue × (Fin n → Nat)) →
          Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentFiniteTowerObservation l r n J N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedRawCongruentFiniteTower_notInjective l r n M
  intro a b hab
  calc
    a = decode (selectedRawCongruentFiniteTowerObservation l r n J N a) := (h a).symm
    _ = decode (selectedRawCongruentFiniteTowerObservation l r n J N b) :=
      congrArg decode hab
    _ = b := h b

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedFiniteTowerPair
#print axioms PentagonAdjoinedSixCell.selectedFiniteTowerLeft
#print axioms PentagonAdjoinedSixCell.selectedFiniteTowerRight
#print axioms PentagonAdjoinedSixCell.selectedFiniteTower_prefix
#print axioms PentagonAdjoinedSixCell.selectedFiniteTower_nextGap
#print axioms PentagonAdjoinedSixCell.selectedFiniteTower_topZero
#print axioms PentagonAdjoinedSixCell.selectedAncestorShift_eightSignatureOfPrefix
#print axioms PentagonAdjoinedSixCell.selectedFiniteTower_eightSignature
#print axioms PentagonAdjoinedSixCell.selectedFiniteTowerFiberLeft
#print axioms PentagonAdjoinedSixCell.selectedFiniteTowerFiberRight
#print axioms PentagonAdjoinedSixCell.selectedFiniteTowerFiber_prefix
#print axioms PentagonAdjoinedSixCell.selectedFiniteTowerFiber_nextGap
#print axioms PentagonAdjoinedSixCell.selectedFiniteTowerFiber_eightSignature
#print axioms PentagonAdjoinedSixCell.selectedFiniteTowerFiber_nineObservedEq
#print axioms PentagonAdjoinedSixCell.selectedFiniteTowerFiber_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFiniteTowerObservation
#print axioms PentagonAdjoinedSixCell.selectedFiniteTowerFiber_observedEq
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFiniteTower_notInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFiniteTower_endomorphismNotInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFiniteTower_noNextDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFiniteTower_noClassDecoder

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
