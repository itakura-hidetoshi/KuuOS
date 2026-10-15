import KUOS.DependentOriginationFiniteRankedScheduleV3_43

namespace KUOS.DependentOriginationCountableRankedEnumerationV3_44

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
open KUOS.DependentOriginationFiniteRankedScheduleV3_43

universe u v uH vH

set_option autoImplicit false

/-!
# Countable rank-monotone enumeration gives a safe schedule v3.44

v3.43 constructs a finite safe schedule by sorting a finite presentation by an
actual dependency rank. For a countably infinite sector, sorting by rank is a
separate enumeration problem: finite lower-rank fibres are needed if every task
is to occur at a finite natural-number stage.

This layer therefore isolates the exact intermediate object needed by v3.39:
an injective enumeration of the complete fresh/interior sector whose ranks are
nondecreasing. If every distinct actual footprint dependency strictly lowers
rank, the enumeration is automatically forward-noninterfering.

Thus the external v3.39 safety hypothesis is removed once such a ranked
enumeration is supplied. Constructing the enumeration from local finiteness is
left to the next theorem unit.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- One injective natural-number enumeration of the entire fresh/interior
sector, already arranged in nondecreasing dependency rank. -/
structure CountableRankedFreshInteriorEnumeration where
  tasks : ℕ → AssociatorTask W
  injective : Function.Injective tasks
  sound : ∀ i : ℕ, FreshInteriorAssociatorTask W (tasks i)
  covers : ∀ a : AssociatorTask W,
    FreshInteriorAssociatorTask W a → ∃ i : ℕ, a = tasks i
  rank : AssociatorTask W → ℕ
  rank_monotone :
    ∀ {i j : ℕ}, i < j → rank (tasks i) ≤ rank (tasks j)
  rank_decreases :
    ∀ {a b : AssociatorTask W},
      FreshInteriorAssociatorTask W a →
      FreshInteriorAssociatorTask W b →
      a ≠ b →
      AssociatorScheduleDependency W a b →
        rank b < rank a

/-- Distinct enumeration indices contain distinct actual tasks. -/
theorem rankedEnumeration_tasks_ne
    (E : CountableRankedFreshInteriorEnumeration W)
    {i j : ℕ} (hij : i < j) :
    E.tasks i ≠ E.tasks j := by
  intro hEq
  exact (Nat.ne_of_lt hij) (E.injective hEq)

/-- Rank monotonicity contradicts every forbidden forward dependency. -/
theorem countableForwardNoninterference_of_rankMonotone
    (E : CountableRankedFreshInteriorEnumeration W) :
    CountableForwardNoninterference W E.tasks := by
  intro i j hij hDependency
  have hNe : E.tasks i ≠ E.tasks j :=
    rankedEnumeration_tasks_ne W E hij
  have hDecrease : E.rank (E.tasks j) < E.rank (E.tasks i) :=
    E.rank_decreases (E.sound i) (E.sound j) hNe hDependency
  exact (Nat.not_lt_of_ge (E.rank_monotone hij)) hDecrease

/-- The ranked enumeration is exactly a v3.42 countable coverage object. -/
def countableFreshInteriorCoverageOfRankedEnumeration
    (E : CountableRankedFreshInteriorEnumeration W) :
    CountableFreshInteriorCoverage W where
  tasks := E.tasks
  fresh := fun i => (E.sound i).1
  safe := countableForwardNoninterference_of_rankMonotone W E
  interior := fun i => (E.sound i).2
  covers := E.covers

/-- The v3.39 leading-coordinate map of the constructed coverage is injective.
This is a derived incidence fact, not a separate enumeration hypothesis. -/
theorem rankedEnumeration_leadingCoordinate_injective
    (E : CountableRankedFreshInteriorEnumeration W) :
    Function.Injective
      (fun i => associatorTaskLeadingCoordinate W (E.tasks i)) := by
  exact countable_leadingCoordinate_injective W E.tasks
    (countableForwardNoninterference_of_rankMonotone W E)

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- A countable rank-monotone enumeration of the entire fresh/interior sector
therefore gives one gauge correcting all unitors and every nonresidual
associator. The v3.39 safety premise is derived from the rank. -/
theorem exists_commonGauge_for_all_nonresidual_of_countableRankedEnumeration
    (H : HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D)
    (E : CountableRankedFreshInteriorEnumeration W) :
    ∃ Q : GeneratedQuotientGaugeParameters W R D,
      (∀ X (s : UnitorRouteAt W X),
        Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s)) ∧
      ∀ a : AssociatorTask W,
        ¬ ResidualAssociatorIncidence W a →
          Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  exact exists_commonGauge_for_all_nonresidual_of_countableCoverage
    W R D H (countableFreshInteriorCoverageOfRankedEnumeration W E)

/-!
## Boundary after v3.44

The remaining countable scheduling problem is now sharper. One no longer needs
to prove forward noninterference separately once an injective rank-monotone
enumeration exists. What remains is to construct such an enumeration from
actual incidence hypotheses.

A natural candidate is finite lower-rank sublevel sets (or finite rank fibres)
plus countability of the fresh/interior sector. Without such local finiteness,
infinitely many rank-zero tasks can prevent any rank-one task from appearing at
a finite stage of a nondecreasing natural-number enumeration.

No theorem here derives countability, local finiteness, rank existence, or a
rank-monotone enumeration from weak admissibility. The v3.41 residual sector is
unchanged. No schedule independence, comparison-gauge equations, general
Stage I, Stage II, or final DO universality is asserted.

Protected validation-only #1558 is untouched.
-/

end KUOS.DependentOriginationCountableRankedEnumerationV3_44
