import Mathlib
import KUOS.Architecture.LeanPythonLocallyMacBoundPlanClaimsV0_52
import KUOS.Architecture.LeanPythonTwoDeclaredPlanResultClaimsV0_51
import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-!
# v0.53: Finite abstract replay-key reservation versus original PlanOS authority

An exact pair of locally MAC-checked claim envelopes can be recorded in a
separately provided local SQLite ledger. This formal module models ONLY the
finite key-membership boundary and append-only inclusion of seen keys.

It does not prove SQLite atomicity, HMAC security, issuer identity,
cross-machine freshness, external causal history, or that the original
Python PlanOS emitted the three resulting Finsets. The actual original
typed PlanOS certificate is imported directly and remains unchanged.
-/

namespace KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53

open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03
open KUOS.Architecture.LeanPythonLocallyMacBoundPlanClaimsV0_52

/-- A declared key/context/sequence and key/nonce pair, not an issuer proof. -/
structure LocalReplayTicket where
  keyId : String
  contextId : String
  sequence : Nat
  nonceHex : String
  deriving DecidableEq, Repr

def sequenceKey (t : LocalReplayTicket) : String × String × Nat :=
  (t.keyId, t.contextId, t.sequence)

def nonceKey (t : LocalReplayTicket) : String × String :=
  (t.keyId, t.nonceHex)

/-- In-memory abstract set state. Physical SQLite/locking is OUTSIDE Lean. -/
structure LocalReplayLedger where
  seenSequences : Finset (String × String × Nat)
  seenNonces : Finset (String × String)

/-- Freshness means both keys are absent, only within this supplied state. -/
def locallyFresh (s : LocalReplayLedger) (t : LocalReplayTicket) : Prop :=
  sequenceKey t ∉ s.seenSequences ∧ nonceKey t ∉ s.seenNonces

/-- Pairwise freshness also rejects duplicate keys within the pair. -/
def pairFresh (s : LocalReplayLedger)
    (a b : LocalReplayTicket) : Prop :=
  locallyFresh s a ∧ locallyFresh s b ∧
  sequenceKey a ≠ sequenceKey b ∧ nonceKey a ≠ nonceKey b

def appendTicket (s : LocalReplayLedger)
    (t : LocalReplayTicket) : LocalReplayLedger where
  seenSequences := insert (sequenceKey t) s.seenSequences
  seenNonces := insert (nonceKey t) s.seenNonces

/-- The pure mathematical analogue of an all-or-nothing pair reservation.
It does not establish that any particular SQLite transaction committed. -/
def reserveIfPairFresh (s : LocalReplayLedger)
    (a b : LocalReplayTicket) : LocalReplayLedger :=
  if pairFresh s a b then appendTicket (appendTicket s a) b else s

theorem rejected_pair_leaves_ledger_unchanged
    (s : LocalReplayLedger) (a b : LocalReplayTicket)
    (h : ¬ pairFresh s a b) :
    reserveIfPairFresh s a b = s := by
  simp [reserveIfPairFresh, h]

theorem successful_pair_retains_previous_sequences
    (s : LocalReplayLedger) (a b : LocalReplayTicket)
    (h : pairFresh s a b)
    (k : String × String × Nat) (hk : k ∈ s.seenSequences) :
    k ∈ (reserveIfPairFresh s a b).seenSequences := by
  simp [reserveIfPairFresh, h, appendTicket, hk]

theorem successful_pair_contains_both_keys
    (s : LocalReplayLedger) (a b : LocalReplayTicket)
    (h : pairFresh s a b) :
    sequenceKey a ∈ (reserveIfPairFresh s a b).seenSequences ∧
    sequenceKey b ∈ (reserveIfPairFresh s a b).seenSequences ∧
    nonceKey a ∈ (reserveIfPairFresh s a b).seenNonces ∧
    nonceKey b ∈ (reserveIfPairFresh s a b).seenNonces := by
  simp [reserveIfPairFresh, h, appendTicket]

theorem fresh_pair_has_distinct_keys
    (s : LocalReplayLedger) (a b : LocalReplayTicket)
    (h : pairFresh s a b) :
    sequenceKey a ≠ sequenceKey b ∧ nonceKey a ≠ nonceKey b := by
  rcases h with ⟨_, _, hs, hn⟩
  exact ⟨hs, hn⟩

/-- Reservation is never a substitute for original valid PlanOS permissions.
No proof of a committed SQLite transaction is supplied by this theorem. -/
theorem local_replay_reservation_grants_no_original_execution
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (valid : MiddleWayBoundedSynthesisIntakeCertificateValid p)
    (s : LocalReplayLedger) (a b : LocalReplayTicket)
    (_fresh : pairFresh s a b) :
    p.executionPermission = false ∧
    p.executionAuthorityGranted = false ∧
    p.selectionAuthorityGrantedToPlanOS = false := by
  exact ⟨valid.execution_permission_false,
    valid.execution_authority_not_granted,
    valid.selection_authority_not_granted⟩

end KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53

#print axioms KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53.sequenceKey
#print axioms KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53.nonceKey
#print axioms KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53.locallyFresh
#print axioms KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53.pairFresh
#print axioms KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53.appendTicket
#print axioms KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53.reserveIfPairFresh
#print axioms KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53.rejected_pair_leaves_ledger_unchanged
#print axioms KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53.successful_pair_retains_previous_sequences
#print axioms KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53.successful_pair_contains_both_keys
#print axioms KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53.fresh_pair_has_distinct_keys
#print axioms KUOS.Architecture.LeanPythonLocalReplayLedgerBoundaryV0_53.local_replay_reservation_grants_no_original_execution
