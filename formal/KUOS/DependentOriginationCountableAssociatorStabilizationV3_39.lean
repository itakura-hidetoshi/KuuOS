import KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
import Mathlib.Data.Nat.Basic

namespace KUOS.DependentOriginationCountableAssociatorStabilizationV3_39

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
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38

universe u v uH vH

set_option autoImplicit false

/-!
# Countable associator completion by exact coordinate stabilization v3.39

v3.38 constructs one gauge for a finite forward-noninterfering schedule.
Here a prescribed sequence of actual tasks is processed from the same initial
gauge, with the same v3.37 update at every successor stage. Later leading
coordinates avoid earlier footprints. This implies that the leading-coordinate
map is injective, and that every coordinate becomes exactly constant.

Choose a stabilization index separately at each dependent coordinate. Comparing
two such indices at their maximum proves equality of the resulting values.
The assembled gauge therefore agrees with the gauge immediately after task i
on the entire footprint of task i. Existing footprint locality transfers its
correction to the assembled gauge. Interior leading coordinates preserve every
unitor value from stage zero, and the v3.38 seed theorem supplies that stage.

No compactness, finite-intersection principle, or choice of unrelated finite
solutions is used. This constructs a common witness for the prescribed sequence,
not an enumeration or a simultaneous correction of all possible associators.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The sequence analogue of v3.38's directional list condition. -/
def CountableForwardNoninterference (tasks : ℕ → AssociatorTask W) : Prop :=
  ∀ i j : ℕ, i < j →
    ¬ RouteFootprintContains W (associatorTaskRoute W (tasks i))
      (associatorTaskLeadingCoordinate W (tasks j))

/-- Every leading key belongs to its own actual associator footprint. -/
theorem associatorTaskLeadingCoordinate_mem (a : AssociatorTask W) :
    RouteFootprintContains W (associatorTaskRoute W a)
      (associatorTaskLeadingCoordinate W a) :=
  Or.inl rfl

/-- Forward noninterference forbids repeated leading keys, without freshness
or any assumption about the gauge values. -/
theorem countable_leadingCoordinate_injective
    (tasks : ℕ → AssociatorTask W)
    (hSafe : CountableForwardNoninterference W tasks) :
    Function.Injective (fun i => associatorTaskLeadingCoordinate W (tasks i)) := by
  intro i j hij
  rcases lt_trichotomy i j with hlt | heq | hgt
  · exact False.elim (hSafe i j hlt
      (hij ▸ associatorTaskLeadingCoordinate_mem W (tasks i)))
  · exact heq
  · exact False.elim (hSafe j i hgt
      (hij.symm ▸ associatorTaskLeadingCoordinate_mem W (tasks j)))

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-! ## Assemble an exactly stabilizing dependent gauge sequence -/

/-- Each coordinate of one sequence is eventually exactly constant.
This is an algebraic condition, not topological convergence. -/
def GaugeSequenceStabilizes
    (G : ℕ → GeneratedQuotientGaugeParameters W R D) : Prop :=
  ∀ c : QuotientGaugeCoordinate W, ∃ N : ℕ, ∀ n : ℕ, N ≤ n →
    quotientGaugeCoordinateValue W R D (G n) c =
      quotientGaugeCoordinateValue W R D (G N) c

/-- Read the coordinate at one certified stabilization index. -/
noncomputable def stabilizedGaugeValue
    (G : ℕ → GeneratedQuotientGaugeParameters W R D)
    (hG : GaugeSequenceStabilizes W R D G)
    (c : QuotientGaugeCoordinate W) : QuotientGaugeCoordinateFiber W R D c :=
  quotientGaugeCoordinateValue W R D (G (Classical.choose (hG c))) c

/-- Assemble the dependent coordinate values into the existing gauge structure. -/
noncomputable def stabilizedGauge
    (G : ℕ → GeneratedQuotientGaugeParameters W R D)
    (hG : GaugeSequenceStabilizes W R D G) :
    GeneratedQuotientGaugeParameters W R D where
  mapIdGauge X := stabilizedGaugeValue W R D G hG (.identity X)
  mapCompGauge f g := stabilizedGaugeValue W R D G hG (.composition f g)

/-- Evaluation recovers exactly the selected value, for both key constructors. -/
theorem stabilizedGauge_value
    (G : ℕ → GeneratedQuotientGaugeParameters W R D)
    (hG : GaugeSequenceStabilizes W R D G)
    (c : QuotientGaugeCoordinate W) :
    quotientGaugeCoordinateValue W R D (stabilizedGauge W R D G hG) c =
      stabilizedGaugeValue W R D G hG c := by
  cases c <;> rfl

/-- Any certified stabilization index gives the same value. The comparison at
max M N prevents an arbitrary choice of indices from standing in for coherence. -/
theorem stabilizedGauge_value_eq_of_stable
    (G : ℕ → GeneratedQuotientGaugeParameters W R D)
    (hG : GaugeSequenceStabilizes W R D G)
    (c : QuotientGaugeCoordinate W) (N : ℕ)
    (hN : ∀ n : ℕ, N ≤ n →
      quotientGaugeCoordinateValue W R D (G n) c =
        quotientGaugeCoordinateValue W R D (G N) c) :
    quotientGaugeCoordinateValue W R D (stabilizedGauge W R D G hG) c =
      quotientGaugeCoordinateValue W R D (G N) c := by
  let M : ℕ := Classical.choose (hG c)
  have hM : ∀ n : ℕ, M ≤ n →
      quotientGaugeCoordinateValue W R D (G n) c =
        quotientGaugeCoordinateValue W R D (G M) c :=
    Classical.choose_spec (hG c)
  rw [stabilizedGauge_value]
  change quotientGaugeCoordinateValue W R D (G M) c =
    quotientGaugeCoordinateValue W R D (G N) c
  exact (hM (max M N) (le_max_left M N)).symm.trans
    (hN (max M N) (le_max_right M N))

/-! ## One evolving sequence of actual local completions -/

/-- Stage n is the result after the first n tasks. The accumulator is always
the current gauge, never an independently chosen finite witness. -/
noncomputable def countableAssociatorStage
    (tasks : ℕ → AssociatorTask W) (Q0 : GeneratedQuotientGaugeParameters W R D) :
    ℕ → GeneratedQuotientGaugeParameters W R D :=
  Nat.rec (motive := fun _ => GeneratedQuotientGaugeParameters W R D) Q0
    (fun n current => completeAssociatorLeading W R D current
      (tasks n).f (tasks n).g (tasks n).h)

/-- Each successor stage changes only the current leading coordinate. -/
theorem countableAssociatorStage_succ_value_of_ne
    (tasks : ℕ → AssociatorTask W) (Q0 : GeneratedQuotientGaugeParameters W R D)
    (n : ℕ) (c : QuotientGaugeCoordinate W)
    (hc : c ≠ associatorTaskLeadingCoordinate W (tasks n)) :
    quotientGaugeCoordinateValue W R D (countableAssociatorStage W R D tasks Q0 (n + 1)) c =
      quotientGaugeCoordinateValue W R D (countableAssociatorStage W R D tasks Q0 n) c := by
  exact quotientGaugeUpdate_value_of_ne W R D
    (countableAssociatorStage W R D tasks Q0 n)
    (associatorTaskLeadingCoordinate W (tasks n))
    (associatorLeadingGaugeValue W R D (countableAssociatorStage W R D tasks Q0 n)
      (tasks n).f (tasks n).g (tasks n).h) c hc

/-- Avoidance after N implies literal constancy after N. The induction motive
keeps both the stage and its lower-bound proof explicit. -/
theorem countableAssociatorStage_value_eq_of_avoids_after
    (tasks : ℕ → AssociatorTask W) (Q0 : GeneratedQuotientGaugeParameters W R D)
    (c : QuotientGaugeCoordinate W) (N : ℕ)
    (hAvoid : ∀ k : ℕ, N ≤ k → c ≠ associatorTaskLeadingCoordinate W (tasks k)) :
    ∀ n : ℕ, N ≤ n →
      quotientGaugeCoordinateValue W R D (countableAssociatorStage W R D tasks Q0 n) c =
        quotientGaugeCoordinateValue W R D (countableAssociatorStage W R D tasks Q0 N) c := by
  intro n hn
  refine Nat.le_induction (m := N)
    (P := fun k _ =>
      quotientGaugeCoordinateValue W R D (countableAssociatorStage W R D tasks Q0 k) c =
        quotientGaugeCoordinateValue W R D (countableAssociatorStage W R D tasks Q0 N) c)
    rfl ?_ n hn
  intro k hk ih
  exact (countableAssociatorStage_succ_value_of_ne W R D tasks Q0 k c (hAvoid k hk)).trans ih

/-- Every coordinate stabilizes: it is never selected, or it is selected at i
and no later leading key can revisit it. No correction premise is needed. -/
theorem countableAssociatorStage_stabilizes
    (tasks : ℕ → AssociatorTask W) (Q0 : GeneratedQuotientGaugeParameters W R D)
    (hSafe : CountableForwardNoninterference W tasks) :
    GaugeSequenceStabilizes W R D (countableAssociatorStage W R D tasks Q0) := by
  classical
  intro c
  by_cases hHit : ∃ i : ℕ, c = associatorTaskLeadingCoordinate W (tasks i)
  · rcases hHit with ⟨i, rfl⟩
    refine ⟨i + 1, ?_⟩
    exact countableAssociatorStage_value_eq_of_avoids_after W R D tasks Q0
      (associatorTaskLeadingCoordinate W (tasks i)) (i + 1)
      (fun j hij heq => hSafe i j (Nat.lt_of_succ_le hij)
        (heq ▸ associatorTaskLeadingCoordinate_mem W (tasks i)))
  · refine ⟨0, ?_⟩
    exact countableAssociatorStage_value_eq_of_avoids_after W R D tasks Q0 c 0
      (fun j _hc heq => hHit ⟨j, heq⟩)

/-- The actual assembled gauge for a safe countable schedule. -/
noncomputable def countableAssociatorGauge
    (tasks : ℕ → AssociatorTask W) (Q0 : GeneratedQuotientGaugeParameters W R D)
    (hSafe : CountableForwardNoninterference W tasks) :
    GeneratedQuotientGaugeParameters W R D :=
  stabilizedGauge W R D (countableAssociatorStage W R D tasks Q0)
    (countableAssociatorStage_stabilizes W R D tasks Q0 hSafe)

/-- The assembled value equals any stage after which that coordinate is untouched. -/
theorem countableAssociatorGauge_value_eq_of_avoids_after
    (tasks : ℕ → AssociatorTask W) (Q0 : GeneratedQuotientGaugeParameters W R D)
    (hSafe : CountableForwardNoninterference W tasks)
    (c : QuotientGaugeCoordinate W) (N : ℕ)
    (hAvoid : ∀ k : ℕ, N ≤ k → c ≠ associatorTaskLeadingCoordinate W (tasks k)) :
    quotientGaugeCoordinateValue W R D (countableAssociatorGauge W R D tasks Q0 hSafe) c =
      quotientGaugeCoordinateValue W R D (countableAssociatorStage W R D tasks Q0 N) c := by
  exact stabilizedGauge_value_eq_of_stable W R D
    (countableAssociatorStage W R D tasks Q0)
    (countableAssociatorStage_stabilizes W R D tasks Q0 hSafe) c N
    (countableAssociatorStage_value_eq_of_avoids_after W R D tasks Q0 c N hAvoid)

/-- A processed associator footprint is frozen at its immediate post-completion
stage, even though coordinates outside it may continue to change. -/
theorem countableAssociatorGauge_agrees_at_completion
    (tasks : ℕ → AssociatorTask W) (Q0 : GeneratedQuotientGaugeParameters W R D)
    (hSafe : CountableForwardNoninterference W tasks) (i : ℕ) :
    QuotientGaugesAgreeOnRouteState W R D
      (countableAssociatorGauge W R D tasks Q0 hSafe)
      (countableAssociatorStage W R D tasks Q0 (i + 1))
      (associatorTaskRoute W (tasks i)) := by
  apply quotientGaugesAgreeOnRouteState_of_coordinateValue_eq W R D
  intro c hc
  exact countableAssociatorGauge_value_eq_of_avoids_after W R D tasks Q0 hSafe c (i + 1)
    (fun j hij heq => hSafe i j (Nat.lt_of_succ_le hij) (heq ▸ hc))

/-- Freshness corrects the current task at its successor stage; footprint
locality then transfers that same equation to the assembled gauge. -/
theorem countableAssociatorGauge_corrects_task
    (tasks : ℕ → AssociatorTask W) (Q0 : GeneratedQuotientGaugeParameters W R D)
    (hSafe : CountableForwardNoninterference W tasks) (i : ℕ)
    (hFresh : FreshAssociatorLeadingCoordinate W (tasks i).f (tasks i).g (tasks i).h) :
    countableAssociatorGauge W R D tasks Q0 hSafe ∈
      quotientRouteCorrectionLocus W R D (associatorTaskRoute W (tasks i)) := by
  have hDone : countableAssociatorStage W R D tasks Q0 (i + 1) ∈
      quotientRouteCorrectionLocus W R D (associatorTaskRoute W (tasks i)) :=
    completeAssociatorLeading_corrected W R D
      (countableAssociatorStage W R D tasks Q0 i) (tasks i).f (tasks i).g (tasks i).h hFresh
  exact (quotientRouteCorrectedBy_congr_of_agreesOnRouteState W R D
    (countableAssociatorGauge W R D tasks Q0 hSafe)
    (countableAssociatorStage W R D tasks Q0 (i + 1))
    (associatorTaskRoute W (tasks i))
    (countableAssociatorGauge_agrees_at_completion W R D tasks Q0 hSafe i)).2 hDone

/-- Every route avoiding all leading keys retains its complete initial footprint. -/
theorem countableAssociatorGauge_agrees_of_avoided
    (tasks : ℕ → AssociatorTask W) (Q0 : GeneratedQuotientGaugeParameters W R D)
    (hSafe : CountableForwardNoninterference W tasks) (s : ThreeQuotientRouteState W)
    (hAvoid : ∀ i : ℕ, ¬ RouteFootprintContains W s
      (associatorTaskLeadingCoordinate W (tasks i))) :
    QuotientGaugesAgreeOnRouteState W R D
      (countableAssociatorGauge W R D tasks Q0 hSafe) Q0 s := by
  apply quotientGaugesAgreeOnRouteState_of_coordinateValue_eq W R D
  intro c hc
  exact countableAssociatorGauge_value_eq_of_avoids_after W R D tasks Q0 hSafe c 0
    (fun i _hi heq => hAvoid i (heq ▸ hc))

/-- Existing corrections on every untouched route survive, in both directions. -/
theorem countableAssociatorGauge_mem_locus_iff_of_avoided
    (tasks : ℕ → AssociatorTask W) (Q0 : GeneratedQuotientGaugeParameters W R D)
    (hSafe : CountableForwardNoninterference W tasks) (s : ThreeQuotientRouteState W)
    (hAvoid : ∀ i : ℕ, ¬ RouteFootprintContains W s
      (associatorTaskLeadingCoordinate W (tasks i))) :
    countableAssociatorGauge W R D tasks Q0 hSafe ∈ quotientRouteCorrectionLocus W R D s ↔
      Q0 ∈ quotientRouteCorrectionLocus W R D s := by
  exact quotientRouteCorrectedBy_congr_of_agreesOnRouteState W R D
    (countableAssociatorGauge W R D tasks Q0 hSafe) Q0 s
    (countableAssociatorGauge_agrees_of_avoided W R D tasks Q0 hSafe s hAvoid)

/-- Interior leading keys preserve all unitor-boundary values from stage zero. -/
theorem countableAssociatorGauge_boundary_value_eq
    (tasks : ℕ → AssociatorTask W) (Q0 : GeneratedQuotientGaugeParameters W R D)
    (hSafe : CountableForwardNoninterference W tasks)
    (hInterior : ∀ i : ℕ, ¬ UnitorVisibleCoordinate W
      (associatorTaskLeadingCoordinate W (tasks i)))
    (c : QuotientGaugeCoordinate W) (hc : UnitorVisibleCoordinate W c) :
    quotientGaugeCoordinateValue W R D (countableAssociatorGauge W R D tasks Q0 hSafe) c =
      quotientGaugeCoordinateValue W R D Q0 c := by
  exact countableAssociatorGauge_value_eq_of_avoids_after W R D tasks Q0 hSafe c 0
    (fun i _hi heq => hInterior i (heq ▸ hc))

/-- All previously corrected unitors remain corrected in the assembled gauge. -/
theorem countableAssociatorGauge_unitor_corrected_iff
    (tasks : ℕ → AssociatorTask W) (Q0 : GeneratedQuotientGaugeParameters W R D)
    (hSafe : CountableForwardNoninterference W tasks)
    (hInterior : ∀ i : ℕ, ¬ UnitorVisibleCoordinate W
      (associatorTaskLeadingCoordinate W (tasks i)))
    {X : W.Localization} (s : UnitorRouteAt W X) :
    countableAssociatorGauge W R D tasks Q0 hSafe ∈
        quotientRouteCorrectionLocus W R D (unitorRouteState W s) ↔
      Q0 ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s) := by
  exact countableAssociatorGauge_mem_locus_iff_of_avoided W R D tasks Q0 hSafe
    (unitorRouteState W s) (fun i hMem =>
      hInterior i (unitorVisibleCoordinate_of_mem W s
        (associatorTaskLeadingCoordinate W (tasks i)) hMem))

/-- One gauge corrects every unitor and every task in the prescribed countable
sequence. The seed comes from v3.38, and coordinate stabilization is proved above. -/
theorem exists_commonGauge_for_countableSchedule_of_pairwiseShared
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
      ∀ i : ℕ, Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W (tasks i)) := by
  rcases exists_unitorSeed_of_pairwiseShared W R D H with ⟨Q0, hQ0⟩
  refine ⟨countableAssociatorGauge W R D tasks Q0 hSafe, ?_, ?_⟩
  · intro X s
    exact (countableAssociatorGauge_unitor_corrected_iff W R D tasks Q0 hSafe hInterior s).2
      (hQ0 X s)
  · intro i
    exact countableAssociatorGauge_corrects_task W R D tasks Q0 hSafe i (hFresh i)

/-!
## Boundary

The input is one specified natural-number-indexed sequence satisfying explicit
freshness, directional noninterference, and unitor-interiority. No existence of
such an ordering, countability of all route states, or coverage of all
associators is inferred. In particular the v3.37 middle-identity collision is
still outside the freshness premise.

The stabilization-index choice is value-independent for this fixed sequence
and fixed initial gauge. It is not independence from a different schedule,
seed, or W/R/D. No order-independence, compactness, general finite-intersection
principle, unrestricted witness correlation, or comparison-gauge equation is
asserted. General Stage I, Stage II and final universality remain separate.
-/

end KUOS.DependentOriginationCountableAssociatorStabilizationV3_39
