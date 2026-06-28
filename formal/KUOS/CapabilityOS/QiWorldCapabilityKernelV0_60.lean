import Mathlib
import KUOS.Architecture.QiWorldYinYangProcessBlockerComplementarityV2_3

namespace KUOS.CapabilityOS

structure QiWorldCapabilityState where
  qiIntensity : Nat
  qiCapacity : Nat
  requiredGuards : KUOS.Architecture.CrossCycleBlockerVector
  activeGuards : KUOS.Architecture.CrossCycleBlockerVector
  processTensorVisible : Bool
  transitionContinuityVisible : Bool
  memoryContinuityVisible : Bool
  worldPreconditionsSupported : Bool
  verifierAvailable : Bool
  noActiveImpediment : Bool
  contextAllowsCandidateFlow : Bool
  worldCandidateCount : Nat
  worldCollapsed : Bool
  grantsPlanActivation : Bool
  grantsExecution : Bool
  grantsTruth : Bool
  grantsCausalAuthority : Bool
  grantsWorldCommit : Bool
  grantsBlockerDischarge : Bool
  overwritesMemory : Bool
  automaticLearning : Bool
  no_world_collapse : worldCollapsed = false
  no_plan_activation : grantsPlanActivation = false
  no_execution_authority : grantsExecution = false
  no_truth_authority : grantsTruth = false
  no_causal_authority : grantsCausalAuthority = false
  no_world_commit : grantsWorldCommit = false
  no_blocker_discharge : grantsBlockerDischarge = false
  no_memory_overwrite : overwritesMemory = false
  no_automatic_learning : automaticLearning = false

namespace QiWorldCapabilityState

variable (state : QiWorldCapabilityState)

def GuardSatisfied : Prop :=
  KUOS.Architecture.BlockerLe state.requiredGuards state.activeGuards


def ProcessVisible : Prop :=
  state.processTensorVisible = true ∧
    state.transitionContinuityVisible = true ∧
    state.memoryContinuityVisible = true


def WithinCapacity : Prop :=
  state.qiIntensity ≤ state.qiCapacity


structure Ready : Prop where
  processVisible : state.ProcessVisible
  guardsSatisfied : state.GuardSatisfied
  withinCapacity : state.WithinCapacity
  worldSupported : state.worldPreconditionsSupported = true
  verifierPresent : state.verifierAvailable = true
  noImpediment : state.noActiveImpediment = true
  contextAllows : state.contextAllowsCandidateFlow = true


noncomputable def effectiveCapability : Nat := by
  classical
  exact if state.Ready then state.qiIntensity else 0


theorem effectiveCapability_eq_of_ready
    (ready : state.Ready) :
    state.effectiveCapability = state.qiIntensity := by
  simp [effectiveCapability, ready]


theorem effectiveCapability_zero_of_not_ready
    (notReady : ¬state.Ready) :
    state.effectiveCapability = 0 := by
  simp [effectiveCapability, notReady]


theorem missing_guard_implies_zero_effective_capability
    (loss : ∃ guard,
      state.requiredGuards guard = true ∧
        state.activeGuards guard = false) :
    state.effectiveCapability = 0 := by
  apply state.effectiveCapability_zero_of_not_ready
  intro ready
  rcases loss with ⟨guard, required, inactive⟩
  have active := ready.guardsSatisfied guard required
  rw [inactive] at active
  cases active


theorem capacity_overflow_implies_containment
    (overflow : state.qiCapacity < state.qiIntensity) :
    state.effectiveCapability = 0 := by
  apply state.effectiveCapability_zero_of_not_ready
  intro ready
  exact (Nat.not_le_of_gt overflow) ready.withinCapacity


theorem active_impediment_implies_nonready
    (active : state.noActiveImpediment = false) :
    state.effectiveCapability = 0 := by
  apply state.effectiveCapability_zero_of_not_ready
  intro ready
  have noImpediment := ready.noImpediment
  rw [active] at noImpediment
  cases noImpediment


theorem verifier_absence_implies_hold
    (absent : state.verifierAvailable = false) :
    state.effectiveCapability = 0 := by
  apply state.effectiveCapability_zero_of_not_ready
  intro ready
  have verifierPresent := ready.verifierPresent
  rw [absent] at verifierPresent
  cases verifierPresent


theorem unsupported_world_implies_nonready
    (unsupported : state.worldPreconditionsSupported = false) :
    state.effectiveCapability = 0 := by
  apply state.effectiveCapability_zero_of_not_ready
  intro ready
  have worldSupported := ready.worldSupported
  rw [unsupported] at worldSupported
  cases worldSupported


theorem ready_flow_preserves_non_authority
    (ready : state.Ready) :
    state.effectiveCapability = state.qiIntensity ∧
      state.grantsPlanActivation = false ∧
      state.grantsExecution = false ∧
      state.grantsTruth = false ∧
      state.grantsCausalAuthority = false ∧
      state.grantsWorldCommit = false ∧
      state.grantsBlockerDischarge = false ∧
      state.overwritesMemory = false ∧
      state.automaticLearning = false ∧
      state.worldCollapsed = false := by
  exact ⟨state.effectiveCapability_eq_of_ready ready,
    state.no_plan_activation,
    state.no_execution_authority,
    state.no_truth_authority,
    state.no_causal_authority,
    state.no_world_commit,
    state.no_blocker_discharge,
    state.no_memory_overwrite,
    state.no_automatic_learning,
    state.no_world_collapse⟩

end QiWorldCapabilityState


structure CapabilityCandidateReceipt where
  state : QiWorldCapabilityState
  candidateOnly : Bool
  qiSupportIsNotTruth : Bool
  protectiveGuardIsNotImpediment : Bool
  worldImaginationOnly : Bool
  worldImaginationMutatesWorld : Bool
  worldPluralityPreserved : Bool
  memoryRetrievalActivatesPlan : Bool
  dispositionActivatesPlan : Bool
  learningFutureOnly : Bool
  candidate_only : candidateOnly = true
  qi_not_truth : qiSupportIsNotTruth = true
  guard_impediment_separated : protectiveGuardIsNotImpediment = true
  imagination_only : worldImaginationOnly = true
  no_world_imagination_mutation : worldImaginationMutatesWorld = false
  plurality_preserved : worldPluralityPreserved = true
  retrieval_not_activation : memoryRetrievalActivatesPlan = false
  disposition_not_activation : dispositionActivatesPlan = false
  future_only_learning : learningFutureOnly = true


namespace CapabilityCandidateReceipt

variable (receipt : CapabilityCandidateReceipt)


theorem world_imagination_does_not_mutate_world :
    receipt.worldImaginationOnly = true ∧
      receipt.worldImaginationMutatesWorld = false ∧
      receipt.state.grantsWorldCommit = false := by
  exact ⟨receipt.imagination_only,
    receipt.no_world_imagination_mutation,
    receipt.state.no_world_commit⟩


theorem world_plurality_is_preserved :
    receipt.worldPluralityPreserved = true ∧
      receipt.state.worldCollapsed = false := by
  exact ⟨receipt.plurality_preserved, receipt.state.no_world_collapse⟩


theorem capability_disposition_not_plan_activation :
    receipt.dispositionActivatesPlan = false ∧
      receipt.state.grantsPlanActivation = false := by
  exact ⟨receipt.disposition_not_activation,
    receipt.state.no_plan_activation⟩


theorem qi_world_capability_boundary
    (ready : receipt.state.Ready) :
    receipt.candidateOnly = true ∧
      receipt.qiSupportIsNotTruth = true ∧
      receipt.protectiveGuardIsNotImpediment = true ∧
      receipt.worldImaginationMutatesWorld = false ∧
      receipt.worldPluralityPreserved = true ∧
      receipt.memoryRetrievalActivatesPlan = false ∧
      receipt.dispositionActivatesPlan = false ∧
      receipt.learningFutureOnly = true ∧
      receipt.state.effectiveCapability = receipt.state.qiIntensity ∧
      receipt.state.grantsPlanActivation = false ∧
      receipt.state.grantsExecution = false ∧
      receipt.state.grantsTruth = false ∧
      receipt.state.grantsCausalAuthority = false ∧
      receipt.state.grantsWorldCommit = false ∧
      receipt.state.grantsBlockerDischarge = false ∧
      receipt.state.overwritesMemory = false ∧
      receipt.state.automaticLearning = false ∧
      receipt.state.worldCollapsed = false := by
  rcases receipt.state.ready_flow_preserves_non_authority ready with
    ⟨effective, plan, execution, truth, causal, worldCommit,
      blocker, memory, learning, collapse⟩
  exact ⟨receipt.candidate_only,
    receipt.qi_not_truth,
    receipt.guard_impediment_separated,
    receipt.no_world_imagination_mutation,
    receipt.plurality_preserved,
    receipt.retrieval_not_activation,
    receipt.disposition_not_activation,
    receipt.future_only_learning,
    effective,
    plan,
    execution,
    truth,
    causal,
    worldCommit,
    blocker,
    memory,
    learning,
    collapse⟩

end CapabilityCandidateReceipt


structure CapabilityPathState where
  leftSupport : Nat
  rightSupport : Nat
  allComponentsReady : Bool
  guardMeetSatisfied : Bool
  noImpedimentJoin : Bool
  grantsPlanActivation : Bool
  grantsExecution : Bool
  no_plan_activation : grantsPlanActivation = false
  no_execution_authority : grantsExecution = false


namespace CapabilityPathState

variable (path : CapabilityPathState)


def Ready : Prop :=
  path.allComponentsReady = true ∧
    path.guardMeetSatisfied = true ∧
    path.noImpedimentJoin = true


noncomputable def effectivePathSupport : Nat := by
  classical
  exact if path.Ready then min path.leftSupport path.rightSupport else 0


theorem effectivePathSupport_le_left :
    path.effectivePathSupport ≤ path.leftSupport := by
  classical
  by_cases ready : path.Ready
  · simp [effectivePathSupport, ready]
  · simp [effectivePathSupport, ready]


theorem effectivePathSupport_le_right :
    path.effectivePathSupport ≤ path.rightSupport := by
  classical
  by_cases ready : path.Ready
  · simp [effectivePathSupport, ready]
  · simp [effectivePathSupport, ready]


theorem missing_path_guard_cannot_be_repaired_by_strong_component
    (missing : path.guardMeetSatisfied = false) :
    path.effectivePathSupport = 0 := by
  classical
  simp only [effectivePathSupport]
  split
  · rename_i ready
    exact False.elim (by
      rcases ready with ⟨_, guard, _⟩
      rw [missing] at guard
      cases guard)
  · rfl


theorem active_path_impediment_cannot_be_repaired_by_strong_component
    (active : path.noImpedimentJoin = false) :
    path.effectivePathSupport = 0 := by
  classical
  simp only [effectivePathSupport]
  split
  · rename_i ready
    exact False.elim (by
      rcases ready with ⟨_, _, noImpediment⟩
      rw [active] at noImpediment
      cases noImpediment)
  · rfl

end CapabilityPathState

end KUOS.CapabilityOS
