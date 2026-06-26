import Mathlib
import KUOS.PlanOS.VacuumExpectationSelectedCandidateNextCycleSynthesisV0_21
import KUOS.PlanOS.NextCycleBasisCompilerAdapterV0_3

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS


def compilerRouteOfCandidate : ReplanCandidateType → ReplanAdapterRoute
  | .continuePlan => .nextPlanCandidate
  | .strengthen => .nextPlanCandidate
  | .repair => .repairPlanCandidate
  | .slowDown => .repairPlanCandidate
  | .reobserve => .reobservationPlanCandidate
  | .reroute => .reroutePlanCandidate
  | .hold => .hold
  | .terminateCandidate => .terminationPlanCandidate


theorem hold_candidate_compiler_route :
    compilerRouteOfCandidate .hold = .hold := by
  rfl


theorem termination_candidate_compiler_route :
    compilerRouteOfCandidate .terminateCandidate = .terminationPlanCandidate := by
  rfl


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


structure VacuumExpectationCompilerMaterializationBridge where
  Digest : Type
  digestOf :
    VacuumExpectationSelectedCandidateNextCycleSynthesisReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge →
    ReplanAdapterRoute → AdapterRoute → ExactNextCycleGate →
    DualLineageBoundary → DigestBindingBoundary → MaterializationBoundary →
    HoldMaterializationBoundary → CompilerReuseBoundary → SingleUseBoundary →
    ReplanEventIndex → ReplanEventIndex → AdapterHistory → Digest
  nonAuthority : AdapterNonAuthority
  materializationOwnedByPlanOS : Bool
  executionOwnedByActOS : Bool
  runtimeActivatesPlan : Bool
  runtimeExecutes : Bool
  runtimeGrantsHostLicense : Bool
  runtimeOverwritesMemory : Bool
  runtimeUpdatesWorld : Bool
  materializationOwnerRequired : materializationOwnedByPlanOS = true
  executionOwnerRequired : executionOwnedByActOS = true
  activationForbidden : runtimeActivatesPlan = false
  executionForbidden : runtimeExecutes = false
  licenseForbidden : runtimeGrantsHostLicense = false
  overwriteForbidden : runtimeOverwritesMemory = false
  worldUpdateForbidden : runtimeUpdatesWorld = false


structure VacuumExpectationCompilerMaterializationReceipt
    (Bridge : VacuumExpectationCompilerMaterializationBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge) where
  source : VacuumExpectationSelectedCandidateNextCycleSynthesisReceipt
    K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
  route : ReplanAdapterRoute
  projectedRoute : AdapterRoute
  exactNextCycle : ExactNextCycleGate
  dualLineage : DualLineageBoundary
  digestBinding : DigestBindingBoundary
  materialization : MaterializationBoundary
  holdMaterialization : HoldMaterializationBoundary
  compilerReuse : CompilerReuseBoundary
  singleUse : SingleUseBoundary
  materializationIndex : ReplanEventIndex
  receiptIndex : ReplanEventIndex
  historyAfter : AdapterHistory
  digest : Bridge.Digest
  sourceBound : Bool
  materializationCommitted : Bool
  sourceRequired : sourceBound = true
  materializationRequired : materializationCommitted = true
  sourceBasisCommitted : source.nextPlanBasisCommitted = true
  routeExact : route = compilerRouteOfCandidate source.selectedCandidate
  projectionExact : projectedRoute = route.project
  previousCycleExact : exactNextCycle.previousCycle = source.synthesis.currentCycle
  activeCycleExact : exactNextCycle.activeFromCycle = source.synthesis.activeFromCycle
  selectedIdentityPreserved : materialization.selectedCandidatePreserved = true
  holdZeroExecutable : source.selectedCandidate = .hold →
    holdMaterialization.executableStepCount = 0
  holdWithheldVisible : source.selectedCandidate = .hold →
    holdMaterialization.withheldTemplateCount = holdMaterialization.expectedTemplateCount
  materializationIndexExact : materializationIndex = source.commitIndex.append
  receiptIndexExact : receiptIndex = materializationIndex.append
  historyExact : historyAfter.committedRecords = source.historyAfter.committedRecords + 2
  digestExact : digest = Bridge.digestOf source route projectedRoute exactNextCycle
    dualLineage digestBinding materialization holdMaterialization compilerReuse
    singleUse materializationIndex receiptIndex historyAfter


namespace VacuumExpectationCompilerMaterializationBridge

variable
    {Bridge : VacuumExpectationCompilerMaterializationBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge}

local notation "Receipt" =>
  VacuumExpectationCompilerMaterializationReceipt
    K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge Bridge


theorem materialization_requires_committed_next_plan_basis (r : Receipt) :
    r.sourceBound = true ∧ r.source.nextPlanBasisCommitted = true ∧
      r.materializationCommitted = true := by
  exact ⟨r.sourceRequired, r.sourceBasisCommitted, r.materializationRequired⟩


theorem compiler_route_is_exact_and_projected (r : Receipt) :
    r.route = compilerRouteOfCandidate r.source.selectedCandidate ∧
      r.projectedRoute = r.route.project := by
  exact ⟨r.routeExact, r.projectionExact⟩


theorem hold_selection_projects_to_hold
    (r : Receipt) (hhold : r.source.selectedCandidate = .hold) :
    r.route = .hold ∧ r.projectedRoute = .hold := by
  have hroute : r.route = .hold := by
    calc
      r.route = compilerRouteOfCandidate r.source.selectedCandidate := r.routeExact
      _ = compilerRouteOfCandidate .hold := by rw [hhold]
      _ = .hold := hold_candidate_compiler_route
  have hprojected : r.projectedRoute = .hold := by
    calc
      r.projectedRoute = r.route.project := r.projectionExact
      _ = ReplanAdapterRoute.hold.project := by rw [hroute]
      _ = .hold := hold_projects_to_hold
  exact ⟨hroute, hprojected⟩


theorem termination_selection_projects_to_handover
    (r : Receipt) (htermination : r.source.selectedCandidate = .terminateCandidate) :
    r.route = .terminationPlanCandidate ∧
      r.projectedRoute = .handoverPlan := by
  have hroute : r.route = .terminationPlanCandidate := by
    calc
      r.route = compilerRouteOfCandidate r.source.selectedCandidate := r.routeExact
      _ = compilerRouteOfCandidate .terminateCandidate := by rw [htermination]
      _ = .terminationPlanCandidate := termination_candidate_compiler_route
  have hprojected : r.projectedRoute = .handoverPlan := by
    calc
      r.projectedRoute = r.route.project := r.projectionExact
      _ = ReplanAdapterRoute.terminationPlanCandidate.project := by rw [hroute]
      _ = .handoverPlan := termination_projects_to_handover
  exact ⟨hroute, hprojected⟩


theorem exact_next_cycle_gate_matches_synthesis (r : Receipt) :
    r.exactNextCycle.missionCycle = r.source.synthesis.currentCycle + 1 ∧
      r.exactNextCycle.missionPhaseIsPlan = true := by
  constructor
  · calc
      r.exactNextCycle.missionCycle = r.exactNextCycle.previousCycle + 1 :=
        adapter_activates_in_exact_next_cycle r.exactNextCycle
      _ = r.source.synthesis.currentCycle + 1 := by rw [r.previousCycleExact]
  · exact adapter_requires_plan_phase r.exactNextCycle


theorem exact_next_cycle_gate_uses_source_active_cycle (r : Receipt) :
    r.exactNextCycle.activeFromCycle = r.source.synthesis.currentCycle + 1 := by
  calc
    r.exactNextCycle.activeFromCycle = r.source.synthesis.activeFromCycle :=
      r.activeCycleExact
    _ = r.source.synthesis.currentCycle + 1 := r.source.synthesis.nextCycleRequired


theorem compiler_reuses_v01_and_all_guards (r : Receipt) :
    r.compilerReuse.structuredCompilerIsV01 = true ∧
      r.compilerReuse.dependencyValidationReused = true ∧
      r.compilerReuse.resourceValidationReused = true ∧
      r.compilerReuse.effectGuardReused = true ∧
      r.compilerReuse.checkpointValidationReused = true ∧
      r.compilerReuse.verificationReused = true := by
  have hguards := adapter_reuses_v01_guards r.compilerReuse
  exact ⟨v01_remains_sole_structured_compiler r.compilerReuse,
    hguards.1, hguards.2.1, hguards.2.2.1, hguards.2.2.2.1,
    hguards.2.2.2.2⟩


theorem materialization_preserves_templates_identity_and_recovery (r : Receipt) :
    r.materialization.materializedTemplateCount =
        r.materialization.expectedTemplateCount ∧
      r.materialization.exactOrderPreserved = true ∧
      r.materialization.exactIdentityPreserved = true ∧
      r.materialization.selectedCandidatePreserved = true ∧
      r.materialization.observationCoverage = true ∧
      r.materialization.verificationCoverage = true ∧
      r.materialization.stopCoverage = true ∧
      r.materialization.rollbackCoverage = true := by
  have hidentity := materialization_preserves_count_order_and_identity r.materialization
  have hcoverage :=
    materialization_covers_observation_verification_and_recovery r.materialization
  exact ⟨hidentity.1, hidentity.2.1, hidentity.2.2,
    r.selectedIdentityPreserved, hcoverage.1, hcoverage.2.1,
    hcoverage.2.2.1, hcoverage.2.2.2⟩


theorem hold_materializes_zero_executable_steps
    (r : Receipt) (hhold : r.source.selectedCandidate = .hold) :
    r.holdMaterialization.executableStepCount = 0 ∧
      r.holdMaterialization.withheldTemplateCount =
        r.holdMaterialization.expectedTemplateCount := by
  exact ⟨r.holdZeroExecutable hhold, r.holdWithheldVisible hhold⟩


theorem materialization_preserves_dual_lineage_and_digest_bindings (r : Receipt) :
    r.dualLineage.waAuthorizationBound = true ∧
      r.dualLineage.replanIdentityBound = true ∧
      r.dualLineage.waIdentityUsedAsReplanIdentity = false ∧
      r.dualLineage.lineageCollapseDetected = false ∧
      r.digestBinding.replanReceiptPreserved = true ∧
      r.digestBinding.nextPlanBasisPreserved = true ∧
      r.digestBinding.selectedCandidatePreserved = true ∧
      r.digestBinding.qiConditionPreserved = true ∧
      r.digestBinding.decisionReceiptPreserved = true ∧
      r.digestBinding.synthesisPacketPreserved = true := by
  have hlineage := adapter_preserves_dual_lineage r.dualLineage
  have hdigest1 := adapter_preserves_replan_and_basis_identity r.digestBinding
  have hdigest2 := adapter_preserves_qi_decision_and_synthesis r.digestBinding
  exact ⟨hlineage.1, hlineage.2, r.dualLineage.identityCollapseForbidden,
    r.dualLineage.lineageCollapseForbidden, hdigest1.1, hdigest1.2.1,
    hdigest1.2.2, hdigest2.1, hdigest2.2.1, hdigest2.2.2⟩


theorem materialization_is_single_use_and_replay_safe (r : Receipt) :
    r.singleUse.replanReceiptConsumed = true ∧
      r.singleUse.nextPlanBasisConsumed = true ∧
      r.singleUse.conflictingReplayAccepted = false ∧
      r.singleUse.exactReplayIdempotent = true := by
  have hsingle := adapter_activation_is_single_use r.singleUse
  exact ⟨hsingle.1, hsingle.2.1, hsingle.2.2,
    exact_adapter_replay_is_idempotent r.singleUse⟩


theorem materialization_events_append_strictly (r : Receipt) :
    r.source.commitIndex.current < r.materializationIndex.current ∧
      r.materializationIndex.current < r.receiptIndex.current := by
  constructor
  · rw [r.materializationIndexExact]
    exact replanEventIndex_strict r.source.commitIndex
  · rw [r.receiptIndexExact]
    exact replanEventIndex_strict r.materializationIndex


theorem materialization_history_appends_two_records (r : Receipt) :
    r.historyAfter.committedRecords = r.source.historyAfter.committedRecords + 2 ∧
      r.historyAfter.snapshotRecords = r.source.historyAfter.committedRecords + 2 := by
  refine ⟨r.historyExact, ?_⟩
  rw [adapterHistory_snapshot_matches_commits r.historyAfter]
  exact r.historyExact


theorem materialization_bridge_preserves_ownership (_r : Receipt) :
    Bridge.materializationOwnedByPlanOS = true ∧
      Bridge.executionOwnedByActOS = true := by
  exact ⟨Bridge.materializationOwnerRequired, Bridge.executionOwnerRequired⟩


theorem materialization_bridge_grants_no_activation_or_execution (_r : Receipt) :
    Bridge.runtimeActivatesPlan = false ∧ Bridge.runtimeExecutes = false ∧
      Bridge.runtimeGrantsHostLicense = false ∧
      Bridge.runtimeOverwritesMemory = false ∧ Bridge.runtimeUpdatesWorld = false ∧
      Bridge.nonAuthority.previousPlanUnchanged = true ∧
      Bridge.nonAuthority.executionGranted = false ∧
      Bridge.nonAuthority.truthAuthority = false ∧
      Bridge.nonAuthority.clinicalAuthority = false ∧
      Bridge.nonAuthority.legalAuthority = false ∧
      Bridge.nonAuthority.memoryOverwrite = false ∧
      Bridge.nonAuthority.hostLicenseGranted = false := by
  exact ⟨Bridge.activationForbidden, Bridge.executionForbidden,
    Bridge.licenseForbidden, Bridge.overwriteForbidden,
    Bridge.worldUpdateForbidden, Bridge.nonAuthority.previousRequired,
    Bridge.nonAuthority.executionForbidden, Bridge.nonAuthority.truthForbidden,
    Bridge.nonAuthority.clinicalForbidden, Bridge.nonAuthority.legalForbidden,
    Bridge.nonAuthority.overwriteForbidden, Bridge.nonAuthority.licenseForbidden⟩


theorem materialization_digest_is_exact (r : Receipt) :
    r.digest = Bridge.digestOf r.source r.route r.projectedRoute r.exactNextCycle
      r.dualLineage r.digestBinding r.materialization r.holdMaterialization
      r.compilerReuse r.singleUse r.materializationIndex r.receiptIndex
      r.historyAfter := by
  exact r.digestExact

end VacuumExpectationCompilerMaterializationBridge
end
end PlanOS
end KUOS
