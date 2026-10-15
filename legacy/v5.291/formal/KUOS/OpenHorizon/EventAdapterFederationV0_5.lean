import Mathlib

/-!
A finite formal surface for event-source fan-in and single-adapter selection.
The runtime may assimilate many source events in one cycle, but it selects at most
one adapter for the delegated local intervention.
-/

namespace KUOS
namespace OpenHorizon

structure AdapterSelection where
  selectedAdapterCount : ℕ
  uniqueSelection : selectedAdapterCount ≤ 1

theorem selectedAdapterCount_le_one (selection : AdapterSelection) :
    selection.selectedAdapterCount ≤ 1 :=
  selection.uniqueSelection

theorem selectedAdapterCount_eq_zero_or_one (selection : AdapterSelection) :
    selection.selectedAdapterCount = 0 ∨ selection.selectedAdapterCount = 1 := by
  omega

structure FederationState where
  cycle : ℕ
  sourceEvents : ℕ
  adapterSelections : ℕ

def assimilate (sourceCount : ℕ) (state : FederationState) : FederationState where
  cycle := state.cycle + 1
  sourceEvents := state.sourceEvents + sourceCount
  adapterSelections := state.adapterSelections + 1

theorem assimilate_cycle_strict (sourceCount : ℕ) (state : FederationState) :
    state.cycle < (assimilate sourceCount state).cycle := by
  simp [assimilate]

theorem assimilate_sourceEvents_monotone (sourceCount : ℕ) (state : FederationState) :
    state.sourceEvents ≤ (assimilate sourceCount state).sourceEvents := by
  simp [assimilate]

theorem assimilate_sourceEvents_strict
    (sourceCount : ℕ) (state : FederationState) (h : 0 < sourceCount) :
    state.sourceEvents < (assimilate sourceCount state).sourceEvents := by
  simp [assimilate, h]

theorem iterate_assimilate_sourceEvents
    (sourceCount n : ℕ) (state : FederationState) :
    (Function.iterate (assimilate sourceCount) n state).sourceEvents =
      state.sourceEvents + n * sourceCount := by
  induction n with
  | zero => simp
  | succ n ih =>
      simp [Function.iterate_succ_apply, ih, assimilate, Nat.succ_mul, Nat.add_assoc]

theorem iterate_assimilate_adapterSelections
    (sourceCount n : ℕ) (state : FederationState) :
    (Function.iterate (assimilate sourceCount) n state).adapterSelections =
      state.adapterSelections + n := by
  induction n with
  | zero => simp
  | succ n ih =>
      simp [Function.iterate_succ_apply, ih, assimilate, Nat.add_assoc]

theorem arbitrarily_many_source_events
    (sourceCount : ℕ) (h : 0 < sourceCount) (state : FederationState) (bound : ℕ) :
    ∃ n : ℕ,
      bound < (Function.iterate (assimilate sourceCount) n state).sourceEvents := by
  refine ⟨bound + state.sourceEvents + 1, ?_⟩
  rw [iterate_assimilate_sourceEvents]
  nlinarith

end OpenHorizon
end KUOS
