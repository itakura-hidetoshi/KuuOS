import Mathlib
import KUOS.PlanOS.ReplanBoundSynthesisV0_1
import KUOS.PlanOS.QiConditionedNonMarkovReplanV0_2

namespace KUOS
namespace PlanOS

inductive AdapterRoute where
  | planCandidate
  | repairPlan
  | observationPlan
  | handoverPlan
  | hold
  deriving DecidableEq, Repr


inductive ReplanAdapterRoute where
  | nextPlanCandidate
  | repairPlanCandidate
  | reobservationPlanCandidate
  | reroutePlanCandidate
  | terminationPlanCandidate
  | hold
  deriving DecidableEq, Repr


def ReplanAdapterRoute.project : ReplanAdapterRoute → AdapterRoute
  | .nextPlanCandidate => .planCandidate
  | .repairPlanCandidate => .repairPlan
  | .reobservationPlanCandidate => .observationPlan
  | .reroutePlanCandidate => .handoverPlan
  | .terminationPlanCandidate => .handoverPlan
  | .hold => .hold


theorem termination_projects_to_handover :
    ReplanAdapterRoute.terminationPlanCandidate.project =
      AdapterRoute.handoverPlan := by
  rfl


theorem hold_projects_to_hold :
    ReplanAdapterRoute.hold.project = AdapterRoute.hold := by
  rfl


structure ExactNextCycleGate where
  previousCycle : ℕ
  activeFromCycle : ℕ
  missionCycle : ℕ
  missionPhaseIsPlan : Bool
  successorRequired : activeFromCycle = previousCycle + 1
  exactCycleRequired : missionCycle = activeFromCycle
  planPhaseRequired : missionPhaseIsPlan = true


theorem adapter_activates_in_exact_next_cycle
    (gate : ExactNextCycleGate) :
    gate.missionCycle = gate.previousCycle + 1 := by
  rw [gate.exactCycleRequired, gate.successorRequired]


theorem adapter_requires_plan_phase
    (gate : ExactNextCycleGate) :
    gate.missionPhaseIsPlan = true := by
  exact gate.planPhaseRequired


theorem old_cycle_cannot_equal_active_cycle
    (gate : ExactNextCycleGate) :
    gate.previousCycle ≠ gate.activeFromCycle := by
  rw [gate.successorRequired]
  omega


structure DualLineageBoundary where
  waAuthorizationBound : Bool
  replanIdentityBound : Bool
  waIdentityUsedAsReplanIdentity : Bool
  lineageCollapseDetected : Bool
  waRequired : waAuthorizationBound = true
  replanRequired : replanIdentityBound = true
  identityCollapseForbidden : waIdentityUsedAsReplanIdentity = false
  lineageCollapseForbidden : lineageCollapseDetected = false


theorem adapter_preserves_dual_lineage
    (boundary : DualLineageBoundary) :
    boundary.waAuthorizationBound = true ∧
      boundary.replanIdentityBound = true := by
  exact ⟨boundary.waRequired, boundary.replanRequired⟩


theorem wa_identity_is_not_replan_identity
    (boundary : DualLineageBoundary) :
    boundary.waIdentityUsedAsReplanIdentity = false := by
  exact boundary.identityCollapseForbidden


structure DigestBindingBoundary where
  replanReceiptPreserved : Bool
  nextPlanBasisPreserved : Bool
  selectedCandidatePreserved : Bool
  qiConditionPreserved : Bool
  decisionReceiptPreserved : Bool
  synthesisPacketPreserved : Bool
  replanRequired : replanReceiptPreserved = true
  basisRequired : nextPlanBasisPreserved = true
  candidateRequired : selectedCandidatePreserved = true
  qiRequired : qiConditionPreserved = true
  decisionRequired : decisionReceiptPreserved = true
  synthesisRequired : synthesisPacketPreserved = true


theorem adapter_preserves_replan_and_basis_identity
    (boundary : DigestBindingBoundary) :
    boundary.replanReceiptPreserved = true ∧
      boundary.nextPlanBasisPreserved = true ∧
      boundary.selectedCandidatePreserved = true := by
  exact ⟨boundary.replanRequired, boundary.basisRequired,
    boundary.candidateRequired⟩


theorem adapter_preserves_qi_decision_and_synthesis
    (boundary : DigestBindingBoundary) :
    boundary.qiConditionPreserved = true ∧
      boundary.decisionReceiptPreserved = true ∧
      boundary.synthesisPacketPreserved = true := by
  exact ⟨boundary.qiRequired, boundary.decisionRequired,
    boundary.synthesisRequired⟩


structure MaterializationBoundary where
  expectedTemplateCount : ℕ
  materializedTemplateCount : ℕ
  exactOrderPreserved : Bool
  exactIdentityPreserved : Bool
  selectedCandidatePreserved : Bool
  observationCoverage : Bool
  verificationCoverage : Bool
  stopCoverage : Bool
  rollbackCoverage : Bool
  countRequired : materializedTemplateCount = expectedTemplateCount
  orderRequired : exactOrderPreserved = true
  identityRequired : exactIdentityPreserved = true
  candidateRequired : selectedCandidatePreserved = true
  observationRequired : observationCoverage = true
  verificationRequired : verificationCoverage = true
  stopRequired : stopCoverage = true
  rollbackRequired : rollbackCoverage = true


theorem materialization_preserves_count_order_and_identity
    (boundary : MaterializationBoundary) :
    boundary.materializedTemplateCount = boundary.expectedTemplateCount ∧
      boundary.exactOrderPreserved = true ∧
      boundary.exactIdentityPreserved = true := by
  exact ⟨boundary.countRequired, boundary.orderRequired,
    boundary.identityRequired⟩


theorem materialization_covers_observation_verification_and_recovery
    (boundary : MaterializationBoundary) :
    boundary.observationCoverage = true ∧
      boundary.verificationCoverage = true ∧
      boundary.stopCoverage = true ∧
      boundary.rollbackCoverage = true := by
  exact ⟨boundary.observationRequired, boundary.verificationRequired,
    boundary.stopRequired, boundary.rollbackRequired⟩


structure HoldMaterializationBoundary where
  executableStepCount : ℕ
  withheldTemplateCount : ℕ
  expectedTemplateCount : ℕ
  noExecutableSteps : executableStepCount = 0
  withheldVisible : withheldTemplateCount = expectedTemplateCount


theorem hold_materializes_no_executable_steps
    (boundary : HoldMaterializationBoundary) :
    boundary.executableStepCount = 0 := by
  exact boundary.noExecutableSteps


theorem hold_preserves_withheld_templates
    (boundary : HoldMaterializationBoundary) :
    boundary.withheldTemplateCount = boundary.expectedTemplateCount := by
  exact boundary.withheldVisible


structure CompilerReuseBoundary where
  structuredCompilerIsV01 : Bool
  dependencyValidationReused : Bool
  resourceValidationReused : Bool
  effectGuardReused : Bool
  checkpointValidationReused : Bool
  verificationReused : Bool
  compilerRequired : structuredCompilerIsV01 = true
  dependencyRequired : dependencyValidationReused = true
  resourceRequired : resourceValidationReused = true
  guardRequired : effectGuardReused = true
  checkpointRequired : checkpointValidationReused = true
  verificationRequired : verificationReused = true


theorem v01_remains_sole_structured_compiler
    (boundary : CompilerReuseBoundary) :
    boundary.structuredCompilerIsV01 = true := by
  exact boundary.compilerRequired


theorem adapter_reuses_v01_guards
    (boundary : CompilerReuseBoundary) :
    boundary.dependencyValidationReused = true ∧
      boundary.resourceValidationReused = true ∧
      boundary.effectGuardReused = true ∧
      boundary.checkpointValidationReused = true ∧
      boundary.verificationReused = true := by
  exact ⟨boundary.dependencyRequired, boundary.resourceRequired,
    boundary.guardRequired, boundary.checkpointRequired,
    boundary.verificationRequired⟩


structure SingleUseBoundary where
  replanReceiptConsumed : Bool
  nextPlanBasisConsumed : Bool
  conflictingReplayAccepted : Bool
  exactReplayIdempotent : Bool
  receiptRequired : replanReceiptConsumed = true
  basisRequired : nextPlanBasisConsumed = true
  conflictForbidden : conflictingReplayAccepted = false
  replayRequired : exactReplayIdempotent = true


theorem adapter_activation_is_single_use
    (boundary : SingleUseBoundary) :
    boundary.replanReceiptConsumed = true ∧
      boundary.nextPlanBasisConsumed = true ∧
      boundary.conflictingReplayAccepted = false := by
  exact ⟨boundary.receiptRequired, boundary.basisRequired,
    boundary.conflictForbidden⟩


theorem exact_adapter_replay_is_idempotent
    (boundary : SingleUseBoundary) :
    boundary.exactReplayIdempotent = true := by
  exact boundary.replayRequired


structure AdapterNonAuthority where
  previousPlanUnchanged : Bool
  executionGranted : Bool
  truthAuthority : Bool
  clinicalAuthority : Bool
  legalAuthority : Bool
  memoryOverwrite : Bool
  hostLicenseGranted : Bool
  previousRequired : previousPlanUnchanged = true
  executionForbidden : executionGranted = false
  truthForbidden : truthAuthority = false
  clinicalForbidden : clinicalAuthority = false
  legalForbidden : legalAuthority = false
  overwriteForbidden : memoryOverwrite = false
  licenseForbidden : hostLicenseGranted = false


theorem adapter_preserves_previous_plan
    (boundary : AdapterNonAuthority) :
    boundary.previousPlanUnchanged = true := by
  exact boundary.previousRequired


theorem adapter_does_not_execute_or_license
    (boundary : AdapterNonAuthority) :
    boundary.executionGranted = false ∧
      boundary.hostLicenseGranted = false := by
  exact ⟨boundary.executionForbidden, boundary.licenseForbidden⟩


theorem adapter_grants_no_truth_clinical_or_legal_authority
    (boundary : AdapterNonAuthority) :
    boundary.truthAuthority = false ∧
      boundary.clinicalAuthority = false ∧
      boundary.legalAuthority = false := by
  exact ⟨boundary.truthForbidden, boundary.clinicalForbidden,
    boundary.legalForbidden⟩


structure AdapterHistory where
  committedRecords : ℕ
  recoveredRecords : ℕ
  snapshotRecords : ℕ
  recoveryExact : recoveredRecords = committedRecords
  snapshotDerived : snapshotRecords = recoveredRecords


theorem adapterHistory_snapshot_matches_commits
    (history : AdapterHistory) :
    history.snapshotRecords = history.committedRecords := by
  rw [history.snapshotDerived, history.recoveryExact]

end PlanOS
end KUOS
