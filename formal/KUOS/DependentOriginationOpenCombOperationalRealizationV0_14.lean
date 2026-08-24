import Mathlib
import KUOS.DependentOriginationMultiSlotInstrumentCombContractionV0_13

namespace KUOS.DependentOriginationOpenCombOperationalRealizationV0_14

open scoped BigOperators
open KUOS.DependentOriginationQuantumChoiCombV0_9

noncomputable section

universe u

/-!
# Open quantum-comb operational realization v0.14

The preceding layer proved the generalized Born rule for the closed sequential
process obtained from an initial density boundary and final trace.  This file
keeps the genuinely open `QuantumCombChoi` carrier and gives it a direct
multi-slot operational semantics.

The construction is intentionally history-sensitive.  A fixed-length word of
slot Choi matrices is tensored over the recursive comb history index, and the
result is paired directly with the open comb Choi matrix.  No collapse to a
single composed channel is built into this semantics.

A separate `SequentialFactorization` certificate records the special case in
which all responses do factor through one composed channel acting on one fixed
initial matrix followed by one fixed readout.  If an open comb distinguishes
two histories with the same composed channel, such a factorization is
impossible.  This is the finite-dimensional Choi analogue of the earlier
history-sensitivity obstructions in the dependent-origination spine.
-/

/--
A fixed-length word of Choi matrices.  The head is the newest slot and the tail
contains the earlier history.  This matches the recursive presentation of
`CombIndex`.
-/
inductive ChoiSlotWord (d : ℕ) : ℕ → Type
  | nil : ChoiSlotWord d 0
  | cons {n : ℕ} (newest : ChoiMat d d) (past : ChoiSlotWord d n) :
      ChoiSlotWord d (Nat.succ n)

/-- A fixed-length word of complex-linear interventions with the same newest-first convention. -/
inductive InterventionSlotWord (d : ℕ) : ℕ → Type
  | nil : InterventionSlotWord d 0
  | cons {n : ℕ} (newest : QMat d →ₗ[ℂ] QMat d)
      (past : InterventionSlotWord d n) :
      InterventionSlotWord d (Nat.succ n)

namespace ChoiSlotWord

/--
Tensor the slot Choi matrices over the complete recursive comb history index.
For a successor slot the past tensor and newest Choi matrix are multiplied
entrywise on their respective tensor legs.
-/
def slotTensor {d : ℕ} : {n : ℕ} → ChoiSlotWord d n →
    Matrix (CombIndex d n) (CombIndex d n) ℂ
  | 0, .nil => 1
  | Nat.succ n, .cons newest past =>
      fun r c => slotTensor past r.1 c.1 * newest r.2 c.2

@[simp] theorem slotTensor_nil (d : ℕ) :
    slotTensor (ChoiSlotWord.nil : ChoiSlotWord d 0) = 1 := by
  rfl

@[simp] theorem slotTensor_cons_apply
    {d n : ℕ}
    (newest : ChoiMat d d)
    (past : ChoiSlotWord d n)
    (r c : CombIndex d (Nat.succ n)) :
    slotTensor (.cons newest past) r c =
      slotTensor past r.1 c.1 * newest r.2 c.2 := by
  rfl

/-- The newest Choi slot enters the full history tensor additively. -/
theorem slotTensor_cons_add
    {d n : ℕ}
    (A B : ChoiMat d d)
    (past : ChoiSlotWord d n) :
    slotTensor (.cons (A + B) past) =
      slotTensor (.cons A past) + slotTensor (.cons B past) := by
  ext r c
  simp [slotTensor, mul_add]

/-- The newest Choi slot enters the full history tensor complex-linearly. -/
theorem slotTensor_cons_smul
    {d n : ℕ}
    (a : ℂ)
    (A : ChoiMat d d)
    (past : ChoiSlotWord d n) :
    slotTensor (.cons (a • A) past) =
      a • slotTensor (.cons A past) := by
  ext r c
  simp [slotTensor]
  ring

end ChoiSlotWord

namespace InterventionSlotWord

/-- Encode every intervention slot by its exact Choi matrix. -/
def toChoi {d : ℕ} : {n : ℕ} → InterventionSlotWord d n → ChoiSlotWord d n
  | 0, .nil => .nil
  | Nat.succ n, .cons newest past =>
      .cons (choiMatrix newest) (toChoi past)

/-- Compose a newest-first intervention history into one complex-linear channel map. -/
def operator {d : ℕ} : {n : ℕ} → InterventionSlotWord d n →
    QMat d →ₗ[ℂ] QMat d
  | 0, .nil => LinearMap.id
  | Nat.succ n, .cons newest past =>
      newest.comp (operator past)

@[simp] theorem operator_nil (d : ℕ) :
    operator (InterventionSlotWord.nil : InterventionSlotWord d 0) =
      (LinearMap.id : QMat d →ₗ[ℂ] QMat d) := by
  rfl

@[simp] theorem operator_cons
    {d n : ℕ}
    (newest : QMat d →ₗ[ℂ] QMat d)
    (past : InterventionSlotWord d n) :
    operator (.cons newest past) = newest.comp (operator past) := by
  rfl

end InterventionSlotWord

/-!
## Direct open-comb tensor-link response
-/

namespace QuantumCombChoi

/--
Direct all-leg tensor-link pairing of an open comb Choi matrix with a complete
fixed-length slot Choi tensor.  The slot tensor is transposed in the bilinear
pairing, matching the matrix-unit contraction convention used by the existing
Choi reconstruction formulas.
-/
def tensorLinkScalar
    {d n : ℕ}
    (Q : QuantumCombChoi d n)
    (slots : ChoiSlotWord d n) : ℂ :=
  ∑ r : CombIndex d n, ∑ c : CombIndex d n,
    Q.choi r c * ChoiSlotWord.slotTensor slots c r

/-- Direct operational response of an open comb to a fixed intervention history. -/
def interventionResponse
    {d n : ℕ}
    (Q : QuantumCombChoi d n)
    (slots : InterventionSlotWord d n) : ℂ :=
  Q.tensorLinkScalar slots.toChoi

/-- Additivity of the direct comb contraction in the newest Choi slot. -/
theorem tensorLinkScalar_cons_add
    {d n : ℕ}
    (Q : QuantumCombChoi d (Nat.succ n))
    (A B : ChoiMat d d)
    (past : ChoiSlotWord d n) :
    Q.tensorLinkScalar (.cons (A + B) past) =
      Q.tensorLinkScalar (.cons A past) +
        Q.tensorLinkScalar (.cons B past) := by
  simp [tensorLinkScalar, ChoiSlotWord.slotTensor_cons_add,
    Finset.sum_add_distrib, mul_add]

/-- Complex homogeneity of the direct comb contraction in the newest Choi slot. -/
theorem tensorLinkScalar_cons_smul
    {d n : ℕ}
    (Q : QuantumCombChoi d (Nat.succ n))
    (a : ℂ)
    (A : ChoiMat d d)
    (past : ChoiSlotWord d n) :
    Q.tensorLinkScalar (.cons (a • A) past) =
      a * Q.tensorLinkScalar (.cons A past) := by
  simp [tensorLinkScalar, ChoiSlotWord.slotTensor_cons_smul,
    Finset.mul_sum]
  ring

end QuantumCombChoi

/-!
## External operational realization
-/

/--
An explicit realization of an external history carrier by one open quantum
comb.  The external response is required to agree with the direct all-leg Choi
contraction for the encoded fixed-length intervention history.

This is a witness, not an automatic identification of arbitrary history data
with a quantum process tensor.
-/
structure OpenCombOperationalRealization
    {d n : ℕ}
    (Q : QuantumCombChoi d n)
    (History : Type u) where
  interventionWord : History → InterventionSlotWord d n
  response : History → ℂ
  response_eq : ∀ h : History,
    response h = Q.interventionResponse (interventionWord h)

namespace OpenCombOperationalRealization

variable {d n : ℕ} {Q : QuantumCombChoi d n} {History : Type u}

/-- Every realized history response is exactly the direct open-comb tensor-link scalar. -/
theorem response_eq_tensorLinkScalar
    (R : OpenCombOperationalRealization Q History)
    (h : History) :
    R.response h =
      Q.tensorLinkScalar (R.interventionWord h).toChoi := by
  exact R.response_eq h

end OpenCombOperationalRealization

/-!
## Sequential factorization as a special case
-/

/--
Certificate that an open-comb response actually depends only on the one channel
obtained by composing all intervention slots, acting on one fixed initial matrix
and followed by one fixed complex-linear readout.

This is a strict specialization of the open history-sensitive semantics.
-/
structure SequentialFactorization
    {d n : ℕ}
    (Q : QuantumCombChoi d n) where
  initial : QMat d
  readout : QMat d →ₗ[ℂ] ℂ
  response_eq : ∀ slots : InterventionSlotWord d n,
    Q.interventionResponse slots =
      readout (InterventionSlotWord.operator slots initial)

/--
The open comb distinguishes two intervention histories even though their total
composed channel maps are identical.
-/
def DistinguishesEqualOperatorHistories
    {d n : ℕ}
    (Q : QuantumCombChoi d n) : Prop :=
  ∃ left right : InterventionSlotWord d n,
    InterventionSlotWord.operator left =
      InterventionSlotWord.operator right ∧
    Q.interventionResponse left ≠ Q.interventionResponse right

/--
If an open comb distinguishes equal-composite intervention histories, it cannot
factor through one fixed initial matrix, the composed channel alone, and one
fixed final readout.
-/
theorem not_sequentiallyFactorizable_of_distinguishesEqualOperatorHistories
    {d n : ℕ}
    (Q : QuantumCombChoi d n)
    (hDist : DistinguishesEqualOperatorHistories Q) :
    ¬ Nonempty (SequentialFactorization Q) := by
  rintro ⟨F⟩
  rcases hDist with ⟨left, right, hOperator, hResponse⟩
  apply hResponse
  calc
    Q.interventionResponse left =
        F.readout (InterventionSlotWord.operator left F.initial) :=
      F.response_eq left
    _ = F.readout (InterventionSlotWord.operator right F.initial) := by
      rw [hOperator]
    _ = Q.interventionResponse right :=
      (F.response_eq right).symm

/--
The same obstruction can be stated directly for an external operational
realization: equal-composite histories with distinct realized responses force
the representing open comb to be non-sequential in the above sense.
-/
theorem no_sequentialFactorization_of_realized_equalOperator_distinction
    {d n : ℕ}
    {Q : QuantumCombChoi d n}
    {History : Type u}
    (R : OpenCombOperationalRealization Q History)
    (left right : History)
    (hOperator :
      InterventionSlotWord.operator (R.interventionWord left) =
        InterventionSlotWord.operator (R.interventionWord right))
    (hResponse : R.response left ≠ R.response right) :
    ¬ Nonempty (SequentialFactorization Q) := by
  apply not_sequentiallyFactorizable_of_distinguishesEqualOperatorHistories Q
  refine ⟨R.interventionWord left, R.interventionWord right, hOperator, ?_⟩
  intro hEq
  apply hResponse
  calc
    R.response left = Q.interventionResponse (R.interventionWord left) :=
      R.response_eq left
    _ = Q.interventionResponse (R.interventionWord right) := hEq
    _ = R.response right := (R.response_eq right).symm

end

end KUOS.DependentOriginationOpenCombOperationalRealizationV0_14
