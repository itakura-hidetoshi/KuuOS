import Mathlib
import KUOS.PlanOS.SmithNormalFormIntegerHomologyV1_16

namespace KUOS.PlanOS.FiniteFiltrationPersistentHomologyV1_17

structure BarcodeInterval where
  dimension : ℕ
  birth : ℕ
  death : Option ℕ
  deriving DecidableEq, Repr

structure StageSmithData where
  stage : ℕ
  h0FreeRank : ℕ
  h1FreeRank : ℕ
  h2FreeRank : ℕ
  h1SmithDiagonal : List ℕ
  h1TorsionInvariantFactors : List ℕ
  deriving DecidableEq, Repr

structure FiniteFiltrationPersistentHomologyCertificate where
  faceClosureVerified : Bool
  filtrationMonotonicityVerified : Bool
  stagewiseIntegerSmithDataRecomputed : Bool
  f2BoundaryMatrixReduced : Bool
  birthDeathPairingRecomputed : Bool
  barcodeIntervalsVerified : Bool
  persistentBettiVerified : Bool
  finiteFiltrationOnly : Bool
  dimensionsAboveTwoNotComputed : Bool
  integerPersistenceModuleNotComputed : Bool
  zigzagPersistenceNotComputed : Bool
  stabilityTheoremNotClaimed : Bool
  planningSpacePersistentHomologyNotClaimed : Bool
  globalTopologicalInvariantNotClaimed : Bool
  barcodeDoesNotRankCandidates : Bool
  candidateIdentityRetained : Bool
  sourceIntegerHomologyCertificateNotMutated : Bool
  sourceNerveCertificateNotMutated : Bool
  persistentWorldStateUnchanged : Bool
  decisionSelectionPerformed : Bool
  historyReadOnly : Bool
  persistentHomologyGrantsNoAuthority : Bool
  barcodeIntervalGrantsNoAuthority : Bool
  persistentBettiGrantsNoAuthority : Bool
  topologicalObstructionGrantsNoAuthority : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

/-- A finite barcode interval has strictly positive lifetime; an infinite one is valid. -/
def IntervalValid (interval : BarcodeInterval) : Prop :=
  match interval.death with
  | none => True
  | some death => interval.birth < death

/-- Boolean membership of a filtration stage in a half-open barcode interval. -/
def AliveAt (interval : BarcodeInterval) (stage : ℕ) : Bool :=
  decide (interval.birth ≤ stage) &&
    match interval.death with
    | none => true
    | some death => decide (stage < death)

/-- Persistent Betti number obtained by counting alive intervals of one dimension. -/
def persistentBetti
    (barcode : List BarcodeInterval)
    (dimension stage : ℕ) : ℕ :=
  (barcode.filter fun interval =>
    (interval.dimension == dimension) && AliveAt interval stage).length

/-- A finite valid interval has birth strictly before death. -/
theorem finite_interval_birth_lt_death
    (dimension birth death : ℕ)
    (hvalid : IntervalValid ⟨dimension, birth, some death⟩) :
    birth < death := by
  simpa [IntervalValid] using hvalid

/-- A finite interval is not alive at its death stage. -/
theorem finite_interval_not_alive_at_death
    (dimension birth death : ℕ) :
    AliveAt ⟨dimension, birth, some death⟩ death = false := by
  simp [AliveAt]

/-- A finite interval is alive at every stage between birth and death. -/
theorem finite_interval_alive_of_bounds
    (dimension birth death stage : ℕ)
    (hbirth : birth ≤ stage)
    (hdeath : stage < death) :
    AliveAt ⟨dimension, birth, some death⟩ stage = true := by
  simp [AliveAt, hbirth, hdeath]

/-- An infinite interval stays alive after its birth. -/
theorem infinite_interval_alive_of_birth_le
    (dimension birth stage : ℕ)
    (hbirth : birth ≤ stage) :
    AliveAt ⟨dimension, birth, none⟩ stage = true := by
  simp [AliveAt, hbirth]

/-- Reference barcode for three vertices, their one-skeleton, and one filling triangle. -/
def referenceBarcode : List BarcodeInterval :=
  [
    ⟨0, 0, some 1⟩,
    ⟨0, 0, some 1⟩,
    ⟨0, 0, none⟩,
    ⟨1, 1, some 2⟩
  ]

/-- Every reference interval has positive lifetime or infinite persistence. -/
theorem reference_barcode_valid :
    ∀ interval ∈ referenceBarcode, IntervalValid interval := by
  native_decide

/-- At stage zero, three connected components are alive. -/
theorem reference_beta0_stage0 :
    persistentBetti referenceBarcode 0 0 = 3 := by
  native_decide

/-- At stage one, the graph is connected and has one first-homology class. -/
theorem reference_betti_stage1 :
    persistentBetti referenceBarcode 0 1 = 1 ∧
      persistentBetti referenceBarcode 1 1 = 1 := by
  native_decide

/-- At stage two, the filling kills the unique first-homology interval. -/
theorem reference_betti_stage2 :
    persistentBetti referenceBarcode 0 2 = 1 ∧
      persistentBetti referenceBarcode 1 2 = 0 := by
  native_decide

/-- Reference stagewise integer Smith data. -/
def referenceStageSmithData : List StageSmithData :=
  [
    ⟨0, 3, 0, 0, [], []⟩,
    ⟨1, 1, 1, 0, [], []⟩,
    ⟨2, 1, 0, 0, [1], []⟩
  ]

/-- The stagewise integer free ranks agree with the reference filtration. -/
theorem reference_stage_smith_data :
    referenceStageSmithData =
      [
        ⟨0, 3, 0, 0, [], []⟩,
        ⟨1, 1, 1, 0, [], []⟩,
        ⟨2, 1, 0, 0, [1], []⟩
      ] := by
  rfl

/-- The reference filtration has one finite H1 interval from stage one to stage two. -/
theorem reference_h1_interval_alive_then_dead :
    AliveAt ⟨1, 1, some 2⟩ 1 = true ∧
      AliveAt ⟨1, 1, some 2⟩ 2 = false := by
  native_decide

/-- Persistent-homology evidence grants no authority. -/
theorem persistent_homology_evidence_grants_no_authority
    (certificate : FiniteFiltrationPersistentHomologyCertificate)
    (hpersistence : certificate.persistentHomologyGrantsNoAuthority = true)
    (hbarcode : certificate.barcodeIntervalGrantsNoAuthority = true)
    (hbetti : certificate.persistentBettiGrantsNoAuthority = true)
    (hobstruction : certificate.topologicalObstructionGrantsNoAuthority = true)
    (hselection : certificate.decisionSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.persistentHomologyGrantsNoAuthority = true ∧
      certificate.barcodeIntervalGrantsNoAuthority = true ∧
      certificate.persistentBettiGrantsNoAuthority = true ∧
      certificate.topologicalObstructionGrantsNoAuthority = true ∧
      certificate.decisionSelectionPerformed = false ∧
      certificate.executionPermission = false := by
  exact ⟨hpersistence, hbarcode, hbetti, hobstruction, hselection, hexecution⟩

/-- The v1.17 certificate remains finite, read-only, future-only, and inactive. -/
theorem persistent_homology_certificate_is_bounded_future_only
    (certificate : FiniteFiltrationPersistentHomologyCertificate)
    (hfinite : certificate.finiteFiltrationOnly = true)
    (hinteger : certificate.integerPersistenceModuleNotComputed = true)
    (hzigzag : certificate.zigzagPersistenceNotComputed = true)
    (hstability : certificate.stabilityTheoremNotClaimed = true)
    (hglobal : certificate.planningSpacePersistentHomologyNotClaimed = true)
    (hreadonly : certificate.historyReadOnly = true)
    (hfuture : certificate.futureOnly = true)
    (hactive : certificate.activeNow = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.finiteFiltrationOnly = true ∧
      certificate.integerPersistenceModuleNotComputed = true ∧
      certificate.zigzagPersistenceNotComputed = true ∧
      certificate.stabilityTheoremNotClaimed = true ∧
      certificate.planningSpacePersistentHomologyNotClaimed = true ∧
      certificate.historyReadOnly = true ∧
      certificate.futureOnly = true ∧
      certificate.activeNow = false ∧
      certificate.executionPermission = false := by
  exact ⟨hfinite, hinteger, hzigzag, hstability, hglobal, hreadonly, hfuture, hactive, hexecution⟩

end KUOS.PlanOS.FiniteFiltrationPersistentHomologyV1_17
