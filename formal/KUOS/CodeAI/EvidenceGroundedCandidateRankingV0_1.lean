import Mathlib

namespace KuuOS.CodeAI.EvidenceGroundedCandidateRankingV0_1

/-! Generic ranking facts are established before the concrete KuuOS receipt. -/

inductive EvidenceClass where
  | admissible
  | repairable
  | held
  | rejected
  deriving DecidableEq, Repr

/-- The fixed routing priority used by the evidence-grounded ranking surface. -/
def classPriority : EvidenceClass → Nat
  | .admissible => 0
  | .repairable => 1
  | .held => 2
  | .rejected => 3

/-- The four evidence classes are strictly ordered by the declared routing priority. -/
theorem classPriority_chain :
    classPriority .admissible < classPriority .repairable ∧
      classPriority .repairable < classPriority .held ∧
      classPriority .held < classPriority .rejected := by
  decide

/-- One-based contiguous positions assigned to a ranking of cardinality `n`. -/
def rankingPositions (n : Nat) : List Nat :=
  (List.range n).map Nat.succ

/-- Generic ranking-position accounting preserves the source candidate cardinality. -/
theorem rankingPositions_length (n : Nat) :
    (rankingPositions n).length = n := by
  simp [rankingPositions]

/-- A deterministic ranking boundary records ordering without downstream authority. -/
structure RankingBoundary where
  rankingPerformed : Bool
  candidateSelected : Bool
  selectionAuthorityGranted : Bool
  verificationRunnerInvoked : Bool
  repairExecuted : Bool
  repositoryMutationPerformed : Bool
  gitEffectPerformed : Bool
  executionAuthorityGranted : Bool
  gitAuthorityGranted : Bool
  rankingTreatedAsCorrectnessProof : Bool
  rankingTreatedAsSelection : Bool
  deriving DecidableEq, Repr

/-- Generic predicate expressing the no-selection and no-effect boundary. -/
def NoDownstreamAuthority (boundary : RankingBoundary) : Prop :=
  boundary.rankingPerformed = true ∧
    boundary.candidateSelected = false ∧
    boundary.selectionAuthorityGranted = false ∧
    boundary.verificationRunnerInvoked = false ∧
    boundary.repairExecuted = false ∧
    boundary.repositoryMutationPerformed = false ∧
    boundary.gitEffectPerformed = false ∧
    boundary.executionAuthorityGranted = false ∧
    boundary.gitAuthorityGranted = false ∧
    boundary.rankingTreatedAsCorrectnessProof = false ∧
    boundary.rankingTreatedAsSelection = false

/-- The concrete KuuOS v0.1 ranking boundary. -/
def kuuOSRankingBoundary : RankingBoundary where
  rankingPerformed := true
  candidateSelected := false
  selectionAuthorityGranted := false
  verificationRunnerInvoked := false
  repairExecuted := false
  repositoryMutationPerformed := false
  gitEffectPerformed := false
  executionAuthorityGranted := false
  gitAuthorityGranted := false
  rankingTreatedAsCorrectnessProof := false
  rankingTreatedAsSelection := false

/-- The concrete KuuOS surface performs ranking and preserves every downstream denial. -/
theorem kuuOSRankingBoundary_noDownstreamAuthority :
    NoDownstreamAuthority kuuOSRankingBoundary := by
  decide

structure ConcreteRankingReceipt where
  sourceCandidateCount : Nat
  orderedCandidateCount : Nat
  positions : List Nat
  admissibleCount : Nat
  repairableCount : Nat
  holdCount : Nat
  rejectedCount : Nat
  deriving DecidableEq, Repr

/-- The committed example has one candidate in each evidence class. -/
def committedRankingReceipt : ConcreteRankingReceipt where
  sourceCandidateCount := 4
  orderedCandidateCount := 4
  positions := rankingPositions 4
  admissibleCount := 1
  repairableCount := 1
  holdCount := 1
  rejectedCount := 1

/-- The concrete ordering neither loses nor creates candidates. -/
theorem committedRankingReceipt_candidateAccounting :
    committedRankingReceipt.orderedCandidateCount =
      committedRankingReceipt.sourceCandidateCount := by
  rfl

/-- The concrete ranking positions are contiguous and cardinality preserving. -/
theorem committedRankingReceipt_positionAccounting :
    committedRankingReceipt.positions.length =
      committedRankingReceipt.sourceCandidateCount := by
  simpa [committedRankingReceipt] using rankingPositions_length 4

/-- The concrete four-way classification accounting equals the ranked cardinality. -/
theorem committedRankingReceipt_classificationAccounting :
    committedRankingReceipt.admissibleCount +
        committedRankingReceipt.repairableCount +
        committedRankingReceipt.holdCount +
        committedRankingReceipt.rejectedCount =
      committedRankingReceipt.orderedCandidateCount := by
  norm_num [committedRankingReceipt]

/-- The committed routing order realizes the generic strict priority chain. -/
theorem committedRankingReceipt_priorityOrder :
    classPriority .admissible < classPriority .repairable ∧
      classPriority .repairable < classPriority .held ∧
      classPriority .held < classPriority .rejected :=
  classPriority_chain

end KuuOS.CodeAI.EvidenceGroundedCandidateRankingV0_1
