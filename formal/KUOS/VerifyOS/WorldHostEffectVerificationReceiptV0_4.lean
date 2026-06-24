import Mathlib
import KUOS.ObserveOS.WorldHostEffectObservationReceiptV0_4
import KUOS.VerifyOS.EvidenceBoundVerificationV0_1
import KUOS.VerifyOS.ReplanLineageVerificationEnvelopeV0_2

namespace KUOS
namespace VerifyOS

open WORLD ObserveOS LearnOS DecisionOS PlanOS ActOS

structure QualifyingObservationBoundary where
  sourceReceiptBound : Bool
  sourceReceiptCommitted : Bool
  observationDebtDischarged : Bool
  qualifyingObservationSupplied : Bool
  reobservationRequired : Bool
  verificationRequired : Bool
  verifyReceiptAlreadySupplied : Bool
  sourceRequired : sourceReceiptBound = true
  committedRequired : sourceReceiptCommitted = true
  observationDebtRequired : observationDebtDischarged = true
  qualificationRequired : qualifyingObservationSupplied = true
  reobservationClosed : reobservationRequired = false
  verificationDebtRequired : verificationRequired = true
  duplicateVerifyForbidden : verifyReceiptAlreadySupplied = false

structure IndependentVerificationExecutionBoundary where
  verifyRequestAuthorized : Bool
  verifierIndependentFromObserveOS : Bool
  verifierIndependentFromActOS : Bool
  verifierIndependentFromHostReceipt : Bool
  verificationWindowBound : Bool
  protocolBound : Bool
  criterionBoundBeforeAdjudication : Bool
  evidenceIntegrityRechecked : Bool
  provenanceIntegrityRechecked : Bool
  uncertaintyPreserved : Bool
  calibrationPreserved : Bool
  verificationCount : Nat
  exactReplayIdempotent : Bool
  conflictingReplayAccepted : Bool
  authorizationRequired : verifyRequestAuthorized = true
  observeIndependenceRequired : verifierIndependentFromObserveOS = true
  actIndependenceRequired : verifierIndependentFromActOS = true
  hostIndependenceRequired : verifierIndependentFromHostReceipt = true
  windowRequired : verificationWindowBound = true
  protocolRequired : protocolBound = true
  temporalRequired : criterionBoundBeforeAdjudication = true
  evidenceRequired : evidenceIntegrityRechecked = true
  provenanceRequired : provenanceIntegrityRechecked = true
  uncertaintyRequired : uncertaintyPreserved = true
  calibrationRequired : calibrationPreserved = true
  countRequired : verificationCount = 1
  replayRequired : exactReplayIdempotent = true
  conflictingReplayForbidden : conflictingReplayAccepted = false

inductive WorldDispositionCandidate where
  | adopt
  | reject
  | deferOrReobserve
  deriving DecidableEq, Repr

structure WorldDispositionCandidateBoundary where
  verdict : VerificationVerdict
  disposition : WorldDispositionCandidate
  dispositionCandidateCommitted : Bool
  governanceReviewRequired : Bool
  worldCommitSeparate : Bool
  freshCommitAuthorizationRequired : Bool
  freshCommitAuthorizationSupplied : Bool
  atomicCommitReady : Bool
  automaticWorldAdoption : Bool
  automaticWorldRejection : Bool
  automaticWorldCommit : Bool
  passedRule : verdict = .passed → disposition = .adopt
  failedRule : verdict = .failed → disposition = .reject
  indeterminateRule : verdict = .indeterminate → disposition = .deferOrReobserve
  candidateRequired : dispositionCandidateCommitted = true
  governanceRequired : governanceReviewRequired = true
  separateCommitRequired : worldCommitSeparate = true
  authorizationRequired : freshCommitAuthorizationRequired = true
  authorizationNotYetSupplied : freshCommitAuthorizationSupplied = false
  readinessForbidden : atomicCommitReady = false
  adoptionForbidden : automaticWorldAdoption = false
  rejectionForbidden : automaticWorldRejection = false
  commitForbidden : automaticWorldCommit = false

structure VerificationReceiptBoundary where
  sourceObservationBound : Bool
  criterionBound : Bool
  challengeBound : Bool
  corroborationBound : Bool
  adjudicationBound : Bool
  debtSemanticsBound : Bool
  receiptCommitted : Bool
  receiptImmutable : Bool
  appendOnly : Bool
  exactReplayIdempotent : Bool
  conflictingReplayAccepted : Bool
  sourceRequired : sourceObservationBound = true
  criterionRequired : criterionBound = true
  challengeRequired : challengeBound = true
  corroborationRequired : corroborationBound = true
  adjudicationRequired : adjudicationBound = true
  debtRequired : debtSemanticsBound = true
  commitRequired : receiptCommitted = true
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
          MaterializationBridge AdmissionBridge AuthorizationBridge
            InvocationBridge)
    (ObservationBridge : WorldHostEffectObservationBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge
            InvocationBridge WorldIntakeBridge)

structure WorldHostEffectVerificationBridge where
  ReceiptDigest : Type
  receiptDigestOf :
    WorldHostEffectObservationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge
            InvocationBridge WorldIntakeBridge ObservationBridge →
    ExactVerifyCycleGate → UpstreamLineageBoundary →
    QualifyingObservationBoundary → SourceObservationBinding →
    CriterionEvidenceBinding → CriterionBinding → FalsificationBoundary →
    ChallengeRequirements → CorroborationSurface → AdjudicationBoundary →
    VerificationDebtSemantics → VerificationTruthBoundary →
    QiVerificationBoundary → FutureOnlyLearningBoundary →
    IndependentVerificationExecutionBoundary → SingleUseVerification →
    VerificationReceiptBoundary → WorldDispositionCandidateBoundary →
    VerifyEventIndex → VerifyEventIndex → VerifyHistory → ReceiptDigest
  nonAuthority : VerifyNonAuthority
  lineageNonAuthority : NonAuthorityBoundary
  verificationOwnedByVerifyOS : Bool
  observationOwnedByObserveOS : Bool
  dispositionCandidateOwnedByWORLD : Bool
  futureCommitOwnedByWORLD : Bool
  runtimePerformsVerification : Bool
  verificationOwnerRequired : verificationOwnedByVerifyOS = true
  observationOwnerRequired : observationOwnedByObserveOS = true
  dispositionOwnerRequired : dispositionCandidateOwnedByWORLD = true
  commitOwnerRequired : futureCommitOwnedByWORLD = true
  runtimeVerificationForbidden : runtimePerformsVerification = false

structure WorldHostEffectVerificationReceipt
    (Bridge : WorldHostEffectVerificationBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge
            InvocationBridge WorldIntakeBridge ObservationBridge) where
  source : WorldHostEffectObservationReceipt
    K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge AuthorizationBridge
          InvocationBridge WorldIntakeBridge ObservationBridge
  exactVerifyCycle : ExactVerifyCycleGate
  upstreamLineage : UpstreamLineageBoundary
  qualification : QualifyingObservationBoundary
  sourceBinding : SourceObservationBinding
  criterionEvidence : CriterionEvidenceBinding
  criterion : CriterionBinding
  falsification : FalsificationBoundary
  challenge : ChallengeRequirements
  corroboration : CorroborationSurface
  adjudication : AdjudicationBoundary
  debtSemantics : VerificationDebtSemantics
  truthBoundary : VerificationTruthBoundary
  qiBoundary : QiVerificationBoundary
  learningBoundary : FutureOnlyLearningBoundary
  executionBoundary : IndependentVerificationExecutionBoundary
  singleUse : SingleUseVerification
  receiptBoundary : VerificationReceiptBoundary
  disposition : WorldDispositionCandidateBoundary
  indexBefore : VerifyEventIndex
  indexAfter : VerifyEventIndex
  historyAfter : VerifyHistory
  receiptDigest : Bridge.ReceiptDigest
  sourceAccepted : Bool
  sourceAcceptedRequired : sourceAccepted = true
  sourceReceiptCommitted : source.receiptBoundary.receiptCommitted = true
  sourceQualifyingObservation :
    source.worldPrerequisite.qualifyingObservationSupplied = true
  sourceObservationDebtDischarged :
    source.worldPrerequisite.observationDebtDischarged = true
  sourceReobservationClosed : source.worldPrerequisite.reobservationRequired = false
  sourceVerificationDebtOpen : source.debtSemantics.verificationRequired = true
  sourceVerifyReceiptAbsent : source.worldPrerequisite.verifyReceiptSupplied = false
  verifyCycleExact : exactVerifyCycle.observeCycle = source.exactObserveCycle.observeCycle
  verdictExact : debtSemantics.verdict = adjudication.verdict
  dispositionVerdictExact : disposition.verdict = adjudication.verdict
  verificationRecordExact :
    debtSemantics.verificationRecorded = receiptBoundary.receiptCommitted
  indexStartsAfterObservation : indexBefore.current = source.receiptIndex.current + 1
  indexAppendExact : indexAfter = indexBefore.append
  historyExact : historyAfter.committedRecords =
    source.historyAfter.committedRecords + 1
  receiptDigestExact : receiptDigest = Bridge.receiptDigestOf source
    exactVerifyCycle upstreamLineage qualification sourceBinding
    criterionEvidence criterion falsification challenge corroboration
    adjudication debtSemantics truthBoundary qiBoundary learningBoundary
    executionBoundary singleUse receiptBoundary disposition indexBefore
    indexAfter historyAfter

namespace WorldHostEffectVerificationBridge

variable
    {Bridge : WorldHostEffectVerificationBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge
            InvocationBridge WorldIntakeBridge ObservationBridge}

abbrev Receipt := WorldHostEffectVerificationReceipt
  K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
    GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
      MaterializationBridge AdmissionBridge AuthorizationBridge
        InvocationBridge WorldIntakeBridge ObservationBridge Bridge

theorem verification_requires_qualifying_observation (r : Receipt) :
    r.sourceAccepted = true ∧
      r.source.receiptBoundary.receiptCommitted = true ∧
      r.source.worldPrerequisite.qualifyingObservationSupplied = true ∧
      r.source.worldPrerequisite.observationDebtDischarged = true ∧
      r.source.worldPrerequisite.reobservationRequired = false ∧
      r.source.debtSemantics.verificationRequired = true ∧
      r.source.worldPrerequisite.verifyReceiptSupplied = false := by
  exact ⟨r.sourceAcceptedRequired, r.sourceReceiptCommitted,
    r.sourceQualifyingObservation, r.sourceObservationDebtDischarged,
    r.sourceReobservationClosed, r.sourceVerificationDebtOpen,
    r.sourceVerifyReceiptAbsent⟩

theorem qualification_gate_is_complete (r : Receipt) :
    r.qualification.sourceReceiptBound = true ∧
      r.qualification.sourceReceiptCommitted = true ∧
      r.qualification.observationDebtDischarged = true ∧
      r.qualification.qualifyingObservationSupplied = true ∧
      r.qualification.reobservationRequired = false ∧
      r.qualification.verificationRequired = true ∧
      r.qualification.verifyReceiptAlreadySupplied = false := by
  exact ⟨r.qualification.sourceRequired, r.qualification.committedRequired,
    r.qualification.observationDebtRequired,
    r.qualification.qualificationRequired,
    r.qualification.reobservationClosed,
    r.qualification.verificationDebtRequired,
    r.qualification.duplicateVerifyForbidden⟩

theorem nonqualifying_observation_cannot_satisfy_gate
    (q : QualifyingObservationBoundary)
    (h : q.qualifyingObservationSupplied = false) : False := by
  rw [q.qualificationRequired] at h
  contradiction

theorem verification_uses_exact_observe_cycle (r : Receipt) :
    r.exactVerifyCycle.verifyCycle = r.source.exactObserveCycle.observeCycle ∧
      r.exactVerifyCycle.verifyPhase = true := by
  constructor
  · calc
      r.exactVerifyCycle.verifyCycle = r.exactVerifyCycle.observeCycle :=
        r.exactVerifyCycle.exactCycleRequired
      _ = r.source.exactObserveCycle.observeCycle := r.verifyCycleExact
  · exact r.exactVerifyCycle.verifyPhaseRequired

theorem verification_preserves_full_lineage (r : Receipt) :
    r.upstreamLineage.observeHandoffPreserved = true ∧
      r.upstreamLineage.observeCompletionPreserved = true ∧
      r.upstreamLineage.actCompletionPreserved = true ∧
      r.upstreamLineage.compilerReceiptPreserved = true ∧
      r.upstreamLineage.replanReceiptPreserved = true ∧
      r.upstreamLineage.qiConditionPreserved = true ∧
      r.upstreamLineage.decisionReceiptPreserved = true ∧
      r.upstreamLineage.selectedCandidatePreserved = true ∧
      r.upstreamLineage.selectedStepPreserved = true := by
  exact ⟨r.upstreamLineage.observeHandoffRequired,
    r.upstreamLineage.observeCompletionRequired,
    r.upstreamLineage.actCompletionRequired,
    r.upstreamLineage.compilerRequired, r.upstreamLineage.replanRequired,
    r.upstreamLineage.qiRequired, r.upstreamLineage.decisionRequired,
    r.upstreamLineage.candidateRequired, r.upstreamLineage.stepRequired⟩

theorem source_observation_criterion_and_evidence_are_exact (r : Receipt) :
    r.sourceBinding.committedObserveState = true ∧
      r.sourceBinding.observationRecorded = true ∧
      r.sourceBinding.verificationRequired = true ∧
      r.sourceBinding.comparisonReceiptCanonical = true ∧
      r.sourceBinding.sourceEffectBound = true ∧
      r.sourceBinding.evidencePacketBound = true ∧
      r.sourceBinding.qualityReportBound = true ∧
      r.criterionEvidence.handoffObserveDigest =
        r.criterionEvidence.sourceObserveDigest ∧
      r.criterionEvidence.verifiedCriterionDigest =
        r.criterionEvidence.sourceCriterionDigest ∧
      r.criterionEvidence.verifiedEvidenceDigest =
        r.criterionEvidence.sourceEvidenceDigest := by
  exact ⟨r.sourceBinding.committedRequired,
    r.sourceBinding.recordedRequired, r.sourceBinding.debtRequired,
    r.sourceBinding.comparisonRequired, r.sourceBinding.effectRequired,
    r.sourceBinding.evidenceRequired, r.sourceBinding.qualityRequired,
    r.criterionEvidence.observeRequired, r.criterionEvidence.criterionRequired,
    r.criterionEvidence.evidenceRequired⟩

theorem criterion_challenge_and_falsification_are_complete (r : Receipt) :
    r.criterion.inheritedCriterionBound = true ∧
      r.criterion.evaluationMethodBound = true ∧
      r.criterion.successConditionBound = true ∧
      r.criterion.failureConditionBound = true ∧
      r.criterion.falsificationConditionBound = true ∧
      r.criterion.evidenceRequirementsBound = true ∧
      r.criterion.definedBeforeAdjudication = true ∧
      r.criterion.permitsCausalAttribution = false ∧
      r.falsification.falsificationAttempted = true ∧
      r.falsification.counterevidencePreserved = true ∧
      r.falsification.independentAssessmentPreserved = true ∧
      r.challenge.challengeComplete = true := by
  exact ⟨r.criterion.inheritedRequired, r.criterion.methodRequired,
    r.criterion.successRequired, r.criterion.failureRequired,
    r.criterion.falsificationRequired, r.criterion.evidenceRequired,
    r.criterion.temporalRequired, r.criterion.causalForbidden,
    r.falsification.falsificationRequired,
    r.falsification.counterevidenceRequired,
    r.falsification.independenceRequired, r.challenge.completionRequired⟩

theorem verification_execution_is_independent_single_and_replay_safe (r : Receipt) :
    r.executionBoundary.verifyRequestAuthorized = true ∧
      r.executionBoundary.verifierIndependentFromObserveOS = true ∧
      r.executionBoundary.verifierIndependentFromActOS = true ∧
      r.executionBoundary.verifierIndependentFromHostReceipt = true ∧
      r.executionBoundary.verificationWindowBound = true ∧
      r.executionBoundary.protocolBound = true ∧
      r.executionBoundary.evidenceIntegrityRechecked = true ∧
      r.executionBoundary.provenanceIntegrityRechecked = true ∧
      r.executionBoundary.verificationCount = 1 ∧
      r.executionBoundary.exactReplayIdempotent = true ∧
      r.executionBoundary.conflictingReplayAccepted = false := by
  exact ⟨r.executionBoundary.authorizationRequired,
    r.executionBoundary.observeIndependenceRequired,
    r.executionBoundary.actIndependenceRequired,
    r.executionBoundary.hostIndependenceRequired,
    r.executionBoundary.windowRequired, r.executionBoundary.protocolRequired,
    r.executionBoundary.evidenceRequired,
    r.executionBoundary.provenanceRequired, r.executionBoundary.countRequired,
    r.executionBoundary.replayRequired,
    r.executionBoundary.conflictingReplayForbidden⟩

theorem passed_verification_maps_to_adopt_candidate
    (r : Receipt) (h : r.adjudication.verdict = .passed) :
    r.debtSemantics.verificationDebtDischarged = true ∧
      r.debtSemantics.verificationRequired = false ∧
      r.debtSemantics.correctiveActionRequired = false ∧
      r.disposition.disposition = .adopt := by
  have hd : r.debtSemantics.verdict = .passed := r.verdictExact.trans h
  have hw : r.disposition.verdict = .passed := r.dispositionVerdictExact.trans h
  exact ⟨(r.debtSemantics.passedDebt hd).1,
    (r.debtSemantics.passedDebt hd).2.1,
    (r.debtSemantics.passedDebt hd).2.2.2,
    r.disposition.passedRule hw⟩

theorem failed_verification_maps_to_reject_candidate
    (r : Receipt) (h : r.adjudication.verdict = .failed) :
    r.debtSemantics.verificationDebtDischarged = true ∧
      r.debtSemantics.verificationRequired = false ∧
      r.debtSemantics.correctiveActionRequired = true ∧
      r.disposition.disposition = .reject := by
  have hd : r.debtSemantics.verdict = .failed := r.verdictExact.trans h
  have hw : r.disposition.verdict = .failed := r.dispositionVerdictExact.trans h
  exact ⟨(r.debtSemantics.failedDebt hd).1,
    (r.debtSemantics.failedDebt hd).2.1,
    (r.debtSemantics.failedDebt hd).2.2.2,
    r.disposition.failedRule hw⟩

theorem indeterminate_verification_maps_to_defer_or_reobserve
    (r : Receipt) (h : r.adjudication.verdict = .indeterminate) :
    r.debtSemantics.verificationDebtDischarged = false ∧
      r.debtSemantics.verificationRequired = true ∧
      r.debtSemantics.reobservationRequired = true ∧
      r.disposition.disposition = .deferOrReobserve := by
  have hd : r.debtSemantics.verdict = .indeterminate := r.verdictExact.trans h
  have hw : r.disposition.verdict = .indeterminate :=
    r.dispositionVerdictExact.trans h
  exact ⟨(r.debtSemantics.indeterminateDebt hd).1,
    (r.debtSemantics.indeterminateDebt hd).2.1,
    (r.debtSemantics.indeterminateDebt hd).2.2.1,
    r.disposition.indeterminateRule hw⟩

theorem verification_remains_candidate_not_truth_causality_or_commit
    (r : Receipt) :
    r.truthBoundary.verificationRecorded = true ∧
      r.truthBoundary.verificationNotTruth = true ∧
      r.truthBoundary.causalAttributionGranted = false ∧
      r.disposition.dispositionCandidateCommitted = true ∧
      r.disposition.governanceReviewRequired = true ∧
      r.disposition.worldCommitSeparate = true ∧
      r.disposition.freshCommitAuthorizationRequired = true ∧
      r.disposition.freshCommitAuthorizationSupplied = false ∧
      r.disposition.atomicCommitReady = false ∧
      r.disposition.automaticWorldAdoption = false ∧
      r.disposition.automaticWorldRejection = false ∧
      r.disposition.automaticWorldCommit = false := by
  exact ⟨r.truthBoundary.recordRequired, r.truthBoundary.distinctionRequired,
    r.truthBoundary.causalAttributionForbidden,
    r.disposition.candidateRequired, r.disposition.governanceRequired,
    r.disposition.separateCommitRequired, r.disposition.authorizationRequired,
    r.disposition.authorizationNotYetSupplied,
    r.disposition.readinessForbidden, r.disposition.adoptionForbidden,
    r.disposition.rejectionForbidden, r.disposition.commitForbidden⟩

theorem verification_learning_handoff_is_future_only (r : Receipt) :
    r.debtSemantics.learningRequired = true ∧
      r.learningBoundary.learningRequired = true ∧
      r.learningBoundary.learningFutureOnly = true ∧
      r.learningBoundary.automaticLearning = false := by
  exact ⟨r.debtSemantics.learningAlways,
    r.learningBoundary.learningDebtRequired,
    r.learningBoundary.futureOnlyRequired,
    r.learningBoundary.automaticLearningForbidden⟩

theorem verification_receipt_is_immutable_append_only_and_single_use
    (r : Receipt) :
    r.receiptBoundary.receiptCommitted = true ∧
      r.receiptBoundary.receiptImmutable = true ∧
      r.receiptBoundary.appendOnly = true ∧
      r.receiptBoundary.exactReplayIdempotent = true ∧
      r.receiptBoundary.conflictingReplayAccepted = false ∧
      r.singleUse.completionCount ≤ 1 := by
  exact ⟨r.receiptBoundary.commitRequired,
    r.receiptBoundary.immutableRequired,
    r.receiptBoundary.appendOnlyRequired,
    r.receiptBoundary.replayRequired,
    r.receiptBoundary.conflictingReplayForbidden,
    verification_completion_is_single_use r.singleUse⟩

theorem verification_events_append_exactly_once (r : Receipt) :
    r.source.receiptIndex.current < r.indexBefore.current ∧
      r.indexBefore.current < r.indexAfter.current := by
  constructor
  · rw [r.indexStartsAfterObservation]
    omega
  · rw [r.indexAppendExact]
    exact verifyEventIndex_strict r.indexBefore

theorem verification_history_appends_one_record (r : Receipt) :
    r.historyAfter.committedRecords = r.source.historyAfter.committedRecords + 1 ∧
      r.historyAfter.snapshotRecords = r.source.historyAfter.committedRecords + 1 := by
  refine ⟨r.historyExact, ?_⟩
  rw [verifyHistory_snapshot_matches_commits r.historyAfter]
  exact r.historyExact

theorem verification_grants_no_downstream_authority (r : Receipt) :
    Bridge.verificationOwnedByVerifyOS = true ∧
      Bridge.observationOwnedByObserveOS = true ∧
      Bridge.dispositionCandidateOwnedByWORLD = true ∧
      Bridge.futureCommitOwnedByWORLD = true ∧
      Bridge.runtimePerformsVerification = false ∧
      Bridge.nonAuthority.truthAuthority = false ∧
      Bridge.nonAuthority.causalAuthority = false ∧
      Bridge.nonAuthority.executionAuthority = false ∧
      Bridge.nonAuthority.memoryOverwriteAuthority = false ∧
      Bridge.lineageNonAuthority.truthGranted = false ∧
      Bridge.lineageNonAuthority.causalGranted = false ∧
      Bridge.lineageNonAuthority.executionGranted = false ∧
      Bridge.lineageNonAuthority.memoryOverwrite = false ∧
      Bridge.lineageNonAuthority.automaticLearning = false := by
  exact ⟨Bridge.verificationOwnerRequired, Bridge.observationOwnerRequired,
    Bridge.dispositionOwnerRequired, Bridge.commitOwnerRequired,
    Bridge.runtimeVerificationForbidden, Bridge.nonAuthority.truthForbidden,
    Bridge.nonAuthority.causalForbidden, Bridge.nonAuthority.executionForbidden,
    Bridge.nonAuthority.overwriteForbidden,
    Bridge.lineageNonAuthority.truthForbidden,
    Bridge.lineageNonAuthority.causalForbidden,
    Bridge.lineageNonAuthority.executionForbidden,
    Bridge.lineageNonAuthority.overwriteForbidden,
    Bridge.lineageNonAuthority.automaticLearningForbidden⟩

theorem verification_receipt_digest_is_exact (r : Receipt) :
    r.receiptDigest = Bridge.receiptDigestOf r.source r.exactVerifyCycle
      r.upstreamLineage r.qualification r.sourceBinding
      r.criterionEvidence r.criterion r.falsification r.challenge
      r.corroboration r.adjudication r.debtSemantics r.truthBoundary
      r.qiBoundary r.learningBoundary r.executionBoundary r.singleUse
      r.receiptBoundary r.disposition r.indexBefore r.indexAfter
      r.historyAfter := by
  exact r.receiptDigestExact

end WorldHostEffectVerificationBridge
end
end VerifyOS
end KUOS
