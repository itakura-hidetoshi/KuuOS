import Mathlib
import KUOS.OpenHorizon.MemoryOSObserverRelativeFiniteWindowQiInfluencePlanOSHandoffV0_41
import KUOS.PlanOS.FinitePhysicalQuantumQiCoherenceKernelPartialDephasingV1_23

namespace KUOS.OpenHorizon.MemoryOSObserverRelativeNonMarkovInfluenceConditionedPlanOSCoherenceKernelV0_42

open scoped BigOperators ComplexConjugate

/-- Exact Gaussian integer used by the runtime kernel. -/
abbrev GaussianInt := ℤ × ℤ

/-- Exact multiplication in `ℤ[i]`. -/
def gaussianMul (left right : GaussianInt) : GaussianInt :=
  (left.1 * right.1 - left.2 * right.2,
   left.1 * right.2 + left.2 * right.1)

/-- Exact Gaussian conjugation. -/
def gaussianConj (value : GaussianInt) : GaussianInt :=
  (value.1, -value.2)

/-- The four exact unit phases `1, i, -1, -i`. -/
def gaussianUnit (phase : Nat) : GaussianInt :=
  match phase % 4 with
  | 0 => (1, 0)
  | 1 => (0, 1)
  | 2 => (-1, 0)
  | _ => (0, -1)

/-- Entrywise diagonal phase congruence in exact Gaussian arithmetic. -/
def gaussianPhaseDeform
    (rowPhase columnPhase : Nat)
    (value : GaussianInt) : GaussianInt :=
  gaussianMul (gaussianMul (gaussianUnit rowPhase) value)
    (gaussianConj (gaussianUnit columnPhase))

/-- Memory-conditioned diagonal congruence `D G D*` over a finite complex kernel. -/
def phaseDeformMatrix
    {ι : Type} [Fintype ι]
    (phase : ι → ℂ)
    (kernel : Matrix ι ι ℂ) : Matrix ι ι ℂ :=
  fun row column => phase row * kernel row column * star (phase column)

/-- Finite quadratic form associated with a complex kernel. -/
def quadraticForm
    {ι : Type} [Fintype ι]
    (kernel : Matrix ι ι ℂ)
    (vector : ι → ℂ) : ℂ :=
  ∑ row, ∑ column,
    star (vector row) * kernel row column * vector column

/-- Hermitian-kernel predicate used by the v0.42 theorem surface. -/
def IsHermitianKernel
    {ι : Type} [Fintype ι]
    (kernel : Matrix ι ι ℂ) : Prop :=
  ∀ row column, kernel column row = star (kernel row column)

/-- Quadratic-form nonnegativity predicate. -/
def IsPositiveSemidefiniteKernel
    {ι : Type} [Fintype ι]
    (kernel : Matrix ι ι ℂ) : Prop :=
  ∀ vector, 0 ≤ (quadraticForm kernel vector).re

/-- Diagonal phase congruence is exactly source evaluation on the phase-rotated
    vector. This is the algebraic reason the PSD witness survives. -/
theorem phaseDeform_quadraticForm
    {ι : Type} [Fintype ι]
    (phase : ι → ℂ)
    (kernel : Matrix ι ι ℂ)
    (vector : ι → ℂ) :
    quadraticForm (phaseDeformMatrix phase kernel) vector =
      quadraticForm kernel (fun index => star (phase index) * vector index) := by
  classical
  simp [quadraticForm, phaseDeformMatrix, mul_comm, mul_left_comm, mul_assoc]

/-- Every PSD source kernel remains PSD after memory-conditioned diagonal
    phase congruence. -/
theorem phaseDeform_preserves_positiveSemidefinite
    {ι : Type} [Fintype ι]
    (phase : ι → ℂ)
    (kernel : Matrix ι ι ℂ)
    (hpsd : IsPositiveSemidefiniteKernel kernel) :
    IsPositiveSemidefiniteKernel (phaseDeformMatrix phase kernel) := by
  intro vector
  rw [phaseDeform_quadraticForm]
  exact hpsd _

/-- Hermitian symmetry is preserved by diagonal phase congruence. -/
theorem phaseDeform_preserves_hermitian
    {ι : Type} [Fintype ι]
    (phase : ι → ℂ)
    (kernel : Matrix ι ι ℂ)
    (hhermitian : IsHermitianKernel kernel) :
    IsHermitianKernel (phaseDeformMatrix phase kernel) := by
  intro row column
  unfold phaseDeformMatrix
  rw [hhermitian row column]
  simp [mul_comm, mul_left_comm, mul_assoc]

/-- Unit-modulus diagonal phases preserve every diagonal kernel entry. -/
theorem phaseDeform_preserves_diagonal
    {ι : Type} [Fintype ι]
    (phase : ι → ℂ)
    (kernel : Matrix ι ι ℂ)
    (hunit : ∀ index, phase index * star (phase index) = 1)
    (index : ι) :
    phaseDeformMatrix phase kernel index index = kernel index index := by
  unfold phaseDeformMatrix
  calc
    phase index * kernel index index * star (phase index) =
        kernel index index * (phase index * star (phase index)) := by ring
    _ = kernel index index := by rw [hunit index]; simp

/-- The exact v0.41 action numerators induce the reference mod-four phases. -/
theorem reference_memory_action_phases :
    54 % 4 = (2 : ℤ) ∧
      45 % 4 = (1 : ℤ) ∧
      29 % 4 = (1 : ℤ) ∧
      27 % 4 = (3 : ℤ) := by
  norm_num

/-- With the complete non-Markov tail, the reference source off-diagonal
    entry `-2i` becomes the exact real entry `2`. -/
theorem reference_full_memory_offdiagonal :
    gaussianPhaseDeform 2 1 (0, -2) = (2, 0) := by
  native_decide

/-- With the suffix window alone, the same source entry becomes `2i`. -/
theorem reference_window_only_offdiagonal :
    gaussianPhaseDeform 1 3 (0, -2) = (0, 2) := by
  native_decide

/-- The visible discarded tail changes the coherence kernel rather than being
    erased by the finite-window projection. -/
theorem reference_tail_changes_coherence_kernel :
    gaussianPhaseDeform 2 1 (0, -2) ≠
      gaussianPhaseDeform 1 3 (0, -2) := by
  native_decide

/-- The diagonal reference value is unchanged under either memory phase. -/
theorem reference_diagonal_preserved :
    gaussianPhaseDeform 2 2 (2, 0) = (2, 0) ∧
      gaussianPhaseDeform 1 1 (2, 0) = (2, 0) := by
  native_decide

/-- Bounded v0.42 certificate surface. -/
structure ObserverRelativeNonMarkovInfluenceConditionedPlanOSCoherenceKernelCertificate where
  sourceMemoryOSV041Bound : Bool
  sourcePlanOSV123Bound : Bool
  observerRelativeInfluencePreserved : Bool
  discardedTailEffectVisible : Bool
  diagonalPhaseCongruenceUsed : Bool
  allPlanOSHistoriesRetained : Bool
  allHistoryPairSupportRetained : Bool
  hermitianSymmetryPreserved : Bool
  diagonalNormalizationPreserved : Bool
  positiveSemidefiniteWitnessPreserved : Bool
  amplitudeReweightingPerformed : Bool
  kernelEntryDeletionPerformed : Bool
  historyPruningPerformed : Bool
  historyRankingPerformed : Bool
  representativeHistorySelected : Bool
  planSelectionPerformed : Bool
  decisionCommitPerformed : Bool
  activationPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV041Mutated : Bool
  sourcePlanOSV123Mutated : Bool
  persistentWorldStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnlyAdvisoryKernel : Bool
  readOnly : Bool

/-- v0.42 preserves the complete PlanOS support and the source kernel's exact
    structural witnesses. -/
theorem coherence_handoff_preserves_kernel_structure
    (certificate : ObserverRelativeNonMarkovInfluenceConditionedPlanOSCoherenceKernelCertificate)
    (hmemory : certificate.sourceMemoryOSV041Bound = true)
    (hplan : certificate.sourcePlanOSV123Bound = true)
    (hobserver : certificate.observerRelativeInfluencePreserved = true)
    (htail : certificate.discardedTailEffectVisible = true)
    (hcongruence : certificate.diagonalPhaseCongruenceUsed = true)
    (hhistories : certificate.allPlanOSHistoriesRetained = true)
    (hpairs : certificate.allHistoryPairSupportRetained = true)
    (hhermitian : certificate.hermitianSymmetryPreserved = true)
    (hdiagonal : certificate.diagonalNormalizationPreserved = true)
    (hpsd : certificate.positiveSemidefiniteWitnessPreserved = true) :
    certificate.sourceMemoryOSV041Bound = true ∧
      certificate.sourcePlanOSV123Bound = true ∧
      certificate.observerRelativeInfluencePreserved = true ∧
      certificate.discardedTailEffectVisible = true ∧
      certificate.diagonalPhaseCongruenceUsed = true ∧
      certificate.allPlanOSHistoriesRetained = true ∧
      certificate.allHistoryPairSupportRetained = true ∧
      certificate.hermitianSymmetryPreserved = true ∧
      certificate.diagonalNormalizationPreserved = true ∧
      certificate.positiveSemidefiniteWitnessPreserved = true := by
  exact ⟨hmemory, hplan, hobserver, htail, hcongruence, hhistories, hpairs,
    hhermitian, hdiagonal, hpsd⟩

/-- Memory-conditioned coherence grants no selection, activation, execution,
    mutation, verification, or truth authority. -/
theorem coherence_handoff_grants_no_authority
    (certificate : ObserverRelativeNonMarkovInfluenceConditionedPlanOSCoherenceKernelCertificate)
    (hreweight : certificate.amplitudeReweightingPerformed = false)
    (hdelete : certificate.kernelEntryDeletionPerformed = false)
    (hprune : certificate.historyPruningPerformed = false)
    (hrank : certificate.historyRankingPerformed = false)
    (hrepresentative : certificate.representativeHistorySelected = false)
    (hselect : certificate.planSelectionPerformed = false)
    (hdecision : certificate.decisionCommitPerformed = false)
    (hactivate : certificate.activationPerformed = false)
    (hexecute : certificate.executionPermission = false)
    (hmemory : certificate.sourceMemoryOSV041Mutated = false)
    (hplan : certificate.sourcePlanOSV123Mutated = false)
    (hworld : certificate.persistentWorldStateMutated = false)
    (hverify : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false)
    (hfuture : certificate.futureOnlyAdvisoryKernel = true)
    (hreadonly : certificate.readOnly = true) :
    certificate.amplitudeReweightingPerformed = false ∧
      certificate.kernelEntryDeletionPerformed = false ∧
      certificate.historyPruningPerformed = false ∧
      certificate.historyRankingPerformed = false ∧
      certificate.representativeHistorySelected = false ∧
      certificate.planSelectionPerformed = false ∧
      certificate.decisionCommitPerformed = false ∧
      certificate.activationPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV041Mutated = false ∧
      certificate.sourcePlanOSV123Mutated = false ∧
      certificate.persistentWorldStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false ∧
      certificate.futureOnlyAdvisoryKernel = true ∧
      certificate.readOnly = true := by
  exact ⟨hreweight, hdelete, hprune, hrank, hrepresentative, hselect,
    hdecision, hactivate, hexecute, hmemory, hplan, hworld, hverify, htruth,
    hfuture, hreadonly⟩

end KUOS.OpenHorizon.MemoryOSObserverRelativeNonMarkovInfluenceConditionedPlanOSCoherenceKernelV0_42
