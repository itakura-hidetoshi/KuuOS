import Mathlib

namespace KUOS.CodeAI.EnvironmentCapsuleLivelockEfficiencyGateV0_1

inductive SubtaskKind
  | localize
  | diagnose
  | edit
  | verify
  deriving DecidableEq, BEq

inductive SpecialistKind
  | formal
  | behavioral
  | adversarial
  | maintainability
  deriving DecidableEq, BEq

structure Binding where
  repositoryVersion : Nat
  sourceTree : Nat
  routerManifest : Nat
  routerPack : Nat
  routerReceipt : Nat
  selectedSpecialist : Nat
  selectedSpecialistKind : SpecialistKind
  selectedSubtask : SubtaskKind
  dependencySlice : Nat
  toolchain : Nat
  environmentContract : Nat
  progressContract : Nat
  gatePolicy : Nat
  deriving DecidableEq

structure EnvironmentCapsule where
  binding : Binding
  runnerImage : Nat
  operatingSystem : Nat
  architecture : Nat
  pythonToolchain : Nat
  leanToolchain : Nat
  dependencyManifest : Nat
  workflowDefinition : Nat
  environmentVariables : Nat
  rootFilesystemImmutable : Bool
  dependencyLockVerified : Bool
  capsuleComplete : Bool
  capsuleObserved : Bool
  selfReportOnly : Bool
  networkAccessAllowed : Bool
  deriving DecidableEq

structure ProgressMetrics where
  stepCount : Nat
  toolCallCount : Nat
  modelCallCount : Nat
  tokenUnits : Nat
  wallClockUnits : Nat
  failedActionCount : Nat
  totalProgressUnits : Nat
  distinctStateCount : Nat
  maximumNoProgressStreak : Nat
  repeatedZeroProgressTransitions : Nat
  cycleCount : Nat
  cycleDetected : Bool
  traceObservable : Bool
  traceComplete : Bool
  selfReportOnly : Bool
  deriving DecidableEq

structure Budget where
  maximumSteps : Nat
  maximumToolCalls : Nat
  maximumModelCalls : Nat
  maximumTokenUnits : Nat
  maximumWallClockUnits : Nat
  maximumFailedActions : Nat
  maximumNoProgressStreak : Nat
  maximumRepeatedZeroProgressTransitions : Nat
  maximumCycleCount : Nat
  minimumTotalProgressUnits : Nat
  minimumDistinctStateCount : Nat
  deriving DecidableEq

structure GateEvidence where
  capsule : EnvironmentCapsule
  progress : ProgressMetrics
  continuationHintOnly : Bool
  continuationAuthority : Bool
  executionAuthority : Bool
  repositoryMutated : Bool
  gitAuthority : Bool
  correctnessClaimed : Bool
  deriving DecidableEq

def BoundaryPreserved (evidence : GateEvidence) : Prop :=
  evidence.continuationHintOnly = true ∧
  evidence.continuationAuthority = false ∧
  evidence.executionAuthority = false ∧
  evidence.repositoryMutated = false ∧
  evidence.gitAuthority = false ∧
  evidence.correctnessClaimed = false


def CapsuleReproducible (query : Binding) (capsule : EnvironmentCapsule) : Prop :=
  capsule.binding = query ∧
  capsule.rootFilesystemImmutable = true ∧
  capsule.dependencyLockVerified = true ∧
  capsule.capsuleComplete = true ∧
  capsule.capsuleObserved = true ∧
  capsule.selfReportOnly = false ∧
  capsule.networkAccessAllowed = false


def TraceGrounded (progress : ProgressMetrics) : Prop :=
  progress.traceObservable = true ∧
  progress.traceComplete = true ∧
  progress.selfReportOnly = false


def LivelockFree (budget : Budget) (progress : ProgressMetrics) : Prop :=
  progress.cycleDetected = false ∧
  progress.cycleCount ≤ budget.maximumCycleCount ∧
  progress.repeatedZeroProgressTransitions ≤ budget.maximumRepeatedZeroProgressTransitions ∧
  progress.maximumNoProgressStreak ≤ budget.maximumNoProgressStreak


def Efficient (budget : Budget) (progress : ProgressMetrics) : Prop :=
  progress.stepCount ≤ budget.maximumSteps ∧
  progress.toolCallCount ≤ budget.maximumToolCalls ∧
  progress.modelCallCount ≤ budget.maximumModelCalls ∧
  progress.tokenUnits ≤ budget.maximumTokenUnits ∧
  progress.wallClockUnits ≤ budget.maximumWallClockUnits ∧
  progress.failedActionCount ≤ budget.maximumFailedActions ∧
  budget.minimumTotalProgressUnits ≤ progress.totalProgressUnits ∧
  budget.minimumDistinctStateCount ≤ progress.distinctStateCount


def GateAdmitted (query : Binding) (budget : Budget) (evidence : GateEvidence) : Prop :=
  CapsuleReproducible query evidence.capsule ∧
  TraceGrounded evidence.progress ∧
  LivelockFree budget evidence.progress ∧
  Efficient budget evidence.progress ∧
  BoundaryPreserved evidence


theorem admitted_exact_binding
    {query : Binding} {budget : Budget} {evidence : GateEvidence}
    (h : GateAdmitted query budget evidence) :
    evidence.capsule.binding = query := by
  exact h.1.1


theorem admitted_trace_grounded
    {query : Binding} {budget : Budget} {evidence : GateEvidence}
    (h : GateAdmitted query budget evidence) :
    TraceGrounded evidence.progress := by
  exact h.2.1


theorem admitted_livelock_free
    {query : Binding} {budget : Budget} {evidence : GateEvidence}
    (h : GateAdmitted query budget evidence) :
    LivelockFree budget evidence.progress := by
  exact h.2.2.1


theorem admitted_efficient
    {query : Binding} {budget : Budget} {evidence : GateEvidence}
    (h : GateAdmitted query budget evidence) :
    Efficient budget evidence.progress := by
  exact h.2.2.2.1


theorem admitted_boundary_preserved
    {query : Binding} {budget : Budget} {evidence : GateEvidence}
    (h : GateAdmitted query budget evidence) :
    BoundaryPreserved evidence := by
  exact h.2.2.2.2


theorem repository_version_mismatch_forbids_admission
    {query : Binding} {budget : Budget} {evidence : GateEvidence}
    (hMismatch : evidence.capsule.binding.repositoryVersion ≠ query.repositoryVersion) :
    ¬ GateAdmitted query budget evidence := by
  intro h
  exact hMismatch (congrArg Binding.repositoryVersion (admitted_exact_binding h))


theorem cycle_detected_forbids_admission
    {query : Binding} {budget : Budget} {evidence : GateEvidence}
    (hCycle : evidence.progress.cycleDetected = true) :
    ¬ GateAdmitted query budget evidence := by
  intro h
  have hNoCycle := (admitted_livelock_free h).1
  rw [hCycle] at hNoCycle
  contradiction


theorem repeated_zero_progress_excess_forbids_admission
    {query : Binding} {budget : Budget} {evidence : GateEvidence}
    (hExcess : budget.maximumRepeatedZeroProgressTransitions <
      evidence.progress.repeatedZeroProgressTransitions) :
    ¬ GateAdmitted query budget evidence := by
  intro h
  have hBound := (admitted_livelock_free h).2.2.1
  omega


theorem step_budget_excess_forbids_admission
    {query : Binding} {budget : Budget} {evidence : GateEvidence}
    (hExcess : budget.maximumSteps < evidence.progress.stepCount) :
    ¬ GateAdmitted query budget evidence := by
  intro h
  have hBound := (admitted_efficient h).1
  omega


theorem trace_self_report_only_forbids_admission
    {query : Binding} {budget : Budget} {evidence : GateEvidence}
    (hSelfReport : evidence.progress.selfReportOnly = true) :
    ¬ GateAdmitted query budget evidence := by
  intro h
  have hNoSelfReport := (admitted_trace_grounded h).2.2
  rw [hSelfReport] at hNoSelfReport
  contradiction


def referenceQuery : Binding where
  repositoryVersion := 1332
  sourceTree := 232
  routerManifest := 1
  routerPack := 2
  routerReceipt := 3
  selectedSpecialist := 4
  selectedSpecialistKind := .formal
  selectedSubtask := .verify
  dependencySlice := 5
  toolchain := 6
  environmentContract := 7
  progressContract := 8
  gatePolicy := 9


def referenceCapsule : EnvironmentCapsule where
  binding := referenceQuery
  runnerImage := 10
  operatingSystem := 11
  architecture := 12
  pythonToolchain := 13
  leanToolchain := 14
  dependencyManifest := 15
  workflowDefinition := 16
  environmentVariables := 17
  rootFilesystemImmutable := true
  dependencyLockVerified := true
  capsuleComplete := true
  capsuleObserved := true
  selfReportOnly := false
  networkAccessAllowed := false


def referenceProgress : ProgressMetrics where
  stepCount := 6
  toolCallCount := 9
  modelCallCount := 6
  tokenUnits := 46000
  wallClockUnits := 1380000
  failedActionCount := 0
  totalProgressUnits := 20
  distinctStateCount := 7
  maximumNoProgressStreak := 0
  repeatedZeroProgressTransitions := 0
  cycleCount := 0
  cycleDetected := false
  traceObservable := true
  traceComplete := true
  selfReportOnly := false


def referenceBudget : Budget where
  maximumSteps := 12
  maximumToolCalls := 20
  maximumModelCalls := 12
  maximumTokenUnits := 80000
  maximumWallClockUnits := 3600000
  maximumFailedActions := 2
  maximumNoProgressStreak := 2
  maximumRepeatedZeroProgressTransitions := 0
  maximumCycleCount := 0
  minimumTotalProgressUnits := 15
  minimumDistinctStateCount := 5


def referenceEvidence : GateEvidence where
  capsule := referenceCapsule
  progress := referenceProgress
  continuationHintOnly := true
  continuationAuthority := false
  executionAuthority := false
  repositoryMutated := false
  gitAuthority := false
  correctnessClaimed := false


def referenceCycle : GateEvidence :=
  { referenceEvidence with
    progress := { referenceProgress with cycleDetected := true, cycleCount := 1 } }


def referenceOverBudget : GateEvidence :=
  { referenceEvidence with
    progress := { referenceProgress with stepCount := 13 } }


def referenceSelfReport : GateEvidence :=
  { referenceEvidence with
    progress := { referenceProgress with selfReportOnly := true } }


theorem reference_admitted :
    GateAdmitted referenceQuery referenceBudget referenceEvidence := by
  norm_num [GateAdmitted, CapsuleReproducible, TraceGrounded, LivelockFree,
    Efficient, BoundaryPreserved, referenceQuery, referenceCapsule,
    referenceProgress, referenceBudget, referenceEvidence]


theorem reference_exact_environment :
    referenceEvidence.capsule.binding = referenceQuery := by
  exact admitted_exact_binding reference_admitted


theorem reference_livelock_free :
    LivelockFree referenceBudget referenceEvidence.progress := by
  exact admitted_livelock_free reference_admitted


theorem reference_efficient :
    Efficient referenceBudget referenceEvidence.progress := by
  exact admitted_efficient reference_admitted


theorem reference_preserves_boundary :
    BoundaryPreserved referenceEvidence := by
  exact admitted_boundary_preserved reference_admitted


theorem reference_cycle_not_admitted :
    ¬ GateAdmitted referenceQuery referenceBudget referenceCycle := by
  apply cycle_detected_forbids_admission
  rfl


theorem reference_over_budget_not_admitted :
    ¬ GateAdmitted referenceQuery referenceBudget referenceOverBudget := by
  apply step_budget_excess_forbids_admission
  norm_num [referenceBudget, referenceOverBudget, referenceEvidence, referenceProgress]


theorem reference_self_report_not_admitted :
    ¬ GateAdmitted referenceQuery referenceBudget referenceSelfReport := by
  apply trace_self_report_only_forbids_admission
  rfl

end KUOS.CodeAI.EnvironmentCapsuleLivelockEfficiencyGateV0_1
