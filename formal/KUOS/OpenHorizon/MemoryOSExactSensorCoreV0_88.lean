import Mathlib
import KUOS.OpenHorizon.MemoryOSFiniteSensorFamilyRefinementV0_87

namespace KUOS.OpenHorizon.MemoryOSExactSensorCoreV0_88

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

/-- Invisible kernel of a finite support selected from a homogeneous sensor family. -/
def finiteSensorSupportKernel
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Subgroup GlobalNormalizedWordSection :=
  ⨅ i, ⨅ (_ : i ∈ support),
    sensorObservableKernel (sensors i) atlas targetDefect root

/-- Membership means invisibility to every sensor retained by the support. -/
theorem mem_finite_sensor_support_kernel_iff
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) (section : GlobalNormalizedWordSection) :
    section ∈ finiteSensorSupportKernel sensors support atlas targetDefect root ↔
      ∀ i ∈ support,
        section ∈ sensorObservableKernel (sensors i) atlas targetDefect root := by
  simp [finiteSensorSupportKernel]

/-- The empty support has top invisible kernel. -/
theorem empty_finite_sensor_support_kernel_eq_top
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    finiteSensorSupportKernel sensors ∅ atlas targetDefect root = ⊤ := by
  ext section
  simp [mem_finite_sensor_support_kernel_iff]

/-- Adding sensors can only shrink the invisible kernel. -/
theorem finite_sensor_support_kernel_antitone
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) {smaller larger : Finset ι}
    (hsubset : smaller ⊆ larger)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    finiteSensorSupportKernel sensors larger atlas targetDefect root ≤
      finiteSensorSupportKernel sensors smaller atlas targetDefect root := by
  intro section hsection
  rw [mem_finite_sensor_support_kernel_iff] at hsection ⊢
  intro i hi
  exact hsection i (hsubset hi)

/-- Erasing one coordinate can only enlarge the invisible kernel. -/
theorem finite_sensor_support_kernel_le_erase
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι) (i : ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    finiteSensorSupportKernel sensors support atlas targetDefect root ≤
      finiteSensorSupportKernel sensors (support.erase i) atlas targetDefect root := by
  exact finite_sensor_support_kernel_antitone sensors (Finset.erase_subset i support)
    atlas targetDefect root

/-- A coordinate is redundant when its erasure preserves the exact kernel. -/
def SensorRedundantAt
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι) (i : ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Prop :=
  i ∈ support ∧
    finiteSensorSupportKernel sensors support atlas targetDefect root =
      finiteSensorSupportKernel sensors (support.erase i) atlas targetDefect root

/-- A support is irredundant when every one-coordinate erasure changes its kernel. -/
def SensorSupportIrredundant
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Prop :=
  ∀ i ∈ support,
    finiteSensorSupportKernel sensors support atlas targetDefect root ≠
      finiteSensorSupportKernel sensors (support.erase i) atlas targetDefect root

/-- If the remaining support already implies invisibility to the erased sensor,
then that sensor is redundant. -/
theorem erase_kernel_eq_of_dominated
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι) (i : ι)
    (hi : i ∈ support)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hdominated :
      finiteSensorSupportKernel sensors (support.erase i) atlas targetDefect root ≤
        sensorObservableKernel (sensors i) atlas targetDefect root) :
    finiteSensorSupportKernel sensors support atlas targetDefect root =
      finiteSensorSupportKernel sensors (support.erase i) atlas targetDefect root := by
  apply le_antisymm
  · exact finite_sensor_support_kernel_le_erase sensors support i atlas targetDefect root
  · intro section hsection
    rw [mem_finite_sensor_support_kernel_iff] at hsection ⊢
    intro j hj
    by_cases hji : j = i
    · subst j
      exact hdominated hsection
    · exact hsection j (Finset.mem_erase.mpr ⟨hji, hj⟩)

/-- Duplicate coordinates are exactly removable. -/
theorem erase_duplicate_sensor_kernel_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι) (i j : ι)
    (hi : i ∈ support) (hj : j ∈ support) (hij : i ≠ j)
    (hduplicate : sensors i = sensors j)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    finiteSensorSupportKernel sensors support atlas targetDefect root =
      finiteSensorSupportKernel sensors (support.erase j) atlas targetDefect root := by
  apply erase_kernel_eq_of_dominated sensors support j hj atlas targetDefect root
  intro section hsection
  rw [← hduplicate]
  rw [mem_finite_sensor_support_kernel_iff] at hsection
  exact hsection i (Finset.mem_erase.mpr ⟨hij, hi⟩)

/-- Erasure witnesses certify one-step irredundancy. -/
theorem sensor_support_irredundant_of_erase_witnesses
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hwitness : ∀ i ∈ support, ∃ section : GlobalNormalizedWordSection,
      section ∈ finiteSensorSupportKernel sensors (support.erase i)
        atlas targetDefect root ∧
      section ∉ sensorObservableKernel (sensors i) atlas targetDefect root) :
    SensorSupportIrredundant sensors support atlas targetDefect root := by
  intro i hi heq
  obtain ⟨section, herased, hnot⟩ := hwitness i hi
  have hsupport :
      section ∈ finiteSensorSupportKernel sensors support atlas targetDefect root := by
    rw [heq]
    exact herased
  rw [mem_finite_sensor_support_kernel_iff] at hsupport
  exact hnot (hsupport i hi)

/-- Exact core relation: inclusion, exact kernel preservation, and irredundancy. -/
def IsExactSensorCore
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (core support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Prop :=
  core ⊆ support ∧
    finiteSensorSupportKernel sensors core atlas targetDefect root =
      finiteSensorSupportKernel sensors support atlas targetDefect root ∧
    SensorSupportIrredundant sensors core atlas targetDefect root

/-- Exact-core equality composes through an intermediate support. -/
theorem exact_sensor_core_trans
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) {core middle support : Finset ι}
    (atlas : DualFourRouteAtlas G) (targetDefect : G) (root : RouteLabel)
    (hcore : IsExactSensorCore sensors core middle atlas targetDefect root)
    (hmiddleSubset : middle ⊆ support)
    (hmiddleKernel :
      finiteSensorSupportKernel sensors middle atlas targetDefect root =
        finiteSensorSupportKernel sensors support atlas targetDefect root) :
    IsExactSensorCore sensors core support atlas targetDefect root := by
  rcases hcore with ⟨hcoreSubset, hcoreKernel, hirredundant⟩
  exact ⟨hcoreSubset.trans hmiddleSubset, hcoreKernel.trans hmiddleKernel,
    hirredundant⟩

/-- Finite formal authority boundary of the v0.88 certificate. -/
structure ExactSensorCoreCertificate where
  sourceMemoryOSV087Bound : Bool
  finiteSupportKernelExact : Bool
  supportKernelAntitoneExact : Bool
  dominatedSensorErasureExact : Bool
  duplicateSensorErasureExact : Bool
  irredundancyWitnessExact : Bool
  canonicalCoreKernelPreservationExact : Bool
  canonicalCoreMinimumCardinalityFiniteSearchExact : Bool
  universalMinimumCoreUniquenessClaimed : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSExactSensorCoreV0_88
