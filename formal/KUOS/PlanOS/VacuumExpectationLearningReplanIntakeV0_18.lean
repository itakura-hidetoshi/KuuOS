import Mathlib
import KUOS.LearnOS.VacuumExpectationVerificationFutureOnlyDeltaV0_3
import KUOS.PlanOS.QiConditionedNonMarkovReplanV0_2
import KUOS.PlanOS.ClosedLoopReplanIntakeAdapterV0_4

/-!
PlanOS v0.18: exact replan intake for a WORLD-derived LearnOS v0.3 receipt.

This adapter binds an immutable, future-only LearnOS receipt to the existing
PlanOS replan source and pristine closed-loop bind contracts. It commits one
intake/bind record, but does not activate replan, synthesize or activate a plan,
permit execution, grant a host licence, overwrite memory, or update WORLD.
-/

namespace KUOS
namespace PlanOS

open WORLD
open ObserveOS
open VerifyOS
open LearnOS

structure VacuumExpectationLearningReplanIntakeBridge
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
        K O Intake ObserveBridge VerifyBridge) where
  IntakeDigest : Type
  digestOf :
    VacuumExpectationVerificationLearningReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge →
      ReplanSourceBinding →
      ClosedLoopBindState →
      ClosedLoopFutureBoundary →
      ReplanOwnership →
      ClosedLoopActivationSeparation →
      ReplanEventIndex →
      ReplanEventIndex →
      ReplanHistory →
      ReplanHistory →
      IntakeDigest
  replanNonAuthority : ReplanNonAuthority
  planOSOwnsReplan : Bool
  decisionOSOwnsSelection : Bool
  planOSOwnsSynthesis : Bool
  actOSOwnsExecution : Bool
  bridgeRuntimeActivatesReplan : Bool
  bridgeRuntimeActivatesPlan : Bool
  bridgeRuntimePermitsExecution : Bool
  bridgeRuntimeGrantsHostLicense : Bool
  bridgeRuntimeOverwritesMemory : Bool
  bridgeRuntimeUpdatesWORLD : Bool
  replanOwnershipRequired : planOSOwnsReplan = true
  selectionOwnershipRequired : decisionOSOwnsSelection = true
  synthesisOwnershipRequired : planOSOwnsSynthesis = true
  executionOwnershipRequired : actOSOwnsExecution = true
  replanActivationForbidden : bridgeRuntimeActivatesReplan = false
  planActivationForbidden : bridgeRuntimeActivatesPlan = false
  executionPermissionForbidden : bridgeRuntimePermitsExecution = false
  hostLicenseForbidden : bridgeRuntimeGrantsHostLicense = false
  memoryOverwriteForbidden : bridgeRuntimeOverwritesMemory = false
  worldUpdateForbidden : bridgeRuntimeUpdatesWORLD = false

structure VacuumExpectationLearningReplanIntakeReceipt
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
    (Bridge : VacuumExpectationLearningReplanIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge) where
  learning : VacuumExpectationVerificationLearningReceipt
    K O Intake ObserveBridge VerifyBridge LearnBridge
  sourceBinding : ReplanSourceBinding
  bindState : ClosedLoopBindState
  futureBoundary : ClosedLoopFutureBoundary
  ownership : ReplanOwnership
  activation : ClosedLoopActivationSeparation
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
  sourceLearningRecorded : learning.learningRecorded = true
  sourceReplanRequired : learning.debtSemantics.replanRequired = true
  sourceFutureOnly : learning.delta.futureOnly = true
  sourceInactiveNow : learning.delta.activeNow = false
  sourceCurrentUnchanged : learning.delta.currentCycleMutation = false
  sourcePastUnchanged : learning.delta.pastRecordMutation = false
  currentPlanExact :
    sourceBinding.committedCurrentPlan = currentPlanCommitted
  learningCommitExact :
    sourceBinding.committedLearnState = learning.learningRecorded
  learningDeltaExact :
    sourceBinding.learningDeltaBound = sourceLearningBound
  middleWayExact :
    sourceBinding.middleWayReportBound = learning.middleWay.candidateAdmissible
  verificationExact :
    sourceBinding.verificationEvidenceBound =
      learning.verification.verificationRecorded
  futureOnlyExact :
    sourceBinding.futureOnlyLearning = learning.delta.futureOnly
  replanDebtExact :
    sourceBinding.replanRequiredByLearnOS =
      learning.debtSemantics.replanRequired
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
  intakeDigestExact :
    intakeDigest = Bridge.digestOf learning sourceBinding bindState
      futureBoundary ownership activation indexBefore indexAfter
      historyBefore historyAfter

namespace VacuumExpectationLearningReplanIntakeBridge

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
    {Bridge : VacuumExpectationLearningReplanIntakeBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge}

theorem intake_requires_committed_future_only_learning
    (receipt : VacuumExpectationLearningReplanIntakeReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge Bridge) :
    receipt.learning.learningRecorded = true ∧
      receipt.learning.debtSemantics.replanRequired = true ∧
      receipt.learning.delta.futureOnly = true ∧
      receipt.learning.delta.activeNow = false ∧
      receipt.learning.delta.currentCycleMutation = false ∧
      receipt.learning.delta.pastRecordMutation = false := by
  exact ⟨receipt.sourceLearningRecorded,
    receipt.sourceReplanRequired,
    receipt.sourceFutureOnly,
    receipt.sourceInactiveNow,
    receipt.sourceCurrentUnchanged,
    receipt.sourcePastUnchanged⟩

theorem intake_binds_existing_replan_source
    (receipt : VacuumExpectationLearningReplanIntakeReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge Bridge) :
    receipt.sourceBinding.committedCurrentPlan = true ∧
      receipt.sourceBinding.committedLearnState = true ∧
      receipt.sourceBinding.learningDeltaBound = true ∧
      receipt.sourceBinding.middleWayReportBound = true ∧
      receipt.sourceBinding.verificationEvidenceBound = true ∧
      receipt.sourceBinding.futureOnlyLearning = true ∧
      receipt.sourceBinding.learningInactiveNow = true ∧
      receipt.sourceBinding.replanRequiredByLearnOS = true := by
  exact ⟨receipt.sourceBinding.currentPlanRequired,
    receipt.sourceBinding.learnStateRequired,
    receipt.sourceBinding.deltaRequired,
    receipt.sourceBinding.middleWayRequired,
    receipt.sourceBinding.evidenceRequired,
    receipt.sourceBinding.futureRequired,
    receipt.sourceBinding.inactiveRequired,
    receipt.sourceBinding.replanDebtRequired⟩

theorem intake_enters_pristine_planos_bind
    (receipt : VacuumExpectationLearningReplanIntakeReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge Bridge) :
    receipt.bindState.phaseIsBind = true ∧
      receipt.bindState.eventIndex = 0 ∧
      receipt.bindState.historyRequired = true := by
  exact closed_loop_enters_pristine_bind receipt.bindState

theorem intake_event_index_appends_exactly_once
    (receipt : VacuumExpectationLearningReplanIntakeReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge Bridge) :
    receipt.indexBefore.current = 0 ∧
      receipt.indexAfter.current = 1 := by
  have hbefore : receipt.indexBefore.current = 0 := by
    calc
      receipt.indexBefore.current = receipt.bindState.eventIndex :=
        receipt.indexBeforeExact
      _ = 0 := receipt.bindState.pristineRequired
  refine ⟨hbefore, ?_⟩
  calc
    receipt.indexAfter.current = receipt.indexBefore.append.current := by
      rw [receipt.indexAppendExact]
    _ = receipt.indexBefore.current + 1 := rfl
    _ = 1 := by simp [hbefore]

theorem intake_history_appends_exactly_once
    (receipt : VacuumExpectationLearningReplanIntakeReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge Bridge) :
    receipt.historyAfter.committedRecords =
        receipt.historyBefore.committedRecords + 1 ∧
      receipt.historyAfter.snapshotRecords =
        receipt.historyBefore.committedRecords + 1 := by
  refine ⟨receipt.historyAppendExact, ?_⟩
  rw [replanHistory_snapshot_matches_commits receipt.historyAfter]
  exact receipt.historyAppendExact

theorem intake_preserves_planos_decisionos_actos_ownership
    (receipt : VacuumExpectationLearningReplanIntakeReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge Bridge) :
    receipt.ownership.replanOwnedByPlanOS = true ∧
      receipt.ownership.selectionOwnedByDecisionOS = true ∧
      receipt.ownership.synthesisOwnedByPlanOS = true ∧
      receipt.ownership.executionOwnedByActOS = true := by
  exact ⟨receipt.ownership.replanOwnerRequired,
    receipt.ownership.selectionOwnerRequired,
    receipt.ownership.synthesisOwnerRequired,
    receipt.ownership.executionOwnerRequired⟩

theorem intake_commit_is_not_activation_plan_or_execution
    (receipt : VacuumExpectationLearningReplanIntakeReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge Bridge) :
    receipt.activation.intakeCommitted = true ∧
      receipt.activation.bindCommitted = true ∧
      receipt.activation.replanActivated = false ∧
      receipt.activation.planActivated = false ∧
      receipt.activation.executionPermitted = false ∧
      receipt.activation.hostLicenseGranted = false ∧
      Bridge.bridgeRuntimeActivatesReplan = false ∧
      Bridge.bridgeRuntimeActivatesPlan = false ∧
      Bridge.bridgeRuntimePermitsExecution = false := by
  exact ⟨receipt.activation.intakeRequired,
    receipt.activation.bindRequired,
    receipt.activation.replanForbidden,
    receipt.activation.planForbidden,
    receipt.activation.executionForbidden,
    receipt.activation.hostLicenseForbidden,
    Bridge.replanActivationForbidden,
    Bridge.planActivationForbidden,
    Bridge.executionPermissionForbidden⟩

theorem intake_future_boundary_preserves_current_and_past
    (receipt : VacuumExpectationLearningReplanIntakeReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge Bridge) :
    receipt.futureBoundary.futureOnly = true ∧
      receipt.futureBoundary.activeNow = false ∧
      receipt.futureBoundary.currentCycleUnchanged = true ∧
      receipt.futureBoundary.pastPlanUnchanged = true ∧
      receipt.futureBoundary.memoryOverwrite = false := by
  exact closed_loop_bind_is_future_only receipt.futureBoundary

theorem intake_bridge_grants_no_new_authority
    (_receipt : VacuumExpectationLearningReplanIntakeReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge Bridge) :
    Bridge.planOSOwnsReplan = true ∧
      Bridge.decisionOSOwnsSelection = true ∧
      Bridge.planOSOwnsSynthesis = true ∧
      Bridge.actOSOwnsExecution = true ∧
      Bridge.bridgeRuntimeActivatesReplan = false ∧
      Bridge.bridgeRuntimeActivatesPlan = false ∧
      Bridge.bridgeRuntimePermitsExecution = false ∧
      Bridge.bridgeRuntimeGrantsHostLicense = false ∧
      Bridge.bridgeRuntimeOverwritesMemory = false ∧
      Bridge.bridgeRuntimeUpdatesWORLD = false ∧
      Bridge.replanNonAuthority.truthAuthority = false ∧
      Bridge.replanNonAuthority.causalAuthority = false ∧
      Bridge.replanNonAuthority.executionAuthority = false ∧
      Bridge.replanNonAuthority.memoryOverwriteAuthority = false ∧
      Bridge.replanNonAuthority.selfModificationAuthority = false := by
  exact ⟨Bridge.replanOwnershipRequired,
    Bridge.selectionOwnershipRequired,
    Bridge.synthesisOwnershipRequired,
    Bridge.executionOwnershipRequired,
    Bridge.replanActivationForbidden,
    Bridge.planActivationForbidden,
    Bridge.executionPermissionForbidden,
    Bridge.hostLicenseForbidden,
    Bridge.memoryOverwriteForbidden,
    Bridge.worldUpdateForbidden,
    Bridge.replanNonAuthority.truthForbidden,
    Bridge.replanNonAuthority.causalForbidden,
    Bridge.replanNonAuthority.executionForbidden,
    Bridge.replanNonAuthority.overwriteForbidden,
    Bridge.replanNonAuthority.selfModificationForbidden⟩

theorem intake_digest_is_exact
    (receipt : VacuumExpectationLearningReplanIntakeReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge Bridge) :
    receipt.intakeDigest =
      Bridge.digestOf receipt.learning receipt.sourceBinding receipt.bindState
        receipt.futureBoundary receipt.ownership receipt.activation
        receipt.indexBefore receipt.indexAfter receipt.historyBefore
        receipt.historyAfter := by
  exact receipt.intakeDigestExact

theorem intake_candidate_value_remains_exact
    (receipt : VacuumExpectationLearningReplanIntakeReceipt
      K O Intake ObserveBridge VerifyBridge LearnBridge Bridge) :
    receipt.learning.verification.observeCommit.envelope.candidate.value =
      K.vacuumState
        receipt.learning.verification.observeCommit.envelope.candidate.observable := by
  exact receipt.learning.verification.observeCommit.envelope.candidate.value_eq_vacuum_expectation

end VacuumExpectationLearningReplanIntakeBridge
end PlanOS
end KUOS
