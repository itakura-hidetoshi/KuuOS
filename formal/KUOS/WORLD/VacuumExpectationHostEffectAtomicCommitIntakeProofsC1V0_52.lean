import KUOS.WORLD.VacuumExpectationHostEffectAtomicCommitIntakeCoreV0_52

namespace KUOS.WORLD
open ObserveOS VerifyOS LearnOS DecisionOS PlanOS ActOS
namespace WorldVacuumExpectationHostEffectAtomicCommitIntakeBridge

abbrev EnvelopeC1 := WorldVacuumExpectationHostEffectAtomicCommitIntakeEnvelope

theorem intake_history_appends_one_record
    {Bridge : WorldVacuumExpectationHostEffectAtomicCommitIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge}
    (envelope : EnvelopeC1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge Bridge) :
    envelope.historyAfter.committedRecords =
        envelope.source.historyAfter.committedRecords + 1 ∧
      envelope.historyAfter.snapshotRecords =
        envelope.source.historyAfter.committedRecords + 1 := by
  refine ⟨envelope.historyExact, ?_⟩
  rw [worldAtomicCommitIntakeHistory_snapshot_matches_commits envelope.historyAfter]
  exact envelope.historyExact

theorem intake_index_follows_host_receipt
    {Bridge : WorldVacuumExpectationHostEffectAtomicCommitIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge}
    (envelope : EnvelopeC1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge Bridge) :
    envelope.source.hostReceiptIndex.current < envelope.intakeIndex.current := by
  rw [envelope.intakeIndexExact]
  omega

theorem ownership_boundaries_are_preserved
    {Bridge : WorldVacuumExpectationHostEffectAtomicCommitIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge}
    (_envelope : EnvelopeC1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge Bridge) :
    Bridge.intakeOwnedByWORLD = true ∧
      Bridge.observationOwnedByObserveOS = true ∧
      Bridge.verificationOwnedByVerifyOS = true ∧
      Bridge.atomicCommitOwnedByWORLD = true := by
  exact ⟨Bridge.intakeOwnerRequired, Bridge.observationOwnerRequired,
    Bridge.verificationOwnerRequired, Bridge.atomicCommitOwnerRequired⟩

end WorldVacuumExpectationHostEffectAtomicCommitIntakeBridge
end KUOS.WORLD
