import Mathlib

namespace KUOS
namespace OpenHorizon

structure DispatchCapacity where
  eligibleJobs : ℕ
  healthyWorkers : ℕ
  policyMaximum : ℕ
  assignments : ℕ
  boundedByJobs : assignments ≤ eligibleJobs
  boundedByWorkers : assignments ≤ healthyWorkers
  boundedByPolicy : assignments ≤ policyMaximum


theorem assignments_bounded_by_jobs (capacity : DispatchCapacity) :
    capacity.assignments ≤ capacity.eligibleJobs := by
  exact capacity.boundedByJobs


theorem assignments_bounded_by_workers (capacity : DispatchCapacity) :
    capacity.assignments ≤ capacity.healthyWorkers := by
  exact capacity.boundedByWorkers


theorem assignments_bounded_by_policy (capacity : DispatchCapacity) :
    capacity.assignments ≤ capacity.policyMaximum := by
  exact capacity.boundedByPolicy


structure DistinctCycleAssignments where
  workerIds : List String
  jobIds : List String
  workersDistinct : workerIds.Nodup
  jobsDistinct : jobIds.Nodup


theorem one_assignment_per_worker (assignments : DistinctCycleAssignments) :
    assignments.workerIds.Nodup := by
  exact assignments.workersDistinct


theorem one_assignment_per_job (assignments : DistinctCycleAssignments) :
    assignments.jobIds.Nodup := by
  exact assignments.jobsDistinct


structure ServiceProgress where
  before : ℕ
  after : ℕ
  monotone : before ≤ after


theorem service_count_monotone (progress : ServiceProgress) :
    progress.before ≤ progress.after := by
  exact progress.monotone


structure DeadLetterObservation where
  observationCount : ℕ
  threshold : ℕ
  quarantined : Bool
  quarantineRequiresThreshold : quarantined = true → threshold ≤ observationCount


theorem deadLetter_requires_threshold (observation : DeadLetterObservation)
    (h : observation.quarantined = true) :
    observation.threshold ≤ observation.observationCount := by
  exact observation.quarantineRequiresThreshold h


structure WorkerFreshness where
  age : ℕ
  ttl : ℕ
  dispatchable : Bool
  dispatchRequiresFreshness : dispatchable = true → age ≤ ttl


theorem dispatchable_worker_is_fresh (worker : WorkerFreshness)
    (h : worker.dispatchable = true) :
    worker.age ≤ worker.ttl := by
  exact worker.dispatchRequiresFreshness h


def recordPlan (processed : Finset ℕ) (digest : ℕ) : Finset ℕ :=
  insert digest processed


theorem recordPlan_idempotent (processed : Finset ℕ) (digest : ℕ) :
    recordPlan (recordPlan processed digest) digest = recordPlan processed digest := by
  simp [recordPlan]


structure OrchestratorHistory where
  cycles : ℕ
  receipts : ℕ
  aligned : cycles = receipts


def appendOrchestratorCycle (history : OrchestratorHistory) : OrchestratorHistory where
  cycles := history.cycles + 1
  receipts := history.receipts + 1
  aligned := by simp [history.aligned]


theorem orchestratorCycleHistory_strict (history : OrchestratorHistory) :
    history.cycles < (appendOrchestratorCycle history).cycles := by
  simp [appendOrchestratorCycle]


theorem orchestratorReceiptHistory_strict (history : OrchestratorHistory) :
    history.receipts < (appendOrchestratorCycle history).receipts := by
  simp [appendOrchestratorCycle]

end OpenHorizon
end KUOS
