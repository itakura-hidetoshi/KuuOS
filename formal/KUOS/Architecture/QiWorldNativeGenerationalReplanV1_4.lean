import Mathlib
import KUOS.Architecture.QiWorldNativeFullCycleV1_3

/-!
Qi–WORLD native generational replan bridge v1.4.

The bridge closes one bounded inter-generation edge:

  committed LearnOS future-only delta
    → native PlanOS replan
    → native DecisionOS / plural / Wa selection
    → committed next-PLAN basis

The Qi process tensor is the non-Markov temporal context and WORLD remains a
read-only candidate projection. No present activation, execution authority,
truth authority, exact-WORLD update, or history overwrite is introduced.
-/

namespace KUOS.Architecture

structure QiWorldNativeGenerationalReplan where
  sourceGeneration : Nat
  targetGeneration : Nat
  target_is_next_generation : targetGeneration = sourceGeneration + 1

  sourceFullCycleDigest : Nat
  sourcePlanDigest : Nat
  replanSourcePlanDigest : Nat
  sourceLearnDigest : Nat
  replanSourceLearnDigest : Nat
  sourceLearningDeltaDigest : Nat
  replanSourceLearningDeltaDigest : Nat

  replan_binds_source_plan : replanSourcePlanDigest = sourcePlanDigest
  replan_binds_source_learn : replanSourceLearnDigest = sourceLearnDigest
  replan_binds_learning_delta :
    replanSourceLearningDeltaDigest = sourceLearningDeltaDigest

  sourceBeliefReceiptDigest : Nat
  decisionSourceBeliefDigest : Nat
  decisionDigest : Nat
  pluralSourceDecisionDigest : Nat
  pluralDigest : Nat
  waSourcePluralDigest : Nat
  waDigest : Nat
  replanDecisionDigest : Nat
  replanWaDigest : Nat

  decision_binds_source_belief :
    decisionSourceBeliefDigest = sourceBeliefReceiptDigest
  plural_binds_decision : pluralSourceDecisionDigest = decisionDigest
  wa_binds_plural : waSourcePluralDigest = pluralDigest
  replan_binds_decision : replanDecisionDigest = decisionDigest
  replan_binds_wa : replanWaDigest = waDigest

  selectedDecisionCandidate : Nat
  selectedReplanCandidate : Nat
  selected_identity_preserved :
    selectedReplanCandidate = selectedDecisionCandidate

  sourceQiReceiptDigest : Nat
  sourceQiHistoryDigest : Nat
  extendedQiReceiptDigest : Nat
  sourceWorldProjectionDigest : Nat
  nextWorldProjectionSourceDigest : Nat
  nextWorldProjectionDigest : Nat
  nextPlanBasisDigest : Nat
  qiNextPlanBasisDigest : Nat
  worldNextPlanBasisDigest : Nat

  next_world_binds_source_world :
    nextWorldProjectionSourceDigest = sourceWorldProjectionDigest
  qi_binds_next_plan_basis : qiNextPlanBasisDigest = nextPlanBasisDigest
  world_binds_next_plan_basis : worldNextPlanBasisDigest = nextPlanBasisDigest

  qiProcessVisible : Prop
  qiProcessVisibleProof : qiProcessVisible
  qiTransitionContinuity : Prop
  qiTransitionContinuityProof : qiTransitionContinuity
  qiMemoryContinuity : Prop
  qiMemoryContinuityProof : qiMemoryContinuity
  qiNonMarkovMemory : Prop
  qiNonMarkovMemoryProof : qiNonMarkovMemory
  qiHistoryPrefixPreserved : Prop
  qiHistoryPrefixPreservedProof : qiHistoryPrefixPreserved
  qiContextOnly : Prop
  qiContextOnlyProof : qiContextOnly

  worldProjectionReadOnly : Prop
  worldProjectionReadOnlyProof : worldProjectionReadOnly
  worldCandidateOnly : Prop
  worldCandidateOnlyProof : worldCandidateOnly
  worldTwoTruthsSeparated : Prop
  worldTwoTruthsSeparatedProof : worldTwoTruthsSeparated
  exactWorldIdentified : Bool
  exact_world_not_identified : exactWorldIdentified = false
  runtimeUpdatesWorld : Bool
  no_runtime_world_update : runtimeUpdatesWorld = false

  learningFutureOnly : Prop
  learningFutureOnlyProof : learningFutureOnly
  nextPlanFutureOnly : Prop
  nextPlanFutureOnlyProof : nextPlanFutureOnly
  nextPlanActiveNow : Bool
  next_plan_not_active_now : nextPlanActiveNow = false
  nextPlanIsExecution : Bool
  next_plan_not_execution : nextPlanIsExecution = false
  hostLicenseGranted : Bool
  no_host_license : hostLicenseGranted = false
  externalAuthorityRequired : Prop
  externalAuthorityRequiredProof : externalAuthorityRequired

  currentCycleChanged : Bool
  current_cycle_unchanged : currentCycleChanged = false
  pastHistoryOverwritten : Bool
  no_past_history_overwrite : pastHistoryOverwritten = false

  adapterGrantsExecution : Bool
  no_adapter_execution : adapterGrantsExecution = false
  adapterGrantsTruth : Bool
  no_adapter_truth : adapterGrantsTruth = false
  adapterIssuesAuthority : Bool
  no_adapter_authority_issue : adapterIssuesAuthority = false
  adapterActivatesNextPlan : Bool
  no_adapter_next_plan_activation : adapterActivatesNextPlan = false

namespace QiWorldNativeGenerationalReplan

variable (G : QiWorldNativeGenerationalReplan)

theorem generation_strictly_advances :
    G.sourceGeneration < G.targetGeneration := by
  rw [G.target_is_next_generation]
  exact Nat.lt_succ_self G.sourceGeneration

theorem source_native_bindings :
    G.replanSourcePlanDigest = G.sourcePlanDigest ∧
    G.replanSourceLearnDigest = G.sourceLearnDigest ∧
    G.replanSourceLearningDeltaDigest = G.sourceLearningDeltaDigest :=
  ⟨G.replan_binds_source_plan,
    G.replan_binds_source_learn,
    G.replan_binds_learning_delta⟩

theorem native_deliberation_provenance :
    G.decisionSourceBeliefDigest = G.sourceBeliefReceiptDigest ∧
    G.pluralSourceDecisionDigest = G.decisionDigest ∧
    G.waSourcePluralDigest = G.pluralDigest ∧
    G.replanDecisionDigest = G.decisionDigest ∧
    G.replanWaDigest = G.waDigest ∧
    G.selectedReplanCandidate = G.selectedDecisionCandidate :=
  ⟨G.decision_binds_source_belief,
    G.plural_binds_decision,
    G.wa_binds_plural,
    G.replan_binds_decision,
    G.replan_binds_wa,
    G.selected_identity_preserved⟩

theorem next_plan_basis_shared_by_qi_and_world :
    G.qiNextPlanBasisDigest = G.nextPlanBasisDigest ∧
    G.worldNextPlanBasisDigest = G.nextPlanBasisDigest ∧
    G.nextWorldProjectionSourceDigest = G.sourceWorldProjectionDigest :=
  ⟨G.qi_binds_next_plan_basis,
    G.world_binds_next_plan_basis,
    G.next_world_binds_source_world⟩

theorem qi_is_nonmarkov_context_not_authority :
    G.qiProcessVisible ∧
    G.qiTransitionContinuity ∧
    G.qiMemoryContinuity ∧
    G.qiNonMarkovMemory ∧
    G.qiHistoryPrefixPreserved ∧
    G.qiContextOnly ∧
    G.adapterGrantsExecution = false ∧
    G.adapterIssuesAuthority = false :=
  ⟨G.qiProcessVisibleProof,
    G.qiTransitionContinuityProof,
    G.qiMemoryContinuityProof,
    G.qiNonMarkovMemoryProof,
    G.qiHistoryPrefixPreservedProof,
    G.qiContextOnlyProof,
    G.no_adapter_execution,
    G.no_adapter_authority_issue⟩

theorem world_remains_read_only_candidate_projection :
    G.worldProjectionReadOnly ∧
    G.worldCandidateOnly ∧
    G.worldTwoTruthsSeparated ∧
    G.exactWorldIdentified = false ∧
    G.runtimeUpdatesWorld = false :=
  ⟨G.worldProjectionReadOnlyProof,
    G.worldCandidateOnlyProof,
    G.worldTwoTruthsSeparatedProof,
    G.exact_world_not_identified,
    G.no_runtime_world_update⟩

theorem next_generation_basis_is_inactive_nonexecution :
    G.learningFutureOnly ∧
    G.nextPlanFutureOnly ∧
    G.nextPlanActiveNow = false ∧
    G.nextPlanIsExecution = false ∧
    G.hostLicenseGranted = false ∧
    G.externalAuthorityRequired :=
  ⟨G.learningFutureOnlyProof,
    G.nextPlanFutureOnlyProof,
    G.next_plan_not_active_now,
    G.next_plan_not_execution,
    G.no_host_license,
    G.externalAuthorityRequiredProof⟩

theorem additive_only_intergeneration_transition :
    G.currentCycleChanged = false ∧
    G.pastHistoryOverwritten = false ∧
    G.adapterActivatesNextPlan = false ∧
    G.adapterGrantsTruth = false :=
  ⟨G.current_cycle_unchanged,
    G.no_past_history_overwrite,
    G.no_adapter_next_plan_activation,
    G.no_adapter_truth⟩

theorem bounded_generational_replan_boundary :
    G.sourceGeneration < G.targetGeneration ∧
    G.worldProjectionReadOnly ∧
    G.qiContextOnly ∧
    G.nextPlanActiveNow = false ∧
    G.nextPlanIsExecution = false ∧
    G.hostLicenseGranted = false ∧
    G.runtimeUpdatesWorld = false ∧
    G.pastHistoryOverwritten = false := by
  exact
    ⟨generation_strictly_advances G,
      G.worldProjectionReadOnlyProof,
      G.qiContextOnlyProof,
      G.next_plan_not_active_now,
      G.next_plan_not_execution,
      G.no_host_license,
      G.no_runtime_world_update,
      G.no_past_history_overwrite⟩

end QiWorldNativeGenerationalReplan
end KUOS.Architecture
