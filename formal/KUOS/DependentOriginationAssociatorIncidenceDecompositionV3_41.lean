import KUOS.DependentOriginationCollisionSectorPreservationV3_40

namespace KUOS.DependentOriginationAssociatorIncidenceDecompositionV3_41

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

universe u v uH vH

set_option autoImplicit false

noncomputable section

/-!
# Actual associator incidence decomposition v3.41

v3.40 shows that the middle-identity collision sector is corrected
semantically by one common unitor gauge, while v3.37-v3.39 handle a prescribed
fresh, unitor-interior, forward-noninterfering schedule.

This layer separates the remaining local incidence question from the global
scheduling question.

For one actual associator task, its v3.37 leading key can collide only through
one of the three suffix keys appearing in the same four-coordinate footprint.
We prove that failure of v3.37 freshness is exactly the disjunction of those
literal dependent-key equalities.

We then partition actual tasks into:

* the unitor-generated middle-identity collision sector;
* the fresh/interior local candidate sector;
* a residual local incidence sector.

The residual sector has an exact normal form: away from middle identity it is
either a genuine leading-key collision or a fresh leading key that lies on the
unitor-visible boundary.

Finally, for one v3.39 schedule, v3.40 is repackaged as a coverage theorem:
the same gauge corrects every middle-identity task and every task occurring in
that schedule. This does not assert that every fresh/interior task occurs in
the schedule, nor that every associator belongs to one of the two corrected
subsets.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Package one genuine middle-identity associator as an actual task. -/
def middleIdentityAssociatorTask
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    AssociatorTask W where
  X := X
  Y := Y
  Z := Y
  T := Z
  f := f
  g := 𝟙 Y
  h := g

/-- The entire middle-identity collision sector, stated by equality of actual
dependent task data rather than by a tag attached from outside. -/
def IsMiddleIdentityAssociatorTask (a : AssociatorTask W) : Prop :=
  ∃ (X Y Z : W.Localization) (f : X ⟶ Y) (g : Y ⟶ Z),
    a = middleIdentityAssociatorTask W f g

/-- First suffix key in the actual four-coordinate associator footprint. -/
def associatorTaskFirstSuffixCoordinate (a : AssociatorTask W) :
    QuotientGaugeCoordinate W :=
  .composition a.f a.g

/-- Second suffix key in the actual four-coordinate associator footprint. -/
def associatorTaskSecondSuffixCoordinate (a : AssociatorTask W) :
    QuotientGaugeCoordinate W :=
  .composition a.g a.h

/-- Trailing suffix key in the actual four-coordinate associator footprint. -/
def associatorTaskTrailingCoordinate (a : AssociatorTask W) :
    QuotientGaugeCoordinate W :=
  .composition a.f (a.g ≫ a.h)

/-- Literal collision of the v3.37 leading key with one of the other three
coordinates inspected by that same actual associator route. -/
def HasAssociatorLeadingCoordinateCollision (a : AssociatorTask W) : Prop :=
  associatorTaskFirstSuffixCoordinate W a =
      associatorTaskLeadingCoordinate W a ∨
  associatorTaskSecondSuffixCoordinate W a =
      associatorTaskLeadingCoordinate W a ∨
  associatorTaskTrailingCoordinate W a =
      associatorTaskLeadingCoordinate W a

/-- v3.37 freshness is exactly absence of all three actual leading-key
collisions. This is a dependent-coordinate statement, not an abstract graph
condition. -/
theorem not_fresh_iff_hasAssociatorLeadingCoordinateCollision
    (a : AssociatorTask W) :
    ¬ FreshAssociatorLeadingCoordinate W a.f a.g a.h ↔
      HasAssociatorLeadingCoordinateCollision W a := by
  change ¬ (
      associatorTaskFirstSuffixCoordinate W a ≠
          associatorTaskLeadingCoordinate W a ∧
      associatorTaskSecondSuffixCoordinate W a ≠
          associatorTaskLeadingCoordinate W a ∧
      associatorTaskTrailingCoordinate W a ≠
          associatorTaskLeadingCoordinate W a) ↔
    HasAssociatorLeadingCoordinateCollision W a
  constructor
  · intro h
    by_cases h₁ :
        associatorTaskFirstSuffixCoordinate W a =
          associatorTaskLeadingCoordinate W a
    · exact Or.inl h₁
    by_cases h₂ :
        associatorTaskSecondSuffixCoordinate W a =
          associatorTaskLeadingCoordinate W a
    · exact Or.inr (Or.inl h₂)
    by_cases h₃ :
        associatorTaskTrailingCoordinate W a =
          associatorTaskLeadingCoordinate W a
    · exact Or.inr (Or.inr h₃)
    exact False.elim (h ⟨h₁, h₂, h₃⟩)
  · intro hCollision hFresh
    rcases hCollision with h₁ | h₂ | h₃
    · exact hFresh.1 h₁
    · exact hFresh.2.1 h₂
    · exact hFresh.2.2 h₃

/-- Middle identity realizes the trailing/leading collision concretely. -/
theorem middleIdentityAssociatorTask_trailing_eq_leading
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    associatorTaskTrailingCoordinate W (middleIdentityAssociatorTask W f g) =
      associatorTaskLeadingCoordinate W (middleIdentityAssociatorTask W f g) := by
  simp [associatorTaskTrailingCoordinate, associatorTaskLeadingCoordinate,
    middleIdentityAssociatorTask]

/-- The packaged middle-identity task lies in the collision predicate. -/
theorem middleIdentityAssociatorTask_hasCollision
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    HasAssociatorLeadingCoordinateCollision W
      (middleIdentityAssociatorTask W f g) := by
  exact Or.inr (Or.inr
    (middleIdentityAssociatorTask_trailing_eq_leading W f g))

/-- Every task in the middle-identity sector fails the v3.37 freshness premise. -/
theorem middleIdentityAssociatorTask_not_fresh
    (a : AssociatorTask W) (hMiddle : IsMiddleIdentityAssociatorTask W a) :
    ¬ FreshAssociatorLeadingCoordinate W a.f a.g a.h := by
  rcases hMiddle with ⟨X, Y, Z, f, g, rfl⟩
  exact (not_fresh_iff_hasAssociatorLeadingCoordinateCollision
    W (middleIdentityAssociatorTask W f g)).2
      (middleIdentityAssociatorTask_hasCollision W f g)

/-- Local v3.39 candidate: the v3.37 leading update is fresh and lies outside
the complete unitor-visible boundary. Global forward noninterference is
deliberately not folded into this one-task predicate. -/
def FreshInteriorAssociatorTask (a : AssociatorTask W) : Prop :=
  FreshAssociatorLeadingCoordinate W a.f a.g a.h ∧
    ¬ UnitorVisibleCoordinate W (associatorTaskLeadingCoordinate W a)

/-- The local incidence not handled by either middle-identity semantic
reduction or the v3.37 fresh/interior update interface. -/
def ResidualAssociatorIncidence (a : AssociatorTask W) : Prop :=
  ¬ IsMiddleIdentityAssociatorTask W a ∧
    ¬ FreshInteriorAssociatorTask W a

/-- Every actual associator task lies in exactly the intended three-way
case split at the level of local incidence. This theorem does not choose a
global schedule for the fresh/interior case. -/
theorem associatorTask_incidence_trichotomy (a : AssociatorTask W) :
    IsMiddleIdentityAssociatorTask W a ∨
      FreshInteriorAssociatorTask W a ∨
        ResidualAssociatorIncidence W a := by
  classical
  by_cases hMiddle : IsMiddleIdentityAssociatorTask W a
  · exact Or.inl hMiddle
  by_cases hFreshInterior : FreshInteriorAssociatorTask W a
  · exact Or.inr (Or.inl hFreshInterior)
  · exact Or.inr (Or.inr ⟨hMiddle, hFreshInterior⟩)

/-- Middle identity and the fresh/interior sector are disjoint for the actual
v3.37 coordinate definitions. -/
theorem middleIdentityAssociatorTask_not_freshInterior
    (a : AssociatorTask W) (hMiddle : IsMiddleIdentityAssociatorTask W a) :
    ¬ FreshInteriorAssociatorTask W a := by
  intro hFreshInterior
  exact middleIdentityAssociatorTask_not_fresh W a hMiddle hFreshInterior.1

/-- Exact local normal form for the residual sector. Away from middle identity,
the remaining obstruction is either an actual leading-key collision or a
fresh leading key that still lies on the unitor-visible boundary. -/
theorem residualAssociatorIncidence_iff_collision_or_boundary
    (a : AssociatorTask W) :
    ResidualAssociatorIncidence W a ↔
      ¬ IsMiddleIdentityAssociatorTask W a ∧
        (HasAssociatorLeadingCoordinateCollision W a ∨
          (FreshAssociatorLeadingCoordinate W a.f a.g a.h ∧
            UnitorVisibleCoordinate W
              (associatorTaskLeadingCoordinate W a))) := by
  classical
  constructor
  · rintro ⟨hNotMiddle, hNotFreshInterior⟩
    refine ⟨hNotMiddle, ?_⟩
    by_cases hFresh : FreshAssociatorLeadingCoordinate W a.f a.g a.h
    · refine Or.inr ⟨hFresh, ?_⟩
      by_contra hNotVisible
      exact hNotFreshInterior ⟨hFresh, hNotVisible⟩
    · exact Or.inl
        ((not_fresh_iff_hasAssociatorLeadingCoordinateCollision W a).1 hFresh)
  · rintro ⟨hNotMiddle, hCase⟩
    refine ⟨hNotMiddle, ?_⟩
    intro hFreshInterior
    rcases hCase with hCollision | ⟨_hFresh, hVisible⟩
    · exact ((not_fresh_iff_hasAssociatorLeadingCoordinateCollision W a).2
        hCollision) hFreshInterior.1
    · exact hFreshInterior.2 hVisible

/-- Relative to one prescribed v3.39 schedule, this is the part of the actual
associator task space already covered either by v3.40 or by an explicit
scheduled v3.37 completion. -/
def AssociatorTaskCoveredByMiddleOrSchedule
    (tasks : ℕ → AssociatorTask W) (a : AssociatorTask W) : Prop :=
  IsMiddleIdentityAssociatorTask W a ∨ ∃ i : ℕ, a = tasks i

/-- Every scheduled task is locally fresh/interior under exactly the local
premises already required by v3.39. -/
theorem scheduledTask_freshInterior
    (tasks : ℕ → AssociatorTask W)
    (hFresh : ∀ i : ℕ,
      FreshAssociatorLeadingCoordinate W (tasks i).f (tasks i).g (tasks i).h)
    (hInterior : ∀ i : ℕ, ¬ UnitorVisibleCoordinate W
      (associatorTaskLeadingCoordinate W (tasks i)))
    (i : ℕ) :
    FreshInteriorAssociatorTask W (tasks i) :=
  ⟨hFresh i, hInterior i⟩

/-- Every task covered by the middle-identity sector or the selected schedule
is outside the residual local incidence sector. The converse is intentionally
not claimed: a fresh/interior task need not occur in this particular schedule. -/
theorem coveredTask_not_residual
    (tasks : ℕ → AssociatorTask W)
    (hFresh : ∀ i : ℕ,
      FreshAssociatorLeadingCoordinate W (tasks i).f (tasks i).g (tasks i).h)
    (hInterior : ∀ i : ℕ, ¬ UnitorVisibleCoordinate W
      (associatorTaskLeadingCoordinate W (tasks i)))
    (a : AssociatorTask W)
    (hCovered : AssociatorTaskCoveredByMiddleOrSchedule W tasks a) :
    ¬ ResidualAssociatorIncidence W a := by
  intro hResidual
  rcases hCovered with hMiddle | ⟨i, rfl⟩
  · exact hResidual.1 hMiddle
  · exact hResidual.2 (scheduledTask_freshInterior W tasks hFresh hInterior i)

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- One gauge corrects the entire currently covered incidence sector:
all unitors, every middle-identity collision task, and every task appearing in
one prescribed v3.39 schedule. This is the constructive union of the v3.40 and
v3.39 sectors, not a claim that the schedule covers all fresh/interior tasks. -/
theorem exists_commonGauge_for_middleOrScheduledTasks_of_pairwiseShared
    (H : HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D)
    (tasks : ℕ → AssociatorTask W)
    (hFresh : ∀ i : ℕ,
      FreshAssociatorLeadingCoordinate W (tasks i).f (tasks i).g (tasks i).h)
    (hSafe : CountableForwardNoninterference W tasks)
    (hInterior : ∀ i : ℕ, ¬ UnitorVisibleCoordinate W
      (associatorTaskLeadingCoordinate W (tasks i))) :
    ∃ Q : GeneratedQuotientGaugeParameters W R D,
      (∀ X (s : UnitorRouteAt W X),
        Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s)) ∧
      ∀ a : AssociatorTask W,
        AssociatorTaskCoveredByMiddleOrSchedule W tasks a →
          Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  rcases exists_commonGauge_for_middleIdentity_and_countableSchedule_of_pairwiseShared
    W R D H tasks hFresh hSafe hInterior with
      ⟨Q, hUnit, hMiddle, hTasks⟩
  refine ⟨Q, hUnit, ?_⟩
  intro a hCovered
  rcases hCovered with hIsMiddle | ⟨i, rfl⟩
  · rcases hIsMiddle with ⟨X, Y, Z, f, g, rfl⟩
    simpa [associatorTaskRoute, middleIdentityAssociatorTask] using
      hMiddle X Y Z f g
  · exact hTasks i

/-!
## Boundary after v3.41

The local incidence partition is exhaustive, but the proved common-gauge
coverage is intentionally smaller than "all nonresidual tasks": v3.39 still
needs one actual countable ordering satisfying forward noninterference.
A fresh/interior task that is not listed in the selected schedule is not
thereby corrected by the final theorem.

The residual normal form is exact only for the present local mechanism:
non-middle-identity leading collisions and fresh but unitor-visible leading
keys. It does not assert that these cases are impossible, inconsistent, or
uncorrectable by another construction.

No countability of all associators, existence of a global schedule, finite-rank
dependency theorem, schedule/seed/W/R/D independence, comparison-gauge
equations, general Stage I, Stage II, or final DO universality is asserted.
Protected validation-only #1558 is untouched.
-/

end KUOS.DependentOriginationAssociatorIncidenceDecompositionV3_41
