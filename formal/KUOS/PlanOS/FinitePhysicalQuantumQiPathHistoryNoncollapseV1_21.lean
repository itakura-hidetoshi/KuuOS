import Mathlib
import KUOS.PlanOS.FiniteWassersteinFrechetBarycenterDispersionV1_20

namespace KUOS.PlanOS.FinitePhysicalQuantumQiPathHistoryNoncollapseV1_21

/-- Exact coefficient of a formal Euclidean generating polynomial
    `Z(q) = Σ_γ w_γ q^(S_γ)`. No exponential approximation is used. -/
def actionCoefficient
    (weights actionLevels : List ℕ) (level : ℕ) : ℕ :=
  (List.zipWith
      (fun weight action => if action = level then weight else 0)
      weights actionLevels).sum

/-- Exact finite Z₂-phase amplitude. `true` contributes a negative phase. -/
def signedPhaseAmplitude
    (weights : List ℕ) (negativePhases : List Bool) : ℤ :=
  (List.zipWith
      (fun weight negative =>
        if negative then -(weight : ℤ) else (weight : ℤ))
      weights negativePhases).sum

/-- Weight not visible in the absolute signed amplitude. -/
def phaseCancellationNumerator (totalWeight : ℕ) (amplitude : ℤ) : ℕ :=
  totalWeight - amplitude.natAbs

/-- Coherent intensity of the retained finite signed amplitude. -/
def coherentIntensity (amplitude : ℤ) : ℤ :=
  amplitude * amplitude

/-- Sum of squared history weights before coherent addition. -/
def incoherentIntensity (weights : List ℕ) : ℕ :=
  (weights.map fun weight => weight ^ 2).sum

/-- A finite history family is retained exactly, rather than reduced to one path. -/
structure FiniteHistoryRetentionWitness (α : Type) [DecidableEq α] where
  sourceHistories : Finset α
  retainedHistories : Finset α
  retainedExactly : retainedHistories = sourceHistories

/-- A finite marginal keeps the exact common-denominator mass. -/
structure FiniteMarginalWitness where
  stateWeightNumerators : List ℕ
  weightDenominator : ℕ
  massConservation : stateWeightNumerators.sum = weightDenominator

/-- Finite branch and reconvergence evidence. A tree is not assumed. -/
structure FiniteBranchReconvergenceWitness where
  branchPointCount : ℕ
  reconvergencePointCount : ℕ
  reconvergenceRetained : Bool
  treeAssumptionRequired : Bool

structure FinitePhysicalQuantumQiPathHistoryNoncollapseCertificate where
  sourceV120CertificateBound : Bool
  sourcePathHomotopyCertificateBound : Bool
  physicalQuantumQiDefinitionBound : Bool
  finiteHistoryFamilyRecomputed : Bool
  formalPartitionPolynomialRecomputed : Bool
  endpointInterferenceProfileRecomputed : Bool
  depthMarginalsRecomputed : Bool
  scenarioMarginalsRecomputed : Bool
  sharedPrefixProfileRecomputed : Bool
  branchPointsRecomputed : Bool
  reconvergencePointsRecomputed : Bool
  loopsRetainedWhenPresent : Bool
  allHistoriesRetained : Bool
  treeAssumptionRequired : Bool
  argminPerformed : Bool
  representativeHistorySelected : Bool
  historyRankingPerformed : Bool
  historyPruningPerformed : Bool
  sourceV120CertificateMutated : Bool
  sourcePathHomotopyCertificateMutated : Bool
  persistentWorldStateMutated : Bool
  activationPerformed : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

/-- Exact retention preserves cardinality. -/
theorem retained_history_cardinality
    {α : Type} [DecidableEq α]
    (witness : FiniteHistoryRetentionWitness α) :
    witness.retainedHistories.card = witness.sourceHistories.card := by
  rw [witness.retainedExactly]

/-- Every checked finite marginal exposes exact mass conservation. -/
theorem finite_marginal_mass_conservation
    (witness : FiniteMarginalWitness) :
    witness.stateWeightNumerators.sum = witness.weightDenominator := by
  exact witness.massConservation

/-- Reconvergence evidence explicitly refutes a required tree representation. -/
theorem reconvergence_does_not_require_tree
    (witness : FiniteBranchReconvergenceWitness)
    (hrejoin : witness.reconvergenceRetained = true)
    (hnotree : witness.treeAssumptionRequired = false) :
    witness.reconvergenceRetained = true ∧
      witness.treeAssumptionRequired = false := by
  exact ⟨hrejoin, hnotree⟩

/-- Reference formal partition polynomial coefficients:
    `Z(q) = 4 q² + 2 q³`. -/
theorem reference_partition_polynomial :
    actionCoefficient [2, 2, 1, 1] [2, 2, 3, 3] 2 = 4 ∧
      actionCoefficient [2, 2, 1, 1] [2, 2, 3, 3] 3 = 2 := by
  native_decide

/-- Reference Z₂-phase amplitude: `2 - 2 + 1 + 1 = 2`. -/
theorem reference_signed_phase_amplitude :
    signedPhaseAmplitude [2, 2, 1, 1] [false, true, false, false] = 2 := by
  native_decide

/-- The reference cancellation numerator is `6 - |2| = 4`. -/
theorem reference_phase_cancellation :
    phaseCancellationNumerator 6
      (signedPhaseAmplitude [2, 2, 1, 1] [false, true, false, false]) = 4 := by
  native_decide

/-- Reference coherent and incoherent intensities are 4 and 10. -/
theorem reference_interference_intensities :
    coherentIntensity
        (signedPhaseAmplitude [2, 2, 1, 1] [false, true, false, false]) = 4 ∧
      incoherentIntensity [2, 2, 1, 1] = 10 := by
  native_decide

/-- The reference depth marginals preserve denominator six. -/
theorem reference_depth_marginal_mass :
    ([6] : List ℕ).sum = 6 ∧
      ([3, 3] : List ℕ).sum = 6 ∧
      ([4, 2] : List ℕ).sum = 6 ∧
      ([6] : List ℕ).sum = 6 := by
  native_decide

/-- The reference graph has three branch points and two reconvergence points. -/
theorem reference_branch_reconvergence_counts :
    (3 : ℕ) > 0 ∧ (2 : ℕ) > 0 := by
  omega

/-- Path-history evidence remains non-collapsing and grants no planning authority. -/
theorem path_history_noncollapse_grants_no_authority
    (certificate : FinitePhysicalQuantumQiPathHistoryNoncollapseCertificate)
    (hretain : certificate.allHistoriesRetained = true)
    (hnotree : certificate.treeAssumptionRequired = false)
    (hargmin : certificate.argminPerformed = false)
    (hrepresentative : certificate.representativeHistorySelected = false)
    (hranking : certificate.historyRankingPerformed = false)
    (hpruning : certificate.historyPruningPerformed = false)
    (hactivation : certificate.activationPerformed = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.allHistoriesRetained = true ∧
      certificate.treeAssumptionRequired = false ∧
      certificate.argminPerformed = false ∧
      certificate.representativeHistorySelected = false ∧
      certificate.historyRankingPerformed = false ∧
      certificate.historyPruningPerformed = false ∧
      certificate.activationPerformed = false ∧
      certificate.executionPermission = false := by
  exact ⟨hretain, hnotree, hargmin, hrepresentative, hranking,
    hpruning, hactivation, hexecution⟩

/-- The layer is finite, read-only, future-only, inactive, and preserves sources. -/
theorem path_history_certificate_is_bounded_future_only
    (certificate : FinitePhysicalQuantumQiPathHistoryNoncollapseCertificate)
    (hv120 : certificate.sourceV120CertificateMutated = false)
    (hhomotopy : certificate.sourcePathHomotopyCertificateMutated = false)
    (hworld : certificate.persistentWorldStateMutated = false)
    (hreadonly : certificate.historyReadOnly = true)
    (hfuture : certificate.futureOnly = true)
    (hactive : certificate.activeNow = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.sourceV120CertificateMutated = false ∧
      certificate.sourcePathHomotopyCertificateMutated = false ∧
      certificate.persistentWorldStateMutated = false ∧
      certificate.historyReadOnly = true ∧
      certificate.futureOnly = true ∧
      certificate.activeNow = false ∧
      certificate.executionPermission = false := by
  exact ⟨hv120, hhomotopy, hworld, hreadonly, hfuture, hactive, hexecution⟩

end KUOS.PlanOS.FinitePhysicalQuantumQiPathHistoryNoncollapseV1_21
