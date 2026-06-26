import KUOS.ObserveOS.WorldHostEffectObservationReceiptCoreV0_4

namespace KUOS.ObserveOS
open WORLD VerifyOS LearnOS DecisionOS PlanOS ActOS
namespace WorldHostEffectObservationBridge

abbrev ReceiptA1 := WorldHostEffectObservationReceipt

theorem observation_requires_ready_uncommitted_world_intake
    {Bridge : WorldHostEffectObservationBridge K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge}
    (r : ReceiptA1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge Bridge) :
    r.sourceAccepted = true ∧ r.source.intakeReady = true ∧
      r.source.candidateOnly = true ∧
      r.source.pendingDebt.observationCommitted = false ∧
      r.source.pendingDebt.verificationCommitted = false ∧
      r.source.pendingDebt.independentWorldEvidencePresent = false := by
  exact ⟨r.sourceAcceptedRequired, r.sourceIntakeReady,
    r.sourceCandidateOnly, r.sourceObservationUncommitted,
    r.sourceVerificationUncommitted, r.sourceIndependentEvidenceAbsent⟩

theorem observation_uses_exact_act_cycle
    {Bridge : WorldHostEffectObservationBridge K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge}
    (r : ReceiptA1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge Bridge) :
    r.exactObserveCycle.observeCycle = r.source.source.source.exactActCycle.actCycle ∧
      r.exactObserveCycle.observePhase = true := by
  constructor
  · calc
      r.exactObserveCycle.observeCycle = r.exactObserveCycle.actCycle :=
        r.exactObserveCycle.exactCycleRequired
      _ = r.source.source.source.exactActCycle.actCycle := r.observeCycleExact
  · exact r.exactObserveCycle.observePhaseRequired

theorem observation_preserves_upstream_lineage
    {Bridge : WorldHostEffectObservationBridge K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge}
    (r : ReceiptA1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge Bridge) :
    r.upstreamLineage.actHandoffPreserved = true ∧
      r.upstreamLineage.actCompletionPreserved = true ∧
      r.upstreamLineage.compilerReceiptPreserved = true ∧
      r.upstreamLineage.replanReceiptPreserved = true ∧
      r.upstreamLineage.qiConditionPreserved = true ∧
      r.upstreamLineage.decisionReceiptPreserved = true ∧
      r.upstreamLineage.selectedCandidatePreserved = true ∧
      r.upstreamLineage.selectedStepPreserved = true := by
  exact ⟨r.upstreamLineage.actHandoffRequired,
    r.upstreamLineage.actCompletionRequired,
    r.upstreamLineage.compilerRequired, r.upstreamLineage.replanRequired,
    r.upstreamLineage.qiRequired, r.upstreamLineage.decisionRequired,
    r.upstreamLineage.candidateRequired, r.upstreamLineage.stepRequired⟩

theorem source_effect_and_identity_are_exactly_bound
    {Bridge : WorldHostEffectObservationBridge K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge}
    (r : ReceiptA1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge Bridge) :
    r.effectObservation.sourceEffectRecorded = true ∧
      r.effectObservation.observationRequired = true ∧
      r.effectObservation.observationTargetPreserved = true ∧
      r.identity.worldIntakeBound = true ∧ r.identity.hostReceiptBound = true ∧
      r.identity.effectRecordBound = true ∧ r.identity.operationIdentityExact = true ∧
      r.identity.operationInputExact = true ∧ r.identity.selectedStepExact = true ∧
      r.identity.targetCycleExact = true ∧ r.identity.sessionExact = true ∧
      r.identity.actionIntentExact = true ∧ r.identity.expectedObservationExact = true := by
  exact ⟨r.effectObservation.sourceRequired,
    r.effectObservation.debtRequired, r.effectObservation.targetRequired,
    r.identity.worldIntakeRequired, r.identity.hostReceiptRequired,
    r.identity.effectRecordRequired, r.identity.operationRequired,
    r.identity.inputRequired, r.identity.stepRequired,
    r.identity.cycleRequired, r.identity.sessionRequired,
    r.identity.intentRequired, r.identity.expectedRequired⟩

end WorldHostEffectObservationBridge
end KUOS.ObserveOS
