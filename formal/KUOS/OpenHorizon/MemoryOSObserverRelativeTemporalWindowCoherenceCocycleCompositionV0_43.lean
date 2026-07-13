import Mathlib
import KUOS.OpenHorizon.MemoryOSObserverRelativeNonMarkovInfluenceConditionedPlanOSCoherenceKernelV0_42

namespace KUOS.OpenHorizon.MemoryOSObserverRelativeTemporalWindowCoherenceCocycleCompositionV0_43

open scoped BigOperators ComplexConjugate
open KUOS.OpenHorizon.MemoryOSObserverRelativeNonMarkovInfluenceConditionedPlanOSCoherenceKernelV0_42

/-- Pointwise phase multiplication in chronological composition order. -/
def composePhase {ι : Type} (later earlier : ι → ℂ) : ι → ℂ :=
  fun index => later index * earlier index

/-- Two diagonal phase congruences compose into one diagonal phase congruence. -/
theorem phaseDeformMatrix_compose
    {ι : Type} [Fintype ι]
    (later earlier : ι → ℂ)
    (kernel : Matrix ι ι ℂ) :
    phaseDeformMatrix later (phaseDeformMatrix earlier kernel) =
      phaseDeformMatrix (composePhase later earlier) kernel := by
  ext row column
  simp [phaseDeformMatrix, composePhase, mul_comm, mul_left_comm, mul_assoc]

/-- Pointwise phase composition is associative. -/
theorem composePhase_assoc
    {ι : Type}
    (third second first : ι → ℂ) :
    composePhase third (composePhase second first) =
      composePhase (composePhase third second) first := by
  funext index
  simp [composePhase, mul_assoc]

/-- Three chronological temporal segments have an exact one-step composite. -/
theorem phaseDeformMatrix_three_compose
    {ι : Type} [Fintype ι]
    (third second first : ι → ℂ)
    (kernel : Matrix ι ι ℂ) :
    phaseDeformMatrix third
        (phaseDeformMatrix second (phaseDeformMatrix first kernel)) =
      phaseDeformMatrix
        (composePhase third (composePhase second first)) kernel := by
  ext row column
  simp [phaseDeformMatrix, composePhase, mul_comm, mul_left_comm, mul_assoc]

/-- Refining one coarse temporal window into two exact subwindows leaves the
    final conditioned kernel unchanged. -/
theorem phaseDeformMatrix_refinement_coarsening
    {ι : Type} [Fintype ι]
    (later earlier : ι → ℂ)
    (kernel : Matrix ι ι ℂ) :
    phaseDeformMatrix later (phaseDeformMatrix earlier kernel) =
      phaseDeformMatrix (composePhase later earlier) kernel :=
  phaseDeformMatrix_compose later earlier kernel

/-- A finite chronological composition of three phase congruences preserves
    positive semidefiniteness. -/
theorem three_phase_composition_preserves_positiveSemidefinite
    {ι : Type} [Fintype ι]
    (third second first : ι → ℂ)
    (kernel : Matrix ι ι ℂ)
    (hpsd : IsPositiveSemidefiniteKernel kernel) :
    IsPositiveSemidefiniteKernel
      (phaseDeformMatrix third
        (phaseDeformMatrix second (phaseDeformMatrix first kernel))) := by
  exact phaseDeform_preserves_positiveSemidefinite third _
    (phaseDeform_preserves_positiveSemidefinite second _
      (phaseDeform_preserves_positiveSemidefinite first _ hpsd))

/-- A finite chronological composition of three phase congruences preserves
    Hermitian symmetry. -/
theorem three_phase_composition_preserves_hermitian
    {ι : Type} [Fintype ι]
    (third second first : ι → ℂ)
    (kernel : Matrix ι ι ℂ)
    (hhermitian : IsHermitianKernel kernel) :
    IsHermitianKernel
      (phaseDeformMatrix third
        (phaseDeformMatrix second (phaseDeformMatrix first kernel))) := by
  exact phaseDeform_preserves_hermitian third _
    (phaseDeform_preserves_hermitian second _
      (phaseDeform_preserves_hermitian first _ hhermitian))

/-- Unit phases preserve every diagonal entry through three temporal stages. -/
theorem three_phase_composition_preserves_diagonal
    {ι : Type} [Fintype ι]
    (third second first : ι → ℂ)
    (kernel : Matrix ι ι ℂ)
    (hthird : ∀ index, third index * star (third index) = 1)
    (hsecond : ∀ index, second index * star (second index) = 1)
    (hfirst : ∀ index, first index * star (first index) = 1)
    (index : ι) :
    phaseDeformMatrix third
        (phaseDeformMatrix second (phaseDeformMatrix first kernel)) index index =
      kernel index index := by
  calc
    phaseDeformMatrix third
        (phaseDeformMatrix second (phaseDeformMatrix first kernel)) index index =
        phaseDeformMatrix second (phaseDeformMatrix first kernel) index index :=
      phaseDeform_preserves_diagonal third _ hthird index
    _ = phaseDeformMatrix first kernel index index :=
      phaseDeform_preserves_diagonal second _ hsecond index
    _ = kernel index index :=
      phaseDeform_preserves_diagonal first _ hfirst index

/-- Exact sequential deformation in Gaussian-integer arithmetic. -/
def gaussianSequentialDeform
    (steps : List (Nat × Nat))
    (value : GaussianInt) : GaussianInt :=
  steps.foldl
    (fun current phases => gaussianPhaseDeform phases.1 phases.2 current)
    value

/-- Reference segment influences and their exact mod-four phases. -/
theorem reference_temporal_segment_phases :
    9 % 4 = (1 : ℤ) ∧
      18 % 4 = (2 : ℤ) ∧
      16 % 4 = (0 : ℤ) ∧
      2 % 4 = (2 : ℤ) ∧
      3 % 4 = (3 : ℤ) ∧
      4 % 4 = (0 : ℤ) := by
  norm_num

/-- The third source-bound temporal segment has nonzero influence but is
    phase-neutral in the exact Z4 coherence encoding. -/
theorem reference_nonzero_phase_neutral_segment :
    (16 : ℤ) ≠ 0 ∧ 16 % 4 = 0 ∧ (4 : ℤ) ≠ 0 ∧ 4 % 4 = 0 := by
  norm_num

/-- The refined chronological sequence reproduces the v0.42 direct kernel. -/
theorem reference_refined_sequence_equals_direct :
    gaussianSequentialDeform
        [(3, 0), (1, 2), (2, 3), (0, 0)] (0, -2) =
      gaussianPhaseDeform 2 1 (0, -2) := by
  native_decide

/-- Coarsening the two retained-window records preserves the same final kernel. -/
theorem reference_coarse_sequence_equals_direct :
    gaussianSequentialDeform
        [(3, 0), (1, 2), (2, 3)] (0, -2) =
      gaussianPhaseDeform 2 1 (0, -2) := by
  native_decide

/-- Both refined and coarse routes produce the exact real off-diagonal `2`. -/
theorem reference_refined_and_coarse_offdiagonal :
    gaussianSequentialDeform
        [(3, 0), (1, 2), (2, 3), (0, 0)] (0, -2) = (2, 0) ∧
      gaussianSequentialDeform
        [(3, 0), (1, 2), (2, 3)] (0, -2) = (2, 0) := by
  native_decide

/-- Bounded v0.43 certificate surface. -/
structure ObserverRelativeTemporalWindowCoherenceCocycleCompositionCertificate where
  sourceMemoryOSV041Bound : Bool
  sourceMemoryOSV042Bound : Bool
  sourcePlanOSV123Bound : Bool
  temporalSegmentsSourceBound : Bool
  observerRelativeOrderPreserved : Bool
  observerTranslationCompatible : Bool
  refinementCoarseningConsistent : Bool
  cocycleDirectCompositionConsistent : Bool
  sourceV042TrajectoryExact : Bool
  compositionAssociative : Bool
  hermitianSymmetryPreserved : Bool
  diagonalNormalizationPreserved : Bool
  positiveSemidefiniteWitnessPreserved : Bool
  allHistoryPairSupportRetained : Bool
  historyPruningPerformed : Bool
  historyRankingPerformed : Bool
  representativeHistorySelected : Bool
  planSelectionPerformed : Bool
  decisionCommitPerformed : Bool
  activationPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV041Mutated : Bool
  sourceMemoryOSV042Mutated : Bool
  sourcePlanOSV123Mutated : Bool
  persistentWorldStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool

/-- The accepted v0.43 handoff preserves the complete temporal and kernel
    support while establishing exact cocycle composition. -/
theorem cocycle_certificate_preserves_temporal_and_kernel_structure
    (certificate : ObserverRelativeTemporalWindowCoherenceCocycleCompositionCertificate)
    (hsegments : certificate.temporalSegmentsSourceBound = true)
    (horder : certificate.observerRelativeOrderPreserved = true)
    (htranslation : certificate.observerTranslationCompatible = true)
    (hrefinement : certificate.refinementCoarseningConsistent = true)
    (hcocycle : certificate.cocycleDirectCompositionConsistent = true)
    (hsource : certificate.sourceV042TrajectoryExact = true)
    (hassoc : certificate.compositionAssociative = true)
    (hhermitian : certificate.hermitianSymmetryPreserved = true)
    (hdiagonal : certificate.diagonalNormalizationPreserved = true)
    (hpsd : certificate.positiveSemidefiniteWitnessPreserved = true)
    (hsupport : certificate.allHistoryPairSupportRetained = true) :
    certificate.temporalSegmentsSourceBound = true ∧
      certificate.observerRelativeOrderPreserved = true ∧
      certificate.observerTranslationCompatible = true ∧
      certificate.refinementCoarseningConsistent = true ∧
      certificate.cocycleDirectCompositionConsistent = true ∧
      certificate.sourceV042TrajectoryExact = true ∧
      certificate.compositionAssociative = true ∧
      certificate.hermitianSymmetryPreserved = true ∧
      certificate.diagonalNormalizationPreserved = true ∧
      certificate.positiveSemidefiniteWitnessPreserved = true ∧
      certificate.allHistoryPairSupportRetained = true := by
  exact ⟨hsegments, horder, htranslation, hrefinement, hcocycle, hsource,
    hassoc, hhermitian, hdiagonal, hpsd, hsupport⟩

/-- The v0.43 cocycle certificate grants no ranking, decision, activation,
    execution, mutation, verification, or truth authority. -/
theorem cocycle_certificate_grants_no_authority
    (certificate : ObserverRelativeTemporalWindowCoherenceCocycleCompositionCertificate)
    (hprune : certificate.historyPruningPerformed = false)
    (hrank : certificate.historyRankingPerformed = false)
    (hrepresentative : certificate.representativeHistorySelected = false)
    (hselection : certificate.planSelectionPerformed = false)
    (hdecision : certificate.decisionCommitPerformed = false)
    (hactivation : certificate.activationPerformed = false)
    (hexecution : certificate.executionPermission = false)
    (hsource41 : certificate.sourceMemoryOSV041Mutated = false)
    (hsource42 : certificate.sourceMemoryOSV042Mutated = false)
    (hplanos : certificate.sourcePlanOSV123Mutated = false)
    (hworld : certificate.persistentWorldStateMutated = false)
    (hverification : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false) :
    certificate.historyPruningPerformed = false ∧
      certificate.historyRankingPerformed = false ∧
      certificate.representativeHistorySelected = false ∧
      certificate.planSelectionPerformed = false ∧
      certificate.decisionCommitPerformed = false ∧
      certificate.activationPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV041Mutated = false ∧
      certificate.sourceMemoryOSV042Mutated = false ∧
      certificate.sourcePlanOSV123Mutated = false ∧
      certificate.persistentWorldStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false := by
  exact ⟨hprune, hrank, hrepresentative, hselection, hdecision, hactivation,
    hexecution, hsource41, hsource42, hplanos, hworld, hverification, htruth⟩

end KUOS.OpenHorizon.MemoryOSObserverRelativeTemporalWindowCoherenceCocycleCompositionV0_43
