import Mathlib
import KUOS.DependentOriginationFiniteTransferWordV0_4

namespace KUOS.DependentOriginationHistorySensitiveTransportV0_5

open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationExponentialGapTransportV0_2
open KUOS.DependentOriginationLinearTransferConnectedReadoutV0_3
open KUOS.DependentOriginationFiniteTransferWordV0_4

universe u v w

/--
History-sensitive dependent-origination transport.

The free finite word is primary: its denotation is not defined through any
summary such as total elapsed time.  The only laws required here are the empty
history law and compositionality under word concatenation.

Thus this structure can host genuinely history-sensitive / non-Markov
semantics, while ordinary one-parameter semigroups arise by an additional
factorization theorem rather than by definition.
-/
structure HistoryTransport (Event : Type u) (State : Type v) where
  eval : List Event → State → State
  eval_nil : ∀ x : State, eval [] x = x
  eval_append : ∀ (left right : List Event) (x : State),
    eval (left ++ right) x = eval left (eval right x)

namespace HistoryTransport

variable {Event : Type u} {State : Type v}

/-- The empty history acts as the identity. -/
@[simp] theorem eval_nil_apply
    (H : HistoryTransport Event State) (x : State) :
    H.eval [] x = x :=
  H.eval_nil x

/-- Concatenation is composition of history transports. -/
theorem eval_append_apply
    (H : HistoryTransport Event State)
    (left right : List Event) (x : State) :
    H.eval (left ++ right) x = H.eval left (H.eval right x) :=
  H.eval_append left right x

/-- Two finite histories are semantically distinguished when they differ on some state. -/
def Distinguishes
    (H : HistoryTransport Event State)
    (left right : List Event) : Prop :=
  ∃ x : State, H.eval left x ≠ H.eval right x

/-- Distinguishability is symmetric. -/
theorem distinguishes_symm
    (H : HistoryTransport Event State)
    {left right : List Event}
    (h : H.Distinguishes left right) :
    H.Distinguishes right left := by
  rcases h with ⟨x, hx⟩
  exact ⟨x, ne_comm.mp hx⟩

end HistoryTransport

/--
An additional certificate saying that a history transport factors through the
sum of its letters and an additive one-parameter transport.

This is the precise Markov/semigroup specialization boundary.  It is not a
field of `HistoryTransport` itself.
-/
structure TotalTimeFactorization
    {Time : Type u} [AddMonoid Time]
    {State : Type v}
    (H : HistoryTransport Time State) where
  semigroup : AdditiveEndoTransport Time State
  eval_eq_totalTime : ∀ (word : List Time) (x : State),
    H.eval word x = semigroup.transport word.sum x

namespace TotalTimeFactorization

variable {Time : Type u} [AddMonoid Time]
variable {State : Type v}
variable {H : HistoryTransport Time State}

/-- Equal-total-time histories have equal state denotation whenever factorization holds. -/
theorem eval_eq_of_sum_eq
    (F : TotalTimeFactorization H)
    (left right : List Time) (x : State)
    (hSum : left.sum = right.sum) :
    H.eval left x = H.eval right x := by
  calc
    H.eval left x = F.semigroup.transport left.sum x :=
      F.eval_eq_totalTime left x
    _ = F.semigroup.transport right.sum x := by rw [hSum]
    _ = H.eval right x :=
      (F.eval_eq_totalTime right x).symm

/-- Every ordinary readout is also equal on equal-total-time histories. -/
theorem readout_eq_of_sum_eq
    (F : TotalTimeFactorization H)
    {Output : Type w}
    (readout : State → Output)
    (left right : List Time) (x : State)
    (hSum : left.sum = right.sum) :
    readout (H.eval left x) = readout (H.eval right x) := by
  exact congrArg readout (F.eval_eq_of_sum_eq left right x hSum)

end TotalTimeFactorization

namespace HistoryTransport

variable {Time : Type u} [AddMonoid Time]
variable {State : Type v}

/--
Genuine history sensitivity relative to total time: two histories with the same
sum have different denotation on at least one state.
-/
def GenuinelyHistorySensitive
    (H : HistoryTransport Time State) : Prop :=
  ∃ left right : List Time,
    left.sum = right.sum ∧ H.Distinguishes left right

/-- A total-time factorization rules out genuine history sensitivity. -/
theorem not_genuinelyHistorySensitive_of_factorization
    (H : HistoryTransport Time State)
    (F : TotalTimeFactorization H) :
    ¬ H.GenuinelyHistorySensitive := by
  intro h
  rcases h with ⟨left, right, hSum, hDist⟩
  rcases hDist with ⟨x, hne⟩
  exact hne (F.eval_eq_of_sum_eq left right x hSum)

end HistoryTransport

/-!
## The v0.4 finite transfer word as the factorizable specialization

The existing linear positive-time transfer word is embedded into the new parent
history structure.  Its total-time collapse is then re-expressed as an explicit
`TotalTimeFactorization` certificate.
-/

namespace ExponentiallyGappedVacuumTransport

variable {State : Type u} [SeminormedAddCommGroup State] [NormedSpace ℝ State]

namespace LinearTransferRealization

variable {D : ExponentiallyGappedVacuumTransport State}

/-- The v0.4 finite transfer-word evaluator is a compositional history transport. -/
def toHistoryTransport
    (L : KUOS.DependentOriginationLinearTransferConnectedReadoutV0_3.ExponentiallyGappedVacuumTransport.LinearTransferRealization D) :
    HistoryTransport NNReal State where
  eval := L.wordOperatorApply
  eval_nil := fun x => L.wordOperatorApply_nil x
  eval_append := fun left right x => L.wordOperatorApply_append left right x

/--
The current positive-time semigroup supplies an explicit total-time
factorization of the finite history semantics.
-/
def toTotalTimeFactorization
    (L : KUOS.DependentOriginationLinearTransferConnectedReadoutV0_3.ExponentiallyGappedVacuumTransport.LinearTransferRealization D) :
    TotalTimeFactorization L.toHistoryTransport where
  semigroup := {
    transport := D.transport
    transport_zero := D.transport_zero
    transport_add := D.transport_add
  }
  eval_eq_totalTime := by
    intro word x
    simpa [toHistoryTransport, wordTotalTime] using
      L.wordOperatorApply_eq_totalTime word x

/-- Consequently, the current semigroup specialization is not genuinely history-sensitive. -/
theorem semigroup_not_genuinely_history_sensitive
    (L : KUOS.DependentOriginationLinearTransferConnectedReadoutV0_3.ExponentiallyGappedVacuumTransport.LinearTransferRealization D) :
    ¬ L.toHistoryTransport.GenuinelyHistorySensitive := by
  exact L.toHistoryTransport.not_genuinelyHistorySensitive_of_factorization
    L.toTotalTimeFactorization

/-- Equal-total-time finite words also have equal arbitrary readouts in the semigroup specialization. -/
theorem semigroup_readout_eq_of_totalTime_eq
    (L : KUOS.DependentOriginationLinearTransferConnectedReadoutV0_3.ExponentiallyGappedVacuumTransport.LinearTransferRealization D)
    {Output : Type w}
    (readout : State → Output)
    (left right : List NNReal) (x : State)
    (hSum : left.sum = right.sum) :
    readout (L.toHistoryTransport.eval left x) =
      readout (L.toHistoryTransport.eval right x) := by
  exact L.toTotalTimeFactorization.readout_eq_of_sum_eq
    readout left right x hSum

end LinearTransferRealization

end ExponentiallyGappedVacuumTransport

end KUOS.DependentOriginationHistorySensitiveTransportV0_5
