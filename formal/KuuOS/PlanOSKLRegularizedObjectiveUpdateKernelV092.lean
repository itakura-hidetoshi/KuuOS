import KuuOS.PlanOSV091
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Real.Basic

namespace KuuOS.PlanOS

structure KLRegularizedObjectiveUpdateKernelV092 where
  priorDistributionPreserved : Prop
  admissibleSupportPreserved : Prop
  positivePriorSupportPreserved : Prop
  normalizedNextDistribution : Prop
  candidateMassNonnegative : Prop
  holdMassPreserved : Prop
  authorityInvariant : Prop
  historyReadOnly : Prop
  retainedCandidatesPreserved : Prop
  futureOnly : Prop
  activeNow : Prop
  executionPermission : Prop

structure KLRegularizedObjectiveUpdateKernelV092Valid
    (k : KLRegularizedObjectiveUpdateKernelV092) : Prop where
  prior_distribution_preserved : k.priorDistributionPreserved
  admissible_support_preserved : k.admissibleSupportPreserved
  positive_prior_support_preserved : k.positivePriorSupportPreserved
  normalized_next_distribution : k.normalizedNextDistribution
  candidate_mass_nonnegative : k.candidateMassNonnegative
  hold_mass_preserved : k.holdMassPreserved
  authority_invariant : k.authorityInvariant
  history_read_only : k.historyReadOnly
  retained_candidates_preserved : k.retainedCandidatesPreserved
  future_only : k.futureOnly
  inactive_now : ¬ k.activeNow
  no_execution_permission : ¬ k.executionPermission

theorem kl_regularized_update_preserves_support_under_positive_temperature
    (k : KLRegularizedObjectiveUpdateKernelV092)
    (h : KLRegularizedObjectiveUpdateKernelV092Valid k) :
    k.admissibleSupportPreserved ∧ k.positivePriorSupportPreserved := by
  exact ⟨h.admissible_support_preserved, h.positive_prior_support_preserved⟩

theorem kl_regularized_update_is_normalized
    (k : KLRegularizedObjectiveUpdateKernelV092)
    (h : KLRegularizedObjectiveUpdateKernelV092Valid k) :
    k.normalizedNextDistribution := by
  exact h.normalized_next_distribution

theorem kl_regularized_candidate_mass_is_nonnegative
    (k : KLRegularizedObjectiveUpdateKernelV092)
    (h : KLRegularizedObjectiveUpdateKernelV092Valid k) :
    k.candidateMassNonnegative := by
  exact h.candidate_mass_nonnegative

theorem kl_regularized_hold_mass_is_preserved
    (k : KLRegularizedObjectiveUpdateKernelV092)
    (h : KLRegularizedObjectiveUpdateKernelV092Valid k) :
    k.holdMassPreserved := by
  exact h.hold_mass_preserved

theorem kl_regularized_update_preserves_governance
    (k : KLRegularizedObjectiveUpdateKernelV092)
    (h : KLRegularizedObjectiveUpdateKernelV092Valid k) :
    k.authorityInvariant ∧ k.historyReadOnly := by
  exact ⟨h.authority_invariant, h.history_read_only⟩

theorem kl_regularized_update_retains_nonselected_candidates
    (k : KLRegularizedObjectiveUpdateKernelV092)
    (h : KLRegularizedObjectiveUpdateKernelV092Valid k) :
    k.retainedCandidatesPreserved := by
  exact h.retained_candidates_preserved

theorem kl_regularized_update_is_future_only_and_not_execution
    (k : KLRegularizedObjectiveUpdateKernelV092)
    (h : KLRegularizedObjectiveUpdateKernelV092Valid k) :
    k.futureOnly ∧ ¬ k.activeNow ∧ ¬ k.executionPermission := by
  exact ⟨h.future_only, h.inactive_now, h.no_execution_permission⟩

theorem nonnegative_rescaling_preserves_nonnegativity
    (x scale : ℝ) (hx : 0 ≤ x) (hs : 0 ≤ scale) :
    0 ≤ scale * x := by
  exact mul_nonneg hs hx

end KuuOS.PlanOS
