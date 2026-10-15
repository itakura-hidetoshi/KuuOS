import Mathlib
import KUOS.OpenHorizon.MemoryOSNormalizedRootWordGroupoidDescentV0_81

namespace KUOS.OpenHorizon.MemoryOSGlobalWordCechDescentV0_82

open KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
open KUOS.OpenHorizon.MemoryOSRootedRouteAtlasNielsenChangeV0_78
open KUOS.OpenHorizon.MemoryOSFreeGroupMixedWilsonWordV0_79
open KUOS.OpenHorizon.MemoryOSAllRootChartDefectAwareWordTransportV0_80
open KUOS.OpenHorizon.MemoryOSNormalizedRootWordGroupoidDescentV0_81

/-- The normalized free word carried by one root chart. -/
abbrev NormalizedWord := FreeGroup NormalizedRootWordGenerator

/-- A local word at each of the four route roots. -/
structure LocalNormalizedWordFamily where
  word : RouteLabel → NormalizedWord

/-- Exact pairwise descent compatibility of a local word family. -/
def LocalNormalizedWordFamily.DescentCompatible
    (family : LocalNormalizedWordFamily) : Prop :=
  ∀ sourceRoot targetRoot,
    normalizedTransitionHom sourceRoot targetRoot (family.word targetRoot) =
      family.word sourceRoot

/-- Non-Abelian Čech mismatch of a local family on one ordered root overlap. -/
def descentMismatch
    (family : LocalNormalizedWordFamily)
    (sourceRoot targetRoot : RouteLabel) : NormalizedWord :=
  (family.word sourceRoot)⁻¹ *
    normalizedTransitionHom sourceRoot targetRoot (family.word targetRoot)

/-- Every self-overlap mismatch is identity, even for an incompatible family. -/
theorem descent_mismatch_self
    (family : LocalNormalizedWordFamily) (root : RouteLabel) :
    descentMismatch family root root = 1 := by
  unfold descentMismatch
  rw [DFunLike.congr_fun (normalized_transition_hom_identity root)
    (family.word root)]
  simp

/-- Compatibility is exactly the vanishing of all ordered overlap mismatches. -/
theorem descent_compatible_iff_mismatch_identity
    (family : LocalNormalizedWordFamily) :
    family.DescentCompatible ↔
      ∀ sourceRoot targetRoot,
        descentMismatch family sourceRoot targetRoot = 1 := by
  constructor
  · intro h sourceRoot targetRoot
    unfold descentMismatch
    rw [h sourceRoot targetRoot]
    simp
  · intro h sourceRoot targetRoot
    have hm := h sourceRoot targetRoot
    unfold descentMismatch at hm
    have hp := congrArg (fun value => family.word sourceRoot * value) hm
    simpa [mul_assoc] using hp

/-- Ordered mismatches satisfy the exact non-Abelian Čech cocycle law. -/
theorem descent_mismatch_cocycle
    (family : LocalNormalizedWordFamily)
    (sourceRoot middleRoot targetRoot : RouteLabel) :
    descentMismatch family sourceRoot middleRoot *
        normalizedTransitionHom sourceRoot middleRoot
          (descentMismatch family middleRoot targetRoot) =
      descentMismatch family sourceRoot targetRoot := by
  unfold descentMismatch
  rw [map_mul, map_inv, normalized_transition_word_comp]
  group

/-- Reverse overlap mismatch is the transported inverse of the forward mismatch. -/
theorem descent_mismatch_inverse
    (family : LocalNormalizedWordFamily)
    (sourceRoot targetRoot : RouteLabel) :
    descentMismatch family sourceRoot targetRoot *
        normalizedTransitionHom sourceRoot targetRoot
          (descentMismatch family targetRoot sourceRoot) = 1 := by
  calc
    descentMismatch family sourceRoot targetRoot *
        normalizedTransitionHom sourceRoot targetRoot
          (descentMismatch family targetRoot sourceRoot) =
        descentMismatch family sourceRoot sourceRoot :=
      descent_mismatch_cocycle family sourceRoot targetRoot sourceRoot
    _ = 1 := descent_mismatch_self family sourceRoot

/-- Reconstruct the complete local family from one anchor-root word. -/
def reconstructedLocalWordFamily
    (anchorRoot : RouteLabel) (anchorWord : NormalizedWord) :
    LocalNormalizedWordFamily :=
  { word := fun root => normalizedTransitionHom root anchorRoot anchorWord }

/-- Reconstruction from one anchor always produces a compatible family. -/
theorem reconstructed_local_word_family_compatible
    (anchorRoot : RouteLabel) (anchorWord : NormalizedWord) :
    (reconstructedLocalWordFamily anchorRoot anchorWord).DescentCompatible := by
  intro sourceRoot targetRoot
  exact normalized_transition_word_comp sourceRoot targetRoot anchorRoot anchorWord

/-- The reconstructed component at the anchor is the original word. -/
theorem reconstructed_local_word_family_anchor
    (anchorRoot : RouteLabel) (anchorWord : NormalizedWord) :
    (reconstructedLocalWordFamily anchorRoot anchorWord).word anchorRoot =
      anchorWord := by
  exact DFunLike.congr_fun (normalized_transition_hom_identity anchorRoot)
    anchorWord

/-- Every compatible family is uniquely reconstructed from any one component. -/
theorem compatible_family_reconstructed_from_any_root
    (family : LocalNormalizedWordFamily)
    (h : family.DescentCompatible) (anchorRoot : RouteLabel) :
    reconstructedLocalWordFamily anchorRoot (family.word anchorRoot) = family := by
  apply LocalNormalizedWordFamily.ext
  funext root
  exact h root anchorRoot

/-- A genuine global descent section is a compatible local family. -/
structure NormalizedWordDescentSection where
  local : LocalNormalizedWordFamily
  compatible : local.DescentCompatible

/-- Canonical descent section generated by an arbitrary anchor word. -/
def descentSectionFrom
    (anchorRoot : RouteLabel) (anchorWord : NormalizedWord) :
    NormalizedWordDescentSection :=
  { local := reconstructedLocalWordFamily anchorRoot anchorWord
    compatible := reconstructed_local_word_family_compatible anchorRoot anchorWord }

/-- Evaluation of a descent section in one atlas root chart. -/
def evalDescentSectionAt
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (section : NormalizedWordDescentSection) (root : RouteLabel) : G :=
  evalNormalizedRootWord (atlasRootChart atlas targetDefect root) root
    (section.local.word root)

/-- A compatible section has one root-independent exact group value. -/
theorem descent_section_evaluation_root_independent
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (section : NormalizedWordDescentSection)
    (sourceRoot targetRoot : RouteLabel) :
    evalDescentSectionAt atlas targetDefect section sourceRoot =
      evalDescentSectionAt atlas targetDefect section targetRoot := by
  unfold evalDescentSectionAt
  rw [← section.compatible sourceRoot targetRoot]
  exact normalized_atlas_word_transport_exact atlas targetDefect sourceRoot
    targetRoot (section.local.word targetRoot)

/-- Class-function Wilson evaluation of a global descent section. -/
def descentSectionWilsonAt
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (section : NormalizedWordDescentSection) (root : RouteLabel) : R :=
  χ.toFun (evalDescentSectionAt atlas targetDefect section root)

/-- Wilson evaluation descends to the global section and is root independent. -/
theorem descent_section_wilson_root_independent
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (section : NormalizedWordDescentSection)
    (sourceRoot targetRoot : RouteLabel) :
    descentSectionWilsonAt χ atlas targetDefect section sourceRoot =
      descentSectionWilsonAt χ atlas targetDefect section targetRoot := by
  unfold descentSectionWilsonAt
  rw [descent_section_evaluation_root_independent atlas targetDefect section
    sourceRoot targetRoot]

/-- Replace one local chart word by a right-multiplied perturbation. -/
def tamperLocalWordFamily
    (family : LocalNormalizedWordFamily) (tamperedRoot : RouteLabel)
    (delta : NormalizedWord) : LocalNormalizedWordFamily :=
  { word := fun root =>
      if root = tamperedRoot then family.word root * delta else family.word root }

/-- A one-chart perturbation leaves every overlap away from that chart flat. -/
theorem tampered_mismatch_away_from_root
    (family : LocalNormalizedWordFamily)
    (h : family.DescentCompatible)
    (tamperedRoot sourceRoot targetRoot : RouteLabel)
    (delta : NormalizedWord)
    (hs : sourceRoot ≠ tamperedRoot) (ht : targetRoot ≠ tamperedRoot) :
    descentMismatch (tamperLocalWordFamily family tamperedRoot delta)
      sourceRoot targetRoot = 1 := by
  unfold descentMismatch tamperLocalWordFamily
  simp only [if_neg hs, if_neg ht]
  rw [h sourceRoot targetRoot]
  simp

/-- Incoming mismatch to the perturbed chart is exactly the transported perturbation. -/
theorem tampered_mismatch_into_root
    (family : LocalNormalizedWordFamily)
    (h : family.DescentCompatible)
    (tamperedRoot sourceRoot : RouteLabel)
    (delta : NormalizedWord)
    (hs : sourceRoot ≠ tamperedRoot) :
    descentMismatch (tamperLocalWordFamily family tamperedRoot delta)
      sourceRoot tamperedRoot =
        normalizedTransitionHom sourceRoot tamperedRoot delta := by
  unfold descentMismatch tamperLocalWordFamily
  simp only [if_neg hs, if_pos, map_mul]
  rw [h sourceRoot tamperedRoot]
  group

/-- Outgoing mismatch from the perturbed chart is the inverse perturbation. -/
theorem tampered_mismatch_out_of_root
    (family : LocalNormalizedWordFamily)
    (h : family.DescentCompatible)
    (tamperedRoot targetRoot : RouteLabel)
    (delta : NormalizedWord)
    (ht : targetRoot ≠ tamperedRoot) :
    descentMismatch (tamperLocalWordFamily family tamperedRoot delta)
      tamperedRoot targetRoot = delta⁻¹ := by
  unfold descentMismatch tamperLocalWordFamily
  simp only [if_pos, if_neg ht]
  rw [h tamperedRoot targetRoot]
  group

/-- The v0.81 mixed separator promoted to one global descent section. -/
def canonicalMixedDescentSection : NormalizedWordDescentSection :=
  descentSectionFrom .route0 (normalizedRouteDefectWord .third)

/-- Ordered-AB global-section Wilson value is 3 in every root chart. -/
theorem canonical_ordered_ab_global_section_wilson
    (root : RouteLabel) :
    descentSectionWilsonAt (identityWilsonClass S3) orderedABAtlas
      atlasTargetDefect canonicalMixedDescentSection root = 3 := by
  simpa [descentSectionWilsonAt, evalDescentSectionAt,
    canonicalMixedDescentSection, descentSectionFrom,
    reconstructedLocalWordFamily] using
      canonical_ordered_ab_normalized_groupoid_mixed_wilson root

/-- Ordered-BA global-section Wilson value is 0 in every root chart. -/
theorem canonical_ordered_ba_global_section_wilson
    (root : RouteLabel) :
    descentSectionWilsonAt (identityWilsonClass S3) orderedBAAtlas
      atlasTargetDefect canonicalMixedDescentSection root = 0 := by
  simpa [descentSectionWilsonAt, evalDescentSectionAt,
    canonicalMixedDescentSection, descentSectionFrom,
    reconstructedLocalWordFamily] using
      canonical_ordered_ba_normalized_groupoid_mixed_wilson root

/-- The global descent section separates the mirrored profiles in every chart. -/
theorem canonical_global_section_wilson_separates
    (root : RouteLabel) :
    descentSectionWilsonAt (identityWilsonClass S3) orderedABAtlas
        atlasTargetDefect canonicalMixedDescentSection root ≠
      descentSectionWilsonAt (identityWilsonClass S3) orderedBAAtlas
        atlasTargetDefect canonicalMixedDescentSection root := by
  rw [canonical_ordered_ab_global_section_wilson,
    canonical_ordered_ba_global_section_wilson]
  norm_num

/-- Finite formal authority boundary of the v0.82 certificate. -/
structure GlobalWordCechDescentCertificate where
  sourceMemoryOSV081Bound : Bool
  mismatchIdentityExact : Bool
  mismatchCocycleExact : Bool
  mismatchInverseExact : Bool
  compatibleFamilyReconstructionExact : Bool
  globalEvaluationDescentExact : Bool
  globalWilsonDescentExact : Bool
  singleChartTamperLocalizationExact : Bool
  universalSheafDescentClaimed : Bool
  continuumStackClaimed : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSGlobalWordCechDescentV0_82
