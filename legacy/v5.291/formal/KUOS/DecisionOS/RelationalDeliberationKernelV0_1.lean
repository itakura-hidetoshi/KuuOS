import Mathlib
import KUOS.BeliefOS.ContextGerbeCoherenceV0_3

namespace KUOS
namespace DecisionOS

inductive DecisionPhase where
  | frame
  | generate
  | constrain
  | evaluate
  | challenge
  | qiCondition
  | twoTruthsCheck
  | middleWayGate
  | decide
  | commit
  deriving DecidableEq, Repr


def DecisionPhase.next : DecisionPhase → Option DecisionPhase
  | .frame => some .generate
  | .generate => some .constrain
  | .constrain => some .evaluate
  | .evaluate => some .challenge
  | .challenge => some .qiCondition
  | .qiCondition => some .twoTruthsCheck
  | .twoTruthsCheck => some .middleWayGate
  | .middleWayGate => some .decide
  | .decide => some .commit
  | .commit => none


theorem decisionPhase_next_deterministic
    (phase left right : DecisionPhase)
    (hleft : phase.next = some left)
    (hright : phase.next = some right) :
    left = right := by
  rw [hleft] at hright
  exact Option.some.inj hright


theorem decisionPhase_no_frame_skip :
    DecisionPhase.frame.next = some DecisionPhase.generate := by
  rfl


theorem decisionPhase_no_generate_skip :
    DecisionPhase.generate.next = some DecisionPhase.constrain := by
  rfl


theorem decisionPhase_no_decide_skip :
    DecisionPhase.decide.next = some DecisionPhase.commit := by
  rfl


structure DecisionEventIndex where
  current : ℕ


def DecisionEventIndex.append (index : DecisionEventIndex) : DecisionEventIndex where
  current := index.current + 1


theorem decisionEventIndex_strict
    (index : DecisionEventIndex) :
    index.current < index.append.current := by
  simp [DecisionEventIndex.append]


structure DecisionValueInterval where
  lower : ℝ
  upper : ℝ
  ordered : lower ≤ upper


def intervalWidth (interval : DecisionValueInterval) : ℝ :=
  interval.upper - interval.lower


theorem intervalWidth_nonnegative
    (interval : DecisionValueInterval) :
    0 ≤ intervalWidth interval := by
  unfold intervalWidth
  linarith [interval.ordered]


def robustDominates
    (margin : ℝ)
    (left right : DecisionValueInterval) : Prop :=
  right.upper + margin < left.lower


theorem robustDominates_strict_separation
    (margin : ℝ)
    (left right : DecisionValueInterval)
    (marginNonnegative : 0 ≤ margin)
    (dominates : robustDominates margin left right) :
    right.upper < left.lower := by
  unfold robustDominates at dominates
  linarith


theorem robustDominates_excludes_reverse
    (margin : ℝ)
    (left right : DecisionValueInterval)
    (marginNonnegative : 0 ≤ margin)
    (dominates : robustDominates margin left right) :
    ¬ robustDominates margin right left := by
  intro reverse
  unfold robustDominates at dominates reverse
  linarith [left.ordered, right.ordered]


structure SelectionCertificate where
  selected : DecisionValueInterval
  alternatives : List DecisionValueInterval
  margin : ℝ
  marginNonnegative : 0 ≤ margin
  dominatesAll : ∀ alternative ∈ alternatives,
    robustDominates margin selected alternative


theorem selectionCertificate_separates_every_alternative
    (certificate : SelectionCertificate)
    (alternative : DecisionValueInterval)
    (member : alternative ∈ certificate.alternatives) :
    alternative.upper < certificate.selected.lower := by
  exact robustDominates_strict_separation
    certificate.margin
    certificate.selected
    alternative
    certificate.marginNonnegative
    (certificate.dominatesAll alternative member)


structure OptionPlurality where
  optionCount : ℕ
  retainedAlternativeCount : ℕ
  retainedWithinField : retainedAlternativeCount ≤ optionCount


theorem retainedAlternatives_do_not_exceed_option_field
    (plurality : OptionPlurality) :
    plurality.retainedAlternativeCount ≤ plurality.optionCount := by
  exact plurality.retainedWithinField


structure ConstraintGate where
  missionAllowed : Bool
  prohibited : Bool
  authorityClaimed : Bool
  withinBudget : Bool
  withinRisk : Bool
  recoverable : Bool
  reversible : Bool
  evidencePresent : Bool


def ConstraintGate.admissible (gate : ConstraintGate) : Prop :=
  gate.missionAllowed = true ∧
  gate.prohibited = false ∧
  gate.authorityClaimed = false ∧
  gate.withinBudget = true ∧
  gate.withinRisk = true ∧
  gate.recoverable = true ∧
  gate.reversible = true ∧
  gate.evidencePresent = true


theorem admissibleOption_does_not_claim_authority
    (gate : ConstraintGate)
    (admissible : gate.admissible) :
    gate.authorityClaimed = false := by
  exact admissible.2.2.1


theorem admissibleOption_is_not_prohibited
    (gate : ConstraintGate)
    (admissible : gate.admissible) :
    gate.prohibited = false := by
  exact admissible.2.1


structure QiDecisionBoundary where
  contextOnly : Bool
  grantsTruthAuthority : Bool
  grantsExecutionLicense : Bool
  grantsMoralVeto : Bool
  contextRequired : contextOnly = true
  truthForbidden : grantsTruthAuthority = false
  executionForbidden : grantsExecutionLicense = false
  vetoForbidden : grantsMoralVeto = false


theorem qiDecision_does_not_grant_truth
    (boundary : QiDecisionBoundary) :
    boundary.grantsTruthAuthority = false := by
  exact boundary.truthForbidden


theorem qiDecision_does_not_grant_execution
    (boundary : QiDecisionBoundary) :
    boundary.grantsExecutionLicense = false := by
  exact boundary.executionForbidden


theorem qiDecision_does_not_grant_moral_veto
    (boundary : QiDecisionBoundary) :
    boundary.grantsMoralVeto = false := by
  exact boundary.vetoForbidden


structure DecisionTwoTruthsBoundary where
  samvrtiUsable : Bool
  paramarthaNonReified : Bool
  selectedOptionNotAbsolute : Bool
  separated : Bool
  samvrtiRequired : samvrtiUsable = true
  nonReificationRequired : paramarthaNonReified = true
  nonAbsolutizationRequired : selectedOptionNotAbsolute = true
  separationRequired : separated = true


theorem decisionTwoTruths_is_non_reified
    (boundary : DecisionTwoTruthsBoundary) :
    boundary.paramarthaNonReified = true := by
  exact boundary.nonReificationRequired


theorem decisionTwoTruths_does_not_absolutize_option
    (boundary : DecisionTwoTruthsBoundary) :
    boundary.selectedOptionNotAbsolute = true := by
  exact boundary.nonAbsolutizationRequired


theorem decisionTwoTruths_remains_separated
    (boundary : DecisionTwoTruthsBoundary) :
    boundary.separated = true := by
  exact boundary.separationRequired


structure MiddleWayDecisionBoundary where
  prematureCollapse : Bool
  nihilisticErasure : Bool
  responsibilityAbandonment : Bool
  stakeholderErasure : Bool
  collapseForbidden : prematureCollapse = false
  erasureForbidden : nihilisticErasure = false
  abandonmentForbidden : responsibilityAbandonment = false
  stakeholderErasureForbidden : stakeholderErasure = false


theorem middleWayDecision_avoids_premature_collapse
    (boundary : MiddleWayDecisionBoundary) :
    boundary.prematureCollapse = false := by
  exact boundary.collapseForbidden


theorem middleWayDecision_avoids_nihilistic_erasure
    (boundary : MiddleWayDecisionBoundary) :
    boundary.nihilisticErasure = false := by
  exact boundary.erasureForbidden


theorem middleWayDecision_preserves_responsibility
    (boundary : MiddleWayDecisionBoundary) :
    boundary.responsibilityAbandonment = false := by
  exact boundary.abandonmentForbidden


structure DecisionAuthorityBoundary where
  decisionIsTruth : Bool
  decisionIsExecution : Bool
  decisionIsHostLicense : Bool
  grantsClinicalAuthority : Bool
  grantsInstitutionalAuthority : Bool
  truthForbidden : decisionIsTruth = false
  executionForbidden : decisionIsExecution = false
  licenseForbidden : decisionIsHostLicense = false
  clinicalForbidden : grantsClinicalAuthority = false
  institutionalForbidden : grantsInstitutionalAuthority = false


theorem decision_does_not_become_truth
    (boundary : DecisionAuthorityBoundary) :
    boundary.decisionIsTruth = false := by
  exact boundary.truthForbidden


theorem decision_does_not_execute
    (boundary : DecisionAuthorityBoundary) :
    boundary.decisionIsExecution = false := by
  exact boundary.executionForbidden


theorem decision_does_not_grant_host_license
    (boundary : DecisionAuthorityBoundary) :
    boundary.decisionIsHostLicense = false := by
  exact boundary.licenseForbidden


structure DecisionCommitBoundary where
  futureOnly : Bool
  memoryOverwrite : Bool
  decisionNotExecution : Bool
  futureRequired : futureOnly = true
  overwriteForbidden : memoryOverwrite = false
  nonExecutionRequired : decisionNotExecution = true


theorem decisionCommit_is_future_only
    (boundary : DecisionCommitBoundary) :
    boundary.futureOnly = true := by
  exact boundary.futureRequired


theorem decisionCommit_does_not_overwrite_memory
    (boundary : DecisionCommitBoundary) :
    boundary.memoryOverwrite = false := by
  exact boundary.overwriteForbidden


theorem decisionCommit_is_not_execution
    (boundary : DecisionCommitBoundary) :
    boundary.decisionNotExecution = true := by
  exact boundary.nonExecutionRequired


structure DecisionHistory where
  commits : ℕ
  summaries : ℕ
  aligned : summaries = commits


def appendDecision (history : DecisionHistory) : DecisionHistory where
  commits := history.commits + 1
  summaries := history.summaries + 1
  aligned := by simp [history.aligned]


theorem decisionHistory_commit_strict
    (history : DecisionHistory) :
    history.commits < (appendDecision history).commits := by
  simp [appendDecision]


theorem decisionHistory_recovered_count_aligned
    (history : DecisionHistory) :
    history.summaries = history.commits := by
  exact history.aligned


structure ReplanDecisionActivation where
  missionPhaseIsReplan : Bool
  futureOnly : Bool
  memoryOverwrite : Bool
  decisionNotExecution : Bool
  hostLicenseGranted : Bool
  replanRequired : missionPhaseIsReplan = true
  futureRequired : futureOnly = true
  overwriteForbidden : memoryOverwrite = false
  nonExecutionRequired : decisionNotExecution = true
  hostLicenseForbidden : hostLicenseGranted = false


theorem decisionActivation_requires_replan
    (receipt : ReplanDecisionActivation) :
    receipt.missionPhaseIsReplan = true := by
  exact receipt.replanRequired


theorem decisionActivation_is_future_only
    (receipt : ReplanDecisionActivation) :
    receipt.futureOnly = true := by
  exact receipt.futureRequired


theorem decisionActivation_does_not_overwrite
    (receipt : ReplanDecisionActivation) :
    receipt.memoryOverwrite = false := by
  exact receipt.overwriteForbidden


theorem decisionActivation_does_not_execute
    (receipt : ReplanDecisionActivation) :
    receipt.decisionNotExecution = true := by
  exact receipt.nonExecutionRequired


theorem decisionActivation_does_not_grant_host_license
    (receipt : ReplanDecisionActivation) :
    receipt.hostLicenseGranted = false := by
  exact receipt.hostLicenseForbidden

end DecisionOS
end KUOS
