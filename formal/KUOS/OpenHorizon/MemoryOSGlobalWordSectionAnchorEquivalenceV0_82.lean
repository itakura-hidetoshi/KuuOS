import Mathlib
import KUOS.OpenHorizon.MemoryOSNormalizedRootWordGroupoidDescentV0_81

namespace KUOS.OpenHorizon.MemoryOSGlobalWordSectionAnchorEquivalenceV0_82

open KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
open KUOS.OpenHorizon.MemoryOSRootedRouteAtlasNielsenChangeV0_78
open KUOS.OpenHorizon.MemoryOSFreeGroupMixedWilsonWordV0_79
open KUOS.OpenHorizon.MemoryOSAllRootChartDefectAwareWordTransportV0_80
open KUOS.OpenHorizon.MemoryOSNormalizedRootWordGroupoidDescentV0_81

/-- A global section is one normalized free word at every root, compatible with all transports. -/
structure NormalizedWordSection where
  wordAt : RouteLabel → FreeGroup NormalizedRootWordGenerator
  compatible : ∀ sourceRoot targetRoot,
    normalizedTransitionHom sourceRoot targetRoot (wordAt targetRoot) =
      wordAt sourceRoot

/-- Any word in one anchor fiber extends canonically to a global section. -/
def sectionOfAnchor
    (anchor : RouteLabel)
    (word : FreeGroup NormalizedRootWordGenerator) :
    NormalizedWordSection :=
  {
    wordAt := fun root => normalizedTransitionHom root anchor word
    compatible := by
      intro sourceRoot targetRoot
      exact normalized_transition_word_comp sourceRoot targetRoot anchor word
  }

/-- The canonical section returns its original word at the anchor root. -/
@[simp] theorem section_of_anchor_at_anchor
    (anchor : RouteLabel)
    (word : FreeGroup NormalizedRootWordGenerator) :
    (sectionOfAnchor anchor word).wordAt anchor = word := by
  change normalizedTransitionHom anchor anchor word = word
  exact DFunLike.congr_fun (normalized_transition_hom_identity anchor) word

/-- Every compatible global section is reconstructed from any selected anchor fiber. -/
theorem section_reconstruct_from_anchor
    (anchor : RouteLabel)
    (section : NormalizedWordSection) :
    sectionOfAnchor anchor (section.wordAt anchor) = section := by
  apply NormalizedWordSection.ext
  funext root
  exact section.compatible root anchor

/-- Global compatible sections are equivalent to the free-word fiber at any root. -/
def normalizedWordSectionEquiv
    (anchor : RouteLabel) :
    NormalizedWordSection ≃ FreeGroup NormalizedRootWordGenerator where
  toFun section := section.wordAt anchor
  invFun word := sectionOfAnchor anchor word
  left_inv section := section_reconstruct_from_anchor anchor section
  right_inv word := section_of_anchor_at_anchor anchor word

/-- Evaluation of a global section in one atlas root chart. -/
def atlasWordSectionEvaluation
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G)
    (targetDefect : G)
    (section : NormalizedWordSection)
    (root : RouteLabel) : G :=
  evalNormalizedRootWord (atlasRootChart atlas targetDefect root)
    root (section.wordAt root)

/-- A compatible section has root-independent exact evaluation. -/
theorem atlas_word_section_evaluation_root_independent
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G)
    (targetDefect : G)
    (section : NormalizedWordSection)
    (sourceRoot targetRoot : RouteLabel) :
    atlasWordSectionEvaluation atlas targetDefect section sourceRoot =
      atlasWordSectionEvaluation atlas targetDefect section targetRoot := by
  unfold atlasWordSectionEvaluation
  rw [← section.compatible sourceRoot targetRoot]
  exact normalized_atlas_word_transport_exact atlas targetDefect
    sourceRoot targetRoot (section.wordAt targetRoot)

/-- Class-function Wilson value of a global section at one root chart. -/
def atlasWordSectionWilson
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R)
    (atlas : DualFourRouteAtlas G)
    (targetDefect : G)
    (section : NormalizedWordSection)
    (root : RouteLabel) : R :=
  normalizedRootWordWilson χ (atlasRootChart atlas targetDefect root)
    root (section.wordAt root)

/-- Wilson evaluation of a global section is independent of the chosen root. -/
theorem atlas_word_section_wilson_root_independent
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R)
    (atlas : DualFourRouteAtlas G)
    (targetDefect : G)
    (section : NormalizedWordSection)
    (sourceRoot targetRoot : RouteLabel) :
    atlasWordSectionWilson χ atlas targetDefect section sourceRoot =
      atlasWordSectionWilson χ atlas targetDefect section targetRoot := by
  unfold atlasWordSectionWilson
  rw [← section.compatible sourceRoot targetRoot]
  exact normalized_atlas_word_wilson_transport_exact χ atlas targetDefect
    sourceRoot targetRoot (section.wordAt targetRoot)

/-- The canonical mixed separator as a single global word section. -/
def canonicalMixedWordSection : NormalizedWordSection :=
  sectionOfAnchor .route0 (normalizedRouteDefectWord .third)

/-- The ordered-AB global section has Wilson trace three at every root. -/
theorem canonical_ordered_ab_global_section_wilson
    (root : RouteLabel) :
    atlasWordSectionWilson (identityWilsonClass S3)
      orderedABAtlas atlasTargetDefect canonicalMixedWordSection root = 3 := by
  simpa [atlasWordSectionWilson, canonicalMixedWordSection, sectionOfAnchor] using
    canonical_ordered_ab_normalized_groupoid_mixed_wilson root

/-- The ordered-BA global section has Wilson trace zero at every root. -/
theorem canonical_ordered_ba_global_section_wilson
    (root : RouteLabel) :
    atlasWordSectionWilson (identityWilsonClass S3)
      orderedBAAtlas atlasTargetDefect canonicalMixedWordSection root = 0 := by
  simpa [atlasWordSectionWilson, canonicalMixedWordSection, sectionOfAnchor] using
    canonical_ordered_ba_normalized_groupoid_mixed_wilson root

/-- The canonical global-section Wilson observable separates ordered AB and BA. -/
theorem canonical_global_section_wilson_separates
    (root : RouteLabel) :
    atlasWordSectionWilson (identityWilsonClass S3)
      orderedABAtlas atlasTargetDefect canonicalMixedWordSection root ≠
    atlasWordSectionWilson (identityWilsonClass S3)
      orderedBAAtlas atlasTargetDefect canonicalMixedWordSection root := by
  rw [canonical_ordered_ab_global_section_wilson,
    canonical_ordered_ba_global_section_wilson]
  norm_num

/-- Finite formal authority boundary of the v0.82 certificate. -/
structure GlobalWordSectionAnchorEquivalenceCertificate where
  sourceMemoryOSV081Bound : Bool
  globalSectionCompatibilityExact : Bool
  anchorExtensionExact : Bool
  anchorReconstructionExact : Bool
  anchorFiberEquivalenceExact : Bool
  sectionEvaluationRootIndependent : Bool
  sectionWilsonRootIndependent : Bool
  universalSheafClassificationClaimed : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSGlobalWordSectionAnchorEquivalenceV0_82
