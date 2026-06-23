import Mathlib
import KUOS.PlanOS.VacuumExpectationLearningReplanIntakeV0_18
import KUOS.PlanOS.QiConditionedNonMarkovReplanV0_2

/-!
PlanOS v0.19: read-only history, Qi conditioning, and candidate generation
for the WORLD-derived LearnOS v0.3 replan path.

The module advances only the deterministic phase prefix

  bind → history → qiCondition → generate

and generates one primary candidate plus an explicit hold alternative.
It does not constrain, select, synthesize, activate, execute, license,
overwrite memory, or update WORLD.
-/

namespace KUOS
namespace PlanOS

open WORLD
open ObserveOS
open VerifyOS
open LearnOS
open KUOS.LearnOS.VacuumExpectationVerificationLearningBridge


def replanCandidateOfLearningKind : LearningKind → ReplanCandidateType
  | .reinforcement => .strengthen
  | .repair => .repair
  | .reobservation => .reobserve
  | .hold => .hold


structure VacuumExpectationHistoryQiCandidateGenerationBridge
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
    (VerifyBridge :
      VacuumExpectationCommitVerificationBridge K O Intake ObserveBridge)
    (LearnBridge :
      VacuumExpectationVerificationLearningBridge
        K O Intake ObserveBridge VerifyBridge)
    (ReplanBridge : VacuumExpectationLearningReplanIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge) where
  GenerationDigest : Type
  digestOf :
    VacuumExpectationLearningReplanIntakeReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge →
      NonMarkovHistoryBoundary →
      QiReplanBoundary →
      ReplanCandidateType →
      ReplanCandidateType →
      ReplanEventIndex →
      ReplanEventIndex →
      ReplanEventIndex →
      ReplanHistory →
      GenerationDigest
  replanNonAuthority : ReplanNonAuthority
  candidateGenerationOwnedByPlanOS : Bool
  candidateSelectionOwnedByDecisionOS : Bool
  planSynthesisOwnedByPlanOS : Bool
  executionOwnedByActOS : Bool
  bridgeRuntimeSelectsCandidate : Bool
  bridgeRuntimeSynthesizesPlan : Bool
  bridgeRuntimeActivatesReplan : Bool
  bridgeRuntimeActivatesPlan : Bool
  bridgeRuntimePermitsExecution : Bool
  bridgeRuntimeGrantsHostLicense : Bool
  bridgeRuntimeOverwritesMemory : Bool
  bridgeRuntimeUpdatesWORLD : Bool
  generationOwnershipRequired : candidateGenerationOwnedByPlanOS = true
  selectionOwnershipRequired : candidateSelectionOwnedByDecisionOS = true
  synthesisOwnershipRequired : planSynthesisOwnedByPlanOS = true
  executionOwnershipRequired : executionOwnedByActOS = true
  selectionForbidden : bridgeRuntimeSelectsCandidate = false
  synthesisForbidden : bridgeRuntimeSynthesizesPlan = false
  replanActivationForbidden : bridgeRuntimeActivatesReplan = false
  planActivationForbidden : bridgeRuntimeActivatesPlan = false
  executionForbidden : bridgeRuntimePermitsExecution = false
  hostLicenseForbidden : bridgeRuntimeGrantsHostLicense = false
  memoryOverwriteForbidden : bridgeRuntimeOverwritesMemory = false
  worldUpdateForbidden : bridgeRuntimeUpdatesWORLD = false


structure VacuumExpectationHistoryQiCandidateGenerationReceipt
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
    (VerifyBridge :
      VacuumExpectationCommitVerificationBridge K O Intake ObserveBridge)
    (LearnBridge :
      VacuumExpectationVerificationLearningBridge
        K O Intake ObserveBridge VerifyBridge)
    (ReplanBridge : VacuumExpectationLearningReplanIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge)
    (GenerationBridge : VacuumExpectationHistoryQiCandidateGenerationBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge) where
  intake : VacuumExpectationLearningReplanIntakeReceipt
    K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
  historyBoundary : NonMarkovHistoryBoundary
  qiBoundary : QiReplanBoundary
  primaryCandidate : ReplanCandidateType
  holdAlternative : ReplanCandidateType
  historyIndex : ReplanEventIndex
  qiIndex : ReplanEventIndex
  generationIndex : ReplanEventIndex
  historyAfterGeneration : ReplanHistory
  generationDigest : GenerationBridge.GenerationDigest
  sourceIntakeBound : Bool
  historyPhaseCommitted : Bool
  qiPhaseCommitted : Bool
  generationPhaseCommitted : Bool
  sourceRequired : sourceIntakeBound = true
  historyCommitRequired : historyPhaseCommitted = true
  qiCommitRequired : qiPhaseCommitted = true
  generationCommitRequired : generationPhaseCommitted = true
  sourceIntakeCommitted : intake.intakeCommitted = true
  sourceBindCommitted : intake.bindCommitted = true
  sourceFutureOnly : intake.learning.delta.futureOnly = true
  sourceInactiveNow : intake.learning.delta.activeNow = false
  primaryCandidateExact :
    primaryCandidate =
      replanCandidateOfLearningKind intake.learning.compatibility.kind
  holdAlternativeExact : holdAlternative = .hold
  historyIndexExact : historyIndex = intake.indexAfter.append
  qiIndexExact : qiIndex = historyIndex.append
  generationIndexExact : generationIndex = qiIndex.append
  historyAppendExact :
    historyAfterGeneration.committedRecords =
      intake.historyAfter.committedRecords + 3
  generationDigestExact :
    generationDigest = GenerationBridge.digestOf intake historyBoundary
      qiBoundary primaryCandidate holdAlternative historyIndex qiIndex
      generationIndex historyAfterGeneration


namespace VacuumExpectationHistoryQiCandidateGenerationBridge

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
    {K : WorldKuuVacuumOSHilbertCompletionBridge Mix}
    {O : WorldVacuumExpectationObservationBridge K}
    {Intake : WorldVacuumExpectationObserveOSEvidenceIntakeBridge K O}
    {ObserveBridge : VacuumExpectationIntakeCommitBridge K O Intake}
    {VerifyBridge :
      VacuumExpectationCommitVerificationBridge K O Intake ObserveBridge}
    {LearnBridge :
      VacuumExpectationVerificationLearningBridge
        K O Intake ObserveBridge VerifyBridge}
    {ReplanBridge : VacuumExpectationLearningReplanIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge}
    {GenerationBridge : VacuumExpectationHistoryQiCandidateGenerationBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge}


theorem generation_requires_exact_planos_intake
    (receipt : VacuumExpectationHistoryQiCandidateGenerationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge) :
    receipt.sourceIntakeBound = true ∧
      receipt.intake.intakeCommitted = true ∧
      receipt.intake.bindCommitted = true ∧
      receipt.intake.learning.delta.futureOnly = true ∧
      receipt.intake.learning.delta.activeNow = false := by
  exact ⟨receipt.sourceRequired,
    receipt.sourceIntakeCommitted,
    receipt.sourceBindCommitted,
    receipt.sourceFutureOnly,
    receipt.sourceInactiveNow⟩


theorem generation_follows_deterministic_phase_prefix
    (_receipt : VacuumExpectationHistoryQiCandidateGenerationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge) :
    ReplanPhase.bind.next = some ReplanPhase.history ∧
      ReplanPhase.history.next = some ReplanPhase.qiCondition ∧
      ReplanPhase.qiCondition.next = some ReplanPhase.generate := by
  exact ⟨rfl, rfl, rfl⟩


theorem generation_phase_events_append_strictly
    (receipt : VacuumExpectationHistoryQiCandidateGenerationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge) :
    receipt.intake.indexAfter.current < receipt.historyIndex.current ∧
      receipt.historyIndex.current < receipt.qiIndex.current ∧
      receipt.qiIndex.current < receipt.generationIndex.current := by
  constructor
  · rw [receipt.historyIndexExact]
    exact replanEventIndex_strict receipt.intake.indexAfter
  constructor
  · rw [receipt.qiIndexExact]
    exact replanEventIndex_strict receipt.historyIndex
  · rw [receipt.generationIndexExact]
    exact replanEventIndex_strict receipt.qiIndex


theorem generation_history_is_nonmarkov_and_read_only
    (receipt : VacuumExpectationHistoryQiCandidateGenerationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge) :
    receipt.historyBoundary.previousPlanChangesVisible = true ∧
      receipt.historyBoundary.failedTransitionsVisible = true ∧
      receipt.historyBoundary.oscillationHistoryVisible = true ∧
      receipt.historyBoundary.recoveryHistoryVisible = true ∧
      receipt.historyBoundary.stagnationHistoryVisible = true ∧
      receipt.historyBoundary.pathDependenceVisible = true ∧
      receipt.historyBoundary.sourceHistoryMutation = false := by
  exact ⟨receipt.historyBoundary.changesRequired,
    receipt.historyBoundary.failureRequired,
    receipt.historyBoundary.oscillationRequired,
    receipt.historyBoundary.recoveryRequired,
    receipt.historyBoundary.stagnationRequired,
    receipt.historyBoundary.pathRequired,
    receipt.historyBoundary.mutationForbidden⟩


theorem generation_qi_is_context_without_authority
    (receipt : VacuumExpectationHistoryQiCandidateGenerationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge) :
    receipt.qiBoundary.processTensorBound = true ∧
      receipt.qiBoundary.processHistoryBound = true ∧
      receipt.qiBoundary.transitionReadinessVisible = true ∧
      receipt.qiBoundary.hysteresisVisible = true ∧
      receipt.qiBoundary.qiContextOnly = true ∧
      receipt.qiBoundary.qiTruthAuthority = false ∧
      receipt.qiBoundary.qiCausalAuthority = false ∧
      receipt.qiBoundary.qiExecutionAuthority = false ∧
      receipt.qiBoundary.qiClinicalAuthority = false ∧
      receipt.qiBoundary.qiActivatesPlan = false := by
  exact ⟨receipt.qiBoundary.tensorRequired,
    receipt.qiBoundary.historyRequired,
    receipt.qiBoundary.transitionRequired,
    receipt.qiBoundary.hysteresisRequired,
    receipt.qiBoundary.contextRequired,
    receipt.qiBoundary.truthForbidden,
    receipt.qiBoundary.causalForbidden,
    receipt.qiBoundary.executionForbidden,
    receipt.qiBoundary.clinicalForbidden,
    receipt.qiBoundary.activationForbidden⟩


theorem passed_verification_generates_strengthen_or_hold
    (receipt : VacuumExpectationHistoryQiCandidateGenerationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge)
    (hpassed :
      receipt.intake.learning.verification.adjudication.verdict = .passed) :
    receipt.primaryCandidate = .strengthen ∨
      receipt.primaryCandidate = .hold := by
  have hkind := passed_verification_yields_reinforcement_or_hold
    receipt.intake.learning hpassed
  rcases hkind with hreinforcement | hhold
  · left
    calc
      receipt.primaryCandidate =
          replanCandidateOfLearningKind
            receipt.intake.learning.compatibility.kind :=
        receipt.primaryCandidateExact
      _ = .strengthen := by rw [hreinforcement]; rfl
  · right
    calc
      receipt.primaryCandidate =
          replanCandidateOfLearningKind
            receipt.intake.learning.compatibility.kind :=
        receipt.primaryCandidateExact
      _ = .hold := by rw [hhold]; rfl


theorem failed_verification_generates_repair_or_hold
    (receipt : VacuumExpectationHistoryQiCandidateGenerationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge)
    (hfailed :
      receipt.intake.learning.verification.adjudication.verdict = .failed) :
    receipt.primaryCandidate = .repair ∨
      receipt.primaryCandidate = .hold := by
  have hkind := failed_verification_yields_repair_or_hold
    receipt.intake.learning hfailed
  rcases hkind with hrepair | hhold
  · left
    calc
      receipt.primaryCandidate =
          replanCandidateOfLearningKind
            receipt.intake.learning.compatibility.kind :=
        receipt.primaryCandidateExact
      _ = .repair := by rw [hrepair]; rfl
  · right
    calc
      receipt.primaryCandidate =
          replanCandidateOfLearningKind
            receipt.intake.learning.compatibility.kind :=
        receipt.primaryCandidateExact
      _ = .hold := by rw [hhold]; rfl


theorem indeterminate_verification_generates_reobserve_or_hold
    (receipt : VacuumExpectationHistoryQiCandidateGenerationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge)
    (hindeterminate :
      receipt.intake.learning.verification.adjudication.verdict =
        .indeterminate) :
    receipt.primaryCandidate = .reobserve ∨
      receipt.primaryCandidate = .hold := by
  have hkind := indeterminate_verification_yields_reobservation_or_hold
    receipt.intake.learning hindeterminate
  rcases hkind with hreobserve | hhold
  · left
    calc
      receipt.primaryCandidate =
          replanCandidateOfLearningKind
            receipt.intake.learning.compatibility.kind :=
        receipt.primaryCandidateExact
      _ = .reobserve := by rw [hreobserve]; rfl
  · right
    calc
      receipt.primaryCandidate =
          replanCandidateOfLearningKind
            receipt.intake.learning.compatibility.kind :=
        receipt.primaryCandidateExact
      _ = .hold := by rw [hhold]; rfl


theorem generation_preserves_explicit_hold_alternative
    (receipt : VacuumExpectationHistoryQiCandidateGenerationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge) :
    receipt.holdAlternative = .hold := by
  exact receipt.holdAlternativeExact


theorem generation_history_appends_three_phase_records
    (receipt : VacuumExpectationHistoryQiCandidateGenerationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge) :
    receipt.historyAfterGeneration.committedRecords =
        receipt.intake.historyAfter.committedRecords + 3 ∧
      receipt.historyAfterGeneration.snapshotRecords =
        receipt.intake.historyAfter.committedRecords + 3 := by
  refine ⟨receipt.historyAppendExact, ?_⟩
  rw [replanHistory_snapshot_matches_commits receipt.historyAfterGeneration]
  exact receipt.historyAppendExact


theorem generation_commit_is_not_selection_synthesis_or_activation
    (receipt : VacuumExpectationHistoryQiCandidateGenerationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge) :
    receipt.historyPhaseCommitted = true ∧
      receipt.qiPhaseCommitted = true ∧
      receipt.generationPhaseCommitted = true ∧
      GenerationBridge.bridgeRuntimeSelectsCandidate = false ∧
      GenerationBridge.bridgeRuntimeSynthesizesPlan = false ∧
      GenerationBridge.bridgeRuntimeActivatesReplan = false ∧
      GenerationBridge.bridgeRuntimeActivatesPlan = false ∧
      GenerationBridge.bridgeRuntimePermitsExecution = false := by
  exact ⟨receipt.historyCommitRequired,
    receipt.qiCommitRequired,
    receipt.generationCommitRequired,
    GenerationBridge.selectionForbidden,
    GenerationBridge.synthesisForbidden,
    GenerationBridge.replanActivationForbidden,
    GenerationBridge.planActivationForbidden,
    GenerationBridge.executionForbidden⟩


theorem generation_preserves_os_ownership
    (_receipt : VacuumExpectationHistoryQiCandidateGenerationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge) :
    GenerationBridge.candidateGenerationOwnedByPlanOS = true ∧
      GenerationBridge.candidateSelectionOwnedByDecisionOS = true ∧
      GenerationBridge.planSynthesisOwnedByPlanOS = true ∧
      GenerationBridge.executionOwnedByActOS = true := by
  exact ⟨GenerationBridge.generationOwnershipRequired,
    GenerationBridge.selectionOwnershipRequired,
    GenerationBridge.synthesisOwnershipRequired,
    GenerationBridge.executionOwnershipRequired⟩


theorem generation_bridge_grants_no_new_authority
    (_receipt : VacuumExpectationHistoryQiCandidateGenerationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge) :
    GenerationBridge.bridgeRuntimeGrantsHostLicense = false ∧
      GenerationBridge.bridgeRuntimeOverwritesMemory = false ∧
      GenerationBridge.bridgeRuntimeUpdatesWORLD = false ∧
      GenerationBridge.replanNonAuthority.truthAuthority = false ∧
      GenerationBridge.replanNonAuthority.causalAuthority = false ∧
      GenerationBridge.replanNonAuthority.executionAuthority = false ∧
      GenerationBridge.replanNonAuthority.finalCommitmentAuthority = false ∧
      GenerationBridge.replanNonAuthority.memoryOverwriteAuthority = false ∧
      GenerationBridge.replanNonAuthority.selfModificationAuthority = false := by
  exact ⟨GenerationBridge.hostLicenseForbidden,
    GenerationBridge.memoryOverwriteForbidden,
    GenerationBridge.worldUpdateForbidden,
    GenerationBridge.replanNonAuthority.truthForbidden,
    GenerationBridge.replanNonAuthority.causalForbidden,
    GenerationBridge.replanNonAuthority.executionForbidden,
    GenerationBridge.replanNonAuthority.finalForbidden,
    GenerationBridge.replanNonAuthority.overwriteForbidden,
    GenerationBridge.replanNonAuthority.selfModificationForbidden⟩


theorem generation_digest_is_exact
    (receipt : VacuumExpectationHistoryQiCandidateGenerationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge) :
    receipt.generationDigest =
      GenerationBridge.digestOf receipt.intake receipt.historyBoundary
        receipt.qiBoundary receipt.primaryCandidate receipt.holdAlternative
        receipt.historyIndex receipt.qiIndex receipt.generationIndex
        receipt.historyAfterGeneration := by
  exact receipt.generationDigestExact


theorem generated_candidate_value_remains_exact
    (receipt : VacuumExpectationHistoryQiCandidateGenerationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge) :
    receipt.intake.learning.verification.observeCommit.envelope.candidate.value =
      K.vacuumState
        receipt.intake.learning.verification.observeCommit.envelope.candidate.observable := by
  exact learned_candidate_value_remains_exact receipt.intake.learning

end VacuumExpectationHistoryQiCandidateGenerationBridge
end PlanOS
end KUOS
