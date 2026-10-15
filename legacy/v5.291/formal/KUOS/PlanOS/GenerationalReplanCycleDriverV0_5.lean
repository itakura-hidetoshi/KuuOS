import Mathlib
import KUOS.PlanOS.ClosedLoopReplanIntakeAdapterV0_4
import KUOS.PlanOS.QiConditionedNonMarkovReplanV0_2
import KUOS.PlanOS.NextCycleBasisCompilerAdapterV0_3
import KUOS.ActOS.ReplanLineageAuthorityEnvelopeV0_2

namespace KUOS.PlanOS

inductive GenerationalPhase where
  | history
  | qiCondition
  | generate
  | constrain
  | deliberate
  | synthesize
  | commitNext
  deriving DecidableEq


def generationalPhaseSequence : List GenerationalPhase :=
  [.history, .qiCondition, .generate, .constrain,
    .deliberate, .synthesize, .commitNext]


theorem generational_phase_sequence_length :
    generationalPhaseSequence.length = 7 := by
  rfl

structure GenerationalCycle where
  sourceCycle : Nat
  nextCycle : Nat
  successorRequired : nextCycle = sourceCycle + 1


theorem generational_cycle_is_exact_successor
    (cycle : GenerationalCycle) :
    cycle.nextCycle = cycle.sourceCycle + 1 := by
  exact cycle.successorRequired

structure GenerationalLineage where
  sourcePlanDigest : Nat
  bindPlanDigest : Nat
  replanSourceDigest : Nat
  compilerPreviousDigest : Nat
  planBindRequired : sourcePlanDigest = bindPlanDigest
  replanBindRequired : replanSourceDigest = bindPlanDigest
  compilerRequired : compilerPreviousDigest = sourcePlanDigest


theorem generational_lineage_preserves_source_plan
    (lineage : GenerationalLineage) :
    lineage.sourcePlanDigest = lineage.bindPlanDigest ∧
      lineage.replanSourceDigest = lineage.bindPlanDigest ∧
      lineage.compilerPreviousDigest = lineage.sourcePlanDigest := by
  exact ⟨lineage.planBindRequired, lineage.replanBindRequired,
    lineage.compilerRequired⟩

structure GenerationalSelectionIdentity where
  decisionCandidateDigest : Nat
  replanCandidateDigest : Nat
  compilerCandidateDigest : Nat
  actCandidateDigest : Nat
  replanRequired : decisionCandidateDigest = replanCandidateDigest
  compilerRequired : compilerCandidateDigest = replanCandidateDigest
  actRequired : actCandidateDigest = compilerCandidateDigest


theorem generational_selection_identity_is_transitive
    (identity : GenerationalSelectionIdentity) :
    identity.decisionCandidateDigest = identity.actCandidateDigest := by
  calc
    identity.decisionCandidateDigest = identity.replanCandidateDigest :=
      identity.replanRequired
    _ = identity.compilerCandidateDigest := identity.compilerRequired.symm
    _ = identity.actCandidateDigest := identity.actRequired.symm

structure GenerationalCompilation where
  replanBasisDigest : Nat
  compilerBasisDigest : Nat
  compiledPlanBasisDigest : Nat
  compilerInputRequired : compilerBasisDigest = replanBasisDigest
  compiledRequired : compiledPlanBasisDigest = compilerBasisDigest


theorem generational_compiler_preserves_next_basis
    (compilation : GenerationalCompilation) :
    compilation.compiledPlanBasisDigest = compilation.replanBasisDigest := by
  exact compilation.compiledRequired.trans compilation.compilerInputRequired

structure GenerationalActHandoff where
  compilerReceiptDigest : Nat
  actCompilerReceiptDigest : Nat
  compiledPlanDigest : Nat
  actPlanDigest : Nat
  compilerRequired : actCompilerReceiptDigest = compilerReceiptDigest
  planRequired : actPlanDigest = compiledPlanDigest


theorem generational_act_handoff_preserves_compiler_and_plan
    (handoff : GenerationalActHandoff) :
    handoff.actCompilerReceiptDigest = handoff.compilerReceiptDigest ∧
      handoff.actPlanDigest = handoff.compiledPlanDigest := by
  exact ⟨handoff.compilerRequired, handoff.planRequired⟩

structure GenerationalAuthorityBoundary where
  executionGranted : Bool
  hostLicenseGranted : Bool
  memoryOverwrite : Bool
  currentCycleUnchanged : Bool
  pastPlanUnchanged : Bool
  executionForbidden : executionGranted = false
  hostLicenseForbidden : hostLicenseGranted = false
  overwriteForbidden : memoryOverwrite = false
  currentCycleRequired : currentCycleUnchanged = true
  pastPlanRequired : pastPlanUnchanged = true


theorem generational_cycle_grants_no_execution_or_mutation
    (boundary : GenerationalAuthorityBoundary) :
    boundary.executionGranted = false ∧
      boundary.hostLicenseGranted = false ∧
      boundary.memoryOverwrite = false ∧
      boundary.currentCycleUnchanged = true ∧
      boundary.pastPlanUnchanged = true := by
  exact ⟨boundary.executionForbidden, boundary.hostLicenseForbidden,
    boundary.overwriteForbidden, boundary.currentCycleRequired,
    boundary.pastPlanRequired⟩

structure GenerationalOwnership where
  replanOwnedByPlanOS : Bool
  selectionOwnedByDecisionOS : Bool
  executionOwnedByActOS : Bool
  replanRequired : replanOwnedByPlanOS = true
  selectionRequired : selectionOwnedByDecisionOS = true
  executionRequired : executionOwnedByActOS = true


theorem generational_cycle_preserves_os_ownership
    (ownership : GenerationalOwnership) :
    ownership.replanOwnedByPlanOS = true ∧
      ownership.selectionOwnedByDecisionOS = true ∧
      ownership.executionOwnedByActOS = true := by
  exact ⟨ownership.replanRequired, ownership.selectionRequired,
    ownership.executionRequired⟩

structure GenerationalSingleUse where
  sourceGenerationCount : Nat
  committedGenerationCount : Nat
  sourceBound : sourceGenerationCount ≤ 1
  commitBound : committedGenerationCount ≤ sourceGenerationCount


theorem generational_source_is_consumed_at_most_once
    (single : GenerationalSingleUse) :
    single.committedGenerationCount ≤ 1 := by
  exact le_trans single.commitBound single.sourceBound

structure GenerationalRecovery where
  committedGenerations : Nat
  recoveredGenerations : Nat
  recoveryRequired : recoveredGenerations = committedGenerations


theorem generational_recovery_preserves_generation_count
    (recovery : GenerationalRecovery) :
    recovery.recoveredGenerations = recovery.committedGenerations := by
  exact recovery.recoveryRequired

end KUOS.PlanOS
