import Mathlib
import KUOS.OpenHorizon.MemoryOSLogSobolevHypercontractiveMixingV0_59

namespace KUOS.OpenHorizon.MemoryOSModifiedLogSobolevHellingerSeparationV0_60

open Set
open KUOS.OpenHorizon.MemoryOSLogSobolevHypercontractiveMixingV0_59

def uniformKLFunEntropy (r₀ r₁ r₂ : ℝ) : ℝ :=
  (InformationTheory.klFun r₀ +
    InformationTheory.klFun r₁ +
    InformationTheory.klFun r₂) / 3

def residualLikelihoodEarly (r₀ r₁ : ℝ) : ℝ :=
  ((9 : ℝ) / 13) * r₀ + ((4 : ℝ) / 13) * r₁

def residualLikelihoodMiddle (r₀ r₁ r₂ : ℝ) : ℝ :=
  ((4 : ℝ) / 13) * r₀ +
    ((5 : ℝ) / 13) * r₁ +
    ((4 : ℝ) / 13) * r₂

def residualLikelihoodLate (r₁ r₂ : ℝ) : ℝ :=
  ((4 : ℝ) / 13) * r₁ + ((9 : ℝ) / 13) * r₂

def twoStepLikelihoodEarly (r₀ r₁ r₂ : ℝ) : ℝ :=
  ((5 : ℝ) / 8) * r₀ +
    ((5 : ℝ) / 16) * r₁ +
    ((1 : ℝ) / 16) * r₂

def twoStepLikelihoodMiddle (r₀ r₁ r₂ : ℝ) : ℝ :=
  ((5 : ℝ) / 16) * r₀ +
    ((3 : ℝ) / 8) * r₁ +
    ((5 : ℝ) / 16) * r₂

def twoStepLikelihoodLate (r₀ r₁ r₂ : ℝ) : ℝ :=
  ((1 : ℝ) / 16) * r₀ +
    ((5 : ℝ) / 16) * r₁ +
    ((5 : ℝ) / 8) * r₂

def doeblinLikelihoodMix (x : ℝ) : ℝ :=
  ((3 : ℝ) / 16) + ((13 : ℝ) / 16) * x

def uniformLikelihoodHellingerSquared (r₀ r₁ r₂ : ℝ) : ℝ :=
  ((Real.sqrt r₀ - 1) ^ 2 +
    (Real.sqrt r₁ - 1) ^ 2 +
    (Real.sqrt r₂ - 1) ^ 2) / 6

def uniformLikelihoodSeparation (r₀ r₁ r₂ : ℝ) : ℝ :=
  1 - min r₀ (min r₁ r₂)

def worstCaseSeparationProfile (n : ℕ) : ℚ :=
  ((3 : ℚ) / 2) * (((3 : ℚ) / 4) ^ n) -
    ((1 : ℚ) / 2) * (((1 : ℚ) / 4) ^ n)

def referenceSeparationProfile (n : ℕ) : ℚ :=
  ((9 : ℚ) / 20) * (((3 : ℚ) / 4) ^ n)

def referenceHellingerSquaredEnvelope (n : ℕ) : ℚ :=
  ((1 : ℚ) / 3) * (referenceSeparationProfile n) ^ 2

def worstCaseKLBlockEnvelope (blocks : ℕ) : ℚ :=
  2 * (((13 : ℚ) / 16) ^ blocks)

theorem klFun_two_point_jensen
    (x y a b : ℝ)
    (hx : 0 ≤ x) (hy : 0 ≤ y)
    (ha : 0 ≤ a) (hb : 0 ≤ b)
    (hab : a + b = 1) :
    InformationTheory.klFun (a * x + b * y) ≤
      a * InformationTheory.klFun x +
        b * InformationTheory.klFun y := by
  have h := InformationTheory.convexOn_klFun.2
    (show x ∈ Set.Ici (0 : ℝ) by exact hx)
    (show y ∈ Set.Ici (0 : ℝ) by exact hy)
    ha hb hab
  simpa [smul_eq_mul] using h

theorem uniform_klFun_eq_uniform_kl
    (r₀ r₁ r₂ : ℝ)
    (hmass : r₀ + r₁ + r₂ = 3) :
    uniformKLFunEntropy r₀ r₁ r₂ =
      uniformLikelihoodKLEntropy r₀ r₁ r₂ := by
  unfold uniformKLFunEntropy uniformLikelihoodKLEntropy
    InformationTheory.klFun
  nlinarith

theorem residual_likelihood_mass_exact
    (r₀ r₁ r₂ : ℝ)
    (hmass : r₀ + r₁ + r₂ = 3) :
    residualLikelihoodEarly r₀ r₁ +
        residualLikelihoodMiddle r₀ r₁ r₂ +
        residualLikelihoodLate r₁ r₂ = 3 := by
  unfold residualLikelihoodEarly residualLikelihoodMiddle
    residualLikelihoodLate
  nlinarith

theorem two_step_likelihood_mass_exact
    (r₀ r₁ r₂ : ℝ)
    (hmass : r₀ + r₁ + r₂ = 3) :
    twoStepLikelihoodEarly r₀ r₁ r₂ +
        twoStepLikelihoodMiddle r₀ r₁ r₂ +
        twoStepLikelihoodLate r₀ r₁ r₂ = 3 := by
  unfold twoStepLikelihoodEarly twoStepLikelihoodMiddle
    twoStepLikelihoodLate
  nlinarith

theorem residual_klFun_data_processing
    (r₀ r₁ r₂ : ℝ)
    (h₀ : 0 ≤ r₀) (h₁ : 0 ≤ r₁) (h₂ : 0 ≤ r₂) :
    uniformKLFunEntropy
        (residualLikelihoodEarly r₀ r₁)
        (residualLikelihoodMiddle r₀ r₁ r₂)
        (residualLikelihoodLate r₁ r₂) ≤
      uniformKLFunEntropy r₀ r₁ r₂ := by
  have hearly := klFun_two_point_jensen
    r₀ r₁ ((9 : ℝ) / 13) ((4 : ℝ) / 13)
    h₀ h₁ (by norm_num) (by norm_num) (by norm_num)
  have hlate := klFun_two_point_jensen
    r₁ r₂ ((4 : ℝ) / 13) ((9 : ℝ) / 13)
    h₁ h₂ (by norm_num) (by norm_num) (by norm_num)
  have hinner := klFun_two_point_jensen
    r₁ r₂ ((5 : ℝ) / 9) ((4 : ℝ) / 9)
    h₁ h₂ (by norm_num) (by norm_num) (by norm_num)
  have hinner_nonneg :
      0 ≤ ((5 : ℝ) / 9) * r₁ + ((4 : ℝ) / 9) * r₂ := by
    positivity
  have hmiddleOuter := klFun_two_point_jensen
    r₀ (((5 : ℝ) / 9) * r₁ + ((4 : ℝ) / 9) * r₂)
    ((4 : ℝ) / 13) ((9 : ℝ) / 13)
    h₀ hinner_nonneg (by norm_num) (by norm_num) (by norm_num)
  have hmiddle :
      InformationTheory.klFun (residualLikelihoodMiddle r₀ r₁ r₂) ≤
        ((4 : ℝ) / 13) * InformationTheory.klFun r₀ +
        ((5 : ℝ) / 13) * InformationTheory.klFun r₁ +
        ((4 : ℝ) / 13) * InformationTheory.klFun r₂ := by
    calc
      InformationTheory.klFun (residualLikelihoodMiddle r₀ r₁ r₂) =
          InformationTheory.klFun
            (((4 : ℝ) / 13) * r₀ +
              ((9 : ℝ) / 13) *
                (((5 : ℝ) / 9) * r₁ + ((4 : ℝ) / 9) * r₂)) := by
                  congr 1
                  unfold residualLikelihoodMiddle
                  ring
      _ ≤ ((4 : ℝ) / 13) * InformationTheory.klFun r₀ +
          ((9 : ℝ) / 13) *
            InformationTheory.klFun
              (((5 : ℝ) / 9) * r₁ + ((4 : ℝ) / 9) * r₂) :=
        hmiddleOuter
      _ ≤ ((4 : ℝ) / 13) * InformationTheory.klFun r₀ +
          ((5 : ℝ) / 13) * InformationTheory.klFun r₁ +
          ((4 : ℝ) / 13) * InformationTheory.klFun r₂ := by
        nlinarith
  unfold uniformKLFunEntropy residualLikelihoodEarly residualLikelihoodLate
  nlinarith

theorem doeblin_klFun_cell_decay
    (x : ℝ) (hx : 0 ≤ x) :
    InformationTheory.klFun (doeblinLikelihoodMix x) ≤
      ((13 : ℝ) / 16) * InformationTheory.klFun x := by
  have h := klFun_two_point_jensen
    1 x ((3 : ℝ) / 16) ((13 : ℝ) / 16)
    (by norm_num) hx (by norm_num) (by norm_num) (by norm_num)
  simpa [doeblinLikelihoodMix, InformationTheory.klFun_one] using h

theorem uniform_doeblin_klFun_decay
    (u₀ u₁ u₂ : ℝ)
    (h₀ : 0 ≤ u₀) (h₁ : 0 ≤ u₁) (h₂ : 0 ≤ u₂) :
    uniformKLFunEntropy
        (doeblinLikelihoodMix u₀)
        (doeblinLikelihoodMix u₁)
        (doeblinLikelihoodMix u₂) ≤
      ((13 : ℝ) / 16) * uniformKLFunEntropy u₀ u₁ u₂ := by
  have hcell₀ := doeblin_klFun_cell_decay u₀ h₀
  have hcell₁ := doeblin_klFun_cell_decay u₁ h₁
  have hcell₂ := doeblin_klFun_cell_decay u₂ h₂
  unfold uniformKLFunEntropy
  nlinarith

theorem two_step_early_doeblin_decomposition
    (r₀ r₁ r₂ : ℝ)
    (hmass : r₀ + r₁ + r₂ = 3) :
    twoStepLikelihoodEarly r₀ r₁ r₂ =
      doeblinLikelihoodMix (residualLikelihoodEarly r₀ r₁) := by
  unfold twoStepLikelihoodEarly doeblinLikelihoodMix
    residualLikelihoodEarly
  nlinarith

theorem two_step_middle_doeblin_decomposition
    (r₀ r₁ r₂ : ℝ)
    (hmass : r₀ + r₁ + r₂ = 3) :
    twoStepLikelihoodMiddle r₀ r₁ r₂ =
      doeblinLikelihoodMix (residualLikelihoodMiddle r₀ r₁ r₂) := by
  unfold twoStepLikelihoodMiddle doeblinLikelihoodMix
    residualLikelihoodMiddle
  nlinarith

theorem two_step_late_doeblin_decomposition
    (r₀ r₁ r₂ : ℝ)
    (hmass : r₀ + r₁ + r₂ = 3) :
    twoStepLikelihoodLate r₀ r₁ r₂ =
      doeblinLikelihoodMix (residualLikelihoodLate r₁ r₂) := by
  unfold twoStepLikelihoodLate doeblinLikelihoodMix
    residualLikelihoodLate
  nlinarith

theorem two_step_modified_log_sobolev_entropy_decay
    (r₀ r₁ r₂ : ℝ)
    (h₀ : 0 ≤ r₀) (h₁ : 0 ≤ r₁) (h₂ : 0 ≤ r₂)
    (hmass : r₀ + r₁ + r₂ = 3) :
    uniformLikelihoodKLEntropy
        (twoStepLikelihoodEarly r₀ r₁ r₂)
        (twoStepLikelihoodMiddle r₀ r₁ r₂)
        (twoStepLikelihoodLate r₀ r₁ r₂) ≤
      ((13 : ℝ) / 16) * uniformLikelihoodKLEntropy r₀ r₁ r₂ := by
  have hr₀ : 0 ≤ residualLikelihoodEarly r₀ r₁ := by
    unfold residualLikelihoodEarly
    positivity
  have hr₁ : 0 ≤ residualLikelihoodMiddle r₀ r₁ r₂ := by
    unfold residualLikelihoodMiddle
    positivity
  have hr₂ : 0 ≤ residualLikelihoodLate r₁ r₂ := by
    unfold residualLikelihoodLate
    positivity
  have hresidual := residual_klFun_data_processing r₀ r₁ r₂ h₀ h₁ h₂
  have hmix := uniform_doeblin_klFun_decay
    (residualLikelihoodEarly r₀ r₁)
    (residualLikelihoodMiddle r₀ r₁ r₂)
    (residualLikelihoodLate r₁ r₂)
    hr₀ hr₁ hr₂
  have houtmass := two_step_likelihood_mass_exact r₀ r₁ r₂ hmass
  have hinput := uniform_klFun_eq_uniform_kl r₀ r₁ r₂ hmass
  calc
    uniformLikelihoodKLEntropy
        (twoStepLikelihoodEarly r₀ r₁ r₂)
        (twoStepLikelihoodMiddle r₀ r₁ r₂)
        (twoStepLikelihoodLate r₀ r₁ r₂) =
      uniformKLFunEntropy
        (twoStepLikelihoodEarly r₀ r₁ r₂)
        (twoStepLikelihoodMiddle r₀ r₁ r₂)
        (twoStepLikelihoodLate r₀ r₁ r₂) :=
      (uniform_klFun_eq_uniform_kl _ _ _ houtmass).symm
    _ = uniformKLFunEntropy
        (doeblinLikelihoodMix (residualLikelihoodEarly r₀ r₁))
        (doeblinLikelihoodMix (residualLikelihoodMiddle r₀ r₁ r₂))
        (doeblinLikelihoodMix (residualLikelihoodLate r₁ r₂)) := by
      rw [
        two_step_early_doeblin_decomposition r₀ r₁ r₂ hmass,
        two_step_middle_doeblin_decomposition r₀ r₁ r₂ hmass,
        two_step_late_doeblin_decomposition r₀ r₁ r₂ hmass
      ]
    _ ≤ ((13 : ℝ) / 16) *
        uniformKLFunEntropy
          (residualLikelihoodEarly r₀ r₁)
          (residualLikelihoodMiddle r₀ r₁ r₂)
          (residualLikelihoodLate r₁ r₂) := hmix
    _ ≤ ((13 : ℝ) / 16) * uniformKLFunEntropy r₀ r₁ r₂ := by
      exact mul_le_mul_of_nonneg_left hresidual (by norm_num)
    _ = ((13 : ℝ) / 16) * uniformLikelihoodKLEntropy r₀ r₁ r₂ := by
      rw [hinput]

theorem iterated_two_step_modified_entropy_decay
    (entropy : ℕ → ℝ)
    (hstep :
      ∀ n, entropy (n + 1) ≤ ((13 : ℝ) / 16) * entropy n) :
    ∀ n, entropy n ≤ (((13 : ℝ) / 16) ^ n) * entropy 0 := by
  intro n
  induction n with
  | zero =>
      simp
  | succ n ih =>
      calc
        entropy (n + 1) ≤ ((13 : ℝ) / 16) * entropy n := hstep n
        _ ≤ ((13 : ℝ) / 16) *
            ((((13 : ℝ) / 16) ^ n) * entropy 0) := by
          exact mul_le_mul_of_nonneg_left ih (by norm_num)
        _ = (((13 : ℝ) / 16) ^ (n + 1)) * entropy 0 := by
          rw [pow_succ]
          ring

theorem sqrt_deviation_sq_le_deviation_sq
    (x : ℝ) (hx : 0 ≤ x) :
    (Real.sqrt x - 1) ^ 2 ≤ (x - 1) ^ 2 := by
  have hsqrt : (Real.sqrt x) ^ 2 = x := Real.sq_sqrt hx
  have hsqrt_nonneg : 0 ≤ Real.sqrt x := Real.sqrt_nonneg x
  have hfactor : 0 ≤ (Real.sqrt x) ^ 2 + 2 * Real.sqrt x := by
    nlinarith [sq_nonneg (Real.sqrt x)]
  have hprod :
      0 ≤ (Real.sqrt x - 1) ^ 2 *
        ((Real.sqrt x) ^ 2 + 2 * Real.sqrt x) :=
    mul_nonneg (sq_nonneg (Real.sqrt x - 1)) hfactor
  nlinarith

theorem uniform_hellinger_squared_le_chi_square_half
    (r₀ r₁ r₂ : ℝ)
    (h₀ : 0 ≤ r₀) (h₁ : 0 ≤ r₁) (h₂ : 0 ≤ r₂) :
    uniformLikelihoodHellingerSquared r₀ r₁ r₂ ≤
      ((1 : ℝ) / 2) * uniformLikelihoodChiSquare r₀ r₁ r₂ := by
  have hroot₀ := sqrt_deviation_sq_le_deviation_sq r₀ h₀
  have hroot₁ := sqrt_deviation_sq_le_deviation_sq r₁ h₁
  have hroot₂ := sqrt_deviation_sq_le_deviation_sq r₂ h₂
  unfold uniformLikelihoodHellingerSquared uniformLikelihoodChiSquare
  nlinarith

theorem uniform_hellinger_squared_eq_one_sub_affinity
    (r₀ r₁ r₂ : ℝ)
    (h₀ : 0 ≤ r₀) (h₁ : 0 ≤ r₁) (h₂ : 0 ≤ r₂)
    (hmass : r₀ + r₁ + r₂ = 3) :
    uniformLikelihoodHellingerSquared r₀ r₁ r₂ =
      1 - (Real.sqrt r₀ + Real.sqrt r₁ + Real.sqrt r₂) / 3 := by
  have hsqrt₀ : (Real.sqrt r₀) ^ 2 = r₀ := Real.sq_sqrt h₀
  have hsqrt₁ : (Real.sqrt r₁) ^ 2 = r₁ := Real.sq_sqrt h₁
  have hsqrt₂ : (Real.sqrt r₂) ^ 2 = r₂ := Real.sq_sqrt h₂
  unfold uniformLikelihoodHellingerSquared
  nlinarith

theorem reference_hellinger_squared_envelope
    (u : ℝ) (h₀ : 0 ≤ u) (h₁ : u ≤ 1) :
    uniformLikelihoodHellingerSquared (1 - u) 1 (1 + u) ≤
      u ^ 2 / 3 := by
  have hleft : 0 ≤ 1 - u := by linarith
  have hright : 0 ≤ 1 + u := by linarith
  calc
    uniformLikelihoodHellingerSquared (1 - u) 1 (1 + u) ≤
      ((1 : ℝ) / 2) *
        uniformLikelihoodChiSquare (1 - u) 1 (1 + u) :=
      uniform_hellinger_squared_le_chi_square_half
        (1 - u) 1 (1 + u) hleft (by norm_num) hright
    _ = u ^ 2 / 3 := by
      unfold uniformLikelihoodChiSquare
      ring

theorem reference_separation_exact
    (u : ℝ) (hu : 0 ≤ u) :
    uniformLikelihoodSeparation (1 - u) 1 (1 + u) = u := by
  have hmiddle : min (1 : ℝ) (1 + u) = 1 := min_eq_left (by linarith)
  have hearly : min (1 - u) 1 = 1 - u := min_eq_left (by linarith)
  unfold uniformLikelihoodSeparation
  rw [hmiddle, hearly]
  ring

theorem exact_two_step_doeblin_kernel_decomposition :
    ((5 : ℚ) / 8 = 1 / 16 + (13 / 16) * (9 / 13)) ∧
      ((5 : ℚ) / 16 = 1 / 16 + (13 / 16) * (4 / 13)) ∧
      ((1 : ℚ) / 16 = 1 / 16 + (13 / 16) * 0) ∧
      ((3 : ℚ) / 8 = 1 / 16 + (13 / 16) * (5 / 13)) ∧
      ((9 : ℚ) / 13 + 4 / 13 = 1) ∧
      ((4 : ℚ) / 13 + 5 / 13 + 4 / 13 = 1) := by
  norm_num

theorem exact_worst_case_separation_quarter_cutoff :
    worstCaseSeparationProfile 7 ≤ (1 : ℚ) / 4 ∧
      worstCaseSeparationProfile 6 > (1 : ℚ) / 4 := by
  norm_num [worstCaseSeparationProfile]

theorem exact_worst_case_separation_eighth_cutoff :
    worstCaseSeparationProfile 9 ≤ (1 : ℚ) / 8 ∧
      worstCaseSeparationProfile 8 > (1 : ℚ) / 8 := by
  norm_num [worstCaseSeparationProfile]

theorem exact_reference_separation_twentieth_cutoff :
    referenceSeparationProfile 8 ≤ (1 : ℚ) / 20 ∧
      referenceSeparationProfile 7 > (1 : ℚ) / 20 := by
  norm_num [referenceSeparationProfile]

theorem exact_reference_hellinger_twentieth_envelope_cutoff :
    referenceHellingerSquaredEnvelope 6 ≤ ((1 : ℚ) / 20) ^ 2 ∧
      referenceHellingerSquaredEnvelope 5 > ((1 : ℚ) / 20) ^ 2 := by
  norm_num [referenceHellingerSquaredEnvelope, referenceSeparationProfile]

theorem exact_worst_case_kl_quarter_block_cutoff :
    worstCaseKLBlockEnvelope 11 ≤ (1 : ℚ) / 4 ∧
      worstCaseKLBlockEnvelope 10 > (1 : ℚ) / 4 := by
  norm_num [worstCaseKLBlockEnvelope]

theorem full_rank_modified_entropy_profile_transport_commutes
    (sourceBefore sourceAfter targetBefore targetAfter : ℝ)
    (hbefore : targetBefore = sourceBefore)
    (hafter : targetAfter = sourceAfter)
    (hsource :
      sourceAfter ≤ ((13 : ℝ) / 16) * sourceBefore) :
    targetAfter ≤ ((13 : ℝ) / 16) * targetBefore := by
  linarith

structure ModifiedLogSobolevHellingerSeparationCertificate where
  sourceMemoryOSV059Bound : Bool
  sourceMemoryOSV058Bound : Bool
  twoStepDoeblinDecompositionExact : Bool
  modifiedLogSobolevEntropyDecayExact : Bool
  residualKernelDataProcessingExact : Bool
  hellingerProfileExact : Bool
  separationProfileExact : Bool
  finiteCutoffThresholdsExact : Bool
  fullRankTransportCommutes : Bool
  singularAtomicProfilesRetained : Bool
  rankOneDensityRecoveryNotClaimed : Bool
  candidatePruningPerformed : Bool
  candidateSelectionPerformed : Bool
  executionPermission : Bool
  persistentWORLDStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

theorem certificate_grants_no_authority
    (certificate : ModifiedLogSobolevHellingerSeparationCertificate)
    (hpruning : certificate.candidatePruningPerformed = false)
    (hselection : certificate.candidateSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false)
    (hworld : certificate.persistentWORLDStateMutated = false)
    (hverification : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false) :
    certificate.candidatePruningPerformed = false ∧
      certificate.candidateSelectionPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.persistentWORLDStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false := by
  exact ⟨hpruning, hselection, hexecution, hworld, hverification, htruth⟩

end KUOS.OpenHorizon.MemoryOSModifiedLogSobolevHellingerSeparationV0_60
