import Mathlib
import KUOS.DependentOriginationQuantumTesterBornV0_15

namespace KUOS.DependentOriginationTesterDualNormalizationV0_16

open scoped BigOperators MatrixOrder CStarAlgebra ComplexOrder Kronecker
open Matrix
open KUOS.DependentOriginationQuantumChoiCombV0_9
open KUOS.DependentOriginationOpenCombOperationalRealizationV0_14
open KUOS.DependentOriginationQuantumTesterBornV0_15

noncomputable section

/-!
# Causal tester normalization and dual partial-trace recursion v0.16

The v0.15 predicate `TesterNormalized` asks only for total scalar weight one on
complete words of trace-preserving slots.  That is enough for the Born-law
normalization proved there, but it is deliberately weaker than a conditional
causal statement about every residual tester.

This layer introduces that missing conditional statement and identifies it
exactly with the standard dual recursive matrix normalization.

For the newest slot, write a closed tester matrix as

`W[p,(i,a); q,(j,b)]`.

The dual recursive form is

`W = I_output ⊗ X`

in explicit indices, followed by

`Tr_input X = W_previous`.

The operational form says that inserting any trace-preserving newest slot leaves
exactly the same previous residual tester.  The two forms are proved equivalent
entrywise.  Recursing gives the full finite tester theorem.

No converse from the weaker v0.15 `TesterNormalized` predicate is asserted.
-/

/-!
## One-step dual operations
-/

/-- Partial trace over the newest input leg of the dual tester core. -/
def partialTraceNewestInput
    {d n : ℕ}
    (X : Matrix (CombIndex d n × Fin d) (CombIndex d n × Fin d) ℂ) :
    Matrix (CombIndex d n) (CombIndex d n) ℂ :=
  fun p q => ∑ i : Fin d, X (p, i) (q, i)

/--
Insert the identity on the newest output leg.  In the recursive index order
`past × (input × output)`, this is the explicit matrix form of
`I_output ⊗ X`.
-/
def liftNewestOutputIdentity
    {d n : ℕ}
    (X : Matrix (CombIndex d n × Fin d) (CombIndex d n × Fin d) ℂ) :
    Matrix (CombIndex d (Nat.succ n)) (CombIndex d (Nat.succ n)) ℂ :=
  fun r c =>
    if r.2.2 = c.2.2 then
      X (r.1, r.2.1) (c.1, c.2.1)
    else 0

/-- Slice a tester matrix at one fixed newest-output basis index. -/
def newestOutputSlice
    {d n : ℕ}
    (W : Matrix (CombIndex d (Nat.succ n)) (CombIndex d (Nat.succ n)) ℂ)
    (a : Fin d) :
    Matrix (CombIndex d n × Fin d) (CombIndex d n × Fin d) ℂ :=
  fun r c => W (r.1, (r.2, a)) (c.1, (c.2, a))

/--
Contract only the newest Choi slot and retain the complete past tester matrix.
The Choi slot uses the same transposed bilinear pairing convention as v0.14-v0.15.
-/
def contractNewest
    {d n : ℕ}
    (W : Matrix (CombIndex d (Nat.succ n)) (CombIndex d (Nat.succ n)) ℂ)
    (J : ChoiMat d d) :
    Matrix (CombIndex d n) (CombIndex d n) ℂ :=
  fun p q =>
    ∑ i : Fin d, ∑ j : Fin d,
      ∑ a : Fin d, ∑ b : Fin d,
        W (p, (i, a)) (q, (j, b)) * J (j, b) (i, a)

@[simp] theorem partialTraceOutput_add
    {d : ℕ} (A B : ChoiMat d d) :
    partialTraceOutput (A + B) =
      partialTraceOutput A + partialTraceOutput B := by
  ext i j
  simp [partialTraceOutput, Finset.sum_add_distrib]

@[simp] theorem partialTraceOutput_zero (d : ℕ) :
    partialTraceOutput (0 : ChoiMat d d) = 0 := by
  ext i j
  simp [partialTraceOutput]

@[simp] theorem contractNewest_add
    {d n : ℕ}
    (W : Matrix (CombIndex d (Nat.succ n)) (CombIndex d (Nat.succ n)) ℂ)
    (A B : ChoiMat d d) :
    contractNewest W (A + B) =
      contractNewest W A + contractNewest W B := by
  ext p q
  simp [contractNewest, mul_add, Finset.sum_add_distrib]

@[simp] theorem contractNewest_zero
    {d n : ℕ}
    (W : Matrix (CombIndex d (Nat.succ n)) (CombIndex d (Nat.succ n)) ℂ) :
    contractNewest W (0 : ChoiMat d d) = 0 := by
  ext p q
  simp [contractNewest]

/-- The identity-channel Choi matrix is trace preserving. -/
theorem identityChoi_partialTraceOutput (d : ℕ) :
    partialTraceOutput (identityChoi d) = 1 := by
  apply partialTraceOutput_eq_one_of_tracePreserving
  unfold TracePreserving
  apply LinearMap.ext
  intro X
  rfl

/-- Entrywise form of a trace-preserving Choi normalization. -/
theorem partialTraceOutput_entry_of_eq_one
    {d : ℕ}
    {J : ChoiMat d d}
    (hJ : partialTraceOutput J = 1)
    (j i : Fin d) :
    (∑ a : Fin d, J (j, a) (i, a)) =
      if j = i then 1 else 0 := by
  have h := congrArg (fun M : QMat d => M j i) hJ
  simpa [partialTraceOutput, Matrix.one_apply] using h

/--
A dual core contracts against every trace-preserving newest slot to its input
partial trace, independently of the detailed deterministic channel.
-/
theorem contractNewest_liftNewestOutputIdentity
    {d n : ℕ}
    (X : Matrix (CombIndex d n × Fin d) (CombIndex d n × Fin d) ℂ)
    (J : ChoiMat d d)
    (hJ : partialTraceOutput J = 1) :
    contractNewest (liftNewestOutputIdentity X) J =
      partialTraceNewestInput X := by
  classical
  ext p q
  simp [contractNewest, liftNewestOutputIdentity]
  simp_rw [← Finset.mul_sum]
  simp_rw [partialTraceOutput_entry_of_eq_one hJ]
  simp [partialTraceNewestInput]

/-!
## Matrix-unit probes for the converse
-/

/-- An output-off-diagonal Choi matrix unit has zero output partial trace. -/
theorem partialTraceOutput_single_output_ne
    {d : ℕ}
    (i j a b : Fin d)
    (hab : a ≠ b) :
    partialTraceOutput
      (Matrix.single (j, b) (i, a) (1 : ℂ) : ChoiMat d d) = 0 := by
  classical
  ext x y
  simp [partialTraceOutput, Matrix.single, hab, Ne.symm hab]

/-- The difference of two output-diagonal matrix units has zero output partial trace. -/
theorem partialTraceOutput_single_diag_sub
    {d : ℕ}
    (i j a b : Fin d) :
    partialTraceOutput
      ((Matrix.single (j, a) (i, a) (1 : ℂ) : ChoiMat d d) -
        Matrix.single (j, b) (i, b) (1 : ℂ)) = 0 := by
  classical
  ext x y
  simp [partialTraceOutput]

/--
If every trace-preserving newest Choi slot gives one fixed residual tester, then
all zero-partial-trace perturbations contract to zero.
-/
theorem contractNewest_eq_zero_of_partialTraceOutput_eq_zero
    {d n : ℕ}
    {W : Matrix (CombIndex d (Nat.succ n)) (CombIndex d (Nat.succ n)) ℂ}
    {previous : Matrix (CombIndex d n) (CombIndex d n) ℂ}
    (hResidual : ∀ J : ChoiMat d d,
      partialTraceOutput J = 1 → contractNewest W J = previous)
    (K : ChoiMat d d)
    (hK : partialTraceOutput K = 0) :
    contractNewest W K = 0 := by
  have hbase := hResidual (identityChoi d) (identityChoi_partialTraceOutput d)
  have hsum : partialTraceOutput (identityChoi d + K) = 1 := by
    rw [partialTraceOutput_add, identityChoi_partialTraceOutput, hK, add_zero]
  have hpert := hResidual (identityChoi d + K) hsum
  rw [contractNewest_add, hbase] at hpert
  simpa using hpert

/-- Conditional residual invariance forces every newest-output off-diagonal entry to vanish. -/
theorem newestOutput_offdiag_eq_zero_of_residual
    {d n : ℕ}
    {W : Matrix (CombIndex d (Nat.succ n)) (CombIndex d (Nat.succ n)) ℂ}
    {previous : Matrix (CombIndex d n) (CombIndex d n) ℂ}
    (hResidual : ∀ J : ChoiMat d d,
      partialTraceOutput J = 1 → contractNewest W J = previous)
    (p q : CombIndex d n)
    (i j a b : Fin d)
    (hab : a ≠ b) :
    W (p, (i, a)) (q, (j, b)) = 0 := by
  let K : ChoiMat d d := Matrix.single (j, b) (i, a) (1 : ℂ)
  have hK : partialTraceOutput K = 0 := by
    simpa [K] using partialTraceOutput_single_output_ne i j a b hab
  have hzero :=
    contractNewest_eq_zero_of_partialTraceOutput_eq_zero hResidual K hK
  have hpq := congrArg (fun M => M p q) hzero
  simpa [contractNewest, K] using hpq

/-- Conditional residual invariance makes the newest-output diagonal independent of its basis index. -/
theorem newestOutput_diag_eq_of_residual
    {d n : ℕ}
    {W : Matrix (CombIndex d (Nat.succ n)) (CombIndex d (Nat.succ n)) ℂ}
    {previous : Matrix (CombIndex d n) (CombIndex d n) ℂ}
    (hResidual : ∀ J : ChoiMat d d,
      partialTraceOutput J = 1 → contractNewest W J = previous)
    (p q : CombIndex d n)
    (i j a b : Fin d) :
    W (p, (i, a)) (q, (j, a)) =
      W (p, (i, b)) (q, (j, b)) := by
  let K : ChoiMat d d :=
    Matrix.single (j, a) (i, a) (1 : ℂ) -
      Matrix.single (j, b) (i, b) (1 : ℂ)
  have hK : partialTraceOutput K = 0 := by
    simpa [K] using partialTraceOutput_single_diag_sub i j a b
  have hzero :=
    contractNewest_eq_zero_of_partialTraceOutput_eq_zero hResidual K hK
  have hpq := congrArg (fun M => M p q) hzero
  have hdiff :
      W (p, (i, a)) (q, (j, a)) -
        W (p, (i, b)) (q, (j, b)) = 0 := by
    simpa [contractNewest, K] using hpq
  exact sub_eq_zero.mp hdiff

/--
One-step converse: a residual independent of the deterministic newest channel
is exactly an output-identity lift of one core whose newest-input partial trace
is that residual.
-/
theorem deterministicResidual_iff_exists_dualCore
    {d n : ℕ}
    (W : Matrix (CombIndex d (Nat.succ n)) (CombIndex d (Nat.succ n)) ℂ)
    (previous : Matrix (CombIndex d n) (CombIndex d n) ℂ) :
    (∀ J : ChoiMat d d,
      partialTraceOutput J = 1 → contractNewest W J = previous) ↔
    ∃ X : Matrix (CombIndex d n × Fin d) (CombIndex d n × Fin d) ℂ,
      W = liftNewestOutputIdentity X ∧
        partialTraceNewestInput X = previous := by
  classical
  constructor
  · intro hResidual
    by_cases hd : d = 0
    · subst d
      let X : Matrix (CombIndex 0 n × Fin 0) (CombIndex 0 n × Fin 0) ℂ := 0
      refine ⟨X, ?_, ?_⟩
      · ext r c
        exact Fin.elim0 r.2.1
      · have hbase :=
          hResidual (identityChoi 0) (identityChoi_partialTraceOutput 0)
        have hprev : previous = 0 := by
          rw [← hbase]
          ext p q
          simp [contractNewest]
        simp [partialTraceNewestInput, X, hprev]
    · have hdpos : 0 < d := Nat.pos_of_ne_zero hd
      let a0 : Fin d := ⟨0, hdpos⟩
      let X := newestOutputSlice W a0
      refine ⟨X, ?_, ?_⟩
      · ext r c
        by_cases hout : r.2.2 = c.2.2
        · have hdiag := newestOutput_diag_eq_of_residual hResidual
            r.1 c.1 r.2.1 c.2.1 r.2.2 a0
          simp [liftNewestOutputIdentity, hout, X, newestOutputSlice]
          exact hdiag
        · have hoff := newestOutput_offdiag_eq_zero_of_residual hResidual
            r.1 c.1 r.2.1 c.2.1 r.2.2 c.2.2 hout
          simp [liftNewestOutputIdentity, hout, hoff]
      · have hbase :=
          hResidual (identityChoi d) (identityChoi_partialTraceOutput d)
        have hlift := contractNewest_liftNewestOutputIdentity
          X (identityChoi d) (identityChoi_partialTraceOutput d)
        have hW : W = liftNewestOutputIdentity X := by
          ext r c
          by_cases hout : r.2.2 = c.2.2
          · have hdiag := newestOutput_diag_eq_of_residual hResidual
              r.1 c.1 r.2.1 c.2.1 r.2.2 a0
            simp [liftNewestOutputIdentity, hout, X, newestOutputSlice]
            exact hdiag
          · have hoff := newestOutput_offdiag_eq_zero_of_residual hResidual
              r.1 c.1 r.2.1 c.2.1 r.2.2 c.2.2 hout
            simp [liftNewestOutputIdentity, hout, hoff]
        rw [hW] at hbase
        exact hlift.symm.trans hbase
  · rintro ⟨X, rfl, hX⟩ J hJ
    rw [contractNewest_liftNewestOutputIdentity X J hJ, hX]

/-!
## Recursive causal and dual normalization
-/

/--
Operational causal tester normalization: every deterministic newest channel
leaves exactly one previous residual tester, recursively down to the scalar
unit.
-/
def CausalTesterNormalized (d : ℕ) :
    (n : ℕ) →
      Matrix (CombIndex d n) (CombIndex d n) ℂ → Prop
  | 0, W => W = 1
  | Nat.succ n, W =>
      ∃ previous : Matrix (CombIndex d n) (CombIndex d n) ℂ,
        CausalTesterNormalized d n previous ∧
          ∀ J : ChoiMat d d,
            partialTraceOutput J = 1 →
              contractNewest W J = previous

/--
Dual recursive matrix normalization for a closed tester:

`W_{n+1} = I_output ⊗ X_{n+1}` and
`Tr_input X_{n+1} = W_n`, recursively with `W_0 = 1`.
-/
def DualTesterNormalized (d : ℕ) :
    (n : ℕ) →
      Matrix (CombIndex d n) (CombIndex d n) ℂ → Prop
  | 0, W => W = 1
  | Nat.succ n, W =>
      ∃ X : Matrix (CombIndex d n × Fin d) (CombIndex d n × Fin d) ℂ,
        ∃ previous : Matrix (CombIndex d n) (CombIndex d n) ℂ,
          W = liftNewestOutputIdentity X ∧
            partialTraceNewestInput X = previous ∧
              DualTesterNormalized d n previous

/-- Exact finite-dimensional equivalence of conditional operational causality and dual recursion. -/
theorem causalTesterNormalized_iff_dualTesterNormalized
    (d : ℕ) :
    ∀ (n : ℕ)
      (W : Matrix (CombIndex d n) (CombIndex d n) ℂ),
      CausalTesterNormalized d n W ↔ DualTesterNormalized d n W := by
  intro n
  induction n with
  | zero =>
      intro W
      rfl
  | succ n ih =>
      intro W
      constructor
      · rintro ⟨previous, hPrevious, hResidual⟩
        rcases (deterministicResidual_iff_exists_dualCore W previous).mp hResidual with
          ⟨X, hW, hTrace⟩
        exact ⟨X, previous, hW, hTrace, (ih previous).mp hPrevious⟩
      · rintro ⟨X, previous, hW, hTrace, hPrevious⟩
        refine ⟨previous, (ih previous).mpr hPrevious, ?_⟩
        exact (deterministicResidual_iff_exists_dualCore W previous).mpr
          ⟨X, hW, hTrace⟩

/-!
## Causal normalization implies the v0.15 total-word normalization
-/

/-- A structured newest-slot contraction reduces the complete tester pairing by one slot. -/
theorem testerPairing_lift_cons_of_tracePreserving
    {d n : ℕ}
    (X : Matrix (CombIndex d n × Fin d) (CombIndex d n × Fin d) ℂ)
    (newest : ChoiMat d d)
    (past : ChoiSlotWord d n)
    (hNewest : partialTraceOutput newest = 1) :
    testerPairing (liftNewestOutputIdentity X) (.cons newest past) =
      testerPairing (partialTraceNewestInput X) past := by
  classical
  simp [testerPairing, liftNewestOutputIdentity,
    partialTraceNewestInput, Matrix.trace, Matrix.mul_apply,
    ChoiSlotWord.slotTensor, Finset.mul_sum, Finset.sum_mul]
  simp_rw [← Finset.mul_sum]
  simp_rw [partialTraceOutput_entry_of_eq_one hNewest]
  simp [Finset.sum_comm]
  ring

/-- Dual recursive normalization implies the weaker v0.15 operational normalization. -/
theorem dualTesterNormalized_implies_testerNormalized
    (d : ℕ) :
    ∀ (n : ℕ)
      (W : Matrix (CombIndex d n) (CombIndex d n) ℂ),
      DualTesterNormalized d n W → TesterNormalized W := by
  intro n
  induction n with
  | zero =>
      intro W hDual slots hTP
      cases slots with
      | nil =>
          simpa [DualTesterNormalized, testerPairing] using hDual
  | succ n ih =>
      intro W hDual slots hTP
      rcases hDual with ⟨X, previous, hW, hTrace, hPrevious⟩
      cases slots with
      | cons newest past =>
          rw [hW, testerPairing_lift_cons_of_tracePreserving X newest past hTP.1,
            hTrace]
          exact ih previous hPrevious past hTP.2

/-- Conditional causal normalization implies the v0.15 total-word normalization. -/
theorem causalTesterNormalized_implies_testerNormalized
    (d n : ℕ)
    (W : Matrix (CombIndex d n) (CombIndex d n) ℂ)
    (h : CausalTesterNormalized d n W) :
    TesterNormalized W := by
  apply dualTesterNormalized_implies_testerNormalized d n W
  exact (causalTesterNormalized_iff_dualTesterNormalized d n W).mp h

/-!
## Bundled causal and dual testers
-/

/-- Positive tester carrying the conditional causal normalization. -/
structure CausalQuantumProcessTesterChoi (d n : ℕ) where
  choi : Matrix (CombIndex d n) (CombIndex d n) ℂ
  positive : choi.PosSemidef
  causalNormalized : CausalTesterNormalized d n choi

/-- Positive tester carrying the dual recursive matrix normalization. -/
structure DualQuantumProcessTesterChoi (d n : ℕ) where
  choi : Matrix (CombIndex d n) (CombIndex d n) ℂ
  positive : choi.PosSemidef
  dualNormalized : DualTesterNormalized d n choi

namespace CausalQuantumProcessTesterChoi

/-- Forget conditional causality to the v0.15 normalized Born tester. -/
def toOperationalTester
    {d n : ℕ}
    (T : CausalQuantumProcessTesterChoi d n) :
    QuantumProcessTesterChoi d n where
  choi := T.choi
  positive := T.positive
  normalized := causalTesterNormalized_implies_testerNormalized d n T.choi
    T.causalNormalized

/-- Convert a causal tester to the exactly equivalent dual recursive certificate. -/
def toDualTester
    {d n : ℕ}
    (T : CausalQuantumProcessTesterChoi d n) :
    DualQuantumProcessTesterChoi d n where
  choi := T.choi
  positive := T.positive
  dualNormalized :=
    (causalTesterNormalized_iff_dualTesterNormalized d n T.choi).mp
      T.causalNormalized

@[simp] theorem toOperationalTester_choi
    {d n : ℕ}
    (T : CausalQuantumProcessTesterChoi d n) :
    T.toOperationalTester.choi = T.choi := rfl

@[simp] theorem toDualTester_choi
    {d n : ℕ}
    (T : CausalQuantumProcessTesterChoi d n) :
    T.toDualTester.choi = T.choi := rfl

end CausalQuantumProcessTesterChoi

namespace DualQuantumProcessTesterChoi

/-- Convert a dual recursive tester to the exactly equivalent causal certificate. -/
def toCausalTester
    {d n : ℕ}
    (T : DualQuantumProcessTesterChoi d n) :
    CausalQuantumProcessTesterChoi d n where
  choi := T.choi
  positive := T.positive
  causalNormalized :=
    (causalTesterNormalized_iff_dualTesterNormalized d n T.choi).mpr
      T.dualNormalized

/-- Every dual recursive tester yields the v0.15 Born tester. -/
def toOperationalTester
    {d n : ℕ}
    (T : DualQuantumProcessTesterChoi d n) :
    QuantumProcessTesterChoi d n :=
  T.toCausalTester.toOperationalTester

@[simp] theorem toCausalTester_choi
    {d n : ℕ}
    (T : DualQuantumProcessTesterChoi d n) :
    T.toCausalTester.choi = T.choi := rfl

@[simp] theorem toOperationalTester_choi
    {d n : ℕ}
    (T : DualQuantumProcessTesterChoi d n) :
    T.toOperationalTester.choi = T.choi := rfl

end DualQuantumProcessTesterChoi

end

end KUOS.DependentOriginationTesterDualNormalizationV0_16
