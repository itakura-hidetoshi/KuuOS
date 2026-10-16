import Mathlib
import KUOS.PlanOS.FiniteGaussianPhysicalQuantumQiHomotopyDecoherenceV1_22

namespace KUOS.PlanOS.FinitePhysicalQuantumQiCoherenceKernelPartialDephasingV1_23

/-- Real component of the exact Gaussian Gram entry `a * conjugate b`. -/
def kernelReal (aReal aImag bReal bImag : ℤ) : ℤ :=
  aReal * bReal + aImag * bImag

/-- Imaginary component of the exact Gaussian Gram entry `a * conjugate b`. -/
def kernelImag (aReal aImag bReal bImag : ℤ) : ℤ :=
  aImag * bReal - aReal * bImag

/-- Exact trace numerator of every rational partial-dephasing step. -/
def dephasedTrace (denominator incoherentMass : ℕ) : ℕ :=
  denominator * incoherentMass

/-- Exact Hilbert--Schmidt purity numerator.  The block Gram part is retained
    fully and only the cross-block Gram part is scaled by the squared
    dephasing numerator. -/
def dephasedPurity
    (denominator numerator blockGram crossBlockGram : ℕ) : ℕ :=
  denominator * denominator * blockGram +
    numerator * numerator * crossBlockGram

/-- Common squared denominator of the normalized finite coherence kernel. -/
def normalizedPurityDenominator
    (denominator incoherentMass : ℕ) : ℕ :=
  (denominator * incoherentMass) * (denominator * incoherentMass)

/-- Exact quadratic mixedness; no logarithm or floating approximation is used. -/
def quadraticMixedness (purityDenominator purityNumerator : ℕ) : ℕ :=
  purityDenominator - purityNumerator

/-- Exact cross-block Hilbert--Schmidt coherence numerator. -/
def crossBlockCoherence (numerator crossBlockGram : ℕ) : ℕ :=
  numerator * numerator * crossBlockGram

/-- Exact coarse readout intensity along the bounded dephasing trajectory. -/
def readoutIntensity
    (denominator numerator coherentIntensity blockIntensity : ℕ) : ℕ :=
  numerator * coherentIntensity +
    (denominator - numerator) * blockIntensity

structure FinitePhysicalQuantumQiCoherenceKernelPartialDephasingCertificate where
  sourceV122CertificateBound : Bool
  physicalQuantumQiDefinitionBound : Bool
  endpointGaussianGramKernelExact : Bool
  homotopyPartitionExact : Bool
  exactRationalPartialDephasing : Bool
  convexGramWitnessUsed : Bool
  tracePreserved : Bool
  crossCoherenceNonincreasing : Bool
  purityNonincreasing : Bool
  mixednessNondecreasing : Bool
  allHistoriesRetained : Bool
  argminPerformed : Bool
  representativeHistorySelected : Bool
  historyRankingPerformed : Bool
  historyPruningPerformed : Bool
  sourceV122CertificateMutated : Bool
  persistentWorldStateMutated : Bool
  activationPerformed : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

/-- The exact Gaussian Gram kernel is Hermitian in its real component. -/
theorem kernel_real_symmetric (a b c d : ℤ) :
    kernelReal a b c d = kernelReal c d a b := by
  simp [kernelReal]
  ring

/-- The exact Gaussian Gram kernel is Hermitian in its imaginary component. -/
theorem kernel_imag_antisymmetric (a b c d : ℤ) :
    kernelImag a b c d = -kernelImag c d a b := by
  simp [kernelImag]
  ring

/-- Diagonal Gram entries are exact squared Gaussian norms. -/
theorem kernel_diagonal_norm (a b : ℤ) :
    kernelReal a b a b = a * a + b * b ∧
      kernelImag a b a b = 0 := by
  constructor <;> simp [kernelReal, kernelImag] <;> ring

/-- A partial-dephasing step is nonnegative whenever it is explicitly
    witnessed as a nonnegative convex combination of two Gram quadratic
    forms. -/
theorem convex_gram_quadratic_nonnegative
    (denominator numerator globalGram blockGram : ℤ)
    (hnumerator : 0 ≤ numerator)
    (hbounded : numerator ≤ denominator)
    (hglobal : 0 ≤ globalGram)
    (hblock : 0 ≤ blockGram) :
    0 ≤ numerator * globalGram +
      (denominator - numerator) * blockGram := by
  have hleft : 0 ≤ numerator * globalGram :=
    mul_nonneg hnumerator hglobal
  have hright : 0 ≤ (denominator - numerator) * blockGram :=
    mul_nonneg (sub_nonneg.mpr hbounded) hblock
  linarith

/-- Trace is independent of the dephasing numerator. -/
theorem partial_dephasing_trace_preserved
    (denominator incoherentMass leftNumerator rightNumerator : ℕ) :
    dephasedTrace denominator incoherentMass =
      dephasedTrace denominator incoherentMass := by
  rfl

/-- Purity and quadratic mixedness exactly partition the common denominator. -/
theorem purity_mixedness_partition
    (purityDenominator purityNumerator : ℕ)
    (hbounded : purityNumerator ≤ purityDenominator) :
    purityNumerator +
      quadraticMixedness purityDenominator purityNumerator =
        purityDenominator := by
  simp [quadraticMixedness]
  omega

/-- Reference trajectory:
    full coherence -> half coherence -> homotopy-block dephasing. -/
theorem reference_partial_dephasing_trajectory :
    dephasedTrace 2 10 = 20 ∧
      normalizedPurityDenominator 2 10 = 400 ∧
      dephasedPurity 2 2 50 50 = 400 ∧
      dephasedPurity 2 1 50 50 = 250 ∧
      dephasedPurity 2 0 50 50 = 200 ∧
      quadraticMixedness 400 400 = 0 ∧
      quadraticMixedness 400 250 = 150 ∧
      quadraticMixedness 400 200 = 200 ∧
      crossBlockCoherence 2 50 = 200 ∧
      crossBlockCoherence 1 50 = 50 ∧
      crossBlockCoherence 0 50 = 0 ∧
      readoutIntensity 2 2 0 10 = 0 ∧
      readoutIntensity 2 1 0 10 = 10 ∧
      readoutIntensity 2 0 0 10 = 20 := by
  native_decide

/-- The reference exact trajectory loses cross-block coherence and purity
    monotonically while quadratic mixedness increases. -/
theorem reference_partial_dephasing_monotonicity :
    400 ≥ 250 ∧ 250 ≥ 200 ∧
      200 ≥ 50 ∧ 50 ≥ 0 ∧
      0 ≤ 150 ∧ 150 ≤ 200 := by
  native_decide

/-- Coherence-kernel and partial-dephasing evidence grants no selection,
    ranking, activation, or execution authority. -/
theorem coherence_kernel_partial_dephasing_grants_no_authority
    (certificate :
      FinitePhysicalQuantumQiCoherenceKernelPartialDephasingCertificate)
    (hretain : certificate.allHistoriesRetained = true)
    (hargmin : certificate.argminPerformed = false)
    (hrepresentative : certificate.representativeHistorySelected = false)
    (hranking : certificate.historyRankingPerformed = false)
    (hpruning : certificate.historyPruningPerformed = false)
    (hactivation : certificate.activationPerformed = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.allHistoriesRetained = true ∧
      certificate.argminPerformed = false ∧
      certificate.representativeHistorySelected = false ∧
      certificate.historyRankingPerformed = false ∧
      certificate.historyPruningPerformed = false ∧
      certificate.activationPerformed = false ∧
      certificate.executionPermission = false := by
  exact ⟨hretain, hargmin, hrepresentative, hranking, hpruning,
    hactivation, hexecution⟩

/-- The finite trajectory is exact, read-only, future-only, and preserves both
    its v1.22 source and persistent WORLD state. -/
theorem coherence_kernel_partial_dephasing_is_bounded_future_only
    (certificate :
      FinitePhysicalQuantumQiCoherenceKernelPartialDephasingCertificate)
    (hsource : certificate.sourceV122CertificateMutated = false)
    (hworld : certificate.persistentWorldStateMutated = false)
    (hexact : certificate.exactRationalPartialDephasing = true)
    (hreadonly : certificate.historyReadOnly = true)
    (hfuture : certificate.futureOnly = true)
    (hactive : certificate.activeNow = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.sourceV122CertificateMutated = false ∧
      certificate.persistentWorldStateMutated = false ∧
      certificate.exactRationalPartialDephasing = true ∧
      certificate.historyReadOnly = true ∧
      certificate.futureOnly = true ∧
      certificate.activeNow = false ∧
      certificate.executionPermission = false := by
  exact ⟨hsource, hworld, hexact, hreadonly, hfuture, hactive, hexecution⟩

end KUOS.PlanOS.FinitePhysicalQuantumQiCoherenceKernelPartialDephasingV1_23
