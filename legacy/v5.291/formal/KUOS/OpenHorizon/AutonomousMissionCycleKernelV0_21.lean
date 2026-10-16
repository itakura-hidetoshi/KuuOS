import Mathlib

namespace KUOS
namespace OpenHorizon

inductive AutonomousMissionPhase where
  | mission
  | plan
  | act
  | observe
  | verify
  | learn
  | replan
  deriving DecidableEq, Repr


def AutonomousMissionPhase.next : AutonomousMissionPhase → AutonomousMissionPhase
  | .mission => .plan
  | .plan => .act
  | .act => .observe
  | .observe => .verify
  | .verify => .learn
  | .learn => .replan
  | .replan => .plan


theorem autonomousMissionPhase_next_ne
    (phase : AutonomousMissionPhase) : phase.next ≠ phase := by
  cases phase <;> decide


structure PersistentMissionCycleTransition where
  sourceCycle : ℕ
  targetCycle : ℕ
  sourceEventIndex : ℕ
  targetEventIndex : ℕ
  sourcePhase : AutonomousMissionPhase
  targetPhase : AutonomousMissionPhase
  phaseOrdered : targetPhase = sourcePhase.next
  eventAppended : targetEventIndex = sourceEventIndex + 1
  cyclePreservedUnlessReplan :
    sourcePhase ≠ .learn → targetCycle = sourceCycle
  replanClosesCycle :
    sourcePhase = .learn → targetCycle = sourceCycle + 1


theorem persistentMissionCycle_event_advances
    (transition : PersistentMissionCycleTransition) :
    transition.targetEventIndex > transition.sourceEventIndex := by
  rw [transition.eventAppended]
  omega


theorem persistentMissionCycle_phase_is_ordered
    (transition : PersistentMissionCycleTransition) :
    transition.targetPhase = transition.sourcePhase.next := by
  exact transition.phaseOrdered


theorem persistentMissionCycle_replan_advances_cycle
    (transition : PersistentMissionCycleTransition)
    (h : transition.sourcePhase = .learn) :
    transition.targetCycle = transition.sourceCycle + 1 := by
  exact transition.replanClosesCycle h


structure PersistentActReceipt where
  actionReceiptPresent : Bool
  lowerAuthorityReceiptPresent : Bool
  licensedEffectApplied : Bool
  grantsExecutionAuthority : Bool
  actionReceiptRequired : actionReceiptPresent = true
  lowerReceiptRequired : lowerAuthorityReceiptPresent = true
  realEffectRequired : licensedEffectApplied = true
  authorityNotGranted : grantsExecutionAuthority = false


theorem persistentActReceipt_has_real_effect
    (receipt : PersistentActReceipt) :
    receipt.licensedEffectApplied = true := by
  exact receipt.realEffectRequired


theorem persistentActReceipt_preserves_lower_authority
    (receipt : PersistentActReceipt) :
    receipt.grantsExecutionAuthority = false := by
  exact receipt.authorityNotGranted


structure FutureOnlyLearningReceipt where
  futureOnly : Bool
  memoryOverwrite : Bool
  futureBounded : futureOnly = true
  overwriteForbidden : memoryOverwrite = false


theorem futureOnlyLearning_does_not_overwrite
    (receipt : FutureOnlyLearningReceipt) :
    receipt.memoryOverwrite = false := by
  exact receipt.overwriteForbidden


structure AppendOnlyMissionLedger where
  committedEvents : ℕ
  recoveredEvents : ℕ
  snapshotEvents : ℕ
  recoveryExact : recoveredEvents = committedEvents
  snapshotDerived : snapshotEvents = recoveredEvents


theorem appendOnlyMissionLedger_snapshot_matches_commits
    (ledger : AppendOnlyMissionLedger) :
    ledger.snapshotEvents = ledger.committedEvents := by
  rw [ledger.snapshotDerived, ledger.recoveryExact]

end OpenHorizon
end KUOS
