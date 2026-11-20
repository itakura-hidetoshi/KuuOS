import Mathlib
import KUOS.Architecture.LeanPythonVerifyPlanSixRoutesV0_45

/-!
# v0.46 DecisionOS source-mapped conditional three-stage witness

The original 2026-11-20 DecisionOS v0.8 Lean source is pinned byte-for-byte
by a separate read-only checker. Importing the original type currently fails
in its historical import closure at KuuOS.PlanOSV102, a Lake-unregistered
legacy root. We DO NOT hide that obstruction or claim definitional equality.

The following receipt AND validity structures repeat every field and every
validity premise of the original v0.8 public source within this independent
module. This is a separately proved source-mapped model, NOT an imported
proof of original-type equality or CPython semantic equivalence.

The original Python DecisionOS/VerifyOS/PlanOS builders are exercised in a
separate read-only runtime gate; no authority flows from this Lean model.
-/

namespace KUOS.Architecture.LeanPythonDecisionVerifyPlanNativeHandoffV0_46

open KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4
open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03
open KUOS.Architecture.LeanPythonMiddleWaySemanticBridgeV0_43
open KUOS.Architecture.LeanPythonVerifyPlanSixRoutesV0_45

/-- Field-for-field source-mapped model of the exact pinned original
    DecisionOS v0.8 BoundedPlanSynthesisRequestHandoffReceipt. -/
structure SourceMappedDecisionHandoffReceipt where
  selectedCandidateNotSubstituted : Prop
  selectionRemainsDecisionOSOwned : Prop
  candidateEvidenceLineagePreserved : Prop
  retainedAlternativesVisibleToSynthesis : Prop
  retainedNonadmissibleCandidatesVisible : Prop
  nonselectionReasonsPreserved : Prop
  dissentVisibilityPreserved : Prop
  minorityVisibilityPreserved : Prop
  requiredReviewFieldPreserved : Prop
  planningHorizonBounded : Prop
  planStepCountBounded : Prop
  branchingFactorBounded : Prop
  revisionCyclesBounded : Prop
  reversibleActionsRequired : Prop
  irreversibleStepRequiresCheckpoint : Prop
  stopConditionsPresent : Prop
  forbiddenEffectsFixed : Prop
  persistentWorldStateUnchanged : Prop
  worldModelPredictionNotTruth : Prop
  worldMutationNotGranted : Prop
  historyReadOnly : Prop
  qiGrantsNoAuthority : Prop
  planSynthesisRequestIssued : Bool
  planosSynthesisScopeBounded : Bool
  planosReceivesRequestNotSelectionAuthority : Bool
  selectionAuthorityTransferredToPlanOS : Bool
  executionAuthorityGrantedToPlanOS : Bool
  planosPlanReceiptRequired : Bool
  planSynthesisResultNotAcceptedWithoutReceipt : Bool
  planSynthesisPerformed : Bool
  concretePlanIssued : Bool
  planReceiptIssued : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

/-- Original v0.8 validity hypotheses are retained field-for-field;
    no validity premise is dropped to make the source-mapped proof pass. -/
structure SourceMappedDecisionHandoffValid
    (r : SourceMappedDecisionHandoffReceipt) : Prop where
  selected_candidate_not_substituted : r.selectedCandidateNotSubstituted
  selection_remains_decision_os_owned : r.selectionRemainsDecisionOSOwned
  candidate_evidence_lineage_preserved : r.candidateEvidenceLineagePreserved
  retained_alternatives_visible : r.retainedAlternativesVisibleToSynthesis
  retained_nonadmissible_visible : r.retainedNonadmissibleCandidatesVisible
  nonselection_reasons_preserved : r.nonselectionReasonsPreserved
  dissent_visibility_preserved : r.dissentVisibilityPreserved
  minority_visibility_preserved : r.minorityVisibilityPreserved
  required_review_field_preserved : r.requiredReviewFieldPreserved
  planning_horizon_bounded : r.planningHorizonBounded
  plan_step_count_bounded : r.planStepCountBounded
  branching_factor_bounded : r.branchingFactorBounded
  revision_cycles_bounded : r.revisionCyclesBounded
  reversible_actions_required : r.reversibleActionsRequired
  irreversible_step_requires_checkpoint : r.irreversibleStepRequiresCheckpoint
  stop_conditions_present : r.stopConditionsPresent
  forbidden_effects_fixed : r.forbiddenEffectsFixed
  persistent_world_state_unchanged : r.persistentWorldStateUnchanged
  world_model_prediction_not_truth : r.worldModelPredictionNotTruth
  world_mutation_not_granted : r.worldMutationNotGranted
  history_read_only : r.historyReadOnly
  qi_grants_no_authority : r.qiGrantsNoAuthority
  plan_synthesis_request_issued : r.planSynthesisRequestIssued = true
  planos_synthesis_scope_bounded : r.planosSynthesisScopeBounded = true
  planos_receives_request_not_selection_authority :
    r.planosReceivesRequestNotSelectionAuthority = true
  selection_authority_not_transferred_to_plan_os :
    r.selectionAuthorityTransferredToPlanOS = false
  execution_authority_not_granted_to_plan_os :
    r.executionAuthorityGrantedToPlanOS = false
  planos_plan_receipt_required : r.planosPlanReceiptRequired = true
  synthesis_result_requires_receipt :
    r.planSynthesisResultNotAcceptedWithoutReceipt = true
  plan_synthesis_not_performed : r.planSynthesisPerformed = false
  concrete_plan_not_issued : r.concretePlanIssued = false
  plan_receipt_not_issued : r.planReceiptIssued = false
  future_only : r.futureOnly = true
  active_now_false : r.activeNow = false
  execution_permission_false : r.executionPermission = false

/-- Source-mapped DecisionOS keeps its five hard authority boundaries. -/
def sourceMappedDecisionAuthorityBoundary
    (r : SourceMappedDecisionHandoffReceipt) : Prop :=
  r.planSynthesisRequestIssued = true ∧
  r.selectionAuthorityTransferredToPlanOS = false ∧
  r.executionAuthorityGrantedToPlanOS = false ∧
  r.planSynthesisPerformed = false ∧
  r.executionPermission = false

theorem sourceMappedDecisionAuthorityBoundary_of_valid
    (r : SourceMappedDecisionHandoffReceipt)
    (h : SourceMappedDecisionHandoffValid r) :
    sourceMappedDecisionAuthorityBoundary r := by
  exact ⟨h.plan_synthesis_request_issued,
    h.selection_authority_not_transferred_to_plan_os,
    h.execution_authority_not_granted_to_plan_os,
    h.plan_synthesis_not_performed,
    h.execution_permission_false⟩

/-- This is WHOLE packet identity over a supplied type, not just a hash. -/
structure WholeReceiptSeam (Receipt : Type)
    (decisionOutput verifySource : Receipt) : Prop where
  exactPacket : decisionOutput = verifySource

/-- Constructed only when exact packet identity and the entire original
    source-mapped validity premise are explicitly supplied. -/
theorem decisionVerifyPlanConditionalWitness
    {Receipt : Type}
    (r : SourceMappedDecisionHandoffReceipt)
    (decisionOutput verifySource : Receipt)
    (hDecision : SourceMappedDecisionHandoffValid r)
    (hSeam : WholeReceiptSeam Receipt decisionOutput verifySource)
    (context : ContextKey) (transition : TransitionKind) :
    sourceMappedDecisionAuthorityBoundary r ∧
    decisionOutput = verifySource ∧
    intakeRouteSimulation.targetRelation
      (dispositionForStatus (statusForTransition transition),
        admittedForStatus (statusForTransition transition))
      (encodeIntake (dispositionForStatus (statusForTransition transition)),
        admittedForStatus (statusForTransition transition)) := by
  exact ⟨sourceMappedDecisionAuthorityBoundary_of_valid r hDecision,
    hSeam.exactPacket, sixRouteConditionalTwoStageWitness context transition⟩

/-- Exactly one bounded intake route in the finite conditional model. -/
theorem decisionHandoff_onlyRetainIsBoundedIntake
    (transition : TransitionKind) :
    admittedForStatus (statusForTransition transition) = true ↔
      transition = .retain :=
  onlyRetainRouteAdmitted transition

/-- Local consistency never turns either original-source-mapped Decision
    validity or v0.45 VerifyOS/PlanOS routing into host execution authority. -/
theorem decisionAndRouteCannotLicenseExecution
    (r : SourceMappedDecisionHandoffReceipt)
    (hDecision : SourceMappedDecisionHandoffValid r)
    (transition : TransitionKind) :
    r.executionPermission = false ∧
    ¬ CanExecute {
      evidence := .locallyChecked
      globalDescentCertified := false
      universalLeanPythonRefinementCertified := false
      executionLicensed := false
    } := by
  exact ⟨hDecision.execution_permission_false,
    sixRouteCannotLicenseExecution transition⟩

end KUOS.Architecture.LeanPythonDecisionVerifyPlanNativeHandoffV0_46
