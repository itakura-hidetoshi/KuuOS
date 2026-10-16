import Mathlib

namespace KUOS.CodeAI.EvidenceBearingCandidatePortfolioV0_1

/-- The four static-preflight classifications remain distinct in the portfolio. -/
inductive Classification where
  | admissible
  | repairable
  | hold
  | rejected
  deriving DecidableEq, Repr

/-- Generic evidence retained for one candidate before ranking or selection. -/
structure CandidateEvidence where
  candidateId : String
  classification : Classification
  findingCount : Nat
  deriving DecidableEq, Repr

/-- Count exactly one requested classification without changing candidate order. -/
def classificationCount
    (classification : Classification)
    (candidates : List CandidateEvidence) : Nat :=
  (candidates.filter fun candidate => candidate.classification = classification).length

/-- Every candidate belongs to exactly one of the four disjoint classifications. -/
theorem classification_partition (candidates : List CandidateEvidence) :
    classificationCount .admissible candidates +
        classificationCount .repairable candidates +
        classificationCount .hold candidates +
        classificationCount .rejected candidates =
      candidates.length := by
  induction candidates with
  | nil =>
      simp [classificationCount]
  | cons candidate candidates ih =>
      rcases candidate with ⟨candidateId, classification, findingCount⟩
      cases classification <;>
        simp [classificationCount] at ih ⊢ <;>
        omega

/-- Generic classification summary for an evidence-bearing portfolio. -/
structure ClassificationSummary where
  admissible : Nat
  repairable : Nat
  hold : Nat
  rejected : Nat
  total : Nat
  deriving DecidableEq, Repr

/-- Deterministically summarize classifications while retaining the candidate list separately. -/
def summarize (candidates : List CandidateEvidence) : ClassificationSummary where
  admissible := classificationCount .admissible candidates
  repairable := classificationCount .repairable candidates
  hold := classificationCount .hold candidates
  rejected := classificationCount .rejected candidates
  total := candidates.length

/-- The deterministic summary accounts for every candidate exactly once. -/
theorem summarize_partition (candidates : List CandidateEvidence) :
    (summarize candidates).admissible +
        (summarize candidates).repairable +
        (summarize candidates).hold +
        (summarize candidates).rejected =
      (summarize candidates).total := by
  exact classification_partition candidates

/-- Concrete KuuOS portfolio receipt before ranking, selection, or verification. -/
structure Receipt where
  candidates : List CandidateEvidence
  summary : ClassificationSummary
  exactLineageVerified : Bool
  classificationEvidencePreserved : Bool
  findingEvidencePreserved : Bool
  preflightRouteReceiptsPreserved : Bool
  rankingPerformed : Bool
  candidateSelected : Bool
  verificationRunnerInvoked : Bool
  repairExecuted : Bool
  repositoryMutationPerformed : Bool
  executionAuthorityGranted : Bool
  gitAuthorityGranted : Bool
  deriving DecidableEq, Repr

/-- Well-formedness records exact evidence accounting and all no-authority boundaries. -/
structure Receipt.WellFormed (receipt : Receipt) : Prop where
  summaryExact : receipt.summary = summarize receipt.candidates
  exactLineage : receipt.exactLineageVerified = true
  classificationPreserved : receipt.classificationEvidencePreserved = true
  findingsPreserved : receipt.findingEvidencePreserved = true
  routeReceiptsPreserved : receipt.preflightRouteReceiptsPreserved = true
  noRanking : receipt.rankingPerformed = false
  noSelection : receipt.candidateSelected = false
  noVerification : receipt.verificationRunnerInvoked = false
  noRepair : receipt.repairExecuted = false
  noRepositoryMutation : receipt.repositoryMutationPerformed = false
  noExecutionAuthority : receipt.executionAuthorityGranted = false
  noGitAuthority : receipt.gitAuthorityGranted = false

/-- A well-formed portfolio has an exact four-way candidate accounting identity. -/
theorem Receipt.WellFormed.classificationAccounting
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.summary.admissible +
        receipt.summary.repairable +
        receipt.summary.hold +
        receipt.summary.rejected =
      receipt.summary.total := by
  rw [h.summaryExact]
  exact summarize_partition receipt.candidates

/-- Normalization does not assign a candidate rank. -/
theorem Receipt.WellFormed.rankingRemainsSeparate
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.rankingPerformed = false :=
  h.noRanking

/-- Static admissibility evidence does not select a candidate. -/
theorem Receipt.WellFormed.selectionRemainsSeparate
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.candidateSelected = false :=
  h.noSelection

/-- Portfolio normalization does not invoke independent verification. -/
theorem Receipt.WellFormed.verificationRemainsSeparate
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.verificationRunnerInvoked = false :=
  h.noVerification

/-- Repairable evidence remains evidence and is not an executed repair. -/
theorem Receipt.WellFormed.repairRemainsSeparate
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.repairExecuted = false :=
  h.noRepair

/-- Evidence normalization remains read-only with respect to the repository. -/
theorem Receipt.WellFormed.repositoryRemainsReadOnly
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.repositoryMutationPerformed = false :=
  h.noRepositoryMutation

/-- A portfolio receipt cannot grant execution authority. -/
theorem Receipt.WellFormed.executionAuthorityRemainsSeparate
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.executionAuthorityGranted = false :=
  h.noExecutionAuthority

/-- A portfolio receipt cannot grant Git authority. -/
theorem Receipt.WellFormed.gitAuthorityRemainsSeparate
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.gitAuthorityGranted = false :=
  h.noGitAuthority

/-- Exact lineage and preserved findings are jointly recorded without authority escalation. -/
theorem Receipt.WellFormed.evidencePreservedWithoutSelection
    {receipt : Receipt} (h : receipt.WellFormed) :
    receipt.exactLineageVerified = true ∧
      receipt.classificationEvidencePreserved = true ∧
      receipt.findingEvidencePreserved = true ∧
      receipt.candidateSelected = false :=
  ⟨h.exactLineage, h.classificationPreserved, h.findingsPreserved, h.noSelection⟩

end KUOS.CodeAI.EvidenceBearingCandidatePortfolioV0_1
