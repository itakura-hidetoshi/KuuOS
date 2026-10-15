import Mathlib

namespace KUOS.CodeAI.BaselineVersusCodeAIAblationComparisonV0_1

structure Binding where
  controllerVersion : Nat
  predecessorManifest : Nat
  predecessorPack : Nat
  predecessorReceipt : Nat
  sampleBinding : Nat
  holdoutPartition : Nat
  comparisonContract : Nat
  deriving DecidableEq

structure ComparisonPlan where
  binding : Binding
  phasePreregistration : Bool
  aggregateOnly : Bool
  holdoutFrozen : Bool
  comparisonDirectionPredeclared : Bool
  limitedComparisonAuthority : Bool
  repositoryMutationAuthority : Bool
  gitAuthority : Bool
  correctnessClaimed : Bool
  deriving DecidableEq

structure CohortRegistry where
  binding : Binding
  baselineCount : Nat
  codeaiCount : Nat
  ablationCount : Nat
  equalTargetSampleCount : Bool
  nonzeroTargetSampleCount : Bool
  frozenBeforeObservation : Bool
  aggregateOnly : Bool
  commonSampleBinding : Bool
  commonHoldoutPartition : Bool
  goldVisible : Bool
  rawTestNamesVisible : Bool
  rawLogsVisible : Bool
  candidateFeedback : Bool
  repairMemoryFeedback : Bool
  deriving DecidableEq

structure MetricRegistry where
  binding : Binding
  metricCount : Nat
  primaryMetricCount : Nat
  allMetricsPredeclared : Bool
  comparisonDirectionPredeclared : Bool
  missingEvidenceHolds : Bool
  executionFailureCountsAsUnresolved : Bool
  deriving DecidableEq

structure ObservationRegistry where
  binding : Binding
  codeaiPredecessorBound : Bool
  codeaiMeasuredCount : Nat
  pendingCohortCount : Nat
  aggregateOnly : Bool
  rawGoldVisible : Bool
  rawTestNamesVisible : Bool
  rawLogsVisible : Bool
  performanceComparisonCompleted : Bool
  performanceClaimed : Bool
  deriving DecidableEq

structure ComparisonEvidence where
  plan : ComparisonPlan
  cohorts : CohortRegistry
  metrics : MetricRegistry
  observations : ObservationRegistry
  deriving DecidableEq

def ExactBinding (query : Binding) (evidence : ComparisonEvidence) : Prop :=
  evidence.plan.binding = query ∧
  evidence.cohorts.binding = query ∧
  evidence.metrics.binding = query ∧
  evidence.observations.binding = query

def CohortsPreregistered (evidence : ComparisonEvidence) : Prop :=
  evidence.cohorts.baselineCount = 1 ∧
  evidence.cohorts.codeaiCount = 1 ∧
  evidence.cohorts.ablationCount = 3 ∧
  evidence.cohorts.equalTargetSampleCount = true ∧
  evidence.cohorts.nonzeroTargetSampleCount = true ∧
  evidence.cohorts.frozenBeforeObservation = true ∧
  evidence.cohorts.aggregateOnly = true ∧
  evidence.cohorts.commonSampleBinding = true ∧
  evidence.cohorts.commonHoldoutPartition = true

def MetricsPreregistered (evidence : ComparisonEvidence) : Prop :=
  evidence.metrics.metricCount = 5 ∧
  evidence.metrics.primaryMetricCount = 1 ∧
  evidence.metrics.allMetricsPredeclared = true ∧
  evidence.metrics.comparisonDirectionPredeclared = true ∧
  evidence.metrics.missingEvidenceHolds = true ∧
  evidence.metrics.executionFailureCountsAsUnresolved = true

def ObservationPreregistrationComplete (evidence : ComparisonEvidence) : Prop :=
  evidence.observations.codeaiPredecessorBound = true ∧
  evidence.observations.codeaiMeasuredCount = 1 ∧
  evidence.observations.pendingCohortCount = 4 ∧
  evidence.observations.aggregateOnly = true ∧
  evidence.observations.performanceComparisonCompleted = false ∧
  evidence.observations.performanceClaimed = false

def IsolationPreserved (evidence : ComparisonEvidence) : Prop :=
  evidence.cohorts.goldVisible = false ∧
  evidence.cohorts.rawTestNamesVisible = false ∧
  evidence.cohorts.rawLogsVisible = false ∧
  evidence.cohorts.candidateFeedback = false ∧
  evidence.cohorts.repairMemoryFeedback = false ∧
  evidence.observations.rawGoldVisible = false ∧
  evidence.observations.rawTestNamesVisible = false ∧
  evidence.observations.rawLogsVisible = false

def BoundaryPreserved (evidence : ComparisonEvidence) : Prop :=
  evidence.plan.phasePreregistration = true ∧
  evidence.plan.aggregateOnly = true ∧
  evidence.plan.holdoutFrozen = true ∧
  evidence.plan.comparisonDirectionPredeclared = true ∧
  evidence.plan.limitedComparisonAuthority = true ∧
  evidence.plan.repositoryMutationAuthority = false ∧
  evidence.plan.gitAuthority = false ∧
  evidence.plan.correctnessClaimed = false

def PreregistrationAdmitted (query : Binding) (evidence : ComparisonEvidence) : Prop :=
  ExactBinding query evidence ∧
  CohortsPreregistered evidence ∧
  MetricsPreregistered evidence ∧
  ObservationPreregistrationComplete evidence ∧
  IsolationPreserved evidence ∧
  BoundaryPreserved evidence

theorem admitted_exact_binding
    {query : Binding} {evidence : ComparisonEvidence}
    (h : PreregistrationAdmitted query evidence) :
    ExactBinding query evidence := h.1

theorem admitted_cohorts_preregistered
    {query : Binding} {evidence : ComparisonEvidence}
    (h : PreregistrationAdmitted query evidence) :
    CohortsPreregistered evidence := h.2.1

theorem admitted_metrics_preregistered
    {query : Binding} {evidence : ComparisonEvidence}
    (h : PreregistrationAdmitted query evidence) :
    MetricsPreregistered evidence := h.2.2.1

theorem admitted_observation_preregistration_complete
    {query : Binding} {evidence : ComparisonEvidence}
    (h : PreregistrationAdmitted query evidence) :
    ObservationPreregistrationComplete evidence := h.2.2.2.1

theorem admitted_isolation_preserved
    {query : Binding} {evidence : ComparisonEvidence}
    (h : PreregistrationAdmitted query evidence) :
    IsolationPreserved evidence := h.2.2.2.2.1

theorem admitted_boundary_preserved
    {query : Binding} {evidence : ComparisonEvidence}
    (h : PreregistrationAdmitted query evidence) :
    BoundaryPreserved evidence := h.2.2.2.2.2

theorem binding_mismatch_forbids_admission
    {query : Binding} {evidence : ComparisonEvidence}
    (hMismatch : evidence.plan.binding ≠ query) :
    ¬ PreregistrationAdmitted query evidence := by
  intro h
  exact hMismatch (admitted_exact_binding h).1

theorem cohort_imbalance_forbids_admission
    {query : Binding} {evidence : ComparisonEvidence}
    (hImbalance : evidence.cohorts.equalTargetSampleCount = false) :
    ¬ PreregistrationAdmitted query evidence := by
  intro h
  rcases admitted_cohorts_preregistered h with ⟨_, _, _, hEqual, _, _, _, _, _⟩
  rw [hImbalance] at hEqual
  contradiction

theorem missing_primary_metric_forbids_admission
    {query : Binding} {evidence : ComparisonEvidence}
    (hMissing : evidence.metrics.primaryMetricCount = 0) :
    ¬ PreregistrationAdmitted query evidence := by
  intro h
  rcases admitted_metrics_preregistered h with ⟨_, hPrimary, _, _, _, _⟩
  omega

theorem gold_visibility_forbids_admission
    {query : Binding} {evidence : ComparisonEvidence}
    (hGold : evidence.cohorts.goldVisible = true) :
    ¬ PreregistrationAdmitted query evidence := by
  intro h
  rcases admitted_isolation_preserved h with ⟨hHidden, _, _, _, _, _, _, _⟩
  rw [hGold] at hHidden
  contradiction

theorem raw_test_names_forbid_admission
    {query : Binding} {evidence : ComparisonEvidence}
    (hNames : evidence.observations.rawTestNamesVisible = true) :
    ¬ PreregistrationAdmitted query evidence := by
  intro h
  rcases admitted_isolation_preserved h with ⟨_, _, _, _, _, _, hHidden, _⟩
  rw [hNames] at hHidden
  contradiction

theorem repository_mutation_authority_forbids_admission
    {query : Binding} {evidence : ComparisonEvidence}
    (hMutation : evidence.plan.repositoryMutationAuthority = true) :
    ¬ PreregistrationAdmitted query evidence := by
  intro h
  rcases admitted_boundary_preserved h with ⟨_, _, _, _, _, hNone, _, _⟩
  rw [hMutation] at hNone
  contradiction

theorem correctness_claim_forbids_admission
    {query : Binding} {evidence : ComparisonEvidence}
    (hClaim : evidence.plan.correctnessClaimed = true) :
    ¬ PreregistrationAdmitted query evidence := by
  intro h
  rcases admitted_boundary_preserved h with ⟨_, _, _, _, _, _, _, hNone⟩
  rw [hClaim] at hNone
  contradiction

def referenceBinding : Binding where
  controllerVersion := 1340
  predecessorManifest := 1
  predecessorPack := 2
  predecessorReceipt := 3
  sampleBinding := 4
  holdoutPartition := 5
  comparisonContract := 6

def referencePlan : ComparisonPlan where
  binding := referenceBinding
  phasePreregistration := true
  aggregateOnly := true
  holdoutFrozen := true
  comparisonDirectionPredeclared := true
  limitedComparisonAuthority := true
  repositoryMutationAuthority := false
  gitAuthority := false
  correctnessClaimed := false

def referenceCohorts : CohortRegistry where
  binding := referenceBinding
  baselineCount := 1
  codeaiCount := 1
  ablationCount := 3
  equalTargetSampleCount := true
  nonzeroTargetSampleCount := true
  frozenBeforeObservation := true
  aggregateOnly := true
  commonSampleBinding := true
  commonHoldoutPartition := true
  goldVisible := false
  rawTestNamesVisible := false
  rawLogsVisible := false
  candidateFeedback := false
  repairMemoryFeedback := false

def referenceMetrics : MetricRegistry where
  binding := referenceBinding
  metricCount := 5
  primaryMetricCount := 1
  allMetricsPredeclared := true
  comparisonDirectionPredeclared := true
  missingEvidenceHolds := true
  executionFailureCountsAsUnresolved := true

def referenceObservations : ObservationRegistry where
  binding := referenceBinding
  codeaiPredecessorBound := true
  codeaiMeasuredCount := 1
  pendingCohortCount := 4
  aggregateOnly := true
  rawGoldVisible := false
  rawTestNamesVisible := false
  rawLogsVisible := false
  performanceComparisonCompleted := false
  performanceClaimed := false

def referenceEvidence : ComparisonEvidence where
  plan := referencePlan
  cohorts := referenceCohorts
  metrics := referenceMetrics
  observations := referenceObservations

def referenceGoldLeak : ComparisonEvidence :=
  { referenceEvidence with
    cohorts := { referenceCohorts with goldVisible := true } }

def referenceRepositoryMutation : ComparisonEvidence :=
  { referenceEvidence with
    plan := { referencePlan with repositoryMutationAuthority := true } }

theorem reference_preregistration_admitted :
    PreregistrationAdmitted referenceBinding referenceEvidence := by
  simp [PreregistrationAdmitted, ExactBinding, CohortsPreregistered,
    MetricsPreregistered, ObservationPreregistrationComplete,
    IsolationPreserved, BoundaryPreserved, referenceBinding, referencePlan,
    referenceCohorts, referenceMetrics, referenceObservations, referenceEvidence]

theorem reference_performance_comparison_not_completed :
    referenceEvidence.observations.performanceComparisonCompleted = false := by
  rfl

theorem reference_gold_leak_not_admitted :
    ¬ PreregistrationAdmitted referenceBinding referenceGoldLeak := by
  exact gold_visibility_forbids_admission rfl

theorem reference_repository_mutation_not_admitted :
    ¬ PreregistrationAdmitted referenceBinding referenceRepositoryMutation := by
  exact repository_mutation_authority_forbids_admission rfl

end KUOS.CodeAI.BaselineVersusCodeAIAblationComparisonV0_1
