import Mathlib
import KUOS.DependentOriginationExponentialGapTransportV0_2

namespace KUOS.DependentOriginationLinearTransferConnectedReadoutV0_3

open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationExponentialGapTransportV0_2

universe u

namespace ExponentiallyGappedVacuumTransport

variable {State : Type u} [SeminormedAddCommGroup State] [NormedSpace ℝ State]

/--
A linear-transfer realization of an already supplied exponentially gapped
vacuum transport.

The v0.2 transport layer deliberately allowed nonlinear endomorphisms.  This
witness records the additional structure present in transfer-operator models:
for every positive time, the same transport is represented by an actual real
linear map.  No Hamiltonian, spectral theorem, or physical mass gap is created
here.
-/
structure LinearTransferRealization
    (D : ExponentiallyGappedVacuumTransport State) where
  operator : NNReal → State →ₗ[ℝ] State
  operator_eq_transport : ∀ (t : NNReal) (x : State),
    operator t x = D.transport t x

namespace LinearTransferRealization

variable {D : ExponentiallyGappedVacuumTransport State}

/-- The linear operator realizes exactly the underlying dependent-origination transport. -/
@[simp] theorem operator_apply
    (L : D.LinearTransferRealization) (t : NNReal) (x : State) :
    L.operator t x = D.transport t x :=
  L.operator_eq_transport t x

/-- Time zero acts identically in the linear transfer realization. -/
@[simp] theorem operator_zero_apply
    (L : D.LinearTransferRealization) (x : State) :
    L.operator 0 x = x := by
  calc
    L.operator 0 x = D.transport 0 x := L.operator_eq_transport 0 x
    _ = x := D.transport_zero x

/-- The linear transfer realization inherits the additive semigroup law pointwise. -/
theorem operator_add_apply
    (L : D.LinearTransferRealization)
    (s t : NNReal) (x : State) :
    L.operator (s + t) x = L.operator s (L.operator t x) := by
  calc
    L.operator (s + t) x = D.transport (s + t) x :=
      L.operator_eq_transport (s + t) x
    _ = D.transport s (D.transport t x) := D.transport_add s t x
    _ = L.operator s (L.operator t x) := by
      rw [L.operator_eq_transport s (L.operator t x),
        L.operator_eq_transport t x]

/-- The distinguished vacuum is a fixed vector of every linear transfer operator. -/
@[simp] theorem operator_vacuum_fixed
    (L : D.LinearTransferRealization) (t : NNReal) :
    L.operator t D.vacuum = D.vacuum := by
  calc
    L.operator t D.vacuum = D.transport t D.vacuum :=
      L.operator_eq_transport t D.vacuum
    _ = D.vacuum := D.vacuum_fixed t

/--
Linearity and vacuum fixation imply exact transport of vacuum-subtracted states:
`T_t (x - Ω) = T_t x - Ω`.
-/
theorem transport_sub_vacuum
    (L : D.LinearTransferRealization)
    (t : NNReal) (x : State) :
    D.transport t (x - D.vacuum) = D.transport t x - D.vacuum := by
  calc
    D.transport t (x - D.vacuum) = L.operator t (x - D.vacuum) :=
      (L.operator_eq_transport t (x - D.vacuum)).symm
    _ = L.operator t x - L.operator t D.vacuum := by
      rw [map_sub]
    _ = D.transport t x - D.vacuum := by
      rw [L.operator_eq_transport t x, L.operator_vacuum_fixed t]

/-- Vacuum-centered initial state associated with a supplied presentation. -/
def centeredState
    (L : D.LinearTransferRealization) (x : State) : State :=
  x - D.vacuum

/-- A presentation is centered-excitatory when its vacuum-subtracted state lies in the gap sector. -/
def CenteredExcitation
    (L : D.LinearTransferRealization) (x : State) : Prop :=
  D.Excitation (L.centeredState x)

/--
Connected/vacuum-subtracted scalar readout after positive-time transport.
The subtraction is performed at the transported state; linearity will identify
this with transporting the centered initial state.
-/
def connectedReadout
    (L : D.LinearTransferRealization)
    (R : BoundedReadout State)
    (t : NNReal) (x : State) : ℝ :=
  R.readout (D.transport t x - D.vacuum)

/-- Connected readout is exactly readout of the transported centered state. -/
theorem connectedReadout_eq_centered_transport
    (L : D.LinearTransferRealization)
    (R : BoundedReadout State)
    (t : NNReal) (x : State) :
    L.connectedReadout R t x =
      R.readout (D.transport t (L.centeredState x)) := by
  unfold connectedReadout centeredState
  rw [L.transport_sub_vacuum t x]

/--
The exponential excitation gap therefore gives exponential decay of every
bounded connected readout.
-/
theorem connected_readout_decay
    (L : D.LinearTransferRealization)
    (R : BoundedReadout State)
    (t : NNReal) (x : State)
    (hx : L.CenteredExcitation x) :
    |L.connectedReadout R t x| ≤
      R.amplitude * D.decayFactor t * ‖L.centeredState x‖ := by
  rw [L.connectedReadout_eq_centered_transport R t x]
  exact D.bounded_readout_decay R t (L.centeredState x) hx

/-- Connected readout along two successive transfers. -/
def connectedReadoutTwoStep
    (L : D.LinearTransferRealization)
    (R : BoundedReadout State)
    (s t : NNReal) (x : State) : ℝ :=
  R.readout (D.transport s (D.transport t x) - D.vacuum)

/-- Two successive connected transports are exactly connected transport at summed time. -/
theorem connectedReadoutTwoStep_eq_sum
    (L : D.LinearTransferRealization)
    (R : BoundedReadout State)
    (s t : NNReal) (x : State) :
    L.connectedReadoutTwoStep R s t x =
      L.connectedReadout R (s + t) x := by
  unfold connectedReadoutTwoStep connectedReadout
  rw [D.transport_add s t x]

/-- Two-step connected readout obeys the same summed-time exponential gap bound. -/
theorem connected_readout_two_step_decay
    (L : D.LinearTransferRealization)
    (R : BoundedReadout State)
    (s t : NNReal) (x : State)
    (hx : L.CenteredExcitation x) :
    |L.connectedReadoutTwoStep R s t x| ≤
      R.amplitude * D.decayFactor (s + t) * ‖L.centeredState x‖ := by
  rw [L.connectedReadoutTwoStep_eq_sum R s t x]
  exact L.connected_readout_decay R (s + t) x hx

/-- The two-step connected bound factors into the product of the two gap factors. -/
theorem connected_readout_two_step_decay_product
    (L : D.LinearTransferRealization)
    (R : BoundedReadout State)
    (s t : NNReal) (x : State)
    (hx : L.CenteredExcitation x) :
    |L.connectedReadoutTwoStep R s t x| ≤
      R.amplitude * D.decayFactor s * D.decayFactor t *
        ‖L.centeredState x‖ := by
  have h := L.connected_readout_two_step_decay R s t x hx
  rw [D.decayFactor_add s t] at h
  simpa [mul_assoc] using h

end LinearTransferRealization

end ExponentiallyGappedVacuumTransport

end KUOS.DependentOriginationLinearTransferConnectedReadoutV0_3
