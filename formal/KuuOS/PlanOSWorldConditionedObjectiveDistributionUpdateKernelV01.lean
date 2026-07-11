import Mathlib
import KuuOS.PlanOSV100

namespace KuuOS.PlanOSWorldConditionedObjectiveDistributionUpdateKernelV01

structure DistributionUpdateCertificate where
  sourceWorldActionBundlePreserved : Prop
  normalizedNextDistribution : Prop
  candidateMassNonnegative : Prop
  admissibleSupportPreserved : Prop
  positivePriorSupportPreserved : Prop
  holdMassPreserved : Prop
  candidateFieldRetained : Prop
  nonadmissibleCandidatesZeroMass : Prop
  persistentWorldStateUnchanged : Prop
  worldModelPredictionNotTruth : Prop
  worldMutationNotGranted : Prop
  historyReadOnly : Prop
  qiGrantsNoAuthority : Prop
  decisionSelectionPerformed : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

structure DistributionUpdateCertificateValid
    (c : DistributionUpdateCertificate) : Prop where
  source_world_action_bundle_preserved : c.sourceWorldActionBundlePreserved
  normalized_next_distribution : c.normalizedNextDistribution
  candidate_mass_nonnegative : c.candidateMassNonnegative
  admissible_support_preserved : c.admissibleSupportPreserved
  positive_prior_support_preserved : c.positivePriorSupportPreserved
  hold_mass_preserved : c.holdMassPreserved
  candidate_field_retained : c.candidateFieldRetained
  nonadmissible_candidates_zero_mass : c.nonadmissibleCandidatesZeroMass
  persistent_world_state_unchanged : c.persistentWorldStateUnchanged
  world_model_prediction_not_truth : c.worldModelPredictionNotTruth
  world_mutation_not_granted : c.worldMutationNotGranted
  history_read_only : c.historyReadOnly
  qi_grants_no_authority : c.qiGrantsNoAuthority
  decision_selection_not_performed : c.decisionSelectionPerformed = false
  future_only : c.futureOnly = true
  active_now_false : c.activeNow = false
  execution_permission_false : c.executionPermission = false

/-- Positive-temperature WORLD-conditioned Gibbs factor. -/
def worldConditionedGibbsFactor
    (beta action temperature : ℝ) : ℝ :=
  Real.exp (-beta * action / temperature)

theorem world_conditioned_gibbs_factor_positive
    (beta action temperature : ℝ) :
    0 < worldConditionedGibbsFactor beta action temperature := by
  exact Real.exp_pos _

theorem world_conditioned_raw_weight_nonnegative
    (priorPower beta action temperature : ℝ)
    (hprior : 0 ≤ priorPower) :
    0 ≤ priorPower * worldConditionedGibbsFactor beta action temperature := by
  exact mul_nonneg hprior (le_of_lt (world_conditioned_gibbs_factor_positive
    beta action temperature))

theorem world_conditioned_distribution_is_normalized
    (c : DistributionUpdateCertificate)
    (h : DistributionUpdateCertificateValid c) :
    c.normalizedNextDistribution := by
  exact h.normalized_next_distribution

theorem world_conditioned_candidate_mass_is_nonnegative
    (c : DistributionUpdateCertificate)
    (h : DistributionUpdateCertificateValid c) :
    c.candidateMassNonnegative := by
  exact h.candidate_mass_nonnegative

theorem world_conditioned_admissible_support_is_preserved
    (c : DistributionUpdateCertificate)
    (h : DistributionUpdateCertificateValid c) :
    c.admissibleSupportPreserved ∧ c.positivePriorSupportPreserved := by
  exact ⟨h.admissible_support_preserved,
    h.positive_prior_support_preserved⟩

theorem world_conditioned_hold_mass_is_preserved
    (c : DistributionUpdateCertificate)
    (h : DistributionUpdateCertificateValid c) :
    c.holdMassPreserved := by
  exact h.hold_mass_preserved

theorem world_conditioned_candidate_field_is_retained
    (c : DistributionUpdateCertificate)
    (h : DistributionUpdateCertificateValid c) :
    c.candidateFieldRetained ∧ c.nonadmissibleCandidatesZeroMass := by
  exact ⟨h.candidate_field_retained,
    h.nonadmissible_candidates_zero_mass⟩

theorem world_conditioned_update_does_not_select
    (c : DistributionUpdateCertificate)
    (h : DistributionUpdateCertificateValid c) :
    c.decisionSelectionPerformed = false := by
  exact h.decision_selection_not_performed

theorem world_conditioned_update_preserves_world_read_only_boundary
    (c : DistributionUpdateCertificate)
    (h : DistributionUpdateCertificateValid c) :
    c.persistentWorldStateUnchanged ∧
      c.worldModelPredictionNotTruth ∧
      c.worldMutationNotGranted := by
  exact ⟨h.persistent_world_state_unchanged,
    h.world_model_prediction_not_truth,
    h.world_mutation_not_granted⟩

theorem world_conditioned_update_preserves_history_and_authority
    (c : DistributionUpdateCertificate)
    (h : DistributionUpdateCertificateValid c) :
    c.historyReadOnly ∧ c.qiGrantsNoAuthority := by
  exact ⟨h.history_read_only, h.qi_grants_no_authority⟩

theorem world_conditioned_update_is_future_only_and_not_execution
    (c : DistributionUpdateCertificate)
    (h : DistributionUpdateCertificateValid c) :
    c.futureOnly = true ∧ c.activeNow = false ∧
      c.executionPermission = false := by
  exact ⟨h.future_only, h.active_now_false,
    h.execution_permission_false⟩

end KuuOS.PlanOSWorldConditionedObjectiveDistributionUpdateKernelV01
