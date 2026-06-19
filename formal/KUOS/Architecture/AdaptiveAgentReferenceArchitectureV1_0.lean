import Mathlib

namespace KUOS.Architecture

inductive Plane where
  | deliberation
  | execution
  | learning
  | authority
  | assurance
  | recovery
  deriving DecidableEq, Repr

inductive TaskStage where
  | belief
  | decision
  | plan
  | act
  | observe
  | verify
  | learn
  | terminal
  deriving DecidableEq, Repr

inductive ControlMode where
  | idle
  | active
  | suspended
  | recovering
  | terminated
  deriving DecidableEq, Repr

inductive AuthorityMode where
  | unbound
  | bound
  | leased
  | renewalReview
  | escalation
  | rerotation
  deriving DecidableEq, Repr

inductive ModuleStatus where
  | idle
  | running
  | succeeded
  | failed
  | blocked
  | suspended
  deriving DecidableEq, Repr

inductive RecoveryDecision where
  | continue
  | retry
  | revalidate
  | replan
  | renew
  | escalate
  | rerotate
  | requestHuman
  | abort
  deriving DecidableEq, Repr

inductive AdaptiveEvent where
  | decisionCommitted
  | planBound
  | authorityBound
  | leaseActivated
  | sessionBootstrapped
  | actAuthorized
  | effectRecorded
  | observationCommitted
  | verificationPassed
  | verificationFailed
  | learningCommitted
  | leaseAnomaly
  | recoveryRouted (decision : RecoveryDecision)
  | recoveryCompleted (decision : RecoveryDecision)
  | aborted
  deriving DecidableEq, Repr

structure AdaptiveControlState where
  taskStage : TaskStage
  controlMode : ControlMode
  authorityMode : AuthorityMode
  moduleStatus : ModuleStatus
  owner : Nat
  epoch : Nat
  lineage : Nat
  activeSession : Option Nat
  terminalSessions : Finset Nat
  observationCommitted : Bool
  verificationCommitted : Bool
  recoveryDecision : RecoveryDecision
  requiresNewActivation : Bool
  requiresNewSession : Bool
  executionAllowed : Bool
  deriving DecidableEq


def SafeState (state : AdaptiveControlState) : Prop :=
  (state.executionAllowed = true →
    state.taskStage = TaskStage.act ∧
    state.controlMode = ControlMode.active ∧
    state.authorityMode = AuthorityMode.leased ∧
    state.moduleStatus = ModuleStatus.running ∧
    ∃ session, state.activeSession = some session) ∧
  ((state.controlMode = ControlMode.suspended ∨
      state.controlMode = ControlMode.recovering ∨
      state.controlMode = ControlMode.terminated) →
    state.executionAllowed = false) ∧
  (∀ session, state.activeSession = some session →
    session ∉ state.terminalSessions) ∧
  (state.verificationCommitted = true →
    state.observationCommitted = true) ∧
  (state.requiresNewSession = true → state.activeSession = none) ∧
  (state.controlMode = ControlMode.terminated →
    state.taskStage = TaskStage.terminal ∧
    state.executionAllowed = false ∧
    state.activeSession = none)


def TransitionAdmissible
    (source : AdaptiveControlState)
    (event : AdaptiveEvent)
    (target : AdaptiveControlState) : Prop :=
  SafeState target ∧
  match event with
  | AdaptiveEvent.sessionBootstrapped =>
      ∃ session,
        target.activeSession = some session ∧
        session ∉ source.terminalSessions
  | AdaptiveEvent.actAuthorized =>
      target.executionAllowed = true
  | AdaptiveEvent.observationCommitted =>
      source.taskStage = TaskStage.observe ∧
      target.taskStage = TaskStage.verify ∧
      target.observationCommitted = true ∧
      target.verificationCommitted = false
  | AdaptiveEvent.verificationPassed =>
      source.taskStage = TaskStage.verify ∧
      source.observationCommitted = true ∧
      target.verificationCommitted = true
  | AdaptiveEvent.verificationFailed =>
      source.taskStage = TaskStage.verify ∧
      source.observationCommitted = true ∧
      target.controlMode = ControlMode.suspended ∧
      target.executionAllowed = false
  | AdaptiveEvent.leaseAnomaly =>
      target.controlMode = ControlMode.suspended ∧
      target.executionAllowed = false ∧
      target.activeSession = none ∧
      ∀ session, source.activeSession = some session →
        session ∈ target.terminalSessions
  | AdaptiveEvent.recoveryRouted decision =>
      source.controlMode = ControlMode.suspended ∧
      target.recoveryDecision = decision ∧
      (decision = RecoveryDecision.abort →
        target.controlMode = ControlMode.terminated) ∧
      (decision ≠ RecoveryDecision.abort →
        target.controlMode = ControlMode.recovering ∧
        target.requiresNewActivation = true ∧
        target.requiresNewSession = true)
  | AdaptiveEvent.recoveryCompleted decision =>
      source.controlMode = ControlMode.recovering ∧
      target.controlMode = ControlMode.active ∧
      target.taskStage = TaskStage.plan ∧
      target.lineage ≠ source.lineage ∧
      target.activeSession = none ∧
      target.requiresNewActivation = true ∧
      target.requiresNewSession = true ∧
      (decision = RecoveryDecision.rerotate →
        target.epoch = source.epoch + 1)
  | AdaptiveEvent.aborted =>
      target.taskStage = TaskStage.terminal ∧
      target.controlMode = ControlMode.terminated ∧
      target.executionAllowed = false ∧
      target.activeSession = none
  | _ => True


theorem safe_execution_requires_active_leased_session
    (state : AdaptiveControlState)
    (safe : SafeState state)
    (allowed : state.executionAllowed = true) :
    state.taskStage = TaskStage.act ∧
    state.controlMode = ControlMode.active ∧
    state.authorityMode = AuthorityMode.leased ∧
    state.moduleStatus = ModuleStatus.running ∧
    ∃ session, state.activeSession = some session := by
  exact safe.1 allowed


theorem inactive_control_blocks_execution
    (state : AdaptiveControlState)
    (safe : SafeState state)
    (inactive : state.controlMode = ControlMode.suspended ∨
      state.controlMode = ControlMode.recovering ∨
      state.controlMode = ControlMode.terminated) :
    state.executionAllowed = false := by
  exact safe.2.1 inactive


theorem terminal_session_never_active
    (state : AdaptiveControlState)
    (safe : SafeState state)
    (session : Nat)
    (active : state.activeSession = some session) :
    session ∉ state.terminalSessions := by
  exact safe.2.2.1 session active


theorem verification_requires_observation
    (state : AdaptiveControlState)
    (safe : SafeState state)
    (verified : state.verificationCommitted = true) :
    state.observationCommitted = true := by
  exact safe.2.2.2.1 verified


theorem new_session_debt_has_no_active_session
    (state : AdaptiveControlState)
    (safe : SafeState state)
    (debt : state.requiresNewSession = true) :
    state.activeSession = none := by
  exact safe.2.2.2.2.1 debt


theorem lease_anomaly_suspends_and_terminalizes
    (source target : AdaptiveControlState)
    (step : TransitionAdmissible source AdaptiveEvent.leaseAnomaly target) :
    target.controlMode = ControlMode.suspended ∧
    target.executionAllowed = false ∧
    target.activeSession = none ∧
    ∀ session, source.activeSession = some session →
      session ∈ target.terminalSessions := by
  exact step.2


theorem terminal_session_rebootstrap_forbidden
    (source target : AdaptiveControlState)
    (step : TransitionAdmissible source AdaptiveEvent.sessionBootstrapped target) :
    ∃ session,
      target.activeSession = some session ∧
      session ∉ source.terminalSessions := by
  exact step.2


theorem recovery_completion_requires_fresh_lineage_and_session
    (source target : AdaptiveControlState)
    (decision : RecoveryDecision)
    (step : TransitionAdmissible source
      (AdaptiveEvent.recoveryCompleted decision) target) :
    target.lineage ≠ source.lineage ∧
    target.activeSession = none ∧
    target.requiresNewActivation = true ∧
    target.requiresNewSession = true := by
  exact ⟨step.2.2.2.2.1,
    step.2.2.2.2.2.1,
    step.2.2.2.2.2.2.1,
    step.2.2.2.2.2.2.2.1⟩


theorem rerotation_completion_increments_epoch
    (source target : AdaptiveControlState)
    (step : TransitionAdmissible source
      (AdaptiveEvent.recoveryCompleted RecoveryDecision.rerotate) target) :
    target.epoch = source.epoch + 1 := by
  exact step.2.2.2.2.2.2.2.2 rfl


theorem abort_is_nonexecuting_terminal
    (source target : AdaptiveControlState)
    (step : TransitionAdmissible source AdaptiveEvent.aborted target) :
    target.taskStage = TaskStage.terminal ∧
    target.controlMode = ControlMode.terminated ∧
    target.executionAllowed = false ∧
    target.activeSession = none := by
  exact step.2


def planOSImplementationPlane (version : Nat) : Plane :=
  if version ≤ 8 then Plane.deliberation
  else if version ≤ 14 then Plane.authority
  else if version = 15 then Plane.execution
  else if version = 16 then Plane.assurance
  else Plane.recovery


theorem planOS_v0_1_plane :
    planOSImplementationPlane 1 = Plane.deliberation := by
  norm_num [planOSImplementationPlane]


theorem planOS_v0_8_plane :
    planOSImplementationPlane 8 = Plane.deliberation := by
  norm_num [planOSImplementationPlane]


theorem planOS_v0_9_plane :
    planOSImplementationPlane 9 = Plane.authority := by
  norm_num [planOSImplementationPlane]


theorem planOS_v0_14_plane :
    planOSImplementationPlane 14 = Plane.authority := by
  norm_num [planOSImplementationPlane]


theorem planOS_v0_15_plane :
    planOSImplementationPlane 15 = Plane.execution := by
  norm_num [planOSImplementationPlane]


theorem planOS_v0_16_plane :
    planOSImplementationPlane 16 = Plane.assurance := by
  norm_num [planOSImplementationPlane]


theorem planOS_v0_17_plane :
    planOSImplementationPlane 17 = Plane.recovery := by
  norm_num [planOSImplementationPlane]

end KUOS.Architecture
