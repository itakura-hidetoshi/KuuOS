import Mathlib

namespace KUOS.CodeAI.TrajectoryGroundedSpecialistRouterAdmissionV0_1

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
  memoryPack : Nat
  memoryReceipt : Nat
  subtaskKind : SubtaskKind
  subtaskContract : Nat
  predecessorOutput : Nat
  dependencySlice : Nat
  toolchain : Nat
  environment : Nat
  trajectoryContract : Nat
  routingPolicy : Nat
  deriving DecidableEq

structure Measurement where
  explorationTurns : Nat
  observationCount : Nat
  executionSignalCount : Nat
  groundingSourceCount : Nat
  observableArtifactCount : Nat
  selfReportOnly : Bool
  measurementComplete : Bool
  repositoryStateObserved : Bool
  testsObserved : Bool
  deriving DecidableEq

structure SpecialistEvidence where
  specialistKind : SpecialistKind
  supportedSubtask : SubtaskKind
  binding : Binding
  measurement : Measurement
  fitScore : Nat
  reliabilityScore : Nat
  estimatedCostUnits : Nat
  independentMeasurement : Bool
  routeHintOnly : Bool
  repositoryMutated : Bool
  specialistDispatched : Bool
  candidateSelected : Bool
  executionAuthority : Bool
  gitAuthority : Bool
  correctnessClaimed : Bool
  deriving DecidableEq

def BoundaryPreserved (evidence : SpecialistEvidence) : Prop :=
  evidence.routeHintOnly = true ∧
  evidence.repositoryMutated = false ∧
  evidence.specialistDispatched = false ∧
  evidence.candidateSelected = false ∧
  evidence.executionAuthority = false ∧
  evidence.gitAuthority = false ∧
  evidence.correctnessClaimed = false

def MeasurementGrounded
    (minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts : Nat)
    (measurement : Measurement) : Prop :=
  minimumTurns ≤ measurement.explorationTurns ∧
  minimumObservations ≤ measurement.observationCount ∧
  minimumExecutionSignals ≤ measurement.executionSignalCount ∧
  minimumGroundingSources ≤ measurement.groundingSourceCount ∧
  minimumObservableArtifacts ≤ measurement.observableArtifactCount ∧
  measurement.selfReportOnly = false ∧
  measurement.measurementComplete = true ∧
  measurement.repositoryStateObserved = true ∧
  measurement.testsObserved = true

def Utility (evidence : SpecialistEvidence) : Nat :=
  evidence.fitScore + evidence.reliabilityScore - evidence.estimatedCostUnits

def AdmissibleCandidate
    (query : Binding)
    (minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts minimumFit
      minimumReliability maximumCost : Nat)
    (evidence : SpecialistEvidence) : Prop :=
  evidence.binding = query ∧
  evidence.supportedSubtask = query.subtaskKind ∧
  MeasurementGrounded minimumTurns minimumObservations minimumExecutionSignals
    minimumGroundingSources minimumObservableArtifacts evidence.measurement ∧
  evidence.independentMeasurement = true ∧
  minimumFit ≤ evidence.fitScore ∧
  minimumReliability ≤ evidence.reliabilityScore ∧
  evidence.estimatedCostUnits ≤ maximumCost ∧
  BoundaryPreserved evidence

def Dominates
    (minimumMargin : Nat)
    (selected alternative : SpecialistEvidence) : Prop :=
  Utility selected ≥ Utility alternative + minimumMargin

def RouteAdmitted
    (query : Binding)
    (minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts minimumFit
      minimumReliability maximumCost minimumMargin : Nat)
    (selected : SpecialistEvidence)
    (alternatives : List SpecialistEvidence) : Prop :=
  AdmissibleCandidate query minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts minimumFit minimumReliability
      maximumCost selected ∧
  ∀ alternative ∈ alternatives, Dominates minimumMargin selected alternative

theorem admitted_exact_binding
    {query : Binding}
    {minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts minimumFit
      minimumReliability maximumCost minimumMargin : Nat}
    {selected : SpecialistEvidence}
    {alternatives : List SpecialistEvidence}
    (h : RouteAdmitted query minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts minimumFit minimumReliability
      maximumCost minimumMargin selected alternatives) :
    selected.binding = query := by
  rcases h.1 with ⟨hBinding, _, _, _, _, _, _, _⟩
  exact hBinding

theorem admitted_measurement_grounded
    {query : Binding}
    {minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts minimumFit
      minimumReliability maximumCost minimumMargin : Nat}
    {selected : SpecialistEvidence}
    {alternatives : List SpecialistEvidence}
    (h : RouteAdmitted query minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts minimumFit minimumReliability
      maximumCost minimumMargin selected alternatives) :
    MeasurementGrounded minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts selected.measurement := by
  rcases h.1 with ⟨_, _, hMeasurement, _, _, _, _, _⟩
  exact hMeasurement

theorem admitted_boundary_preserved
    {query : Binding}
    {minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts minimumFit
      minimumReliability maximumCost minimumMargin : Nat}
    {selected : SpecialistEvidence}
    {alternatives : List SpecialistEvidence}
    (h : RouteAdmitted query minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts minimumFit minimumReliability
      maximumCost minimumMargin selected alternatives) :
    BoundaryPreserved selected := by
  rcases h.1 with ⟨_, _, _, _, _, _, _, hBoundary⟩
  exact hBoundary

theorem admitted_not_self_report_only
    {query : Binding}
    {minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts minimumFit
      minimumReliability maximumCost minimumMargin : Nat}
    {selected : SpecialistEvidence}
    {alternatives : List SpecialistEvidence}
    (h : RouteAdmitted query minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts minimumFit minimumReliability
      maximumCost minimumMargin selected alternatives) :
    selected.measurement.selfReportOnly = false := by
  rcases admitted_measurement_grounded h with ⟨_, _, _, _, _, hNoSelfReport, _, _, _⟩
  exact hNoSelfReport

theorem repository_version_mismatch_forbids_candidate
    {query : Binding}
    {minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts minimumFit
      minimumReliability maximumCost : Nat}
    {evidence : SpecialistEvidence}
    (hMismatch : evidence.binding.repositoryVersion ≠ query.repositoryVersion) :
    ¬ AdmissibleCandidate query minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts minimumFit minimumReliability
      maximumCost evidence := by
  intro h
  rcases h with ⟨hBinding, _, _, _, _, _, _, _⟩
  exact hMismatch (congrArg Binding.repositoryVersion hBinding)

theorem self_report_only_forbids_candidate
    {query : Binding}
    {minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts minimumFit
      minimumReliability maximumCost : Nat}
    {evidence : SpecialistEvidence}
    (hSelfReport : evidence.measurement.selfReportOnly = true) :
    ¬ AdmissibleCandidate query minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts minimumFit minimumReliability
      maximumCost evidence := by
  intro h
  rcases h with ⟨_, _, hMeasurement, _, _, _, _, _⟩
  rcases hMeasurement with ⟨_, _, _, _, _, hNoSelfReport, _, _, _⟩
  rw [hSelfReport] at hNoSelfReport
  contradiction

theorem incomplete_measurement_forbids_candidate
    {query : Binding}
    {minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts minimumFit
      minimumReliability maximumCost : Nat}
    {evidence : SpecialistEvidence}
    (hIncomplete : evidence.measurement.measurementComplete = false) :
    ¬ AdmissibleCandidate query minimumTurns minimumObservations minimumExecutionSignals
      minimumGroundingSources minimumObservableArtifacts minimumFit minimumReliability
      maximumCost evidence := by
  intro h
  rcases h with ⟨_, _, hMeasurement, _, _, _, _, _⟩
  rcases hMeasurement with ⟨_, _, _, _, _, _, hComplete, _, _⟩
  rw [hIncomplete] at hComplete
  contradiction

def referenceQuery : Binding where
  repositoryVersion := 1331
  sourceTree := 231
  memoryPack := 1
  memoryReceipt := 2
  subtaskKind := .verify
  subtaskContract := 3
  predecessorOutput := 4
  dependencySlice := 5
  toolchain := 6
  environment := 7
  trajectoryContract := 8
  routingPolicy := 9

def referenceMeasurement : Measurement where
  explorationTurns := 4
  observationCount := 7
  executionSignalCount := 2
  groundingSourceCount := 3
  observableArtifactCount := 4
  selfReportOnly := false
  measurementComplete := true
  repositoryStateObserved := true
  testsObserved := true

def referenceFormal : SpecialistEvidence where
  specialistKind := .formal
  supportedSubtask := .verify
  binding := referenceQuery
  measurement := referenceMeasurement
  fitScore := 95
  reliabilityScore := 94
  estimatedCostUnits := 35
  independentMeasurement := true
  routeHintOnly := true
  repositoryMutated := false
  specialistDispatched := false
  candidateSelected := false
  executionAuthority := false
  gitAuthority := false
  correctnessClaimed := false

def referenceBehavioral : SpecialistEvidence where
  specialistKind := .behavioral
  supportedSubtask := .verify
  binding := referenceQuery
  measurement := referenceMeasurement
  fitScore := 88
  reliabilityScore := 90
  estimatedCostUnits := 30
  independentMeasurement := true
  routeHintOnly := true
  repositoryMutated := false
  specialistDispatched := false
  candidateSelected := false
  executionAuthority := false
  gitAuthority := false
  correctnessClaimed := false

def referenceAdversarial : SpecialistEvidence where
  specialistKind := .adversarial
  supportedSubtask := .verify
  binding := referenceQuery
  measurement := referenceMeasurement
  fitScore := 84
  reliabilityScore := 87
  estimatedCostUnits := 28
  independentMeasurement := true
  routeHintOnly := true
  repositoryMutated := false
  specialistDispatched := false
  candidateSelected := false
  executionAuthority := false
  gitAuthority := false
  correctnessClaimed := false

def referenceMaintainability : SpecialistEvidence where
  specialistKind := .maintainability
  supportedSubtask := .verify
  binding := referenceQuery
  measurement := referenceMeasurement
  fitScore := 80
  reliabilityScore := 86
  estimatedCostUnits := 25
  independentMeasurement := true
  routeHintOnly := true
  repositoryMutated := false
  specialistDispatched := false
  candidateSelected := false
  executionAuthority := false
  gitAuthority := false
  correctnessClaimed := false

def referenceAlternatives : List SpecialistEvidence :=
  [referenceBehavioral, referenceAdversarial, referenceMaintainability]

def referenceSelfReport : SpecialistEvidence :=
  { referenceFormal with
    measurement := { referenceMeasurement with selfReportOnly := true } }

theorem referenceFormal_admitted :
    RouteAdmitted referenceQuery 3 5 1 3 3 80 80 40 5
      referenceFormal referenceAlternatives := by
  constructor
  · norm_num [AdmissibleCandidate, MeasurementGrounded, BoundaryPreserved,
      referenceFormal, referenceMeasurement, referenceQuery]
  · intro alternative hAlternative
    simp [referenceAlternatives] at hAlternative
    rcases hAlternative with rfl | rfl | rfl
    · norm_num [Dominates, Utility, referenceFormal, referenceBehavioral]
    · norm_num [Dominates, Utility, referenceFormal, referenceAdversarial]
    · norm_num [Dominates, Utility, referenceFormal, referenceMaintainability]

theorem referenceFormal_measurement_grounded :
    MeasurementGrounded 3 5 1 3 3 referenceFormal.measurement := by
  exact admitted_measurement_grounded referenceFormal_admitted

theorem referenceFormal_preserves_boundary :
    BoundaryPreserved referenceFormal := by
  exact admitted_boundary_preserved referenceFormal_admitted

theorem referenceFormal_not_dispatched :
    referenceFormal.specialistDispatched = false := by
  exact referenceFormal_preserves_boundary.2.2.1

theorem referenceSelfReport_not_admissible :
    ¬ AdmissibleCandidate referenceQuery 3 5 1 3 3 80 80 40 referenceSelfReport := by
  apply self_report_only_forbids_candidate
  rfl

end KUOS.CodeAI.TrajectoryGroundedSpecialistRouterAdmissionV0_1
