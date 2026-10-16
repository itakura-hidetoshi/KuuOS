import KUOS.DependentOriginationLowerRankFinitenessV3_45
import Mathlib.Data.Fintype.Sets
import Mathlib.Data.Set.Finite.Basic

namespace KUOS.DependentOriginationLocallyFiniteRankedEnumerationV3_46

open CategoryTheory
open Set
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationUnitorWitnessCorrelationV3_35
open KUOS.DependentOriginationAssociatorUnitorBoundaryReductionV3_36
open KUOS.DependentOriginationFreshAssociatorCompletionV3_37
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
open KUOS.DependentOriginationCountableAssociatorStabilizationV3_39
open KUOS.DependentOriginationCollisionSectorPreservationV3_40
open KUOS.DependentOriginationAssociatorIncidenceDecompositionV3_41
open KUOS.DependentOriginationFreshInteriorGlobalCoverageV3_42
open KUOS.DependentOriginationFiniteRankedScheduleV3_43
open KUOS.DependentOriginationCountableRankedEnumerationV3_44
open KUOS.DependentOriginationLowerRankFinitenessV3_45

universe u v uH vH

set_option autoImplicit false

/-!
# Construct a countable rank-monotone enumeration from local finiteness v3.46

v3.44 removes the v3.39 safety premise once an injective, rank-monotone
enumeration of the complete fresh/interior sector is given. This layer
constructs that enumeration from a sharper actual-incidence hypothesis.

Let S be the subtype of fresh/interior associator tasks. Assume:

* S is infinite;
* every natural-rank sublevel {a in S | rank a <= n} is finite;
* every distinct actual schedule dependency a ↝ b strictly lowers rank.

At each stage choose, among tasks not selected earlier, one of minimum rank.
The selected tasks are automatically distinct and their ranks are
nondecreasing.

The key coverage argument is finite-sublevel exhaustion. If some x : S were
never selected, minimality would force every selected task to have rank at most
rank x. The greedy sequence is injective, so this would embed ℕ into the finite
sublevel at rank x, a contradiction. Thus the greedy sequence enumerates all
of S.

This derives countability from local finiteness plus infinitude; countability is
not separately assumed.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The actual task type restricted to the locally solvable fresh/interior
sector from v3.41. -/
abbrev FreshInteriorTaskType :=
  {a : AssociatorTask W // FreshInteriorAssociatorTask W a}

/-- Actual local-finiteness/rank data sufficient to construct the v3.44
rank-monotone enumeration. -/
structure LocallyFiniteRankedFreshInteriorSector where
  rank : AssociatorTask W → ℕ
  infinite : Infinite (FreshInteriorTaskType W)
  sublevel_finite :
    ∀ n : ℕ,
      Set.Finite {x : FreshInteriorTaskType W | rank x.1 ≤ n}
  rank_decreases :
    ∀ {a b : AssociatorTask W},
      FreshInteriorAssociatorTask W a →
      FreshInteriorAssociatorTask W b →
      a ≠ b →
      AssociatorScheduleDependency W a b →
        rank b < rank a

/-- The finite natural-rank sublevel hypothesis used for the greedy
construction implies the strict-lower-rank finite-cover condition proved
necessary in v3.45. Thus v3.46 strengthens, rather than bypasses, the v3.45
scheduling obstruction. -/
theorem locallyFiniteRankedSector_hasFiniteLowerRankFreshInteriorCovers
    (P : LocallyFiniteRankedFreshInteriorSector W) :
    HasFiniteLowerRankFreshInteriorCovers W P.rank := by
  classical
  intro a ha
  let lowerSet : Set (FreshInteriorTaskType W) :=
    {x | P.rank x.1 ≤ P.rank a}
  have hFinite : lowerSet.Finite := by
    exact P.sublevel_finite (P.rank a)
  refine ⟨hFinite.toFinset.toList.map (fun x => x.1), ?_⟩
  intro b hb hlt
  have hbLower : (⟨b, hb⟩ : FreshInteriorTaskType W) ∈ lowerSet := by
    exact hlt.le
  have hbFin :
      (⟨b, hb⟩ : FreshInteriorTaskType W) ∈ hFinite.toFinset := by
    exact (Set.Finite.mem_toFinset hFinite).2 hbLower
  exact List.mem_map.mpr ⟨⟨b, hb⟩, by simpa using hbFin, rfl⟩

/-- An infinite fresh/interior sector always contains a task outside any
previously selected finite list. -/
theorem exists_freshInteriorTask_not_mem
    (P : LocallyFiniteRankedFreshInteriorSector W)
    (selected : List (FreshInteriorTaskType W)) :
    ∃ x : FreshInteriorTaskType W, x ∉ selected := by
  classical
  letI : Infinite (FreshInteriorTaskType W) := P.infinite
  by_contra h
  have hAll : ∀ x : FreshInteriorTaskType W, x ∈ selected := by
    intro x
    by_contra hx
    exact h ⟨x, hx⟩
  letI : Fintype {x : FreshInteriorTaskType W // x ∈ selected} :=
    List.Subtype.fintype selected
  have hFinite : Finite (FreshInteriorTaskType W) :=
    Finite.of_injective
      (fun x : FreshInteriorTaskType W =>
        (⟨x, hAll x⟩ : {y : FreshInteriorTaskType W // y ∈ selected}))
      (by
        intro x y hxy
        exact congrArg Subtype.val hxy)
  letI : Finite (FreshInteriorTaskType W) := hFinite
  exact not_finite (FreshInteriorTaskType W)

/-- Some natural rank is realized by a task outside the selected prefix. -/
theorem exists_remaining_freshInterior_rank
    (P : LocallyFiniteRankedFreshInteriorSector W)
    (selected : List (FreshInteriorTaskType W)) :
    ∃ n : ℕ, ∃ x : FreshInteriorTaskType W,
      x ∉ selected ∧ P.rank x.1 = n := by
  rcases exists_freshInteriorTask_not_mem W P selected with ⟨x, hx⟩
  exact ⟨P.rank x.1, x, hx, rfl⟩

/-- Least rank represented outside one finite selected prefix. -/
noncomputable def leastRemainingFreshInteriorRank
    (P : LocallyFiniteRankedFreshInteriorSector W)
    (selected : List (FreshInteriorTaskType W)) : ℕ := by
  classical
  exact Nat.find (exists_remaining_freshInterior_rank W P selected)

/-- Choose one task of the least rank not yet present in the selected prefix. -/
noncomputable def nextGreedyFreshInteriorTask
    (P : LocallyFiniteRankedFreshInteriorSector W)
    (selected : List (FreshInteriorTaskType W)) :
    FreshInteriorTaskType W := by
  classical
  exact Classical.choose
    (Nat.find_spec (exists_remaining_freshInterior_rank W P selected))

/-- The greedy choice is new and realizes the least remaining rank. -/
theorem nextGreedyFreshInteriorTask_spec
    (P : LocallyFiniteRankedFreshInteriorSector W)
    (selected : List (FreshInteriorTaskType W)) :
    nextGreedyFreshInteriorTask W P selected ∉ selected ∧
      P.rank (nextGreedyFreshInteriorTask W P selected).1 =
        leastRemainingFreshInteriorRank W P selected := by
  classical
  exact Classical.choose_spec
    (Nat.find_spec (exists_remaining_freshInterior_rank W P selected))

/-- The greedy choice has rank no larger than any other unselected task. -/
theorem nextGreedyFreshInteriorTask_rank_le
    (P : LocallyFiniteRankedFreshInteriorSector W)
    (selected : List (FreshInteriorTaskType W))
    (x : FreshInteriorTaskType W)
    (hx : x ∉ selected) :
    P.rank (nextGreedyFreshInteriorTask W P selected).1 ≤ P.rank x.1 := by
  classical
  rw [(nextGreedyFreshInteriorTask_spec W P selected).2]
  exact Nat.find_min'
    (exists_remaining_freshInterior_rank W P selected)
    ⟨x, hx, rfl⟩

/-- Prefix of the greedy enumeration after n choices. -/
noncomputable def greedyFreshInteriorPrefix
    (P : LocallyFiniteRankedFreshInteriorSector W) :
    ℕ → List (FreshInteriorTaskType W)
  | 0 => []
  | n + 1 =>
      greedyFreshInteriorPrefix P n ++
        [nextGreedyFreshInteriorTask W P (greedyFreshInteriorPrefix P n)]

/-- The nth greedy task is the minimum-rank task outside the first n choices. -/
noncomputable def greedyFreshInteriorTask
    (P : LocallyFiniteRankedFreshInteriorSector W)
    (n : ℕ) : FreshInteriorTaskType W :=
  nextGreedyFreshInteriorTask W P (greedyFreshInteriorPrefix W P n)

@[simp]
theorem greedyFreshInteriorPrefix_zero
    (P : LocallyFiniteRankedFreshInteriorSector W) :
    greedyFreshInteriorPrefix W P 0 = [] :=
  rfl

@[simp]
theorem greedyFreshInteriorPrefix_succ
    (P : LocallyFiniteRankedFreshInteriorSector W)
    (n : ℕ) :
    greedyFreshInteriorPrefix W P (n + 1) =
      greedyFreshInteriorPrefix W P n ++ [greedyFreshInteriorTask W P n] :=
  rfl

/-- The next greedy task has not appeared in its preceding prefix. -/
theorem greedyFreshInteriorTask_not_mem_prefix
    (P : LocallyFiniteRankedFreshInteriorSector W)
    (n : ℕ) :
    greedyFreshInteriorTask W P n ∉ greedyFreshInteriorPrefix W P n := by
  exact (nextGreedyFreshInteriorTask_spec
    W P (greedyFreshInteriorPrefix W P n)).1

/-- Exact membership normal form for a greedy prefix. -/
theorem mem_greedyFreshInteriorPrefix_iff
    (P : LocallyFiniteRankedFreshInteriorSector W)
    (x : FreshInteriorTaskType W) (n : ℕ) :
    x ∈ greedyFreshInteriorPrefix W P n ↔
      ∃ i : ℕ, i < n ∧ greedyFreshInteriorTask W P i = x := by
  induction n with
  | zero =>
      simp
  | succ n ih =>
      rw [greedyFreshInteriorPrefix_succ]
      constructor
      · intro hx
        rcases List.mem_append.mp hx with hx | hx
        · rcases ih.mp hx with ⟨i, hi, hix⟩
          exact ⟨i, hi.trans (Nat.lt_succ_self n), hix⟩
        · have hxEq : x = greedyFreshInteriorTask W P n := by
            simpa using hx
          exact ⟨n, Nat.lt_succ_self n, hxEq.symm⟩
      · rintro ⟨i, hi, hix⟩
        have hle : i ≤ n := Nat.lt_succ_iff.mp hi
        rcases lt_or_eq_of_le hle with hlt | hEq
        · exact List.mem_append.mpr
            (Or.inl (ih.mpr ⟨i, hlt, hix⟩))
        · subst i
          exact List.mem_append.mpr
            (Or.inr (by simpa using hix.symm))

/-- Greedy tasks at distinct natural stages are distinct. -/
theorem greedyFreshInteriorTask_injective
    (P : LocallyFiniteRankedFreshInteriorSector W) :
    Function.Injective (greedyFreshInteriorTask W P) := by
  intro i j hij
  rcases lt_trichotomy i j with hlt | heq | hgt
  · have hiMem :
        greedyFreshInteriorTask W P i ∈ greedyFreshInteriorPrefix W P j :=
      (mem_greedyFreshInteriorPrefix_iff W P
        (greedyFreshInteriorTask W P i) j).2 ⟨i, hlt, rfl⟩
    rw [hij] at hiMem
    exact False.elim
      ((greedyFreshInteriorTask_not_mem_prefix W P j) hiMem)
  · exact heq
  · have hjMem :
        greedyFreshInteriorTask W P j ∈ greedyFreshInteriorPrefix W P i :=
      (mem_greedyFreshInteriorPrefix_iff W P
        (greedyFreshInteriorTask W P j) i).2 ⟨j, hgt, rfl⟩
    rw [← hij] at hjMem
    exact False.elim
      ((greedyFreshInteriorTask_not_mem_prefix W P i) hjMem)

/-- The later greedy task was still available when the earlier task was
chosen. -/
theorem greedyFreshInteriorTask_not_mem_earlier_prefix
    (P : LocallyFiniteRankedFreshInteriorSector W)
    {i j : ℕ} (hij : i < j) :
    greedyFreshInteriorTask W P j ∉ greedyFreshInteriorPrefix W P i := by
  intro hMem
  rcases (mem_greedyFreshInteriorPrefix_iff W P
    (greedyFreshInteriorTask W P j) i).1 hMem with
      ⟨k, hki, hkj⟩
  have hkEqj : k = j :=
    greedyFreshInteriorTask_injective W P hkj
  subst k
  exact (Nat.not_lt_of_ge (Nat.le_of_lt hij)) hki

/-- Greedy ranks are nondecreasing. -/
theorem greedyFreshInteriorTask_rank_monotone
    (P : LocallyFiniteRankedFreshInteriorSector W)
    {i j : ℕ} (hij : i < j) :
    P.rank (greedyFreshInteriorTask W P i).1 ≤
      P.rank (greedyFreshInteriorTask W P j).1 := by
  exact nextGreedyFreshInteriorTask_rank_le W P
    (greedyFreshInteriorPrefix W P i)
    (greedyFreshInteriorTask W P j)
    (greedyFreshInteriorTask_not_mem_earlier_prefix W P hij)

/-- No fresh/interior task can be omitted forever: otherwise the injective
greedy sequence would lie entirely in one finite rank sublevel. -/
theorem greedyFreshInteriorTask_covers
    (P : LocallyFiniteRankedFreshInteriorSector W)
    (x : FreshInteriorTaskType W) :
    ∃ i : ℕ, greedyFreshInteriorTask W P i = x := by
  classical
  by_contra hCover
  have hNe : ∀ i : ℕ, greedyFreshInteriorTask W P i ≠ x := by
    intro i hi
    exact hCover ⟨i, hi⟩
  have hxNotPrefix :
      ∀ n : ℕ, x ∉ greedyFreshInteriorPrefix W P n := by
    intro n hx
    rcases (mem_greedyFreshInteriorPrefix_iff W P x n).1 hx with
      ⟨i, _hi, hix⟩
    exact hNe i hix
  have hRank :
      ∀ n : ℕ,
        P.rank (greedyFreshInteriorTask W P n).1 ≤ P.rank x.1 := by
    intro n
    exact nextGreedyFreshInteriorTask_rank_le W P
      (greedyFreshInteriorPrefix W P n) x (hxNotPrefix n)
  let sublevel : Set (FreshInteriorTaskType W) :=
    {y | P.rank y.1 ≤ P.rank x.1}
  letI : Finite sublevel :=
    Set.Finite.to_subtype (P.sublevel_finite (P.rank x.1))
  have hInjective :
      Function.Injective
        (fun n : ℕ =>
          (⟨greedyFreshInteriorTask W P n, hRank n⟩ : sublevel)) := by
    intro i j hij
    apply greedyFreshInteriorTask_injective W P
    exact congrArg (fun y : sublevel => (y.1 : FreshInteriorTaskType W)) hij
  have hFiniteNat : Finite ℕ :=
    Finite.of_injective
      (fun n : ℕ =>
        (⟨greedyFreshInteriorTask W P n, hRank n⟩ : sublevel))
      hInjective
  letI : Finite ℕ := hFiniteNat
  exact not_finite ℕ

/-- The greedy construction is a surjection onto the complete fresh/interior
subtype. -/
theorem greedyFreshInteriorTask_surjective
    (P : LocallyFiniteRankedFreshInteriorSector W) :
    Function.Surjective (greedyFreshInteriorTask W P) := by
  intro x
  exact greedyFreshInteriorTask_covers W P x

/-- Local finiteness plus infinitude therefore imply countability of the
fresh/interior sector. -/
theorem freshInteriorTaskType_countable
    (P : LocallyFiniteRankedFreshInteriorSector W) :
    Countable (FreshInteriorTaskType W) := by
  exact (greedyFreshInteriorTask_surjective W P).countable

/-- Assemble the v3.44 ranked enumeration from the greedy construction. -/
noncomputable def countableRankedEnumerationOfLocallyFiniteSector
    (P : LocallyFiniteRankedFreshInteriorSector W) :
    CountableRankedFreshInteriorEnumeration W where
  tasks := fun n => (greedyFreshInteriorTask W P n).1
  injective := by
    intro i j hij
    apply greedyFreshInteriorTask_injective W P
    exact Subtype.ext hij
  sound := fun n => (greedyFreshInteriorTask W P n).2
  covers := by
    intro a ha
    let x : FreshInteriorTaskType W := ⟨a, ha⟩
    rcases greedyFreshInteriorTask_covers W P x with ⟨i, hi⟩
    refine ⟨i, ?_⟩
    exact (congrArg Subtype.val hi).symm
  rank := P.rank
  rank_monotone := by
    intro i j hij
    exact greedyFreshInteriorTask_rank_monotone W P hij
  rank_decreases := P.rank_decreases

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- Actual local finiteness and rank decrease are sufficient for one common
gauge correcting all unitors and every nonresidual associator. Countability,
enumeration and forward noninterference are all derived. -/
theorem exists_commonGauge_for_all_nonresidual_of_locallyFiniteRankedSector
    (H : HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D)
    (P : LocallyFiniteRankedFreshInteriorSector W) :
    ∃ Q : GeneratedQuotientGaugeParameters W R D,
      (∀ X (s : UnitorRouteAt W X),
        Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s)) ∧
      ∀ a : AssociatorTask W,
        ¬ ResidualAssociatorIncidence W a →
          Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  exact exists_commonGauge_for_all_nonresidual_of_countableRankedEnumeration
    W R D H (countableRankedEnumerationOfLocallyFiniteSector W P)

/-!
## Boundary after v3.46

The external countable enumeration has now been removed. The remaining
scheduling hypotheses are actual incidence conditions:

* the fresh/interior sector is infinite;
* each natural-rank sublevel is finite;
* every distinct actual footprint dependency strictly lowers rank.

These hypotheses imply countability, a rank-monotone injective enumeration,
forward noninterference, and hence one common gauge for every nonresidual task.

The finite sector remains handled separately by v3.43. v3.46 does not derive
the rank or finite-sublevel property from weak admissibility, and it does not
eliminate the v3.41 residual collision/boundary sector.

No schedule independence, residual-sector vanishing, comparison-gauge
equations, general Stage I, Stage II, or final DO universality is asserted.
Protected validation-only #1558 is untouched.
-/

end KUOS.DependentOriginationLocallyFiniteRankedEnumerationV3_46
