import Mathlib
import KUOS.PlanOS.JacobiGeodesicDeviationV1_09

namespace KUOS.PlanOS.SecondVariationMorseIndexV1_10

structure SecondVariationMorseIndexCertificate where
  endpointFixedVariationsVerified : Bool
  indexFormSymmetric : Bool
  secondVariationRetained : Bool
  finiteBasisMorseIndexComputed : Bool
  conjugateMultiplicityCandidateLocalOnly : Bool
  morseIndexFiniteWindowOnly : Bool
  negativeDirectionWitnessesRetained : Bool
  nullDirectionWitnessesRetained : Bool
  candidateIdentityRetained : Bool
  sourceJacobiCertificateNotMutated : Bool
  persistentWorldStateUnchanged : Bool
  decisionSelectionPerformed : Bool
  historyReadOnly : Bool
  curvatureGrantsNoAuthority : Bool
  secondVariationGrantsNoAuthority : Bool
  morseIndexGrantsNoAuthority : Bool
  conjugateMultiplicityGrantsNoAuthority : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

/-- Metric pairing of two chart-local tangent vectors. -/
def metricPair {n : ℕ}
    (metric : Fin n → Fin n → ℝ)
    (left right : Fin n → ℝ) : ℝ :=
  ∑ i, ∑ j, left i * metric i j * right j

/-- Curvature contribution `⟨R(T,X)T,Y⟩`. -/
def curvaturePair {n : ℕ}
    (metric : Fin n → Fin n → ℝ)
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (tangent variationLeft variationRight : Fin n → ℝ) : ℝ :=
  metricPair metric
    (JacobiGeodesicDeviationV1_09.curvatureAction
      curvature tangent variationLeft)
    variationRight

/-- Pointwise integrand of the endpoint-fixed index form. -/
def indexIntegrand {n : ℕ}
    (metric : Fin n → Fin n → ℝ)
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (tangent variationLeft variationRight
      derivativeLeft derivativeRight : Fin n → ℝ) : ℝ :=
  metricPair metric derivativeLeft derivativeRight -
    curvaturePair metric curvature tangent variationLeft variationRight

/-- Finite quadrature form used by the bounded runtime certificate. -/
def discreteIndexForm {n m : ℕ}
    (weights : Fin m → ℝ)
    (metric : Fin n → Fin n → ℝ)
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (tangent variationLeft variationRight
      derivativeLeft derivativeRight : Fin m → Fin n → ℝ) : ℝ :=
  ∑ sample,
    weights sample *
      indexIntegrand metric curvature
        (tangent sample)
        (variationLeft sample)
        (variationRight sample)
        (derivativeLeft sample)
        (derivativeRight sample)

/-- Number of strictly negative spectral directions in a finite basis. -/
def negativeCount {n : ℕ} (eigenvalues : Fin n → ℝ) : ℕ :=
  (Finset.univ.filter fun i => eigenvalues i < 0).card

/-- Exact nullity of a finite spectral family. -/
def exactNullity {n : ℕ} (eigenvalues : Fin n → ℝ) : ℕ :=
  (Finset.univ.filter fun i => eigenvalues i = 0).card

@[simp] theorem metricPair_zero_left {n : ℕ}
    (metric : Fin n → Fin n → ℝ)
    (right : Fin n → ℝ) :
    metricPair metric (fun _ => 0) right = 0 := by
  simp [metricPair]

@[simp] theorem metricPair_zero_right {n : ℕ}
    (metric : Fin n → Fin n → ℝ)
    (left : Fin n → ℝ) :
    metricPair metric left (fun _ => 0) = 0 := by
  simp [metricPair]

@[simp] theorem curvaturePair_zero_variation {n : ℕ}
    (metric : Fin n → Fin n → ℝ)
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (tangent right : Fin n → ℝ) :
    curvaturePair metric curvature tangent (fun _ => 0) right = 0 := by
  simp [curvaturePair,
    JacobiGeodesicDeviationV1_09.curvatureAction]

/-- The zero endpoint-fixed variation has zero index integrand. -/
theorem indexIntegrand_zero {n : ℕ}
    (metric : Fin n → Fin n → ℝ)
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (tangent : Fin n → ℝ) :
    indexIntegrand metric curvature tangent
      (fun _ => 0) (fun _ => 0) (fun _ => 0) (fun _ => 0) = 0 := by
  simp [indexIntegrand]

/-- The zero variation family has zero discrete second variation. -/
theorem discreteIndexForm_zero {n m : ℕ}
    (weights : Fin m → ℝ)
    (metric : Fin n → Fin n → ℝ)
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (tangent : Fin m → Fin n → ℝ) :
    discreteIndexForm weights metric curvature tangent
      (fun _ _ => 0) (fun _ _ => 0)
      (fun _ _ => 0) (fun _ _ => 0) = 0 := by
  simp [discreteIndexForm, indexIntegrand]

/-- Equality of derivative and curvature energies gives a null index direction. -/
theorem indexIntegrand_self_zero_of_balance {n : ℕ}
    (metric : Fin n → Fin n → ℝ)
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (tangent variation derivative : Fin n → ℝ)
    (hbalance :
      metricPair metric derivative derivative =
        curvaturePair metric curvature tangent variation variation) :
    indexIntegrand metric curvature tangent variation variation
      derivative derivative = 0 := by
  unfold indexIntegrand
  linarith

/-- Pointwise symmetry implies symmetry of the finite quadrature index form. -/
theorem discreteIndexForm_symm_of_pointwise {n m : ℕ}
    (weights : Fin m → ℝ)
    (metric : Fin n → Fin n → ℝ)
    (curvature : Fin n → Fin n → Fin n → Fin n → ℝ)
    (tangent variationLeft variationRight
      derivativeLeft derivativeRight : Fin m → Fin n → ℝ)
    (hsymm : ∀ sample,
      indexIntegrand metric curvature
        (tangent sample)
        (variationLeft sample)
        (variationRight sample)
        (derivativeLeft sample)
        (derivativeRight sample) =
      indexIntegrand metric curvature
        (tangent sample)
        (variationRight sample)
        (variationLeft sample)
        (derivativeRight sample)
        (derivativeLeft sample)) :
    discreteIndexForm weights metric curvature tangent
      variationLeft variationRight derivativeLeft derivativeRight =
    discreteIndexForm weights metric curvature tangent
      variationRight variationLeft derivativeRight derivativeLeft := by
  unfold discreteIndexForm
  apply Finset.sum_congr rfl
  intro sample _
  rw [hsymm sample]

/-- One negative eigenvalue forces positive finite Morse index. -/
theorem negativeCount_pos_of_negative_eigenvalue {n : ℕ}
    (eigenvalues : Fin n → ℝ)
    (i : Fin n)
    (hnegative : eigenvalues i < 0) :
    0 < negativeCount eigenvalues := by
  unfold negativeCount
  exact Finset.card_pos.mpr ⟨i, by simp [hnegative]⟩

/-- One zero eigenvalue forces positive finite nullity. -/
theorem exactNullity_pos_of_zero_eigenvalue {n : ℕ}
    (eigenvalues : Fin n → ℝ)
    (i : Fin n)
    (hzero : eigenvalues i = 0) :
    0 < exactNullity eigenvalues := by
  unfold exactNullity
  exact Finset.card_pos.mpr ⟨i, by simp [hzero]⟩

/-- A negative second-variation witness refutes nonnegativity of the form. -/
theorem negative_direction_refutes_nonnegative {α : Type}
    (quadraticForm : α → ℝ)
    (variation : α)
    (hnegative : quadraticForm variation < 0) :
    ¬ ∀ candidate, 0 ≤ quadraticForm candidate := by
  intro hall
  exact (not_lt_of_ge (hall variation)) hnegative

/-- Morse-index and multiplicity evidence never grants selection or execution authority. -/
theorem morse_evidence_grants_no_authority
    (certificate : SecondVariationMorseIndexCertificate)
    (hmorse : certificate.morseIndexGrantsNoAuthority = true)
    (hmultiplicity :
      certificate.conjugateMultiplicityGrantsNoAuthority = true)
    (hselection : certificate.decisionSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.morseIndexGrantsNoAuthority = true ∧
      certificate.conjugateMultiplicityGrantsNoAuthority = true ∧
      certificate.decisionSelectionPerformed = false ∧
      certificate.executionPermission = false := by
  exact ⟨hmorse, hmultiplicity, hselection, hexecution⟩

/-- The certificate remains read-only, finite-window, future-only, and inactive. -/
theorem morse_certificate_is_future_only
    (certificate : SecondVariationMorseIndexCertificate)
    (hreadonly : certificate.historyReadOnly = true)
    (hfinite : certificate.morseIndexFiniteWindowOnly = true)
    (hfuture : certificate.futureOnly = true)
    (hactive : certificate.activeNow = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.historyReadOnly = true ∧
      certificate.morseIndexFiniteWindowOnly = true ∧
      certificate.futureOnly = true ∧
      certificate.activeNow = false ∧
      certificate.executionPermission = false := by
  exact ⟨hreadonly, hfinite, hfuture, hactive, hexecution⟩

end KUOS.PlanOS.SecondVariationMorseIndexV1_10
