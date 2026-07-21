import Mathlib

namespace KUOS.CodeAI.ExternalGeneralBenchmarkSWEBenchVerifiedAdapterV0_1

inductive BenchmarkKind
  | sweBenchVerified
  deriving DecidableEq, BEq

structure Binding where
  controllerVersion : Nat
  sourceTree : Nat
  benchmarkContract : Nat
  runPlan : Nat
  modelConfiguration : Nat
  codeaiPipeline : Nat
  harnessContract : Nat
  evaluationProtocol : Nat
  deriving DecidableEq

structure BenchmarkContract where
  binding : Binding
  benchmarkKind : BenchmarkKind
  expectedInstanceCount : Nat
  corpusFrozen : Bool
  harnessPinned : Bool
  containerizedHarness : Bool
  officialPredictionShape : Bool
  protectedTestPathsSealed : Bool
  deriving DecidableEq

structure RunPlan where
  sampleCount : Nat
  selectionFrozen : Bool
  holdoutLabelsExposed : Bool
  goldPatchesExposed : Bool
  harnessExecutionRequested : Bool
  deriving DecidableEq

structure PredictionEvidence where
  predictionCount : Nat
  uniqueInstances : Bool
  officialShape : Bool
  patchDigestsValid : Bool
  changedPathsDerived : Bool
  protectedTestPathOverlap : Bool
  withinBudget : Bool
  deriving DecidableEq

structure AdapterEvidence where
  contract : BenchmarkContract
  plan : RunPlan
  predictions : PredictionEvidence
  protocolProjectionOnly : Bool
  harnessExecuted : Bool
  benchmarkResultIngested : Bool
  networkAccessed : Bool
  secretsAccessed : Bool
  repositoryMutated : Bool
  gitAuthority : Bool
  correctnessClaimed : Bool
  deriving DecidableEq

def ContractExact (query : Binding) (contract : BenchmarkContract) : Prop :=
  contract.binding = query ∧
  contract.benchmarkKind = .sweBenchVerified ∧
  contract.expectedInstanceCount = 500 ∧
  contract.corpusFrozen = true ∧
  contract.harnessPinned = true ∧
  contract.containerizedHarness = true ∧
  contract.officialPredictionShape = true ∧
  contract.protectedTestPathsSealed = true

def PlanFrozen (plan : RunPlan) : Prop :=
  0 < plan.sampleCount ∧
  plan.sampleCount ≤ 500 ∧
  plan.selectionFrozen = true ∧
  plan.holdoutLabelsExposed = false ∧
  plan.goldPatchesExposed = false ∧
  plan.harnessExecutionRequested = false

def PredictionsAdmissible (plan : RunPlan) (predictions : PredictionEvidence) : Prop :=
  predictions.predictionCount = plan.sampleCount ∧
  predictions.uniqueInstances = true ∧
  predictions.officialShape = true ∧
  predictions.patchDigestsValid = true ∧
  predictions.changedPathsDerived = true ∧
  predictions.protectedTestPathOverlap = false ∧
  predictions.withinBudget = true

def BoundaryPreserved (evidence : AdapterEvidence) : Prop :=
  evidence.protocolProjectionOnly = true ∧
  evidence.harnessExecuted = false ∧
  evidence.benchmarkResultIngested = false ∧
  evidence.networkAccessed = false ∧
  evidence.secretsAccessed = false ∧
  evidence.repositoryMutated = false ∧
  evidence.gitAuthority = false ∧
  evidence.correctnessClaimed = false

def AdapterAdmitted (query : Binding) (evidence : AdapterEvidence) : Prop :=
  ContractExact query evidence.contract ∧
  PlanFrozen evidence.plan ∧
  PredictionsAdmissible evidence.plan evidence.predictions ∧
  BoundaryPreserved evidence

theorem admitted_exact_binding
    {query : Binding} {evidence : AdapterEvidence}
    (h : AdapterAdmitted query evidence) :
    evidence.contract.binding = query := by
  exact h.1.1

theorem admitted_official_verified_count
    {query : Binding} {evidence : AdapterEvidence}
    (h : AdapterAdmitted query evidence) :
    evidence.contract.expectedInstanceCount = 500 := by
  exact h.1.2.2.1

theorem admitted_sample_frozen
    {query : Binding} {evidence : AdapterEvidence}
    (h : AdapterAdmitted query evidence) :
    evidence.plan.selectionFrozen = true := by
  exact h.2.1.2.2.1

theorem admitted_holdout_hidden
    {query : Binding} {evidence : AdapterEvidence}
    (h : AdapterAdmitted query evidence) :
    evidence.plan.holdoutLabelsExposed = false := by
  exact h.2.1.2.2.2.1

theorem admitted_protected_paths_nonoverlap
    {query : Binding} {evidence : AdapterEvidence}
    (h : AdapterAdmitted query evidence) :
    evidence.predictions.protectedTestPathOverlap = false := by
  exact h.2.2.1.2.2.2.2.2.1

theorem admitted_boundary_preserved
    {query : Binding} {evidence : AdapterEvidence}
    (h : AdapterAdmitted query evidence) :
    BoundaryPreserved evidence := by
  exact h.2.2.2

theorem controller_version_mismatch_forbids_admission
    {query : Binding} {evidence : AdapterEvidence}
    (hMismatch :
      evidence.contract.binding.controllerVersion ≠ query.controllerVersion) :
    ¬ AdapterAdmitted query evidence := by
  intro h
  exact hMismatch (congrArg Binding.controllerVersion (admitted_exact_binding h))

theorem holdout_exposure_forbids_admission
    {query : Binding} {evidence : AdapterEvidence}
    (hExposed : evidence.plan.holdoutLabelsExposed = true) :
    ¬ AdapterAdmitted query evidence := by
  intro h
  have hHidden := admitted_holdout_hidden h
  rw [hExposed] at hHidden
  contradiction

theorem protected_test_path_overlap_forbids_admission
    {query : Binding} {evidence : AdapterEvidence}
    (hOverlap : evidence.predictions.protectedTestPathOverlap = true) :
    ¬ AdapterAdmitted query evidence := by
  intro h
  have hNoOverlap := admitted_protected_paths_nonoverlap h
  rw [hOverlap] at hNoOverlap
  contradiction

theorem harness_execution_forbids_admission
    {query : Binding} {evidence : AdapterEvidence}
    (hExecuted : evidence.harnessExecuted = true) :
    ¬ AdapterAdmitted query evidence := by
  intro h
  have hBoundary := admitted_boundary_preserved h
  have hNotExecuted := hBoundary.2.1
  rw [hExecuted] at hNotExecuted
  contradiction

def referenceQuery : Binding where
  controllerVersion := 1334
  sourceTree := 1
  benchmarkContract := 2
  runPlan := 3
  modelConfiguration := 4
  codeaiPipeline := 5
  harnessContract := 6
  evaluationProtocol := 7

def referenceContract : BenchmarkContract where
  binding := referenceQuery
  benchmarkKind := .sweBenchVerified
  expectedInstanceCount := 500
  corpusFrozen := true
  harnessPinned := true
  containerizedHarness := true
  officialPredictionShape := true
  protectedTestPathsSealed := true

def referencePlan : RunPlan where
  sampleCount := 3
  selectionFrozen := true
  holdoutLabelsExposed := false
  goldPatchesExposed := false
  harnessExecutionRequested := false

def referencePredictions : PredictionEvidence where
  predictionCount := 3
  uniqueInstances := true
  officialShape := true
  patchDigestsValid := true
  changedPathsDerived := true
  protectedTestPathOverlap := false
  withinBudget := true

def referenceEvidence : AdapterEvidence where
  contract := referenceContract
  plan := referencePlan
  predictions := referencePredictions
  protocolProjectionOnly := true
  harnessExecuted := false
  benchmarkResultIngested := false
  networkAccessed := false
  secretsAccessed := false
  repositoryMutated := false
  gitAuthority := false
  correctnessClaimed := false

def referenceHoldoutLeak : AdapterEvidence :=
  { referenceEvidence with
    plan := { referencePlan with holdoutLabelsExposed := true } }

def referenceProtectedPathOverlap : AdapterEvidence :=
  { referenceEvidence with
    predictions := {
      referencePredictions with protectedTestPathOverlap := true
    } }

def referenceHarnessExecution : AdapterEvidence :=
  { referenceEvidence with harnessExecuted := true }

theorem reference_admitted : AdapterAdmitted referenceQuery referenceEvidence := by
  simp [
    AdapterAdmitted,
    ContractExact,
    PlanFrozen,
    PredictionsAdmissible,
    BoundaryPreserved,
    referenceEvidence,
    referenceContract,
    referencePlan,
    referencePredictions,
    referenceQuery
  ]

theorem reference_holdout_leak_not_admitted :
    ¬ AdapterAdmitted referenceQuery referenceHoldoutLeak := by
  apply holdout_exposure_forbids_admission
  rfl

theorem reference_protected_path_overlap_not_admitted :
    ¬ AdapterAdmitted referenceQuery referenceProtectedPathOverlap := by
  apply protected_test_path_overlap_forbids_admission
  rfl

theorem reference_harness_execution_not_admitted :
    ¬ AdapterAdmitted referenceQuery referenceHarnessExecution := by
  apply harness_execution_forbids_admission
  rfl

end KUOS.CodeAI.ExternalGeneralBenchmarkSWEBenchVerifiedAdapterV0_1
