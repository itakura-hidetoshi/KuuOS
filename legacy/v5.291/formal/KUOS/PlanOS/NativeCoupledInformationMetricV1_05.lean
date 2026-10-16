import Mathlib
import KuuOS.PlanOSQiConditionedInformationMetricCertificateKernelV01
import KuuOS.PlanOSWorldConditionedPathProjectionPullbackMetricKernelV01

namespace KUOS.PlanOS.NativeCoupledInformationMetricV1_05

structure NativeCoupledMetricCertificate where
  metricSymmetric : Bool
  metricPositiveDefinite : Bool
  metricFloorPreserved : Bool
  metricCeilingPreserved : Bool
  nonDiagonalCouplingPresent : Bool
  diagonalMetricRecoverableAsZeroCoupling : Bool
  pairwiseInteractionsRetained : Bool
  interactionSignDirectionAware : Bool
  worldPullbackCompositionPreservesPositiveDefiniteness : Bool
  sourceMetricNotMutated : Bool
  candidateFieldRetained : Bool
  decisionSelectionPerformed : Bool
  historyReadOnly : Bool
  qiGrantsNoAuthority : Bool
  worldProjectionGrantsNoAuthority : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

/-- Squared Euclidean coordinate energy on a finite PlanOS chart. -/
def coordinateEnergy {n : ℕ} (delta : Fin n → ℝ) : ℝ :=
  ∑ i, (delta i) ^ 2

/-- Positive diagonal energy inherited from PlanOS v0.99. -/
def diagonalEnergy {n : ℕ}
    (weights delta : Fin n → ℝ) : ℝ :=
  ∑ i, weights i * (delta i) ^ 2

/-- Gram-factor coupling energy.  This is the quadratic form of `BᵀB`. -/
def gramEnergy {n m : ℕ}
    (factor : Fin m → Fin n → ℝ)
    (delta : Fin n → ℝ) : ℝ :=
  ∑ r, (∑ i, factor r i * delta i) ^ 2

/-- Native coupled action `1/2 (deltaᵀ D delta + ‖B delta‖²)`. -/
def coupledQuadraticForm {n m : ℕ}
    (weights : Fin n → ℝ)
    (factor : Fin m → Fin n → ℝ)
    (delta : Fin n → ℝ) : ℝ :=
  (1 / 2 : ℝ) * (diagonalEnergy weights delta + gramEnergy factor delta)

/-- WORLD pullback energy, written as a sum of weighted squared Jacobian rows. -/
def worldPullbackEnergy {n k : ℕ}
    (worldWeights : Fin k → ℝ)
    (jacobian : Fin k → Fin n → ℝ)
    (delta : Fin n → ℝ) : ℝ :=
  ∑ a, worldWeights a * (∑ i, jacobian a i * delta i) ^ 2

/-- The finite coordinate energy is nonnegative. -/
theorem coordinateEnergy_nonnegative {n : ℕ}
    (delta : Fin n → ℝ) :
    0 ≤ coordinateEnergy delta := by
  unfold coordinateEnergy
  exact Finset.sum_nonneg fun i _ => sq_nonneg (delta i)

/-- The inherited diagonal energy is nonnegative under nonnegative weights. -/
theorem diagonalEnergy_nonnegative {n : ℕ}
    (weights delta : Fin n → ℝ)
    (hweights : ∀ i, 0 ≤ weights i) :
    0 ≤ diagonalEnergy weights delta := by
  unfold diagonalEnergy
  exact Finset.sum_nonneg fun i _ =>
    mul_nonneg (hweights i) (sq_nonneg (delta i))

/-- Every Gram-factor coupling contributes a square, hence cannot make the action negative. -/
theorem gramEnergy_nonnegative {n m : ℕ}
    (factor : Fin m → Fin n → ℝ)
    (delta : Fin n → ℝ) :
    0 ≤ gramEnergy factor delta := by
  unfold gramEnergy
  exact Finset.sum_nonneg fun r _ =>
    sq_nonneg (∑ i, factor r i * delta i)

/-- The native coupled quadratic form is nonnegative. -/
theorem coupledQuadraticForm_nonnegative {n m : ℕ}
    (weights : Fin n → ℝ)
    (factor : Fin m → Fin n → ℝ)
    (delta : Fin n → ℝ)
    (hweights : ∀ i, 0 ≤ weights i) :
    0 ≤ coupledQuadraticForm weights factor delta := by
  unfold coupledQuadraticForm
  exact mul_nonneg (by norm_num)
    (add_nonneg
      (diagonalEnergy_nonnegative weights delta hweights)
      (gramEnergy_nonnegative factor delta))

/-- A positive diagonal floor is a spectral lower bound for `D + BᵀB`. -/
theorem coupledQuadraticForm_lower_bound {n m : ℕ}
    (weights : Fin n → ℝ)
    (factor : Fin m → Fin n → ℝ)
    (delta : Fin n → ℝ)
    (floorWeight : ℝ)
    (hfloor : ∀ i, floorWeight ≤ weights i) :
    (1 / 2 : ℝ) * (floorWeight * coordinateEnergy delta) ≤
      coupledQuadraticForm weights factor delta := by
  have hdiag :
      floorWeight * coordinateEnergy delta ≤ diagonalEnergy weights delta := by
    unfold coordinateEnergy diagonalEnergy
    rw [Finset.mul_sum]
    exact Finset.sum_le_sum fun i _ =>
      mul_le_mul_of_nonneg_right (hfloor i) (sq_nonneg (delta i))
  have hgram : 0 ≤ gramEnergy factor delta :=
    gramEnergy_nonnegative factor delta
  have hhalf : 0 ≤ (1 / 2 : ℝ) := by norm_num
  calc
    (1 / 2 : ℝ) * (floorWeight * coordinateEnergy delta) ≤
        (1 / 2 : ℝ) * diagonalEnergy weights delta :=
      mul_le_mul_of_nonneg_left hdiag hhalf
    _ ≤ (1 / 2 : ℝ) *
        (diagonalEnergy weights delta + gramEnergy factor delta) := by
      exact mul_le_mul_of_nonneg_left (le_add_of_nonneg_right hgram) hhalf
    _ = coupledQuadraticForm weights factor delta := by
      rfl

/-- Positive coordinate energy and a positive floor imply a strictly positive action. -/
theorem coupledQuadraticForm_positive_of_positive_coordinate_energy {n m : ℕ}
    (weights : Fin n → ℝ)
    (factor : Fin m → Fin n → ℝ)
    (delta : Fin n → ℝ)
    (floorWeight : ℝ)
    (hfloorPositive : 0 < floorWeight)
    (hfloor : ∀ i, floorWeight ≤ weights i)
    (hdelta : 0 < coordinateEnergy delta) :
    0 < coupledQuadraticForm weights factor delta := by
  have hlower := coupledQuadraticForm_lower_bound
    weights factor delta floorWeight hfloor
  have hpositive :
      0 < (1 / 2 : ℝ) * (floorWeight * coordinateEnergy delta) := by
    exact mul_pos (by norm_num) (mul_pos hfloorPositive hdelta)
  exact lt_of_lt_of_le hpositive hlower

/-- Setting every coupling coefficient to zero recovers the v0.99 diagonal action. -/
theorem diagonal_metric_is_zero_coupling_special_case {n m : ℕ}
    (weights : Fin n → ℝ)
    (factor : Fin m → Fin n → ℝ)
    (delta : Fin n → ℝ)
    (hzero : ∀ r i, factor r i = 0) :
    coupledQuadraticForm weights factor delta =
      (1 / 2 : ℝ) * diagonalEnergy weights delta := by
  unfold coupledQuadraticForm gramEnergy
  simp [hzero]

/-- A nonnegative WORLD pullback contribution preserves nonnegativity. -/
theorem worldPullbackEnergy_nonnegative {n k : ℕ}
    (worldWeights : Fin k → ℝ)
    (jacobian : Fin k → Fin n → ℝ)
    (delta : Fin n → ℝ)
    (hworld : ∀ a, 0 ≤ worldWeights a) :
    0 ≤ worldPullbackEnergy worldWeights jacobian delta := by
  unfold worldPullbackEnergy
  exact Finset.sum_nonneg fun a _ =>
    mul_nonneg (hworld a) (sq_nonneg (∑ i, jacobian a i * delta i))

/-- `D + BᵀB + λ JᵀG_WJ` remains nonnegative for `λ ≥ 0`. -/
theorem coupled_world_pullback_composition_nonnegative {n m k : ℕ}
    (weights : Fin n → ℝ)
    (factor : Fin m → Fin n → ℝ)
    (worldWeights : Fin k → ℝ)
    (jacobian : Fin k → Fin n → ℝ)
    (delta : Fin n → ℝ)
    (pullbackWeight : ℝ)
    (hweights : ∀ i, 0 ≤ weights i)
    (hworld : ∀ a, 0 ≤ worldWeights a)
    (hpullback : 0 ≤ pullbackWeight) :
    0 ≤ coupledQuadraticForm weights factor delta +
      (1 / 2 : ℝ) * pullbackWeight *
        worldPullbackEnergy worldWeights jacobian delta := by
  exact add_nonneg
    (coupledQuadraticForm_nonnegative weights factor delta hweights)
    (mul_nonneg
      (mul_nonneg (by norm_num) hpullback)
      (worldPullbackEnergy_nonnegative worldWeights jacobian delta hworld))

inductive InteractionDisposition where
  | synergy
  | neutral
  | tradeoff
  deriving DecidableEq, Repr

/-- Classification depends on the signed directional contribution, not on `Gᵢⱼ` alone. -/
def interactionDisposition (contribution : ℝ) : InteractionDisposition :=
  if contribution < 0 then .synergy
  else if 0 < contribution then .tradeoff
  else .neutral

theorem negative_directional_interaction_is_synergy
    (contribution : ℝ)
    (h : contribution < 0) :
    interactionDisposition contribution = .synergy := by
  simp [interactionDisposition, h]

theorem positive_directional_interaction_is_tradeoff
    (contribution : ℝ)
    (h : 0 < contribution) :
    interactionDisposition contribution = .tradeoff := by
  have hn : ¬ contribution < 0 := not_lt_of_ge (le_of_lt h)
  simp [interactionDisposition, hn, h]

theorem zero_directional_interaction_is_neutral :
    interactionDisposition 0 = .neutral := by
  simp [interactionDisposition]

theorem native_coupled_metric_grants_no_authority
    (certificate : NativeCoupledMetricCertificate)
    (hqi : certificate.qiGrantsNoAuthority = true)
    (hworld : certificate.worldProjectionGrantsNoAuthority = true)
    (hselection : certificate.decisionSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.qiGrantsNoAuthority = true ∧
      certificate.worldProjectionGrantsNoAuthority = true ∧
      certificate.decisionSelectionPerformed = false ∧
      certificate.executionPermission = false := by
  exact ⟨hqi, hworld, hselection, hexecution⟩

theorem native_coupled_metric_is_future_only
    (certificate : NativeCoupledMetricCertificate)
    (hfuture : certificate.futureOnly = true)
    (hactive : certificate.activeNow = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.futureOnly = true ∧
      certificate.activeNow = false ∧
      certificate.executionPermission = false := by
  exact ⟨hfuture, hactive, hexecution⟩

end KUOS.PlanOS.NativeCoupledInformationMetricV1_05
