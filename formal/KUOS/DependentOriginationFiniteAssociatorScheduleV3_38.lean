import KUOS.DependentOriginationFreshAssociatorCompletionV3_37
import Mathlib.Data.List.Pairwise

namespace KUOS.DependentOriginationFiniteAssociatorScheduleV3_38

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateFootprintV3_12
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationPairwiseFiniteExtensionV3_15
open KUOS.DependentOriginationUnitorWitnessCorrelationV3_35
open KUOS.DependentOriginationAssociatorUnitorBoundaryReductionV3_36
open KUOS.DependentOriginationFreshAssociatorCompletionV3_37

universe u v uH vH

set_option autoImplicit false

/-!
# Finite forward-noninterfering associator completion v3.38

The v3.37 constructor solves one fresh leading coordinate. This file composes
those actual updates along a finite ordered list. Later leading coordinates
must avoid the footprints of earlier tasks. Earlier updates may affect later
tasks: each later correction is computed from the then-current gauge.
Thus neither disjoint footprints nor commutation of arbitrary updates is used.

First realize a compatible unitor family as one quotient gauge, using the
v3.36 boundary value and identity values outside that boundary. The v3.35
nested-witness theorem supplies such a family without an assumed global
associator witness. Then a fresh, interior, forward-noninterfering schedule
produces one gauge correcting all unitors and every listed associator.

No claim is made that an arbitrary list can be ordered in this way, or that
finite scheduled completion yields a simultaneous solution of all routes.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- An actual composable triple, with its dependent endpoints stored together. -/
structure AssociatorTask where
  X : W.Localization
  Y : W.Localization
  Z : W.Localization
  T : W.Localization
  f : X ⟶ Y
  g : Y ⟶ Z
  h : Z ⟶ T

/-- The actual route to be corrected by a task. -/
def associatorTaskRoute (a : AssociatorTask W) : ThreeQuotientRouteState W :=
  .associator a.f a.g a.h

/-- The single coordinate changed by the v3.37 constructor. -/
noncomputable def associatorTaskLeadingCoordinate (a : AssociatorTask W) : QuotientGaugeCoordinate W :=
  .composition (a.f ≫ a.g) a.h

/-- A later leading update may not change an already processed footprint.
This is a directional list condition, not symmetric disjointness. -/
def ForwardNoninterferingSchedule (tasks : List (AssociatorTask W)) : Prop :=
  tasks.Pairwise (fun a b =>
    ¬ RouteFootprintContains W (associatorTaskRoute W a)
      (associatorTaskLeadingCoordinate W b))

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-! ## Realize the already correlated unitor family as one gauge -/

/-- Extend a unitor family only to use the v3.36 boundary interface.
The arbitrary associator entries assert no associator correction. -/
noncomputable def extendUnitorFamily
    (U : (X : W.Localization) →
      UnitorRouteAt W X → GeneratedQuotientGaugeParameters W R D) :
    ThreeQuotientRouteState W → GeneratedQuotientGaugeParameters W R D
  | .associator (X := X) _ _ _ => U X (.left (𝟙 X))
  | .leftUnitor (X := X) f => U X (.left f)
  | .rightUnitor (Y := Y) f => U Y (.right f)

/-- The auxiliary extension preserves every actual unitor entry. -/
theorem extendUnitorFamily_unitor
    (U : (X : W.Localization) →
      UnitorRouteAt W X → GeneratedQuotientGaugeParameters W R D)
    {X : W.Localization} (s : UnitorRouteAt W X) :
    extendUnitorFamily W R D U (unitorRouteState W s) = U X s := by
  cases s <;> rfl

/-- Fill the unitor boundary with its common value and use identity gauges
elsewhere. No full-family associator overlap is assumed by this definition. -/
noncomputable def unitorSeedGauge
    (Qlocal : ThreeQuotientRouteState W → GeneratedQuotientGaugeParameters W R D) :
    GeneratedQuotientGaugeParameters W R D := by
  classical
  exact
    { mapIdGauge := fun X =>
        unitorBoundaryValue W R D Qlocal (.identity X)
          (identity_unitorVisibleCoordinate W X)
      mapCompGauge := fun f g =>
        if hc : UnitorVisibleCoordinate W (.composition f g) then
          unitorBoundaryValue W R D Qlocal (.composition f g) hc
        else Iso.refl _ }

/-- The seed has exactly the prescribed boundary value at every visible key. -/
theorem unitorSeedGauge_value
    (Qlocal : ThreeQuotientRouteState W → GeneratedQuotientGaugeParameters W R D)
    (c : QuotientGaugeCoordinate W) (hc : UnitorVisibleCoordinate W c) :
    quotientGaugeCoordinateValue W R D (unitorSeedGauge W R D Qlocal) c =
      unitorBoundaryValue W R D Qlocal c hc := by
  classical
  cases c with
  | identity X => rfl
  | composition f g =>
      change (if hVisible : UnitorVisibleCoordinate W (.composition f g) then
        unitorBoundaryValue W R D Qlocal (.composition f g) hVisible
        else Iso.refl _) = unitorBoundaryValue W R D Qlocal (.composition f g) hc
      rw [dif_pos hc]

/-- Compatibility of the unitor restriction makes the seed extend each
unitor's entire footprint, not only its identity coordinate. -/
theorem unitorSeedGauge_agrees
    (Qlocal : ThreeQuotientRouteState W → GeneratedQuotientGaugeParameters W R D)
    (hUnit : UnitorRestrictionPairwise W R D Qlocal)
    {X : W.Localization} (s : UnitorRouteAt W X) :
    QuotientGaugesAgreeOnRouteState W R D
      (unitorSeedGauge W R D Qlocal) (Qlocal (unitorRouteState W s))
      (unitorRouteState W s) := by
  apply quotientGaugesAgreeOnRouteState_of_coordinateValue_eq W R D
  intro c hc
  have hVisible : UnitorVisibleCoordinate W c := unitorVisibleCoordinate_of_mem W s c hc
  exact (unitorSeedGauge_value W R D Qlocal c hVisible).trans
    (unitorBoundaryValue_eq_of_mem W R D Qlocal hUnit s c hVisible hc)

/-- Footprint locality transfers every unitor correction to this one seed. -/
theorem unitorSeedGauge_corrected
    (Qlocal : ThreeQuotientRouteState W → GeneratedQuotientGaugeParameters W R D)
    (hUnit : UnitorRestrictionPairwise W R D Qlocal)
    (hCorrect : ∀ X (s : UnitorRouteAt W X),
      Qlocal (unitorRouteState W s) ∈
        quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    {X : W.Localization} (s : UnitorRouteAt W X) :
    unitorSeedGauge W R D Qlocal ∈
      quotientRouteCorrectionLocus W R D (unitorRouteState W s) := by
  exact (quotientRouteCorrectedBy_congr_of_agreesOnRouteState W R D
    (unitorSeedGauge W R D Qlocal) (Qlocal (unitorRouteState W s))
    (unitorRouteState W s) (unitorSeedGauge_agrees W R D Qlocal hUnit s)).2
      (hCorrect X s)

/-- The existing nested-witness hypothesis supplies a single gauge correcting
all unitors. No associator correction or nonempty object type is assumed. -/
theorem exists_unitorSeed_of_pairwiseShared
    (H : HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D) :
    ∃ Q : GeneratedQuotientGaugeParameters W R D,
      ∀ X (s : UnitorRouteAt W X),
        Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s) := by
  rcases globalUnitorFamily_of_pairwiseShared W R D H with ⟨U, hCorrect, hPair⟩
  let F := extendUnitorFamily W R D U
  have hUnit : UnitorRestrictionPairwise W R D F := by
    intro X Y s t
    change AgreeOnRouteFootprintOverlap W R D
      (unitorRouteState W s) (unitorRouteState W t)
      (extendUnitorFamily W R D U (unitorRouteState W s))
      (extendUnitorFamily W R D U (unitorRouteState W t))
    rw [extendUnitorFamily_unitor, extendUnitorFamily_unitor]
    exact hPair X Y s t
  have hCorrectF : ∀ X (s : UnitorRouteAt W X),
      F (unitorRouteState W s) ∈
        quotientRouteCorrectionLocus W R D (unitorRouteState W s) := by
    intro X s
    change extendUnitorFamily W R D U (unitorRouteState W s) ∈
      quotientRouteCorrectionLocus W R D (unitorRouteState W s)
    rw [extendUnitorFamily_unitor]
    exact hCorrect X s
  exact ⟨unitorSeedGauge W R D F,
    fun X s => unitorSeedGauge_corrected W R D F hUnit hCorrectF s⟩

/-! ## Finite sequential completion and its invariants -/

/-- Apply actual v3.37 completions in list order, always using the current gauge. -/
noncomputable def runAssociatorSchedule
    (tasks : List (AssociatorTask W)) (Q : GeneratedQuotientGaugeParameters W R D) :
    GeneratedQuotientGaugeParameters W R D :=
  tasks.foldl (fun current a => completeAssociatorLeading W R D current a.f a.g a.h) Q

/-- A coordinate never selected as a leading key keeps its original value.
No freshness, correction, or noninterference hypothesis is needed here. -/
theorem runAssociatorSchedule_value_eq_of_untouched
    (tasks : List (AssociatorTask W)) (Q : GeneratedQuotientGaugeParameters W R D)
    (c : QuotientGaugeCoordinate W)
    (hAvoid : ∀ a ∈ tasks, c ≠ associatorTaskLeadingCoordinate W a) :
    quotientGaugeCoordinateValue W R D (runAssociatorSchedule W R D tasks Q) c =
      quotientGaugeCoordinateValue W R D Q c := by
  revert hAvoid
  induction tasks generalizing Q with
  | nil =>
      intro _hAvoid
      rfl
  | cons a tasks ih =>
      intro hAvoid
      change quotientGaugeCoordinateValue W R D
        (runAssociatorSchedule W R D tasks
          (completeAssociatorLeading W R D Q a.f a.g a.h)) c = _
      exact (ih (completeAssociatorLeading W R D Q a.f a.g a.h)
        (fun b hb => hAvoid b (List.mem_cons_of_mem a hb))).trans
          (quotientGaugeUpdate_value_of_ne W R D Q (associatorTaskLeadingCoordinate W a)
            (associatorLeadingGaugeValue W R D Q a.f a.g a.h) c
            (hAvoid a (by simp)))

/-- Every route avoiding all selected leading keys keeps its full footprint. -/
theorem runAssociatorSchedule_agrees_of_avoided
    (tasks : List (AssociatorTask W)) (Q : GeneratedQuotientGaugeParameters W R D)
    (s : ThreeQuotientRouteState W)
    (hAvoid : ∀ a ∈ tasks,
      ¬ RouteFootprintContains W s (associatorTaskLeadingCoordinate W a)) :
    QuotientGaugesAgreeOnRouteState W R D
      (runAssociatorSchedule W R D tasks Q) Q s := by
  apply quotientGaugesAgreeOnRouteState_of_coordinateValue_eq W R D
  intro c hc
  exact runAssociatorSchedule_value_eq_of_untouched W R D tasks Q c
    (fun a ha hca => hAvoid a ha (hca ▸ hc))

/-- Correction of every avoided route is preserved in both directions. -/
theorem runAssociatorSchedule_mem_locus_iff_of_avoided
    (tasks : List (AssociatorTask W)) (Q : GeneratedQuotientGaugeParameters W R D)
    (s : ThreeQuotientRouteState W)
    (hAvoid : ∀ a ∈ tasks,
      ¬ RouteFootprintContains W s (associatorTaskLeadingCoordinate W a)) :
    runAssociatorSchedule W R D tasks Q ∈ quotientRouteCorrectionLocus W R D s ↔
      Q ∈ quotientRouteCorrectionLocus W R D s := by
  exact quotientRouteCorrectedBy_congr_of_agreesOnRouteState W R D
    (runAssociatorSchedule W R D tasks Q) Q s
    (runAssociatorSchedule_agrees_of_avoided W R D tasks Q s hAvoid)

/-- Later updates avoid every earlier footprint, so all scheduled corrections
hold simultaneously at the end. Initially none of them need be corrected. -/
theorem runAssociatorSchedule_corrects
    (tasks : List (AssociatorTask W)) (Q : GeneratedQuotientGaugeParameters W R D)
    (hFresh : ∀ a ∈ tasks, FreshAssociatorLeadingCoordinate W a.f a.g a.h)
    (hSafe : ForwardNoninterferingSchedule W tasks) :
    ∀ a ∈ tasks, runAssociatorSchedule W R D tasks Q ∈
      quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  revert hFresh hSafe
  induction tasks generalizing Q with
  | nil =>
      intro _hFresh _hSafe a ha
      cases ha
  | cons a tasks ih =>
      intro hFresh hSafe
      have hParts :
          (∀ b ∈ tasks, ¬ RouteFootprintContains W (associatorTaskRoute W a)
            (associatorTaskLeadingCoordinate W b)) ∧
          ForwardNoninterferingSchedule W tasks := List.pairwise_cons.mp hSafe
      have hTailFresh : ∀ b ∈ tasks, FreshAssociatorLeadingCoordinate W b.f b.g b.h :=
        fun b hb => hFresh b (List.mem_cons_of_mem a hb)
      intro b hb
      change runAssociatorSchedule W R D tasks
        (completeAssociatorLeading W R D Q a.f a.g a.h) ∈
          quotientRouteCorrectionLocus W R D (associatorTaskRoute W b)
      rcases List.mem_cons.mp hb with hba | hb
      · subst b
        exact (runAssociatorSchedule_mem_locus_iff_of_avoided W R D tasks
          (completeAssociatorLeading W R D Q a.f a.g a.h)
          (associatorTaskRoute W a) hParts.1).2
            (completeAssociatorLeading_corrected W R D Q a.f a.g a.h
              (hFresh a (by simp)))
      · exact ih (completeAssociatorLeading W R D Q a.f a.g a.h)
          hTailFresh hParts.2 b hb

/-- Interior schedules leave the whole unitor boundary fixed, even before
freshness and forward noninterference are imposed. -/
theorem runAssociatorSchedule_boundary_value_eq
    (tasks : List (AssociatorTask W)) (Q : GeneratedQuotientGaugeParameters W R D)
    (hInterior : ∀ a ∈ tasks, ¬ UnitorVisibleCoordinate W (associatorTaskLeadingCoordinate W a))
    (c : QuotientGaugeCoordinate W) (hc : UnitorVisibleCoordinate W c) :
    quotientGaugeCoordinateValue W R D (runAssociatorSchedule W R D tasks Q) c =
      quotientGaugeCoordinateValue W R D Q c := by
  exact runAssociatorSchedule_value_eq_of_untouched W R D tasks Q c
    (fun a ha hca => hInterior a ha (hca ▸ hc))

/-- Every unitor correction survives an interior schedule. -/
theorem runAssociatorSchedule_unitor_corrected_iff
    (tasks : List (AssociatorTask W)) (Q : GeneratedQuotientGaugeParameters W R D)
    (hInterior : ∀ a ∈ tasks, ¬ UnitorVisibleCoordinate W (associatorTaskLeadingCoordinate W a))
    {X : W.Localization} (s : UnitorRouteAt W X) :
    runAssociatorSchedule W R D tasks Q ∈
        quotientRouteCorrectionLocus W R D (unitorRouteState W s) ↔
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s) := by
  exact runAssociatorSchedule_mem_locus_iff_of_avoided W R D tasks Q
    (unitorRouteState W s) (fun a ha hMem =>
      hInterior a ha (unitorVisibleCoordinate_of_mem W s
        (associatorTaskLeadingCoordinate W a) hMem))

/-- A single witness corrects all unitors and the entire prescribed finite
schedule. The witness is constructed, not assumed in the hypotheses. -/
theorem exists_commonGauge_for_finiteSchedule_of_pairwiseShared
    (H : HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D)
    (tasks : List (AssociatorTask W))
    (hFresh : ∀ a ∈ tasks, FreshAssociatorLeadingCoordinate W a.f a.g a.h)
    (hSafe : ForwardNoninterferingSchedule W tasks)
    (hInterior : ∀ a ∈ tasks, ¬ UnitorVisibleCoordinate W (associatorTaskLeadingCoordinate W a)) :
    ∃ Q : GeneratedQuotientGaugeParameters W R D,
      (∀ X (s : UnitorRouteAt W X),
        Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s)) ∧
      ∀ a ∈ tasks, Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  rcases exists_unitorSeed_of_pairwiseShared W R D H with ⟨Q, hQ⟩
  refine ⟨runAssociatorSchedule W R D tasks Q, ?_,
    runAssociatorSchedule_corrects W R D tasks Q hFresh hSafe⟩
  intro X s
  exact (runAssociatorSchedule_unitor_corrected_iff W R D tasks Q hInterior s).2 (hQ X s)

/-!
## Boundary

One common gauge is obtained for all unitors and the listed associators under
three explicit conditions: each leading key is fresh within its own route,
later keys avoid earlier footprints, and every leading key is unitor-interior.
No pairwise disjointness of entire footprints is required. The schedule is
ordered; no order-independence or arbitrary reordering theorem is asserted.

This does not prove that every finite collection admits such a schedule, or
that a sequence of finite witnesses yields a global all-route witness. In
particular the middle-identity obstruction from v3.37 still excludes those
tasks from the freshness premise. No general finite-intersection, compactness,
all-route gluing, comparison-coherence, Stage-I or Stage-II conclusion follows.
All W/R/D choices and the earlier mixed-triangle hypotheses remain fixed.
-/

end KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
