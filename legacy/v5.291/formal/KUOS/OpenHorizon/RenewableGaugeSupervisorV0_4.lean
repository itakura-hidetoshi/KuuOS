import Mathlib

/-!
A small formal surface for renewable supervision.
Each invocation is locally bounded, while repeated renewal can pass every finite
bound on the generation index.
-/

namespace KUOS
namespace OpenHorizon

structure SupervisorState where
  generation : ℕ
  cycle : ℕ

structure LocalInvocation where
  interventionCount : ℕ
  interventionBound : interventionCount ≤ 1

def renew (s : SupervisorState) : SupervisorState where
  generation := s.generation + 1
  cycle := s.cycle + 1

theorem renew_generation_strict (s : SupervisorState) :
    s.generation < (renew s).generation := by
  simp [renew]

theorem renew_cycle_strict (s : SupervisorState) :
    s.cycle < (renew s).cycle := by
  simp [renew]

theorem iterate_renew_generation (s : SupervisorState) (n : ℕ) :
    (Function.iterate renew n s).generation = s.generation + n := by
  induction n with
  | zero => simp
  | succ n ih =>
      simp [Function.iterate_succ_apply, ih, renew, Nat.add_assoc]

theorem iterate_renew_cycle (s : SupervisorState) (n : ℕ) :
    (Function.iterate renew n s).cycle = s.cycle + n := by
  induction n with
  | zero => simp
  | succ n ih =>
      simp [Function.iterate_succ_apply, ih, renew, Nat.add_assoc]

theorem arbitrarily_many_renewals (s : SupervisorState) (bound : ℕ) :
    ∃ n : ℕ, bound < (Function.iterate renew n s).generation := by
  refine ⟨bound + 1, ?_⟩
  rw [iterate_renew_generation]
  omega

theorem local_invocation_at_most_one_intervention (i : LocalInvocation) :
    i.interventionCount = 0 ∨ i.interventionCount = 1 := by
  omega

end OpenHorizon
end KUOS
