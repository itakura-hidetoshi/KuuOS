import Mathlib
import KuuOS.PlanOSV101

namespace KuuOS.PlanOSWorldConditionedDistributionDecisionHandoffCertificateKernelV01

structure DecisionHandoffCertificate where
  sourceDistributionPreserved : Prop
  rankingAdvisoryOnly : Prop
  candidateFieldRetained : Prop
  persistentWorldStateUnchanged : Prop
  worldModelPredictionNotTruth : Prop
  worldMutationNotGranted : Prop
  historyReadOnly : Prop
  qiGrantsNoAuthority : Prop
  decisionSelectionPerformed : Bool
  decisionAuthorityGranted : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

structure DecisionHandoffCertificateValid
    (c : DecisionHandoffCertificate) : Prop where
  source_distribution_preserved : c.sourceDistributionPreserved
  ranking_advisory_only : c.rankingAdvisoryOnly
  candidate_field_retained : c.candidateFieldRetained
  persistent_world_state_unchanged : c.persistentWorldStateUnchanged
  world_model_prediction_not_truth : c.worldModelPredictionNotTruth
  world_mutation_not_granted : c.worldMutationNotGranted
  history_read_only : c.historyReadOnly
  qi_grants_no_authority : c.qiGrantsNoAuthority
  decision_selection_not_performed : c.decisionSelectionPerformed = false
  decision_authority_not_granted : c.decisionAuthorityGranted = false
  future_only : c.futureOnly = true
  active_now_false : c.activeNow = false
  execution_permission_false : c.executionPermission = false

/-- Difference between the highest and runner-up candidate masses. -/
def leadMargin (topMass runnerUpMass : ℝ) : ℝ :=
  topMass - runnerUpMass

theorem lead_margin_nonnegative
    (topMass runnerUpMass : ℝ)
    (h : runnerUpMass ≤ topMass) :
    0 ≤ leadMargin topMass runnerUpMass := by
  dsimp [leadMargin]
  linarith

/-- Reciprocal concentration used as finite effective support. -/
def effectiveSupport (concentration : ℝ) : ℝ :=
  1 / concentration

theorem effective_support_positive
    (concentration : ℝ)
    (h : 0 < concentration) :
    0 < effectiveSupport concentration := by
  exact one_div_pos.mpr h

theorem handoff_preserves_source_distribution
    (c : DecisionHandoffCertificate)
    (h : DecisionHandoffCertificateValid c) :
    c.sourceDistributionPreserved := by
  exact h.source_distribution_preserved

theorem handoff_ranking_is_advisory_only
    (c : DecisionHandoffCertificate)
    (h : DecisionHandoffCertificateValid c) :
    c.rankingAdvisoryOnly := by
  exact h.ranking_advisory_only

theorem handoff_retains_candidate_field
    (c : DecisionHandoffCertificate)
    (h : DecisionHandoffCertificateValid c) :
    c.candidateFieldRetained := by
  exact h.candidate_field_retained

theorem handoff_does_not_select_or_grant_decision_authority
    (c : DecisionHandoffCertificate)
    (h : DecisionHandoffCertificateValid c) :
    c.decisionSelectionPerformed = false ∧
      c.decisionAuthorityGranted = false := by
  exact ⟨h.decision_selection_not_performed,
    h.decision_authority_not_granted⟩

theorem handoff_preserves_world_read_only_boundary
    (c : DecisionHandoffCertificate)
    (h : DecisionHandoffCertificateValid c) :
    c.persistentWorldStateUnchanged ∧
      c.worldModelPredictionNotTruth ∧
      c.worldMutationNotGranted := by
  exact ⟨h.persistent_world_state_unchanged,
    h.world_model_prediction_not_truth,
    h.world_mutation_not_granted⟩

theorem handoff_preserves_history_and_authority_boundary
    (c : DecisionHandoffCertificate)
    (h : DecisionHandoffCertificateValid c) :
    c.historyReadOnly ∧ c.qiGrantsNoAuthority := by
  exact ⟨h.history_read_only, h.qi_grants_no_authority⟩

theorem handoff_is_future_only_and_not_execution
    (c : DecisionHandoffCertificate)
    (h : DecisionHandoffCertificateValid c) :
    c.futureOnly = true ∧ c.activeNow = false ∧
      c.executionPermission = false := by
  exact ⟨h.future_only, h.active_now_false,
    h.execution_permission_false⟩

end KuuOS.PlanOSWorldConditionedDistributionDecisionHandoffCertificateKernelV01
