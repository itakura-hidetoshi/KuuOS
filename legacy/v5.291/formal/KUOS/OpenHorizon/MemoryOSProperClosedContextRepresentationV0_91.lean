import Mathlib
import KUOS.OpenHorizon.MemoryOSFullClosedSupportRepresentationV0_90

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

/-- All closed supports except the universal context. The universal context cannot
separate any failed implication, so it is observationally redundant for consequence. -/
noncomputable def properClosedSensorSupports
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset (Finset ι) := by
  classical
  exact (allClosedSensorSupports sensors atlas targetDefect root).filter fun context =>
    context ≠ Finset.univ

theorem mem_proper_closed_sensor_supports_iff
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    context ∈ properClosedSensorSupports sensors atlas targetDefect root ↔
      SensorSupportClosed sensors context atlas targetDefect root ∧
        context ≠ Finset.univ := by
  classical
  simp [properClosedSensorSupports, mem_all_closed_sensor_supports_iff]

/-- The universal support is always closed. -/
theorem univ_sensor_support_closed
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    SensorSupportClosed sensors Finset.univ atlas targetDefect root := by
  unfold SensorSupportClosed
  apply Finset.Subset.antisymm
  · exact Finset.subset_univ _
  · exact sensor_support_subset_closure sensors Finset.univ atlas targetDefect root

theorem proper_closed_sensor_supports_subset_all
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    properClosedSensorSupports sensors atlas targetDefect root ⊆
      allClosedSensorSupports sensors atlas targetDefect root := by
  intro context hcontext
  rw [mem_proper_closed_sensor_supports_iff] at hcontext
  rw [mem_all_closed_sensor_supports_iff]
  exact hcontext.1

theorem proper_closed_contexts_are_closed
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    ∀ context ∈ properClosedSensorSupports sensors atlas targetDefect root,
      SensorSupportClosed sensors context atlas targetDefect root := by
  intro context hcontext
  have hproper := (mem_proper_closed_sensor_supports_iff sensors context
    atlas targetDefect root).mp hcontext
  exact hproper.1

/-- Removing the universal context preserves soundness. -/
theorem proper_closed_context_truth_region_sound
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (premise : Finset ι) (i : ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    i ∈ sensorSupportClosure sensors premise atlas targetDefect root →
      supportTruthRegion
          (properClosedSensorSupports sensors atlas targetDefect root) premise ⊆
        sensorTruthRegion
          (properClosedSensorSupports sensors atlas targetDefect root) i := by
  exact selected_closed_context_truth_region_sound sensors
    (properClosedSensorSupports sensors atlas targetDefect root)
    premise i atlas targetDefect root
    (proper_closed_contexts_are_closed sensors atlas targetDefect root)

/-- Every failed singleton consequence is still separated after deleting the universal context. -/
theorem mem_sensor_support_closure_iff_proper_truth_region_subset
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (premise : Finset ι) (i : ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    i ∈ sensorSupportClosure sensors premise atlas targetDefect root ↔
      supportTruthRegion
          (properClosedSensorSupports sensors atlas targetDefect root) premise ⊆
        sensorTruthRegion
          (properClosedSensorSupports sensors atlas targetDefect root) i := by
  constructor
  · exact proper_closed_context_truth_region_sound sensors premise i
      atlas targetDefect root
  · intro hregion
    let closure := sensorSupportClosure sensors premise atlas targetDefect root
    by_cases htop : closure = Finset.univ
    · rw [htop]
      exact Finset.mem_univ i
    · have hclosure_mem :
          closure ∈ properClosedSensorSupports sensors atlas targetDefect root := by
        rw [mem_proper_closed_sensor_supports_iff]
        exact ⟨sensor_support_closure_closed sensors premise atlas targetDefect root,
          htop⟩
      have hpremise_mem :
          closure ∈ supportTruthRegion
            (properClosedSensorSupports sensors atlas targetDefect root) premise := by
        rw [mem_support_truth_region_iff]
        exact ⟨hclosure_mem,
          sensor_support_subset_closure sensors premise atlas targetDefect root⟩
      have hi_region := hregion hpremise_mem
      exact ((mem_sensor_truth_region_iff
        (properClosedSensorSupports sensors atlas targetDefect root)
        closure i).mp hi_region).2

/-- Proper closed contexts exactly represent finite-support consequence. -/
theorem support_subset_closure_iff_proper_truth_region_subset
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (premise target : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    target ⊆ sensorSupportClosure sensors premise atlas targetDefect root ↔
      supportTruthRegion
          (properClosedSensorSupports sensors atlas targetDefect root) premise ⊆
        supportTruthRegion
          (properClosedSensorSupports sensors atlas targetDefect root) target := by
  constructor
  · intro htarget context hcontext
    rw [mem_support_truth_region_iff] at hcontext ⊢
    refine ⟨hcontext.1, ?_⟩
    have hfixed :=
      proper_closed_contexts_are_closed sensors atlas targetDefect root
        context hcontext.1
    have hclosure_subset :=
      sensor_support_closure_mono sensors hcontext.2 atlas targetDefect root
    rw [hfixed] at hclosure_subset
    exact htarget.trans hclosure_subset
  · intro hregion
    let closure := sensorSupportClosure sensors premise atlas targetDefect root
    by_cases htop : closure = Finset.univ
    · rw [htop]
      exact Finset.subset_univ _
    · have hclosure_mem :
          closure ∈ properClosedSensorSupports sensors atlas targetDefect root := by
        rw [mem_proper_closed_sensor_supports_iff]
        exact ⟨sensor_support_closure_closed sensors premise atlas targetDefect root,
          htop⟩
      have hpremise_mem :
          closure ∈ supportTruthRegion
            (properClosedSensorSupports sensors atlas targetDefect root) premise := by
        rw [mem_support_truth_region_iff]
        exact ⟨hclosure_mem,
          sensor_support_subset_closure sensors premise atlas targetDefect root⟩
      have htarget_mem := hregion hpremise_mem
      exact ((mem_support_truth_region_iff
        (properClosedSensorSupports sensors atlas targetDefect root)
        closure target).mp htarget_mem).2

/-- The universal closed context is redundant for singleton consequence. -/
theorem proper_and_full_single_sensor_consequence_equiv
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (premise : Finset ι) (i : ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    (supportTruthRegion
          (properClosedSensorSupports sensors atlas targetDefect root) premise ⊆
        sensorTruthRegion
          (properClosedSensorSupports sensors atlas targetDefect root) i) ↔
      (supportTruthRegion
          (allClosedSensorSupports sensors atlas targetDefect root) premise ⊆
        sensorTruthRegion
          (allClosedSensorSupports sensors atlas targetDefect root) i) := by
  constructor
  · intro hproper
    exact (mem_sensor_support_closure_iff_full_truth_region_subset
      sensors premise i atlas targetDefect root).mp
      ((mem_sensor_support_closure_iff_proper_truth_region_subset
        sensors premise i atlas targetDefect root).mpr hproper)
  · intro hfull
    exact (mem_sensor_support_closure_iff_proper_truth_region_subset
      sensors premise i atlas targetDefect root).mp
      ((mem_sensor_support_closure_iff_full_truth_region_subset
        sensors premise i atlas targetDefect root).mpr hfull)

/-- The universal closed context is redundant for finite-support consequence. -/
theorem proper_and_full_support_consequence_equiv
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (premise target : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    (supportTruthRegion
          (properClosedSensorSupports sensors atlas targetDefect root) premise ⊆
        supportTruthRegion
          (properClosedSensorSupports sensors atlas targetDefect root) target) ↔
      (supportTruthRegion
          (allClosedSensorSupports sensors atlas targetDefect root) premise ⊆
        supportTruthRegion
          (allClosedSensorSupports sensors atlas targetDefect root) target) := by
  constructor
  · intro hproper
    exact (support_subset_closure_iff_full_truth_region_subset
      sensors premise target atlas targetDefect root).mp
      ((support_subset_closure_iff_proper_truth_region_subset
        sensors premise target atlas targetDefect root).mpr hproper)
  · intro hfull
    exact (support_subset_closure_iff_proper_truth_region_subset
      sensors premise target atlas targetDefect root).mp
      ((support_subset_closure_iff_full_truth_region_subset
        sensors premise target atlas targetDefect root).mpr hfull)


end KUOS.OpenHorizon.MemoryOSCounterexampleGuidedContextRefinementV0_91
