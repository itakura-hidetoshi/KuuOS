import Mathlib
import KUOS.PlanOS.FinitePWassersteinPersistenceTransportV1_19

namespace KUOS.PlanOS.FiniteWassersteinFrechetBarycenterDispersionV1_20

/-- Exact common-denominator numerator for a weighted finite Fréchet functional. -/
def weightedFrechetNumerator (weights transportPowers : List ℕ) : ℕ :=
  (List.zipWith (fun weight power => weight * power) weights transportPowers).sum

/-- Exact weighted tail count numerator over the retained common denominator. -/
def weightedTailCountNumerator (weights tailCounts : List ℕ) : ℕ :=
  (List.zipWith (fun weight count => weight * count) weights tailCounts).sum

/-- A finite candidate-set minimizer witness; it does not quantify over all diagrams. -/
structure FiniteFrechetMinimizerWitness where
  candidateFunctionals : Finset ℕ
  selectedNumerator : ℕ
  selectedMem : selectedNumerator ∈ candidateFunctionals
  minimal : ∀ value ∈ candidateFunctionals, selectedNumerator ≤ value

/-- Source contributions whose exact sum is the retained dispersion numerator. -/
structure FiniteDispersionWitness where
  sourceContributions : List ℕ
  dispersionNumerator : ℕ
  contributionSum : sourceContributions.sum = dispersionNumerator

/-- A checked weighted consensus tail bound. -/
structure WeightedConsensusTailWitness where
  thresholdTwice : ℕ
  pExponent : ℕ
  weightedCountNumerator : ℕ
  dispersionNumerator : ℕ
  bound : weightedCountNumerator * thresholdTwice ^ pExponent ≤ dispersionNumerator

structure FiniteWassersteinFrechetBarycenterDispersionCertificate where
  sourceCertificateDigestsBound : Bool
  candidateDiagramDigestsRecomputed : Bool
  candidateFunctionalsRecomputed : Bool
  finiteMinimizerWitnessRecomputed : Bool
  minimizerTieSetRecomputed : Bool
  lexicalRepresentativeRecomputed : Bool
  consensusTransportsRecomputed : Bool
  sourceContributionsSumToDispersion : Bool
  maximumSourceDeviationRecomputed : Bool
  weightedMomentProfileRecomputed : Bool
  consensusTailProfileRecomputed : Bool
  weightedConsensusTailBoundsVerified : Bool
  zeroDispersionImpliesZeroSourceContributions : Bool
  finiteDiagramFamilyOnly : Bool
  finiteCandidateBarycenterSetOnly : Bool
  boundedPositiveIntegerPOnly : Bool
  exactRationalWeightsOnly : Bool
  globalWassersteinBarycenterNotClaimed : Bool
  globalBarycenterExistenceNotClaimed : Bool
  globalBarycenterUniquenessNotClaimed : Bool
  finiteCandidateUniquenessOnlyWhenTieSetSingleton : Bool
  frechetMinimizerDoesNotRankPlans : Bool
  consensusDiagramIsNotSelectedPlan : Bool
  lowDispersionGrantsNoActivationAuthorization : Bool
  highDispersionDoesNotAutomaticallyReject : Bool
  diagonalConsensusGrantsNoDeletionAuthority : Bool
  finiteDiagramFamilyIsNotPlanningPopulation : Bool
  sourceV117CertificatesNotMutated : Bool
  sourceV118CertificatesNotMutated : Bool
  sourceV119CertificatesNotMutated : Bool
  persistentWorldStateUnchanged : Bool
  candidateSelectionPerformed : Bool
  candidateRankingPerformed : Bool
  activationPerformed : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

/-- A weighted finite Fréchet numerator is a natural number and hence nonnegative. -/
theorem weightedFrechetNumerator_nonnegative
    (weights transportPowers : List ℕ) :
    0 ≤ weightedFrechetNumerator weights transportPowers := by
  exact Nat.zero_le _

/-- The selected value in a finite minimizer witness is below every retained candidate value. -/
theorem finiteFrechetMinimizerWitness_lower
    (witness : FiniteFrechetMinimizerWitness)
    (value : ℕ)
    (hvalue : value ∈ witness.candidateFunctionals) :
    witness.selectedNumerator ≤ value := by
  exact witness.minimal value hvalue

/-- The source contribution list adds exactly to the retained dispersion numerator. -/
theorem finiteDispersionWitness_sum
    (witness : FiniteDispersionWitness) :
    witness.sourceContributions.sum = witness.dispersionNumerator := by
  exact witness.contributionSum

/-- Zero finite dispersion forces every retained natural-number source contribution to vanish. -/
theorem all_source_contributions_zero_of_dispersion_zero
    (contributions : List ℕ)
    (hzero : contributions.sum = 0) :
    ∀ contribution ∈ contributions, contribution = 0 := by
  induction contributions with
  | nil => simp
  | cons head tail ih =>
      simp only [List.sum_cons] at hzero
      have hhead : head = 0 := by omega
      have htail : tail.sum = 0 := by omega
      simp [hhead, ih htail]

/-- A checked consensus tail witness exposes its exact weighted p-power bound. -/
theorem weightedConsensusTailWitness_valid
    (witness : WeightedConsensusTailWitness) :
    witness.weightedCountNumerator *
        witness.thresholdTwice ^ witness.pExponent ≤
      witness.dispersionNumerator := by
  exact witness.bound

/-- Reference candidate-center functional: 1·12 + 2·4 + 1·12 = 32. -/
theorem reference_center_frechet_numerator :
    weightedFrechetNumerator [1, 2, 1] [12, 4, 12] = 32 := by
  native_decide

/-- The retained left and right candidates each have numerator 72. -/
theorem reference_side_candidate_functionals :
    weightedFrechetNumerator [1, 2, 1] [0, 16, 40] = 72 ∧
      weightedFrechetNumerator [1, 2, 1] [40, 16, 0] = 72 := by
  native_decide

/-- The reference finite candidate set has the explicit minimum witness 32. -/
theorem reference_finite_candidate_minimum :
    ∃ minimum ∈ ({32, 72} : Finset ℕ),
      ∀ value ∈ ({32, 72} : Finset ℕ), minimum ≤ value := by
  refine ⟨32, by decide, ?_⟩
  intro value hvalue
  simp only [Finset.mem_insert, Finset.mem_singleton] at hvalue
  rcases hvalue with rfl | rfl <;> omega

/-- The exact weighted source contributions sum to the reference dispersion numerator. -/
theorem reference_source_contribution_sum :
    ([12, 8, 12] : List ℕ).sum = 32 := by
  native_decide

/-- The reference weighted first moment is 16 and the p=2 moment is dispersion 32. -/
theorem reference_weighted_moment_profile :
    weightedFrechetNumerator [1, 2, 1] [6, 2, 6] = 16 ∧
      weightedFrechetNumerator [1, 2, 1] [12, 4, 12] = 32 := by
  native_decide

/-- The threshold-two weighted consensus tail bound saturates the reference dispersion. -/
theorem reference_consensus_tail_bound :
    weightedTailCountNumerator [1, 2, 1] [3, 1, 3] * (2 : ℕ) ^ 2 ≤ 32 := by
  native_decide

/-- Barycenter, consensus, and dispersion evidence grants no planning authority. -/
theorem barycenter_consensus_dispersion_grants_no_authority
    (certificate : FiniteWassersteinFrechetBarycenterDispersionCertificate)
    (hminimizer : certificate.frechetMinimizerDoesNotRankPlans = true)
    (hconsensus : certificate.consensusDiagramIsNotSelectedPlan = true)
    (hlow : certificate.lowDispersionGrantsNoActivationAuthorization = true)
    (hhigh : certificate.highDispersionDoesNotAutomaticallyReject = true)
    (hselection : certificate.candidateSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.frechetMinimizerDoesNotRankPlans = true ∧
      certificate.consensusDiagramIsNotSelectedPlan = true ∧
      certificate.lowDispersionGrantsNoActivationAuthorization = true ∧
      certificate.highDispersionDoesNotAutomaticallyReject = true ∧
      certificate.candidateSelectionPerformed = false ∧
      certificate.executionPermission = false := by
  exact ⟨hminimizer, hconsensus, hlow, hhigh, hselection, hexecution⟩

/-- The v1.20 layer is finite, bounded, read-only, future-only, and inactive. -/
theorem frechet_certificate_is_bounded_future_only
    (certificate : FiniteWassersteinFrechetBarycenterDispersionCertificate)
    (hfamily : certificate.finiteDiagramFamilyOnly = true)
    (hcandidates : certificate.finiteCandidateBarycenterSetOnly = true)
    (hp : certificate.boundedPositiveIntegerPOnly = true)
    (hweights : certificate.exactRationalWeightsOnly = true)
    (hglobal : certificate.globalWassersteinBarycenterNotClaimed = true)
    (hreadonly : certificate.historyReadOnly = true)
    (hfuture : certificate.futureOnly = true)
    (hactive : certificate.activeNow = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.finiteDiagramFamilyOnly = true ∧
      certificate.finiteCandidateBarycenterSetOnly = true ∧
      certificate.boundedPositiveIntegerPOnly = true ∧
      certificate.exactRationalWeightsOnly = true ∧
      certificate.globalWassersteinBarycenterNotClaimed = true ∧
      certificate.historyReadOnly = true ∧
      certificate.futureOnly = true ∧
      certificate.activeNow = false ∧
      certificate.executionPermission = false := by
  exact ⟨hfamily, hcandidates, hp, hweights, hglobal, hreadonly, hfuture, hactive, hexecution⟩

end KUOS.PlanOS.FiniteWassersteinFrechetBarycenterDispersionV1_20
