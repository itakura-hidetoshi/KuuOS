import Mathlib
import KUOS.Architecture.LeanPythonPriorCheckpointPrefixBoundaryV0_55
import KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54
import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-!
# v0.56: local fork obstructions for two declared descendants of one snapshot

The abstract model uses the real v0.54 detached witness and v0.55 prefix
interfaces without altering any earlier theorem or original PlanOS.
Its histories are caller-declared lists. Different first appended tickets
after a common prefix prevent either history from extending the other.

These are List theorems, NOT authentication of historical issuers,
independent custody, SHA-256, SQLite/CPython refinement, network events,
global causality, or host execution authority.
-/

namespace KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56

open KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53
open KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54
open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-- A declared exact extension, including the empty extension. -/
def declaredExtension (older newer : DetachedReplayWitness) : Prop :=
  ∃ additional : List LocalReplayTicket,
    newer.observedTickets = older.observedTickets ++ additional

/-- Declared linear comparability, not a proof of actual causal ordering. -/
def locallyComparable (left right : DetachedReplayWitness) : Prop :=
  declaredExtension left right ∨ declaredExtension right left

/-- Two locally valid declared descendants can be mutually incomparable. -/
def declaredForkObstruction
    (older left right : DetachedReplayWitness) : Prop :=
  declaredExtension older left ∧
  declaredExtension older right ∧
  ¬ locallyComparable left right

/-- The exact list-cancellation fact, independent of hash security. -/
private theorem append_left_cancel
    (initial xs ys : List LocalReplayTicket)
    (h : initial ++ xs = initial ++ ys) : xs = ys := by
  induction initial with
  | nil => simpa using h
  | cons x rest ih =>
      apply ih
      exact (List.cons.inj h).2

theorem declared_extension_reflexive (w : DetachedReplayWitness) :
    declaredExtension w w := by
  exact ⟨[], by simp⟩

theorem declared_extension_transitive
    (a b c : DetachedReplayWitness)
    (hab : declaredExtension a b)
    (hbc : declaredExtension b c) :
    declaredExtension a c := by
  rcases hab with ⟨ab, hab⟩
  rcases hbc with ⟨bc, hbc⟩
  refine ⟨ab ++ bc, ?_⟩
  calc
    c.observedTickets = b.observedTickets ++ bc := hbc
    _ = (a.observedTickets ++ ab) ++ bc := by rw [hab]
    _ = a.observedTickets ++ (ab ++ bc) := by simp [List.append_assoc]

theorem extension_implies_comparability
    (left right : DetachedReplayWitness)
    (h : declaredExtension left right) :
    locallyComparable left right := by
  exact Or.inl h

/-- If the first new tickets differ, the two descendant paths cannot
be declared extensions of one another, regardless of later suffixes. -/
theorem differing_first_successors_are_incomparable
    (older left right : DetachedReplayWitness)
    (a b : LocalReplayTicket)
    (tailA tailB : List LocalReplayTicket)
    (hl : left.observedTickets =
      older.observedTickets ++ (a :: tailA))
    (hr : right.observedTickets =
      older.observedTickets ++ (b :: tailB))
    (hne : a ≠ b) :
    ¬ locallyComparable left right := by
  intro comparable
  rcases comparable with ⟨more, hmore⟩ | ⟨more, hmore⟩
  · have heq :
        older.observedTickets ++ (b :: tailB) =
          older.observedTickets ++ ((a :: tailA) ++ more) := by
      calc
        _ = right.observedTickets := hr.symm
        _ = left.observedTickets ++ more := hmore
        _ = (older.observedTickets ++ (a :: tailA)) ++ more := by rw [hl]
        _ = _ := by simp [List.append_assoc]
    have ht := append_left_cancel older.observedTickets
      (b :: tailB) ((a :: tailA) ++ more) heq
    have hb : b = a := by
      have hhead := congrArg List.head? ht
      simpa using hhead
    exact hne hb.symm
  · have heq :
        older.observedTickets ++ (a :: tailA) =
          older.observedTickets ++ ((b :: tailB) ++ more) := by
      calc
        _ = left.observedTickets := hl.symm
        _ = right.observedTickets ++ more := hmore
        _ = (older.observedTickets ++ (b :: tailB)) ++ more := by rw [hr]
        _ = _ := by simp [List.append_assoc]
    have ht := append_left_cancel older.observedTickets
      (a :: tailA) ((b :: tailB) ++ more) heq
    have hab : a = b := by
      have hhead := congrArg List.head? ht
      simpa using hhead
    exact hne hab

theorem differing_first_successors_give_fork
    (older left right : DetachedReplayWitness)
    (a b : LocalReplayTicket)
    (tailA tailB : List LocalReplayTicket)
    (hl : left.observedTickets =
      older.observedTickets ++ (a :: tailA))
    (hr : right.observedTickets =
      older.observedTickets ++ (b :: tailB))
    (hne : a ≠ b) :
    declaredForkObstruction older left right := by
  exact ⟨⟨a :: tailA, hl⟩, ⟨b :: tailB, hr⟩,
    differing_first_successors_are_incomparable
      older left right a b tailA tailB hl hr hne⟩

theorem fork_histories_cannot_agree
    (older left right : DetachedReplayWitness)
    (hf : declaredForkObstruction older left right) :
    left.observedTickets ≠ right.observedTickets := by
  rcases hf with ⟨_, _, hnc⟩
  intro heq
  have hc : locallyComparable left right := by
    apply Or.inl
    exact ⟨[], by simpa using heq.symm⟩
  exact hnc hc

theorem fork_retains_each_prior_ticket
    (older left right : DetachedReplayWitness)
    (hf : declaredForkObstruction older left right)
    (t : LocalReplayTicket) (ht : t ∈ older.observedTickets) :
    t ∈ left.observedTickets ∧ t ∈ right.observedTickets := by
  rcases hf with ⟨⟨leftTail, hl⟩, ⟨rightTail, hr⟩, _⟩
  constructor
  · rw [hl]
    exact List.mem_append.mpr (Or.inl ht)
  · rw [hr]
    exact List.mem_append.mpr (Or.inl ht)

/-- Unrelated local fork observations never grant original host authority. -/
theorem local_fork_does_not_grant_planos_execution
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (valid : MiddleWayBoundedSynthesisIntakeCertificateValid p)
    (older left right : DetachedReplayWitness)
    (_fork : declaredForkObstruction older left right) :
    p.executionPermission = false ∧
    p.executionAuthorityGranted = false ∧
    p.selectionAuthorityGrantedToPlanOS = false := by
  exact ⟨valid.execution_permission_false,
    valid.execution_authority_not_granted,
    valid.selection_authority_not_granted⟩

end KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56

#print axioms KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56.declaredExtension
#print axioms KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56.locallyComparable
#print axioms KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56.declaredForkObstruction
#print axioms KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56.declared_extension_reflexive
#print axioms KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56.declared_extension_transitive
#print axioms KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56.extension_implies_comparability
#print axioms KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56.differing_first_successors_are_incomparable
#print axioms KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56.differing_first_successors_give_fork
#print axioms KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56.fork_histories_cannot_agree
#print axioms KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56.fork_retains_each_prior_ticket
#print axioms KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56.local_fork_does_not_grant_planos_execution
