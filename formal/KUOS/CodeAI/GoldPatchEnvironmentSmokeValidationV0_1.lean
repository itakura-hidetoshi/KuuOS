import Mathlib

namespace KUOS.CodeAI.GoldPatchEnvironmentSmokeValidationV0_1

structure Binding where
  controllerVersion : Nat
  predecessorManifest : Nat
  predecessorPack : Nat
  predecessorReceipt : Nat
  datasetRevision : Nat
  datasetArtifact : Nat
  harnessVersion : Nat
  instance : Nat
  smokeContract : Nat
  environmentContract : Nat
  deriving DecidableEq

structure SmokePlan where
  binding : Binding
  preregistered : Bool
  goldPredictionMode : Bool
  evaluatorOnlyGold : Bool
  solverGoldAccess : Bool
  smokeRunCount : Nat
  maximumWorkers : Nat
  timeoutSeconds : Nat
  deriving DecidableEq

structure SmokeObservation where
  binding : Binding
  externalHarnessObserved : Bool
  harnessExecutedByKernel : Bool
  networkUsedByExternalHarness : Bool
  dockerUsed : Bool
  imageAvailable : Bool
  containerStarted : Bool
  goldPatchApplied : Bool
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

structure SmokeEvidence where
  plan : SmokePlan
  observation : SmokeObservation
  futureHarnessAuthority : Bool
  futureRepositoryMutationAuthority : Bool
  futureGitAuthority : Bool
  deriving DecidableEq

def ExactBinding (query : Binding) (evidence : SmokeEvidence) : Prop :=
  evidence.plan.binding = query ∧ evidence.observation.binding = query

def PlanPreregistered (evidence : SmokeEvidence) : Prop :=
  evidence.plan.preregistered = true ∧
  evidence.plan.goldPredictionMode = true ∧
  evidence.plan.evaluatorOnlyGold = true ∧
  evidence.plan.solverGoldAccess = false ∧
  evidence.plan.smokeRunCount = 1 ∧
  evidence.plan.maximumWorkers = 1

def ObservationVerified (evidence : SmokeEvidence) : Prop :=
  evidence.observation.externalHarnessObserved = true ∧
  evidence.observation.networkUsedByExternalHarness = true ∧
  evidence.observation.dockerUsed = true ∧
  evidence.observation.imageAvailable = true ∧
  evidence.observation.containerStarted = true ∧
  evidence.observation.goldPatchApplied = true ∧
  evidence.observation.evaluationCompleted = true ∧
  evidence.observation.resolved = true ∧
  evidence.observation.reportObserved = true ∧
  evidence.observation.logsObserved = true

def GoldIsolationPreserved (evidence : SmokeEvidence) : Prop :=
  evidence.observation.harnessExecutedByKernel = false ∧
  evidence.observation.goldExposedToSolver = false ∧
  evidence.observation.goldUsedForCandidateGeneration = false ∧
  evidence.observation.goldUsedForRepairMemory = false

def BoundaryPreserved (evidence : SmokeEvidence) : Prop :=
  evidence.observation.repositoryMutated = false ∧
  evidence.observation.gitAuthority = false ∧
  evidence.observation.correctnessClaimed = false ∧
  evidence.futureHarnessAuthority = false ∧
  evidence.futureRepositoryMutationAuthority = false ∧
  evidence.futureGitAuthority = false

def SmokeAdmitted (query : Binding) (evidence : SmokeEvidence) : Prop :=
  ExactBinding query evidence ∧
  PlanPreregistered evidence ∧
  ObservationVerified evidence ∧
  GoldIsolationPreserved evidence ∧
  BoundaryPreserved evidence

theorem admitted_exact_binding
    {query : Binding} {evidence : SmokeEvidence}
    (h : SmokeAdmitted query evidence) :
    ExactBinding query evidence := h.1

theorem admitted_plan_preregistered
    {query : Binding} {evidence : SmokeEvidence}
    (h : SmokeAdmitted query evidence) :
    PlanPreregistered evidence := h.2.1

theorem admitted_observation_verified
    {query : Binding} {evidence : SmokeEvidence}
    (h : SmokeAdmitted query evidence) :
    ObservationVerified evidence := h.2.2.1

theorem admitted_gold_isolation
    {query : Binding} {evidence : SmokeEvidence}
    (h : SmokeAdmitted query evidence) :
    GoldIsolationPreserved evidence := h.2.2.2.1

theorem admitted_boundary_preserved
    {query : Binding} {evidence : SmokeEvidence}
    (h : SmokeAdmitted query evidence) :
    BoundaryPreserved evidence := h.2.2.2.2

theorem controller_version_mismatch_forbids_admission
    {query : Binding} {evidence : SmokeEvidence}
    (hMismatch : evidence.plan.binding.controllerVersion ≠ query.controllerVersion) :
    ¬ SmokeAdmitted query evidence := by
  intro h
  exact hMismatch (congrArg Binding.controllerVersion (admitted_exact_binding h).1)

theorem unresolved_forbids_admission
    {query : Binding} {evidence : SmokeEvidence}
    (hUnresolved : evidence.observation.resolved = false) :
    ¬ SmokeAdmitted query evidence := by
  intro h
  have hResolved := (admitted_observation_verified h).2.2.2.2.2.2.2.1
  rw [hUnresolved] at hResolved
  contradiction

theorem solver_gold_exposure_forbids_admission
    {query : Binding} {evidence : SmokeEvidence}
    (hExposure : evidence.observation.goldExposedToSolver = true) :
    ¬ SmokeAdmitted query evidence := by
  intro h
  have hNoExposure := (admitted_gold_isolation h).2.1
  rw [hExposure] at hNoExposure
  contradiction

theorem candidate_generation_gold_use_forbids_admission
    {query : Binding} {evidence : SmokeEvidence}
    (hUse : evidence.observation.goldUsedForCandidateGeneration = true) :
    ¬ SmokeAdmitted query evidence := by
  intro h
  have hNoUse := (admitted_gold_isolation h).2.2.1
  rw [hUse] at hNoUse
  contradiction

theorem repair_memory_gold_use_forbids_admission
    {query : Binding} {evidence : SmokeEvidence}
    (hUse : evidence.observation.goldUsedForRepairMemory = true) :
    ¬ SmokeAdmitted query evidence := by
  intro h
  have hNoUse := (admitted_gold_isolation h).2.2.2
  rw [hUse] at hNoUse
  contradiction

theorem kernel_harness_execution_forbids_admission
    {query : Binding} {evidence : SmokeEvidence}
    (hExecution : evidence.observation.harnessExecutedByKernel = true) :
    ¬ SmokeAdmitted query evidence := by
  intro h
  have hNoExecution := (admitted_gold_isolation h).1
  rw [hExecution] at hNoExecution
  contradiction

theorem repository_mutation_forbids_admission
    {query : Binding} {evidence : SmokeEvidence}
    (hMutation : evidence.observation.repositoryMutated = true) :
    ¬ SmokeAdmitted query evidence := by
  intro h
  have hNoMutation := (admitted_boundary_preserved h).1
  rw [hMutation] at hNoMutation
  contradiction

def referenceBinding : Binding where
  controllerVersion := 1337
  predecessorManifest := 1
  predecessorPack := 2
  predecessorReceipt := 3
  datasetRevision := 4
  datasetArtifact := 5
  harnessVersion := 6
  instance := 20590
  smokeContract := 7
  environmentContract := 8

def referencePlan : SmokePlan where
  binding := referenceBinding
  preregistered := true
  goldPredictionMode := true
  evaluatorOnlyGold := true
  solverGoldAccess := false
  smokeRunCount := 1
  maximumWorkers := 1
  timeoutSeconds := 1800

def referenceObservation : SmokeObservation where
  binding := referenceBinding
  externalHarnessObserved := true
  harnessExecutedByKernel := false
  networkUsedByExternalHarness := true
  dockerUsed := true
  imageAvailable := true
  containerStarted := true
  goldPatchApplied := true
  evaluationCompleted := true
  resolved := true
  reportObserved := true
  logsObserved := true
  goldExposedToSolver := false
  goldUsedForCandidateGeneration := false
  goldUsedForRepairMemory := false
  repositoryMutated := false
  gitAuthority := false
  correctnessClaimed := false

def referenceEvidence : SmokeEvidence where
  plan := referencePlan
  observation := referenceObservation
  futureHarnessAuthority := false
  futureRepositoryMutationAuthority := false
  futureGitAuthority := false

def referenceUnresolved : SmokeEvidence :=
  { referenceEvidence with
    observation := { referenceObservation with resolved := false } }

def referenceGoldExposed : SmokeEvidence :=
  { referenceEvidence with
    observation := { referenceObservation with goldExposedToSolver := true } }

def referenceKernelExecution : SmokeEvidence :=
  { referenceEvidence with
    observation := { referenceObservation with harnessExecutedByKernel := true } }

theorem reference_admitted :
    SmokeAdmitted referenceBinding referenceEvidence := by
  simp [SmokeAdmitted, ExactBinding, PlanPreregistered, ObservationVerified,
    GoldIsolationPreserved, BoundaryPreserved, referenceBinding, referenceEvidence,
    referencePlan, referenceObservation]

theorem reference_unresolved_not_admitted :
    ¬ SmokeAdmitted referenceBinding referenceUnresolved := by
  exact unresolved_forbids_admission rfl

theorem reference_gold_exposed_not_admitted :
    ¬ SmokeAdmitted referenceBinding referenceGoldExposed := by
  exact solver_gold_exposure_forbids_admission rfl

theorem reference_kernel_execution_not_admitted :
    ¬ SmokeAdmitted referenceBinding referenceKernelExecution := by
  exact kernel_harness_execution_forbids_admission rfl

end KUOS.CodeAI.GoldPatchEnvironmentSmokeValidationV0_1
