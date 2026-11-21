import Mathlib
import KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53
import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-!
# v0.54: detached replay witnesses and caller-supplied checkpoint conditions

The previous v0.53 model formalizes finite LOCAL replay-key reservation.
This module adds a pure, abstract left-fold history and a detached witness
whose stated head may be compared with an EXTERNALLY SUPPLIED string.

The hash step is an arbitrary function: this is NOT a Lean verification of
SHA-256, Python JSON canonicalization, SQLite, checkpoint provenance,
external publisher authentication, causal time or cross-host uniqueness.
Even equality of two strings does NOT establish independent custody.
The original typed PlanOS remains unchanged and grants no host authority.
-/

namespace KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54

open KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53
open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-- Declared local entries and a declared chain head, not an issued certificate. -/
structure DetachedReplayWitness where
  observedTickets : List LocalReplayTicket
  announcedHead : String
  deriving Repr

/-- Abstract deterministic fold, with no cryptographic assumption on step. -/
def replayRoot (step : String → LocalReplayTicket → String)
    (genesis : String) (tickets : List LocalReplayTicket) : String :=
  tickets.foldl step genesis

def selfConsistent (step : String → LocalReplayTicket → String)
    (genesis : String) (w : DetachedReplayWitness) : Prop :=
  replayRoot step genesis w.observedTickets = w.announcedHead

/-- Equality of supplied strings, not authentication of their origins. -/
def callerCheckpointMatches (w : DetachedReplayWitness)
    (checkpoint : String) : Prop :=
  w.announcedHead = checkpoint

theorem replayRoot_append (step : String → LocalReplayTicket → String)
    (genesis : String) (initial rest : List LocalReplayTicket) :
    replayRoot step genesis (initial ++ rest) =
      replayRoot step (replayRoot step genesis initial) rest := by
  simp [replayRoot, List.foldl_append]

theorem supplied_checkpoint_agrees_with_replay
    (step : String → LocalReplayTicket → String)
    (genesis : String) (w : DetachedReplayWitness)
    (checkpoint : String)
    (hself : selfConsistent step genesis w)
    (hmatch : callerCheckpointMatches w checkpoint) :
    replayRoot step genesis w.observedTickets = checkpoint := by
  exact hself.trans hmatch

theorem checkpoint_mismatch_remains_obstruction
    (w : DetachedReplayWitness) (checkpoint : String)
    (hne : w.announcedHead ≠ checkpoint) :
    ¬ callerCheckpointMatches w checkpoint := by
  simpa [callerCheckpointMatches] using hne

theorem prefix_extension_replays
    (step : String → LocalReplayTicket → String)
    (genesis : String) (initial rest : List LocalReplayTicket)
    (announced : String)
    (h : selfConsistent step genesis
      ⟨initial ++ rest, announced⟩) :
    replayRoot step (replayRoot step genesis initial) rest = announced := by
  simpa [selfConsistent, replayRoot_append] using h

/-- Explicitly retain the v0.53 finite local inclusion theorem. -/
theorem recorded_fresh_pair_contains_both_local_keys
    (s : LocalReplayLedger) (a b : LocalReplayTicket)
    (hfresh : pairFresh s a b) :
    sequenceKey a ∈ (reserveIfPairFresh s a b).seenSequences ∧
    sequenceKey b ∈ (reserveIfPairFresh s a b).seenSequences ∧
    nonceKey a ∈ (reserveIfPairFresh s a b).seenNonces ∧
    nonceKey b ∈ (reserveIfPairFresh s a b).seenNonces := by
  exact successful_pair_contains_both_keys s a b hfresh

/-- A matching detached checkpoint cannot grant the original PlanOS host power. -/
theorem detached_witness_grants_no_original_execution
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (valid : MiddleWayBoundedSynthesisIntakeCertificateValid p)
    (step : String → LocalReplayTicket → String)
    (genesis : String) (w : DetachedReplayWitness)
    (checkpoint : String)
    (_self : selfConsistent step genesis w)
    (_match : callerCheckpointMatches w checkpoint) :
    p.executionPermission = false ∧
    p.executionAuthorityGranted = false ∧
    p.selectionAuthorityGrantedToPlanOS = false := by
  exact ⟨valid.execution_permission_false,
    valid.execution_authority_not_granted,
    valid.selection_authority_not_granted⟩

end KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54

#print axioms KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54.replayRoot
#print axioms KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54.selfConsistent
#print axioms KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54.callerCheckpointMatches
#print axioms KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54.replayRoot_append
#print axioms KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54.supplied_checkpoint_agrees_with_replay
#print axioms KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54.checkpoint_mismatch_remains_obstruction
#print axioms KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54.prefix_extension_replays
#print axioms KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54.recorded_fresh_pair_contains_both_local_keys
#print axioms KUOS.Architecture.LeanPythonDetachedReplayWitnessBoundaryV0_54.detached_witness_grants_no_original_execution
