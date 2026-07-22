import Mathlib

namespace KUOS.CodeAI.FrozenCohortPredictionPackExecutionShardContractV0_1

structure Contract where
  cohortCount : Nat
  targetPerCohort : Nat
  shardSize : Nat
  shardsPerCohort : Nat
  opaqueSlots : Bool
  sameSamples : Bool
  authenticPacksComplete : Bool
  smokeCountsAsPerformance : Bool
  labelOnlyRelabeling : Bool
  rawGoldVisible : Bool
  rawTestNamesVisible : Bool
  rawLogsVisible : Bool
  kernelExecutionAuthority : Bool
  repositoryMutationAuthority : Bool
  gitAuthority : Bool
  correctnessClaimed : Bool
  performanceClaimed : Bool
  externalExecutionReady : Bool
  deriving DecidableEq

def ContractAdmitted (c : Contract) : Prop :=
  c.cohortCount = 5 ∧
  c.targetPerCohort = 100 ∧
  c.shardSize = 10 ∧
  c.shardsPerCohort = 10 ∧
  c.opaqueSlots = true ∧
  c.sameSamples = true ∧
  c.smokeCountsAsPerformance = false ∧
  c.labelOnlyRelabeling = false ∧
  c.rawGoldVisible = false ∧
  c.rawTestNamesVisible = false ∧
  c.rawLogsVisible = false ∧
  c.kernelExecutionAuthority = false ∧
  c.repositoryMutationAuthority = false ∧
  c.gitAuthority = false ∧
  c.correctnessClaimed = false ∧
  c.performanceClaimed = false

theorem label_only_relabeling_forbids_admission
    {c : Contract} (h : c.labelOnlyRelabeling = true) : ¬ ContractAdmitted c := by
  intro ha
  rw [h] at ha
  simp [ContractAdmitted] at ha

theorem smoke_as_performance_forbids_admission
    {c : Contract} (h : c.smokeCountsAsPerformance = true) : ¬ ContractAdmitted c := by
  intro ha
  rw [h] at ha
  simp [ContractAdmitted] at ha

theorem raw_gold_forbids_admission
    {c : Contract} (h : c.rawGoldVisible = true) : ¬ ContractAdmitted c := by
  intro ha
  rw [h] at ha
  simp [ContractAdmitted] at ha

theorem kernel_execution_forbids_admission
    {c : Contract} (h : c.kernelExecutionAuthority = true) : ¬ ContractAdmitted c := by
  intro ha
  rw [h] at ha
  simp [ContractAdmitted] at ha

theorem repository_mutation_forbids_admission
    {c : Contract} (h : c.repositoryMutationAuthority = true) : ¬ ContractAdmitted c := by
  intro ha
  rw [h] at ha
  simp [ContractAdmitted] at ha

theorem performance_claim_forbids_admission
    {c : Contract} (h : c.performanceClaimed = true) : ¬ ContractAdmitted c := by
  intro ha
  rw [h] at ha
  simp [ContractAdmitted] at ha

def referenceContract : Contract where
  cohortCount := 5
  targetPerCohort := 100
  shardSize := 10
  shardsPerCohort := 10
  opaqueSlots := true
  sameSamples := true
  authenticPacksComplete := false
  smokeCountsAsPerformance := false
  labelOnlyRelabeling := false
  rawGoldVisible := false
  rawTestNamesVisible := false
  rawLogsVisible := false
  kernelExecutionAuthority := false
  repositoryMutationAuthority := false
  gitAuthority := false
  correctnessClaimed := false
  performanceClaimed := false
  externalExecutionReady := false

theorem reference_contract_admitted : ContractAdmitted referenceContract := by
  native_decide

theorem reference_not_execution_ready : referenceContract.externalExecutionReady = false := rfl

theorem reference_packs_pending : referenceContract.authenticPacksComplete = false := rfl

end KUOS.CodeAI.FrozenCohortPredictionPackExecutionShardContractV0_1
