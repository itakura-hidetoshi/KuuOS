import Mathlib

namespace KUOS.CodeAI.BoundedOfficialHarnessExecutionV0_1

structure Binding where
  controllerVersion : Nat
  predecessorManifest : Nat
  predecessorPack : Nat
  predecessorReceipt : Nat
  externalArtifact : Nat
  datasetRevision : Nat
  harnessVersion : Nat
  instanceId : Nat
  baseCommit : Nat
  prediction : Nat
  executionContract : Nat
  deriving DecidableEq

structure ExecutionPlan where
  binding : Binding
  sampleCount : Nat
  maximumWorkers : Nat
  timeoutSeconds : Nat
  sampleFrozen : Bool
  predictionFrozen : Bool
  officialPredictionShape : Bool
  nonGoldPrediction : Bool
  goldAvailableToSolver : Bool
  deriving DecidableEq

structure PredictionEvidence where
  binding : Binding
  patchPresent : Bool
  changedPathDerived : Bool
  goldDerived : Bool
  goldAccessed : Bool
  claimsResolved : Bool
  claimsCorrectness : Bool
  deriving DecidableEq

structure ExecutionObservation where
  binding : Binding
  externalHarnessObserved : Bool
  harnessExecutedByKernel : Bool
  dockerUsed : Bool
  imageAvailable : Bool
  containerStarted : Bool
  patchApplied : Bool
  evaluationCompleted : Bool
  resolved : Bool
  reportObserved : Bool
  logsObserved : Bool
  goldExposedToSolver : Bool
  goldUsedForCandidateGeneration : Bool
  goldUsedForRepairMemory : Bool
  repositoryMutated : Bool
  gitAuthority : Bool
  correctnessClaimed : Bool
  deriving DecidableEq

structure ExecutionEvidence where
  plan : ExecutionPlan
  predictionEvidence : PredictionEvidence
  observation : ExecutionObservation
  futureHarnessAuthority : Bool
  futureRepositoryMutationAuthority : Bool
  futureGitAuthority : Bool
  deriving DecidableEq

def ExactBinding (query : Binding) (evidence : ExecutionEvidence) : Prop :=
  evidence.plan.binding = query ∧
  evidence.predictionEvidence.binding = query ∧
  evidence.observation.binding = query

def PlanBounded (evidence : ExecutionEvidence) : Prop :=
  evidence.plan.sampleCount = 1 ∧
  evidence.plan.maximumWorkers = 1 ∧
  evidence.plan.timeoutSeconds = 1800 ∧
  evidence.plan.sampleFrozen = true ∧
  evidence.plan.predictionFrozen = true ∧
  evidence.plan.officialPredictionShape = true ∧
  evidence.plan.nonGoldPrediction = true ∧
  evidence.plan.goldAvailableToSolver = false

def PredictionFrozen (evidence : ExecutionEvidence) : Prop :=
  evidence.predictionEvidence.patchPresent = true ∧
  evidence.predictionEvidence.changedPathDerived = true ∧
  evidence.predictionEvidence.goldDerived = false ∧
  evidence.predictionEvidence.goldAccessed = false ∧
  evidence.predictionEvidence.claimsResolved = false ∧
  evidence.predictionEvidence.claimsCorrectness = false

def ObservationComplete (evidence : ExecutionEvidence) : Prop :=
  evidence.observation.externalHarnessObserved = true ∧
  evidence.observation.dockerUsed = true ∧
  evidence.observation.imageAvailable = true ∧
  evidence.observation.containerStarted = true ∧
  evidence.observation.patchApplied = true ∧
  evidence.observation.evaluationCompleted = true ∧
  evidence.observation.reportObserved = true ∧
  evidence.observation.logsObserved = true

def GoldIsolationPreserved (evidence : ExecutionEvidence) : Prop :=
  evidence.observation.harnessExecutedByKernel = false ∧
  evidence.observation.goldExposedToSolver = false ∧
  evidence.observation.goldUsedForCandidateGeneration = false ∧
  evidence.observation.goldUsedForRepairMemory = false

def BoundaryPreserved (evidence : ExecutionEvidence) : Prop :=
  evidence.observation.repositoryMutated = false ∧
  evidence.observation.gitAuthority = false ∧
  evidence.observation.correctnessClaimed = false ∧
  evidence.futureHarnessAuthority = false ∧
  evidence.futureRepositoryMutationAuthority = false ∧
  evidence.futureGitAuthority = false

def ExecutionAdmitted (query : Binding) (evidence : ExecutionEvidence) : Prop :=
  ExactBinding query evidence ∧
  PlanBounded evidence ∧
  PredictionFrozen evidence ∧
  ObservationComplete evidence ∧
  GoldIsolationPreserved evidence ∧
  BoundaryPreserved evidence

theorem admitted_exact_binding
    {query : Binding} {evidence : ExecutionEvidence}
    (h : ExecutionAdmitted query evidence) :
    ExactBinding query evidence := h.1

theorem admitted_plan_bounded
    {query : Binding} {evidence : ExecutionEvidence}
    (h : ExecutionAdmitted query evidence) :
    PlanBounded evidence := h.2.1

theorem admitted_prediction_frozen
    {query : Binding} {evidence : ExecutionEvidence}
    (h : ExecutionAdmitted query evidence) :
    PredictionFrozen evidence := h.2.2.1

theorem admitted_observation_complete
    {query : Binding} {evidence : ExecutionEvidence}
    (h : ExecutionAdmitted query evidence) :
    ObservationComplete evidence := h.2.2.2.1

theorem admitted_gold_isolation
    {query : Binding} {evidence : ExecutionEvidence}
    (h : ExecutionAdmitted query evidence) :
    GoldIsolationPreserved evidence := h.2.2.2.2.1

theorem admitted_boundary_preserved
    {query : Binding} {evidence : ExecutionEvidence}
    (h : ExecutionAdmitted query evidence) :
    BoundaryPreserved evidence := h.2.2.2.2.2

theorem controller_version_mismatch_forbids_admission
    {query : Binding} {evidence : ExecutionEvidence}
    (hMismatch : evidence.plan.binding.controllerVersion ≠ query.controllerVersion) :
    ¬ ExecutionAdmitted query evidence := by
  intro h
  exact hMismatch (congrArg Binding.controllerVersion (admitted_exact_binding h).1)

theorem missing_patch_forbids_admission
    {query : Binding} {evidence : ExecutionEvidence}
    (hMissing : evidence.predictionEvidence.patchPresent = false) :
    ¬ ExecutionAdmitted query evidence := by
  intro h
  have hPresent := (admitted_prediction_frozen h).1
  rw [hMissing] at hPresent
  contradiction

theorem unapplied_patch_forbids_admission
    {query : Binding} {evidence : ExecutionEvidence}
    (hUnapplied : evidence.observation.patchApplied = false) :
    ¬ ExecutionAdmitted query evidence := by
  intro h
  have hApplied := (admitted_observation_complete h).2.2.2.2.1
  rw [hUnapplied] at hApplied
  contradiction

theorem incomplete_evaluation_forbids_admission
    {query : Binding} {evidence : ExecutionEvidence}
    (hIncomplete : evidence.observation.evaluationCompleted = false) :
    ¬ ExecutionAdmitted query evidence := by
  intro h
  have hCompleted := (admitted_observation_complete h).2.2.2.2.2.1
  rw [hIncomplete] at hCompleted
  contradiction

theorem gold_exposure_forbids_admission
    {query : Binding} {evidence : ExecutionEvidence}
    (hExposure : evidence.observation.goldExposedToSolver = true) :
    ¬ ExecutionAdmitted query evidence := by
  intro h
  have hHidden := (admitted_gold_isolation h).2.1
  rw [hExposure] at hHidden
  contradiction

theorem kernel_harness_execution_forbids_admission
    {query : Binding} {evidence : ExecutionEvidence}
    (hKernel : evidence.observation.harnessExecutedByKernel = true) :
    ¬ ExecutionAdmitted query evidence := by
  intro h
  have hExternal := (admitted_gold_isolation h).1
  rw [hKernel] at hExternal
  contradiction

theorem repository_mutation_forbids_admission
    {query : Binding} {evidence : ExecutionEvidence}
    (hMutation : evidence.observation.repositoryMutated = true) :
    ¬ ExecutionAdmitted query evidence := by
  intro h
  have hNoMutation := (admitted_boundary_preserved h).1
  rw [hMutation] at hNoMutation
  contradiction

def referenceBinding : Binding where
  controllerVersion := 1338
  predecessorManifest := 1
  predecessorPack := 2
  predecessorReceipt := 3
  externalArtifact := 4
  datasetRevision := 5
  harnessVersion := 6
  instanceId := 20590
  baseCommit := 7
  prediction := 8
  executionContract := 9

def referencePlan : ExecutionPlan where
  binding := referenceBinding
  sampleCount := 1
  maximumWorkers := 1
  timeoutSeconds := 1800
  sampleFrozen := true
  predictionFrozen := true
  officialPredictionShape := true
  nonGoldPrediction := true
  goldAvailableToSolver := false

def referencePrediction : PredictionEvidence where
  binding := referenceBinding
  patchPresent := true
  changedPathDerived := true
  goldDerived := false
  goldAccessed := false
  claimsResolved := false
  claimsCorrectness := false

def referenceObservation : ExecutionObservation where
  binding := referenceBinding
  externalHarnessObserved := true
  harnessExecutedByKernel := false
  dockerUsed := true
  imageAvailable := true
  containerStarted := true
  patchApplied := true
  evaluationCompleted := true
  resolved := false
  reportObserved := true
  logsObserved := true
  goldExposedToSolver := false
  goldUsedForCandidateGeneration := false
  goldUsedForRepairMemory := false
  repositoryMutated := false
  gitAuthority := false
  correctnessClaimed := false

def referenceEvidence : ExecutionEvidence where
  plan := referencePlan
  predictionEvidence := referencePrediction
  observation := referenceObservation
  futureHarnessAuthority := false
  futureRepositoryMutationAuthority := false
  futureGitAuthority := false

def referencePatchMissing : ExecutionEvidence :=
  { referenceEvidence with
    predictionEvidence := { referencePrediction with patchPresent := false } }

def referenceGoldExposed : ExecutionEvidence :=
  { referenceEvidence with
    observation := { referenceObservation with goldExposedToSolver := true } }

def referenceKernelExecution : ExecutionEvidence :=
  { referenceEvidence with
    observation := { referenceObservation with harnessExecutedByKernel := true } }

theorem reference_unresolved_admitted :
    ExecutionAdmitted referenceBinding referenceEvidence := by
  simp [ExecutionAdmitted, ExactBinding, PlanBounded, PredictionFrozen,
    ObservationComplete, GoldIsolationPreserved, BoundaryPreserved,
    referenceBinding, referencePlan, referencePrediction, referenceObservation,
    referenceEvidence]

theorem reference_admission_does_not_require_resolution :
    referenceEvidence.observation.resolved = false := by
  rfl

theorem reference_patch_missing_not_admitted :
    ¬ ExecutionAdmitted referenceBinding referencePatchMissing := by
  exact missing_patch_forbids_admission rfl

theorem reference_gold_exposed_not_admitted :
    ¬ ExecutionAdmitted referenceBinding referenceGoldExposed := by
  exact gold_exposure_forbids_admission rfl

theorem reference_kernel_execution_not_admitted :
    ¬ ExecutionAdmitted referenceBinding referenceKernelExecution := by
  exact kernel_harness_execution_forbids_admission rfl

end KUOS.CodeAI.BoundedOfficialHarnessExecutionV0_1
