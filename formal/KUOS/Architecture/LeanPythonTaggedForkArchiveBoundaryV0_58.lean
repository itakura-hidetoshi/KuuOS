import Mathlib
import KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57
import KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56
import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-!
# v0.58: a tagged fork-preserving archive, NOT a linear gluing theorem

v0.57 proves that two locally incomparable histories cannot both be exact
prefixes of a *single* append-only List. Here the representation is
enlarged: it explicitly stores one common ancestor and TWO tagged branches.
Both branch projections preserve their original declared histories.

Existence of this data structure is not a descent theorem for a single
linear history, a proof of external provenance, a signature/cryptography
theorem, or a grant of original PlanOS host action authority. Interpreting
the tags as historical actors or causality is outside the Lean proof.
-/

namespace KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58

open KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56
open KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57
open KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54
open KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53
open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-- A LOCAL tagged representation preserving both declared descendants. -/
structure TaggedForkArchive where
  ancestor : DetachedReplayWitness
  left : DetachedReplayWitness
  right : DetachedReplayWitness
  leftExtends : declaredExtension ancestor left
  rightExtends : declaredExtension ancestor right

/-- Tags are presentation choices, not authenticated issuers. -/
def branchProjection (a : TaggedForkArchive) (tag : Bool) :
    DetachedReplayWitness :=
  match tag with
  | true => a.left
  | false => a.right

/-- A declared fork is sufficient to construct this *branched* archive. -/
def archiveDeclaredFork
    (ancestor left right : DetachedReplayWitness)
    (h : declaredForkObstruction ancestor left right) : TaggedForkArchive where
  ancestor := ancestor
  left := left
  right := right
  leftExtends := h.1
  rightExtends := h.2.1

theorem left_branch_projection_exact (a : TaggedForkArchive) :
    branchProjection a true = a.left := by
  rfl

theorem right_branch_projection_exact (a : TaggedForkArchive) :
    branchProjection a false = a.right := by
  rfl

theorem either_branch_extends_ancestor
    (a : TaggedForkArchive) (tag : Bool) :
    declaredExtension a.ancestor (branchProjection a tag) := by
  cases tag with
  | false => exact a.rightExtends
  | true => exact a.leftExtends

theorem prior_ticket_retained_in_both_branches
    (a : TaggedForkArchive) (ticket : LocalReplayTicket)
    (h : ticket ∈ a.ancestor.observedTickets) :
    ticket ∈ (branchProjection a true).observedTickets ∧
    ticket ∈ (branchProjection a false).observedTickets := by
  change ticket ∈ a.left.observedTickets ∧
    ticket ∈ a.right.observedTickets
  rcases a.leftExtends with ⟨leftExtra, hl⟩
  rcases a.rightExtends with ⟨rightExtra, hr⟩
  constructor
  · rw [hl]
    exact List.mem_append.mpr (Or.inl h)
  · rw [hr]
    exact List.mem_append.mpr (Or.inl h)

theorem archive_of_fork_has_exact_projections
    (ancestor left right : DetachedReplayWitness)
    (h : declaredForkObstruction ancestor left right) :
    (archiveDeclaredFork ancestor left right h).ancestor = ancestor ∧
    branchProjection (archiveDeclaredFork ancestor left right h) true = left ∧
    branchProjection (archiveDeclaredFork ancestor left right h) false = right := by
  exact ⟨rfl, rfl, rfl⟩

theorem archive_of_fork_preserves_incomparability
    (ancestor left right : DetachedReplayWitness)
    (h : declaredForkObstruction ancestor left right) :
    ¬ locallyComparable
      (branchProjection (archiveDeclaredFork ancestor left right h) true)
      (branchProjection (archiveDeclaredFork ancestor left right h) false) := by
  exact h.2.2

theorem archived_fork_still_has_no_common_linear_successor
    (ancestor left right : DetachedReplayWitness)
    (h : declaredForkObstruction ancestor left right) :
    ¬ hasDeclaredCommonLinearSuccessor
      (branchProjection (archiveDeclaredFork ancestor left right h) true)
      (branchProjection (archiveDeclaredFork ancestor left right h) false) := by
  exact declared_fork_blocks_linear_gluing ancestor left right h

/-- The branched archive exists even when a linear common future is blocked.
This is a change of representation, not proof of a forbidden linear descent. -/
theorem fork_can_be_archived_without_linear_gluing
    (ancestor left right : DetachedReplayWitness)
    (h : declaredForkObstruction ancestor left right) :
    (∃ a : TaggedForkArchive,
      a.ancestor = ancestor ∧ a.left = left ∧ a.right = right) ∧
    ¬ hasDeclaredCommonLinearSuccessor left right := by
  constructor
  · refine ⟨archiveDeclaredFork ancestor left right h, ?_, ?_, ?_⟩
    all_goals rfl
  · exact declared_fork_blocks_linear_gluing ancestor left right h

theorem tagged_archive_does_not_grant_original_execution
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (valid : MiddleWayBoundedSynthesisIntakeCertificateValid p)
    (_a : TaggedForkArchive) :
    p.executionPermission = false ∧
    p.executionAuthorityGranted = false ∧
    p.selectionAuthorityGrantedToPlanOS = false := by
  exact ⟨valid.execution_permission_false,
    valid.execution_authority_not_granted,
    valid.selection_authority_not_granted⟩

end KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58

#print axioms KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58.branchProjection
#print axioms KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58.archiveDeclaredFork
#print axioms KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58.left_branch_projection_exact
#print axioms KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58.right_branch_projection_exact
#print axioms KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58.either_branch_extends_ancestor
#print axioms KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58.prior_ticket_retained_in_both_branches
#print axioms KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58.archive_of_fork_has_exact_projections
#print axioms KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58.archive_of_fork_preserves_incomparability
#print axioms KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58.archived_fork_still_has_no_common_linear_successor
#print axioms KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58.fork_can_be_archived_without_linear_gluing
#print axioms KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58.tagged_archive_does_not_grant_original_execution
