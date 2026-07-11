import KuuOS.PlanOSV090
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Real.Basic

namespace KuuOS.PlanOS

structure InformationGeometricQiObjectiveKernelV01 where
  qiMetricNonnegative : Prop
  authorityForbiddenPathsZeroMass : Prop
  normalizedPathMass : Prop
  candidateMassNonnegative : Prop
  holdMassPreserved : Prop
  historyReadOnly : Prop
  qiGrantsNoAuthority : Prop
  selectedCandidateInField : Prop
  retainedCandidatesSurviveSelection : Prop
  futureOnlyUpdate : Prop
  currentCyclePreserved : Prop
  planCommitNotExecution : Prop

structure InformationGeometricQiObjectiveKernelV01Valid
    (k : InformationGeometricQiObjectiveKernelV01) : Prop where
  qi_metric_nonnegative : k.qiMetricNonnegative
  authority_forbidden_paths_zero_mass : k.authorityForbiddenPathsZeroMass
  normalized_path_mass : k.normalizedPathMass
  candidate_mass_nonnegative : k.candidateMassNonnegative
  hold_mass_preserved : k.holdMassPreserved
  history_read_only : k.historyReadOnly
  qi_grants_no_authority : k.qiGrantsNoAuthority
  selected_candidate_in_field : k.selectedCandidateInField
  retained_candidates_survive_selection : k.retainedCandidatesSurviveSelection
  future_only_update : k.futureOnlyUpdate
  current_cycle_preserved : k.currentCyclePreserved
  plan_commit_not_execution : k.planCommitNotExecution

theorem qi_metric_preserves_nonnegativity
    (k : InformationGeometricQiObjectiveKernelV01)
    (h : InformationGeometricQiObjectiveKernelV01Valid k) :
    k.qiMetricNonnegative := by
  exact h.qi_metric_nonnegative

theorem authority_forbidden_paths_have_zero_mass
    (k : InformationGeometricQiObjectiveKernelV01)
    (h : InformationGeometricQiObjectiveKernelV01Valid k) :
    k.authorityForbiddenPathsZeroMass := by
  exact h.authority_forbidden_paths_zero_mass

theorem normalized_path_mass_sums_to_one
    (k : InformationGeometricQiObjectiveKernelV01)
    (h : InformationGeometricQiObjectiveKernelV01Valid k) :
    k.normalizedPathMass := by
  exact h.normalized_path_mass

theorem candidate_mass_is_nonnegative
    (k : InformationGeometricQiObjectiveKernelV01)
    (h : InformationGeometricQiObjectiveKernelV01Valid k) :
    k.candidateMassNonnegative := by
  exact h.candidate_mass_nonnegative

theorem hold_mass_is_preserved
    (k : InformationGeometricQiObjectiveKernelV01)
    (h : InformationGeometricQiObjectiveKernelV01Valid k) :
    k.holdMassPreserved := by
  exact h.hold_mass_preserved

theorem history_conditioning_is_read_only
    (k : InformationGeometricQiObjectiveKernelV01)
    (h : InformationGeometricQiObjectiveKernelV01Valid k) :
    k.historyReadOnly := by
  exact h.history_read_only

theorem qi_conditioning_grants_no_authority
    (k : InformationGeometricQiObjectiveKernelV01)
    (h : InformationGeometricQiObjectiveKernelV01Valid k) :
    k.qiGrantsNoAuthority := by
  exact h.qi_grants_no_authority

theorem selected_candidate_belongs_to_candidate_field
    (k : InformationGeometricQiObjectiveKernelV01)
    (h : InformationGeometricQiObjectiveKernelV01Valid k) :
    k.selectedCandidateInField := by
  exact h.selected_candidate_in_field

theorem retained_candidates_survive_selection
    (k : InformationGeometricQiObjectiveKernelV01)
    (h : InformationGeometricQiObjectiveKernelV01Valid k) :
    k.retainedCandidatesSurviveSelection := by
  exact h.retained_candidates_survive_selection

theorem future_only_update_preserves_current_cycle
    (k : InformationGeometricQiObjectiveKernelV01)
    (h : InformationGeometricQiObjectiveKernelV01Valid k) :
    k.futureOnlyUpdate ∧ k.currentCyclePreserved := by
  exact ⟨h.future_only_update, h.current_cycle_preserved⟩

theorem plan_commit_is_not_execution
    (k : InformationGeometricQiObjectiveKernelV01)
    (h : InformationGeometricQiObjectiveKernelV01Valid k) :
    k.planCommitNotExecution := by
  exact h.plan_commit_not_execution

structure FinitePathMass (α : Type) where
  mass : α → ℝ
  nonnegative : ∀ a, 0 ≤ mass a

structure NormalizedFinitePathMass (α : Type) [Fintype α] extends FinitePathMass α where
  normalized : Finset.univ.sum mass = 1

theorem finite_candidate_mass_nonnegative
    {α : Type} [Fintype α]
    (p : NormalizedFinitePathMass α)
    (S : Finset α) :
    0 ≤ S.sum p.mass := by
  exact Finset.sum_nonneg fun i _ => p.nonnegative i

end KuuOS.PlanOS
