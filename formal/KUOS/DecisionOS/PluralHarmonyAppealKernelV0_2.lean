import Mathlib
import KUOS.DecisionOS.RelationalDeliberationKernelV0_1

namespace KUOS
namespace DecisionOS

inductive PluralDecisionPhase where
  | bindV01
  | registerStakeholders
  | evaluatePlurality
  | validateVetoes
  | aggregate
  | explain
  | appealWindow
  | adjudicate
  | commit
  deriving DecidableEq, Repr


def PluralDecisionPhase.next : PluralDecisionPhase → Option PluralDecisionPhase
  | .bindV01 => some .registerStakeholders
  | .registerStakeholders => some .evaluatePlurality
  | .evaluatePlurality => some .validateVetoes
  | .validateVetoes => some .aggregate
  | .aggregate => some .explain
  | .explain => some .appealWindow
  | .appealWindow => some .adjudicate
  | .adjudicate => some .commit
  | .commit => none


theorem pluralPhase_next_deterministic
    (phase left right : PluralDecisionPhase)
    (hleft : phase.next = some left)
    (hright : phase.next = some right) :
    left = right := by
  rw [hleft] at hright
  exact Option.some.inj hright


theorem pluralPhase_no_bind_skip :
    PluralDecisionPhase.bindV01.next =
      some PluralDecisionPhase.registerStakeholders := by
  rfl


theorem pluralPhase_no_appeal_skip :
    PluralDecisionPhase.appealWindow.next =
      some PluralDecisionPhase.adjudicate := by
  rfl


theorem pluralPhase_no_adjudicate_skip :
    PluralDecisionPhase.adjudicate.next =
      some PluralDecisionPhase.commit := by
  rfl


structure PluralEventIndex where
  current : ℕ


def PluralEventIndex.append (index : PluralEventIndex) : PluralEventIndex where
  current := index.current + 1


theorem pluralEventIndex_strict
    (index : PluralEventIndex) :
    index.current < index.append.current := by
  simp [PluralEventIndex.append]


structure StakeholderUtilityInterval where
  lower : ℝ
  upper : ℝ
  ordered : lower ≤ upper


def StakeholderUtilityInterval.midpoint
    (interval : StakeholderUtilityInterval) : ℝ :=
  (interval.lower + interval.upper) / 2


theorem stakeholderUtility_ordered
    (interval : StakeholderUtilityInterval) :
    interval.lower ≤ interval.upper := by
  exact interval.ordered


def nashSurplus (disagreement utility : ℝ) : ℝ :=
  max 0 (utility - disagreement)


theorem nashSurplus_nonnegative
    (disagreement utility : ℝ) :
    0 ≤ nashSurplus disagreement utility := by
  exact le_max_left _ _


structure NashProductBoundary where
  lowerProduct : ℝ
  upperProduct : ℝ
  lowerNonnegative : 0 ≤ lowerProduct
  upperNonnegative : 0 ≤ upperProduct
  ordered : lowerProduct ≤ upperProduct


theorem nashProduct_lower_nonnegative
    (boundary : NashProductBoundary) :
    0 ≤ boundary.lowerProduct := by
  exact boundary.lowerNonnegative


theorem nashProduct_upper_nonnegative
    (boundary : NashProductBoundary) :
    0 ≤ boundary.upperProduct := by
  exact boundary.upperNonnegative


structure WeightedSupportBoundary where
  supportWeight : ℝ
  oppositionWeight : ℝ
  uncertaintyWeight : ℝ
  totalWeight : ℝ
  supportNonnegative : 0 ≤ supportWeight
  oppositionNonnegative : 0 ≤ oppositionWeight
  uncertaintyNonnegative : 0 ≤ uncertaintyWeight
  partitioned : supportWeight + oppositionWeight + uncertaintyWeight = totalWeight


theorem supportWeight_le_total
    (boundary : WeightedSupportBoundary) :
    boundary.supportWeight ≤ boundary.totalWeight := by
  rw [← boundary.partitioned]
  linarith [boundary.oppositionNonnegative, boundary.uncertaintyNonnegative]


theorem oppositionWeight_le_total
    (boundary : WeightedSupportBoundary) :
    boundary.oppositionWeight ≤ boundary.totalWeight := by
  rw [← boundary.partitioned]
  linarith [boundary.supportNonnegative, boundary.uncertaintyNonnegative]


structure WeightedMedianWitness where
  minimumValue : ℝ
  medianValue : ℝ
  maximumValue : ℝ
  lowerBounded : minimumValue ≤ medianValue
  upperBounded : medianValue ≤ maximumValue


theorem weightedMedian_within_bounds
    (witness : WeightedMedianWitness) :
    witness.minimumValue ≤ witness.medianValue ∧
      witness.medianValue ≤ witness.maximumValue := by
  exact ⟨witness.lowerBounded, witness.upperBounded⟩


structure WorstCaseLowerWitness where
  worstCaseLower : ℝ
  stakeholderLowers : List ℝ
  lowerThanEveryStakeholder :
    ∀ value ∈ stakeholderLowers, worstCaseLower ≤ value


theorem worstCaseLower_le_each
    (witness : WorstCaseLowerWitness)
    (value : ℝ)
    (member : value ∈ witness.stakeholderLowers) :
    witness.worstCaseLower ≤ value := by
  exact witness.lowerThanEveryStakeholder value member


structure RawVetoSignal where
  optionInSourceField : Bool
  missionBoundConstraint : Bool
  stakeholderProtectedConstraint : Bool
  evidencePresent : Bool
  grantsAuthority : Bool
  authorityForbidden : grantsAuthority = false


theorem rawVeto_does_not_grant_authority
    (signal : RawVetoSignal) :
    signal.grantsAuthority = false := by
  exact signal.authorityForbidden


def RawVetoSignal.validated (signal : RawVetoSignal) : Prop :=
  signal.optionInSourceField = true ∧
  signal.missionBoundConstraint = true ∧
  signal.stakeholderProtectedConstraint = true ∧
  signal.evidencePresent = true


structure ValidatedProtectiveVeto where
  signal : RawVetoSignal
  validation : signal.validated
  excludesConsensusOption : Bool
  exclusionRequired : excludesConsensusOption = true


theorem validatedVeto_excludes_consensus
    (veto : ValidatedProtectiveVeto) :
    veto.excludesConsensusOption = true := by
  exact veto.exclusionRequired


theorem validatedVeto_is_mission_bound
    (veto : ValidatedProtectiveVeto) :
    veto.signal.missionBoundConstraint = true := by
  exact veto.validation.2.1


theorem validatedVeto_is_stakeholder_protected
    (veto : ValidatedProtectiveVeto) :
    veto.signal.stakeholderProtectedConstraint = true := by
  exact veto.validation.2.2.1


structure BroadAcceptabilityBoundary where
  validatedVetoPresent : Bool
  supportWeight : ℝ
  minimumSupportWeight : ℝ
  oppositionWeight : ℝ
  maximumOppositionWeight : ℝ
  worstCaseLower : ℝ
  minimumWorstCaseValue : ℝ


def BroadAcceptabilityBoundary.eligible
    (boundary : BroadAcceptabilityBoundary) : Prop :=
  boundary.validatedVetoPresent = false ∧
  boundary.minimumSupportWeight ≤ boundary.supportWeight ∧
  boundary.oppositionWeight ≤ boundary.maximumOppositionWeight ∧
  boundary.minimumWorstCaseValue ≤ boundary.worstCaseLower


structure ConsensusCertificate where
  optionId : String
  boundary : BroadAcceptabilityBoundary
  broadAcceptability : boundary.eligible
  uniqueTopCandidate : Bool
  uniqueTopRequired : uniqueTopCandidate = true
  consensusIsTruth : Bool
  consensusTruthForbidden : consensusIsTruth = false


theorem consensusCertificate_has_no_validated_veto
    (certificate : ConsensusCertificate) :
    certificate.boundary.validatedVetoPresent = false := by
  exact certificate.broadAcceptability.1


theorem consensusCertificate_meets_support_floor
    (certificate : ConsensusCertificate) :
    certificate.boundary.minimumSupportWeight ≤
      certificate.boundary.supportWeight := by
  exact certificate.broadAcceptability.2.1


theorem consensusCertificate_meets_opposition_ceiling
    (certificate : ConsensusCertificate) :
    certificate.boundary.oppositionWeight ≤
      certificate.boundary.maximumOppositionWeight := by
  exact certificate.broadAcceptability.2.2.1


theorem consensusCertificate_meets_worst_case_floor
    (certificate : ConsensusCertificate) :
    certificate.boundary.minimumWorstCaseValue ≤
      certificate.boundary.worstCaseLower := by
  exact certificate.broadAcceptability.2.2.2


theorem consensusCertificate_is_not_truth
    (certificate : ConsensusCertificate) :
    certificate.consensusIsTruth = false := by
  exact certificate.consensusTruthForbidden


structure StakeholderAblationBoundary where
  explanationNotCausalTruth : Bool
  explanationNotMoralWorth : Bool
  causalTruthForbidden : explanationNotCausalTruth = true
  moralWorthForbidden : explanationNotMoralWorth = true


theorem stakeholderAblation_is_not_causal_truth
    (boundary : StakeholderAblationBoundary) :
    boundary.explanationNotCausalTruth = true := by
  exact boundary.causalTruthForbidden


theorem stakeholderAblation_is_not_moral_worth
    (boundary : StakeholderAblationBoundary) :
    boundary.explanationNotMoralWorth = true := by
  exact boundary.moralWorthForbidden


structure AppealHistory where
  appealCount : ℕ
  preservedPriorDecisionCount : ℕ
  aligned : preservedPriorDecisionCount = appealCount


def appendAppeal (history : AppealHistory) : AppealHistory where
  appealCount := history.appealCount + 1
  preservedPriorDecisionCount := history.preservedPriorDecisionCount + 1
  aligned := by simp [history.aligned]


theorem appealHistory_strict
    (history : AppealHistory) :
    history.appealCount < (appendAppeal history).appealCount := by
  simp [appendAppeal]


theorem appealHistory_preserves_prior_record
    (history : AppealHistory) :
    history.preservedPriorDecisionCount = history.appealCount := by
  exact history.aligned


structure AppealBoundary where
  futureOnly : Bool
  rewritesPriorDecision : Bool
  grantsExecutionAuthority : Bool
  futureRequired : futureOnly = true
  rewriteForbidden : rewritesPriorDecision = false
  executionForbidden : grantsExecutionAuthority = false


theorem appeal_is_future_only
    (boundary : AppealBoundary) :
    boundary.futureOnly = true := by
  exact boundary.futureRequired


theorem appeal_does_not_rewrite_prior_decision
    (boundary : AppealBoundary) :
    boundary.rewritesPriorDecision = false := by
  exact boundary.rewriteForbidden


theorem appeal_does_not_grant_execution
    (boundary : AppealBoundary) :
    boundary.grantsExecutionAuthority = false := by
  exact boundary.executionForbidden


structure PluralDecisionCommitBoundary where
  sourceV01ReadOnly : Bool
  futureOnly : Bool
  memoryOverwrite : Bool
  pluralDecisionNotExecution : Bool
  consensusNotTruth : Bool
  sourceReadOnlyRequired : sourceV01ReadOnly = true
  futureRequired : futureOnly = true
  overwriteForbidden : memoryOverwrite = false
  nonExecutionRequired : pluralDecisionNotExecution = true
  nonTruthRequired : consensusNotTruth = true


theorem pluralCommit_preserves_v01
    (boundary : PluralDecisionCommitBoundary) :
    boundary.sourceV01ReadOnly = true := by
  exact boundary.sourceReadOnlyRequired


theorem pluralCommit_is_future_only
    (boundary : PluralDecisionCommitBoundary) :
    boundary.futureOnly = true := by
  exact boundary.futureRequired


theorem pluralCommit_does_not_overwrite
    (boundary : PluralDecisionCommitBoundary) :
    boundary.memoryOverwrite = false := by
  exact boundary.overwriteForbidden


theorem pluralCommit_does_not_execute
    (boundary : PluralDecisionCommitBoundary) :
    boundary.pluralDecisionNotExecution = true := by
  exact boundary.nonExecutionRequired


theorem pluralCommit_consensus_is_not_truth
    (boundary : PluralDecisionCommitBoundary) :
    boundary.consensusNotTruth = true := by
  exact boundary.nonTruthRequired


structure PluralDecisionHistory where
  commits : ℕ
  summaries : ℕ
  aligned : summaries = commits


def appendPluralDecision
    (history : PluralDecisionHistory) : PluralDecisionHistory where
  commits := history.commits + 1
  summaries := history.summaries + 1
  aligned := by simp [history.aligned]


theorem pluralDecisionHistory_strict
    (history : PluralDecisionHistory) :
    history.commits < (appendPluralDecision history).commits := by
  simp [appendPluralDecision]


theorem pluralDecisionHistory_recovery_aligned
    (history : PluralDecisionHistory) :
    history.summaries = history.commits := by
  exact history.aligned


structure ReplanPluralActivation where
  missionPhaseIsReplan : Bool
  futureOnly : Bool
  memoryOverwrite : Bool
  pluralDecisionNotExecution : Bool
  consensusNotTruth : Bool
  hostLicenseGranted : Bool
  replanRequired : missionPhaseIsReplan = true
  futureRequired : futureOnly = true
  overwriteForbidden : memoryOverwrite = false
  nonExecutionRequired : pluralDecisionNotExecution = true
  nonTruthRequired : consensusNotTruth = true
  hostLicenseForbidden : hostLicenseGranted = false


theorem pluralActivation_requires_replan
    (receipt : ReplanPluralActivation) :
    receipt.missionPhaseIsReplan = true := by
  exact receipt.replanRequired


theorem pluralActivation_is_future_only
    (receipt : ReplanPluralActivation) :
    receipt.futureOnly = true := by
  exact receipt.futureRequired


theorem pluralActivation_does_not_overwrite
    (receipt : ReplanPluralActivation) :
    receipt.memoryOverwrite = false := by
  exact receipt.overwriteForbidden


theorem pluralActivation_does_not_execute
    (receipt : ReplanPluralActivation) :
    receipt.pluralDecisionNotExecution = true := by
  exact receipt.nonExecutionRequired


theorem pluralActivation_consensus_is_not_truth
    (receipt : ReplanPluralActivation) :
    receipt.consensusNotTruth = true := by
  exact receipt.nonTruthRequired


theorem pluralActivation_does_not_grant_host_license
    (receipt : ReplanPluralActivation) :
    receipt.hostLicenseGranted = false := by
  exact receipt.hostLicenseForbidden

end DecisionOS
end KUOS
