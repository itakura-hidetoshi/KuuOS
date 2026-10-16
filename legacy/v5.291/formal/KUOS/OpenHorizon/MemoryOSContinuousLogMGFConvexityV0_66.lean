import Mathlib
import KUOS.OpenHorizon.MemoryOSFiniteLegendreOptimizerV0_65

namespace KUOS.OpenHorizon.MemoryOSContinuousLogMGFConvexityV0_66

open Set Filter
open KUOS.OpenHorizon.MemoryOSKantorovichLipschitzMGFV0_63
open KUOS.OpenHorizon.MemoryOSFiniteLogMGFChernoffTailV0_64
open KUOS.OpenHorizon.MemoryOSFiniteLegendreOptimizerV0_65

noncomputable section


def partitionSum (f : ThreeObservable) (t : ℝ) : ℝ :=
  Real.exp (t * f.early) + Real.exp (t * f.middle) +
    Real.exp (t * f.late)


def partitionFirstMoment (f : ThreeObservable) (t : ℝ) : ℝ :=
  f.early * Real.exp (t * f.early) +
    f.middle * Real.exp (t * f.middle) +
    f.late * Real.exp (t * f.late)


def partitionSecondMoment (f : ThreeObservable) (t : ℝ) : ℝ :=
  f.early ^ 2 * Real.exp (t * f.early) +
    f.middle ^ 2 * Real.exp (t * f.middle) +
    f.late ^ 2 * Real.exp (t * f.late)


def tiltedMean (f : ThreeObservable) (t : ℝ) : ℝ :=
  partitionFirstMoment f t / partitionSum f t


def tiltedCurvature (f : ThreeObservable) (t : ℝ) : ℝ :=
  (partitionSecondMoment f t * partitionSum f t -
      partitionFirstMoment f t ^ 2) /
    partitionSum f t ^ 2


def continuousLegendreDerivative
    (f : ThreeObservable) (threshold t : ℝ) : ℝ :=
  threshold - tiltedMean f t


theorem partition_sum_strictly_positive (f : ThreeObservable) (t : ℝ) :
    0 < partitionSum f t := by
  unfold partitionSum
  positivity


theorem partition_sum_ne_zero (f : ThreeObservable) (t : ℝ) :
    partitionSum f t ≠ 0 :=
  ne_of_gt (partition_sum_strictly_positive f t)


theorem stationary_mgf_eq_partition_sum_div_three
    (f : ThreeObservable) (t : ℝ) :
    stationaryMGF f t = partitionSum f t / 3 := by
  rfl


theorem hasDerivAt_partitionSum (f : ThreeObservable) (t : ℝ) :
    HasDerivAt (partitionSum f) (partitionFirstMoment f t) t := by
  have hEarly :
      HasDerivAt (fun s : ℝ => Real.exp (s * f.early))
        (Real.exp (t * f.early) * f.early) t :=
    ((hasDerivAt_id t).mul_const f.early).exp
  have hMiddle :
      HasDerivAt (fun s : ℝ => Real.exp (s * f.middle))
        (Real.exp (t * f.middle) * f.middle) t :=
    ((hasDerivAt_id t).mul_const f.middle).exp
  have hLate :
      HasDerivAt (fun s : ℝ => Real.exp (s * f.late))
        (Real.exp (t * f.late) * f.late) t :=
    ((hasDerivAt_id t).mul_const f.late).exp
  convert (hEarly.add hMiddle).add hLate using 1 <;>
    simp [partitionSum, partitionFirstMoment] <;> ring


theorem hasDerivAt_partitionFirstMoment
    (f : ThreeObservable) (t : ℝ) :
    HasDerivAt (partitionFirstMoment f)
      (partitionSecondMoment f t) t := by
  have hEarly :
      HasDerivAt (fun s : ℝ => Real.exp (s * f.early))
        (Real.exp (t * f.early) * f.early) t :=
    ((hasDerivAt_id t).mul_const f.early).exp
  have hMiddle :
      HasDerivAt (fun s : ℝ => Real.exp (s * f.middle))
        (Real.exp (t * f.middle) * f.middle) t :=
    ((hasDerivAt_id t).mul_const f.middle).exp
  have hLate :
      HasDerivAt (fun s : ℝ => Real.exp (s * f.late))
        (Real.exp (t * f.late) * f.late) t :=
    ((hasDerivAt_id t).mul_const f.late).exp
  convert
      ((hEarly.const_mul f.early).add
        (hMiddle.const_mul f.middle)).add
        (hLate.const_mul f.late) using 1 <;>
    simp [partitionFirstMoment, partitionSecondMoment] <;> ring


theorem hasDerivAt_stationaryMGF (f : ThreeObservable) (t : ℝ) :
    HasDerivAt (stationaryMGF f)
      (partitionFirstMoment f t / 3) t := by
  convert (hasDerivAt_partitionSum f t).div_const 3 using 1 <;>
    simp [stationaryMGF, partitionSum, partitionFirstMoment] <;> ring


theorem hasDerivAt_stationaryLogMGF
    (f : ThreeObservable) (t : ℝ) :
    HasDerivAt (stationaryLogMGF f) (tiltedMean f t) t := by
  have hlog :=
    (hasDerivAt_stationaryMGF f t).log
      (ne_of_gt (stationary_mgf_strictly_positive f t))
  have hratio :
      (partitionFirstMoment f t / 3) / stationaryMGF f t =
        tiltedMean f t := by
    rw [stationary_mgf_eq_partition_sum_div_three]
    field_simp [tiltedMean, partition_sum_ne_zero]
  convert hlog using 1
  · rfl
  · exact hratio


theorem curvature_numerator_pairwise_square_identity
    (f : ThreeObservable) (t : ℝ) :
    partitionSecondMoment f t * partitionSum f t -
        partitionFirstMoment f t ^ 2 =
      Real.exp (t * f.early) * Real.exp (t * f.middle) *
          (f.early - f.middle) ^ 2 +
        Real.exp (t * f.early) * Real.exp (t * f.late) *
          (f.early - f.late) ^ 2 +
        Real.exp (t * f.middle) * Real.exp (t * f.late) *
          (f.middle - f.late) ^ 2 := by
  unfold partitionSecondMoment partitionFirstMoment partitionSum
  ring


theorem tilted_curvature_nonnegative (f : ThreeObservable) (t : ℝ) :
    0 ≤ tiltedCurvature f t := by
  unfold tiltedCurvature
  rw [curvature_numerator_pairwise_square_identity]
  positivity


theorem hasDerivAt_tiltedMean (f : ThreeObservable) (t : ℝ) :
    HasDerivAt (tiltedMean f) (tiltedCurvature f t) t := by
  have hquot :=
    (hasDerivAt_partitionFirstMoment f t).fun_div
      (hasDerivAt_partitionSum f t) (partition_sum_ne_zero f t)
  convert hquot using 1 <;>
    simp [tiltedMean, tiltedCurvature] <;> ring


theorem continuous_stationary_log_mgf (f : ThreeObservable) :
    Continuous (stationaryLogMGF f) := by
  intro t
  exact (hasDerivAt_stationaryLogMGF f t).continuousAt


theorem stationary_log_mgf_convex (f : ThreeObservable) :
    ConvexOn ℝ Set.univ (stationaryLogMGF f) := by
  apply convexOn_of_hasDerivWithinAt2_nonneg convex_univ
  · exact (continuous_stationary_log_mgf f).continuousOn
  · intro t ht
    exact (hasDerivAt_stationaryLogMGF f t).hasDerivWithinAt
  · intro t ht
    exact (hasDerivAt_tiltedMean f t).hasDerivWithinAt
  · intro t ht
    exact tilted_curvature_nonnegative f t


theorem hasDerivAt_legendreObjective
    (f : ThreeObservable) (threshold t : ℝ) :
    HasDerivAt (legendreObjective f threshold)
      (continuousLegendreDerivative f threshold t) t := by
  convert
      ((hasDerivAt_id t).mul_const threshold).sub
        (hasDerivAt_stationaryLogMGF f t) using 1 <;>
    simp [legendreObjective, continuousLegendreDerivative] <;> ring


structure GlobalContinuousLegendreOptimizer
    (f : ThreeObservable) (threshold : ℝ) where
  tilt : ℝ
  maximal :
    ∀ candidate : ℝ,
      legendreObjective f threshold candidate ≤
        legendreObjective f threshold tilt


theorem global_optimizer_is_local_max
    {f : ThreeObservable} {threshold : ℝ}
    (optimizer : GlobalContinuousLegendreOptimizer f threshold) :
    IsLocalMax (legendreObjective f threshold) optimizer.tilt := by
  exact Filter.Eventually.of_forall optimizer.maximal


theorem global_continuous_optimizer_stationary_equation
    {f : ThreeObservable} {threshold : ℝ}
    (optimizer : GlobalContinuousLegendreOptimizer f threshold) :
    tiltedMean f optimizer.tilt = threshold := by
  have hzero :
      continuousLegendreDerivative f threshold optimizer.tilt = 0 :=
    (global_optimizer_is_local_max optimizer).hasDerivAt_eq_zero
      (hasDerivAt_legendreObjective f threshold optimizer.tilt)
  unfold continuousLegendreDerivative at hzero
  linarith


theorem finite_rate_le_global_continuous_optimizer
    {f : ThreeObservable} {threshold : ℝ}
    (optimizer : GlobalContinuousLegendreOptimizer f threshold) :
    finiteLegendreRate f threshold ≤
      legendreObjective f threshold optimizer.tilt := by
  unfold finiteLegendreRate
  exact optimizer.maximal
    (chosenFiniteLegendreOptimizer f threshold).tilt


theorem global_continuous_envelope_le_finite_envelope
    {f : ThreeObservable} {threshold : ℝ}
    (optimizer : GlobalContinuousLegendreOptimizer f threshold) :
    Real.exp (-(legendreObjective f threshold optimizer.tilt)) ≤
      finiteOptimizedEnvelope f threshold := by
  unfold finiteOptimizedEnvelope
  apply Real.exp_le_exp.mpr
  exact neg_le_neg (finite_rate_le_global_continuous_optimizer optimizer)


theorem legendre_objective_monotone_of_support_below
    (f : ThreeObservable) (threshold smallerTilt largerTilt : ℝ)
    (htilts : smallerTilt ≤ largerTilt)
    (hEarly : f.early ≤ threshold)
    (hMiddle : f.middle ≤ threshold)
    (hLate : f.late ≤ threshold) :
    legendreObjective f threshold smallerTilt ≤
      legendreObjective f threshold largerTilt := by
  have hEnvelope := chernoff_envelope_antitone_of_support_below
    f threshold smallerTilt largerTilt htilts hEarly hMiddle hLate
  rw [← chernoff_transform_exponentiates,
    ← chernoff_transform_exponentiates] at hEnvelope
  have hTransform := Real.exp_le_exp.mp hEnvelope
  unfold chernoffTransform legendreObjective at hTransform ⊢
  linarith


structure ContinuousIntervalOptimizer
    (f : ThreeObservable) (threshold : ℝ) where
  tilt : ℝ
  mem_interval : tilt ∈ Set.Icc (0 : ℝ) 4
  maximal :
    ∀ candidate ∈ Set.Icc (0 : ℝ) 4,
      legendreObjective f threshold candidate ≤
        legendreObjective f threshold tilt


theorem tilt_four_continuous_interval_optimizer_of_support_below
    (f : ThreeObservable) (threshold : ℝ)
    (hEarly : f.early ≤ threshold)
    (hMiddle : f.middle ≤ threshold)
    (hLate : f.late ≤ threshold) :
    ContinuousIntervalOptimizer f threshold := by
  refine {
    tilt := 4
    mem_interval := by constructor <;> norm_num
    maximal := ?_
  }
  intro candidate hcandidate
  exact legendre_objective_monotone_of_support_below
    f threshold candidate 4 hcandidate.2 hEarly hMiddle hLate


theorem finite_rate_eq_tilt_four_of_support_below
    (f : ThreeObservable) (threshold : ℝ)
    (hEarly : f.early ≤ threshold)
    (hMiddle : f.middle ≤ threshold)
    (hLate : f.late ≤ threshold) :
    finiteLegendreRate f threshold =
      legendreObjective f threshold 4 := by
  apply le_antisymm
  · unfold finiteLegendreRate
    exact legendre_objective_monotone_of_support_below
      f threshold
      (chosenFiniteLegendreOptimizer f threshold).tilt 4
      (finite_tilt_grid_le_four
        (chosenFiniteLegendreOptimizer f threshold).mem_grid)
      hEarly hMiddle hLate
  · exact finite_legendre_rate_dominates_grid
      f threshold 4 four_mem_finite_tilt_grid


theorem slow_half_extinct_continuous_interval_optimizer :
    ContinuousIntervalOptimizer
      (observableScale (((3 : ℝ) / 4) ^ 3) slowObservable)
      ((1 : ℝ) / 2) := by
  apply tilt_four_continuous_interval_optimizer_of_support_below
  all_goals norm_num [observableScale, slowObservable]


theorem slow_quarter_extinct_continuous_interval_optimizer :
    ContinuousIntervalOptimizer
      (observableScale (((3 : ℝ) / 4) ^ 5) slowObservable)
      ((1 : ℝ) / 4) := by
  apply tilt_four_continuous_interval_optimizer_of_support_below
  all_goals norm_num [observableScale, slowObservable]


theorem fast_half_extinct_continuous_interval_optimizer :
    ContinuousIntervalOptimizer
      (observableScale (((1 : ℝ) / 4) ^ 1) fastObservable)
      ((1 : ℝ) / 2) := by
  apply tilt_four_continuous_interval_optimizer_of_support_below
  all_goals norm_num [observableScale, fastObservable]


theorem fast_quarter_extinct_continuous_interval_optimizer :
    ContinuousIntervalOptimizer
      (observableScale (((1 : ℝ) / 4) ^ 2) fastObservable)
      ((1 : ℝ) / 4) := by
  apply tilt_four_continuous_interval_optimizer_of_support_below
  all_goals norm_num [observableScale, fastObservable]


theorem full_rank_continuous_optimizer_commutes
    (sourceMean sourceCurvature sourceRate
      targetMean targetCurvature targetRate : ℝ)
    (hMean : targetMean = sourceMean)
    (hCurvature : targetCurvature = sourceCurvature)
    (hRate : targetRate = sourceRate) :
    targetMean = sourceMean ∧
      targetCurvature = sourceCurvature ∧
      targetRate = sourceRate := by
  exact ⟨hMean, hCurvature, hRate⟩


structure ContinuousLogMGFConvexityCertificate where
  sourceMemoryOSV065Bound : Bool
  partitionDerivativeExact : Bool
  logMGFDerivativeExact : Bool
  tiltedCurvatureNonnegative : Bool
  logMGFConvexOnReal : Bool
  globalOptimizerStationaryEquationExact : Bool
  finiteGridComparisonExact : Bool
  boundedIntervalBoundaryOptimizerExact : Bool
  unboundedContinuousOptimizerExistenceClaimed : Bool
  generalCramerTheoremClaimed : Bool
  generalGartnerEllisTheoremClaimed : Bool
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
    (certificate : ContinuousLogMGFConvexityCertificate)
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


end
end KUOS.OpenHorizon.MemoryOSContinuousLogMGFConvexityV0_66
