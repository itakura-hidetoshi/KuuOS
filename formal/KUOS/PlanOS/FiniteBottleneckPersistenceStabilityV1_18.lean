import Mathlib
import KUOS.PlanOS.FiniteFiltrationPersistentHomologyV1_17

namespace KUOS.PlanOS.FiniteBottleneckPersistenceStabilityV1_18

inductive MatchKind where
  | pointToPoint
  | leftToDiagonal
  | diagonalToRight
  deriving DecidableEq, Repr

structure DiagramPoint where
  dimension : ℕ
  birth : ℕ
  death : Option ℕ
  deriving DecidableEq, Repr

structure MatchingEdge where
  kind : MatchKind
  dimension : ℕ
  costTwice : ℕ
  deriving DecidableEq, Repr

structure FiniteBottleneckPersistenceStabilityCertificate where
  intervalEndpointBindingsVerified : Bool
  pointMatchingRecomputed : Bool
  diagonalMatchingRecomputed : Bool
  infiniteIntervalsNeverMatchedToDiagonal : Bool
  bottleneckDistanceRecomputed : Bool
  filtrationSupNormRecomputed : Bool
  finiteStabilityInequalityVerified : Bool
  finiteDiagramPairOnly : Bool
  dimensionsAboveTwoNotCompared : Bool
  sourceFiltrationToBarcodeRelationNotRecomputed : Bool
  fullPersistenceStabilityTheoremNotClaimed : Bool
  wassersteinDistanceNotComputed : Bool
  interleavingDistanceNotComputed : Bool
  zigzagDistanceNotComputed : Bool
  persistenceDistanceDoesNotRankCandidates : Bool
  candidateIdentityRetained : Bool
  sourcePersistentHomologyCertificateANotMutated : Bool
  sourcePersistentHomologyCertificateBNotMutated : Bool
  persistentWorldStateUnchanged : Bool
  decisionSelectionPerformed : Bool
  historyReadOnly : Bool
  bottleneckDistanceGrantsNoAuthority : Bool
  stabilityWitnessGrantsNoAuthority : Bool
  diagonalMatchingGrantsNoAuthority : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

/-- Infinite persistence points cannot be sent to the diagonal. -/
def CanMatchDiagonal (point : DiagramPoint) : Prop :=
  point.death.isSome

/-- Twice the exact L-infinity distance from a finite persistence point to the diagonal. -/
def diagonalCostTwice (point : DiagramPoint) : ℕ :=
  match point.death with
  | none => 0
  | some death => death - point.birth

/-- Twice the point-to-point L-infinity cost, when dimensions and infinity status agree. -/
def pointCostTwice (left right : DiagramPoint) : Option ℕ :=
  if left.dimension = right.dimension then
    match left.death, right.death with
    | none, none => some (2 * Nat.dist left.birth right.birth)
    | some leftDeath, some rightDeath =>
        some (2 * max (Nat.dist left.birth right.birth) (Nat.dist leftDeath rightDeath))
    | _, _ => none
  else
    none

/-- Bottleneck cost is the largest retained doubled edge cost. -/
def matchingBottleneckTwice (matching : List MatchingEdge) : ℕ :=
  matching.foldl (fun current edge => max current edge.costTwice) 0

/-- A finite instance satisfies the retained stability inequality. -/
def FiniteStabilityWitness (distanceTwice filtrationSupNorm : ℕ) : Prop :=
  distanceTwice ≤ 2 * filtrationSupNorm

/-- Point-to-point doubled cost is symmetric. -/
theorem point_cost_twice_comm (left right : DiagramPoint) :
    pointCostTwice left right = pointCostTwice right left := by
  cases left with
  | mk leftDimension leftBirth leftDeath =>
    cases right with
    | mk rightDimension rightBirth rightDeath =>
      cases leftDeath <;> cases rightDeath <;>
        simp [pointCostTwice, eq_comm, Nat.dist_comm, max_comm]

/-- A finite point has doubled diagonal cost equal to its persistence. -/
theorem finite_diagonal_cost_twice (dimension birth death : ℕ) :
    diagonalCostTwice ⟨dimension, birth, some death⟩ = death - birth := by
  rfl

/-- A valid finite persistence interval has positive doubled diagonal cost. -/
theorem finite_diagonal_cost_positive
    (dimension birth death : ℕ)
    (hvalid : birth < death) :
    0 < diagonalCostTwice ⟨dimension, birth, some death⟩ := by
  simpa [diagonalCostTwice] using Nat.sub_pos_of_lt hvalid

/-- Infinite intervals are never eligible for diagonal matching. -/
theorem infinite_interval_cannot_match_diagonal (dimension birth : ℕ) :
    ¬ CanMatchDiagonal ⟨dimension, birth, none⟩ := by
  simp [CanMatchDiagonal]

/-- A checked doubled-distance bound is exactly the finite stability witness. -/
theorem finite_stability_of_distance_bound
    (distanceTwice filtrationSupNorm : ℕ)
    (hbound : distanceTwice ≤ 2 * filtrationSupNorm) :
    FiniteStabilityWitness distanceTwice filtrationSupNorm := by
  exact hbound

/-- Reference matching: three point matches and one diagonal match, all with doubled cost two. -/
def referenceMatching : List MatchingEdge :=
  [
    ⟨MatchKind.pointToPoint, 0, 2⟩,
    ⟨MatchKind.pointToPoint, 0, 2⟩,
    ⟨MatchKind.pointToPoint, 1, 2⟩,
    ⟨MatchKind.diagonalToRight, 1, 2⟩
  ]

/-- The reference matching has exact doubled bottleneck distance two. -/
theorem reference_matching_bottleneck_twice :
    matchingBottleneckTwice referenceMatching = 2 := by
  native_decide

/-- The extra H1 interval [4,6) has diagonal cost one, encoded as doubled cost two. -/
theorem reference_extra_interval_diagonal_cost :
    diagonalCostTwice ⟨1, 4, some 6⟩ = 2 := by
  native_decide

/-- The reference comparison saturates the retained sup-norm stability budget. -/
theorem reference_finite_stability_witness :
    FiniteStabilityWitness 2 1 := by
  native_decide

/-- Bottleneck, diagonal, and stability evidence grants no authority. -/
theorem bottleneck_stability_evidence_grants_no_authority
    (certificate : FiniteBottleneckPersistenceStabilityCertificate)
    (hbottleneck : certificate.bottleneckDistanceGrantsNoAuthority = true)
    (hstability : certificate.stabilityWitnessGrantsNoAuthority = true)
    (hdiagonal : certificate.diagonalMatchingGrantsNoAuthority = true)
    (hselection : certificate.decisionSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.bottleneckDistanceGrantsNoAuthority = true ∧
      certificate.stabilityWitnessGrantsNoAuthority = true ∧
      certificate.diagonalMatchingGrantsNoAuthority = true ∧
      certificate.decisionSelectionPerformed = false ∧
      certificate.executionPermission = false := by
  exact ⟨hbottleneck, hstability, hdiagonal, hselection, hexecution⟩

/-- The v1.18 certificate remains finite, read-only, future-only, and inactive. -/
theorem bottleneck_stability_certificate_is_bounded_future_only
    (certificate : FiniteBottleneckPersistenceStabilityCertificate)
    (hfinite : certificate.finiteDiagramPairOnly = true)
    (hsource : certificate.sourceFiltrationToBarcodeRelationNotRecomputed = true)
    (htheorem : certificate.fullPersistenceStabilityTheoremNotClaimed = true)
    (hwasserstein : certificate.wassersteinDistanceNotComputed = true)
    (hglobal : certificate.dimensionsAboveTwoNotCompared = true)
    (hreadonly : certificate.historyReadOnly = true)
    (hfuture : certificate.futureOnly = true)
    (hactive : certificate.activeNow = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.finiteDiagramPairOnly = true ∧
      certificate.sourceFiltrationToBarcodeRelationNotRecomputed = true ∧
      certificate.fullPersistenceStabilityTheoremNotClaimed = true ∧
      certificate.wassersteinDistanceNotComputed = true ∧
      certificate.dimensionsAboveTwoNotCompared = true ∧
      certificate.historyReadOnly = true ∧
      certificate.futureOnly = true ∧
      certificate.activeNow = false ∧
      certificate.executionPermission = false := by
  exact ⟨hfinite, hsource, htheorem, hwasserstein, hglobal, hreadonly, hfuture, hactive, hexecution⟩

end KUOS.PlanOS.FiniteBottleneckPersistenceStabilityV1_18
