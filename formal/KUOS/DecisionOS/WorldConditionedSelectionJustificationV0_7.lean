import Mathlib
import KUOS.DecisionOS.WorldConditionedRelationalDeliberationV0_6

namespace KUOS
namespace DecisionOS

structure WorldConditionedSelectionJustificationReceipt where
  allCandidatesConsidered : Prop
  candidateIdentityPreserved : Prop
  retainedAlternativesPreserved : Prop
  nonselectedReasonsPreserved : Prop
  dissentVisibilityPreserved : Prop
  minorityVisibilityPreserved : Prop
  requiredReviewFieldPreserved : Prop
  selectedCandidateFromRelationalFrontier : Prop
  persistentWorldStateUnchanged : Prop
  worldModelPredictionNotTruth : Prop
  worldMutationNotGranted : Prop
  historyReadOnly : Prop
  qiGrantsNoAuthority : Prop
  sourceProbabilityAdvisoryOnly : Bool
  sourceActionAdvisoryOnly : Bool
  relationalPartialOrderUsed : Bool
  singleScalarUtilitySelectionForbidden : Bool
  silentSubstitutionDetected : Bool
  selectionAuthorityExercisedByDecisionOS : Bool
  selectionAuthorityInheritedFromPlanOS : Bool
  selectionAuthorityInheritedFromWorldModel : Bool
  selectionAuthorityInheritedFromQi : Bool
  decisionSelectionPerformed : Bool
  selectedCandidatePresent : Bool
  decisionReceiptIssued : Bool
  selectionIsNotPlanSynthesis : Bool
  selectionIsNotExecution : Bool
  planSynthesisPerformed : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

structure WorldConditionedSelectionJustificationValid
    (r : WorldConditionedSelectionJustificationReceipt) : Prop where
  all_candidates_considered : r.allCandidatesConsidered
  candidate_identity_preserved : r.candidateIdentityPreserved
  retained_alternatives_preserved : r.retainedAlternativesPreserved
  nonselected_reasons_preserved : r.nonselectedReasonsPreserved
  dissent_visibility_preserved : r.dissentVisibilityPreserved
  minority_visibility_preserved : r.minorityVisibilityPreserved
  required_review_field_preserved : r.requiredReviewFieldPreserved
  selected_candidate_from_relational_frontier :
    r.selectedCandidateFromRelationalFrontier
  persistent_world_state_unchanged : r.persistentWorldStateUnchanged
  world_model_prediction_not_truth : r.worldModelPredictionNotTruth
  world_mutation_not_granted : r.worldMutationNotGranted
  history_read_only : r.historyReadOnly
  qi_grants_no_authority : r.qiGrantsNoAuthority
  source_probability_advisory_only : r.sourceProbabilityAdvisoryOnly = true
  source_action_advisory_only : r.sourceActionAdvisoryOnly = true
  relational_partial_order_used : r.relationalPartialOrderUsed = true
  single_scalar_utility_selection_forbidden :
    r.singleScalarUtilitySelectionForbidden = true
  silent_substitution_forbidden : r.silentSubstitutionDetected = false
  selection_authority_exercised_by_decision_os :
    r.selectionAuthorityExercisedByDecisionOS = true
  selection_authority_not_inherited_from_plan_os :
    r.selectionAuthorityInheritedFromPlanOS = false
  selection_authority_not_inherited_from_world_model :
    r.selectionAuthorityInheritedFromWorldModel = false
  selection_authority_not_inherited_from_qi :
    r.selectionAuthorityInheritedFromQi = false
  decision_selection_performed : r.decisionSelectionPerformed = true
  selected_candidate_present : r.selectedCandidatePresent = true
  decision_receipt_issued : r.decisionReceiptIssued = true
  selection_not_plan_synthesis : r.selectionIsNotPlanSynthesis = true
  selection_not_execution : r.selectionIsNotExecution = true
  plan_synthesis_not_performed : r.planSynthesisPerformed = false
  future_only : r.futureOnly = true
  active_now_false : r.activeNow = false
  execution_permission_false : r.executionPermission = false

theorem selection_comes_from_relational_frontier
    (r : WorldConditionedSelectionJustificationReceipt)
    (h : WorldConditionedSelectionJustificationValid r) :
    r.selectedCandidateFromRelationalFrontier := by
  exact h.selected_candidate_from_relational_frontier

theorem selection_preserves_all_candidates_and_alternatives
    (r : WorldConditionedSelectionJustificationReceipt)
    (h : WorldConditionedSelectionJustificationValid r) :
    r.allCandidatesConsidered ∧ r.candidateIdentityPreserved ∧
      r.retainedAlternativesPreserved ∧ r.nonselectedReasonsPreserved := by
  exact ⟨h.all_candidates_considered, h.candidate_identity_preserved,
    h.retained_alternatives_preserved, h.nonselected_reasons_preserved⟩

theorem selection_preserves_dissent_minority_and_required_review
    (r : WorldConditionedSelectionJustificationReceipt)
    (h : WorldConditionedSelectionJustificationValid r) :
    r.dissentVisibilityPreserved ∧ r.minorityVisibilityPreserved ∧
      r.requiredReviewFieldPreserved := by
  exact ⟨h.dissent_visibility_preserved, h.minority_visibility_preserved,
    h.required_review_field_preserved⟩

theorem selection_is_not_probability_or_scalar_shortcut
    (r : WorldConditionedSelectionJustificationReceipt)
    (h : WorldConditionedSelectionJustificationValid r) :
    r.sourceProbabilityAdvisoryOnly = true ∧
      r.sourceActionAdvisoryOnly = true ∧
      r.relationalPartialOrderUsed = true ∧
      r.singleScalarUtilitySelectionForbidden = true := by
  exact ⟨h.source_probability_advisory_only,
    h.source_action_advisory_only,
    h.relational_partial_order_used,
    h.single_scalar_utility_selection_forbidden⟩

theorem decision_os_exercises_selection_without_inherited_authority
    (r : WorldConditionedSelectionJustificationReceipt)
    (h : WorldConditionedSelectionJustificationValid r) :
    r.selectionAuthorityExercisedByDecisionOS = true ∧
      r.selectionAuthorityInheritedFromPlanOS = false ∧
      r.selectionAuthorityInheritedFromWorldModel = false ∧
      r.selectionAuthorityInheritedFromQi = false := by
  exact ⟨h.selection_authority_exercised_by_decision_os,
    h.selection_authority_not_inherited_from_plan_os,
    h.selection_authority_not_inherited_from_world_model,
    h.selection_authority_not_inherited_from_qi⟩

theorem selection_issues_decision_receipt_without_silent_substitution
    (r : WorldConditionedSelectionJustificationReceipt)
    (h : WorldConditionedSelectionJustificationValid r) :
    r.decisionSelectionPerformed = true ∧
      r.selectedCandidatePresent = true ∧
      r.decisionReceiptIssued = true ∧
      r.silentSubstitutionDetected = false := by
  exact ⟨h.decision_selection_performed, h.selected_candidate_present,
    h.decision_receipt_issued, h.silent_substitution_forbidden⟩

theorem selection_preserves_world_history_and_qi_boundaries
    (r : WorldConditionedSelectionJustificationReceipt)
    (h : WorldConditionedSelectionJustificationValid r) :
    r.persistentWorldStateUnchanged ∧ r.worldModelPredictionNotTruth ∧
      r.worldMutationNotGranted ∧ r.historyReadOnly ∧
      r.qiGrantsNoAuthority := by
  exact ⟨h.persistent_world_state_unchanged,
    h.world_model_prediction_not_truth, h.world_mutation_not_granted,
    h.history_read_only, h.qi_grants_no_authority⟩

theorem decision_selection_is_not_plan_synthesis_or_execution
    (r : WorldConditionedSelectionJustificationReceipt)
    (h : WorldConditionedSelectionJustificationValid r) :
    r.selectionIsNotPlanSynthesis = true ∧
      r.selectionIsNotExecution = true ∧
      r.planSynthesisPerformed = false ∧
      r.futureOnly = true ∧ r.activeNow = false ∧
      r.executionPermission = false := by
  exact ⟨h.selection_not_plan_synthesis, h.selection_not_execution,
    h.plan_synthesis_not_performed, h.future_only,
    h.active_now_false, h.execution_permission_false⟩

end DecisionOS
end KUOS
