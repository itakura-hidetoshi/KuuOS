import KUOS.ObserveOS.WorldHostEffectObservationReceiptCoreV0_4

namespace KUOS.ObserveOS
open WORLD VerifyOS LearnOS DecisionOS PlanOS ActOS
namespace WorldHostEffectObservationBridge

abbrev ReceiptC1 := WorldHostEffectObservationReceipt

theorem evidence_collection_and_receipt_are_single_use
    {Bridge : WorldHostEffectObservationBridge K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge}
    (r : ReceiptC1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge Bridge) :
    r.collection.exactReplayIdempotent = true ∧
      r.collection.conflictingReplayAccepted = false ∧
      r.singleUse.completionCount ≤ 1 := by
  exact ⟨r.collection.replayRequired,
    r.collection.conflictingReplayForbidden,
    completion_is_single_use r.singleUse⟩

theorem observation_events_append_strictly
    {Bridge : WorldHostEffectObservationBridge K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge}
    (r : ReceiptC1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge Bridge) :
    r.source.intakeIndex.current < r.collectionIndex.current ∧
      r.collectionIndex.current < r.receiptIndex.current := by
  constructor
  · rw [r.collectionIndexExact]
    omega
  · rw [r.receiptIndexExact]
    exact observeEventIndex_strict r.collectionIndex

theorem observation_history_appends_two_records
    {Bridge : WorldHostEffectObservationBridge K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge}
    (r : ReceiptC1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge Bridge) :
    r.historyAfter.committedRecords = r.source.historyAfter.committedRecords + 2 ∧
      r.historyAfter.snapshotRecords = r.source.historyAfter.committedRecords + 2 := by
  refine ⟨r.historyExact, ?_⟩
  rw [observeHistory_snapshot_matches_commits r.historyAfter]
  exact r.historyExact

theorem ownership_is_separated
    {Bridge : WorldHostEffectObservationBridge K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge}
    (_r : ReceiptC1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge Bridge) :
    Bridge.observationOwnedByObserveOS = true ∧
      Bridge.verificationOwnedByVerifyOS = true ∧
      Bridge.futureAtomicCommitOwnedByWORLD = true ∧
      Bridge.runtimeCollectsEvidence = false ∧
      Bridge.runtimeCommitsObservation = false := by
  exact ⟨Bridge.observationOwnerRequired, Bridge.verificationOwnerRequired,
    Bridge.atomicCommitOwnerRequired, Bridge.collectionForbidden,
    Bridge.runtimeCommitForbidden⟩

theorem observation_receipt_digest_is_exact
    {Bridge : WorldHostEffectObservationBridge K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge}
    (r : ReceiptC1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge Bridge) :
    r.receiptDigest = Bridge.receiptDigestOf r.source r.exactObserveCycle
      r.upstreamLineage r.effectObservation r.identity r.collection
      r.evidenceRequirements r.provenance r.comparison r.debtSemantics
      r.observationVerification r.singleUse r.receiptBoundary
      r.worldPrerequisite r.collectionIndex r.receiptIndex r.historyAfter := by
  exact r.receiptDigestExact

end WorldHostEffectObservationBridge
end KUOS.ObserveOS
