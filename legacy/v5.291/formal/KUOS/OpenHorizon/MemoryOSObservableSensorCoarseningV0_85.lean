import Mathlib
import KUOS.OpenHorizon.MemoryOSGlobalObservableKernelQuotientV0_84

namespace KUOS.OpenHorizon.MemoryOSObservableSensorCoarseningV0_85

open KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
open KUOS.OpenHorizon.MemoryOSRootedRouteAtlasNielsenChangeV0_78
open KUOS.OpenHorizon.MemoryOSAllRootChartDefectAwareWordTransportV0_80
open KUOS.OpenHorizon.MemoryOSNormalizedRootWordGroupoidDescentV0_81
open KUOS.OpenHorizon.MemoryOSGlobalWordCechDescentV0_82
open KUOS.OpenHorizon.MemoryOSGlobalSectionGroupAnchorCoherenceV0_83
open KUOS.OpenHorizon.MemoryOSGlobalObservableKernelQuotientV0_84

/-- Post-process exact global evaluation through an external group-valued sensor. -/
def sensorGlobalEvaluationHom
    {G H : Type*} [Group G] [Group H]
    (sensor : G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : GlobalNormalizedWordSection →* H :=
  sensor.comp (globalSectionEvaluationHom atlas targetDefect root)

/-- Sections invisible after the selected sensor has coarsened exact evaluation. -/
def sensorObservableKernel
    {G H : Type*} [Group G] [Group H]
    (sensor : G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Subgroup GlobalNormalizedWordSection :=
  (sensorGlobalEvaluationHom sensor atlas targetDefect root).ker

/-- Exact image subgroup seen by the selected sensor. -/
def sensorObservableRange
    {G H : Type*} [Group G] [Group H]
    (sensor : G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Subgroup H :=
  (sensorGlobalEvaluationHom sensor atlas targetDefect root).range

/-- Exact invisibility implies sensor-level invisibility. -/
theorem global_kernel_le_sensor_kernel
    {G H : Type*} [Group G] [Group H]
    (sensor : G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    globalObservableKernel atlas targetDefect root ≤
      sensorObservableKernel sensor atlas targetDefect root := by
  intro section hsection
  change sensor (globalSectionEvaluationHom atlas targetDefect root section) = 1
  have heval :=
    (mem_global_observable_kernel_iff atlas targetDefect root section).mp hsection
  simp [heval]

/-- Sensor-level evaluation remains independent of the selected root chart. -/
theorem sensor_global_evaluation_hom_root_independent
    {G H : Type*} [Group G] [Group H]
    (sensor : G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    sensorGlobalEvaluationHom sensor atlas targetDefect sourceRoot =
      sensorGlobalEvaluationHom sensor atlas targetDefect targetRoot := by
  unfold sensorGlobalEvaluationHom
  rw [global_section_evaluation_hom_root_independent atlas targetDefect
    sourceRoot targetRoot]

/-- The coarsened invisible kernel is root independent. -/
theorem sensor_observable_kernel_root_independent
    {G H : Type*} [Group G] [Group H]
    (sensor : G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    sensorObservableKernel sensor atlas targetDefect sourceRoot =
      sensorObservableKernel sensor atlas targetDefect targetRoot := by
  unfold sensorObservableKernel
  rw [sensor_global_evaluation_hom_root_independent sensor atlas targetDefect
    sourceRoot targetRoot]

/-- The sensor-visible image subgroup is root independent. -/
theorem sensor_observable_range_root_independent
    {G H : Type*} [Group G] [Group H]
    (sensor : G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    sensorObservableRange sensor atlas targetDefect sourceRoot =
      sensorObservableRange sensor atlas targetDefect targetRoot := by
  unfold sensorObservableRange
  rw [sensor_global_evaluation_hom_root_independent sensor atlas targetDefect
    sourceRoot targetRoot]

/-- A second sensor can only enlarge the invisible kernel. -/
theorem sensor_kernel_mono_under_postcomposition
    {G H I : Type*} [Group G] [Group H] [Group I]
    (sensor : G →* H) (postSensor : H →* I)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    sensorObservableKernel sensor atlas targetDefect root ≤
      sensorObservableKernel (postSensor.comp sensor) atlas targetDefect root := by
  intro section hsection
  change postSensor (sensor (globalSectionEvaluationHom atlas targetDefect root section)) = 1
  change sensor (globalSectionEvaluationHom atlas targetDefect root section) = 1 at hsection
  simp [hsection]

/-- An injective sensor loses no exact observable information. -/
theorem sensor_kernel_eq_global_kernel_of_injective
    {G H : Type*} [Group G] [Group H]
    (sensor : G →* H) (hsensor : Function.Injective sensor)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    sensorObservableKernel sensor atlas targetDefect root =
      globalObservableKernel atlas targetDefect root := by
  apply le_antisymm
  · intro section hsection
    change globalSectionEvaluationHom atlas targetDefect root section = 1
    apply hsensor
    change sensor (globalSectionEvaluationHom atlas targetDefect root section) = sensor 1
    change sensor (globalSectionEvaluationHom atlas targetDefect root section) = 1 at hsection
    simpa using hsection
  · exact global_kernel_le_sensor_kernel sensor atlas targetDefect root

/-- Quotient by the sensor-level invisible kernel. -/
abbrev SensorObservableQuotient
    {G H : Type*} [Group G] [Group H]
    (sensor : G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :=
  GlobalNormalizedWordSection ⧸ sensorObservableKernel sensor atlas targetDefect root

/-- First isomorphism theorem for a coarsened sensor. -/
noncomputable def sensorObservableFirstIso
    {G H : Type*} [Group G] [Group H]
    (sensor : G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    SensorObservableQuotient sensor atlas targetDefect root ≃*
      sensorObservableRange sensor atlas targetDefect root :=
  QuotientGroup.quotientKerEquivRange
    (sensorGlobalEvaluationHom sensor atlas targetDefect root)

/-- Exact observables map canonically to every coarser sensor quotient. -/
def observableSensorQuotientHom
    {G H : Type*} [Group G] [Group H]
    (sensor : G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    GlobalObservableQuotient atlas targetDefect root →*
      SensorObservableQuotient sensor atlas targetDefect root :=
  QuotientGroup.map
    (globalObservableKernel atlas targetDefect root)
    (sensorObservableKernel sensor atlas targetDefect root)
    (MonoidHom.id GlobalNormalizedWordSection) (by
      intro section hsection
      change section ∈ sensorObservableKernel sensor atlas targetDefect root
      exact global_kernel_le_sensor_kernel sensor atlas targetDefect root hsection)

/-- The quotient map sends each representative to the same representative class. -/
@[simp] theorem observable_sensor_quotient_hom_mk
    {G H : Type*} [Group G] [Group H]
    (sensor : G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) (section : GlobalNormalizedWordSection) :
    observableSensorQuotientHom sensor atlas targetDefect root
        (QuotientGroup.mk' (globalObservableKernel atlas targetDefect root) section) =
      QuotientGroup.mk' (sensorObservableKernel sensor atlas targetDefect root) section := by
  rfl

/-- Injective sensors induce an exact equivalence of observable quotients. -/
noncomputable def observableSensorQuotientMulEquivOfInjective
    {G H : Type*} [Group G] [Group H]
    (sensor : G →* H) (hsensor : Function.Injective sensor)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    GlobalObservableQuotient atlas targetDefect root ≃*
      SensorObservableQuotient sensor atlas targetDefect root :=
  QuotientGroup.quotientMulEquivOfEq
    (sensor_kernel_eq_global_kernel_of_injective sensor hsensor atlas targetDefect root).symm

/-- Pull a class function back along a group-valued sensor. -/
def sensorPullbackClassFunction
    {G H : Type*} [Group G] [Group H] {R : Type*}
    (sensor : G →* H) (χ : ClassFunction H R) : ClassFunction G R where
  toFun value := χ.toFun (sensor value)
  conjugationInvariant := by
    intro g h
    change χ.toFun (sensor (g⁻¹ * h * g)) = χ.toFun (sensor h)
    simp only [map_mul, map_inv]
    exact χ.conjugationInvariant (sensor g) (sensor h)

/-- Sensor-level Wilson evaluation of one global section. -/
def sensorGlobalSectionWilson
    {G H : Type*} [Group G] [Group H] {R : Type*}
    (sensor : G →* H) (χ : ClassFunction H R)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (section : GlobalNormalizedWordSection) (root : RouteLabel) : R :=
  χ.toFun (sensorGlobalEvaluationHom sensor atlas targetDefect root section)

/-- Sensor Wilson evaluation is exactly the pullback of a class function. -/
theorem sensor_global_section_wilson_eq_pullback
    {G H : Type*} [Group G] [Group H] {R : Type*}
    (sensor : G →* H) (χ : ClassFunction H R)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (section : GlobalNormalizedWordSection) (root : RouteLabel) :
    sensorGlobalSectionWilson sensor χ atlas targetDefect section root =
      globalSectionWilson (sensorPullbackClassFunction sensor χ)
        atlas targetDefect section root := by
  rfl

/-- Sensor-level Wilson evaluation is root independent. -/
theorem sensor_global_section_wilson_root_independent
    {G H : Type*} [Group G] [Group H] {R : Type*}
    (sensor : G →* H) (χ : ClassFunction H R)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (section : GlobalNormalizedWordSection)
    (sourceRoot targetRoot : RouteLabel) :
    sensorGlobalSectionWilson sensor χ atlas targetDefect section sourceRoot =
      sensorGlobalSectionWilson sensor χ atlas targetDefect section targetRoot := by
  unfold sensorGlobalSectionWilson
  rw [DFunLike.congr_fun
    (sensor_global_evaluation_hom_root_independent sensor atlas targetDefect
      sourceRoot targetRoot) section]

/-- Identity sensing preserves ordered-AB invisibility. -/
theorem canonical_ordered_ab_mem_identity_sensor_kernel
    (root : RouteLabel) :
    canonicalMixedGlobalSection ∈
      sensorObservableKernel (MonoidHom.id S3)
        orderedABAtlas atlasTargetDefect root := by
  exact global_kernel_le_sensor_kernel (MonoidHom.id S3)
    orderedABAtlas atlasTargetDefect root
      (canonical_ordered_ab_mem_global_observable_kernel root)

/-- Identity sensing preserves ordered-BA visibility. -/
theorem canonical_ordered_ba_not_mem_identity_sensor_kernel
    (root : RouteLabel) :
    canonicalMixedGlobalSection ∉
      sensorObservableKernel (MonoidHom.id S3)
        orderedBAAtlas atlasTargetDefect root := by
  rw [sensor_kernel_eq_global_kernel_of_injective
    (MonoidHom.id S3) Function.injective_id orderedBAAtlas atlasTargetDefect root]
  exact canonical_ordered_ba_not_mem_global_observable_kernel root

/-- The canonical separator survives every root under the exact identity sensor. -/
theorem canonical_identity_sensor_kernel_separates
    (root : RouteLabel) :
    canonicalMixedGlobalSection ∈
        sensorObservableKernel (MonoidHom.id S3)
          orderedABAtlas atlasTargetDefect root ∧
      canonicalMixedGlobalSection ∉
        sensorObservableKernel (MonoidHom.id S3)
          orderedBAAtlas atlasTargetDefect root :=
  ⟨canonical_ordered_ab_mem_identity_sensor_kernel root,
    canonical_ordered_ba_not_mem_identity_sensor_kernel root⟩

/-- Finite formal authority boundary of the v0.85 certificate. -/
structure ObservableSensorCoarseningCertificate where
  sourceMemoryOSV084Bound : Bool
  sensorEvaluationHomExact : Bool
  globalKernelIncludedInSensorKernelExact : Bool
  sensorKernelRootIndependentExact : Bool
  sensorRangeRootIndependentExact : Bool
  sensorCompositionKernelMonotoneExact : Bool
  quotientFunctorialMapExact : Bool
  injectiveSensorQuotientEquivalenceExact : Bool
  sensorWilsonPullbackExact : Bool
  canonicalIdentitySensorSeparatorExact : Bool
  universalSensorClassificationClaimed : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSObservableSensorCoarseningV0_85
