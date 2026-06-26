import KUOS.ActOS.VacuumExpectationActivationAuthorizationIntakeCoreV0_3

namespace KUOS
namespace ActOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS PlanOS

section

variable
    {C : RealHilbertL2Carrier}
    {W : WorldNoncommutativeOperatorAlgebra C}
    [PartialOrder W.Region]
    {B : WorldCStarLocalNetBridge C W}
    {V : WorldVonNeumannBicommutantBridge B}
    {M : WorldStandardFormModularFlowBridge V}
    {R : WorldModularStateKMSRelativeFlowBridge M}
    {E : WorldArakiRelativeEntropyBridge R}
    {P : WorldPetzRecoverySufficiencyBridge E}
    {T : WorldConditionalExpectationTakesakiBridge P}
    {J : WorldJonesBasicConstructionIndexBridge T}
    {S : WorldJonesTowerStandardInvariantBridge J}
    {Q : WorldCanonicalEndomorphismQSystemFrobeniusBridge S}
    {F : WorldBimoduleSectorFusionCategoryBridge Q}
    {Z : WorldModuleCategoryNimrepTubeCenterBridge F}
    {G : WorldGaugeCategoricalIndraNetBridge Z}
    {I : WorldInformationGeometricHigherGaugeBridge G}
    {H : WorldArakiPetzQuantumInformationGeometryBridge I}
    {D : WorldQuantumExponentialDualAffineProjectionBridge H}
    {Vary : WorldQuantumGeodesicMirrorDescentFreeEnergyBridge D}
    {Flow : WorldQuantumGradientJKOEntropyProductionBridge Vary}
    {Mix : WorldQuantumLogSobolevContractivityMixingBridge Flow}
    (K : WorldKuuVacuumOSHilbertCompletionBridge Mix)
    (O : WorldVacuumExpectationObservationBridge K)
    (Intake : WorldVacuumExpectationObserveOSEvidenceIntakeBridge K O)
    (ObserveBridge : VacuumExpectationIntakeCommitBridge K O Intake)
    (VerifyBridge : VacuumExpectationCommitVerificationBridge K O Intake ObserveBridge)
    (LearnBridge : VacuumExpectationVerificationLearningBridge
      K O Intake ObserveBridge VerifyBridge)
    (ReplanBridge : VacuumExpectationLearningReplanIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge)
    (GenerationBridge : VacuumExpectationHistoryQiCandidateGenerationBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge)
    (HandoffBridge : VacuumExpectationHysteresisConstraintDecisionHandoffBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge)
    (SelectionBridge : VacuumExpectationAdmissibleCandidateSelectionBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge)
    (SynthesisBridge : VacuumExpectationSelectedCandidateNextCycleSynthesisBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge)
    (MaterializationBridge : VacuumExpectationCompilerMaterializationBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge)
    (AdmissionBridge : VacuumExpectationActivationAdmissionActOSHandoffBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge)

namespace VacuumExpectationActivationAuthorizationIntakeBridge

variable
    {Bridge : VacuumExpectationActivationAuthorizationIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge}

abbrev ReceiptB2 := VacuumExpectationActivationAuthorizationIntakeReceipt

theorem session_and_intent_are_fresh_distinct_and_nonreplayed
    (r : ReceiptB2 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge Bridge) :
    r.sessionIntent.sessionOpen = true ∧
      r.sessionIntent.sessionIdExact = true ∧
      r.sessionIntent.generationExact = true ∧
      r.sessionIntent.actionIntentBound = true ∧
      r.sessionIntent.actionIntentDistinctFromDecision = true ∧
      r.sessionIntent.intentNonceFresh = true ∧
      r.sessionIntent.intentPreviouslyConsumed = false ∧
      r.sessionIntent.conflictingReplayDetected = false ∧
      r.sessionIntent.exactReceiptReplayIdempotent = true := by
  exact ⟨r.sessionIntent.sessionOpenRequired,
    r.sessionIntent.sessionIdRequired, r.sessionIntent.generationRequired,
    r.sessionIntent.intentRequired, r.sessionIntent.distinctIntentRequired,
    r.sessionIntent.nonceRequired,
    r.sessionIntent.previousConsumptionForbidden,
    r.sessionIntent.conflictForbidden, r.sessionIntent.replayRequired⟩

theorem authorization_is_single_use_and_cannot_widen_license
    (r : ReceiptB2 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge Bridge) :
    r.innerAuthorization.explicitStepAuthorization = true ∧
      r.innerAuthorization.humanApprovalWhenRequired = true ∧
      r.innerAuthorization.singleUse = true ∧
      r.innerAuthorization.doesNotWidenLicense = true ∧
      r.authorizationEnvelope.licenseWidened = false ∧
      r.authorizationEnvelope.executionGrantedByEnvelope = false := by
  exact ⟨r.innerAuthorization.authorizationRequired,
    r.innerAuthorization.approvalRequired,
    r.innerAuthorization.singleUseRequired,
    r.innerAuthorization.noWideningRequired,
    r.authorizationEnvelope.wideningForbidden,
    r.authorizationEnvelope.executionForbidden⟩

end VacuumExpectationActivationAuthorizationIntakeBridge
end
end ActOS
end KUOS
