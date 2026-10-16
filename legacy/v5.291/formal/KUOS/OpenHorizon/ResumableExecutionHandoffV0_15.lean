import Mathlib

namespace KUOS
namespace OpenHorizon

inductive HandoffState where
  | running
  | backgroundQueued
  | waitingExternal
  | budgetPaused
  | retryBackoff
  | blockedBug
  | permissionBlocked
  | needsUserInput
  | retryExhausted
  | completed
  | cancelled
  deriving DecidableEq, Repr


def pausedOrBlocked : HandoffState → Prop
  | .running => False
  | .completed => False
  | .cancelled => False
  | .backgroundQueued => True
  | .waitingExternal => True
  | .budgetPaused => True
  | .retryBackoff => True
  | .blockedBug => True
  | .permissionBlocked => True
  | .needsUserInput => True
  | .retryExhausted => True


structure HandoffDecision where
  state : HandoffState
  feedbackRecords : ℕ
  checkpointRecords : ℕ
  foregroundReleased : Bool
  feedbackForPause : pausedOrBlocked state → 0 < feedbackRecords
  checkpointForPause : pausedOrBlocked state → 0 < checkpointRecords
  foregroundReleaseForPause : pausedOrBlocked state → foregroundReleased = true


theorem paused_has_feedback (decision : HandoffDecision)
    (hpaused : pausedOrBlocked decision.state) :
    0 < decision.feedbackRecords := by
  exact decision.feedbackForPause hpaused


theorem paused_has_checkpoint (decision : HandoffDecision)
    (hpaused : pausedOrBlocked decision.state) :
    0 < decision.checkpointRecords := by
  exact decision.checkpointForPause hpaused


theorem paused_releases_foreground (decision : HandoffDecision)
    (hpaused : pausedOrBlocked decision.state) :
    decision.foregroundReleased = true := by
  exact decision.foregroundReleaseForPause hpaused


def boundedProgress (raw : ℚ) : ℚ := max 0 (min 1 raw)


theorem boundedProgress_nonnegative (raw : ℚ) :
    0 ≤ boundedProgress raw := by
  simp [boundedProgress]


theorem boundedProgress_upper (raw : ℚ) :
    boundedProgress raw ≤ 1 := by
  simp [boundedProgress]


structure BackgroundTicket where
  checkpointRecords : ℕ
  checkpointPresent : 0 < checkpointRecords
  leaseDurationMs : ℕ


theorem backgroundTicket_has_checkpoint (ticket : BackgroundTicket) :
    0 < ticket.checkpointRecords := by
  exact ticket.checkpointPresent


theorem backgroundTicket_lease_nonnegative (ticket : BackgroundTicket) :
    0 ≤ ticket.leaseDurationMs := by
  exact Nat.zero_le _


structure RetrySchedule where
  delayMs : ℕ


theorem retryDelay_nonnegative (schedule : RetrySchedule) :
    0 ≤ schedule.delayMs := by
  exact Nat.zero_le _


structure HandoffHistory where
  cycles : ℕ
  feedbackRecords : ℕ
  checkpointRecords : ℕ
  feedbackAligned : feedbackRecords = cycles
  checkpointAligned : checkpointRecords = cycles


def appendHandoffCycle (history : HandoffHistory) : HandoffHistory where
  cycles := history.cycles + 1
  feedbackRecords := history.feedbackRecords + 1
  checkpointRecords := history.checkpointRecords + 1
  feedbackAligned := by simp [history.feedbackAligned]
  checkpointAligned := by simp [history.checkpointAligned]


theorem handoffFeedback_strict (history : HandoffHistory) :
    history.feedbackRecords < (appendHandoffCycle history).feedbackRecords := by
  simp [appendHandoffCycle]


theorem handoffCheckpoint_strict (history : HandoffHistory) :
    history.checkpointRecords < (appendHandoffCycle history).checkpointRecords := by
  simp [appendHandoffCycle]

end OpenHorizon
end KUOS
