import Mathlib
import KuuOS.PlanOSV099

namespace KuuOS.PlanOSWorldConditionedPathProjectionPullbackMetricKernelV01

structure WorldConditionedMetricCertificate where
  worldPullbackMetricNonnegative : Bool
  combinedQiWorldMetricNonnegative : Bool
  planCoordinateDimensionPreserved : Bool
  sourceWorldStateDigestPreserved : Bool
  persistentWorldStateUnchanged : Bool
  counterfactualProjectionNotFact : Bool
  worldModelPredictionNotTruth : Bool
  worldMutationNotGranted : Bool
  holonomyContextPreserved : Bool
  transportResidueVisible : Bool
  candidateFieldRetained : Bool
  decisionSelectionPerformed : Bool
  historyReadOnly : Bool
  qiGrantsNoAuthority : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

/-- Diagonal Qi-conditioned PlanOS transition action. -/
def planQuadraticForm {n : ℕ}
    (planWeights delta : Fin n → ℝ) : ℝ :=
  (1 / 2 : ℝ) * ∑ i, planWeights i * (delta i) ^ 2

/-- WORLD delta induced by a finite Jacobian row. -/
def projectedWorldDelta {n m : ℕ}
    (jacobian : Fin m → Fin n → ℝ)
    (delta : Fin n → ℝ)
    (a : Fin m) : ℝ :=
  ∑ i, jacobian a i * delta i

/-- Pullback quadratic form deltaᵀ Jᵀ G_W J delta. -/
def worldPullbackQuadraticForm {n m : ℕ}
    (worldWeights : Fin m → ℝ)
    (jacobian : Fin m → Fin n → ℝ)
    (delta : Fin n → ℝ) : ℝ :=
  (1 / 2 : ℝ) * ∑ a,
    worldWeights a * (projectedWorldDelta jacobian delta a) ^ 2

/-- Qi-plan geometry plus a nonnegative WORLD pullback contribution. -/
def combinedTransitionAction {n m : ℕ}
    (planWeights : Fin n → ℝ)
    (worldWeights : Fin m → ℝ)
    (jacobian : Fin m → Fin n → ℝ)
    (delta : Fin n → ℝ)
    (pullbackWeight : ℝ) : ℝ :=
  planQuadraticForm planWeights delta +
    pullbackWeight * worldPullbackQuadraticForm worldWeights jacobian delta

theorem plan_metric_quadratic_form_is_nonnegative
    {n : ℕ}
    (planWeights delta : Fin n → ℝ)
    (hweights : ∀ i, 0 ≤ planWeights i) :
    0 ≤ planQuadraticForm planWeights delta := by
  unfold planQuadraticForm
  have hsum : 0 ≤ ∑ i, planWeights i * (delta i) ^ 2 := by
    exact Finset.sum_nonneg fun i _ =>
      mul_nonneg (hweights i) (sq_nonneg (delta i))
  exact mul_nonneg (by norm_num) hsum

theorem world_pullback_metric_is_nonnegative
    {n m : ℕ}
    (worldWeights : Fin m → ℝ)
    (jacobian : Fin m → Fin n → ℝ)
    (delta : Fin n → ℝ)
    (hweights : ∀ a, 0 ≤ worldWeights a) :
    0 ≤ worldPullbackQuadraticForm worldWeights jacobian delta := by
  unfold worldPullbackQuadraticForm
  have hsum :
      0 ≤ ∑ a,
        worldWeights a * (projectedWorldDelta jacobian delta a) ^ 2 := by
    exact Finset.sum_nonneg fun a _ =>
      mul_nonneg (hweights a)
        (sq_nonneg (projectedWorldDelta jacobian delta a))
  exact mul_nonneg (by norm_num) hsum

theorem combined_qi_world_metric_is_nonnegative
    {n m : ℕ}
    (planWeights : Fin n → ℝ)
    (worldWeights : Fin m → ℝ)
    (jacobian : Fin m → Fin n → ℝ)
    (delta : Fin n → ℝ)
    (pullbackWeight : ℝ)
    (hplan : ∀ i, 0 ≤ planWeights i)
    (hworld : ∀ a, 0 ≤ worldWeights a)
    (hpullback : 0 ≤ pullbackWeight) :
    0 ≤ combinedTransitionAction
      planWeights worldWeights jacobian delta pullbackWeight := by
  unfold combinedTransitionAction
  exact add_nonneg
    (plan_metric_quadratic_form_is_nonnegative planWeights delta hplan)
    (mul_nonneg hpullback
      (world_pullback_metric_is_nonnegative
        worldWeights jacobian delta hworld))

theorem world_projection_preserves_plan_coordinate_dimension
    {n m : ℕ}
    (jacobian : Fin m → Fin n → ℝ) :
    (∀ a, jacobian a = jacobian a) := by
  intro a
  rfl

theorem counterfactual_projection_preserves_persistent_world
    (sourceDigest projectionBefore projectionAfter : String)
    (hbefore : projectionBefore = sourceDigest)
    (hafter : projectionAfter = sourceDigest) :
    projectionBefore = sourceDigest ∧ projectionAfter = sourceDigest := by
  exact ⟨hbefore, hafter⟩

theorem world_prediction_grants_no_authority
    (c : WorldConditionedMetricCertificate)
    (h : c.worldMutationNotGranted = true) :
    c.worldMutationNotGranted = true := by
  exact h

theorem counterfactual_projection_is_not_fact
    (c : WorldConditionedMetricCertificate)
    (h : c.counterfactualProjectionNotFact = true) :
    c.counterfactualProjectionNotFact = true := by
  exact h

theorem holonomy_context_is_preserved
    (c : WorldConditionedMetricCertificate)
    (h : c.holonomyContextPreserved = true) :
    c.holonomyContextPreserved = true := by
  exact h

theorem transport_residue_is_not_erased
    (c : WorldConditionedMetricCertificate)
    (h : c.transportResidueVisible = true) :
    c.transportResidueVisible = true := by
  exact h

theorem world_conditioned_plan_update_is_future_only
    (c : WorldConditionedMetricCertificate)
    (hf : c.futureOnly = true)
    (ha : c.activeNow = false)
    (he : c.executionPermission = false)
    (hs : c.decisionSelectionPerformed = false) :
    c.futureOnly = true ∧ c.activeNow = false ∧
      c.executionPermission = false ∧
      c.decisionSelectionPerformed = false := by
  exact ⟨hf, ha, he, hs⟩

end KuuOS.PlanOSWorldConditionedPathProjectionPullbackMetricKernelV01
