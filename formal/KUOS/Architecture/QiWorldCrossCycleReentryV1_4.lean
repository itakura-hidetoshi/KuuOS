import Mathlib
import KUOS.Architecture.QiWorldNativeFullCycleV1_3

/-!
Qi–WORLD cross-cycle re-entry v1.4.

This structure records how a completed native cycle contributes only to a
future Belief → Decision → Plan branch.  The previous cycle remains immutable,
LearnOS remains future-only, and no ActOS state is created by this bridge.
-/

namespace KUOS.Architecture

structure QiWorldCrossCycleReentry where
  lineage : Nat
  missionContract : Nat

  previousCycleReceiptDigest : Nat
  previousLearnStateDigest : Nat
  previousLearningDeltaDigest : Nat
  previousObserveEvidenceDigest : Nat
  previousVerificationEvidenceDigest : Nat

  nextBeliefStateDigest : Nat
  nextBeliefSourceMemoryDigest : Nat
  nextBeliefEvidenceDigests : Finset Nat
  nextBeliefActivationDigest : Nat
  nextBeliefActivationStateDigest : Nat
  nextBeliefNextPlanBasisDigest : Nat

  nextDecisionStateDigest : Nat
  nextDecisionSourceBeliefReceiptDigest : Nat
  nextPluralStateDigest : Nat
  nextPluralSourceDecisionDigest : Nat
  nextWaStateDigest : Nat
  nextWaSourcePluralDigest : Nat
  nextPlanStateDigest : Nat
  nextPlanSourceWaDigest : Nat

  previousLearnLineage : Nat
  nextBeliefLineage : Nat
  nextDecisionLineage : Nat
  nextPluralLineage : Nat
  nextWaLineage : Nat
  nextPlanLineage : Nat

  previousLearnMissionContract : Nat
  nextDecisionMissionContract : Nat
  nextPluralMissionContract : Nat
  nextWaMissionContract : Nat
  nextPlanMissionContract : Nat

  belief_memory_from_learning :
    nextBeliefSourceMemoryDigest = previousLearnStateDigest
  belief_contains_observe_evidence :
    previousObserveEvidenceDigest ∈ nextBeliefEvidenceDigests
  belief_contains_verification_evidence :
    previousVerificationEvidenceDigest ∈ nextBeliefEvidenceDigests
  belief_contains_learning_delta :
    previousLearningDeltaDigest ∈ nextBeliefEvidenceDigests
  belief_activation_binds_state :
    nextBeliefActivationStateDigest = nextBeliefStateDigest
  learning_delta_is_next_plan_basis :
    nextBeliefNextPlanBasisDigest = previousLearningDeltaDigest
  decision_binds_belief_activation :
    nextDecisionSourceBeliefReceiptDigest = nextBeliefActivationDigest
  plural_binds_decision :
    nextPluralSourceDecisionDigest = nextDecisionStateDigest
  wa_binds_plural : nextWaSourcePluralDigest = nextPluralStateDigest
  plan_binds_wa : nextPlanSourceWaDigest = nextWaStateDigest

  previous_learn_lineage_eq : previousLearnLineage = lineage
  next_belief_lineage_eq : nextBeliefLineage = lineage
  next_decision_lineage_eq : nextDecisionLineage = lineage
  next_plural_lineage_eq : nextPluralLineage = lineage
  next_wa_lineage_eq : nextWaLineage = lineage
  next_plan_lineage_eq : nextPlanLineage = lineage

  previous_learn_mission_eq : previousLearnMissionContract = missionContract
  next_decision_mission_eq : nextDecisionMissionContract = missionContract
  next_plural_mission_eq : nextPluralMissionContract = missionContract
  next_wa_mission_eq : nextWaMissionContract = missionContract
  next_plan_mission_eq : nextPlanMissionContract = missionContract

  previousCycleImmutable : Prop
  previousCycleImmutableProof : previousCycleImmutable
  previousLearningFutureOnly : Prop
  previousLearningFutureOnlyProof : previousLearningFutureOnly
  previousPastRecordsUnchanged : Prop
  previousPastRecordsUnchangedProof : previousPastRecordsUnchanged
  nextPlanCommitted : Prop
  nextPlanCommittedProof : nextPlanCommitted
  nextActStarted : Bool
  next_act_not_started : nextActStarted = false

  qiProcessVisible : Prop
  qiProcessVisibleProof : qiProcessVisible
  qiMemoryContinuous : Prop
  qiMemoryContinuousProof : qiMemoryContinuous
  qiNonMarkovVisible : Prop
  qiNonMarkovVisibleProof : qiNonMarkovVisible
  worldProjectionReadOnly : Prop
  worldProjectionReadOnlyProof : worldProjectionReadOnly
  exactWorldUpdated : Bool
  exact_world_not_updated : exactWorldUpdated = false

  bridgeGrantsExecution : Bool
  no_bridge_execution_authority : bridgeGrantsExecution = false
  bridgeIssuesAuthority : Bool
  no_bridge_authority_issue : bridgeIssuesAuthority = false
  bridgeOverwritesPreviousCycle : Bool
  no_previous_cycle_overwrite : bridgeOverwritesPreviousCycle = false

namespace QiWorldCrossCycleReentry

variable (R : QiWorldCrossCycleReentry)

theorem learning_enters_next_belief_memory :
    R.nextBeliefSourceMemoryDigest = R.previousLearnStateDigest :=
  R.belief_memory_from_learning

theorem prior_evidence_enters_next_belief :
    R.previousObserveEvidenceDigest ∈ R.nextBeliefEvidenceDigests ∧
    R.previousVerificationEvidenceDigest ∈ R.nextBeliefEvidenceDigests ∧
    R.previousLearningDeltaDigest ∈ R.nextBeliefEvidenceDigests :=
  ⟨R.belief_contains_observe_evidence,
    R.belief_contains_verification_evidence,
    R.belief_contains_learning_delta⟩

theorem learning_delta_drives_future_plan_basis :
    R.nextBeliefNextPlanBasisDigest = R.previousLearningDeltaDigest :=
  R.learning_delta_is_next_plan_basis

theorem next_reasoning_chain_is_digest_bound :
    R.nextDecisionSourceBeliefReceiptDigest = R.nextBeliefActivationDigest ∧
    R.nextPluralSourceDecisionDigest = R.nextDecisionStateDigest ∧
    R.nextWaSourcePluralDigest = R.nextPluralStateDigest ∧
    R.nextPlanSourceWaDigest = R.nextWaStateDigest :=
  ⟨R.decision_binds_belief_activation,
    R.plural_binds_decision,
    R.wa_binds_plural,
    R.plan_binds_wa⟩

theorem cross_cycle_lineage_preserved :
    R.previousLearnLineage = R.nextBeliefLineage ∧
    R.nextBeliefLineage = R.nextDecisionLineage ∧
    R.nextDecisionLineage = R.nextPluralLineage ∧
    R.nextPluralLineage = R.nextWaLineage ∧
    R.nextWaLineage = R.nextPlanLineage := by
  constructor
  · rw [R.previous_learn_lineage_eq, R.next_belief_lineage_eq]
  constructor
  · rw [R.next_belief_lineage_eq, R.next_decision_lineage_eq]
  constructor
  · rw [R.next_decision_lineage_eq, R.next_plural_lineage_eq]
  constructor
  · rw [R.next_plural_lineage_eq, R.next_wa_lineage_eq]
  · rw [R.next_wa_lineage_eq, R.next_plan_lineage_eq]

theorem cross_cycle_mission_preserved :
    R.previousLearnMissionContract = R.nextDecisionMissionContract ∧
    R.nextDecisionMissionContract = R.nextPluralMissionContract ∧
    R.nextPluralMissionContract = R.nextWaMissionContract ∧
    R.nextWaMissionContract = R.nextPlanMissionContract := by
  constructor
  · rw [R.previous_learn_mission_eq, R.next_decision_mission_eq]
  constructor
  · rw [R.next_decision_mission_eq, R.next_plural_mission_eq]
  constructor
  · rw [R.next_plural_mission_eq, R.next_wa_mission_eq]
  · rw [R.next_wa_mission_eq, R.next_plan_mission_eq]

theorem previous_cycle_remains_immutable :
    R.previousCycleImmutable ∧
    R.previousLearningFutureOnly ∧
    R.previousPastRecordsUnchanged :=
  ⟨R.previousCycleImmutableProof,
    R.previousLearningFutureOnlyProof,
    R.previousPastRecordsUnchangedProof⟩

theorem next_plan_stops_before_act :
    R.nextPlanCommitted ∧ R.nextActStarted = false :=
  ⟨R.nextPlanCommittedProof, R.next_act_not_started⟩

theorem cross_cycle_process_visibility :
    R.qiProcessVisible ∧ R.qiMemoryContinuous ∧ R.qiNonMarkovVisible :=
  ⟨R.qiProcessVisibleProof,
    R.qiMemoryContinuousProof,
    R.qiNonMarkovVisibleProof⟩

theorem cross_cycle_world_boundary :
    R.worldProjectionReadOnly ∧ R.exactWorldUpdated = false :=
  ⟨R.worldProjectionReadOnlyProof, R.exact_world_not_updated⟩

theorem cross_cycle_non_authority :
    R.bridgeGrantsExecution = false ∧
    R.bridgeIssuesAuthority = false ∧
    R.bridgeOverwritesPreviousCycle = false :=
  ⟨R.no_bridge_execution_authority,
    R.no_bridge_authority_issue,
    R.no_previous_cycle_overwrite⟩

theorem cross_cycle_safety_package :
    R.nextBeliefSourceMemoryDigest = R.previousLearnStateDigest ∧
    R.nextBeliefNextPlanBasisDigest = R.previousLearningDeltaDigest ∧
    R.previousCycleImmutable ∧
    R.nextActStarted = false ∧
    R.exactWorldUpdated = false ∧
    R.bridgeGrantsExecution = false :=
  ⟨R.belief_memory_from_learning,
    R.learning_delta_is_next_plan_basis,
    R.previousCycleImmutableProof,
    R.next_act_not_started,
    R.exact_world_not_updated,
    R.no_bridge_execution_authority⟩

end QiWorldCrossCycleReentry
end KUOS.Architecture
