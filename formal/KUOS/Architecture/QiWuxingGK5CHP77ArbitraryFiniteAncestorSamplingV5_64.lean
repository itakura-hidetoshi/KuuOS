import KUOS.Architecture.QiWuxingGK5CHP77UniformFiniteAncestorTowerObstructionV5_63

/-!
Qi v5.64 — arbitrary FINITE selections of the already certified
reverse-ancestor tower observables remain insufficient to identify
original 18D evidence modulo the actual seven-generator quotient.

Unlike v5.63's consecutive C7..C(6+n) observation, an input List Nat
specifies arbitrary degrees in arbitrary order, with duplicates
allowed. A constructive finite budget bounds each requested degree.
The original Nat-recursive typed 18D witness pair at that budget
matches the existing NINE quotient observations and ALL requested
tower degrees, while its next (unsampled) degree differs by exactly
two and separates the genuine quotient classes.

The mathematical scope is arbitrary finite subsets/multisets of THIS
ancestor-tower coordinate family, not arbitrary unrelated measurements,
all mathematical invariants, arbitrary heterogenous fiber inhabitants,
20D gluing, independent WORLD identification, or external authority.

Original dependent 18D Type constructors, old selected19 comparison,
new seven-generator raw congruence, import aggregate, root107, pins and
protected PR #1558 remain unchanged.
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

/-- An explicit finite bound, without assuming that observations are
consecutive or ordered. This is a computable selection budget, NOT a
bound on arbitrary unlisted invariants. -/
def selectedFiniteSampleBudget : List Nat → Nat
  | [] => 0
  | a :: as => a + selectedFiniteSampleBudget as

/-- Every requested degree really lies below the finite budget.
No use of an unproved existential or abstract choice of a maximum. -/
theorem selectedFiniteSampleBudget_mem_le :
    ∀ (indices : List Nat) (k : Nat),
      k ∈ indices → k ≤ selectedFiniteSampleBudget indices := by
  intro indices
  induction indices with
  | nil =>
      intro k hk
      cases hk
  | cons a as ih =>
      intro k hk
      change k ≤ a + selectedFiniteSampleBudget as
      rcases List.mem_cons.mp hk with heq | hmem
      · subst k
        omega
      · have hle : k ≤ selectedFiniteSampleBudget as := ih k hmem
        omega

/-- For any actually supplied raw M:J→N, use the original,
certified Nat-indexed 18D Type family at the finite sample budget. -/
def selectedFiniteSampleFiberLeft (indices : List Nat)
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  selectedFiniteTowerFiberLeft l r (selectedFiniteSampleBudget indices) M

def selectedFiniteSampleFiberRight (indices : List Nat)
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  selectedFiniteTowerFiberRight l r (selectedFiniteSampleBudget indices) M

/-- The actual tower counts agree at every requested degree, even if
the list is nonconsecutive, reordered, duplicated, or empty. -/
theorem selectedFiniteSampleFiber_selectedEq (indices : List Nat)
    (M : SelectedContextualEighteen W l r J N) :
    ∀ k ∈ indices,
      selectedAncestorTowerCount l r k (selectedFiniteSampleFiberLeft l r indices M) =
        selectedAncestorTowerCount l r k (selectedFiniteSampleFiberRight l r indices M) := by
  intro k hk
  exact selectedFiniteTowerFiber_prefix l r
    (selectedFiniteSampleBudget indices) M k (by
      have hle := selectedFiniteSampleBudget_mem_le indices k hk
      omega)

/-- The genuine quotient classes are still distinct, because the
first unobserved tower coordinate at budget+7 differs by exactly +2. -/
theorem selectedFiniteSampleFiber_nextGap (indices : List Nat)
    (M : SelectedContextualEighteen W l r J N) :
    selectedAncestorTowerCount l r (selectedFiniteSampleBudget indices + 7)
        (selectedFiniteSampleFiberRight l r indices M) =
      selectedAncestorTowerCount l r (selectedFiniteSampleBudget indices + 7)
        (selectedFiniteSampleFiberLeft l r indices M) + 2 :=
  selectedFiniteTowerFiber_nextGap l r
    (selectedFiniteSampleBudget indices) M

theorem selectedFiniteSampleFiber_classDistinct (indices : List Nat)
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r (selectedFiniteSampleFiberLeft l r indices M) ≠
      selectedRawCongruentClass l r (selectedFiniteSampleFiberRight l r indices M) :=
  selectedFiniteTowerFiber_classDistinct l r
    (selectedFiniteSampleBudget indices) M

/-- Exactly the existing NINE independently justified quotient
observations, plus a LIST of tower counts sampled at the explicitly
specified natural degrees. The quotient lifts are those already
certified for every degree in v5.59. -/
def selectedRawCongruentFiniteSampleObservation (indices : List Nat)
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      selectedRawNineObservationValue × List Nat :=
  fun q =>
    (selectedRawCongruentNineObservation l r J N q,
      indices.map (fun k => selectedAncestorTowerOnNewQuotient l r k J N q))

/-- Pointwise equality on the ACTUAL raw typed values implies
equality of their requested list of degrees. No quotient shortcut. -/
theorem selectedFiniteSampleMapEq
    {X Y : SelectedContextualEighteen W l r J N}
    (indices : List Nat) :
    (∀ k ∈ indices,
      selectedAncestorTowerCount l r k X =
        selectedAncestorTowerCount l r k Y) →
      indices.map (fun k => selectedAncestorTowerCount l r k X) =
        indices.map (fun k => selectedAncestorTowerCount l r k Y) := by
  induction indices with
  | nil =>
      intro _
      rfl
  | cons k ks ih =>
      intro h
      simp only [List.map_cons]
      apply congrArg₂ List.cons
      · exact h k (by simp)
      · apply ih
        intro j hj
        exact h j (by simp [hj])

/-- The finite sampling observation is exactly equal on two genuinely
different raw quotient classes in the same supplied original fiber. -/
theorem selectedFiniteSampleFiber_observedEq (indices : List Nat)
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentFiniteSampleObservation l r indices J N
        (selectedRawCongruentClass l r (selectedFiniteSampleFiberLeft l r indices M)) =
      selectedRawCongruentFiniteSampleObservation l r indices J N
        (selectedRawCongruentClass l r (selectedFiniteSampleFiberRight l r indices M)) := by
  apply Prod.ext
  · exact selectedFiniteTowerFiber_nineObservedEq l r
      (selectedFiniteSampleBudget indices) M
  · change indices.map
        (fun k => selectedAncestorTowerCount l r k
          (selectedFiniteSampleFiberLeft l r indices M)) =
      indices.map
        (fun k => selectedAncestorTowerCount l r k
          (selectedFiniteSampleFiberRight l r indices M))
    exact selectedFiniteSampleMapEq l r indices
      (selectedFiniteSampleFiber_selectedEq l r indices M)

/-- For EVERY arbitrary finite degree list, the genuine nine+sample
observer is not injective whenever an actual M:J→N is supplied. -/
theorem selectedRawCongruentFiniteSample_notInjective (indices : List Nat)
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedRawCongruentFiniteSampleObservation l r indices J N) := by
  intro hinj
  exact (selectedFiniteSampleFiber_classDistinct l r indices M)
    (hinj (selectedFiniteSampleFiber_observedEq l r indices M))

/-- The explicit raw strict constructor supplies all J→J fibers;
no arbitrary heterogeneous fiber is postulated inhabited. -/
theorem selectedRawCongruentFiniteSample_endomorphismNotInjective (indices : List Nat)
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentFiniteSampleObservation l r indices J J) :=
  selectedRawCongruentFiniteSample_notInjective l r indices
    (SelectedContextualEighteen.strict J)

/-- No next-count decoder from these nine plus arbitrary sampled
tower values, even when the exact original fiber is supplied. -/
theorem selectedRawCongruentFiniteSample_noNextDecoder (indices : List Nat)
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode : (selectedRawNineObservationValue × List Nat) → Nat,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentFiniteSampleObservation l r indices J N q) =
          selectedAncestorTowerOnNewQuotient l r
            (selectedFiniteSampleBudget indices + 7) J N q := by
  rintro ⟨decode, h⟩
  have hc :
      selectedAncestorTowerOnNewQuotient l r
          (selectedFiniteSampleBudget indices + 7) J N
          (selectedRawCongruentClass l r (selectedFiniteSampleFiberLeft l r indices M)) =
        selectedAncestorTowerOnNewQuotient l r
          (selectedFiniteSampleBudget indices + 7) J N
          (selectedRawCongruentClass l r (selectedFiniteSampleFiberRight l r indices M)) := by
    calc
      _ = decode (selectedRawCongruentFiniteSampleObservation l r indices J N
            (selectedRawCongruentClass l r (selectedFiniteSampleFiberLeft l r indices M))) :=
        (h _).symm
      _ = decode (selectedRawCongruentFiniteSampleObservation l r indices J N
            (selectedRawCongruentClass l r (selectedFiniteSampleFiberRight l r indices M))) :=
        congrArg decode (selectedFiniteSampleFiber_observedEq l r indices M)
      _ = _ := h _
  change selectedAncestorTowerCount l r
      (selectedFiniteSampleBudget indices + 7)
        (selectedFiniteSampleFiberLeft l r indices M) =
    selectedAncestorTowerCount l r
      (selectedFiniteSampleBudget indices + 7)
        (selectedFiniteSampleFiberRight l r indices M) at hc
  rw [selectedFiniteSampleFiber_nextGap l r indices M] at hc
  omega

/-- A complete class decoder would force injectivity, contradicted by
the constructed genuine same-fiber 18D witness pair. -/
theorem selectedRawCongruentFiniteSample_noClassDecoder (indices : List Nat)
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode :
        (selectedRawNineObservationValue × List Nat) →
          Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentFiniteSampleObservation l r indices J N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedRawCongruentFiniteSample_notInjective l r indices M
  intro a b hab
  calc
    a = decode (selectedRawCongruentFiniteSampleObservation l r indices J N a) :=
      (h a).symm
    _ = decode (selectedRawCongruentFiniteSampleObservation l r indices J N b) :=
      congrArg decode hab
    _ = b := h b

/-- Universal quantification over finite sample lists is genuine:
the list itself is arbitrary, though every observation coordinate
is from the previously certified ancestor tower. -/
theorem selectedRawCongruentEveryFiniteSample_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ∀ indices : List Nat,
      ¬ Function.Injective
        (selectedRawCongruentFiniteSampleObservation l r indices J N) := by
  intro indices
  exact selectedRawCongruentFiniteSample_notInjective l r indices M

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedFiniteSampleBudget
#print axioms PentagonAdjoinedSixCell.selectedFiniteSampleBudget_mem_le
#print axioms PentagonAdjoinedSixCell.selectedFiniteSampleFiberLeft
#print axioms PentagonAdjoinedSixCell.selectedFiniteSampleFiberRight
#print axioms PentagonAdjoinedSixCell.selectedFiniteSampleFiber_selectedEq
#print axioms PentagonAdjoinedSixCell.selectedFiniteSampleFiber_nextGap
#print axioms PentagonAdjoinedSixCell.selectedFiniteSampleFiber_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFiniteSampleObservation
#print axioms PentagonAdjoinedSixCell.selectedFiniteSampleMapEq
#print axioms PentagonAdjoinedSixCell.selectedFiniteSampleFiber_observedEq
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFiniteSample_notInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFiniteSample_endomorphismNotInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFiniteSample_noNextDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFiniteSample_noClassDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentEveryFiniteSample_notInjective

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
