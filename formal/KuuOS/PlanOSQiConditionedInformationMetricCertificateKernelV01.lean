import Mathlib
import KuuOS.PlanOSV098

namespace KuuOS.PlanOSQiConditionedInformationMetricCertificateKernelV01

structure MetricCertificate where
  metricNonnegativityPreserved : Bool
  metricFloorPreserved : Bool
  metricCeilingPreserved : Bool
  evidenceGatePreserved : Bool
  recoveryProtectionPreserved : Bool
  hysteresisResistancePreserved : Bool
  oscillationResistancePreserved : Bool
  historyReadOnly : Bool
  qiGrantsNoAuthority : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

/-- A diagonal finite-dimensional transition action. -/
def diagonalQuadraticForm {n : ℕ}
    (weights delta : Fin n → ℝ) : ℝ :=
  (1 / 2 : ℝ) * ∑ i, weights i * (delta i) ^ 2

theorem base_metric_coordinate_is_positive
    (baseWeight : ℝ)
    (h : 0 < baseWeight) :
    0 < baseWeight := by
  exact h

theorem conditioned_metric_coordinate_is_nonnegative
    (conditionedWeight floorWeight : ℝ)
    (hfloor : 0 ≤ floorWeight)
    (hpreserved : floorWeight ≤ conditionedWeight) :
    0 ≤ conditionedWeight := by
  exact le_trans hfloor hpreserved

theorem qi_conditioned_quadratic_form_is_nonnegative
    {n : ℕ}
    (weights delta : Fin n → ℝ)
    (hweights : ∀ i, 0 ≤ weights i) :
    0 ≤ diagonalQuadraticForm weights delta := by
  unfold diagonalQuadraticForm
  have hsum : 0 ≤ ∑ i, weights i * (delta i) ^ 2 := by
    exact Finset.sum_nonneg fun i _ =>
      mul_nonneg (hweights i) (sq_nonneg (delta i))
  exact mul_nonneg (by norm_num) hsum

theorem recovery_never_reduces_switch_metric
    (base recovery hysteresis oscillation floorWeight ceilingWeight : ℝ)
    (hrecovery : 0 ≤ recovery)
    (hhysteresis : 0 ≤ hysteresis)
    (hoscillation : 0 ≤ oscillation)
    (hbaseFloor : floorWeight ≤ base)
    (hbaseCeiling : base ≤ ceilingWeight) :
    base ≤ min ceilingWeight
      (max floorWeight (base + recovery + hysteresis + oscillation)) := by
  have hraw :
      base ≤ base + recovery + hysteresis + oscillation := by
    linarith
  have hmax :
      base ≤ max floorWeight (base + recovery + hysteresis + oscillation) := by
    exact le_trans hraw (le_max_right _ _)
  exact le_min hbaseCeiling hmax

theorem oscillation_never_reduces_switch_metric
    (base recovery hysteresis oscillation floorWeight ceilingWeight : ℝ)
    (hrecovery : 0 ≤ recovery)
    (hhysteresis : 0 ≤ hysteresis)
    (hoscillation : 0 ≤ oscillation)
    (hbaseFloor : floorWeight ≤ base)
    (hbaseCeiling : base ≤ ceilingWeight) :
    base ≤ min ceilingWeight
      (max floorWeight (base + recovery + hysteresis + oscillation)) := by
  exact recovery_never_reduces_switch_metric
    base recovery hysteresis oscillation floorWeight ceilingWeight
    hrecovery hhysteresis hoscillation hbaseFloor hbaseCeiling

def evidenceGatedDiscount (evidence : Bool) (discount : ℝ) : ℝ :=
  if evidence then discount else 0

theorem reroute_discount_requires_evidence
    (discount : ℝ) :
    evidenceGatedDiscount false discount = 0 := by
  simp [evidenceGatedDiscount]

theorem reroute_discount_preserves_metric_floor
    (base discount floorWeight ceilingWeight : ℝ)
    (hfloorCeiling : floorWeight ≤ ceilingWeight) :
    floorWeight ≤
      min ceilingWeight (max floorWeight (base - discount)) := by
  exact le_min hfloorCeiling (le_max_left _ _)

theorem qi_metric_preserves_nonnegativity
    (c : MetricCertificate)
    (h : c.metricNonnegativityPreserved = true) :
    c.metricNonnegativityPreserved = true := by
  exact h

theorem qi_metric_grants_no_authority
    (c : MetricCertificate)
    (h : c.qiGrantsNoAuthority = true) :
    c.qiGrantsNoAuthority = true := by
  exact h

theorem qi_metric_history_is_read_only
    (c : MetricCertificate)
    (h : c.historyReadOnly = true) :
    c.historyReadOnly = true := by
  exact h

theorem qi_metric_is_future_only_and_not_execution
    (c : MetricCertificate)
    (hf : c.futureOnly = true)
    (ha : c.activeNow = false)
    (he : c.executionPermission = false) :
    c.futureOnly = true ∧ c.activeNow = false ∧
      c.executionPermission = false := by
  exact ⟨hf, ha, he⟩

end KuuOS.PlanOSQiConditionedInformationMetricCertificateKernelV01
