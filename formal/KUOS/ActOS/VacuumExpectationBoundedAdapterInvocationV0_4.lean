import Mathlib
import KUOS.ActOS.VacuumExpectationActivationAuthorizationIntakeV0_3

namespace KUOS
namespace ActOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS PlanOS

structure ActOSPlanActivationBoundary where
  authorizationBound : Bool
  leaseReservationBound : Bool
  sessionIntentBound : Bool
  activationCommitted : Bool
  activationCount : Nat
  adapterInvoked : Bool
  externalEffectPerformed : Bool
  effectRecordCount : Nat
  authorizationRequired : authorizationBound = true
  reservationRequired : leaseReservationBound = true
  sessionIntentRequired : sessionIntentBound = true
  activationRequired : activationCommitted = true
  activationCountExact : activationCount = 1
  invocationForbidden : adapterInvoked = false
  effectForbidden : externalEffectPerformed = false
  recordCountRequired : effectRecordCount = 0

structure ExactAdapterInvocationBinding where
  activationReceiptBound : Bool
  authorizationReceiptBound : Bool
  leaseReservationReceiptBound : Bool
  selectedStepExact : Bool
  operationIdentityExact : Bool
  operationInputExact : Bool
  targetCycleExact : Bool
  adaptiveEpochExact : Bool
  capabilityEpochExact : Bool
  sessionExact : Bool
  actionIntentExact : Bool
  adapterKindExact : Bool
  hostLicenseExact : Bool
  capabilityExact : Bool
  activationRequired : activationReceiptBound = true
  authorizationRequired : authorizationReceiptBound = true
  reservationRequired : leaseReservationReceiptBound = true
  stepRequired : selectedStepExact = true
  operationRequired : operationIdentityExact = true
  inputRequired : operationInputExact = true
  targetCycleRequired : targetCycleExact = true
  adaptiveEpochRequired : adaptiveEpochExact = true
  capabilityEpochRequired : capabilityEpochExact = true
  sessionRequired : sessionExact = true
  intentRequired : actionIntentExact = true
  adapterRequired : adapterKindExact = true
  licenseRequired : hostLicenseExact = true
  capabilityRequired : capabilityExact = true

structure AdapterInvocationProjectionBoundary where
  selectedStepBound : Bool
  operationIdentityBound : Bool
  operationInputBound : Bool
  resourceScopeBound : Bool
  stopConditionsPreserved : Bool
  observationDigestPreserved : Bool
  verificationCriterionPreserved : Bool
  projectedEffectWithinCapability : Bool
  projectedEffectWithinLease : Bool
  projectedOnly : Bool
  stepRequired : selectedStepBound = true
  operationRequired : operationIdentityBound = true
  inputRequired : operationInputBound = true
  resourceRequired : resourceScopeBound = true
  stopRequired : stopConditionsPreserved = true
  observationRequired : observationDigestPreserved = true
  verificationRequired : verificationCriterionPreserved = true
  capabilityRequired : projectedEffectWithinCapability = true
  leaseRequired : projectedEffectWithinLease = true
  projectionRequired : projectedOnly = true

structure AdapterInvocationRouteBoundary where
  route : HostRoute
  invocationAttempted : Bool
  hostAdapterCalled : Bool
  externalEffectPerformed : Bool
  effectRecordCount : Nat
  effectRecordedRule : route = .effectRecorded →
    invocationAttempted = true ∧ hostAdapterCalled = true ∧
      externalEffectPerformed = true ∧ effectRecordCount = 1
  blockedRule : route = .blocked →
    invocationAttempted = true ∧ hostAdapterCalled = false ∧
      externalEffectPerformed = false ∧ effectRecordCount = 0
  replayedRule : route = .replayed →
    invocationAttempted = false ∧ hostAdapterCalled = false ∧
      externalEffectPerformed = false ∧ effectRecordCount = 0

structure CanonicalHostInvocationReceiptBinding where
  activationReceiptBound : Bool
  invocationReceiptBound : Bool
  operationIdentityPreserved : Bool
  operationInputPreserved : Bool
  selectedStepPreserved : Bool
  targetCyclePreserved : Bool
  sessionPreserved : Bool
  actionIntentPreserved : Bool
  leaseReservationConsumed : Bool
  hostReceiptCanonical : Bool
  worldCommitPerformed : Bool
  activationRequired : activationReceiptBound = true
  invocationRequired : invocationReceiptBound = true
  operationRequired : operationIdentityPreserved = true
  inputRequired : operationInputPreserved = true
  stepRequired : selectedStepPreserved = true
  targetCycleRequired : targetCyclePreserved = true
  sessionRequired : sessionPreserved = true
  intentRequired : actionIntentPreserved = true
  leaseRequired : leaseReservationConsumed = true
  canonicalRequired : hostReceiptCanonical = true
  worldCommitForbidden : worldCommitPerformed = false

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
    (AuthorizationBridge : VacuumExpectationActivationAuthorizationIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge)

structure VacuumExpectationBoundedAdapterInvocationBridge where
  Digest : Type
  digestOf :
    VacuumExpectationActivationAuthorizationIntakeReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge →
    ActOSPlanActivationBoundary → ExactAdapterInvocationBinding →
    AdapterInvocationProjectionBoundary → BoundedInvocation →
    AdapterInvocationRouteBoundary → HostReceiptSemantics →
    CanonicalHostInvocationReceiptBinding → PostEffectDebt →
    ActEventIndex → ActEventIndex → ActEventIndex → ActHistory → Digest
  lowerAuthority : LowerAuthorityBoundary
  activationOwnedByActOS : Bool
  invocationOwnedByActOS : Bool
  hostReceiptOwnedByHost : Bool
  worldCommitOwnedByWorld : Bool
  worldCommitPerformed : Bool
  automaticTruthPromotion : Bool
  automaticPlanCompletion : Bool
  automaticRollback : Bool
  activationOwnerRequired : activationOwnedByActOS = true
  invocationOwnerRequired : invocationOwnedByActOS = true
  hostOwnerRequired : hostReceiptOwnedByHost = true
  worldOwnerRequired : worldCommitOwnedByWorld = true
  worldCommitForbidden : worldCommitPerformed = false
  truthPromotionForbidden : automaticTruthPromotion = false
  planCompletionForbidden : automaticPlanCompletion = false
  rollbackForbidden : automaticRollback = false

structure VacuumExpectationBoundedAdapterInvocationReceipt
    (Bridge : VacuumExpectationBoundedAdapterInvocationBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge) where
  source : VacuumExpectationActivationAuthorizationIntakeReceipt
    K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge AuthorizationBridge
  activation : ActOSPlanActivationBoundary
  binding : ExactAdapterInvocationBinding
  projection : AdapterInvocationProjectionBoundary
  invocation : BoundedInvocation
  route : AdapterInvocationRouteBoundary
  hostReceipt : HostReceiptSemantics
  hostBinding : CanonicalHostInvocationReceiptBinding
  postEffectDebt : PostEffectDebt
  activationIndex : ActEventIndex
  invocationIndex : ActEventIndex
  hostReceiptIndex : ActEventIndex
  historyAfter : ActHistory
  digest : Bridge.Digest
  sourceBound : Bool
  sourceRequired : sourceBound = true
  sourceAuthorizationCommitted : source.authorization.authorizationCommitted = true
  sourceActivationAuthorized : source.authorization.activationAuthorized = true
  sourceNotActivated : source.authorization.planActivated = false
  sourceNotInvoked : source.authorization.adapterInvoked = false
  sourceNoEffect : source.authorization.externalEffectPerformed = false
  sourceNoEffectRecord : source.authorization.effectRecordCount = 0
  sourceReservationCommitted : source.leaseReservation.reservationCommitted = true
  sourceReservationCountExact : source.leaseReservation.reservationCount = 1
  hostRouteExact : hostReceipt.route = route.route
  hostEffectCountExact : hostReceipt.effectRecordCount = route.effectRecordCount
  effectRecordedUsesOneBoundedSlice : hostReceipt.route = .effectRecorded →
    invocation.jobsClaimed = 1 ∧ invocation.slicesRun = 1
  replayUsesNoNewInvocation : hostReceipt.route = .replayed →
    invocation.jobsClaimed = 0 ∧ invocation.slicesRun = 0
  effectDebtExact : hostReceipt.route = .effectRecorded →
    postEffectDebt.effectRecorded = true
  blockedDebtExact : hostReceipt.route = .blocked →
    postEffectDebt.effectRecorded = false
  replayDebtExact : hostReceipt.route = .replayed →
    postEffectDebt.effectRecorded = false
  activationIndexExact : activationIndex = source.reservationIndex.append
  invocationIndexExact : invocationIndex = activationIndex.append
  hostReceiptIndexExact : hostReceiptIndex = invocationIndex.append
  historyExact : historyAfter.committedRecords =
    source.historyAfter.committedRecords + 3
  digestExact : digest = Bridge.digestOf source activation binding projection
    invocation route hostReceipt hostBinding postEffectDebt activationIndex
    invocationIndex hostReceiptIndex historyAfter

namespace VacuumExpectationBoundedAdapterInvocationBridge

variable
    {Bridge : VacuumExpectationBoundedAdapterInvocationBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge}

local notation "Receipt" =>
  VacuumExpectationBoundedAdapterInvocationReceipt
    K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge AuthorizationBridge Bridge

theorem invocation_requires_committed_nonexecuting_authorization (r : Receipt) :
    r.sourceBound = true ∧
      r.source.authorization.authorizationCommitted = true ∧
      r.source.authorization.activationAuthorized = true ∧
      r.source.authorization.planActivated = false ∧
      r.source.authorization.adapterInvoked = false ∧
      r.source.authorization.externalEffectPerformed = false ∧
      r.source.authorization.effectRecordCount = 0 := by
  exact ⟨r.sourceRequired, r.sourceAuthorizationCommitted,
    r.sourceActivationAuthorized, r.sourceNotActivated, r.sourceNotInvoked,
    r.sourceNoEffect, r.sourceNoEffectRecord⟩

theorem invocation_consumes_exact_reserved_lease_use (r : Receipt) :
    r.source.leaseReservation.reservationCommitted = true ∧
      r.source.leaseReservation.reservationCount = 1 ∧
      r.hostBinding.leaseReservationConsumed = true := by
  exact ⟨r.sourceReservationCommitted, r.sourceReservationCountExact,
    r.hostBinding.leaseRequired⟩

theorem activation_is_committed_before_invocation_without_effect (r : Receipt) :
    r.activation.authorizationBound = true ∧
      r.activation.leaseReservationBound = true ∧
      r.activation.sessionIntentBound = true ∧
      r.activation.activationCommitted = true ∧
      r.activation.activationCount = 1 ∧
      r.activation.adapterInvoked = false ∧
      r.activation.externalEffectPerformed = false ∧
      r.activation.effectRecordCount = 0 := by
  exact ⟨r.activation.authorizationRequired, r.activation.reservationRequired,
    r.activation.sessionIntentRequired, r.activation.activationRequired,
    r.activation.activationCountExact, r.activation.invocationForbidden,
    r.activation.effectForbidden, r.activation.recordCountRequired⟩

theorem exact_invocation_binding_is_complete (r : Receipt) :
    r.binding.activationReceiptBound = true ∧
      r.binding.authorizationReceiptBound = true ∧
      r.binding.leaseReservationReceiptBound = true ∧
      r.binding.selectedStepExact = true ∧
      r.binding.operationIdentityExact = true ∧
      r.binding.operationInputExact = true ∧
      r.binding.targetCycleExact = true ∧
      r.binding.adaptiveEpochExact = true ∧
      r.binding.capabilityEpochExact = true ∧
      r.binding.sessionExact = true ∧
      r.binding.actionIntentExact = true ∧
      r.binding.adapterKindExact = true ∧
      r.binding.hostLicenseExact = true ∧
      r.binding.capabilityExact = true := by
  exact ⟨r.binding.activationRequired, r.binding.authorizationRequired,
    r.binding.reservationRequired, r.binding.stepRequired,
    r.binding.operationRequired, r.binding.inputRequired,
    r.binding.targetCycleRequired, r.binding.adaptiveEpochRequired,
    r.binding.capabilityEpochRequired, r.binding.sessionRequired,
    r.binding.intentRequired, r.binding.adapterRequired,
    r.binding.licenseRequired, r.binding.capabilityRequired⟩

theorem invocation_projection_preserves_safety_and_effect_ceilings (r : Receipt) :
    r.projection.selectedStepBound = true ∧
      r.projection.operationIdentityBound = true ∧
      r.projection.operationInputBound = true ∧
      r.projection.resourceScopeBound = true ∧
      r.projection.stopConditionsPreserved = true ∧
      r.projection.observationDigestPreserved = true ∧
      r.projection.verificationCriterionPreserved = true ∧
      r.projection.projectedEffectWithinCapability = true ∧
      r.projection.projectedEffectWithinLease = true ∧
      r.projection.projectedOnly = true := by
  exact ⟨r.projection.stepRequired, r.projection.operationRequired,
    r.projection.inputRequired, r.projection.resourceRequired,
    r.projection.stopRequired, r.projection.observationRequired,
    r.projection.verificationRequired, r.projection.capabilityRequired,
    r.projection.leaseRequired, r.projection.projectionRequired⟩

theorem adapter_invocation_is_bounded (r : Receipt) :
    r.invocation.jobsClaimed ≤ 1 ∧ r.invocation.slicesRun ≤ 1 := by
  exact ⟨r.invocation.jobsBounded, r.invocation.slicesBounded⟩

theorem effect_recorded_route_invokes_once_and_records_once
    (r : Receipt) (hroute : r.hostReceipt.route = .effectRecorded) :
    r.route.invocationAttempted = true ∧
      r.route.hostAdapterCalled = true ∧
      r.route.externalEffectPerformed = true ∧
      r.hostReceipt.effectRecordCount = 1 ∧
      r.invocation.jobsClaimed = 1 ∧ r.invocation.slicesRun = 1 := by
  have routeExact : r.route.route = .effectRecorded := by
    rw [← r.hostRouteExact]
    exact hroute
  have h := r.route.effectRecordedRule routeExact
  have hostCount : r.hostReceipt.effectRecordCount = 1 := by
    exact effectRecorded_means_one_record r.hostReceipt hroute
  have bounded := r.effectRecordedUsesOneBoundedSlice hroute
  exact ⟨h.1, h.2.1, h.2.2.1, hostCount, bounded.1, bounded.2⟩

theorem blocked_route_has_no_call_effect_or_record
    (r : Receipt) (hroute : r.hostReceipt.route = .blocked) :
    r.route.invocationAttempted = true ∧
      r.route.hostAdapterCalled = false ∧
      r.route.externalEffectPerformed = false ∧
      r.hostReceipt.effectRecordCount = 0 := by
  have routeExact : r.route.route = .blocked := by
    rw [← r.hostRouteExact]
    exact hroute
  have h := r.route.blockedRule routeExact
  have hostCount := blocked_records_no_effect r.hostReceipt hroute
  exact ⟨h.1, h.2.1, h.2.2.1, hostCount⟩

theorem replayed_route_is_idempotent_and_starts_no_new_invocation
    (r : Receipt) (hroute : r.hostReceipt.route = .replayed) :
    r.route.invocationAttempted = false ∧
      r.route.hostAdapterCalled = false ∧
      r.route.externalEffectPerformed = false ∧
      r.route.effectRecordCount = 0 ∧
      r.invocation.jobsClaimed = 0 ∧ r.invocation.slicesRun = 0 := by
  have routeExact : r.route.route = .replayed := by
    rw [← r.hostRouteExact]
    exact hroute
  have h := r.route.replayedRule routeExact
  have noInvocation := r.replayUsesNoNewInvocation hroute
  exact ⟨h.1, h.2.1, h.2.2.1, h.2.2.2, noInvocation.1,
    noInvocation.2⟩

theorem host_receipt_is_canonical_and_preserves_identity (r : Receipt) :
    r.hostBinding.activationReceiptBound = true ∧
      r.hostBinding.invocationReceiptBound = true ∧
      r.hostBinding.operationIdentityPreserved = true ∧
      r.hostBinding.operationInputPreserved = true ∧
      r.hostBinding.selectedStepPreserved = true ∧
      r.hostBinding.targetCyclePreserved = true ∧
      r.hostBinding.sessionPreserved = true ∧
      r.hostBinding.actionIntentPreserved = true ∧
      r.hostBinding.hostReceiptCanonical = true := by
  exact ⟨r.hostBinding.activationRequired, r.hostBinding.invocationRequired,
    r.hostBinding.operationRequired, r.hostBinding.inputRequired,
    r.hostBinding.stepRequired, r.hostBinding.targetCycleRequired,
    r.hostBinding.sessionRequired, r.hostBinding.intentRequired,
    r.hostBinding.canonicalRequired⟩

theorem host_route_and_effect_count_are_exact (r : Receipt) :
    r.hostReceipt.route = r.route.route ∧
      r.hostReceipt.effectRecordCount = r.route.effectRecordCount := by
  exact ⟨r.hostRouteExact, r.hostEffectCountExact⟩

theorem effect_recorded_preserves_observation_and_verification_debt
    (r : Receipt) (hroute : r.hostReceipt.route = .effectRecorded) :
    r.postEffectDebt.observationRequired = true ∧
      r.postEffectDebt.verificationRequired = true := by
  have hdebt : r.postEffectDebt.effectRecorded = true := r.effectDebtExact hroute
  exact ⟨effect_preserves_observation_debt r.postEffectDebt hdebt,
    effect_preserves_verification_debt r.postEffectDebt hdebt⟩

theorem blocked_or_replayed_records_no_posteffect_effect
    (r : Receipt)
    (hroute : r.hostReceipt.route = .blocked ∨
      r.hostReceipt.route = .replayed) :
    r.postEffectDebt.effectRecorded = false := by
  cases hroute with
  | inl h => exact r.blockedDebtExact h
  | inr h => exact r.replayDebtExact h

theorem posteffect_debt_grants_no_automatic_promotion_completion_or_rollback
    (r : Receipt) :
    r.postEffectDebt.automaticTruthPromotion = false ∧
      r.postEffectDebt.automaticPlanCompletion = false ∧
      r.postEffectDebt.automaticRollback = false := by
  exact ⟨r.postEffectDebt.truthPromotionForbidden,
    r.postEffectDebt.planCompletionForbidden,
    r.postEffectDebt.rollbackForbidden⟩

theorem invocation_events_append_strictly (r : Receipt) :
    r.source.reservationIndex.current < r.activationIndex.current ∧
      r.activationIndex.current < r.invocationIndex.current ∧
      r.invocationIndex.current < r.hostReceiptIndex.current := by
  constructor
  · rw [r.activationIndexExact]
    exact actEventIndex_strict r.source.reservationIndex
  constructor
  · rw [r.invocationIndexExact]
    exact actEventIndex_strict r.activationIndex
  · rw [r.hostReceiptIndexExact]
    exact actEventIndex_strict r.invocationIndex

theorem invocation_history_appends_three_records (r : Receipt) :
    r.historyAfter.committedRecords = r.source.historyAfter.committedRecords + 3 ∧
      r.historyAfter.snapshotRecords = r.source.historyAfter.committedRecords + 3 := by
  refine ⟨r.historyExact, ?_⟩
  rw [actHistory_snapshot_matches_commits r.historyAfter]
  exact r.historyExact

theorem bridge_preserves_separated_ownership (_r : Receipt) :
    Bridge.activationOwnedByActOS = true ∧
      Bridge.invocationOwnedByActOS = true ∧
      Bridge.hostReceiptOwnedByHost = true ∧
      Bridge.worldCommitOwnedByWorld = true := by
  exact ⟨Bridge.activationOwnerRequired, Bridge.invocationOwnerRequired,
    Bridge.hostOwnerRequired, Bridge.worldOwnerRequired⟩

theorem invocation_and_host_receipt_do_not_commit_world_or_promote_truth
    (r : Receipt) :
    r.hostBinding.worldCommitPerformed = false ∧
      Bridge.worldCommitPerformed = false ∧
      Bridge.automaticTruthPromotion = false ∧
      Bridge.automaticPlanCompletion = false ∧
      Bridge.automaticRollback = false ∧
      Bridge.lowerAuthority.clinicalAuthority = false ∧
      Bridge.lowerAuthority.legalAuthority = false ∧
      Bridge.lowerAuthority.institutionalAuthority = false ∧
      Bridge.lowerAuthority.theoremAuthority = false := by
  exact ⟨r.hostBinding.worldCommitForbidden, Bridge.worldCommitForbidden,
    Bridge.truthPromotionForbidden, Bridge.planCompletionForbidden,
    Bridge.rollbackForbidden, Bridge.lowerAuthority.clinicalForbidden,
    Bridge.lowerAuthority.legalForbidden,
    Bridge.lowerAuthority.institutionalForbidden,
    Bridge.lowerAuthority.theoremForbidden⟩

theorem invocation_digest_is_exact (r : Receipt) :
    r.digest = Bridge.digestOf r.source r.activation r.binding r.projection
      r.invocation r.route r.hostReceipt r.hostBinding r.postEffectDebt
      r.activationIndex r.invocationIndex r.hostReceiptIndex r.historyAfter := by
  exact r.digestExact

end VacuumExpectationBoundedAdapterInvocationBridge
end
end ActOS
end KUOS
