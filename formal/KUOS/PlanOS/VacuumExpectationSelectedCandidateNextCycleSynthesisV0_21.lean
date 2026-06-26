import Mathlib
import KUOS.DecisionOS.VacuumExpectationAdmissibleCandidateSelectionV0_4
import KUOS.PlanOS.QiConditionedNonMarkovReplanV0_2

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS

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

structure VacuumExpectationSelectedCandidateNextCycleSynthesisBridge where
  Digest : Type
  digestOf :
    VacuumExpectationAdmissibleCandidateSelectionReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge →
    ReplanCandidateType → NextCycleSynthesis → ReplanCommitBoundary →
    ReplanEventIndex → ReplanEventIndex → ReplanHistory → Digest
  nonAuthority : ReplanNonAuthority
  synthesisOwnedByPlanOS : Bool
  selectionOwnedByDecisionOS : Bool
  executionOwnedByActOS : Bool
  runtimeActivatesPlan : Bool
  runtimeExecutes : Bool
  runtimeGrantsHostLicense : Bool
  runtimeOverwritesMemory : Bool
  runtimeUpdatesWorld : Bool
  synthesisOwnerRequired : synthesisOwnedByPlanOS = true
  selectionOwnerRequired : selectionOwnedByDecisionOS = true
  executionOwnerRequired : executionOwnedByActOS = true
  activationForbidden : runtimeActivatesPlan = false
  executionForbidden : runtimeExecutes = false
  licenseForbidden : runtimeGrantsHostLicense = false
  overwriteForbidden : runtimeOverwritesMemory = false
  worldUpdateForbidden : runtimeUpdatesWorld = false

structure VacuumExpectationSelectedCandidateNextCycleSynthesisReceipt
    (Bridge : VacuumExpectationSelectedCandidateNextCycleSynthesisBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge) where
  selection : VacuumExpectationAdmissibleCandidateSelectionReceipt
    K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge
  selectedCandidate : ReplanCandidateType
  synthesis : NextCycleSynthesis
  commitBoundary : ReplanCommitBoundary
  synthesisIndex : ReplanEventIndex
  commitIndex : ReplanEventIndex
  historyAfter : ReplanHistory
  digest : Bridge.Digest
  sourceBound : Bool
  synthesisCommitted : Bool
  nextPlanBasisCommitted : Bool
  sourceRequired : sourceBound = true
  synthesisRequired : synthesisCommitted = true
  basisRequired : nextPlanBasisCommitted = true
  sourceSelectionPerformed : selection.selectionPerformed = true
  selectedCandidateExact : selectedCandidate = selection.selectedCandidate
  synthesisSelectedExact : synthesis.selectedCandidateBound = true
  synthesisDecisionExact : synthesis.decisionReceiptBound = true
  synthesisHistoryExact : synthesis.historyBound = true
  synthesisQiExact : synthesis.qiConditionBound = true
  synthesisLearningExact : synthesis.learningDeltaBound = true
  synthesisMissionExact : synthesis.missionContractBound = true
  commitBasisExact : commitBoundary.nextPlanBasisCommitted = nextPlanBasisCommitted
  synthesisIndexExact :
    synthesisIndex = selection.source.handoffIndex.append
  commitIndexExact : commitIndex = synthesisIndex.append
  historyExact : historyAfter.committedRecords =
    selection.source.historyAfter.committedRecords + 2
  digestExact : digest = Bridge.digestOf selection selectedCandidate synthesis
    commitBoundary synthesisIndex commitIndex historyAfter

namespace VacuumExpectationSelectedCandidateNextCycleSynthesisBridge

variable
    {Bridge : VacuumExpectationSelectedCandidateNextCycleSynthesisBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge}

theorem synthesis_requires_exact_decision_selection
    (r : VacuumExpectationSelectedCandidateNextCycleSynthesisReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge Bridge) :
    r.sourceBound = true ∧ r.selection.selectionPerformed = true ∧
      r.selectedCandidate = r.selection.selectedCandidate ∧
      r.synthesis.selectedCandidateBound = true ∧
      r.synthesis.decisionReceiptBound = true := by
  exact ⟨r.sourceRequired, r.sourceSelectionPerformed, r.selectedCandidateExact,
    r.synthesisSelectedExact, r.synthesisDecisionExact⟩

theorem synthesis_binds_history_qi_learning_and_mission
    (r : VacuumExpectationSelectedCandidateNextCycleSynthesisReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge Bridge) :
    r.synthesis.historyBound = true ∧ r.synthesis.qiConditionBound = true ∧
      r.synthesis.learningDeltaBound = true ∧
      r.synthesis.missionContractBound = true := by
  exact ⟨r.synthesisHistoryExact, r.synthesisQiExact,
    r.synthesisLearningExact, r.synthesisMissionExact⟩

theorem synthesis_starts_exactly_next_cycle
    (r : VacuumExpectationSelectedCandidateNextCycleSynthesisReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge Bridge) :
    r.synthesis.activeFromCycle = r.synthesis.currentCycle + 1 := by
  exact r.synthesis.nextCycleRequired

theorem synthesis_is_future_only_and_inactive
    (r : VacuumExpectationSelectedCandidateNextCycleSynthesisReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge Bridge) :
    r.synthesis.futureOnly = true ∧ r.synthesis.activeNow = false ∧
      r.synthesis.currentCycleUnchanged = true ∧
      r.synthesis.pastPlanUnchanged = true := by
  exact ⟨r.synthesis.futureRequired, r.synthesis.activationForbidden,
    r.synthesis.currentRequired, r.synthesis.pastRequired⟩

theorem synthesis_commit_requires_next_plan_phase
    (r : VacuumExpectationSelectedCandidateNextCycleSynthesisReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge Bridge) :
    r.synthesisCommitted = true ∧ r.nextPlanBasisCommitted = true ∧
      r.commitBoundary.nextPlanBasisCommitted = true ∧
      r.commitBoundary.nextPlanPhaseRequired = true := by
  have hbasis : r.commitBoundary.nextPlanBasisCommitted = true := by
    calc
      r.commitBoundary.nextPlanBasisCommitted = r.nextPlanBasisCommitted :=
        r.commitBasisExact
      _ = true := r.basisRequired
  exact ⟨r.synthesisRequired, r.basisRequired, hbasis,
    r.commitBoundary.nextPlanRequired⟩

theorem synthesis_commit_does_not_activate_execute_or_license
    (r : VacuumExpectationSelectedCandidateNextCycleSynthesisReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge Bridge) :
    r.synthesis.planNotExecution = true ∧
      r.synthesis.hostLicenseGranted = false ∧
      r.commitBoundary.activeNow = false ∧
      r.commitBoundary.memoryOverwrite = false ∧
      r.commitBoundary.hostLicenseGranted = false := by
  exact ⟨r.synthesis.executionForbidden, r.synthesis.licenseForbidden,
    r.commitBoundary.activationForbidden, r.commitBoundary.overwriteForbidden,
    r.commitBoundary.licenseForbidden⟩

theorem synthesis_events_append_strictly
    (r : VacuumExpectationSelectedCandidateNextCycleSynthesisReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge Bridge) :
    r.selection.source.handoffIndex.current < r.synthesisIndex.current ∧
      r.synthesisIndex.current < r.commitIndex.current := by
  constructor
  · rw [r.synthesisIndexExact]
    exact replanEventIndex_strict r.selection.source.handoffIndex
  · rw [r.commitIndexExact]
    exact replanEventIndex_strict r.synthesisIndex

theorem synthesis_history_appends_two_records
    (r : VacuumExpectationSelectedCandidateNextCycleSynthesisReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge Bridge) :
    r.historyAfter.committedRecords =
        r.selection.source.historyAfter.committedRecords + 2 ∧
      r.historyAfter.snapshotRecords =
        r.selection.source.historyAfter.committedRecords + 2 := by
  refine ⟨r.historyExact, ?_⟩
  rw [replanHistory_snapshot_matches_commits r.historyAfter]
  exact r.historyExact

theorem synthesis_bridge_preserves_ownership
    (_r : VacuumExpectationSelectedCandidateNextCycleSynthesisReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge Bridge) :
    Bridge.synthesisOwnedByPlanOS = true ∧
      Bridge.selectionOwnedByDecisionOS = true ∧
      Bridge.executionOwnedByActOS = true := by
  exact ⟨Bridge.synthesisOwnerRequired, Bridge.selectionOwnerRequired,
    Bridge.executionOwnerRequired⟩

theorem synthesis_bridge_grants_no_downstream_authority
    (_r : VacuumExpectationSelectedCandidateNextCycleSynthesisReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge Bridge) :
    Bridge.runtimeActivatesPlan = false ∧ Bridge.runtimeExecutes = false ∧
      Bridge.runtimeGrantsHostLicense = false ∧
      Bridge.runtimeOverwritesMemory = false ∧ Bridge.runtimeUpdatesWorld = false ∧
      Bridge.nonAuthority.truthAuthority = false ∧
      Bridge.nonAuthority.causalAuthority = false ∧
      Bridge.nonAuthority.executionAuthority = false ∧
      Bridge.nonAuthority.finalCommitmentAuthority = false := by
  exact ⟨Bridge.activationForbidden, Bridge.executionForbidden,
    Bridge.licenseForbidden, Bridge.overwriteForbidden,
    Bridge.worldUpdateForbidden, Bridge.nonAuthority.truthForbidden,
    Bridge.nonAuthority.causalForbidden, Bridge.nonAuthority.executionForbidden,
    Bridge.nonAuthority.finalForbidden⟩

theorem synthesis_digest_is_exact
    (r : VacuumExpectationSelectedCandidateNextCycleSynthesisReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge Bridge) :
    r.digest = Bridge.digestOf r.selection r.selectedCandidate r.synthesis
      r.commitBoundary r.synthesisIndex r.commitIndex r.historyAfter := by
  exact r.digestExact

end VacuumExpectationSelectedCandidateNextCycleSynthesisBridge
end
end PlanOS
end KUOS
