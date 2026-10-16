import Mathlib
import KUOS.OpenHorizon.MemoryOSLineageQuotientRevocationCutV0_69

namespace KUOS.OpenHorizon.MemoryOSCollusionCorrelationWeightedCutV0_70

structure CollusionSignal where
  leftLineageRootId : ℕ
  rightLineageRootId : ℕ
  provenanceOverlap : ℚ
  behavioralCorrelation : ℚ
  synchronizedSupport : Bool
deriving DecidableEq


def SuspectedCollusion (signal : CollusionSignal) : Prop :=
  signal.leftLineageRootId ≠ signal.rightLineageRootId ∧
    (1 / 2 : ℚ) ≤ signal.provenanceOverlap ∧
    (3 / 4 : ℚ) ≤ signal.behavioralCorrelation ∧
    signal.synchronizedSupport = true


theorem suspected_collusion_requires_distinct_lineages
    {signal : CollusionSignal}
    (h : SuspectedCollusion signal) :
    signal.leftLineageRootId ≠ signal.rightLineageRootId :=
  h.1


def canonicalCollusionSignal : CollusionSignal where
  leftLineageRootId := 101
  rightLineageRootId := 102
  provenanceOverlap := 3 / 4
  behavioralCorrelation := 7 / 8
  synchronizedSupport := true


def canonicalBenignSignal : CollusionSignal where
  leftLineageRootId := 101
  rightLineageRootId := 103
  provenanceOverlap := 1 / 4
  behavioralCorrelation := 1 / 5
  synchronizedSupport := false


theorem canonical_collusion_detected :
    SuspectedCollusion canonicalCollusionSignal := by
  norm_num [SuspectedCollusion, canonicalCollusionSignal]


theorem canonical_benign_pair_not_detected :
    ¬ SuspectedCollusion canonicalBenignSignal := by
  norm_num [SuspectedCollusion, canonicalBenignSignal]


def effectiveIndependentCountOnePair (rho : ℚ) : ℚ :=
  16 / (4 + 2 * rho)


theorem independent_four_source_effective_count :
    effectiveIndependentCountOnePair 0 = 4 := by
  norm_num [effectiveIndependentCountOnePair]


theorem canonical_correlated_effective_count :
    effectiveIndependentCountOnePair (3 / 4) = 32 / 11 := by
  norm_num [effectiveIndependentCountOnePair]


theorem canonical_correlation_reduces_effective_count :
    effectiveIndependentCountOnePair (3 / 4) < 4 := by
  norm_num [effectiveIndependentCountOnePair]


theorem positive_pair_correlation_reduces_effective_count
    (rho : ℚ) (hrho : 0 < rho) :
    effectiveIndependentCountOnePair rho < 4 := by
  unfold effectiveIndependentCountOnePair
  have hden : 0 < 4 + 2 * rho := by
    linarith
  apply (div_lt_iff₀ hden).2
  nlinarith


def splitCoalitionWeight (coalitionBudget : ℚ) : ℚ :=
  coalitionBudget / 2


theorem collusive_pair_weight_conservation (coalitionBudget : ℚ) :
    splitCoalitionWeight coalitionBudget +
      splitCoalitionWeight coalitionBudget =
      coalitionBudget := by
  unfold splitCoalitionWeight
  ring


def coalitionContribution
    (adjustedWeight rootConfidence : ℚ) : ℚ :=
  adjustedWeight * rootConfidence


theorem collusive_pair_contribution_conservation
    (coalitionBudget rootConfidence : ℚ) :
    coalitionContribution
        (splitCoalitionWeight coalitionBudget)
        rootConfidence +
      coalitionContribution
        (splitCoalitionWeight coalitionBudget)
        rootConfidence =
      coalitionBudget * rootConfidence := by
  unfold coalitionContribution splitCoalitionWeight
  ring


def naiveFourSourceConfidence
    (first second third fourth : ℚ) : ℚ :=
  (first + second + third + fourth) / 4


def componentCappedConfidence
    (collusiveComponent independentA independentB : ℚ) : ℚ :=
  (collusiveComponent + independentA + independentB) / 3


theorem canonical_naive_confidence :
    naiveFourSourceConfidence
        (19 / 20) (19 / 20) (3 / 5) (7 / 10) =
      4 / 5 := by
  norm_num [naiveFourSourceConfidence]


theorem canonical_component_capped_confidence :
    componentCappedConfidence (19 / 20) (3 / 5) (7 / 10) =
      3 / 4 := by
  norm_num [componentCappedConfidence]


theorem canonical_component_cap_reduces_collusive_inflation :
    componentCappedConfidence (19 / 20) (3 / 5) (7 / 10) <
      naiveFourSourceConfidence
        (19 / 20) (19 / 20) (3 / 5) (7 / 10) := by
  norm_num [componentCappedConfidence, naiveFourSourceConfidence]


theorem component_capped_confidence_mem_unit_interval
    (collusiveComponent independentA independentB : ℚ)
    (hcollusive : 0 ≤ collusiveComponent ∧ collusiveComponent ≤ 1)
    (ha : 0 ≤ independentA ∧ independentA ≤ 1)
    (hb : 0 ≤ independentB ∧ independentB ≤ 1) :
    componentCappedConfidence
        collusiveComponent independentA independentB ∈ Set.Icc (0 : ℚ) 1 := by
  unfold componentCappedConfidence
  constructor <;> linarith


inductive RevocationNode
  | hub
  | branchA
  | branchB
  | leafA
  | leafB
deriving DecidableEq, Repr


def revocationNodeCost : RevocationNode → ℚ
  | .hub => 3
  | .branchA => 1
  | .branchB => 1
  | .leafA => 2
  | .leafB => 2


def weightedCutCost (cut : Finset RevocationNode) : ℚ :=
  ∑ node ∈ cut, revocationNodeCost node


def branchingRevocationPaths : Finset (List RevocationNode) :=
  {
    [.hub, .branchA, .leafA],
    [.hub, .branchB, .leafB]
  }


def BlocksAll
    {α : Type} [DecidableEq α]
    (paths : Finset (List α))
    (cut : Finset α) : Prop :=
  ∀ path ∈ paths, ∃ node ∈ path, node ∈ cut


def weightedBranchCut : Finset RevocationNode :=
  {.branchA, .branchB}


def cardinalityHubCut : Finset RevocationNode :=
  {.hub}


def inclusionMinimalBlockingCuts : Finset (Finset RevocationNode) :=
  {
    {.hub},
    {.branchA, .branchB},
    {.branchA, .leafB},
    {.leafA, .branchB},
    {.leafA, .leafB}
  }


def WeightedMinimumWithin
    (paths : Finset (List RevocationNode))
    (candidates : Finset (Finset RevocationNode))
    (cut : Finset RevocationNode) : Prop :=
  cut ∈ candidates ∧
    BlocksAll paths cut ∧
    ∀ other ∈ candidates,
      BlocksAll paths other →
        weightedCutCost cut ≤ weightedCutCost other


theorem weighted_branch_cut_blocks_all :
    BlocksAll branchingRevocationPaths weightedBranchCut := by
  native_decide


theorem weighted_branch_cut_cost :
    weightedCutCost weightedBranchCut = 2 := by
  native_decide


theorem cardinality_hub_cut_cost :
    weightedCutCost cardinalityHubCut = 3 := by
  native_decide


theorem weighted_cut_differs_from_minimum_cardinality_cut :
    weightedBranchCut.card = 2 ∧
      cardinalityHubCut.card = 1 ∧
      weightedCutCost weightedBranchCut <
        weightedCutCost cardinalityHubCut := by
  native_decide


theorem weighted_branch_cut_unique_minimum :
    WeightedMinimumWithin
        branchingRevocationPaths
        inclusionMinimalBlockingCuts
        weightedBranchCut ∧
      ∀ other ∈ inclusionMinimalBlockingCuts,
        BlocksAll branchingRevocationPaths other →
          weightedCutCost other = weightedCutCost weightedBranchCut →
          other = weightedBranchCut := by
  native_decide


structure CollusionCorrelationWeightedCutCertificate where
  sourceMemoryOSV069Bound : Bool
  collusionSignalFusionExact : Bool
  correlationMatrixExact : Bool
  effectiveIndependentSourceCountExact : Bool
  componentCappedConfidenceExact : Bool
  collusiveCopiesCountedIndependently : Bool
  minimumWeightedRevocationCutExact : Bool
  minimumCardinalityCutClaimedWeightedOptimal : Bool
  sourceRecordDeletedByRevocationCut : Bool
  candidateSelectionPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSCollusionCorrelationWeightedCutV0_70
