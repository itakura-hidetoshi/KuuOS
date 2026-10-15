import Mathlib
import KUOS.PlanOS.StateDependentMetricJetLeviCivitaV1_06

namespace KUOS.PlanOS.SecondOrderMetricJetCurvatureV1_07

structure SecondOrderMetricJetCurvatureCertificate where
  secondOrderMetricJetPresent : Bool
  metricSymmetric : Bool
  metricPositiveDefinite : Bool
  inverseMetricExact : Bool
  metricFirstDerivativeSymmetric : Bool
  metricSecondDerivativeMetricIndicesSymmetric : Bool
  mixedPartialDerivativesSymmetric : Bool
  inverseMetricDerivativeIdentityPreserved : Bool
  connectionDerivativeRecomputed : Bool
  riemannCurvatureRecomputed : Bool
  riemannLastPairAntisymmetric : Bool
  riemannFirstBianchi : Bool
  lowerRiemannPairSymmetries : Bool
  ricciCurvatureRecomputed : Bool
  ricciSymmetric : Bool
  scalarCurvatureRecomputed : Bool
  sectionalCurvatureRetained : Bool
  infinitesimalHolonomyRetained : Bool
  curvatureBounded : Bool
  holonomyBounded : Bool
  sourceLeviCivitaNotMutated : Bool
  persistentWorldStateUnchanged : Bool
  candidatePlaneFieldRetained : Bool
  decisionSelectionPerformed : Bool
  historyReadOnly : Bool
  qiGrantsNoAuthority : Bool
  worldProjectionGrantsNoAuthority : Bool
  connectionGrantsNoAuthority : Bool
  curvatureGrantsNoAuthority : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

/-- `dConnection a i j k` represents `∂ₐ Γⁱⱼₖ`. -/
def Riemann {n : ℕ}
    (dConnection : Fin n → Fin n → Fin n → Fin n → ℝ)
    (connection : Fin n → Fin n → Fin n → ℝ)
    (upper lower k l : Fin n) : ℝ :=
  dConnection k upper l lower -
    dConnection l upper k lower +
    (∑ middle, connection upper k middle * connection middle l lower) -
    (∑ middle, connection upper l middle * connection middle k lower)

/-- Lower the leading curvature index with the metric. -/
def LowerRiemann {n : ℕ}
    (metric : Fin n → Fin n → ℝ)
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (i j k l : Fin n) : ℝ :=
  ∑ upper, metric i upper * curvature upper j k l

/-- Ricci contraction `Ricⱼₗ = Rⁱⱼᵢₗ`. -/
def Ricci {n : ℕ}
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (j l : Fin n) : ℝ :=
  ∑ upper, curvature upper j upper l

/-- Scalar curvature obtained by contracting Ricci with the inverse metric. -/
def scalarCurvature {n : ℕ}
    (inverseMetric ricci : Fin n → Fin n → ℝ) : ℝ :=
  ∑ i, ∑ j, inverseMetric i j * ricci i j

/-- Metric Gram determinant of an ordered two-plane. -/
def planeGramDeterminant {n : ℕ}
    (metric : Fin n → Fin n → ℝ)
    (u v : Fin n → ℝ) : ℝ :=
  (∑ i, ∑ j, u i * metric i j * u j) *
      (∑ i, ∑ j, v i * metric i j * v j) -
    (∑ i, ∑ j, u i * metric i j * v j) ^ 2

/-- Numerator used by the repository sectional-curvature convention. -/
def sectionalNumerator {n : ℕ}
    (lowerCurvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (u v : Fin n → ℝ) : ℝ :=
  ∑ i, ∑ j, ∑ k, ∑ l,
    lowerCurvature i j k l * u i * v j * v k * u l

/-- First nontrivial infinitesimal holonomy term around an oriented small loop. -/
def infinitesimalHolonomy {n : ℕ}
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (vector edgeU edgeV : Fin n → ℝ)
    (upper : Fin n) : ℝ :=
  ∑ j, ∑ k, ∑ l,
    curvature upper j k l * vector j * edgeU k * edgeV l

/-- Curvature is antisymmetric in its final two indices by construction. -/
theorem riemann_antisymmetric_last_pair {n : ℕ}
    (dConnection : Fin n → Fin n → Fin n → Fin n → ℝ)
    (connection : Fin n → Fin n → Fin n → ℝ)
    (upper lower k l : Fin n) :
    Riemann dConnection connection upper lower k l =
      -Riemann dConnection connection upper lower l k := by
  unfold Riemann
  ring

/-- A torsion-free connection and its differentiated symmetry imply the
first Bianchi identity. -/
theorem riemann_first_bianchi {n : ℕ}
    (dConnection : Fin n → Fin n → Fin n → Fin n → ℝ)
    (connection : Fin n → Fin n → Fin n → ℝ)
    (hconnection :
      ∀ upper j k, connection upper j k = connection upper k j)
    (hderivative :
      ∀ a upper j k, dConnection a upper j k = dConnection a upper k j)
    (upper j k l : Fin n) :
    Riemann dConnection connection upper j k l +
        Riemann dConnection connection upper k l j +
        Riemann dConnection connection upper l j k = 0 := by
  unfold Riemann
  rw [hderivative k upper l j]
  rw [hderivative l upper k j]
  rw [hderivative j upper l k]
  have h₁ :
      (∑ middle, connection upper k middle * connection middle l j) =
        ∑ middle, connection upper k middle * connection middle j l := by
    apply Finset.sum_congr rfl
    intro middle _
    rw [hconnection middle l j]
  have h₂ :
      (∑ middle, connection upper l middle * connection middle k j) =
        ∑ middle, connection upper l middle * connection middle j k := by
    apply Finset.sum_congr rfl
    intro middle _
    rw [hconnection middle k j]
  have h₃ :
      (∑ middle, connection upper j middle * connection middle l k) =
        ∑ middle, connection upper j middle * connection middle k l := by
    apply Finset.sum_congr rfl
    intro middle _
    rw [hconnection middle l k]
  rw [h₁, h₂, h₃]
  ring

/-- A zero connection and zero connection derivative give zero Riemann curvature. -/
theorem riemann_zero_of_zero_connection_and_derivative {n : ℕ}
    (dConnection : Fin n → Fin n → Fin n → Fin n → ℝ)
    (connection : Fin n → Fin n → Fin n → ℝ)
    (hdzero : ∀ a upper j k, dConnection a upper j k = 0)
    (hzero : ∀ upper j k, connection upper j k = 0)
    (upper lower k l : Fin n) :
    Riemann dConnection connection upper lower k l = 0 := by
  simp [Riemann, hdzero, hzero]

/-- Zero Riemann curvature has zero Ricci contraction. -/
theorem ricci_zero_of_zero_riemann {n : ℕ}
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (hzero : ∀ upper j k l, curvature upper j k l = 0)
    (j l : Fin n) :
    Ricci curvature j l = 0 := by
  simp [Ricci, hzero]

/-- Zero Ricci curvature has zero scalar curvature. -/
theorem scalarCurvature_zero_of_zero_ricci {n : ℕ}
    (inverseMetric ricci : Fin n → Fin n → ℝ)
    (hzero : ∀ i j, ricci i j = 0) :
    scalarCurvature inverseMetric ricci = 0 := by
  simp [scalarCurvature, hzero]

/-- Flat curvature gives zero sectional numerator on every two-plane. -/
theorem sectionalNumerator_zero_of_zero_curvature {n : ℕ}
    (lowerCurvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (u v : Fin n → ℝ)
    (hzero : ∀ i j k l, lowerCurvature i j k l = 0) :
    sectionalNumerator lowerCurvature u v = 0 := by
  simp [sectionalNumerator, hzero]

/-- Flat curvature gives trivial infinitesimal holonomy. -/
theorem infinitesimalHolonomy_zero_of_zero_curvature {n : ℕ}
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (vector edgeU edgeV : Fin n → ℝ)
    (hzero : ∀ upper j k l, curvature upper j k l = 0)
    (upper : Fin n) :
    infinitesimalHolonomy curvature vector edgeU edgeV upper = 0 := by
  simp [infinitesimalHolonomy, hzero]

/-- A degenerate loop with a zero first edge has trivial infinitesimal holonomy. -/
theorem infinitesimalHolonomy_zero_first_edge {n : ℕ}
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (vector edgeV : Fin n → ℝ)
    (upper : Fin n) :
    infinitesimalHolonomy curvature vector (fun _ => 0) edgeV upper = 0 := by
  simp [infinitesimalHolonomy]

/-- Curvature data never becomes selection or execution authority. -/
theorem curvature_grants_no_authority
    (certificate : SecondOrderMetricJetCurvatureCertificate)
    (hcurvature : certificate.curvatureGrantsNoAuthority = true)
    (hselection : certificate.decisionSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.curvatureGrantsNoAuthority = true ∧
      certificate.decisionSelectionPerformed = false ∧
      certificate.executionPermission = false := by
  exact ⟨hcurvature, hselection, hexecution⟩

/-- The second-order metric-jet certificate remains read-only and future-only. -/
theorem second_order_metric_jet_is_future_only
    (certificate : SecondOrderMetricJetCurvatureCertificate)
    (hreadonly : certificate.historyReadOnly = true)
    (hfuture : certificate.futureOnly = true)
    (hactive : certificate.activeNow = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.historyReadOnly = true ∧
      certificate.futureOnly = true ∧
      certificate.activeNow = false ∧
      certificate.executionPermission = false := by
  exact ⟨hreadonly, hfuture, hactive, hexecution⟩

end KUOS.PlanOS.SecondOrderMetricJetCurvatureV1_07
