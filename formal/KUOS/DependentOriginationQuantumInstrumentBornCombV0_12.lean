import Mathlib
import KUOS.DependentOriginationCPTPChoiWordV0_11

namespace KUOS.DependentOriginationQuantumInstrumentBornCombV0_12

open scoped BigOperators MatrixOrder CStarAlgebra ComplexOrder
open KUOS.DependentOriginationQuantumChoiCombV0_9
open KUOS.DependentOriginationChoiCompletelyPositiveEquivalenceV0_10
open KUOS.DependentOriginationCPTPChoiWordV0_11

noncomputable section

universe u

/-!
# Quantum instruments, Born normalization, and comb causality v0.12

This layer adds the operational probability structure that was deliberately
kept separate from the arbitrary readout interface in v0.8-v0.11.

There are two independent normalization mechanisms and both are proved from
their actual hypotheses.

* A finite quantum instrument consists of outcome-wise Mathlib completely
  positive maps whose finite sum is trace preserving.  For every density
  matrix, each outcome weight is nonnegative and the finite outcome sum is
  exactly one.  Iterating a finite schedule gives a normalized finite-history
  Born law.
* A deterministic `QuantumCombChoi` already carries recursive Choi causality.
  We derive its scalar trace law directly from the recursive partial-trace
  equation: an `n`-slot uniform-`d` comb has Choi trace `d^n`.

The file also exposes the exact Choi normalization of a quantum instrument and
places it next to the newest-slot causal boundary of a deterministic comb.
No arbitrary complex-linear readout is reinterpreted as a probability.
-/

/-!
## Finite quantum instruments
-/

/--
A finite quantum instrument on `M_d(C)`.

Each outcome is a native Mathlib completely-positive map.  The finite sum of
all outcome maps is required to preserve trace.  Individual outcomes need not
be trace preserving; they are the trace-nonincreasing branches operationally,
while the summed operation is deterministic at the level needed for Born
normalization.
-/
structure QuantumInstrument (d : ℕ) (Outcome : Type u) [Fintype Outcome] where
  operation : Outcome → QMat d →CP QMat d
  totalTracePreserving :
    TracePreserving
      (∑ o : Outcome, (operation o : QMat d →ₗ[ℂ] QMat d))

namespace QuantumInstrument

variable {d : ℕ} {Outcome : Type u} [Fintype Outcome]

/-- The complex-linear total operation obtained by summing all outcomes. -/
def totalMap (I : QuantumInstrument d Outcome) :
    QMat d →ₗ[ℂ] QMat d :=
  ∑ o : Outcome, (I.operation o : QMat d →ₗ[ℂ] QMat d)

/-- The total map is trace preserving by the instrument normalization field. -/
theorem totalMap_tracePreserving (I : QuantumInstrument d Outcome) :
    TracePreserving I.totalMap := by
  simpa [totalMap] using I.totalTracePreserving

/-- Unnormalized post-measurement matrix for one outcome. -/
def outcomeMatrix
    (I : QuantumInstrument d Outcome)
    (o : Outcome)
    (ρ : DensityMatrix d) : QMat d :=
  I.operation o ρ.matrix

/-- Every outcome branch sends a positive input matrix to a positive matrix. -/
theorem outcomeMatrix_posSemidef
    (I : QuantumInstrument d Outcome)
    (o : Outcome)
    (ρ : DensityMatrix d) :
    (I.outcomeMatrix o ρ).PosSemidef := by
  have hIn : 0 ≤ ρ.matrix := ρ.positive.nonneg
  have hOut : 0 ≤ I.operation o ρ.matrix := map_nonneg (I.operation o) hIn
  exact Matrix.nonneg_iff_posSemidef.mp hOut

/-- Complex Born weight of one instrument outcome. -/
def bornWeight
    (I : QuantumInstrument d Outcome)
    (o : Outcome)
    (ρ : DensityMatrix d) : ℂ :=
  matrixTraceLinear d (I.outcomeMatrix o ρ)

/-- Every complex Born weight is nonnegative in the canonical complex order. -/
theorem bornWeight_nonneg
    (I : QuantumInstrument d Outcome)
    (o : Outcome)
    (ρ : DensityMatrix d) :
    0 ≤ I.bornWeight o ρ := by
  have hPos := I.outcomeMatrix_posSemidef o ρ
  change 0 ≤ ∑ i : Fin d, (I.outcomeMatrix o ρ) i i
  exact Finset.sum_nonneg fun i _ => hPos.diag_nonneg

/-- Real-valued Born probability extracted from the necessarily real weight. -/
def bornProbability
    (I : QuantumInstrument d Outcome)
    (o : Outcome)
    (ρ : DensityMatrix d) : ℝ :=
  (I.bornWeight o ρ).re

/-- Outcome probabilities are nonnegative real numbers. -/
theorem bornProbability_nonneg
    (I : QuantumInstrument d Outcome)
    (o : Outcome)
    (ρ : DensityMatrix d) :
    0 ≤ I.bornProbability o ρ := by
  exact (Complex.nonneg_iff.mp (I.bornWeight_nonneg o ρ)).1

/-- The complex Born weights of all outcomes sum exactly to one. -/
theorem bornWeight_sum_eq_one
    (I : QuantumInstrument d Outcome)
    (ρ : DensityMatrix d) :
    (∑ o : Outcome, I.bornWeight o ρ) = 1 := by
  have hTP := LinearMap.congr_fun I.totalTracePreserving ρ.matrix
  calc
    (∑ o : Outcome, I.bornWeight o ρ) =
        matrixTraceLinear d (I.totalMap ρ.matrix) := by
      simp [bornWeight, outcomeMatrix, totalMap]
    _ = matrixTraceLinear d ρ.matrix := by
      simpa [totalMap] using hTP
    _ = 1 := ρ.trace_one

/-- The real Born probabilities of all outcomes sum exactly to one. -/
theorem bornProbability_sum_eq_one
    (I : QuantumInstrument d Outcome)
    (ρ : DensityMatrix d) :
    (∑ o : Outcome, I.bornProbability o ρ) = 1 := by
  have h := congrArg Complex.re (I.bornWeight_sum_eq_one ρ)
  simpa [bornProbability] using h

/-!
### Choi form of an instrument
-/

/-- Choi matrix of one instrument outcome. -/
def outcomeChoi
    (I : QuantumInstrument d Outcome)
    (o : Outcome) : ChoiMat d d :=
  choiMatrix (I.operation o : QMat d →ₗ[ℂ] QMat d)

/-- Every outcome Choi matrix is positive semidefinite. -/
theorem outcomeChoi_posSemidef
    (I : QuantumInstrument d Outcome)
    (o : Outcome) :
    (I.outcomeChoi o).PosSemidef := by
  exact choi_posSemidef_of_completelyPositive (I.operation o)

/-- Total instrument Choi matrix, obtained by summing outcome Choi matrices. -/
def totalChoi (I : QuantumInstrument d Outcome) : ChoiMat d d :=
  ∑ o : Outcome, I.outcomeChoi o

/-- Choi encoding is additive over the finite outcome sum. -/
theorem choiMatrix_totalMap_eq_totalChoi
    (I : QuantumInstrument d Outcome) :
    choiMatrix I.totalMap = I.totalChoi := by
  classical
  ext p q
  simp [totalMap, totalChoi, outcomeChoi, choiMatrix]

/-- The total instrument Choi matrix is positive semidefinite. -/
theorem totalChoi_posSemidef
    (I : QuantumInstrument d Outcome) :
    I.totalChoi.PosSemidef := by
  classical
  unfold totalChoi
  apply Matrix.posSemidef_sum Finset.univ
  intro o _
  exact I.outcomeChoi_posSemidef o

/-- The summed instrument has the exact deterministic channel normalization. -/
theorem totalChoi_normalized
    (I : QuantumInstrument d Outcome) :
    partialTraceOutput I.totalChoi = 1 := by
  rw [← I.choiMatrix_totalMap_eq_totalChoi]
  exact partialTraceOutput_eq_one_of_tracePreserving
    I.totalMap I.totalMap_tracePreserving

/-- The whole instrument therefore determines a normalized positive Choi channel. -/
def totalChoiCertificate
    (I : QuantumInstrument d Outcome) :
    ChoiMatrixChannelCertificate d d where
  choi := I.totalChoi
  positive := I.totalChoi_posSemidef
  normalized := I.totalChoi_normalized

end QuantumInstrument

/-!
## Finite-history Born law

The schedule below is chronological: the head instrument acts first.  The
recursive total is an iterated finite outcome sum, so it is exactly the total
weight of the finite outcome tree without introducing a separate enumeration
of all Cartesian-product histories.
-/

section FiniteHistoryBorn

variable {d : ℕ} {Outcome : Type u} [Fintype Outcome]

/--
State along one explicitly selected outcome history.  Length mismatch is mapped
to zero; the positivity theorem below is stated under exact length agreement.
-/
def branchState :
    List (QuantumInstrument d Outcome) →
      List Outcome → QMat d → QMat d
  | [], [], X => X
  | [], _ :: _, _ => 0
  | _ :: _, [], _ => 0
  | I :: tail, o :: outcomes, X =>
      branchState tail outcomes (I.operation o X)

/-- A matching finite outcome branch preserves positive semidefiniteness. -/
theorem branchState_posSemidef
    (schedule : List (QuantumInstrument d Outcome))
    (outcomes : List Outcome)
    (X : QMat d)
    (hX : X.PosSemidef)
    (hlen : outcomes.length = schedule.length) :
    (branchState schedule outcomes X).PosSemidef := by
  induction schedule generalizing outcomes X with
  | nil =>
      cases outcomes with
      | nil =>
          simpa [branchState] using hX
      | cons o os =>
          simp at hlen
  | cons I tail ih =>
      cases outcomes with
      | nil =>
          simp at hlen
      | cons o os =>
          have hlen' : os.length = tail.length := by
            simpa using hlen
          have hBranch : (I.operation o X).PosSemidef := by
            have hNonneg : 0 ≤ I.operation o X :=
              map_nonneg (I.operation o) hX.nonneg
            exact Matrix.nonneg_iff_posSemidef.mp hNonneg
          simpa [branchState] using
            ih (outcomes := os) (X := I.operation o X) hBranch hlen'

/-- Complex joint Born weight of one selected finite outcome history. -/
def jointBornWeight
    (schedule : List (QuantumInstrument d Outcome))
    (outcomes : List Outcome)
    (ρ : DensityMatrix d) : ℂ :=
  matrixTraceLinear d (branchState schedule outcomes ρ.matrix)

/-- A matching finite-history branch has nonnegative complex Born weight. -/
theorem jointBornWeight_nonneg
    (schedule : List (QuantumInstrument d Outcome))
    (outcomes : List Outcome)
    (ρ : DensityMatrix d)
    (hlen : outcomes.length = schedule.length) :
    0 ≤ jointBornWeight schedule outcomes ρ := by
  have hPos := branchState_posSemidef schedule outcomes ρ.matrix ρ.positive hlen
  change 0 ≤ ∑ i : Fin d, (branchState schedule outcomes ρ.matrix) i i
  exact Finset.sum_nonneg fun i _ => hPos.diag_nonneg

/-- Real joint Born probability of one selected finite outcome history. -/
def jointBornProbability
    (schedule : List (QuantumInstrument d Outcome))
    (outcomes : List Outcome)
    (ρ : DensityMatrix d) : ℝ :=
  (jointBornWeight schedule outcomes ρ).re

/-- Every matching finite-history joint probability is nonnegative. -/
theorem jointBornProbability_nonneg
    (schedule : List (QuantumInstrument d Outcome))
    (outcomes : List Outcome)
    (ρ : DensityMatrix d)
    (hlen : outcomes.length = schedule.length) :
    0 ≤ jointBornProbability schedule outcomes ρ := by
  exact (Complex.nonneg_iff.mp
    (jointBornWeight_nonneg schedule outcomes ρ hlen)).1

/--
Iterated total weight of all branches of a finite instrument schedule.
The head instrument is summed first, then the remaining schedule recursively.
-/
def totalJointWeight :
    List (QuantumInstrument d Outcome) → QMat d → ℂ
  | [], X => matrixTraceLinear d X
  | I :: tail, X =>
      ∑ o : Outcome, totalJointWeight tail (I.operation o X)

/-- Instrument normalization at each slot telescopes the whole outcome tree to input trace. -/
theorem totalJointWeight_eq_trace
    (schedule : List (QuantumInstrument d Outcome))
    (X : QMat d) :
    totalJointWeight schedule X = matrixTraceLinear d X := by
  induction schedule generalizing X with
  | nil =>
      rfl
  | cons I tail ih =>
      rw [totalJointWeight]
      calc
        (∑ o : Outcome, totalJointWeight tail (I.operation o X)) =
            ∑ o : Outcome, matrixTraceLinear d (I.operation o X) := by
          apply Finset.sum_congr rfl
          intro o _
          exact ih (I.operation o X)
        _ = matrixTraceLinear d (I.totalMap X) := by
          simp [QuantumInstrument.totalMap]
        _ = matrixTraceLinear d X := by
          have hTP := LinearMap.congr_fun I.totalTracePreserving X
          simpa [QuantumInstrument.totalMap] using hTP

/-- The complete finite-history Born law has total complex weight one. -/
theorem totalJointWeight_density_eq_one
    (schedule : List (QuantumInstrument d Outcome))
    (ρ : DensityMatrix d) :
    totalJointWeight schedule ρ.matrix = 1 := by
  rw [totalJointWeight_eq_trace]
  exact ρ.trace_one

/-- Real total probability of the full finite outcome tree. -/
def totalJointProbability
    (schedule : List (QuantumInstrument d Outcome))
    (ρ : DensityMatrix d) : ℝ :=
  (totalJointWeight schedule ρ.matrix).re

/-- The complete finite-history Born probability is normalized to one. -/
theorem totalJointProbability_eq_one
    (schedule : List (QuantumInstrument d Outcome))
    (ρ : DensityMatrix d) :
    totalJointProbability schedule ρ = 1 := by
  have h := congrArg Complex.re (totalJointWeight_density_eq_one schedule ρ)
  simpa [totalJointProbability] using h

end FiniteHistoryBorn

/-!
## Deterministic quantum-comb scalar normalization

The v0.9 comb causality condition says

`Tr_newest-output W_(n+1) = I_newest-input ⊗ W_n`.

Taking the ordinary matrix trace on both sides contributes one factor of the
uniform input dimension `d` at each slot.  Hence a normalized `n`-slot comb has
raw Choi trace `d^n`.
-/

section CombScalarNormalization

/-- Ordinary scalar trace of a comb Choi matrix. -/
def combTrace {d n : ℕ}
    (W : Matrix (CombIndex d n) (CombIndex d n) ℂ) : ℂ :=
  ∑ i : CombIndex d n, W i i

/-- Trace of a successor comb is the diagonal sum of its newest-output partial trace. -/
theorem combTrace_succ_eq_partialTrace_diagonal
    {d n : ℕ}
    (W : Matrix (CombIndex d (Nat.succ n))
      (CombIndex d (Nat.succ n)) ℂ) :
    combTrace W =
      ∑ r : CombIndex d n × Fin d,
        partialTraceLastOutput W r r := by
  classical
  simp [combTrace, partialTraceLastOutput, CombIndex,
    Fintype.sum_prod_type]

/-- One recursive comb-causality step multiplies the scalar trace by `d`. -/
theorem combTrace_succ_of_causal
    {d n : ℕ}
    (W : Matrix (CombIndex d (Nat.succ n))
      (CombIndex d (Nat.succ n)) ℂ)
    (previous : Matrix (CombIndex d n) (CombIndex d n) ℂ)
    (hCausal :
      partialTraceLastOutput W = liftInputIdentity previous) :
    combTrace W = (d : ℂ) * combTrace previous := by
  classical
  rw [combTrace_succ_eq_partialTrace_diagonal, hCausal]
  simp [liftInputIdentity, combTrace, Fintype.sum_prod_type,
    Finset.mul_sum]

/-- Recursive deterministic comb normalization fixes the raw Choi trace to `d^n`. -/
theorem combNormalized_trace
    {d n : ℕ}
    {W : Matrix (CombIndex d n) (CombIndex d n) ℂ}
    (hW : CombNormalized d n W) :
    combTrace W = (d : ℂ) ^ n := by
  induction n generalizing W with
  | zero =>
      simp [CombNormalized] at hW
      subst W
      simp [combTrace, CombIndex]
  | succ n ih =>
      rcases hW with ⟨_, previous, hPrevious, hCausal⟩
      calc
        combTrace W = (d : ℂ) * combTrace previous :=
          combTrace_succ_of_causal W previous hCausal
        _ = (d : ℂ) * ((d : ℂ) ^ n) := by
          rw [ih hPrevious]
        _ = (d : ℂ) ^ (Nat.succ n) := by
          simp [pow_succ]

namespace QuantumCombChoi

/-- Every deterministic quantum comb has the exact scalar Choi normalization `d^n`. -/
theorem trace_eq_dimension_pow
    (Q : QuantumCombChoi d n) :
    combTrace Q.choi = (d : ℂ) ^ n :=
  combNormalized_trace Q.normalized

end QuantumCombChoi

end CombScalarNormalization

/-!
## Instrument/comb causal boundary compatibility

This theorem does not replace the full tensor-link contraction.  It records the
exact normalization data that such a contraction consumes: the summed
instrument is TP in Choi form, while the deterministic comb exposes the
previous comb through its newest-output partial trace.
-/

section InstrumentCombBoundary

variable {d n : ℕ} {Outcome : Type u} [Fintype Outcome]

/-- The two exact causal-normalization boundaries are simultaneously available. -/
theorem instrument_comb_causal_boundaries
    (Q : QuantumCombChoi d (Nat.succ n))
    (I : QuantumInstrument d Outcome) :
    ∃ previous : Matrix (CombIndex d n) (CombIndex d n) ℂ,
      CombNormalized d n previous ∧
      partialTraceLastOutput Q.choi = liftInputIdentity previous ∧
      partialTraceOutput I.totalChoi = 1 := by
  rcases Q.exists_previous with ⟨previous, hPrevious, hCausal⟩
  exact ⟨previous, hPrevious, hCausal, I.totalChoi_normalized⟩

end InstrumentCombBoundary

end

end KUOS.DependentOriginationQuantumInstrumentBornCombV0_12
