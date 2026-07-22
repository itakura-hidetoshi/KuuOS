import Mathlib

namespace KUOS.CodeAI.ExternalResultProcessEvidenceIngestionV0_1

structure Binding where
  controllerVersion : Nat
  predecessorManifest : Nat
  predecessorPack : Nat
  predecessorReceipt : Nat
  workflowRun : Nat
  externalArtifact : Nat
  prediction : Nat
  externalObservation : Nat
  ingestionContract : Nat
  deriving DecidableEq

structure IngestionPlan where
  binding : Binding
  resultCount : Nat
  processEvidenceCount : Nat
  aggregateOnly : Bool
  sourceArtifactExternal : Bool
  rawArtifactCommitted : Bool
  rawTestNamesIngested : Bool
  rawLogsIngested : Bool
  candidateFeedback : Bool
  repairMemoryFeedback : Bool
  comparisonAuthority : Bool
  deriving DecidableEq

structure ResultEvidence where
  binding : Binding
  patchExists : Bool
  patchApplied : Bool
  evaluationCompleted : Bool
  resolved : Bool
  failToPassSuccessCount : Nat
  failToPassFailureCount : Nat
  passToPassSuccessCount : Nat
  passToPassFailureCount : Nat
  errorCount : Nat
  rawTestNamesIncluded : Bool
  goldMaterialIncluded : Bool
  deriving DecidableEq

structure ProcessEvidence where
  binding : Binding
  workflowCompleted : Bool
  artifactExpired : Bool
  dockerUsed : Bool
  imageAvailable : Bool
  containerStarted : Bool
  patchAppliedCleanly : Bool
  evaluationCompleted : Bool
  gitDiffStable : Bool
  containerRemoved : Bool
  imageRemoved : Bool
  reportObserved : Bool
  logsObserved : Bool
  harnessExecutedByKernel : Bool
  rawLogsCommitted : Bool
  repositoryMutated : Bool
  gitAuthority : Bool
  correctnessClaimed : Bool
  deriving DecidableEq

structure IngestionEvidence where
  plan : IngestionPlan
  resultEvidence : ResultEvidence
  processEvidence : ProcessEvidence
  futureComparisonAuthority : Bool
  futureRepositoryMutationAuthority : Bool
  futureGitAuthority : Bool
  deriving DecidableEq

def ExactBinding (query : Binding) (evidence : IngestionEvidence) : Prop :=
  evidence.plan.binding = query ∧
  evidence.resultEvidence.binding = query ∧
  evidence.processEvidence.binding = query

def PlanAggregateOnly (evidence : IngestionEvidence) : Prop :=
  evidence.plan.resultCount = 1 ∧
  evidence.plan.processEvidenceCount = 1 ∧
  evidence.plan.aggregateOnly = true ∧
  evidence.plan.sourceArtifactExternal = true ∧
  evidence.plan.rawArtifactCommitted = false ∧
  evidence.plan.rawTestNamesIngested = false ∧
  evidence.plan.rawLogsIngested = false ∧
  evidence.plan.candidateFeedback = false ∧
  evidence.plan.repairMemoryFeedback = false ∧
  evidence.plan.comparisonAuthority = false

def ResultComplete (evidence : IngestionEvidence) : Prop :=
  evidence.resultEvidence.patchExists = true ∧
  evidence.resultEvidence.patchApplied = true ∧
  evidence.resultEvidence.evaluationCompleted = true ∧
  evidence.resultEvidence.errorCount = 0

def ProcessComplete (evidence : IngestionEvidence) : Prop :=
  evidence.processEvidence.workflowCompleted = true ∧
  evidence.processEvidence.artifactExpired = false ∧
  evidence.processEvidence.dockerUsed = true ∧
  evidence.processEvidence.imageAvailable = true ∧
  evidence.processEvidence.containerStarted = true ∧
  evidence.processEvidence.patchAppliedCleanly = true ∧
  evidence.processEvidence.evaluationCompleted = true ∧
  evidence.processEvidence.gitDiffStable = true ∧
  evidence.processEvidence.containerRemoved = true ∧
  evidence.processEvidence.imageRemoved = true ∧
  evidence.processEvidence.reportObserved = true ∧
  evidence.processEvidence.logsObserved = true

def IsolationPreserved (evidence : IngestionEvidence) : Prop :=
  evidence.resultEvidence.rawTestNamesIncluded = false ∧
  evidence.resultEvidence.goldMaterialIncluded = false ∧
  evidence.processEvidence.harnessExecutedByKernel = false ∧
  evidence.processEvidence.rawLogsCommitted = false ∧
  evidence.plan.candidateFeedback = false ∧
  evidence.plan.repairMemoryFeedback = false

def BoundaryPreserved (evidence : IngestionEvidence) : Prop :=
  evidence.processEvidence.repositoryMutated = false ∧
  evidence.processEvidence.gitAuthority = false ∧
  evidence.processEvidence.correctnessClaimed = false ∧
  evidence.futureComparisonAuthority = false ∧
  evidence.futureRepositoryMutationAuthority = false ∧
  evidence.futureGitAuthority = false

def IngestionAdmitted (query : Binding) (evidence : IngestionEvidence) : Prop :=
  ExactBinding query evidence ∧
  PlanAggregateOnly evidence ∧
  ResultComplete evidence ∧
  ProcessComplete evidence ∧
  IsolationPreserved evidence ∧
  BoundaryPreserved evidence

theorem admitted_exact_binding
    {query : Binding} {evidence : IngestionEvidence}
    (h : IngestionAdmitted query evidence) :
    ExactBinding query evidence := h.1

theorem admitted_plan_aggregate_only
    {query : Binding} {evidence : IngestionEvidence}
    (h : IngestionAdmitted query evidence) :
    PlanAggregateOnly evidence := h.2.1

theorem admitted_result_complete
    {query : Binding} {evidence : IngestionEvidence}
    (h : IngestionAdmitted query evidence) :
    ResultComplete evidence := h.2.2.1

theorem admitted_process_complete
    {query : Binding} {evidence : IngestionEvidence}
    (h : IngestionAdmitted query evidence) :
    ProcessComplete evidence := h.2.2.2.1

theorem admitted_isolation_preserved
    {query : Binding} {evidence : IngestionEvidence}
    (h : IngestionAdmitted query evidence) :
    IsolationPreserved evidence := h.2.2.2.2.1

theorem admitted_boundary_preserved
    {query : Binding} {evidence : IngestionEvidence}
    (h : IngestionAdmitted query evidence) :
    BoundaryPreserved evidence := h.2.2.2.2.2

theorem controller_version_mismatch_forbids_admission
    {query : Binding} {evidence : IngestionEvidence}
    (hMismatch : evidence.plan.binding.controllerVersion ≠ query.controllerVersion) :
    ¬ IngestionAdmitted query evidence := by
  intro h
  exact hMismatch (congrArg Binding.controllerVersion (admitted_exact_binding h).1)

theorem missing_patch_forbids_admission
    {query : Binding} {evidence : IngestionEvidence}
    (hMissing : evidence.resultEvidence.patchExists = false) :
    ¬ IngestionAdmitted query evidence := by
  intro h
  rcases admitted_result_complete h with ⟨hPatch, _, _, _⟩
  rw [hMissing] at hPatch
  contradiction

theorem incomplete_evaluation_forbids_admission
    {query : Binding} {evidence : IngestionEvidence}
    (hIncomplete : evidence.processEvidence.evaluationCompleted = false) :
    ¬ IngestionAdmitted query evidence := by
  intro h
  rcases admitted_process_complete h with ⟨_, _, _, _, _, _, hComplete, _, _, _, _, _⟩
  rw [hIncomplete] at hComplete
  contradiction

theorem raw_test_names_forbid_admission
    {query : Binding} {evidence : IngestionEvidence}
    (hNames : evidence.resultEvidence.rawTestNamesIncluded = true) :
    ¬ IngestionAdmitted query evidence := by
  intro h
  rcases admitted_isolation_preserved h with ⟨hHidden, _, _, _, _, _⟩
  rw [hNames] at hHidden
  contradiction

theorem gold_material_forbids_admission
    {query : Binding} {evidence : IngestionEvidence}
    (hGold : evidence.resultEvidence.goldMaterialIncluded = true) :
    ¬ IngestionAdmitted query evidence := by
  intro h
  rcases admitted_isolation_preserved h with ⟨_, hHidden, _, _, _, _⟩
  rw [hGold] at hHidden
  contradiction

theorem repair_feedback_forbids_admission
    {query : Binding} {evidence : IngestionEvidence}
    (hFeedback : evidence.plan.repairMemoryFeedback = true) :
    ¬ IngestionAdmitted query evidence := by
  intro h
  rcases admitted_isolation_preserved h with ⟨_, _, _, _, _, hDisabled⟩
  rw [hFeedback] at hDisabled
  contradiction

theorem kernel_harness_execution_forbids_admission
    {query : Binding} {evidence : IngestionEvidence}
    (hKernel : evidence.processEvidence.harnessExecutedByKernel = true) :
    ¬ IngestionAdmitted query evidence := by
  intro h
  rcases admitted_isolation_preserved h with ⟨_, _, hExternal, _, _, _⟩
  rw [hKernel] at hExternal
  contradiction

theorem repository_mutation_forbids_admission
    {query : Binding} {evidence : IngestionEvidence}
    (hMutation : evidence.processEvidence.repositoryMutated = true) :
    ¬ IngestionAdmitted query evidence := by
  intro h
  rcases admitted_boundary_preserved h with ⟨hNoMutation, _, _, _, _, _⟩
  rw [hMutation] at hNoMutation
  contradiction

theorem correctness_claim_forbids_admission
    {query : Binding} {evidence : IngestionEvidence}
    (hClaim : evidence.processEvidence.correctnessClaimed = true) :
    ¬ IngestionAdmitted query evidence := by
  intro h
  rcases admitted_boundary_preserved h with ⟨_, _, hNoClaim, _, _, _⟩
  rw [hClaim] at hNoClaim
  contradiction

def referenceBinding : Binding where
  controllerVersion := 1339
  predecessorManifest := 1
  predecessorPack := 2
  predecessorReceipt := 3
  workflowRun := 29894633457
  externalArtifact := 8520539325
  prediction := 4
  externalObservation := 5
  ingestionContract := 6

def referencePlan : IngestionPlan where
  binding := referenceBinding
  resultCount := 1
  processEvidenceCount := 1
  aggregateOnly := true
  sourceArtifactExternal := true
  rawArtifactCommitted := false
  rawTestNamesIngested := false
  rawLogsIngested := false
  candidateFeedback := false
  repairMemoryFeedback := false
  comparisonAuthority := false

def referenceResult : ResultEvidence where
  binding := referenceBinding
  patchExists := true
  patchApplied := true
  evaluationCompleted := true
  resolved := false
  failToPassSuccessCount := 0
  failToPassFailureCount := 1
  passToPassSuccessCount := 21
  passToPassFailureCount := 0
  errorCount := 0
  rawTestNamesIncluded := false
  goldMaterialIncluded := false

def referenceProcess : ProcessEvidence where
  binding := referenceBinding
  workflowCompleted := true
  artifactExpired := false
  dockerUsed := true
  imageAvailable := true
  containerStarted := true
  patchAppliedCleanly := true
  evaluationCompleted := true
  gitDiffStable := true
  containerRemoved := true
  imageRemoved := true
  reportObserved := true
  logsObserved := true
  harnessExecutedByKernel := false
  rawLogsCommitted := false
  repositoryMutated := false
  gitAuthority := false
  correctnessClaimed := false

def referenceEvidence : IngestionEvidence where
  plan := referencePlan
  resultEvidence := referenceResult
  processEvidence := referenceProcess
  futureComparisonAuthority := false
  futureRepositoryMutationAuthority := false
  futureGitAuthority := false

def referenceRawNames : IngestionEvidence :=
  { referenceEvidence with
    resultEvidence := { referenceResult with rawTestNamesIncluded := true } }

def referenceRepairFeedback : IngestionEvidence :=
  { referenceEvidence with
    plan := { referencePlan with repairMemoryFeedback := true } }

def referenceRepositoryMutation : IngestionEvidence :=
  { referenceEvidence with
    processEvidence := { referenceProcess with repositoryMutated := true } }

theorem reference_unresolved_admitted :
    IngestionAdmitted referenceBinding referenceEvidence := by
  simp [IngestionAdmitted, ExactBinding, PlanAggregateOnly, ResultComplete,
    ProcessComplete, IsolationPreserved, BoundaryPreserved, referenceBinding,
    referencePlan, referenceResult, referenceProcess, referenceEvidence]

theorem reference_admission_preserves_unresolved_outcome :
    referenceEvidence.resultEvidence.resolved = false := by
  rfl

theorem reference_raw_names_not_admitted :
    ¬ IngestionAdmitted referenceBinding referenceRawNames := by
  exact raw_test_names_forbid_admission rfl

theorem reference_repair_feedback_not_admitted :
    ¬ IngestionAdmitted referenceBinding referenceRepairFeedback := by
  exact repair_feedback_forbids_admission rfl

theorem reference_repository_mutation_not_admitted :
    ¬ IngestionAdmitted referenceBinding referenceRepositoryMutation := by
  exact repository_mutation_forbids_admission rfl

end KUOS.CodeAI.ExternalResultProcessEvidenceIngestionV0_1
