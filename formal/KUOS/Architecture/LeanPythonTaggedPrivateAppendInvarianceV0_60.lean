import Mathlib
import KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59
import KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58
import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-!
# v0.60 — private append, overlap invariance and retained obstruction

The v0.59 tagged positional span is enlarged ONLY by appending private
left/right tickets. The old common positions, their observations, and
all old private observations are explicitly preserved as hypotheses.
This proves equivalence of the old and extended shared-ancestor compatibility
conditions, gluing existence, and persistence of any shared mismatch.

These are conditional typed facts, NOT verification that an arbitrary
detached manifest was appended in the real world, and NOT a single linear
history gluing, actual external authentication, universal Lean↔Python
refinement, or permission for an original PlanOS action.
-/

namespace KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60

open KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59
open KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58
open KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56
open KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57
open KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54
open KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53
open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

universe u

/-- Only left/right PRIVATE tickets extend; the shared ancestor is untouched. -/
def appendPrivate (s : BranchPositionSpan)
    (newLeft newRight : List LocalReplayTicket) : BranchPositionSpan where
  shared := s.shared
  leftExtra := s.leftExtra ++ newLeft
  rightExtra := s.rightExtra ++ newRight

/-- Transport an old left suffix index into the append-extended left suffix. -/
def oldLeftIndex (s : BranchPositionSpan)
    (newLeft newRight : List LocalReplayTicket)
    (i : Fin s.leftExtra.length) :
    Fin (appendPrivate s newLeft newRight).leftExtra.length := by
  refine ⟨i.val, ?_⟩
  simp only [appendPrivate, List.length_append]
  omega

/-- Transport an old right suffix index into the append-extended right suffix. -/
def oldRightIndex (s : BranchPositionSpan)
    (newLeft newRight : List LocalReplayTicket)
    (i : Fin s.rightExtra.length) :
    Fin (appendPrivate s newLeft newRight).rightExtra.length := by
  refine ⟨i.val, ?_⟩
  simp only [appendPrivate, List.length_append]
  omega

/-- Old and new observation maps, with preservation specified for shared
ancestor positions and EACH old private position. These assumptions do not
follow from mere timestamps, hashes, or a claimed append operation. -/
structure AppendObservationRecord (s : BranchPositionSpan)
    (newLeft newRight : List LocalReplayTicket) (X : Type u) where
  oldLeft : LeftPosition s → X
  oldRight : RightPosition s → X
  newerLeft : LeftPosition (appendPrivate s newLeft newRight) → X
  newerRight : RightPosition (appendPrivate s newLeft newRight) → X
  leftSharedKept :
    ∀ i : Fin s.shared.length, newerLeft (.inl i) = oldLeft (.inl i)
  rightSharedKept :
    ∀ i : Fin s.shared.length, newerRight (.inl i) = oldRight (.inl i)
  leftPrivateKept :
    ∀ i : Fin s.leftExtra.length,
      newerLeft (.inr (oldLeftIndex s newLeft newRight i)) =
        oldLeft (.inr i)
  rightPrivateKept :
    ∀ i : Fin s.rightExtra.length,
      newerRight (.inr (oldRightIndex s newLeft newRight i)) =
        oldRight (.inr i)

theorem shared_positions_unchanged (s : BranchPositionSpan)
    (newLeft newRight : List LocalReplayTicket) :
    (appendPrivate s newLeft newRight).shared = s.shared := by
  rfl

theorem left_history_has_exact_append (s : BranchPositionSpan)
    (newLeft newRight : List LocalReplayTicket) :
    (appendPrivate s newLeft newRight).shared ++
        (appendPrivate s newLeft newRight).leftExtra =
      (s.shared ++ s.leftExtra) ++ newLeft := by
  simp [appendPrivate, List.append_assoc]

theorem right_history_has_exact_append (s : BranchPositionSpan)
    (newLeft newRight : List LocalReplayTicket) :
    (appendPrivate s newLeft newRight).shared ++
        (appendPrivate s newLeft newRight).rightExtra =
      (s.shared ++ s.rightExtra) ++ newRight := by
  simp [appendPrivate, List.append_assoc]

theorem old_left_private_observations_retained
    {s : BranchPositionSpan} {newLeft newRight : List LocalReplayTicket}
    {X : Type u} (e : AppendObservationRecord s newLeft newRight X)
    (i : Fin s.leftExtra.length) :
    e.newerLeft (.inr (oldLeftIndex s newLeft newRight i)) =
      e.oldLeft (.inr i) := by
  exact e.leftPrivateKept i

theorem old_right_private_observations_retained
    {s : BranchPositionSpan} {newLeft newRight : List LocalReplayTicket}
    {X : Type u} (e : AppendObservationRecord s newLeft newRight X)
    (i : Fin s.rightExtra.length) :
    e.newerRight (.inr (oldRightIndex s newLeft newRight i)) =
      e.oldRight (.inr i) := by
  exact e.rightPrivateKept i

/-- The strong logical invariant: compatibility is REFLECTED as well as
preserved, provided both old common observation maps really are unchanged. -/
theorem overlap_compatible_after_private_append_iff
    {s : BranchPositionSpan} {newLeft newRight : List LocalReplayTicket}
    {X : Type u} (e : AppendObservationRecord s newLeft newRight X) :
    overlapCompatible (appendPrivate s newLeft newRight)
      e.newerLeft e.newerRight ↔
    overlapCompatible s e.oldLeft e.oldRight := by
  constructor
  · intro h i
    calc
      e.oldLeft (.inl i) = e.newerLeft (.inl i) :=
        (e.leftSharedKept i).symm
      _ = e.newerRight (.inl i) := h i
      _ = e.oldRight (.inl i) := e.rightSharedKept i
  · intro h i
    calc
      e.newerLeft (.inl i) = e.oldLeft (.inl i) :=
        e.leftSharedKept i
      _ = e.oldRight (.inl i) := h i
      _ = e.newerRight (.inl i) := (e.rightSharedKept i).symm

theorem compatible_old_observations_remain_compatible
    {s : BranchPositionSpan} {newLeft newRight : List LocalReplayTicket}
    {X : Type u} (e : AppendObservationRecord s newLeft newRight X)
    (h : overlapCompatible s e.oldLeft e.oldRight) :
    overlapCompatible (appendPrivate s newLeft newRight)
      e.newerLeft e.newerRight := by
  exact (overlap_compatible_after_private_append_iff e).mpr h

theorem incompatibility_does_not_disappear_under_private_append
    {s : BranchPositionSpan} {newLeft newRight : List LocalReplayTicket}
    {X : Type u} (e : AppendObservationRecord s newLeft newRight X)
    (h : ¬ overlapCompatible s e.oldLeft e.oldRight) :
    ¬ overlapCompatible (appendPrivate s newLeft newRight)
      e.newerLeft e.newerRight := by
  intro future
  exact h ((overlap_compatible_after_private_append_iff e).mp future)

/-- The genuine v0.59 set-level gluing exists in the enlarged tagged
position space exactly when it existed before the private append. -/
theorem tagged_gluing_existence_after_private_append_iff
    {s : BranchPositionSpan} {newLeft newRight : List LocalReplayTicket}
    {X : Type u} (e : AppendObservationRecord s newLeft newRight X) :
    (∃ g : TaggedPosition (appendPrivate s newLeft newRight) → X,
      (∀ i, g (leftInclusion (appendPrivate s newLeft newRight) i) =
        e.newerLeft i) ∧
      (∀ i, g (rightInclusion (appendPrivate s newLeft newRight) i) =
        e.newerRight i)) ↔
    (∃ g : TaggedPosition s → X,
      (∀ i, g (leftInclusion s i) = e.oldLeft i) ∧
      (∀ i, g (rightInclusion s i) = e.oldRight i)) := by
  exact (tagged_observation_gluing_iff
      (appendPrivate s newLeft newRight) e.newerLeft e.newerRight).trans
    ((overlap_compatible_after_private_append_iff e).trans
      (tagged_observation_gluing_iff s e.oldLeft e.oldRight).symm)

theorem old_tagged_gluing_constructs_new_tagged_gluing
    {s : BranchPositionSpan} {newLeft newRight : List LocalReplayTicket}
    {X : Type u} (e : AppendObservationRecord s newLeft newRight X)
    (h : ∃ g : TaggedPosition s → X,
      (∀ i, g (leftInclusion s i) = e.oldLeft i) ∧
      (∀ i, g (rightInclusion s i) = e.oldRight i)) :
    ∃ g : TaggedPosition (appendPrivate s newLeft newRight) → X,
      (∀ i, g (leftInclusion (appendPrivate s newLeft newRight) i) =
        e.newerLeft i) ∧
      (∀ i, g (rightInclusion (appendPrivate s newLeft newRight) i) =
        e.newerRight i) := by
  exact (tagged_gluing_existence_after_private_append_iff e).mpr h

theorem old_gluing_obstruction_persists_after_private_append
    {s : BranchPositionSpan} {newLeft newRight : List LocalReplayTicket}
    {X : Type u} (e : AppendObservationRecord s newLeft newRight X)
    (h : ¬ ∃ g : TaggedPosition s → X,
      (∀ i, g (leftInclusion s i) = e.oldLeft i) ∧
      (∀ i, g (rightInclusion s i) = e.oldRight i)) :
    ¬ ∃ g : TaggedPosition (appendPrivate s newLeft newRight) → X,
      (∀ i, g (leftInclusion (appendPrivate s newLeft newRight) i) =
        e.newerLeft i) ∧
      (∀ i, g (rightInclusion (appendPrivate s newLeft newRight) i) =
        e.newerRight i) := by
  intro future
  exact h ((tagged_gluing_existence_after_private_append_iff e).mp future)

/-- A concrete mismatch at a shared position cannot be erased by extending
only private branches; its INDEX and contradictory old values remain fixed. -/
theorem old_shared_disagreement_remains_obstruction
    {s : BranchPositionSpan} {newLeft newRight : List LocalReplayTicket}
    {X : Type u} (e : AppendObservationRecord s newLeft newRight X)
    (i : Fin s.shared.length)
    (h : e.oldLeft (.inl i) ≠ e.oldRight (.inl i)) :
    ¬ overlapCompatible (appendPrivate s newLeft newRight)
      e.newerLeft e.newerRight := by
  have hold : ¬ overlapCompatible s e.oldLeft e.oldRight :=
    shared_value_disagreement_obstructs s e.oldLeft e.oldRight i h
  exact incompatibility_does_not_disappear_under_private_append e hold

/-- Newly extended private positions remain tagged and mutually distinct. -/
theorem extended_private_branches_remain_disjoint
    (s : BranchPositionSpan)
    (newLeft newRight : List LocalReplayTicket)
    (i : Fin (appendPrivate s newLeft newRight).leftExtra.length)
    (j : Fin (appendPrivate s newLeft newRight).rightExtra.length) :
    leftInclusion (appendPrivate s newLeft newRight) (.inr i) ≠
      rightInclusion (appendPrivate s newLeft newRight) (.inr j) := by
  exact branch_private_positions_disjoint (appendPrivate s newLeft newRight) i j

/-- Tagged observation gluing does not override the older separate theorem
for a fork's lack of a common single-linear historical successor. -/
theorem prior_linear_fork_obstruction_still_holds
    (ancestor left right : DetachedReplayWitness)
    (h : declaredForkObstruction ancestor left right) :
    ¬ hasDeclaredCommonLinearSuccessor left right := by
  exact declared_fork_blocks_linear_gluing ancestor left right h

theorem append_only_tagged_gluing_does_not_grant_planos_execution
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (valid : MiddleWayBoundedSynthesisIntakeCertificateValid p)
    {s : BranchPositionSpan} {newLeft newRight : List LocalReplayTicket}
    (_e : AppendObservationRecord s newLeft newRight String) :
    p.executionPermission = false ∧
    p.executionAuthorityGranted = false ∧
    p.selectionAuthorityGrantedToPlanOS = false := by
  exact ⟨valid.execution_permission_false,
    valid.execution_authority_not_granted,
    valid.selection_authority_not_granted⟩

end KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60

#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.appendPrivate
#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.oldLeftIndex
#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.oldRightIndex
#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.shared_positions_unchanged
#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.left_history_has_exact_append
#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.right_history_has_exact_append
#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.old_left_private_observations_retained
#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.old_right_private_observations_retained
#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.overlap_compatible_after_private_append_iff
#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.compatible_old_observations_remain_compatible
#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.incompatibility_does_not_disappear_under_private_append
#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.tagged_gluing_existence_after_private_append_iff
#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.old_tagged_gluing_constructs_new_tagged_gluing
#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.old_gluing_obstruction_persists_after_private_append
#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.old_shared_disagreement_remains_obstruction
#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.extended_private_branches_remain_disjoint
#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.prior_linear_fork_obstruction_still_holds
#print axioms KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60.append_only_tagged_gluing_does_not_grant_planos_execution
