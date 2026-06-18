import Mathlib
import KUOS.PlanOS.GenerationalReplanCycleDriverV0_5

namespace KUOS.PlanOS

inductive MultiGenerationDecision where
  | continue
  | stopConverged
  | stopMaximum
  | stopStagnation
  | stopOscillation
  | holdObservationDebt
  | holdRecovery
  | stopMissionComplete
  | handoverRequested
  | handoverBoundary
  deriving DecidableEq

structure MultiGenerationPolicy where
  maximumGenerations : Nat
  maximumPositive : 0 < maximumGenerations

structure BoundedGenerationState where
  completedGenerations : Nat
  policy : MultiGenerationPolicy
  bounded : completedGenerations ≤ policy.maximumGenerations


theorem completed_generations_are_bounded
    (state : BoundedGenerationState) :
    state.completedGenerations ≤ state.policy.maximumGenerations := by
  exact state.bounded

structure SuccessorGeneration where
  sourceCycle : Nat
  nextCycle : Nat
  exactSuccessor : nextCycle = sourceCycle + 1


theorem multi_generation_cycle_is_exact_successor
    (generation : SuccessorGeneration) :
    generation.nextCycle = generation.sourceCycle + 1 := by
  exact generation.exactSuccessor

structure GenerationDigestChain where
  expectedPreviousDigest : Nat
  suppliedPreviousDigest : Nat
  chainRequired : suppliedPreviousDigest = expectedPreviousDigest


theorem generation_digest_chain_is_preserved
    (chain : GenerationDigestChain) :
    chain.suppliedPreviousDigest = chain.expectedPreviousDigest := by
  exact chain.chainRequired

inductive SupervisorStatus where
  | active
  | hold
  | stopped
  | handover
  deriving DecidableEq


def isTerminal : SupervisorStatus → Bool
  | .active => false
  | .hold => true
  | .stopped => true
  | .handover => true

structure ContinuationBoundary where
  status : SupervisorStatus
  nextGenerationAuthorized : Bool
  terminalBlocks : isTerminal status = true → nextGenerationAuthorized = false


theorem terminal_state_blocks_automatic_continuation
    (boundary : ContinuationBoundary)
    (terminal : isTerminal boundary.status = true) :
    boundary.nextGenerationAuthorized = false := by
  exact boundary.terminalBlocks terminal

structure StopSignals where
  handoverRequest : Bool
  boundaryReached : Bool
  missionComplete : Bool
  maximumReached : Bool
  converged : Bool
  stagnated : Bool
  oscillating : Bool
  observationDebtHigh : Bool
  recoveryProtectionHigh : Bool


def chooseMultiGenerationDecision
    (signals : StopSignals) : MultiGenerationDecision :=
  if signals.handoverRequest then .handoverRequested
  else if signals.boundaryReached then .handoverBoundary
  else if signals.missionComplete then .stopMissionComplete
  else if signals.maximumReached then .stopMaximum
  else if signals.converged then .stopConverged
  else if signals.stagnated then .stopStagnation
  else if signals.oscillating then .stopOscillation
  else if signals.observationDebtHigh then .holdObservationDebt
  else if signals.recoveryProtectionHigh then .holdRecovery
  else .continue


theorem handover_request_has_highest_priority
    (signals : StopSignals)
    (requested : signals.handoverRequest = true) :
    chooseMultiGenerationDecision signals = .handoverRequested := by
  simp [chooseMultiGenerationDecision, requested]


theorem boundary_precedes_lower_priority_stops
    (signals : StopSignals)
    (notRequested : signals.handoverRequest = false)
    (boundary : signals.boundaryReached = true) :
    chooseMultiGenerationDecision signals = .handoverBoundary := by
  simp [chooseMultiGenerationDecision, notRequested, boundary]


theorem no_signal_means_continue
    (signals : StopSignals)
    (hRequest : signals.handoverRequest = false)
    (hBoundary : signals.boundaryReached = false)
    (hMission : signals.missionComplete = false)
    (hMaximum : signals.maximumReached = false)
    (hConverged : signals.converged = false)
    (hStagnated : signals.stagnated = false)
    (hOscillating : signals.oscillating = false)
    (hDebt : signals.observationDebtHigh = false)
    (hRecovery : signals.recoveryProtectionHigh = false) :
    chooseMultiGenerationDecision signals = .continue := by
  simp [chooseMultiGenerationDecision, hRequest, hBoundary, hMission,
    hMaximum, hConverged, hStagnated, hOscillating, hDebt, hRecovery]

structure MultiGenerationAuthorityBoundary where
  executionGranted : Bool
  hostLicenseGranted : Bool
  memoryOverwrite : Bool
  executionForbidden : executionGranted = false
  hostLicenseForbidden : hostLicenseGranted = false
  overwriteForbidden : memoryOverwrite = false


theorem multi_generation_supervisor_grants_no_authority
    (boundary : MultiGenerationAuthorityBoundary) :
    boundary.executionGranted = false ∧
      boundary.hostLicenseGranted = false ∧
      boundary.memoryOverwrite = false := by
  exact ⟨boundary.executionForbidden, boundary.hostLicenseForbidden,
    boundary.overwriteForbidden⟩

structure MultiGenerationOwnership where
  replanOwnedByPlanOS : Bool
  selectionOwnedByDecisionOS : Bool
  executionOwnedByActOS : Bool
  replanRequired : replanOwnedByPlanOS = true
  selectionRequired : selectionOwnedByDecisionOS = true
  executionRequired : executionOwnedByActOS = true


theorem multi_generation_supervisor_preserves_os_ownership
    (ownership : MultiGenerationOwnership) :
    ownership.replanOwnedByPlanOS = true ∧
      ownership.selectionOwnedByDecisionOS = true ∧
      ownership.executionOwnedByActOS = true := by
  exact ⟨ownership.replanRequired, ownership.selectionRequired,
    ownership.executionRequired⟩

structure MultiGenerationRecovery where
  committedGenerations : Nat
  recoveredGenerations : Nat
  recoveryRequired : recoveredGenerations = committedGenerations


theorem multi_generation_recovery_preserves_count
    (recovery : MultiGenerationRecovery) :
    recovery.recoveredGenerations = recovery.committedGenerations := by
  exact recovery.recoveryRequired

end KUOS.PlanOS
