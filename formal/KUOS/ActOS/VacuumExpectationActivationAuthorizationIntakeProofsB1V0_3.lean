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

abbrev ReceiptB1 := VacuumExpectationActivationAuthorizationIntakeReceipt

theorem lease_reservation_consumes_exactly_one_remaining_use
    (r : ReceiptB1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge Bridge) :
    r.leaseReservation.leaseValid = true ∧
      r.leaseReservation.leaseExpired = false ∧
      0 < r.leaseReservation.remainingUsesBefore ∧
      r.leaseReservation.remainingUsesAfter + 1 =
        r.leaseReservation.remainingUsesBefore ∧
      r.leaseReservation.reservationCount = 1 ∧
      r.leaseReservation.reservationCommitted = true := by
  exact ⟨r.leaseReservation.validityRequired,
    r.leaseReservation.expiryForbidden, r.leaseReservation.remainingPositive,
    r.leaseReservation.decrementExact,
    r.leaseReservation.reservationCountExact,
    r.leaseReservation.reservationRequired⟩

theorem lease_reservation_preserves_holder_scope_session_and_intent
    (r : ReceiptB1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge Bridge) :
    r.leaseReservation.holderExact = true ∧
      r.leaseReservation.scopeExact = true ∧
      r.leaseReservation.sessionExact = true ∧
      r.leaseReservation.intentExact = true := by
  exact ⟨r.leaseReservation.holderRequired,
    r.leaseReservation.scopeRequired, r.leaseReservation.sessionRequired,
    r.leaseReservation.intentRequired⟩

theorem lease_reservation_is_replay_safe
    (r : ReceiptB1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge Bridge) :
    r.leaseReservation.duplicateReservation = false ∧
      r.leaseReservation.exactReplayIdempotent = true := by
  exact ⟨r.leaseReservation.duplicateForbidden,
    r.leaseReservation.replayRequired⟩

end VacuumExpectationActivationAuthorizationIntakeBridge
end
end ActOS
end KUOS
