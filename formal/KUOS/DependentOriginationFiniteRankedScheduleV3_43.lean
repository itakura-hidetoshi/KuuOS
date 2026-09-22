import KUOS.DependentOriginationFreshInteriorGlobalCoverageV3_42
import Mathlib.Data.List.Sort

namespace KUOS.DependentOriginationFiniteRankedScheduleV3_43

open CategoryTheory
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

universe u v uH vH

set_option autoImplicit false

/-!
# Finite rank construction of a safe fresh/interior schedule v3.43

v3.42 separates correction from scheduling: once the fresh/interior sector is
covered by a finite or countable forward-noninterfering schedule, one common
gauge corrects every nonresidual associator.

This layer constructs the finite coverage from a rank on the actual footprint
dependency relation.

For actual tasks a and b, write

  a ↝ b

when the leading coordinate selected for b occurs in the route footprint of a.
Then b cannot safely be processed after a. For distinct tasks, assume this
dependency strictly lowers a natural-number rank:

  a ↝ b  ->  rank b < rank a.

Start from one finite, duplicate-free list containing exactly the
fresh/interior sector, and sort it by nondecreasing rank. If an earlier task a
could see the leading key of a later task b, the rank hypothesis would give
rank b < rank a, contradicting the sorted order rank a <= rank b. Thus the
sorted list satisfies the v3.38 directional noninterference condition.

No abstract graph is introduced: the dependency is the existing
RouteFootprintContains predicate on actual QuotientGaugeCoordinate values.
The theorem does not prove that the fresh/interior sector is finite or that
such a rank exists.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Actual directional dependency relevant to the v3.38/v3.39 schedule:
b's selected leading coordinate occurs in a's already-corrected footprint. -/
def AssociatorScheduleDependency (a b : AssociatorTask W) : Prop :=
  RouteFootprintContains W (associatorTaskRoute W a)
    (associatorTaskLeadingCoordinate W b)

/-- Finite presentation of the entire fresh/interior sector together with a
rank strictly decreasing along every distinct actual schedule dependency. -/
structure FiniteRankedFreshInteriorPresentation where
  candidates : List (AssociatorTask W)
  nodup : candidates.Nodup
  sound : ∀ a : AssociatorTask W, a ∈ candidates →
    FreshInteriorAssociatorTask W a
  covers : ∀ a : AssociatorTask W, FreshInteriorAssociatorTask W a →
    a ∈ candidates
  rank : AssociatorTask W → ℕ
  rank_decreases :
    ∀ {a b : AssociatorTask W},
      a ∈ candidates → b ∈ candidates → a ≠ b →
        AssociatorScheduleDependency W a b →
          rank b < rank a

/-- Sort the finite fresh/interior presentation by nondecreasing dependency
rank. No equality decision on the dependent task structure is needed. -/
def rankedFreshInteriorSchedule
    (P : FiniteRankedFreshInteriorPresentation W) :
    List (AssociatorTask W) :=
  P.candidates.insertionSort (fun a b => P.rank a ≤ P.rank b)

/-- Rank sorting preserves exact task membership. -/
@[simp]
theorem mem_rankedFreshInteriorSchedule
    (P : FiniteRankedFreshInteriorPresentation W)
    (a : AssociatorTask W) :
    a ∈ rankedFreshInteriorSchedule W P ↔ a ∈ P.candidates := by
  simp [rankedFreshInteriorSchedule]

/-- Rank sorting preserves duplicate-freeness. -/
theorem rankedFreshInteriorSchedule_nodup
    (P : FiniteRankedFreshInteriorPresentation W) :
    (rankedFreshInteriorSchedule W P).Nodup := by
  have hPerm :
      rankedFreshInteriorSchedule W P ~ P.candidates := by
    exact List.perm_insertionSort
      (fun a b : AssociatorTask W => P.rank a ≤ P.rank b) P.candidates
  exact (hPerm.nodup_iff).2 P.nodup

/-- The constructed schedule is pairwise nondecreasing in dependency rank. -/
theorem rankedFreshInteriorSchedule_pairwise_rank
    (P : FiniteRankedFreshInteriorPresentation W) :
    (rankedFreshInteriorSchedule W P).Pairwise
      (fun a b => P.rank a ≤ P.rank b) := by
  classical
  let rel : AssociatorTask W → AssociatorTask W → Prop :=
    fun a b => P.rank a ≤ P.rank b
  letI : Std.Total rel :=
    ⟨fun a b => Nat.le_total (P.rank a) (P.rank b)⟩
  letI : IsTrans (AssociatorTask W) rel :=
    ⟨fun _ _ _ hab hbc => Nat.le_trans hab hbc⟩
  change (P.candidates.insertionSort rel).Pairwise rel
  exact List.pairwise_insertionSort rel P.candidates

/-- A nondecreasing rank list with no duplicates is forward-noninterfering
whenever every distinct actual dependency strictly lowers rank. -/
theorem forwardNoninterferingSchedule_of_pairwise_rank
    (tasks : List (AssociatorTask W))
    (rank : AssociatorTask W → ℕ)
    (hRank : tasks.Pairwise (fun a b => rank a ≤ rank b))
    (hNodup : tasks.Nodup)
    (hDecrease :
      ∀ {a b : AssociatorTask W},
        a ∈ tasks → b ∈ tasks → a ≠ b →
          AssociatorScheduleDependency W a b →
            rank b < rank a) :
    ForwardNoninterferingSchedule W tasks := by
  induction tasks with
  | nil =>
      exact List.Pairwise.nil
  | cons a tasks ih =>
      have hRankParts :
          (∀ b ∈ tasks, rank a ≤ rank b) ∧
            tasks.Pairwise (fun x y => rank x ≤ rank y) :=
        List.pairwise_cons.mp hRank
      have hNodupParts : a ∉ tasks ∧ tasks.Nodup :=
        List.nodup_cons.mp hNodup
      apply List.pairwise_cons.mpr
      constructor
      · intro b hb hDependency
        have hab : a ≠ b := by
          intro hEq
          subst b
          exact hNodupParts.1 hb
        have hlt : rank b < rank a :=
          hDecrease (by simp) (by simp [hb]) hab hDependency
        exact (Nat.not_lt_of_ge (hRankParts.1 b hb)) hlt
      · apply ih hRankParts.2 hNodupParts.2
        intro x y hx hy hxy hDependency
        exact hDecrease (by simp [hx]) (by simp [hy]) hxy hDependency

/-- The rank-sorted presentation satisfies exactly the directional schedule
condition consumed by v3.38. -/
theorem rankedFreshInteriorSchedule_safe
    (P : FiniteRankedFreshInteriorPresentation W) :
    ForwardNoninterferingSchedule W (rankedFreshInteriorSchedule W P) := by
  apply forwardNoninterferingSchedule_of_pairwise_rank W
    (rankedFreshInteriorSchedule W P) P.rank
    (rankedFreshInteriorSchedule_pairwise_rank W P)
    (rankedFreshInteriorSchedule_nodup W P)
  intro a b ha hb hab hDependency
  exact P.rank_decreases
    ((mem_rankedFreshInteriorSchedule W P a).1 ha)
    ((mem_rankedFreshInteriorSchedule W P b).1 hb)
    hab hDependency

/-- The sorted list is a genuine v3.42 finite coverage of the entire
fresh/interior sector. -/
def finiteFreshInteriorCoverageOfRankedPresentation
    (P : FiniteRankedFreshInteriorPresentation W) :
    FiniteFreshInteriorCoverage W where
  tasks := rankedFreshInteriorSchedule W P
  fresh := by
    intro a ha
    exact (P.sound a ((mem_rankedFreshInteriorSchedule W P a).1 ha)).1
  safe := rankedFreshInteriorSchedule_safe W P
  interior := by
    intro a ha
    exact (P.sound a ((mem_rankedFreshInteriorSchedule W P a).1 ha)).2
  covers := by
    intro a ha
    exact (mem_rankedFreshInteriorSchedule W P a).2 (P.covers a ha)

/-- Every member of the constructed finite schedule is exactly a
fresh/interior task from the original presentation. -/
theorem rankedFreshInteriorSchedule_sound
    (P : FiniteRankedFreshInteriorPresentation W)
    {a : AssociatorTask W}
    (ha : a ∈ rankedFreshInteriorSchedule W P) :
    FreshInteriorAssociatorTask W a :=
  P.sound a ((mem_rankedFreshInteriorSchedule W P a).1 ha)

/-- Every fresh/interior task occurs in the constructed rank-sorted schedule. -/
theorem rankedFreshInteriorSchedule_covers
    (P : FiniteRankedFreshInteriorPresentation W)
    (a : AssociatorTask W)
    (ha : FreshInteriorAssociatorTask W a) :
    a ∈ rankedFreshInteriorSchedule W P :=
  (mem_rankedFreshInteriorSchedule W P a).2 (P.covers a ha)

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- A finite ranked presentation of the actual fresh/interior incidence sector
therefore supplies one common gauge correcting every unitor and every
nonresidual associator. The ordering is constructed rather than assumed. -/
theorem exists_commonGauge_for_all_nonresidual_of_finiteRankedPresentation
    (H : HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D)
    (P : FiniteRankedFreshInteriorPresentation W) :
    ∃ Q : GeneratedQuotientGaugeParameters W R D,
      (∀ X (s : UnitorRouteAt W X),
        Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s)) ∧
      ∀ a : AssociatorTask W,
        ¬ ResidualAssociatorIncidence W a →
          Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  exact exists_commonGauge_for_all_nonresidual_of_finiteCoverage
    W R D H (finiteFreshInteriorCoverageOfRankedPresentation W P)

/-!
## Boundary after v3.43

This theorem removes an externally supplied finite ordering from the v3.42
hypotheses. It still assumes:

* a finite duplicate-free list covering the full fresh/interior sector; and
* a natural-number rank strictly decreasing along every distinct actual
  footprint dependency.

Thus finiteness and existence of the rank remain genuine incidence-geometry
questions. The result does not construct a finite presentation from weak
admissibility, prove that the dependency relation is well-founded, prove finite
rank for a countable sector, or eliminate the v3.41 residual collision/boundary
sector.

No schedule independence, residual-sector vanishing, comparison-gauge
equations, general Stage I, Stage II, or final DO universality is asserted.
Protected validation-only #1558 is untouched.
-/

end KUOS.DependentOriginationFiniteRankedScheduleV3_43
