import Mathlib
import KUOS.ActOS.VacuumExpectationBoundedAdapterInvocationV0_4
import KUOS.OpenHorizon.AuthorizedAtomicWorldCommitKernelV0_34
import KUOS.OpenHorizon.TransactionalEffectReconciliationKernelV0_24

namespace KUOS
namespace WORLD

open ObserveOS VerifyOS LearnOS DecisionOS PlanOS ActOS

structure WorldCommitIndex where
  current : Nat

namespace WorldCommitIndex

def append (index : WorldCommitIndex) : WorldCommitIndex :=
  ⟨index.current + 1⟩

@[simp] theorem append_current (index : WorldCommitIndex) :
    index.append.current = index.current + 1 := rfl

theorem strict (index : WorldCommitIndex) :
    index.current < index.append.current := by
  simp [append]

end WorldCommitIndex

structure WorldCommitHistory where
  committedRecords : Nat
  snapshotRecords : Nat
  snapshotExact : snapshotRecords = committedRecords

@[simp] theorem worldCommitHistory_snapshot_matches_commits
    (history : WorldCommitHistory) :
    history.snapshotRecords = history.committedRecords :=
  history.snapshotExact

structure HostEffectRecordCommitBinding where
  sourceReceiptBound : Bool
  effectRouteRecorded : Bool
  canonicalHostReceiptBound : Bool
  effectRecordCountOne : Bool
  externalEffectRecorded : Bool
  operationIdentityPreserved : Bool
  operationInputPreserved : Bool
  selectedStepPreserved : Bool
  targetCyclePreserved : Bool
  sessionPreserved : Bool
  actionIntentPreserved : Bool
  leaseReservationConsumed : Bool
  effectRecordImmutable : Bool
  sourceWorldCommitAbsent : Bool
  sourceRequired : sourceReceiptBound = true
  routeRequired : effectRouteRecorded = true
  canonicalRequired : canonicalHostReceiptBound = true
  countRequired : effectRecordCountOne = true
  effectRequired : externalEffectRecorded = true
  operationRequired : operationIdentityPreserved = true
  inputRequired : operationInputPreserved = true
  stepRequired : selectedStepPreserved = true
  cycleRequired : targetCyclePreserved = true
  sessionRequired : sessionPreserved = true
  intentRequired : actionIntentPreserved = true
  leaseRequired : leaseReservationConsumed = true
  immutabilityRequired : effectRecordImmutable = true
  priorCommitRequired : sourceWorldCommitAbsent = true

structure WorldPostEffectDebtCommitBinding where
  sourceDebtBound : Bool
  effectRecorded : Bool
  observationDebtPreserved : Bool
  verificationDebtPreserved : Bool
  observationCommitted : Bool
  verificationCommitted : Bool
  automaticTruthPromotion : Bool
  automaticPlanCompletion : Bool
  automaticRollback : Bool
  debtRequired : sourceDebtBound = true
  effectRequired : effectRecorded = true
  observationRequired : observationDebtPreserved = true
  verificationRequired : verificationDebtPreserved = true
  observationCommitForbidden : observationCommitted = false
  verificationCommitForbidden : verificationCommitted = false
  truthPromotionForbidden : automaticTruthPromotion = false
  planCompletionForbidden : automaticPlanCompletion = false
  rollbackForbidden : automaticRollback = false

structure WorldAtomicCommitAdmissionBoundary where
  hostReceiptBound : Bool
  effectRecordBound : Bool
  postEffectDebtBound : Bool
  requestReconstructible : Bool
  commitAuthorizationFinite : Bool
  commitAuthorizationSingleUse : Bool
  optimisticConcurrencyMatched : Bool
  admissionCommitted : Bool
  atomicCommitPerformed : Bool
  observationDebtDischarged : Bool
  verificationDebtDischarged : Bool
  hostRequired : hostReceiptBound = true
  effectRequired : effectRecordBound = true
  debtRequired : postEffectDebtBound = true
  reconstructionRequired : requestReconstructible = true
  finiteAuthorizationRequired : commitAuthorizationFinite = true
  singleUseRequired : commitAuthorizationSingleUse = true
  concurrencyRequired : optimisticConcurrencyMatched = true
  admissionRequired : admissionCommitted = true
  commitForbidden : atomicCommitPerformed = false
  observationDischargeForbidden : observationDebtDischarged = false
  verificationDischargeForbidden : verificationDebtDischarged = false

structure WorldCommitNonAuthority where
  commitRecordIsTruth : Bool
  causalAttributionGranted : Bool
  observationAuthority : Bool
  verificationAuthority : Bool
  executionAuthority : Bool
  planActivationAuthority : Bool
  actOSInvocationAuthority : Bool
  memoryOverwrite : Bool
  constitutionalRootRewrite : Bool
  automaticRollback : Bool
  automaticMissionCompletion : Bool
  truthForbidden : commitRecordIsTruth = false
  causalityForbidden : causalAttributionGranted = false
  observationForbidden : observationAuthority = false
  verificationForbidden : verificationAuthority = false
  executionForbidden : executionAuthority = false
  planActivationForbidden : planActivationAuthority = false
  invocationForbidden : actOSInvocationAuthority = false
  overwriteForbidden : memoryOverwrite = false
  rootRewriteForbidden : constitutionalRootRewrite = false
  rollbackForbidden : automaticRollback = false
  missionCompletionForbidden : automaticMissionCompletion = false

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
    (InvocationBridge : VacuumExpectationBoundedAdapterInvocationBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge)

structure WorldVacuumExpectationHostEffectAtomicCommitBridge where
  Digest : Type
  digestOf :
    VacuumExpectationBoundedAdapterInvocationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge
            InvocationBridge →
    HostEffectRecordCommitBinding → WorldPostEffectDebtCommitBinding →
    WorldAtomicCommitAdmissionBoundary →
    OpenHorizon.WorldEffectReconciliationBoundary →
    OpenHorizon.TransactionCommitBoundary →
    OpenHorizon.AuthorizedAtomicWorldCommitKernelV034 →
    WorldCommitIndex → WorldCommitIndex → WorldCommitHistory → Digest
  nonAuthority : WorldCommitNonAuthority
  worldOwnsAtomicCommit : Bool
  hostOwnsHostReceipt : Bool
  observeOSOwnsObservation : Bool
  verifyOSOwnsVerification : Bool
  worldOwnerRequired : worldOwnsAtomicCommit = true
  hostOwnerRequired : hostOwnsHostReceipt = true
  observeOwnerRequired : observeOSOwnsObservation = true
  verifyOwnerRequired : verifyOSOwnsVerification = true

structure WorldVacuumExpectationHostEffectAtomicCommitReceipt
    (Bridge : WorldVacuumExpectationHostEffectAtomicCommitBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge
            InvocationBridge) where
  source : VacuumExpectationBoundedAdapterInvocationReceipt
    K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge AuthorizationBridge
          InvocationBridge
  effectBinding : HostEffectRecordCommitBinding
  debtBinding : WorldPostEffectDebtCommitBinding
  admission : WorldAtomicCommitAdmissionBoundary
  reconciliation : OpenHorizon.WorldEffectReconciliationBoundary
  transactionCommit : OpenHorizon.TransactionCommitBoundary
  atomicKernel : OpenHorizon.AuthorizedAtomicWorldCommitKernelV034
  intakeIndex : WorldCommitIndex
  commitIndex : WorldCommitIndex
  historyAfter : WorldCommitHistory
  digest : Bridge.Digest
  sourceBound : Bool
  sourceRequired : sourceBound = true
  sourceRouteEffectRecorded : source.hostReceipt.route = .effectRecorded
  sourceEffectRecordCount : source.hostReceipt.effectRecordCount = 1
  sourceExternalEffectRecorded : source.route.externalEffectPerformed = true
  sourceHostReceiptCanonical : source.hostBinding.hostReceiptCanonical = true
  sourceWorldCommitAbsent : source.hostBinding.worldCommitPerformed = false
  sourceDebtEffectRecorded : source.postEffectDebt.effectRecorded = true
  sourceObservationDebt : source.postEffectDebt.observationRequired = true
  sourceVerificationDebt : source.postEffectDebt.verificationRequired = true
  reconciliationEffectUnconfirmed : reconciliation.worldEffectConfirmed = false
  intakeIndexExact : intakeIndex.current = source.hostReceiptIndex.current + 1
  commitIndexExact : commitIndex = intakeIndex.append
  historyExact : historyAfter.committedRecords =
    source.historyAfter.committedRecords + 2
  digestExact : digest = Bridge.digestOf source effectBinding debtBinding
    admission reconciliation transactionCommit atomicKernel intakeIndex
    commitIndex historyAfter

namespace WorldVacuumExpectationHostEffectAtomicCommitBridge

variable
    {Bridge : WorldVacuumExpectationHostEffectAtomicCommitBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge
            InvocationBridge}

abbrev Receipt := WorldVacuumExpectationHostEffectAtomicCommitReceipt
  K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
    GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
      MaterializationBridge AdmissionBridge AuthorizationBridge
        InvocationBridge Bridge

theorem commit_intake_requires_canonical_effect_record (r : Receipt) :
    r.sourceBound = true ∧
      r.source.hostReceipt.route = .effectRecorded ∧
      r.source.hostReceipt.effectRecordCount = 1 ∧
      r.source.route.externalEffectPerformed = true ∧
      r.source.hostBinding.hostReceiptCanonical = true ∧
      r.source.hostBinding.worldCommitPerformed = false := by
  exact ⟨r.sourceRequired, r.sourceRouteEffectRecorded,
    r.sourceEffectRecordCount, r.sourceExternalEffectRecorded,
    r.sourceHostReceiptCanonical, r.sourceWorldCommitAbsent⟩

theorem effect_record_binding_preserves_exact_identity (r : Receipt) :
    r.effectBinding.sourceReceiptBound = true ∧
      r.effectBinding.effectRouteRecorded = true ∧
      r.effectBinding.canonicalHostReceiptBound = true ∧
      r.effectBinding.effectRecordCountOne = true ∧
      r.effectBinding.externalEffectRecorded = true ∧
      r.effectBinding.operationIdentityPreserved = true ∧
      r.effectBinding.operationInputPreserved = true ∧
      r.effectBinding.selectedStepPreserved = true ∧
      r.effectBinding.targetCyclePreserved = true ∧
      r.effectBinding.sessionPreserved = true ∧
      r.effectBinding.actionIntentPreserved = true ∧
      r.effectBinding.leaseReservationConsumed = true ∧
      r.effectBinding.effectRecordImmutable = true ∧
      r.effectBinding.sourceWorldCommitAbsent = true := by
  exact ⟨r.effectBinding.sourceRequired, r.effectBinding.routeRequired,
    r.effectBinding.canonicalRequired, r.effectBinding.countRequired,
    r.effectBinding.effectRequired, r.effectBinding.operationRequired,
    r.effectBinding.inputRequired, r.effectBinding.stepRequired,
    r.effectBinding.cycleRequired, r.effectBinding.sessionRequired,
    r.effectBinding.intentRequired, r.effectBinding.leaseRequired,
    r.effectBinding.immutabilityRequired,
    r.effectBinding.priorCommitRequired⟩

theorem post_effect_debts_survive_world_commit (r : Receipt) :
    r.source.postEffectDebt.effectRecorded = true ∧
      r.source.postEffectDebt.observationRequired = true ∧
      r.source.postEffectDebt.verificationRequired = true ∧
      r.debtBinding.sourceDebtBound = true ∧
      r.debtBinding.effectRecorded = true ∧
      r.debtBinding.observationDebtPreserved = true ∧
      r.debtBinding.verificationDebtPreserved = true ∧
      r.debtBinding.observationCommitted = false ∧
      r.debtBinding.verificationCommitted = false := by
  exact ⟨r.sourceDebtEffectRecorded, r.sourceObservationDebt,
    r.sourceVerificationDebt, r.debtBinding.debtRequired,
    r.debtBinding.effectRequired, r.debtBinding.observationRequired,
    r.debtBinding.verificationRequired,
    r.debtBinding.observationCommitForbidden,
    r.debtBinding.verificationCommitForbidden⟩

theorem commit_admission_is_single_use_and_precedes_atomic_commit (r : Receipt) :
    r.admission.hostReceiptBound = true ∧
      r.admission.effectRecordBound = true ∧
      r.admission.postEffectDebtBound = true ∧
      r.admission.requestReconstructible = true ∧
      r.admission.commitAuthorizationFinite = true ∧
      r.admission.commitAuthorizationSingleUse = true ∧
      r.admission.optimisticConcurrencyMatched = true ∧
      r.admission.admissionCommitted = true ∧
      r.admission.atomicCommitPerformed = false := by
  exact ⟨r.admission.hostRequired, r.admission.effectRequired,
    r.admission.debtRequired, r.admission.reconstructionRequired,
    r.admission.finiteAuthorizationRequired, r.admission.singleUseRequired,
    r.admission.concurrencyRequired, r.admission.admissionRequired,
    r.admission.commitForbidden⟩

theorem admission_does_not_discharge_observation_or_verification (r : Receipt) :
    r.admission.observationDebtDischarged = false ∧
      r.admission.verificationDebtDischarged = false := by
  exact ⟨r.admission.observationDischargeForbidden,
    r.admission.verificationDischargeForbidden⟩

theorem atomic_commit_binds_source_generation_fencing_and_lease (r : Receipt) :
    r.atomicKernel.adoptCandidateBoundExactly = true ∧
      r.atomicKernel.authorizationBoundExactly = true ∧
      r.atomicKernel.requestReconstructibleExactly = true ∧
      r.atomicKernel.storeIdentityBoundExactly = true ∧
      r.atomicKernel.rootLineageBoundExactly = true ∧
      r.atomicKernel.priorFragmentBoundExactly = true ∧
      r.atomicKernel.priorCommitBoundExactly = true ∧
      r.atomicKernel.expectedGenerationBoundExactly = true ∧
      r.atomicKernel.targetGenerationIsSuccessor = true ∧
      r.atomicKernel.fencingTokenStrictlyFresh = true ∧
      r.atomicKernel.leaseEpochNondecreasing = true ∧
      r.atomicKernel.optimisticConcurrencyMatched = true := by
  exact ⟨r.atomicKernel.candidateBindingRequired,
    r.atomicKernel.authorizationBindingRequired,
    r.atomicKernel.requestReconstructionRequired,
    r.atomicKernel.storeBindingRequired, r.atomicKernel.rootBindingRequired,
    r.atomicKernel.priorFragmentRequired, r.atomicKernel.priorCommitRequired,
    r.atomicKernel.generationBindingRequired,
    r.atomicKernel.successorGenerationRequired,
    r.atomicKernel.freshFencingRequired, r.atomicKernel.leaseEpochRequired,
    r.atomicKernel.optimisticConcurrencyRequired⟩

theorem atomic_commit_is_one_append_only_immutable_state (r : Receipt) :
    r.atomicKernel.atomicReplaceCommitted = true ∧
      r.atomicKernel.oneAtomicStoreAndReceiptState = true ∧
      r.atomicKernel.appendOnlyHistoryPreserved = true ∧
      r.atomicKernel.immutableCommitReceipt = true ∧
      r.atomicKernel.sameRootPreserved = true ∧
      r.atomicKernel.worldCommitRecorded = true := by
  exact ⟨r.atomicKernel.atomicReplaceRequired,
    r.atomicKernel.atomicStateRequired, r.atomicKernel.appendOnlyRequired,
    r.atomicKernel.immutableReceiptRequired, r.atomicKernel.sameRootRequired,
    r.atomicKernel.commitRecordRequired⟩

theorem atomic_commit_preserves_open_horizon (r : Receipt) :
    r.atomicKernel.localCommitAuthorizationFinite = true ∧
      r.atomicKernel.localCommitAuthorizationSingleUse = true ∧
      r.atomicKernel.openHorizonPreserved = true ∧
      r.atomicKernel.globalCycleLimitAbsent = true ∧
      r.atomicKernel.globalGenerationLimitAbsent = true ∧
      r.atomicKernel.globalTimeHorizonLimitAbsent = true := by
  exact OpenHorizon.AuthorizedAtomicWorldCommit.
    local_commit_authorization_does_not_shrink_open_horizon r.atomicKernel

theorem rollback_reference_is_preserved_but_not_executed (r : Receipt) :
    r.atomicKernel.rollbackReferencePreserved = true ∧
      r.atomicKernel.rollbackRequiresFreshAuthorization = true ∧
      r.atomicKernel.rollbackDeletesHistory = false ∧
      r.atomicKernel.automaticRollbackPerformed = false := by
  exact OpenHorizon.AuthorizedAtomicWorldCommit.
    rollback_reference_is_not_automatic_history_deletion r.atomicKernel

theorem atomic_commit_is_not_truth_causality_or_new_execution_authority
    (r : Receipt) :
    r.atomicKernel.worldCommitIsTruth = false ∧
      r.atomicKernel.worldCommitIsCausalAttribution = false ∧
      r.atomicKernel.constitutionalRootRewritten = false ∧
      r.atomicKernel.memoryHistoryOverwritten = false ∧
      r.atomicKernel.automaticRollbackPerformed = false ∧
      r.atomicKernel.automaticMissionCompletion = false ∧
      r.atomicKernel.planActivationGranted = false ∧
      r.atomicKernel.actosInvocationGranted = false := by
  exact ⟨r.atomicKernel.truthForbidden,
    r.atomicKernel.causalAttributionForbidden,
    r.atomicKernel.rootRewriteForbidden,
    r.atomicKernel.historyOverwriteForbidden,
    r.atomicKernel.automaticRollbackForbidden,
    r.atomicKernel.automaticMissionCompletionForbidden,
    r.atomicKernel.planActivationForbidden,
    r.atomicKernel.actosInvocationForbidden⟩

theorem atomic_commit_replay_and_stale_rejection_are_total (r : Receipt) :
    r.atomicKernel.replayIdempotent = true ∧
      r.atomicKernel.staleGenerationRejected = true ∧
      r.atomicKernel.stalePriorFragmentRejected = true ∧
      r.atomicKernel.stalePriorCommitRejected = true ∧
      r.atomicKernel.staleFencingRejected = true ∧
      r.atomicKernel.staleLeaseEpochRejected = true := by
  exact ⟨r.atomicKernel.replayRequired,
    r.atomicKernel.staleGenerationRejectionRequired,
    r.atomicKernel.stalePriorFragmentRejectionRequired,
    r.atomicKernel.stalePriorCommitRejectionRequired,
    r.atomicKernel.staleFencingRejectionRequired,
    r.atomicKernel.staleLeaseRejectionRequired⟩

theorem transaction_commit_preserves_lower_receipts_and_grants_no_authority
    (r : Receipt) :
    r.transactionCommit.appendOnly = true ∧
      r.transactionCommit.lowerActReceiptCanonical = true ∧
      r.transactionCommit.lowerObserveReceiptCanonical = true ∧
      r.transactionCommit.lowerVerifyReceiptCanonical = true ∧
      r.transactionCommit.memoryOverwrite = false ∧
      r.transactionCommit.executionAuthority = false ∧
      r.transactionCommit.finalCommitmentAuthority = false ∧
      r.transactionCommit.worldRewriteAuthority = false ∧
      r.transactionCommit.wakeUpAuthority = false := by
  have hreceipts := OpenHorizon.TransactionalEffectReconciliation.
    transaction_commit_preserves_lower_receipts r.transactionCommit
  have hauthority := OpenHorizon.TransactionalEffectReconciliation.
    transaction_commit_grants_no_new_authority r.transactionCommit
  exact ⟨hreceipts.1, hreceipts.2.1, hreceipts.2.2.1,
    hreceipts.2.2.2, hauthority.1, hauthority.2.1,
    hauthority.2.2.1, hauthority.2.2.2.1,
    hauthority.2.2.2.2⟩

theorem committed_host_effect_is_not_world_confirmation_or_verification
    (r : Receipt) :
    r.reconciliation.worldEffectConfirmed = false ∧
      r.reconciliation.observationIsVerification = false ∧
      r.reconciliation.reconciliationIsTruth = false ∧
      r.reconciliation.causalAttributionGranted = false := by
  have h := OpenHorizon.TransactionalEffectReconciliation.
    reconciliation_is_neither_verification_nor_truth r.reconciliation
  exact ⟨r.reconciliationEffectUnconfirmed, h.1, h.2.1, h.2.2⟩

theorem debt_binding_forbids_automatic_promotion_completion_or_rollback
    (r : Receipt) :
    r.debtBinding.automaticTruthPromotion = false ∧
      r.debtBinding.automaticPlanCompletion = false ∧
      r.debtBinding.automaticRollback = false := by
  exact ⟨r.debtBinding.truthPromotionForbidden,
    r.debtBinding.planCompletionForbidden,
    r.debtBinding.rollbackForbidden⟩

theorem world_commit_events_append_strictly (r : Receipt) :
    r.source.hostReceiptIndex.current < r.intakeIndex.current ∧
      r.intakeIndex.current < r.commitIndex.current := by
  constructor
  · rw [r.intakeIndexExact]
    omega
  · rw [r.commitIndexExact]
    exact WorldCommitIndex.strict r.intakeIndex

theorem world_commit_history_appends_two_records (r : Receipt) :
    r.historyAfter.committedRecords = r.source.historyAfter.committedRecords + 2 ∧
      r.historyAfter.snapshotRecords = r.source.historyAfter.committedRecords + 2 := by
  refine ⟨r.historyExact, ?_⟩
  rw [worldCommitHistory_snapshot_matches_commits r.historyAfter]
  exact r.historyExact

theorem commit_ownership_is_separated (_r : Receipt) :
    Bridge.worldOwnsAtomicCommit = true ∧
      Bridge.hostOwnsHostReceipt = true ∧
      Bridge.observeOSOwnsObservation = true ∧
      Bridge.verifyOSOwnsVerification = true := by
  exact ⟨Bridge.worldOwnerRequired, Bridge.hostOwnerRequired,
    Bridge.observeOwnerRequired, Bridge.verifyOwnerRequired⟩

theorem bridge_grants_no_truth_observation_verification_or_execution
    (_r : Receipt) :
    Bridge.nonAuthority.commitRecordIsTruth = false ∧
      Bridge.nonAuthority.causalAttributionGranted = false ∧
      Bridge.nonAuthority.observationAuthority = false ∧
      Bridge.nonAuthority.verificationAuthority = false ∧
      Bridge.nonAuthority.executionAuthority = false ∧
      Bridge.nonAuthority.planActivationAuthority = false ∧
      Bridge.nonAuthority.actOSInvocationAuthority = false ∧
      Bridge.nonAuthority.memoryOverwrite = false ∧
      Bridge.nonAuthority.constitutionalRootRewrite = false ∧
      Bridge.nonAuthority.automaticRollback = false ∧
      Bridge.nonAuthority.automaticMissionCompletion = false := by
  exact ⟨Bridge.nonAuthority.truthForbidden,
    Bridge.nonAuthority.causalityForbidden,
    Bridge.nonAuthority.observationForbidden,
    Bridge.nonAuthority.verificationForbidden,
    Bridge.nonAuthority.executionForbidden,
    Bridge.nonAuthority.planActivationForbidden,
    Bridge.nonAuthority.invocationForbidden,
    Bridge.nonAuthority.overwriteForbidden,
    Bridge.nonAuthority.rootRewriteForbidden,
    Bridge.nonAuthority.rollbackForbidden,
    Bridge.nonAuthority.missionCompletionForbidden⟩

theorem atomic_commit_digest_is_exact (r : Receipt) :
    r.digest = Bridge.digestOf r.source r.effectBinding r.debtBinding
      r.admission r.reconciliation r.transactionCommit r.atomicKernel
      r.intakeIndex r.commitIndex r.historyAfter := by
  exact r.digestExact

end WorldVacuumExpectationHostEffectAtomicCommitBridge
end
end WORLD
end KUOS
