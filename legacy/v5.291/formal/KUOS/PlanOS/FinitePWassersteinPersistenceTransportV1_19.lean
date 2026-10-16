import Mathlib
import KUOS.PlanOS.FiniteBottleneckPersistenceStabilityV1_18

namespace KUOS.PlanOS.FinitePWassersteinPersistenceTransportV1_19

/-- Exact doubled-cost p-power sum for a finite transport matching. -/
def transportPowerSum (p : ℕ) (costs : List ℕ) : ℕ :=
  (costs.map fun cost => cost ^ p).sum

/-- Exact doubled-cost moment of a finite matching. -/
def momentPowerSum (order : ℕ) (costs : List ℕ) : ℕ :=
  transportPowerSum order costs

/-- Number of retained matching costs at or above a doubled threshold. -/
def tailCount (threshold : ℕ) (costs : List ℕ) : ℕ :=
  (costs.filter fun cost => decide (threshold ≤ cost)).length

/-- Integer bracket for twice a p-Wasserstein distance. -/
structure RootBracket where
  pExponent : ℕ
  totalPower : ℕ
  floorTwice : ℕ
  ceilTwice : ℕ
  lowerBound : floorTwice ^ pExponent ≤ totalPower
  upperBound : totalPower ≤ ceilTwice ^ pExponent

/-- Checked tail lower bound against the exact transport p-power. -/
structure TailMomentWitness where
  thresholdTwice : ℕ
  pExponent : ℕ
  countAtOrAbove : ℕ
  totalPower : ℕ
  bound : countAtOrAbove * thresholdTwice ^ pExponent ≤ totalPower

/-- Finite-cardinality relations between bottleneck, Wasserstein, and perturbation data. -/
structure FiniteTransportBounds where
  pExponent : ℕ
  bottleneckTwice : ℕ
  matchingCardinality : ℕ
  totalPower : ℕ
  filtrationSupNorm : ℕ
  bottleneckLower : bottleneckTwice ^ pExponent ≤ totalPower
  bottleneckCardinalityUpper :
    totalPower ≤ matchingCardinality * bottleneckTwice ^ pExponent
  bottleneckStability : bottleneckTwice ≤ 2 * filtrationSupNorm
  filtrationCardinalityUpper :
    totalPower ≤ matchingCardinality * (2 * filtrationSupNorm) ^ pExponent

structure FinitePWassersteinPersistenceTransportCertificate where
  intervalEndpointBindingsVerified : Bool
  optimalTransportMatchingRecomputed : Bool
  transportPowerSumRecomputed : Bool
  integerRootBoundsRecomputed : Bool
  bottleneckDistanceRecomputed : Bool
  filtrationSupNormRecomputed : Bool
  costMomentProfileRecomputed : Bool
  tailProfileRecomputed : Bool
  tailMarkovPowerBoundsVerified : Bool
  bottleneckToWassersteinPowerBoundsVerified : Bool
  finitePerturbationTransportBudgetVerified : Bool
  infiniteIntervalsNeverMatchedToDiagonal : Bool
  finiteDiagramPairOnly : Bool
  boundedPExponentOnly : Bool
  dimensionsAboveTwoNotCompared : Bool
  irrationalWassersteinRootsNotDecimalApproximated : Bool
  sourceFiltrationToBarcodeRelationNotRecomputed : Bool
  fullPWassersteinStabilityTheoremNotClaimed : Bool
  unboundedDiagramTransportNotComputed : Bool
  wassersteinTransportDoesNotRankCandidates : Bool
  tailProfileDoesNotRankCandidates : Bool
  momentProfileDoesNotRankCandidates : Bool
  candidateIdentityRetained : Bool
  sourcePersistentHomologyCertificateANotMutated : Bool
  sourcePersistentHomologyCertificateBNotMutated : Bool
  sourceBottleneckStabilityCertificateNotMutated : Bool
  persistentWorldStateUnchanged : Bool
  decisionSelectionPerformed : Bool
  historyReadOnly : Bool
  pWassersteinDistanceGrantsNoAuthority : Bool
  transportMatchingGrantsNoAuthority : Bool
  tailMomentEvidenceGrantsNoAuthority : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

@[simp] theorem momentPowerSum_eq_transportPowerSum
    (order : ℕ)
    (costs : List ℕ) :
    momentPowerSum order costs = transportPowerSum order costs := by
  rfl

/-- A root bracket exposes its exact lower p-power inequality. -/
theorem rootBracket_lower (witness : RootBracket) :
    witness.floorTwice ^ witness.pExponent ≤ witness.totalPower := by
  exact witness.lowerBound

/-- A root bracket exposes its exact upper p-power inequality. -/
theorem rootBracket_upper (witness : RootBracket) :
    witness.totalPower ≤ witness.ceilTwice ^ witness.pExponent := by
  exact witness.upperBound

/-- A checked tail witness gives the finite Markov-style p-power bound. -/
theorem tailMomentWitness_valid (witness : TailMomentWitness) :
    witness.countAtOrAbove * witness.thresholdTwice ^ witness.pExponent ≤
      witness.totalPower := by
  exact witness.bound

/-- The retained bottleneck lower bound is part of every finite transport witness. -/
theorem finiteTransportBounds_bottleneck_lower
    (witness : FiniteTransportBounds) :
    witness.bottleneckTwice ^ witness.pExponent ≤ witness.totalPower := by
  exact witness.bottleneckLower

/-- The retained finite-cardinality bottleneck upper bound is explicit. -/
theorem finiteTransportBounds_bottleneck_upper
    (witness : FiniteTransportBounds) :
    witness.totalPower ≤
      witness.matchingCardinality * witness.bottleneckTwice ^ witness.pExponent := by
  exact witness.bottleneckCardinalityUpper

/-- The retained finite perturbation budget is explicit. -/
theorem finiteTransportBounds_filtration_upper
    (witness : FiniteTransportBounds) :
    witness.totalPower ≤
      witness.matchingCardinality *
        (2 * witness.filtrationSupNorm) ^ witness.pExponent := by
  exact witness.filtrationCardinalityUpper

/-- Reference doubled costs for three point matches and one diagonal match. -/
def referenceCosts : List ℕ := [2, 2, 2, 2]

/-- The reference p=2 transport power is sixteen. -/
theorem reference_transport_power_sum_p2 :
    transportPowerSum 2 referenceCosts = 16 := by
  native_decide

/-- The reference first and second doubled-cost moments are eight and sixteen. -/
theorem reference_moment_profile :
    momentPowerSum 1 referenceCosts = 8 ∧
      momentPowerSum 2 referenceCosts = 16 := by
  native_decide

/-- All four reference costs are at least two, and none is at least three. -/
theorem reference_tail_profile :
    tailCount 2 referenceCosts = 4 ∧
      tailCount 3 referenceCosts = 0 := by
  native_decide

/-- The reference p=2 root is exact: twice W₂ is four. -/
theorem reference_exact_root :
    (4 : ℕ) ^ 2 = transportPowerSum 2 referenceCosts := by
  native_decide

/-- The reference bottleneck and finite-cardinality bounds are saturated. -/
theorem reference_transport_bounds :
    (2 : ℕ) ^ 2 ≤ transportPowerSum 2 referenceCosts ∧
      transportPowerSum 2 referenceCosts ≤ 4 * (2 : ℕ) ^ 2 ∧
      (2 : ℕ) ≤ 2 * 1 ∧
      transportPowerSum 2 referenceCosts ≤ 4 * (2 * 1) ^ 2 := by
  native_decide

/-- The reference threshold-two tail lower bound saturates the p-power sum. -/
theorem reference_tail_power_bound :
    tailCount 2 referenceCosts * (2 : ℕ) ^ 2 ≤
      transportPowerSum 2 referenceCosts := by
  native_decide

/-- p-Wasserstein, matching, and tail/moment evidence grants no authority. -/
theorem transport_evidence_grants_no_authority
    (certificate : FinitePWassersteinPersistenceTransportCertificate)
    (hdistance : certificate.pWassersteinDistanceGrantsNoAuthority = true)
    (hmatching : certificate.transportMatchingGrantsNoAuthority = true)
    (htail : certificate.tailMomentEvidenceGrantsNoAuthority = true)
    (hselection : certificate.decisionSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.pWassersteinDistanceGrantsNoAuthority = true ∧
      certificate.transportMatchingGrantsNoAuthority = true ∧
      certificate.tailMomentEvidenceGrantsNoAuthority = true ∧
      certificate.decisionSelectionPerformed = false ∧
      certificate.executionPermission = false := by
  exact ⟨hdistance, hmatching, htail, hselection, hexecution⟩

/-- The v1.19 certificate remains finite, bounded-p, read-only, future-only, and inactive. -/
theorem transport_certificate_is_bounded_future_only
    (certificate : FinitePWassersteinPersistenceTransportCertificate)
    (hfinite : certificate.finiteDiagramPairOnly = true)
    (hp : certificate.boundedPExponentOnly = true)
    (hirrational : certificate.irrationalWassersteinRootsNotDecimalApproximated = true)
    (hstability : certificate.fullPWassersteinStabilityTheoremNotClaimed = true)
    (hreadonly : certificate.historyReadOnly = true)
    (hfuture : certificate.futureOnly = true)
    (hactive : certificate.activeNow = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.finiteDiagramPairOnly = true ∧
      certificate.boundedPExponentOnly = true ∧
      certificate.irrationalWassersteinRootsNotDecimalApproximated = true ∧
      certificate.fullPWassersteinStabilityTheoremNotClaimed = true ∧
      certificate.historyReadOnly = true ∧
      certificate.futureOnly = true ∧
      certificate.activeNow = false ∧
      certificate.executionPermission = false := by
  exact ⟨hfinite, hp, hirrational, hstability, hreadonly, hfuture, hactive, hexecution⟩

end KUOS.PlanOS.FinitePWassersteinPersistenceTransportV1_19
