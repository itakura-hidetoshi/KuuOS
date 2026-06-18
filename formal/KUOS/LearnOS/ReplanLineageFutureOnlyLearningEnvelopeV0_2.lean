import Mathlib
import KUOS.VerifyOS.ReplanLineageVerificationEnvelopeV0_2
import KUOS.LearnOS.FutureOnlyEvidenceLearningV0_1

namespace KUOS
namespace LearnOS

structure ExactLearnCycleGate where
  verifyCycle : Nat
  learnCycle : Nat
  learnPhase : Bool
  exactCycleRequired : learnCycle = verifyCycle
  learnPhaseRequired : learnPhase = true


theorem lineage_learning_uses_exact_verify_cycle
    (gate : ExactLearnCycleGate) :
    gate.learnCycle = gate.verifyCycle := by
  exact gate.exactCycleRequired


theorem lineage_learning_requires_learn_phase
    (gate : ExactLearnCycleGate) :
    gate.learnPhase = true := by
  exact gate.learnPhaseRequired


structure UpstreamLearningLineage where
  verifyHandoffPreserved : Bool
  verifyCompletionPreserved : Bool
  observeCompletionPreserved : Bool
  actCompletionPreserved : Bool
  compilerReceiptPreserved : Bool
  replanReceiptPreserved : Bool
  qiConditionPreserved : Bool
  decisionReceiptPreserved : Bool
  selectedCandidatePreserved : Bool
  selectedStepPreserved : Bool
  verifyHandoffRequired : verifyHandoffPreserved = true
  verifyCompletionRequired : verifyCompletionPreserved = true
  observeCompletionRequired : observeCompletionPreserved = true
  actCompletionRequired : actCompletionPreserved = true
  compilerRequired : compilerReceiptPreserved = true
  replanRequired : replanReceiptPreserved = true
  qiRequired : qiConditionPreserved = true
  decisionRequired : decisionReceiptPreserved = true
  candidateRequired : selectedCandidatePreserved = true
  stepRequired : selectedStepPreserved = true


theorem learn_handoff_preserves_full_upstream_lineage
    (lineage : UpstreamLearningLineage) :
    lineage.verifyHandoffPreserved = true ∧
      lineage.verifyCompletionPreserved = true ∧
      lineage.observeCompletionPreserved = true ∧
      lineage.actCompletionPreserved = true ∧
      lineage.compilerReceiptPreserved = true ∧
      lineage.replanReceiptPreserved = true := by
  exact ⟨lineage.verifyHandoffRequired,
    lineage.verifyCompletionRequired,
    lineage.observeCompletionRequired,
    lineage.actCompletionRequired,
    lineage.compilerRequired,
    lineage.replanRequired⟩


theorem learn_handoff_preserves_qi_decision_selection
    (lineage : UpstreamLearningLineage) :
    lineage.qiConditionPreserved = true ∧
      lineage.decisionReceiptPreserved = true ∧
      lineage.selectedCandidatePreserved = true ∧
      lineage.selectedStepPreserved = true := by
  exact ⟨lineage.qiRequired, lineage.decisionRequired,
    lineage.candidateRequired, lineage.stepRequired⟩


structure VerificationEvidenceBinding where
  sourceVerifyDigest : Nat
  handoffVerifyDigest : Nat
  sourceEvidenceDigest : Nat
  learnedEvidenceDigest : Nat
  sourceCriterionDigest : Nat
  learnedCriterionDigest : Nat
  verifyIdentityRequired : handoffVerifyDigest = sourceVerifyDigest
  evidenceIdentityRequired : learnedEvidenceDigest = sourceEvidenceDigest
  criterionIdentityRequired : learnedCriterionDigest = sourceCriterionDigest


theorem learning_preserves_verification_evidence_identity
    (binding : VerificationEvidenceBinding) :
    binding.handoffVerifyDigest = binding.sourceVerifyDigest ∧
      binding.learnedEvidenceDigest = binding.sourceEvidenceDigest ∧
      binding.learnedCriterionDigest = binding.sourceCriterionDigest := by
  exact ⟨binding.verifyIdentityRequired,
    binding.evidenceIdentityRequired,
    binding.criterionIdentityRequired⟩


structure CounterevidenceBoundary where
  counterevidencePreserved : Bool
  falsificationPreserved : Bool
  independentAssessmentPreserved : Bool
  alternativeExplanationsPreserved : Bool
  antiOvergeneralizationTested : Bool
  counterevidenceRequired : counterevidencePreserved = true
  falsificationRequired : falsificationPreserved = true
  independenceRequired : independentAssessmentPreserved = true
  alternativesRequired : alternativeExplanationsPreserved = true
  antiOvergeneralizationRequired : antiOvergeneralizationTested = true


theorem learning_preserves_challenge_surface
    (boundary : CounterevidenceBoundary) :
    boundary.counterevidencePreserved = true ∧
      boundary.falsificationPreserved = true ∧
      boundary.independentAssessmentPreserved = true ∧
      boundary.alternativeExplanationsPreserved = true ∧
      boundary.antiOvergeneralizationTested = true := by
  exact ⟨boundary.counterevidenceRequired,
    boundary.falsificationRequired,
    boundary.independenceRequired,
    boundary.alternativesRequired,
    boundary.antiOvergeneralizationRequired⟩


inductive LearningRoute where
  | reinforcement
  | repair
  | reobservation
  | hold
  deriving DecidableEq, Repr


inductive PlanOSCandidateType where
  | continue
  | strengthen
  | repair
  | slowDown
  | reobserve
  | reroute
  | hold
  deriving DecidableEq, Repr


def compatibleWithPlanOS : LearningRoute → PlanOSCandidateType → Prop
  | .reinforcement, candidate =>
      candidate = .continue ∨ candidate = .strengthen ∨
        candidate = .slowDown ∨ candidate = .hold
  | .repair, candidate =>
      candidate = .repair ∨ candidate = .slowDown ∨
        candidate = .reroute ∨ candidate = .hold
  | .reobservation, candidate =>
      candidate = .reobserve ∨ candidate = .hold
  | .hold, candidate =>
      candidate = .hold ∨ candidate = .reobserve


theorem reinforcement_planos_compatibility
    (candidate : PlanOSCandidateType)
    (h : compatibleWithPlanOS .reinforcement candidate) :
    candidate = .continue ∨ candidate = .strengthen ∨
      candidate = .slowDown ∨ candidate = .hold := by
  exact h


theorem repair_planos_compatibility
    (candidate : PlanOSCandidateType)
    (h : compatibleWithPlanOS .repair candidate) :
    candidate = .repair ∨ candidate = .slowDown ∨
      candidate = .reroute ∨ candidate = .hold := by
  exact h


theorem reobservation_planos_compatibility
    (candidate : PlanOSCandidateType)
    (h : compatibleWithPlanOS .reobservation candidate) :
    candidate = .reobserve ∨ candidate = .hold := by
  exact h


theorem hold_planos_compatibility
    (candidate : PlanOSCandidateType)
    (h : compatibleWithPlanOS .hold candidate) :
    candidate = .hold ∨ candidate = .reobserve := by
  exact h


structure FutureOnlyDeltaBoundary where
  futureOnly : Bool
  activeNow : Bool
  currentCycleUnchanged : Bool
  pastRecordsUnchanged : Bool
  memoryOverwrite : Bool
  activationRequiresReplan : Bool
  futureOnlyRequired : futureOnly = true
  activeNowForbidden : activeNow = false
  currentCycleRequired : currentCycleUnchanged = true
  pastRecordsRequired : pastRecordsUnchanged = true
  overwriteForbidden : memoryOverwrite = false
  replanRequired : activationRequiresReplan = true


theorem learning_delta_is_strictly_future_only
    (boundary : FutureOnlyDeltaBoundary) :
    boundary.futureOnly = true ∧
      boundary.activeNow = false ∧
      boundary.currentCycleUnchanged = true ∧
      boundary.pastRecordsUnchanged = true ∧
      boundary.memoryOverwrite = false ∧
      boundary.activationRequiresReplan = true := by
  exact ⟨boundary.futureOnlyRequired,
    boundary.activeNowForbidden,
    boundary.currentCycleRequired,
    boundary.pastRecordsRequired,
    boundary.overwriteForbidden,
    boundary.replanRequired⟩


structure MiddleWayLearningGate where
  candidateAdmissible : Bool
  counterevidencePreserved : Bool
  samvrtiCandidateUsable : Bool
  paramarthaNonReificationPreserved : Bool
  qiGrantsAuthority : Bool
  admissibilityRequired : candidateAdmissible = true
  counterevidenceRequired : counterevidencePreserved = true
  samvrtiRequired : samvrtiCandidateUsable = true
  nonReificationRequired : paramarthaNonReificationPreserved = true
  qiAuthorityForbidden : qiGrantsAuthority = false


theorem middle_way_gate_preserves_two_truths
    (gate : MiddleWayLearningGate) :
    gate.candidateAdmissible = true ∧
      gate.counterevidencePreserved = true ∧
      gate.samvrtiCandidateUsable = true ∧
      gate.paramarthaNonReificationPreserved = true ∧
      gate.qiGrantsAuthority = false := by
  exact ⟨gate.admissibilityRequired,
    gate.counterevidenceRequired,
    gate.samvrtiRequired,
    gate.nonReificationRequired,
    gate.qiAuthorityForbidden⟩


structure OwnershipBoundary where
  replanOwnedByPlanOS : Bool
  selectionOwnedByDecisionOS : Bool
  executionOwnedByActOS : Bool
  replanOwnershipRequired : replanOwnedByPlanOS = true
  selectionOwnershipRequired : selectionOwnedByDecisionOS = true
  executionOwnershipRequired : executionOwnedByActOS = true


theorem learning_preserves_operating_system_ownership
    (boundary : OwnershipBoundary) :
    boundary.replanOwnedByPlanOS = true ∧
      boundary.selectionOwnedByDecisionOS = true ∧
      boundary.executionOwnedByActOS = true := by
  exact ⟨boundary.replanOwnershipRequired,
    boundary.selectionOwnershipRequired,
    boundary.executionOwnershipRequired⟩


structure ActivationSeparation where
  learningRecorded : Bool
  replanHandoffReady : Bool
  replanActivated : Bool
  planActivated : Bool
  executionPermitted : Bool
  hostLicenseGranted : Bool
  learningRequired : learningRecorded = true
  handoffRequired : replanHandoffReady = true
  replanActivationForbidden : replanActivated = false
  planActivationForbidden : planActivated = false
  executionForbidden : executionPermitted = false
  hostLicenseForbidden : hostLicenseGranted = false


theorem learning_commit_is_not_activation_or_execution
    (separation : ActivationSeparation) :
    separation.learningRecorded = true ∧
      separation.replanHandoffReady = true ∧
      separation.replanActivated = false ∧
      separation.planActivated = false ∧
      separation.executionPermitted = false ∧
      separation.hostLicenseGranted = false := by
  exact ⟨separation.learningRequired,
    separation.handoffRequired,
    separation.replanActivationForbidden,
    separation.planActivationForbidden,
    separation.executionForbidden,
    separation.hostLicenseForbidden⟩


structure QiLearningBoundary where
  qiLineagePreserved : Bool
  qiHistoryPreserved : Bool
  qiGrantsTruth : Bool
  qiGrantsCausality : Bool
  qiGrantsLearningActivation : Bool
  lineageRequired : qiLineagePreserved = true
  historyRequired : qiHistoryPreserved = true
  truthForbidden : qiGrantsTruth = false
  causalityForbidden : qiGrantsCausality = false
  activationForbidden : qiGrantsLearningActivation = false


theorem qi_is_learning_context_not_authority
    (boundary : QiLearningBoundary) :
    boundary.qiLineagePreserved = true ∧
      boundary.qiHistoryPreserved = true ∧
      boundary.qiGrantsTruth = false ∧
      boundary.qiGrantsCausality = false ∧
      boundary.qiGrantsLearningActivation = false := by
  exact ⟨boundary.lineageRequired,
    boundary.historyRequired,
    boundary.truthForbidden,
    boundary.causalityForbidden,
    boundary.activationForbidden⟩


structure SingleUseLearning where
  handoffCount : Nat
  completionCount : Nat
  handoffBound : handoffCount ≤ 1
  completionBound : completionCount ≤ handoffCount


theorem learning_completion_is_single_use
    (single : SingleUseLearning) :
    single.completionCount ≤ 1 := by
  exact le_trans single.completionBound single.handoffBound


structure RecoveryEquality where
  committedRecords : Nat
  recoveredRecords : Nat
  recoveryRequired : recoveredRecords = committedRecords


theorem recovered_learning_count_eq_committed
    (recovery : RecoveryEquality) :
    recovery.recoveredRecords = recovery.committedRecords := by
  exact recovery.recoveryRequired


structure NonAuthorityBoundary where
  truthGranted : Bool
  causalGranted : Bool
  executionGranted : Bool
  memoryOverwrite : Bool
  selfModification : Bool
  replanActivation : Bool
  planActivation : Bool
  truthForbidden : truthGranted = false
  causalForbidden : causalGranted = false
  executionForbidden : executionGranted = false
  overwriteForbidden : memoryOverwrite = false
  selfModificationForbidden : selfModification = false
  replanActivationForbidden : replanActivation = false
  planActivationForbidden : planActivation = false


theorem learn_lineage_envelope_grants_no_new_authority
    (boundary : NonAuthorityBoundary) :
    boundary.truthGranted = false ∧
      boundary.causalGranted = false ∧
      boundary.executionGranted = false ∧
      boundary.memoryOverwrite = false ∧
      boundary.selfModification = false ∧
      boundary.replanActivation = false ∧
      boundary.planActivation = false := by
  exact ⟨boundary.truthForbidden,
    boundary.causalForbidden,
    boundary.executionForbidden,
    boundary.overwriteForbidden,
    boundary.selfModificationForbidden,
    boundary.replanActivationForbidden,
    boundary.planActivationForbidden⟩

end LearnOS
end KUOS
