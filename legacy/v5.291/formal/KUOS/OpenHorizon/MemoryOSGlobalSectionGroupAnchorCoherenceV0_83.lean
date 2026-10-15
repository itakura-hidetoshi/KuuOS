import Mathlib
import KUOS.OpenHorizon.MemoryOSGlobalWordCechDescentV0_82

namespace KUOS.OpenHorizon.MemoryOSGlobalSectionGroupAnchorCoherenceV0_83

open KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
open KUOS.OpenHorizon.MemoryOSRootedRouteAtlasNielsenChangeV0_78
open KUOS.OpenHorizon.MemoryOSAllRootChartDefectAwareWordTransportV0_80
open KUOS.OpenHorizon.MemoryOSNormalizedRootWordGroupoidDescentV0_81
open KUOS.OpenHorizon.MemoryOSGlobalWordCechDescentV0_82

/-- Compatible four-root word families form a subgroup of the pointwise word group. -/
def globalNormalizedWordSectionSubgroup :
    Subgroup (RouteLabel → NormalizedWord) where
  carrier family := ∀ sourceRoot targetRoot,
    normalizedTransitionHom sourceRoot targetRoot (family targetRoot) =
      family sourceRoot
  one_mem := by
    intro sourceRoot targetRoot
    change normalizedTransitionHom sourceRoot targetRoot 1 = 1
    simp
  mul_mem := by
    intro left hleft right hright sourceRoot targetRoot
    change normalizedTransitionHom sourceRoot targetRoot
        (left targetRoot * right targetRoot) =
      left sourceRoot * right sourceRoot
    rw [map_mul, hleft sourceRoot targetRoot, hright sourceRoot targetRoot]
  inv_mem := by
    intro family hfamily sourceRoot targetRoot
    change normalizedTransitionHom sourceRoot targetRoot
        (family targetRoot)⁻¹ = (family sourceRoot)⁻¹
    rw [map_inv, hfamily sourceRoot targetRoot]

/-- The exact group of compatible normalized global word sections. -/
abbrev GlobalNormalizedWordSection := globalNormalizedWordSectionSubgroup

/-- Evaluate a compatible section in one selected anchor fiber. -/
def anchorEvaluationHom (anchorRoot : RouteLabel) :
    GlobalNormalizedWordSection →* NormalizedWord where
  toFun section := section.1 anchorRoot
  map_one' := rfl
  map_mul' _ _ := rfl

/-- Extend one anchor-fiber word to the unique compatible global section. -/
def anchorExtensionHom (anchorRoot : RouteLabel) :
    NormalizedWord →* GlobalNormalizedWordSection where
  toFun word :=
    ⟨fun root => normalizedTransitionHom root anchorRoot word, by
      intro sourceRoot targetRoot
      exact normalized_transition_word_comp sourceRoot targetRoot anchorRoot word⟩
  map_one' := by
    apply Subtype.ext
    funext root
    simp
  map_mul' left right := by
    apply Subtype.ext
    funext root
    simp

/-- Anchor evaluation after extension returns the original word. -/
@[simp] theorem anchor_evaluation_extension
    (anchorRoot : RouteLabel) (word : NormalizedWord) :
    anchorEvaluationHom anchorRoot (anchorExtensionHom anchorRoot word) = word := by
  change normalizedTransitionHom anchorRoot anchorRoot word = word
  exact DFunLike.congr_fun (normalized_transition_hom_identity anchorRoot) word

/-- Extension of the anchor component reconstructs the complete section. -/
@[simp] theorem anchor_extension_evaluation
    (anchorRoot : RouteLabel) (section : GlobalNormalizedWordSection) :
    anchorExtensionHom anchorRoot (anchorEvaluationHom anchorRoot section) =
      section := by
  apply Subtype.ext
  funext root
  exact section.property root anchorRoot

/-- The global section group is multiplicatively equivalent to every anchor fiber. -/
def globalSectionAnchorMulEquiv (anchorRoot : RouteLabel) :
    GlobalNormalizedWordSection ≃* NormalizedWord where
  toFun := anchorEvaluationHom anchorRoot
  invFun := anchorExtensionHom anchorRoot
  left_inv := anchor_extension_evaluation anchorRoot
  right_inv := anchor_evaluation_extension anchorRoot
  map_mul' _ _ := rfl

/-- Pair-groupoid transport is a multiplicative equivalence between any two fibers. -/
def normalizedFiberTransportMulEquiv
    (sourceRoot targetRoot : RouteLabel) : NormalizedWord ≃* NormalizedWord where
  toFun := normalizedTransitionHom sourceRoot targetRoot
  invFun := normalizedTransitionHom targetRoot sourceRoot
  left_inv word := normalized_transition_word_round_trip targetRoot sourceRoot word
  right_inv word := normalized_transition_word_round_trip sourceRoot targetRoot word
  map_mul' left right := by simp

/-- Fiber equivalences compose with the exact pair-groupoid law. -/
theorem normalized_fiber_transport_comp
    (sourceRoot middleRoot targetRoot : RouteLabel) (word : NormalizedWord) :
    normalizedFiberTransportMulEquiv sourceRoot middleRoot
        (normalizedFiberTransportMulEquiv middleRoot targetRoot word) =
      normalizedFiberTransportMulEquiv sourceRoot targetRoot word := by
  exact normalized_transition_word_comp sourceRoot middleRoot targetRoot word

/-- Anchor evaluations of one section are related by the exact fiber equivalence. -/
theorem anchor_evaluation_transport_natural
    (section : GlobalNormalizedWordSection)
    (sourceRoot targetRoot : RouteLabel) :
    normalizedFiberTransportMulEquiv sourceRoot targetRoot
        (anchorEvaluationHom targetRoot section) =
      anchorEvaluationHom sourceRoot section := by
  exact section.property sourceRoot targetRoot

/-- Extending after an anchor change gives the same global section. -/
theorem anchor_extension_change_coherent
    (sourceRoot targetRoot : RouteLabel) (word : NormalizedWord) :
    anchorExtensionHom sourceRoot
        (normalizedFiberTransportMulEquiv sourceRoot targetRoot word) =
      anchorExtensionHom targetRoot word := by
  apply Subtype.ext
  funext root
  exact normalized_transition_word_comp root sourceRoot targetRoot word

/-- Exact group-valued evaluation homomorphism of global sections at one root. -/
def globalSectionEvaluationHom
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : GlobalNormalizedWordSection →* G :=
  (evalNormalizedRootWord (atlasRootChart atlas targetDefect root) root).comp
    (anchorEvaluationHom root)

/-- The global evaluation homomorphism itself is independent of the root chart. -/
theorem global_section_evaluation_hom_root_independent
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    globalSectionEvaluationHom atlas targetDefect sourceRoot =
      globalSectionEvaluationHom atlas targetDefect targetRoot := by
  apply MonoidHom.ext
  intro section
  change evalNormalizedRootWord
      (atlasRootChart atlas targetDefect sourceRoot) sourceRoot
        (section.1 sourceRoot) =
    evalNormalizedRootWord
      (atlasRootChart atlas targetDefect targetRoot) targetRoot
        (section.1 targetRoot)
  rw [← section.property sourceRoot targetRoot]
  exact normalized_atlas_word_transport_exact atlas targetDefect
    sourceRoot targetRoot (section.1 targetRoot)

/-- Class-function Wilson value of one global section. -/
def globalSectionWilson
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (section : GlobalNormalizedWordSection) (root : RouteLabel) : R :=
  χ.toFun (globalSectionEvaluationHom atlas targetDefect root section)

/-- Global-section Wilson evaluation is root independent. -/
theorem global_section_wilson_root_independent
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (section : GlobalNormalizedWordSection)
    (sourceRoot targetRoot : RouteLabel) :
    globalSectionWilson χ atlas targetDefect section sourceRoot =
      globalSectionWilson χ atlas targetDefect section targetRoot := by
  unfold globalSectionWilson
  rw [DFunLike.congr_fun
    (global_section_evaluation_hom_root_independent atlas targetDefect
      sourceRoot targetRoot) section]

/-- The canonical mixed separator represented as one element of the section group. -/
def canonicalMixedGlobalSection : GlobalNormalizedWordSection :=
  anchorExtensionHom .route0 (normalizedRouteDefectWord .third)

/-- Ordered-AB section-group Wilson value is three at every root. -/
theorem canonical_ordered_ab_section_group_wilson
    (root : RouteLabel) :
    globalSectionWilson (identityWilsonClass S3) orderedABAtlas
      atlasTargetDefect canonicalMixedGlobalSection root = 3 := by
  simpa [globalSectionWilson, globalSectionEvaluationHom,
    canonicalMixedGlobalSection, anchorExtensionHom, anchorEvaluationHom,
    normalizedRootWordWilson] using
      canonical_ordered_ab_normalized_groupoid_mixed_wilson root

/-- Ordered-BA section-group Wilson value is zero at every root. -/
theorem canonical_ordered_ba_section_group_wilson
    (root : RouteLabel) :
    globalSectionWilson (identityWilsonClass S3) orderedBAAtlas
      atlasTargetDefect canonicalMixedGlobalSection root = 0 := by
  simpa [globalSectionWilson, globalSectionEvaluationHom,
    canonicalMixedGlobalSection, anchorExtensionHom, anchorEvaluationHom,
    normalizedRootWordWilson] using
      canonical_ordered_ba_normalized_groupoid_mixed_wilson root

/-- The section-group Wilson observable separates ordered AB and BA globally. -/
theorem canonical_section_group_wilson_separates
    (root : RouteLabel) :
    globalSectionWilson (identityWilsonClass S3) orderedABAtlas
        atlasTargetDefect canonicalMixedGlobalSection root ≠
      globalSectionWilson (identityWilsonClass S3) orderedBAAtlas
        atlasTargetDefect canonicalMixedGlobalSection root := by
  rw [canonical_ordered_ab_section_group_wilson,
    canonical_ordered_ba_section_group_wilson]
  norm_num

/-- Finite formal authority boundary of the v0.83 certificate. -/
structure GlobalSectionGroupAnchorCoherenceCertificate where
  sourceMemoryOSV082Bound : Bool
  sectionSubgroupExact : Bool
  anchorExtensionHomExact : Bool
  anchorEvaluationHomExact : Bool
  anchorFiberMulEquivalenceExact : Bool
  anchorChangeCoherenceExact : Bool
  globalEvaluationHomRootIndependent : Bool
  globalWilsonRootIndependent : Bool
  universalSectionGroupClassificationClaimed : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSGlobalSectionGroupAnchorCoherenceV0_83
