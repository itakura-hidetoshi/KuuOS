import Mathlib
import KUOS.PlanOS.ReplanBoundSynthesisV0_1
import KUOS.LearnOS.FutureOnlyEvidenceLearningV0_1

namespace KUOS
namespace PlanOS

inductive ReplanPhase where
  | bind
  | history
  | qiCondition
  | generate
  | constrain
  | deliberate
  | synthesize
  | commitNext
  deriving DecidableEq, Repr


def ReplanPhase.next : ReplanPhase → Option ReplanPhase
  | .bind => some .history
  | .history => some .qiCondition
  | .qiCondition => some .generate
  | .generate => some .constrain
  | .constrain => some .deliberate
  | .deliberate => some .synthesize
  | .synthesize => some .commitNext
  | .commitNext => none


theorem replanPhase_next_deterministic
    (phase left right : ReplanPhase)
    (hleft : phase.next = some left)
    (hright : phase.next = some right) :
    left = right := by
  rw [hleft] at hright
  exact Option.some.inj hright


theorem replanPhase_bind_next :
    ReplanPhase.bind.next = some ReplanPhase.history := by
  rfl


theorem replanPhase_synthesize_next :
    ReplanPhase.synthesize.next = some ReplanPhase.commitNext := by
  rfl


structure ReplanEventIndex where
  current : ℕ


def ReplanEventIndex.append (index : ReplanEventIndex) : ReplanEventIndex where
  current := index.current + 1


theorem replanEventIndex_strict
    (index : ReplanEventIndex) :
    index.current < index.append.current := by
  simp [ReplanEventIndex.append]


structure ReplanOwnership where
  replanOwnedByPlanOS : Bool
  selectionOwnedByDecisionOS : Bool
  synthesisOwnedByPlanOS : Bool
  executionOwnedByActOS : Bool
  replanOwnerRequired : replanOwnedByPlanOS = true
  selectionOwnerRequired : selectionOwnedByDecisionOS = true
  synthesisOwnerRequired : synthesisOwnedByPlanOS = true
  executionOwnerRequired : executionOwnedByActOS = true


theorem replan_belongs_to_planOS
    (ownership : ReplanOwnership) :
    ownership.replanOwnedByPlanOS = true := by
  exact ownership.replanOwnerRequired


theorem decisionOS_selects_planOS_synthesizes
    (ownership : ReplanOwnership) :
    ownership.selectionOwnedByDecisionOS = true ∧
      ownership.synthesisOwnedByPlanOS = true := by
  exact ⟨ownership.selectionOwnerRequired, ownership.synthesisOwnerRequired⟩


theorem actOS_remains_execution_owner
    (ownership : ReplanOwnership) :
    ownership.executionOwnedByActOS = true := by
  exact ownership.executionOwnerRequired


structure ReplanSourceBinding where
  committedCurrentPlan : Bool
  committedLearnState : Bool
  sameMissionContract : Bool
  learningDeltaBound : Bool
  middleWayReportBound : Bool
  verificationEvidenceBound : Bool
  futureOnlyLearning : Bool
  learningInactiveNow : Bool
  replanRequiredByLearnOS : Bool
  currentPlanRequired : committedCurrentPlan = true
  learnStateRequired : committedLearnState = true
  missionRequired : sameMissionContract = true
  deltaRequired : learningDeltaBound = true
  middleWayRequired : middleWayReportBound = true
  evidenceRequired : verificationEvidenceBound = true
  futureRequired : futureOnlyLearning = true
  inactiveRequired : learningInactiveNow = true
  replanDebtRequired : replanRequiredByLearnOS = true


theorem replan_requires_committed_plan_and_learning
    (binding : ReplanSourceBinding) :
    binding.committedCurrentPlan = true ∧
      binding.committedLearnState = true := by
  exact ⟨binding.currentPlanRequired, binding.learnStateRequired⟩


theorem replan_preserves_learning_lineage
    (binding : ReplanSourceBinding) :
    binding.learningDeltaBound = true ∧
      binding.middleWayReportBound = true ∧
      binding.verificationEvidenceBound = true := by
  exact ⟨binding.deltaRequired, binding.middleWayRequired, binding.evidenceRequired⟩


theorem learn_delta_is_not_replan_activation
    (binding : ReplanSourceBinding) :
    binding.futureOnlyLearning = true ∧
      binding.learningInactiveNow = true ∧
      binding.replanRequiredByLearnOS = true := by
  exact ⟨binding.futureRequired, binding.inactiveRequired,
    binding.replanDebtRequired⟩


structure NonMarkovHistoryBoundary where
  currentPlanBound : Bool
  previousPlanChangesVisible : Bool
  successfulTransitionsVisible : Bool
  failedTransitionsVisible : Bool
  oscillationHistoryVisible : Bool
  recoveryHistoryVisible : Bool
  stagnationHistoryVisible : Bool
  actionHistoryVisible : Bool
  observationHistoryVisible : Bool
  verificationHistoryVisible : Bool
  learningHistoryVisible : Bool
  pathDependenceVisible : Bool
  sourceHistoryMutation : Bool
  currentRequired : currentPlanBound = true
  changesRequired : previousPlanChangesVisible = true
  successRequired : successfulTransitionsVisible = true
  failureRequired : failedTransitionsVisible = true
  oscillationRequired : oscillationHistoryVisible = true
  recoveryRequired : recoveryHistoryVisible = true
  stagnationRequired : stagnationHistoryVisible = true
  actionRequired : actionHistoryVisible = true
  observationRequired : observationHistoryVisible = true
  verificationRequired : verificationHistoryVisible = true
  learningRequired : learningHistoryVisible = true
  pathRequired : pathDependenceVisible = true
  mutationForbidden : sourceHistoryMutation = false


theorem replan_is_nonMarkov
    (history : NonMarkovHistoryBoundary) :
    history.previousPlanChangesVisible = true ∧
      history.oscillationHistoryVisible = true ∧
      history.recoveryHistoryVisible = true ∧
      history.stagnationHistoryVisible = true ∧
      history.pathDependenceVisible = true := by
  exact ⟨history.changesRequired, history.oscillationRequired,
    history.recoveryRequired, history.stagnationRequired,
    history.pathRequired⟩


theorem replan_history_is_read_only
    (history : NonMarkovHistoryBoundary) :
    history.sourceHistoryMutation = false := by
  exact history.mutationForbidden


structure QiReplanBoundary where
  processTensorBound : Bool
  processHistoryBound : Bool
  activationVisible : Bool
  stagnationVisible : Bool
  tensionVisible : Bool
  recoveryVisible : Bool
  coherenceVisible : Bool
  couplingVisible : Bool
  transitionReadinessVisible : Bool
  localGlobalBalanceVisible : Bool
  observationDebtVisible : Bool
  hysteresisVisible : Bool
  memoryHorizonVisible : Bool
  qiContextOnly : Bool
  qiTruthAuthority : Bool
  qiCausalAuthority : Bool
  qiExecutionAuthority : Bool
  qiClinicalAuthority : Bool
  qiActivatesPlan : Bool
  tensorRequired : processTensorBound = true
  historyRequired : processHistoryBound = true
  transitionRequired : transitionReadinessVisible = true
  hysteresisRequired : hysteresisVisible = true
  contextRequired : qiContextOnly = true
  truthForbidden : qiTruthAuthority = false
  causalForbidden : qiCausalAuthority = false
  executionForbidden : qiExecutionAuthority = false
  clinicalForbidden : qiClinicalAuthority = false
  activationForbidden : qiActivatesPlan = false


theorem qi_conditions_replan
    (boundary : QiReplanBoundary) :
    boundary.processTensorBound = true ∧
      boundary.processHistoryBound = true ∧
      boundary.transitionReadinessVisible = true ∧
      boundary.hysteresisVisible = true := by
  exact ⟨boundary.tensorRequired, boundary.historyRequired,
    boundary.transitionRequired, boundary.hysteresisRequired⟩


theorem qi_grants_no_replan_authority
    (boundary : QiReplanBoundary) :
    boundary.qiTruthAuthority = false ∧
      boundary.qiCausalAuthority = false ∧
      boundary.qiExecutionAuthority = false ∧
      boundary.qiClinicalAuthority = false := by
  exact ⟨boundary.truthForbidden, boundary.causalForbidden,
    boundary.executionForbidden, boundary.clinicalForbidden⟩


theorem qi_cannot_activate_plan
    (boundary : QiReplanBoundary) :
    boundary.qiActivatesPlan = false := by
  exact boundary.activationForbidden


inductive ReplanCandidateType where
  | continuePlan
  | strengthen
  | repair
  | slowDown
  | reobserve
  | reroute
  | hold
  | terminateCandidate
  deriving DecidableEq, Repr


structure HysteresisGate where
  candidateType : ReplanCandidateType
  switchBenefit : ℚ
  baseSwitchThreshold : ℚ
  qiHysteresis : ℚ
  oscillationPenalty : ℚ
  recoveryProtectionPenalty : ℚ
  switchExempt : Bool
  hysteresisPassed : Bool
  requiredMargin : ℚ
  requiredMarginEq :
    requiredMargin =
      baseSwitchThreshold + qiHysteresis + oscillationPenalty +
        recoveryProtectionPenalty
  switchedRule : switchExempt = false → hysteresisPassed = true →
    requiredMargin ≤ switchBenefit
  exemptRule : switchExempt = true → hysteresisPassed = true


theorem switching_candidate_requires_hysteresis_margin
    (gate : HysteresisGate)
    (hnotExempt : gate.switchExempt = false)
    (hpassed : gate.hysteresisPassed = true) :
    gate.baseSwitchThreshold + gate.qiHysteresis + gate.oscillationPenalty +
      gate.recoveryProtectionPenalty ≤ gate.switchBenefit := by
  rw [← gate.requiredMarginEq]
  exact gate.switchedRule hnotExempt hpassed


theorem exempt_candidate_may_pass_without_switch_benefit
    (gate : HysteresisGate)
    (hexempt : gate.switchExempt = true) :
    gate.hysteresisPassed = true := by
  exact gate.exemptRule hexempt


structure ConstraintBoundary where
  missionInvariantsPreserved : Bool
  authorityBoundaryPreserved : Bool
  resourceEnvelopeSatisfied : Bool
  applicabilityConditionValid : Bool
  reversalConditionVisible : Bool
  expirationConditionValid : Bool
  observationDebtVisible : Bool
  verificationDebtVisible : Bool
  scopeCompatible : Bool
  qiTransitionReady : Bool
  hysteresisPassed : Bool
  admissible : Bool
  admissibilityRule : admissible = true →
    missionInvariantsPreserved = true ∧
      authorityBoundaryPreserved = true ∧
      resourceEnvelopeSatisfied = true ∧
      applicabilityConditionValid = true ∧
      reversalConditionVisible = true ∧
      expirationConditionValid = true ∧
      observationDebtVisible = true ∧
      verificationDebtVisible = true ∧
      scopeCompatible = true ∧
      qiTransitionReady = true ∧
      hysteresisPassed = true


theorem admissible_candidate_preserves_mission_and_authority
    (boundary : ConstraintBoundary)
    (hadmissible : boundary.admissible = true) :
    boundary.missionInvariantsPreserved = true ∧
      boundary.authorityBoundaryPreserved = true := by
  have h := boundary.admissibilityRule hadmissible
  exact ⟨h.1, h.2.1⟩


theorem admissible_candidate_passes_qi_and_hysteresis
    (boundary : ConstraintBoundary)
    (hadmissible : boundary.admissible = true) :
    boundary.qiTransitionReady = true ∧
      boundary.hysteresisPassed = true := by
  have h := boundary.admissibilityRule hadmissible
  exact ⟨h.2.2.2.2.2.2.2.2.2.1,
    h.2.2.2.2.2.2.2.2.2.2⟩


structure DecisionSelectionBoundary where
  allCandidatesConsidered : Bool
  selectedCandidateAdmissible : Bool
  selectedCandidateIdentityPreserved : Bool
  retainedAlternativesPreserved : Bool
  dissentVisible : Bool
  minorityPreserved : Bool
  decisionNotExecution : Bool
  silentSubstitutionDetected : Bool
  allRequired : allCandidatesConsidered = true
  admissibleRequired : selectedCandidateAdmissible = true
  identityRequired : selectedCandidateIdentityPreserved = true
  alternativesRequired : retainedAlternativesPreserved = true
  dissentRequired : dissentVisible = true
  minorityRequired : minorityPreserved = true
  executionForbidden : decisionNotExecution = true
  substitutionForbidden : silentSubstitutionDetected = false


theorem decisionOS_selection_is_admissible_and_preserved
    (selection : DecisionSelectionBoundary) :
    selection.selectedCandidateAdmissible = true ∧
      selection.selectedCandidateIdentityPreserved = true := by
  exact ⟨selection.admissibleRequired, selection.identityRequired⟩


theorem decision_selection_is_not_execution
    (selection : DecisionSelectionBoundary) :
    selection.decisionNotExecution = true := by
  exact selection.executionForbidden


theorem planOS_cannot_silently_substitute_decision
    (selection : DecisionSelectionBoundary) :
    selection.silentSubstitutionDetected = false := by
  exact selection.substitutionForbidden


structure NextCycleSynthesis where
  selectedCandidateBound : Bool
  decisionReceiptBound : Bool
  historyBound : Bool
  qiConditionBound : Bool
  learningDeltaBound : Bool
  missionContractBound : Bool
  currentCycle : ℕ
  activeFromCycle : ℕ
  futureOnly : Bool
  activeNow : Bool
  currentCycleUnchanged : Bool
  pastPlanUnchanged : Bool
  planNotExecution : Bool
  hostLicenseGranted : Bool
  selectedRequired : selectedCandidateBound = true
  decisionRequired : decisionReceiptBound = true
  historyRequired : historyBound = true
  qiRequired : qiConditionBound = true
  learningRequired : learningDeltaBound = true
  missionRequired : missionContractBound = true
  nextCycleRequired : activeFromCycle = currentCycle + 1
  futureRequired : futureOnly = true
  activationForbidden : activeNow = false
  currentRequired : currentCycleUnchanged = true
  pastRequired : pastPlanUnchanged = true
  executionForbidden : planNotExecution = true
  licenseForbidden : hostLicenseGranted = false


theorem synthesized_basis_starts_next_cycle
    (synthesis : NextCycleSynthesis) :
    synthesis.activeFromCycle = synthesis.currentCycle + 1 := by
  exact synthesis.nextCycleRequired


theorem synthesized_basis_is_future_only_and_inactive
    (synthesis : NextCycleSynthesis) :
    synthesis.futureOnly = true ∧ synthesis.activeNow = false := by
  exact ⟨synthesis.futureRequired, synthesis.activationForbidden⟩


theorem synthesis_preserves_current_and_past
    (synthesis : NextCycleSynthesis) :
    synthesis.currentCycleUnchanged = true ∧
      synthesis.pastPlanUnchanged = true := by
  exact ⟨synthesis.currentRequired, synthesis.pastRequired⟩


theorem synthesis_is_not_execution_or_license
    (synthesis : NextCycleSynthesis) :
    synthesis.planNotExecution = true ∧
      synthesis.hostLicenseGranted = false := by
  exact ⟨synthesis.executionForbidden, synthesis.licenseForbidden⟩


structure ReplanCommitBoundary where
  nextPlanBasisCommitted : Bool
  nextPlanPhaseRequired : Bool
  activeNow : Bool
  currentCycleUnchanged : Bool
  pastPlanUnchanged : Bool
  memoryOverwrite : Bool
  hostLicenseGranted : Bool
  committedRequired : nextPlanBasisCommitted = true
  nextPlanRequired : nextPlanPhaseRequired = true
  activationForbidden : activeNow = false
  currentRequired : currentCycleUnchanged = true
  pastRequired : pastPlanUnchanged = true
  overwriteForbidden : memoryOverwrite = false
  licenseForbidden : hostLicenseGranted = false


theorem replan_commit_requires_next_plan_phase
    (commit : ReplanCommitBoundary) :
    commit.nextPlanBasisCommitted = true ∧
      commit.nextPlanPhaseRequired = true := by
  exact ⟨commit.committedRequired, commit.nextPlanRequired⟩


theorem replan_commit_does_not_activate
    (commit : ReplanCommitBoundary) :
    commit.activeNow = false := by
  exact commit.activationForbidden


theorem replan_commit_preserves_current_and_past
    (commit : ReplanCommitBoundary) :
    commit.currentCycleUnchanged = true ∧
      commit.pastPlanUnchanged = true := by
  exact ⟨commit.currentRequired, commit.pastRequired⟩


structure ReplanNonAuthority where
  truthAuthority : Bool
  causalAuthority : Bool
  executionAuthority : Bool
  finalCommitmentAuthority : Bool
  memoryOverwriteAuthority : Bool
  selfModificationAuthority : Bool
  clinicalAuthority : Bool
  legalAuthority : Bool
  institutionalAuthority : Bool
  theoremAuthority : Bool
  hostLicense : Bool
  truthForbidden : truthAuthority = false
  causalForbidden : causalAuthority = false
  executionForbidden : executionAuthority = false
  finalForbidden : finalCommitmentAuthority = false
  overwriteForbidden : memoryOverwriteAuthority = false
  selfModificationForbidden : selfModificationAuthority = false
  clinicalForbidden : clinicalAuthority = false
  legalForbidden : legalAuthority = false
  institutionalForbidden : institutionalAuthority = false
  theoremForbidden : theoremAuthority = false
  licenseForbidden : hostLicense = false


theorem replan_grants_no_truth_causal_or_execution_authority
    (boundary : ReplanNonAuthority) :
    boundary.truthAuthority = false ∧
      boundary.causalAuthority = false ∧
      boundary.executionAuthority = false := by
  exact ⟨boundary.truthForbidden, boundary.causalForbidden,
    boundary.executionForbidden⟩


theorem replan_grants_no_memory_or_self_modification_authority
    (boundary : ReplanNonAuthority) :
    boundary.memoryOverwriteAuthority = false ∧
      boundary.selfModificationAuthority = false := by
  exact ⟨boundary.overwriteForbidden, boundary.selfModificationForbidden⟩


structure ReplanHistory where
  committedRecords : ℕ
  recoveredRecords : ℕ
  snapshotRecords : ℕ
  recoveryExact : recoveredRecords = committedRecords
  snapshotDerived : snapshotRecords = recoveredRecords


theorem replanHistory_snapshot_matches_commits
    (history : ReplanHistory) :
    history.snapshotRecords = history.committedRecords := by
  rw [history.snapshotDerived, history.recoveryExact]

end PlanOS
end KUOS
