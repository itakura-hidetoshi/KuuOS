import KUOS.WORLD.VacuumExpectationHostEffectAtomicCommitIntakeCoreV0_52

namespace KUOS.WORLD
open ObserveOS VerifyOS LearnOS DecisionOS PlanOS ActOS
namespace WorldVacuumExpectationHostEffectAtomicCommitIntakeBridge

abbrev EnvelopeB1 := WorldVacuumExpectationHostEffectAtomicCommitIntakeEnvelope

theorem observation_and_verification_debts_remain_unpaid
    {Bridge : WorldVacuumExpectationHostEffectAtomicCommitIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge}
    (envelope : EnvelopeB1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge Bridge) :
    envelope.source.postEffectDebt.effectRecorded = true ∧
      envelope.source.postEffectDebt.observationRequired = true ∧
      envelope.source.postEffectDebt.verificationRequired = true ∧
      envelope.pendingDebt.sourceDebtBound = true ∧
      envelope.pendingDebt.effectRecorded = true ∧
      envelope.pendingDebt.observationRequired = true ∧
      envelope.pendingDebt.verificationRequired = true ∧
      envelope.pendingDebt.observationCommitted = false ∧
      envelope.pendingDebt.verificationCommitted = false ∧
      envelope.pendingDebt.independentWorldEvidencePresent = false := by
  exact ⟨envelope.sourceDebtEffectRecorded,
    envelope.sourceObservationDebt, envelope.sourceVerificationDebt,
    envelope.pendingDebt.debtRequired, envelope.pendingDebt.effectRequired,
    envelope.pendingDebt.observationRequiredProof,
    envelope.pendingDebt.verificationRequiredProof,
    envelope.pendingDebt.observationCommitForbidden,
    envelope.pendingDebt.verificationCommitForbidden,
    envelope.pendingDebt.independentEvidenceNotYetPresent⟩

theorem atomic_commit_prerequisites_are_explicit_but_unsupplied
    {Bridge : WorldVacuumExpectationHostEffectAtomicCommitIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge}
    (envelope : EnvelopeB1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge Bridge) :
    envelope.prerequisites.observeReceiptRequired = true ∧
      envelope.prerequisites.verifyReceiptRequired = true ∧
      envelope.prerequisites.verifiedWorldDispositionRequired = true ∧
      envelope.prerequisites.freshCommitAuthorizationRequired = true ∧
      envelope.prerequisites.successorGenerationRequired = true ∧
      envelope.prerequisites.freshFencingTokenRequired = true ∧
      envelope.prerequisites.optimisticConcurrencyRequired = true ∧
      envelope.prerequisites.observeReceiptSupplied = false ∧
      envelope.prerequisites.verifyReceiptSupplied = false ∧
      envelope.prerequisites.verifiedWorldDispositionSupplied = false ∧
      envelope.prerequisites.freshCommitAuthorizationSupplied = false := by
  exact ⟨envelope.prerequisites.observeRequirement,
    envelope.prerequisites.verifyRequirement,
    envelope.prerequisites.dispositionRequirement,
    envelope.prerequisites.authorizationRequirement,
    envelope.prerequisites.generationRequirement,
    envelope.prerequisites.fencingRequirement,
    envelope.prerequisites.concurrencyRequirement,
    envelope.prerequisites.observeNotYetSupplied,
    envelope.prerequisites.verifyNotYetSupplied,
    envelope.prerequisites.dispositionNotYetSupplied,
    envelope.prerequisites.authorizationNotYetSupplied⟩

end WorldVacuumExpectationHostEffectAtomicCommitIntakeBridge
end KUOS.WORLD
