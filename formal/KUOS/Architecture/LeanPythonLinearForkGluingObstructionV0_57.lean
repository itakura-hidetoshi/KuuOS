import Mathlib
import KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56
import KUOS.Architecture.LeanPythonPriorCheckpointPrefixBoundaryV0_55
import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-!
# v0.57: a fork has no common successor in a SINGLE append-only list

Two declarations can each extend the same old list but be incomparable.
In this *strictly linear* representation, those histories cannot both be
prefixes of one future list. That is a proven obstruction to this specific
kind of gluing; it is NOT a claim that all models of causal/event graphs,
all histories in other contexts, or external histories are inconsistent.

No independent source authentication, actual SQLite/JSON/SHA256 equivalence,
real-world time, global consensus, PlanOS output or host execution follows.
-/

namespace KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57

open KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56
open KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54
open KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53
open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-- Two histories have a declared linear gluing witness if one later list
contains each history as an exact prefix. -/
def hasDeclaredCommonLinearSuccessor
    (left right : DetachedReplayWitness) : Prop :=
  ∃ later : DetachedReplayWitness,
    declaredExtension left later ∧ declaredExtension right later

/-- Pure list cancellation shows prefixes of the same list must be comparable.
This is an elementary list theorem, not a cryptographic axiom. -/
private theorem two_prefixes_of_one_list_are_comparable
    (xs ys restX restY : List LocalReplayTicket)
    (h : xs ++ restX = ys ++ restY) :
    (∃ remainder, ys = xs ++ remainder) ∨
    (∃ remainder, xs = ys ++ remainder) := by
  induction xs generalizing ys with
  | nil =>
      exact Or.inl ⟨ys, by simp⟩
  | cons x xs ih =>
      cases ys with
      | nil =>
          exact Or.inr ⟨x :: xs, by simp⟩
      | cons y ys =>
          have heq : x :: (xs ++ restX) = y :: (ys ++ restY) := by
            simpa using h
          have hxy : x = y := (List.cons.inj heq).1
          have hrest : xs ++ restX = ys ++ restY := (List.cons.inj heq).2
          subst y
          rcases ih ys hrest with hleft | hright
          · rcases hleft with ⟨remaining, hleft⟩
            exact Or.inl ⟨remaining, by simpa [hleft]⟩
          · rcases hright with ⟨remaining, hright⟩
            exact Or.inr ⟨remaining, by simpa [hright]⟩

theorem common_linear_successor_implies_comparability
    (left right : DetachedReplayWitness)
    (h : hasDeclaredCommonLinearSuccessor left right) :
    locallyComparable left right := by
  rcases h with ⟨later, ⟨leftTail, hleft⟩, ⟨rightTail, hright⟩⟩
  have hboth :
      left.observedTickets ++ leftTail =
        right.observedTickets ++ rightTail :=
    hleft.symm.trans hright
  rcases two_prefixes_of_one_list_are_comparable
      left.observedTickets right.observedTickets
      leftTail rightTail hboth with h | h
  · exact Or.inl h
  · exact Or.inr h

theorem incomparable_histories_have_no_common_linear_successor
    (left right : DetachedReplayWitness)
    (h : ¬ locallyComparable left right) :
    ¬ hasDeclaredCommonLinearSuccessor left right := by
  intro common
  exact h (common_linear_successor_implies_comparability left right common)

/-- This is a bounded non-gluing theorem for one append-only list model.
It says nothing about reconciliation in an explicitly richer data model. -/
theorem declared_fork_blocks_linear_gluing
    (ancestor left right : DetachedReplayWitness)
    (h : declaredForkObstruction ancestor left right) :
    ¬ hasDeclaredCommonLinearSuccessor left right := by
  exact incomparable_histories_have_no_common_linear_successor
    left right h.2.2

theorem declared_fork_excludes_two_extension_witnesses
    (ancestor left right future : DetachedReplayWitness)
    (h : declaredForkObstruction ancestor left right) :
    ¬ (declaredExtension left future ∧ declaredExtension right future) := by
  intro both
  exact declared_fork_blocks_linear_gluing ancestor left right h
    ⟨future, both⟩

theorem common_successor_excludes_declared_fork
    (ancestor left right : DetachedReplayWitness)
    (h : hasDeclaredCommonLinearSuccessor left right) :
    ¬ declaredForkObstruction ancestor left right := by
  intro fork
  exact (declared_fork_blocks_linear_gluing ancestor left right fork) h

theorem comparable_left_has_declared_common_successor
    (left right : DetachedReplayWitness)
    (h : declaredExtension left right) :
    hasDeclaredCommonLinearSuccessor left right := by
  refine ⟨right, h, ?_⟩
  exact declared_extension_reflexive right

theorem comparable_right_has_declared_common_successor
    (left right : DetachedReplayWitness)
    (h : declaredExtension right left) :
    hasDeclaredCommonLinearSuccessor left right := by
  refine ⟨left, ?_, h⟩
  exact declared_extension_reflexive left

theorem comparable_histories_have_declared_common_successor
    (left right : DetachedReplayWitness)
    (h : locallyComparable left right) :
    hasDeclaredCommonLinearSuccessor left right := by
  rcases h with h | h
  · exact comparable_left_has_declared_common_successor left right h
  · exact comparable_right_has_declared_common_successor left right h

theorem common_successor_iff_comparable
    (left right : DetachedReplayWitness) :
    hasDeclaredCommonLinearSuccessor left right ↔
      locallyComparable left right := by
  constructor
  · exact common_linear_successor_implies_comparability left right
  · exact comparable_histories_have_declared_common_successor left right

/-- Preference over two branches cannot turn an incomparable fork into a
certified common append-only history. -/
theorem preference_cannot_resolve_linear_fork
    (ancestor left right : DetachedReplayWitness)
    (h : declaredForkObstruction ancestor left right)
    (_preferred : Bool) :
    ¬ hasDeclaredCommonLinearSuccessor left right := by
  exact declared_fork_blocks_linear_gluing ancestor left right h

/-- A locally possible or impossible prefix relation cannot license the
original PlanOS to select, execute or claim external authority. -/
theorem linear_gluing_check_grants_no_original_execution
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (valid : MiddleWayBoundedSynthesisIntakeCertificateValid p)
    (left right : DetachedReplayWitness)
    (_gluable : hasDeclaredCommonLinearSuccessor left right) :
    p.executionPermission = false ∧
    p.executionAuthorityGranted = false ∧
    p.selectionAuthorityGrantedToPlanOS = false := by
  exact ⟨valid.execution_permission_false,
    valid.execution_authority_not_granted,
    valid.selection_authority_not_granted⟩

end KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57

#print axioms KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57.hasDeclaredCommonLinearSuccessor
#print axioms KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57.common_linear_successor_implies_comparability
#print axioms KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57.incomparable_histories_have_no_common_linear_successor
#print axioms KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57.declared_fork_blocks_linear_gluing
#print axioms KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57.declared_fork_excludes_two_extension_witnesses
#print axioms KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57.common_successor_excludes_declared_fork
#print axioms KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57.comparable_left_has_declared_common_successor
#print axioms KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57.comparable_right_has_declared_common_successor
#print axioms KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57.comparable_histories_have_declared_common_successor
#print axioms KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57.common_successor_iff_comparable
#print axioms KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57.preference_cannot_resolve_linear_fork
#print axioms KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57.linear_gluing_check_grants_no_original_execution
