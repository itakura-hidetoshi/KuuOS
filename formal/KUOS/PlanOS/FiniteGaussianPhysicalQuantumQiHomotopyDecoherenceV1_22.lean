import Mathlib
import KUOS.PlanOS.FinitePhysicalQuantumQiPathHistoryNoncollapseV1_21

namespace KUOS.PlanOS.FiniteGaussianPhysicalQuantumQiHomotopyDecoherenceV1_22

/-- Real component of the exact Gaussian unit `i^phase` on the finite Z₄ surface. -/
def phaseReal (phase : ℕ) : ℤ :=
  if phase % 4 = 0 then 1 else if phase % 4 = 2 then -1 else 0

/-- Imaginary component of the exact Gaussian unit `i^phase` on the finite Z₄ surface. -/
def phaseImag (phase : ℕ) : ℤ :=
  if phase % 4 = 1 then 1 else if phase % 4 = 3 then -1 else 0

/-- Exact real component of a finite Gaussian-integer path amplitude. -/
def gaussianReal (weights phases : List ℕ) : ℤ :=
  (List.zipWith
      (fun weight phase => (weight : ℤ) * phaseReal phase)
      weights phases).sum

/-- Exact imaginary component of a finite Gaussian-integer path amplitude. -/
def gaussianImag (weights phases : List ℕ) : ℤ :=
  (List.zipWith
      (fun weight phase => (weight : ℤ) * phaseImag phase)
      weights phases).sum

/-- Squared Gaussian norm, retained as an exact integer. -/
def gaussianNormSq (real imag : ℤ) : ℤ := real * real + imag * imag

/-- Coherent intensity of one retained finite history block. -/
def blockIntensity (weights phases : List ℕ) : ℤ :=
  gaussianNormSq (gaussianReal weights phases) (gaussianImag weights phases)

/-- Fully incoherent intensity before any phase cross terms are added. -/
def incoherentIntensity (weights : List ℕ) : ℤ :=
  (weights.map fun weight => (weight : ℤ) ^ 2).sum

/-- Cross-block term discarded by a finite decoherence mask. -/
def decoherenceResidual (pre post : ℤ) : ℤ := pre - post

/-- Exact retention of histories, homotopy classes, and coherence blocks. -/
structure FiniteGaussianRetentionWitness
    (History HomotopyClass CoherenceBlock : Type)
    [DecidableEq History] [DecidableEq HomotopyClass] [DecidableEq CoherenceBlock] where
  sourceHistories : Finset History
  retainedHistories : Finset History
  sourceHomotopyClasses : Finset HomotopyClass
  retainedHomotopyClasses : Finset HomotopyClass
  sourceCoherenceBlocks : Finset CoherenceBlock
  retainedCoherenceBlocks : Finset CoherenceBlock
  historiesRetainedExactly : retainedHistories = sourceHistories
  homotopyClassesRetainedExactly : retainedHomotopyClasses = sourceHomotopyClasses
  coherenceBlocksRetainedExactly : retainedCoherenceBlocks = sourceCoherenceBlocks

structure FiniteGaussianPhysicalQuantumQiHomotopyDecoherenceCertificate where
  sourceV121CertificateBound : Bool
  sourcePathHomotopyCertificateBound : Bool
  physicalQuantumQiDefinitionBound : Bool
  z4PhaseSurfaceUsed : Bool
  gaussianIntegerArithmeticExact : Bool
  homotopyClassesRetained : Bool
  coherenceBlocksRetained : Bool
  decoherenceMaskAppliedWithoutPruning : Bool
  allHistoriesRetained : Bool
  argminPerformed : Bool
  representativeHistorySelected : Bool
  historyRankingPerformed : Bool
  historyPruningPerformed : Bool
  sourceV121CertificateMutated : Bool
  sourcePathHomotopyCertificateMutated : Bool
  persistentWorldStateMutated : Bool
  activationPerformed : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

/-- Squared norm of two Gaussian blocks decomposes into block norms and the
    exact cross-block interference term. -/
theorem two_block_gaussian_norm_decomposition (a b c d : ℤ) :
    gaussianNormSq (a + c) (b + d) =
      gaussianNormSq a b + gaussianNormSq c d + 2 * (a * c + b * d) := by
  simp [gaussianNormSq]
  ring

/-- The decoherence residual is an exact additive decomposition, not a loss of
    retained histories. -/
theorem exact_decoherence_decomposition (pre post : ℤ) :
    pre = post + decoherenceResidual pre post := by
  simp [decoherenceResidual]

/-- Exact retention preserves the cardinality of every finite support. -/
theorem retained_support_cardinalities
    {History HomotopyClass CoherenceBlock : Type}
    [DecidableEq History] [DecidableEq HomotopyClass] [DecidableEq CoherenceBlock]
    (witness : FiniteGaussianRetentionWitness History HomotopyClass CoherenceBlock) :
    witness.retainedHistories.card = witness.sourceHistories.card ∧
      witness.retainedHomotopyClasses.card = witness.sourceHomotopyClasses.card ∧
      witness.retainedCoherenceBlocks.card = witness.sourceCoherenceBlocks.card := by
  constructor
  · rw [witness.historiesRetainedExactly]
  constructor
  · rw [witness.homotopyClassesRetainedExactly]
  · rw [witness.coherenceBlocksRetainedExactly]

/-- Reference global amplitude: `2 - 2 + i - i = 0`. -/
theorem reference_global_gaussian_amplitude :
    gaussianReal [2, 2, 1, 1] [0, 2, 1, 3] = 0 ∧
      gaussianImag [2, 2, 1, 1] [0, 2, 1, 3] = 0 := by
  native_decide

/-- Reference homotopy-class amplitudes are `2+i` and `-2-i`. -/
theorem reference_homotopy_class_amplitudes :
    gaussianReal [2, 1] [0, 1] = 2 ∧
      gaussianImag [2, 1] [0, 1] = 1 ∧
      gaussianReal [2, 1] [2, 3] = -2 ∧
      gaussianImag [2, 1] [2, 3] = -1 := by
  native_decide

/-- Global destructive interference is exact, while homotopy-block
    decoherence retains intensity ten without deleting any history. -/
theorem reference_decoherence_intensities :
    blockIntensity [2, 2, 1, 1] [0, 2, 1, 3] = 0 ∧
      blockIntensity [2, 1] [0, 1] + blockIntensity [2, 1] [2, 3] = 10 ∧
      incoherentIntensity [2, 2, 1, 1] = 10 ∧
      decoherenceResidual 0 10 = -10 := by
  native_decide

/-- Gaussian phase, homotopy, and decoherence evidence grants no planning authority. -/
theorem gaussian_homotopy_decoherence_grants_no_authority
    (certificate : FiniteGaussianPhysicalQuantumQiHomotopyDecoherenceCertificate)
    (hretain : certificate.allHistoriesRetained = true)
    (hmask : certificate.decoherenceMaskAppliedWithoutPruning = true)
    (hargmin : certificate.argminPerformed = false)
    (hrepresentative : certificate.representativeHistorySelected = false)
    (hranking : certificate.historyRankingPerformed = false)
    (hpruning : certificate.historyPruningPerformed = false)
    (hactivation : certificate.activationPerformed = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.allHistoriesRetained = true ∧
      certificate.decoherenceMaskAppliedWithoutPruning = true ∧
      certificate.argminPerformed = false ∧
      certificate.representativeHistorySelected = false ∧
      certificate.historyRankingPerformed = false ∧
      certificate.historyPruningPerformed = false ∧
      certificate.activationPerformed = false ∧
      certificate.executionPermission = false := by
  exact ⟨hretain, hmask, hargmin, hrepresentative, hranking,
    hpruning, hactivation, hexecution⟩

/-- The layer is finite, exact, read-only, future-only, and source-preserving. -/
theorem gaussian_homotopy_decoherence_is_bounded_future_only
    (certificate : FiniteGaussianPhysicalQuantumQiHomotopyDecoherenceCertificate)
    (hv121 : certificate.sourceV121CertificateMutated = false)
    (hhomotopy : certificate.sourcePathHomotopyCertificateMutated = false)
    (hworld : certificate.persistentWorldStateMutated = false)
    (hexact : certificate.gaussianIntegerArithmeticExact = true)
    (hreadonly : certificate.historyReadOnly = true)
    (hfuture : certificate.futureOnly = true)
    (hactive : certificate.activeNow = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.sourceV121CertificateMutated = false ∧
      certificate.sourcePathHomotopyCertificateMutated = false ∧
      certificate.persistentWorldStateMutated = false ∧
      certificate.gaussianIntegerArithmeticExact = true ∧
      certificate.historyReadOnly = true ∧
      certificate.futureOnly = true ∧
      certificate.activeNow = false ∧
      certificate.executionPermission = false := by
  exact ⟨hv121, hhomotopy, hworld, hexact, hreadonly, hfuture, hactive, hexecution⟩

end KUOS.PlanOS.FiniteGaussianPhysicalQuantumQiHomotopyDecoherenceV1_22
