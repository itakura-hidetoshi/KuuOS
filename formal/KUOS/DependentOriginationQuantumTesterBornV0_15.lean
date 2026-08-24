import Mathlib
import KUOS.DependentOriginationOpenCombOperationalRealizationV0_14
import KUOS.DependentOriginationQuantumInstrumentBornCombV0_12

namespace KUOS.DependentOriginationQuantumTesterBornV0_15

open scoped BigOperators MatrixOrder CStarAlgebra ComplexOrder Kronecker
open Matrix
open KUOS.DependentOriginationQuantumChoiCombV0_9
open KUOS.DependentOriginationQuantumInstrumentBornCombV0_12
open KUOS.DependentOriginationOpenCombOperationalRealizationV0_14

noncomputable section

universe u

/-!
# Quantum process testers and Born probabilities v0.15

The v0.14 open-comb contraction is a complex-linear response functional.  An
arbitrary open deterministic comb is not, by itself, a normalized scalar
probability tester.  This layer makes that boundary explicit.

A closed quantum process tester is represented on the same recursive
`CombIndex` carrier, but it additionally carries the operational deterministic
tester normalization: every fixed-length word of trace-preserving Choi slots
has scalar response exactly one.

Together with positive semidefiniteness this gives the two Born axioms needed
for arbitrary finite instrument histories:

* every selected CP outcome history has nonnegative weight;
* replacing every instrument by its summed deterministic Choi operation gives
  total weight one.

No arbitrary v0.14 open-comb response is silently promoted to a probability.
-/

/-!
## Positive and deterministic Choi slot words
-/

namespace ChoiSlotWord

/-- Every Choi matrix in a fixed-length slot word is positive semidefinite. -/
def Positive {d : ℕ} : {n : ℕ} → ChoiSlotWord d n → Prop
  | 0, .nil => True
  | Nat.succ _, .cons newest past => newest.PosSemidef ∧ Positive past

/-- Every Choi matrix in the slot word has the trace-preserving Choi normalization. -/
def TracePreserving {d : ℕ} : {n : ℕ} → ChoiSlotWord d n → Prop
  | 0, .nil => True
  | Nat.succ _, .cons newest past =>
      partialTraceOutput newest = 1 ∧ TracePreserving past

/-- The recursive slot tensor is exactly the Kronecker product of past and newest slot. -/
theorem slotTensor_cons_eq_kronecker
    {d n : ℕ}
    (newest : ChoiMat d d)
    (past : ChoiSlotWord d n) :
    slotTensor (.cons newest past) = slotTensor past ⊗ₖ newest := by
  rfl

/-- Positive Choi slots tensor to a positive semidefinite full history matrix. -/
theorem slotTensor_posSemidef {d : ℕ} :
    ∀ {n : ℕ} (slots : ChoiSlotWord d n),
      Positive slots → (slotTensor slots).PosSemidef
  | 0, .nil, _ => by
      simpa using
        (Matrix.posSemidef_conjTranspose_mul_self
          (1 : Matrix (CombIndex d 0) (CombIndex d 0) ℂ))
  | Nat.succ n, .cons newest past, h => by
      rw [slotTensor_cons_eq_kronecker]
      exact (slotTensor_posSemidef past h.2).kronecker h.1

end ChoiSlotWord

/-!
## Positive Hilbert--Schmidt pairing
-/

/-- Trace pairing of a closed tester matrix with a complete slot-history tensor. -/
def testerPairing
    {d n : ℕ}
    (W : Matrix (CombIndex d n) (CombIndex d n) ℂ)
    (slots : ChoiSlotWord d n) : ℂ :=
  Matrix.trace (W * ChoiSlotWord.slotTensor slots)

/-- The v0.14 direct all-leg sum is exactly this trace pairing. -/
theorem openComb_tensorLinkScalar_eq_testerPairing
    {d n : ℕ}
    (Q : QuantumCombChoi d n)
    (slots : ChoiSlotWord d n) :
    Q.tensorLinkScalar slots = testerPairing Q.choi slots := by
  classical
  simp [QuantumCombChoi.tensorLinkScalar, testerPairing,
    Matrix.trace, Matrix.mul_apply]

/-- The trace of the product of two positive semidefinite complex matrices is nonnegative. -/
theorem trace_mul_nonneg_of_posSemidef
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    {A B : Matrix ι ι ℂ}
    (hA : A.PosSemidef)
    (hB : B.PosSemidef) :
    0 ≤ Matrix.trace (A * B) := by
  obtain ⟨C, hC⟩ := CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hB.nonneg
  rw [hC]
  change 0 ≤ Matrix.trace (A * (Cᴴ * C))
  rw [Matrix.trace_mul_cycle']
  have hCAC : (C * A * Cᴴ).PosSemidef :=
    hA.mul_mul_conjTranspose_same C
  simpa [Matrix.mul_assoc] using hCAC.trace_nonneg

/-- Positive tester matrix paired with positive Choi slots has nonnegative complex weight. -/
theorem testerPairing_nonneg
    {d n : ℕ}
    {W : Matrix (CombIndex d n) (CombIndex d n) ℂ}
    (hW : W.PosSemidef)
    (slots : ChoiSlotWord d n)
    (hSlots : ChoiSlotWord.Positive slots) :
    0 ≤ testerPairing W slots := by
  apply trace_mul_nonneg_of_posSemidef hW
  exact ChoiSlotWord.slotTensor_posSemidef slots hSlots

/-!
## Closed quantum process tester
-/

/--
Operational deterministic-tester normalization.

Every admissible deterministic intervention history -- a word whose Choi slots
are trace preserving -- has scalar response exactly one.
-/
def TesterNormalized
    {d n : ℕ}
    (W : Matrix (CombIndex d n) (CombIndex d n) ℂ) : Prop :=
  ∀ slots : ChoiSlotWord d n,
    ChoiSlotWord.TracePreserving slots →
      testerPairing W slots = 1

/-- A positive normalized closed quantum process tester in complete Choi form. -/
structure QuantumProcessTesterChoi (d n : ℕ) where
  choi : Matrix (CombIndex d n) (CombIndex d n) ℂ
  positive : choi.PosSemidef
  normalized : TesterNormalized choi

namespace QuantumProcessTesterChoi

/-- Complex Born weight assigned by a closed tester to a complete Choi-slot history. -/
def weight
    {d n : ℕ}
    (T : QuantumProcessTesterChoi d n)
    (slots : ChoiSlotWord d n) : ℂ :=
  testerPairing T.choi slots

/-- Real Born probability extracted from the complex-order nonnegative weight. -/
def probability
    {d n : ℕ}
    (T : QuantumProcessTesterChoi d n)
    (slots : ChoiSlotWord d n) : ℝ :=
  (T.weight slots).re

/-- Every positive selected slot history has nonnegative complex Born weight. -/
theorem weight_nonneg
    {d n : ℕ}
    (T : QuantumProcessTesterChoi d n)
    (slots : ChoiSlotWord d n)
    (hSlots : ChoiSlotWord.Positive slots) :
    0 ≤ T.weight slots := by
  exact testerPairing_nonneg T.positive slots hSlots

/-- Every positive selected slot history has nonnegative real Born probability. -/
theorem probability_nonneg
    {d n : ℕ}
    (T : QuantumProcessTesterChoi d n)
    (slots : ChoiSlotWord d n)
    (hSlots : ChoiSlotWord.Positive slots) :
    0 ≤ T.probability slots := by
  exact (Complex.nonneg_iff.mp (T.weight_nonneg slots hSlots)).1

/-- Every deterministic trace-preserving slot word has total tester weight exactly one. -/
theorem deterministic_weight_eq_one
    {d n : ℕ}
    (T : QuantumProcessTesterChoi d n)
    (slots : ChoiSlotWord d n)
    (hTP : ChoiSlotWord.TracePreserving slots) :
    T.weight slots = 1 := by
  exact T.normalized slots hTP

/-- Every deterministic trace-preserving slot word has real probability exactly one. -/
theorem deterministic_probability_eq_one
    {d n : ℕ}
    (T : QuantumProcessTesterChoi d n)
    (slots : ChoiSlotWord d n)
    (hTP : ChoiSlotWord.TracePreserving slots) :
    T.probability slots = 1 := by
  have h := congrArg Complex.re (T.deterministic_weight_eq_one slots hTP)
  simpa [probability] using h

end QuantumProcessTesterChoi

/-!
## Finite quantum-instrument schedules
-/

inductive InstrumentSlotSchedule
    (d : ℕ) (Outcome : Type u) [Fintype Outcome] : ℕ → Type
  | nil : InstrumentSlotSchedule d Outcome 0
  | cons {n : ℕ}
      (newest : QuantumInstrument d Outcome)
      (past : InstrumentSlotSchedule d Outcome n) :
      InstrumentSlotSchedule d Outcome (Nat.succ n)

namespace InstrumentSlotSchedule

variable {d : ℕ} {Outcome : Type u} [Fintype Outcome]

/-- Replace each finite instrument by its summed deterministic Choi operation. -/
def totalChoiWord : {n : ℕ} →
    InstrumentSlotSchedule d Outcome n → ChoiSlotWord d n
  | 0, .nil => .nil
  | Nat.succ _, .cons newest past =>
      .cons newest.totalChoi (totalChoiWord past)

/-- Every summed instrument slot is trace preserving in Choi form. -/
theorem totalChoiWord_tracePreserving :
    ∀ {n : ℕ} (schedule : InstrumentSlotSchedule d Outcome n),
      ChoiSlotWord.TracePreserving schedule.totalChoiWord
  | 0, .nil => trivial
  | Nat.succ _, .cons newest past => by
      exact ⟨newest.totalChoi_normalized,
        totalChoiWord_tracePreserving past⟩

/--
Iterated tensor sum over all outcomes, kept at the Choi-history matrix level.
Each recursive finite sum is one instrument outcome sum.
-/
def outcomeTensorSum : {n : ℕ} →
    InstrumentSlotSchedule d Outcome n →
      Matrix (CombIndex d n) (CombIndex d n) ℂ
  | 0, .nil => 1
  | Nat.succ _, .cons newest past =>
      ∑ o : Outcome,
        outcomeTensorSum past ⊗ₖ newest.outcomeChoi o

/-- The iterated all-outcome tensor equals the tensor of the total deterministic Choi word. -/
theorem outcomeTensorSum_eq_totalSlotTensor :
    ∀ {n : ℕ} (schedule : InstrumentSlotSchedule d Outcome n),
      schedule.outcomeTensorSum =
        ChoiSlotWord.slotTensor schedule.totalChoiWord
  | 0, .nil => rfl
  | Nat.succ n, .cons newest past => by
      classical
      ext r c
      simp [outcomeTensorSum, totalChoiWord,
        ChoiSlotWord.slotTensor, outcomeTensorSum_eq_totalSlotTensor past,
        QuantumInstrument.totalChoi, Finset.mul_sum]

end InstrumentSlotSchedule

/-!
## Selected instrument histories
-/

inductive SelectedInstrumentHistory
    (d : ℕ) (Outcome : Type u) [Fintype Outcome] : ℕ → Type
  | nil : SelectedInstrumentHistory d Outcome 0
  | cons {n : ℕ}
      (instrument : QuantumInstrument d Outcome)
      (outcome : Outcome)
      (past : SelectedInstrumentHistory d Outcome n) :
      SelectedInstrumentHistory d Outcome (Nat.succ n)

namespace SelectedInstrumentHistory

variable {d : ℕ} {Outcome : Type u} [Fintype Outcome]

/-- Choi slot word of one explicitly selected finite instrument history. -/
def toChoiWord : {n : ℕ} →
    SelectedInstrumentHistory d Outcome n → ChoiSlotWord d n
  | 0, .nil => .nil
  | Nat.succ _, .cons instrument outcome past =>
      .cons (instrument.outcomeChoi outcome) (toChoiWord past)

/-- Every selected instrument outcome has a positive Choi matrix. -/
theorem toChoiWord_positive :
    ∀ {n : ℕ} (history : SelectedInstrumentHistory d Outcome n),
      ChoiSlotWord.Positive history.toChoiWord
  | 0, .nil => trivial
  | Nat.succ _, .cons instrument outcome past => by
      exact ⟨instrument.outcomeChoi_posSemidef outcome,
        toChoiWord_positive past⟩

end SelectedInstrumentHistory

namespace QuantumProcessTesterChoi

/-- One selected finite quantum-instrument history has nonnegative complex weight. -/
theorem selectedInstrumentWeight_nonneg
    {d n : ℕ} {Outcome : Type u} [Fintype Outcome]
    (T : QuantumProcessTesterChoi d n)
    (history : SelectedInstrumentHistory d Outcome n) :
    0 ≤ T.weight history.toChoiWord := by
  exact T.weight_nonneg history.toChoiWord history.toChoiWord_positive

/-- One selected finite quantum-instrument history has nonnegative real probability. -/
theorem selectedInstrumentProbability_nonneg
    {d n : ℕ} {Outcome : Type u} [Fintype Outcome]
    (T : QuantumProcessTesterChoi d n)
    (history : SelectedInstrumentHistory d Outcome n) :
    0 ≤ T.probability history.toChoiWord := by
  exact T.probability_nonneg history.toChoiWord history.toChoiWord_positive

/-- Complex total weight represented by the iterated finite sum over all instrument outcomes. -/
def totalInstrumentWeight
    {d n : ℕ} {Outcome : Type u} [Fintype Outcome]
    (T : QuantumProcessTesterChoi d n)
    (schedule : InstrumentSlotSchedule d Outcome n) : ℂ :=
  Matrix.trace (T.choi * schedule.outcomeTensorSum)

/-- The explicit iterated all-outcome tensor sum has total tester weight exactly one. -/
theorem totalInstrumentWeight_eq_one
    {d n : ℕ} {Outcome : Type u} [Fintype Outcome]
    (T : QuantumProcessTesterChoi d n)
    (schedule : InstrumentSlotSchedule d Outcome n) :
    T.totalInstrumentWeight schedule = 1 := by
  rw [totalInstrumentWeight,
    InstrumentSlotSchedule.outcomeTensorSum_eq_totalSlotTensor]
  exact T.deterministic_weight_eq_one schedule.totalChoiWord
    schedule.totalChoiWord_tracePreserving

/-- Real total probability of the full finite instrument outcome tensor. -/
def totalInstrumentProbability
    {d n : ℕ} {Outcome : Type u} [Fintype Outcome]
    (T : QuantumProcessTesterChoi d n)
    (schedule : InstrumentSlotSchedule d Outcome n) : ℝ :=
  (T.totalInstrumentWeight schedule).re

/-- The full finite quantum-instrument outcome law is normalized to one. -/
theorem totalInstrumentProbability_eq_one
    {d n : ℕ} {Outcome : Type u} [Fintype Outcome]
    (T : QuantumProcessTesterChoi d n)
    (schedule : InstrumentSlotSchedule d Outcome n) :
    T.totalInstrumentProbability schedule = 1 := by
  have h := congrArg Complex.re (T.totalInstrumentWeight_eq_one schedule)
  simpa [totalInstrumentProbability] using h

end QuantumProcessTesterChoi

end

end KUOS.DependentOriginationQuantumTesterBornV0_15
