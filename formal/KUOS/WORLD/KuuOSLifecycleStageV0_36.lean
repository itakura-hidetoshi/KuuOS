import KUOS.WORLD.KuuOSLifecycleStageV0_35

namespace KUOS.WORLD.KuuOSLifecycleStageV0_36

inductive CompletionStatus where
  | complete
  | alert
  | rejected
  deriving DecidableEq, Repr

structure CompletionWitness where
  sourceReady : Bool
  sourceRecomputed : Bool
  targetBound : Bool
  receiptBound : Bool
  terminalBound : Bool
  memorySealHeld : Bool
  memorialReadOnly : Bool
  covenantActive : Bool
  authorityAuthorized : Bool
  status : CompletionStatus
  recordIssued : Bool
  completed : Bool
  terminal : Bool
  followingRoute : Bool
  responseNext : Bool
  repositoryChanged : Bool
  externalOperationPerformed : Bool

structure CompletionWitness.ValidComplete (w : CompletionWitness) : Prop where
  sourceReady : w.sourceReady = true
  sourceRecomputed : w.sourceRecomputed = true
  targetBound : w.targetBound = true
  receiptBound : w.receiptBound = true
  terminalBound : w.terminalBound = true
  memorySealHeld : w.memorySealHeld = true
  memorialReadOnly : w.memorialReadOnly = true
  covenantActive : w.covenantActive = true
  authorityAuthorized : w.authorityAuthorized = true
  statusComplete : w.status = CompletionStatus.complete
  recordIssued : w.recordIssued = true
  completed : w.completed = true
  terminal : w.terminal = true
  followingRouteFalse : w.followingRoute = false
  responseNotNext : w.responseNext = false

structure CompletionWitness.ValidAlert (w : CompletionWitness) : Prop where
  sourceReady : w.sourceReady = true
  sourceRecomputed : w.sourceRecomputed = true
  targetBound : w.targetBound = true
  statusAlert : w.status = CompletionStatus.alert
  recordIssued : w.recordIssued = true
  completedFalse : w.completed = false
  terminalFalse : w.terminal = false
  responseNext : w.responseNext = true

structure CompletionWitness.ValidRejected (w : CompletionWitness) : Prop where
  statusRejected : w.status = CompletionStatus.rejected
  recordNotIssued : w.recordIssued = false
  completedFalse : w.completed = false
  terminalFalse : w.terminal = false
  responseNotNext : w.responseNext = false

structure CompletionWitness.NoEffect (w : CompletionWitness) : Prop where
  repositoryChangeAbsent : w.repositoryChanged = false
  externalOperationAbsent : w.externalOperationPerformed = false

structure CompletionWitness.Valid (w : CompletionWitness) : Prop where
  caseValid : w.ValidComplete ∨ w.ValidAlert ∨ w.ValidRejected
  noEffect : w.NoEffect

theorem complete_has_no_following_route
    (w : CompletionWitness) (h : w.ValidComplete) :
    w.terminal = true ∧ w.followingRoute = false := by
  exact ⟨h.terminal, h.followingRouteFalse⟩

theorem alert_requests_response_only
    (w : CompletionWitness) (h : w.ValidAlert) :
    w.terminal = false ∧ w.responseNext = true := by
  exact ⟨h.terminalFalse, h.responseNext⟩

theorem rejected_issues_no_record
    (w : CompletionWitness) (h : w.ValidRejected) :
    w.recordIssued = false ∧ w.completed = false := by
  exact ⟨h.recordNotIssued, h.completedFalse⟩

theorem valid_completion_has_no_effect
    (w : CompletionWitness) (h : w.Valid) :
    w.NoEffect := by
  exact h.noEffect

end KUOS.WORLD.KuuOSLifecycleStageV0_36
