import Mathlib
import KUOS.WORLD.VacuumExpectationHostEffectAtomicCommitIntakeV0_52
import KUOS.ObserveOS.ReplanLineageObservationEnvelopeV0_2

namespace KUOS
namespace ObserveOS

open WORLD VerifyOS LearnOS DecisionOS PlanOS ActOS

structure EffectObservationIdentityBoundary where
  worldIntakeBound : Bool
  hostReceiptBound : Bool
  effectRecordBound : Bool
  operationIdentityExact : Bool
  operationInputExact : Bool
  selectedStepExact : Bool
  targetCycleExact : Bool
  sessionExact : Bool
  actionIntentExact : Bool
  expectedObservationExact : Bool
  worldIntakeRequired : worldIntakeBound = true
  hostReceiptRequired : hostReceiptBound = true
  effectRecordRequired : effectRecordBound = true
  operationRequired : operationIdentityExact = true
  inputRequired : operationInputExact = true
  stepRequired : selectedStepExact = true
  cycleRequired : targetCycleExact = true
  sessionRequired : sessionExact = true
  intentRequired : actionIntentExact = true
  expectedRequired : expectedObservationExact = true

structure IndependentEvidenceCollectionBoundary where
  collectionAuthorized : Bool
  rawArtifactCollected : Bool
  valueCollected : Bool
  collectorIdentityBound : Bool
  independentSourceIdentityBound : Bool
  collectionTimeBound : Bool
  uncertaintyBound : Bool
  calibrationBound : Bool
  contextBound : Bool
  tamperEvidenceBound : Bool
  provenanceBound : Bool
  collectorIndependentFromActOS : Bool
  sourceIndependentFromHostReceipt : Bool
  hostReceiptUsedAsIndependentEvidence : Bool
  collectionCount : Nat
  exactReplayIdempotent : Bool
  conflictingReplayAccepted : Bool
  authorizationRequired : collectionAuthorized = true
  rawRequired : rawArtifactCollected = true
  valueRequired : valueCollected = true
  collectorRequired : collectorIdentityBound = true
  sourceRequired : independentSourceIdentityBound = true
  timeRequired : collectionTimeBound = true
  uncertaintyRequired : uncertaintyBound = true
  calibrationRequired : calibrationBound = true
  contextRequired : contextBound = true
  tamperRequired : tamperEvidenceBound = true
  provenanceRequired : provenanceBound = true
  collectorIndependenceRequired : collectorIndependentFromActOS = true
  sourceIndependenceRequired : sourceIndependentFromHostReceipt = true
  hostReceiptSubstitutionForbidden : hostReceiptUsedAsIndependentEvidence = false
  collectionCountExact : collectionCount = 1
  replayRequired : exactReplayIdempotent = true
  conflictingReplayForbidden : conflictingReplayAccepted = false

structure ObservationReceiptBoundary where
  sourceIntakeBound : Bool
  identityBound : Bool
  evidencePacketBound : Bool
  comparisonBound : Bool
  debtSemanticsBound : Bool
  receiptCommitted : Bool
  receiptImmutable : Bool
  appendOnly : Bool
  exactReplayIdempotent : Bool
  conflictingReplayAccepted : Bool
  verificationCompleted : Bool
  truthPromoted : Bool
  causalAttributionGranted : Bool
  worldUpdated : Bool
  sourceRequired : sourceIntakeBound = true
  identityRequired : identityBound = true
  evidenceRequired : evidencePacketBound = true
  comparisonRequired : comparisonBound = true
  debtRequired : debtSemanticsBound = true
  commitRequired : receiptCommitted = true
  immutabilityRequired : receiptImmutable = true
  appendOnlyRequired : appendOnly = true
  replayRequired : exactReplayIdempotent = true
  conflictingReplayForbidden : conflictingReplayAccepted = false
  verificationForbidden : verificationCompleted = false
  truthPromotionForbidden : truthPromoted = false
  causalAttributionForbidden : causalAttributionGranted = false
  worldUpdateForbidden : worldUpdated = false

structure WorldCommitObservationPrerequisiteBoundary where
  verdict : ComparisonVerdict
  observeReceiptSupplied : Bool
  observationDebtDischarged : Bool
  qualifyingObservationSupplied : Bool
  reobservationRequired : Bool
  verifyReceiptSupplied : Bool
  verifiedWorldDispositionSupplied : Bool
  freshCommitAuthorizationSupplied : Bool
  atomicCommitReady : Bool
  matchedRule : verdict = .matched →
    observeReceiptSupplied = true ∧
      observationDebtDischarged = true ∧
      qualifyingObservationSupplied = true ∧
      reobservationRequired = false
  divergentRule : verdict = .divergent →
    observeReceiptSupplied = true ∧
      observationDebtDischarged = true ∧
      qualifyingObservationSupplied = true ∧
      reobservationRequired = false
  inconclusiveRule : verdict = .inconclusive →
    observeReceiptSupplied = true ∧
      observationDebtDischarged = false ∧
      qualifyingObservationSupplied = false ∧
      reobservationRequired = true
  conflictedRule : verdict = .conflicted →
    observeReceiptSupplied = true ∧
      observationDebtDischarged = false ∧
      qualifyingObservationSupplied = false ∧
      reobservationRequired = true
  verificationNotYetSupplied : verifyReceiptSupplied = false
  dispositionNotYetSupplied : verifiedWorldDispositionSupplied = false
  authorizationNotYetSupplied : freshCommitAuthorizationSupplied = false
  readinessForbidden : atomicCommitReady = false

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
          MaterializationBridge AdmissionBridge AuthorizationBridge
            InvocationBridge)

structure WorldHostEffectObservationBridge where
  ReceiptDigest : Type
  receiptDigestOf :
    WorldVacuumExpectationHostEffectAtomicCommitIntakeEnvelope
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge
            InvocationBridge WorldIntakeBridge →
    ExactObserveCycleGate → UpstreamLineageBoundary →
    EffectObservationBinding → EffectObservationIdentityBoundary →
    IndependentEvidenceCollectionBoundary → EvidenceRequirements →
    ProvenanceTrace → ComparisonBoundary → ObservationDebtSemantics →
    ObservationVerificationBoundary → SingleUseObservation →
    ObservationReceiptBoundary → WorldCommitObservationPrerequisiteBoundary →
    ObserveEventIndex → ObserveEventIndex → ObserveHistory → ReceiptDigest
  nonAuthority : ObserveNonAuthority
  lineageNonAuthority : NonAuthorityBoundary
  observationOwnedByObserveOS : Bool
  verificationOwnedByVerifyOS : Bool
  futureAtomicCommitOwnedByWORLD : Bool
  runtimeCollectsEvidence : Bool
  runtimeCommitsObservation : Bool
  observationOwnerRequired : observationOwnedByObserveOS = true
  verificationOwnerRequired : verificationOwnedByVerifyOS = true
  atomicCommitOwnerRequired : futureAtomicCommitOwnedByWORLD = true
  collectionForbidden : runtimeCollectsEvidence = false
  runtimeCommitForbidden : runtimeCommitsObservation = false

structure WorldHostEffectObservationReceipt
    (Bridge : WorldHostEffectObservationBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge
            InvocationBridge WorldIntakeBridge) where
  source : WorldVacuumExpectationHostEffectAtomicCommitIntakeEnvelope
    K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge AuthorizationBridge
          InvocationBridge WorldIntakeBridge
  exactObserveCycle : ExactObserveCycleGate
  upstreamLineage : UpstreamLineageBoundary
  effectObservation : EffectObservationBinding
  identity : EffectObservationIdentityBoundary
  collection : IndependentEvidenceCollectionBoundary
  evidenceRequirements : EvidenceRequirements
  provenance : ProvenanceTrace
  comparison : ComparisonBoundary
  debtSemantics : ObservationDebtSemantics
  observationVerification : ObservationVerificationBoundary
  singleUse : SingleUseObservation
  receiptBoundary : ObservationReceiptBoundary
  worldPrerequisite : WorldCommitObservationPrerequisiteBoundary
  collectionIndex : ObserveEventIndex
  receiptIndex : ObserveEventIndex
  historyAfter : ObserveHistory
  receiptDigest : Bridge.ReceiptDigest
  sourceAccepted : Bool
  sourceAcceptedRequired : sourceAccepted = true
  sourceIntakeReady : source.intakeReady = true
  sourceCandidateOnly : source.candidateOnly = true
  sourceObservationUncommitted : source.pendingDebt.observationCommitted = false
  sourceVerificationUncommitted : source.pendingDebt.verificationCommitted = false
  sourceIndependentEvidenceAbsent :
    source.pendingDebt.independentWorldEvidencePresent = false
  observeCycleExact :
    exactObserveCycle.actCycle = source.source.binding.targetCycleExact.toNat
  evidenceRequirementsExact :
    evidenceRequirements = WorldIntakeBridge.evidenceRequirements
  provenanceExact : provenance = WorldIntakeBridge.provenanceTrace
  verdictExact : debtSemantics.verdict = comparison.verdict
  qualificationVerdictExact : worldPrerequisite.verdict = comparison.verdict
  observationRecordExact :
    debtSemantics.observationRecorded = receiptBoundary.receiptCommitted
  observationVerificationExact :
    observationVerification.observationRecorded = receiptBoundary.receiptCommitted
  verificationDebtExact :
    observationVerification.verificationRequired = debtSemantics.verificationRequired
  collectionIndexExact :
    collectionIndex.current = source.intakeIndex.current + 1
  receiptIndexExact : receiptIndex = collectionIndex.append
  historyExact : historyAfter.committedRecords =
    source.historyAfter.committedRecords + 2
  receiptDigestExact : receiptDigest = Bridge.receiptDigestOf source
    exactObserveCycle upstreamLineage effectObservation identity collection
    evidenceRequirements provenance comparison debtSemantics
    observationVerification singleUse receiptBoundary worldPrerequisite
    collectionIndex receiptIndex historyAfter

namespace WorldHostEffectObservationBridge

variable
    {Bridge : WorldHostEffectObservationBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge
            InvocationBridge WorldIntakeBridge}

abbrev Receipt := WorldHostEffectObservationReceipt
  K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
    GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
      MaterializationBridge AdmissionBridge AuthorizationBridge
        InvocationBridge WorldIntakeBridge Bridge

theorem observation_requires_ready_uncommitted_world_intake (r : Receipt) :
    r.sourceAccepted = true ∧ r.source.intakeReady = true ∧
      r.source.candidateOnly = true ∧
      r.source.pendingDebt.observationCommitted = false ∧
      r.source.pendingDebt.verificationCommitted = false ∧
      r.source.pendingDebt.independentWorldEvidencePresent = false := by
  exact ⟨r.sourceAcceptedRequired, r.sourceIntakeReady,
    r.sourceCandidateOnly, r.sourceObservationUncommitted,
    r.sourceVerificationUncommitted, r.sourceIndependentEvidenceAbsent⟩

theorem observation_uses_exact_cycle_and_preserves_lineage (r : Receipt) :
    r.exactObserveCycle.observeCycle = r.exactObserveCycle.actCycle ∧
      r.exactObserveCycle.observePhase = true ∧
      r.upstreamLineage.actHandoffPreserved = true ∧
      r.upstreamLineage.actCompletionPreserved = true ∧
      r.upstreamLineage.compilerReceiptPreserved = true ∧
      r.upstreamLineage.replanReceiptPreserved = true ∧
      r.upstreamLineage.qiConditionPreserved = true ∧
      r.upstreamLineage.decisionReceiptPreserved = true ∧
      r.upstreamLineage.selectedCandidatePreserved = true ∧
      r.upstreamLineage.selectedStepPreserved = true := by
  exact ⟨r.exactObserveCycle.exactCycleRequired,
    r.exactObserveCycle.observePhaseRequired,
    r.upstreamLineage.actHandoffRequired,
    r.upstreamLineage.actCompletionRequired,
    r.upstreamLineage.compilerRequired, r.upstreamLineage.replanRequired,
    r.upstreamLineage.qiRequired, r.upstreamLineage.decisionRequired,
    r.upstreamLineage.candidateRequired, r.upstreamLineage.stepRequired⟩

theorem source_effect_and_expected_observation_are_bound (r : Receipt) :
    r.effectObservation.sourceEffectRecorded = true ∧
      r.effectObservation.observationRequired = true ∧
      r.effectObservation.observationTargetPreserved = true ∧
      r.identity.worldIntakeBound = true ∧
      r.identity.hostReceiptBound = true ∧
      r.identity.effectRecordBound = true ∧
      r.identity.expectedObservationExact = true := by
  exact ⟨r.effectObservation.sourceRequired, r.effectObservation.debtRequired,
    r.effectObservation.targetRequired, r.identity.worldIntakeRequired,
    r.identity.hostReceiptRequired, r.identity.effectRecordRequired,
    r.identity.expectedRequired⟩

theorem effect_identity_is_exactly_preserved (r : Receipt) :
    r.identity.operationIdentityExact = true ∧
      r.identity.operationInputExact = true ∧
      r.identity.selectedStepExact = true ∧
      r.identity.targetCycleExact = true ∧
      r.identity.sessionExact = true ∧
      r.identity.actionIntentExact = true := by
  exact ⟨r.identity.operationRequired, r.identity.inputRequired,
    r.identity.stepRequired, r.identity.cycleRequired,
    r.identity.sessionRequired, r.identity.intentRequired⟩

theorem evidence_collection_is_independent_complete_and_single (r : Receipt) :
    r.collection.collectionAuthorized = true ∧
      r.collection.rawArtifactCollected = true ∧
      r.collection.valueCollected = true ∧
      r.collection.collectorIdentityBound = true ∧
      r.collection.independentSourceIdentityBound = true ∧
      r.collection.collectorIndependentFromActOS = true ∧
      r.collection.sourceIndependentFromHostReceipt = true ∧
      r.collection.hostReceiptUsedAsIndependentEvidence = false ∧
      r.collection.collectionCount = 1 := by
  exact ⟨r.collection.authorizationRequired, r.collection.rawRequired,
    r.collection.valueRequired, r.collection.collectorRequired,
    r.collection.sourceRequired, r.collection.collectorIndependenceRequired,
    r.collection.sourceIndependenceRequired,
    r.collection.hostReceiptSubstitutionForbidden,
    r.collection.collectionCountExact⟩

theorem evidence_quality_context_and_provenance_are_bound (r : Receipt) :
    r.collection.collectionTimeBound = true ∧
      r.collection.uncertaintyBound = true ∧
      r.collection.calibrationBound = true ∧
      r.collection.contextBound = true ∧
      r.collection.tamperEvidenceBound = true ∧
      r.collection.provenanceBound = true ∧
      r.provenance.evidenceChainComplete = true ∧
      r.provenance.sourceIdentityPreserved = true ∧
      r.provenance.rawArtifactsImmutable = true ∧
      r.provenance.noUnboundEvidence = true := by
  exact ⟨r.collection.timeRequired, r.collection.uncertaintyRequired,
    r.collection.calibrationRequired, r.collection.contextRequired,
    r.collection.tamperRequired, r.collection.provenanceRequired,
    r.provenance.chainRequired, r.provenance.sourceRequired,
    r.provenance.immutableRequired, r.provenance.boundRequired⟩

theorem evidence_contract_reuses_world_intake_requirements (r : Receipt) :
    r.evidenceRequirements = WorldIntakeBridge.evidenceRequirements ∧
      r.provenance = WorldIntakeBridge.provenanceTrace := by
  exact ⟨r.evidenceRequirementsExact, r.provenanceExact⟩

theorem comparison_is_observation_not_verification_truth_or_causality
    (r : Receipt) :
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

theorem matched_observation_discharges_observation_debt
    (r : Receipt) (h : r.comparison.verdict = .matched) :
    r.debtSemantics.observationDebtDischarged = true ∧
      r.debtSemantics.reobservationRequired = false ∧
      r.worldPrerequisite.qualifyingObservationSupplied = true := by
  have hdebt : r.debtSemantics.verdict = .matched := by
    rw [r.verdictExact]
    exact h
  have hqualification : r.worldPrerequisite.verdict = .matched := by
    rw [r.qualificationVerdictExact]
    exact h
  exact ⟨(r.debtSemantics.matchedDebt hdebt).1,
    (r.debtSemantics.matchedDebt hdebt).2,
    (r.worldPrerequisite.matchedRule hqualification).2.2.1⟩

theorem divergent_observation_discharges_observation_debt
    (r : Receipt) (h : r.comparison.verdict = .divergent) :
    r.debtSemantics.observationDebtDischarged = true ∧
      r.debtSemantics.reobservationRequired = false ∧
      r.worldPrerequisite.qualifyingObservationSupplied = true := by
  have hdebt : r.debtSemantics.verdict = .divergent := by
    rw [r.verdictExact]
    exact h
  have hqualification : r.worldPrerequisite.verdict = .divergent := by
    rw [r.qualificationVerdictExact]
    exact h
  exact ⟨(r.debtSemantics.divergentDebt hdebt).1,
    (r.debtSemantics.divergentDebt hdebt).2,
    (r.worldPrerequisite.divergentRule hqualification).2.2.1⟩

theorem inconclusive_observation_requires_reobservation
    (r : Receipt) (h : r.comparison.verdict = .inconclusive) :
    r.debtSemantics.observationDebtDischarged = false ∧
      r.debtSemantics.reobservationRequired = true ∧
      r.worldPrerequisite.qualifyingObservationSupplied = false := by
  have hdebt : r.debtSemantics.verdict = .inconclusive := by
    rw [r.verdictExact]
    exact h
  have hqualification : r.worldPrerequisite.verdict = .inconclusive := by
    rw [r.qualificationVerdictExact]
    exact h
  exact ⟨(r.debtSemantics.inconclusiveDebt hdebt).1,
    (r.debtSemantics.inconclusiveDebt hdebt).2,
    (r.worldPrerequisite.inconclusiveRule hqualification).2.2.1⟩

theorem conflicted_observation_requires_reobservation
    (r : Receipt) (h : r.comparison.verdict = .conflicted) :
    r.debtSemantics.observationDebtDischarged = false ∧
      r.debtSemantics.reobservationRequired = true ∧
      r.worldPrerequisite.qualifyingObservationSupplied = false := by
  have hdebt : r.debtSemantics.verdict = .conflicted := by
    rw [r.verdictExact]
    exact h
  have hqualification : r.worldPrerequisite.verdict = .conflicted := by
    rw [r.qualificationVerdictExact]
    exact h
  exact ⟨(r.debtSemantics.conflictedDebt hdebt).1,
    (r.debtSemantics.conflictedDebt hdebt).2,
    (r.worldPrerequisite.conflictedRule hqualification).2.2.1⟩

theorem every_observation_receipt_preserves_verification_debt (r : Receipt) :
    r.debtSemantics.verificationRequired = true ∧
      r.observationVerification.observationNotVerification = true ∧
      r.observationVerification.verificationRequired = true ∧
      r.worldPrerequisite.verifyReceiptSupplied = false ∧
      r.worldPrerequisite.verifiedWorldDispositionSupplied = false ∧
      r.worldPrerequisite.freshCommitAuthorizationSupplied = false ∧
      r.worldPrerequisite.atomicCommitReady = false := by
  exact ⟨r.debtSemantics.verificationPreserved,
    r.observationVerification.distinctionRequired,
    r.observationVerification.verificationDebtRequired,
    r.worldPrerequisite.verificationNotYetSupplied,
    r.worldPrerequisite.dispositionNotYetSupplied,
    r.worldPrerequisite.authorizationNotYetSupplied,
    r.worldPrerequisite.readinessForbidden⟩

theorem observation_receipt_is_immutable_append_only_and_replay_safe
    (r : Receipt) :
    r.receiptBoundary.sourceIntakeBound = true ∧
      r.receiptBoundary.identityBound = true ∧
      r.receiptBoundary.evidencePacketBound = true ∧
      r.receiptBoundary.comparisonBound = true ∧
      r.receiptBoundary.debtSemanticsBound = true ∧
      r.receiptBoundary.receiptCommitted = true ∧
      r.receiptBoundary.receiptImmutable = true ∧
      r.receiptBoundary.appendOnly = true ∧
      r.receiptBoundary.exactReplayIdempotent = true ∧
      r.receiptBoundary.conflictingReplayAccepted = false := by
  exact ⟨r.receiptBoundary.sourceRequired, r.receiptBoundary.identityRequired,
    r.receiptBoundary.evidenceRequired,
    r.receiptBoundary.comparisonRequired, r.receiptBoundary.debtRequired,
    r.receiptBoundary.commitRequired,
    r.receiptBoundary.immutabilityRequired,
    r.receiptBoundary.appendOnlyRequired, r.receiptBoundary.replayRequired,
    r.receiptBoundary.conflictingReplayForbidden⟩

theorem observation_receipt_grants_no_verification_truth_causality_or_world_update
    (r : Receipt) :
    r.receiptBoundary.verificationCompleted = false ∧
      r.receiptBoundary.truthPromoted = false ∧
      r.receiptBoundary.causalAttributionGranted = false ∧
      r.receiptBoundary.worldUpdated = false ∧
      Bridge.nonAuthority.truthAuthority = false ∧
      Bridge.nonAuthority.verificationAuthority = false ∧
      Bridge.nonAuthority.executionAuthority = false ∧
      Bridge.lineageNonAuthority.effectPermissionGranted = false ∧
      Bridge.lineageNonAuthority.memoryOverwrite = false := by
  exact ⟨r.receiptBoundary.verificationForbidden,
    r.receiptBoundary.truthPromotionForbidden,
    r.receiptBoundary.causalAttributionForbidden,
    r.receiptBoundary.worldUpdateForbidden,
    Bridge.nonAuthority.truthForbidden,
    Bridge.nonAuthority.verificationForbidden,
    Bridge.nonAuthority.executionForbidden,
    Bridge.lineageNonAuthority.effectPermissionForbidden,
    Bridge.lineageNonAuthority.overwriteForbidden⟩

theorem evidence_collection_and_receipt_are_single_use (r : Receipt) :
    r.collection.exactReplayIdempotent = true ∧
      r.collection.conflictingReplayAccepted = false ∧
      r.singleUse.completionCount ≤ 1 := by
  exact ⟨r.collection.replayRequired,
    r.collection.conflictingReplayForbidden,
    completion_is_single_use r.singleUse⟩

theorem observation_events_append_strictly (r : Receipt) :
    r.source.intakeIndex.current < r.collectionIndex.current ∧
      r.collectionIndex.current < r.receiptIndex.current := by
  constructor
  · rw [r.collectionIndexExact]
    omega
  · rw [r.receiptIndexExact]
    exact observeEventIndex_strict r.collectionIndex

theorem observation_history_appends_two_records (r : Receipt) :
    r.historyAfter.committedRecords = r.source.historyAfter.committedRecords + 2 ∧
      r.historyAfter.snapshotRecords = r.source.historyAfter.committedRecords + 2 := by
  refine ⟨r.historyExact, ?_⟩
  rw [observeHistory_snapshot_matches_commits r.historyAfter]
  exact r.historyExact

theorem ownership_is_separated (_r : Receipt) :
    Bridge.observationOwnedByObserveOS = true ∧
      Bridge.verificationOwnedByVerifyOS = true ∧
      Bridge.futureAtomicCommitOwnedByWORLD = true ∧
      Bridge.runtimeCollectsEvidence = false ∧
      Bridge.runtimeCommitsObservation = false := by
  exact ⟨Bridge.observationOwnerRequired, Bridge.verificationOwnerRequired,
    Bridge.atomicCommitOwnerRequired, Bridge.collectionForbidden,
    Bridge.runtimeCommitForbidden⟩

theorem observation_receipt_digest_is_exact (r : Receipt) :
    r.receiptDigest = Bridge.receiptDigestOf r.source r.exactObserveCycle
      r.upstreamLineage r.effectObservation r.identity r.collection
      r.evidenceRequirements r.provenance r.comparison r.debtSemantics
      r.observationVerification r.singleUse r.receiptBoundary
      r.worldPrerequisite r.collectionIndex r.receiptIndex r.historyAfter := by
  exact r.receiptDigestExact

end WorldHostEffectObservationBridge
end
end ObserveOS
end KUOS
