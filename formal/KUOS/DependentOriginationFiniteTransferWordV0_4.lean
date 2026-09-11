import Mathlib
import KUOS.DependentOriginationLinearTransferConnectedReadoutV0_3

namespace KUOS.DependentOriginationFiniteTransferWordV0_4

open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationExponentialGapTransportV0_2
open KUOS.DependentOriginationLinearTransferConnectedReadoutV0_3

universe u

namespace ExponentiallyGappedVacuumTransport

variable {State : Type u} [SeminormedAddCommGroup State] [NormedSpace ℝ State]

namespace LinearTransferRealization

variable {D : ExponentiallyGappedVacuumTransport State}

/--
A finite positive-time transfer word.  The list order is retained syntactically
as a finite history of composable dependent-origination transfers.
-/
abbrev TransferWord := List NNReal

/-- Total elapsed positive time represented by a finite transfer word. -/
def wordTotalTime (word : TransferWord) : NNReal :=
  word.sum

/--
Evaluate a finite transfer word using the supplied linear transfer realization.
The head transfer acts after the recursively evaluated tail, matching the
semigroup convention `T_(s+t) = T_s ∘ T_t` used by the transport spine.
-/
def wordOperatorApply
    (L : D.LinearTransferRealization) : TransferWord → State → State
  | [], x => x
  | t :: tail, x => L.operator t (L.wordOperatorApply tail x)

/-- The empty transfer word is the identity history. -/
@[simp] theorem wordOperatorApply_nil
    (L : D.LinearTransferRealization) (x : State) :
    L.wordOperatorApply [] x = x :=
  rfl

/-- A nonempty word evaluates by applying its head transfer to its tail history. -/
@[simp] theorem wordOperatorApply_cons
    (L : D.LinearTransferRealization)
    (t : NNReal) (tail : TransferWord) (x : State) :
    L.wordOperatorApply (t :: tail) x =
      L.operator t (L.wordOperatorApply tail x) :=
  rfl

/-- Concatenation of transfer words is composition of their transfer histories. -/
theorem wordOperatorApply_append
    (L : D.LinearTransferRealization)
    (left right : TransferWord) (x : State) :
    L.wordOperatorApply (left ++ right) x =
      L.wordOperatorApply left (L.wordOperatorApply right x) := by
  induction left with
  | nil => rfl
  | cons t tail ih =>
      change
        L.operator t (L.wordOperatorApply (tail ++ right) x) =
          L.operator t (L.wordOperatorApply tail (L.wordOperatorApply right x))
      rw [ih]

/-- Total time is additive under word concatenation. -/
theorem wordTotalTime_append
    (left right : TransferWord) :
    wordTotalTime (left ++ right) =
      wordTotalTime left + wordTotalTime right := by
  simp [wordTotalTime]

/--
Every finite transfer word in the one-parameter additive semigroup evaluates to
the single transfer at its total elapsed time.

This theorem is the precise boundary between history syntax and semigroup
semantics: the word remembers the ordered finite history, while the present
Markov/semigroup realization factors its denotation through total time.
-/
theorem wordOperatorApply_eq_totalTime
    (L : D.LinearTransferRealization)
    (word : TransferWord) (x : State) :
    L.wordOperatorApply word x =
      D.transport (wordTotalTime word) x := by
  induction word with
  | nil =>
      calc
        L.wordOperatorApply [] x = x := rfl
        _ = D.transport 0 x := (D.transport_zero x).symm
        _ = D.transport (wordTotalTime []) x := by
          simp [wordTotalTime]
  | cons t tail ih =>
      calc
        L.wordOperatorApply (t :: tail) x =
            L.operator t (L.wordOperatorApply tail x) := rfl
        _ = L.operator t (D.transport (wordTotalTime tail) x) := by
          rw [ih]
        _ = D.transport t (D.transport (wordTotalTime tail) x) := by
          rw [L.operator_apply]
        _ = D.transport (t + wordTotalTime tail) x :=
          (D.transport_add t (wordTotalTime tail) x).symm
        _ = D.transport (wordTotalTime (t :: tail)) x := by
          simp [wordTotalTime]

/-- Two words with the same total time have the same denotation in this semigroup realization. -/
theorem wordOperatorApply_eq_of_totalTime_eq
    (L : D.LinearTransferRealization)
    (left right : TransferWord) (x : State)
    (h : wordTotalTime left = wordTotalTime right) :
    L.wordOperatorApply left x = L.wordOperatorApply right x := by
  calc
    L.wordOperatorApply left x = D.transport (wordTotalTime left) x :=
      L.wordOperatorApply_eq_totalTime left x
    _ = D.transport (wordTotalTime right) x := by rw [h]
    _ = L.wordOperatorApply right x :=
      (L.wordOperatorApply_eq_totalTime right x).symm

/-- Product of the exponential decay factors associated with all letters of a word. -/
def wordDecayProduct
    (D : ExponentiallyGappedVacuumTransport State) : TransferWord → ℝ
  | [] => 1
  | t :: tail => D.decayFactor t * D.wordDecayProduct tail

/-- The decay product of a finite word is exactly the decay factor at total time. -/
theorem wordDecayProduct_eq_totalTime
    (D : ExponentiallyGappedVacuumTransport State)
    (word : TransferWord) :
    D.wordDecayProduct word = D.decayFactor (wordTotalTime word) := by
  induction word with
  | nil =>
      simp [wordDecayProduct, wordTotalTime]
  | cons t tail ih =>
      calc
        D.wordDecayProduct (t :: tail) =
            D.decayFactor t * D.wordDecayProduct tail := rfl
        _ = D.decayFactor t * D.decayFactor (wordTotalTime tail) := by
          rw [ih]
        _ = D.decayFactor (t + wordTotalTime tail) :=
          (D.decayFactor_add t (wordTotalTime tail)).symm
        _ = D.decayFactor (wordTotalTime (t :: tail)) := by
          simp [wordTotalTime]

/-- Connected/vacuum-subtracted readout after a finite transfer word. -/
def connectedWordReadout
    (L : D.LinearTransferRealization)
    (R : BoundedReadout State)
    (word : TransferWord) (x : State) : ℝ :=
  R.readout (L.wordOperatorApply word x - D.vacuum)

/-- Finite-word connected readout factors through the total elapsed time. -/
theorem connectedWordReadout_eq_totalTime
    (L : D.LinearTransferRealization)
    (R : BoundedReadout State)
    (word : TransferWord) (x : State) :
    L.connectedWordReadout R word x =
      L.connectedReadout R (wordTotalTime word) x := by
  unfold connectedWordReadout connectedReadout
  rw [L.wordOperatorApply_eq_totalTime]

/--
A centered excitation has exponentially decaying connected readout along every
finite transfer word, with the rate controlled only by total elapsed time.
-/
theorem connected_word_readout_decay
    (L : D.LinearTransferRealization)
    (R : BoundedReadout State)
    (word : TransferWord) (x : State)
    (hx : L.CenteredExcitation x) :
    |L.connectedWordReadout R word x| ≤
      R.amplitude * D.decayFactor (wordTotalTime word) *
        ‖L.centeredState x‖ := by
  rw [L.connectedWordReadout_eq_totalTime R word x]
  exact L.connected_readout_decay R (wordTotalTime word) x hx

/-- The same finite-word decay bound written as the product of per-letter gap factors. -/
theorem connected_word_readout_decay_product
    (L : D.LinearTransferRealization)
    (R : BoundedReadout State)
    (word : TransferWord) (x : State)
    (hx : L.CenteredExcitation x) :
    |L.connectedWordReadout R word x| ≤
      R.amplitude * D.wordDecayProduct word * ‖L.centeredState x‖ := by
  rw [D.wordDecayProduct_eq_totalTime word]
  exact L.connected_word_readout_decay R word x hx

/-- Connected readout is invariant under replacing a word by any word of equal total time. -/
theorem connectedWordReadout_eq_of_totalTime_eq
    (L : D.LinearTransferRealization)
    (R : BoundedReadout State)
    (left right : TransferWord) (x : State)
    (h : wordTotalTime left = wordTotalTime right) :
    L.connectedWordReadout R left x =
      L.connectedWordReadout R right x := by
  calc
    L.connectedWordReadout R left x =
        L.connectedReadout R (wordTotalTime left) x :=
      L.connectedWordReadout_eq_totalTime R left x
    _ = L.connectedReadout R (wordTotalTime right) x := by rw [h]
    _ = L.connectedWordReadout R right x :=
      (L.connectedWordReadout_eq_totalTime R right x).symm

end LinearTransferRealization

end ExponentiallyGappedVacuumTransport

end KUOS.DependentOriginationFiniteTransferWordV0_4
