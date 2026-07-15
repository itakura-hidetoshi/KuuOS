import Mathlib
import KUOS.OpenHorizon.MemoryOSJointSensorProductRefinementV0_86

namespace KUOS.OpenHorizon.MemoryOSFiniteSensorFamilyRefinementV0_87

open KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
open KUOS.OpenHorizon.MemoryOSRootedRouteAtlasNielsenChangeV0_78
open KUOS.OpenHorizon.MemoryOSAllRootChartDefectAwareWordTransportV0_80
open KUOS.OpenHorizon.MemoryOSNormalizedRootWordGroupoidDescentV0_81
open KUOS.OpenHorizon.MemoryOSGlobalWordCechDescentV0_82
open KUOS.OpenHorizon.MemoryOSGlobalSectionGroupAnchorCoherenceV0_83
open KUOS.OpenHorizon.MemoryOSGlobalObservableKernelQuotientV0_84
open KUOS.OpenHorizon.MemoryOSObservableSensorCoarseningV0_85
open KUOS.OpenHorizon.MemoryOSJointSensorProductRefinementV0_86

/-- Pointwise product of a finite, possibly heterogeneous, family of group-valued sensors. -/
def finiteSensorFamily
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i) : G →* ∀ i, H i where
  toFun value i := sensors i value
  map_one' := by
    funext i
    simp
  map_mul' := by
    intro x y
    funext i
    simp

@[simp] theorem finite_sensor_family_apply
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i) (value : G) (i : ι) :
    finiteSensorFamily sensors value i = sensors i value := rfl

/-- Global evaluation through a finite sensor family. -/
def finiteSensorFamilyGlobalEvaluationHom
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : GlobalNormalizedWordSection →* ∀ i, H i :=
  sensorGlobalEvaluationHom (finiteSensorFamily sensors) atlas targetDefect root

/-- Sections invisible to every member of a finite sensor family. -/
def finiteSensorFamilyObservableKernel
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Subgroup GlobalNormalizedWordSection :=
  sensorObservableKernel (finiteSensorFamily sensors) atlas targetDefect root

/-- Exact range visible to a finite sensor family. -/
def finiteSensorFamilyObservableRange
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Subgroup (∀ i, H i) :=
  sensorObservableRange (finiteSensorFamily sensors) atlas targetDefect root

/-- The family-invisible kernel is exactly the infimum of component kernels. -/
theorem finite_sensor_family_kernel_eq_iInf
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    finiteSensorFamilyObservableKernel sensors atlas targetDefect root =
      ⨅ i, sensorObservableKernel (sensors i) atlas targetDefect root := by
  ext section
  simp [finiteSensorFamilyObservableKernel, sensorObservableKernel,
    sensorGlobalEvaluationHom, finiteSensorFamily]

/-- An empty finite family sees nothing, so its invisible kernel is top. -/
theorem empty_finite_sensor_family_kernel_eq_top
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [IsEmpty ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    finiteSensorFamilyObservableKernel sensors atlas targetDefect root = ⊤ := by
  rw [finite_sensor_family_kernel_eq_iInf]
  simp

/-- A family refines each component sensor. -/
theorem finite_sensor_family_kernel_le_component
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) (i : ι) :
    finiteSensorFamilyObservableKernel sensors atlas targetDefect root ≤
      sensorObservableKernel (sensors i) atlas targetDefect root := by
  rw [finite_sensor_family_kernel_eq_iInf]
  exact iInf_le _ i

/-- Family evaluation remains independent of the selected root chart. -/
theorem finite_sensor_family_evaluation_root_independent
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    finiteSensorFamilyGlobalEvaluationHom sensors atlas targetDefect sourceRoot =
      finiteSensorFamilyGlobalEvaluationHom sensors atlas targetDefect targetRoot := by
  exact sensor_global_evaluation_hom_root_independent
    (finiteSensorFamily sensors) atlas targetDefect sourceRoot targetRoot

/-- Family-invisible kernels are root independent. -/
theorem finite_sensor_family_kernel_root_independent
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    finiteSensorFamilyObservableKernel sensors atlas targetDefect sourceRoot =
      finiteSensorFamilyObservableKernel sensors atlas targetDefect targetRoot := by
  exact sensor_observable_kernel_root_independent
    (finiteSensorFamily sensors) atlas targetDefect sourceRoot targetRoot

/-- Family-visible ranges are root independent. -/
theorem finite_sensor_family_range_root_independent
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    finiteSensorFamilyObservableRange sensors atlas targetDefect sourceRoot =
      finiteSensorFamilyObservableRange sensors atlas targetDefect targetRoot := by
  exact sensor_observable_range_root_independent
    (finiteSensorFamily sensors) atlas targetDefect sourceRoot targetRoot

/-- Projection from the product output to one component sensor. -/
def finiteSensorFamilyProjection
    {ι : Type*} {H : ι → Type*}
    [Fintype ι] [∀ i, Group (H i)] (i : ι) :
    (∀ j, H j) →* H i where
  toFun values := values i
  map_one' := rfl
  map_mul' := by intro x y; rfl

/-- The family quotient maps canonically to every component quotient. -/
def finiteSensorFamilyToComponentQuotientHom
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) (i : ι) :
    SensorObservableQuotient (finiteSensorFamily sensors) atlas targetDefect root →*
      SensorObservableQuotient (sensors i) atlas targetDefect root :=
  QuotientGroup.map
    (sensorObservableKernel (finiteSensorFamily sensors) atlas targetDefect root)
    (sensorObservableKernel (sensors i) atlas targetDefect root)
    (MonoidHom.id GlobalNormalizedWordSection) (by
      intro section hsection
      exact finite_sensor_family_kernel_le_component
        sensors atlas targetDefect root i hsection)

@[simp] theorem finite_sensor_family_to_component_quotient_mk
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) (i : ι) (section : GlobalNormalizedWordSection) :
    finiteSensorFamilyToComponentQuotientHom sensors atlas targetDefect root i
        (QuotientGroup.mk'
          (sensorObservableKernel (finiteSensorFamily sensors) atlas targetDefect root)
          section) =
      QuotientGroup.mk' (sensorObservableKernel (sensors i) atlas targetDefect root)
        section := by
  rfl

/-- First isomorphism theorem for a finite sensor family. -/
noncomputable def finiteSensorFamilyObservableFirstIso
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    SensorObservableQuotient (finiteSensorFamily sensors) atlas targetDefect root ≃*
      finiteSensorFamilyObservableRange sensors atlas targetDefect root :=
  sensorObservableFirstIso (finiteSensorFamily sensors) atlas targetDefect root

/-- Family injectivity is exact point separation by all components. -/
theorem finite_sensor_family_injective_iff
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i) :
    Function.Injective (finiteSensorFamily sensors) ↔
      ∀ x y, (∀ i, sensors i x = sensors i y) → x = y := by
  constructor
  · intro h x y hxy
    apply h
    funext i
    exact hxy i
  · intro h x y hxy
    apply h
    intro i
    exact congrFun hxy i

/-- One injective component makes the entire family injective. -/
theorem finite_sensor_family_injective_of_component
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i) (i : ι)
    (hi : Function.Injective (sensors i)) :
    Function.Injective (finiteSensorFamily sensors) := by
  intro x y hxy
  apply hi
  exact congrFun hxy i

/-- A separating finite family loses no exact observable information. -/
theorem finite_sensor_family_kernel_eq_global_kernel_of_injective
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i)
    (hfamily : Function.Injective (finiteSensorFamily sensors))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    finiteSensorFamilyObservableKernel sensors atlas targetDefect root =
      globalObservableKernel atlas targetDefect root := by
  exact sensor_kernel_eq_global_kernel_of_injective
    (finiteSensorFamily sensors) hfamily atlas targetDefect root

/-- A separating finite family gives an exact observable-quotient equivalence. -/
noncomputable def observableFiniteSensorFamilyQuotientMulEquivOfInjective
    {ι G : Type*} {H : ι → Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i)
    (hfamily : Function.Injective (finiteSensorFamily sensors))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    GlobalObservableQuotient atlas targetDefect root ≃*
      SensorObservableQuotient (finiteSensorFamily sensors)
        atlas targetDefect root :=
  observableSensorQuotientMulEquivOfInjective
    (finiteSensorFamily sensors) hfamily atlas targetDefect root

/-- Wilson observation through a family projection equals component sensing. -/
theorem finite_sensor_family_wilson_eq_component
    {ι G : Type*} {H : ι → Type*} {R : Type*}
    [Fintype ι] [Group G] [∀ i, Group (H i)]
    (sensors : ∀ i, G →* H i) (i : ι) (χ : ClassFunction (H i) R)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (section : GlobalNormalizedWordSection) (root : RouteLabel) :
    sensorGlobalSectionWilson (finiteSensorFamily sensors)
        (sensorPullbackClassFunction (finiteSensorFamilyProjection i) χ)
        atlas targetDefect section root =
      sensorGlobalSectionWilson (sensors i) χ
        atlas targetDefect section root := by
  rfl

/-- Restricting to a reindexed subfamily can only enlarge the invisible kernel. -/
theorem finite_sensor_family_kernel_le_reindexed
    {ι κ G H : Type*}
    [Fintype ι] [Fintype κ] [Group G] [Group H]
    (f : ι → κ) (sensors : κ → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    finiteSensorFamilyObservableKernel sensors atlas targetDefect root ≤
      finiteSensorFamilyObservableKernel (fun i => sensors (f i))
        atlas targetDefect root := by
  rw [finite_sensor_family_kernel_eq_iInf,
    finite_sensor_family_kernel_eq_iInf]
  exact le_iInf (fun i => iInf_le _ (f i))

/-- A surjective reindexing, including duplicate coordinates, preserves the kernel exactly. -/
theorem finite_sensor_family_kernel_eq_reindexed_of_surjective
    {ι κ G H : Type*}
    [Fintype ι] [Fintype κ] [Group G] [Group H]
    (f : ι → κ) (hf : Function.Surjective f)
    (sensors : κ → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    finiteSensorFamilyObservableKernel sensors atlas targetDefect root =
      finiteSensorFamilyObservableKernel (fun i => sensors (f i))
        atlas targetDefect root := by
  apply le_antisymm
  · exact finite_sensor_family_kernel_le_reindexed
      f sensors atlas targetDefect root
  · rw [finite_sensor_family_kernel_eq_iInf,
      finite_sensor_family_kernel_eq_iInf]
    refine le_iInf ?_
    intro k
    obtain ⟨i, rfl⟩ := hf k
    exact iInf_le _ i

/-- A family containing identity sensing preserves the canonical AB/BA separator. -/
theorem canonical_identity_component_family_kernel_separates
    {ι : Type*} [Fintype ι]
    (sensors : ι → S3 →* S3) (identityIndex : ι)
    (hidentity : sensors identityIndex = MonoidHom.id S3)
    (root : RouteLabel) :
    canonicalMixedGlobalSection ∈
        finiteSensorFamilyObservableKernel sensors
          orderedABAtlas atlasTargetDefect root ∧
      canonicalMixedGlobalSection ∉
        finiteSensorFamilyObservableKernel sensors
          orderedBAAtlas atlasTargetDefect root := by
  constructor
  · change finiteSensorFamily sensors
      (globalSectionEvaluationHom orderedABAtlas atlasTargetDefect root
        canonicalMixedGlobalSection) = 1
    have heval :=
      (mem_global_observable_kernel_iff orderedABAtlas atlasTargetDefect root
        canonicalMixedGlobalSection).mp
        (canonical_ordered_ab_mem_global_observable_kernel root)
    funext i
    simp [finiteSensorFamily, heval]
  · intro hfamily
    change finiteSensorFamily sensors
      (globalSectionEvaluationHom orderedBAAtlas atlasTargetDefect root
        canonicalMixedGlobalSection) = 1 at hfamily
    have hcomponent := congrFun hfamily identityIndex
    change sensors identityIndex
      (globalSectionEvaluationHom orderedBAAtlas atlasTargetDefect root
        canonicalMixedGlobalSection) = 1 at hcomponent
    rw [hidentity] at hcomponent
    exact canonical_ordered_ba_not_mem_global_observable_kernel root hcomponent

/-- Finite formal authority boundary of the v0.87 certificate. -/
structure FiniteSensorFamilyRefinementCertificate where
  sourceMemoryOSV086Bound : Bool
  finiteSensorFamilyProductExact : Bool
  familyKernelFiniteInfimumExact : Bool
  emptyFamilyKernelTopExact : Bool
  familyKernelRefinesComponentsExact : Bool
  familyRootIndependenceExact : Bool
  componentQuotientProjectionExact : Bool
  separatingFamilyQuotientEquivalenceExact : Bool
  componentWilsonProjectionExact : Bool
  surjectiveReindexRedundancyExact : Bool
  canonicalIdentityFamilySeparatorExact : Bool
  universalSensorFamilyClassificationClaimed : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSFiniteSensorFamilyRefinementV0_87
