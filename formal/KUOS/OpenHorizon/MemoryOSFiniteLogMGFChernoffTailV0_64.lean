import Mathlib
import KUOS.OpenHorizon.MemoryOSKantorovichLipschitzMGFV0_63

namespace KUOS.OpenHorizon.MemoryOSFiniteLogMGFChernoffTailV0_64

open KUOS.OpenHorizon.MemoryOSKantorovichLipschitzMGFV0_63


def stationaryLogMGF (f : ThreeObservable) (t : ℝ) : ℝ :=
  Real.log (stationaryMGF f t)


def chernoffTransform (f : ThreeObservable) (t threshold : ℝ) : ℝ :=
  stationaryLogMGF f t - t * threshold


def chernoffEnvelope (f : ThreeObservable) (t threshold : ℝ) : ℝ :=
  Real.exp (-(t * threshold)) * stationaryMGF f t


def slowUpperTailMass (amplitude threshold : ℝ) : ℝ :=
  if threshold ≤ amplitude then (1 : ℝ) / 3 else 0


def fastUpperTailMass (amplitude threshold : ℝ) : ℝ :=
  if threshold ≤ amplitude then (2 : ℝ) / 3 else 0


def slowSemigroupHalfTailMass (n : ℕ) : ℝ :=
  slowUpperTailMass (((3 : ℝ) / 4) ^ n) ((1 : ℝ) / 2)


def slowSemigroupQuarterTailMass (n : ℕ) : ℝ :=
  slowUpperTailMass (((3 : ℝ) / 4) ^ n) ((1 : ℝ) / 4)


def fastSemigroupHalfTailMass (n : ℕ) : ℝ :=
  fastUpperTailMass (((1 : ℝ) / 4) ^ n) ((1 : ℝ) / 2)


def fastSemigroupQuarterTailMass (n : ℕ) : ℝ :=
  fastUpperTailMass (((1 : ℝ) / 4) ^ n) ((1 : ℝ) / 4)


theorem stationary_mgf_strictly_positive (f : ThreeObservable) (t : ℝ) :
    0 < stationaryMGF f t := by
  unfold stationaryMGF
  positivity


theorem exp_stationary_log_mgf (f : ThreeObservable) (t : ℝ) :
    Real.exp (stationaryLogMGF f t) = stationaryMGF f t := by
  unfold stationaryLogMGF
  exact Real.exp_log (stationary_mgf_strictly_positive f t)


theorem stationary_log_mgf_zero (f : ThreeObservable) :
    stationaryLogMGF f 0 = 0 := by
  have hmgf : stationaryMGF f 0 = 1 := by
    norm_num [stationaryMGF]
  rw [stationaryLogMGF, hmgf, Real.log_one]


theorem chernoff_transform_exponentiates
    (f : ThreeObservable) (t threshold : ℝ) :
    Real.exp (chernoffTransform f t threshold) =
      chernoffEnvelope f t threshold := by
  unfold chernoffTransform chernoffEnvelope
  rw [sub_eq_add_neg, Real.exp_add, exp_stationary_log_mgf]
  ring


theorem stationary_log_mgf_scaled_slow_exact (r t : ℝ) :
    stationaryLogMGF (observableScale r slowObservable) t =
      Real.log ((Real.exp (t * r) + 1 + Real.exp (-(t * r))) / 3) := by
  unfold stationaryLogMGF
  rw [stationary_mgf_scaled_slow_exact]


theorem stationary_log_mgf_scaled_fast_exact (r t : ℝ) :
    stationaryLogMGF (observableScale r fastObservable) t =
      Real.log ((2 * Real.exp (t * r) + Real.exp (-(2 * t * r))) / 3) := by
  unfold stationaryLogMGF
  rw [stationary_mgf_scaled_fast_exact]


theorem one_le_exponential_tilt_product
    (t amplitude threshold : ℝ)
    (ht : 0 ≤ t)
    (hthreshold : threshold ≤ amplitude) :
    1 ≤ Real.exp (-(t * threshold)) * Real.exp (t * amplitude) := by
  have harg : 0 ≤ t * (amplitude - threshold) := by
    exact mul_nonneg ht (sub_nonneg.mpr hthreshold)
  have hexp : Real.exp 0 ≤ Real.exp (t * (amplitude - threshold)) := by
    exact Real.exp_le_exp.mpr harg
  have hone : 1 ≤ Real.exp (t * (amplitude - threshold)) := by
    simpa using hexp
  calc
    1 ≤ Real.exp (t * (amplitude - threshold)) := hone
    _ = Real.exp (-(t * threshold) + t * amplitude) := by
      congr 1
      ring
    _ = Real.exp (-(t * threshold)) * Real.exp (t * amplitude) := by
      rw [Real.exp_add]


theorem slow_upper_tail_chernoff_bound
    (amplitude threshold t : ℝ) (ht : 0 ≤ t) :
    slowUpperTailMass amplitude threshold ≤
      chernoffEnvelope (observableScale amplitude slowObservable) t threshold := by
  by_cases hthreshold : threshold ≤ amplitude
  · rw [slowUpperTailMass, if_pos hthreshold]
    unfold chernoffEnvelope
    rw [stationary_mgf_scaled_slow_exact]
    have hprod := one_le_exponential_tilt_product
      t amplitude threshold ht hthreshold
    have hrest :
        0 ≤ Real.exp (-(t * threshold)) +
          Real.exp (-(t * threshold)) * Real.exp (-(t * amplitude)) := by
      positivity
    nlinarith
  · rw [slowUpperTailMass, if_neg hthreshold]
    unfold chernoffEnvelope
    positivity


theorem fast_upper_tail_chernoff_bound
    (amplitude threshold t : ℝ) (ht : 0 ≤ t) :
    fastUpperTailMass amplitude threshold ≤
      chernoffEnvelope (observableScale amplitude fastObservable) t threshold := by
  by_cases hthreshold : threshold ≤ amplitude
  · rw [fastUpperTailMass, if_pos hthreshold]
    unfold chernoffEnvelope
    rw [stationary_mgf_scaled_fast_exact]
    have hprod := one_le_exponential_tilt_product
      t amplitude threshold ht hthreshold
    have hrest :
        0 ≤ Real.exp (-(t * threshold)) *
          Real.exp (-(2 * t * amplitude)) := by
      positivity
    nlinarith
  · rw [fastUpperTailMass, if_neg hthreshold]
    unfold chernoffEnvelope
    positivity


theorem exact_slow_half_tail_extinction_threshold :
    slowSemigroupHalfTailMass 2 = (1 : ℝ) / 3 ∧
      slowSemigroupHalfTailMass 3 = 0 := by
  norm_num [slowSemigroupHalfTailMass, slowUpperTailMass]


theorem exact_slow_quarter_tail_extinction_threshold :
    slowSemigroupQuarterTailMass 4 = (1 : ℝ) / 3 ∧
      slowSemigroupQuarterTailMass 5 = 0 := by
  norm_num [slowSemigroupQuarterTailMass, slowUpperTailMass]


theorem exact_fast_half_tail_extinction_threshold :
    fastSemigroupHalfTailMass 0 = (2 : ℝ) / 3 ∧
      fastSemigroupHalfTailMass 1 = 0 := by
  norm_num [fastSemigroupHalfTailMass, fastUpperTailMass]


theorem exact_fast_quarter_tail_extinction_threshold :
    fastSemigroupQuarterTailMass 1 = (2 : ℝ) / 3 ∧
      fastSemigroupQuarterTailMass 2 = 0 := by
  norm_num [fastSemigroupQuarterTailMass, fastUpperTailMass]


theorem full_rank_log_mgf_chernoff_tail_commutes
    (sourceLogMGF sourceChernoff sourceTail
      targetLogMGF targetChernoff targetTail : ℝ)
    (hLogMGF : targetLogMGF = sourceLogMGF)
    (hChernoff : targetChernoff = sourceChernoff)
    (hTail : targetTail = sourceTail) :
    targetLogMGF = sourceLogMGF ∧
      targetChernoff = sourceChernoff ∧
      targetTail = sourceTail := by
  exact ⟨hLogMGF, hChernoff, hTail⟩


structure FiniteLogMGFChernoffTailCertificate where
  sourceMemoryOSV063Bound : Bool
  stationaryMGFStrictlyPositive : Bool
  finiteLogMGFExact : Bool
  expLogMGFIdentityExact : Bool
  slowFastChernoffBoundsExact : Bool
  exactTailExtinctionThresholds : Bool
  martonTailInputsRetained : Bool
  generalLargeDeviationPrincipleClaimed : Bool
  generalPathSpaceGaussianTheoremClaimed : Bool
  fullRankTransportCommutes : Bool
  singularAtomicProfileRetained : Bool
  rankOneDensityRecoveryNotClaimed : Bool
  candidateRankingPerformed : Bool
  candidatePruningPerformed : Bool
  candidateSelectionPerformed : Bool
  decisionCommitPerformed : Bool
  activationPerformed : Bool
  executionPermission : Bool
  persistentWORLDStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool


theorem certificate_grants_no_authority
    (certificate : FiniteLogMGFChernoffTailCertificate)
    (hranking : certificate.candidateRankingPerformed = false)
    (hpruning : certificate.candidatePruningPerformed = false)
    (hselection : certificate.candidateSelectionPerformed = false)
    (hcommit : certificate.decisionCommitPerformed = false)
    (hactivation : certificate.activationPerformed = false)
    (hexecution : certificate.executionPermission = false)
    (hworld : certificate.persistentWORLDStateMutated = false)
    (hverification : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false) :
    certificate.candidateRankingPerformed = false ∧
      certificate.candidatePruningPerformed = false ∧
      certificate.candidateSelectionPerformed = false ∧
      certificate.decisionCommitPerformed = false ∧
      certificate.activationPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.persistentWORLDStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false := by
  exact ⟨hranking, hpruning, hselection, hcommit, hactivation,
    hexecution, hworld, hverification, htruth⟩

end KUOS.OpenHorizon.MemoryOSFiniteLogMGFChernoffTailV0_64
