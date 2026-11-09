import KUOS.Architecture.QiWuxingGK5CHP77ArbitraryFiniteAncestorSamplingV5_64

/-!
Qi v5.65 — genuine independent adjacency obstruction to the ENTIRE
natural-indexed ancestor tower, even when the FULL ordered raw trace
and the true top-reverse flag are observed.

The source terms are actual raw18D N→N proofs:
  S = strict N, R = reverse S,
  A = chain (reverse (chain R S)) S,
  B = chain (reverse R) S.
Both have the same trace, top reverse flag, and EVERY C_n for all
n : Nat, not merely any finite sample. Nonetheless their *directly
adjacent* raw reverse counts are 0 and 1. This invariant is already
certified to descend through each of the seven new comparison
constructors, therefore their true new quotient classes differ.

For any genuinely supplied M:J→N, chain M A and chain M B retain the
same full tower/trace/top collision and +1 adjacency gap in that EXACT
original dependent fiber. This separates independently preserved
syntactic adjacency from the all-degree reverse-ancestor count tower.
It does not imply nonfaithfulness of the existing NINE observation
(which explicitly includes adjacency), or classify the whole quotient.

No old proof terms, dependent endpoints, comparison constructors,
imports, root107, pins, validation-only #1558, or authority change.
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

/-- Genuine one-reversal N→N raw proof. -/
def selectedFullTowerAdjacencySpine
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (.strict N)

/-- A raw chain separates two reversals. It has the same positive-degree
ancestor tower counts as a single reverse, with C0 fixed at 1. -/
def selectedFullTowerAdjacencyBranch
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain (selectedFullTowerAdjacencySpine l r N) (.strict N)

/-- Left is externally a chain; the two reverse nodes are separated
by a raw chain, and are NOT immediately adjacent. -/
def selectedFullTowerAdjacencyLeft
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain (.reverse (selectedFullTowerAdjacencyBranch l r N)) (.strict N)

/-- Right is externally a chain with directly nested raw reversals.
Its ancestor tower matches the left term at ALL natural degrees. -/
def selectedFullTowerAdjacencyRight
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain (.reverse (selectedFullTowerAdjacencySpine l r N)) (.strict N)

/-- Right-composing a strict N→N identity is invisible to ALL
ancestor-tower counts, including the special degree-zero seed. -/
theorem selectedFullTowerAdjacency_branchTowerEq
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    selectedAncestorTowerCount l r n
        (selectedFullTowerAdjacencyBranch l r N) =
      selectedAncestorTowerCount l r n
        (selectedFullTowerAdjacencySpine l r N) := by
  cases n with
  | zero => rfl
  | succ n =>
      change selectedAncestorTowerCount l r (n + 1)
          (selectedFullTowerAdjacencySpine l r N) + 0 =
        selectedAncestorTowerCount l r (n + 1)
          (selectedFullTowerAdjacencySpine l r N)
      exact Nat.add_zero _

/-- Raw reverse respects equality of EVERY tower count for
genuine same-endpoint Type-valued evidence. -/
theorem selectedFullTowerAdjacency_reverseTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualEighteen W l r N N)
    (h : ∀ n : Nat, selectedAncestorTowerCount l r n A =
      selectedAncestorTowerCount l r n B)
    (n : Nat) :
    selectedAncestorTowerCount l r n (.reverse A) =
      selectedAncestorTowerCount l r n (.reverse B) := by
  cases n with
  | zero => rfl
  | succ n =>
      change
        selectedAncestorTowerCount l r (n + 1) A +
          selectedAncestorTowerCount l r n A =
        selectedAncestorTowerCount l r (n + 1) B +
          selectedAncestorTowerCount l r n B
      rw [h (n + 1), h n]

/-- Raw chain with a common true strict identity also preserves
pointwise tower equality for ALL natural degrees. -/
theorem selectedFullTowerAdjacency_chainStrictTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualEighteen W l r N N)
    (h : ∀ n : Nat, selectedAncestorTowerCount l r n A =
      selectedAncestorTowerCount l r n B)
    (n : Nat) :
    selectedAncestorTowerCount l r n (.chain A (.strict N)) =
      selectedAncestorTowerCount l r n (.chain B (.strict N)) := by
  cases n with
  | zero => rfl
  | succ n =>
      change
        selectedAncestorTowerCount l r (n + 1) A + 0 =
        selectedAncestorTowerCount l r (n + 1) B + 0
      rw [h (n + 1)]

/-- Core INFINITE tower coincidence, with a proof for every natural
degree and not an inference from finite sample results. -/
theorem selectedFullTowerAdjacency_allTowerEq
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    selectedAncestorTowerCount l r n
        (selectedFullTowerAdjacencyLeft l r N) =
      selectedAncestorTowerCount l r n
        (selectedFullTowerAdjacencyRight l r N) :=
  selectedFullTowerAdjacency_chainStrictTowerEq l r N
    (.reverse (selectedFullTowerAdjacencyBranch l r N))
    (.reverse (selectedFullTowerAdjacencySpine l r N))
    (selectedFullTowerAdjacency_reverseTowerEq l r N
      (selectedFullTowerAdjacencyBranch l r N)
      (selectedFullTowerAdjacencySpine l r N)
      (selectedFullTowerAdjacency_branchTowerEq l r N)) n

/-- Both genuinely typed raw loops have the SAME full ordered
external context trace (empty, not only the same length). -/
theorem selectedFullTowerAdjacency_traceEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenTrace l r
        (selectedFullTowerAdjacencyLeft l r N) =
      selectedContextEighteenTrace l r
        (selectedFullTowerAdjacencyRight l r N) := by
  rfl

/-- The top raw constructor on BOTH loops is a chain. -/
theorem selectedFullTowerAdjacency_topZero
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenTopReverseFlag l r
        (selectedFullTowerAdjacencyLeft l r N) = 0 ∧
      selectedContextEighteenTopReverseFlag l r
        (selectedFullTowerAdjacencyRight l r N) = 0 := by
  exact ⟨rfl, rfl⟩

/-- Directly adjacent reverse nodes are ABSENT on the left. -/
theorem selectedFullTowerAdjacency_leftAdjacentZero
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenAdjacentReverseCount l r
      (selectedFullTowerAdjacencyLeft l r N) = 0 := by
  rfl

/-- Directly adjacent reverse nodes occur EXACTLY ONCE on the right. -/
theorem selectedFullTowerAdjacency_rightAdjacentOne
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenAdjacentReverseCount l r
      (selectedFullTowerAdjacencyRight l r N) = 1 := by
  rfl

/-- The independently preserved quotient invariant differs by +1
despite complete natural-indexed ancestor-tower equality. -/
theorem selectedFullTowerAdjacency_adjGap
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenAdjacentReverseCount l r
        (selectedFullTowerAdjacencyRight l r N) =
      selectedContextEighteenAdjacentReverseCount l r
        (selectedFullTowerAdjacencyLeft l r N) + 1 := by
  rw [selectedFullTowerAdjacency_rightAdjacentOne l r N,
    selectedFullTowerAdjacency_leftAdjacentZero l r N]

/-- Distinct ORIGINAL new seven-generator quotient classes.
No comparison is invented between fibers or surrogates. -/
theorem selectedFullTowerAdjacency_classDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentClass l r
        (selectedFullTowerAdjacencyLeft l r N) ≠
      selectedRawCongruentClass l r
        (selectedFullTowerAdjacencyRight l r N) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentAdjacentReverseOnQuotient l r N N) h
  change selectedContextEighteenAdjacentReverseCount l r
      (selectedFullTowerAdjacencyLeft l r N) =
    selectedContextEighteenAdjacentReverseCount l r
      (selectedFullTowerAdjacencyRight l r N) at hc
  rw [selectedFullTowerAdjacency_adjGap l r N] at hc
  omega

/-- No Type-valued new 19D comparison exists between the genuine
same-endpoint raw loops, even with complete tower coincidence. -/
theorem selectedFullTowerAdjacency_noComparison
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedFullTowerAdjacencyLeft l r N)
      (selectedFullTowerAdjacencyRight l r N)) := by
  rintro ⟨A⟩
  exact (selectedFullTowerAdjacency_classDistinct l r N)
    (Quotient.sound ⟨A⟩)

/-- Transport to the SAME original J→N fiber requires an actual M,
not an unjustified nonempty-fiber assumption. -/
def selectedFullTowerAdjacencyFiberLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedFullTowerAdjacencyLeft l r N)

def selectedFullTowerAdjacencyFiberRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedFullTowerAdjacencyRight l r N)

/-- ALL tower counts still agree after real right concatenation. -/
theorem selectedFullTowerAdjacencyFiber_allTowerEq
    (M : SelectedContextualEighteen W l r J N) (n : Nat) :
    selectedAncestorTowerCount l r n
        (selectedFullTowerAdjacencyFiberLeft l r M) =
      selectedAncestorTowerCount l r n
        (selectedFullTowerAdjacencyFiberRight l r M) := by
  cases n with
  | zero => rfl
  | succ n =>
      change
        selectedAncestorTowerCount l r (n + 1) M +
          selectedAncestorTowerCount l r (n + 1)
            (selectedFullTowerAdjacencyLeft l r N) =
        selectedAncestorTowerCount l r (n + 1) M +
          selectedAncestorTowerCount l r (n + 1)
            (selectedFullTowerAdjacencyRight l r N)
      exact congrArg
        (fun x : Nat => selectedAncestorTowerCount l r (n + 1) M + x)
        (selectedFullTowerAdjacency_allTowerEq l r N (n + 1))

/-- Both external traces agree exactly after attaching the
original raw M:J→N. -/
theorem selectedFullTowerAdjacencyFiber_traceEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenTrace l r
        (selectedFullTowerAdjacencyFiberLeft l r M) =
      selectedContextEighteenTrace l r
        (selectedFullTowerAdjacencyFiberRight l r M) := by
  change
    selectedContextEighteenTrace l r M ++
      selectedContextEighteenTrace l r (selectedFullTowerAdjacencyLeft l r N) =
    selectedContextEighteenTrace l r M ++
      selectedContextEighteenTrace l r (selectedFullTowerAdjacencyRight l r N)
  exact congrArg (fun t : List Bool => selectedContextEighteenTrace l r M ++ t)
    (selectedFullTowerAdjacency_traceEq l r N)

/-- Both transported raw proofs are top-level chains. -/
theorem selectedFullTowerAdjacencyFiber_topEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenTopReverseFlag l r
        (selectedFullTowerAdjacencyFiberLeft l r M) =
      selectedContextEighteenTopReverseFlag l r
        (selectedFullTowerAdjacencyFiberRight l r M) := by
  rfl

/-- The independent adjacent-reversal count retains an exact +1
residual in EVERY supplied original J→N fiber. -/
theorem selectedFullTowerAdjacencyFiber_adjGap
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenAdjacentReverseCount l r
        (selectedFullTowerAdjacencyFiberRight l r M) =
      selectedContextEighteenAdjacentReverseCount l r
        (selectedFullTowerAdjacencyFiberLeft l r M) + 1 := by
  change selectedContextEighteenAdjacentReverseCount l r M +
      selectedContextEighteenAdjacentReverseCount l r
        (selectedFullTowerAdjacencyRight l r N) =
    (selectedContextEighteenAdjacentReverseCount l r M +
      selectedContextEighteenAdjacentReverseCount l r
        (selectedFullTowerAdjacencyLeft l r N)) + 1
  rw [selectedFullTowerAdjacency_adjGap l r N]
  omega

/-- The two genuinely transported quotient classes remain distinct. -/
theorem selectedFullTowerAdjacencyFiber_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r
        (selectedFullTowerAdjacencyFiberLeft l r M) ≠
      selectedRawCongruentClass l r
        (selectedFullTowerAdjacencyFiberRight l r M) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentAdjacentReverseOnQuotient l r J N) h
  change selectedContextEighteenAdjacentReverseCount l r
      (selectedFullTowerAdjacencyFiberLeft l r M) =
    selectedContextEighteenAdjacentReverseCount l r
      (selectedFullTowerAdjacencyFiberRight l r M) at hc
  rw [selectedFullTowerAdjacencyFiber_adjGap l r M] at hc
  omega

/-- The COMPLETE infinite tower q ↦ (n ↦ C_n(q)) on the existing
genuine new quotient. The function space is not truncated to finite n. -/
def selectedRawCongruentFullTowerObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → (Nat → Nat) :=
  fun q n => selectedAncestorTowerOnNewQuotient l r n J N q

/-- Even adding the independently certified FULL ordered raw trace
and top-reverse flag does not make the entire ancestor tower injective.
AdjacentReverse is deliberately NOT one of these observed coordinates.
This is not a claim that the existing nine-observer is noninjective
because of this pair. -/
def selectedRawCongruentTraceTopFullTowerObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      (List Bool × Nat) × (Nat → Nat) :=
  fun q =>
    ((selectedRawCongruentTraceOnQuotient l r J N q,
      selectedRawCongruentTopReverseOnQuotient l r J N q),
      selectedRawCongruentFullTowerObservation l r J N q)

/-- Every coordinate of the actual full tower, and BOTH independent
trace/top observations, agrees on the genuine transported pair. -/
theorem selectedFullTowerAdjacencyFiber_observedEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentTraceTopFullTowerObservation l r J N
        (selectedRawCongruentClass l r (selectedFullTowerAdjacencyFiberLeft l r M)) =
      selectedRawCongruentTraceTopFullTowerObservation l r J N
        (selectedRawCongruentClass l r (selectedFullTowerAdjacencyFiberRight l r M)) := by
  apply Prod.ext
  · apply Prod.ext
    · exact selectedFullTowerAdjacencyFiber_traceEq l r M
    · exact selectedFullTowerAdjacencyFiber_topEq l r M
  · funext n
    change selectedAncestorTowerCount l r n
        (selectedFullTowerAdjacencyFiberLeft l r M) =
      selectedAncestorTowerCount l r n
        (selectedFullTowerAdjacencyFiberRight l r M)
    exact selectedFullTowerAdjacencyFiber_allTowerEq l r M n

/-- The full tower + trace + top observation is provably NONINJECTIVE
on every exact fiber with an actually supplied original raw witness. -/
theorem selectedRawCongruentTraceTopFullTower_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedRawCongruentTraceTopFullTowerObservation l r J N) := by
  intro hinj
  exact (selectedFullTowerAdjacencyFiber_classDistinct l r M)
    (hinj (selectedFullTowerAdjacencyFiber_observedEq l r M))

/-- Strong separation: no function of the entire infinite ancestor
tower, full ordered trace and top reverse flag can recover the already
quotient-invariant adjacent reverse count on all classes of a supplied
original fiber. -/
theorem selectedRawCongruentTraceTopFullTower_noAdjacentDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode : ((List Bool × Nat) × (Nat → Nat)) → Nat,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentTraceTopFullTowerObservation l r J N q) =
          selectedRawCongruentAdjacentReverseOnQuotient l r J N q := by
  rintro ⟨decode, h⟩
  have hc :
      selectedRawCongruentAdjacentReverseOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedFullTowerAdjacencyFiberLeft l r M)) =
        selectedRawCongruentAdjacentReverseOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedFullTowerAdjacencyFiberRight l r M)) := by
    calc
      _ = decode (selectedRawCongruentTraceTopFullTowerObservation l r J N
            (selectedRawCongruentClass l r (selectedFullTowerAdjacencyFiberLeft l r M))) :=
        (h _).symm
      _ = decode (selectedRawCongruentTraceTopFullTowerObservation l r J N
            (selectedRawCongruentClass l r (selectedFullTowerAdjacencyFiberRight l r M))) :=
        congrArg decode (selectedFullTowerAdjacencyFiber_observedEq l r M)
      _ = _ := h _
  change selectedContextEighteenAdjacentReverseCount l r
      (selectedFullTowerAdjacencyFiberLeft l r M) =
    selectedContextEighteenAdjacentReverseCount l r
      (selectedFullTowerAdjacencyFiberRight l r M) at hc
  rw [selectedFullTowerAdjacencyFiber_adjGap l r M] at hc
  omega

/-- No complete class decoder exists for this named observation,
even with access to ALL tower degrees as an infinite function. -/
theorem selectedRawCongruentTraceTopFullTower_noClassDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode :
        ((List Bool × Nat) × (Nat → Nat)) →
          Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentTraceTopFullTowerObservation l r J N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedRawCongruentTraceTopFullTower_notInjective l r M
  intro a b hab
  calc
    a = decode (selectedRawCongruentTraceTopFullTowerObservation l r J N a) :=
      (h a).symm
    _ = decode (selectedRawCongruentTraceTopFullTowerObservation l r J N b) :=
      congrArg decode hab
    _ = b := h b

/-- Each specified endomorphism fiber has the actual strict N→N
identity, yielding the full-tower noninjectivity without a separate
inhabitance hypothesis. -/
theorem selectedRawCongruentTraceTopFullTower_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentTraceTopFullTowerObservation l r J J) :=
  selectedRawCongruentTraceTopFullTower_notInjective l r
    (SelectedContextualEighteen.strict J)

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacencySpine
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacencyBranch
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacencyLeft
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacencyRight
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacency_branchTowerEq
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacency_reverseTowerEq
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacency_chainStrictTowerEq
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacency_allTowerEq
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacency_traceEq
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacency_topZero
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacency_leftAdjacentZero
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacency_rightAdjacentOne
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacency_adjGap
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacency_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacency_noComparison
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacencyFiberLeft
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacencyFiberRight
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacencyFiber_allTowerEq
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacencyFiber_traceEq
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacencyFiber_topEq
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacencyFiber_adjGap
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacencyFiber_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullTowerObservation
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTraceTopFullTowerObservation
#print axioms PentagonAdjoinedSixCell.selectedFullTowerAdjacencyFiber_observedEq
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTraceTopFullTower_notInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTraceTopFullTower_noAdjacentDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTraceTopFullTower_noClassDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentTraceTopFullTower_endomorphismNotInjective

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
