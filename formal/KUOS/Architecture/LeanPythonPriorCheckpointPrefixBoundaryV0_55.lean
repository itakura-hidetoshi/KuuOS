import Mathlib
import KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54
import KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53
import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-!
# v0.55: conditional strict-prefix descent for detached LOCAL replay histories

The underlying v0.53 finite replay-key ledger and v0.54 abstract fold are
imported unchanged. A two-snapshot strict extension must preserve EVERY old
ticket in order and add at least one declared ticket. An independently
*supplied string* may be compared to an abstract digest of the prior
snapshot, but its external custody, provenance, independence, signature
and real-world time are not provided by this formal hypothesis.

This does NOT formalize Python canonical JSON/SHA-256, SQLite, actual issuer
authority, original missing PlanOS Finsets, cross-host replay protection,
global descent or host-execution rights.
-/

namespace KUOS.Architecture.LeanPythonPriorCheckpointPrefixBoundaryV0_55

open KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53
open KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54
open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-- A stated exact prefix, not proof of historical receipt or publication. -/
def declaredPrefixExtension (older newer : DetachedReplayWitness)
    (additional : List LocalReplayTicket) : Prop :=
  newer.observedTickets = older.observedTickets ++ additional

/-- Exclude a no-op repetition: at least one abstract new ticket is required. -/
def strictPrefixExtension (older newer : DetachedReplayWitness)
    (additional : List LocalReplayTicket) : Prop :=
  declaredPrefixExtension older newer additional ∧ additional ≠ []

/-- Abstract snapshot-digest value agreement only, not independent custody. -/
def callerPriorSnapshotMatches
    (digest : DetachedReplayWitness → String)
    (older : DetachedReplayWitness) (checkpoint : String) : Prop :=
  digest older = checkpoint

theorem strict_extension_has_longer_history
    (older newer : DetachedReplayWitness)
    (additional : List LocalReplayTicket)
    (h : strictPrefixExtension older newer additional) :
    older.observedTickets.length < newer.observedTickets.length := by
  rcases h with ⟨hcomp, hnonempty⟩
  change newer.observedTickets = older.observedTickets ++ additional at hcomp
  have hpos : 0 < additional.length := by
    cases additional with
    | nil => exact False.elim (hnonempty rfl)
    | cons t ts => simp
  rw [hcomp, List.length_append]
  omega

theorem prior_ticket_remains_in_extended_history
    (older newer : DetachedReplayWitness)
    (additional : List LocalReplayTicket)
    (h : declaredPrefixExtension older newer additional)
    (t : LocalReplayTicket) (ht : t ∈ older.observedTickets) :
    t ∈ newer.observedTickets := by
  change newer.observedTickets = older.observedTickets ++ additional at h
  rw [h]
  exact List.mem_append.mpr (Or.inl ht)

theorem prefix_extension_replays_from_prior_head
    (step : String → LocalReplayTicket → String)
    (genesis : String) (older newer : DetachedReplayWitness)
    (additional : List LocalReplayTicket)
    (hOld : selfConsistent step genesis older)
    (hNew : selfConsistent step genesis newer)
    (h : declaredPrefixExtension older newer additional) :
    newer.announcedHead = replayRoot step older.announcedHead additional := by
  change replayRoot step genesis older.observedTickets = older.announcedHead at hOld
  change replayRoot step genesis newer.observedTickets = newer.announcedHead at hNew
  change newer.observedTickets = older.observedTickets ++ additional at h
  calc
    newer.announcedHead = replayRoot step genesis newer.observedTickets := hNew.symm
    _ = replayRoot step genesis (older.observedTickets ++ additional) := by rw [h]
    _ = replayRoot step (replayRoot step genesis older.observedTickets) additional :=
      replayRoot_append step genesis older.observedTickets additional
    _ = replayRoot step older.announcedHead additional := by rw [hOld]

theorem divergent_history_blocks_declared_prefix
    (older newer : DetachedReplayWitness)
    (additional : List LocalReplayTicket)
    (h : newer.observedTickets ≠ older.observedTickets ++ additional) :
    ¬ declaredPrefixExtension older newer additional := by
  simpa [declaredPrefixExtension] using h

theorem checkpoint_value_mismatch_remains_obstruction
    (digest : DetachedReplayWitness → String)
    (older : DetachedReplayWitness) (checkpoint : String)
    (h : digest older ≠ checkpoint) :
    ¬ callerPriorSnapshotMatches digest older checkpoint := by
  simpa [callerPriorSnapshotMatches] using h

theorem compatible_strict_extension_with_checkpoint_value
    (step : String → LocalReplayTicket → String)
    (genesis : String) (digest : DetachedReplayWitness → String)
    (older newer : DetachedReplayWitness)
    (additional : List LocalReplayTicket) (checkpoint : String)
    (hOld : selfConsistent step genesis older)
    (hNew : selfConsistent step genesis newer)
    (hStrict : strictPrefixExtension older newer additional)
    (hCheckpoint : callerPriorSnapshotMatches digest older checkpoint) :
    digest older = checkpoint ∧
    newer.announcedHead = replayRoot step older.announcedHead additional ∧
    older.observedTickets.length < newer.observedTickets.length := by
  rcases hStrict with ⟨hPrefix, hNonempty⟩
  change digest older = checkpoint at hCheckpoint
  exact ⟨hCheckpoint,
    prefix_extension_replays_from_prior_head step genesis older newer
      additional hOld hNew hPrefix,
    strict_extension_has_longer_history older newer additional ⟨hPrefix, hNonempty⟩⟩

theorem strict_extension_histories_distinct
    (older newer : DetachedReplayWitness)
    (additional : List LocalReplayTicket)
    (h : strictPrefixExtension older newer additional) :
    older.observedTickets ≠ newer.observedTickets := by
  have hlen := strict_extension_has_longer_history older newer additional h
  intro heq
  have hlenEq := congrArg List.length heq
  omega

/-- Even matching declarations and checkpoint VALUES grant no PlanOS authority. -/
theorem local_prefix_check_does_not_grant_original_execution
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (valid : MiddleWayBoundedSynthesisIntakeCertificateValid p)
    (older newer : DetachedReplayWitness)
    (additional : List LocalReplayTicket)
    (_strict : strictPrefixExtension older newer additional)
    (digest : DetachedReplayWitness → String) (checkpoint : String)
    (_checkpoint : callerPriorSnapshotMatches digest older checkpoint) :
    p.executionPermission = false ∧
    p.executionAuthorityGranted = false ∧
    p.selectionAuthorityGrantedToPlanOS = false := by
  exact ⟨valid.execution_permission_false,
    valid.execution_authority_not_granted,
    valid.selection_authority_not_granted⟩

end KUOS.Architecture.LeanPythonPriorCheckpointPrefixBoundaryV0_55

#print axioms KUOS.Architecture.LeanPythonPriorCheckpointPrefixBoundaryV0_55.declaredPrefixExtension
#print axioms KUOS.Architecture.LeanPythonPriorCheckpointPrefixBoundaryV0_55.strictPrefixExtension
#print axioms KUOS.Architecture.LeanPythonPriorCheckpointPrefixBoundaryV0_55.callerPriorSnapshotMatches
#print axioms KUOS.Architecture.LeanPythonPriorCheckpointPrefixBoundaryV0_55.strict_extension_has_longer_history
#print axioms KUOS.Architecture.LeanPythonPriorCheckpointPrefixBoundaryV0_55.prior_ticket_remains_in_extended_history
#print axioms KUOS.Architecture.LeanPythonPriorCheckpointPrefixBoundaryV0_55.prefix_extension_replays_from_prior_head
#print axioms KUOS.Architecture.LeanPythonPriorCheckpointPrefixBoundaryV0_55.divergent_history_blocks_declared_prefix
#print axioms KUOS.Architecture.LeanPythonPriorCheckpointPrefixBoundaryV0_55.checkpoint_value_mismatch_remains_obstruction
#print axioms KUOS.Architecture.LeanPythonPriorCheckpointPrefixBoundaryV0_55.compatible_strict_extension_with_checkpoint_value
#print axioms KUOS.Architecture.LeanPythonPriorCheckpointPrefixBoundaryV0_55.strict_extension_histories_distinct
#print axioms KUOS.Architecture.LeanPythonPriorCheckpointPrefixBoundaryV0_55.local_prefix_check_does_not_grant_original_execution
