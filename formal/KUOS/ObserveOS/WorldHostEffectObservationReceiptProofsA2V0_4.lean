import KUOS.ObserveOS.WorldHostEffectObservationReceiptCoreV0_4

namespace KUOS.ObserveOS
open WORLD VerifyOS LearnOS DecisionOS PlanOS ActOS
namespace WorldHostEffectObservationBridge

abbrev ReceiptA2 := WorldHostEffectObservationReceipt

theorem evidence_collection_is_independent_complete_and_single
    {Bridge : WorldHostEffectObservationBridge K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge}
    (r : ReceiptA2 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge Bridge) :
    r.collection.collectionAuthorized = true ∧ r.collection.rawArtifactCollected = true ∧
      r.collection.valueCollected = true ∧ r.collection.collectorIdentityBound = true ∧
      r.collection.independentSourceIdentityBound = true ∧ r.collection.collectionTimeBound = true ∧
      r.collection.uncertaintyBound = true ∧ r.collection.calibrationBound = true ∧
      r.collection.contextBound = true ∧ r.collection.tamperEvidenceBound = true ∧
      r.collection.provenanceBound = true ∧ r.collection.collectorIndependentFromActOS = true ∧
      r.collection.sourceIndependentFromHostReceipt = true ∧
      r.collection.hostReceiptUsedAsIndependentEvidence = false ∧
      r.collection.collectionCount = 1 := by
  exact ⟨r.collection.authorizationRequired, r.collection.rawRequired,
    r.collection.valueRequired, r.collection.collectorRequired,
    r.collection.sourceRequired, r.collection.timeRequired,
    r.collection.uncertaintyRequired, r.collection.calibrationRequired,
    r.collection.contextRequired, r.collection.tamperRequired,
    r.collection.provenanceRequired, r.collection.collectorIndependenceRequired,
    r.collection.sourceIndependenceRequired,
    r.collection.hostReceiptSubstitutionForbidden,
    r.collection.collectionCountExact⟩

theorem evidence_contract_reuses_world_intake_requirements
    {Bridge : WorldHostEffectObservationBridge K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge}
    (r : ReceiptA2 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge Bridge) :
    r.evidenceRequirements = WorldIntakeBridge.evidenceRequirements ∧
      r.provenance = WorldIntakeBridge.provenanceTrace ∧
      r.provenance.evidenceChainComplete = true ∧
      r.provenance.sourceIdentityPreserved = true ∧
      r.provenance.rawArtifactsImmutable = true ∧
      r.provenance.noUnboundEvidence = true := by
  exact ⟨r.evidenceRequirementsExact, r.provenanceExact,
    r.provenance.chainRequired, r.provenance.sourceRequired,
    r.provenance.immutableRequired, r.provenance.boundRequired⟩

theorem comparison_is_observation_not_verification_truth_or_causality
    {Bridge : WorldHostEffectObservationBridge K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge}
    (r : ReceiptA2 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge Bridge) :
    r.comparison.expectedTargetBound = true ∧
      r.comparison.evidencePacketBound = true ∧
      r.comparison.qualityReportBound = true ∧
      r.comparison.methodBound = true ∧
      r.comparison.comparisonIsVerification = false ∧
      r.comparison.truthAuthority = false ∧
      r.comparison.causalAttribution = false := by
  exact ⟨r.comparison.expectedRequired, r.comparison.evidenceRequired,
    r.comparison.qualityRequired, r.comparison.methodRequired,
    r.comparison.verificationForbidden, r.comparison.truthForbidden,
    r.comparison.causalForbidden⟩

end WorldHostEffectObservationBridge
end KUOS.ObserveOS
