import Mathlib
import KUOS.OpenHorizon.MemoryOSSensorSupportClosureV0_89

namespace KUOS.OpenHorizon.MemoryOSFullClosedSupportRepresentationV0_90

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

/-- All closed sensor supports at one root, used as the full finite context space. -/
noncomputable def allClosedSensorSupports
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset (Finset ι) := by
  classical
  exact Finset.univ.filter fun context =>
    SensorSupportClosed sensors context atlas targetDefect root

/-- Contexts in which one sensor is visible as a retained consequence. -/
noncomputable def sensorTruthRegion
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (contexts : Finset (Finset ι)) (i : ι) : Finset (Finset ι) := by
  classical
  exact contexts.filter fun context => i ∈ context

/-- Contexts containing every sensor in a premise support. -/
noncomputable def supportTruthRegion
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (contexts : Finset (Finset ι)) (premise : Finset ι) : Finset (Finset ι) := by
  classical
  exact contexts.filter fun context => premise ⊆ context

theorem mem_all_closed_sensor_supports_iff
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    context ∈ allClosedSensorSupports sensors atlas targetDefect root ↔
      SensorSupportClosed sensors context atlas targetDefect root := by
  classical
  simp [allClosedSensorSupports]

theorem mem_sensor_truth_region_iff
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (contexts : Finset (Finset ι)) (context : Finset ι) (i : ι) :
    context ∈ sensorTruthRegion contexts i ↔ context ∈ contexts ∧ i ∈ context := by
  classical
  simp [sensorTruthRegion]

theorem mem_support_truth_region_iff
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (contexts : Finset (Finset ι)) (context premise : Finset ι) :
    context ∈ supportTruthRegion contexts premise ↔
      context ∈ contexts ∧ premise ⊆ context := by
  classical
  simp [supportTruthRegion]

/-- Closure consequence is sound in every selected family of closed contexts. -/
theorem selected_closed_context_truth_region_sound
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (contexts : Finset (Finset ι))
    (premise : Finset ι) (i : ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hclosed : ∀ context ∈ contexts,
      SensorSupportClosed sensors context atlas targetDefect root) :
    i ∈ sensorSupportClosure sensors premise atlas targetDefect root →
      supportTruthRegion contexts premise ⊆ sensorTruthRegion contexts i := by
  intro hi context hcontext
  rw [mem_support_truth_region_iff] at hcontext
  rw [mem_sensor_truth_region_iff]
  refine ⟨hcontext.1, ?_⟩
  have himplied :=
    (sensor_support_closure_mono sensors hcontext.2 atlas targetDefect root) hi
  have hfixed := hclosed context hcontext.1
  rw [hfixed] at himplied
  exact himplied

/-- The full family of closed supports exactly represents single-sensor consequence. -/
theorem mem_sensor_support_closure_iff_full_truth_region_subset
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (premise : Finset ι) (i : ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    i ∈ sensorSupportClosure sensors premise atlas targetDefect root ↔
      supportTruthRegion
          (allClosedSensorSupports sensors atlas targetDefect root) premise ⊆
        sensorTruthRegion
          (allClosedSensorSupports sensors atlas targetDefect root) i := by
  constructor
  · exact selected_closed_context_truth_region_sound sensors
      (allClosedSensorSupports sensors atlas targetDefect root)
      premise i atlas targetDefect root (by
        intro context hcontext
        exact (mem_all_closed_sensor_supports_iff sensors context
          atlas targetDefect root).mp hcontext)
  · intro hregion
    let closure := sensorSupportClosure sensors premise atlas targetDefect root
    have hclosure_mem :
        closure ∈ allClosedSensorSupports sensors atlas targetDefect root := by
      rw [mem_all_closed_sensor_supports_iff]
      exact sensor_support_closure_closed sensors premise atlas targetDefect root
    have hpremise_mem :
        closure ∈ supportTruthRegion
          (allClosedSensorSupports sensors atlas targetDefect root) premise := by
      rw [mem_support_truth_region_iff]
      exact ⟨hclosure_mem,
        sensor_support_subset_closure sensors premise atlas targetDefect root⟩
    have hi_region := hregion hpremise_mem
    have hi_membership := (mem_sensor_truth_region_iff
      (allClosedSensorSupports sensors atlas targetDefect root) closure i).mp hi_region
    exact hi_membership.2

/-- The full family represents finite support consequence, not only singleton consequence. -/
theorem support_subset_closure_iff_full_truth_region_subset
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (premise target : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    target ⊆ sensorSupportClosure sensors premise atlas targetDefect root ↔
      supportTruthRegion
          (allClosedSensorSupports sensors atlas targetDefect root) premise ⊆
        supportTruthRegion
          (allClosedSensorSupports sensors atlas targetDefect root) target := by
  constructor
  · intro htarget context hcontext
    rw [mem_support_truth_region_iff] at hcontext ⊢
    refine ⟨hcontext.1, ?_⟩
    have hfixed := (mem_all_closed_sensor_supports_iff sensors context
      atlas targetDefect root).mp hcontext.1
    have hclosure_subset :=
      sensor_support_closure_mono sensors hcontext.2 atlas targetDefect root
    rw [hfixed] at hclosure_subset
    exact htarget.trans hclosure_subset
  · intro hregion
    let closure := sensorSupportClosure sensors premise atlas targetDefect root
    have hclosure_mem :
        closure ∈ allClosedSensorSupports sensors atlas targetDefect root := by
      rw [mem_all_closed_sensor_supports_iff]
      exact sensor_support_closure_closed sensors premise atlas targetDefect root
    have hpremise_mem :
        closure ∈ supportTruthRegion
          (allClosedSensorSupports sensors atlas targetDefect root) premise := by
      rw [mem_support_truth_region_iff]
      exact ⟨hclosure_mem,
        sensor_support_subset_closure sensors premise atlas targetDefect root⟩
    have htarget_mem := hregion hpremise_mem
    have htarget_membership := (mem_support_truth_region_iff
      (allClosedSensorSupports sensors atlas targetDefect root)
      closure target).mp htarget_mem
    exact htarget_membership.2

/-- Closing a premise does not change its full truth region. -/
theorem support_truth_region_closure_invariant
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (premise : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    supportTruthRegion (allClosedSensorSupports sensors atlas targetDefect root)
        (sensorSupportClosure sensors premise atlas targetDefect root) =
      supportTruthRegion (allClosedSensorSupports sensors atlas targetDefect root)
        premise := by
  classical
  apply Finset.ext
  intro context
  rw [mem_support_truth_region_iff, mem_support_truth_region_iff]
  constructor
  · rintro ⟨hcontext, hsubset⟩
    exact ⟨hcontext,
      (sensor_support_subset_closure sensors premise atlas targetDefect root).trans hsubset⟩
  · rintro ⟨hcontext, hsubset⟩
    refine ⟨hcontext, ?_⟩
    have hfixed := (mem_all_closed_sensor_supports_iff sensors context
      atlas targetDefect root).mp hcontext
    have hmono := sensor_support_closure_mono sensors hsubset
      atlas targetDefect root
    rw [hfixed] at hmono
    exact hmono

/-- Equal full truth regions are exactly equal support closures. -/
theorem support_truth_region_eq_iff_closure_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    supportTruthRegion (allClosedSensorSupports sensors atlas targetDefect root) left =
        supportTruthRegion (allClosedSensorSupports sensors atlas targetDefect root) right ↔
      sensorSupportClosure sensors left atlas targetDefect root =
        sensorSupportClosure sensors right atlas targetDefect root := by
  constructor
  · intro hregions
    classical
    apply Finset.ext
    intro i
    constructor
    · intro hi
      apply (mem_sensor_support_closure_iff_full_truth_region_subset
        sensors right i atlas targetDefect root).mpr
      rw [← hregions]
      exact (mem_sensor_support_closure_iff_full_truth_region_subset
        sensors left i atlas targetDefect root).mp hi
    · intro hi
      apply (mem_sensor_support_closure_iff_full_truth_region_subset
        sensors left i atlas targetDefect root).mpr
      rw [hregions]
      exact (mem_sensor_support_closure_iff_full_truth_region_subset
        sensors right i atlas targetDefect root).mp hi
  · intro hclosure
    calc
      supportTruthRegion (allClosedSensorSupports sensors atlas targetDefect root) left =
          supportTruthRegion (allClosedSensorSupports sensors atlas targetDefect root)
            (sensorSupportClosure sensors left atlas targetDefect root) :=
        (support_truth_region_closure_invariant sensors left
          atlas targetDefect root).symm
      _ = supportTruthRegion (allClosedSensorSupports sensors atlas targetDefect root)
            (sensorSupportClosure sensors right atlas targetDefect root) := by rw [hclosure]
      _ = supportTruthRegion (allClosedSensorSupports sensors atlas targetDefect root) right :=
        support_truth_region_closure_invariant sensors right atlas targetDefect root

/-- Full truth-region equality is also an exact classifier of invisible kernels. -/
theorem finite_sensor_support_kernel_eq_iff_full_truth_region_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    finiteSensorSupportKernel sensors left atlas targetDefect root =
        finiteSensorSupportKernel sensors right atlas targetDefect root ↔
      supportTruthRegion (allClosedSensorSupports sensors atlas targetDefect root) left =
        supportTruthRegion (allClosedSensorSupports sensors atlas targetDefect root) right := by
  constructor
  · intro hkernel
    exact (support_truth_region_eq_iff_closure_eq sensors left right
      atlas targetDefect root).mpr
      ((finite_sensor_support_kernel_eq_iff_closure_eq sensors left right
        atlas targetDefect root).mp hkernel)
  · intro hregions
    exact (finite_sensor_support_kernel_eq_iff_closure_eq sensors left right
      atlas targetDefect root).mpr
      ((support_truth_region_eq_iff_closure_eq sensors left right
        atlas targetDefect root).mp hregions)

/-- Every failed consequence has the canonical separating closed support `cl(premise)`. -/
theorem closure_nonmembership_has_canonical_closed_separator
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (premise : Finset ι) (i : ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hi : i ∉ sensorSupportClosure sensors premise atlas targetDefect root) :
    ∃ context : Finset ι,
      SensorSupportClosed sensors context atlas targetDefect root ∧
      premise ⊆ context ∧ i ∉ context := by
  exact ⟨sensorSupportClosure sensors premise atlas targetDefect root,
    sensor_support_closure_closed sensors premise atlas targetDefect root,
    sensor_support_subset_closure sensors premise atlas targetDefect root,
    hi⟩

/-- The full context family does not depend on the selected route root. -/
theorem all_closed_sensor_supports_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    allClosedSensorSupports sensors atlas targetDefect sourceRoot =
      allClosedSensorSupports sensors atlas targetDefect targetRoot := by
  classical
  apply Finset.ext
  intro context
  rw [mem_all_closed_sensor_supports_iff,
    mem_all_closed_sensor_supports_iff]
  unfold SensorSupportClosed
  rw [sensor_support_closure_root_independent sensors context atlas targetDefect
    sourceRoot targetRoot]

/-- Full support truth regions are root independent. -/
theorem full_support_truth_region_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (premise : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    supportTruthRegion (allClosedSensorSupports sensors atlas targetDefect sourceRoot) premise =
      supportTruthRegion (allClosedSensorSupports sensors atlas targetDefect targetRoot) premise := by
  rw [all_closed_sensor_supports_root_independent sensors atlas targetDefect
    sourceRoot targetRoot]

/-- Full single-sensor truth regions are root independent. -/
theorem full_sensor_truth_region_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (i : ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    sensorTruthRegion (allClosedSensorSupports sensors atlas targetDefect sourceRoot) i =
      sensorTruthRegion (allClosedSensorSupports sensors atlas targetDefect targetRoot) i := by
  rw [all_closed_sensor_supports_root_independent sensors atlas targetDefect
    sourceRoot targetRoot]

/-- Finite formal authority boundary of the v0.90 certificate. -/
structure FullClosedSupportRepresentationCertificate where
  sourceMemoryOSV089Bound : Bool
  selectedClosedContextSoundnessExact : Bool
  fullContextSingleSensorCompletenessExact : Bool
  fullContextFiniteSupportCompletenessExact : Bool
  closureTruthRegionInvariantExact : Bool
  kernelTruthRegionClassificationExact : Bool
  canonicalClosedSeparatorExact : Bool
  rootIndependenceExact : Bool
  reducedContextCompletenessClaimed : Bool
  universalConceptLatticeClaimed : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSFullClosedSupportRepresentationV0_90
