import Mathlib
import KUOS.DependentOriginationFunctorialTransportV0_1

namespace KUOS.DependentOriginationExponentialGapTransportV0_2

open KUOS.DependentOriginationFunctorialTransportV0_1

universe u

/--
A vacuum-fixed positive-time dependent-origination transport carrying an
abstract exponential gap on a distinguished excitation predicate.

This is intentionally weaker than a physical Hamiltonian/spectral-gap package:
`Excitation` is an abstract transport-stable predicate.  A physical
specialization may instantiate it by a vacuum-orthogonal sector, but this file
does not construct such a sector or claim a Yang--Mills mass gap.
-/
structure ExponentiallyGappedVacuumTransport
    (State : Type u) [SeminormedAddCommGroup State]
    extends VacuumContractiveAdditiveEndoTransport NNReal State where
  mass : ℝ
  mass_nonneg : 0 ≤ mass
  Excitation : State → Prop
  excitation_zero : Excitation 0
  excitation_transport : ∀ (t : NNReal) (x : State),
    Excitation x → Excitation (transport t x)
  excitation_decay : ∀ (t : NNReal) (x : State),
    Excitation x →
      ‖transport t x‖ ≤ Real.exp (-(mass * (t : ℝ))) * ‖x‖

namespace ExponentiallyGappedVacuumTransport

variable {State : Type u} [SeminormedAddCommGroup State]

/-- The exponential factor attached to elapsed positive time. -/
noncomputable def decayFactor (D : ExponentiallyGappedVacuumTransport State)
    (t : NNReal) : ℝ :=
  Real.exp (-(D.mass * (t : ℝ)))

/-- The gap factor is strictly positive at every finite positive time. -/
theorem decayFactor_pos
    (D : ExponentiallyGappedVacuumTransport State) (t : NNReal) :
    0 < D.decayFactor t := by
  exact Real.exp_pos _

/-- In particular the gap factor is nonnegative. -/
theorem decayFactor_nonneg
    (D : ExponentiallyGappedVacuumTransport State) (t : NNReal) :
    0 ≤ D.decayFactor t :=
  le_of_lt (D.decayFactor_pos t)

/-- At zero elapsed time the exponential factor is exactly one. -/
@[simp] theorem decayFactor_zero
    (D : ExponentiallyGappedVacuumTransport State) :
    D.decayFactor 0 = 1 := by
  simp [decayFactor]

/-- Exponential gap factors compose multiplicatively under additive time. -/
theorem decayFactor_add
    (D : ExponentiallyGappedVacuumTransport State)
    (s t : NNReal) :
    D.decayFactor (s + t) = D.decayFactor s * D.decayFactor t := by
  rw [decayFactor, decayFactor, decayFactor, NNReal.coe_add, ← Real.exp_add]
  congr 1
  ring

/-- The inherited distinguished vacuum is fixed by every positive-time transport. -/
theorem vacuum_fixed_transport
    (D : ExponentiallyGappedVacuumTransport State) (t : NNReal) :
    D.transport t D.vacuum = D.vacuum :=
  D.vacuum_fixed t

/-- The distinguished excitation predicate is stable under transport. -/
theorem excitation_stable
    (D : ExponentiallyGappedVacuumTransport State)
    (t : NNReal) (x : State) (hx : D.Excitation x) :
    D.Excitation (D.transport t x) :=
  D.excitation_transport t x hx

/-- The defining exponential decay estimate in named-factor form. -/
theorem excitation_norm_decay
    (D : ExponentiallyGappedVacuumTransport State)
    (t : NNReal) (x : State) (hx : D.Excitation x) :
    ‖D.transport t x‖ ≤ D.decayFactor t * ‖x‖ := by
  simpa [decayFactor] using D.excitation_decay t x hx

/--
A bounded scalar readout.  It need not be linear: the only property needed for
transfer-to-observable decay is a uniform norm bound.
-/
structure BoundedReadout (State : Type u) [SeminormedAddCommGroup State] where
  readout : State → ℝ
  amplitude : ℝ
  amplitude_nonneg : 0 ≤ amplitude
  norm_bound : ∀ x : State, |readout x| ≤ amplitude * ‖x‖

/--
Exponential decay of the transported excitation passes directly to every
bounded readout.  This is the abstract KuuOS-side form of the
transfer-operator-to-correlation-decay step.
-/
theorem bounded_readout_decay
    (D : ExponentiallyGappedVacuumTransport State)
    (R : BoundedReadout State)
    (t : NNReal) (x : State) (hx : D.Excitation x) :
    |R.readout (D.transport t x)| ≤
      R.amplitude * D.decayFactor t * ‖x‖ := by
  have hdecay := D.excitation_norm_decay t x hx
  calc
    |R.readout (D.transport t x)| ≤
        R.amplitude * ‖D.transport t x‖ :=
      R.norm_bound (D.transport t x)
    _ ≤ R.amplitude * (D.decayFactor t * ‖x‖) :=
      mul_le_mul_of_nonneg_left hdecay R.amplitude_nonneg
    _ = R.amplitude * D.decayFactor t * ‖x‖ := by
      ring

/--
The same observable decay law is coherent with two successive transports: the
two-step path is exactly the transport at summed time.
-/
theorem bounded_readout_two_step_decay
    (D : ExponentiallyGappedVacuumTransport State)
    (R : BoundedReadout State)
    (s t : NNReal) (x : State) (hx : D.Excitation x) :
    |R.readout (D.transport s (D.transport t x))| ≤
      R.amplitude * D.decayFactor (s + t) * ‖x‖ := by
  rw [← D.transport_add s t x]
  exact D.bounded_readout_decay R (s + t) x hx

/-- Two-step observable decay can equivalently be written as a product of gap factors. -/
theorem bounded_readout_two_step_decay_product
    (D : ExponentiallyGappedVacuumTransport State)
    (R : BoundedReadout State)
    (s t : NNReal) (x : State) (hx : D.Excitation x) :
    |R.readout (D.transport s (D.transport t x))| ≤
      R.amplitude * D.decayFactor s * D.decayFactor t * ‖x‖ := by
  have h := D.bounded_readout_two_step_decay R s t x hx
  rw [D.decayFactor_add s t] at h
  simpa [mul_assoc] using h

end ExponentiallyGappedVacuumTransport

end KUOS.DependentOriginationExponentialGapTransportV0_2
