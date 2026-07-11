import Mathlib
import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

namespace KUOS.PlanOS.BoundedSynthesisReceiptV1_04

open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

inductive PlanActionClass where
  | analyze
  | conditionReassessment
  | evidenceCollection
  | hold
  | prepareReversible
  | requestRevision
  | reviewCheckpoint
  | terminate
  deriving DecidableEq, Repr

structure BoundedPlanStep where
  stepId : String
  sequenceIndex : Nat
  actionClass : PlanActionClass
  reversible : Bool
  irreversible : Bool
  checkpointPresent : Bool
  stopConditionsPresent : Bool
  forbiddenEffectsAbsent : Bool
  evidenceLineageBound : Bool
  deriving Repr

structure BoundedSynthesisReceipt where
  sourceDisposition : IntakeDisposition
  sourceDispositionReady :
    sourceDisposition = .boundedSynthesisIntakeReady
  planSteps : List BoundedPlanStep
  maximumPlanSteps : Nat
  planStepsNonempty : planSteps ≠ []
  stepCountBounded : planSteps.length ≤ maximumPlanSteps
  selectedCandidatePreserved : Bool
  planIntentBindingPreserved : Bool
  worldStateDependencyPreserved : Bool
  finitePlanConstructed : Bool
  branchingFactorBounded : Bool
  revisionCyclesBounded : Bool
  irreversibleStepsCheckpointGuarded : Bool
  stopConditionsPreserved : Bool
  forbiddenEffectsAbsent : Bool
  alternativeCandidatesRetained : Bool
  dissentEvidencePreserved : Bool
  minorityEvidencePreserved : Bool
  lineageExtendedNotReplaced : Bool
  responsibilityExtendedNotReplaced : Bool
  planIsConditionallyBinding : Bool
  planIsNotAbsoluteCommand : Bool
  planIsNotContentlessProposal : Bool
  selectionRemainsDecisionOSOwned : Bool
  selectionAuthorityGrantedToPlanOS : Bool
  planSynthesisPerformed : Bool
  concretePlanIssued : Bool
  planReceiptIssued : Bool
  planActivated : Bool
  materializationPerformed : Bool
  executionAuthorityGranted : Bool
  executionPermission : Bool
  persistentWorldStateChanged : Bool
  activeNow : Bool

structure BoundedSynthesisReceiptValid
    (receipt : BoundedSynthesisReceipt) : Prop where
  selected_candidate_preserved : receipt.selectedCandidatePreserved = true
  plan_intent_binding_preserved : receipt.planIntentBindingPreserved = true
  world_state_dependency_preserved :
    receipt.worldStateDependencyPreserved = true
  finite_plan_constructed : receipt.finitePlanConstructed = true
  branching_factor_bounded : receipt.branchingFactorBounded = true
  revision_cycles_bounded : receipt.revisionCyclesBounded = true
  irreversible_steps_checkpoint_guarded :
    receipt.irreversibleStepsCheckpointGuarded = true
  stop_conditions_preserved : receipt.stopConditionsPreserved = true
  forbidden_effects_absent : receipt.forbiddenEffectsAbsent = true
  alternative_candidates_retained : receipt.alternativeCandidatesRetained = true
  dissent_evidence_preserved : receipt.dissentEvidencePreserved = true
  minority_evidence_preserved : receipt.minorityEvidencePreserved = true
  lineage_extended_not_replaced : receipt.lineageExtendedNotReplaced = true
  responsibility_extended_not_replaced :
    receipt.responsibilityExtendedNotReplaced = true
  plan_is_conditionally_binding : receipt.planIsConditionallyBinding = true
  plan_is_not_absolute_command : receipt.planIsNotAbsoluteCommand = true
  plan_is_not_contentless_proposal :
    receipt.planIsNotContentlessProposal = true
  selection_remains_decisionos_owned :
    receipt.selectionRemainsDecisionOSOwned = true
  selection_authority_not_granted :
    receipt.selectionAuthorityGrantedToPlanOS = false
  plan_synthesis_performed : receipt.planSynthesisPerformed = true
  concrete_plan_issued : receipt.concretePlanIssued = true
  plan_receipt_issued : receipt.planReceiptIssued = true
  plan_not_activated : receipt.planActivated = false
  materialization_not_performed : receipt.materializationPerformed = false
  execution_authority_not_granted : receipt.executionAuthorityGranted = false
  execution_permission_false : receipt.executionPermission = false
  persistent_world_state_unchanged : receipt.persistentWorldStateChanged = false
  active_now_false : receipt.activeNow = false

theorem synthesis_requires_ready_middle_way_intake
    (receipt : BoundedSynthesisReceipt) :
    receipt.sourceDisposition = .boundedSynthesisIntakeReady := by
  exact receipt.sourceDispositionReady

theorem bounded_plan_is_nonempty
    (receipt : BoundedSynthesisReceipt) :
    receipt.planSteps ≠ [] := by
  exact receipt.planStepsNonempty

theorem bounded_plan_respects_step_limit
    (receipt : BoundedSynthesisReceipt) :
    receipt.planSteps.length ≤ receipt.maximumPlanSteps := by
  exact receipt.stepCountBounded

theorem synthesis_preserves_selected_candidate_and_plan_intent
    (receipt : BoundedSynthesisReceipt)
    (valid : BoundedSynthesisReceiptValid receipt) :
    receipt.selectedCandidatePreserved = true ∧
      receipt.planIntentBindingPreserved = true := by
  exact ⟨valid.selected_candidate_preserved,
    valid.plan_intent_binding_preserved⟩

theorem synthesis_preserves_world_dependency_and_bounds
    (receipt : BoundedSynthesisReceipt)
    (valid : BoundedSynthesisReceiptValid receipt) :
    receipt.worldStateDependencyPreserved = true ∧
      receipt.finitePlanConstructed = true ∧
      receipt.branchingFactorBounded = true ∧
      receipt.revisionCyclesBounded = true := by
  exact ⟨valid.world_state_dependency_preserved,
    valid.finite_plan_constructed,
    valid.branching_factor_bounded,
    valid.revision_cycles_bounded⟩

theorem irreversible_steps_require_checkpoint
    (receipt : BoundedSynthesisReceipt)
    (valid : BoundedSynthesisReceiptValid receipt) :
    receipt.irreversibleStepsCheckpointGuarded = true := by
  exact valid.irreversible_steps_checkpoint_guarded

theorem synthesis_preserves_stop_and_effect_boundaries
    (receipt : BoundedSynthesisReceipt)
    (valid : BoundedSynthesisReceiptValid receipt) :
    receipt.stopConditionsPreserved = true ∧
      receipt.forbiddenEffectsAbsent = true := by
  exact ⟨valid.stop_conditions_preserved,
    valid.forbidden_effects_absent⟩

theorem synthesis_preserves_alternatives_dissent_and_minority
    (receipt : BoundedSynthesisReceipt)
    (valid : BoundedSynthesisReceiptValid receipt) :
    receipt.alternativeCandidatesRetained = true ∧
      receipt.dissentEvidencePreserved = true ∧
      receipt.minorityEvidencePreserved = true := by
  exact ⟨valid.alternative_candidates_retained,
    valid.dissent_evidence_preserved,
    valid.minority_evidence_preserved⟩

theorem synthesis_extends_lineage_and_responsibility
    (receipt : BoundedSynthesisReceipt)
    (valid : BoundedSynthesisReceiptValid receipt) :
    receipt.lineageExtendedNotReplaced = true ∧
      receipt.responsibilityExtendedNotReplaced = true := by
  exact ⟨valid.lineage_extended_not_replaced,
    valid.responsibility_extended_not_replaced⟩

theorem synthesized_plan_remains_middle_way_conditioned
    (receipt : BoundedSynthesisReceipt)
    (valid : BoundedSynthesisReceiptValid receipt) :
    receipt.planIsConditionallyBinding = true ∧
      receipt.planIsNotAbsoluteCommand = true ∧
      receipt.planIsNotContentlessProposal = true := by
  exact ⟨valid.plan_is_conditionally_binding,
    valid.plan_is_not_absolute_command,
    valid.plan_is_not_contentless_proposal⟩

theorem plan_synthesis_does_not_inherit_selection_authority
    (receipt : BoundedSynthesisReceipt)
    (valid : BoundedSynthesisReceiptValid receipt) :
    receipt.selectionRemainsDecisionOSOwned = true ∧
      receipt.selectionAuthorityGrantedToPlanOS = false := by
  exact ⟨valid.selection_remains_decisionos_owned,
    valid.selection_authority_not_granted⟩

theorem receipt_issues_plan_without_activation_or_execution
    (receipt : BoundedSynthesisReceipt)
    (valid : BoundedSynthesisReceiptValid receipt) :
    receipt.planSynthesisPerformed = true ∧
      receipt.concretePlanIssued = true ∧
      receipt.planReceiptIssued = true ∧
      receipt.planActivated = false ∧
      receipt.materializationPerformed = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.executionPermission = false ∧
      receipt.persistentWorldStateChanged = false ∧
      receipt.activeNow = false := by
  exact ⟨valid.plan_synthesis_performed,
    valid.concrete_plan_issued,
    valid.plan_receipt_issued,
    valid.plan_not_activated,
    valid.materialization_not_performed,
    valid.execution_authority_not_granted,
    valid.execution_permission_false,
    valid.persistent_world_state_unchanged,
    valid.active_now_false⟩

end KUOS.PlanOS.BoundedSynthesisReceiptV1_04
