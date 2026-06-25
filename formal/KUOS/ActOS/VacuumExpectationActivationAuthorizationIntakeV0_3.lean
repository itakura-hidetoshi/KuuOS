import Mathlib
import KUOS.PlanOS.VacuumExpectationActivationAdmissionActOSHandoffV0_23
import KUOS.ActOS.AuthorityBoundInvocationV0_1
import KUOS.ActOS.ReplanLineageAuthorityEnvelopeV0_2

namespace KUOS
namespace ActOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS PlanOS

structure IndependentActFreshnessRevalidation where
  targetCycle : Nat
  adaptiveEpoch : Nat
  capabilityEpoch : Nat
  handoffFresh : Bool
  approvalFresh : Bool
  licenseFresh : Bool
  capabilityFresh : Bool
  leaseFresh : Bool
  sessionFresh : Bool
  intentFresh : Bool
  adaptiveEpochRequired : adaptiveEpoch = targetCycle
  capabilityEpochRequired : capabilityEpoch = adaptiveEpoch
  handoffRequired : handoffFresh = true
  approvalRequired : approvalFresh = true
  licenseRequired : licenseFresh = true
  capabilityRequired : capabilityFresh = true
  leaseRequired : leaseFresh = true
  sessionRequired : sessionFresh = true
  intentRequired : intentFresh = true

structure CapabilityRegistryConfirmation where
  registryEntryPresent : Bool
  registryEntryRevoked : Bool
  ownerExact : Bool
  lineageExact : Bool
  capabilityIdExact : Bool
  adapterKindExact : Bool
  capabilityEpochExact : Bool
  operationAllowed : Bool
  resourceAllowed : Bool
  effectWithinCeiling : Bool
  entryRequired : registryEntryPresent = true
  revocationForbidden : registryEntryRevoked = false
  ownerRequired : ownerExact = true
  lineageRequired : lineageExact = true
  capabilityIdRequired : capabilityIdExact = true
  adapterKindRequired : adapterKindExact = true
  epochRequired : capabilityEpochExact = true
  operationRequired : operationAllowed = true
  resourceRequired : resourceAllowed = true
  effectRequired : effectWithinCeiling = true

structure LeaseUseReservationBoundary where
  leaseValid : Bool
  leaseExpired : Bool
  holderExact : Bool
  scopeExact : Bool
  sessionExact : Bool
  intentExact : Bool
  remainingUsesBefore : Nat
  remainingUsesAfter : Nat
  reservationCount : Nat
  reservationCommitted : Bool
  duplicateReservation : Bool
  exactReplayIdempotent : Bool
  validityRequired : leaseValid = true
  expiryForbidden : leaseExpired = false
  holderRequired : holderExact = true
  scopeRequired : scopeExact = true
  sessionRequired : sessionExact = true
  intentRequired : intentExact = true
  remainingPositive : 0 < remainingUsesBefore
  decrementExact : remainingUsesAfter + 1 = remainingUsesBefore
  reservationCountExact : reservationCount = 1
  reservationRequired : reservationCommitted = true
  duplicateForbidden : duplicateReservation = false
  replayRequired : exactReplayIdempotent = true

structure SessionIntentReplayBoundary where
  sessionOpen : Bool
  sessionIdExact : Bool
  generationExact : Bool
  actionIntentBound : Bool
  actionIntentDistinctFromDecision : Bool
  intentNonceFresh : Bool
  intentPreviouslyConsumed : Bool
  conflictingReplayDetected : Bool
  exactReceiptReplayIdempotent : Bool
  sessionOpenRequired : sessionOpen = true
  sessionIdRequired : sessionIdExact = true
  generationRequired : generationExact = true
  intentRequired : actionIntentBound = true
  distinctIntentRequired : actionIntentDistinctFromDecision = true
  nonceRequired : intentNonceFresh = true
  previousConsumptionForbidden : intentPreviouslyConsumed = false
  conflictForbidden : conflictingReplayDetected = false
  replayRequired : exactReceiptReplayIdempotent = true

structure StagedEffectAuthorizationBoundary where
  selectedStepBound : Bool
  operationInputBound : Bool
  stopConditionsPreserved : Bool
  observationDigestPreserved : Bool
  verificationCriterionPreserved : Bool
  projectedOnly : Bool
  hostAdapterInvoked : Bool
  externalEffectPerformed : Bool
  effectRecordCount : Nat
  stepRequired : selectedStepBound = true
  inputRequired : operationInputBound = true
  stopRequired : stopConditionsPreserved = true
  observationRequired : observationDigestPreserved = true
  verificationRequired : verificationCriterionPreserved = true
  projectionRequired : projectedOnly = true
  invocationForbidden : hostAdapterInvoked = false
  effectForbidden : externalEffectPerformed = false
  recordCountRequired : effectRecordCount = 0

structure ActivationAuthorizationReceiptBoundary where
  handoffIntakeBound : Bool
  freshnessRevalidated : Bool
  capabilityRegistryConfirmed : Bool
  leaseReservationBound : Bool
  sessionIntentConfirmed : Bool
  stagedEffectConfirmed : Bool
  activationAuthorized : Bool
  authorizationCommitted : Bool
  planActivated : Bool
  adapterInvoked : Bool
  externalEffectPerformed : Bool
  effectRecordCount : Nat
  intakeRequired : handoffIntakeBound = true
  freshnessRequired : freshnessRevalidated = true
  registryRequired : capabilityRegistryConfirmed = true
  leaseRequired : leaseReservationBound = true
  sessionIntentRequired : sessionIntentConfirmed = true
  stagedEffectRequired : stagedEffectConfirmed = true
  authorizationRequired : activationAuthorized = true
  commitRequired : authorizationCommitted = true
  activationForbidden : planActivated = false
  invocationForbidden : adapterInvoked = false
  effectForbidden : externalEffectPerformed = false
  recordCountRequired : effectRecordCount = 0

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

structure VacuumExpectationActivationAuthorizationIntakeBridge where
  Digest : Type
  digestOf :
    VacuumExpectationActivationAdmissionActOSHandoffReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge →
    ExactActCycleGate → FivefoldBinding → SelectedActStep →
    AuthorizationBoundary → AuthorizationEnvelopeBoundary →
    IndependentActFreshnessRevalidation → CapabilityRegistryConfirmation →
    LeaseUseReservationBoundary → SessionIntentReplayBoundary →
    StagedEffectAuthorizationBoundary → ActivationAuthorizationReceiptBoundary →
    ActEventIndex → ActEventIndex → ActEventIndex → ActHistory → Digest
  lowerAuthority : LowerAuthorityBoundary
  authorizationOwnedByActOS : Bool
  invocationOwnedByActOS : Bool
  executionOwnedByActOS : Bool
  runtimeActivatesPlan : Bool
  runtimeInvokesAdapter : Bool
  runtimePerformsExternalEffect : Bool
  runtimeCommitsEffectRecord : Bool
  authorizationOwnerRequired : authorizationOwnedByActOS = true
  invocationOwnerRequired : invocationOwnedByActOS = true
  executionOwnerRequired : executionOwnedByActOS = true
  activationForbidden : runtimeActivatesPlan = false
  invocationForbidden : runtimeInvokesAdapter = false
  effectForbidden : runtimePerformsExternalEffect = false
  effectRecordForbidden : runtimeCommitsEffectRecord = false

structure VacuumExpectationActivationAuthorizationIntakeReceipt
    (Bridge : VacuumExpectationActivationAuthorizationIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge) where
  source : VacuumExpectationActivationAdmissionActOSHandoffReceipt
    K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge
  exactActCycle : ExactActCycleGate
  fivefold : FivefoldBinding
  selectedStep : SelectedActStep
  innerAuthorization : AuthorizationBoundary
  authorizationEnvelope : AuthorizationEnvelopeBoundary
  freshness : IndependentActFreshnessRevalidation
  registry : CapabilityRegistryConfirmation
  leaseReservation : LeaseUseReservationBoundary
  sessionIntent : SessionIntentReplayBoundary
  stagedEffect : StagedEffectAuthorizationBoundary
  authorization : ActivationAuthorizationReceiptBoundary
  intakeIndex : ActEventIndex
  authorizationIndex : ActEventIndex
  reservationIndex : ActEventIndex
  historyAfter : ActHistory
  digest : Bridge.Digest
  sourceBound : Bool
  sourceRequired : sourceBound = true
  sourceHandoffCommitted : source.handoff.handoffCommitted = true
  sourceAdmissionCommitted : source.admission.admitted = true
  sourceNotActivated : source.handoff.activated = false
  sourceNotExecuted : source.handoff.executed = false
  sourceLeaseNotReserved : source.handoff.leaseUseReserved = false
  actPlanCycleExact : exactActCycle.planCycle = source.freshness.targetCycle
  freshnessTargetExact : freshness.targetCycle = source.freshness.targetCycle
  freshnessAdaptiveExact : freshness.adaptiveEpoch = source.freshness.adaptiveEpoch
  freshnessCapabilityExact :
    freshness.capabilityEpoch = source.freshness.capabilityEpoch
  intakeIndexExact : intakeIndex.current = source.handoffIndex.current + 1
  authorizationIndexExact : authorizationIndex = intakeIndex.append
  reservationIndexExact : reservationIndex = authorizationIndex.append
  historyExact : historyAfter.committedRecords =
    source.historyAfter.committedRecords + 3
  digestExact : digest = Bridge.digestOf source exactActCycle fivefold selectedStep
    innerAuthorization authorizationEnvelope freshness registry leaseReservation
    sessionIntent stagedEffect authorization intakeIndex authorizationIndex
    reservationIndex historyAfter

namespace VacuumExpectationActivationAuthorizationIntakeBridge

variable
    {Bridge : VacuumExpectationActivationAuthorizationIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge}

local notation "Receipt" =>
  VacuumExpectationActivationAuthorizationIntakeReceipt
    K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge Bridge

theorem intake_requires_committed_nonexecuting_planos_handoff (r : Receipt) :
    r.sourceBound = true ∧ r.source.handoff.handoffCommitted = true ∧
      r.source.admission.admitted = true ∧
      r.source.handoff.activated = false ∧
      r.source.handoff.executed = false ∧
      r.source.handoff.leaseUseReserved = false := by
  exact ⟨r.sourceRequired, r.sourceHandoffCommitted, r.sourceAdmissionCommitted,
    r.sourceNotActivated, r.sourceNotExecuted, r.sourceLeaseNotReserved⟩

theorem exact_act_cycle_revalidates_planos_target (r : Receipt) :
    r.exactActCycle.actCycle = r.source.freshness.targetCycle ∧
      r.exactActCycle.actPhase = true := by
  constructor
  · calc
      r.exactActCycle.actCycle = r.exactActCycle.planCycle :=
        lineage_handoff_uses_exact_act_cycle r.exactActCycle
      _ = r.source.freshness.targetCycle := r.actPlanCycleExact
  · exact lineage_handoff_requires_act_phase r.exactActCycle

theorem fivefold_binding_is_complete (r : Receipt) :
    r.fivefold.committedPlanBound = true ∧
      r.fivefold.exactStepBound = true ∧
      r.fivefold.actPhaseBound = true ∧
      r.fivefold.hostLicenseBound = true ∧
      r.fivefold.projectionReceiptBound = true := by
  exact ⟨r.fivefold.planRequired, r.fivefold.stepRequired,
    r.fivefold.actPhaseRequired, r.fivefold.licenseRequired,
    r.fivefold.projectionRequired⟩

theorem selected_step_is_effectful_and_safety_bound (r : Receipt) :
    r.selectedStep.isActCandidate = true ∧
      r.selectedStep.effectful = true ∧
      r.selectedStep.stopConditionsPresent = true ∧
      r.selectedStep.observationDigestPresent = true ∧
      r.selectedStep.verificationCriterionPresent = true := by
  exact ⟨r.selectedStep.candidateRequired, r.selectedStep.effectRequired,
    r.selectedStep.stopRequired, r.selectedStep.observationRequired,
    r.selectedStep.verificationRequired⟩

theorem freshness_is_independently_revalidated (r : Receipt) :
    r.freshness.targetCycle = r.source.freshness.targetCycle ∧
      r.freshness.adaptiveEpoch = r.source.freshness.adaptiveEpoch ∧
      r.freshness.capabilityEpoch = r.source.freshness.capabilityEpoch ∧
      r.freshness.handoffFresh = true ∧
      r.freshness.approvalFresh = true ∧
      r.freshness.licenseFresh = true ∧
      r.freshness.capabilityFresh = true ∧
      r.freshness.leaseFresh = true ∧
      r.freshness.sessionFresh = true ∧
      r.freshness.intentFresh = true := by
  exact ⟨r.freshnessTargetExact, r.freshnessAdaptiveExact,
    r.freshnessCapabilityExact, r.freshness.handoffRequired,
    r.freshness.approvalRequired, r.freshness.licenseRequired,
    r.freshness.capabilityRequired, r.freshness.leaseRequired,
    r.freshness.sessionRequired, r.freshness.intentRequired⟩

theorem freshness_epochs_match_exact_target (r : Receipt) :
    r.freshness.adaptiveEpoch = r.freshness.targetCycle ∧
      r.freshness.capabilityEpoch = r.freshness.adaptiveEpoch := by
  exact ⟨r.freshness.adaptiveEpochRequired,
    r.freshness.capabilityEpochRequired⟩

theorem registry_entry_is_present_unrevoked_and_exact (r : Receipt) :
    r.registry.registryEntryPresent = true ∧
      r.registry.registryEntryRevoked = false ∧
      r.registry.ownerExact = true ∧ r.registry.lineageExact = true ∧
      r.registry.capabilityIdExact = true ∧
      r.registry.adapterKindExact = true ∧
      r.registry.capabilityEpochExact = true := by
  exact ⟨r.registry.entryRequired, r.registry.revocationForbidden,
    r.registry.ownerRequired, r.registry.lineageRequired,
    r.registry.capabilityIdRequired, r.registry.adapterKindRequired,
    r.registry.epochRequired⟩

theorem registry_scope_and_effect_are_allowed (r : Receipt) :
    r.registry.operationAllowed = true ∧
      r.registry.resourceAllowed = true ∧
      r.registry.effectWithinCeiling = true := by
  exact ⟨r.registry.operationRequired, r.registry.resourceRequired,
    r.registry.effectRequired⟩

theorem lease_reservation_consumes_exactly_one_remaining_use (r : Receipt) :
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

theorem lease_reservation_preserves_holder_scope_session_and_intent (r : Receipt) :
    r.leaseReservation.holderExact = true ∧
      r.leaseReservation.scopeExact = true ∧
      r.leaseReservation.sessionExact = true ∧
      r.leaseReservation.intentExact = true := by
  exact ⟨r.leaseReservation.holderRequired,
    r.leaseReservation.scopeRequired, r.leaseReservation.sessionRequired,
    r.leaseReservation.intentRequired⟩

theorem lease_reservation_is_replay_safe (r : Receipt) :
    r.leaseReservation.duplicateReservation = false ∧
      r.leaseReservation.exactReplayIdempotent = true := by
  exact ⟨r.leaseReservation.duplicateForbidden,
    r.leaseReservation.replayRequired⟩

theorem session_and_intent_are_fresh_distinct_and_nonreplayed (r : Receipt) :
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

theorem authorization_is_single_use_and_cannot_widen_license (r : Receipt) :
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

theorem authorization_envelope_preserves_operation_receipts_and_approval
    (r : Receipt) :
    r.authorizationEnvelope.innerAuthorizationCanonical = true ∧
      r.authorizationEnvelope.innerAuthorizationUnchanged = true ∧
      r.authorizationEnvelope.operationIdentityPreserved = true ∧
      r.authorizationEnvelope.operationInputPreserved = true ∧
      r.authorizationEnvelope.actReceiptPreserved = true ∧
      r.authorizationEnvelope.hostLicensePreserved = true ∧
      r.authorizationEnvelope.humanApprovalPreserved = true := by
  exact ⟨r.authorizationEnvelope.canonicalRequired,
    r.authorizationEnvelope.unchangedRequired,
    r.authorizationEnvelope.operationRequired,
    r.authorizationEnvelope.inputRequired,
    r.authorizationEnvelope.actRequired,
    r.authorizationEnvelope.hostRequired,
    r.authorizationEnvelope.humanRequired⟩

theorem staged_effect_remains_projected_and_noninvoked (r : Receipt) :
    r.stagedEffect.selectedStepBound = true ∧
      r.stagedEffect.operationInputBound = true ∧
      r.stagedEffect.stopConditionsPreserved = true ∧
      r.stagedEffect.observationDigestPreserved = true ∧
      r.stagedEffect.verificationCriterionPreserved = true ∧
      r.stagedEffect.projectedOnly = true ∧
      r.stagedEffect.hostAdapterInvoked = false ∧
      r.stagedEffect.externalEffectPerformed = false ∧
      r.stagedEffect.effectRecordCount = 0 := by
  exact ⟨r.stagedEffect.stepRequired, r.stagedEffect.inputRequired,
    r.stagedEffect.stopRequired, r.stagedEffect.observationRequired,
    r.stagedEffect.verificationRequired, r.stagedEffect.projectionRequired,
    r.stagedEffect.invocationForbidden, r.stagedEffect.effectForbidden,
    r.stagedEffect.recordCountRequired⟩

theorem activation_authorization_is_committed_without_activation_or_effect
    (r : Receipt) :
    r.authorization.handoffIntakeBound = true ∧
      r.authorization.freshnessRevalidated = true ∧
      r.authorization.capabilityRegistryConfirmed = true ∧
      r.authorization.leaseReservationBound = true ∧
      r.authorization.sessionIntentConfirmed = true ∧
      r.authorization.stagedEffectConfirmed = true ∧
      r.authorization.activationAuthorized = true ∧
      r.authorization.authorizationCommitted = true ∧
      r.authorization.planActivated = false ∧
      r.authorization.adapterInvoked = false ∧
      r.authorization.externalEffectPerformed = false ∧
      r.authorization.effectRecordCount = 0 := by
  exact ⟨r.authorization.intakeRequired, r.authorization.freshnessRequired,
    r.authorization.registryRequired, r.authorization.leaseRequired,
    r.authorization.sessionIntentRequired, r.authorization.stagedEffectRequired,
    r.authorization.authorizationRequired, r.authorization.commitRequired,
    r.authorization.activationForbidden, r.authorization.invocationForbidden,
    r.authorization.effectForbidden, r.authorization.recordCountRequired⟩

theorem act_events_append_strictly_from_planos_handoff (r : Receipt) :
    r.source.handoffIndex.current < r.intakeIndex.current ∧
      r.intakeIndex.current < r.authorizationIndex.current ∧
      r.authorizationIndex.current < r.reservationIndex.current := by
  constructor
  · rw [r.intakeIndexExact]
    omega
  constructor
  · rw [r.authorizationIndexExact]
    exact actEventIndex_strict r.intakeIndex
  · rw [r.reservationIndexExact]
    exact actEventIndex_strict r.authorizationIndex

theorem act_history_appends_three_records (r : Receipt) :
    r.historyAfter.committedRecords = r.source.historyAfter.committedRecords + 3 ∧
      r.historyAfter.snapshotRecords = r.source.historyAfter.committedRecords + 3 := by
  refine ⟨r.historyExact, ?_⟩
  rw [actHistory_snapshot_matches_commits r.historyAfter]
  exact r.historyExact

theorem bridge_preserves_actos_ownership (_r : Receipt) :
    Bridge.authorizationOwnedByActOS = true ∧
      Bridge.invocationOwnedByActOS = true ∧
      Bridge.executionOwnedByActOS = true := by
  exact ⟨Bridge.authorizationOwnerRequired, Bridge.invocationOwnerRequired,
    Bridge.executionOwnerRequired⟩

theorem bridge_grants_no_activation_invocation_or_effect (_r : Receipt) :
    Bridge.runtimeActivatesPlan = false ∧
      Bridge.runtimeInvokesAdapter = false ∧
      Bridge.runtimePerformsExternalEffect = false ∧
      Bridge.runtimeCommitsEffectRecord = false ∧
      Bridge.lowerAuthority.lowerAuthorityPreserved = true ∧
      Bridge.lowerAuthority.clinicalAuthority = false ∧
      Bridge.lowerAuthority.legalAuthority = false ∧
      Bridge.lowerAuthority.institutionalAuthority = false ∧
      Bridge.lowerAuthority.theoremAuthority = false := by
  exact ⟨Bridge.activationForbidden, Bridge.invocationForbidden,
    Bridge.effectForbidden, Bridge.effectRecordForbidden,
    Bridge.lowerAuthority.lowerRequired,
    Bridge.lowerAuthority.clinicalForbidden,
    Bridge.lowerAuthority.legalForbidden,
    Bridge.lowerAuthority.institutionalForbidden,
    Bridge.lowerAuthority.theoremForbidden⟩

theorem authorization_digest_is_exact (r : Receipt) :
    r.digest = Bridge.digestOf r.source r.exactActCycle r.fivefold
      r.selectedStep r.innerAuthorization r.authorizationEnvelope r.freshness
      r.registry r.leaseReservation r.sessionIntent r.stagedEffect
      r.authorization r.intakeIndex r.authorizationIndex r.reservationIndex
      r.historyAfter := by
  exact r.digestExact

end VacuumExpectationActivationAuthorizationIntakeBridge
end
end ActOS
end KUOS
