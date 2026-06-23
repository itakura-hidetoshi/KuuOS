import Mathlib
import KUOS.LearnOS.WorldHostEffectVerificationFutureOnlyLearningV0_4
import KUOS.PlanOS.QiConditionedNonMarkovReplanV0_2
import KUOS.PlanOS.ClosedLoopReplanIntakeAdapterV0_4

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS ActOS

structure WorldDispositionReplanBoundary where
  sourceDispositionPreserved : Bool
  governanceReviewPreserved : Bool
  worldCommitSeparate : Bool
  freshCommitAuthorizationRequired : Bool
  freshCommitAuthorizationSupplied : Bool
  atomicCommitReady : Bool
  replanIntakeResolvesWorldDisposition : Bool
  automaticWorldAdoption : Bool
  automaticWorldRejection : Bool
  automaticWorldCommit : Bool
  automaticRollback : Bool
  dispositionRequired : sourceDispositionPreserved = true
  governanceRequired : governanceReviewPreserved = true
  separateCommitRequired : worldCommitSeparate = true
  authorizationRequired : freshCommitAuthorizationRequired = true
  authorizationNotSupplied : freshCommitAuthorizationSupplied = false
  readinessForbidden : atomicCommitReady = false
  resolutionForbidden : replanIntakeResolvesWorldDisposition = false
  adoptionForbidden : automaticWorldAdoption = false
  rejectionForbidden : automaticWorldRejection = false
  commitForbidden : automaticWorldCommit = false
  rollbackForbidden : automaticRollback = false

structure ReplanIntakeReceiptBoundary where
  receiptCommitted : Bool
  receiptImmutable : Bool
  appendOnly : Bool
  exactReplayIdempotent : Bool
  conflictingReplayAccepted : Bool
  receiptRequired : receiptCommitted = true
  immutableRequired : receiptImmutable = true
  appendOnlyRequired : appendOnly = true
  replayRequired : exactReplayIdempotent = true
  conflictingReplayForbidden : conflictingReplayAccepted = false

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
    (WorldIntakeBridge : WorldVacuumExpectationHostEffectAtomicCommitIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge)
    (ObservationBridge : WorldHostEffectObservationBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge
            InvocationBridge WorldIntakeBridge)
    (WorldVerificationBridge : WorldHostEffectVerificationBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge
            InvocationBridge WorldIntakeBridge ObservationBridge)
    (WorldLearningBridge : LearnOS.WorldHostEffectVerificationLearningBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge
            InvocationBridge WorldIntakeBridge ObservationBridge
              WorldVerificationBridge)

abbrev SourceLearningReceipt := LearnOS.WorldHostEffectVerificationLearningReceipt
  K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge
    HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge
      AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge
        ObservationBridge WorldVerificationBridge WorldLearningBridge

structure WorldHostEffectLearningReplanIntakeBridge where
  IntakeDigest : Type
  digestOf :
    SourceLearningReceipt K O Intake ObserveBridge VerifyBridge LearnBridge
      ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge
          WorldIntakeBridge ObservationBridge WorldVerificationBridge
            WorldLearningBridge →
    ReplanSourceBinding → ClosedLoopBindState → ClosedLoopFutureBoundary →
    ReplanOwnership → ClosedLoopActivationSeparation →
    WorldDispositionReplanBoundary → ReplanIntakeReceiptBoundary →
    ReplanEventIndex → ReplanEventIndex → ReplanHistory → ReplanHistory → IntakeDigest
  replanNonAuthority : ReplanNonAuthority
  planOSOwnsReplan : Bool
  decisionOSOwnsSelection : Bool
  planOSOwnsSynthesis : Bool
  actOSOwnsExecution : Bool
  learnOSOwnsLearning : Bool
  worldOwnsDisposition : Bool
  bridgeRuntimeActivatesReplan : Bool
  bridgeRuntimeGeneratesCandidates : Bool
  bridgeRuntimeSelectsCandidate : Bool
  bridgeRuntimeSynthesizesPlan : Bool
  bridgeRuntimePermitsExecution : Bool
  bridgeRuntimeResolvesWorldDisposition : Bool
  bridgeRuntimeUpdatesWORLD : Bool
  bridgeRuntimeOverwritesMemory : Bool
  replanOwnershipRequired : planOSOwnsReplan = true
  selectionOwnershipRequired : decisionOSOwnsSelection = true
  synthesisOwnershipRequired : planOSOwnsSynthesis = true
  executionOwnershipRequired : actOSOwnsExecution = true
  learningOwnershipRequired : learnOSOwnsLearning = true
  dispositionOwnershipRequired : worldOwnsDisposition = true
  replanActivationForbidden : bridgeRuntimeActivatesReplan = false
  candidateGenerationForbidden : bridgeRuntimeGeneratesCandidates = false
  candidateSelectionForbidden : bridgeRuntimeSelectsCandidate = false
  planSynthesisForbidden : bridgeRuntimeSynthesizesPlan = false
  executionPermissionForbidden : bridgeRuntimePermitsExecution = false
  dispositionResolutionForbidden : bridgeRuntimeResolvesWorldDisposition = false
  worldUpdateForbidden : bridgeRuntimeUpdatesWORLD = false
  memoryOverwriteForbidden : bridgeRuntimeOverwritesMemory = false

structure WorldHostEffectLearningReplanIntakeReceipt
    (Bridge : WorldHostEffectLearningReplanIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge
            InvocationBridge WorldIntakeBridge ObservationBridge
              WorldVerificationBridge WorldLearningBridge) where
  learning : SourceLearningReceipt K O Intake ObserveBridge VerifyBridge LearnBridge
    ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
      MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge
        WorldIntakeBridge ObservationBridge WorldVerificationBridge
          WorldLearningBridge
  sourceBinding : ReplanSourceBinding
  bindState : ClosedLoopBindState
  futureBoundary : ClosedLoopFutureBoundary
  ownership : ReplanOwnership
  activation : ClosedLoopActivationSeparation
  dispositionBoundary : WorldDispositionReplanBoundary
  receiptBoundary : ReplanIntakeReceiptBoundary
  indexBefore : ReplanEventIndex
  indexAfter : ReplanEventIndex
  historyBefore : ReplanHistory
  historyAfter : ReplanHistory
  intakeDigest : Bridge.IntakeDigest
  currentPlanCommitted : Bool
  sourceLearningBound : Bool
  intakeCommitted : Bool
  bindCommitted : Bool
  currentPlanRequired : currentPlanCommitted = true
  sourceLearningRequired : sourceLearningBound = true
  intakeRequired : intakeCommitted = true
  bindRequired : bindCommitted = true
  sourceLearningReceiptCommitted : learning.receiptBoundary.receiptCommitted = true
  sourceLearningRecorded : learning.learningRecorded = true
  sourceReplanRequired : learning.debtSemantics.replanRequired = true
  sourceFutureOnly : learning.delta.futureOnly = true
  sourceInactiveNow : learning.delta.activeNow = false
  sourceCurrentUnchanged : learning.delta.currentCycleMutation = false
  sourcePastUnchanged : learning.delta.pastRecordMutation = false
  sourceDispositionPreserved :
    learning.dispositionBoundary.sourceDispositionPreserved = true
  sourceGovernancePreserved :
    learning.dispositionBoundary.governanceReviewPreserved = true
  sourceWorldCommitSeparate : learning.dispositionBoundary.worldCommitSeparate = true
  sourceFreshAuthorizationRequired :
    learning.dispositionBoundary.freshCommitAuthorizationRequired = true
  sourceFreshAuthorizationAbsent :
    learning.dispositionBoundary.freshCommitAuthorizationSupplied = false
  sourceAtomicCommitNotReady : learning.dispositionBoundary.atomicCommitReady = false
  currentPlanExact : sourceBinding.committedCurrentPlan = currentPlanCommitted
  learningCommitExact : sourceBinding.committedLearnState = learning.learningRecorded
  missionExact :
    sourceBinding.sameMissionContract = learning.sourceBinding.missionContractBound
  learningDeltaExact : sourceBinding.learningDeltaBound = sourceLearningBound
  middleWayExact :
    sourceBinding.middleWayReportBound = learning.middleWay.candidateAdmissible
  verificationExact :
    sourceBinding.verificationEvidenceBound =
      learning.sourceBinding.verificationEvidenceBound
  futureOnlyExact : sourceBinding.futureOnlyLearning = learning.delta.futureOnly
  inactiveExact : sourceBinding.learningInactiveNow = learning.delta.activeNow
  replanDebtExact :
    sourceBinding.replanRequiredByLearnOS = learning.debtSemantics.replanRequired
  dispositionExact :
    dispositionBoundary.sourceDispositionPreserved =
      learning.dispositionBoundary.sourceDispositionPreserved
  governanceExact :
    dispositionBoundary.governanceReviewPreserved =
      learning.dispositionBoundary.governanceReviewPreserved
  worldCommitExact :
    dispositionBoundary.worldCommitSeparate =
      learning.dispositionBoundary.worldCommitSeparate
  freshAuthorizationRequiredExact :
    dispositionBoundary.freshCommitAuthorizationRequired =
      learning.dispositionBoundary.freshCommitAuthorizationRequired
  freshAuthorizationSuppliedExact :
    dispositionBoundary.freshCommitAuthorizationSupplied =
      learning.dispositionBoundary.freshCommitAuthorizationSupplied
  atomicCommitReadyExact :
    dispositionBoundary.atomicCommitReady =
      learning.dispositionBoundary.atomicCommitReady
  activationIntakeExact : activation.intakeCommitted = intakeCommitted
  activationBindExact : activation.bindCommitted = bindCommitted
  replanOwnershipExact :
    ownership.replanOwnedByPlanOS = Bridge.planOSOwnsReplan
  selectionOwnershipExact :
    ownership.selectionOwnedByDecisionOS = Bridge.decisionOSOwnsSelection
  synthesisOwnershipExact :
    ownership.synthesisOwnedByPlanOS = Bridge.planOSOwnsSynthesis
  executionOwnershipExact :
    ownership.executionOwnedByActOS = Bridge.actOSOwnsExecution
  indexBeforeExact : indexBefore.current = bindState.eventIndex
  indexAppendExact : indexAfter = indexBefore.append
  historyAppendExact :
    historyAfter.committedRecords = historyBefore.committedRecords + 1
  intakeDigestExact : intakeDigest = Bridge.digestOf learning sourceBinding bindState
    futureBoundary ownership activation dispositionBoundary receiptBoundary
    indexBefore indexAfter historyBefore historyAfter

namespace WorldHostEffectLearningReplanIntakeBridge

variable
    {Bridge : WorldHostEffectLearningReplanIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge
            InvocationBridge WorldIntakeBridge ObservationBridge
              WorldVerificationBridge WorldLearningBridge}

abbrev Receipt := WorldHostEffectLearningReplanIntakeReceipt
  K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge
    HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge
      AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge
        ObservationBridge WorldVerificationBridge WorldLearningBridge Bridge

theorem intake_requires_committed_future_only_learning (r : Receipt) :
    r.learning.receiptBoundary.receiptCommitted = true ∧
      r.learning.learningRecorded = true ∧
      r.learning.debtSemantics.replanRequired = true ∧
      r.learning.delta.futureOnly = true ∧
      r.learning.delta.activeNow = false ∧
      r.learning.delta.currentCycleMutation = false ∧
      r.learning.delta.pastRecordMutation = false := by
  exact ⟨r.sourceLearningReceiptCommitted, r.sourceLearningRecorded,
    r.sourceReplanRequired, r.sourceFutureOnly, r.sourceInactiveNow,
    r.sourceCurrentUnchanged, r.sourcePastUnchanged⟩

theorem intake_binds_existing_replan_source (r : Receipt) :
    r.sourceBinding.committedCurrentPlan = true ∧
      r.sourceBinding.committedLearnState = true ∧
      r.sourceBinding.sameMissionContract = true ∧
      r.sourceBinding.learningDeltaBound = true ∧
      r.sourceBinding.middleWayReportBound = true ∧
      r.sourceBinding.verificationEvidenceBound = true ∧
      r.sourceBinding.futureOnlyLearning = true ∧
      r.sourceBinding.learningInactiveNow = true ∧
      r.sourceBinding.replanRequiredByLearnOS = true := by
  exact ⟨r.sourceBinding.currentPlanRequired, r.sourceBinding.learnStateRequired,
    r.sourceBinding.missionRequired, r.sourceBinding.deltaRequired,
    r.sourceBinding.middleWayRequired, r.sourceBinding.evidenceRequired,
    r.sourceBinding.futureRequired, r.sourceBinding.inactiveRequired,
    r.sourceBinding.replanDebtRequired⟩

theorem intake_enters_pristine_planos_bind (r : Receipt) :
    r.bindState.phaseIsBind = true ∧ r.bindState.eventIndex = 0 ∧
      r.bindState.historyRequired = true := by
  exact closed_loop_enters_pristine_bind r.bindState

theorem intake_preserves_future_boundary (r : Receipt) :
    r.futureBoundary.futureOnly = true ∧
      r.futureBoundary.activeNow = false ∧
      r.futureBoundary.currentCycleUnchanged = true ∧
      r.futureBoundary.pastPlanUnchanged = true ∧
      r.futureBoundary.memoryOverwrite = false := by
  exact closed_loop_bind_is_future_only r.futureBoundary

theorem intake_preserves_world_disposition_candidate (r : Receipt) :
    r.learning.dispositionBoundary.sourceDispositionPreserved = true ∧
      r.learning.dispositionBoundary.governanceReviewPreserved = true ∧
      r.learning.dispositionBoundary.worldCommitSeparate = true ∧
      r.learning.dispositionBoundary.freshCommitAuthorizationRequired = true ∧
      r.learning.dispositionBoundary.freshCommitAuthorizationSupplied = false ∧
      r.learning.dispositionBoundary.atomicCommitReady = false ∧
      r.dispositionBoundary.sourceDispositionPreserved = true ∧
      r.dispositionBoundary.governanceReviewPreserved = true ∧
      r.dispositionBoundary.worldCommitSeparate = true ∧
      r.dispositionBoundary.freshCommitAuthorizationRequired = true ∧
      r.dispositionBoundary.freshCommitAuthorizationSupplied = false ∧
      r.dispositionBoundary.atomicCommitReady = false ∧
      r.dispositionBoundary.replanIntakeResolvesWorldDisposition = false := by
  exact ⟨r.sourceDispositionPreserved, r.sourceGovernancePreserved,
    r.sourceWorldCommitSeparate, r.sourceFreshAuthorizationRequired,
    r.sourceFreshAuthorizationAbsent, r.sourceAtomicCommitNotReady,
    r.dispositionBoundary.dispositionRequired,
    r.dispositionBoundary.governanceRequired,
    r.dispositionBoundary.separateCommitRequired,
    r.dispositionBoundary.authorizationRequired,
    r.dispositionBoundary.authorizationNotSupplied,
    r.dispositionBoundary.readinessForbidden,
    r.dispositionBoundary.resolutionForbidden⟩

theorem intake_preserves_planos_decisionos_actos_ownership (r : Receipt) :
    r.ownership.replanOwnedByPlanOS = true ∧
      r.ownership.selectionOwnedByDecisionOS = true ∧
      r.ownership.synthesisOwnedByPlanOS = true ∧
      r.ownership.executionOwnedByActOS = true ∧
      Bridge.learnOSOwnsLearning = true ∧
      Bridge.worldOwnsDisposition = true := by
  exact ⟨r.ownership.replanOwnerRequired,
    r.ownership.selectionOwnerRequired, r.ownership.synthesisOwnerRequired,
    r.ownership.executionOwnerRequired, Bridge.learningOwnershipRequired,
    Bridge.dispositionOwnershipRequired⟩

theorem intake_commit_is_not_activation_generation_selection_or_execution
    (r : Receipt) :
    r.activation.intakeCommitted = true ∧
      r.activation.bindCommitted = true ∧
      r.activation.replanActivated = false ∧
      r.activation.planActivated = false ∧
      r.activation.executionPermitted = false ∧
      r.activation.hostLicenseGranted = false ∧
      Bridge.bridgeRuntimeGeneratesCandidates = false ∧
      Bridge.bridgeRuntimeSelectsCandidate = false ∧
      Bridge.bridgeRuntimeSynthesizesPlan = false ∧
      Bridge.bridgeRuntimeResolvesWorldDisposition = false := by
  exact ⟨r.activation.intakeRequired, r.activation.bindRequired,
    r.activation.replanForbidden, r.activation.planForbidden,
    r.activation.executionForbidden, r.activation.hostLicenseForbidden,
    Bridge.candidateGenerationForbidden, Bridge.candidateSelectionForbidden,
    Bridge.planSynthesisForbidden, Bridge.dispositionResolutionForbidden⟩

theorem intake_receipt_is_immutable_append_only_and_replay_safe (r : Receipt) :
    r.receiptBoundary.receiptCommitted = true ∧
      r.receiptBoundary.receiptImmutable = true ∧
      r.receiptBoundary.appendOnly = true ∧
      r.receiptBoundary.exactReplayIdempotent = true ∧
      r.receiptBoundary.conflictingReplayAccepted = false := by
  exact ⟨r.receiptBoundary.receiptRequired,
    r.receiptBoundary.immutableRequired,
    r.receiptBoundary.appendOnlyRequired,
    r.receiptBoundary.replayRequired,
    r.receiptBoundary.conflictingReplayForbidden⟩

theorem intake_event_index_appends_exactly_once (r : Receipt) :
    r.indexBefore.current = 0 ∧ r.indexAfter.current = 1 := by
  have hbefore : r.indexBefore.current = 0 := by
    calc
      r.indexBefore.current = r.bindState.eventIndex := r.indexBeforeExact
      _ = 0 := r.bindState.pristineRequired
  refine ⟨hbefore, ?_⟩
  calc
    r.indexAfter.current = r.indexBefore.append.current := by
      rw [r.indexAppendExact]
    _ = r.indexBefore.current + 1 := rfl
    _ = 1 := by simp [hbefore]

theorem intake_history_appends_one_record (r : Receipt) :
    r.historyAfter.committedRecords = r.historyBefore.committedRecords + 1 ∧
      r.historyAfter.snapshotRecords = r.historyBefore.committedRecords + 1 := by
  refine ⟨r.historyAppendExact, ?_⟩
  rw [replanHistory_snapshot_matches_commits r.historyAfter]
  exact r.historyAppendExact

theorem intake_grants_no_downstream_authority (r : Receipt) :
    Bridge.bridgeRuntimeActivatesReplan = false ∧
      Bridge.bridgeRuntimePermitsExecution = false ∧
      Bridge.bridgeRuntimeUpdatesWORLD = false ∧
      Bridge.bridgeRuntimeOverwritesMemory = false ∧
      Bridge.replanNonAuthority.truthAuthority = false ∧
      Bridge.replanNonAuthority.causalAuthority = false ∧
      Bridge.replanNonAuthority.executionAuthority = false ∧
      Bridge.replanNonAuthority.finalCommitmentAuthority = false ∧
      Bridge.replanNonAuthority.memoryOverwriteAuthority = false ∧
      Bridge.replanNonAuthority.selfModificationAuthority = false ∧
      Bridge.replanNonAuthority.hostLicense = false := by
  exact ⟨Bridge.replanActivationForbidden,
    Bridge.executionPermissionForbidden, Bridge.worldUpdateForbidden,
    Bridge.memoryOverwriteForbidden, Bridge.replanNonAuthority.truthForbidden,
    Bridge.replanNonAuthority.causalForbidden,
    Bridge.replanNonAuthority.executionForbidden,
    Bridge.replanNonAuthority.finalForbidden,
    Bridge.replanNonAuthority.overwriteForbidden,
    Bridge.replanNonAuthority.selfModificationForbidden,
    Bridge.replanNonAuthority.licenseForbidden⟩

theorem intake_digest_is_exact (r : Receipt) :
    r.intakeDigest = Bridge.digestOf r.learning r.sourceBinding r.bindState
      r.futureBoundary r.ownership r.activation r.dispositionBoundary
      r.receiptBoundary r.indexBefore r.indexAfter r.historyBefore
      r.historyAfter := by
  exact r.intakeDigestExact

end WorldHostEffectLearningReplanIntakeBridge
end
end PlanOS
end KUOS
