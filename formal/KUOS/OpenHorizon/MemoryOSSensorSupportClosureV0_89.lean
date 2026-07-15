import Mathlib
import KUOS.OpenHorizon.MemoryOSExactSensorCoreV0_88

namespace KUOS.OpenHorizon.MemoryOSSensorSupportClosureV0_89

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

/-- Closure of a finite sensor support under exact kernel implication. -/
noncomputable def sensorSupportClosure
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset ι := by
  classical
  exact Finset.univ.filter fun i =>
    finiteSensorSupportKernel sensors support atlas targetDefect root ≤
      sensorObservableKernel (sensors i) atlas targetDefect root

/-- Closure membership is exact kernel domination. -/
theorem mem_sensor_support_closure_iff
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι) (i : ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    i ∈ sensorSupportClosure sensors support atlas targetDefect root ↔
      finiteSensorSupportKernel sensors support atlas targetDefect root ≤
        sensorObservableKernel (sensors i) atlas targetDefect root := by
  classical
  simp [sensorSupportClosure]

/-- Every support is contained in its closure. -/
theorem sensor_support_subset_closure
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    support ⊆ sensorSupportClosure sensors support atlas targetDefect root := by
  intro i hi
  rw [mem_sensor_support_closure_iff]
  intro section hsection
  rw [mem_finite_sensor_support_kernel_iff] at hsection
  exact hsection i hi

/-- Sensor-support closure is monotone. -/
theorem sensor_support_closure_mono
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) {smaller larger : Finset ι}
    (hsubset : smaller ⊆ larger)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    sensorSupportClosure sensors smaller atlas targetDefect root ⊆
      sensorSupportClosure sensors larger atlas targetDefect root := by
  intro i hi
  rw [mem_sensor_support_closure_iff] at hi ⊢
  exact (finite_sensor_support_kernel_antitone sensors hsubset
    atlas targetDefect root).trans hi

/-- Passing to the closure preserves the exact invisible kernel. -/
theorem sensor_support_closure_kernel_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    finiteSensorSupportKernel sensors
        (sensorSupportClosure sensors support atlas targetDefect root)
        atlas targetDefect root =
      finiteSensorSupportKernel sensors support atlas targetDefect root := by
  apply le_antisymm
  · exact finite_sensor_support_kernel_antitone sensors
      (sensor_support_subset_closure sensors support atlas targetDefect root)
      atlas targetDefect root
  · intro section hsection
    rw [mem_finite_sensor_support_kernel_iff]
    intro i hi
    have hle := (mem_sensor_support_closure_iff sensors support i
      atlas targetDefect root).mp hi
    exact hle hsection

/-- Sensor-support closure is idempotent. -/
theorem sensor_support_closure_idempotent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    sensorSupportClosure sensors
        (sensorSupportClosure sensors support atlas targetDefect root)
        atlas targetDefect root =
      sensorSupportClosure sensors support atlas targetDefect root := by
  classical
  apply Finset.ext
  intro i
  rw [mem_sensor_support_closure_iff, mem_sensor_support_closure_iff,
    sensor_support_closure_kernel_eq]

/-- Equal kernels are exactly equal closures. -/
theorem finite_sensor_support_kernel_eq_iff_closure_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    finiteSensorSupportKernel sensors left atlas targetDefect root =
        finiteSensorSupportKernel sensors right atlas targetDefect root ↔
      sensorSupportClosure sensors left atlas targetDefect root =
        sensorSupportClosure sensors right atlas targetDefect root := by
  constructor
  · intro hkernel
    classical
    apply Finset.ext
    intro i
    rw [mem_sensor_support_closure_iff, mem_sensor_support_closure_iff,
      hkernel]
  · intro hclosure
    calc
      finiteSensorSupportKernel sensors left atlas targetDefect root =
          finiteSensorSupportKernel sensors
            (sensorSupportClosure sensors left atlas targetDefect root)
            atlas targetDefect root :=
        (sensor_support_closure_kernel_eq sensors left atlas targetDefect root).symm
      _ = finiteSensorSupportKernel sensors
            (sensorSupportClosure sensors right atlas targetDefect root)
            atlas targetDefect root := by rw [hclosure]
      _ = finiteSensorSupportKernel sensors right atlas targetDefect root :=
        sensor_support_closure_kernel_eq sensors right atlas targetDefect root

/-- A sensor is redundant exactly when it belongs to the closure after erasure. -/
theorem sensor_redundant_iff_mem_erased_closure
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι) (i : ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    SensorRedundantAt sensors support i atlas targetDefect root ↔
      i ∈ support ∧
        i ∈ sensorSupportClosure sensors (support.erase i)
          atlas targetDefect root := by
  constructor
  · rintro ⟨hi, hkernel⟩
    refine ⟨hi, ?_⟩
    rw [mem_sensor_support_closure_iff]
    rw [← hkernel]
    intro section hsection
    rw [mem_finite_sensor_support_kernel_iff] at hsection
    exact hsection i hi
  · rintro ⟨hi, hclosure⟩
    refine ⟨hi, ?_⟩
    apply erase_kernel_eq_of_dominated sensors support i hi
      atlas targetDefect root
    exact (mem_sensor_support_closure_iff sensors (support.erase i) i
      atlas targetDefect root).mp hclosure

/-- A support is closed when it already contains every sensor implied by its kernel. -/
def SensorSupportClosed
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Prop :=
  sensorSupportClosure sensors support atlas targetDefect root = support

/-- Every closure is a closed support. -/
theorem sensor_support_closure_closed
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    SensorSupportClosed sensors
      (sensorSupportClosure sensors support atlas targetDefect root)
      atlas targetDefect root := by
  exact sensor_support_closure_idempotent sensors support atlas targetDefect root

/-- Exact cores and their source supports generate the same closed support. -/
theorem exact_sensor_core_closure_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (core support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hcore : IsExactSensorCore sensors core support atlas targetDefect root) :
    sensorSupportClosure sensors core atlas targetDefect root =
      sensorSupportClosure sensors support atlas targetDefect root := by
  exact (finite_sensor_support_kernel_eq_iff_closure_eq sensors core support
    atlas targetDefect root).mp hcore.2.1

/-- Finite support kernels remain independent of the selected root chart. -/
theorem finite_sensor_support_kernel_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    finiteSensorSupportKernel sensors support atlas targetDefect sourceRoot =
      finiteSensorSupportKernel sensors support atlas targetDefect targetRoot := by
  ext section
  rw [mem_finite_sensor_support_kernel_iff,
    mem_finite_sensor_support_kernel_iff]
  constructor
  · intro h i hi
    have hs := h i hi
    rw [sensor_observable_kernel_root_independent
      (sensors i) atlas targetDefect sourceRoot targetRoot] at hs
    exact hs
  · intro h i hi
    have ht := h i hi
    rw [← sensor_observable_kernel_root_independent
      (sensors i) atlas targetDefect sourceRoot targetRoot] at ht
    exact ht

/-- The closure itself is root independent. -/
theorem sensor_support_closure_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    sensorSupportClosure sensors support atlas targetDefect sourceRoot =
      sensorSupportClosure sensors support atlas targetDefect targetRoot := by
  classical
  apply Finset.ext
  intro i
  rw [mem_sensor_support_closure_iff, mem_sensor_support_closure_iff]
  constructor
  · intro h
    rw [← finite_sensor_support_kernel_root_independent sensors support atlas
      targetDefect sourceRoot targetRoot]
    rw [← sensor_observable_kernel_root_independent
      (sensors i) atlas targetDefect sourceRoot targetRoot]
    exact h
  · intro h
    rw [finite_sensor_support_kernel_root_independent sensors support atlas
      targetDefect sourceRoot targetRoot]
    rw [sensor_observable_kernel_root_independent
      (sensors i) atlas targetDefect sourceRoot targetRoot]
    exact h

/-- Quotients by a support and by its closure are canonically equivalent. -/
noncomputable def sensorSupportClosureQuotientMulEquiv
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    QuotientGroup.Quotient
        (finiteSensorSupportKernel sensors
          (sensorSupportClosure sensors support atlas targetDefect root)
          atlas targetDefect root) ≃*
      QuotientGroup.Quotient
        (finiteSensorSupportKernel sensors support atlas targetDefect root) := by
  rw [sensor_support_closure_kernel_eq]

/-- Finite formal authority boundary of the v0.89 certificate. -/
structure SensorSupportClosureCertificate where
  sourceMemoryOSV088Bound : Bool
  closureMembershipExact : Bool
  closureExtensiveExact : Bool
  closureMonotoneExact : Bool
  closureKernelInvariantExact : Bool
  closureIdempotentExact : Bool
  kernelClosureEquivalenceExact : Bool
  redundancyClosureCriterionExact : Bool
  exactCoreClosureEquivalenceExact : Bool
  rootIndependenceExact : Bool
  universalSensorClosureClassificationClaimed : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSSensorSupportClosureV0_89
