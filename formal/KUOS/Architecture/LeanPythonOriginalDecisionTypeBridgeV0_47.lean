import Mathlib
import KUOS.DecisionOS.BoundedPlanSynthesisRequestHandoffV0_8
import KUOS.Architecture.LeanPythonDecisionVerifyPlanNativeHandoffV0_46

/-!
# v0.47 actual original DecisionOS Lean type ↔ independent source-mapped v0.46

The original Lean type is imported and used here, not recreated or renamed.
The fixed Lake build globs must include the exact finite legacy dependencies.

Proof obligations:
* actual imported receipt type ↔ source-mapped receipt type with two inverse maps;
* actual imported validity type ↔ source-mapped validity for each original receipt;
* the original DecisionOS authority theorem can feed the existing v0.46
  conditional typed whole-receipt/VerifyOS→PlanOS six-route theorem.

Still NOT proved: a Lean↔CPython interpreter refinement, actual external
issuer authenticity, global descent, a shared causal clock or execution license.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.LeanPythonOriginalDecisionTypeBridgeV0_47

open KUOS.DecisionOS
open KUOS.Architecture.LeanPythonDecisionVerifyPlanNativeHandoffV0_46
open KUOS.Architecture.LeanPythonVerifyPlanSixRoutesV0_45
open KUOS.Architecture.LeanPythonMiddleWaySemanticBridgeV0_43
open KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4
open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-- Exact map FROM the imported original v0.8 receipt type. -/
def originalToMapped (r : BoundedPlanSynthesisRequestHandoffReceipt) :
    SourceMappedDecisionHandoffReceipt where
  selectedCandidateNotSubstituted := r.selectedCandidateNotSubstituted
  selectionRemainsDecisionOSOwned := r.selectionRemainsDecisionOSOwned
  candidateEvidenceLineagePreserved := r.candidateEvidenceLineagePreserved
  retainedAlternativesVisibleToSynthesis := r.retainedAlternativesVisibleToSynthesis
  retainedNonadmissibleCandidatesVisible := r.retainedNonadmissibleCandidatesVisible
  nonselectionReasonsPreserved := r.nonselectionReasonsPreserved
  dissentVisibilityPreserved := r.dissentVisibilityPreserved
  minorityVisibilityPreserved := r.minorityVisibilityPreserved
  requiredReviewFieldPreserved := r.requiredReviewFieldPreserved
  planningHorizonBounded := r.planningHorizonBounded
  planStepCountBounded := r.planStepCountBounded
  branchingFactorBounded := r.branchingFactorBounded
  revisionCyclesBounded := r.revisionCyclesBounded
  reversibleActionsRequired := r.reversibleActionsRequired
  irreversibleStepRequiresCheckpoint := r.irreversibleStepRequiresCheckpoint
  stopConditionsPresent := r.stopConditionsPresent
  forbiddenEffectsFixed := r.forbiddenEffectsFixed
  persistentWorldStateUnchanged := r.persistentWorldStateUnchanged
  worldModelPredictionNotTruth := r.worldModelPredictionNotTruth
  worldMutationNotGranted := r.worldMutationNotGranted
  historyReadOnly := r.historyReadOnly
  qiGrantsNoAuthority := r.qiGrantsNoAuthority
  planSynthesisRequestIssued := r.planSynthesisRequestIssued
  planosSynthesisScopeBounded := r.planosSynthesisScopeBounded
  planosReceivesRequestNotSelectionAuthority := r.planosReceivesRequestNotSelectionAuthority
  selectionAuthorityTransferredToPlanOS := r.selectionAuthorityTransferredToPlanOS
  executionAuthorityGrantedToPlanOS := r.executionAuthorityGrantedToPlanOS
  planosPlanReceiptRequired := r.planosPlanReceiptRequired
  planSynthesisResultNotAcceptedWithoutReceipt := r.planSynthesisResultNotAcceptedWithoutReceipt
  planSynthesisPerformed := r.planSynthesisPerformed
  concretePlanIssued := r.concretePlanIssued
  planReceiptIssued := r.planReceiptIssued
  futureOnly := r.futureOnly
  activeNow := r.activeNow
  executionPermission := r.executionPermission

/-- Exact map BACK TO the imported original v0.8 receipt type. -/
def mappedToOriginal (r : SourceMappedDecisionHandoffReceipt) :
    BoundedPlanSynthesisRequestHandoffReceipt where
  selectedCandidateNotSubstituted := r.selectedCandidateNotSubstituted
  selectionRemainsDecisionOSOwned := r.selectionRemainsDecisionOSOwned
  candidateEvidenceLineagePreserved := r.candidateEvidenceLineagePreserved
  retainedAlternativesVisibleToSynthesis := r.retainedAlternativesVisibleToSynthesis
  retainedNonadmissibleCandidatesVisible := r.retainedNonadmissibleCandidatesVisible
  nonselectionReasonsPreserved := r.nonselectionReasonsPreserved
  dissentVisibilityPreserved := r.dissentVisibilityPreserved
  minorityVisibilityPreserved := r.minorityVisibilityPreserved
  requiredReviewFieldPreserved := r.requiredReviewFieldPreserved
  planningHorizonBounded := r.planningHorizonBounded
  planStepCountBounded := r.planStepCountBounded
  branchingFactorBounded := r.branchingFactorBounded
  revisionCyclesBounded := r.revisionCyclesBounded
  reversibleActionsRequired := r.reversibleActionsRequired
  irreversibleStepRequiresCheckpoint := r.irreversibleStepRequiresCheckpoint
  stopConditionsPresent := r.stopConditionsPresent
  forbiddenEffectsFixed := r.forbiddenEffectsFixed
  persistentWorldStateUnchanged := r.persistentWorldStateUnchanged
  worldModelPredictionNotTruth := r.worldModelPredictionNotTruth
  worldMutationNotGranted := r.worldMutationNotGranted
  historyReadOnly := r.historyReadOnly
  qiGrantsNoAuthority := r.qiGrantsNoAuthority
  planSynthesisRequestIssued := r.planSynthesisRequestIssued
  planosSynthesisScopeBounded := r.planosSynthesisScopeBounded
  planosReceivesRequestNotSelectionAuthority := r.planosReceivesRequestNotSelectionAuthority
  selectionAuthorityTransferredToPlanOS := r.selectionAuthorityTransferredToPlanOS
  executionAuthorityGrantedToPlanOS := r.executionAuthorityGrantedToPlanOS
  planosPlanReceiptRequired := r.planosPlanReceiptRequired
  planSynthesisResultNotAcceptedWithoutReceipt := r.planSynthesisResultNotAcceptedWithoutReceipt
  planSynthesisPerformed := r.planSynthesisPerformed
  concretePlanIssued := r.concretePlanIssued
  planReceiptIssued := r.planReceiptIssued
  futureOnly := r.futureOnly
  activeNow := r.activeNow
  executionPermission := r.executionPermission

/-- The original-to-model map has a proven two-sided inverse. -/
def originalReceiptEquiv :
    BoundedPlanSynthesisRequestHandoffReceipt ≃
      SourceMappedDecisionHandoffReceipt where
  toFun := originalToMapped
  invFun := mappedToOriginal
  left_inv := by
    intro r
    cases r
    rfl
  right_inv := by
    intro r
    cases r
    rfl

/-- No DecisionOS v0.8 validity hypothesis was lost in the mapping. -/
theorem originalValid_iff_mappedValid
    (r : BoundedPlanSynthesisRequestHandoffReceipt) :
    BoundedPlanSynthesisRequestHandoffValid r ↔
      SourceMappedDecisionHandoffValid (originalToMapped r) := by
  constructor
  · intro h
    exact {
      selected_candidate_not_substituted := h.selected_candidate_not_substituted
      selection_remains_decision_os_owned := h.selection_remains_decision_os_owned
      candidate_evidence_lineage_preserved := h.candidate_evidence_lineage_preserved
      retained_alternatives_visible := h.retained_alternatives_visible
      retained_nonadmissible_visible := h.retained_nonadmissible_visible
      nonselection_reasons_preserved := h.nonselection_reasons_preserved
      dissent_visibility_preserved := h.dissent_visibility_preserved
      minority_visibility_preserved := h.minority_visibility_preserved
      required_review_field_preserved := h.required_review_field_preserved
      planning_horizon_bounded := h.planning_horizon_bounded
      plan_step_count_bounded := h.plan_step_count_bounded
      branching_factor_bounded := h.branching_factor_bounded
      revision_cycles_bounded := h.revision_cycles_bounded
      reversible_actions_required := h.reversible_actions_required
      irreversible_step_requires_checkpoint := h.irreversible_step_requires_checkpoint
      stop_conditions_present := h.stop_conditions_present
      forbidden_effects_fixed := h.forbidden_effects_fixed
      persistent_world_state_unchanged := h.persistent_world_state_unchanged
      world_model_prediction_not_truth := h.world_model_prediction_not_truth
      world_mutation_not_granted := h.world_mutation_not_granted
      history_read_only := h.history_read_only
      qi_grants_no_authority := h.qi_grants_no_authority
      plan_synthesis_request_issued := h.plan_synthesis_request_issued
      planos_synthesis_scope_bounded := h.planos_synthesis_scope_bounded
      planos_receives_request_not_selection_authority := h.planos_receives_request_not_selection_authority
      selection_authority_not_transferred_to_plan_os := h.selection_authority_not_transferred_to_plan_os
      execution_authority_not_granted_to_plan_os := h.execution_authority_not_granted_to_plan_os
      planos_plan_receipt_required := h.planos_plan_receipt_required
      synthesis_result_requires_receipt := h.synthesis_result_requires_receipt
      plan_synthesis_not_performed := h.plan_synthesis_not_performed
      concrete_plan_not_issued := h.concrete_plan_not_issued
      plan_receipt_not_issued := h.plan_receipt_not_issued
      future_only := h.future_only
      active_now_false := h.active_now_false
      execution_permission_false := h.execution_permission_false
    }
  · intro h
    exact {
      selected_candidate_not_substituted := h.selected_candidate_not_substituted
      selection_remains_decision_os_owned := h.selection_remains_decision_os_owned
      candidate_evidence_lineage_preserved := h.candidate_evidence_lineage_preserved
      retained_alternatives_visible := h.retained_alternatives_visible
      retained_nonadmissible_visible := h.retained_nonadmissible_visible
      nonselection_reasons_preserved := h.nonselection_reasons_preserved
      dissent_visibility_preserved := h.dissent_visibility_preserved
      minority_visibility_preserved := h.minority_visibility_preserved
      required_review_field_preserved := h.required_review_field_preserved
      planning_horizon_bounded := h.planning_horizon_bounded
      plan_step_count_bounded := h.plan_step_count_bounded
      branching_factor_bounded := h.branching_factor_bounded
      revision_cycles_bounded := h.revision_cycles_bounded
      reversible_actions_required := h.reversible_actions_required
      irreversible_step_requires_checkpoint := h.irreversible_step_requires_checkpoint
      stop_conditions_present := h.stop_conditions_present
      forbidden_effects_fixed := h.forbidden_effects_fixed
      persistent_world_state_unchanged := h.persistent_world_state_unchanged
      world_model_prediction_not_truth := h.world_model_prediction_not_truth
      world_mutation_not_granted := h.world_mutation_not_granted
      history_read_only := h.history_read_only
      qi_grants_no_authority := h.qi_grants_no_authority
      plan_synthesis_request_issued := h.plan_synthesis_request_issued
      planos_synthesis_scope_bounded := h.planos_synthesis_scope_bounded
      planos_receives_request_not_selection_authority := h.planos_receives_request_not_selection_authority
      selection_authority_not_transferred_to_plan_os := h.selection_authority_not_transferred_to_plan_os
      execution_authority_not_granted_to_plan_os := h.execution_authority_not_granted_to_plan_os
      planos_plan_receipt_required := h.planos_plan_receipt_required
      synthesis_result_requires_receipt := h.synthesis_result_requires_receipt
      plan_synthesis_not_performed := h.plan_synthesis_not_performed
      concrete_plan_not_issued := h.concrete_plan_not_issued
      plan_receipt_not_issued := h.plan_receipt_not_issued
      future_only := h.future_only
      active_now_false := h.active_now_false
      execution_permission_false := h.execution_permission_false
    }

/-- Native DecisionOS original theorem governs authority; it does not
    transfer selection, grant execution or perform synthesis. -/
theorem originalDecisionBoundaries
    (r : BoundedPlanSynthesisRequestHandoffReceipt)
    (h : BoundedPlanSynthesisRequestHandoffValid r) :
    r.planSynthesisRequestIssued = true ∧
    r.selectionAuthorityTransferredToPlanOS = false ∧
    r.executionAuthorityGrantedToPlanOS = false ∧
    r.planSynthesisPerformed = false ∧
    r.executionPermission = false := by
  obtain ⟨hRequest, _, _, hSelection, hExecution⟩ :=
    planos_receives_bounded_request_without_selection_or_execution_authority r h
  exact ⟨hRequest, hSelection, hExecution,
    h.plan_synthesis_not_performed, h.execution_permission_false⟩

/-- The *actual* v0.8 imported validity certificate enters the previously
    proved middle-way route composition, conditional on a full typed seam.
    No Python execution witness is manufactured by this theorem. -/
theorem originalDecisionSixRouteConditionalWitness
    {Receipt : Type}
    (r : BoundedPlanSynthesisRequestHandoffReceipt)
    (decisionOutput verifySource : Receipt)
    (hOriginal : BoundedPlanSynthesisRequestHandoffValid r)
    (hSeam : WholeReceiptSeam Receipt decisionOutput verifySource)
    (context : ContextKey) (transition : TransitionKind) :
    sourceMappedDecisionAuthorityBoundary (originalToMapped r) ∧
    decisionOutput = verifySource ∧
    intakeRouteSimulation.targetRelation
      (dispositionForStatus (statusForTransition transition),
        admittedForStatus (statusForTransition transition))
      (encodeIntake (dispositionForStatus (statusForTransition transition)),
        admittedForStatus (statusForTransition transition)) := by
  exact decisionVerifyPlanConditionalWitness
    (originalToMapped r) decisionOutput verifySource
    ((originalValid_iff_mappedValid r).mp hOriginal)
    hSeam context transition

/-- Boundaries of native v0.8 and finite v0.45 cannot promote local
    preference/intake into general execution authority. -/
theorem originalHandoffNeverLicensesHostExecution
    (r : BoundedPlanSynthesisRequestHandoffReceipt)
    (hOriginal : BoundedPlanSynthesisRequestHandoffValid r)
    (transition : TransitionKind) :
    r.executionPermission = false ∧
    ¬ CanExecute {
      evidence := .locallyChecked
      globalDescentCertified := false
      universalLeanPythonRefinementCertified := false
      executionLicensed := false
    } := by
  exact decisionAndRouteCannotLicenseExecution
    (originalToMapped r)
    ((originalValid_iff_mappedValid r).mp hOriginal)
    transition

end KUOS.Architecture.LeanPythonOriginalDecisionTypeBridgeV0_47

/-!
# v0.47 exact-head kernel axiom audit (non-mutating elaboration commands)
Every new declaration above is examined independently; output is scoped to
this source HEAD and is not a certificate of Python execution semantics.
-/
#print axioms KUOS.Architecture.LeanPythonOriginalDecisionTypeBridgeV0_47.originalToMapped
#print axioms KUOS.Architecture.LeanPythonOriginalDecisionTypeBridgeV0_47.mappedToOriginal
#print axioms KUOS.Architecture.LeanPythonOriginalDecisionTypeBridgeV0_47.originalReceiptEquiv
#print axioms KUOS.Architecture.LeanPythonOriginalDecisionTypeBridgeV0_47.originalValid_iff_mappedValid
#print axioms KUOS.Architecture.LeanPythonOriginalDecisionTypeBridgeV0_47.originalDecisionBoundaries
#print axioms KUOS.Architecture.LeanPythonOriginalDecisionTypeBridgeV0_47.originalDecisionSixRouteConditionalWitness
#print axioms KUOS.Architecture.LeanPythonOriginalDecisionTypeBridgeV0_47.originalHandoffNeverLicensesHostExecution
