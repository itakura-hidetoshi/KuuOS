import Mathlib
import KUOS.OpenHorizon.MemoryOSProvenanceDAGRevocationV0_68

namespace KUOS.OpenHorizon.MemoryOSLineageQuotientRevocationCutV0_69

structure LineageEvidence where
  evidenceId : ℕ
  lineageRootId : ℕ
  surfaceConfidence : ℚ
  rootConfidence : ℚ
  lineageBudget : ℚ
deriving DecidableEq

def SameLineage (left right : LineageEvidence) : Prop :=
  left.lineageRootId = right.lineageRootId

theorem same_lineage_refl (evidence : LineageEvidence) :
    SameLineage evidence evidence :=
  rfl

theorem same_lineage_symmetric
    {left right : LineageEvidence}
    (h : SameLineage left right) :
    SameLineage right left :=
  h.symm

theorem same_lineage_transitive
    {first second third : LineageEvidence}
    (hfirst : SameLineage first second)
    (hsecond : SameLineage second third) :
    SameLineage first third :=
  hfirst.trans hsecond

def IndependentFrom
    (accepted : Finset LineageEvidence)
    (evidence : LineageEvidence) : Prop :=
  ∀ prior ∈ accepted, ¬ SameLineage prior evidence

theorem duplicate_lineage_not_independent
    {accepted : Finset LineageEvidence}
    {prior evidence : LineageEvidence}
    (hprior : prior ∈ accepted)
    (hsame : SameLineage prior evidence) :
    ¬ IndependentFrom accepted evidence := by
  intro hindependent
  exact hindependent prior hprior hsame

def splitAdjustedWeight (lineageBudget : ℚ) : ℚ :=
  lineageBudget / 2

theorem duplicate_pair_weight_conservation (lineageBudget : ℚ) :
    splitAdjustedWeight lineageBudget +
      splitAdjustedWeight lineageBudget =
      lineageBudget := by
  unfold splitAdjustedWeight
  ring

def rootScopedContribution
    (adjustedWeight rootConfidence surfaceConfidence : ℚ) : ℚ :=
  adjustedWeight * rootConfidence

theorem surface_rewrite_not_promoted
    (adjustedWeight rootConfidence firstSurface secondSurface : ℚ) :
    rootScopedContribution adjustedWeight rootConfidence firstSurface =
      rootScopedContribution adjustedWeight rootConfidence secondSurface :=
  rfl

theorem duplicate_pair_root_contribution_conservation
    (lineageBudget rootConfidence firstSurface secondSurface : ℚ) :
    rootScopedContribution
        (splitAdjustedWeight lineageBudget)
        rootConfidence
        firstSurface +
      rootScopedContribution
        (splitAdjustedWeight lineageBudget)
        rootConfidence
        secondSurface =
      lineageBudget * rootConfidence := by
  unfold rootScopedContribution splitAdjustedWeight
  ring

structure LineageBundle where
  lineageRootId : ℕ
  adjustedWeight : ℚ
  rootConfidence : ℚ
deriving DecidableEq

def totalLineageWeight (bundles : Finset LineageBundle) : ℚ :=
  ∑ bundle ∈ bundles, bundle.adjustedWeight

def lineageConfidenceNumerator (bundles : Finset LineageBundle) : ℚ :=
  ∑ bundle ∈ bundles, bundle.adjustedWeight * bundle.rootConfidence

def lineageAdjustedConfidence (bundles : Finset LineageBundle) : ℚ :=
  lineageConfidenceNumerator bundles / totalLineageWeight bundles

theorem lineage_confidence_numerator_nonnegative
    (bundles : Finset LineageBundle)
    (hbounded : ∀ bundle ∈ bundles,
      0 ≤ bundle.adjustedWeight ∧
      0 ≤ bundle.rootConfidence ∧
      bundle.rootConfidence ≤ 1) :
    0 ≤ lineageConfidenceNumerator bundles := by
  unfold lineageConfidenceNumerator
  apply Finset.sum_nonneg
  intro bundle hbundle
  exact mul_nonneg
    (hbounded bundle hbundle).1
    (hbounded bundle hbundle).2.1

theorem lineage_confidence_numerator_le_total_weight
    (bundles : Finset LineageBundle)
    (hbounded : ∀ bundle ∈ bundles,
      0 ≤ bundle.adjustedWeight ∧
      0 ≤ bundle.rootConfidence ∧
      bundle.rootConfidence ≤ 1) :
    lineageConfidenceNumerator bundles ≤ totalLineageWeight bundles := by
  unfold lineageConfidenceNumerator totalLineageWeight
  apply Finset.sum_le_sum
  intro bundle hbundle
  have h := hbounded bundle hbundle
  have hmul :=
    mul_le_mul_of_nonneg_left h.2.2 h.1
  simpa using hmul

theorem lineage_adjusted_confidence_nonnegative
    (bundles : Finset LineageBundle)
    (hbounded : ∀ bundle ∈ bundles,
      0 ≤ bundle.adjustedWeight ∧
      0 ≤ bundle.rootConfidence ∧
      bundle.rootConfidence ≤ 1)
    (htotal : 0 < totalLineageWeight bundles) :
    0 ≤ lineageAdjustedConfidence bundles := by
  unfold lineageAdjustedConfidence
  exact div_nonneg
    (lineage_confidence_numerator_nonnegative bundles hbounded)
    (le_of_lt htotal)

theorem lineage_adjusted_confidence_le_one
    (bundles : Finset LineageBundle)
    (hbounded : ∀ bundle ∈ bundles,
      0 ≤ bundle.adjustedWeight ∧
      0 ≤ bundle.rootConfidence ∧
      bundle.rootConfidence ≤ 1)
    (htotal : 0 < totalLineageWeight bundles) :
    lineageAdjustedConfidence bundles ≤ 1 := by
  unfold lineageAdjustedConfidence
  apply (div_le_iff₀ htotal).2
  simpa using
    lineage_confidence_numerator_le_total_weight bundles hbounded

theorem lineage_adjusted_confidence_mem_unit_interval
    (bundles : Finset LineageBundle)
    (hbounded : ∀ bundle ∈ bundles,
      0 ≤ bundle.adjustedWeight ∧
      0 ≤ bundle.rootConfidence ∧
      bundle.rootConfidence ≤ 1)
    (htotal : 0 < totalLineageWeight bundles) :
    lineageAdjustedConfidence bundles ∈ Set.Icc (0 : ℚ) 1 := by
  exact ⟨
    lineage_adjusted_confidence_nonnegative bundles hbounded htotal,
    lineage_adjusted_confidence_le_one bundles hbounded htotal
  ⟩

def BlocksAll
    {α : Type} [DecidableEq α]
    (paths : Finset (List α))
    (cut : Finset α) : Prop :=
  ∀ path ∈ paths, ∃ node ∈ path, node ∈ cut

def ErasureMinimalCut
    {α : Type} [DecidableEq α]
    (paths : Finset (List α))
    (cut : Finset α) : Prop :=
  BlocksAll paths cut ∧
    ∀ node ∈ cut, ¬ BlocksAll paths (cut.erase node)

def legacyRevocationPaths : Finset (List String) :=
  {
    ["policy-legacy-derived"],
    ["policy-legacy-derived", "policy-legacy-downstream"]
  }

def legacyBridgeCut : Finset String :=
  {"policy-legacy-derived"}

theorem legacy_bridge_cut_blocks_all :
    BlocksAll legacyRevocationPaths legacyBridgeCut := by
  simp [BlocksAll, legacyRevocationPaths, legacyBridgeCut]

theorem legacy_empty_cut_does_not_block :
    ¬ BlocksAll legacyRevocationPaths (∅ : Finset String) := by
  simp [BlocksAll, legacyRevocationPaths]

theorem legacy_bridge_cut_erasure_minimal :
    ErasureMinimalCut legacyRevocationPaths legacyBridgeCut := by
  simp [
    ErasureMinimalCut,
    BlocksAll,
    legacyRevocationPaths,
    legacyBridgeCut
  ]

structure LineageQuotientRevocationCutCertificate where
  sourceMemoryOSV068Bound : Bool
  lineageDuplicateDetectionExact : Bool
  lineageRootPartitionExact : Bool
  dependentCopyWeightConservationExact : Bool
  lineageAdjustedConfidenceExact : Bool
  derivedSurfaceConfidencePromoted : Bool
  singleLoadBearingMemorySilentlyTrusted : Bool
  minimalRevocationCutExact : Bool
  sourceRecordDeletedByRevocationCut : Bool
  candidateSelectionPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSLineageQuotientRevocationCutV0_69
