import Mathlib
import KUOS.OpenHorizon.MemoryOSObservableSensorCoarseningV0_85

namespace KUOS.OpenHorizon.MemoryOSJointSensorProductRefinementV0_86

open KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
open KUOS.OpenHorizon.MemoryOSRootedRouteAtlasNielsenChangeV0_78
open KUOS.OpenHorizon.MemoryOSAllRootChartDefectAwareWordTransportV0_80
open KUOS.OpenHorizon.MemoryOSNormalizedRootWordGroupoidDescentV0_81
open KUOS.OpenHorizon.MemoryOSGlobalWordCechDescentV0_82
open KUOS.OpenHorizon.MemoryOSGlobalSectionGroupAnchorCoherenceV0_83
open KUOS.OpenHorizon.MemoryOSGlobalObservableKernelQuotientV0_84
open KUOS.OpenHorizon.MemoryOSObservableSensorCoarseningV0_85

/-- Product of two group-valued sensors. -/
def jointSensor
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I) : G →* H × I where
  toFun value := (left value, right value)
  map_one' := by simp
  map_mul' := by intro x y; simp

@[simp] theorem joint_sensor_apply
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I) (value : G) :
    jointSensor left right value = (left value, right value) := rfl

/-- Product-sensor evaluation of global normalized sections. -/
def jointSensorGlobalEvaluationHom
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : GlobalNormalizedWordSection →* H × I :=
  sensorGlobalEvaluationHom (jointSensor left right) atlas targetDefect root

/-- Sections invisible to both sensor components simultaneously. -/
def jointSensorObservableKernel
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Subgroup GlobalNormalizedWordSection :=
  sensorObservableKernel (jointSensor left right) atlas targetDefect root

/-- Exact range jointly visible to the product sensor. -/
def jointSensorObservableRange
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Subgroup (H × I) :=
  sensorObservableRange (jointSensor left right) atlas targetDefect root

/-- The product-sensor invisible kernel is exactly the intersection of component kernels. -/
theorem joint_sensor_kernel_eq_inf
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    jointSensorObservableKernel left right atlas targetDefect root =
      sensorObservableKernel left atlas targetDefect root ⊓
        sensorObservableKernel right atlas targetDefect root := by
  ext section
  simp [jointSensorObservableKernel, sensorObservableKernel,
    sensorGlobalEvaluationHom, jointSensor]

/-- Membership in the joint kernel means simultaneous invisibility to both components. -/
theorem mem_joint_sensor_kernel_iff
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) (section : GlobalNormalizedWordSection) :
    section ∈ jointSensorObservableKernel left right atlas targetDefect root ↔
      section ∈ sensorObservableKernel left atlas targetDefect root ∧
        section ∈ sensorObservableKernel right atlas targetDefect root := by
  rw [joint_sensor_kernel_eq_inf]
  rfl

/-- Joint sensing refines the left component. -/
theorem joint_sensor_kernel_le_left
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    jointSensorObservableKernel left right atlas targetDefect root ≤
      sensorObservableKernel left atlas targetDefect root := by
  rw [joint_sensor_kernel_eq_inf]
  exact inf_le_left

/-- Joint sensing refines the right component. -/
theorem joint_sensor_kernel_le_right
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    jointSensorObservableKernel left right atlas targetDefect root ≤
      sensorObservableKernel right atlas targetDefect root := by
  rw [joint_sensor_kernel_eq_inf]
  exact inf_le_right

/-- Joint evaluation is independent of the selected root chart. -/
theorem joint_sensor_evaluation_root_independent
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    jointSensorGlobalEvaluationHom left right atlas targetDefect sourceRoot =
      jointSensorGlobalEvaluationHom left right atlas targetDefect targetRoot := by
  exact sensor_global_evaluation_hom_root_independent
    (jointSensor left right) atlas targetDefect sourceRoot targetRoot

/-- Joint invisible kernels are root independent. -/
theorem joint_sensor_kernel_root_independent
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    jointSensorObservableKernel left right atlas targetDefect sourceRoot =
      jointSensorObservableKernel left right atlas targetDefect targetRoot := by
  exact sensor_observable_kernel_root_independent
    (jointSensor left right) atlas targetDefect sourceRoot targetRoot

/-- Joint visible ranges are root independent. -/
theorem joint_sensor_range_root_independent
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    jointSensorObservableRange left right atlas targetDefect sourceRoot =
      jointSensorObservableRange left right atlas targetDefect targetRoot := by
  exact sensor_observable_range_root_independent
    (jointSensor left right) atlas targetDefect sourceRoot targetRoot

/-- Injectivity of the left component implies joint injectivity. -/
theorem joint_sensor_injective_of_left
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (hleft : Function.Injective left) :
    Function.Injective (jointSensor left right) := by
  intro x y hxy
  apply hleft
  exact congrArg Prod.fst hxy

/-- Injectivity of the right component implies joint injectivity. -/
theorem joint_sensor_injective_of_right
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (hright : Function.Injective right) :
    Function.Injective (jointSensor left right) := by
  intro x y hxy
  apply hright
  exact congrArg Prod.snd hxy

/-- Joint injectivity is equivalent to pairwise separation by the two sensors. -/
theorem joint_sensor_injective_iff
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I) :
    Function.Injective (jointSensor left right) ↔
      ∀ x y, left x = left y → right x = right y → x = y := by
  constructor
  · intro h x y hleft hright
    apply h
    exact Prod.ext hleft hright
  · intro h x y hxy
    exact h x y (congrArg Prod.fst hxy) (congrArg Prod.snd hxy)

/-- A jointly injective sensor pair loses no exact observable information. -/
theorem joint_sensor_kernel_eq_global_kernel_of_injective
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (hjoint : Function.Injective (jointSensor left right))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    jointSensorObservableKernel left right atlas targetDefect root =
      globalObservableKernel atlas targetDefect root := by
  exact sensor_kernel_eq_global_kernel_of_injective
    (jointSensor left right) hjoint atlas targetDefect root

/-- The joint quotient maps canonically to the left-component quotient. -/
def jointSensorToLeftQuotientHom
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    SensorObservableQuotient (jointSensor left right) atlas targetDefect root →*
      SensorObservableQuotient left atlas targetDefect root :=
  QuotientGroup.map
    (sensorObservableKernel (jointSensor left right) atlas targetDefect root)
    (sensorObservableKernel left atlas targetDefect root)
    (MonoidHom.id GlobalNormalizedWordSection) (by
      intro section hsection
      exact joint_sensor_kernel_le_left left right atlas targetDefect root hsection)

/-- The joint quotient maps canonically to the right-component quotient. -/
def jointSensorToRightQuotientHom
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    SensorObservableQuotient (jointSensor left right) atlas targetDefect root →*
      SensorObservableQuotient right atlas targetDefect root :=
  QuotientGroup.map
    (sensorObservableKernel (jointSensor left right) atlas targetDefect root)
    (sensorObservableKernel right atlas targetDefect root)
    (MonoidHom.id GlobalNormalizedWordSection) (by
      intro section hsection
      exact joint_sensor_kernel_le_right left right atlas targetDefect root hsection)

@[simp] theorem joint_sensor_to_left_quotient_mk
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) (section : GlobalNormalizedWordSection) :
    jointSensorToLeftQuotientHom left right atlas targetDefect root
        (QuotientGroup.mk'
          (sensorObservableKernel (jointSensor left right) atlas targetDefect root)
          section) =
      QuotientGroup.mk' (sensorObservableKernel left atlas targetDefect root)
        section := by
  rfl

@[simp] theorem joint_sensor_to_right_quotient_mk
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) (section : GlobalNormalizedWordSection) :
    jointSensorToRightQuotientHom left right atlas targetDefect root
        (QuotientGroup.mk'
          (sensorObservableKernel (jointSensor left right) atlas targetDefect root)
          section) =
      QuotientGroup.mk' (sensorObservableKernel right atlas targetDefect root)
        section := by
  rfl

/-- First isomorphism theorem for the joint sensor. -/
noncomputable def jointSensorObservableFirstIso
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    SensorObservableQuotient (jointSensor left right) atlas targetDefect root ≃*
      jointSensorObservableRange left right atlas targetDefect root :=
  sensorObservableFirstIso (jointSensor left right) atlas targetDefect root

/-- A jointly injective pair gives an exact equivalence with the source observable quotient. -/
noncomputable def observableJointSensorQuotientMulEquivOfInjective
    {G H I : Type*} [Group G] [Group H] [Group I]
    (left : G →* H) (right : G →* I)
    (hjoint : Function.Injective (jointSensor left right))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    GlobalObservableQuotient atlas targetDefect root ≃*
      SensorObservableQuotient (jointSensor left right) atlas targetDefect root :=
  observableSensorQuotientMulEquivOfInjective
    (jointSensor left right) hjoint atlas targetDefect root

/-- Wilson observation through the left projection of a joint sensor equals left sensing. -/
theorem joint_sensor_left_wilson_eq_component
    {G H I : Type*} [Group G] [Group H] [Group I] {R : Type*}
    (left : G →* H) (right : G →* I) (χ : ClassFunction H R)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (section : GlobalNormalizedWordSection) (root : RouteLabel) :
    sensorGlobalSectionWilson (jointSensor left right)
        (sensorPullbackClassFunction
          ({ toFun := Prod.fst, map_one' := rfl, map_mul' := by intro x y; rfl } :
            H × I →* H) χ)
        atlas targetDefect section root =
      sensorGlobalSectionWilson left χ atlas targetDefect section root := by
  rfl

/-- Wilson observation through the right projection of a joint sensor equals right sensing. -/
theorem joint_sensor_right_wilson_eq_component
    {G H I : Type*} [Group G] [Group H] [Group I] {R : Type*}
    (left : G →* H) (right : G →* I) (χ : ClassFunction I R)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (section : GlobalNormalizedWordSection) (root : RouteLabel) :
    sensorGlobalSectionWilson (jointSensor left right)
        (sensorPullbackClassFunction
          ({ toFun := Prod.snd, map_one' := rfl, map_mul' := by intro x y; rfl } :
            H × I →* I) χ)
        atlas targetDefect section root =
      sensorGlobalSectionWilson right χ atlas targetDefect section root := by
  rfl

/-- Identity paired with any sensor preserves the canonical ordered-AB/BA separator. -/
theorem canonical_identity_joint_sensor_kernel_separates
    {H : Type*} [Group H] (sensor : S3 →* H) (root : RouteLabel) :
    canonicalMixedGlobalSection ∈
        sensorObservableKernel (jointSensor (MonoidHom.id S3) sensor)
          orderedABAtlas atlasTargetDefect root ∧
      canonicalMixedGlobalSection ∉
        sensorObservableKernel (jointSensor (MonoidHom.id S3) sensor)
          orderedBAAtlas atlasTargetDefect root := by
  have hinjective : Function.Injective (jointSensor (MonoidHom.id S3) sensor) :=
    joint_sensor_injective_of_left (MonoidHom.id S3) sensor Function.injective_id
  constructor
  · rw [sensor_kernel_eq_global_kernel_of_injective
      (jointSensor (MonoidHom.id S3) sensor) hinjective
      orderedABAtlas atlasTargetDefect root]
    exact canonical_ordered_ab_mem_global_observable_kernel root
  · rw [sensor_kernel_eq_global_kernel_of_injective
      (jointSensor (MonoidHom.id S3) sensor) hinjective
      orderedBAAtlas atlasTargetDefect root]
    exact canonical_ordered_ba_not_mem_global_observable_kernel root

/-- Finite formal authority boundary of the v0.86 certificate. -/
structure JointSensorProductRefinementCertificate where
  sourceMemoryOSV085Bound : Bool
  jointSensorProductExact : Bool
  jointKernelIntersectionExact : Bool
  jointKernelRefinesComponentsExact : Bool
  jointRootIndependenceExact : Bool
  componentQuotientProjectionExact : Bool
  jointlyInjectiveQuotientEquivalenceExact : Bool
  componentWilsonProjectionExact : Bool
  canonicalIdentityJointSeparatorExact : Bool
  universalSensorFamilyClassificationClaimed : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSJointSensorProductRefinementV0_86
