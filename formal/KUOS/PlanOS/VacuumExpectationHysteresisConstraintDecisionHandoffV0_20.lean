import Mathlib
import KUOS.PlanOS.VacuumExpectationHistoryQiCandidateGenerationV0_19
import KUOS.PlanOS.QiConditionedNonMarkovReplanV0_2

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS

structure CandidateAdmissibilityReceipt where
  candidate : ReplanCandidateType
  hysteresis : HysteresisGate
  constraints : ConstraintBoundary
  included : Bool
  gateCandidateExact : hysteresis.candidateType = candidate
  hysteresisExact : constraints.hysteresisPassed = hysteresis.hysteresisPassed
  inclusionExact : included = constraints.admissible

namespace CandidateAdmissibilityReceipt

theorem admissible_of_included
    (r : CandidateAdmissibilityReceipt) (h : r.included = true) :
    r.constraints.admissible = true := by
  calc
    r.constraints.admissible = r.included := r.inclusionExact.symm
    _ = true := h

theorem included_preserves_boundaries
    (r : CandidateAdmissibilityReceipt) (h : r.included = true) :
    r.constraints.missionInvariantsPreserved = true ∧
      r.constraints.authorityBoundaryPreserved = true ∧
      r.constraints.qiTransitionReady = true ∧
      r.hysteresis.hysteresisPassed = true := by
  have ha := r.admissible_of_included h
  have hm := admissible_candidate_preserves_mission_and_authority r.constraints ha
  have hq := admissible_candidate_passes_qi_and_hysteresis r.constraints ha
  refine ⟨hm.1, hm.2, hq.1, ?_⟩
  calc
    r.hysteresis.hysteresisPassed = r.constraints.hysteresisPassed :=
      r.hysteresisExact.symm
    _ = true := hq.2

end CandidateAdmissibilityReceipt

structure DecisionOSAdmissibleSetHandoff where
  generatedSetBound : Bool
  admissibleSetBound : Bool
  primaryForwarded : Bool
  holdForwarded : Bool
  allForwardedAdmissible : Bool
  identitiesPreserved : Bool
  alternativesPreserved : Bool
  dissentVisible : Bool
  minorityPreserved : Bool
  decisionOSOwnsSelection : Bool
  selectionReceiptSupplied : Bool
  selectionPerformed : Bool
  planSynthesisPerformed : Bool
  decisionNotExecution : Bool
  silentSubstitutionDetected : Bool
  handoffCommitted : Bool
  generatedRequired : generatedSetBound = true
  admissibleRequired : admissibleSetBound = true
  holdRequired : holdForwarded = true
  allAdmissibleRequired : allForwardedAdmissible = true
  identitiesRequired : identitiesPreserved = true
  alternativesRequired : alternativesPreserved = true
  dissentRequired : dissentVisible = true
  minorityRequired : minorityPreserved = true
  ownerRequired : decisionOSOwnsSelection = true
  selectionReceiptForbidden : selectionReceiptSupplied = false
  selectionForbidden : selectionPerformed = false
  synthesisForbidden : planSynthesisPerformed = false
  executionForbidden : decisionNotExecution = true
  substitutionForbidden : silentSubstitutionDetected = false
  handoffRequired : handoffCommitted = true

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

structure VacuumExpectationHysteresisConstraintDecisionHandoffBridge where
  Digest : Type
  digestOf :
    VacuumExpectationHistoryQiCandidateGenerationReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge →
    CandidateAdmissibilityReceipt → CandidateAdmissibilityReceipt →
    DecisionOSAdmissibleSetHandoff → ReplanEventIndex → ReplanEventIndex →
    ReplanHistory → Digest
  nonAuthority : ReplanNonAuthority
  constraintOwnerPlanOS : Bool
  selectionOwnerDecisionOS : Bool
  synthesisOwnerPlanOS : Bool
  executionOwnerActOS : Bool
  runtimeSelects : Bool
  runtimeSynthesizes : Bool
  runtimeActivates : Bool
  runtimeExecutes : Bool
  runtimeLicenses : Bool
  runtimeOverwritesMemory : Bool
  runtimeUpdatesWorld : Bool
  constraintOwnerRequired : constraintOwnerPlanOS = true
  selectionOwnerRequired : selectionOwnerDecisionOS = true
  synthesisOwnerRequired : synthesisOwnerPlanOS = true
  executionOwnerRequired : executionOwnerActOS = true
  selectionForbidden : runtimeSelects = false
  synthesisForbidden : runtimeSynthesizes = false
  activationForbidden : runtimeActivates = false
  executionForbidden : runtimeExecutes = false
  licenseForbidden : runtimeLicenses = false
  overwriteForbidden : runtimeOverwritesMemory = false
  worldUpdateForbidden : runtimeUpdatesWorld = false

structure VacuumExpectationHysteresisConstraintDecisionHandoffReceipt
    (Bridge : VacuumExpectationHysteresisConstraintDecisionHandoffBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge) where
  generation : VacuumExpectationHistoryQiCandidateGenerationReceipt
    K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge
  primary : CandidateAdmissibilityReceipt
  hold : CandidateAdmissibilityReceipt
  handoff : DecisionOSAdmissibleSetHandoff
  constrainIndex : ReplanEventIndex
  handoffIndex : ReplanEventIndex
  historyAfter : ReplanHistory
  digest : Bridge.Digest
  sourceBound : Bool
  constrainCommitted : Bool
  handoffCommitted : Bool
  sourceRequired : sourceBound = true
  constrainRequired : constrainCommitted = true
  handoffRequired : handoffCommitted = true
  primaryExact : primary.candidate = generation.primaryCandidate
  holdExact : hold.candidate = generation.holdAlternative
  primaryQiExact : primary.constraints.qiTransitionReady =
    generation.qiBoundary.transitionReadinessVisible
  holdQiExact : hold.constraints.qiTransitionReady =
    generation.qiBoundary.transitionReadinessVisible
  holdExempt : hold.hysteresis.switchExempt = true
  holdIncluded : hold.included = true
  primaryForwardExact : handoff.primaryForwarded = primary.included
  holdForwardExact : handoff.holdForwarded = hold.included
  constrainIndexExact : constrainIndex = generation.generationIndex.append
  handoffIndexExact : handoffIndex = constrainIndex.append
  historyExact : historyAfter.committedRecords =
    generation.historyAfterGeneration.committedRecords + 2
  digestExact : digest = Bridge.digestOf generation primary hold handoff
    constrainIndex handoffIndex historyAfter

namespace VacuumExpectationHysteresisConstraintDecisionHandoffBridge

variable
    {K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge}
    {Bridge : VacuumExpectationHysteresisConstraintDecisionHandoffBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge}

abbrev Receipt := VacuumExpectationHysteresisConstraintDecisionHandoffReceipt
  K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge Bridge

theorem follows_constraint_deliberation_prefix (_r : Receipt) :
    ReplanPhase.generate.next = some ReplanPhase.constrain ∧
      ReplanPhase.constrain.next = some ReplanPhase.deliberate := by
  exact ⟨rfl, rfl⟩

theorem hold_is_admissible_and_forwarded (r : Receipt) :
    r.hold.candidate = .hold ∧ r.hold.constraints.admissible = true ∧
      r.hold.hysteresis.hysteresisPassed = true ∧
      r.handoff.holdForwarded = true := by
  have hc : r.hold.candidate = .hold := by
    calc
      r.hold.candidate = r.generation.holdAlternative := r.holdExact
      _ = .hold := r.generation.holdAlternativeExact
  have ha := r.hold.admissible_of_included r.holdIncluded
  have hg := r.hold.included_preserves_boundaries r.holdIncluded
  have hf : r.handoff.holdForwarded = true := by
    calc
      r.handoff.holdForwarded = r.hold.included := r.holdForwardExact
      _ = true := r.holdIncluded
  exact ⟨hc, ha, hg.2.2.2, hf⟩

theorem included_primary_requires_hysteresis_margin
    (r : Receipt) (hi : r.primary.included = true)
    (hne : r.primary.hysteresis.switchExempt = false) :
    r.primary.hysteresis.baseSwitchThreshold + r.primary.hysteresis.qiHysteresis +
        r.primary.hysteresis.oscillationPenalty +
        r.primary.hysteresis.recoveryProtectionPenalty ≤
      r.primary.hysteresis.switchBenefit := by
  have hp := r.primary.included_preserves_boundaries hi
  exact switching_candidate_requires_hysteresis_margin r.primary.hysteresis hne hp.2.2.2

theorem handoff_preserves_admissible_set (r : Receipt) :
    r.handoff.generatedSetBound = true ∧ r.handoff.admissibleSetBound = true ∧
      r.handoff.holdForwarded = true ∧
      r.handoff.allForwardedAdmissible = true ∧
      r.handoff.alternativesPreserved = true := by
  exact ⟨r.handoff.generatedRequired, r.handoff.admissibleRequired,
    r.handoff.holdRequired, r.handoff.allAdmissibleRequired,
    r.handoff.alternativesRequired⟩

theorem handoff_is_not_selection_or_synthesis (r : Receipt) :
    r.handoff.handoffCommitted = true ∧ r.handoff.decisionOSOwnsSelection = true ∧
      r.handoff.selectionReceiptSupplied = false ∧
      r.handoff.selectionPerformed = false ∧
      r.handoff.planSynthesisPerformed = false ∧
      r.handoff.decisionNotExecution = true := by
  exact ⟨r.handoff.handoffRequired, r.handoff.ownerRequired,
    r.handoff.selectionReceiptForbidden, r.handoff.selectionForbidden,
    r.handoff.synthesisForbidden, r.handoff.executionForbidden⟩

theorem events_append_strictly (r : Receipt) :
    r.generation.generationIndex.current < r.constrainIndex.current ∧
      r.constrainIndex.current < r.handoffIndex.current := by
  constructor
  · rw [r.constrainIndexExact]
    exact replanEventIndex_strict r.generation.generationIndex
  · rw [r.handoffIndexExact]
    exact replanEventIndex_strict r.constrainIndex

theorem history_appends_two_records (r : Receipt) :
    r.historyAfter.committedRecords =
        r.generation.historyAfterGeneration.committedRecords + 2 ∧
      r.historyAfter.snapshotRecords =
        r.generation.historyAfterGeneration.committedRecords + 2 := by
  refine ⟨r.historyExact, ?_⟩
  rw [replanHistory_snapshot_matches_commits r.historyAfter]
  exact r.historyExact

theorem preserves_identity_dissent_and_minority (r : Receipt) :
    r.handoff.identitiesPreserved = true ∧ r.handoff.dissentVisible = true ∧
      r.handoff.minorityPreserved = true ∧
      r.handoff.silentSubstitutionDetected = false := by
  exact ⟨r.handoff.identitiesRequired, r.handoff.dissentRequired,
    r.handoff.minorityRequired, r.handoff.substitutionForbidden⟩

theorem bridge_grants_no_new_authority (_r : Receipt) :
    Bridge.constraintOwnerPlanOS = true ∧ Bridge.selectionOwnerDecisionOS = true ∧
      Bridge.synthesisOwnerPlanOS = true ∧ Bridge.executionOwnerActOS = true ∧
      Bridge.runtimeSelects = false ∧ Bridge.runtimeSynthesizes = false ∧
      Bridge.runtimeActivates = false ∧ Bridge.runtimeExecutes = false ∧
      Bridge.runtimeLicenses = false ∧ Bridge.runtimeOverwritesMemory = false ∧
      Bridge.runtimeUpdatesWorld = false ∧
      Bridge.nonAuthority.truthAuthority = false ∧
      Bridge.nonAuthority.causalAuthority = false ∧
      Bridge.nonAuthority.executionAuthority = false := by
  exact ⟨Bridge.constraintOwnerRequired, Bridge.selectionOwnerRequired,
    Bridge.synthesisOwnerRequired, Bridge.executionOwnerRequired,
    Bridge.selectionForbidden, Bridge.synthesisForbidden,
    Bridge.activationForbidden, Bridge.executionForbidden,
    Bridge.licenseForbidden, Bridge.overwriteForbidden,
    Bridge.worldUpdateForbidden, Bridge.nonAuthority.truthForbidden,
    Bridge.nonAuthority.causalForbidden, Bridge.nonAuthority.executionForbidden⟩

theorem digest_is_exact (r : Receipt) :
    r.digest = Bridge.digestOf r.generation r.primary r.hold r.handoff
      r.constrainIndex r.handoffIndex r.historyAfter := by
  exact r.digestExact

end VacuumExpectationHysteresisConstraintDecisionHandoffBridge
end
end PlanOS
end KUOS
