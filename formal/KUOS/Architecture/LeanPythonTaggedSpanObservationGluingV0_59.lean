import Mathlib
import KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58
import KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57
import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-!
# v0.59 — exact tagged-span gluing for branch-local observations

This constructs the finite, disjoint TAGGED POSITION SPACE underlying the
v0.58 fork archive: common positions are identified ONCE, and private left
and right positions remain distinct even when their values happen to agree.

The precise SET-LEVEL universal mapping property is proved: two functions
on the left/right positional branches have a unique function on the tagged
amalgam IF AND ONLY IF they agree on all ancestor positions.

This is not a CategoryTheory.IsPushout declaration, nor a gluing of two
incomparable lists into a single chronological list. v0.57's obstruction
remains. Tags are not external actor identifiers or issuer signatures.
-/

namespace KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59

open KUOS.Architecture.LeanPythonTaggedForkArchiveBoundaryV0_58
open KUOS.Architecture.LeanPythonCommonAncestorForkBoundaryV0_56
open KUOS.Architecture.LeanPythonLinearForkGluingObstructionV0_57
open KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54
open KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53
open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

universe u

/-- Retain positions, not merely ticket values: duplicate payloads still
occupy distinct slots, and a branch suffix retains its own tag. -/
structure BranchPositionSpan where
  shared : List LocalReplayTicket
  leftExtra : List LocalReplayTicket
  rightExtra : List LocalReplayTicket

abbrev LeftPosition (s : BranchPositionSpan) : Type :=
  Fin s.shared.length ⊕ Fin s.leftExtra.length

abbrev RightPosition (s : BranchPositionSpan) : Type :=
  Fin s.shared.length ⊕ Fin s.rightExtra.length

/-- Three kinds of slots, with ancestor slots represented only once. -/
inductive TaggedPosition (s : BranchPositionSpan) : Type
  | common : Fin s.shared.length → TaggedPosition s
  | left : Fin s.leftExtra.length → TaggedPosition s
  | right : Fin s.rightExtra.length → TaggedPosition s

def leftInclusion (s : BranchPositionSpan) :
    LeftPosition s → TaggedPosition s
  | .inl i => .common i
  | .inr i => .left i

def rightInclusion (s : BranchPositionSpan) :
    RightPosition s → TaggedPosition s
  | .inl i => .common i
  | .inr i => .right i

theorem common_position_identified (s : BranchPositionSpan)
    (i : Fin s.shared.length) :
    leftInclusion s (.inl i) = rightInclusion s (.inl i) := by
  rfl

theorem branch_private_positions_disjoint (s : BranchPositionSpan)
    (i : Fin s.leftExtra.length) (j : Fin s.rightExtra.length) :
    leftInclusion s (.inr i) ≠ rightInclusion s (.inr j) := by
  intro h
  cases h

/-- The payload at a tagged position; identity is the TAGGED POSITION,
not equality of the payload itself. -/
def ticketAt (s : BranchPositionSpan) :
    TaggedPosition s → LocalReplayTicket
  | .common i => s.shared[i]
  | .left i => s.leftExtra[i]
  | .right i => s.rightExtra[i]

/-- Produce a tagged span from an already-proved v0.58 ancestor relation.
Classical choice selects the two existing suffix WITNESSES, not a real event. -/
noncomputable def spanFromArchive (a : TaggedForkArchive) :
    BranchPositionSpan where
  shared := a.ancestor.observedTickets
  leftExtra := Classical.choose a.leftExtends
  rightExtra := Classical.choose a.rightExtends

theorem archived_left_history_exact (a : TaggedForkArchive) :
    (spanFromArchive a).shared ++ (spanFromArchive a).leftExtra =
      a.left.observedTickets := by
  change a.ancestor.observedTickets ++ Classical.choose a.leftExtends =
    a.left.observedTickets
  exact (Classical.choose_spec a.leftExtends).symm

theorem archived_right_history_exact (a : TaggedForkArchive) :
    (spanFromArchive a).shared ++ (spanFromArchive a).rightExtra =
      a.right.observedTickets := by
  change a.ancestor.observedTickets ++ Classical.choose a.rightExtends =
    a.right.observedTickets
  exact (Classical.choose_spec a.rightExtends).symm

/-- The ONLY local compatibility condition for X-valued observations:
equality on the same prior (ancestor) positions. -/
def overlapCompatible {X : Type u} (s : BranchPositionSpan)
    (fL : LeftPosition s → X) (fR : RightPosition s → X) : Prop :=
  ∀ i : Fin s.shared.length, fL (.inl i) = fR (.inl i)

/-- The canonical gluing of compatible local observations onto the richer
tagged positional span. No linear event sequence is produced. -/
def glueTagged {X : Type u} (s : BranchPositionSpan)
    (fL : LeftPosition s → X) (fR : RightPosition s → X)
    (_h : overlapCompatible s fL fR) : TaggedPosition s → X
  | .common i => fL (.inl i)
  | .left i => fL (.inr i)
  | .right i => fR (.inr i)

theorem glue_left {X : Type u} (s : BranchPositionSpan)
    (fL : LeftPosition s → X) (fR : RightPosition s → X)
    (h : overlapCompatible s fL fR) (i : LeftPosition s) :
    glueTagged s fL fR h (leftInclusion s i) = fL i := by
  cases i with
  | inl j => rfl
  | inr j => rfl

theorem glue_right {X : Type u} (s : BranchPositionSpan)
    (fL : LeftPosition s → X) (fR : RightPosition s → X)
    (h : overlapCompatible s fL fR) (i : RightPosition s) :
    glueTagged s fL fR h (rightInclusion s i) = fR i := by
  cases i with
  | inl j => exact h j
  | inr j => rfl

theorem tagged_gluing_unique {X : Type u} (s : BranchPositionSpan)
    (fL : LeftPosition s → X) (fR : RightPosition s → X)
    (h : overlapCompatible s fL fR)
    (g : TaggedPosition s → X)
    (hl : ∀ i, g (leftInclusion s i) = fL i)
    (hr : ∀ i, g (rightInclusion s i) = fR i) :
    g = glueTagged s fL fR h := by
  funext pos
  cases pos with
  | common i => exact hl (.inl i)
  | left i => exact hl (.inr i)
  | right i => exact hr (.inr i)

/-- Genuine set-level universal mapping property of the tagged positional
amalgam: a simultaneous global observation exists iff the local values agree
on the shared ancestor. This says NOTHING about chronological linear descent. -/
theorem tagged_observation_gluing_iff {X : Type u} (s : BranchPositionSpan)
    (fL : LeftPosition s → X) (fR : RightPosition s → X) :
    (∃ g : TaggedPosition s → X,
      (∀ i, g (leftInclusion s i) = fL i) ∧
      (∀ i, g (rightInclusion s i) = fR i)) ↔
        overlapCompatible s fL fR := by
  constructor
  · rintro ⟨g, hl, hr⟩ i
    calc
      fL (.inl i) = g (leftInclusion s (.inl i)) := (hl (.inl i)).symm
      _ = g (rightInclusion s (.inl i)) := by rfl
      _ = fR (.inl i) := hr (.inl i)
  · intro h
    refine ⟨glueTagged s fL fR h, ?_, ?_⟩
    · intro i
      exact glue_left s fL fR h i
    · intro i
      exact glue_right s fL fR h i

theorem incompatible_observations_block_gluing {X : Type u}
    (s : BranchPositionSpan)
    (fL : LeftPosition s → X) (fR : RightPosition s → X)
    (h : ¬ overlapCompatible s fL fR) :
    ¬ ∃ g : TaggedPosition s → X,
      (∀ i, g (leftInclusion s i) = fL i) ∧
      (∀ i, g (rightInclusion s i) = fR i) := by
  intro witness
  exact h ((tagged_observation_gluing_iff s fL fR).mp witness)

/-- A particular ancestor-position disagreement is a concrete obstruction. -/
theorem shared_value_disagreement_obstructs {X : Type u}
    (s : BranchPositionSpan)
    (fL : LeftPosition s → X) (fR : RightPosition s → X)
    (i : Fin s.shared.length)
    (hne : fL (.inl i) ≠ fR (.inl i)) :
    ¬ overlapCompatible s fL fR := by
  intro h
  exact hne (h i)

/-- The v0.57 linear obstruction persists despite a richer positional span. -/
theorem archived_fork_remains_non_linear
    (ancestor left right : DetachedReplayWitness)
    (h : declaredForkObstruction ancestor left right) :
    ¬ hasDeclaredCommonLinearSuccessor left right := by
  exact declared_fork_blocks_linear_gluing ancestor left right h

/-- Even exact local branch-observation gluing is not host authority. -/
theorem tagged_span_gluing_grants_no_original_execution
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (valid : MiddleWayBoundedSynthesisIntakeCertificateValid p)
    (s : BranchPositionSpan)
    (fL : LeftPosition s → String) (fR : RightPosition s → String)
    (_h : overlapCompatible s fL fR) :
    p.executionPermission = false ∧
    p.executionAuthorityGranted = false ∧
    p.selectionAuthorityGrantedToPlanOS = false := by
  exact ⟨valid.execution_permission_false,
    valid.execution_authority_not_granted,
    valid.selection_authority_not_granted⟩

end KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59

#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.leftInclusion
#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.rightInclusion
#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.common_position_identified
#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.branch_private_positions_disjoint
#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.ticketAt
#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.spanFromArchive
#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.archived_left_history_exact
#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.archived_right_history_exact
#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.overlapCompatible
#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.glueTagged
#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.glue_left
#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.glue_right
#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.tagged_gluing_unique
#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.tagged_observation_gluing_iff
#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.incompatible_observations_block_gluing
#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.shared_value_disagreement_obstructs
#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.archived_fork_remains_non_linear
#print axioms KUOS.Architecture.LeanPythonTaggedSpanObservationGluingV0_59.tagged_span_gluing_grants_no_original_execution
