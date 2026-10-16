import Mathlib
import KUOS.Architecture.QiWorldNativeEvidenceLoopV1_2

/-!
Native end-to-end OS-cycle provenance for the Qi–WORLD bridge.

The structure records the canonical bindings exported by the existing BeliefOS,
DecisionOS, PlanOS, ActOS, ObserveOS, VerifyOS, and LearnOS artifacts. Governance
remains represented by the independent step-authorization and host-license
witnesses at the Act boundary.
-/

namespace KUOS.Architecture

structure QiWorldNativeFullCycle where
  lineage : Nat

  beliefLineage : Nat
  decisionLineage : Nat
  pluralLineage : Nat
  waLineage : Nat
  planLineage : Nat
  actLineage : Nat
  observeLineage : Nat
  verifyLineage : Nat
  learnLineage : Nat

  belief_lineage_eq : beliefLineage = lineage
  decision_lineage_eq : decisionLineage = lineage
  plural_lineage_eq : pluralLineage = lineage
  wa_lineage_eq : waLineage = lineage
  plan_lineage_eq : planLineage = lineage
  act_lineage_eq : actLineage = lineage
  observe_lineage_eq : observeLineage = lineage
  verify_lineage_eq : verifyLineage = lineage
  learn_lineage_eq : learnLineage = lineage

  beliefReceiptDigest : Nat
  decisionSourceBeliefDigest : Nat
  decisionDigest : Nat
  pluralSourceDecisionDigest : Nat
  pluralDigest : Nat
  waSourcePluralDigest : Nat
  waDigest : Nat
  planSourceWaDigest : Nat
  planDigest : Nat
  actSourcePlanDigest : Nat
  actDigest : Nat
  observeSourceActDigest : Nat
  observeDigest : Nat
  verifySourceObserveDigest : Nat
  verifyDigest : Nat
  learnSourceVerifyDigest : Nat
  learnDigest : Nat

  decision_binds_belief : decisionSourceBeliefDigest = beliefReceiptDigest
  plural_binds_decision : pluralSourceDecisionDigest = decisionDigest
  wa_binds_plural : waSourcePluralDigest = pluralDigest
  plan_binds_wa : planSourceWaDigest = waDigest
  act_binds_plan : actSourcePlanDigest = planDigest
  observe_binds_act : observeSourceActDigest = actDigest
  verify_binds_observe : verifySourceObserveDigest = observeDigest
  learn_binds_verify : learnSourceVerifyDigest = verifyDigest

  missionContract : Nat
  decisionMissionContract : Nat
  pluralMissionContract : Nat
  waMissionContract : Nat
  planMissionContract : Nat
  actMissionContract : Nat
  observeMissionContract : Nat
  verifyMissionContract : Nat
  learnMissionContract : Nat

  decision_mission_eq : decisionMissionContract = missionContract
  plural_mission_eq : pluralMissionContract = missionContract
  wa_mission_eq : waMissionContract = missionContract
  plan_mission_eq : planMissionContract = missionContract
  act_mission_eq : actMissionContract = missionContract
  observe_mission_eq : observeMissionContract = missionContract
  verify_mission_eq : verifyMissionContract = missionContract
  learn_mission_eq : learnMissionContract = missionContract

  governanceCertificatePresent : Prop
  governanceCertificateProof : governanceCertificatePresent
  externalAuthorityReceiptPresent : Prop
  externalAuthorityReceiptProof : externalAuthorityReceiptPresent

  beliefConditional : Prop
  beliefConditionalProof : beliefConditional
  decisionNotExecution : Prop
  decisionNotExecutionProof : decisionNotExecution
  planNotExecution : Prop
  planNotExecutionProof : planNotExecution
  actEffectRecorded : Prop
  actEffectRecordedProof : actEffectRecorded
  observationRecorded : Prop
  observationRecordedProof : observationRecorded
  verificationRecorded : Prop
  verificationRecordedProof : verificationRecorded
  learningFutureOnly : Prop
  learningFutureOnlyProof : learningFutureOnly

  worldProjectionReadOnly : Prop
  worldProjectionReadOnlyProof : worldProjectionReadOnly
  exactWorldIdentified : Bool
  exact_world_not_identified : exactWorldIdentified = false
  runtimeUpdatesWorld : Bool
  no_runtime_world_update : runtimeUpdatesWorld = false

  adapterGrantsExecution : Bool
  no_adapter_execution_authority : adapterGrantsExecution = false
  adapterIssuesAuthority : Bool
  no_adapter_authority_issue : adapterIssuesAuthority = false
  adapterOverwritesHistory : Bool
  no_adapter_history_overwrite : adapterOverwritesHistory = false

namespace QiWorldNativeFullCycle

variable (C : QiWorldNativeFullCycle)

theorem all_native_interfaces_share_lineage :
    C.beliefLineage = C.decisionLineage ∧
    C.decisionLineage = C.pluralLineage ∧
    C.pluralLineage = C.waLineage ∧
    C.waLineage = C.planLineage ∧
    C.planLineage = C.actLineage ∧
    C.actLineage = C.observeLineage ∧
    C.observeLineage = C.verifyLineage ∧
    C.verifyLineage = C.learnLineage := by
  constructor
  · rw [C.belief_lineage_eq, C.decision_lineage_eq]
  constructor
  · rw [C.decision_lineage_eq, C.plural_lineage_eq]
  constructor
  · rw [C.plural_lineage_eq, C.wa_lineage_eq]
  constructor
  · rw [C.wa_lineage_eq, C.plan_lineage_eq]
  constructor
  · rw [C.plan_lineage_eq, C.act_lineage_eq]
  constructor
  · rw [C.act_lineage_eq, C.observe_lineage_eq]
  constructor
  · rw [C.observe_lineage_eq, C.verify_lineage_eq]
  · rw [C.verify_lineage_eq, C.learn_lineage_eq]

theorem native_full_provenance_chain :
    C.decisionSourceBeliefDigest = C.beliefReceiptDigest ∧
    C.pluralSourceDecisionDigest = C.decisionDigest ∧
    C.waSourcePluralDigest = C.pluralDigest ∧
    C.planSourceWaDigest = C.waDigest ∧
    C.actSourcePlanDigest = C.planDigest ∧
    C.observeSourceActDigest = C.actDigest ∧
    C.verifySourceObserveDigest = C.observeDigest ∧
    C.learnSourceVerifyDigest = C.verifyDigest :=
  ⟨C.decision_binds_belief,
    C.plural_binds_decision,
    C.wa_binds_plural,
    C.plan_binds_wa,
    C.act_binds_plan,
    C.observe_binds_act,
    C.verify_binds_observe,
    C.learn_binds_verify⟩

theorem all_native_stages_share_mission_contract :
    C.decisionMissionContract = C.pluralMissionContract ∧
    C.pluralMissionContract = C.waMissionContract ∧
    C.waMissionContract = C.planMissionContract ∧
    C.planMissionContract = C.actMissionContract ∧
    C.actMissionContract = C.observeMissionContract ∧
    C.observeMissionContract = C.verifyMissionContract ∧
    C.verifyMissionContract = C.learnMissionContract := by
  constructor
  · rw [C.decision_mission_eq, C.plural_mission_eq]
  constructor
  · rw [C.plural_mission_eq, C.wa_mission_eq]
  constructor
  · rw [C.wa_mission_eq, C.plan_mission_eq]
  constructor
  · rw [C.plan_mission_eq, C.act_mission_eq]
  constructor
  · rw [C.act_mission_eq, C.observe_mission_eq]
  constructor
  · rw [C.observe_mission_eq, C.verify_mission_eq]
  · rw [C.verify_mission_eq, C.learn_mission_eq]

theorem act_requires_governance_and_external_authority :
    C.governanceCertificatePresent ∧ C.externalAuthorityReceiptPresent :=
  ⟨C.governanceCertificateProof, C.externalAuthorityReceiptProof⟩

theorem staged_non_execution_boundary :
    C.beliefConditional ∧
    C.decisionNotExecution ∧
    C.planNotExecution ∧
    C.actEffectRecorded ∧
    C.observationRecorded ∧
    C.verificationRecorded ∧
    C.learningFutureOnly :=
  ⟨C.beliefConditionalProof,
    C.decisionNotExecutionProof,
    C.planNotExecutionProof,
    C.actEffectRecordedProof,
    C.observationRecordedProof,
    C.verificationRecordedProof,
    C.learningFutureOnlyProof⟩

theorem world_read_only_boundary :
    C.worldProjectionReadOnly ∧
    C.exactWorldIdentified = false ∧
    C.runtimeUpdatesWorld = false :=
  ⟨C.worldProjectionReadOnlyProof,
    C.exact_world_not_identified,
    C.no_runtime_world_update⟩

theorem adapter_non_authority :
    C.adapterGrantsExecution = false ∧
    C.adapterIssuesAuthority = false ∧
    C.adapterOverwritesHistory = false :=
  ⟨C.no_adapter_execution_authority,
    C.no_adapter_authority_issue,
    C.no_adapter_history_overwrite⟩

theorem native_full_cycle_safety_package :
    C.decisionSourceBeliefDigest = C.beliefReceiptDigest ∧
    C.planSourceWaDigest = C.waDigest ∧
    C.actSourcePlanDigest = C.planDigest ∧
    C.observeSourceActDigest = C.actDigest ∧
    C.verifySourceObserveDigest = C.observeDigest ∧
    C.learnSourceVerifyDigest = C.verifyDigest ∧
    C.learningFutureOnly ∧
    C.worldProjectionReadOnly ∧
    C.adapterGrantsExecution = false :=
  ⟨C.decision_binds_belief,
    C.plan_binds_wa,
    C.act_binds_plan,
    C.observe_binds_act,
    C.verify_binds_observe,
    C.learn_binds_verify,
    C.learningFutureOnlyProof,
    C.worldProjectionReadOnlyProof,
    C.no_adapter_execution_authority⟩

end QiWorldNativeFullCycle
end KUOS.Architecture
