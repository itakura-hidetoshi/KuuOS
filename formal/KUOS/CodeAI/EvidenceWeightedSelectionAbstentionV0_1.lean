import Mathlib

namespace KUOS.CodeAI.EvidenceWeightedSelectionAbstentionV0_1

/-- Static admissibility remains a hard eligibility gate. -/
inductive SourceClassification where
  | admissible
  | repairable
  | hold
  | rejected
  deriving DecidableEq, Repr

/-- Independent obligation evidence is recorded without a correctness theorem. -/
inductive EvidenceStatus where
  | allPassed
  | hasFailure
  | incomplete
  deriving DecidableEq, Repr

/-- One deterministic candidate scorecard. -/
structure Scorecard where
  candidateId : String
  sourceClassification : SourceClassification
  evidenceStatus : EvidenceStatus
  evidenceScore : Nat
  maximumEvidenceScore : Nat
  deriving DecidableEq, Repr

/-- Evidence eligibility is stricter than a high raw score. -/
def Eligible (scorecard : Scorecard) : Prop :=
  scorecard.sourceClassification = .admissible ∧
    scorecard.evidenceStatus = .allPassed

/-- A non-admissible source cannot become eligible merely by accumulating score. -/
theorem highScoreCannotOverrideInadmissible
    (scorecard : Scorecard)
    (hClass : scorecard.sourceClassification ≠ .admissible) :
    ¬ Eligible scorecard := by
  intro h
  exact hClass h.1

/-- Failed or incomplete evidence cannot satisfy the all-passed eligibility gate. -/
theorem incompleteEvidenceCannotBecomeEligible
    (scorecard : Scorecard)
    (hEvidence : scorecard.evidenceStatus ≠ .allPassed) :
    ¬ Eligible scorecard := by
  intro h
  exact hEvidence h.2

/-- Abstention reasons are evidence decisions, not rejection effects. -/
inductive AbstentionReason where
  | noEligibleCandidate
  | topScoreBelowThreshold
  | insufficientScoreMargin
  | tiedTopScore
  deriving DecidableEq, Repr

/-- Selection either records one bounded candidate or an explicit abstention. -/
inductive Decision where
  | selected (scorecard : Scorecard)
  | abstained (reason : AbstentionReason)
  deriving DecidableEq, Repr

/-- The receipt owns only a bounded selection decision. -/
structure Receipt where
  scorecards : List Scorecard
  decision : Decision
  rankingPerformed : Bool
  selectionDecisionRecorded : Bool
  selectionAuthorityBoundedToDecision : Bool
  externalEvidenceConsumed : Bool
  testExecutionPerformedByKernel : Bool
  repairExecuted : Bool
  repositoryMutationPerformed : Bool
  gitEffectPerformed : Bool
  verificationAuthorityGranted : Bool
  repairAuthorityGranted : Bool
  executionAuthorityGranted : Bool
  gitAuthorityGranted : Bool
  scoreTreatedAsProbability : Bool
  scoreTreatedAsCorrectnessProof : Bool
  selectionTreatedAsCorrectnessProof : Bool
  abstentionTreatedAsRejection : Bool
  deriving DecidableEq, Repr

/-- Exact selection semantics and downstream no-effect boundaries. -/
structure Receipt.WellFormed (receipt : Receipt) : Prop where
  rankingRecorded : receipt.rankingPerformed = true
  decisionRecorded : receipt.selectionDecisionRecorded = true
  authorityBounded : receipt.selectionAuthorityBoundedToDecision = true
  evidenceConsumed : receipt.externalEvidenceConsumed = true
  selectedEligible :
    ∀ scorecard, receipt.decision = .selected scorecard → Eligible scorecard
  selectedPresent :
    ∀ scorecard, receipt.decision = .selected scorecard →
      scorecard ∈ receipt.scorecards
  noKernelExecution : receipt.testExecutionPerformedByKernel = false
  noRepair : receipt.repairExecuted = false
  noRepositoryMutation : receipt.repositoryMutationPerformed = false
  noGitEffect : receipt.gitEffectPerformed = false
  noVerificationAuthority : receipt.verificationAuthorityGranted = false
  noRepairAuthority : receipt.repairAuthorityGranted = false
  noExecutionAuthority : receipt.executionAuthorityGranted = false
  noGitAuthority : receipt.gitAuthorityGranted = false
  noProbabilityClaim : receipt.scoreTreatedAsProbability = false
  noScoreCorrectnessClaim : receipt.scoreTreatedAsCorrectnessProof = false
  noSelectionCorrectnessClaim :
    receipt.selectionTreatedAsCorrectnessProof = false
  noAbstentionRejection : receipt.abstentionTreatedAsRejection = false

/-- Every selected candidate satisfies the strict evidence eligibility gate. -/
theorem Receipt.WellFormed.selectedCandidateEligible
    {receipt : Receipt} (h : receipt.WellFormed)
    {scorecard : Scorecard}
    (hSelected : receipt.decision = .selected scorecard) :
    Eligible scorecard :=
  h.selectedEligible scorecard hSelected

/-- A selected candidate is one of the preserved scorecards. -/
theorem Receipt.WellFormed.selectedCandidatePreserved
    {receipt : Receipt} (h : receipt.WellFormed)
    {scorecard : Scorecard}
    (hSelected : receipt.decision = .selected scorecard) :
    scorecard ∈ receipt.scorecards :=
  h.selectedPresent scorecard hSelected

/-- Evidence scores are deterministic weights, not probabilities or correctness proofs. -/
theorem Receipt.WellFormed.scoreBoundary
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.scoreTreatedAsProbability = false ∧
      receipt.scoreTreatedAsCorrectnessProof = false ∧
      receipt.selectionTreatedAsCorrectnessProof = false :=
  ⟨h.noProbabilityClaim, h.noScoreCorrectnessClaim,
    h.noSelectionCorrectnessClaim⟩

/-- Abstention records uncertainty without rejecting or deleting a candidate. -/
theorem Receipt.WellFormed.abstentionIsNotRejection
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.abstentionTreatedAsRejection = false :=
  h.noAbstentionRejection

/-- Selection consumes external evidence but performs no test execution itself. -/
theorem Receipt.WellFormed.externalEvidenceBoundary
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.externalEvidenceConsumed = true ∧
      receipt.testExecutionPerformedByKernel = false :=
  ⟨h.evidenceConsumed, h.noKernelExecution⟩

/-- A selection decision grants no verification, repair, execution, or Git authority. -/
theorem Receipt.WellFormed.downstreamAuthorityRemainsSeparate
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.verificationAuthorityGranted = false ∧
      receipt.repairAuthorityGranted = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.gitAuthorityGranted = false :=
  ⟨h.noVerificationAuthority, h.noRepairAuthority,
    h.noExecutionAuthority, h.noGitAuthority⟩

/-- Ranking and selection create no repair, repository, or Git effect. -/
theorem Receipt.WellFormed.effectBoundary
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.rankingPerformed = true ∧
      receipt.selectionDecisionRecorded = true ∧
      receipt.repairExecuted = false ∧
      receipt.repositoryMutationPerformed = false ∧
      receipt.gitEffectPerformed = false :=
  ⟨h.rankingRecorded, h.decisionRecorded, h.noRepair,
    h.noRepositoryMutation, h.noGitEffect⟩

end KUOS.CodeAI.EvidenceWeightedSelectionAbstentionV0_1
