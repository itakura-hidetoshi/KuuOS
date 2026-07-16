import Mathlib
import KUOS.OpenHorizon.MemoryOSProperClosedContextRepresentationV0_91

namespace KUOS.OpenHorizon.MemoryOSCounterexampleGuidedContextRefinementV0_91

open KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
open KUOS.OpenHorizon.MemoryOSRootedRouteAtlasNielsenChangeV0_78
open KUOS.OpenHorizon.MemoryOSAllRootChartDefectAwareWordTransportV0_80
open KUOS.OpenHorizon.MemoryOSNormalizedRootWordGroupoidDescentV0_81
open KUOS.OpenHorizon.MemoryOSGlobalWordCechDescentV0_82
open KUOS.OpenHorizon.MemoryOSGlobalSectionGroupAnchorCoherenceV0_83
open KUOS.OpenHorizon.MemoryOSGlobalObservableKernelQuotientV0_84
open KUOS.OpenHorizon.MemoryOSObservableSensorCoarseningV0_85
open KUOS.OpenHorizon.MemoryOSJointSensorProductRefinementV0_86
open KUOS.OpenHorizon.MemoryOSFiniteSensorFamilyRefinementV0_87
open KUOS.OpenHorizon.MemoryOSExactSensorCoreV0_88
open KUOS.OpenHorizon.MemoryOSSensorSupportClosureV0_89
open KUOS.OpenHorizon.MemoryOSFullClosedSupportRepresentationV0_90

/-- Add the canonical closed counterexample `cl(premise)` to a selected context family. -/
noncomputable def refineClosedContexts
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (contexts : Finset (Finset ι))
    (premise : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset (Finset ι) := by
  classical
  exact insert (sensorSupportClosure sensors premise atlas targetDefect root) contexts

theorem mem_refine_closed_contexts_iff
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (contexts : Finset (Finset ι))
    (premise context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    context ∈ refineClosedContexts sensors contexts premise atlas targetDefect root ↔
      context = sensorSupportClosure sensors premise atlas targetDefect root ∨
        context ∈ contexts := by
  classical
  simp [refineClosedContexts]

/-- Canonical refinement preserves the invariant that every selected context is closed. -/
theorem refine_closed_contexts_are_closed
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (contexts : Finset (Finset ι))
    (premise : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hclosed : ∀ context ∈ contexts,
      SensorSupportClosed sensors context atlas targetDefect root) :
    ∀ context ∈ refineClosedContexts sensors contexts premise atlas targetDefect root,
      SensorSupportClosed sensors context atlas targetDefect root := by
  intro context hcontext
  rw [mem_refine_closed_contexts_iff] at hcontext
  rcases hcontext with hclosure | hold
  · subst context
    exact sensor_support_closure_closed sensors premise atlas targetDefect root
  · exact hclosed context hold

/-- Adding contexts can only remove selected-context consequences. -/
theorem selected_context_consequence_antitone
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (smaller larger : Finset (Finset ι)) (premise : Finset ι) (i : ι)
    (hsubset : smaller ⊆ larger)
    (hconsequence :
      supportTruthRegion larger premise ⊆ sensorTruthRegion larger i) :
    supportTruthRegion smaller premise ⊆ sensorTruthRegion smaller i := by
  intro context hcontext
  rw [mem_support_truth_region_iff] at hcontext
  have hlarger_premise : context ∈ supportTruthRegion larger premise := by
    rw [mem_support_truth_region_iff]
    exact ⟨hsubset hcontext.1, hcontext.2⟩
  have hlarger_sensor := hconsequence hlarger_premise
  rw [mem_sensor_truth_region_iff] at hlarger_sensor
  rw [mem_sensor_truth_region_iff]
  exact ⟨hcontext.1, hlarger_sensor.2⟩

theorem contexts_subset_refinement
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (contexts : Finset (Finset ι))
    (premise : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    contexts ⊆ refineClosedContexts sensors contexts premise atlas targetDefect root := by
  intro context hcontext
  rw [mem_refine_closed_contexts_iff]
  exact Or.inr hcontext

/-- A true closure consequence survives canonical counterexample refinement. -/
theorem canonical_refinement_preserves_consequence
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (contexts : Finset (Finset ι))
    (premise : Finset ι) (i : ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hclosed : ∀ context ∈ contexts,
      SensorSupportClosed sensors context atlas targetDefect root)
    (hi : i ∈ sensorSupportClosure sensors premise atlas targetDefect root) :
    supportTruthRegion
        (refineClosedContexts sensors contexts premise atlas targetDefect root) premise ⊆
      sensorTruthRegion
        (refineClosedContexts sensors contexts premise atlas targetDefect root) i := by
  exact selected_closed_context_truth_region_sound sensors
    (refineClosedContexts sensors contexts premise atlas targetDefect root)
    premise i atlas targetDefect root
    (refine_closed_contexts_are_closed sensors contexts premise
      atlas targetDefect root hclosed) hi

/-- If an implication is false, inserting `cl(premise)` refutes it immediately. -/
theorem canonical_refinement_refutes_nonconsequence
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (contexts : Finset (Finset ι))
    (premise : Finset ι) (i : ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hi : i ∉ sensorSupportClosure sensors premise atlas targetDefect root) :
    ¬ (supportTruthRegion
          (refineClosedContexts sensors contexts premise atlas targetDefect root) premise ⊆
        sensorTruthRegion
          (refineClosedContexts sensors contexts premise atlas targetDefect root) i) := by
  intro hconsequence
  let closure := sensorSupportClosure sensors premise atlas targetDefect root
  have hcontext :
      closure ∈ refineClosedContexts sensors contexts premise atlas targetDefect root := by
    rw [mem_refine_closed_contexts_iff]
    exact Or.inl rfl
  have hpremise :
      closure ∈ supportTruthRegion
        (refineClosedContexts sensors contexts premise atlas targetDefect root) premise := by
    rw [mem_support_truth_region_iff]
    exact ⟨hcontext,
      sensor_support_subset_closure sensors premise atlas targetDefect root⟩
  have hsensor := hconsequence hpremise
  have himembership := (mem_sensor_truth_region_iff
    (refineClosedContexts sensors contexts premise atlas targetDefect root)
    closure i).mp hsensor
  exact hi himembership.2

/-- One canonical counterexample makes the selected family exact for the queried implication. -/
theorem canonical_refinement_exact_for_query
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (contexts : Finset (Finset ι))
    (premise : Finset ι) (i : ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hclosed : ∀ context ∈ contexts,
      SensorSupportClosed sensors context atlas targetDefect root) :
    i ∈ sensorSupportClosure sensors premise atlas targetDefect root ↔
      supportTruthRegion
          (refineClosedContexts sensors contexts premise atlas targetDefect root) premise ⊆
        sensorTruthRegion
          (refineClosedContexts sensors contexts premise atlas targetDefect root) i := by
  constructor
  · exact canonical_refinement_preserves_consequence sensors contexts premise i
      atlas targetDefect root hclosed
  · intro hconsequence
    by_contra hi
    exact (canonical_refinement_refutes_nonconsequence sensors contexts premise i
      atlas targetDefect root hi) hconsequence

/-- Repeating the same canonical refinement is idempotent. -/
theorem refine_closed_contexts_idempotent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (contexts : Finset (Finset ι))
    (premise : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    refineClosedContexts sensors
        (refineClosedContexts sensors contexts premise atlas targetDefect root)
        premise atlas targetDefect root =
      refineClosedContexts sensors contexts premise atlas targetDefect root := by
  classical
  simp [refineClosedContexts]

/-- Proper closed contexts are root independent. -/
theorem proper_closed_sensor_supports_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    properClosedSensorSupports sensors atlas targetDefect sourceRoot =
      properClosedSensorSupports sensors atlas targetDefect targetRoot := by
  classical
  simp [properClosedSensorSupports,
    all_closed_sensor_supports_root_independent sensors atlas targetDefect
      sourceRoot targetRoot]

/-- Canonical refinement is root independent when its selected context family is fixed. -/
theorem refine_closed_contexts_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (contexts : Finset (Finset ι))
    (premise : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    refineClosedContexts sensors contexts premise atlas targetDefect sourceRoot =
      refineClosedContexts sensors contexts premise atlas targetDefect targetRoot := by
  classical
  simp [refineClosedContexts,
    sensor_support_closure_root_independent sensors premise atlas targetDefect
      sourceRoot targetRoot]

/-- Proper support truth regions are root independent. -/
theorem proper_support_truth_region_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (premise : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    supportTruthRegion
        (properClosedSensorSupports sensors atlas targetDefect sourceRoot) premise =
      supportTruthRegion
        (properClosedSensorSupports sensors atlas targetDefect targetRoot) premise := by
  rw [proper_closed_sensor_supports_root_independent sensors atlas targetDefect
    sourceRoot targetRoot]


end KUOS.OpenHorizon.MemoryOSCounterexampleGuidedContextRefinementV0_91
