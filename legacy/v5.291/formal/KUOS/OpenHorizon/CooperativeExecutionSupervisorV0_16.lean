import Mathlib

namespace KUOS
namespace OpenHorizon

structure BoundedExecutionSlice where
  maximumSteps : ℕ
  executedSteps : ℕ
  bounded : executedSteps ≤ maximumSteps


theorem executionSlice_bounded (slice : BoundedExecutionSlice) :
    slice.executedSteps ≤ slice.maximumSteps := by
  exact slice.bounded


structure AllowlistedStep where
  operationId : String
  operationRegistered : True


theorem allowlistedStep_registered (step : AllowlistedStep) :
    step.operationRegistered := by
  exact step.operationRegistered


structure ForegroundYield where
  unfinished : Bool
  checkpointRecords : ℕ
  foregroundReleased : Bool
  checkpointPresent : unfinished = true → 0 < checkpointRecords
  releasedWhenUnfinished : unfinished = true → foregroundReleased = true


theorem unfinishedYield_has_checkpoint (yieldState : ForegroundYield)
    (h : yieldState.unfinished = true) :
    0 < yieldState.checkpointRecords := by
  exact yieldState.checkpointPresent h


theorem unfinishedYield_releases_prompt (yieldState : ForegroundYield)
    (h : yieldState.unfinished = true) :
    yieldState.foregroundReleased = true := by
  exact yieldState.releasedWhenUnfinished h


structure ContinuationTicket where
  checkpointRecords : ℕ
  checkpointPresent : 0 < checkpointRecords
  queued : Bool
  leased : Bool


theorem continuationTicket_has_checkpoint (ticket : ContinuationTicket) :
    0 < ticket.checkpointRecords := by
  exact ticket.checkpointPresent


theorem queuedTicket_not_claimed_by_definition (ticket : ContinuationTicket)
    (hqueued : ticket.queued = true)
    (hleased : ticket.leased = false) :
    ticket.queued = true ∧ ticket.leased = false := by
  exact ⟨hqueued, hleased⟩


structure JobPrefixProgress where
  completedBefore : ℕ
  completedAfter : ℕ
  monotone : completedBefore ≤ completedAfter


theorem completedPrefix_monotone (progress : JobPrefixProgress) :
    progress.completedBefore ≤ progress.completedAfter := by
  exact progress.monotone


def applyCommandOnce (processed : Finset ℕ) (digest : ℕ) : Finset ℕ :=
  insert digest processed


theorem applyCommandOnce_idempotent (processed : Finset ℕ) (digest : ℕ) :
    applyCommandOnce (applyCommandOnce processed digest) digest =
      applyCommandOnce processed digest := by
  simp [applyCommandOnce]


structure SupervisorHistory where
  cycles : ℕ
  sliceRecords : ℕ
  checkpointRecords : ℕ
  sliceAligned : sliceRecords = cycles
  checkpointAligned : checkpointRecords = cycles


def appendSupervisorCycle (history : SupervisorHistory) : SupervisorHistory where
  cycles := history.cycles + 1
  sliceRecords := history.sliceRecords + 1
  checkpointRecords := history.checkpointRecords + 1
  sliceAligned := by simp [history.sliceAligned]
  checkpointAligned := by simp [history.checkpointAligned]


theorem supervisorSliceHistory_strict (history : SupervisorHistory) :
    history.sliceRecords < (appendSupervisorCycle history).sliceRecords := by
  simp [appendSupervisorCycle]


theorem supervisorCheckpointHistory_strict (history : SupervisorHistory) :
    history.checkpointRecords <
      (appendSupervisorCycle history).checkpointRecords := by
  simp [appendSupervisorCycle]

end OpenHorizon
end KUOS
