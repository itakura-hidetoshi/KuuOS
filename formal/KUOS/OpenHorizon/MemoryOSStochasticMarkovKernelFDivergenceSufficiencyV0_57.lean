import Mathlib
import KUOS.OpenHorizon.MemoryOSFDivergenceTransportDataProcessingV0_56

namespace KUOS.OpenHorizon.MemoryOSStochasticMarkovKernelFDivergenceSufficiencyV0_57

open KUOS.OpenHorizon.MemoryOSRelativeEntropyTransportLebesgueDecompositionV0_55
open KUOS.OpenHorizon.MemoryOSFDivergenceTransportDataProcessingV0_56

def markovPushforward
    {ι κ : Type*} [Fintype ι]
    (kernel : ι → κ → ℝ) (mass : ι → ℝ) (target : κ) : ℝ :=
  ∑ source, mass source * kernel source target

def finiteFDivergence
    {ι : Type*} [Fintype ι]
    (f : ℝ → ℝ) (pMass qMass : ι → ℝ) : ℝ :=
  ∑ i, qMass i * f (pMass i / qMass i)

theorem finite_data_processing_of_cellwise_jensen_witness
    {κ : Type*} [Fintype κ]
    (f : ℝ → ℝ)
    (pTarget qTarget sourceBudget : κ → ℝ)
    (hcell :
      ∀ target,
        qTarget target * f (pTarget target / qTarget target) ≤
          sourceBudget target) :
    finiteFDivergence f pTarget qTarget ≤
      ∑ target, sourceBudget target := by
  unfold finiteFDivergence
  exact Finset.sum_le_sum fun target _ => hcell target

theorem data_processing_equality_of_explicit_recovery
    (sourceDivergence forwardDivergence recoveredDivergence : ℝ)
    (hforward : forwardDivergence ≤ sourceDivergence)
    (hrecovery : recoveredDivergence ≤ forwardDivergence)
    (hrecovered : recoveredDivergence = sourceDivergence) :
    forwardDivergence = sourceDivergence := by
  linarith

theorem strict_contraction_rules_out_sufficiency
    (sourceDivergence forwardDivergence recoveredDivergence : ℝ)
    (hstrict : forwardDivergence < sourceDivergence)
    (hrecovery : recoveredDivergence ≤ forwardDivergence)
    (hrecovered : recoveredDivergence = sourceDivergence) :
    False := by
  linarith

theorem tagged_split_mass_recovery_exact
    (mass splitWeight : ℝ) :
    mass * splitWeight + mass * (1 - splitWeight) = mass := by
  ring

theorem split_f_divergence_contribution_exact
    (f : ℝ → ℝ)
    (pMass qMass splitWeight : ℝ)
    (hq : qMass ≠ 0)
    (hweight : splitWeight ≠ 0)
    (hcomplement : 1 - splitWeight ≠ 0) :
    fDivergenceDensityContribution f
          (pMass * splitWeight) (qMass * splitWeight) 1 +
        fDivergenceDensityContribution f
          (pMass * (1 - splitWeight))
          (qMass * (1 - splitWeight)) 1 =
      fDivergenceDensityContribution f pMass qMass 1 := by
  unfold fDivergenceDensityContribution
  rw [likelihood_ratio_invariant_under_common_density_scaling
    pMass qMass splitWeight hq hweight]
  rw [likelihood_ratio_invariant_under_common_density_scaling
    pMass qMass (1 - splitWeight) hq hcomplement]
  ring

theorem finite_support_split_f_divergence_exact
    {ι : Type*}
    (support : Finset ι)
    (f : ℝ → ℝ)
    (pMass qMass : ι → ℝ)
    (splitWeight : ℝ)
    (hq : ∀ i ∈ support, qMass i ≠ 0)
    (hweight : splitWeight ≠ 0)
    (hcomplement : 1 - splitWeight ≠ 0) :
    ∑ i ∈ support,
        (fDivergenceDensityContribution f
              (pMass i * splitWeight)
              (qMass i * splitWeight) 1 +
          fDivergenceDensityContribution f
              (pMass i * (1 - splitWeight))
              (qMass i * (1 - splitWeight)) 1) =
      ∑ i ∈ support,
        fDivergenceDensityContribution f (pMass i) (qMass i) 1 := by
  apply Finset.sum_congr rfl
  intro i hi
  exact split_f_divergence_contribution_exact
    f (pMass i) (qMass i) splitWeight
    (hq i hi) hweight hcomplement

theorem one_third_two_thirds_split_exact
    (f : ℝ → ℝ)
    (pMass qMass : ℝ)
    (hq : qMass ≠ 0) :
    fDivergenceDensityContribution f
          (pMass * ((1 : ℝ) / 3))
          (qMass * ((1 : ℝ) / 3)) 1 +
        fDivergenceDensityContribution f
          (pMass * (1 - ((1 : ℝ) / 3)))
          (qMass * (1 - ((1 : ℝ) / 3))) 1 =
      fDivergenceDensityContribution f pMass qMass 1 := by
  exact split_f_divergence_contribution_exact
    f pMass qMass ((1 : ℝ) / 3) hq (by norm_num) (by norm_num)

def neymanRationalContribution (pMass qMass : ℚ) : ℚ :=
  (pMass - qMass) ^ 2 / pMass

def triangularRationalContribution (pMass qMass : ℚ) : ℚ :=
  (pMass - qMass) ^ 2 / (pMass + qMass)

theorem exact_reference_stochastic_markov_masses :
    ((2 : ℚ) / 15) * (3 / 4) +
          ((1 : ℚ) / 3) * (1 / 4) +
          ((8 : ℚ) / 15) * 0 = (11 : ℚ) / 60 ∧
      ((2 : ℚ) / 15) * (1 / 4) +
          ((1 : ℚ) / 3) * (1 / 2) +
          ((8 : ℚ) / 15) * (1 / 4) = (1 : ℚ) / 3 ∧
      ((2 : ℚ) / 15) * 0 +
          ((1 : ℚ) / 3) * (1 / 4) +
          ((8 : ℚ) / 15) * (3 / 4) = (29 : ℚ) / 60 ∧
      ((8 : ℚ) / 15) * (3 / 4) +
          ((1 : ℚ) / 3) * (1 / 4) +
          ((2 : ℚ) / 15) * 0 = (29 : ℚ) / 60 ∧
      ((8 : ℚ) / 15) * (1 / 4) +
          ((1 : ℚ) / 3) * (1 / 2) +
          ((2 : ℚ) / 15) * (1 / 4) = (1 : ℚ) / 3 ∧
      ((8 : ℚ) / 15) * 0 +
          ((1 : ℚ) / 3) * (1 / 4) +
          ((2 : ℚ) / 15) * (3 / 4) = (11 : ℚ) / 60 := by
  norm_num

theorem exact_reference_stochastic_pearson_contraction :
    let deterministicCoarse :=
      pearsonRationalContribution ((2 : ℚ) / 15) ((8 : ℚ) / 15) +
      pearsonRationalContribution ((1 : ℚ) / 3) ((1 : ℚ) / 3) +
      pearsonRationalContribution ((8 : ℚ) / 15) ((2 : ℚ) / 15)
    let stochastic :=
      pearsonRationalContribution ((11 : ℚ) / 60) ((29 : ℚ) / 60) +
      pearsonRationalContribution ((1 : ℚ) / 3) ((1 : ℚ) / 3) +
      pearsonRationalContribution ((29 : ℚ) / 60) ((11 : ℚ) / 60)
    deterministicCoarse = (3 : ℚ) / 2 ∧
      stochastic = (216 : ℚ) / 319 ∧
      stochastic < deterministicCoarse ∧
      deterministicCoarse - stochastic = (525 : ℚ) / 638 := by
  norm_num [pearsonRationalContribution]

theorem exact_reference_stochastic_neyman_contraction :
    let deterministicCoarse :=
      neymanRationalContribution ((2 : ℚ) / 15) ((8 : ℚ) / 15) +
      neymanRationalContribution ((1 : ℚ) / 3) ((1 : ℚ) / 3) +
      neymanRationalContribution ((8 : ℚ) / 15) ((2 : ℚ) / 15)
    let stochastic :=
      neymanRationalContribution ((11 : ℚ) / 60) ((29 : ℚ) / 60) +
      neymanRationalContribution ((1 : ℚ) / 3) ((1 : ℚ) / 3) +
      neymanRationalContribution ((29 : ℚ) / 60) ((11 : ℚ) / 60)
    deterministicCoarse = (3 : ℚ) / 2 ∧
      stochastic = (216 : ℚ) / 319 ∧
      stochastic < deterministicCoarse ∧
      deterministicCoarse - stochastic = (525 : ℚ) / 638 := by
  norm_num [neymanRationalContribution]

theorem exact_reference_stochastic_triangular_contraction :
    let deterministicCoarse :=
      triangularRationalContribution
        ((2 : ℚ) / 15) ((8 : ℚ) / 15) +
      triangularRationalContribution
        ((1 : ℚ) / 3) ((1 : ℚ) / 3) +
      triangularRationalContribution
        ((8 : ℚ) / 15) ((2 : ℚ) / 15)
    let stochastic :=
      triangularRationalContribution
        ((11 : ℚ) / 60) ((29 : ℚ) / 60) +
      triangularRationalContribution
        ((1 : ℚ) / 3) ((1 : ℚ) / 3) +
      triangularRationalContribution
        ((29 : ℚ) / 60) ((11 : ℚ) / 60)
    deterministicCoarse = (12 : ℚ) / 25 ∧
      stochastic = (27 : ℚ) / 100 ∧
      stochastic < deterministicCoarse ∧
      deterministicCoarse - stochastic = (21 : ℚ) / 100 := by
  norm_num [triangularRationalContribution]

theorem exact_reference_fine_to_stochastic_gaps :
    (2593 : ℚ) / 1134 - (216 : ℚ) / 319 =
        (582223 : ℚ) / 361746 ∧
      (8 : ℚ) / 15 - (27 : ℚ) / 100 = (79 : ℚ) / 300 := by
  norm_num

theorem exact_tagged_split_weights :
    (1 : ℚ) / 3 + (2 : ℚ) / 3 = 1 := by
  norm_num

theorem full_rank_transport_and_sufficiency_commute
    (sourceDivergence splitDivergence
      targetDivergence targetSplitDivergence : ℝ)
    (hsplit : splitDivergence = sourceDivergence)
    (htransport : targetDivergence = sourceDivergence)
    (htransportSplit : targetSplitDivergence = splitDivergence) :
    targetSplitDivergence = targetDivergence := by
  linarith

structure StochasticMarkovKernelFDivergenceSufficiencyCertificate where
  sourceMemoryOSV056Bound : Bool
  sourceMemoryOSV055Bound : Bool
  stochasticKernelRowStochastic : Bool
  stochasticDataProcessingExact : Bool
  stochasticReferenceContractionStrict : Bool
  stochasticReferenceKernelSufficient : Bool
  taggedSplitChannelRowStochastic : Bool
  explicitRecoveryKernelExact : Bool
  sufficientFDivergenceEqualityExact : Bool
  transportStochasticChannelCommutes : Bool
  transportSufficiencyChannelCommutes : Bool
  singularAtomicProcessingRetained : Bool
  rankOneDensityRecoveryNotClaimed : Bool
  allDecisionCandidatesRetained : Bool
  allPlanOSHistoriesRetained : Bool
  candidatePruningPerformed : Bool
  candidateSelectionPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV056Mutated : Bool
  sourceMemoryOSV055Mutated : Bool
  persistentWORLDStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

theorem certificate_grants_no_authority
    (certificate :
      StochasticMarkovKernelFDivergenceSufficiencyCertificate)
    (hnotsufficient :
      certificate.stochasticReferenceKernelSufficient = false)
    (hpruning : certificate.candidatePruningPerformed = false)
    (hselection : certificate.candidateSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false)
    (hsource56 : certificate.sourceMemoryOSV056Mutated = false)
    (hsource55 : certificate.sourceMemoryOSV055Mutated = false)
    (hworld : certificate.persistentWORLDStateMutated = false)
    (hverification : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false) :
    certificate.stochasticReferenceKernelSufficient = false ∧
      certificate.candidatePruningPerformed = false ∧
      certificate.candidateSelectionPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV056Mutated = false ∧
      certificate.sourceMemoryOSV055Mutated = false ∧
      certificate.persistentWORLDStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false := by
  exact ⟨hnotsufficient, hpruning, hselection, hexecution,
    hsource56, hsource55, hworld, hverification, htruth⟩

end KUOS.OpenHorizon.MemoryOSStochasticMarkovKernelFDivergenceSufficiencyV0_57
