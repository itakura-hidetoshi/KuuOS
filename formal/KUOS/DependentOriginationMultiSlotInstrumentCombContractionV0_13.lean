import Mathlib
import KUOS.DependentOriginationQuantumInstrumentBornCombV0_12

namespace KUOS.DependentOriginationMultiSlotInstrumentCombContractionV0_13

open scoped BigOperators MatrixOrder CStarAlgebra ComplexOrder
open KUOS.DependentOriginationQuantumChoiCombV0_9
open KUOS.DependentOriginationChoiCompletelyPositiveEquivalenceV0_10
open KUOS.DependentOriginationCPTPChoiWordV0_11
open KUOS.DependentOriginationQuantumInstrumentBornCombV0_12

noncomputable section

universe u

/-!
# Multi-slot instrument Choi / closed-comb contraction v0.13

This file closes the generalized-Born-rule equality that was deliberately left
open in v0.12.

The existing v0.9 `QuantumCombChoi` is an open deterministic comb: its recursive
partial-trace law describes causal normalization but does not by itself provide
a scalar boundary condition.  A scalar Born weight additionally requires an
initial state and final trace closure.

For the v0.12 finite-history operational process, that closure is explicit.  We
therefore define the corresponding closed sequential process-comb Choi boundary
and prove, without an extra response-equality assumption, that arbitrary finite
lists of slot Choi matrices satisfy

  tensor-link scalar = decoded operational response.

Specializing the slot matrices to arbitrary selected outcomes of a finite
quantum-instrument schedule gives the exact theorem

  multi-slot instrument Choi contraction = v0.12 joint Born weight,

and hence equality of the real generalized-Born scalar with the previously
proved joint Born probability.

The chronological-order convention is made explicit.  v0.12 schedules act
head-first, whereas v0.9 `complexInterventionWordOperator` is head-after-tail;
therefore the selected intervention word is built in reverse chronological
order before repeated `choiLink` composition.
-/

/-!
## A scalar Choi contraction and the density/trace comb boundary
-/

/--
Entrywise Choi contraction in the repository's Choi convention.

The transpose convention normally written in a Hilbert--Schmidt generalized
Born rule is absorbed into the coefficient placement of `W`; no conjugation or
implicit transpose is hidden in this definition.
-/
def choiTensorLinkScalar {d : ℕ}
    (W J : ChoiMat d d) : ℂ :=
  ∑ p : ChoiIndex d d, ∑ q : ChoiIndex d d,
    W p q * J p q

/--
Closed density/trace process-comb boundary.

For an input density matrix `ρ`, the coefficient

`W[(i,a),(j,b)] = ρ[i,j] δ[a,b]`

encodes the initial state on the input legs and the final trace on the output
legs.  It is intentionally distinct from the open deterministic-channel
normalization `Tr_output J = I`.
-/
def closedBornCombChoi {d : ℕ}
    (ρ : DensityMatrix d) : ChoiMat d d :=
  fun p q => if p.2 = q.2 then ρ.matrix p.1 q.1 else 0

/--
Contracting the closed density/trace comb boundary with an arbitrary Choi matrix
is exactly the trace of the Choi-decoded operator applied to the initial state.
-/
theorem closedBornCombChoi_tensorLink_eq_trace_fromChoi
    {d : ℕ}
    (ρ : DensityMatrix d)
    (J : ChoiMat d d) :
    choiTensorLinkScalar (closedBornCombChoi ρ) J =
      matrixTraceLinear d (fromChoi J ρ.matrix) := by
  classical
  calc
    choiTensorLinkScalar (closedBornCombChoi ρ) J =
        ∑ i : Fin d, ∑ a : Fin d, ∑ j : Fin d,
          ρ.matrix i j * J (i, a) (j, a) := by
      simp [choiTensorLinkScalar, closedBornCombChoi,
        Fintype.sum_prod_type]
    _ = ∑ a : Fin d, ∑ i : Fin d, ∑ j : Fin d,
          ρ.matrix i j * J (i, a) (j, a) := by
      rw [Fintype.sum_comm]
    _ = matrixTraceLinear d (fromChoi J ρ.matrix) := by
      rfl

/-- The empty intervention history closes to unit Born weight. -/
theorem closedBornCombChoi_identity_normalized
    {d : ℕ}
    (ρ : DensityMatrix d) :
    choiTensorLinkScalar (closedBornCombChoi ρ) (identityChoi d) = 1 := by
  rw [closedBornCombChoi_tensorLink_eq_trace_fromChoi]
  simpa [identityChoi] using ρ.trace_one

/--
Closed sequential process comb carrying the exact density/trace boundary used by
the v0.12 operational finite-history Born law.
-/
structure ClosedSequentialProcessCombChoi (d : ℕ) where
  initial : DensityMatrix d

namespace ClosedSequentialProcessCombChoi

variable {d : ℕ}

/-- Choi boundary matrix of the closed sequential process comb. -/
def boundaryChoi (C : ClosedSequentialProcessCombChoi d) : ChoiMat d d :=
  closedBornCombChoi C.initial

/--
Repeated tensor-link contraction of an arbitrary finite list of slot Choi
matrices against the closed process comb.

`choiWord` performs all internal causal Choi links; the final scalar contraction
closes the remaining input/output boundary with the initial density and trace.
-/
def tensorLinkScalar
    (C : ClosedSequentialProcessCombChoi d)
    (slots : List (ChoiMat d d)) : ℂ :=
  choiTensorLinkScalar C.boundaryChoi (choiWord d slots)

/--
Arbitrary multi-slot Choi theorem.

Every finite list of Choi matrices, with no positivity assumption required for
the algebraic identity, has tensor-link scalar equal to the operational response
of the exactly Choi-decoded intervention word.
-/
theorem tensorLinkScalar_eq_decodedOperationalResponse
    (C : ClosedSequentialProcessCombChoi d)
    (slots : List (ChoiMat d d)) :
    C.tensorLinkScalar slots =
      matrixTraceLinear d
        (complexInterventionWordOperator d (slots.map fromChoi)
          C.initial.matrix) := by
  unfold tensorLinkScalar boundaryChoi
  rw [closedBornCombChoi_tensorLink_eq_trace_fromChoi]
  have hChoi :
      choiWord d slots =
        choiMatrix
          (complexInterventionWordOperator d (slots.map fromChoi)) := by
    have h :=
      choiMatrix_complexInterventionWordOperator d (slots.map fromChoi)
    simpa [List.map_map, Function.comp_def] using h.symm
  rw [hChoi, fromChoi_choiMatrix]

/--
The same theorem for arbitrary complex-linear interventions, stated directly in
operator form.  Their Choi matrices may be linked first without changing the
response.
-/
theorem tensorLinkScalar_map_choiMatrix_eq_operationalResponse
    (C : ClosedSequentialProcessCombChoi d)
    (word : List (QMat d →ₗ[ℂ] QMat d)) :
    C.tensorLinkScalar (word.map choiMatrix) =
      matrixTraceLinear d
        (complexInterventionWordOperator d word C.initial.matrix) := by
  rw [C.tensorLinkScalar_eq_decodedOperationalResponse]
  simp [List.map_map, Function.comp_def]

end ClosedSequentialProcessCombChoi

/-!
## Exact chronological bridge to v0.12 instrument histories
-/

section InstrumentHistory

variable {d : ℕ} {Outcome : Type u} [Fintype Outcome]

/--
Selected intervention word in the order expected by v0.9 Choi composition.

The v0.12 schedule is chronological (head acts first).  v0.9 operator words are
head-after-tail, so the selected head operation is appended after the recursively
built tail word.  For chronological operations `[Φ₁, Φ₂, ..., Φₙ]` the result is
`[Φₙ, ..., Φ₂, Φ₁]`.
-/
def selectedReverseInterventionWord :
    List (QuantumInstrument d Outcome) →
      List Outcome → List (QMat d →ₗ[ℂ] QMat d)
  | [], [] => []
  | [], _ :: _ => []
  | _ :: _, [] => []
  | I :: tail, o :: outcomes =>
      selectedReverseInterventionWord tail outcomes ++
        [(I.operation o : QMat d →ₗ[ℂ] QMat d)]

/-- v0.9 word evaluation distributes over append with the causal convention. -/
theorem complexInterventionWordOperator_append_apply
    (left right : List (QMat d →ₗ[ℂ] QMat d))
    (X : QMat d) :
    complexInterventionWordOperator d (left ++ right) X =
      complexInterventionWordOperator d left
        (complexInterventionWordOperator d right X) := by
  induction left with
  | nil =>
      rfl
  | cons A tail ih =>
      simp [complexInterventionWordOperator, ih]

/--
The v0.12 branch-state recursion is exactly the v0.9 operator word evaluated on
the reverse-chronological selected intervention word.
-/
theorem branchState_eq_selectedReverseInterventionWord
    (schedule : List (QuantumInstrument d Outcome))
    (outcomes : List Outcome)
    (X : QMat d)
    (hlen : outcomes.length = schedule.length) :
    branchState schedule outcomes X =
      complexInterventionWordOperator d
        (selectedReverseInterventionWord schedule outcomes) X := by
  induction schedule generalizing outcomes X with
  | nil =>
      cases outcomes with
      | nil =>
          rfl
      | cons o os =>
          simp at hlen
  | cons I tail ih =>
      cases outcomes with
      | nil =>
          simp at hlen
      | cons o os =>
          have hlen' : os.length = tail.length := by
            simpa using hlen
          change
            branchState tail os (I.operation o X) =
              complexInterventionWordOperator d
                (selectedReverseInterventionWord tail os ++
                  [(I.operation o : QMat d →ₗ[ℂ] QMat d)]) X
          rw [complexInterventionWordOperator_append_apply]
          change
            branchState tail os (I.operation o X) =
              complexInterventionWordOperator d
                (selectedReverseInterventionWord tail os)
                (I.operation o X)
          exact ih os (I.operation o X) hlen'

/-- Choi matrices of the selected reverse-chronological instrument history. -/
def selectedOutcomeChoiList
    (schedule : List (QuantumInstrument d Outcome))
    (outcomes : List Outcome) : List (ChoiMat d d) :=
  (selectedReverseInterventionWord schedule outcomes).map choiMatrix

/--
Exact multi-slot instrument/comb scalar in Choi language.

All selected outcome Choi matrices are linked causally first, then contracted
against the closed density/trace process comb.
-/
def multiSlotInstrumentChoiTensorLinkScalar
    (schedule : List (QuantumInstrument d Outcome))
    (outcomes : List Outcome)
    (ρ : DensityMatrix d) : ℂ :=
  (ClosedSequentialProcessCombChoi.mk ρ).tensorLinkScalar
    (selectedOutcomeChoiList schedule outcomes)

/--
Main generalized Born theorem: for every matching finite instrument/outcome
history, the scalar obtained by multi-slot Choi tensor-link contraction against
the closed process comb is exactly the v0.12 operational joint Born weight.
-/
theorem multiSlotInstrumentChoi_tensorLink_eq_jointBornWeight
    (schedule : List (QuantumInstrument d Outcome))
    (outcomes : List Outcome)
    (ρ : DensityMatrix d)
    (hlen : outcomes.length = schedule.length) :
    multiSlotInstrumentChoiTensorLinkScalar schedule outcomes ρ =
      jointBornWeight schedule outcomes ρ := by
  unfold multiSlotInstrumentChoiTensorLinkScalar jointBornWeight
  rw [ClosedSequentialProcessCombChoi.tensorLinkScalar_eq_decodedOperationalResponse]
  simp [selectedOutcomeChoiList, List.map_map, Function.comp_def]
  rw [← branchState_eq_selectedReverseInterventionWord
    schedule outcomes ρ.matrix hlen]

/-- Real scalar extracted from the exact multi-slot Choi tensor-link contraction. -/
def multiSlotInstrumentChoiTensorLinkProbability
    (schedule : List (QuantumInstrument d Outcome))
    (outcomes : List Outcome)
    (ρ : DensityMatrix d) : ℝ :=
  (multiSlotInstrumentChoiTensorLinkScalar schedule outcomes ρ).re

/--
The Choi tensor-link probability is exactly the previously proved operational
joint Born probability.
-/
theorem multiSlotInstrumentChoi_tensorLinkProbability_eq_jointBornProbability
    (schedule : List (QuantumInstrument d Outcome))
    (outcomes : List Outcome)
    (ρ : DensityMatrix d)
    (hlen : outcomes.length = schedule.length) :
    multiSlotInstrumentChoiTensorLinkProbability schedule outcomes ρ =
      jointBornProbability schedule outcomes ρ := by
  unfold multiSlotInstrumentChoiTensorLinkProbability jointBornProbability
  rw [multiSlotInstrumentChoi_tensorLink_eq_jointBornWeight
    schedule outcomes ρ hlen]

/-- Nonnegativity transfers to the exact Choi tensor-link scalar probability. -/
theorem multiSlotInstrumentChoi_tensorLinkProbability_nonneg
    (schedule : List (QuantumInstrument d Outcome))
    (outcomes : List Outcome)
    (ρ : DensityMatrix d)
    (hlen : outcomes.length = schedule.length) :
    0 ≤ multiSlotInstrumentChoiTensorLinkProbability schedule outcomes ρ := by
  rw [multiSlotInstrumentChoi_tensorLinkProbability_eq_jointBornProbability
    schedule outcomes ρ hlen]
  exact jointBornProbability_nonneg schedule outcomes ρ hlen

end InstrumentHistory

end

end KUOS.DependentOriginationMultiSlotInstrumentCombContractionV0_13
