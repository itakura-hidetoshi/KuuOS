import KUOS.WORLD.VacuumExpectationHostEffectAtomicCommitIntakeCoreV0_52

namespace KUOS.WORLD
open ObserveOS VerifyOS LearnOS DecisionOS PlanOS ActOS
namespace WorldVacuumExpectationHostEffectAtomicCommitIntakeBridge

abbrev EnvelopeA2 := WorldVacuumExpectationHostEffectAtomicCommitIntakeEnvelope

theorem evidence_requirements_are_complete
    {Bridge : WorldVacuumExpectationHostEffectAtomicCommitIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge}
    (_envelope : EnvelopeA2 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge Bridge) :
    Bridge.evidenceRequirements.rawArtifactDigest = true ∧
      Bridge.evidenceRequirements.valueDigest = true ∧
      Bridge.evidenceRequirements.collectorIdentity = true ∧
      Bridge.evidenceRequirements.independentSourceIdentity = true ∧
      Bridge.evidenceRequirements.collectionTime = true ∧
      Bridge.evidenceRequirements.uncertaintyDigest = true ∧
      Bridge.evidenceRequirements.calibrationDigest = true ∧
      Bridge.evidenceRequirements.contextDigest = true ∧
      Bridge.evidenceRequirements.tamperEvidenceDigest = true ∧
      Bridge.evidenceRequirements.provenanceChain = true := by
  exact ⟨Bridge.evidenceRequirements.rawRequired,
    Bridge.evidenceRequirements.valueRequired,
    Bridge.evidenceRequirements.collectorRequired,
    Bridge.evidenceRequirements.sourceRequired,
    Bridge.evidenceRequirements.timeRequired,
    Bridge.evidenceRequirements.uncertaintyRequired,
    Bridge.evidenceRequirements.calibrationRequired,
    Bridge.evidenceRequirements.contextRequired,
    Bridge.evidenceRequirements.tamperRequired,
    Bridge.evidenceRequirements.provenanceRequired⟩

theorem provenance_is_complete_and_immutable
    {Bridge : WorldVacuumExpectationHostEffectAtomicCommitIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge}
    (_envelope : EnvelopeA2 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge Bridge) :
    Bridge.provenanceTrace.evidenceChainComplete = true ∧
      Bridge.provenanceTrace.sourceIdentityPreserved = true ∧
      Bridge.provenanceTrace.rawArtifactsImmutable = true ∧
      Bridge.provenanceTrace.noUnboundEvidence = true := by
  exact provenance_trace_preserves_sources Bridge.provenanceTrace

end WorldVacuumExpectationHostEffectAtomicCommitIntakeBridge
end KUOS.WORLD
