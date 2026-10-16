import Mathlib
import KUOS.PlanOS.QiConditionedNonMarkovReplanV0_2
import KUOS.PlanOS.NextCycleBasisCompilerAdapterV0_3
import KUOS.LearnOS.ReplanLineageFutureOnlyLearningEnvelopeV0_2

namespace KUOS.PlanOS

structure ClosedLoopSourceIdentity where
  compiledPlanDigest : Nat
  currentPlanDigest : Nat
  committedLearnDigest : Nat
  intakeLearnDigest : Nat
  compilerIdentityRequired : compiledPlanDigest = currentPlanDigest
  learningIdentityRequired : committedLearnDigest = intakeLearnDigest


theorem closed_loop_preserves_source_identity
    (source : ClosedLoopSourceIdentity) :
    source.compiledPlanDigest = source.currentPlanDigest ∧
      source.committedLearnDigest = source.intakeLearnDigest := by
  exact ⟨source.compilerIdentityRequired, source.learningIdentityRequired⟩

structure ClosedLoopCycleGate where
  compilerCycle : Nat
  learnCycle : Nat
  intakeCycle : Nat
  activeFromCycle : Nat
  compilerRequired : intakeCycle = compilerCycle
  learnRequired : intakeCycle = learnCycle
  successorRequired : activeFromCycle = intakeCycle + 1


theorem closed_loop_uses_exact_cycle_and_successor
    (gate : ClosedLoopCycleGate) :
    gate.intakeCycle = gate.compilerCycle ∧
      gate.intakeCycle = gate.learnCycle ∧
      gate.activeFromCycle = gate.intakeCycle + 1 := by
  exact ⟨gate.compilerRequired, gate.learnRequired, gate.successorRequired⟩

structure ClosedLoopRuntimeLineage where
  compilerReceiptPreserved : Bool
  actCompletionPreserved : Bool
  observeCompletionPreserved : Bool
  verifyCompletionPreserved : Bool
  learnCompletionPreserved : Bool
  qiConditionPreserved : Bool
  decisionReceiptPreserved : Bool
  compilerRequired : compilerReceiptPreserved = true
  actRequired : actCompletionPreserved = true
  observeRequired : observeCompletionPreserved = true
  verifyRequired : verifyCompletionPreserved = true
  learnRequired : learnCompletionPreserved = true
  qiRequired : qiConditionPreserved = true
  decisionRequired : decisionReceiptPreserved = true


theorem closed_loop_preserves_runtime_lineage
    (lineage : ClosedLoopRuntimeLineage) :
    lineage.compilerReceiptPreserved = true ∧
      lineage.actCompletionPreserved = true ∧
      lineage.observeCompletionPreserved = true ∧
      lineage.verifyCompletionPreserved = true ∧
      lineage.learnCompletionPreserved = true ∧
      lineage.qiConditionPreserved = true ∧
      lineage.decisionReceiptPreserved = true := by
  exact ⟨lineage.compilerRequired, lineage.actRequired,
    lineage.observeRequired, lineage.verifyRequired,
    lineage.learnRequired, lineage.qiRequired, lineage.decisionRequired⟩

structure ClosedLoopBindState where
  phaseIsBind : Bool
  eventIndex : Nat
  historyRequired : Bool
  phaseRequired : phaseIsBind = true
  pristineRequired : eventIndex = 0
  historyRequiredProof : historyRequired = true


theorem closed_loop_enters_pristine_bind
    (state : ClosedLoopBindState) :
    state.phaseIsBind = true ∧ state.eventIndex = 0 ∧
      state.historyRequired = true := by
  exact ⟨state.phaseRequired, state.pristineRequired,
    state.historyRequiredProof⟩

structure ClosedLoopFutureBoundary where
  futureOnly : Bool
  activeNow : Bool
  currentCycleUnchanged : Bool
  pastPlanUnchanged : Bool
  memoryOverwrite : Bool
  futureOnlyRequired : futureOnly = true
  activeNowForbidden : activeNow = false
  currentCycleRequired : currentCycleUnchanged = true
  pastPlanRequired : pastPlanUnchanged = true
  overwriteForbidden : memoryOverwrite = false


theorem closed_loop_bind_is_future_only
    (boundary : ClosedLoopFutureBoundary) :
    boundary.futureOnly = true ∧ boundary.activeNow = false ∧
      boundary.currentCycleUnchanged = true ∧
      boundary.pastPlanUnchanged = true ∧
      boundary.memoryOverwrite = false := by
  exact ⟨boundary.futureOnlyRequired, boundary.activeNowForbidden,
    boundary.currentCycleRequired, boundary.pastPlanRequired,
    boundary.overwriteForbidden⟩

structure ClosedLoopOwnership where
  replanOwnedByPlanOS : Bool
  selectionOwnedByDecisionOS : Bool
  executionOwnedByActOS : Bool
  replanRequired : replanOwnedByPlanOS = true
  selectionRequired : selectionOwnedByDecisionOS = true
  executionRequired : executionOwnedByActOS = true


theorem closed_loop_preserves_os_ownership
    (ownership : ClosedLoopOwnership) :
    ownership.replanOwnedByPlanOS = true ∧
      ownership.selectionOwnedByDecisionOS = true ∧
      ownership.executionOwnedByActOS = true := by
  exact ⟨ownership.replanRequired, ownership.selectionRequired,
    ownership.executionRequired⟩

structure ClosedLoopActivationSeparation where
  intakeCommitted : Bool
  bindCommitted : Bool
  replanActivated : Bool
  planActivated : Bool
  executionPermitted : Bool
  hostLicenseGranted : Bool
  intakeRequired : intakeCommitted = true
  bindRequired : bindCommitted = true
  replanForbidden : replanActivated = false
  planForbidden : planActivated = false
  executionForbidden : executionPermitted = false
  hostLicenseForbidden : hostLicenseGranted = false


theorem closed_loop_bind_is_not_activation_or_execution
    (s : ClosedLoopActivationSeparation) :
    s.intakeCommitted = true ∧ s.bindCommitted = true ∧
      s.replanActivated = false ∧ s.planActivated = false ∧
      s.executionPermitted = false ∧ s.hostLicenseGranted = false := by
  exact ⟨s.intakeRequired, s.bindRequired, s.replanForbidden,
    s.planForbidden, s.executionForbidden, s.hostLicenseForbidden⟩

structure ClosedLoopSingleUse where
  intakeCount : Nat
  bindCount : Nat
  intakeBound : intakeCount ≤ 1
  bindBound : bindCount ≤ intakeCount


theorem closed_loop_bind_is_single_use
    (single : ClosedLoopSingleUse) : single.bindCount ≤ 1 := by
  exact le_trans single.bindBound single.intakeBound

structure ClosedLoopRecovery where
  committedRecords : Nat
  recoveredRecords : Nat
  recoveryRequired : recoveredRecords = committedRecords


theorem closed_loop_recovery_eq_commit_count
    (recovery : ClosedLoopRecovery) :
    recovery.recoveredRecords = recovery.committedRecords := by
  exact recovery.recoveryRequired

end KUOS.PlanOS
