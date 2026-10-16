import Mathlib
import KUOS.OpenHorizon.MemoryOSGlobalSectionGroupAnchorCoherenceV0_83

namespace KUOS.OpenHorizon.MemoryOSGlobalObservableKernelQuotientV0_84

open KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
open KUOS.OpenHorizon.MemoryOSRootedRouteAtlasNielsenChangeV0_78
open KUOS.OpenHorizon.MemoryOSAllRootChartDefectAwareWordTransportV0_80
open KUOS.OpenHorizon.MemoryOSNormalizedRootWordGroupoidDescentV0_81
open KUOS.OpenHorizon.MemoryOSGlobalWordCechDescentV0_82
open KUOS.OpenHorizon.MemoryOSGlobalSectionGroupAnchorCoherenceV0_83

/-- Sections invisible to exact group evaluation at one root. -/
def globalObservableKernel
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Subgroup GlobalNormalizedWordSection :=
  (globalSectionEvaluationHom atlas targetDefect root).ker

/-- Exact image subgroup of the global section evaluation. -/
def globalObservableRange
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Subgroup G :=
  (globalSectionEvaluationHom atlas targetDefect root).range

/-- The invisible kernel is independent of the selected root chart. -/
theorem global_observable_kernel_root_independent
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    globalObservableKernel atlas targetDefect sourceRoot =
      globalObservableKernel atlas targetDefect targetRoot := by
  unfold globalObservableKernel
  rw [global_section_evaluation_hom_root_independent atlas targetDefect
    sourceRoot targetRoot]

/-- The exact observable image subgroup is independent of the selected root chart. -/
theorem global_observable_range_root_independent
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    globalObservableRange atlas targetDefect sourceRoot =
      globalObservableRange atlas targetDefect targetRoot := by
  unfold globalObservableRange
  rw [global_section_evaluation_hom_root_independent atlas targetDefect
    sourceRoot targetRoot]

/-- Quotient of global sections by the exact observationally invisible kernel. -/
abbrev GlobalObservableQuotient
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :=
  GlobalNormalizedWordSection ⧸ globalObservableKernel atlas targetDefect root

/-- First isomorphism theorem: observable quotient equals the exact evaluation range. -/
noncomputable def globalObservableFirstIso
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    GlobalObservableQuotient atlas targetDefect root ≃*
      globalObservableRange atlas targetDefect root :=
  QuotientGroup.quotientKerEquivRange
    (globalSectionEvaluationHom atlas targetDefect root)

/-- On representatives, the quotient-range equivalence is exactly global evaluation. -/
@[simp] theorem global_observable_first_iso_mk_coe
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) (section : GlobalNormalizedWordSection) :
    ((globalObservableFirstIso atlas targetDefect root
        (QuotientGroup.mk' (globalObservableKernel atlas targetDefect root)
          section) : globalObservableRange atlas targetDefect root) : G) =
      globalSectionEvaluationHom atlas targetDefect root section := by
  rfl

/-- Kernel membership is exactly evaluation to the identity observable. -/
theorem mem_global_observable_kernel_iff
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) (section : GlobalNormalizedWordSection) :
    section ∈ globalObservableKernel atlas targetDefect root ↔
      globalSectionEvaluationHom atlas targetDefect root section = 1 := by
  rfl

/-- Two sections have the same observable exactly when their ratio is invisible. -/
theorem section_ratio_mem_kernel_iff_same_evaluation
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (left right : GlobalNormalizedWordSection) :
    left⁻¹ * right ∈ globalObservableKernel atlas targetDefect root ↔
      globalSectionEvaluationHom atlas targetDefect root left =
        globalSectionEvaluationHom atlas targetDefect root right := by
  change
    globalSectionEvaluationHom atlas targetDefect root (left⁻¹ * right) = 1 ↔
      globalSectionEvaluationHom atlas targetDefect root left =
        globalSectionEvaluationHom atlas targetDefect root right
  rw [map_mul, map_inv]
  constructor
  · intro h
    have h' := congrArg
      (fun value => globalSectionEvaluationHom atlas targetDefect root left * value) h
    have : globalSectionEvaluationHom atlas targetDefect root right =
        globalSectionEvaluationHom atlas targetDefect root left := by
      simpa [mul_assoc] using h'
    exact this.symm
  · intro h
    rw [h, inv_mul]

/-- Class-function observable on the quotient, transported through the exact range. -/
def globalObservableQuotientWilson
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (observable : GlobalObservableQuotient atlas targetDefect root) : R :=
  χ.toFun ((globalObservableFirstIso atlas targetDefect root observable :
    globalObservableRange atlas targetDefect root) : G)

/-- Quotient Wilson evaluation on a representative equals the section Wilson value. -/
@[simp] theorem global_observable_quotient_wilson_mk
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) (section : GlobalNormalizedWordSection) :
    globalObservableQuotientWilson χ atlas targetDefect root
        (QuotientGroup.mk' (globalObservableKernel atlas targetDefect root)
          section) =
      globalSectionWilson χ atlas targetDefect section root := by
  rfl

/-- The ordered-AB canonical section is invisible to exact group evaluation. -/
theorem canonical_ordered_ab_mem_global_observable_kernel
    (root : RouteLabel) :
    canonicalMixedGlobalSection ∈
      globalObservableKernel orderedABAtlas atlasTargetDefect root := by
  rw [mem_global_observable_kernel_iff]
  rw [global_section_evaluation_hom_root_independent orderedABAtlas
    atlasTargetDefect root .route0]
  native_decide

/-- The ordered-BA canonical section remains visible after quotienting by the kernel. -/
theorem canonical_ordered_ba_not_mem_global_observable_kernel
    (root : RouteLabel) :
    canonicalMixedGlobalSection ∉
      globalObservableKernel orderedBAAtlas atlasTargetDefect root := by
  intro h
  have heval :
      globalSectionEvaluationHom orderedBAAtlas atlasTargetDefect root
        canonicalMixedGlobalSection = 1 :=
    (mem_global_observable_kernel_iff orderedBAAtlas atlasTargetDefect root
      canonicalMixedGlobalSection).mp h
  have hw := canonical_ordered_ba_section_group_wilson root
  unfold globalSectionWilson at hw
  rw [heval] at hw
  native_decide at hw

/-- Kernel visibility separates the mirrored canonical profiles at every root. -/
theorem canonical_global_observable_kernel_separates
    (root : RouteLabel) :
    canonicalMixedGlobalSection ∈
        globalObservableKernel orderedABAtlas atlasTargetDefect root ∧
      canonicalMixedGlobalSection ∉
        globalObservableKernel orderedBAAtlas atlasTargetDefect root :=
  ⟨canonical_ordered_ab_mem_global_observable_kernel root,
    canonical_ordered_ba_not_mem_global_observable_kernel root⟩

/-- Finite formal authority boundary of the v0.84 certificate. -/
structure GlobalObservableKernelQuotientCertificate where
  sourceMemoryOSV083Bound : Bool
  evaluationKernelNormalExact : Bool
  evaluationKernelRootIndependentExact : Bool
  evaluationRangeRootIndependentExact : Bool
  quotientRangeFirstIsomorphismExact : Bool
  observationalEquivalenceExact : Bool
  quotientWilsonFactorizationExact : Bool
  canonicalKernelVisibilitySeparatorExact : Bool
  universalObservableModuliClassificationClaimed : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSGlobalObservableKernelQuotientV0_84
