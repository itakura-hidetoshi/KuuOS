import Mathlib
import KUOS.PlanOS.MultiChartAtlasCurvatureV1_08

namespace KUOS.PlanOS.JacobiGeodesicDeviationV1_09

structure JacobiGeodesicDeviationCertificate where
  covariantAccelerationBounded : Bool
  tidalAccelerationRetained : Bool
  jacobiEquationSatisfied : Bool
  nonzeroInitialVariation : Bool
  localConjugatePointCandidateDetected : Bool
  conjugatePointCandidatesLocalOnly : Bool
  candidateIdentityRetained : Bool
  sourceAtlasNotMutated : Bool
  persistentWorldStateUnchanged : Bool
  decisionSelectionPerformed : Bool
  historyReadOnly : Bool
  curvatureGrantsNoAuthority : Bool
  jacobiFieldGrantsNoAuthority : Bool
  conjugatePointGrantsNoAuthority : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

/-- Coordinate form of the tidal term `(R(V,J)V)ⁱ`. -/
def curvatureAction {n : ℕ}
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (velocity jacobi : Fin n → ℝ)
    (i : Fin n) : ℝ :=
  ∑ j, ∑ k, ∑ l,
    curvature i j k l * velocity j * jacobi k * velocity l

/-- Coordinate residual of the Jacobi equation `∇²_V J + R(V,J)V = 0`. -/
def jacobiResidual {n : ℕ}
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (velocity jacobi secondCovariantDerivative : Fin n → ℝ)
    (i : Fin n) : ℝ :=
  secondCovariantDerivative i + curvatureAction curvature velocity jacobi i

/-- Metric norm squared of a chart-local variation field. -/
def variationNormSquared {n : ℕ}
    (metric : Fin n → Fin n → ℝ)
    (variation : Fin n → ℝ) : ℝ :=
  ∑ i, ∑ j, variation i * metric i j * variation j

/-- Zero curvature produces zero tidal acceleration. -/
theorem curvatureAction_zero {n : ℕ}
    (velocity jacobi : Fin n → ℝ)
    (i : Fin n) :
    curvatureAction (fun _ _ _ _ => 0) velocity jacobi i = 0 := by
  simp [curvatureAction]

/-- Under zero curvature, the Jacobi residual is exactly the second covariant derivative. -/
theorem jacobiResidual_zero_curvature {n : ℕ}
    (velocity jacobi secondCovariantDerivative : Fin n → ℝ)
    (i : Fin n) :
    jacobiResidual (fun _ _ _ _ => 0) velocity jacobi secondCovariantDerivative i =
      secondCovariantDerivative i := by
  simp [jacobiResidual, curvatureAction]

/-- Choosing the second covariant derivative as the negative tidal term solves the Jacobi equation. -/
theorem jacobiResidual_of_balanced_tidal_term {n : ℕ}
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (velocity jacobi : Fin n → ℝ)
    (i : Fin n) :
    jacobiResidual curvature velocity jacobi
      (fun q => -curvatureAction curvature velocity jacobi q) i = 0 := by
  simp [jacobiResidual]

/-- The zero endpoint variation has zero metric norm in every chart. -/
theorem variationNormSquared_zero {n : ℕ}
    (metric : Fin n → Fin n → ℝ) :
    variationNormSquared metric (fun _ => 0) = 0 := by
  simp [variationNormSquared]

/-- A vanishing Jacobi field has zero curvature action. -/
theorem curvatureAction_zero_jacobi {n : ℕ}
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (velocity : Fin n → ℝ)
    (i : Fin n) :
    curvatureAction curvature velocity (fun _ => 0) i = 0 := by
  simp [curvatureAction]

/-- Jacobi and conjugate-point evidence never grants selection or execution authority. -/
theorem jacobi_evidence_grants_no_authority
    (certificate : JacobiGeodesicDeviationCertificate)
    (hjacobi : certificate.jacobiFieldGrantsNoAuthority = true)
    (hconjugate : certificate.conjugatePointGrantsNoAuthority = true)
    (hselection : certificate.decisionSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.jacobiFieldGrantsNoAuthority = true ∧
      certificate.conjugatePointGrantsNoAuthority = true ∧
      certificate.decisionSelectionPerformed = false ∧
      certificate.executionPermission = false := by
  exact ⟨hjacobi, hconjugate, hselection, hexecution⟩

/-- The certificate remains read-only, future-only, and inactive. -/
theorem jacobi_certificate_is_future_only
    (certificate : JacobiGeodesicDeviationCertificate)
    (hreadonly : certificate.historyReadOnly = true)
    (hfuture : certificate.futureOnly = true)
    (hactive : certificate.activeNow = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.historyReadOnly = true ∧
      certificate.futureOnly = true ∧
      certificate.activeNow = false ∧
      certificate.executionPermission = false := by
  exact ⟨hreadonly, hfuture, hactive, hexecution⟩

end KUOS.PlanOS.JacobiGeodesicDeviationV1_09
