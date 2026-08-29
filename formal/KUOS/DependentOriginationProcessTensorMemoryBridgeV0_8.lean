import Mathlib
import KUOS.DependentOriginationMemoryLiftedHistoryTransportV0_7

namespace KUOS.DependentOriginationProcessTensorMemoryBridgeV0_8

open KUOS.DependentOriginationHistorySensitiveTransportV0_5
open KUOS.DependentOriginationMemoryLiftedHistoryTransportV0_7

universe u v w

/-!
# Operational linear process tensor and finite-memory realization bridge

This file gives a mathematically explicit bridge between the v0.7 memory-lifted
non-Markov transport and an operational process-tensor interface.

The process tensor used here is structural rather than physical: it is a causal,
slotwise-linear functional of a finite ordered word of real-linear interventions.
No Choi representation, complete positivity, trace preservation, Hilbert-space
quantum channel structure, or Yang--Mills physical theorem is asserted.
-/

section LinearProcessTensor

variable {State : Type u} {Output : Type v}
variable [AddCommGroup State] [Module ℝ State]
variable [AddCommGroup Output] [Module ℝ Output]

/--
The linear operator represented by a finite ordered intervention word.
The head intervention acts after the recursively evaluated tail, matching the
KuuOS finite-history convention.
-/
def interventionWordOperator :
    List (State →ₗ[ℝ] State) → State →ₗ[ℝ] State
  | [] => LinearMap.id
  | intervention :: tail =>
      intervention.comp (interventionWordOperator tail)

@[simp] theorem interventionWordOperator_nil_apply
    (x : State) :
    interventionWordOperator ([] : List (State →ₗ[ℝ] State)) x = x :=
  rfl

@[simp] theorem interventionWordOperator_cons_apply
    (intervention : State →ₗ[ℝ] State)
    (tail : List (State →ₗ[ℝ] State))
    (x : State) :
    interventionWordOperator (intervention :: tail) x =
      intervention (interventionWordOperator tail x) :=
  rfl

/-- Concatenating intervention words is causal composition. -/
theorem interventionWordOperator_append
    (left right : List (State →ₗ[ℝ] State)) :
    interventionWordOperator (left ++ right) =
      (interventionWordOperator left).comp
        (interventionWordOperator right) := by
  induction left with
  | nil =>
      ext x
      rfl
  | cons intervention tail ih =>
      ext x
      simp [interventionWordOperator, ih]

/-- Elementwise form of causal intervention-word composition. -/
@[simp] theorem interventionWordOperator_append_apply
    (left right : List (State →ₗ[ℝ] State))
    (x : State) :
    interventionWordOperator (left ++ right) x =
      interventionWordOperator left
        (interventionWordOperator right x) := by
  rw [interventionWordOperator_append]
  rfl

/--
Operational linear process tensor: an initial enlarged state together with a
linear readout.  Its response to intervention slots is obtained by composing
the supplied interventions and then applying the readout.
-/
structure OperationalLinearProcessTensor
    (State : Type u) (Output : Type v)
    [AddCommGroup State] [Module ℝ State]
    [AddCommGroup Output] [Module ℝ Output] where
  initial : State
  readout : State →ₗ[ℝ] Output

namespace OperationalLinearProcessTensor

variable (P : OperationalLinearProcessTensor State Output)

/-- Response of the process tensor to a finite ordered intervention word. -/
def response
    (word : List (State →ₗ[ℝ] State)) : Output :=
  P.readout (interventionWordOperator word P.initial)

/-- Empty intervention history returns the initial-state readout. -/
@[simp] theorem response_nil :
    P.response [] = P.readout P.initial :=
  rfl

/--
Causal split: the right history prepares the intermediate state before the left
history acts.  No operation in `left` is needed to define that intermediate
state.
-/
theorem response_append
    (left right : List (State →ₗ[ℝ] State)) :
    P.response (left ++ right) =
      P.readout
        (interventionWordOperator left
          (interventionWordOperator right P.initial)) := by
  simp [response]

/--
The defining process-tensor multilinearity, written without choosing a tensor
product representation: with all other slots fixed, the response is real-linear
in the selected intervention slot.
-/
theorem response_slotwise_linear
    (left right : List (State →ₗ[ℝ] State))
    (A B : State →ₗ[ℝ] State)
    (a b : ℝ) :
    P.response (left ++ [a • A + b • B] ++ right) =
      a • P.response (left ++ [A] ++ right) +
        b • P.response (left ++ [B] ++ right) := by
  simp [response, List.append_assoc]

end OperationalLinearProcessTensor

end LinearProcessTensor

/-!
## Finite-memory realization of the process tensor

A v0.7 `MemoryLiftedStep` becomes a genuine operational linear process tensor
once each event update on `Visible × Memory` is supplied as a real-linear map.
That extra witness is explicit: the generic nonlinear v0.7 layer is not silently
promoted to a linear process tensor.
-/

section MemoryRealization

variable {Event : Type u}
variable {Visible : Type v} {Memory : Type w}
variable [AddCommGroup Visible] [Module ℝ Visible]
variable [AddCommGroup Memory] [Module ℝ Memory]

namespace MemoryLiftedStep

/--
Explicit real-linear realization of each event update on the enlarged
visible-plus-memory carrier.
-/
structure LinearRealization
    (S : MemoryLiftedStep Event Visible Memory) where
  eventOperator : Event → ((Visible × Memory) →ₗ[ℝ] (Visible × Memory))
  eventOperator_apply : ∀ (event : Event) (state : Visible × Memory),
    eventOperator event state = S.extendedStep event state

namespace LinearRealization

variable {S : MemoryLiftedStep Event Visible Memory}

/-- Visible projection from the enlarged state carrier. -/
def visibleProjection : (Visible × Memory) →ₗ[ℝ] Visible where
  toFun := Prod.fst
  map_add' := by
    intro x y
    rfl
  map_smul' := by
    intro c x
    rfl

/-- Memory projection from the enlarged state carrier. -/
def memoryProjection : (Visible × Memory) →ₗ[ℝ] Memory where
  toFun := Prod.snd
  map_add' := by
    intro x y
    rfl
  map_smul' := by
    intro c x
    rfl

/-- Process tensor with visible readout at a fixed initial visible/memory state. -/
def toVisibleProcessTensor
    (L : MemoryLiftedStep.LinearRealization S)
    (initialMemory : Memory) (x : Visible) :
    OperationalLinearProcessTensor (Visible × Memory) Visible where
  initial := (x, initialMemory)
  readout := visibleProjection

/-- Process tensor with memory readout at the same initial enlarged state. -/
def toMemoryProcessTensor
    (L : MemoryLiftedStep.LinearRealization S)
    (initialMemory : Memory) (x : Visible) :
    OperationalLinearProcessTensor (Visible × Memory) Memory where
  initial := (x, initialMemory)
  readout := memoryProjection

/-- Convert an event word into the corresponding linear intervention word. -/
def eventInterventionWord
    (L : MemoryLiftedStep.LinearRealization S)
    (word : List Event) :
    List ((Visible × Memory) →ₗ[ℝ] (Visible × Memory)) :=
  word.map L.eventOperator

/--
The linear intervention word evaluates exactly to the original v0.7 enlarged
history transport.  This is the core realization theorem.
-/
theorem interventionWordOperator_eventInterventionWord
    (L : MemoryLiftedStep.LinearRealization S)
    (word : List Event)
    (state : Visible × Memory) :
    interventionWordOperator (L.eventInterventionWord word) state =
      S.toHistoryTransport.eval word state := by
  induction word with
  | nil =>
      exact (S.toHistoryTransport.eval_nil_apply state).symm
  | cons event tail ih =>
      change
        L.eventOperator event
            (interventionWordOperator (L.eventInterventionWord tail) state) =
          S.extendedStep event (S.toHistoryTransport.eval tail state)
      rw [ih, L.eventOperator_apply]

/-- Visible process-tensor response to an event word. -/
def eventVisibleResponse
    (L : MemoryLiftedStep.LinearRealization S)
    (initialMemory : Memory)
    (word : List Event)
    (x : Visible) : Visible :=
  (L.toVisibleProcessTensor initialMemory x).response
    (L.eventInterventionWord word)

/-- Memory process-tensor response to the same event word. -/
def eventMemoryResponse
    (L : MemoryLiftedStep.LinearRealization S)
    (initialMemory : Memory)
    (word : List Event)
    (x : Visible) : Memory :=
  (L.toMemoryProcessTensor initialMemory x).response
    (L.eventInterventionWord word)

/--
Exact bridge: visible process-tensor response is the v0.7 visible non-Markov
evaluation, not merely an approximation or analogy.
-/
theorem eventVisibleResponse_eq_visibleEval
    (L : MemoryLiftedStep.LinearRealization S)
    (initialMemory : Memory)
    (word : List Event)
    (x : Visible) :
    L.eventVisibleResponse initialMemory word x =
      S.visibleEval initialMemory word x := by
  unfold eventVisibleResponse OperationalLinearProcessTensor.response
    toVisibleProcessTensor eventInterventionWord
    KUOS.DependentOriginationMemoryLiftedHistoryTransportV0_7.MemoryLiftedStep.visibleEval
  change
    (interventionWordOperator (L.eventInterventionWord word) (x, initialMemory)).1 =
      (S.toHistoryTransport.eval word (x, initialMemory)).1
  exact congrArg Prod.fst
    (L.interventionWordOperator_eventInterventionWord word (x, initialMemory))

/-- Exact bridge for the hidden memory output. -/
theorem eventMemoryResponse_eq_memoryEval
    (L : MemoryLiftedStep.LinearRealization S)
    (initialMemory : Memory)
    (word : List Event)
    (x : Visible) :
    L.eventMemoryResponse initialMemory word x =
      S.memoryEval initialMemory word x := by
  unfold eventMemoryResponse OperationalLinearProcessTensor.response
    toMemoryProcessTensor eventInterventionWord
    KUOS.DependentOriginationMemoryLiftedHistoryTransportV0_7.MemoryLiftedStep.memoryEval
  change
    (interventionWordOperator (L.eventInterventionWord word) (x, initialMemory)).2 =
      (S.toHistoryTransport.eval word (x, initialMemory)).2
  exact congrArg Prod.snd
    (L.interventionWordOperator_eventInterventionWord word (x, initialMemory))

/--
Process-tensor causal composition reproduces the exact v0.7 non-Markov visible
composition law: the earlier/right history passes both visible state and memory
to the later/left history.
-/
theorem eventVisibleResponse_append
    (L : MemoryLiftedStep.LinearRealization S)
    (initialMemory : Memory)
    (left right : List Event)
    (x : Visible) :
    L.eventVisibleResponse initialMemory (left ++ right) x =
      L.eventVisibleResponse
        (L.eventMemoryResponse initialMemory right x)
        left
        (L.eventVisibleResponse initialMemory right x) := by
  rw [L.eventVisibleResponse_eq_visibleEval,
    S.visibleEval_append,
    L.eventMemoryResponse_eq_memoryEval,
    L.eventVisibleResponse_eq_visibleEval,
    L.eventVisibleResponse_eq_visibleEval]

/-- The hidden-memory causal composition law in process-tensor language. -/
theorem eventMemoryResponse_append
    (L : MemoryLiftedStep.LinearRealization S)
    (initialMemory : Memory)
    (left right : List Event)
    (x : Visible) :
    L.eventMemoryResponse initialMemory (left ++ right) x =
      L.eventMemoryResponse
        (L.eventMemoryResponse initialMemory right x)
        left
        (L.eventVisibleResponse initialMemory right x) := by
  rw [L.eventMemoryResponse_eq_memoryEval,
    S.memoryEval_append,
    L.eventMemoryResponse_eq_memoryEval,
    L.eventVisibleResponse_eq_visibleEval,
    L.eventMemoryResponse_eq_memoryEval]

end LinearRealization

end MemoryLiftedStep

end MemoryRealization

/-!
## Non-Markov history sensitivity as process-tensor history sensitivity
-/

section AdditiveSummary

variable {Time : Type u} [AddMonoid Time]
variable {Visible : Type v} {Memory : Type w}
variable [AddCommGroup Visible] [Module ℝ Visible]
variable [AddCommGroup Memory] [Module ℝ Memory]

namespace MemoryLiftedStep.LinearRealization

variable {S : MemoryLiftedStep Time Visible Memory}

/--
Process-tensor version of genuine history sensitivity: equal-summary event words
produce different visible process-tensor responses for some initial visible state
at the same initial memory.
-/
def GenuinelyProcessTensorHistorySensitive
    (L : MemoryLiftedStep.LinearRealization S)
    (initialMemory : Memory) : Prop :=
  ∃ left right : List Time,
    left.sum = right.sum ∧
      ∃ x : Visible,
        L.eventVisibleResponse initialMemory left x ≠
          L.eventVisibleResponse initialMemory right x

/--
Exact equivalence: the v0.7 visible non-Markov witness and the operational
process-tensor history-sensitivity witness are the same mathematical statement
under a linear realization.
-/
theorem genuinelyProcessTensorHistorySensitive_iff_visible
    (L : MemoryLiftedStep.LinearRealization S)
    (initialMemory : Memory) :
    L.GenuinelyProcessTensorHistorySensitive initialMemory ↔
      S.GenuinelyVisibleHistorySensitive initialMemory := by
  constructor
  · intro h
    rcases h with ⟨left, right, hSum, x, hx⟩
    refine ⟨left, right, hSum, x, ?_⟩
    simpa [L.eventVisibleResponse_eq_visibleEval] using hx
  · intro h
    rcases h with ⟨left, right, hSum, x, hx⟩
    refine ⟨left, right, hSum, x, ?_⟩
    simpa [L.eventVisibleResponse_eq_visibleEval] using hx

/--
Therefore a genuine non-Markov process-tensor witness rules out every additive
one-parameter total-time factorization of the enlarged history transport.
-/
theorem no_totalTimeFactorization_of_processTensor_history_sensitive
    (L : MemoryLiftedStep.LinearRealization S)
    (initialMemory : Memory)
    (h : L.GenuinelyProcessTensorHistorySensitive initialMemory) :
    ¬ Nonempty (TotalTimeFactorization S.toHistoryTransport) := by
  apply S.no_totalTimeFactorization_of_visible_history_sensitive initialMemory
  exact
    (L.genuinelyProcessTensorHistorySensitive_iff_visible initialMemory).mp h

/--
Conversely, any total-time factorization forces equal-summary event words to
have the same visible process-tensor response.
-/
theorem eventVisibleResponse_eq_of_sum_eq_of_factorization
    (L : MemoryLiftedStep.LinearRealization S)
    (F : TotalTimeFactorization S.toHistoryTransport)
    (initialMemory : Memory)
    (left right : List Time)
    (x : Visible)
    (hSum : left.sum = right.sum) :
    L.eventVisibleResponse initialMemory left x =
      L.eventVisibleResponse initialMemory right x := by
  rw [L.eventVisibleResponse_eq_visibleEval,
    L.eventVisibleResponse_eq_visibleEval]
  exact
    S.visibleEval_eq_of_sum_eq_of_factorization F initialMemory left right x hSum

end MemoryLiftedStep.LinearRealization

end AdditiveSummary

end KUOS.DependentOriginationProcessTensorMemoryBridgeV0_8
