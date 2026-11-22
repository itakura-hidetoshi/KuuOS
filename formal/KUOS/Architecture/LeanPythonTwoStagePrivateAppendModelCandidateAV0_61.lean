import Mathlib
import KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60
import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-!
# v0.61 — two-stage private append of tagged observation gluing

The v0.60 proof is composed through two exact branch-private append stages.
Both AppendObservationRecord hypotheses retain all old shared/private values.
The intermediate observation maps are explicitly equal. Neither bare
checkpoint equality nor an asserted append event supplies those hypotheses.

These theorems do not establish independently issued historical data,
a single linear history, global descent, or original PlanOS authority.
This is a MODEL-SUPPLIED candidate, submitted through CodeAI and requiring
independent actual pinned Lean certification.
-/

namespace KUOS.Architecture.LeanPythonTwoStagePrivateAppendV0_61

open KUOS.Architecture.LeanPythonTaggedPrivateAppendInvarianceV0_60
open KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59
open KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58
open KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53
open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

universe u

/-- Successive private append operations have the expected concatenated
result, without identifying the branch tags or modifying the ancestor. -/
theorem private_append_two_stage_assoc
    (s : BranchPositionSpan)
    (l₁ r₁ l₂ r₂ : List LocalReplayTicket) :
    appendPrivate (appendPrivate s l₁ r₁) l₂ r₂ =
      appendPrivate s (l₁ ++ l₂) (r₁ ++ r₂) := by
  cases s with
  | mk shared leftExtra rightExtra =>
      simp [appendPrivate, List.append_assoc]

/-- Exact preservation of both intermediate observation maps makes
two-stage compatibility equivalent to the original compatibility. -/
theorem two_stage_overlap_compatibility_iff
    {s : BranchPositionSpan}
    {l₁ r₁ l₂ r₂ : List LocalReplayTicket}
    {X : Type u}
    (first : AppendObservationRecord s l₁ r₁ X)
    (second : AppendObservationRecord (appendPrivate s l₁ r₁) l₂ r₂ X)
    (hL : second.oldLeft = first.newerLeft)
    (hR : second.oldRight = first.newerRight) :
    overlapCompatible
      (appendPrivate (appendPrivate s l₁ r₁) l₂ r₂)
      second.newerLeft second.newerRight ↔
    overlapCompatible s first.oldLeft first.oldRight := by
  calc
    overlapCompatible
        (appendPrivate (appendPrivate s l₁ r₁) l₂ r₂)
        second.newerLeft second.newerRight
      ↔ overlapCompatible (appendPrivate s l₁ r₁)
          second.oldLeft second.oldRight :=
        overlap_compatible_after_private_append_iff second
    _ ↔ overlapCompatible (appendPrivate s l₁ r₁)
          first.newerLeft first.newerRight := by rw [hL, hR]
    _ ↔ overlapCompatible s first.oldLeft first.oldRight :=
        overlap_compatible_after_private_append_iff first

theorem two_stage_obstruction_persists
    {s : BranchPositionSpan}
    {l₁ r₁ l₂ r₂ : List LocalReplayTicket}
    {X : Type u}
    (first : AppendObservationRecord s l₁ r₁ X)
    (second : AppendObservationRecord (appendPrivate s l₁ r₁) l₂ r₂ X)
    (hL : second.oldLeft = first.newerLeft)
    (hR : second.oldRight = first.newerRight)
    (h : ¬ overlapCompatible s first.oldLeft first.oldRight) :
    ¬ overlapCompatible
      (appendPrivate (appendPrivate s l₁ r₁) l₂ r₂)
      second.newerLeft second.newerRight := by
  intro later
  exact h ((two_stage_overlap_compatibility_iff first second hL hR).mp later)

/-- v0.59 tagged set-level gluing exists after two private append stages
exactly when it existed before both stages. -/
theorem two_stage_tagged_gluing_iff
    {s : BranchPositionSpan}
    {l₁ r₁ l₂ r₂ : List LocalReplayTicket}
    {X : Type u}
    (first : AppendObservationRecord s l₁ r₁ X)
    (second : AppendObservationRecord (appendPrivate s l₁ r₁) l₂ r₂ X)
    (hL : second.oldLeft = first.newerLeft)
    (hR : second.oldRight = first.newerRight) :
    (∃ g : TaggedPosition (appendPrivate (appendPrivate s l₁ r₁) l₂ r₂) → X,
      (∀ i, g (leftInclusion (appendPrivate (appendPrivate s l₁ r₁) l₂ r₂) i) =
        second.newerLeft i) ∧
      (∀ i, g (rightInclusion (appendPrivate (appendPrivate s l₁ r₁) l₂ r₂) i) =
        second.newerRight i)) ↔
    (∃ g : TaggedPosition s → X,
      (∀ i, g (leftInclusion s i) = first.oldLeft i) ∧
      (∀ i, g (rightInclusion s i) = first.oldRight i)) := by
  have hsecond := tagged_gluing_existence_after_private_append_iff second
  have hfirst := tagged_gluing_existence_after_private_append_iff first
  rw [hL, hR] at hsecond
  exact hsecond.trans hfirst

theorem two_stage_tagged_gluing_obstruction
    {s : BranchPositionSpan}
    {l₁ r₁ l₂ r₂ : List LocalReplayTicket}
    {X : Type u}
    (first : AppendObservationRecord s l₁ r₁ X)
    (second : AppendObservationRecord (appendPrivate s l₁ r₁) l₂ r₂ X)
    (hL : second.oldLeft = first.newerLeft)
    (hR : second.oldRight = first.newerRight)
    (h : ¬ ∃ g : TaggedPosition s → X,
      (∀ i, g (leftInclusion s i) = first.oldLeft i) ∧
      (∀ i, g (rightInclusion s i) = first.oldRight i)) :
    ¬ ∃ g : TaggedPosition (appendPrivate (appendPrivate s l₁ r₁) l₂ r₂) → X,
      (∀ i, g (leftInclusion (appendPrivate (appendPrivate s l₁ r₁) l₂ r₂) i) =
        second.newerLeft i) ∧
      (∀ i, g (rightInclusion (appendPrivate (appendPrivate s l₁ r₁) l₂ r₂) i) =
        second.newerRight i) := by
  intro later
  exact h ((two_stage_tagged_gluing_iff first second hL hR).mp later)

/-- Old left private labels also survive both stages, at their transported
positions. No new chronological validity is implied by the equality. -/
theorem two_stage_old_left_private_observation
    {s : BranchPositionSpan}
    {l₁ r₁ l₂ r₂ : List LocalReplayTicket}
    {X : Type u}
    (first : AppendObservationRecord s l₁ r₁ X)
    (second : AppendObservationRecord (appendPrivate s l₁ r₁) l₂ r₂ X)
    (hL : second.oldLeft = first.newerLeft)
    (i : Fin s.leftExtra.length) :
    second.newerLeft
        (.inr (oldLeftIndex (appendPrivate s l₁ r₁) l₂ r₂
          (oldLeftIndex s l₁ r₁ i))) = first.oldLeft (.inr i) := by
  calc
    _ = second.oldLeft (.inr (oldLeftIndex s l₁ r₁ i)) :=
      second.leftPrivateKept _
    _ = first.newerLeft (.inr (oldLeftIndex s l₁ r₁ i)) := by rw [hL]
    _ = first.oldLeft (.inr i) := first.leftPrivateKept i

theorem two_stage_old_right_private_observation
    {s : BranchPositionSpan}
    {l₁ r₁ l₂ r₂ : List LocalReplayTicket}
    {X : Type u}
    (first : AppendObservationRecord s l₁ r₁ X)
    (second : AppendObservationRecord (appendPrivate s l₁ r₁) l₂ r₂ X)
    (hR : second.oldRight = first.newerRight)
    (i : Fin s.rightExtra.length) :
    second.newerRight
        (.inr (oldRightIndex (appendPrivate s l₁ r₁) l₂ r₂
          (oldRightIndex s l₁ r₁ i))) = first.oldRight (.inr i) := by
  calc
    _ = second.oldRight (.inr (oldRightIndex s l₁ r₁ i)) :=
      second.rightPrivateKept _
    _ = first.newerRight (.inr (oldRightIndex s l₁ r₁ i)) := by rw [hR]
    _ = first.oldRight (.inr i) := first.rightPrivateKept i

/-- Neither an external model candidate nor two-stage proof existence grants
original PlanOS host execution or unilateral selection authority. -/
theorem two_stage_proof_grants_no_original_execution
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (valid : MiddleWayBoundedSynthesisIntakeCertificateValid p)
    {s : BranchPositionSpan}
    {l₁ r₁ l₂ r₂ : List LocalReplayTicket}
    (_first : AppendObservationRecord s l₁ r₁ String)
    (_second : AppendObservationRecord (appendPrivate s l₁ r₁) l₂ r₂ String) :
    p.executionPermission = false ∧
    p.executionAuthorityGranted = false ∧
    p.selectionAuthorityGrantedToPlanOS = false := by
  exact ⟨valid.execution_permission_false,
    valid.execution_authority_not_granted,
    valid.selection_authority_not_granted⟩

end KUOS.Architecture.LeanPythonTwoStagePrivateAppendV0_61

#print axioms KUOS.Architecture.LeanPythonTwoStagePrivateAppendV0_61.private_append_two_stage_assoc
#print axioms KUOS.Architecture.LeanPythonTwoStagePrivateAppendV0_61.two_stage_overlap_compatibility_iff
#print axioms KUOS.Architecture.LeanPythonTwoStagePrivateAppendV0_61.two_stage_obstruction_persists
#print axioms KUOS.Architecture.LeanPythonTwoStagePrivateAppendV0_61.two_stage_tagged_gluing_iff
#print axioms KUOS.Architecture.LeanPythonTwoStagePrivateAppendV0_61.two_stage_tagged_gluing_obstruction
#print axioms KUOS.Architecture.LeanPythonTwoStagePrivateAppendV0_61.two_stage_old_left_private_observation
#print axioms KUOS.Architecture.LeanPythonTwoStagePrivateAppendV0_61.two_stage_old_right_private_observation
#print axioms KUOS.Architecture.LeanPythonTwoStagePrivateAppendV0_61.two_stage_proof_grants_no_original_execution
