import Mathlib
import KUOS.PlanOS.NextCycleBasisCompilerAdapterV0_3
import KUOS.ActOS.AuthorityBoundInvocationV0_1

namespace KUOS
namespace ActOS

structure ExactActCycleGate where
  planCycle : ℕ
  actCycle : ℕ
  actPhase : Bool
  exactCycleRequired : actCycle = planCycle
  actPhaseRequired : actPhase = true


theorem lineage_handoff_uses_exact_act_cycle
    (gate : ExactActCycleGate) :
    gate.actCycle = gate.planCycle := by
  exact gate.exactCycleRequired


theorem lineage_handoff_requires_act_phase
    (gate : ExactActCycleGate) :
    gate.actPhase = true := by
  exact gate.actPhaseRequired


structure UpstreamLineageBoundary where
  compilerReceiptPreserved : Bool
  replanReceiptPreserved : Bool
  nextPlanActivationPreserved : Bool
  materializationPreserved : Bool
  nextPlanBasisPreserved : Bool
  selectedCandidatePreserved : Bool
  qiConditionPreserved : Bool
  decisionReceiptPreserved : Bool
  synthesisPacketPreserved : Bool
  compilerRequired : compilerReceiptPreserved = true
  replanRequired : replanReceiptPreserved = true
  activationRequired : nextPlanActivationPreserved = true
  materializationRequired : materializationPreserved = true
  basisRequired : nextPlanBasisPreserved = true
  candidateRequired : selectedCandidatePreserved = true
  qiRequired : qiConditionPreserved = true
  decisionRequired : decisionReceiptPreserved = true
  synthesisRequired : synthesisPacketPreserved = true


theorem act_handoff_preserves_planOS_lineage
    (boundary : UpstreamLineageBoundary) :
    boundary.compilerReceiptPreserved = true ∧
      boundary.replanReceiptPreserved = true ∧
      boundary.nextPlanActivationPreserved = true ∧
      boundary.materializationPreserved = true ∧
      boundary.nextPlanBasisPreserved = true := by
  exact ⟨boundary.compilerRequired, boundary.replanRequired,
    boundary.activationRequired, boundary.materializationRequired,
    boundary.basisRequired⟩


theorem act_handoff_preserves_qi_decision_candidate
    (boundary : UpstreamLineageBoundary) :
    boundary.selectedCandidatePreserved = true ∧
      boundary.qiConditionPreserved = true ∧
      boundary.decisionReceiptPreserved = true ∧
      boundary.synthesisPacketPreserved = true := by
  exact ⟨boundary.candidateRequired, boundary.qiRequired,
    boundary.decisionRequired, boundary.synthesisRequired⟩


structure HandoffNonExecutionBoundary where
  planActivationNotExecution : Bool
  actReceiptStillRequired : Bool
  stepAuthorizationStillRequired : Bool
  hostLicenseStillRequired : Bool
  executionGranted : Bool
  hostLicenseGranted : Bool
  planRequired : planActivationNotExecution = true
  actRequired : actReceiptStillRequired = true
  authorizationRequired : stepAuthorizationStillRequired = true
  hostRequired : hostLicenseStillRequired = true
  executionForbidden : executionGranted = false
  licenseForbidden : hostLicenseGranted = false


theorem plan_activation_remains_nonexecuting
    (boundary : HandoffNonExecutionBoundary) :
    boundary.planActivationNotExecution = true ∧
      boundary.executionGranted = false := by
  exact ⟨boundary.planRequired, boundary.executionForbidden⟩


theorem act_and_host_authority_still_required
    (boundary : HandoffNonExecutionBoundary) :
    boundary.actReceiptStillRequired = true ∧
      boundary.stepAuthorizationStillRequired = true ∧
      boundary.hostLicenseStillRequired = true := by
  exact ⟨boundary.actRequired, boundary.authorizationRequired,
    boundary.hostRequired⟩


structure ExactEffectfulStepBoundary where
  selectedStepInCommittedPlan : Bool
  selectedStepIsActCandidate : Bool
  selectedStepIsEffectful : Bool
  stopConditionsPreserved : Bool
  observationDigestPreserved : Bool
  verificationDigestPreserved : Bool
  stepRequired : selectedStepInCommittedPlan = true
  classRequired : selectedStepIsActCandidate = true
  effectRequired : selectedStepIsEffectful = true
  stopRequired : stopConditionsPreserved = true
  observationRequired : observationDigestPreserved = true
  verificationRequired : verificationDigestPreserved = true


theorem handoff_selects_exact_effectful_step
    (boundary : ExactEffectfulStepBoundary) :
    boundary.selectedStepInCommittedPlan = true ∧
      boundary.selectedStepIsActCandidate = true ∧
      boundary.selectedStepIsEffectful = true := by
  exact ⟨boundary.stepRequired, boundary.classRequired,
    boundary.effectRequired⟩


theorem handoff_preserves_step_safety_boundaries
    (boundary : ExactEffectfulStepBoundary) :
    boundary.stopConditionsPreserved = true ∧
      boundary.observationDigestPreserved = true ∧
      boundary.verificationDigestPreserved = true := by
  exact ⟨boundary.stopRequired, boundary.observationRequired,
    boundary.verificationRequired⟩


structure AuthorizationEnvelopeBoundary where
  innerAuthorizationCanonical : Bool
  innerAuthorizationUnchanged : Bool
  operationIdentityPreserved : Bool
  operationInputPreserved : Bool
  actReceiptPreserved : Bool
  hostLicensePreserved : Bool
  humanApprovalPreserved : Bool
  licenseWidened : Bool
  executionGrantedByEnvelope : Bool
  canonicalRequired : innerAuthorizationCanonical = true
  unchangedRequired : innerAuthorizationUnchanged = true
  operationRequired : operationIdentityPreserved = true
  inputRequired : operationInputPreserved = true
  actRequired : actReceiptPreserved = true
  hostRequired : hostLicensePreserved = true
  humanRequired : humanApprovalPreserved = true
  wideningForbidden : licenseWidened = false
  executionForbidden : executionGrantedByEnvelope = false


theorem envelope_preserves_inner_authorization
    (boundary : AuthorizationEnvelopeBoundary) :
    boundary.innerAuthorizationCanonical = true ∧
      boundary.innerAuthorizationUnchanged = true := by
  exact ⟨boundary.canonicalRequired, boundary.unchangedRequired⟩


theorem envelope_preserves_operation_and_receipts
    (boundary : AuthorizationEnvelopeBoundary) :
    boundary.operationIdentityPreserved = true ∧
      boundary.operationInputPreserved = true ∧
      boundary.actReceiptPreserved = true ∧
      boundary.hostLicensePreserved = true ∧
      boundary.humanApprovalPreserved = true := by
  exact ⟨boundary.operationRequired, boundary.inputRequired,
    boundary.actRequired, boundary.hostRequired, boundary.humanRequired⟩


theorem envelope_cannot_widen_or_execute
    (boundary : AuthorizationEnvelopeBoundary) :
    boundary.licenseWidened = false ∧
      boundary.executionGrantedByEnvelope = false := by
  exact ⟨boundary.wideningForbidden, boundary.executionForbidden⟩


structure QiNonAuthorityBoundary where
  qiContextPreserved : Bool
  qiTruthAuthority : Bool
  qiCausalAuthority : Bool
  qiExecutionAuthority : Bool
  qiClinicalAuthority : Bool
  contextRequired : qiContextPreserved = true
  truthForbidden : qiTruthAuthority = false
  causalForbidden : qiCausalAuthority = false
  executionForbidden : qiExecutionAuthority = false
  clinicalForbidden : qiClinicalAuthority = false


theorem qi_is_preserved_without_authority
    (boundary : QiNonAuthorityBoundary) :
    boundary.qiContextPreserved = true ∧
      boundary.qiTruthAuthority = false ∧
      boundary.qiCausalAuthority = false ∧
      boundary.qiExecutionAuthority = false ∧
      boundary.qiClinicalAuthority = false := by
  exact ⟨boundary.contextRequired, boundary.truthForbidden,
    boundary.causalForbidden, boundary.executionForbidden,
    boundary.clinicalForbidden⟩


inductive CompletionRoute where
  | effectRecorded
  | blocked
  | replayed
  deriving DecidableEq, Repr


structure CompletionDebtBoundary where
  route : CompletionRoute
  effectRecorded : Bool
  observationRequired : Bool
  verificationRequired : Bool
  effectRule : effectRecorded = true →
    route = CompletionRoute.effectRecorded ∧
      observationRequired = true ∧
      verificationRequired = true
  noneffectRule : route = CompletionRoute.blocked ∨
      route = CompletionRoute.replayed → effectRecorded = false


theorem recorded_effect_preserves_observation_and_verification_debt
    (boundary : CompletionDebtBoundary)
    (heffect : boundary.effectRecorded = true) :
    boundary.observationRequired = true ∧
      boundary.verificationRequired = true := by
  have h := boundary.effectRule heffect
  exact ⟨h.2.1, h.2.2⟩


theorem blocked_or_replayed_is_not_effect
    (boundary : CompletionDebtBoundary)
    (hroute : boundary.route = CompletionRoute.blocked ∨
      boundary.route = CompletionRoute.replayed) :
    boundary.effectRecorded = false := by
  exact boundary.noneffectRule hroute


structure SingleUseHandoffBoundary where
  handoffCountForCompilerAndStep : ℕ
  completionCountForHandoff : ℕ
  handoffAtMostOne : handoffCountForCompilerAndStep ≤ 1
  completionAtMostOne : completionCountForHandoff ≤ 1


theorem compiler_step_handoff_is_single_use
    (boundary : SingleUseHandoffBoundary) :
    boundary.handoffCountForCompilerAndStep ≤ 1 := by
  exact boundary.handoffAtMostOne


theorem handoff_completion_is_single_use
    (boundary : SingleUseHandoffBoundary) :
    boundary.completionCountForHandoff ≤ 1 := by
  exact boundary.completionAtMostOne


structure LineageStoreHistory where
  committedRecords : ℕ
  recoveredRecords : ℕ
  snapshotRecords : ℕ
  recoveryExact : recoveredRecords = committedRecords
  snapshotDerived : snapshotRecords = recoveredRecords


theorem lineage_store_snapshot_matches_commits
    (history : LineageStoreHistory) :
    history.snapshotRecords = history.committedRecords := by
  rw [history.snapshotDerived, history.recoveryExact]

end ActOS
end KUOS
